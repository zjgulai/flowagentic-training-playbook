#!/usr/bin/env python3
"""Validate Playbook metadata, cross-references, catalogs, and release invariants."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

try:  # Script execution and package import use different module roots.
    from provider_budget import BudgetError, money, validate_ledger_file
except ModuleNotFoundError:  # pragma: no cover - exercised by package consumers
    from scripts.provider_budget import BudgetError, money, validate_ledger_file

try:
    from provider_attestation import (
        ProviderAttestationError,
        verify_provider_attestation,
    )
except ModuleNotFoundError:  # pragma: no cover - exercised by package consumers
    from scripts.provider_attestation import (
        ProviderAttestationError,
        verify_provider_attestation,
    )


ROOT = Path(__file__).resolve().parents[1]
FEATURE_STATUSES = {
    "production-enabled",
    "feature-gated",
    "deprecated",
    "experimental",
    "upstream-only",
}
REQUIRED_EXTERNAL_GATES = {
    "github_repository",
    "chinese_release",
    "isolated_training_environment",
    "provider_credentials",
    "provider_executions",
    "chrome_pc_acceptance",
    "firefox_pc_acceptance",
    "accessibility_wcag",
    "role_walkthroughs",
}

# Public release gates are deliberately a closed contract.  Keeping the IDs here,
# instead of trusting the mutable release.yml copy, prevents a release author from
# deleting an inconvenient requirement and then producing a smaller receipt.
GATE_EVIDENCE_CONTRACTS: dict[str, dict[str, Any]] = {
    "github_repository": {
        "evidence_type": "repository",
        "evidence_ids": (
            "EVD-GITHUB-REPOSITORY",
            "EVD-GITHUB-PAGES-WRITE",
            "EVD-GITHUB-MAIN-PROTECTION",
        ),
    },
    "chinese_release": {
        "evidence_type": "deployment",
        "evidence_ids": (
            "EVD-CHINESE-RELEASE-IDENTITY",
            "EVD-CHINESE-RELEASE-DEPLOYMENT",
            "EVD-CHINESE-PC-ACCEPTANCE",
            "EVD-CHINESE-BROWSER-ROUTES",
            "EVD-CHINESE-BASELINE-DIFF",
        ),
    },
    "isolated_training_environment": {
        "evidence_type": "environment",
        "evidence_ids": (
            "EVD-TRAINING-IMAGE",
            "EVD-TRAINING-MIGRATIONS",
            "EVD-TRAINING-FEATURE-FLAGS",
            "EVD-TRAINING-ACCESS",
        ),
    },
    "provider_credentials": {
        "evidence_type": "credentials",
        "evidence_ids": (
            "EVD-PROVIDER-DEEPSEEK-CREDENTIAL",
            "EVD-PROVIDER-KIMI-CREDENTIAL",
            "EVD-PROVIDER-BUDGET-STOP",
        ),
    },
    "provider_executions": {
        "evidence_type": "provider-execution",
        "evidence_ids": (
            "EVD-PROVIDER-DEEPSEEK-RUN",
            "EVD-PROVIDER-KIMI-RUN",
            "EVD-PROVIDER-ACCOUNT-CONTROLS",
            "EVD-PROVIDER-CLEANUP-METRICS",
            "EVD-PROVIDER-SIGNED-ATTESTATION",
        ),
    },
    "chrome_pc_acceptance": {
        "evidence_type": "browser",
        "evidence_ids": (
            "EVD-CHROME-PC-FLOW",
            "EVD-CHROME-CONSOLE-NETWORK",
        ),
    },
    "firefox_pc_acceptance": {
        "evidence_type": "browser",
        "evidence_ids": (
            "EVD-FIREFOX-PC-FLOW",
            "EVD-FIREFOX-LAYOUT",
        ),
    },
    "accessibility_wcag": {
        "evidence_type": "accessibility",
        "evidence_ids": (
            "EVD-WCAG-KEYBOARD",
            "EVD-WCAG-VISUAL-SEMANTICS",
        ),
    },
    "role_walkthroughs": {
        "evidence_type": "walkthrough",
        "evidence_ids": (
            "EVD-ROLE-BEGINNER",
            "EVD-ROLE-BUILDER",
            "EVD-ROLE-DEVELOPER",
            "EVD-ROLE-ADMIN",
        ),
    },
}


def normalize(value: Any) -> Any:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return normalize(yaml.safe_load(handle))


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(name: str) -> dict[str, Any]:
    return load_json(ROOT / "schemas" / name)


def format_errors(validator: Draft202012Validator, value: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{prefix}:{location}: {error.message}")
    return errors


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    metadata = normalize(yaml.safe_load(text[4:end])) or {}
    return metadata, text[end + 5 :]


def validate_docs(
    release_mode: bool,
    *,
    baseline: dict[str, Any] | None = None,
) -> tuple[list[str], list[str], set[str], set[str]]:
    schema = load_schema("sop.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    warnings: list[str] = []
    evidence_ids: set[str] = set()
    screenshot_ids: set[str] = set()
    for path in sorted((ROOT / "docs").rglob("*.md")):
        relative = path.relative_to(ROOT)
        try:
            metadata, body = parse_frontmatter(path)
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"{relative}: invalid frontmatter: {exc}")
            continue
        if metadata is None:
            errors.append(f"{relative}: missing YAML frontmatter")
            continue
        errors.extend(format_errors(validator, metadata, str(relative)))
        if release_mode and baseline is not None:
            expected_version = str(baseline.get("product_version", ""))
            expected_sha = str(baseline.get("release_sha", ""))
            if str(metadata.get("release_version", "")) != expected_version:
                errors.append(f"{relative}: release_version does not match fact baseline")
            if str(metadata.get("release_sha", "")) != expected_sha:
                errors.append(f"{relative}: release_sha does not match fact baseline")
            try:
                page_date = dt.date.fromisoformat(str(metadata.get("last_verified", ""))[:10])
                baseline_date = dt.date.fromisoformat(str(baseline.get("verified_at", ""))[:10])
            except ValueError:
                errors.append(f"{relative}: release verification date is invalid")
            else:
                if page_date < baseline_date:
                    errors.append(
                        f"{relative}: last_verified predates the fact baseline verification"
                    )
        evidence_ids.update(metadata.get("evidence_ids", []))
        screenshot_ids.update(metadata.get("screenshot_ids", []))
        if not re.search(r"^#\s+\S", body, flags=re.MULTILINE):
            errors.append(f"{relative}: missing level-one title")
        if release_mode and re.search(r"\b(TODO|TBD|FIXME)\b|占位截图|待补", body, re.IGNORECASE):
            errors.append(f"{relative}: release content contains an unfinished marker")
        elif re.search(r"\b(TODO|TBD|FIXME)\b|占位截图|待补", body, re.IGNORECASE):
            warnings.append(f"{relative}: draft contains an unfinished marker")
    return errors, warnings, evidence_ids, screenshot_ids


def validate_screenshot_refs(referenced: set[str], release_mode: bool) -> tuple[list[str], list[str]]:
    manifest_path = ROOT / "data" / "manifests" / "screenshots.yml"
    payload = load_yaml(manifest_path)
    items = payload.get("screenshots", [])
    schema = load_schema("screenshot.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    warnings: list[str] = []
    ids: list[str] = []
    for index, item in enumerate(items):
        errors.extend(format_errors(validator, item, f"{manifest_path.relative_to(ROOT)}[{index}]"))
        ids.append(item.get("id", ""))
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"screenshot manifest has duplicate ids: {', '.join(duplicates)}")
    missing = sorted(referenced - set(ids))
    if missing:
        errors.append(f"frontmatter references missing screenshots: {', '.join(missing)}")
    orphaned = sorted(set(ids) - referenced)
    if release_mode and orphaned:
        errors.append(f"release manifest contains orphan screenshots: {', '.join(orphaned)}")
    elif orphaned:
        warnings.append(f"draft manifest contains {len(orphaned)} orphan screenshots")
    if release_mode and not items:
        errors.append("release mode requires a non-empty screenshot manifest")
    if release_mode and payload.get("capture_status") != "passed":
        errors.append("release mode requires screenshot capture_status=passed")
    plan_path = ROOT / "data" / "manifests" / "screenshot-plan.yml"
    if plan_path.exists():
        plan = load_yaml(plan_path)
        planned = {
            item.get("id")
            for item in plan.get("shots", [])
            if item.get("required_for_release")
        }
        if not 180 <= len(planned) <= 260:
            errors.append(f"screenshot plan must contain 180-260 required ids, found {len(planned)}")
        if release_mode:
            uncaptured = sorted(planned - set(ids))
            if uncaptured:
                errors.append(
                    f"release manifest is missing {len(uncaptured)} planned screenshots"
                )
    elif release_mode:
        errors.append("release mode requires data/manifests/screenshot-plan.yml")
    return errors, warnings


def validate_node_catalog() -> list[str]:
    path = ROOT / "data" / "catalog" / "nodes.json"
    if not path.exists():
        return ["data/catalog/nodes.json is missing"]
    payload = load_json(path)
    schema = load_schema("node.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    nodes = payload.get("nodes", [])
    if payload.get("count") != len(nodes):
        errors.append("node catalog count does not match nodes length")
    if len(nodes) != 311:
        errors.append(f"expected 311 nodes at baseline commit, found {len(nodes)}")
    ids = [node.get("id") for node in nodes]
    if len(ids) != len(set(ids)):
        errors.append("node catalog ids are not unique")
    for index, node in enumerate(nodes):
        errors.extend(format_errors(validator, node, f"data/catalog/nodes.json[{index}]"))
    return errors


def validate_feature_status(
    release_mode: bool = False,
    *,
    baseline: dict[str, Any] | None = None,
) -> list[str]:
    payload = load_yaml(ROOT / "data" / "feature-status.yml")
    errors: list[str] = []
    feature_ids: set[str] = set()
    complete_sops = 0
    for item in payload.get("features", []):
        if item.get("id") in feature_ids:
            errors.append(f"duplicate feature id: {item.get('id')}")
        feature_ids.add(item.get("id"))
        if item.get("status") not in FEATURE_STATUSES:
            errors.append(f"invalid feature status: {item.get('status')}")
        if item.get("training_scope") == "complete-sop":
            complete_sops += 1
    if complete_sops != 10:
        errors.append(f"expected 10 production complete-SOP modules, found {complete_sops}")
    if release_mode and baseline is not None:
        if str(payload.get("release_sha", "")) != str(baseline.get("release_sha", "")):
            errors.append("feature status SHA does not match fact baseline")
        try:
            status_date = dt.date.fromisoformat(str(payload.get("last_verified", ""))[:10])
            baseline_date = dt.date.fromisoformat(str(baseline.get("verified_at", ""))[:10])
        except ValueError:
            errors.append("feature status verification date is invalid")
        else:
            if status_date < baseline_date:
                errors.append("feature status predates fact baseline verification")
    return errors


def validate_content_evidence_map() -> list[str]:
    """Require every public page to use the reviewed, topic-specific Claim set."""

    payload = load_yaml(ROOT / "data" / "content-evidence-map.yml")
    rules = sorted(
        payload.get("rules", []),
        key=lambda item: len(str(item.get("path_prefix", ""))),
        reverse=True,
    )
    known_claims = {
        item.get("claim_id")
        for item in load_yaml(ROOT / "research" / "claims.yml").get("claims", [])
    }
    errors: list[str] = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        rule = next(
            (
                item
                for item in rules
                if relative.startswith(str(item.get("path_prefix", "")))
            ),
            None,
        )
        if rule is None:
            errors.append(f"{relative}: no content evidence-map rule")
            continue
        metadata, _ = parse_frontmatter(path)
        actual = metadata.get("evidence_ids", []) if metadata else []
        expected = rule.get("claim_ids", [])
        if actual != expected:
            errors.append(
                f"{relative}: evidence_ids must exactly match reviewed map "
                f"{expected}, found {actual}"
            )
        if any(not str(item).startswith("CLM-") for item in actual):
            errors.append(f"{relative}: page evidence must reference Claims, not raw sources")
        unknown = sorted(set(actual) - known_claims)
        if unknown:
            errors.append(f"{relative}: evidence map references unknown claims: {unknown}")
    return errors


def validate_sop_coverage(release_mode: bool) -> list[str]:
    """Bind the ten promised modules to substantive fourteen-section SOP pages."""

    coverage = load_yaml(ROOT / "data" / "sop-coverage.yml")
    required_sections = coverage.get("required_sections", [])
    entries = coverage.get("sops", [])
    features = load_yaml(ROOT / "data" / "feature-status.yml").get("features", [])
    expected_ids = {
        item.get("id")
        for item in features
        if item.get("training_scope") == "complete-sop"
    }
    actual_ids = [item.get("feature_id") for item in entries]
    errors: list[str] = []
    if len(entries) != 10 or set(actual_ids) != expected_ids:
        errors.append(
            "data/sop-coverage.yml must bind exactly the ten complete-SOP features"
        )
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("data/sop-coverage.yml has duplicate feature ids")
    if len(required_sections) != 14 or len(required_sections) != len(set(required_sections)):
        errors.append("SOP contract must define exactly fourteen unique sections")

    for entry in entries:
        feature_id = entry.get("feature_id", "<unknown>")
        relative = Path(str(entry.get("page", "")))
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{feature_id}: SOP page is missing: {relative}")
            continue
        metadata, body = parse_frontmatter(path)
        if metadata is None:
            errors.append(f"{relative}: SOP page has no frontmatter")
            continue
        sections: dict[str, str] = {}
        matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", body))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            sections.setdefault(match.group(1).strip(), body[match.end() : end].strip())
        for section in required_sections:
            value = sections.get(section, "")
            if not value:
                errors.append(f"{relative}: missing or empty required SOP section: {section}")
            elif len(re.sub(r"\s+", "", value)) < 12:
                errors.append(f"{relative}: SOP section is too thin: {section}")
        if metadata.get("feature_status") != "production-enabled":
            errors.append(f"{relative}: complete SOP must be production-enabled")
        if not metadata.get("permissions"):
            errors.append(f"{relative}: complete SOP must declare permissions")
        if not metadata.get("side_effects"):
            errors.append(f"{relative}: complete SOP must declare side effects")
        if not metadata.get("evidence_ids"):
            errors.append(f"{relative}: complete SOP must cite semantic Claims")
        if release_mode and not metadata.get("screenshot_ids"):
            errors.append(f"{relative}: release SOP must bind screenshots")
    return errors


def validate_provider_budget(release_mode: bool = False) -> list[str]:
    try:
        validate_ledger_file(
            ROOT / "data" / "experiments" / "provider-budget.yml",
            require_release_clean=release_mode,
        )
    except BudgetError as exc:
        return [f"provider budget ledger is invalid: {exc}"]
    return []


def _is_real_sha256(value: object) -> bool:
    """Reject syntactically valid but unmistakably placeholder SHA-256 values."""

    digest = str(value)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        return False
    if len(set(digest)) == 1:
        return False
    return digest not in {
        "1234567890abcdef" * 4,
        "deadbeef" * 8,
    }


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_aggregate_sha256(items: list[tuple[str, str]]) -> str:
    """Return the canonical aggregate of sorted ``evidence-id:digest`` pairs."""

    canonical = "".join(
        f"{item_id}:{digest}\n" for item_id, digest in sorted(items)
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_required_evidence_contract(
    gate_name: str,
    state: dict[str, Any],
) -> list[str]:
    """Ensure release.yml cannot weaken the compiled gate contract."""

    contract = GATE_EVIDENCE_CONTRACTS.get(gate_name)
    if contract is None:
        return [f"release gate has no fixed evidence contract: {gate_name}"]
    expected = list(contract["evidence_ids"])
    actual = state.get("required_evidence")
    if actual != expected:
        return [
            f"release gate required_evidence differs from fixed contract: {gate_name}"
        ]
    return []


def validate_external_gate_contracts(value: object) -> list[str]:
    """Validate the closed gate set and globally unique structured receipt IDs."""

    if not isinstance(value, dict):
        return ["release config external_gates must be an object"]
    errors: list[str] = []
    present = set(value)
    missing = sorted(REQUIRED_EXTERNAL_GATES - present)
    unknown = sorted(present - REQUIRED_EXTERNAL_GATES)
    if missing:
        errors.append(f"release config is missing mandatory gates: {missing}")
    if unknown:
        errors.append(f"release config contains unknown gates: {unknown}")

    receipt_ids: list[str] = []
    for gate_name in sorted(REQUIRED_EXTERNAL_GATES & present):
        state = value.get(gate_name)
        if not isinstance(state, dict):
            errors.append(f"release gate state must be an object: {gate_name}")
            continue
        errors.extend(validate_required_evidence_contract(gate_name, state))
        receipt = state.get("receipt")
        if isinstance(receipt, dict) and receipt.get("receipt_id") is not None:
            receipt_ids.append(str(receipt.get("receipt_id")))
    duplicates = sorted(
        receipt_id
        for receipt_id in set(receipt_ids)
        if receipt_ids.count(receipt_id) > 1
    )
    if duplicates:
        errors.append(f"release gate receipt ids are duplicated: {duplicates}")
    return errors


def _resolve_evidence_artifact(
    root: Path,
    value: object,
) -> tuple[Path | None, str | None]:
    """Resolve a regular, non-symlink artifact confined to data/evidence."""

    if not isinstance(value, str) or not value.strip():
        return None, "artifact path is missing"
    try:
        relative = Path(value)
        if relative.is_absolute() or relative.parts[:2] != ("data", "evidence"):
            return None, "artifact path is outside data/evidence"
        if ".." in relative.parts:
            return None, "artifact path contains traversal"

        candidate = root / relative
        current = root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                return None, "artifact path contains a symlink"
        if not candidate.is_file():
            return None, "artifact is not a regular file"
        candidate.resolve(strict=True).relative_to(
            (root / "data" / "evidence").resolve(strict=True)
        )
    except (FileNotFoundError, OSError, ValueError):
        return None, "artifact does not resolve inside data/evidence"
    return candidate, None


def validate_gate_receipt(
    gate_name: str,
    state: dict[str, Any],
    *,
    release_sha: str,
    product_version: str,
    root: Path = ROOT,
    now: dt.datetime | None = None,
) -> list[str]:
    """Validate a public-safe, artifact-bound external-gate attestation."""

    errors = validate_required_evidence_contract(gate_name, state)
    contract = GATE_EVIDENCE_CONTRACTS.get(gate_name)
    if contract is None:
        return errors
    expected_ids = list(contract["evidence_ids"])
    receipt = state.get("receipt")
    if not isinstance(receipt, dict):
        return errors + [
            f"release gate receipt must be a structured object: {gate_name}"
        ]
    if not re.fullmatch(r"RCT-[A-Z0-9-]{8,80}", str(receipt.get("receipt_id", ""))):
        errors.append(f"release gate receipt id is invalid: {gate_name}")
    if receipt.get("evidence_type") != contract["evidence_type"]:
        errors.append(f"release gate receipt evidence type does not match: {gate_name}")
    if str(receipt.get("release_sha", "")) != release_sha:
        errors.append(f"release gate receipt SHA does not match: {gate_name}")
    if str(receipt.get("product_version", "")) != product_version:
        errors.append(f"release gate receipt product version does not match: {gate_name}")
    if receipt.get("public_safe") is not True:
        errors.append(f"release gate receipt is not public-safe: {gate_name}")
    reviewer = receipt.get("reviewer")
    if not isinstance(reviewer, str) or not 3 <= len(reviewer.strip()) <= 120:
        errors.append(f"release gate receipt reviewer is invalid: {gate_name}")

    verified_at = receipt.get("verified_at")
    try:
        receipt_time = dt.datetime.fromisoformat(str(verified_at).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"release gate receipt time is invalid: {gate_name}")
    else:
        if receipt_time.tzinfo is None:
            errors.append(f"release gate receipt time lacks timezone: {gate_name}")
        else:
            reference_time = now or dt.datetime.now(dt.timezone.utc)
            if reference_time.tzinfo is None:
                reference_time = reference_time.replace(tzinfo=dt.timezone.utc)
            if receipt_time.astimezone(dt.timezone.utc) > reference_time.astimezone(
                dt.timezone.utc
            ):
                errors.append(f"release gate receipt time is in the future: {gate_name}")
        if str(state.get("verified_at", "")) != str(verified_at):
            errors.append(f"release gate and receipt times differ: {gate_name}")

    artifact_digest = receipt.get("artifact_sha256")
    if not _is_real_sha256(artifact_digest):
        errors.append(f"release gate artifact digest is invalid or placeholder: {gate_name}")

    evidence_items = receipt.get("evidence_items")
    if not isinstance(evidence_items, list):
        errors.append(f"release gate receipt lacks required evidence items: {gate_name}")
        return errors

    item_ids: list[str] = []
    actual_digests: list[tuple[str, str]] = []
    for item in evidence_items:
        if not isinstance(item, dict):
            errors.append(f"release gate evidence item is invalid: {gate_name}")
            continue
        item_id = str(item.get("id", ""))
        if not re.fullmatch(r"EVD-[A-Z0-9-]{6,80}", item_id):
            errors.append(f"release gate evidence id is invalid: {gate_name}")
        item_ids.append(item_id)
        if item.get("status") != "passed":
            errors.append(f"release gate evidence is not passed: {gate_name}")
        count = item.get("count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            errors.append(f"release gate evidence count is invalid: {gate_name}")

        claimed_digest = item.get("sha256")
        if not _is_real_sha256(claimed_digest):
            errors.append(
                f"release gate evidence digest is invalid or placeholder: {gate_name}"
            )
        artifact, artifact_error = _resolve_evidence_artifact(
            root, item.get("artifact")
        )
        if artifact_error is not None:
            errors.append(
                f"release gate evidence artifact is invalid ({artifact_error}): {gate_name}"
            )
        elif artifact is not None:
            try:
                computed_digest = _file_sha256(artifact)
            except OSError:
                errors.append(f"release gate evidence artifact is unreadable: {gate_name}")
            else:
                actual_digests.append((item_id, computed_digest))
                if str(claimed_digest) != computed_digest:
                    errors.append(
                        f"release gate evidence digest does not match file: {gate_name}"
                    )

    if len(item_ids) != len(set(item_ids)):
        errors.append(f"release gate evidence ids are duplicated: {gate_name}")
    if item_ids != expected_ids:
        errors.append(f"release gate evidence ids do not match fixed contract: {gate_name}")
    if len(actual_digests) == len(expected_ids):
        expected_aggregate = evidence_aggregate_sha256(actual_digests)
        if str(artifact_digest) != expected_aggregate:
            errors.append(f"release gate artifact digest does not match evidence: {gate_name}")
    return errors


def validate_provider_account_controls(value: object) -> tuple[set[str], list[str]]:
    """Return providers with valid account controls and fail-closed diagnostics."""

    errors: list[str] = []
    valid_providers: set[str] = set()
    provider_counts: dict[str, int] = {}
    aggregate_hard_limit = money(0)
    if not isinstance(value, list):
        return set(), ["provider receipt account_budget_controls must be a list"]
    for control in value:
        if not isinstance(control, dict):
            errors.append("provider receipt contains an invalid account control")
            continue
        try:
            hard_limit = money(control.get("hard_limit", -1))
        except BudgetError:
            hard_limit = None
        provider = control.get("provider")
        if (
            provider in {"DeepSeek", "Kimi"}
            and control.get("auto_recharge") is False
            and control.get("status") == "passed"
            and str(control.get("currency", "")) == "CNY"
            and hard_limit is not None
            and 0 < hard_limit <= money(300)
            and re.fullmatch(
                r"[0-9a-f]{64}", str(control.get("receipt_sha256", ""))
            )
        ):
            valid_providers.add(str(provider))
            provider_name = str(provider)
            provider_counts[provider_name] = provider_counts.get(provider_name, 0) + 1
            aggregate_hard_limit += hard_limit
        else:
            errors.append("provider receipt contains an incomplete account control")
    if any(count != 1 for count in provider_counts.values()):
        errors.append("provider receipt must contain exactly one control per provider")
    if aggregate_hard_limit > money(300):
        errors.append("provider account hard limits exceed the shared CNY 300 cap")
    return valid_providers, errors


def validate_provider_signed_receipt(
    receipt: dict[str, Any],
    *,
    release_sha: str,
    product_version: str,
    root: Path = ROOT,
    now: dt.datetime | None = None,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Bind public Provider claims to one externally signed execution payload."""

    errors: list[str] = []
    attestation_path = receipt.get("attestation_path")
    if not isinstance(attestation_path, str) or not attestation_path.strip():
        return None, ["provider execution receipt lacks a signed attestation path"]

    evidence_items = receipt.get("evidence_items")
    signed_item = None
    if isinstance(evidence_items, list):
        signed_item = next(
            (
                item
                for item in evidence_items
                if isinstance(item, dict)
                and item.get("id") == "EVD-PROVIDER-SIGNED-ATTESTATION"
            ),
            None,
        )
    if not isinstance(signed_item, dict) or signed_item.get("artifact") != attestation_path:
        errors.append(
            "provider signed attestation path is not bound to its fixed evidence item"
        )

    try:
        payload = verify_provider_attestation(
            attestation_path,
            expected_release_sha=release_sha,
            expected_product_version=product_version,
            project_root=root,
            now=now,
        )
    except ProviderAttestationError as exc:
        errors.append(f"provider signed attestation is invalid: {exc}")
        return None, errors

    bindings = (
        ("provider_runs", "provider runs"),
        ("account_budget_controls", "account budget controls"),
        ("verified_at", "verification time"),
    )
    for field, label in bindings:
        if receipt.get(field) != payload.get(field):
            errors.append(
                f"provider receipt {label} does not match the signed attestation"
            )

    claim_ids = [
        item_id
        for item_id in GATE_EVIDENCE_CONTRACTS["provider_executions"][
            "evidence_ids"
        ]
        if item_id != "EVD-PROVIDER-SIGNED-ATTESTATION"
    ]
    claim_pairs: list[tuple[str, str]] = []
    if isinstance(evidence_items, list):
        for item_id in claim_ids:
            matches = [
                item
                for item in evidence_items
                if isinstance(item, dict) and item.get("id") == item_id
            ]
            if len(matches) != 1 or not _is_real_sha256(matches[0].get("sha256")):
                errors.append(
                    "provider signed claims bundle lacks a fixed evidence digest"
                )
                continue
            claim_pairs.append((item_id, str(matches[0]["sha256"])))
    if len(claim_pairs) == len(claim_ids):
        expected_claims_digest = evidence_aggregate_sha256(claim_pairs)
        if payload.get("claims_bundle_sha256") != expected_claims_digest:
            errors.append(
                "provider signed claims bundle does not match the four source evidences"
            )
    return payload, errors


def provider_run_matches_ledger_call(
    call: object,
    run: dict[str, Any],
) -> bool:
    """Compare signed Provider metrics with a ledger call using money semantics."""

    if not isinstance(call, dict):
        return False
    if not all(
        call.get(field) == run.get(field)
        for field in (
            "provider",
            "model",
            "input_tokens",
            "output_tokens",
            "latency_ms",
        )
    ):
        return False
    try:
        return money(call.get("actual_cost", -1)) == money(
            run.get("actual_cost", -1)
        )
    except BudgetError:
        return False


def validate_release_config(release_mode: bool) -> list[str]:
    payload = load_yaml(ROOT / "data" / "release.yml")
    errors: list[str] = []
    external_gates_value = payload.get("external_gates", {})
    errors.extend(validate_external_gate_contracts(external_gates_value))
    external_gates = (
        external_gates_value if isinstance(external_gates_value, dict) else {}
    )
    baseline = payload.get("fact_baseline", {})
    release_sha = str(baseline.get("release_sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", release_sha):
        errors.append("fact baseline release SHA must be a 40-character lowercase Git SHA")
    if not baseline.get("product_version"):
        errors.append("fact baseline product version is missing")
    source_baseline_path = ROOT / "data" / "catalog" / "source-baseline.json"
    node_catalog_path = ROOT / "data" / "catalog" / "nodes.json"
    if source_baseline_path.exists():
        source_baseline = load_json(source_baseline_path)
        if source_baseline.get("release_sha") != release_sha:
            errors.append("fact baseline and source-baseline.json release SHA differ")
        if source_baseline.get("product_version") != baseline.get("product_version"):
            errors.append("fact baseline and source-baseline.json product version differ")
    if node_catalog_path.exists():
        node_catalog = load_json(node_catalog_path)
        if node_catalog.get("release_sha") != release_sha:
            errors.append("fact baseline and node catalog release SHA differ")
    if not payload.get("release_invariants", {}).get("provider_calls_in_ci") is False:
        errors.append("release invariant must prohibit provider calls in CI")
    if not payload.get("release_invariants", {}).get("production_writes_forbidden"):
        errors.append("release invariant must prohibit production writes")
    if release_mode:
        mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        version_match = re.search(
            r'(?m)^    product_version:\s*["\']?([^"\'\s]+)', mkdocs_text
        )
        sha_match = re.search(
            r'(?m)^    release_sha:\s*["\']?([0-9a-f]{40})', mkdocs_text
        )
        if not version_match or version_match.group(1) != str(
            baseline.get("product_version", "")
        ):
            errors.append("MkDocs product version does not match fact baseline")
        if not sha_match or sha_match.group(1) != release_sha:
            errors.append("MkDocs release SHA does not match fact baseline")
        feature_status = load_yaml(ROOT / "data" / "feature-status.yml")
        if str(feature_status.get("release_sha", "")) != release_sha:
            errors.append("feature-status release SHA does not match fact baseline")
        for gate in sorted(REQUIRED_EXTERNAL_GATES):
            state = external_gates.get(gate, {})
            if state.get("status") != "passed":
                errors.append(f"release gate is not passed: {gate}")
                continue
            if state.get("release_sha") != release_sha:
                errors.append(f"release gate SHA does not match: {gate}")
            if not state.get("verified_at") or not state.get("receipt"):
                errors.append(f"release gate lacks timestamp or receipt: {gate}")
            else:
                errors.extend(
                    validate_gate_receipt(
                        gate,
                        state,
                        release_sha=release_sha,
                        product_version=str(baseline.get("product_version", "")),
                    )
                )
        provider_gate = external_gates.get("provider_executions", {})
        provider_receipt = provider_gate.get("receipt")
        if isinstance(provider_receipt, dict):
            _, attestation_errors = validate_provider_signed_receipt(
                provider_receipt,
                release_sha=release_sha,
                product_version=str(baseline.get("product_version", "")),
            )
            errors.extend(attestation_errors)
            provider_runs = provider_receipt.get("provider_runs", [])
            valid_runs: list[dict[str, Any]] = []
            if not isinstance(provider_runs, list):
                errors.append("provider execution receipt provider_runs must be a list")
                provider_runs = []
            for run in provider_runs:
                if not isinstance(run, dict):
                    errors.append("provider execution receipt contains an invalid run")
                    continue
                run_ok = True
                if run.get("provider") not in {"DeepSeek", "Kimi"}:
                    run_ok = False
                if run.get("status") != "success" or run.get("synthetic_data") is not True:
                    run_ok = False
                if run.get("cleanup_status") != "passed":
                    run_ok = False
                if str(run.get("release_sha", "")) != release_sha:
                    run_ok = False
                if not re.fullmatch(r"EXP-[A-Z0-9-]{4,64}", str(run.get("experiment_id", ""))):
                    run_ok = False
                if not re.fullmatch(r"[A-Za-z0-9._:/-]{1,128}", str(run.get("model", ""))):
                    run_ok = False
                fixture = str(run.get("fixture", ""))
                if not fixture.startswith("synthetic-"):
                    run_ok = False
                for metric in ("input_tokens", "output_tokens", "latency_ms"):
                    value = run.get(metric)
                    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                        run_ok = False
                try:
                    actual_cost = money(run.get("actual_cost", -1))
                except BudgetError:
                    run_ok = False
                else:
                    if actual_cost <= 0:
                        run_ok = False
                if not re.fullmatch(
                    r"[0-9a-f]{64}", str(run.get("cleanup_receipt_sha256", ""))
                ):
                    run_ok = False
                if run_ok:
                    valid_runs.append(run)
                else:
                    errors.append("provider execution receipt contains an incomplete run")
            providers = {item.get("provider") for item in valid_runs}
            if providers != {"DeepSeek", "Kimi"}:
                errors.append(
                    "provider execution receipt must contain successful DeepSeek and Kimi runs"
                )
            valid_controls, control_errors = validate_provider_account_controls(
                provider_receipt.get("account_budget_controls", [])
            )
            errors.extend(control_errors)
            if valid_controls != {"DeepSeek", "Kimi"}:
                errors.append(
                    "provider receipt must prove account hard limits and disabled auto-recharge"
                )
            try:
                ledger = validate_ledger_file(
                    ROOT / "data" / "experiments" / "provider-budget.yml",
                    require_release_clean=True,
                )
            except BudgetError as exc:
                errors.append(f"provider execution ledger is invalid: {exc}")
            else:
                settled_success = {
                    item.get("provider")
                    for item in ledger.get("calls", [])
                    if item.get("status") == "success"
                }
                if settled_success != {"DeepSeek", "Kimi"}:
                    errors.append(
                        "provider budget ledger must contain successful DeepSeek and Kimi calls"
                    )
                ledger_by_id = {
                    str(item.get("experiment_id")): item
                    for item in ledger.get("calls", [])
                    if isinstance(item, dict)
                }
                for run in valid_runs:
                    call = ledger_by_id.get(str(run.get("experiment_id")))
                    if not provider_run_matches_ledger_call(call, run):
                        errors.append(
                            "provider execution receipt does not match its settled ledger call"
                        )
        screenshot = payload.get("screenshot_baseline", {})
        if screenshot.get("status") != "passed" or not screenshot.get("release_sha"):
            errors.append("release screenshot baseline is not bound to a passed release SHA")
        if screenshot.get("release_sha") != release_sha:
            errors.append("screenshot baseline release SHA does not match fact baseline")
        if screenshot.get("product_version") != baseline.get("product_version"):
            errors.append("screenshot baseline product version does not match fact baseline")
        env_sha = os.getenv("PLAYBOOK_RELEASE_SHA")
        env_version = os.getenv("FLOWAGENTIC_PRODUCT_VERSION")
        if env_sha and env_sha != release_sha:
            errors.append("workflow release SHA does not match data/release.yml")
        if env_version and env_version != str(baseline.get("product_version")):
            errors.append("workflow product version does not match data/release.yml")
        screenshot_manifest = load_yaml(
            ROOT / "data" / "manifests" / "screenshots.yml"
        )
        if screenshot_manifest.get("release_sha") != release_sha:
            errors.append("screenshot manifest release SHA does not match fact baseline")
        screenshot_plan = load_yaml(
            ROOT / "data" / "manifests" / "screenshot-plan.yml"
        )
        if screenshot_plan.get("release_sha") != release_sha:
            errors.append("screenshot plan release SHA does not match fact baseline")
        if payload.get("publication_status") != "release-ready":
            errors.append("publication_status must be release-ready")
    return errors


def validate_evidence_refs(referenced: set[str], release_mode: bool) -> tuple[list[str], list[str]]:
    claims_path = ROOT / "research" / "claims.yml"
    sources_path = ROOT / "research" / "sources.yml"
    if not claims_path.exists() or not sources_path.exists():
        message = "research/sources.yml and research/claims.yml are not available yet"
        return ([message], []) if release_mode else ([], [message])
    claims = load_yaml(claims_path).get("claims", [])
    sources = load_yaml(sources_path).get("sources", [])
    known_ids = {item.get("claim_id") for item in claims}
    known_ids.update(item.get("source_id") for item in sources)
    missing = sorted(referenced - known_ids)
    if missing and release_mode:
        return ([f"frontmatter references unknown claims: {', '.join(missing)}"], [])
    if missing:
        return ([], [f"draft references {len(missing)} claims not yet in the research matrix"])
    if release_mode:
        claims_by_id = {item.get("claim_id"): item for item in claims}
        for claim_id in sorted(item for item in referenced if str(item).startswith("CLM-")):
            claim = claims_by_id.get(claim_id, {})
            if claim.get("evidence_status") not in {"triangulated", "verified"}:
                missing.append(f"{claim_id}: evidence_status={claim.get('evidence_status')}")
            local = claim.get("local_verification", {})
            if local.get("status") != "passed":
                missing.append(f"{claim_id}: local_verification={local.get('status')}")
            if claim.get("public_safe") is not True:
                missing.append(f"{claim_id}: public_safe is not true")
        if missing:
            return (["release pages reference unverified claims: " + "; ".join(missing)], [])
    return ([], [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        default=os.getenv("PLAYBOOK_RELEASE_MODE") == "1",
        help="Enable fail-closed publication checks.",
    )
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    release_payload = load_yaml(ROOT / "data" / "release.yml")
    baseline = release_payload.get("fact_baseline", {})
    doc_errors, doc_warnings, evidence_ids, screenshot_ids = validate_docs(
        args.release,
        baseline=baseline,
    )
    errors.extend(doc_errors)
    warnings.extend(doc_warnings)
    shot_errors, shot_warnings = validate_screenshot_refs(screenshot_ids, args.release)
    errors.extend(shot_errors)
    warnings.extend(shot_warnings)
    evidence_errors, evidence_warnings = validate_evidence_refs(evidence_ids, args.release)
    errors.extend(evidence_errors)
    warnings.extend(evidence_warnings)
    errors.extend(validate_node_catalog())
    errors.extend(validate_feature_status(args.release, baseline=baseline))
    errors.extend(validate_content_evidence_map())
    errors.extend(validate_sop_coverage(args.release))
    errors.extend(validate_provider_budget(args.release))
    errors.extend(validate_release_config(args.release))

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(
        json.dumps(
            {
                "mode": "release" if args.release else "draft",
                "documents": len(list((ROOT / "docs").rglob("*.md"))),
                "referenced_evidence": len(evidence_ids),
                "referenced_screenshots": len(screenshot_ids),
                "warnings": len(warnings),
                "errors": len(errors),
            },
            ensure_ascii=False,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
