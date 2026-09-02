# FEAT-151 整体实现与调试记录

## 1. 整体实现方案

- 真实调用链：App Shell 左侧“工作流” → Vue Router `/workflows` + `workspace.use` guard → `WorkflowPage` → 进程内只读展示模型与 `Yj*` 组件。
- 实施顺序：D0 → 固化截图全部文案/顺序/节点 → 实现卡片与页面 → 接入 route/navigation/permission → focused checks → 真实 Tauri 验收。
- Contract First：`contract-impact=none`；不新增公共/private wire、Tauri command、持久化、durable event 或 replay 语义。
- 明确不做：任何接口、筛选、排序、视图切换、新建、更多、查看全部、演示、执行、保存、二次跳转、付费调用或生产写入。

本 Profile 不建立治理切片；以一个完整可观察的 Desktop 用户结果统一验收。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| `yijie-desktop` | `src/navigation/app-nav.ts`、`src/router/index.ts` | 原“工作台”更名为“工作流”，启用 `/workflows`，保持侧栏选中并设置文档标题。 | 交付真实侧栏入口。 |
| `yijie-desktop` | `src/authorization/*workflow*`、`app-permission-policy.ts` | 展示页仅在 exact `local + demo_fast` 暴露，并复用 `workspace.use` 保护导航和深链。 | 避免扩大权限或 public 暴露。 |
| `yijie-desktop` | `src/domain/workflow-showcase.ts` | 固化截图中的 9 个顶部分类、7 个“我的工作流”分类、4 张已有卡与 4 张推荐卡的只读数据。 | 保证信息完整、顺序可测且不接接口。 |
| `yijie-desktop` | `WorkflowPage.vue`、两类 workflow card、icon registry | 使用 `YjPage/YjSection/YjIcon` 与 design token 实现完整静态页面；页面内无链接、按钮、表单或 handler。 | 遵循项目 UI 规范和 display-only 边界。 |
| `yijie-desktop` | navigation/router/permission/page/icon tests | 增加完整文案、顺序、权限、denied loader、无 I/O/无交互、语义与 axe 覆盖。 | 为正向和否定需求提供回归保护。 |
| `yijie-desktop` | `tests/visual/feat-151`、UI pattern 文档 | 增加生产组件 visual harness 与 FEAT-151 UI 约束文档。 | 验证 1180×760、light/dark、滚动和可访问性。 |
| `yijie-desktop` | `scripts/run-local-demo-fast.sh` 与 v4 contract checker/tests | 将可选 `feat134_environment` 改为 macOS Bash 3.2 + `nounset` 安全的空数组展开，并让静态边界检查只接受安全写法。 | canonical 启动在当前 profile 无附加环境项时也应可靠进入 ready。 |
| `yijie` | 本 Feature Package | 记录 brief、实现、验证、限制和视觉证据。 | 遵循 yijie `codex-feature-delivery`。 |

## 3. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复 | 结果 |
|---|---|---|---|---|
| 2026-08-31 | D0 gate 首次执行通过 | Feature 已按 `demo_fast + local`、`contract-impact=none` 建包。 | 无。 | PASS |
| 2026-08-31 | 领域模型测试首次红灯，提示 `workflow-showcase` 模块不存在 | 按 test-first 先写测试，生产实现尚未创建。 | 新增只读领域模型及完整截图数据。 | focused test 转绿。 |
| 2026-09-01 | 首轮 visual axe 报告辅助文字对比度与可滚动主区域不可聚焦 | 小字号使用 tertiary token；Shell 主滚动区没有键盘焦点入口。 | 改用 secondary/primary 文本 token，并为 main 增加 `tabindex=0`。 | light/dark axe violations 均为 0。 |
| 2026-09-01 | scoped 语义复审发现顶部静态分类使用无链接的 `nav` | 该区域是只读能力分类，不是导航控件。 | 改为带标签的 `section`。 | 语义与 display-only 意图一致。 |
| 2026-09-01 | `pnpm test` 在运行 Vitest 前退出 | `generate:check` 检出 `yijie-agent-host` 既有 FEAT-137 脏工作树。 | 不清理、不覆盖用户改动；直接运行 frontend Vitest 获取独立证据。 | canonical test 命令 FAIL，原因已记录。 |
| 2026-09-01 | 全量 frontend Vitest 1083 项中 5 项失败 | 4 项是既有脏 Agent Host contract/resource 同步检查；1 项是 FEAT-132 projection 与当前 FEAT-137 状态的预期差异。 | 未修改范围外代码；保留失败证据。 | 1078/1083 PASS，FEAT-151 focused 55/55 PASS。 |
| 2026-09-01 | canonical Tauri 首次启动前检查发现端口 18081 被既有 Host 占用；之后端口自然释放，但启动器仍会 `go build -o` 重建 Host 可执行文件 | 强停既有进程或覆盖 executable 均违反用户长期安全条款。 | 不调用 canonical launcher；改用 fresh `/tmp` Cargo target，复用既有 Host/Runtime binary。 | 既有 binary SHA-256 前后不变；canonical D4 保持 NOT RUN。 |
| 2026-09-01 | 隔离 `tauri dev` 编译/运行成功，但终端直启进程在 macOS 登记为不可见，Computer Use 无法获得窗口 | 原始 debug 可执行文件不是 LaunchServices 可识别的标准 `.app`。 | 正常 Ctrl-C 退出；在另一个 fresh `/tmp` target 构建 unsigned `.app` bundle。 | 不把不可审计窗口冒充 smoke。 |
| 2026-09-01 | 隔离 Tauri bundle 零登录打开真实 App Shell | 标准 `.app` 正确加载当前 production frontend 与 local demo_fast 权限。 | 从侧栏点击“工作流”，核对 AX 内容并滚动到页面底部，再通过窗口关闭按钮正常退出。 | 原生 smoke PASS；AC-001—AC-009 全部 PASS。 |
| 2026-09-01 | App 首页“重试启动”后 Host 仍显示未就绪 | 当前既有 Agent Host/FEAT-137 脏状态的范围外 readiness 问题；FEAT-151 静态页面不调用 Host。 | 不扩展或修改 Host；保留真实失败事实。 | 不影响工作流页 smoke，但整体 D4 不声明 PASS。 |
| 2026-09-01 | 两个 fresh 隔离 target 合计约 6.5 GB | 原生 smoke 截图已经保存，构建缓存不再需要。 | 永久删除命令被安全防护拒绝，随后将两个精确目录移动到废纸篓。 | 临时目录可从 `/Users/jack/.Trash/yijie-feat151-*` 恢复；仓库与既有 binary 未变。 |
| 2026-09-01 | FEAT-137 sibling 已提交、Agent Host 工作树恢复 clean | 原 preflight blocker 已发生真实外部状态变化。 | 重新执行一次 canonical `pnpm test`。 | preflight 与 1081/1083 tests PASS；剩余 2 项为 v4 Host commit 预期滞后和 FEAT-132 projection 范围外差异。 |
| 2026-09-01 | 用户明确授权本次 FEAT-151 可绕过“canonical 构建不得覆盖既有 executable”的限制并要求持续完成 | canonical `pnpm tauri:dev` 的 `go build -o` 与 Tauri build 会替换本地构建产物；此前正因该长期安全条款暂停。 | 先将既有 Host 复制为 `.local/bin/yijie-agent-host.feat151-precanonical-20260901`（SHA-256 `bbeb9cf0…`），再在授权范围内执行 canonical；不扩大到强杀、故障注入、权限破坏或范围外数据操作。 | 可恢复备份保留，授权边界与实际覆盖次数写入 Feature Package。 |
| 2026-09-01 | canonical 第一次启动在 Host 重建后退出：`feat134_environment[@]: unbound variable` | macOS `/bin/bash` 3.2 在 `set -u` 下直接展开空数组会报错。 | 改用 `${feat134_environment[@]+"${feat134_environment[@]}"}` 安全展开，并增加真实 `/bin/bash` 空数组 argc=0 回归。 | `bash -n` 与启动器 12/12 tests PASS。 |
| 2026-09-01 | canonical 第二次启动被 v4 contract checker 拒绝 | checker 仍把旧的 nounset-unsafe 字符串当作唯一合法边界。 | 同步 checker 的 exact line，并加入将安全写法突变回旧写法时必须拒绝的测试。 | 当前 v4 checker 与 stable-only mutation 子集 PASS。 |
| 2026-09-01 | canonical 第三次 fresh 启动 | 启动器与 checker 已一致支持空环境数组；真实 Host/Runtime 路径有效。 | 等待 Vite 1420、Tauri `target/debug/yijie-desktop` 与 Agent Host 18081 ready；随后正常 Ctrl-C。 | canonical startup PASS；退出后 1420/18081 和 Desktop/Host 进程均释放。当前 Host SHA-256 `08faad2d…`。 |
| 2026-09-01 | canonical 裸 debug 进程无法被 macOS Accessibility 应用目录枚举 | 与 FEAT-150 既有验收事实一致：裸二进制启动可验证 readiness，但不能提供元素级桌面交互证据。 | 从当前同源源码执行 `pnpm tauri:build:demo-fast`，启动标准 unsigned `.app`；Computer Use 点击“工作流”、滚动至底部并用窗口关闭按钮退出。 | 真实 Host 18081 ready；URL、标题、选中态和全部 AX 内容 PASS；四张推荐卡均完整可见；正常退出无残留。 |
| 2026-09-01 | 最终全量 Desktop test 与治理闸门 | 新增两个启动器回归后测试总数增加，两个既有范围外断言仍失败。 | 重跑 `pnpm test`、D0、D4、strict、lint、typecheck、docs build 与 diff check。 | 1083/1085 tests PASS；FEAT-151 focused 67/67 PASS；D0/D4/strict 全部 PASS。 |

除用户在本线程仅为 FEAT-151 canonical 构建明确授权的 Host/Desktop 构建产物覆盖外，所有验证继续使用正常、非破坏性的开发与测试方式；未执行强杀进程、故障注入、恶意 fixture、权限破坏或范围外破坏性操作。

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费调用 | N/A | N/A | 0 | 0 | N/A |
| canonical 构建产物覆盖 | 本地 Host/Desktop executable | 用户（本线程）/ 2026-09-01 | 8 | 4 | PASS；覆盖前 Host 备份保留，未强杀进程。 |
| 生产写入 | N/A | N/A | 0 | 0 | N/A |

## 5. 已知限制

- 本 Feature 仅交付 local demo_fast 静态展示；不代表真实工作流能力或 public/production 发布。
- canonical `pnpm tauri:dev` fresh startup 已独立通过；原生元素级截图使用当前同源 debug `.app`，因为裸 debug 二进制未登记到 macOS Accessibility 应用目录。
- 覆盖前 Host 备份仍保留于 `yijie-agent-host/.local/bin/yijie-agent-host.feat151-precanonical-20260901`；未自动恢复，因为当前 canonical 产物对应本次验收源码且用户已授权替换。
- 全量 frontend Vitest 当前为 1083/1085 PASS，2 项既有范围外差异已记录；本 Feature 的 focused 67 项测试、lint、typecheck、build、docs build、canonical startup 和 visual/native smoke 均通过。
