# FEAT-127 验证证据与独立审查报告

> 结论范围：G4 `PASS for local candidate`，受 `EXC-127-001` 与 `EXC-127-002` 约束。2026-08-19 已形成并推送最终 Contracts/Host/Desktop commit 与 downstream exact pin，完成提交后门禁、semantic Owner/consumer review、独立审查、Reviewer 批准、用户部分 Desktop 人工验收及三组针对性自动回归。没有 tag、PR、merge、release artifact、真实模型调用或生产环境证据；G5/G6 未通过。

## 1. 验证上下文

| Repository | Branch | Delivery full commit | Push/worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| `yijie-contracts` | `feat/feat-126-content-free-candidate` | `747cf740f2d91e76e5c1a130e8e009f1efa821b8` | pushed；clean/synchronized | openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Go | 2026-08-19 |
| `yijie-agent-host` | `feat/feat-126-foundation-closure` | `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86` | pushed；clean/synchronized | Go / pinned Codex Runtime 0.144.6 | 2026-08-19 |
| `yijie-desktop` | `feat/feat-126-foundation-closure` | `2cb4ffdd87055e5f70aafacc63479154e0c62cad` | pushed；clean/synchronized | Node / Rust / Cargo | 2026-08-19 |

`yijie` 交付包由包含本报告的提交标识；不在报告正文自引用其自身 commit，避免循环身份。

固定 Runtime manifest：`codex-cli 0.144.6`，binary SHA-256 `98910475280a2a8abc10a1c104d4072358121aee33de5fee3dda75418ccf84c1`，canonical schema tree SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`。

## 2. Baseline 与环境门禁

| ID | CWD | Command | Exit | Result | 说明 |
|---|---|---|---:|---|---|
| BASE-001 | `yijie-contracts` | `git rev-parse HEAD` | 0 | PASS | 本地实现基线 `98e89d...`；受支持 breaking 基线另为 `f16a497...` |
| BASE-002 | `yijie-desktop` | 默认 `make lint` | 2 | EXPECTED BLOCK | 相邻 Contracts 含 tracked candidate changes，`generate:check` 正确拒绝 dirty sibling |
| BASE-003 | `yijie-desktop` | 默认 `pnpm test` | 1 | EXPECTED BLOCK | 同一不可变来源门禁；没有运行 Vitest，不计功能失败 |
| BASE-004 | `/tmp/yijie-contracts-feat127.jYJulc/repo` | `git status --short && git rev-parse HEAD` | 0 | PASS | 干净 Contracts source，供 Host/Desktop 在不读取 dirty sibling 的前提下完成最终复验 |

## 3. 2026-08-18 候选命令记录

| Check | Repository | Command | Exit | Result | Evidence |
|---|---|---|---:|---|---|
| C-GEN | Contracts | `make generate` | 0 | PASS | OpenAPI、Protobuf、9 个 JSON Schema SDK sources generated |
| C-LINT | Contracts | `make lint` | 0 | PASS | OpenAPI/AsyncAPI/JSON Schema/Proto/TS/Go |
| C-TEST | Contracts | `make test` | 0 | PASS | 31 Node tests；Go packages PASS；29 generated files current |
| C-BUILD | Contracts | `make build` | 0 | PASS | regenerate + TypeScript SDK compile |
| C-BREAK | Contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | PASS | OpenAPI、AsyncAPI、JSON Schema 无结构性 breaking |
| C-V1 | Contracts | `pnpm check:v1-wire f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | PASS | Public 2 条与 Host 7 条 legacy v1 path/reference closure equal |
| H-LINT | Agent Host | `make lint`（Contracts source=`/tmp/yijie-contracts-feat127.jYJulc/repo`） | 0 | PASS | gofmt/vet/shell；只读干净 Contracts source |
| H-TEST | Agent Host | `make test`（Contracts source=`/tmp/yijie-contracts-feat127.jYJulc/repo`） | 0 | PASS | contract-check + race/coverage packages |
| H-RACE | Agent Host | `go test -race -count=1 -cover ./...` | 0 | PASS | 强制非缓存；session 79.6%、app 74.0%、codex 71.6% statement coverage |
| H-RUNTIME | Agent Host | `make runtime-test` | 0 | PASS | 固定 Runtime artifact/manifest，无模型请求 |
| H-VERTICAL | Agent Host | `YIJIE_RUN_FEAT126_FAKE_INTEGRATION=1 ... go test ./internal/integration -run '^TestPinnedRuntimeFEAT127MultimodalFakeResponses$' -count=1 -v` | 0 | PASS | 固定 Runtime + 本地 fake Responses；ordered text/image/file turn complete |
| D-LINT | Desktop | `YIJIE_DESKTOP_CONTRACTS_DIR=/tmp/yijie-contracts-feat127.jYJulc/repo pnpm lint` | 0 | PASS | ESLint + repository lint surface；缺口修复后静止工作树复验 |
| D-TEST | Desktop | `YIJIE_DESKTOP_CONTRACTS_DIR=/tmp/yijie-contracts-feat127.jYJulc/repo pnpm test` | 0 | PASS | 33 Vitest files / 261 tests |
| D-RUST-EXIT | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml --all-targets --all-features` | 0 | PASS | 208 passed / 3 ignored by design；92.52s |
| D-BUILD | Desktop | `pnpm build` | 0 | PASS | vue-tsc + Vite production build |
| D-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | VitePress build |
| D-CHECK | Desktop | `cargo check --manifest-path src-tauri/Cargo.toml --all-features` | 0 | PASS | all features compile |
| D-CLIPPY | Desktop | `cargo clippy --manifest-path src-tauri/Cargo.toml --all-targets --all-features -- -D warnings` | 0 | PASS | no warnings |
| D-FMT | Desktop | `cargo fmt --manifest-path src-tauri/Cargo.toml --all -- --check` | 0 | PASS | formatting current |
| D-VISUAL | Desktop | local browser matrix against FEAT-127 visual fixture | 0 | PASS | 1180x760 light/dark、draft queue、drag overlay、expired history、590x380 等效 200%；每视图 axe 0 |
| LOCAL-API | API/Caddy | loopback `18080` 与 HTTPS gateway `9443` health/readiness probes；bearer-less protected request | 0 | PASS | 两条入口均健康/ready；无 bearer 精确返回 401 |

Host fake integration 最初使用相对 Runtime artifact path 时被 Host 的绝对路径安全校验拒绝；改为 `realpath` 得到的绝对 binary/manifest 后通过。该失败保留为安全边界证据，不通过放宽校验解决。

### 2026-08-19 pre-reconciliation 提交与精确 pin 重验

| Check | Repository | Command | Result | Evidence |
|---|---|---|---|---|
| C-FINAL | Contracts | `make generate`; `make lint`; `make test`; `./scripts/check-breaking.sh f16a497e...` | PASS | 31 Node tests + Go packages；新增 `kin-openapi` 整份规范兼容回归；无结构性 breaking |
| H-SYNC | Agent Host | `YIJIE_CONTRACTS_REF=ebdd30f... make sync-contracts` | PASS | lock、OpenAPI snapshot、generated DTO 固定到 `ebdd30f...` |
| H-FINAL | Agent Host | `make lint`; `make test`; `make runtime-test` | PASS | contract-check、race suites、固定 Runtime handshake；无模型调用 |
| D-FINAL | Desktop | `make lint`; `make test`; `make build`; `pnpm docs:build` | PASS | 34 Vitest files / 263 tests；Rust 174 passed / 3 ignored；ESLint、typecheck、fmt、Clippy、Vite/VitePress PASS |
| META-DOC | yijie | `check-feature-package.sh --strict`; `pnpm lint`; `pnpm test`; `bash -n scripts/*.sh` | PASS | package 结构/占位符/manifest/Shell syntax |
| GIT-PUSH | Contracts/Host/Desktop | `git push`; branch/upstream status | PASS | 当时 checkpoint `ebdd30f...`、`673de86...`、`3efed9a...` 均已推送；后续由下表 reconciliation commits 取代 |

首次同步 `bd0dc050...` 后，Host 测试发现文件名 schema 使用 Go/RE2 不支持的负向前瞻。Contracts 在 `ebdd30f...` checkpoint 改为 RE2-compatible pattern + `not enum`，并增加 Go validator 回归。后续 canonical PNG 严格解码问题与 provenance 由 `747cf740...` reconciliation 修复；Host/Desktop 再次精确 pin。该过程没有绕过或关闭校验。

### 2026-08-19 最终 reconciliation 与 G4 关闭

| Check | Repository | Command | Result | Evidence |
|---|---|---|---|---|
| C-RECON | Contracts | `make generate`; `make lint`; `make test`; `make build`; fresh `go test -count=1 ./...`; breaking + v1 equality | PASS | 31 Node tests + Go；canonical PNG decode/size/SHA；full commit `747cf740...`；OpenAPI `3d2f2273...`；fixture `ec464ce5...` |
| H-REPIN | Agent Host | `make lint`; `make test`; fresh `go test -race -count=1 -cover ./...`; `make runtime-test`; `contract-check` | PASS | full commit `e2f0f5d...` 精确 pin `747cf740...`；无模型调用 |
| D-CONTRACT | Desktop | `pnpm generate:check`; contract Vitest；Rust exact canonical serialization | PASS | 2 files / 8 tests；Rust 1/1；OpenAPI/fixture/adapter/readiness digest、comment spoof 与 2026-11-17/18 expiry boundary fail closed |
| D-G4 | Desktop | `make lint`; `make test`; `make build`; `pnpm docs:build`；all-target/all-feature check/clippy/test | PASS | 35 Vitest files / 270 tests；Rust 175 passed / 3 ignored；all-target/all-feature 209 passed / 3 ignored；Vite/VitePress PASS |
| REVIEW-G4 | Desktop/package | 独立只读 diff、契约/证据与负向门禁复审 | PASS | 最终 adapter audit 的 1 个 P1、2 个 P2 已修复；P0/P1/P2 均清零 |
| GIT-FINAL | Contracts/Host/Desktop | push + branch/upstream status | PASS | `747cf740...`、`e2f0f5d...`、`2cb4ffd...` 均 clean 且 `0 ahead / 0 behind`；未创建 tag |
| META-G4 | yijie | feature package `--strict` + `--gate G4`; `pnpm lint`; `pnpm test`; `bash -n scripts/*.sh`; YAML parse; `git diff --check` | PASS | 文档结构/G4 markers、10 仓 manifest/Contract First governance、1 Node test、Shell/YAML/diff 全部通过 |

### 2026-08-19 人工验收后的针对性自动回归

本轮不使用 Computer Use，也不操作 Desktop UI。前三组由测试层自动验证，结果不得改写为人工通过。

| Check | Repository | Command | Result | Evidence |
|---|---|---|---|---|
| D-ACC-FE | Desktop | `pnpm exec vitest run` 对 Store、Composer、Accessibility、chat-client 的 9 个既有 focused cases | PASS | 9 passed；草稿恢复/删除失败保留、达到 10 项关闭入口、remove IPC、键盘语义、axe serious/critical=0 |
| D-ACC-GAPS | Desktop | `pnpm exec vitest run src/stores/chat.store.test.ts -t 'does not restore...\|rejects an eleventh...'` | PASS | 新增 2 passed；成功移除后新 Pinia bind 不再恢复；第 11 个 drop 返回 `too_many`、不调用 native、原 10 项不变 |
| D-ACC-NATIVE | Desktop | 7 条 exact Cargo 命令，完整命令如下 | PASS | 7/7；exact 10 MiB/10 MiB+1、archive terminal、remaining-capacity、IPC error/remove、DB delete/chunk/WAL、reopen/order/append；测试 1.48s，墙钟合计 2.57s |
| D-ACC-FINAL | Desktop | `make lint test build` | PASS | generate check、ESLint、typecheck、fmt、Clippy；34 files / 265 Vitest；Rust 174 passed / 3 ignored；Vite build PASS |

实际 focused 命令如下；命令中的筛选文本均为仓库内真实 test name，不是人工步骤或 UI 自动化：

```bash
pnpm exec vitest run \
  src/stores/chat.store.test.ts \
  src/components/chat/ChatComposer.test.ts \
  src/pages/chat/ChatAccessibility.test.ts \
  -t 'restores the scoped native draft in a new Pinia process without deleting it on dispose|keeps the attachment draft when native removal fails|disables attachment import for every unavailable composer state|renders the project strip and keeps permission and send actions inside the input panel|submits with Enter|allows attachment-only send and exposes terminal recovery through remove and reselect|disables the unified entry and hides drag feedback when sending is unavailable|has no serious or critical axe violations in the ready new-task surface'
pnpm exec vitest run src/api/chat-client.test.ts \
  -t 'uses additive v2 envelopes for attachment metadata and ordered multimodal turns'
pnpm exec vitest run src/stores/chat.store.test.ts \
  -t 'does not restore a successfully removed native draft after restart|rejects an eleventh dropped attachment without mutating the full draft'

cargo test --manifest-path src-tauri/Cargo.toml --lib chat::attachment::tests::filesystem_boundary_accepts_exactly_ten_mib_and_rejects_oversize_and_non_regular_files -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::attachment::tests::native_preparation_reports_minimal_ordered_batch_stages_and_a_terminal_failure -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::attachment::tests::over_capacity_batches_are_rejected_before_any_path_is_opened -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::ipc::tests::attachment_v2_payloads_freeze_capacity_and_remove_contracts -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::database::tests::ready_attachment_removal_is_scoped_idempotent_and_cascades_chunks -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::database::tests::draft_attachment_ordinals_preserve_same_second_import_order_across_reopen -- --exact
cargo test --manifest-path src-tauri/Cargo.toml --lib chat::database::tests::draft_attachment_ordinals_are_target_scoped_and_append_after_removal -- --exact
```

人工结果单独记录：用户通过 picker、仅附件 Runtime、不支持格式提示、修复后图片拖拽、图文文件 mixed send、已发送历史重开和未发送附件草稿重开。未人工执行附件移除后重开、>10 MiB/压缩包、10+1 容量，以及真实 macOS 可访问性；前三项以上述自动回归作为证据，最后一项保持 `NOT RUN`。

### G3 例外决定

用户于 2026-08-19 明确批准 `EXC-127-001`：仅在当前本地候选的 G3 中，允许以上三项 `AUTOMATED ONLY` 证据替代人工补验，并将 VoiceOver、真实系统 200% 缩放和 reduced motion 延期。人工验收状态保持 `PARTIAL`，可访问性手工状态保持 `NOT RUN`，没有被重标为人工通过。该例外至 2026-11-17（含）或 `03-decisions-and-risks.md` 所列任一触发条件更早发生时有效；失效后 G3 回退 `PENDING`。它本身不替代 G2A semantic review 或 G4 Reviewer approval，这两项已另行完成；也不覆盖 merge、tag、release、G5/G6 或生产激活。

## 4. 契约与版本兼容

| 结论 | Candidate identity | Result | 限制 |
|---|---|---|---|
| 源结构与生成无漂移 | Contracts `747cf740...`；OpenAPI `3d2f2273...`；Chat Schema `3f277898...`；canonical fixture `ec464ce5...`；Host generated `862ff4c2...` | PASS | full commit 是 immutable candidate identity；未形成 release tag/artifact |
| Supported baseline breaking check | `contracts-v0.2.0` / `f16a497...` | PASS | 自动结构检查不替代语义 review；人工 semantic review 已另行批准 |
| Producer conformance | Host strict HTTP、closed blocks、idempotency、order、bounds、no persistence | PASS | Host `e2f0f5d...` 通过 `api/contracts.lock` 精确 pin `747cf740...` |
| Consumer conformance | Desktop HostBridge、private IPC schema、history parser、outbox replay、canonical Rust serialization | PASS | Desktop `2cb4ffd...` pin `747cf740...`；private IPC `b03e3c8f...`；adapter `c6e90e0e...`；readiness `9a070251...` |
| Runtime compatibility | fixed Runtime 0.144.6 + local fake Responses | PASS | 没有调用付费模型，不证明答案质量 |
| Gate 2A | immutable full commit + downstream pins + semantic review | PASS WITH EXCEPTION (`EXC-127-002`) for local candidate | Rust generator `N/A` 由有期限 adapter 例外管理；release tag 与 supported/release-ready 仍 PENDING |

## 5. AC 到证据追踪

| AC | 实现/测试摘要 | 结果 |
|---|---|---|
| AC-001 | `ChatComposer.vue` 单一 40x40px plus、Lucide registry、tooltip/accessible name；各视觉视图只有一个 plus，证据含 `visual-ready-file-light-1180x760.png` | PASS |
| AC-002 | picker/drop 共用 native importer；IPC path-free parser、ordered aggregate progress、command/event agreement、迟到导入清理与 drag overlay tests | PASS |
| AC-003 | 10 MiB、archive/macro/directory/symlink/magic、PDF/OOXML adversarial Rust tests | PASS |
| AC-004 | ordered DB blocks、Host mapping、fixed Runtime fake vertical slice | PASS |
| AC-005 | attachment-only store/database tests与安全文件名回退标题 | PASS |
| AC-006 | atomic SQLCipher transaction、same-operation Host replay、invalid 202 recovery、refresh-after-accept regression | PASS |
| AC-007 | close/reopen/history v2、target-scoped draft recovery/stable ordinal、legacy text synthesis、path/body/chunk exclusion | PASS |
| AC-008 | exact TTL boundary、startup all-scope cleanup、expired context exclusion、WAL retry | PASS |
| AC-009 | session cascade、secure delete、checkpoint/truncate recovery tests | PASS |
| AC-010 | light/dark、1180x760、draft queue、drag overlay、expired history、590x380 等效 200% CSS viewport；无横向溢出或控件重叠，每视图 axe 0，keyboard semantics 通过 | PARTIAL：真实 VoiceOver、系统缩放与 reduced-motion 手工检查未执行 |
| AC-011 | v1 wire equality、v1-v5 migration、future schema fail closed、forward-only rollback boundary | PASS |

## 6. 专项验证

| 专项 | 结果 | Evidence / 边界 |
|---|---|---|
| E2E | PASS（本地无模型） | Host fixed Runtime + fake Responses；Desktop Rust fake Host/application path |
| Security/tenant | PASS（合成数据） | owner/tenant binding、path/body/data URL redaction、strict token/loopback/database rules |
| Failure/resilience | PASS | lost response、invalid accepted response、typed conflict、draft reload fail-closed、progress mismatch、late import、DB rollback、WAL busy/worker-exit recovery |
| Migration rehearsal | PASS | v6 expand + v7 target migration/idempotency、v1-v5 preservation、populated-v6 cleanup、v5 reader future-schema rejection |
| Performance | PARTIAL | byte/count/depth/time budgets and 10k reducer tests；无生产 p95/内存基准 |
| AI Eval | NOT RUN | 未授权真实模型；无批准 dataset/quality threshold；只证明输入映射 |
| Visual/accessibility | PARTIAL | 1180x760 light/dark、draft queue、drag overlay、expired history、590x380 equivalent 200%；plus 恰好一个且为 40x40px；每视图 axe 0，无水平溢出/控件重叠；VoiceOver/真实系统缩放/reduced motion NOT RUN |
| Desktop manual acceptance | PARTIAL | 人工 PASS：picker、仅附件 Runtime、不支持格式提示、修复后图片拖拽、mixed image/file send、已发送历史重开、未发送附件草稿重开；移除/边界/容量为 AUTOMATED ONLY；真实 macOS accessibility NOT RUN |

视觉证据位于 `references/visual-*.png`。加号参考 `references/plus-entry.png` 的 SHA-256 与 1086x210 尺寸已复核；红框只作为位置标注。

## 7. Diff 与依赖完整性

- 各仓 `git status`、`git diff --stat` 与 `git diff --check` 已检查；改动范围限于 FEAT-127 及 Desktop 既有 FEAT-126 overlap。
- Contracts 生成物由仓库 generator 重建并通过 current check；没有手改 generated SDK。
- `pnpm-lock.yaml` 使用声明的 `pnpm@11.7.0` 重新解析确认 current；Ajv 及其传递依赖之外的 peer key 重写是 pnpm 的一致解析结果。
- `Cargo.lock` 对应显式固定的 base64/flate2/infer/image/pdf-extract/quick-xml/zip 依赖；all-feature check/clippy/test 通过。
- SQLCipher migrations：`0006_chat_attachments.sql` SHA-256 `60b08d6c...`；`0007_chat_attachment_draft_targets.sql` SHA-256 `aae67ca5...`。最终 schema v7，forward-only，不提供 destructive down migration。
- 视觉夹具曾漏设 `draftTarget`/`draftTargetReady`，导致验收页把可用 composer 错画成禁用；已在 `tests/visual/feat-127/main.ts` 初始化权威草稿 target 状态并复验全部视觉矩阵。该问题只影响证据夹具，不掩盖或改写生产 Store 行为。
- 未发现 `.only`、`.skip`、secret、真实 PII、本机绝对路径、调试后门或冲突标记进入 FEAT-127 变更。
- 三个实现仓的最终 delivery commit 已形成、可审查、clean 且与 upstream `0/0` 同步；包含本报告的元仓提交关闭交付包 worktree，但不在正文自引用自身 SHA。G2A/G3 例外、semantic review 与 Reviewer 批准均已记录，因此 G4 不再有开放阻断。

## 8. 独立 Review Findings

| Finding | Severity | 触发与影响 | 处理与复验 |
|---|---|---|---|
| REV-127-001 | P1 | Host 接受 v2 turn 后返回非法 202，Desktop 可能把未知结果永久失败或重复发送 | 新增 `AcceptedResponseInvalid`；同 body/operation 有界重放，typed conflict 不重试；tests PASS |
| REV-127-002 | P1 | TTL/delete 已提交但 WAL truncate busy/进程退出，旧帧可能保留 confidential bytes | open 时无条件 pending checkpoint；零行变化也重试；busy/startup tests PASS |
| REV-127-003 | P1 | PDF Form XObject 自递归导致栈溢出 | active set + 16 层限制；recursive/depth tests PASS |
| REV-127-004 | P1 | 多页重复引用同一 stream 导致解压/输出引用放大 | 按页面/Form 实际引用累计 4096 streams/32 MiB，bounded writer；amplification test PASS |
| REV-127-005 | P1 | 缺 `/Type /XRef` 的 xref stream 绕过类型扫描 | `startxref` 必须指向 classic `xref`；object/xref stream、`Prev`、加密 fail closed；test PASS |
| REV-127-006 | P1 | OOXML 信任 central directory size，伪造元数据造成解压膨胀 | 按实际读取字节核对声明、单项/总量/ratio；forged-size test PASS |
| REV-127-007 | P1 | native 已接受 create，但 sidebar refresh 失败，UI 保留 prompt 且附件引用已清，重试可能重复/降级纯文本 | accepted command 与 projection refresh 分离；新 session projection upsert；Vitest regression PASS |
| REV-127-008 | P1 | `DatabaseWorker` 丢弃 `JoinHandle`，测试/应用退出时后台 SQLCipher connection 可与库级 `atexit` 清理竞态并 `SIGSEGV` | 最后一个共享 worker drop 先关 channel 再 join；确定性 thread-lifetime test；连续三轮完整 Rust tests 且无新 crash report |
| REV-127-009 | P1 | 初始或 session 草稿 reload 失败后 composer 仍可能允许发送/导入，造成持久草稿被遗漏或发错 target | `draftTargetReady` fail-closed；new/session 显式恢复重载；send/picker/drop 与页面 retry regressions PASS |
| REV-127-010 | P1 | 同一秒导入依赖 timestamp/UUID 排序，重开后 Content Block 次序可能偏离用户选择次序 | v7 target-scoped `draft_ordinal`、唯一约束与 append 规则；same-second/reopen/remove tests PASS |
| REV-127-011 | P1 | native command 成功但 progress 缺失/乱序/数量不一致时 UI 可展示虚假 ready 或永久 importing | command 与 ordered aggregate terminal event 必须一致；synthetic terminal failure、持久行清理、minimum display/dismiss tests PASS |
| REV-127-012 | P1 | `ChatPage` 在注册拖拽监听前调用未授权的 `scaleFactor()`，异常被吞后 drop 完全无响应 | 移除该调用并直接使用 macOS/Wry AppKit point 坐标；mock 不再提供 `scaleFactor`，focused 14/14 与全量门禁 PASS；用户已完成修复后图片拖拽复验并通过 |
| REV-127-013 | P1 | Contracts 文件名正则含负向前瞻，Redocly 通过但 Host 的 Go OpenAPI validator 拒绝，阻断 Host 启动测试 | 改为 RE2-compatible pattern + `not enum`；新增整份 OpenAPI `kin-openapi` Go validation test；Contracts/Host 全量门禁 PASS |
| REV-127-014 | P1 | Desktop JS contract gate 只读取 Rust adapter 文件但不约束内容，serialization test 被删除或忽略后可能误绿 | lock 固定完整 `host_bridge.rs` SHA `c6e90e0e...`；实际校验 digest；Rust exact canonical test 1/1 与完整 suite PASS |
| REV-127-015 | P2 | readiness commit substring 可由注释中的期望值伪装，真实常量错误时仍可能通过 | lock 固定 `chat/mod.rs` SHA `9a070251...`，先核对 reviewed digest 再检查唯一声明；comment-spoof negative test PASS |
| REV-127-016 | P2 | `EXC-127-002` 只保存到期字符串，不比较当前日期，到期后门禁仍可能放行 | 使用本地日历日期做 inclusive expiry；2026-11-17 PASS、2026-11-18 fail closed，非法日期 negative test PASS |

审查由与实现切片分离的 Codex audit 角色及主代理 diff 审查完成；最终复验后 P0/P1/P2 全部清零，没有用例外豁免缺陷。它们不是段成威的人工批准来源；段成威在当前任务中另行明确接受 semantic Owner/consumer review 与本地 G4 Reviewer 结论。`EXC-127-001/002` 只治理已列明的证据/adapter 边界，自动回归没有被重标为人工验收。

## 9. 未验证项与残余风险

| Item | 原因与风险 | 补验证条件 | Owner | 阻断 |
|---|---|---|---|---|
| Desktop 功能人工验收 | 已记录的 picker/仅附件/drop/mixed send/两类 reopen 通过；移除/边界/容量只有自动证据，完整人工验收未形成 | `EXC-127-001` 失效或要求完整人工证据时，在当时的 Desktop 候选补验 automated-only 场景并记录 | Product Owner | 例外有效期内不阻断本地 G3；触发后阻断 G3 |
| Contract release identity | semantic review、full commit 与 downstream pin 已完成，但无 `contracts-v0.3.0` tag，candidate 不是 supported/release-ready | 若进入正式发布，经独立发布批准后创建并核对不可移动 tag/digest，再切换 release provenance | Contracts/Release Owner | 不阻断本地 G4；阻断 release/G5 |
| Temporary Rust adapter | 没有批准的 Rust OpenAPI generator，未来 source/schema 漂移可能误解释 wire | `EXC-127-002` 到期、digest/schema 变化、approved generator 出现或进入 signed/release candidate 时移除或重审 | Desktop/Contracts Owner | 例外有效时不阻断本地 G4；触发后阻断 G2A/G4/release |
| 现代/增量/加密 PDF | 为控制 parser 风险采取 fail closed，部分常规 PDF 会被拒绝 | 独立评估隔离 parser/子进程资源限制与兼容 dataset | Client Owner | 否，已记录兼容边界 |
| VoiceOver、真实 200% 系统缩放、reduced motion | 当前自动化只覆盖 axe 与等效 CSS viewport；真实平台问题可能晚发现 | 在真实 macOS/Tauri bundle 手工验收；最晚在签名/可分发候选前完成 | Product/Design Owner | `EXC-127-001` 触发后阻断 G3；始终阻断生产激活 |
| 真实模型答案质量 | 无付费模型授权和 Eval dataset | 批准模型、dataset、阈值后独立 Eval | Product/AI Owner | 质量声明 |
| 签名、公证、生产资源、监控、回滚演练 | 用户明确本期无部署计划 | 进入真实部署准备时执行 G5/G6 | Release Owner | 生产激活 |

## 10. 结论

- FEAT-127 状态：`G4 PASS for local candidate with EXC-127-001/002 / Production Activation Blocked`；自动证据与人工结果严格分开。
- Gate G3：`PASS WITH EXCEPTION`（`EXC-127-001`）；仅当前本地候选适用，人工仍为 `PARTIAL`、真实 macOS accessibility 仍为 `NOT RUN`，不能据此声明完整人工验收或需求关闭。
- Gate 2A：`PASS WITH EXCEPTION`（`EXC-127-002`）for local candidate；semantic Owner/consumer review、immutable pin 与 conformance 已完成。release tag/supported 状态仍 `PENDING`，但不是本地 G2A 前置。
- Code Complete / G4：`PASS` for local candidate；最终 commits 已推送，门禁与独立审查通过，P0/P1/P2 清零，Reviewer 段成威于 2026-08-19 批准。两项例外均有期限和触发条件。
- G5/G6：本地范围 `N/A`，没有被评估或通过；Production Activation Blocked。
- 验证日期：2026-08-19。
