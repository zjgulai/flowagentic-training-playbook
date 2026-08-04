---
title: 受限与实验能力附录
audience:
  - developer
  - admin
difficulty: advanced
duration: "45 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: feature-gated
permissions:
  - admin
  - feature-specific-permission
cost_class: medium
side_effects:
  - varies-by-feature
last_verified: "2026-08-04"
evidence_ids:
  - CLM-003
  - CLM-005
  - CLM-011
screenshot_ids: []
---

# 受限与实验能力附录

本章不承诺以下能力在当前部署可用。进入正文课程前，每项都要补齐功能开关、权限、许可证、目标提交源码、官方语义和培训环境验证。

| 能力 | 当前 Playbook 状态 | 发布前所需证据 |
| --- | --- | --- |
| 数据集 | `feature-gated` | 页面、API、权限与完整实验 |
| 评估器 | `feature-gated` | 评分语义、数据边界与运行结果 |
| 评估任务 | `feature-gated` | 创建、运行、结果与清理 |
| 用户、角色、工作空间 | `feature-gated` | 许可证、权限矩阵与隔离验证 |
| SSO | `feature-gated` | IdP 配置、登录、退出、失败和回退 |
| 登录活动 | `feature-gated` | 访问权限、字段、保留与脱敏 |
| 服务端日志页面 | `feature-gated` | 权限、敏感字段和审计 |
| Agentflow SDK | `experimental` | API 稳定性和目标部署复现 |
| Observe SDK | `experimental` | 数据范围、隐私和性能验证 |

如果目标部署未启用，页面中统一使用“本部署未启用”，不提供会诱导用户绕过开关或权限的操作步骤。

## 能力转正流程

1. 固定目标版本和上游语义。
2. 完成功能、权限、数据和安全模型。
3. 在隔离环境复现成功、失败、权限不足和清理。
4. 添加 SOP、证据、截图和故障排查。
5. 通过内容与发布评审后，才将状态改为 `production-enabled`。
