# FEAT-126 本地启动、停止与恢复 Runbook（S8B0 Closure Passed，G3 Partial）

> DEC-126-022将本需求冻结为Local-only Delivery。S4–S8A Closure已接受；DEC-126-032/033 Accepted且LIA-126-005 / S8B0 Closure Passed。本文仍不是可执行的完整启动runbook，也不包含完整S8B Vue UI、线上部署、生产灰度/启用、tag、package publish或registry。

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| contracts replacement | `0.3.0 sole source candidate` / tag N/A | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | SDK `21b17b50…b082`；Public `c8d9e674…354b` | DEC-126-024/025 Approved；openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Buf 1.71.0 | `origin/feat/feat-126-content-free-candidate` exact；not merged/tagged/published/activated |
| contracts prior remote | `0.3.0 historical candidate` / tag N/A | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | SDK `334db014…9404` | historical exact projection only | Draft PR/HOLD；remote CI red blocks merge only；unchanged |
| yijie-api | S4 Accepted local checkpoint / no tag | `a64f9f591fb594818c1778e30c6941e2574b3264` | generated Go `438b084d…ab33`；migration v4 `b56f7f5a…ee14` | exact `29317b...` lock；DEC-126-026 Accepted | local-lab only；secure route default off；not pushed |
| yijie-agent-host | S5 Accepted local checkpoint / no tag | `3e8df026110f0c895262329c2384d3896598f3d9` | generated Go `629ddf…63b0`；store schema v3 | exact `29317b...` source lock / oapi-codegen 2.7.2 | local only；v2 flags off；title flag forced off；not pushed |
| yijie-desktop | S6–S8A Accepted local checkpoint / no tag | `3adcb0380561c294412bc24767e4651ca872455a` | public TS `e84b70be…b678`；SQL v4/Bridge/Domain/Application/Auth/IPC/Store digests in `feature.yaml` | exact `29317b...` lock / reqwest 0.12.28 | local only；all flags off；private IPC/store present；no Vue page/route/style changes；not pushed |
| yijie governance | Accepted S8A docs baseline / no tag | `6de641f715751bb8ca94ce6804e5a33ff18d9569` | 12-file manifest in `08` | feature package | DESIGN-126-006 docs follow locally；not pushed |
| yijie-infra | no activation | N/A | N/A | N/A | none |

## 2. Local Runtime Ready 前提

- [x] G1/G2、DEC-126-024 G2A重审与LIA-126-001真实通过并有段成威批准
- [x] DEC-126-023方案C Accepted、Q-017 Resolved；本地replacement source/generated/fixtures与post-commit证据已形成
- [x] DEC-126-024批准`29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一candidate；DEC-126-025随后单独恢复LIA-126-002的S4–S6范围
- [ ] G4仍需完成S8B、S9–S10与完整本地E2E后另行通过；DEC-126-033仅接受S8B0 Closure
- [ ] Contracts/Runtime/app本地输入来自clean immutable source，full SHA/digest/generator可追溯；tag为N/A
- [ ] 本地合成identity/tenant/permission链路通过；FEAT-125 production prerequisites不属于Local-only G6
- [ ] Public Tasks consumer inventory、secure version migration 和 legacy retirement plan 完成
- [ ] Desktop本地sidecar/token/project/DB路径E2E完成
- [ ] local/API migrations在临时本地环境演练；Desktop不创建静默app backup，以rollback-in-place/forward repair/explicit reset恢复
- [ ] Permanent delete 包含批准的 SQLite/FK/WAL/checkpoint、Host bbolt/replay、Runtime thread 与 content-free receipt scope，且 app/OS backup 边界已披露并演练
- [ ] ADR-0015/0016 已批准；session-event v2 immutable pin/consumer-first conformance、raw delta/finalized reconciliation、plain-text/no-log/security fixtures、title ephemeral/pathless assertions通过；缺raw/invalid时reasoning Gate失败，不允许静默时长-only降级
- [x] DEC-126-016/Q-016已批准：raw reasoning采用Desktop SQLCipher历史持久化、history懒加载、session级联删除；正文不进入Host/云端/日志
- [x] DESIGN-126-003/DEC-126-017已批准：v2 raw events、SQLCipher schema、caps、aggregation/reconciliation、history/migration/cascade已冻结
- [x] Public Tasks仓内consumer inventory完成并关闭Q-010；DEC-126-011/012已Accepted，unknown external按safe compatibility category处理
- [x] FEAT-126 Chat/App Shell Pattern已Accepted，只取代现有Pattern中的FEAT-126冲突段落
- [x] Owner明确批准DEC-126-017、DEC-126-011/012和Pattern并给出G2通过结论
- [x] 历史G2A source/generate/fixtures/pack/supported-baseline与legacy wire equality曾PASS
- [x] DEC-126-018获得Owner批准；已形成并复验immutable source/generated full commit `c000a0245acb5c3f7ead5d2a877fb60c281c588c`
- [x] DEC-126-019历史G2A曾获Owner批准；`c000a0245acb5c3f7ead5d2a877fb60c281c588c`保持immutable
- [x] DEC-126-020仅授权并完成专用candidate branch远端可用性；remote SHA与clean clone证据PASS，`origin/develop`未移动
- [x] Draft PR #1按`develop <- feat/feat-126-contract-candidate@c000a024…588c`创建，完整摘要与CI证据已回填
- [x] DEC-126-021已Accepted/HOLD；Draft PR保持不变，不rerun/waive/fix/push；CI红灯只阻断merge
- [x] DEC-126-022已Accepted；tag/package publish/registry/线上部署/G5明确N/A
- [x] DEC-126-027/028已接受S7A/S7B Closure
- [x] DESIGN-126-005/DEC-126-029与DEC-126-030已获Owner批准；LIA-126-004只授权S8A，DEC-126-031已接受S8A Closure
- [x] DEC-126-033已Accepted；当前S8B及S9–S11仍禁止，S8B0 checkpoint不得启用flag
- [ ] Owner另行授权任何后续远端变更，包括更新/删除candidate branch、移动`origin/develop`、merge、tag或package发布
- [x] S4–S6 checkpoint记录prior exact SHA、generated digest和generator；未使用浮动branch；该记录不代表current G2A readiness
- [ ] 删除/卸载文案只承诺当前 app-managed live store 不可恢复，披露 Time Machine/APFS/第三方副本与 Application Support/Keychain 普通卸载残留
- [ ] 本地diagnostics、security assertions、startup/stop/recovery runbook已存在；生产dashboard/alerts为N/A
- [ ] Feature flags 默认 false，unsafe config fail closed
- [ ] 回滚责任人在线，真实 Go/No-Go 批准存在

## 3. 本地实现、启动、验证与停止顺序

| Order | Action | Component/Environment | Operator | Preconditions | Verification | Rollback point |
|---:|---|---|---|---|---|---|
| 1 | 核验exact contract/Runtime refs与本地工具 | local worktrees | approved implementer | LIA + digests | provenance/generator/status | stop before source edit |
| 2 | 实现并验证S4–S6 Corrective Closure | API/Host/Desktop local drafts | approved implementer | LIA-126-002 | repo tests/security/migrations/fixed Runtime | DEC-126-026 Accepted；flags off |
| 3 | 实现并验证S7A Desktop Rust Host Bridge/Domain | Desktop Rust local draft | approved implementer | DEC-126-026 accepted + explicit S7A authorization | bearer/token/nonce/SSE/domain tests；full Desktop gates；no Vue | complete/accepted by DEC-126-027；flags off |
| 4 | 实现并验证S7B application domain/outbox/reducer/history/title | Desktop Rust local draft | approved implementer | DEC-126-027 accepted + explicit S7B authorization | fake Host application E2E、migration/restart/10k reducer；no Vue | complete/accepted by DEC-126-028；flags off |
| 5 | 实现并验证S7C Rust actions/delete/interrupt/coordinator | Desktop Rust local draft | approved implementer | DEC-126-029 accepted + LIA-126-003 | fixed fixture/fake Host fault/race/restart/no-log；no Tauri/TS/Vue | complete/DEC-126-030 accepted；flags off |
| 6 | S7C Closure后单独批准S8A private IPC + TS store/view-model | Desktop Rust/TS local draft | approved implementer | LIA-126-004 | schema↔serde↔TS、auth/backpressure/stale/restart；no Vue/flag | DEC-126-031 Accepted / S8A Closure Passed；flags off |
| 7 | S8A Closure后单独执行S8B0 integration | Desktop Rust/TS local draft | approved implementer | DEC-126-032 Accepted + LIA-126-005 | exact-off gate、route/lifecycle/store/readiness schema↔serde↔TS；no full Vue/flag | DEC-126-033 Accepted / Closure Passed |
| 8 | S8B0 Closure后单独批准S8B Vue UI/a11y | Desktop Vue local draft | approved implementer | explicit S8B authorization | real store、UI/unit/visual/a11y；不得启用flag或使用production mock | not authorized / NOT RUN |
| 9 | S9 fake-provider title/raw Eval | local fixed harness | test owner | S8B Closure + explicit S9 authorization | no MiniMax/key；raw/title/no-log matrix | not authorized / NOT RUN |
| 10 | S10临时test profile启动local API/Host/pinned Runtime/Desktop并跑完整E2E | Owner machine + synthetic tenant/project | approved operator/test owner | exact local startup manifest + explicit S10 authorization | AC-001–052/security/delete/restart/process/config/SHA | stop processes；delete temp data；default flags unchanged |
| 11 | S11 Owner Local-only G6验收 | Owner machine | 段成威 | G4 evidence | AC-043 + evidence review | do not mark complete；return failing slice |
| 12 | optional future merge review | remote repos | separately approved owner | local E2E + audit fix + green CI | PR/SHA/checks | keep Draft/feature branches |

代码本地实现、schema migration、本地进程启动、feature enable、merge和部署是不同动作。LIA-126-005只覆盖S8B0本地Rust/TS integration；完整本地进程启动、feature enable以及S8B、S9–S11仍待后续明确授权，tag/publish/deploy/生产traffic/legacy retirement均N/A。

## 4. Feature Flags

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `VITE_YIJIE_CHAT_LOCAL_UI_ENABLED` | implemented but unset/default false | Chat/Tasks nav、`/chat`、`/chat/:sessionId`、component/store lifecycle | only after S8B Closure and separate activation approval；exact string `true` only；env/CI/default dev/build不得预置 | unset/false + rebuild/restart；route/loader absent | 段成威 |
| `YIJIE_DESKTOP_CHAT_SESSIONS_ENABLED` | false | Desktop local conversation | internal after base E2E | set false/restart per approved config | 段成威 |
| `YIJIE_DESKTOP_CHAT_RAW_REASONING_ENABLED` | false | Host/Desktop raw-reasoning projection/rendering/history | after v2 exact allowlist/caps/reconciliation/no-log conformance + SQLCipher migration/delete E2E + Eval | false → capability unavailable；不得用状态/时长冒充能力通过 | 段成威 |
| `YIJIE_DESKTOP_CHAT_TITLE_MODEL_ENABLED` | false | model title job | after ephemeral/pathless/schema/cost/injection Eval | false → deterministic fallback；never hidden user-thread turn | 段成威 |
| `YIJIE_DESKTOP_CHAT_DELETE_ENABLED` | false | permanent delete | after full cleanup drill | false hides/disables operation | 段成威 |
| `YIJIE_API_SECURE_TASKS_ENABLED` | false | local synthetic API profile only | after local auth/tenant/IDOR E2E；production profile remains denied | false + legacy/production isolation | 段成威 |
| `YIJIE_CHAT_LOCAL_ENABLED` | false | Desktop Rust S6 foundation | local only；requires valid synthetic owner/tenant and protected Keychain | false prevents DB/sidecar initialization | 段成威 |
| `YIJIE_CHAT_LOCAL_HOST_ENABLED` | false | Desktop sidecar supervisor | local only；absolute safe Host/Home paths | false leaves supervisor disabled | 段成威 |
| `YIJIE_AGENT_HOST_V2_RAW_REASONING_ENABLED` / `...TITLE_ENABLED` / `...CLEANUP_ENABLED` | false | Host S5 v2 surfaces | only after later cross-process authorization | false keeps v2 routes/events unavailable | 段成威 |

`YIJIE_CHAT_LOCAL_ENABLED`与`YIJIE_CHAT_LOCAL_HOST_ENABLED`是现有Rust exact-true gates；新的Vite UI flag仅为DESIGN-126-006候选。其它`YIJIE_DESKTOP_*`名称仍是未来产品级候选，不能据此认为已有实现。任何重命名需同步docs/schema/tests并重新评审。

## 5. Migration/Backfill

| Phase | Command/job | Batch/lock controls | Validation | Pause/resume | Recovery |
|---|---|---|---|---|---|
| Desktop expand | exact migration command not yet defined | app startup lock/single writer | version/checksum/FK/counts | fail before UI enable | transaction rollback-in-place；forward repair；explicit destructive reset only，no hidden backup |
| API owner expand | exact migration command not yet defined | transactional DDL/online index policy | schema/index/old app | stop before switch | keep nullable/additive state |
| API legacy owner handling | approved batch job not yet defined | bounded batches/checkpoints | no guessed owner/cross tenant | resumable | quarantine/forward correction |
| contract cleanup | future migration only after observation | no active legacy consumers | traffic/audit/contract checks | stop before destructive step | forward versioned compatibility |

Exact local migration commands must come from approved implementation slices and be recorded before G4/local G6；Codex will not invent them。

## 6. 本地验证阶段（生产灰度 N/A）

| Stage | Scope/tenant/% | Observation window | Success criteria | Stop threshold | Decision owner |
|---|---|---|---|---|---|
| Local component | temp data/individual process | ≥1 repository cycle | repo tests/readiness PASS | any migration/security/secret failure | 段成威 |
| Local integrated | synthetic user/tenant/project + fake provider | ≥1 full E2E cycle | create/stream/raw/history/restart/delete PASS | duplicate/data loss/crash/security event | 段成威 |
| Owner acceptance | Owner machine only | complete acceptance session | AC-043 and evidence PASS | any blocking gap or unverifiable claim | 段成威 |
| Production canary/expand | N/A | N/A | out of scope | future online intent must reopen production G5 | 段成威 |

## 7. Smoke

| Smoke ID | 用户路径 | 输入/租户 | 预期 | 避免真实副作用方式 |
|---|---|---|---|---|
| SMOKE-001 | new text session → stream → history reopen | synthetic prompt/project/tenant | one durable session/answer | temp project + fake provider |
| SMOKE-002 | no create permission/deep link | synthetic read-only user | fail closed, no data | no write operation |
| SMOKE-003 | cross-tenant task/session ID | synthetic A/B tenants | no existence/content leak | fixture only |
| SMOKE-004 | stop/reconnect/Host restart | synthetic active turn | deterministic terminal/recovery | temp Host/CODEX_HOME |
| SMOKE-005 | rename/pin/project remove | synthetic records | exact menus/sorting/no disk delete | temp directory |
| SMOKE-006 | permanent delete | synthetic session/temp homes | approved surfaces absent after restart | no real user data |
| SMOKE-007 | title/raw-reasoning boundaries | provider/title/raw flags off；raw正常；raw缺失/无效 | title deterministic fallback；raw正常时显示具体纯文本；raw异常时明确 unavailable 并阻断reasoning Gate | fake provider；不得新增真实MiniMax调用 |
| SMOKE-008 | raw reasoning history/delete | synthetic session with distinctive reasoning canary | 重开session按需加载；删除后DB/live UI不可恢复且checkpoint结果满足批准边界 | encrypted temp DB/CODEX_HOME；不触碰真实数据 |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| create/turn success | local test report/diagnostics | not established | exact expected sessions/turns | duplicate >0 or missing durable result | 段成威 |
| error/latency/reconnect | local E2E output | not established | NFR/SLO candidate | infinite retry or approved threshold breach | 段成威 |
| DB/migration/delete | local SQLCipher/Host/Runtime diagnostics | not established | zero corruption/fake success | any silent loss/incomplete required cleanup | 段成威 |
| auth/tenant/IDOR | local security assertions | zero unauthorized allow | only expected denies | any unauthorized allow/data leak | 段成威 |
| model quality/security | fake title/raw Eval metadata | not established | approved raw availability/plain-text/security | any MiniMax call；正文进入logs/telemetry/audit；secret/prompt/path leak | 段成威 |
| sidecar health | local Host readiness/process output | not established | ready/stable for test | crash loop/token/key exposure | 段成威 |

## 9. 回滚决策

```text
stop threshold
  → freeze expansion
  → close the narrowest affected flag/route
  → preserve local DB/audit and stop writers if integrity uncertain
  → rollback immutable app/provider artifacts only if reader-compatible
  → otherwise roll forward migration/cleanup
  → verify scope/data/audit/sidecar readiness
  → repeat synthetic smoke before any re-enable
```

| Trigger | Immediate action | Code rollback | Data action | Verification | Escalation |
|---|---|---|---|---|---|
| unauthorized allow/IDOR | close secure/legacy routes and chat flag | previous artifacts after isolation | preserve audit/evidence; no destructive cleanup | cross-tenant negatives | security incident owner |
| duplicate/data loss/corruption | stop writers/create | only reader-compatible artifact | snapshot/forward repair | counts/checksum/transcript | data owner |
| incomplete delete | disable delete only | keep chat if otherwise safe | forward cleanup; don't restore user-visible record silently | residue/deep-link test | security/data owner |
| Host/Runtime crash loop | disable send/sidecar feature | previous pinned bundle | keep local queued records | readiness/resume | runtime owner |
| title/raw-reasoning leak/cost | disable narrow flags | no base chat rollback required | purge affected SQLCipher reasoning/title records only under approved repair；session deletion uses cascade+checkpoint；保留content-free receipt | UI/DB/log/telemetry/audit/backup-boundary scan + Eval | AI/security owner |
| UI/a11y regression | halt expansion | previous Desktop artifact | preserve DB | visual/a11y smoke | client owner |

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Start local API/Host/Runtime/Desktop | Not defined until authorized slices add exact commands | local owner | blocks G4/local G6 | future local startup record |
| Disable local feature | Not defined until flags/config exist | local owner | blocks G4/local G6 | future local runbook |
| Stop/recover local processes | Not defined until orchestration exists | local owner | blocks G4/local G6 | future recovery drill |
| Migrate temp local DB | API `make test-integration`; Desktop embedded migration tests | data owner | foundation PASS；populated release/E2E still blocks G4 | evidence in `08` |
| Deploy/tag/publish | N/A under DEC-126-022 | N/A | must not execute | N/A record only |

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| 2026-08-03 | local synthetic foundations + S7A–S8A Desktop domain/IPC | API migration v4；Desktop SQLCipher schema v4 + Rust Host/application/IPC + TS ViewModel；Host bbolt schema v3 | S4–S7C matrix + S8A schema/serde/TS/auth/event/store/restart/no-log and full Desktop gates | DEC-126-026/027/028/030/031 Accepted；S4–S8A Closure Passed | S8B0/S8B、S9–S11 and four-component saga still block G4/local G6 |
| 2026-08-03 | S8B0 Desktop integration | Desktop private IPC 22 commands + exact-off UI gate/routes/lifecycle/store/readiness/Tasks metadata | 135 TS、95/96 Rust、lint/type/build/fmt/clippy/no-log | DEC-126-032/033 Accepted；S8B0 Closure Passed | S8B、S9–S11、flag activation and four-component saga still block G4/local G6 |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Product/Technical/Local Operator/Reviewer | 段成威 | current project task | decisions, local go/no-go, recovery, acceptance |
| Codex | Codex | current task | evidence drafting/execution only under explicit scope; cannot self-approve |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G5 Production Ready | 段成威 | N/A / Out of Scope under DEC-126-022 | 2026-08-02 | no deployment/tag/publish/production environment |
| G6 Local-only Delivery Complete | 段成威 | Pending Owner local startup and functional acceptance | N/A | requires G4 + AC-043；does not mean Production Ready |
