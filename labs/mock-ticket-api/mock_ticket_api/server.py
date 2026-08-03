# SPDX-License-Identifier: MIT
"""只面向本机隔离培训环境的合成工单 HTTP API。"""

from __future__ import annotations

import argparse
import copy
import hashlib
import ipaddress
import json
import re
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Final, cast
from urllib.parse import unquote, urlsplit

LOOPBACK_HOST: Final = "127.0.0.1"
DEMO_WRITE_HEADER: Final = "X-FlowAgentic-Demo"
DEMO_WRITE_VALUE: Final = "synthetic-training-write"
IDEMPOTENCY_HEADER: Final = "Idempotency-Key"
MAX_BODY_BYTES: Final = 16 * 1024

_TICKET_ID_PATTERN = re.compile(r"^TKT-[0-9]{4}$")
_IDEMPOTENCY_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
_ALLOWED_PRIORITIES = frozenset({"低", "中", "高", "紧急"})
_TICKET_FIELDS = frozenset(
    {
        "ticket_id",
        "customer",
        "subject",
        "category",
        "priority",
        "status",
        "description",
        "contains_personal_data",
    }
)
_TICKET_STRING_FIELDS = _TICKET_FIELDS - {"contains_personal_data"}

# Fixture validation deliberately duplicates a small, dependency-free subset
# of the public-site safety scanner.  The lab can therefore run with the Python
# standard library alone while still failing closed before serving any string.
_EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b", re.IGNORECASE),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", re.IGNORECASE),
    re.compile(r"(?i)\bbearer\s*[:=]?\s*[A-Za-z0-9._~+/=-]{12,}\b"),
    re.compile(
        r"(?i)\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|"
        r"password|passwd|client[_ -]?secret|authorization|cookie|set-cookie)"
        r"\s*[:=]\s*['\"]?(?:bearer\s+)?[^\s'\"<{][^\s'\"]{3,}"
    ),
    re.compile(r"(?i)\b(?:[0-9a-f]{32,}|[A-Za-z0-9_-]{40,})\b"),
)
_LOCAL_PATH_PATTERNS = (
    re.compile(r"(?i)\bfile://"),
    re.compile(r"/(?:Users|home|private|var|etc|opt|tmp)/[^\s]*"),
    re.compile(r"(?i)\b[A-Z]:\\(?:[^\\\s]+\\)*[^\\\s]*"),
    re.compile(r"\\\\[^\\\s]+\\[^\s]+"),
)
_URL_PATTERN = re.compile(r"(?i)\bhttps?://[^\s<>'\"，。；]+")
_INTERNAL_HOST_PATTERN = re.compile(
    r"(?i)(?:^|\b)(?:localhost|[a-z0-9-]+(?:\.[a-z0-9-]+)*\."
    r"(?:internal|intranet|corp|lan|local))(?:\b|$)"
)
_IPV4_PATTERN = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
_IPV6_CANDIDATE_PATTERN = re.compile(r"(?<![0-9A-Fa-f:])[0-9A-Fa-f:]{2,}(?![0-9A-Fa-f:])")


def default_fixture_path() -> Path:
    """返回仓库内合成工单 fixture 的默认位置。"""

    return (
        Path(__file__).resolve().parents[3]
        / "data"
        / "fixtures"
        / "tickets"
        / "tickets.json"
    )


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _meta(**extra: Any) -> dict[str, Any]:
    return {"synthetic_data": True, **extra}


def _error(
    code: str,
    message: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        },
        "meta": _meta(),
    }
    if details:
        payload["error"]["details"] = details
    return payload


def _fixture_string_violation(value: str) -> str | None:
    """Classify unsafe public fixture text without returning the matched value."""

    if any(ord(character) < 32 and character not in "\t\n\r" for character in value):
        return "control character"
    if _EMAIL_PATTERN.search(value):
        return "email"
    if any(pattern.search(value) for pattern in _SECRET_PATTERNS):
        return "credential or token"
    if any(pattern.search(value) for pattern in _LOCAL_PATH_PATTERNS):
        return "local path"
    if _INTERNAL_HOST_PATTERN.search(value):
        return "internal hostname"

    for match in _URL_PATTERN.finditer(value):
        parsed = urlsplit(match.group(0))
        if parsed.username is not None or parsed.password is not None:
            return "credential-bearing URL"
        hostname = parsed.hostname
        if hostname is None:
            return "invalid URL"
        if _INTERNAL_HOST_PATTERN.search(hostname):
            return "internal URL"
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            pass
        else:
            # Literal addresses are unnecessary in a synthetic public fixture
            # and can reveal infrastructure even when globally routable.
            return "IP literal URL"

    if _IPV4_PATTERN.search(value):
        return "IP literal"
    for match in _IPV6_CANDIDATE_PATTERN.finditer(value):
        candidate = match.group(0)
        if candidate.count(":") < 2:
            continue
        try:
            ipaddress.ip_address(candidate)
        except ValueError:
            continue
        return "IP literal"
    return None


def _load_fixture(path: Path) -> dict[str, dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"找不到合成工单 fixture：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"合成工单 fixture 不是有效 JSON：{path}") from exc

    if not isinstance(raw, list) or not raw:
        raise ValueError("合成工单 fixture 必须是非空数组")

    tickets: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"fixture 第 {index + 1} 项必须是对象")
        missing = sorted(_TICKET_FIELDS - set(item))
        if missing:
            raise ValueError(f"fixture 第 {index + 1} 项缺少字段：{', '.join(missing)}")
        unexpected = sorted(set(item) - _TICKET_FIELDS)
        if unexpected:
            raise ValueError(
                f"fixture 第 {index + 1} 项包含未定义字段：{', '.join(unexpected)}"
            )
        for field in sorted(_TICKET_STRING_FIELDS):
            value = item[field]
            if not isinstance(value, str):
                raise ValueError(f"fixture 第 {index + 1} 项 {field} 必须是字符串")
            violation = _fixture_string_violation(value)
            if violation is not None:
                raise ValueError(
                    f"fixture 第 {index + 1} 项 {field} 未通过公开安全校验（{violation}）"
                )
        ticket_id = item["ticket_id"]
        if not _TICKET_ID_PATTERN.fullmatch(ticket_id):
            raise ValueError(f"fixture 第 {index + 1} 项 ticket_id 格式无效")
        if ticket_id in tickets:
            raise ValueError(f"fixture 存在重复 ticket_id：{ticket_id}")
        if item["contains_personal_data"] is not False:
            raise ValueError(f"fixture {ticket_id} 未明确声明为无个人数据")
        if item["priority"] not in _ALLOWED_PRIORITIES:
            raise ValueError(f"fixture {ticket_id} 的 priority 不在允许列表")
        ticket = copy.deepcopy(item)
        ticket["revision"] = 0
        tickets[ticket_id] = ticket
    return tickets


@dataclass(frozen=True)
class StoredResponse:
    generation: int
    fingerprint: str
    status: int
    payload: dict[str, Any]


class SlidingWindowLimiter:
    """线程安全的进程内滑动窗口限流器。"""

    def __init__(self, limit: int, window_seconds: float) -> None:
        if limit < 1:
            raise ValueError("rate_limit 必须大于 0")
        if window_seconds <= 0:
            raise ValueError("rate_window 必须大于 0")
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: defaultdict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> tuple[bool, int]:
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= self.limit:
                retry_after = max(1, int(self.window_seconds - (now - events[0]) + 0.999))
                return False, retry_after
            events.append(now)
            return True, 0


class MockTicketApplication:
    """保存合成工单、幂等回执和限流状态的进程内应用。"""

    def __init__(
        self,
        fixture_path: Path | None = None,
        *,
        rate_limit: int = 60,
        rate_window: float = 60.0,
    ) -> None:
        self.fixture_path = (fixture_path or default_fixture_path()).resolve()
        self._initial_tickets = _load_fixture(self.fixture_path)
        self._tickets = copy.deepcopy(self._initial_tickets)
        self._idempotency: dict[str, StoredResponse] = {}
        self._generation = 1
        self._lock = threading.RLock()
        self.rate_limiter = SlidingWindowLimiter(rate_limit, rate_window)

    @property
    def ticket_count(self) -> int:
        with self._lock:
            return len(self._tickets)

    @property
    def generation(self) -> int:
        with self._lock:
            return self._generation

    def get_ticket(self, ticket_id: str) -> dict[str, Any] | None:
        ticket, _ = self.get_ticket_snapshot(ticket_id)
        return ticket

    def get_ticket_snapshot(
        self,
        ticket_id: str,
    ) -> tuple[dict[str, Any] | None, int]:
        """Return ticket state and generation from one lock-protected snapshot."""

        with self._lock:
            ticket = self._tickets.get(ticket_id)
            snapshot = copy.deepcopy(ticket) if ticket is not None else None
            return snapshot, self._generation

    def _fingerprint(self, operation: str, body: dict[str, Any]) -> str:
        canonical = json.dumps(
            {"operation": operation, "body": body},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def update_classification(
        self,
        ticket_id: str,
        body: dict[str, Any],
        idempotency_key: str,
    ) -> tuple[int, dict[str, Any], bool]:
        operation = f"PUT:/tickets/{ticket_id}/classification"
        fingerprint = self._fingerprint(operation, body)
        with self._lock:
            stored = self._idempotency.get(idempotency_key)
            if stored is not None:
                # A receipt is valid only for the fixture generation that
                # produced it. ``reset`` also clears the cache, while this
                # marker keeps stale entries fail-safe if cache maintenance is
                # ever changed independently.
                if stored.generation != self._generation:
                    del self._idempotency[idempotency_key]
                    stored = None
            if stored is not None:
                if stored.fingerprint != fingerprint:
                    return (
                        HTTPStatus.CONFLICT,
                        _error(
                            "IDEMPOTENCY_KEY_REUSED",
                            "同一幂等键不能用于不同请求。",
                            details={"idempotency_key": idempotency_key},
                        ),
                        False,
                    )
                return stored.status, copy.deepcopy(stored.payload), True

            ticket = self._tickets.get(ticket_id)
            if ticket is None:
                return (
                    HTTPStatus.NOT_FOUND,
                    _error("TICKET_NOT_FOUND", "未找到指定的合成工单。"),
                    False,
                )

            expected_revision = body.get("expected_revision")
            if (
                expected_revision is not None
                and expected_revision != ticket["revision"]
            ):
                return (
                    HTTPStatus.CONFLICT,
                    _error(
                        "REVISION_CONFLICT",
                        "工单版本已变化，请重新读取后再提交。",
                        details={
                            "expected_revision": expected_revision,
                            "current_revision": ticket["revision"],
                        },
                    ),
                    False,
                )

            changed = False
            for field in ("category", "priority"):
                if field in body and ticket[field] != body[field]:
                    ticket[field] = body[field]
                    changed = True
            if (
                "reason" in body
                and ticket.get("classification_reason") != body["reason"]
            ):
                ticket["classification_reason"] = body["reason"]
                changed = True
            if changed:
                ticket["revision"] += 1
                ticket["classification_updated_at"] = _utc_now()

            payload = {
                "data": copy.deepcopy(ticket),
                "meta": _meta(
                    changed=changed,
                    idempotency_key=idempotency_key,
                    generation=self._generation,
                ),
            }
            self._idempotency[idempotency_key] = StoredResponse(
                generation=self._generation,
                fingerprint=fingerprint,
                status=HTTPStatus.OK,
                payload=copy.deepcopy(payload),
            )
            return HTTPStatus.OK, payload, False

    def reset(
        self,
        body: dict[str, Any],
        idempotency_key: str,
    ) -> tuple[int, dict[str, Any], bool]:
        operation = "POST:/reset"
        fingerprint = self._fingerprint(operation, body)
        with self._lock:
            stored = self._idempotency.get(idempotency_key)
            if stored is not None:
                if stored.generation != self._generation:
                    del self._idempotency[idempotency_key]
                    stored = None
            if stored is not None:
                if stored.fingerprint != fingerprint:
                    return (
                        HTTPStatus.CONFLICT,
                        _error(
                            "IDEMPOTENCY_KEY_REUSED",
                            "同一幂等键不能用于不同请求。",
                            details={"idempotency_key": idempotency_key},
                        ),
                        False,
                    )
                return stored.status, copy.deepcopy(stored.payload), True

            self._tickets = copy.deepcopy(self._initial_tickets)
            self._generation += 1
            # Reset is a new fixture generation. Responses from the prior
            # generation must never be replayed into the new state. Keep only
            # the new reset receipt (stored below) so an immediate retry of
            # this reset remains idempotent.
            self._idempotency.clear()
            payload = {
                "data": {
                    "reset": True,
                    "ticket_count": len(self._tickets),
                    "generation": self._generation,
                },
                "meta": _meta(idempotency_key=idempotency_key),
            }
            self._idempotency[idempotency_key] = StoredResponse(
                generation=self._generation,
                fingerprint=fingerprint,
                status=HTTPStatus.OK,
                payload=copy.deepcopy(payload),
            )
            return HTTPStatus.OK, payload, False


class LocalOnlyThreadingHTTPServer(ThreadingHTTPServer):
    """携带应用状态且强制绑定 IPv4 loopback 的 HTTP 服务。"""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler],
        application: MockTicketApplication,
    ) -> None:
        host, _ = server_address
        if host != LOOPBACK_HOST:
            raise ValueError(f"训练 API 只允许绑定 {LOOPBACK_HOST}")
        self.application = application
        super().__init__(server_address, handler_class)


class MockTicketRequestHandler(BaseHTTPRequestHandler):
    """合成工单 API 请求处理器。"""

    protocol_version = "HTTP/1.1"
    server_version = "FlowAgenticTrainingAPI/1.0"
    sys_version = ""

    @property
    def application(self) -> MockTicketApplication:
        return cast(LocalOnlyThreadingHTTPServer, self.server).application

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        status = str(args[1]) if len(args) > 1 else "unknown"
        print(
            json.dumps(
                {
                    "timestamp": _utc_now(),
                    "event": "http_request",
                    "client": self.client_address[0],
                    "method": self.command,
                    "path": self._path(),
                    "status": status,
                    "synthetic_data": True,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    def _send_json(
        self,
        status: int,
        payload: dict[str, Any],
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        body = _json_bytes(payload)
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Synthetic-Data", "true")
        self.send_header("Connection", "close")
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True

    def _path(self) -> str:
        return unquote(urlsplit(self.path).path)

    def _rate_limit_write(self) -> bool:
        allowed, retry_after = self.application.rate_limiter.check(
            f"{self.client_address[0]}:write"
        )
        if allowed:
            return True
        self._send_json(
            HTTPStatus.TOO_MANY_REQUESTS,
            _error(
                "RATE_LIMITED",
                "培训写入请求过于频繁，请稍后重试。",
                details={
                    "limit": self.application.rate_limiter.limit,
                    "window_seconds": self.application.rate_limiter.window_seconds,
                },
            ),
            extra_headers={"Retry-After": str(retry_after)},
        )
        return False

    def _validate_write_headers(self) -> str | None:
        if self.headers.get(DEMO_WRITE_HEADER) != DEMO_WRITE_VALUE:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error(
                    "DEMO_WRITE_HEADER_REQUIRED",
                    f"写操作必须携带公开培训标头 {DEMO_WRITE_HEADER}。",
                    details={"expected_value": DEMO_WRITE_VALUE},
                ),
            )
            return None
        key = self.headers.get(IDEMPOTENCY_HEADER, "")
        if not _IDEMPOTENCY_KEY_PATTERN.fullmatch(key):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error(
                    "INVALID_IDEMPOTENCY_KEY",
                    "Idempotency-Key 必须为 8–128 位字母、数字或 . _ : -。",
                ),
            )
            return None
        return key

    def _read_json_object(self) -> dict[str, Any] | None:
        if self.headers.get_content_type() != "application/json":
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error("INVALID_CONTENT_TYPE", "请求体必须使用 application/json。"),
            )
            return None
        raw_length = self.headers.get("Content-Length")
        try:
            length = int(raw_length or "")
        except ValueError:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error("INVALID_CONTENT_LENGTH", "Content-Length 无效。"),
            )
            return None
        if length < 0 or length > MAX_BODY_BYTES:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error(
                    "BODY_SIZE_INVALID",
                    f"请求体必须在 0–{MAX_BODY_BYTES} 字节内。",
                ),
            )
            return None
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error("INVALID_JSON", "请求体不是有效的 UTF-8 JSON。"),
            )
            return None
        if not isinstance(payload, dict):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error("INVALID_BODY", "请求体必须是 JSON 对象。"),
            )
            return None
        return payload

    def _ticket_id_from_classification_path(self) -> str | None:
        match = re.fullmatch(r"/tickets/([^/]+)/classification", self._path())
        if match is None:
            return None
        return match.group(1)

    def _ticket_id_from_get_path(self) -> str | None:
        match = re.fullmatch(r"/tickets/([^/]+)", self._path())
        if match is None:
            return None
        return match.group(1)

    def _validate_ticket_id(self, ticket_id: str) -> bool:
        if _TICKET_ID_PATTERN.fullmatch(ticket_id):
            return True
        self._send_json(
            HTTPStatus.BAD_REQUEST,
            _error(
                "INVALID_TICKET_ID",
                "工单编号必须符合 TKT-0000 格式。",
            ),
        )
        return False

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = self._path()
        if path == "/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "data": {
                        "status": "ok",
                        "service": "flowagentic-mock-ticket-api",
                        "ticket_count": self.application.ticket_count,
                        "generation": self.application.generation,
                        "bound_host": LOOPBACK_HOST,
                    },
                    "meta": _meta(),
                },
            )
            return

        ticket_id = self._ticket_id_from_get_path()
        if ticket_id is None:
            self._send_json(
                HTTPStatus.NOT_FOUND,
                _error("ROUTE_NOT_FOUND", "未找到请求的培训 API 路由。"),
            )
            return
        if not self._validate_ticket_id(ticket_id):
            return
        ticket, generation = self.application.get_ticket_snapshot(ticket_id)
        if ticket is None:
            self._send_json(
                HTTPStatus.NOT_FOUND,
                _error("TICKET_NOT_FOUND", "未找到指定的合成工单。"),
            )
            return
        self._send_json(
            HTTPStatus.OK,
            {
                "data": ticket,
                "meta": _meta(generation=generation),
            },
        )

    def do_PUT(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        ticket_id = self._ticket_id_from_classification_path()
        if ticket_id is None:
            self._send_json(
                HTTPStatus.NOT_FOUND,
                _error("ROUTE_NOT_FOUND", "未找到请求的培训 API 路由。"),
            )
            return
        if not self._validate_ticket_id(ticket_id):
            return
        if not self._rate_limit_write():
            return
        idempotency_key = self._validate_write_headers()
        if idempotency_key is None:
            return
        body = self._read_json_object()
        if body is None:
            return
        validation_error = self._validate_classification_body(body)
        if validation_error is not None:
            self._send_json(HTTPStatus.BAD_REQUEST, validation_error)
            return
        status, payload, replayed = self.application.update_classification(
            ticket_id,
            body,
            idempotency_key,
        )
        headers = {"Idempotent-Replayed": "true"} if replayed else None
        self._send_json(status, payload, extra_headers=headers)

    def _validate_classification_body(
        self,
        body: dict[str, Any],
    ) -> dict[str, Any] | None:
        allowed_fields = {"category", "priority", "reason", "expected_revision"}
        unexpected = sorted(set(body) - allowed_fields)
        if unexpected:
            return _error(
                "UNKNOWN_FIELDS",
                "请求包含未支持的字段。",
                details={"fields": unexpected},
            )
        if "category" not in body:
            return _error("CATEGORY_REQUIRED", "category 为必填字段。")
        category = body["category"]
        if not isinstance(category, str) or not 1 <= len(category.strip()) <= 40:
            return _error("INVALID_CATEGORY", "category 必须是 1–40 个字符的字符串。")
        body["category"] = category.strip()
        if "priority" in body and body["priority"] not in _ALLOWED_PRIORITIES:
            return _error(
                "INVALID_PRIORITY",
                "priority 必须是低、中、高或紧急。",
            )
        if "reason" in body:
            reason = body["reason"]
            if not isinstance(reason, str) or len(reason.strip()) > 200:
                return _error("INVALID_REASON", "reason 必须是不超过 200 个字符的字符串。")
            body["reason"] = reason.strip()
        if "expected_revision" in body:
            revision = body["expected_revision"]
            if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
                return _error(
                    "INVALID_EXPECTED_REVISION",
                    "expected_revision 必须是非负整数。",
                )
        return None

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self._path() != "/reset":
            self._send_json(
                HTTPStatus.NOT_FOUND,
                _error("ROUTE_NOT_FOUND", "未找到请求的培训 API 路由。"),
            )
            return
        if not self._rate_limit_write():
            return
        idempotency_key = self._validate_write_headers()
        if idempotency_key is None:
            return
        body = self._read_json_object()
        if body is None:
            return
        if body:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error("RESET_BODY_NOT_EMPTY", "重置请求体必须是空 JSON 对象。"),
            )
            return
        status, payload, replayed = self.application.reset(
            body,
            idempotency_key,
        )
        headers = {"Idempotent-Replayed": "true"} if replayed else None
        self._send_json(status, payload, extra_headers=headers)


def create_server(
    *,
    host: str = LOOPBACK_HOST,
    port: int = 8765,
    fixture_path: Path | None = None,
    rate_limit: int = 60,
    rate_window: float = 60.0,
) -> LocalOnlyThreadingHTTPServer:
    """创建只绑定本机 IPv4 loopback 的测试服务器。"""

    application = MockTicketApplication(
        fixture_path,
        rate_limit=rate_limit,
        rate_window=rate_window,
    )
    return LocalOnlyThreadingHTTPServer(
        (host, port),
        MockTicketRequestHandler,
        application,
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="启动仅监听 127.0.0.1 的 FlowAgentic 合成工单培训 API。"
    )
    parser.add_argument("--port", type=int, default=8765, help="监听端口，默认 8765")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=default_fixture_path(),
        help="合成工单 JSON fixture 路径",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=60,
        help="单个滑动窗口内允许的写请求数，默认 60",
    )
    parser.add_argument(
        "--rate-window",
        type=float,
        default=60.0,
        help="限流滑动窗口秒数，默认 60",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if not 1 <= args.port <= 65535:
        raise SystemExit("--port 必须在 1–65535 之间")
    server = create_server(
        port=args.port,
        fixture_path=args.fixture,
        rate_limit=args.rate_limit,
        rate_window=args.rate_window,
    )
    print(
        json.dumps(
            {
                "event": "server_started",
                "url": f"http://{LOOPBACK_HOST}:{server.server_port}",
                "fixture": str(args.fixture.resolve()),
                "synthetic_data": True,
                "warning": "公开演示标头不是身份认证；禁止用于生产。",
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
