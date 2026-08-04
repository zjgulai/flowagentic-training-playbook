---
title: "节点目录：Sequential Agents"
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

# 节点目录：Sequential Agents

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 11 个节点。动态参数需以对应版本界面为准。

## Agent

Agent that can execute tools

- 内部名称：`seqAgent`
- 版本：`4.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/Agent/Agent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `agentName` | Agent Name | `string` | 是 |
| `systemMessagePrompt` | System Prompt | `string` | 否 |
| `messageHistory` | Prepend Messages History | `code` | 否 |
| `conversationHistorySelection` | Conversation History | `options` | 否 |
| `humanMessagePrompt` | Human Prompt | `string` | 否 |
| `tools` | Tools | `Tool` | 否 |
| `sequentialNode` | Sequential Node | `Start \| Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `model` | Chat Model | `BaseChatModel` | 否 |
| `interrupt` | Require Approval | `boolean` | 否 |
| `promptValues` | Format Prompt Values | `json` | 否 |
| `approvalPrompt` | Approval Prompt | `string` | 否 |
| `approveButtonText` | Approve Button Text | `string` | 否 |
| `rejectButtonText` | Reject Button Text | `string` | 否 |
| `updateStateMemory` | Update State | `tabs` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输入包含动态表达式，目录仅列出可静态解析参数；源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Condition

Conditional function to determine which route to take next

- 内部名称：`seqCondition`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/Condition/Condition.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：Sequential Agent Condition 只进行条件分支，节点本身不调用外部服务或写入
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `conditionName` | Condition Name | `string` | 否 |
| `sequentialNode` | Sequential Node | `Start \| Agent \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `condition` | Condition | `conditionFunction` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `next` | Next | `dynamic` |
| `end` | End | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Condition”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

## Condition Agent

Uses an agent to determine which route to take next

- 内部名称：`seqConditionAgent`
- 版本：`3.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/ConditionAgent/ConditionAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `conditionAgentName` | Name | `string` | 是 |
| `sequentialNode` | Sequential Node | `Start \| Agent \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `model` | Chat Model | `BaseChatModel` | 否 |
| `systemMessagePrompt` | System Prompt | `string` | 否 |
| `conversationHistorySelection` | Conversation History | `options` | 否 |
| `humanMessagePrompt` | Human Prompt | `string` | 否 |
| `promptValues` | Format Prompt Values | `json` | 否 |
| `conditionAgentStructuredOutput` | JSON Structured Output | `datagrid` | 否 |
| `condition` | Condition | `conditionFunction` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `next` | Next | `dynamic` |
| `end` | End | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Condition Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Custom JS Function

Execute custom javascript function

- 内部名称：`seqCustomFunction`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/CustomFunction/CustomFunction.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `functionInputVariables` | Input Variables | `json` | 否 |
| `sequentialNode` | Sequential Node | `Start \| Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `functionName` | Function Name | `string` | 是 |
| `javascriptFunction` | Javascript Function | `code` | 是 |
| `returnValueAs` | Return Value As | `options` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Custom JS Function”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## End

End conversation

- 内部名称：`seqEnd`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/End/End.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sequentialNode` | Sequential Node | `Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“End”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Execute Flow

Execute chatflow/agentflow and return final response

- 内部名称：`seqExecuteFlow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/ExecuteFlow/ExecuteFlow.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`chatflowApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sequentialNode` | Sequential Node | `Start \| Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `seqExecuteFlowName` | Name | `string` | 是 |
| `selectedFlow` | Select Flow | `asyncOptions` | 是 |
| `seqExecuteFlowInput` | Input | `options` | 是 |
| `overrideConfig` | Override Config | `json` | 否 |
| `baseURL` | Base URL | `string` | 否 |
| `startNewSession` | Start new session per message | `boolean` | 否 |
| `returnValueAs` | Return Value As | `options` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Execute Flow”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LLM Node

Run Chat Model and return the output

- 内部名称：`seqLLMNode`
- 版本：`4.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/LLMNode/LLMNode.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `llmNodeName` | Name | `string` | 是 |
| `systemMessagePrompt` | System Prompt | `string` | 否 |
| `messageHistory` | Prepend Messages History | `code` | 否 |
| `conversationHistorySelection` | Conversation History | `options` | 否 |
| `humanMessagePrompt` | Human Prompt | `string` | 否 |
| `sequentialNode` | Sequential Node | `Start \| Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `model` | Chat Model | `BaseChatModel` | 否 |
| `promptValues` | Format Prompt Values | `json` | 否 |
| `llmStructuredOutput` | JSON Structured Output | `datagrid` | 否 |
| `updateStateMemory` | Update State | `tabs` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LLM Node”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输入包含动态表达式，目录仅列出可静态解析参数；源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Loop

Loop back to the specific sequential node

- 内部名称：`seqLoop`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/Loop/Loop.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sequentialNode` | Sequential Node | `Agent \| Condition \| LLMNode \| ToolNode \| CustomFunction \| ExecuteFlow` | 是 |
| `loopToName` | Loop To | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Loop”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Start

Starting point of the conversation

- 内部名称：`seqStart`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/Start/Start.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `agentMemory` | Agent Memory | `BaseCheckpointSaver` | 否 |
| `state` | State | `State` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Start”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## State

A centralized state object, updated by nodes in the graph, passing from one node to another

- 内部名称：`seqState`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/State/State.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `stateMemory` | Custom State | `tabs` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“State”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Tool Node

Execute tool and return tool's output

- 内部名称：`seqToolNode`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/sequentialagents/ToolNode/ToolNode.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv1/sequential-agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool` | 否 |
| `llmNode` | LLM Node | `LLMNode` | 是 |
| `toolNodeName` | Name | `string` | 是 |
| `interrupt` | Require Approval | `boolean` | 否 |
| `approvalPrompt` | Approval Prompt | `string` | 否 |
| `approveButtonText` | Approve Button Text | `string` | 否 |
| `rejectButtonText` | Reject Button Text | `string` | 否 |
| `updateStateMemory` | Update State | `tabs` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Tool Node”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输入包含动态表达式，目录仅列出可静态解析参数；源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
