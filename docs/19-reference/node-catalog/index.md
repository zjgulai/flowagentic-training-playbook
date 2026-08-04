---
title: "全量节点参数目录"
audience:
  - builder
  - developer
difficulty: intermediate
duration: 10 分钟
release_version: 3.1.3
release_sha: 96f6ae464f7f4757883a5ba6bec26ca951b4da4d
feature_status: production-enabled
permissions: []
cost_class: none
side_effects: []
last_verified: "2026-08-04"
evidence_ids:
  - CLM-014
screenshot_ids: []
---

# 全量节点参数目录

本目录绑定提交 `96f6ae464f7f4757883a5ba6bec26ca951b4da4d`，收录 311 个实现 `INode` 接口的节点类。
它是固定提交的静态参数索引，不等于某一运行实例已经启用或配置了全部节点。

## 分类

- [Agent Flows（15）](01-agent--flows.md)
- [Agents（9）](02-agents.md)
- [Analytic（7）](03-analytic.md)
- [Cache（6）](04-cache.md)
- [Chains（13）](05-chains.md)
- [Chat Models（37）](06-chat--models.md)
- [Document Loaders（41）](07-document--loaders.md)
- [Embeddings（18）](08-embeddings.md)
- [Engine（4）](09-engine.md)
- [Graph（1）](10-graph.md)
- [LLMs（12）](11-llms.md)
- [Memory（15）](12-memory.md)
- [Moderation（2）](13-moderation.md)
- [Multi Agents（2）](14-multi--agents.md)
- [Prompts（4）](15-prompts.md)
- [Record Manager（3）](16-record--manager.md)
- [Response Synthesizer（4）](17-response--synthesizer.md)
- [Retrievers（15）](18-retrievers.md)
- [Sequential Agents（11）](19-sequential--agents.md)
- [SpeechToText（1）](20-speechtotext.md)
- [Text Splitters（6）](21-text--splitters.md)
- [Tools（39）](22-tools.md)
- [Tools (MCP)（11）](23-tools--mcp.md)
- [Utilities（5）](24-utilities.md)
- [Vector Stores（26）](25-vector--stores.md)
- [outputparsers（4）](26-outputparsers.md)

## 使用边界

- `production-enabled` 表示代码路径属于生产组件包，不代表外部 Provider 或凭据已经可用。
- 风险值 `yes` 表示静态证据确认存在可能性，`no` 表示该节点本身无对应行为，`review-required` 表示静态信息不足，执行前必须按实际配置复核。
- 动态生成的参数、模型列表和凭据条件必须在同版本隔离环境复核。
- 正式截图仅覆盖 13 个 Agentflow V2 节点和高频节点；其余节点以本参数目录完整覆盖。
