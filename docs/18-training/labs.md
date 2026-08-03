---
title: 学员实验手册
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: intermediate
duration: "10 小时"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - training-environment-user
cost_class: budget-controlled
side_effects:
  - creates-training-resources
  - may-call-provider
last_verified: "2026-08-04"
evidence_ids:
  - CLM-006
  - CLM-007
  - CLM-013
  - CLM-018
  - CLM-023
screenshot_ids: []
---

# 学员实验手册

## 共用起始状态

每组只使用分配的合成命名空间，例如 `班次-组号-对象类型`。开始前记录培训版本、角色、预算余额和基线对象数；结束时用同一查询复核。实验中不得粘贴真实 Key、邮箱、客户文档、内网 URL 或生产资源 ID。

| 实验 | 预计时间 | 外部调用 | 主要产出 |
| --- | ---: | --- | --- |
| L0 登录与导航 | 20 分钟 | 无 | 登录、退出与受保护路由回执 |
| L1 凭据与变量 | 40 分钟 | 无 | 遮罩凭据与变量作用域表 |
| L2 最小 Chatflow | 75 分钟 | 可选 1 次 | 可重开的最小流程与执行记录 |
| L3 文档库与 RAG | 90 分钟 | Embedding/模型 | 检索对照表 |
| L4 Agentflow 条件分流 | 120 分钟 | 模型 | 13 节点边界表与分流执行 |
| L5 Tool 与 MCP | 75 分钟 | 模拟 API | 查询和幂等更新回执 |
| L6 HITL 恢复 | 60 分钟 | 可选 | Proceed/Reject 两条证据 |
| L7 执行诊断 | 60 分钟 | 由 fixture 决定 | 根因报告 |
| L8 Provider 切换 | 45 分钟 | DeepSeek/Kimi | 成本、延迟和降级对照 |

## L0：管理员登录与会话边界

**目标：**证明登录、受保护页面、退出和退出后拒绝是四个独立检查点。

1. 确认地址、版本提示和“注册关闭”说明，不尝试创建新用户。
2. 用分配的培训管理员登录，进入“对话流程”。
3. 记录当前页面标题与可见的十个主模块，不记录 Cookie 值。
4. 从个人菜单退出；直接访问受保护路由。
5. 确认回到登录页，再安全关闭浏览器会话。

**验收：**登录成功、受保护页面可见、退出成功、退出后路由被拒绝；控制台无未解释错误。**清理：**Cookie/local storage 清空，数据库会话数回到基线。

## L1：凭据、变量与 API 密钥

**目标：**区分三类对象的职责与生命周期。

1. 创建只含合成值的课程 Credential，确认 UI 只显示遮罩。
2. 创建静态变量 `training_department`，值为虚构部门。
3. 在测试流程中设置 Runtime 变量，并用请求级覆盖替换一次。
4. 从执行记录核对最终值来源；不得通过截图暴露值。
5. 创建仅关联课程流程的 API Key，验证未关联流程不可访问。

**故障注入：**把 Runtime 变量名改错一个字符。**诊断：**从节点输入追踪，而不是把值硬编码进 Prompt。**清理：**删除 API Key、Credential 和变量，确认引用关系为零。

## L2：最小 Chatflow

**目标：**完成“构建—保存—重开—运行—诊断”的完整闭环。

1. 新建空白 Chatflow，添加输入、聊天模型和输出所需节点。
2. 绑定课程 Credential，设置最小 Prompt 和模型参数。
3. 连接节点并运行画布验证，保存后返回列表。
4. 从列表重新打开，确认节点、边和参数仍在。
5. 输入虚构企业问题，记录回答、耗时、token 和来源。
6. 打开执行记录，核对每个节点输入输出。

**失败分支：**移除 Credential 后运行一次，保存错误证据，再恢复。**验收：**成功执行与预期失败均可解释。**清理：**删除流程和测试消息；若 Provider 门禁未通过，本实验只使用模拟响应。

## L3：文档库与 RAG

**目标：**证明文档加载成功、向量写入成功和检索可用不是同一件事。

1. 创建课程文档库并选择固定中文手册。
2. 配置 Loader；在 Chunk Preview 中比较两种切块大小。
3. 为每块增加 `department`、`document_version` 和 `public_safe` metadata。
4. 选择固定 Embedding、Vector Store 和 Record Manager，执行 Process/Upsert。
5. 在 Retrieval Playground 测试“有明确答案”“无答案”“跨部门”三个问题。
6. 把文档库接入 Chatflow，并比较 retrieved context 与最终回答。

**故障注入：**使用维度不匹配 fixture。**诊断顺序：**状态 → Embedding → 向量集合 → Upsert 历史 → 查询参数。**验收：**提交召回结果、答案一致性和无答案策略。**清理：**删除向量集合、文档库和上传文件，不留下 stale 记录。

## L4：Agentflow V2 条件分流

**目标：**构建普通工单直答、高风险工单人工审批的流程。

1. Start 定义 `ticket_id`、`summary`、`risk_level` Schema。
2. 在 Flow State 表中记录每个字段的写入者、读取者和类型。
3. 用 Condition 处理明确风险等级；无法判断才进入 Agent Condition。
4. 用 Retriever 获取合成政策，用 LLM 生成结构化建议。
5. 普通工单走 Direct Reply；高风险工单进入 HITL。
6. 批量标签使用 Iteration，并设置最大 5 项和失败策略。
7. 用 Execute Flow 调用只读摘要子流程，验证无递归。
8. 在 Sticky Note 中记录教学说明，确认它不参与执行。

**节点检查：**对 Start、Agent、LLM、Condition、Agent Condition、Direct Reply、Custom Function、Tool、Retriever、Sticky Note、HTTP、Iteration、Execute Flow 分别填写“输入、输出、失败、副作用”。**清理：**停止执行，禁用触发器，删除父子流程和等待审批项。

## L5：Tool 与 MCP 工单服务

**目标：**先证明只读查询，再证明受控写入具有幂等性。

1. 查看模拟工单 API `/health`，确认只绑定 loopback 和合成数据。
2. 创建查询 Tool，参数只允许 `TKT-` 合成编号。
3. 在 Chatflow 中调用查询并核对外部回执。
4. 配置课程 MCP Server，完成授权、工具发现和查询。
5. 创建更新 Tool，要求 `classification`、`reason` 和幂等键。
6. 对同一幂等键发送两次相同请求，确认只产生一次业务变更。
7. 用同一幂等键发送不同请求，确认得到冲突而非覆盖。

**安全检查：**URL 不得指向私网、元数据地址或生产；返回值不得包含 Token。**清理：**删除 Tool/MCP 对象，重置模拟 API，确认 generation 与对象状态回到新基线。

## L6：HITL Proceed、Reject 与 Resume

**目标：**从原执行恢复，而不是复制流程绕开等待状态。

1. 运行一条高风险工单，使执行进入 `STOPPED`。
2. 记录执行 ID 的合成别名、流程版本、Session 和待审批摘要。
3. 用授权角色执行 Proceed，确认后续 Tool 只写入一次。
4. 新建第二条执行并 Reject，确认写入 Tool 未触发。
5. 构造权限不足 fixture，确认 Resume 被拒绝。

**验收：**Proceed、Reject、权限拒绝三条状态链完整；不记录真实资源 ID。**清理：**无等待中的执行，模拟工单恢复。

## L7：从执行记录定位根因

每组领取一个未知 fixture。依次回答：症状是什么、第一处异常节点在哪里、该节点收到什么、它调用了什么、外部回执是什么、最小修复是什么、复跑是否改变副作用。只允许一次修复后复跑；在根因未定位前禁止连续重试。

**报告模板：**版本 → 输入分类 → 时间线 → 首个异常 → 排除证据 → 根因 → 修复 → 回归 → 清理。评分重点是证据链，不是“最终能运行”。

## L8：DeepSeek 与 Kimi 切换

本实验只有在 `provider_credentials`、隔离环境和预算门禁通过时开放。

1. 在排他锁内为单次调用预留最坏费用。
2. 用同一合成 Prompt 分别执行 DeepSeek 主线与 Kimi 备用线。
3. 记录模型、输入/输出 token、延迟、实际费用和成功/失败状态。
4. 实际费用结算到原 reservation；未发起网络调用才能 release。
5. 比较结构化输出、延迟、费用和降级条件，不比较真实客户数据。

**停止条件：**累计已花费加 pending／in_flight 预留达到 ¥300、两家账户子限额合计超过 ¥300、关闭自动充值或受信执行签名无回执、凭据来源不明、费用无法计算，或任何真实数据进入请求。当前仓库状态为阻断等待安全凭据，因此不得把本页当作已完成 Provider 实验的证据。

## 全班清理验收

- [ ] 所有实验对象均能从创建 ledger 对应到删除回执。
- [ ] Credential、API Key、变量、MCP Token 和浏览器会话为零。
- [ ] Schedule、Webhook、HITL、执行和 Provider reservation 无悬挂状态。
- [ ] 文档、向量、上传文件、Tool 写入和模拟工单恢复基线。
- [ ] 任何不确定残留都按“未清理”处理并升级给讲师。

## 来源与验证

实验设计引用 `CLM-006/007/013/018/023`。正式版逐步截图必须来自与精确候选提交相同的隔离环境；当前实验文本不代表 Provider 或截图门禁已经通过。
