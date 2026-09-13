# FEAT-153 第 2 步：API / Infra 最小边界方案

日期：2026-09-12。性质：用户同意继续方案后的只读源码核查与可实施设计，未修改 API/Infra/Coze 代码、启动服务或安装依赖。本文件不把设计可行性写成真实运行 PASS。路径均相对 CrossBSD 根目录。

## 1. 推荐结论

采用 **独立 local workflow API 进程入口 + 单个 Infra 生命周期 + 两段独立机器凭据 + 独立合成数据库**。Desktop 到服务的请求由 native 受管 transport 发起；18888 仅为固定访问位置，不能作为身份凭据。

具体推荐为在 `yijie-api` 新增 `cmd/workflow-local-server` 和 `internal/modules/workflows`，由 `yijie-infra` 的独立 FEAT-153 profile 管理。该二进制只装配 workflow 路由及其私有存储，不改原 `cmd/api-server` 的 OIDC、Tasks、FEAT-125/126 profile 或全局 migration version。不是另建代码仓，也不是在 Desktop 内实现业务后端。

本次 D0 具体方案采用 **HTTP 静态 editor → MessageChannel 非机密业务操作 → 父 Vue 的具名 native workflow command → native 固定 API transport**。静态资产与 API 共用18888，只有限定 editor assets GET 无认证；工作流 API 全部要求机器凭据，编辑操作另需短时 resource-bound session。iframe 不直接 fetch API，CSP `connect-src 'none'`；无新 URI scheme、TLS CA、WK cookie 注入或远程 native grant。真实平台资格仍在第5步验证，不能把设计写成运行通过。

## 2. 源码依据及已有约束

| 已有事实 | 证据 | 设计影响 |
|---|---|---|
| 原 API 只接受 default、FEAT-125、FEAT-126 profile | `yijie-api/internal/app/app.go:102` | 用新 workflow-local 专用 config，不把新行为塞进旧 profile |
| 原 API 启动需要 tasks/authn/RBAC/secure-task schema，严格要求 migration 4 | `yijie-api/internal/platform/database/database.go:36`；`yijie-api/internal/platform/migrations/migrations.go:16`、`:63` | 独立 workflow migration book 和独立数据库，避免本需求让所有旧 API 库无关升级 |
| 现有 JWT、tenant、permission 是公开 API 真实边界 | `yijie-api/internal/interfaces/publicapi/secure_task_handler.go:129` | 新 local adapter 单独路由/进程 gate；原公开校验不删除、不弱化 |
| API 已有 pgx、goose、uuid、oapi-codegen | `yijie-api/go.mod:5` | 无需新增数据库驱动、ORM、身份供应商或 generator |
| 现有 public-api lock 固定 SHA `29317b6426578749dc698fc2ad32b986ee5c8e9f` | `yijie-api/contracts/public-api.lock.json:3` | 单独新增 workflow source lock，不绕过或改旧 public lock |
| Source checker 核对 exact HEAD、tracked clean 和 digest | `yijie-api/internal/contracts/pin/pin.go:81` | 用精确 source checkout/候选生成入口，不能偷渡当前 dirty sibling 或手改 DTO |
| Native local scope 已固定 owner、tenant、revision | `yijie-desktop/src-tauri/src/local_profile.rs:6` | 复用同一 native scope 值，不让 renderer 输入任意 user/tenant |
| Coze Web API 使用 session cookie 和 context Session | `yijie-coze/backend/api/middleware/session.go:42` | PAT 不是 Web editor session 的替代；新内部桥必须明确建立受信 context |
| Coze Create user 依次写 space、user、membership，不是一个显式跨三项事务 | `yijie-coze/backend/domain/user/service/user_impl.go:252`、`:298`、`:329`、`:334` | 不无条件重复调用 register 当 bootstrap；需正常幂等 EnsureLocalScope 与读回核对 |
| OpenAPI run 会从真实 workflow meta 读取 SpaceID 并检查已发布版/用户权限 | `yijie-coze/backend/application/workflow/workflow.go:1551` | 内部 adapter 也必须读取真实资源归属，不能只信任请求的 SpaceID |
| Coze 默认主 server CORS 为 AllowAllOrigins | `yijie-coze/backend/main.go:86` | 不向宿主公开该原始 server；新增 local gateway 不继承 wildcard CORS |
| Coze debug access log 会记录 query/request/response 片段 | `yijie-coze/backend/api/middleware/log.go:64` | 新认证/编辑会话路径必须 content-free，运行 profile 不启用正文 DEBUG |

## 3. 精确入口、scope 与机器身份

### 3.1 新 local 服务 gate

新 workflow-local config 要求以下条件共同成立；任何一项缺失/不同均拒绝启动或不注册功能，不降级匿名模式：

- `YIJIE_ENV=local`；
- `YIJIE_LOCAL_PROFILE=demo_fast`；
- `YIJIE_WORKFLOW_LOCAL_ENABLED=true`；
- 版本化 profile 名 `feat-153-workflow-local-v1`；
- 固定 run generation、固定 local data-set ID、机器凭据文件和来源 manifest 合法；
- 宿主公开地址只有 `127.0.0.1:18888`；原始 API/Coze/PostgreSQL/MySQL/Redis/MinIO 等不另发宿主端口。

如果进程在 Compose 内，容器 listen 可以是其内部接口 `:8080`，**loopback 约束由唯一发布映射 `127.0.0.1:18888:8080` 加应用 Host/path/auth 校验共同实现**；不能虚称容器内 `127.0.0.1` 是宿主 loopback，也不能仅凭环境变量认定安全。

固定 native scope 来自已有 source authority：owner `12500000-0000-4000-8000-000000000001`、tenant `12500000-0000-4000-8000-100000000001`、authorization revision `1`。这些值复用的是当前 Desktop local authority，不复用 FEAT-125 的 OIDC profile、数据库或历史运行证据。API 的 local scope registry 必须与同源 scope fixture 相等；请求中的同名字段不构成授权，首版写请求不接受可覆盖 user/tenant/space 的字段。

local workflow 操作权限闭集建议为 `workflow.read`、`workflow.edit`、`workflow.run`。固定 local owner 允许三项；session 进一步只授予所需资源与操作。先登记 Contracts/本地 capability source，再扩展 Desktop local capability，不能在原公开 API `InitialPermissions` 中暗增生产授权。`workflow.read` 覆盖列表/读回/结果历史，`workflow.edit` 覆盖创建/保存/试运行/内部发布，`workflow.run` 覆盖选定内部版本运行。

### 3.2 两段机器凭据：生成者、持有者、交接

| 凭据 | 生成者 | 允许持有者 | 用途和失效 |
|---|---|---|---|
| `K_NA`，native→API | Infra 唯一 workflow lifecycle helper，以 CSPRNG 生成 32 bytes | Desktop native transport；workflow API | 一个 run generation 的机器 bearer；只向精确 origin 和 operation 路由附加，停止该 generation 后失效 |
| `K_AC`，API→Coze | 同一个 helper，独立随机值，不能复用 K_NA | workflow API；Coze local internal adapter | 只用于固定 internal workflow bridge，不能调用通用管理 API；停止后失效 |
| editor session `E` | workflow API 在 K_NA 认证后生成独立 32 bytes | workflow API；该 editor 专属 native 内存 jar | 一个 workflow/resource、一组 editor operation、一个 generation；5 分钟绝对期限，关闭销毁，到期由可信parent显式重连同resource |

生成与交接方法：helper 在被 Git 忽略的 `yijie-infra/environments/local/generated/feat-153/<generation>/` 下用排他创建写文件，目录 `0700`、新 secret 文件 `0600`，避免覆盖已有文件；这属于正常创建受保护数据，不是权限故障注入。各服务只挂载自己的 secret 文件为只读；Compose environment 只包含文件路径，不含 secret 值。Native 只接收 K_NA 文件的固定路径/manifest，不接收 K_AC；renderer、Coze frontend、构建命令、模型/Host 子进程均不收到这些凭据。

Native/服务读取时验证路径处于该 generation 下、普通文件/非 symlink、owner、权限、长度；在内存保管，错误不打印值。API 使用固定长度的常量时间比较，不把 generation、Host、Origin、tenant ID 或端口空闲当作身份验证。请求不允许 redirect，HTTP client 不继承环境代理，固定 method/path/body schema，不提供通用 proxy IPC。记录仅包括 generation、operation、request ID、资源 opaque ID、状态码及耗时，不记录 Authorization/Cookie/正文。

为避免端口占用被误认为服务：启动前核查端口；既有监听者不是本 helper 管理的当前 generation 时拒绝接管；up 完成后核对 Compose project/service/image/source labels 与机器认证的 readiness 响应，再返回 ready。Native 不向用户任意输入的 URL 或未匹配 manifest 的旧服务发送 K_NA。此方案不把 loopback 变成公开授权，也不设计一个新的生产身份系统。

### 3.3 API→Coze 内部身份

新增 Coze local-only `/internal/yijie-workflows/v1/...` 窄路由和 middleware。先检查 exact profile、K_AC、generation，再加载该 data set 固定 synthetic user/space；把经过查询核验的主体写入调用 context，调用真实 application/domain 服务。不要把请求 header 提供的 userID 直接塞进现有 Session context，不构造或泄漏 PAT，也不拿一个万能上游账号 cookie 当整个产品边界。

创建合成 scope 使用 Coze 自己的 `EnsureLocalScope`：以固定 local scope key/合成 unique identity 找到或创建同一 user、space、membership，原子创建或准确读回核对。现有 Create 的多个写入不能被当成已具备该原子性；需要在 Coze 所有的 DAL/transaction 内补齐，失败/部分完成时查询核对，不能盲目重建。随机不可交互 password 可仅在初次创建时由服务生成、只保存现有 Argon2id hash，不向用户或 API 返回；不开放 register/login 管理页。

每次资源操作：API 验证 `(local scope, Yijie workflow ID)` 映射；Coze adapter 再从真实 Meta 读取 `SpaceID`、`CreatorID`/所属关系并与固定 Coze scope 相等，才调用业务。编辑器操作通过同一允许列表，不能绕过这条核权。原有普通 Web API 的 request SpaceID 校验不足以替代实际资源核对。

## 4. 编辑器 session 与 native transport 的分界

E 不返回给 renderer。API 可通过带 HttpOnly 属性的 Set-Cookie 交给 **native HTTP client 的专属内存 cookie jar**，作用域只限精确18888 API与本editor。候选cookie为host-only、无Domain、固定editor API Path、Max-Age=300、HttpOnly；由于此专属jar只走HTTP loopback，不使用要求HTTPS的Secure前缀，也不把这份local-only cookie设置复制到浏览器或公开入口。不能把该响应转发给 iframe/WKWebView，也不能把Cookie值放进IPC、postMessage、MessageChannel、URL、localStorage或日志。K_NA/K_AC从不成为cookie。API只保留E哈希、scope、workflow ID、operation set、run generation、issued_at/expires_at。

静态 editor 只做无认证 GET 加载自有 HTML/JS/CSS/固定图标；由父窗口向本次真实 iframe 交付一个 MessagePort。通道只允许源契约中的白名单业务operation、关联ID和受控业务参数，**不是身份凭据，也不包含机器key或E**。父Vue只调用已命名的native workflow commands；native根据自己持有的editor会话、固定resource与generation验证操作，再向精确API附加K_NA及E。iframe的JS没有invoke权限、通用fetch、任意URL代理或原生能力。

所有来自editor的resource/space/user字段均为不可信业务选择；native和API使用当前受管会话绑定的真实resource，不能因MessageChannel连通就视其参数为已授权。API请求还必须通过真实workflow Meta归属核验。父窗口/iframe销毁后关闭MessagePort并销毁对应native jar；迟到消息因会话generation失效拒绝，不能转到新editor。

E绝对有效期固定5分钟，无滑动自动延期。到期返回稳定的`editor_session_expired`，保留未保存内容并暂停写入；可信父页面明确显示重新连接动作，用户操作后由native重新鉴权并为**同一resource**创建新E。不能无限自动续期或把重连改成新建workflow。关闭editor时销毁E；正常stop/new run-epoch后所有旧E失效；服务端状态丢失亦拒绝旧E，不以旧cookie恢复授权。

请求allowlist分开静态assets GET与受认证API：editor assets不读取业务/用户数据；全部workflow API要求K_NA，编辑API同时要求E。固定user/space自身元数据、workflow画布/保存/试运行/内部发布/节点结果由MessageChannel→native链承接。禁止`/admin`、通用login/register、插件、知识库、市场、任意上传/URL代理，不直接转发全部`/api/*`。Coze前端必须将实际API调用改接白名单transport，缺路径时明确不支持，不放开CSP补洞。

本D0选择HTTP静态资产与native-only机密传输，不需要browser cookie，也不需要给HTTP跨站iframe塞Secure Cookie。必须在第5步验证静态资产/MessageChannel/CSP/具名IPC/native jar/真实provider全链；不能因为没有TLS依赖就提前记资格PASS。

## 5. 最小 API 私有 schema 与数据保留

**需要私有新表。** 仅 memory map 不能满足正常停止后列表、资源归属、create/run 不确定结果追踪与历史。建议独立 PostgreSQL 数据库 `yijie_workflow_feat153_local`；复用已有 PostgreSQL 16 系列镜像和 pgx/goose 库，但独立容器/volume/用户，不使用 `yijie_api`、FEAT125/126 或 Chat 数据。

`cmd/workflow-local-migrate` 管理独立 embed migration，初版 `00001` expand；使用该数据库自己的 goose book。旧 API 的 `LatestVersion=4` 和既有 migrations 不改。若未来合并进普通 API，应另作迁移设计，不在本地方案中偷偷变更旧启动兼容。

| 表/字段建议 | 约束与用途 |
|---|---|
| `workflow_scope_bindings`：scope_key、owner_user_id、tenant_id、coze_user_id、coze_space_id、created_at | scope_key 主键；固定 native tuple；Coze int64 ID 在 wire/Go adapter 边界使用十进制字符串，数据库可 bounded text；Coze user/space 各自唯一；无 secret |
| `workflow_resources`：id UUID、scope_key、coze_workflow_id、created_at、updated_at | `(scope_key,id)` 唯一与所有查询复合约束；Coze ID 唯一；只建立真实资源归属/映射，不复制流程图。名称/revision/published version 可从 provider 查询，不作为另一权威 |
| `workflow_operations`：id UUID、scope_key、workflow_id nullable、kind、idempotency_key UUID、request_sha256、delivery_state、coze_run_id nullable、coze_version nullable、result_ref nullable、created_at、updated_at | unique(scope_key,kind,idempotency_key)；kind 为 create/save/test_run/publish_internal/run；delivery_state 只描述接收/转交/结果已知或未知，不能冒充 workflow 执行状态；只存无正文的结果关联 |
| `workflow_audit`：id、scope_key、operation_id nullable、resource_id nullable、action、outcome_code、occurred_at | append-only；记录允许/拒绝/写入意图/结果与 resource 关联；不记录图/输入/输出/凭据；事务写入与本地映射/receipt 同提交 |

运行历史首版可从 `workflow_operations` 中已建立关联的 test_run/run 行形成 **本产品发起的运行索引**，逐项向 Coze 查询真实执行事实；这不冒称可列出所有上游历史。无 Coze run ID 的未知操作单独显示“请求结果待确认”，不造一条 execution。分页固定 created_at/id cursor，范围限制固定 scope。若 Coze 自身已提供合适的带 scope 历史列表，则 adapter 可使用它，仍以其结果为真实运行来源。

revision/version 的权威在 Coze：保存需要 Coze 支持并核验 expected revision，或在其本地扩展中以单一事务实现版本检查；API 只保存关联/最后读到的值，不能靠本地加一假装跨进程原子 CAS。API 的单在途限制、per-resource 串行化能减少并发，但不能替代 Coze 的保存原子性。已发布 version 与 run 绑定必须由 provider 返回/读回证实。

保留建议：此 data set 仅合成内容；草稿、内部版本、操作关联、审计和已完成运行数据保留直到明确删除该 FEAT-153 data set，无后台自动清理/TTL 删除。session/E 只在内存存活5分钟，关闭即销毁，run-epoch变化即失效，机器 secrets 仅本 generation；停止后废止并正常删除该次临时 secret 文件，保留业务 volume。首期表数/记录规模有明确上限（建议最多100个流程、每流程100条运行展示），达到上限显示可理解限制，不自动删历史或后台清库。最终数值由 Contracts/产品规范一次冻结。

## 6. 操作映射与不确定结果

| 易界 operation | API 工作 | Coze 工作 |
|---|---|---|
| list/read | 固定scope查询资源映射，bounded分页/逐条lookup | 真实Meta/Canvas/版本信息，只访问本scope |
| create | 先持久化意图/idempotency，再调用、读回并建立资源映射 | 真实创建有效三节点草稿；按同一operation查询结果，不能盲目重建 |
| save | 核对资源和expected revision，写入receipt | 原生或local扩展CAS保存；返回新revision/读回 |
| test-run | 核对草稿限制，1在途，记录operation→run关联 | 原生草稿试运行，返回执行ID/节点结果 |
| publish-internal | 只对成功试运行对应revision，禁止Force | 内部发布固定版本并读回 |
| run | 固定已发布version，记录关联，不能选任意scope/节点 | 真实版本执行与原生终态 |
| get-run/list-runs | 验证workflow/run属于scope；索引后读真实provider | 按真实execute ID/版本查询，不由API创建第二状态机 |

create/publish/run 不作无条件 HTTP 自动重试。连接在结果返回前中断时，receipt 进入 outcome_unknown，后续先按同一 operation/provider key 查回；未能证明未执行时不得再次发送。不存在 provider 幂等/按意图查询能力时必须明确“未知，需要核对”，而不是给自己生成新 run ID 后重跑。这是传递状态追踪，不是新工作流执行引擎。

## 7. Infra 拓扑与唯一生命周期

唯一 authority 为 `yijie-infra` 的 FEAT-153 Compose/profile 及固定 `workflow-local up|status|stop` helper。Native 通过窄操作请求 helper；native 不另行 spawn 第二份 API/Coze，也不自己运行 docker kill/down。Compose 使用固定 project/data-set ID；同一时刻只允许一个 owner generation，第二个 Desktop 请求不能默默接管旧栈。

推荐拓扑：宿主 `127.0.0.1:18888` → workflow-local API/gateway → 内部 Coze adapter；其余 API PostgreSQL、Coze MySQL/Redis/Elasticsearch/MinIO/Milvus/etcd 按当前真实初始化链在专用 Docker 网络中。前端仍由 Coze canonical Rush 构建，静态结果供 gateway 的受控 editor route 使用；能否省去独立 coze-web 容器以实际构建产物装配为准，不先假定 backend Dockerfile 已包含前端（`yijie-coze/backend/Dockerfile:55` 中 static copy 目前注释，frontend Dockerfile `:48` 另拷贝 dist）。

不引入 Keycloak、Caddy 或其它新框架为默认依赖；PostgreSQL/pgx/goose、Go net/http/crypto、Coze 现有组件足够承载此边界。Milvus 等即使不用于三节点，初始化链是否可裁掉仍需 Coze 源码与真实启动证明；不预先宣布极简三服务栈 ready。所有新增镜像固定 version/digest 或本地 canonical build identity，禁止 latest、privileged、host networking、Docker socket mount，禁止继承 upstream 开放 admin/CORS 的 gateway。

正常启动：检查daemon/plugin和端口 → 验证source/build manifest → 创建本generation两段secret → 启动审查过的依赖并等待health → 运行该独立数据库的显式migration与正常scope bootstrap → 启动API/Coze bridge → 验证机器鉴权ready → native取得会话。任何一步失败不得把已启动部分标为整体ready；记录并正常停止自己创建的服务，不删除业务volume。

正常停止：先禁止新workflow写操作并关闭editor session，查询原生在途状态；首期要求已执行短流程完成后停止。Native调同一个helper release，由它核对本project/generation的精确container IDs并按依赖逆序停止。先调用服务可用的正常清理入口；容器停止使用官方`docker container stop --signal SIGTERM --timeout -1 <已核对的自有container ID>`，避免默认超时升级SIGKILL。Helper以有界状态观察并向UI回报；仍未退出则报告`STOP_PENDING`并停止后续清理，不升级kill、不删除volume、不让重复up占用旧数据。这里只冻结安全停止语义，未实际执行该命令。依据[Docker官方stop文档](https://docs.docker.com/reference/cli/docker/container/stop/)：默认宽限期结束会强杀，timeout=-1则等待自然退出。

不要机械复用旧`compose down --timeout 30`作为本需求“不强杀”的证明。不支持的在途取消显示等待/明确限制，不用故障注入验证；已全部正常停止后才允许移除自有已停止容器/网络，业务volume保留。未选用工作流时不调用up流程，不影响原Chat使用。

## 8. 端口、Docker 与 TLS 只读结果

本次命令：`lsof -nP -iTCP:18888 -sTCP:LISTEN`，18889、18890 同样查询，均无输出。说明该时点未见监听，**不是端口预留、可绑定保证或启动成功证据**；启动前须再次检查。本方案只建议使用18888，不因为另外两口空闲就自动开放它们。

原厂 `/Users/jack/Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose version` 返回 `Docker Compose version v5.3.0`。`docker version` 为 CLI `29.6.1`、server unavailable；当前 daemon socket 不可达。本次未 open app、切 context 或启动容器。

已有 TLS 只能复用做法，不能复用身份和资源：

- `yijie-infra/config/feat-125-local/Caddyfile:1` 与 feat126 文件都声明 `skip_install_trust`，站点固定旧 8443/9443、旧upstream；不能直接把它们改成FEAT153入口。
- `yijie-api/internal/platform/authn/local_ca.go:38` 的固定CA client只约束该API出站TLS，不改变WKWebView系统信任。
- `yijie-infra/scripts/feat-125-local-ca-trust-macos.sh` 的 install 明确修改用户Keychain trust，既有授权/证书不自动覆盖新服务；本次没有读取Keychain或证书秘密，也没有导入信任。
- 若最终选择HTTPS iframe，应新建独立证书/CA scope并具体确认WKWebView信任方式；不得关闭TLS验证、借旧私钥/volume、自动全局trust或将HTTP跨站cookie成功当既定事实。

本次确定采用HTTP静态editor/MessageChannel/具名native command：静态资产可以浏览器GET，全部业务API由native请求，E只在native内存jar，iframe CSP connect-src none。不引入新custom scheme、系统信任或remote native capability。该方案的真实资格仍须第5步实跑；如失败，收口替代设计后再启用，不用“localhost安全”作为绕过身份或浏览器安全的理由。

## 9. Source-first 和下一步可判定输出

先在 Contracts 新建 workflow-local 源及fixtures，冻结scope、operation、ID string、revision/version、session handle、错误、读写与取消语义；API 新增独立 `workflow-local.lock.json`、生成目标和conformance。现有 public lock保持原SHA，原generate-check继续使用其准确source checkout；不同契约有不同真实来源可以记录，但不能把一个sibling HEAD同时写成两个不同exact pin都已验证。未形成immutable source时仅按已批准demo_fast规则候选生成，不宣称发布/全量兼容或关闭旧锁。

本文件可用于D0决策的具体输出是：独立API入口/数据库、固定native tuple、三项local权限、两段机器secret的生成/持有/交接、E仅native jar/5分钟绝对期限/显式同resource重连、四张最小私有表、来源锁策略、18888候选、唯一Infra生命周期与无超时强杀的正常停止。静态editor和MessageChannel传输已确定，契约须同步定义operation闭集与失败语义；真实资格在第5步，不省略它后声称端到端可用。

未执行：所有构建/生成/migration/bootstrap、Docker Desktop启动、容器ready、机密创建/读取、API/Coze请求、编辑器加载、cookie/native jar资格、真实运行/正常stop-start、所有攻击或故障注入。原因是本步只做精确设计与只读可行性核查；因此本文件不存在运行PASS、D4、生产安全或可恢复执行承诺。
