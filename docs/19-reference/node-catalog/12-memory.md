---
title: "节点目录：Memory"
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

# 节点目录：Memory

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 15 个节点。动态参数需以对应版本界面为准。

## Agent Memory

Memory for agentflow to remember the state of the conversation

- 内部名称：`agentMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/AgentMemory/AgentMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`MySQLApi`, `PostgresApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `databaseType` | Database | `options` | 是 |
| `databaseFilePath` | Database File Path | `string` | 否 |
| `host` | Host | `string` | 否 |
| `database` | Database | `string` | 否 |
| `port` | Port | `number` | 否 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Agent Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Buffer Memory

Retrieve chat messages stored in database

- 内部名称：`bufferMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/BufferMemory/BufferMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sessionId` | Session Id | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Buffer Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Buffer Window Memory

Uses a window of size k to surface the last k back-and-forth to use as memory

- 内部名称：`bufferWindowMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/BufferWindowMemory/BufferWindowMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `k` | Size | `number` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Buffer Window Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Conversation Summary Buffer Memory

Uses token length to decide when to summarize conversations

- 内部名称：`conversationSummaryBufferMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/ConversationSummaryBufferMemory/ConversationSummaryBufferMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `maxTokenLimit` | Max Token Limit | `number` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversation Summary Buffer Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Conversation Summary Memory

Summarizes the conversation and stores the current summary in memory

- 内部名称：`conversationSummaryMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/ConversationSummaryMemory/ConversationSummaryMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Chat Model | `BaseChatModel` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Conversation Summary Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## DynamoDB Chat Memory

Stores the conversation in dynamo db table

- 内部名称：`DynamoDBChatMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/DynamoDb/DynamoDb.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`dynamodbMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `tableName` | Table Name | `string` | 是 |
| `partitionKey` | Partition Key | `string` | 是 |
| `region` | Region | `string` | 是 |
| `sessionId` | Session ID | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“DynamoDB Chat Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Mem0

Stores and manages chat memory using Mem0 service

- 内部名称：`mem0`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/Mem0/Mem0.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`mem0MemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `user_id` | User ID | `string` | 否 |
| `useFlowiseChatId` | Use Flowise Chat ID | `boolean` | 否 |
| `searchOnly` | Search Only | `boolean` | 否 |
| `run_id` | Run ID | `string` | 否 |
| `agent_id` | Agent ID | `string` | 否 |
| `app_id` | App ID | `string` | 否 |
| `project_id` | Project ID | `string` | 否 |
| `org_id` | Organization ID | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 否 |
| `inputKey` | Input Key | `string` | 否 |
| `outputKey` | Output Key | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Mem0”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## MongoDB Atlas Chat Memory

Stores the conversation in MongoDB Atlas

- 内部名称：`MongoDBAtlasChatMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/MongoDBMemory/MongoDBMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`mongoDBUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `databaseName` | Database | `string` | 是 |
| `collectionName` | Collection Name | `string` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“MongoDB Atlas Chat Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## MySQL Agent Memory

Memory for agentflow to remember the state of the conversation using MySQL database

- 内部名称：`mySQLAgentMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/AgentMemory/MySQLAgentMemory/MySQLAgentMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`MySQLApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `port` | Port | `number` | 是 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“MySQL Agent Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Postgres Agent Memory

Memory for agentflow to remember the state of the conversation using Postgres database

- 内部名称：`postgresAgentMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/AgentMemory/PostgresAgentMemory/PostgresAgentMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`PostgresApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `port` | Port | `number` | 是 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Postgres Agent Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Redis-Backed Chat Memory

Summarizes the conversation and stores the memory in Redis server

- 内部名称：`RedisBackedChatMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/RedisBackedChatMemory/RedisBackedChatMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`redisCacheApi`, `redisCacheUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sessionId` | Session Id | `string` | 否 |
| `sessionTTL` | Session Timeouts | `number` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |
| `windowSize` | Window Size | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Redis-Backed Chat Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## SQLite Agent Memory

Memory for agentflow to remember the state of the conversation using SQLite database

- 内部名称：`sqliteAgentMemory`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/AgentMemory/SQLiteAgentMemory/SQLiteAgentMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `databaseFilePath` | Database File Path | `string` | 否 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“SQLite Agent Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Upstash Redis-Backed Chat Memory

Summarizes the conversation and stores the memory in Upstash Redis server

- 内部名称：`upstashRedisBackedChatMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/UpstashRedisBackedChatMemory/UpstashRedisBackedChatMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：Upstash Chat Memory 连接托管 Redis 并写入会话；费用取决于 Upstash 套餐
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`upstashRedisMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseURL` | Upstash Redis REST URL | `string` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `sessionTTL` | Session Timeouts | `number` | 否 |
| `memoryKey` | Memory Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Upstash Redis-Backed Chat Memory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Zep Memory - Cloud

Summarizes the conversation and stores the memory in zep server

- 内部名称：`ZepMemoryCloud`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/ZepMemoryCloud/ZepMemoryCloud.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`zepMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sessionId` | Session Id | `string` | 否 |
| `memoryType` | Memory Type | `string` | 是 |
| `aiPrefix` | AI Prefix | `string` | 是 |
| `humanPrefix` | Human Prefix | `string` | 是 |
| `memoryKey` | Memory Key | `string` | 是 |
| `inputKey` | Input Key | `string` | 是 |
| `outputKey` | Output Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Zep Memory - Cloud”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Zep Memory - Open Source

Summarizes the conversation and stores the memory in zep server

- 内部名称：`ZepMemory`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/memory/ZepMemory/ZepMemory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/memory)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`zepMemoryApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseURL` | Base URL | `string` | 是 |
| `sessionId` | Session Id | `string` | 否 |
| `k` | Size | `number` | 是 |
| `aiPrefix` | AI Prefix | `string` | 是 |
| `humanPrefix` | Human Prefix | `string` | 是 |
| `memoryKey` | Memory Key | `string` | 是 |
| `inputKey` | Input Key | `string` | 是 |
| `outputKey` | Output Key | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Zep Memory - Open Source”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
