---
title: "节点目录：Cache"
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

# 节点目录：Cache

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 6 个节点。动态参数需以对应版本界面为准。

## InMemory Cache

Cache LLM response in memory, will be cleared once app restarted

- 内部名称：`inMemoryCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/InMemoryCache/InMemoryCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“InMemory Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## InMemory Embedding Cache

Cache generated Embeddings in memory to avoid needing to recompute them.

- 内部名称：`inMemoryEmbeddingCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/InMemoryCache/InMemoryEmbeddingCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `namespace` | Namespace | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“InMemory Embedding Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Momento Cache

Cache LLM response using Momento, a distributed, serverless cache

- 内部名称：`momentoCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/MomentoCache/MomentoCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`momentoCacheApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Momento Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Redis Cache

Cache LLM response in Redis, useful for sharing cache across multiple processes or servers

- 内部名称：`redisCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/RedisCache/RedisCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`redisCacheApi`, `redisCacheUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `ttl` | Time to Live (ms) | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Redis Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Redis Embeddings Cache

Cache generated Embeddings in Redis to avoid needing to recompute them.

- 内部名称：`redisEmbeddingsCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/RedisCache/RedisEmbeddingsCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`redisCacheApi`, `redisCacheUrlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `embeddings` | Embeddings | `Embeddings` | 是 |
| `ttl` | Time to Live (ms) | `number` | 否 |
| `namespace` | Namespace | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Redis Embeddings Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Upstash Redis Cache

Cache LLM response in Upstash Redis, serverless data for Redis and Kafka

- 内部名称：`upstashRedisCache`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/cache/UpstashRedisCache/UpstashRedisCache.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/cache)
- 风险：Upstash Redis Cache 连接托管 Redis 并写入缓存；费用取决于 Upstash 套餐
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`upstashRedisApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Upstash Redis Cache”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
