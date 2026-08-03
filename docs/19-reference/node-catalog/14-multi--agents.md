---
title: "节点目录：Multi Agents"
audience:
  - builder
  - developer
difficulty: intermediate
duration: 10 分钟
release_version: 3.1.3
release_sha: 6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64
feature_status: production-enabled
permissions: []
cost_class: none
side_effects: []
last_verified: "2026-08-04"
evidence_ids:
  - CLM-014
screenshot_ids: []
---

# 节点目录：Multi Agents

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 2 个节点。动态参数需以对应版本界面为准。

## Supervisor

源码未提供静态描述；请结合节点标签、参数和官方文档判断用途。

- 内部名称：`supervisor`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/multiagents/Supervisor/Supervisor.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `supervisorName` | Supervisor Name | `string` | 是 |
| `supervisorPrompt` | Supervisor Prompt | `string` | 是 |
| `model` | Tool Calling Chat Model | `BaseChatModel` | 是 |
| `agentMemory` | Agent Memory | `BaseCheckpointSaver` | 否 |
| `summarization` | Summarization | `boolean` | 否 |
| `recursionLimit` | Recursion Limit | `number` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Supervisor”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Worker

源码未提供静态描述；请结合节点标签、参数和官方文档判断用途。

- 内部名称：`worker`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/multiagents/Worker/Worker.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `workerName` | Worker Name | `string` | 是 |
| `workerPrompt` | Worker Prompt | `string` | 是 |
| `tools` | Tools | `Tool` | 否 |
| `supervisor` | Supervisor | `Supervisor` | 是 |
| `model` | Tool Calling Chat Model | `BaseChatModel` | 否 |
| `promptValues` | Format Prompt Values | `json` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Worker”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
