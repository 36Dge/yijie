# FEAT-132 — Desktop 对话领域模型与确定性状态机 Brief

> Profile：`demo_fast` · Exposure：`local` · Checkpoint：`D0` · Created：`2026-08-27`

## 1. 需求背景、目标与非目标

### 背景

Desktop 当前由 SQLite history snapshot、Rust `LiveTurnProjection`、WebView private IPC 与 Pinia
分别解释同一段对话。实时 assistant 正文仍以 Turn 级单缓冲区追加；Item identity、最终
`item.completed` 对账与确定性 hydrate 没有一个统一权威。继续按页面或能力分别扩展，会在
Command、Tool、Approval、Artifact 和恢复场景中产生串写、重复、状态冲突以及不可重放结果。

FEAT-131 已把 Epic 的参考策略改为
`codex-inspired-approximate-parity-v1-2026-08-27`：允许依据固定 Runtime、现有 Host 能力、易界 UI
规范和工程判断实现 Codex 风格近似交互，不再依赖人工截图或逐像素一致。

### 目标

- 建立与 Vue、Tauri 和传输协议解耦的 `Thread / Turn / Item / ContentBlock` 领域模型。
- 让 snapshot、live event 与 resync 进入同一个确定性 reducer；相同输入得到字节级等价状态。
- 以稳定 `turnId + itemId` 汇聚流式内容，去重事件，准确处理 sequence、终态和最终文本对账。
- 保持固定 `yijie-codex` Runtime 的普通文本 Chat 可用，为 FEAT-133–143 提供唯一 timeline 状态来源。
- 所有 Feature 仍服务同一 Epic 总目标：在 Vue 技术栈和固定 Runtime 不变的前提下，逐步实现符合
  易界 UI 规范的 Codex 风格近似端到端对话体验；FEAT-132 单独完成不代表 Epic 完成。

### 非目标

- 不修改、升级、重编译、替换或同步 `yijie-codex` Runtime、schema、binary 或 pin。
- 不修改模型、prompt、Provider、Agent 决策或 `experimentalApi`。
- 不新增 SQLite schema，不创建第二份正文 authority。
- 不在本 Feature 完成具体 Timeline 视觉、Command/Tool/Approval 卡片、滚动优化或复杂重连 UI。
- 不实现 Owner 已排除的语音、模型版本、模型推理强度、分享、置顶摘要切换、侧边面板、分支到新聊天，
  以及 GS-006 文件修改与 Diff。
- 不放宽 private IPC exact parser、不展示 raw Host/Runtime payload，也不伪造上游未投影能力。

## 2. 用户结果与完整主流程

目标用户是在易界 AI Desktop 中发起、查看、切换和恢复本地 Agent 对话的用户，以及后续对话 Feature
的实现者。完成后，用户看到的普通文本对话外观基本不变，但流式内容不串写、重复事件不重复显示、
错误不会提前宣布结束、最终快照不会让正文倒退或重复。

1. Desktop 绑定授权上下文并选择本地 session；selection authority 仍由现有路由和 Chat store 管理。
2. 采用 subscribe-before-resync，snapshot 经 adapter 规范化并 hydrate 到领域状态。
3. Rust 投影只输出 Desktop 需要的稳定、脱敏字段；TypeScript exact parser 拒绝 malformed wire。
4. 领域 adapter 把合法 wire 转为 normalized event；unknown semantic 只保留固定 code，不保留 raw payload。
5. reducer 按 `thread/session + turn + item` 写入 delta，按 event ID 去重并检查 stream sequence。
6. `item.completed` 对账累计内容；匹配则封口 Item，不匹配则保留已确认内容并记录脱敏 mismatch。
7. error/warning 作为非终态 notice；只有 `turn.completed` 能把 Turn 封口为 completed/interrupted/failed，并原子封口同 Turn 尚未完成的 Item。
8. terminal resync 以稳定 identity 原子 merge/replace；重选、重开和分页顺序变化不产生重复。
9. A→B 快速切换后，A 的迟到 live/history/artifact/draft 结果因 token 不匹配被丢弃。

## 3. 领域边界与业务规则

- Thread 状态：`not_loaded / ready / active / archived / unavailable`。
- Turn 状态：`queued / in_progress / waiting_approval / completed / interrupted / failed / recovery_required`。
- 当前 Item 语义：`user_message / assistant_message / reasoning / artifact / unknown`；Command、Tool、
  Approval 只允许保留未实现的 closed discriminator，不能伪造成已投影行为。执行进度属于 Turn lifecycle，
  error/warning 属于 Turn notice，不伪装成 Item。
- ContentBlock 当前包含安全 `text / code / attachment_reference / artifact_reference / unknown`；Artifact
  继续由 FEAT-128 原生 cache/SQLite 投影负责内容 authority，conversation reducer 只拥有 timeline
  identity/order/status。
- 一个 active Thread 同时最多一个 active regular Turn。
- Item identity 从 started 到 completed 不变；delta 只能落到对应 Item。
- `turn.completed` 是 Turn 唯一权威终态；它同时封口同 Turn 的 started/streaming Item，error/warning 不封口。
- 重复 event 必须幂等；sequence gap、非法迁移或 malformed wire 进入 `recovery_required`。
- unknown semantic 使用固定诊断 code 并 fail-soft；raw wire、路径、正文、secret 和 Runtime identity 不进入 UI。
- canonical serialization 按稳定 ID/ordinal 排序，不受 Map 插入顺序、分页到达顺序或 dedupe cache 影响。

## 4. 交互与 UI 状态

本 Feature 不新增页面、组件库、色值或视觉资产；使用现有 Vue、Pinia、Naive UI、`YjIcon` 和易界 token。

- Idle/Ready：历史已 hydrate 且没有 active Turn；composer 可用性仍由 readiness 与 permission 决定。
- Loading：history/resync 进行中时保留已确认安全内容，不闪成空白。
- Active：只在权威状态机中存在 active Turn 时显示执行中。
- Success：只有 `turn.completed` 后显示 completed/interrupted/failed，正文与 Item 不重复。
- Empty：没有 Turn/Item 时沿用新对话空状态，不创建假消息。
- Error：固定中文恢复提示与脱敏 code；不显示 raw payload。
- Retry：gap/非法迁移触发现有 resync/recovery 意图，不建立旁路状态。
- Cancel：沿用正常 interrupt，保留已确认内容；禁止用强杀或故障注入制造验收状态。

## 5. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 同一 snapshot/events 重放多次得到字节级等价 canonical state | reducer replay/permutation 测试 |
| AC-002 | 两个 Item 交错 delta 不串写，生产 adapter 不再依赖 Turn 级单缓冲 | TS reducer + Rust projection + Store 集成测试 |
| AC-003 | 重复 event 不重复正文、Item 或终态；cleanup 辅助事件也消费同一 eventId/sequence 游标 | domain/cleanup duplicate、连续性与 gap 测试 |
| AC-004 | error/warning 后仍可流式更新；仅 `turn.completed` 原子封口 Turn 与未完成 Item | 状态迁移、迟到 delta 与 Store 终态-resync-failure 测试 |
| AC-005 | completed final text 不重复、不倒退；不一致记录 `reconciliation_mismatch` | match/mismatch/resync/restart 测试 |
| AC-006 | unknown semantic 脱敏 fail-soft；malformed private wire fail closed | adapter/parser 负向测试与 canary |
| AC-007 | A→B 后 A 的 late history/live/artifact/draft/create/submit/cleanup 不能污染 B | selection/authorization/draft epoch 与 post-response race tests |
| AC-008 | fixed Runtime 普通文本 Turn 为 ready→in_progress→completed，重开不重复 | 两次独立授权累计 2/2；保留首次 queued 失败，以第二次 valid-project canonical stable real smoke 验证主流程与重开幂等 |

## 6. 工程事实、Contract First 与边界

- 受影响仓库：`yijie`（Feature Package）与 `yijie-desktop`（私有 domain/IPC/store/tests）。
- 真实入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`。
- 当前分支仍为 FEAT-131，两个工作区有 FEAT-131 完成结果和独立 FEAT-150 脏改动；本需求不
  reset、stash、覆盖或提交它们，也不擅自切换分支。
- `contract-impact=semantic`：公共 Host/Contracts 不变，但 Desktop 私有事件的 identity 与 Store
  合并/终态语义发生变化。
- 私有权威源顺序：领域规则 → Desktop JSON schema/Rust DTO → fixture/conformance → TypeScript exact
  parser/adapter → Pinia consumer。
- 仅 Rust WebView 投影丢失最小语义时，才 additive/versioned 扩展 Desktop private IPC；不修改
  Tauri capability/plugin/command，也不触碰 Host 或 Runtime。
- SQLite 仍是历史正文 authority；当前 private live projection 不携带 message `item_id`，因此消息使用
  `turnId + role + roleIndex` 合成稳定本地 identity，Reasoning 使用 `turnId + itemOrdinal`，Artifact
  使用既有 artifact ID。不会伪称数据库 `message_id` 已贯通 live wire；若上游未来投影真实 Item identity
  或非消息 Item 需要跨重启持久化，必须由后续 Feature source-first 另行治理。
- live `turn_state` 不携带持久化 Turn ordinal，adapter 明确投影为 `ordinal=null`；reducer 对已存在 Turn
  保留历史 ordinal，对 snapshot 尚未出现的新 Turn（含 item-first race）按同 Thread 当前最大 ordinal + 1
  确定性推导，避免第 2+ Turn 被误判为旧 Turn。

## 7. 授权与停止条件

- FEAT-132 共取得两份彼此独立的单条真实 prompt 授权，累计上限 2、已用 2/2。首次授权于 `2026-08-27T15:22:41+08:00` 消费并在 Host/Runtime/Provider 前停于 `queued`；Owner 随后明确增加第二份“最多 1 次、无敏感纯文本、禁止工具与文件读写、不自动重试”授权，valid-project fresh canonical Turn 已 completed。未授权任何更多 prompt。
- 破坏性操作、生产写入、故障注入、频繁/异常强杀均未授权且禁止。
- 若必须改变中央 Contracts、Host 或 Runtime 才能满足 Must AC，停止并登记 capability gap。
- 若 30 分钟没有新证据，回到 snapshot/IPC/store 单一链路，不扩建未来 UI。
- 若同一 blocker 达 90 分钟，保留最小完整文本/Reasoning 状态机，明确后续能力缺口。
- 完成结论为“FEAT-132 统一状态机局部完成，D4=PASS；整个 Epic 尚未完成”。
