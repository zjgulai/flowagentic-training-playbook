---
title: 公开发布门禁
audience:
  - admin
  - developer
difficulty: advanced
duration: "25 分钟"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - repository-maintainer
cost_class: none
side_effects:
  - may-publish-public-site
last_verified: "2026-08-04"
evidence_ids:
  - CLM-015
  - CLM-021
  - CLM-024
screenshot_ids: []
---

# 公开发布门禁

公开发布前必须同时满足：

- 中文源码候选的精确 SHA、版本和部署时间均有回执，十个主页面、弹窗和关键路由的 G1 中文 PC 验收通过。
- 正式截图全部来自同版本隔离培训环境，manifest 无缺失、孤儿或版本混用。
- OCR、EXIF、PNG/WebP 非必要元数据和秘密扫描确认真实邮箱、IP、内部域名、Token、Key、Cookie、UUID 和路径为零。
- 每条核心结论具备目标系统事实、官方语义和培训环境复现。
- DeepSeek 与 Kimi 实验成功；两家账户子限额合计不超过人民币 300 元，关闭自动充值、一次性预算包装器及费用 ledger 均有结构化回执。
- Provider 成功结论必须由仓库信任清单中的隔离执行器使用 Ed25519 签名，签名载荷同时绑定发布 SHA、模型、合成 fixture、token、延迟、实际费用、Provider 用量摘要和清理摘要；本地模拟 transport 不能满足该门禁。
- 站点严格构建、链接、frontmatter、引用、可访问性和 PDF 验证通过。
- 四类角色完成盲走验收。
- 每道外部门禁使用固定的证据 ID 与回执类型，并提交绑定版本、SHA、时间、评审人和公开安全证据制品的结构化回执；CI 会重新计算每个制品及聚合 SHA-256，不能用自报摘要或删空证据清单绕过。
- 构建与测试 Job 只有只读权限；写权限 Job 只发布已验证的 mike 静态树，`latest` 与版本目录在同一个 Git 提交中更新，并在发布后执行只读 HTTP 冒烟。

PR 预览制品不等于公开发布；`main` 合并也不自动证明 GitHub Pages 已更新。
