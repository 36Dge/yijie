# FEAT-124 — 易界桌面端登录后首页

## 1. 文档信息

| 字段 | 内容 |
|---|---|
| 状态 | Requirements Complete / G0—G3 Passed / S2—S4 Complete / S5 Authorized |
| 需求负责人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |
| 创建日期 | 2026-07-29 |
| 最后更新 | 2026-07-31 |
| 原始需求来源 | 用户提供的登录后首页视觉稿 |
| 视觉参考 | `/Users/jack/Downloads/Personal_Info/易界文档/00yiyjie_fronted/01_index.html` |

## 2. 一句话目标

已登录的跨境电商卖家打开易界 Mac 桌面端后，默认进入 `/chat` 的“新建任务”首页，在本地输入跨境业务需求，并通过可展开/收起的左侧导航访问现有 Tasks 和 Settings。

## 3. 问题与用户价值

- 目标用户：已登录的易界桌面端卖家用户。
- 当前问题：当前 `/chat` 页面仍是蓝色早期骨架，品牌、导航、布局和易界已接受设计系统不一致。
- 用户可观察结果：登录后看到绿色品牌 App Shell、标题“易界AI”、居中的本地任务输入区，以及 240px 展开/72px 收起的左侧导航。
- 用户价值：降低进入业务任务的操作和认知成本，使首页与易界品牌、Mac 桌面产品定位一致。
- 为什么现在做：当前应用骨架与已接受设计规范存在明显视觉和信息架构差异，继续在旧骨架上叠加功能会扩大设计系统债务。

## 4. 范围

### In Scope

- `yijie-desktop` 登录后主应用的默认首页视觉与 App Shell。
- 默认路由保持 `/chat`，默认展示“新建任务”首页。
- 240px 展开式和 72px 收起式左侧导航、品牌区、导航选中/悬停/焦点状态。
- 默认“新建任务”页面的标题“易界AI”、副标题、五条轮播 placeholder 和仅保存在当前页面内存中的任务输入区。
- 使用 Vue Router 表达导航状态，不使用 `hidden` 模拟生产路由。
- 易界品牌 token、亮色/暗色、最小窗口和可访问性落地。
- “我的店铺、工作台、定时任务、插件、资料库”等未实现导航暂时禁用。
- 现有 Tasks 以“任务记录”独立入口放在“新建任务”正下方，Settings 固定在侧栏底部。
- 无权限模块不出现在导航中。
- 本页不展示租户、店铺、同步、Runtime 状态或用户入口。
- 侧栏收起按钮固定在侧栏右边界并与品牌区垂直居中；状态以版本化普通本地偏好跨路由和应用重启保留。

### Out of Scope

- 登录后端、会话协议、token/Keychain/租户上下文方案。
- 真实任务创建 API、Agent Host 或 Codex Runtime 接入。
- 我的店铺、工作台、定时任务、插件、资料库的完整业务能力。
- Tauri capability、Rust command、sidecar、CSP 或外部网络权限变更。
- 新通用 UI 框架、新图标库和未经批准的视觉资产。
- 移动端或 Web 响应式页面。

## 5. 成功指标

| 指标 | 当前基线 | 目标值 | 测量窗口 | 数据来源 |
|---|---:|---:|---|---|
| 支持视口 | 当前页面仅有早期响应式骨架 | 1180×760、1280×820、1440×900 均可用 | 每次 UI 验证 | 浏览器与 Tauri 视觉检查 |
| 设计系统一致性 | 蓝色硬编码骨架 | 颜色、间距、字号、圆角、阴影均来自易界 token | Code Review | Diff 与设计审查 |
| 导航可达性 | Chat/Tasks/Settings 英文入口 | 新建任务、Tasks、Settings 可键盘访问；未实现项明确禁用；无权限项隐藏 | 自动化与人工验证 | 组件/路由测试 |
| 首页引导文案 | 单条预填 prompt | 5 条指定 placeholder 按顺序轮播，交互和 reduced-motion 行为可判定 | 自动化与人工验证 | 组件测试与视觉检查 |
| 工程门禁 | 未针对本需求执行 | `make lint && make test && make build` 通过 | 候选提交 | CI/终端证据 |

## 6. 约束

- 技术栈：Tauri v2、Vue 3、Vite、TypeScript、Pinia、Vue Router、Naive UI。
- 品牌主色由 `#95BF47` 设计决策派生，但业务组件只能消费语义 token。
- 图标使用 Lucide/YjIcon registry；参考 HTML 内联 SVG 不进入生产组件。
- Logo 使用批准资产；参考 HTML 的 base64 Logo 不是运行时权威源。
- 默认中文、专业文案，主题跟随系统并支持亮色/暗色。
- 最小窗口 1180×760，不得产生主体横向滚动。
- `docs/design/exports/` 只能作为迁移参考，活跃 `src/` 不得直接导入。
- 不得因本需求猜测认证、权限、租户或真实任务提交协议。

## 7. 已确认事实、假设与未知项

| 类型 | 内容 | 证据/来源 | Owner | 处理状态 |
|---|---|---|---|---|
| Fact | 参考稿默认展示“新建任务”、240px 左栏和 960px 居中输入区 | `01_index.html` 源码及 1440×900 渲染 | 需求负责人 | Confirmed as reference |
| Fact | 当前 `/` 重定向到 `/chat` | `yijie-desktop/src/router/index.ts` | 段成威 | Confirmed |
| Fact | 当前 Chat 页面为 220px 蓝色侧栏、英文 Chat/Tasks/Settings | `src/pages/chat/ChatPage.vue` | 段成威 | Confirmed |
| Fact | Design System 已接受绿色品牌、系统主题、1180×760 最小窗口和 240px 展开侧栏 | `docs/design/docs/design/00-final-decisions.md` 等 | 段成威 | Confirmed |
| Fact | 活跃 `src/` 尚未完整迁移 token、YjIcon 和 Yj* 组件 | `yijie-desktop/AGENTS.md` 与代码扫描 | 段成威 | Confirmed |
| Fact | 登录后默认路由保持 `/chat`，首页标题为“易界AI” | 用户确认，2026-07-30 | 需求提出人 | Confirmed |
| Fact | 输入框仅实现首页视觉与本地输入，不触发真实任务提交 | 用户确认，2026-07-30 | 需求提出人 | Confirmed |
| Fact | 未实现的其他产品导航暂时禁用；无权限模块隐藏 | 用户确认，2026-07-30 | 需求提出人 | Confirmed |
| Fact | 本页不展示租户、店铺、同步、Runtime 状态和用户入口 | 用户确认，2026-07-30 | 需求提出人 | Confirmed |
| Fact | 左侧导航支持 240px 展开和 72px 收起；Settings 位于底部；现有 Tasks 保持独立 | 用户确认，2026-07-30 | 需求提出人 | Confirmed |
| Fact | 需求负责人、Reviewer 和发布负责人均为段成威，当前里程碑日期均为 2026-07-30 | 用户确认，2026-07-30 | 段成威 | Confirmed |
| Fact | 首页依次轮播用户指定的 5 条 placeholder；每 4 秒切换，聚焦/输入时暂停，reduced-motion 时固定第一条 | 用户提供文案并授权 Codex 定稿交互 | 段成威 | Documented for review |
| Fact | Tasks 文案为“任务记录”，位于“新建任务”正下方并与后续业务模块分组 | 需求负责人授权 Codex 定稿 | 段成威 | Documented for review |
| Fact | 收起按钮位于侧栏右边界并与品牌区垂直居中；状态跨路由和重启持久化，异常时回退 240px | 需求负责人授权 Codex 定稿 | 段成威 | Documented for review |
| Fact | `/chat` 规范区分新建任务入口态和未来活跃会话态；入口态没有顶部状态、会话列表或右侧面板 | Accepted App Shell 2.0.0 / Chat 1.1.0 | 段成威 | Confirmed |
| Fact | 当前不调用 API、Agent Host 或 Runtime；因新增版本化侧栏本地偏好，整体 `contract-impact = additive`，公共 wire 仍为 none | Contract Impact 复核 | 段成威 | Confirmed for design |

## 8. 初始仓库基线

| Repository | Remote | Branch | Full HEAD SHA | Worktree | Existing changes owner |
|---|---|---|---|---|---|
| yijie | `https://github.com/36Dge/yijie.git` | develop | `82f39ee97e40f5932c6f59a5567342ee4c8aaf04` | clean before package creation | N/A |
| yijie-desktop | `https://github.com/36Dge/yijie-desktop.git` | develop | `09d987f09c2f2eac2575187ef57b9b65d1e89ae3` | clean | N/A |

## 9. 里程碑与状态

| 里程碑 | 目标日期 | Owner | 状态 |
|---|---|---|---|
| G0 需求建档 | 2026-07-30 | 段成威 | Passed |
| G1 设计就绪 | 2026-07-30 | 段成威 | Passed |
| G2 可开始实现 | 2026-07-30 | 段成威 | Passed；用户明确批准 |
| G2A 私有契约就绪 | 2026-07-30 | 段成威 | Passed；用户明确批准并授权执行 S1 |
| G4 Code Complete | 2026-07-30 | 段成威 | Pending |
| G5 Production Ready | 2026-07-30 | 段成威 | Pending |
| G6 Delivery Complete | 2026-07-30 | 段成威 | Pending |

## 10. 变更日志

| 日期 | 修改人 | 变化 | 原因/批准 |
|---|---|---|---|
| 2026-07-29 | Codex | 创建 Brief，写入已验证事实与阻塞项 | 用户要求创建 Feature Package |
| 2026-07-30 | Codex | 写入默认路由、标题、输入范围、导航、顶部状态、侧栏、Settings、Tasks 与权限呈现决策 | 用户逐项确认 |
| 2026-07-30 | Codex | 补齐 Owner/里程碑，定稿 placeholder、任务记录位置、侧栏偏好，并同步 Desktop 设计 Pattern | 段成威提供信息并授权 Codex 设计 |
