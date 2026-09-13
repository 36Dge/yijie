# 多仓策略

## 仓库结论

易界 AI 使用 12 个仓库：

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
| yijie-coze | Coze上游源码与工作流引擎适配；FEAT-153 local完整集成及D4已通过 |

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

## 本地拓扑

12 个仓库在同一个父目录下以兄弟目录存在，不使用 Git submodule。`yijie/repos.yaml` 是仓库 URL、路径和默认分支的唯一数据源，`yijie/scripts/bootstrap.sh` 负责初始化缺失仓库。

FEAT-153 首步使用用户提供的 Coze 上游作为 source origin，显式采用其 `main` 分支；其余子仓仍默认 `develop`。
上游源提交由 `yijie-coze/yijie-upstream.lock.json` 固定，不代表其它仓库开始由元仓 pin。
本地恢复 Git 元数据保留了六份既有缺失文档，详见 FEAT-153 源审计。
2026-09-13用户授权创建私有`36Dge/yijie-coze`并提交/推送。清单已指向实际易界仓；本机origin指向易界，upstream保留原始Coze来源，禁止向上游推送本地易界修改。

工作流的候选依赖是 Desktop → API → Coze，外部电商节点后续通过 Connectors；
受控local运行依赖已按FEAT-153逐步接入，真实dev/packaged统一D4见该需求17，Git交付见18。
具体身份、编辑器和数据边界见Accepted [ADR-0019](../adr/ADR-0019-coze-workflow-foundation.md)，不代表公网或生产资格。
