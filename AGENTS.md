# AGENTS.md

## 仓库职责

`yijie` 是易界 AI 的项目元仓库，负责多仓入口、架构治理、跨仓 ADR、开发说明、脚本入口、发布与安全规范。它不承载具体业务代码。

## 禁止事项

- 禁止在本仓库实现桌面端、后台、后端、连接器、RAG 或 Codex Runtime 业务代码；
- 禁止提交真实 token、secret、cookie、access key、平台凭证或真实商家数据；
- 禁止把跨境电商业务逻辑写进 `yijie-codex` 的说明或脚本中；
- 禁止绕过 contract-first、审批策略、审计和日志脱敏要求；
- 禁止在未更新 ADR 或架构文档的情况下改变跨仓边界。

## 技术栈

本仓库以 Markdown、YAML 和 Shell 脚本为主。业务仓库使用 Vue、Go、Tauri、Codex Runtime、RAG、MCP 工具服务、OpenAPI、Protobuf 和 JSON Schema。

## 目录约定

- `docs/architecture/`：跨仓架构说明；
- `docs/adr/`：跨仓架构决策记录；
- `docs/product/`：产品范围和跨境电商 SOP；
- `docs/dev/`：本地开发、测试、调试和 Codex 协作；
- `docs/security/`：安全模型、数据分类、密钥、审计和审批策略；
- `docs/runbook/`：本地和服务故障排查；
- `docs/release/`：发布规范；
- `scripts/`：多仓开发入口脚本；
- `repos.yaml`：兄弟目录多仓清单、远端 URL、默认分支和 Owner 的唯一数据源。
- `apps/`、`services/`、`packages/`、`codex/`、`platform/`：仅保留职责索引，不作为仓库挂载位置。

## 开发命令

```bash
make bootstrap
make lint
make test
make generate
```

## 测试要求

修改文档后至少运行：

```bash
./scripts/lint-all.sh
```

修改脚本后至少运行：

```bash
bash -n scripts/*.sh
```

## 安全要求

所有文档和示例必须使用假数据。涉及 token、PII、平台凭证、店铺经营数据、订单数据和财务数据的示例必须脱敏或使用合成数据。

## API 契约要求

任何跨仓 API、事件、DTO、工具 schema 或 SDK 变更都必须先更新 `yijie-contracts`，再由业务仓库实现。

## PR 要求

- 必须更新相关文档；
- 涉及跨仓边界必须更新 ADR；
- 涉及 API 必须更新 contract；
- 涉及高风险工具必须更新 approval policy；
- 涉及安全边界必须更新 security 文档。
