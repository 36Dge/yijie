# FEAT-137 — Delivery Log

> 2026-09-05 最终决定：Owner 永久终止、未完成验收。未来不再执行本日志中的后续实现、RCA、refreeze 或 D4。历史过程原样保留；本次退役与归档记录见 [03-termination.md](03-termination.md)。

> 本日志保留 Owner-authorized D0、Contracts/Host/Desktop source checkpoint、clean-tree findings、authority composition repair 与真实 D4 历史。2026-09-01 Runtime stable sandbox provenance patch 及 Runtime→Contracts→Host→Desktop refreeze/source conformance 已 PASS；真实 approval vertical 与 D4 的既有 BLOCKED 结论不变，本批真实调用 0。

## 1. 2026-08-30 — 输入固化

| Repository | Branch | HEAD | Worktree at preflight |
|---|---|---|---|
| yijie-codex | `feat/feat-136-command-failed-lifecycle` | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean |
| yijie-contracts | `feat/feat-136-desktop-command-tool-items` | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean |
| yijie-agent-host | `feat/feat-136-desktop-command-tool-items` | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean |
| yijie-desktop | `feat/feat-136-desktop-command-tool-items` | `7026b47828961e58854b06c822c9c9e11252260d` | clean |
| yijie | `feat/feat-136-desktop-command-tool-items` | `ed6e8cc6d4a0cc9e675f189be0973c38ad193e3a` | clean |

Runtime 继续冻结在 0.144.6、267-file stable schema、`experimentalApi=false`；本 D0 不构建、不生成、不重新 pin Runtime。

## 2. Owner decision record

Owner 明确确认推荐方案：

- exact local/demo_fast/FEAT-137 gate 使用稳定 `on-request`；其它组合保持 `never`；sandbox 始终 `read-only`。
- Host 可装配受管、精确的单 Command prompt policy；唯一 argv 为 `git rev-parse --is-inside-work-tree`，cwd 为 workspace root。
- 第一阶段决定集固定为 `accept_once/cancel_current_turn`；独立 decline-and-continue、session approval 和 amendments 不实现。
- 禁止网络、写入、额外权限、shell wrapper、多 action 和 unsandboxed escalation。
- pending TTL 120 秒；TTL first-writer-wins 时只向仍 pending 的 Runtime request 发送一次 `Cancel` 并投影 `expired`，Runtime/Item/Turn 已先清理时投影 `resolved_elsewhere` 且不再响应；SSE 断线只禁用/重连对账。
- pending memory-only；resolved content-free audit 每 session 上限 128 条并随 session 删除。
- Contracts 新建显式 v6；v1-v5、Runtime schema/artifact/pin 不变。
- CAP-020/021、FileChange/Diff、MCP/平台/生产审批全部不属于本 Feature。
- 本 D0 不启动应用/Runtime/Provider/model，真实调用额度 0。

## 3. 原 Draft 冲突的治理收敛

| Draft statement | D0 authority |
|---|---|
| 第一阶段 accept once / decline / cancel | 收敛为 accept once / cancel current turn；不把 decline-and-continue 作为用户动作 |
| UI 精确跟随 Runtime available decisions | stable request schema 不提供可依赖字段；Host 按 Owner policy 固定两个决定并兼容忽略额外字段 |
| 任意只读 Command approval | 收敛为唯一 argv、workspace cwd、单 action 与固定业务 identity |
| 审计字段/保留期未定 | 固定为 content-free、128/session、随 session 删除；pending memory-only |
| CAP-020/021 也由 FEAT-137 承接 | 移出 FEAT-137，保持独立 Owner-deferred capability gaps |
| approval dialog focus trap | 改为 inline Item focus management；不把审批实现成 modal |

## 4. 后续 source-first 实施顺序

1. Contracts：v6 requested/resolved、pending snapshot、one-shot decision、stable errors、closed fixtures 与 v1-v5 compatibility。
2. Host：exact gate、thread/turn policy、managed prompt policy、reverse request allowlist、pending/TTL/single-response、snapshot、redaction/audit 与 cleanup。
3. Desktop：v6 closed decoder、reducer、SQLCipher safe projection、inline UI、键盘/焦点/aria-live/safe copy。
4. Host→Desktop source conformance 与独立结构化审查。
5. Owner 单独授权后执行 fresh real allow/cancel D4；自然 expiry/reconnect 未观察时如实记录。

本 Profile 不建立 production governance slices；上述只是 source-first 技术顺序。D0 当时按要求停止；其后的 Contracts 与 Host 批次均由 Owner 分别单独授权。

## 5. 本批活动

| Activity | Result |
|---|---|
| FEAT-137 four-file package | created；D0 semantic content completed |
| Epic source / CAP-019 / GS-005 / evidence / dependency rebaseline | completed in this D0 diff |
| D0 package gate | PASS（exit 0） |
| Strict D0 package gate | PASS（exit 0） |
| Whole-package strict gate | PASS（exit 0） |
| yijie lint | PASS（exit 0） |
| yijie test | PASS（48 passed、0 failed，exit 0） |
| yijie feature audit | PASS（exit 0；仅 legacy schema-v1 warnings；审计 17 个 committed packages） |
| shell syntax / git diff checks | PASS（exit 0） |
| Contracts/Host/Desktop/Runtime code or config implementation | NOT RUN |
| App / Runtime / Provider / model startup | NOT RUN |
| Real calls | 0 |
| D4 | NOT RUN |

> FEAT-137 在本批未提交，因此全局 feature audit 按设计只统计 17 个 committed packages；新包本身由直接 D0、strict D0 与 whole-package strict gates 覆盖。最终结果于 `2026-08-30T20:02:51+0800` 回填，并在回填后再次复核。

## 6. 已知限制与停止

- 本 D0 不证明 exact prompt policy 已能自然产生 approval；该事实必须由后续 focused conformance 与单独授权的真实 D4 证明。
- `decline-and-continue` 不属于第一阶段；Cancel 表示取消本轮，并由 Runtime 映射为 Command declined/Turn terminal 结果。
- 自然 expiry/reconnect、SQLCipher hydration、dark、1180×760、200%、VoiceOver 均未执行。
- 本批 D0 文档门禁已通过；立即停止，不 commit、push、tag、merge、发布或部署。

## 7. 2026-08-30 — Contracts working-tree source candidate checkpoint（historical pre-freeze）

| Field | Result |
|---|---|
| Repository / branch | `yijie-contracts` / `feat/feat-137-contracts-v6-approval` |
| Immutable foundation / checkpoint HEAD at that time | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` / unpublished `0.7.0` |
| Worktree | dirty；v6 source/generated/docs/tests candidate 尚未提交 |
| Working-tree source candidate review | `PASS` |
| Immutable Contracts commit / authority / consumer pin | `NOT RUN`；没有可供 Host pin 的新 SHA |
| Aggregate `contract.status` | `NOT RUN` |
| Runtime / Host / Desktop | 分别保持 `b2b20e2…` / `96b1fa1…` / `7026b47…`，未修改 |
| App / Runtime / Provider / model startup | `NOT RUN` |
| Real calls | 0 |

候选范围包括独立协商的 v6 requested/resolved lifecycle、owner-only pending snapshot、one-shot decision API、closed stable errors、独立 Runtime approval compatibility projection、generated Go/TypeScript SDK 与 closed synthetic fixtures；v1-v5 与既有 `agent-host-runtime-v1` authority 保持不变。`yijie-contracts/docs/reviews/FEAT-137-semantic-review.md` 记录的候选门禁为：focused compatibility 25/25、全部安全合规 Node tests 88/88、Go tests、lint、`check-generated:safe`、`build:safe`、legacy equality、双基线 breaking 与 `git diff --check` 全部 PASS。默认 `pnpm test` / `pnpm generate` / `pnpm build` 未作为验收门禁。独立复审代理曾因 raw all-test glob 误执行一次既有 Zip Slip 归档测试；该测试正常自清理且仓库未变化，但违反本批安全边界，已排除出验收证据且未重跑。

在这个历史 checkpoint，`PASS` 只评价当时的 working-tree source candidate，不把 dirty tree 提升为 immutable authority；当时的下一步是单独授权创建本地 Contracts commit，再以 clean tree、完整 SHA 和门禁复核形成可 pin authority。该步骤后来已由 §8 完成；本段不代表当前状态。

## 8. 2026-08-30 — Contracts local immutable freeze checkpoint

| Field | Result |
|---|---|
| Repository / branch | `yijie-contracts` / `feat/feat-137-contracts-v6-approval` |
| Immutable commit | `2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6` / unpublished `0.7.0` |
| Parent / tree | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` / `0041ca35366ec4718f9937398924983591bd7010` |
| Commit scope | exactly 50 reviewed FEAT-137 files：14 modified、36 added |
| Worktree / index | clean / clean |
| Legacy authority | v1-v5 sources unchanged；`agent-host-runtime-v1.json` blob remains `456edc9865ae29e229fb8958413d876009ba4c15` |
| Safe gates | generated 45 current、build safe、focused 25/25、non-attack Node 88/88、Go、lint、dual-baseline equality/breaking、diff checks全部 PASS |
| Immutable Contracts authority | `PASS` |
| Host/Desktop consumer pin | `NOT RUN` at this checkpoint |
| Runtime / Provider / model / D4 | `NOT RUN`；real calls 0 |

该 commit 是 FEAT-137 v6 可供 Host 精确 pin 的本地 immutable authority，但不是 published/supported tag。冻结批只创建上述一个 Contracts local commit，未 amend、push、tag、merge 或发布；默认 archive-attack 路径未作为验收门禁。当前用户指令随后单独进入 Host pin/mapper/pending/decision 实现，仍不得开始 Desktop 或 D4。

## 9. 2026-08-30 — Host v6 consumer / mapper / pending / decision checkpoint

| Field | Result |
|---|---|
| Repository / base | `yijie-agent-host` / `96b1fa19783694aef583b614c492fd2b6b5c15cc` |
| Consumer authority | exact `yijie-contracts@2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6`；parent/tree 与 generated Go equality复核 PASS |
| Worktree | reviewed FEAT-137 candidate；HEAD 未移动、未创建 commit |
| Gate / Runtime policy | exact explicit `local + demo_fast + FEAT-134 + FEAT-136 + FEAT-137 + stable MiniMax` 才启用；`thread/start/resume` 与 `turn/start` 使用 `on-request/read-only`，turn network=false；gate-off wire 保持旧形状 |
| Mapper | closed exact outer envelope、typed RequestId、closed params/action、固定 accept/cancel；未知/非法请求 fail closed；`serverRequest/resolved` 按 generation + typed ID + thread ack |
| Pending / decision | memory-only max 1/session、120s monotonic TTL、first-writer-wins、single Runtime response；user decision 在 matching ack 后 HTTP 200，TTL 仅在 stdio response-written 与 matching ack 双信号后投影 expired；idempotent decision、bounded content-free audit |
| Cleanup / replay | same-key pending reuse、payload drift resolves elsewhere、resolved typed-key digest 按 Runtime generation 精确保留并在 generation close 清理、close marker 阻止 late admission；不使用 Contracts 未授权的 cardinality cutoff，Item/Turn/session cleanup 均无第二响应 |
| HTTP / projection | explicit v6 SSE、owner-bound pending snapshot、one-shot decision；strict Content-Type/query/method/UUID；fixed safe action projection、no-store、bearer、无 command/cwd/reason/wire |
| Safe gates | `make test-feat137` PASS；`make test-feat136` PASS；`make lint` PASS；`git diff --check` PASS |
| Independent conformance/security review | PASS；optional identity bounds、>128 typed-key replay、response-written + matching ack TTL ordering、write-failure/cleanup、dynamic-tool gate-off compatibility 均无剩余阻断 |
| App / Runtime / Provider / model | NOT STARTED |
| Real calls / D4 | 0 / NOT RUN |

统一门禁实际结果：

- `make test-feat137`：Contracts exact source/generated/equality PASS；Codex、Session、App `^TestFEAT137` race suites PASS；包含 response-written/ack/cleanup 顺序与 >128 全新 typed-key replay 回归；`cmd/desktop-host` compile-only PASS。
- `make test-feat136`：v1-v5 equality 超集检查、FEAT-136 Session/App race regression 与 Runtime compatibility adapter PASS。
- `make lint`：gofmt clean、`go vet ./...`、`bash -n scripts/*.sh` PASS。
- 未执行 broad repository tests、archive/checksum/Zip-Slip/archive-error、权限/进程故障、Runtime/Provider/Desktop 启动或真实请求。

本 checkpoint 仅证明 Host source slice。Desktop v6 decoder/reducer/SQLCipher/inline UI、Host→Desktop conformance、真实 allow/cancel、自然 reconnect/expiry 与 D4 均未执行；不得将 FEAT-137 implementation/verification 或任一完整 Must AC 标为 PASS。

## 10. 2026-08-31 — 首次 Host/Desktop immutable freeze 与 source conformance finding

| Field | Result |
|---|---|
| Host first freeze | `01c4a406dec5e582d208113e1a1669d031023556` / tree `8c26b907f12d4adcd68678da145ae6d774a30b40`；parent `96b1fa19783694aef583b614c492fd2b6b5c15cc`；45 reviewed files；clean |
| Desktop first freeze | `6a9786b7ddfc20af001488a2feef81b8e68eb093` / tree `89ee8a228449a94063c6a07e56492e81a4bb3527`；parent `7026b47828961e58854b06c822c9c9e11252260d`；46 reviewed files；clean |
| Initial gates | Host FEAT-137/136、lint、diff PASS；Desktop authority、Web 291/291、Rust 19/19、lint/build/Cargo PASS；strict Clippy 仅命中 Desktop base 既有 `database.rs type_complexity` |
| Independent clean-tree review | `FAIL`：发现 1 个 P1；无其它 P0/P1/P2 |
| P1 | decision 在 deadline 前 commit、Runtime ack 在 deadline 后到达时，Host 以 ack 当前时间发布 accepted/cancelled，违反 v6 non-expired `resolved_at < expires_at`；deadline 后 pending cleanup 也可能发布 late `resolved_elsewhere` |
| Governance action | 立即停止；未提交错误 PASS 治理，yijie 恢复到原 reviewed D0 diff；外部 Epic package 未改 |

首次冻结 commits 只作为可追溯 candidate，不是最终 Host/Desktop authority。该 finding 也说明 §9 的历史 working-tree review 未覆盖 commit→late-ack 与 deadline→cleanup 交叉边界，不能单独作为最终 conformance 结论。

## 11. 2026-08-31 — Host TTL/ack boundary repair immutable freeze

| Field | Result |
|---|---|
| Repository / branch | `yijie-agent-host` / `feat/feat-137-host-ttl-ack-boundary-repair` |
| Immutable commit | `118651804b7f5a7849bc68cdf29d88c74a21f8a1` |
| Parent / tree | `01c4a406dec5e582d208113e1a1669d031023556` / `9ae73d7b6f024bda241071371487a627810c1058` |
| Repair scope | 4 files；decision winner 保存 Host monotonic commit time；late ack 只放行 terminal/HTTP 200；deadline 后 pending cleanup 由 TTL winner 接管；retained event 与 HTTP result 显式校验完整时间窗 |
| Deterministic tests | accept/cancel commit-before-deadline + ack-after-deadline；late Runtime resolved、Turn cleanup、generation/request/session teardown；invalid at-expiry retained/HTTP result |
| Clean-tree gates | `make test-feat137`、`make test-feat136`、`make lint`、focused race、Contracts at-expiry boundary、`git diff --check` 全部 PASS |
| Runtime / Provider / model / D4 | NOT STARTED / 0 real calls / NOT RUN |

## 12. 2026-08-31 — Desktop Host authority repin immutable freeze

| Field | Result |
|---|---|
| Repository / branch | `yijie-desktop` / `feat/feat-137-desktop-host-ttl-ack-repin` |
| Immutable commit | `918bd26b04a32ab20433e2ea991cc0a4ea282c34` |
| Parent / tree | `6a9786b7ddfc20af001488a2feef81b8e68eb093` / `e5f5af31773852af6eefa65a62080c87b3ac1384` |
| Repin scope | 2 authority files；Host exact commit/tree 更新为 `118651804…` / `9ae73d7b…`；Desktop 功能、capability、plugin、CSP、依赖、Cargo/lock 与外部 URL 无扩张 |
| Clean-tree gates | authority checker、Web 291/291、Rust 19/19、pnpm lint/build、Cargo fmt/check、scoped strict Clippy 与 `git diff --check` PASS |
| Strict Clippy boundary | raw `-D warnings` 仅命中 Desktop base 已存在且字节一致的 `database.rs type_complexity`；只放行该项后无其它 warning |

## 13. 2026-08-31 — final clean-tree source conformance

不可变输入：Runtime `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`、Contracts `2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6`、Host `118651804b7f5a7849bc68cdf29d88c74a21f8a1`、Desktop `918bd26b04a32ab20433e2ea991cc0a4ea282c34`；四仓均 clean。

最终独立结构化复审 `PASS`：exact local/demo_fast 与 FEAT-134/136/137 gates、v6 negotiation、v1-v5 equality、closed pending/decision/error shapes、Rust identity/stream mapping、fresh GET→single POST、无自动重试、unknown revoke+resync、SSE-first/double-click/selection/TTL races、SQLCipher safe hydration/cardinality、event-id idempotency/late-event no rollback、redaction/safe-copy、normal handler=1/S10=0 及 capability/plugin/CSP/dependency/external URL 边界均通过。原 TTL/ack P1 已由 Contracts executable at-expiry test与 Host deterministic late-ack/cleanup race tests闭合；无剩余 P0–P2。

本结论只把 source implementation/conformance 标为 PASS。真实 allow/cancel、自然 expiry/reconnect、人工 light/dark/1180×760/200%/键盘/VoiceOver、D4 与发布继续 NOT RUN；十条 Feature-level Must 继续 pending，真实调用为 0。

## 14. 2026-08-31 — fresh real D4 canonical startup blocker

Owner 单独授权 fresh real allow/cancel D4 最多 7 次真实 Provider/模型调用，并允许调用层受限自动重试；approval decision POST 的 closed single-write/no-retry 语义不变。

| Field | Result |
|---|---|
| Five-repository preflight | PASS：Runtime `b2b20e2…`、Contracts `2e490dea…`、Host `118651804…`、Desktop `918bd26b…`、yijie `56b922c…` exact clean |
| Runtime stable artifact | PASS：0.144.6、`experimentalApi=false`、267 schemas；binary SHA-256 `4efe16d2…` / 355676760 bytes；manifest SHA-256 `1cfa2e0a…` / 1475 bytes |
| Contracts/Desktop authority | PASS：v6 checker确认 Contracts、Host、Desktop exact clean authority |
| Host focused gate | PASS：`make test-feat137`；Codex/Session/App race suites 与 desktop-host compile-only通过 |
| Isolated workspace | PASS：新建无敏感 Git repository，branch `feat-137-d4`，仅一个 benign untracked文本文件 |
| Canonical command | `pnpm tauri:demo-fast:stable` |
| Startup result | BLOCKED / exit 1 before build or app start：旧 `check-agent-host-v4-contract.mjs` 要求 Host HEAD `96b1fa19783694aef583b614c492fd2b6b5c15cc`，当前冻结 FEAT-137 Host 为 `118651804b7f5a7849bc68cdf29d88c74a21f8a1` |
| v6 relation | 独立 v6 checker对当前 Host/Contracts/Desktop PASS；失败发生在 runner 先执行的旧 v4 exact-checkout gate |
| App / Runtime / Provider / model | NOT STARTED |
| Real calls | 0/7；没有发生或重试任何真实请求 |
| accept_once / cancel_current_turn | NOT RUN / NOT RUN |
| Hydration / reconnect / expiry / visual / VoiceOver | NOT RUN；未改变系统无障碍设置 |

结论：这是 canonical stable entrypoint authority composition regression，不是 Provider、模型、workspace 或 approval producer 失败。绕过 v4 checker、手工拼接 launcher 或直接运行已构建 binary 都会使 D4 失去 canonical authority，因此本批安全停止。下一步需单独修复 v4 checker，使其从冻结历史 Git object 验证 v4 byte/source authority，同时由当前 Host HEAD `118651804…` 提供运行实现；随后重新冻结 Desktop SHA、更新 v6 authority、复审并重跑 fresh D4。

## 15. 2026-08-31 — canonical stable entrypoint v4/v6 authority composition repair

| Field | Result |
|---|---|
| Desktop branch | `feat/feat-137-desktop-v4-v6-authority-composition-repair` |
| Immutable commit / tree | `27d6c6a2a9f8a9984b47b27143f8c9090815dbd3` / `6cefcc7a6deed7924f64ba32b06ac7c084fd654d` |
| Repair | v4 checker不再要求当前 sibling HEAD等于历史 v4 commit；继续要求clean checkout与exact origin，并从历史 commit/tree读取Contracts/Host source、Host consumption lock与五个fixture，逐项验证blob类型、大小、digest和tree OID |
| Runtime implementation authority | 当前 Host `118651804b7f5a7849bc68cdf29d88c74a21f8a1` 仍由v6 checker精确约束并提供实际运行实现；v1-v5 wire与Runtime未修改 |
| Contract / permission / dependency impact | none / none / none；无capability、plugin、CSP、Cargo/lock或外部URL扩张 |
| Desktop clean gates | v4/v6 checker PASS；14 Web focused files 294/294；Rust FEAT-137 19/19；pnpm lint/build；Cargo fmt/check；`git diff --check` PASS |
| Strict Clippy | raw `-D warnings`仅命中base既有且字节一致的`database.rs type_complexity`；只放行该项后无其它warning |
| Cross-repository gates | Host `make test-feat137`、`make test-feat136`、`make lint` PASS；五仓clean preflight与stable Runtime artifact digest PASS |

## 16. 2026-08-31 — fresh real D4 after entrypoint repair

Canonical `pnpm tauri:demo-fast:stable` 三次均通过v4/v6 checker、safe build并正常启动；所有关闭均使用应用自身 `Quit`，runner exit 0，未强杀或注入故障。真实调用按UI发送保守计数为4/7，decision POST为0。

| Call | Safe observed result |
|---|---|
| 1 | 新任务首轮短暂显示task不可用；随后自然封口为Command declined / Turn interrupted。没有出现可操作approval card，Command未执行。 |
| 2 | 改用稳定的隔离无敏感Git目录；live视图仍短暂不可读。正常关闭并重开后，SQLCipher只恢复一个completed Command item；Command直接完成，未产生approval lifecycle，不能作为accept_once证据。 |
| 3 | 在已hydration任务内明确请求approval；Provider/turn立即generation failed，没有Command、pending或decision。 |
| 4 | 在同一任务再次请求approval；超过一分钟且跨正常关闭/重开仍为单一waiting turn，没有approval card、terminal或decision。应用自带权限说明仅显示通用read-only/fixed-no-escalation策略，不是FEAT-137 action authority。 |

结论：authority composition repair `PASS`，但真实 approval producer/task lifecycle → Host pending → Desktop inline action authority链路 `BLOCKED`。`accept_once`、`cancel_current_turn`、真实approval hydration/cardinality、approval replay/expiry与approval card视觉/VoiceOver均未完成；剩余3次额度未继续消耗。自然正常重开已观察，但没有可归因于approval event的replay；不得标为PASS。下一步必须单独RCA live producer、首轮task binding/SSE与pending GET/action-authority组合，不得绕过产品入口、伪造pending或直接调用内部decision command。

治理回填门禁：D0、strict D0、whole-package strict、lint、治理 tests 48/48、17个committed package audit、shell syntax与`git diff --check`全部PASS。D4 closure gate按设计FAIL，因为Feature/implementation/verification、real smoke、representative failure及十条Must没有PASS；该结果是正确的fail-closed治理证据，不得通过改写状态绕过。

## 17. 2026-09-01 — Runtime stable sandbox provenance patch 与全链 refreeze

Owner 单独授权 pinned Runtime 0.144.6 补丁链增加 stable sandbox provenance；本批不得执行 D4，真实调用额度为 0。实现只把既有 sandbox permission provenance 传到 stable reverse-request wire，不改变执行权限、审批决定或 Yijie public v6 API。

| Repository | Immutable authority | Result |
|---|---|---|
| Runtime | `acf2da55d8a53175343aaf112e03368dfef9922a` / tree `97557e0bd736a91bbbf94ccfa11b57a4bbf23a74` / reported 0.144.6 | `0003-feat-137-stable-sandbox-provenance.patch` 在既有 `0001`/`0002` 后精确应用；stable `sandboxPermissions` 必填且 enum 恰为 `use_default`、`require_escalated`、`with_additional_permissions`；tool request → `ExecApprovalRequestEvent` → app-server wire 原值；clean |
| Contracts | `aeccf5d561bd4259389cdb325bae84ce3e0dea86` / tree `7a864645bf552a8b7457b6338a30f6626ce15d3a` | source-first 新增版本化 compatibility v3；历史 v1/v2 digest 不变，public event v6 不暴露 raw provenance；clean |
| Host | `078769a22d035c2921e315e5776185bed6f7feeb` / tree `df7e5b6bc4994a1a4023793e766a87c7806f1e07` | exact pin Runtime artifact/Contracts v3；closed decoder 要求三值 enum，只有 `use_default` 可形成 pending；其它值、缺失与未知 fail closed；provenance 进入 replay fingerprint 但不进入 public v6；clean |
| Desktop | `56f88856125d2affd98f4c0c984792d47b444ca7` / tree `2d580bbe70ebe537cbfc13dae0d9b50b57a007c8`；parent `13277c03…` | exact pin Runtime/Contracts/Host；v4 checker继续从历史immutable objects验证，v6 checker验证Runtime clean SHA/tree、Runtime build artifact与Host stable artifact；provenance不进入IPC/domain/store/UI；canonical runner用nounset-safe数组展开兼容macOS Bash 3.2；隔离clean worktree与stable build PASS；主checkout的FEAT-151改动未暂存、未提交 |

Runtime frozen artifact：binary SHA-256 `84bb0445a15f99354ddd38ccb407b9b0d3d28522accece3fa9755918ab6978e3` / 356082232 bytes；manifest SHA-256 `e62d8210f5abcad7ff0fc1b4d068c7fe4da59501c6fa6b12f18dc4a1f939c6aa` / 1649 bytes；stable schema 267 files / tree SHA-256 `d82a33f683e554c10dd056a0101c26fd24477928e3f98ee3d9ef250b97395228`；patch 0003 SHA-256 `af7196f609fbbe722f69e7913d2aeb2f38bfc5f4cbed4bfb32c9e6f844a9910c`。

安全门禁结果：

- Runtime source/focused、三补丁 replay、fmt、scoped Clippy、release build、267-file schema generation、stable protocol normal-EOF smoke、historical v1 + active v3 authority checker全部 PASS；没有 thread/turn/Provider/model。
- Contracts focused 13/13、非攻击性 Node 80/80、Go、lint、safe generated 47 files、safe build、历史 equality、相对 `0acf2a39…`、`2e490dea…` 与 published `f16a497…` 的 breaking checks及 clean-tree audit全部 PASS。archive/Zip Slip 与 structured-artifact injection-invalid套件按安全边界未执行。一次 lint 与并行 safe build 的瞬时生成目录竞争不计验收；串行复跑 PASS。
- Host `make test-feat137`、`make test-feat136`、`make lint`、`git diff --check` 与 pinned Runtime stable integration PASS。integration 使用正常 0700 临时 CODEX_HOME、正常启动/EOF；没有应用、thread/turn、Provider或模型。
- Desktop isolated clean-tree v4/v6 checker PASS；Web focused 244/244；Rust `feat137` 32/32；ESLint/Vue typecheck、Vite build、Cargo fmt/check PASS。raw strict Clippy唯一命中 Desktop base `7026b478…` 已存在的 `database.rs type_complexity`；仅放行该项后无其它 warning。无 capability、plugin、CSP、Cargo/lock、依赖或外部 URL 扩张。
- yijie FEAT-137 D0、strict D0、whole-package strict、lint、tests 48/48、18 committed-package audit、shell syntax与`git diff --check`全部PASS；audit仅保留既有schema-v1历史warning。未跟踪FEAT-151 package未进入本批commit。

Desktop freeze后又发现canonical runner在macOS系统Bash 3.2的`set -u`下展开空`feat134_environment`数组会在非stable入口启动前失败。最终commit `13277c03…`只修改runner、v4 activation checker及对应tests：空数组展开为0个参数，非空数组仍逐项保留；runner/v4 tests 25/25、v4/v6 checker、ESLint、Vue typecheck、Vite build与clean-tree audit PASS。完整非攻击性demo_fast Web套件为1070/1071；唯一失败的FEAT-132 projection replay在immutable Desktop base `7026b478…`上同样失败，故记录为既有基线问题，不将其伪造为PASS，也不在FEAT-137批内扩修。

随后在D4前canonical readiness audit中发现stable runner仍指向历史FEAT-136 Runtime artifact `b2b20e2…`，无法把本批新增provenance带入真实运行。Desktop `56f88856…`将runner重pin至新建的版本化Host本地artifact目录`feat-137-acf2da55d8a5`，并把Runtime commit/tree、build binary/manifest digest、Host稳定副本digest与runner三条authority同时纳入v6 checker。新SHA的isolated clean worktree中v4/v6、runner/v4 25/25、lint、Vue typecheck、Vite build、Cargo fmt与原始`pnpm tauri:build:demo-fast:stable`全部PASS；未签名debug `.app`正常生成，bundle与target Desktop binary均为SHA-256 `23e0472875e4f1543c10f035b94822cd9ffb55b5655c09a6c694656a9fa2dcdc`。构建未启动app、Runtime、Provider或模型，真实调用0。

一次 isolated Desktop Rust 初跑因 fixture 的 sibling repository 相对路径在临时 worktree 中不存在而出现 30/32（2 个 `ENOENT`）；建立只读 sibling 链接后同一冻结 SHA 复跑为 32/32。一次 `pnpm exec` 因临时 worktree 的复用模块链接触发非 TTY 清理保护而在测试前退出；改用同一 lock 对应的已安装固定本地二进制后 Web 244/244、lint/typecheck/build 均 PASS。两项均没有代码、依赖、lockfile或权限变化，不计失败功能证据。

本批没有启动 Desktop、Provider或模型，不执行 D4；真实调用 0，decision POST 0。历史 fresh D4 的 4/7 与 blocker 结论保持不变。没有 amend、push、tag、merge或发布，也没有强杀、故障注入、权限破坏、binary替换或攻击 fixture。
