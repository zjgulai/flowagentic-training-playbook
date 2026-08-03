---
title: "节点目录：Tools"
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

# 节点目录：Tools

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 39 个节点。动态参数需以对应版本界面为准。

## Agent as Tool

Use as a tool to execute another agentflow

- 内部名称：`agentAsTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/AgentAsTool/AgentAsTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`agentflowApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedAgentflow` | Select Agent | `asyncOptions` | 是 |
| `name` | Tool Name | `string` | 是 |
| `description` | Tool Description | `string` | 是 |
| `returnDirect` | Return Direct | `boolean` | 否 |
| `overrideConfig` | Override Config | `json` | 否 |
| `baseURL` | Base URL | `string` | 否 |
| `startNewSession` | Start new session per message | `boolean` | 否 |
| `useQuestionFromChat` | Use Question from Chat | `boolean` | 否 |
| `customInput` | Custom Input | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Agent as Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Arxiv

Search and read content from academic papers on Arxiv

- 内部名称：`arxiv`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Arxiv/Arxiv.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `arxivName` | Name | `string` | 否 |
| `arxivDescription` | Description | `string` | 否 |
| `topKResults` | Top K Results | `number` | 否 |
| `maxQueryLength` | Max Query Length | `number` | 否 |
| `docContentCharsMax` | Max Content Length | `number` | 否 |
| `loadFullContent` | Load Full Content | `boolean` | 否 |
| `continueOnFailure` | Continue On Failure | `boolean` | 否 |
| `legacyBuild` | Use Legacy Build | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Arxiv”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## AWS DynamoDB KV Storage

Store and retrieve versioned text values in AWS DynamoDB

- 内部名称：`awsDynamoDBKVStorage`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/AWSDynamoDBKVStorage/AWSDynamoDBKVStorage.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `region` | AWS Region | `options` | 是 |
| `tableName` | DynamoDB Table | `asyncOptions` | 是 |
| `keyPrefix` | Key Prefix | `string` | 否 |
| `operation` | Operation | `options` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AWS DynamoDB KV Storage”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## AWS SNS

Publish messages to AWS SNS topics

- 内部名称：`awsSNS`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/AWSSNS/AWSSNS.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `region` | AWS Region | `options` | 是 |
| `topicArn` | SNS Topic | `asyncOptions` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“AWS SNS”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## BraveSearch API

Wrapper around BraveSearch API - a real-time API to access Brave search results

- 内部名称：`braveSearchAPI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/BraveSearchAPI/BraveSearchAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`braveSearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“BraveSearch API”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Calculator

Perform calculations on response

- 内部名称：`calculator`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Calculator/Calculator.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
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

**隔离环境示例：** 在隔离培训画布中添加“Calculator”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Chain Tool

Use a chain as allowed tool for agent

- 内部名称：`chainTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/ChainTool/ChainTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `name` | Chain Name | `string` | 是 |
| `description` | Chain Description | `string` | 是 |
| `returnDirect` | Return Direct | `boolean` | 否 |
| `baseChain` | Base Chain | `BaseChain` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Chain Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Chatflow Tool

Use as a tool to execute another chatflow

- 内部名称：`ChatflowTool`
- 版本：`5.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/ChatflowTool/ChatflowTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`chatflowApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedChatflow` | Select Chatflow | `asyncOptions` | 是 |
| `name` | Tool Name | `string` | 是 |
| `description` | Tool Description | `string` | 是 |
| `returnDirect` | Return Direct | `boolean` | 否 |
| `overrideConfig` | Override Config | `json` | 否 |
| `baseURL` | Base URL | `string` | 否 |
| `startNewSession` | Start new session per message | `boolean` | 否 |
| `useQuestionFromChat` | Use Question from Chat | `boolean` | 否 |
| `customInput` | Custom Input | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Chatflow Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Code Interpreter by E2B

Execute code in a sandbox environment

- 内部名称：`codeInterpreterE2B`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/CodeInterpreterE2B/CodeInterpreterE2B.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`E2BApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `toolName` | Tool Name | `string` | 是 |
| `toolDesc` | Tool Description | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Code Interpreter by E2B”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Composio

Toolset with over 250+ Apps for building AI-powered applications

- 内部名称：`composio`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Composio/Composio.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`composioApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `appName` | App Name | `asyncOptions` | 是 |
| `connectedAccountId` | Connected Account | `asyncOptions` | 是 |
| `actions` | Actions to Use | `asyncMultiOptions` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Composio”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## CurrentDateTime

Get todays day, date and time.

- 内部名称：`currentDateTime`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/CurrentDateTime/CurrentDateTime.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
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

**隔离环境示例：** 在隔离培训画布中添加“CurrentDateTime”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Custom Tool

Use custom tool you've created in Flowise within chatflow

- 内部名称：`customTool`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/CustomTool/CustomTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedTool` | Select Tool | `asyncOptions` | 是 |
| `returnDirect` | Return Direct | `boolean` | 否 |
| `customToolName` | Custom Tool Name | `string` | 是 |
| `customToolDesc` | Custom Tool Description | `string` | 是 |
| `customToolSchema` | Custom Tool Schema | `string` | 是 |
| `customToolFunc` | Custom Tool Func | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Custom Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Exa Search

Wrapper around Exa Search API - search engine fully designed for use by LLMs

- 内部名称：`exaSearch`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/ExaSearch/ExaSearch.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`exaSearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `description` | Tool Description | `string` | 是 |
| `numResults` | Num of Results | `number` | 否 |
| `type` | Search Type | `options` | 否 |
| `useAutoprompt` | Use Auto Prompt | `boolean` | 否 |
| `category` | Category (Beta) | `options` | 否 |
| `includeDomains` | Include Domains | `string` | 否 |
| `excludeDomains` | Exclude Domains | `string` | 否 |
| `startCrawlDate` | Start Crawl Date | `string` | 否 |
| `endCrawlDate` | End Crawl Date | `string` | 否 |
| `startPublishedDate` | Start Published Date | `string` | 否 |
| `endPublishedDate` | End Published Date | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Exa Search”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Gmail

Perform Gmail operations for drafts, messages, labels, and threads

- 内部名称：`gmail`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Gmail/Gmail.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`gmailOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `gmailType` | Type | `options` | 是 |
| `draftActions` | Draft Actions | `multiOptions` | 是 |
| `messageActions` | Message Actions | `multiOptions` | 是 |
| `labelActions` | Label Actions | `multiOptions` | 是 |
| `threadActions` | Thread Actions | `multiOptions` | 是 |
| `draftMaxResults` | Max Results | `number` | 否 |
| `draftTo` | To | `string` | 否 |
| `draftSubject` | Subject | `string` | 否 |
| `draftBody` | Body | `string` | 否 |
| `draftCc` | CC | `string` | 否 |
| `draftBcc` | BCC | `string` | 否 |
| `draftId` | Draft ID | `string` | 否 |
| `draftUpdateTo` | To (Update) | `string` | 否 |
| `draftUpdateSubject` | Subject (Update) | `string` | 否 |
| `draftUpdateBody` | Body (Update) | `string` | 否 |
| `messageMaxResults` | Max Results | `number` | 否 |
| `messageQuery` | Query | `string` | 否 |
| `messageTo` | To | `string` | 否 |
| `messageSubject` | Subject | `string` | 否 |
| `messageBody` | Body | `string` | 否 |
| `messageCc` | CC | `string` | 否 |
| `messageBcc` | BCC | `string` | 否 |
| `messageId` | Message ID | `string` | 否 |
| `messageAddLabelIds` | Add Label IDs | `string` | 否 |
| `messageRemoveLabelIds` | Remove Label IDs | `string` | 否 |
| `labelName` | Label Name | `string` | 否 |
| `labelColor` | Label Color | `string` | 否 |
| `labelId` | Label ID | `string` | 否 |
| `threadMaxResults` | Max Results | `number` | 否 |
| `threadQuery` | Query | `string` | 否 |
| `threadId` | Thread ID | `string` | 否 |
| `threadAddLabelIds` | Add Label IDs | `string` | 否 |
| `threadRemoveLabelIds` | Remove Label IDs | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Gmail”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Calendar

Perform Google Calendar operations such as managing events, calendars, and checking availability

- 内部名称：`googleCalendarTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/GoogleCalendar/GoogleCalendar.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：`googleCalendarOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `calendarType` | Type | `options` | 是 |
| `eventActions` | Event Actions | `multiOptions` | 是 |
| `calendarActions` | Calendar Actions | `multiOptions` | 是 |
| `freebusyActions` | Freebusy Actions | `multiOptions` | 是 |
| `calendarId` | Calendar ID | `string` | 否 |
| `eventId` | Event ID | `string` | 否 |
| `summary` | Summary | `string` | 否 |
| `description` | Description | `string` | 否 |
| `location` | Location | `string` | 否 |
| `startDateTime` | Start Date Time | `string` | 否 |
| `endDateTime` | End Date Time | `string` | 否 |
| `timeZone` | Time Zone | `string` | 否 |
| `allDay` | All Day Event | `boolean` | 否 |
| `startDate` | Start Date | `string` | 否 |
| `endDate` | End Date | `string` | 否 |
| `attendees` | Attendees | `string` | 否 |
| `sendUpdates` | Send Updates to | `options` | 否 |
| `recurrence` | Recurrence Rules | `string` | 否 |
| `reminderMinutes` | Reminder Minutes | `number` | 否 |
| `visibility` | Visibility | `options` | 否 |
| `quickAddText` | Quick Add Text | `string` | 否 |
| `timeMin` | Time Min | `string` | 否 |
| `timeMax` | Time Max | `string` | 否 |
| `maxResults` | Max Results | `number` | 否 |
| `singleEvents` | Single Events | `boolean` | 否 |
| `orderBy` | Order By | `options` | 否 |
| `query` | Query | `string` | 否 |
| `calendarIdForCalendar` | Calendar ID | `string` | 否 |
| `calendarSummary` | Calendar Summary | `string` | 否 |
| `calendarDescription` | Calendar Description | `string` | 否 |
| `calendarLocation` | Calendar Location | `string` | 否 |
| `calendarTimeZone` | Calendar Time Zone | `string` | 否 |
| `showHidden` | Show Hidden | `boolean` | 否 |
| `minAccessRole` | Min Access Role | `options` | 否 |
| `freebusyTimeMin` | Time Min | `string` | 否 |
| `freebusyTimeMax` | Time Max | `string` | 否 |
| `calendarIds` | Calendar IDs | `string` | 否 |
| `groupExpansionMax` | Group Expansion Max | `number` | 否 |
| `calendarExpansionMax` | Calendar Expansion Max | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Calendar”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Custom Search

Wrapper around Google Custom Search API - a real-time API to access Google search results

- 内部名称：`googleCustomSearch`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/GoogleSearchAPI/GoogleSearchAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：`googleCustomSearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Custom Search”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Docs

Perform Google Docs operations such as creating, reading, updating, and deleting documents, as well as text manipulation

- 内部名称：`googleDocsTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/GoogleDocs/GoogleDocs.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：`googleDocsOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `actions` | Actions | `multiOptions` | 是 |
| `documentId` | Document ID | `string` | 否 |
| `title` | Title | `string` | 否 |
| `text` | Text | `string` | 否 |
| `index` | Index | `number` | 否 |
| `replaceText` | Replace Text | `string` | 否 |
| `newText` | New Text | `string` | 否 |
| `matchCase` | Match Case | `boolean` | 否 |
| `imageUrl` | Image URL | `string` | 否 |
| `rows` | Table Rows | `number` | 否 |
| `columns` | Table Columns | `number` | 否 |
| `includeTabsContent` | Include Tabs Content | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Docs”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Drive

Perform Google Drive operations such as managing files, folders, sharing, and searching

- 内部名称：`googleDriveTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/GoogleDrive/GoogleDrive.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：`googleDriveOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `driveType` | Type | `options` | 是 |
| `fileActions` | File Actions | `multiOptions` | 是 |
| `folderActions` | Folder Actions | `multiOptions` | 是 |
| `searchActions` | Search Actions | `multiOptions` | 是 |
| `shareActions` | Share Actions | `multiOptions` | 是 |
| `fileId` | File ID | `string` | 否 |
| `fileId` | File ID | `string` | 否 |
| `folderId` | Folder ID | `string` | 否 |
| `permissionId` | Permission ID | `string` | 否 |
| `fileName` | File Name | `string` | 否 |
| `fileName` | Folder Name | `string` | 否 |
| `fileContent` | File Content | `string` | 否 |
| `mimeType` | MIME Type | `string` | 否 |
| `parentFolderId` | Parent Folder ID | `string` | 否 |
| `parentFolderId` | Parent Folder ID | `string` | 否 |
| `description` | File Description | `string` | 否 |
| `description` | Folder Description | `string` | 否 |
| `searchQuery` | Search Query | `string` | 否 |
| `maxResults` | Max Results | `number` | 否 |
| `maxResults` | Max Results | `number` | 否 |
| `orderBy` | Order By | `options` | 否 |
| `orderBy` | Order By | `options` | 否 |
| `shareRole` | Share Role | `options` | 否 |
| `shareType` | Share Type | `options` | 否 |
| `emailAddress` | Email Address | `string` | 否 |
| `domainName` | Domain Name | `string` | 否 |
| `sendNotificationEmail` | Send Notification Email | `boolean` | 否 |
| `emailMessage` | Email Message | `string` | 否 |
| `includeItemsFromAllDrives` | Include Items From All Drives | `boolean` | 否 |
| `includeItemsFromAllDrives` | Include Items From All Drives | `boolean` | 否 |
| `supportsAllDrives` | Supports All Drives | `boolean` | 否 |
| `supportsAllDrives` | Supports All Drives | `boolean` | 否 |
| `supportsAllDrives` | Supports All Drives | `boolean` | 否 |
| `supportsAllDrives` | Supports All Drives | `boolean` | 否 |
| `fields` | Fields | `string` | 否 |
| `acknowledgeAbuse` | Acknowledge Abuse | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Drive”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Google Sheets

Perform Google Sheets operations such as managing spreadsheets, reading and writing values

- 内部名称：`googleSheetsTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/GoogleSheets/GoogleSheets.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：是；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`yes`
- 凭据：`googleSheetsOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `sheetsType` | Type | `options` | 是 |
| `spreadsheetActions` | Spreadsheet Actions | `multiOptions` | 是 |
| `valuesActions` | Values Actions | `multiOptions` | 是 |
| `spreadsheetId` | Spreadsheet ID | `string` | 否 |
| `title` | Title | `string` | 否 |
| `sheetCount` | Sheet Count | `number` | 否 |
| `range` | Range | `string` | 否 |
| `ranges` | Ranges | `string` | 否 |
| `values` | Values | `string` | 否 |
| `valueInputOption` | Value Input Option | `options` | 否 |
| `valueRenderOption` | Value Render Option | `options` | 否 |
| `dateTimeRenderOption` | Date Time Render Option | `options` | 否 |
| `insertDataOption` | Insert Data Option | `options` | 否 |
| `includeGridData` | Include Grid Data | `boolean` | 否 |
| `majorDimension` | Major Dimension | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Google Sheets”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Jira

Perform Jira operations for issues, comments, and users

- 内部名称：`jiraTool`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Jira/Jira.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`jiraApi`, `jiraApiBearerToken`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `jiraHost` | Host | `string` | 是 |
| `enableSSL` | Enable SSL Certificate | `boolean` | 否 |
| `caFile` | SSL Certificate | `file` | 否 |
| `jiraType` | Type | `options` | 是 |
| `issueActions` | Issue Actions | `multiOptions` | 是 |
| `commentActions` | Comment Actions | `multiOptions` | 是 |
| `userActions` | User Actions | `multiOptions` | 是 |
| `projectKey` | Project Key | `string` | 否 |
| `issueType` | Issue Type | `string` | 否 |
| `issueSummary` | Summary | `string` | 否 |
| `issueDescription` | Description | `string` | 否 |
| `issuePriority` | Priority | `string` | 否 |
| `issueKey` | Issue Key | `string` | 否 |
| `assigneeAccountId` | Assignee Account ID | `string` | 否 |
| `transitionId` | Transition ID | `string` | 否 |
| `jqlQuery` | JQL Query | `string` | 否 |
| `issueMaxResults` | Max Results | `number` | 否 |
| `commentIssueKey` | Issue Key (for Comments) | `string` | 否 |
| `commentText` | Comment Text | `string` | 否 |
| `commentId` | Comment ID | `string` | 否 |
| `userQuery` | Search Query | `string` | 否 |
| `userAccountId` | Account ID | `string` | 否 |
| `userEmail` | Email Address | `string` | 否 |
| `userDisplayName` | Display Name | `string` | 否 |
| `userMaxResults` | User Max Results | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Jira”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## JSON Path Extractor

Extract values from JSON using path expressions

- 内部名称：`jsonPathExtractor`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/JSONPathExtractor/JSONPathExtractor.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `path` | JSON Path | `string` | 是 |
| `returnNullOnError` | Return Null on Error | `boolean` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“JSON Path Extractor”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Microsoft Outlook

Perform Microsoft Outlook operations for calendars, events, and messages

- 内部名称：`microsoftOutlook`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/MicrosoftOutlook/MicrosoftOutlook.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`microsoftOutlookOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `outlookType` | Type | `options` | 是 |
| `calendarActions` | Calendar Actions | `multiOptions` | 是 |
| `messageActions` | Message Actions | `multiOptions` | 是 |
| `maxResultsListCalendars` | Max Results [List Calendars] | `number` | 否 |
| `calendarIdGetCalendar` | Calendar ID [Get Calendar] | `string` | 否 |
| `calendarNameCreateCalendar` | Calendar Name [Create Calendar] | `string` | 否 |
| `calendarIdUpdateCalendar` | Calendar ID [Update Calendar] | `string` | 否 |
| `calendarNameUpdateCalendar` | Calendar Name [Update Calendar] | `string` | 否 |
| `calendarIdDeleteCalendar` | Calendar ID [Delete Calendar] | `string` | 否 |
| `calendarIdListEvents` | Calendar ID [List Events] | `string` | 否 |
| `maxResultsListEvents` | Max Results [List Events] | `number` | 否 |
| `startDateTimeListEvents` | Start Date Time [List Events] | `string` | 否 |
| `endDateTimeListEvents` | End Date Time [List Events] | `string` | 否 |
| `eventIdGetEvent` | Event ID [Get Event] | `string` | 否 |
| `subjectCreateEvent` | Subject [Create Event] | `string` | 否 |
| `bodyCreateEvent` | Body [Create Event] | `string` | 否 |
| `startDateTimeCreateEvent` | Start Date Time [Create Event] | `string` | 否 |
| `endDateTimeCreateEvent` | End Date Time [Create Event] | `string` | 否 |
| `timeZoneCreateEvent` | Time Zone [Create Event] | `string` | 否 |
| `locationCreateEvent` | Location [Create Event] | `string` | 否 |
| `attendeesCreateEvent` | Attendees [Create Event] | `string` | 否 |
| `eventIdUpdateEvent` | Event ID [Update Event] | `string` | 否 |
| `subjectUpdateEvent` | Subject [Update Event] | `string` | 否 |
| `eventIdDeleteEvent` | Event ID [Delete Event] | `string` | 否 |
| `maxResultsListMessages` | Max Results [List Messages] | `number` | 否 |
| `filterListMessages` | Filter [List Messages] | `string` | 否 |
| `messageIdGetMessage` | Message ID [Get Message] | `string` | 否 |
| `toCreateDraftMessage` | To [Create Draft Message] | `string` | 否 |
| `subjectCreateDraftMessage` | Subject [Create Draft Message] | `string` | 否 |
| `bodyCreateDraftMessage` | Body [Create Draft Message] | `string` | 否 |
| `ccCreateDraftMessage` | CC [Create Draft Message] | `string` | 否 |
| `bccCreateDraftMessage` | BCC [Create Draft Message] | `string` | 否 |
| `toSendMessage` | To [Send Message] | `string` | 否 |
| `subjectSendMessage` | Subject [Send Message] | `string` | 否 |
| `bodySendMessage` | Body [Send Message] | `string` | 否 |
| `messageIdUpdateMessage` | Message ID [Update Message] | `string` | 否 |
| `isReadUpdateMessage` | Is Read [Update Message] | `boolean` | 否 |
| `messageIdDeleteMessage` | Message ID [Delete Message] | `string` | 否 |
| `messageIdCopyMessage` | Message ID [Copy Message] | `string` | 否 |
| `destinationFolderIdCopyMessage` | Destination Folder ID [Copy Message] | `string` | 否 |
| `messageIdMoveMessage` | Message ID [Move Message] | `string` | 否 |
| `destinationFolderIdMoveMessage` | Destination Folder ID [Move Message] | `string` | 否 |
| `messageIdReplyMessage` | Message ID [Reply Message] | `string` | 否 |
| `replyBodyReplyMessage` | Reply Body [Reply Message] | `string` | 否 |
| `messageIdForwardMessage` | Message ID [Forward Message] | `string` | 否 |
| `forwardToForwardMessage` | Forward To [Forward Message] | `string` | 否 |
| `forwardCommentForwardMessage` | Forward Comment [Forward Message] | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Microsoft Outlook”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Microsoft Teams

Perform Microsoft Teams operations for channels, chats, and chat messages

- 内部名称：`microsoftTeams`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/MicrosoftTeams/MicrosoftTeams.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`microsoftTeamsOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `teamsType` | Type | `options` | 是 |
| `channelActions` | Channel Actions | `multiOptions` | 是 |
| `chatActions` | Chat Actions | `multiOptions` | 是 |
| `chatMessageActions` | Chat Message Actions | `multiOptions` | 是 |
| `teamIdListChannels` | Team ID [List Channels] | `string` | 否 |
| `maxResultsListChannels` | Max Results [List Channels] | `number` | 否 |
| `teamIdGetChannel` | Team ID [Get Channel] | `string` | 否 |
| `channelIdGetChannel` | Channel ID [Get Channel] | `string` | 否 |
| `teamIdCreateChannel` | Team ID [Create Channel] | `string` | 否 |
| `displayNameCreateChannel` | Display Name [Create Channel] | `string` | 否 |
| `descriptionCreateChannel` | Description [Create Channel] | `string` | 否 |
| `membershipTypeCreateChannel` | Membership Type [Create Channel] | `options` | 否 |
| `teamIdUpdateChannel` | Team ID [Update Channel] | `string` | 否 |
| `channelIdUpdateChannel` | Channel ID [Update Channel] | `string` | 否 |
| `displayNameUpdateChannel` | Display Name [Update Channel] | `string` | 否 |
| `teamIdDeleteChannel` | Team ID [Delete/Archive Channel] | `string` | 否 |
| `channelIdDeleteChannel` | Channel ID [Delete/Archive Channel] | `string` | 否 |
| `teamIdChannelMembers` | Team ID [Channel Members] | `string` | 否 |
| `channelIdChannelMembers` | Channel ID [Channel Members] | `string` | 否 |
| `userIdChannelMember` | User ID [Add/Remove Channel Member] | `string` | 否 |
| `maxResultsListChats` | Max Results [List Chats] | `number` | 否 |
| `chatIdGetChat` | Chat ID [Get Chat] | `string` | 否 |
| `chatTypeCreateChat` | Chat Type [Create Chat] | `options` | 否 |
| `topicCreateChat` | Topic [Create Chat] | `string` | 否 |
| `membersCreateChat` | Members [Create Chat] | `string` | 否 |
| `chatIdUpdateChat` | Chat ID [Update Chat] | `string` | 否 |
| `topicUpdateChat` | Topic [Update Chat] | `string` | 否 |
| `chatIdDeleteChat` | Chat ID [Delete Chat] | `string` | 否 |
| `chatIdChatMembers` | Chat ID [Chat Members] | `string` | 否 |
| `userIdChatMember` | User ID [Add/Remove Chat Member] | `string` | 否 |
| `chatIdPinMessage` | Chat ID [Pin/Unpin Message] | `string` | 否 |
| `messageIdPinMessage` | Message ID [Pin/Unpin Message] | `string` | 否 |
| `chatChannelIdListMessages` | Chat/Channel ID [List Messages] | `string` | 否 |
| `teamIdListMessages` | Team ID [List Messages - Channel Only] | `string` | 否 |
| `maxResultsListMessages` | Max Results [List Messages] | `number` | 否 |
| `chatChannelIdGetMessage` | Chat/Channel ID [Get Message] | `string` | 否 |
| `teamIdGetMessage` | Team ID [Get Message - Channel Only] | `string` | 否 |
| `messageIdGetMessage` | Message ID [Get Message] | `string` | 否 |
| `chatChannelIdSendMessage` | Chat/Channel ID [Send Message] | `string` | 否 |
| `teamIdSendMessage` | Team ID [Send Message - Channel Only] | `string` | 否 |
| `messageBodySendMessage` | Message Body [Send Message] | `string` | 否 |
| `contentTypeSendMessage` | Content Type [Send Message] | `options` | 否 |
| `chatChannelIdUpdateMessage` | Chat/Channel ID [Update Message] | `string` | 否 |
| `teamIdUpdateMessage` | Team ID [Update Message - Channel Only] | `string` | 否 |
| `messageIdUpdateMessage` | Message ID [Update Message] | `string` | 否 |
| `chatChannelIdDeleteMessage` | Chat/Channel ID [Delete Message] | `string` | 否 |
| `teamIdDeleteMessage` | Team ID [Delete Message - Channel Only] | `string` | 否 |
| `messageIdDeleteMessage` | Message ID [Delete Message] | `string` | 否 |
| `chatChannelIdReplyMessage` | Chat/Channel ID [Reply to Message] | `string` | 否 |
| `teamIdReplyMessage` | Team ID [Reply to Message - Channel Only] | `string` | 否 |
| `messageIdReplyMessage` | Message ID [Reply to Message] | `string` | 否 |
| `replyBodyReplyMessage` | Reply Body [Reply to Message] | `string` | 否 |
| `chatChannelIdReaction` | Chat/Channel ID [Set/Unset Reaction] | `string` | 否 |
| `teamIdReaction` | Team ID [Set/Unset Reaction - Channel Only] | `string` | 否 |
| `messageIdReaction` | Message ID [Set/Unset Reaction] | `string` | 否 |
| `reactionTypeSetReaction` | Reaction Type [Set Reaction] | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Microsoft Teams”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## OpenAPI Toolkit

Load OpenAPI specification, and converts each API endpoint to a tool

- 内部名称：`openAPIToolkit`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/OpenAPIToolkit/OpenAPIToolkit.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `inputType` | Input Type | `options` | 是 |
| `openApiFile` | OpenAPI File | `file` | 是 |
| `openApiLink` | OpenAPI Link | `string` | 是 |
| `selectedServer` | Server | `asyncOptions` | 是 |
| `selectedEndpoints` | Available Endpoints | `asyncMultiOptions` | 是 |
| `returnDirect` | Return Direct | `boolean` | 否 |
| `headers` | Headers | `json` | 否 |
| `removeNulls` | Remove null parameters | `boolean` | 否 |
| `customCode` | Custom Code | `code` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“OpenAPI Toolkit”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## QueryEngine Tool

Tool used to invoke query engine

- 内部名称：`queryEngineToolLlamaIndex`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/QueryEngineTool/QueryEngineTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `baseQueryEngine` | Base QueryEngine | `BaseQueryEngine` | 是 |
| `toolName` | Tool Name | `string` | 是 |
| `toolDesc` | Tool Description | `string` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“QueryEngine Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Requests Delete

Execute HTTP DELETE requests

- 内部名称：`requestsDelete`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/RequestsDelete/RequestsDelete.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `requestsDeleteUrl` | URL | `string` | 是 |
| `requestsDeleteName` | Name | `string` | 否 |
| `requestsDeleteDescription` | Description | `string` | 否 |
| `requestsDeleteHeaders` | Headers | `string` | 否 |
| `requestsDeleteQueryParamsSchema` | Query Params Schema | `code` | 否 |
| `requestsDeleteMaxOutputLength` | Max Output Length | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Requests Delete”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Requests Get

Execute HTTP GET requests

- 内部名称：`requestsGet`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/RequestsGet/RequestsGet.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `requestsGetUrl` | URL | `string` | 是 |
| `requestsGetName` | Name | `string` | 否 |
| `requestsGetDescription` | Description | `string` | 否 |
| `requestsGetHeaders` | Headers | `string` | 否 |
| `requestsGetQueryParamsSchema` | Query Params Schema | `code` | 否 |
| `requestsGetMaxOutputLength` | Max Output Length | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Requests Get”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Requests Post

Execute HTTP POST requests

- 内部名称：`requestsPost`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/RequestsPost/RequestsPost.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `requestsPostUrl` | URL | `string` | 是 |
| `requestsPostName` | Name | `string` | 否 |
| `requestsPostDescription` | Description | `string` | 否 |
| `requestsPostHeaders` | Headers | `string` | 否 |
| `requestPostBody` | Body | `string` | 否 |
| `requestsPostBodySchema` | Body Schema | `code` | 否 |
| `requestsPostMaxOutputLength` | Max Output Length | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Requests Post”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Requests Put

Execute HTTP PUT requests

- 内部名称：`requestsPut`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/RequestsPut/RequestsPut.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `requestsPutUrl` | URL | `string` | 是 |
| `requestsPutName` | Name | `string` | 否 |
| `requestsPutDescription` | Description | `string` | 否 |
| `requestsPutHeaders` | Headers | `string` | 否 |
| `requestPutBody` | Body | `string` | 否 |
| `requestsPutBodySchema` | Body Schema | `code` | 否 |
| `requestsPutMaxOutputLength` | Max Output Length | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Requests Put”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Retriever Tool

Use a retriever as allowed tool for agent

- 内部名称：`retrieverTool`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/RetrieverTool/RetrieverTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `name` | Retriever Name | `string` | 是 |
| `description` | Retriever Description | `string` | 是 |
| `retriever` | Retriever | `BaseRetriever` | 是 |
| `returnSourceDocuments` | Return Source Documents | `boolean` | 否 |
| `retrieverToolMetadataFilter` | Additional Metadata Filter | `json` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Retriever Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## SearchApi

Real-time API for accessing Google Search data

- 内部名称：`searchAPI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/SearchApi/SearchAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`searchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“SearchApi”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## SearXNG

Wrapper around SearXNG - a free internet metasearch engine

- 内部名称：`searXNG`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Searxng/Searxng.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `apiBase` | Base URL | `string` | 是 |
| `toolName` | Tool Name | `string` | 是 |
| `toolDescription` | Tool Description | `string` | 是 |
| `headers` | Headers | `json` | 否 |
| `format` | Format | `options` | 是 |
| `categories` | Categories | `string` | 否 |
| `engines` | Engines | `string` | 否 |
| `language` | Language | `string` | 否 |
| `pageno` | Page No. | `number` | 否 |
| `time_range` | Time Range | `string` | 否 |
| `safesearch` | Safe Search | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“SearXNG”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Serp API

Wrapper around SerpAPI - a real-time API to access Google search results

- 内部名称：`serpAPI`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/SerpAPI/SerpAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`serpApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Serp API”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Serper

Wrapper around Serper.dev - Google Search API

- 内部名称：`serper`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/Serper/Serper.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`serperApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Serper”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## StripeAgentTool

Use Stripe Agent function calling for financial transactions

- 内部名称：`stripeAgentTool`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/StripeTool/StripeTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`stripeApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `paymentLinks` | Payment Links | `multiOptions` | 否 |
| `products` | Products | `multiOptions` | 否 |
| `prices` | Prices | `multiOptions` | 否 |
| `balance` | Balance | `multiOptions` | 否 |
| `invoiceItems` | Invoice Items | `multiOptions` | 否 |
| `invoices` | Invoices | `multiOptions` | 否 |
| `customers` | Customers | `multiOptions` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“StripeAgentTool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Tavily API

Wrapper around TavilyAPI - A specialized search engine designed for LLMs and AI agents

- 内部名称：`tavilyAPI`
- 版本：`1.2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/TavilyAPI/TavilyAPI.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`tavilyApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `topic` | Topic | `options` | 否 |
| `searchDepth` | Search Depth | `options` | 否 |
| `chunksPerSource` | Chunks Per Source | `number` | 否 |
| `maxResults` | Max Results | `number` | 否 |
| `timeRange` | Time Range | `options` | 否 |
| `days` | Days | `number` | 否 |
| `includeAnswer` | Include Answer | `boolean` | 否 |
| `includeRawContent` | Include Raw Content | `boolean` | 否 |
| `includeImages` | Include Images | `boolean` | 否 |
| `includeImageDescriptions` | Include Image Descriptions | `boolean` | 否 |
| `includeDomains` | Include Domains | `string` | 否 |
| `excludeDomains` | Exclude Domains | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Tavily API”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Web Browser

Gives agent the ability to visit a website and extract information

- 内部名称：`webBrowser`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/WebBrowser/WebBrowser.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `model` | Language Model | `BaseLanguageModel` | 是 |
| `embeddings` | Embeddings | `Embeddings` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Web Browser”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## Web Scraper Tool

Scrapes web pages recursively by following links OR by fetching URLs from the default sitemap.

- 内部名称：`webScraperTool`
- 版本：`1.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/WebScraperTool/WebScraperTool.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `scrapeMode` | Scraping Mode | `options` | 是 |
| `maxDepth` | Max Depth | `number` | 否 |
| `maxPages` | Max Pages | `number` | 否 |
| `timeoutS` | Timeout (s) | `number` | 否 |
| `description` | Tool Description | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“Web Scraper Tool”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准

## WolframAlpha

Wrapper around WolframAlpha - a powerful computational knowledge engine

- 内部名称：`wolframAlpha`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/tools/WolframAlpha/WolframAlpha.ts@6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/tools)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：`wolframAlphaAppId`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| — | 未静态解析到参数 | — | — |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| — | 源码未静态声明 `outputs`；运行输出以版本界面与执行记录为准 | — |

**隔离环境示例：** 在隔离培训画布中添加“WolframAlpha”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    源码未静态声明 outputs；运行输出以对应版本界面与执行记录为准
