# FEAT-125 现状扫描与影响评估

## 1. 调查基线

| Repository | Rules read | Branch | Full HEAD SHA | Worktree | Toolchain |
|---|---|---|---|---|---|
| yijie | AGENTS、project memory、contract-first、Feature handbook | develop | `ef0f50e41128c44ea91bf2e581e1fecf14c7b95c` | clean / remote equal | Markdown/Bash |
| yijie-contracts | AGENTS、README、SECURITY、CONTRIBUTING、contract/version policies | develop | `5320c302f5c00f4080e9c3662a3f21cc1c4b813e` | clean / remote equal | Node 24–26、pnpm 11、Go |
| yijie-api | AGENTS、README、SECURITY、CONTRIBUTING、architecture/API/DB docs | develop | `2834b412ad565651215bd12458276c4e0d8fecf5` | clean / remote equal | Go 1.26.5、PostgreSQL 16 |
| yijie-desktop | AGENTS、README、SECURITY、CONTRIBUTING、design navigation rule | develop | `be01cc2d0a1c9c4b057de616be201a4843d0a035` | clean / remote equal | Vue 3、Tauri 2、pnpm 11 |

## 2. 已验证的当前行为

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
| yijie-infra | local/production dependencies | indirect/conditional | direct IdP RS256 JWT 架构已批准；具体 issuer/client/JWKS、API origin、secret 与 TLS 配置仍待落地 | 段成威 | G3/G5 前单独确认；当前不改 |
| yijie-admin-web | RBAC 管理 UI | none for first slice | 首版只允许受控 bootstrap，不做管理 UI | 段成威 | N/A |
| yijie-agent-host | local Runtime boundary | none | 不消费平台身份；继续固定 contracts-v0.2.0 | Agent Runtime Owner | N/A |
| yijie-codex/Runtime | Runtime source | none | 无 Runtime/AI 协议变化 | Runtime Owner | N/A |

## 4. 调用链与数据流

```text
approved external IdP → direct RS256 JWT
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
| tenants/memberships | yijie-api | expand candidate | 现有 tasks tenant_id 无 FK | 新 tenancy 读取 active/suspended 与 `authorization_revision` | bootstrap 与历史 task 归属另审 |
| roles/permissions/assignments | yijie-api | expand candidate | 无旧数据 | 新 authorization 读取 | 可禁用新 endpoint；保留 expand 表 |
| API session table | yijie-api | none / prohibited in this feature | direct IdP RS256 JWT 不需要本地 API session | yijie-api 只验证 IdP JWT，不签发或持久化 API session | N/A；不得创建 session 表 |
| audit_logs | yijie-api | semantic schema candidate | 当前 resource_id FK 仅指 tasks | 新授权变更无法直接复用 | 需独立 migration 设计并保持 append-only |
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
| Identity provider | direct IdP RS256 JWT architecture approved；具体 provider/issuer/client ID/JWKS 待 G3/G5 固定；audience 固定 `https://api.yijie.ai` | 否 | 配置形成后评估 | staging tenant | auth unavailable→deny |
| PostgreSQL | 16 / yijie-api 当前基线 | 现有任务链路已验证，RBAC 未验证 | 需容量测试 | 临时 schema integration | endpoint disable |
| Contracts generator | openapi-typescript 7.13.0；oapi-codegen 2.7.2 | 当前生成链存在 | N/A | repo CI | pin candidate |
| Tauri network/CSP | Tauri 2 / Desktop candidate | operation-scoped transport 设计已批准；生产 API origin 未验证 | N/A | local/staging | 不新增普通 fetch command 或通用 native proxy |
| Codex Runtime/AI | N/A | 不受影响 | N/A | N/A | N/A |

## 9. 现有测试、构建与发布入口

| 目的 | 真实命令/配置来源 | 作用范围 | 已知限制 |
|---|---|---|---|
| Contracts generate/lint/test/build | `make generate/lint/test/build` | 源、SDK、schema | CI breaking 仅 origin/main |
| Contracts baseline check | `./scripts/check-breaking.sh <full SHA>` | OpenAPI/AsyncAPI/JSON Schema | 必须显式用 v0.2.0 full SHA |
| API unit/lint | `make lint && make test` | Go/race/coverage | 当前无 auth/RBAC tests |
| API PostgreSQL integration | `make test-integration` / `make test-all` | 临时 schema/migration | 当前只覆盖 tasks |
| API generate | `make generate` | Go OpenAPI types | 当前读取 floating sibling |
| Desktop quality | `make lint && make test && make build` | Vue/TS/Rust | generate 仍是 placeholder |
| Desktop docs/native | `pnpm docs:build`、Tauri checks | design/native | API origin/CSP 未定 |
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
| SPIKE-001 | direct IdP RS256 JWT 与 Desktop login flow | 固定 provider metadata、issuer/client/JWKS 并验证 Tauri flow | 不注册生产应用、不写 secret | 段成威 | A1/A2 Approved；配置验证待 G3/G5 |
| SPIKE-002 | required `X-Yijie-Tenant-ID` 与 membership/status 验证 | 用合成状态图/测试替身验证 missing/invalid/denied | 不把 request tenant 当授权事实 | 段成威 | A3 Approved；实现验证待 G3 |
| SPIKE-003 | RBAC schema 与 bootstrap | 临时 schema migration rehearsal | 不写真实用户/租户，不建 API session 表 | 段成威 | A4 Approved；migration rehearsal 待 S3 |
| SPIKE-004 | 现有 Tasks API production disposition | 验证 ingress + handler 双隔离并创建 FEAT-126 | 不静默改 Tasks wire contract | 段成威 | A6 Approved；到期为 FEAT-126 生产启用或 2026-09-30 较早者；隔离证据待 G5 |
| SPIKE-005 | API origin/CSP/Keychain | local/staging 配置验证 | 不新增生产 URL/capability | 段成威 | Open / G3 |
