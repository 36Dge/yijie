# FEAT-124 测试与验证计划

## 1. 测试策略

- 风险等级：`medium`。业务副作用低，但影响全局 App Shell、路由、主题、可访问性和一个跨版本本地偏好。
- 测试原则：纯规则下沉为 TypeScript 并用现有 Vitest 验证；Vue 渲染、主题、布局和键盘行为必须在真实浏览器/Tauri 窗口验证。
- 阻断质量门槛：所有 Must AC 有证据；`make lint && make test && make build && pnpm docs:build` 通过；`PREF-*` 兼容测试通过；light/dark 与三个目标视口、两种 sidebar 模式均检查。
- 类生产依赖：本地 Tauri WebView、系统 light/dark、普通 Web Storage；无 API、数据库、Agent Host、Runtime、模型或第三方账户。
- 当前限制：仓库没有 Vue component-test DOM 环境或 visual regression runner；不得把纯 TS 绿色替代实际 UI/Tauri 验证。

## 2. AC → 测试追踪矩阵

| AC/NFR | 主要风险 | Test ID | 层级 | 场景 | 环境 | 预期证据 |
|---|---|---|---|---|---|---|
| AC-001 | 默认路由/旧骨架残留 | ROUTE-001、SMOKE-001 | router unit + smoke | `/`→`/chat`，新建任务 selected | memory router + Tauri | 断言 + `/chat` 截图 |
| AC-002、NFR-001 | 240/72px、裁切/滚动 | VIS-001—VIS-006 | visual | 1180×760、1280×820、1440×900 × 两模式 | browser/Tauri | 尺寸矩阵截图与检查记录 |
| AC-003 | 导航顺序、disabled/hidden、Settings 位置 | NAV-001—NAV-005 | pure unit + visual | 任务组、业务组、底部组、权限过滤 | Vitest + Tauri | nav config 断言 + 截图 |
| AC-004 | 输入被提交/持久化/记录 | INPUT-001—INPUT-003 | unit + smoke + diff | 输入、切路由、重启、网络/存储检查 | browser/Tauri | 无请求、无正文 storage/log |
| AC-005 | Router/focus/disabled 误导航 | ROUTE-002—ROUTE-005 | router unit + keyboard smoke | `/chat`、`/tasks`、`/settings`、disabled | memory router + Tauri | 路由/选中/focus 记录 |
| AC-006、NFR-002 | 暗色不可读/主题不同步 | THEME-001—THEME-003 | unit + visual | follow-system light/dark | matchMedia stub + Tauri | 两主题截图 |
| AC-007、NFR-003 | 键盘、ARIA、reduced-motion | A11Y-001—A11Y-006 | unit + manual a11y | tab、toggle、tooltip、label、motion | browser/Tauri | 键盘检查表 |
| AC-008、NFR-006 | 工程门禁 | GATE-001—GATE-004 | repo gates | lint/test/build/docs | local + CI | 命令、exit code、SHA |
| AC-009、NFR-007 | placeholder 顺序/计时/泄漏 | PH-001—PH-007 | pure unit + fake timers + visual | 五条循环、pause、resume、reduce、dispose | Vitest + browser | 断言 + 观察记录 |
| AC-010 | 本地偏好兼容/损坏/异常 | PREF-001—PREF-006 | conformance unit + restart smoke | no key、两值、unknown、throws、rollback | Vitest + Tauri | 兼容矩阵 |
| NFR-004 | 第二套 token/icon | MAINT-001 | static/diff review | 硬编码、直接 Lucide import、exports import | repository | `rg`/diff 证据 |
| NFR-005 | secret/正文泄漏 | SEC-001—SEC-004 | unit + static + smoke | storage、console、URL、权限过滤 | Vitest + Tauri | 无敏感写入 |

## 3. 领域与边界测试

| 类别 | 正常 | 边界 | 非法/失败 | Test IDs |
|---|---|---|---|---|
| Sidebar preference | 读写两个合法值 | 无 key、重复写 | unknown、空、get/set throw | PREF-001—PREF-006 |
| Placeholder | 0→1→…→4→0 | focus/blur、empty/non-empty | 多 timer、dispose 后 tick、reduced-motion | PH-001—PH-007 |
| Navigation projection | 三个 enabled 路由、五个 disabled 项 | collapsed tooltip、selected | `visible=false`、disabled click | NAV-001—NAV-005 |
| Router | `/` redirect、三条真实路由 | direct `/tasks`、`/settings` | 禁用模块没有 route | ROUTE-001—ROUTE-005 |
| 输入正文 | 页面内编辑 | 清空、切路由 | storage/network/log 出现正文 | INPUT-001—INPUT-003 |
| 公共 API/事件 | N/A：无调用 | N/A | 发现新增调用即失败 | SEC-003 |
| 数据库/事务 | N/A：无数据库 | N/A | N/A | N/A |
| 外部服务 | N/A：无外部服务 | N/A | N/A | N/A |
| UI/可访问性 | light/dark、两 sidebar、三视口 | 长文案、focus-visible | 重叠、陷阱、无 label | VIS-*、A11Y-* |

## 4. 兼容与 Conformance

- 公共未知字段/enum/event：N/A；无公共 wire。
- 私有值域：reader 只接受 `expanded`、`collapsed`，其它值安全回退。
- 新旧组合：覆盖旧 app/新 key、新 app/无 key、新 app/合法/未知 key。
- Generator 漂移：N/A；`pnpm generate` 是占位，不能作为证据。
- Canonical schema：App Shell Pattern 2.0.0；实现共享常量必须与文档一致。
- Runtime/第三方：N/A。

| Test ID | 组合 | 预期 |
|---|---|---|
| PREF-001 | new reader + no key | `expanded` |
| PREF-002 | new writer/reader + `expanded` | `expanded`，一次 key 写入 |
| PREF-003 | new writer/reader + `collapsed` | `collapsed`，一次 key 写入 |
| PREF-004 | new reader + empty/unknown/corrupt | `expanded`，不抛错 |
| PREF-005 | old app + v1 key / rollback | 旧 app 忽略；新 app 再升级仍可读 |
| PREF-006 | storage get/set throws | 读回退；写失败不破坏当前内存 UI |

## 5. 安全与隐私测试

| Test ID | 威胁 | 场景 | 预期结果 |
|---|---|---|---|
| SEC-001 | 任务正文进入持久化 | 输入五类业务文本并检查 Web Storage | 只有 sidebar key；无正文 |
| SEC-002 | 任务正文进入 URL/日志 | 输入后切路由、触发普通错误检查 | URL、console、错误信息无正文 |
| SEC-003 | 隐式外部调用 | 首页输入、placeholder、sidebar 操作 | 无 fetch/API/Agent/Runtime 调用 |
| SEC-004 | 无权限模块被展示 | nav resolver 注入 `visible=false` | item 不在输出和 DOM；disabled 不等于授权 |
| SEC-005 | storage 被滥用为 secret 容器 | 检查 writer API 和调用点 | writer 只接受封闭 enum 与固定 key |

## 6. 韧性与资源释放

| Test ID | 故障 | 注入方式 | 恢复预期 | 观测 |
|---|---|---|---|---|
| RES-001 | `getItem` 抛错 | 合成 Storage stub | `expanded`，页面继续 | unit assertion |
| RES-002 | `setItem` 抛错 | 合成 Storage stub | 当前内存切换成功，无未捕获异常 | unit assertion |
| RES-003 | 损坏 preference | 写入未知字符串 | 默认 240px | unit + restart smoke |
| RES-004 | 重复 focus/blur | fake timers 多次切换 | 最多一个 timer | timer count/assertion |
| RES-005 | 页面销毁 | unmount/dispose 后推进 timer | 无状态更新、listener 清理 | unit/manual |
| RES-006 | 系统主题变化 | mock/实际切换系统主题 | 页面无刷新、输入不丢失 | unit + Tauri |

网络超时、限流、断线、服务端重试和部分服务失败均为 N/A，因为本需求没有网络或服务调用。

## 7. Migration/回滚演练

| 组合 | 数据状态 | Reader/Writer | 预期 | 校验 |
|---|---|---|---|---|
| old app + no key | 未安装 FEAT-124 | 无 reader/writer | 旧行为 | baseline smoke |
| new app + no key | 首次升级 | new reader | 240px expanded | PREF-001 |
| new app + valid key | 已切换模式 | new reader/writer | 恢复对应模式 | PREF-002/003 + restart |
| new app + invalid key | 损坏/未来值 | new reader | expanded | PREF-004 |
| rollback + v1 key | 新版写过后回旧版 | old app ignores | 旧版正常 | PREF-005 |
| roll-forward again | 旧版保留 key 后再升级 | new reader | 合法值恢复，非法值回退 | restart smoke |

无数据库 migration、backfill 或 destructive cleanup。

## 8. 性能与容量

| Metric | Workload | Pass threshold | Stop threshold |
|---|---|---|---|
| FEAT-124 网络请求 | 输入、导航、toggle 10 次 | 0 | 任意新增请求 |
| placeholder timer | 连续 5 轮 + focus/blur | 同时最多 1 个；4000ms 顺序 | 多 timer、乱序、销毁后执行 |
| storage 调用 | hydrate + toggle 10 次 | hydrate 1 read；每 toggle 最多 1 write | 循环读写或写入正文 |
| sidebar transition | 240↔72 连续切换 | ≤240ms token；无明显卡顿 | 内容重叠/横向滚动 |
| 目标窗口 | 6 个 width/mode 组合 × light/dark | 全部可用 | 任一关键操作不可达 |
| 外部费用 | 全流程 | 0 | 任意付费/模型调用 |

## 9. AI Eval

N/A。本需求不调用模型、prompt、skill、knowledge、retrieval 或 tool，不得用主观对话代替 UI、兼容与可访问性验证。

## 10. Fixture 与测试数据

| Fixture/Dataset | 权威位置 | 分类 | 生成方式 | Consumer |
|---|---|---|---|---|
| Sidebar enum + invalid values | `sidebar-preference.test.ts`，语义引用 App Shell 2.0.0 | Public synthetic | 手写 `expanded/collapsed/unknown/empty` | PREF-* |
| Placeholder 五条文案 | `placeholder-rotation.ts`，内容引用 Chat 1.1.0 | Internal synthetic copy | 已批准中文文案 | PH-*、ChatPage |
| Nav definitions | `app-nav.ts` | Internal synthetic config | 路由/文案配置 | NAV-*、YjSidebar |
| 用户输入样例 | 测试内短合成字符串，不使用真实商家数据 | Potentially Confidential semantics / synthetic content | “测试输入” | INPUT-*、SEC-* |

Feature 文档只记录语义，不复制生产用户数据。

## 11. 实际执行命令

| 层级 | Repository/CWD | Command | 环境依赖 | 执行阶段 |
|---|---|---|---|---|
| Local preference conformance | `yijie-desktop` | `pnpm exec vitest run src/domain/sidebar-preference.test.ts` | Node 24–26、pnpm 11 | G2A |
| Domain/nav/router unit | `yijie-desktop` | `pnpm test -- src/domain/placeholder-rotation.test.ts src/navigation/app-nav.test.ts src/router/index.test.ts` | Node 24–26 | 每切片 |
| Full lint | `yijie-desktop` | `make lint` | Node/pnpm/Rust | baseline、G2A、G4 |
| Full test | `yijie-desktop` | `make test` | Node/pnpm/Rust | baseline、G2A、G4 |
| Frontend build | `yijie-desktop` | `make build` | Node/pnpm | baseline、G2A、G4 |
| Production dependency audit | `yijie-desktop` | `pnpm audit --prod` | npm advisory service | 新增/更新依赖、G4/G5 |
| Design docs | `yijie-desktop` | `pnpm docs:build` | VitePress | 设计/G2/G4 |
| Native visual smoke | `yijie-desktop` | `pnpm tauri:dev` | macOS GUI | S5/G4；人工记录 |
| Release build CI | GitHub Actions | `pnpm tauri:build --debug` + audits | macOS runner | G5 |
| Feature docs gate | `yijie` | `check-feature-package.sh --gate G2|G3|G4|G5|G6` | Bash | 各 Gate |

当前没有 Playwright、Vue Test Utils、jsdom/happy-dom 或 visual regression runner；除非段成威另行批准新增测试依赖，否则计划不声称存在自动组件 E2E。

## 12. 通过、失败与 Flaky 策略

- PASS：命令完成、exit code 0、断言符合 AC，视觉矩阵有真实截图/检查记录。
- FAIL：任何 Must AC、compatibility、安全、lint、test、build 或目标视口失败。
- NOT RUN：未执行、环境缺失、进程未完成、输出被跳过；不得写 PASS。
- Flaky：调查 timer、system theme、GUI 状态根因；不允许重跑到绿。
- Snapshot/golden：当前不采用；如后续引入必须人工审阅语义 diff。
- 手工视觉：记录 OS、主题、窗口尺寸、sidebar 模式、route、commit 和结果。

## 13. 测试计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 测试/技术 Owner | 段成威 | G2 Approved；S0 测试已按本计划执行 | 2026-07-30 |
| 安全/数据 Owner | 段成威 | G2 Approved；当前无网络/真实数据/高风险写入 | 2026-07-30 |
