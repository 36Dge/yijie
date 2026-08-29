# FEAT-134 只读 Contract First 能力矩阵

> Audit date: `2026-08-28` · Mode: read-only · Result: Contracts/Host branches required

> D4 follow-up `2026-08-29`: source-first gap 已闭环并通过最终验证。历史 tranche `4/4` 保留；当前 tranche `6/7`、剩余 `1`，Feature 累计 `10/11`。#5 提供 attempts=1/outbox done/completed/terminal1/v4 events187/reasoning1-part1/plan0/phase null 的 content-free 持久化事实；#6 final-source 提供 processing→completed、reasoning/unknown expanded、Composer 恢复与正常清理。#6 未另取 DB counts，不继承 #5 的 187。TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff 与 review 无 open P0/P1/P2。Runtime 固定不变。D4=PASS；Desktop immutable commit 为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`，clean、未 push；`yijie` 治理包未提交。

`phase=null` 合法映射 unknown，canonical 只证明负向 producer shape；显式 `final_answer` 与 stable plan 正向 shape 由确定性 Contracts/Host/Desktop tests 证明。dark theme、Reduce Motion、精确 1180×760 逐项 `WAIVED / NOT REQUIRED`，不是 PASS，未执行、无需恢复，系统设置未变。

## 1. 审计问题

在不修改固定 `yijie-codex` Runtime 核心、`experimentalApi=false`、不让 Vue 推测语义的前提下，现有 Contracts → Host → Desktop 链路是否足以实现：

1. 多 Assistant Item 流式聚合；
2. commentary/progress、模型推理记录和 final answer 分层；
3. Item/Turn 独立 lifecycle 与 completed reconciliation；
4. live 与本地历史 hydration 等价。

结论：**不足。** CAP-010 与 CAP-012 是明确的 semantic wire gap；CAP-011 虽已有 v2/v3 raw reasoning contract，但兼容 pin、默认配置和 Desktop snapshot 仍未形成 canonical 可用闭环。因此保持原 Must 范围时，需要 `yijie-contracts` 与 `yijie-agent-host` 分支，且必须 source-first。

## 2. 审计基线

| 层 | Branch / Commit | 关键版本事实 |
|---|---|---|
| Runtime | `yijie-codex develop@0ce5902ed400866be0196886bb78f693a004d68d` | `0.144.6` / upstream `rust-v0.144.6@5d1fbf26...` / stdio / `experimentalApi=false` |
| Contracts | `feat/feat-129-desktop-skill-marketplace@164b14f609537d727a52326832da04430aecc4ab` | working candidate `0.5.1`，HEAD 无 tag；公开 supported baseline 仍为 `contracts-v0.2.0@f16a497...` |
| Host | `feat/feat-129-desktop-skill-marketplace@1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | `api/contracts.lock` 精确 pin Contracts `0.5.1@164b14f...`，snapshot 与 Contracts HEAD 一致 |
| Desktop | FEAT-134 branch baseline `af38353694c3eb045365b7f3450ffc8a95aaf8a1` | 继承 FEAT-132 ConversationState、FEAT-133 ChatTimeline、SQLCipher history |

Runtime freeze 的 267 files schema tree SHA-256 为：

`82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`

## 3. 层级能力总览

| 能力 | 固定 Runtime stable fact | 当前 Contracts / Host | 当前 Desktop | D0 分类 | FEAT-134 决策 |
|---|---|---|---|---|---|
| Assistant delta identity | `item/agentMessage/delta` 带真实 item context | v1 delta 有 `thread_id/turn_id/item_id/delta`；Host 可发布 | WebView 生产链路压成固定 `turnId:assistant:0`，单 accumulator | Desktop private projection gap | 保留真实 itemId/block identity，禁止单 Item 合并 |
| AgentMessage phase | Item lifecycle 含 `commentary/final_answer/null`；schema 明示 provider 不保证稳定产生 | schema/mapper 丢失 phase | history/live 均无 discriminator | **semantic contract gap + canonical producer evidence gap** | vNext 投影 lifecycle phase；null 显式 unknown，不猜 final；D4 前需 content-free event-shape 证据 |
| Item lifecycle | stable `item/started`、`item/completed` | v1 已有，completed 可带 authoritative text | WebView 只暴露 append/Turn terminal，首 delta 隐式建 Item，terminal 批量封口 | Desktop private semantic gap | 保留 started/completed；item completed 不终止 Turn |
| Stable plan | stable `turn/plan/updated`，ordered steps/status；schema presence 不证明 current provider 会发送 | compatibility/schema/Host 未投影 | 仅由 Turn status 派生通用“处理中” | **semantic contract gap + canonical producer evidence gap** | vNext 投影 ordered snapshot；无 plan 不生成 step；D4 前需 content-free event-shape 证据 |
| Experimental plan | `item/plan/delta` 属于 experimental path | 无受支持 producer/projection | 无 | excluded capability | `experimentalApi=false`；明确不实现、不伪造 |
| Raw reasoning | stable reasoning text delta/item completion 可观察 | v2/v3 有 delta/finalized；Host mapper 存在但 flag 默认 false；compat 清单未锁 notification | live/persistence 基础存在；无 Item 时 snapshot adapter 丢 status，Timeline 仅元数据 note | negotiated/config/persistence gap；local high/raw 已授权 | 继承 ADR-0016 raw plain text；历史失败保留，当前 #5 reasoning item/part=1/1，#6 reasoning expanded，D4 PASS |
| Reasoning summary | Runtime 有 summary events/parts | Contracts/Host 未投影，Host parser 丢弃 | 无 authority | semantic contract gap if requested | 本 Feature 不把 summary 冒充 raw；若未来纳入必须另做 source-first contract |
| Turn lifecycle | stable started/completed | v1 支持 `completed/interrupted/failed` | FEAT-132 支持 Turn terminal 并保留 partial | available with Desktop refinement | 继续以 `turn.completed` 为唯一 Turn terminal |
| Error | stable error 有 turn context | v1 支持 turn-correlated error | Rust live reducer 当前忽略，Timeline domain 可显示 notice | Desktop private projection gap | 按真实 Turn scope 呈现，不自动封口 |
| Warning | stable warning 只有 thread context | v1 schema 同样无 turnId | Rust live reducer忽略 | upstream attribution limit | 只显示 thread/session scope，不猜 active Turn |
| Sequence/dedupe/replay | upstream notification order是输入事实 | Host stream sequence 单调、event_id dedupe、at-least-once、默认 512 条 process-local replay | FEAT-132 reducer 有 sequence/dedupe/gap | available with boundary | replay 只用于进程内恢复，不当 durable history |
| Durable hydration | Runtime/Host 不承担产品历史 | Host thread/resume 只保留 ID/status；旧 Item 不可跨进程 replay | SQLCipher 有 local history，但 phase/plan/reasoning status 不完整 | DB expand + durable change | 只保证 Desktop 已观察并持久化事实的 live/hydration 等价 |
| Render batching | Runtime 可高频发布 | Host 可批量/顺序发布 | Rust 16 events / 50ms checkpoint；WebView 每 envelope 同步重算 Timeline | Desktop performance gap | 在不丢事件基础上展示节流，保持 selection/layout/a11y；滚动策略属于 FEAT-141 |

## 4. FEAT-131 CAP / Golden Scenario 责任

| ID | FEAT-131 状态 / provenance | 当前审计判定 | FEAT-134 D0 Gate |
|---|---|---|---|
| CAP-009 Assistant 流式文本 | `available / desktop-only`；当前聚合为单一 live Assistant | 基础可用，但真实多 Item identity 在 Desktop private wire 丢失 | pending：完成 itemId/block 聚合与 reconciliation |
| CAP-010 commentary vs final | `requires Host/Contracts projection` | Host 丢 `AgentMessage.phase`，且 provider 可能只给 null；Desktop 不可推断 | partial/pending：现行 canonical `phase=null`，准确保留 unknown；没有 commentary/final positive producer，fresh UI/D4 未验证 |
| CAP-011 用户可见 reasoning | FEAT-131 标为需 projection；现有 v2/v3 是后续 implementation extension | raw contract 存在但 canonical flag off、managed reasoning 为 none、compat 未锁、Desktop hydration 不完整 | pending：local high/raw 已授权；不得沿用 FEAT-133 metadata-only/unavailable 作为通过证据 |
| CAP-012 稳定 plan/step | `requires Host/Contracts projection` | stable `turn/plan/updated` 未进入任何受支持 projection，也没有 current canonical producer evidence | partial/pending：现行 canonical plan=`0/0`，absence 不得伪造；positive producer 与 fresh UI/D4 未验证 |
| CAP-013 experimental plan delta | `real-runtime-producer-unavailable` | 不是 FEAT-134 应补的稳定能力 | intentionally excluded；不得伪造 |
| CAP-014 Turn lifecycle | `available / desktop-only` | completed/interrupted/failed 基础存在 | pending：Item 与 Turn lifecycle 解耦、UI 状态对账 |
| CAP-015 warning/error context | `available / desktop-only`，UI 无独立详细 projection | error 可按 Turn；warning 只能 thread scope；Desktop live 忽略二者 | pending：按真实 scope 呈现，不扩写上游事实 |
| GS-001 普通流式完成 | historical synthetic PASS；current real-runtime PASS；旧 pre-runtime FAIL 保留 | 历史事实不能替代 FEAT-134 新链路 D4 | pending：新 vNext/Host/Desktop canonical evidence |
| GS-002 过程/reasoning | metadata-only；real-runtime NOT RUN | FEAT-133 临时缺失提示不满足 CAP-011 | pending：真实或被授权的 canonical evidence；否则保持 NOT RUN |

## 5. Contracts 当前事实

### 5.1 v1 stable projection

当前 `session-event` v1 支持：

- `thread.started`
- `turn.started`
- `item.started`
- `item.agent_message.delta`
- `item.completed`
- `turn.completed`
- `error`
- `warning`

Assistant `item.completed` 可带完整 text，足以作为 accumulated delta 的 authoritative snapshot。`turn.completed` 的 status 是 `completed | interrupted | failed`，仍是唯一 Turn terminal。

### 5.2 v2/v3 reasoning

v2 新增 raw reasoning：

- `item.reasoning_text.delta`
- `item.reasoning_text.finalized`
- status：`complete | incomplete | unavailable`
- reason：`reasoning_not_emitted | turn_interrupted | stream_gap | runtime_error | limit_exceeded | protocol_error | host_shutdown`

v3 保留 v2 reasoning 并增加 Artifact。该 schema 事实不等于 canonical CAP-011 已可用：Host raw flag 默认 `false`，managed provider reasoning effort/summary 为 `none`，compatibility manifest 也未列 reasoning notification。

### 5.3 Compatibility pin 缺口

`compatibility/agent-host-runtime-v1.json` 当前允许的 Runtime notifications 只有：

```text
error
item/agentMessage/delta
item/completed
item/started
skills/changed
thread/started
turn/completed
turn/started
warning
```

没有：

- AgentMessage phase 字段语义；
- `turn/plan/updated`；
- reasoning delta/finalized 对应 Runtime notification；
- reasoning summary projection。

## 6. Host 当前事实

- `api/contracts.lock` 固定 `CONTRACTS_VERSION=0.5.1` 与 `CONTRACTS_COMMIT=164b14f...`；Host snapshot 与 Contracts HEAD 经 hash/compare 一致。
- v1 mapper 可生成 delta、Item lifecycle、Turn lifecycle、error/warning。
- raw reasoning mapper、limit/sparse/terminal tests 已存在，但由 Host feature flag 控制且 canonical 默认关闭。
- Host session event stream 提供 sequence、event_id、at-least-once 与 512 条 process-local replay；进程重启后 stream 身份变化，旧 delta 不能作为 durable history 恢复。
- Runtime AgentMessage Item parser 没有把 phase 投到 Contracts；reasoning summary 被丢弃；`turn/plan/updated` 未进入 mapper。

## 7. Desktop 当前事实

- FEAT-132 domain event 模型已能按 `threadId + turnId + itemId + blockIndex` 追加 delta，处理 dedupe、sequence gap、started/completed/finalBlocks 和 notice。
- 生产 `chat-conversation-adapter` 把 live Assistant identity 固定成 `turnId:assistant:0`。
- private WebView event closed union 只有 `assistant_append`、`reasoning_append`、`turn_state`、`turn_terminal` 和 resync/context 类事件，没有 Assistant phase。
- Rust accumulator 只维护单 Assistant Item，并在 Turn terminal 时一次性封口；Item started/completed、error/warning 未完整进入 WebView projection。
- raw reasoning live append 和 SQLCipher 元数据基础存在，但 canonical stable 关闭 Host raw flag；无 reasoning Item 时 `reasoningStatus/reasonCode` 被 snapshot adapter 丢失。
- FEAT-133 Timeline 有最终回答、过程 disclosure、notice、安全 Content 和 a11y 基础，但不能修复上游缺失语义。

## 8. Negotiated vNext 最小语义

D0 不虚构 release tag；实现阶段应创建一个**不复用 v1/v2/v3**的显式协商版本。候选命名为 `AgentSessionEventV4`，最终名称必须与实际 Contracts source 和生成产物一致。

最小语义：

1. 在 AgentMessage `item.started` / `item.completed` lifecycle 中保留真实 `phase=commentary|final_answer|null`；delta 通过 itemId 关联 lifecycle，不复制或猜测 phase。
2. 增加 stable `turn.plan.updated` ordered snapshot，保留 explanation（存在时）与每个 step 的真实 status/order；上游没有 step ID 时不得发明跨 update 永久 identity。
3. 继承 v3 的 raw reasoning delta/finalized，明确锁定 Runtime compatibility 与 version negotiation；保持 complete/incomplete/unavailable reason model。
4. 保留 v1 Item/Turn lifecycle、error/warning、sequence/event_id 与 v3 Artifact，不破坏旧消费者。
5. 明确不支持 experimental `item/plan/delta`。

如果产品未来改为 provider-approved summary，而不是 ADR-0016 raw reasoning，必须先新增独立 contract 语义；不能把 Runtime summary、final 或 Host 模板混为 raw reasoning。

### 8.1 vNext 不能解除的 producer blockers

新增 contract 只能保留和约束已经产生的事件，不能制造 raw reasoning 正文。canonical stable 原先同时存在三项事实：Host raw projection flag 为 `false`、managed provider reasoning effort/summary 为 `none`、Desktop start-turn 不请求 reasoning effort。

ADR-0016 要求 reasoning-enabled Turn 至少有一个非空 raw reasoning Item；只有 unavailable/status 不能作为 reasoning PASS。Owner 已明确批准 `ai_behavior_change=model`，仅在 `demo_fast/local` 固定 reasoning effort=`high` 并开启 Host raw projection，不新增 UI、不影响 public/production。该决定解除范围 blocker，但不把授权本身当作 producer PASS。

CAP-010/012 还有同类证据门槛：Runtime schema 自身允许 AgentMessage phase 为 `null`，stable plan event 的存在也不证明 current provider 会发送。Contracts/Host 可以准确透传，却不能制造 `commentary/final_answer` 或 plan。Owner 初始授权 1 次、随后明确增加 2 次 canonical 重试，并在前三次用尽后额外批准 1 次；现已消费 `4/4`，均不是程序自动重试。前三次 content-free 结果为非空 raw reasoning、AgentMessage `phase=null`、plan update/step=`0/0`；第四次在 Provider 前 `turn_start_failed`，零事件且 cursor 未前进。unknown/no-plan 仍必须准确，不能支持 commentary/final 或 plan positive producer claim；corrective 已重建启动但未获准发送新 prompt，仍没有 fresh 正向 producer 证据。正文与哈希均未保存。

第四次失败后的 Desktop-only repair/recovery 不扩张跨仓 contract，且仅适用于 exact-local payload v2。该历史 candidate 的 834 TS / 313 Rust / 00:34 no-prompt 结果已被后续证据超越；当前 #5/#6、跨层 P2 修复、835 TS / 316 Rust 与 D4 结论见本文顶部 follow-up。

Owner 已将 dark theme、Reduce Motion 与精确 1180×760 设为 `WAIVED / NOT REQUIRED`；三项不是 PASS，也不再属于 D4 必需证据。

## 9. Source-first 实施顺序与 Gate

| Gate | 仓库 | 必须完成 | 下游开始条件 |
|---|---|---|---|
| CF-1 | `yijie-contracts` | vNext schema/compat/OpenAPI/protobuf/JSON schema/fixtures/tests；旧版本不变 | contract checks PASS，真实版本/ref/commit 可 pin |
| CF-2 | `yijie-agent-host` | 协商版本、phase/plan/reasoning mapper、terminal/replay 边界、精确 pin | Host full tests + snapshot/pin checks PASS |
| CF-3 | `yijie-desktop` private/domain | private wire、FEAT-132 authority、reconciliation、notice、DB expand/hydration | adapter/reducer/DB tests PASS，无第二 authority |
| CF-4 | `yijie-desktop` UI | 在 FEAT-133 Timeline 上组合层级、节流、a11y | component/integration/full tests PASS |
| D4 | 四仓 + `yijie` | canonical normal lifecycle、evidence、scoped diff、strict claims | 所有 Must AC PASS，未执行项如实记录 |

## 10. 不可由建分支解决的上游限制

- Warning 没有 turnId：只能 thread/session scope，不能按到达时间绑定 active Turn。
- experimental `item/plan/delta` 没有合法 producer：不能通过 Host fixture 冒充真实能力。
- Host process-local replay 不能恢复 Desktop 从未观察的跨进程事件：复杂 gap/resync 属于 FEAT-140/142。
- D0 时 canonical managed provider 尚无可用 raw reasoning；后续 content-free producer 事实已确认非空 raw reasoning，但 fresh、不间断 UI streaming 仍未证明，因此 CAP-011/D4 不能宣称 PASS。
- FEAT-139 才拥有 Stop action：FEAT-134 可以安全测试 interrupted 状态渲染，但不能用强杀或故障注入制造真实中断。

## 11. 最终判定

| 问题 | 判定 |
|---|---|
| 只创建 `yijie` + `yijie-desktop` 是否足够？ | 否，除非删除 commentary/final 与 stable plan Must |
| Contracts 分支是否必要？ | 是，phase 与 plan 是 semantic wire gap；reasoning compatibility 也需治理 |
| Host 分支是否必要？ | 是，必须保存/投影 lifecycle phase、stable plan、reasoning 并执行版本协商 |
| Runtime 分支/核心修改是否必要？ | 否，且硬性禁止；固定 stable schema 已提供必要上游事实 |
| 当前 contract impact | `semantic`；以 versioned vNext 避免 breaking |
| 当前 database/persistence impact | `expand` + `durable` |
| CAP-011 / D4 当前状态 | partial/pending；canonical content-free 确认非空 raw reasoning，但 fresh 最终重建 UI/hydration 与 D4 未验证 |
| CAP-010/012 当前状态 | partial/pending；本次 phase=null、plan=0/0，准确不推断；没有 positive producer，fresh UI/D4 未验证 |
| 是否可直接修改 Vue？ | 否；必须先 Contracts → Host → Desktop authority，最后 Timeline |

因此，Contracts/Host 条件分支的创建依据已经满足；本 D0 仍不修改任何实现文件。
