# FEAT-127 验证证据与独立审查报告

> 结论范围：本地 Desktop 人工验收进行中。2026-08-19 已形成并推送实现 commit 与 downstream exact pin，并完成提交后自动复验；没有 tag、merge、release artifact、真实模型调用或生产环境证据。

## 1. 验证上下文

| Repository | Branch | Delivery full commit | Push/worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| `yijie-contracts` | `feat/feat-126-content-free-candidate` | `ebdd30f076614ebc7f5149aebf70e851b81ff32b` | pushed；clean/synchronized | openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Go | 2026-08-19 |
| `yijie-agent-host` | `feat/feat-126-foundation-closure` | `673de86d3d076f4600eb0d0bfb215382677afd72` | pushed；clean/synchronized | Go / pinned Codex Runtime 0.144.6 | 2026-08-19 |
| `yijie-desktop` | `feat/feat-126-foundation-closure` | `3efed9aba5faab90ca3ea397a4d6489890df2026` | pushed；clean/synchronized | Node / Rust / Cargo | 2026-08-19 |

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

### 2026-08-19 提交与精确 pin 后重验

| Check | Repository | Command | Result | Evidence |
|---|---|---|---|---|
| C-FINAL | Contracts | `make generate`; `make lint`; `make test`; `./scripts/check-breaking.sh f16a497e...` | PASS | 31 Node tests + Go packages；新增 `kin-openapi` 整份规范兼容回归；无结构性 breaking |
| H-SYNC | Agent Host | `YIJIE_CONTRACTS_REF=ebdd30f... make sync-contracts` | PASS | lock、OpenAPI snapshot、generated DTO 固定到 `ebdd30f...` |
| H-FINAL | Agent Host | `make lint`; `make test`; `make runtime-test` | PASS | contract-check、race suites、固定 Runtime handshake；无模型调用 |
| D-FINAL | Desktop | `make lint`; `make test`; `make build`; `pnpm docs:build` | PASS | 34 Vitest files / 263 tests；Rust 174 passed / 3 ignored；ESLint、typecheck、fmt、Clippy、Vite/VitePress PASS |
| META-DOC | yijie | `check-feature-package.sh --strict`; `pnpm lint`; `pnpm test`; `bash -n scripts/*.sh` | PASS | package 结构/占位符/manifest/Shell syntax |
| GIT-PUSH | Contracts/Host/Desktop | `git push`; branch/upstream status | PASS | `ebdd30f...`、`673de86...`、`3efed9a...` 均已推送并与当前 upstream 同步 |

首次同步 `bd0dc050...` 后，Host 测试发现文件名 schema 使用 Go/RE2 不支持的负向前瞻。Contracts 在 `ebdd30f...` 改为 RE2-compatible pattern + `not enum`，并增加 Go validator 回归；Host 随后同步最终 commit 并全量通过。该过程没有绕过或关闭校验。

## 4. 契约与版本兼容

| 结论 | Candidate identity | Result | 限制 |
|---|---|---|---|
| 源结构与生成无漂移 | Contracts `ebdd30f...`；OpenAPI `3d2f2273...`；Chat Schema `3f277898...`；Host generated `862ff4c2...` | PASS | full commit 是 immutable source identity；未形成 release tag/artifact |
| Supported baseline breaking check | `contracts-v0.2.0` / `f16a497...` | PASS | 自动结构检查不替代语义/Owner review |
| Producer conformance | Host strict HTTP、closed blocks、idempotency、order、bounds、no persistence | PASS | Host `673de86...` 通过 `api/contracts.lock` 精确 pin `ebdd30f...` |
| Consumer conformance | Desktop HostBridge、private IPC schema、history parser、outbox replay | PASS | Desktop `3efed9a...` pin `ebdd30f...`；private IPC schema SHA-256 `b03e3c8f...` |
| Runtime compatibility | fixed Runtime 0.144.6 + local fake Responses | PASS | 没有调用付费模型，不证明答案质量 |
| Gate 2A | immutable full commit/tag + downstream pins | PENDING | full commit 与 downstream pins 已形成；Owner/consumer 明确 review 与 release tag 未形成 |

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
| Desktop manual acceptance | PARTIAL | picker 与仅附件 Runtime 路径通过；不支持格式的红色提示与预期一致；drop 首次无响应，修复已提交，修复后 drop 及其余步骤待用户复验 |

视觉证据位于 `references/visual-*.png`。加号参考 `references/plus-entry.png` 的 SHA-256 与 1086x210 尺寸已复核；红框只作为位置标注。

## 7. Diff 与依赖完整性

- 各仓 `git status`、`git diff --stat` 与 `git diff --check` 已检查；改动范围限于 FEAT-127 及 Desktop 既有 FEAT-126 overlap。
- Contracts 生成物由仓库 generator 重建并通过 current check；没有手改 generated SDK。
- `pnpm-lock.yaml` 使用声明的 `pnpm@11.7.0` 重新解析确认 current；Ajv 及其传递依赖之外的 peer key 重写是 pnpm 的一致解析结果。
- `Cargo.lock` 对应显式固定的 base64/flate2/infer/image/pdf-extract/quick-xml/zip 依赖；all-feature check/clippy/test 通过。
- SQLCipher migrations：`0006_chat_attachments.sql` SHA-256 `60b08d6c...`；`0007_chat_attachment_draft_targets.sql` SHA-256 `aae67ca5...`。最终 schema v7，forward-only，不提供 destructive down migration。
- 视觉夹具曾漏设 `draftTarget`/`draftTargetReady`，导致验收页把可用 composer 错画成禁用；已在 `tests/visual/feat-127/main.ts` 初始化权威草稿 target 状态并复验全部视觉矩阵。该问题只影响证据夹具，不掩盖或改写生产 Store 行为。
- 未发现 `.only`、`.skip`、secret、真实 PII、本机绝对路径、调试后门或冲突标记进入 FEAT-127 变更。
- 三个实现仓已形成干净、可审查且与 upstream 同步的 commit；元仓只包含本次交付包更新。G3/G4 的剩余阻断是完整人工验收、G2A 与 Reviewer 批准，不再是缺少实现 commit。

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
| REV-127-012 | P1 | `ChatPage` 在注册拖拽监听前调用未授权的 `scaleFactor()`，异常被吞后 drop 完全无响应 | 移除该调用并直接使用 macOS/Wry AppKit point 坐标；mock 不再提供 `scaleFactor`，focused 14/14 与全量 263 Vitest PASS；用户 post-fix retest pending |
| REV-127-013 | P1 | Contracts 文件名正则含负向前瞻，Redocly 通过但 Host 的 Go OpenAPI validator 拒绝，阻断 Host 启动测试 | 改为 RE2-compatible pattern + `not enum`；新增整份 OpenAPI `kin-openapi` Go validation test；Contracts/Host 全量门禁 PASS |

审查由与实现切片分离的 Codex audit 角色及主代理 diff 审查完成，不是段成威的独立人工批准。复验后未发现开放 P0/P1；未形成 P2 例外批准。用户 Desktop 人工验收仍为独立待办。

## 9. 未验证项与残余风险

| Item | 原因与风险 | 补验证条件 | Owner | 阻断 |
|---|---|---|---|---|
| Desktop 功能人工验收 | picker/仅附件路径已通过，但 post-fix drop、mixed send、reopen 与恢复等未完整记录 | 在当前本地 Desktop 继续逐项验收并记录结果 | Product Owner | G3 |
| Contract review/release identity | full commit 与 downstream pin 已形成，但无明确 semantic Owner/consumer review 或 release tag | Owner 完成 review；若进入发布，再创建并核对不可移动 tag | Contracts/Host/Desktop Owner | G2A/G4 |
| 现代/增量/加密 PDF | 为控制 parser 风险采取 fail closed，部分常规 PDF 会被拒绝 | 独立评估隔离 parser/子进程资源限制与兼容 dataset | Client Owner | 否，已记录兼容边界 |
| VoiceOver、真实 200% 系统缩放、reduced motion | 当前自动化只覆盖 axe 与等效 CSS viewport | 在真实 macOS/Tauri bundle 手工验收 | Product/Design Owner | 生产激活 |
| 真实模型答案质量 | 无付费模型授权和 Eval dataset | 批准模型、dataset、阈值后独立 Eval | Product/AI Owner | 质量声明 |
| 签名、公证、生产资源、监控、回滚演练 | 用户明确本期无部署计划 | 进入真实部署准备时执行 G5/G6 | Release Owner | 生产激活 |

## 10. 结论

- Automated manual-acceptance candidate：`READY`；用户 Desktop 人工验收：`PARTIAL/IN PROGRESS`。
- Gate G3：`PENDING`，post-fix drag 与其余人工验收记录形成前不得声明 slice complete 或需求关闭。
- Formal Gate 2A：`PENDING`；full contract commit 与 downstream pins 已形成，仍缺 Owner/consumer review 与 release tag。
- Formal Code Complete / G4：`PENDING`；实现 commit 已干净推送，仍缺完整人工验收、G2A 与 Reviewer 批准。
- G5/G6：本地范围 `N/A`，没有被评估或通过；Production Activation Blocked。
- 验证日期：2026-08-19。
