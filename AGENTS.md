# AGENTS.md

## 适用范围与指令优先级

本文件适用于 `yijie` 元仓库本身。十个业务/平台仓库位于它的兄弟目录，不受本文件直接覆盖；修改兄弟仓库前必须重新读取该仓库自己的 `AGENTS.md`、README、SECURITY 和相关设计文档，更具体的仓库规则优先。

## 仓库职责与当前工作区模型

`yijie` 是易界 AI 的项目元仓库，负责多仓入口、仓库清单、跨仓架构治理、ADR、产品边界、本地开发脚本、发布和安全规范。它不承载具体业务代码。

当前工作区采用兄弟仓库模式：

- `repos.yaml` 记录十个子仓库的路径、HTTPS 远端、类型、Owner 和默认 `develop` 分支；
- 子仓库位于 `../yijie-*`，每个仓库有独立 `.git`、分支、提交和发布历史；
- 当前不使用 Git submodule，`.gitmodules` 只是说明占位；
- `apps/`、`services/`、`packages/`、`codex/`、`platform/` 仅是职责索引，不挂载或复制业务代码；
- 元仓库不记录各子仓库 commit pin，因此一次跨仓功能需要在每个受影响仓库独立提交、PR 和发布。

## 仓库边界

- 不在本仓库实现 Desktop、Admin、API、Agent Host、Connectors、Knowledge、Skills、Contracts、Infra 或 Codex Runtime 代码；
- 不把兄弟仓库复制进索引目录，也不擅自改为 monorepo 或 submodule；
- 不提交真实 token、secret、cookie、access key、平台凭据、DSN、PII 或真实商家数据；
- 不在 `yijie-codex` 中设计业务逻辑，不在 Agent Host 中重建完整 Agent 平台；
- 不绕过 Contract First、服务端授权、审批、审计和日志脱敏要求；
- 不在未更新 ADR、架构和相关仓库文档时改变跨仓职责或依赖方向。

## 权威文档与目录

- `repos.yaml`：兄弟仓库清单、远端、默认分支和 Owner 的唯一机器可读来源；
- `docs/architecture/`：跨仓边界、依赖方向、数据流、发布和观测原则；
- `docs/adr/`：已接受的跨仓不可逆或高成本决策；
- `docs/product/`：产品范围、卖家 SOP 和 MVP 边界；
- `docs/dev/`：本地开发、测试、分支、调试和 Codex 协作；
- `docs/security/`：安全模型、数据分类、秘密、审批和审计；
- `docs/runbook/`：故障诊断和恢复入口；
- `docs/release/`：各类制品及跨仓发布约束；
- `scripts/`：基于 `repos.yaml` 的多仓操作入口；
- `.codex/`：元仓治理任务的提示和模板，不替代各仓 AGENTS.md。

文档出现冲突时，先核对已接受 ADR 和当前代码事实。不要静默选择其中一个版本，应修正文档或向用户确认是否需要新 ADR 取代旧决策。

## Codex 多仓工作流程

开始任何跨仓任务前：

1. 从 `repos.yaml` 确认受影响仓库，不根据目录名猜测；
2. 查看每个仓库当前分支、远端和 `git status`，记录已有未提交改动；
3. 阅读每个仓库自己的 AGENTS.md 和相关设计文档；
4. 识别契约、安全、数据库、Runtime、平台和基础设施决策是否缺失；
5. 明确实施及发布顺序，再逐仓修改和验证。

- 已有工作区改动默认属于用户或前序任务，不得 reset、checkout、覆盖、批量格式化或混入无关提交；
- 多仓命令执行前后都检查各仓状态，尤其是 generate、测试生成物和 lockfile；
- 不因“统一治理”批量改写各仓配置，除非用户明确要求且每个仓库都完成独立验证；
- 不自动 commit、push、创建分支或改远端，除非用户明确要求；
- 跨仓提交保持可独立审查，提交信息说明依赖的契约版本和关联仓库。

## Contract First 与跨仓顺序

任何跨仓 API、事件、DTO、MCP tool schema 或 SDK 变更必须先更新 `yijie-contracts`，完成生成和兼容性检查后再更新下游。

推荐依赖顺序：

```text
decision/ADR
  -> yijie-contracts
  -> producer and core services
  -> yijie-agent-host / yijie-connectors / yijie-knowledge
  -> yijie-desktop / yijie-admin-web / yijie-skills
  -> yijie-infra and release documentation
```

实际顺序根据依赖和向后兼容方案确定。破坏性变更必须采用扩展、双写/双读、迁移、弃用和清理等分阶段发布，不在多个仓库同时硬切。

## 仓库清单与初始化脚本

- 修改 `repos.yaml` 时同步更新 manifest 测试、README、架构、CODEOWNERS 和相关脚本；
- 新增、删除、重命名仓库或改变 Owner、远端、默认分支前必须取得用户明确确认；
- `scripts/bootstrap.sh` 会检查本地工具、安装元仓依赖并调用 checkout 脚本；
- `scripts/checkout-all.sh` 会 clone 缺失仓库、fetch 现有仓库，并可能为缺少 origin 的仓库添加远端；
- `checkout-all.sh` 虽名为 checkout，但不会切换现有仓库当前分支，也不会覆盖工作区；
- 现有 origin 必须与 `repos.yaml` 中 HTTPS URL 完全一致，否则脚本失败；
- bootstrap/checkout 涉及网络和多个 Git 仓库，不作为普通文档或 lint 任务的默认步骤。

## 多仓命令的真实语义

```bash
pnpm lint              # 只验证 repos.yaml
pnpm test              # 只测试 manifest 结构
bash -n scripts/*.sh   # 只检查元仓 Shell 语法
make bootstrap         # 安装元仓依赖并 clone/fetch 兄弟仓库
make checkout          # clone/fetch/remote 检查，不切换现有分支
make lint              # 元仓 manifest + 十个兄弟仓库 make lint
make test              # 元仓 manifest + 十个兄弟仓库 make test
make generate          # 对十个兄弟仓库执行 generate，可能改写多个工作区
make dev-up            # 启动 infra Compose，但当前不等待健康检查
make dev-down          # 停止 infra Compose并保留命名 volume
```

- 根仓文档或 manifest 小改动先运行 `pnpm lint && pnpm test && bash -n scripts/*.sh`；
- 修改多仓脚本、清单或全局门禁时再运行 `make lint` 和必要的 `make test`；
- `make generate` 会跨仓写文件，且部分子仓 generate 仍是占位。执行前必须确认各仓干净或已记录改动，成功也不代表所有生成能力真实存在；
- `make dev-up` 当前使用 `docker compose up -d`，不能只凭退出码声称依赖 ready；需要 readiness 时使用 `make -C ../yijie-infra dev-up` 并检查 `dev-status`；
- Infra 的 lint 和本地启动要求 Docker Compose v2；只有 `docker` CLI 而缺少 `docker compose` plugin 时，多仓门禁会失败；
- 不为纯文档任务启动、停止或改变用户当前容器和本地数据。

## 分支、提交与发布

- `develop` 是日常集成分支，`staging` 是预发基线，`main` 是生产基线；
- 功能和常规修复从 `develop` 建短期分支，通过 PR 合回；长期分支间通过 PR 晋升；
- hotfix 从 `main` 创建，并回灌 `staging` 和 `develop`；
- 十一个仓库独立提交和发布，元仓文档提交不能替代业务仓实现提交；
- 跨仓 PR 需要互相引用，说明合并顺序、兼容窗口、migration、灰度和回滚；
- 未经用户明确要求，不推送、合并、打 tag、改分支保护或触发发布。

## 安全与治理红线

- Codex Runtime 不接触商家平台 token，平台凭据留在 Connectors 的安全边界；
- 身份、RBAC、审批和审计主状态由服务端权威控制，前端和 prompt 不能替代；
- 高风险写操作必须绑定明确用户意图、租户、工具、参数、影响范围、有效期和审计；
- 真实商家数据不得进入示例、fixtures、Skill eval、RAG eval、日志或文档；
- 数据库、认证、云厂商、embedding、平台 API、Runtime 协议和生产 secret 等信息缺失时必须询问，不得猜测；
- 安全边界变化同步更新 ADR、security、runbook、测试和发布/回滚说明。

## 必须先确认的决策

- 仓库新增/删除/重命名、远端、Owner、默认分支或工作区模型；
- 跨仓职责、依赖方向、公共契约或 Accepted ADR 的改变；
- 认证、租户、RBAC、审批、审计、数据保留和秘密管理；
- 数据库 schema、Redis 用途、embedding、平台授权和 Runtime transport；
- 云厂商、生产环境、基础设施、发布、迁移和回滚方案；
- 任何跨仓 generate、批量修改、提交、推送、分支或远端操作；
- 真实账户、生产数据、付费服务或不可逆命令。

## 完成标准

- 变更位于正确仓库，相关仓库规则和已有用户改动得到保护；
- 跨仓职责、契约、安全和 ADR 保持一致，没有用元仓文档代替实际实现；
- 各仓按依赖顺序完成独立生成、lint、测试和必要的集成验证；
- 每个仓库的状态、提交、发布、迁移和回滚均可独立追踪；
- 多仓脚本的网络、写入、readiness 和占位语义被准确报告；
- 未执行或尚未接通的 Runtime、数据库、平台、模型、云端和端到端验证被如实列出。
