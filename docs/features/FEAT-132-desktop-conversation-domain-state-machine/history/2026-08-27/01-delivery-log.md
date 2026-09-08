# FEAT-132 整体实现与调试记录

## 1. 整体实现方案

- 参考策略：`codex-inspired-approximate-parity-v1-2026-08-27`，不采集人工 Codex 证据。
- 推荐路径：冻结 normalized domain 与状态迁移 → Desktop 私有 schema/DTO（仅必要增量）→ exact parser/adapter
  → Pinia 唯一 reducer consumer → history/live/resync/race 回归 → canonical local 验证。
- 硬边界：`yijie-codex` Runtime、中央 `yijie-contracts` 和 `yijie-agent-host` 均只读；SQLite schema 不迁移。
- 数据边界：只使用合成无敏感 fixtures；日志、unknown 与 mismatch 不保留 raw wire、用户正文、路径或 secret。

## 2. 开始状态与调查证据

| 时间 | 范围 | 事实/结果 |
|---|---|---|
| 2026-08-27 | Git | `yijie`=`feat/feat-131-desktop-codex-parity-baseline@16e67c2`；`yijie-desktop`=`feat/feat-131-desktop-codex-parity-baseline@00c8227`；均有既有未提交改动 |
| 2026-08-27 | 隔离 | FEAT-131 package/replay 与 FEAT-150 Store 页面改动均不属于 FEAT-132；不 reset/stash/覆盖/提交 |
| 2026-08-27 | Runtime | 固定 `yijie-codex` 0.144.6/`0ce5902e…`/stable schema，禁止修改、升级、重编译或启用 experimental API |
| 2026-08-27 | WebView | `ChatProjectionEvent.assistant_append` 只有 Turn 级 text；Pinia 使用全局 `liveAssistantText`；unknown kind 在 exact parser fail closed |
| 2026-08-27 | Rust | Host event 已含 turn/item/event/stream/sequence，但 `LiveTurnProjection`/Tauri event 丢失 assistant item identity 与多数 lifecycle；reasoning 仍保留 Rust item ID |
| 2026-08-27 | Persistence | 当前 SQLite 已有 message ID、reasoning item ID、附件 blocks、artifact ID/ordinal/status；FEAT-132 无需 migration |
| 2026-08-27 | Compatibility | FEAT-127 draft 不进入 conversation reducer；FEAT-128 artifact channel 继续 invalidation-only；FEAT-130 route/selection 继续是选择权威 |

## 3. 修改前基线

| Repository | Command | Result |
|---|---|---|
| yijie-desktop | `pnpm exec vitest run src/domain/chat-ipc.test.ts src/stores/chat.store.test.ts src/pages/chat/ChatPage.test.ts tests/feat-131/chat-event-replay-harness.test.ts scripts/check-feat131-replay-boundary.test.mjs` | PASS：5 files / 111 tests |
| yijie-desktop | `pnpm exec vue-tsc --noEmit` | PASS |
| yijie + yijie-desktop | `git diff --check` | PASS |

## 4. 实际改动

| Repository | 文件/边界 | 实现结果 |
|---|---|---|
| yijie-desktop | `src/domain/conversation-state.ts` | 新增纯 TypeScript immutable reducer、Thread/Turn/Item/ContentBlock、canonical serializer、FIFO eventId 去重、共享 stream sequence、单 active Turn、缺失 ordinal 的 max+1 推导、Turn 终态原子封口 Item、终态对账与有界脱敏 diagnostic/notice |
| yijie-desktop | `src/api/chat-conversation-adapter.ts` | 将 V1/V2/V3 history 与既有 private live projection 适配为稳定本地 Item identity；`turn_state` 显式使用 nullable ordinal，cleanup 映射为只消费游标的 auxiliary event；不扩展 Rust/IPC wire |
| yijie-desktop | `src/api/chat-client.ts` | malformed event 继续 exact parser fail-closed，仅提取三个合法 UUID routing 字段用于丢弃旧会话错误，不泄露 raw body |
| yijie-desktop | `src/stores/chat.store.ts` | `conversationState` 成为对话语义 authority；旧 history/live/sidebar refs 仅作 lifecycle 兼容投影；create 前重验项目；create/submit/cleanup 的 pre/post-await authority、selection、draft 与 subscription guard 隔离迟到结果；terminal resync 统一 reconciliation |
| yijie-desktop | `src/pages/chat/ChatPage.vue` | assistant live region 使用动态 streaming/ready aria-label，仅在领域 Turn 实际 streaming 时显示 caret；未新增页面或排除功能 |
| yijie-desktop | focused/integration tests | 新增 domain/adapter/store/parser 测试与 `tests/feat-132/conversation-projection-replay.test.ts`；复用 FEAT-131 GS-001/012/013 回归 |
| yijie | FEAT-132 package/evidence | 记录 D0、实现、验证、Runtime freeze、独立审查、首次 queued 失败历史、最终代码 canonical startup 与第二次 valid-project AC-008 成功证据 |

没有修改 `src-tauri`、SQLite migration、`yijie-contracts`、`yijie-agent-host` 或 `yijie-codex`。

## 5. 调试循环

| 时间 | 现象 | 根因/证据 | 修复/决策 | 结果 |
|---|---|---|---|---|
| 2026-08-27 | 旧 Desktop Epic 文档仍要求冻结基准完全一致，并包含 file change | 与 FEAT-131 owner policy 和 GS-006 exclusion 冲突 | 更新为 Codex-inspired approximation，移除 FileChange/Diff，并保留 reasoning summary/Artifact 边界 | D0 policy aligned |
| 2026-08-27 | 合成 TS reducer 可以测试多 Item，但生产 Rust→Tauri→TS 丢 assistant item identity | Rust `TurnEventReducer` 有 Host item ID；`LiveTurnProjection` 和 event envelope 未贯通 | 先冻结领域 identity；再决定最小 additive/versioned Desktop 私有投影，不修改 Host/Contracts/Runtime | 后续能力审计判定无需 wire 扩展 |
| 2026-08-27 | 能力审计确认普通文本 live projection 没有 assistant itemId | FEAT-132 只需每 Turn 单 assistant Item 与按 ordinal 的 Reasoning Item；公共 Host/Contracts 扩展会越界且无必要 | 使用 `turnId:assistant:0`、`turnId:reasoning:itemOrdinal` 与 artifact ID 的确定性本地 identity | 无 Rust/schema/Runtime 修改 |
| 2026-08-27 | 同 eventId 携带不同 sequence 会绕过旧 Store 去重 | 旧逻辑先按 sequence 分支，去重 ledger 不是领域 authority | reducer 先按 FIFO 有界 eventId ledger 去重，再检查 per-stream sequence | duplicate 不追加且不触发伪 gap |
| 2026-08-27 | malformed A event 在切换 B 后可能触发 B resync | parser failure 回调没有安全 routing scope | chat-client 仅 best-effort 提取合法 context/session/subscription UUID；Store 丢弃旧 scope，未知 scope 对当前会话 fail-closed | A/B race tests PASS |
| 2026-08-27 | 独立审查发现 terminal lifecycle regression、双 active Turn 与字典序 eviction | 初版只对账 Item content，active conflict 检查过晚，eventId 账本按 lexical 排序 | 增加 lifecycle equal/divergence/missing 对账、所有激活事件 preflight、FIFO eviction、snapshot invariant 与有界 notice/diagnostic | 中间问题修复，继续执行 final-delta 复核 |
| 2026-08-27 | canonical final readiness 需要当前代码 fresh 证据 | 调试期截图和后续代码修改不能支持最终结论 | 最后一次代码修改后重新执行 `pnpm tauri:demo-fast:stable`；核对空输入/disabled send、`/readyz`、`/v1/status`，Cmd-Q 正常退出并检查进程/端口 | startup PASS；未键入或发送 prompt；见 `evidence/canonical-current-code-startup-2026-08-27.md` |
| 2026-08-27 | AC-008 获得一次性真实 prompt 授权 | Owner 限定最多一次、无敏感纯文本、禁止工具/文件、失败不重试 | fresh canonical 启动并再次核对 Runtime 0.144.6、MiniMax-M3 与 `experimental_api=false` | readiness PASS |
| 2026-08-27 | 首个 AX send-button click 后界面完全未变 | 输入未清空、仍在 `/chat`、没有 session/user message，证明应用 submit 未触发 | 聚焦 textarea 后使用组件明确支持的 Enter，只执行一次应用 submit | 创建唯一 session `01a0421d-10dc-7972-a79e-72f29469cb46` 与唯一 user message |
| 2026-08-27 | 唯一 Turn 持续显示“状态已更新”且没有 assistant | 历史快照 latest Turn 为 `queued`；没有工具/审批 UI，Runtime logs 未出现 Turn target；原 FEAT-131 临时项目已被清理 | 重建同一路径空目录，通过应用 picker 刷新只读 bookmark，重选并正常 Cmd-Q/reopen，同一 operation 继续观察；不再次 submit | 仍为 queued，零 assistant；AC-008/real smoke FAIL |
| 2026-08-27 | 失败态收口 | Owner 要求失败不重试；不得用第二条 prompt 或合成 fixture 覆盖真实结果 | 保存 1162×768 失败态截图；应用自身 Cmd-Q 退出并核对进程/端口 | App/Host/Runtime 均退出，18081/1420 释放；D4 保持失败 |
| 2026-08-27 | `queued` 根因只读定位 | Public Task=`bound`；session 无 Host/Runtime ID；`create_session` outbox=`failed`、attempt=16；Runtime thread=0 | 对照 coordinator、bookmark 和 outbox claim 源码；不写数据库、不重放 operation | 确认失效 bookmark 在 Host 前反复耗尽 lease；picker 只刷新 bookmark，不能恢复 failed outbox；排除 Runtime/Provider |
| 2026-08-27 | 独立复核发现第 2+ Turn live ordinal 回归 | history adapter 给 Turn 正确 ordinal，但 live `turn_state` 没有持久化 ordinal | adapter 投影 `ordinal=null`；reducer 保留既有 ordinal，新 Turn（含 item-first）按同 Thread max+1 推导 | domain/adapter/store/replay 回归 PASS |
| 2026-08-27 | 新 create 可能再次使用失效项目 bookmark | 旧失败发生在 Host 前；picker 更新不能恢复已 failed outbox | 每次 create 前调用既有 project revalidation；invalid project 返回稳定 `chat_project_invalid`，保留 draft 与幂等 operation | 不改 Rust/outbox；新会话 fail-closed preflight 回归 PASS |
| 2026-08-27 | cleanup 绕过领域 sequence，且 A 的异步 cleanup 结果可迟到污染 B | cleanup 分支提前 return；首个 status await 未绑定 selection/subscription | cleanup 映射 auxiliary event 共享 eventId/sequence；status refresh 绑定 context/session/subscription/selection epoch | N→N+1、duplicate、gap 与 A→B late cleanup 回归 PASS |
| 2026-08-27 | create/submit 返回后的旧结果和“live 先于 invoke response”竞态 | 初版只在 dispatch 前校验；post-response 误依赖瞬时 `canSend` | post-response/reload 校验 authority/context/selection/draft；发送能力只在 dispatch 前检查 | stale response、rebind、switch 与 live-first 回归 PASS |
| 2026-08-27 | terminal resync 失败时 Turn 已终态但 Item 仍 streaming | 生产 wire 没有独立 item.completed | `turn.completed` 原子封口同 Turn 未完成 Item，保留 partial content/reconciliation；迟到 delta fail-closed | domain/store terminal-resync-failure 回归 PASS |
| 2026-08-27 | 最终 scoped/boundary/delta 复核 | 逐项回查 ordinal、cleanup、post-response、terminal sealing、Owner exclusions 与 Runtime freeze | 两名独立 agent 只读复核，修复所有发现后再次检查 focused/typecheck/eslint/diff | 最终未发现剩余 P0–P2 |
| 2026-08-27 | Owner 增加第二份且最终的单条真实 prompt 授权 | 首次 1/1 已失败并按约束未重试；新授权明确限定 canonical、无敏感纯文本、禁工具/文件、不自动重试 | fresh canonical 使用已验证有效项目；只点击一次发送任务 | 创建 session `01a04297-890b-7aa0-99db-b431829f67f1`，直接观察 completed 与严格单行回复 |
| 2026-08-27 | 最终 AC-008 历史幂等与退出 | 新 session 历史恰好 1 user + 1 assistant；没有工具/审批/文件/Diff | 切换到旧任务后重开新 session；再通过应用自身 Quit 正常退出 | 同一 session、消息和终态无重复；launcher exit 0，App/Host/Runtime 退出，18081/1420 释放；AC-008/real_smoke PASS |
| 2026-08-27 | AX 采样未单独捕获瞬时 `in_progress` | 响应约 1.45 秒完成，首个提交后 AX 帧已是 completed | 正常退出后只读核对 canonical 专属 Runtime state/rollout，并对照固定 Runtime/Host lifecycle 映射源码 | 唯一 Runtime thread 的固定 prompt/reply 匹配；同一 Turn 持久化 `task_started`/TurnStarted 与 `task_complete`，Host 强制 started=`in_progress`；真实 lifecycle 补证 PASS |

## 6. 外部授权与调用

| 类型 | 上限 | 已用 | 结果 |
|---|---:|---:|---|
| FEAT-132 受限真实 prompt submit | 2 | 2 | 两份独立授权各执行一次；首次 queued 历史失败，第二次 valid-project canonical PASS；两次均未自动重试 |
| 破坏性操作/生产写入 | 0 | 0 | 禁止且未执行 |

2026-08-27T15:22:41+08:00，Owner 新授权 FEAT-132 从 canonical
`pnpm tauri:demo-fast:stable` 入口最多发送 1 次无敏感纯文本 prompt；禁止工具调用和文件读写，失败不自动重试。该授权不改变破坏性操作与生产写入的禁止状态。

Owner 后续“已解锁”仅用于继续桌面只读操作，不增加 prompt 次数。首次授权失败之后，Owner 在当前会话又明确授权 FEAT-132 在同一 canonical 入口**再发送最多 1 次**无敏感纯文本 prompt；禁止工具调用和文件读写，不自动重试。第二份授权已消费 1/1；累计 2/2，未授权更多 prompt。

## 7. 已知限制

- Host/Contracts 当前没有完整 command/tool/approval 投影；本 Feature 只定义安全领域占位，不伪造生产行为。
- Owner 排除的八项能力（包含 GS-006 File modification & Diff）不进入模型实现、fixture 或 UI。
- 当前工作区同时承载 FEAT-131 未提交结果与 FEAT-150 独立改动；已完成 scoped diff 与完整 status 审查，后续仍不得 reset/stash/覆盖/提交它们。
- 首次独立授权的真实 submit 停在 `queued`，该失败和根因继续作为历史证据保留，未被重放或改写；第二次明确独立授权的 valid-project fresh session 已 completed，历史 1+1 且重开无重复。
- 只读证据已把 AC-008 失败定位到 Desktop 的失效 bookmark 与 exhausted `create_session` outbox；目标 operation 没有到达 Host session、Runtime 或 Provider。现有 failed 行缺少 failure provenance，不进行猜测式自动恢复。
- 第二次真实 Turn 在 1.5 秒 AX 采样前完成，瞬时 `in_progress` 未被单帧采样；canonical Runtime rollout 的同一 TurnStarted/TurnComplete 持久化记录和固定 Host in_progress 强校验已补足真实 lifecycle，终态 completed、1+1 历史与重开幂等均已记录。
- 当前实现、自动化、Runtime freeze、canonical real smoke 与独立复核已收敛；D4=PASS，FEAT-132 可用，但整个 Epic 尚未完成。
