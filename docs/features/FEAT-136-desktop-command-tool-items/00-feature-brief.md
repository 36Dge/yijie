# FEAT-136 — Desktop Command 与 Tool 执行 Item Demo Brief

> Profile: demo_fast · Exposure: local · Created: 2026-08-29
>
> 当前结论：D0 与 Contracts slice complete（`yijie-contracts@3c3000a6fbe2f08ab2131a463a1691e867d661b1`）；Host、Desktop 与 canonical D4 entrypoint gate repair 已形成 clean 本地 commits，source-anchored conformance 和修复后独立审查均 PASS；用户已授权最多 3 次真实 Provider/模型请求用于安全只读 Command D4，但当前尚未发起调用。Tool D4 继续等待真实 producer/Owner 决策；整体 Feature in progress。

## 1. 用户问题、目标与 Epic 关系

- 目标用户：在易界 AI Desktop 中需要理解 Agent 执行过程与结果的本地用户。
- 当前问题：固定 Runtime 已提供 CommandExecution 和 McpToolCall 稳定事实，但当前 Host/Desktop 只暴露泛化 Item，安全摘要、输出、进度、耗时、exit code、失败和拒绝均不可见。
- 用户结果：本地实现已经可以消费由真实 Host 事件形状驱动、可重放、可 hydration 的 Command/Tool Item，且 WebView 与持久化只接收有界、脱敏、版本化投影；是否在真实 Runtime Command 路径成立，留给单独 D4 验证。
- Epic authority：CAP-016 与 GS-003 是 Command Must；CAP-017 与 GS-004 是通用 MCP Tool 目标。CAP-018 的 experimental dynamic image tool 不得冒充 MCP Tool。CAP-019 至 CAP-021、GS-005 属于 FEAT-137 或未决产品/安全决策。CAP-022、GS-006 与 FEAT-138 永久保持 owner-excluded。

### In scope

- schema v3、demo_fast + local 正式四文件包和 D0。
- yijie-contracts 0.7.0 local candidate：显式协商 AgentSessionEventV5。
- Command started/output delta/completed/failed/declined 安全投影。
- MCP Tool started/progress/completed/failed 及预留 declined 的安全通用投影。
- event identity、at-least-once replay、completed reconciliation、caps、redaction、unknown 与持久化最小字段。
- published contracts-v0.2.0 和 FEAT-134 candidate 双基线兼容检查。
- Host 从 `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` 实现默认关闭的 v5 negotiation、Command mapper/redactor/caps、event ID/replay 与 completed reconciliation，并固化为本地 commit `83d3163e21579042d2cc21f303e943946ff97eb0`；Tool 只提供通用稳定投影。
- Desktop 从 `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` 实现 v5 closed decoder、event-ID reducer、SQLCipher additive migration、持久化/hydration、Command/Tool UI、unknown fail-soft 与无障碍状态；core 与 canonical gate repair 分别固化为 `69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba`、`65ee3062833ef3d185511599d8f3a4018f635369`。
- 使用同一 Contracts schema 与 11 个普通 fixture 完成 Host producer 到 Desktop consumer 的 source-anchored conformance；不把它表述为真实 Runtime D4。
- 修复 canonical `local/demo_fast --stable-api-only` 入口：runner/stable build 同步开启 FEAT-134/136 Native/Web gates，非 stable/release 路径清除 ambient FEAT-136，sidecar 在 `env_clear()` 后只白名单转发依赖闭合的 Native gate；精确 preflight 重基线到当前 Contracts/Host commits 且保留 v4 不变量。
- 本第三批仅执行最多 3 次真实 Provider/模型请求的安全只读 Command D4，并通过正常关闭、重开观察 hydration；不扩大到 Tool D4。

### Out of scope

- 不执行 Tool D4；不注册或制造 Tool producer。Command D4 只允许用户已授权的最多 3 次真实请求和两个指定只读 Command，不得重试。
- 在完成真实 App light/dark、1180×760、200% 交互前，不把 component tests 表述为视觉实测。
- 不修改 Runtime、experimentalApi、approvalPolicy、sandbox、network、filesystem、shell 或 Tauri 权限。
- 不注册 MCP/Connector/dynamic tool，不制造真实 Tool producer，不把 synthetic fixture 表述为真实能力。
- 不增加 Command approval、FileChange、Diff、patch、file approval、write gate、Artifact 合并或相关 fixture。
- 不 push、tag、merge、publish、release、deploy 或创建远端 PR。

## 2. D0 工程事实

### Feature ID 与工作区

- FEAT-136 正式目录创建前不存在，ID 可用。
- 最初发现：yijie 位于 FEAT-135 分支 e654dcb4b09c9daa5904a365ab202c9dc0f1c2e4，只有 6 个 FEAT-138 取消范围的正式 FEAT-131 文档改动。
- 治理固化：在 yijie 的 feat/feat-136-desktop-command-tool-items 分支先形成独立 commit 67f219b6cf825357285215fcbaafb33c3978acb3，随后工作树 clean。
- D0/Contracts slice 固化：yijie 随后形成本地 commit c7bc206e89692b591eb044af09de21fdb4f1154d；本次 source-conformance evidence commit 基于该 HEAD，固化 Host/Desktop commits、canonical gate repair 与真实调用授权边界。
- Contracts 起点：feat/feat-136-desktop-command-tool-items，基线 3832a6c5e99b2a6365f193280fdb887c8fdbc2de，创建分支时 clean。
- Contracts 不可变本地提交：3c3000a6fbe2f08ab2131a463a1691e867d661b1，提交后 clean，未 push/tag/publish。
- Host 实现起点：feat/feat-134-desktop-streaming-progress-final-response@b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe；当前 clean 本地 commit 为 `83d3163e21579042d2cc21f303e943946ff97eb0`，未 push/tag/publish。
- Desktop 实现起点：feat/feat-135-desktop-codex-style-composer@fc52ef33cdf040d9b6e8d71bd7498811c5c38c51；当前分支 feat/feat-136-desktop-command-tool-items 的 clean HEAD 为 `65ee3062833ef3d185511599d8f3a4018f635369`，其 core parent 为 `69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba`，未 push/tag/publish。
- Runtime 只读：develop@0ce5902ed400866be0196886bb78f693a004d68d，clean，本地落后 origin/develop 1 个提交且有意不更新。

### Runtime freeze

- Runtime 0.144.6 / upstream rust-v0.144.6@5d1fbf26c43abc65a203928b2e31561cb039e06d。
- 267 个 canonical schema，tree SHA-256 82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1。
- stdio、experimentalApi=false、Host sandbox=read-only、approvalPolicy=never。
- 不 fetch/pull/rebase/build/generate/patch/replace Runtime。

## 3. Contract impact 与版本决定

最终分类为 semantic。

现有 v4 的顶层 oneOf、事件 discriminator 与 Item payload 均为闭合/严格结构，直接增加 Command/Tool 字段或事件会让旧 strict consumer 失败或误解。因此不能写 additive，也不能扩写 v4。本 Feature 新增独立 v5 schema/proto/channel/route，要求 event_schema_version=5；v1 至 v4 的源、路由和 consumer 语义保持原样。

权威顺序：

1. 固定 Runtime stable canonical schema，只读；
2. AgentSessionEventV5 JSON/SSE source authority；
3. AsyncAPI v5 与 Agent Host v5 OpenAPI 引用 JSON authority；Protobuf v5 是 typed transport，所有可解码 message 仍须经过 JSON-equivalent semantic gate；
4. 本批 Host 是唯一 Runtime mapper；
5. FEAT-132 ConversationState 与 Desktop SQLCipher 分别承担 UI 状态和已观察历史 authority。

## 4. v5 冻结安全语义

### Common identity 与终态

- 最小关联字段：task_id、agent_session_id、codex_thread_id、turn_id、item_id。
- 事件字段：event_id、stream_id、sequence、occurred_at、event_type、terminal。
- delivery 至少一次；sequence 只在同一 stream_id 内单调；consumer 只按 event_id 去重。
- 相同输出文本可合法连续出现；不同 event_id 的相同文本不得按内容去重。
- item.completed 封口对应 Item，terminal=false；只有 turn.completed 是 Turn terminal。
- 普通 error/warning 均不是 Turn terminal。

### Caps 与保留策略

| Surface | Frozen cap / policy |
|---|---|
| 单个 compact JSON SSE data value | projection 后 1,048,576 UTF-8 bytes |
| Command display summary | 4,096 UTF-8 bytes |
| cwd | closed workspace_root / workspace_relative segments / redacted；含 `/` 分隔符总计 1,024 UTF-8 bytes |
| Command output delta | 每事件 16,384 UTF-8 bytes；未投影内容以 closed truncation metadata 表达 |
| Command completed output | 每 Item 262,144 UTF-8 bytes；完整、head_tail（各 131,072 bytes）或显式 unavailable |
| Tool server/tool display identity | 各 256 UTF-8 bytes；不安全或未登记时固定 unknown |
| Tool arguments summary | 8,192 UTF-8 bytes，metadata-only |
| Tool progress summary | 每事件 4,096 UTF-8 bytes；每 Item 最多 32 个、合计最多 65,536 bytes |
| Tool result summary | 65,536 UTF-8 bytes，metadata-only |
| Stable error summary | 4,096 UTF-8 bytes |

契约要求所有文本先执行 allowlist/redaction，再按 UTF-8 bytes 计数与截断。Command live delta 达到 aggregate cap 后显式标记 truncated 并停止继续发布 delta；completed 的 complete/head-tail/unavailable union 是最终 authority。所有 bounded summary 自带 `truncated`，只有截断时才携带闭合 `truncation_reason`；不存在 `redacted` 自证字段。Host sanitizer 已由聚焦 redaction/caps tests 覆盖，但 source-anchored tests 仍不能替代真实 Runtime D4。

### Command allowlist

- 允许：安全 display summary、结构化 cwd、running/completed/failed/declined、duration_ms、exit_code、安全 delta、bounded completed output（含 Runtime aggregate 缺失时的 unavailable）、truncated/reason、stable error code/summary。
- Stable error code：command_failed、command_declined、projection_limit_exceeded、projection_redaction_failed、protocol_error。
- 禁止：raw command、绝对/canonical cwd、processId、source、commandActions、raw aggregatedOutput、原始 Runtime item/wire。

### Tool allowlist 与 capability gap

- 允许：安全 server/tool display identity、known/unknown、in_progress/completed/failed 与 Yijie 预留 declined、metadata-only arguments/progress/result summary、duration_ms、stable error、truncated/reason；unknown identity 固定为 `unknown` sentinels，不保留源标签。
- Stable error code：tool_failed、tool_declined、unknown_tool、projection_limit_exceeded、projection_redaction_failed、protocol_error。
- 禁止：raw arguments/result/content/structuredContent/meta、appContext/resource URI、plugin/connector id、token、secret、Runtime wire。
- 固定 Runtime 的 McpToolCall status 只有 inProgress/completed/failed，没有 declined。v5 declined 仅是 Yijie 预留/合成 conformance 状态，当前 Host 不得把缺失事实猜成 declined。
- 固定 Runtime `is_error=true` 的真实形态是 failed + result + no raw error；v5 允许保留 bounded safe result summary，并要求根据失败状态产生 normalized stable error，不透传 raw MCP result/error。
- Generic Tool contract 可以完成；CAP-017 的实际产品 Tool、Owner 决策与 GS-004 real-runtime 仍 BLOCKED/NOT RUN。该 gap 不阻塞 Command。

### Unknown 与 persistence/hydration

- 不安全/未登记 Tool identity 降级为 unknown；只保留 metadata-only summary，不阻断其它 Item 或 Turn。
- v5 generic Item 只允许命名的 stable allowlist；未知 v5 event/variant 必须被 closed parser 丢弃并触发保守 resync，不允许 raw fallback；旧 v1 至 v4 consumer 不会收到 v5。
- Desktop durable Item 保存 common identity、kind/status、安全摘要、cap/truncation、duration/exit/error 与 completed authority，不保存 raw wire 或秘密；mixed legacy/v4/v5 history 按每个 Turn 的真实 authority hydration，不把旧行伪装成 v5。

## 5. Must 验收

| AC | 可观察行为 | 本批证据边界 |
|---|---|---|
| AC-001 | Command started/output/completed 与 completed/failed/declined 准确 | Host/Desktop focused conformance PASS；真实 Command D4 NOT RUN |
| AC-002 | event_id 去重，合法重复文本不被内容去重 | Host replay + Desktop reducer tests PASS；真实 replay D4 NOT RUN |
| AC-003 | completed bounded snapshot 权威封口，late delta 不改终态 | Host reconciliation + Desktop persistence/hydration tests PASS |
| AC-004 | Command allowlist、cwd、caps、redaction 与 stable error | Host sanitizer/caps + Desktop closed decoder tests PASS；真实 Runtime content NOT RUN |
| AC-005 | Tool lifecycle/progress、安全摘要与 capability gap 如实 | 通用 source conformance PASS；无 producer，真实 Tool BLOCKED/NOT RUN |
| AC-006 | unknown Tool fail-soft，unknown event fail-closed/resync | Host projection + Desktop parser/resync tests PASS |
| AC-007 | persistence/hydration 最小结构足以只恢复一份 Item | additive migration、mixed authority 与 hydration tests PASS |
| AC-008 | Command/Tool UI 可读、可折叠、可安全复制且可访问 | component/a11y tests PASS；真实视觉矩阵 NOT RUN |

所有 Must AC 在真实 Command D4、视觉矩阵及 Tool capability 决策完成前保持 pending；source conformance 通过不等于 Feature usable。

## 6. 第三批执行与停止条件

- FEAT-136 整体仍为目标 12 小时、硬停止 16 小时；当前第三批只收口 canonical gate repair 与 Command D4。
- 已完成顺序：D0 → Contracts commit → Host mapper/pin/conformance → Desktop decoder/reducer/persistence/UI → Host→Desktop source-anchored conformance → canonical gate repair/review → clean local commits。下一步才是单独 Command D4。
- 标准 composite generate/test/build 因预存 Zip Slip archive fixture 不作为验收证据；最终采用定向生成、重复 digest、63 个非 archive Node tests、完整 Go tests 与 direct TypeScript build，并在验证文档记录例外与影响。
- 当前实现没有修改 Runtime、experimental API、权限或 Tool producer；Host 的额外 active-item 数量上限未由 Contracts 冻结，保留为后续 Owner/Contracts hardening，不在 consumer 中伪造 wire constraint。
- Command D4 完成或遇到门禁/安全阻断后立即停止；Tool D4 保持 BLOCKED/NOT RUN，不得顺带启动、注册 producer 或扩展范围。
