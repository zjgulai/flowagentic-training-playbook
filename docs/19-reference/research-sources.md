---
title: 研究来源与可信度
audience:
  - builder
  - developer
  - admin
difficulty: intermediate
duration: 15 分钟
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - public
cost_class: none
side_effects:
  - none
last_verified: "2026-08-04"
evidence_ids:
  - CLM-001
  - CLM-003
  - CLM-014
  - CLM-017
  - CLM-024
screenshot_ids: []
---

# 研究来源与可信度

本页是读者导航，机器可审计的完整字段保存在 `research/sources.yml`，结论与来源的多对多关系保存在 `research/claims.yml`。截至 2026-08-04，研究库共收录 53 个去重来源：15 个目标系统证据、21 个 Flowise 官方资料、9 个 Release/PR 维护者记录，以及 8 个来自 8 位不同开发者的一手问题案例。

## 目标系统证据

目标证据全部锚定提交 `6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64`，主要覆盖：

- 根包版本、工作区与构建入口；
- 十个中文主模块、路由、权限和 feature gate；
- 登录、注册重定向、未授权和限流路由；
- 13 个 Agentflow 节点和 Agentflow 包的 Dev 状态；
- 311 个 `implements INode` 实现文件；
- DeepSeek、Kimi、Prediction、Document Store、Variables、Custom Tool 和 MCP 的代码入口。
- G1-K 工作区可移植性、MCP Token／请求边界和 Provider-backed Assistant 权限加固。

这些证据可以证明“固定提交中声明或实现了什么”，不能单独证明部署配置、许可证、外部网络、Provider 凭据和真实执行结果。

## Flowise 官方资料

官方资料覆盖 Agentflow V2、Flow State、Document Stores、Upsertion、Variables、Prediction、Streaming、Embed、Uploads、API Reference、Authorization、Rate Limit、Workspaces、Evaluations、环境变量和生产运行。官方资料用于定义术语和预期语义，但页面是滚动更新的；发布日期晚于目标版本的内容必须回查固定源码，并在页面上标记为 `upstream-only` 或 `feature-gated`。

主要入口：

- [Flowise 官方能力概览](https://docs.flowiseai.com/)
- [Agentflow V2](https://docs.flowiseai.com/using-flowise/agentflowv2)
- [Document Stores](https://docs.flowiseai.com/using-flowise/document-stores)
- [Variables](https://docs.flowiseai.com/using-flowise/variables)
- [Prediction API](https://docs.flowiseai.com/api-reference/prediction)
- [Authorization](https://docs.flowiseai.com/configuration/authorization)
- [Running Flowise in Production](https://docs.flowiseai.com/configuration/running-in-production)

## Release 与维护者记录

[flowise@3.1.3](https://github.com/FlowiseAI/Flowise/releases/tag/flowise%403.1.3) 用来解释目标上游版本的新增与修复，[flowise@3.1.4](https://github.com/FlowiseAI/Flowise/releases/tag/flowise%403.1.4) 用来识别目标版本之后的漂移。研究库还收录了点击劫持、Agentflow 变更通知、Start 表单过滤、Chatflow MCP Server、FlowConfigDialog 重设计、Agent 知识字段和 Custom MCP stdio allowlist 等合并 PR。

PR 能证明维护者修改了什么和何时合并，但不自动证明目标分支是否原样包含、是否被定制修改或是否完成生产配置。每条 PR 结论都需要目标 SHA 对照。

## 开发者一手案例

八个一手案例来自八位不同作者，覆盖：

- API 创建 Document Loader 后 UI 预览空白；
- Prediction SSE 偶发无内容；
- Embed 网络流暴露 Agentflow 内部事件的风险；
- Start/Form Input 请求缺少 `question`；
- Custom MCP SSRF 策略与 Docker 内部主机名冲突；
- Embed `sessionId` 行为不符合预期；
- Kubernetes Worker 内存持续增长；
- 受限网络下 tokenizer 静态资源导致节点等待。

这些案例的用途是生成对抗性测试与排障分支，而不是宣布目标系统存在相同缺陷。每个案例都在来源库中标记“target applicability unverified”，直到同版本隔离环境复现或排除。

## 如何阅读 Claim

`research/claims.yml` 中每条结论都包含：

- `experience_label`：`system-fact`、`official-semantics`、`inference` 或 `experience-advice`；
- `source_ids`：直接支撑来源；
- `local_verification`：已经完成和仍缺少的验证；
- `evidence_status`：当前证据门禁；
- `public_safe`：是否允许进入公开站。

若一条结论只有开发者案例而没有目标源码或培训环境证据，正文必须使用“报告显示”“风险假设”或“经验建议”等限定语，不能写成普遍事实。
