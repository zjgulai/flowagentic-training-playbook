---
title: PRD-3 KOL 智能匹配系统
description: KOL 智能匹配系统设计与 SOP，结合 TikHub API 实时数据搜索筛选适合 Momcozy 的母婴博主，生成外联 DM 模板，包含 TikHub API 端点验证结果。
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
evidence_ids: [CLM-005, CLM-006, CLM-009, CLM-011, CLM-014, CLM-016, CLM-018, CLM-023]
screenshot_ids: []
---

# PRD-3：KOL 智能匹配系统

**生产地址**：`https://flowise.example.com/chatbot/{chatbot-id}`

## 适用场景

- 新品上市前的 KOL 资源储备
- 季度营销活动的博主招募
- 竞品合作 KOL 的反向吸引

## Flow 架构

```
[用户输入：目标博主画像]
           ↓
[Tool Agent (DeepSeek)]
      ↙           ↘
[kol_search]    [tikhub_social_data]
(Google 搜索)   (TikHub API 真实数据)
      ↓                ↓
[汇总分析 + 评分 + 外联模板]
           ↑
    [BufferMemory]
```

**两个工具的分工**：
- `kol_search`（requestsGet）：Google 搜索找候选博主账号名
- `tikhub_social_data`（requestsGet + TikHub Headers）：查询真实粉丝数、互动数据

## TikHub API 配置

在 `tikhub_social_data` 节点的 headers 中配置：
```json
{
  "Authorization": "Bearer {your_tikhub_api_key}"
}
```

**已验证的有效 Endpoints**：

```
## 按关键词搜索博主（⭐ 包含实时粉丝数，最推荐）
GET https://api.tikhub.io/api/v1/tiktok/web/fetch_search_user?keyword={关键词}&count=10

## 查询特定博主（需要精确 uniqueId）
GET https://api.tikhub.io/api/v1/tiktok/web/fetch_user_profile?uniqueId={handle}

## Instagram 博主信息
GET https://api.tikhub.io/api/v1/instagram/v1/fetch_user_info_by_username?username={handle}
```

**注意**：搜索关键词直接影响结果质量。推荐用：
- `pumping mom usa baby`
- `wireless breast pump review`
- `exclusively pumping working mom`

## 操作 SOP

### Step 1：描述目标博主画像

```
帮我找 [数量] 个适合推广 Momcozy [产品名] 的 [平台] 博主。

要求：
- 粉丝量：[X万-X万]
- 内容方向：[育儿/母乳/职场妈妈等]
- 地区：[美国/全球]
- 互动率：≥[X]%
```

### Step 2：Agent 自动搜索和验证

Agent 将：
1. 用 Google 搜索找候选博主账号名
2. 用 TikHub API 验证真实粉丝数
3. 评分（100分制）
4. 输出推荐列表 + 外联 DM

### Step 3：人工复核

| 复核项 | 方法 |
|--------|------|
| 账号是否真实存在 | 直接在 TikTok/Instagram 搜索验证 |
| 粉丝数是否匹配 | TikHub 数据与 App 内显示对比 |
| 有无竞品合作 | 查看博主最近 50 条内容 |
| 有无联系方式 | 看 bio 是否有 email/collabs 链接 |

## 已发现的真实 KOL 数据

通过 TikHub API 验证的真实数据：

| 博主 | 平台 | 粉丝 | 内容方向 |
|------|------|------|---------|
| @momcozyofficial | TikTok | 445,000 | Momcozy 官方账号 |
| @momcozyshop | TikTok | 388,000 | Momcozy 官方店铺 |
| @lactationlink | Instagram | 113,913 | 哺乳/泵奶专业课程 |
| @daniela.soho | TikTok | ~10,000 | exclusive pumping mom，有合作邮件 |
| @pumpwithpurpose | TikTok | ~16,000 | 泵奶专家/产品推荐 |

!!! tip "最高效的 KOL 搜索策略"
    直接用 `fetch_search_user?keyword=pumping+mom+usa` 获取带真实 `follower_count` 的搜索结果，比先找账号名再查 profile 效率高 3 倍。

## 外联 DM 模板（已测试）

Agent 为每个博主生成的个性化模板格式：
```
Hi [Name]! 👋

I'm reaching out from Momcozy, the brand behind the wireless breast pump 
you may have seen trending on TikTok! 

We've been following your [specific content] and love how authentic your 
[specific praise]. Your [follower count] community of moms trusts you, 
and we'd love to partner with you for [specific campaign].

We'd love to send you our [product] to try — completely free. If you love it, 
we can discuss a paid collaboration.

Are you open to a quick chat? 💌
[Contact]
```
