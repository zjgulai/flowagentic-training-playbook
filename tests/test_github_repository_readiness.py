from __future__ import annotations

import datetime as dt
from typing import Any

import pytest

from scripts.github_repository_readiness import (
    GitHubApiError,
    build_report,
)


REPOSITORY = "zjgulai/flowagentic-training-playbook"
RELEASE_SHA = "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"


def ready_repository(*, size: int = 42) -> dict[str, Any]:
    return {
        "full_name": REPOSITORY,
        "private": False,
        "visibility": "public",
        "fork": False,
        "parent": None,
        "source": None,
        "archived": False,
        "disabled": False,
        "size": size,
        "default_branch": "main",
        "permissions": {"admin": True, "push": True},
    }


def classic_ready_api(endpoint: str) -> Any:
    responses: dict[str, Any] = {
        f"/repos/{REPOSITORY}": ready_repository(size=0),
        f"/repos/{REPOSITORY}/branches/main": {
            "name": "main",
            "commit": {"sha": "23b805de49f55034603ed3c99419132cb568f015"},
        },
        f"/repos/{REPOSITORY}/actions/permissions": {
            "enabled": True,
            "allowed_actions": "all",
        },
        f"/repos/{REPOSITORY}/actions/permissions/workflow": {
            "default_workflow_permissions": "read",
            "can_approve_pull_request_reviews": False,
        },
        f"/repos/{REPOSITORY}/pages": {
            "html_url": "https://zjgulai.github.io/flowagentic-training-playbook/",
            "build_type": "legacy",
            "source": {"branch": "gh-pages", "path": "/"},
        },
        f"/repos/{REPOSITORY}/environments/github-pages": {
            "protection_rules": [
                {
                    "type": "required_reviewers",
                    "reviewers": [{"type": "User", "reviewer": {"login": "reviewer"}}],
                }
            ]
        },
        f"/repos/{REPOSITORY}/branches/main/protection": {
            "required_pull_request_reviews": {
                "required_approving_review_count": 1
            },
            "required_status_checks": {
                "checks": [{"context": "站点、PDF 与内容门禁", "app_id": 15368}]
            },
            "enforce_admins": {"enabled": True},
        },
    }
    if endpoint not in responses:
        raise AssertionError(f"unexpected endpoint: {endpoint}")
    return responses[endpoint]


def test_intake_requires_an_empty_public_independent_repository() -> None:
    requested: list[str] = []

    def api(endpoint: str) -> Any:
        requested.append(endpoint)
        return ready_repository(size=0)

    report = build_report(
        REPOSITORY,
        release_sha=RELEASE_SHA,
        product_version="3.1.3",
        phase="intake",
        api_get=api,
        now=dt.datetime(2026, 8, 4, tzinfo=dt.timezone.utc),
    )

    assert requested == [f"/repos/{REPOSITORY}"]
    assert report["decision"]["status"] == "ready-for-bootstrap"
    assert [item["status"] for item in report["evidence"]] == [
        "passed",
        "not-evaluated",
        "not-evaluated",
    ]
    assert report["evidence_boundary"]["external_writes"] is False
    assert report["decision"]["receipt_created"] is False


def test_release_accepts_classic_protection_pages_and_human_approval() -> None:
    report = build_report(
        REPOSITORY,
        release_sha=RELEASE_SHA,
        product_version="3.1.3",
        phase="release",
        api_get=classic_ready_api,
        now=dt.datetime(2026, 8, 4, tzinfo=dt.timezone.utc),
    )

    assert report["decision"]["status"] == "ready-for-receipt-review"
    assert all(item["status"] == "passed" for item in report["evidence"])
    assert report["public_safe"] is True
    assert report["evidence_boundary"]["human_review_still_required"] is True


def test_release_accepts_an_active_ruleset_for_main() -> None:
    def api(endpoint: str) -> Any:
        if endpoint == f"/repos/{REPOSITORY}/branches/main/protection":
            raise GitHubApiError(endpoint, 404)
        if endpoint == f"/repos/{REPOSITORY}/rulesets?includes_parents=true":
            return [{"id": 7, "name": "Protect main"}]
        if endpoint == f"/repos/{REPOSITORY}/rulesets/7":
            return {
                "id": 7,
                "target": "branch",
                "enforcement": "active",
                "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"]}},
                "rules": [
                    {
                        "type": "pull_request",
                        "parameters": {"required_approving_review_count": 1},
                    },
                    {
                        "type": "required_status_checks",
                        "parameters": {
                            "required_status_checks": [
                                {"context": "站点、PDF 与内容门禁"}
                            ]
                        },
                    },
                ],
            }
        return classic_ready_api(endpoint)

    report = build_report(
        REPOSITORY,
        release_sha=RELEASE_SHA,
        product_version="3.1.3",
        phase="release",
        api_get=api,
    )

    protection = report["evidence"][2]
    assert protection["status"] == "passed"
    assert report["decision"]["status"] == "ready-for-receipt-review"


def test_release_fails_closed_when_pages_and_protection_are_missing() -> None:
    def api(endpoint: str) -> Any:
        if endpoint == f"/repos/{REPOSITORY}":
            return ready_repository()
        if endpoint == f"/repos/{REPOSITORY}/branches/main":
            return {
                "name": "main",
                "commit": {"sha": "23b805de49f55034603ed3c99419132cb568f015"},
            }
        if endpoint == f"/repos/{REPOSITORY}/actions/permissions":
            return {"enabled": True}
        if endpoint == f"/repos/{REPOSITORY}/actions/permissions/workflow":
            return {"default_workflow_permissions": "read"}
        raise GitHubApiError(endpoint, 404)

    report = build_report(
        REPOSITORY,
        release_sha=RELEASE_SHA,
        product_version="3.1.3",
        phase="release",
        api_get=api,
    )

    assert report["decision"]["status"] == "blocked"
    assert report["evidence"][0]["status"] == "passed"
    assert report["evidence"][1]["status"] == "blocked"
    assert report["evidence"][2]["status"] == "blocked"
    assert report["decision"]["release_state_changed"] is False


def test_private_repository_identity_is_redacted_and_not_public_safe() -> None:
    def api(endpoint: str) -> Any:
        if endpoint == f"/repos/{REPOSITORY}":
            repo = ready_repository(size=0)
            repo["private"] = True
            repo["visibility"] = "private"
            return repo
        raise AssertionError(f"unexpected endpoint: {endpoint}")

    report = build_report(
        REPOSITORY,
        release_sha=RELEASE_SHA,
        product_version="3.1.3",
        phase="intake",
        api_get=api,
    )

    assert report["decision"]["status"] == "blocked"
    assert report["repository"] == "<redacted-non-public-repository>"
    assert report["public_safe"] is False


def test_product_source_repository_is_rejected() -> None:
    with pytest.raises(ValueError, match="product source repository"):
        build_report(
            "zjgulai/Flowise",
            release_sha=RELEASE_SHA,
            product_version="3.1.3",
            phase="intake",
            api_get=lambda _endpoint: {},
        )
