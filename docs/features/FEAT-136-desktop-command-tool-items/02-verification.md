# FEAT-136 Demo 验证

> 当前 verdict：D0/Contracts、Host/Desktop source-anchored conformance 与 canonical D4 entrypoint gate repair 保持 PASS；原真实 Command D4 保持 FAIL。追加的 failed lifecycle RCA 已 PASS 并定位 fixed Runtime pre-emitter early return，但 repair 因 Runtime freeze 为 BLOCKED。RCA 本轮 Provider/模型调用 0 次，fresh D4 新额度 NOT REQUESTED、fresh D4 NOT RUN；Tool D4 BLOCKED/NOT RUN；overall Feature active / in progress。
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
| Scope exclusions | PASS | Runtime、审批、FileChange/Diff、Artifact producer/产品能力、权限与 Tool producer 未新增或改变；Desktop 仅为 inherited v5 Artifact 事件做 closed-decoder/Unicode 边界兼容；真实 D4 未扩大到 Tool |
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

## 3. 真实 Command D4 调用证据

| Call | 安全设置 | 实际结果 |
|---|---|---|
| Call 1 | canonical gates 开启；既有 bookmark 目标仍是非 Git 的历史空 smoke 目录；只使用两个 allowlisted 只读 Command 形式 | 两个结果均 exit 128；无 Command Item。归类为环境/项目绑定失败，不冒充功能 PASS |
| Call 2 | 同一 bookmark 精确目标已初始化为无 remote 的隔离 Git repo；仅一个 benign untracked 文件；恰好两次 `exec_command`，参数逐字匹配 allowlist | 结果为 exit 0 / exit 128，无第三条命令；只有成功结果形成 completed Command Item，失败结果没有 failed Item/stable error |
| Call 3 | 只使用一次 allowlisted missing-ref 失败形式，无额外命令 | exit 128；仍无 Command Item，仅过程/未分类消息 |

Call 2/3 是当前用户在 Call 1 后明确允许的追加真实请求。Call 1→2 重复两个允许形式以验证修复后的项目绑定，Call 2→3 重复失败形式以隔离投影缺口；没有自动、隐式、越界或超出 3/3 授权的重试。

| Area | Result | 脱敏证据边界 |
|---|---|---|
| Canonical v5 gate | PARTIAL PASS | FEAT-134/136 dependent gates 实际开启，success Command 的 v5-only 投影可见；没有检查或记录握手/Runtime wire，不宣称 wire-level negotiation |
| Success Command | PARTIAL PASS | completed、exit 0、duration 0、安全 cwd 与脱敏输出可见；started/output delta 因执行过快未直接观察 |
| Failed Command | FAIL | 两个正常 exit 128 结果均没有 failed Command Item 或 stable error |
| Command cardinality | FAIL | 三次调用共 5 个允许的命令执行结果只形成一个 Command Item；其中有效 Git 绑定下 3 个结果也只形成一个 Item，不满足每个 Command 恰好一次 |
| event identity/reconciliation | NOT OBSERVED | 真实 event_id 幂等、completed authoritative reconciliation、late event 不回滚均未独立观察 |
| replay | NOT OBSERVED | 正常流程未自然出现 replay；未断连、注入或伪造 |
| SQLCipher hydration | PASS（局部） | 正常 Cmd+Q、runner exit 0、canonical 重开后恰好恢复一个 success Command Item，未重复；最终再次正常 Cmd+Q，runner exit 0 |
| Host post-run metadata | PASS（局部） | App/Host stopped、loopback 端口 idle；bbolt format 2、store schema 4、7 个预期 bucket、unknown/malformed 0；14/14 session safe projection 可解析，唯一 latest session 为 idle/completed 且无 active turn |
| Item UI/a11y | PASS（局部） | success Item 的折叠、键盘、状态文字、AX live announcement 与安全复制 live 可见；状态图标只有 component 证据，未单独做 live 判定 |
| light / 200% | PASS（局部） | 当前 light 主题 live 可见；键盘缩放到 AX 明确的 200% 后仍可键盘/AX 访问，并正常恢复 100% |
| 1180×760 / dark | NOT RUN（live） | 源码配置静态覆盖 width 1180、height 780、minWidth 1180、minHeight 760，但未精确调整到 1180×760；dark 跟随系统外观，本轮未更改系统设置 |
| Command Item / evidence safety | PASS（局部） | Command Item 未暴露 producer raw command、绝对路径、secret、raw bookmark 或 Runtime wire；四文件与保留截图/证据不记录命令字面量、路径、prompt 或 wire |
| Whole WebView no-raw | FAIL | 用户消息为指定 allowlist 而显示了用户亲自输入的命令文本；这不是 producer 投影泄漏，但意味着不能声称整个 WebView 不含任何 raw command |

原真实调用额度 3/3 已耗尽。由于 failed lifecycle、stable error、每命令一次与整个 WebView 的字面 no-raw 标准不成立，Command D4 verdict 为 **FAIL**。failed lifecycle RCA 阶段没有发起新调用；fresh D4 只有在合法修复和复审通过后才可单独申请新额度，当前未满足。

## 4. Host→Desktop 验证矩阵

| Area | Required evidence | Current result |
|---|---|---|
| Command started/output/completed | canonical safe fixtures + Host mapper + Desktop decoder/reducer | focused source conformance PASS；真实 success completed 可见，started/delta 未直接观察 |
| Command failed/declined | closed status/error + persistence/hydration | focused source conformance PASS；真实 failed lifecycle/stable error FAIL |
| Duplicate identity | same event_id consumed once | Host replay + Desktop event-ID reducer PASS |
| Legal duplicate text | identical text with distinct event_id retained twice | Host/Desktop focused tests PASS |
| Output cap/truncation | 16 KiB delta、256 KiB complete/head-tail/unavailable snapshot、compact SSE 1 MiB | Host projection + Desktop DB/UI decoder PASS |
| Secret/path boundary | allowlist、redaction before caps、closed cwd、copy safe output | Host sanitizer + Desktop parser/component tests PASS；真实 success Item 仅见安全 cwd 与脱敏输出 |
| Tool progress/result/error | bounded metadata-only stable projection | producer/consumer source tests PASS；real Tool BLOCKED/NOT RUN |
| Unknown Tool/event | fixed unknown sentinel；unknown variant fail-closed + resync | Host projection + Desktop decoder/application PASS |
| V5 closed decoder | exact variants/null/Unicode char+UTF-8 boundaries | focused Desktop Rust/TS PASS；v1-v4 path preserved |
| Completed reconciliation | authoritative completed snapshot and late-delta rule | Host mapper + Desktop reducer/SQLCipher hydration PASS |
| Mixed history | populated v9→v10、legacy/v4/v5 Turn authority | additive migration + IPC/adapter/store tests PASS；旧行未伪装 v5 |
| v1-v4 compatibility | named-family isolation + v1 wire equality + dual breaking baselines | PASS |
| FEAT-138 exclusion | closed schema/proto/event/generic allowlist；不创建 FileChange/Diff fixture | PASS |

## 5. Must AC 状态

| AC | Result | 当前证据边界 |
|---|---|---|
| AC-001 | FAIL（focused tests PASS） | success completed 可见，但两个 exit 128 结果无 failed Item；started/delta 未直接观察 |
| AC-002 | PENDING（source conformance PASS） | 真实 event_id/replay 未独立观察；normal replay NOT OBSERVED |
| AC-003 | PENDING（reducer/DB/hydration PASS） | success Item 重开后恰好一次；Host metadata 证明 session 终态 reconciliation/无 active turn，但无 Command event journal，late event 未独立观察 |
| AC-004 | FAIL（sanitizer/closed consumer PASS） | success 安全投影可见，但两个失败结果无 stable error |
| AC-005 | PENDING（generic source conformance PASS） | 真实 Tool producer/Owner blocked |
| AC-006 | PENDING（unknown/resync focused PASS） | 真实 recovery vertical NOT RUN |
| AC-007 | PENDING（migration/mixed hydration focused PASS） | 真实重开仅证明 success Item 恰好一次；failed Item 从未产生 |
| AC-008 | PENDING（component/a11y PASS） | live light、200%、折叠/键盘/状态文字/AX announcement/复制局部 PASS；状态图标仅 component 证据，1180×760 exact 与 dark live NOT RUN |

AC-001 与 AC-004 为 FAIL；其余 Must AC 保持 pending。不得把局部 success、hydration 或 UI 证据改写为完整 D4/Feature PASS。

## 6. 安全未执行项

- 未执行强杀、故障注入、权限破坏、可执行文件/binary 替换、fixture 提取或新增攻击载荷；这些行为由长期安全条款禁止。
- 初始标准门禁审计中，在识别前曾各调用一次 `make generate`、`node scripts/check-generated.mjs`、`make test`、`make build`；它们会创建或读取仓库预存 Zip Slip archive fixture。其机械 exit-0 结果不接受为 FEAT-136 证据，识别后未重跑，并改用定向生成、重复 digest、63 个非 archive Node tests、完整 Go tests 与 direct TS build。
- 原 Command D4 的 Provider/模型请求已使用 3/3；Call 2/3 是用户明确允许的追加请求，没有自动、隐式或超额重试。追加 RCA 阶段调用数为 0，fresh D4 新额度未申请、fresh D4 未执行。MCP Tool、生产写或公网访问均未执行。隔离 repo 仅在既有空 smoke 目录内正常初始化，无 remote，且只有 benign untracked 文件。
- 未执行 FileChange/Diff synthetic event 或 fixture；不存在性只通过 source allowlist 静态审计证明。
- 未运行仓库全量 Rust/composite suite，因为其中存在长期安全条款禁止的权限破坏、故障/攻击与危险 archive fixture；使用 `cargo check`、命名聚焦 Rust tests、带单一既有 baseline allowance 的 strict clippy、TS/Vue scoped suite替代。原始 `cargo clippy --lib -- -D warnings` 仅在 HEAD 已存在的 `database.rs` type-complexity 上失败；影响是未覆盖与 FEAT-136 无关的全仓测试，也未把该既有 lint 债务伪报为通过。
- 未通过断连、重放注入、故障注入或伪造来制造 event_id/reconciliation/late-event/replay 证据；normal replay 如实记录为 NOT OBSERVED。
- 当前 light 与 AX 200% live 可见；精确 1180×760 只由 static/config 覆盖、live NOT RUN，dark 因未更改 macOS 系统外观而 live NOT RUN。
- App 只使用正常 Cmd+Q、runner 正常退出与 canonical 重开；未强杀进程。Command Item 没有 producer raw command/path/secret/wire 泄漏，四文件与保留截图/证据也不记录命令字面量、绝对路径、secret、raw bookmark、prompt 或 Runtime wire；但用户消息本身显示 allowlist 文本，因此 whole-WebView no-raw 验收为 FAIL。
- Host 后置检查只读取/输出 closed metadata；未读取或输出任何 ID、cwd、provider、model 或 raw 内容。bbolt store schema 4 是存储 schema，不得据此推断 wire v4/v5；该 DB 也不含 Command exit/duration 或 event journal。
- 影响：本批证明一个 success Command 的 v5-only安全投影、单 Item hydration 与局部 UI 成立，但真实 failed lifecycle/stable error 和完整事件语义不成立或未观察，因此 Command D4 FAIL。

## 7. Worktree 与 diff

- yijie 先以 67f219b6cf825357285215fcbaafb33c3978acb3 固化 FEAT-138 owner exclusion，再以 c7bc206e89692b591eb044af09de21fdb4f1154d 固化 FEAT-136 D0/Contracts slice；source-conformance evidence 为 82e4010ff34309998c405085c14e3a8988c7113a，D4 FAIL evidence 为 be5c1f91bd1c0f1f10878ea279721dac4eab3dc8；本次 RCA evidence delta 基于后者。
- yijie-contracts 起点：feat/feat-136-desktop-command-tool-items@3832a6c5e99b2a6365f193280fdb887c8fdbc2de；最终 immutable local commit：3c3000a6fbe2f08ab2131a463a1691e867d661b1，clean。
- Host 起点精确为 b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe，当前 clean commit 为 83d3163e21579042d2cc21f303e943946ff97eb0。
- Desktop 起点精确为 fc52ef33cdf040d9b6e8d71bd7498811c5c38c51；core commit 为 69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba，canonical repair clean HEAD 为 65ee3062833ef3d185511599d8f3a4018f635369。
- Runtime 保持只读 clean；Contracts 仍为 exact clean commit。所有 commits 仅本地，未 amend/push/tag/merge。
- 最终 diff review 已覆盖 core 与 10-file canonical repair：Desktop 无剩余 P0/P1/P2；Host 无 P0/P1，并保留 active-item count cap 的后续 P2。

## 8. 结论

- D0：PASS。
- Contracts slice：COMPLETE / PASS（safety-compliant scoped gate）。
- Host/Desktop implementation：本地 source-complete；最终聚焦门禁与独立 diff review PASS，clean local commits 已形成。
- Host→Desktop source-anchored conformance：PASS；不等于 real service。
- Real Command / D4 tranche：FAIL；原 3/3 次授权调用已耗尽。failed lifecycle RCA PASS，但 Runtime repair BLOCKED；fresh D4 新额度未申请且 fresh D4 NOT RUN。success 投影/hydration 局部 PASS，failed lifecycle/stable error 与 whole-WebView no-raw 标准缺失或不成立。
- Real Tool / D4：BLOCKED / NOT RUN，等待 producer/Owner。
- FEAT-136 overall：ACTIVE / IN PROGRESS；不是 usable、implementation complete、完整 D4 或 Epic complete。

## 9. Command failed lifecycle RCA 验证

| 层级 | 只读证据 | 结果 |
|---|---|---|
| Runtime authority | `core/src/tools/events.rs` 定义 started；非零 exit 映射 failed；terminal `item/completed` 携带 status、exit code、duration | PASS：canonical 语义闭合 |
| Existing real-call metadata | 唯一 exit 0 窗口有 started=1/completed=1；四个 exit 128 窗口均为 started=0/completed=0 | PASS：首次缺失早于 Host intake |
| Runtime root cause | `sandboxing/src/denial.rs` denial heuristic + `core/src/unified_exec/process.rs` quick-exit check + `core/src/unified_exec/process_manager.rs` pre-emitter error return | PASS：失败结果在 emitter 创建前被误判并提前返回 |
| Host projector/consumer | source review：failed mapper、stable `command_failed`、completed-only recovery、duplicate/late sealing；16 个 FEAT-136 focused tests | PASS（source）；无 failed-only drop branch且未收到 Runtime producer Item。16 tests 全 PASS，但缺少 exact failed/nonzero mapper regression，保留 coverage gap |
| Desktop consumer | Rust decoder/reducer/SQLCipher/IPC 与 TS decoder/store/UI source review；Rust 20/20、TS 5 files / 119 tests | PASS（source/分层）；未发现 drop 或生产代码修复点，但缺少 failed+nonzero→SQLCipher reopen→IPC→store/UI 的单一整链回归，不把分层 PASS 扩写为完整 failed hydration vertical |
| Contracts | v5 closed failed status/error/exit/duration 语义 | PASS；无需改约 |
| Repair feasibility | 固定 Runtime 禁止修改/升级/重编译/替换；Host/Desktop 禁止制造 producer；shell/sandbox 不变 | BLOCKED：当前授权内无合法修复 |
| Fresh D4 | 仅在修复并复审通过后单独申请新额度 | NOT AUTHORIZED / NOT RUN；本轮真实调用 0 次 |
| Tool D4 | 等待真实 producer/Owner | BLOCKED / NOT RUN |

复审结论：RCA 证据能够解释“模型看到非零结果但 Desktop 没有 failed Item”的表面矛盾。Host/Desktop 从 output 文本反推 lifecycle 会绕过 identity、redaction、event-ID、replay 与 reconciliation authority，故明确拒绝该伪修复。唯一推荐的下一步是先取得 Owner 对 Runtime producer patch/升级的单独授权，使 early sandbox-denial 路径发布 canonical lifecycle；完成修复和独立复审后，才进入“申请 fresh D4 新额度”阶段。
