---
title: PRD-2 新品上市 GTM Launcher
description: 新品上市 GTM Launcher 设计与 SOP，输入产品信息，自动输出 Amazon Listing、TikTok 脚本、邮件序列、关键词策略，实测生成 13000 字完整内容包。
audience:
  - builder
  - developer
  - admin
difficulty: advanced
duration: "60 分钟"
release_version: "3.1.3"
release_sha: "96f6ae464f7f4757883a5ba6bec26ca951b4da4d"
feature_status: production-enabled
permissions:
  - admin
cost_class: medium
side_effects:
  - creates-and-updates-flow
  - may-call-provider
last_verified: "2026-08-06"
evidence_ids: []
screenshot_ids: []
---

# PRD-2：新品上市 GTM Launcher

**生产地址**：`https://flowise.lute-tlz-dddd.top/chatbot/edf2357f-6f7e-469d-803c-e642d80b3bb3`

## 适用场景

- 新品上市前需要快速生成多渠道内容
- 运营/市场人员直接在对话框输入产品信息，5-30 分钟获得完整内容包
- 内容输出可直接复制到 Amazon 后台、TikTok 创作工具、邮件营销平台

## Flow 架构

```
[用户输入产品信息]
        ↓
[ChatDeepseek] ← deepseekApi Credential
        ↓
[ConversationChain] ← System Prompt (Momcozy 品牌指令)
        ↑
[BufferMemory]    ← 保持对话上下文（可多轮追问）
        ↓
[输出：完整 GTM 内容包]
```

**节点清单**：

| 节点 ID | name | 类型 | 参数 |
|---------|------|------|------|
| `ds_0` | `chatDeepseek` | Chat Models | model: deepseek-chat, temp: 0.7, maxTokens: 4096 |
| `mem_0` | `bufferMemory` | Memory | memoryKey: chat_history |
| `chain_0` | `conversationChain` | Chains | systemMessagePrompt: Momcozy 品牌 System Prompt |

## 操作 SOP

### Step 1：进入 Chatbot
打开 `https://flowise.lute-tlz-dddd.top/chatbot/edf2357f-...`，显示对话输入框。

### Step 2：输入产品信息

```
我需要为 [产品名称] 生成[内容类型]。

产品信息：
- 产品名：[具体型号]
- 核心卖点：[3-5 条]
- 目标用户：[用户画像]
- 主要竞品区分：[vs 竞品的差异点]
- 价格：[$XX.XX]

需要：[从以下选择]
1. Amazon Listing（Title + Bullets + Description）
2. TikTok 脚本（情感型/测评型/教程型）
3. 邮件序列（5封）
4. 关键词策略（Top20）
5. 全套 GTM 包
```

### Step 3：审查输出

Amazon Listing 审查清单：
- [ ] Title ≤ 200 字符，含核心关键词
- [ ] 每条 Bullet ≤ 250 字符，首词大写
- [ ] 无禁用词（guarantee/cure/best/proven）
- [ ] 品牌声调一致（温暖、真实）

### Step 4：多轮追问优化

对话记忆保持，可以追问：
- "把 Bullet 3 改成更突出静音功能"
- "TikTok 脚本改成测评型"
- "关键词按月搜索量从高到低排序"

## 实测输出质量

测试产品：Momcozy M5 Pro 无线双边电动吸奶器（$119.99）

| 内容类型 | 字数 | 质量评估 |
|---------|------|---------|
| Amazon Title | 183字符 | ✅ 含 6 个核心关键词，规格完整 |
| 5 条 Bullets | 每条 200-245 字符 | ✅ 场景化描述，竞品差异清晰 |
| Description | ~1500 字 | ✅ 品牌故事 + 功能 + 保证，情感共鸣强 |
| 总输出 | 13,051 字 | ✅ 可直接用，修改量 <10% |
