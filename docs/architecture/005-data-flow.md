# 数据流

## Listing 诊断 MVP

```text
Desktop Chat
  -> yijie-api task
  -> yijie-agent-host session
  -> yijie-codex runtime
  -> yijie-skills listing diagnosis
  -> yijie-connectors public listing fetch
  -> yijie-knowledge retrieval
  -> yijie-agent-host event stream
  -> yijie-api audit log
  -> Desktop report view
```

## Trace 字段

跨服务请求必须携带：

- `trace_id`
- `request_id`
- `tenant_id`
- `user_id`
- `task_id`
- `agent_session_id`
- `codex_thread_id`

## 数据约束

- Fixtures 只能使用合成数据；
- Eval 数据集不得包含真实商家敏感数据；
- 本地 mock 平台 API 不得使用真实 token；
- Knowledge 的政策类回答需要 citation。
