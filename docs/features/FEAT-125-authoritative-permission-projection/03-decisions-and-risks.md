# FEAT-125 决策、风险与安全预审

## 1. 关键决策

| Decision ID | 问题 | 可选方案 | 选择 | 理由 | Owner | 状态/批准证据 |
|---|---|---|---|---|---|---|
| DEC-001 | 权限真相位于哪里 | Desktop / Agent Host / yijie-api | yijie-api | 符合现有仓库职责；前端不可信，Host 不拥有平台身份 | 段成威 | Existing accepted boundary |
| DEC-002 | 权限和产品可用性是否合并 | 单布尔值 / 两个正交维度 | 正交维度 | 避免“未发布”被误判为“无权限”，也避免 disabled 绕过权限过滤 | 段成威 | Accepted / A5 |
| DEC-003 | capability wire 类型 | 封闭 enum / 开放 namespaced string | 开放字符串 | 新 key 不使旧 consumer 崩溃；未知值默认忽略 | 段成威 | Accepted / A4 |
| DEC-004 | Desktop 默认策略 | 缺失即显示 / 缺失即拒绝 | deny-by-default | loading/error/context mismatch 不能泄露导航或页面 | 段成威 | Accepted / A5 |
| DEC-005 | 身份方式 | 自建账户 / 外部 OIDC / opaque API session | 外部 OIDC；仅系统浏览器 Authorization Code + PKCE S256；精确 ephemeral `127.0.0.1` loopback + state/nonce；禁 WebView/implicit/plain/secret/`localhost`；API 直接验证 audience=`https://api.yijie.ai` 的 RS256 access JWT，以 `(issuer, subject)` 映射 user；无 opaque API session | 使用标准原生应用登录流；不自建密码和 API session/token authority | 段成威 | Accepted / A1 |
| DEC-006 | 凭证生命周期与 Desktop 原生边界 | LocalStorage / cookie / memory+OS secure storage | access token 仅 Rust 内存；refresh token 仅 macOS Keychain `ai.yijie.desktop.auth`；10 分钟 access、30 天 idle/90 天 absolute refresh、旋转与 reuse detection；logout 撤销 refresh、删 Keychain 并清空内存/context；WebView 仅能调用固定 API HTTPS origin 上的 `listMyTenants`/`getMyCapabilities`，Rust 内附加 bearer，token 不跨 IPC，不提供通用 native proxy | 最小化凭证驻留与暴露，把刷新/撤销交给 IdP，同时避免 privileged Rust transport 成为 confused deputy | 段成威 | Accepted / A2 |
| DEC-007 | 活动租户 | 客户端任意 tenant / token 固定 / 逐请求选择并验证 | 必需 `X-Yijie-Tenant-ID`；它只是选择提示，API 每次验证 user/tenant/membership；0 个进入 recovery、1 个自动选、多个必须用户选，切换 abort+epoch+clear 后原子加载；v1 不持久化 last tenant，重启重选 | 无服务端 active-tenant session，避免把客户端 tenant 当授权事实 | 段成威 | Accepted / A3 |
| DEC-008 | Settings 与根路由 | 整页受 capability 控制 / core 常显 | Settings core/recovery 常显；`/` 在 ready 后选择首个允许入口 | 零权限、错误或被撤权时仍有 retry/logout/recovery | 段成威 | Accepted / A5 |
| DEC-009 | 现有 Tasks API | 本需求静默加 auth / 独立 breaking 轨 / 双隔离 | FEAT-125 不改 Tasks wire；service config 不注册 task handlers 且生产 ingress 拒绝；由 FEAT-126 独立改造 | 避免破坏匿名 consumer，也不让旧 Tasks 随 API 上线 | 段成威 | Accepted / A6 |
| DEC-010 | Contract 版本与影响 | additive 0.3 / semantic 0.3 / breaking 1.0 | semantic 0.3 | 新 operation 首次建立身份、租户和权限语义；既有 operation 不变且被隔离 | 段成威 | Accepted / A6 |
| DEC-011 | RBAC v1 | deny/allow、单/多角色、动态策略 | PostgreSQL allow-only、deny-by-default、多角色 union；`tenant_owner` 全 7 个点号 key，`tenant_member` 仅 `task.create`/`task.read`；user/tenant/membership 为 `active\|suspended` | 最小可解释、可审计并保持租户约束 | 段成威 | Accepted / A4 |
| DEC-012 | 数据与审计 | 无持久化 / session store / PostgreSQL expand | PostgreSQL expand；`authorization_revision` int64、wire 范围 `1..9007199254740991`、投影最长 5 分钟；无 Redis 权限缓存、无 sessions 表；授权写与通用 append-only audit 同事务 | PostgreSQL 是唯一事实源，失败整体回滚 | 段成威 | Accepted / A4 |
| DEC-013 | Public API 错误 | 复用任意 HTTP 状态 / 固定安全语义 | 仅 400/401/403/500/503；不使用 409；200-empty 表示合法零权限 | consumer 可稳定 fail-closed 且不混淆无权限与依赖故障 | 段成威 | Accepted / A3、A4 |

段成威已于 2026-07-31 明确批准 A1—A6。G1 需求/架构决策与 G2 设计门通过；2026-08-01
已执行并完成获特别授权的 S1/S2 Contracts local candidate。Provider/consumer 实施授权 G2A
仍为 Pending，具体 IdP 产品、issuer、client ID、生产域名/TLS
与 secret 配置属于 G3/G5 前置条件。

## 2. ADR 判定

- 是否改变仓库职责、依赖方向、公共契约、安全边界或既有 Accepted ADR：是。它首次把
  Public API 身份、活动租户、RBAC、Desktop 凭证和 fail-closed 边界连接成生产链路。
- 结论：安全/架构 ADR 已 Accepted，路径：
  `yijie/docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md`。
- ADR 固定：系统浏览器 Code + PKCE S256、API 直接验证 IdP JWT、凭证生命周期、
  operation-scoped Rust authenticated transport、`X-Yijie-Tenant-ID`、RBAC 数据权威、
  bootstrap、审计、Tasks 双隔离/FEAT-126 与 Infra/CSP 责任。
- 架构 Owner：段成威。
- 当前状态：Accepted；G1/G2 Passed；S1/S2 candidate complete and remote verified。API/Desktop 实现仍需
  段成威单独批准 G2A。

## 3. 风险登记

| Risk ID | 风险事件/触发条件 | 概率 | 影响 | 预防控制 | 检测 | 恢复/回滚 | Owner | 残余风险 |
|---|---|---:|---:|---|---|---|---|---|
| R-001 | 客户端 tenant/user 被当作授权事实 | high | critical | JWT 导出可信 Principal；`X-Yijie-Tenant-ID` 只作选择提示并逐请求验证 membership | 缺失/伪造 header 与双租户安全测试 | 关闭 endpoint/consumer | 段成威 | low |
| R-002 | loading/error 缺省显示全部模块 | high | high | deny-by-default total policy | AppShell/route E2E | kill switch 全部隐藏 | 段成威 | low |
| R-003 | 切租户时旧响应覆盖新状态 | medium | critical | abort+epoch+context 校验、clear-before-fetch | 延迟/乱序测试 | 清空 store、重新获取 | 段成威 | low |
| R-004 | capability 被误当业务授权凭证 | medium | critical | projection 永不作为授权票据；FEAT-125 隔离旧 Tasks，FEAT-126 才为资源 API 接入独立 `AuthorizationService.Check` | projection 篡改不改变 API 结果；Tasks 双隔离负测 | 禁用 consumer、保持 Tasks 隔离 | 段成威 | low |
| R-005 | token 进入前端存储或日志 | medium | critical | memory/Keychain 边界、日志 allowlist | storage/log scan | 撤销 token、清理日志 | 段成威 | low-medium |
| R-006 | 权限撤销后 UI 长期陈旧 | medium | high | `authorization_revision` + 最长 5 分钟快照；foreground/login/switch/403 refresh；旧 Tasks 在 FEAT-126 前保持双隔离 | expiry/revocation E2E | 清空投影、强制重登 | 段成威 | low |
| R-007 | RBAC 数据跨租户串线 | medium | critical | 复合 FK/唯一约束、tenant-scoped repository | 两租户 integration | 禁用写入口、roll-forward | 段成威 | low |
| R-008 | auth/RBAC 依赖故障被解释为零权限 | medium | medium | 503 与 200-empty 分离 | fault injection/metrics | retry、provider rollback | 段成威 | low |
| R-009 | 新 endpoint 以 additive 名义绕过安全评审 | medium | high | semantic 分类、G2/G2A/ADR | Reviewer checklist | 阻断 merge/tag | 段成威 | low |
| R-010 | 现有 Tasks 匿名/跨租户风险随 API 一同上线 | high | critical | FEAT-125 中 service config 不注册 task handlers + 生产 ingress 拒绝双隔离；FEAT-126 才修改 auth/tenant contract | 独立验证 service config 未注册 handlers；从 internet、Desktop、untrusted network 三来源负测 | 阻断生产或关闭整个 API 暴露 | 段成威 | low-medium |
| R-011 | floating contracts 产生 wire drift | high | high | exact tag/SHA/digest/generator + drift CI | clean regenerate | 回退到 pinned artifact | 段成威 | low |
| R-012 | 单人多角色导致自我批准掩盖缺陷 | medium | high | 分离 Codex Planner/Implementer/Reviewer pass，批准证据单独记录 | G4 review | 回到前一 gate | 段成威 | medium |
| R-013 | Rust authenticated transport 被滥用为通用代理或泄漏 bearer | medium | critical | 只暴露两个 operation intent；固定 API HTTPS origin/GET/path；Rust 内附加 bearer；IPC schema 不接受 URL/method/header/body且不返回 token | command allowlist/redirect/IPC fuzz + token scan | disable native commands、撤销 token、feature off | 段成威 | low |

## 4. 威胁建模

| 资产/边界 | 威胁 | 攻击路径 | 服务端控制 | 安全测试 | 残余风险 |
|---|---|---|---|---|---|
| access/refresh credential | 窃取与重放 | LocalStorage、日志、redirect 泄漏 | 系统浏览器、PKCE S256、10 分钟 access、Keychain、refresh rotation/reuse detection、TLS | storage/log/redirect；验证有效 bearer 在到期前的残余重放窗口 | IdP/OS 风险；无 DPoP，access JWT 最长 10 分钟可重放 |
| Desktop authenticated transport | confused deputy/SSRF/token IPC | 任意 operation/URL/method/header/body、redirect 越界、command/event 泄漏 | 固定两 GET operations 与 API HTTPS origin/path；Rust 内附加 bearer；IPC 无 token/Authorization 输入 | SEC-005/012 allowlist、redirect、IPC fuzz | 已批准 API origin 或 Rust dependency compromise |
| Principal | 伪造 issuer/subject | 错签名、错误 audience、alg confusion、未知 kid | 严格 issuer/aud/alg/time/JWKS 验证 | auth matrix | IdP compromise |
| active tenant | 越权切租户 | 缺失或伪造 `X-Yijie-Tenant-ID` | header 只作选择提示；user/tenant/membership 每请求验证；repository 显式 tenant | 0/1/多租户、header 与 two-tenant forgery | 管理员错误授权 |
| RBAC tables | 跨租户角色注入 | 跨 tenant role assignment | 复合 FK、事务、最小权限 DB role | DB constraint/integration | DB operator risk |
| capability endpoint | 枚举/缓存/泄漏 | CDN/browser cache、角色结构回传 | no-store、最小响应、rate limit | header/schema/log tests | 肩窥/UI 泄漏 |
| Desktop state | stale/篡改 | 修改 Pinia、迟到 response、离线重放 | UI 非安全边界；epoch/context/expiry | concurrency/E2E | 本地受控设备 |
| business API | IDOR/跨租户读取 | 猜 task ID、绕过 router | FEAT-125 通过 service config 不注册 task handlers 且生产 ingress 拒绝；FEAT-126 实施 server-side tenant/resource/action check | 独立 handler registration 断言 + internet/Desktop/untrusted network 三来源负测；FEAT-126 direct authorization tests | FEAT-126 完成前不得开放旧 Tasks |
| JWKS/redirect URL | SSRF/重定向劫持 | 动态 URL、宽泛 redirect | 固定 allowlist、TLS、配置验证 | malicious URL tests | provider outage |
| logs/audit | 敏感泄漏或伪造 | 记录 token/subject、换行注入 | 结构化日志、字段 allowlist、append-only | log scan/injection | privileged operator |
| dependency supply chain | 恶意 SDK/plugin | 未固定 generator/依赖 | lockfile、digest、audit、CODEOWNERS | generate drift/audit | upstream compromise |

本功能无文件路径、用户 URL、prompt、模型或工具调用，因此路径穿越、SSRF、提示注入和
越权工具在业务 payload 中为 N/A；IdP/JWKS URL 的 SSRF 风险仍按固定配置处理。

## 5. 数据生命周期

| 数据类别 | 收集 | 使用 | 存储 | 共享 | 保留 | 删除 | 审计 |
|---|---|---|---|---|---|---|---|
| OIDC issuer+subject 映射 | 首次认证 | 定位内部 user | PostgreSQL `user_identities` | yijie-api 内部 | 身份存续期 | 合规停用/删除流程 | 建立/状态变更 |
| tenant membership | bootstrap/Admin | 验证 tenant scope | PostgreSQL | yijie-api 内部 | membership 历史策略 | 状态化撤销优先 | 所有变更 |
| role/permission assignment | 受控写入口 | 服务端授权 | PostgreSQL | Authorization Service | 版本/审计窗口 | 受控撤销 | 同事务 |
| capability snapshot | API 计算 | Desktop 展示/路由 | 仅进程内存 | 当前 Desktop | 最长 5 分钟 | 到期、logout、切租户立即清空 | 只记 `authorization_revision`/result |
| IdP access/refresh token | IdP | API 认证/刷新 | access 仅内存；refresh 仅 macOS Keychain `ai.yijie.desktop.auth` | TLS 到 API/IdP | access 10 分钟；refresh idle 30 天、absolute 90 天 | logout 撤销 refresh、删除 Keychain 并清空内存 | 不记 token 内容 |

## 6. 高风险操作、审批与审计

| 工具/操作 | 用户意图 | 参数/影响范围 | 审批人/有效期 | 默认行为 | 审计字段 |
|---|---|---|---|---|---|
| bootstrap owner/tenant | 建立首个合法管理主体 | 单环境、单 tenant/user | 段成威；一次性且可撤销 | deny | actor、env、tenant、result、request |
| membership grant/revoke | 改变租户访问 | tenant+user | 授权管理员；即时生效 | deny | actor、target、from/to status、revision |
| role assign/remove | 改变 capability 集 | tenant+membership+role | 授权管理员；即时生效 | deny | actor、role、membership、diff、revision |
| permission catalog change | 改变授权语义 | 全局 key | Contract/Security review | deny | actor、old/new semantics、release |
| active tenant switch | 切换工作上下文 | 当前 user + target tenant | 0 个进入无租户 recovery；1 个自动选；多个必须用户选择；每次验证 membership | deny | user、from/to、result |
| read projection | 展示允许能力 | 当前 context | 有效身份即可 | deny on uncertainty | tenant、revision、status、latency |

## 7. 临时例外

| Exception ID | 原因 | 范围 | Owner | 批准证据 | 到期日 | 补偿控制 | 移除条件 |
|---|---|---|---|---|---|---|---|
| EXC-125-001 | 旧 `/v1/tasks` 尚未迁移到权威身份/租户/RBAC | 仅旧 Tasks handlers 与生产暴露；不覆盖 capability endpoint | 段成威 | A6 | FEAT-126 生产启用或 2026-09-30，取较早者 | service config 不注册 task handlers + 生产 ingress 拒绝；独立 handler registration 断言 + internet/Desktop/untrusted network 三来源负测 | FEAT-126 完成并生产启用；到期未完成不得开放 Tasks，必须重新审批 |

## 8. Codex 停止条件

- G2A 尚未由段成威批准时要求修改 yijie-api/yijie-desktop provider/consumer 或 migration；
  S1/S2 contracts source/generated candidate 可按已批准 G2 计划执行，但不得激活 provider；
- 要求在未重分类时修改既有 Tasks auth/tenant/error 语义；
- 不能从已验证凭证和 membership 导出 user+active tenant；
- 需要把 token/capability 写入前端普通存储或日志；
- 实现拟偏离已批准 migration、复合 FK、`authorization_revision` 或通用 append-only audit；
- 具体 IdP 产品/issuer/client ID、API origin、CSP、JWKS、TLS 或 secret 未在 G3/G5 配置并验证却要求生产启用；
- candidate 来自 dirty/floating sibling 或没有远端完整 SHA/digest；
- 任一安全测试出现默认放行、跨租户泄漏或弱化断言；
- API/Desktop 没有真实 candidate 集成却要求关闭 FEAT-124 G4-001；
- 工作区出现归属未知变更、生产 secret、真实用户或真实租户数据。

## 9. 批准记录

| 范围 | 决策人 | 结论 | 日期 | 证据 |
|---|---|---|---|---|
| 业务目标与保持 FEAT-124 阻断 | 段成威 | Approved；FEAT-124 G4-001 继续阻断到 FEAT-125 完成 | 2026-07-31 | 用户批准 A1—A6 |
| 架构与身份（DEC-005） | 段成威 | Approved；G1 Passed | 2026-07-31 | A1；ADR-0012 Accepted |
| 凭证生命周期（DEC-006） | 段成威 | Approved；G2 Passed | 2026-07-31 | A2 |
| 活动租户（DEC-007） | 段成威 | Approved；G2 Passed | 2026-07-31 | A3 |
| RBAC vocabulary/roles/data/audit（DEC-003/011/012） | 段成威 | Approved；G2 Passed | 2026-07-31 | A4 |
| Settings/root（DEC-002/004/008） | 段成威 | Approved；G2 Passed | 2026-07-31 | A5 |
| Tasks 双隔离与 FEAT-126（DEC-009/010、EXC-125-001） | 段成威 | Approved；G2 Passed | 2026-07-31 | A6 |
| Contracts S1/S2 授权 | 段成威 | Approved and executed；candidate/gates/remote verification PASS | 2026-08-01 | 用户明确指令；`9ec34abd...` |
| Provider/consumer 实施授权 | 段成威 | Pending G2A；API/Desktop implementation/test NOT RUN | 2026-08-01 | 需单独用户指令 |
| 具体 IdP 与生产配置 | 段成威 | Pending；G3/G5 blocker | 2026-07-31 | issuer/client ID/domain/TLS/secret 尚未登记 |
