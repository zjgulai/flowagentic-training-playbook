---
title: "功能状态矩阵"
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: beginner
duration: 10 分钟
release_version: 3.1.3
release_sha: 6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64
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

# 功能状态矩阵

状态标签说明的是“本培训站如何处理该能力”，不是营销意义上的可用性承诺。

| 状态 | 含义 | 培训处理 |
|---|---|---|
| `production-enabled` | 目标基线源码与主导航把它列为正式产品路径；不单独证明候选已部署 | 提供完整 SOP，并在同版本隔离环境复验 |
| `feature-gated` | 依赖许可证、功能开关、角色或工作空间权限 | 放入扩展附录，不能暗示默认可见 |
| `deprecated` | 仍可能存在，但已进入迁移或兼容阶段 | 只讲迁移和风险，不作为新建主线 |
| `experimental` | SDK 或能力尚未达到生产承诺 | 仅限隔离实验，不能作为生产方案 |
| `upstream-only` | 上游存在，但当前部署没有交付证据 | 只作差异说明 |

## 十个完整 SOP 模块

对话流程、智能体流程、执行记录、助手、模板市场、工具与 MCP、凭据、变量、API 密钥和文档库属于首版完整 SOP 范围。

## 扩展附录

数据集、评估器、评估任务、用户、角色、工作空间、SSO、登录活动和服务端日志均按 `feature-gated` 处理。Agentflow SDK 与 Observe SDK 按 `experimental` 处理。Agentflow V1 和 OpenAI Assistant 按 `deprecated` 处理。

机器可读真相源位于仓库的 `data/feature-status.yml`，发布验证会检查完整 SOP 恰好覆盖十个主模块。
