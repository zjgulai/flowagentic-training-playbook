---
title: PRD-1 竞品情报雷达
description: 竞品情报雷达 Agent 设计与 SOP，监控 Medela、Spectra 等竞品定价、评价、内容动态，输出 Momcozy 差异化机会和反制行动。
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

# PRD-1：竞品情报雷达

**生产地址**：`https://flowise.lute-tlz-dddd.top/chatbot/59cf963a-f0de-4134-96af-81ee6c20b572`

## 适用场景

- 每周竞品监控例会前快速生成报告
- 竞品改价/新品发布后的实时分析
- 制定反制广告策略前的情报收集

## Flow 架构

```
[用户输入：竞品名称]
         ↓
[RequestsGet Tool] ← 网页搜索爬虫
         ↓
[Tool Agent (DeepSeek)] ← 搜索+分析双功能
         ↑
[BufferMemory] ← 支持多轮追问（⚠️ 必须接，否则崩溃）
         ↓
[输出：竞情分析报告]
```

!!! warning "必须连接 BufferMemory"
    `toolAgent` 节点在没有连接 Memory 时会在运行时崩溃（`memoryKey undefined`），**即使你不需要记忆对话，也必须接一个 BufferMemory 节点**。这是平台 3.1.3 版本的已知 Bug。

## 操作 SOP

### Step 1：输入竞品名称

```
帮我分析 [竞品名] 的最新动态和用户评价
```

支持的竞品：Medela、Spectra、Lansinoh、Haakaa、Willow、Elvie

### Step 2：Agent 自动搜索

Agent 会自动搜索以下内容：
- Amazon 评价页（用户差评关键词）
- Reddit 讨论（真实用户体验）
- 竞品官网/社交媒体（营销策略）

### Step 3：解读报告

输出包含：
1. **近期动态 3 条**：附来源和时间
2. **差评痛点 TOP5**：Momcozy 的机会点
3. **差异化建议 2 条**：具体可执行的行动
4. **立即反制 1 条**：今天就能做的

## 提升搜索质量（升级建议）

当前使用 `requestsGet` 爬 Google 搜索结果页，受 robots.txt 限制，数据质量不稳定。

**推荐升级**：接入 **Tavily API**（结构化搜索，返回干净的网页内容）：
1. 在 [tavily.com](https://tavily.com) 注册获取免费 API Key
2. 在 FlowAgentic 创建 `tavilyApi` 凭证
3. 将 `requestsGet` 替换为 `tavilyAPI` 节点

## 实测输出质量

测试：「分析 Spectra S2 在 Amazon 的用户评价」

| 输出内容 | 质量评估 |
|---------|---------|
| 竞品动态（3条） | ✅ 精准，含配件转接头市场机会等深度洞察 |
| 差评 TOP5 | ✅ 直接引用用户原声，可信度高 |
| 差异化建议 | ✅ 提出「Spectra 转接头套装」等具体策略 |
| 反制行动 | ✅ 具体的 Amazon 和 TikTok 操作建议 |
