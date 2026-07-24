# 易界 AI

易界 AI 是服务跨境电商卖家的 AI native TOB 产品。卖家授权店铺权限后，易界 AI 结合店铺数据、平台规则、跨境电商 SOP 和外部平台 API，在选品、合规、Listing 优化、广告投流、物流追踪、经营分析、客户沟通等场景中提供智能体能力。

## 产品形态

当前唯一面向卖家的产品形态是易界 AI Mac 桌面端应用；另有一个 Admin Web 管理后台，用于租户、权限、插件、知识库、审计和运营管理。

## 技术栈

- 桌面端：Tauri + Vue
- Admin Web：Vue
- 后端：Go
- Agent Runtime：Codex Runtime
- 连接器：Go + MCP 工具服务
- 知识库：RAG 架构
- API 契约：OpenAPI / Protobuf / JSON Schema
- 基础设施：本地 Docker Compose；生产 IaC、观测和云环境待部署方案确认后引入

## 仓库结构

```text
yijie-ai/
  yijie
  yijie-codex
  yijie-desktop
  yijie-admin-web
  yijie-api
  yijie-agent-host
  yijie-skills
  yijie-connectors
  yijie-knowledge
  yijie-contracts
  yijie-infra
```

## 架构分层

```text
Product Experience Layer
  yijie-desktop
  yijie-admin-web

Business Platform Layer
  yijie-api

Agent Runtime Adapter Layer
  yijie-agent-host

Agent Runtime Kernel
  yijie-codex

Domain Capability Layer
  yijie-skills

Tool Execution Layer
  yijie-connectors

Knowledge Layer
  yijie-knowledge

Contract & Infra Layer
  yijie-contracts
  yijie-infra
```

## 本地启动

```bash
./scripts/bootstrap.sh
./scripts/dev-up.sh
```

`bootstrap.sh` 会校验本机工具、安装元仓库依赖，并根据 `repos.yaml` 将缺失仓库克隆到 `yijie` 的兄弟目录。已有仓库只执行 remote 校验和 fetch，不会覆盖工作区。

常用命令：

```bash
./scripts/checkout-all.sh
./scripts/dev-down.sh
./scripts/lint-all.sh
./scripts/test-all.sh
./scripts/generate-all.sh
make contract-governance
```

`make contract-governance` 要求十个兄弟仓库都存在，并校验中央规范、PR 模板和每个
仓库 `AGENTS.md` 的 Contract First 最小门禁。独立元仓 CI 只能验证中央文件，不能
替代下游仓的版本锁、生成漂移和 conformance CI。

## 文档入口

```text
docs/
  architecture/      # 架构文档
  adr/               # 架构决策记录
  product/           # 产品与跨境电商 SOP
  dev/               # 开发说明；contract-first.md 是跨仓契约操作规范
  security/          # 安全规范
  runbook/           # 运维手册
  release/           # 发布规范
```

## Codex 开发约定

本项目全部使用 Codex 辅助开发。每个仓库必须包含：

```text
AGENTS.md
.codex/
  config.toml
  prompts/
  tasks/
```

Codex 修改代码时必须遵循对应仓库的 `AGENTS.md`。

## 安全红线

- 不得提交任何平台 token、secret、cookie、access key；
- Codex Runtime 不得直接持有商家平台 token；
- 高风险写操作必须经过 approval policy；
- 所有外部平台 API 调用必须有审计日志；
- 所有日志必须做 PII 和密钥脱敏；
- 所有跨仓契约变更必须遵循 [`docs/dev/contract-first.md`](docs/dev/contract-first.md)，
  先形成权威契约和不可变引用，再合并或启用下游实现。

## 仓库 Owner

| 仓库 | Owner |
|---|---|
| yijie | Platform Team |
| yijie-codex | Agent Runtime Team |
| yijie-desktop | Client Team |
| yijie-admin-web | Admin Platform Team |
| yijie-api | Backend Team |
| yijie-agent-host | Agent Runtime Team |
| yijie-skills | AI Product Team |
| yijie-connectors | Integration Team |
| yijie-knowledge | Data AI Team |
| yijie-contracts | Platform Team |
| yijie-infra | DevOps Team |
