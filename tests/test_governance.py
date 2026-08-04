from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.validate_content import (
    GATE_EVIDENCE_CONTRACTS,
    evidence_aggregate_sha256,
    provider_run_matches_ledger_call,
    validate_external_gate_contracts,
    validate_gate_receipt,
    validate_provider_account_controls,
)


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_browser_bootstrap_guards_empty_hash_and_scopes_mermaid() -> None:
    content_override = (
        ROOT / "overrides/partials/javascripts/content.html"
    ).read_text(encoding="utf-8")
    main_override = (ROOT / "overrides/main.html").read_text(encoding="utf-8")
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    diagram_pages = [
        path
        for path in (ROOT / "docs").rglob("*.md")
        if "```mermaid\n" in path.read_text(encoding="utf-8")
    ]

    assert "hash?document.getElementById(hash):null" in content_override
    assert "var target=document.getElementById(location.hash.slice(1))" not in content_override
    assert "page.meta.mermaid" in main_override
    assert "'assets/vendor/mermaid.min.js' | url" in main_override
    assert diagram_pages
    assert all(
        "\nmermaid: true\n" in path.read_text(encoding="utf-8").split("---", 2)[1]
        for path in diagram_pages
    )
    assert "assets/vendor/mermaid.min.js" not in mkdocs
    assert "assets/javascripts/mermaid-init.js" not in mkdocs


def test_browser_smoke_wrapper_rejects_cli_soft_errors() -> None:
    wrapper = (ROOT / "scripts/browser_smoke_cli.sh").read_text(encoding="utf-8")

    assert 'grep -Fq "### Error"' in wrapper
    assert '"status"[[:space:]]*:[[:space:]]*"passed"' in wrapper
    assert "browser workflow did not produce an explicit pass" in wrapper


def test_pages_publish_workflow_archives_and_deploys_verified_tree() -> None:
    workflow = (ROOT / ".github/workflows/publish.yml").read_text(
        encoding="utf-8"
    )

    assert (
        "uses: actions/upload-pages-artifact@"
        "fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0"
    ) in workflow
    assert "path: ${{ runner.temp }}/published-site" in workflow
    assert "include-hidden-files: true" in workflow
    assert "pages: write" in workflow
    assert "id-token: write" in workflow
    assert (
        "uses: actions/deploy-pages@"
        "cd2ce8fcbc39b97be8ca5fce6e763baed58fa128 # v5.0.0"
    ) in workflow
    assert workflow.index("git push origin HEAD:gh-pages") < workflow.index(
        "uses: actions/deploy-pages@"
    )
    assert "url: ${{ steps.deployment.outputs.page_url }}" in workflow


def _run_release_gate(release_sha: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "release_gate.py"),
            "--release-version",
            f"flowagentic-3.1.3-{release_sha[:8]}",
            "--release-sha",
            release_sha,
            "--product-version",
            "3.1.3",
            "--screenshot-gate",
            "passed",
            "--chinese-gate",
            "passed",
            "--confirmation",
            "publish",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_release_gate_does_not_reject_current_fact_baseline_as_legacy() -> None:
    result = _run_release_gate("96f6ae464f7f4757883a5ba6bec26ca951b4da4d")

    assert result.returncode == 1
    assert "不得用旧基线 70d8040e 发布正式截图版" not in result.stderr


def test_release_gate_rejects_actual_legacy_baseline() -> None:
    result = _run_release_gate("70d8040e5ead30a7a51e2231a6a156d5632e6e25")

    assert result.returncode == 1
    assert "不得用旧基线 70d8040e 发布正式截图版" in result.stderr


def test_release_readiness_reports_current_external_blockers() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "release_readiness.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["publication_status"] == "working-draft"
    assert report["fact_baseline"]["release_sha"] == (
        "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
    )
    assert report["decision"]["status"] == "blocked"
    assert report["decision"]["blocker_count"] == 10
    assert report["external_gates"]["total"] == 9
    assert report["external_gates"]["passed"] == 2
    assert report["external_gates"]["blocked"] == 7
    assert report["external_gates"]["missing"] == []
    assert report["external_gates"]["unexpected"] == []
    assert report["external_gates"]["items"][0]["name"] == "github_repository"
    assert report["external_gates"]["items"][0]["status"] == "passed"
    assert report["screenshots"] == {
        "baseline_status": "blocked",
        "manifest_status": "blocked",
        "planned": 252,
        "captured": 0,
    }
    assert report["evidence_boundary"][
        "local_browser_smoke_is_production_acceptance"
    ] is False
    assert report["evidence_boundary"]["public_deployment_evidenced"] is False
    assert report["evidence_boundary"]["report_alone_is_release_evidence"] is False


def test_current_github_repository_receipt_is_artifact_bound() -> None:
    release = load("data/release.yml")
    state = release["external_gates"]["github_repository"]

    assert validate_gate_receipt(
        "github_repository",
        state,
        release_sha=release["fact_baseline"]["release_sha"],
        product_version=release["fact_baseline"]["product_version"],
        root=ROOT,
        now=dt.datetime(2026, 8, 4, 13, 0, tzinfo=dt.timezone.utc),
    ) == []


def test_current_isolated_training_receipt_is_artifact_bound() -> None:
    release = load("data/release.yml")
    state = release["external_gates"]["isolated_training_environment"]

    assert validate_gate_receipt(
        "isolated_training_environment",
        state,
        release_sha=release["fact_baseline"]["release_sha"],
        product_version=release["fact_baseline"]["product_version"],
        root=ROOT,
        now=dt.datetime(2026, 8, 4, 13, 0, tzinfo=dt.timezone.utc),
    ) == []


def test_release_readiness_require_ready_fails_closed() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "release_readiness.py"),
            "--require-ready",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert json.loads(result.stdout)["decision"]["status"] == "blocked"


def _valid_gate_state(
    tmp_path: Path,
    gate_name: str = "chrome_pc_acceptance",
) -> dict[str, Any]:
    contract = GATE_EVIDENCE_CONTRACTS[gate_name]
    evidence_items: list[dict[str, Any]] = []
    aggregate_items: list[tuple[str, str]] = []
    for index, item_id in enumerate(contract["evidence_ids"], start=1):
        relative = Path("data") / "evidence" / gate_name / f"evidence-{index}.json"
        artifact = tmp_path / relative
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(
            f'{{"evidence_id":"{item_id}","result":"passed"}}\n',
            encoding="utf-8",
        )
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        evidence_items.append(
            {
                "id": item_id,
                "status": "passed",
                "count": 1,
                "artifact": relative.as_posix(),
                "sha256": digest,
            }
        )
        aggregate_items.append((item_id, digest))
    verified_at = "2026-08-01T00:00:00Z"
    return {
        "status": "passed",
        "release_sha": "1" * 40,
        "verified_at": verified_at,
        "required_evidence": list(contract["evidence_ids"]),
        "receipt": {
            "receipt_id": "RCT-CHROME-ACCEPTANCE-001",
            "evidence_type": contract["evidence_type"],
            "release_sha": "1" * 40,
            "product_version": "3.1.3",
            "public_safe": True,
            "reviewer": "independent-reviewer",
            "verified_at": verified_at,
            "artifact_sha256": evidence_aggregate_sha256(aggregate_items),
            "evidence_items": evidence_items,
        },
    }


def test_ten_complete_sop_modules_are_declared() -> None:
    features = load("data/feature-status.yml")["features"]
    assert sum(item["training_scope"] == "complete-sop" for item in features) == 10


def test_provider_budget_is_hard_capped() -> None:
    budget = load("data/experiments/provider-budget.yml")
    assert budget["currency"] == "CNY"
    assert float(budget["hard_limit"]) == 300.0
    assert budget["enforcement"]["stop_when_spent_gte_hard_limit"] is True
    assert budget["enforcement"]["allow_override"] is False
    assert budget["enforcement"]["ci_provider_calls"] is False
    assert budget["enforcement"]["synthetic_data_only"] is True
    assert budget["enforcement"]["start_requires_pending_reservation"] is True
    assert budget["enforcement"]["in_flight_reservations_count_against_limit"] is True
    assert budget["enforcement"]["uncertain_failure_charged_at_reserved_maximum"] is True
    assert budget["enforcement"]["provider_transport_must_use_budget_wrapper"] is True
    assert budget["enforcement"]["provider_account_hard_limit_receipt_required"] is True


def test_release_lifecycle_is_internally_consistent() -> None:
    release = load("data/release.yml")
    plan = load("data/manifests/screenshot-plan.yml")
    manifest = load("data/manifests/screenshots.yml")
    status = release["publication_status"]
    assert status in {"working-draft", "release-ready"}

    if status == "working-draft":
        assert all(
            gate["status"] in {"blocked", "passed"}
            for gate in release["external_gates"].values()
        )
        assert any(
            gate["status"] == "blocked"
            for gate in release["external_gates"].values()
        )
        assert release["screenshot_baseline"]["status"] == "blocked"
        assert manifest["capture_status"] == "blocked"
        assert manifest["screenshots"] == []
        assert all(item["capture_status"] == "blocked-by-G1" for item in plan["shots"])
        return

    release_sha = release["fact_baseline"]["release_sha"]
    product_version = str(release["fact_baseline"]["product_version"])
    assert all(gate["status"] == "passed" for gate in release["external_gates"].values())
    for gate in release["external_gates"].values():
        assert gate["release_sha"] == release_sha
        assert dt.datetime.fromisoformat(gate["verified_at"].replace("Z", "+00:00"))
        assert isinstance(gate["receipt"], dict)
        assert gate["receipt"]["release_sha"] == release_sha
        assert gate["receipt"]["public_safe"] is True
    screenshot = release["screenshot_baseline"]
    assert screenshot["status"] == "passed"
    assert screenshot["release_sha"] == release_sha
    assert str(screenshot["product_version"]) == product_version
    assert plan["release_sha"] == release_sha
    assert manifest["release_sha"] == release_sha
    assert manifest["capture_status"] == "passed"
    assert len(manifest["screenshots"]) == plan["count"]
    assert all(item["capture_status"] == "captured-verified" for item in plan["shots"])


def test_release_required_evidence_matches_fixed_contract() -> None:
    gates = load("data/release.yml")["external_gates"]

    assert validate_external_gate_contracts(gates) == []
    assert {
        gate_name: gate["required_evidence"] for gate_name, gate in gates.items()
    } == {
        gate_name: list(contract["evidence_ids"])
        for gate_name, contract in GATE_EVIDENCE_CONTRACTS.items()
    }


def test_gate_receipt_binds_exact_contract_and_real_artifacts(tmp_path: Path) -> None:
    state = _valid_gate_state(tmp_path)

    errors = validate_gate_receipt(
        "chrome_pc_acceptance",
        state,
        release_sha="1" * 40,
        product_version="3.1.3",
        root=tmp_path,
        now=dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc),
    )

    assert errors == []


def test_gate_receipt_rejects_weakened_ids_and_wrong_type(tmp_path: Path) -> None:
    state = _valid_gate_state(tmp_path)
    state["required_evidence"] = state["required_evidence"][:-1]
    state["receipt"]["evidence_type"] = "repository"

    errors = validate_gate_receipt(
        "chrome_pc_acceptance",
        state,
        release_sha="1" * 40,
        product_version="3.1.3",
        root=tmp_path,
        now=dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc),
    )

    assert any("required_evidence differs from fixed contract" in item for item in errors)
    assert any("evidence type does not match" in item for item in errors)


def test_gate_receipt_recomputes_artifact_digest(tmp_path: Path) -> None:
    state = _valid_gate_state(tmp_path)
    artifact = tmp_path / state["receipt"]["evidence_items"][0]["artifact"]
    artifact.write_text('{"result":"tampered"}\n', encoding="utf-8")

    errors = validate_gate_receipt(
        "chrome_pc_acceptance",
        state,
        release_sha="1" * 40,
        product_version="3.1.3",
        root=tmp_path,
        now=dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc),
    )

    assert any("evidence digest does not match file" in item for item in errors)
    assert any("artifact digest does not match evidence" in item for item in errors)


def test_gate_receipt_rejects_symlink_artifact(tmp_path: Path) -> None:
    state = _valid_gate_state(tmp_path)
    artifact = tmp_path / state["receipt"]["evidence_items"][0]["artifact"]
    target = artifact.with_name("target.json")
    target.write_bytes(artifact.read_bytes())
    artifact.unlink()
    artifact.symlink_to(target)

    errors = validate_gate_receipt(
        "chrome_pc_acceptance",
        state,
        release_sha="1" * 40,
        product_version="3.1.3",
        root=tmp_path,
        now=dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc),
    )

    assert any("artifact path contains a symlink" in item for item in errors)


def test_gate_receipt_rejects_future_time_placeholders_and_duplicate_ids(
    tmp_path: Path,
) -> None:
    state = _valid_gate_state(tmp_path)
    future = "2026-08-03T00:00:00Z"
    state["verified_at"] = future
    state["receipt"]["verified_at"] = future
    state["receipt"]["artifact_sha256"] = "0" * 64
    state["receipt"]["evidence_items"][0]["sha256"] = "a" * 64
    state["receipt"]["evidence_items"][1]["id"] = state["receipt"][
        "evidence_items"
    ][0]["id"]

    errors = validate_gate_receipt(
        "chrome_pc_acceptance",
        state,
        release_sha="1" * 40,
        product_version="3.1.3",
        root=tmp_path,
        now=dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc),
    )

    assert any("time is in the future" in item for item in errors)
    assert any("artifact digest is invalid or placeholder" in item for item in errors)
    assert any("evidence digest is invalid or placeholder" in item for item in errors)
    assert any("evidence ids are duplicated" in item for item in errors)


def test_external_gate_contract_rejects_duplicate_receipt_ids() -> None:
    gates = copy.deepcopy(load("data/release.yml")["external_gates"])
    duplicate = {"receipt_id": "RCT-DUPLICATE-RECEIPT"}
    gates["chrome_pc_acceptance"]["receipt"] = duplicate
    gates["firefox_pc_acceptance"]["receipt"] = duplicate.copy()

    errors = validate_external_gate_contracts(gates)

    assert any("receipt ids are duplicated" in item for item in errors)


def test_synthetic_fixtures_contain_no_real_endpoint() -> None:
    api = (ROOT / "data" / "fixtures" / "api" / "openapi.yml").read_text(encoding="utf-8")
    assert "training.invalid" in api


def test_screenshot_plan_stays_within_approved_budget() -> None:
    plan = load("data/manifests/screenshot-plan.yml")
    release = load("data/release.yml")
    assert plan["count"] == len(plan["shots"])
    assert 180 <= plan["count"] <= 260
    assert len({item["id"] for item in plan["shots"]}) == plan["count"]
    expected = (
        "blocked-by-G1"
        if release["publication_status"] == "working-draft"
        else "captured-verified"
    )
    assert all(item["capture_status"] == expected for item in plan["shots"])


def test_provider_guard_fails_closed_before_activation() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "provider_budget_guard.py"),
            "--provider",
            "DeepSeek",
            "--estimated-cost",
            "0.01",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "provider experiments are not active" in result.stderr


def test_provider_account_controls_accept_both_capped_providers() -> None:
    controls = [
        {
            "provider": provider,
            "auto_recharge": False,
            "status": "passed",
            "currency": "CNY",
            "hard_limit": 150,
            "receipt_sha256": "a" * 64,
        }
        for provider in ("DeepSeek", "Kimi")
    ]

    providers, errors = validate_provider_account_controls(controls)

    assert providers == {"DeepSeek", "Kimi"}
    assert errors == []


def test_provider_account_controls_reject_malformed_amount_without_crashing() -> None:
    providers, errors = validate_provider_account_controls(
        [
            {
                "provider": "DeepSeek",
                "auto_recharge": False,
                "status": "passed",
                "currency": "CNY",
                "hard_limit": "not-a-number",
                "receipt_sha256": "b" * 64,
            }
        ]
    )

    assert providers == set()
    assert errors == ["provider receipt contains an incomplete account control"]


def test_provider_account_controls_share_one_cny_300_cap() -> None:
    controls = [
        {
            "provider": provider,
            "auto_recharge": False,
            "status": "passed",
            "currency": "CNY",
            "hard_limit": 300,
            "receipt_sha256": "c" * 64,
        }
        for provider in ("DeepSeek", "Kimi")
    ]

    providers, errors = validate_provider_account_controls(controls)

    assert providers == {"DeepSeek", "Kimi"}
    assert "provider account hard limits exceed the shared CNY 300 cap" in errors


def test_provider_ledger_match_normalizes_equivalent_money_values() -> None:
    run = {
        "provider": "DeepSeek",
        "model": "deepseek-chat",
        "input_tokens": 120,
        "output_tokens": 30,
        "latency_ms": 500,
        "actual_cost": "0.12",
    }
    call = {**run, "actual_cost": 0.12}

    assert provider_run_matches_ledger_call(call, run) is True

    call["actual_cost"] = 0.13
    assert provider_run_matches_ledger_call(call, run) is False
