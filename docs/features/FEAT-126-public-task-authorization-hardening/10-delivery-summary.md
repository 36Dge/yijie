# FEAT-126 交付总结与关闭记录

## 1. 当前结果

- 用户可观察行为：无变化；S4–S8A Accepted变更已保存为四个仅本地checkpoint，所有新routes/features默认关闭且未push。private Tauri IPC与TypeScript ViewModel已存在，但没有Vue页面/组件/动态路由/视觉接线；DESIGN-126-006仅完成S8B0 readiness设计。
- 原目标是否达成：未达成。DEC-126-026/027/028/030/031已接受S4–S8A Closure。DEC-126-032仍待Owner，S8B0/S8B、S9–S11、完整本地对话E2E与Owner验收均未完成。
- 当前范围：安全的新建任务对话、任务记录、聊天项目、本地持久化及Public Tasks hardening的完整Local-only需求/设计/测试/实施候选。
- 非目标：见`00-feature-brief.md`；没有文件/图片/工具/云同步；tag/package publish/registry/线上部署/生产灰度/云数据库/真实用户数据均N/A。
- 交付状态：`G1 Passed / G2 Passed / G2A Re-review Passed / S4–S8A Closure Passed / S8B0 Design Review Ready / G3 Partial`。DEC-126-031已Accepted；DEC-126-032为Proposed且不授权S8B0/S8B。DEC-126-021继续HOLD；sole contract candidate远端可达，新local checkpoints未push；当前不是Code Complete、Production Ready或Local-only Delivery Complete。

## 2. 实际版本与本地候选（未发布）

| Component | Environment | Version/tag | Full commit | Artifact digest | Contract version/pin |
|---|---|---|---|---|---|
| yijie-contracts sole source candidate | dedicated remote branch | `0.3.0 candidate` / tag N/A | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | SDK `21b17b50…b082`；Public `c8d9e674…354b`；TS `e84b70be…b678`；Go `c3d6e58e…c697` | `origin/feat/feat-126-content-free-candidate` exact；G2A Passed；not merged/tagged/published/activated |
| yijie-contracts prior remote candidate | dedicated branch + Draft PR #1 | `0.3.0 historical candidate` / tag N/A | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | SDK `334db014…9404` | unchanged；remote CI failed dependency audit；merge HOLD |
| yijie governance Accepted baseline | local only / no release | tag N/A | `6de641f715751bb8ca94ce6804e5a33ff18d9569` | 12-file manifest见`08` | parent remote unchanged；not pushed；DESIGN-126-006 docs follow locally |
| yijie-api S4 Accepted checkpoint | local only / no release | tag N/A | `a64f9f591fb594818c1778e30c6941e2574b3264` | Go `438b084d…ab33`；migration v4 `b56f7f5a…ee14` | parent remote unchanged；`29317b...` lock；default off；not pushed |
| yijie-agent-host S5 Accepted checkpoint | local only / no release | tag N/A | `3e8df026110f0c895262329c2384d3896598f3d9` | Go `629ddf…63b0`；store v3 | parent remote unchanged；`29317b...` source；v2 flags off；not pushed |
| yijie-desktop S6–S8A Accepted checkpoint | local only / no release | tag N/A | `3adcb0380561c294412bc24767e4651ca872455a` | TS `e84b70be…b678`；SQL v4/Bridge/Domain/Application/Auth/IPC/Store digests见`feature.yaml` | parent remote unchanged；`29317b...` lock；flags off；private IPC/store present；no Vue/router/style addition；not pushed |

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| S4 AC-025–030 foundation | CORRECTIVE CLOSURE PASS / OWNER ACCEPTED | content-free audit matrix, nil tenant, idempotency retention/cleanup, read-only generate drift, exact `29317b...` runtime conformance and isolated PostgreSQL PASS；DEC-126-026 | none / production N/A |
| S5 raw/title/cleanup foundation AC subset | CORRECTIVE CLOSURE PASS / OWNER ACCEPTED | persisted cleanup/restart, atomic lease, title idempotency/isolation with forced-off capability hold, receipt/schema/no-log/bbolt and fixed Runtime PASS；DEC-126-026 | none / production N/A |
| S6 local DB/project/sidecar foundation AC subset | CORRECTIVE CLOSURE PASS / OWNER ACCEPTED | terminal reasoning, joined history, full cascade/FK, migration negative matrix, spawn nonce and readiness separation PASS；DEC-126-026 | none / production N/A |
| S7A Rust Host Bridge/Domain subset | CLOSURE PASS / OWNER ACCEPTED | fake Host、canonical fixture、Desktop full gates；DEC-126-027 | none / local-only |
| S7B Rust Application Orchestration/Domain subset | CLOSURE PASS / OWNER ACCEPTED | outbox/reducer/history/title/migration/fake Host application chain；113 TS + 78/79 Rust pass；DEC-126-028 | none / local-only |
| DESIGN-126-005 private IPC/ViewModel | DESIGN ACCEPTED / DEC-126-029 ACCEPTED | ConversationApplication/Tauri/TS gap inventory、closed commands/events/cursor/error、Rust-bound context、capacity/backpressure/stale/restart和S7C/S8A/S8B计划 | none / production N/A |
| S7C Rust Actions/Coordinator subset | CLOSURE PASS / OWNER ACCEPTED | auth context/facade、actions/interrupt、SQLCipher v4 cleanup/receipt、coordinator/restart/resync/live raw；Desktop 113 TS + 87/88 Rust；DEC-126-030 Accepted | none / local-only |
| S8A private IPC/TypeScript ViewModel subset | DEC-126-031 ACCEPTED / CLOSURE PASS | 20 commands、closed schema/fixtures、Rust auth/event/cursor、TS validators/client/store；Desktop 127 TS + 93/94 Rust | none / local-only |
| DESIGN-126-006 / DEC-126-032 | DESIGN READY / OWNER REVIEW PENDING | default-off gate、dynamic route/auth、permission lifecycle、store paging/cleanup、readiness/storage private IPC stop condition、Tasks/scroll方案；0 source diff | none / design only |
| Remaining AC/NFR / S8B0、S8B、S9–S11 | NOT RUN | not authorized；full traceability in `08` | none / production N/A |
| Requirement package/G0/G1 | G1 product scope approved；structure evidence in `08` | user approval + default/G0/G1/strict package, YAML and diff checks | N/A |
| G2 data authority | ACCEPTED DESIGN | ADR-0013 + 段成威 2026-08-02 approval；SQLite/PostgreSQL/Redis/pgvector/bbolt 职责已冻结 | N/A |
| G2 SQLite/delete design | ACCEPTED DESIGN | ADR-0014/DEC-126-006 + Rust dependency build + fixed Runtime functional/restart delete evidence；Q-006/Q-015 Resolved，forensic WAL/log residue remains explicit limitation | N/A |
| G2 Runtime title/raw-reasoning capability | ACCEPTED DESIGN / FOUNDATION CLOSURE PASS | Host/Desktop S5–S6 closure evidence PASS；title flag因Runtime不能能力级禁用tools而强制off；historical MiniMax evidence retained；本轮0 provider calls | N/A |
| G2 DESIGN-126-003 | ACCEPTED DESIGN | exact v2 raw variants、SQLCipher schema、caps、aggregation/reconciliation、history/migration/cascade frozen；fixed raw upstream fixtures 4/4 PASS；DEC-126-017 Accepted | N/A |
| G2 Public Tasks/Pattern | ACCEPTED DESIGN | repo-local consumer inventory complete、Q-010 Resolved、DEC-126-011/012和Desktop Pattern Accepted | N/A |
| G2A source contract | PASSED / APPROVED | DEC-126-023/024与Q-017 closed；replacement `29317b...`及source/generated/fixtures/digests/post-commit gates approved；sole candidate confirmed | N/A |
| Contract Draft PR / remote CI | PR CREATED / CI FAILED / MERGE BLOCKED | [PR #1](https://github.com/36Dge/yijie-contracts/pull/1)为OPEN/DRAFT，base/head/SHA精确匹配；run 30741466028的generate/diff/lint/test/pack PASS，`pnpm audit`因`brace-expansion 2.1.2` high失败，后续`govulncheck`/`origin/main` breaking skipped；candidate未改依赖文件 | N/A |
| Local-only Delivery Strategy | ACCEPTED / G3 PARTIAL | DEC-126-021 HOLD、DEC-126-022/026/027/028/029/030/031 accepted；DEC-126-032 Proposed；S4–S8A Closure Passed；fake-first/default-off；G5/tag/publish/deploy N/A | N/A |

## 4. 本地 Smoke 与观察

| Check/Metric | Window | Baseline | Actual | Threshold | Result |
|---|---|---:|---:|---:|---|
| local four-component startup/E2E | none | S4–S8A service/domain/IPC foundations | not established | G4/local G6 prerequisites | NOT RUN |
| production deploy/smoke/metrics | N/A | N/A | out of scope | DEC-126-022 | N/A |

## 5. 安全与审计抽查

| 项目 | Trace/request/task/session 标识 | 结果 | Evidence |
|---|---|---|---|
| 授权/租户/审计 | synthetic IDs only | creator-private 401/403/404/409/503/read/create content-free audit matrix、nil tenant与PostgreSQL正文边界 PASS | API unit/race + isolated PostgreSQL + generated contract negative fixtures |
| raw/no-log/secret | synthetic canaries only | Host raw正文不进logs或synced bbolt；Desktop key/error/Host message/raw/token/path Debug redaction、sidecar env/nonce及S8A IPC/client/store no-log字段扫描PASS | Host/Desktop tests + logger/bbolt/source scan；future UI/E2E pending |

## 6. 本地执行事件、恢复与数据状态

- Incident/异常：无发布、无feature runtime incident；评审期远端CI dependency audit只作为merge blocker登记，不属于生产事故或G2/G2A回退。
- 本地工具限制：总仓`make lint/test`在所有先行仓门禁及Infra静态/76项Node测试通过后，因本机Docker 29.6.1未安装Compose plugin而在Infra `docker compose -f ... config`退出125；未豁免或标记全绿。FEAT-126受影响的API/Host/Desktop/Contracts门禁均已单独通过，因此不形成S4–S6代码P1，但应在未来S10前补齐本机Compose能力。
- 是否触发停止或回滚：N/A。
- 数据/队列/缓存最终状态：只创建过隔离的synthetic PostgreSQL/SQLCipher/Host temp stores，测试后停止并清理；真实业务数据未触碰。
- 回滚路径当前是否仍有效：新能力默认off；API migration为expand-only，Desktop/Host按forward repair；完整跨进程rollback尚待S10。
- Workspace：本轮checkpoint未包含任何FEAT-123删除或无关改动；yijie/API/Host/Desktop均有仅本地Accepted checkpoint，未push；contracts candidate、Runtime与Infra未改。

## 7. 未验证项、已知限制与接受风险

| Item | 影响 | Owner | 批准 | 截止/复查 |
|---|---|---|---|---|
| Host/Desktop title/raw-reasoning integration | Host producer、Desktop SQLCipher、S7A transport/domain与S7B reducer/history PASS；Vue UI/full E2E未实现 | 段成威 | flags off；按S8–S10实施/验证 | before G4 |
| Raw reasoning schema/caps | immutable source + Host caps/reconciliation + Desktop terminal schema基础PASS | 段成威 | S4–S6 accepted as implementation evidence only | S7/S9/S10 |
| S8B0/S8B authorization | S7C已由DEC-126-030接受；S8A已由DEC-126-031接受；DESIGN-126-006/DEC-126-032待审，S8B0/S8B及S9–S11仍禁止 | 段成威 | 先批准DEC-126-032，再分别授权S8B0与S8B | before each slice |
| Draft PR dependency audit / merge readiness | 当前CI红灯，且两个后续job steps未运行；当前candidate/PR保持不变 | 段成威 | DEC-126-021 Accepted/HOLD；只阻断merge，无audit waiver/rerun/fix/push授权 | before any future merge approval |
| Public Tasks anonymous/IDOR debt | production route must remain isolated | 段成威 | inherited controlled exception only | FEAT-126 production or 2026-09-30 earlier |
| SQLite/SQLCipher 与 delete/backup boundary | 单仓wrong-key/migration/cascade/checkpoint/backup exclusion基础PASS；完整删除saga/OS副本语义未E2E | 段成威 | flags off；不承诺forensic erase | future G4/local G6 |
| Host raw/title/Runtime cleanup | fake Runtime foundation与S8A IPC/store PASS；真实Runtime跨Desktop与raw稳定性/Eval未验证 | 段成威 | v2 flags off | S8B、S9–S10 |
| Desktop sidecar | supervisor/health/env/path基础已实现；真实child与signed Keychain未运行 | 段成威 | foundation only | S10 |
| production identity/infra absent | no production activation | 段成威 | N/A for DEC-126-022 local-only scope；future online intent reopens production track | does not block local G6 |

## 8. 后续工作

| Issue | 内容 | 触发条件 | Owner | 截止 |
|---|---|---|---|---|
| REVIEW-126-001 | G1 推荐产品方案确认 | 需求包交付 | 段成威 | Complete 2026-08-01 |
| DESIGN-126-001 | 将 G1 规则固化为 Chat/App Shell Pattern并审查 | Accepted 2026-08-02 | 段成威 | Complete |
| ADR-0013 | 冻结 local data authority、storage roles、local/cloud boundary | G1 complete | 段成威 | Complete 2026-08-02；不含 implementation details |
| ADR-0014 / DESIGN-126-002 | 物理删除状态机、SQLite protection/backup/uninstall 与 content-free receipt | Owner approval complete | 段成威 | Design complete 2026-08-02；S5/S6 foundation implemented/tested，完整删除 E2E 仍待 S7+ |
| DESIGN-126-003 | 冻结raw reasoning SQLCipher表结构、caps、coalesced flush、partial/finalized reconciliation、history分页、migration和删除fixture | DEC-126-017 Accepted；fixed raw fixtures 4/4 PASS | 段成威 | Complete |
| DESIGN-126-004 | 关闭Public Tasks consumer inventory并选择兼容分支 | Q-010 Resolved；DEC-126-011/012 Accepted | 段成威 | Complete |
| SPIKE-126-001–006 | 完成 Runtime/data/consumer/layout evidence | Complete for G2 design inputs | assigned owners | implementation evidence remains future |
| CONTRACT-126-001 | DEC-126-018/019/020已批准；immutable candidate、G2A、专用branch远端可用性与clean-clone门禁完成 | G2/G2A/remote availability approved | platform/consumer owners | Complete 2026-08-02；S4–S6 已按完整 SHA 建立本地 projection/lock，S7+ 与 merge 另行授权 |
| CONTRACT-126-002 | Draft PR #1远端CI dependency audit remediation与未来merge readiness | local E2E完成且Owner重新开启merge轨后 | platform owner / 段成威 | Deferred/HOLD；不阻断local draft，不得修改现有candidate或merge |
| LIA-126-001 | S4–S6本地基础实现授权 | DEC-126-022 Accepted + Owner明确批准LIA | 段成威 | Complete 2026-08-02；不授权S7–S11/MiniMax/远端写入 |
| LIA-126-002 | Foundation Corrective Closure | DEC-126-025恢复、DEC-126-026接受；只允许S4–S6、fake/fixture/temp环境 | 段成威 | Closure Passed 2026-08-02 |
| S7A | Desktop Rust Host Bridge/Domain | DEC-126-026单独授权；fake Host/fixed fixtures；no Vue/flag | 段成威 | Closure Passed / DEC-126-027 Accepted 2026-08-03 |
| S7B | Desktop Rust Application Orchestration/Domain | DEC-126-027单独授权；fake Host/fixed fixtures/temp SQLCipher；no Tauri/Vue/flag | 段成威 | Closure Passed / DEC-126-028 Accepted |
| DESIGN-126-005 / DEC-126-029 | Desktop private IPC/ViewModel contract与S7C/S8A/S8B重切 | 只读源码盘点与需求包设计 | 段成威 | Accepted；S7C/S8A later separately authorized |
| LIA-126-003 / S7C / DEC-126-030 | Rust authorization、session/project actions、delete/interrupt/coordinator/restart-resync | Owner明确授权；fake Host/fixed fixtures/temp SQLCipher；no Tauri/TS/Vue/flag | 段成威 | Closure Passed / DEC-126-030 Accepted |
| LIA-126-004 / S8A / DEC-126-031 | private Tauri IPC、Rust auth/event/cursor、TS validators/client/Pinia ViewModel | Owner明确授权；fake Host/fixed fixtures/temp SQLCipher/CODEX_HOME；no Vue/flag | 段成威 | DEC-126-031 Accepted / S8A Closure Passed；S8B不随之授权 |
| DESIGN-126-006 / DEC-126-032 | S8B0 default-off gate、route/lifecycle/store/readiness/tasks/scroll integration contract | S8A Accepted + read-only UI consumption audit | 段成威 | Proposed / Ready for Owner Approval；private IPC stop condition；不授权source |
| S8B0 | 只做gate/router/lifecycle/store/private IPC readiness integration，不做完整Vue页面 | DEC-126-032 Accepted后另行明确授权 | 段成威 | Not authorized / NOT RUN |
| S8B | 真实Vue页面、App Shell/session树、composer/conversation/reasoning/menu/delete/visual/a11y | S8B0 Closure Accepted后另行授权 | 段成威 | Not authorized / NOT RUN |
| CLEAN-125-004 | 完成 Public Tasks hardening并退出 FEAT-125 临时隔离例外 | G5/G6 | 段成威 | FEAT-126 production or 2026-09-30 earlier |

## 9. 文档与运维交接

| Artifact | Final path/link | Owner | Updated |
|---|---|---|---|
| Feature package | `docs/features/FEAT-126-public-task-authorization-hardening/` | 段成威 | 2026-08-01 |
| Existing auth ADR | `docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md` | 段成威 | existing Accepted source |
| Local conversation data ADR | `docs/adr/ADR-0013-desktop-local-conversation-data-authority.md` | 段成威 | Accepted 2026-08-02 |
| Desktop Chat/App Shell Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/12-feat-126-chat-app-shell-candidate.md` | 段成威 | Accepted 2026-08-02；仅取代01/02中的FEAT-126冲突段落 |
| Runtime isolated title ADR | `docs/adr/ADR-0015-isolated-title-and-public-reasoning-summary-projection.md` | 段成威 | Accepted 2026-08-02；title方向有效；public-summary-only部分由ADR-0016取代；历史provider证据保留 |
| Raw model reasoning ADR | `docs/adr/ADR-0016-display-raw-model-reasoning.md` | 段成威 | Accepted 2026-08-02；raw纯文本展示、no-log/no-silent-degrade与DEC-126-016 SQLCipher生命周期已冻结 |
| G2A source candidate | sole candidate `yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f` + historical remote `c000a024...` | 段成威 | DEC-126-023/024与Q-017 closed；G2A Re-review Passed；old PR/remote unchanged；merge HOLD；tag/publish N/A；no business pin |
| Contract Draft PR / CI evidence | [yijie-contracts PR #1](https://github.com/36Dge/yijie-contracts/pull/1) + run 30741466028/job 91479562558 | 段成威 | exact immutable head；CI failed dependency audit；DEC-126-021 Accepted/HOLD |
| Release runbook | `09-release-and-rollback.md` | 段成威 | plan only |

## 10. 复盘

- 有效流程：先发现 FEAT-126 编号已绑定安全债务；把 UI 截图要求转为可测行为；明确 raw CoT、permission UI、physical delete 与 local/cloud 误区；保护 dirty FEAT-123。
- 当前返工/缺陷：S4–S6审查发现的Desktop跨scope复合FK、Host私有文件symlink/hardlink、title隔离与raw stream-gap问题均已修复；完整产品链路仍未实现。
- 根因：产品需求到来时，security feature 已预留编号但尚未建立目录；当前 Chat/Host/Public Tasks 都是不同成熟度的基线。
- 流程改进候选：Feature ID registry/checker 应检查 Accepted ADR/Feature 引用，避免只按目录判断空闲编号；截图应进入 durable approved Pattern/asset 而非临时 OS 路径。

## 11. 关闭批准

| Gate | Owner | Decision | Date | Evidence |
|---|---|---|---|---|
| G0 Intake | 段成威 | Passed — requested requirement creation | 2026-08-01 | user request + `00` |
| G1 Design Ready | 段成威 | Passed — approved FEAT-126 recommended product scheme | 2026-08-01 | user statement + resolved G1 Q/accepted product DEC |
| G2 Design Review | 段成威 | Passed — DEC-126-017/011/012与FEAT-126 Pattern Accepted；进入G2A/no business coding | 2026-08-02 | Owner statement + `03`/`04`/`05`/`08` |
| G2A Source Contract + Remote Availability | 段成威 | DEC-126-023/024 Accepted，G2A Re-review Passed；`29317b...`为唯一candidate；old remote availability仅适用于历史`c000a024...`，Draft PR #1不变 | 2026-08-02 | `29317b...` post-commit source/fixture/generated/digest review + `03`/`04`/`08` |
| Contract Merge Readiness | 段成威 | DEC-126-021 Accepted/HOLD；PR #1 CI red，not approved for merge；merge不是local draft前置 | 2026-08-02 | PR #1 + run 30741466028 + `03`/`08`/`09` |
| Local-only Delivery Strategy | 段成威 | DEC-126-022 Accepted；Local Runtime Ready目标；tag/publish/deploy/G5 N/A | 2026-08-02 | Owner statement + `03`/`07`/`09` |
| LIA-126-001 | 段成威 | Approved / Executed — produced S4–S6 foundations；later review supersedes Complete claim | 2026-08-02 | repository gates + digests + structured review in `07`/`08` |
| LIA-126-002 / S7A Authorization | 段成威 | DEC-126-026 Accepted；S4–S6 Passed；S7A only authorized and executed locally | 2026-08-02 | DEC-126-023/024/025/026 + `07`/`08` |
| S7A Closure Review / S7B Authorization | 段成威 | DEC-126-027 Accepted；S7A Closure Passed；S7B Rust application only authorized and executed locally；G3仍Partial | 2026-08-03 | Desktop S7A gates + Owner statement；no S8/UI/flag/MiniMax/remote action |
| S7B Closure Review | 段成威 | DEC-126-028 Accepted；S7B Closure Passed，G3仍Partial | 2026-08-03 | Desktop 113 TS + 78/79 Rust、fake Host application chain、structured review；no Tauri/Vue/flag/MiniMax/remote action |
| Desktop IPC/ViewModel Contract Review | 段成威 | DESIGN-126-005、DEC-126-029 Accepted；LIA-126-003/004依次授权S7C/S8A | 2026-08-03 | closed private IPC与S7C/S8A/S8B顺序；S8B implementation NOT RUN |
| S7C Closure Review | 段成威 | DEC-126-030 Accepted；S7C Closure Passed；G3仍Partial | 2026-08-03 | Desktop 113 TS + 87/88 Rust、fake Host cleanup/restart/race链；no Tauri conversation IPC/TS/Vue/flag/MiniMax/remote action |
| S8A Closure Review | 段成威 | DEC-126-031 Accepted；S8A Closure Passed；G3仍Partial | 2026-08-03 | Desktop 127 TS + 93/94 Rust、closed IPC/TS store/auth/event/restart/no-log链；no Vue/flag/MiniMax/central pin/remote action |
| S8B0 UI Integration Readiness Review | 段成威 | DESIGN-126-006 complete；DEC-126-032 Proposed，等待Owner；不授权source | 2026-08-03 | four local Accepted checkpoints + read-only UI audit；private IPC stop condition；no Vue/flag/MiniMax/remote action |
| G5 Production Ready | 段成威 | N/A / Out of Scope under DEC-126-022 | 2026-08-02 | no deployment/tag/publish/production environment |
| G6 Local-only Delivery Complete | 段成威 | Pending Owner local startup and functional acceptance | N/A | requires G4 + AC-043；not Production Ready |

- 正式关闭时间：N/A；feature remains active at G2A Re-review Passed / G3-partial boundary。S4–S8A Closure已由Owner接受；DEC-126-032及S8B0/S8B、S9–S11仍须分别审批。dependency remediation/merge与MiniMax local smoke继续分别单审，tag/publish/deploy不在本期范围。
