# 合成工单培训 API

这是“虚构企业知识库与工单处理系统”贯穿案例的本地 mock API。它只读取仓库内的合成工单，不连接真实工单系统，也不会处理个人信息。

代码采用 [MIT](../../LICENSE-CODE) 许可。工单 fixture 和说明文字遵循仓库根目录的内容许可。

## 安全边界

- 服务固定绑定 `127.0.0.1`，不能通过参数改为公网或局域网地址。
- 所有响应都包含 `X-Synthetic-Data: true`，正文也包含 `synthetic_data: true`。
- 启动时会校验每条 fixture 的 `contains_personal_data` 必须为 `false`。
- 写操作必须同时携带公开演示标头和幂等键。
- 公开演示标头只是防误操作护栏，**不是密码、Token 或身份认证机制**，禁止用于生产。
- 状态只保存在进程内存；重启或调用显式重置接口会恢复 fixture。
- 日志不记录请求体和请求标头，避免把后续扩展示例中的数据带入日志。

固定演示标头为：

```text
X-FlowAgentic-Demo: synthetic-training-write
```

## 启动

要求 Python 3.12；不需要安装第三方依赖。在仓库根目录执行：

```bash
uv run python labs/mock-ticket-api/run.py --port 8765
```

也可以在已经激活的 Python 3.12 虚拟环境中使用 `python` 运行同一命令。

默认读取：

```text
data/fixtures/tickets/tickets.json
```

可通过 `--fixture` 指向另一份同结构的纯合成数据。`--rate-limit` 和 `--rate-window` 分别控制写请求窗口内上限和窗口秒数：

```bash
uv run python labs/mock-ticket-api/run.py \
  --port 8765 \
  --rate-limit 20 \
  --rate-window 60
```

服务始终只监听 `127.0.0.1`。若 FlowAgentic 运行在容器中，不能为了连通而把本服务改绑 `0.0.0.0`；应使用隔离网络中另行部署的同等受控 mock 服务。

## API

### 健康检查

```bash
curl --fail --silent http://127.0.0.1:8765/health
```

### 查询合成工单

```bash
curl --fail --silent http://127.0.0.1:8765/tickets/TKT-1001
```

### 更新工单分类

每次业务操作生成一个新的幂等键；网络重试必须复用原键和完全相同的请求体。

```bash
curl --fail-with-body \
  --request PUT \
  --header 'Content-Type: application/json' \
  --header 'X-FlowAgentic-Demo: synthetic-training-write' \
  --header 'Idempotency-Key: lab-update-tkt-1001-001' \
  --data '{
    "category": "检索质量",
    "priority": "高",
    "reason": "合成训练样例",
    "expected_revision": 0
  }' \
  http://127.0.0.1:8765/tickets/TKT-1001/classification
```

同一幂等键和同一请求重放时，服务返回原始回执并附带：

```text
Idempotent-Replayed: true
```

同一幂等键用于不同请求时返回 `409 IDEMPOTENCY_KEY_REUSED`。`expected_revision` 与当前版本不一致时返回 `409 REVISION_CONFLICT`。

### 显式重置

重置会恢复启动时读取的全部合成工单。重置本身也必须幂等：

```bash
curl --fail-with-body \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'X-FlowAgentic-Demo: synthetic-training-write' \
  --header 'Idempotency-Key: lab-reset-session-001' \
  --data '{}' \
  http://127.0.0.1:8765/reset
```

## 错误合同

错误统一返回 JSON：

```json
{
  "error": {
    "code": "REVISION_CONFLICT",
    "message": "工单版本已变化，请重新读取后再提交。",
    "details": {
      "expected_revision": 0,
      "current_revision": 1
    }
  },
  "meta": {
    "synthetic_data": true
  }
}
```

训练用例覆盖：

| HTTP 状态 | 典型原因 |
| --- | --- |
| `400` | 标头、幂等键、JSON、字段或工单编号无效 |
| `404` | 路由或合成工单不存在 |
| `409` | revision 冲突或幂等键被用于不同请求 |
| `429` | 写请求超过进程内滑动窗口上限 |

收到 `429` 时读取 `Retry-After`，等待后使用**原幂等键和原请求体**重试。

## 测试

```bash
uv run python -m unittest discover \
  -s labs/mock-ticket-api/tests \
  -p 'test_*.py' \
  -v
```

测试会在随机空闲端口启动真实 HTTP 服务，覆盖健康检查、读取、写保护、schema 校验、显式重置、幂等重放、版本冲突和限流；不会进行网络外连。
