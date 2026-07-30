# FEAT-124 技术设计

## 1. 设计摘要

- 问题：把当前 `ChatPage.vue` 内部的 220px 蓝色一次性 Shell，迁移为全路由共享的易界 App Shell，并在 `/chat` 实现只含本地输入的新建任务入口态。
- 方案：`App.vue` 组合全局 `YjAppShell + RouterView`；导航、侧栏偏好和 placeholder 轮播分别使用纯配置/纯领域逻辑与薄 Vue 组件；视觉从已接受的 design exports 有边界地迁入活跃 `src/`。
- 关键约束：Vue 3、Pinia、Vue Router、Naive UI；240/72px；1180×760；light/dark/follow-system；Lucide 统一 registry；不从 `docs/design/exports` 运行时导入。
- Contract Impact：`additive`，仅因 `yijie.desktop.ui.sidebar.v1` 私有持久偏好；公共 wire 为 none。
- 明确不做：真实任务提交、Chat 活跃会话、附件、API/Agent Host/Runtime、认证/session 协议、权限服务、Tauri capability/command/CSP、业务模块页面、遥测和新通用 UI 框架。

## 2. 当前事实与迁移边界

| 当前事实 | 证据 | 设计影响 |
|---|---|---|
| `/` 已重定向 `/chat`，仅有 `/chat`、`/tasks`、`/settings` | `src/router/index.ts` | 保持路径，不创建禁用模块占位路由 |
| Shell 只存在于 `ChatPage.vue`，宽 220px | `src/pages/chat/ChatPage.vue` | Shell 上移至 `App.vue`，Tasks/Settings 共用 |
| 当前主题在 `App.vue` 硬编码蓝色 | `src/App.vue` | 迁移语义 token 与集中 Naive theme |
| 当前输入有预填正文和“创建本地任务”按钮 | `ChatPage.vue` | 改为空 textarea + 轮播 placeholder；删除提交动作 |
| `TasksPage`、`SettingsPage` 各自全屏布局并带“返回 Chat” | 对应页面 | 移除重复全屏 Shell 语义，保留独立路由内容 |
| 当前只有纯 TS Vitest 测试，没有组件测试环境 | `src/domain/tasks.test.ts`、`package.json` | 领域/配置逻辑用纯 TS 测试；渲染与可访问性用实际浏览器/Tauri 验证 |
| Lucide 已是 Accepted 设计决策 | Design P0-06、S1 `package.json` | 已精确锁定 `@lucide/vue@1.27.0`，只通过 registry 暴露；不引入第二图标库 |
| 活跃 `src/` 没有 token、YjIcon、YjLogo、YjAppShell | 文件扫描 | 只迁移当前首页必需的最小集合 |

## 3. 组件职责与依赖方向

| Component/Path | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| `src/App.vue` | 全局 Naive provider、主题和 `YjAppShell` 组合 | system theme、Router | 全路由统一 Shell | 页面业务、存储解析 |
| `src/components/yijie/YjAppShell.vue` | sidebar + main slot 布局 | collapsed、nav items、route | 稳定 App Shell | 路由定义、权限判定、网络 |
| `src/components/yijie/YjSidebar.vue` | 品牌、任务组、业务组、底部 Settings、收起按钮 | 已解析 nav、collapsed | toggle/nav 用户事件 | 读取 Web Storage、业务授权 |
| `src/components/yijie/YjNavItem.vue` | selected/disabled/hidden 前的单项呈现 | item、collapsed | navigate intent | 自行创建路由或权限 |
| `src/navigation/app-nav.ts` | 唯一导航定义、分组、路由、文案、icon key | route key、上游 `visible` 投影 | 纯 `ResolvedNavItem[]` | 调用服务或伪造权限 |
| `src/domain/sidebar-preference.ts` | key、枚举、reader/writer、回退语义 | 注入的 `StorageLike` | `expanded/collapsed` | Vue 状态、用户/租户数据 |
| `src/stores/sidebar.store.ts` | 全局 sidebar 内存状态和切换动作 | preference adapter | reactive collapsed | 其它设置或认证 |
| `src/domain/placeholder-rotation.ts` | 五条文案与纯 index 转移 | index、事件 | 下一 index/状态 | timer/DOM |
| `src/composables/useRotatingPlaceholder.ts` | interval、focus、input、reduced-motion 生命周期 | pure rotation model | 当前 placeholder | 任务提交 |
| `src/pages/chat/ChatPage.vue` | `/chat` 新建任务入口态 | local text、placeholder | 本地编辑 UI | Shell、API、持久化、Agent |
| `src/router/index.ts` | 真实路由与 meta/nav key/title | route definitions | Router | 禁用模块占位 |
| `src/styles/variables.css`、`src/design/theme/naive-theme.ts` | token 与 Naive theme 唯一入口 | system light/dark | 语义视觉 | 页面局部风格 |
| `src/icons/registry.ts`、`YjIcon.vue`、`YjLogo.vue` | 批准图标/Logo 入口 | icon key、variant | 可访问品牌和图标 | 页面直接 import Lucide |

```text
system theme ───────────────→ App.vue / Naive provider
Vue Router route/meta ──────→ YjAppShell ─→ YjSidebar
                                        └→ RouterView ─→ Chat/Tasks/Settings
App Shell 2.0.0 ─→ sidebar-preference domain ─→ Pinia sidebar store ─→ YjSidebar
Chat 1.1.0 ─────→ placeholder pure model ─────→ composable ─────────→ ChatPage
permission projection (future/upstream) ──────→ app-nav visible flag
```

依赖只从页面/组件指向 store、navigation 和 domain；domain 不依赖 Vue、Tauri、Naive UI 或浏览器全局。

## 4. 关键时序

### 4.1 应用启动与侧栏恢复

1. `App.vue` 创建全局 Shell。
2. sidebar store 通过注入 adapter 读取 `yijie.desktop.ui.sidebar.v1`。
3. 合法值恢复对应宽度；无值、未知值或异常回退 `expanded`。
4. Router 解析当前 `/chat`、`/tasks` 或 `/settings`。
5. 导航配置按 `visible` 过滤，再按 route meta 计算 selected。
6. Shell 渲染 240px 或 72px；主内容通过 `RouterView` 呈现。

### 4.2 用户切换侧栏

1. 用户通过鼠标或键盘激活边界按钮。
2. store 先切换内存状态，保证当前 UI 立即响应。
3. adapter 写入 `expanded` 或 `collapsed`。
4. 写入失败不破坏当前交互，不记录敏感信息；重启可能恢复旧值或默认展开。

### 4.3 `/chat` placeholder 与本地输入

1. 页面 ready、textarea 为空且未聚焦时显示第一条。
2. 每 4 秒通过纯 model 递增 index，超过第五条回到第一条。
3. focus 或出现输入时暂停并清理 interval。
4. 清空且 blur 后从当前序列继续。
5. `prefers-reduced-motion: reduce` 时固定第一条且不创建轮播 interval。
6. 页面 unmount 时清理 interval 和 media-query listener；textarea ref 被释放。

### 4.4 导航

1. `/chat`、`/tasks`、`/settings` 使用真实 RouterLink/`router.push`。
2. 未实现模块呈 disabled，既不创建 route 也不响应点击/快捷键。
3. 上游投影给出 `visible=false` 时，item 在解析阶段被过滤，不进入 DOM。
4. 当前仓没有真实权限层；本需求只实现安全过滤接口和合成测试，不虚构服务端授权。

## 5. 状态模型

### 5.1 Sidebar

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 失败处理 |
|---|---|---|---|---|---|
| uninitialized | hydrate | storage=`collapsed` | collapsed | none | N/A |
| uninitialized | hydrate | storage=`expanded`/missing/unknown/throws | expanded | none | 捕获异常 |
| expanded | toggle | 用户激活 | collapsed | 尝试写 `collapsed` | 写失败保持 collapsed 内存态 |
| collapsed | toggle | 用户激活 | expanded | 尝试写 `expanded` | 写失败保持 expanded 内存态 |
| 任意 | route change | N/A | 保持 | none | 不重置 |

### 5.2 Placeholder

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 非法处理 |
|---|---|---|---|---|---|
| rotating | tick | empty + unfocused + motion allowed | rotating(next index) | 重置 timer | index 归一化到 0—4 |
| rotating | focus/input | N/A | paused | 清理 timer | 重复 pause 幂等 |
| paused | blur/clear | empty + motion allowed | rotating | 启动单一 timer | 已有 timer 不重复创建 |
| any | reduced-motion on | N/A | static-first | index=0、清理 timer | N/A |
| any | unmount | N/A | disposed | 清理 timer/listener | 后续事件忽略 |

### 5.3 Navigation

| 状态 | 行为 | 可聚焦 | Router | 可访问性 |
|---|---|---:|---|---|
| selected | 当前可用页面 | yes | current | `aria-current="page"` |
| enabled | 可导航 | yes | push/link | 完整 label；收起态 tooltip |
| disabled | 尚未开放 | no interactive action | none | disabled 语义 + “即将开放”说明 |
| hidden | 上游投影不可见 | no | none | 不进入 DOM/a11y tree |

## 6. 领域模型与不变量

| Entity/Value | Scope | 不变量 | 生命周期 |
|---|---|---|---|
| `SidebarMode` | 当前 Desktop 安装 | 只能是 `expanded` 或 `collapsed` | Web Storage 到应用数据清理 |
| `NavItemDefinition` | 构建版本 | 唯一 key；enabled 项必须有真实 route；disabled 项不得有可执行动作 | 应用版本 |
| `ResolvedNavItem` | 当前渲染 | `visible=false` 已被过滤；selected 来自 Router | 路由生命周期 |
| `PlaceholderIndex` | 当前 ChatPage | 整数 0—4；reduced-motion 强制 0 | 页面生命周期 |
| `LocalPrompt` | 当前 ChatPage | 不持久化、不发送、不记录 | 页面生命周期 |

## 7. 数据与 Migration

- 数据库、缓存、Keychain、服务端数据：N/A，无变化。
- 私有持久状态：新增一个普通 Web Storage key。

| Phase | Schema/Data action | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | 新 reader 支持无 key、两个合法值和未知值回退 | 旧 app 不受影响 | 无 key默认展开 | `PREF-001`—`PREF-004` | 删除 reader 即回旧行为 |
| Backfill | N/A；不扫描、不回填用户数据 | N/A | 首次切换才写入 | 确认首次启动无写入要求 | N/A |
| Switch | UI toggle 开始写 v1 key | 旧 app 忽略 key | 新 app 恢复选择 | `PREF-002`、`PREF-003`、重启 smoke | 回滚 UI；key 可遗留 |
| Contract | 当前不删除/重命名 v1 key | 旧 app 仍忽略 | 新 app 持续兼容 | 发布窗口验证 | 未来升级必须新增版本 key 或兼容 reader |

## 8. 一致性与韧性

- 事务：N/A；单 key 同步读写。
- 并发：单 WebView 主窗口；最后一次用户切换生效。
- 幂等：重复写相同值安全。
- 超时/取消：Web Storage 同步调用，无网络超时；组件销毁取消 interval。
- 重试：写失败不自动循环重试，避免阻塞 UI；下一次显式 toggle 再尝试。
- 限流/熔断：N/A。
- 部分失败：内存切换成功但持久化失败时，当前页面可用，重启后允许回退。
- 资源释放：placeholder interval、`matchMedia` listener 必须在暂停/unmount 时释放。

## 9. 安全与隐私

- 认证：只消费已有登录结果；当前代码尚无完整 session guard，本需求不发明认证协议。
- 资源授权：导航 `visible` 由上游投影决定；隐藏不是服务端授权。当前禁用模块没有 route，无法由导航深链。
- 租户：不读取、不构造、不持久化租户。
- 输入：textarea 是普通本地字符串，不提交；不得进入 storage、URL、console、日志、错误上报或 fixture。
- Secret/token：Web Storage 只允许 sidebar enum；禁止 token、cookie、Keychain 替代。
- Tauri：不新增 capability、command、plugin、sidecar、外部 URL 或 CSP。
- 高风险审批/审计：N/A；只有低风险 UI preference 写入。

## 10. 主题、可访问性与视觉

- 默认跟随系统；`App.vue` 集中解析 light/dark，设置 Naive theme 和根 `data-theme`。
- 1180×760 下两种 sidebar 宽度均无主体横向滚动；`tauri.conf.json` 计划补 `minWidth=1180`、`minHeight=760`，不改变 capability。
- Shell toggle 命中区域至少 32×32，动态 `aria-label` 和 `aria-expanded`。
- 可用 nav 有 visible focus；selected 同步 `aria-current`；collapsed 使用 tooltip。
- textarea 有稳定 label“输入你的跨境业务需求”，placeholder 不充当 label。
- reduced-motion 禁止 placeholder 轮播；其它布局动效使用 token 且不超过 240ms。
- Logo 使用批准资产，图标通过 `YjIcon` registry；不使用 base64、未知 SVG 或 CSS filter。

## 11. 可观测性

| Signal | 设计 | 成功条件 | 告警/停止条件 | Runbook |
|---|---|---|---|---|
| 服务端 metric/log/trace/audit | N/A：无网络与业务副作用 | 无新增调用 | 发现意外请求或正文日志即阻断 | 回退相关实现并检查 diff |
| UI error reporting | 不新增遥测 | storage 异常不导致白屏 | 未捕获异常、输入正文进入错误对象 | 删除记录点；回退默认展开 |
| Build/size evidence | Vite build 产物 diff | 仅迁入必要 token/assets/icons | 出现第二 UI/icon 库或异常大依赖 | 停止 S1，复核依赖 |
| Visual evidence | light/dark × 1180×760/1280×820/1440×900 × 240/72 | 无重叠、裁切或横向滚动 | 任一关键状态不可用 | 回到对应 slice 修正 |

## 12. 性能、容量与成本

| 项目 | 目标 | 测试方法 | 降级/停止 |
|---|---|---|---|
| 首页网络 | 0 个 FEAT-124 网络请求 | DevTools/代码 diff/Tauri smoke | 发现请求即停止 |
| Sidebar 切换 | CSS token 动效 ≤240ms，无 layout 卡死 | 实际窗口操作 | 关闭非必要动效 |
| Placeholder | 4000ms 间隔；最多一个 timer | fake timer 单测 + 实际检查 | 固定第一条 |
| Storage | 每次 hydrate 读一个 key、toggle 写一个 key | Storage stub 断言调用次数 | 读写异常回退内存态 |
| 新依赖 | 只允许已接受的 `@lucide/vue@1.27.0`；PostCSS 仅作 `8.5.18` 安全 override | package/workspace/lockfile diff + audit + build | 出现第二图标库或审计高危即阻断 |
| 外部费用 | 0 | 无 API/模型调用 | N/A |

## 13. 配置、发布与回滚

- Feature Flag：不新增；当前早期 Desktop 骨架直接替换。
- 默认：`/chat` 入口态、sidebar expanded、follow-system theme。
- 安全关闭：回滚 FEAT-124 实现提交；旧应用忽略 sidebar key。
- 配置验证：Tauri window min size、Router routes、storage enum 和 theme 均由测试/build/smoke 验证。
- 共存：旧 build 无 key；新 build 兼容无 key；回滚后遗留 key 无副作用。
- 清理：必要时删除 `yijie.desktop.ui.sidebar.v1` 恢复默认展开。

## 14. AI 功能专项

N/A。当前输入不调用模型，不改变 prompt、model、retrieval、skill、knowledge 或 tool schema，不需要 AI Eval。未来真实任务提交必须新建/扩展需求并重新进行契约、安全和 Eval 设计。

## 15. 方案比较

| 方案 | 优点 | 缺点/风险 | 结论 |
|---|---|---|---|
| A：全局 App Shell + 纯 domain adapter + 薄组件 | 三路由一致；逻辑可用现有 Vitest 测；持久化边界清晰 | 需要最小组件/token 迁移 | 选择 |
| B：继续在 ChatPage 内堆 Shell 和 storage | diff 表面较小 | Tasks/Settings 不一致；页面承载持久化；难测试 | 拒绝 |
| C：只做 240px、不持久化 | contract-impact 可保持 none | 不满足已确认 72px 与跨重启偏好 | 拒绝 |
| D：立即接真实 Chat/权限/API | 看似功能完整 | 严重扩大范围、契约和安全风险 | 拒绝 |

## 16. ADR 与批准

- ADR：N/A；仓库职责和跨仓依赖不变。本次通过 App Shell 2.0.0、Chat 1.1.0、Navigation 1.1.0 管理设计 Pattern 变化。
- 技术负责人：段成威。
- 安全/数据 Owner：段成威。
- Product/Design：Approved，2026-07-30。
- 技术设计：G2 Approved；段成威于 2026-07-30 明确批准，并限定先执行 S0。
