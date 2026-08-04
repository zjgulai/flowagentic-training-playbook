---
title: 实验安全合同
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: beginner
duration: "10 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: budget-controlled
side_effects:
  - governs-training-experiments
last_verified: "2026-08-04"
evidence_ids:
  - CLM-013
  - CLM-018
  - CLM-023
  - CLM-024
screenshot_ids: []
---

# 实验安全合同

开始实验即表示遵守：

1. 只在版本匹配的隔离培训环境操作。
2. 只输入培训包中的合成数据。
3. 凭据只进入秘密存储，不进入 Git、截图、日志或导出物。
4. 外部写入只指向模拟工单 API。
5. 每个对象先登记再创建，结束后按 ledger 清理。
6. Provider 调用必须先生成 pending 预留，再由预算包装器原子消费为 in_flight；异常结果按预留上限记账。DeepSeek 与 Kimi 的账户子限额合计不得超过 ¥300，关闭自动充值、本地 ledger 和隔离执行器签名四项缺一不可。
7. 生产环境只允许只读交叉核验。
8. 发现真实个人信息、内部域名、Token、Key、Cookie 或未知资源 ID 时立即停止并报告。

讲师在每节实验前确认门禁；学员无权自行绕过。

Provider 预留不是“可以调用多次”的额度券。每个实验 ID 只授权一次 transport；进程崩溃后保留的 in_flight 金额继续占用预算，必须先完成受控对账，不能直接 release。若实际账单高于预留，ledger 标记 `breached` 并阻断后续调用；本地控制不能替代 Provider 账户侧子限额，ledger 中的“成功”也不能替代隔离执行器签名及 Provider 用量摘要。
