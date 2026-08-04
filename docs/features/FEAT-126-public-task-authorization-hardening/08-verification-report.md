# FEAT-126 验证证据与独立审查报告

> LIA-126-002第二轮独立审查曾把S4–S6从Complete调整为`Conditional / Corrective Closure Required`。
> DEC-126-025现已完成Remote State Reconciliation：sole candidate与yijie/API/Host/Desktop checkpoint
> 分支均已精确远端可达，旧Draft PR #1与各`origin/develop`不变。DEC-126-026已接受S4–S6
> Foundation Corrective Closure并单独授权S7A Desktop Rust Host Bridge/Domain；DEC-126-027已由
> Owner接受。随后单独授权的S7B Rust Application Orchestration/Domain已完成并由Owner通过DEC-126-028接受；远端可达不等于merge、发布或生产启用。
> 随后Owner接受DESIGN-126-005/006和S7C–S9 Closure。DESIGN-126-007/DEC-126-037方案C、DESIGN-126-008/DEC-126-038方案B、S10E/DEC-126-039、S10P1/DEC-126-040及DEC-126-041 Option B现均已接受；BLK-001/002/003关闭。DEC-126-041只接受S10P2源码checkpoint并保持Closure HOLD；原生Protected Data证明仍因缺Apple Development identity/provisioning而阻断，BLK-004保持Open。S10B继续HOLD，LIA-126-008保持Blocked Draft。没有调用MiniMax、真实数据、生产环境或业务四组件；S10P3/S10B–S11仍未授权。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | `feat/feat-126-foundation-closure` | LIA-126-009 fixed governance baseline `6f76a5b8f7e50d995c04323d03bd2733f2fe7f91`；本轮governance checkpoint在最终门禁后回报 | 开始时clean；仅FEAT-126 package diff；0 FEAT-123/unrelated；不push | zsh/macOS；feature package checker | 2026-08-04 Asia/Shanghai |
| yijie-infra | `feat/feat-126-s10e` | `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf`；parent `f040492e7c4af4aa7cc94a343140c58befae3af2` | clean；16-file local checkpoint；not pushed | Docker 29.6.1；Compose 5.3.0；Node 26/pnpm 11 | 2026-08-04 Asia/Shanghai |
| yijie-api | `feat/feat-126-foundation-closure` | local/remote exact `a64f9f591fb594818c1778e30c6941e2574b3264` | clean after 16-file Accepted checkpoint；candidate branch exact | Go 1.26.5 + isolated PostgreSQL | 2026-08-03 |
| yijie-agent-host | `feat/feat-126-foundation-closure` | S10P1 local checkpoint `e0a8d3d29a335571d1654d95e1e262c240755674`；parent S9 `8707dea552cff74121b89aa8045f27da2c8c9378` | clean；15-file S10P1 private test profile/fake authority/watchdog diff；not pushed | Go 1.26.5 + deterministic fake Responses + fixed Runtime | 2026-08-04 |
| yijie-desktop | `feat/feat-126-foundation-closure` | S10P2 local checkpoint `c863b2ab30d185201bff5736a308d7078ee5dc68`；parent S10P1 `fba934c524852719904657d0a4155142040e7285` | clean；8-file Rust/example private storage diff；not pushed | Node 26/pnpm 11/Rust 1.95/Protected Data probe | 2026-08-04 |
| yijie-contracts | `feat/feat-126-content-free-candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` local/remote exact | clean；unchanged during review | locked generators | 2026-08-03 |
| yijie-codex | `develop` | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | clean；unchanged | Runtime 0.144.6；binary `1ef4f1…8df1fe`；manifest `2560a3‧6682` | 2026-08-04 |

## 2. Baseline

| ID | CWD | Command | Exit code | Result | 摘要/日志位置 | 历史失败 |
|---|---|---|---:|---|---|---|
| BASE-DOC-001 | yijie | `check-feature-package.sh <feature-dir>` + `--strict` | 0 | PASS | structure present; template/incomplete markers absent; script note retained | none known |
| BASE-DOC-002 | yijie | Ruby `YAML.safe_load` on `feature.yaml` | 0 | PASS | root parsed as mapping | none known |
| BASE-DOC-003 | yijie | per-file `git diff --no-index --check /dev/null <new-file>` with expected new-file code normalized | 0 | PASS | no whitespace/conflict diagnostics | four EOF blank lines found once and fixed before PASS |
| BASE-APP-001 | API/Host/Desktop | repository gates on LIA-126-001 foundations | 0 final | HISTORICAL PASS / insufficient for closure | exact commands in §4 | green tests did not cover the P1 branches found by LIA-126-002；cannot support Complete status |
| BASE-CTR-001 | yijie-contracts | initial narrow source tests + validation | 0 | PASS | FEAT-126 local source shape established | initial TypeScript wildcard collision and v1 shared-error enum warnings found, fixed, then full gates rerun |

## 3. Requirements-package 证据

| Scope | Head SHA | Command/inspection | Exit code | Result | Diff/证据 |
|---|---|---|---:|---|---|
| Requirements investigation/G1 | yijie baseline + uncommitted docs | source requirements + screenshots + code/ADR scan + 段成威明确批准 | 0 for read commands | PASS as requirements evidence | `00`–`07`; G1/G2 Passed，G2A current |
| G2 storage authority | yijie baseline + uncommitted ADR-0013 | storage-role source scan + 段成威明确同意推荐方案 | 0 for read commands | PASS as decision evidence | ADR-0013/DEC-126-005/014 Accepted；G2 Passed；其后 S4–S6 foundation 已按 LIA-126-001 实现 |
| G2 SQLite/delete boundary | uncommitted ADR-0014 + isolated temp environments | official dependency/SQLite/SQLCipher/Apple review + Rust build + fixed Runtime delete/restart/residue scan + 段成威明确批准 | 0 for selected build/delete harness | PASS as accepted design evidence with recorded limitation | ADR-0014/DEC-126-006 Accepted，Q-006/Q-015 Resolved；not implementation/G2 pass |
| G2 Runtime title/raw-reasoning capability | Accepted ADR-0015/0016/DEC-126-016/017 + exact Runtime SHA | canonical schema/source + prior 5 fake fixtures + raw delta/history/interleaving/interruption fixed fixtures 4/4 + historical `MM-126-001/002` harness | 0 for local fixtures；2 historical external calls；本轮0 provider calls | fixed raw primitives PASS / title PASS / historical public-summary FAIL / raw observed | DESIGN-126-003 accepted；不证明Host/Desktop实现、raw跨输入稳定性或生产安全 |
| G2 Public Tasks investigation | exact sibling SHAs in `feature.yaml` | Public OpenAPI/API/Infra/Desktop/Host/admin/connectors/knowledge/skills source scan | 0 for read commands | COMPLETE for repo-local inventory | Q-010 Resolved；unknown external保留为safe compatibility category；DEC-126-011/012 Accepted |
| G2 Chat/App Shell Pattern | yijie-desktop baseline + Accepted docs-only FEAT-126 Pattern | current Accepted Pattern comparison + docs build | 0 | PASS as approved design evidence | 只取代FEAT-126冲突段落；无业务source |
| G2A source contract candidate | `yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f` | DEC-126-023 content-free replacement + post-commit source/fixture/generated/breaking/equality/digest review + DEC-126-024 Owner approval | 0 | PASS / APPROVED | parent=`c000a024`；new sole candidate；old candidate/PR/remote unchanged；not implementation authorization |
| LIA-126-002 corrective closure | API `a64f9f5…3264`、Host `3e8df02…f3d9`、Desktop ancestor `3adcb03…455a` | exact `29317b...` locks, repository gates, isolated PostgreSQL, fixed Runtime, migration/security/no-log evidence and structured review | 0 final | CLOSURE PASS / OWNER ACCEPTED / REMOTE CANDIDATES VERIFIED | listed S4–S6 P1 closed；DEC-126-026 Accepted；flags/routes default off；later Owner-authorized checkpoint push不改变Closure语义 |
| S7A Desktop Rust Host Bridge/Domain | Desktop `3adcb0380561c294412bc24767e4651ca872455a` | exact loopback/bearer/nonce/v2 SSE/domain implementation + fake Host/canonical fixture/full repo gates | 0 final | CLOSURE PASS / OWNER ACCEPTED / CHECKPOINTED LOCAL | no Vue surface, no flag/MiniMax/remote action；DEC-126-027 Accepted；G3 Partial |
| S7B Desktop Rust Application Orchestration/Domain | Desktop `3adcb0380561c294412bc24767e4651ca872455a` | durable outbox、strict/coalesced reducer、batched history、title CAS、migration/fault/fake Host application integration | 0 final | CLOSURE PASS / OWNER ACCEPTED / CHECKPOINTED LOCAL | no Vue surface, no flag/MiniMax/remote action；DEC-126-028 Accepted；G3 Partial |
| DESIGN-126-005 Desktop IPC/ViewModel Review | no implementation SHA | read-only ConversationApplication/Tauri/TS gap inventory + private IPC commands/events/cursor/error/security/recovery contract + S7C/S8A/S8B plan | 0 for read/docs checks | DESIGN ACCEPTED / DEC-126-029 ACCEPTED | S7C/S8A later separately authorized；G3 Partial |
| LIA-126-003 / S7C Desktop Rust Actions/Coordinator | Desktop `3adcb0380561c294412bc24767e4651ca872455a` | auth context/facade、session/project actions、interrupt、SQLCipher v4 cleanup/receipt、background coordinator、restart/resync/live raw source + fake Host/migration/race/no-log/full gates | 0 final | CLOSURE PASS / DEC-126-030 OWNER ACCEPTED / CHECKPOINTED LOCAL | no Vue、flag/MiniMax/pin/remote action；G3 Partial |
| LIA-126-004 / S8A Desktop IPC/ViewModel | Desktop `3adcb0380561c294412bc24767e4651ca872455a` | 20 private commands、closed schema/fixtures、Rust native auth/event/cursor、strict TS validators、real Tauri client、authoritative Pinia reducer + auth/caps/backpressure/stale/restart/no-log/full gates | 0 final | DEC-126-031 ACCEPTED / S8A CLOSURE PASS / CHECKPOINTED LOCAL | 127 TS + 93/94 Rust；no Vue/flag/MiniMax/central pin/remote action；G3 Partial |
| DESIGN-126-006 / DEC-126-032 | yijie approval checkpoint `804b62a` | read-only Desktop router/nav/permission/store/IPC/pages/env/CI inventory + closed design/stop condition | 0 for read/docs checks | DESIGN ACCEPTED / DEC-126-032 ACCEPTED | Owner随后以LIA-126-005单独授权S8B0；不自动授权S8B；G3 Partial |
| LIA-126-005 / S8B0 | Desktop `5dab02a1ad5f03fead236aa7060fa6a75a234d85` | exact-off gate、guarded route/lazy loader、permission lifecycle、project/session/cleanup store consumption、Rust-owned readiness/recovery/storage projection、真实Tasks metadata接线 | 0 final | DEC-126-033 ACCEPTED / CLOSURE PASS | 135 TS、95/96 Rust（1既有ignored）及lint/build/fmt/clippy通过；full Chat Vue page/visual、flag activation、MiniMax与远端动作均未发生；G3 Partial |
| LIA-126-006 / S8B | Desktop `35f27447398529cca4dec85fa1f67e779c7a7cbd` | production Vue pages/App Shell/composer/reasoning/menus/scroll/a11y + real Pinia reducer + test-only harness | 0 final | DEC-126-034 ACCEPTED / S8B CLOSURE PASS | 29 TS test files/164 tests、axe 0 serious/critical、build、95/96 Rust、audit/security/bundle/browser证据；flag off；no IPC/Rust/central wire/MiniMax/remote action；G3 Partial |
| DEC-126-035 Remote State Reconciliation | five exact candidate refs | `git ls-remote` + temporary single-branch/no-tags clean clones；HEAD/status/develop refs核对 | 0 | PASS / OWNER ACCEPTED | exact `650254b…139fa`、`a64f9f5…3264`、`3e8df02…f3d9`、`35f2744…7cbd`、`29317b6…e9f`；Owner-authorized historical push；reconciliation轮0 remote write |
| DESIGN-126-007 / S10A | six fixed baselines + local tool/source/port inventory | branch/SHA/worktree exact；Runtime digest/version；Docker/Compose/PostgreSQL/listener；Host provider；Desktop sidecar/Keychain/Public Tasks consumer scan | 0 for read-only commands | REVIEW ACCEPTED / S10B HOLD | BLK-001–005详见§9.12；DEC-126-037 Option C Accepted；无process/flag/provider/Keychain/business-source mutation |
| DESIGN-126-008 / S10P0 | six fixed baselines + Infra/Host/Desktop/contracts read-only inventory | Compose stale-link/root cause and bundled v5 hash/config；pinned image/volume choice；fake child profile；run-derived secure storage；Public Tasks idempotency/delete/private IPC shape | 0 for read-only commands | OWNER ACCEPTED / IMPLEMENTATION HOLD | DEC-126-038 Option B Accepted；0 process/container/flag/provider/Keychain/DB/business-source/remote writes |
| S10E / DEC-126-039 | Infra parent `f040492…af2` + fixed API `a64f9f…3264` + local Docker/Compose/image content | recoverable plugin discovery；default-off exact-digest profile；synthetic identity/TLS；migration v4；runtime/no-secret-log/rejected-run；stop/retained-resource inventory | 0 | CLOSURE PASS / OWNER ACCEPTED | Infra `99e50d8…6baf` local/clean/not pushed；BLK-001 closed；not S10P1/S10B evidence |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh docs/features/FEAT-126-public-task-authorization-hardening` | project shell script | 0 | PASS | structure/templates only; not Gate approval |
| V-STRICT | yijie | same checker with `--strict` | project shell script | 0 | PASS | lexical completeness only; Open/NOT RUN remain intentional |
| V-G0 | yijie | same checker with `--gate G0` | project shell script | 0 | PASS | G0 document scope only; human Gate recorded separately |
| V-G1 | yijie | same checker with `--gate G1` | project shell script | 0 | PASS | G1 document scope has no incomplete markers；human approval recorded in `feature.yaml`/`01`/`03` |
| V-G2 | yijie | same checker with `--gate G2` | project shell script | 0 | PASS | G2文档结构与Owner Passed状态一致；不代表G2A/业务实现 |
| V-G2A | yijie | same checker with `--gate G2A` | project shell script | 0 | STRUCTURE PASS / HUMAN APPROVAL RECORDED | checker proves lexical completeness；DEC-126-024 Owner approval separately recorded，G2A Re-review Passed |
| V-LOCAL-STRATEGY | yijie FEAT-126 package | package + strict + G2A checker、YAML parse、`pnpm lint/test`、diff check，cross-document review including DEC-126-023–034 | docs + accepted closure | 0 | PASS 2026-08-03 after final rerun | package/default/strict/G2A、YAML、governance lint/test PASS；G2A与S4–S8B Closure Passed；DEC-126-034 Accepted；G3 Partial |
| V-S8A-DESKTOP | yijie-desktop | `cargo fmt && make lint && make test && make build` | Node 26.0.0 / pnpm 11.9.0 / Rust 1.95.0；SQLCipher；fake Host | 0 | PASS 2026-08-03 | generate exact `29317b...`；21 TS files/127 tests；94 Rust（93 pass/1 existing ignored）；fmt/clippy `-D warnings`/Vite build PASS；schema/serde/TS、auth/events/cancel/stale/restart/no-log覆盖 |
| V-S8B0-DESKTOP | yijie-desktop `5dab02a1ad5f03fead236aa7060fa6a75a234d85` | `pnpm lint && pnpm test && pnpm build`；`cargo fmt --check`；`cargo clippy --all-targets -- -D warnings`；`cargo test` | Node 26 / pnpm 11 / Rust 1.95 / bundled SQLCipher；fake/fixed/temp only | 0 | PASS 2026-08-03 | 22 TS files/135 tests；96 Rust（95 pass/1 existing Keychain ignored）；22 closed commands/7 unchanged events；gate/route/lifecycle/readiness/storage/paging/delete/Tasks/no-log覆盖；0 MiniMax/flag activation/remote action |
| V-S8B-DESKTOP | yijie-desktop `35f27447398529cca4dec85fa1f67e779c7a7cbd` | `pnpm lint`；`pnpm test`；`pnpm build`；unchanged `cargo test`；`pnpm audit --audit-level high`；browser/security/bundle/diff checks | Node 26 / pnpm 11 / Rust 1.95 / bundled SQLCipher；fake/fixed/temp only | 0 final | PASS 2026-08-03 | 29 TS test files/164 tests；axe 0 serious/critical；4625 build modules；95 Rust pass/1 existing ignored；audit 0；light/dark/1180×760/200%-equivalent/focus/plaintext PASS |
| V-S9-HOST | yijie-agent-host `8707dea552cff74121b89aa8045f27da2c8c9378` | `make feat126-eval`；`make lint`；`make test`；`go build ./...`；security/diff/hash checks | Go 1.26.5；deterministic fake provider | 0 | PASS 2026-08-04 | 250 cases；title 250/250 + semantic 200/200 + unsafe 50/50；raw 210/210 + negative 40/40；session coverage 77.8%；body leak=0 |
| V-S9-DESKTOP | yijie-desktop `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb` | targeted Rust/TS fixture tests；`pnpm lint/test/build`；`cargo fmt --check`；`cargo clippy --all-targets -- -D warnings`；`cargo test --all-targets`；`cargo build --all-targets`；bundle/security/diff checks | Node 26 / pnpm 11 / Rust 1.95 / SQLCipher | 0 final | PASS 2026-08-04 | 30 TS files/165 tests；Rust final rerun 96 pass/0 fail/1 existing ignored；exact Host fixture hash、restart/history/delete/title/plaintext PASS；production bundle canary=0 |
| V-S9-FLAKY-AUDIT | yijie-desktop unchanged `application.rs` test | first full Rust run → isolated rerun → second full rerun | same source/environment | 1 then 0/0 | CLASSIFIED NON-S9 TIMING FLAKE | first run only: existing cleanup test reused pre-bind `now` across a second boundary and saw no outbox；targeted rerun and second full run PASS；file absent from S9 diff，no waiver or product-code change |
| V-S10A-BASELINES | six repositories | `git rev-parse --abbrev-ref HEAD` + `git rev-parse HEAD` + `git status --short` + remote/config read | Git | 0 | PASS | all six exact fixed SHAs/branches and clean worktrees at start；no checkout/reset/pull/fetch/push |
| V-S10A-RUNTIME | yijie-codex artifact | manifest read + `shasum -a 256` + `codex --version` | codex-cli 0.144.6 | 0 | PASS READ-ONLY | artifact/manifest digest exact；app-server not started；no model/provider call |
| V-S10A-ENV | local machine | `docker --version`; `docker compose version`; `command -v psql/pg_isready/lsof`; fixed-port listener scan | Docker 29.6.1 | Compose command non-zero expected | ENVIRONMENT BLOCKED | S10A当时仅观察到`docker compose`不可用；S10P0后来定位为用户plugin symlink失效且bundled v5存在；psql/pg_isready present；no observed service listeners；no install/container/service action |
| V-S10A-SOURCE | API/Host/Desktop read-only | exact config/start/sidecar/keychain/provider/Public Tasks consumer source inventory | rg/sed | 0 | HOLD FINDINGS | fake provider unrepresentable；child flags forced false/log null；fixed Keychain；Desktop `/v2/tasks` call absent |
| V-S10A-GOV | yijie | feature package default/`--strict`/`--gate G2A`；Node YAML parse；`pnpm lint`；`pnpm test`；shell `bash -n`；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | DESIGN-126-007与DEC-126-037 Option C Accepted；LIA-126-008仍为Blocked Draft；不代表S10B已执行 |
| V-S10P0-GOV | yijie | feature package default/`--strict`/`--gate G2A`；Node YAML parse；`pnpm lint`；`pnpm test`；shell `bash -n`；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | design checkpoint `514559265ac4a675115984650a0782f09b481748`形成DESIGN-126-008/DEC-126-038候选；该轮不代表Owner批准或任何corrective执行 |
| V-DEC-126-038-APPROVAL | yijie | Owner approval state reconciliation；feature package default/`--strict`/`--gate G2A`；YAML；`pnpm lint/test`；shell；diff/personal-path scan | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | DEC-126-038 Option B与retained-Public-row边界已登记为Accepted；S10E/P1/P2/P3/S10B仍NOT AUTHORIZED/NOT RUN；0 business/runtime/remote mutation |
| V-YAML | yijie | Node ESM + `yaml` parse | Node/pnpm workspace dependency | 0 | PASS | `PASS: feature.yaml parsed` |
| V-YIJIE-LOCAL | yijie | `pnpm lint && pnpm test` | Node/pnpm project scripts | 0 | PASS 2026-08-03 | repository manifest/contract governance valid；1/1 Node test PASS |
| V-AGGREGATE-LINT-TEST | yijie | historical `make lint` and `make test` after package/strict/G2A/YAML | workspace aggregate scripts | 2 | HISTORICAL ENVIRONMENT BLOCKED | historical run stopped at stale Compose discovery after Infra static 76 tests；S10E has now repaired discovery and Infra static suite is 80/80, but no new workspace aggregate/four-component E2E green is claimed |
| V-S10E-INFRA-STATIC | yijie-infra | `pnpm validate`; `pnpm test`; `bash -n scripts/*.sh`; `git diff --check` | Node 26 / pnpm 11 | 0 | PASS 2026-08-04 | 80/80；default-off/exact images/ports/resources/secrets/failure cases；FEAT-125 regression included |
| V-S10E-RUNTIME | isolated local Docker project | `make feat-126-s10-up/export-ca/provision-users/api-migrate/verify-runtime/stop` under fresh run | Docker 29.6.1 / Compose 5.3.0 / API exact SHA | 0 | PASS 2026-08-04 | 4 services healthy；identity 2+2 idempotent；migration v4 + no-op；TLS/OIDC/Tasks 404；generated secret log hits 0；stop active resources 0 |
| V-S10E-CLEANUP | two exact S10E projects | container/network/listener inventory plus volume count | Docker/lsof | 0 | PASS WITH DISCLOSED RETENTION | 0 containers/networks/listeners；8 named volumes + 2 owner-only ignored run roots retained because deletion was not authorized |
| V-S10E-AGG-LINT | workspace | `make lint` across repository manifest | repository toolchains + Compose 5.3.0 | 0 | PASS 2026-08-04 | all 10 repos reached and passed；Infra Compose semantic validation passed。首次sandbox run only因Go build cache读取被OS policy拒绝，沙箱外相同只读命令通过；不是产品豁免 |
| V-DEC-126-039-APPROVAL | yijie | Owner approval state reconciliation；feature package default/`--strict`/`--gate G2A`；YAML；`pnpm lint/test`；shell；diff/scope check | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | DEC-126-039 Option A与S10E Closure已登记为Accepted，仅关闭BLK-001；G3 Partial、LIA-126-008 HOLD及S10P1–S11/activation/remote禁令保持不变 |
| V-S10P1-HOST | yijie-agent-host `e0a8d3d29a335571d1654d95e1e262c240755674` | `make lint`；`make contract-check`；`make test`；`go build`；fake protocol/default config/parent-watchdog/security/diff checks | Go 1.26.5 | 0 | PASS 2026-08-04 | full race/coverage PASS；fake Responses 79.8%、codex 71.0%、app 68.9%、session 77.6%；exact profile、key conflict、nonloopback、parent exit、incomplete/error/oversize PASS |
| V-S10P1-RUNTIME | Host parent `8707dea…c9378` + S10P1 diff + Runtime `3aa317ce…5d6f` | opt-in `TestPinnedRuntimeFEAT126FakeResponses` with fixed binary/manifest and `127.0.0.1:18082` | fixed codex-cli 0.144.6 | 0 | PASS 2026-08-04 | assistant/raw delta+final、item/turn complete、thread delete；fake accepted=1/rejected=0；external/MiniMax call=0 |
| V-S10P1-DESKTOP | yijie-desktop `fba934c524852719904657d0a4155142040e7285` | `make lint`；`make test`；`make build`；`cargo build`；actual fixed Host child integration；security/diff checks | Node 26 / pnpm 11 / Rust 1.95 | 0 | PASS 2026-08-04 | TS 30/165；Rust 101 pass/1 existing ignored；env allowlist、pre-spawn evidence、PID/run/nonce、0700/0600/256KiB logs、crash/restart/stale/stop PASS |
| V-S10P1-SCOPE | Host/Desktop/yijie | per-repo status/diff/name scan；`.env`/CI/default config、IPC/TS/Vue/contracts/wire/schema/pin and no-log/bbolt/process evidence scan | Git/rg/tests | 0 | PASS 2026-08-04 | 0 MiniMax/external/Keychain/real-data/remote write；0 raw/secret/path/bearer/DB-key covered hits；default flags unchanged |
| V-S10P2-DESKTOP | yijie-desktop `c863b2ab30d185201bff5736a308d7078ee5dc68` | `make lint/test/build`；`cargo build --locked --all-targets`；targeted secure-storage tests；source/bundle/diff scans | Node 26 / pnpm 11 / Rust 1.95 | 0 | PASS 2026-08-04 | TS 30 files/165；Rust 113 pass/0 fail/2 signed probes ignored；12 S10P2 unit tests PASS；no dependency/schema/IPC/TS/Vue/default-config change |
| V-S10P2-NATIVE | random run-derived three exact tuples | sandbox-exempt explicit signed-bundle probe + exact inventory/cleanup | unsigned Rust test binary / macOS Protected Data | non-zero expected blocker | **BLOCKED** | pre/post three tuples absent；cleanupComplete=true；temp roots=0；first write failed `required entitlement isn't present`；codesigning identities=0；no default/legacy/foreign tuple touched |
| V-S10P2-SECURITY | Desktop source/artifacts | exact-gate/default namespace/manifest/no-log/path/secret/bundle/lockfile scans；RustSec offline；pnpm audit | Git/rg/cargo-audit/pnpm advisory | mixed | PASS for source boundary / dependency follow-up | new Rust logging/bundle secret hits=0；RustSec 0 unallowed/17 allowed；pnpm reports pre-existing dev-tool `brace-expansion 5.0.8` high (patched ≥5.0.9), no lockfile change in this slice |
| V-DIFF | yijie | per-new-file `git diff --no-index --check` loop + tracked `git diff --check` | Git | 0 | PASS | FEAT-126/ADR-0013/ADR-0014/ADR-0015/ADR-0016 additions and tracked diff have no whitespace/conflict diagnostics |
| V-DESKTOP-DOCS | yijie-desktop | `pnpm docs:build` | pnpm + VitePress 1.6.4 | 0 | PASS | FEAT-126 Pattern and SUMMARY rendered；no business source modified |
| V-ADR | yijie | `git diff --check -- docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md` | Git | 0 | PASS | only factual create/not-implemented linkage changed |
| V-SQLITE-DEPS | temporary Rust project | `cargo check --locked` with exact rusqlite/rusqlite_migration selection | Rust/Cargo 1.95.0 | 0 | PASS | `rusqlite 0.40.1` bundled-sqlcipher + `rusqlite_migration 2.6.0` resolves/builds；temp project removed |
| V-REFINERY-COMPAT | temporary Rust project | dependency resolution comparison | Cargo 1.95.0 | non-zero expected | PASS as rejection evidence | Refinery 0.9.2 rusqlite support ≤0.39 conflicts with rusqlite 0.40.1 `libsqlite3-sys` native `links`；not selected |
| V-RUNTIME-DELETE | temporary `CODEX_HOME` + workspace | start one synthetic thread → name canary → one `thread/delete` → same-process read → shutdown/restart read + DB/file/byte scan | fixed `codex-cli 0.144.6`, arm64, SHA-256 `1ef4f1…8df1fe` | 0 | PARTIAL by design boundary | functional/restart absence PASS；Runtime WAL/log byte residue FOUND；0 model turn/no provider creds/no MiniMax/no real data；temp home removed |
| V-RUNTIME-EPHEMERAL | yijie-codex/codex-rs | key-cleared `cargo test -p codex-app-server --test all thread_start_ephemeral_remains_pathless -- --nocapture` | Cargo / Runtime source `3aa317ce...` | 0 | PASS | 1 passed/687 filtered；ephemeral=true、path=null；local fixture only |
| V-RUNTIME-OUTPUT-SCHEMA | yijie-codex/codex-rs | key-cleared app-server tests `turn_start_accepts_output_schema_v2` and `turn_start_output_schema_is_per_turn_v2` | Cargo / Runtime source `3aa317ce...` | 0 each | PASS | each 1 passed/687 filtered；mock Responses request uses strict `text.format`；schema only first turn |
| V-RUNTIME-SUMMARY-REQUEST | yijie-codex/codex-rs | key-cleared `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all configured_reasoning_summary_is_sent -- --nocapture` | Cargo / Runtime source `3aa317ce...` | 0 | PASS | 1 passed/954 filtered；mock request contains concise summary |
| V-RUNTIME-SUMMARY-DELTA | yijie-codex/codex-rs | same key-cleared command for `reasoning_content_delta_has_item_metadata` | Cargo / Runtime source `3aa317ce...` | 0 final | PASS after environment retry | first run SIGABRT stack overflow；same source with 32MiB worker stack: 1 passed/954 filtered，delta item ID关联正确 |
| V-RUNTIME-RAW-DELTA | yijie-codex/codex-rs | key-cleared `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all reasoning_raw_content_delta_respects_flag -- --nocapture` | Cargo / Runtime source `3aa317ce...` | 0 | PASS | 1 passed/954 filtered；local mock Responses only；无MiniMax/source diff |
| V-RUNTIME-RAW-HISTORY | yijie-codex/codex-rs | `cargo test -p codex-app-server-protocol protocol::thread_history::tests::<test>` for raw history/interleaving/interruption exact fixtures | Cargo / Runtime source `3aa317ce...` | 0 each | PASS 3/3 | completed raw content、interleaved items与aborted/interrupted事实；fixed fixtures only |
| V-DESIGN-126-003 | yijie + Host/Desktop | exact v2/schema/caps/reconciliation/history/migration/delete consistency review | fixed Runtime + contract candidate + local closure diff | 0 | S4–S7B SLICE PASS | Host cleanup/title/lease、Desktop reasoning/history/migration/nonce、S7A transport/domain及S7B reducer/terminal/history findings closed；UI/full E2E remain NOT RUN |
| V-MINIMAX-TITLE | temporary `CODEX_HOME` + empty cwd | `MM-126-001` isolated title harness；exactly one `turn/start`；request/stream retry=0 | fixed `codex-cli 0.144.6` SHA-256 `1ef4f1…8df1fe` + Host `34e94acf…` config + MiniMax-M3 | 0 | PASS | 1 call；1,853 ms；terminal completed；strict JSON/sanitizer 18 grapheme；0 tool/rollout candidate/secret leak；5,232 tokens；cost absent；temp root removed |
| V-MINIMAX-SUMMARY | temporary `CODEX_HOME` + empty cwd | `MM-126-002` isolated high+concise harness；exactly one `turn/start`；request/stream retry=0 | same fixed Runtime/Host pin + MiniMax-M3 | 0 harness / frozen historical gate FAIL | FAIL under ADR-0015 historical gate | 1 call；9,256 ms；answer completed；0 public-summary event；7 raw delta + 1 raw completed content part；0 tool/secret leak；5,664 tokens；cost absent；temp root removed；不得事后改写为新raw Gate PASS |
| V-ADR-0016 | yijie | Owner product direction/lifecycle decision + document consistency review | no model/provider command | N/A | ACCEPTED DESIGN ONLY | raw reasoning必须以纯文本显示；缺失/无效阻断reasoning Gate；不进logs/telemetry/audit；DEC-126-016要求SQLCipher历史持久化和session级联删除；非实现证据 |
| V-CONTRACT-GENERATE | yijie-contracts | `make generate` | locked generators | 0 | PASS | 29 generated files current；v2 schema exported via namespace to preserve v1 TS root API |
| V-CONTRACT-LINT | yijie-contracts | `make lint` | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 0 | PASS | OpenAPI/AsyncAPI/JSON Schema/Buf/TS/Go vet |
| V-CONTRACT-TEST | yijie-contracts | `make test` | Node/Go above | 0 | PASS | Node 27/27 + Go packages；FEAT-126 narrow source tests 11/11 |
| V-CONTRACT-BUILD | yijie-contracts | `make build && pnpm pack:sdk` | package 0.3.0 candidate / `29317b6426578749dc698fc2ad32b986ee5c8e9f` | 0 | PASS | SDK tarball SHA-256 `21b17b50ee265e1ebbd7a5248880c7874c88def65c538f1216d0413e85fab082`；not published |
| V-CONTRACT-BREAKING | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | sole supported baseline | 0 | PASS | OpenAPI/Buf/AsyncAPI/JSON Schema无breaking；v2错误schema隔离后无v1 enum warnings |
| V-CONTRACT-LEGACY | yijie-contracts | parsed structural comparison against supported baseline | Node/YAML/Git | 0 | PASS | Public Tasks v1 2 paths + Agent Host v1 7 paths equality |
| V-CONTRACT-COMMIT | yijie-contracts | `git rev-parse HEAD && git rev-parse origin/feat/feat-126-content-free-candidate && git status --short --branch` | Git | 0 | PASS | local/remote HEAD=`29317b6426578749dc698fc2ad32b986ee5c8e9f`，parent=`c000a0245acb5c3f7ead5d2a877fb60c281c588c`，worktree clean |
| V-REMOTE-RECONCILIATION | yijie/contracts/API/Host/Desktop | `git ls-remote`核对candidate/develop refs；每仓临时`git clone --single-branch --no-tags --branch <candidate>`后核对`HEAD`与`status --porcelain` | Git | 0 | PASS 2026-08-03 / READ-ONLY | exact heads=`650254b…139fa`、`29317b6…e9f`、`a64f9f5…3264`、`3e8df02…f3d9`、`35f2744…7cbd`；五个clone均clean并已删除；develop=`6c23dc3…513b`/`9ec34ab…ebbb`/`faeb780…bf34`/`34e94ac…18e4`/`155854c…70b5`；Draft PR #1不变；本轮0 remote write |
| V-CONTRACT-CONTENT-FREE | yijie-contracts | Public Tasks v2 targeted AJV/schema/fixture tests + generated TS/Go review | fixed synthetic UUID fixtures | 0 | PASS | request/success/error仅closed discriminator/reference/code；prompt/message/raw/title/path/result/error-message canaries rejected；3/3 targeted、27/27 all Node、Go PASS |
| V-CONTRACT-DIGEST | yijie-contracts | SHA-256 of canonical sources/generated outputs + deterministic SDK repack | `shasum -a 256` | 0 | PASS | replacement完整摘要见`04-contract-change-plan.md`/`feature.yaml`；SDK post-commit重复打包均为`21b17b50ee265e1ebbd7a5248880c7874c88def65c538f1216d0413e85fab082` |
| V-CONTRACT-REMOTE | origin + temporary clean clone | push exact SHA to `refs/heads/feat/feat-126-contract-candidate`；`git ls-remote`；clean clone locked install + generate/diff/lint/test/build/breaking/pack/equality/digest | Git/pnpm/Go/locked generators | 0 | PASS | remote branch=`c000a024…588c`；`origin/develop`仍=`9ec34abd…ebbb`；29 generated current、Node 27/27、Go PASS、v1 2+7 equality、九项摘要一致、clone clean；无merge/tag/发布/pin/编码 |
| V-CONTRACT-PR | GitHub PR #1 | create Draft PR with base `develop`, head `feat/feat-126-contract-candidate`; verify draft/state/base/head/OID/commit count/files and backfill CI result | GitHub/`gh` | 0 | PASS | [Draft PR #1](https://github.com/36Dge/yijie-contracts/pull/1) OPEN/DRAFT；head=`c000a0245acb5c3f7ead5d2a877fb60c281c588c`；1 commit、39 files；完整9项摘要与授权边界已登记；无candidate mutation或push |
| V-CONTRACT-CI | GitHub Actions | observe [run 30741466028](https://github.com/36Dge/yijie-contracts/actions/runs/30741466028) / [job 91479562558](https://github.com/36Dge/yijie-contracts/actions/runs/30741466028/job/91479562558) to terminal; read failure logs only | CI on exact PR head | 1 | FAIL / MERGE BLOCKED | PASS至checkout、locked install、Go modules、generate、generated diff、lint、test、SDK pack；`pnpm audit --audit-level high`发现`brace-expansion 2.1.2`高危GHSA-mh99-v99m-4gvg（patched `>=2.1.3`）；后续`govulncheck`与`./scripts/check-breaking.sh origin/main` SKIPPED；未rerun/waive/fix/push |
| V-CONTRACT-DEPENDENCY-ATTRIBUTION | yijie-contracts | `git diff --exit-code 9ec34abd... c000a024... -- package.json pnpm-lock.yaml` + `pnpm why brace-expansion` | Git/pnpm lock graph | 0 | PASS attribution | candidate未修改manifest/lockfile；锁定链为`openapi-typescript@7.13.0 -> @redocly/openapi-core@1.34.17 -> minimatch@5.1.9 -> brace-expansion@2.1.2`。这是既有工具链dependency baseline blocker，不是FEAT-126契约diff新增依赖；仍不能绕过红色CI |
| V-WORKTREE | yijie/contracts/API/Host/Desktop | status/name-only/untracked/diff-check + FEAT-123/sensitive-path scan before checkpoints；current status + remote provenance复核 | Git | 0 | PASS scoped to Accepted FEAT-126 | contracts unchanged/clean；Accepted checkpoints只含manifest §8.1范围；no FEAT-123/unrelated；Owner-authorized candidate push已发生并精确复验；本轮0 push，始终0 merge/tag/publish/deploy/activation |
| V-GENERATE | API/Host/Desktop | exact candidate lock + read-only generate/check scripts | oapi-codegen 2.7.2 / openapi-typescript 7.13.0 | 0 | PASS | API Go `438b084d…ab33`；Host Go `629ddf20…63b0`；Desktop TS `e84b70be…b678`；all locks resolve `29317b...`；API generate-check uses temp output + byte comparison |
| V-API | yijie-api | `make generate-check && make test && make lint`；fresh trust-only loopback PostgreSQL on 127.0.0.1:55432执行`make migrate-up/status`与`make test-integration` | Go 1.26.5 / race / synthetic local PostgreSQL | 0 final | PASS 2026-08-03 | migration 1–4 applied；publicapi 72.5%、PostgreSQL task repo 70.3%、migration/auth packages PASS；并行integration曾因information_schema未限定schema产生subquery多行，测试已限定`current_schema()`后完整race suite PASS；临时实例停止/清理 |
| V-HOST | yijie-agent-host | `make contract-check && make test && make lint && make runtime-test` | Go 1.26.5 / race + fixed Runtime + temp CODEX_HOME | 0 | PASS | app 67.7%、codex 70.8%、session 77.6%；persisted cleanup/restart/fault injection、atomic lease、title key/isolation/forced-off safety、receipt expiry/schema header、nonce、raw log+bbolt canary covered；no model turn/provider call |
| V-DESKTOP | yijie-desktop | `make lint && make test && make build` | Node 26.0.0 / pnpm 11.9.0 / Rust 1.95.0 / bundled SQLCipher | 0 | PASS 2026-08-03 | 21 files/127 TS；94 Rust tests（93 PASS、1既有signed Keychain integration ignored）；Clippy/fmt/Vite build PASS；no Vue UI source changed |
| V-DESKTOP-S7A | yijie-desktop | targeted bridge/domain + full repository gates | reqwest 0.12.28 rustls/stream；fake TCP Host；canonical `29317b...` fixtures | 0 | PASS / DEC-126-027 ACCEPTED | exact loopback/nonce/owner-token/text-only/strict SSE/domain/error redaction；no invoke/Vue/flag |
| V-DESKTOP-S7B | yijie-desktop | application/database/migration tests + full `make lint/test/build` + diff/no-log scan | SQLCipher；fake TCP Host；synthetic macOS bookmark；canonical v2 events | 0 | PASS / DEC-126-028 ACCEPTED | idempotent/recoverable outbox、accepted/unknown outcome controls、strict cursor/restart、complete/incomplete/unavailable reasoning、10,000 deltas、20/50 history、late-title CAS、v1/v2 migration与Host→SSE→SQLCipher chain；no invoke/Vue/flag/provider call |
| V-INTEGRATION | affected repos | API PostgreSQL + Desktop SQLCipher/native/fake Host/application/IPC fixtures + Host fixed Runtime/fake fixtures | local synthetic only / temp stores | 0 for S4–S8A | AUTHORIZED SLICES PASS | repository/contract/migration/security/Rust application/TypeScript store integrations pass；four-component process E2E remains NOT RUN and blocks G4/local G6 |
| V-SQLITE-LINK | yijie-desktop/src-tauri | `cargo tree -i libsqlite3-sys` + feature tree | Cargo 1.95 | 0 | PASS | single `libsqlite3-sys 0.38.1` via `rusqlite 0.40.1`/`rusqlite_migration 2.6.0`；`bundled-sqlcipher` active |
| V-NO-LOG | API/Host/Desktop source + tests | content-free audit inspection、logger sink scan、raw canary assertions against logger/synced bbolt/HostBridge/application/IPC Debug、sidecar env allowlist、redacted errors/token Debug | local synthetic canaries | 0 | S4–S8A PASS | Public Tasks/PostgreSQL audit content-free；Host raw canary absent from logs/bbolt；Desktop private IPC/client/store无日志调用，secret/path/raw-wire字段扫描为0；future UI/E2E scan remains required |

## 5. 契约与版本兼容

| 结论 | Contract version/full commit/digest/generator | Command/Test | Result | Evidence |
|---|---|---|---|---|
| 源结构与生成无漂移 | `0.3.0 local replacement candidate` / `29317b6426578749dc698fc2ad32b986ee5c8e9f` / digests见`feature.yaml` | post-commit generate/current/lint/test/build/pack | PASS | worktree clean；未远端写入/merge/tag/发布/downstream pin |
| Draft PR merge readiness | PR #1 / exact candidate head | remote CI + dependency attribution | FAIL / HOLD | source/generate/test/pack步骤通过，但high audit失败且两个后续步骤未执行；DEC-126-021已Accepted/HOLD，当前不批准merge |
| Supported baseline breaking check | `f16a497…` sole supported baseline | check-breaking + legacy structural equality | PASS | 自动工具+人工语义；v1错误enum隔离缺陷已修复 |
| Producer conformance | replacement source + API/Host local closure diff | source tests + generated projection + handler/repository + Host schema/fake/fixed-Runtime tests | S4–S6 PASS | API/Host locks resolve`29317b...`；Public Tasks closed content-free shape and Host unchanged source digests conform；flags/routes remain off |
| Consumer conformance | API/Host/Desktop exact locks、generated projections + Desktop S7A/S7B Rust adapters | generate checks + source digest + canonical fixtures/fake Host | S7A TRANSPORT/DOMAIN + S7B APPLICATION PASS | exact existing wire映射与private application语义通过；Vue UI仍未实现 |
| Runtime canonical capability | `yijie-codex@3aa317...` / `codex-cli 0.144.6` artifact | source inspection + fake title/summary/raw/history fixtures + isolated exact artifact delete/restart | raw upstream 4/4 PASS；title/summary primitives PASS；raw observed once；delete functional；forensic erase NOT PROVIDED | 未证明Host/Desktop mapping、raw稳定性/安全性；Runtime WAL/log residue recorded |
| Host v2 title/raw-reasoning compatibility | Host local closure diff + candidate `29317b...` | contract-check/race/fake/fixed Runtime/title/raw/no-log/cleanup recovery + LIA-126-002 review | FOUNDATION CLOSURE PASS | v1 unchanged；cleanup/title/lease/no-log P1 closed；pinned Runtime cannot capability-disable tools so title flag is forced off；all v2 flags off |
| MiniMax feature compatibility | pinned Runtime/MiniMax-M3 + Host `34e94acf…` config | `MM-126-001/002` 各一次、0 retry | title PASS / historical public-summary FAIL / raw observed | structured title可进入后续 Eval；raw展示/SQLCipher生命周期已批准，但单样本不构成raw稳定性、持久化实现或安全conformance；Q-009/Q-016 Resolved |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-025–030 | API secure v2 handler/service/repository/migration | API auth/security/idempotency/integration tests | V-API | S4 PASS；activation/legacy retirement not performed |
| AC-007/010/011/013/014/017/020/021 | Host v2 raw/title/cleanup foundation | Host fake/fixed Runtime、schema/no-log/bbolt/store/restart/race tests | V-HOST | S5 Corrective Closure PASS；title capability hold和Desktop/E2E portions remain |
| AC-001–006/015/020–024/029/030/034/035/037 foundation subset | Desktop SQLCipher/project/sidecar/native commands | Rust/TS migration/repository/nonce/build tests + LIA-126-002 review | V-DESKTOP | S6 Corrective Closure PASS |
| AC-003/007/013/017/020/021 S7A subset | Desktop `HostBridge`/`HostEventStream`/typed event/session/cleanup domain | SEC-011/013/026/027、RES-002/003/004/011 | V-DESKTOP-S7A | Closure PASS / DEC-126-027 Accepted；no WebView/UI behavior claim |
| AC-003/005/007/013–018/025/029 S7B subset | Desktop `ConversationApplication`、outbox/reducer/history/title repository | DOM/RES/DB/SEC Rust tests | V-DESKTOP-S7B | Closure PASS / DEC-126-028 Accepted；no WebView/UI behavior claim |
| AC-003/005/007/013–018/020/021/029/030 S7C subset | Desktop `AuthorizedConversationApplication`、authorization context、session/project actions、interrupt、SQLCipher v4 cleanup/receipt、coordinator与restart/resync projection | S7C auth/action/interrupt/delete/restart/migration/race/no-log Rust tests | S7C historical full gates | CLOSURE PASS / DEC-126-030 Accepted；no Vue or feature activation claim |
| AC-045–047/NFR-008/009 S8A subset | Desktop private schema/fixtures、Tauri commands/events、TS validators/client/Pinia store | IPC-CON/SEQ/CANCEL/RESTART/AUTH/LOG/RACE matrix | V-S8A-DESKTOP | DEC-126-031 Accepted / S8A Closure Passed；no Vue or feature activation claim |
| AC-045–052/NFR-008/009 S8B0 subset | Desktop gate/router/lifecycle/store/readiness/recovery/storage/Tasks metadata | S8B0 conformance/auth/race/default-off/no-log matrix | V-S8B0-DESKTOP | DEC-126-033 ACCEPTED / CLOSURE PASS；no full Vue or activation claim |
| S8B Vue UI/a11y subset | production Vue components + authoritative Pinia store + test-only harness | V-S8B-DESKTOP + browser/axe/security/bundle evidence | LIA-126-006 authorized commands | DEC-126-034 ACCEPTED / CLOSURE PASS；VoiceOver manual remains not run |
| S9 title/raw Eval subset | Host versioned authority/runner/dataset + Desktop exact fixture consumer | V-S9-HOST / V-S9-DESKTOP / V-S9-FLAKY-AUDIT | LIA-126-007 authorized commands | PASS / DEC-126-036 Accepted；test-only，no production behavior claim |
| S10A planning/readiness | process/test-profile/evidence design only | V-S10A-BASELINES/RUNTIME/ENV/SOURCE | DEC-126-037 Accepted / Option C | COMPLETE / S10B HOLD |
| remaining AC/NFR | S10B–S11 | S10B-001–012 matrix in `05/06` | no authorized command | NOT RUN |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| Local four-component E2E | API/Host/Desktop/pinned Runtime create/stream/raw/history/actions/delete/restart | S4–S9 foundations/Eval + accepted S10E + accepted S10P1 | NOT RUN / READINESS HOLD | BLK-001/002/003 closed；BLK-004/005 open；blocks G4/Local-only G6 |
| Security/tenant | Public/local auth/IDOR/path/secret | synthetic tests + source/fixture review + fake Host/IPC/store + production Vue consumer | CURRENT AUTHORIZED SLICES PASS | nonce/token/loopback/error/application/context/IPC scope/cleanup receipt、plaintext rendering和no-log/bundle scan通过；process E2E仍待S10 |
| Failure/resilience | DB/SSE/Host/Runtime/provider faults | repository fault tests + fake TCP Host/TS store + S8B production components | PARTIAL PASS | wrong nonce/token/SSE/error、outbox expiry/unknown outcome、event gap/backpressure/cancel/stale/restart、cleanup lease及UI closed states PASS；full process crash/reconnect/E2E still blocks G4 |
| Migration rehearsal | Desktop SQLCipher + API Tasks owner | embedded SQLCipher + API PostgreSQL foundations | FOUNDATION PASS | populated Desktop v1→current与v2→v3、repeated/read-only/corrupt cases及API idempotency expiry migration PASS；full app rollback/startup E2E pending |
| Isolated Runtime delete | fixed artifact/temp `CODEX_HOME`/synthetic canary | no credentials, model requests 0 | FUNCTIONAL PASS / BYTE RESIDUE FOUND | thread/read fails before and after restart；state row/rollout/index absent；WAL/log byte scan records limitation |
| SQLite dependency selection | Rust 1.95 temp project/macOS arm64 | exact locked dependencies | PASS | selected SQLCipher/migration pair builds；Refinery comparison rejected |
| Runtime fake + bounded MiniMax title/raw reasoning | pinned source/local mock Responses + fixed artifact/Host config | historical 5 upstream fixtures + S5/S7B fake Host fixtures；S9 `feat126-title-raw-v1` deterministic fake dataset；historical 2 provider calls | Host/application foundation PASS / title historical PASS / historical public-summary FAIL / S9 fake-provider Eval PASS | 本轮外部provider调用0；Vue raw plaintext display已在S8B通过，S9 fixed fake Eval通过，flags off；不外推为MiniMax稳定性结论 |
| Performance | list/history/reducer/DB/title | Rust synthetic 10,000 ordered deltas | SLICE PASS | reducer回归0.02s且不逐事件clone/写完整snapshot；正式G4性能矩阵仍NOT RUN |
| AI Eval | title/raw reasoning availability、plain-text safety、sensitive-fragment handling | Host authority `feat126-title-raw-v1`：250 samples、train 200/holdout 50；Desktop exact fixtures | PASS / DEC-126-036 ACCEPTED | title 250/250 schema、200/200 semantic、50/50 unsafe；raw 210/210 valid、40/40 negative；body leak/execution/action/late overwrite均0；仍不等于S10四组件E2E |
| Visual/accessibility | approved Pattern + production Vue implementation | S8B unit/browser/axe/light-dark/1180×760/200%-equivalent/reduced-motion | AUTOMATED/BROWSER PASS | DEC-126-034 Accepted；VoiceOver真人验证留到S11/G6；不等于四组件E2E |

## 8. Diff 与制品完整性

- [x] commit前后`git status`、tracked/untracked name-only和`git diff --check`已复核；S9 Host/Desktop本地checkpoint只包含test-only FEAT-126文件，FEAT-123和其它无关修改均为0
- [x] 范围统计已复核：S9 Host新增版本化runner/dataset/fixtures/lock和test；Desktop仅新增exact fixture consumer与test；Runtime/Infra/API/contracts candidate及production Host/Desktop行为未改
- [x] commit前untracked文件已纳入精确清单并通过仓库门禁；commit后Host/Desktop worktree clean，yijie Governance `1e7a3122…6353` baseline clean后才开始本轮文档diff
- [x] FEAT-126内容与跨文档Gate/ADR/AC已由Codex执行结构化review；最终独立人工Reviewer仍为段成威
- [x] Owner另行授权的checkpoint push已完成；五仓候选分支经`ls-remote`与临时clean clone确认为exact `650254b…139fa`、`a64f9f5…3264`、`3e8df02…f3d9`、`35f2744…7cbd`、`29317b6…e9f`。远端可达不代表merge、tag、publish、deploy、activation、G4或G6
- [x] 本轮MiniMax调用为0；历史两次bounded请求不重跑；无生产资源或其它外部写操作
- [x] 未修改、恢复或覆盖 FEAT-123 既有删除
- [x] 文档未写入 key、token、真实 message、真实 project path 或商家数据

### 8.1 Accepted checkpoint manifest

| Repository | Accepted/current checkpoint SHA | Parent | Files | Validation summary | Remote candidate state |
|---|---|---|---:|---|---|
| yijie | remote Accepted baseline `650254b3c009c4098f7d7b2d415ed8082b0139fa`；DEC-126-036 candidate baseline `ea33f7c23ef9583f8829e9aa456920c0d04afc0c`；Accepted docs commit另行本地回报 | `ea33f7c…fc0c` | 12 current governance files | package/strict/G2A/YAML/pnpm lint/test/diff rerun for Owner acceptance | remote candidate remains exact `650254b…139fa`；本轮不追加push |
| yijie-api | `a64f9f591fb594818c1778e30c6941e2574b3264` | `b5e601764357512208cc09bfb2b30b244a1b82ac` | 16 | generate-check、vet/lint、race/unit、isolated PostgreSQL migration 1–4/integration、scope/no-log/diff PASS | `origin/feat/feat-126-foundation-closure` exact；develop unchanged |
| yijie-agent-host | S9 local `8707dea552cff74121b89aa8045f27da2c8c9378` over remote Accepted `3e8df026110f0c895262329c2384d3896598f3d9` | `3e8df026…f3d9` | test-only Eval authority/runner/dataset/fixtures/lock | `feat126-eval`、lint、test/race/coverage、build、scope/no-log/diff PASS | remote remains `3e8df026…f3d9` exact；S9 checkpoint local only/not pushed |
| yijie-desktop | S9 local `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb` over remote Accepted `35f27447398529cca4dec85fa1f67e779c7a7cbd` | `35f27447…7cbd` | exact Host fixtures + Rust/TS test consumer | 30 TS files/165 tests、96/97 Rust（1 existing ignored）、lint/build/fmt/clippy/bundle/security/no-log PASS；existing cleanup timing flake audited and clean rerun PASS | remote remains `35f27447…7cbd` exact；S9 checkpoint local only/not pushed |
| yijie-contracts | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | source/fixtures/generated package | generate/lint/test/build/pack/breaking/v1 equality/conformance PASS | `origin/feat/feat-126-content-free-candidate` exact；Draft PR #1仍指向历史candidate且不变 |

文件清单（相对各仓库根）：

- yijie：`docs/features/FEAT-126-public-task-authorization-hardening/{feature.yaml,00-feature-brief.md,01-requirements.md,02-impact-assessment.md,03-decisions-and-risks.md,04-contract-change-plan.md,05-technical-design.md,06-test-plan.md,07-implementation-plan.md,08-verification-report.md,09-release-and-rollback.md,10-delivery-summary.md}`。
- yijie-api：`.github/workflows/ci.yml`、`Makefile`、`contracts/public-api.lock.json`、`internal/interfaces/publicapi/{access_handler.go,secure_task_handler.go,secure_task_handler_test.go,types.gen.go}`、`internal/modules/tasks/application/{secure_service.go,secure_service_test.go}`、`internal/modules/tasks/domain/task.go`、`internal/modules/tasks/infrastructure/postgres/{repository.go,repository_integration_test.go}`、`internal/platform/database/database.go`、`internal/platform/migrations/{migrations.go,migrations_integration_test.go,sql/00004_harden_secure_task_audit_and_idempotency.sql}`。
- yijie-agent-host：`api/contracts.lock`、`internal/app/{app.go,app_test.go}`、`internal/codex/{runtime_test.go,session_protocol.go,title.go}`、`internal/session/{service.go,service_test.go,store.go,store_test.go,title.go}`。
- yijie-desktop：`.github/workflows/ci.yml`、`contracts/public-api.lock.json`、`scripts/{generate-public-api.mjs,generate-public-api.test.mjs}`、`src-tauri/{Cargo.lock,Cargo.toml,capabilities/default.json}`、`src-tauri/fixtures/chat-ipc-v1/{bind-request.json,context-response.json,error.json,event-corpus.json,reasoning-event.json,response-corpus.json}`、`src-tauri/migrations/chat/{0003_chat_application_domain.sql,0004_chat_s7c_orchestration.sql}`、`src-tauri/schemas/chat-ipc-v1.schema.json`、`src-tauri/src/chat/{application.rs,authorization.rs,database.rs,error.rs,host_bridge.rs,host_domain.rs,ipc.rs,keychain.rs,migrations.rs,mod.rs,sidecar.rs,worker.rs}`、`src-tauri/src/{lib.rs,native_auth/mod.rs,native_auth/runtime.rs}`、`src/api/{chat-client.test.ts,chat-client.ts,generated/public.gen.ts}`、`src/domain/{chat-ipc.test.ts,chat-ipc.ts}`、`src/stores/{chat.store.test.ts,chat.store.ts}`。

## 9. 独立 Requirements Review Findings

并行只读审查由三个隔离子任务完成：UI/UX、cross-repository/security、Feature Package process。它们不是独立人工批准。

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| REQ-REV-001 | P1 resolved | Feature ID/ADR-0012 | FEAT-126 已预留，纯 UI 复用会破坏安全例外追踪 | 合并安全纵向需求；DEC-126-001 Accepted | 段成威 G1 approval 2026-08-01 |
| REQ-REV-002 | P1 resolved | permission entry/Host policy | fixed `never` 与可编辑审批入口冲突，可能假授权 | 固定只读 read-only/deny；DEC-126-003 Accepted | 段成威 G1 approval 2026-08-01 |
| REQ-REV-003 | P1 resolved for G2 design | permanent delete | Runtime functional/restart deletion 已证明，同时 WAL/log 字节残留否定 forensic erase；Host bridge/bbolt/replay 与 Desktop SQLCipher/checkpoint 尚待实现 | ADR-0014/DEC-126-006 Accepted；Q-006 Resolved；限定成功语义并冻结 saga | Owner approval 2026-08-02；implementation E2E still G4 blocker |
| REQ-REV-004 | P1 resolved for S4 foundation | Public Tasks | anonymous/body tenant/ID-only query 存在 IDOR | secure creator-private `/v2/tasks` source candidate + v1双隔离；S4 provider/repository/authz/audit 已实现，默认关闭 | contract source gates、API unit/integration/security conformance PASS；完整跨仓 E2E 仍待 S7+ |
| REQ-REV-005 | P2 resolved for G2 | Chat/App Shell Pattern | active Pattern 与极简需求/侧栏规则冲突 | 独立FEAT-126 Pattern已Accepted，只取代冲突段落 | Owner approval 2026-08-02 |
| REQ-REV-006 | P2 resolved for product/source shape；implementation仍待 Gate | reasoning/title | Runtime fake fixtures证明 primitives；`MM-126-001` title PASS；`MM-126-002` 无public summary但观察到raw reasoning | ADR-0015保留title；ADR-0016要求raw纯文本；DEC-126-016/017固定SQLCipher生命周期和closed v2；Host source只投影受控raw variants | source fixtures PASS；Host/Desktop runtime conformance pending |
| REQ-REV-007 | P2 resolved for G2 design | local persistence | Desktop 无 DB，Host 不应成为业务 DB | ADR-0013 accepts authority；ADR-0014 accepts exact SQLCipher driver/migration/key/file/backup boundary | Owner approval/Q-015 Resolved 2026-08-02；implementation security pending |
| REQ-REV-008 | P1 resolved | ADR-0012 linkage | ADR 在目录创建后仍写“尚未创建” | 先修正创建事实，G1 批准后再同步为“已创建、G1 Passed、G2/实施未批准”；create/implement checklist 分离 | scoped diff/checker rerun PASS |
| REQ-REV-009 | P1 resolved | `07` S0/S1 | G1 前置循环且 Runtime write 可能绕过 G2 | S0 前置改为 G0+明确评审；S1 在 G2 前只读，任何 source write 需 G2 | plan wording reviewed |
| REQ-REV-010 | P2 resolved | `01` BR/Q | 侧栏引用错号且 Candidate Must 易被误读为批准 | 修正为 Q-005；顶部加入 Candidate Must 声明 | strict checker PASS |
| REQ-REV-011 | P2 resolved for G2 | visual references | 临时截图只有 hash/摘要，无法作为 durable release asset | Accepted FEAT-126 Pattern已承接，不要求保存临时附件 | Owner approval 2026-08-02 |

### 9.1 LIA-126-001 Structured Review

该评审由Codex基于最终diff、契约、测试与安全边界执行，不冒充独立人工review。最终Owner审查仍由段成威完成。

| Finding | Severity | 影响 | 处理 | 复验/状态 |
|---|---|---|---|---|
| LIA-REV-001 | P1 resolved | Desktop session最初只有`project_id`单列FK，数据库层不能阻止跨owner/tenant项目关联 | `chat_projects`增加复合唯一键，`chat_sessions`使用`(project_id, owner_user_id, tenant_id)`复合FK并加负向测试 | Rust SQLCipher/migration/full gates PASS |
| LIA-REV-002 | P1 resolved | Host既有bbolt与新增receipt key在已存在路径上可能跟随symlink/hardlink | Host home、DB、key加入Lstat/type/owner/nlink/mode fail-closed校验；保留安全regular file权限修复；补symlink tests | Host race/full gates PASS |
| LIA-REV-003 | P1 resolved | title ephemeral notification可能泄入主session，且响应身份/path若未精确校验会破坏隔离 | pending title start隔离、private collector路由、unexpected item interrupt、exact provider/model/ephemeral/path-null验证 | fake Runtime title test与Host full gates PASS |
| LIA-REV-004 | P2 resolved | completed前存在delta gap时不能把非连续内容冒充完整推理 | 只发布已验证连续prefix并以`stream_gap` finalized incomplete；无prefix时unavailable | Host sparse-gap fixture PASS |
| LIA-REV-005 | P2 resolved | API v3 tenant FK使旧integration fixture暴露缺少tenant seed | 修正synthetic fixture先创建tenant；没有放松FK或migration | isolated PostgreSQL `make test-integration` final PASS |
| LIA-REV-006 | Residual / accepted for slice | signed Keychain round-trip、真实sidecar进程、四组件E2E、UI reducer/visual均不属于S4–S6完整证据 | 明确列为NOT RUN；flags保持off；不得据此通过G4/G6 | blocks S7–S11/G4，不阻断S4–S6 completion |

### 9.2 LIA-126-002 Foundation Corrective Closure Review

| Finding | Severity | 事实 | 要求/状态 |
|---|---|---|---|
| LIA2-API-001 | P1 / CLOSED | secure Tasks只在成功create事务写business audit；401/403/404/409/503、get及拒绝路径未形成完整content-free审计矩阵 | handler/repository矩阵及isolated PostgreSQL tests PASS；unresolved tenant允许nullable tenant，UUID-only request/trace与status/reason metadata不含正文 |
| LIA2-CONTRACT-001 | P1 / CLOSED | 历史candidate的`CreateTaskV2Request.input`/`TaskV2.input`为arbitrary object；canonical conversation fixture携带并回显`input.text` | DEC-126-023/024形成并批准`29317b...`；API/Desktop lock及生成投影已切换，closed content-free negative conformance PASS |
| LIA2-API-002 | P1 / CLOSED | API及Desktop远端CI仍checkout旧contracts SHA；API `generate-check`实际执行generate并重写，不能证明只读drift | 本地CI投影统一完整SHA`29317b...`；API generate-check在临时目录生成并逐字节比较，不改工作树；drift gate PASS |
| LIA2-HOST-001 | P1 / CLOSED | Runtime delete成功而通知/Host落库失败时没有durable intermediate state；同operation retry可能永久卡在Runtime NotFound | bbolt schema v3持久化pending/confirmed operation；notification loss、Runtime exact NotFound、Host落库失败、restart与same-operation replay tests PASS |
| LIA2-HOST-002 | P1 / CLOSED | cleanup与StartTurn缺少原子lease；并发starting turn可能与mapping删除竞态 | BeginCleanup在单一bbolt事务获取session lease；turn/resume/mark paths均拒绝cleaning；race test PASS |
| LIA2-HOST-003 | P1 / CLOSED WITH CAPABILITY HOLD | title idempotency只按operation ID、失败可重复调用；空cwd/no-tools未在能力层保证 | key改为`(session_id, operation_id)`且failed/unknown不重调；owner-only 0700空temp cwd；固定Runtime不能能力级禁用tools，因此production config强制拒绝title flag=true，保持关闭 |
| LIA2-DESKTOP-001 | P1 / CLOSED | reasoning commit未强制terminal turn及turn/item一致终态 | terminal_at/status与aggregate/item/reason-code一致性强制；joined history消除item N+1；negative and populated-history tests PASS |
| LIA2-DESKTOP-002 | P1 / CLOSED | sidecar spawn后只接受固定loopback health JSON，不能证明是本次实例；旧/同用户进程可伪装ready | 每次spawn生成UUID nonce并要求health/ready响应头匹配；Host liveness与Runtime ready分层；wrong nonce/liveness-only/503/ready tests PASS |

- LIA-126-002执行结论：前轮在`LIA2-CONTRACT-001`处暂停；DEC-126-025完成远端状态校正后，S4–S6 Corrective Closure通过逐仓/隔离验证并获DEC-126-026接受；其Accepted checkpoints后来按Owner明确授权推到专用候选分支，并已由DEC-126-035只读复验为exact。
- Contract impact：`breaking`。DEC-126-023 C已形成新source commit而未amend既有candidate；DEC-126-024已批准，G2A重审通过。
- S7A授权结果：DEC-126-026另行授权Desktop Rust拥有Host bearer/token注入、loopback HTTP/SSE、schema header与nonce校验、typed wire/domain adapter；DEC-126-027已接受该closure并单独授权S7B，不授权Tauri/WebView或Vue UI。

- Reviewer 是否独立于主起草上下文：否；本轮是 Owner 前的设计候选自检，最终独立 Reviewer 为段成威。
- P0/P1 是否清零：对已实现的S4–S9范围为是。FEAT-126全需求仍未清零；S10A发现5个S10B readiness P1，不回退已接受的S4–S9 Closure，但继续阻断S10B/G4/G6。
- P2 例外批准：无；不是 accepted risk。

### 9.3 S7A Desktop Rust Host Bridge/Domain Closure Review

| Finding | Severity | 事实 | 处理/复验 |
|---|---|---|---|
| S7A-REV-001 | P1 / CLOSED | 仅检查固定loopback health不能把调用绑定到本次spawn实例，且proxy/redirect可能扩大transport边界 | 每次受保护调用先严格校验`/readyz` nonce；两个reqwest client均`no_proxy`、redirect none；wrong nonce在token读取和protected request前失败；tests PASS |
| S7A-REV-002 | P1 / CLOSED | 直接`read_to_string`可能跟随token symlink、接受开放权限或在错误/Debug中泄漏bearer | `O_NOFOLLOW|O_CLOEXEC`、regular/current euid/nlink=1/mode 0600-ish/size/base64url检查；zeroizing holder与redacted Debug；0644/symlink/bearer tests PASS |
| S7A-REV-003 | P1 / CLOSED | 宽松HTTP/SSE解析会把错误schema、stream切换、重复sequence或超限raw作为有效内容交给后续UI | no-store/content-type/schema/stream headers与UUID cursor严格校验；single-line bounded SSE；canonical reasoning/caps/duplicate/malformed tests PASS |
| S7A-REV-004 | P1 / CLOSED | “兼容未知事件”若保留任意payload会绕过closed known domain；若接受未知terminal会破坏turn终态 | 未知非terminal仅保留event identity并丢payload；未知terminal fail closed；future-event canary与redacted Debug tests PASS |
| S7A-REV-005 | P1 / CLOSED | 公开Tauri command可能过早把token/path/raw wire暴露给WebView并越过S8授权 | S7A只在Rust module公开领域API，由`ChatRuntime`内部持有；invoke handler未变、无`.vue` diff；source/diff scan + build PASS |
| S7A-REV-006 | P2 / CLOSED | fixed Runtime不能能力级禁用tools，若S7A暴露title HTTP method会形成误启用路径 | bridge刻意不实现title operation；Host title flag仍false；生命周期请求测试确认无model/reasoning-effort selector |

- Contract impact：对FEAT-126总体仍是`breaking`（DEC-126-023 replacement）；S7A自身为现有Host v1/v2 wire的`additive local consumer`，没有source-contract/producer change，因此不触发新的G2A source candidate。
- Reviewer独立性：Codex执行结构化自检，不冒充独立人工Reviewer；DEC-126-027已由Owner段成威接受。
- S7A范围P0/P1：未发现P0；上表S7A P1均有本地fake/fixture证据关闭。G3仍Partial；Owner随后只授权S7B，未授权S8或G4/G6。

### 9.4 S7B Desktop Rust Application Orchestration/Domain Closure Review

| Finding | Severity | 事实 | 处理/复验 |
|---|---|---|---|
| S7B-REV-001 | P1 / CLOSED | create/turn网络重试若没有持久化operation与accepted边界，可能重复创建Host session或重复计费 | session/message/outbox单事务；same-operation payload一致性；lease/max16；Host已接受turn后暂停自动重放，unknown outcome fail closed；expiry/restart/fake Host tests PASS |
| S7B-REV-002 | P1 / CLOSED | assistant、cursor、reasoning与outbox分开写会在崩溃后出现重复文本或假completed | assistant/cursor按16 events或50ms合并checkpoint；terminal一次事务提交assistant/reasoning/cursor/outbox；snapshot conflict显式incomplete；tests PASS |
| S7B-REV-003 | P1 / CLOSED | duplicate、gap、stream/turn身份混淆或restart cursor可能污染另一会话历史 | 严格task/session/thread/turn/stream/event/sequence；exact duplicate忽略，gap/mixup拒绝，restart从durable cursor继续；tests PASS |
| S7B-REV-004 | P1 / CLOSED | 列表若预取正文或history逐item查询，会泄漏/放大且快速切换易竞态 | 列表仅metadata；history按turn稳定分页默认20/最大50，messages/reasoning metadata批量装配；DB tests PASS |
| S7B-REV-005 | P1 / CLOSED | 迟到模型标题覆盖人工rename或失败结果无限重试 | title source CAS；user rename取消job且永远优先；model title严格校验，总调用cap=2；fixed Runtime能力hold下不派发title operation；tests PASS |
| S7B-REV-006 | P1 / CLOSED | Rust Debug/error可能打印prompt、assistant、raw reasoning、title或project | 对含敏感字段的projection自定义redacted Debug，错误只含稳定content-free code；canary tests PASS |
| S7B-REV-007 | P2 / CLOSED | 每个delta clone完整assistant/reasoning会形成O(n²)开销 | reducer outcome只返回progress marker，按batch构造snapshot；10,000 ordered deltas回归0.02s PASS |

- Contract impact：FEAT-126总体仍是`breaking`；S7B自身只增加Desktop private schema v3索引和durable/application semantic behavior，不改变Host/Public Tasks wire、producer或`29317b...`，不触发新的G2A candidate。
- Reviewer独立性：Codex执行结构化自检，不冒充独立人工Reviewer；DEC-126-028已由Owner段成威接受。
- S7B范围P0/P1：未发现P0；上表P1均由fake Host、固定fixture、临时SQLCipher和full Desktop gates关闭。G3仍Partial，不能据此进入S8或通过G4/G6。

### 9.5 DESIGN-126-005 Desktop IPC/ViewModel Contract Review

| Finding | Severity | DESIGN-126-005设计时事实 | 当时设计关闭/后续验证 |
|---|---|---|---|
| IPC-REV-001 | P1 / DESIGN CLOSED / S7C SOURCE PASS | ConversationApplication无Tauri command/event；直接做Vue会复制dispatch/retry/cleanup状态机 | S7C已独占Rust coordinator/actions/delete/interrupt/restart；S8A/S8B顺序后移。IPC adapter仍NOT RUN |
| IPC-REV-002 | P1 / DESIGN CLOSED / S7C SOURCE PASS | WebView capability投影不能证明active owner/tenant/resource authorization | S7C已实现Rust-bound 300s context、tenant/revision/capability复验与authorized facade；S8A command resource/DTO conformance仍NOT RUN |
| IPC-REV-003 | P1 / DESIGN CLOSED | Host bearer、SQLCipher key、canonical path或Host raw wire若过桥会扩大攻击面 | private schema从字段级排除；event/error只含stable DTO与bounded plain text；canary/no-log matrix冻结。实现证据NOT RUN |
| IPC-REV-004 | P1 / DESIGN CLOSED | Tauri event无ack，无queue/sequence规则会丢增量、内存放大或串session | 64 events/256KiB、20Hz coalesce、严格projectionSequence、gap/overflow→resync、terminal不可丢。实现证据NOT RUN |
| IPC-REV-005 | P1 / DESIGN CLOSED | 快速A→B、logout/restart与late response/event会闪现旧scope正文 | context+subscription+selectionEpoch三元绑定，切换先清空，process-bound cursor失效并从SQLCipher resync。实现证据NOT RUN |
| IPC-REV-006 | P1 / DESIGN CLOSED | 前端cancel若被当作已接受写操作回滚，会产生重复turn/delete不确定状态 | 仅read/subscription可cancel；durable write按operation对账，stop只走interrupt，delete走Rust saga/status。实现证据NOT RUN |

- Contract impact：DESIGN-126-005是Desktop private additive/semantic contract候选，不改变central `yijie-contracts@29317b...`或Runtime pin，不触发新G2A source candidate。
- 审查结论：本节保留DESIGN-126-005当时的差距快照。随后DEC-126-030/031已Accepted，LIA-126-004 S8A Closure Passed；实现关闭证据见§9.7。S8B0/S8B仍须按DESIGN-126-006分别授权。
- 设计评审变更边界当时仅为需求包；后续S7C修改Desktop Rust/SQLCipher，S8A再按LIA-126-004修改private Tauri IPC与TypeScript ViewModel；两者均不含Vue、feature flag、MiniMax、contracts/Runtime或远端状态。

### 9.6 LIA-126-003 / S7C Closure Review

| Finding | Severity | 关闭证据 | 状态 |
|---|---|---|---|
| S7C-REV-001 | P1 | `ChatAuthorizationManager`把tenant绑定在Rust；opaque context最长300秒；revision前进清空旧context，revision回退/logout/expiry/missing capability均fail closed；`AuthorizedConversationApplication`逐动作复验，Debug不含tenant/capabilities | CLOSED |
| S7C-REV-002 | P1 | project/session pin幂等保留首次时间；project remove与turn enqueue由同一SQLCipher worker串行，removed project和deleting session拒绝新turn；rename继续user-wins | CLOSED |
| S7C-REV-003 | P1 | interrupt持久化stable operation，同operation重试同turn；Host `turn_not_active`经get-session确认后本地terminal reconcile；transport/not-ready只重试同operation | CLOSED |
| S7C-REV-004 | P1 | schema v4持久化cleanup job/lease/attempt/next-at/error；delete与active turn共享session lease，先interrupt并确认terminal；Host cleanup complete后才级联Desktop并checkpoint；checkpoint后生成content-free receipt | CLOSED |
| S7C-REV-005 | P1 | receipt HMAC使用独立`com.yijie.ai.chat-receipt` protected Keychain 32-byte key；key缺失仅在没有现存job/receipt时可初始化；receipt无session/owner/tenant/path/body并30天到期清理 | CLOSED |
| S7C-REV-006 | P1 | `ConversationCoordinator`只在Rust调度outbox/stream/cleanup；restart snapshot恢复active session和cleanup operation；live raw/assistant projection受既有1MiB/256KiB caps约束，Debug只输出字节数；历史raw按turn读取 | CLOSED |
| S7C-REV-007 | P1 | populated v1/v2/v3→v4、重复启动、legacy v3 job显式`legacy_unrecoverable`、operation idempotency、restart、delete-vs-turn、cascade/FK/WAL、receipt expiry、fake Host完整cleanup与raw no-log tests通过 | CLOSED |
| S7C-REV-008 | P2 | `src-tauri/src/lib.rs`仍只有7个既有foundation chat invoke，conversation invoke/event为0；本切片没有TS/Vue或feature flag diff | CLOSED |

- Contract impact：S7C为Desktop-private `additive/semantic` Rust domain + SQLCipher schema v4，不改变Host/Public Tasks wire、唯一contracts candidate或Runtime pin，不触发新G2A。
- Gates：Desktop `make lint/test/build`均exit 0；113 TS；88 Rust（87 pass、1个既有signed Keychain integration ignored）；Clippy `-D warnings`、fmt与Vite build通过。
- 环境/调用：仅fake Host、固定fixture、临时SQLCipher/temp目录；0 MiniMax/provider、0真实数据、0 flag activation、0远端写入。
- 结论：S7C范围未发现残余P0/P1；Owner已接受DEC-126-030。G3仍Partial，且DEC-126-030只单独导出LIA-126-004/S8A，不授权S8B。

### 9.7 LIA-126-004 / S8A Closure Review

| Finding | Severity | 关闭证据 | 状态 |
|---|---|---|---|
| S8A-REV-001 | P1 | `chat_bind_context_v1`只接收tenant selector；Rust native authority绑定owner/tenant/revision/expiry/capabilities并只返回300秒opaque context、expiry和allowlisted actions；same-revision rebind、revision切换、logout、expiry和较慢旧tenant bind均使旧结果失效 | CLOSED |
| S8A-REV-002 | P1 | Desktop-owned Schema为20/20 command指定closed request/response refs，为7/7 event指定互斥closed variants；Rust `deny_unknown_fields`、golden serde fixtures与TypeScript exact-object validators共同冻结v1 shape，unknown field/kind/cursor/u64越界均拒绝 | CLOSED |
| S8A-REV-003 | P1 | 20个Tauri commands逐动作复验capability/resource；owner/tenant、Host bearer、SQLCipher key、canonical path、Host/Runtime ID和原始wire不在DTO；旧unversioned project invokes从handler移除 | CLOSED |
| S8A-REV-004 | P1 | assistant append≤64KiB、reasoning append≤16KiB，reasoning只用local ordinal/content index；单batch≤64 events/256KiB并最多20Hz；duplicate忽略，gap/overflow/protocol error停止增量并resync | CLOSED |
| S8A-REV-005 | P1 | TypeScript store只有一个authoritative reducer；`contextId + subscriptionId + selection generation`绑定，A→B先清正文/取消read/退订，late response/event、乱序或错误session不能commit；newest tenant bind wins | CLOSED |
| S8A-REV-006 | P1 | 只有read可通过request ID取消，durable write不伪回滚；interrupt/delete使用既有stable operation/status；restart后旧context/subscription/cursor失效，新subscribe+resync恢复SQLCipher history和content-free cleanup状态 | CLOSED |
| S8A-REV-007 | P1 | Tauri capability只增加`core:event:allow-listen/unlisten`，明确无WebView emit/emit-to；生产client直接使用Tauri invoke/listen，注入transport仅限测试；Vue页面/组件/路由/样式diff为0，feature flags保持关闭 | CLOSED |
| S8A-REV-008 | P1 | full Desktop gates：21/21 TS files、127 tests；94 Rust tests中93 pass/1既有signed Keychain ignored；generate exact `29317b...`、eslint/vue-tsc、rustfmt/clippy `-D warnings`、Vite build全绿；secret/path/raw-wire/no-log scan为0 | CLOSED |

- Contract impact：S8A为Desktop-private `additive/semantic` IPC/ViewModel contract，不改变Host/Public Tasks wire、唯一contracts candidate或Runtime pin，不触发新G2A。
- 摘要：Schema=`21112a5d…eb1a`，Rust IPC=`f8504976…155a`，response/event corpus=`d1a69914…2e52`/`60e667b9…e60b`，TS domain/client/store=`d96b3cf9…e121`/`e96fe294…27de`/`c194c304…bc3`，Tauri capability=`48da0d1c…e39`；完整值见`feature.yaml`。
- Full-suite审计：并行测试暴露两个既有时间夹具读取过早问题（outbox claim与rename activity）；已改为在操作点读取测试时钟，未放宽业务断言。Schema初稿的generic payload也在Closure前收紧为逐command/逐event closed refs。
- 环境/调用：仅fake Host、固定fixture、临时SQLCipher/temp目录；0 MiniMax/provider、0真实数据、0 flag activation、0远端写入。
- 结论：Owner已接受DEC-126-031；S8A范围未发现残余P0/P1，S8A Closure Passed。G3仍Partial，接受不自动授权S8B。

### 9.8 DESIGN-126-006 / DEC-126-032 / LIA-126-005 S8B0 Closure Review

| Finding | Severity | Evidence | Candidate closure | Status |
|---|---|---|---|---|
| S8B0-REV-001 | P1 | 没有`VITE_YIJIE_CHAT_LOCAL_UI_ENABLED`；router/nav可创建`/chat` loader | exact-true/default-false gate覆盖nav、routes、deep-link和loader；env/CI/default build未设置true；truth-table与loader spy PASS | CLOSED IN `5dab02a1…34d85` |
| S8B0-REV-002 | P1 | permission policy按exact path查找且无session deep route | `/chat`=`task.create`，`/chat/:sessionId`=`task.read`；invalid/not-found/denied/stale按closed recovery处理，Rust resource check不变 | CLOSED |
| S8B0-REV-003 | P1 | permission tenant/revision/logout未与Chat bind/clear/dispose形成唯一app lifecycle | testable app-level lifecycle先dispose旧scope，epoch阻止stale bind；default-off/无revision/无cap不bind | CLOSED |
| S8B0-REV-004 | P1 | store缺project actions、追加分页和delete完成导航 | authoritative store新增project pick/revalidate、dedupe append、cleanup reload/clear与closed DeleteDisposition，App只消费store导航 | CLOSED |
| S8B0-REV-005 | P1 / PRIVATE IPC STOP | `phase=ready`不证明Host/Runtime/storage ready | 两个closed commands、Rust-owned start/retry/storage probe、schema↔serde↔TS fixture/client/store完成；send必须`canSend`且Rust再复验 | CLOSED |
| S8B0-REV-006 | P1 | `/tasks` production使用`sampleTasks` | sample production module/test删除；Tasks消费真实Pinia session metadata分页并受default-off gate保护 | CLOSED |
| S8B0-REV-007 | P2 | requirements 96px与Accepted Pattern 48/160冲突 | Pattern 1.0.0优先：follow≤48px、button>160px、exact aria-label | CLOSED IN DOCS |
| S8B0-REV-008 | P1 governance | 只能在DEC-126-032后单独实现S8B0，不能进入S8B | LIA-126-005只改Rust/TS integration与既有Tasks metadata页；`src/pages/chat/ChatPage.vue`、production deps、flag config、central pin和远端均未变 | PASS |

- Contract impact：`semantic` Desktop-private candidate；central `yijie-contracts@29317b...`、Host/Public Tasks wire和Runtime pin均未变，不触发G2A重审。
- 实施状态：LIA-126-005完成并形成slice checkpoint；DEC-126-033已由Owner接受，S8B0 Closure Passed；该slice现为Desktop远端exact S8B candidate的祖先，不代表独立merge/activation。
- 测试依赖：0新增。未来S8B若需依赖，只允许fixed devDependency并提供audit/lockfile证据；production dependency保持0新增。
- 结论：S8B0 P1全部关闭，Owner已接受DEC-126-033并保持G3 Partial；仅可另行评审S8B，不能自动开始。

### 9.9 LIA-126-006 / DEC-126-034 S8B Closure Review

| Finding | Severity | 证据 | 状态 |
|---|---|---|---|
| S8B-REV-001 | P1 scope | commit仅含Vue/TS/style/test/docs/lockfile；无`src-tauri`、private schema/client/store wire shape、central contract、Host或Runtime diff | CLOSED |
| S8B-REV-002 | P1 authority | Vue源码扫描无`chatClient`/raw`invoke`/Host；所有操作进入authoritative Pinia actions；App继续消费closed `DeleteDisposition` | CLOSED |
| S8B-REV-003 | P1 content safety | assistant/raw reasoning仅文本插值，无`v-html`/Markdown；browser正文容器HTML descendants=0；secret/path/raw-wire扫描PASS | CLOSED |
| S8B-REV-004 | P1 interaction | composer/IME/readiness/interrupt、history/reasoning、project/session menus、delete/cleanup、48/160 scroll与排除功能有生产组件测试 | CLOSED |
| S8B-REV-005 | P1 visual/a11y | 1180×760 light/dark无横向overflow；200%等价590×380主要操作纵向可达；permission/delete modal焦点恢复；axe 0 serious/critical | CLOSED FOR AUTOMATED/BROWSER EVIDENCE |
| S8B-REV-006 | P2 manual | VoiceOver人工清单已新增；当前没有人类执行结果 | OPEN FOR OWNER MANUAL REVIEW；不得写成已通过 |
| S8B-REV-007 | P1 dependency/bundle | `axe-core@4.10.3` exact dev-only；npm audit 0；production deps/bundle无axe/test harness/synthetic fixture | CLOSED |
| S8B-REV-008 | P1 governance | flag仍unset/default false；无MiniMax、真实数据、S9–S11、四组件E2E、push/merge/tag/publish/deploy | PASS |

- Desktop checkpoint：`35f27447398529cca4dec85fa1f67e779c7a7cbd`，parent=`5dab02a1ad5f03fead236aa7060fa6a75a234d85`，27 files，clean；后续Owner-authorized push已使同SHA在专用远端候选分支精确可达，未merge/启用。
- Frontend：`pnpm lint/test/build` PASS；29个TS测试文件 / 164 tests；production build 4625 modules。
- Rust：unchanged suite在允许loopback、SQLCipher temp permissions与security-scoped bookmark的环境PASS，95/95 + 1既有ignored。首轮sandbox 21 failures均为`Operation not permitted`/unsafe temp path，不是产品断言失败。
- Dependency/security：`pnpm audit --audit-level high` PASS；bundle/direct-boundary/secret/path/flag scans和`git diff --check` PASS。
- Visual evidence：test-only harness直接挂载生产组件和真实Pinia reducer；浏览器light/dark/1180×760、200%-equivalent、permission/delete focus、plain-text projection PASS。harness不在production entry/bundle。
- 结构化结论：未发现S8B范围内残余P0/P1；Owner已接受DEC-126-034方案A，S8B Closure Passed，G3仍Partial。VoiceOver真人清单、S9 Eval、S10四组件E2E与S11 G6分别保留，不能合并宣称。

### 9.10 DEC-126-035 Remote State Reconciliation（Accepted）

- `git ls-remote`与五个临时single-branch clean clone均确认候选HEAD精确匹配；clone worktree全部clean，临时目录已删除。
- Owner此前已明确授权对应checkpoint push；本轮只读复验，没有fetch-to-worktree、push、force update、branch mutation或PR操作。
- 各`origin/develop`仍为复验时的`6c23dc3…513b`、`faeb780…bf34`、`34e94ac…18e4`、`155854c…70b5`、`9ec34ab…ebbb`；Draft PR #1、历史`c000a024…588c`、contracts sole candidate均未改变。
- Owner决策：DEC-126-035已接受“远端精确可达”作为provenance事实；不得将其升级为merge/tag/publish/deploy/feature activation/G4/G6或Code Complete结论。
- Owner随后单独授权LIA-126-007：Host持有版本化runner/dataset authority，Desktop做exact downstream fixture validation；固定fake provider、Runtime/Host pins与合成数据。执行结果见§9.11，不追溯扩大DEC-126-035。

### 9.11 DEC-126-036 / S9 fake-provider Eval Closure Review（Accepted）

| Finding | Severity | 事实与结果 | 状态 |
|---|---|---|---|
| S9-REV-001 | P1 authority/determinism | Host唯一维护`feat126-title-raw-v1` manifest/schema/dataset/split/generator/runner/fixtures；runner在执行前校验lock内完整SHA-256；Desktop只锁定并消费Host exact SSE/consumer fixtures | CLOSED |
| S9-REV-002 | P1 dataset | 250条全合成样本：200多语言普通、50 injection/adversarial；train=200、holdout=50（20%）；不含真实用户数据或真实项目路径 | CLOSED |
| S9-REV-003 | P1 title gate | `title-v1` strict schema/sanitizer 250/250；普通语义200/200；unsafe拒绝50/50；late model覆盖用户rename=0；HTML/control/system prompt/secret/path/action泄漏=0 | CLOSED |
| S9-REV-004 | P1 raw gate | valid reasoning 210/210产生非空具体纯文本并精确完成delta/index/final/reconciliation；missing/gap/invalid/oversize各10、合计40/40明确Gate FAIL；HTML/Markdown执行=0 | CLOSED |
| S9-REV-005 | P1 persistence/consumer | Desktop production SSE decoder、authoritative reducer、临时SQLCipher terminal commit/history reload/restart/title priority/session cascade delete及Vue纯文本projection消费同一fixture均PASS；raw正文未进入DB残留、bundle或测试日志 | CLOSED |
| S9-REV-006 | P1 boundary | production Host/Desktop行为、central contracts、Host/Public Tasks wire、private IPC与Runtime pin均未改；flags保持off；MiniMax/外部provider调用0；真实数据0；远端写入0 | CLOSED |
| S9-REV-007 | P2 test stability | Desktop首次全量Rust运行中，既有`fake_host_coordinator_finishes_durable_content_free_cleanup`因复用跨秒前`now`出现一次timing failure；该生产文件不在S9 diff，目标重跑与第二次全量96/96均PASS | CLASSIFIED PRE-EXISTING FLAKE；未修改生产代码、未豁免失败 |

- Authority摘要：manifest `7196ede3defe1b34e7f9c2cc2e869dedf887206112ace31d94f3cf87fa5f2f2c`；schema `c2ffb1631fe6d1709356ab61ea841a4b74b9e9ffd0a5880edec6cc7365d6a60c`；dataset `523609b44fd244fff18b930c992375999276c2e0d5786efadfd8858ec623b308`；split `abeecfa113ba6a7eecee9be6e3d2ba97377c596bdddf4553cabc50668916afc7`；runner `3590ec732c4665b5fed541adad672153cabc196d9938e16acf3c264b8d1921f1`。
- Shared fixture摘要：SSE `e8c2d5ebca2182b7b07ad30761c07b5986139f2ff8ec9bbbf9b4ecaae6d6a0e6`；consumer `5ad29b750693ecf95a0cabab4fe7c2ada6f6dbb9b10f9f99c3d5c25654d32cf1`；Host/Desktop逐字节一致。
- 本地checkpoints：Host `8707dea552cff74121b89aa8045f27da2c8c9378`；Desktop `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb`；均clean、未push。
- Owner结论：接受DEC-126-036，S9授权范围未发现残余P0/P1。G3继续Partial；该接受不授权S10、MiniMax、feature activation、真实数据、远端动作或四组件E2E。

### 9.12 DEC-126-037 / S10A Readiness Review（Accepted / Option C）

| Finding | Severity | 事实/证据 | 状态 |
|---|---|---|---|
| S10A-REV-001 | P1 environment | S10A观察到Docker存在但`docker compose`不可用；S10P0定位为stale link；S10E现已完成Compose discovery与isolated PostgreSQL/Keycloak/Caddy profile验证 | CLOSED BY DEC-126-039 |
| S10A-REV-002 | P1 provider | S10A原缺口已由LIA-126-009的exact/keyless loopback fake Responses、fixed fixture和Runtime turn证据覆盖 | CLOSED BY DEC-126-040 |
| S10A-REV-003 | P1 effective profile | S10A原缺口已由LIA-126-009的closed child allowlist、raw/cleanup=true/title=false、bounded logs和PID/run/nonce证据覆盖 | CLOSED BY DEC-126-040 |
| S10A-REV-004 | P1 data isolation | Chat DB/receipt与native-auth Keychain service/account固定，无test namespace | OPEN / stop condition |
| S10A-REV-005 | P1 chain integrity | Desktop无`/v2/tasks` production call；生成SDK不是consumer，空PostgreSQL rows不能证明content-free create | OPEN / stop condition |
| S10A-REV-006 | P2 title capability | Host title flag因Runtime无法capability-disable tools持续fail closed | DOCUMENTED LIMIT；S10只验fallback/user precedence |
| S10A-REV-007 | boundary | 本轮未安装/下载/启动任何服务，未开flag，未读写Keychain，未修改业务码，未调provider，未远端写 | CLOSED for S10A scope |

- 备选方案：S10A原建议补齐Compose；S10P0细化为可恢复地修复用户级link并使用摘要固定的bundled Compose v5，再建权威run-scoped profile。该方案已在S10E单独授权下执行并验证；不再把“已有PostgreSQL”作为等价替代。
- process/evidence冻结：端口为API 18080、Host 18081、fake Responses 18082、OIDC 8443、API edge 9443、Vite 1420/1421、PostgreSQL 5432，全部loopback；用例为S10B-001–012；证据只保留PID/SHA/nonce/count/hash/state/duration/failure class，不保留正文/secret/path/key。
- 结构化结论：Owner已接受DEC-126-037选项C与DESIGN-126-007，并继续HOLD S10B。DEC-126-039关闭BLK-001；DEC-126-040接受LIA-126-009/S10P1 Closure并正式关闭BLK-002/003。LIA-126-008仍为`Blocked Draft / NOT AUTHORIZED`，S10P2/P3仍须逐项明确授权。

### 9.13 DESIGN-126-008 / DEC-126-038 S10P0 Corrective Design Review（Accepted / Option B）

| Finding | Severity | 只读事实/设计处置 | 状态 |
|---|---|---|---|
| S10P0-REV-001 | P1 environment | Compose二进制并非缺失；用户plugin symlink指向失效AppTranslocation路径。Docker Desktop bundled v5.3.0摘要为`2642b635…d265`，direct read-only config/features PASS；官方说明v5与v2功能等价 | CLOSED BY DEC-126-039 |
| S10P0-REV-002 | P1 isolation | 新run-scoped profile只用三个pinned image digests、四个volumes和API-local CA pin，不启Redis/pgvector；runtime verifier PASS | CLOSED BY DEC-126-039 |
| S10P0-REV-003 | P1 provider/profile | Host默认MiniMax保持不变；exact master+run ID+loopback keyless Responses及Desktop child raw/cleanup=true/title=false已按LIA-126-009实现并全绿 | CLOSED BY DEC-126-040 |
| S10P0-REV-004 | P1 secure storage | 三个test Keychain service只从run ID派生，native-auth无legacy fallback，pre/post只检exact tuple状态，不枚举/读取真实Keychain | DESIGN FROZEN / historical S10P0 status；后续LIA-126-010结果见§9.16 |
| S10P0-REV-005 | P1 main chain | `29317b...`能表达content-free create/idempotency；候选SQLCipher v5绑定local/public/Host operation，先Public bind后Host start，提交独立closed control-plane command/channel | PRIVATE IPC CANDIDATE / S10P3 not authorized |
| S10P0-REV-006 | P1 deletion disclosure | contract明确permanent delete不在candidate；Owner已接受本地session delete不删PostgreSQL content-free Public Task row；未来若改变要求必须转G2A缺口 | DESIGN BOUNDARY ACCEPTED / implementation evidence pending S10P3 |
| S10P0-REV-007 | boundary | 六仓exact/clean开始；本轮只读并只修改FEAT-126治理文档；0 process/container/provider/flag/Keychain/DB/business-source/remote writes | CLOSED for S10P0 scope |

只读环境摘要：Docker CLI=`29.6.1`；bundled Compose=`v5.3.0`、size=`30,780,320`、SHA-256=`2642b6354b323be90cf28460ac186499fbc85381b9ce5e6681fdefb2d0a7d265`；现有Infra固定Keycloak=`0f198be…b13`、PostgreSQL=`4e6e670…d50`、Caddy=`5f5c864…58648`，Compose/Caddy/profile/script摘要已记录于S10P0 working evidence。本轮仅运行二进制version/config/help等静态命令，未使用daemon状态作实施证据。

Contract impact结论：S10P0自身`none`；S10E为Infra/deployment-only；S10P1为Host/Desktop private deployment config additive；S10P2为Desktop private storage config additive；S10P3为Desktop semantic orchestration + SQLCipher v5 + additive private IPC，central Public Tasks/Host wire与Runtime pin仍`none`。这些分类只是设计候选，不授权代码变更。

结构化结论（S10P0评审时点）：Owner已接受DESIGN-126-008和DEC-126-038方案B，包括Public Task retained-row边界；DEC-126-039随后接受S10E Closure并关闭BLK-001，DEC-126-040接受S10P1 Closure并关闭BLK-002/003。该时点S10P2/P3/S10B/S11为`NOT AUTHORIZED / NOT RUN`；之后LIA-126-010的S10P2执行结果见§9.16。LIA-126-008仍Blocked Draft，G3 Partial、G4/G6 Pending。

### 9.14 DEC-126-039 / S10E Closure Review（Accepted / Option A）

| Finding | Severity | 实际证据 | 状态 |
|---|---|---|---|
| S10E-REV-001 | P1 environment | current-user Compose discovery恢复为bundled v5.3.0；size/SHA/config/profiles/services/`--wait`精确PASS；旧link在owner-only备份 | CLOSED / ACCEPTED |
| S10E-REV-002 | P1 isolation | explicit default-off profile；4 exact-digest services、4 project volumes、4 project networks；API DB/Caddy只bind loopback；无host/shared network、普通DB/volume复用 | CLOSED / ACCEPTED |
| S10E-REV-003 | P1 migration/identity | API exact SHA对empty dedicated DB执行00001–00004到v4，second run no-op；synthetic users连续两次provision；OIDC issuer/TLS/public CA exact | CLOSED / ACCEPTED |
| S10E-REV-004 | P1 no-log/security | fresh run runtime verifier检查exact image/health/labels/security/resources/ports；generated secret在container logs和candidate files命中0 | CLOSED / ACCEPTED |
| S10E-REV-005 | P1 cleanup | 两次run停止后container/network/listener=0；未做未授权volume/prune删除 | CLOSED / ACCEPTED WITH DISCLOSED RETENTION |
| S10E-REV-006 | P1 evidence integrity | 初始diagnostic run发生synthetic credential process-output展开，整轮证据作废；fresh run重新生成全部Gate；污染run有owner-only `REJECTED` marker且config/provision/migration/verify均fail closed | CLOSED / ACCEPTED |
| S10E-REV-007 | boundary | MiniMax/外部provider=0、Keychain=0、业务四组件=0、flag=0、远端写入=0；contracts/Runtime/API/Host/Desktop业务源码不变 | CLOSED FOR S10E SCOPE |

Infra checkpoint为`99e50d8b47e13fc3e3b7501617a307e1ba5d6baf`，parent=`f040492e7c4af4aa7cc94a343140c58befae3af2`，local branch clean且未push。Infra static gate为80/80；fresh runtime/migration/identity/TLS/no-log及rejected-run fail-closed均PASS。

停止后的八个named volumes与两个owner-only ignored run root是明确披露的保留物：它们没有active container/network/listener，删除仍需单独Owner授权。Owner已按DEC-126-039方案A只接受S10E并关闭BLK-001；该决定不授权S10P1或S10B。

### 9.15 DEC-126-040 / S10P1 Closure Review（Accepted / Option A）

| Finding | Severity | 实际证据 | 状态 |
|---|---|---|---|
| S10P1-REV-001 | P1 provider config | exact master、canonical run UUID、fixed IPv4 loopback/port/path、local/raw+cleanup/title、parent PID/log manifest、MiniMax key冲突均有正负测试 | CLOSED / OWNER ACCEPTED |
| S10P1-REV-002 | P1 fake protocol | frozen S9 dataset SHA、complete/incomplete/http-error/disconnect/oversize、request/call cap、no reflection/content-free counters | CLOSED / OWNER ACCEPTED |
| S10P1-REV-003 | P1 Runtime | fixed Runtime artifact实际产生assistant与raw reasoning delta/final并完成turn/delete；未用key/外网 | CLOSED / OWNER ACCEPTED |
| S10P1-REV-004 | P1 effective child profile | `env_clear` closed allowlist，raw/cleanup=true、title=false，PID/run/nonce readiness；wrong nonce/port、crash/restart/stale fail closed | CLOSED / OWNER ACCEPTED |
| S10P1-REV-005 | P1 evidence/no-log | 0700 directories、0600 files、256 KiB cap、content-free manifest、unique atomic temp；raw/secret/path/bearer/DB-key covered hits=0 | CLOSED / OWNER ACCEPTED |
| S10P1-REV-006 | boundary | private IPC/TS/Vue/contracts/Public Tasks wire/DB schema/Runtime pin/default config均未变；MiniMax/external/Keychain/real data/remote actions=0 | CLOSED FOR S10P1 SCOPE |

结构化结论：两个本地checkpoint均clean且未push；Owner选择DEC-126-040方案A，接受S10P1 Closure并正式关闭BLK-002/003。BLK-004/005仍Open；本Review不授权S10P2/P3/S10B/S11或默认activation。

### 9.16 DEC-126-041 / S10P2 Closure Review（Option B Accepted / Closure HOLD）

| Finding | Severity | 实际证据 | 状态 |
|---|---|---|---|
| S10P2-REV-001 | P1 default compatibility | 独立secure-storage与master双exact gate；master-only/default/false固定namespace回归；`.env`/CI/build defaults无启用值 | CLOSED IN SOURCE |
| S10P2-REV-002 | P1 namespace/legacy | 三service由canonical UUID派生；native-auth test store不构建legacy entry；WebView/TS/shell不能给service/account | CLOSED IN SOURCE |
| S10P2-REV-003 | P1 manifest/path authority | temp-root/owner/0700/non-symlink、固定directory roles、Host/CODEX/project精确匹配、0600 closed manifest | CLOSED IN SOURCE |
| S10P2-REV-004 | P1 inventory/no-secret | exact attribute-only search；只返回3 role的state/schema-valid与SHA；无enumeration/get_secret/hash/path/service正文 | CLOSED IN SOURCE |
| S10P2-REV-005 | P1 cleanup/recovery/race | pre-present拒绝、stale PID、same-run retry、cross-run disjoint、interrupted cleanup、missing idempotency、mismatch delete=0、root exact delete | CLOSED IN SOURCE |
| S10P2-REV-006 | P1 native lifecycle | random Protected Data create/use/restart/delete probe | **OPEN / ENVIRONMENT BLOCKED**：required entitlement missing；0 signing identities |
| S10P2-REV-007 | boundary | SQLCipher schema/private IPC/TS/Vue/contracts/Host/API/Runtime/dependencies/default flags/remote均未改 | CLOSED FOR SOURCE SCOPE |

结构化结论：Desktop checkpoint clean且未push；仓内source P1均关闭，但原生create/use/restart/delete是BLK-004的不可豁免证据。Owner已接受DEC-126-041 Option B，只接受source checkpoint并保持Closure HOLD；不得把该决定写成BLK-004 Closed，也不得授权S10P3/S10B。

批准后的native signing readiness复验：canonical bundle为`com.yijie.ai`；`security find-identity -v -p codesigning`为0；`profiles show -type provisioning`确认没有已安装profile；仓库无macOS entitlements/embedded profile；active developer directory只有Command Line Tools。因此无法验证Team Identifier/Application Identifier Prefix，也不能安全形成effective keychain access group。此次复验只读，新增certificate/CSR/profile/entitlements/Keychain item均为0，Protected Data write attempt保持2，Desktop仍为`c863b2a…5dc68` clean。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| VoiceOver manual verification | DEC-126-034已接受S8B自动化/browser Closure证据，但VoiceOver人工清单尚未执行 | 若把Closure接受写成真人VoiceOver通过会夸大a11y证据 | 保留到S11/G6 Owner本地验收并记录实际结果 | 段成威 | does not reopen S8B Closure；blocks corresponding manual G6 claim |
| Draft PR dependency audit / merge approval | PR #1 exact head CI在`brace-expansion 2.1.2` high失败；candidate本身未改依赖；后续`govulncheck`与`origin/main` breaking未运行 | 若豁免红灯会留下已知high dependency并缺两项远端证据 | DEC-126-021 Accepted/HOLD；保持Draft，不rerun/waive/fix/push；未来需本地E2E、audit修复、全绿CI与单独Owner批准 | 段成威 | blocks merge only；不阻断未来明确批准的local draft implementation |
| Public/Host runtime conformance | S4–S8B分层实现与S9 Host→Desktop exact fixture/SQLCipher/plaintext consumer Eval PASS | 真实多进程链仍可能产生scope/raw/cleanup disagreement | S10须另行授权；保持flags off | 段成威 | blocks G4/local G6, not S9 Closure candidate |
| DB/encryption/delete E2E | SQLCipher v4 job/receipt、independent HMAC key、migration/cascade/checkpoint、restart和fake Host cleanup单仓PASS | 跨Desktop/Host/Runtime真实进程partial delete仍未运行 | S10验证完整多进程job/receipt/restart/fault E2E | 段成威 | blocks G4/local G6 |
| Runtime raw-reasoning/title/delete | S9 deterministic Eval与S10P1 Host→fixed Runtime assistant/raw真实turn PASS；完整Desktop turn/history/delete多进程链仍未运行 | raw UX/residual/inconsistent history | keep default flags off until S10B；历史MiniMax public-summary FAIL不改写 | 段成威 | blocks G4/local G6 |
| Desktop sidecar/Keychain | actual Desktop supervisor→Host→fixed Runtime child readiness/stop PASS；run-derived隔离源码与exact inventory/cleanup PASS；DEC-126-041 Option B Accepted | signed storage create/use/restart/delete因本机无identity/profile/entitlement未验证 | 提供匹配`com.yijie.ai`及team/access-group的Apple Development identity/provisioning，只重跑native matrix并重新提交S10P2 Closure | 段成威 | blocks BLK-004/S10P3/S10B/G4/local G6 |
| S10B test profile/chain readiness | BLK-001/002/003 closed；BLK-004 source ready但native proof blocked；BLK-005仍缺Desktop Public Tasks主链 | 直接启动完整链仍无法建立signed Keychain与Public Tasks主链证据 | 关闭BLK-004并另行授权/关闭S10P3与BLK-005，再重新提交LIA-126-008 | 段成威 | blocks S10B/G4/local G6；does not reopen earlier closures |
| production identity/infra | FEAT-125 deferred | no production safety | N/A for DEC-126-022 local-only scope；future online intent must reopen production track and FEAT-125 prerequisites | 段成威 | does not block local G6；blocks any production claim |

## 11. 结论

- Requirements package：G1/G2/G2A Re-review Passed；DEC-126-023–041 Accepted。DEC-126-039关闭BLK-001，DEC-126-040关闭BLK-002/003；DEC-126-041接受S10P2 source checkpoint但保持Closure HOLD，native proof blocked、BLK-004 Open；DEC-126-037方案C继续HOLD S10B。
- Code Complete：No。G3仍Partial；S10P2 Closure、S10P3/S10B–S11、四组件E2E、G4与Owner G6均未完成。
- 验证人：Codex（文档事实与结构）；最终 Reviewer 为段成威。
- 日期：2026-08-04。
- 结论依据：S4–S9 accepted链、七仓fixed baseline、Runtime artifact digest、S10E/S10P1 accepted证据，以及S10P2 Desktop checkpoint、仓库全量门禁、exact pre/post inventory和明确的entitlement失败。S10P2无MiniMax/外部provider、真实数据、API/Host/Runtime/central contract/private IPC/DB schema/TS/Vue修改、default activation、push/merge/tag/publish/deploy或生产证据。
