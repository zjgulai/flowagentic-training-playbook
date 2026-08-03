---
title: "节点目录：Utilities"
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

# 节点目录：Utilities

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 5 个节点。动态参数需以对应版本界面为准。

## Custom JS Function

Execute custom javascript function

- 内部名称：`customFunction`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/utilities/CustomFunction/CustomFunction.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `functionInputVariables` | Input Variables | `json` | 否 |
| `functionName` | Function Name | `string` | 否 |
| `tools` | Additional Tools | `Tool` | 否 |
| `javascriptFunction` | Javascript Function | `code` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `output` | Output | `dynamic` |
| `EndingNode` | Ending Node | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Custom JS Function”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Get Variable

Get variable that was saved using Set Variable node

- 内部名称：`getVariable`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/utilities/GetVariable/GetVariable.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `variableName` | Variable Name | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `output` | Output | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Get Variable”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## IfElse Function

Split flows based on If Else javascript functions

- 内部名称：`ifElseFunction`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/utilities/IfElseFunction/IfElseFunction.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `functionInputVariables` | Input Variables | `json` | 否 |
| `functionName` | IfElse Name | `string` | 否 |
| `ifFunction` | If Function | `code` | 是 |
| `elseFunction` | Else Function | `code` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `returnTrue` | True | `dynamic` |
| `returnFalse` | False | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“IfElse Function”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Set Variable

Set variable which can be retrieved at a later stage. Variable is only available during runtime.

- 内部名称：`setVariable`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/utilities/SetVariable/SetVariable.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `input` | Input | `string \| number \| boolean \| json \| array` | 否 |
| `variableName` | Variable Name | `string` | 是 |
| `showOutput` | Show Output | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `output` | Output | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Set Variable”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

## Sticky Note

Add a sticky note

- 内部名称：`stickyNote`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/utilities/StickyNote/StickyNote.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：未提供分类级官方链接，请以源码锚点和版本界面为准
- 风险：Sticky Note 是画布注释，节点本身不执行外部调用或写入
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `note` | note | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Sticky Note”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
