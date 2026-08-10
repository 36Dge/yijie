# FEAT-126 本地启动、停止与恢复 Runbook（DESIGN-126-017 Complete / Preclaim Corrective Closure Accepted / BLK-008/009/010/011 Closed）

> DEC-126-022将本需求冻结为Local-only Delivery。DEC-126-062/063关闭BLK-007并形成clean checkpoints后，LIA-126-024/S10B-R7已单独授权和消费：S10B-001 PASS，S10B-002因缺少完整四组件orchestrator fail closed，003–011 NOT RUN，012仅abort cleanup subset。Owner已接受DEC-126-064/065/066并完成DESIGN-126-014、LIA-126-025/S10BO1 Corrective Closure及`S10B-BLK-008`关闭；DEC-126-067进一步形成API/Host/Desktop/Infra/Governance本地clean checkpoints。LIA-126-027 isolated live 的失败事实保留且run不可复用；Owner已接受DESIGN-126-016与LIA-126-028/S10BO3 Corrective Closure并关闭`S10B-BLK-010`。G3保持Partial。本文不授权isolated live、fresh R8、S11、MiniMax、default activation或发布。

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| contracts replacement | `0.3.0 sole source candidate` / tag N/A | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | SDK `21b17b50…b082`；Public `c8d9e674…354b` | DEC-126-024/025 Approved；openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Buf 1.71.0 | `origin/feat/feat-126-content-free-candidate` exact；not merged/tagged/published/activated |
| contracts prior remote | `0.3.0 historical candidate` / tag N/A | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | SDK `334db014…9404` | historical exact projection only | Draft PR/HOLD；remote CI red blocks merge only；unchanged |
| yijie-api | S4 Accepted remote candidate checkpoint / no tag | `a64f9f591fb594818c1778e30c6941e2574b3264` | generated Go `438b084d…ab33`；migration v4 `b56f7f5a…ee14` | exact `29317b...` lock；DEC-126-026 Accepted | `origin/feat/feat-126-foundation-closure` exact；local-lab only；secure route default off；not merged/activated |
| yijie-agent-host | S10P1 local test-profile checkpoint over S9 / no tag | local `e0a8d3d29a335571d1654d95e1e262c240755674`；parent `8707dea552cff74121b89aa8045f27da2c8c9378`；remote remains `3e8df026110f0c895262329c2384d3896598f3d9` | S9 fixture authority + fixed loopback fake Responses + parent watchdog；store schema v3 unchanged | exact `29317b...` source lock / fixed Runtime `3aa317ce...` | local/not pushed；default MiniMax/v2/title paths unchanged；not merged/activated |
| yijie-agent-host | S10BF1 Host-owned readiness checkpoint / no tag | local `1ca4ee555586e5243f7101b9fe056c6fa117a560`；parent `e0a8d3d29a335571d1654d95e1e262c240755674` | explicit dataset/case/digest health + closed probe；business store/wire unchanged | exact `29317b...` / fixed Runtime `3aa317ce...` | clean local/not pushed；test-only；default provider unchanged |
| yijie-desktop | S10P3 local Closure candidate / no tag | local `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；parent `46107eec1e9cba0257252cae8678a4233ef20036`；remote remains `35f27447398529cca4dec85fa1f67e779c7a7cbd` | SQLCipher v5 + Public-before-Host + closed control-plane IPC/TS；repo + real main-chain PASS | exact `29317b...` lock；Cargo/pnpm locks unchanged | clean local checkpoint/no push；all default flags off |
| yijie governance | S10BF1 Closure accepted / no tag | execution baseline `db12fe6ce4a8c1f84ac90781191d8a1b26dbcc4d`；remote remains `650254b3c009c4098f7d7b2d415ed8082b0139fa` | FEAT-126 governance only | DEC-126-053–057 Accepted；package/strict/G2A/YAML/lint/test/shell/diff required | local/not pushed；S10B-BLK-005 Closed；no R5/S11 authorization |
| yijie-api | LIA-126-013 accepted local checkpoint / no tag | local `c5f334e88d54d9e04f388d0349f4f5925124abd6` | exact FEAT-126 profile/matrix, atomic batch, verifier, tests | lint/vet/race/unit PASS；historical fresh-v4 integration PASS | clean local checkpoint；no central wire/schema；not pushed |
| yijie-api | S10BRP1 accepted local checkpoint / no tag | local `d1c72b29ffc567abdb4521343a73ceef9ac9da34`；parent `c5f334e88d54d9e04f388d0349f4f5925124abd6` | closed API runtime profile + strict config/route/address regression | `make lint/test` PASS | clean local/not pushed/activated；not S10B evidence |
| yijie-infra | S10BM1 corrective local checkpoint / no tag | local `bb96333df908d6fea72ec0a1f57a64477c2428e4` | accepted bootstrap/image helpers + migration/bootstrap shared run-scoped full API SHA authority | validate/lint/test 87/87 + security/shell/Node/diff PASS | clean local checkpoint；not pushed；no S10B rerun/resource start |
| yijie-infra | S10BD1 corrective local checkpoint / no tag | local `2a643caef210e32cab80242ede46b96927b2097a`；parent `bb96333df908d6fea72ec0a1f57a64477c2428e4` | capability-first closed classifier + exact immutable identity + bounded no-start resolver | focused 12/12、full 99/99、validate/lint/shell/security/diff与live 3 identity/3 probe PASS | clean local/not pushed；no pull；post resources 0；Docker restored stopped |
| yijie-infra | S10BF1 single-preflight checkpoint / no tag | local `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`；parent `2a643caef210e32cab80242ede46b96927b2097a` | single seven-SHA runner consuming Host-owned probe；no fixture input | full 103/103 + fresh combined preflight PASS | clean local/not pushed；R5=false；Docker restored stopped |
| yijie-infra | S10BRP1 accepted local checkpoint / no tag | local `8f9b8965dbd32bb7273059a80bb818d4344e7135`；parent `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9` | single runtime authority、preflight summary `api_binary_sha256`、same-run closed continuation launcher | validate/lint/test 113/113 + launcher child/negative/binary-drift conformance PASS | clean local；no service/Docker run；not pushed |
| yijie-infra | S10I local identity-profile checkpoint / no tag | local `8d7c84dc963141931c6c5d3c3aded3218247df0b`；parent `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf` | exact dynamic numeric nbf mapper/static-live conformance；Compose/image digests unchanged | private default-off profile | DEC-126-044 Accepted；not pushed/activated |

## 2. Local Runtime Ready 前提

- [x] G1/G2、DEC-126-024 G2A重审与LIA-126-001真实通过并有段成威批准
- [x] DEC-126-023方案C Accepted、Q-017 Resolved；本地replacement source/generated/fixtures与post-commit证据已形成
- [x] DEC-126-024批准`29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一candidate；DEC-126-025随后单独恢复LIA-126-002的S4–S6范围
- [ ] G4仍需完整fresh S10B Closure；LIA-126-024/S10B-R7已消费，S10B-001 PASS但002因缺少完整四组件可执行authority fail closed，003–011未运行，012仅abort cleanup subset；DEC-126-066已接受S10BO1 repository Corrective Closure并关闭`S10B-BLK-008`，但isolated live与fresh R8仍未授权，完整fresh S10B-001–012尚未PASS
- [ ] Contracts/Runtime/app本地输入来自clean immutable source，full SHA/digest/generator可追溯；tag为N/A
- [x] 本地合成identity/tenant/permission链路通过；standard Authorization Code + PKCE含numeric `nbf`，unchanged API capability/Public create通过；FEAT-125 production prerequisites不属于Local-only G6
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
- [x] S4–S9 Closure Passed；S10A read-only review complete；DEC-126-037 Option C Accepted；S10P0只读设计候选已形成
- [x] DEC-126-038方案B已由Owner接受；Public Task retained-row删除边界已冻结，但不授权实现
- [x] DEC-126-039已接受S10E Closure并关闭BLK-001；本地Infra checkpoint未push
- [x] DEC-126-040接受LIA-126-009/S10P1 Closure并正式关闭BLK-002/003
- [x] DEC-126-041保留历史native HOLD；DEC-126-043关闭BLK-004；DEC-126-045接受S10P3 Closure并关闭BLK-005；LIA-126-008现仅授权S10B-001–012，S11和default activation仍未授权
- [x] DEC-126-042 Option A已由Owner安全/G2正式接受；只改变Local-only BLK-004退出设计，不自动关闭blocker或授权代码
- [x] LIA-126-011已通过S10P2F-001–012与Desktop全门禁；[x] DEC-126-043 Option A已接受，S10P2F Closure Passed、Local-only BLK-004 Closed；Apple signed Keychain只登记Deferred Native Hardening，不得写成PASS
- [x] Owner另行授权的yijie/API/Host/Desktop checkpoint push已完成；连同contracts候选共五仓经`ls-remote`和临时clean clone复验为exact SHA；这不代表merge、tag、publish、deploy、activation、G4或G6
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
| 8 | S8B0 Closure后单独批准S8B Vue UI/a11y | Desktop Vue local draft | approved implementer | LIA-126-006 | real store、UI/unit/visual/a11y；不得启用flag或使用production mock | implemented at `35f2744…7cbd`; DEC-126-034 Accepted / Closure Passed |
| 9 | S9 fake-provider title/raw Eval | versioned Host runner/dataset + Desktop exact consumer validation | test owner | DEC-126-035 Accepted + explicit LIA-126-007 authorization + frozen dataset/split/runner/fixture hashes | fixed fake provider/pins/synthetic data；title 250/250 schema、200/200 semantic、50/50 unsafe；raw 210/210 valid、40/40 negative；plaintext/no-log/injection gates PASS | EXECUTED / DEC-126-036 Accepted；Host `8707dea…9378`、Desktop `adfdb5b…f9cb` local only |
| 10 | S10A只读readiness/test-profile评审 | yijie docs + affected repos | Codex/reviewer | DEC-126-036 + Owner S10A scope | exact SHA/tool/source/port inventory + DESIGN-126-007 | COMPLETE / DEC-126-037 Option C Accepted；no process/flag/data write |
| 11 | S10P0 corrective设计评审 | yijie docs + affected repos read-only | Codex/reviewer | Owner S10P0 scope | DESIGN-126-008/DEC-126-038 Option B Accepted + governance gates | docs-only；no runtime rollback |
| 12 | S10E Compose/isolated identity准备 | local Infra + user-level plugin discovery | separately approved operator | DEC-126-038 Accepted + explicit S10E authorization | PASS；DEC-126-039 Accepted / Closure Passed，Infra `99e50d8…6baf` | restore link backup；stop exact run；volume deletion separately approved |
| 13 | S10P1 fake provider/child profile | Host/Desktop private config | LIA-126-009 approved implementer | S10E Closure + explicit S10P1 authorization | CLOSURE PASS；DEC-126-040 Accepted | master false；terminate only this run；preserve content-free evidence |
| 14 | S10P2 secure-storage isolation | Desktop private storage config | LIA-126-010 approved implementer | S10P1 Closure + explicit S10P2 authorization | source gates PASS；signed native lifecycle BLOCKED | remove only exact run manifest items；Closure HOLD |
| 15 | S10P2F ephemeral local-only adjustment（Closure Passed） | Desktop Rust test-only storage | LIA-126-011 approved implementer | explicit S10P2F authorization | PASS：double-exact/CSPRNG/0700-0600/O_EXCL/O_NOFOLLOW/restart/cross-run/no-log/exact cleanup | checkpoint `46107ee…0036`；DEC-126-043 Accepted；independent flag false returns Protected Data path |
| 16 | S10P3 Public Tasks main chain + S10I（Closure Passed） | Desktop Rust/TS/Vue private domain + local S10E identity profile | separately approved implementer | BLK-004 closure + retained-row acceptance + DEC-126-044 | repo/static-live/real numeric nbf/Public bind/delete-retention PASS；DEC-126-045 Accepted | flags off；forward reader；do not delete Public row |
| 17 | S10B临时test profile四组件E2E（Executed / Blocked） | Owner machine + synthetic tenant/project | approved operator/test owner | BLK-001–005 closed + LIA-126-008 Accepted | S10B-001 bootstrap-profile FAIL；002–012 NOT RUN；DEC-126-046 Accepted/rejected Closure | stopped containers/networks；deleted temp binaries；defaults unchanged；volumes retained |
| 18 | S10BP0/S10BP1 closed bootstrap纠偏 | yijie + API + Infra local | reviewer / approved implementer | DEC-126-046/047 + LIA-126-013 | S10BP1-001–013 PASS；DEC-126-048 Accepted | remove only new profile/batch/verifier/wrapper；never alter feat125/generic |
| 19 | S10BR1 exact image availability纠偏 | yijie + Infra local | reviewer / approved implementer | DESIGN-126-010 / DEC-126-049/050 | S10BR1-001–010 PASS；Closure Accepted | restore old preflight only；never pull/floating-tag/delete volume |
| 19 | S11 Owner Local-only G6验收 | Owner machine | 段成威 | accepted fresh S10B Closure + G4 evidence | AC-043 + evidence review | do not mark complete；return failing slice |
| 19 | optional future merge review | remote repos | separately approved owner | local E2E + audit fix + green CI | PR/SHA/checks | keep Draft/feature branches |

代码实现、Closure接受、环境准备、schema migration、本地进程启动、临时test flag、默认feature activation、merge和部署是不同动作。DEC-126-039只接受S10E；DEC-126-040只接受LIA-126-009/S10P1 Closure；DEC-126-041 Option B保留历史native S10P2 source/HOLD事实；DEC-126-043只接受S10P2F并关闭BLK-004；DEC-126-045只接受S10P3 Closure并关闭BLK-005。S10B/S11仍须依序单独批准。

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
| `YIJIE_AGENT_HOST_V2_RAW_REASONING_ENABLED` / `...TITLE_ENABLED` / `...CLEANUP_ENABLED` | false | Host S5 v2 surfaces | LIA-126-008仅允许raw/cleanup在S10B child profile临时exact true；title持续false；普通启动与退出后仍false | false keeps v2 routes/events unavailable | 段成威 |
| `YIJIE_FEAT126_S10_EPHEMERAL_SECRET_BACKEND_ENABLED` | implemented / unset / default false | S10P2F Desktop Rust test-only secret backend | 只能在S10 master exact true、本flag exact true、canonical run manifest合法且经单独批准的test run中使用；不得写入`.env`/CI/build default | unset/false；完全回到Protected Data Keychain路径 | 段成威 |

`YIJIE_CHAT_LOCAL_ENABLED`与`YIJIE_CHAT_LOCAL_HOST_ENABLED`是现有Rust exact-true gates；Vite UI flag已在S8B0实现为unset/default-false且未启用。其它`YIJIE_DESKTOP_*`名称仍是未来产品级候选，不能据此认为已有实现。任何重命名需同步docs/schema/tests并重新评审。

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
| S10P2F file-integrity/secret/no-log failure | 立即关闭ephemeral独立flag并停止本run | 不改production/default artifact；获批slice只在reader-compatible时回退 | 停Desktop/Host/Runtime与SQLCipher后，仅对owner/run/manifest/mode/nlink/canonical全匹配的三文件执行exact cleanup；mismatch时不删 | default Protected Data回归、post exact inventory、source/log/process/bundle hit=0 | security/data owner |

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Preflight local stack | `docker compose version`；六仓SHA/status；Runtime digest；fixed-port listener scan | local owner | Compose v5.3.0 discovery修复、hash/config PASS；停止后fixed ports无listener | DEC-126-039 Accepted evidence |
| Prepare S10E environment | 备份/修复用户Compose plugin link；新`feat-126-s10`run-scoped profile的validate/prepare/status/stop | local owner | EXECUTED / PASS / OWNER ACCEPTED | Infra `99e50d8…6baf` + S10E manifest |
| Start local dependencies | S10E exact profile；digest-pinned API DB/Keycloak DB/Keycloak/Caddy | local owner | EXECUTED FOR S10E ONLY / stopped after verification | runtime verifier + stop inventory；not S10B evidence |
| Migrate/bootstrap API | `feat-126-s10-local-lab`权威wrapper已由DEC-126-048接受，内部固定4份reviewed manifests及API-owned atomic batch/verifier | data owner | 只允许隔离验证；不得用于未授权S10B，不得使用generic/manual SQL | S10BP1 Closure Passed；not S10B evidence |
| Build/start API | host process on fixed loopback with S10E DB/OIDC/TLS profile | local owner | S10I fresh run started and stopped；standard native token accepted；Public create/bind/delete-retention PASS | DEC-126-045 Accepted Closure evidence；not S10B evidence |
| Inspect FEAT-126 API runtime authority | `make feat-126-s10-api-runtime-profile` | read-only reviewer | closed content-free authority only；无profile override | DEC-126-059 Accepted；Infra `8f9b8965…7135` |
| Continue API after accepted preflight | `make feat-126-s10b-api-continuation`只接收canonical run ID与七仓SHA；从固定run路径读summary/secrets/CA/binary，校验`api_binary_sha256`与文件身份双快照后由同一reader/builder产生profile/env；该入口只启动API | future separately authorized full-process corrective only | R7审查确认它不启动Compose、fake、Desktop、Host或Runtime，不能作为S10B-002–012完整authority；本次未执行 | LIA-126-024 consumed / S10B-002 FAIL-CLOSED / BLK-008 Open；禁止人工拼接续跑 |
| Build Host/start Desktop/Runtime | Host/fake临时binary已build；Desktop `pnpm tauri dev`与Host/Runtime child因bootstrap stop condition未执行 | local owner | S10B-001 fail closed；业务进程启动数0 | DEC-126-046 Accepted / rejected Closure evidence |
| Stop local stack | process-group SIGTERM/deadline；Infra `make feat-125-local-stop && make dev-down`；verify no PID/listener/default-on | local owner | command frozen；not executed | future cleanup manifest |
| Migrate temp local DB | API `make test-integration`; Desktop embedded migration tests | data owner | foundation PASS；populated release/E2E still blocks G4 | evidence in `08` |
| Deploy/tag/publish | N/A under DEC-126-022 | N/A | must not execute | N/A record only |
| Verify candidate provenance | `git ls-remote` + temporary exact single-branch clean clone | read-only reviewer | exact HEAD + clean status；no remote mutation | DEC-126-035 evidence in `08` |

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| 2026-08-03 | local synthetic foundations + S7A–S8A Desktop domain/IPC | API migration v4；Desktop SQLCipher schema v4 + Rust Host/application/IPC + TS ViewModel；Host bbolt schema v3 | S4–S7C matrix + S8A schema/serde/TS/auth/event/store/restart/no-log and full Desktop gates | DEC-126-026/027/028/030/031 Accepted；S4–S8A Closure Passed | historical checkpoint；later S8B0/S8B rows supersede UI gaps；S9–S11/four-component saga remain |
| 2026-08-03 | S8B0 Desktop integration | Desktop private IPC 22 commands + exact-off UI gate/routes/lifecycle/store/readiness/Tasks metadata | 135 TS、95/96 Rust、lint/type/build/fmt/clippy/no-log | DEC-126-032/033 Accepted；S8B0 Closure Passed | S8B later implemented under LIA-126-006；S9–S11/activation/four-component saga remain |
| 2026-08-03 | LIA-126-006 S8B Desktop Vue UI | Desktop `35f2744…7cbd`；real Vue pages/App Shell/composer/reasoning/menus/scroll/a11y；flag off | 29/164 TS、axe 0 serious/critical、build、95/96 Rust、npm audit、browser/security scans | DEC-126-034 Accepted / S8B Closure Passed | VoiceOver manual remains for S11/G6；S9–S11、flag activation and four-component saga still block later gates |
| 2026-08-04 | LIA-126-007 S9 deterministic fake Eval | Host `8707dea…9378` + Desktop `adfdb5b…f9cb`；`feat126-title-raw-v1` 250 synthetic samples；flags off | Host title/raw authority gates、Desktop exact SSE→reducer→SQLCipher→history/delete→plain-text Vue consumer、repo/security/no-log gates | DEC-126-036 Accepted；all S9 P1 closed | no process startup/rollback drill；S10–S11、activation and four-component saga remain |
| 2026-08-04 | S10A read-only readiness review | six fixed SHAs + Runtime artifact + local tool/source inventory | no process startup；Compose/provider/sidecar/Keychain/Public Tasks checks | DESIGN-126-007 + DEC-126-037 Option C Accepted；S10B HOLD | S10A-BLK-001–005 open；no rollback action because no mutable runtime state was created |
| 2026-08-04 | S10P0 corrective design review | Governance `0ceb047…b43cfb` + design checkpoint `5145592…1748` + fixed Contracts/API/Host/Desktop/Runtime；Infra read-only inventory | bundled Compose direct version/config only；Host/Desktop/Public Tasks source inspection；governance docs | DESIGN-126-008/DEC-126-038 Option B Accepted；0 runtime mutation | S10E/P1/P2/P3均NOT RUN，无可执行rollback |
| 2026-08-04 | S10E isolated environment | Infra parent `f040492…af2` + API exact `a64f9f…3264`；local Compose/images | recoverable user plugin link；default-off profile；two isolated synthetic runs；migration/identity/TLS/runtime/no-log/rejected-run/stop | DEC-126-039 Accepted / Closure Passed / BLK-001 Closed；Infra `99e50d8…6baf` local/clean/not pushed | zero active container/network/listener；8 volumes + 2 ignored run roots retained；polluted run marked REJECTED；restore old link or delete exact resources only after separate approval |
| 2026-08-04 | LIA-126-009 S10P1 | Host `e0a8d3d…5674` + Desktop `fba934c…7285` + fixed Runtime | exact keyless loopback fake turn；actual Desktop child readiness/stop；pre-spawn evidence、parent watchdog、crash/restart/stale/log cap/no-log；default-off scan | DEC-126-040 Accepted；S10P1 Closure Passed；BLK-002/003 Closed；local clean/not pushed | close master returns default path；no Keychain/DB schema/IPC/remote state；S10P2/P3/S10B remain blocked |
| 2026-08-04 | LIA-126-010 S10P2 | Desktop `c863b2a…5dc68` | double exact gate、run-derived namespaces、manifest、app-data/Home/project binding、exact inventory、cleanup/recovery/race；165 TS + 113 Rust | source PASS；DEC-126-041 Option B historical Closure HOLD；native probe BLOCKED；Local-only successor later closed BLK-004 under DEC-126-043 | close secure-storage gate returns fixed namespace；post exact tuples absent，temp root removed；no S10P3/S10B |
| 2026-08-04 | DEC-126-042 Local-only adjustment review | Governance candidate `35cbf8e…52667` + unchanged Desktop `c863b2a…5dc68` | docs-only freeze and Owner acceptance of double-exact/CSPRNG/owner-only file/restart/cross-run/cleanup/no-log/default-off design | DESIGN ACCEPTED / Option A；at that time BLK-004 Open；later closed by DEC-126-043 | 无runtime/data rollback；S10P2F was then separately authorized |
| 2026-08-04 | LIA-126-011 S10P2F | Desktop `46107ee…0036` + Governance baseline `a5c5dde…ae04` | 6 Rust files；19 targeted pass/1 native ignored；124 full pass/2 native ignored；165 TS；CSPRNG/restart/cross-run/fault/exact cleanup/no-log/default-off | CLOSURE PASS / DEC-126-043 Option A Accepted；0 Xcode/Keychain/MiniMax/real data/remote write；BLK-004 Closed | unset ephemeral flag returns Protected Data；final exact temp root=0；no recursive cleanup；no S10P3/S10B |
| 2026-08-04 | DEC-126-043 approval reconciliation | Governance baseline `24e6ef4…e7c1` + unchanged Desktop `46107ee…0036` | Owner Option A acceptance；package/strict/G2A/YAML/lint/test/diff/scope | S10P2F Closure Passed / Local-only BLK-004 Closed；no business source/runtime/remote action | 当时S10P3/S10B/S11未授权、BLK-005 Open；BLK-005后由DEC-126-045关闭；native Deferred/NOT RUN |
| 2026-08-04/05 | LIA-126-012 + DEC-126-044/S10I + DEC-126-045 | Desktop `ed9eb14…b78c` + Infra `8d7c84d…df0b` + fresh S10E run | TS/Rust/migration/private projection；exact mapper；native Authorization Code + PKCE；unchanged API；real create/bind/delete-retention；DB denylist | implementation/real main chain PASS；S10P3 Closure Passed；BLK-005 Closed | API/containers stopped；named volumes retained；local checkpoints only/no push；S10B unauthorized |
| 2026-08-05 | LIA-126-008 authorization | fixed Contracts/API/Host/Desktop/Runtime/Infra baselines + current governance approval overlay | governance reconciliation only；no process start or flag activation | S10B AUTHORIZED / NOT RUN；S10B-001–012 only | no rollback state；S11/MiniMax/default activation/remote actions remain unauthorized |
| 2026-08-05 | LIA-126-008 S10B first execution | run `9b9d455f-0500-4dd0-a008-d5a862bf6f20`；exact baselines；fresh exact-digest dependencies | init/config/up/TLS/OIDC/users/migration PASS；tracked bootstrap with approved profile fail closed；DB count reconcile；authoritative stop | S10B-001 FAIL；002–012 NOT RUN；当时S10B-BLK-001 Open、后来由DEC-126-048关闭；DEC-126-046 Option A Accepted，Closure rejected | containers/networks/listeners 0；temporary binaries removed；4 run volumes + ignored record retained；no correction/retry authorized |
| 2026-08-05 | S10BP0 corrective design | API/Infra read-only source + current yijie governance overlay | profile/ordering/manifest/matrix/transaction/Infra gap inventory；DESIGN-126-009/DEC-126-047/LIA-126-013 proposal | DESIGN COMPLETE；0 source/process/data mutation；LIA-126-013 NOT AUTHORIZED | no runtime rollback；do not implement or rerun until separate approval |
| 2026-08-05 | LIA-126-013 S10BP1 implementation | API/Infra/yijie local diffs + fresh isolated PostgreSQL | exact profile/order negatives；migration v4；two atomic passes；exact counts/audits；rollback injection；full repo/governance gates | S10BP1-001–013 PASS；DEC-126-048 Accepted；BLK-001 Closed；S10B not rerun | temporary container/anonymous volume/candidate/secret removed；three 0600 content-free summaries retained ignored；no commit/push |
| 2026-08-05 | S10B-BLK-002 observation | accepted S10E helper + local Docker 29.6.1 image inventory | exact local ID/digest exists；tag/tag@digest `docker image inspect`曾失败，Docker重启后恢复；helper因此存在状态敏感假阴性 | historical OPEN / outside LIA-126-013 | 后续由DESIGN-126-010/DEC-126-049/050单独纠偏并Closed |
| 2026-08-05 | DESIGN-126-010 / S10BR1 image corrective | Infra local diff + fresh run `ae1c892a-4819-40bc-9ce9-d72f6ea2fcd7` | 从唯一Compose pin派生3个repository@digest；85/85与negative matrix PASS；`--pull never`四服务healthy；权威stop | DEC-126-050 Accepted / S10BR1 Closure Passed / BLK-002 Closed | 0 image pull/API/Desktop/Host/Runtime；container/network=0；4 volumes与ignored run record保留；无commit/push |
| 2026-08-05 | LIA-126-014 / S10B-R2 fresh preflight | clean seven-repository checkpoint + run `4ffa07b9-6e4c-45d4-b5d5-3b3be5d7d818` | migration wrapper固定旧API `a64f9f...`并在secret/run/Docker/DB前拒绝当前`c5f334e...` | S10B-001 FAIL / 002–012 NOT RUN / S10B-BLK-003 Open / DEC-126-051 Accepted、Closure Rejected | run root/container/network/volume/process/model/keychain/real-data/remote-write=0；不修复、不重跑 |
| 2026-08-05 | DEC-126-051/052 / LIA-126-015 / S10BM1 | Owner接受fail-closed事实并拒绝S10B-R2 Closure；随后接受shared API authority corrective Closure | migration/bootstrap统一full API SHA + run-scoped closed authority；private old two-arg helper fail closed | Infra `bb96333d...`；87/87 + validate/lint/shell/Node/diff PASS；DEC-126-052 Accepted | runtime resource=0；BLK-003 Closed；先形成Governance SHA再单独审批LIA-126-016 |
| 2026-08-05 | Governance checkpoint / LIA-126-016 | DEC-126-052 Accepted overlay形成clean local checkpoint，随后Owner单独批准并已消费S10B-R3 | Governance `441663faf7d505015f03d572c8e9f30b3ba1a2df`；six implementation pins unchanged | CONSUMED / CLOSURE FAIL | actual run见下一行；S11仍未授权 |
| 2026-08-05 | LIA-126-016 / S10B-R3 single execution | execution Governance `784c970a7d6330fc2c2432f0ae9bf7bca400b15c` + exact six implementation pins + run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5` | seven clean SHA/tool/port/init/config PASS；generic immutable-image verifier FAIL before Compose up | S10B-001 FAIL；002–012 NOT RUN；S10B-BLK-004 Open；DEC-126-053 Accepted/Closure rejected | owner-only REJECTED + exact stop；container/network/volume/listener=0；ignored run root/secret retained；no pull/retag/restart workaround/rerun/model/remote action |
| 2026-08-05 | DESIGN-126-011 / S10BD0 / LIA-126-017 approval | Infra read-only verifier/Compose/test inventory + Docker capability differential + governance update | endpoint unavailable被generic verifier误报；此前capability可用时correct pin可解析；capability-first/closed classes/exact original pin/no-pull resolver probe设计冻结 | DESIGN/DECISION ACCEPTED；LIA-126-017 APPROVED / HELD / NOT STARTED | 未启动Docker/container/service；未修改Infra源码；未执行create/remove、pull/retag/restart或S10B；授权未消费 |
| 2026-08-05 | LIA-126-017 / S10BD1 execution | Governance `075a5051…4484` + Infra `2a643cae…97a` + live run `12600000-0000-4000-8000-000000000055` | capability-first、12 closed classes、exact Compose identity与no-start resolver | 12/12 + 99/99 + 3 identity/3 probe PASS；DEC-126-055 candidate | labeled resources=0；Docker restored stopped；no pull/retag/workaround/S10B/model/remote action；BLK-004 Owner Pending |
| 2026-08-05 | DEC-126-055 Option A acceptance | Owner接受S10BD1 Closure | S10B-BLK-004 Closed；S10B-BLK-001–004均Closed | G3 Partial；G4/G6 Pending | 不自动授权S10B-R4/S11/MiniMax/activation/remote action |
| 2026-08-05 | LIA-126-018 / S10B-R4 single execution | exact seven-repository pins + fresh run `96a0a80d-27d4-4022-a470-4a7f004d9c4c` | resolver/dependencies/TLS/OIDC/users/migration/bootstrap/API ready PASS；fake request fixture identity 403 | S10B-001 FAIL；002–012 NOT RUN；S10B-BLK-005 Open；DEC-126-056 Accepted disposition | API/fake stopped；container/network/listener=0；temp root deleted；4 volumes + ignored run record retained；Docker restored stopped；no correction/retry/model/remote action |
| 2026-08-05 | DEC-126-056/057 / LIA-126-019 / S10BF1 | Governance `db12fe6…cc4d`、Host `1ca4ee5…a560`、Infra `5723ffd…c0c9`、fresh run `ed22fc82…f3f4` | single runner完成resolver/dependencies/TLS/OIDC/users/migration/bootstrap/API/fake readiness；summary `8198442e…f7d9` | S10B-001 combined preflight PASS；DEC-126-057 Accepted；BLK-005 Closed；R5 NOT RUN/unauthorized | API/fake/container/network/listener=0；4 volumes/ignored record retained；Docker restored stopped；no MiniMax/Keychain/real data/remote action |

S10BF1唯一入口为Infra的`make feat-126-s10b-preflight`。它只接受fresh `RUN_ID`和七个full SHA；严禁新增dataset/fixture/header参数或用手工curl代替Host probe。失败只记录closed class并停止；成功摘要必须明确`scope=S10B-001-combined-preflight`与`s10b_r5_executed=false`。该命令不是日常启动入口；DEC-126-057已接受，而fresh R5仍须单独明确授权。

DESIGN-126-008对未来corrective的回滚语义冻结如下：

- S10E：恢复备份的旧plugin symlink；只停本run Compose project；只能在manifest精确列出且Owner授权时删除本run volumes，绝不处理普通/foreign volumes。
- S10P1：关闭master profile即回到MiniMax/default-off路径；终止fake/Host/Runtime child并保留最小content-free failure manifest；不修改Runtime pin。
- S10P2：只在master与`YIJIE_FEAT126_S10_SECURE_STORAGE_ENABLED`均exact `true`时运行。先停Desktop/Host/Runtime并关SQLCipher，再由`cargo run --locked --example feat126_secure_storage -- cleanup`从canonical run manifest内部派生并删除三个exact test items和run root；shell不得传service/account。manifest mismatch、活跃Desktop PID或路径/owner/mode异常时停止而不删。
- S10P2F（DEC-126-043 Accepted）：独立ephemeral flag缺失/false即完全回到当前Protected Data路径。获批test run只能在完成进程/SQLCipher停止序列后unlink当前run manifest的三个exact files；symlink/hardlink/foreign owner/wrong mode/canonical mismatch时delete=0，不递归删除未知文件。unlink不承诺SSD/swap/backup法证擦除。
- S10P3：保持forward SQLCipher v5 reader，关闭feature flags/停coordinator；完成已接受Host/Runtime cleanup和local cascade；不猜测/删除Public Task row，不回滚到会丢失binding的旧writer。
- S10B授权边界：DEC-126-044/S10I已完成且API verifier未改，DEC-126-045已关闭BLK-005；LIA-126-008授权已在首次fail-closed执行中消费。DEC-126-046拒绝Closure；不得手工token、放宽claim、generic bootstrap、manual SQL或mock signer替代。
- S10BP1候选回滚：只关闭/移除新`feat-126-s10-local-lab`分支与Infra权威wrapper；既有feat125/generic路径不得变化。出现validation-order、audit atomicity、no-log或兼容回归时停止，不用旧volume补证据；S10B重跑必须另行授权。

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Product/Technical/Local Operator/Reviewer | 段成威 | current project task | decisions, local go/no-go, recovery, acceptance |
| Codex | Codex | current task | evidence drafting/execution only under explicit scope; cannot self-approve |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G5 Production Ready | 段成威 | N/A / Out of Scope under DEC-126-022 | 2026-08-02 | no deployment/tag/publish/production environment |
| G6 Local-only Delivery Complete | 段成威 | Pending Owner local startup and functional acceptance | N/A | requires G4 + AC-043；does not mean Production Ready |

### S10B-R5 abort/restore记录

- run：`24ae14b7-46d1-4fd5-a7ac-a30932586ad6`；S10B-001 summary SHA-256：`b3e4b833283bf0102edfc4100cd0339002d769d839b7903a2a4426c531b6b1f8`。
- stop trigger：完整链要求的FEAT-126 runtime service-profile authority不能由当前API表达；不得用旧FEAT-125 profile替代。
- restore：停止API/fake；移除本run四个containers和四个networks；确认受控端口free；恢复Docker Desktop为stopped；四个named volumes按已接受非破坏边界保留，不执行volume删除或prune。
- default/security：没有Desktop/Host/Runtime业务状态；没有Public Task/conversation；没有Keychain/MiniMax/真实数据；生成secret在日志/证据中0命中；默认flag仍off。
- recovery gate：仅Owner接受DEC-126-058并另行批准corrective后，才可修改private local profile；corrective Closure与新的fresh E2E仍分别单审。

### S10B-R6 abort/restore记录

- run：`28afba8b-573a-46ec-b9d1-8a635c7b9cf0`；授权已消费。
- stop trigger：唯一preflight在image resolver返回`preflight_image_resolver_failed`；S10B-001 FAIL，S10B-002–012 NOT RUN。
- safe diagnosis：三项冻结image只读identity/descriptor/repository/platform匹配；未重跑no-start create probe，父runner未保存子leaf class，因此根因不猜测。
- restore：没有run-labeledcontainer/network/volume；七个固定端口无listener；Docker执行前后均running；不删除保留的owner-only ignored run root。
- evidence：run root 0700；`infra-secrets.env`与`REJECTED`为ignored 0600；REJECTED SHA-256=`7c7c5f61d03614f41dec86fd051bda8668bebf208ff53349fe5535ba5f765e11`；secret evidence hits=0。
- recovery gate：DEC-126-060/061 Option A已Accepted，LIA-126-023 repository corrective与S10BEP1-014 isolated live验证已PASS；DEC-126-062已接受Corrective Closure并关闭BLK-007，DEC-126-063已形成本地clean checkpoints。当前仍不得直接重跑或进入S11；fresh R7仍须另行授权。

### BLK-007 corrective恢复边界

- 默认`make feat-126-s10-verify-images`/human CLI必须保持；新closed mode只能由同commit父preflight内部固定调用，不能成为operator override。
- new parent以namespace export guard识别old/invalid child并必须以closed protocol class停止；禁止回退到stderr scraping、generic PASS或自动重试。
- failure context按每个leaf的显式合法phase/target/cleanup tuple校验；validation后owned cleanup成功须保留原leaf与`removed`，opaque cleanup失败须归一化为cleanup leaf，不得折叠成generic protocol error。
- corrective回滚必须成组撤销parent/child；回滚后继续HOLD S10B。任何ignored resolver evidence均不被continuation消费，也不得含raw stderr、路径或image pin。
- timeout、cleanup incomplete/unknown或foreign identity时parent删除数量必须为0；资源处置只能沿S10BD1 exact ownership边界另行评审。
- closed PASS/evidence后必须按固定顺序重跑只读config guard，再以同源profile/services和`--pull never`直接启动；不得回退到会二次调用human resolver的公开`up`路径。
- 2026-08-09已在Docker client/server 29.6.1、Compose 5.3.0和daemon access通过后，使用canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`完成S10BEP1-014。exact closed parent、3 identity/3 no-start probe、0600五字段evidence、no-log、三项exact image identity前后一致、image count均为6及container/network/volume/listener归零均PASS；该动作不是S10B-R7，`s10b_r7_executed=false`。
- Infra 128/128、targeted 34/34、validate、完整`make lint/test`及Governance门禁PASS。证据SHA-256=`e13f633fb331e3b0c0d08f22e16f7126980555ae849a73766a7bcc2259be6b34`；S10BEP1-014当时未授权commit/push，未形成checkpoint。
- DEC-126-062已接受Corrective Closure并关闭`S10B-BLK-007`；DEC-126-063随后形成Infra checkpoint `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`与Governance本地checkpoint。continuation或fresh R7仍未授权；S11、MiniMax、activation、真实数据与远端动作继续禁止。

### S10B-R7 abort/restore记录

- authorization/run：LIA-126-024已消费；canonical run `d553e6ea-e10f-4470-b357-a41807d6fb06`，七仓fixed SHA、Docker client/server 29.6.1、Compose 5.3.0与daemon access均PASS。
- reached gate：唯一preflight PASS，S10B-001完成3 identity/3 no-start probe、fresh dependencies、TLS/OIDC、synthetic identity、migration/bootstrap、API/fake readiness与no-log。
- stop class：`S10B-002 full_process_orchestration_authority_missing`。唯一continuation只启动API，治理manifest不是executable authority；未调用continuation，未启动Host/Desktop/Runtime，不人工拼接、不修复、不续跑、不重试。
- cleanup：执行`make feat-126-s10-stop RUN_ID=d553e6ea-e10f-4470-b357-a41807d6fb06`；run container/network/process/listener=0；4 named volumes与owner-only ignored run root保留；daemon恢复6 containers/0 running/6 images；不prune、不删除volume。
- evidence/no-log：summary=`de994e3d…12b80`，resolver result=`c424a4e8…177e9e`；8个允许文件对5个生成secret和664个冻结payload值均0命中，bearer/DSN/private-key=0，continuation log absent。
- governance：feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS。
- state：S10B-001 PASS；002 FAIL-CLOSED；003–011 NOT RUN；012 abort subset PASS/overall NOT RUN；`s10b_r7_executed=true`；DEC-126-064 Option A Accepted；`S10B-BLK-008 Open`。
- recovery gate：不得复用R7。DESIGN-126-014与S10BO1 repository corrective均已完成，全量门禁PASS并提交Owner Corrective Closure Review；isolated live、fresh R8与S11仍各自需要新的明确授权。

### BLK-008 orchestrator实现与恢复边界

- `DESIGN-126-014 Complete`冻结实现边界；`LIA-126-025/S10BO1`已完成repository implementation，但不是可执行live runbook，也不授权启动任何组件。
- 未来唯一入口必须只收canonical run ID和七仓full SHA，内部消费same-run preflight，并保持Infra→Desktop→Host→Runtime所有权；禁止Infra直接启动Host/Runtime或人工拼接API-only continuation。
- existing run ID只允许精确reconcile cleanup，永不允许continue/resume/retry；planned Desktop restart只能是同一live orchestrator内的显式状态转换。
- repository corrective限定Infra/API/Host/Desktop且已按此实现；Contracts/Runtime源码、public wire、durable schema、Compose pin与默认flags保持不变。若后续发现这些影响，立即停止并重新进行contract-impact/G2A评审。
- 最终能力前置PASS：Docker client/server `29.6.1`、Compose `5.3.0`、daemon、loopback、0700/0600临时文件、subprocess、native bookmark及SQLCipher/file-security测试均可用。
- API/Host完整lint/race/build PASS；Desktop 30个TS文件/167 tests、Rust 129 PASS/3 ignored、production/default/feature build与clippy、driver 2/2及production driver-absent PASS；Infra validate、完整lint/test、Compose semantic、142/142与S10BO1-001–014 14/14 PASS。
- Desktop两个仅driver消费的方法缺少同源feature cfg，按单独授权增加`#[cfg(feature = "feat126-s10-driver")]`后default/feature全套回归PASS；该最小修复`contract-impact=none`。
- `DEC-126-067 Accepted / S10BO1 Local Clean Checkpoints Formed / S10B-BLK-008 Closed`。本轮已形成五个明确授权的本地checkpoint；isolated live、fresh R8、额外commit和远端动作仍为Not Authorized。

## 12. LIA-126-025 / S10BO1 Release Boundary

- Owner已接受S10BO1 Corrective Closure；本决定不授权clean checkpoint、live或fresh run，后续任何动作须另行明确授权。
- Governance default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与所有受影响仓库`git diff --check`最终复跑PASS；该PASS不扩大live、commit或release授权。
- 不得把repository Corrective Closure Passed写成G4或fresh四组件E2E PASS；完整S10B-001–012仍须单独授权的新run证明。
- 回滚按仓撤销Infra orchestrator、API verifier、Host evidence/fake support和Desktop test driver；现有default-off路径与既有业务wire保持可用。不得prune、删除named volumes或修改foreign resources。
- DEC-126-066接受Corrective Closure后，决策后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`均PASS；isolated live与fresh R8仍需新的Owner一次性授权；S11/G6、MiniMax、真实数据/Keychain和默认功能启用继续受原审批边界约束。

## 13. DEC-126-067 Local Checkpoint Manifest

- API=`451940b282d8dd3e232ed414bd44b0677897f4c4`；Host=`c5939b4d8b5ebc318a7beeb49b20f343802e59b9`；Desktop=`d51e435cb8ea224e69f9707831ee71022d0a7b6e`；Infra=`0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c`。
- Governance为包含DEC-126-067、上述精确SHA与post-update Governance PASS证据的本地commit；Contracts=`29317b6426578749dc698fc2ad32b986ee5c8e9f`、Runtime=`3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`保持clean/unchanged。
- 所有checkpoint均local/not pushed；不得将其视为isolated live、fresh R8、完整S10B-001–012、G4或G6证据。
- 后续若授权isolated live或fresh R8，必须使用新的canonical run ID和这组clean exact SHAs；本节本身不授权启动、重试、prune、volume删除或任何远端动作。

## 14. S10BO2 Candidate Publication Boundary

- S10BO2 repository candidates为Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`与Infra `0fed8187d6051c011e67142d90feff89de326cfe`；Contracts/API/Host/Runtime本轮源码不变。
- Owner本轮明确授权将Governance、API、Host、Desktop与Infra的现有FEAT-126提交推送到对应候选分支；这是source candidate availability，不是merge、tag、publish、deploy或默认功能启用。
- 回滚必须分别撤销Desktop feature-only bootstrap/control channel与Infra startup/abort runner；不得只删除hard stop、手工拼接组件、让Infra直接启动Host/Runtime或弱化strict termination identity。
- Owner已接受S10BO2 Corrective Closure并关闭`S10B-BLK-009`；该决定不构成live/release授权。isolated live和fresh R8仍需各自的新Owner授权与new canonical run ID；本轮`s10b_r8_executed=false`，没有live资源可回滚。
- Owner决定登记后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`首轮及最终证据回填后复跑均PASS。没有commit、push、merge、tag、publish或deploy。

## 15. Failed Isolated Live Containment

- LIA-126-027已消费且Closure FAIL；run `b68804f0-aaf9-4da4-95e1-aa3b605bfada`不得重试或复用。
- 失败发生在run root建立前；无候选run资源可通过existing-run reconcile验证。不得通过创建伪process evidence、手工kill、直接调用preflight或删除hard stop恢复。
- 观测到project container/network/volume=0、fixed listener=0及daemon基线恢复；因身份/no-log证据缺失，rollback状态保持fail closed而非PASS。
- `S10B-BLK-010 Closed`：LIA-126-028/S10BO3 Corrective Closure已由Owner接受；这不授权再次isolated live或fresh R8，后续仍需新的clean checkpoint和单独Owner授权。
- Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check`首轮及本条回写后的最终复跑均PASS。本轮无commit、push或远端写入。

## 16. S10BO3 Corrective Rollback Boundary

- Corrective只改变Infra private local test/deployment scripts与tests；central contracts、API/Host/Desktop/Runtime、Compose pins、named volumes和default flags未改变。
- 回滚必须整体撤销七SHA Make authority、attempt ledger、failure/closure projection、scope-aware cleanup/no-log及S10BO3 tests，不能只删除attempt claim、放宽strict parser或恢复cleanup覆盖primary的旧行为。
- 失败run ID永久不可复用；回滚或corrective review都不授权手工拼接组件、manual kill、resume或业务case。
- 当前repository corrective Closure已由Owner接受；`S10B-BLK-010 Closed`。在新的clean checkpoint和单独Owner授权前不得授权下一次isolated live。
- 本轮没有Docker live、prune、volume删除、commit、push、merge、tag、publish或deploy；没有运行态资源需要回滚。

## 17. DEC-126-070 Local Checkpoint Boundary

- Infra local clean checkpoint=`91f7ec03372b1528abb93818abfad432a83327c4`；仅包含五个S10BO3 corrective文件，worktree clean，未push。
- Governance local checkpoint为包含本节与Infra精确SHA的单一commit；精确SHA只能在commit形成后报告，不能写入commit自身。
- Contracts/API/Host/Desktop/Runtime保持既定clean checkpoint；本次没有部署、发布、默认启用或运行态配置变化。
- 如需撤销，只能按仓撤销上述local commits；不得prune、删除named volumes或影响foreign resources。
- `s10b_r8_executed=false`、G3 Partial、G4/G6 Pending保持；本checkpoint不授权isolated live、fresh R8、业务case、push或其他远端动作。

## 18. Second Failed Isolated-Live Containment

- LIA-126-029已消费；run `8b94dc6d-5984-4579-9e0c-bed43a4b872f`在attempt marker/preflight前以`orchestrator_process_identity_unknown`停止并永久不可复用。
- 不得用manual Node路径、直接script调用、手工preflight或复用run ID绕过canonical入口；不得创建补写的模拟ledger/no-log/cleanup evidence。
- 外部观测container/network/volume/listener为0，但正式cleanup/no-log保持NOT ESTABLISHED；Public Tasks/conversation/turn/provider均为0，`s10b_r8_executed=false`。

## 19. Absolute Node / Preclaim Corrective Rollback Boundary

- Corrective同时包含绝对Node入口与preclaim-before-identity，二者共同关闭BLK-011；不得只回滚其中一个、恢复相对`node`或把claim重新移到identity之后。
- preclaim与preclaim-failure为run single-use authority。删除、覆盖或忽略这些文件不能恢复run；failed/incomplete preclaim只能保持fail closed。
- Legacy marker-only reconcile兼容必须保留；central contracts、Runtime/Compose pins、default flags与named volumes不受本corrective影响。

## 20. DEC-126-072 Checkpoint Boundary

- Infra checkpoint=`c7edbc344daecb84553efafe86dfe335a5c0c72d`；Governance checkpoint为包含该SHA和本节的本地commit；均未push。
- 如需撤销，只能按仓对这两个local commit执行独立、可审查的revert；不得prune、删除named volumes或影响foreign resources。
- 在获得新Governance SHA和另一份isolated-live明确授权前，不得运行`make feat-126-s10b-orchestrator`。fresh R8、业务case、S11、MiniMax和远端动作仍禁止。
