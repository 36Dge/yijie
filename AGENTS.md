# AGENTS.md

## 适用范围与指令优先级

本文件的文件系统指令范围仅覆盖 `yijie` 元仓库。十个业务/平台仓库位于它的兄弟目录，不会自动继承本文件；修改兄弟仓库前必须重新读取该仓库自己的 `AGENTS.md`、README、SECURITY 和相关设计文档。

本文件同时记录易界多仓项目的中央治理基线。兄弟仓规则可以细化实现方式，但不得在没有新 Accepted ADR 和用户明确确认的情况下弱化本文的 Contract First、安全、审批、审计或发布红线。只在兄弟仓单独工作的 Agent 仍需依靠该仓 `AGENTS.md` 和 CI 执行这些规则，不能把本文件误称为自动生效的全局指令。

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
- `docs/dev/contract-first.md`：当前项目级 Contract First 操作规范；
- `docs/dev/`：其它本地开发、测试、分支、调试和 Codex 协作说明；
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

## Contract First 项目级强制评审门禁

完整规范见 `docs/dev/contract-first.md`，相关任务开始时必须先给出
`contract-impact = none | additive | semantic | breaking`。选择 `none` 必须说明为什么没有改变跨进程、跨仓库、跨版本或持久化/重放边界上的可观察行为；不能因为 JSON/DTO 形状未变就忽略语义变化。

分类按最高风险唯一选择：任何仍受支持的 producer/consumer 可能失败或错误解释时为
`breaking`；改变既有值/操作的解释、默认或行为，但经方向性验证仍兼容时为
`semantic`，与结构形状是否改变无关；只有保留既有交互解释并通过方向性验证的新能力
才是 `additive`；不确定时不得选择 `none` 或直接假定 additive。

这是项目级合并/发布规范。当前自动化只覆盖 contracts 仓结构门禁和本地
`make contract-governance` 的规则存在性检查；PR body validator、所有兄弟仓 required
checks 和 branch protection 尚未全部接通，不能声称已经形成不可绕过的机器门禁。

以下内容均属于契约影响：HTTP/RPC/SSE/WebSocket 路径、方法、请求响应、状态码和错误码；字段必填性、null/default、枚举、单位、时间、分页和排序；认证、租户、权限、scope、审批和审计上下文；事件 channel、envelope、顺序、重复、重试、重放和终态；MCP tool 名称、输入输出、风险等级和失败语义；共享 JSON Schema、SDK 公共签名以及 Runtime 能力投影。

纯进程内函数、未暴露的领域模型、服务私有数据库/缓存格式和不可发布的本地试验通常
不进入 `yijie-contracts`，但仍分别遵守本仓 migration/data compatibility 规则。只有
它们被独立发布单元/兄弟仓消费，或成为跨版本 durable event、audit、replay/public
payload 时才进入公共契约判定；不得用“临时 DTO”“先写死再补契约”规避门禁。

易界拥有的跨仓 HTTP、RPC、事件、工具和共享 payload 以 `yijie-contracts` 的源契约为权威。生成代码、SDK、快照和文档示例都是派生物。两个必要特例是：

- Codex app-server 协议以上游固定 Runtime 及其 canonical schema 为权威，先形成 Runtime 候选，再更新 `yijie-contracts` 的兼容投影，最后由 Agent Host/客户端消费；
- 第三方平台协议以当前官方规范为外部权威，`yijie-connectors` 负责适配；任何易界公开的归一化 tool/API/event 仍须先进入 `yijie-contracts`。

除上述权威源特例外，跨仓变更必须按以下门禁执行：

1. 明确 Owner、producer、全部已知/登记 consumers、权威源、输入/输出方向、安全与失败语义、兼容窗口和回滚；高成本决策先更新 ADR；
2. 对 `yijie-contracts` 治理的边界，先修改所有受影响且适用的源契约、示例/fixture、生成物、一致性测试、版本及迁移说明，执行 generate、lint、test，并对所有仍受支持或处于生产兼容窗口的基线执行 breaking check；尚无已发布基线时必须使用契约仓登记的 fallback 完整 commit，不能形成零基线检查真空；
3. additive 至少取得一个代表性 consumer 评审（存在 consumer 时）；semantic/breaking 取得所有受影响 consumer Owner 的确认或逐仓例外；未知公开消费者按最保守兼容假设并由 SDK/代表性客户端 Owner 评审；全新无 consumer 契约由架构及适用时的安全 Owner 评审；
4. 契约 PR 满足计划版本、评审和检查后先合并，形成不可变完整 commit；生产发布必须使用不可移动 tag，下游不得从 dirty 或浮动 sibling 工作树制作发布产物；
5. 每一个下游实现 PR 在自身合并前固定精确版本、完整 commit 和可用时的 digest/generator 版本，重新生成或同步派生物，并增加 producer/consumer conformance、未知字段/未知变体和失败路径测试；
6. 实现代码是否可以激活或开始发出新值按兼容方向决定；provider-first 变更不要求所有 consumers 先 pin，response/event/breaking 切换则不得早于相应 consumer 就绪。

契约草案稳定后可以并行开发下游 draft，但不能先合并实现再补契约。公共 wire DTO 不得手写复制；暂时没有 generator 时，只允许显式 adapter、同源 schema conformance test 和有 Owner、期限、移除条件的例外记录。

兼容与部署必须区分方向：

- 新请求字段或新操作：先部署 provider 支持，再由 consumer 发送或调用；
- 新响应字段、枚举值或事件变体：先确认旧 consumer 容忍未知值，或先升级 consumer，再让 producer 发出；
- semantic change 必须人工证明兼容；若使任一仍受支持的有效交互失效，升级为 breaking；
- breaking change：采用 expand 或新版本、producer 双轨、consumer 迁移、观测确认、弃用和清理；禁止多仓同时硬切。

自动 breaking check 绿色只证明工具覆盖到的结构兼容，不证明默认值、权限、错误、幂等、顺序、实现一致性或端到端兼容。跳过检查、手改生成物、复制影子 schema、伪造版本引用或关闭门禁均不构成修复。

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
make contract-governance # 要求十个 sibling 均存在并校验其 Contract First 最小门禁
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
- 当 `contract-impact != none` 时，按权威源路由提供完成证据：`yijie-contracts` 治理的公共跨仓 wire 边界包含契约 PR/tag/完整 commit、全部适用 breaking 基线（尚无发布版本时为已登记 fallback 完整 commit）、consumer pin、生成差异和 conformance；私有存储、部署接口、Runtime/第三方上游边界则包含对应不可变权威源、migration/data/runtime/deployment compatibility、受影响方验证及回滚；不适用的 contracts 字段明确写 `N/A` 和理由；所有路径都包含分级 Owner/consumer 评审或例外、验证命令和部署顺序；`none` 只需有可复核理由；
- 各仓按依赖顺序完成独立生成、lint、测试和必要的集成验证；
- 每个仓库的状态、提交、发布、迁移和回滚均可独立追踪；
- 多仓脚本的网络、写入、readiness 和占位语义被准确报告；
- 未执行或尚未接通的 Runtime、数据库、平台、模型、云端和端到端验证被如实列出。
