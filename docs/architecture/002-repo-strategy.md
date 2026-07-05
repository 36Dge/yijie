# 多仓策略

## 仓库结论

易界 AI 使用 11 个仓库：

| 仓库 | 职责 |
|---|---|
| yijie | 元仓库、多仓入口、架构治理 |
| yijie-codex | Codex 上游 fork 和 Runtime 内核 |
| yijie-desktop | Mac 桌面端，Tauri + Vue |
| yijie-admin-web | 内部管理后台，Vue |
| yijie-api | Go 业务后端，模块化单体优先 |
| yijie-agent-host | Codex Runtime 薄宿主适配层 |
| yijie-skills | 跨境电商 Skills、Plugins、Prompt Packs、Evals |
| yijie-connectors | 平台和三方 API 连接器、MCP 工具服务 |
| yijie-knowledge | RAG 知识库、规则库、政策库、检索服务 |
| yijie-contracts | OpenAPI、Protobuf、JSON Schema、SDK |
| yijie-infra | IaC、K8s、CI/CD、观测和安全配置 |

## 不拆的内容

MVP 阶段不把 Amazon、Temu、Shopee、TikTok Shop 拆成多个连接器仓库；先放在 `yijie-connectors` 内按模块隔离。

## 依赖方向

```text
frontend -> contracts -> api
api -> agent-host / connectors / knowledge
agent-host -> codex / skills / connectors / knowledge
skills -> contracts / connector schemas / knowledge schemas
connectors -> contracts
knowledge -> contracts
infra -> deploys all service repos
```

`yijie-codex` 不依赖任何易界业务仓。
