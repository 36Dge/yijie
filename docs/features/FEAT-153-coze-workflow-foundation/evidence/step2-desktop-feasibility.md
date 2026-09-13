# FEAT-153 第 2 步 — Desktop 编辑器与会话可实施性

- 日期：2026-09-12。
- 授权事实：主任务已转达用户“批准该方案，继续第 2 步”。本文件据此细化设计，不重复索取原生/会话方向的既有授权。
- 范围：当前锁定 Tauri/Wry/Apple 绑定源码、实际平台版本、Coze HTTP 扩展点及官方 WebKit/HTML 规范；只新增本证据文件，不实现业务、不构建、不启动栈、不运行攻击或故障注入。
- 本步技术权威：[05-local-integration-design.md](../05-local-integration-design.md)；本附件提供锁定源码依据，命名/操作以 05 为准，精确 wire 尚待第 3 步源 schema。
- 当前结论：原生 cookie 写入 API 存在，但不能据此证明第三方 iframe 会带 cookie。本步采用同 App 的独立 HTTP React iframe，将会话收敛为 native 内存保管，通过封闭 MessageChannel/具名 native 操作访问 API；这是用户已批准同窗口、固定 local scope 与 native/server 桥接的具体化，不把 WK cookie 可行性写成 D0 已证事实。

## 1. 固定源码与平台

实际读取 `yijie-desktop/src-tauri/Cargo.toml:45` 和 Cargo.lock：

| 依赖 | 锁定版本 |
|---|---|
| tauri | 2.11.5 |
| tauri-runtime / tauri-runtime-wry | 2.11.3 / 2.11.4 |
| wry | 0.55.1 |
| objc2 / objc2-foundation / objc2-web-kit | 0.6.4 / 0.3.2 / 0.3.2 |
| cookie | 0.18.1 |

当前宿主 `sw_vers`：macOS 26.5，build 25F71。系统 WebKit framework `CFBundleVersion` 为 `21624.2.5.11.4`。这些是只读版本事实，不是运行资格。

下文 `registry/<crate>/...:line` 对应本机 `/Users/jack/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/<crate>/...`；项目引用相对 CrossBSD 根目录。

## 2. HttpOnly cookie 能怎样写入，哪些结论不能推出

### 2.1 已存在的 API 调用链

`tauri::WebviewWindow::set_cookie(cookie)` 确实存在，转入 Webview dispatcher，再由 Wry 调用目标 WKWebsiteDataStore 的 `httpCookieStore().setCookie_completionHandler(...)`。

| 事实 | 锁定源码 |
|---|---|
| Tauri WebviewWindow 暴露 set_cookie | `registry/tauri-2.11.5/src/webview/webview_window.rs:2571` |
| dispatcher 的 set_cookie 将消息入队后立即返回 Ok；实际处理错误只记录日志 | `registry/tauri-runtime-wry-2.11.4/src/lib.rs:1803`、同文件 `:3918` |
| Wry 在实际 cookieStore completion 后结束其内部操作 | `registry/wry-0.55.1/src/wkwebview/mod.rs:1227` |
| HttpOnly、Secure、SameSite 转换 | `registry/wry-0.55.1/src/wkwebview/mod.rs:1140` |

因此 native 收到 API 的 Set-Cookie 后，技术上可以写入 main 的 cookie store；但 `set_cookie` 外层 Ok 只证明消息已提交，不能直接发 editor-ready 或立刻假定 iframe 已有可用会话。

作为审计排除项，以下是这条路线确实存在、但本期不实施的公开 API 调用方式：

1. Rust 以受管凭据请求固定 API，验证返回的唯一会话 cookie 名、host、path、期限、HttpOnly/Secure/SameSite；不把 header 值返回 renderer。
2. `WebviewWindow::with_webview` 在主线程取得 `PlatformWebview.inner()`，按当前 pinned 类型转为 `&objc2_web_kit::WKWebView`。
3. 由 `WKWebView.configuration().websiteDataStore().httpCookieStore()` 取得**该 main WebView 实际使用的 store**，不是 NSHTTPCookieStorage 的全局替代品。
4. Foundation `NSHTTPCookie::cookiesWithResponseHeaderFields_forURL` 解析服务端 header 与固定响应 URL；调用 `WKHTTPCookieStore::setCookie_completionHandler`，通过 oneshot 在 async command 等待回调。主线程不阻塞等自己的 callback。
5. 用同 store 的 `getAllCookies` 回调只在 Rust 核对目标 cookie 的属性、值相等和期限；不将 cookie 列表写日志或传页面。随后真实 authenticated 请求才判断会话能否使用。
6. 关闭时只删除此会话 cookie并服务端撤销；不 clear 整个 WebView 数据，不影响 Chat 历史/其它已有存储。

源码：`registry/tauri-2.11.5/src/webview/mod.rs:195`、`:1610`、`:1668`；`registry/objc2-web-kit-0.3.2/src/generated/WKWebView.rs:170`；`WKWebViewConfiguration.rs:173`；`WKWebsiteDataStore.rs:117`；`WKHTTPCookieStore.rs:61`、`:72`；`registry/objc2-foundation-0.3.2/src/generated/NSHTTPCookie.rs:488`。

若实现这条排除路线，本需在 Cargo.toml 显式声明已锁定的 Apple 绑定/block2 直接依赖及 Foundation NSHTTPCookie/NSDictionary feature；不能假定传递依赖可直接 import。本期不采用这条路线，不新增这些依赖，也不升级 Tauri、替换 Wry 或覆盖 WK navigation delegate。[Apple cookie store 文档](https://developer.apple.com/documentation/webkit/wkhttpcookiestore?language=objc)也明确其属于具体 WebView 的 website data store。

### 2.2 SameSite、Secure 和第三方策略是独立限制

Wry 的 SameSite::None 分支不写 SameSite property，不能直接称为库缺陷：当前 Foundation 绑定说明 `sameSitePolicy` 只有 strict/lax，nil 表达可随 cross-site 请求。该注释只解释 cookie 属性，不能证明当前 WKWebView 网络策略放行。证据：`registry/wry-0.55.1/src/wkwebview/mod.rs:1157`；`registry/objc2-foundation-0.3.2/src/generated/NSHTTPCookie.rs:678`。

dev 主文档为 `http://localhost:1420`；packaged 为 `tauri://localhost`。后者与 HTTP editor 的 scheme/site 不同。`SameSite=Lax/Strict` 不能作为跨 site 子 frame cookie 的通用解决方案；`SameSite=None` 也不关闭 Secure 或 WebKit 第三方策略。Wry `cookies_for_url` 包含 Secure HTTP localhost 特例，只是本库枚举结果过滤，不证明 WebKit 实际请求会发送。证据：`yijie-desktop/src-tauri/tauri.conf.json:8`；`registry/wry-0.55.1/src/wkwebview/mod.rs:1177`。

[WebKit 官方 tracking prevention](https://webkit.org/tracking-prevention/)区分 cookie policy 与第三方 cookie 限制；把 cookie 写入 store，不等于已获第三方请求存取权限。旧 Safari/iOS bug、现代 WebKit 修订和本机安装版本也不能替代本机真实 iframe 验证。

在上述 pinned Tauri webview、runtime-wry 和 Wry wkwebview 源码中检索 certificate / authentication challenge / serverTrust，**未找到可配置的窄 host 证书 pin 或 trust-challenge callback**。现有 `native_auth::config` 的 CA 只用于 reqwest；不扩展为 WK trust。故不建议为了该功能安装系统 CA、改 Wry delegate、忽略所有证书错误或先假设 Caddy local CA 已被 WK 信任。

## 3. 第 2 步采用：HTTP iframe + 封闭消息操作 + native 短会话

保留用户批准的同一 App、独立 React editor、固定 loopback、固定 local scope、无第二次登录、无 native capability 和秘密不进 renderer。把未证实的“浏览器保存 HttpOnly cookie”换为“native 保存服务端短会话并替 editor 执行固定工作流操作”。这是会话运输层的具体实现收敛，不是关闭资源授权；主设计据此明确它**不再依赖 WK cookie store**，不能声称完成 HttpOnly 浏览器会话验证。

```text
同一 main WebView
  Vue /workflows（既有受信应用 origin）
       ↕ MessagePort：版本化、封闭 editor 操作/结果，无凭据
  iframe（http://127.0.0.1:18888 的独立 React 静态 editor）

Vue 具名 native command
  → Rust：main + exact local profile + capability；editor操作另验绑定
  → 固定 loopback API：受管进程凭据 + Rust 内存短会话
  → 服务端 user/space/workflow 归属校验 → Coze
```

端口 18888/18889/18890 的无监听状态由主任务本轮检查。按 05 冻结，唯一 host gateway 为 http://127.0.0.1:18888，静态壳位于 /editor/，workflow-local API 经同一 gateway 的独立受认证路径访问；18889/18890 只作内部保留，不默认发布。端口空闲不是服务所有权；Infra须证明受管固定 build 和 authenticated epoch/readiness，native才返回该静态入口。只有 /editor/ 静态资产可无认证读取，资源/API不因此匿名开放，不依赖WK cookie。

### 3.1 最小 native surface

| 05 规定的 editor command | 输入与结果 | 强制边界 |
|---|---|---|
| `workflow_editor_open` | 输入 requestId/workflowId；返回 editorId、固定 editor URL、revision、非机密会话到期时间/能力描述。 | Rust 获取固定 owner/tenant并向 API核权；创建短会话。URL 无 token；只允许当前 main 一个活动 editor。 |
| `workflow_editor_exchange` | 输入 editorId/requestId/版本化 operation/payload；返回相同 requestId 对应的限定结果或错误。 | operation 为封闭 union：bootstrap、read_draft、save_draft、test_draft、publish_internal、read_run、read_operation 七项；新增操作必须先改源契约与允许表；不接受任意 URL、headers、HTTP method、native command 名、owner 或 tenant。每次校验 native editor 绑定和 API 归属。 |
| `workflow_editor_close` | 输入 editorId/requestId；返回关闭/已关闭。 | 撤销服务端短会话，清理 native 内存与 pending 读取；重复关闭可识别。已发出的运行不能凭本地关闭推定取消或未执行。 |

05 规划的完整 native surface 共八项：workflow_service_status、workflow_list、workflow_create、workflow_editor_open、workflow_editor_exchange、workflow_editor_close、workflow_run_start、workflow_run_query。query只有指定run、分页历史与operation receipt三种typed查询。editor消息另有dirty_changed/request_close两个UI意图，不属于exchange数据权限。精确字段由 `yijie-contracts` 先生成；本表不是手写消费DTO。

公共校验为main、exact profile/enable、固定native identity和workspace.use；exchange/close另验当前editor绑定。open应先核资源再创建绑定，status/list/create不能以尚不存在的editor为前置；run_start/query按scope及实际workflow/run/operation归属核验，关闭editor后仍可查询已发出的运行结果。

Native HTTP client 独立于现有 OIDC transport，固定目的地、no_proxy、禁止 redirect、严格请求/响应上限和 timeout。机器凭据 `K_NA` 按05通过ignored owner-only运行文件交接至native/API，再由受管进程持有；`K_AC`仅用于API→Coze。API颁发的短会话 `E` 绝对有效期300秒，仅在API/native内存，绑定actor、resource与run epoch。iframe、Vue、URL和MessagePort均不得获得这些机密。会话创建/显式重连/撤销由 native→API 处理；本期不需要 HttpOnly 浏览器 cookie 或 cookie store 写入。错误响应剥离 Set-Cookie、Authorization、redirect_uri 和秘密。不无限自动续期；300秒到期禁写并提示重新连接，只重新核权和颁发E，不自动重放save/publish/run；写入结果不确定先查operation receipt。

### 3.2 MessageChannel 与防止泛化 bridge

- 按05，父Vue先经native打开资源取得非机密bridge ID，iframe load后建立MessageChannel并向精确editor origin转移port；子页核对event.source为window.parent、预配置parent origin及协议版本。若使用window级hello/ack，父侧同时核对event.origin为http://127.0.0.1:18888、event.source为当前iframe.contentWindow。主文档origin由native/启动配置确定，不从未验证消息取值；packaged序列化不符即资格失败，不接受任意null。
- 后续只在该port通讯，不监听全局任意业务消息；window握手的origin/source检查不机械应用到MessagePort事件，后者按已绑定port、native editorId、workflowId及generation核对。port的possession是有限会话访问能力，不称为普通无权限字符串，不日志打印或转发给其它frame。
- 请求只有版本、requestId、operation、受控payload；版本/operation未知返回明确不支持。按05冻结envelope≤512KiB、canvas≤256KiB UTF-8 JSON，其它文本/图规模限额见05第5节；限制每帧在途量和重复requestId，响应只对应原请求。MessagePort requestId不代替native生成的operation ID或服务端写入去重；不传credentials、任意URL/headers。
- `load`、离开路由、错误、关闭时关闭 port、失效 generation、结束 native editor lease；旧响应不得写入新 editor。父页面不把子 frame 的 saved/run-completed 通知当执行事实，状态从 native/API读回。
- E到期后的显式重连不reload/unmount iframe，不丢React内存草稿；关闭旧port，native重验同一资源颁新E，以新generation/new channel重握手并比较服务端revision。发生冲突继续保留本地内容，不自动hydrate覆盖。
- 原生调用仅在 Vue API/composable adapter，不放卡片组件，不向 child 暴露 `invoke`、`__TAURI_INTERNALS__` 或全局 native 调用器。

上述 API 是 HTML 标准的 `MessageChannel()`、`window.postMessage(..., exactOrigin, [port])`、`port.start()/postMessage()/close()`；使用方式及 origin/消息格式检查见[WHATWG Web messaging](https://html.spec.whatwg.org/multipage/web-messaging.html#channel-messaging)。新消息 schema 应从同一权威源产生，producer/consumer 不各维护一份 DTO。

### 3.3 Coze 适配点不是改所有全局 fetch

Coze `frontend/packages/arch/bot-http/src/axios.ts:39` 暴露真实 axiosInstance，`:159` 有 request interceptor 扩展点；`frontend/packages/arch/bot-api/src/axios.ts:19` 复用该实例。独立 editor 构建模式可安装限定 custom adapter，把已登记的 editor API调用映射为上述消息 union，并把正常结果适配回原 Coze envelope。

不得只改 baseURL 后让未知 Coze endpoint继续通过。需要登记 context/canvas/save/test/publish/history 实际调用集合，非首期 endpoint明确 unavailable，禁止 fallback 外部网络。这个 source adapter 位于 Coze 独立 editor 模式，不改变其它 Coze 应用或把 React 依赖装入 Vue。

同时本模式不沿用原 `bot-http/src/axios.ts:109` 的 401 redirect_uri 自动跳转，也不记录 `:50` 的完整 response；会话错误交由 bridge 显示并重连。它不伪造登录页通过，而由真实固定 scope provider 返回当前 editor 所需 context。

## 4. CSP、sandbox、导航和 native capability

- 主窗口只在 exact local 工作流配置增加 `frame-src http://127.0.0.1:18888`；原 Chat 的 connect/img/media/IPC 配置保持，主文档不需要新增直连 API origin。不开 `http:`/`https:`/`*` 通配。
- iframe 使用 `sandbox="allow-scripts allow-same-origin"`；HTTP child 与 Vue origin不同，不能移除父 iframe sandbox。不给 allow-top-navigation、allow-popups、allow-downloads；Permissions Policy/allow显式禁止 camera、microphone、geolocation、clipboard。首期不提供文件上传。
- editor 的响应 CSP 限于自身静态资源、必需的本地样式/字体/image；`connect-src 'none'`，因为业务通过 MessagePort；`frame-src 'none'`、`object-src 'none'`、`form-action 'none'`，`frame-ancestors` 只列实际 dev/packaged 父 origin。若真实 bundle需要 blob worker或inline style，在固定 build实证后精确登记，不能一次放宽所有资源。
- Tauri IPC/init脚本在 `registry/tauri-2.11.5/src/manager/webview.rs:159`–`:182` 为 main-frame-only；保持该默认，不添加 all-frame注入。HTTP child 属 Remote，`registry/tauri-2.11.5/src/webview/mod.rs:1819`–`:1826` 要求显式 remote capability 才可访问 custom command；本设计不配置该项。
- 八个native入口共用main/exact profile/enable/fixed-scope capability检查；editor lease按3.1区分，不能要求列表、创建或首次open先有editor。不要为新入口突然启用全App ACL manifest而使既有native commands失配；当前remote拒绝规则和具名native guards均需保留。
- Tauri有 `WebviewWindowBuilder::on_navigation`、`on_new_window(NewWindowResponse::Deny)` 和 `from_config`，可在创建main时保留原配置安装窄导航策略。若保持既有main自动创建，内置 `tauri::plugin::Builder::on_navigation` 也有同样 URL拒绝 hook，不需新第三方插件包；child的popup/top-navigation由sandbox禁止。实现时选择一种，避免重复创建main。
- `on_navigation` 只传 URL，不包含是否主 frame。Wry 实际对导航请求提取 URL后调用此函数；不能声称仅该hook就完成主/子frame区分。允许既有应用 origin和活动 editor 的固定路径，禁止其它导航；child top导航另由sandbox限制，child load变化使port失效。

导航源码：`registry/tauri-2.11.5/src/webview/webview_window.rs:150`、`:266`、`:315`；`registry/tauri-2.11.5/src/plugin.rs:441`；`registry/wry-0.55.1/src/wkwebview/navigation.rs:49`。上述均为存在的公开 Rust API；第 3/5 步实现仍需正常编译与 App验证。

## 5. 自定义 URI 原生代理的核实与取舍

可用：现有 Desktop已经注册异步 `yijie-artifact-preview`/video；Tauri提供 `register_asynchronous_uri_scheme_protocol`、`UriSchemeContext.webview_label()`、`UriSchemeResponder.respond()`。Wry WK handler读取实际 HTTP method、body/bodyStream和headers，再将异步 response送回。故可以设计数据专用 `yijie-workflow-api://localhost/...`，Rust保管session并只代理固定API。

证据：`yijie-desktop/src-tauri/src/lib.rs:198`；`registry/tauri-2.11.5/src/app.rs:2198`、`:2458`、`:2469`；`registry/wry-0.55.1/src/wkwebview/class/url_scheme_handler.rs:88`–`:132`、`:182`。

但它不能直接被描述为“任何 iframe 页面无native capability”：Tauri `webview/mod.rs:1715`–`:1738` 把注册 custom scheme页面视为 Local。若选此方式，必须保持**HTTP editor document**，自定义scheme只回受控JSON/二进制数据、不回HTML/JS，不作为frame-src，禁止导航至它；并核对request的main label、活动lease、固定Origin和路径/CORS，永不代理任意 URL。

此外 fetch/XHR→custom scheme、CORS、取消/超时仍须当前WKWebView验证。MessageChannel不增加scheme，不涉及该Local-origin语义，也不依赖跨scheme fetch，因此本步采用第3节消息方案；本节是审计排除记录，不新增scheme代理、TLS系统信任、CookieStore私有API或脚本注入，也不声称平台PASS。

## 6. 第 5 步资格验证必须保留的 NOT RUN

| ID | 要验证的真实行为 | 本步状态 |
|---|---|---|
| Q-D01 | canonical dev及packaged主窗口均加载固定HTTP editor；无第二App/登录，资源与MIME正确。 | NOT RUN |
| Q-D02 | 真实iframe origin/source握手及MessagePort transfer正常；默认main-only IPC及无remote capability保持。 | NOT RUN |
| Q-D03 | 服务端固定scope→真实Coze context/canvas；通过消息/native/provider保存，再返回/重开读到同一草稿。 | NOT RUN |
| Q-D04 | 真实bundle的全部必要API已被adapter登记；没有其它API/日志/遥测或登录redirect残留。 | NOT RUN |
| Q-D05 | session正常到期/关闭后显示重连；续期不重发写入，旧editor响应不会污染新页面。 | NOT RUN |
| Q-D06 | 普通参数校验错误→修正重试、已完成流程后正常停止/重开、键盘/主题/最小窗口。 | NOT RUN |

不执行远程脚本注入、伪造origin请求、cookie窃取、权限破坏或强杀等攻击/故障测试。相关边界先静态审阅并用正常消费者行为验证，未做的安全专项明确保留；不输出“完整安全通过”。

## 7. 实施顺序与本文件结论边界

第2步可据上述真实API和源码确定运输层设计及D0可审阅性；第3步先落权威消息/native/API契约及最小provider，第4步受控栈ready，第5步先通过真实资格再扩展产品列表/执行/结果，第6步完整D4。本步不要求先运行尚无provider的编辑器，也不以文档审核替代运行证据。

本文件新增了明确采用的运输层设计与可实施API，不声称业务已实现。原“WK HttpOnly cookie”候选在主设计保留变更记录：用户已批准的隔离/零登录/固定scope目标保持，最终采用native会话+限定操作后，WK cookie方案属于已评估但不作为首期运行依赖，不能写“cookie问题已验证解决”。
