# FEAT-125 现状扫描与影响评估

## 1. 调查基线

| Repository | Rules read | Branch | Full HEAD SHA | Worktree | Toolchain |
|---|---|---|---|---|---|
| yijie | AGENTS、project memory、contract-first、Feature handbook | develop | `ef0f50e41128c44ea91bf2e581e1fecf14c7b95c` | clean / remote equal | Markdown/Bash |
| yijie-contracts | AGENTS、README、SECURITY、CONTRIBUTING、contract/version policies | develop | `5320c302f5c00f4080e9c3662a3f21cc1c4b813e` | clean / remote equal | Node 24–26、pnpm 11、Go |
| yijie-api | AGENTS、README、SECURITY、CONTRIBUTING、architecture/API/DB docs | develop | `2834b412ad565651215bd12458276c4e0d8fecf5` | clean / remote equal | Go 1.26.5、PostgreSQL 16 |
| yijie-desktop | AGENTS、README、SECURITY、CONTRIBUTING、design navigation rule | develop | `be01cc2d0a1c9c4b057de616be201a4843d0a035` | clean / remote equal | Vue 3、Tauri 2、pnpm 11 |
| yijie-infra | AGENTS、README、SECURITY、CONTRIBUTING、environment/deployment/rollback docs | develop | `47c9e826d1f860d872958b05bafa44b1c3232f62` | clean / remote equal before G3 preparation | Node 26、pnpm 11、Docker Compose |

## 2. 初始已验证行为（2026-07-31）

| 事实 | 文件/符号/行号或命令 | 结果 | 事实/推断 |
|---|---|---|---|
| Public API 显式无认证 | `yijie-contracts/openapi/public/public.yaml:8` | 全局 `security: []` | Fact |
| Public API 没有 identity/capability operation | 同一 OpenAPI paths/components 扫描 | 只有 System 与 Tasks | Fact |
| Tasks 创建信任客户端 `tenant_id` | `public.yaml#CreateTaskRequest`、API handler | 不能作为可信租户来源 | Fact |
| API 没有 auth middleware | `internal/app/app.go#NewHandler` | 路由直接挂到 ServeMux | Fact |
| DB 没有用户/租户/RBAC/session | `00001_create_tasks_and_audit_logs.sql` | 只有 tasks 与 append-only audit_logs | Fact |
| Task Get 未显式带租户 | `tasks/infrastructure/postgres/repository.go#Get` | 只按 task id 查询 | Fact |
| API 生成使用浮动 sibling | `yijie-api/Makefile#generate` | 无 tag/SHA/digest lock 或 drift CI | Fact |
| Desktop client 是本地 placeholder | `src/api/client.ts` | 没有真实网络 I/O | Fact |
| Desktop generate 是占位 | `package.json#scripts.generate` | 输出 No generated assets yet | Fact |
| App Shell 缺生产权限输入 | `src/App.vue`、`YjAppShell.vue` | 默认投影 `{}` | Fact |
| 缺省 visibility 会显示条目 | `src/navigation/app-nav.ts#resolveAppNavigation` | 只有显式 false 才隐藏 | Fact |
| Router 无授权 guard | `src/router/index.ts` | `/` 无条件跳 `/chat` | Fact |
| LocalStorage 仅有 sidebar 偏好 | sidebar preference/store | 不得混入权限或凭证 | Fact |
| supported contracts baseline 可远端解析 | `git ls-remote` | v0.2.0→`f16a497...` | Fact |
| FEAT-124 G4 被 G4-001 阻断 | FEAT-124 verification report | 必须保持阻断 | Fact |

### 2.1 已完成切片后的事实（2026-08-01）

| 事实 | 不可变证据 | 结果 | 剩余边界 |
|---|---|---|---|
| S4 API producer 已远端可用 | `yijie-api@360a526b679147472e7cc82ca7ac9db9d18a371d`，`origin/develop` 相等 | tenants/capabilities、逐请求 tenant 验证、稳定错误、revision、metrics 与 producer/fault conformance PASS；flag 默认 false | staging/performance/exporter、生产配置与激活未执行 |
| S5A/S5B Desktop boundary 与 consumer 已远端可用 | S5A `3798c67d260237928730758c7ec4c1fbe6fcf7d2`；S5B final `f94ac343881b0f7df59c0f5f4169372e612fd019`；`origin/develop` 已核验 | system-browser OIDC、operation-scoped transport、exact generated types/adapter、0/1/多租户状态与内存 fail-closed store 全部门禁 PASS；flag 关闭 | S6 UI、真实 IdP/API/正式 Keychain provisioning 未执行 |
| G3 通用准备层已远端可用 | `yijie-infra@2f01f22b46f313f8ff0b9973e417f7ccae654318`；`yijie@9c732e0a8f8c7eb9d31d371300225ea105018879` | strict template/ready validator、bounded online preflight、runbook 与本地 flag-off baseline 已提交并推送 | A7 已把外部资源前置替换为 G3-NP-LOCAL；历史首次 online 的 API health 502 已由 local-only 显式 CA pin 修复关闭 |
| G3-NP-LOCAL 已提交基线 | API `faeb78019d...`、Desktop `446b4d6085...`、Infra `298192e386...`；三个 `origin/develop` 完整 SHA 已核验 | API/Desktop/Infra 最终门禁 PASS；Keycloak/PostgreSQL/Caddy、专用 DB/2×2 bootstrap、offline ready PASS；API 仅 local profile 使用严格显式 CA PEM+SHA-256 pin且未改系统 Keychain；core online 的 discovery/JWKS/callback、health/ready、两个 401、Tasks edge/direct 404 全部 PASS | G3 PASS；随后 S5B 已单独批准并以 Desktop `f94ac34...` 完成；signed app/Keychain/full auth E2E 与生产配置仍 NOT RUN |

## 3. 仓库与组件影响矩阵

| Repository/Component | 职责 | 影响 | 原因 | Owner | 预计改动 |
|---|---|---|---|---|---|
| yijie | 跨仓治理 | direct | Feature、ADR、门禁、FEAT-124 linkage | 段成威 | docs/features、必要 ADR |
| yijie-contracts / Public OpenAPI | wire authority | direct | 新 security scheme、两个 operations、schemas、SDK | 段成威 | `openapi/public`、生成物、测试、release docs |
| yijie-api / authn | 凭证验证 | direct | 生成可信 Principal | 段成威 | 新 platform adapter/middleware |
| yijie-api / identity+tenancy+authorization | 业务权威 | direct | membership、RBAC、projection、audit | 段成威 | modules、migration、tests |
| yijie-desktop / native auth+transport | OIDC public client、凭证保管与受限 authenticated transport | direct | system-browser PKCE、loopback、Keychain、logout；token 不跨 IPC 时由 Rust 仅执行两个固定 GET operations | 段成威 | Rust/Tauri modules、固定 API origin/method/path allowlist、最小 capability、tests |
| yijie-desktop / API+store | contract consumer | direct | exact pin、生成类型/adapter、fail-closed state | 段成威 | api/domain/store/tests；禁止通用 native proxy |
| yijie-desktop / navigation+router | 呈现与 UX guard | direct | deny-by-default、深链与恢复 | 段成威 | nav/router/AppShell/pages/tests |
| yijie-infra | local/nonproduction dependencies | direct for G3-NP-LOCAL | 固定本地 Keycloak、专用 PostgreSQL、Caddy HTTPS、loopback ports、合成数据与 offline/online preflight；生产资源继续 N/A/deferred | 段成威 | local-lab Compose profile、realm/Caddy public config、validator/preflight/runbook；不创建生产或云资源 |
| yijie-admin-web | RBAC 管理 UI | none for first slice | 首版只允许受控 bootstrap，不做管理 UI | 段成威 | N/A |
| yijie-agent-host | local Runtime boundary | none | 不消费平台身份；继续固定 contracts-v0.2.0 | Agent Runtime Owner | N/A |
| yijie-codex/Runtime | Runtime source | none | 无 Runtime/AI 协议变化 | Runtime Owner | N/A |

## 4. 调用链与数据流

```text
approved local or production IdP → direct RS256 JWT
  → Desktop Rust credential boundary
  → operation-scoped authenticated transport
    (fixed API HTTPS origin + listMyTenants/getMyCapabilities; bearer attached in Rust)
  → yijie-api issuer/audience/RS256/JWKS authentication adapter
  → Principal(user identity)
  → GET /v1/me/tenants (active memberships only; no tenant header)
  → Desktop handles 0/1/multiple tenant selection
  + required X-Yijie-Tenant-ID (untrusted tenant-selection hint)
  → tenancy membership/status validation
  → Authorization Service + PostgreSQL RBAC
  → GET /v1/me/capabilities
  → generated Desktop types + fixed-contract adapter
  → in-memory Permission Store
  → deny-by-default navigation + route policy

tampered Desktop / direct API call
  → yijie-api authenticates and authorizes again
  → allow or deny independently of UI
```

| 边界 | 方向 | 权威源 | Producer | Consumers | 失败传播 |
|---|---|---|---|---|---|
| IdP JWT→Principal | request | 已批准的 direct IdP RS256 JWT ADR + issuer/JWKS 配置 | external IdP + yijie-api | authorization module | 401 / fail-closed |
| Rust credential→Public API | request | ADR-0012 的 token/IPC 边界与 Public OpenAPI operation | Desktop Rust operation-scoped transport | `listMyTenants`/`getMyCapabilities` only | 非 allowlisted origin/method/path/header/operation 拒绝；token 不跨 IPC |
| Active tenant memberships HTTP | response | Public OpenAPI `listMyTenants` | yijie-api | yijie-desktop | 0/1/多租户列表；401/403/500/503 |
| Principal + `X-Yijie-Tenant-ID`→租户上下文 | request | PostgreSQL membership/status；header 仅是不可信选择提示 | tenancy module | authorization | 缺失/非法 400；membership/status 拒绝 403 |
| Capability HTTP | response | Public OpenAPI | yijie-api | yijie-desktop | 400/401/403/500/503 |
| RBAC data | DB read/write | yijie-api migration/domain | authorization module | projection + business checks | transaction rollback/503 |
| Capability→UI | process-local | Desktop mapping policy | Permission Store | nav/router | error/recovery state |

### 4.1 G3-NP-LOCAL 本地拓扑

```text
system browser / Desktop Rust
  → https://localhost:8443 → Caddy → Keycloak → dedicated PostgreSQL
  → https://localhost:9443 → Caddy → host-loopback yijie-api
      → dedicated API DB yijie_api_feat125_local on 127.0.0.1:5432

OIDC callback remains http://127.0.0.1:{ephemeral-port}/oauth/callback
```

两个 HTTPS 入口使用同一持久化本地 CA；preflight 与 Desktop 必须显式加载并校验该 CA，
不能关闭证书或 hostname 校验。只有 `feat-125-local-lab` API service profile 不注册 legacy
Tasks handlers，默认 profile 的 legacy wire 保持不变；Caddy 再拒绝本地 Tasks 路径。本地
环境只处理 synthetic identities/tenants，不改变固定 API audience。`feat-125-local-lab`
bootstrap profile 在读取 manifest、检查 migration 或访问数据库之前，必须同时验证 exact
issuer、专用 loopback DB 结构和四份 tracked manifest 的固定 subject/tenant/role/actor tuple；
unknown profile 或任一漂移 fail closed，且错误不得回显 DSN。

该拓扑已形成部分运行时证据：Keycloak/PostgreSQL/Caddy 容器健康；live Keycloak 已证明
exact realm、两个 clients、canonicalized scope sets、显式 `userinfo.token.claim=false` 的
audience mapper、strict managed `data_classification` user profile（Keycloak 26.7 REST 中
omitted field = unmanaged disabled）、两名固定合成用户、password resets 与 refresh
revocation `invalid_grant`。两名用户已经固定 HTTPS 置密；API 专用 DB 已证明空库起步、migration 1→2、bootstrap 前零业务行，
最终仅含固定 2×2 合成授权矩阵且 tasks=0；公开 CA 已导出并通过 offline ready 严格校验。
API 已仅在 `feat-125-local-lab` 使用绝对 CA PEM 路径、lowercase SHA-256 pin 与隔离的
proxy-free/no-redirect TLS client；default/production/disabled projection 对这些变量 fail closed，
没有安装系统信任。最终 startup/readiness 与 core online preflight PASS；禁止将该部署信任
接口扩展到生产或解释为公共 wire/contracts 变更。

## 5. Contract Impact

- 分类：`semantic`。
- 选择最高风险分类的理由：结构上是新增 operation，但这是 Public API 首次建立用户身份、
  活动租户和授权语义；认证/权限变化按仓库政策必须做 semantic/security 人工评审。
- 是否存在公开未知消费者：Public API 理论上存在 `unknown-public`；新 operation 无旧调用方，
  但整个 SDK bundle 的 Agent Host consumer 必须证明其既有投影不变。
- 请求方向兼容：两个新 GET 不修改现有 operation；只在新 operations 上声明认证。
- 响应方向兼容：capability 使用七个已批准的开放点号字符串，旧 Desktop 忽略未知值；
  新增 key provider-first。Settings core 无 capability，始终保留恢复、重试和退出入口。
- 支持基线：`contracts-v0.2.0` /
  `f16a497e1377f45747f8ff9292b4b60cf2027f88`。
- 重分类停止条件：若给既有 Tasks operation 增加强制认证、移除/改义 request
  `tenant_id` 或改变既有错误，则至少 semantic，匿名 consumer 失效时为 breaking。
- A6 临时例外：现有 Tasks wire 暂不硬化，但生产必须 ingress + handler 双隔离并由
  FEAT-126 补偿。例外在 FEAT-126 生产启用或 `2026-09-30` 中较早者到期；到期仍未完成
  时不得开放 Tasks，必须保持隔离并由段成威重新审批。

## 6. 数据与 Migration 影响

| 存储/Schema | Owner | 变化 | 旧数据影响 | 新旧 Reader/Writer | 回填/回滚 |
|---|---|---|---|---|---|
| users | yijie-api | expand candidate | 无现有用户表 | 旧 API 忽略；新 identity 读取内部 user/status | 空表先部署；不写真实用户 |
| user_identities | yijie-api | expand candidate | 无外部 identity mapping | 新 authn 用 `(issuer, subject)` 映射 user | 与 users 分表；不把 email/display name 当真相 |
| tenants/memberships | yijie-api | expand candidate | 现有 tasks tenant_id 无 FK | 新 tenancy 读取 active/suspended 与 `authorization_revision` | synthetic bootstrap candidate 已验证；生产 bootstrap 与历史 task 归属另审 |
| roles/permissions/assignments | yijie-api | expand candidate | 无旧数据 | 新 authorization 读取 | 可禁用新 endpoint；保留 expand 表 |
| API session table | yijie-api | none / prohibited in this feature | direct IdP RS256 JWT 不需要本地 API session | yijie-api 只验证 IdP JWT，不签发或持久化 API session | N/A；不得创建 session 表 |
| audit_logs | yijie-api | semantic expand in migration v2 | 00001 resource_id FK 仅指 tasks；旧 rows 保留 | v2 支持授权资源标识并保持 append-only；G3 bootstrap 已写 success audits | app rollback 保留 expand schema/audit；禁止 destructive down |
| Desktop memory | yijie-desktop | ephemeral state | 无旧权限状态 | 新进程内 store | logout/restart 即清空 |

G1/G2 已于 2026-07-31 批准 A1—A6。具体 migration 字段、索引、FK、保留期和 down
语义必须符合这些决策，并在 G2A/S3 形成后复核。数据库只走 expand-first；migration
不包含真实用户、租户、角色分配或 API session 表。

## 7. 安全与隐私影响

- 认证：已批准 Desktop 直接从外部 IdP 取得 RS256 JWT；API 必须严格验证
  issuer、固定 audience `https://api.yijie.ai`、RS256 signature、`exp`/`nbf`、`kid` 与
  JWKS rotation，不接受本地
  session、cookie 或自签 opaque bearer 代替。
- 资源级授权：Authorization Service 是唯一 policy implementation；projection 只读，
  不成为授权凭证。
- 租户隔离：required `X-Yijie-Tenant-ID` 只是客户端的不可信选择提示；API 必须以 JWT
  Principal 验证 membership/status，repository 查询必须显式带验证后的 tenant。
- 数据分类与脱敏：identity mapping、membership、roles、capabilities 为 Confidential；
  token/secret 为 Restricted。
- Secret/token：access token 只在内存；refresh credential 仅在获批的 OS 安全存储；
  不进入前端持久化、URL 或日志。IdP access JWT 最大有效期为 10 分钟；refresh 撤销或
  重用检测在下一次 refresh 时失败，不承诺即时撤销已签发 JWT；内部 user/membership
  suspension 由 API 实时返回 403。
- Provider limitation：本地 Keycloak 配置证明 rotation，但未证明 reuse 自动撤销整个 token
  family；完整 A2 生命周期证据必须留在 S7/G5，本地 G3 不得宣称通过。
- 原生传输：Rust 只接受 `listMyTenants` 与 `getMyCapabilities` 两个 operation intent 以及
  后者所需的 tenant UUID，并使用固定的已批准 API HTTPS origin、GET method 和 path；
  WebView 不能提交任意 URL/method/header/body，IPC 不返回 token，不建立通用代理。
- 高风险审批：membership/role/permission/bootstrap 写操作默认拒绝，需可审计运维路径。
- 审计字段：内部 actor/user、tenant、action、resource、result、request/trace、
  `authorization_revision`；
  不记 token 或外部 subject 原文。
- 输入/文件/URL 风险：endpoint 无业务输入；IdP/JWKS URL 与 redirect URI 必须固定 allowlist。

## 8. Runtime、模型与第三方影响

| 依赖 | 固定版本/完整 SHA | 能力是否已验证 | 费用/限流 | Sandbox | Fallback |
|---|---|---|---|---|---|
| Identity provider | local engineering provider fixed to pinned Keycloak under A7；production provider remains open；audience fixed `https://api.yijie.ai` | G3-NP-LOCAL live realm/offline ready/core online PASS；family reuse limitation 留在 S7/G5 | 本地无外部费用 | synthetic realm | auth unavailable→deny |
| PostgreSQL | 16 / yijie-api S4 candidate | local migration/RBAC 2×2 integration PASS；staging/performance 未验证 | 需容量测试 | 临时 schema integration | endpoint disable |
| Contracts generator | openapi-typescript 7.13.0；oapi-codegen 2.7.2 | 当前生成链存在 | N/A | repo CI | pin candidate |
| Tauri network/CSP | Tauri 2 / Desktop `3798c67d...` | S5A operation-scoped transport/config/redirect/IPC 本地矩阵 PASS；生产 API origin/CSP 未验证 | N/A | local/staging | native flag off；不新增普通 fetch command 或通用 native proxy |
| Codex Runtime/AI | N/A | 不受影响 | N/A | N/A | N/A |

## 9. 现有测试、构建与发布入口

| 目的 | 真实命令/配置来源 | 作用范围 | 已知限制 |
|---|---|---|---|
| Contracts generate/lint/test/build | `make generate/lint/test/build` | 源、SDK、schema | CI breaking 仅 origin/main |
| Contracts baseline check | `./scripts/check-breaking.sh <full SHA>` | OpenAPI/AsyncAPI/JSON Schema | 必须显式用 v0.2.0 full SHA |
| API unit/lint | `make lint && make test` | Go/race/coverage | S3/S4 auth/RBAC/endpoint/fault/metrics PASS；staging 不在该命令内 |
| API PostgreSQL integration | `make test-integration` / `make test-all` | 临时 schema/migration | S3/S4 migration、复合 FK、2×2 RBAC projection PASS；G3 synthetic bootstrap 首次/幂等/audit/revision PASS；staging 待 S7 |
| API generate | `make generate-check` | Go OpenAPI types | exact `9ec34abd...` + oapi-codegen v2.7.2 drift check PASS |
| Desktop quality | `make lint && make test && make build` | Vue/TS/Rust | S5A—S6 remote PASS；S6 18 files/113 frontend + 36 Rust tests、browser、docs、debug Tauri 与 audits PASS；final `688fb72ddf...` |
| Desktop docs/native | `pnpm docs:build`、`pnpm tauri:build --debug`、cargo/npm/license audit | design/native | S5A 本地 `.app/.dmg` 与审计 PASS；真实 API origin/CSP、签名/公证未定 |
| Feature package | `check-feature-package.sh` | 文档结构 | 不替代人工批准 |

## 10. 初步交付顺序

### 合并顺序

1. yijie：登记已批准的 A1—A6，固化安全 ADR、需求、风险、测试与实施计划。
2. yijie-contracts：0.3.0 candidate 源、生成物、测试和发布说明。
3. yijie-api：固定 candidate，完成 expand migration、authn/RBAC/projection。
4. yijie-desktop：固定同一 candidate，完成 client/store/nav/router。
5. yijie：登记集成证据、tag provenance、FEAT-124 G4 复审。

### 部署顺序

1. 非生产 migration expand。
2. 非生产 yijie-api provider，feature flag 默认关闭。
3. Candidate API/Desktop conformance 与真实 auth 测试。
4. tag 必须指向相同 candidate；两端验证 digest 后，API provider first。
5. Desktop consumer 灰度；不能先发依赖新 endpoint 的 Desktop。

### 功能启用顺序

1. 内部测试 tenant。
2. 两角色×两租户 canary。
3. 观测 400/401/403/503、延迟、stale/跨租户拒绝。
4. 扩量后才回到 FEAT-124 关闭 G4-001。

## 11. 阻塞项与 Spike

| ID | 未知项 | 允许的只读/隔离验证 | 禁止副作用 | Owner | 结论 |
|---|---|---|---|---|---|
| SPIKE-001 | direct IdP RS256 JWT 与 Desktop login flow | G3 只验证固定本地 Keycloak metadata、issuer/client/JWKS 与 API startup/readiness；完整 Tauri login/refresh/Keychain 属于 S7/G5 | 不注册生产应用、不写 secret | 段成威 | A1/A2/A7 Approved；live realm/offline ready/core online PASS；本地 family reuse 未证明；production provider 仍待 G5 |
| SPIKE-002 | required `X-Yijie-Tenant-ID` 与 membership/status 验证 | 用合成状态图/测试替身验证 missing/invalid/denied | 不把 request tenant 当授权事实 | 段成威 | A3 Approved；S4 header/endpoint、原子 projection 与 400/403 负测 PASS；跨仓 E2E 待 S7 |
| SPIKE-003 | RBAC schema 与 bootstrap | 临时 schema migration rehearsal | 不写真实用户/租户，不建 API session 表 | 段成威 | A4 Approved；G3 local DB migration 2 与可审计幂等 synthetic bootstrap candidate PASS；生产 bootstrap 仍待 G5 |
| SPIKE-004 | 现有 Tasks API production disposition | 验证本地 `feat-125-local-lab` profile + Caddy 双隔离并创建 FEAT-126 | 不静默改 Tasks wire contract 或默认 API profile | 段成威 | A6 Approved；local runtime direct+edge 404 PASS；未来生产宿主 API profile/ingress 方案待 G5 |
| SPIKE-005 | API origin/CSP/Keychain | local 配置验证 | 不新增生产 URL/capability | 段成威 | A7 固定 `localhost` HTTPS、本地 CA 显式注入与环境绑定；本机当前无有效 code-sign identity/provisioning profile，正式 Keychain native evidence 与生产配置仍 Open |
