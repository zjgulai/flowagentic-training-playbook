#!/usr/bin/env python3
"""Enforce the minimum UltraDeep source mix and claim/source integrity."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


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


def validate_items(items: list[dict[str, Any]], schema_name: str, label: str) -> list[str]:
    validator = Draft202012Validator(
        load_json(ROOT / "schemas" / schema_name),
        format_checker=FormatChecker(),
    )
    errors: list[str] = []
    for index, item in enumerate(items):
        for error in validator.iter_errors(item):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{label}[{index}].{location}: {error.message}")
    return errors


def validate_release_claims(
    claims: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    *,
    baseline: dict[str, Any],
) -> list[str]:
    contract = load_yaml(ROOT / "research" / "release-claims.yml")
    claims_by_id = {item.get("claim_id"): item for item in claims}
    sources_by_id = {item.get("source_id"): item for item in sources}
    errors: list[str] = []
    target_types = {"target-source", "target-test", "target-runtime"}
    official_types = {
        "official-doc",
        "official-source",
        "official-release",
        "official-pr",
        "maintainer-discussion",
    }
    expected_sha = str(baseline.get("release_sha", ""))
    expected_version = str(baseline.get("product_version", ""))
    try:
        baseline_date = dt.date.fromisoformat(str(baseline.get("verified_at", ""))[:10])
    except ValueError:
        errors.append("fact baseline verification date is invalid")
        baseline_date = None

    for claim in claims:
        claim_id = claim.get("claim_id", "<unknown>")
        applies_to = claim.get("applies_to", {})
        if str(applies_to.get("release_sha", "")) != expected_sha:
            errors.append(f"{claim_id} release SHA does not match fact baseline")
        if str(applies_to.get("product_version", "")) != expected_version:
            errors.append(f"{claim_id} product version does not match fact baseline")
        try:
            claim_date = dt.date.fromisoformat(str(claim.get("last_verified", ""))[:10])
        except ValueError:
            errors.append(f"{claim_id} verification date is invalid")
        else:
            if baseline_date is not None and claim_date < baseline_date:
                errors.append(f"{claim_id} verification predates fact baseline")

    for claim_id in contract.get("core_claim_ids", []):
        claim = claims_by_id.get(claim_id)
        if claim is None:
            errors.append(f"release core claim is missing: {claim_id}")
            continue
        linked = [sources_by_id.get(item, {}) for item in claim.get("source_ids", [])]
        if claim.get("evidence_status") not in {"triangulated", "verified"}:
            errors.append(f"{claim_id} is not triangulated/verified")
        if claim.get("local_verification", {}).get("status") != "passed":
            errors.append(f"{claim_id} has no passed training-environment verification")
        if not any(item.get("source_type") in target_types for item in linked):
            errors.append(f"{claim_id} has no target-system source")
        if not any(item.get("source_type") in official_types for item in linked):
            errors.append(f"{claim_id} has no official-semantics source")

    for claim in claims:
        if claim.get("experience_label") != "experience-advice":
            continue
        claim_id = claim.get("claim_id")
        linked = [sources_by_id.get(item, {}) for item in claim.get("source_ids", [])]
        authors = {
            item.get("author")
            for item in linked
            if item.get("source_type") == "developer-case"
            and item.get("author")
            and item.get("author") != "unknown"
        }
        if claim.get("evidence_status") not in {"triangulated", "verified"}:
            errors.append(f"{claim_id} experience advice is not triangulated/verified")
        if claim.get("local_verification", {}).get("status") != "passed":
            errors.append(f"{claim_id} experience advice lacks local reproduction")
        if len(authors) < 2:
            errors.append(
                f"{claim_id} experience advice needs two independent developer authors"
            )
        if not any(
            item.get("source_type") in target_types | official_types for item in linked
        ):
            errors.append(f"{claim_id} experience advice has no official/source anchor")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        default=os.getenv("PLAYBOOK_RELEASE_MODE") == "1",
        help="Require release-grade triangulation and training reproduction.",
    )
    args = parser.parse_args()
    source_path = ROOT / "research" / "sources.yml"
    claim_path = ROOT / "research" / "claims.yml"
    if not source_path.exists() or not claim_path.exists():
        print("ERROR: research/sources.yml and research/claims.yml are required", file=sys.stderr)
        return 1

    sources = load_yaml(source_path).get("sources", [])
    claim_payload = load_yaml(claim_path)
    claims = claim_payload.get("claims", [])
    errors = validate_items(sources, "source.schema.json", "sources")
    errors.extend(validate_items(claims, "claim.schema.json", "claims"))

    source_ids = [item.get("source_id") for item in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source ids must be unique")
    claim_ids = [item.get("claim_id") for item in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("claim ids must be unique")
    known_sources = set(source_ids)
    for claim in claims:
        unknown = sorted(set(claim.get("source_ids", [])) - known_sources)
        if unknown:
            errors.append(f"{claim.get('claim_id')} references unknown sources: {unknown}")

    counts = Counter(item.get("source_type") for item in sources)
    target_count = sum(counts[item] for item in ("target-source", "target-test", "target-runtime"))
    official_semantics = counts["official-doc"] + counts["official-source"]
    maintainer_count = (
        counts["official-release"] + counts["official-pr"] + counts["maintainer-discussion"]
    )
    developer_cases = [item for item in sources if item.get("source_type") == "developer-case"]
    developer_authors = {
        item.get("author")
        for item in developer_cases
        if item.get("author") and item.get("author") != "unknown"
    }
    if len(sources) < 45:
        errors.append(f"at least 45 unique sources required, found {len(sources)}")
    if target_count < 12:
        errors.append(f"at least 12 target-system sources required, found {target_count}")
    if official_semantics < 15:
        errors.append(f"at least 15 official docs/source items required, found {official_semantics}")
    if maintainer_count < 8:
        errors.append(f"at least 8 release/PR/maintainer items required, found {maintainer_count}")
    if len(developer_cases) < 8:
        errors.append(f"at least 8 developer cases required, found {len(developer_cases)}")
    if len(developer_authors) < 5:
        errors.append(f"developer cases must cover at least 5 authors, found {len(developer_authors)}")
    if sources:
        average_credibility = sum(item.get("credibility", 0) for item in sources) / len(sources)
        if average_credibility < 75:
            errors.append(f"average source credibility must be >=75, found {average_credibility:.1f}")
    else:
        average_credibility = 0

    if args.release:
        baseline = load_yaml(ROOT / "data" / "release.yml").get("fact_baseline", {})
        if str(claim_payload.get("target_release_sha", "")) != str(
            baseline.get("release_sha", "")
        ):
            errors.append("research target release SHA does not match fact baseline")
        errors.extend(validate_release_claims(claims, sources, baseline=baseline))

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(
        json.dumps(
            {
                "sources": len(sources),
                "claims": len(claims),
                "target_system": target_count,
                "official_semantics": official_semantics,
                "maintainer": maintainer_count,
                "developer_cases": len(developer_cases),
                "developer_authors": len(developer_authors),
                "average_credibility": round(average_credibility, 1),
                "mode": "release" if args.release else "draft",
                "errors": len(errors),
            },
            ensure_ascii=False,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
