---
title: "节点目录：Document Loaders"
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

# 节点目录：Document Loaders

本页由 `static-ts-metadata-v2` 从固定提交只读生成，共 41 个节点。动态参数需以对应版本界面为准。

## Airtable

Load data from Airtable table

- 内部名称：`airtable`
- 版本：`3.02`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Airtable/Airtable.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`airtableApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `baseId` | Base Id | `string` | 是 |
| `tableId` | Table Id | `string` | 是 |
| `viewId` | View Id | `string` | 否 |
| `fields` | Include Only Fields | `string` | 否 |
| `returnAll` | Return All | `boolean` | 否 |
| `limit` | Limit | `number` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |
| `filterByFormula` | Filter By Formula | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Airtable”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## API Loader

Load data from an API

- 内部名称：`apiLoader`
- 版本：`2.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/API/APILoader.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `method` | Method | `options` | 是 |
| `url` | URL | `string` | 是 |
| `headers` | Headers | `json` | 否 |
| `caFile` | SSL Certificate | `file` | 否 |
| `body` | Body | `json` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“API Loader”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Apify Website Content Crawler

Load data from Apify Website Content Crawler

- 内部名称：`apifyWebsiteContentCrawler`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/ApifyWebsiteContentCrawler/ApifyWebsiteContentCrawler.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`apifyApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `urls` | Start URLs | `string` | 是 |
| `crawlerType` | Crawler type | `options` | 是 |
| `maxCrawlDepth` | Max crawling depth | `number` | 否 |
| `maxCrawlPages` | Max crawl pages | `number` | 否 |
| `additionalInput` | Additional input | `json` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Apify Website Content Crawler”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## BraveSearch API Document Loader

Load and process data from BraveSearch results

- 内部名称：`braveSearchApiLoader`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/BraveSearchAPI/BraveSearchAPI.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`braveSearchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `query` | Query | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“BraveSearch API Document Loader”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Cheerio Web Scraper

Load data from webpages

- 内部名称：`cheerioWebScraper`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Cheerio/Cheerio.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `url` | URL | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `relativeLinksMethod` | Get Relative Links Method | `options` | 否 |
| `limit` | Get Relative Links Limit | `number` | 否 |
| `selector` | Selector (CSS) | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Cheerio Web Scraper”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Confluence

Load data from a Confluence Document

- 内部名称：`confluence`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Confluence/Confluence.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`confluenceCloudApi`, `confluenceServerDCApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `baseUrl` | Base URL | `string` | 是 |
| `spaceKey` | Space Key | `string` | 是 |
| `limit` | Limit | `number` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Confluence”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Csv File

Load data from CSV files

- 内部名称：`csvFile`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Csv/Csv.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `csvFile` | Csv File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `columnName` | Single Column Extraction | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Csv File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Custom Document Loader

Custom function for loading documents

- 内部名称：`customDocumentLoader`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/CustomDocumentLoader/CustomDocumentLoader.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `functionInputVariables` | Input Variables | `json` | 否 |
| `javascriptFunction` | Javascript Function | `code` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Custom Document Loader”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Document Store

Load data from pre-configured document stores

- 内部名称：`documentStore`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/DocumentStore/DocStoreLoader.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：是
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`yes`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedStore` | Select Store | `asyncOptions` | 是 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Document Store”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Docx File

Load data from DOCX files

- 内部名称：`docxFile`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Docx/Docx.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `docxFile` | Docx File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Docx File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Epub File

Load data from EPUB files

- 内部名称：`epubFile`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Epub/Epub.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `epubFile` | Epub File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `usage` | Usage | `options` | 是 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Epub File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Figma

Load data from a Figma file

- 内部名称：`figma`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Figma/Figma.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`figmaApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `fileKey` | File Key | `string` | 是 |
| `nodeIds` | Node IDs | `string` | 是 |
| `recursive` | Recursive | `boolean` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Figma”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## File Loader

A generic file loader that can load different file types

- 内部名称：`fileLoader`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/File/File.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `file` | File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `usage` | Pdf Usage | `options` | 否 |
| `legacyBuild` | Use Legacy Build | `boolean` | 否 |
| `pointerName` | JSONL Pointer Extraction | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“File Loader”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## FireCrawl

Load data from URL using FireCrawl

- 内部名称：`fireCrawl`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/FireCrawl/FireCrawl.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`fireCrawlApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `crawlerType` | Type | `options` | 是 |
| `url` | URLs | `string` | 否 |
| `includeTags` | Include Tags | `string` | 否 |
| `excludeTags` | Exclude Tags | `string` | 否 |
| `onlyMainContent` | Only Main Content | `boolean` | 否 |
| `limit` | Limit | `string` | 否 |
| `includePaths` | Include Paths | `string` | 否 |
| `excludePaths` | Exclude Paths | `string` | 否 |
| `extractSchema` | Schema | `json` | 否 |
| `extractPrompt` | Prompt | `string` | 否 |
| `searchQuery` | Query | `string` | 否 |
| `searchLimit` | Limit | `string` | 否 |
| `searchLang` | Language | `string` | 否 |
| `searchCountry` | Country | `string` | 否 |
| `searchTimeout` | Timeout | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“FireCrawl”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Folder with Files

Load data from folder with multiple files

- 内部名称：`folderFiles`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Folder/Folder.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `folderPath` | Folder Path | `string` | 是 |
| `recursive` | Recursive | `boolean` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `pdfUsage` | Pdf Usage | `options` | 否 |
| `pointerName` | JSONL Pointer Extraction | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Folder with Files”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## GitBook

Load data from GitBook

- 内部名称：`gitbook`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Gitbook/Gitbook.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `webPath` | Web Path | `string` | 是 |
| `shouldLoadAllPaths` | Should Load All Paths | `boolean` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“GitBook”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Github

Load data from a GitHub repository

- 内部名称：`github`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Github/Github.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`githubApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `repoLink` | Repo Link | `string` | 是 |
| `branch` | Branch | `string` | 是 |
| `recursive` | Recursive | `boolean` | 否 |
| `maxConcurrency` | Max Concurrency | `number` | 否 |
| `githubBaseUrl` | Github Base URL | `string` | 否 |
| `githubInstanceApi` | Github Instance API | `string` | 否 |
| `ignorePath` | Ignore Paths | `string` | 否 |
| `maxRetries` | Max Retries | `number` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Github”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Google Drive

Load documents from Google Drive files

- 内部名称：`googleDrive`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/GoogleDrive/GoogleDrive.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleDriveOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `selectedFiles` | Select Files | `asyncMultiOptions` | 否 |
| `folderId` | Folder ID | `string` | 否 |
| `fileTypes` | File Types | `multiOptions` | 否 |
| `includeSubfolders` | Include Subfolders | `boolean` | 否 |
| `includeSharedDrives` | Include Shared Drives | `boolean` | 否 |
| `maxFiles` | Max Files | `number` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Google Drive”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Google Sheets

Load data from Google Sheets as documents

- 内部名称：`googleSheets`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/GoogleSheets/GoogleSheets.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：是；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`yes`
  - 可能写入：`review-required`
- 凭据：`googleSheetsOAuth2`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `spreadsheetIds` | Select Spreadsheet | `asyncMultiOptions` | 是 |
| `sheetNames` | Sheet Names | `string` | 否 |
| `range` | Range | `string` | 否 |
| `includeHeaders` | Include Headers | `boolean` | 是 |
| `valueRenderOption` | Value Render Option | `options` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Google Sheets”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Jira

Load issues from Jira

- 内部名称：`jira`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Jira/Jira.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`jiraApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `host` | Host | `string` | 是 |
| `projectKey` | Project Key | `string` | 是 |
| `limitPerRequest` | Limit per request | `number` | 否 |
| `createdAfter` | Created after | `string` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Jira”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Json File

Load data from JSON files

- 内部名称：`jsonFile`
- 版本：`3.1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Json/Json.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `jsonFile` | Json File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `separateByObject` | Separate by JSON Object (JSON Array) | `boolean` | 否 |
| `pointersName` | Pointers Extraction (separated by commas) | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Json File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Json Lines File

Load data from JSON Lines files

- 内部名称：`jsonlinesFile`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Jsonlines/Jsonlines.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `jsonlinesFile` | Jsonlines File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `pointerName` | Pointer Extraction | `string` | 是 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Json Lines File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Microsoft Excel

Load data from Microsoft Excel files

- 内部名称：`microsoftExcel`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/MicrosoftExcel/MicrosoftExcel.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `excelFile` | Excel File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Microsoft Excel”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Microsoft PowerPoint

Load data from Microsoft PowerPoint files

- 内部名称：`microsoftPowerpoint`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/MicrosoftPowerpoint/MicrosoftPowerpoint.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `powerpointFile` | PowerPoint File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Microsoft PowerPoint”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Microsoft Word

Load data from Microsoft Word files

- 内部名称：`microsoftWord`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/MicrosoftWord/MicrosoftWord.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `docxFile` | Word File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Microsoft Word”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Notion Database

Load data from Notion Database (each row is a separate document with all properties as metadata)

- 内部名称：`notionDB`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Notion/NotionDB.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`notionApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `databaseId` | Notion Database Id | `string` | 是 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Notion Database”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Notion Folder

Load data from the exported and unzipped Notion folder

- 内部名称：`notionFolder`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Notion/NotionFolder.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `notionFolder` | Notion Folder | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Notion Folder”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Notion Page

Load data from Notion Page (including child pages all as separate documents)

- 内部名称：`notionPage`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Notion/NotionPage.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`notionApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `pageId` | Notion Page Id | `string` | 是 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Notion Page”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Oxylabs

Extract data from URLs using Oxylabs

- 内部名称：`oxylabs`
- 版本：`1`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Oxylabs/Oxylabs.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`oxylabsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 是 |
| `query` | Query | `string` | 是 |
| `source` | Source | `options` | 是 |
| `geo_location` | Geolocation | `string` | 否 |
| `render` | Render | `boolean` | 否 |
| `parse` | Parse | `boolean` | 否 |
| `user_agent_type` | User Agent Type | `options` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Oxylabs”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Pdf File

Load data from PDF files

- 内部名称：`pdfFile`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Pdf/Pdf.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `pdfFile` | Pdf File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `usage` | Usage | `options` | 是 |
| `legacyBuild` | Use Legacy Build | `boolean` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Pdf File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Plain Text

Load data from plain text

- 内部名称：`plainText`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/PlainText/PlainText.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `text` | Text | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Plain Text”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输入包含动态表达式，目录仅列出可静态解析参数；输出包含动态表达式，目录仅列出可静态解析参数

## Playwright Web Scraper

Load data from webpages

- 内部名称：`playwrightWebScraper`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Playwright/Playwright.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `url` | URL | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `relativeLinksMethod` | Get Relative Links Method | `options` | 否 |
| `limit` | Get Relative Links Limit | `number` | 否 |
| `waitUntilGoToOption` | Wait Until | `options` | 否 |
| `waitForSelector` | Wait for selector to load | `string` | 否 |
| `cssSelector` | CSS Selector (Optional) | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Playwright Web Scraper”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Puppeteer Web Scraper

Load data from webpages

- 内部名称：`puppeteerWebScraper`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Puppeteer/Puppeteer.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `url` | URL | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `relativeLinksMethod` | Get Relative Links Method | `options` | 否 |
| `limit` | Get Relative Links Limit | `number` | 否 |
| `waitUntilGoToOption` | Wait Until | `options` | 否 |
| `waitForSelector` | Wait for selector to load | `string` | 否 |
| `cssSelector` | CSS Selector (Optional) | `string` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Puppeteer Web Scraper”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## S3

Load Data from S3 Buckets

- 内部名称：`S3`
- 版本：`5`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/S3File/S3File.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `bucketName` | Bucket | `string` | 是 |
| `keyName` | Object Key | `string` | 是 |
| `region` | Region | `asyncOptions` | 是 |
| `fileProcessingMethod` | File Processing Method | `options` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |
| `unstructuredAPIUrl` | Unstructured API URL | `string` | 是 |
| `unstructuredAPIKey` | Unstructured API KEY | `password` | 否 |
| `strategy` | Strategy | `options` | 否 |
| `encoding` | Encoding | `string` | 否 |
| `skipInferTableTypes` | Skip Infer Table Types | `multiOptions` | 否 |
| `hiResModelName` | Hi-Res Model Name | `options` | 否 |
| `chunkingStrategy` | Chunking Strategy | `options` | 否 |
| `ocrLanguages` | OCR Languages | `multiOptions` | 否 |
| `sourceIdKey` | Source ID Key | `string` | 否 |
| `coordinates` | Coordinates | `boolean` | 否 |
| `xmlKeepTags` | XML Keep Tags | `boolean` | 否 |
| `includePageBreaks` | Include Page Breaks | `boolean` | 否 |
| `multiPageSections` | Multi-Page Sections | `boolean` | 否 |
| `combineUnderNChars` | Combine Under N Chars | `number` | 否 |
| `newAfterNChars` | New After N Chars | `number` | 否 |
| `maxCharacters` | Max Characters | `number` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“S3”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## S3 Directory

Load Data from S3 Buckets

- 内部名称：`s3Directory`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/S3Directory/S3Directory.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`awsApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `bucketName` | Bucket | `string` | 是 |
| `region` | Region | `asyncOptions` | 是 |
| `serverUrl` | Server URL | `string` | 否 |
| `prefix` | Prefix | `string` | 否 |
| `pdfUsage` | Pdf Usage | `options` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“S3 Directory”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## SearchApi For Web Search

Load data from real-time search results

- 内部名称：`searchApi`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/SearchApi/SearchAPI.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`searchApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `query` | Query | `string` | 否 |
| `customParameters` | Custom Parameters | `json` | 否 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“SearchApi For Web Search”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## SerpApi For Web Search

Load and process data from web search results

- 内部名称：`serpApi`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/SerpApi/SerpAPI.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`serpApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `query` | Query | `string` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“SerpApi For Web Search”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Spider Document Loaders

Scrape & Crawl the web with Spider

- 内部名称：`spiderDocumentLoaders`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Spider/Spider.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`spiderApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `mode` | Mode | `options` | 是 |
| `url` | Web Page URL | `string` | 是 |
| `limit` | Limit | `number` | 是 |
| `additional_metadata` | Additional Metadata | `json` | 否 |
| `params` | Additional Parameters | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Spider Document Loaders”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Text File

Load data from text files

- 内部名称：`textFile`
- 版本：`3`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Text/Text.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：需按实际配置复核；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`review-required`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `txtFile` | Txt File | `file` | 是 |
| `textSplitter` | Text Splitter | `TextSplitter` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Text File”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## Unstructured File Loader

Use Unstructured.io to load data from a file path

- 内部名称：`unstructuredFileLoader`
- 版本：`4`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/Unstructured/UnstructuredFile.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：`unstructuredApi`

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `fileObject` | Files Upload | `file` | 是 |
| `unstructuredAPIUrl` | Unstructured API URL | `string` | 是 |
| `strategy` | Strategy | `options` | 否 |
| `encoding` | Encoding | `string` | 否 |
| `skipInferTableTypes` | Skip Infer Table Types | `multiOptions` | 否 |
| `hiResModelName` | Hi-Res Model Name | `options` | 否 |
| `chunkingStrategy` | Chunking Strategy | `options` | 否 |
| `ocrLanguages` | OCR Languages | `multiOptions` | 否 |
| `sourceIdKey` | Source ID Key | `string` | 否 |
| `coordinates` | Coordinates | `boolean` | 否 |
| `xmlKeepTags` | XML Keep Tags | `boolean` | 否 |
| `includePageBreaks` | Include Page Breaks | `boolean` | 否 |
| `xmlKeepTags` | XML Keep Tags | `boolean` | 否 |
| `multiPageSections` | Multi-Page Sections | `boolean` | 否 |
| `combineUnderNChars` | Combine Under N Chars | `number` | 否 |
| `newAfterNChars` | New After N Chars | `number` | 否 |
| `maxCharacters` | Max Characters | `number` | 否 |
| `metadata` | Additional Metadata | `json` | 否 |
| `omitMetadataKeys` | Omit Metadata Keys | `string` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“Unstructured File Loader”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 凭据未绑定、已失效或当前工作空间无权读取
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数

## VectorStore To Document

Search documents with scores from vector store

- 内部名称：`vectorStoreToDocument`
- 版本：`2`
- 功能状态：`production-enabled`
- 源码锚点：`packages/components/nodes/documentloaders/VectorStoreToDocument/VectorStoreToDocument.ts@96f6ae464f7f4757883a5ba6bec26ca951b4da4d`
- 官方文档：[分类级官方文档](https://docs.flowiseai.com/integrations/langchain/document-loaders)
- 风险：外部调用：是；可能计费：需按实际配置复核；可能写入：需按实际配置复核
  - 外部调用：`yes`
  - 可能计费：`review-required`
  - 可能写入：`review-required`
- 凭据：无静态凭据声明

| 参数 | 界面标签 | 类型 | 必填 |
|---|---|---|---|
| `vectorStore` | Vector Store | `VectorStore` | 是 |
| `query` | Query | `string` | 否 |
| `minScore` | Minimum Score (%) | `number` | 否 |

**静态输出声明：**

| 输出 | 界面标签 | 类型 |
|---|---|---|
| `document` | Document | `dynamic` |
| `text` | Text | `dynamic` |

**隔离环境示例：** 在隔离培训画布中添加“VectorStore To Document”，绑定合成输入并运行一次，在执行记录中核对输入、输出与错误。

**常见错误：**

- 必填输入为空或类型与上游节点输出不匹配
- 外部服务超时、限流、网络策略或接口版本不兼容
- 重复执行造成非幂等写入，或目标资源权限不足

!!! warning "静态解析限制"
    输出包含动态表达式，目录仅列出可静态解析参数
