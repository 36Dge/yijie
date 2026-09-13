# FEAT-153 第 2 步：本地基础集成设计

日期：2026-09-12。用户已明确回复“批准该方案，继续第 2 步”。批准范围是同一窗口内嵌独立编辑器、限定本地地址、不给编辑器原生权限、native/服务端固定本地身份与短时会话。本文件将该范围细化为可实施设计；不表示服务已实现、真实资格或 D4 已通过。第 3 步才写源契约及 provider。

## 1. 冻结的产品与技术结果

同一个易界 Desktop，从 `/workflows` 管理真实通用流程，进入独立 React 编辑器，创建/保存/重开草稿，试运行后内部发布，执行明确版本并查看原生结果与历史。流程只能处理合成文本，模型/平台/付费调用为 0。原有电商示意卡保留示意语义，不把它们连接到通用示例后声称 ERP 已可用。

保持现有窗口、Vue 设计和 `workspace.use` 检查。工作流服务未启动只影响工作流，原 Chat/Host/Runtime 仍可正常启动；不更改 FEAT-152、已退役 FEAT-137 或现有 Chat 数据。

## 2. 编辑器载体与会话传输

### 2.1 最终选择

固定静态入口：`http://127.0.0.1:18888/editor/`。同一 main window 的 iframe 仅加载该本地专用 editor bundle。此路径只提供公开静态代码/内置图标，不返回工作流、身份或会话秘密。工作流数据通过以下路径获取：

```text
独立 React iframe
  → 版本化、限定业务操作的 MessageChannel
  → 主 Vue 容器校验 frame/source/origin/协议/容量
  → 具名 workflow Rust command
  → Rust 内存中的固定服务身份和短会话
  → 127.0.0.1:18888 的 workflow-local API
  → 私有 Coze adapter（独立服务凭据）
  → Coze 工作流领域与存储
```

这是已批准的同窗口/独立编辑器/native 服务桥的传输实现细化。编辑器没有直接 Tauri invoke、文件系统、shell、Keychain、进程或任意 HTTP 能力。MessageChannel 只暴露本需求的有限工作流操作，不转发任意原生命令、URL、headers、tenant/user/space 或服务凭据。

服务端短编辑会话继续独立于机器凭据；若以 HttpOnly `Set-Cookie` 颁发，由 Rust 原生 HTTP 端保存并附加，响应头不转交 renderer。**不写入 WKWebView cookie store，不依赖跨站 iframe Cookie，不新增系统 CA、TLS 忽略验证或自定义 URI scheme。** 机器 K_NA 与 K_AC 永远不能充当浏览器 cookie。

### 2.2 选择依据

已锁定的 Tauri 2.11.5/runtime-wry 2.11.4/Wry 0.55.1 有原生 cookie API，但入队或 cookie store 写入不证明网络请求能携带第三方 cookie。WebKit 的跨站策略独立于 SameSite/store，详见[官方 tracking prevention](https://webkit.org/tracking-prevention/)。宿主当前 API 自定义 CA 只约束 reqwest，不构成 WK 信任。

用户注册的 custom scheme 在当前 Tauri 中可能被分类为 Local；不能通过“新 scheme + 不配置 remote capability”就证明无原生能力。为避免这一边界，editor 保持 HTTP Remote 内容，不添加 scheme。MessageChannel 是普通 Web 通道，实际 Tauri 中的握手/隔离仍在第 5 步验证；原生具体代码依据见 [Desktop 可行性附件](evidence/step2-desktop-feasibility.md)。

### 2.3 CSP、隔离与握手

| 位置 | 冻结要求 |
|---|---|
| 主窗口 CSP | local workflow 启用配置仅增加 `frame-src http://127.0.0.1:18888`；不把整个 HTTP origin 加入 native remote capability，不改原脚本/网络权限为通配 |
| iframe | `sandbox="allow-scripts allow-same-origin"`；不允许 top-navigation、popup、download、camera、microphone、geolocation；不向 URL 放 resource/session/token |
| editor CSP | `default-src 'none'`，script 仅 self，style self 与必要 inline，内置字体/图片只 self/data，`connect-src 'none'`，`frame-src 'none'`，`form-action 'none'`；禁直接 Coze API、注册、PAT、上传和外域资源 |
| 嵌入来源 | dev 父页固定 `http://localhost:1420`，packaged 父页按实际 Tauri 配置 `tauri://localhost`；frame-ancestors 和消息来源需同时通过真实两个入口资格，不因序列化 origin 差异放开星号 |
| 导航 | 父 Vue 只设置 iframe.src；iframe sandbox 禁止子页顶层导航/popup。Tauri URL-only hook 拒绝非 allowlist URL，新窗口统一拒绝；不能声称该 hook 能辨认主 frame 与子 frame。主文档如异常离开既有应用 origin，销毁业务消息绑定且不继续授权。静态路由不作开放代理 |

父容器先经受信 native 打开 workflow，得到非机密 bridge ID 与绑定后的视图；iframe load 后建立新 MessageChannel，向精确 editor origin 转交 port。只在匹配 iframe 的 `contentWindow` 上握手；不向 `*` 发送敏感数据。子页同时检查预配置 parent origin、`event.source === window.parent` 和协议版本；父页校验 editor origin/contentWindow，不将子页宣称的身份作为事实。实际 packaged origin 若不能按预期校验，资格失败并分析，不接受任意 `null` origin。后续 MessagePort 事件不能当作 window message 再期待相同 origin/source 字段；改以已绑定的 port/editor ID/generation 校验。

端口消息包含 protocol version、非机密 request ID、operation 和 typed payload。版本/操作未知、重复已完成 request ID、当前 editor generation 不匹配或消息过大时明确拒绝。每个端口只绑定当前 workflow/session，关闭、重新加载、离开页面即关闭旧 port，旧消息不得触发新会话。写入去重以服务端 operation ID 为准，不以 MessagePort request ID 替代。

父容器只匹配有限消息：`bootstrap`、`read_draft`、`save_draft`、`test_draft`、`publish_internal`、`read_run`、`read_operation`、`dirty_changed`、`request_close`。所有数据操作走下方 source-first 契约；dirty/close 只是 UI 意图，不授予服务权限。响应不含 Cookie、Set-Cookie、Authorization、任意内部 URL 或原始错误堆栈。

### 2.4 Native 命令范围

规划最多八个具名入口：`workflow_service_status`、`workflow_list`、`workflow_create`、`workflow_editor_open`、`workflow_editor_exchange`、`workflow_editor_close`、`workflow_run_start`、`workflow_run_query`。query 只包含指定 run、分页历史与 operation receipt 三种 typed 查询；exchange 只支持上述 editor 数据操作。具体 wire 在第 3 步生成，不在本文件手写第二份 DTO。

通用检查包括 exact local/profile/enable、现有 native identity、`workspace.use` 与可信 main window，所有会发起业务请求的命令都执行。status 可以先返回 profile_disabled/服务未就绪而不联系 API。list/create 不要求 editor；open 先核验资源再建立绑定；exchange 要求当前有效 editor/session；close 校验该绑定并幂等关闭，过期 E 不妨碍本地关闭。独立 run_start/run_query 校验 workflow/run/operation 的真实 scope 归属，不依赖 editor，所以关闭编辑器或 E 到期后仍能查询已发出操作。

API base/密钥路径只来自受管启动配置；输入不能携带替代 URL、headers、actor 或文件路径。关闭 editor 只撤销会话/等待，不声称远端运行已经取消。不得将通用 `invoke(command,args)`、`fetch(url,headers)` 作为 iframe 中继接口。

## 3. 身份、会话与凭据生命周期

| 项目 | 明确定义 |
|---|---|
| 精确启用 | `YIJIE_ENV=local`、`YIJIE_LOCAL_PROFILE=demo_fast`、`YIJIE_WORKFLOW_ENABLED=true` 三项同时成立；API 专用 `YIJIE_API_SERVICE_PROFILE=feat-153-workflow-local`；缺失时不启用，不改变原 api-server/OIDC/Tasks |
| 易界主体 | 使用既有 Rust owner `12500000-0000-4000-8000-000000000001`、tenant `12500000-0000-4000-8000-100000000001`、authorization revision 1；与 FEAT-125 历史 IdP profile 无关 |
| 服务身份 | Infra 受管启动每次生成 run epoch 和两个独立 256-bit 随机机密 K_NA、K_AC；K_NA 只供 native→API，K_AC 只供 API→Coze，不互用 |
| 交接 | 新建 ignored owner-only 运行文件，分别给需要的进程/只读容器挂载；不使用命令行明文、renderer env、日志或 Host/Codex 子进程环境传递；不改已有文件权限制造测试故障 |
| 短会话 E | API 颁发随机、resource/actor/run-epoch 绑定的编辑会话，绝对有效期 300 秒；只存 API/原生内存，server cookie 属性如使用则 HttpOnly，浏览器不接收该 cookie |
| 到期/关闭 | 不无限自动续期。到期保留未保存画布、禁写并显示“重新连接”；可信父页/native 重验同一主体/资源后重连，无账号登录。关闭、关功能、换 epoch、正常退出均撤销；旧 port/E 不复用 |
| API/Coze 校验 | 每次请求验证自己的服务凭据、run epoch、固定 scope、实际资源；editor 写入另验 E；Coze 内部读取真实 user/space/membership/workflow 绑定，不信任请求 space_id |

原有 `workspace.use` 只作本地产品入口条件；不添加生产 `workflow.*` 权限或扩大七项现有服务端权限集。新专用 local service 自己验证明确的 workflow 操作政策。浏览器 Origin/loopback 是附加限制，不是认证凭据。静态资产可以无认证读取，但所有资源、bootstrap、metadata、operation 和运行查询均要求正确受管身份。

Coze 新增 `EnsureLocalPrincipal`：通过 Coze 自己的事务创建或读取 synthetic user/space/membership 与本地映射；不得以同名邮箱领用其它账户，不调用公开注册/登录/PAT，不伪造 ApiKey 权限对象。API 不直接写 Coze 表。

## 4. 进程、存储及服务拓扑

同一个 API 仓新增专用 `cmd/workflow-local-server` 与 workflows 模块，复用已锁定 pgx/goose；不修改原 api-server 的认证入口、数据库 LatestVersion 或 public-api.lock。新模块采用独立 `yijie_workflow_local` PostgreSQL 数据库与自己的 migration 入口，正常启动前由受控脚本显式迁移。

Coze 保留 MySQL/Redis/搜索/对象存储及必要初始化依赖；首期不从源中拆纯引擎。新增 local adapter 和它自己的 MySQL migration，不要求 API 互读 Coze 私有表。具体必要镜像在第 4 步固定源构建及 digest 后激活，本文件不伪造未拉取的 digest。

| 存储 | 最少数据与权威 |
|---|---|
| API 独立 PG | fixed scope→Coze principal 关联；易界资源→Coze workflow 关联；operation 意图/请求摘要/相关 ID；append-only 业务审计。不要保存第二份 canvas、版本内容或引擎运行状态机 |
| Coze MySQL | 原有 draft/version/execution/node 事实；新增 local principal mapping 与 scope+operation ID+request hash 的写入关联；运行槽位/去重需与实际 execution 登记绑定 |
| 进程内存 | K_NA/K_AC、短编辑会话与 port/native editor binding；这些机密不入业务表 |
| Redis/对象存储 | 保留上游所需 checkpoint/临时数据/内置资源；不把 Redis 一概描述为可随意删除的缓存 |

本期只处理合成数据，草稿、内部版本、历史、operation receipt 和审计保留到显式另行清理；不做自动 TTL 删除、data migration downgrade 或 volume 重建。API/Coze 私有 schema 使用各自 migration，源契约由 Contracts 管 wire，不将数据库模型直接公开。

Infra 是工作流栈的唯一生命周期所有者，记录自有 project/run/container/process ID。18888 是唯一 host loopback gateway；18889/18890 仅作内部实现保留，不默认对宿主或公网发布。当前只读检查未见这些端口监听，不保证未来绑定成功；冲突时提示停止，不杀占用进程、不自动另选公网地址。

最小栈 opt-in 使用，不进入现有 Chat 默认必需依赖。Desktop 只能调用已经受管并验证 epoch/version 的服务，不通过任意 shell 启停 Docker。第 4 步为正常 up/status/stop 明确入口，使用已安装 Docker Desktop 及原厂 Compose；不自动启用上游 privileged/latest 默认配置。

正常停止先停止接收新写入、确认在途短运行达到真实终态、撤销 E，再停止自有服务并保留数据。**Docker stop 的有限超时会回退强杀，所以不得沿用默认/有限 timeout**；自有容器使用官方支持的 SIGTERM + timeout=-1，观察超时只报告 STOP_PENDING，不升级 SIGKILL、不清理未退出对象。使用有界客户端等待或异步观察，不能因此长时间阻断用户沟通。实际源码与 Docker 官方依据见 [边界附件](evidence/step2-boundary-feasibility.md)。

## 5. 工作流语义、并发和容量

| 项目 | 本期冻结语义 |
|---|---|
| 三节点 | 开始 type 1 → TextProcessor type 15 且 concat → 结束 type 2 且 returnVariables；一个 input 字符串、一个 result 字符串；前缀字面量 + 一次 input 引用；无代码/HTTP/模型/插件/循环/子流/跨流引用 |
| 未完成草稿 | 创建后默认 2 节点/空边仍可保存；草稿需通过安全结构/大小检查但可以不可运行。试运行与内部发布时才要求完整的 3 节点/2 边线性连通 |
| 容量 | input ≤4096 UTF-8 bytes，prefix ≤1024 bytes，result ≤5120 bytes；canvas ≤256 KiB UTF-8 JSON，消息 envelope ≤512 KiB；草稿 node≤3、edge≤2。大小限制在 API/Coze 两端最终校验，UI 提前反馈 |
| Revision | 使用 Coze draft.commit_id 的 string 投影；save 必带 expected revision，Coze 事务/CAS 更新图、新 revision 和 operation receipt。API 先读后写、进程内 mutex 或按钮禁用都不替代 CAS |
| 保存冲突 | 409/revision_conflict，保留未保存画布，允许明确重读/比较；不自动覆盖。不做本地持久化第二份权威草稿 |
| 试运行 | 固定请求 revision 的快照，再登记原生 debug execution。后续保存不改变该试运行输入图；不能仅靠 workflow 级 TestRunSuccess bool |
| 内部发布 | 必须引用同 workflow/scope/revision 的真实成功 debug run；再次检查当前 revision。Coze 事务分配 `v0.0.1` 起单调 patch 版本、保存版本并更新元信息；同次 operation 不重分配版本，不传 Force |
| 发布版执行 | 明确请求版本，以领域 FromSpecificVersion+Version 运行；不代理只执行 latest 的公开 `/v1/workflow/run` 后声称固定版本 |
| 并发 | 同 scope 的 debug/release 共用 1 个在途槽位；仅真实引擎终态释放。页面关闭、HTTP 超时、E 到期和 lease TTL 都不释放 |
| 时间 | 30 秒是绑定 runner 生命周期的合作式执行预算；不是 HTTP 等待超时，也不保证强制结束进程。预算到期无原生终态时显示 unknown/待核对并保留槽位，不猜 failed/cancelled，不强杀 |
| 历史 | Coze 新增按实际 scope/workflow 过滤的根 execution 列表；`created_at,id` 倒序 cursor，默认 20/最多 50；区分 debug/release 与 revision/version。不能用空 trace stub 或浏览器数组代替 |

Coze 原生 Save 未做 CAS、成功试运行标记未绑定 revision、公开 run 固定 latest、trace handler 为 stub 的出处及最小修改位置见 [Coze 可行性附件](evidence/step2-coze-feasibility.md)。这些是第 3 步待实现的能力，不是已完成承诺。

### 写操作与未知结果

所有 create/save/test/publish/run 由 native 生成 UUID operation ID。API 先记录意图/请求摘要；同一 ID、同一内容查询或返回原结果，不以重连生成新 ID 重复执行；同 ID 不同内容返回明确冲突。Coze 自己将 scope+operation ID+request hash 关联到 workflow/revision/version/execute ID，关键写入和关联在同一事务；API 不能在响应后才补映射并宣称幂等。

execution 准备阶段即建立 operation→execute ID 关联，再启动同一进程内任务。若只有已登记记录而执行事实未知，返回可查询未知状态，不自动重启作业；本期不实现崩溃后的调度恢复。创建/保存/内部发布也采用读回和 operation 查询确认。UI 的“再试一次”优先查原 operation；只有明确未执行或最终失败且用户再次发起时才建立新的操作意图。

Coze 是执行状态权威，API 只保存 receipt/关联；对状态的 unknown 是查询可用性信息，不能改写持久执行事实。

## 6. Contract First 的第 3 步输入

本文件规定语义，不取代 schema。计划在 `yijie-contracts` 新增独立 workflow-local OpenAPI 组和 workflow editor/native bridge v1 JSON Schema；原 public/Agent Host schema 及 API public-api.lock 不改成新工作流权威。

| 边界 | Producer / consumer | 源与兼容要求 |
|---|---|---|
| editor messages / native IPC | Coze React、Desktop Vue/Rust | Contracts bridge v1，未知 version/op 明确拒绝，受控容量；生成或同源 validator，禁止影子 DTO |
| native→API | workflow-local API / Desktop native | 新的本地 API 契约与独立 consumer source/digest/generator lock；原 API 锁不绕过 |
| API→Coze adapter | Coze adapter / API | 新可信内部接口同样源契约在先；Coze 现有原始图/节点 schema 固定上游作为内部适配依据 |
| 私有数据/部署 | 各服务 / Infra | 对应 migration/配置来源、reader 兼容、run epoch、probe、loopback 与正常停止，不硬塞 API wire |

需要定义的操作为 list/create/read/save/test/publish/run/get-run/list-runs/get-operation、editor open/close/status 和 bootstrap metadata。ID/revision/run 都用 string，版本为有限 `v0.0.N` 形式；error 至少区分 profile_disabled、service_unavailable、unauthorized、session_expired、resource_not_found、revision_conflict、operation_conflict、invalid_draft、input_too_large、run_busy、operation_unknown、protocol_mismatch。HTTP 状态及 JSON 精确形状在源文件一次定义，再生成实现，不在各仓独立发明。

本地源候选按 demo_fast 记录实际 full SHA/文件摘要与安全生成 conformance；不手改原生成文件、不虚构发布 tag/consumer 人工批准。整体 contract-impact=semantic；若方向验证发现破坏旧交互，升级 breaking。当前第 2 步只有文档，不改变 wire 或业务持久化，实际变更为 none。

## 7. UI 状态与正常验证

- 空列表明确提示创建通用流程；现有推荐卡保持示意，不纳入真实列表/历史计数。
- editor 服务加载、握手、保存、试运行/执行分别提示；10 秒静态壳或握手无 ready 时提供重新连接，保留返回。客户端等待超时不改远端状态。
- 未保存离开提供保存后返回/继续编辑/明确放弃；save 失败时不自动离开。
- E 到期保留内存画布并禁写；重新连接不 reload/unmount iframe，只关闭旧 port，由 native 重验资源并获得新 E，再对同一 iframe 建新 channel/generation。核对远端 revision，冲突仍保留内容，不自动 hydrate 覆盖草稿，不恢复过期端口。
- 关闭或停止等待只取消本地等待；已发出的写入由 receipt 查询确定结果，不能取消提示后偷偷重发。
- 结果页区分草稿试运行与固定版本执行，显示实际 run ID/版本/输出/时间；未知就显示待核对。
- 亮/暗、1180×760/1440×900、键盘与焦点、原用户布局/青柠色遵照 Brief。既有 contrast 问题独立记录，不冒称全页 axe PASS。

第 5 步资格必须先在真实最小 provider/受控栈和同一个正常 Desktop 中验证静态壳加载、MessageChannel 双向、IPC隔离、会话到期/重连、创建保存重开；dev 与 packaged 都需证据。未通过则不扩展完整 Desktop 功能，不用 browser-only、mock、任意 CORS 或宽泛 native capability 替代。

只使用正常操作与合成数据：空/普通输入校验错误→修正→成功，正常并发保存得到冲突，完成短流程后正常停止重开。禁止攻击 payload、危险归档、权限破坏、故障式强杀；默认危险测试保持 NOT RUN，使用已审查的 safe/focused 路径。未执行项及影响必须写验收记录。

## 8. D0、后续顺序与停止条件

第 2 步关闭的是设计问题：已批准方向、具体传输、固定 actor/机密生命周期、Coze 缺失能力的实施归属、UI 状态和 Must AC；不是运行资格。ADR-0019 转为 Accepted 时注明真实用户批准及本步技术细化，不捏造逐字段人工审查或已实现事实。

顺序固定：第 3 步源契约与最小 provider/native-session → 第 4 步受控栈 → 第 5 步真实载体资格再完整 Desktop → 第 6 步一次 fresh run 全部 Must AC/D4。未创建 GitHub 远端、未 commit/push，模型/付费/生产授权仍为 0。

保留的运行未知项是实际 bundle 初始化、MessageChannel 在两个 WKWebView 入口的表现、构建镜像/资源、数据库事务与执行取消配合。它们在后续真实步骤验证，不能写 PASS；失败按既有 30/90/120/240 分钟与 16 小时时间盒收敛，不扩大权限或跳过源契约。

## 第4步部署实现细化（2026-09-12）

实际依赖审计确认，上游完整 `application.Init` 会初始化与三节点文本流程无关的知识库、搜索、向量、MQ 与模型组件。第4步在同一 Coze 仓增加专用 `workflowlocal.InitRuntime`：直接组装原生 `NewWorkflowRepository`、`NewWorkflowService` 与节点适配器，保留 Redis ID/checkpoint、MinIO 对象存储和真实 MySQL；不拆出新引擎仓，不替换原应用入口。受控栈因此只有上述三项 Coze 依赖、独立 API PostgreSQL、Coze 与 API 六服务。此节取代第4节“保留搜索依赖”的宽泛假设，wire、身份、三节点与预算语义保持第3步源定义。

镜像在 Infra `images.lock.json` 中记录实际 registry digest、Linux arm64 与本机 image ID；API/Coze 另记录双采样源码摘要和标准 Docker build ID。MySQL 新数据集只提取已固定上游 schema 的55条 CREATE TABLE，排除原 opencoze 建库与业务 seed；随后显式执行 Coze 三项私有表 migration。PG 使用独立服务 migration。所有凭据由受管文件提供，API/Coze 配置权威已增加有界 FILE 输入和互斥校验，不通过环境值或 argv 传递机密。

Redis 采用官方固定8.0.3镜像，独立专用 volume，直接 redis-server 入口以 root 和唯一 DAC_OVERRIDE 读取 owner-only 配置；无 privileged、host network 或 Docker socket。MinIO 使用厂商 Quay 同一已审计 release。运行网络 internal，只有 API 发布 loopback18888。详见第4步实施记录与 Infra 操作手册；这些部署决策不代表 Desktop 或 D4 已通过。


第4步首次实际启动后，全部服务容器内ready且显式migration成功，但Docker29的internal-only API没有建立host端口（NetworkSettings.Ports为空）；资格工具在status前失败，尚未创建业务流程。已正常SIGTERM停止所有8个自有容器，均exit0/noOOM。拓扑细化为API同时连接本project的workflow-edge桥进行loopback18888发布，Coze及四项依赖保持internal-only；没有新增host端口/通用代理/模型平台调用。API edge不等同于物理禁止出站，实际入口仍固定源定义与私有Coze URL。后续readiness同时要求六服务健康及宿主带K_NA的真实status，不能仅凭容器内probe写PASS。此修正不涉及旧项目或数据库重建。
