# SPDX-License-Identifier: MIT
"""合成工单培训 API 的端到端 HTTP 测试。"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from unittest import mock

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from mock_ticket_api.server import (  # noqa: E402
    DEMO_WRITE_HEADER,
    DEMO_WRITE_VALUE,
    MockTicketApplication,
    create_server,
    default_fixture_path,
)


class ServerHarness:
    def __init__(self, *, rate_limit: int = 60) -> None:
        self.server = create_server(port=0, rate_limit=rate_limit, rate_window=60)
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            name="mock-ticket-api-test",
            daemon=True,
        )

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_port}"

    def __enter__(self) -> "ServerHarness":
        self.thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, Any], dict[str, str]]:
        encoded = None if body is None else json.dumps(body).encode("utf-8")
        request_headers = dict(headers or {})
        if body is not None:
            request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=encoded,
            headers=request_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                return (
                    response.status,
                    json.loads(response.read()),
                    dict(response.headers.items()),
                )
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read()), dict(exc.headers.items())


def write_headers(key: str) -> dict[str, str]:
    return {
        DEMO_WRITE_HEADER: DEMO_WRITE_VALUE,
        "Idempotency-Key": key,
    }


class MockTicketApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = ServerHarness()
        self.harness.__enter__()

    def tearDown(self) -> None:
        self.harness.__exit__(None, None, None)

    def assert_fixture_rejected(
        self,
        item: dict[str, Any],
        message_pattern: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture_path = Path(directory) / "tickets.json"
            fixture_path.write_text(
                json.dumps([item], ensure_ascii=False),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, message_pattern):
                MockTicketApplication(fixture_path)

    def repository_fixture_item(self) -> dict[str, Any]:
        items = json.loads(default_fixture_path().read_text(encoding="utf-8"))
        return copy.deepcopy(items[0])

    def test_health_declares_synthetic_data_and_loopback(self) -> None:
        status, payload, headers = self.harness.request("GET", "/health")

        self.assertEqual(status, 200)
        self.assertEqual(payload["data"]["status"], "ok")
        self.assertEqual(payload["data"]["bound_host"], "127.0.0.1")
        self.assertTrue(payload["meta"]["synthetic_data"])
        self.assertEqual(headers["X-Synthetic-Data"], "true")

    def test_get_ticket_uses_repository_fixture(self) -> None:
        status, payload, _ = self.harness.request("GET", "/tickets/TKT-1001")

        self.assertEqual(status, 200)
        self.assertTrue(payload["data"]["customer"].endswith("（虚构）"))
        self.assertFalse(payload["data"]["contains_personal_data"])
        self.assertEqual(payload["data"]["revision"], 0)

    def test_fixture_rejects_every_undefined_field(self) -> None:
        item = self.repository_fixture_item()
        item["debug_note"] = "不应进入公开 fixture"

        self.assert_fixture_rejected(item, "包含未定义字段：debug_note")

    def test_fixture_public_safety_checks_every_string_field(self) -> None:
        for field in (
            "ticket_id",
            "customer",
            "subject",
            "category",
            "priority",
            "status",
            "description",
        ):
            with self.subTest(field=field):
                item = self.repository_fixture_item()
                item[field] = "person" + "@" + "example.com"
                self.assert_fixture_rejected(
                    item,
                    rf"{field} 未通过公开安全校验（email）",
                )

    def test_fixture_rejects_secret_network_and_local_path_classes(self) -> None:
        unsafe_values = {
            "token": "api_" + "key=" + "abcdefghijklmnopqrstuvwxyz0123456789",
            "internal_url": "https://" + "support.ops" + ".internal/tickets/1",
            "literal_ip": "调试入口为 " + "10.10." + "12.8",
            "local_path": "/" + "Users/operator/private/ticket.json",
        }
        for unsafe_class, value in unsafe_values.items():
            with self.subTest(unsafe_class=unsafe_class):
                item = self.repository_fixture_item()
                item["description"] = value
                self.assert_fixture_rejected(item, "未通过公开安全校验")

    def test_invalid_ticket_id_is_400(self) -> None:
        status, payload, _ = self.harness.request("GET", "/tickets/not-a-ticket")

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "INVALID_TICKET_ID")

    def test_unknown_ticket_is_404(self) -> None:
        status, payload, _ = self.harness.request("GET", "/tickets/TKT-9999")

        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "TICKET_NOT_FOUND")

    def test_write_requires_public_demo_header(self) -> None:
        status, payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量"},
            headers={"Idempotency-Key": "missing-header-001"},
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "DEMO_WRITE_HEADER_REQUIRED")

    def test_invalid_classification_is_400(self) -> None:
        status, payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "", "unexpected": True},
            headers=write_headers("invalid-body-001"),
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "UNKNOWN_FIELDS")

    def test_revision_conflict_is_409(self) -> None:
        status, payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量", "expected_revision": 99},
            headers=write_headers("revision-conflict-001"),
        )

        self.assertEqual(status, 409)
        self.assertEqual(payload["error"]["code"], "REVISION_CONFLICT")
        self.assertEqual(payload["error"]["details"]["current_revision"], 0)

    def test_idempotency_replay_does_not_repeat_side_effect(self) -> None:
        body = {
            "category": "检索质量",
            "priority": "紧急",
            "expected_revision": 0,
            "reason": "合成训练样例",
        }
        headers = write_headers("idempotent-update-001")

        first_status, first_payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body=body,
            headers=headers,
        )
        second_status, second_payload, second_headers = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body=body,
            headers=headers,
        )
        _, current_payload, _ = self.harness.request("GET", "/tickets/TKT-1001")

        self.assertEqual(first_status, 200)
        self.assertEqual(second_status, 200)
        self.assertEqual(first_payload, second_payload)
        self.assertEqual(second_headers["Idempotent-Replayed"], "true")
        self.assertEqual(current_payload["data"]["revision"], 1)
        self.assertEqual(current_payload["data"]["category"], "检索质量")

    def test_reusing_key_for_different_request_is_409(self) -> None:
        headers = write_headers("key-reuse-conflict-001")
        self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量"},
            headers=headers,
        )

        status, payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "其他分类"},
            headers=headers,
        )

        self.assertEqual(status, 409)
        self.assertEqual(payload["error"]["code"], "IDEMPOTENCY_KEY_REUSED")

    def test_reset_restores_fixture_and_is_idempotent(self) -> None:
        self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量"},
            headers=write_headers("before-reset-001"),
        )
        headers = write_headers("explicit-reset-001")

        first_status, first_payload, _ = self.harness.request(
            "POST",
            "/reset",
            body={},
            headers=headers,
        )
        second_status, second_payload, second_headers = self.harness.request(
            "POST",
            "/reset",
            body={},
            headers=headers,
        )
        _, ticket_payload, _ = self.harness.request("GET", "/tickets/TKT-1001")

        self.assertEqual(first_status, 200)
        self.assertEqual(second_status, 200)
        self.assertEqual(first_payload, second_payload)
        self.assertEqual(second_headers["Idempotent-Replayed"], "true")
        self.assertEqual(ticket_payload["data"]["category"], "知识库")
        self.assertEqual(ticket_payload["data"]["revision"], 0)
        self.assertEqual(ticket_payload["meta"]["generation"], 2)

    def test_get_and_reset_return_one_generation_consistent_snapshot(self) -> None:
        update_status, _, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量"},
            headers=write_headers("snapshot-before-reset-001"),
        )
        self.assertEqual(update_status, 200)

        application = self.harness.server.application
        original_snapshot = application.get_ticket_snapshot
        snapshot_captured = threading.Barrier(2)
        allow_response = threading.Barrier(2)
        get_result: dict[str, tuple[int, dict[str, Any], dict[str, str]]] = {}

        def paused_snapshot(
            ticket_id: str,
        ) -> tuple[dict[str, Any] | None, int]:
            snapshot = original_snapshot(ticket_id)
            snapshot_captured.wait(timeout=3)
            allow_response.wait(timeout=3)
            return snapshot

        def read_ticket() -> None:
            get_result["response"] = self.harness.request(
                "GET",
                "/tickets/TKT-1001",
            )

        with mock.patch.object(
            application,
            "get_ticket_snapshot",
            side_effect=paused_snapshot,
        ):
            reader = threading.Thread(target=read_ticket, name="paused-ticket-get")
            reader.start()
            snapshot_captured.wait(timeout=3)
            reset_status, reset_payload, _ = self.harness.request(
                "POST",
                "/reset",
                body={},
                headers=write_headers("snapshot-reset-001"),
            )
            allow_response.wait(timeout=3)
            reader.join(timeout=3)

        self.assertFalse(reader.is_alive())
        self.assertEqual(reset_status, 200)
        self.assertEqual(reset_payload["data"]["generation"], 2)
        get_status, old_snapshot, _ = get_result["response"]
        self.assertEqual(get_status, 200)
        self.assertEqual(old_snapshot["data"]["category"], "检索质量")
        self.assertEqual(old_snapshot["data"]["revision"], 1)
        self.assertEqual(old_snapshot["meta"]["generation"], 1)

        current_status, current_snapshot, _ = self.harness.request(
            "GET",
            "/tickets/TKT-1001",
        )
        self.assertEqual(current_status, 200)
        self.assertEqual(current_snapshot["data"]["category"], "知识库")
        self.assertEqual(current_snapshot["data"]["revision"], 0)
        self.assertEqual(current_snapshot["meta"]["generation"], 2)

    def test_pre_reset_write_receipt_is_not_replayed_in_new_generation(self) -> None:
        body = {
            "category": "检索质量",
            "priority": "紧急",
            "expected_revision": 0,
            "reason": "跨代幂等测试",
        }
        old_headers = write_headers("generation-write-001")
        first_status, first_payload, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body=body,
            headers=old_headers,
        )
        reset_status, _, _ = self.harness.request(
            "POST",
            "/reset",
            body={},
            headers=write_headers("generation-reset-001"),
        )
        replay_status, replay_payload, replay_headers = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body=body,
            headers=old_headers,
        )
        second_status, second_payload, second_headers = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body=body,
            headers=old_headers,
        )

        self.assertEqual(first_status, 200)
        self.assertEqual(reset_status, 200)
        self.assertEqual(replay_status, 200)
        self.assertNotIn("Idempotent-Replayed", replay_headers)
        self.assertEqual(first_payload["meta"]["generation"], 1)
        self.assertEqual(replay_payload["meta"]["generation"], 2)
        self.assertEqual(replay_payload["data"]["revision"], 1)
        self.assertEqual(second_status, 200)
        self.assertEqual(second_payload, replay_payload)
        self.assertEqual(second_headers["Idempotent-Replayed"], "true")

    def test_pre_reset_key_may_be_reused_for_a_different_new_generation_request(self) -> None:
        old_headers = write_headers("generation-different-001")
        first_status, _, _ = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "检索质量"},
            headers=old_headers,
        )
        reset_status, _, _ = self.harness.request(
            "POST",
            "/reset",
            body={},
            headers=write_headers("generation-different-reset-001"),
        )
        new_status, new_payload, new_headers = self.harness.request(
            "PUT",
            "/tickets/TKT-1001/classification",
            body={"category": "平台限制"},
            headers=old_headers,
        )

        self.assertEqual(first_status, 200)
        self.assertEqual(reset_status, 200)
        self.assertEqual(new_status, 200)
        self.assertEqual(new_payload["data"]["category"], "平台限制")
        self.assertEqual(new_payload["meta"]["generation"], 2)
        self.assertNotIn("Idempotent-Replayed", new_headers)

    def test_write_rate_limit_is_structured_429(self) -> None:
        with ServerHarness(rate_limit=1) as limited:
            first_status, _, _ = limited.request(
                "PUT",
                "/tickets/TKT-1001/classification",
                body={"category": "检索质量"},
                headers=write_headers("rate-limit-first-001"),
            )
            second_status, payload, headers = limited.request(
                "PUT",
                "/tickets/TKT-1002/classification",
                body={"category": "平台限制"},
                headers=write_headers("rate-limit-second-001"),
            )

        self.assertEqual(first_status, 200)
        self.assertEqual(second_status, 429)
        self.assertEqual(payload["error"]["code"], "RATE_LIMITED")
        self.assertIn("Retry-After", headers)

    def test_server_rejects_non_loopback_binding(self) -> None:
        with self.assertRaisesRegex(ValueError, "只允许绑定"):
            create_server(host="0.0.0.0", port=0)


if __name__ == "__main__":
    unittest.main()
