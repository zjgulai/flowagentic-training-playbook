---
title: "节点目录：Record Manager"
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

# 节点目录：Record Manager

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 3 个节点。动态参数需以对应版本界面为准。

## MySQL Record Manager

Use MySQL to keep track of document writes into the vector databases

- 内部名称：`MySQLRecordManager`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/recordmanager/MySQLRecordManager/MySQLrecordManager.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/document-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`MySQLApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `port` | Port | `number` | 否 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |
| `tableName` | Table Name | `string` | 否 |
| `namespace` | Namespace | `string` | 否 |
| `cleanup` | Cleanup | `options` | 是 |
| `sourceIdKey` | SourceId Key | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“MySQL Record Manager”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Postgres Record Manager

Use Postgres to keep track of document writes into the vector databases

- 内部名称：`postgresRecordManager`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/recordmanager/PostgresRecordManager/PostgresRecordManager.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/document-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`PostgresApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `host` | Host | `string` | 是 |
| `database` | Database | `string` | 是 |
| `port` | Port | `number` | 否 |
| `ssl` | SSL | `boolean` | 否 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |
| `tableName` | Table Name | `string` | 否 |
| `namespace` | Namespace | `string` | 否 |
| `cleanup` | Cleanup | `options` | 是 |
| `sourceIdKey` | SourceId Key | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Postgres Record Manager”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## SQLite Record Manager

Use SQLite to keep track of document writes into the vector databases

- 内部名称：`SQLiteRecordManager`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/recordmanager/SQLiteRecordManager/SQLiteRecordManager.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/using-flowise/document-stores)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `databaseFilePath` | Database File Path | `string` | 是 |
| `additionalConfig` | Additional Connection Configuration | `json` | 否 |
| `tableName` | Table Name | `string` | 否 |
| `namespace` | Namespace | `string` | 否 |
| `cleanup` | Cleanup | `options` | 是 |
| `sourceIdKey` | SourceId Key | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“SQLite Record Manager”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
