---
title: "节点目录：Text Splitters"
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

# 节点目录：Text Splitters

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 6 个节点。动态参数需以对应版本界面为准。

## Character Text Splitter

splits only on one type of character (defaults to "\\n\\n").

- 内部名称：`characterTextSplitter`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/CharacterTextSplitter/CharacterTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |
| `separator` | Custom Separator | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Character Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Code Text Splitter

Split documents based on language-specific syntax

- 内部名称：`codeTextSplitter`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/CodeTextSplitter/CodeTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `language` | Language | `options` | 是 |
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Code Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## HtmlToMarkdown Text Splitter

Converts Html to Markdown and then split your content into documents based on the Markdown headers

- 内部名称：`htmlToMarkdownTextSplitter`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/HtmlToMarkdownTextSplitter/HtmlToMarkdownTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“HtmlToMarkdown Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Markdown Text Splitter

Split your content into documents based on the Markdown headers

- 内部名称：`markdownTextSplitter`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/MarkdownTextSplitter/MarkdownTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |
| `splitByHeaders` | Split by Headers | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Markdown Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Recursive Character Text Splitter

Split documents recursively by different characters - starting with "\\n\\n", then "\\n", then " "

- 内部名称：`recursiveCharacterTextSplitter`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/RecursiveCharacterTextSplitter/RecursiveCharacterTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |
| `separators` | Custom Separators | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Recursive Character Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 节点版本或连线类型与当前画布不兼容

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Token Text Splitter

Splits a raw text string by first converting the text into BPE tokens, then split these tokens into chunks and convert the tokens within a single chunk back into text.

- 内部名称：`tokenTextSplitter`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/textsplitters/TokenTextSplitter/TokenTextSplitter.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/text-splitters)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `encodingName` | Encoding Name | `options` | 是 |
| `chunkSize` | Chunk Size | `number` | 否 |
| `chunkOverlap` | Chunk Overlap | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Token Text Splitter”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
