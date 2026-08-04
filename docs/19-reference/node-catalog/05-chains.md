---
title: "节点目录：Chains"
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

# 节点目录：Chains

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 13 个节点。动态参数需以对应版本界面为准。

## Conversation Chain

Chat models specific conversational chain with memory

- 内部名称：`conversationChain`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/ConversationChain/ConversationChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `memory` | Memory | `BaseMemory` | 是 |
| `chatPromptTemplate` | Chat Prompt Template | `ChatPromptTemplate` | 否 |
| `document` | Document | `Document` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `systemMessagePrompt` | System Message | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversation Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Conversational Retrieval QA Chain

Document QA - built on RetrievalQAChain to provide a chat history component

- 内部名称：`conversationalRetrievalQAChain`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/ConversationalRetrievalQAChain/ConversationalRetrievalQAChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `vectorStoreRetriever` | Vector Store Retriever | `BaseRetriever` | 是 |
| `memory` | Memory | `BaseMemory` | 否 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |
| `rephrasePrompt` | Rephrase Prompt | `string` | 否 |
| `responsePrompt` | Response Prompt | `string` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `systemMessagePrompt` | System Message | `string` | 否 |
| `chainOption` | Chain Option | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversational Retrieval QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## GET API Chain

Chain to run queries against GET API

- 内部名称：`getApiChain`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/ApiChain/GETApiChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `apiDocs` | API Documentation | `string` | 是 |
| `headers` | Headers | `json` | 否 |
| `urlPrompt` | URL Prompt | `string` | 是 |
| `ansPrompt` | Answer Prompt | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“GET API Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Graph Cypher QA Chain

Advanced chain for question-answering against a Neo4j graph by generating Cypher statements

- 内部名称：`graphCypherQAChain`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/GraphCypherQAChain/GraphCypherQAChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `graph` | Neo4j Graph | `Neo4j` | 是 |
| `cypherPrompt` | Cypher Generation Prompt | `BasePromptTemplate` | 否 |
| `cypherModel` | Cypher Generation Model | `BaseLanguageModel` | 否 |
| `qaPrompt` | QA Prompt | `BasePromptTemplate` | 否 |
| `qaModel` | QA Model | `BaseLanguageModel` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `returnDirect` | Return Direct | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `graphCypherQAChain` | Graph Cypher QA Chain | `dynamic` |
| `outputPrediction` | Output Prediction | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Graph Cypher QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## LLM Chain

Chain to run queries against LLMs

- 内部名称：`llmChain`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/LLMChain/LLMChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `prompt` | Prompt | `BasePromptTemplate` | 是 |
| `outputParser` | Output Parser | `BaseLLMOutputParser` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |
| `chainName` | Chain Name | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `llmChain` | LLM Chain | `dynamic` |
| `outputPrediction` | Output Prediction | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“LLM Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Multi Prompt Chain

Chain automatically picks an appropriate prompt from multiple prompt templates

- 内部名称：`multiPromptChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/MultiPromptChain/MultiPromptChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `promptRetriever` | Prompt Retriever | `PromptRetriever` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Multi Prompt Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Multi Retrieval QA Chain

QA Chain that automatically picks an appropriate vector store from multiple retrievers

- 内部名称：`multiRetrievalQAChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/MultiRetrievalQAChain/MultiRetrievalQAChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `vectorStoreRetriever` | Vector Store Retriever | `VectorStoreRetriever` | 是 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Multi Retrieval QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAPI Chain

Chain that automatically select and call APIs based only on an OpenAPI spec

- 内部名称：`openApiChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/ApiChain/OpenAPIChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `yamlLink` | YAML Link | `string` | 是 |
| `yamlFile` | YAML File | `file` | 是 |
| `headers` | Headers | `json` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAPI Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## POST API Chain

Chain to run queries against POST API

- 内部名称：`postApiChain`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/ApiChain/POSTApiChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：POST API Chain 调用所选模型并向配置的 API 发起 POST；两者可能产生费用或外部副作用
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `apiDocs` | API Documentation | `string` | 是 |
| `headers` | Headers | `json` | 否 |
| `urlPrompt` | URL Prompt | `string` | 是 |
| `ansPrompt` | Answer Prompt | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“POST API Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Retrieval QA Chain

QA chain to answer a question based on the retrieved documents

- 内部名称：`retrievalQAChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/RetrievalQAChain/RetrievalQAChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `vectorStoreRetriever` | Vector Store Retriever | `BaseRetriever` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Retrieval QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Sql Database Chain

Answer questions over a SQL database

- 内部名称：`sqlDatabaseChain`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/SqlDatabaseChain/SqlDatabaseChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `database` | Database | `options` | 是 |
| `url` | Connection string or file path (sqlite only) | `string` | 是 |
| `includesTables` | Include Tables | `string` | 否 |
| `ignoreTables` | Ignore Tables | `string` | 否 |
| `sampleRowsInTableInfo` | Sample table's rows info | `number` | 否 |
| `topK` | Top Keys | `number` | 否 |
| `customPrompt` | Custom Prompt | `string` | 否 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Sql Database Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Vectara QA Chain

QA chain for Vectara

- 内部名称：`vectaraQAChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/VectaraChain/VectaraChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectaraStore` | Vectara Store | `VectorStore` | 是 |
| `summarizerPromptName` | Summarizer Prompt Name | `options` | 是 |
| `responseLang` | Response Language | `options` | 否 |
| `maxSummarizedResults` | Max Summarized Results | `number` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Vectara QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## VectorDB QA Chain

QA chain for vector databases

- 内部名称：`vectorDBQAChain`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/chains/VectorDBQAChain/VectorDBQAChain.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/chains)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `inputModeration` | Input Moderation | `Moderation` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“VectorDB QA Chain”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
