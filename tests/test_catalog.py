from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA = "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"


def catalog() -> dict:
    return json.loads((ROOT / "data" / "catalog" / "nodes.json").read_text(encoding="utf-8"))


def test_baseline_catalog_is_complete_and_unique() -> None:
    payload = catalog()
    nodes = payload["nodes"]
    assert payload["release_sha"] == BASELINE_SHA
    assert payload["count"] == 311
    assert len(nodes) == 311
    assert len({node["id"] for node in nodes}) == 311
    assert len({node["category"] for node in nodes}) >= 25


def test_every_node_has_public_reference_fields() -> None:
    allowed_risk_values = {"yes", "no", "review-required"}
    for node in catalog()["nodes"]:
        assert node["name"]
        assert node["label"]
        assert node["category"]
        assert node["source_anchor"].endswith(f"@{BASELINE_SHA}")
        assert node["example"]
        assert node["common_errors"]
        assert set(node["risk"]) == {"external_call", "may_cost", "may_write", "rationale"}
        assert {
            node["risk"]["external_call"],
            node["risk"]["may_cost"],
            node["risk"]["may_write"],
        } <= allowed_risk_values
        if not node["outputs"]:
            assert any("源码未静态声明 outputs" in warning for warning in node["extraction"]["warnings"])


def test_thirteen_detailed_agentflow_nodes_are_present() -> None:
    names = {node["name"] for node in catalog()["nodes"]}
    expected = {
        "startAgentflow",
        "agentAgentflow",
        "llmAgentflow",
        "conditionAgentflow",
        "conditionAgentAgentflow",
        "directReplyAgentflow",
        "customFunctionAgentflow",
        "toolAgentflow",
        "retrieverAgentflow",
        "stickyNoteAgentflow",
        "httpAgentflow",
        "iterationAgentflow",
        "executeFlowAgentflow",
    }
    assert expected <= names


def test_representative_risk_golden_cases() -> None:
    nodes = {node["name"]: node for node in catalog()["nodes"]}

    assert nodes["agentAgentflow"]["risk"] == {
        "external_call": "yes",
        "may_cost": "yes",
        "may_write": "review-required",
        "rationale": "Agent 会调用所选模型，模型可能计费；是否经工具写入取决于运行配置",
    }
    assert nodes["llmAgentflow"]["risk"]["external_call"] == "yes"
    assert nodes["llmAgentflow"]["risk"]["may_cost"] == "yes"
    assert nodes["conditionAgentflow"]["risk"]["external_call"] == "no"
    assert nodes["directReplyAgentflow"]["risk"]["external_call"] == "no"
    assert nodes["stickyNoteAgentflow"]["risk"] == {
        "external_call": "no",
        "may_cost": "no",
        "may_write": "no",
        "rationale": "Agentflow Sticky Note 是画布注释，节点本身不执行外部调用或写入",
    }
    assert nodes["postApiChain"]["risk"]["external_call"] == "yes"
    assert nodes["postApiChain"]["risk"]["may_write"] == "yes"
    assert nodes["upstashRedisCache"]["risk"] == {
        "external_call": "yes",
        "may_cost": "review-required",
        "may_write": "yes",
        "rationale": "Upstash Redis Cache 连接托管 Redis 并写入缓存；费用取决于 Upstash 套餐",
    }


def test_generated_markdown_exposes_evidence_docs_outputs_and_risk_semantics() -> None:
    catalog_root = ROOT / "docs" / "19-reference" / "node-catalog"
    index = (catalog_root / "index.md").read_text(encoding="utf-8")
    pages = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(catalog_root.glob("*.md"))
    )

    assert "  - CLM-014" in index
    assert "  - SRC-001" not in pages
    assert "风险值 `yes`" in index
    assert "官方文档：[分类级官方文档]" in pages
    assert "源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准" in pages
