# FEAT-151 — Desktop 工作流展示页 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Created: `2026-08-31`

## 1. 用户问题与结果

- 目标用户：需要快速浏览现有与推荐自动化工作流的跨境电商卖家和运营人员。
- 当前问题：左侧“工作台”仍是禁用入口，参考截图中的工作流总览没有页面承载。
- 用户完成后能看到或使用的真实结果：点击左侧“工作流”进入 `/workflows`，完整浏览截图中的分类、已有工作流和推荐工作流信息。
- In scope：导航更名并启用；静态呈现截图的全部信息；复用易界设计系统；覆盖亮色、暗色、1180×760 与基本可访问性；修复 canonical demo_fast 启动器在 macOS Bash 3.2 `nounset` 下的空数组兼容问题。
- Out of scope：任何接口、持久化、筛选、排序、视图切换、新建、更多、查看全部、演示、执行或二次跳转实现。

## 2. 完整主流程

1. 用户通过 canonical `demo_fast` 启动器零登录进入应用。
2. 固定本地身份具有 `workspace.use`，用户点击左侧“工作流”，路由进入 `/workflows`，侧栏条目保持 selected。
3. 页面从上至下展示九个顶部分类、“我的工作流”和“推荐工作流”。
4. 用户滚动浏览全部静态卡片；页面内视觉控件不响应点击、不请求接口、不持久化也不跳转。

## 3. 交互与 UI

- 视觉方向：保留截图的双层分类、五列已有工作流卡与四列推荐工作流卡信息架构；使用易界品牌绿、标准密度、轻边框和 token 化卡片层级，不复制外部品牌色或未知品牌图标。
- 页面结构：`YjPage` → 顶部分类导航 → `YjSection`“我的工作流” → 静态工具条与卡片网格 → `YjSection`“推荐工作流” → 推荐卡片网格。
- 主次操作：页面不存在可用操作。截图中的按钮、切换器、排序、更多、查看全部、演示和执行均以明确不可用的展示语义呈现。
- Idle：由侧栏“工作流”链接提供入口；不预取数据。
- Loading：不适用；内容来自同步打包的只读常量。
- Success：所有标题、标签、描述、修改时间、使用量、流程节点和操作文案完整展示。
- Empty：不适用；固定展示集合不为空。
- Error：无 `workspace.use` 的深链由既有 Router guard 在页面加载前拦截。
- Retry：不适用远程重试；权限恢复沿用既有设置/权限刷新链路。
- Cancel：不适用；没有提交、执行或其他副作用。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 左侧“工作台”变为“工作流”；拥有 `workspace.use` 时可进入 `/workflows`，selected 与标题正确。 | 导航、Router、Sidebar 测试；真实 smoke。 |
| AC-002 | 顶部按截图顺序显示九个分类。 | 领域模型、组件测试和截图。 |
| AC-003 | “我的工作流”显示全部分类/工具条、创建卡和四张已有工作流卡的完整信息。 | 组件内容与顺序断言；截图。 |
| AC-004 | “推荐工作流”显示刷新/查看全部，以及四张推荐卡的完整信息、节点、使用量和操作文案。 | 领域模型、组件测试和截图。 |
| AC-005 | 页面内所有截图控件仅展示，不请求、不写入、不执行、不跳转。 | 否定断言、调用搜索和 smoke。 |
| AC-006 | 页面只消费本地只读模型，无 API/Tauri/Runtime/持久化依赖。 | 源码审阅和调用搜索。 |
| AC-007 | 缺少 `workspace.use` 时导航隐藏且深链在页面实例化前拒绝。 | 权限、Router、Sidebar 测试。 |
| AC-008 | UI 使用 `Yj*`、token 和 registry，light/dark 及 1180×760 无关键重叠或主体横向滚动。 | lint/build 与视觉矩阵。 |
| AC-009 | 页面语义清晰、展示控件不伪装可用，axe 无 serious/critical violation。 | 组件语义、axe 和键盘 smoke。 |
| AC-010 | canonical `pnpm tauri:dev` 在 macOS Bash 3.2 的空可选 profile 环境下完成 Desktop/Host ready，并可正常退出清理。 | 启动器回归、静态契约检查与 fresh canonical 启动。 |

## 5. 工程事实与边界

- 受影响仓库：`yijie` 保存 FEAT-151 四文件治理包；`yijie-desktop` 保存展示模型、页面/卡片、route/navigation/permission 与测试。其他兄弟仓不受影响。
- 真实入口：在 `yijie-desktop` 运行 `pnpm tauri:dev`，通过 local demo_fast 正常入口进入应用后点击“工作流”。`pnpm dev` 只能辅助视觉诊断，不能替代 D4。
- local direct-entry 与权限：沿用 ADR-0018；固定 local scope 已包含 `workspace.use`。不修改 capability、身份、租户或 public/production 权限边界。
- `contract-impact`：`none`。变更仅存在于 Desktop 进程内静态 TypeScript 模型、Vue 组件和 Router；Desktop↔API/Agent Host/Runtime wire、Tauri command、持久化、durable event 和 replay 均无可观察变化。
- 权威源与 source-first：公共契约不适用；先固化本 Feature 的截图内容模型，再实现组件/页面，最后接入既有 `workspace.use` 导航与 Router。
- 数据与外部操作：文案、时间和使用量完全来自用户提供的截图；不读取 PII、店铺数据、token 或 secret；付费和生产写入额度为 0。用户在本线程明确授权仅为完成 FEAT-151 而执行 canonical 构建产生的既有 Host/Desktop executable 覆盖；覆盖前 Host 已做可恢复备份，禁止范围未扩大到强杀、故障注入、权限破坏或其他仓库数据。
- 工作区：`yijie` 的既有 FEAT-137 治理文档改动与 `yijie-desktop` 当前分支内容均保持原状；FEAT-151 不切分支、不 reset/checkout、不覆盖或批量格式化范围外源码。canonical 构建产物覆盖仅按上述用户例外授权执行。

## 6. 推荐方案与停止条件

- 推荐方案：用一个纯领域模型固定截图信息；建立两种职责单一的工作流卡片组件；页面只做 `YjPage/YjSection` 组合；新增 exact `local + demo_fast` 展示开关，沿用现有 `workspace.use` 权限；用 Bash 3.2 安全的可选数组展开保持 canonical 启动链路兼容。
- 取舍：顶部和卡片图标全部使用现有/新增 Lucide registry 语义图标；不自行复刻抖音、小红书等未经授权的品牌 Logo，而用带文字的中性平台节点保留信息语义。
- 30 分钟无新证据：停止猜测式 CSS/Router 补丁，检查失败测试、路由状态和实际计算样式。
- 90 分钟同一阻塞：保留全部信息与 Must AC，优先减少非关键装饰和动效，使用稳定 CSS Grid 完成布局。
- 超过 16 小时：停止扩展非 Must 自动化或装饰；不得删除截图信息、权限边界、主题、1180×760 或可访问性验收。
