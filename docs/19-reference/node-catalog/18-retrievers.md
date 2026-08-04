---
title: "节点目录：Retrievers"
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

# 节点目录：Retrievers

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 15 个节点。动态参数需以对应版本界面为准。

## AWS Bedrock Knowledge Base Retriever

Connect to AWS Bedrock Knowledge Base API and retrieve relevant chunks

- 内部名称：`awsBedrockKBRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/AWSBedrockKBRetriever/AWSBedrockKBRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `region` | Region | `asyncOptions` | 是 |
| `knoledgeBaseID` | Knowledge Base ID | `string` | 是 |
| `query` | Query | `string` | 否 |
| `topK` | TopK | `number` | 否 |
| `searchType` | SearchType | `options` | 否 |
| `filter` | Filter | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AWS Bedrock Knowledge Base Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Azure Rerank Retriever

Azure Rerank indexes the documents from most to least semantically relevant to the query.

- 内部名称：`AzureRerankRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/AzureRerankRetriever/AzureRerankRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`azureFoundryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Model Name | `options` | 否 |
| `query` | Query | `string` | 否 |
| `topK` | Top K | `number` | 否 |
| `maxChunksPerDoc` | Max Chunks Per Doc | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Azure Rerank Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Azure Rerank Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Cohere Rerank Retriever

Cohere Rerank indexes the documents from most to least semantically relevant to the query.

- 内部名称：`cohereRerankRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/CohereRerankRetriever/CohereRerankRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`cohereApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Model Name | `options` | 否 |
| `query` | Query | `string` | 否 |
| `topK` | Top K | `number` | 否 |
| `maxChunksPerDoc` | Max Chunks Per Doc | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Cohere Rerank Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Cohere Rerank Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Custom Retriever

Return results based on predefined format

- 内部名称：`customRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/CustomRetriever/CustomRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `query` | Query | `string` | 否 |
| `resultFormat` | Result Format | `string` | 是 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Custom Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Custom Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Embeddings Filter Retriever

A document compressor that uses embeddings to drop documents unrelated to the query

- 内部名称：`embeddingsFilterRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/EmbeddingsFilterRetriever/EmbeddingsFilterRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `query` | Query | `string` | 否 |
| `similarityThreshold` | Similarity Threshold | `number` | 否 |
| `k` | K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Embeddings Filter Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Embeddings Filter Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Extract Metadata Retriever

Extract keywords/metadata from the query and use it to filter documents

- 内部名称：`extractMetadataRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/ExtractMetadataRetriever/ExtractMetadataRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `model` | Chat Model | `BaseChatModel` | 是 |
| `query` | Query | `string` | 否 |
| `dynamicMetadataFilterRetrieverPrompt` | Prompt | `string` | 是 |
| `dynamicMetadataFilterRetrieverStructuredOutput` | JSON Structured Output | `datagrid` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Extract Metadata Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Extract Metadata Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## HyDE Retriever

Use HyDE retriever to retrieve from a vector store

- 内部名称：`HydeRetriever`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/HydeRetriever/HydeRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `query` | Query | `string` | 否 |
| `promptKey` | Select Defined Prompt | `options` | 是 |
| `customPrompt` | Custom Prompt | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | HyDE Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“HyDE Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Jina AI Rerank Retriever

Jina AI Rerank indexes the documents from most to least semantically relevant to the query.

- 内部名称：`JinaRerankRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/JinaRerankRetriever/JinaRerankRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`jinaAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Model Name | `options` | 否 |
| `query` | Query | `string` | 否 |
| `topN` | Top N | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Jina AI Rerank Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Jina AI Rerank Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## LLM Filter Retriever

Iterate over the initially returned documents and extract, from each, only the content that is relevant to the query

- 内部名称：`llmFilterRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/LLMFilterRetriever/LLMFilterCompressionRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `query` | Query | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | LLM Filter Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“LLM Filter Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Multi Query Retriever

Generate multiple queries from different perspectives for a given user input query

- 内部名称：`multiQueryRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/MultiQueryRetriever/MultiQueryRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `modelPrompt` | Prompt | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Multi Query Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Prompt Retriever

Store prompt template with name & description to be later queried by MultiPromptChain

- 内部名称：`promptRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/PromptRetriever/PromptRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `name` | Prompt Name | `string` | 是 |
| `description` | Prompt Description | `string` | 是 |
| `systemMessage` | Prompt System Message | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Prompt Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Reciprocal Rank Fusion Retriever

Reciprocal Rank Fusion to re-rank search results by multiple query generation.

- 内部名称：`RRFRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/RRFRetriever/RRFRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `query` | Query | `string` | 否 |
| `queryCount` | Query Count | `number` | 否 |
| `topK` | Top K | `number` | 否 |
| `c` | Constant | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Reciprocal Rank Fusion Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Reciprocal Rank Fusion Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Similarity Score Threshold Retriever

Return results based on the minimum similarity percentage

- 内部名称：`similarityThresholdRetriever`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/SimilarityThresholdRetriever/SimilarityThresholdRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `query` | Query | `string` | 否 |
| `minSimilarityScore` | Minimum Similarity Score (%) | `number` | 是 |
| `maxK` | Max K | `number` | 是 |
| `kIncrement` | K Increment | `number` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Similarity Threshold Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Similarity Score Threshold Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Vector Store Retriever

Store vector store as retriever to be later queried by MultiRetrievalQAChain

- 内部名称：`vectorStoreRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/VectorStoreRetriever/VectorStoreRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `name` | Retriever Name | `string` | 是 |
| `description` | Retriever Description | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Vector Store Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Voyage AI Rerank Retriever

Voyage AI Rerank indexes the documents from most to least semantically relevant to the query.

- 内部名称：`voyageAIRerankRetriever`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/retrievers/VoyageAIRetriever/VoyageAIRerankRetriever.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/retrievers)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`voyageAIApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `model` | Model Name | `options` | 否 |
| `query` | Query | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Voyage AI Rerank Retriever | `dynamic` |
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Voyage AI Rerank Retriever”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足
