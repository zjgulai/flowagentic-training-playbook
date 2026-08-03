---
title: "节点目录：outputparsers"
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

# 节点目录：outputparsers

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 4 个节点。动态参数需以对应版本界面为准。

## Advanced Structured Output Parser

Parse the output of an LLM call into a given structure by providing a Zod schema.

- 内部名称：`advancedStructuredOutputParser`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/outputparsers/StructuredOutputParserAdvanced/StructuredOutputParserAdvanced.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/output-parsers)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `autofixParser` | Autofix | `boolean` | 否 |
| `exampleJson` | Example JSON | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Advanced Structured Output Parser”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## CSV Output Parser

Parse the output of an LLM call as a comma-separated list of values

- 内部名称：`csvOutputParser`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/outputparsers/CSVListOutputParser/CSVListOutputParser.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/output-parsers)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `autofixParser` | Autofix | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“CSV Output Parser”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Custom List Output Parser

Parse the output of an LLM call as a list of values.

- 内部名称：`customListOutputParser`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/outputparsers/CustomListOutputParser/CustomListOutputParser.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/output-parsers)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `length` | Length | `number` | 否 |
| `separator` | Separator | `string` | 否 |
| `autofixParser` | Autofix | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Custom List Output Parser”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Structured Output Parser

Parse the output of an LLM call into a given (JSON) structure.

- 内部名称：`structuredOutputParser`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/outputparsers/StructuredOutputParser/StructuredOutputParser.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/output-parsers)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `autofixParser` | Autofix | `boolean` | 否 |
| `jsonStructure` | JSON Structure | `datagrid` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Structured Output Parser”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
