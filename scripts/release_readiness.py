#!/usr/bin/env python3
"""Render the declared Playbook release state without changing any gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

try:
    from validate_content import GATE_EVIDENCE_CONTRACTS
except ModuleNotFoundError:  # pragma: no cover - package import path
    from scripts.validate_content import GATE_EVIDENCE_CONTRACTS


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return payload


def build_report(root: Path = PROJECT_ROOT) -> dict[str, Any]:
    release = load_yaml(root / "data/release.yml")
    screenshot_plan = load_yaml(root / "data/manifests/screenshot-plan.yml")
    screenshot_manifest = load_yaml(root / "data/manifests/screenshots.yml")

    gate_items: list[dict[str, Any]] = []
    for name, raw_gate in release.get("external_gates", {}).items():
        gate = raw_gate if isinstance(raw_gate, dict) else {}
        gate_items.append(
            {
                "name": name,
                "status": gate.get("status", "invalid"),
                "release_sha": gate.get("release_sha"),
                "verified_at": gate.get("verified_at"),
                "required_evidence": gate.get("required_evidence", []),
            }
        )

    passed_gates = [item for item in gate_items if item["status"] == "passed"]
    blocked_gates = [item for item in gate_items if item["status"] != "passed"]
    declared_gate_names = {str(item["name"]) for item in gate_items}
    expected_gate_names = set(GATE_EVIDENCE_CONTRACTS)
    missing_gates = sorted(expected_gate_names - declared_gate_names)
    unexpected_gates = sorted(declared_gate_names - expected_gate_names)
    captured = screenshot_manifest.get("screenshots", [])
    captured_count = len(captured) if isinstance(captured, list) else 0
    planned_count = screenshot_plan.get("count", 0)
    screenshots_ready = (
        release.get("screenshot_baseline", {}).get("status") == "passed"
        and screenshot_manifest.get("capture_status") == "passed"
        and isinstance(planned_count, int)
        and planned_count > 0
        and captured_count == planned_count
    )
    ready = (
        release.get("publication_status") == "release-ready"
        and bool(gate_items)
        and not blocked_gates
        and not missing_gates
        and not unexpected_gates
        and screenshots_ready
    )

    blockers = [f"external_gate:{item['name']}" for item in blocked_gates]
    blockers.extend(f"missing_external_gate:{name}" for name in missing_gates)
    blockers.extend(f"unexpected_external_gate:{name}" for name in unexpected_gates)
    if release.get("screenshot_baseline", {}).get("status") != "passed":
        blockers.append("screenshot_baseline")
    if screenshot_manifest.get("capture_status") != "passed":
        blockers.append("screenshot_manifest")
    if release.get("publication_status") != "release-ready":
        blockers.append("publication_status")

    return {
        "schema_version": 1,
        "site_title": release.get("site_title"),
        "publication_status": release.get("publication_status"),
        "fact_baseline": release.get("fact_baseline"),
        "decision": {
            "status": "ready" if ready else "blocked",
            "blocker_count": len(blockers),
            "blockers": blockers,
        },
        "external_gates": {
            "total": len(gate_items),
            "passed": len(passed_gates),
            "blocked": len(blocked_gates),
            "missing": missing_gates,
            "unexpected": unexpected_gates,
            "items": gate_items,
        },
        "screenshots": {
            "baseline_status": release.get("screenshot_baseline", {}).get("status"),
            "manifest_status": screenshot_manifest.get("capture_status"),
            "planned": planned_count,
            "captured": captured_count,
        },
        "evidence_boundary": {
            "declared_scope": "repository-state-only",
            "local_browser_smoke_is_production_acceptance": False,
            "public_deployment_evidenced": False,
            "report_alone_is_release_evidence": False,
            "forbidden_claims_when_blocked": [
                "GitHub Pages 已发布",
                "FlowAgentic 生产环境已完成 Chrome/Firefox 验收",
                "正式截图已采集并脱敏",
                "DeepSeek 与 Kimi 隔离实验已完成",
            ],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="同时写入 UTF-8 JSON 文件")
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="状态不是 ready 时返回退出码 2",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    if args.require_ready and report["decision"]["status"] != "ready":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
