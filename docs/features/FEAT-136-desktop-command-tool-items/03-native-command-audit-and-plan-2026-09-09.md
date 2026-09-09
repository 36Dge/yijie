# FEAT-136 原生 Command 审计与调整方案

日期：2026-09-09。本文件保留提交方案时的源码审计与设计。用户随后“授权执行”，现已进入实施；当前修改和验收状态见 [01-delivery-log.md](01-delivery-log.md) 与 [02-verification.md](02-verification.md)，不能把下文审计时缺陷视为修复后的当前结论。

本记录回答 FEAT-132/134 改造后的现状，不覆盖 2026-08-30 原 Command D4。原五项 Must、日期、固定提交、prior 3/3 FAIL、RCA 0-call 和 fresh 1/5 PASS 保持其历史语义。旧 PASS 不能证明当前 native 路径的全部 Command 行为。真实 Tool 仍属于 FEAT-144，implementation blocked / D4 NOT RUN。

## 1. 审计基线与结论

五仓分支均为 `chore/retirement-baseline-20260905`，审计开始时工作区干净：

| 仓库 | 完整 HEAD |
|---|---|
| Contracts | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 |
| Host | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b |
| Desktop | 6e5047d1c23041c46dd495ddb89e24c7e4db5d47 |
| 元仓 | 7ddf9e64a56df2af4aa4f6906408b0d1a85a48df |
| Codex | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

Host/Desktop native consumer 均固定 Contracts `6f632f155eacdaf93df0e0b00b5dab9e369c5442`；Desktop 权限 source lock 固定 Host `f4cf01bd6f7e9f37792ef743d44f0ce10527c10b`。当前仓库 HEAD 与被锁定的源提交职责不同，不能把文档 HEAD 前进理解为协议升级。Runtime 继续使用已有 FEAT-136 两补丁构建，不修改或升级。

**结论：有调整必要，但没有重写命令执行器。** 新对话的生命周期和最终结果来自 Codex；FEAT-132 已移除 Desktop 的旧事件 reducer。仍存在旧 v5 兼容投影与计数状态，以及新事实套入旧卡片时的信息损失。最合适的方案是“原生 Command 事实 + 既有安全最终输出 + 忠实的只读卡片”，不恢复原先的客户端状态推演。

## 2. 实际调用链与复用证据

| 层 | 当前事实与源码入口 | 判断 |
|---|---|---|
| Runtime | `codex-rs/app-server-protocol/src/protocol/v2/item.rs` 的 CommandExecution、McpToolCall；`protocol/event_mapping.rs` 的 ItemStarted/ItemCompleted/ExecCommandOutputDelta；`app-server/src/bespoke_event_handling.rs` 转发原生输出 delta | 命令执行、输出聚合、status、exitCode、durationMs 由 Codex 提供；没有 Host 自研执行器 |
| Host native | `internal/session/native_conversation.go` 的 projectNativeItem、publishNativeNotification、ReadNativeThread；`internal/codex/session_protocol.go` 的 ReadThread | 复用原始通知和 thread/read(includeTurns=true)，只做类型、身份、资源、安全投影 |
| Desktop 订阅 | `src-tauri/src/chat/application.rs::stream_native_conversation` → open_native_event_stream → NativeDisplayBuffer → commit_native_view → publish_native | 新对话统一 native v7；Artifact 使用独立既有 v3 资源通道，不把普通 v3 事件送入 native 缓冲 |
| 唯一显示缓冲 | `src-tauri/src/chat/native_conversation.rs::observe` | 原生 Item 完整对象直接替换；仅文本/reasoning delta 追加；Turn 结束不封口其余 Item |
| 保存与读取 | `src-tauri/src/chat/native_conversation_storage.rs` 的 chat_native_facts/chat_native_views、native_recovery_views | SQLCipher 保存已观察安全事实/显示副本；已观察终态优先；冷历史不猜 ID 合并 |
| 展示 | `src/domain/conversation-view.ts::nativeExecution` → conversation-timeline → ChatCommandItem / ChatToolItem | 是只读适配，但旧卡片模型损失或误解释了一些 native 信息 |
| 兼容 | Host `feat136_projection.go`、Desktop `feat136.rs`、ipc.rs 的 v5 历史 DTO、chat.store.ts::loadHistoryAuthority | 仍有路由、旧历史和资源消费者，不是仅凭文件名可删除的垃圾代码 |

Host 的 `processNotification` 对非 Turn terminal 在 defer 中发布原始参数的 native 投影，未使用旧 v5 合成结果。v5 仍由 `cmd/desktop-host/main.go` 按旧开关创建事件 hub，`publishV5Lifecycle/publishV5CommandDelta/publishV5ToolProgress` 仍被调用。`v5Items` 保存实际 started/completed 观察、sealed 和安全输出/进度容量计数；旧 FEAT-137 身份检查也引用它，但 FEAT-137 入口永久关闭。这不是新 native 显示 authority，也不能未经兼容决策移除活跃 v5 路由。

Desktop `feat136.rs` 当前主要是只读投影类型和转换，未保留旧 Command reducer。当前源码已没有 FEAT-132 删除的 TurnEventReducer/ReasoningAccumulator；不得为了清理指标再新增替代机制。

## 3. 为什么 Command 完成后才显示输出

1. Codex 原生提供 `item/commandExecution/outputDelta`，不是 Runtime 没有流式能力。
2. Host native 收到该事件时，明确生成 `projection_notice`，code 为 `command_output_pending_final`，不转发 delta 正文。
3. 原因已经写在 Contracts `openapi/native-conversation/native-conversation.yaml` 的 SSE 语义中：任意分片可能切开秘密/路径，逐片脱敏不足；又不能为此新增第二套 Host 正文累积器。
4. 收到原生 `item/completed` 后，Host 使用 Codex `aggregatedOutput` 调用已有安全投影和 UTF-8 容量限制；Desktop 直接展示这个最终对象。TypeScript 当前 `liveOutput: null` 是这一策略的结果。

所以它是当前明确的安全/复用取舍，不能通过重新接入 v5 流式正文、放宽脱敏、双订阅累计或把原始输出发进 WebView 来“修复”。原历史记录的“执行太快未捕获 delta”只解释当时的 v5 D4，不能解释现在 native v7 的最终输出策略。

冷历史也需精确区分：Runtime 的 ThreadHistoryBuilder **能够处理** ExecCommandBegin/End；但是固定 Runtime 的 Legacy rollout policy 不持久化这些 Command 事件，Command ItemCompleted 主要依赖 Paginated 模式。因此不能承诺 cold thread/read 恢复每条完整 Command。不得复制 HistoryBuilder、解析 rollout 或开启实验模式补齐；优先读取已保留的 SQLCipher 原生事实，没有保存过的内容明确不可用。

## 4. 需要修正的问题

| 编号 | 当前代码事实 | 用户影响与调整 |
|---|---|---|
| C136-01 | nativeExecution 忽略 Host 已提供的 cwdLabel，一律构造 redacted cwd | 丢失“当前项目”等安全信息；直接显示安全标签，不把标签反解成路径 |
| C136-02 | item.availability != available 就标记 output.truncated/upstream_truncated，retention 却固定 complete | duration 等元数据不完整也被说成上游输出截断；改为分别表达已收到输出与 Item 信息完整性，无证据不归因 |
| C136-03 | ChatCommandItem 对 output 文本为空一律说“命令已完成”，不检查 native status | failed 或仍 inProgress 的合法空输出会产生矛盾；区分原生结果、是否有输出字段、合法空内容、未收到完成对象 |
| C136-04 | shell 已停止 busy，但 Command 卡片仍依据旧 running 状态播报“正在执行”，默认展开及“等待安全输出”也未使用 activityLabel | 历史或 Turn 已结束却缺 Item end 时误报正在执行；用既有 busy/activityLabel 显示“最后观察到执行中 / 本轮已结束，未观察到该项结束记录” |
| C136-05 | nativeExecution 的 error 恒为 null；原 CommandExecution 本来没有通用 error 字段，旧 v5 command_failed 是安全映射码 | 当前不满足原 AC 的 stable error 展示描述；由显式 native failed/declined 映射稳定产品文案/代码，并标明其为展示映射，不能冒称 Codex 原生 error |
| C136-06 | command_output_pending_final 存为会话级 diagnostic，最终对象到达后该观察记录仍可能保留 | 不能根据会话 warning 的到达时间猜归某个 Item；卡片以自身最后观察对象提示输出策略，会话诊断使用历史观察文案，不伪称当前一直等待 |
| C136-07 | McpToolCall 只转发安全通用标签、参数/结果有无，始终 partial；未转发 tool error、duration，progress 不进入 native 展示 | 现有 native Tool 不是完整 Tool 产品；保留占位并记录 FEAT-144 缺口，不制造真实 producer 或补写 Tool 执行器 |

当前协议只有 Item 级 availability，没有输出专属截断原因/完整性字段。推荐本次先诚实表达“已收到的安全输出；部分信息不完整”，不新增猜测字段。精确区分 Host 容量截断、Runtime 输出截断等属于后续源契约方案；没有可信证据不能声称任何一方发生截断。

## 5. 可直接交给 Codex 的执行任务

### 范围与权威

执行 FEAT-136 原生 Command 展示调整。保持 Command-only 产品范围，复用 FEAT-132 native v7、唯一 NativeDisplayBuffer、thread/read/resume 和 SQLCipher。沿用 FEAT-134 对 summary/raw、availability、busy 的职责分离。FEAT-137 永久退役，FEAT-152 权限不变。本方案不授权 Runtime、新 Tool、原始输出透传、权限扩大、付费调用或推送。

实施前重新检查各仓 AGENTS、工作区、当前 full commit/pin/digest、FEAT-132/134 最终验收及本记录；保护并发修改。本次候选纯进程内展示方案 `contract-impact=none`：不改 Host wire、private IPC、持久化 schema、历史解释或权限。如必须增加跨进程字段/改变 native output-delta 行为，立即重新分类并先提交 Contract First 方案，不把它混入 UI 修复。

### 实施步骤

1. 原 2026-08-30 四文件包先完整归档；重写当前 feature.yaml/brief/交付/验收的原生实施权威。新 AC 从 pending 开始，旧数目与 PASS 不继承。保留原五项用户目标、范围拆分与豁免，按下表细化当前验收。
2. 优先在 `conversation-view.ts` 的进程内模型区分 native Command 与 legacy 只读投影；保留 native provenance，不为满足旧卡片必填项伪造 startedSource、retention 或 cwd 结构。使用现有字段，不复制 Native wire DTO。
3. 修改 ChatCommandItem，必要时微调 timeline 的只读 props：修复 C136-01～06。输出文本继续纯文本、安全复制；只有真实 clipboard 成功才提示成功。命令的状态、退出码、耗时不由 UI 重新计算。0ms、exit 0 和空字符串都属于合法值。
4. failed/declined 的固定产品文案和代码只由显式 native status 映射；exit 非零不自动改写 completed，Turn failed 不自动改写 Command。Tool 的未知或不完整信息保持明示，C136-07 转 FEAT-144 决策清单。
5. 按引用清理**确实无调用**的 Command 专属适配残留。已经删除的 reducer/publish 函数不重复立项。保留旧 v4/v5 DTO、IPC、数据库 reader、safe projection helper、v5 hub/route 及资源依赖；没有消费者退役证据时不删除它们。若提取共用安全纯函数，只移动实现并保持行为/来源校验，不复制第二份。
6. 增加 native Command → readonly view → 真实组件的普通合成定向回归。现有 ChatCommandItem 主要直接构造旧 execution DTO，不能单独证明 native 字段没有丢失。保留原 schema/security/caps/脱敏和旧历史断言，不批量跳过。
7. 实现阶段结束后单独做结构化自审：检查原生身份、终态、不猜测原因、无第二累计、旧历史兼容、无日志正文及 FEAT-152。只执行正常非破坏性测试；不跑含攻击/故障注入/强杀等禁止场景的广泛套件。
8. 运行适用的源生成/来源检查、TypeScript/lint/构建、定向 Command/Native/SQLCipher/Composer/Artifact/权限回归及需求包门禁。若只改 UI，不机械 repin Contracts/Host；改到被校验来源时按 Contracts → Host → Desktop 固定真实提交。commit/push 另按本次明确授权执行。
9. 使用 `pnpm tauri:demo-fast:app` 日常 canonical 入口。先核对普通身份、实际 Host Home、app-data、映射及活跃 Turn，等正常完成再正常退出。已有数据优先；无可信绑定的旧任务不续跑、不补发。检查历史 Command、会话切换、附件/Artifact、权限入口、键盘/200%和正常重启。
10. 确需新 Command 成功/失败样本时，为本次另核实模型预算和普通验证操作范围；旧 FEAT-132/134/136 额度不可相加或转用。所有新 Must 满足后才能关闭此次调整 D4。未运行、缺样本及旧限制逐项保留。

### 本次调整建议验收标准

| AC | 可判定结果 |
|---|---|
| N136-001 | 原生 Command ID/status/exitCode/durationMs 按事实显示，0 值保留；failed/declined 文案仅为显式 status 的安全映射，投影问题不改原生结果 |
| N136-002 | 完整 Item 替换临时对象，覆盖更短、不同、空输出及 completed 没有先观察到 started；无前缀对账、自动封口或第二累计 |
| N136-003 | Turn 结束、历史读取、连接不可确认时没有错误 busy/“正在执行”播报；Item 原始状态及缺结束观察仍保留 |
| N136-004 | 安全 cwdLabel 不丢失；null/空输出/最终片段/Item partial 区分，未知截断原因不伪造；不把失败空输出说成执行成功 |
| N136-005 | 继续只显示和复制已有安全最终输出；不重新启用原始 delta；会话诊断不猜 Item 归属，不制造 pending final 的永久当前状态 |
| N136-006 | SQLCipher 原生事实正常重开保持同一 ID/来源/终态；冷历史不覆盖已观察内容，旧 Command 历史只读可访问 |
| N136-007 | Command 原生适配与组件联合定向测试通过；canonical 切换/退出重启、light/键盘/aria-live/200%、附件/Artifact/Composer/FEAT-152 无定向回归 |
| N136-008 | 无新 reducer、状态推演、历史重建器、正文累积器；保留兼容有调用证据，删除项有引用核对；Tool 未实现范围、历史验收及豁免如实保留 |

## 6. 方案自审与取舍

- 推荐方案不承诺实时 Command 正文：最小改动即可修复信息损失，保持既有安全边界及单一 native 通道。
- 不选“恢复 v5 输出”：它会把旧分片处理再次带入新对话，增加来源/重复累计复杂度，也不能凭旧测试证明任意分片脱敏可靠。
- 不选“升级 Runtime/开启实验历史/自己解析 rollout”：超出授权且重新制造历史 authority；不存在必须这样做才能修好卡片的问题。
- 后续若产品必须显示安全实时输出，应独立确定原生支持、安全输出边界及跨仓契约，然后决定是否可行。不能把这一需求隐藏在本次 UI 修复中。
- 提交本方案的审计阶段仅执行源码/需求/依赖审计与文档修正，没有产品代码修改或模型调用；随后用户授权实施与10次文本预算，结果以当前01/02记录为准。检查结果统一记在[一致性复核](../FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。
