---
title: Agentflow V2
audience:
  - builder
  - developer
difficulty: advanced
duration: "150 分钟"
release_version: "3.1.3"
release_sha: "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - creates-and-updates-agentflow
  - may-call-provider
  - may-write-external-system
last_verified: "2026-08-04"
evidence_ids:
  - CLM-005
  - CLM-006
  - CLM-018
  - CLM-023
screenshot_ids: []
---

# Agentflow V2

## 心智模型

Agentflow V2 把“什么时候开始、怎样判断、执行什么、怎样循环、何时等待人工、怎样调用子流程”显式画在控制流中。Flow State 保存本次运行中的状态；Session 用于关联多轮或多次交互；持久状态是否跨运行存在必须按节点和部署配置验证。

## 13 个核心节点

| 节点 | 作用 | 关键输入 | 主要风险 |
| --- | --- | --- | --- |
| Start | 定义 Chat、Form、Webhook、Schedule 等触发入口 | 触发类型、输入 Schema | 未授权触发、输入未校验 |
| Agent | 让模型规划并调用工具 | 指令、模型、工具、记忆 | 不可预测调用、循环、费用 |
| LLM | 单次模型推理或结构化输出 | 提示、模型、输出 Schema | 幻觉、Schema 不匹配 |
| Condition | 按确定性条件分支 | 表达式、状态字段 | 空值和类型判断错误 |
| Agent Condition | 借助模型判断分支 | 判定标准、模型 | 非确定性、额外费用 |
| Direct Reply | 直接返回内容 | 文本或状态引用 | 泄露内部状态 |
| Custom Function | 执行自定义逻辑 | 代码、输入 | 不可信代码、资源消耗 |
| Tool | 调用已定义工具 | Tool、参数 | 外部写入和重复执行 |
| Retriever | 从知识库检索 | 查询、文档库、Top K | 空召回、越权数据 |
| Sticky Note | 画布注释 | 说明文本 | 不参与执行，易被误当逻辑 |
| HTTP | 调用 HTTP 服务 | URL、方法、头、正文 | SSRF、Token 泄露、副作用 |
| Iteration | 逐项迭代集合 | 集合、子步骤、上限 | 无限循环、费用放大 |
| Execute Flow | 调用另一个流程 | 目标流程、输入映射 | 递归、权限和版本漂移 |

以上节点名绑定基线源码中的 Agentflow 包。该精确提交进入同版本隔离环境后必须复核标签、参数和运行语义，再绑定截图。

## 构建 SOP

### 1. 从触发器开始

先定义 Start 的触发类型与输入 Schema，再设计后续节点。Webhook 和 Schedule 在培训环境验证前不能标为生产可用。

### 2. 明确状态契约

为每个 Flow State 字段记录名称、类型、来源、写入节点和读取节点。避免多个节点用同名字段表达不同含义。

### 3. 优先确定性分支

能用 Condition 明确判断的规则，不先用 Agent Condition。模型判定应有置信阈值、无法判断分支和人工复核。

### 4. 控制工具副作用

查询工具与写入工具分开。写入工具要求幂等键、预览、确认、超时和回执；Agent 不应仅凭模糊自然语言直接执行高风险写入。

### 5. 设置循环上限

Iteration 必须定义最大项目数、每项超时、失败策略和总预算。Agent 自我反思循环也需要最大步数。

### 6. 处理 HITL

进入人工审核时，执行状态应变为 `STOPPED`。恢复前核对原流程版本、Session、待审批内容和操作者权限。Proceed、Reject 和 Resume 是不同业务决策，不能只靠按钮颜色区分。

### 7. 验证子流程

Execute Flow 要固定输入输出契约，避免 A 调 B、B 又调 A。目标流程变更后，调用方必须重新做兼容性验证。

## 失败恢复

- 状态字段缺失：回看 Start 和前置节点输出，不直接给空值兜底掩盖错误。
- 无限循环：立即停止执行，检查退出条件和最大步数。
- HITL 无法恢复：核对原执行状态、权限、版本和 Session，禁止新建一条“相似流程”替代恢复。
- Schedule/Webhook 不触发：分层检查开关、注册、时区、认证、网络和服务端日志。
- 子流程失败：保留父子执行关联，分别定位边界输入和内部节点。

## 截图范围

正式版为 13 个节点分别提供“加入画布、关键参数、成功结果、典型失败”截图；Start、Agent、Tool、HTTP、Iteration、Execute Flow 和 HITL 还要覆盖高风险状态。当前未满足 G1 和训练环境门禁，因此不展示任何未经版本绑定和脱敏验收的图片。

## 目标

从明确触发器和状态合同出发，构建可终止、可恢复、可追踪副作用的 Agentflow V2，并能解释 13 个核心节点各自的使用边界。

## 适用角色

流程搭建者负责控制流，开发者负责 Tool／HTTP／函数合同，管理员负责触发入口、权限、费用和外部写入边界。

## 适用版本与功能状态

页面绑定 Flowise `3.1.3`、提交 `6a5bb28b…`。13 个节点名已由目标源码确认；SDK 稳定性和新中文界面仍按 `experimental`／待复验处理。

## 前置条件与风险

需要合成触发数据、Flow State 字段表、最大步数、总预算、工具幂等合同和失败清理方案。Agent、LLM、Retriever、Tool、HTTP 和子流程可能产生费用或外部副作用。

## 初始状态

从 Agentflow 列表新建空白 V2 流程，确认无同名对象、无遗留 schedule/webhook、训练 Provider 未超预算。

## 操作步骤

依次完成 Start Schema、Flow State、确定性分支、模型节点、工具副作用、循环上限、HITL、子流程、验证、保存重开和执行检查；每次只增加一种控制结构。

## 逐步检查点

每个节点记录输入来源、输出目标、失败分支和是否计费／写入；Condition 有兜底分支，Iteration 有上限，Execute Flow 无递归，HITL 能从原执行恢复。

## 成功结果

成功输入到达预期 Direct Reply；失败输入进入明确失败分支；HITL 可 Proceed/Reject；执行树能还原每个节点状态、费用和外部回执。

## 常见错误与诊断

状态缺失从 Start 与前置输出查起；循环不收敛立即停止；工具重复写入检查幂等键；HITL 恢复失败核对执行状态、Session、流程版本和权限。

## 回退与清理

禁用 schedule/webhook，停止运行中执行，恢复上一只读版本；删除本次流程、子流程、工具写入和合成外部对象，复核没有等待中的 HITL。

## 安全提示

查询与写入工具分离；不可信模型输出不能直接决定高风险写入；HTTP 阻断内网和元数据地址；所有循环、重试、子流程和模型调用都有硬上限。

## 练习任务

构建工单条件分流：普通问题直接回复，高风险工单进入 HITL，批准后调用幂等更新工具；补做拒绝、超时和重复恢复测试。

## 验收清单

- [ ] 13 个核心节点均有用途、输入输出、失败和风险说明。
- [ ] 条件、循环、HITL、子流程和副作用路径通过。
- [ ] schedule/webhook、执行、外部对象与费用残留清零。

## 来源与验证

节点集合、Flow State、触发器和副作用引用 `CLM-005/006/018/023`。正式发布需要同版本训练复现与逐节点截图，当前发布门禁保持关闭。
