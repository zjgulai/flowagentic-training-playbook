---
title: 开发测试与浏览器验收
audience:
  - developer
difficulty: advanced
duration: "60 分钟"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - source-code-access
cost_class: none
side_effects:
  - runs-local-tests
last_verified: "2026-08-04"
evidence_ids:
  - CLM-014
  - CLM-017
  - CLM-023
screenshot_ids: []
---

# 开发测试与浏览器验收

## 测试分层

- 静态检查：格式、类型、依赖、秘密和许可证。
- 单元测试：纯逻辑、Schema、状态转换和错误映射。
- 集成测试：路由、服务、数据库、节点池和权限边界。
- 运行测试：真实构建制品、迁移和配置。
- 浏览器测试：用户主链、错误状态、键盘导航、控制台与网络。

## PC 主链

以 `1440×1000`、100% 缩放、`zh-CN`、浅色主题为基线，在 Chrome 与 Firefox 逐页验证十个主模块及其关键弹窗。移动端只要求没有关键导航阻断；PC 端交互完整性优先。

## 证据

每次验收记录精确 SHA、环境、浏览器版本、路线、输入、预期、实际、截图 ID、控制台和网络摘要。自动化成功、页面可见和生产发布回执是不同证据，不能互相替代。
