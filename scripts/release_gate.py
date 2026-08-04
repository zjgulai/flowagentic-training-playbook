#!/usr/bin/env python3
"""Validate all human-provided inputs before a mike production publish."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

try:
    from validate_content import validate_release_config
except ModuleNotFoundError:  # pragma: no cover - package import path
    from scripts.validate_content import validate_release_config

LEGACY_BASELINE_SHA = "70d8040e5ead30a7a51e2231a6a156d5632e6e25"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHORT_SHA = re.compile(r"^[0-9a-f]{7,12}$")
PRODUCT_VERSION = re.compile(
    r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?$"
)
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验中文版本、截图和人工确认发布门禁。"
    )
    parser.add_argument(
        "--release-version",
        default=os.environ.get("PLAYBOOK_RELEASE_VERSION", ""),
    )
    parser.add_argument(
        "--release-sha",
        default=os.environ.get("PLAYBOOK_RELEASE_SHA", ""),
    )
    parser.add_argument(
        "--product-version",
        default=os.environ.get("FLOWAGENTIC_PRODUCT_VERSION", ""),
    )
    parser.add_argument(
        "--screenshot-gate",
        default=os.environ.get("PLAYBOOK_SCREENSHOT_GATE", ""),
    )
    parser.add_argument(
        "--chinese-gate",
        default=os.environ.get("PLAYBOOK_CHINESE_GATE", ""),
    )
    parser.add_argument(
        "--confirmation",
        default=os.environ.get("PLAYBOOK_RELEASE_CONFIRMATION", ""),
    )
    return parser.parse_args()


def load_yaml(path: Path, issues: list[str], label: str) -> dict[str, object]:
    if not path.is_file():
        issues.append(f"缺少{label}：{path.relative_to(PROJECT_ROOT)}")
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        issues.append(f"{label}无法读取：{exc}")
        return {}
    if not isinstance(payload, dict):
        issues.append(f"{label}顶层必须是对象")
        return {}
    return payload


def validate_repository_bindings(
    args: argparse.Namespace, issues: list[str]
) -> None:
    release = load_yaml(
        PROJECT_ROOT / "data/release.yml",
        issues,
        "版本事实文件",
    )
    manifest = load_yaml(
        PROJECT_ROOT / "data/manifests/screenshots.yml",
        issues,
        "截图 manifest",
    )
    screenshot_plan = load_yaml(
        PROJECT_ROOT / "data/manifests/screenshot-plan.yml",
        issues,
        "截图计划",
    )
    if not release or not manifest or not screenshot_plan:
        return

    baseline = release.get("fact_baseline", {})
    if not isinstance(baseline, dict):
        issues.append("data/release.yml 缺少 fact_baseline")
        baseline = {}
    fact_version = str(baseline.get("product_version", ""))
    fact_sha = str(baseline.get("release_sha", ""))
    if fact_version != args.product_version:
        issues.append("工作流产品版本与 data/release.yml fact_baseline 不一致")
    if fact_sha != args.release_sha:
        issues.append("工作流发布 SHA 与 data/release.yml fact_baseline 不一致")
    if release.get("publication_status") != "release-ready":
        issues.append("data/release.yml publication_status 必须为 release-ready")

    external_gates = release.get("external_gates", {})
    if not isinstance(external_gates, dict):
        issues.append("data/release.yml 缺少 external_gates")
        external_gates = {}
    present_gates = set(external_gates)
    missing_gates = sorted(REQUIRED_EXTERNAL_GATES - present_gates)
    unknown_gates = sorted(present_gates - REQUIRED_EXTERNAL_GATES)
    if missing_gates:
        issues.append(f"缺少强制外部门禁：{', '.join(missing_gates)}")
    if unknown_gates:
        issues.append(f"存在未审批的外部门禁：{', '.join(unknown_gates)}")
    for gate_name in sorted(REQUIRED_EXTERNAL_GATES):
        state = external_gates.get(gate_name)
        if not isinstance(state, dict) or state.get("status") != "passed":
            issues.append(f"外部门禁未通过：{gate_name}")
            continue
        if str(state.get("release_sha", "")) != args.release_sha:
            issues.append(f"外部门禁未绑定发布 SHA：{gate_name}")
        if not state.get("verified_at"):
            issues.append(f"外部门禁缺少验收时间：{gate_name}")
        receipt = state.get("receipt")
        if not isinstance(receipt, dict):
            issues.append(f"外部门禁缺少结构化回执：{gate_name}")
            continue
        if str(receipt.get("release_sha", "")) != args.release_sha:
            issues.append(f"外部门禁回执未绑定发布 SHA：{gate_name}")
        if str(receipt.get("product_version", "")) != args.product_version:
            issues.append(f"外部门禁回执未绑定产品版本：{gate_name}")
        if receipt.get("public_safe") is not True:
            issues.append(f"外部门禁回执未通过公开安全检查：{gate_name}")
        if not re.fullmatch(
            r"[0-9a-f]{64}", str(receipt.get("artifact_sha256", ""))
        ):
            issues.append(f"外部门禁回执缺少有效制品摘要：{gate_name}")
        evidence_items = receipt.get("evidence_items")
        required_evidence = state.get("required_evidence", [])
        if (
            not isinstance(evidence_items, list)
            or len(evidence_items) < len(required_evidence)
        ):
            issues.append(f"外部门禁回执未覆盖强制证据：{gate_name}")

    screenshot_baseline = release.get("screenshot_baseline", {})
    if not isinstance(screenshot_baseline, dict):
        issues.append("data/release.yml 缺少 screenshot_baseline")
        screenshot_baseline = {}
    if screenshot_baseline.get("status") != "passed":
        issues.append("screenshot_baseline.status 必须为 passed")
    if str(screenshot_baseline.get("product_version", "")) != args.product_version:
        issues.append("截图基线产品版本与工作流输入不一致")
    if str(screenshot_baseline.get("release_sha", "")) != args.release_sha:
        issues.append("截图基线 SHA 与工作流输入不一致")
    if not screenshot_baseline.get("deployed_at"):
        issues.append("截图基线缺少 deployed_at")

    if manifest.get("capture_status") != "passed":
        issues.append("截图 manifest capture_status 必须为 passed")
    if str(manifest.get("release_sha", "")) != args.release_sha:
        issues.append("截图 manifest SHA 与工作流输入不一致")
    screenshots = manifest.get("screenshots", [])
    if not isinstance(screenshots, list) or not screenshots:
        issues.append("截图 manifest 必须包含已采集截图")
        screenshots = []
    screenshot_sha_mismatches: list[str] = []
    for item in screenshots:
        if not isinstance(item, dict):
            issues.append("截图 manifest 包含无效条目")
            continue
        identifier = item.get("id", "<unknown>")
        if str(item.get("release_sha", "")) != args.release_sha:
            screenshot_sha_mismatches.append(str(identifier))
    if screenshot_sha_mismatches:
        sample = ", ".join(screenshot_sha_mismatches[:5])
        issues.append(
            f"{len(screenshot_sha_mismatches)} 张截图未绑定工作流发布 SHA"
            f"（示例：{sample}）"
        )

    if str(screenshot_plan.get("release_sha", "")) != args.release_sha:
        issues.append("截图计划 SHA 与工作流输入不一致")
    planned = screenshot_plan.get("shots", [])
    if not isinstance(planned, list) or not planned:
        issues.append("截图计划不得为空")
        planned = []
    plan_sha_mismatches: list[str] = []
    for item in planned:
        if not isinstance(item, dict):
            issues.append("截图计划包含无效条目")
            continue
        if not item.get("required_for_release"):
            continue
        identifier = item.get("id", "<unknown>")
        if str(item.get("release_sha", "")) != args.release_sha:
            plan_sha_mismatches.append(str(identifier))
    if plan_sha_mismatches:
        sample = ", ".join(plan_sha_mismatches[:5])
        issues.append(
            f"{len(plan_sha_mismatches)} 个必需截图计划未绑定工作流发布 SHA"
            f"（示例：{sample}）"
        )

    issues.extend(
        f"发布证据门禁：{issue}" for issue in validate_release_config(True)
    )


def main() -> int:
    args = parse_args()
    issues: list[str] = []

    if not FULL_SHA.fullmatch(args.release_sha):
        issues.append("release_sha 必须是 40 位小写十六进制 Git SHA")
    elif args.release_sha == LEGACY_BASELINE_SHA:
        issues.append("不得用旧基线 70d8040e 发布正式截图版")

    if not PRODUCT_VERSION.fullmatch(args.product_version):
        issues.append("product_version 必须是明确的语义化产品版本")

    expected_prefix = f"flowagentic-{args.product_version}-"
    if not args.release_version.startswith(expected_prefix):
        issues.append(
            "release_version 必须采用 "
            "flowagentic-<product_version>-<short-sha> 格式"
        )
        short_sha = ""
    else:
        short_sha = args.release_version[len(expected_prefix) :]
    if not SHORT_SHA.fullmatch(short_sha):
        issues.append("release_version 末尾必须是 7 至 12 位小写短 SHA")
    elif FULL_SHA.fullmatch(args.release_sha) and not args.release_sha.startswith(
        short_sha
    ):
        issues.append("release_version 的短 SHA 与 release_sha 不一致")

    if args.chinese_gate != "passed":
        issues.append("全中文优化版验收门禁未通过")
    if args.screenshot_gate != "passed":
        issues.append("截图、脱敏和 manifest 门禁未通过")
    if args.confirmation != "publish":
        issues.append("人工发布确认词必须精确为 publish")

    validate_repository_bindings(args, issues)

    if os.environ.get("GITHUB_ACTIONS") == "true":
        if os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch":
            issues.append("生产发布只能由 workflow_dispatch 手动触发")
        if os.environ.get("GITHUB_REF") != "refs/heads/main":
            issues.append("生产发布只能从 main 分支触发")
        if os.environ.get("PLAYBOOK_RELEASE_MODE") != "1":
            issues.append("发布工作流必须启用 PLAYBOOK_RELEASE_MODE=1")

    if issues:
        print("发布门禁失败：", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print(
        "发布门禁通过："
        f"{args.release_version} -> {args.release_sha}；中文与截图门禁均已确认。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
