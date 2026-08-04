---
title: "节点目录：Graph"
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

# 节点目录：Graph

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 1 个节点。动态参数需以对应版本界面为准。

## Neo4j

Connect with Neo4j graph database

- 内部名称：`Neo4j`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/graphs/Neo4j/Neo4j.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`neo4jApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `database` | Database | `string` | 否 |
| `timeoutMs` | Timeout (ms) | `number` | 否 |
| `enhancedSchema` | Enhanced Schema | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Neo4j”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
