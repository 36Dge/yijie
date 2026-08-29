# FEAT-135 Contract First 只读能力矩阵

> Audited: `2026-08-29` · Result: `contract-impact=none` · Mode: source-first read-only audit

> D4 follow-up: Desktop 实现已固化为 `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51`；focused 141/141、full 872/872、lint/typecheck/build/diff PASS。canonical final-source 以 Runtime 0.144.6、`experimental_api=false` ready，1/1 content-free Turn completed 并正常 Cmd+Q 清理。Contracts `3832a6c5...`、Host `b9358f06...`、Runtime `0ce5902e...` 保持 clean 不变，证明原 `contract-impact=none` 结论成立。AC-001 人工视觉与 reduced-motion 为 Owner `WAIVED / NOT REQUIRED`。

## 1. 审计问题与结论

问题：实现 Codex 风格 Composer、新 Turn 提交、防重复、失败保留、target-scoped 草稿与焦点恢复，是否必须改变跨进程、跨仓、跨版本、durable 或 replay 契约？

结论：**当前不需要，`contract-impact=none`。**

现有链路已经提供：

1. Contracts/Host 的 canonical ordered blocks、operation ID 与 exact replay idempotency；
2. Desktop native 的权限校验、原子 SQLCipher message/Turn/outbox 写入与回显 operation ID；
3. FEAT-127 的 attachment target/ordered blocks/durable-before-Host authority；
4. FEAT-132/134 的 queued、active 与 terminal 展示 authority。

缺口位于 Desktop 进程内组合：store 的 reply submit 返回 `Promise<void>` 且可静默 no-op，页面无法判定 local durable acceptance；纯文本草稿是 page-global ref；Composer 缺 auto-grow/focus API。它们可以通过内部 application result、WebView target map 和 Vue 组件能力补齐，无需新增 wire 或数据库语义。

## 2. Source-first identity

| Authority | Branch | Immutable HEAD | D0 状态 |
|---|---|---|---|
| `yijie-contracts` | `feat/feat-134-desktop-streaming-progress-final-response` | `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` | clean / read-only / no FEAT-135 branch |
| `yijie-agent-host` | `feat/feat-134-desktop-streaming-progress-final-response` | `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` | clean / read-only / no FEAT-135 branch |
| `yijie-desktop` | `feat/feat-135-desktop-codex-style-composer` | baseline `7b9daa791635250d0628c9e9f553cf40fab5ad96`；final `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` | implementation complete / D4 PASS / clean / unpushed |
| `yijie-codex` Runtime | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | clean / fixed / no branch / no build |

Audit order：Contracts → Host snapshot/mapper → Desktop native transaction/private IPC → store/application authority → page/composer → FEAT-127/132/134 integration。

## 3. 能力矩阵

| 能力/语义 | 权威源与只读事实 | 当前覆盖 | FEAT-135 缺口 | 后续允许动作 | Contract 结论 |
|---|---|---|---|---|---|
| canonical ordered blocks | Contracts `/v2/.../turns` 与 Desktop `turnContentBlocks()`；文本先、附件后 | 文本、attachment-only、组合输入均可表达 | UI 必须复用同一 enabled rule | 只增加测试与内部组合 | none |
| operation idempotency | Contracts 说明同一 Agent session + canonical blocks + reasoning effort 的 exact replay 返回原 accepted Turn，不再调用 Runtime；store `pendingSubmission` 按 submission key 重用 operation ID | 丢响应重试基础已存在 | 页面连续按键/点击还需统一 in-flight gate | 保留现有 key/id，增加页面防重复测试 | none |
| local durable acceptance | `chat_create_session_v1/v2`、`chat_submit_turn_v1/v2` 调用 `create_local_session*`/`enqueue_turn*`，完成本地队列写入后才启动 coordinator，并返回 session/turn/operation ID | native response 可证明 local transaction 已接受/排队 | store reply API 不向页面返回可判定结果 | 在 Desktop 内映射显式 submission result | none |
| Host/Runtime acceptance | Contracts HTTP 202 明确表示 Runtime accepted；Desktop coordinator 在 local enqueue 后异步调用 Host | Timeline/control-plane 已承载后续进展 | 容易与 Composer accepted 混称 | 文档和类型名区分 `local_durable_accepted` 与后续状态 | none |
| reply no-op/failure | `chat.store.ts::submitTurn()` 在权限、readiness、blocks 或 stale authority 不满足时直接 `return`；异常会抛出 | fail closed 本身正确 | `ChatPage.submit()` await 后无条件清空 `prompt` | 返回 sealed internal outcome；只有 matching accepted 才清理 | none |
| new-session result | `createSession()` 返回 `sessionId|null` 并验证 operation ID、epoch、target | 页面已能在 null 时保留文本 | result 语义与 reply 不统一，route race 需要明确 | 统一内部 result，但不改变 native DTO | none |
| attachment draft/transaction | FEAT-127 store/native authority：target-scoped draft、状态/容量校验、ordered blocks、同 operation retry、durable 后 drop refs | 完整且必须保护 | 文本 draft 不是 target-scoped | 文本 target map 与附件 target 对齐，不触碰附件 persistence | none |
| text draft | `ChatPage.vue` 只有一个 `prompt = ref("")` | 单页面可编辑 | 切换 new/session 可能串草稿；无 matching-target clear | WebView 内 `new`/`sessionId` map，route/epoch-safe | none；不做 durable persistence |
| Enter/Shift+Enter/IME | `ChatComposer.vue` 已使用 `composing`、`event.isComposing`、Shift 判定与共享 `submit()` | 基本键盘语义已覆盖 | 连续动作、programmatic submit 和所有 authority deny 的统一性待验证 | 收敛单一 derived enabled/submit intent | none |
| auto-grow/max scroll | textarea 当前 `resize:none` 且固定 `min-height`，没有 element ref | 未覆盖 | 长输入体验和 200% zoom 可用性不足 | 无依赖的 scrollHeight 同步、CSS max-height/overflow | none |
| focus/selection | Composer 没有 textarea ref 或 expose focus；页面成功后仅滚动/路由 | 未覆盖 | 成功/失败后焦点不确定 | 组件 expose 稳定 focus method；nextTick 后按结果恢复 | none |
| validation/readiness/permission | `sendDisabled`、store `canSend`、allowed action、project revalidation、input byte limit 与 attachment状态 | 多层 fail closed 已存在 | UI validating/submitting 语义未完全分开 | 只组合现有 authority，不在 Vue 伪造 permission | none |
| queued/active/terminal UI | FEAT-132 ConversationState、FEAT-134 v4 projection 与 FEAT-133 Timeline | 提交后状态 authority 已存在 | Composer 不应等待终态才清理，也不应在 terminal failure 恢复正文 | local accepted 后交给 Timeline | none |
| active Turn action | 当前 Composer 在 streaming 时显示既有 Stop predecessor | 既有最小行为 | FEAT-139 还需正式 steer/stop semantics | 只保留 action slot，不新增命令或状态机 | none |
| Runtime/model behavior | fixed Runtime、`experimentalApi=false`；FEAT-134 local model/high/raw 授权是上一 Feature 专属 | FEAT-135 无需 AI 行为变化 | 无 | 不修改、不启动、不调用 | none |

## 4. 关键语义决策

### 4.1 Composer accepted 的精确定义

`local_durable_accepted` 同时满足：

1. native command 成功返回；
2. response operation ID 与当前 pending operation ID 相同；
3. 返回时 context、selection epoch、draft epoch 与 draft target 仍属于该提交；
4. native transaction 已创建或重放同一 durable session/Turn/user Item/outbox 结果。

满足后，页面可以清空且只清空匹配 target 的 WebView 草稿，并显示 durable queued 用户 Item。

它**不表示** Host HTTP 202、Runtime start、Agent active 或 final completion。后四者继续由现有异步 authority 表达。

### 4.2 失败与草稿恢复

| 阶段 | 示例 | 草稿行为 | operation 行为 |
|---|---|---|---|
| pre-dispatch | permission/readiness/invalid project/invalid blocks | 保留 | 不创建新意图 |
| dispatched but not durably confirmed | native reject/throw/mismatched operation/uncertain response | 保留；不得跨 target 清理 | 相同 canonical input 复用 pending operation ID |
| local durable accepted | native matching response | 清空匹配 target；其他 target 不变 | pending intent 完成，显示唯一 queued Item |
| post-durable Host/Runtime failed/interrupted | Timeline terminal state | 不恢复为 Composer 草稿，避免重复提交 | 后续恢复属于 FEAT-139/140/142 |

### 4.3 草稿持久化边界

FEAT-135 采用当前 WebView 生命周期内的 target-scoped text map：

- key：`new` 或稳定 `sessionId`；
- value：用户未提交的原始 textarea 字符串；
- 只由页面组合层管理，附件继续使用 FEAT-127 native authority；
- 不写 SQLCipher、文件、localStorage 或 Host；
- 应用重启恢复明确 out of scope。

这个取舍消除 session mixing，又保持 `persistence_change=none`。

## 5. 已发现的实现风险与 D1 测试入口

| 风险 | 当前证据 | 必须先红后绿的测试 |
|---|---|---|
| reply no-op 丢草稿 | `ChatPage.submit()` 在 `await chatStore.submitTurn(input)` 后直接 `prompt.value = ""` | store blocked/stale 返回时 draft 不变 |
| 双入口重复意图 | 页面仅有 `submitting` ref，组件与 store 各有 gate | 同 tick Enter+click / repeated Enter 最多一个 native call/operation |
| target race 误清理 | 文本 prompt 全局，附件 target-scoped | submit 期间切 session/new，不清理新 target 或旧 target 错误内容 |
| operation mismatch | store 已 throw protocol error | 页面保留 draft/attachment并显示安全错误 |
| auto-grow 抢焦点/选择 | textarea 无 ref，需 DOM height sync | value、selectionStart/End、focus 在 grow/accepted/error 后符合预期 |
| attachment remove 重复 handler | `ChatComposer.vue` baseline 存在重复 `@click` | 先确认实际 emit 次数；只有证明属于本 Feature 才最小修复 |
| active Turn scope creep | current streaming 分支包含 Stop | snapshot 确认只保留 predecessor/slot，无新 control IPC |

## 6. Negative sentinels

后续 scoped diff 必须证明以下均未改变：

- `yijie-contracts` 与 Host snapshot/lock/mapper；
- `yijie-codex` branch/HEAD/source/schema/manifest/binary/build；
- Desktop private IPC DTO/command list、database schema/migration、Tauri capability；
- FEAT-127 attachment identity/persistence/order、FEAT-128 Artifact authority、FEAT-132 ConversationState wire/domain、FEAT-134 streaming semantics；
- dependencies 与 lockfile；
- public/production、model/Provider/prompt/reasoning 配置；
- Owner 排除的八项能力，特别是 CAP-022 / GS-006 File Modification & Diff。

## 7. 重分类停止条件

出现以下任一事实，`contract-impact=none` 立即失效，停止实现并请求 Owner 授权：

1. native response 不能可靠证明 local durable acceptance，必须新增/改 private IPC 字段；
2. target-scoped text draft 必须跨重启持久化，需要 SQLCipher schema/migration 或 replay；
3. operation ID/canonical key/idempotency 行为必须跨仓改变；
4. 权限/readiness 需要新 Host/Contracts 字段；
5. action slot 必须承载新 Stop/Steer/Retry 命令；
6. 需要 Runtime、`experimentalApi`、model/Provider/prompt/reasoning 或依赖变化。

届时必须按 Contracts/Host/native authority 的 source-first 顺序重新建 D0；不得在 Vue、store 或文档中伪造通过。

## 8. D0 审计与 D4 对账结论

- Contract impact：`none`
- 受影响仓库：`yijie`、`yijie-desktop`
- Contracts/Host/Runtime FEAT-135 分支：不需要，且本轮禁止创建
- D0 当时实现代码、prompt 与提交均为 0；该历史事实保留。
- D4 最终 Desktop：`fc52ef33cdf040d9b6e8d71bd7498811c5c38c51`，clean、未 push。
- D4 Provider：Owner 独立确认后 1/1，无工具或任务文件读写；终态 completed，正文不落证据。
- D4 source-first 对账：Contracts/Host/Runtime、private IPC、database、依赖与保护 authority 均未改变；`contract-impact=none` 保持有效。
