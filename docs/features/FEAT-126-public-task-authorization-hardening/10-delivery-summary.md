# FEAT-126 交付总结与关闭记录

## 1. 当前结果

- 用户可观察行为：无变化；S4–S6只有Conditional基础，所有新routes/features默认关闭，S7–S8 UI未开始。
- 原目标是否达成：未达成。DEC-126-023/024已关闭source conflict并通过G2A重审，但LIA-126-002仍暂停；S4–S6纠偏、S7–S11、完整本地对话E2E与Owner验收均未完成。
- 当前范围：安全的新建任务对话、任务记录、聊天项目、本地持久化及Public Tasks hardening的完整Local-only需求/设计/测试/实施候选。
- 非目标：见`00-feature-brief.md`；没有文件/图片/工具/云同步；tag/package publish/registry/线上部署/生产灰度/云数据库/真实用户数据均N/A。
- 交付状态：`G1 Passed / G2 Passed / G2A Re-review Passed / S4–S6 Conditional / LIA-126-002 Paused / G3 Partial`。DEC-126-021继续HOLD；`29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一source-contract candidate，`c000a024...`仅为历史远端候选。当前不是Code Complete、Production Ready或Local-only Delivery Complete。

## 2. 实际版本与本地候选（未发布）

| Component | Environment | Version/tag | Full commit | Artifact digest | Contract version/pin |
|---|---|---|---|---|---|
| yijie-contracts sole source candidate | local branch only | `0.3.0 candidate` / tag N/A | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | SDK `21b17b50…b082`；Public `c8d9e674…354b`；TS `e84b70be…b678`；Go `c3d6e58e…c697` | post-commit gates verified；DEC-126-024 Approved / G2A Re-review Passed；not pushed/merged/tagged/published/pinned |
| yijie-contracts prior remote candidate | dedicated branch + Draft PR #1 | `0.3.0 historical candidate` / tag N/A | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | SDK `334db014…9404` | unchanged；remote CI failed dependency audit；merge HOLD |
| yijie-api S4 local checkpoint | local only / no release | tag N/A | `b5e601764357512208cc09bfb2b30b244a1b82ac` | Go `05d417…af51`；migration `ee5a3a…f86c` | prior candidate lock；Conditional/default off |
| yijie-agent-host S5 local checkpoint | local only / no release | tag N/A | `f6e4a5902d8f25632408c1c699ba17b8c66ef214` | Go `629ddf…63b0` | Conditional；v2 flags off |
| yijie-desktop S6 local checkpoint | local only / no release | tag N/A | `40413b409a467a133d178137651622e167d512de` | TS `d3493a…03b`；SQL/Cargo digests见`feature.yaml` | Conditional；foundation off |

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| S4 AC-025–030 foundation | CONDITIONAL / NOT CLOSED | prior API tests pass but rejection audit, content boundary, TTL and drift gate have open findings | none / production N/A |
| S5 raw/title/cleanup foundation AC subset | CONDITIONAL / NOT CLOSED | prior tests pass but partial cleanup recovery, atomic lease and title isolation/idempotency P1 remain | none / production N/A |
| S6 local DB/project/sidecar foundation AC subset | CONDITIONAL / NOT CLOSED | prior tests pass but reasoning terminal invariants and sidecar instance identity P1 remain | none / production N/A |
| Remaining AC/NFR / S7–S11 | NOT RUN | not authorized；full traceability in `08` | none / production N/A |
| Requirement package/G0/G1 | G1 product scope approved；structure evidence in `08` | user approval + default/G0/G1/strict package, YAML and diff checks | N/A |
| G2 data authority | ACCEPTED DESIGN | ADR-0013 + 段成威 2026-08-02 approval；SQLite/PostgreSQL/Redis/pgvector/bbolt 职责已冻结 | N/A |
| G2 SQLite/delete design | ACCEPTED DESIGN | ADR-0014/DEC-126-006 + Rust dependency build + fixed Runtime functional/restart delete evidence；Q-006/Q-015 Resolved，forensic WAL/log residue remains explicit limitation | N/A |
| G2 Runtime title/raw-reasoning capability | ACCEPTED DESIGN / CONDITIONAL IMPLEMENTATION | Host/Desktop foundations exist；LIA-126-002 P1 remain；historical MiniMax evidence retained；本轮0 provider calls | N/A |
| G2 DESIGN-126-003 | ACCEPTED DESIGN | exact v2 raw variants、SQLCipher schema、caps、aggregation/reconciliation、history/migration/cascade frozen；fixed raw upstream fixtures 4/4 PASS；DEC-126-017 Accepted | N/A |
| G2 Public Tasks/Pattern | ACCEPTED DESIGN | repo-local consumer inventory complete、Q-010 Resolved、DEC-126-011/012和Desktop Pattern Accepted | N/A |
| G2A source contract | PASSED / APPROVED | DEC-126-023/024与Q-017 closed；replacement `29317b...`及source/generated/fixtures/digests/post-commit gates approved；sole candidate confirmed | N/A |
| Contract Draft PR / remote CI | PR CREATED / CI FAILED / MERGE BLOCKED | [PR #1](https://github.com/36Dge/yijie-contracts/pull/1)为OPEN/DRAFT，base/head/SHA精确匹配；run 30741466028的generate/diff/lint/test/pack PASS，`pnpm audit`因`brace-expansion 2.1.2` high失败，后续`govulncheck`/`origin/main` breaking skipped；candidate未改依赖文件 | N/A |
| Local-only Delivery Strategy | ACCEPTED / S4–S6 CONDITIONAL | DEC-126-021 HOLD、DEC-126-022与LIA-126-002 pause；fake-first/default-off；G5/tag/publish/deploy N/A | N/A |

## 4. 本地 Smoke 与观察

| Check/Metric | Window | Baseline | Actual | Threshold | Result |
|---|---|---:|---:|---:|---|
| local four-component startup/E2E | none | S4–S6 foundations | not established | G4/local G6 prerequisites | NOT RUN |
| production deploy/smoke/metrics | N/A | N/A | out of scope | DEC-126-022 | N/A |

## 5. 安全与审计抽查

| 项目 | Trace/request/task/session 标识 | 结果 | Evidence |
|---|---|---|---|
| 授权/租户/审计 | synthetic IDs only | creator-private foundation exists；rejection/read audit matrix and content-free boundary NOT CLOSED | prior API tests + LIA-126-002 source/handler review |
| raw/no-log/secret | synthetic canaries only | Host raw正文不进logs/bbolt；Desktop key/error redaction与sidecar env allowlist PASS | Host/Desktop tests + logger/source scan；future UI/E2E pending |

## 6. 本地执行事件、恢复与数据状态

- Incident/异常：无发布、无feature runtime incident；评审期远端CI dependency audit只作为merge blocker登记，不属于生产事故或G2/G2A回退。
- 是否触发停止或回滚：N/A。
- 数据/队列/缓存最终状态：只创建过隔离的synthetic PostgreSQL/SQLCipher/Host temp stores，测试后停止并清理；真实业务数据未触碰。
- 回滚路径当前是否仍有效：新能力默认off；API migration为expand-only，Desktop/Host按forward repair；完整跨进程rollback尚待S10。
- Workspace：yijie既有FEAT-123删除保持未暂存/未提交；yijie/API/Host/Desktop均有仅本地closure branch与WIP checkpoint；contracts candidate、Runtime与Infra未改。

## 7. 未验证项、已知限制与接受风险

| Item | 影响 | Owner | 批准 | 截止/复查 |
|---|---|---|---|---|
| Host/Desktop title/raw-reasoning integration | Host bridge与Desktop SQLCipher基础PASS；reducer/UI/full E2E未实现 | 段成威 | flags off；按S7–S10实施/验证 | before G4 |
| Raw reasoning schema/caps | immutable source + Host caps/reconciliation + Desktop terminal schema基础PASS | 段成威 | S4–S6 accepted as implementation evidence only | S7/S9/S10 |
| Foundation Corrective Closure resume | content-free source已批准，但LIA-126-002与S7–S11仍禁止 | 段成威 | Owner另行明确恢复LIA-126-002时仅授权S4–S6；S7–S11仍单独审批 | next decision |
| Draft PR dependency audit / merge readiness | 当前CI红灯，且两个后续job steps未运行；当前candidate/PR保持不变 | 段成威 | DEC-126-021 Accepted/HOLD；只阻断merge，无audit waiver/rerun/fix/push授权 | before any future merge approval |
| Public Tasks anonymous/IDOR debt | production route must remain isolated | 段成威 | inherited controlled exception only | FEAT-126 production or 2026-09-30 earlier |
| SQLite/SQLCipher 与 delete/backup boundary | 单仓wrong-key/migration/cascade/checkpoint/backup exclusion基础PASS；完整删除saga/OS副本语义未E2E | 段成威 | flags off；不承诺forensic erase | future G4/local G6 |
| Host raw/title/Runtime cleanup | fake Runtime foundation PASS；真实Runtime跨Desktop与raw稳定性/Eval未验证 | 段成威 | v2 flags off | S7–S10 |
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
| LIA-126-002 | Foundation Corrective Closure | 已Approved并在contract-conflict stop condition暂停；DEC-126-024已通过但不自动恢复 | 段成威 | Paused；须Owner另行明确恢复，本报告不预先授权 |
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
| LIA-126-002 | 段成威 | Approved / Paused；source conflict与DEC-126-024审批均已关闭，但separate resume仍required；local checkpoints complete，S4–S6 Conditional | 2026-08-02 | DEC-126-023/024 + `07`/`08` |
| G5 Production Ready | 段成威 | N/A / Out of Scope under DEC-126-022 | 2026-08-02 | no deployment/tag/publish/production environment |
| G6 Local-only Delivery Complete | 段成威 | Pending Owner local startup and functional acceptance | N/A | requires G4 + AC-043；not Production Ready |

- 正式关闭时间：N/A；feature remains active at G2A Re-review Passed / G3-partial boundary。当前等待Owner另行决定是否恢复LIA-126-002；在明确恢复前不得继续S4–S6或进入S7。dependency remediation/merge与一次MiniMax local smoke继续分别单审，tag/publish/deploy不在本期范围。
