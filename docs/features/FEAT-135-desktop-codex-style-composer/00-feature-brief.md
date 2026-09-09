# FEAT-135 — Desktop Codex 风格 Composer 与新 Turn 提交 Demo Brief

> 2026-09-09 当前依赖与证据适用范围：Composer 继续保留目标草稿、operation ID 和本地 durable acceptance；queued 属于本地提交记录。后续执行只读 FEAT-132 native v7/ConversationView，不能伪造 Codex Item 或按正文匹配。原 ConversationState 集成及 stable 隔离 D4 是历史证据；日常入口为 pnpm tauri:demo-fast:app。详见[整体一致性复核](../FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。

> Profile: `demo_fast` · Exposure: `local` · Created: `2026-08-29`

## 1. 需求背景、目标与非目标

- 目标用户：在易界 AI Desktop 中向固定 Codex Runtime 提交本地新 Turn，并希望输入、附件、权限和失败恢复行为稳定可预测的用户。
- 需求背景：FEAT-132/133/134 已建立 ConversationState、Timeline 和真实流式展示，FEAT-127 已建立附件 authority；当前 Composer 仍缺少自适应高度、target-scoped 文本草稿、明确的本地接受结果和完整焦点/防重复行为。尤其已有会话的 `submitTurn()` 返回 `void` 且可静默拒绝，页面随后无条件清空 `prompt`，存在“没有真正接受却丢草稿”的确定性缺口。
- 目标：实现一个符合 Yijie UI 规范的 Codex 风格近似 Composer；让 Enter、按钮、IME、文本、附件、权限、operation ID、本地持久化接受、失败保留和焦点恢复成为一条可验证的新 Turn 提交流程。该 Feature 完成 Epic 的 G2 输入与提交体验，但不代表整个 Epic 完成。
- 用户完成后能看到或使用的真实结果：多行输入自然增长，超高后局部滚动；Enter 发送、Shift+Enter 换行、中文输入法不误发；相同请求不会重复创建 Turn；只有匹配 target 的内容在 Desktop 本地 durable acceptance 后才清空，提交前失败会保留草稿和附件。

### In scope

- `ChatComposer` 的自动增长、最大高度、局部滚动、键盘、IME、busy/disabled、可访问反馈与焦点接口。
- 页面组合层按 `new`/`sessionId` target 隔离当前 WebView 生命周期内的纯文本草稿。
- 统一按钮、Enter 和 store 的提交条件；校验项目、权限、local/Host readiness、64 KiB 文本限制和附件状态。
- 复用 FEAT-127 ordered blocks、attachment draft、operation ID 重试和 native durable transaction。
- 明确 `idle → validating → submitting → locally accepted/queued | failed`；本地接受后只清理匹配 target。
- 为 FEAT-139 保留 active-Turn action slot；不在本 Feature 定义控制命令。
- light/dark、1180×760、200% zoom、键盘、可见焦点和 reduced-motion 验证基线。

### Out of scope

- 修改、升级、重编译、替换或重新固定 `yijie-codex` Runtime；Runtime 固定在 `0ce5902ed400866be0196886bb78f693a004d68d`，`experimentalApi=false`。
- 修改 Contracts、Host、Runtime、Desktop private IPC、SQLCipher schema/migration 或跨版本 replay；一旦确需修改必须停止并重新做 Contract First 治理。
- 真实 prompt、Provider 付费调用、工具调用、任务文件读写、production/public 发布；FEAT-134 的授权和额度不继承。
- 新增依赖、React、`assistant-ui` 或第二套 Composer/状态/持久化 authority。
- active Turn 的 steer、Stop、Cancel、Retry、Continue、恢复和重连语义。
- 应用重启后恢复未提交纯文本草稿；当前范围只保证同一 WebView 生命周期内按 target 隔离。
- 人工 Codex reference evidence、版本 Freeze 或逐像素一致；采用 `codex-inspired-approximate-parity-v1-2026-08-27 / owner-approved-inference`。
- 语音、模型版本、模型推理强度配置 UI、分享、切换置顶摘要、右侧上下文面板、分支到新聊天，以及 CAP-022 / GS-006 文件修改与 Diff。

## 2. 完整主流程

1. 用户通过 canonical `pnpm tauri:demo-fast:stable` 零登录进入 Chat，选择项目以及新会话或已有会话；Composer 绑定当前 draft target，并恢复该 target 的 WebView 文本草稿与 FEAT-127 附件。
2. 用户输入多行文本或添加附件；输入框在上限内自动增长，达到上限后只在输入区纵向滚动。
3. 用户按 Enter 或点击发送；Shift+Enter 只换行，IME composition 期间不发送。两个入口读取同一 enabled rule；纯空白且无 ready 附件时不得进入提交。
4. 页面与 store 按现有 authority 校验项目、权限、local readiness、control-plane/Host readiness、文本字节和附件状态；`validating` 与 `submitting` 期间禁止重复提交，但不清空内容。
5. 同一 target 与 canonical ordered blocks 使用稳定 operation ID 调用既有 native command。前置 no-op、拒绝、异常、过期 target 或 operation mismatch 均保留匹配 target 的草稿与附件。
6. native command 确认原子本地事务并回显同一 operation ID 后，页面清空且只清空匹配 target，Timeline 出现唯一 queued 用户 Item，Composer 恢复可输入焦点。
7. 稍后的 Host/Runtime accepted、active、failed、interrupted 或 completed 继续由 FEAT-132/134 authority 展示；post-durable 失败不把正文重新塞回 Composer，以免重复发送。
8. active Turn 只使用预留的 FEAT-139 action slot；FEAT-135 不新增控制命令。

## 3. 交互与 UI

- 视觉方向、布局和关键控件：继承 Yijie Chat workspace token、Naive UI 与 Lucide registry；Composer 保持克制的圆角容器、项目/权限/附件层级、左侧附件入口和右下主发送动作。允许与 Codex Desktop 在颜色、间距、图标和局部尺寸上合理不同。
- Idle：当前 target 草稿可编辑；空白且无附件时发送不可用，有有效 blocks 时 Enter 与按钮同时可用。
- Loading：`validating` 与 `submitting` 分离；通过 busy 状态和可访问文案反馈，不伪造进度值，也不改写正文或选择。
- Success：仅在本地 durable acceptance 后清空匹配 target 并显示 queued 用户 Item；焦点回到 Composer。这不等于 Host/Runtime 已完成。
- Empty：纯空白且无 ready 附件不创建 Turn；attachment-only 完全沿用 FEAT-127 判定。
- Error：项目、权限、readiness、输入/附件限制、target race、operation mismatch 或 native failure 使用固定安全文案；pre-durable 失败保留草稿和附件。
- Retry：恢复权威条件后，相同 canonical input 重用 pending operation ID；只形成一个 durable 用户 Item。post-durable Host 失败由 Timeline/后续 Feature 处理。
- Cancel：FEAT-135 不新增 Stop/Cancel/Steer；提交在途只做防重复，active Turn 控制属于 FEAT-139。
- Focus：成功后恢复到可继续输入的 textarea；失败后焦点保持在可修复位置；组件不得因高度同步或状态切换抢走正文选择。
- Responsive/accessibility：1180×760、200% zoom、light/dark 下关键动作可见；按钮具有可访问名称，focus ring 可见，reduced-motion 下不依赖动画表达状态。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 多行输入自动增长，达到上限后只在输入区滚动；light/dark、1180×760、200% zoom 下关键输入和发送动作可见。 | 组件 scrollHeight/layout tests；canonical 主题、窗口、zoom smoke。 |
| AC-002 | Enter 与按钮同规则且一次只 submit 一次；Shift+Enter 换行；IME composition 不发送。 | Vue 键盘/按钮/IME/连续动作测试，核对 submit 次数与 draft。 |
| AC-003 | 空白且无附件不提交；文本、attachment-only、组合输入沿用 FEAT-127 blocks、限制、顺序和 target authority。 | FEAT-127 fixture 与保护 hash，覆盖 10 个/10 MiB/64 KiB/unfinished/error。 |
| AC-004 | 项目、权限、local/Host readiness、输入和附件条件在所有入口 fail closed。 | 页面/store 状态矩阵，覆盖直接 store 调用、route/context/session race。 |
| AC-005 | 重复点击、Enter 或丢响应重试最多一个 operation ID、native intent 和 durable 用户 Item；不同 input 不复用。 | store/native idempotency 与页面双提交测试。 |
| AC-006 | 仅 native durable confirmation 且 operation ID/target 匹配时清空对应草稿；所有 pre-durable 失败保留。 | 显式内部 submission result 测试，覆盖 create/reply/no-op/reject/throw/mismatch/route race。 |
| AC-007 | durable acceptance 后显示唯一 queued 用户 Item并恢复焦点；后续失败/中断不恢复已提交草稿。 | ChatPage + ConversationState/Timeline 集成测试。 |
| AC-008 | 当前 WebView 内文本草稿按 `new`/`sessionId` target 隔离；只清空匹配 target；附件与 Artifact authority 不变。 | 多会话 target switch/route race 测试和无发送 UI smoke。 |
| AC-009 | 提供 FEAT-139 action slot，但不新增任何 active Turn 后端控制语义或第二 authority。 | 组件/API 快照、scoped diff 与 Contracts/Host/Runtime negative sentinel。 |

## 5. 工程事实与边界

- 受影响仓库：`yijie`（治理文档）与 `yijie-desktop`（后续实现）。本轮不创建或修改 `yijie-contracts`、`yijie-agent-host`、`yijie-codex` 分支/文件。
- 真实入口/启动方式：后续 D4 使用 `cd ../yijie-desktop && pnpm tauri:demo-fast:stable`；本轮不启动、不发送 prompt。
- local direct-entry、固定 scope 与 public/production 鉴权边界：仅 `demo_fast/local` 零登录直达现有 Chat；不影响 public/production，不改变 auth/permission contract。
- `contract-impact`：`none`。只读 Contract First 审计确认现有 Contracts/Host/native/store 已覆盖 ordered blocks、operation idempotency 与 local durable transaction；FEAT-135 只需在 Desktop 进程内把结果表达得可判定并补充 target-scoped WebView draft。
- 权威契约源与 source-first 顺序：`yijie-contracts` OpenAPI → Host exact snapshot/mapper → Desktop private IPC/native transaction → `chat.store.ts` operation/attachment authority → `ChatPage.vue`/`ChatComposer.vue` 组合。详细矩阵见 `evidence/contract-first-capability-matrix-2026-08-29.md`。
- 接受语义：Composer `accepted` = Desktop native command 已确认原子本地持久化并回显当前 operation ID；Host HTTP 202/Runtime accepted 是后续异步事实，不是清空草稿的额外等待条件。
- 数据、密钥、付费调用和外部写操作边界：Restricted 对话数据不进入 D0 证据；付费调用、工具/文件读写、生产写入均未授权且上限为 0。
- 已有工作区改动：分支建立前 `yijie` 与 `yijie-desktop` 均为 FEAT-134 clean HEAD；生成治理包后只有 `yijie/docs/features/FEAT-135-desktop-codex-style-composer/` 为未跟踪文件，Desktop 仍 clean。
- 依赖边界：不得新增依赖；确需依赖时停止申请授权。

## 6. 推荐方案与停止条件

- Codex 推荐方案及主要取舍：保留现有 native/FEAT-127 durable transaction 与 store operation authority；把 `createSession`/`submitTurn` 在 Desktop 内部收敛为显式、可测试的 submission result，让页面只在 `accepted + matching operation/target` 时清草稿。文本草稿使用 WebView 内 target map，避免新数据库迁移；Host/Runtime 后续失败继续留在 Timeline，避免恢复正文造成重复发送。
- Contract 停止条件：若需要新增或改变 public/private IPC、SQLCipher schema、跨版本 wire、operation/replay、权限或 Runtime/Host 行为，立即停止，将 `contract-impact` 重分类为 `semantic`，并在获得新授权后从权威源开始。
- Scope 停止条件：若需要新依赖、Runtime 改动、`experimentalApi=true`、真实 prompt、模型/Provider/reasoning 配置或 active Turn 控制语义，立即停止并申请 Owner 决策。
- 30 分钟无新证据时的诊断动作：停止猜测式 Vue 补丁，建立最小 deterministic failing test，重新追踪 `Composer → Page → Store → native response` 的 target、operation ID 和 durable 边界。
- 90 分钟同一核心阻塞时的简化/替代方案：保留自动增长与显式 submission result，缩减 target draft map 为当前 session/new 两类且不扩展持久化；不得绕过 authority 或提前清草稿。
- 超过 16 小时时的缩减范围：优先交付 AC-002 至 AC-007 的提交正确性，把非关键视觉微调延后；不得删除 durable acceptance、IME、防重复、失败保留或 target 隔离这些核心 Must。
