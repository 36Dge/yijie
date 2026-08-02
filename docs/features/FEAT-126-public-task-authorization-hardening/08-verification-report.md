# FEAT-126 验证证据与独立审查报告

> LIA-126-002第二轮独立审查已把S4–S6从Complete调整为`Conditional / Corrective Closure Required`。
> 四仓仅本地WIP checkpoint已建立；Runtime、业务源码和远端均未修改。DEC-126-023方案C已Accepted、
> Q-017已关闭；本地contracts replacement `29317b6426578749dc698fc2ad32b986ee5c8e9f`已通过post-commit门禁，
> 现提交DEC-126-024最终G2A审批，代码纠偏继续暂停。
> 没有调用MiniMax、真实数据或生产环境；S7–S11与完整E2E仍为`NOT RUN`。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | `feat/feat-126-foundation-closure` | `d9fb8007d7b7e1b265e566d53f8b2e408ff0821d` | FEAT-126 WIP checkpoint；pre-existing FEAT-123 deletions仍未暂存/未提交 | zsh/macOS；feature package checker | 2026-08-02 Asia/Shanghai |
| sibling repos | local closure/candidate branches | Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `b5e601764357512208cc09bfb2b30b244a1b82ac`；Host `f6e4a5902d8f25632408c1c699ba17b8c66ef214`；Desktop `40413b409a467a133d178137651622e167d512de` | contracts local replacement clean；Runtime/Infra未改；三个business repo为local WIP checkpoint，无push | contracts post-commit gates + existing repo gates/LIA-126-002 review；GitHub Actions仅为旧PR历史run | 2026-08-02 |

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
| G2A source contract candidate | `yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f` | DEC-126-023 content-free replacement + post-commit source/fixture/generated/breaking/equality/digest review | 0 | READY FOR OWNER APPROVAL | parent=`c000a024`；old candidate/PR/remote unchanged；DEC-126-024 Pending；not implementation authorization |
| LIA-126-001 implementation | API/Host/Desktop foundation checkpoints | exact contract locks, historical repository tests and LIA-126-002 review | 0 final | CONDITIONAL | flags/routes default off；current P1 open；local checkpoint commits exist；no remote action |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh docs/features/FEAT-126-public-task-authorization-hardening` | project shell script | 0 | PASS | structure/templates only; not Gate approval |
| V-STRICT | yijie | same checker with `--strict` | project shell script | 0 | PASS | lexical completeness only; Open/NOT RUN remain intentional |
| V-G0 | yijie | same checker with `--gate G0` | project shell script | 0 | PASS | G0 document scope only; human Gate recorded separately |
| V-G1 | yijie | same checker with `--gate G1` | project shell script | 0 | PASS | G1 document scope has no incomplete markers；human approval recorded in `feature.yaml`/`01`/`03` |
| V-G2 | yijie | same checker with `--gate G2` | project shell script | 0 | PASS | G2文档结构与Owner Passed状态一致；不代表G2A/业务实现 |
| V-G2A | yijie | same checker with `--gate G2A` | project shell script | 0 | STRUCTURE PASS / HUMAN APPROVAL PENDING | checker only proves lexical completeness；DEC-126-024 remains Ready for Owner Approval |
| V-LOCAL-STRATEGY | yijie FEAT-126 package | package + strict + G2A checker、YAML parse、cross-document review including DEC-126-023/024/LIA-126-002 | docs + conditional foundations | 0 | PASS 2026-08-02 | Q-017 closed、G2A final approval pending、S4–S6 Conditional、G3 Partial与S7–S11 prohibition一致；does not approve DEC-126-024 |
| V-YAML | yijie | Ruby safe load + root map assertion | local Ruby | 0 | PASS | `YAML OK` |
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
| V-DESIGN-126-003 | yijie + Host/Desktop | exact v2/schema/caps/reconciliation/history/migration/delete consistency review | fixed Runtime + contract candidate + local checkpoints | 0 | CONDITIONAL | raw/SQLCipher foundations exist；Host cleanup/title and Desktop invariants/history/migration findings remain open |
| V-MINIMAX-TITLE | temporary `CODEX_HOME` + empty cwd | `MM-126-001` isolated title harness；exactly one `turn/start`；request/stream retry=0 | fixed `codex-cli 0.144.6` SHA-256 `1ef4f1…8df1fe` + Host `34e94acf…` config + MiniMax-M3 | 0 | PASS | 1 call；1,853 ms；terminal completed；strict JSON/sanitizer 18 grapheme；0 tool/rollout candidate/secret leak；5,232 tokens；cost absent；temp root removed |
| V-MINIMAX-SUMMARY | temporary `CODEX_HOME` + empty cwd | `MM-126-002` isolated high+concise harness；exactly one `turn/start`；request/stream retry=0 | same fixed Runtime/Host pin + MiniMax-M3 | 0 harness / frozen historical gate FAIL | FAIL under ADR-0015 historical gate | 1 call；9,256 ms；answer completed；0 public-summary event；7 raw delta + 1 raw completed content part；0 tool/secret leak；5,664 tokens；cost absent；temp root removed；不得事后改写为新raw Gate PASS |
| V-ADR-0016 | yijie | Owner product direction/lifecycle decision + document consistency review | no model/provider command | N/A | ACCEPTED DESIGN ONLY | raw reasoning必须以纯文本显示；缺失/无效阻断reasoning Gate；不进logs/telemetry/audit；DEC-126-016要求SQLCipher历史持久化和session级联删除；非实现证据 |
| V-CONTRACT-GENERATE | yijie-contracts | `make generate` | locked generators | 0 | PASS | 29 generated files current；v2 schema exported via namespace to preserve v1 TS root API |
| V-CONTRACT-LINT | yijie-contracts | `make lint` | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 0 | PASS | OpenAPI/AsyncAPI/JSON Schema/Buf/TS/Go vet |
| V-CONTRACT-TEST | yijie-contracts | `make test` | Node/Go above | 0 | PASS | Node 27/27 + Go packages；FEAT-126 narrow source tests 11/11 |
| V-CONTRACT-BUILD | yijie-contracts | `make build && pnpm pack:sdk` | package 0.3.0 candidate / `29317b6426578749dc698fc2ad32b986ee5c8e9f` | 0 | PASS | SDK tarball SHA-256 `21b17b50ee265e1ebbd7a5248880c7874c88def65c538f1216d0413e85fab082`；not published |
| V-CONTRACT-BREAKING | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | sole supported baseline | 0 | PASS | OpenAPI/Buf/AsyncAPI/JSON Schema无breaking；v2错误schema隔离后无v1 enum warnings |
| V-CONTRACT-LEGACY | yijie-contracts | parsed structural comparison against supported baseline | Node/YAML/Git | 0 | PASS | Public Tasks v1 2 paths + Agent Host v1 7 paths equality |
| V-CONTRACT-COMMIT | yijie-contracts | `git rev-parse HEAD && git rev-parse HEAD^ && git status --short --branch` | Git | 0 | PASS | HEAD=`29317b6426578749dc698fc2ad32b986ee5c8e9f`，parent=`c000a0245acb5c3f7ead5d2a877fb60c281c588c`，worktree clean；local branch only |
| V-CONTRACT-CONTENT-FREE | yijie-contracts | Public Tasks v2 targeted AJV/schema/fixture tests + generated TS/Go review | fixed synthetic UUID fixtures | 0 | PASS | request/success/error仅closed discriminator/reference/code；prompt/message/raw/title/path/result/error-message canaries rejected；3/3 targeted、27/27 all Node、Go PASS |
| V-CONTRACT-DIGEST | yijie-contracts | SHA-256 of canonical sources/generated outputs + deterministic SDK repack | `shasum -a 256` | 0 | PASS | replacement完整摘要见`04-contract-change-plan.md`/`feature.yaml`；SDK post-commit重复打包均为`21b17b50ee265e1ebbd7a5248880c7874c88def65c538f1216d0413e85fab082` |
| V-CONTRACT-REMOTE | origin + temporary clean clone | push exact SHA to `refs/heads/feat/feat-126-contract-candidate`；`git ls-remote`；clean clone locked install + generate/diff/lint/test/build/breaking/pack/equality/digest | Git/pnpm/Go/locked generators | 0 | PASS | remote branch=`c000a024…588c`；`origin/develop`仍=`9ec34abd…ebbb`；29 generated current、Node 27/27、Go PASS、v1 2+7 equality、九项摘要一致、clone clean；无merge/tag/发布/pin/编码 |
| V-CONTRACT-PR | GitHub PR #1 | create Draft PR with base `develop`, head `feat/feat-126-contract-candidate`; verify draft/state/base/head/OID/commit count/files and backfill CI result | GitHub/`gh` | 0 | PASS | [Draft PR #1](https://github.com/36Dge/yijie-contracts/pull/1) OPEN/DRAFT；head=`c000a0245acb5c3f7ead5d2a877fb60c281c588c`；1 commit、39 files；完整9项摘要与授权边界已登记；无candidate mutation或push |
| V-CONTRACT-CI | GitHub Actions | observe [run 30741466028](https://github.com/36Dge/yijie-contracts/actions/runs/30741466028) / [job 91479562558](https://github.com/36Dge/yijie-contracts/actions/runs/30741466028/job/91479562558) to terminal; read failure logs only | CI on exact PR head | 1 | FAIL / MERGE BLOCKED | PASS至checkout、locked install、Go modules、generate、generated diff、lint、test、SDK pack；`pnpm audit --audit-level high`发现`brace-expansion 2.1.2`高危GHSA-mh99-v99m-4gvg（patched `>=2.1.3`）；后续`govulncheck`与`./scripts/check-breaking.sh origin/main` SKIPPED；未rerun/waive/fix/push |
| V-CONTRACT-DEPENDENCY-ATTRIBUTION | yijie-contracts | `git diff --exit-code 9ec34abd... c000a024... -- package.json pnpm-lock.yaml` + `pnpm why brace-expansion` | Git/pnpm lock graph | 0 | PASS attribution | candidate未修改manifest/lockfile；锁定链为`openapi-typescript@7.13.0 -> @redocly/openapi-core@1.34.17 -> minimatch@5.1.9 -> brace-expansion@2.1.2`。这是既有工具链dependency baseline blocker，不是FEAT-126契约diff新增依赖；仍不能绕过红色CI |
| V-WORKTREE | all sibling repos | `git status --short --branch` | Git | 0 | PASS scoped | Contracts clean/exact candidate；API/Host/Desktop只有本次与已记录既有改动；Runtime/Infra未改；无commit/remote write |
| V-GENERATE | API/Host/Desktop | exact candidate lock + generate/check scripts | oapi-codegen 2.7.2 / openapi-typescript 7.13.0 | 0 | PASS | API Go `05d417…af51`；Host Go `629ddf…63b0`；Desktop TS `d3493a…03b`；source digests match candidate |
| V-API | yijie-api | `make generate-check && make test && make lint`；isolated PostgreSQL `make test-integration` | Go 1.26.5 / synthetic local PostgreSQL | 0 final | PASS | auth/tenant/permission/creator-private/404/idempotency/audit + migration v3；route default off/local-lab only |
| V-HOST | yijie-agent-host | `make contract-check && make test && make lint` | Go 1.26.5 / race + fake Runtime | 0 | PASS | app 67.1%、codex 71.0%、session 77.7%；raw no-log/no-bbolt、title isolation、cleanup receipt/store migration/path safety |
| V-DESKTOP | yijie-desktop | `make lint && make test && make build` | pnpm/Vue/Rust 1.95 / bundled SQLCipher | 0 | PASS | 18 files/113 TS；51 Rust PASS、1既有S7 Keychain test ignored；Clippy/fmt/Vite build PASS |
| V-INTEGRATION | affected repos | API PostgreSQL + Desktop SQLCipher/native fixture + Host fake Runtime | local synthetic only | 0 for S4–S6 | PARTIAL PASS | repository integrations pass；four-component E2E remains NOT RUN and blocks G4/local G6 |
| V-SQLITE-LINK | yijie-desktop/src-tauri | `cargo tree -i libsqlite3-sys` + feature tree | Cargo 1.95 | 0 | PASS | single `libsqlite3-sys 0.38.1` via `rusqlite 0.40.1`/`rusqlite_migration 2.6.0`；`bundled-sqlcipher` active |
| V-NO-LOG | API/Host/Desktop source + tests | logger sink scan、raw canary assertions、sidecar env allowlist、redacted command errors/key Debug | local synthetic canaries | 0 | SUBSET PASS | existing assertions pass；direct raw-canary bbolt and future S7/UI/E2E scans remain required |

## 5. 契约与版本兼容

| 结论 | Contract version/full commit/digest/generator | Command/Test | Result | Evidence |
|---|---|---|---|---|
| 源结构与生成无漂移 | `0.3.0 local replacement candidate` / `29317b6426578749dc698fc2ad32b986ee5c8e9f` / digests见`feature.yaml` | post-commit generate/current/lint/test/build/pack | PASS | worktree clean；未远端写入/merge/tag/发布/downstream pin |
| Draft PR merge readiness | PR #1 / exact candidate head | remote CI + dependency attribution | FAIL / HOLD | source/generate/test/pack步骤通过，但high audit失败且两个后续步骤未执行；DEC-126-021已Accepted/HOLD，当前不批准merge |
| Supported baseline breaking check | `f16a497…` sole supported baseline | check-breaking + legacy structural equality | PASS | 自动工具+人工语义；v1错误enum隔离缺陷已修复 |
| Producer conformance | replacement source + API/Host local checkpoints | source tests + handler/repository + Host schema/fake tests | SOURCE PASS / RUNTIME NOT RUN | source conflict resolved；API/Host仍锁旧candidate且本轮禁止修改，flags/routes remain off；DEC-126-024/LIA resume required |
| Consumer conformance | API/Host/Desktop exact locks and generated projections | generate checks + source digest verification | PROJECTION PASS | Desktop reducer/transport behavior remains S7 |
| Runtime canonical capability | `yijie-codex@3aa317...` / `codex-cli 0.144.6` artifact | source inspection + fake title/summary/raw/history fixtures + isolated exact artifact delete/restart | raw upstream 4/4 PASS；title/summary primitives PASS；raw observed once；delete functional；forensic erase NOT PROVIDED | 未证明Host/Desktop mapping、raw稳定性/安全性；Runtime WAL/log residue recorded |
| Host v2 title/raw-reasoning compatibility | Host local checkpoint + candidate `c000a024...` | contract-check/race/fake Runtime/title/raw/no-log + LIA-126-002 review | CONDITIONAL | v1 unchanged；partial cleanup/title/lease P1 open；v2 flags off |
| MiniMax feature compatibility | pinned Runtime/MiniMax-M3 + Host `34e94acf…` config | `MM-126-001/002` 各一次、0 retry | title PASS / historical public-summary FAIL / raw observed | structured title可进入后续 Eval；raw展示/SQLCipher生命周期已批准，但单样本不构成raw稳定性、持久化实现或安全conformance；Q-009/Q-016 Resolved |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-025–030 | API secure v2 handler/service/repository/migration | API auth/security/idempotency/integration tests | V-API | S4 PASS；activation/legacy retirement not performed |
| AC-007/010/011/013/014/017/020/021 | Host v2 raw/title/cleanup foundation | Host fake Runtime/schema/no-log/store tests | V-HOST | S5 PASS；Desktop/E2E portions remain |
| AC-001–006/015/020–024/029/030/034/035/037 foundation subset | Desktop SQLCipher/project/sidecar/native commands | prior Rust tests + LIA-126-002 review | V-DESKTOP | CONDITIONAL；reasoning terminal invariants、bulk history、cascade verification、migration matrix与instance readiness仍待关闭 |
| remaining AC/NFR | S7–S11 | matrix in `06-test-plan.md` | no authorized command | NOT RUN |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| Local four-component E2E | API/Host/Desktop/pinned Runtime create/stream/raw/history/actions/delete/restart | S4–S6 foundations only | NOT RUN | S7–S10 unauthorized；blocks G4/Local-only G6 |
| Security/tenant | Public/local auth/IDOR/path/secret | synthetic tests + source/fixture review | CONDITIONAL | audit matrix、Public Tasks正文边界和sidecar identity P1阻断closure |
| Failure/resilience | DB/SSE/Host/Runtime/provider faults | no harness | NOT RUN | blocks G4 |
| Migration rehearsal | Desktop SQLCipher + API Tasks owner | embedded SQLCipher + API PostgreSQL foundations | CONDITIONAL | populated Desktop v1→v2、repeated/read-only/corrupt cases与API idempotency expiry migration仍待补 |
| Isolated Runtime delete | fixed artifact/temp `CODEX_HOME`/synthetic canary | no credentials, model requests 0 | FUNCTIONAL PASS / BYTE RESIDUE FOUND | thread/read fails before and after restart；state row/rollout/index absent；WAL/log byte scan records limitation |
| SQLite dependency selection | Rust 1.95 temp project/macOS arm64 | exact locked dependencies | PASS | selected SQLCipher/migration pair builds；Refinery comparison rejected |
| Runtime fake + bounded MiniMax title/raw reasoning | pinned source/local mock Responses + fixed artifact/Host config | historical 5 upstream fixtures + S5 fake Host fixtures；historical 2 provider calls | Host foundation PASS / title historical PASS / historical public-summary FAIL / raw observed | no provider call this round；Desktop display/Eval remains NOT RUN，flags off |
| Performance | list/history/reducer/DB/title | no baseline | NOT RUN | blocks G4 |
| AI Eval | title/raw reasoning availability、plain-text safety、sensitive-fragment handling | no dataset/runner/prompt candidate | NOT RUN | blocks G4 |
| Visual/accessibility | approved Pattern/implementation | no active chat UI | NOT RUN | blocks G4 |

## 8. Diff 与制品完整性

- [x] `git status` 已复核：只有既有 FEAT-123 删除、新 FEAT-126 目录和 ADR-0012 的创建状态/未实施 checklist 事实更新
- [x] 范围统计已复核：FEAT-126文档/ADR与LIA-126-001限定的API、Host、Desktop源码；Runtime/Infra/contracts candidate未改
- [x] untracked new files 已用逐文件 `git diff --no-index --check` 验证
- [x] FEAT-126内容与跨文档Gate/ADR/AC已由Codex执行结构化review；最终独立人工Reviewer仍为段成威
- [x] S4–S6新增本地contract locks/generated projections、Go/Rust代码、PostgreSQL/SQLCipher migrations与Cargo lock；均未提交或远端写入
- [x] 本轮MiniMax调用为0；历史两次bounded请求不重跑；无生产资源或其它外部写操作
- [x] 未修改、恢复或覆盖 FEAT-123 既有删除
- [x] 文档未写入 key、token、真实 message、真实 project path 或商家数据

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
| LIA2-API-001 | P1 | secure Tasks只在成功create事务写business audit；401/403/404/409/503、get及拒绝路径未形成完整content-free审计矩阵 | S4 closure required；需先冻结pre-auth/unresolved-tenant审计语义 |
| LIA2-CONTRACT-001 | P1 source issue resolved / implementation stop remains | 历史candidate的`CreateTaskV2Request.input`/`TaskV2.input`为arbitrary object；canonical conversation fixture携带并回显`input.text` | DEC-126-023方案C形成`29317b...`并从schema/fixture关闭；DEC-126-024批准及LIA-126-002恢复前，业务checkpoint仍不得切换或继续 |
| LIA2-API-002 | P1 | API及Desktop远端CI仍checkout旧contracts SHA；API `generate-check`实际执行generate并重写，不能证明只读drift | S4 closure required；当前不做远端写入 |
| LIA2-HOST-001 | P1 | Runtime delete成功而通知/Host落库失败时没有durable intermediate state；同operation retry可能永久卡在Runtime NotFound | S5 closure required；可恢复operation状态机和fault/restart tests |
| LIA2-HOST-002 | P1 | cleanup与StartTurn缺少原子lease；并发starting turn可能与mapping删除竞态 | S5 closure required；race tests |
| LIA2-HOST-003 | P1 | title idempotency只按operation ID、失败可重复调用；空cwd/no-tools未在能力层保证 | S5 closure required；若固定Runtime不能保证，title flag继续关闭并复审 |
| LIA2-DESKTOP-001 | P1 | reasoning commit未强制terminal turn及turn/item一致终态 | S6 closure required；负向migration/repository tests |
| LIA2-DESKTOP-002 | P1 | sidecar spawn后只接受固定loopback health JSON，不能证明是本次实例；旧/同用户进程可伪装ready | S6 closure required；instance nonce/process identity及Runtime-ready分层 |

- LIA-126-002执行结论：已完成状态校正与四仓local WIP checkpoint；在`LIA2-CONTRACT-001`处依Owner预设停止条件暂停，没有继续修改API/Host/Desktop业务源码。
- Contract impact：`breaking`。DEC-126-023 C已形成新source commit而未amend既有candidate；重新执行的source G2A证据已就绪，等待DEC-126-024。
- S7A responsibility freeze：尚未完成；只有DEC-126-024批准并另行恢复closure后，才可冻结Rust-owned Host bearer/token/SSE bridge，当前不得实现。

- Reviewer 是否独立于主起草上下文：否；本轮是 Owner 前的设计候选自检，最终独立 Reviewer 为段成威。
- P0/P1 是否清零：否。未发现P0；上表P1仍Open，S4–S6均不得标记Complete。
- P2 例外批准：无；不是 accepted risk。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| DEC-126-024 final G2A | replacement source证据已完成但Owner尚未最终批准 | 未经批准切换下游会绕过Contract First gate | Owner基于`29317b...`、digests、breaking/v1 equality和source conformance批准或退回；之后仍需另行恢复LIA-126-002 | 段成威 | blocks LIA-126-002 continuation and S7–S11 |
| Draft PR dependency audit / merge approval | PR #1 exact head CI在`brace-expansion 2.1.2` high失败；candidate本身未改依赖；后续`govulncheck`与`origin/main` breaking未运行 | 若豁免红灯会留下已知high dependency并缺两项远端证据 | DEC-126-021 Accepted/HOLD；保持Draft，不rerun/waive/fix/push；未来需本地E2E、audit修复、全绿CI与单独Owner批准 | 段成威 | blocks merge only；不阻断未来明确批准的local draft implementation |
| Public/Host runtime conformance | API/Host/Desktop foundations Conditional；Desktop reducer未实现 | contract drift、IDOR/raw leak/cleanup disagreement | 先批准DEC-126-024、恢复并关闭S4–S6 P1；随后才可评审S7–S10 | 段成威 | blocks closure/G4/local G6 |
| DB/encryption/delete E2E | SQLCipher/migration/cascade/checkpoint单仓PASS；完整saga未运行 | cross-surface partial delete/recovery | S7/S10实现job/receipt orchestration并做restart/fault E2E | 段成威 | blocks G4/local G6 |
| Runtime raw-reasoning/title/delete | Host bridge foundation与fake fixtures PASS；真实Runtime跨Host/Desktop未运行 | raw UX/residual/inconsistent history | keep flags off until S7–S10 conformance/Eval；历史FAIL不改写 | 段成威 | blocks G4/local G6 |
| Desktop sidecar/Keychain | supervisor/static safety与synthetic bookmark PASS；真实signed Keychain和actual Host child未运行 | packaged/native lifecycle unknown | authorized signed-like local E2E | 段成威 | blocks G4/local G6 |
| production identity/infra | FEAT-125 deferred | no production safety | N/A for DEC-126-022 local-only scope；future online intent must reopen production track and FEAT-125 prerequisites | 段成威 | does not block local G6；blocks any production claim |

## 11. 结论

- Requirements package：G1/G2 Passed；原G2A作为历史批准保留。DEC-126-023方案C Accepted、Q-017 Resolved、replacement source complete；DEC-126-024 final G2A Pending。DEC-126-021/022仍Accepted；Draft PR #1与`c000a024`保持不变。
- Code Complete：No。S4–S6 Conditional / Corrective Closure Required，G3 Partial；LIA-126-002已暂停，S7–S11、四组件E2E、G4与Owner G6均未完成。
- 验证人：Codex（文档事实与结构）；最终 Reviewer 为段成威。
- 日期：2026-08-02。
- 结论依据：replacement source/fixture/generated三向核对、post-commit全门禁、三仓实现审查及local checkpoint。新source shape满足content-free边界，但业务P1与runtime conformance仍未关闭；本轮无MiniMax、业务/Runtime修改、remote write、push/merge/tag/publish/deploy或生产证据。
