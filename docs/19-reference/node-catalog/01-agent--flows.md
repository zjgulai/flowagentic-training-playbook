---
title: "节点目录：Agent Flows"
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

# 节点目录：Agent Flows

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 15 个节点。动态参数需以对应版本界面为准。

## Agent

Dynamically choose and utilize tools during runtime, enabling multi-step reasoning

- 内部名称：`agentAgentflow`
- 版本：`3.2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Agent/Agent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：Agent 会调用所选模型，模型可能计费；是否经工具写入取决于运行配置
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `agentModel` | Model | `asyncOptions` | 是 |
| `agentMessages` | Messages | `array` | 否 |
| `agentToolsBuiltInOpenAI` | OpenAI Built-in Tools | `multiOptions` | 否 |
| `agentToolsBuiltInGemini` | Gemini Built-in Tools | `multiOptions` | 否 |
| `agentToolsBuiltInAnthropic` | Anthropic Built-in Tools | `multiOptions` | 否 |
| `agentTools` | Tools | `array` | 否 |
| `agentKnowledgeDocumentStores` | Knowledge (Document Stores) | `array` | 否 |
| `agentKnowledgeVSEmbeddings` | Knowledge (Vector Embeddings) | `array` | 否 |
| `agentEnableMemory` | Enable Memory | `boolean` | 否 |
| `agentMemoryType` | Memory Type | `options` | 否 |
| `agentMemoryWindowSize` | Window Size | `number` | 是 |
| `agentMemoryMaxTokenLimit` | Max Token Limit | `number` | 是 |
| `agentUserMessage` | Input Message | `string` | 否 |
| `agentReturnResponseAs` | Return Response As | `options` | 是 |
| `agentStructuredOutput` | JSON Structured Output | `array` | 否 |
| `agentUpdateState` | Update Flow State | `array` | 否 |

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
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Condition

Split flows based on If Else conditions

- 内部名称：`conditionAgentflow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Condition/Condition.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：Condition 只在进程内判断已配置条件，节点本身不调用外部服务或写入
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `conditions` | Conditions | `array` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `0` | 0 | `dynamic` |
| `1` | 1 | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Condition”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

## Condition Agent

Utilize an agent to split flows based on dynamic conditions

- 内部名称：`conditionAgentAgentflow`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/ConditionAgent/ConditionAgent.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：Condition Agent 会调用所选聊天模型且模型可能计费
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `conditionAgentModel` | Model | `asyncOptions` | 是 |
| `conditionAgentInstructions` | Instructions | `string` | 是 |
| `conditionAgentInput` | Input | `string` | 是 |
| `conditionAgentScenarios` | Scenarios | `array` | 是 |
| `conditionAgentEnableMemory` | Enable Memory | `boolean` | 否 |
| `conditionAgentMemoryType` | Memory Type | `options` | 否 |
| `conditionAgentMemoryWindowSize` | Window Size | `number` | 是 |
| `conditionAgentMemoryMaxTokenLimit` | Max Token Limit | `number` | 是 |
| `conditionAgentOverrideSystemPrompt` | Override System Prompt | `boolean` | 否 |
| `conditionAgentSystemPrompt` | Condition Agent System Prompt | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `0` | 0 | `dynamic` |
| `1` | 1 | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Condition Agent”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容

## Custom Function

Execute custom function

- 内部名称：`customFunctionAgentflow`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/CustomFunction/CustomFunction.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `customFunctionInputVariables` | Input Variables | `array` | 否 |
| `customFunctionJavascriptFunction` | Javascript Function | `code` | 是 |
| `customFunctionUpdateState` | Update Flow State | `array` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Custom Function”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Direct Reply

Directly reply to the user with a message

- 内部名称：`directReplyAgentflow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/DirectReply/DirectReply.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：Direct Reply 只形成直接回复，节点本身不调用外部服务或写入
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `directReplyMessage` | Message | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Direct Reply”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Execute Flow

Execute another flow

- 内部名称：`executeFlowAgentflow`
- 版本：`1.2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/ExecuteFlow/ExecuteFlow.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`chatflowApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `executeFlowSelectedFlow` | Select Flow | `asyncOptions` | 是 |
| `executeFlowInput` | Input | `string` | 是 |
| `executeFlowOverrideConfig` | Override Config | `json` | 否 |
| `executeFlowBaseURL` | Base URL | `string` | 否 |
| `executeFlowReturnResponseAs` | Return Response As | `options` | 是 |
| `executeFlowUpdateState` | Update Flow State | `array` | 否 |

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

## HTTP

Send a HTTP request

- 内部名称：`httpAgentflow`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/HTTP/HTTP.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`httpApiKey`, `httpBasicAuth`, `httpBearerToken`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `method` | Method | `options` | 是 |
| `url` | URL | `string` | 是 |
| `headers` | Headers | `array` | 否 |
| `queryParams` | Query Params | `array` | 否 |
| `bodyType` | Body Type | `options` | 否 |
| `body` | Body | `string` | 否 |
| `body` | Body | `array` | 否 |
| `responseType` | Response Type | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“HTTP”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Human Input

Request human input, approval or rejection during execution

- 内部名称：`humanInputAgentflow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/HumanInput/HumanInput.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `humanInputDescriptionType` | Description Type | `options` | 是 |
| `humanInputDescription` | Description | `string` | 是 |
| `humanInputModel` | Model | `asyncOptions` | 是 |
| `humanInputModelPrompt` | Prompt | `string` | 是 |
| `humanInputEnableFeedback` | Enable Feedback | `boolean` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `proceed` | Proceed | `dynamic` |
| `reject` | Reject | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Human Input”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Iteration

Execute the nodes within the iteration block through N iterations

- 内部名称：`iterationAgentflow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Iteration/Iteration.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `iterationInput` | Array Input | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Iteration”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LLM

Large language models to analyze user-provided inputs and generate responses

- 内部名称：`llmAgentflow`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/LLM/LLM.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：LLM 会调用所选模型且模型可能计费；节点本身未声明持久化写入
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `llmModel` | Model | `asyncOptions` | 是 |
| `llmMessages` | Messages | `array` | 否 |
| `llmEnableMemory` | Enable Memory | `boolean` | 否 |
| `llmMemoryType` | Memory Type | `options` | 否 |
| `llmMemoryWindowSize` | Window Size | `number` | 是 |
| `llmMemoryMaxTokenLimit` | Max Token Limit | `number` | 是 |
| `llmUserMessage` | Input Message | `string` | 否 |
| `llmReturnResponseAs` | Return Response As | `options` | 是 |
| `llmStructuredOutput` | JSON Structured Output | `array` | 否 |
| `llmUpdateState` | Update Flow State | `array` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LLM”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Loop

Loop back to a previous node

- 内部名称：`loopAgentflow`
- 版本：`1.2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Loop/Loop.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `loopBackToNode` | Loop Back To | `asyncOptions` | 是 |
| `maxLoopCount` | Max Loop Count | `number` | 是 |
| `fallbackMessage` | Fallback Message | `string` | 否 |
| `loopUpdateState` | Update Flow State | `array` | 否 |

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

## Retriever

Retrieve information from vector database

- 内部名称：`retrieverAgentflow`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Retriever/Retriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `retrieverKnowledgeDocumentStores` | Knowledge (Document Stores) | `array` | 是 |
| `retrieverQuery` | Retriever Query | `string` | 是 |
| `outputFormat` | Output Format | `options` | 是 |
| `retrieverUpdateState` | Update Flow State | `array` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Start

Starting point of the agentflow

- 内部名称：`startAgentflow`
- 版本：`1.4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Start/Start.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `startInputType` | Input Type | `options` | 是 |
| `formTitle` | Form Title | `string` | 是 |
| `formDescription` | Form Description | `string` | 是 |
| `formInputTypes` | Form Input Types | `array` | 是 |
| `webhookMethod` | HTTP Method | `options` | 是 |
| `webhookContentType` | Content Type | `options` | 否 |
| `webhookURL` | Webhook URL | `string` | 否 |
| `webhookInputMode` | Input Mode | `options` | 是 |
| `webhookDefaultInput` | Custom Text | `string` | 否 |
| `webhookEnableAuth` | Verify request signature | `boolean` | 否 |
| `webhookSecret` | Webhook Secret | `string` | 否 |
| `webhookSignatureHeader` | Signature Header | `string` | 否 |
| `webhookSignatureType` | Signature Type | `options` | 否 |
| `webhookResponseMode` | Response Mode | `options` | 是 |
| `callbackUrl` | Callback URL | `string` | 否 |
| `callbackSecret` | Callback Secret | `string` | 否 |
| `webhookEnableValidation` | Validate request shape | `boolean` | 否 |
| `webhookQueryParams` | Expected Query Parameters | `array` | 否 |
| `webhookBodyParams` | Expected Body Parameters | `array` | 否 |
| `webhookHeaderParams` | Expected Headers | `array` | 否 |
| `scheduleType` | Schedule Type | `options` | 是 |
| `scheduleCronExpression` | Cron Expression | `string` | 是 |
| `scheduleFrequency` | Frequency | `options` | 是 |
| `scheduleOnMinute` | On Minute | `number` | 是 |
| `scheduleOnTime` | On Time | `timePicker` | 是 |
| `scheduleOnDayOfWeek` | On Day of Week | `weekDaysPicker` | 是 |
| `scheduleOnDayOfMonth` | On Day of Month | `monthDaysPicker` | 是 |
| `scheduleEndDate` | End Date | `datePicker` | 否 |
| `scheduleTimezone` | Timezone | `options` | 否 |
| `scheduleInputMode` | Schedule Input Mode | `options` | 是 |
| `scheduleDefaultInput` | Default Input | `string` | 是 |
| `scheduleFormInputTypes` | Form Fields | `array` | 是 |
| `scheduleFormDefaults` | Default Form Values | `json` | 否 |
| `startEphemeralMemory` | Ephemeral Memory | `boolean` | 否 |
| `startState` | Flow State | `array` | 否 |
| `startPersistState` | Persist State | `boolean` | 否 |

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

## Sticky Note

Add notes to the agent flow

- 内部名称：`stickyNoteAgentflow`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/StickyNote/StickyNote.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：Agentflow Sticky Note 是画布注释，节点本身不执行外部调用或写入
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `note` | note | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Sticky Note”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Tool

Tools allow LLM to interact with external systems

- 内部名称：`toolAgentflow`
- 版本：`1.2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/agentflow/Tool/Tool.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/agentflowv2)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `toolAgentflowSelectedTool` | Tool | `asyncOptions` | 是 |
| `toolInputArgs` | Tool Input Arguments | `array` | 是 |
| `toolUpdateState` | Update Flow State | `array` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
