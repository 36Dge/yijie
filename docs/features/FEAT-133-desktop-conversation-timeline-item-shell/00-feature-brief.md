# FEAT-133 — Desktop 对话 Timeline 与通用 Item 展示框架 Brief

> 2026-09-09 当前依赖与证据适用范围：当前输入为 FEAT-132 的只读 ConversationView；新对话来自 native v7/NativeDisplayBuffer，旧 ConversationState、reducer 与 legacy rollback 已删除。reasoning 正文按 FEAT-134 区分 summary/raw；原 metadata-only note 只适用于缺正文的旧档案。下文 2026-08-28 的源码哈希、旧调用链及 PASS 是历史证据，不是恢复旧机制的要求。详见[整体一致性复核](../FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。

> Profile：`demo_fast` · Exposure：`local` · Checkpoint：`D4` · Created：`2026-08-27` · Verified：`2026-08-28`
>
> 参考策略：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`

## 1. 需求背景、目标与非目标

### 背景

当前 Chat 页面分别处理用户文本、Assistant 文本、reasoning 与 Artifact，缺少由 FEAT-132
`Thread → Turn → Item → ContentBlock` 领域顺序驱动的统一信息层级。若后续每种能力继续在页面中独立
追加卡片，状态、间距、折叠、错误反馈、复制和可访问性会逐步分裂，也会诱使 Vue 页面直接解释
Host/Runtime raw wire。

FEAT-132 已建立唯一进程内领域 ViewModel。FEAT-133 只把该 ViewModel 转换为易读、可扩展、无原生
副作用的 Timeline 与 Item shell。它服务于同一个 Epic 总目标：在保留 Vue 技术栈和固定
`yijie-codex` Runtime 不变的前提下，逐步形成符合易界 UI 规范、信息层级和状态反馈接近 Codex 类桌面
对话产品的端到端体验。

FEAT-131 已废止版本/build Freeze、人工截图和逐像素基准。先前三张人工材料均已撤回，不能再作为需求、
设计、验收或 provenance。正式依据从高到低为：Owner 最新决定、易界 Design System、固定 Runtime 与
Host/Contracts 权威投影、当前 Yijie UI、工程推测。

### 目标

- 按 Turn 分组、按 FEAT-132 的 ordinal/identity 顺序展示 Timeline。
- 清楚区分用户输入、过程呈现、最终回答和安全系统 notice/error。
- 建立可复用 Item shell：header、真实状态、body、折叠控制和 action slot。
- 安全展示纯文本、Markdown 子集、代码、列表、表格与行内代码，不执行 HTML/script。
- 统一文本选择、复制、复制失败反馈、折叠、键盘与焦点行为。
- 为 empty、loading、ready、error、permission denied、unknown 和 interrupted/cancelled 提供明确状态。
- 保留 FEAT-127 附件和 FEAT-128 Artifact authority，不新建第二套内容或显示 authority。
- 所有结果继续服务完整 Epic；FEAT-133 单独完成时只能表述“Timeline 框架局部完成，Epic 尚未完成”。

### 非目标

- 不修改、升级、重编译、替换或同步 `yijie-codex` Runtime、binary、schema 或 pin；保持 Runtime
  `0.144.6`、固定 commit 和 `experimentalApi=false`。
- 不修改 `yijie-contracts`、`yijie-agent-host`、Desktop private IPC、`src-tauri`、数据库、持久化、
  Tauri capability、模型、prompt、Provider 或 Agent 决策。
- 不实现 FEAT-134 流式分层、FEAT-136 Command 详情、FEAT-144 Tool、FEAT-152 权限（FEAT-137 永久退役）、FEAT-139 Turn 控制、
  FEAT-140/142 复杂恢复与重连或 FEAT-141 长对话滚动策略。
- 不重构 Sidebar、Composer、附件存储或 Artifact authority。
- 不引入 React、`assistant-ui`、第二套通用 UI/Markdown 组件库；新增依赖必须另获 Owner 批准。
- 不逐像素复制 Codex Desktop，不复制其品牌或私有素材，不声明版本专属 observed parity。
- 不实现 8 项 `intentional product difference`：语音、模型版本信息、模型推理强度配置/档位 UI、分享、
  切换置顶摘要、显示侧边面板、分支到新聊天、GS-006 文件修改与 Diff。
- GS-006 的排除不删除既有 Artifact，但 Artifact 不得包装或描述为 FileChange/Diff。
- 不发布 public/production，不执行生产写入、付费调用或破坏性操作。

## 2. 完整用户流程与业务规则

1. 用户通过 canonical `cd ../yijie-desktop && pnpm tauri:demo-fast:stable` 零登录直达 Chat，选择新
   Thread 或已有会话；固定 local owner/tenant/capability 只用于 ADR-0018 本机 direct-entry。
2. Timeline selector 只读取 FEAT-132 领域 ViewModel，按 Turn ordinal 与 Item ordinal/identity 生成稳定
   展示模型；组件不接触 raw event method、payload、数据库或原生 command。
3. Timeline 依次展示用户输入、允许的过程呈现、最终回答与安全 notice。progress 是原生 Turn lifecycle
   的只读呈现，error/warning 只按已知来源范围展示；仅 thread 范围的 notice 保留在会话层；组件不伪造新的领域 Item。
4. Item header 只显示 ViewModel 中真实存在的类型、状态、时间或耗时；缺少字段时隐藏，不从到达时间、
   DOM 顺序或文案推测。
5. 用户可通过键盘或指针展开/收起允许折叠的过程内容，复制文本/代码；shell 仅发出显式事件，上层
   action handler 决定是否执行已批准操作。
6. 最终回答永不默认折叠。unknown、error 与 permission denied 只影响对应位置，固定安全文案不得泄露
   raw payload、资源存在性、路径、secret 或用户正文。
7. 外链不自动打开；没有已批准的安全 handler 时只显示、选择或复制，不交给系统。
8. FEAT-127 附件与 FEAT-128 Artifact 使用既有 identity 和 authority；Timeline 不复制正文、资源或状态。

稳定规则：

- 视觉顺序必须来自领域 ordinal/identity，不能用 DOM 到达顺序、时间猜测或 raw wire method 决定。
- 折叠状态按稳定 Item ID 管理；重新 hydrate 不得把一个 Item 的 disclosure 状态转移给另一个 Item。
- 只有过程类展示允许依据已确认类型与内容长度默认折叠；最终回答、错误摘要和 header/status 始终可见。
- 复制只能读取展示文本，不修改消息、领域状态或选择；成功/失败反馈必须与真实 clipboard 结果一致。
- 安全内容 renderer 不使用 `v-html`，不创建可执行节点，不自动导航；代码和表格只允许局部横向滚动。
- 新建 Thread 不显示虚假示例消息；加载已有历史时不以空白覆盖已确认内容。
- Yijie Chat Pattern 中原有“右侧上下文面板”描述与 Owner 的“显示侧边面板不实现”冲突时，Owner 最新
  排除决定优先；本 Feature 不新增或恢复侧边面板。

## 3. 交互与 UI

### 视觉方向

采用 `owner-approved-inference` 的 Codex 风格近似方案：以易界 token、Naive UI、Lucide registry、标准
密度和当前 Chat 组件能力为准；Timeline 保持适度留白，用户输入、过程项与最终回答形成明确层级，过程
项克制且可折叠，最终回答保持最高阅读优先级。允许颜色、间距、图标、文案与局部布局不同，不依赖已撤回
的 Codex Desktop 人工证据。

### 状态行为

- Idle：Thread 已加载且无 active Turn；历史可读，Item action 只显示当前可用的无副作用操作。
- Loading：初次加载显示稳定 skeleton；刷新已有历史时保留已确认内容和阅读位置。
- Success：按领域顺序展示完整内容；状态同时使用文字/语义，不只使用颜色。
- Empty：显示如何开始新任务的中文说明，不生成虚假消息；Composer 仍由既有页面/FEAT-135 管理。
- Error：错误位于对应 Turn/Item 或 Timeline 状态中，不全屏吞掉可读历史；使用固定安全文案。
- Permission denied：显示通用不可用状态，不泄露目标资源是否存在；没有安全恢复权时不展示伪重试。
- Retry：只有上层已有安全恢复意图时显示“重新加载/重试”；shell 只发事件，不直接调用 Host/Tauri。
- Cancel：本 Feature 不新增 Stop/Cancel 控件；若 ViewModel 已是 interrupted/cancelled，保留已确认内容并
  显示终态，实际控制由 FEAT-139 承接。
- Unknown：显示“此内容类型暂不支持”与安全诊断 code，不显示 raw payload，其他 Item 继续渲染。
- Keyboard/A11y：header、折叠和复制可聚焦；焦点顺序等于视觉顺序；图标按钮有可访问名称；状态反馈
  使用合适 live region 且不造成重复播报。
- Theme/Viewport：light/dark、`1180×760`、200% zoom 和 reduced motion 下关键内容不重叠；主体不产生
  横向滚动，代码/表格内部可以局部滚动。

### 推荐组件边界

- `conversation-timeline` selector/ViewModel：只从 FEAT-132 只读 ConversationView 派生展示数据，纯函数、确定性、可测试。
- `ChatTimeline`：组织 Thread 状态和 Turn group，不执行 I/O。
- `ChatTurnGroup`：呈现 Turn 层级、状态与有序 Item。
- `ChatTimelineItemShell`：提供 header/status/body/disclosure/action slot。
- `ChatSafeContent`：把受限内容树渲染成 Vue 节点，不使用 `v-html`。
- 用户、Assistant、process、unknown/error 基础 renderer：只消费类型化展示模型。
- clipboard、retry、link 等操作通过显式事件和注入 adapter 交由上层；组件本身不发起 Host/Tauri 副作用。

推荐先实现受限、类型化 Markdown 子集，避免新增依赖。如果真实需求证明无法安全满足 AC-002，停止并
请求一次明确的依赖选择/批准，不能偷偷使用 docs 的传递依赖或直接插入 HTML。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 多 Turn、多 Item 的视觉顺序与 FEAT-132 领域顺序一致，用户与 Assistant/过程/系统角色清楚 | selector + Vue DOM 顺序/identity 测试；canonical history smoke |
| AC-002 | Markdown、代码、表格安全显示；不执行 HTML/script、不用 `v-html`、不自动打开 URL | 良性惰性 markup/text 组件测试；无可执行节点/隐式导航断言 |
| AC-003 | 长过程 Item 折叠/展开后 header/status 可见，最终回答永不默认隐藏 | disclosure/长度阈值/键盘/final non-collapsible 测试 |
| AC-004 | unknown Item fail-soft；不崩溃、不输出 raw payload，其他 Item 正常 | unknown ViewModel、固定 code、canary 与相邻 Item 测试 |
| AC-005 | 文本/代码复制成功或失败反馈准确，内容与选择不变 | clipboard success/rejection、live region、焦点与正文快照测试 |
| AC-006 | empty/loading/error/permission denied 有明确文案及适用恢复入口 | 状态矩阵测试；canonical empty/history smoke；安全领域权限状态 |
| AC-007 | light/dark、1180×760、200% zoom 与键盘下无关键重叠/主体横滚，焦点可见、按钮有名称 | a11y/focus 测试与 canonical Desktop 人工 smoke |
| AC-008 | FEAT-127 附件和 FEAT-128 Artifact 不丢失、不重复、不产生第二 authority | attachment/artifact 集成回归与 authority 路径审阅 |

D0 建立时所有 AC 均为 `pending`。2026-08-28 的 D4 实现、focused/full checks、真实 canonical UI 和
代表性安全失败/恢复均已完成，8 条 AC 原子更新为 `pass`；逐项证据见 `02-verification.md`。

## 5. 工程事实与 Contract First

- 正式受影响仓库：`yijie`（Feature Package）与 `yijie-desktop`（后续 selector/components/tests）。
- 真实入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`。
- 前置：FEAT-131 reference policy 与 capability/golden 索引；FEAT-132 D4 已完成并提供唯一领域 VM。
- 稳定参考：`BASIS-001`、`BASIS-004`，`CAP-008/009/010/011/015/023/029/030/031`，
  `GS-001/002/013`；`GS-006` 仅作为 Owner 排除的 negative sentinel。
- `contract-impact=none`：推荐方案只在 Vue 进程内从 FEAT-132 ViewModel 派生展示模型，不改变跨进程、
  跨仓、跨版本、持久化或重放语义。FEAT-127/128 authority 也保持不变。
- source-first 停止条件：若 ViewModel 缺少排序、角色、状态或安全内容字段，必须停止，回到 FEAT-132 或
  对应权威源重新分类/治理；禁止在 Vue 中读取 raw wire、猜时间/耗时或复制影子 DTO。
- local direct-entry 只在固定本地 scope 生效；public/production 鉴权、审批和审计边界不变。
- 数据边界：只使用无敏感领域 fixture 和既有无敏感历史；不把 prompt、raw payload、路径、secret、PII
  或真实商家数据写入 fixture、日志、截图或文档。
- 外部授权：付费调用、破坏性操作、生产写入均为 `false/0`；FEAT-132 的 2/2 prompt 授权已耗尽且
  不可转用于 FEAT-133。本 Feature 当前不需要新 prompt。
- 安全测试只能使用正常、非破坏性方法；不强杀、不故障注入、不破坏权限、不替换二进制、不使用攻击性
  fixture。无法安全执行的验收必须如实标记未执行并说明影响。

## 6. D0 历史工作区隔离记录（已被后续授权取代）

D0 建立时采用**路径级逻辑隔离**，尚无独立 worktree 或新分支授权；当时保留 FEAT-131 分支，使用精确
HEAD、clean-start、写入 allowlist 和保护哈希控制范围。随后 Owner 已授权创建两个 FEAT-133 分支并提交
D0 基线，因此下表只作为 2026-08-27 的历史证据，不描述 D4 当前分支或写入范围。

修改前五个核心仓库均 clean：

| Repository | Branch | Baseline HEAD | D0 写入权限 |
|---|---|---|---|
| `yijie` | `feat/feat-131-desktop-codex-parity-baseline` | `aed49b78f21c264bb13c05c1976f11f7fc14b520` | 仅 FEAT-133 正式包 |
| `yijie-desktop` | `feat/feat-131-desktop-codex-parity-baseline` | `f96fe05ca81d6bc7fac97ecbf81bcbab32b8aaa0` | 无；本 D0 全仓只读 |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | 无；固定只读 |
| `yijie-contracts` | `feat/feat-129-desktop-skill-marketplace` | `164b14f609537d727a52326832da04430aecc4ab` | 无 |
| `yijie-agent-host` | `feat/feat-129-desktop-skill-marketplace` | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | 无 |

D0 exact allowlist：

- `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/feature.yaml`
- `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/00-feature-brief.md`
- `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/01-delivery-log.md`
- `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/02-verification.md`
- `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/evidence/workspace-isolation-baseline-2026-08-27.md`

`yijie-desktop` D0 allowlist 为空。尤其 [ChatPage.vue] 保持 Git blob
`ea2c3a1e606d687981d7a11fec3ac7196baa56f9`、SHA-256
`b89e1204864656de800c5d2682100116b2784ebd17b48534b705ba58bb8dfef1`。这是 D0 阶段保护约束，
不把“永远不能组合 Timeline”误写成整个 Feature 的永久非目标。

完整 11 仓基线、更多保护哈希、允许/禁止范围和停止条件见
`evidence/workspace-isolation-baseline-2026-08-27.md`。

D4 收口状态：治理演进基线为 `yijie@a154fcea9fc6073af30ac14b3ada8eaf490f754b`，最终 Desktop
实现为 `yijie-desktop@af38353694c3eb045365b7f3450ffc8a95aaf8a1`；两个仓库均位于
`feat/feat-133-desktop-conversation-timeline-item-shell`。selector、独立组件以及页面组合/交互/缩放/
测试已有三个 scoped Desktop commit，本治理包由包含本文的 FEAT-133 收口提交固化。`ChatPage.vue` 的
只读限制只属于 D0，后续实现已按 Owner 任务做最小组合。没有执行 push、reset、stash 或 clean。

## 7. D0 历史实施计划与持续停止条件

D0 当时推荐按一个连续 Feature 实施，不建立治理切片；以下 1–7 步现已全部完成：

1. 只读对账 FEAT-132 ViewModel 与 FEAT-127/128 authority。
2. 先补纯 selector 和基础 Item/state 组件测试。
3. 实现 Timeline、Turn group、Item shell、安全内容树和基础 renderers。
4. 接通 disclosure、clipboard 与显式 action events；不让组件执行 I/O。
5. 以最小页面组合接入既有 Chat，保持附件、Artifact、Composer 和 Sidebar authority 不变。
6. 运行 focused/full checks、独立只读审查与 canonical no-prompt UI smoke。
7. 所有 Must AC 在一次 fresh run 中通过后再更新 D4；结论仅为“Timeline 框架局部完成，Epic 尚未完成”。

立即停止并重新治理的条件：

- 出现 allowlist 外 diff、未知工作区改动或保护 HEAD/hash 漂移。
- 需要在 Vue 解释 raw wire，或需要修改 FEAT-132 domain/adapter/store、Desktop IPC、`src-tauri`、数据库、
  Host、Contracts 或 Runtime 才能满足 Must AC。
- 需要新增 Markdown/UI 依赖、Tauri capability、原生 URL opener 或第二套 authority，且尚未获批。
- 触及 8 项 Owner 排除能力，尤其 GS-006 File modification & Diff。
- 需要真实 prompt、付费调用、生产写入、破坏性操作、分支、worktree、stash、commit 或 push 的新授权。
- 测试只能通过降低断言、使用攻击性 fixture、破坏权限、替换二进制或故障注入。
- 30 分钟没有新事实时回到 FEAT-132→selector→component 单链路；90 分钟同一阻塞时保留最小文本/
  unknown/error shell 并关闭非核心花活；240 分钟核心路径不通时缩小 MVP；16 小时未 D4 时停止并重新定范围。

## 8. D0 与 D4 结论

2026-08-27，Owner 要求先完成正式 D0 包且不直接修改 `ChatPage.vue`；产品/UX、Must AC、Contract First、
授权和隔离边界据此登记为 `D0 Product/UX Ready`。该限制只属于 D0 阶段。

2026-08-28，Owner 允许进入完整 FEAT-133 实现，并接受以下历史 reasoning 边界：默认 Timeline 只展示
FEAT-132 已持久化的 identity、ordinal、角色和 lifecycle 元数据；若 completed reasoning 没有 ContentBlock，
显示固定提示“此过程仅包含状态元数据；详情未进入当前对话投影。”active/streaming 空 reasoning 不显示该
提示。默认路径不调用旧 `loadReasoning`，不在 FEAT-132、adapter、store 或 raw wire 中补字段，也不建立第二
authority。由此不能声明“历史 reasoning 正文已迁移”或“正文与 Codex 完全一致”。

D4 已完成纯 selector、独立 Timeline/TurnGroup/ItemShell/SafeContent、受限 Markdown、稳定 disclosure、
注入式 clipboard、页面最小组合、FEAT-127/128 authority slots、确定性 permission denied、显式 legacy
rollback 和前端 80–200% 缩放。rollback 只有
`VITE_YIJIE_LEGACY_CHAT_TIMELINE_ROLLBACK_ENABLED=true` 才启用；unset、其他值以及 canonical build/startup
均使用新 Timeline，分页或 selector 暂时为空不会切回旧 renderer。

最终准确结论：**FEAT-133 D4 本地可用，Timeline 框架局部完成；完整 Epic 尚未完成。**

[ChatPage.vue]: /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/pages/chat/ChatPage.vue
