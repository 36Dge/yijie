# FEAT-136 Demo 验证

> 当前 verdict：D0/Contracts、Host/Desktop source-anchored conformance 与 canonical D4 entrypoint gate repair PASS；Host/Desktop 已形成 clean 本地 commits。Command real-service tranche 已授权但尚未启动（0/3 次真实请求）；Tool D4 BLOCKED/NOT RUN；overall Feature in progress。
>
> 本文不会把 synthetic fixture、source-anchored Host→Desktop conformance 或 component test 写成 Runtime real vertical、真实 Tool producer或视觉实测。

## 1. D0 检查

| Check | Result | 实际事实 |
|---|---|---|
| Feature ID | PASS | 正式 feature 目录创建前无 FEAT-136，ID 可用 |
| schema/profile/exposure | PASS | schema v3 / demo_fast / local |
| Product/UX | PASS | 用户、问题、结果、主流程、7 个 UI 状态与 8 条可判定 Must AC 已冻结 |
| Contract classification | PASS | semantic；closed v4 使用显式协商 v5，不修改 v1 至 v4 |
| Runtime freeze | PASS | 0.144.6、0ce5902e、267 schema、固定 digest、experimentalApi=false |
| Scope exclusions | PASS | Runtime、审批、FileChange/Diff、Artifact producer/产品能力、权限与 Tool producer 未新增或改变；Desktop 仅为 inherited v5 Artifact 事件做 closed-decoder/Unicode 边界兼容；无真实 D4 |
| Tool gap | PASS | generic contract 可做；真实 Tool producer/GS-004 仍 blocked/not run，不阻塞 Command |
| Git protection | PASS | FEAT-138 治理 commit 已独立固化；其它已完成 commits 未改写 |

## 2. D0 与 Contracts focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| yijie | pnpm lint && pnpm test && pnpm feature:audit | 0 | PASS：10 repos、48 tests、15 committed claims；仅预期 legacy v1 warnings；当前包另由 strict D0 gate 直接验证 | 2026-08-29 |
| yijie | strict D0 package check | 0 | PASS：schema v3 / demo_fast / local D0 gate | 2026-08-29 |
| yijie-contracts | scoped generation + repeated generated SHA comparison | 0 | PASS：Buf、Agent Host OpenAPI Go/TS、AsyncAPI、v5 JSON Schema TS；7 项 HASH_MATCH=true | 2026-08-29 |
| yijie-contracts | make lint | 0 | PASS：OpenAPI/AsyncAPI、15 JSON Schema、Buf、TS no-emit、Go vet | 2026-08-29 |
| yijie-contracts | safe Node suite / Go tests / direct TS build | 0 | PASS：63/63 Node（排除 archive fixture test）、go test ./...、tsc | 2026-08-29 |
| yijie-contracts | v1 equality / candidate + published breaking | 0 | PASS：v1 exact；两个 baseline 均无结构 breaking | 2026-08-29 |
| yijie-contracts | diff/protected/generated/semantic review | 0 | PASS：最终无 open P0/P1/P2；commit 3c3000a6fbe2f08ab2131a463a1691e867d661b1 clean | 2026-08-29 |
| yijie-agent-host | `make lint && make test-feat136 && git diff --check` | 0 | PASS：exact contract checker；session/app race tests；runtime compatibility；未读取禁止 fixture blob | 2026-08-29 |
| yijie-desktop | `cargo fmt --all -- --check`；`cargo check --lib`；`cargo test feat136_ --lib`；targeted strict clippy | 0 | PASS：fmt/check；修复后统一 FEAT-136 Rust suite 20/20；`cargo clippy --lib -- -D warnings -A clippy::type_complexity`；原始 strict clippy 仅命中 base HEAD 已存在的 type-complexity baseline | 2026-08-30 |
| yijie-desktop | FEAT-136 domain/API/store + chat component Vitest；`vue-tsc --noEmit`；scoped ESLint；`pnpm build` | 0 | PASS：27 files / 298 tests；typecheck、lint、production build；仅既有 500 KiB chunk warning；不等于真实 App visual | 2026-08-30 |
| yijie-desktop | canonical gate direct checker；repair Vitest；`cargo test feat136_sidecar_ --lib`；runner/release/build focused checks | 0 | PASS：exact Contracts/Host clean checkout；3 files / 27 Node tests；sidecar 2/2；`bash -n`、release env、Skill resource boundary、fmt/check/clippy/typecheck/lint/diff check；独立 repair review 无 P0/P1/P2 | 2026-08-30 |
| Host→Desktop | exact schema/11 ordinary fixtures byte comparison + producer/consumer focused suites | 0 | PASS：Host/Desktop schema SHA-256 均为 `2f773dd6dc60bc7dc01bcdb434447e945e0a98317534498f54325fcdabb27008`，11 个普通 fixture 逐字节匹配 exact Contracts commit；不是 live Runtime D4 | 2026-08-30 |

## 3. Host→Desktop 验证矩阵

| Area | Required evidence | Current result |
|---|---|---|
| Command started/output/completed | canonical safe fixtures + Host mapper + Desktop decoder/reducer | focused source conformance PASS；real Runtime D4 NOT RUN |
| Command failed/declined | closed status/error + persistence/hydration | focused source conformance PASS；real failure D4 NOT RUN |
| Duplicate identity | same event_id consumed once | Host replay + Desktop event-ID reducer PASS |
| Legal duplicate text | identical text with distinct event_id retained twice | Host/Desktop focused tests PASS |
| Output cap/truncation | 16 KiB delta、256 KiB complete/head-tail/unavailable snapshot、compact SSE 1 MiB | Host projection + Desktop DB/UI decoder PASS |
| Secret/path boundary | allowlist、redaction before caps、closed cwd、copy safe output | Host sanitizer + Desktop parser/component tests PASS；real content NOT RUN |
| Tool progress/result/error | bounded metadata-only stable projection | producer/consumer source tests PASS；real Tool BLOCKED/NOT RUN |
| Unknown Tool/event | fixed unknown sentinel；unknown variant fail-closed + resync | Host projection + Desktop decoder/application PASS |
| V5 closed decoder | exact variants/null/Unicode char+UTF-8 boundaries | focused Desktop Rust/TS PASS；v1-v4 path preserved |
| Completed reconciliation | authoritative completed snapshot and late-delta rule | Host mapper + Desktop reducer/SQLCipher hydration PASS |
| Mixed history | populated v9→v10、legacy/v4/v5 Turn authority | additive migration + IPC/adapter/store tests PASS；旧行未伪装 v5 |
| v1-v4 compatibility | named-family isolation + v1 wire equality + dual breaking baselines | PASS |
| FEAT-138 exclusion | closed schema/proto/event/generic allowlist；不创建 FileChange/Diff fixture | PASS |

## 4. Must AC 状态

| AC | Result | 当前证据边界 |
|---|---|---|
| AC-001 | PENDING（Host/Desktop focused PASS） | 真实安全只读 Command D4 NOT RUN |
| AC-002 | PENDING（source conformance PASS） | 真实 replay vertical NOT RUN |
| AC-003 | PENDING（reducer/DB/hydration PASS） | 真实 reopen vertical NOT RUN |
| AC-004 | PENDING（sanitizer/closed consumer PASS） | 真实 Runtime output boundary NOT RUN |
| AC-005 | PENDING（generic source conformance PASS） | 真实 Tool producer/Owner blocked |
| AC-006 | PENDING（unknown/resync focused PASS） | 真实 recovery vertical NOT RUN |
| AC-007 | PENDING（migration/mixed hydration focused PASS） | 真实 App reopen NOT RUN |
| AC-008 | PENDING（component/a11y PASS） | light/dark、1180×760、200% visual NOT RUN |

所有 Must AC 保持 pending。Host/Desktop source conformance PASS 后也不得把本表改为完整 Feature PASS。

## 5. 安全未执行项

- 未执行强杀、故障注入、权限破坏、可执行文件/binary 替换、fixture 提取或新增攻击载荷；这些行为由长期安全条款禁止。
- 初始标准门禁审计中，在识别前曾各调用一次 `make generate`、`node scripts/check-generated.mjs`、`make test`、`make build`；它们会创建或读取仓库预存 Zip Slip archive fixture。其机械 exit-0 结果不接受为 FEAT-136 证据，识别后未重跑，并改用定向生成、重复 digest、63 个非 archive Node tests、完整 Go tests 与 direct TS build。
- Command D4 的 Provider/模型请求已获最多 3 次授权，但当前为 0/3，尚未启动真实 Command；MCP Tool、生产写或公网访问均未执行。代码构建/测试仅正常读写各仓构建缓存与私有测试数据库。
- 未执行 FileChange/Diff synthetic event 或 fixture；不存在性只通过 source allowlist 静态审计证明。
- 未运行仓库全量 Rust/composite suite，因为其中存在长期安全条款禁止的权限破坏、故障/攻击与危险 archive fixture；使用 `cargo check`、命名聚焦 Rust tests、带单一既有 baseline allowance 的 strict clippy、TS/Vue scoped suite替代。原始 `cargo clippy --lib -- -D warnings` 仅在 HEAD 已存在的 `database.rs` type-complexity 上失败；影响是未覆盖与 FEAT-136 无关的全仓测试，也未把该既有 lint 债务伪报为通过。
- 未运行真实 App light/dark、1180×760、200% 视觉矩阵。影响：组件结构、键盘和 aria 有自动化证据，但没有真实 WebView 截图/交互证据。
- 影响：本批只能证明 Contracts 与 Host/Desktop 本地实现的确定性 source conformance，不能证明真实 Runtime、异常进程 cleanup 或 D4。

## 6. Worktree 与 diff

- yijie 先以 67f219b6cf825357285215fcbaafb33c3978acb3 固化 FEAT-138 owner exclusion，再以 c7bc206e89692b591eb044af09de21fdb4f1154d 固化 FEAT-136 D0/Contracts slice；本次 source-conformance evidence commit 基于后者。
- yijie-contracts 起点：feat/feat-136-desktop-command-tool-items@3832a6c5e99b2a6365f193280fdb887c8fdbc2de；最终 immutable local commit：3c3000a6fbe2f08ab2131a463a1691e867d661b1，clean。
- Host 起点精确为 b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe，当前 clean commit 为 83d3163e21579042d2cc21f303e943946ff97eb0。
- Desktop 起点精确为 fc52ef33cdf040d9b6e8d71bd7498811c5c38c51；core commit 为 69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba，canonical repair clean HEAD 为 65ee3062833ef3d185511599d8f3a4018f635369。
- Runtime 保持只读 clean；Contracts 仍为 exact clean commit。所有 commits 仅本地，未 amend/push/tag/merge。
- 最终 diff review 已覆盖 core 与 10-file canonical repair：Desktop 无剩余 P0/P1/P2；Host 无 P0/P1，并保留 active-item count cap 的后续 P2。

## 7. 结论

- D0：PASS。
- Contracts slice：COMPLETE / PASS（safety-compliant scoped gate）。
- Host/Desktop implementation：本地 source-complete；最终聚焦门禁与独立 diff review PASS，clean local commits 已形成。
- Host→Desktop source-anchored conformance：PASS；不等于 real service。
- Real Command / D4 tranche：已明确授权，当前 NOT RUN / 0 of 3；source evidence 固化后通过 canonical `pnpm tauri:demo-fast:stable` 执行。
- Real Tool / D4：BLOCKED / NOT RUN，等待 producer/Owner。
- FEAT-136 overall：IN PROGRESS；不是 usable、implementation complete 或 Epic complete。
