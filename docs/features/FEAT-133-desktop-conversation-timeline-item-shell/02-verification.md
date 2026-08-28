# FEAT-133 Demo 验证

## 1. 当前门禁状态

| Gate | Result | 说明 |
|---|---|---|
| D0 | PASS | 正式 Brief、Must AC、Contract First 与双仓隔离基线已提交 |
| D4 | PASS | 实现、focused/full checks、代表性安全失败与 fresh canonical UI 均完成 |
| DP | N/A | `exposure=local`，不提供公网入口 |

D4 的准确结论是“Timeline 框架局部完成，Epic 尚未完成”，不是 Production Ready，也不是 Codex Desktop
逐像素或历史 reasoning 正文 parity。

## 2. D4 Focused 与 full checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie-desktop` | `pnpm vitest run src/domain/conversation-timeline.test.ts src/domain/conversation-timeline-copy.test.ts src/domain/ui-zoom.test.ts src/api/chat-clipboard-adapter.test.ts src/authorization/chat-timeline-ui-config.test.ts src/components/chat/ChatCopyAction.test.ts src/components/chat/ChatSafeContent.test.ts src/components/chat/ChatTimelineItemShell.test.ts src/components/chat/ChatTurnGroup.test.ts src/components/chat/ChatTimeline.test.ts src/pages/chat/ChatPage.test.ts src/App.test.ts` | 0 | PASS：12 files / 80 tests | 2026-08-28 |
| `yijie-desktop` | `make lint` | 0 | PASS：Contracts generation check、ESLint、vue-tsc、cargo fmt、cargo clippy | 2026-08-28 |
| `yijie-desktop` | `make test` | 0 | PASS：94 TypeScript files / 748 tests；Rust 265 PASS、3 条既有条件测试 ignored | 2026-08-28 |
| `yijie-desktop` | `make build` | 0 | PASS：Vite production build，5308 modules | 2026-08-28 |
| `yijie-desktop` | `git diff --check` | 0 | PASS：无 patch whitespace error | 2026-08-28 |
| `yijie-codex` | `git rev-parse HEAD && git status --short` | 0 | PASS：`0ce5902…`，clean，Runtime 未修改 | 2026-08-28 |
| `yijie` | strict D4 checker + direct claims audit + `git diff --check` | 0 | PASS：schema v3、文档、D4 范围与声明一致 | 2026-08-28 |
| `yijie` | `pnpm feature:audit -- --base-ref a154fcea… && pnpm lint && pnpm test && bash -n scripts/*.sh` | 0 | PASS：12 packages claims；10 仓治理；48 tests；Shell syntax | 2026-08-28 |

完整 Desktop test 仍会输出两类既有非失败诊断：happy-dom worker module loading warning，以及 Vite 单 chunk
超过 500 kB 的 warning；命令最终 exit 0，未隐藏或改写这些结果。

## 3. Must AC 证据

| AC | Result | 实际证据 |
|---|---|---|
| AC-001 | PASS | selector 测试覆盖 Turn/Item ordinal、stable identity、重复 identity、角色/状态映射；Timeline DOM tests 与 canonical 既有 1 user + 1 assistant 历史顺序一致 |
| AC-002 | PASS | `ChatSafeContent` tests 覆盖受限 Markdown、代码、列表、表格、行内代码、惰性 HTML/URL；无 `v-html`、可执行节点或自动导航；无新增依赖 |
| AC-003 | PASS | TurnGroup/ItemShell tests 覆盖过程 disclosure、稳定 Item ID、键盘、重渲染和 final non-collapsible；completed 空 reasoning 显示固定元数据 note，active 空 reasoning 不显示 |
| AC-004 | PASS | unknown/error tests 使用固定 code 与安全 canary，raw payload 不进入 DOM，相邻 Item 正常；canonical 页面未崩溃 |
| AC-005 | PASS | 注入 clipboard adapter 的 success/rejection/retry tests 覆盖文本/代码、live region、正文/选择/焦点保持；canonical 指针与 Tab→Return 均得到“文本已复制。”且焦点留在复制按钮 |
| AC-006 | PASS | 组件/页面状态矩阵覆盖 empty/loading/error/permission denied/unknown 与安全恢复；permission 只取既有 control plane/context；canonical 观察新建 empty、queued waiting 与 completed history |
| AC-007 | PASS | App/zoom/a11y tests 与 canonical light/dark、1180×760、100→200%、键盘 smoke；200% composer 可见，只有对话区单轴滚动，主体无横向滚动，按钮有可访问名称 |
| AC-008 | PASS | ChatPage/Timeline slots tests 复用 FEAT-127 attachment reference 和 FEAT-128 exact artifactId/context/session/turn authority；未复制正文/资源 authority，Artifact 未被包装成 GS-006 Diff |

## 4. Canonical 启动与真实 UI Smoke

| Check | Command/steps | Actual result | Result |
|---|---|---|---|
| Startup/readiness | `cd ../yijie-desktop && pnpm tauri:demo-fast:stable` fresh build/start；使用 FEAT-131 stable config；默认 rollback flag 未设置；最后应用自身 Cmd-Q | 零登录进入 Chat；已有无敏感历史与 composer 可用；stable `experimentalApi=false` 边界未变；launcher exit 0 | PASS |
| Existing history | 只打开 FEAT-132 已存在的三条历史；不输入/发送 prompt | completed 1 user + 1 assistant 正常显示；queued history 显示等待；新建页 empty 不生成虚假消息 | PASS |
| Clipboard | 指针点击 Assistant copy；点击标题后 Tab 到 user copy 并 Return；200% 再 Tab/Return | live region 均出现“文本已复制。”；键盘焦点保持在复制按钮 | PASS |
| Viewport/theme | 窗口校准为 1180×760；切换 light/dark；Cmd+plus 五次到 200%，Cmd+0 复位 | 100/120/140/160/180/200% 逐级可观察；200% composer 可见、无主体横滚；light/dark 均正常 | PASS |
| Normal cleanup | 每次 canonical 与系统设置均走应用自身 Cmd-Q | canonical launcher exit 0；没有强杀或故障注入 | PASS |

FEAT-133 没有真实 prompt 授权，实际发送 0 次；没有由新 Turn 触发的工具调用、Agent 项目文件读写、
Provider 付费调用或自动重试。

现有三条 canonical 历史都没有 reasoning Item，因此没有真实历史 reasoning 截图。Owner 接受的固定元数据 note
由组件和页面测试验证；D4 不把“没有样本”伪写为 canonical 已观察到 reasoning 正文或 note。

## 5. UI Artifact

| Artifact | 尺寸/用途 | SHA-256 |
|---|---|---|
| `evidence/canonical-light-1180x760-2026-08-28.jpeg` | 1180×760，默认新 Timeline、完成历史、composer | `f45e13f9a03969162bc069bdb069f002731c0ef709f1bdecded798027caea989` |
| `evidence/canonical-zoom-200pct-1180x760-2026-08-28.jpeg` | 1180×760，200% 重排、composer 可见 | `07adf77da067da80fcd4d84042dd5c47e7b64a82cc7e2e9b818946fc446149cf` |
| `evidence/canonical-dark-1180x760-2026-08-28.jpeg` | 1180×760，暗色新 Timeline、同一完成历史 | `1368da2cc6fabf7ffa8dbb5b6656043cdc517fdc8c557845454fa537265bee61` |

这些 Artifact 只记录 Yijie canonical；没有采集、恢复或引用已撤回的 Codex Desktop 人工证据。

## 6. 代表性安全失败与恢复

- clipboard adapter rejection：固定失败 live feedback，并允许正常重试；不改正文、选择或领域状态。
- unknown Item：固定脱敏占位与诊断 code；不输出 raw payload，其他 Item 继续渲染。
- permission denied：既有确定性 control plane/context authority 驱动；没有破坏真实文件权限或伪造 FEAT-132。
- selector-null/history loading/error：使用新 Timeline 的同步/empty/error 状态，不自动切 legacy renderer。
- inert markup/URL：按文本或受限节点展示，不执行 script/HTML，不自动打开外链。
- 所有失败测试使用正常、非破坏性的无敏感 fixture；未强杀、未故障注入、未破坏权限、未替换 executable。

## 7. 边界与 Diff 复核

- `yijie`、`yijie-desktop` 均在 `feat/feat-133-desktop-conversation-timeline-item-shell`；最终 Desktop
  页面组合/交互已由 `af38353694c3eb045365b7f3450ffc8a95aaf8a1` 固化，D4 治理包由包含本文的收口
  commit 固化；未执行 reset、stash、clean 或 push。
- FEAT-132 `conversation-state.ts`、adapter、store 的 SHA-256 与 D0 完全一致；`package.json`、lockfile 与
  `src-tauri` tree 也一致，没有新依赖或 capability。
- `yijie-codex` 位于 `develop@0ce5902…` 且 clean；Contracts、Host、Runtime、private IPC、数据库与持久化均
  未修改。
- 新 Timeline 默认开启；legacy rollback 仅 exact `true` 可达，canonical build/startup 为 false；分页与
  selector-null 不切 renderer。
- 三轮独立只读审查分别覆盖整体实现、historical reasoning boundary 与 zoom/reflow；最新 diff 未发现
  P0/P1/P2。

## 8. 已知限制

- historical reasoning 只有 identity/order/lifecycle 元数据和固定缺失提示，不含正文、lazy load 或逐 Item
  不完整详情；不能声明该正文已经迁移或与 Codex 一致。
- canonical 没有真实 reasoning Item 样本；这项只有自动化与静态边界证据。
- 200% 时较长对话依靠对话区纵向滚动；代码/表格保留组件内局部横向滚动，这是预期边界。
- public/production、签名、公证、完整性能/安全专项不在 local D4。
- GS-006 File modification & Diff，以及语音、模型版本、模型推理强度、分享、置顶摘要切换、侧边面板和
  分支到新聊天均未实现。

## 9. 结论

- `D0` 产品/UX 可实施：PASS。
- `D4` 本地真实可用：PASS。
- `DP` 公开 Demo 可用：N/A。
- 验证时间：`2026-08-28T01:55:39+08:00`。
- 最终事实：**Timeline 框架局部完成，Epic 尚未完成。**
