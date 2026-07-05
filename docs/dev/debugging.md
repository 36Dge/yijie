# Debugging

## 链路定位

排查跨服务问题时先收集：

- `trace_id`
- `request_id`
- `tenant_id`
- `task_id`
- `agent_session_id`
- `codex_thread_id`

## 常见方向

- Desktop 是否创建了任务；
- API 是否持久化任务状态；
- Agent Host 是否成功连接 Codex app-server；
- Connectors 是否触发限流或鉴权失败；
- Knowledge 是否有对应版本和 citation；
- Audit log 是否记录工具调用。
