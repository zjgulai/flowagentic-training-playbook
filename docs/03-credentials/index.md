---
title: 凭据、变量与 API 密钥
audience:
  - builder
  - developer
  - admin
difficulty: intermediate
duration: "45 分钟"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - manages-secrets
  - may-change-api-access
last_verified: "2026-08-04"
evidence_ids:
  - CLM-008
  - CLM-015
  - CLM-023
screenshot_ids: []
---

# 凭据、变量与 API 密钥

## 三者的边界

- **凭据**：访问 Provider、数据库或外部服务的秘密，必须进入秘密存储。
- **变量**：流程运行时需要的非秘密或受控配置，通过 `$vars` 读取。
- **API 密钥**：调用 FlowAgentic 接口的访问令牌，不等同于模型 Provider Key。

不要把 Token 放在变量、节点说明、URL、截图或导出的流程 JSON 中。

## 凭据生命周期 SOP

1. 记录用途、所有者、目标环境、最小权限和轮换日期。
2. 在培训环境创建凭据，名称采用“环境—服务—用途”，不含秘密片段。
3. 绑定到最小实验流程并执行一次合成数据验证。
4. 查看执行记录，确认日志和节点输出没有回显秘密。
5. 轮换时先新增、验证、切换引用，再撤销旧凭据。
6. 删除前列出关联流程；删除后确认没有孤儿引用。

检查点：页面遮罩不等于秘密安全；还必须扫描导出物、日志、截图和 Git 历史。

## 变量与请求级覆盖

为变量定义名称、类型、默认值、可覆盖范围和敏感等级。请求级 `overrideConfig` 或 `$vars` 覆盖应采用允许列表；不要允许客户端覆盖模型端点、内部 URL、系统指令或安全开关。

## API 密钥

创建前明确调用对象、权限、来源和失效时间。密钥只显示一次时立即保存到秘密管理工具。轮换遵循“新增 → 双轨验证 → 切换 → 观测 → 撤销”，不要直接覆盖唯一可用密钥。

## 泄露响应

1. 立即撤销或禁用疑似泄露密钥。
2. 查找调用日志、时间范围和影响对象。
3. 轮换依赖该密钥的流程与自动化。
4. 清理公开仓库、制品、截图和缓存；仅删除最新文件不足以消除 Git 历史。
5. 记录事件、根因和防复发控制。

OAuth、细粒度权限和企业能力若未在目标部署验证，按 `feature-gated` 处理，不以页面存在推断可用。
