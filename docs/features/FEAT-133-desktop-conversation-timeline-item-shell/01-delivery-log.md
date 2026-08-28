# FEAT-133 整体实现与调试记录

> 当前阶段：`D4 PASS` · 实现状态：`complete` · 记录日期：`2026-08-28`

## 1. 最终实现方案

- 数据单链路：FEAT-132 `ConversationState` → `conversation-timeline` 纯 selector/ViewModel →
  `ChatTimeline` → `ChatTurnGroup` → `ChatTimelineItemShell` → `ChatSafeContent`。
- selector 只消费 FEAT-132 领域对象，保持 Turn/Item ordinal、稳定 identity、角色和真实状态；没有读取 raw
  wire、数据库、Tauri command 或 Host payload。
- 安全内容树以 Vue 节点展示纯文本、段落、标题、强调、行内代码、代码块、列表和表格；未使用
  `v-html`，未自动打开 URL，也未新增 Markdown/UI 依赖。
- 过程 Item 以稳定 Item ID 管理 disclosure；最终回答永不默认折叠。unknown/error 使用固定脱敏文案，
  相邻 Item 不受影响。
- clipboard 通过注入的 `ChatClipboardAdapter` 和 `ChatCopyAction` 完成文本/代码复制；Timeline 不直接访问
  Tauri/Host。成功与拒绝均进入可访问 live region，正文、选择和焦点保持不变。
- `ChatPage.vue` 最小组合新 Timeline；FEAT-127 attachment reference 与 FEAT-128 Artifact exact authority
  通过 typed slots 接入。permission denied 只读取既有 `controlPlane`、`lastErrorCode` 与 context
  `allowedActions`，没有在 Vue 伪造领域权限。
- 旧 renderer 只保留为显式 rollback：仅环境值精确为 `true` 时启用；默认、canonical、selector-null 和分页
  均不自动进入旧路径。
- Tauri WebView 的原生缩放需要新增 capability，属于禁止的 `src-tauri` 边界。因此用无依赖前端
  Cmd/Ctrl `+`、`-`、`0` 实现 80–200% 缩放，并反向折算 viewport/minimum；180/200% 复用既有窄屏
  chat sidebar，使 1180×760 下 composer 可见且主体不产生横向滚动。

## 2. Owner reasoning 决策

2026-08-28，Owner 明确接受“历史 reasoning 仅显示元数据和固定缺失提示”。最终规则为：

- completed reasoning 且 `contentBlocks.length === 0` 时显示固定 note：
  “此过程仅包含状态元数据；详情未进入当前对话投影。”
- active/streaming 空 reasoning 不显示“历史缺失”提示。
- 默认 Timeline 不调用 `loadReasoning`，不把旧 `ChatReasoningItem` 拼进 FEAT-132 state，也不新增 lazy body
  authority、adapter、store 或 raw wire 字段。
- legacy 分支只有显式 rollback 开关可达。
- canonical 现有三条无敏感历史都没有 reasoning Item，所以真实 UI 没有可展示的 reasoning 样本；该规则由
  TurnGroup 与 ChatPage 组件测试证明。D4 不宣称历史 reasoning 正文已迁移或与 Codex 正文等价。

## 3. 工作区与实现记录

D0 于 2026-08-27 在两个目标仓建立独立分支并提交基线；实现沿用同名分支：

| Repository | Branch | D4 基线/最终引用 | D4 状态 |
|---|---|---|---|
| `yijie` | `feat/feat-133-desktop-conversation-timeline-item-shell` | 演进基线 `a154fcea9fc6073af30ac14b3ada8eaf490f754b` | D4 文档与 3 个截图由包含本文的治理收口 commit 固化 |
| `yijie-desktop` | `feat/feat-133-desktop-conversation-timeline-item-shell` | 最终实现 `af38353694c3eb045365b7f3450ffc8a95aaf8a1` | 页面组合、交互、缩放与测试已提交，worktree clean |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | clean / fixed / 未修改、升级、重编译或替换 |

FEAT-133 Desktop 已有三个 scoped implementation commit：

- `cf61a8c feat(feat-133): add conversation timeline view model`
- `4ef3f57 feat(feat-133): add standalone conversation timeline components`
- `af38353 feat(feat-133): integrate timeline interactions and accessibility`

Owner 已授权正式收口：页面组合与交互由 `af38353694c3eb045365b7f3450ffc8a95aaf8a1` 固化，D4 治理结果由
包含本文的治理收口 commit 固化。未执行 push、reset、stash、clean，也未覆盖用户改动。FEAT-132 保护哈希
保持 D0 值：

- `conversation-state.ts`：`148a3f573f62139175906fb2f5073eab60bc91ceab12135522def56252a99490`
- `chat-conversation-adapter.ts`：`834094b683e63e26fddf65ac03475fe7e73097ae3dc3f74ead02574790e273a8`
- `chat.store.ts`：`89832e87dccc0f53cf379a85ed3eae6ca3ebaae9e2839aa298a042d33f545f4a`
- `package.json` / `pnpm-lock.yaml`：`8316e5…7d4eced7b9` / `e48e21…72f00cc89`
- `src-tauri` Git tree：`4d59b67cc602f76f0b9603614d0057741c97a109`

## 4. 关键调试循环

| 现象 | 根因/边界 | 修复 | 结果 |
|---|---|---|---|
| permission denied 不在 `ConversationTimelineViewModel` | 权限 authority 属于既有页面 control plane/context | 只在页面组合层读取确定性现有来源；不改 FEAT-132 | 状态矩阵与页面 tests PASS |
| completed 历史 reasoning 没有正文 | FEAT-132 当前持久化投影只有元数据 | 按 Owner 决策显示固定 note；不 lazy load、不建第二 authority | 边界 tests 与独立审查 PASS |
| 默认 Timeline selector 暂空时可能误入旧 renderer | 旧模板最初与 `v-else` 绑定 | legacy 分支改为显式 exact-true rollback；selector-null 显示新同步/empty 状态 | 页面 tests PASS |
| Tauri WebView Cmd+plus 不缩放 | 原生 zoom 需要新增 Tauri capability，超出允许范围 | 前端纯规则 20% 步进到 200%，不改 `src-tauri` | domain/App tests 与 canonical PASS |
| 初版 root CSS zoom 在 200% 放大 1180×760 minimum 与 `100vh` | viewport unit/media query 不会自动反向折算 | 动态折算 viewport/minimum，180/200% 复用 196px chat sidebar | composer 可见；仅保留对话区滚动，无主体横滚 |

没有通过强杀、故障注入、权限破坏、二进制替换或攻击性 fixture 制造失败。canonical 每次都使用应用自身
Cmd-Q 正常退出，launcher exit 0。

## 5. 外部授权与实际调用

| 类型 | 上限 | 已用 | 结果 |
|---|---:|---:|---|
| FEAT-133 付费/Provider prompt | 0 | 0 | 未授权且未执行；只读取 FEAT-132 既有无敏感历史 |
| 工具调用或项目文件读写（Agent Turn） | 0 | 0 | 未执行任何新 Turn |
| 破坏性操作/生产写入 | 0 | 0 | 未授权且未执行 |
| Runtime/Contracts/Host 修改 | 0 | 0 | 未执行 |

## 6. 验证结果摘要

- FEAT-133 focused：12 files / 80 tests PASS。
- Desktop full：`make lint && make test && make build` PASS；94 TypeScript test files / 748 tests；Rust
  265 PASS、3 条既有条件测试 ignored；Vite production build PASS。
- canonical：`pnpm tauri:demo-fast:stable` fresh build/start PASS；默认 rollback=false，
  `experimentalApi=false` stable 入口；没有发送 prompt。
- 真实 UI：light/dark、1180×760、100→120→140→160→180→200%、pointer copy、keyboard Tab/Return、
  live feedback、empty/history/waiting 状态 PASS；正常退出 PASS。
- 独立只读复核：Timeline/reasoning/zoom 最新 diff 未发现 P0/P1/P2。

## 7. 当前限制

- canonical 三条既有历史没有 reasoning Item；固定元数据缺失提示只有自动化证据，没有真实历史截图。
- 历史 reasoning 正文、lazy load、逐 Item “正文不完整/不可用”详情不在 FEAT-133；不能据此声明正文 parity。
- 200% 时可视对话区自然缩小，用户通过该区域的单轴滚动访问较长内容；代码/表格仍允许局部横向滚动。
- public/production、签名、公证、性能与完整安全专项不在 `demo_fast + local` D4。
- GS-006 File modification & Diff 及其余七项 Owner 排除功能仍不实现。

最终结论：**Timeline 框架局部完成，Epic 尚未完成。**
