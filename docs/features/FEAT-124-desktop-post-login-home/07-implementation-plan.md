# FEAT-124 原子实施计划

## 1. 实施原则

- 一次只完成一个可独立验证、可独立回滚的行为。
- 先建立失败证据，再做满足当前 slice 的最小实现。
- G2 通过后只允许先实现 S0 私有持久化契约切片；G2A 通过前不实现 App Shell 业务 consumer。
- 不夹带真实任务、认证、权限服务、API、Runtime、Tauri capability、依赖升级或全仓格式化。
- `docs/design/exports` 只作迁移参考，活跃 `src/` 不得导入。
- 每个 commit 只表达一个可审查目的；测试、状态和证据按真实结果更新。

## 2. 依赖 DAG

```text
Accepted requirements + App Shell 2.0.0 + Chat 1.1.0 + Navigation 1.1.0
  → G2 technical/test/implementation approval
  → S0 sidebar-preference-v1 reader/writer + PREF tests
  → full lint/test/build + rollback compatibility evidence
  → G2A approval
  → S1 design foundations/assets/icons/theme
  → S2 global App Shell + navigation + sidebar store
  → S3 /chat entry state + placeholder rotation
  → S4 Tasks/Settings/router/window integration
  → S5 accessibility/visual/full verification
  → G4 code review and completion
```

## 3. 实施切片

| Slice | 主要意图 | AC/NFR | Repository | 允许修改 | 禁止修改 | 前置 | 验证 | 回滚 |
|---|---|---|---|---|---|---|---|---|
| S0 | 建立 sidebar preference v1 权威投影 | AC-010、NFR-005 | yijie-desktop | `src/domain/sidebar-preference.ts`、对应 test | Vue 页面、store、路由、package 依赖 | G2 人工批准 | `pnpm exec vitest run src/domain/sidebar-preference.test.ts`；`make lint/test/build` | 删除两个新增文件 |
| S1 | 迁入最小 token、Naive theme、Logo、YjIcon | AC-002/003/006、NFR-002/004 | yijie-desktop | `src/styles/variables.css`、`src/design/theme/`、`src/assets/brand/`、`src/icons/`、`src/components/yijie/YjIcon.vue`、`YjLogo.vue`、`package.json`、`pnpm-workspace.yaml`、`pnpm-lock.yaml` | 其它依赖、exports runtime import、页面业务 | G2A passed | exact Lucide + PostCSS security override；audit；`make lint/test/build`；lockfile/diff review | 回退 S1 commit 和依赖/override |
| S2 | 建立全局 App Shell、导航和 sidebar store | AC-002/003/005/010 | yijie-desktop | `YjAppShell.vue`、`YjSidebar.vue`、`YjNavItem.vue`、`src/navigation/app-nav.ts` + tests、`src/stores/sidebar.store.ts` + tests、`App.vue`；`ChatPage.vue` 只允许移除旧内嵌 shell；`src/styles/main.css` 只允许把旧全局硬编码值切到既有 token | 真实权限 API、禁用模块路由、任务提交、S3 首页内容 | S0/S1 + G2A/G3 | nav/store unit；`make lint/test/build`；browser smoke | 回退 S2，恢复旧 RouterView/Chat 内嵌 shell |
| S3 | 实现 `/chat` 新建任务入口和轮播 | AC-001/004/007/009 | yijie-desktop | `placeholder-rotation.ts` + test、`useRotatingPlaceholder.ts`、`ChatPage.vue`、必要 scoped CSS | 发送、附件、草稿持久化、API/Agent/Runtime | S2 | PH tests；`make lint/test/build`；浏览器输入检查 | 回退 S3，保留新 Shell |
| S4 | 整合三条真实路由和窗口基线 | AC-001/005、NFR-001 | yijie-desktop | `router/index.ts` + test、`TasksPage.vue`、`SettingsPage.vue`、`src-tauri/tauri.conf.json` 的 minWidth/minHeight | 新业务路由、capability/CSP/command、Tasks 业务重构 | S2/S3 | router tests；`make lint/test/build`；direct-route smoke | 回退 S4；旧路由表恢复 |
| S5 | 完成主题、键盘、视觉矩阵和证据 | AC-002/006/007/008、全部 NFR | yijie-desktop + yijie evidence | FEAT-124 对应修复、`08-verification-report.md` | 降低断言、跳过暗色/最小窗口、无关重构 | S0—S4 | 全门禁、`pnpm docs:build`、`pnpm tauri:dev`、12 组合视觉检查 | 失败回到对应 slice，不进入 G4 |

## 4. Slice 详细 Context 与停止条件

### S0 — 私有持久化契约

- 输入权威：App Shell 2.0.0、`04-contract-change-plan.md`。
- 设计：导出固定 key、封闭 `SidebarMode`、`readSidebarMode(storage)`、`writeSidebarMode(storage, mode)`；Storage 通过窄接口注入。
- 测试：`PREF-001`—`PREF-006` 先失败后通过。
- 停止条件：需要保存 JSON、用户/租户信息、多个 key、Tauri storage plugin 或改变默认值。
- G2A 证据：局部 test、完整 lint/test/build、回滚矩阵、实现完整 SHA、段成威批准。

### S1 — Design foundation

- 只迁移本页实际使用的 token 和批准品牌 SVG；保留来源记录。
- `@lucide/vue@1.27.0` 是唯一计划新增的运行依赖：registry 查询于 2026-07-30，peer `vue >=3.0.1`、ISC license；必须用 exact pin 和 lockfile。
- `postcss@8.5.18` 不是新增直接依赖；它是段成威单独批准的 workspace override，用于修复 baseline `8.5.16` 的高危公告，必须以 audit 0 known vulnerabilities 为通过条件。
- 页面不得直接 import Lucide；图标必须先进入 `src/icons/registry.ts`。
- 停止条件：需要第二图标库、远程字体、未知品牌资产、CSS filter、从 exports 运行时 import，或 package peer/build 不兼容。

### S2 — App Shell/Nav

- App Shell 上移至 `App.vue`，避免每个页面重复 sidebar。
- 代码事实显示旧 `ChatPage` 内嵌 220px sidebar；S2 只移除该旧壳层并保留主内容，避免双侧栏，标题/输入/轮播仍由 S3 重做。
- 导航顺序：新建任务、任务记录、分隔、五个 disabled 模块；Settings 底部。
- `visible=false` 在纯 resolver 阶段过滤；当前不实现权限服务。
- disabled 项无 route、无点击/键盘动作；enabled route meta 驱动 selected。
- 停止条件：需要猜 session/RBAC、为 disabled 模块创建假页面、隐藏替代服务端授权。

### S3 — Chat entry

- textarea 初始为空，仅页面内 ref；无按钮、附件、预填正文或提交事件。
- 五条文案及 4000ms、focus/input pause、reduced-motion、dispose 规则来自 Chat 1.1.0。
- 停止条件：需要保存草稿、创建任务、接 API/Agent/Runtime、增加快捷提交。

### S4 — Routes/Window

- `/` 继续 redirect `/chat`；只保留 `/chat`、`/tasks`、`/settings`。
- Tasks 文案改“任务记录”但不扩展现有业务数据。
- Settings 保持独立并位于 Shell 底部。
- 仅允许 `tauri.conf.json` 增加 `minWidth:1180`、`minHeight:760`；不改 capability、CSP、command、plugin、sidecar。
- 停止条件：window 配置需要新原生权限，或现有 Tauri schema/build 不接受字段。

### S5 — Verification

- 视觉矩阵：light/dark × 1180×760、1280×820、1440×900 × 240/72。
- 路由矩阵：直接进入 `/chat`、`/tasks`、`/settings`，返回与 selected/focus 正确。
- 存储矩阵：no key、两个合法值、unknown、throw、rollback。
- 只有真实执行结果能进入 `08-verification-report.md`。

## 5. 跨仓与候选顺序

| 阶段 | Repository | Branch/base full SHA | 输出 | Pin/引用 | Owner |
|---|---|---|---|---|---|
| Governance docs | yijie | develop / `82f39ee97e40f5932c6f59a5567342ee4c8aaf04` | FEAT-124 00—07 | Feature ID/path | 段成威 |
| Design authority | yijie-desktop | develop / `4480f4a93eac59b3277fb0650e25f156e7fbc6a9` | App Shell 2.0.0、Chat 1.1.0、Navigation 1.1.0 | Accepted 设计完整 SHA | 段成威 |
| Private contract candidate | yijie-desktop | design `4480f4a93eac59b3277fb0650e25f156e7fbc6a9` / implementation `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e` | `sidebar-preference-v1` + tests | 实现完整 SHA；无 generator/digest | 段成威 |
| UI consumer | yijie-desktop | G2A-approved preference commit `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e` | S1—S4 | 同仓精确前置 commit | 段成威 |
| Activation/evidence | yijie-desktop + yijie | code candidate commit | Desktop candidate + verification | 两仓 commit 互相引用 | 段成威 |

公共 contracts/provider/consumer 阶段为 N/A；无 `yijie-contracts`、API、Agent Host 或 Runtime 改动。

## 6. Migration 实施序列

| Phase | 代码/数据动作 | 兼容要求 | 验证 | 停止/回滚点 |
|---|---|---|---|---|
| Expand | S0 新 reader 支持无 key/合法/未知/异常 | 旧环境无 key 可启动 | PREF-001/004/006 | 删除 S0 |
| Backfill | N/A；不回填 | 首次启动不写业务数据 | 断言 hydrate 只读一次 | N/A |
| Switch | S2 toggle 开始写 v1 | old app 忽略，新 app 恢复 | PREF-002/003 + restart | 回退 S2，遗留 key 无害 |
| Contract | v1 在当前版本保留 | 不删除/改义 | rollback/roll-forward smoke | 删除 key 恢复默认 |

## 7. Commit/PR 计划

| Commit | 单一目的 | Files/Repo | 必需证据 | Cross-link |
|---|---|---|---|---|
| C1-yijie | 完成 FEAT-124 G2 文档与长期协作规则 | `yijie/docs/features/FEAT-124-*`、Codex memory docs | package G2、meta lint/test | FEAT-124 |
| C1-desktop | 接受 FEAT-124 Design Pattern | 三份 design docs | `pnpm docs:build` | FEAT-124 |
| C2-desktop | sidebar preference v1 + conformance | S0 files | PREF-*、full lint/test/build | G2A evidence |
| C3-desktop | token/theme/logo/icon foundation | S1 files + workspace override + lockfile；`efa1e465b478d131f769654075c057132d01a747` | lint/test/build/docs、audit、dependency diff | App Shell 2.0.0 |
| C4-desktop | global App Shell/nav/sidebar | S2 files | NAV/PREF + full gates | FEAT-124 AC-002/003/005/010 |
| C5-desktop | `/chat` entry + placeholder | S3 files | PH/INPUT + full gates | FEAT-124 AC-004/009 |
| C6-desktop | route/window/visual completion | S4/S5 files | router/full gates/visual matrix | Verification report |
| C7-yijie | 最终验证与交付证据 | `08—10` | G4/G5/G6 适用证据 | Desktop final commit |

提交、push、PR、tag 和发布均需段成威另行明确授权；本计划不自动执行。

## 8. Slice 状态

| Slice | Base full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | `4480f4a93eac59b3277fb0650e25f156e7fbc6a9` | `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`：`src/domain/sidebar-preference.ts` + test | local 9/9；full frontend 10/10；Rust 0 tests；lint/build/docs PASS | G2A Approved by 段成威 | Complete |
| S1 | `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e` | `efa1e465b478d131f769654075c057132d01a747`：exact Lucide + PostCSS 8.5.18 override + token/theme/brand/icon foundations | audit 0 known vulnerabilities；lint、3 files/12 frontend tests、Rust、build、docs、asset/import checks PASS | G3 Approved by 段成威 | Complete |
| S2 | `efa1e465b478d131f769654075c057132d01a747` | `e488259fe31a21c4e691646a971b812c00760863`：global App Shell/nav/sidebar/store + theme runtime bridge fix；已推送 `origin/develop` | nav/store/theme 11 tests；full 6 files/23 tests；Rust/lint/build/docs/audit PASS；1180×760 browser smoke PASS | Implementer self-check complete；段成威已授权提交与推送 | Complete |
| S3 | `e488259fe31a21c4e691646a971b812c00760863` | none | NOT RUN | Pending；等待段成威授权执行 | Ready |
| S4 | S2/S3 commits | none | NOT RUN | Pending | Blocked |
| S5 | S0—S4 | none | NOT RUN | Pending | Blocked |

## 9. 每个 Codex 实现任务固定 Context

```text
Feature ID / Slice ID: FEAT-124 / Sx
角色：Implementer（完成后另开 Reviewer pass）
Repository / branch / base full SHA:
权威输入：01 requirements、04 contract、05 design、06 test、07 plan、Accepted Pattern
目标及 AC:
允许修改:
禁止修改:
前置 Gate/commit:
先失败的测试:
真实验证命令:
证据输出:
停止条件:
最终报告：diff、命令/exit、未执行项、风险、下一 Gate
```

## 10. 变更控制

| 变化 | 必须回到 | 停止条件 |
|---|---|---|
| 用户行为、文案、路由或 AC | `01-requirements.md` | 不静默改 UI |
| 仓库、依赖或权限边界 | `02-impact-assessment.md` | 新仓/新依赖方向先复核 |
| 风险、认证、授权、数据分类 | `03-decisions-and-risks.md` | 高风险变化请求段成威确认 |
| sidebar key/default/值域/持久化 | `04-contract-change-plan.md` | 重做 G2A |
| 组件、状态、主题、window 方案 | `05-technical-design.md` | 重做 G2 |
| 测试层级、阈值或缺失环境 | `06-test-plan.md` | 不降低断言绕过 |
| Slice 范围、顺序或回滚 | 本文件 | 更新 DAG 后再继续 |

## 11. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 技术负责人 | 段成威 | G2 Approved；明确授权执行 S0 | 2026-07-30 |
| Contract/Consumer Owner | 段成威 | G2A Approved；明确授权执行 S1 | 2026-07-30 |
| S1/G3 Owner Reviewer | 段成威 | G3 Approved；明确授权执行 S2 | 2026-07-31 |
| Reviewer | 段成威 | 实现后必须进行与实现阶段分离的结构化审查 | 2026-07-30 |
| 发布负责人 | 段成威 | 当前只批准计划，不批准提交、push 或发布 | 2026-07-30 |
