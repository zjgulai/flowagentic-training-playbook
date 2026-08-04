---
title: "公开站与私有 Runbook 边界"
audience:
  - developer
  - admin
difficulty: advanced
duration: 10 分钟
release_version: 3.1.3
release_sha: 96f6ae464f7f4757883a5ba6bec26ca951b4da4d
feature_status: production-enabled
permissions:
  - content-review
cost_class: none
side_effects: []
last_verified: "2026-08-04"
evidence_ids:
  - CLM-001
  - CLM-003
  - CLM-014
  - CLM-017
  - CLM-024
screenshot_ids: []
---

# 公开站与私有 Runbook 边界

公开 Playbook 解释用户如何安全完成任务；私有 Runbook 记录真实基础设施如何部署、恢复和取证。两者使用相同的门禁语言，但不共享敏感操作细节。

| 可以公开 | 必须留在私有 Runbook |
|---|---|
| 通用发布、回滚和验收原则 | 真实主机、域名、IP、端口和容器编排细节 |
| 脱敏后的 UI SOP | 管理员账号、Cookie、Token、API Key 和 Provider 凭据 |
| 合成数据和虚构 API | 数据库连接、加密密钥和真实对象 ID |
| 风险模型与检查表 | 可直接执行的备份恢复命令和生产回执 |
| 受控参考编号 | 内部链接、事故证据和人员联系方式 |

公开站只写“恢复前必须同时核验数据库、持久卷和加密密钥连续性”，不提供能直接作用于真实基础设施的命令。需要执行真实恢复时，操作者必须转入相应受控 Runbook，并重新取得该动作的授权与现场证据。
