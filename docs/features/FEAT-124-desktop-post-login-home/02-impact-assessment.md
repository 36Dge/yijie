# FEAT-124 现状扫描与影响评估

## 1. 调查基线

| Repository | Rules read | Branch | Full HEAD SHA | Worktree | Toolchain |
|---|---|---|---|---|---|
| yijie | `AGENTS.md`、Feature Delivery Handbook、`repos.yaml` | develop | `82f39ee97e40f5932c6f59a5567342ee4c8aaf04` | clean before package creation | pnpm/Make governance |
| yijie-desktop | `AGENTS.md`、README、App Shell/Chat/页面生成/UI Review/窗口规范 | develop | `09d987f09c2f2eac2575187ef57b9b65d1e89ae3` | clean | Node 24–26、pnpm 11、Vue 3、Tauri 2 |

## 2. 已验证的当前行为

| 事实 | 文件/符号/行号或命令 | 结果 | 事实/推断 |
|---|---|---|---|
| `/` 当前重定向到 `/chat` | `yijie-desktop/src/router/index.ts` | 路由只有 `/chat`、`/tasks`、`/settings` | Fact |
| 当前首页为早期 Chat 骨架 | `src/pages/chat/ChatPage.vue` | 220px 蓝色侧栏、英文导航、预填 prompt、创建本地任务按钮 | Fact |
| 当前 Naive UI 主题仍是蓝色 | `src/App.vue` | `primaryColor: #1f6feb` | Fact |
| 当前全局样式未接入完整易界 token | `src/styles/main.css` | 仍使用蓝灰硬编码基础值 | Fact |
| API client 仍返回本地占位数据 | `yijie-desktop/AGENTS.md`、`src/api/client.ts` | 不代表真实 Runtime/后端已接通 | Fact |
| 活跃 `src/` 中没有完整 `YjAppShell`、`YjIcon` registry 和设计 token 目录 | `find src` 与 `AGENTS.md` | 需要有边界地迁移/实现，不能假设存在 | Fact |
| Design System 已确定绿色品牌和布局基线 | `docs/design/docs/design/00-final-decisions.md`、窗口规范 | 主色 `#95BF47`、系统主题、240/72px 侧栏、1180×760 最小窗口 | Fact |
| 参考 HTML 的默认视觉是“新建任务” | 源码与 1440×900 浏览器渲染 | 240px 侧栏、960px 内容、176px 输入框、6 个中文入口 | Fact |
| 参考 HTML 其他导航仅切换到说明性空态 | `01_index.html` script | 未定义生产路由或业务页面 | Fact |
| 参考稿不含旧 App Shell Pattern 要求的顶部状态区 | HTML 与 `05-patterns/01-app-shell-navigation.md` 对比 | 产品确认本页不展示；Accepted App Shell 2.0.0 已将顶部状态改为由页面 pattern 决定 | Fact + documented product exception |
| 参考稿是无会话入口态，不是完整 Chat 三栏工作区 | HTML、`05-patterns/02-chat-workspace.md` 与用户决策对比 | `/chat` 在本需求中定义为新建任务入口态，完整会话工作区不在当前范围 | Confirmed product scope |
| App Shell/Chat/Navigation 规范已补充 FEAT-124 规则 | `01-app-shell-navigation.md` 2.0.0、`02-chat-workspace.md` 1.1.0、`02-navigation-components.md` 1.1.0 | 定义入口态、任务记录、五条 placeholder、禁用/隐藏和侧栏偏好 | Accepted |

## 3. 仓库与组件影响矩阵

| Repository/Component | 职责 | 影响 | 原因 | Owner | 预计改动 |
|---|---|---|---|---|---|
| yijie | 跨仓治理与 Feature 证据 | direct | 保存 FEAT-124 文档与门禁 | Platform Team | `docs/features/FEAT-124-*` |
| yijie-desktop | Mac 用户体验 | direct | 首页、App Shell、路由、token、组件和测试 | 段成威 | `src/` 与必要设计文档 |
| yijie-contracts | 公共 wire 契约 | none | 当前 `additive` 只来自 Desktop 私有本地偏好，不改变跨仓 wire | Platform Team | N/A |
| yijie-api | 认证/业务后端 | none | 不改变登录或任务 API | Backend Team | N/A |
| yijie-agent-host | Agent 运行适配 | none | 不接真实任务 | Agent Runtime Team | N/A |
| yijie-codex | Runtime Kernel | none | 普通 Desktop UI 不修改 Runtime | Agent Runtime Team | N/A |
| yijie-connectors | 平台工具执行 | none | 无平台 API 变化 | Integration Team | N/A |
| yijie-infra | 环境与发布 | none | 不新增服务/配置；Desktop 构建仍需验证 | DevOps Team | N/A |

跨仓仓库仍为 `none`；但侧栏模式现在跨应用重启持久化，因此整个 Feature 的最高影响从 `none` 调整为 `additive`。若未来增加真实任务提交、认证或跨进程通信，必须再次重新分类并扫描相关仓库。

## 4. 调用链与数据流

```text
已有认证/会话层（本需求只消费结果）
  → Vue Router `/chat`
  → Desktop App Shell
  → 新建任务入口页
  → 页面内存中的未提交 textarea 状态

YjSidebar toggle
  → `yijie.desktop.ui.sidebar.v1`
  → 下一路由/下一次应用启动恢复 240px 或 72px
```

当前范围在 textarea 页面内存状态结束，不持久化，也不调用 API、Agent Host 或 Runtime。

| 边界 | 方向 | 权威源 | Producer | Consumers | 失败传播 |
|---|---|---|---|---|---|
| Router path/route meta | Desktop 内部 | `src/router/index.ts` | Router config | App Shell/页面 | route loading/error/permission |
| Design token | Desktop 内部设计系统 | `docs/design` + 迁移后的 `src/styles/variables.css`/theme | Design System | Vue/Naive UI 组件 | theme/contrast/layout defect |
| Login/session | 跨边界，当前不修改 | 既有认证服务/层 | 既有认证服务/层 | Desktop Router/Shell | 由既有登录恢复流程处理 |
| Task submission | 不在当前范围 | 若启用则应由 contracts 定义 | Desktop | API/Agent Host | 必须重新做 Contract First |
| Sidebar preference | Desktop 私有持久状态 | App Shell Pattern 2.0.0 | `YjSidebar`/UI preference adapter | `YjSidebar` on route/app start | 缺失、未知、损坏或读取失败均回退 `expanded` |

## 5. Contract Impact

- 分类：`additive`（Desktop 私有本地偏好）
- 可复核理由：新增 `yijie.desktop.ui.sidebar.v1`，使侧栏模式跨路由和应用重启可观察；不改变任何公共 HTTP/RPC/event/Agent/Runtime wire。
- 权威源：`yijie-desktop/docs/design/docs/design/05-patterns/01-app-shell-navigation.md` 2.0.0。
- Producer/Consumer：`YjSidebar` 或其 UI preference adapter 写入；`YjSidebar` 在初始化时读取。
- 值域：`expanded | collapsed`；默认 `expanded`；未知/损坏值按 `expanded` 处理。
- 兼容与回滚：旧 Desktop 忽略新 key；新 Desktop 能读取无 key 的旧环境；回滚遗留 key 不产生业务或安全副作用。
- 公共 wire：`none`，`yijie-contracts` version/SHA/digest/generator 均为 `N/A`。
- 升级条件：如果偏好开始绑定用户/租户、跨设备同步，或改变登录/session、真实任务、Agent/Runtime transport，必须重新分类和设计。

## 6. 数据与 Migration 影响

| 存储/Schema | Owner | 变化 | 旧数据影响 | 新旧 Reader/Writer | 回填/回滚 |
|---|---|---|---|---|---|
| 数据库/缓存 | N/A | 无 | 无 | N/A | N/A |
| Keychain/session secret storage | 未授权修改 | 无 | 无 | N/A | 不得用普通 Web Storage 临时代替 session/secret 存储 |
| 未提交 textarea | Desktop 页面本地状态 | 只在内存，不持久化 | 无历史数据 | 页面实例内 | 离开页面或应用重启后清除 |
| `yijie.desktop.ui.sidebar.v1` | Desktop UI preference | 新增 `expanded｜collapsed` 字符串 | 旧版本无此 key | 新 reader 接受无 key/未知值；旧 reader 忽略新 key | 删除 key 即恢复默认展开；无需 migration/backfill |

## 7. 安全与隐私影响

- 认证：本需求消费既有登录结论，不实现或改变认证。
- 资源级授权：已有权限投影判定无权限时隐藏对应导航；直接深链仍必须由已有授权层拒绝。
- 租户隔离：页面不得自行构造租户上下文；未来状态区必须来自服务端权威。
- 数据分类：未提交任务文本可能包含 Confidential 商家信息。
- Secret/token：不得进入组件、store、localStorage、日志或 fixture。
- 侧栏偏好：仅保存 `expanded` 或 `collapsed`，不得混入用户、租户、权限或业务正文。
- 高风险审批：当前无真实写操作；如启用任务提交，需重新评估。
- 审计字段：当前导航不新增审计；任务创建需要另行定义。
- 输入风险：不记录 textarea 正文；如果未来提交，必须由下游验证长度、结构和权限。

## 8. Runtime、模型与第三方影响

| 依赖 | 固定版本/完整 SHA | 能力是否已验证 | 费用/限流 | Sandbox | Fallback |
|---|---|---|---|---|---|
| Codex Runtime | N/A | 本需求不接入 | N/A | N/A | N/A |
| Agent Host | N/A | 本需求不接入 | N/A | N/A | N/A |
| 平台 API | N/A | 本需求不调用 | N/A | N/A | N/A |
| Lucide | `@lucide/vue@1.27.0` exact；S1 `efa1e465b478d131f769654075c057132d01a747` | registry、typecheck、test、build 已验证；ISC、Vue peer `>=3.0.1` | N/A | 本地 UI | 不引入第二图标体系 |
| PostCSS security resolution | workspace override `8.5.18`；S1 `efa1e465b478d131f769654075c057132d01a747` | `pnpm why postcss` 仅一个版本；`pnpm audit --prod` 0 known vulnerabilities | N/A | 构建链 | 上游全部约束到修复版本后再评估移除 override |

## 9. 现有测试、构建与发布入口

| 目的 | 真实命令/配置来源 | 作用范围 | 已知限制 |
|---|---|---|---|
| Lint/typecheck | `make lint` / `pnpm lint` | Vue、TS、ESLint、Rust 相关门禁 | 不证明视觉正确 |
| Unit test | `make test` / `pnpm test` | Vitest 与 Rust 测试 | 当前 UI 组件测试基础需调查 |
| Build | `make build` / `pnpm build` | Vue typecheck + Vite/Tauri 构建入口 | 构建通过不证明路由/主题可用 |
| UI visual | 手工/自动浏览器 + Tauri 目标视口 | 亮/暗色、1180×760、1440×900 | 当前无已确认 visual regression runner |
| Design docs | `pnpm docs:build` | Design System 文档 | 只有设计文档变更时适用 |
| Generate | `pnpm generate` | 当前只输出占位文本 | 不能作为设计 token/generator 已接通证据 |

## 10. 初步交付顺序

### 合并顺序

1. 在 yijie 中登记 FEAT-124 已确认需求、Owner、里程碑和本地偏好影响。
2. 评审已更新的 `/chat` 入口态、导航和 Chat 设计规范。
3. 在 yijie-desktop 落地所需 token、主题、Logo/Icon registry 和基础 App Shell 组件。
4. 实现路由与默认新建任务入口。
5. 增加状态、可访问性、组件/路由测试和视觉证据。
6. 更新 Feature 验证与交付文档。

### 部署顺序

1. 构建 Desktop 候选。
2. 在本地/Tauri 环境验证窗口、主题、路由和回退。
3. 按 Desktop release 流程发布；本需求不触发后端部署。

### 功能启用顺序

1. 保持 `/chat` 默认路由，不做路由迁移。
2. 先落地能安全读取/回退的侧栏偏好，再启用收起写入行为。
3. 新 App Shell 与入口页同时启用，避免新旧视觉混杂。
4. 未完成业务模块保持明确禁用，无权限模块隐藏；“任务记录”和底部 Settings 保持可用。

## 11. 阻塞项与 Spike

| ID | 未知项 | 允许的只读/隔离验证 | 禁止副作用 | Owner | 结论 |
|---|---|---|---|---|---|
| SPIKE-001 | `/chat` 与现有 Tasks/Settings 的布局映射 | 扫描 Router、页面引用和测试 | 不改生产路由 | 段成威 | Resolved：`/chat` 新建任务；`/tasks`“任务记录”紧随其后；`/settings` 置底 |
| SPIKE-002 | token、Logo、YjIcon、YjAppShell 可从 exports 迁移的最小集合 | 比较 docs/design/exports 与活跃 src | 不直接从 src import exports | 段成威 | Investigation needed |
| SPIKE-003 | 参考入口态与 Accepted Chat/App Shell Pattern 的关系 | App Shell 2.0.0 与 Chat 1.1.0 | 不静默覆盖 Accepted Pattern | 段成威 | Resolved and Accepted |
| SPIKE-004 | 现有登录/session 层是否已存在 | 仅在实现前确认页面接入点，不改变协议 | 不新增临时 localStorage/session | 段成威 | Out of scope for feature behavior |
