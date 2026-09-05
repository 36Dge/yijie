# FEAT-131 — Codex 风格近似对话黄金场景

> 当前范围修订（2026-09-05）：FEAT-137 已由 Owner 永久终止且未完成验收，未来不重启。CAP-019 / GS-005 为 `owner-terminated-unaccepted`，不再属于 active 交付范围；现行 active 范围排除 FEAT-137/138。下文旧 active 范围及 FEAT-137 source PASS 为历史记录，不构成审批可用或 D4 PASS。最终权威见 [FEAT-137 永久终止记录](../FEAT-137-desktop-approval-interaction/03-termination.md)。

> 作用：固定后续 active FEAT-132–137、FEAT-139–144 共用的行为场景 ID，不实现生产交互；FEAT-138 仅保留取消记录。
>
> Reference policy：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`。不绑定 Codex Desktop version/build，不需要人工媒体，也不要求一模一样。
>
> 结论：D0 场景 ID 与范围已固定，FEAT-131 D4 已通过；完整 Epic 仍需 active FEAT-132–137、FEAT-139–144 完成，FEAT-138 已正式取消/排除。FEAT-136 已交付 GS-003 的当前 Command terminal scope，FEAT-144 独立承接 GS-004。

## 1. 使用规则

每个场景区分设计依据和执行 provenance：

- `owner-approved-inference`：Owner 允许开发根据 Yijie UI 规范、固定能力与工程判断推测 Codex 风格；它不是视觉实测或版本专属事实。
- `owner-excluded`：Owner 主动排除，不实现、不建 fixture、不做真实验收。
- `real-runtime`：通过 Yijie 正常入口连接固定 Runtime 真实产生。
- `synthetic`：只用于 parser/reducer/UI 状态机的确定性回放，不能证明真实 Runtime/Host 支持。

机器目录中的 `variants` 是场景要求全集；`replayedVariants` 只列 fixture 实际覆盖的子集，并必须与 fixture 的 `coveredVariants` 精确一致。未列入的 variant 保持 metadata-only/`NOT RUN`。

安全验证约束：不得通过频繁或故障注入式强杀、替换 binary、破坏权限、恶意 fixture 或攻击载荷制造失败。断线、gap、未知事件和终态冲突优先使用非攻击性的 synthetic replay；真实进程验证只允许应用自身正常启动、停止、退出和清理流程。

## 2. 场景总表

| Scenario | Purpose | Primary classification | Owner | Reference basis | Current Yijie evidence |
|---|---|---|---|---|---|
| GS-001 | 普通问题的流式回答与最终完成 | `available` | FEAT-134、FEAT-135 | `owner-approved-inference` | `synthetic: PASS`；current canonical `real-runtime: PASS`；predecessor `pre-runtime: FAIL` |
| GS-002 | 多段过程更新与用户可见推理信息 | `requires Host/Contracts projection` | FEAT-134 | `owner-approved-inference` | metadata only；`real-runtime: NOT RUN` |
| GS-003 | Command 执行成功和失败 | `available` | FEAT-136；完整 started/delta 集成顺序由 FEAT-143 | `owner-approved-inference` | current terminal scope `real-runtime: PASS`；completed=1、failed=1、normal hydration each once；individual started/delta live 未捕获 |
| GS-004 | Tool 调用成功和失败 | `requires Host/Contracts projection` | FEAT-144 | `owner-approved-inference` | generic source conformance `PASS`；real producer/entrypoint decision `BLOCKED`；Tool D4 `NOT RUN` |
| GS-005 | 命令审批一次性允许、取消和过期（历史场景） | `owner-terminated-unaccepted` | FEAT-137（永久终止） | `owner-explicit-decision` | 未完成验收；不再实现、不重启 |
| GS-006 | 文件修改与 Diff | `intentional product difference` | FEAT-131 scope decision | `owner-excluded` | metadata-only exclusion；无 fixture、无真实验收 |
| GS-007 | 执行中补充指令 | `requires Host/Contracts projection` | FEAT-139 | `owner-approved-inference` | metadata only；projection unavailable |
| GS-008 | 用户停止 Turn | `available` | FEAT-139 | `owner-approved-inference` | `real-runtime: NOT RUN` |
| GS-009 | 失败后重试或继续 | `available` | FEAT-139 | `owner-approved-inference` | metadata only；`real-runtime: NOT RUN` |
| GS-010 | 切换并恢复历史会话 | `available` | FEAT-140 | `owner-approved-inference` | `real-runtime: NOT RUN` |
| GS-011 | 用户上滚后的新消息与回到底部 | `available` | FEAT-141 | `owner-approved-inference` | `synthetic: NOT RUN` |
| GS-012 | SSE 或 Host 断线和恢复 | `requires Host/Contracts projection` | FEAT-142 | `owner-approved-inference` | safe `synthetic: PASS`；real lifecycle `NOT RUN` |
| GS-013 | 未知 Item、缺失 delta 或无最终回答 | `requires Host/Contracts projection` | FEAT-142 | `owner-approved-inference` | sequence-gap `synthetic: PASS`；其余 variants metadata only |

## 3. 详细场景

### GS-001 — 普通问题的流式回答与最终完成

- 前置条件：Host/Runtime ready；已有 idle session 或可以创建新 session；安全纯文本输入；没有 active Turn。
- 用户操作：在 Composer 输入普通问题并发送。
- 目标状态顺序：`idle → validating → submitting → accepted → turn.in_progress → agentMessage.started → agentMessage.delta* → agentMessage.completed → turn.completed(completed) → ready`。
- 可用动作：提交前可编辑；active 后可 Stop；完成后可选择/复制回答并开始新 Turn。
- 最终结果：只有一个 user Item、一个 Turn 和一份权威 final；完成后无 streaming 光标，历史 hydration 不重复内容。
- Reference basis：`owner-approved-inference`；上述顺序是 Codex-inspired 设计目标，不是参考 App 实测事实。
- Provenance：streaming/completed raw-event fixture 为 `synthetic: PASS`。current canonical 安全纯文本 Turn 首轮完成并精确返回 `FEAT-131_SMOKE_OK`，记为 `real-runtime: PASS`；没有工具调用或重试。predecessor submission 没有产生 Runtime thread/turn/delta/terminal，继续单独记为 `pre-runtime: FAIL`。
- Owner：FEAT-134、FEAT-135。

### GS-002 — 多段过程更新与用户可见推理信息

- 前置条件：固定 Runtime/Provider 实际发出多个 Assistant/reasoning Item；未发出时显示 unavailable，不补造。
- 用户操作：提交需要多步处理、但不触发危险写操作的任务。
- 目标状态顺序：`turn.in_progress → commentary/progress Item* ↔ reasoning-visible Item* → final agentMessage → item.completed* → turn.completed`。
- 可用动作：过程/reasoning 可展开折叠；active 时可 Stop；隐藏 reasoning 不提供批准或信任入口。
- 最终结果：progress/reasoning 保持次级层级，final 是唯一主结果。
- Reference basis：`owner-approved-inference`；模型推理强度配置 UI 已排除，但用户可见 reasoning summary 仍在范围内。
- Provenance：当前 metadata-only；只有真实 Runtime 事件可标 `real-runtime`。
- Owner：FEAT-134。

### GS-003 — Command 执行成功和失败

- 前置条件：固定 Runtime 真实产生安全、只读 Command Item；FEAT-136 已完成 Contracts/Host allowlist 投影；失败 variant 只使用正常、非破坏性命令。
- 用户操作：分别提交可正常成功与可预期失败的安全只读检查，并展开 Command Item。
- 目标状态顺序：success 为 `command.started → outputDelta* → command.completed(completed, exitCode=0)`；failure 为 `command.started → outputDelta* → command.completed(failed|declined, stable error)`，随后 Turn 继续或终止。
- 可用动作：展开/折叠、复制脱敏且有界的输出；失败后可以显式开始新尝试，不自动重放命令。
- 最终结果：Command success/failure 与 Turn terminal 分开；无假成功、隐式重跑或无限 retry。
- Reference basis：`owner-approved-inference`。
- Provenance：Owner-authorized Runtime repair 与 final cross-pin 后，fresh canonical tranche 得到 completed=1、failed=1、exit/duration/stable error、安全复制与正常 hydration 各一次，当前 terminal scope 记为 `real-runtime: PASS`。Command Item started 与独立 output-delta live 因执行过快未捕获；focused source tests 不冒充 live evidence，完整集成状态顺序由 FEAT-143 承接。
- Owner：FEAT-136；FEAT-143 承接明确后移的完整状态顺序。

### GS-004 — Tool 调用成功和失败

- 前置条件：存在当前产品批准且真实注册的 Tool；没有真实 Tool 时保持 capability gap。
- 用户操作：提交会明确触发该 Tool 的任务，观察成功一次及正常失败一次。
- 目标状态顺序：`tool.started(inProgress) → progress* → tool.completed(completed|failed) → turn continues|completes`。
- 可用动作：展开/折叠安全参数摘要与结果；不显示 raw secret、绝对路径或未批准重试。
- 最终结果：成功/失败由真实 completed Item 决定；未知 Tool 安全降级但不阻断其它 Item。
- Reference basis：`owner-approved-inference`。
- Provenance：Contracts/Host/Desktop generic Tool source conformance 为 `PASS`，但没有 Owner-approved real producer 或产品入口，因此 real success/failure 与 D4 保持 `BLOCKED / NOT RUN`；不使用 experimental dynamic tool、临时注册或 fixture 冒充。
- Owner：FEAT-144。

### GS-005 — 命令审批一次性允许、取消和过期

- 前置条件：exact `local + demo_fast + FEAT-137 gate`；`experimentalApi=false`、`sandbox=read-only`、`approvalPolicy=on-request`、唯一 allowlisted Git repository check 与 120 秒 TTL。默认、gate 关闭和非 local 仍为 `never`。
- 用户操作：对绑定到具体 active Command Item 的请求分别执行 Accept once、Cancel，并在安全自然条件下观察一个过期/失效请求。
- 目标状态顺序：`command approval requested → waiting_approval → accepted|cancelled|expired → serverRequest.resolved → command/turn authoritative result`。
- 可用动作：仅在请求 active、身份匹配且未过期时显示 accept once / cancel current turn；不显示 decline、session approval 或 policy/network amendment；重复点击禁用，断线后动作立即禁用。
- 最终结果：Accept once 只在 read-only 内执行一次；Cancel/expired 不执行目标 Command。TTL 先胜时 Host 只向仍 pending 的 Runtime request 发送一次 `Cancel` 并投影 `expired`；Runtime/Item/Turn cleanup 先胜时投影 `resolved_elsewhere` 且不再响应。
- Reference basis：`owner-approved-inference`。FileChange approval 不属于本场景，也不纳入 Epic。
- Provenance：Owner D0 decision与Contracts `2e490dea…` / Host `118651804…` / Desktop `918bd26b…` immutable source conformance `PASS`；真实allow/cancel、自然expiry/reconnect与D4 `NOT RUN`。synthetic/source证据不能证明真实审批闭环。
- Owner：FEAT-137。

### GS-006 — 文件修改与 Diff（Owner 主动排除）

- 前置条件：N/A；Owner 已明确不实现。
- 用户操作：N/A；产品不提供 FileChange/Diff 入口或审批动作。
- 目标状态顺序：N/A；不得在生产 UI 或 test-only fixture 中合成 FileChange/patch/diff 状态。
- 可用动作：无。
- 最终结果：保持 `intentional product difference`；既有 Artifact 能力继续独立存在，但不得包装成 Diff。
- Reference basis：`owner-excluded`。
- Provenance：metadata-only exclusion；无 synthetic fixture、无 `real-runtime` 验收；FEAT-138 已于 2026-08-29 正式取消/排除，无实现责任。
- Owner：FEAT-131 scope decision。

### GS-007 — 执行中补充指令

- 前置条件：active Turn 可 steer；Contracts/Host 已投影 stable `turn/steer`；已知 active turnId。
- 用户操作：Turn 执行中输入补充要求并发送。
- 目标状态顺序：`turn.in_progress → steer.submitting → steer.accepted → same turn user Item → execution continues → turn.completed`。
- 可用动作：补充输入、取消本地未提交草稿、Stop；non-steerable 或 stale Turn 说明原因。
- 最终结果：仍是同一个 Turn，只有一个新 user Item；响应未知时不重复 steer。
- Reference basis：`owner-approved-inference`。
- Provenance：Host 未投影，当前 metadata-only；真实路径由 FEAT-139 建立。
- Owner：FEAT-139。

### GS-008 — 用户停止 Turn

- 前置条件：active Turn 已真实开始；Host/Runtime ready；没有待确认的第二次 stop。
- 用户操作：点击 Stop 一次。
- 目标状态顺序：`turn.in_progress → interrupt.submitting/stopping → turn.completed(interrupted) → ready`。
- 可用动作：Stop 发出后按钮 disabled；等待权威终态；完成后可开始新 Turn。
- 最终结果：只发送一次 interrupt；自然完成竞态仍以唯一 `turn.completed` 为准；已确认的部分内容保留并标 incomplete/interrupted。
- Reference basis：`owner-approved-inference`。
- Provenance：计划通过正常 UI/Runtime 路径取得 `real-runtime`；不通过强杀模拟中断。
- Owner：FEAT-139。

### GS-009 — 失败后重试或继续

- 前置条件：已有 failed/completed/interrupted Turn；不存在 active Turn 或悬空审批；原输入和结果可读。
- 用户操作：失败时显式选择 Retry；完成/中断后选择 Continue 或直接提交新输入。
- 目标状态顺序：`terminal turn → retry/continue intent → new turn validating/submitting → accepted → new turn.in_progress → terminal`。
- 可用动作：确认 Retry、编辑新输入、取消；危险 Command/Tool 不得自动重放。
- 最终结果：保留原 Turn；创建有明确新 identity 的新 Turn；Continue 不发送隐藏 prompt。
- Reference basis：`owner-approved-inference`。
- Provenance：synthetic 可验证 identity/竞态；真实普通文本新尝试计划为 `real-runtime`。
- Owner：FEAT-139。

### GS-010 — 切换并恢复历史会话

- 前置条件：至少两个本地 session，均有已保存历史；其中一个可正常 Runtime resume。
- 用户操作：A→B 快速切换，向上加载历史；重开 A 并继续对话；正常重启 Desktop 后恢复选择。
- 目标状态顺序：`selection A → loading A → ready A → selection B → loading B → ready B → resume A when continuing → ready|failed-read-only`。
- 可用动作：切换、加载更早记录、重试 resume、新建 session；浏览历史不无条件启动 Runtime Turn。
- 最终结果：A/B 内容不串线；本地历史在 Runtime unavailable 时仍可读；未知 active 状态不伪装 completed。
- Reference basis：`owner-approved-inference`。
- Provenance：计划使用正常 Desktop/Host 生命周期取得 `real-runtime`，不清除用户数据制造场景。
- Owner：FEAT-140。

### GS-011 — 用户上滚后的新消息与回到底部

- 前置条件：对话足够长并有 active streaming；scroll container 可滚动。
- 用户操作：保持底部观察自动跟随，再主动上滚；等待新内容；点击回到底部；向上加载历史。
- 目标状态顺序：`following → new content/autofollow → user_scrolled_up → new_content_pending → back_to_bottom → following`；分页加载保持视觉锚点。
- 可用动作：上滚阅读、回到底部、加载更早历史；文本选择不被强制滚动打断。
- 最终结果：用户上滚后不抢位置；提示真实反映新内容；reduced motion 生效。
- Reference basis：`owner-approved-inference`。
- Provenance：Desktop-only deterministic fixture 可标 `synthetic`；最终视觉行为只需在 Yijie App 中验收，不依赖 Codex 媒体。
- Owner：FEAT-141。

### GS-012 — SSE 或 Host 断线和恢复

- 前置条件：已有 durable 历史和已知 stream/event cursor；准备非攻击性的 deterministic stream fixture。
- 用户操作：fixture 模拟连接关闭、同 stream gap 和新 stream；真实验证只使用正常停止/退出/重启流程。
- 目标状态顺序：`streaming → reconnecting|resync_required → authoritative snapshot/history reconciliation → restored|recovery_required|unrecoverable`。
- 可用动作：有界重连、重新同步、重新打开或安全新建 Turn；达到上限后停止循环。
- 最终结果：不重复消息、不跨 stream 比 sequence、不伪造 completed、不自动重放副作用。
- Reference basis：`owner-approved-inference`。
- Provenance：resync/recovered raw-event fixture 为 `synthetic: PASS`；真实应用 lifecycle `NOT RUN`。
- Owner：FEAT-142。

### GS-013 — 未知 Item、缺失 delta 或无最终回答

- 前置条件：准备无正文、路径或 secret 的 `unknown-item`、`missing-delta`、`missing-final` safe variants；completed authority 可用或明确不可用。
- 用户操作：依次回放三个序列；遇到冲突只触发保守 resync/recovery。
- 目标状态顺序：`known prefix → unknown|missing detected → safe placeholder|resync_required → completed reconciliation|completed-without-final|incomplete`。
- 可用动作：查看安全占位、重新同步、打开历史或开始新的安全 Turn；不执行 unknown Item、不补造 final。
- 最终结果：其它已知 Item/Turn 可继续；有权威 completed 时只收敛一份内容，否则保持更保守状态。
- Reference basis：`owner-approved-inference`。
- Provenance：sequence-gap/missing-delta recovery 为 `synthetic: PASS`；unknown-item 与 missing-final 仍是 metadata-only。
- Owner：FEAT-142。

## 4. 固定与变更规则

- 每个 `GS-*` 必须在 `05-reference-evidence-index.md` 中有唯一索引。
- 后续实现不得把 `owner-approved-inference` 写成参考 App 实测，也不得把 `synthetic` 写成 `real-runtime`。
- 如果最终冻结 Runtime `b2b20e2…` 无法产生某场景，按 `03-capability-matrix.md` 登记 capability gap；不得再次修改、升级或替换 Runtime。
- GS-006 永久保留稳定 ID 作为负范围哨兵；除非 Owner 重新修改 Epic 范围，否则不得添加 fixture、投影或 UI。
- policy ID、13 个场景 ID 与 Owner 排除边界已固定；FEAT-131 D4 已通过，完整 Epic 尚未完成。
