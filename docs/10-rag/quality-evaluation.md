---
title: RAG 质量评估 SOP
audience:
  - builder
  - developer
difficulty: advanced
duration: "60 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - may-call-embedding-and-llm-provider
last_verified: "2026-08-04"
evidence_ids:
  - CLM-007
  - CLM-019
  - CLM-023
screenshot_ids: []
---

# RAG 质量评估 SOP

## 测试集

至少包含：

- 文档中有直接答案的问题；
- 需要跨两个片段组合的问题；
- 同义改写和口语问题；
- 文档中没有答案的问题；
- 多版本冲突问题；
- 试图诱导忽略知识库的恶意问题。

每题记录期望答案要点、允许来源、禁止结论和难度。

## 分层评估

1. **载入层**：文档是否完整、编码是否正确。
2. **切分层**：答案信息是否集中在合理 chunk 中。
3. **检索层**：正确片段是否进入 Top K。
4. **生成层**：回答是否忠于片段、引用是否对应。
5. **体验层**：延迟、费用和无答案提示是否可接受。

一次只改变一个变量，对比 chunk、overlap、Top K、metadata、Embedding 或 rerank。不要同时改变所有参数后把提升归因给某一个设置。

## 验收

- 有答案问题的正确片段可稳定召回。
- 无答案问题不会编造。
- 冲突版本能按 metadata 或时间策略选择。
- token、延迟和费用处于培训预算内。
- 实验输入、配置、结果和结论可复现。
