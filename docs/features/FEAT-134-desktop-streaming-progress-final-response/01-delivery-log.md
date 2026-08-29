# FEAT-134 Delivery Log

> Profile: `demo_fast` · Exposure: `local` · Current gate: `D4 PASS` · Implementation: `COMPLETE`

## 2026-08-29 — #5/#6 final-source 收口、跨层 P2 修复与 D4

历史 canonical tranche `4/4` 原样保留；当前追加 tranche 已消费 `6/7`、剩余 `1`，Feature 累计 `10/11`。所有调用均为 Owner 显式授权、无敏感纯文本、禁止工具/文件读写且无程序自动重试；任何治理文件都不保存、复述或哈希 prompt、reasoning、plan、final 正文。

#5（首次 finalized-content P2 修复源码）进程为 Desktop `2026-08-29 01:49:09`、Host `01:49:34`、Runtime `01:49:35`（Asia/Shanghai）。持久化 content-free 事实为 attempts=`1`、outbox=`done`、Turn=`completed`、terminal=`1`、v4 events=`187`、raw reasoning item/part=`1/1`、stable plan update/step=`0/0`、AgentMessage `phase=null`；light、200% zoom 与键盘 PASS。`null` 合法映射 unknown，canonical 只证明负向 producer shape；显式 `final_answer` 正向行为由 Contracts/Host/Desktop 确定性测试证明。

#5 后终审发现跨层 P2：native 已接受 repeated finalized reasoning lifecycle 并持久化 cursor/source，但 `TimelineDelta::Ignored` 不跨 WebView，TS 仍 fail-closed。修复后最终门禁为 TS `835/835`、Rust `316 pass + 3 ignored`、lint/build/fmt/diff PASS，独立终审无 open P0/P1/P2。

#6 final-source canonical 进程为 Desktop `02:02:12`、Host `02:02:39`、Runtime `02:02:40`，fresh task content-free ID `01a0498a-5574-7cf2-9652-14f47b6db9d4`。UI 观察到 processing→completed，reasoning 与 unknown assistant 均 expanded，Composer 恢复；随后使用应用自身 `Cmd+Q` 正常清理。#6 未另取 DB event counts，绝不把 #5 的 `187` 冒充 #6。

临时 probe 源码和 target 残留均为 `0`，Host 空 probe 目录已删除。Runtime 保持 clean `yijie-codex@0ce5902ed400866be0196886bb78f693a004d68d`，binary/manifest 匹配，`experimentalApi=false`，未修改、升级或重编译。

- dark theme：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。
- Reduce Motion：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。
- 精确 `1180×760`：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。

按 `demo_fast` 规范 D4 不要求 implementation commit；D4=`PASS`。Owner 后续授权 Desktop 提交，immutable commit 为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`，message `feat(chat): deliver FEAT-134 streaming progress and final response`，工作树 clean、未 push。`yijie` 治理包仍未提交；D4 只表示本地真实 Demo 可用，不表示生产可用或完整 Epic 完成。

## 2026-08-29 — 历史：failed-start 终态修复、Owner UI waiver 与 no-prompt smoke

Owner 于 `2026-08-28/29` 明确将 dark theme、Reduce Motion 与精确 `1180×760` 三项从 FEAT-134 治理门禁移除。三项统一登记为 `WAIVED / NOT REQUIRED`，不是 PASS；无需执行或恢复，系统设置未变。

最终 Desktop failed-start repair/recovery 收敛为 exact-local payload v2-only：

- v1 exact-local/legacy 语义保持不变；
- pre-POST resume 的 matching Active 按 provenance 对账：claimed `attempt_count==1` 必定不是当前 operation，保持 inflight/queued/runtime NULL、发布 `TurnReconciliationRequired` 且 0 次新 POST；只有 `attempt_count>1` crash-reclaim 才绑定既有 runtime Turn且 0 次新 POST；
- post-error reconciliation 的 matching Active 因本调用已 POST 同 operation 而直接绑定；
- Host 确认 `turn_start_failed` 时才原子提交 outbox=`failed` 与 Turn=`failed`，reasoning=`unavailable/reasoning_not_emitted`，`terminal_code=NULL` 且无 v4 source facts；
- identity mismatch/non-idle/Err 时挂起自动 retry，保持 outbox=`inflight`、Turn=`queued`、no runtime/no v4，并发送 content-free `TurnReconciliationRequired`，不伪造 failed；
- unknown payload version 保持原 generic fail，不走 specialized finalize，避免 specialized 约束冲突；
- Vue、Contracts、Host、Runtime、public 与 production 均不修改。

该历史时点，`legacy_background_does_not_run_feat134_failed_turn_recovery` 与当时的 834 TS / 313 Rust / targeted 31/31 静态验证 PASS；这些结果不替代本文首节的最终 835 TS 与跨层 P2 复验。

最终源码通过正常退出/清理旧构建、v4 pin 与 stable debug app rebuild 后启动：Desktop `2026-08-29 00:34:04`、Host `00:34:30`、Runtime `00:34:30`（Asia/Shanghai）。最终 content-free AX controls 均 present；状态计数 queued=`0`、streaming=`0`、completed=`2`、stopped=`1`、failed=`2`、updated=`1`。未点击历史正文、未发送 prompt；不保存、引用、复述 prompt、reasoning、plan、final 正文、raw AX 或截图。该事实仅为 startup/state smoke，不替代 fresh corrected successful Turn。

该历史时点 D4 为 `NOT RUN`、首个 tranche 为 `4/4` exhausted；现行 D4 与授权 ledger 见本文首节。

## 2026-08-28 — 历史：Desktop Contract First、canonical 4/4、第四次 pre-Provider 失败与 D4 pending

Desktop 已精确 pin Contracts `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` 和 Host final authority `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`，完成 private v4 projection、FEAT-132 reducer/SQLCipher authority、FEAT-133 Timeline 分层以及安全 recovery/liveness 边界。验证结果：

- `make lint` PASS；
- terminal repair 之前的 `pnpm test` PASS：103 个 Vue/TypeScript files、833 tests；
- terminal repair 之前的 `cargo test` PASS：300 pass、3 ignored、0 fail；
- `pnpm lint` 与 `pnpm build` PASS；
- `make build` PASS；
- `pnpm tauri:build:demo-fast:stable` PASS，exact checker 确认 local/demo_fast/stable、Contracts/Host 两个完整 SHA，final `.app` 已重建；
- 历史时点记录：`git diff --check` PASS；Desktop 62 个未提交 status entries、0 staged，`src-tauri/src/bin` 无残留源文件。

Host 提交历史必须保留为线性 provenance：baseline `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` → 首个 FEAT-134 实现 `201fd9f8fff6e1ee18ddc1a0477e329b0d75af0c` → corrective child/final authority `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`。首个实现对 structured Item content 的解码过窄；corrective child 修复为一般 content opaque raw JSON，并只对已完成 reasoning 的受支持 shape 执行专门解码。Desktop 只 pin `b9358f…`，但治理记录不抹去 `201fd9…` 的失败历史。

canonical 初始授权 `1` 次，Owner 随后明确增加 `2` 次重试，并在前三次用尽后另外批准 `1` 次；四次均为 Owner 分别授权，不是程序自动重试，现已消费 `4/4`。四次 content-free 结果：

1. Host 首个 structured-content decoder 失败，形成上述 corrective commit；
2. 暴露 stale Host session 占据 recovery queue；仅调用与 UI Stop 相同的正常领域 interrupt action 收口 stale session，没有强杀或直接改库；
3. Host 到 sequence `87`，Desktop 初始停在 `32`；根因是 parser 错误拒绝 Contracts v3/v4 合法的空 lifecycle `text` snapshot。修复并加测试后，同一已接受 Turn 的 retained tail 只通过生产 v4 GET/reducer/persistence 路径原子提交 completed terminal，没有新 POST、Provider call 或 prompt；
4. `23:02` 在 `22:22` 启动的旧/pre-corrective bundle 中提交了额外授权的唯一一次无敏感纯文本 Turn；Desktop Turn queued 后 outbox 以 `failed` 收口，`attempt_count=1`、`runtime_turn_id` 为空，事件/Item/notice/terminal 均为 `0`，cursor 未前进。Host 保持 idle 并记录 `turn_start_failed`；Provider 与 Runtime Turn 均未启动，没有工具调用、文件读写或自动重试。corrective 是本次失败后才写入，不能把第四次描述为 corrective 验证。

sequence `87` 的 content-free 结果确认非空 raw reasoning；AgentMessage `phase=null`；plan update/step 为 `0/0`；没有猜 final、没有伪造 plan、没有保存任何 prompt/reasoning/plan/final 正文或哈希。详细计数与边界见 [canonical v4 content-free 验证记录](evidence/canonical-v4-content-free-2026-08-28.md)。

前三次的 retained-tail recovery 仍不是 fresh、不间断 UI streaming 证明。Mac 解锁后，旧 canonical 应用已通过 `Cmd+Q` 正常退出，旧 Desktop/Host/Runtime PID 均消失，全程没有强杀；随后启动的 `22:22` pre-corrective bundle 通过 exact Contracts/Host/local-demo_fast-stable checker。第四次授权于 `23:02` 在该旧 bundle 中只消费一次，并在 Provider 前失败；Desktop corrective 于失败后的 `23:16+` 才写入。

在第四次失败前的旧应用中，打开最近既有 FEAT-134 session 后，SQLCipher hydration 显示 Timeline、第 1 轮和“已完成”，同时 `loading=false`、`streaming=false`；过程记录默认折叠，并在该旧进程中通过键盘展开/收起。该历史证据不冒充 corrective 新进程的 disclosure 操作。

第四次失败的直接持久证据最深仅为 `turn_start_failed`。bundle 与 Runtime 新进程均在 `22:22` 启动，历史 thread 形成于 `18:55`；结合旧纯文本 v1 start 不执行 resume、固定 Runtime `turn/start` 只读取进程内 thread manager 的确定性路径，高置信根因推断为 Provider 前 thread-not-found，不把该推断冒充直接 Runtime 日志。

corrective 仅位于 Desktop exact local FEAT-134 flag：纯文本 create/submit 在 `feat134_streaming_enabled=true` 时走 v2，start 前 resume 并严格校验 task、agent session、Codex thread、idle、无 active Turn、model ready 与无 failure；resume/start 失败 fail closed，且按次授权的 local canonical 禁止 outbox 自动重试。flag=false、public/production、旧 v1 与既有 flag=false v2 幂等重试语义不变，Contracts/Host/Runtime 不变。新增 TS/Rust/DB 测试覆盖 v2 routing、dispatch identity、resume→start 顺序、Host 未就绪/身份错误 fail closed 和无自动重试；全量结果为 103 files / 833 tests、Rust 300 pass / 3 ignored / 0 fail，lint/build PASS。

第四次失败所在的旧 canonical 随后通过 `Cmd+Q` 正常退出，Host、Runtime、runner 均正常清理，没有强杀。Desktop corrective stable build PASS；随后从 corrective 源码重新构建并启动 canonical 新进程：Desktop `23:30:38`，Host/Runtime `23:30:52`。没有发送 prompt。新任务页在 100% 与 200% zoom 下 AX tree 均可读，Composer、附件、权限与发送控件存在。`23:34` 使用键盘打开既有 FEAT-134 session，SQLCipher hydration 显示第 1 轮 completed、第 2 轮 queued，process/unknown rows 默认折叠；本轮未在新进程展开 disclosure。100%→200% zoom 时 Tab 聚焦 Composer，Shift+Tab 返回项目选择器，随后恢复 100%。

该历史时点没有完成 dark/reduced-motion/exact-size 检查，且 `1162×768` CUA 窗口截图像素不能冒充精确 `1180×760`。Owner 后续已将这三项设为 `WAIVED / NOT REQUIRED`，所以它们不再是待办或 D4 blocker。corrected fresh successful Turn 仍需新的 Owner 授权；D4 保持 `NOT RUN`，不声明 FEAT-134 或 Epic 完成。`4/4` 已用尽。

## 2026-08-28 — D0 授权修订（当时状态）

Owner 于 `2026-08-28T13:35:01+08:00` 批准：

- 仅在 `demo_fast/local` 将固定 managed provider reasoning effort 设置为 `high`；
- 启用 Host raw-reasoning projection；
- `ai_behavior_change=model` 仅限 FEAT-134 本地链路；
- 不新增推理强度 UI，不修改/升级/重编译 Runtime，`experimentalApi=false`，不影响 public/production；
- 完整 Contract First 链路后，canonical `pnpm tauri:demo-fast:stable` 最多发送 1 次无敏感纯文本 prompt；禁止工具调用和文件读写，不自动重试；验证证据只保存 content-free event shape，不保存 prompt、reasoning、plan 或 final 正文。

该时点授权写入 `feature.yaml`，调用消费为 `0/1`。后续 Owner 又明确增加 `2` 次重试，并在前三次用尽后另外批准 `1` 次；该历史 tranche 最终消费 `4/4`。当时 Feature 与 implementation 保持 `active`，CAP-010/011/012 不能因授权本身标记通过；现行累计见本文首节。

## 2026-08-28 — Contracts v4 source-first candidate 与不可变提交

在 `yijie-contracts` FEAT-134 分支完成并提交 `0.6.0` candidate：

- 新增显式协商 `AgentSessionEventV4`，v1/v2/v3 权威源不修改；
- AgentMessage lifecycle 要求 `text + phase(commentary|final_answer|null)`，delta 保持 text-only；
- 新增稳定 `turn.plan.updated` 完整有序快照，禁止 experimental `item.plan.delta`、item ID 和伪造 step ID；
- v4 保留 reasoning/artifact 语义并恢复 raw-reasoning byte/index bounds；
- 单个 compact SSE data 冻结为 1 MiB UTF-8 上限；Host 必须在 replay/write 前验证，禁止截断，超限以脱敏 `limit_exceeded` 和 failed terminal 失败关闭；stable Runtime 空 plan step 被保留而不伪造正文；
- compatibility allowlist 仅补入固定 Runtime 已存在的 stable `item/reasoning/textDelta` 与 `turn/plan/updated`；Runtime identity、schema count/digest 和 `experimentalApi=false` 不变；
- OpenAPI/AsyncAPI/Protobuf/JSON Schema、Go/TypeScript SDK、合成 fixtures、release/semantic review 文档已生成。

门禁结果：`pnpm generate/lint/test/build` PASS（56 tests）；legacy v1 wire equality PASS；相对 `164b14f...` 与 supported `f16a497...` 的 OpenAPI/Protobuf/AsyncAPI/JSON Schema breaking 检查均 PASS。

Owner 随后授权只提交 Contracts、不 push。候选已提交为 `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`，Contracts 工作树 clean；Host 现在可以使用该完整 SHA 执行精确 pin。未创建 tag、未 publish、未 push；该时点付费 prompt 消费仍为 `0/1`，后续现行状态见本文首节。

## 2026-08-28 — Host v4 projection immutable commit

在 `yijie-agent-host` FEAT-134 分支完成并提交已验证的 Host candidate：

- 从 clean Contracts commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` 同步并精确 pin `0.6.0` v4 authority；
- 新增 gated `/v4/.../events?event_schema_version=4`，实现 AgentMessage phase、stable plan、raw reasoning 与全部 v3 Artifact/lifecycle variant 的 v4 producer；
- 每轮 managed effective effort 固定 `high`，managed config 开启 raw reasoning，`experimentalApi=false`；激活只允许显式 `local + demo_fast + managed MiniMax`，并拒绝 DynamicTools、public/production 与 Host/Runtime physical/symlink home alias；
- v4 closed producer 在 retention/replay 前执行 1 MiB 检查且不截断；一般 Turn-scoped 超限或 malformed source 只产生 content-free failure；reasoning-specific 限额按专属 finalized/unavailable 语义收口；malformed terminal 先以 `protocol_error` 收口已进入 v4 的未完成 reasoning，再同步关闭 Turn Store 并发布一次 sanitized failed terminal；
- v1-v3 不携带 phase/plan，shared control request 不继承 v4 trace 上限；AgentMessage delta 必须匹配同 Turn lifecycle；第九个 unique reasoning item 的正文不进入 v4，只发布一次 `reasoning_text.finalized(status=unavailable, reason_code=limit_exceeded, contents=[])`，且不把整个 Turn projection 标记为失败。

独立审查的首轮五个 P1，以及首轮修复后复核发现的两个剩余 reasoning 语义 P1，均已补入回归测试并关闭。最终及主代理独立复核均通过 `go test ./... -count=1`、focused race、`go vet ./...`、`make contract-check` 与 `git diff --check`。`api/contracts.lock` SHA-256 为 `c1ae8d7d363269c29a1858142c07a1c6041d9fbd394c126539e12dee767934d9`。

Owner 授权 Host `git add` 与提交、禁止 push。首个 FEAT-134 实现提交是 `201fd9f8fff6e1ee18ddc1a0477e329b0d75af0c`；首次 canonical 暴露 structured-content decoder 过窄后，其直接 corrective child `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` 成为最终 Host authority。Host 最终工作树 clean，未 push。Desktop 只精确 pin `b9358f…`。该小节原始候选时点 prompt 消费为 `0/1`；现行累计见本文首节。

## 2026-08-28 — D0 Intake 与隔离

### Owner 指令

- 创建 FEAT-134 的 `yijie` 与 `yijie-desktop` 分支。
- 完成正式 D0 治理包、工作区隔离记录和只读 Contract First 能力矩阵。
- 暂不修改实现代码。
- 不创建 Contracts/Host 分支，除非审计证明需要。

### 已执行

1. 读取 `yijie`、`yijie-desktop`、`yijie-contracts`、`yijie-agent-host` 的仓库规则、README/SECURITY，以及 Contract First、Feature Delivery、ADR 和 UI 规范。
2. 在 clean baseline 上创建：
   - `yijie@9a8f1d7b49a9b362c03085740f6f8f75c67d5cf7`
   - `yijie-desktop@af38353694c3eb045365b7f3450ffc8a95aaf8a1`
3. 以只读方式审计固定 Runtime schema、Contracts v1/v2/v3、Host projection/pin、Desktop private IPC、FEAT-132 ConversationState、SQLCipher history 与 FEAT-133 Timeline。
4. 审计证明当前链路丢失 AgentMessage `phase` 和稳定 `turn/plan/updated`，无法只在 Desktop 合法完成 FEAT-134 Must；依据条件授权，在各自 clean baseline 上补建：
   - `yijie-contracts@164b14f609537d727a52326832da04430aecc4ab`
   - `yijie-agent-host@1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`
5. 仅在 `yijie/docs/features/FEAT-134-desktop-streaming-progress-final-response/` 新建正式 D0 文档；没有修改任何实现代码、schema、pin、数据库、依赖或 Runtime。

### 未执行

- 未修改 `yijie-contracts`、`yijie-agent-host`、`yijie-desktop` 或 `yijie-codex` 文件。
- 未创建 `yijie-codex` 分支，未 fetch/pull/rebase，未升级、编译、替换或同步 Runtime。
- 未运行实现测试、canonical Desktop smoke 或真实 Provider Turn。
- 未发送 prompt、调用工具、触发 Agent 文件读写、执行生产写入或公开发布。
- 未 stage、commit 或 push；Owner 本轮只授权了分支创建与 D0 产物，没有授权提交。

## D0 决策记录

### D0-001 — 保留 FEAT-134 原始三层 Must

决定：保留 commentary/progress、模型推理记录与 final answer 的真实分层，不把 FEAT-134 收窄成单 Assistant 文本美化。

依据：该分层是完整 Epic 对话可理解性的核心；若删除 CAP-010/011/012，Feature 将无法实现其主要目标。

影响：受影响仓库从 `yijie + yijie-desktop` 扩展为 `yijie + yijie-contracts + yijie-agent-host + yijie-desktop`。

### D0-002 — Contract First，禁止 Vue 推断

决定：采用 negotiated Agent session event vNext，保留 v1/v2/v3；Contracts → Host → Desktop private IPC/ConversationState/SQLCipher → ChatTimeline。

依据：当前 Contracts/Host 不投影 AgentMessage phase 或稳定 plan；Desktop 生产 live wire 也没有足够 identity/lifecycle。按文本、最后一项或到达时间推断会破坏重放与历史等价。

停止条件：若实现需要原地修改旧 closed union、启用 Runtime experimental API、从缺失字段猜语义或建立第二 authority，立即停止并重新治理。

### D0-003 — Reasoning 采用 ADR-0016 raw projection

决定：产品名称为“模型推理记录”，展示受支持 raw reasoning 的不可信纯文本；`complete/incomplete/unavailable` 与 reason code 独立于 final。

约束：不解析 Markdown/HTML、不激活链接、不创建 tool action、不增加产品级复制按钮；不得进入日志、遥测、审计、错误正文或 receipt。缺失正文不得用 final、工具输出、模板或元数据冒充。

当前缺口：Contracts v2/v3 虽有 raw reasoning 事件，canonical Host 默认关闭该投影，compatibility 清单也未锁定对应 Runtime notification；managed provider reasoning effort/summary 为 `none`，Desktop start-turn 也不请求 reasoning effort。仅完成 contract/mapper 不会产生 ADR-0016 可验收的非空正文。

后续修订：Owner 已批准精确的 local-only `reasoning effort=high + raw projection`，`ai_behavior_change=model`，该范围 blocker 已解除；不能用 unavailable 冒充 PASS 的 ADR-0016 门槛保持不变。

### D0-004 — 稳定 plan 与 experimental plan 分离

决定：只投影固定 Runtime 的稳定 `turn/plan/updated`；明确排除 experimental `item/plan/delta`，`experimentalApi=false` 保持不变。

语义：plan 是有权威来源时才显示的 ordered snapshot；没有真实 plan 时只显示 Turn lifecycle 的克制等待态，不生成步骤、进度百分比或耗时。

### D0-005 — Desktop SQLCipher 是历史 authority

决定：live/hydration 等价只覆盖 Desktop 已观察并成功持久化的事实。Host 的 512 条 process-local replay 不承担产品历史。

边界：Host 重启后补回从未被 Desktop 观察的内容、复杂 gap/resync 和 missing-final 恢复属于 FEAT-140/142；FEAT-134 不虚构这类保证。

### D0-006 — Reference Policy 与 Owner exclusions

决定：沿用 `codex-inspired-approximate-parity-v1-2026-08-27 / owner-approved-inference`。不建立 Codex Desktop version/build Freeze，不使用已撤回的三项人工材料，也不要求补采。

固定排除：语音、模型版本、推理强度配置/档位 UI、分享、切换置顶摘要、右侧上下文面板、分支到新聊天、CAP-022 / GS-006 文件修改与 Diff。

### D0-007 — 安全验证边界

初始决定：FEAT-134 paid call 允许 Owner 明确授权的 canonical 无敏感纯文本 prompt `1` 次。后续 Owner 明确增加 `2` 次重试，并在前三次用尽后另外批准 `1` 次；四次均为显式授权而非程序自动重试，现已消费 `4/4`。新增 Turn 前必须取得新授权。destructive operations 与 production writes 均为 `false / 0`；历史 Feature 授权不可转移。

只允许正常、非破坏性测试。禁止强杀、故障注入、权限破坏、binary 替换、恶意或攻击 fixture。不能安全执行的验收必须记录 `NOT RUN + 原因 + 影响`，不得伪造 PASS。

### D0-008 — Schema presence 不等于 canonical producer

决定：Contracts/Host vNext 只保留真实 Runtime 事实，不把可选字段或 schema event 解释成当前 provider 一定会产生。

- AgentMessage phase 可能为 `null`，且 Runtime schema 明示 provider 并不稳定地产生；`null` 只能映射 unknown，不能由“最后一项”或 `turn.completed` 猜成 final。
- 稳定 `turn/plan/updated` 存在于 schema，但当前没有 FEAT-134 canonical producer evidence；没有事件时不显示 plan、不生成步骤。
- canonical `4/4` 已消费：前三次取得 raw reasoning 非空、AgentMessage phase=`null`、plan update=`0` 的 retained-tail content-free shape；第四次在 Provider 前 `turn_start_failed`，零事件且 cursor 未前进。corrective 已重建并完成无 prompt 的静态页面 smoke，但没有 fresh 正向 streaming，所以 CAP 与 D4 仍保持 pending/NOT RUN。

## 当前工作区边界

| 仓库 | 当前分支 | 文件变化允许范围 |
|---|---|---|
| `yijie` | `feat/feat-134-desktop-streaming-progress-final-response` | FEAT-134 治理包与 source-first 证据 |
| `yijie-contracts` | 同名 FEAT-134 分支 | 0.6.0/v4 source、生成物、fixtures、tests 与治理文档；immutable HEAD `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`，未 push |
| `yijie-agent-host` | 同名 FEAT-134 分支 | baseline `1b7bfd…` → initial `201fd9…` → corrective child/final `b9358f…`；精确 pin Contracts `3832a6…`，工作树 clean、未 push |
| `yijie-desktop` | 同名 FEAT-134 分支 | 精确 pin Host `b9358f…`；实现、lint/test/build 与 corrective stable/canonical rebuild PASS；immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`，工作树 clean、未 push |
| `yijie-codex` | `develop` | 永久不允许 FEAT-134 修改 Runtime 核心、binary、schema 或 pin |

完整 11 仓 baseline 和 clean-start 事实见 `evidence/workspace-isolation-baseline-2026-08-28.md`。

## Gate 状态

| Gate/活动 | 状态 | 说明 |
|---|---|---|
| D0 Product/UX | PASS | 背景、目标、非目标、主流程、七类 UI 状态、8 条 Must AC、Contract First 顺序与安全边界完整 |
| Workspace isolation | PASS | 四仓均有独立 FEAT-134 分支；Contracts/Host/Desktop 已形成各自 immutable commits 且未 push，Desktop clean；yijie 治理包未提交，Runtime 不变 |
| Read-only capability audit | PASS | 已定位 phase、plan、reasoning、lifecycle、notice、hydration 的真实可用与缺口 |
| CAP-011 canonical producer | PASS | #5 持久化 raw reasoning item/part=`1/1`；#6 final-source UI reasoning expanded |
| CAP-010 canonical producer | PASS（负向 shape） | #5/#6 AgentMessage phase=`null` 准确保留 unknown，不执行 final 推断；显式 final_answer 正向由确定性 Contracts/Host/Desktop tests 证明 |
| CAP-012 canonical producer | PASS（absence/no-fake） | #5 plan update/step=`0/0`，准确保持 no-plan；稳定 plan 正向 shape 由确定性 contract/mapper/reducer tests 证明 |
| Contracts v4 source candidate | PASS | immutable commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；Host/Desktop 均精确 pin，未 push |
| Host implementation candidate | PASS | 线性历史 `1b7bfd… -> 201fd9… -> b9358f…`；final authority 全量门禁 PASS，未 push |
| Desktop implementation | PASS / COMMITTED | `7b9daa791635250d0628c9e9f553cf40fab5ad96`；工作树 clean、未 push；TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff PASS，review 无 open P0/P1/P2 |
| Canonical smoke | PASS | #5 提供持久化计数与 light/200%/键盘；#6 提供 final-source processing→completed UI、expanded rows、Composer 恢复与正常清理，二者证据不混用 |
| dark theme | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| Reduce Motion | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| 精确 1180×760 | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| D4 | PASS | implementation、8 条 Must AC、真实 canonical、representative failure、focused/full checks、Artifact 与 scoped diff review 完成；demo_fast 不要求 implementation commit |

## 下一阶段顺序

实现按 source-first 顺序工作：

0. `COMPLETED / CONSUMED 10/11`：历史 tranche `4/4` 与当前 tranche `6/7` 均保留；当前剩余 `1` 次，没有程序自动重试。
1. `COMPLETED / COMMITTED`：在 `yijie-contracts` 完成 v4 contract、compatibility、fixture、生成物与 contract tests，并形成 immutable commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；未 push。
2. `COMPLETED / COMMITTED`：在 `yijie-agent-host` 完成 version-gated mapper、精确 Contracts pin、local fixed high/raw、closed producer与测试；线性提交历史 `201fd9… -> b9358f…`，最终 authority 为 `b9358f…`，未 push。
3. `COMPLETED / COMMITTED`：Desktop private projection / FEAT-132 authority / SQLCipher / FEAT-133 Timeline、payload-v2-only reconciliation 与跨层 repeated-finalized 修复已提交为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`；clean、未 push。
4. `COMPLETED`：#5 保存 content-free 持久化计数与 light/200%/键盘，#6 保存 final-source UI 状态与正常清理；不保存正文，且不混用两次证据。
5. `WAIVED / NOT REQUIRED`：dark theme、Reduce Motion、精确 1180×760 逐项移出 FEAT-134 门禁；不执行、不恢复、不写 PASS。
6. `D4 PASS`：本地真实 Demo 可用。
7. `PENDING YIJIE CLOSEOUT`：Desktop 已提交、clean、未 push；`yijie` 治理包仍未提交，需 Owner 授权，不影响已成立的 demo_fast D4。

当前无 D4 产品证据 blocker。Desktop immutable commit 已形成且未 push；D4 PASS 不表示 `yijie` 已提交、任何仓库已 push、生产可用或完整 Epic 完成。
