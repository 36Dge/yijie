# FEAT-130 整体实现与调试记录

## 1. 整体实现方案

- 真实调用链：`ChatPermissionLifecycle → chatStore.bind → listProjects/listSessions → YjAppShell → YjSidebar → ChatSidebarTree → /chat/:sessionId`。
- 实施顺序：冻结 UI override → 调整内部导航模型/路由 → 移动并增强任务树 → 调整项目选择条 token → focused/full/visual 验证。
- Contract First：`contract-impact=none`，不修改 wire 或持久化权威源；复用既有 `ChatProject`/`ChatSession` 投影。
- 明确不做：不扩展 IPC 以恢复已移除项目名称，不新增依赖、Tauri capability 或 production 发布加固。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| yijie-desktop | `src/navigation/app-nav.ts`、`YjSidebar.vue`、`YjAppShell.vue` | 重排主导航，将任务记录改为静态分组并在全局展开侧栏中承载历史树 | 满足 AC-001–004，并保留只读用户入口 |
| yijie-desktop | `ChatSidebarTree.vue` | 项目→对话两层、独立滚动、removed-project fallback 与状态文案 | 复用权威元数据且不丢失历史 |
| yijie-desktop | `chat.store.ts`、Tree 菜单 | `task.read` 只加载项目/会话/历史，不触发 create/submit 草稿命令，并隐藏无权 mutation 菜单 | 保证移除 `/tasks` 后只读入口真实可达且不越权 |
| yijie-desktop | router/policy/`TasksPage.vue` | 移除 `/tasks` 页面、loader 与路由；read-only root 安全回到 Settings shell | 删除独立页面且保留侧栏选择路径 |
| yijie-desktop | `ChatComposer.vue` | 新建态项目选择条使用 `radius-lg/bg-app`，hover 仅使用品牌 soft 且不改变描边 | 按易界 token 完成 +4 圆角与更克制的对比调整 |
| yijie-desktop | tests/design docs | 更新行为测试、视觉 harness 与 FEAT-130 Accepted override | 防回归并消除旧规范冲突 |
| yijie | `docs/features/FEAT-130-desktop-sidebar-layout/` | 建立 demo_fast D0/D4 追踪记录 | 满足项目治理与证据要求 |

## 3. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复 | 结果 | 累计耗时 |
|---|---|---|---|---|---:|
| 2026-08-25 | 基线 focused tests 6 文件、44 测试通过 | 可将后续失败归因于 FEAT-130 diff | 无 | PASS | < 1h |
| 2026-08-25 | 直接复用现有树会遗漏 removed project sessions | Rust `list_projects` 排除 removed，但 `list_sessions` 保留并投影 `projectAvailable=false` | 前端按 projectId 建安全 fallback group | focused tests PASS | < 1h |
| 2026-08-25 | 独立审查发现 task.read-only bind 会误触 draft attachment 命令 | native draft target 要求 `task.create`，项目/会话/history 读取只要求 `task.read` | Store 按 `create_session` / `submit_turn` 跳过草稿，菜单按 allowedActions 投影 | read-only focused tests PASS | < 2h |
| 2026-08-25 | 全局任务树暴露迟到异步发布、跨路由误操作与删除后误跳转风险 | Settings/其他会话也能看到任务树，Store 命令返回时 context/selection 可能已变化 | 所有迟到结果绑定 context/session/epoch；仅当前会话显示 mutation 菜单；删除结果携带 ID 并精确匹配当前路由后跳转 | 最终独立复审无 P0/P1/P2；8 文件、104 测试 PASS | < 2h |
| 2026-08-25 | 视觉复核认为静态背景略重且 hover 描边过强 | `bg-subtle` 与 brand border 同时提高了两层视觉对比 | 静态态降为 `bg-app`，hover 只改变为 `brand-soft`，保留独立键盘 focus ring | Composer focused test 与 renderer 复核 PASS | < 1h |
| 2026-08-25 | fresh `pnpm tauri:dev` 拒绝启动 | 固定端口 18081 已有既存 Demo listener；来源不属于本次进程 | 不终止未知会话，保留 renderer smoke 与完整自动化证据 | D4 fresh run 待外部会话释放 | < 2h |

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费调用/破坏性外部操作/生产写入 | N/A | N/A | 0 | 0 | N/A |

## 5. 已知限制

- “项目已移除”只保留安全状态与对话，不显示已移除项目原名称或路径；恢复名称需要新的持久化/IPC 语义，不在本需求范围。
- task.read-only 用户从 Settings shell 的全局侧栏选择历史对话；不提供新的只读落地页面。
- 多个已移除 projectId 保留为多个安全边界组，显示名均为“项目已移除”，不合并或泄漏原项目身份。
- UI 实现与视觉矩阵已完成；canonical fresh D4 因既有本地 Demo 占用固定端口而未宣称通过，详见 `02-verification.md`。
