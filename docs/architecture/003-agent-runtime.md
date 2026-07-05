# Agent Runtime 架构

## 结论

易界 AI 使用 Codex Runtime 作为 Agent Runtime 内核，不从 0 自研完整 `yijie-agent-platform`。

## 分工

| 模块 | 责任 |
|---|---|
| yijie-codex | Runtime 内核、上游同步、必要 patch、app-server 能力 |
| yijie-agent-host | 进程管理、任务映射、上下文注入、工具配置、审批和事件转发 |
| yijie-skills | 领域提示词、技能说明、评测数据、输出 schema |
| yijie-connectors | 外部平台 API 调用和 MCP 工具执行 |
| yijie-knowledge | 规则、政策和 SOP 的 RAG 检索 |

## 禁止边界

- 不在 `yijie-codex` 写跨境电商业务逻辑；
- 不在 `yijie-agent-host` 自研 planner、prompt engine 或任务编排平台；
- 不让 Codex Runtime 直接接触平台 token；
- 不让 Skills 直接访问真实商家数据或外部 API。

## 事件映射

`yijie-agent-host` 维护 `yijie_task_id` 与 `codex_thread_id` 的映射，并把 Codex 事件转换为易界任务事件，供桌面端和后台订阅。
