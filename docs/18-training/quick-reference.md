---
title: 课中速查与清理卡
audience:
  - beginner
  - builder
  - developer
  - admin
difficulty: beginner
duration: "10 分钟"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - training-environment-user
cost_class: low
side_effects:
  - guides-training-actions
last_verified: "2026-08-04"
evidence_ids:
  - CLM-002
  - CLM-015
  - CLM-023
  - CLM-024
screenshot_ids: []
---

# 课中速查与清理卡

## 先选对象

| 需求 | 首选 | 不要混淆 |
| --- | --- | --- |
| 单一对话/RAG 链 | Chatflow | 不等于可自主调用多工具的 Agent |
| 条件、循环、HITL、子流程 | Agentflow V2 | 不用模型替代明确条件 |
| 封装模型、指令、知识和工具 | Assistant | 先确认文档库已 Upsert |
| 保存 Provider 秘密 | Credential | 不写入变量、Prompt 或截图 |
| 非秘密部署配置 | 静态变量 | 请求覆盖有独立作用域 |
| 调用已发布流程 | API Key | 不替代 Flow/Provider Credential |
| 可追踪文档检索 | Document Store | Loader 成功不等于检索成功 |
| 外部动作 | Tool/MCP/HTTP | 先标注只读、写入、费用和清理 |

## 每次操作前的五问

1. 我正在什么版本和环境？
2. 当前角色是否有权限，功能是否启用？
3. 会调用 Provider、写外部系统或产生费用吗？
4. 成功证据在哪里，失败从哪里回退？
5. 创建的对象由谁、何时、怎样清理？

答不出任一项，就先停止操作。

## 五分钟诊断

1. 固定症状、时间、流程版本、Session 和输入分类。
2. 在执行树找到第一个异常节点，不从最后错误倒猜。
3. 核对该节点的实际输入、解析后的变量和 Credential 引用。
4. 区分本地验证、Flowise 服务、Provider、Tool/MCP、数据库和浏览器网络层。
5. 选择最小修复，只复跑一次，并比较副作用与费用。

## 常见状态与动作

| 状态/响应 | 优先检查 | 禁止动作 |
| --- | --- | --- |
| 401 | 登录、Cookie、token 到期、API Key | 公开分享认证材料 |
| 403 | 角色、权限、工作空间、对象范围 | 用管理员绕过验证 |
| 409 | 幂等键、对象版本、并发更新 | 换键制造重复写入 |
| 429 | Provider/登录限流、预算、重试策略 | 无限重试 |
| RAG 空 | 状态、Upsert、Embedding、集合、过滤 | 直接加长 Prompt |
| STOPPED | 原执行、HITL、版本、Session、审批者 | 新建流程冒充恢复 |
| Streaming 无内容 | HTTP 状态、事件序列、错误/中断 | 只检查首 token |

## Provider 预算卡

- 调用前：在排他锁内 reserve 最坏费用。
- 调用后：以同一 experiment ID settle 实际费用。
- 未发起网络请求：才允许 release。
- `spent + pending + in_flight reservations` 不得超过 ¥300；账户级硬限额与关闭自动充值必须另有回执。
- CI、站点和 PDF 构建永不调用 Provider。
- 凭据、请求 ID、Token 和真实数据不进入公开 ledger。

## 高风险节点卡

- Agent/LLM：限制步数、token、费用和结构化输出。
- Tool/HTTP/MCP：限制目标、超时、重试、幂等和返回字段。
- Iteration：限制项目数、单项失败策略和总预算。
- Execute Flow：固定输入输出、权限和无递归。
- Retriever：核对 metadata、Top K、权限和空召回。
- HITL：从原执行恢复，分别验证 Proceed 与 Reject。

## 下课清理顺序

1. 禁用 Schedule、Webhook 和公开入口。
2. 停止运行中 Agentflow 和等待中的 HITL。
3. 删除外部模拟写入，再删 Tool/MCP。
4. 删除 Chatflow、Agentflow、Assistant 和执行记录。
5. 删除文档库、向量集合、上传文件和 Upsert 历史。
6. 撤销 API Key、Credential、变量和浏览器会话。
7. 结算或安全释放 Provider reservation。
8. 以基线查询确认残留为零，并由另一人复核。

如果对象归属不明、删除会影响共享基线或外部写入状态不确定，停止清理并升级给讲师，不能“先删再说”。

## 证据等级速查

| 证据 | 能证明 | 不能证明 |
| --- | --- | --- |
| 页面可见 | 路由和渲染 | 权限、保存、外部调用 |
| UI 成功提示 | 前端收到成功响应 | 数据库、Provider 或业务系统最终状态 |
| 执行记录 | 节点运行、输入输出、错误 | 生产发布与长期稳定性 |
| 外部回执 | 对端接受或完成动作 | 无重复副作用，除非有幂等证据 |
| 发布回执 | 特定版本完成发布流程 | 所有角色和业务场景均正确 |

## 来源与验证

本卡引用 `CLM-002/015/023/024`。公开版只保留安全原则与合成标识；真实运维步骤继续使用私有 Runbook 受控编号。
