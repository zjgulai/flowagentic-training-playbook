---
title: 实验答案与评分锚点
audience:
  - builder
  - developer
  - admin
difficulty: advanced
duration: "90 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - training-instructor
cost_class: low
side_effects:
  - reviews-training-evidence
last_verified: "2026-08-04"
evidence_ids:
  - CLM-007
  - CLM-015
  - CLM-020
  - CLM-023
screenshot_ids: []
---

# 实验答案与评分锚点

## 使用方式

本页给出可观察结果和判分边界，不提供真实账号、固定对象 ID 或可复制到生产的命令。讲师先看学员证据，再看答案；只得到正确最终页面但无法解释权限、费用、副作用与清理，不算完整通过。

## L0 答案锚点

完整证据包含两次独立状态：认证后受保护页面可见，退出后访问同一路由回到登录页。只截图登录页、只看到导航或只检查 Cookie 任一项都不足。高风险错误包括开放注册、共享管理员密码、把浏览器关闭当作服务端会话已撤销。

## L1 答案锚点

- Credential 保存秘密并被节点引用；静态变量提供部署级非秘密配置；Runtime/请求覆盖只在明确作用域内改变运行值；API Key 控制 API 调用，不替代 Provider Credential。
- 变量故障的根因应落在“最终解析键不存在或作用域不匹配”，修复是更正引用或作用域，而不是把值写入 Prompt。
- 清理证据必须覆盖对象本身与引用它的流程。

## L2 答案锚点

合格流程能在保存后重开，节点和边不丢失；成功执行记录中节点顺序、输入输出和最终回答一致。缺失 Credential 的失败应在模型调用前终止，不能产生未解释 Provider 费用。若学员连续点击重试而未读取首个失败节点，诊断项不得分。

## L3 答案锚点

有答案问题应在 retrieved context 中出现正确片段；无答案问题应触发保守回答而非编造；跨部门问题应受 metadata 过滤。维度错误修复必须使 Embedding 与既有集合维度一致，或在清理旧集合后重新 Upsert，不能在未知残留上反复写入。

## L4 答案锚点

确定性风险等级使用 Condition；只有语义模糊输入才进入 Agent Condition。Iteration 有数量和费用上限；Execute Flow 无循环调用；写入 Tool 位于 HITL 之后且使用幂等键。Sticky Note 不应出现在执行路径。Flow State 只宣称本次执行内共享，跨执行持久化必须另有证据。

## L5 答案锚点

第一次更新返回成功回执；同一幂等键和相同请求返回同一业务结果且不重复写入；同一键不同请求返回冲突。把 409 当作系统失败并换新幂等键重试，会破坏“恰好一次”目标，应扣除副作用控制分。

## L6 答案锚点

Proceed 从原 `STOPPED` 执行继续并触发一次受控写入；Reject 终止且不写；无权限 Resume 被拒绝。新建相似流程、编辑原流程版本后继续或用管理员代替学员审批，都不能证明原执行恢复合同。

## L7 根因报告范例结构

1. **症状：**用户看到检索结果为空。
2. **第一处异常：**Retriever 输出为空，而前置查询文本正确。
3. **排除：**模型节点尚未运行，故不是最终 Prompt 问题。
4. **根因：**文档库状态 stale，最近 Upsert 使用了不同 Embedding 维度。
5. **最小修复：**清理课程向量集合，以固定 Embedding 重新 Process/Upsert。
6. **回归：**Retrieval Playground 命中固定片段，Chatflow 回答引用该片段。
7. **清理：**删除课程集合与上传文件，残留查询为零。

报告把根因写成“RAG 坏了”或“重启后好了”不得分。

## L8 答案锚点

只有同时出现已绑定 reservation、Provider/模型、token、延迟、实际费用、settlement 回执、Provider 用量摘要和受信隔离执行器签名，才算真实实验。若凭据或隔离环境门禁未通过，正确答案是停止并说明阻断，不是用生产或个人 Key 补做。DeepSeek/Kimi 的比较只对同一合成输入和同一验收 Schema 有意义。

## 评分裁决表

| 情况 | 处理 |
| --- | --- |
| 主链正确、证据完整、清理为零 | 主链与证据满分 |
| 结果正确但无执行记录或外部回执 | 主链最多一半 |
| 能定位根因但未做回归 | 诊断得分，恢复不得分 |
| 误用真实数据、泄露秘密或越权 | 安全项 0 分，停止实验 |
| 未结算 Provider reservation | 清理项 0 分，不得结业 |
| 明确识别外部门禁并安全停止 | 按正确风险决策给分 |

## 结业测验参考要点

1. Credential、Variable、API Key 分别回答“秘密、配置作用域、API 访问”。
2. 画布验证只说明结构/参数检查，不证明网络、凭据、配额和 Provider 响应。
3. RAG 先看 retrieved context，因为最终模型只能基于收到的上下文回答。
4. HITL 核对原执行、流程版本、Session、审批内容和权限。
5. Tool 幂等键防止超时或重试造成重复副作用。
6. 401 优先认证与会话；403 优先已认证后的角色、权限与资源范围。
7. PR 构建是候选证据；Pages 发布还需 main、人工环境审批、mike 和发布后复核。
8. 生产只读可确认运行态，不应通过创建对象或调用 Provider来证明培训内容。

## 来源与验证

评分锚点引用 `CLM-007/015/020/023`，强调证据层级、会话隔离、RAG 分层与副作用控制。正式截图和新版本差异仍受外部门禁约束。
