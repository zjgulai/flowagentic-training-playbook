---
title: Chatflow 发布前验收清单
audience:
  - builder
  - admin
difficulty: intermediate
duration: "20 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: low
side_effects:
  - may-publish-flow
last_verified: "2026-08-04"
evidence_ids:
  - CLM-009
  - CLM-016
  - CLM-020
  - CLM-023
screenshot_ids: []
---

# Chatflow 发布前验收清单

## 功能

- [ ] 正常、空输入、长输入、附件和异常路径均有预期结果。
- [ ] 所有节点必填项、输入输出类型和连线通过验证。
- [ ] 保存后刷新，流程结构与配置不丢失。
- [ ] 来源、工具结果和结构化输出可被下游正确解析。

## 安全

- [ ] 流程、导出 JSON、日志、截图中没有 Key、Token、Cookie、真实邮箱、内部域名或资源 ID。
- [ ] API Key 采用最小权限并有轮换计划。
- [ ] `overrideConfig` 只开放明确允许的字段。
- [ ] HTTP、Tool、MCP 和自定义代码经过 SSRF、注入与副作用评审。

## 可靠性与成本

- [ ] Provider 设有超时、有限重试和并发约束。
- [ ] 外部写入具备幂等键或重复请求保护。
- [ ] token、延迟和费用有基线与告警阈值。
- [ ] RAG、工具或下游失败时有可理解的降级响应。

## 发布证据

- [ ] 目标环境、版本 SHA、流程 ID、验收时间和验收人已记录。
- [ ] Chrome 与 Firefox PC 主链通过。
- [ ] 浏览器控制台和关键接口没有未解释错误。
- [ ] 回滚制品已验证可导入，但未在公开站暴露内部路径。

清单完成不自动授权发布；仍需通过人工发布门禁。
