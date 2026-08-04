---
title: 练习、评分与结业测验
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: intermediate
duration: "60 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - training-environment-user
cost_class: low
side_effects:
  - creates-training-resources
last_verified: "2026-08-04"
evidence_ids:
  - CLM-002
  - CLM-024
screenshot_ids: []
---

# 练习、评分与结业测验

## 实操任务

### 新手使用者

登录培训环境，运行 FAQ 流程，从执行记录找出模型、耗时和来源，安全退出。

### 流程搭建者

搭建带 RAG 的 Chatflow，处理有答案和无答案问题；再修复一条预置的维度不匹配故障。

### 二次开发者

从 UI 操作追踪到服务端处理路径，指出权限检查和节点执行边界，补充一项测试。

### 管理员

根据发布候选证据判断是否允许发布，并解释一个“构建通过但不可发布”的原因。

## 评分规则

| 维度 | 分值 | 评分点 |
| --- | ---: | --- |
| 正确完成主链 | 30 | 结果与检查点一致 |
| 诊断与恢复 | 25 | 找到第一处异常，回退安全 |
| 安全与数据边界 | 25 | 无秘密、真实数据或越权 |
| 证据与表达 | 10 | 区分事实、推断和未验证 |
| 清理 | 10 | ledger 完整且无残留 |

总分 80 分及格；安全与数据边界低于 20 分不得结业。

## 结业测验样题

1. 凭据、变量和 API Key 的职责分别是什么？
2. 为什么画布验证通过仍不能证明 Provider 可用？
3. RAG 回答错误时，为什么要先检查 retrieved context？
4. HITL 恢复前必须核对哪些状态？
5. Tool 写入外部系统为何需要幂等键？
6. 401 与 403 的排查方向有什么不同？
7. PR 构建成功是否等于 GitHub Pages 已发布？为什么？
8. 为什么生产环境只用于只读交叉核验？

## 参考答案要点

答案必须体现权限、版本、证据、副作用、费用和回退。只复述按钮位置不算完整；以生产写入“证明功能”的答案判为高风险错误。

## 学员清理清单

- [ ] Chatflow、Agentflow、Assistant、Tool 和 MCP 实验对象。
- [ ] 文档库、向量集合、合成上传文件和处理历史。
- [ ] 临时 API Key、Credential 和变量。
- [ ] 会话、执行、Schedule、Webhook 和模拟工单。
- [ ] Provider 调用与费用 ledger 完整。
- [ ] 残留查询结果为零；共享基线对象未被修改。
