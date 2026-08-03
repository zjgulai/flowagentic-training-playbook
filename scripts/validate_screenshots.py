#!/usr/bin/env python3
"""Validate screenshot plan and evidence from the actual image bytes.

The manifest's human-entered ``passed`` flags are never sufficient for a
release.  This validator resolves files under fixed screenshot roots, verifies
both image hashes, reruns OCR and secret rules over both images, and binds the
result to a hashed scan receipt and the exact product release SHA.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from PIL import Image

from check_public_safety import (
    ALLOWED_IMAGE_METADATA_KEYS,
    OCRUnavailable,
    image_ruleset_sha256,
    scan_image,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path("data/manifests/screenshots.yml")
PLAN_PATH = Path("data/manifests/screenshot-plan.yml")
SOURCE_ROOT = Path("data/screenshots/source")
ANNOTATED_ROOT = Path("docs/assets/screenshots")
RECEIPT_ROOT = Path("data/screenshots/receipts")
VALIDATOR_NAME = "flowagentic-screenshot-validator"
VALIDATOR_VERSION = "3.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RELEASE_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
APPROVAL_ID_RE = re.compile(r"^SHR-[A-Z0-9][A-Z0-9_-]{5,63}$")
SCREENSHOT_IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]\n]+)\]\((?P<src>[^)\s]+)\)\s*\{(?P<attrs>[^}\n]*)\}"
)
SCREENSHOT_ID_ATTR_RE = re.compile(
    r"\bdata-screenshot-id\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s}]+))"
)

PLAN_MANIFEST_FIELDS = {
    "sop_id": "sop_id",
    "step": "step",
    "route": "route",
    "planned_state": "state",
    "role": "role",
    "viewport": "viewport",
    "locale": "locale",
    "provider": "provider",
    "release_sha": "release_sha",
    "doc_path": "doc_path",
    "fixture": "fixture",
    "feature_status": "feature_status",
    "theme": "theme",
}

ALLOWED_STATES = {
    "before",
    "during",
    "success",
    "empty",
    "error",
    "permission-denied",
    "rate-limited",
    "recovery",
}
CORE_SOPS = {
    "chatflow",
    "agentflow-v2",
    "executions",
    "assistants",
    "marketplace",
    "tools",
    "credentials",
    "variables",
    "api-keys",
    "document-store",
}
CORE_STATES = {"before", "during", "success"}
HIGH_RISK_STATES = {"before", "during", "success", "error", "recovery"}
EXT_SEMANTICS = {
    "EXT-001": ("/datasets", "none", "feature-gated"),
    "EXT-002": ("/dataset_rows/:id", "none", "feature-gated"),
    "EXT-003": ("/evaluators", "none", "feature-gated"),
    "EXT-004": ("/evaluations", "none", "feature-gated"),
    "EXT-005": ("/users", "none", "feature-gated"),
    "EXT-006": ("/roles", "none", "feature-gated"),
    "EXT-007": ("/workspaces", "none", "feature-gated"),
    "EXT-008": ("/sso-config", "none", "feature-gated"),
    "EXT-009": ("/login-activity", "none", "feature-gated"),
    "EXT-010": ("/logs", "none", "feature-gated"),
    "EXT-011": ("/agentflows", "none", "experimental"),
    "EXT-012": ("/executions", "none", "experimental"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _resolve_confined_path(
    value: Any,
    allowed_root: Path,
    suffixes: set[str],
) -> tuple[Path | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, "path is missing"
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None, "path must be a normalized repository-relative path"
    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return None, "symlinked screenshot evidence is forbidden"
    allowed = (ROOT / allowed_root).resolve()
    resolved = (ROOT / relative).resolve()
    try:
        resolved.relative_to(allowed)
    except ValueError:
        return None, f"path is outside {allowed_root.as_posix()}"
    if relative.suffix.lower() not in suffixes:
        return None, f"file extension must be one of {sorted(suffixes)}"
    if not resolved.is_file():
        return None, "file does not exist"
    return resolved, None


def _inventory_evidence_root(root: Path, suffixes: set[str]) -> tuple[set[str], list[str]]:
    absolute_root = ROOT / root
    if not absolute_root.exists():
        return set(), []
    files: set[str] = set()
    errors: list[str] = []
    for path in absolute_root.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"{relative}: symlinked screenshot evidence is forbidden")
            continue
        if path.suffix.lower() not in suffixes:
            errors.append(f"{relative}: unexpected file type in screenshot evidence root")
            continue
        files.add(relative)
    return files, errors


def _validate_doc_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return "doc_path is missing"
    relative = Path(value)
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or not relative.parts
        or relative.parts[0] != "docs"
        or relative.suffix.lower() != ".md"
    ):
        return "doc_path must be a normalized Markdown path below docs/"
    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return "doc_path may not traverse a symlink"
    resolved = (ROOT / relative).resolve()
    try:
        resolved.relative_to((ROOT / "docs").resolve())
    except ValueError:
        return "doc_path is outside docs/"
    if not resolved.is_file():
        return "doc_path does not exist"
    return None


def _parse_page_screenshot_contract(path: Path) -> tuple[list[str], dict[str, tuple[str, str]]]:
    """Return frontmatter IDs and actual screenshot image references."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [], {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return [], {}
    metadata = yaml.safe_load(text[4:end]) or {}
    declared = metadata.get("screenshot_ids", []) if isinstance(metadata, dict) else []
    declared_ids = [str(value) for value in declared] if isinstance(declared, list) else []
    references: dict[str, tuple[str, str]] = {}
    for match in SCREENSHOT_IMAGE_RE.finditer(text[end + 5 :]):
        attr_match = SCREENSHOT_ID_ATTR_RE.search(match.group("attrs"))
        if attr_match is None:
            continue
        identifier = next(value for value in attr_match.groups() if value is not None)
        if identifier in references:
            references[identifier] = ("<duplicate>", "<duplicate>")
        else:
            references[identifier] = (match.group("src"), match.group("alt").strip())
    return declared_ids, references


def validate_page_bindings(
    plan: dict[str, Any],
    manifest: dict[str, Any],
) -> list[str]:
    """Bind every release screenshot to the exact page image rendered from Markdown."""

    errors: list[str] = []
    planned_by_doc: dict[str, list[str]] = defaultdict(list)
    for item in plan.get("shots", []):
        if isinstance(item, dict) and item.get("required_for_release"):
            planned_by_doc[str(item.get("doc_path", ""))].append(str(item.get("id", "")))
    manifest_by_id = {
        str(item.get("id")): item
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }

    for doc_path, planned_ids in sorted(planned_by_doc.items()):
        path = ROOT / doc_path
        if not path.is_file():
            errors.append(f"{doc_path}: screenshot page does not exist")
            continue
        declared_ids, references = _parse_page_screenshot_contract(path)
        expected = set(planned_ids)
        if len(declared_ids) != len(set(declared_ids)):
            errors.append(f"{doc_path}: screenshot_ids contains duplicates")
        if set(declared_ids) != expected:
            errors.append(f"{doc_path}: frontmatter screenshot_ids do not match its plan")
        if set(references) != expected:
            errors.append(f"{doc_path}: rendered screenshot references do not match its plan")

        for identifier in sorted(expected & set(references)):
            src, alt = references[identifier]
            if src == "<duplicate>":
                errors.append(f"{doc_path}: screenshot reference is duplicated: {identifier}")
                continue
            item = manifest_by_id.get(identifier)
            if item is None:
                errors.append(f"{doc_path}: screenshot reference lacks manifest item: {identifier}")
                continue
            parsed = urlsplit(src)
            if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
                errors.append(f"{doc_path}: screenshot source must be repository-relative: {identifier}")
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            expected_file = (ROOT / str(item.get("annotated_file", ""))).resolve()
            if resolved != expected_file:
                errors.append(f"{doc_path}: screenshot source does not match manifest: {identifier}")
            if not alt or alt != str(item.get("alt_text", "")).strip():
                errors.append(f"{doc_path}: screenshot alt text does not match manifest: {identifier}")
    return errors


def validate_plan(plan: dict[str, Any], *, release: bool = False) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != 3:
        errors.append("screenshot plan schema_version must be 3")
    shots = plan.get("shots")
    if not isinstance(shots, list):
        return ["screenshot plan shots must be a list"]
    required = [item for item in shots if isinstance(item, dict) and item.get("required_for_release")]
    if plan.get("count") != len(shots):
        errors.append("screenshot plan count does not match shots length")
    if not 180 <= len(shots) <= 260:
        errors.append(f"screenshot plan total must contain 180-260 shots, found {len(shots)}")
    if len(required) != len(shots):
        errors.append("every planned screenshot must be required for the first release")

    ids = [str(item.get("id", "")) for item in shots if isinstance(item, dict)]
    duplicate_ids = sorted(identifier for identifier, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        errors.append("screenshot plan contains duplicate ids: " + ", ".join(duplicate_ids[:5]))

    states_by_sop: dict[str, set[str]] = defaultdict(set)
    states_by_risk_case: dict[str, set[str]] = defaultdict(set)
    ext_seen: dict[str, tuple[str, str, str]] = {}
    unbound_release_ids: list[str] = []
    mismatched_release_ids: list[str] = []
    uncaptured_release_ids: list[str] = []
    for index, item in enumerate(shots):
        if not isinstance(item, dict):
            errors.append(f"screenshot plan item {index} is not an object")
            continue
        identifier = str(item.get("id", f"#{index}"))
        sop_id = item.get("sop_id")
        state = item.get("planned_state")
        route = item.get("route")
        provider = item.get("provider")
        status = item.get("feature_status")
        doc_path_error = _validate_doc_path(item.get("doc_path"))
        description = str(item.get("description", ""))
        if state not in ALLOWED_STATES:
            errors.append(f"{identifier}: invalid planned_state")
        if isinstance(sop_id, str) and isinstance(state, str):
            states_by_sop[sop_id].add(state)
        if not isinstance(route, str) or not route.startswith("/") or "://" in route:
            errors.append(f"{identifier}: route must be a product-relative route")
        if provider not in {"none", "DeepSeek", "Kimi"}:
            errors.append(f"{identifier}: invalid provider")
        if status not in {
            "production-enabled",
            "feature-gated",
            "deprecated",
            "experimental",
            "upstream-only",
        }:
            errors.append(f"{identifier}: invalid feature_status")
        if doc_path_error:
            errors.append(f"{identifier}: {doc_path_error}")
        if "Kimi" in description and provider != "Kimi":
            errors.append(f"{identifier}: Kimi description must bind provider=Kimi")
        if "DeepSeek" in description and provider != "DeepSeek":
            errors.append(f"{identifier}: DeepSeek description must bind provider=DeepSeek")
        risk_case = item.get("risk_case")
        if risk_case is not None:
            if not isinstance(risk_case, str) or not risk_case.strip():
                errors.append(f"{identifier}: risk_case must be a non-empty string")
            elif isinstance(state, str):
                states_by_risk_case[risk_case].add(state)
        if identifier.startswith("EXT-"):
            ext_seen[identifier] = (str(route), str(provider), str(status))
        if release:
            release_sha = item.get("release_sha")
            if not isinstance(release_sha, str) or not RELEASE_SHA_RE.fullmatch(release_sha):
                unbound_release_ids.append(identifier)
            elif release_sha != plan.get("release_sha"):
                mismatched_release_ids.append(identifier)
            if item.get("capture_status") != "captured-verified":
                uncaptured_release_ids.append(identifier)

    if release:
        plan_release_sha = plan.get("release_sha")
        if not isinstance(plan_release_sha, str) or not RELEASE_SHA_RE.fullmatch(plan_release_sha):
            errors.append("release screenshot plan must bind a 40-character release SHA")
        if unbound_release_ids:
            errors.append(
                f"{len(unbound_release_ids)} release plan item(s) are not bound to a release SHA"
            )
        if mismatched_release_ids:
            errors.append(
                f"{len(mismatched_release_ids)} release plan item(s) do not match plan release SHA"
            )
        if uncaptured_release_ids:
            errors.append(
                f"{len(uncaptured_release_ids)} release plan item(s) are not captured-verified"
            )

    missing_core = sorted(CORE_SOPS - set(states_by_sop))
    if missing_core:
        errors.append("screenshot plan is missing core SOPs: " + ", ".join(missing_core))
    for sop_id in sorted(CORE_SOPS & set(states_by_sop)):
        missing = sorted(CORE_STATES - states_by_sop[sop_id])
        if missing:
            errors.append(f"{sop_id}: core SOP lacks states: {', '.join(missing)}")
    if not states_by_risk_case:
        errors.append("screenshot plan contains no explicit high-risk action case")
    for risk_case, states in sorted(states_by_risk_case.items()):
        missing = sorted(HIGH_RISK_STATES - states)
        if missing:
            errors.append(f"risk case {risk_case} lacks states: {', '.join(missing)}")

    missing_ext = sorted(set(EXT_SEMANTICS) - set(ext_seen))
    extra_ext = sorted(set(ext_seen) - set(EXT_SEMANTICS))
    if missing_ext:
        errors.append("screenshot plan is missing EXT entries: " + ", ".join(missing_ext))
    if extra_ext:
        errors.append("screenshot plan has unknown EXT entries: " + ", ".join(extra_ext))
    for identifier, expected in EXT_SEMANTICS.items():
        if identifier in ext_seen and ext_seen[identifier] != expected:
            errors.append(
                f"{identifier}: route/provider/status {ext_seen[identifier]} does not match {expected}"
            )
    return errors


def _validate_hash_reuse_group(
    *,
    hash_field: str,
    actual_hash: str,
    occurrences: list[tuple[str, dict[str, Any]]],
) -> list[str]:
    """Validate a deliberate duplicate-image exception without printing bytes/hash."""

    errors: list[str] = []
    related_ids = sorted(identifier for identifier, _item in occurrences)
    approvals: list[dict[str, Any]] = []
    for identifier, item in occurrences:
        approval = item.get("hash_reuse_approval")
        if not isinstance(approval, dict):
            errors.append(
                f"{identifier}: reused {hash_field} requires structured hash_reuse_approval"
            )
            continue
        approvals.append(approval)
        if approval.get("status") != "approved":
            errors.append(f"{identifier}: hash reuse approval status must be approved")
        if not APPROVAL_ID_RE.fullmatch(str(approval.get("approval_id", ""))):
            errors.append(f"{identifier}: hash reuse approval_id is invalid")
        if not isinstance(approval.get("approved_by"), str) or len(
            approval.get("approved_by", "").strip()
        ) < 3:
            errors.append(f"{identifier}: hash reuse approved_by is missing")
        if not isinstance(approval.get("reason"), str) or len(
            approval.get("reason", "").strip()
        ) < 20:
            errors.append(f"{identifier}: hash reuse reason must be specific")
        if _parse_datetime(approval.get("approved_at")) is None:
            errors.append(f"{identifier}: hash reuse approved_at must be timezone-aware")
        hash_types = approval.get("hash_types")
        valid_hash_types = (
            isinstance(hash_types, list)
            and bool(hash_types)
            and all(isinstance(value, str) for value in hash_types)
        )
        if (
            not valid_hash_types
            or any(
                value not in {"source_sha256", "annotated_sha256"}
                for value in hash_types or []
            )
            or len(hash_types or []) != len(set(hash_types or []))
            or hash_field not in (hash_types or [])
        ):
            errors.append(f"{identifier}: hash reuse approval does not cover {hash_field}")
        screenshot_ids = approval.get("screenshot_ids")
        if (
            not isinstance(screenshot_ids, list)
            or not all(isinstance(value, str) for value in screenshot_ids)
            or sorted(screenshot_ids) != related_ids
        ):
            errors.append(
                f"{identifier}: hash reuse approval screenshot_ids do not match reuse group"
            )
        approved_hashes = approval.get("approved_hashes")
        if (
            not isinstance(approved_hashes, dict)
            or approved_hashes.get(hash_field) != actual_hash
            or any(
                key not in {"source_sha256", "annotated_sha256"}
                or not SHA256_RE.fullmatch(str(value))
                for key, value in approved_hashes.items()
            )
        ):
            errors.append(f"{identifier}: hash reuse approval is not bound to current bytes")

    if len(approvals) == len(occurrences):
        approval_ids = {str(approval.get("approval_id", "")) for approval in approvals}
        if len(approval_ids) != 1:
            errors.append(
                f"{', '.join(related_ids)}: reused {hash_field} lacks one shared approval_id"
            )
        canonical = {
            (
                repr(approval.get("status")),
                repr(approval.get("approved_by")),
                repr(approval.get("approved_at")),
                repr(approval.get("reason")),
                tuple(sorted(map(str, approval.get("hash_types", []))))
                if isinstance(approval.get("hash_types"), list)
                else (),
                tuple(sorted(map(str, approval.get("screenshot_ids", []))))
                if isinstance(approval.get("screenshot_ids"), list)
                else (),
                tuple(
                    sorted(
                        (str(key), str(value))
                        for key, value in approval.get("approved_hashes", {}).items()
                    )
                )
                if isinstance(approval.get("approved_hashes"), dict)
                else (),
            )
            for approval in approvals
        }
        if len(canonical) != 1:
            errors.append(
                f"{', '.join(related_ids)}: reused {hash_field} approvals are inconsistent"
            )
    return errors


def _validate_receipt(
    *,
    identifier: str,
    item: dict[str, Any],
    receipt_path: Path,
    source_hash: str,
    annotated_hash: str,
    source_scan: dict[str, Any],
    annotated_scan: dict[str, Any],
    source_findings: list[dict[str, object]],
    annotated_findings: list[dict[str, object]],
) -> list[str]:
    errors: list[str] = []
    receipt = load_yaml(receipt_path)
    expected_top_level = {
        "schema_version": 1,
        "screenshot_id": identifier,
        "release_sha": item.get("release_sha"),
        "validator": {"name": VALIDATOR_NAME, "version": VALIDATOR_VERSION},
        "status": "passed",
    }
    for key, expected_value in expected_top_level.items():
        if receipt.get(key) != expected_value:
            errors.append(f"{identifier}: scan receipt field {key} does not bind current evidence")

    for label, expected_file, expected_hash, current_scan in (
        ("source", item.get("source_file"), source_hash, source_scan),
        ("annotated", item.get("annotated_file"), annotated_hash, annotated_scan),
    ):
        section = receipt.get(label)
        if not isinstance(section, dict):
            errors.append(f"{identifier}: scan receipt {label} evidence is missing")
            continue
        if section.get("file") != expected_file or section.get("sha256") != expected_hash:
            errors.append(f"{identifier}: scan receipt {label} does not bind current image bytes")
        recorded_scan = section.get("ocr")
        if not isinstance(recorded_scan, dict):
            errors.append(f"{identifier}: scan receipt {label} OCR evidence is missing")
            continue
        if recorded_scan.get("engine") != "tesseract":
            errors.append(f"{identifier}: scan receipt {label} OCR engine is invalid")
        if recorded_scan.get("languages") != ["chi_sim", "eng"]:
            errors.append(f"{identifier}: scan receipt {label} OCR languages are invalid")
        if recorded_scan.get("psm") != "11":
            errors.append(f"{identifier}: scan receipt {label} OCR PSM is invalid")
        if recorded_scan.get("ruleset_sha256") != image_ruleset_sha256():
            errors.append(f"{identifier}: scan receipt {label} ruleset is stale")
        if not isinstance(recorded_scan.get("engine_version"), str) or not recorded_scan.get(
            "engine_version"
        ):
            errors.append(f"{identifier}: scan receipt {label} OCR version is missing")
        if not SHA256_RE.fullmatch(str(recorded_scan.get("text_sha256", ""))):
            errors.append(f"{identifier}: scan receipt {label} OCR text digest is invalid")
        if not isinstance(recorded_scan.get("character_count"), int) or recorded_scan.get(
            "character_count", 0
        ) < 4:
            errors.append(f"{identifier}: scan receipt {label} OCR text is insufficient")
        # OCR output can vary across Tesseract versions.  The release gate still
        # reruns OCR over the current bytes and current rules.  When the engine
        # version matches, require byte-for-byte normalized OCR evidence too.
        if recorded_scan.get("engine_version") == current_scan.get("engine_version"):
            if recorded_scan.get("text_sha256") != current_scan.get("text_sha256"):
                errors.append(f"{identifier}: scan receipt {label} OCR digest mismatch")

    secret_scan = receipt.get("secret_scan")
    expected_secret_scan = {
        "ruleset_sha256": image_ruleset_sha256(),
        "source_findings": 0,
        "annotated_findings": 0,
    }
    if secret_scan != expected_secret_scan:
        errors.append(f"{identifier}: scan receipt must report zero findings under current rules")
    if source_findings or annotated_findings:
        errors.append(f"{identifier}: current OCR rescan contradicts the passed receipt")
    captured_at = _parse_datetime(item.get("captured_at"))
    scanned_at = _parse_datetime(receipt.get("scanned_at"))
    if scanned_at is None:
        errors.append(f"{identifier}: scan receipt scanned_at must be timezone-aware")
    elif captured_at is not None and scanned_at < captured_at:
        errors.append(f"{identifier}: scan receipt predates screenshot capture")
    return errors


def validate_manifest(
    manifest: dict[str, Any],
    plan: dict[str, Any],
    *,
    release: bool,
) -> list[str]:
    errors = validate_plan(plan, release=release)
    if manifest.get("schema_version") != 3:
        errors.append("screenshot manifest schema_version must be 3")
    items = manifest.get("screenshots")
    if not isinstance(items, list):
        return errors + ["screenshot manifest screenshots must be a list"]
    if release and not items:
        errors.append("release requires captured screenshots")
    if release and manifest.get("capture_status") != "passed":
        errors.append("release requires screenshot manifest capture_status=passed")
    manifest_release_sha = manifest.get("release_sha")
    if release and (
        not isinstance(manifest_release_sha, str)
        or not RELEASE_SHA_RE.fullmatch(manifest_release_sha)
    ):
        errors.append("release screenshot manifest must bind a 40-character release SHA")
    if release and plan.get("release_sha") != manifest_release_sha:
        errors.append("screenshot plan and manifest release SHA do not match")

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    plan_by_id = {
        str(item.get("id")): item
        for item in plan.get("shots", [])
        if isinstance(item, dict)
    }
    hash_occurrences: dict[str, dict[str, list[tuple[str, dict[str, Any]]]]] = {
        "source_sha256": defaultdict(list),
        "annotated_sha256": defaultdict(list),
    }
    manifest_sources: set[str] = set()
    manifest_annotated: set[str] = set()
    manifest_receipts: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("screenshot manifest contains a non-object item")
            continue
        identifier = str(item.get("id", "<unknown>"))
        if identifier in seen_ids:
            errors.append(f"{identifier}: duplicate manifest id")
        seen_ids.add(identifier)
        if release and item.get("release_sha") != manifest_release_sha:
            errors.append(f"{identifier}: item release SHA does not match manifest")
        if release:
            planned = plan_by_id.get(identifier)
            if planned is None:
                errors.append(f"{identifier}: no matching screenshot plan item")
            else:
                for plan_field, manifest_field in PLAN_MANIFEST_FIELDS.items():
                    if item.get(manifest_field) != planned.get(plan_field):
                        errors.append(
                            f"{identifier}: manifest {manifest_field} does not match plan {plan_field}"
                        )
                if item.get("risk_case") != planned.get("risk_case"):
                    errors.append(f"{identifier}: manifest risk_case does not match plan")

        source_path, source_path_error = _resolve_confined_path(
            item.get("source_file"), SOURCE_ROOT, {".png"}
        )
        annotated_path, annotated_path_error = _resolve_confined_path(
            item.get("annotated_file"), ANNOTATED_ROOT, {".webp"}
        )
        receipt_path, receipt_path_error = _resolve_confined_path(
            item.get("scan_receipt"), RECEIPT_ROOT, {".yml", ".yaml"}
        )
        for label, value, path_error in (
            ("source_file", item.get("source_file"), source_path_error),
            ("annotated_file", item.get("annotated_file"), annotated_path_error),
            ("scan_receipt", item.get("scan_receipt"), receipt_path_error),
        ):
            if path_error:
                if release or value:
                    errors.append(f"{identifier}: {label} {path_error}")
            elif isinstance(value, str):
                if value in seen_files:
                    errors.append(f"{identifier}: evidence path is reused: {label}")
                seen_files.add(value)
        if source_path is None or annotated_path is None or receipt_path is None:
            continue
        manifest_sources.add(str(item.get("source_file")))
        manifest_annotated.add(str(item.get("annotated_file")))
        manifest_receipts.add(str(item.get("scan_receipt")))
        if source_path == annotated_path:
            errors.append(f"{identifier}: source and annotated files must be distinct")
            continue

        source_hash = sha256(source_path)
        annotated_hash = sha256(annotated_path)
        hash_occurrences["source_sha256"][source_hash].append((identifier, item))
        hash_occurrences["annotated_sha256"][annotated_hash].append((identifier, item))
        if not SHA256_RE.fullmatch(str(item.get("source_sha256", ""))):
            errors.append(f"{identifier}: source_sha256 is missing or invalid")
        elif source_hash != item.get("source_sha256"):
            errors.append(f"{identifier}: source SHA-256 mismatch")
        if not SHA256_RE.fullmatch(str(item.get("annotated_sha256", ""))):
            errors.append(f"{identifier}: annotated_sha256 is missing or invalid")
        elif annotated_hash != item.get("annotated_sha256"):
            errors.append(f"{identifier}: annotated SHA-256 mismatch")
        receipt_hash = sha256(receipt_path)
        if not SHA256_RE.fullmatch(str(item.get("scan_receipt_sha256", ""))):
            errors.append(f"{identifier}: scan_receipt_sha256 is missing or invalid")
        elif receipt_hash != item.get("scan_receipt_sha256"):
            errors.append(f"{identifier}: scan receipt SHA-256 mismatch")

        expected_dimensions: tuple[int, int] | None = None
        viewport = item.get("viewport")
        match = re.fullmatch(r"(\d{3,4})x(\d{3,4})@100%", str(viewport))
        if match:
            expected_dimensions = (int(match.group(1)), int(match.group(2)))
        else:
            errors.append(f"{identifier}: invalid viewport")
        for label, path, expected_format in (
            ("source", source_path, "PNG"),
            ("annotated", annotated_path, "WEBP"),
        ):
            try:
                with Image.open(path) as image:
                    image.load()
                    if image.format != expected_format:
                        errors.append(f"{identifier}: {label} bytes are not {expected_format}")
                    if image.getexif():
                        errors.append(f"{identifier}: {label} EXIF metadata is not empty")
                    allowed_metadata = ALLOWED_IMAGE_METADATA_KEYS.get(
                        str(image.format or "").upper(), frozenset()
                    )
                    metadata_keys = {
                        key.casefold() if isinstance(key, str) else repr(key)
                        for key in image.info
                    }
                    if metadata_keys - allowed_metadata:
                        errors.append(
                            f"{identifier}: {label} nonessential image metadata is not empty"
                        )
                    if expected_dimensions and image.size != expected_dimensions:
                        errors.append(
                            f"{identifier}: {label} dimensions {image.size} do not match {expected_dimensions}"
                        )
            except Exception as exc:
                errors.append(f"{identifier}: cannot inspect {label} image: {type(exc).__name__}")
        if annotated_path.stat().st_size > 512000:
            errors.append(f"{identifier}: public WebP exceeds 500 KiB")

        try:
            source_scan, source_findings = scan_image(source_path)
            annotated_scan, annotated_findings = scan_image(annotated_path)
        except OCRUnavailable:
            errors.append(f"{identifier}: required OCR engine/languages are unavailable")
            continue
        if source_scan.get("character_count", 0) < 4:
            errors.append(f"{identifier}: source OCR produced insufficient text")
        if annotated_scan.get("character_count", 0) < 4:
            errors.append(f"{identifier}: annotated OCR produced insufficient text")
        if source_findings:
            errors.append(
                f"{identifier}: source image safety scan found {len(source_findings)} issue(s)"
            )
        if annotated_findings:
            errors.append(
                f"{identifier}: annotated image safety scan found {len(annotated_findings)} issue(s)"
            )
        errors.extend(
            _validate_receipt(
                identifier=identifier,
                item=item,
                receipt_path=receipt_path,
                source_hash=source_hash,
                annotated_hash=annotated_hash,
                source_scan=source_scan,
                annotated_scan=annotated_scan,
                source_findings=source_findings,
                annotated_findings=annotated_findings,
            )
        )
        captured_at = _parse_datetime(item.get("captured_at"))
        if captured_at is None:
            errors.append(f"{identifier}: captured_at must be timezone-aware")
        if release and item.get("redaction_status") != "passed":
            errors.append(f"{identifier}: redaction_status must be passed")
        if release:
            checks = item.get("quality_checks")
            required_checks = {
                "ocr",
                "exif",
                "metadata",
                "secrets",
                "dimensions",
                "file_size",
            }
            if not isinstance(checks, dict):
                errors.append(f"{identifier}: quality_checks are missing")
            else:
                missing = sorted(name for name in required_checks if checks.get(name) != "passed")
                if missing:
                    errors.append(
                        f"{identifier}: quality checks not passed: {', '.join(missing)}"
                    )

    for hash_field, groups in hash_occurrences.items():
        for actual_hash, occurrences in groups.items():
            if len(occurrences) > 1:
                errors.extend(
                    _validate_hash_reuse_group(
                        hash_field=hash_field,
                        actual_hash=actual_hash,
                        occurrences=occurrences,
                    )
                )

    actual_sources, source_inventory_errors = _inventory_evidence_root(SOURCE_ROOT, {".png"})
    actual_annotated, annotated_inventory_errors = _inventory_evidence_root(
        ANNOTATED_ROOT, {".webp"}
    )
    actual_receipts, receipt_inventory_errors = _inventory_evidence_root(
        RECEIPT_ROOT, {".yml", ".yaml"}
    )
    errors.extend(source_inventory_errors)
    errors.extend(annotated_inventory_errors)
    errors.extend(receipt_inventory_errors)
    for label, actual, declared in (
        ("source image", actual_sources, manifest_sources),
        ("annotated image", actual_annotated, manifest_annotated),
        ("scan receipt", actual_receipts, manifest_receipts),
    ):
        orphaned = sorted(actual - declared)
        if orphaned:
            errors.append(f"{len(orphaned)} orphan {label} file(s) are outside the manifest")
    public_image_bytes = sum((ROOT / path).stat().st_size for path in actual_annotated)
    if public_image_bytes > 150 * 1024 * 1024:
        errors.append(f"public screenshot assets exceed 150 MiB: {public_image_bytes} bytes")
    if release:
        planned_ids = {
            str(item.get("id"))
            for item in plan.get("shots", [])
            if isinstance(item, dict) and item.get("required_for_release")
        }
        missing = sorted(planned_ids - seen_ids)
        extra = sorted(seen_ids - planned_ids)
        if missing:
            errors.append(f"release manifest is missing {len(missing)} planned screenshots")
        if extra:
            errors.append(f"release manifest contains {len(extra)} unplanned screenshots")
        errors.extend(validate_page_bindings(plan, manifest))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        default=os.getenv("PLAYBOOK_RELEASE_MODE") == "1",
    )
    args = parser.parse_args()
    manifest = load_yaml(ROOT / MANIFEST_PATH)
    plan = load_yaml(ROOT / PLAN_PATH)
    errors = validate_manifest(manifest, plan, release=args.release)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(
        f"screenshot validation: {len(manifest.get('screenshots', []))} item(s), "
        f"{len(plan.get('shots', []))} planned, {len(errors)} error(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
