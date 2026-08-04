---
title: Agentflow V2 设计审查清单
audience:
  - builder
  - developer
difficulty: advanced
duration: "25 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - none
last_verified: "2026-08-04"
evidence_ids:
  - CLM-005
  - CLM-006
  - CLM-018
  - CLM-023
screenshot_ids: []
---

# Agentflow V2 设计审查清单

- [ ] Start 触发器、输入 Schema、认证和重放策略明确。
- [ ] Flow State 每个字段都有唯一含义、类型和责任节点。
- [ ] 确定性规则使用 Condition，模型判断有兜底与人工复核。
- [ ] Agent 的最大步数、工具允许列表和费用上限明确。
- [ ] Tool／HTTP 的外部写入具备预览、确认、幂等和回执。
- [ ] Iteration 有集合上限、单项超时和整体预算。
- [ ] HITL 的 STOPPED、Proceed、Reject、Resume 均有测试。
- [ ] Execute Flow 没有递归环，输入输出契约已固定。
- [ ] Schedule 时区、重复触发和漏触发恢复策略明确。
- [ ] Webhook 验证签名、重放、载荷大小和错误响应。
- [ ] 正常、空状态、错误、超时、限流和恢复路径均有执行证据。
