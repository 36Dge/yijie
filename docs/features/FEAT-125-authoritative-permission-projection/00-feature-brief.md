# FEAT-125 — authoritative-permission-projection

## 1. 文档信息

| 字段 | 内容 |
|---|---|
| 状态 | G0/G1/G2/G2A Passed / S1/S2 Candidate Remote Verified / S3 API Foundation Committed + Structured Review PASS |
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
- WebView 仅能调用 Rust 暴露的 `listMyTenants`/`getMyCapabilities` 两个 operation-scoped
  authenticated operations；Rust 对已批准的固定 API HTTPS origin、method 与 path
  附加 bearer。IPC 不返回 token，也不接受任意 URL、method、Authorization header 或
  通用代理 payload；响应由固定契约生成的 TypeScript 类型与 adapter 消费。
- 完成 Contracts/API/Desktop 的 conformance、两角色×两租户安全集成与发布顺序验证。
- FEAT-125 完成后更新 FEAT-124 的 Desktop candidate，关闭 `G4-001` 并独立复跑 G4。

### Out of Scope

- 由 Codex 擅自选择具体 OIDC 厂商、生产域名、TLS、Secret Manager 或云基础设施。
- 把角色名、菜单文案、排序、`disabled` 产品状态或内部策略表达式返回给 Desktop。
- 在 LocalStorage、SessionStorage、IndexedDB 或普通日志中保存 token、租户或 capability。
- Admin RBAC 管理 UI、批量授权 UI、计费 entitlement、第三方平台 access token。
- 修改既有 `/v1/tasks` 的契约、匿名访问、`tenant_id` 或错误语义；它保持 contract
  unchanged，并在生产同时由 public ingress 拒绝且 service 不注册 legacy Tasks handlers，后续由
  `FEAT-126` 完成独立 breaking hardening。该临时例外在 FEAT-126 生产启用或
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

## 7. 已确认事实、假设与未知项

| 类型 | 内容 | 证据/来源 | Owner | 处理状态 |
|---|---|---|---|---|
| Fact | yijie-api 是用户、租户与 RBAC 的业务权威仓 | `yijie-api/AGENTS.md` 与 README | 段成威 | Confirmed |
| Fact | 基线 `5320c302...` 的 Public OpenAPI 全局 `security: []`，没有正式身份契约 | `yijie-contracts` baseline scan | 段成威 | Confirmed |
| Fact | `0.3.0` candidate 已新增 operation-level `userBearer`、tenant discovery 与 capability projection；全局 `security: []` 和旧 operations 保持不变 | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` + remote/semantic equality checks | 段成威 | S1/S2 + remote Complete；G2A Passed |
| Fact | API 当前没有 auth/session/users/tenants/RBAC 表或 middleware | `yijie-api/internal` 与 migration 扫描 | 段成威 | Confirmed |
| Fact | Desktop 缺真实 API client、contract pin、permission store 和 route guard | `src/api/client.ts`、`package.json`、router | 段成威 | Confirmed |
| Fact | FEAT-124 G4-001 仍是阻断 finding | FEAT-124 `08-verification-report.md` | 段成威 | Confirmed |
| Decision | 外部 OIDC native public client；系统浏览器 Code+PKCE S256，精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback`、state/nonce；Desktop 校验 auth response/state/PKCE 与 ID token nonce，API 以 audience `https://api.yijie.ai` 严格验证 IdP RS256 access JWT；不采用 opaque session | 段成威 A1/A2 | 段成威 | Approved / G1 |
| Decision | Desktop 通过 `X-Yijie-Tenant-ID` 表达当前租户选择；header 不是授权事实，API 每个请求重新验证 membership | 段成威 A3 | 段成威 | Approved / G1 |
| Decision | access/ID token 仅 Rust 内存；refresh token 仅 Keychain service `ai.yijie.desktop.auth`；access 最长 10 分钟、<2 分钟 single-flight refresh，refresh 30 天 idle/90 天 absolute、rotation+reuse family revoke；native opener/listener 与仅允许两个固定 GET 的 operation-scoped transport 构成 A2 的最小原生边界，token 不跨 IPC | 段成威 A2 | 段成威 | Approved / G1 |
| Decision | 初始 vocabulary 固定 7 个点号 capability；`tenant_owner` 拥有全部 7 项，`tenant_member` 仅有 `task.create`/`task.read`；以 2 角色×2 租户验证，bootstrap 与变更必须审计 | 段成威 A4 | 段成威 | Approved / G2 |
| Decision | Settings core 对已登录用户常显；`/` 按 `task.create`→`/chat`、否则 `task.read`→`/tasks`、否则 `/settings`；denied deep-link 不实例化页面 | 段成威 A5 | 段成威 | Approved / G2 |
| Decision | `/v1/tasks` 契约不变，生产 public ingress 拒绝且 service 不注册 legacy Tasks handlers；独立 `FEAT-126` 承接 hardening；例外于 FEAT-126 生产启用或 2026-09-30 较早者到期 | 段成威 A6 | 段成威 | Approved / G2 |
| Unknown | 具体 IdP vendor/issuer/client ID/JWKS 生产值、TLS/CSP、签名与发布环境配置；API audience 已固定为 `https://api.yijie.ai` | 尚未选择生产基础设施 | 段成威 | Open / G3-G5 blocker；不阻断 G1/G2 |

## 8. 初始仓库基线

| Repository | Remote | Branch | Full HEAD SHA | Worktree | Existing changes owner |
|---|---|---|---|---|---|
| yijie | https://github.com/36Dge/yijie.git | develop | `ef0f50e41128c44ea91bf2e581e1fecf14c7b95c` | clean；与远端一致 | N/A |
| yijie-contracts | https://github.com/36Dge/yijie-contracts.git | develop | `5320c302f5c00f4080e9c3662a3f21cc1c4b813e` | clean；与远端一致 | N/A |
| yijie-api | https://github.com/36Dge/yijie-api.git | develop | `2834b412ad565651215bd12458276c4e0d8fecf5` | clean；与远端一致 | N/A |
| yijie-desktop | https://github.com/36Dge/yijie-desktop.git | develop | `be01cc2d0a1c9c4b057de616be201a4843d0a035` | clean；与远端一致 | N/A |

远端 `origin/develop` 与上述 SHA 已在 2026-07-31 使用 `git ls-remote` 复核。

## 9. 里程碑与状态

| 里程碑 | 目标日期 | Owner | 状态 |
|---|---|---|---|
| G0 需求建档 | 2026-07-31 | 段成威 | Passed |
| G1 设计就绪 | 2026-07-31 | 段成威 | Passed：A1—A3/A6 身份、凭证、租户与隔离边界已批准 |
| G2 可开始实现 | 2026-07-31 | 段成威 | Passed：A4—A6 RBAC、Settings/root route 与实施范围已批准 |
| G2A Contract Ready | 2026-08-01 | 段成威 | Passed：固定 candidate `9ec34abd6e7dfb5a23b0154d467694167224ebbb`，授权执行 S3 |
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
