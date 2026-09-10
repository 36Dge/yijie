# FEAT-131 — Codex 风格近似对话能力矩阵

> 2026-09-11 FEAT-144 当前本地范围：Sorftime 单工具 product_detail、US 单公开 ASIN。原生成功、参数/结果核对、权限停用与模式复原、最终来源原生拒绝和普通重开已完成；九项活动 AC 的证据与 D4 检查见[24 最终报告](../FEAT-144-desktop-real-tool-producer-items/24-final-native-decline-and-delivery-2026-09-11.md)。元数据14/20、文本9/13、业务2逻辑调用保守扣4/10、图片0。AC-004业务失败用户排除，不计PASS；E/F分次实跑保留各自来源，未观察的progress/冷历史缺失仍保留。后续22个提交已获授权普通推送、远端SHA一致，CI未触发；实际结果见[26](../FEAT-144-desktop-real-tool-producer-items/26-remote-delivery-2026-09-11.md)，不改写FEAT-131历史D4。

> 2026-09-09：下表 native 相关行已按当前源码修正；原始基线/历史证据保留，交付范围与限制见[一致性复核](06-native-consistency-review-2026-09-09.md)。

> 当前范围修订（2026-09-05）：FEAT-137 已由 Owner 永久终止且未完成验收，未来不重启。CAP-019 / GS-005 为 `owner-terminated-unaccepted`，不再属于 active 交付范围；现行 active 范围排除 FEAT-137/138。下文旧 active 范围及 FEAT-137 source PASS 为历史记录，不构成审批可用或 D4 PASS。最终权威见 [FEAT-137 永久终止记录](../FEAT-137-desktop-approval-interaction/03-termination.md)。

> Profile：`demo_fast` · Exposure：`local`
>
> Runtime 约束：原始冻结点为 `0ce5902…`；Owner 后续仅授权 FEAT-136 early-denial producer 的最小 source patch。当前最终冻结点为 `b2b20e2…` / 0.144.6，此后不再修改、升级、重编译、替换或启用新的实验 API
>
> Reference policy：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`
>
> 结论：本矩阵固定能力边界和近似设计依据；它不代表后续交互已经实现，也不代表 Epic 已完成。

## 1. 固定身份与策略

| Identity | Frozen value | Authority |
|---|---|---|
| Codex-inspired design policy | `codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference` | `references/reference-inference-policy.md` |
| Yijie Runtime repository commit（final re-freeze） | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:4-13` |
| Yijie Runtime original freeze（history） | `0ce5902ed400866be0196886bb78f693a004d68d` | `references/runtime-freeze-evidence.md`；FEAT-136 history |
| Upstream Codex tag | `rust-v0.144.6` | 同上 |
| Upstream Codex commit | `5d1fbf26c43abc65a203928b2e31561cb039e06d` | 同上；`yijie-codex/.yijie/schemas/app-server/baseline.json:3-5` |
| Runtime version | `0.144.6` | 同上 |
| App-server schema file count | `267` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:12` |
| App-server schema tree SHA-256 | `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:13` |
| API mode | stable；`experimentalApi=false` | `yijie-codex/.yijie/schemas/app-server/baseline.json:8-9` |
| Runtime transport | stdio | 同上 |
| Host transport/auth | local HTTP/SSE；owner-only bearer | `yijie-contracts/compatibility/agent-host-runtime-v1.json:15-19` |
| Host sandbox/approval | 当前 FEAT-152 原生权限配置；旧 FEAT-137 opt-in 永久拒绝 | read-only/never 仅为原隔离验收配置；不得改当前权限匹配旧文档，FEAT-152 不继承 FEAT-137 验收 |

“Runtime repository commit”和“upstream Codex commit”是两个不同身份，不得互相替换。`b2b20e2…` 仅包含 Owner-authorized FEAT-136 minimal producer repair；upstream tag/commit、Runtime version、267-file schema corpus 与 tree digest 保持不变。当前工作区即使发现远端更新，也不得通过 pull、同步、构建或重生成 schema 改变最终冻结值。

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
- `blocker`：`none`、`owner-product-decision`、`owner-security-decision`、`experimental-api-disabled`、`real-runtime-producer-unavailable`。
- `design_basis`：在范围内的 Codex-inspired 目标使用 `owner-approved-inference`；Owner 主动排除使用 `owner-excluded`；既有 Yijie authority 差异使用 `yijie-product-authority`。它不是视觉实测或 Runtime provenance。

## 3. 当前受支持 Host 投影

权威兼容清单只允许下列 Runtime surface：

- methods：`skills/config/write`、`skills/extraRoots/set`、`skills/list`、`thread/resume`、`thread/start`、`turn/interrupt`、`turn/start`；
- notifications（13 个）：`error`、`item/agentMessage/delta`、`item/commandExecution/outputDelta`、`item/completed`、`item/mcpToolCall/progress`、`item/reasoning/textDelta`、`item/started`、`skills/changed`、`thread/started`、`turn/completed`、`turn/plan/updated`、`turn/started`、`warning`。

来源：`yijie-contracts/compatibility/agent-host-runtime-v1.json:20-43`。

Host 代码中另有 `thread/delete` 和受条件开关约束的 `generate_image` 路径，但它们没有进入上述锁定 projection。`item/reasoning/textDelta` 已进入最终清单；其余路径继续标为“实现路径已观察、supported projection 未确认”，不得仅凭代码存在判定 `available`。

## 4. 能力矩阵

所有 Codex 风格目标均以 Owner 批准的近似策略为设计依据，不绑定 Codex Desktop version/build，也不等待人工媒体。表中的 Runtime、Host 和 Desktop 列仍必须来自可核对的代码或运行事实；`owner-approved-inference` 不能被写成参考 App 实测结论。

| ID | Observable capability | Runtime stable method/event | Primary classification | Delivery lane | Blocker | Current Host/Contracts | Current Desktop | Owner Feature | Design basis |
|---|---|---|---|---|---|---|---|---|---|
| CAP-001 | 固定 Runtime/Host 能力身份 | initialize/baseline metadata | `available` | `baseline-documentation` | `none` | manifest 已固定 | readiness 已校验版本边界 | FEAT-131 | `owner-approved-inference` |
| CAP-002 | 新建并恢复 Thread | `thread/start`、`thread/resume`、`thread/started` | `available` | `none` | `none` | 已锁定投影 | 已有 session 创建/恢复与映射 | FEAT-132、FEAT-140 | `owner-approved-inference` |
| CAP-003 | Thread active/idle/system-error 状态 | `thread/status/changed` | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未投影 | 仅由本地阶段粗粒度派生 | FEAT-132、FEAT-140 | `owner-approved-inference` |
| CAP-004 | 产品会话列表与正文历史 authority | thread/read(includeTurns=true)、thread/resume | `available` | `contracts-host-desktop` | `none` | native v7 读取原生历史；不解析 rollout | SQLCipher 保管产品记录及已观察事实，冷历史分开标来源、旧历史只读 | FEAT-132、FEAT-140 | `yijie-product-authority` |
| CAP-005 | Archive/Unarchive | `thread/archive`、`thread/unarchive` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 未投影 | 无对应交互；Owner 尚未决定纳入或形成主动产品差异 | FEAT-140 | `owner-approved-inference` |
| CAP-006 | 删除/重命名 Thread | `thread/delete`、`thread/name/set` | `available` | `desktop-only` | `none` | delete 有未登记扩展；name 未投影 | 已有本地删除、重命名 authority | FEAT-140 | `owner-approved-inference` |
| CAP-007 | 文本新 Turn | `turn/start` + text input | `available` | `desktop-only` | `none` | 已投影 | 已有 Composer 与提交闭环 | FEAT-135 | `owner-approved-inference` |
| CAP-008 | 图片/文件附件随 Turn 提交 | `turn/start` 的 text/image/localImage；无通用 file input | `available` | `desktop-only` | `none` | v2 受控转换复用 `turn/start` | 已有附件导入、解析、绑定和历史 | FEAT-135；复用 FEAT-127 | `owner-approved-inference` |
| CAP-009 | Assistant Item 流式文本 | item/started、item/agentMessage/delta、item/completed | `available` | `contracts-host-desktop` | `none` | native v7 保留原生身份和内容 | 唯一 NativeDisplayBuffer 按 Item 累计，完整 Item 直接替换；不做正文对账 | FEAT-132、FEAT-134 | `owner-approved-inference` |
| CAP-010 | Commentary 与 final answer 分层 | AgentMessage.phase | `available` | `contracts-host-desktop` | `none` | native v7 保留 phase，缺失保持 null | FEAT-134 按原生阶段显示；缺 phase 未分类，不声称 provider 稳定提供 | FEAT-134 | `owner-approved-inference` |
| CAP-011 | 推理摘要与模型推理记录 | summaryTextDelta、summaryPartAdded、textDelta、reasoning completed | `available` | `contracts-host-desktop` | `none` | 原生 summary/content 分类与索引，沿用 local-only raw 权限 | FEAT-134 分类别/原生索引纯文本展示；summary-only 不冒充 raw，缺失如实披露 | FEAT-134 | `owner-approved-inference` |
| CAP-012 | 稳定计划/步骤更新 | turn/plan/updated | `available` | `contracts-host-desktop` | `none` | native v7 已投影原生 plan | FEAT-134 只显示实际 plan；没有 plan 不造步骤，正向新模型样本未补跑 | FEAT-134 | `owner-approved-inference` |
| CAP-013 | schema 注释为实验的 Plan Item/delta | `item/plan/delta` 存在于 non-experimental schema，协议只有 EXPERIMENTAL 注释、没有 runtime gate attribute | `requires Host/Contracts projection` | `contracts-host-desktop` | `real-runtime-producer-unavailable` | 未进入锁定投影，也没有当前 producer 证据 | 不得生成假步骤；优先使用稳定 `turn/plan/updated` | FEAT-134 | `owner-approved-inference` |
| CAP-014 | Turn started/completed/interrupted/failed | turn/started、turn/completed | `available` | `contracts-host-desktop` | `none` | 原生 turn/completed 的 status 决定 Turn 结果 | Turn 与 Item 独立；UI busy 与执行事实分离，不自动封口 Item | FEAT-132、FEAT-134 | `owner-approved-inference` |
| CAP-015 | 非终态 error/warning 与投影诊断 | error、warning、projection notice | `available` | `contracts-host-desktop` | `none` | 安全代码与 availability 独立于执行状态 | FEAT-134 仅安全代码映射；范围不足时放会话层，不猜 Turn/Item 归属 | FEAT-134、FEAT-142 | `owner-approved-inference` |
| CAP-016 | Command 生命周期与安全输出 | commandExecution、item/commandExecution/outputDelta | `available` | `contracts-host-desktop` | `none` | native v7 转发原生 Item；delta 仅输出 pending-final 诊断；最终 aggregatedOutput 安全投影，v5 保留兼容 | 原五项 D4 属历史 v5；2026-09-09 native 卡片修复/八项 local D4 已通过，真实两条成功/失败及重开；final-only 策略保留 | FEAT-136；FEAT-143 后移项不授权恢复 v5；FEAT-137 永久终止 | `owner-approved-inference` |
| CAP-017 | MCP Tool 生命周期与 progress | mcpToolCall、item/mcpToolCall/progress | `available` | `contracts-host-desktop` | `none` | Sorftime 单工具原生身份、参数、安全文本、availability、原生Prompt、兼容reader及保存/重开已实现 | E真实成功与F原生拒绝/重开通过；progress未观察且不补造，正文安全脱敏为partial；业务失败用户排除 | FEAT-144 | `owner-approved-inference` |
| CAP-018 | Runtime 发起的 dynamic image tool | `item/tool/call`；当前 Host 注册路径会开启 experimental capability | `blocked by frozen Runtime` | `baseline-documentation` | `experimental-api-disabled` | 仅 FEAT-128 条件路径，默认 baseline 不支持；不能作为 CAP-017 替代品 | Artifact UI 存在，但不能证明 final frozen baseline 的真实 producer | FEAT-144 boundary；复用 FEAT-128 | `owner-approved-inference` |
| CAP-019 | Command 本地审批 | `item/commandExecution/requestApproval`（仅历史 schema） | `owner-terminated-unaccepted` | `none` | `owner-permanent-termination` | Owner 因实现耗时过长永久终止；旧 v6 source/reader 保留审计，Host/Native/UI 入口关闭 | 未完成真实审批及 D4 验收；不再实现、不重启、不以收尾检查替代验收 | FEAT-137（永久终止） | `owner-explicit-decision` |
| CAP-020 | 一般权限请求与 MCP elicitation | `item/permissions/requestApproval`、`mcpServer/elicitation/request` | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-security-decision` | FEAT-144已薄适配稳定Sorftime空表单；一般表单/URL/requestUserInput及其它未支持请求仍拒绝，不属于FEAT-137 | Sorftime实际批准/拒绝与模式停用已验证；不宣称一般MCP表单或所有权限请求完整支持 | FEAT-144有限范围；一般能力仍为Owner backlog | `owner-approved-inference` |
| CAP-021 | Tool 请求用户结构化输入 | `item/tool/requestUserInput` 存在于 non-experimental schema，协议只有 EXPERIMENTAL 注释、没有 runtime gate attribute | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 未进入锁定投影；当前无真实 producer 证据；明确不属于 FEAT-137 | 不得显示假问答卡 | 未分配 Owner backlog（不属于 FEAT-137） | `owner-approved-inference` |
| CAP-022 | FileChange Item、逐文件 patch 与 turn diff | fileChange Item、`item/fileChange/patchUpdated`、`turn/diff/updated` | `intentional product difference` | `none` | `none` | stable schema 存在，但本 Epic 不新增投影 | Owner 明确不实现；Artifact 不能代替 Diff | FEAT-131 scope decision | `owner-excluded` |
| CAP-023 | Host v3 Artifact 图片/视频/文件/报告展示 | Host v3 `item.artifact.*` 是 Yijie 归一化事件，不等同于 Runtime dynamic tool | `available` | `desktop-only` | `none` | v3 Artifact 事件和资源接口存在 | 已有 Artifact cards；真实 producer 限制另见 CAP-018 | 复用 FEAT-128；FEAT-143 回归 | `owner-approved-inference` |
| CAP-024 | Stop active Turn | `turn/interrupt` + terminal `turn/completed` | `available` | `desktop-only` | `none` | 已投影 | 已有 Stop 按钮；等待真实终态 | FEAT-139 | `owner-approved-inference` |
| CAP-025 | 执行中补充指令 | `turn/steer` stable | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未投影 | streaming 时 Composer 当前禁用 | FEAT-139 | `owner-approved-inference` |
| CAP-026 | Retry/Continue | 无专用 retry；使用新的 `turn/start` 和明确 operation identity | `available` | `desktop-only` | `none` | 可创建后续 Turn | 无独立 Retry/Continue intent 与副作用保护 UI | FEAT-139 | `owner-approved-inference` |
| CAP-027 | 长对话自动跟随、上滚、新内容提示、回到底部 | 客户端行为 | `available` | `desktop-only` | `none` | N/A | 已有自动跟随、回到底部、分页位置保持；无新内容计数/阅读位置持久化 | FEAT-141 | `owner-approved-inference` |
| CAP-028 | SSE gap、断线、Host restart 后确定性恢复 | `thread/resume` 只恢复 Runtime thread 身份 | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 仅进程内 replay；重启后无正文重放/完整 Item snapshot | 已有 sequence/eventId/resync，但不能证明全部 Item 结果 | FEAT-142 | `owner-approved-inference` |
| CAP-029 | Unknown Item、缺失 delta、无 final 的保守收敛 | item/turn completed、thread read 可提供部分权威事实 | `requires Host/Contracts projection` | `contracts-host-desktop` | `none` | 未支持 notification 被忽略；未知 Item 只保留 type | 未知 Item 不展示；assistant completed 只能部分对账 | FEAT-142 | `owner-approved-inference` |
| CAP-030 | 其他 stable Item：hook、collab/subagent、webSearch、imageView、sleep、review、compaction | 固定 schema 中存在对应 ThreadItem | `requires Host/Contracts projection` | `contracts-host-desktop` | `owner-product-decision` | 只有泛化生命周期，详情丢失 | 无通用 Item shell 展示 | FEAT-133、FEAT-136、FEAT-140 | `owner-approved-inference` |
| CAP-031 | 亮暗主题、最小窗口、缩放、键盘、焦点、VoiceOver、reduced motion | 客户端行为 | `available` | `desktop-only` | `none` | N/A | 有部分现状；按 Yijie UI 规范完成近似体验 | FEAT-143 | `owner-approved-inference` |
| CAP-032 | 分支到新聊天 / Fork | `thread/fork` | `intentional product difference` | `none` | `none` | 未投影且无需为本 Epic 新增 | Owner 明确不实现“回复不佳”右侧的分支按钮 | FEAT-131 scope decision | `owner-excluded` |
| CAP-033 | 语音 | 客户端能力 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现 | FEAT-131 scope decision | `owner-excluded` |
| CAP-034 | 模型版本信息 | 展示策略 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现 | FEAT-131 scope decision | `owner-excluded` |
| CAP-035 | 模型推理强度信息 | 展示策略 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现；不影响 CAP-011 reasoning summary | FEAT-131 scope decision | `owner-excluded` |
| CAP-036 | 右上角分享 | 客户端能力 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现 | FEAT-131 scope decision | `owner-excluded` |
| CAP-037 | 切换置顶摘要 | 客户端能力 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现 | FEAT-131 scope decision | `owner-excluded` |
| CAP-038 | 显示侧边面板 | 客户端能力 | `intentional product difference` | `none` | `none` | N/A | Owner 明确不实现 | FEAT-131 scope decision | `owner-excluded` |

CAP-022 与 CAP-032～038 共计 8 项 Owner 主动排除。CAP-032 只排除 Fork，CAP-005 的 Archive/Unarchive 保持独立待决；CAP-035 只排除模型配置/档位信息，CAP-011 的用户可见 reasoning summary 仍在 Epic 范围内。

## 5. Owner 与停止条件

- Active FEAT-132–136、FEAT-139–144 必须引用相应 `CAP-*` 和固定 reference policy；FEAT-138 已正式取消/排除，仅保留决策记录。FEAT-144 独立承接 CAP-017 / GS-004，不能被 CAP-018 替代。后续只根据 Owner 明确范围变更更新，不跟随某个 Codex Desktop 版本自动漂移。
- `requires Host/Contracts projection` 只允许投影上述固定 Runtime stable 能力；必须先改权威 Contracts，再改 Host 和 Desktop。
- `blocked by frozen Runtime` 不得通过开启 experimental API、修改 schema、替换 binary、模拟事件或硬编码 UI 绕过。
- CAP-019 的早期 security/source PASS 仅为历史。Owner 已永久终止 FEAT-137，未完成验收；不再要求补齐 allow/cancel、expiry/reconnect 或 D4。CAP-020仅增加FEAT-144已验收的Sorftime空表单薄适配；其余未支持请求及CAP-021继续fail closed，不扩大权限。
- `owner-approved-inference` 允许合理近似，但不能覆盖 Runtime/Host 事实、伪造生产能力或被表述为视觉实测。
- 当前 policy ID、38 个能力 ID 与分类词表已固定；FEAT-131 D4 已通过，完整 Epic 尚未完成。
