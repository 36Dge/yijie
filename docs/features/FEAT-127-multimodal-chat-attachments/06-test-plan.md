# FEAT-127 测试与 Eval 计划

## 1. 策略与门槛

- 风险：high；涉及 confidential 文件、跨仓 wire、SQLCipher migration、native parser 与 Runtime input。
- 阻断：contracts generate/lint/test/breaking/v1 equality；Host lint/race tests/runtime no-model conformance；Desktop lint/unit/Rust clippy/tests/build；migration/security/failure tests；UI light/dark/minimum viewport。
- 类生产依赖：本地 SQLCipher、loopback fake Host、固定 Runtime schema/binary handshake；不需要云资源。
- NOT RUN：真实 MiniMax turn、生产身份/部署、签名/公证、真实商家文件、云 DLP/AV、生产性能与 AI 答案质量。
- 状态门槛：自动化、合成 E2E 和视觉 harness 通过后默认只可声明“Desktop 人工验收候选已准备”。2026-08-19 用户批准 `EXC-127-001` 后，仅当前本地 G3 可在人工结果仍为 `PARTIAL`、可访问性仍为 `NOT RUN` 的情况下记为 `PASS WITH EXCEPTION`；G4 还必须独立满足 contract pin/conformance、审查、提交和 Reviewer approval。当前这些条件已完成，因此 G4 可记 `PASS for local candidate`，但不得改写为完整人工验收或发布就绪。

## 2. AC 追踪矩阵

| AC | Test IDs | Layer | Pass evidence |
|---|---|---|---|
| AC-001 | UI-001, A11Y-001 | Vue/visual | exactly one plus before permission; 40px; tooltip/name |
| AC-002 | IPC-001, SEC-001, STORE-002..003 | Rust/Vue integration | picker/drop call same importer; response/state contain no path; command/event terminal remains monotonic |
| AC-003 | PARSE-001..006 | Rust unit/integration | 10 MiB edge, archive/macro/symlink/directory/magic/container reject |
| AC-004 | DB-002, HOST-002, RT-001 | DB/Host/Runtime adapter | ordered text/file/image persisted and mapped |
| AC-005 | UI-003, DB-003 | Store/DB | attachment-only accepted and fallback title safe |
| AC-006 | DB-004, HOST-003, RES-001 | transaction/idempotency | rollback keeps draft; lost response replay has one turn/binding |
| AC-007 | DB-005, DB-008, IPC-003, STORE-001 | migration/history/store | reopen returns target-scoped ordered metadata; old text synthesized; failed reload never publishes an empty usable draft |
| AC-008 | TTL-001..003 | DB/integration | exact boundary clears BLOB/chunks and blocks dispatch |
| AC-009 | DB-006 | DB cleanup | cascade rows absent after session delete/checkpoint path |
| AC-010 | UI-002, UI-004, A11Y-001..003 | visual/manual | light/dark, 1180x760, five observable stages, keyboard, zoom, VoiceOver |
| AC-011 | CONTRACT-001..003, MIG-001 | contract/migration | v1 equality, v1-v5 upgrade retention, explicit forward-only downgrade boundary |

## 3. Contract 与 Conformance

| ID | Scenario | Expected |
|---|---|---|
| CONTRACT-001 | compare to supported `f16a497...` | no structural breaking |
| CONTRACT-002 | v1 selected path/reference closure | byte-semantic equality |
| CONTRACT-003 | canonical v2 fixture + invalid variants | closed union, UUID, limits, unknown fields enforced |
| CONTRACT-004 | Desktop exact contract checkout、OpenAPI/fixture/adapter/readiness digest、exception expiry | drift/comment spoof/expired exception fail closed；Rust canonical serialization executes |
| HOST-001 | strict HTTP decode, body cap, unknown field | 400 safe `invalid_request`; Runtime not called |
| HOST-002 | ordered blocks with image/file/text | Runtime receives same order and bounded values |
| HOST-003 | same operation/same input then conflict input | original turn returned once; conflict is 409 |
| HOST-004 | aggregate 11 attachments, >10 MiB image, >256 KiB context | fail before Runtime |
| HOST-005 | malformed base64/media/size/SHA | fail safe; no content in store/log/error |
| RT-001 | generated Runtime request fixture | canonical `UserInput::Text/Image` mapping matches 0.144.6 schema |

Unknown response fields remain tolerated by Desktop transport adapter; unknown content `type` is rejected fail closed because the v2 union is intentionally closed.

## 4. Parser 与 Native 边界

| ID | Scenario | Expected |
|---|---|---|
| PARSE-001 | exactly 10 MiB / 10 MiB + 1 | first accepted if format valid; second rejected |
| PARSE-002 | `.jpg` containing PNG, malformed PDF, invalid UTF-8/NUL | `attachment_content_invalid`/parse error |
| PARSE-003 | ZIP/RAR/7Z/TAR/GZ, SVG, executable, macro Office | unsupported without persisted row |
| PARSE-004 | symlink, directory, FIFO, relative/duplicate/NUL path | rejected by native boundary |
| PARSE-005 | OOXML traversal, duplicate entry, VBA/bin, >512 entries, >32 MiB expansion | bounded reject; no panic/OOM |
| PARSE-006 | valid synthetic PNG/PDF/TXT/MD/CSV/JSON/YAML/XML/HTML/RTF/DOCX/XLSX/PPTX | correct kind/media/chunks/hash/TTL |
| SEC-001 | inspect serialized IPC/store/error/log capture | no raw path, body, chunks, data URL or digest leak |

All fixtures are generated, minimal and content-free with respect to real sellers.

## 5. Database、Migration 与 TTL

| ID | Scenario | Expected |
|---|---|---|
| MIG-001 | `migrations.rs` authoritative catalog applies `0006_chat_attachments` then `0007_chat_attachment_draft_targets` to empty/populated v1-v5 and populated v6；repeat startup；v5 reader opens copied v7 DB | ledger name/SHA and FK checks pass；`user_version=7`；old text/bound history intact；unroutable v6 ready drafts removed；v5 reader rejects future schema |
| DB-001 | import set transaction fails midway | no partial attachments/chunks |
| DB-002 | bind ordered blocks | one message, unique ordinal and attachment binding |
| DB-003 | no text + ready attachment | valid message and safe attachment-name title |
| DB-004 | reused operation/binding or injected commit failure | idempotent original or full rollback |
| DB-005 | close/reopen/load history | safe ordered metadata; no BLOB in DTO |
| DB-006 | permanent session delete | attachment, chunk and block rows absent; unrelated session intact |
| DB-007 | remove ready vs bound attachment | ready row deleted; bound/expired removal refused |
| DB-008 | several attachments share one imported second, then reopen/remove/append across new/session targets | target-scoped `draft_ordinal` starts at `MAX + 1`, preserves exact selection order without UUID/time tie-breaking, does not renumber gaps, and clears on bind |
| TTL-001 | `now = expires_at - 1`, `=`, `+1` | available before; expired at/after boundary |
| TTL-002 | expire bound | chunks deleted, BLOB NULL, metadata retained |
| TTL-003 | expire ready and dispatch race | ready row deleted; expired context never sent |

Rollback evidence uses a copied database: old readers must reject the v7 copy, while the migration rehearsal preserves a separate pre-migration encrypted backup for application rollback. No destructive down migration is attempted.

## 6. UI、Store 与 IPC

| ID | Scenario | Expected |
|---|---|---|
| UI-001 | composer normal/disabled/importing/error/ready | stable layout, one plus, stage text, remove/reselect; no attachment retry action |
| UI-002 | 1180x760 light/dark and long UTF-8 filename | no overlap/shift; ellipsis; send remains reachable |
| UI-003 | only attachment, mixed content, empty, >10 attachments | only valid cases enabled; order preserved |
| IPC-001 | picker/drop same synthetic paths | same command result shape and validations |
| IPC-002 | malformed schemaVersion/request/response | strict typed error, no partial state mutation |
| IPC-003 | v2 history plus legacy text message | blocks parsed; legacy text synthesized |
| STORE-001 | bind/new/session `listDraftAttachments` first fails, then retry succeeds | preserve target/session identity without publishing an empty usable draft；send/create/picker/drop stay closed；explicit page retry reloads the same target and session retry completes subscription/history/resync before reopening |
| STORE-002 | native command success and aggregate progress stream disagree, arrive out of order, duplicate, use a different item count, or omit stages/terminal state | accept only current operation/epoch and contiguous valid events；synthesize missing success stages when safe；on irreconcilable result remove newly persisted drafts and fail closed |
| STORE-003 | native command rejects before its terminal event, then queued/intermediate events arrive late | synthesize the legal failure prefix plus `error_terminal` from typed issue/item count；late events cannot overwrite terminal state；dismissal is required before another import |
| UI-004 | native success events arrive immediately or are synthesized | `queued -> importing -> parsing -> indexing -> ready` each remains observable for at least 220ms；ready clears only after its interval；error terminal persists |
| A11Y-001 | keyboard Tab/Enter/Escape/focus return | visual order and visible focus |
| A11Y-002 | VoiceOver names/status | plus/remove/status understandable without color |
| A11Y-003 | 200% zoom/reduced motion | no clipping; overlay and status do not animate materially |

## 7. 韧性与失败恢复

| ID | Fault | Expected recovery |
|---|---|---|
| RES-001 | Host accepts turn but response lost | retry same operation ID returns original; no duplicate Runtime call |
| RES-002 | Host unavailable/502 | outbox retries within existing policy; draft/message remains authoritative |
| RES-003 | DB full/read-only/corrupt/migration failure | stable typed error; no UI success or lost draft |
| RES-004 | app restarts after import before send | ready metadata remains locally available until removed/expired |
| RES-005 | cancel picker/drop during session switch or receive a late event after command rejection | old operation/epoch cannot overwrite the new target or a terminal failure |
| RES-006 | Runtime v2 unsupported | fail closed; never strip attachments and silently send text-only |
| RES-007 | last `DatabaseWorker` clone drops while SQLCipher is open | close channel, join the named database thread, then allow connection/process shutdown without exit crash |

## 8. 性能与容量

| Workload | Threshold/stop condition |
|---|---|
| one 10 MiB valid file | bounded memory/read; no unbounded allocation; command completes under test timeout |
| ten attachments | no 11th acceptance; stable UI and DB transaction |
| OOXML adversarial container | stops at declared entry/size limits |
| 512 KiB extracted text | <=128 chunks; Runtime selection <=256 KiB |
| history 50 turns with attachment metadata | no BLOB/data URL returned or decoded |
| instantaneous native import completion | each of five UI success stages remains visible for >=220ms without blocking native persistence |

No production p95 target is claimed from local synthetic tests. Observed durations may be recorded as informational only.

## 9. AI Eval 判定

This feature changes retrieval input but does not change model, prompt, tools or structured output. Deterministic lexical selection and exact Runtime input mapping are tested. Answer-quality Eval is `NOT RUN`: no approved dataset/threshold and no paid-model authorization. Therefore the delivery may claim “attachments reach Runtime input locally” only when no-model conformance proves it; it may not claim answer quality improvement.

## 10. Commands

| Repository | Commands |
|---|---|
| contracts | `pnpm generate`; `pnpm lint`; `pnpm test`; `pnpm breaking <baseline>`; `pnpm check:v1-wire <baseline>` |
| Agent Host | `make lint`; `make test`; focused v2 Go tests; `make runtime-test` without model |
| Desktop | `pnpm lint`; `pnpm test`; `pnpm build`; `cargo fmt --check`; `cargo clippy --all-targets --all-features -- -D warnings`; `cargo test` |
| governance docs | `scripts/check-feature-package.sh`; `pnpm docs:build` in Desktop |

`make runtime-turn-test`, production smoke, signing and deployment remain NOT RUN unless separately authorized.

## 11. PASS/FAIL 与批准

PASS requires completed command, exit 0 and asserted behavior. A skipped test, unavailable environment, truncated output or mock-only path is NOT RUN. Flaky results require root-cause analysis; rerun-to-green is insufficient.

Plan author: Codex, updated 2026-08-19. 用户的本地实现授权覆盖本测试计划作为 G2 候选依据；最终命令结果见 `08-verification-report.md`。独立 Codex audit 只提供技术审查证据；Reviewer 段成威另行明确接受当前本地 G4 证据。两者都不构成完整用户人工验收、release 或生产批准。

## 12. 人工验收与状态声明

| Item | Current state | Completion evidence |
|---|---|---|
| 针对性自动回归 | `PASS` | ready 附件移除后重绑不恢复；10 MiB/10 MiB+1、压缩包；10 项后第 11 项 `too_many` 且原草稿不变；命令与计数见 `08-verification-report.md` |
| Desktop 功能人工验收 | `PARTIAL` | 用户人工通过 picker、仅附件 Runtime、不支持格式提示、修复后图片拖拽、图文文件 mixed send、已发送历史重开、未发送附件草稿重开；移除/边界/容量仅为 `AUTOMATED ONLY` |
| VoiceOver/真实系统 200% 缩放/reduced motion | `NOT RUN` | 自动证据只覆盖 axe、键盘语义、light/dark 与等效 200% CSS viewport；没有真实 macOS/Tauri 手工记录 |
| G3 Slice Complete | `PASS WITH EXCEPTION` | `EXC-127-001` 仅对当前本地候选生效；自动证据不冒充人工，至 2026-11-17 或更早触发失效 |
| G2A contract ready | `PASS WITH EXCEPTION` for local candidate | semantic Owner/consumer review、supported-baseline checks、immutable pin 与 conformance PASS；Rust adapter 由 `EXC-127-002` 管理；tag/supported/release-ready 仍 PENDING |
| G4 Code Complete | `PASS` for local candidate | 两项例外已登记；35 Vitest files / 270 tests、Rust 175 passed / 3 ignored、build/docs、独立复审 P0/P1/P2 清零、Reviewer 批准、提交/推送/干净状态 |
| commit/push/downstream pin | `PASS` | Contracts `747cf740...`、Host `e2f0f5d...`、Desktop `2cb4ffd...` 已按依赖顺序推送并完成提交后重验 |
| tag/merge/release | `PENDING/NOT AUTHORIZED` | semantic/Reviewer 本地批准不等于 Release approval；未创建 tag、PR、merge 或制品 |
| deploy/production smoke/G5/G6 | 当前本地范围 `N/A`，未通过 | 只有未来明确部署授权和环境准备后才能执行 |
