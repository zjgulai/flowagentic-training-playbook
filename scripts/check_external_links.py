#!/usr/bin/env python3
"""Check public HTTP links without granting the build runner SSRF access.

The checker deliberately does not use ``urllib.request.urlopen`` (or ambient
proxy configuration).  Every request and redirect target is resolved, every
resolved address must be globally routable, and the socket is connected to one
of those already-validated addresses while retaining the original Host header
and TLS SNI name.  This closes the usual redirect, proxy, and DNS-rebinding
paths into loopback or private infrastructure.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import http.client
import ipaddress
import json
import re
import socket
import ssl
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s<>\"'`\])}]+")
SCAN_ROOTS = ("docs", "research")
IGNORED_HOST_SUFFIXES = (".invalid", ".example")
ALLOWED_SCHEMES = frozenset({"http", "https"})
LOCAL_HOST_SUFFIXES = (
    "localhost",
    "local",
    "localdomain",
    "internal",
    "lan",
    "home",
    "home.arpa",
)
HEAD_FALLBACK_STATUSES = frozenset({400, 401, 403, 405, 429, 501})
REACHABLE_RESTRICTED_STATUSES = frozenset({401, 403, 429})
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
DEFAULT_MAX_REDIRECTS = 5


class URLPolicyError(ValueError):
    """A URL or one of its resolved destinations violates the public-only policy."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class RedirectLimitError(RuntimeError):
    """The manual redirect budget was exhausted."""


@dataclass(frozen=True)
class ResolvedTarget:
    """A validated URL plus IPs captured in the same resolution operation."""

    url: str
    scheme: str
    host: str
    port: int
    host_header: str
    request_target: str
    addresses: tuple[str, ...]


@dataclass(frozen=True)
class LinkResponse:
    status: int
    headers: Mapping[str, str]


Resolver = Callable[[str, int], Sequence[str]]
Transport = Callable[[ResolvedTarget, str, Mapping[str, str], float, str], LinkResponse]


def collect_urls() -> list[str]:
    urls: set[str] = set()
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".yml", ".yaml", ".json"}:
                continue
            for url in URL_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
                clean = url.rstrip(".,;:")
                try:
                    host = urllib.parse.urlsplit(clean).hostname or ""
                except ValueError:
                    host = ""
                if any(host.lower().rstrip(".").endswith(suffix) for suffix in IGNORED_HOST_SUFFIXES):
                    continue
                urls.add(clean)
    return sorted(urls)


def _display_url(url: str) -> str:
    """Return a printable URL that never includes userinfo, query values, or fragments."""

    try:
        parsed = urllib.parse.urlsplit(url)
        host = parsed.hostname or "<invalid-host>"
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        try:
            port = parsed.port
        except ValueError:
            port = None
        netloc = f"{host}:{port}" if port is not None else host
        query = "<redacted>" if parsed.query else ""
        return urllib.parse.urlunsplit((parsed.scheme or "<invalid-scheme>", netloc, parsed.path, query, ""))
    except (TypeError, ValueError):
        return "<redacted-url>"


def _normalise_host(host: str) -> str:
    host = host.rstrip(".")
    if not host or "%" in host:
        raise URLPolicyError("invalid-host")
    try:
        return str(ipaddress.ip_address(host))
    except ValueError:
        try:
            normalised = host.encode("idna").decode("ascii").lower()
        except UnicodeError as exc:
            raise URLPolicyError("invalid-host") from exc
        if not normalised or len(normalised) > 253:
            raise URLPolicyError("invalid-host")
        return normalised


def _is_local_hostname(host: str) -> bool:
    return any(host == suffix or host.endswith(f".{suffix}") for suffix in LOCAL_HOST_SUFFIXES)


def _validated_ip(address: str) -> str:
    if "%" in address:
        raise URLPolicyError("non-public-address")
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError as exc:
        raise URLPolicyError("invalid-resolved-address") from exc
    if isinstance(parsed, ipaddress.IPv6Address) and parsed.ipv4_mapped is not None:
        policy_address: ipaddress.IPv4Address | ipaddress.IPv6Address = parsed.ipv4_mapped
    else:
        policy_address = parsed
    # is_global is intentionally stricter than checking only is_private: it
    # also rejects loopback, link-local, multicast, reserved, unspecified,
    # documentation, and shared carrier-grade NAT ranges.
    if not policy_address.is_global:
        raise URLPolicyError("non-public-address")
    return str(parsed)


def _system_resolver(host: str, port: int) -> Sequence[str]:
    results = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    return tuple(
        address
        for item in results
        if isinstance((address := item[4][0]), str)
    )


def _resolve_target(url: str, resolver: Resolver = _system_resolver) -> ResolvedTarget:
    if any(ord(char) < 0x20 or char.isspace() for char in url):
        raise URLPolicyError("invalid-url")
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise URLPolicyError("invalid-url") from exc
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise URLPolicyError("scheme-not-allowed")
    if parsed.username is not None or parsed.password is not None or "@" in parsed.netloc:
        raise URLPolicyError("userinfo-not-allowed")
    if not parsed.hostname:
        raise URLPolicyError("missing-host")
    host = _normalise_host(parsed.hostname)
    if _is_local_hostname(host):
        raise URLPolicyError("local-hostname")
    try:
        port = parsed.port or (443 if scheme == "https" else 80)
    except ValueError as exc:
        raise URLPolicyError("invalid-port") from exc
    if not 1 <= port <= 65535:
        raise URLPolicyError("invalid-port")

    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        try:
            resolved = tuple(resolver(host, port))
        except (OSError, socket.gaierror) as exc:
            raise URLPolicyError("dns-resolution-failed") from exc
    else:
        resolved = (str(literal),)
    if not resolved:
        raise URLPolicyError("dns-resolution-empty")

    # Fail closed if *any* DNS answer is non-public.  Selecting only a public
    # answer from a mixed public/private set would leave rebinding ambiguity.
    addresses = tuple(dict.fromkeys(_validated_ip(address) for address in resolved))
    default_port = 443 if scheme == "https" else 80
    host_for_header = f"[{host}]" if ":" in host else host
    host_header = host_for_header if port == default_port else f"{host_for_header}:{port}"
    path = parsed.path or "/"
    request_target = urllib.parse.urlunsplit(("", "", path, parsed.query, ""))
    canonical_url = urllib.parse.urlunsplit((scheme, host_header, path, parsed.query, ""))
    return ResolvedTarget(
        url=canonical_url,
        scheme=scheme,
        host=host,
        port=port,
        host_header=host_header,
        request_target=request_target,
        addresses=addresses,
    )


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float) -> None:
        self._pinned_ip = pinned_ip
        super().__init__(host=host, port=port, timeout=timeout)

    def connect(self) -> None:
        # This transport never supports proxies or CONNECT tunnels: the socket
        # destination is exactly the public address validated for this request.
        self.sock = socket.create_connection((self._pinned_ip, self.port), self.timeout)


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float) -> None:
        self._pinned_ip = pinned_ip
        self._tls_context = ssl.create_default_context()
        super().__init__(host=host, port=port, timeout=timeout, context=self._tls_context)

    def connect(self) -> None:
        # As above, no proxy/tunnel path is available.  TLS verification and
        # SNI retain the original host even though the destination IP is pinned.
        raw_socket = socket.create_connection((self._pinned_ip, self.port), self.timeout)
        # The socket destination stays pinned to the validated IP, while
        # certificate verification and SNI use the original URL hostname.
        self.sock = self._tls_context.wrap_socket(raw_socket, server_hostname=self.host)


def _pinned_transport(
    target: ResolvedTarget,
    method: str,
    headers: Mapping[str, str],
    timeout: float,
    pinned_ip: str,
) -> LinkResponse:
    connection_type = _PinnedHTTPSConnection if target.scheme == "https" else _PinnedHTTPConnection
    connection = connection_type(target.host, target.port, pinned_ip, timeout)
    try:
        request_headers = dict(headers)
        request_headers["Host"] = target.host_header
        connection.request(method, target.request_target, headers=request_headers)
        response = connection.getresponse()
        return LinkResponse(
            status=int(response.status),
            headers={key.lower(): value for key, value in response.getheaders()},
        )
    finally:
        connection.close()


def _request_following_redirects(
    url: str,
    method: str,
    timeout: float,
    headers: Mapping[str, str],
    *,
    resolver: Resolver,
    transport: Transport,
    max_redirects: int,
) -> int:
    current_url = url
    for redirect_count in range(max_redirects + 1):
        # Resolution is repeated for every hop (and every retry), then the
        # connection is pinned to an address from this exact result set.
        target = _resolve_target(current_url, resolver)
        response = transport(target, method, headers, timeout, target.addresses[0])
        if response.status not in REDIRECT_STATUSES:
            return response.status
        location = next(
            (value for key, value in response.headers.items() if key.lower() == "location"),
            None,
        )
        if not location:
            return response.status
        if redirect_count >= max_redirects:
            raise RedirectLimitError
        current_url = urllib.parse.urljoin(target.url, location)
    raise RedirectLimitError  # pragma: no cover - loop is exhaustive


def request(
    url: str,
    timeout: float,
    *,
    resolver: Resolver = _system_resolver,
    transport: Transport = _pinned_transport,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
) -> tuple[int | None, str]:
    headers = {
        "User-Agent": "FlowAgentic-Playbook-Link-Checker/2.0",
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Connection": "close",
    }
    last_note = "no response"
    for method in ("HEAD", "GET"):
        try:
            status = _request_following_redirects(
                url,
                method,
                timeout,
                headers,
                resolver=resolver,
                transport=transport,
                max_redirects=max_redirects,
            )
        except URLPolicyError as exc:
            return None, f"blocked by URL policy ({exc.code})"
        except RedirectLimitError:
            return None, "redirect limit exceeded"
        except Exception as exc:  # network failures are expected and must be redacted
            last_note = f"network error ({type(exc).__name__})"
            if method == "HEAD":
                continue
            return None, last_note

        if method == "HEAD" and status in HEAD_FALLBACK_STATUSES:
            continue
        if status in REACHABLE_RESTRICTED_STATUSES:
            return status, "reachable but access-controlled or rate-limited"
        return status, ""
    return None, last_note


def check(
    url: str,
    timeout: float,
    retries: int,
    *,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
) -> dict[str, object]:
    last_status: int | None = None
    last_error = ""
    for attempt in range(retries + 1):
        last_status, last_error = request(url, timeout, max_redirects=max_redirects)
        if last_status and (
            200 <= last_status < 400 or last_status in REACHABLE_RESTRICTED_STATUSES
        ):
            return {
                "url": _display_url(url),
                "status": last_status,
                "ok": True,
                "note": last_error,
            }
        if attempt < retries:
            time.sleep(0.5 * (attempt + 1))
    return {
        "url": _display_url(url),
        "status": last_status,
        "ok": False,
        "note": last_error,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=12)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-redirects", type=int, default=DEFAULT_MAX_REDIRECTS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.timeout <= 0 or args.retries < 0 or args.workers < 1 or args.max_redirects < 0:
        parser.error("timeout/workers must be positive; retries/max-redirects cannot be negative")
    urls = collect_urls()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(
            executor.map(
                lambda url: check(
                    url,
                    args.timeout,
                    args.retries,
                    max_redirects=args.max_redirects,
                ),
                urls,
            )
        )
    failures = [item for item in results if not item["ok"]]
    if args.json:
        print(json.dumps({"checked": len(urls), "failures": failures}, ensure_ascii=False, indent=2))
    else:
        for item in failures:
            print(f"ERROR: {item['url']} -> {item['status']} {item['note']}")
        print(f"external links: {len(urls)} checked, {len(failures)} failed")
    return 1 if failures else 0
if __name__ == "__main__":
    raise SystemExit(main())
