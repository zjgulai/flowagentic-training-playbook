#!/usr/bin/env python3
"""Verify detached, signed Provider execution evidence.

The attestation is deliberately verification-only: signing keys and signing
operations do not belong in this repository.  A trusted runner writes a raw
JSON payload and a small detached envelope below ``data/evidence``.  This
module verifies the exact payload bytes with an allow-listed Ed25519 public
key, then validates the release, Provider, synthetic-data, cleanup, usage and
account-budget claims before returning the parsed payload.

No caller should consume fields from an attestation before
``verify_provider_attestation`` returns successfully.
"""

from __future__ import annotations

import base64
import binascii
import datetime as dt
import decimal
import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

import yaml
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_SEPARATOR = b"FLOWAGENTIC-PROVIDER-ATTESTATION-V1\x00"
MAX_ENVELOPE_BYTES = 64 * 1024
MAX_PAYLOAD_BYTES = 2 * 1024 * 1024
EXPECTED_PROVIDERS = {"DeepSeek", "Kimi"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RELEASE_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SIGNER_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,79}$")
EXPERIMENT_ID_RE = re.compile(r"^EXP-[A-Z0-9-]{4,64}$")
MODEL_RE = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")

_KNOWN_PLACEHOLDER_DIGESTS = {
    "0" * 64,
    "f" * 64,
    hashlib.sha256(b"").hexdigest(),
    hashlib.sha256(b"placeholder").hexdigest(),
    hashlib.sha256(b"todo").hexdigest(),
    hashlib.sha256(b"test").hexdigest(),
    hashlib.sha256(b"example").hexdigest(),
}


class ProviderAttestationError(Exception):
    """Fail-closed Provider attestation verification error."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ProviderAttestationError("trust configuration contains an invalid key") from exc
        if duplicate:
            raise ProviderAttestationError("trust configuration contains a duplicate key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def signature_message(raw_payload: bytes) -> bytes:
    """Return the versioned byte sequence that an external signer must sign."""

    return DOMAIN_SEPARATOR + raw_payload


def _is_placeholder_digest(value: str) -> bool:
    if value in _KNOWN_PLACEHOLDER_DIGESTS:
        return True
    # Reject obvious hand-written/repeated stand-ins without imposing a
    # statistical entropy rule on legitimate SHA-256 values.
    return any(value == value[:width] * (64 // width) for width in (1, 2, 4, 8, 16, 32))


def _require_digest(value: object, label: str) -> str:
    digest = str(value)
    if not SHA256_RE.fullmatch(digest):
        raise ProviderAttestationError(f"{label} is not a lowercase SHA-256 digest")
    if _is_placeholder_digest(digest):
        raise ProviderAttestationError(f"{label} is a placeholder digest")
    return digest


def _validate_all_digest_fields(value: object, location: str = "payload") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            next_location = f"{location}.{key_text}"
            if key_text.endswith("_sha256"):
                _require_digest(item, next_location)
            else:
                _validate_all_digest_fields(item, next_location)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_all_digest_fields(item, f"{location}[{index}]")


def _absolute_without_symlink_resolution(path: Path, project_root: Path) -> Path:
    if path.is_absolute():
        return Path(os.path.abspath(os.fspath(path)))
    return Path(os.path.abspath(os.fspath(project_root / path)))


def _confined_regular_file(
    value: str | Path,
    *,
    project_root: Path,
    relative_base: Path,
    label: str,
    max_bytes: int,
) -> Path:
    """Resolve one regular file while rejecting traversal and every symlink."""

    root = Path(os.path.abspath(os.fspath(project_root)))
    base = Path(os.path.abspath(os.fspath(root / relative_base)))
    candidate = _absolute_without_symlink_resolution(Path(value), root)
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ProviderAttestationError(f"{label} must stay below {relative_base.as_posix()}") from exc

    try:
        relative_to_root = candidate.relative_to(root)
    except ValueError as exc:  # Defensive: relative_base itself must be under root.
        raise ProviderAttestationError(f"{label} is outside the project root") from exc

    cursor = root
    try:
        if cursor.is_symlink():
            raise ProviderAttestationError("project root must not be a symlink")
        for part in relative_to_root.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ProviderAttestationError(f"{label} must not traverse a symlink")
        metadata = os.lstat(candidate)
    except FileNotFoundError as exc:
        raise ProviderAttestationError(f"{label} does not exist") from exc
    except OSError as exc:
        raise ProviderAttestationError(f"{label} cannot be inspected") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise ProviderAttestationError(f"{label} must be a regular file")
    if metadata.st_size > max_bytes:
        raise ProviderAttestationError(f"{label} exceeds its size limit")

    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(base.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ProviderAttestationError(f"{label} escapes its allowed directory") from exc
    return candidate


def _decode_base64(value: object, *, expected_length: int, label: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise ProviderAttestationError(f"{label} is missing")
    try:
        decoded = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ProviderAttestationError(f"{label} is not valid base64") from exc
    if len(decoded) != expected_length:
        raise ProviderAttestationError(f"{label} has an invalid length")
    return decoded


def _load_json_object(raw: bytes, label: str) -> dict[str, Any]:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ProviderAttestationError(f"{label} contains a duplicate JSON key")
            result[key] = value
        return result

    def reject_nonstandard_number(value: str) -> object:
        raise ProviderAttestationError(f"{label} contains a non-standard number: {value}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonstandard_number,
        )
    except UnicodeDecodeError as exc:
        raise ProviderAttestationError(f"{label} is not UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ProviderAttestationError(f"{label} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise ProviderAttestationError(f"{label} must be a JSON object")
    return value


def _load_trust_configuration(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except UnicodeDecodeError as exc:
        raise ProviderAttestationError("trust configuration is not UTF-8") from exc
    except yaml.YAMLError as exc:
        raise ProviderAttestationError("trust configuration is invalid YAML") from exc
    if not isinstance(value, dict):
        raise ProviderAttestationError("trust configuration must be a YAML object")
    if value.get("schema_version") != 1:
        raise ProviderAttestationError("trust configuration schema version must be 1")
    if value.get("status") != "active":
        raise ProviderAttestationError("Provider attestation trust is blocked")
    if not isinstance(value.get("signers"), list) or not value["signers"]:
        raise ProviderAttestationError("Provider attestation trust has no active signers")
    return value


def _parse_timestamp(value: object, label: str) -> dt.datetime:
    if not isinstance(value, str) or not value:
        raise ProviderAttestationError(f"{label} is missing")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProviderAttestationError(f"{label} is not an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ProviderAttestationError(f"{label} must include a timezone")
    return parsed.astimezone(dt.UTC)


def _positive_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ProviderAttestationError(f"{label} must be a positive integer")
    return value


def _positive_amount(value: object, label: str) -> decimal.Decimal:
    try:
        amount = decimal.Decimal(str(value))
    except decimal.InvalidOperation as exc:
        raise ProviderAttestationError(f"{label} is not a decimal amount") from exc
    if not amount.is_finite() or amount <= 0:
        raise ProviderAttestationError(f"{label} must be finite and positive")
    return amount


def _validate_payload(
    payload: dict[str, Any],
    *,
    expected_release_sha: str,
    expected_product_version: str,
    now: dt.datetime,
) -> None:
    if payload.get("schema_version") != 1:
        raise ProviderAttestationError("Provider payload schema version must be 1")
    if payload.get("evidence_type") != "provider-execution":
        raise ProviderAttestationError("Provider payload evidence_type is invalid")
    if payload.get("release_sha") != expected_release_sha:
        raise ProviderAttestationError("Provider payload release SHA does not match")
    if str(payload.get("product_version", "")) != expected_product_version:
        raise ProviderAttestationError("Provider payload product version does not match")
    if payload.get("public_safe") is not True:
        raise ProviderAttestationError("Provider payload is not marked public-safe")

    verified_at = _parse_timestamp(payload.get("verified_at"), "payload.verified_at")
    if verified_at > now:
        raise ProviderAttestationError("Provider payload verification time is in the future")
    _require_digest(
        payload.get("claims_bundle_sha256"),
        "payload.claims_bundle_sha256",
    )

    runs = payload.get("provider_runs")
    if not isinstance(runs, list) or len(runs) != 2:
        raise ProviderAttestationError("Provider payload must contain exactly two runs")
    run_providers: list[str] = []
    total_cost = decimal.Decimal(0)
    for index, run in enumerate(runs):
        label = f"payload.provider_runs[{index}]"
        if not isinstance(run, dict):
            raise ProviderAttestationError(f"{label} must be an object")
        provider = run.get("provider")
        if provider not in EXPECTED_PROVIDERS:
            raise ProviderAttestationError(f"{label}.provider is invalid")
        run_providers.append(str(provider))
        if run.get("status") != "success" or run.get("synthetic_data") is not True:
            raise ProviderAttestationError(f"{label} is not a successful synthetic run")
        if run.get("release_sha") != expected_release_sha:
            raise ProviderAttestationError(f"{label}.release_sha does not match")
        if str(run.get("product_version", "")) != expected_product_version:
            raise ProviderAttestationError(f"{label}.product_version does not match")
        if not EXPERIMENT_ID_RE.fullmatch(str(run.get("experiment_id", ""))):
            raise ProviderAttestationError(f"{label}.experiment_id is invalid")
        if not MODEL_RE.fullmatch(str(run.get("model", ""))):
            raise ProviderAttestationError(f"{label}.model is invalid")
        fixture = run.get("fixture")
        if not isinstance(fixture, str) or not re.fullmatch(r"synthetic-[A-Za-z0-9._-]{2,120}", fixture):
            raise ProviderAttestationError(f"{label}.fixture is not synthetic")
        _require_digest(run.get("fixture_sha256"), f"{label}.fixture_sha256")
        _positive_integer(run.get("input_tokens"), f"{label}.input_tokens")
        _positive_integer(run.get("output_tokens"), f"{label}.output_tokens")
        _positive_integer(run.get("latency_ms"), f"{label}.latency_ms")
        total_cost += _positive_amount(run.get("actual_cost"), f"{label}.actual_cost")
        if run.get("currency") != "CNY":
            raise ProviderAttestationError(f"{label}.currency must be CNY")
        if run.get("cleanup_status") != "passed":
            raise ProviderAttestationError(f"{label}.cleanup_status is not passed")
        if run.get("residual_object_count") != 0:
            raise ProviderAttestationError(f"{label} has residual training objects")
        _require_digest(
            run.get("cleanup_receipt_sha256"),
            f"{label}.cleanup_receipt_sha256",
        )
        _require_digest(
            run.get("provider_usage_sha256"),
            f"{label}.provider_usage_sha256",
        )
        executed_at = _parse_timestamp(run.get("executed_at"), f"{label}.executed_at")
        if executed_at > verified_at or executed_at > now:
            raise ProviderAttestationError(f"{label}.executed_at is in the future")
    if set(run_providers) != EXPECTED_PROVIDERS or len(set(run_providers)) != 2:
        raise ProviderAttestationError("Provider payload needs one DeepSeek and one Kimi run")
    if total_cost > decimal.Decimal("300"):
        raise ProviderAttestationError("Provider run costs exceed the shared CNY 300 cap")

    controls = payload.get("account_budget_controls")
    if not isinstance(controls, list) or len(controls) != 2:
        raise ProviderAttestationError("Provider payload must contain exactly two account controls")
    control_providers: list[str] = []
    aggregate_limit = decimal.Decimal(0)
    for index, control in enumerate(controls):
        label = f"payload.account_budget_controls[{index}]"
        if not isinstance(control, dict):
            raise ProviderAttestationError(f"{label} must be an object")
        provider = control.get("provider")
        if provider not in EXPECTED_PROVIDERS:
            raise ProviderAttestationError(f"{label}.provider is invalid")
        control_providers.append(str(provider))
        if control.get("status") != "passed" or control.get("auto_recharge") is not False:
            raise ProviderAttestationError(f"{label} does not prove a disabled auto-recharge")
        if control.get("currency") != "CNY":
            raise ProviderAttestationError(f"{label}.currency must be CNY")
        aggregate_limit += _positive_amount(control.get("hard_limit"), f"{label}.hard_limit")
        _require_digest(control.get("receipt_sha256"), f"{label}.receipt_sha256")
        control_time = _parse_timestamp(control.get("verified_at"), f"{label}.verified_at")
        if control_time > verified_at or control_time > now:
            raise ProviderAttestationError(f"{label}.verified_at is in the future")
    if set(control_providers) != EXPECTED_PROVIDERS or len(set(control_providers)) != 2:
        raise ProviderAttestationError(
            "Provider payload needs one DeepSeek and one Kimi account control"
        )
    if aggregate_limit > decimal.Decimal("300"):
        raise ProviderAttestationError("Provider account hard limits exceed the shared CNY 300 cap")

    _validate_all_digest_fields(payload)


def verify_provider_attestation(
    attestation_path: str | Path,
    *,
    expected_release_sha: str,
    expected_product_version: str,
    project_root: Path = ROOT,
    trust_config_path: str | Path | None = None,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    """Verify and return one signed Provider execution payload.

    ``attestation_path`` and its detached ``payload_path`` must both be regular,
    non-symlink files below ``data/evidence``.  The trust configuration is
    similarly confined below ``data/trust``.  Any malformed, untrusted,
    mismatched or incomplete evidence raises :class:`ProviderAttestationError`.
    """

    if not RELEASE_SHA_RE.fullmatch(expected_release_sha):
        raise ProviderAttestationError("expected release SHA must be 40 lowercase hex characters")
    if not isinstance(expected_product_version, str) or not expected_product_version.strip():
        raise ProviderAttestationError("expected product version is missing")
    current_time = now or dt.datetime.now(dt.UTC)
    if current_time.tzinfo is None or current_time.utcoffset() is None:
        raise ProviderAttestationError("verification time must include a timezone")
    current_time = current_time.astimezone(dt.UTC)

    root = Path(project_root)
    envelope_file = _confined_regular_file(
        attestation_path,
        project_root=root,
        relative_base=Path("data/evidence"),
        label="Provider attestation envelope",
        max_bytes=MAX_ENVELOPE_BYTES,
    )
    envelope = _load_json_object(envelope_file.read_bytes(), "Provider attestation envelope")
    expected_envelope_keys = {
        "schema_version",
        "algorithm",
        "signer_id",
        "payload_path",
        "payload_sha256",
        "signature_base64",
    }
    if set(envelope) != expected_envelope_keys:
        raise ProviderAttestationError("Provider attestation envelope fields are invalid")
    if envelope.get("schema_version") != 1 or envelope.get("algorithm") != "Ed25519":
        raise ProviderAttestationError("Provider attestation algorithm or schema is invalid")
    signer_id = envelope.get("signer_id")
    if not isinstance(signer_id, str) or not SIGNER_ID_RE.fullmatch(signer_id):
        raise ProviderAttestationError("Provider attestation signer id is invalid")
    payload_path = envelope.get("payload_path")
    if not isinstance(payload_path, str) or Path(payload_path).is_absolute():
        raise ProviderAttestationError("Provider attestation payload path must be relative")
    payload_file = _confined_regular_file(
        payload_path,
        project_root=root,
        relative_base=Path("data/evidence"),
        label="Provider attestation payload",
        max_bytes=MAX_PAYLOAD_BYTES,
    )
    raw_payload = payload_file.read_bytes()
    actual_payload_digest = hashlib.sha256(raw_payload).hexdigest()
    declared_payload_digest = _require_digest(
        envelope.get("payload_sha256"), "Provider attestation payload_sha256"
    )
    if actual_payload_digest != declared_payload_digest:
        raise ProviderAttestationError("Provider attestation payload digest does not match")

    trust_value = trust_config_path or Path("data/trust/provider-attestors.yml")
    trust_file = _confined_regular_file(
        trust_value,
        project_root=root,
        relative_base=Path("data/trust"),
        label="Provider attestor trust configuration",
        max_bytes=MAX_ENVELOPE_BYTES,
    )
    trust = _load_trust_configuration(trust_file)
    signer_entries = [
        item
        for item in trust["signers"]
        if isinstance(item, dict) and item.get("signer_id") == signer_id
    ]
    if len(signer_entries) != 1:
        raise ProviderAttestationError("Provider attestation signer is unknown or duplicated")
    signer = signer_entries[0]
    if signer.get("status") != "active" or signer.get("algorithm") != "Ed25519":
        raise ProviderAttestationError("Provider attestation signer is not active")
    public_key_bytes = _decode_base64(
        signer.get("public_key_base64"),
        expected_length=32,
        label="Provider attestor public key",
    )
    if public_key_bytes == b"\x00" * 32:
        raise ProviderAttestationError("Provider attestor public key is invalid")
    signature = _decode_base64(
        envelope.get("signature_base64"),
        expected_length=64,
        label="Provider attestation signature",
    )
    try:
        Ed25519PublicKey.from_public_bytes(public_key_bytes).verify(
            signature,
            signature_message(raw_payload),
        )
    except (InvalidSignature, ValueError) as exc:
        raise ProviderAttestationError("Provider attestation signature verification failed") from exc

    payload = _load_json_object(raw_payload, "Provider attestation payload")
    _validate_payload(
        payload,
        expected_release_sha=expected_release_sha,
        expected_product_version=expected_product_version,
        now=current_time,
    )

    verified_at = _parse_timestamp(payload.get("verified_at"), "payload.verified_at")
    not_before = _parse_timestamp(signer.get("not_before"), "trusted signer not_before")
    if verified_at < not_before:
        raise ProviderAttestationError("Provider attestation predates signer trust")
    if signer.get("not_after") is not None:
        not_after = _parse_timestamp(signer.get("not_after"), "trusted signer not_after")
        if not_after < not_before:
            raise ProviderAttestationError("Provider attestor trust interval is invalid")
        if verified_at > not_after:
            raise ProviderAttestationError("Provider attestation signer trust has expired")
    return payload


__all__ = [
    "DOMAIN_SEPARATOR",
    "ProviderAttestationError",
    "signature_message",
    "verify_provider_attestation",
]
