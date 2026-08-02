# FEAT-126 本地启动、停止与恢复 Runbook（G2A重审通过，Foundation Closure暂停）

> DEC-126-022将本需求冻结为Local-only Delivery。S4–S6已有基础但均为Conditional；DEC-126-023/024已关闭source conflict并通过G2A重审，但LIA-126-002仍暂停，不能继续Foundation Corrective Closure。因此本文不是可执行的完整启动runbook，也不包含线上部署、生产灰度/启用、tag、package publish或registry。

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| contracts replacement | `0.3.0 sole source candidate` / tag N/A | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | SDK `21b17b50…b082`；Public `c8d9e674…354b` | DEC-126-024 Approved；openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Buf 1.71.0 | local clean commit；not pushed/merged/tagged/published/pinned |
| contracts prior remote | `0.3.0 historical candidate` / tag N/A | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | SDK `334db014…9404` | historical exact projection only | Draft PR/HOLD；remote CI red blocks merge only；unchanged |
| yijie-api | local conditional S4 checkpoint | `b5e601764357512208cc09bfb2b30b244a1b82ac` | generated Go `05d417…af51`；migration `ee5a3a…f86c` | prior candidate lock；paused LIA-126-002 blocks continuation | local-lab only；secure route default off |
| yijie-agent-host | local conditional S5 checkpoint | `f6e4a5902d8f25632408c1c699ba17b8c66ef214` | generated Go `629ddf…63b0` | prior candidate lock / oapi-codegen 2.7.2 | local only；v2 flags off；P1 closure pending |
| yijie-desktop | local conditional S6 checkpoint | `40413b409a467a133d178137651622e167d512de` | public TS `d3493a…03b`；SQL migration digests in `feature.yaml` | prior candidate lock / openapi-typescript 7.13.0 | local only；foundation off；P1 closure pending；no final Vue flow |
| yijie-infra | no activation | N/A | N/A | N/A | none |

## 2. Local Runtime Ready 前提

- [x] G1/G2、DEC-126-024 G2A重审与LIA-126-001真实通过并有段成威批准
- [x] DEC-126-023方案C Accepted、Q-017 Resolved；本地replacement source/generated/fixtures与post-commit证据已形成
- [x] DEC-126-024批准`29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一candidate；LIA-126-002仍需另行恢复
- [ ] G4需S7–S10与完整本地E2E后另行通过
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
- [ ] LIA-126-002关闭S4–S6当前P1；DEC-126-024已通过但未自动恢复，现继续暂停，S7–S11仍禁止
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
| 2 | 实现并验证S4–S6基础切片 | API/Host/Desktop local drafts | approved implementer | LIA-126-001 | repo tests/security/migrations | revert local slice；flags off |
| 3 | 后续批准后实现consumer domain/UI | Desktop local draft | approved implementer | S4–S6 evidence | reducer/UI/a11y tests | local chat flag off |
| 4 | 启动local API/Host/pinned Runtime/Desktop | Owner machine | approved operator | exact local startup manifest | readiness/process/config/SHA | stop processes；preserve temp DB for diagnosis |
| 5 | fake-provider完整E2E | local synthetic tenant/project | test owner | four components ready | AC-001–042/security/delete/restart | close local flags；repair/retry fixtures |
| 6 | Owner Local-only G6验收 | Owner machine | 段成威 | G4 evidence | AC-043 + evidence review | do not mark complete；return failing slice |
| 7 | optional future merge review | remote repos | separately approved owner | local E2E + audit fix + green CI | PR/SHA/checks | keep Draft/feature branches |

代码本地实现、schema migration、本地进程启动、feature enable、merge和部署是不同动作。LIA-126-001 只覆盖前两项的 S4–S6 基础层；完整本地进程启动、feature enable 与 S7–S11 仍待后续明确授权，tag/publish/deploy/生产traffic/legacy retirement均N/A。

## 4. Feature Flags

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `YIJIE_DESKTOP_CHAT_SESSIONS_ENABLED` | false | Desktop local conversation | internal after base E2E | set false/restart per approved config | 段成威 |
| `YIJIE_DESKTOP_CHAT_RAW_REASONING_ENABLED` | false | Host/Desktop raw-reasoning projection/rendering/history | after v2 exact allowlist/caps/reconciliation/no-log conformance + SQLCipher migration/delete E2E + Eval | false → capability unavailable；不得用状态/时长冒充能力通过 | 段成威 |
| `YIJIE_DESKTOP_CHAT_TITLE_MODEL_ENABLED` | false | model title job | after ephemeral/pathless/schema/cost/injection Eval | false → deterministic fallback；never hidden user-thread turn | 段成威 |
| `YIJIE_DESKTOP_CHAT_DELETE_ENABLED` | false | permanent delete | after full cleanup drill | false hides/disables operation | 段成威 |
| `YIJIE_API_SECURE_TASKS_ENABLED` | false | local synthetic API profile only | after local auth/tenant/IDOR E2E；production profile remains denied | false + legacy/production isolation | 段成威 |
| `YIJIE_CHAT_LOCAL_ENABLED` | false | Desktop Rust S6 foundation | local only；requires valid synthetic owner/tenant and protected Keychain | false prevents DB/sidecar initialization | 段成威 |
| `YIJIE_CHAT_LOCAL_HOST_ENABLED` | false | Desktop sidecar supervisor | local only；absolute safe Host/Home paths | false leaves supervisor disabled | 段成威 |
| `YIJIE_AGENT_HOST_V2_RAW_REASONING_ENABLED` / `...TITLE_ENABLED` / `...CLEANUP_ENABLED` | false | Host S5 v2 surfaces | only after later cross-process authorization | false keeps v2 routes/events unavailable | 段成威 |

Exact config names remain candidate until implementation review；renaming requires synchronized docs/tests。

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
| 2026-08-02 | local synthetic foundations | API migration v3；Desktop SQLCipher schema v2；Host bbolt schema v2 | isolated PostgreSQL migrate/tests；SQLCipher wrong-key/drift/future/cascade/WAL；Host v1→v2 receipt migration/symlink tests | HISTORICAL FOUNDATION PASS / closure incomplete | current P1 + paused LIA-126-002 + four-component saga block G4/local G6 |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Product/Technical/Local Operator/Reviewer | 段成威 | current project task | decisions, local go/no-go, recovery, acceptance |
| Codex | Codex | current task | evidence drafting/execution only under explicit scope; cannot self-approve |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G5 Production Ready | 段成威 | N/A / Out of Scope under DEC-126-022 | 2026-08-02 | no deployment/tag/publish/production environment |
| G6 Local-only Delivery Complete | 段成威 | Pending Owner local startup and functional acceptance | N/A | requires G4 + AC-043；does not mean Production Ready |
