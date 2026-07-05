# 安全边界

## Token 边界

```text
Desktop
  不保存平台 access token

Yijie API
  管理店铺授权状态和租户权限
  不直接暴露 token 给前端或 Codex

Yijie Connectors
  管理 token vault、refresh 和 rotation
  执行平台 API 调用

Yijie Agent Host
  不直接持有平台 token
  只能请求连接器执行工具

Codex Runtime
  不直接接触平台 token
```

## 审批边界

```text
Codex tool call proposal
  -> yijie-agent-host policy check
  -> yijie-api approval task
  -> desktop approval card
  -> user approve / reject
  -> connectors execute
  -> audit log
```

## 日志边界

日志中不得出现 access token、refresh token、cookie、平台密钥、买家邮箱、电话、地址、完整订单号、银行卡或未脱敏经营数据。
