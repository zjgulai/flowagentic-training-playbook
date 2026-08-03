#!/usr/bin/env python3
"""Generate the deterministic 252-shot capture plan.

This is a plan, not capture evidence. The release manifest remains empty until
each image is captured, hashed, redacted, and bound to the Chinese release SHA.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "manifests" / "screenshot-plan.yml"
PLAN: list[dict[str, Any]] = []

# Each capture is bound to the public page that must consume the evidence.  A
# release manifest may not silently move a screenshot to a different SOP/page.
SOP_DOC_PATHS = {
    "login-navigation": "docs/02-account/index.md",
    "credentials": "docs/03-credentials/credentials.md",
    "variables": "docs/03-credentials/variables.md",
    "api-keys": "docs/03-credentials/api-keys.md",
    "chatflow": "docs/04-chatflow/index.md",
    "agentflow-v2": "docs/05-agentflow-v2/index.md",
    "agentflow-v2-nodes": "docs/05-agentflow-v2/index.md",
    "executions": "docs/06-executions/index.md",
    "assistants": "docs/07-assistant/index.md",
    "marketplace": "docs/08-marketplace/index.md",
    "tools": "docs/09-tools-mcp/index.md",
    "mcp": "docs/09-tools-mcp/index.md",
    "document-store": "docs/10-rag/index.md",
    "api-embed-sdk": "docs/11-api-sdk/index.md",
    "enterprise-ticket-lab": "docs/12-lab/index.md",
    "troubleshooting": "docs/14-troubleshooting/index.md",
    "restricted-features": "docs/17-restricted/index.md",
}


def add_series(
    prefix: str,
    sop_id: str,
    route: str,
    labels: list[str],
    *,
    role: str = "builder",
    state: str = "success",
    provider: str = "none",
    feature_status: str = "production-enabled",
    states: list[str] | None = None,
    routes: list[str] | None = None,
    providers: list[str] | None = None,
    feature_statuses: list[str] | None = None,
    risk_case: str | None = None,
    doc_path: str | None = None,
) -> None:
    target_doc = doc_path or SOP_DOC_PATHS.get(sop_id)
    if target_doc is None:
        raise ValueError(f"{prefix}: no doc_path mapping for SOP {sop_id}")
    for field_name, values in (
        ("states", states),
        ("routes", routes),
        ("providers", providers),
        ("feature_statuses", feature_statuses),
    ):
        if values is not None and len(values) != len(labels):
            raise ValueError(f"{prefix}: {field_name} length must match labels")
    start = sum(1 for item in PLAN if item["id"].startswith(f"{prefix}-")) + 1
    for offset, label in enumerate(labels):
        item = {
            "id": f"{prefix}-{start + offset:03d}",
            "sop_id": sop_id,
            "doc_path": target_doc,
            "step": start + offset,
            "route": routes[offset] if routes is not None else route,
            "planned_state": states[offset] if states is not None else state,
            "role": role,
            "viewport": "1440x1000@100%",
            "locale": "zh-CN",
            "theme": "light",
            "fixture": "synthetic-enterprise-v1",
            "provider": providers[offset] if providers is not None else provider,
            "feature_status": (
                feature_statuses[offset]
                if feature_statuses is not None
                else feature_status
            ),
            "description": label,
            "release_sha": None,
            "capture_status": "blocked-by-G1",
            "required_for_release": True,
        }
        if risk_case is not None:
            item["risk_case"] = risk_case
        PLAN.append(item)


add_series(
    "AUTH",
    "login-navigation",
    "/signin",
    [
        "登录封面初始状态",
        "邮箱字段校验",
        "密码显示与隐藏",
        "虚构账号登录失败",
        "限流提示",
        "忘记密码入口",
        "重置密码边界",
        "登录成功跳转",
        "访问受限页面",
        "退出后的会话失效",
    ],
    role="admin",
    states=[
        "before",
        "during",
        "during",
        "error",
        "rate-limited",
        "during",
        "during",
        "success",
        "permission-denied",
        "recovery",
    ],
)
add_series(
    "NAV",
    "login-navigation",
    "/chatflows",
    ["十项主导航", "折叠侧边栏", "个人菜单", "浅色主题", "深色主题代表图", "无权限菜单差异"],
    role="admin",
    states=["before", "during", "success", "success", "success", "permission-denied"],
)
add_series(
    "CR",
    "credentials",
    "/credentials",
    ["凭据列表", "类型搜索", "新建动态字段"],
    role="admin",
    states=["before", "during", "success"],
)
add_series(
    "CR",
    "credentials",
    "/credentials",
    ["删除前引用检查", "删除确认输入中", "未引用凭据删除成功", "仍被引用时删除失败", "取消删除并完成轮换恢复"],
    role="admin",
    states=["before", "during", "success", "error", "recovery"],
    risk_case="credential-delete-and-rotation",
)
add_series(
    "VAR",
    "variables",
    "/variables",
    ["变量列表"],
    states=["before"],
)
add_series(
    "VAR",
    "variables",
    "/variables",
    ["删除前依赖检查", "删除确认输入中", "未引用变量删除成功", "仍被引用时删除失败", "取消删除并恢复变量值"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="variable-delete",
)
add_series(
    "KEY",
    "api-keys",
    "/apikey",
    ["密钥遮罩列表"],
    role="admin",
    states=["before"],
)
add_series(
    "KEY",
    "api-keys",
    "/apikey",
    ["轮换前关联流程检查", "创建替代密钥并改绑", "旧密钥撤销成功", "仍被使用时删除失败", "恢复关联并确认调用成功"],
    role="admin",
    states=["before", "during", "success", "error", "recovery"],
    risk_case="api-key-rotation",
)
add_series(
    "CF",
    "chatflow",
    "/chatflows",
    [
        "卡片视图",
        "列表视图",
        "搜索结果",
        "排序",
        "空状态",
        "新建流程",
        "空白画布",
        "节点分类",
        "节点搜索",
        "添加模型节点",
        "必填参数",
        "绑定凭据",
        "节点连线",
        "验证失败",
        "保存命名",
        "未保存提醒",
        "聊天测试操作前",
        "聊天流式输出中",
        "聊天测试成功",
        "来源与工具结果",
        "反馈与追问",
        "通用配置",
        "对话配置",
        "媒体与文件配置",
        "高级配置",
    ],
    states=[
        "before", "success", "success", "during", "empty",
        "before", "before", "during", "during", "during",
        "during", "during", "during", "error", "success",
        "during", "before", "during", "success", "success",
        "success", "during", "during", "during", "during",
    ],
    providers=[
        "none", "none", "none", "none", "none",
        "none", "none", "none", "none", "none",
        "none", "DeepSeek", "none", "none", "none",
        "none", "none", "DeepSeek", "DeepSeek", "DeepSeek",
        "DeepSeek", "none", "none", "none", "none",
    ],
)
add_series(
    "CF",
    "chatflow",
    "/chatflows",
    ["公开发布前影响检查", "公开配置进行中", "公开聊天发布成功", "公开发布校验失败", "撤销公开并恢复私有"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="chatflow-publication",
)
add_series(
    "AF",
    "agentflow-v2",
    "/agentflows",
    [
        "V2 列表",
        "V1 弃用提示",
        "新建 V2",
        "自动 Start 节点",
        "节点面板",
        "条件连线",
        "迭代连线",
        "结构化输出",
        "验证失败",
        "测试运行中",
    ],
    states=["before", "during", "before", "success", "during", "during", "during", "success", "error", "during"],
    providers=["none", "none", "none", "none", "none", "none", "none", "none", "none", "DeepSeek"],
)
add_series(
    "AF",
    "agentflow-v2",
    "/agentflows",
    ["定时触发启用前", "定时配置进行中", "定时执行成功", "Webhook 验证失败", "禁用触发并恢复手动运行"],
    states=["before", "during", "success", "error", "recovery"],
    providers=["none", "none", "DeepSeek", "none", "none"],
    risk_case="agentflow-trigger-activation",
)

agentflow_nodes = [
    ("START", "Start"),
    ("AGENT", "Agent"),
    ("LLM", "LLM"),
    ("COND", "Condition"),
    ("ACOND", "Agent Condition"),
    ("REPLY", "Direct Reply"),
    ("FUNC", "Custom Function"),
    ("TOOL", "Tool"),
    ("RETR", "Retriever"),
    ("NOTE", "Sticky Note"),
    ("HTTP", "HTTP"),
    ("ITER", "Iteration"),
    ("EXEC", "Execute Flow"),
]
for short, label in agentflow_nodes:
    add_series(
        f"AFN-{short}",
        "agentflow-v2-nodes",
        "/v2/agentcanvas/:id",
        [f"{label} 添加前", f"{label} 参数配置", f"{label} 运行结果"],
        provider="DeepSeek" if label in {"Agent", "LLM"} else "none",
        states=["before", "during", "success"],
    )

add_series(
    "EX",
    "executions",
    "/executions",
    [
        "执行列表",
        "状态筛选",
        "时间筛选",
        "流程筛选",
        "Session 筛选",
        "执行树",
        "节点输入",
        "节点输出",
        "节点错误",
        "Token 与费用",
    ],
    states=["before", "during", "during", "during", "during", "success", "success", "success", "error", "success"],
)
add_series(
    "EX",
    "executions",
    "/executions",
    ["HITL 停止待处理", "Proceed 确认中", "执行恢复成功", "恢复请求失败", "修正输入后重新恢复"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="hitl-resume",
)
add_series(
    "AS",
    "assistants",
    "/assistants",
    [
        "助手类型入口",
        "Custom Assistant 新建",
        "模型选择",
        "凭据绑定",
        "指令编辑",
        "知识库选择",
        "未 Upsert 警告",
        "工具选择",
        "保存",
        "对话预览",
        "API 配置",
        "助手配置",
        "OpenAI Assistant 弃用提示",
    ],
    states=[
        "before", "before", "during", "during", "during", "during", "error",
        "during", "success", "success", "during", "success", "error",
    ],
    providers=[
        "none", "none", "DeepSeek", "DeepSeek", "none", "none", "none",
        "none", "none", "DeepSeek", "none", "none", "none",
    ],
)
add_series(
    "MP",
    "marketplace",
    "/marketplaces",
    ["社区模板", "我的模板", "搜索过滤"],
    states=["before", "success", "during"],
)
add_series(
    "MP",
    "marketplace",
    "/marketplaces",
    ["使用模板前依赖检查", "替换凭据与变量中", "模板导入成功", "依赖缺失导致导入失败", "补齐依赖后恢复流程"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="marketplace-template-import",
)
add_series(
    "TOOL",
    "tools",
    "/tools",
    [
        "工具标签页",
        "新建基础信息",
        "snake_case 校验",
        "Schema 行模式",
        "Schema JSON 模式",
        "JavaScript 编辑器",
        "可用变量帮助",
    ],
    states=["before", "before", "error", "during", "during", "during", "success"],
)
add_series(
    "TOOL",
    "tools",
    "/tools",
    ["外部调用前副作用检查", "工具调用进行中", "工具调用成功", "超时或返回值错误", "修正超时与幂等键后恢复"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="custom-tool-external-call",
)
add_series(
    "MCP",
    "mcp",
    "/tools",
    [
        "MCP 标签页",
        "新建服务器",
        "SSE transport",
        "Streamable HTTP transport",
        "鉴权 Header 遮罩",
        "Authorize 前",
        "Authorize 中",
        "工具发现成功",
        "工具注解",
        "授权失败恢复",
    ],
    states=["before", "before", "during", "during", "during", "before", "during", "success", "success", "recovery"],
)
add_series(
    "DS",
    "document-store",
    "/document-stores",
    [
        "卡片视图",
        "列表视图",
        "新建文档库",
        "空详情",
        "选择 Loader",
        "上传合成 PDF",
        "来源凭据",
        "Splitter 选择",
        "Splitter 参数",
        "Chunk Preview",
        "Metadata 预览",
        "敏感数据人工检查",
        "处理进行中",
        "处理成功",
        "Chunk 列表",
        "编辑内容",
        "编辑 Metadata",
        "Embedding 选择",
        "Embedding 凭据",
        "Vector Store 选择",
        "Vector Store 参数",
        "Record Manager",
        "Upsert 前",
        "Upsert 中",
        "Upsert 成功",
    ],
    states=[
        "before", "success", "before", "empty", "during",
        "during", "during", "during", "during", "success",
        "success", "during", "during", "success", "success",
        "during", "during", "during", "during", "during",
        "during", "during", "before", "during", "success",
    ],
)
add_series(
    "DS",
    "document-store",
    "/document-stores",
    ["重建向量前影响检查", "重新配置向量维度中", "检索恢复成功", "维度不匹配导致失败", "回退旧索引并恢复检索"],
    states=["before", "during", "success", "error", "recovery"],
    risk_case="document-store-vector-rebuild",
)
add_series(
    "API",
    "api-embed-sdk",
    "/canvas/:id",
    [
        "Prediction API",
        "SSE 示例",
        "Upload 示例",
        "overrideConfig",
        "服务端调用",
        "Web Component",
        "React Embed",
        "CSP 错误",
        "CORS 错误",
        "SDK 实验状态",
    ],
    states=["before", "during", "during", "during", "success", "success", "success", "error", "error", "success"],
)
add_series(
    "LAB",
    "enterprise-ticket-lab",
    "/chatflows",
    [
        "FAQ 初始数据",
        "FAQ Chatflow",
        "RAG 助手",
        "工单分类输入",
        "结构化输出",
        "工单查询 Tool",
        "MCP 工单服务",
        "条件分流",
        "HITL 审批",
        "定时摘要",
        "DeepSeek 成功",
        "Kimi 降级成功",
    ],
    states=["before", "before", "during", "during", "success", "success", "success", "during", "during", "success", "success", "recovery"],
    providers=["none", "none", "none", "none", "DeepSeek", "none", "none", "DeepSeek", "DeepSeek", "DeepSeek", "DeepSeek", "Kimi"],
)
add_series(
    "ERR",
    "troubleshooting",
    "/executions",
    [
        "401",
        "403",
        "429",
        "节点面板为空",
        "凭据解密失败",
        "变量未生效",
        "Provider 超时",
        "Streaming 中断",
        "MCP 发现失败",
        "HITL 恢复失败",
    ],
    role="admin",
    state="error",
    providers=["none", "none", "none", "none", "none", "none", "DeepSeek", "none", "none", "none"],
)
add_series(
    "EXT",
    "restricted-features",
    "/datasets",
    [
        "数据集 feature-gated",
        "CSV 导入",
        "评估器 feature-gated",
        "评估任务 feature-gated",
        "用户 feature-gated",
        "角色 feature-gated",
        "工作空间 feature-gated",
        "SSO feature-gated",
        "登录活动 feature-gated",
        "服务端日志 feature-gated",
        "Agentflow SDK experimental",
        "Observe SDK experimental",
    ],
    role="admin",
    states=["before"] * 12,
    routes=[
        "/datasets",
        "/dataset_rows/:id",
        "/evaluators",
        "/evaluations",
        "/users",
        "/roles",
        "/workspaces",
        "/sso-config",
        "/login-activity",
        "/logs",
        "/agentflows",
        "/executions",
    ],
    providers=["none"] * 12,
    feature_statuses=["feature-gated"] * 10 + ["experimental", "experimental"],
)


def main() -> int:
    if not 180 <= len(PLAN) <= 260:
        raise RuntimeError(f"screenshot plan must contain 180–260 entries, got {len(PLAN)}")
    ids = [item["id"] for item in PLAN]
    if len(ids) != len(set(ids)):
        raise RuntimeError("screenshot plan ids are not unique")
    payload = {
        "schema_version": 3,
        "status": "planned-blocked-by-G1",
        "target_range": "180-260",
        "count": len(PLAN),
        "release_sha": None,
        "generated_from": "scripts/generate_screenshot_plan.py",
        "by_feature_status": dict(Counter(item["feature_status"] for item in PLAN)),
        "shots": PLAN,
    }
    # Import only at execution time so this generator remains a pure data
    # declaration when imported by tests.
    from validate_screenshots import validate_plan

    validation_errors = validate_plan(payload, release=False)
    if validation_errors:
        raise RuntimeError("invalid screenshot plan:\n- " + "\n- ".join(validation_errors))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(f"generated {len(PLAN)} planned screenshots at {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
