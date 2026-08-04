#!/usr/bin/env python3
"""Read-only readiness audit for the independent public Playbook repository."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
PRODUCT_VERSION = re.compile(
    r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?$"
)
FORBIDDEN_REPOSITORIES = {
    "flowiseai/flowise",
    "zjgulai/flowise",
}
EVIDENCE_IDS = (
    "EVD-GITHUB-REPOSITORY",
    "EVD-GITHUB-PAGES-WRITE",
    "EVD-GITHUB-MAIN-PROTECTION",
)


class GitHubApiError(RuntimeError):
    """A sanitized GitHub API failure without response bodies or credentials."""

    def __init__(self, endpoint: str, status_code: int | None) -> None:
        self.endpoint = endpoint
        self.status_code = status_code
        status = str(status_code) if status_code is not None else "unknown"
        super().__init__(f"GitHub API GET failed ({status})")


ApiGet = Callable[[str], Any]


def load_release_baseline(root: Path = PROJECT_ROOT) -> tuple[str, str]:
    payload = yaml.safe_load((root / "data/release.yml").read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("data/release.yml root must be an object")
    baseline = payload.get("fact_baseline")
    if not isinstance(baseline, dict):
        raise ValueError("data/release.yml lacks fact_baseline")
    return (
        str(baseline.get("release_sha", "")),
        str(baseline.get("product_version", "")),
    )


def gh_api_get(endpoint: str) -> Any:
    """Execute one authenticated GET and expose only parsed JSON or an HTTP code."""

    result = subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "GET",
            "-H",
            "Accept: application/vnd.github+json",
            "-H",
            "X-GitHub-Api-Version: 2022-11-28",
            endpoint,
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        match = re.search(r"HTTP\s+(\d{3})", result.stderr)
        raise GitHubApiError(endpoint, int(match.group(1)) if match else None)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise GitHubApiError(endpoint, None) from exc


def optional_get(api_get: ApiGet, endpoint: str) -> Any | None:
    try:
        return api_get(endpoint)
    except GitHubApiError as exc:
        if exc.status_code == 404:
            return None
        raise


def _bool_check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def _evidence(
    evidence_id: str,
    checks: list[dict[str, Any]],
    *,
    status: str | None = None,
) -> dict[str, Any]:
    resolved = status or ("passed" if checks and all(item["passed"] for item in checks) else "blocked")
    return {
        "id": evidence_id,
        "status": resolved,
        "count": 1 if resolved == "passed" else 0,
        "checks": checks,
    }


def _required_reviewer_count(environment: Any) -> int:
    if not isinstance(environment, dict):
        return 0
    rules = environment.get("protection_rules")
    if not isinstance(rules, list):
        return 0
    count = 0
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("type") != "required_reviewers":
            continue
        reviewers = rule.get("reviewers")
        if isinstance(reviewers, list):
            count += len(reviewers)
    return count


def _classic_protection_checks(protection: Any) -> tuple[int, int, bool]:
    if not isinstance(protection, dict):
        return 0, 0, False
    reviews = protection.get("required_pull_request_reviews")
    review_count = (
        reviews.get("required_approving_review_count", 0)
        if isinstance(reviews, dict)
        else 0
    )
    statuses = protection.get("required_status_checks")
    status_count = 0
    if isinstance(statuses, dict):
        checks = statuses.get("checks")
        contexts = statuses.get("contexts")
        if isinstance(checks, list):
            status_count = len(checks)
        elif isinstance(contexts, list):
            status_count = len(contexts)
    enforce_admins = protection.get("enforce_admins")
    admin_enabled = (
        enforce_admins.get("enabled") is True
        if isinstance(enforce_admins, dict)
        else False
    )
    return (
        review_count if isinstance(review_count, int) else 0,
        status_count,
        admin_enabled,
    )


def _ruleset_targets_main(ruleset: dict[str, Any]) -> bool:
    if ruleset.get("target") != "branch" or ruleset.get("enforcement") != "active":
        return False
    conditions = ruleset.get("conditions")
    if not isinstance(conditions, dict):
        return False
    ref_name = conditions.get("ref_name")
    if not isinstance(ref_name, dict):
        return False
    includes = ref_name.get("include")
    if not isinstance(includes, list):
        return False
    return any(value in {"~DEFAULT_BRANCH", "refs/heads/main"} for value in includes)


def _ruleset_protection(
    repository: str,
    api_get: ApiGet,
) -> tuple[int, int, int]:
    summaries = optional_get(
        api_get, f"/repos/{repository}/rulesets?includes_parents=true"
    )
    if not isinstance(summaries, list):
        return 0, 0, 0
    review_count = 0
    status_count = 0
    active_count = 0
    for summary in summaries:
        if not isinstance(summary, dict) or not isinstance(summary.get("id"), int):
            continue
        detail = optional_get(api_get, f"/repos/{repository}/rulesets/{summary['id']}")
        if not isinstance(detail, dict) or not _ruleset_targets_main(detail):
            continue
        active_count += 1
        rules = detail.get("rules")
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            parameters = rule.get("parameters")
            parameters = parameters if isinstance(parameters, dict) else {}
            if rule.get("type") == "pull_request":
                count = parameters.get("required_approving_review_count", 0)
                if isinstance(count, int):
                    review_count = max(review_count, count)
            if rule.get("type") == "required_status_checks":
                checks = parameters.get("required_status_checks")
                if isinstance(checks, list):
                    status_count = max(status_count, len(checks))
    return review_count, status_count, active_count


def build_report(
    repository: str,
    *,
    release_sha: str,
    product_version: str,
    phase: str,
    api_get: ApiGet = gh_api_get,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    if not REPOSITORY.fullmatch(repository):
        raise ValueError("repository must use OWNER/REPO syntax")
    if repository.casefold() in FORBIDDEN_REPOSITORIES:
        raise ValueError("product source repository cannot host the independent Playbook")
    if not FULL_SHA.fullmatch(release_sha):
        raise ValueError("release_sha must be a 40-character lowercase Git SHA")
    if not PRODUCT_VERSION.fullmatch(product_version):
        raise ValueError("product_version is invalid")
    if phase not in {"intake", "release"}:
        raise ValueError("phase must be intake or release")

    repo = api_get(f"/repos/{repository}")
    if not isinstance(repo, dict):
        raise GitHubApiError(f"/repos/{repository}", None)

    full_name = str(repo.get("full_name", ""))
    is_public = repo.get("private") is False and repo.get("visibility") == "public"
    permissions = repo.get("permissions")
    permissions = permissions if isinstance(permissions, dict) else {}
    size = repo.get("size")
    is_empty = isinstance(size, int) and size == 0
    repository_checks = [
        _bool_check(
            "exact_repository_identity",
            full_name.casefold() == repository.casefold(),
            "GitHub returned the requested OWNER/REPO identity",
        ),
        _bool_check(
            "public_visibility",
            is_public,
            "the training website repository must be public",
        ),
        _bool_check(
            "independent_history",
            repo.get("fork") is False
            and not repo.get("parent")
            and not repo.get("source"),
            "the repository must not be a fork or derived source relationship",
        ),
        _bool_check(
            "active_repository",
            repo.get("archived") is False and repo.get("disabled") is False,
            "the repository must be active",
        ),
        _bool_check(
            "administrator_access",
            permissions.get("admin") is True,
            "the authenticated operator needs repository administration access",
        ),
    ]
    if phase == "intake":
        repository_checks.append(
            _bool_check(
                "empty_repository",
                is_empty,
                "intake requires the user-provided repository to be empty",
            )
        )
    else:
        repository_checks.append(
            _bool_check(
                "main_branch_present",
                repo.get("default_branch") == "main" and not is_empty,
                "release audit requires the independent main branch",
            )
        )

    repository_evidence = _evidence(EVIDENCE_IDS[0], repository_checks)
    if phase == "intake":
        evidence = [
            repository_evidence,
            _evidence(EVIDENCE_IDS[1], [], status="not-evaluated"),
            _evidence(EVIDENCE_IDS[2], [], status="not-evaluated"),
        ]
        ready = repository_evidence["status"] == "passed"
        decision = "ready-for-bootstrap" if ready else "blocked"
    else:
        actions = optional_get(api_get, f"/repos/{repository}/actions/permissions")
        workflow_permissions = optional_get(
            api_get, f"/repos/{repository}/actions/permissions/workflow"
        )
        pages = optional_get(api_get, f"/repos/{repository}/pages")
        environment = optional_get(
            api_get, f"/repos/{repository}/environments/github-pages"
        )
        reviewer_count = _required_reviewer_count(environment)
        source = pages.get("source") if isinstance(pages, dict) else None
        source = source if isinstance(source, dict) else {}
        pages_checks = [
            _bool_check(
                "actions_enabled",
                isinstance(actions, dict) and actions.get("enabled") is True,
                "GitHub Actions must be enabled",
            ),
            _bool_check(
                "workflow_permissions_visible",
                isinstance(workflow_permissions, dict)
                and workflow_permissions.get("default_workflow_permissions")
                in {"read", "write"},
                "workflow token policy must be readable",
            ),
            _bool_check(
                "pages_gh_pages_source",
                isinstance(pages, dict) and source.get("branch") == "gh-pages",
                "Pages must publish from the independent gh-pages branch",
            ),
            _bool_check(
                "pages_environment_approval",
                reviewer_count >= 1,
                "the github-pages environment needs at least one required reviewer",
            ),
            _bool_check(
                "pages_administrator_access",
                permissions.get("admin") is True,
                "the operator needs administration access for Pages settings",
            ),
        ]
        pages_evidence = _evidence(EVIDENCE_IDS[1], pages_checks)

        classic = optional_get(
            api_get, f"/repos/{repository}/branches/main/protection"
        )
        classic_reviews, classic_statuses, classic_admins = (
            _classic_protection_checks(classic)
        )
        classic_ready = (
            classic_reviews >= 1 and classic_statuses >= 1 and classic_admins
        )
        if classic_ready:
            ruleset_reviews, ruleset_statuses, active_rulesets = 0, 0, 0
        else:
            ruleset_reviews, ruleset_statuses, active_rulesets = _ruleset_protection(
                repository, api_get
            )
        ruleset_ready = (
            ruleset_reviews >= 1
            and ruleset_statuses >= 1
            and active_rulesets >= 1
        )
        protected = classic_ready or ruleset_ready
        protection_checks = [
            _bool_check(
                "main_protection_active",
                protected,
                "main needs classic protection with admin enforcement or an active ruleset",
            ),
            _bool_check(
                "pull_request_review_required",
                max(classic_reviews, ruleset_reviews) >= 1,
                "main changes need at least one approving review",
            ),
            _bool_check(
                "validation_status_required",
                max(classic_statuses, ruleset_statuses) >= 1,
                "main needs at least one required validation status check",
            ),
        ]
        protection_evidence = _evidence(EVIDENCE_IDS[2], protection_checks)
        evidence = [repository_evidence, pages_evidence, protection_evidence]
        ready = all(item["status"] == "passed" for item in evidence)
        decision = "ready-for-receipt-review" if ready else "blocked"

    blocked = [
        {
            "evidence_id": item["id"],
            "checks": [
                check["name"]
                for check in item["checks"]
                if check.get("passed") is False
            ],
        }
        for item in evidence
        if item["status"] == "blocked"
    ]
    checked_at = now or dt.datetime.now(dt.timezone.utc)
    if checked_at.tzinfo is None:
        checked_at = checked_at.replace(tzinfo=dt.timezone.utc)
    displayed_repository = (
        full_name if is_public else "<redacted-non-public-repository>"
    )
    return {
        "schema_version": 1,
        "audit_mode": "read-only-github-api",
        "phase": phase,
        "checked_at": checked_at.astimezone(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "release_sha": release_sha,
        "product_version": product_version,
        "repository": displayed_repository,
        "public_safe": is_public,
        "decision": {
            "status": decision,
            "blocked": blocked,
            "receipt_created": False,
            "release_state_changed": False,
        },
        "evidence": evidence,
        "evidence_boundary": {
            "external_writes": False,
            "repository_created": False,
            "remote_added": False,
            "branch_pushed": False,
            "pages_deployed": False,
            "human_review_still_required": True,
        },
    }


def parse_args() -> argparse.Namespace:
    default_sha, default_version = load_release_baseline()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="独立公开仓库 OWNER/REPO")
    parser.add_argument(
        "--phase",
        choices=("intake", "release"),
        default="release",
        help="intake 要求空仓库；release 核验 Pages 与 main 保护",
    )
    parser.add_argument("--release-sha", default=default_sha)
    parser.add_argument("--product-version", default=default_version)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = build_report(
            args.repository,
            release_sha=args.release_sha,
            product_version=args.product_version,
            phase=args.phase,
        )
    except (GitHubApiError, OSError, ValueError) as exc:
        print(f"GitHub 仓库只读门禁失败：{exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0 if report["decision"]["status"] != "blocked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
