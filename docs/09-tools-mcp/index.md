---
title: Tools 与 MCP
audience:
  - builder
  - developer
  - admin
difficulty: advanced
duration: "100 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - executes-custom-code
  - may-call-or-write-external-system
last_verified: "2026-08-04"
evidence_ids:
  - CLM-011
  - CLM-012
  - CLM-023
  - CLM-025
screenshot_ids:
  - TOOL-001
  - TOOL-002
  - TOOL-003
  - TOOL-004
  - TOOL-005
  - TOOL-006
  - TOOL-007
  - TOOL-008
  - TOOL-009
  - TOOL-010
  - TOOL-011
  - TOOL-012
  - MCP-001
  - MCP-002
  - MCP-003
  - MCP-004
  - MCP-005
  - MCP-006
  - MCP-007
  - MCP-008
  - MCP-009
  - MCP-010

---

# Tools 与 MCP

## Tool 是能力契约

一个可用的 Custom Tool 需要清楚的名称、用途说明、JSON Schema、输入校验、返回格式、超时和错误处理。模型依赖名称与描述决定是否调用；描述模糊会导致误调用。

## Custom Tool SOP

1. 把查询与写入拆成不同工具。
2. 使用 JSON Schema 约束必填字段、类型、枚举、长度和格式。
3. 仅从受控的 `$flow`、`$vars` 和输入参数读取数据。
4. 为网络、计算和返回大小设置上限。
5. 返回结构化结果，并区分业务失败与系统失败。
6. 用正常、空值、越界、恶意输入、超时和重复请求测试。
7. 对写入工具加入幂等键、预览或人工确认。

自定义 JavaScript 按不可信代码处理：禁止访问未授权环境变量、文件系统或内网，审查动态执行和依赖来源。

## MCP 连接

Custom MCP Server 可能使用 HTTP、SSE 或 Streamable HTTP。配置时记录服务端所有者、认证方式、允许的工具、数据边界和撤销方式。

### 授权与发现

1. 先验证服务端 URL 和证书。
2. 通过秘密存储配置 Token 或 OAuth，不写进 URL。
3. 完成 Authorize 后只读发现工具列表。
4. 检查工具名称、说明、输入 Schema 和注解。
5. 只允许本实验需要的工具，再执行合成数据调用。

## 将 Flow 暴露为 MCP Server

暴露前确认身份认证、工具允许列表、输入大小、限流、超时、审计和撤销。不要把内部管理流程直接公开为 MCP 工具。

### 旧 Token 迁移与重新启用

目标候选遇到旧版 `mcpServerConfig.token` 时采用 fail-closed 迁移：配置被禁用，旧明文和旧摘要被删除，不会把旧 Token 静默转换成继续有效的凭据。管理员必须在维护窗口内逐个重新启用需要的 MCP Server，领取只显示一次的新 Token，并通过受控渠道分发。验收同时检查旧 Token 失败、新 Token 成功、响应禁止缓存，以及数据库和日志中没有 Token 值。

### 公共请求解析与审计边界

MCP 公共命名空间只在 bearer 鉴权和限流后解析有界 JSON；未知 method 或子路径在 MCP 路由内固定结束，不能落入应用级大正文解析器。每个请求最多形成一条审计和一条指标，字段只保留随机请求标识、规范化方法、固定路由、状态码、耗时和完成方式。流程 ID、原始路径、Header、query、body、Token、Cookie、用户输入和错误正文均不得进入日志或指标标签。

## 主要威胁

- Token 泄露：禁止进入 URL、日志、截图和导出物。
- SSRF：限制协议、主机、端口和重定向，阻止访问内网元数据地址。
- 提示注入：外部工具返回值是不可信数据，不能当系统指令。
- 误写入：查询与写入隔离，写入要求幂等和确认。
- 工具投毒：工具说明和 Schema 变化后必须重新审查。
- 无限或级联调用：设置每次运行的最大工具调用数和费用上限。
- 迁移中断：旧 MCP Token 会有意失效，未提前通知客户端和准备新 Token 分发会造成可用性中断。

本章正式截图将在隔离环境覆盖 Tool Schema、测试结果、MCP 授权、工具发现、失败与撤销。

## 目标

建立输入受约束、权限最小、可超时、可撤销的 Tool／MCP 能力，并证明查询、写入和失败恢复互不混淆。

## 适用角色

搭建者定义能力契约，开发者实现 Schema／代码／transport，管理员审批网络、Token、工具允许列表和撤销。

## 适用版本与功能状态

Custom Tool 为 `production-enabled`；将 Flow 暴露为 MCP 的代码能力已存在，但目标部署开关和运行链仍需复验。

## 前置条件与风险

需要合成 MCP 服务、允许主机列表、秘密存储、超时／调用数上限、写入幂等键和回滚 API。风险包括 SSRF、代码执行、Token 泄露、提示注入和级联费用。

## 初始状态

从 Tools 页面确认无同名对象、MCP 未授权、目标服务只含合成数据，内网和元数据地址阻断规则已启用。

## 操作步骤

定义名称说明 → 写 JSON Schema → 实现查询逻辑 → 测正常／恶意／超时 → 配 MCP transport → 安全授权 → 只读发现 → 审查工具 → 最小调用 → 撤销。

## 逐步检查点

Schema 拒绝未知字段；返回结构稳定；写入要求幂等和确认；授权 Header 被遮罩；发现列表只含允许工具；超时后没有后台继续写入。

## 成功结果

正常查询成功，恶意输入、内网目标和越权工具被拒绝；写入重放不重复；撤销后授权和工具调用均失效。

## 常见错误与诊断

Authorize 失败检查 URL、证书、transport 和 Token；发现为空检查协议版本和权限；超时区分客户端、服务端和下游；重复写入检查幂等键和重试层。

## 回退与清理

先撤销 Token／OAuth，再禁用服务器和写入工具；删除合成外部对象、Tool、MCP 配置和执行记录，复核无后台任务和开放连接。

## 安全提示

禁止任意命令、任意 URL 和未审查 JavaScript。外部工具说明与返回均不可信；MCP Token 不进入 URL、日志、导出或截图。

## 练习任务

实现只读工单查询 Tool 和合成 MCP 服务，验证正常发现、错误 Token、SSRF 阻断、超时和撤销。

## 验收清单

- [ ] Schema、允许列表、超时、幂等和撤销完整。
- [ ] 正常、恶意、失败、恢复路径通过。
- [ ] 网络、Token、费用、外部对象和残留清零。

## 来源与验证

MCP 能力、安全差异和副作用引用 `CLM-011/012/023`；目标部署授权、发现、调用与撤销尚待隔离环境三角验证。
