---
title: "参考与溯源"
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: intermediate
duration: 15 分钟
release_version: 3.1.3
release_sha: 96f6ae464f7f4757883a5ba6bec26ca951b4da4d
feature_status: production-enabled
permissions: []
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

# 参考与溯源

这里不是一份泛化的 Flowise 教程索引，而是 FlowAgentic 培训内容的事实底座。每一条关键结论都应能回答四个问题：

1. 它适用于哪个产品版本和提交？
2. 它来自目标系统、官方语义、培训复现还是开发者经验？
3. 它是否已在隔离培训环境复现？
4. 它与上游当前版本有什么差异？

## 可审计资产

- [全量节点参数目录](node-catalog/index.md)：固定提交中 311 个 `INode` 实现的可搜索索引。
- [功能状态矩阵](feature-status.md)：生产启用、受限、弃用、实验和仅上游能力的边界。
- [截图与脱敏合同](screenshot-governance.md)：截图从计划到可发布证据的状态机。
- [公开站与私有 Runbook 边界](public-private-boundary.md)：哪些内容必须留在受控环境。
- 研究方法、来源库、Claim—Evidence 矩阵和版本差异由 UltraDeep Research 章节维护。

## 当前事实边界

逻辑稿绑定 Flowise `3.1.3` 与提交 `96f6ae464f7f4757883a5ba6bec26ca951b4da4d`。同版本隔离培训环境已完成镜像、迁移、功能开关、基础认证与隔离边界验收；正式截图仍因生产部署、中文 PC 验收和截图回执未满足而保持关闭。源码存在或基础运行通过不等于生产已验证；页面可见也不等于外部 Provider、邮件、SSO 或写入链路已完成。
