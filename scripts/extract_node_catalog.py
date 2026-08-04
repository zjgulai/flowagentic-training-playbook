#!/usr/bin/env python3
"""Generate a public-safe, searchable FlowAgentic node catalog from one Git commit.

The extractor never checks out or modifies the source repository. It reads Git
objects with ``git ls-tree`` and ``git show`` so a dirty source worktree cannot
silently change the documentation baseline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_REF = "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
NODES_ROOT = "packages/components/nodes"
PARSER_VERSION = "static-ts-metadata-v2"

LITERAL_RE_TEMPLATE = r"this\.{field}\s*=\s*(['\"`])(?P<value>.*?)\1"
NUMBER_RE_TEMPLATE = r"this\.{field}\s*=\s*(?P<value>[0-9]+(?:\.[0-9]+)?)"

DOCS_BY_CATEGORY = {
    "Agentflow": "https://docs.flowiseai.com/using-flowise/agentflowv2",
    "Agent Flows": "https://docs.flowiseai.com/using-flowise/agentflowv2",
    "Agents": "https://docs.flowiseai.com/integrations/langchain/agents",
    "Cache": "https://docs.flowiseai.com/integrations/langchain/cache",
    "Chains": "https://docs.flowiseai.com/integrations/langchain/chains",
    "Chat Models": "https://docs.flowiseai.com/integrations/langchain/chat-models",
    "Document Loaders": "https://docs.flowiseai.com/integrations/langchain/document-loaders",
    "Embeddings": "https://docs.flowiseai.com/integrations/langchain/embeddings",
    "LLMs": "https://docs.flowiseai.com/integrations/langchain/llms",
    "Memory": "https://docs.flowiseai.com/integrations/langchain/memory",
    "Output Parsers": "https://docs.flowiseai.com/integrations/langchain/output-parsers",
    "outputparsers": "https://docs.flowiseai.com/integrations/langchain/output-parsers",
    "Prompts": "https://docs.flowiseai.com/integrations/langchain/prompts",
    "Record Manager": "https://docs.flowiseai.com/using-flowise/document-stores",
    "Retrievers": "https://docs.flowiseai.com/integrations/langchain/retrievers",
    "Sequential Agents": "https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents",
    "Text Splitters": "https://docs.flowiseai.com/integrations/langchain/text-splitters",
    "Tools": "https://docs.flowiseai.com/integrations/langchain/tools",
    "Tools (MCP)": "https://docs.flowiseai.com/integrations/langchain/tools",
    "Vector Stores": "https://docs.flowiseai.com/integrations/langchain/vector-stores",
}

EXTERNAL_CATEGORY_WORDS = {
    "analytics",
    "chat model",
    "embedding",
    "mcp",
    "memory",
    "retriever",
    "tool",
    "vector",
}
COST_WORDS = {
    "anthropic",
    "azure",
    "bedrock",
    "chat model",
    "cohere",
    "deepseek",
    "embedding",
    "gemini",
    "google",
    "groq",
    "huggingface",
    "kimi",
    "mistral",
    "model",
    "ollama",
    "openai",
    "replicate",
    "together",
    "vertex",
}
WRITE_WORDS = {
    "create",
    "delete",
    "document store",
    "http",
    "mcp",
    "memory",
    "record manager",
    "tool",
    "update",
    "upsert",
    "vector store",
    "webhook",
}

RISK_YES = "yes"
RISK_NO = "no"
RISK_REVIEW = "review-required"
RISK_VALUES = {RISK_YES, RISK_NO, RISK_REVIEW}

# Exact overrides are intentionally small and source-path based. They document
# cases where a category-level heuristic is either unsafe (for example, a
# Condition node inside Agent Flows) or known to miss an indirect dependency
# (for example, POST API Chain delegates network I/O to APIChain).
RISK_OVERRIDES: dict[str, tuple[str, str, str, str]] = {
    "packages/components/nodes/agentflow/Agent/Agent.ts": (
        RISK_YES,
        RISK_YES,
        RISK_REVIEW,
        "Agent 会调用所选模型，模型可能计费；是否经工具写入取决于运行配置",
    ),
    "packages/components/nodes/agentflow/LLM/LLM.ts": (
        RISK_YES,
        RISK_YES,
        RISK_NO,
        "LLM 会调用所选模型且模型可能计费；节点本身未声明持久化写入",
    ),
    "packages/components/nodes/agentflow/ConditionAgent/ConditionAgent.ts": (
        RISK_YES,
        RISK_YES,
        RISK_NO,
        "Condition Agent 会调用所选聊天模型且模型可能计费",
    ),
    "packages/components/nodes/agentflow/Condition/Condition.ts": (
        RISK_NO,
        RISK_NO,
        RISK_NO,
        "Condition 只在进程内判断已配置条件，节点本身不调用外部服务或写入",
    ),
    "packages/components/nodes/agentflow/DirectReply/DirectReply.ts": (
        RISK_NO,
        RISK_NO,
        RISK_NO,
        "Direct Reply 只形成直接回复，节点本身不调用外部服务或写入",
    ),
    "packages/components/nodes/agentflow/StickyNote/StickyNote.ts": (
        RISK_NO,
        RISK_NO,
        RISK_NO,
        "Agentflow Sticky Note 是画布注释，节点本身不执行外部调用或写入",
    ),
    "packages/components/nodes/sequentialagents/Condition/Condition.ts": (
        RISK_NO,
        RISK_NO,
        RISK_NO,
        "Sequential Agent Condition 只进行条件分支，节点本身不调用外部服务或写入",
    ),
    "packages/components/nodes/utilities/StickyNote/StickyNote.ts": (
        RISK_NO,
        RISK_NO,
        RISK_NO,
        "Sticky Note 是画布注释，节点本身不执行外部调用或写入",
    ),
    "packages/components/nodes/chains/ApiChain/POSTApiChain.ts": (
        RISK_YES,
        RISK_YES,
        RISK_YES,
        "POST API Chain 调用所选模型并向配置的 API 发起 POST；两者可能产生费用或外部副作用",
    ),
    "packages/components/nodes/cache/UpstashRedisCache/UpstashRedisCache.ts": (
        RISK_YES,
        RISK_REVIEW,
        RISK_YES,
        "Upstash Redis Cache 连接托管 Redis 并写入缓存；费用取决于 Upstash 套餐",
    ),
    "packages/components/nodes/memory/UpstashRedisBackedChatMemory/UpstashRedisBackedChatMemory.ts": (
        RISK_YES,
        RISK_REVIEW,
        RISK_YES,
        "Upstash Chat Memory 连接托管 Redis 并写入会话；费用取决于 Upstash 套餐",
    ),
    "packages/components/nodes/vectorstores/Upstash/Upstash.ts": (
        RISK_YES,
        RISK_REVIEW,
        RISK_YES,
        "Upstash Vector 连接托管向量服务并可能写入数据；费用取决于 Upstash 套餐",
    ),
}

PURE_CATEGORIES = {
    "Output Parsers",
    "outputparsers",
    "Prompts",
    "Text Splitters",
}

NETWORK_SOURCE_RE = re.compile(
    r"\b(fetch|axios|request|client|api[_-]?key|base[_-]?url|endpoint|"
    r"connection[_-]?(?:url|token)|https?://|redis|websocket)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class GitReader:
    repo: Path
    ref: str

    def run(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout

    def verify(self) -> str:
        resolved = self.run("rev-parse", f"{self.ref}^{{commit}}").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", resolved):
            raise RuntimeError(f"Cannot resolve an immutable commit: {self.ref}")
        return resolved

    def list_node_files(self) -> list[str]:
        files = self.run("ls-tree", "-r", "--name-only", self.ref, NODES_ROOT)
        return [
            line
            for line in files.splitlines()
            if line.endswith((".ts", ".js")) and not line.endswith((".test.ts", ".test.js"))
        ]

    def read(self, path: str) -> str:
        return self.run("show", f"{self.ref}:{path}")


def literal(source: str, field: str, fallback: str = "") -> str:
    pattern = LITERAL_RE_TEMPLATE.format(field=re.escape(field))
    match = re.search(pattern, source, re.DOTALL)
    if not match:
        return fallback
    return " ".join(match.group("value").replace("\\'", "'").split())


def number(source: str, field: str) -> float | int | None:
    pattern = NUMBER_RE_TEMPLATE.format(field=re.escape(field))
    match = re.search(pattern, source)
    if not match:
        return None
    value = float(match.group("value"))
    return int(value) if value.is_integer() else value


def balanced_segment(source: str, marker: str, opening: str, closing: str) -> str | None:
    start = source.find(marker)
    if start < 0:
        return None
    start = source.find(opening, start + len(marker))
    if start < 0:
        return None
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"`":
            quote = char
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    return None


def top_level_objects(array_source: str | None) -> list[str]:
    if not array_source:
        return []
    objects: list[str] = []
    depth = 0
    start: int | None = None
    quote: str | None = None
    escaped = False
    for index, char in enumerate(array_source):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"`":
            quote = char
        elif char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(array_source[start : index + 1])
                start = None
    return objects


def object_literal(source: str, field: str, fallback: str = "") -> str:
    match = re.search(
        rf"(?:^|[,{{\s]){re.escape(field)}\s*:\s*(['\"`])(?P<value>.*?)\1",
        source,
        re.DOTALL,
    )
    return " ".join(match.group("value").split()) if match else fallback


def parse_params(source: str, field: str) -> tuple[list[dict[str, Any]], bool]:
    segment = balanced_segment(source, f"this.{field}", "[", "]")
    if not segment:
        return [], f"this.{field}" in source
    params: list[dict[str, Any]] = []
    for item in top_level_objects(segment):
        name = object_literal(item, "name")
        label = object_literal(item, "label")
        param_type = object_literal(item, "type")
        if not name and not label:
            continue
        params.append(
            {
                "name": name or label,
                "label": label or name,
                "type": param_type or "dynamic",
                "optional": bool(re.search(r"\boptional\s*:\s*true\b", item)),
            }
        )
    has_dynamic_parts = "..." in segment or "${" in segment
    return params, has_dynamic_parts


def credential_names(source: str) -> list[str]:
    names: set[str] = set()
    for match in re.finditer(r"credentialNames\s*:\s*\[(?P<body>.*?)\]", source, re.DOTALL):
        names.update(re.findall(r"['\"]([^'\"]+)['\"]", match.group("body")))
    return sorted(names)


def slug(path: str) -> str:
    relative = path.removeprefix(f"{NODES_ROOT}/").rsplit(".", 1)[0]
    value = re.sub(r"[^a-z0-9._-]+", "--", relative.lower())
    return value.strip("-")


def infer_risk(label: str, category: str, path: str, source: str) -> dict[str, Any]:
    if path in RISK_OVERRIDES:
        external, may_cost, may_write, rationale = RISK_OVERRIDES[path]
        return {
            "external_call": external,
            "may_cost": may_cost,
            "may_write": may_write,
            "rationale": rationale,
        }

    haystack = " ".join([label, category, path]).lower()
    is_pure_category = category in PURE_CATEGORIES
    has_external_signal = any(word in haystack for word in EXTERNAL_CATEGORY_WORDS) or bool(
        NETWORK_SOURCE_RE.search(source)
    )
    external = RISK_NO if is_pure_category else (RISK_YES if has_external_signal else RISK_REVIEW)

    has_cost_signal = any(word in haystack for word in COST_WORDS)
    if external == RISK_NO:
        may_cost = RISK_NO
    elif has_cost_signal:
        may_cost = RISK_YES
    else:
        may_cost = RISK_REVIEW

    has_write_signal = any(word in haystack for word in WRITE_WORDS)
    if is_pure_category:
        may_write = RISK_NO
    elif has_write_signal:
        may_write = RISK_YES
    else:
        may_write = RISK_REVIEW

    labels = {
        RISK_YES: "是",
        RISK_NO: "否",
        RISK_REVIEW: "需按实际配置复核",
    }
    reasons = [
        f"外部调用：{labels[external]}",
        f"可能计费：{labels[may_cost]}",
        f"可能写入：{labels[may_write]}",
    ]
    return {
        "external_call": external,
        "may_cost": may_cost,
        "may_write": may_write,
        "rationale": "；".join(reasons),
    }


def infer_status(path: str, source: str) -> str:
    lowered = f"{path}\n{source}".lower()
    if re.search(r"\bdeprecated\s*:\s*true\b", lowered):
        return "deprecated"
    if "openaiassistant" in lowered:
        return "deprecated"
    return "production-enabled"


def common_errors(inputs: list[dict[str, Any]], credentials: list[str], risk: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if any(not item["optional"] for item in inputs):
        errors.append("必填输入为空或类型与上游节点输出不匹配")
    if credentials:
        errors.append("凭据未绑定、已失效或当前工作空间无权读取")
    if risk["external_call"] != RISK_NO:
        errors.append("外部服务超时、限流、网络策略或接口版本不兼容")
    if risk["may_write"] != RISK_NO:
        errors.append("重复执行造成非幂等写入，或目标资源权限不足")
    return errors or ["节点版本或连线类型与当前画布不兼容"]


def parse_node(path: str, source: str, release_sha: str) -> dict[str, Any] | None:
    if "implements INode" not in source:
        return None
    warnings: list[str] = []
    label = literal(source, "label", Path(path).stem)
    name = literal(source, "name", Path(path).stem)
    category = literal(source, "category", path.split("/")[-3].replace("_", " "))
    description = literal(source, "description")
    inputs, dynamic_inputs = parse_params(source, "inputs")
    outputs, dynamic_outputs = parse_params(source, "outputs")
    if dynamic_inputs:
        warnings.append("输入包含动态表达式，目录仅列出可静态解析参数")
    if dynamic_outputs:
        warnings.append("输出包含动态表达式，目录仅列出可静态解析参数")
    if not outputs:
        warnings.append("源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准")
    if not literal(source, "name"):
        warnings.append("节点名称由动态表达式或非标准语法定义")
    credentials = credential_names(source)
    risk = infer_risk(label, category, path, source)
    status = infer_status(path, source)
    return {
        "id": slug(path),
        "name": name,
        "label": label,
        "category": category,
        "version": number(source, "version"),
        "description": description,
        "inputs": inputs,
        "outputs": outputs,
        "credential_names": credentials,
        "risk": risk,
        "production_status": status,
        "source_anchor": f"{path}@{release_sha}",
        "official_docs": DOCS_BY_CATEGORY.get(category),
        "example": f"在隔离培训画布中添加“{label}”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。",
        "common_errors": common_errors(inputs, credentials, risk),
        "extraction": {
            "release_sha": release_sha,
            "parser": PARSER_VERSION,
            "warnings": warnings,
        },
    }


def yaml_frontmatter(title: str, release_sha: str) -> str:
    return "\n".join(
        [
            "---",
            f'title: "{title}"',
            "audience:",
            "  - builder",
            "  - developer",
            "difficulty: intermediate",
            "duration: 10 分钟",
            "release_version: 3.1.3",
            f"release_sha: {release_sha}",
            "feature_status: production-enabled",
            "permissions: []",
            "cost_class: none",
            "side_effects: []",
            'last_verified: "2026-08-04"',
            "evidence_ids:",
            "  - CLM-014",
            "screenshot_ids: []",
            "---",
            "",
        ]
    )


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def write_markdown(catalog: list[dict[str, Any]], docs_root: Path, release_sha: str) -> None:
    docs_root.mkdir(parents=True, exist_ok=True)
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in catalog:
        by_category[node["category"]].append(node)

    links: list[str] = []
    for index, (category, nodes) in enumerate(sorted(by_category.items()), start=1):
        filename = f"{index:02d}-{slug(category)}.md"
        links.append(f"- [{category}（{len(nodes)}）]({filename})")
        lines = [
            yaml_frontmatter(f"节点目录：{category}", release_sha),
            f"# 节点目录：{category}",
            "",
            f"本页由 `{PARSER_VERSION}` 从固定提交只读生成，共 {len(nodes)} 个节点。动态参数需以对应版本界面为准。",
            "",
        ]
        for node in sorted(nodes, key=lambda item: (item["label"].lower(), item["id"])):
            lines.extend(
                [
                    f"## {node['label']}",
                    "",
                    node["description"] or "源码未提供静态描述；请结合节点标签、参数和官方文档判断用途。",
                    "",
                    f"- 内部名称：`{node['name']}`",
                    f"- 版本：`{node['version'] if node['version'] is not None else '动态'}`",
                    f"- 功能状态：`{node['production_status']}`",
                    f"- 源码锚点：`{node['source_anchor']}`",
                    (
                        f"- 官方文档：[分类级官方文档]({node['official_docs']})"
                        if node["official_docs"]
                        else "- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准"
                    ),
                    f"- 风险：{node['risk']['rationale']}",
                    f"  - 外部调用：`{node['risk']['external_call']}`",
                    f"  - 可能计费：`{node['risk']['may_cost']}`",
                    f"  - 可能写入：`{node['risk']['may_write']}`",
                    f"- 凭据：{', '.join(f'`{item}`' for item in node['credential_names']) or '无静态凭据声明'}",
                    "",
                    "| 参数 | 界面标签 | 类型 | 必填 |",
                    "|---|---|---|---|",
                ]
            )
            if node["inputs"]:
                for param in node["inputs"]:
                    lines.append(
                        f"| `{md_escape(param['name'])}` | {md_escape(param['label'])} | "
                        f"`{md_escape(param['type'])}` | {'否' if param['optional'] else '是'} |"
                    )
            else:
                lines.append("| — | 未静态解析到参数 | — | — |")
            lines.extend(
                [
                    "",
                    "**静态输出声明：**",
                    "",
                    "| 输出 | 界面标签 | 类型 |",
                    "|---|---|---|",
                ]
            )
            if node["outputs"]:
                for output in node["outputs"]:
                    lines.append(
                        f"| `{md_escape(output['name'])}` | {md_escape(output['label'])} | "
                        f"`{md_escape(output['type'])}` |"
                    )
            else:
                lines.append("| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |")
            lines.extend(
                [
                    "",
                    f"**隔离环境示例：** {node['example']}",
                    "",
                    "**常见错误：**",
                    "",
                    *[f"- {error}" for error in node["common_errors"]],
                    "",
                ]
            )
            if node["extraction"]["warnings"]:
                lines.extend(
                    [
                        '!!! warning "静态解析限制"',
                        "    " + "；".join(node["extraction"]["warnings"]),
                        "",
                    ]
                )
        (docs_root / filename).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    index_lines = [
        yaml_frontmatter("全量节点参数目录", release_sha),
        "# 全量节点参数目录",
        "",
        f"本目录绑定提交 `{release_sha}`，收录 {len(catalog)} 个实现 `INode` 接口的节点类。",
        "它是固定提交的静态参数索引，不等于某一运行实例已经启用或配置了全部节点。",
        "",
        "## 分类",
        "",
        *links,
        "",
        "## 使用边界",
        "",
        "- `production-enabled` 表示代码路径属于生产组件包，不代表外部 Provider 或凭据已经可用。",
        "- 风险值 `yes` 表示静态证据确认存在可能性，`no` 表示该节点本身无对应行为，`review-required` 表示静态信息不足，执行前必须按实际配置复核。",
        "- 动态生成的参数、模型列表和凭据条件必须在同版本隔离环境复核。",
        "- 正式截图仅覆盖 13 个 Agentflow V2 节点和高频节点；其余节点以本参数目录完整覆盖。",
    ]
    (docs_root / "index.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--output", type=Path, default=Path("data/catalog/nodes.json"))
    parser.add_argument(
        "--docs-output",
        type=Path,
        default=Path("docs/19-reference/node-catalog"),
    )
    args = parser.parse_args()

    reader = GitReader(args.source_repo.resolve(), args.ref)
    release_sha = reader.verify()
    catalog: list[dict[str, Any]] = []
    for path in reader.list_node_files():
        source = reader.read(path)
        node = parse_node(path, source, release_sha)
        if node:
            catalog.append(node)
    catalog.sort(key=lambda item: item["id"])
    ids = [node["id"] for node in catalog]
    if len(ids) != len(set(ids)):
        duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
        raise RuntimeError(f"Duplicate node ids: {duplicates}")
    if not 290 <= len(catalog) <= 340:
        raise RuntimeError(f"Unexpected node count {len(catalog)}; inspect parser or source drift")

    payload = {
        "schema_version": 1,
        "release_sha": release_sha,
        "source_tree": reader.run("show", "-s", "--format=%T", release_sha).strip(),
        "parser": PARSER_VERSION,
        "catalog_sha256": "",
        "count": len(catalog),
        "nodes": catalog,
    }
    canonical_nodes = json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()
    payload["catalog_sha256"] = hashlib.sha256(canonical_nodes).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(catalog, args.docs_output, release_sha)

    categories = Counter(node["category"] for node in catalog)
    print(
        json.dumps(
            {
                "release_sha": release_sha,
                "node_count": len(catalog),
                "category_count": len(categories),
                "catalog_sha256": payload["catalog_sha256"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
