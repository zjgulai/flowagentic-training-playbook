---
title: "节点目录：Embeddings"
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

# 节点目录：Embeddings

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 18 个节点。动态参数需以对应版本界面为准。

## AWS Bedrock Embedding

AWSBedrock embedding models to generate embeddings for a given text

- 内部名称：`AWSBedrockEmbeddings`
- 版本：`5.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/AWSBedrockEmbedding/AWSBedrockEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `region` | Region | `asyncOptions` | 是 |
| `model` | Model Name | `asyncOptions` | 是 |
| `customModel` | Custom Model Name | `string` | 否 |
| `endpointHost` | Custom Endpoint Host | `string` | 否 |
| `inputType` | Cohere Input Type | `options` | 否 |
| `batchSize` | Batch Size | `number` | 否 |
| `maxRetries` | Max AWS API retries | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AWS Bedrock Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Azure OpenAI Embedding

Azure OpenAI API to generate embeddings for a given text

- 内部名称：`azureOpenAIEmbeddings`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/AzureOpenAIEmbedding/AzureOpenAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`azureOpenAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `batchSize` | Batch Size | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Azure OpenAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Azure OpenAI Embeddings

Azure OpenAI API embeddings specific for LlamaIndex

- 内部名称：`azureOpenAIEmbeddingsLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/AzureOpenAIEmbedding/AzureOpenAIEmbedding_LlamaIndex.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`azureOpenAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `timeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Azure OpenAI Embeddings”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Baidu Qianfan Embedding

Baidu Qianfan API to generate embeddings for a given text

- 内部名称：`baiduQianfanEmbeddings`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/BaiduQianfanEmbedding/BaiduQianfanEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`baiduQianfanApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `customModelName` | Custom Model Name | `string` | 否 |
| `stripNewLines` | Strip New Lines | `boolean` | 否 |
| `batchSize` | Batch Size | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Baidu Qianfan Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Cohere Embedding

Cohere API to generate embeddings for a given text

- 内部名称：`cohereEmbeddings`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/CohereEmbedding/CohereEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cohereApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `inputType` | Type | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Cohere Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Gemini Embedding

Google Generative API to generate embeddings for a given text

- 内部名称：`googleGenerativeAiEmbeddings`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/GoogleGenerativeAIEmbedding/GoogleGenerativeAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleGenerativeAI`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `tasktype` | Task Type | `options` | 是 |
| `stripNewLines` | Strip New Lines | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Gemini Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google VertexAI Embedding

Google vertexAI API to generate embeddings for a given text

- 内部名称：`googlevertexaiEmbeddings`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/GoogleVertexAIEmbedding/GoogleVertexAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleVertexAuth`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `region` | Region | `asyncOptions` | 否 |
| `stripNewLines` | Strip New Lines | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google VertexAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## HuggingFace Inference Embedding

HuggingFace Inference API to generate embeddings for a given text

- 内部名称：`huggingFaceInferenceEmbeddings`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/HuggingFaceInferenceEmbedding/HuggingFaceInferenceEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`huggingFaceApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model | `string` | 否 |
| `endpoint` | Endpoint | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“HuggingFace Inference Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## IBM Watsonx Embedding

Generate embeddings for a given text using open source model on IBM Watsonx

- 内部名称：`ibmEmbedding`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/IBMWatsonxEmbedding/IBMWatsonxEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`ibmWatsonx`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `string` | 是 |
| `truncateInputTokens` | Truncate Input Tokens | `number` | 否 |
| `maxRetries` | Max Retries | `number` | 否 |
| `maxConcurrency` | Max Concurrency | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“IBM Watsonx Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Jina Embedding

JinaAI API to generate embeddings for a given text

- 内部名称：`jinaEmbeddings`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/JinaAIEmbedding/JinaAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`jinaAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `string` | 是 |
| `modelDimensions` | Dimensions | `number` | 是 |
| `allowLateChunking` | Allow Late Chunking | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Jina Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LocalAI Embedding

Use local embeddings models like llama.cpp

- 内部名称：`localAIEmbeddings`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/LocalAIEmbedding/LocalAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`localAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `basePath` | Base Path | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LocalAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## MistralAI Embedding

MistralAI API to generate embeddings for a given text

- 内部名称：`mistralAIEmbeddings`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/MistralEmbedding/MistralEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`mistralAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `batchSize` | Batch Size | `number` | 否 |
| `stripNewLines` | Strip New Lines | `boolean` | 否 |
| `overrideEndpoint` | Override Endpoint | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“MistralAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Ollama Embedding

Generate embeddings for a given text using open source model on Ollama

- 内部名称：`ollamaEmbedding`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/OllamaEmbedding/OllamaEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseUrl` | Base URL | `string` | 是 |
| `modelName` | Model Name | `string` | 是 |
| `numGpu` | Number of GPU | `number` | 否 |
| `numThread` | Number of Thread | `number` | 否 |
| `useMMap` | Use MMap | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Ollama Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Custom Embedding

OpenAI API to generate embeddings for a given text

- 内部名称：`openAIEmbeddingsCustom`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/OpenAIEmbeddingCustom/OpenAIEmbeddingCustom.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `stripNewLines` | Strip New Lines | `boolean` | 否 |
| `batchSize` | Batch Size | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |
| `modelName` | Model Name | `string` | 否 |
| `dimensions` | Dimensions | `number` | 否 |
| `encodingFormat` | Encoding Format | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Custom Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Embedding

OpenAI API to generate embeddings for a given text

- 内部名称：`openAIEmbeddings`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/OpenAIEmbedding/OpenAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `stripNewLines` | Strip New Lines | `boolean` | 否 |
| `batchSize` | Batch Size | `number` | 否 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | Base Path | `string` | 否 |
| `baseOptions` | Base Options | `json` | 否 |
| `dimensions` | Dimensions | `number` | 否 |
| `encodingFormat` | Encoding Format | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAI Embedding

OpenAI Embedding specific for LlamaIndex

- 内部名称：`openAIEmbedding_LlamaIndex`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/OpenAIEmbedding/OpenAIEmbedding_LlamaIndex.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`openAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |
| `timeout` | Timeout | `number` | 否 |
| `basepath` | BasePath | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## TogetherAI Embedding

TogetherAI Embedding models to generate embeddings for a given text

- 内部名称：`togetherAIEmbedding`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/TogetherAIEmbedding/TogetherAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`togetherAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `cache` | Cache | `BaseCache` | 否 |
| `modelName` | Model Name | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“TogetherAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## VoyageAI Embedding

Voyage AI API to generate embeddings for a given text

- 内部名称：`voyageAIEmbeddings`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/embeddings/VoyageAIEmbedding/VoyageAIEmbedding.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/embeddings)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`voyageAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `modelName` | Model Name | `asyncOptions` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“VoyageAI Embedding”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
