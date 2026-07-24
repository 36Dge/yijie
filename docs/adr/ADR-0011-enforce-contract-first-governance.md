# ADR-0011: 强制执行跨仓 Contract First 治理

## 状态

Accepted

## 日期

2026-07-24

## 修订

补充并强化 ADR-0004，不改变 `yijie-contracts` 作为易界公共契约中心的决定。

## 背景

ADR-0004 确立了契约优先方向，但“优先”没有定义可判定范围、可消费时点、输入与输出的兼容方向、Runtime/第三方权威源特例、下游版本锁定和例外流程。

多仓工作区中的 `yijie/AGENTS.md` 也不会通过目录层级自动覆盖兄弟仓。仅有中央文档和 checkbox 无法阻止下游先实现 endpoint、事件或 DTO，再补契约；仓内 breaking check 绿色也无法证明下游实现与端到端发布兼容。

## 决策

1. 所有代码、配置、契约和发布变更在实现前必须分类 `contract-impact = none | additive | semantic | breaking`；按 `breaking > semantic > additive > none` 的最高风险唯一选择，`none` 必须说明没有跨边界可观察变化。
2. 易界拥有的跨仓 HTTP、RPC、事件、MCP tool、共享 schema 和 SDK 表面以 `yijie-contracts` 的源文件为权威。
3. 契约必须先完成设计、生成、兼容检查和分级 Owner/consumer 评审并形成不可变引用；每个下游实现 PR 在自身合并前固定引用并建立 conformance，功能激活顺序再按数据方向决定。
4. 请求、响应和事件按各自方向部署；semantic 必须人工证明兼容，不兼容时升级为 breaking；breaking 使用 expand/新版本、双轨、迁移、观测、弃用和清理，不允许多仓硬切。
5. Codex app-server 与第三方平台协议保留外部权威源；易界兼容投影和归一化公共表面仍进入契约评审。
6. 每个兄弟仓必须用本仓 `AGENTS.md`、PR/CODEOWNERS、生成漂移、版本/hash 锁、producer/consumer tests 和 required CI 落实规则；所有 GitHub 治理文件也不会从元仓自动继承。
7. 例外必须有明确 Owner、理由、范围、期限、回滚和补偿变更；未批准或无期限的“先实现后补契约”不允许合并。

现行操作细节以 `docs/dev/contract-first.md` 为准。当前属于强制评审规范：contracts
结构门禁和本地规则存在性检查已自动化，但跨仓 PR body、required checks、Owner
审批和到期例外尚未全部机器化，不能宣称不可绕过的工程门禁已经闭环。

## 备选方案

- **只依赖人工 Review**：成本低，但无法防止遗漏消费者、影子 DTO 和生成漂移。
- **把所有接口都放入中央仓库**：看似统一，但会错误吞并私有领域模型、数据库 migration、部署配置和第三方原始协议。
- **实现与契约同时硬切**：短期快，但在独立发布和回滚时不可控。

## 影响

- 契约 PR 或稳定草案可以与下游 draft 并行，但合并与启用存在明确依赖门禁；
- 下游需要记录不可变 contract ref，并逐步增加生成/快照漂移和符合性检查；
- PR 必须提供兼容方向、consumer、发布顺序和回滚证据；
- 少量前置设计成本换取可审查、可回滚和可独立发布的跨仓演进。

## 风险

- 规则只写在文档中仍可被人为绕过，因此必须由各仓 CI、CODEOWNERS、分支保护和评审流程共同执行；
- 过度中心化会阻碍内部重构，所以权威源路由和 `none` 分类必须保留清晰边界；
- 自动 breaking 工具覆盖不完整，仍需要语义和 consumer 评审。

## 后续动作

- [x] 建立中央 Contract First 操作规范与 PR 证据要求；
- [x] 在 `yijie-contracts` 建立生成、lint、test 和结构性 breaking 门禁；
- [x] 将最小 contract-impact 与合并红线同步到十个兄弟仓 `AGENTS.md`，并增加本地存在性检查；
- [ ] 将 PR 模板或 reusable PR-body validator、CODEOWNERS 和 ruleset 同步到每个适用兄弟仓；
- [ ] 在 contracts 建立机器可读 contract/owner/producer/consumer catalog，并自动校验源文件登记；
- [ ] 为所有 consumer 统一 `version + full commit + digest + generator version` 锁；
- [ ] 为 API、Agent Host 等 producer 增加 required generate-drift 和 conformance CI；
- [ ] 建立 checkout 固定 commit 的真实跨仓兼容 CI；
- [x] 在中央及 contracts PR 模板建立可审计的临时例外记录格式；
- [ ] 将临时例外字段同步到各适用兄弟仓 PR 模板，并建立自动到期检查；
- [ ] 在各 GitHub 仓分别配置 required checks、CODEOWNERS review 和长期分支禁止直推。
