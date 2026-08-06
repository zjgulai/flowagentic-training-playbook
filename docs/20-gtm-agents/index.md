---
title: GTM Agent 设计与实战
description: 跨境电商品牌 GTM Agent 完整方法论，以 Momcozy 为案例，涵盖竞品情报、新品上市、KOL 匹配三类 Agent 的设计、踩坑和 SOP。构建 GTM Agent 前必读。
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

# GTM Agent 设计与实战

> 本章以 **Momcozy（跨境母婴品牌）** 为真实案例，记录在 FlowAgentic 平台上从零构建 3 个生产级 GTM Agent 的完整过程：设计决策、遇到的问题、逐条修复方案，以及可直接复用的 SOP。

## 为什么需要 GTM Agent？

跨境电商团队的 GTM 痛点：

| 痛点 | 手动耗时 | Agent 后 |
|------|---------|---------|
| 竞品定价/评价监控 | 2-3 天/周 | 10 分钟/次 |
| 新品 Amazon Listing + TikTok 脚本 | 3-5 天 × 3 人 | 30 分钟 |
| KOL 筛选 + 外联模板 | 2 周 | 2 小时 |

---

## 三个核心 Agent

| Agent | 类型 | 核心节点 | 生产地址 |
|-------|------|---------|---------|
| [PRD-1 竞品情报雷达](./prd1-competitor.md) | Tool Agent | RequestsGet + DeepSeek | `chatbot/59cf963a-...` |
| [PRD-2 新品上市 GTM Launcher](./prd2-gtm-launcher.md) | Conversation Chain | DeepSeek + BufferMemory | `chatbot/edf2357f-...` |
| [PRD-3 KOL 智能匹配系统](./prd3-kol-matching.md) | Tool Agent + TikHub | RequestsGet × 2 + DeepSeek | `chatbot/a70a9e99-...` |

---

## 平台能力速查（FlowAgentic 3.1.3）

### 可用 Chat Models（已验证）

| 节点 name | 说明 | credentialName |
|-----------|------|----------------|
| `chatDeepseek` | DeepSeek Chat/Reasoner | `deepseekApi` |
| `chatKimi` | Kimi / Moonshot | `kimiApi` |

### 可用 Agent 类型

| 节点 name | 适用场景 |
|-----------|---------|
| `toolAgent` | 有工具调用需求（搜索、API） |
| `reactAgentLLM` | 需要推理链（CoT）的复杂任务 |
| `conversationChain` | 纯对话、内容生成，不需要工具 |

### 可用 Tools（与外部数据交互）

| 节点 name | 说明 |
|-----------|------|
| `requestsGet` | HTTP GET 请求，可设置 Headers（用于 TikHub 等 API） |
| `customTool` | 自定义代码工具（JavaScript/Python） |
| `tavilyAPI` | Tavily 搜索 API（结构化网页搜索，需 API Key） |
| `serpAPI` | SerpAPI 搜索（Google 结果，需 API Key） |

---

## 关键踩坑与修复（必读）

构建过程中遇到的 6 个 Bug，全部已修复：

### Bug 1：500 错误 `filePath undefined`

**现象**：Flow 创建成功但调用时报 `Cannot read properties of undefined (reading 'filePath')`

**根因**：节点的 `data.name` 写错了。FlowAgentic 节点名称不等于 UI 显示名：
```
❌ 错误：name: "Deepseek"
✅ 正确：name: "chatDeepseek"
```

**查询正确节点名的方法**（在服务器上执行）：
```bash
docker exec flowise-chinese node -e "
const {NodesPool} = require('{api-key-value}');
const pool = new NodesPool();
pool.initialize().then(() => {
  Object.keys(pool.componentNodes).forEach(k => console.log(k));
  process.exit(0);
});
"
```

### Bug 2：`inputParams.find is not a function`（500 错误）

**现象**：调用时报 `Cannot read properties of undefined (reading 'find')` at `resolveVariables`

**根因**：节点 `data` 里缺少 `inputParams` 字段。FlowAgentic 在运行时需要从 `inputParams`（节点 schema）里查找字段的 `acceptVariable` 属性。

**修复**：每个节点必须包含完整的 `inputParams` 数组（来自节点定义的 `inputs` schema）：
```python
## 获取节点的完整 inputParams
docker exec flowise-chinese node -e "
const {NodesPool} = require('...');
pool.initialize().then(() => {
  const n = pool.componentNodes['chatDeepseek'];
  const inst = new (require(n.filePath)).nodeClass();
  console.log(JSON.stringify(inst.inputs));
});
"
```

### Bug 3：LangChain prompt variable 冲突

**现象**：System Message 中的 `{username}` 导致 500 报错 `Missing value for input variable`

**根因**：LangChain 的 ChatPromptTemplate 会将 `{花括号}` 内容识别为 prompt 变量，找不到对应值就报错。

**修复**：用描述性占位符替代，如 `HANDLE` 代替 `{username}`，`ACCOUNT_NAME` 代替 `{account}`。

### Bug 4：Tool Agent 无 Memory 时崩溃

**现象**：`TypeError: Cannot read properties of undefined (reading 'memoryKey')`

**根因**：`ToolAgent.js` 的 `init()` 方法无条件访问 `memory.memoryKey`，当 memory 连接为空时崩溃。

**修复**：**即使 Tool Agent 不需要记忆对话，也必须连接一个 BufferMemory 节点**：
```
BufferMemory → toolAgent (memory input)
```

### Bug 5：outputAnchors ID 格式

**节点 sourceHandle 的正确格式**：
```
{nodeId}-output-{nodeName}-{baseClasses joined by |}

例：
ds_0-output-chatDeepseek-chatDeepseek|ChatOpenAICompletions|BaseChatOpenAI|BaseChatModel|BaseLanguageModel|Runnable
mem_0-output-bufferMemory-BufferMemory|BaseChatMemory|BaseMemory
```

**获取正确 anchor ID 的方法**：
```bash
docker exec flowise-chinese node -e "
const {NodesPool} = require('...');
pool.initialize().then(() => {
  const n = pool.componentNodes['chatDeepseek'];
  const inst = new (require(n.filePath)).nodeClass();
  const base = inst.baseClasses.join('|');
  console.log('nodeId-output-' + inst.name + '-' + base);
});
"
```

### Bug 6：API Key 权限（403 Forbidden）

**现象**：用 API Key 调用 `/api/v1/chatflows` 等端点返回 `{"message":"Forbidden"}`

**根因**：API Key 的 `permissions` 字段需要包含对应操作的权限字符串。

**修复**：在数据库中更新 API Key 权限：
```sql
UPDATE apikey SET permissions = '["chatflows:create","chatflows:view","credentials:view",...]'::jsonb
WHERE "keyName" = 'your-key-name';
```

常用权限列表（按路由 checkPermission 要求）：
- `chatflows:view/create/update/delete`
- `agentflows:view/create/update/delete`
- `credentials:view/create/update/delete`
- `tool:view/create/update/delete`

---

## 外部数据源接入

### TikHub API（社媒数据）

- **文档**：https://api.tikhub.io/docs
- **认证**：`Authorization: Bearer {token}`（在 requestsGet 节点的 headers 中配置）
- **已验证 Endpoints**：

```
## TikTok 博主资料
GET https://api.tikhub.io/api/v1/tiktok/web/fetch_user_profile?uniqueId={handle}

## TikTok 搜索用户（按关键词）⭐ 包含 follower_count
GET https://api.tikhub.io/api/v1/tiktok/web/fetch_search_user?keyword={kw}&count=10

## TikTok 热搜词
GET https://api.tikhub.io/api/v1/tiktok/web/fetch_trending_searchwords

## Instagram 用户信息
GET https://api.tikhub.io/api/v1/instagram/v1/fetch_user_info_by_username?username={handle}
```

**重要注意事项**：
- `fetch_search_user` 返回的 `user_info.follower_count` **是准确的实时数据**
- `fetch_user_profile` 对于某些账号返回 `statusCode: 10221`（账号不存在或名称错误）
- Instagram v2/v3 端点有时返回空数据，优先用 v1

### 数据验证结果（已测试真实博主）

| 博主 | 平台 | 粉丝 | TikHub 准确性 |
|------|------|------|------|
| @lactationlink | Instagram | 113,913 | ✅ 准确 |
| @momcozyofficial | TikTok | 445,000 | ✅ 准确（Momcozy 官方账号）|
| @momcozyshop | TikTok | 388,000 | ✅ 准确 |
| @daniela.soho | TikTok | 10,000 | ✅ 准确 |

---

## API 访问方式

FlowAgentic 使用 **JWT Cookie（HttpOnly）** 认证，通过编程创建 API Key 的完整流程：

1. 在容器内生成正确格式的 API Key（使用 scryptSync）：
```bash
# 在 Flowise 容器内生成 API Key
docker exec flowise-chinese node -e "
const {randomBytes, scryptSync} = require('crypto');
const key = randomBytes(32).toString('base64url');
const salt = randomBytes(8).toString('hex');
const buf = scryptSync(key, salt, 64);
const hash = buf.toString('hex') + '.' + salt;
console.log('生成完成，key='+key.substring(0,8)+'...');
"
```

2. 插入数据库（将生成的 key 和 hash 填入）：
```sql
INSERT INTO apikey (id, "apiKey", "apiSecret", "keyName", "updatedDate", "workspaceId", permissions)
VALUES (uuid_generate_v4(), '[生成的key]', '[生成的hash]', 'my-key', NOW(), '[工作区ID]', '[...]'::jsonb);
```

3. 使用：
```bash
curl -H "Authorization: Bearer [your-generated-key]" https://flowise.example.com/api/v1/chatflows
```
