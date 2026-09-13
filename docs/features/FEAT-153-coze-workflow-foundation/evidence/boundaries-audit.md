# FEAT-153 API、Contracts、Infra 接入边界审计

- 审计日期：2026-09-12，Asia/Shanghai。
- 审计性质：接入前只读源码、配置、工具可用性核查；不是运行、漏洞扫描或 D4 通过证据。
- 本文件所有 `仓库/路径:行号` 均相对 CrossBSD 工作区根目录，行号为本次读取时位置。
- 审计阶段未修改业务仓、安装依赖、启动/停止服务、构建、运行容器、读取真实凭据或实施攻击测试。本文件是该阶段唯一新增的审计产物。

## 1. 来源与事实范围

| 仓库 | 完整 HEAD | 初始工作区 |
|---|---|---|
| yijie-api | `f9d730a157bcb012a8fe178cbfebcd4ea27419fc` | `git status --short` 无输出 |
| yijie-contracts | `811f38d6b104fa18477107e7ac91a85e19c445d1` | `git status --short` 无输出 |
| yijie-infra | `19b7920696904f83030a8ddaba71af15c3c05ad8` | `git status --short` 无输出 |

本次完整读取上述仓库 AGENTS.md、README.md、SECURITY.md，并定位实际入口、契约锁、身份/租户/授权模块、migration、Compose 和正常退出代码。另核对元仓 AGENTS.md、Contract First、ADR-0012 与 ADR-0018，区分本地 Demo 和公开/生产边界。

Coze 上游来源比对由并行的源码来源审计负责。主任务已报告当前目录对照 `coze-dev/coze-studio@fefb05ff27be1da939612fbf9faf5db62583b8ae`；本边界审计不把该报告写成自己重新完成的 Git 来源验证。`36Dge/yijie-coze` 可访问性、远端创建和仓库可见性由主审计/Owner 决定，本文件不创建或更改远端。

## 2. 已核实事实、冲突和影响

### B-01：不存在可直接消费的易界工作流服务接口

**事实。** `yijie-api/internal/app/app.go:193` 起组装 status、access、legacy Tasks 和 gated secure Tasks；`:217`–`:229` 没有 workflow list/create/read/save/run/history 路由。对 API internal、Contracts OpenAPI、Infra 配置的 workflow 检索没有发现对应业务实现。

**事实。** 现有 secure Tasks 仅支持 `conversation`，输入被严格限制为 `schema_version=1`、`content_mode=local_only`、`client_reference_id`：`yijie-api/internal/modules/tasks/application/secure_service.go:44`、`:53`、`:67`。它不是工作流图、执行参数或执行历史的通用存储接口。

**建议。** 在 API 新建 workflows 模块及明确的 application port；Coze DTO 和协议映射留在 infrastructure adapter。不要复用 `/v2/tasks` 填入流程图，也不要让 Desktop 绕过资源授权直接使用任意 Coze workflow ID。

**未知。** 最终工作流公开路径、保存 revision、执行 snapshot、发布是否为必需步骤、列表与历史分页、超时/重试/终态和资源保留策略尚未冻结。

### B-02：已有身份组件，不代表新服务身份桥已经获准或实现

**事实。** API 具备固定 audience、RS256、issuer、JWKS 和时间声明校验：`yijie-api/internal/platform/authn/verifier.go:69`、`:91`。现有 secure handler 依次 authenticate、解析不受信任的 tenant header、VerifyActive、Check permission：`yijie-api/internal/interfaces/publicapi/secure_task_handler.go:129`。

**事实。** 当前 domain permission 目录只有 7 项，无 `workflow.*`：`yijie-api/internal/modules/authorization/domain/permission.go:27`。未知 permission 会被拒绝：`yijie-api/internal/modules/authorization/application/service.go:50`。当前身份/RBAC schema 由 goose migration 00002 管理：`yijie-api/internal/platform/migrations/sql/00002_expand_identity_tenancy_rbac.sql:2`、`:19`、`:29`、`:41`。

**事实。** 既有 FEAT-125/126 是历史专项 profile。API 配置只接受 default、feat-125-local-lab、feat-126-s10-local-lab：`yijie-api/internal/app/app.go:102`。FEAT-126 还锁定 nonproduction、专用数据库、issuer/JWKS/CA 和 secure Tasks：`:142`；FEAT-125 同样有精确 local issuer/CA 边界：`:176`。不能把 FEAT-153 工作流搭在历史 profile 的名义下。

**事实。** ADR-0018 的现有授权是 Desktop Rust native 固定 synthetic owner/tenant/revision、既有本地 capability 和 Chat/Artifact direct-entry：`yijie/docs/adr/ADR-0018-local-demo-direct-entry.md:31`。其 public-task 本地绑定明确不访问 API access/Tasks：`:38`；canonical launcher 当前只装配 Desktop、Host、Runtime、MiniMax 与 Artifact 所需变量：`:44`。这不等于已授权 API 或 Coze 接收前端提交的固定 tenant/user，也没有定义新服务会话或 token。

**建议。** FEAT-153 新服务桥必须独立写清 local-only 信任边界。沿用零登录的产品要求，不引入正常使用时的账号/密码/Keycloak 步骤；同时保留 ADR-0012 的 public/production JWT 与服务端租户授权，不把 local bridge 变成通用生产入口。

### B-03：API 已有契约锁；仓库文字状态过时

**事实。** `yijie-api/contracts/public-api.lock.json:3` 固定 `0.3.0-candidate`、Contracts 完整 SHA `29317b6426578749dc698fc2ad32b986ee5c8e9f`、源/生成物 SHA-256 和 oapi-codegen v2.7.2。CI 在 `yijie-api/.github/workflows/ci.yml:34` 固定相同 Contracts SHA，并在 `:43` 执行 generate-check。

**事实。** `yijie-api/internal/contracts/pin/pin.go:81` 要求 source HEAD 精确匹配 lock、tracked worktree clean、source digest 相同。当前 sibling Contracts HEAD 为 `811f38d6...`，不能把默认 sibling 路径当作现有 pin 的验证来源。`yijie-api/Makefile:28`、`:35` 已调用这些锁校验。

**冲突。** `yijie-api/AGENTS.md:23`–`:25` 仍称没有 lock 和 CI drift，已与上述代码冲突。`yijie-contracts/AGENTS.md:110` 仍称 OpenAPI 未定义认证，但 `yijie-contracts/openapi/public/public.yaml:282` 已有 userBearer，`:294` 定义经服务端验证的 tenant selection header。应在后续限定范围内修正文档事实，不能据旧文字再造第二套机制。

**治理区分。** `yijie/AGENTS.md` 的当前 demo_fast 规范允许 source-first 且适用 generate/lint/focused conformance 通过后，使用当前 sibling commits 做本地真实闭环；这不是发布 tag、生产兼容或 Consumer 批准。另一方面，现有 API pin checker 是真实代码限制，不能跳过或手改生成文件。应确定本地 candidate 来源/摘要并按正式生成机制更新验证，或使用锁定 source checkout；公开/生产再履行完整不可变 pin、支持基线及下游评审门禁。

### B-04：默认 Contracts 全量验证包含被用户禁止的危险 fixture 生成

**事实。** `yijie-contracts/scripts/generate.mjs:251` 默认调用 `generate-skill-bundle-fixtures.mjs`；后者 `:424` 写出 `fixture-zip-slip.zip`。`yijie-contracts/package.json:25`、`:31` 的默认 generate/test 会经过生成或生成同步链。

**事实。** `yijie-contracts/package.json:26`、`:32` 已提供 `generate:safe`、`check-generated:safe`，其参数跳过上述 skill fixture 生成。

**执行约束。** 本轮用户明确禁止危险归档/攻击 fixture 和攻击注入测试，不能以历史测试、开发环境为理由执行。后续选用安全生成和经源码审查的针对性 conformance；不得直接把默认全量命令作为“必须执行”的捷径。

**未执行及影响。** 本审计没有运行任何生成或测试。未来若跳过历史 skill archive 测试，必须写明该历史能力未复验；针对新增 workflow 的正常输入、空列表、失败、并发、重试和持久化仍应提供独立真实证据，不得以跳过危险 fixture 为由跳过必要功能验证。

### B-05：原始 Coze Compose 不可原样并入现有 Infra

**事实。** Infra 对允许服务集合做精确校验：`yijie-infra/scripts/compose-model.mjs:68`。新服务必须同步拓扑 authority、validator 和文档，不能只复制一段 Compose。

**事实。** 原始 Coze Compose 包含 `latest` app images（`yijie-coze/docker/docker-compose.yml:389`、`:421`）、多个 `privileged: true`（例如 `:88`、`:121`、`:207`）、固定 container_name；web 端口默认 `${WEB_LISTEN_ADDR:-8888}:80`（`:424`），未默认约束 loopback。server depends_on MySQL、Redis、Elasticsearch、MinIO、Milvus（`:404`）；不能假定简单流程已经证明可裁掉其它初始化依赖。

**规则。** Infra 要求 loopback、明确 image、healthcheck、持久数据用途和不影响已有默认启动：`yijie-infra/AGENTS.md:60`。新服务/端口/volume、出站网络和额外 capability 需要审查：`:81`、`:107`。

**建议。** 新增默认关闭、命名空间独立的 FEAT-153 local profile，固定经过审查的镜像版本/摘要，只开放必要 loopback 入口；Coze 的 MySQL/Redis/对象存储等不直接复用易界已有业务数据。先按实际初始化链验证最小依赖，再决定裁剪。不能先启动 upstream privileged/latest 默认栈再补审查。

### B-06：正常退出路径可参考，当前没有运行验证

**事实。** API 正常监听 Interrupt/SIGTERM 后调用 `server.Shutdown`：`yijie-api/cmd/api-server/main.go:154`、`:166`。FEAT-125 wrapper 的 stop 指定自己的服务：`yijie-infra/scripts/feat-125-local-compose.sh:23`；FEAT-126 wrapper 使用独立 project，down 不删除 named volumes：`yijie-infra/scripts/feat-126-s10-compose.sh:28`、`:60`。

**建议。** FEAT-153 正常停止应只影响自己持有的服务和应用，保留持久 volume，优先应用自身清理及正常停止；若不能正常退出，停止步骤并报告，不追加强杀。不要复用旧 profile 的资源标识，不运行 down --volumes、volume rm 或 prune。

**未知。** Coze/依赖在本机是否能 ready、正常停止及重启恢复数据均未验证。现有脚本存在 stop 命令不等于本次已获得 graceful-stop PASS。

## 3. 宿主工具与 Docker 运行时只读核查

| 命令/核查 | 本次实际结果 | 可据此得出的结论 |
|---|---|---|
| `command -v docker` | `/opt/homebrew/bin/docker` | PATH 中有 Docker CLI |
| `docker version --format '{{.Client.Version}} / {{if .Server}}{{.Server.Version}}{{else}}server unavailable{{end}}'` | `29.6.1 / server unavailable`；提示无法连接 `unix:///Users/jack/.docker/run/docker.sock` | 当前 daemon 不可达，未启动 daemon |
| `docker context ls --format '{{.Name}} {{.Current}}'` | `default false`；`desktop-linux true` | 当前使用 desktop-linux context；未更改 context |
| `docker compose version` | `docker: unknown command: docker compose` | 当前 PATH CLI 没有发现 Compose plugin |
| 常规应用路径目录检查 | `/Users/jack/Applications/Docker.app` 存在 | Docker Desktop 已安装 |
| `PlistBuddy -c 'Print CFBundleShortVersionString' .../Docker.app/Contents/Info.plist` | `4.82.0` | 本地 app metadata 版本 |
| `/Users/jack/Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose version` | `Docker Compose version v5.3.0` | 原厂 bundled Compose 存在且 version 子命令成功；无需推断机器根本没有 Compose |
| `command -v docker-compose colima limactl orb orbstack podman nerdctl` | 均无路径 | 这些命令不在当前 PATH |
| `/Applications` 与 `~/Applications` 的 Docker/OrbStack 常规位置，以及 `/Applications/Podman Desktop.app` | 除上述用户目录 Docker 外未发现 | 不代表经过全盘安装清单审计；不断言所有其它位置均不存在 |
| 工作区根目录 `go version` | `go version go1.26.4 darwin/arm64` | 宿主默认 Go 版本；未触发项目内 toolchain 自动下载 |
| `node --version` / `pnpm --version` | `v26.0.0` / `11.19.0` | 满足 Contracts/Infra engines；packageManager 声明为 pnpm 11.7.0 |

`yijie-api/go.mod:3` 要求 Go 1.26.5；宿主默认 Go 1.26.4 尚不足以单凭版本命令证明 API toolchain ready。`yijie-coze/backend/go.mod:3` 声明 Go 1.24.0。未安装、切换或下载任何 toolchain。

**正常启动候选与实际验证必须分开。** 已安装的 Docker Desktop 可作为后续原生正常启动候选，bundled Compose 可以通过其实际路径使用。尚未执行 app launch，不能声称 Docker Desktop 启动成功；daemon、容器和服务 readiness 仍为 NOT RUN。不能通过强杀残留进程、替换 binary 或临时伪装可执行程序修复这一前置条件。

## 4. 最小 local 身份桥接候选（建议，尚未批准/实现）

候选目标：保留 canonical Desktop 零登录体验，使每一次 workflow 操作有真实的受管进程身份和固定本地资源 scope；不把生产 OIDC 改成固定用户。

1. 以 FEAT-153 专门决策扩展 local direct-entry 边界，要求精确 `local + demo_fast`、额外 workflow 启用门禁和 loopback listener。非 local 或缺 gate 时整个 bridge 不注册。ADR-0018 只提供产品入口原则与既有 native authority，不能自动替代此项决策。
2. Desktop Rust native authority 是本地 synthetic owner/tenant 的来源；renderer 只调用有名称的 workflow IPC 操作，不提交任意身份、任意 URL 或任意 Authorization header。
3. 推荐首期由 API 的独立 local workflow adapter 接受受管 native transport。进程凭据由 launcher/native 自动生成与保管，面向精确 API origin，用户无需输入；凭据不放在 URL、renderer storage 或日志。其生命周期、传递介质和验证方式必须在源契约/部署方案中具体化，不在此凭空指定为已实现 JWT/SSO。
4. local adapter 核验进程调用资格后，在服务端绑定固定 synthetic scope；客户端提交的 tenant/user 不构成授权。API 只允许该 scope 对映射资源执行已定义的 list/create/read/save/run/history，不能根据任意 Coze ID 执行。正常 public API 继续走原 JWT/RBAC，不将 local adapter 混入既有 production endpoints。
5. API/Coze 的桥接在服务端维护一个合成用户/空间映射；Coze 原生流程定义、版本和执行事实仍由 Coze 管理。映射的创建、重开、持久化和恢复必须可追踪；若需要新 API 私有表，走新 migration 及明确兼容方案，不改历史 migration。
6. 编辑器入口必须补完同一授权链。推荐评估同源的受控 editor gateway/session handoff：仅为指定资源创建有时效的会话，秘密不经 URL；不能简单打开原始 Coze 管理台并把登录页或匿名权限当作整合完成。Cookie/session、CSRF、origin、WebView 限制、外部浏览器是否允许，以及 Coze session 退出/过期处理仍需源码可行性核查。
7. 正常关闭由原生 launcher/API/Coze 各自正常退出/清理；进程凭据失效，已有流程与历史保留。重开验证使用同一批准的 synthetic resource mapping，不复用 FEAT-125/126 的数据库、profile 或证据。

其它可行方向：完全走公开 OIDC 模型更接近生产，但与当前本地零登录和最小依赖目标不匹配；Desktop 直接访问 Coze 能减少一次请求跳转，但会绕开拟定 API 资源关联/审计，并迫使桌面承担 Coze 认证与协议耦合，不推荐作为该基础集成的默认架构。上述比较不是对 API bridge 安全设计的最终批准。

需由 FEAT-153 设计/Owner 收口的事项：新 local bridge 的具体 authority 与 token/session 生命周期；API 是否进 canonical launcher；固定 scope 的身份值和资源映射保留；工作流 capability 名称/编辑与执行权限；Coze 会话桥接可行性；编辑器窗口形态；使用哪个已安装 Docker 启动入口；镜像/端口/volume/资源限制；远端仓库归属、可见性和创建方式。

## 5. 契约路由与实施依赖建议

本审计文档自身 `contract-impact=none`，没有修改 wire/持久化/启动默认行为。FEAT-153 整体应至少按 `semantic` 评审其新增 local 服务身份、启动与权限边界；若发现任何受支持交互被拒绝或错误解释，应升级为 breaking，不提前假设 additive。依据：`yijie/docs/dev/contract-first.md:29`、`:37`。

| 变化 | 权威源 | 分类/验证要求 |
|---|---|---|
| 仓库清单与索引文档 | 元仓 repos.yaml/文档 | 无可观察运行边界变化时 none |
| 易界 workflow HTTP/IPC 共享 payload | yijie-contracts 源契约 | 新端点可独立 additive，但 local auth/默认语义纳入整体最高风险分类；source-first 和同源 conformance |
| API/Coze 本地身份、资源 scope、错误/审计 | Contracts + 新架构/安全决策 | 至少 semantic 审查，禁止临时手写 DTO 绕过 |
| 沿用的 Coze 上游协议 | 固定上游 IDL/源码及受审查适配记录 | 不能仅因来自第三方就把新增易界拥有的跨仓协议排除在 Contract First 之外；新增归一化协议仍入 Contracts |
| API 关联表、Coze 私有存储 | respective service migration/data compatibility | 明确旧/新数据兼容和回滚，不让独立服务直接读私有表 |
| opt-in profile、端口、probe、环境变量 | 服务仓与 yijie-infra | deployment interface，保留已有默认和正常退出语义 |

建议顺序：审计收口及仓库来源/远端决策 → local identity/editor/数据决策 → Contracts 源与安全生成 → API adapter 与 Coze 必要接入 → Infra 独立 profile/正常启停 → Desktop 列表/创建/保存/重开/运行/历史 → 一个 fresh local run 验证全部 Must AC。

这是用户要求的分步技术执行顺序，不自动建立 production_hardened 治理切片；应采用当前需求声明的交付 profile。具体电商节点、真实店铺、模型服务、平台凭据、定时任务和生产部署不进入基础闭环。

## 6. 尚未执行项目、原因和影响

| 项目 | 原因 | 影响 |
|---|---|---|
| Docker Desktop app launch、daemon ready | 只读审计范围 | 尚不能证明容器运行环境 ready |
| Coze dependencies/server/editor 启停 | 来源、拓扑、安全桥尚待设计；本次未启动 | 无健康、正常退出、编辑器可用和持久化重开证据 |
| API/Contracts 构建与生成 | 本次只读；已有 source pin 与 sibling HEAD 不同 | 无本次编译或生成符合性 PASS |
| 默认 Contracts skill archive fixture 路径 | 用户禁止危险归档/攻击性 fixture | 历史 archive 相关验证 NOT RUN；后续须采用安全路径并如实标记覆盖范围 |
| 强杀、权限破坏、binary 替换、攻击注入 | 用户长期硬性安全条款禁止 | 不执行、不作为验收通过条件，不伪造 PASS |
| 真实商家、多租户用户、外部模型、公开/生产调用 | 不属于本需求基础审计 | 本地合成闭环不能替代 DP 或 production_hardened |
| GitHub 远端创建、push/tag/release | 本文件只做边界审计，远端决策归主任务/Owner | 本地文件不代表仓库已在 GitHub 接入或发布 |

审计结论：仓库登记、文档整理和可审查设计可继续；实际运行必须在新服务身份/编辑器/数据边界收口并满足工具前置条件后按顺序完成。没有把现有安全组件、Docker 应用安装、Compose version 输出或静态脚本存在性写成 FEAT-153 真实集成已经完成。
