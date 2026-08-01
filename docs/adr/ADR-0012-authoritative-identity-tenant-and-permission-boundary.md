# ADR-0012: 固定权威身份、租户与权限投影边界

## 状态

Accepted

## 日期

2026-07-31

## 决策负责人

段成威

## 关联需求

- `FEAT-125-authoritative-permission-projection`
- `FEAT-124-desktop-post-login-home` / `G4-001`
- 后续需求：`FEAT-126-public-task-authorization-hardening`（仅登记，尚未创建）

## 背景

FEAT-124 已实现 Desktop 登录后首页、导航和本地权限映射候选，但生产入口尚无可信权限
输入。当前 Public API 没有用户认证契约，`yijie-api` 也没有用户、租户、membership 或
RBAC 权威数据；既有 `/v1/tasks*` 仍信任客户端提交的租户信息。仅在 Desktop 中硬编码
权限会造成默认放行、跨租户复用和直接调用 API 绕过。

本 ADR 固定 FEAT-125 G1/G2 所需的架构与安全决策。具体 IdP 厂商、issuer、client ID、
JWKS、生产域名和生产控制面配置不由本 ADR 虚构，仍是 G3/G5 前置。G2A 已在
`contracts-v0.3.0` candidate 形成并通过契约门禁后由段成威于 2026-08-01 单独批准。

## 决策

### A1. 身份与 API 认证

1. 采用外部 OIDC，不自建密码认证。
2. Desktop 是 public client，使用系统浏览器执行 Authorization Code + PKCE S256；禁止
   embedded WebView 登录、Implicit Flow 和 Desktop client secret。
3. 回调固定为 `http://127.0.0.1:{ephemeral-port}/oauth/callback`。Desktop 必须使用一次性
   Rust loopback listener，并验证 `state`、`nonce` 和 PKCE verifier；禁止使用
   `localhost` 代替 loopback IP。
4. `yijie-api` 直接验证面向 API audience 的 IdP access JWT，不建立 Yijie opaque session。
   固定算法为 RS256，固定 audience 为 `https://api.yijie.ai`，并严格验证 issuer、
   signature、audience、时间与 JWKS key。API 不接受 ID token、email、display name 或 JWT
   中的 role 作为认证/RBAC 真相。
5. `(issuer, subject)` 映射到内部 user；外部 subject 与业务用户分表保存。
6. 若最终 IdP 不支持 API-audience JWT、动态 loopback redirect，或不支持本 ADR 所需的
   refresh rotation/reuse detection，必须重新打开 G1，不能静默切换到弱化方案。

### A2. 凭证生命周期与 Desktop 原生边界

1. Access token 生命周期 10 分钟；剩余不足 2 分钟时主动刷新，刷新必须 single-flight。
2. Refresh credential 最长空闲期 30 天、绝对最长 90 天；每次使用都轮换，旧 refresh
   credential 被重用时撤销整个 token family。
3. JWT 允许的 clock skew 为 60 秒；不得按 token 输入动态选择算法。
4. Access token、ID token 和 PKCE verifier 仅存在于进程内存。Refresh credential 仅保存到
   macOS Keychain，service 固定为 `ai.yijie.desktop.auth`。
5. Logout 必须撤销 refresh credential、删除 Keychain 项、清空内存 token、当前租户和
   capability。token 不得进入 LocalStorage、SessionStorage、IndexedDB、普通配置、日志、
   URL、崩溃报告或提交的 fixture。
6. 允许引入官方 Tauri opener plugin、Rust 一次性 loopback listener 和 Rust Keychain
   adapter。opener 只允许精确 IdP HTTPS origin；依赖与 capability 必须最小化、固定版本并
   通过 lockfile/audit 审核。具体 Keychain adapter crate/version 在实现切片内选择和审计。
7. Access token 由 Rust auth boundary 持有时，Desktop 只能通过 operation-scoped native
   transport 调用 `GET /v1/me/tenants` 与 `GET /v1/me/capabilities`。transport 使用固定的
   API HTTPS origin、method 和 path，在 Rust 内附加 Authorization；IPC 不返回 token，也
   不接受任意 URL、method、Authorization header 或通用代理 payload。响应继续由固定
   contracts candidate 生成的 TypeScript 类型/adapter 消费，禁止手写第二份 wire DTO。

### A3. 活动租户

1. 活动租户不写入 JWT，也不保存为 API server session。`GET /v1/me/tenants` 返回当前用户
   可用的 active memberships，最小字段为 `tenant_id` 与用户可识别的 `display_name`；该
   endpoint 不需要 tenant header，且响应必须 `no-store`。
2. 所有租户范围请求必须带 `X-Yijie-Tenant-ID: <uuid>`。该 header 只是客户端的租户选择
   提示，不是授权事实。
3. API 每个请求都以已验证 Principal 检查 user、tenant、membership 状态，并在同一租户内
   解析 role/permission；repository 必须显式使用经过验证的 tenant scope。
4. 零个租户进入 no-tenant recovery；一个租户自动选择；多个租户必须由用户明确选择，
   不得默认取第一个。第一版不持久化 last tenant 或 capability。
5. 切换顺序固定为：暂停新业务请求，取消旧请求，清空旧 capability/store/cache，设置候选
   tenant，获取新投影，最后原子激活。旧 context generation 的迟到响应必须丢弃。
6. `GET /v1/me/capabilities` 使用 bearer JWT 与 `X-Yijie-Tenant-ID`，返回
   `schema_version: 1`、已验证的 `tenant_id`、`authorization_revision: int64`、RFC 3339
   `expires_at` 和开放 capability 集合。wire revision 必须限制在 JavaScript 安全整数范围
   `1..9007199254740991`，或由 G2A 证明生成器使用不丢精度的精确表示；快照最大时效为
   5 分钟，响应必须 `no-store`。
7. 缺失或格式非法的 tenant header 返回 400；认证失败返回 401；user、tenant 或 membership
   拒绝返回 403；认证/JWKS/RBAC 依赖不可用返回 503；未预期内部错误返回 500。有效零权限
   返回 `200` 与空数组，不使用旧候选的 `409 tenant_context_required`。
8. Desktop 在启动、切租户、前台恢复、快照到期和权限相关 403 后刷新投影；任何不确定
   状态都 fail closed。

### A4. RBAC 与数据权威

1. PostgreSQL 是 RBAC 唯一权威源；第一版不引入 Redis 权限缓存。
2. 模型为 allow-only、default-deny、多角色 capability 并集；不实现 explicit deny、角色继承、
   ABAC、资源表达式或直接 user grant。
3. user、tenant 和 membership 状态只允许 `active | suspended`；任一为 suspended 即拒绝。
4. 初始 capability vocabulary 固定为：`task.create`、`task.read`、`store.read`、
   `workspace.use`、`schedule.read`、`plugin.read`、`knowledge.read`。Settings core 没有页面级
   capability。
5. 初始角色矩阵固定为：
   - `tenant_owner`：以上 7 项全部允许；
   - `tenant_member`：只允许 `task.create`、`task.read`。
6. 最小模型包含 `users`、`user_identities`、`tenants`（含从 1 开始的
   `authorization_revision bigint`）、`tenant_memberships`、`permissions`、`roles`、
   `role_permissions` 和 `membership_roles`；不得创建 `sessions` 表。
7. schema 必须使用 tenant 复合唯一/FK 约束防止跨租户 assignment。role、membership 或
   permission 变化必须在同一事务中递增 tenant `authorization_revision`。
8. 现有只绑定 task 的 `audit_logs` 边界必须泛化，或新增独立的 append-only authorization
   audit；授权写与审计同事务。读取 projection 不逐请求写业务审计，只记录脱敏状态、
   指标和 trace，不记录 token 或完整 capability 集。
9. `bootstrap-owner` 必须受控、幂等、可审计；migration 不写真实 user/tenant。FEAT-125
   不提供角色管理 UI 或公开角色管理 API。

### A5. Settings recovery 与默认路由

1. 已认证用户始终可见 Settings core，包括本地设置、重试、租户选择/切换和 logout；零权限
   或 permission error 时也必须可达。未来敏感 section 单独 gate。
2. `/` 在权限 ready 后按以下顺序选择入口：有 `task.create` 到 `/chat`；否则有
   `task.read` 到 `/tasks`；否则到 `/settings`。
3. 明确访问无权限业务深链时显示 forbidden，且不得实例化业务页面或静默跳转到另一个
   业务页面。无有效身份时进入 login/re-auth recovery。
4. 该规则有意修订 FEAT-124 的无条件 `/` → `/chat` 行为；FEAT-124 的视觉与 Tasks 独立
   页面要求不变。

### A6. 现有 Tasks API 处置

1. FEAT-125 不修改现有 `/v1/tasks*` wire contract，不在本版本引入 v2，也不宣称当前 Tasks
   API 是受支持的生产授权表面。
2. FEAT-125 生产激活前必须提供双层隔离：生产 ingress 拒绝 `/v1/tasks` 和
   `/v1/tasks/*`；生产 service configuration 不注册 task handlers。
3. 必须从互联网、Desktop 和不可信网络分别执行负向测试，证明被隔离路径不可达。
4. 该隔离作为有期限的临时例外登记：Owner 段成威；原因是避免在 FEAT-125 中静默破坏未知
   consumer；范围仅为旧 Tasks endpoints；补偿控制为 ingress + handler 双隔离与负向测试；
   到期时间为 FEAT-126 生产启用或 2026-09-30（取较早者）。到期未完成不得延用例外或开放
   Tasks，必须重新审批并继续阻断生产。
5. 后续 `FEAT-126-public-task-authorization-hardening` 负责身份、权威租户、handler/repository
   授权、consumer migration 和 v1 retirement。未知 consumer 存在时优先新增受保护 v2 再
   迁移；删除 v1 只能进入 major breaking release。
6. FEAT-124 `G4-001` 只有在真实权限 producer/consumer 集成和生产 Tasks 双隔离证据同时
   完成后才能关闭。G1/G2 或纯文档通过不能关闭该 finding。

## 生产配置保留门

- G3 前必须固定并验证：IdP 厂商、issuer、client ID、JWKS endpoint、精确 redirect
  registration、开发/测试 API origin，以及依赖版本/audit 证据。
- G5 前必须固定并验证：生产 tenant/client、生产 issuer/JWKS/domain/TLS、secret/config
  控制面、ingress 双隔离、Desktop 签名公证和 release/rollback 操作。
- G2A 是独立人工门，已于 2026-08-01 依据 `contracts-v0.3.0` candidate 的 source、生成物、
  完整 SHA、digest、generator、breaking check 和 semantic review 证据通过；它不批准生产配置。

## 备选方案

- **自建账户与密码**：扩大密码、恢复和风控责任面，拒绝。
- **yijie-api opaque session**：增加 session store、cookie/refresh 边界且无当前必要性，拒绝。
- **Embedded WebView 或 Implicit Flow**：不满足 native OAuth 安全边界，拒绝。
- **JWT 携带 Yijie role/capability**：策略陈旧、撤销困难并把 IdP claim 当业务真相，拒绝。
- **服务端隐式 active-tenant session**：增加状态同步并隐藏租户选择，拒绝。
- **客户端 tenant header 直接判权**：可伪造并导致跨租户访问，拒绝；header 仅作选择提示。
- **Settings 使用 `settings.read`**：零权限或授权故障时失去恢复入口，拒绝。
- **在 FEAT-125 静默硬化 Tasks v1**：可能破坏未知 consumer，拒绝；采用双隔离并另立需求。
- **Redis 权限缓存或独立 policy service**：首版增加一致性和运维复杂度，暂不采用。

## 影响

- `yijie-contracts` 将首次定义 user bearer、tenant selection header、tenants/capability operations
  与稳定错误语义，按 semantic `0.3.0` 管理。
- `yijie-api` 需要 identity/tenancy/authorization 模块、expand migration、严格 JWT adapter、
  tenant-scoped repository 与 append-only authorization audit。
- `yijie-desktop` 需要原生 OAuth/Keychain 与 operation-scoped authenticated transport
  边界、生成 TypeScript 类型/固定 contract adapter、内存 permission store、原子 tenant
  switch、deny-by-default navigation/router 和 recovery UI。
- API provider 必须先于 Desktop consumer 激活；旧 `contracts-v0.2.0` 继续作为受支持基线，
  Agent Host 不随 FEAT-125 迁移。
- 具体第三方和生产配置延后不会弱化 fail-closed：配置不完整时不得启用功能。

## 风险

- 外部 IdP 能力可能不满足本 ADR 的 native OAuth 或 refresh 安全要求；此时必须重开 G1。
- Direct bearer access JWT 在签发后无法由本地 session store 单独撤销；若被窃取，最长可重放至
  10 分钟 expiry。TLS、最小内存暴露、日志/存储禁入和服务端 user/membership suspension
  降低风险，但不能把 PKCE 或 refresh 撤销误称为 access-token replay 防护。
- direct JWT 依赖 issuer/JWKS 可用性；缓存、轮换和故障路径必须把不确定性映射为拒绝。
- 单人承担需求、技术、安全和发布责任；实现阶段必须由 Codex 分离 Planner、Implementer、
  Tester 与独立 G4 Reviewer pass，并以门禁证据代替主观自批。
- Tasks 双隔离是临时补偿控制，不是长期授权方案；未完成 FEAT-126 前不得开放这些路径。

## 后续动作

- [x] 段成威批准 A1—A6、G1 与 G2；
- [x] 将本 ADR 标记为 Accepted，并同步 FEAT-125 需求包；
- [x] 在 `yijie-contracts` 形成 `contracts-v0.3.0` local candidate
      `9ec34abd6e7dfb5a23b0154d467694167224ebbb`，执行生成、lint、test、build、
      pack、baseline breaking check 与 semantic review（2026-08-01 PASS；已 push，未 tag）；
- [x] 候选证据完成后由段成威单独批准 G2A（2026-08-01）；
- [ ] 在 G3 前固定 IdP 厂商、issuer、client ID、JWKS、redirect 和依赖审计；
- [x] 在 G2A 后完成 S3 API exact pin、expand migration、JWT/JWKS、identity/tenancy/RBAC
      foundation 与依赖审计（2026-08-01；`fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`；
      structured review PASS；无生产激活）；
- [x] 完成 S4 provider：tenant discovery/capability endpoints、逐请求 tenant 验证、稳定错误、
      producer conformance 与 metrics（2026-08-01；`360a526b679147472e7cc82ca7ac9db9d18a371d`；
      默认关闭、未 push、无生产 IdP 配置或激活）；
- [ ] 按 provider-first 顺序完成 Desktop consumer；
- [ ] 在 G5 前完成 Tasks ingress + handler 双隔离和三来源负向验证；
- [ ] 创建并实施 `FEAT-126-public-task-authorization-hardening`；
- [ ] 完成 FEAT-125 跨仓集成后回到 FEAT-124，独立关闭并复验 `G4-001`。
