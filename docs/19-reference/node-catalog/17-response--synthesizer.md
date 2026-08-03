---
title: "节点目录：Response Synthesizer"
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

# 节点目录：Response Synthesizer

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 4 个节点。动态参数需以对应版本界面为准。

## Compact and Refine

CompactRefine is a slight variation of Refine that first compacts the text chunks into the smallest possible number of chunks.

- 内部名称：`compactrefineLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/responsesynthesizer/CompactRefine/CompactRefine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `refinePrompt` | Refine Prompt | `string` | 否 |
| `textQAPrompt` | Text QA Prompt | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Compact and Refine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Refine

Create and refine an answer by sequentially going through each retrieved text chunk. This makes a separate LLM call per Node. Good for more detailed answers.

- 内部名称：`refineLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/responsesynthesizer/Refine/Refine.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `refinePrompt` | Refine Prompt | `string` | 否 |
| `textQAPrompt` | Text QA Prompt | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Refine”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Simple Response Builder

Apply a query to a collection of text chunks, gathering the responses in an array, and return a combined string of all responses. Useful for individual queries on each text chunk.

- 内部名称：`simpleResponseBuilderLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/responsesynthesizer/SimpleResponseBuilder/SimpleResponseBuilder.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Simple Response Builder”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## TreeSummarize

Given a set of text chunks and the query, recursively construct a tree and return the root node as the response. Good for summarization purposes.

- 内部名称：`treeSummarizeLlamaIndex`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/responsesynthesizer/TreeSummarize/TreeSummarize.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `prompt` | Prompt | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“TreeSummarize”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
