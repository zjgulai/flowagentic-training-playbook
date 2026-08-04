---
title: API、Embed 与 SDK
audience:
  - developer
  - admin
difficulty: advanced
duration: "90 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - invokes-flow
  - may-upload-data
last_verified: "2026-08-04"
evidence_ids:
  - CLM-009
  - CLM-010
  - CLM-020
screenshot_ids: []
---

# API、Embed 与 SDK

## 认证材料不要混用

- 管理 API Key：面向管理接口，权限通常更高。
- Flow API Key：限制到具体流程时优先使用。
- Cookie：浏览器登录会话，不应复制到服务端脚本。
- MCP Token：用于 MCP 连接，不替代 Flow API Key。
- Provider Key：Flow 内部调用模型服务的凭据，不发给客户端。

具体权限以目标部署的接口和功能开关为准。

## Prediction API

服务端调用应固定流程 ID、请求超时、重试上限、幂等策略和日志脱敏。Streaming 要分别验证连接建立、分片顺序、中断、超时和最终状态。Upload 限制类型、大小、数量和恶意内容。

`overrideConfig` 只开放允许列表；禁止客户端覆盖内部端点、系统提示、安全开关或不受控凭据引用。

## Embed

Web Component 或 React Embed 上线前验证：

- CSP 和 CORS 只允许预期来源；
- iframe 权限和消息通道最小化；
- 前端不包含管理 Key 或 Provider Key；
- 依赖版本锁定并有升级回归；
- 主题、中文文案、键盘导航和移动端关键路径可用。

## SDK 状态

Agentflow SDK 与 Observe SDK 在本 Playbook 中按 `experimental` 或 `upstream-only` 单独说明，不能因为包存在就承诺本部署生产可用。进入正式课程前需要目标提交源码、官方语义和培训环境复现三角验证。
