---
title: "节点目录：Engine"
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

# 节点目录：Engine

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 4 个节点。动态参数需以对应版本界面为准。

## Context Chat Engine

Answer question based on retrieved documents (context) with built-in memory to remember conversation

- 内部名称：`contextChatEngine`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/engine/ChatEngine/ContextChatEngine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `vectorStoreRetriever` | Vector Store Retriever | `VectorIndexRetriever` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |
| `systemMessagePrompt` | System Message | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Context Chat Engine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Query Engine

Simple query engine built to answer question over your data, without memory

- 内部名称：`queryEngine`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/engine/QueryEngine/QueryEngine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStoreRetriever` | Vector Store Retriever | `VectorIndexRetriever` | 是 |
| `responseSynthesizer` | Response Synthesizer | `ResponseSynthesizer` | 否 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Query Engine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Simple Chat Engine

Simple engine to handle back and forth conversations

- 内部名称：`simpleChatEngine`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/engine/ChatEngine/SimpleChatEngine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `memory` | Memory | `BaseChatMemory` | 是 |
| `systemMessagePrompt` | System Message | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Simple Chat Engine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Sub Question Query Engine

Breaks complex query into sub questions for each relevant data source, then gather all the intermediate responses and synthesizes a final response

- 内部名称：`subQuestionQueryEngine`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/engine/SubQuestionQueryEngine/SubQuestionQueryEngine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `queryEngineTools` | QueryEngine Tools | `QueryEngineTool` | 是 |
| `model` | Chat Model | `BaseChatModel_LlamaIndex` | 是 |
| `embeddings` | Embeddings | `BaseEmbedding_LlamaIndex` | 是 |
| `responseSynthesizer` | Response Synthesizer | `ResponseSynthesizer` | 否 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Sub Question Query Engine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
