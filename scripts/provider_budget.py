#!/usr/bin/env python3
"""Atomic reservation lifecycle for the training-provider budget ledger.

The only safe authority to start a provider request is a persisted ``pending``
reservation created by :func:`reserve` and atomically consumed to ``in_flight``
by :func:`execute_reserved_call`.  A reservation is either settled with the
observed/conservative charge or explicitly released before any network call.
All state transitions are serialized by the same advisory file lock.
"""

from __future__ import annotations

import datetime as dt
import decimal
import fcntl
import os
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import yaml


CENT = decimal.Decimal("0.01")
PROJECT_HARD_LIMIT = decimal.Decimal("300.00")
PROJECT_WARNING_THRESHOLD = decimal.Decimal("240.00")
PROJECT_PROVIDERS = {"DeepSeek", "Kimi"}
SAFE_ID = re.compile(r"^EXP-[A-Z0-9-]{4,64}$")
SAFE_MODEL = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")
REQUIRED_ENFORCEMENT = {
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
}


class BudgetError(Exception):
    """A fail-closed budget transition error with a stable process exit code."""

    def __init__(self, message: str, *, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class ProviderCallResult:
    """Public-safe accounting result returned by a provider transport.

    The transport must not return provider request identifiers, raw prompts, or
    response bodies.  Those values are intentionally outside the public ledger.
    """

    input_tokens: int
    output_tokens: int
    latency_ms: int
    actual_cost: object
    status: str = "success"


def money(value: object) -> decimal.Decimal:
    """Parse a non-negative amount and round upward to a whole CNY cent."""

    try:
        amount = decimal.Decimal(str(value))
    except decimal.InvalidOperation as exc:
        raise BudgetError("amount is not a valid decimal") from exc
    if not amount.is_finite():
        raise BudgetError("amount must be finite")
    if amount < 0:
        raise BudgetError("amount cannot be negative")
    return amount.quantize(CENT, rounding=decimal.ROUND_CEILING)


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def _number(value: decimal.Decimal) -> float:
    return float(value.quantize(CENT))


def _call_cost(item: dict[str, Any]) -> decimal.Decimal:
    if "actual_cost" in item:
        return money(item["actual_cost"])
    # Schema v1 migration compatibility. New receipts always use actual_cost.
    return money(item.get("estimated_cost", 0))


def _reservation_cost(item: dict[str, Any]) -> decimal.Decimal:
    return money(item.get("reserved_cost", 0))


def _totals(payload: dict[str, Any]) -> tuple[decimal.Decimal, decimal.Decimal, decimal.Decimal]:
    limit = money(payload.get("hard_limit", -1))
    spent = sum((_call_cost(item) for item in payload.get("calls", [])), decimal.Decimal(0))
    reserved = sum(
        (
            _reservation_cost(item)
            for item in payload.get("reservations", [])
            if item.get("status") in {"pending", "in_flight"}
        ),
        decimal.Decimal(0),
    )
    if spent + reserved > limit and payload.get("status") != "breached":
        raise BudgetError("ledger already exceeds its hard limit")
    return limit, spent, reserved


def _validate_ledger(payload: object) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise BudgetError("provider budget ledger must be a YAML object")
    if not isinstance(payload.get("calls"), list):
        raise BudgetError("provider budget calls must be a list")
    if not isinstance(payload.get("reservations"), list):
        raise BudgetError("provider budget reservations must be a list")
    allowed = payload.get("allowed_providers")
    if not isinstance(allowed, list) or not allowed:
        raise BudgetError("provider allow-list is missing")
    if payload.get("schema_version") != 2:
        raise BudgetError("provider budget schema version must be 2")
    if payload.get("currency") != "CNY":
        raise BudgetError("provider budget currency must be CNY")
    if money(payload.get("hard_limit", -1)) != PROJECT_HARD_LIMIT:
        raise BudgetError("provider hard limit must remain CNY 300.00")
    if money(payload.get("warning_threshold", -1)) != PROJECT_WARNING_THRESHOLD:
        raise BudgetError("provider warning threshold must remain CNY 240.00")
    if len(allowed) != len(PROJECT_PROVIDERS) or set(allowed) != PROJECT_PROVIDERS:
        raise BudgetError("provider allow-list must contain only DeepSeek and Kimi")
    enforcement = payload.get("enforcement")
    if not isinstance(enforcement, dict):
        raise BudgetError("provider enforcement contract is missing")
    for key, expected in REQUIRED_ENFORCEMENT.items():
        if enforcement.get(key) is not expected:
            raise BudgetError(f"provider enforcement contract is invalid: {key}")

    limit, spent, reserved = _totals(payload)
    declared_spent = money(payload.get("spent", -1))
    declared_reserved = money(payload.get("reserved", -1))
    declared_remaining = money(payload.get("remaining", -1))
    declared_available = money(payload.get("available_to_reserve", -1))
    if declared_spent != spent:
        raise BudgetError("declared spent does not match settled call receipts")
    if declared_reserved != reserved:
        raise BudgetError("declared reserved does not match pending reservations")
    expected_remaining = max(decimal.Decimal(0), limit - spent)
    expected_available = max(decimal.Decimal(0), limit - spent - reserved)
    if declared_remaining != expected_remaining:
        raise BudgetError("declared remaining does not match hard limit minus spent")
    if declared_available != expected_available:
        raise BudgetError("declared available_to_reserve does not match ledger state")
    if spent + reserved > limit and payload.get("status") != "breached":
        raise BudgetError("over-limit ledger must be marked breached")
    has_over_reservation = any(
        _call_cost(item) > _reservation_cost(item)
        for item in payload.get("calls", [])
        if isinstance(item, dict)
    )
    if (
        payload.get("status") == "breached"
        and spent + reserved <= limit
        and not has_over_reservation
    ):
        raise BudgetError("budget is marked breached without an over-reservation receipt")

    reservation_ids: list[str] = []
    for item in payload["reservations"]:
        if not isinstance(item, dict):
            raise BudgetError("reservation entries must be objects")
        experiment_id = item.get("experiment_id")
        if not isinstance(experiment_id, str) or not SAFE_ID.fullmatch(experiment_id):
            raise BudgetError("ledger contains an invalid reservation experiment id")
        if item.get("status") not in {"pending", "in_flight", "settled", "released"}:
            raise BudgetError("ledger contains an invalid reservation status")
        if item.get("provider") not in PROJECT_PROVIDERS:
            raise BudgetError("ledger contains a reservation for a disallowed provider")
        if not isinstance(item.get("model"), str) or not SAFE_MODEL.fullmatch(item["model"]):
            raise BudgetError("ledger contains an invalid reservation model")
        if item.get("synthetic_data") is not True:
            raise BudgetError("ledger contains a non-synthetic reservation")
        if money(item.get("reserved_cost", 0)) <= 0:
            raise BudgetError("ledger contains a non-positive reservation")
        status = item.get("status")
        attempts = item.get("call_attempts")
        if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts < 0:
            raise BudgetError("reservation has an invalid call-attempt count")
        if status == "released" and item.get("network_call_started") is not False:
            raise BudgetError("released reservation claims that a network call started")
        if status == "settled" and item.get("network_call_started") is not True:
            raise BudgetError("settled reservation is missing its network-call marker")
        if status == "in_flight" and item.get("network_call_started") is not True:
            raise BudgetError("in-flight reservation is missing its network-call marker")
        if status == "pending" and item.get("network_call_started") is not False:
            raise BudgetError("pending reservation has an invalid network-call marker")
        expected_attempts = 0 if status in {"pending", "released"} else 1
        if attempts != expected_attempts:
            raise BudgetError("reservation does not authorize exactly one provider call")
        reservation_ids.append(experiment_id)
    if len(reservation_ids) != len(set(reservation_ids)):
        raise BudgetError("ledger contains duplicate reservation experiment ids")

    if any(not isinstance(item, dict) for item in payload["calls"]):
        raise BudgetError("call entries must be objects")
    call_ids = [item.get("experiment_id") for item in payload["calls"]]
    if len(call_ids) != len(set(call_ids)):
        raise BudgetError("ledger contains duplicate call experiment ids")
    if any(experiment_id not in set(reservation_ids) for experiment_id in call_ids):
        raise BudgetError("settled call exists without a reservation")
    reservations_by_id = {
        item["experiment_id"]: item for item in payload["reservations"]
    }
    for call in payload["calls"]:
        experiment_id = call.get("experiment_id")
        reservation = reservations_by_id.get(experiment_id)
        if reservation is None or reservation.get("status") != "settled":
            raise BudgetError("call receipt does not match a settled reservation")
        if call.get("provider") != reservation.get("provider"):
            raise BudgetError("call provider does not match its reservation")
        if call.get("model") != reservation.get("model"):
            raise BudgetError("call model does not match its reservation")
        if call.get("provider") not in PROJECT_PROVIDERS:
            raise BudgetError("ledger contains a call for a disallowed provider")
        if not isinstance(call.get("model"), str) or not SAFE_MODEL.fullmatch(call["model"]):
            raise BudgetError("ledger contains an invalid call model")
        if call.get("synthetic_data") is not True:
            raise BudgetError("ledger contains a non-synthetic call")
        if call.get("status") not in {"success", "failed"}:
            raise BudgetError("ledger contains an invalid call status")
        for metric in ("input_tokens", "output_tokens", "latency_ms"):
            value = call.get(metric)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise BudgetError(f"ledger contains an invalid call metric: {metric}")
        if call.get("provider_request_id_recorded") is not False:
            raise BudgetError("provider request identifiers must not be recorded")
        if _reservation_cost(call) != _reservation_cost(reservation):
            raise BudgetError("call reserved cost does not match its reservation")
        if money(reservation.get("actual_cost", -1)) != _call_cost(call):
            raise BudgetError("call actual cost does not match its reservation")
        over_reserved = _call_cost(call) > _reservation_cost(reservation)
        if call.get("budget_outcome") not in {"within-reservation", "breached"}:
            raise BudgetError("call receipt has an invalid budget outcome")
        if over_reserved != (call.get("budget_outcome") == "breached"):
            raise BudgetError("call budget outcome does not match its actual cost")
    return payload


def _recompute(payload: dict[str, Any]) -> tuple[decimal.Decimal, decimal.Decimal, decimal.Decimal]:
    limit, spent, reserved = _totals(payload)
    payload["spent"] = _number(spent)
    # remaining is total unspent budget; pending reservations are included in it.
    payload["remaining"] = _number(max(decimal.Decimal(0), limit - spent))
    payload["reserved"] = _number(reserved)
    payload["available_to_reserve"] = _number(
        max(decimal.Decimal(0), limit - spent - reserved)
    )
    if spent + reserved > limit:
        payload["status"] = "breached"
    elif spent >= limit:
        payload["status"] = "hard-limit-reached"
    return limit, spent, reserved


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            dir=path.parent,
            prefix=".provider-budget-",
            suffix=".tmp",
            encoding="utf-8",
            delete=False,
        ) as temporary:
            yaml.safe_dump(payload, temporary, allow_unicode=True, sort_keys=False)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        temporary_path.replace(path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _read_locked(path: Path) -> tuple[Any, dict[str, Any]]:
    path = path.resolve()
    lock_path = path.with_suffix(f"{path.suffix}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = lock_path.open("a+", encoding="utf-8")
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    try:
        payload = _validate_ledger(yaml.safe_load(path.read_text(encoding="utf-8")))
    except Exception:
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        lock.close()
        raise
    return lock, payload


def _unlock(lock: Any) -> None:
    fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    lock.close()


def validate_ledger_file(
    ledger_path: Path,
    *,
    require_release_clean: bool = False,
) -> dict[str, Any]:
    """Validate the canonical ledger under its transition lock.

    Release validation additionally rejects unresolved pending or in-flight
    authorities.  A shallow YAML totals check must never be used as a publish
    gate.
    """

    lock, payload = _read_locked(ledger_path)
    try:
        if require_release_clean:
            unresolved = [
                item.get("experiment_id", "<unknown>")
                for item in payload["reservations"]
                if item.get("status") in {"pending", "in_flight"}
            ]
            if unresolved:
                raise BudgetError(
                    "release requires no pending or in-flight provider reservations"
                )
            if payload.get("status") == "breached":
                raise BudgetError("release is blocked because the provider budget was breached")
        return payload
    finally:
        _unlock(lock)


def reserve(
    ledger_path: Path,
    *,
    experiment_id: str | None,
    provider: str,
    model: str | None,
    maximum_cost: object,
    synthetic_data: bool,
) -> dict[str, Any]:
    """Atomically reserve worst-case cost before one provider network call."""

    lock, payload = _read_locked(ledger_path)
    try:
        if payload.get("status") != "active":
            raise BudgetError("provider experiments are not active")
        if experiment_id is None or not SAFE_ID.fullmatch(experiment_id):
            raise BudgetError("experiment id must use the public-safe EXP-* format")
        if model is None or not SAFE_MODEL.fullmatch(model):
            raise BudgetError("model must use a public-safe model identifier")
        if not synthetic_data:
            raise BudgetError("only synthetic-data experiments may reserve budget")
        if provider not in payload["allowed_providers"]:
            raise BudgetError("provider is not allowed")
        cost = money(maximum_cost)
        if cost <= 0:
            raise BudgetError("reserved maximum cost must be greater than zero")

        all_ids = {
            item.get("experiment_id") for item in payload.get("reservations", [])
        } | {item.get("experiment_id") for item in payload.get("calls", [])}
        if experiment_id in all_ids:
            raise BudgetError("experiment id already has a reservation or receipt")

        limit, spent, reserved = _totals(payload)
        if spent + reserved + cost > limit:
            raise BudgetError(
                f"projected committed spend CNY {spent + reserved + cost} "
                f"exceeds hard limit CNY {limit}",
                exit_code=3,
            )
        reservation = {
            "experiment_id": experiment_id,
            "reserved_at": _utc_now(),
            "provider": provider,
            "model": model,
            "reserved_cost": _number(cost),
            "status": "pending",
            "synthetic_data": True,
            "network_call_started": False,
            "call_attempts": 0,
        }
        payload["reservations"].append(reservation)
        _recompute(payload)
        _write_atomic(ledger_path.resolve(), payload)
        return reservation
    finally:
        _unlock(lock)


def begin_call(
    ledger_path: Path,
    *,
    experiment_id: str,
    provider: str,
    model: str,
) -> dict[str, Any]:
    """Atomically consume a pending reservation before the transport runs.

    This transition is deliberately separate from settlement: if the process
    crashes after it returns, the reservation remains ``in_flight`` and its
    full maximum continues to count against the project limit.
    """

    lock, payload = _read_locked(ledger_path)
    try:
        if payload.get("status") != "active":
            raise BudgetError("provider experiments are not active")
        reservation = next(
            (
                item
                for item in payload["reservations"]
                if item.get("experiment_id") == experiment_id
            ),
            None,
        )
        if reservation is None:
            raise BudgetError("no reservation exists for this experiment id")
        if reservation.get("status") != "pending":
            raise BudgetError("reservation is not pending and cannot authorize a call")
        if reservation.get("provider") != provider or reservation.get("model") != model:
            raise BudgetError("provider or model does not match the reservation")
        if reservation.get("network_call_started") is not False:
            raise BudgetError("reservation already claims a network call")
        if reservation.get("call_attempts") != 0:
            raise BudgetError("reservation already authorized a provider call")
        if any(item.get("experiment_id") == experiment_id for item in payload["calls"]):
            raise BudgetError("experiment id already has a settled receipt")

        reservation.update(
            {
                "status": "in_flight",
                "started_at": _utc_now(),
                "network_call_started": True,
                "call_attempts": 1,
            }
        )
        _recompute(payload)
        _write_atomic(ledger_path.resolve(), payload)
        return dict(reservation)
    finally:
        _unlock(lock)


def settle(
    ledger_path: Path,
    *,
    experiment_id: str,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    actual_cost: object,
    call_status: str,
    synthetic_data: bool,
) -> dict[str, Any]:
    """Settle one in-flight reservation with its observed or conservative cost."""

    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0
        for value in (input_tokens, output_tokens, latency_ms)
    ):
        raise BudgetError("token and latency values cannot be negative")
    if call_status not in {"success", "failed"}:
        raise BudgetError("call status must be success or failed")
    if not synthetic_data:
        raise BudgetError("only synthetic-data experiments may be settled")
    cost = money(actual_cost)

    lock, payload = _read_locked(ledger_path)
    try:
        reservation = next(
            (
                item
                for item in payload["reservations"]
                if item.get("experiment_id") == experiment_id
            ),
            None,
        )
        if reservation is None:
            raise BudgetError("no reservation exists for this experiment id")
        if reservation.get("status") != "in_flight":
            raise BudgetError("reservation is not in flight")
        if reservation.get("provider") != provider or reservation.get("model") != model:
            raise BudgetError("provider or model does not match the reservation")
        reserved_cost = _reservation_cost(reservation)
        if any(item.get("experiment_id") == experiment_id for item in payload["calls"]):
            raise BudgetError("experiment id already has a settled receipt")

        now = _utc_now()
        reservation.update(
            {
                "status": "settled",
                "settled_at": now,
                "actual_cost": _number(cost),
                "network_call_started": True,
                "call_attempts": 1,
            }
        )
        budget_outcome = "breached" if cost > reserved_cost else "within-reservation"
        receipt = {
            "experiment_id": experiment_id,
            "recorded_at": now,
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "reserved_cost": _number(reserved_cost),
            "actual_cost": _number(cost),
            # Kept for existing public validation consumers during schema migration.
            "estimated_cost": _number(cost),
            "status": call_status,
            "budget_outcome": budget_outcome,
            "synthetic_data": True,
            "provider_request_id_recorded": False,
        }
        payload["calls"].append(receipt)
        if budget_outcome == "breached":
            payload["status"] = "breached"
        _recompute(payload)
        _write_atomic(ledger_path.resolve(), payload)
        return receipt
    finally:
        _unlock(lock)


def execute_reserved_call(
    ledger_path: Path,
    *,
    experiment_id: str,
    provider: str,
    model: str,
    transport: Callable[[], ProviderCallResult],
) -> ProviderCallResult:
    """Run exactly one transport behind an atomically consumed reservation.

    Unknown outcomes are conservatively charged at the reservation maximum.
    A process crash leaves an in-flight reservation committed at that same
    maximum.  Provider credentials and request payloads stay inside the caller's
    transport closure and are never accepted by this ledger API.
    """

    authority = begin_call(
        ledger_path,
        experiment_id=experiment_id,
        provider=provider,
        model=model,
    )
    started = time.monotonic()
    try:
        result = transport()
        if not isinstance(result, ProviderCallResult):
            raise BudgetError("provider transport returned an invalid accounting result")
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in (result.input_tokens, result.output_tokens, result.latency_ms)
        ):
            raise BudgetError("provider transport returned invalid token or latency metrics")
        if result.status not in {"success", "failed"}:
            raise BudgetError("provider transport returned an invalid call status")
        money(result.actual_cost)
    except BaseException:
        elapsed_ms = max(0, int((time.monotonic() - started) * 1000))
        try:
            settle(
                ledger_path,
                experiment_id=experiment_id,
                provider=provider,
                model=model,
                input_tokens=0,
                output_tokens=0,
                latency_ms=elapsed_ms,
                actual_cost=authority["reserved_cost"],
                call_status="failed",
                synthetic_data=True,
            )
        except BudgetError as accounting_error:
            raise BudgetError(
                "provider call outcome is uncertain and conservative settlement failed",
                exit_code=4,
            ) from accounting_error
        raise

    receipt = settle(
        ledger_path,
        experiment_id=experiment_id,
        provider=provider,
        model=model,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
        actual_cost=result.actual_cost,
        call_status=result.status,
        synthetic_data=True,
    )
    if receipt.get("budget_outcome") == "breached":
        raise BudgetError(
            "provider cost exceeded its reservation; the charge was recorded and future calls are blocked",
            exit_code=3,
        )
    return result


def release(
    ledger_path: Path,
    *,
    experiment_id: str,
    reason: str,
    network_call_not_started: bool,
) -> dict[str, Any]:
    """Release a pending reservation only when no provider request started."""

    clean_reason = reason.strip()
    if not network_call_not_started:
        raise BudgetError("release requires an explicit no-network-call assertion")
    if not 1 <= len(clean_reason) <= 200:
        raise BudgetError("release reason must contain 1-200 characters")

    lock, payload = _read_locked(ledger_path)
    try:
        reservation = next(
            (
                item
                for item in payload["reservations"]
                if item.get("experiment_id") == experiment_id
            ),
            None,
        )
        if reservation is None:
            raise BudgetError("no reservation exists for this experiment id")
        if reservation.get("status") != "pending":
            raise BudgetError("reservation is not pending")
        reservation.update(
            {
                "status": "released",
                "released_at": _utc_now(),
                "release_reason": clean_reason,
                "network_call_started": False,
            }
        )
        _recompute(payload)
        _write_atomic(ledger_path.resolve(), payload)
        return reservation
    finally:
        _unlock(lock)
