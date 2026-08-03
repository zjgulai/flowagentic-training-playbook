---
title: "节点目录：Prompts"
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

# 节点目录：Prompts

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 4 个节点。动态参数需以对应版本界面为准。

## Chat Prompt Template

Schema to represent a chat prompt

- 内部名称：`chatPromptTemplate`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/prompts/ChatPromptTemplate/ChatPromptTemplate.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/prompts)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `systemMessagePrompt` | System Message | `string` | 是 |
| `humanMessagePrompt` | Human Message | `string` | 是 |
| `promptValues` | Format Prompt Values | `json` | 否 |
| `messageHistory` | Messages History | `tabs` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Chat Prompt Template”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Few Shot Prompt Template

Prompt template you can build with examples

- 内部名称：`fewShotPromptTemplate`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/prompts/FewShotPromptTemplate/FewShotPromptTemplate.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/prompts)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `examples` | Examples | `string` | 是 |
| `examplePrompt` | Example Prompt | `PromptTemplate` | 是 |
| `prefix` | Prefix | `string` | 是 |
| `suffix` | Suffix | `string` | 是 |
| `exampleSeparator` | Example Separator | `string` | 是 |
| `templateFormat` | Template Format | `options` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Few Shot Prompt Template”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## LangFuse Prompt Template

Fetch schema from LangFuse to represent a prompt for an LLM

- 内部名称：`promptLangFuse`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/prompts/PromptLangfuse/PromptLangfuse.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/prompts)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：`langfuseApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `template` | Prompt Name | `string` | 是 |
| `promptValues` | Format Prompt Values | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“LangFuse Prompt Template”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Prompt Template

Schema to represent a basic prompt for an LLM

- 内部名称：`promptTemplate`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/prompts/PromptTemplate/PromptTemplate.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/prompts)
- 风险：外部调用：否；可能计费：否；可能写入：否
  - 外部调用：`no`
  - 可能计费：`no`
  - 可能写入：`no`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `template` | Template | `string` | 是 |
| `promptValues` | Format Prompt Values | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Prompt Template”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
