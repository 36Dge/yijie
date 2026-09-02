# FEAT-151 Demo 验证

## 1. Focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie` | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-151-desktop-workflow-showcase` | 0 | PASS | 2026-08-31 |
| `yijie` | `pnpm lint && pnpm test` | 0 | manifest/Contract First lint PASS；48/48 tests PASS | 2026-09-01 |
| `yijie-desktop` | FEAT-151 focused Vitest（9 files） | 0 | 67/67 PASS | 2026-09-01 |
| `yijie-desktop` | `pnpm lint` | 0 | PASS | 2026-09-01 |
| `yijie-desktop` | `pnpm exec vue-tsc --noEmit` | 0 | PASS | 2026-09-01 |
| `yijie-desktop` | `pnpm build` | 0 | PASS；生成 WorkflowPage chunk | 2026-09-01 |
| `yijie-desktop` | `pnpm docs:build` | 0 | PASS | 2026-09-01 |
| `yijie-desktop` | 首次 `pnpm test` | 1 | FAIL；preflight 因当时既有脏 Agent Host checkout 退出 | 2026-09-01 |
| `yijie-desktop` | 首次直接 `pnpm exec vitest run --maxWorkers=4` | 1 | 115/119 files、1078/1083 tests PASS；当时 5 项范围外失败 | 2026-09-01 |
| `yijie-desktop` | 最终重跑 `pnpm test` | 1 | preflight PASS；117/119 files、1083/1085 tests PASS；剩余 v4 Contracts HEAD 预期和 FEAT-132 projection 两项范围外失败 | 2026-09-01 |
| `yijie-desktop` | 1180×760 light/dark browser visual harness | 0 | PASS；横向 overflow=0、interactive=0、axe violations=0 | 2026-09-01 |
| `yijie-desktop` | fresh `/tmp` target `tauri build --debug --bundles app --no-sign` | 0 | production frontend + Rust/Tauri bundle PASS；既有 binary 未覆盖 | 2026-09-01 |
| `yijie-desktop` | Computer Use：真实 `.app` App Shell 点击/滚动 smoke | 0 | `/workflows`、标题、选中态、完整 AX 内容与正常窗口退出 PASS | 2026-09-01 |
| `yijie-desktop` | `/bin/bash -n scripts/run-local-demo-fast.sh` + 启动器 Vitest | 0 | Bash 语法、macOS Bash 3.2 nounset 空数组与 12/12 tests PASS | 2026-09-01 |
| `yijie-desktop` | `node scripts/check-agent-host-v4-contract.mjs` + stable-only launcher mutation 子集 | 0 | 安全展开式边界 PASS；unsafe 旧写法被拒绝 | 2026-09-01 |
| `yijie-desktop` | 第三次 fresh `pnpm tauri:dev` + readiness probe | 0（probe；launcher Ctrl-C 后预期为 1） | Vite 1420、Tauri Desktop、Agent Host 18081 ready；Ctrl-C 正常停止后端口/进程清理 | 2026-09-01 |
| `yijie-desktop` | `pnpm tauri:build:demo-fast` + Computer Use 当前同源 `.app` smoke | 0 | 构建、Host ready、`/workflows` 全量 AX 内容、滚动到底部和正常窗口退出 PASS | 2026-09-01 |
| `yijie` | `check-feature-package.sh --gate D0`、`--gate D4`、`--strict` | 0 | schema v3、文档结构、D0/D4 语义与未完成标记检查全部 PASS | 2026-09-01 |

## 2. 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | 用户明确授权本 Feature 的构建产物覆盖后，fresh 执行 canonical `pnpm tauri:dev`；等待 Vite/Tauri/Host ready；Ctrl-C 正常退出 | macOS local demo_fast、系统 Bash 3.2、真实 Codex Runtime/Agent Host | 第一次发现并修复 nounset 空数组，第二次修复静态 checker，第三次 fresh 运行 1420/18081 与 Desktop/Host 均 ready；退出后全部清理。覆盖前 Host 备份 SHA `bbeb9cf0…`，当前 Host SHA `08faad2d…`。 | PASS |
| Real happy path | 从当前同源 unsigned `.app` App Shell 点击“工作流”并核对页面全部信息 | 真实 Tauri WebView 1162×768、真实 Host 18081；canonical startup 已独立 PASS | 点击进入 `tauri://localhost/workflows`；标题/选中态正确，AX 树逐项包含全部分类、卡片、时间、节点、用量和展示操作；滚动到底部第四张推荐卡完整可见，关闭后无残留。 | PASS |
| Representative failure/retry | 缺少 `workspace.use` 时深链拒绝且 loader 不运行 | Vitest memory router | 进入 `/access-denied`，loader 调用次数为 0；exact profile 外路由不注册。 | PASS |

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | PASS | 真实 App Shell 从 `/chat` 点击“工作流”进入 `tauri://localhost/workflows`，标题为“工作流 · 易界 AI”，侧栏选中。 |
| AC-002 | PASS | 领域模型/Page 测试按顺序核对 9 个分类；亮色截图。 |
| AC-003 | PASS | Page 测试核对分类、排序/视图、创建卡与 4 张已有工作流；亮色截图。 |
| AC-004 | PASS | Page/领域模型测试核对 4 张推荐卡全部文案、节点、使用量和展示操作；暗色滚动截图。 |
| AC-005 | PASS | 页面测试断言 `button/a/input/select` 为 0、20+ `aria-disabled`，无页面内跳转或 handler。 |
| AC-006 | PASS | 源码否定搜索与测试确认无 fetch/axios/invoke/Tauri/localStorage/sessionStorage/indexedDB。 |
| AC-007 | PASS | permission/router/sidebar tests 覆盖导航隐藏和 denied-loader。 |
| AC-008 | PASS | lint/typecheck/build/docs build 与 1180×760 两主题 visual harness。 |
| AC-009 | PASS | 唯一 h1、section/article/list 语义、键盘可聚焦滚动区与 axe violations=0。 |
| AC-010 | PASS | macOS Bash 3.2 空数组回归、v4 静态 checker 与第三次 fresh canonical 启动；Desktop/Host ready 且正常退出清理。 |

## 4. UI 与真实结果

- Artifact：`evidence/workflow-light-1180x760.jpg`、`evidence/workflow-dark-recommended-1180x760.jpg`、`evidence/workflow-native-entry-1162x768.jpg`、`evidence/workflow-native-recommended-1162x768.jpg`、`evidence/workflow-canonical-native-entry-1162x768.jpg`、`evidence/workflow-canonical-native-recommended-1162x768.jpg`。
- Light/dark 均在 1180×760 下 document/main 横向 overflow=0；主区域纵向滚动可用，暗色证据覆盖推荐工作流区。
- Loading/error/retry 不会困住用户：静态页无 loading/retry；权限失败在页面实例化前进入既有无权访问页。
- 最终真实用户结果：真实 Tauri App Shell 可点击进入工作流页并完整滚动浏览全部静态信息；页面内展示项不形成可操作按钮或二次链接。

## 5. Diff 与限制

- `git status` 已确认 yijie 存在既有 FEAT-137 治理文档改动；本实现未清理或覆盖这些改动。
- FEAT-151 scoped diff、权限/I/O 边界与 UI 语义已复审；`git diff --check` PASS，无剩余可操作问题。
- 已知限制：仅 local demo_fast 静态展示；不实现截图内页面操作；canonical 裸 debug 二进制不在 macOS Accessibility 应用目录，元素级 smoke 使用当前同源 debug `.app`；全量 frontend Vitest 仍有 2 个范围外既有失败。

## 6. Public Demo

- `exposure=local`，DP 不适用；不创建公网入口，不调用付费 API，不处理真实数据。

## 7. 结论

- `D4` 本地真实可用：PASS。
- `DP` 公开 Demo 可用：N/A。
- 验证时间：2026-09-01T11:05:38+08:00（自动化、visual harness、fresh canonical 启动与当前同源真实 Tauri `.app` smoke）。
