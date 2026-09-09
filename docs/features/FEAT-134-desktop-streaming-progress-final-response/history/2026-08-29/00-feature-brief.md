# FEAT-134 — Desktop 流式响应、过程状态与最终回答分层

> Profile: `demo_fast` · Exposure: `local` · D0: `PASS` · D4: `PASS` · Created: `2026-08-28`

最终源码实现、Must AC、真实 smoke 与 scoped diff review 已完成。Desktop 已形成 immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`，工作树 clean、未 push；`yijie` 治理包仍未提交。历史 canonical 授权 tranche `4/4` 保留；当前追加 tranche已消费 `6/7`、剩余 `1`，Feature 累计 `10/11`。

## 1. 需求背景

FEAT-132 已把 Thread / Turn / Item / ContentBlock 收敛到 `ConversationState`，FEAT-133 已把该领域状态投影为独立 `ChatTimeline`。当前真实链路仍有一层关键缺口：Host 到 Desktop 的 live projection 把 Assistant 流压缩成单一文本，未完整保留 AgentMessage `phase`、稳定 `turn/plan/updated`、reasoning 可用性和 Item 独立 lifecycle。

如果直接在 Vue 中按“最后一条”“文本内容”或“到达顺序”判断 commentary、final、plan 或 reasoning，就会形成第二套不可重放的语义 authority；实时展示和历史重开也会产生差异。因此 FEAT-134 必须以 Contract First 方式补齐投影，再进入 Desktop 聚合、持久化与 Timeline 展示。

本 Feature 是完整 Epic“Yijie 对话工作区与 Codex Desktop 行为对齐”的组成部分。总目标仍是：在不修改固定 `yijie-codex` Runtime 核心的前提下，让 Yijie Desktop 的对话信息层级、状态反馈和主要交互形成 Codex-inspired、Yijie-first 的近似一致体验。FEAT-134 只负责实时流、过程状态、推理记录和最终回答分层；其完成不等于 Epic 完成。

## 2. 目标

- 多个 Assistant Item/ContentBlock 按真实 identity 聚合流式 delta，不丢字、不重复、不串项。
- commentary、稳定 plan、模型推理记录和 final answer 只依据显式协议语义分层。
- `item.completed` 与 `turn.completed` 各司其职；完成、失败、中断和 partial content 准确。
- `item.completed` authoritative snapshot 与累计 delta 确定性对账，重开历史不产生重复 final。
- 对 Desktop 已观察并写入 SQLCipher 的事件，live 与 hydration 保持 identity、顺序、phase、正文和状态等价。
- 在 FEAT-133 `ChatTimeline` 中形成最终回答优先、过程克制、状态可访问的体验，并保留 FEAT-127 附件和 FEAT-128 Artifact authority。

## 3. 非目标

- 不修改、升级、重编译、替换或重新固定 `yijie-codex` Runtime、binary、schema 或 pin；`experimentalApi=false`。
- 不使用实验性的 `item/plan/delta`，不从文本、顺序或时间推测 phase、plan、reasoning 或 warning 归属。
- 不新增 Stop/Cancel 控件；只展示真实 interrupted/failed，控制动作属于 FEAT-139。
- 不把 Host process-local replay 当作产品历史，也不吸收 FEAT-140/142 的复杂重连、漏事件和 missing-final 恢复。
- 不重写 Composer、Sidebar、附件、Artifact、Command/Tool、审批或长对话虚拟化。
- 不新增依赖、React、assistant-ui 或第二套 Timeline/状态 authority；确需依赖时停止并申请 Owner 授权。
- 除 Owner 明确批准的 `demo_fast/local` 固定 reasoning effort=`high` 与 Host raw projection 外，不修改模型、prompt、Provider、summary 或其它 start-turn reasoning 配置；不增加推理强度 UI，不影响 public/production。
- 不实现自动滚动、阅读位置保持、reader state 或跟随策略；FEAT-134 只向 FEAT-141 提供真实 active/streaming signal。
- 不建立 Codex Desktop version/build Freeze，不使用已撤回人工材料，不要求人工补采，也不追求逐像素一致。
- 不实现八项 Owner 主动排除能力：语音、模型版本信息、模型推理强度配置/档位 UI、分享、切换置顶摘要、显示右侧上下文面板、分支到新聊天、CAP-022 / GS-006 文件修改与 Diff。
- 不进行超出 Owner 精确授权的 Provider prompt、付费调用、生产写入或 public 发布；历史 tranche `4/4` 已消费且不覆写，当前追加 tranche 已消费 `6/7`、剩余 `1`，Feature 累计 `10/11`。
- dark theme：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变。
- Reduce Motion：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变。
- 精确 `1180×760`：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变。

## 4. 参考与权威

### 4.1 参考策略

- Policy ID：`codex-inspired-approximate-parity-v1-2026-08-27`
- Mode：`owner-approved-inference`
- 优先级：Owner 最新决定 → Yijie Design System → 固定 Runtime 与 Contracts/Host 权威投影 → 当前 Yijie 实现 → 工程推测。
- 先前三项人工证据已撤回，不进入需求、设计、验收或 provenance。
- 颜色、间距、图标、文案和局部布局可以与 Codex Desktop 合理不同。

### 4.2 Runtime 冻结

| 项目 | 固定事实 |
|---|---|
| `yijie-codex` commit | `0ce5902ed400866be0196886bb78f693a004d68d` |
| upstream | `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| Runtime | `0.144.6` |
| stable schema | 267 files / tree SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` |
| transport | stdio |
| experimental API | `false` |

### 4.3 语义 authority

1. 固定 Runtime stable schema：上游事实，不在本 Feature 修改。
2. `yijie-contracts`：跨仓 Agent session event vNext 的唯一 wire authority。
3. `yijie-agent-host`：唯一 Runtime → negotiated contract mapper。
4. FEAT-132 `ConversationState`：Desktop 进程内 Timeline 唯一语义 authority。
5. Desktop SQLCipher：Desktop 已观察对话历史的 durable authority。
6. FEAT-133 `ChatTimeline`：展示层，不解释 raw wire，不建立第二状态机。

详细审计见 [Contract First 能力矩阵](evidence/contract-first-capability-matrix-2026-08-28.md)。

## 5. Contract First 决策

只读审计证明 Contracts/Host 分支是必要的，而不是预防性扩仓：

- 固定 Runtime 的 AgentMessage lifecycle 有 `phase=commentary|final_answer|null`，当前 Contracts/Host 未投影。
- 固定 Runtime 有稳定 `turn/plan/updated`，当前 Contracts/Host 未投影。
- Contracts v2/v3 已有 raw reasoning delta/finalized，但兼容清单未锁定对应 Runtime notification，canonical Host 默认关闭 raw reasoning，summary 也未投影。
- Desktop WebView live wire 只有 append/Turn terminal 等简化事件，生产 Assistant identity 固定为单 Item，Item lifecycle 和 notice 被压缩或忽略。

因此采用以下 source-first 顺序：

1. `yijie-contracts`：新增显式协商的 Agent session event vNext，保留 v1/v2/v3 closed union；锁定 AgentMessage phase、稳定 `turn/plan/updated` 与受支持 reasoning lifecycle，并同步 compatibility、OpenAPI、protobuf、JSON Schema、fixture 和测试。
2. `yijie-agent-host`：按 itemId/turnId 保存并投影 phase/plan/reasoning，执行版本协商，升级精确 Contracts pin；不得投影 experimental `item/plan/delta`。
3. `yijie-desktop`：扩展私有 IPC、FEAT-132 authority 和 SQLCipher durable schema；不得在页面组合层猜语义。
4. `ChatTimeline`：消费新 ViewModel，完成分层、节流、状态与可访问性，不建立新 authority。

当前分类为 `contract-impact=semantic`。前提是使用新协商版本；如果实现尝试直接改写 v1/v2/v3 closed union，则风险升级为 breaking，必须停止并重新治理。

canonical stable 原先把 Host raw-reasoning projection 设为 `false`，managed provider reasoning effort/summary 为 `none`，因此仅完成 Contract/mapper 不会产生 ADR-0016 可验收正文。Owner 于 `2026-08-28T13:35:01+08:00` 明确批准：仅在 `demo_fast/local` 把固定 managed provider reasoning effort 设为 `high` 并启用 Host raw projection，`ai_behavior_change=model`；不新增推理强度 UI，不修改 Runtime，不影响 public/production。该授权解除实现范围 blocker，但不预先证明 CAP-011；真实 producer 仍需后置验证。

同样，schema 存在不等于 canonical producer 已被证明：Runtime 明确允许 AgentMessage phase 为 `null`，provider 也可能不稳定地产生 phase；稳定 `turn/plan/updated` 的 schema 存在也不等于 provider 会发送。Owner 初始授权 `1` 次无敏感纯文本 canonical 验证，随后明确增加 `2` 次重试，并在前三次用尽后另外批准 `1` 次；四次分别由 Owner 授权，均非程序自动重试，现已消费 `4/4`。前三次 content-free 结果确认 producer 产生非空 raw reasoning，但 AgentMessage `phase=null` 且 plan update 为 `0`；Desktop 必须保留 unknown 且不生成 plan。第三次的 Host retained tail 经 parser 修复后通过生产 v4 GET/reducer/persistence 路径到 sequence `87`，没有新 POST、Provider call 或 prompt；这不是最终重建进程上的 fresh、不间断 UI smoke。

第四次实际只提交一次，按授权禁止工具调用、文件读写和自动重试；Desktop Turn queued 后 outbox 以 `failed` 收口，`attempt_count=1`、`runtime_turn_id` 为空，事件/Item/notice/terminal 均为 `0`，cursor 未前进；Host 保持 idle 并给出 `turn_start_failed`，Provider 与 Runtime Turn 均未启动。直接持久证据最深仅为 `turn_start_failed`；结合 bundle/Runtime 新进程 `22:22` 与历史 thread `18:55` 的时间线，以及旧纯文本 v1 start 不 resume、Runtime `turn/start` 只读取进程内 thread manager 的确定性代码路径，根因高置信推断为 Provider 前 thread-not-found，不把该推断冒充直接日志。

第一层 corrective 只修改 Desktop：仅 exact local FEAT-134 `feat134_streaming_enabled=true` 时，纯文本 create/submit 走 v2，并在 start 前 resume；严格校验 task、agent session、Codex thread、idle、无 active Turn、model ready 与无 failure。resume/start 失败一律 fail closed，且这一按次授权的 local canonical 路径不做 outbox 自动重试。flag=false、public/production、旧 v1 与既有 flag=false v2 幂等重试语义不变；Contracts、Host、Runtime 均不改。其历史全量验证为 103 files / 833 TS tests 与 Rust 300 pass / 3 ignored / 0 fail。

最终 Desktop-only repair/recovery 仅在 exact-local payload v2 生效；v1 exact-local/legacy 语义不变。pre-POST resume 的 matching Active 按 provenance 隔离：claimed `attempt_count==1` 必定不是当前 operation 创建，保持 outbox inflight、Turn queued、runtime NULL，发布 content-free `TurnReconciliationRequired` 且 0 次新 POST；只有 `attempt_count>1` crash-reclaim 才绑定既有 runtime Turn且 0 次新 POST。post-error reconciliation 的 matching Active 因本调用已 POST 同 operation 而直接绑定。confirmed `turn_start_failed` 才原子终态化；identity mismatch/non-idle/Err 保持 inflight/queued/no-runtime/no-v4并挂起 retry，不伪造 failed。unknown payload version 保持 generic fail。没有修改 Vue、Contracts、Host、Runtime、public 或 production。

`legacy_background_does_not_run_feat134_failed_turn_recovery` PASS，明确 flag=false background 不修复或改变 generic failed outbox + queued Turn。#5 后发现 native durable cursor/source 已接受 repeated finalized lifecycle、但 `TimelineDelta::Ignored` 未跨 WebView 导致 TS fail-closed 的跨层 P2；现已修复并复审无 open P0/P1/P2。最终 `pnpm test` 835/835、`pnpm lint/build`、`cargo test` 316 passed / 3 ignored / 0 failed、`cargo fmt --all --check` 与 Desktop `git diff --check` 全部 PASS。临时 probe 源码和 target 残留均为 0，Host 空 probe 目录已删除。

#5（首次 finalized-content P2 修复源码）进程于 Desktop `2026-08-29 01:49:09`、Host `01:49:34`、Runtime `01:49:35`（Asia/Shanghai）启动。fresh Turn content-free 持久化结果为 attempts=`1`、outbox=`done`、Turn=`completed`、terminal=`1`、v4 events=`187`、raw reasoning item/part=`1/1`、stable plan update/step=`0/0`、AgentMessage `phase=null`，并完成 light、200% zoom 与键盘检查。

#6 最终源码进程于 Desktop `02:02:12`、Host `02:02:39`、Runtime `02:02:40` 启动；fresh task content-free ID 为 `01a0498a-5574-7cf2-9652-14f47b6db9d4`。UI 观察到 processing→completed，reasoning 与 unknown assistant 均 expanded，Composer 恢复，随后通过应用自身 `Cmd+Q` 正常清理。#6 未另取 DB event counts，绝不把 #5 的 `187` 冒充 #6。治理记录不保存、复述或哈希任何正文。`null` 是合法 unknown，canonical 只证明负向 producer shape；显式 `final_answer` 正向行为由 Contracts/Host/Desktop 确定性测试证明。详细边界见 [canonical v4 content-free 记录](evidence/canonical-v4-content-free-2026-08-28.md)。

## 6. 完整主流程

1. 用户通过 `cd ../yijie-desktop && pnpm tauri:demo-fast:stable` 零登录进入 Chat。
2. active Turn 尚无正文时，仅显示由真实 lifecycle 驱动的等待反馈，不显示虚假步骤、百分比、耗时或流式正文。
3. Host 按 negotiated vNext 发布 Item lifecycle、delta、phase、稳定 plan 和受支持 reasoning 状态。
4. Desktop 以 itemId、block index、event identity 和 sequence 归并；重复事件幂等，gap 明确，不静默补写。
5. Timeline 把 commentary/plan/reasoning 放在次级可折叠区域，把 `final_answer` 放在主要结果区域且默认展开；`null/unknown` 不猜成 final。
6. `item.completed` 只完成对应 Item；收到 `turn.completed` 前 Turn 保持 active。
7. completed/interrupted/failed 到达后，停止流式指示，保留所有已确认正文，按真实范围显示不完整或错误状态。
8. Desktop 把已观察事实写入 SQLCipher；重开对话时恢复相同的 identity、ordinal、kind、phase、content 和 status，不重复 final。

## 7. 交互与 UI

- 视觉方向：继承 FEAT-133 Timeline 和 Yijie token；最终回答最突出，过程信息克制，reasoning 用“模型推理记录”命名。
- Waiting：只有 active Turn 事实，没有正文时显示“正在处理”类反馈；不伪造 step/time/progress。
- Commentary/plan：次级层级，可折叠；disclosure state 绑定稳定 Item/plan identity。
- Reasoning：不可信纯文本，不能解析 Markdown/HTML、激活链接或创建 tool action；无产品级复制按钮，只保留系统原生选择/复制。
- Final：最高阅读优先级，永不默认折叠；Turn 完成后不保留 streaming cursor。
- Interrupted/failed：保留 partial content，在对应 Turn/Item 显示不完整或失败状态，不覆盖其他历史。
- Warning：上游只有 thread context 时按 thread/session scope 显示，不按到达时间猜 active Turn。
- Loading/empty/error/retry/cancel 的正式语义已写入 `feature.yaml`，后续实现必须逐项测试。

## 8. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 多 Item Unicode delta 交错、重复和批量发布后不丢、不重、不串 | 四层 fixture 与 reducer identity 断言 |
| AC-002 | commentary/plan/reasoning/final 只按显式协议分层 | vNext schema、Host mapping、Desktop negative tests |
| AC-003 | item snapshot 与 delta 确定性对账，final 唯一 | reconciliation 状态表与 history reopen |
| AC-004 | Item 完成不终止 Turn；首 delta 前只显示真实等待 | lifecycle/projection/ConversationState tests |
| AC-005 | completed/interrupted/failed 准确且 partial 保留 | 安全 fixture；不使用破坏性故障注入 |
| AC-006 | raw reasoning 纯文本、状态准确、无冒充与泄漏 | negotiation、mapping、persistence、renderer tests |
| AC-007 | Desktop 已持久化事实的 live/hydration 等价 | DB expand、snapshot/hydration/restart tests |
| AC-008 | 长流节流、文本选区不被装饰改写、布局稳定且 light/200% zoom/键盘 UI/a11y 基线通过 | perf/component tests + canonical local smoke；dark theme、Reduce Motion、精确 1180×760 为 Owner `WAIVED / NOT REQUIRED`；滚动策略留给 FEAT-141 |

所有 AC 在 D0 均为 `pending`；D0 Product/UX Ready 不代表实现或验证通过。

## 9. 工作区隔离

正式分支：

| 仓库 | FEAT-134 分支 | 起点 |
|---|---|---|
| `yijie` | `feat/feat-134-desktop-streaming-progress-final-response` | `9a8f1d7b49a9b362c03085740f6f8f75c67d5cf7` |
| `yijie-desktop` | `feat/feat-134-desktop-streaming-progress-final-response` | `af38353694c3eb045365b7f3450ffc8a95aaf8a1` |
| `yijie-contracts` | `feat/feat-134-desktop-streaming-progress-final-response` | `164b14f609537d727a52326832da04430aecc4ab` |
| `yijie-agent-host` | `feat/feat-134-desktop-streaming-progress-final-response` | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` |

Contracts/Host 分支是在只读审计证明 semantic wire gap 后，依据 Owner 的条件授权创建。Contracts 已提交为 `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；Host 线性历史为 baseline `1b7bfd…` → 首个实现 `201fd9…` → corrective child/final authority `b9358f…`，均未 push。Desktop 最终实现已提交为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`（`feat(chat): deliver FEAT-134 streaming progress and final response`），工作树 clean、未 push。`yijie` 仍仅修改本 Feature 治理目录且尚未提交；Runtime 保持 clean `0ce5902ed400866be0196886bb78f693a004d68d`，未修改、升级或重编译。详见 [工作区隔离记录](evidence/workspace-isolation-baseline-2026-08-28.md)。

## 10. 安全、授权与停止条件

- FEAT-134 历史 paid-call tranche `4/4` 保留；Owner 后续授权当前 tranche `7` 次，已消费 `6/7`、剩余 `1`，Feature 累计 `10/11`。每次均为 Owner 显式授权且没有程序自动重试；destructive operations 与 production writes 仍为 `false / 0`。FEAT-131/132 的历史 prompt 授权不可转用。
- 可执行只读审计、schema/fixture/component/reducer 测试、正常启动和应用自身正常退出。
- 禁止强杀/故障注入、破坏权限、替换 binary、恶意或攻击 fixture；无法安全验证时记录 `NOT RUN + 原因 + 影响`。
- synthetic fixture 不包含真实 prompt、用户正文、绝对路径、账号、PII、secret 或业务数据。
- 如果需要 Runtime 变化、experimental API、旧 closed union 原地修改、页面推断 phase/plan/reasoning、超出已批准 local high/raw 的模型/Provider/config 变化、额外依赖或第二 authority，立即停止。
- 30 分钟没有新事实时回到真实 schema、event trace 和完整调用链；90 分钟同一核心阻塞时采用最小 source-first 方案或请求 Owner 决策；16 小时硬停止时缩小非核心视觉范围，不删除 Must 语义。

## 11. D0 结论

Product/UX、范围、非目标、状态矩阵、Must AC、Contract First 顺序、数据/持久化影响、安全授权和四仓隔离均已定义，D0=`PASS`。最终实现、八条 Must AC、#5 持久化事实、#6 final-source UI smoke、light/200% zoom/键盘、focused/full checks 与 scoped diff review均已完成；跨层 P2 已修复并复审无 open P0/P1/P2。dark theme、Reduce Motion 与精确 1180×760 分别为 `WAIVED / NOT REQUIRED`，不是 PASS。D4=`PASS` 只表示本地真实 Demo 可用；Desktop 已提交 `7b9daa791635250d0628c9e9f553cf40fab5ad96`、clean、未 push，`yijie` 治理包仍待 Owner 授权提交。FEAT-134 D4 不等于完整 Epic 完成。
