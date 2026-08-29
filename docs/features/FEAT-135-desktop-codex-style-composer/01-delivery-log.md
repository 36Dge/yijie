# FEAT-135 整体实现与调试记录

> 当前阶段：`D4 PASS` · 实现状态：`complete` · 收口日期：`2026-08-29`

## 1. 最终实现

- 调用链保持为 `ChatComposer → ChatPage → chat.store → Desktop native durable transaction → ConversationState/Timeline`；没有新增第二套提交、附件或持久化 authority。
- store 对 create/reply 返回 sealed `ChatSubmissionResult`。页面只有在 `local_durable_accepted`、operation ID 与 draft target 匹配时清除对应草稿；no-op、reject、throw、operation mismatch 与 route race 均保留草稿和附件。
- 纯文本草稿在当前 WebView 生命周期内按 `new`/`sessionId` 隔离；附件继续由 FEAT-127 authority 管理。
- Composer 增加无依赖 auto-grow、最大高度局部滚动、validating/submitting、焦点/选择恢复 API，以及 FEAT-139 `active-turn-action` slot；既有 Stop 只作为 predecessor fallback，不新增控制语义。
- durable acceptance 后 Timeline 立即投影一个稳定 identity 的 queued 用户 Item；后续 completed/failed/interrupted 不恢复已提交草稿。
- 最终布局修复把底部 actions 放回正常布局流，并为发送动作保留独立网格列；textarea 扣除 action-row 高度预算，因此长输入不会落到操作行下方，窄 Composer 也不会挤掉发送按钮。

Desktop 最终 immutable commit：`fc52ef33cdf040d9b6e8d71bd7498811c5c38c51`。

## 2. 实际改动

| Repository | 模块 | 行为变化 | 最终状态 |
|---|---|---|---|
| `yijie-desktop` | `domain/chat-composer*`、`stores/chat.store*`、`pages/chat/ChatPage*`、`components/chat/ChatComposer*` | submission result、target draft、竞态/清理边界、auto-grow、busy/focus、稳定 action slot、最终布局修复与测试 | committed / clean |
| `yijie` | `docs/features/FEAT-135-desktop-codex-style-composer/` | D0、Contract First、实现记录、content-free canonical 与 D4 结论 | 本治理收口 commit 固化 |
| Contracts / Host / Runtime | none | 无 FEAT-135 分支、源码、配置、schema、binary 或 pin 变化 | clean / protected |

未修改 Desktop private IPC、SQLCipher schema/migration、依赖、FEAT-127 附件 authority、FEAT-128 Artifact authority、FEAT-132 ConversationState 或 FEAT-134 streaming 语义。

## 3. 调试循环

| 阶段 | 真实现象 | 根因/证据 | 修复与结果 |
|---|---|---|---|
| D0 | reply submit 可静默 `void`，页面可能误清草稿 | 页面无法判定 local durable acceptance | 新增 Desktop 内部 sealed submission result；pre-durable 失败测试 PASS |
| 第一批 | 文本草稿为 page-global，提交与路由切换可能串 target | 附件已有 target authority，文本没有 | 新增 WebView target map 与 route/operation race tests；PASS |
| 第二批 | textarea 固定高度且成功后焦点行为不稳定 | 组件没有 textarea ref/height/focus API | 增加 auto-grow、max-scroll、focus snapshot/restore；Enter/Shift+Enter/IME 回归 PASS |
| 最后一批 | durable accepted 后需唯一 queued identity；terminal failure 不应恢复草稿 | Composer success 与 Timeline authority 需要明确交接 | store/page/Timeline 集成测试覆盖 queued→failed/interrupted；PASS |
| canonical 初轮 | 长输入底部与 actions 重叠，200% 时发送动作不可见 | actions 绝对定位且与输入/窄宽度竞争空间 | 先补 2 条红测，再用正常流网格与独立发送列最小修复；Desktop commit `fc52ef33...` |
| D4 final-source | canonical stable fresh 启动并完成一次真实纯文本 Turn | final-source ready、零登录、local durable 清空与终态需要真实证据 | session ref `01a04ce5-836b-7272-a91e-252d61efd5c6`，终态 completed，正常 Cmd+Q 清理 |

历史失败不删除：初轮视觉问题是真实失败，已经转换为确定性测试并修复。Owner 随后明确豁免 AC-001 人工视觉复验，因此最终不再执行主题、窗口、zoom 视觉检查；该豁免不是 PASS。

## 4. 外部授权与调用

| 类型 | 授权 | 上限/已用 | 结果 |
|---|---|---:|---|
| 分支创建 | `yijie` 与 `yijie-desktop` FEAT-135 分支 | 2/2 | PASS |
| Desktop commits | Owner 分批授权及最终 D4 全部执行授权 | 4 个 Feature commit | PASS；未 push |
| Provider prompt | Owner 授权 D4 其余条件并在发送前再次明确“发送” | 1/1 | completed；无工具、无任务文件读写；不保存 prompt/final 正文 |
| AC-001 人工视觉复验 | Owner 明确豁免 | 0 | `WAIVED / NOT REQUIRED`，不是 PASS |
| reduced-motion | Owner 明确豁免 | 0 | `WAIVED / NOT REQUIRED`，不是 PASS |
| 破坏性/生产/public | 未授权 | 0/0 | NOT RUN |

没有强杀、故障注入、权限破坏、binary 替换、Runtime 重编译或攻击性 fixture。canonical 使用应用自身 Cmd+Q 正常退出，App/Host/Runtime 与 18081 listener 均已清理。

## 5. D4 结论与限制

- focused：3 files / 141 tests PASS；full：104 files / 872 tests PASS；lint/typecheck/build/diff PASS。
- canonical：Host `status=ok`；Runtime `0.144.6`、MiniMax-M3、ready、`experimental_api=false`；零登录直达 Chat。
- real happy path：1/1 无敏感纯文本提交进入新 session，Composer 清空，终态 completed；未保存正文。
- representative failure/retry：安全 deterministic tests 覆盖 deny/no-op/throw、mismatch、route race、duplicate submit、failed/interrupted 与同-input retry；未进行攻击或故障注入。
- AC-001 的 auto-grow、max-scroll、底部不重叠与窄布局固定发送列由测试证明；人工视觉复验和 reduced-motion 均为 Owner waiver。
- 未提交文本草稿只保证当前 WebView 生命周期；`local_durable_accepted` 不等于 Host/Runtime complete。
- D4 只表示 `demo_fast + local` 可用，不表示 public/production、逐像素 Codex Desktop 一致、已 push 或整个 Epic 完成。
