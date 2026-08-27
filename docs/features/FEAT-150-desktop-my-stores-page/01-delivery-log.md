# FEAT-150 整体实现与调试记录

## 1. 整体实现方案

- 真实调用链：App Shell 左侧导航 → Vue Router `/store` + `store.read` guard → `StorePage` → 进程内只读合成模型与 `Yj*` 组件；没有店铺、API、Runtime、数据库或持久化 I/O。
- 跨层实现顺序：先通过 D0；再固定 PDF 九页中的快报、精选筛选、角色筛选和场景标题；随后实现纯领域模型、通用 tabs/指标/场景卡、页面组合，最后接入 route/navigation/权限并跑真实 Tauri 验收。
- Contract First：`contract-impact=none`。本需求没有新增公共/private wire、Tauri command、数据库 schema、durable event 或 replay 语义。
- 明确不做：真实店铺接入、授权、搜索、查看全部、分页、场景执行、保存、预览、付费调用、生产写入和公网发布。

本 Profile 不建立治理切片；以一个完整可观察的 Desktop 用户结果统一验收。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| `yijie-desktop` | `src/domain/store-showcase.ts` 及测试 | 新增 3 组快报（每组 5 指标）、9 个精选筛选、6 个角色筛选、54 个去重合成场景及纯筛选函数 | 覆盖 PDF 全部页面内容，同时保证无真实数据依赖 |
| `yijie-desktop` | `YjTabs`、`YjMetricCard`、`StoreSceneCard` 及测试 | 新增 token 化可复用展示组件；tabs 支持 tablist/tab、roving tabindex、方向键、Home/End | 提供可访问、可单测的统一交互与视觉语言 |
| `yijie-desktop` | `src/pages/store/StorePage.vue` 及测试 | 实现经营快报、精选场景、角色场景推荐三模块；按反馈移除独立“演示内容”提示条，保留模块口径、来源标签、筛选与空态 | 形成更紧凑的“我的店铺”页面，同时维持合成数据边界 |
| `yijie-desktop` | `src/components/store/StoreSceneCard.vue` | 将场景标签统一为 32px 高、两字标签最小 48px 宽和相同内边距/字重，移除全部标签描边与静态卡片伪交互 hover | 修复精品、热门、关联等标签尺寸漂移，并让不可点击卡片不再暗示操作 |
| `yijie-desktop` | store UI config、App、App Shell、navigation、router、permission policy 及测试 | 仅在 exact `local + demo_fast` 暴露 `/store`；启用导航并以既有 `store.read` 保护路由与可见性 | 不扩大 public/production 暴露，不改变 capability 权威来源 |
| `yijie-desktop` | `tests/visual/feat-150/*` | 新增生产组件视觉 harness，支持 1180×760、light/dark 与 axe 证据 | 对齐 Desktop UI 交付门禁，不以截图代替真实 Tauri 启动 |
| `yijie` | `docs/features/FEAT-150-desktop-my-stores-page/*` | 建立 v3 `demo_fast/local` Feature Package 和九张视觉证据 | 落实 codex-feature-delivery D0/D4 治理 |

## 3. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复 | 结果 |
|---|---|---|---|---|
| 2026-08-26 | PDF 目录文本写“放差评”，对应截图全部写“防差评” | 九页逐页渲染核对，截图语义与多页标签一致 | 采用“防差评”，在 Brief 明确记录目录笔误 | PASS |
| 2026-08-26 | PDF 广告页标题与截图内销售激活态存在矛盾 | 第 4 页更像复用态截图，不能把销售指标误当广告数据 | 保留“近 7 天店铺广告”需求，构建广告销售额、花费、订单、ACOS、ROAS 五项合成指标 | PASS |
| 2026-08-26 | 初版组件集成测试出现 wrapper 返回类型与标题空格期望差异 | 测试辅助类型及 PDF 标题原文精确性不足 | 修正测试辅助类型与精确标题映射；focused tests 复跑 | PASS |
| 2026-08-26 | Browser `fullPage` 只能覆盖 App 内部滚动容器的当前视口 | App Shell 主内容使用独立滚动区，document 本身不增长 | 分别捕获首屏、精选筛选和角色筛选视口；同时读取完整 DOM/AX tree | PASS |
| 2026-08-26 | `pnpm tauri:dev` 裸开发二进制未被 macOS Computer Use 枚举 | 未签名 dev process 不在辅助功能应用目录，但 Tauri、Vite 与 Host 均已真实 Running | canonical fresh startup 独立验收；再用同一 local demo 启动器构建可枚举 debug `.app` 完成原生点击、筛选与键盘截图 | PASS |
| 2026-08-26 | 路由拒绝测试只断言跳转，未显式证明 Store loader 未运行 | AC-010 要求在页面实例化前拒绝 | 将 Store loader 改为 spy，补充 denied 路径 `not.toHaveBeenCalled()` 断言 | PASS |
| 2026-08-27 | 用户反馈独立“演示内容”提示条占据首屏空间，场景标签尺寸和描边不统一 | 真实 1180×760 渲染确认：标签随文字与边框自适应，静态卡片还有 hover 反馈 | 删除提示条；统一标签几何尺寸与字重、取消描边和静态 hover；为模块增加轻量层级阴影 | PASS |
| 2026-08-27 | 去掉描边后，axe 报告精品/热门标签文字对比度不足 | 浅色主题下原 warning/error 文字与软色背景的对比度分别为 3.07/4.41 | 标签改用主文字色，保留类型软色背景；重载 light/dark 后 axe 均为 0 violations | PASS |
| 2026-08-27 | 最终源码 fresh Tauri 启动被既有本地 Demo 占用 1420/18081 阻止 | 端口由 01:00 启动且不属于本轮的 Vite/Agent Host 进程占用，没有可安全识别的应用窗口可正常退出 | 不强杀或接管既有进程；保留 2026-08-26 fresh Tauri PASS 基线，以本轮 focused tests、全量前端 641 项、lint/typecheck、production build 和真实浏览器渲染验证 UI delta | 受控跳过，无 UI 影响 |

所有测试均为正常、非破坏性开发验证；未执行强杀进程、恶意 fixture、可执行文件替换或权限破坏。本轮发现既有 Rust sidecar 故障生命周期用例失败后，依据安全条款没有反复执行该故障场景；本轮启动的视觉服务通过正常 Ctrl-C 退出。既有本地 Demo 进程保持原样。

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费调用 | N/A | N/A | 0 | 0 | 未调用 |
| 破坏性操作 | N/A | N/A | 0 | 0 | 未执行 |
| 生产/外部写入 | N/A | N/A | 0 | 0 | 未执行 |

页面使用的金额、订单、比率、库存、趋势、热度、ASIN 和说明均为本地合成内容；没有发送用户文件、密钥或店铺数据。

## 5. 已知限制

- 功能按 Feature Profile 仅在 `local + demo_fast` 暴露；不代表 public/production 已发布。
- 两个“全部”状态按参考稿首屏编排展示 6/12 张卡；PDF 的 54 个去重场景均可通过具体经营目标或角色标签访问，页面按要求不提供搜索与分页。
- canonical `pnpm tauri:dev` fresh startup 已 PASS；原生交互截图使用同一 local demo 启动器生成的可枚举 debug app bundle，原因是裸开发二进制未出现在 macOS 辅助功能应用目录。
- 工作区中既有 FEAT-131 未提交改动保持原样；五个重叠风险文件在启动前后 SHA-256 完全一致，本需求没有 reset、checkout、覆盖或提交这些文件。
