# FEAT-125 技术设计

## 1. 设计摘要

- 要解决的问题：为 Desktop 提供真实、租户隔离、可撤销、可追溯的权限投影，关闭
  FEAT-124 G4-001，而不把前端菜单过滤伪装成授权。
- 选择的方案：系统浏览器 OIDC Authorization Code + PKCE S256；Desktop 持有 IdP
  凭证，yijie-api 直接验证 API-audience RS256 access JWT，再通过
  `X-Yijie-Tenant-ID`、membership 和 PostgreSQL RBAC 计算
  `GET /v1/me/capabilities` 投影；Desktop 使用内存 fail-closed 状态机统一驱动导航与
  Router。
- 关键约束：ADR-0012 与 G1/G2/G2A 已批准；S1/S2 Contracts candidate/test/remote
  verification PASS；S3 API exact pin/migration/authn/identity/tenancy/RBAC
  `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`、S4 producer
  `360a526b679147472e7cc82ca7ac9db9d18a371d` 与 S5A Desktop native boundary
  `3798c67d260237928730758c7ec4c1fbe6fcf7d2` 均已远端核验且门禁/审查 PASS；Desktop
  exact contracts pin/generated store 已由 S5B 完成，UI 仍待 S6；tenant header 只作选择提示并逐请求验证；
  无普通前端持久化；provider first。
- 明确不做：角色/UI schema 下发、离线授权、Admin UI、Agent Host/Runtime、AI 变化、
  静默硬化既有 Tasks contract。

## 2. 组件职责与依赖方向

| Component/Repository | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| Identity Provider | 身份证明、授权码、API-audience access JWT 与 refresh 生命周期 | system-browser Code + PKCE S256 | RS256 JWT/rotating refresh | Yijie tenant/RBAC |
| `yijie-api/internal/platform/authn` | 严格验证 IdP access JWT，构造 Principal | `Authorization: Bearer` JWT | `Principal{issuer, subject, internal user}` | 角色与业务授权、API session 签发 |
| `identity` module | 外部 subject→内部 user、账号状态 | Principal claim | internal user | tenant role 决策 |
| `tenancy` module | 列出 membership 并验证租户选择 | user + `X-Yijie-Tenant-ID` | verified tenant scope | capability mapping、服务端 active session |
| `authorization` module | role/permission、Check、Projection | user+tenant+action/resource | allow/deny + capability set | UI 文案/排序 |
| Public HTTP adapter | contract validation/error/header | authenticated request | CapabilityProjection | 自己实现策略 |
| Contracts SDK | 生成 wire 类型 | OpenAPI source | Go/TS artifacts | domain logic |
| Desktop OIDC/credential adapter | 系统浏览器登录、PKCE、token refresh/logout、Keychain | login/logout intent | auth state；Rust 内部 credential state | tenant/RBAC、WebView 登录、token IPC |
| Desktop authenticated transport | 只执行 `listMyTenants`/`getMyCapabilities`，在 Rust 内附加 bearer | operation intent + optional tenant UUID | fixed status/headers/body envelope（无 token） | 任意 URL/method/header/body、通用 native proxy |
| Desktop permissions client | 使用生成 TypeScript 类型与固定 contract adapter 映射 transport 结果 | operation-scoped transport result + tenant selection | typed result/error | token 读取、nav decisions |
| Desktop permission store | context/epoch/expiry 状态机 | client result/auth/tenant events | current permission state | 持久化 token/capability |
| Desktop access policy | known capability→nav/route | ready set + availability | resolved entries/guard decision | 服务端授权 |
| Settings/recovery pages | 错误、retry、logout、tenant recovery | store state | user recovery intent | 敏感管理操作 |

```text
system browser OIDC Code + PKCE S256
  → IdP API-audience RS256 access JWT
  → Desktop Rust credential boundary
  → operation-scoped authenticated transport
    (fixed API HTTPS origin + two approved GET operations; bearer attached in Rust)
  → authn adapter
  → Principal
  → identity + tenancy
  → AuthorizationService.ProjectCapabilities
  → Public OpenAPI response
  → generated TypeScript types + fixed-contract adapter
  → PermissionStore(context, epoch)
  → access policy
  ├─ navigation
  └─ router guard

business request
  → AuthorizationService.Check(principal, tenant, resource, action)
  → repository scoped by tenant
```

business-request 分支是目标授权架构。现有 `/v1/tasks` 不由 FEAT-125 静默改造：默认
API profile 继续保留 legacy wire；本地 `feat-125-local-lab` 与未来获批宿主 profile 不注册
task handlers，并由对应 ingress 显式拒绝，直到 FEAT-126 完成 breaking auth/tenant
migration。

### 2.1 G3-NP-LOCAL 拓扑

```text
Desktop / system browser
  ├─ HTTPS https://localhost:8443
  │    → Caddy → Keycloak 26.7.0 → dedicated local PostgreSQL
  └─ HTTPS https://localhost:9443
       → Caddy → host-loopback yijie-api
            → dedicated yijie_api_feat125_local on 127.0.0.1:5432

OIDC callback
  → http://127.0.0.1:{ephemeral-port}/oauth/callback
  → one-shot Desktop Rust listener
```

- Keycloak、其 PostgreSQL 与 Caddy 只在显式 local profile 启动；镜像使用精确 tag+digest、
  healthcheck、命名 volume 和最小网络，published ports 只绑定 `127.0.0.1`。
- Caddy local CA data 使用持久 volume；只把公开 root certificate 导出到 ignored 本地目录，
  CA private key 不离开 volume。Node/Desktop 的显式 CA 路径已获批；API 的
  local-profile-only CA client 尚未获批，系统用户信任库安装也未获批。API 获批后必须用
  single PEM、owner-only file、大小限制与 lowercase SHA-256 pin 验证 TLS，禁止 insecure
  verifier。
- Keycloak realm import 只包含公开 client/mapper/policy 结构，不包含用户密码、admin secret
  或 token。Live validator 必须锁定 exact realm、两个 client、规范化后的 scope set、显式
  `userinfo.token.claim=false` 的 audience mapper 与 strict managed `data_classification` user
  profile；Keycloak 26.7 REST 中 omitted field 表示 unmanaged disabled。Provisioner 在任何
  mutation 前先只读核验 exact realm/clients、完整 two-user inventory 及 core/attribute state；
  若目标 profile 尚未存在，只允许 exact default profile + empty attributes 迁移，unexpected
  profile/attributes 必须在 PUT/password reset 前 fail closed。synthetic user/subject 与 2×2
  tenant/role 由受控本地 bootstrap 生成，且只能存在两名固定用户；HTTPS password resets
  与 admin refresh revocation 返回 `invalid_grant` 必须形成运行证据。
- API `feat-125-local-lab` bootstrap profile 在读取 manifest、检查 migration 或访问数据库前，
  锁死 exact local issuer、credentialed PostgreSQL URL（`127.0.0.1:5432`、database
  `yijie_api_feat125_local`、唯一 query `sslmode=disable`）和四份 tracked 2×2 manifest 的 subject/tenant/
  role/actor tuple。unknown profile、共享 DB、query/issuer/tuple 漂移均 fail closed；错误不回显
  DSN。空 profile 只保留 generic nonproduction 行为，不获得 local-lab 身份。
- Keycloak 将 `http://127.0.0.1/oauth/callback` 作为 native loopback redirect 基准；运行时只
  忽略 loopback port，path 仍精确匹配。online preflight 必须同时证明正确 path 接受、错误
  path 拒绝。
- Caddy 对 `/v1/tasks` 和其子路径拒绝；API `feat-125-local-lab` profile 同时不注册相应
  handlers；默认 profile 不受本地 profile 改动。
- Caddy 通过 Docker Desktop host gateway 访问宿主 `127.0.0.1:18080` 的可达性必须由真实
  `https://localhost:9443` preflight 证明；失败即 G3 FAIL，不得把 API bind 放宽到
  `0.0.0.0`、host network 或公网接口。

当前拓扑状态为 PASS。Keycloak/PostgreSQL/Caddy 容器已健康启动，
Infra 71/71 tests + lint/Compose/shell/diff PASS；live Keycloak 的 exact realm、two clients、
canonicalized scope sets、explicit `userinfo.token.claim=false` mapper、strict managed
`data_classification` user profile、two fixed users、password resets 与 refresh revocation
`invalid_grant` 已验证；profile migration 仅在全量 read-only checks 后对 exact default
profile + empty attributes 执行，profile/attribute drift 在 PUT/reset 前 fail closed。两名固定
合成用户已经固定 HTTPS 置密；API 专用 DB 已从 public tables=0 完成 migration 1→2，
bootstrap 前授权/Tasks 行数为 0，首次 4 次写入与第二轮 4 次幂等复跑、最终 inventory/
revision/audit 均 PASS；final offline ready 也已 PASS。
但 API 在 projection 开启时于 startup 同步获取 HTTPS JWKS，缺少获批 CA trust。
Online preflight 已执行，trusted discovery/JWKS 和 callback 正/负检查通过后在
历史首次 `API /healthz` 502 已关闭；最终 API readiness、两个未认证 `401` 和 Tasks
edge/direct `404` 全部 PASS。
G3 只覆盖 TLS、discovery/JWKS、API startup/readiness、bootstrap、未认证 `401` 与 Tasks
edge/direct `404`；完整浏览器、Rust bearer、refresh/Keychain E2E 仍属于 S7/G5。

## 3. 关键时序

### 登录与正常路径

1. Desktop 仅使用系统默认浏览器启动 Authorization Code flow；生成高熵 `state`、OIDC
   `nonce` 和 PKCE verifier，固定 `S256` challenge，回调必须是精确
   `http://127.0.0.1:{ephemeral-port}/oauth/callback`。禁止 WebView 登录、implicit flow、
   `localhost` 回调、plain PKCE 和 public-client secret。
2. Desktop 校验 callback state、ID token nonce 和 redirect ownership；PKCE verifier、ID token
   与 access token 只进内存，完成 nonce/identity 校验后不持久化 ID token；rotating refresh
   token 只进 macOS Keychain service `ai.yijie.desktop.auth`。
3. WebView 不读取 access token，只向 Rust 发送 `listMyTenants` 或
   `getMyCapabilities(tenant UUID)` operation intent。Rust 从 G3/G5 批准的固定 API HTTPS
   origin 选择预定义 GET path 并在内部附加 bearer；不接受任意 URL、method、header、body
   或通用代理 payload，IPC response 不含 token。
4. API 对 access JWT 固定验证：受配置 allowlist 的 HTTPS issuer、audience 精确等于
   `https://api.yijie.ai`、算法精确 `RS256`、signature、`exp`/`nbf`/`iat`（60 秒 skew）与
   JWKS `kid`；禁止 ID token 和动态 issuer/JWKS URL。identity 仅以 `(issuer, subject)`
   映射内部 user，不信任 email、display name 或 token role/capability。
5. Desktop 通过受限原生传输执行 `GET /v1/me/tenants`，再由固定契约生成的 TypeScript
   类型/adapter 消费当前 user 的活跃 tenant memberships：0 个进入
   无租户 recovery；1 个自动选择；多个必须由用户明确选择，不能隐式取第一项。v1 的
   tenant 选择只保存在进程内，不持久化 last tenant；应用重启后必须重新获取 memberships
   并重新自动选择或由用户选择。
6. 选择或切换 tenant 时，Store 暂停新业务请求、abort 旧请求、`epoch++`、清空旧
   capability/store/query cache，再把 tenant UUID 交给 `getMyCapabilities` 原生 operation；
   Rust 只在固定 request 上设置必需的 `X-Yijie-Tenant-ID`。
7. tenancy 把 header 视为不可信选择提示，逐请求验证 active user、active tenant 与 active
   membership；repository 查询继续显式带 tenant。
8. Authorization Service 在同一一致性读取中计算 allow-only、多角色 union、去重排序的
   capability，并返回当前 `authorization_revision` 与最长 5 分钟 `expires_at`。
9. API 按契约返回并设置 `Cache-Control: no-store`；固定 contract adapter 完成响应映射，
   Store 只接受 epoch、tenant、schema、revision 和 expiry 均有效的完整响应，然后进入
   ready。
10. Resolver 先权限后 availability；Router guard 与导航使用同一 policy。切换失败保持
   protected=0，不恢复旧 tenant Set；旧 tenant 的迟到响应必须丢弃。

### 失败、取消与恢复

1. 新 login/switch/logout 到达时，先 abort + epoch++ + clear；旧 response 无法提交。
2. access JWT 剩余不足 2 分钟时执行 single-flight refresh。401 或 refresh
   `invalid_grant` 时清 auth 状态、Keychain 和 projection，进入 signedOut；不得循环刷新。
3. 缺失/非法 tenant header 的 400，或 user/tenant/membership 拒绝的 403，清 context
   权限并进入 tenant recovery；本契约不使用 409。
4. 非预期 500、依赖不可用 503、network/timeout 进入 error，受保护入口为 0；retry 使用
   有上限退避。
5. malformed、unsupported schema、tenant mismatch 或 already expired 全量拒绝。
6. 当前 protected route 在刷新后失权时，先停止渲染，再进入 forbidden/recovery。

## 4. 状态模型

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 非法处理 |
|---|---|---|---|---|---|
| signedOut | oidcAuthenticated | JWT 与 identity mapping 合法 | selectingTenant/或 loading(context, epoch+1) | clear+fetch memberships | 非法保持 signedOut |
| selectingTenant | membershipsLoaded | 0 个 active tenant | contextError(noTenant) | protected=0、保留 recovery | 不默认 owner |
| selectingTenant | membershipsLoaded | 1 个 active tenant | loading(context, epoch+1) | 自动选择、clear+fetch | membership 变化→重新选择 |
| selectingTenant | membershipsLoaded | 多个 active tenant | tenantSelectionRequired | 等待明确用户选择 | 不隐式选择第一项 |
| tenantSelectionRequired | tenantSelected | target 在最新 membership set | loading(context, epoch+1) | abort+clear+fetch | 非法 target→contextError |
| loading | response200 | epoch/context/schema/expiry 全部匹配 | ready(context, revision, expiresAt, Set) | resolve routes/nav | 任一不匹配→error |
| loading | 401 | current epoch | signedOut | clear auth/Keychain/projection | 迟到→drop |
| loading | 400/403 | current epoch | contextError | clear projection | 迟到→drop |
| loading | timeout/network/500/503 | current epoch | error(retryable) | clear projection | 迟到→drop |
| ready | expires/foreground | 当前 auth + tenant | loading(epoch+1) | 先 clear 再 fetch | 无 stale-while-error |
| ready | tenantSwitch | target membership intent | loading(new context, epoch+1) | abort+clear | 不沿用 old Set |
| ready | capabilityRevoked response | valid snapshot | ready(new revision) 或 contextError | 当前 route re-evaluate | 禁止保持旧页面 |
| any | logout | current user intent | signedOut | 撤销 refresh、删除 Keychain、清内存/auth/tenant/projection | 重复 logout 幂等 |
| error/contextError | retry | auth/context 可恢复 | loading(epoch+1) | fetch | 无效 JWT→signedOut |

第一版禁止 stale permission fallback。HTTP `no-store` 不等于内存失效，故
`expires_at` 最大 5 分钟、foreground refresh 与 clear-before-fetch 均为 Must。

## 5. 领域模型与不变量

| Entity/Value | Owner/tenant scope | ID/幂等键 | 不变量 | 生命周期 |
|---|---|---|---|---|
| Principal | authn / global identity | internal user mapping | 只由验证后的 credential 产生 | 单请求 |
| TenantMembership | yijie-api / tenant+user | composite key | active user 只能使用 active membership | 状态化 |
| Role | yijie-api / tenant | role id + role_key | assignment tenant 与 role tenant 一致 | 可撤销 |
| Permission | yijie-api / catalog | immutable namespaced key | 已发布 key 不重用/改义 | 版本化 |
| RolePermission | yijie-api / role | role+permission | 去重，更新可审计 | 状态化 |
| MembershipRole | yijie-api / tenant+user | membership+role | FK 保证不跨 tenant | 状态化 |
| CapabilityProjection | current user+tenant | `authorization_revision` int64；wire 范围 `1..9007199254740991` | 原子、去重、限长、最长 5 分钟、无角色细节 | 短期 |
| PermissionState | Desktop process | context+epoch | 非 ready 无 protected allow | 进程内 |

已批准的 UI mapping：

| Desktop key | Required capability | Availability v1 |
|---|---|---|
| newTask | `task.create` | enabled → `/chat` |
| taskHistory | `task.read` | enabled → `/tasks` |
| store | `store.read` | disabled / 即将开放 |
| workspace | `workspace.use` | disabled / 即将开放 |
| scheduledTask | `schedule.read` | disabled / 即将开放 |
| plugin | `plugin.read` | disabled / 即将开放 |
| knowledge | `knowledge.read` | disabled / 即将开放 |
| settings | core/recovery，无页面级 capability | enabled → `/settings` |

已批准的 RBAC v1 使用 allow-only、deny-by-default 和多角色 capability union，不支持显式
deny、角色继承、ABAC 或用户直接 grant：

| Role | Capability set |
|---|---|
| `tenant_owner` | `task.create`、`task.read`、`store.read`、`workspace.use`、`schedule.read`、`plugin.read`、`knowledge.read` |
| `tenant_member` | `task.create`、`task.read` |

user、tenant 或 membership 任一为 `suspended` 时拒绝全部 tenant capability。Settings
core/recovery 不属于这 7 个 capability，不因 ready-empty/error 而消失。

`/` 在 permission ready 后按 chat→tasks→settings 选择首个允许入口。显式受保护深链
无权限时进入 forbidden，不静默跳到另一个业务页面。

## 6. 数据与 Migration 专项

- 是否涉及数据库/缓存/持久化：是，使用已批准的 PostgreSQL expand migration。
  PostgreSQL 是 RBAC 唯一事实源；第一版不引入 Redis 权限缓存，也不创建 API sessions
  表。
- 状态：schema/索引/FK/audit/roll-forward 方案已通过 G2；S3 migration v2 已实现，并在
  PostgreSQL 16.14 完成空路径、00001 existing data upgrade、append-only 与 expand-only 演练。

已批准最小模型：

- `users(id uuid PK, status active|suspended, created_at, updated_at)`；
- `user_identities(user_id, issuer, subject, created_at)`，`PRIMARY KEY (issuer, subject)`，
  `user_id` FK 到 users，并对 `user_id` 建索引；email/display name 不作身份键；
- `tenants(id uuid PK, name, status active|suspended, authorization_revision bigint NOT NULL
  DEFAULT 1 CHECK BETWEEN 1 AND 9007199254740991, created_at, updated_at)`；
- `tenant_memberships(tenant_id, user_id, status active|suspended, created_at, updated_at)`，
  `PRIMARY KEY (tenant_id, user_id)`，分别 FK 到 tenants/users，并建立
  `(user_id, status, tenant_id)` membership discovery 索引；
- `permissions(permission_key text PK, description)`，只登记批准的 7 个点号 key；
- `roles(id uuid PK, tenant_id, role_key, name, is_system)`，`UNIQUE (tenant_id, role_key)` 与
  `UNIQUE (tenant_id, id)`，tenant FK 到 tenants；
- `role_permissions(tenant_id, role_id, permission_key)`，PK 覆盖三列，复合 FK
  `(tenant_id, role_id)` 到 roles，permission FK 到 permissions，并对 `permission_key` 建反查索引；
- `membership_roles(tenant_id, user_id, role_id)`，PK 覆盖三列，复合 FK
  `(tenant_id, user_id)` 到 memberships、`(tenant_id, role_id)` 到 roles，数据库级阻止
  跨租户 assignment，并对 `(tenant_id, role_id)` 建反查索引；
- 不存在 `sessions`、direct user grant、deny、role inheritance 或 ABAC 表。

membership/tenant/status/role/permission 变更在同一事务中原子递增 tenant 的
`authorization_revision` 并写 append-only audit。revision 更新采用 tenant row 的原子
`UPDATE ... SET authorization_revision = authorization_revision + 1 ... RETURNING`，避免
lost update。全局 user status 变化必须递增其所有 membership tenants 的 revision。

| Phase | Schema/Data change | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | 新表、索引、复合约束；把 audit 从 task-only 扩展为通用 resource audit | 旧 API 忽略新表且旧 task audit 可读 | 新代码在 flag off 下启动 | empty DB + existing 00001 upgrade | 回退 app；保留 expand schema，不 destructive down |
| Bootstrap | 幂等运维命令建立合成/staging tenant+owner | 旧 app 无影响 | 新 auth 可解析 | 审计、重复执行、rollback test | revoke/bootstrap compensation |
| Switch | 开启 projection read path | 旧 Desktop 不调用 | 新 Desktop 读取 | 2×2 E2E、metrics | flag off |
| Contract | 第一版不删旧表/列 | 旧 app 继续可运行 | 新 app 正常 | 观察窗口 | 后续独立 migration |

当前 `audit_logs.resource_id` FK 指向 tasks。已批准 migration 解除 task-only resource FK，
保留 `resource_type`，让 `resource_id uuid` 对 UUID 资源可空并新增 `resource_key text` 承载
permission key，使用 CHECK 保证二者至少一个存在；保留 append-only trigger、既有 task
audit 可读性与现有索引，并为 `(tenant_id, resource_type, resource_id/resource_key)` 增加查找
索引；
bootstrap、membership/status/role/permission 变更与 audit 在同一事务，audit 失败则业务写
整体回滚。进入 Runner/数据库边界后的、被拒绝且没有业务写的授权 mutation 通过独立
append-only failure audit 记录；CLI 环境、issuer 或 manifest 的前置校验失败发生在 actor/
事务建立前，只返回脱敏稳定错误，不得误称已有审计行。不得为写失败审计而提交部分业务
状态。migration 不写真实 user/tenant；幂等
`bootstrap-nonprod-authz` 受控命令创建明确 manifest 中的
tenant、identity、`tenant_owner`/`tenant_member` assignment 和审计。显式
`feat-125-local-lab` profile 还必须在任何 DB 访问前锁死 exact local issuer、专用 loopback
database、唯一 query 与固定 tracked 2×2 tuple；generic nonproduction profile 不得被误报为
local-lab 证据。

现有 Tasks tenant/auth wire 不在本 semantic slice 修改：默认 API profile 保持既有
`/v1/tasks` handlers；本地 `feat-125-local-lab`/未来获批宿主 profile 不注册旧 handlers，
对应 ingress 同时显式拒绝该路径。双隔离例外在 FEAT-126 生产启用或 2026-09-30（取较早者）
到期；到期未完成不得开放 Tasks，必须重新审批。

## 7. 一致性与韧性

- 事务边界：membership/role/permission 变更与对应 append-only audit 同事务；只读
  projection 读取一个可解释的一致版本并返回 revision。
- 并发冲突：授权写原子递增 `authorization_revision`；需要 compare-and-swap 的管理写以
  expected revision 拒绝陈旧更新，不允许 lost update。
- 幂等：read projection 天然幂等；bootstrap 和 assignment mutation 必须有幂等键。
- 超时/取消：API request context 贯穿 DB；Desktop AbortController 取消旧请求。
- 重试/退避/上限：只对网络/503 GET 做有限指数退避+jitter；400/401/403 不自动风暴重试。
- 限流/熔断/降级：endpoint 按内部 user、tenant 和来源 IP 限流；故障降级为 deny，不读取
  跨用户缓存。
- 部分失败与补偿：不能返回部分 capability；写事务失败整体回滚。
- 资源释放：DB rows/transactions、HTTP body、timers、foreground listener 和 abort
  controller 均在完成/logout/unmount 时释放。

## 8. 安全设计

- 认证入口：Accepted operation-level Bearer；API 直接验证 IdP 签发、audience 精确为
  `https://api.yijie.ai` 的 RS256 access JWT，不接受 ID token 或 API opaque session。
- 资源级授权：共享 `AuthorizationService.Check`；projection 由相同 policy 计算。
- 租户隔离：`X-Yijie-Tenant-ID` 是不可信选择提示；active user/tenant/membership 每请求
  验证；repository 显式 tenant。
- 输入验证：endpoint 无 body/query；必需 tenant header 限长且为 UUID；capability output
  受 schema 限制。
- Secret/token 边界：PKCE verifier、ID token、access token 仅内存；refresh 仅 macOS
  Keychain `ai.yijie.desktop.auth`；public client 无 secret。access 为 10 分钟，剩余不足
  2 分钟 single-flight refresh；refresh idle 30 天、absolute 90 天、每次 rotation，reuse
  撤销 token family；logout 撤销 refresh、删除 Keychain 并清空 token/auth/tenant/projection；
  不进入 Git/env 前端包/日志。该 family 语义是最终要求；本地 Keycloak 只证明 rotation，
  `provider_limit_documented` 继续阻断 S7/G5。
- PII/日志脱敏：只记录内部 opaque IDs、revision、状态、latency；不记录 token/subject/集合。
- 高风险审批：授权写默认拒绝，bootstrap/assignment 走受控且可审计路径。
- 审计：授权变化成功与失败、actor、tenant、对象、diff、revision、request/trace。

## 9. 可观测性

| Signal | 名称/字段 | 成功基线 | 告警阈值 | Runbook 动作 |
|---|---|---:|---:|---|
| Metric | `permission_projection_requests_total{status}` | staging 建立 | 5xx/503 比例阈值在 G5 固定 | 停扩量、查 auth/DB |
| Metric | `permission_projection_duration_seconds` | staging p50/p95 | p95 candidate >300ms/5min | 查 query/index |
| Metric | `authorization_denials_total{reason}` | role matrix 建立 | 跨租户/invalid-context 突增 | 安全调查 |
| Metric | `permission_context_mismatch_total` | 0 | >0 | 停止 Desktop 灰度 |
| Log/Trace | request_id、trace_id、user_id、tenant_id、revision、status | 100% 有脱敏关联 | 缺失率 >0 | 修复观测 |
| Audit | membership/role/permission mutation | 每次写 1 条或事务回滚 | 漏审计 >0 | 阻断写入口 |

日志和 metric label 不包含 token、外部 subject 或完整 capability，避免高基数与泄漏。

## 10. 性能、容量与成本

| 项目 | 基线 | 目标/上限 | 测试方法 | 降级 |
|---|---:|---:|---|---|
| projection p95 | 未建立 | ≤300ms @ 50 RPS/staging | k6/Go benchmark after G2A implementation | deny + retry |
| capability 数量 | 0 | ≤256/user/tenant | contract/property test | 500/error，不截断 |
| DB round trips | 未建立 | 受控且无 N+1 | query trace/EXPLAIN | flag off |
| Desktop refresh | 无 | ≤1 active request/context | fake clock/concurrency test | cancel old |
| snapshot age | 无 | server `expires_at` ≤5min | clock-controlled test | clear+refresh |

性能数字已作为 G2 测试目标批准；只有实现并建立 staging baseline 后才能在 G5 判定 PASS。

## 11. 配置、Feature Flag 与部署

- API flag：S4 已固定 `YIJIE_API_PERMISSION_PROJECTION_ENABLED`，默认 `false` 时不注册新
  endpoint；显式开启才要求 issuer/JWKS 配置。本候选没有生产值、Desktop consumer 或激活；具体 IdP issuer/client
  ID、JWKS discovery、API/redirect origin、TLS 与 secret 配置的本地值由 A7 固定；生产值仍是
  G5 blocker。本地 API 仅在 `feat-125-local-lab` 使用严格显式 CA PEM + lowercase pin；
  default/production/disabled projection fail closed，系统 Keychain 未修改。
- Desktop native auth flag：S5A 已固定 `YIJIE_DESKTOP_NATIVE_AUTH_ENABLED`，默认 false；
  S6 已固定 `VITE_YIJIE_AUTHORITATIVE_PERMISSION_UI_ENABLED`，仅精确 `true` 启用，默认 false；
  S5B authoritative permission consumer/store 已由 S6 接入 UI。任何 flag 都不能
  提供“静态显示全部”的 fallback。
- 默认值：off。
- 安全关闭行为：API endpoint 不启用；Desktop protected entries 为 0，仅保留 login/core
  recovery，不复用旧 projection。
- 配置验证：issuer 必须是固定 allowlist HTTPS URL；audience 固定
  `https://api.yijie.ai`；RS256/JWKS/API origin/TTL 在启动时 fail-fast；public client 无
  secret，任何生产 secret 不进入前端。
- 新旧版本共存窗口：API provider 必须覆盖所有已发布 FEAT-125 Desktop；不能先回滚 endpoint。
- CSP/外部 URL：只有批准的 HTTPS API/IdP origin；普通 fetch 不新增 Tauri command。
- G3-NP-LOCAL local identity origin：`https://localhost:8443/realms/yijie-local`；local API
  origin：`https://localhost:9443/`。这两个值仅属于 ignored local runtime config，不能作为
  production default。
- Desktop local CA：只有显式 local-integration mode 且两个 origin 都为 `localhost` 时才
  接受；CA 文件需 regular/no-symlink、权限/大小与 SHA-256 pin 验证，并同时注入 OIDC 与
  operation transport client。生产/普通 native-auth 模式继续只使用默认 WebPKI roots。
- Keychain envelope：schema version + issuer + client ID + environment + token lifecycle；旧版
  或绑定不匹配时删除并重新登录，禁止跨环境 refresh。
- 本机于 2026-08-01 检查为 `0 valid identities` 且没有 provisioning profiles；因此
  G3-NP-LOCAL 在修复 CA blocker 后只验证 TLS/OIDC/API readiness；Protected Data Keychain
  的正式签名 App、完整浏览器/refresh/Rust bearer smoke 必须保持 S7/G5 `NOT RUN`，不伪造
  为本地 G3 PASS。
- 本地回滚必须停止独占 `127.0.0.1:18080` 宿主 API 进程、清除其
  `YIJIE_API_SERVICE_PROFILE=feat-125-local-lab` 与本地 issuer/JWKS 环境，关闭 local Compose
  profile，并恢复 Desktop local flags/凭证；不得把 default API profile 当作回滚目标启动，
  也不得停止或修改用户其它宿主 API 进程。

## 12. AI 功能专项

- 是否改变 prompt/model/retrieval/tool schema：否。
- 固定版本、结构化输出、拒答、提示注入、Eval：N/A；本需求是身份/RBAC/HTTP/UI 状态，
  不调用模型或工具。

## 13. 方案比较

| 方案 | 优点 | 缺点 | 风险 | 结论 |
|---|---|---|---|---|
| A：Desktop 硬编码 role/menu | 快 | 无法撤销、易伪造、跨租户泄漏 | critical | 拒绝 |
| B：JWT 内直接放完整 capability | 读取快 | stale、token 膨胀、策略泄漏、撤销复杂 | high | 非首选 |
| C：新建独立 policy microservice | 边界独立 | 当前规模过度、增加网络与运维面 | high | 暂不采用 |
| D：yijie-api 模块化 authorization + projection | 符合权威边界、可复用、可审计 | 需要 auth/RBAC/migration 基础 | manageable | 推荐 |
| E：服务端下发完整菜单 schema | UI 灵活 | 把产品布局耦合授权，客户端兼容复杂 | medium-high | 拒绝 |

## 14. ADR 与批准

- ADR：Accepted
  `yijie/docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md`。
- 技术负责人：段成威。
- 安全/数据 Owner：段成威。
- 结论与日期：三路只读设计审核于 2026-07-31 完成；段成威已批准 A1—A7，ADR
  Accepted，G1/G2/G2A Passed，S1—S4 contract/API 与 S5A Desktop native boundary 均已
  commit/test/review/remote verified。S5B generated consumer/store 也已在 Desktop
  `f94ac343881b0f7df59c0f5f4169372e612fd019` 完成并远端核验；S6 UI final
  `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` 已远端核验；S7 已执行到真实 IdP/Keychain
  blocker 并按 Local Engineering Baseline Complete 冻结。安全收口已远端核验为 Desktop
  `155854cf3662384caa2c8bffe0a47935ef4a70b5` 与 Infra
  `f040492e7c4af4aa7cc94a343140c58befae3af2`，但尚未形成生产 PASS 证据。G3 local IdP/client/JWKS/API origin 已固定，local stack/offline ready/HTTPS synthetic
  user provisioning、API bootstrap 与 core online PASS。G3 与 S5B PASS，feature 继续关闭。
  生产 IdP、域名/TLS、Secret Manager、Apple 签名与 ingress 配置保持 G5 Blocked；真实部署前
  必须恢复完整生产级身份安全链路和 S7/G4/G5/G6。

## 15. 本地白名单登录附录（EXC-125-003）

该附录只定义本地 Desktop 私有登录入口，`contract-impact = semantic`，原因是新增了携带一次性
本地凭据的私有 Tauri IPC 和本地 deployment flags；Public OpenAPI、API handler、JWT verifier、
PostgreSQL schema 和 Agent Host wire 均为 N/A/未改变。

```text
Settings 空白账号/密码表单
  -> native_auth_local_whitelist_login(request)
  -> Rust local + local-integration + exact-true gates
  -> username/password SHA-256 fingerprint match
  -> owner-only ignored FEAT-125 synthetic secret authority
  -> existing synthetic Authorization Code + PKCE client
  -> existing install_issued_tokens / refresh / logout
  -> existing tenants + capabilities + Chat authorization
```

前端 `VITE_YIJIE_LOCAL_WHITELIST_LOGIN_ENABLED` 与 `VITE_YIJIE_ENV=local` 只决定第一步是否
显示表单；它们不替代 Rust runtime gate。表单隐藏时，原有系统浏览器登录按钮仍可用。

不变量：

- 前端开关 `VITE_YIJIE_LOCAL_WHITELIST_LOGIN_ENABLED` 默认关闭且只在
  `VITE_YIJIE_ENV=local` 时显示表单；它不是 native 安全边界。Rust 开关
  `YIJIE_DESKTOP_LOCAL_WHITELIST_LOGIN_ENABLED` 默认关闭且只接受精确 `true`；Rust 另要求
  `YIJIE_ENV=local` 与 `YIJIE_DESKTOP_AUTH_ENVIRONMENT=local-integration`。
- `YIJIE_DESKTOP_LOCAL_WHITELIST_IDP_SECRETS_PATH` 必须为 absolute、owner-owned、regular
  non-symlink、`0400/0600` 文件，并包含精确四项 FEAT-125 local secret inventory；production
  或部分配置直接使 native auth runtime invalid。
- tracked code 只保存 Owner 指定账号和密码各自的 SHA-256 指纹；原文不进入源码、文档、
  fixture、日志或初始 DOM。Tauri request 拒绝未知字段并在 drop 时 zeroize。
- 白名单匹配只选择既有 synthetic user A；它不生成 Principal、capability 或 API session。
  API 仍从标准 bearer `(issuer, subject)` 映射 user，并逐请求验证 tenant/membership/RBAC。
- 回滚关闭两个白名单开关并重启 Desktop；标准系统浏览器 `native_auth_login` 始终保留且未修改。
