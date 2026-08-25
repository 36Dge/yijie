# FEAT-130 — Desktop UI 布局调整 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Checkpoint: `D0` · Created: `2026-08-25`

## 1. 用户问题与结果

- 目标用户：在易界 AI Desktop 中新建任务、切换项目并回看本地对话的用户。
- 当前问题：主导航顺序与最新业务优先级不一致；任务记录仍跳往独立页面；项目与对话树挂在“新建任务”下且长列表没有独立滚动区；主页项目选择条的层级与背景对比偏弱。
- 真实结果：用户在一个稳定的 App Shell 中按批准顺序浏览入口，在“任务记录”下直接按项目展开对话，点击对话进入 Chat；主页项目选择条更清晰且保持易界设计语言。

### In scope

- 主导航顺序固定为“新建任务、我的店铺、工作台、定时任务、插件、资料库、任务记录”。
- “任务记录”改为无跳转静态分组，第一层项目、第二层对话，列表区域独立滚动。
- 移除 `/tasks` 独立页面、页面布局、lazy route 与导航关系。
- 保留项目移除后的历史对话可发现性，使用“项目已移除”安全分组。
- 主页项目选择条圆角由 8px 增加到 12px，并提高未 hover 背景与页面背景的轻微对比。
- 同步测试与 yijie Desktop Design System override 文档。

### Out of scope

- 不改变 Desktop、Agent Host、API、Runtime 或公共契约。
- 不改变项目/session 排序、重命名、置顶、删除、持久化或安全授权语义。
- 不恢复已移除项目的真实路径或名称，不新增 IPC 字段。
- 不实现当前仍标记“即将开放”的业务模块。

## 2. 完整主流程

1. 用户通过 canonical `demo_fast` local 启动器零登录交互进入 Desktop。
2. 左侧主导航按批准顺序显示；资料库后为任务记录，设置仍固定在底部。
3. 任务记录标题本身不导航；项目文件夹与其对话记录显示在标题下方。
4. 用户展开项目并点击对话，应用进入 `/chat/:sessionId`；只有具体对话显示当前页语义。
5. 对话较多时，仅任务记录树滚动，顶部导航和底部设置保持可见。
6. 用户在主页通过 12px 圆角、对比更清晰的项目选择条选择本地项目并继续既有任务流程。

## 3. 交互与 UI

- 视觉方向：完全使用 `yijie-desktop/docs/design/docs/design` 的语义 token、`YjIcon` 与现有组件；不新增视觉资产或硬编码色值。
- Idle/Success：项目树显示当前项目与对话，项目选择条使用 `radius-lg + bg-app`，hover 不增加描边。
- Loading：任务树区域内显示稳定加载文案，导航位置不跳动。
- Empty：任务树显示“暂无任务记录”。
- Error / permission denied：显示稳定中文原因；已加载的安全元数据仍可浏览。
- Retry：沿用 Chat store 与现有恢复入口；本需求不新增网络或原生重试。
- Cancel：N/A；本需求没有新增可取消操作，现有删除/移除确认保持不变。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 主导航顺序精确为新建任务、我的店铺、工作台、定时任务、插件、资料库、任务记录；设置仍置底 | 导航单测 + 1180×760 截图 |
| AC-002 | 任务记录不是链接/按钮，不改变路由；`/tasks` 页面、loader 和 route 不存在 | 组件与路由单测 + source inventory |
| AC-003 | 任务记录按项目→对话两层显示，点击对话进入 `/chat/:sessionId`；已移除项目历史位于“项目已移除”组 | Tree 单测 + 真实 UI smoke |
| AC-004 | 长任务列表只在任务记录区域滚动，主导航与设置不被推出视口 | 1180×760 长列表视觉检查 |
| AC-005 | 主页项目选择条为 12px 圆角，未 hover 使用轻微对比的语义背景；hover 不增加描边，focus 与暗色主题清晰 | static/hover/light/dark 截图 + token source check |
| AC-006 | 核心流程保持键盘可用，无严重/致命 axe 问题，200% zoom 和 reduced-motion 不遮挡关键操作 | focused accessibility + 人工视觉矩阵 |

## 5. 工程事实与边界

- 受影响仓库：`yijie-desktop`（实现、测试、设计规范）；`yijie`（Feature Package）。
- 真实入口：`cd ../yijie-desktop && pnpm tauri:dev`。
- 工作区：两个仓库均已有 FEAT-128、demo_fast 治理等未提交改动；本需求只做最小增量，不 reset、覆盖或提交。
- `contract-impact = none`：只改变 Desktop 进程内 Vue 路由/布局与 CSS；Desktop↔Host/API/Runtime wire、持久化 schema、重放和 native capability 均不变。
- 数据/密钥/外部写：不新增数据采集、付费调用、生产写入或破坏性外部操作；删除的是 Git 可恢复的旧 Vue 页面源文件。

## 6. 推荐方案与停止条件

- 推荐方案：复用现有 `ChatSidebarTree` 与同一 Pinia 权威元数据，把任务记录建模为静态 section；前端为 orphan session 生成安全的“项目已移除”分组，不扩展 IPC。
- 30 分钟无新证据：读取完整 router、permission lifecycle、store 与 SQL 排序链路，不做猜测式 CSS/状态补丁。
- 90 分钟同一阻塞：保留静态任务记录树与 `/chat/:sessionId` 核心结果，延后非核心视觉 harness 扩展。
- 超过 16 小时：停止扩建，保留 AC-001–005 的最小完整结果并重新评估 AC-006 的人工矩阵。
