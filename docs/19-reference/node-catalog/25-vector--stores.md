---
title: "节点目录：Vector Stores"
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

# 节点目录：Vector Stores

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 26 个节点。动态参数需以对应版本界面为准。

## Astra

Upsert embedded data and perform similarity or mmr search upon query using DataStax Astra DB, a serverless vector database that’s perfect for managing mission-critical AI workloads

- 内部名称：`Astra`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Astra/Astra.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`AstraDBApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `astraCollection` | Collection | `string` | 是 |
| `vectorDimension` | Vector Dimension | `number` | 否 |
| `similarityMetric` | Similarity Metric | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Astra Retriever | `dynamic` |
| `vectorStore` | Astra Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Astra”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## AWS Kendra

Use AWS Kendra's intelligent search service for document retrieval and semantic search

- 内部名称：`kendra`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Kendra/Kendra.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `region` | Region | `asyncOptions` | 是 |
| `indexId` | Kendra Index ID | `string` | 是 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `topK` | Top K | `number` | 否 |
| `attributeFilter` | Attribute Filter | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Kendra Retriever | `dynamic` |
| `vectorStore` | Kendra Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“AWS Kendra”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Chroma

Upsert embedded data and perform similarity search upon query using Chroma, an open-source embedding database

- 内部名称：`chroma`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Chroma/Chroma.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`chromaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `collectionName` | Collection Name | `string` | 是 |
| `chromaURL` | Chroma URL | `string` | 否 |
| `chromaMetadataFilter` | Chroma Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Chroma Retriever | `dynamic` |
| `vectorStore` | Chroma Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Chroma”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Couchbase

Upsert embedded data and load existing index using Couchbase, a award-winning distributed NoSQL database

- 内部名称：`couchbase`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Couchbase/Couchbase.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`couchbaseApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `bucketName` | Bucket Name | `string` | 是 |
| `scopeName` | Scope Name | `string` | 是 |
| `collectionName` | Collection Name | `string` | 是 |
| `indexName` | Index Name | `string` | 是 |
| `textKey` | Content Field | `string` | 否 |
| `embeddingKey` | Embedded Field | `string` | 否 |
| `couchbaseMetadataFilter` | Couchbase Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Couchbase Retriever | `dynamic` |
| `vectorStore` | Couchbase Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Couchbase”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Document Store (Vector)

Search and retrieve documents from Document Store

- 内部名称：`documentStoreVS`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/DocumentStoreVS/DocStoreVector.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedStore` | Select Store | `asyncOptions` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Retriever | `dynamic` |
| `vectorStore` | Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Document Store (Vector)”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Elasticsearch

Upsert embedded data and perform similarity search upon query using Elasticsearch, a distributed search and analytics engine

- 内部名称：`elasticsearch`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Elasticsearch/Elasticsearch.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`elasticSearchUserPassword`, `elasticsearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `indexName` | Index Name | `string` | 是 |
| `topK` | Top K | `number` | 否 |
| `similarity` | Similarity | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Elasticsearch Retriever | `dynamic` |
| `vectorStore` | Elasticsearch Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Elasticsearch”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Faiss

Upsert embedded data and perform similarity search upon query using Faiss library from Meta

- 内部名称：`faiss`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Faiss/Faiss.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `basePath` | Base Path to load | `string` | 是 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Faiss Retriever | `dynamic` |
| `vectorStore` | Faiss Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Faiss”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## In-Memory Vector Store

In-memory vectorstore that stores embeddings and does an exact, linear search for the most similar embeddings.

- 内部名称：`memoryVectorStore`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/InMemory/InMemoryVectorStore.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Memory Retriever | `dynamic` |
| `vectorStore` | Memory Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“In-Memory Vector Store”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Meilisearch

Upsert embedded data and perform similarity search upon query using Meilisearch hybrid search functionality

- 内部名称：`meilisearch`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Meilisearch/Meilisearch.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`meilisearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `host` | Host | `string` | 是 |
| `indexUid` | Index Uid | `string` | 是 |
| `deleteIndex` | Delete Index if exists | `boolean` | 否 |
| `K` | Top K | `number` | 否 |
| `semanticRatio` | Semantic Ratio | `number` | 否 |
| `searchFilter` | Search Filter | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `MeilisearchRetriever` | Meilisearch Retriever | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Meilisearch”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Milvus

Upsert embedded data and perform similarity search upon query using Milvus, world's most advanced open-source vector database

- 内部名称：`milvus`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Milvus/Milvus.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`milvusAuth`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `milvusServerUrl` | Milvus Server URL | `string` | 是 |
| `milvusCollection` | Milvus Collection Name | `string` | 是 |
| `milvusPartition` | Milvus Partition Name | `string` | 否 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `milvusTextField` | Milvus Text Field | `string` | 否 |
| `milvusFilter` | Milvus Filter | `string` | 否 |
| `topK` | Top K | `number` | 否 |
| `secure` | Secure | `boolean` | 否 |
| `clientPemPath` | Client PEM Path | `string` | 否 |
| `clientKeyPath` | Client Key Path | `string` | 否 |
| `caPemPath` | CA PEM Path | `string` | 否 |
| `serverName` | Server Name | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Milvus Retriever | `dynamic` |
| `vectorStore` | Milvus Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Milvus”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## MongoDB Atlas

Upsert embedded data and perform similarity or mmr search upon query using MongoDB Atlas, a managed cloud mongodb database

- 内部名称：`mongoDBAtlas`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/MongoDBAtlas/MongoDBAtlas.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`mongoDBUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `databaseName` | Database | `string` | 是 |
| `collectionName` | Collection Name | `string` | 是 |
| `indexName` | Index Name | `string` | 是 |
| `textKey` | Content Field | `string` | 否 |
| `embeddingKey` | Embedded Field | `string` | 否 |
| `mongoMetadataFilter` | Mongodb Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | MongoDB Retriever | `dynamic` |
| `vectorStore` | MongoDB Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“MongoDB Atlas”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## OpenSearch

Upsert embedded data and perform similarity search upon query using OpenSearch, an open-source, all-in-one vector database

- 内部名称：`openSearch`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/OpenSearch/OpenSearch.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`openSearchUrl`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `indexName` | Index Name | `string` | 是 |
| `topK` | Top K | `number` | 否 |
| `engine` | Engine | `options` | 否 |
| `spaceType` | Space Type | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | OpenSearch Retriever | `dynamic` |
| `vectorStore` | OpenSearch Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“OpenSearch”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Pinecone

Upsert embedded data and perform similarity or mmr search using Pinecone, a leading fully managed hosted vector database

- 内部名称：`pinecone`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Pinecone/Pinecone.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`pineconeApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `pineconeIndex` | Pinecone Index | `string` | 是 |
| `pineconeNamespace` | Pinecone Namespace | `string` | 否 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `pineconeTextKey` | Pinecone Text Key | `string` | 否 |
| `pineconeMetadataFilter` | Pinecone Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Pinecone Retriever | `dynamic` |
| `vectorStore` | Pinecone Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Pinecone”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Pinecone

Upsert embedded data and perform similarity search upon query using Pinecone, a leading fully managed hosted vector database

- 内部名称：`pineconeLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Pinecone/Pinecone_LlamaIndex.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`pineconeApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `model` | Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `embeddings` | Embeddings | `BaseEmbedding_LlamaIndex` | 是 |
| `pineconeIndex` | Pinecone Index | `string` | 是 |
| `pineconeNamespace` | Pinecone Namespace | `string` | 否 |
| `pineconeMetadataFilter` | Pinecone Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Pinecone Retriever | `dynamic` |
| `vectorStore` | Pinecone Vector Store Index | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Pinecone”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Postgres

Upsert embedded data and perform similarity search upon query using pgvector on Postgres

- 内部名称：`postgres`
- 版本：`7.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Postgres/Postgres.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`PostgresApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `port` | Port | `number` | 否 |
| `ssl` | SSL | `boolean` | 否 |
| `tableName` | Table Name | `string` | 否 |
| `driver` | Driver | `options` | 否 |
| `distanceStrategy` | Distance Strategy | `options` | 否 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `batchSize` | Upsert Batch Size | `number` | 否 |
| `additionalConfig` | Additional Configuration | `json` | 否 |
| `topK` | Top K | `number` | 否 |
| `pgMetadataFilter` | Postgres Metadata Filter | `json` | 否 |
| `contentColumnName` | Content Column Name | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Postgres Retriever | `dynamic` |
| `vectorStore` | Postgres Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Postgres”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Qdrant

Upsert embedded data and perform similarity search upon query using Qdrant, a scalable open source vector database written in Rust

- 内部名称：`qdrant`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Qdrant/Qdrant.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`qdrantApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `qdrantServerUrl` | Qdrant Server URL | `string` | 是 |
| `qdrantCollection` | Qdrant Collection Name | `string` | 是 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `qdrantVectorDimension` | Vector Dimension | `number` | 是 |
| `contentPayloadKey` | Content Key | `string` | 否 |
| `metadataPayloadKey` | Metadata Key | `string` | 否 |
| `batchSize` | Upsert Batch Size | `number` | 否 |
| `qdrantSimilarity` | Similarity | `options` | 是 |
| `qdrantCollectionConfiguration` | Additional Collection Cofiguration | `json` | 否 |
| `topK` | Top K | `number` | 否 |
| `qdrantFilter` | Qdrant Search Filter | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Qdrant Retriever | `dynamic` |
| `vectorStore` | Qdrant Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Qdrant”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Redis

Upsert embedded data and perform similarity search upon query using Redis, an open source, in-memory data structure store

- 内部名称：`redis`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Redis/Redis.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`redisCacheApi`, `redisCacheUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `indexName` | Index Name | `string` | 是 |
| `replaceIndex` | Replace Index on Upsert | `boolean` | 是 |
| `contentKey` | Content Field | `string` | 否 |
| `metadataKey` | Metadata Field | `string` | 否 |
| `vectorKey` | Vector Field | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Redis Retriever | `dynamic` |
| `vectorStore` | Redis Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Redis”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## SimpleStore

Upsert embedded data to local path and perform similarity search

- 内部名称：`simpleStoreLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/SimpleStore/SimpleStore.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `model` | Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `embeddings` | Embeddings | `BaseEmbedding_LlamaIndex` | 是 |
| `basePath` | Base Path to store | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | SimpleStore Retriever | `dynamic` |
| `vectorStore` | SimpleStore Vector Store Index | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“SimpleStore”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## SingleStore

Upsert embedded data and perform similarity search upon query using SingleStore, a fast and distributed cloud relational database

- 内部名称：`singlestore`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Singlestore/Singlestore.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`singleStoreApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `tableName` | Table Name | `string` | 否 |
| `contentColumnName` | Content Column Name | `string` | 否 |
| `vectorColumnName` | Vector Column Name | `string` | 否 |
| `metadataColumnName` | Metadata Column Name | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | SingleStore Retriever | `dynamic` |
| `vectorStore` | SingleStore Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“SingleStore”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Supabase

Upsert embedded data and perform similarity or mmr search upon query using Supabase via pgvector extension

- 内部名称：`supabase`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Supabase/Supabase.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`supabaseApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `supabaseProjUrl` | Supabase Project URL | `string` | 是 |
| `tableName` | Table Name | `string` | 是 |
| `queryName` | Query Name | `string` | 是 |
| `supabaseMetadataFilter` | Supabase Metadata Filter | `json` | 否 |
| `supabaseRPCFilter` | Supabase RPC Filter | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Supabase Retriever | `dynamic` |
| `vectorStore` | Supabase Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Supabase”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Upstash Vector

Upsert data as embedding or string and perform similarity search with Upstash, the leading serverless data platform

- 内部名称：`upstash`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Upstash/Upstash.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：Upstash Vector 连接托管向量服务并可能写入数据；费用取决于 Upstash 套餐
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`upstashVectorApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `fileUpload` | File Upload | `boolean` | 否 |
| `upstashMetadataFilter` | Upstash Metadata Filter | `string` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Upstash Retriever | `dynamic` |
| `vectorStore` | Upstash Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Upstash Vector”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Vectara

Upsert embedded data and perform similarity search upon query using Vectara, a LLM-powered search-as-a-service

- 内部名称：`vectara`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Vectara/Vectara.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`vectaraApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `file` | File | `file` | 否 |
| `filter` | Metadata Filter | `string` | 否 |
| `sentencesBefore` | Sentences Before | `number` | 否 |
| `sentencesAfter` | Sentences After | `number` | 否 |
| `lambda` | Lambda | `number` | 否 |
| `topK` | Top K | `number` | 否 |
| `mmrK` | MMR K | `number` | 否 |
| `mmrDiversityBias` | MMR diversity bias | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Vectara Retriever | `dynamic` |
| `vectorStore` | Vectara Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Vectara”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Vectara Upload File

Upload files to Vectara

- 内部名称：`vectaraUpload`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Vectara/Vectara_Upload.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`vectaraApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `file` | File | `file` | 是 |
| `filter` | Metadata Filter | `string` | 否 |
| `sentencesBefore` | Sentences Before | `number` | 否 |
| `sentencesAfter` | Sentences After | `number` | 否 |
| `lambda` | Lambda | `number` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Vectara Retriever | `dynamic` |
| `vectorStore` | Vectara Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Vectara Upload File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Weaviate

Upsert embedded data and perform similarity or mmr search using Weaviate, a scalable open-source vector database

- 内部名称：`weaviate`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Weaviate/Weaviate.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`weaviateApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `recordManager` | Record Manager | `RecordManager` | 否 |
| `weaviateConnectionType` | Weaviate Connection Type | `options` | 是 |
| `weaviateHost` | Weaviate Host/URL | `string` | 是 |
| `weaviateHttpSecure` | HTTP Secure | `boolean` | 否 |
| `weaviateGrpcHost` | GRPC Host/URL | `string` | 否 |
| `weaviateGrpcSecure` | GRPC Secure | `boolean` | 否 |
| `weaviateIndex` | Weaviate Index | `string` | 是 |
| `weaviateTextKey` | Weaviate Text Key | `string` | 否 |
| `weaviateMetadataKeys` | Weaviate Metadata Keys | `string` | 否 |
| `topK` | Top K | `number` | 否 |
| `weaviateFilter` | Weaviate Search Filter | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Weaviate Retriever | `dynamic` |
| `vectorStore` | Weaviate Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Weaviate”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Zep Collection - Cloud

Upsert embedded data and perform similarity or mmr search upon query using Zep, a fast and scalable building block for LLM apps

- 内部名称：`zepCloud`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/ZepCloud/ZepCloud.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`zepMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `zepCollection` | Zep Collection | `string` | 是 |
| `zepMetadataFilter` | Zep Metadata Filter | `json` | 否 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Zep Retriever | `dynamic` |
| `vectorStore` | Zep Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Zep Collection - Cloud”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Zep Collection - Open Source

Upsert embedded data and perform similarity or mmr search upon query using Zep, a fast and scalable building block for LLM apps

- 内部名称：`zep`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/vectorstores/Zep/Zep.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/vector-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`zepMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `document` | Document | `Document` | 否 |
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `baseURL` | Base URL | `string` | 是 |
| `zepCollection` | Zep Collection | `string` | 是 |
| `zepMetadataFilter` | Zep Metadata Filter | `json` | 否 |
| `dimension` | Embedding Dimension | `number` | 是 |
| `topK` | Top K | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `retriever` | Zep Retriever | `dynamic` |
| `vectorStore` | Zep Vector Store | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Zep Collection - Open Source”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数
