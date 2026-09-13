# FEAT-153 — Desktop 接入前审计与本地编辑器会话实验草案

- 日期：2026-09-12。
- 范围：Desktop 工作流入口、现有用户改动、身份/API 路径、Tauri 展示边界和正常验证入口；Coze 会话源码仅补充交叉核对。
- 状态：只读审计完成；本文实验为候选设计，未实施、未启动、未验证，不代表 D0/D4 或 Owner 批准。
- 方法：读取规则、设计 Pattern、FEAT-151、ADR-0018、源码、Git 状态及既有验证记录；未运行应用、构建、测试、安装或外部服务调用。本文件是本审计唯一新增文件。
- 引用约定：下文 `仓库/路径:行号` 均相对于 CrossBSD 工作区根目录；行号对应审计时工作树，包含已记录的用户未提交改动。旧验证结果明确标为历史事实。

## 1. 审计结论

可以在保留独立 Coze React 构建的前提下接入现有“工作流”入口。但当前不存在可直接复用的通用工作流 HTTP client 或 Coze 登录会话；增加按钮与 iframe 本身不能构成真实基础集成。应先验证单一 Desktop 中编辑器的加载、固定本地 scope 映射、会话和保存重开，再开展完整通用流程闭环。

FEAT-151 的静态展示是现状；FEAT-153 将增加跨进程交互和持久化，不能继承其 `contract-impact=none`。整体影响按最终设计取最高风险：新 API 可以是 additive 子边界；若改变启动、身份或既有操作语义，需要评估 semantic；未证明兼容时不得直接假定 additive。

## 2. Git 基线与用户改动保护

审计实际 Git 输出：

| 项目 | 值 |
|---|---|
| Repository | `yijie-desktop` |
| Branch | `chore/retirement-baseline-20260905` |
| HEAD | `5964e2f7c31ea298f801df02086abbc8d6676b91` |
| Origin | `https://github.com/36Dge/yijie-desktop.git` |
| Tracked diff | 6 个文件，228 insertions / 199 deletions；不含两个 untracked 文件 |

既有 dirty 文件：

```text
 M docs/design/docs/design/05-patterns/16-feat-151-workflow-showcase.md
 M src/components/workflows/RecommendedWorkflowCard.vue
 M src/components/workflows/WorkflowSummaryCard.vue
 M src/components/yijie/YjPageHeader.vue
 M src/pages/workflows/WorkflowPage.test.ts
 M src/pages/workflows/WorkflowPage.vue
?? docs/verification/workflow-interactions-and-lime-20260911.md
?? src/components/workflows/workflow-showcase.css
```

这组修改来自用户多轮界面精调。后续必须以实际工作树为起点，按必要范围追加，不 reset/checkout、不覆盖、不批量格式化、不恢复旧截图结构，也不自动混入提交。每步前后检查 status/diff；代码版本引用仅 HEAD 不足以描述本基线，正式实验应同时记录受影响文件摘要。

当前 Pattern 1.2.4 指定自然换行、双组 2/4 列栅格、透明卡片图标背景、中性标签、青柠执行按钮及推荐卡去除流程示意。证据：`yijie-desktop/docs/design/docs/design/05-patterns/16-feat-151-workflow-showcase.md:24`。

## 3. 已确认工程事实

| ID | Fact | 证据 |
|---|---|---|
| F-D01 | `/workflows` 注册名为 workflows，沿用 workspace 导航键；页面只在 exact local + demo_fast 开放，权限仍为 workspace.use。 | `yijie-desktop/src/router/index.ts:126`；`yijie-desktop/src/router/index.ts:211`；`yijie-desktop/src/authorization/workflow-showcase-ui-config.ts:3`；`yijie-desktop/src/authorization/app-permission-policy.ts:33` |
| F-D02 | 当前页面导入 MY_WORKFLOWS/RECOMMENDED_WORKFLOWS 静态集合；创建只切换内存布尔值，分类/排序/视图不改变卡片集合。 | `yijie-desktop/src/pages/workflows/WorkflowPage.vue:9`；`yijie-desktop/src/pages/workflows/WorkflowPage.vue:12`；`yijie-desktop/src/pages/workflows/WorkflowPage.vue:48`；`yijie-desktop/src/pages/workflows/WorkflowPage.vue:81` |
| F-D03 | 现有测试明确禁止工作流页面、模型和卡片依赖 fetch/axios/invoke/Tauri/browser persistence。FEAT-153 应明确替代静态能力边界，不应无说明删除断言或伪造测试成功。 | `yijie-desktop/src/pages/workflows/WorkflowPage.test.ts:135` |
| F-D04 | src/api/client.ts 仅返回占位 Runtime health，不是通用真实 API 客户端；permission client 通过 Tauri invoke 调用 native。 | `yijie-desktop/src/api/client.ts:6`；`yijie-desktop/src/api/permission-client.ts:1` |
| F-D05 | Rust OperationTransport 只提供固定 tenants/capabilities/task 路径；使用 HTTPS、禁止 redirect、有限响应容量，且 token 在 Rust 持有。不能直接用它访问任意 Coze HTTP 路径。 | `yijie-desktop/src-tauri/src/native_auth/transport.rs:10`；`yijie-desktop/src-tauri/src/native_auth/transport.rs:122`；`yijie-desktop/src-tauri/src/native_auth/transport.rs:158` |
| F-D06 | exact local 模式直接选 RuntimeMode::DemoFast，status 返回 signed_in，tenant/capability 本地返回，不建立 yijie-api/OIDC 会话。 | `yijie-desktop/src-tauri/src/native_auth/runtime.rs:154`；`yijie-desktop/src-tauri/src/native_auth/runtime.rs:250`；`yijie-desktop/src-tauri/src/native_auth/runtime.rs:255` |
| F-D07 | 本地 owner 固定为 12500000-0000-4000-8000-000000000001，tenant 固定为 12500000-0000-4000-8000-100000000001，capability 包含 workspace.use；WebView 不决定身份。 | `yijie-desktop/src-tauri/src/local_profile.rs:6`；`yijie-desktop/src-tauri/src/local_profile.rs:38`；`yijie/docs/adr/ADR-0018-local-demo-direct-entry.md:31` |
| F-D08 | 当前 CSP 没有 frame-src，default-src 为 self/customprotocol/asset。connect-src 虽包含 localhost:8080，也不等于允许嵌入该地址页面。 | `yijie-desktop/src-tauri/tauri.conf.json:22` |
| F-D09 | default capability 仅 main/macOS 上的 core app、listen、unlisten，没有 opener、remote 或 window-create 配置；检查 src/src-tauri 未找到已接入的远程编辑器窗口或导航策略。 | `yijie-desktop/src-tauri/capabilities/default.json:4`；`yijie-desktop/src-tauri/src/lib.rs:171` |
| F-D10 | 标准 pnpm tauri:dev 和 tauri:demo-fast 是同一 canonical launcher；packaged alias 沿用相同链路。该链路清理专项认证变量，绑定固定 scope 并管理 Host/Runtime。 | `yijie-desktop/package.json:33`；`yijie-desktop/scripts/run-local-demo-fast.sh:180`；`yijie-desktop/scripts/run-local-demo-fast.sh:212` |
| F-D11 | Desktop 已有每用户单实例保护。新需求应使用同一真实 App，不建立第二个测试 App 作为验收替代。 | `yijie-desktop/src-tauri/src/lib.rs:125`；`yijie-desktop/docs/local-development.md:46`；`yijie/docs/dev/codex-feature-delivery/HANDBOOK.md` 的 A2 |
| F-D12 | Coze WebAPI 的 SessionAuthMW 读取 session cookie，再调用 ValidateSession；登录/注册是特定免会话路径。Coze 前端保留 sign 路由；因此 Desktop 的 signed_in 状态不自动满足 Coze。 | `yijie-coze/backend/api/middleware/session.go:37`；`yijie-coze/backend/api/middleware/session.go:55`；`yijie-coze/frontend/apps/coze-studio/src/routes/index.tsx:88` |
| F-D13 | Coze 注册 handler 当前设置 session cookie，使用 / 路径、GetOriginHost、CookieSameSiteDefaultMode，以及传入 false/true 的 secure/httpOnly 参数位置。实际响应头及 WKWebView 行为仍未验证。 | `yijie-coze/backend/api/handler/coze/passport_service.go:58` |

其中 F-D08 的 iframe 可达性是基于实际 CSP 的静态判断；F-D09 只陈述已查源码范围内没有既有能力，不代表 Tauri 框架不能实现。

## 4. 既有证据与冲突

1. **历史 FEAT-151 与当前工作树不同。** 原 Brief 的 AC 要求纯展示、不点击、不跳转，旧 D4 覆盖当时版本；当前 Pattern/源码已允许本地选择反馈。FEAT-153 不能把旧 D4 当作当前 workflow 集成证据。证据：`yijie/docs/features/FEAT-151-desktop-workflow-showcase/00-feature-brief.md:10`、`yijie/docs/features/FEAT-151-desktop-workflow-showcase/00-feature-brief.md:40`；`yijie-desktop/docs/design/docs/design/05-patterns/16-feat-151-workflow-showcase.md:20`。
2. **已知亮色对比度限制。** 用户明确要求白底青柠说明文字；既有实际 browser 验证报告记录 1 项 serious color-contrast，1.28:1。不能继承旧 0 axe 结论，也不在本需求擅自更改用户指定配色。证据：`yijie-desktop/docs/verification/workflow-interactions-and-lime-20260911.md:90`，尤其 `yijie-desktop/docs/verification/workflow-interactions-and-lime-20260911.md:96`。
3. **文档中“API client 仍占位”不等于所有 API 都占位。** permissions/chat/native 已存在真实特定适配；真正缺的是通用 workflow adapter 与 Coze session，不应据 AGENTS 早期状态说明重建现有认证体系。证据：F-D04 至 F-D07。

## 5. 两种候选方案与推荐

| 方案 | 结构 | 优点 | 代价与验证前提 |
|---|---|---|---|
| A：同窗口编辑器容器，推荐 | Vue /workflows 保持产品入口；编辑时在同一 Desktop 窗口嵌入独立 Coze React editor；固定 local gateway/API 处理资源及 server-side session。 | 保持用户主要入口与返回路径；React 独立构建；不把 Coze 组件库导入 Vue。 | 需要窄 frame-src、frame-ancestors/响应头核对、加载结果协议与 WKWebView 第三方 cookie/存储验证；网关自身会话不能凭空视为存在。 |
| B：同一 App 的专用 editor WebView/window | 由同一 Tauri App 管理专用编辑器 WebView/window；只允许固定编辑器 origin，不授予远程 native capability。 | 可绕开部分 iframe 存储上下文限制，保持 Coze 独立前端。 | 新增原生窗口生命周期、导航范围、关闭/返回/未保存提示；会话仍需设计，且仍须验证平台行为。不得以另建第二个 App 代替。 |

推荐先用 A 做最小会话/保存重开技术验证，再决定是否采用 B。它们都是候选方案，当前没有证明任一方案已可运行；不开放通配 CSP、不把 API/Host token 交给 React、不以 localStorage 或长期 URL token 补洞。

暂不推荐把 Coze React workflow 包直接安装到 Desktop 活跃 Vue 应用。这样会扩大 React、Coze UI、依赖图、全局样式与构建维护范围；现有规范使用 Yj*/Vue/Naive，具体编辑器能力应在独立构建边界保持。证据：`yijie-desktop/package.json:46`；`yijie-desktop/docs/design/docs/design/07-ai-codex/01-ai-development-rules.md`。

## 6. 设计时必须解决的未知项

| ID | Unknown | 解决所需的最小证据 |
|---|---|---|
| U-D01 | native owner/tenant 与 Coze user/space 的单一、稳定映射及服务端会话建立方式。 | 固定映射与允许操作的设计；在真实 local 服务中由受信端建立并读取，不能由 renderer 传 owner/tenant 自证授权。 |
| U-D02 | tauri://localhost 与开发 http://localhost:1420 下，iframe 会话 cookie 是否被 WebKit 正常存取。 | 两种 canonical 展示来源分别观察实际 Set-Cookie 属性、后续请求认证和 reload；证据仅保留属性/状态，不保存 cookie 值。 |
| U-D03 | Coze 响应 frame-ancestors/X-Frame-Options、root-relative API/static asset 路径与 gateway base path 是否兼容。 | 真正加载一个编辑器路由和一次 authenticated metadata 请求；记录 origin/path/status，排除机密值。 |
| U-D04 | 本地服务启动、readiness、退出及 session 失效由谁管理。 | 明确由现有 launcher/Infra 哪一方持有进程，给出正常 up/status/down 和重开行为；不能双重管理同一服务。 |
| U-D05 | editor-ready、加载失败、关闭前未保存、资源不存在与引擎失败如何映射到 Vue UI。 | 契约先行的状态/事件定义；先定义作用域、版本和未知值处理，不接受通配 postMessage 来源。 |
| U-D06 | 既有静态八张电商卡与新真实通用流程如何共同呈现。 | D0 界面与数据来源区分；不能把静态 ERP 卡绑定通用示例后宣称电商服务完成。 |
| U-D07 | 本地会话/流程持久化的保留及回滚边界。 | synthetic 独立数据集、正常初始化入口、旧 reader/升级策略与回滚支持范围；不在真实用户数据库直接 seed。 |

认证、CSP、外部 origin、Rust command/sidecar 等具体安全范围须由主交付中的设计决策明确。Desktop 规则确有“修改前必须向用户确认设计和权限范围”，见 `yijie-desktop/AGENTS.md:73`。本文不判断主线程授权是否覆盖最终具体方案，也不把未展示细节写成 Owner 已批准。

## 7. 最小本地会话实验草案（仅可评审，NOT RUN）

### 7.1 要证明的问题与明确非目标

要证明：用户从 canonical Desktop 的“工作流”进入独立 React editor，无第二次登录；编辑器受固定本地 scope 限制，可以通过真实 provider 创建/保存/重开一个无业务草稿。实验只决定展示与会话方案可行性，不代替 FEAT-153 全部 Must AC 或 D4。

不做：ERP 节点、模型/付费 API、真实商家数据、第三方平台凭据、Agent/Codex 工作流节点、公开部署、生产认证、多租户上线、数据库迁移破坏演练、攻击注入及第二个 Desktop App。

### 7.2 实施前需要审阅的最小设计输入

- 最终固定的 local origin/port、编辑器 route/base path、仅本功能需要的 CSP 差异；HTTP 与 HTTPS 的具体选择由实际 WebKit/session 验证决定，不凭经验先关闭 cookie 安全属性。
- 固定 native scope 到 Coze user/space 的映射；session 在可信端建立、绑定、过期和正常回收的方法。renderer 不选择 user/tenant/space authority，浏览器可见 ID 只作资源选择。
- 新 native/API/editor 消息边界的权威 schema、允许操作、失败语义与消费方式；来源先于实现，token 不进入 query/hash、postMessage、localStorage、日志或截图。
- 受管服务生命周期、readiness 和正常停止命令；只构建本项目 canonical 可复现开发产物，不覆盖受审计 Runtime 或来源不明 binary。
- 独立 synthetic 工作流数据范围与正常创建入口；不直接写 DB/Store 来模拟保存成功。

### 7.3 实验步骤与通过条件

| ID | 操作/条件 | 预期可观察结果 | 所需证据 | 当前 |
|---|---|---|---|---|
| EXP-D01 | 服务按所选正常入口启动，使用当前同源 canonical Desktop 进入 /workflows。 | Desktop 保持既有 direct-entry；无账号、密码、Keycloak/OIDC 浏览器；服务 readiness 真实返回。 | 环境/构建来源、正常命令、只含状态的 readiness、实际入口截图。 | NOT RUN |
| EXP-D02 | 点击独立编辑器入口；等待真实 React 资源及 metadata 加载。 | 同一 App 内到达 editor-ready；没有 sign/login 跳转、空白页、资源路径 404 或 CSP 阻断。 | 实际 origin/path/status、ready 截图、CSP/响应头属性。 | NOT RUN |
| EXP-D03 | 通过受信 bootstrap 建立固定本地会话并读取当前 user/space。 | provider 返回所绑定 synthetic scope；无需用户登录；renderer 不提供身份声明作为权威。 | 非机密的映射标识、认证状态、服务端请求关联信息；源码边界审阅。 | NOT RUN |
| EXP-D04 | 正常创建一个空白/通用草稿，修改名称或普通文本参数并保存。 | provider 成功响应并返回真实资源 ID；不存在仅本地 ref/toast 的伪保存。 | 正常请求 ID、资源 ID、provider 响应状态和 UI 结果；不保存 session 值。 | NOT RUN |
| EXP-D05 | 从编辑器返回 /workflows，再重新打开；正常 reload。 | 同一资源和已保存字段仍可读，会话保持有效或自动安全恢复；不重复创建 user/space/草稿。 | 保存前后字段、相同资源 ID、重开截图与实际请求状态。 | NOT RUN |
| EXP-D06 | 分别在 canonical dev origin 和 packaged tauri origin 复验 EXP-D02 至 05。 | 两种来源都能正常存取必要会话；不存在 browser-only 成功而 packaged 失败。 | 分别记录平台/WebView、cookie 属性及请求认证状态；cookie 值一律不入证据。 | NOT RUN |
| EXP-D07 | 服务正常停止期间进入编辑器，随后按正常入口重启并点击重试。 | 显示明确不可用/重试状态；重启后恢复；不会假称已保存、无限重试或要求重新登录。 | 正常 stop/start 日志摘要、错误及恢复截图。 | NOT RUN |
| EXP-D08 | 编辑器正常返回/关闭，Desktop 正常 Command-Q 退出，再以同入口重开。 | 生命周期所有者正常清理；原有 Chat 历史未改变；草稿按声明保留，会话按声明重建/失效。 | 退出前后受管进程/端口状态、重开后的资源 ID；不以清理失败触发强杀。 | NOT RUN |
| EXP-D09 | 1180×760、亮暗主题、Tab/Enter/返回键与编辑器错误状态。 | 关键入口、保存、返回可达，无主体横向溢出；既有青柠说明对比度限制独立记录。 | 实际截图/键盘记录；不能把已知对比度问题计为通过。 | NOT RUN |

### 7.4 判定与停止

- A 的 cookie、CSP、路径或 native bridge 任何关键证据缺失时，结论为“方案未证明”，不继续横向实现电商节点或扩展完整 Coze 产品。
- 若是 WKWebView iframe 存储上下文阻塞，保留失败证据，评审方案 B；不通过关闭浏览器安全、开放 remote native 权限、手工登录或清空用户数据绕过。
- 30 分钟没有新证据，停止猜测配置并读取完整调用链；90 分钟同一核心阻塞，形成准确失败点与推荐替代；按 demo_fast 时间盒避免扩建测试平台。
- 只在全部适用实验条目有真实证据后宣布“本地编辑器展示与会话技术可行”。通用流程执行/节点结果/正式列表仍属于后续完整实现验收。

## 8. 安全验证限制与未执行项

用户级硬性规则禁止强杀故障注入、替换/伪装受保护 binary、权限破坏及攻击 fixture。后续不得机械运行全量脚本后再补解释。

已核实标准 `make lint` 调 `pnpm generate:check`，`make test` 调 `pnpm test` 和 Rust 全测；`generate:check` 又运行历史 v3 checker。该 checker 包含 `injection-invalid.json` fixture；现有工作流验证报告亦明确记录 Rust 全测含权限故障场景。因此需在执行前按脚本内容选取正常 focused checks，不关闭原门禁或篡改结果来宣称 full-green。

证据：`yijie-desktop/Makefile:20`、`yijie-desktop/Makefile:26`；`yijie-desktop/package.json:18`、`yijie-desktop/package.json:21`；`yijie-desktop/scripts/check-agent-host-v3-contract.mjs:242`；`yijie-desktop/docs/verification/workflow-interactions-and-lime-20260911.md:40`。

| 未执行项目 | 原因 | 影响 |
|---|---|---|
| Desktop/Coze 构建、启动、session/API/持久化/真实编辑器操作 | 本阶段为只读接入前审计与实验设计。 | 不证明 iframe/native window 可用，也不证明源码可构建或服务可运行。 |
| 全仓 make lint/test、攻击 fixture、权限故障场景 | 未运行测试；部分 canonical 全测链含用户明确禁止行为，后续需选正常验证。 | 不声明全仓通过；生产安全/韧性完整验证仍未完成。 |
| 本次视觉/axe/native smoke | 未启动应用；只引用有版本和时间的既有记录。 | 旧截图/旧 D4 不覆盖 FEAT-153；当前亮色对比度限制保留。 |
| 外部模型、付费 API、真实店铺/生产写入 | 不属于基础集成与本实验。 | 不证明任何实际 ERP 服务能力；调用预算为 0。 |

## 9. 本审计产出边界

本文仅新增审计证据和可评审实验条件，未改变 Desktop 业务文件、CSP、capability、依赖、启动器、凭据或既有数据。仓库接入、契约、provider、部署与完整工作流执行由 FEAT-153 主交付按依赖顺序推进；不能用本文件替代真实实现或验收。
