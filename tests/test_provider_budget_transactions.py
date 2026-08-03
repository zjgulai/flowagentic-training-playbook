from __future__ import annotations

import concurrent.futures
import subprocess
import sys
import threading
from pathlib import Path
from typing import Callable

import yaml

from scripts.provider_budget import (
    BudgetError,
    ProviderCallResult,
    execute_reserved_call,
    release as release_reservation,
    validate_ledger_file,
)


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "provider_budget_guard.py"
RECORDER = ROOT / "scripts" / "record_provider_call.py"


def write_ledger(path: Path, *, limit: float = 300.0) -> None:
    payload = {
        "schema_version": 2,
        "currency": "CNY",
        "hard_limit": limit,
        "warning_threshold": 240.0,
        "spent": 0.0,
        "remaining": limit,
        "reserved": 0.0,
        "available_to_reserve": limit,
        "status": "active",
        "allowed_providers": ["DeepSeek", "Kimi"],
        "enforcement": {
            "stop_when_spent_gte_hard_limit": True,
            "allow_override": False,
            "ci_provider_calls": False,
            "synthetic_data_only": True,
            "secrets_in_repository": False,
            "network_call_requires_pending_reservation": True,
            "reservation_created_under_exclusive_lock": True,
            "settlement_requires_matching_reservation": True,
            "over_reservation_marks_budget_breached": True,
            "release_requires_network_call_not_started": True,
            "one_reservation_authorizes_one_call": True,
            "all_ledger_transitions_use_one_exclusive_lock": True,
            "reservation_override": False,
            "start_requires_pending_reservation": True,
            "in_flight_reservations_count_against_limit": True,
            "uncertain_failure_charged_at_reserved_maximum": True,
            "provider_transport_must_use_budget_wrapper": True,
            "provider_account_hard_limit_receipt_required": True,
        },
        "reservations": [],
        "calls": [],
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def reserve(path: Path, experiment_id: str, cost: str = "0.30") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(GUARD),
            "--ledger",
            str(path),
            "--experiment-id",
            experiment_id,
            "--provider",
            "DeepSeek",
            "--model",
            "deepseek-chat",
            "--estimated-cost",
            cost,
            "--synthetic-data",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def settle_cli(path: Path, experiment_id: str, cost: str = "0.20") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RECORDER),
            "--ledger",
            str(path),
            "--experiment-id",
            experiment_id,
            "--provider",
            "DeepSeek",
            "--model",
            "deepseek-chat",
            "--input-tokens",
            "100",
            "--output-tokens",
            "20",
            "--latency-ms",
            "75",
            "--actual-cost",
            cost,
            "--status",
            "success",
            "--synthetic-data",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def execute_once(
    path: Path,
    experiment_id: str,
    cost: str = "0.20",
    *,
    transport: Callable[[], ProviderCallResult] | None = None,
) -> ProviderCallResult:
    callback = transport or (
        lambda: ProviderCallResult(
            input_tokens=100,
            output_tokens=20,
            latency_ms=75,
            actual_cost=cost,
        )
    )
    return execute_reserved_call(
        path,
        experiment_id=experiment_id,
        provider="DeepSeek",
        model="deepseek-chat",
        transport=callback,
    )


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_concurrent_reservations_never_exceed_cny_300_hard_limit(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger, limit=300.0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = list(
            pool.map(
                lambda index: reserve(ledger, f"EXP-CONCURRENT-{index:02d}", "100.00"),
                range(10),
            )
        )

    assert sum(result.returncode == 0 for result in results) == 3
    assert all(result.returncode in {0, 3} for result in results)
    payload = load(ledger)
    pending = [item for item in payload["reservations"] if item["status"] == "pending"]
    assert len(pending) == 3
    assert len({item["experiment_id"] for item in pending}) == 3
    assert payload["spent"] == 0.0
    assert payload["reserved"] == 300.0
    assert payload["available_to_reserve"] == 0.0
    assert payload["spent"] + payload["reserved"] <= payload["hard_limit"]


def test_concurrent_duplicate_id_creates_only_one_authority(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda _: reserve(ledger, "EXP-ONE-AUTHORITY", "0.20"), range(6)))

    assert sum(result.returncode == 0 for result in results) == 1
    payload = load(ledger)
    matching = [
        item for item in payload["reservations"] if item["experiment_id"] == "EXP-ONE-AUTHORITY"
    ]
    assert len(matching) == 1
    assert matching[0]["status"] == "pending"


def test_settlement_consumes_reservation_and_release_returns_availability(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-SETTLE-0001", "0.60").returncode == 0
    assert reserve(ledger, "EXP-RELEASE-0001", "0.20").returncode == 0

    settled = execute_once(ledger, "EXP-SETTLE-0001", "0.40")
    released = subprocess.run(
        [
            sys.executable,
            str(RECORDER),
            "--ledger",
            str(ledger),
            "--action",
            "release",
            "--experiment-id",
            "EXP-RELEASE-0001",
            "--release-reason",
            "调用前验证失败",
            "--network-call-not-started",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert settled.actual_cost == "0.40"
    assert released.returncode == 0, released.stderr
    payload = load(ledger)
    states = {item["experiment_id"]: item["status"] for item in payload["reservations"]}
    assert states == {"EXP-SETTLE-0001": "settled", "EXP-RELEASE-0001": "released"}
    assert payload["spent"] == 0.4
    assert payload["reserved"] == 0.0
    assert payload["remaining"] == 299.6
    assert payload["available_to_reserve"] == 299.6
    assert len(payload["calls"]) == 1


def test_direct_record_without_in_flight_authority_is_blocked(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)

    direct = settle_cli(ledger, "EXP-NO-RESERVATION", "0.10")
    assert direct.returncode == 2
    assert "no reservation exists" in direct.stderr

    assert reserve(ledger, "EXP-TOO-EXPENSIVE", "0.20").returncode == 0
    pending = settle_cli(ledger, "EXP-TOO-EXPENSIVE", "0.10")
    assert pending.returncode == 2
    assert "not in flight" in pending.stderr
    payload = load(ledger)
    reservation = next(
        item for item in payload["reservations"] if item["experiment_id"] == "EXP-TOO-EXPENSIVE"
    )
    assert reservation["status"] == "pending"
    assert payload["spent"] == 0.0
    assert payload["reserved"] == 0.2


def test_concurrent_wrappers_can_start_transport_only_once(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-SINGLE-CONSUME", "0.50").returncode == 0

    transport_calls = 0
    calls_lock = threading.Lock()

    def transport() -> ProviderCallResult:
        nonlocal transport_calls
        with calls_lock:
            transport_calls += 1
        return ProviderCallResult(100, 20, 75, "0.40")

    def run_wrapper() -> str:
        try:
            execute_once(
                ledger,
                "EXP-SINGLE-CONSUME",
                transport=transport,
            )
            return "success"
        except BudgetError:
            return "blocked"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: run_wrapper(), range(2)))

    assert results.count("success") == 1
    assert results.count("blocked") == 1
    assert transport_calls == 1
    payload = load(ledger)
    reservation = payload["reservations"][0]
    assert reservation["status"] == "settled"
    assert reservation["call_attempts"] == 1
    assert len(payload["calls"]) == 1
    assert payload["spent"] + payload["reserved"] <= payload["hard_limit"]


def test_transport_exception_is_charged_at_full_reserved_maximum(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-UNKNOWN-OUTCOME", "2.50").returncode == 0

    def broken_transport() -> ProviderCallResult:
        raise TimeoutError("synthetic provider timeout")

    try:
        execute_once(ledger, "EXP-UNKNOWN-OUTCOME", transport=broken_transport)
    except TimeoutError:
        pass
    else:  # pragma: no cover - explicit fail path
        raise AssertionError("transport exception was not propagated")

    payload = validate_ledger_file(ledger)
    assert payload["spent"] == 2.5
    assert payload["reserved"] == 0.0
    assert payload["calls"][0]["status"] == "failed"
    assert payload["calls"][0]["actual_cost"] == 2.5


def test_reported_over_reservation_is_recorded_and_blocks_future_calls(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-OVER-RESERVE", "299.00").returncode == 0

    try:
        execute_once(ledger, "EXP-OVER-RESERVE", "301.00")
    except BudgetError as exc:
        assert exc.exit_code == 3
        assert "charge was recorded" in str(exc)
    else:  # pragma: no cover - explicit fail path
        raise AssertionError("over-reservation outcome was not surfaced")

    payload = validate_ledger_file(ledger)
    assert payload["spent"] == 301.0
    assert payload["status"] == "breached"
    assert payload["calls"][0]["budget_outcome"] == "breached"
    assert reserve(ledger, "EXP-AFTER-BREACH", "0.01").returncode == 2


def test_small_over_reservation_still_marks_ledger_breached(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-SMALL-OVER", "1.00").returncode == 0

    try:
        execute_once(ledger, "EXP-SMALL-OVER", "1.01")
    except BudgetError as exc:
        assert exc.exit_code == 3
    else:  # pragma: no cover - explicit fail path
        raise AssertionError("small over-reservation was not surfaced")

    payload = validate_ledger_file(ledger)
    assert payload["spent"] == 1.01
    assert payload["status"] == "breached"
    assert payload["remaining"] == 298.99


def test_release_rejects_any_in_flight_reservation(tmp_path: Path) -> None:
    ledger = tmp_path / "budget.yml"
    write_ledger(ledger)
    assert reserve(ledger, "EXP-IN-FLIGHT", "1.00").returncode == 0

    invoked = threading.Event()
    unblock = threading.Event()

    def transport() -> ProviderCallResult:
        invoked.set()
        assert unblock.wait(timeout=3)
        return ProviderCallResult(1, 1, 1, "0.10")

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            execute_once,
            ledger,
            "EXP-IN-FLIGHT",
            transport=transport,
        )
        assert invoked.wait(timeout=3)
        try:
            release_reservation(
                ledger,
                experiment_id="EXP-IN-FLIGHT",
                reason="should be rejected",
                network_call_not_started=True,
            )
        except BudgetError as exc:
            assert "not pending" in str(exc)
        else:  # pragma: no cover - explicit fail path
            raise AssertionError("in-flight reservation was released")
        unblock.set()
        future.result(timeout=3)


def test_runtime_rejects_tampered_project_budget_contract(tmp_path: Path) -> None:
    cases = (
        ("hard-limit", lambda payload: payload.update(
            {"hard_limit": 301.0, "remaining": 301.0, "available_to_reserve": 301.0}
        )),
        ("provider-list", lambda payload: payload["allowed_providers"].append("Other")),
        ("override", lambda payload: payload["enforcement"].update({"allow_override": True})),
    )
    for suffix, mutate in cases:
        ledger = tmp_path / f"budget-{suffix}.yml"
        write_ledger(ledger)
        payload = load(ledger)
        mutate(payload)
        ledger.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

        result = reserve(ledger, f"EXP-TAMPER-{suffix.upper()}", "0.10")

        assert result.returncode == 2
        assert load(ledger)["reservations"] == []
