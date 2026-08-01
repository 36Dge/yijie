# FEAT-125 — authoritative-permission-projection

## 1. 文档信息

| 字段 | 内容 |
|---|---|
| 状态 | G0/G1/G2/G2A Passed / S1—S6 Remote Verified / G3-NP-LOCAL PASS / S7 In Progress / G4 Pending |
| 需求负责人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |
| 创建日期 | 2026-07-31 |
| 最后更新 | 2026-08-01 |
| 原始需求链接/来源 | 本次 Codex 任务；前置关联 `FEAT-124-desktop-post-login-home` 的 `G4-001` |

## 2. 一句话目标

建立由 `yijie-api` 基于受信身份、活动租户和服务端 RBAC 生成的权限投影，让 Desktop
默认拒绝地控制导航与路由，同时确保前端呈现绝不替代服务端业务授权。

## 3. 问题与用户价值

- 目标用户/租户：已完成易界身份认证、且拥有有效活动租户成员资格的 Desktop 用户。
- 当前问题：Desktop 生产 App Shell 没有真实权限输入，缺省空投影会显示全部静态条目；
  Contracts/API 又尚未定义正式身份、会话和 RBAC，因此不能安全补一个前端布尔值。
- 用户可观察结果：用户只看到当前租户允许的模块；有权限但尚未发布的模块显示“即将开放”；
  无权限模块不进入 DOM、可访问性树或受保护页面。
- 为什么现在做：`FEAT-124` 的 `G4-001` 正在阻断 Code Complete，继续业务开发会把
  未定义的身份与权限边界扩散到更多页面。

## 4. 范围

### In Scope

- 固定身份主体、活动租户、凭证生命周期、撤销和 RBAC 的安全决策与 ADR。
- 在 `yijie-contracts/openapi/public/public.yaml` 设计
  `GET /v1/me/capabilities`、认证、错误、缓存和开放 capability vocabulary。
- 在 `yijie-api` 建立受信 Principal、租户成员关系、RBAC/Authorization Service、
  PostgreSQL expand migration、只读 capability projection 和必要审计。
- 在 `yijie-desktop` 建立不可变 contracts pin、生成 client、内存权限状态机、
  deny-by-default 导航映射、路由守卫及 Settings core 恢复页面。
- 在 Desktop Rust 边界实现系统浏览器 OIDC Authorization Code + PKCE S256：使用精确
  `http://127.0.0.1:<ephemeral-port>/oauth/callback` loopback callback、一次性 state/nonce、本地 listener 与
  native opener；直接消费 IdP access JWT，不引入 opaque Yijie session。
- access/ID token 只驻留 Rust 内存，refresh token 只进入获批的 macOS Keychain service
  `ai.yijie.desktop.auth`；access 最长 10 分钟、剩余不足 2 分钟时 single-flight refresh，
  refresh idle 30 天/absolute 90 天且每次旋转，reuse 时撤销整个 token family；
  token、授权码和 verifier 不进入 WebView、普通前端存储、URL 日志或应用日志。
- 上一条是最终产品安全要求。本地 Keycloak 当前只能证明 refresh rotation/旧 refresh 失效，
  没有证据证明 reuse 会自动撤销整个 token family；该 provider limitation 不阻断 S5B 代码
  实现，但必须保持 `S7 auth-lifecycle / G5 NOT RUN`，不得把本地 rotation 写成 A2 全量 PASS。
- WebView 仅能调用 Rust 暴露的 `listMyTenants`/`getMyCapabilities` 两个 operation-scoped
  authenticated operations；Rust 对已批准的固定 API HTTPS origin、method 与 path
  附加 bearer。IPC 不返回 token，也不接受任意 URL、method、Authorization header 或
  通用代理 payload；响应由固定契约生成的 TypeScript 类型与 adapter 消费。
- 完成 Contracts/API/Desktop 的 conformance、两角色×两租户安全集成与发布顺序验证。
- FEAT-125 完成后更新 FEAT-124 的 Desktop candidate，关闭 `G4-001` 并独立复跑 G4。

### Out of Scope

- 生产 OIDC 厂商、生产域名/TLS、Secret Manager、云基础设施与生产激活；当前只使用已批准
  的本地 Keycloak、专用 PostgreSQL、Caddy、loopback 和合成数据。
- 把角色名、菜单文案、排序、`disabled` 产品状态或内部策略表达式返回给 Desktop。
- 在 LocalStorage、SessionStorage、IndexedDB 或普通日志中保存 token、租户或 capability。
- Admin RBAC 管理 UI、批量授权 UI、计费 entitlement、第三方平台 access token。
- 修改既有 `/v1/tasks` 的契约、匿名访问、`tenant_id` 或错误语义；它保持 contract
  unchanged。现有默认 API profile 继续保留 legacy Tasks wire；只有本轮
  `feat-125-local-lab` profile 不注册 handlers，并由本地 Caddy 再拒绝该路径。未来生产必须
  用获批的宿主 API profile + public ingress 完成同等双隔离，后续由 `FEAT-126` 完成独立
  breaking hardening。该临时例外在 FEAT-126 生产启用或
  2026-09-30（取较早者）到期，到期未完成不得开放 Tasks且必须重新审批。
- Agent Host、Codex Runtime、AI prompt/model/retrieval/tool 行为。

## 5. 成功指标

| 指标 | 当前基线 | 目标值 | 测量窗口 | 数据来源 |
|---|---:|---:|---|---|
| 未授权导航进入 DOM/可访问性树 | 生产接入缺失，无法保证 | 0 | 每次 CI 与发布 smoke | Desktop 组件/E2E |
| 未授权深链实例化受保护页面 | 当前无 route guard | 0 | 每次 CI | Router 集成测试 |
| 跨租户权限或迟到响应复用 | 当前无权限状态机 | 0 | 每次 CI 与 staging | API/Desktop 集成 |
| 认证/RBAC 故障时默认放行 | 当前无正式链路 | 0 | 每次故障测试 | API/Desktop resilience |
| Contracts producer/consumer conformance | 当前无该契约 | 100% PASS | candidate 与 tag 各一次 | 三仓门禁 |
| FEAT-124 G4-001 | Open | Closed 后独立 G4 PASS | FEAT-125 完成后 | FEAT-124 验证报告 |

## 6. 约束

- 时间/成本：G1/G2 已于 2026-07-31 通过；G2A 前只允许按已批准边界完成 Contracts
  candidate，不以硬编码换进度。
- 兼容性：当前 supported baseline 为 `contracts-v0.2.0`；计划建立并验证
  `contracts-v0.3.0`，Agent Host 可继续消费 0.2.0。
- 合规/隐私：主体、租户、角色和 capability 为 Confidential；token/外部 subject
  不进入响应、fixture、文档或日志。
- 可用性/性能：授权依赖故障 fail-closed；UI 必须保留 retry、logout 和安全恢复入口。
- G3/S7 边界：G3-NP-LOCAL 只验证 TLS、OIDC discovery/JWKS、API startup/readiness、
  synthetic bootstrap、未认证 `401` 与 Tasks edge/direct `404`；完整系统浏览器登录、Rust
  bearer 调用、refresh/Keychain E2E 属于 S7/G5，不是 G3 PASS 条件。

## 7. 已确认事实、假设与未知项

| 类型 | 内容 | 证据/来源 | Owner | 处理状态 |
|---|---|---|---|---|
| Fact | yijie-api 是用户、租户与 RBAC 的业务权威仓 | `yijie-api/AGENTS.md` 与 README | 段成威 | Confirmed |
| Fact | 基线 `5320c302...` 的 Public OpenAPI 全局 `security: []`，没有正式身份契约 | `yijie-contracts` baseline scan | 段成威 | Confirmed |
| Fact | `0.3.0` candidate 已新增 operation-level `userBearer`、tenant discovery 与 capability projection；全局 `security: []` 和旧 operations 保持不变 | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` + remote/semantic equality checks | 段成威 | S1/S2 + remote Complete；G2A Passed |
| Fact | API 初始基线没有 auth/session/users/tenants/RBAC 表或 middleware；S3/S4 已建立 direct JWT、tenancy/RBAC 与只读 projection producer | `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`、`360a526b679147472e7cc82ca7ac9db9d18a371d` | 段成威 | S3/S4 Remote Verified |
| Fact | Desktop S5A/S5B 已实现原生认证边界、exact generated consumer 与内存 fail-closed store；S6 已接入默认关闭的 total navigation policy、lazy route guard、Settings 0/1/多租户恢复、前台刷新和 denied page | S5A `3798c67...`；S5B base `f94ac343...`；S6 implementation `cf0e080e4cf2fa10e1394aead67c669574714a4d`，final `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` remote verified | 段成威 | S5A—S6 Remote Verified；feature default off |
| Fact | G3-NP-LOCAL 的 API/Desktop/Infra 实现与仓内门禁已完成；Infra 71/71 + lint/Compose/shell/diff PASS；API local profile 在数据库访问前锁死 exact issuer、专用 loopback DB `yijie_api_feat125_local` 与 tracked 2 users × 2 tenants synthetic manifests；空库 migration 1→2、首次写入、幂等复跑及 inventory/revision/audit 已通过；Keycloak/PostgreSQL/Caddy 容器健康，live Keycloak 已证明 exact realm、两个 clients、canonicalized scope sets、显式 `userinfo.token.claim=false` mapper、strict managed `data_classification` user profile（Keycloak 26.7 REST 中 omitted field = unmanaged disabled）、两名固定合成用户、password resets 与 refresh revocation `invalid_grant`；固定 HTTPS 置密和最终 offline ready PASS | API `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34`、Desktop `446b4d608546fca8f53f4582201d6b43ef6f762d`、Infra `298192e386a7f7b81e8f0f8fe733c1f79f096ab4`；三个 `origin/develop` 已核验 | 段成威 | Dedicated DB、local dependencies、bootstrap、offline ready 与 core online PASS；G3 remote verified |
| Fact | 最小充分 G3 已用 API local-profile-only 显式 CA PEM + lowercase SHA-256 pin 关闭启动期 JWKS 信任阻断；默认/生产/disabled profile fail closed，未修改系统 Keychain | `yijie-api@faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` + final offline/core-online evidence | 段成威 | API CA review P0/P1/P2=0；G3 PASS；其后 S5B 已单独批准并完成 |
| Fact | FEAT-124 G4-001 仍是阻断 finding | FEAT-124 `08-verification-report.md` | 段成威 | Confirmed |
| Decision | 外部 OIDC native public client；系统浏览器 Code+PKCE S256，精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback`、state/nonce；Desktop 校验 auth response/state/PKCE 与 ID token nonce，API 以 audience `https://api.yijie.ai` 严格验证 IdP RS256 access JWT；不采用 opaque session | 段成威 A1/A2 | 段成威 | Approved / G1 |
| Decision | Desktop 通过 `X-Yijie-Tenant-ID` 表达当前租户选择；header 不是授权事实，API 每个请求重新验证 membership | 段成威 A3 | 段成威 | Approved / G1 |
| Decision | access/ID token 仅 Rust 内存；refresh token 仅 Keychain service `ai.yijie.desktop.auth`；access 最长 10 分钟、<2 分钟 single-flight refresh，refresh 30 天 idle/90 天 absolute、rotation+reuse family revoke；native opener/listener 与仅允许两个固定 GET 的 operation-scoped transport 构成 A2 的最小原生边界，token 不跨 IPC | 段成威 A2 | 段成威 | Approved / G1；本地 Keycloak 仅证明 rotation，family reuse 继续阻断 S7/G5 |
| Decision | 初始 vocabulary 固定 7 个点号 capability；`tenant_owner` 拥有全部 7 项，`tenant_member` 仅有 `task.create`/`task.read`；以 2 角色×2 租户验证，bootstrap 与变更必须审计 | 段成威 A4 | 段成威 | Approved / G2 |
| Decision | Settings core 对已登录用户常显；`/` 按 `task.create`→`/chat`、否则 `task.read`→`/tasks`、否则 `/settings`；denied deep-link 不实例化页面 | 段成威 A5 | 段成威 | Approved / G2 |
| Decision | `/v1/tasks` 契约不变；默认 API profile 保留 legacy wire；本地 `feat-125-local-lab` 不注册 handlers 且 Caddy 拒绝；未来生产需由获批宿主 profile + ingress 同样双隔离。独立 `FEAT-126` 承接 hardening；例外于 FEAT-126 生产启用或 2026-09-30 较早者到期 | 段成威 A6 | 段成威 | Approved / G2；最终 online edge/direct `404` PASS |
| Decision | 当前工程验证固定本地 Keycloak + 专用 PostgreSQL + Caddy；API bootstrap 只允许专用 loopback DB `yijie_api_feat125_local` 与固定 tracked synthetic matrix；issuer/API 使用 `localhost` 独立 HTTPS 端口，API 仅 local profile 使用严格显式 CA pin | 段成威批准 A7 / G3-NP-LOCAL | 段成威 | Approved；offline ready 与 core online PASS；不安装系统信任 |
| Unknown | 生产 IdP vendor/issuer/client ID/JWKS、生产 TLS/CSP、签名公证与发布环境配置；API audience 已固定为 `https://api.yijie.ai` | A7 只替代当前工程验证环境，不批准生产配置 | 段成威 | 不阻断本地 G3/S5B；继续阻断 G5/G6 |

## 8. 初始仓库基线

| Repository | Remote | Branch | Full HEAD SHA | Worktree | Existing changes owner |
|---|---|---|---|---|---|
| yijie | https://github.com/36Dge/yijie.git | develop | `ef0f50e41128c44ea91bf2e581e1fecf14c7b95c` | clean；与远端一致 | N/A |
| yijie-contracts | https://github.com/36Dge/yijie-contracts.git | develop | `5320c302f5c00f4080e9c3662a3f21cc1c4b813e` | clean；与远端一致 | N/A |
| yijie-api | https://github.com/36Dge/yijie-api.git | develop | `2834b412ad565651215bd12458276c4e0d8fecf5` | clean；与远端一致 | N/A |
| yijie-desktop | https://github.com/36Dge/yijie-desktop.git | develop | `be01cc2d0a1c9c4b057de616be201a4843d0a035` | clean；与远端一致 | N/A |
| yijie-infra | https://github.com/36Dge/yijie-infra.git | develop | `47c9e826d1f860d872958b05bafa44b1c3232f62` | G3 scope entry baseline；当时与远端一致 | N/A |

远端 `origin/develop` 与上述 SHA 已在 2026-07-31 使用 `git ls-remote` 复核。

## 9. 里程碑与状态

| 里程碑 | 目标日期 | Owner | 状态 |
|---|---|---|---|
| G0 需求建档 | 2026-07-31 | 段成威 | Passed |
| G1 设计就绪 | 2026-07-31 | 段成威 | Passed：A1—A3/A6 身份、凭证、租户与隔离边界已批准 |
| G2 可开始实现 | 2026-07-31 | 段成威 | Passed：A4—A6 RBAC、Settings/root route 与实施范围已批准 |
| G2A Contract Ready | 2026-08-01 | 段成威 | Passed：固定 candidate `9ec34abd6e7dfb5a23b0154d467694167224ebbb`，授权执行 S3 |
| G3 Slice/Nonproduction Ready | 2026-08-01 | 段成威 | Passed：最小显式 CA 修复、offline ready、core online 与最终三仓门禁 PASS；随后已单独批准并完成 S5B |
| G4 Code Complete | 跨仓实现与独立 review 后 | 段成威 | Pending |
| G5 Production Ready | 类生产安全验证后 | 段成威 | Pending |
| G6 Delivery Complete | 灰度与观察完成后 | 段成威 | Pending |

## 10. 变更日志

| 日期 | 修改人 | 变化 | 原因/批准 |
|---|---|---|---|
| 2026-07-31 | Codex | 先完成 Contracts/API/Desktop 三路只读审核，再创建完整需求包 | 用户要求先审方案再落地 FEAT-125 |
| 2026-07-31 | Codex | 保持 FEAT-124 G4-001 阻断，并登记身份/RBAC 安全决策门 | 防止前端硬编码或伪造权威权限 |
| 2026-07-31 | 段成威 | 批准 A1—A6 并通过 G1/G2；固定 direct IdP JWT、loopback+Keychain、tenant header、7-key/2-role、Settings/root route 与 Tasks 双隔离 | 用户明确批准；G2A 仍待 Contracts candidate |
| 2026-08-01 | Codex | 执行 S1/S2，形成 `0.3.0` local candidate `9ec34abd6e7dfb5a23b0154d467694167224ebbb`，完成生成、pack、breaking 与 semantic/security review | 用户明确要求执行 S1/S2；未 push、未批准 G2A、未进入 API/Desktop |
| 2026-08-01 | Codex | 将 candidate 推送到 yijie-contracts `origin/develop`，远端核对为 `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 用户明确要求 push；G2A 仍需段成威单独批准 |
| 2026-08-01 | 段成威 | 批准 G2A，固定 `9ec34abd6e7dfb5a23b0154d467694167224ebbb` 并授权 S3 | 生产 IdP 厂商/issuer/client ID/JWKS/配置仍为 G3/G5 前置，不生产激活 |
| 2026-08-01 | Codex | 完成 S3：API exact pin、migration v2、RS256 JWT/JWKS、identity/tenancy/RBAC 与单元/数据库集成/安全审计 | API 完整提交 `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`；未加入生产 IdP 值、endpoint 或生产激活 |
| 2026-08-01 | Codex | 对 S3 执行契约/认证/迁移/租户隔离/CI 依赖/范围六维结构化审查 | P0/P1/P2=0；P3 SHA 格式校验缺口已修复并复验；不代替最终独立 G4 |
| 2026-08-01 | Codex | 将 S3 API 与治理证据推送并远端核验 | yijie-api `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`；yijie `cd365ad095c4af6983b345794f0efef565efddbe` |
| 2026-08-01 | 段成威/Codex | 批准并完成 S4 tenant/capability endpoints、逐请求 tenant 验证、稳定错误、revision、metrics 与 producer/fault tests | API 完整提交 `360a526b679147472e7cc82ca7ac9db9d18a371d`；默认关闭、未 push、无生产配置/激活 |
| 2026-08-01 | Codex | 对 S4 做范围/契约/认证/租户一致性/生命周期/CI 六维结构化审查 | P1=1/P2=2 均修复；最终开放 P0/P1/P2=0；不代替最终独立 G4 |
| 2026-08-01 | Codex | 将 S4 API 与治理证据推送并远端核验 | yijie-api `360a526b679147472e7cc82ca7ac9db9d18a371d`；yijie `28c6f503f2c66a0dc5964d85cc5865fcb4ae2794` |
| 2026-08-01 | 段成威/Codex | 批准并完成 S5A Desktop Rust 原生系统浏览器 OIDC、精确 loopback、PKCE/state/nonce、Keychain token 生命周期与两个固定 authenticated operations | Desktop 完整提交 `3798c67d260237928730758c7ec4c1fbe6fcf7d2` 已推送并远端核验；功能默认关闭，无 S5B/UI、Tasks 或生产配置/激活 |
| 2026-08-01 | Codex | 对 S5A 做 scope、OIDC、token 生命周期、并发、Keychain、IPC/HTTP、依赖与失败语义结构化审查并复跑全部门禁 | 修复 6 类问题；开放 P0/P1/P2=0；前端 37 tests、Rust 27 tests、debug `.app/.dmg`、npm/cargo/license audit PASS；完整浏览器/Rust bearer/refresh/正式 Keychain provisioning 仍为 S7/G5 |
| 2026-08-01 | 段成威/Codex | 执行 G3 非生产环境准备：新增供应商中立、默认关闭、仅合成数据的 infra 模板、strict/online preflight 与 runbook；启动现有 local dependencies，应用 migration 2 并验证 API health/ready 和权限端点 404 | 当时仅完成通用 Preparation，未选择/伪造 IdP 厂商或真实 HTTPS 值，也未激活 API/Desktop；其外部资源前置随后由 A7 的 G3-NP-LOCAL 路径取代 |
| 2026-08-01 | 段成威 | 批准 A7 / G3-NP-LOCAL：以 loopback、Docker、合成数据、本地 Keycloak/专用 PostgreSQL/Caddy 和显式本地 CA 完成工程环境；生产资源、配置与激活继续禁止 | 不再等待云资源；本地门通过不等于 G5/G6 生产就绪 |
| 2026-08-01 | Codex | 以 API local-only 显式 CA PEM + SHA-256 pin 关闭历史 502 阻断，复跑 offline ready、core online 和最终三仓门禁 | G3-NP-LOCAL PASS；系统 Keychain/生产配置未改 |
| 2026-08-01 | 段成威/Codex | 单独批准并完成 S5B：固定 contracts-v0.3.0 candidate/generator，生成并接入 tenants/capabilities 类型与固定 adapter，实现 0/1/多租户状态、operation intent、revision/expiry/context 校验和内存 fail-closed permission store | Desktop implementation `5c4600f...`，CI path fix `942df58...`，final `f94ac343881b0f7df59c0f5f4169372e612fd019` 已推送并远端核验；80 frontend + 36 Rust tests、生成漂移、contract/fault/concurrency/security、结构化审查、全部本地门禁与 GitHub Actions run `30695055988` PASS；S6/UI/Tasks/Rust token lifecycle/生产配置未改，feature off |
| 2026-08-01 | 段成威/Codex | 单独批准并执行 S6：接入 Desktop AppShell/nav/router/Settings，固定 UI flag、root priority、denied lazy guard、0/1/多租户恢复和前台刷新 | implementation `cf0e080e...`、final `688fb72ddf...` 已推送并远端核验；18 frontend files/113 tests + 36 Rust tests、browser fail-closed/72px persistence、lint/build/docs/debug app+dmg/audits 与 review PASS；S7 随后获授权进入执行 |
