# FEAT-126 验证证据与独立审查报告

> LIA-126-002第二轮独立审查曾把S4–S6从Complete调整为`Conditional / Corrective Closure Required`。
> DEC-126-025现已完成Remote State Reconciliation：sole candidate与yijie/API/Host/Desktop checkpoint
> 分支均已精确远端可达，旧Draft PR #1与各`origin/develop`不变。DEC-126-026已接受S4–S6
> Foundation Corrective Closure并单独授权S7A Desktop Rust Host Bridge/Domain；DEC-126-027已由
> Owner接受。随后单独授权的S7B Rust Application Orchestration/Domain已完成并由Owner通过DEC-126-028接受；远端可达不等于merge、发布或生产启用。
> 随后Owner接受S7C–S9及S10E/P1/P2F/P3/S10BD1/S10BF1/S10BRP1 Closure。DEC-126-062/063关闭BLK-007并形成Infra/Governance clean checkpoints后，Owner单独授权并消费LIA-126-024/S10B-R7。R7的S10B-001 PASS，但S10B-002因七仓不存在完整四组件可执行orchestrator而在任何continuation/业务进程启动前fail closed；003–011未运行，012仅完成abort cleanup subset。Owner已接受DEC-126-064/065/066并完成DESIGN-126-014、LIA-126-025/S10BO1 Corrective Closure及`S10B-BLK-008`关闭；DEC-126-067进一步形成API/Host/Desktop/Infra/Governance本地clean checkpoints。G3仍Partial，G4/G6 Pending，isolated live与S11未授权。
> 随后Owner接受S7C–S9及S10E/P1/P2F/P3/S10BD1/S10BF1/S10BRP1 Closure。DEC-126-062/063关闭BLK-007并形成Infra/Governance clean checkpoints后，Owner单独授权并消费LIA-126-024/S10B-R7。R7的S10B-001 PASS，但S10B-002因七仓不存在完整四组件可执行orchestrator而在任何continuation/业务进程启动前fail closed；003–011未运行，012仅完成abort cleanup subset。Owner已接受DEC-126-064/065/066并完成DESIGN-126-014、LIA-126-025/S10BO1 Corrective Closure及`S10B-BLK-008`关闭；DEC-126-067进一步形成API/Host/Desktop/Infra/Governance本地clean checkpoints。随后LIA-126-027 isolated live 保留为不可复用的 fail-closed 历史事实，Owner已接受DESIGN-126-016与LIA-126-028/S10BO3 Corrective Closure并关闭`S10B-BLK-010`。G3仍Partial，G4/G6 Pending，新的isolated live、fresh R8与S11未授权。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | `feat/feat-126-foundation-closure` | R5 execution baseline `fdc4659a999768819d0f55c3fcc8098766240250` | clean before S10B-R5；only accepted FEAT-126 governance；local/not pushed | zsh/macOS；feature package checker | 2026-08-05 Asia/Shanghai |
| yijie-infra | `feat/feat-126-s10e` | S10BD1 checkpoint `2a643caef210e32cab80242ede46b96927b2097a` | clean before S10B-R4；contains accepted bootstrap/image/API-authority corrections plus capability-first immutable resolver；local/not pushed | Docker Desktop 4.82.0 / Engine 29.6.1 / Compose 5.3.0；Node/pnpm | 2026-08-05 Asia/Shanghai |
| yijie-api | `feat/feat-126-foundation-closure` | checkpoint `c5f334e88d54d9e04f388d0349f4f5925124abd6` | clean before S10B-R2；closed profile/batch/verifier committed locally/not pushed | Go 1.26.5 + isolated PostgreSQL 16.13 | 2026-08-05 |
| yijie-agent-host | `feat/feat-126-foundation-closure` | S10P1 local checkpoint `e0a8d3d29a335571d1654d95e1e262c240755674`；parent S9 `8707dea552cff74121b89aa8045f27da2c8c9378` | clean；15-file S10P1 private test profile/fake authority/watchdog diff；not pushed | Go 1.26.5 + deterministic fake Responses + fixed Runtime | 2026-08-04 |
| yijie-desktop | `feat/feat-126-foundation-closure` | S10P3 local checkpoint `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；parent S10P2F `46107eec1e9cba0257252cae8678a4233ef20036` | clean；24-file SQLCipher v5/Public Tasks/private projection diff；not pushed | Node 26/pnpm 11/Rust 1.95/SQLCipher；no Keychain access | 2026-08-04 |
| yijie-contracts | `feat/feat-126-content-free-candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` local/remote exact | clean；unchanged during review | locked generators | 2026-08-03 |
| yijie-codex | `develop` | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | clean；unchanged | Runtime 0.144.6；binary `1ef4f1…8df1fe`；manifest `2560a3‧6682` | 2026-08-04 |

最终S10BO1 Closure复验固定Governance `3d82cda4c3c06928e0111bc1697b0153e8ef76a2`、Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`及Infra `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；Contracts/Runtime clean，其他仓库仅含已授权S10BO1 corrective或九份FEAT-126治理改动。

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
| LIA-126-011 / S10P2F | Desktop `46107eec1e9cba0257252cae8678a4233ef20036` | double-exact selector、CSPRNG三role、closed file/manifest validation、SQLCipher/native-auth restart、cross-run/lease/fault/exact cleanup、full repository/security gates | 0 final | CLOSURE PASS / DEC-126-043 OPTION A ACCEPTED | 6 Rust files；19 targeted pass/1 native ignored；124 full pass/2 native ignored；165 TS；0 Keychain/MiniMax/real-data/remote write；Local-only BLK-004 Closed |

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
| V-DEC-126-042-GOV | yijie | feature package default/`--strict`/`--gate G2A`；YAML parse；`pnpm lint`；`pnpm test`；checker `bash -n`；`git diff --check`；scope/personal-path scan | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | 候选与批准登记轮的8个指定FEAT-126治理文件均通过package/strict/G2A/YAML/lint/test/shell/diff；0 FEAT-123/unrelated/personal-path。Owner现已接受DEC-126-042设计；该PASS仍不代表BLK-004关闭或S10P2F授权 |
| V-S10P1-HOST | yijie-agent-host `e0a8d3d29a335571d1654d95e1e262c240755674` | `make lint`；`make contract-check`；`make test`；`go build`；fake protocol/default config/parent-watchdog/security/diff checks | Go 1.26.5 | 0 | PASS 2026-08-04 | full race/coverage PASS；fake Responses 79.8%、codex 71.0%、app 68.9%、session 77.6%；exact profile、key conflict、nonloopback、parent exit、incomplete/error/oversize PASS |
| V-S10P1-RUNTIME | Host parent `8707dea…c9378` + S10P1 diff + Runtime `3aa317ce…5d6f` | opt-in `TestPinnedRuntimeFEAT126FakeResponses` with fixed binary/manifest and `127.0.0.1:18082` | fixed codex-cli 0.144.6 | 0 | PASS 2026-08-04 | assistant/raw delta+final、item/turn complete、thread delete；fake accepted=1/rejected=0；external/MiniMax call=0 |
| V-S10P1-DESKTOP | yijie-desktop `fba934c524852719904657d0a4155142040e7285` | `make lint`；`make test`；`make build`；`cargo build`；actual fixed Host child integration；security/diff checks | Node 26 / pnpm 11 / Rust 1.95 | 0 | PASS 2026-08-04 | TS 30/165；Rust 101 pass/1 existing ignored；env allowlist、pre-spawn evidence、PID/run/nonce、0700/0600/256KiB logs、crash/restart/stale/stop PASS |
| V-S10P1-SCOPE | Host/Desktop/yijie | per-repo status/diff/name scan；`.env`/CI/default config、IPC/TS/Vue/contracts/wire/schema/pin and no-log/bbolt/process evidence scan | Git/rg/tests | 0 | PASS 2026-08-04 | 0 MiniMax/external/Keychain/real-data/remote write；0 raw/secret/path/bearer/DB-key covered hits；default flags unchanged |
| V-S10P2-DESKTOP | yijie-desktop `c863b2ab30d185201bff5736a308d7078ee5dc68` | `make lint/test/build`；`cargo build --locked --all-targets`；targeted secure-storage tests；source/bundle/diff scans | Node 26 / pnpm 11 / Rust 1.95 | 0 | PASS 2026-08-04 | TS 30 files/165；Rust 113 pass/0 fail/2 signed probes ignored；12 S10P2 unit tests PASS；no dependency/schema/IPC/TS/Vue/default-config change |
| V-S10P2-NATIVE | random run-derived three exact tuples | sandbox-exempt explicit signed-bundle probe + exact inventory/cleanup | unsigned Rust test binary / macOS Protected Data | non-zero expected blocker | **BLOCKED** | pre/post three tuples absent；cleanupComplete=true；temp roots=0；first write failed `required entitlement isn't present`；codesigning identities=0；no default/legacy/foreign tuple touched |
| V-S10P2-SECURITY | Desktop source/artifacts | exact-gate/default namespace/manifest/no-log/path/secret/bundle/lockfile scans；RustSec offline；pnpm audit | Git/rg/cargo-audit/pnpm advisory | mixed | PASS for source boundary / dependency follow-up | new Rust logging/bundle secret hits=0；RustSec 0 unallowed/17 allowed；pnpm reports pre-existing dev-tool `brace-expansion 5.0.8` high (patched ≥5.0.9), no lockfile change in this slice |
| V-S10P2F-TARGETED | yijie-desktop `46107eec1e9cba0257252cae8678a4233ef20036` | isolated subprocess truth table + targeted `feat126_secure_storage`/chat/native-auth tests | Rust 1.95 / temp owner-only roots / synthetic secrets | 0 | PASS 2026-08-04 | 20 tests: 19 pass/0 fail/1 signed-native ignored；covers S10P2F-001–012 including real SQLCipher reopen and exact cleanup |
| V-S10P2F-RUST | yijie-desktop `46107eec1e9cba0257252cae8678a4233ef20036` | `cargo test --all-targets` outside sandbox；`cargo fmt --check`；`cargo check --all-targets`；`cargo clippy --all-targets -- -D warnings`；`cargo build --all-targets` | Rust 1.95 / SQLCipher | 0 | PASS 2026-08-04 | full 126 tests: 124 pass/0 fail/2 signed-Keychain ignored；no warning/error |
| V-S10P2F-TS-BUILD | yijie-desktop `46107eec1e9cba0257252cae8678a4233ef20036` | `pnpm generate:check`；`pnpm lint`；`pnpm test`；`pnpm build` | Node 26 / pnpm 11 | 0 | PASS 2026-08-04 | exact contracts SHA；30 files/165 tests；production bundle builds and contains no ephemeral selector/basename/test harness |
| V-S10P2F-SECURITY | Desktop source/artifacts/temp root | RustSec、`pnpm audit --prod`、source/bundle/log/process/path/secret scans、`git diff --check`、post-temp inventory | cargo-audit/pnpm/rg/find/Git | 0 for implementation gates | PASS WITH DISCLOSED P2 | RustSec 0 vulnerabilities + 17 allowed pre-existing warnings；one pre-existing moderate PostCSS advisory, no dependency/lock change；covered leak hit=0；matching temp root count=0 |
| V-S10P2F-SCOPE | Desktop/yijie | diff/name/config/IPC/schema/TS/Vue/Host/API/Runtime/contracts/pin scan | Git/rg | 0 | PASS | Desktop only 6 Rust files；no dependency, DB migration, IPC, TS/Vue, default flag, external provider or remote mutation |
| V-S10P2F-GOV | yijie | feature package default/`--strict`/`--gate G2A`；YAML parse；`pnpm lint`；`pnpm test`；checker `bash -n`；`git diff --check`；8-file scope/FEAT-123/personal-path/secret scan | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-04 | implementation-candidate and Owner-acceptance reconciliation both pass；DEC-126-043 Accepted，BLK-004 Closed；0 unrelated/remote action |
| V-DEC-126-045-APPROVAL | yijie | Owner approval reconciliation；feature package default/`--strict`/`--gate G2A`；YAML parse；`pnpm lint`；`pnpm test`；shell `bash -n`；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | DEC-126-045 Option A、S10P3 Closure Passed与BLK-005 Closed已同步至8个治理文件；该决策当时保持LIA-126-008/S10B HOLD，后续由单独Owner批准解除；0业务源码或远端动作 |
| V-LIA-126-008-AUTHORIZATION | yijie | Owner authorization reconciliation；feature package default/`--strict`/`--gate G2A`；YAML parse；`pnpm lint/test`；shell；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | LIA-126-008 marked AUTHORIZED / NOT RUN；scope limited to S10B-001–012 and frozen local profile；G3 Partial、G4/G6 Pending；no process/flag/model/business-code/remote action |
| V-S10B-FIRST-RUN | isolated run `9b9d455f-0500-4dd0-a008-d5a862bf6f20` | exact baselines/Runtime/ports；S10E init/config/up/export-ca/verify/provision/migrate；四份tracked bootstrap manifests；DB count reconciliation；stop/active-resource scan | Docker 29.6.1 / Compose 5.3.0 / Go 1.26.5 / fixed repos | non-zero at bootstrap gate | **FAIL-CLOSED 2026-08-05** | dependencies/TLS/OIDC/users/migration PASS；`feat-125-local-lab` profile拒绝`yijie_api_feat126_s10`；migration=4、users/tenants/memberships=0/0/0；S10B-001 FAIL，002–012 NOT RUN；0 API/Desktop/Host/fake/Runtime/MiniMax/Keychain/real-data/remote write |
| V-S10B-ABORT-CLEANUP | same run | authoritative Infra stop；container/network/port inventory；temporary binary root removal | Docker/lsof/Git | 0 | PASS FOR ABORTED RUN | active containers/networks/listeners=0/0/0；temp binary root removed；4 named volumes + owner-only ignored run record retained；no volume deletion |
| V-S10B-GOV | yijie | feature package default/`--strict`/`--gate G2A`；YAML parse；`pnpm lint/test`；checker `bash -n`；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | original eight-file overlay recorded DEC-126-046 Candidate and S10B-BLK-001；Owner has now accepted Option A without accepting Closure；no checkpoint/push |
| V-S10BP0-SOURCE | API/Infra read-only | profile constants/DSN validators/CLI ordering、四manifest、transaction/idempotency tests、S10E Make/scripts inventory | rg/sed/git | 0 | PASS 2026-08-05 | validation order=`profile → manifest → migration/DB`；2x2 matrix与8 audits authority confirmed；0 source/process mutation |
| V-S10BP0-GOV | yijie | current feature checker default/strict/G2A、YAML parse、pnpm lint/test、checker syntax、diff | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | DESIGN-126-009、DEC-126-046 Accepted、DEC-126-047 Candidate、LIA-126-013 NOT AUTHORIZED；首次按历史短路径调用返回127，定位当前`docs/dev/codex-feature-delivery/scripts/check-feature-package.sh`后default/strict/G2A与syntax均exit 0；本轮不commit/push |
| V-DEC-126-047-APPROVAL | yijie | Owner approval reconciliation；feature package default/strict/G2A、YAML、pnpm lint/test、checker syntax、diff/scope | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | all eight gates exit 0；DEC-126-047 Option A Accepted；LIA-126-013/S10BP1、S10B rerun与S11保持NOT AUTHORIZED；0 business source/process/remote action |
| V-S10BP1-API | yijie-api local diff over `a64f9f591fb594818c1778e30c6941e2574b3264` | gofmt；`make lint`；`make test`；`make generate-check`；targeted profile/batch/verifier tests | Go 1.26.5 | 0 | PASS 2026-08-05 | exact profile/matrix、pre-storage rejection、atomic batch、closed verifier；full race/unit green；existing contract generation current |
| V-S10BP1-INTEGRATION | fresh isolated PostgreSQL 16.13 | migration up/status v4；`go test -race -tags=integration ./internal/platform/nonprodbootstrap`；权威wrapper via temporary clean candidate | PostgreSQL/Go/local pinned image | 0 | PASS 2026-08-05 | pre all-zero；post `2 users/2 identities/2 tenants/4 memberships/4 roles/18 role_permissions/4 assignments/8 audits`；4 changed+4 unchanged；audit-failure injection rolls all tracked tables to zero |
| V-S10BP1-INFRA | yijie-infra local diff over `8d7c84dc963141931c6c5d3c3aded3218247df0b` | `pnpm test`；`scripts/plan.sh`；`bash -n`；Node check；wrapper live run | Node/pnpm/Docker 29.6.1/Compose 5.3.0 | 0 | PASS 2026-08-05 | 83/83 tests；fixed SHA/clean/profile/four paths；two API-owned atomic passes；0600 content-free summaries；no business SQL |
| V-S10BP1-CLEANUP | exact temporary run | stop/remove single PostgreSQL container+anonymous volume；delete temporary candidate and generated secret；container/secret inventory | Docker/filesystem | 0 | PASS | no temporary container/candidate/secret remains；only three 0600 content-free JSON summaries retained in ignored run evidence |
| V-S10BP1-S10E-PREFLIGHT | accepted S10E helper + local image inventory | `docker images --digests --no-trunc` then helper/exact `docker image inspect tag@digest` | Docker 29.6.1 | non-zero historical | **BLOCKER OBSERVED / OUTSIDE S10BP1** | local image ID/digest exactly `4e6e670…10d50`, but tag and tag@digest inspect曾返回`No such image`；重启Docker后恢复，确认状态敏感；后续由S10BR1单独纠偏 |
| V-S10BR1-INFRA | yijie-infra local diff | `node --check`；`bash -n`；`pnpm test`；`pnpm validate`；security/diff scan | Node/pnpm | 0 | PASS 2026-08-05 | 85/85；3 unique repository digests；malformed/conflict/missing/identity/descriptor negatives；no pull/floating fallback/volume delete |
| V-S10BR1-LIVE | fresh compatibility run `ae1c892a-4819-40bc-9ce9-d72f6ea2fcd7` | exact local verifier；accepted config/up `--pull never`；authoritative stop；resource inventory | Docker 29.6.1 / Compose 5.3.0 | 0 | PASS 2026-08-05 | 3 exact identities；4 dependencies healthy；pull=0；after stop containers/networks=0；4 named volumes + owner-only ignored record retained；not S10B |
| V-S10BM1-INFRA | yijie-infra `bb96333df908d6fea72ec0a1f57a64477c2428e4` | shared API authority unit/negative matrix；`pnpm validate`；`make lint/test`；Node/shell syntax；diff | Node/pnpm/Git | 0 | PASS 2026-08-05 | 87/87；migration/bootstrap one full clean SHA；wrong/dirty/drift/corrupt/mode/symlink/hardlink fail closed before secret/DB；private old CLI intentionally rejected；not S10B |
| V-S10BM1-GOV | yijie accepted closure checkpoint `441663faf7d505015f03d572c8e9f30b3ba1a2df` | feature package default/strict/G2A；YAML parse；`pnpm lint/test`；checker syntax；diff | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | DEC-126-052 Option A Accepted；BLK-003 Closed；checkpoint clean/local/not pushed；subsequent LIA-126-016 approval does not rewrite this SHA |
| V-S10B-R4-GOV | yijie governance overlay over `02cf06b2993ee18aefe4b7e4d6d40e2d19b2c4c1` | feature package default/strict/G2A；unique-key YAML；`pnpm lint/test`；checker syntax；`git diff --check` | project scripts / Node / pnpm / Git | 0 | PASS 2026-08-05 | LIA-126-018 consumed；S10B-001 fail closed；S10B-BLK-005 Open；DEC-126-056 later Accepted；002–012/S11/MiniMax NOT RUN；no source or remote write |
| V-S10BF1-CLOSURE | Host `1ca4ee5…a560` + Infra `5723ffd…c0c9` + Governance baseline `db12fe6…cc4d` | Host full race/contract/lint；Infra 103 tests/validate/lint；fresh single-runner S10B-001 combined preflight；no-log/cleanup/default-off | Go 1.26.5 / Node 26 / Docker 29.6.1 / Compose 5.3.0 | 0 | PASS 2026-08-05 | run `ed22fc82…f3f4`；summary `8198442e…f7d9`；dataset/case explicit；0 process/container/network/listener；4 volumes disclosed；Docker restored stopped；R5=false；DEC-126-057 Accepted / BLK-005 Closed |
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
| remaining AC/NFR | S10B–S11 | S10B-001–012 matrix in `05/06` | LIA-126-008/014/016 consumed；LIA-126-015 corrective complete | all three runs stopped at 001；BLK-001/002/003 Closed、004 Open；R3 Closure Fail；S11 NOT AUTHORIZED |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| Local four-component E2E | API/Host/Desktop/pinned Runtime create/stream/raw/history/actions/delete/restart | S4–S9 foundations/Eval + accepted S10E/S10P1/S10P2F/S10P3/S10BP1/S10BR1 | EXECUTED / BLOCKED / CLOSURE FAIL | first S10B-001 fail closed；002–012 NOT RUN；BLK-001/002 later Closed；fresh full rerun still blocks G4/Local-only G6 |
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
- P0/P1 是否清零：对已实现并接受的S4–S10P3范围为是。S10A发现的5个readiness P1已由DEC-126-039/040/043/045关闭；S10B现已授权但尚未运行，因此G4/G6仍未通过。
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

结构化结论：两个本地checkpoint均clean且未push；Owner选择DEC-126-040方案A，接受S10P1 Closure并正式关闭BLK-002/003。当时BLK-004/005仍Open；DEC-126-043后来关闭BLK-004。本历史Review不授权S10P2/P3/S10B/S11或默认activation。

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

### 9.17 DEC-126-042 Local-only Secure Storage Adjustment Review（Accepted / Option A，历史设计门禁）

| Finding | Severity | 设计证据/停止条件 | 当前状态 |
|---|---|---|---|
| S10P2F-REV-001 | P1 default isolation | S10 master与`YIJIE_FEAT126_S10_EPHEMERAL_SECRET_BACKEND_ENABLED`均须exact `true`；任一不成立时不得创建/读文件，production/default只走Protected Data Keychain | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-002 | P1 secret generation/storage | 三个固定role只用OS CSPRNG合成secret；0700 root/dir、0600 file、create-new/O_EXCL/O_NOFOLLOW、owner/nlink/canonical/schema校验；禁止固定/run-ID/env派生 | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-003 | P1 restart/cross-run | 同run Desktop重启必须恢复原secret；不run不能读/写/删对方数据；manifest/symlink/mode/owner/nlink任一异常fail closed | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-004 | P1 cleanup/recovery | cleanup只能在停Desktop/Host/Runtime、关SQLCipher后unlink本run manifest的三个exact files；missing幂等；未知/foreign/mismatch时delete=0；crash/interruption可恢复 | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-005 | P1 no-log/no-WebView | secret不得进logs、process output、evidence、Git、bundle或WebView；shell/TS/Vue不得指定文件/path | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-006 | P1 native disclosure | signed Protected Data只转为`Deferred Native Hardening / NOT RUN`，未来native signing/production activation前必须恢复为强制Gate；不得写成PASS/豁免/等价 | HISTORICAL DESIGN FROZEN；见§9.18实现结果 |
| S10P2F-REV-007 | boundary | 不改central contracts、Public Tasks/Host wire、private IPC、TS/Vue、SQLCipher业务schema、API/Host/Runtime pin、default config；如需触碰则重开安全/G2 | CENTRAL G2A N/A / STOP CONDITION FROZEN |

- 批准基线：Governance `35cbf8e75f5ad88d392d164cb529ee5789e52667`；Desktop `c863b2ab30d185201bff5736a308d7078ee5dc68`；contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、Host/API/Runtime/Infra pins不变。
- 影响：`semantic`仅限Desktop-private local-test storage/deployment semantics与Local-only BLK-004退出条件；central contracts/G2A重审=N/A。
- DEC-126-042评审轮只修改治理文档；Desktop与其他业务仓当时保持clean/unchanged。随后LIA-126-011被Owner单独授权，其证据见§9.18；该后续实施不改写本历史事实。
- 结构化结论：Owner正式接受DEC-126-042 Option A与安全/G2设计；DEC-126-041继续作为历史source/entitlement事实保留。LIA-126-011随后执行，DEC-126-043 Option A现已接受并关闭Local-only BLK-004。

### 9.18 DEC-126-043 / S10P2F Closure Review（Accepted / Option A）

| Finding | Severity | 实现与证据 | 当前状态 |
|---|---|---|---|
| S10P2F-REV-001 | P1 default isolation | 双exact selector由隔离子进程真值表覆盖；孤立/冲突selector fail closed；protected schema v1/default路径不变 | CLOSED / OWNER ACCEPTED |
| S10P2F-REV-002 | P1 generation/storage | OS CSPRNG三role；0700/0600；O_EXCL/O_NOFOLLOW；euid/mode/nlink/inode/device/canonical/role/length/schema全校验 | CLOSED / OWNER ACCEPTED |
| S10P2F-REV-003 | P1 restart/cross-run | 同run SQLCipher reopen、receipt/native-auth恢复与rotate通过；cross-run、active lease、manifest/permission fault拒绝 | CLOSED / OWNER ACCEPTED |
| S10P2F-REV-004 | P1 cleanup/recovery | 全target先验证、只unlink三个exact files、missing幂等、unknown/mismatch delete=0、verified-empty non-recursive root删除 | CLOSED / OWNER ACCEPTED |
| S10P2F-REV-005 | P1 no-log/no-WebView | source/bundle/log/process/evidence/path/secret扫描0命中；selector/path不进入TS/Vue/Host；最终temp root=0 | CLOSED / OWNER ACCEPTED |
| S10P2F-REV-006 | P1 native disclosure | 两项signed Keychain测试继续ignored；Keychain访问0；明确`Deferred Native Hardening / NOT RUN` | CLOSED FOR LOCAL-ONLY DISCLOSURE；NATIVE FUTURE GATE OPEN |
| S10P2F-REV-007 | boundary | 仅6个Rust文件；无schema/IPC/TS/Vue/API/Host/Runtime/contracts/dependency/default config或remote变化 | CENTRAL G2A N/A / STOP CONDITION NOT TRIGGERED |

- Desktop checkpoint：`46107eec1e9cba0257252cae8678a4233ef20036`，parent=`c863b2ab30d185201bff5736a308d7078ee5dc68`，clean、local-only、not pushed。
- 逐仓结果：targeted 19 pass/1 native ignored；全量Rust 124 pass/2 native ignored；TS 165；generate/lint/build/fmt/check/clippy/RustSec/bundle/no-log/security/diff通过。既有moderate PostCSS与17项允许的RustSec warning没有由本slice引入，作为独立P2/依赖基线保留。
- 一次sandbox-only SQLCipher诊断因macOS backup-attribute策略失败，随后按正确manifest/run ID受控cleanup；最终matching temp root=0。未递归删除、未接触真实数据。
- 结构化结论：Owner已接受DEC-126-043方案A；S10P2F Closure Passed，Local-only BLK-004 Closed。Owner随后授权LIA-126-012并通过DEC-126-044/S10I关闭真实identity缺口；DEC-126-045接受S10P3 Closure并关闭BLK-005。Owner另行批准并执行LIA-126-008；G3仍Partial，S10B Executed / Blocked / Closure Fail，S11未授权。

### 9.19 LIA-126-012 / DEC-126-044 S10I / DEC-126-045 S10P3 Closure

| Finding | Severity | 实现与证据 | 当前状态 |
|---|---|---|---|
| S10P3-REV-001 | P1 Public-before-Host | local create transaction、stable operation/idempotency、201 identity/reference match、atomic binding、bound后Host start | CLOSED / fixed-provider + real 201/bind PASS |
| S10P3-REV-002 | P1 persistence/recovery | SQLCipher v5 content-free binding/outbox；v1–v4 migration；retry/lease/unknown/restart；authority/logout/tenant/revision stop | CLOSED IN LOCAL CHECKPOINT |
| S10P3-REV-003 | P1 private projection | accepted command/channel、closed Rust/schema/TS/Pinia、gap/resync/stale；WebView sensitive/control-plane IDs absent | CLOSED IN LOCAL CHECKPOINT |
| S10P3-REV-004 | P1 deletion boundary | local binding cascade；late response/delete race不启Host；Public row retain语义固定 | CLOSED / REAL DB RETENTION PASS |
| S10P3-REV-005 | P1 repository gates | TS 30 files/167 tests；lint/build；Rust 129 pass/0 fail/3 ignored；fmt/clippy | PASS |
| S10P3-REV-006 | P1 real native identity | standard Authorization Code + PKCE access token经production Rust authority调用fixed API | PASS；numeric `nbf`；API required-claim verifier unchanged；S10P3-BLK-001 resolved |
| S10P3-REV-007 | P1 real Public/PostgreSQL boundary | 201/bind、delete后Public row retained、正文/path denylist；错误/unknown由既有fixed fault matrix覆盖 | PASS；task 1/closed 1/forbidden 0/path 0；audit 5/forbidden 0/path 0；idempotency 1 |
| S10P3-REV-008 | boundary | contracts/API/Host wire/Runtime pin/default flags/MiniMax/Keychain/real data/remote | unchanged / counts 0；only local S10E token profile changed |

真实环境使用fresh run `90dc0dd9-140d-4ec0-b918-e24faab98aeb`的run-scoped S10E PostgreSQL/Keycloak/Caddy/API，synthetic identity与migration v4均成功；API与containers已按run ID停止，named volumes保留，未执行volume删除。安全证据只记录claim名称/类型与closed状态，不保存token、secret、正文或真实路径。

结构化结论：Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`与Infra `8d7c84dc963141931c6c5d3c3aded3218247df0b`是clean local-only checkpoints，未push。S10P3授权范围内P1为0；Owner于2026-08-05接受DEC-126-045 Option A并关闭BLK-005。该Closure本身未自动授权S10B；Owner随后另行批准并正式执行LIA-126-008，结果见§9.20；G3保持Partial。

### 9.20 LIA-126-008 / S10B First Execution Failed Closure Review（DEC-126-046 Accepted Option A）

| Finding | Severity | 实际证据 | 当前状态 |
|---|---|---|---|
| S10B-REV-001 | P1 bootstrap authority | Infra exact profile只创建`yijie_api_feat126_s10`；API `feat-125-local-lab` validator只接受`yijie_api_feat125_local`，在读取manifest/连接DB前拒绝 | **OPEN AT FIRST RUN / LATER CLOSED BY DEC-126-048** |
| S10B-REV-002 | P1 no-bypass | 未省略profile、未使用generic lane、未手工建库/insert、未复用旧run volume；tracked manifests没有任何授权写入 | CLOSED FOR ABORT SAFETY |
| S10B-REV-003 | P1 data state | migration v4；users/tenants/memberships=`0/0/0`；API/Desktop/Host/fake/Runtime均未启动 | S10B-001 FAIL；002–012 NOT RUN |
| S10B-REV-004 | P1 cleanup | four containers/networks stopped/removed；fixed listeners=0；temporary binaries removed；4 run volumes与ignored run record按删除边界保留 | CLOSED FOR ABORT CLEANUP |
| S10B-REV-005 | boundary | MiniMax/external model、real Keychain/data、default activation、business source、contract/Runtime pin、remote write均0 | CLOSED |

Owner已接受DEC-126-046方案A：接受本次可信fail-closed执行事实，但不接受S10B Closure；当时S10B-BLK-001保持Open，不授权直接修复、重跑或S11。方案B（generic profile）和方案C（手工状态/旧volume）均被拒绝。后续DEC-126-048仅关闭BLK-001，仍未恢复S10B执行授权。

### 9.21 S10BP0 Closed Bootstrap Corrective Design Review（DESIGN-126-009 / DEC-126-047 Accepted Option A）

| Review | 只读证据 | 结论 |
|---|---|---|
| API profile authority | `profile.go/profile_test.go` | 现有feat125 profile精确限制nonproduction/issuer/127.0.0.1:5432/feat125 DB/only sslmode；错误不泄漏DSN/secret |
| Validation order | `cmd/bootstrap-nonprod-authz/main.go` | `ValidateExecutionProfile`先于input open/decode与任何migration/DB；manifest tuple validation也先于DB |
| Matrix authority | four tracked JSON + integration tests | 现有四份reviewed manifests形成2 users/2 identities/2 tenants/4 memberships/4 assignments；两tenant revision=3；第二遍后audit=8 |
| Atomicity | bootstrap integration fault tests | serializable transaction、audit rollback、commit-ack reconciliation与content-free failure classification已有可复用基线 |
| Infra gap | S10E Makefile/scripts read-only inventory | 已有exact migration/run authority，但没有FEAT-126 S10 bootstrap命令；不得使用generic CLI/manual SQL替代 |
| Contract impact | source inventory | central contract none；verifier/Public Tasks/IPC/Host/Runtime/schema不变；G2A N/A |

DESIGN-126-009冻结的新profile为`feat-126-s10-local-lab`，精确绑定nonproduction、local issuer与`yijie_api_feat126_s10` DSN，且只复用四份existing reviewed manifests。兼容策略不是删除API generic lane，而是让新的Infra S10权威命令内部固定profile和显式四文件列表、拒绝caller override；API同时增加独立closed profile校验。由此S10 path的missing/generic/wrong authority在manifest或DB前停止，现有调用者与feat125路径不变。

Owner已接受DEC-126-047 Option A并另行授权LIA-126-013。S10BP1 source和isolated evidence已完成，详见§9.22；本节仍保留当时设计事实。不得把S10BP1实现写成S10B已重跑或G4已通过。

### 9.22 LIA-126-013 / S10BP1 Closure Review（DEC-126-048 Accepted Option A）

| Review | 实际证据 | 判定 |
|---|---|---|
| Closed authority | exact `feat-126-s10-local-lab`、nonproduction、issuer、`127.0.0.1:5432/yijie_api_feat126_s10?sslmode=disable`；full SHA/clean API；四份显式tracked regular manifests | PASS |
| Validation order | profile在manifest open前；ordered matrix在migration/DB前；empty verifier在batch前 | PASS |
| Fresh/migration | pinned PostgreSQL 16.13 fresh DB，migration 1–4成功，pre-state 12项全0 | PASS |
| Atomic/idempotent matrix | 每个四-manifest pass为一个serializable transaction；首次4 changed，第二次4 unchanged；tenant revision 3；post exact counts与8 audits | PASS |
| Rollback | success-audit failure injection后users/identities/tenants/memberships/roles/permissions/assignments/audits均0 | PASS |
| Compatibility/contract | API full race/unit、generate-check；Infra 83/83；existing feat125/generic rules与四manifest bytes unchanged；central wire/schema/verifier/Runtime unchanged | PASS / G2A N/A |
| Security/cleanup | evidence仅count/state/classification，mode 0600；transient per-operation results删除；secret、temp candidate、container和anonymous volume清理 | PASS |
| S10E compatibility observation | accepted helper的tag@digest image inspect在Docker 29.6.1曾拒绝本机已有exact image；S10BP1仅用相同pinned ID启动单DB | historical S10B-BLK-002 / later Closed by DEC-126-050 |

结构化结论：S10BP1-001–013全部PASS、slice内P1=0。Owner已接受DEC-126-048 Option A，S10BP1 Closure Passed并关闭S10B-BLK-001。独立S10B-BLK-002随后由DEC-126-050关闭；两项决定均不自动授权S10B或S11。

### 9.23 DESIGN-126-010 / DEC-126-049 / S10B-BLK-002 Corrective Closure

| Review | 实际证据 | 判定 |
|---|---|---|
| Root cause | Docker 29.6.1 inventory与ID/RepoDigests精确存在；旧tag@digest lookup曾fail，Docker重启后恢复 | state-sensitive reference-index compatibility，不是镜像缺失 |
| Closed authority | verifier只导入现有`FEAT_126_S10_IMAGES`，解析`version-tag@digest`并派生3个唯一`repository@digest` | PASS / no second pin authority |
| Fail closed | malformed/conflicting pin、inspect错误、invalid ID、RepoDigests缺失、descriptor drift均拒绝 | PASS |
| No-pull boundary | helper仍使用原Compose pins和`--pull never`；source无pull/floating-tag fallback | PASS |
| Live startup | fresh run三identity核验后四个S10E依赖全部healthy | PASS / no image pull |
| Cleanup | authoritative stop后container/network=0；4 named volumes与owner-only ignored run record保留 | PASS within accepted retention boundary |
| Scope | API/Desktop/Host/Runtime/fake provider/MiniMax/真实数据/flag/remote write均未启动或发生 | PASS / not S10B rerun |

结构化结论：DESIGN-126-010与DEC-126-049已接受，S10BR1纠偏实现和验证完成，范围内P1=0。Owner现已接受DEC-126-050 Option A，S10BR1 Closure Passed并关闭S10B-BLK-002。G3保持Partial，G4/G6 Pending，不得自动重跑S10B或进入S11。

### 9.24 LIA-126-014 / S10B-R2 Failed Execution Review（DEC-126-051 Accepted）

| Review | 实际证据 | 判定 |
|---|---|---|
| Candidate freeze | 七仓clean；Governance/API/Infra分别形成`9db41b0...`、`c5f334e...`、`597acb3...`本地checkpoint；Contracts/Runtime pin精确不变 | PASS；0 unrelated/FEAT-123；0 push |
| Repository gates | Governance package/strict/G2A/YAML/lint/test；API lint/race tests；Infra 85/85/Compose validation/diff | PASS；API沙箱loopback限制在批准的宿主权限下原命令PASS |
| Fresh authority | run `4ffa07b9-6e4c-45d4-b5d5-3b3be5d7d818`；权威migration Make target/wrapper | FAIL CLOSED before secret/run root/Docker/DB |
| Root cause | wrapper常量固定旧API `a64f9f...`；当前closed bootstrap只在`c5f334e...`；migration wrapper SHA-256=`f7bc532af3cef66eeca251b96fb9d9b18af65c252dda44c703442a8a9cbcaad0` | `S10B-BLK-003 OPEN / migration_wrapper_api_candidate_mismatch` |
| No bypass | 未退回旧API、改hardcode、直接go-run migration、删除profile、手工SQL或复用旧run | PASS |
| Resource/safety | run root/container/network/volume/listener/API/Desktop/Host/fake/Runtime/model/Keychain/real-data/remote-write均0 | PASS for abort safety only |
| Matrix | S10B-001 FAIL；S10B-002–012 NOT RUN | S10B-R2 Closure rejected；G4/G6仍Pending |

结构化结论：LIA-126-014授权已被本次fresh preflight消费。Owner已接受DEC-126-051 Option A：接受可复验的fail-closed事实但不接受S10B-R2 Closure，保持`S10B-BLK-003` Open；后续只允许单独纠正migration/bootstrap共享显式完整API SHA authority，不重跑S10B、不进入S11。

### 9.25 LIA-126-015 / S10BM1 Corrective Closure Review（DEC-126-052 Accepted）

| Review | 实际证据 | 判定 |
|---|---|---|
| Scope | only Infra Make/helper/wrappers/runbook/tests；API/Desktop/Host/Runtime/contracts未改 | PASS；central G2A none |
| Shared authority | migration/bootstrap都强制full lowercase SHA并调用同一run-scoped helper | PASS；no second hardcoded pin |
| Filesystem | canonical owner-only 0700 root；0600 regular authority；O_EXCL/O_NOFOLLOW；owner/mode/nlink验证 | PASS |
| Worktree | exact clean API HEAD接受；wrong SHA、dirty/untracked、candidate drift拒绝 | PASS |
| Closed document | only schema version/run ID/API full commit；corrupt/extra/oversize拒绝 | PASS；content-free |
| Ordering | helper在secret validator和PostgreSQL前执行 | PASS |
| Compatibility | old two-argument migration call fails closed；Make target/runbook同checkpoint更新 | private local helper `breaking`；central contract none |
| Repository gates | Infra validate/lint/test、87/87、Node/shell syntax、diff | PASS |
| Checkpoint | `bb96333df908d6fea72ec0a1f57a64477c2428e4`；worktree clean；not pushed | PASS |
| Runtime boundary | container/service/secret/DB/API/Desktop/Host/Runtime/model/Keychain/real-data/default activation/remote write | 0 / NOT RUN |

artifact SHA-256：authority `a8ba0234d4c1ea13bfaa48ca955f6d5d7ab17c43216fdfa68991f5cf678f08dc`；migration `9efa08b32ef5b3f4ddeed2bda15b961f40fc356d025da175b1c99c73f1cd3f11`；bootstrap `37f70ac6a5342dde31f9adb3ea4a539056df76239bcd5bf34dedf63854f6c626`；tests `38ebde8871f4d3c4644e69eb36bfb917506bf34f7fe2822b042978030587b819`；runbook `853a62af6879caba90e21eec8f6f54a8b51537fa93847d95d20d8d3a4f2925cc`。

结构化结论：Owner已接受DEC-126-052 Option A；LIA-126-015范围内P1=0、S10BM1 Closure Passed、`S10B-BLK-003` Closed。本验证不是S10B rerun/G4证据。LIA-126-016后来获批并已消费，结果见§9.26。

### 9.26 LIA-126-016 / S10B-R3 Execution Review（DEC-126-053 Accepted）

| Review | 实际证据 | 判定 |
|---|---|---|
| Provenance | seven exact clean HEADs: Governance `784c970a...b15c`, Contracts `29317b64...e9f`, API `c5f334e8...abd6`, Host `e0a8d3d2...5674`, Desktop `ed9eb14f...b78c`, Runtime `3aa317ce...d6f`, Infra `bb96333d...28e4` | PASS |
| Local tooling | Compose `5.3.0`, Docker client/server `29.6.1`, required CLI available, ports 5432/8443/9443/18080/18082/1420 free | PASS |
| Run authority | canonical UUID `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5`; ignored secret init and Compose config validated | PASS |
| Immutable image preflight | `postgres:16.13-alpine` reports reviewed RepoDigest, but Docker rejects direct inspect of the exact `postgres@sha256:4e6e...d50` authority used by the accepted verifier | **FAIL / immutable_postgres_repository_digest_unavailable** |
| Startup | verifier fails before Compose `up`; API/Desktop/Host/fake/Runtime not started | container/process=0；S10B-002–012 NOT RUN |
| Containment | owner-only `REJECTED`; exact stop; run-scoped container/network/volume/listener inventory all zero | PASS |
| Scope/security | source/pin/helper unchanged；pull/retag/Docker-restart workaround/rerun=0；MiniMax/Keychain/real-data/default activation/remote write=0 | PASS for abort boundary only |

结构化结论：LIA-126-016已消费，S10B-R3 Closure不成立，G4/G6仍Pending。Owner已接受DEC-126-053 Option A：接受fail-closed事实、拒绝Closure，保持`S10B-BLK-004` Open并校正根因；任何纠偏或新run仍须Owner单独批准。

### 9.27 DESIGN-126-011 / S10BD0 Read-only Differential Review

| Probe/Review | 实际证据 | 判定 |
|---|---|---|
| Seven-repository scope | Governance `784c970a...b15c`含既有R3治理overlay；Contracts/API/Host/Desktop/Runtime/Infra固定SHA且clean | PASS；无实现仓改动 |
| Verifier source | `inspectLocalDigest`对`spawnSync.error`或任意non-zero status统一抛`required immutable image is unavailable locally` | **confirmed diagnostic collapse** |
| Restricted/current Docker capability | existing verifier返回generic image-unavailable；同上下文`docker version`显示`desktop-linux` endpoint socket不存在；context仍指向Docker Desktop socket | **docker_daemon_unavailable evidence；不得归类image missing** |
| Earlier approved read-only differential | Docker capability可用时，正确PostgreSQL `repository@digest`/`version-tag@digest`的Id、RepoDigests和Descriptor曾精确通过，未pull/retag/restart | disproves permanent Docker 29.6.1/digest incompatibility claim |
| Current live identity | 本轮遵守no-start边界，没有启动Docker Desktop，因此未执行当前daemon内image/resolver PASS | NOT RUN / accurately disclosed |
| Contract impact | S10BD0 docs-only=`none`；future S10BD1 local deployment-interface=`semantic`；central contracts/G2A=N/A | REVIEWED |
| Governance gates | feature package、strict、G2A、unique-key YAML、`pnpm lint/test`、shell syntax、diff check | PASS |
| Infra read-only regression | unchanged Infra `bb96333df908d6fea72ec0a1f57a64477c2428e4`；`pnpm validate`、87/87 tests、diff check | PASS；0 source diff |
| Runtime scope | container/create/service/S10B/model/Keychain/real data/flag/remote write=`0` | PASS for scope |

DESIGN-126-011冻结capability-first、closed failure classes、原Compose pin exact identity与单独授权的no-pull create/remove resolver probe。DEC-126-054 Option A已Accepted；LIA-126-017已批准但Held / Not Started，授权尚未消费。本节不是S10BD1实现/Closure、S10B/G4或local G6证据。

### 9.28 LIA-126-017 / S10BD1 Closure Review Candidate

| Review | 实际证据 | 判定 |
|---|---|---|
| Provenance | Governance execution checkpoint `075a5051b538ce8f28834db70de8f4f544ce4484`；Infra exact clean checkpoint `2a643caef210e32cab80242ede46b96927b2097a`；Contracts/Runtime pins unchanged | PASS |
| Closed capability classes | CLI、permission、daemon、image missing/reference unresolved、identity/repository/digest/platform/payload、resolver/cleanup失败均闭合；capability失败时image/create=0 | PASS / S10BD1-001–007 |
| Immutable authority | 只消费Compose原始3个`version-tag@digest`；Id、Descriptor、RepoDigests、repository、OS/server arch与双快照稳定性均校验；tag-only不产生PASS | PASS |
| Resolver safety | `create --pull=never --network none`；never start；run-scoped name/labels；全部声明volume用tmpfs；unknown outcome exact reconcile；foreign/mismatch delete=0 | PASS / S10BD1-008–010 |
| Automated gates | focused S10BD1 12/12；Infra full 99/99；validate/lint/shell/security/no-log/diff；Compose pins与`--pull never` unchanged | PASS |
| Exact-commit live probe | run `12600000-0000-4000-8000-000000000055`；Docker Desktop 4.82.0 / Engine 29.6.1 / linux-arm64；3 immutable identities + 3 no-start probes | PASS / no pull |
| Cleanup/state restoration | labeled containers=0、running=0、networks=0、volumes=0；Docker由本轮启动并恢复执行前stopped | PASS |
| Scope | API/Host/Desktop/Runtime/contracts/wire/schema/MiniMax/Keychain/real data/default flag/remote write/S10B-R4/S11=0 | PASS |

结构化结论：S10BD1授权范围内P1=0；Owner已接受DEC-126-055 Option A，S10BD1 Closure Passed并关闭`S10B-BLK-004`。不得自动申请或执行S10B-R4。

### 9.29 LIA-126-018 / S10B-R4 Fail-closed Review

| Review | 实际证据 | 判定 |
|---|---|---|
| Provenance | 七仓精确匹配Owner固定SHA且worktree clean；Runtime binary/manifest pin unchanged；run `96a0a80d-27d4-4022-a470-4a7f004d9c4c` fresh | PASS |
| Docker/immutable images | Docker Desktop 4.82.0 / Engine 29.6.1 linux-arm64；S10BD1验证3 immutable identity和3 create-never-start resolver probe；`--pull never` | PASS |
| Dependency/identity/bootstrap | fresh四依赖healthy；TLS/OIDC/Tasks denial、2 synthetic users、API migration v4、closed four-manifest bootstrap、API health/readiness | PASS |
| Fake readiness | Host固定request fixture=`normal-000`；本次manual request使用S9 dataset bundle identity=`feat126-title-raw-v1`；正确run ID返回403；accepted fake calls=0 | **FAIL / S10B-001** |
| Remaining E2E | S10B-002–012；Vue/Pinia/Tauri/Desktop/Host/Runtime真实主链 | NOT RUN |
| Safety boundary | Host/Desktop/Runtime未启动；Public Task/conversation action=0；MiniMax/external-model/Keychain/real-data/source/default/remote-write=0 | PASS FOR ABORTED SCOPE ONLY |
| Cleanup | API/fake停止；container/network/listener=0；临时process root删除；4 named volumes与ignored Infra record保留；Docker恢复stopped | PASS FOR ABORTED RUN |
| Contract impact | execution/governance only=`none`；central contracts/private IPC/Public Tasks/Host wire/schema/Runtime pin/G2A unchanged | PASS |

结构化结论：LIA-126-018的一次授权已消费；S10B-R4 Closure不成立。新`S10B-BLK-005`为P1，原因是执行编排没有把Host request fixture身份作为单一machine-readable authority，导致S9 dataset bundle名称被误作fixture。Owner已接受DEC-126-056 Option A并单独授权S10BF1；R4失败历史不变。

### 9.30 LIA-126-019 / S10BF1 Closure Review（Accepted）

| Review | 实际证据 | 判定 |
|---|---|---|
| Host authority | `dataset_id`/`fixture_case_id`显式分离；case/digest从锁定bundle加载；probe自行生成headers | PASS |
| Host negative matrix | invalid run/endpoint、dataset-as-case、dataset/digest drift、unknown/legacy/oversize payload fail closed | PASS |
| Infra authority | 唯一Make runner；七full SHA；无dataset/fixture/endpoint operator input；fresh root/ports | PASS |
| Combined gates | resolver、fresh dependencies、TLS/OIDC、2 users、migration v4、closed bootstrap、API health/ready、fake ready | PASS |
| Repository gates | Host lint/vet/contract/full race；Infra validate/lint/103 tests/Node/shell/diff | PASS |
| No-log/cleanup | generated secrets hit=0；API/fake/container/network/listener=0；4 volumes披露；Docker恢复stopped | PASS |
| Evidence | run `ed22fc82…f3f4`；0600 summary SHA-256 `8198442e…f7d9`；`s10b_r5_executed=false` | PASS |
| Contract impact | private test/deployment tooling `semantic`；central contract/wire/IPC/schema/Runtime pin unchanged | PASS / G2A N/A |

结构化结论：S10BF1范围P1=0，Owner已接受DEC-126-057 Option A；S10BF1 Closure Passed，BLK-005 Closed。该证据不是S10B-R5/G4，不能自动授权fresh E2E、S11或MiniMax。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| VoiceOver manual verification | DEC-126-034已接受S8B自动化/browser Closure证据，但VoiceOver人工清单尚未执行 | 若把Closure接受写成真人VoiceOver通过会夸大a11y证据 | 保留到S11/G6 Owner本地验收并记录实际结果 | 段成威 | does not reopen S8B Closure；blocks corresponding manual G6 claim |
| Draft PR dependency audit / merge approval | PR #1 exact head CI在`brace-expansion 2.1.2` high失败；candidate本身未改依赖；后续`govulncheck`与`origin/main` breaking未运行 | 若豁免红灯会留下已知high dependency并缺两项远端证据 | DEC-126-021 Accepted/HOLD；保持Draft，不rerun/waive/fix/push；未来需本地E2E、audit修复、全绿CI与单独Owner批准 | 段成威 | blocks merge only；不阻断未来明确批准的local draft implementation |
| Public/Host runtime conformance | S4–S8B分层实现与S9 Host→Desktop exact fixture/SQLCipher/plaintext consumer Eval PASS | 真实多进程链仍可能产生scope/raw/cleanup disagreement | S10须另行授权；保持flags off | 段成威 | blocks G4/local G6, not S9 Closure candidate |
| DB/encryption/delete E2E | SQLCipher v4 job/receipt、independent HMAC key、migration/cascade/checkpoint、restart和fake Host cleanup单仓PASS | 跨Desktop/Host/Runtime真实进程partial delete仍未运行 | S10验证完整多进程job/receipt/restart/fault E2E | 段成威 | blocks G4/local G6 |
| Runtime raw-reasoning/title/delete | S9 deterministic Eval与S10P1 Host→fixed Runtime assistant/raw真实turn PASS；完整Desktop turn/history/delete多进程链仍未运行 | raw UX/residual/inconsistent history | keep default flags off until S10B；历史MiniMax public-summary FAIL不改写 | 段成威 | blocks G4/local G6 |
| Desktop sidecar/secret storage | actual Desktop supervisor→Host→fixed Runtime child readiness/stop PASS；S10P2F file integrity/isolation/restart/no-log/exact cleanup实现与证据PASS；DEC-126-043 Accepted | signed native仍Deferred Native Hardening/NOT RUN，不等于PASS | Local-only BLK-004已关闭；未来native signing/production intent恢复native hardening门禁 | 段成威 | no longer blocks Local-only BLK-004；does not authorize S10P3/S10B |
| S10B full-process orchestration readiness | DEC-126-066 Accepted；DESIGN-126-014 Complete；LIA-126-025/S10BO1 full gates与targeted 14/14 PASS；Corrective Closure Passed | 完整fresh S10B-001–012仍未PASS | isolated live与fresh R8仍须分别授权；不得人工拼接或复用R7 | 段成威 | **S10B-BLK-008 Closed；G3 Partial；blocks G4/local G6** |
| S10E image-reference precheck | exact repository-digest verifier、85/85自动化和fresh no-pull四依赖up/stop PASS | 局部启动不能冒充S10B | DEC-126-050 Accepted；保持无floating tag/pull | 段成威 | S10B-BLK-002 Closed |
| production identity/infra | FEAT-125 deferred | no production safety | N/A for DEC-126-022 local-only scope；future online intent must reopen production track and FEAT-125 prerequisites | 段成威 | does not block local G6；blocks any production claim |

## 11. 结论

- Requirements package：G1/G2/G2A Re-review Passed；DEC-126-023–069 Accepted，DESIGN-126-014/016 Complete，`LIA-126-025/S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed`，`LIA-126-028/S10BO3 Corrective Closure Accepted / S10B-BLK-010 Closed`。S10BF1/S10BRP1/S10BEP1 Closure Passed；LIA-126-024/R7与LIA-126-027 isolated live均已消费，后者失败且不可复用。
- Code Complete：No。G3仍Partial；R7仅S10B-001 PASS，002 fail closed，003–011 NOT RUN，012仅abort cleanup subset；G4与Owner G6均未完成。
- 验证人：Codex（文档事实与结构）；最终 Reviewer 为段成威。
- 日期：2026-08-09。
- 结论依据：既有accepted链、R6/S10BEP1证据、R7 run `d553e6ea-e10f-4470-b357-a41807d6fb06`的content-free事实及S10BO3 corrective证据。完整fresh S10B-001–012仍未PASS；无Xcode/Keychain/MiniMax/真实数据/default activation、commit或远端动作；任何preflight或repository corrective PASS都没有被冒充完整S10B E2E。

### 9.30 LIA-126-020 / S10B-R5 fail-closed evidence

| Evidence | Result |
|---|---|
| Seven baselines/worktrees | exact full SHA and clean before run |
| Fresh run | `24ae14b7-46d1-4fd5-a7ac-a30932586ad6` |
| S10B-001 | PASS via sole Infra runner; summary SHA-256 `b3e4b833283bf0102edfc4100cd0339002d769d839b7903a2a4426c531b6b1f8` |
| S10B-002 | FAIL-CLOSED before API readiness: preflight/current API runtime supports `feat-125-local-lab`, while frozen R5 continuation requires `feat-126-s10-local-lab` |
| S10B-003–012 | NOT RUN; only abort cleanup subset executed |
| Data/model | Public Task/session/turn=0；MiniMax/external model/real data/Keychain=0 |
| Secret/no-log | 6 files scanned against generated secret values, hits=0；forbidden Desktop/Host/Runtime run dirs=0；tracked default-on flags=0 |
| Cleanup | API/fake/process/container/network/listener=0；Docker stopped；4 named volumes retained and disclosed |
| Contract/diff | business source, contracts, IPC, wire, schema and Runtime pin unchanged；seven worktrees clean before governance edit |
| Governance gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint`、`pnpm test`、checker shell syntax与`git diff --check` PASS |

结构化结论：LIA-126-020的一次授权已消费，S10B-R5 Closure不成立。`S10B-BLK-006`为新的P1，DEC-126-058 Option A建议接受事实但拒绝Closure，并要求独立runtime-profile authority纠偏评审。Owner决定前不得修复、重跑、进入S11或调用MiniMax。

### 9.31 LIA-126-021 / S10BRP1 Closure Review（Accepted）

Owner于2026-08-06接受DEC-126-058 Option A并以明确实施指令授权、消费LIA-126-021，随后批准DEC-126-059 Option A。父基线为Governance `bcae57085b4fcb21a9d83f2ab08bc6c308228510`、API `c5f334e88d54d9e04f388d0349f4f5925124abd6`与Infra `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`；clean local checkpoints为API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`与Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`，均未push。

| Evidence | Result |
|---|---|
| API source scope | `cmd/api-server/main.go`、`internal/app/app.go`、`internal/app/app_test.go` only；正式closed FEAT-126 runtime profile、pinned CA client、loopback/v1 isolation与strict config matrix |
| API conformance | `make lint`、`make test` PASS；专用profile positive/negative、FEAT-125/default compatibility、secure-v2/legacy-v1 route与loopback assertions PASS |
| Infra source scope | 单一versioned runtime authority、preflight authority consumption/summary、closed continuation launcher、bootstrap/result validators、tests/docs/Make入口；无Compose pin或业务wire变更 |
| Infra conformance | `pnpm validate`、`make lint`、`make test`、Node/shell/diff checks PASS；113/113；preflight summary绑定`api_binary_sha256`，launcher安全open/hash并复核digest与dev/inode/mode/size/mtime；真实child收到FEAT-126/nonproduction/18080并传播exit code，6类spawn前negative与binary drift PASS |
| Contract/security | `contract-impact=semantic` private local deployment only；central contracts/Host wire/Desktop IPC/业务schema/Runtime pin无diff；G2A N/A；secret/DSN/token/path不进入closed evidence |
| Runtime execution | Docker、API/Host/Desktop/Runtime与S10B-002–012均NOT RUN；未调用MiniMax、未处理真实数据、未启用默认flag、未远端写入 |

结构化结论：S10BRP1解决了“只改字符串”“reader未消费”与“binary未绑定summary”三类缺口：API本身执行closed验证；Infra preflight与可执行continuation launcher消费同一authority、同run passed summary、reader和builder，并以`api_binary_sha256`及文件身份双快照绑定实际child。DEC-126-059 Option A已接受该证据，S10BRP1 Closure Passed且`S10B-BLK-006` Closed；它仍不是fresh S10B/G4证据。

### 9.32 LIA-126-022 / S10B-R6 Authorization Evidence

| Evidence | Result |
|---|---|
| Authorization | Owner于2026-08-06单独授权一次fresh S10B-R6 |
| Consumption | `CONSUMED / EXECUTED-BLOCKED / CLOSURE FAIL`；S10B-001 resolver失败后停止 |
| Fixed source candidates | Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`；Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`；Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135` |
| Governance identity | 本次文档commit形成的clean local HEAD；commit后记录并在执行时作为完整SHA输入 |
| Scope | 一次fresh S10B-001–012；fake provider、合成数据、临时exact-true profile与隔离run资源 |
| Exclusions | S11、MiniMax/外部模型、真实数据/Keychain、业务源码修改、default activation与所有远端动作 |

结构化结论：授权已消费且R6 Closure不成立。G3继续Partial，G4/G6继续Pending。

### 9.33 LIA-126-022 / S10B-R6 Fail-closed Evidence

| Evidence | Result |
|---|---|
| Seven repositories | Governance `d5d05a137338e4d72cf69173073fe49858a9a6e3`、Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`；全部exact/clean |
| Run/tooling | run `28afba8b-573a-46ec-b9d1-8a635c7b9cf0`；Docker client/server 29.6.1、Compose 5.3.0、desktop-linux |
| S10B-001 | FAIL-CLOSED at image resolver；top-level class `preflight_image_resolver_failed` |
| Post-failure read-only inspection | 三项冻结image的Id、Descriptor digest、RepoDigest、linux/arm64精确匹配；未重跑create probe，因此leaf root cause unresolved |
| S10B-002–012 | 002–011 NOT RUN；012只执行abort cleanup核对 |
| Resource containment | run-labeled container/network/volume=0；5432/8443/9443/18080/18082/1420/1421 listener=0；Docker保持执行前running |
| Evidence/security | 0700 run root；2个ignored 0600 files；REJECTED SHA-256 `7c7c5f61d03614f41dec86fd051bda8668bebf208ff53349fe5535ba5f765e11`；5个secret对REJECTED命中0 |
| Forbidden actions | no source change/retry/continuation/MiniMax/external model/Keychain/real data/default activation/remote action |

独立审查结论：父runner的步骤级错误折叠使S10BD1 leaf classifier没有进入R6证据，无法安全区分identity、probe create/validation或cleanup失败。DEC-126-060 Option A已被Owner接受：R6 Closure Rejected，`S10B-BLK-007`保持Open；不得把只读inspect PASS冒充resolver或S10B-001 PASS，也不得自动进入纠偏或fresh R7。

### 9.34 DESIGN-126-013 / S10BEP0 Read-only Review Evidence

| Evidence | Result |
|---|---|
| Baselines | Governance HEAD `d5d05a137338e4d72cf69173073fe49858a9a6e3`并保留前序9个FEAT-126治理改动；Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135` exact/clean |
| Parent fact | `feat-126-s10b-preflight.mjs`的`runCommand(label, ...)`在任意child非0时只产生`preflight_<label>_failed`，不解析stdout/stderr；resolver因此折叠为generic class |
| Child fact | `verify-feat-126-s10-images.mjs`已有12个`DOCKER_FAILURE_CLASSES`，但CLI failure只输出human string到stderr；没有versioned child result供parent消费 |
| Authority | `make feat-126-s10b-preflight`继续是唯一operator入口；DESIGN-126-013不增加dataset/fixture/profile/endpoint/image/phase/failure override |
| Recommended protocol | internal closed result v1；exact success/failure variants；同源allowlist/validator；single-line ≤2048 bytes；stderr empty；exit/status、run ID、phase/target/cleanup严格校验；120秒timeout |
| Parent projection | 12个leaf无损映射为`preflight_image_resolver_<leaf>`；REJECTED v1保持exact三字段；validated envelope另存fixed create-new 0600 ignored evidence |
| Compatibility | old/old与old/new维持default human Make行为；new/new closed；new/old protocol fail closed；rollback成组，不修改Compose pins或S10BD1行为 |
| Security | raw stderr、socket、真实路径、secret、DSN/token、image pin/digest、container ID和command不进入parent/evidence；cleanup incomplete/unknown不触发parent删除 |
| Runtime actions | Docker/resolver/container/service/S10B/MiniMax/Keychain/真实数据/远端写入均为0；Infra源码改动为0 |

结构化结论：DESIGN-126-013完成，`contract-impact=semantic`仅限private local deployment interface，central G2A=N/A。DEC-126-061 Option A随后于2026-08-08被Owner接受，并单独授权/消费LIA-126-023；实施证据见§9.35。

### 9.35 LIA-126-023 / S10BEP1 Repository and Isolated Live Verification

| Evidence | Result |
|---|---|
| Authorization | Owner继续执行指令按已声明边界接受DEC-126-061 Option A，并单独授权/消费LIA-126-023；不含fresh R7 |
| Infra scope | `verify-feat-126-s10-images.mjs`、`feat-126-s10b-preflight.mjs`、S10BEP1 tests与Infra runbook；无Compose pin/API/Host/Desktop/Runtime/contracts/business wire/schema/default flag变化 |
| Child/parent protocol | exact closed success/failure shape；12 leaf + 显式合法phase/target/cleanup tuple同源校验；fixed Node/script；namespace export guard；120秒timeout；2048/4096容量；strict UTF-8/单末尾LF/duplicate-key/framing/stderr/exit/run ID；mapped leaf与五个parent-only class |
| Evidence/compatibility | fixed create-new 0600 `image-resolver-result.v1.json`；REJECTED仍exact三字段；default human Make保留；new/old为`result_invalid`；validation leaf在owned cleanup后保留`removed`；cleanup unknown不触发parent删除；closed resolver后只读config recheck再固定`up --pull never` |
| Environment gate | Docker client/server `29.6.1`、Compose `5.3.0`、daemon access PASS；执行前daemon为6 containers/0 running/6 images |
| S10BEP1-014 live | canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`；closed parent exact v1 `passed`、`image_count=3`、`probe_count=3`；唯一调用、无retry |
| Evidence/no-log | 0700 run/evidence目录；唯一普通单链接0600文件`image-resolver-result.v1.json`，SHA-256 `e13f633fb331e3b0c0d08f22e16f7126980555ae849a73766a7bcc2259be6b34`；仅五个success字段，log及secret/path/image/container payload命中0 |
| Resource/image containment | run container/network/volume/listener前后0；daemon前后均6 containers/0 running/6 images；三项exact image Id/RepoDigest/platform前后逐项一致，无pull |
| Automated gates | Infra `pnpm test` 128/128、`pnpm validate`、targeted 34/34、Node syntax、`git diff --check`、完整`make lint/test`及Compose semantic PASS；Governance default/strict/G2A/unique-key YAML/`pnpm lint/test`/shell/diff PASS |
| Not run | clean Infra/Governance checkpoint（commit被明确禁止）、S10B-R7、S11、MiniMax、feature activation、真实数据、远端写入 |
| Security/actions | no service start、network/volume creation、listener、prune、volume deletion、model/Keychain/real data/activation/remote write；`s10b_r7_executed=false` |

Owner disposition：DEC-126-062于2026-08-09明确接受LIA-126-023/S10BEP1 Corrective Closure并关闭`S10B-BLK-007`。

结构化结论：repository corrective、S10BEP1-014 isolated live验证及全量门禁均PASS，Corrective Closure Passed；本轮禁止commit，未形成clean checkpoint。`S10B-BLK-001–007`均Closed，G3 Partial、G4/G6 Pending。fresh R7、S11、MiniMax、activation、真实数据及远端动作仍未授权。

### 9.36 DEC-126-062 / S10BEP1 Corrective Closure Acceptance

| Evidence | Result |
|---|---|
| Owner decision | 接受LIA-126-023/S10BEP1 Corrective Closure；确认S10BEP1-014 isolated live、Infra全量门禁和Governance门禁PASS |
| Blocker disposition | `S10B-BLK-007 Closed`；累计`S10B-BLK-001–007 Closed` |
| Gates unchanged | G3 Partial、G4/G6 Pending；完整S10B-001–012仍未PASS |
| Explicit exclusions | fresh R7、S11、MiniMax、feature activation、真实数据、commit、push及其他远端写入均未授权 |
| Contract impact | governance-only `none`；既有private deployment-interface `semantic`实现分类不变，central G2A=N/A |
| Post-decision governance | package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS |

### 9.37 DEC-126-063 / Local Clean Checkpoint Closure

| Evidence | Result |
|---|---|
| Scope review | Contracts/API/Host/Desktop/Runtime worktrees clean且冻结SHA不变；Infra仅5个S10BEP1 corrective文件，Governance仅9个FEAT-126文件 |
| Infra pre-commit gates | `pnpm validate`、128/128、targeted 34/34、完整`make lint/test`、Compose semantic、Node/Shell syntax、`git diff --check`全部PASS |
| Infra checkpoint | `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；commit后worktree clean；未push |
| Governance pre-commit gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS |
| Governance checkpoint | 包含DEC-126-063及本节的本地commit；commit后必须复核worktree clean；未push |
| Contract/security | checkpoint disposition=`none`；corrective既有`semantic`仅限private local deployment interface；central G2A=N/A；无真实数据、secret、activation或远端写入 |
| State retained | `S10B-BLK-001–007 Closed`；G3 Partial、G4/G6 Pending；fresh R7/S11/MiniMax未授权，`s10b_r7_executed=false` |

### 9.38 LIA-126-024 / S10B-R7 Fail-closed Evidence and Owner Closure Review

| Evidence | Result |
|---|---|
| Authorization/baselines | LIA-126-024单次授权已消费；七仓固定SHA在执行前与治理编辑前均exact/clean |
| Environment | Docker client/server 29.6.1、Compose 5.3.0、daemon access PASS；执行前daemon=`6 containers / 0 running / 6 images` |
| Canonical run | `d553e6ea-e10f-4470-b357-a41807d6fb06`；fresh isolated resources、synthetic identity/data、fixed fake provider、ephemeral secret backend |
| S10B-001 | PASS；唯一preflight summary SHA-256 `de994e3dd155e13ab27d7bb9c8645e4807e050b88fc9b300bdf62bd000612b80`；3 identity/3 no-start probe evidence SHA-256 `c424a4e8e0deb405c713bc689821973f2d99b91f9ef5826d44a88e16a0177e9e` |
| Preflight bindings | dataset=`feat126-title-raw-v1`；fixture=`normal-000`；dataset SHA-256 `523609b44fd244fff18b930c992375999276c2e0d5786efadfd8858ec623b308`；API binary SHA-256 `533ef53fab18ca6cd5c8882b707c50a52a14a9ae7b66680d70323157f6ab0469` |
| S10B-002 | **FAIL-CLOSED before continuation spawn**；唯一launcher是API-only且明确不启动Compose/其他组件；process manifest只是不可执行候选；没有完整四组件S10B-002–012 authority |
| S10B-003–012 | 003–011 NOT RUN；012仅abort cleanup subset PASS/overall NOT RUN；API continuation/Host/Desktop/Runtime/Public Task/session/turn/provider call均0 |
| No-log | 8个允许文件对5个secret和664个冻结payload值命中0；bearer/DSN/private-key命中0；fake log empty；continuation log absent |
| Containment | exact stop PASS；run container/network/process/listener=0；4 named volumes和ignored run root保留；daemon终态=`6/0/6`；无retry/prune/volume deletion |
| Contract/default/remote | execution/governance `contract-impact=none`；central G2A unaffected；source/default flags/contract/wire/schema/Runtime pin unchanged；无S11/MiniMax/Keychain/真实数据/commit/remote write |
| Governance gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS |

独立审查结论：`s10b_r7_executed=true`，但R7 Closure不成立。Owner已接受DEC-126-064 Option A：接受fail-closed事实、拒绝R7 Closure并保持`S10B-BLK-008 Open`；本轮只授权DESIGN-126-014只读设计评审，不得自动继续。

### 9.39 DESIGN-126-014 / Four-component Orchestrator Design Review

| Evidence | Result |
|---|---|
| Review scope | 只读检查Governance、Infra、API、Host、Desktop、Runtime；未启动Docker/服务，未修改实现仓库 |
| Existing ownership | Infra preflight是唯一S10B-001 authority；Desktop通过SidecarSupervisor拥有Host；Host通过codex.Manager拥有固定Runtime；Infra不得直接启动Host/Runtime |
| Confirmed gaps | Desktop无真实Vue/Pinia/Tauri E2E driver且native auth/project picker不可确定自动驱动；Host无Runtime PID/PPID及fake generation证据；API无Tasks/audit/idempotency closed verifier |
| Frozen corrective | Infra单入口、仅run ID+七SHA、same-run preflight、closed S10B-002–012 state machine；test-build-only Desktop driver/PKCE；Host-owned Runtime/fake manifest；API-owned content-free verifier；no-log/crash/reconcile/exact cleanup |
| Repository impact | future corrective涉及Infra/API/Host/Desktop；Contracts与Runtime源码不变；当前review `contract-impact=none`，未来private interface `semantic`，central G2A=N/A |
| Governance gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`首轮及证据登记后复跑均PASS |
| Decision/state | `DEC-126-066 Accepted / DESIGN-126-014 Complete / LIA-126-025/S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed / G3 Partial / G4/G6 Pending` |
| Explicit exclusions | `isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、default activation、commit与远端写入均未执行或授权；全量门禁PASS不扩大任何live或后续阶段授权` |

## 12. LIA-126-025 / S10BO1 Verification Record

- Fixed implementation candidates remained exact: API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`, Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`, Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`, Infra `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`; Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f` and Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` were unchanged.
- An earlier restricted-process attempt was blocked by sandbox loopback/native capabilities and unavailable Compose discovery; it remains historical evidence and did not authorize assertion weakening or product-logic changes.
- Final capability preflight passed for Docker client/server `29.6.1`, Docker Compose `5.3.0`, daemon access, loopback listener, 0700/0600 temporary files, subprocess, native project bookmark and SQLCipher/file-security tests.
- API and Host full lint/race/build passed. Desktop passed frontend lint, 30 TypeScript files/167 tests, Rust 129 pass/3 explicitly ignored, production build, default build/clippy, feature build/clippy, driver tests 2/2 and production-bundle driver absence. Infra passed validate, full lint/test, Compose semantic validation, 142/142 tests and standalone `S10BO1-001–014` 14/14.
- Desktop's first default clippy run found two driver-only methods compiled without the matching feature gate. The separately authorized `contract-impact=none` correction added `#[cfg(feature = "feat126-s10-driver")]` to `run_id` and `validate_fixed_project`; all default and feature regressions then passed.
- Governance default, strict, G2A, unique-key YAML, `pnpm lint/test`, checker shell syntax and all affected-repository `git diff --check` passed after the evidence update.
- Result is `DEC-126-066 Accepted / LIA-126-025/S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed`. G3 remains Partial and G4/G6 Pending. No Docker live run, isolated live, fresh R8, S11, MiniMax, real data/Keychain, default activation, commit or remote write occurred.

## 13. DEC-126-066 / S10BO1 Owner Acceptance Record

| Evidence | Result |
|---|---|
| Owner decision | Accept LIA-126-025/S10BO1 Corrective Closure and close `S10B-BLK-008` |
| Accepted evidence | Capability preflight PASS; API/Host/Desktop/Infra full gates PASS; S10BO1-001–014 14/14 PASS; Governance evidence PASS |
| Boundary | Repository corrective Closure only; not isolated live, fresh R8, complete S10B-001–012, G4 or G6 evidence |
| Retained state | G3 Partial; G4/G6 Pending; all default flags off; Contracts/Runtime unchanged |
| Forbidden actions | No isolated live, fresh R8, S11, MiniMax, real data/Keychain, activation, prune, volume deletion, commit, push or remote write |
| Post-decision Governance | PASS：default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`均已重新执行并通过 |

## 14. DEC-126-067 / Local Clean Checkpoint Verification

| Evidence | Result |
|---|---|
| Scope | Fixed parent SHAs matched; Contracts/Runtime clean; Governance exactly nine FEAT-126 files; implementation diffs restricted to S10BO1 corrective |
| Pre-commit gates | API/Host contract, lint, race and build PASS; Desktop 167 TS, default 129 pass/3 ignored, feature 131 pass/3 ignored, driver 2/2 and production bundle absent PASS; Infra validate, Compose semantic, 142/142 and S10BO1 14/14 PASS |
| Exact checkpoints | API `451940b282d8dd3e232ed414bd44b0677897f4c4`; Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`; Desktop `d51e435cb8ea224e69f9707831ee71022d0a7b6e`; Infra `0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c`; Governance local commit containing DEC-126-067 |
| Governance rerun | default, strict, G2A, unique-key YAML, lint, test, shell syntax and seven-repository `git diff --check` PASS |
| Retained boundary | `S10B-BLK-008 Closed`; G3 Partial; G4/G6 Pending; no isolated live, fresh R8, S11, MiniMax, real data/Keychain, default activation, prune, volume deletion or remote write |

## 35. S10BO2 Repository Corrective Verification

| Evidence | Result |
|---|---|
| Decision/design | DEC-126-068 Accepted Option A；DESIGN-126-015 Complete |
| Desktop | checkpoint `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`；完整lint/test/build PASS；174/174 TS；default 134 PASS/3 ignored；feature 143 PASS/3 ignored；driver TS 7/7、Rust 6/6；production frontend/native driver absent；WebView sensitive scan 0 hits |
| Infra | checkpoint `0fed8187d6051c011e67142d90feff89de326cfe`；validate、完整lint/test PASS；162/162；S10BO1 14/14 + S10BO2 20/20 targeted PASS；Compose semantic PASS |
| Corrective details | durable content-free cleanup outbox claim race使用`now.max(unix_seconds())`关闭跨秒竞争；strict termination identity在有界观察后仅reap已知exit，对unknown identity/status保持`CleanupIncomplete`且不signal未知PID |
| Scope/security | Contracts/API/Host/Runtime本轮源码不变；content-free/no-log、production driver-absent和`git diff --check` PASS；contract-impact仅private semantic，central G2A=N/A |
| Runtime evidence | 未执行Docker live、isolated live、fresh R8、业务调用、真实数据/Keychain或默认启用；`s10b_r8_executed=false` |
| Closure state | Owner Accepted `LIA-126-026/S10BO2 Corrective Closure`；Desktop feature Rust 143 PASS/0 FAIL/3 ignored与其余记录门禁获确认；`S10B-BLK-009 Closed`；G3 Partial、G4/G6 Pending |
| Post-decision Governance | default、strict、G2A、unique-key YAML、lint、test、shell syntax和`git diff --check`首轮及本行回填后最终复跑均全部PASS |

## 36. LIA-126-027 S10BO2 Isolated Live Verification

| Evidence | Actual result |
|---|---|
| Run | `b68804f0-aaf9-4da4-95e1-aa3b605bfada`；single authorization consumed；no retry/resume/reuse |
| Preconditions | seven exact clean repositories；Docker client/server 29.6.1、Compose 5.3.0、daemon及local capability probes PASS |
| Final frame | `{"schema_version":1,"status":"failed","failure_class":"orchestrator_cleanup_unknown"}` |
| Read-only diagnosis | preflight sub-Make did not receive its required seven `*_SHA` Make variables；absent-run cleanup then marked unknown and overrode the original failure |
| Reached states | preflight did not establish run root；Desktop build/dependencies/API/fake/Desktop/Host/Runtime/component_ready/abort NOT RUN |
| Resources | project containers=0、networks=0、volumes=0、listeners=0；daemon 6/0/6 before and after；no prune or volume deletion |
| Evidence limitation | process cleanup and no-log NOT ESTABLISHED because run root and identity/evidence roots are absent；no manual kill/reconcile attempted |
| Repository gates | Desktop full/default/feature/driver/production-absent PASS；Infra validate/full 162/162 and targeted 34/34 PASS |
| Conclusion | isolated live Closure FAIL事实保留；Owner已接受LIA-126-028/S10BO3 Corrective Closure；`S10B-BLK-010 Closed`；`s10b_r8_executed=false` |
| Governance gates | default、strict、G2A、unique-key YAML、lint、test、shell syntax and `git diff --check` initial and final post-record runs PASS |

## 37. LIA-126-028 / S10BO3 Repository Corrective Verification

| Evidence | Actual result |
|---|---|
| Historical run | `b68804f0-aaf9-4da4-95e1-aa3b605bfada` remains FAIL and permanently non-reusable; no live rerun |
| Corrective | Infra-only private deployment/test implementation under DESIGN-126-016; Contracts/API/Host/Desktop/Runtime source unchanged |
| Authority | seven exact SHA Make assignments generated from one validated authority; no second env namespace or operator override |
| Attempt ledger | canonical 0700 directory, 0600 O_EXCL marker/failure/closure, owner/nlink/no-follow/canonical bytes, marker digest and script/binary drift checks |
| Failure semantics | original primary retained; cleanup/evidence/no-log/parent failures persisted and emitted separately; partial Compose/start/root and unknown inventory fail closed |
| Cleanup/no-log | explicit pre-run/preflight/run scopes; exact named-volume before/after set; phase-aware process-role and descendant validation; no prune or volume deletion code path added |
| Targeted | PASS `65/65` across four targeted files; S10BO3-001–020 all PASS including tamper, immutable closure, boundary and reconcile subtests |
| Infra full gates | Node syntax PASS; `pnpm validate` PASS; `make lint` PASS; `make test` `186/186 PASS` (strict Darwin vmmap capability enabled); Compose semantic PASS; `git diff --check` PASS |
| Runtime boundary | Docker live/isolated live/fresh R8/business case NOT RUN; `s10b_r8_executed=false` |
| Contract impact | semantic private local deployment/test interface only; central contracts and G2A N/A |
| Conclusion | `DEC-126-069 Accepted Option A`; `DESIGN-126-016 Complete`; `LIA-126-028/S10BO3 Corrective Closure Accepted`; `S10B-BLK-010 Closed`; G3 Partial、G4/G6 Pending |
| Governance gates | PASS after evidence update: default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check` |

## 38. DEC-126-070 S10BO3 Local Checkpoint Closure Verification

| Evidence | Actual result |
|---|---|
| Scope | PASS：Infra仅五个S10BO3 corrective文件；Governance仅九份FEAT-126治理文件；Contracts/API/Host/Desktop/Runtime clean/unchanged |
| Infra gates | PASS：Node syntax、validate、lint、full `186/186`、targeted `65/65`、Compose semantic及diff check |
| Infra commit | `91f7ec03372b1528abb93818abfad432a83327c4`；local clean checkpoint；not pushed |
| Governance gates | PASS：default、strict、G2A、unique-key YAML、lint、test、shell syntax及`git diff --check` |
| Governance commit | 包含本记录与Infra精确SHA的本地commit；精确SHA在commit形成后报告，文档不声明自引用SHA |
| Preserved state | LIA-126-027历史FAIL及run不可复用；`S10B-BLK-009/010 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false` |
| Prohibited actions | no Docker/isolated live、fresh R8、业务case、prune、volume deletion、push或其他远端写入 |
