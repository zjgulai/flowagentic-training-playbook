---
title: "节点目录：Agents"
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

# 节点目录：Agents

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 9 个节点。动态参数需以对应版本界面为准。

## Anthropic Agent

Agent that uses Anthropic Claude Function Calling to pick the tools and args to call using LlamaIndex

- 内部名称：`anthropicAgentLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/LlamaIndexAgents/AnthropicAgent/AnthropicAgent_LlamaIndex.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：需按实际配置复核；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool_LlamaIndex` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `model` | Anthropic Claude Model | `BaseChatModel_LlamaIndex` | 是 |
| `systemMessage` | System Message | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Anthropic Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Conversational Agent

Conversational agent for a chat model. It will utilize chat specific prompts

- 内部名称：`conversationalAgent`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/ConversationalAgent/ConversationalAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Allowed Tools | `Tool` | 是 |
| `model` | Chat Model | `BaseChatModel` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `systemMessage` | System Message | `string` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversational Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Conversational Retrieval Tool Agent

Agent that calls a vector store retrieval and uses Function Calling to pick the tools and args to call

- 内部名称：`conversationalRetrievalToolAgent`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/ConversationalRetrievalToolAgent/ConversationalRetrievalToolAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `model` | Tool Calling Chat Model | `BaseChatModel` | 是 |
| `systemMessage` | System Message | `string` | 否 |
| `rephrasePrompt` | Rephrase Prompt | `string` | 否 |
| `rephraseModel` | Rephrase Model | `BaseChatModel` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |
| `vectorStoreRetriever` | Vector Store Retriever | `BaseRetriever` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversational Retrieval Tool Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Assistant

An agent that uses OpenAI Assistant API to pick the tool and args to call

- 内部名称：`openAIAssistant`
- 版本：`4`
- 功能状态：`deprecated`
- 源码锚点：`packages/components/nodes/agents/OpenAIAssistant/OpenAIAssistant.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedAssistant` | Select Assistant | `asyncOptions` | 是 |
| `tools` | Allowed Tools | `Tool` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `toolChoice` | Tool Choice | `string` | 否 |
| `parallelToolCalls` | Parallel Tool Calls | `boolean` | 否 |
| `disableFileDownload` | Disable File Download | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Assistant”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Tool Agent

Agent that uses OpenAI Function Calling to pick the tools and args to call using LlamaIndex

- 内部名称：`openAIToolAgentLlamaIndex`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/LlamaIndexAgents/OpenAIToolAgent/OpenAIToolAgent_LlamaIndex.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool_LlamaIndex` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `model` | OpenAI/Azure Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `systemMessage` | System Message | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Tool Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ReAct Agent for Chat Models

Agent that uses the ReAct logic to decide what action to take, optimized to be used with Chat Models

- 内部名称：`reactAgentChat`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/ReActAgentChat/ReActAgentChat.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Allowed Tools | `Tool` | 是 |
| `model` | Chat Model | `BaseChatModel` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ReAct Agent for Chat Models”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ReAct Agent for LLMs

Agent that uses the ReAct logic to decide what action to take, optimized to be used with LLMs

- 内部名称：`reactAgentLLM`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/ReActAgentLLM/ReActAgentLLM.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Allowed Tools | `Tool` | 是 |
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ReAct Agent for LLMs”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Tool Agent

Agent that uses Function Calling to pick the tools and args to call

- 内部名称：`toolAgent`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/ToolAgent/ToolAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `model` | Tool Calling Chat Model | `BaseChatModel` | 是 |
| `chatPromptTemplate` | Chat Prompt Template | `ChatPromptTemplate` | 否 |
| `systemMessage` | System Message | `string` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |
| `enableDetailedStreaming` | Enable Detailed Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Tool Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## XML Agent

Agent that is designed for LLMs that are good for reasoning/writing XML (e.g: Anthropic Claude)

- 内部名称：`xmlAgent`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agents/XMLAgent/XMLAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/agents)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tools` | Tools | `Tool` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `model` | Chat Model | `BaseChatModel` | 是 |
| `systemMessage` | System Message | `string` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `maxIterations` | Max Iterations | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“XML Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
