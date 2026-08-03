---
title: "节点目录：LLMs"
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

# 节点目录：LLMs

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 12 个节点。动态参数需以对应版本界面为准。

## AWS Bedrock

Wrapper around AWS Bedrock large language models

- 内部名称：`awsBedrock`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/AWSBedrock/AWSBedrock.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `region` | Region | `asyncOptions` | 是 |
| `model` | Model Name | `asyncOptions` | 是 |
| `customModel` | Custom Model Name | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `max_tokens_to_sample` | Max Tokens to Sample | `number` | 否 |

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
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Azure OpenAI

Wrapper around Azure OpenAI large language models

- 内部名称：`azureOpenAI`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/Azure OpenAI/AzureOpenAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
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
| `topP` | Top Probability | `number` | 否 |
| `bestOf` | Best Of | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |

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

## Cohere

Wrapper around Cohere large language models

- 内部名称：`cohere`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/Cohere/Cohere.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
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
| `maxTokens` | Max Tokens | `number` | 否 |

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

## Fireworks

Wrapper around Fireworks API for large language models

- 内部名称：`fireworks`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/Fireworks/Fireworks.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`fireworksApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Fireworks”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## GoogleVertexAI

Wrapper around GoogleVertexAI large language models

- 内部名称：`googlevertexai`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/GoogleVertexAI/GoogleVertexAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：需按实际配置复核；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleVertexAuth`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `asyncOptions` | 是 |
| `temperature` | Temperature | `number` | 否 |
| `maxOutputTokens` | max Output Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“GoogleVertexAI”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## HuggingFace Inference

Wrapper around HuggingFace large language models

- 内部名称：`huggingFaceInference_LLMs`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/HuggingFaceInference/HuggingFaceInference.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`huggingFaceApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `model` | Model | `string` | 否 |
| `endpoint` | Endpoint | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `hfTopK` | Top K | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“HuggingFace Inference”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## IBMWatsonx

Wrapper around IBM watsonx.ai foundation models

- 内部名称：`ibmWatsonx`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/IBMWatsonx/IBMWatsonx.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`ibmWatsonx`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelId` | Model | `string` | 是 |
| `decodingMethod` | Decoding Method | `options` | 否 |
| `topK` | Top K | `number` | 否 |
| `topP` | Top P | `number` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `repetitionPenalty` | Repeat Penalty | `number` | 否 |
| `streaming` | Streaming | `boolean` | 是 |
| `maxNewTokens` | Max New Tokens | `number` | 否 |
| `minNewTokens` | Min New Tokens | `number` | 否 |
| `stopSequence` | Stop Sequence | `string` | 否 |
| `includeStopSequence` | Include Stop Sequence | `boolean` | 否 |
| `randomSeed` | Random Seed | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“IBMWatsonx”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Ollama

Wrapper around open source large language models on Ollama

- 内部名称：`ollama`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/Ollama/Ollama.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
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

**隔离环境示例：** 在隔离培训画布中添加“Ollama”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI

Wrapper around OpenAI large language models

- 内部名称：`openAI`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/OpenAI/OpenAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
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
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `bestOf` | Best Of | `number` | 否 |
| `frequencyPenalty` | Frequency Penalty | `number` | 否 |
| `presencePenalty` | Presence Penalty | `number` | 否 |
| `batchSize` | Batch Size | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
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

## Replicate

Use Replicate to run open source models on cloud

- 内部名称：`replicate`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/Replicate/Replicate.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`replicateApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `model` | Model | `string` | 否 |
| `temperature` | Temperature | `number` | 否 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `topP` | Top Probability | `number` | 否 |
| `repetitionPenalty` | Repetition Penalty | `number` | 否 |
| `additionalInputs` | Additional Inputs | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Replicate”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Sambanova

Wrapper around Sambanova API for large language models

- 内部名称：`sambanova`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/SambaNova/Sambanova.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`sambanovaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Sambanova”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## TogetherAI

Wrapper around TogetherAI large language models

- 内部名称：`togetherAI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/llms/TogetherAI/TogetherAI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/llms)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`togetherAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |
| `topK` | Top K | `number` | 是 |
| `topP` | Top P | `number` | 是 |
| `temperature` | Temperature | `number` | 是 |
| `repeatPenalty` | Repeat Penalty | `number` | 是 |
| `streaming` | Streaming | `boolean` | 是 |
| `maxTokens` | Max Tokens | `number` | 否 |
| `stop` | Stop Sequence | `string` | 否 |

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
