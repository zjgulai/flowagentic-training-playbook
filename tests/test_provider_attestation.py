from __future__ import annotations

import base64
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from scripts.provider_attestation import (
    ProviderAttestationError,
    signature_message,
    verify_provider_attestation,
)
from scripts.validate_content import (
    GATE_EVIDENCE_CONTRACTS,
    evidence_aggregate_sha256,
    validate_gate_receipt,
    validate_provider_signed_receipt,
)


RELEASE_SHA = "1234567890abcdef1234567890abcdef12345678"
PRODUCT_VERSION = "3.1.3-cn.1"
NOW = dt.datetime(2026, 8, 1, 0, 0, tzinfo=dt.UTC)


def digest(label: str) -> str:
    return hashlib.sha256(f"flowagentic-test:{label}".encode()).hexdigest()


def make_payload() -> dict[str, Any]:
    run_time = "2026-07-31T23:58:00Z"
    verified_at = "2026-07-31T23:59:00Z"
    runs = []
    for index, (provider, model) in enumerate(
        (("DeepSeek", "deepseek-chat"), ("Kimi", "moonshot-v1-8k")),
        start=1,
    ):
        runs.append(
            {
                "provider": provider,
                "model": model,
                "experiment_id": f"EXP-SIGNED-{index:02d}",
                "status": "success",
                "synthetic_data": True,
                "fixture": f"synthetic-ticket-{index:02d}",
                "fixture_sha256": digest(f"fixture-{index}"),
                "release_sha": RELEASE_SHA,
                "product_version": PRODUCT_VERSION,
                "input_tokens": 120 + index,
                "output_tokens": 30 + index,
                "latency_ms": 500 + index,
                "actual_cost": "0.12",
                "currency": "CNY",
                "executed_at": run_time,
                "provider_usage_sha256": digest(f"usage-{index}"),
                "cleanup_status": "passed",
                "cleanup_receipt_sha256": digest(f"cleanup-{index}"),
                "residual_object_count": 0,
            }
        )
    controls = [
        {
            "provider": provider,
            "status": "passed",
            "currency": "CNY",
            "hard_limit": 150,
            "auto_recharge": False,
            "receipt_sha256": digest(f"account-{provider}"),
            "verified_at": verified_at,
        }
        for provider in ("DeepSeek", "Kimi")
    ]
    claim_ids = [
        item_id
        for item_id in GATE_EVIDENCE_CONTRACTS["provider_executions"][
            "evidence_ids"
        ]
        if item_id != "EVD-PROVIDER-SIGNED-ATTESTATION"
    ]
    claims_bundle_sha256 = evidence_aggregate_sha256(
        [(item_id, digest(f"claim-{item_id}")) for item_id in claim_ids]
    )
    return {
        "schema_version": 1,
        "evidence_type": "provider-execution",
        "release_sha": RELEASE_SHA,
        "product_version": PRODUCT_VERSION,
        "public_safe": True,
        "verified_at": verified_at,
        "claims_bundle_sha256": claims_bundle_sha256,
        "provider_runs": runs,
        "account_budget_controls": controls,
    }


def write_bundle(
    root: Path,
    payload: dict[str, Any],
    *,
    signer_id: str = "training-runner-01",
    envelope_overrides: dict[str, Any] | None = None,
) -> tuple[Path, Path, Ed25519PrivateKey]:
    evidence = root / "data" / "evidence"
    trust = root / "data" / "trust"
    evidence.mkdir(parents=True, exist_ok=True)
    trust.mkdir(parents=True, exist_ok=True)
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    trust_payload = {
        "schema_version": 1,
        "status": "active",
        "signers": [
            {
                "signer_id": signer_id,
                "algorithm": "Ed25519",
                "status": "active",
                "public_key_base64": base64.b64encode(public_key).decode(),
                "not_before": "2026-01-01T00:00:00Z",
                "not_after": "2026-12-31T23:59:59Z",
            }
        ],
    }
    (trust / "provider-attestors.yml").write_text(
        yaml.safe_dump(trust_payload, sort_keys=False),
        encoding="utf-8",
    )
    raw_payload = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    payload_path = evidence / "provider-execution-payload.json"
    payload_path.write_bytes(raw_payload)
    envelope = {
        "schema_version": 1,
        "algorithm": "Ed25519",
        "signer_id": signer_id,
        "payload_path": "data/evidence/provider-execution-payload.json",
        "payload_sha256": hashlib.sha256(raw_payload).hexdigest(),
        "signature_base64": base64.b64encode(
            private_key.sign(signature_message(raw_payload))
        ).decode(),
    }
    if envelope_overrides:
        envelope.update(envelope_overrides)
    envelope_path = evidence / "provider-execution.attestation.json"
    envelope_path.write_text(json.dumps(envelope), encoding="utf-8")
    return envelope_path, payload_path, private_key


def verify(root: Path, envelope: Path) -> dict[str, Any]:
    return verify_provider_attestation(
        envelope,
        expected_release_sha=RELEASE_SHA,
        expected_product_version=PRODUCT_VERSION,
        project_root=root,
        now=NOW,
    )


def make_public_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    attestation_path = "data/evidence/provider-execution.attestation.json"
    evidence_items = []
    aggregate_items: list[tuple[str, str]] = []
    for item_id in GATE_EVIDENCE_CONTRACTS["provider_executions"]["evidence_ids"]:
        item_digest = digest(
            "signed-attestation"
            if item_id == "EVD-PROVIDER-SIGNED-ATTESTATION"
            else f"claim-{item_id}"
        )
        artifact = (
            attestation_path
            if item_id == "EVD-PROVIDER-SIGNED-ATTESTATION"
            else f"data/evidence/{item_id.casefold()}.json"
        )
        evidence_items.append(
            {"id": item_id, "artifact": artifact, "sha256": item_digest}
        )
        aggregate_items.append((item_id, item_digest))
    return {
        "attestation_path": attestation_path,
        "verified_at": payload["verified_at"],
        "artifact_sha256": evidence_aggregate_sha256(aggregate_items),
        "provider_runs": copy.deepcopy(payload["provider_runs"]),
        "account_budget_controls": copy.deepcopy(
            payload["account_budget_controls"]
        ),
        "evidence_items": evidence_items,
    }


def test_valid_ed25519_attestation_returns_verified_payload(tmp_path: Path) -> None:
    expected = make_payload()
    envelope, _, _ = write_bundle(tmp_path, expected)

    assert verify(tmp_path, envelope) == expected


def test_tampered_raw_payload_is_rejected(tmp_path: Path) -> None:
    envelope, payload_path, _ = write_bundle(tmp_path, make_payload())
    payload_path.write_bytes(payload_path.read_bytes().replace(b"0.12", b"9.99", 1))

    with pytest.raises(ProviderAttestationError, match="digest does not match"):
        verify(tmp_path, envelope)


def test_tamper_cannot_be_hidden_by_replacing_only_payload_digest(tmp_path: Path) -> None:
    envelope, payload_path, _ = write_bundle(tmp_path, make_payload())
    payload_path.write_bytes(payload_path.read_bytes().replace(b"0.12", b"9.99", 1))
    envelope_value = json.loads(envelope.read_text(encoding="utf-8"))
    envelope_value["payload_sha256"] = hashlib.sha256(payload_path.read_bytes()).hexdigest()
    envelope.write_text(json.dumps(envelope_value), encoding="utf-8")

    with pytest.raises(ProviderAttestationError, match="signature verification failed"):
        verify(tmp_path, envelope)


def test_missing_signature_is_rejected(tmp_path: Path) -> None:
    envelope, _, _ = write_bundle(
        tmp_path,
        make_payload(),
        envelope_overrides={"signature_base64": ""},
    )

    with pytest.raises(ProviderAttestationError, match="signature is missing"):
        verify(tmp_path, envelope)


def test_unknown_signer_is_rejected(tmp_path: Path) -> None:
    envelope, _, _ = write_bundle(tmp_path, make_payload())
    value = json.loads(envelope.read_text(encoding="utf-8"))
    value["signer_id"] = "unknown-runner"
    envelope.write_text(json.dumps(value), encoding="utf-8")

    with pytest.raises(ProviderAttestationError, match="unknown or duplicated"):
        verify(tmp_path, envelope)


def test_payload_path_traversal_is_rejected(tmp_path: Path) -> None:
    envelope, _, _ = write_bundle(
        tmp_path,
        make_payload(),
        envelope_overrides={"payload_path": "data/evidence/../../outside.json"},
    )

    with pytest.raises(ProviderAttestationError, match="must stay below data/evidence"):
        verify(tmp_path, envelope)


def test_payload_symlink_is_rejected(tmp_path: Path) -> None:
    envelope, payload_path, _ = write_bundle(tmp_path, make_payload())
    target = payload_path.with_name("actual-payload.json")
    payload_path.rename(target)
    payload_path.symlink_to(target.name)

    with pytest.raises(ProviderAttestationError, match="must not traverse a symlink"):
        verify(tmp_path, envelope)


def test_placeholder_digest_is_rejected_even_when_signature_is_valid(tmp_path: Path) -> None:
    payload = make_payload()
    payload["provider_runs"][0]["provider_usage_sha256"] = "a" * 64
    envelope, _, _ = write_bundle(tmp_path, payload)

    with pytest.raises(ProviderAttestationError, match="placeholder digest"):
        verify(tmp_path, envelope)


def test_future_attestation_time_is_rejected(tmp_path: Path) -> None:
    payload = copy.deepcopy(make_payload())
    payload["verified_at"] = "2026-08-02T00:00:00Z"
    payload["provider_runs"][0]["executed_at"] = "2026-08-02T00:00:00Z"
    payload["provider_runs"][1]["executed_at"] = "2026-08-02T00:00:00Z"
    payload["account_budget_controls"][0]["verified_at"] = "2026-08-02T00:00:00Z"
    payload["account_budget_controls"][1]["verified_at"] = "2026-08-02T00:00:00Z"
    envelope, _, _ = write_bundle(tmp_path, payload)

    with pytest.raises(ProviderAttestationError, match="verification time is in the future"):
        verify(tmp_path, envelope)


def test_release_receipt_is_bound_to_verified_attestation(tmp_path: Path) -> None:
    payload = make_payload()
    write_bundle(tmp_path, payload)

    verified, errors = validate_provider_signed_receipt(
        make_public_receipt(payload),
        release_sha=RELEASE_SHA,
        product_version=PRODUCT_VERSION,
        root=tmp_path,
        now=NOW,
    )

    assert verified == payload
    assert errors == []


def test_generic_and_signed_provider_receipts_are_simultaneously_constructible(
    tmp_path: Path,
) -> None:
    evidence_root = tmp_path / "data" / "evidence"
    evidence_root.mkdir(parents=True)
    contract = GATE_EVIDENCE_CONTRACTS["provider_executions"]
    evidence_items: list[dict[str, Any]] = []
    claims: list[tuple[str, str]] = []
    for item_id in contract["evidence_ids"]:
        if item_id == "EVD-PROVIDER-SIGNED-ATTESTATION":
            continue
        relative = Path("data/evidence") / f"{item_id.casefold()}.json"
        artifact = tmp_path / relative
        artifact.write_text(
            json.dumps({"evidence_id": item_id, "status": "passed"}),
            encoding="utf-8",
        )
        item_digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        evidence_items.append(
            {
                "id": item_id,
                "status": "passed",
                "count": 1,
                "artifact": relative.as_posix(),
                "sha256": item_digest,
            }
        )
        claims.append((item_id, item_digest))

    payload = make_payload()
    payload["claims_bundle_sha256"] = evidence_aggregate_sha256(claims)
    envelope, _, _ = write_bundle(tmp_path, payload)
    envelope_relative = envelope.relative_to(tmp_path).as_posix()
    envelope_digest = hashlib.sha256(envelope.read_bytes()).hexdigest()
    evidence_items.append(
        {
            "id": "EVD-PROVIDER-SIGNED-ATTESTATION",
            "status": "passed",
            "count": 1,
            "artifact": envelope_relative,
            "sha256": envelope_digest,
        }
    )
    all_digests = [(item["id"], item["sha256"]) for item in evidence_items]
    receipt = {
        "receipt_id": "RCT-PROVIDER-EXECUTION-001",
        "evidence_type": "provider-execution",
        "release_sha": RELEASE_SHA,
        "product_version": PRODUCT_VERSION,
        "public_safe": True,
        "reviewer": "independent-reviewer",
        "verified_at": payload["verified_at"],
        "artifact_sha256": evidence_aggregate_sha256(all_digests),
        "evidence_items": evidence_items,
        "attestation_path": envelope_relative,
        "provider_runs": copy.deepcopy(payload["provider_runs"]),
        "account_budget_controls": copy.deepcopy(
            payload["account_budget_controls"]
        ),
    }
    state = {
        "status": "passed",
        "release_sha": RELEASE_SHA,
        "verified_at": payload["verified_at"],
        "required_evidence": list(contract["evidence_ids"]),
        "receipt": receipt,
    }

    generic_errors = validate_gate_receipt(
        "provider_executions",
        state,
        release_sha=RELEASE_SHA,
        product_version=PRODUCT_VERSION,
        root=tmp_path,
        now=NOW,
    )
    verified, signed_errors = validate_provider_signed_receipt(
        receipt,
        release_sha=RELEASE_SHA,
        product_version=PRODUCT_VERSION,
        root=tmp_path,
        now=NOW,
    )

    assert generic_errors == []
    assert verified == payload
    assert signed_errors == []


def test_release_receipt_cannot_claim_success_without_attestation() -> None:
    payload = make_payload()
    receipt = make_public_receipt(payload)
    receipt.pop("attestation_path")

    verified, errors = validate_provider_signed_receipt(
        receipt,
        release_sha=RELEASE_SHA,
        product_version=PRODUCT_VERSION,
    )

    assert verified is None
    assert errors == ["provider execution receipt lacks a signed attestation path"]


def test_release_receipt_cannot_diverge_from_signed_cost(tmp_path: Path) -> None:
    payload = make_payload()
    write_bundle(tmp_path, payload)
    receipt = make_public_receipt(payload)
    receipt["provider_runs"][0]["actual_cost"] = "99.00"

    verified, errors = validate_provider_signed_receipt(
        receipt,
        release_sha=RELEASE_SHA,
        product_version=PRODUCT_VERSION,
        root=tmp_path,
        now=NOW,
    )

    assert verified == payload
    assert "provider receipt provider runs does not match the signed attestation" in errors
