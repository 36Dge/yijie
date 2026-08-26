# FEAT-131 — Codex Desktop 对话黄金场景

> 作用：冻结后续 FEAT-132–143 共用的行为场景，不实现生产交互。
>
> Codex Desktop reference：尚未取得与冻结 version/build 匹配的逐场景媒体证据；对应字段统一为 `reference-unobserved`。
>
> 结论：D0 候选场景 ID 已固定；版本专属证据与 D4 未完成前，不宣称场景基线已冻结。Epic 尚未完成。

## 1. 使用规则

每个场景同时区分三类 provenance：

- `reference-observation`：与冻结 Codex Desktop version/build 对应、已经脱敏且可核对的截图、录屏或操作记录；
- `real-runtime`：通过 Yijie 正常入口连接固定 Runtime 真实产生；
- `synthetic`：只用于 reducer/UI 的确定性回放，不能证明真实 Runtime/Host 支持。

机器目录中的 `variants` 是场景要求全集；`replayedVariants` 只列已经由该 fixture 实际覆盖的子集，并必须与 fixture 的 `coveredVariants` 精确一致。未列入的 variant 保持 metadata-only/NOT RUN，不能由场景级 `assetKind=replay` 推断为已通过。

当前没有被证据索引登记为 `reference-observation` 的版本专属交互一律保持 `reference-unobserved`。下面的“Yijie 候选状态顺序”来自固定 Runtime schema、Host/Contracts 与 Desktop 代码事实，是后续 Feature 的规范化目标，不是对 Codex Desktop 当前版本的记忆性复述。

安全验证约束：不得通过频繁强杀、故障注入式强杀、替换 binary、破坏权限、恶意 fixture 或攻击载荷制造失败。断线、gap、未知事件和终态冲突优先使用无攻击性的 synthetic replay；真实进程验证只允许应用自身正常启动、停止、退出和清理流程。

## 2. 场景总表

| Scenario | Purpose | Primary classification | Owner | Codex reference | Current Yijie evidence |
|---|---|---|---|---|---|
| GS-001 | 普通问题的流式回答与最终完成 | `available` | FEAT-134、FEAT-135 | `reference-unobserved` | `synthetic: PASS`；current canonical `real-runtime: NOT RUN`；predecessor `pre-runtime: FAIL` |
| GS-002 | 多段过程更新与用户可见推理信息 | `requires Host/Contracts projection` | FEAT-134 | `reference-unobserved` | metadata only；`real-runtime: NOT RUN` |
| GS-003 | Command 执行成功和失败 | `requires Host/Contracts projection` | FEAT-136 | `reference-unobserved` | metadata only；projection unavailable |
| GS-004 | Tool 调用成功和失败 | `requires Host/Contracts projection` | FEAT-136 | `reference-unobserved` | metadata only；projection unavailable |
| GS-005 | 命令审批允许、拒绝和过期 | `requires Host/Contracts projection` | FEAT-137 | `reference-unobserved` | `BLOCKED`: Owner security decision |
| GS-006 | 文件修改与 Diff | `requires Host/Contracts projection` | FEAT-138 | `reference-unobserved` | `BLOCKED`: Owner security decision |
| GS-007 | 执行中补充指令 | `requires Host/Contracts projection` | FEAT-139 | `reference-unobserved` | metadata only；projection unavailable |
| GS-008 | 用户停止 Turn | `available` | FEAT-139 | `reference-unobserved` | `real-runtime: NOT RUN` |
| GS-009 | 失败后重试或继续 | `available` | FEAT-139 | `reference-unobserved` | metadata only；`real-runtime: NOT RUN` |
| GS-010 | 切换并恢复历史会话 | `available` | FEAT-140 | `reference-unobserved` | `real-runtime: NOT RUN` |
| GS-011 | 用户上滚后的新消息与回到底部 | `available` | FEAT-141 | `reference-unobserved` | `synthetic: NOT RUN` |
| GS-012 | SSE 或 Host 断线和恢复 | `requires Host/Contracts projection` | FEAT-142 | `reference-unobserved` | safe `synthetic: PASS`；real lifecycle `NOT RUN` |
| GS-013 | 未知 Item、缺失 delta 或无最终回答 | `requires Host/Contracts projection` | FEAT-142 | `reference-unobserved` | sequence-gap `synthetic: PASS`；其余 variants metadata only |

## 3. 详细场景

### GS-001 — 普通问题的流式回答与最终完成

- 前置条件：Host/Runtime ready；已有 idle session 或可以创建新 session；安全纯文本输入；没有 active Turn。
- 用户操作：在 Composer 输入普通问题并发送。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`idle → validating → submitting → accepted → turn.in_progress → agentMessage.started → agentMessage.delta* → agentMessage.completed → turn.completed(completed) → ready`。
- 可用动作：提交前可编辑；active 后可 Stop；完成后可选择/复制回答并开始新 Turn。
- 最终结果：只有一个 user Item、一个 Turn 和一份权威 final；完成后无 streaming 光标，历史 hydration 不重复内容。
- Provenance：Codex 为 `reference-unobserved`；streaming/completed raw-event fixture 已以 `synthetic: PASS` 经过真实 Desktop parser/store。当前隔离 canonical stable startup 已 PASS，但授权额度已由 predecessor entry 的一次 UI submission 使用，故 current canonical `real-runtime: NOT RUN`；predecessor submission 没有产生 Runtime thread/turn/delta/terminal 证据，只能记为 `pre-runtime: FAIL`。不得用 synthetic 或 predecessor 结果代替当前真实 happy path。
- Owner：FEAT-134、FEAT-135（前者负责流式 Item/终态展示，后者负责输入提交与 Composer 交互）。

### GS-002 — 多段过程更新与用户可见推理信息

- 前置条件：固定 Runtime/Provider 实际发出多个 Assistant/reasoning Item；若未发出，必须记录 unavailable，不能补造。
- 用户操作：提交一个确实需要多步处理、但不触发危险写操作的任务。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`turn.in_progress → commentary/progress Item* ↔ reasoning-visible Item* → final agentMessage → item.completed* → turn.completed`；具体交错由真实 itemId/sequence 决定。
- 可用动作：过程/reasoning 可展开折叠；active 时可 Stop；隐藏 reasoning 不提供执行、批准或信任入口。
- 最终结果：progress/reasoning 保持次级层级，final 是唯一主结果；未发出 reasoning 时显示 unavailable 而非空假卡。
- Provenance：Codex 为 `reference-unobserved`；schema/reducer fixture 可标 `synthetic`；只有真实 Runtime 事件可标 `real-runtime`。
- Owner：FEAT-134。

### GS-003 — Command 执行成功和失败

- 前置条件：固定 Runtime 真实产生安全、只读 Command Item；FEAT-136 已完成 Contracts/Host allowlist 投影；失败 variant 只使用正常、非破坏性命令，不扩大 sandbox。
- 用户操作：分别提交可正常成功与可预期失败的安全只读检查，并展开 Command Item。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：success variant 为 `command.started(inProgress) → outputDelta* → command.completed(completed, exitCode=0) → turn continues/completes`；failure variant 为 `command.started → outputDelta* → command.completed(failed|declined, stable error) → turn continues|turn.completed(failed)`。
- 可用动作：展开/折叠、复制经过脱敏和有界处理的输出；失败后可按真实恢复语义开始新尝试，但不自动重放命令。
- 最终结果：Command success/failure 与 Turn terminal 分开；无错误正文泄漏、假成功、隐式重跑或无限 retry。
- Provenance：当前只有 metadata definition；取得受支持投影后才能建立 synthetic replay 与 `real-runtime`。Codex reference 为 `reference-unobserved`。
- Owner：FEAT-136。

### GS-004 — Tool 调用成功和失败

- 前置条件：存在当前产品批准且真实注册的 Tool；无真实 Tool 时场景保持 gap，不使用静态卡片冒充。
- 用户操作：提交会明确触发该 Tool 的任务，观察成功一次及正常失败一次。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`tool.started(inProgress) → progress* → tool.completed(completed|failed) → turn continues/completes`。
- 可用动作：展开/折叠安全参数摘要与结果；不显示 raw secret、绝对路径或未批准的重试。
- 最终结果：成功/失败由真实 completed Item 决定；未知 Tool 安全降级但不阻断其它 Item。
- Provenance：当前通用 Tool 为 `synthetic: NOT RUN`；严格 frozen baseline 下 `generate_image` 不能作为通用 real-runtime 证据。Codex reference 为 `reference-unobserved`。
- Owner：FEAT-136。

### GS-005 — 命令审批允许、拒绝和过期

- 前置条件：Owner 已明确 local-only sandbox、approval policy、决定集合、审计和过期语义；未获确认时整个场景 blocked/fail closed。FileChange 审批复用该安全模型，但由 GS-006 的前置条件承接。
- 用户操作：对绑定到具体 active Item 的请求分别执行 Allow、Deny，并观察一个自然过期/失效请求。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`item.running → approval.requested → waiting_approval → allowed|denied|expired → serverRequest.resolved → item/turn authoritative result`。
- 可用动作：仅在请求 active、身份匹配且未过期时显示批准/拒绝；重复点击禁用；断线后不得保留悬空按钮。
- 最终结果：决定真实返回等待中的 Runtime request；没有有效决定时默认拒绝，不能靠 fixture UI 标记完成。
- Provenance：Codex 为 `reference-unobserved`；synthetic 只验证 reducer/UI；真实审批在 Owner 决策前 `NOT RUN/BLOCKED`。
- Owner：FEAT-137。

### GS-006 — 文件修改与 Diff

- 前置条件：Owner 已明确允许的本地写入范围和审批边界；FEAT-137 审批闭环已可用；否则 blocked。
- 用户操作：提交一个限定临时测试工作区内的正常文件编辑任务，查看逐文件和汇总 Diff。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`fileChange.started → patchUpdated/turn.diff.updated* → approval when required → fileChange.completed(completed|failed|declined) → turn.completed`。
- 可用动作：选择文件、查看 Diff、展开/折叠；审批动作由 GS-005 承接；不得把 Artifact 下载卡当作 Diff。
- 最终结果：路径经过安全表示，变更状态真实；失败/拒绝不显示“已修改”。
- Provenance：Codex 为 `reference-unobserved`；synthetic 可验证 Diff renderer；真实写入在 Owner 决策前 `NOT RUN/BLOCKED`。
- Owner：FEAT-138。

### GS-007 — 执行中补充指令

- 前置条件：active Turn 可 steer；Contracts/Host 已投影 stable `turn/steer`；已知当前 active turnId。
- 用户操作：Turn 执行中输入补充要求并发送。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`turn.in_progress → steer.submitting → steer.accepted → same turn user Item → execution continues → turn.completed`。
- 可用动作：补充输入、取消本地未提交草稿、Stop；非 steerable 或 stale Turn 必须说明原因。
- 最终结果：仍是同一个 Turn，只有一个新 user Item；响应未知时不重复 steer。
- Provenance：Codex 为 `reference-unobserved`；当前 Host 未投影，故只能先建 `synthetic: NOT RUN`，真实路径由 FEAT-139 建立。
- Owner：FEAT-139。

### GS-008 — 用户停止 Turn

- 前置条件：active Turn 已真实开始；Host/Runtime ready；没有待确认的第二次 stop。
- 用户操作：点击 Stop 一次。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`turn.in_progress → interrupt.submitting/stopping → turn.completed(interrupted) → ready`。
- 可用动作：Stop 请求发出后按钮 disabled；等待权威终态；完成后可开始新 Turn。
- 最终结果：只发送一次 interrupt；自然完成竞态仍以唯一 `turn.completed` 为准；已确认的部分内容保留并标 incomplete/interrupted。
- Provenance：Codex 为 `reference-unobserved`；计划使用正常 UI 和 Runtime 路径取得 `real-runtime`，不得通过强杀进程模拟中断。
- Owner：FEAT-139。

### GS-009 — 失败后重试或继续

- 前置条件：已有 failed/completed/interrupted Turn；不存在 active Turn 或悬空审批；原输入和结果可读。
- 用户操作：失败时显式选择 Retry；完成/中断后选择 Continue 或直接提交新输入。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`terminal turn → retry/continue intent → new turn validating/submitting → accepted → new turn.in_progress → terminal`。
- 可用动作：确认 Retry、编辑新输入、取消；危险 Command/Tool/FileChange 不得自动重放。
- 最终结果：保留原 Turn；创建有明确新 identity 的新 Turn；Continue 不发送隐藏 prompt。
- Provenance：Codex 为 `reference-unobserved`；synthetic 验证 identity/竞态；真实普通文本新尝试计划为 `real-runtime`。
- Owner：FEAT-139。

### GS-010 — 切换并恢复历史会话

- 前置条件：至少两个本地 session，均有已保存历史；其中一个可正常 Runtime resume。
- 用户操作：A→B 快速切换，向上加载历史；重开 A 并继续对话；随后正常重启 Desktop 再恢复选择。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`selection A → loading A → ready A → selection B → loading B → ready B → resume A when continuing → ready/failed-read-only`。
- 可用动作：切换、加载更早记录、重试 resume、新建 session；浏览历史不应无条件启动 Runtime Turn。
- 最终结果：A/B 内容不串线；本地历史在 Runtime unavailable 时仍可读；未知 active 状态不伪装 completed。
- Provenance：Codex 为 `reference-unobserved`；计划使用正常 Desktop/Host 生命周期取得 `real-runtime`，不清除用户现有数据制造场景。
- Owner：FEAT-140。

### GS-011 — 用户上滚后的新消息与回到底部

- 前置条件：对话足够长并有 active streaming；scroll container 可滚动。
- 用户操作：先保持底部观察自动跟随，再主动上滚；等待新内容；点击回到底部；向上加载历史。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`following → new content/autofollow → user_scrolled_up → new_content_pending → back_to_bottom → following`；分页加载保持视觉锚点。
- 可用动作：上滚阅读、回到底部、加载更早历史；文本选择不能被强制滚动打断。
- 最终结果：用户上滚后不抢滚动位置；提示真实反映新内容；reduced motion 生效。
- Provenance：Codex 为 `reference-unobserved`；Desktop-only deterministic fixture 可标 `synthetic`；最终视觉行为需真实 App 录屏。
- Owner：FEAT-141。

### GS-012 — SSE 或 Host 断线和恢复

- 前置条件：已有 durable 历史和已知 stream/event cursor；准备无攻击性的 deterministic stream fixture；不得强杀进程或破坏权限。
- 用户操作：在 fixture 中模拟连接关闭、同 stream gap 和新 stream；真实验证只使用正常停止/退出/重启流程且不得影响其它进程。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`streaming → reconnecting/resync_required → authoritative snapshot/history reconciliation → restored|recovery_required|unrecoverable`。
- 可用动作：有界重连、重新同步、重新打开或安全新建 Turn；危险动作 disabled；达到上限后停止循环。
- 最终结果：不重复消息、不跨 stream 比 sequence、不伪造 completed、不自动重放副作用。
- Provenance：Codex 为 `reference-unobserved`；resync-required/recovered raw-event fixture 已以 `synthetic: PASS` 经过真实 Desktop parser/store；真实应用 lifecycle `NOT RUN`，不能将 synthetic 写成 real-runtime PASS。
- Owner：FEAT-142。

### GS-013 — 未知 Item、缺失 delta 或无最终回答

- 前置条件：准备不含正文、路径或 secret 的三个 safe synthetic variants：`unknown-item`、`missing-delta`、`missing-final`；completed authority 可用或明确不可用。
- 用户操作：依次回放未知 Item、少一个 delta 但带 completed authority、以及 Turn completed 但没有 final 的序列；遇到冲突只触发保守 resync/recovery。
- Codex reference 状态顺序：`reference-unobserved`。
- Yijie 候选状态顺序：`known prefix → unknown/missing detected → safe placeholder|resync_required → completed reconciliation|completed-without-final|incomplete`。
- 可用动作：安全查看未知占位、重新同步、打开历史或开始新的安全 Turn；不得执行 unknown Item、补造 final 或重放危险副作用。
- 最终结果：其它已知 Item/Turn 可继续；有权威 completed 时只收敛一份内容，无权威内容、terminal 冲突或 outcome unknown 时保持更保守状态。
- Provenance：Codex 为 `reference-unobserved`；sequence-gap/missing-delta recovery fixture 已以 `synthetic: PASS` 经过真实 Desktop parser/store；unknown-item 与 missing-final 仍为 metadata-only，均不得伪装真实模型能力或通过故障注入制造结果。
- Owner：FEAT-142。

## 4. 冻结与变更规则

- 每个 `GS-*` 必须在 `05-reference-evidence-index.md` 中有唯一索引。
- 后续取得 Codex Desktop 证据时只更新 provenance/status 和证据链接，不得无 Owner 确认改写场景的稳定 ID。
- Runtime/Host/Desktop 实施不能反向把 synthetic 行为写成 Codex reference observation。
- 如果真实固定 Runtime 无法产生某场景，按 `03-capability-matrix.md` 登记 gap；不得修改/升级 Runtime。
- D0 候选场景 ID 已固定；基线尚待版本专属证据、Owner 审核与 D4 冻结，Epic 尚未完成。
