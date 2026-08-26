# FEAT-131 — Codex Desktop 对话能力矩阵

> Profile：`demo_fast` · Exposure：`local`
>
> Runtime 约束：固定 `yijie-codex` Runtime，不修改、不升级、不重编译、不替换、不启用新的实验 API
>
> 结论：本矩阵冻结能力边界；它不代表后续交互已经实现，也不代表 Epic 已完成。

## 1. 冻结身份

| Identity | Frozen value | Authority |
|---|---|---|
| Yijie Runtime repository commit | `0ce5902ed400866be0196886bb78f693a004d68d` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:4-13` |
| Upstream Codex tag | `rust-v0.144.6` | 同上 |
| Upstream Codex commit | `5d1fbf26c43abc65a203928b2e31561cb039e06d` | 同上；`yijie-codex/.yijie/schemas/app-server/baseline.json:3-5` |
| Runtime version | `0.144.6` | 同上 |
| App-server schema file count | `267` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:12` |
| App-server schema tree SHA-256 | `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:13` |
| API mode | stable；`experimentalApi=false` | `yijie-codex/.yijie/schemas/app-server/baseline.json:8-9` |
| Runtime transport | stdio | 同上 |
| Host transport/auth | local HTTP/SSE；owner-only bearer | `yijie-contracts/compatibility/agent-host-runtime-v1.json:15-19` |
| Host sandbox/approval | `read-only` / `never` | 同上 |

“Runtime repository commit”和“upstream Codex commit”是两个不同身份，不得互相替换。当前工作区即使发现远端更新，也不得通过 pull、同步、构建或重生成 schema 改变上述冻结值。

## 2. 分类规则

`primary_classification` 只能使用以下四个精确值：

| Value | 含义 |
|---|---|
| `available` | 所需真实事实已经由当前批准边界提供，或该能力不需要新增跨进程事实。它不自动表示 Desktop UI 已完成；具体实施层见 `delivery_lane`。 |
| `requires Host/Contracts projection` | 固定 Runtime stable schema 已有事实，但当前受支持的 Contracts/Host 投影未提供足够语义。必须按 Contracts → Host → Desktop 顺序实施。 |
| `blocked by frozen Runtime` | 所需行为只存在于实验 API、当前固定配置不可用，或必须升级/修改 Runtime 才能成立。不得绕过。 |
| `intentional product difference` | Yijie 明确采用不同产品 authority/行为，或该项被 Owner 主动排除。不能把“尚未实现”伪装成主动差异。 |

补充列不改变 primary classification：

- `delivery_lane`：`none`、`desktop-only`、`contracts-host`、`contracts-host-desktop`、`baseline-documentation`。
- `blocker`：`none`、`reference-unobserved`、`owner-product-decision`、`owner-security-decision`、`experimental-api-disabled`、`real-runtime-producer-unavailable`。
- `reference_status`：没有版本/build 对应的截图、录屏或可核对操作记录时必须为 `reference-unobserved`。

## 3. 当前受支持 Host 投影

权威兼容清单只允许下列 Runtime surface：

- methods：`skills/config/write`、`skills/extraRoots/set`、`skills/list`、`thread/resume`、`thread/start`、`turn/interrupt`、`turn/start`；
- notifications（9 个）：`error`、`item/agentMessage/delta`、`item/completed`、`item/started`、`skills/changed`、`thread/started`、`turn/completed`、`turn/started`、`warning`。

来源：`yijie-contracts/compatibility/agent-host-runtime-v1.json:20-39`。

Host 代码中另有 `thread/delete`、`item/reasoning/textDelta` 和受条件开关约束的 `generate_image` 路径，但它们没有全部进入上述锁定 projection。矩阵将其标为“实现路径已观察、supported projection 未确认”，不得仅凭代码存在判定 `available`。

## 4. 能力矩阵

所有 Codex Desktop 版本专属表现目前均以证据索引为准。没有媒体/操作证据的行保持 `reference-unobserved`；表中的状态顺序来自固定 Runtime schema 和 Yijie 代码事实，不是对 Codex Desktop 外观或版本行为的记忆性描述。

| ID | Observable capability | Runtime stable method/event | Primary classification | Delivery lane | Blocker | Current Host/Contracts | Current Desktop | Owner Feature | Reference status |
|---|---|---|---|---|---|---|---|---|---|
| CAP-001 | 冻结 Runtime/Host 能力身份 | initialize/baseline metadata | `available` | `baseline-documentation` | `none` | manifest 已固定 | readiness 已校验版本边界 | FEAT-131 | `reference-unobserved` |
| CAP-002 | 新建并恢复 Thread | `thread/start`、`thread/resume`、`thread/started` | `available` | `none` | `none` | 已锁定投影 | 已有 session 创建/恢复与映射 | FEAT-132、FEAT-140 | `reference-unobserved` |
| CAP-003 | Thread active/idle/system-error 状态 | `thread/status/changed` | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未投影 | 仅由本地阶段粗粒度派生 | FEAT-132、FEAT-140 | `reference-unobserved` |
| CAP-004 | 产品会话列表与正文历史 authority | `thread/list`、`thread/read` 可作 Runtime 诊断输入 | `intentional product difference` | `desktop-only` | `none` | 不作为产品正文 authority | Desktop SQLite 是既定产品 authority | FEAT-140 | `reference-unobserved` |
| CAP-005 | Fork/Archive/Unarchive | `thread/fork`、`thread/archive`、`thread/unarchive` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 未投影 | 无对应交互；Owner 尚未决定纳入或形成主动产品差异 | FEAT-140 | `reference-unobserved` |
| CAP-006 | 删除/重命名 Thread | `thread/delete`、`thread/name/set` | `available` | `desktop-only` | `none` | delete 有未登记扩展；name 未投影 | 已有本地删除、重命名 authority | FEAT-140 | `reference-unobserved` |
| CAP-007 | 文本新 Turn | `turn/start` + text input | `available` | `desktop-only` | `none` | 已投影 | 已有 Composer 与提交闭环 | FEAT-135 | `reference-unobserved` |
| CAP-008 | 图片/文件附件随 Turn 提交 | `turn/start` 的 text/image/localImage；无通用 file input | `available` | `desktop-only` | `none` | v2 受控转换复用 `turn/start` | 已有附件导入、解析、绑定和历史 | FEAT-135；复用 FEAT-127 | `reference-unobserved` |
| CAP-009 | Assistant Item 流式文本 | `item/started`、`item/agentMessage/delta`、`item/completed` | `available` | `desktop-only` | `none` | 已投影基础生命周期 | 已聚合为单一 live assistant 文本 | FEAT-134 | `reference-unobserved` |
| CAP-010 | Commentary/progress 与 final answer 分层 | `AgentMessage.phase=commentary/final_answer`；Provider 可能不发 phase | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 当前 Item 投影丢弃 phase | 当前合并为同一文本区域 | FEAT-134 | `reference-unobserved` |
| CAP-011 | 用户可见 reasoning summary | `item/reasoning/summaryTextDelta`、`summaryPartAdded`、`textDelta`、reasoning completed | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | textDelta 有实现路径但不在锁定清单；summary 未投影 | 已有 reasoning disclosure，但语义不是完整 summary parity | FEAT-134 | `reference-unobserved` |
| CAP-012 | 稳定计划/步骤更新 | `turn/plan/updated` | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未投影 | 无 | FEAT-134 | `reference-unobserved` |
| CAP-013 | schema 注释为实验的 Plan Item/delta | `item/plan/delta` 存在于 non-experimental schema，协议只有 EXPERIMENTAL 注释、没有 runtime gate attribute | `requires Host/Contracts projection` | `contracts-host-desktop` | `real-runtime-producer-unavailable` | 未进入锁定投影，也没有当前 producer 证据 | 不得生成假步骤；优先使用稳定 `turn/plan/updated` | FEAT-134 | `reference-unobserved` |
| CAP-014 | Turn started/completed/interrupted/failed | `turn/started`、`turn/completed` | `available` | `desktop-only` | `none` | 已投影；completed 是唯一 Turn 终态 | 已有 streaming 与三类终态 | FEAT-132、FEAT-134 | `reference-unobserved` |
| CAP-015 | 非终态 error/warning 的上下文展示 | `error`、`warning` | `available` | `desktop-only` | `none` | 已投影且不等于 Turn 终态 | live projection 未提供独立 error/warning Item | FEAT-134、FEAT-142 | `reference-unobserved` |
| CAP-016 | Command started/output/completed/failed/declined | commandExecution Item、`item/commandExecution/outputDelta` | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 仅泛化 item type，命令/状态/输出被丢弃 | 无 Command Item | FEAT-136 | `reference-unobserved` |
| CAP-017 | MCP Tool 生命周期与 progress | mcpToolCall Item、`item/mcpToolCall/progress` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 当前无通用 MCP/tool 投影 | 无通用 Tool Item | FEAT-136 | `reference-unobserved` |
| CAP-018 | Runtime 发起的 dynamic image tool | `item/tool/call`；当前 Host 注册路径会开启 experimental capability | `blocked by frozen Runtime` | `baseline-documentation` | `experimental-api-disabled` | 仅 FEAT-128 条件路径，默认 baseline 不支持 | Artifact UI 存在，但不能证明 frozen baseline 的真实 producer | FEAT-136、FEAT-138 | `reference-unobserved` |
| CAP-019 | Command/FileChange 本地审批 | `item/commandExecution/requestApproval`、`item/fileChange/requestApproval` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-security-decision` | `read-only/never`；未实现 reverse request 默认拒绝 | 只有只读策略说明，无 Allow/Deny 动作 | FEAT-137 | `reference-unobserved` |
| CAP-020 | 一般权限请求与 MCP elicitation | `item/permissions/requestApproval`、`mcpServer/elicitation/request` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-security-decision` | 未实现 | 无；是否纳入必须由 Owner 决定 | FEAT-137 | `reference-unobserved` |
| CAP-021 | Tool 请求用户结构化输入 | `item/tool/requestUserInput` 存在于 non-experimental schema，协议只有 EXPERIMENTAL 注释、没有 runtime gate attribute | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 未进入锁定投影；当前无真实 producer 证据 | 不得显示假问答卡 | FEAT-137 | `reference-unobserved` |
| CAP-022 | FileChange Item、逐文件 patch 与 turn diff | fileChange Item、`item/fileChange/patchUpdated`、`turn/diff/updated` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-security-decision` | 未投影；read-only 阻止真实写入路径 | 无 Diff；Artifact 不能代替 Diff | FEAT-138 | `reference-unobserved` |
| CAP-023 | Host v3 Artifact 图片/视频/文件/报告展示 | Host v3 `item.artifact.*` 是 Yijie 归一化事件，不等同于 Runtime dynamic tool | `available` | `desktop-only` | `none` | v3 Artifact 事件和资源接口存在 | 已有 Artifact cards；真实 producer 限制另见 CAP-018 | FEAT-138；复用 FEAT-128 | `reference-unobserved` |
| CAP-024 | Stop active Turn | `turn/interrupt` + terminal `turn/completed` | `available` | `desktop-only` | `none` | 已投影 | 已有 Stop 按钮；等待真实终态 | FEAT-139 | `reference-unobserved` |
| CAP-025 | 执行中补充指令 | `turn/steer` stable | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未投影 | streaming 时 Composer 当前禁用 | FEAT-139 | `reference-unobserved` |
| CAP-026 | Retry/Continue | 无专用 retry；使用新的 `turn/start` 和明确 operation identity | `available` | `desktop-only` | `none` | 可创建后续 Turn | 无独立 Retry/Continue intent 与副作用保护 UI | FEAT-139 | `reference-unobserved` |
| CAP-027 | 长对话自动跟随、上滚、新内容提示、回到底部 | 客户端行为 | `available` | `desktop-only` | `none` | N/A | 已有自动跟随、回到底部、分页位置保持；无新内容计数/阅读位置持久化 | FEAT-141 | `reference-unobserved` |
| CAP-028 | SSE gap、断线、Host restart 后确定性恢复 | `thread/resume` 只恢复 Runtime thread 身份 | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 仅进程内 replay；重启后无正文重放/完整 Item snapshot | 已有 sequence/eventId/resync，但不能证明全部 Item 结果 | FEAT-142 | `reference-unobserved` |
| CAP-029 | Unknown Item、缺失 delta、无 final 的保守收敛 | item/turn completed、thread read 可提供部分权威事实 | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未支持 notification 被忽略；未知 Item 只保留 type | 未知 Item 不展示；assistant completed 只能部分对账 | FEAT-142 | `reference-unobserved` |
| CAP-030 | 其他 stable Item：hook、collab/subagent、webSearch、imageView、sleep、review、compaction | 固定 schema 中存在对应 ThreadItem | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 只有泛化生命周期，详情丢失 | 无通用 Item shell 展示 | FEAT-133、FEAT-136、FEAT-138、FEAT-140 | `reference-unobserved` |
| CAP-031 | 亮暗主题、最小窗口、缩放、键盘、焦点、VoiceOver、reduced motion | 客户端行为 | `available` | `desktop-only` | `none` | N/A | 有部分现状，完整 parity 未验收 | FEAT-143 | `reference-unobserved` |

## 5. Owner 与停止条件

- FEAT-132–143 必须引用相应 `CAP-*`，不得根据后来 Codex Desktop 自动更新静默改写本矩阵。
- `requires Host/Contracts projection` 只允许投影上述固定 Runtime stable 能力；必须先改权威 Contracts，再改 Host 和 Desktop。
- `blocked by frozen Runtime` 不得通过开启 experimental API、修改 schema、替换 binary、模拟事件或硬编码 UI 绕过。
- `owner-security-decision` 未关闭前，审批、文件写入、通用工具和权限提升保持 blocked/fail closed。
- `reference-unobserved` 只能由版本/build 匹配、已脱敏且可核对的截图、录屏或操作记录关闭。
- D0 候选能力 ID 与分类词表已固定；待 Owner 证据审查和 D4 完成后才能宣称基线已冻结。Epic 尚未完成。
