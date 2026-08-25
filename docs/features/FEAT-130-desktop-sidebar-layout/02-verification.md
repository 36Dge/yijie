# FEAT-130 Demo 验证

## 1. 自动化与构建

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| yijie-desktop | `pnpm exec vitest run`（修改前 focused 基线） | 0 | PASS：6 files / 44 tests | 2026-08-25 |
| yijie-desktop | `pnpm exec vitest run src/stores/chat.store.test.ts src/components/chat/ChatSidebarTree.test.ts src/components/yijie/YjSidebar.test.ts src/components/chat/ChatComposer.test.ts src/App.test.ts` | 0 | PASS：5 files / 81 tests，含 read-only、权限撤销、axe、跨租户/selection 迟到结果、删除后精确路由与 selector 视觉 token | 2026-08-25 |
| yijie-desktop | `pnpm lint`、target ESLint、`vue-tsc --noEmit` | 0 | PASS | 2026-08-25 |
| yijie-desktop | `cargo fmt --check`、`cargo clippy --all-targets -- -D warnings` | 0 | PASS | 2026-08-25 |
| yijie-desktop | `pnpm exec vitest run`（排除 production-hardened 及两个受外部脏 Contracts 影响的 pin tests） | 0 | PASS：61 files / 454 tests | 2026-08-25 |
| yijie-desktop | `cargo test --manifest-path src-tauri/Cargo.toml` | 0 | PASS：246 passed / 0 failed / 3 environment integrations ignored | 2026-08-25 |
| yijie-desktop | `pnpm build` | 0 | PASS：production renderer build | 2026-08-25 |
| yijie-desktop | `pnpm docs:build` | 0 | PASS：VitePress Design System build | 2026-08-25 |

说明：实现早期、`yijie-contracts` 尚未出现并行改动时，`make lint`、`make test`、`make build` 曾完整
PASS（前端 63 files / 449 tests，Rust 246 passed / 3 ignored）。最终复跑期间，该外部仓库出现与
FEAT-130 无关的 Skills/API 未提交变化；clean-check 与两项 contract digest pin 按设计失败。本需求未修改、
清理或覆盖这些变化，Desktop 自身 lint/type/UI/Rust/build 门禁均独立复跑。

## 2. 真实入口与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Fresh startup/readiness | `pnpm tauri:dev` | Desktop local / demo_fast | 固定端口 `18081` 已由 2026-08-24 启动的既有本地 Demo listener 占用；未擅自终止未知在用会话 | BLOCKED |
| Production-component renderer | visual harness 核对七项顺序、项目→对话树、长列表、项目选择条 | 1180×760 light/dark | UI 结果与 AC-001–005 一致；静态背景为 light `rgb(247, 249, 243)` / dark `rgb(15, 20, 12)`，hover 描边始终透明，截图已保存 | PASS |
| 200% equivalent | 590×380 CSS viewport / DPR 2，检查 document 与内部树滚动并滚到底 | local renderer | `body.scrollHeight=760 > innerHeight=380`；滚动后 Settings、composer 与 send 仍可见，任务树仍独立滚动 | PASS |
| Representative failure | removed project、read-only、write denial、cached unavailable、permission revoke、tenant/session/route race | safe synthetic metadata | focused tests 全部 PASS，旧 context/session 的迟到结果不发布，非当前会话不暴露 mutation，删除只影响精确匹配路由 | PASS（自动化） |

根据项目 Handbook，renderer、synthetic data 与 focused tests 不能替代 fresh canonical real-service run，
因此本记录不宣称 D4 PASS。

## 3. Must AC

| AC | Result | 证据/Artifact |
|---|---|---|
| AC-001 | PASS | 导航单测；light/dark 截图中顺序精确包含“插件 → 资料库 → 任务记录”，设置置底 |
| AC-002 | PASS | 任务记录为 heading/section；router、loader、页面源文件和 production source inventory 均无 `/tasks` 页面 |
| AC-003 | PASS | Tree route/fallback 测试；read-only Store 只调用 read action，点击会话可进入 `/chat/:sessionId` |
| AC-004 | PASS | 1180×760 长列表仅 `.chat-tree` 滚动，顶部导航与设置保持定位 |
| AC-005 | PASS | `radius-lg`、`bg-app`、无描边的 brand-soft hover token source check 与 light/dark 截图 |
| AC-006 | PASS（UI 层） | Expanded Sidebar/Tree axe serious/critical 0；语义 button/link/focus 测试；200% 等效滚动截图；reduced-motion 无新增动画 |

## 4. UI Artifact

- `references/feat130-light.jpg`：1180×760 light，含七项导航、长任务树与项目选择条。
- `references/feat130-hover.jpg`：1180×760 light hover，项目选择条仅改变柔和背景、无新增描边。
- `references/feat130-dark.jpg`：1180×760 dark，验证同一 token 语义。
- `references/feat130-zoom200-scrolled.jpg`：200% 等效视口滚到底，Settings 与 composer/send 可达。
- Loading/empty/error：Tree focused tests 覆盖；缓存 metadata 在 unavailable 时继续显示稳定中文提示。
- 权限：只有 `task.read` 时不准备 writable draft、不渲染 mutation 菜单；权限撤销会关闭已打开确认框。

## 5. Diff、审查与限制

- 独立只读审查完成；read-only draft 阻断、permission 文案误报、retry 越权、modal 权限撤销、
  context/session 迟到发布竞态、非当前会话误操作与删除后错误跳转均已修复并回归；最终矩阵
  8 files / 104 tests PASS，当前无 P0/P1/P2。
- `git diff --check` 对 yijie-desktop 与 FEAT-130 Feature Package 均 PASS。
- 目标 source inventory 仅在负向测试与 supersession 文档保留 `/tasks` 字样；Public API 的 `/v1/tasks`、
  `/v2/tasks` 与本需求无关且未变。
- 多个 removed projectId 保留各自边界，可能出现多个同名“项目已移除”安全组；不泄漏原名称/路径。
- canonical fresh D4 仍待既有本地 Demo 安全释放固定端口后执行。

## 6. Public Demo

- `exposure=local`，`public_readiness.required=false`；DP 不适用。

## 7. 结论

- FEAT-130 代码、UI 层 Must AC、自动化、视觉与构建：PASS。
- D4 本地真实服务 fresh run：PARTIAL / 未宣称 PASS，唯一阻塞为既有 Demo 占用 canonical 端口。
- DP：N/A。
- 验证时间：2026-08-25T01:33:40+08:00。
