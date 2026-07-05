# 可观测性

## Trace

所有跨服务请求必须贯穿 `trace_id` 和 `request_id`，并在任务链路中携带 `tenant_id`、`user_id`、`task_id`、`agent_session_id` 和 `codex_thread_id`。

## 指标

| 模块 | 指标 |
|---|---|
| API | QPS、P95、P99、错误率 |
| Agent Host | task success rate、event lag、runtime crash count |
| Codex Runtime | turn duration、tool call count、runtime error |
| Connectors | API quota、rate limit、external error、retry count |
| Knowledge | retrieval latency、hit rate、citation coverage |
| Desktop | crash rate、update success rate、sidecar health |
| Skills | eval score、approval rate、tool failure rate |

## 日志分类

- application log
- access log
- audit log
- security log
- agent event log
- tool call log
- external api log
