---
title: "节点目录：Chat Models"
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

# 节点目录：Chat Models

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 37 个节点。动态参数需以对应版本界面为准。

## Alibaba Tongyi

Wrapper around Alibaba Tongyi Chat Endpoints

- 内部名称：`chatAlibabaTongyi`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatAlibabaTongyi/ChatAlibabaTongyi.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`AlibabaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Alibaba Tongyi”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Anthropic Claude

Wrapper around ChatAnthropic large language models that use the Chat endpoint

- 内部名称：`chatAnthropic`
- 版本：`8`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatAnthropic/ChatAnthropic.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`anthropicApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `extendedThinking` | Extended Thinking | `boolean` | 否 |
| `budgetTokens` | Budget Tokens | `number` | 否 |
| `adaptiveThinking` | Adaptive Thinking | `boolean` | 否 |
| `thinkingEffort` | Thinking Effort | `options` | 否 |
| `maxTokensToSample` | Max Tokens | `number` | 否 |
| `topP` | Top P | `number` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Anthropic Claude”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## AWS Bedrock

Wrapper around AWS Bedrock large language models. Supports built-in, imported, fine-tuned, and provisioned-throughput models.

- 内部名称：`awsChatBedrock`
- 版本：`6.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/AWSBedrock/AWSChatBedrock.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `region` | Region | `asyncOptions` | 是 |
| `model` | Model Name | `asyncOptions` | 否 |
| `customModel` | Custom Model ARN | `string` | 否 |
| `endpointHost` | Custom Endpoint Host | `string` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `max_tokens_to_sample` | Max Tokens to Sample | `number` | 否 |
| `latencyOptimized` | Latency Optimized | `boolean` | 否 |
| `useGlobalEndpoint` | Use Global Inference Endpoint | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AWS Bedrock”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输入包含动态表达式，目录仅列出可静态解析参数；源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Azure OpenAI

Wrapper around Azure OpenAI large language models that use the Chat endpoint

- 内部名称：`azureChatOpenAI`
- 版本：`7.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/AzureChatOpenAI/AzureChatOpenAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`azureOpenAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `reasoning` | Reasoning | `boolean` | 否 |
| `reasoningEffort` | Reasoning Effort | `options` | 是 |
| `reasoningSummary` | Reasoning Summary | `options` | 是 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Azure OpenAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## AzureChatOpenAI

Wrapper around Azure OpenAI Chat LLM specific for LlamaIndex

- 内部名称：`azureChatOpenAI_LlamaIndex`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/AzureChatOpenAI/AzureChatOpenAI_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`azureOpenAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AzureChatOpenAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Baidu Wenxin

Wrapper around BaiduWenxin Chat Endpoints

- 内部名称：`chatBaiduWenxin`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatBaiduWenxin/ChatBaiduWenxin.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`baiduQianfanApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `customModelName` | Custom Model Name | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `penaltyScore` | Penalty Score | `number` | 否 |
| `userId` | User ID | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Baidu Wenxin”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Cerebras

Wrapper around Cerebras Inference API

- 内部名称：`chatCerebras`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatCerebras/ChatCerebras.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cerebrasAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Cerebras”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatAnthropic

Wrapper around ChatAnthropic LLM specific for LlamaIndex

- 内部名称：`chatAnthropic_LlamaIndex`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatAnthropic/ChatAnthropic_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`anthropicApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokensToSample` | Max Tokens | `number` | 否 |
| `topP` | Top P | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatAnthropic”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatGroq

Wrapper around Groq LLM specific for LlamaIndex

- 内部名称：`chatGroq_LlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/Groq/ChatGroq_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`groqApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatGroq”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatMistral

Wrapper around ChatMistral LLM specific for LlamaIndex

- 内部名称：`chatMistral_LlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatMistral/ChatMistral_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`mistralAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokensToSample` | Max Tokens | `number` | 否 |
| `topP` | Top P | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatMistral”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatOllama

Wrapper around ChatOllama LLM specific for LlamaIndex

- 内部名称：`chatOllama_LlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOllama/ChatOllama_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseUrl` | Base URL | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `topP` | Top P | `number` | 否 |
| `topK` | Top K | `number` | 否 |
| `mirostat` | Mirostat | `number` | 否 |
| `mirostatEta` | Mirostat ETA | `number` | 否 |
| `mirostatTau` | Mirostat TAU | `number` | 否 |
| `numCtx` | Context Window Size | `number` | 否 |
| `numGpu` | Number of GPU | `number` | 否 |
| `numThread` | Number of Thread | `number` | 否 |
| `repeatLastN` | Repeat Last N | `number` | 否 |
| `repeatPenalty` | Repeat Penalty | `number` | 否 |
| `stop` | Stop Sequence | `string` | 否 |
| `tfsZ` | Tail Free Sampling | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatOllama”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatOpenAI

Wrapper around OpenAI Chat LLM specific for LlamaIndex

- 内部名称：`chatOpenAI_LlamaIndex`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOpenAI/ChatOpenAI_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | BasePath | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatOpenAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## ChatTogetherAI

Wrapper around ChatTogetherAI LLM specific for LlamaIndex

- 内部名称：`chatTogetherAI_LlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatTogetherAI/ChatTogether_LlamaIndex.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`togetherAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“ChatTogetherAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Cloudflare Workers AI

Wrapper around Cloudflare Workers AI chat models

- 内部名称：`chatCloudflareWorkersAI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatCloudflareWorkersAI/ChatCloudflareWorkersAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cloudflareApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Model | `string` | 是 |
| `baseUrl` | Base URL | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Cloudflare Workers AI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Cohere

Wrapper around Cohere Chat Endpoints

- 内部名称：`chatCohere`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatCohere/ChatCohere.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cohereApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Cohere”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Comet

Wrapper around CometAPI large language models that use the Chat endpoint

- 内部名称：`chatCometAPI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatCometAPI/ChatCometAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cometApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Comet”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Deepseek

Wrapper around Deepseek large language models that use the Chat endpoint

- 内部名称：`chatDeepseek`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/Deepseek/Deepseek.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`deepseekApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `stopSequence` | Stop Sequence | `string` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Deepseek”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Fireworks AI

Wrapper around Fireworks Chat Endpoints

- 内部名称：`chatFireworks`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatFireworks/ChatFireworks.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`fireworksApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Fireworks AI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Gemini

Wrapper around Google Gemini large language models that use the Chat endpoint

- 内部名称：`chatGoogleGenerativeAI`
- 版本：`3.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatGoogleGenerativeAI/ChatGoogleGenerativeAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleGenerativeAI`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `customModelName` | Custom Model Name | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `thinkingBudget` | Thinking Budget | `number` | 否 |
| `thinkingLevel` | Thinking Level | `options` | 否 |
| `maxOutputTokens` | Max Output Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `topK` | Top Next Highest Probability Tokens | `number` | 否 |
| `safetySettings` | Safety Settings | `array` | 否 |
| `baseUrl` | Base URL | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Gemini”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google VertexAI

Wrapper around VertexAI large language models that use the Chat endpoint

- 内部名称：`chatGoogleVertexAI`
- 版本：`5.3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatGoogleVertexAI/ChatGoogleVertexAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleVertexAuth`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `region` | Region | `asyncOptions` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `customModelName` | Custom Model Name | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `thinkingBudget` | Thinking Budget | `number` | 否 |
| `thinkingLevel` | Thinking Level | `options` | 否 |
| `maxOutputTokens` | Max Output Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `topK` | Top Next Highest Probability Tokens | `number` | 否 |
| `thinkingBudget` | Thinking Budget | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google VertexAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Groq

Wrapper around Groq API with LPU Inference Engine

- 内部名称：`groqChat`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/Groq/Groq.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`groqApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Groq”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## HuggingFace

Wrapper around HuggingFace large language models

- 内部名称：`chatHuggingFace`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatHuggingFace/ChatHuggingFace.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`huggingFaceApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `model` | Model | `string` | 是 |
| `endpoint` | Endpoint | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `hfTopK` | Top K | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `stop` | Stop Sequence | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“HuggingFace”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## IBM Watsonx

Wrapper around IBM watsonx.ai foundation models

- 内部名称：`chatIBMWatsonx`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatIBMWatsonx/ChatIBMWatsonx.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`ibmWatsonx`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `logprobs` | Log Probs | `boolean` | 否 |
| `n` | N | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `topP` | Top P | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“IBM Watsonx”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Kimi (Moonshot)

Kimi (Moonshot AI) 大语言模型，支持 OpenAI 兼容 API

- 内部名称：`chatKimi`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatKimi/ChatKimi.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`kimiApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Kimi (Moonshot)”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LiteLLM

Connect to a Litellm server using OpenAI-compatible API

- 内部名称：`chatLitellm`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatLitellm/ChatLitellm.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`litellmApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `basePath` | Base URL | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top P | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LiteLLM”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LocalAI

Use local LLMs like llama.cpp, gpt4all using LocalAI

- 内部名称：`chatLocalAI`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatLocalAI/ChatLocalAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`localAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `basePath` | Base Path | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LocalAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## MistralAI

Wrapper around Mistral large language models that use the Chat endpoint

- 内部名称：`chatMistralAI`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatMistral/ChatMistral.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`mistralAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxOutputTokens` | Max Output Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `randomSeed` | Random Seed | `number` | 否 |
| `safeMode` | Safe Mode | `boolean` | 否 |
| `overrideEndpoint` | Override Endpoint | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“MistralAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Nemo Guardrails

Access models through the Nemo Guardrails API

- 内部名称：`chatNemoGuardrails`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatNemoGuardrails/ChatNemoGuardrails.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `configurationId` | Configuration ID | `string` | 是 |
| `baseUrl` | Base URL | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Nemo Guardrails”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Nvidia NIM

Wrapper around NVIDIA NIM Inference API

- 内部名称：`chatNvidiaNIM`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatNvdiaNIM/ChatNvdiaNIM.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`nvidiaNIMApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `basePath` | Base Path | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Nvidia NIM”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Ollama

Chat completion using open-source LLM on Ollama

- 内部名称：`chatOllama`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOllama/ChatOllama.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`ollamaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `baseUrl` | Base URL | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `think` | Think | `boolean` | 否 |
| `jsonMode` | JSON Mode | `boolean` | 否 |
| `keepAlive` | Keep Alive | `string` | 否 |
| `topP` | Top P | `number` | 否 |
| `topK` | Top K | `number` | 否 |
| `mirostat` | Mirostat | `number` | 否 |
| `mirostatEta` | Mirostat ETA | `number` | 否 |
| `mirostatTau` | Mirostat TAU | `number` | 否 |
| `numCtx` | Context Window Size | `number` | 否 |
| `numGpu` | Number of GPU | `number` | 否 |
| `numThread` | Number of Thread | `number` | 否 |
| `repeatLastN` | Repeat Last N | `number` | 否 |
| `repeatPenalty` | Repeat Penalty | `number` | 否 |
| `stop` | Stop Sequence | `string` | 否 |
| `tfsZ` | Tail Free Sampling | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Ollama”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI

Wrapper around OpenAI large language models that use the Chat endpoint

- 内部名称：`chatOpenAI`
- 版本：`8.3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOpenAI/ChatOpenAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `reasoning` | Reasoning | `boolean` | 否 |
| `reasoningEffort` | Reasoning Effort | `options` | 是 |
| `reasoningSummary` | Reasoning Summary | `options` | 是 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `strictToolCalling` | Strict Tool Calling | `boolean` | 否 |
| `stopSequence` | Stop Sequence | `string` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Custom Model

Custom/FineTuned model using OpenAI Chat compatible API

- 内部名称：`chatOpenAICustom`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOpenAICustom/ChatOpenAICustom.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Custom Model”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenRouter

Wrapper around Open Router Inference API

- 内部名称：`chatOpenRouter`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatOpenRouter/ChatOpenRouter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openRouterApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenRouter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Perplexity

Wrapper around Perplexity large language models that use the Chat endpoint

- 内部名称：`chatPerplexity`
- 版本：`0.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatPerplexity/ChatPerplexity.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`perplexityApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `model` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top P | `number` | 否 |
| `topK` | Top K | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `searchDomainFilter` | Search Domain Filter | `json` | 否 |
| `returnImages` | Return Images | `boolean` | 否 |
| `returnRelatedQuestions` | Return Related Questions | `boolean` | 否 |
| `searchRecencyFilter` | Search Recency Filter | `options` | 否 |
| `proxyUrl` | Proxy Url | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Perplexity”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## SambaNova

Wrapper around Sambanova Chat Endpoints

- 内部名称：`chatSambanova`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatSambanova/ChatSambanova.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`sambanovaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“SambaNova”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## TogetherAI

Wrapper around TogetherAI large language models

- 内部名称：`chatTogetherAI`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatTogetherAI/ChatTogetherAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`togetherAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“TogetherAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## xAI Grok

Wrapper around Grok from XAI

- 内部名称：`chatXAI`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chatmodels/ChatXAI/ChatXAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chat-models)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`xaiApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model | `string` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `streaming` | Streaming | `boolean` | 否 |
| `allowImageUploads` | Allow Image Uploads | `boolean` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“xAI Grok”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
