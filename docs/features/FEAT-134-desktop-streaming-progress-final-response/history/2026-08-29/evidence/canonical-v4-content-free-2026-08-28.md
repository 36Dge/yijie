# FEAT-134 canonical v4 content-free 验证记录

> 状态：`PASS / D4`
> 范围：`local + demo_fast + stable`
> 内容边界：本文不保存或复述 prompt、reasoning、plan、final 正文，也不保存这些正文的哈希。

## 0. 最终 D4 证据（2026-08-29）

历史授权 tranche `4/4` 保留；当前追加 tranche 已消费 `6/7`、剩余 `1`，Feature 累计 `10/11`。每次均由 Owner 显式授权，不是程序自动重试；工具调用和 Agent 文件/项目读写仍禁止。

### #5：持久化 metadata 与 UI 基线

#5（首次 finalized-content P2 修复源码）进程：Desktop `01:49:09`、Host `01:49:34`、Runtime `01:49:35`（2026-08-29，Asia/Shanghai）。content-free metadata：

| 项目 | 结果 |
|---|---|
| attempts | `1` |
| outbox / Turn | `done / completed` |
| terminal | `1` |
| v4 events | `187` |
| raw reasoning item / part | `1 / 1` |
| stable plan update / step | `0 / 0` |
| AgentMessage phase | `null` |
| UI 基线 | light、200% zoom、键盘 `PASS` |

`phase=null` 是 Runtime 允许的合法 unknown，Desktop 不按位置或 terminal 猜成 final；因此 canonical 只证明负向 producer shape。显式 `final_answer` 默认展开的正向行为由 Contracts/Host/Desktop 确定性测试证明。

#5 后发现跨层 P2：native 已接受 repeated finalized reasoning lifecycle 并持久化 cursor/source，但 `TimelineDelta::Ignored` 未跨 WebView，TS 仍 fail-closed。修复后最终门禁为 TS `835/835`、Rust `316 pass + 3 ignored`、lint/build/fmt/diff PASS，review 无 open P0/P1/P2。

### #6：最终源码 UI smoke

#6 final-source 进程：Desktop `02:02:12`、Host `02:02:39`、Runtime `02:02:40`；fresh task content-free ID `01a0498a-5574-7cf2-9652-14f47b6db9d4`。UI 观察到 processing→completed，reasoning 与 unknown assistant 均 expanded，Composer 恢复；随后使用应用自身 `Cmd+Q` 正常清理。

#6 未另取 DB event counts，绝不把 #5 的 `187` 冒充 #6。临时 probe 源码与 target 残留均为 `0`，Host 空 probe 目录已删除。Runtime 保持 clean `yijie-codex@0ce5902ed400866be0196886bb78f693a004d68d`，binary/manifest 匹配，`experimentalApi=false`，未修改、升级或重编译。

- dark theme：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。
- Reduce Motion：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。
- 精确 `1180×760`：`WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。

按 `demo_fast` 规范 D4 不要求 implementation commit。Owner 后续授权 Desktop 提交，immutable commit 为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`，工作树 clean、未 push；`yijie` 治理包仍未提交。

## 1. 身份与不可变边界

| 项目 | 事实 |
|---|---|
| Contracts authority | `yijie-contracts@3832a6c5e99b2a6365f193280fdb887c8fdbc2de` |
| Host baseline | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` |
| Host 首个 FEAT-134 实现提交 | `201fd9f8fff6e1ee18ddc1a0477e329b0d75af0c` |
| Host corrective child / Desktop authority | `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` |
| Runtime | `yijie-codex@0ce5902ed400866be0196886bb78f693a004d68d`，`experimentalApi=false` |
| Desktop | immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`；message `feat(chat): deliver FEAT-134 streaming progress and final response`；工作树 clean、未 push |
| 发布 | 未 push、未发布、未写 public/production |

Host SHA 是线性历史：`1b7bfd… -> 201fd9… -> b9358f…`。`201fd9…` 首次实现把 Runtime Item content 过窄地解码为字符串数组；`b9358f…` 是其直接 corrective child，将一般 content 保持为 opaque raw JSON，并只对已完成 reasoning 的受支持形状执行专门解码。Desktop 只精确 pin 最终 authority `b9358f…`；不能抹去首个提交暴露问题的历史。

Runtime 未修改、升级、重编译、替换或重新固定。验证没有启用 experimental API，没有影响 public/production。

## 2. Owner 授权与消费

以下记录是历史首个 tranche：初始授权允许 `1` 次 canonical 无敏感纯文本 Turn；Owner 随后明确增加 `2` 次重试授权，并在前三次用尽后另外授权 `1` 次。没有为后三次授权虚构时间戳。

- 总上限：`4`
- 已消费：`4/4`
- 自动重试：`false`
- 每次行为：分别由 Owner 明确授权，不是程序自动重试
- 工具调用：禁止，未授权
- Agent 文件/项目读写：禁止，未授权
- prompt、reasoning、plan、final 正文及其哈希：未进入本文

该历史 tranche 在当时已用尽。Owner 后续另行授权 current tranche `7` 次；现行消费见本文第 0 节。

## 3. 四次 canonical 尝试的 content-free 结果

### 尝试 1/4

Host 已接收 Runtime 事实，但首个 Host 提交 `201fd9…` 对 structured Item content 使用了过窄的字符串数组解码，导致投影失败。该问题通过 corrective child `b9358f…` 修复并加入确定性测试。此尝试不构成 Desktop live smoke PASS。

### 尝试 2/4

暴露 Desktop SSE tail/recovery 缺口：旧的 idle/不可恢复 Host session 占据恢复队列。只对该 stale session 调用了与 UI Stop 相同的正常领域 interrupt action，由 coordinator 正常收口；未强杀、未故障注入、未直接修改数据库。此尝试不构成 Desktop live smoke PASS。

### 尝试 3/4

Host/Runtime 正常完成并保留到 sequence `87`。Desktop 最初只持久化到 sequence `32`；sequence `34` 是合法的 AgentMessage `item.started`，其中生命周期 snapshot 的 `text` 为空且 `phase=null`。Contracts v3/v4 允许空 lifecycle snapshot，但 Desktop parser 错误地拒绝空 `text`，导致同批 replay frames 在交付已解析的后续事实前整体失败。

修复后增加了 v3/v4 空 lifecycle snapshot 与 v4 replay-to-terminal 测试。同一已接受 Turn 的 Host retained tail 随后仅通过生产 `ConversationApplication::stream_active_turn` v4 GET/replay 路径消费，并把 durable cursor 从 `32` 原子推进到 `87`：

- 没有新的 Turn POST；
- 没有新的 Provider/Runtime 调用；
- 没有新增 prompt；
- 没有工具调用或 Agent 文件/项目读写；
- 临时 ignored harness 只调用生产 stream/reducer/persistence 路径，使用后已删除；
- harness 的末尾诊断断言曾把领域类型拼写写成 `agent_message`，而实际类型是 `agentMessage`；该临时断言失败发生在终态已原子提交之后，不改变生产路径提交结果。

### 尝试 4/4

Owner 在前三次授权用尽后另外批准 canonical `pnpm tauri:demo-fast:stable` 最多发送 `1` 次无敏感纯文本 prompt；禁止工具调用和文件读写，不自动重试。实际仅提交 `1` 次，没有重试；本文不保存、复述或哈希该 prompt 以及 reasoning、plan、final 正文。

本次在 Provider 前失败，content-free 持久事实如下：

- Desktop 已建立新 Turn 并进入 queued，但 outbox 以 `failed` 收口，`attempt_count=1`，`runtime_turn_id` 为空；
- 新 Turn 的 events、items、notices、terminal 均为 `0`，durable cursor 未前进；
- Host session 为 `idle`，`failure_code=turn_start_failed`；
- Provider 未启动，Runtime Turn 未启动；没有工具调用、Agent 文件/项目读写或程序自动重试。

高置信根因重建保留两层证据强度：直接持久证据最深只到 `turn_start_failed`；`thread-not-found` 是依据进程时间线和确定性代码路径作出的推断，不冒充直接 Runtime 错误日志。运行 bundle 与 Runtime 新进程均在 `22:22` 启动，而该历史 thread 形成于 `18:55`；旧纯文本链路使用 v1 start，没有在新 Runtime 进程中执行 resume。固定 Runtime 的 `turn/start` 只读取进程内 thread manager；历史 thread 未加载时会在 Provider 前进入 thread-not-found 路径，Host 再把 Runtime start 失败归一为 `turn_start_failed`。这与本次 Provider/Runtime Turn 均未启动、cursor 不前进和零事件事实一致。

针对该问题先形成 Desktop-only corrective：仅当 exact local FEAT-134 `feat134_streaming_enabled` 为真时，纯文本 create/submit 走 v2；v2 在 start 前 resume，并严格校验 task、agent session、Codex thread、idle、无 active Turn、model ready 和无 failure。该阶段建立了按次授权路径的 fail-closed 与无自动重试边界。flag=false、public/production 与旧 v1 行为保持不变，既有 flag=false v2 幂等重试语义也保持；Contracts、Host 与 Runtime 均未修改。最终候选对 Transport/AcceptedResponseInvalid 的三分支 reconciliation 见第 5 节。

该阶段的确定性验证已通过：`pnpm test` 为 103 files / 833 tests，`pnpm lint` PASS，`pnpm build` PASS；`cargo test` 为 300 pass / 3 ignored / 0 fail。它们是 pre-final-candidate 历史，不替代第 5 节最终候选的聚合验证。

## 4. sequence 87 的 content-free 结果

| 事实 | 结果 |
|---|---|
| durable cursor | `87` |
| Turn terminal | `1` 个，`completed`，诊断 code 为空 |
| outbox | `done` |
| `turn.started` | `1` |
| `item.started` | `3` |
| `item.completed` | `3` |
| reasoning delta | `26` |
| reasoning finalized | `1` |
| AgentMessage delta | `51` |
| `turn.completed` | `1` |
| reasoning Item | `complete`，UTF-8 `341` bytes，`1` 个 part |
| AgentMessage Item | `completed`，`phase=null`，UTF-8 `395` bytes |
| stable plan | `0` 个 update，`0` 个 step |
| notices | 空 |

事件 metadata 合计为 `86`，durable sequence/counter 为 `87`；sequence domain 还包含一个 reducer 接收但不生成 Item metadata 的事实。本文不保存该事实或任何内容正文。

上述结果证明：当前 canonical producer 确实产生了非空 raw reasoning；AgentMessage phase 在本次结果中为 `null`，没有被猜成 final；工具禁令下未产生 stable plan，Desktop 没有伪造 plan。稳定 plan 的正向 shape 仍由 Contracts/Host/Desktop 确定性 fixture 与测试覆盖，不能把本次 `0` 个 plan 事件描述为 canonical plan producer PASS。

## 5. 解锁后的应用只读检查与最终候选

解锁后先对更早的 canonical 执行应用自身的 `Cmd+Q`。旧 Desktop、Host 与 Runtime PID 随后均消失；没有使用强杀。随后启动的 `22:22` bundle 通过 exact checker，确认 Contracts `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`、Host `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` 与 `local/demo_fast/stable` 激活均正确。第四次授权于 `23:02` 在该 pre-corrective bundle 中消费；corrective 是失败后的 `23:16+` 才写入。

在第四次失败前的旧进程打开最近既有 FEAT-134 session 后，只保存以下 content-free UI 事实：

- SQLCipher hydration 后存在 Timeline、第 1 轮与“已完成”状态；`loading=false`、`streaming=false`；
- 过程记录默认折叠，键盘可以展开和收起；该 disclosure 操作仅属于旧进程证据；
- canonical 的 AgentMessage `phase=null` 映射为未分类模型消息；展开后显示固定“未标注阶段、不视为最终回答”提示，“模型回答”标签不存在；
- 200% zoom 下 Timeline、Turn、Composer、发送控件均存在，过程记录仍可用键盘展开；随后已恢复 100%；
- 当前 live light theme 完成渲染。

第四次失败所在的旧 canonical 随后通过应用自身 `Cmd+Q` 正常退出，Host、Runtime 与 runner 均完成正常清理，没有强杀。Desktop corrective stable build PASS；随后从 corrective 源码重建并启动 canonical 新进程：Desktop 启动于 `23:30:38`，Host/Runtime 启动于 `23:30:52`。本次重建启动没有发送 prompt，因此没有新增 Provider/Runtime Turn，也不消耗新的授权。

corrective canonical 的新任务页在 100% 与 200% zoom 下 AX tree 均可读，Composer、附件、权限与发送控件存在。`23:34` 使用键盘打开既有 FEAT-134 session 后，SQLCipher hydration 展示第 1 轮 completed、第 2 轮 queued，process/unknown rows 默认折叠，Composer、附件、权限与发送控件仍存在。本轮没有在 corrective 新进程展开 disclosure；不能沿用旧进程的 disclosure 操作冒充本轮事实。100%→200% zoom 时 Tab 聚焦 Composer，Shift+Tab 返回项目选择器，随后恢复 100%。该事实只证明 hydration、静态布局和关键控件在当前重建进程可访问，不证明 fresh streaming。

Owner 于 `2026-08-28/29` 明确将 dark theme、Reduce Motion 与精确 `1180×760` 三项从 FEAT-134 治理门禁移除。三项状态为 `WAIVED / NOT REQUIRED`，不是 PASS；无需执行或恢复，系统设置未变。先前 `1162×768` CUA 窗口截图像素只保留为历史边界，不再构成待办或 blocker。

最终 Desktop-only repair/recovery 仅在 exact-local payload v2 生效，v1 exact-local/legacy 语义不变。pre-POST resume 与 post-error reconciliation 均查询 Host session，但 matching Active 的 provenance 判定不同：

- pre-POST matching Active 若 claimed `attempt_count==1`，该 Turn 必定不是当前 operation 创建，保持 outbox=`inflight`、Turn=`queued`、runtime NULL，发布 `TurnReconciliationRequired` 且 0 次新 `/v2/.../turns` POST；只有 `attempt_count>1` crash-reclaim 才绑定既有 runtime Turn且 0 次新 POST；
- post-error matching Active 因本调用已 POST 同 operation 而直接绑定既有 runtime Turn；
- Host 确认 `turn_start_failed` 时才原子提交 outbox=`failed` 与 Turn=`failed`，reasoning=`unavailable/reasoning_not_emitted`，`terminal_code=NULL` 且无 v4 source facts；
- identity mismatch/non-idle/Err 时挂起自动 retry，保持 outbox=`inflight`、Turn=`queued`、no runtime/no v4，并发 content-free `TurnReconciliationRequired`，不伪造 failed。

启动恢复同样只在 exact-local flag=true 的 payload v2 边界内修复遗留 failed outbox + queued Turn。unknown payload version 保持原 generic fail，不走 specialized finalize；`legacy_background_does_not_run_feat134_failed_turn_recovery` PASS，证明 flag=false background 不修复或改变 generic failed outbox + queued Turn。历史已修复的旧 v1 行仅是本机过渡执行事实，不代表最终 shipped recovery 修改 v1。Vue、Contracts、Host、Runtime、public 与 production 均未修改。

该历史 candidate 的静态验证为 834 TS、313 Rust 与 targeted 31/31 PASS；它不替代本文第 0 节记录的跨层 P2 修复后最终 835 TS / 316 Rust 复验。

最终源码通过 Computer Use 触发应用自身 `Cmd+Q` 正常退出旧构建并完成 Desktop/Host/Runtime/runner 清理，没有强杀。随后 v4 pin 校验与 stable debug app rebuild PASS，并完成 no-prompt startup：Desktop `2026-08-29 00:34:04`、Host `00:34:30`、Runtime `00:34:30`（Asia/Shanghai）。没有发送 prompt，也没有启动新的 Provider/Runtime Turn。

最终 full AX 只登记 content-free 状态：controls 均 present；status counts 为 queued=`0`、streaming=`0`、completed=`2`、stopped=`1`、failed=`2`、updated=`1`。未点击历史正文；不保存 raw AX、UI 截图或任何 prompt/reasoning/plan/final 正文及哈希。该证据只证明 startup/state smoke，不证明 fresh corrected successful Turn。

本节不保存 UI 截图、可访问性树、prompt、reasoning、plan 或 final 正文及其哈希。

## 6. 已证明与限制

已证明：

- Contracts v4、Host v4 projection、Desktop decoder/reducer/SQLCipher persistence 可以在同一已接受 Turn 的 retained-tail production path 上到达唯一 completed terminal；
- raw reasoning 非空事实可以 content-free 地确认；
- `phase=null` 被保留为 unknown，不执行 last-item/terminal 推断；
- 缺少 plan 时不生成步骤；
- 没有重复 POST、重复 Provider call 或重复 terminal。
- 旧 canonical 可以通过应用自身 `Cmd+Q` 正常退出，无强杀；
- pre-final-candidate canonical 可以通过 exact pin/activation checker 后启动，并从 SQLCipher hydration 最近既有 session；
- 旧进程 hydrated Timeline 保留 completed、unknown phase、默认折叠过程记录，并曾完成键盘 disclosure 操作；
- light theme 与 200% zoom 下关键对话控件存在。
- 第四次失败所在的旧 canonical 可通过应用自身 `Cmd+Q` 正常退出，Host/Runtime/runner 均正常清理；
- Desktop corrective stable build PASS，corrective canonical 新进程已重建并启动；100%/200% zoom 的新任务页与既有 session AX tree 可读，SQLCipher hydration 显示第 1 轮 completed、第 2 轮 queued、process/unknown rows 默认折叠，Composer/附件/权限/发送控件与 Tab/Shift+Tab 焦点路径存在，且未发送 prompt。
- 最终 exact-local payload v2 recovery 的 pre-POST matching Active 按 provenance 分支：attempt_count=1 suspend并发 TurnReconciliationRequired，attempt_count>1 crash-reclaim 才 bind，两者均 0 新 POST；post-error matching Active 直接 bind；confirmed failure 才终态化，identity mismatch/non-idle/Err 不伪造 failed；
- 历史 candidate 的 aggregate、lint/build/fmt/diff 与 targeted 31/31 PASS；最终跨层复验见第 0 节；
- 最终源码正常清理、v4 pin、stable rebuild 与 `00:34:04/00:34:30/00:34:30` no-prompt startup/state smoke PASS；
- dark theme、Reduce Motion、精确 1180×760 已由 Owner `WAIVED / NOT REQUIRED`，不是 PASS，也不再是待办或 D4 blocker。
- #5 取得 fresh completed Turn 的持久化 metadata、light/200% zoom/键盘和 unknown/reasoning UI 事实；
- #6 以最终源码观察 processing→completed、expanded reasoning/unknown、Composer 恢复与正常清理；
- repeated finalized lifecycle 的 native/WebView/TS 跨层语义已对齐，最终 TS 835/835、Rust 316+3 ignored，review 无 open P0/P1/P2；
- Runtime binary/manifest 与固定 SHA 匹配，且 probe 源码/target/Host 空目录均已清理。

限制：

- canonical 仍只观察到 `phase=null` 与 plan `0/0`；这证明 unknown/no-fake-step 负向语义，不证明 current provider 的 commentary/final_answer 或 plan 正向 producer。正向 shape 由确定性 Contracts/Host/Desktop tests 证明；
- #6 没有另取 DB event counts，不能把 #5 的 `187` 归给 #6；
- Desktop 已提交 `7b9daa791635250d0628c9e9f553cf40fab5ad96`、clean、未 push；`yijie` 治理包仍未提交，需 Owner 授权；
- D4 不等于 public/production ready，也不等于完整 Epic 完成。

先前 `00:02`、`00:19` 与 `00:34` 进程只属于过渡证据，历史失败不删除。当前权威收口证据是 #5 持久化 metadata 与 #6 final-source UI；历史 tranche `4/4`、当前 tranche `6/7`、Feature 累计 `10/11`。

因此本证据支持 FEAT-134 `D4 PASS`：本地真实 Demo 可用。Desktop immutable commit 已回填；它不声明 `yijie` 已提交、任何仓库已 push、生产可用或完整 Epic 完成。
