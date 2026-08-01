# FEAT-125 决策、风险与安全预审

## 1. 关键决策

| Decision ID | 问题 | 可选方案 | 选择 | 理由 | Owner | 状态/批准证据 |
|---|---|---|---|---|---|---|
| DEC-001 | 权限真相位于哪里 | Desktop / Agent Host / yijie-api | yijie-api | 符合现有仓库职责；前端不可信，Host 不拥有平台身份 | 段成威 | Existing accepted boundary |
| DEC-002 | 权限和产品可用性是否合并 | 单布尔值 / 两个正交维度 | 正交维度 | 避免“未发布”被误判为“无权限”，也避免 disabled 绕过权限过滤 | 段成威 | Accepted / A5 |
| DEC-003 | capability wire 类型 | 封闭 enum / 开放 namespaced string | 开放字符串 | 新 key 不使旧 consumer 崩溃；未知值默认忽略 | 段成威 | Accepted / A4 |
| DEC-004 | Desktop 默认策略 | 缺失即显示 / 缺失即拒绝 | deny-by-default | loading/error/context mismatch 不能泄露导航或页面 | 段成威 | Accepted / A5 |
| DEC-005 | 身份方式 | 自建账户 / 外部 OIDC / opaque API session | 外部 OIDC；仅系统浏览器 Authorization Code + PKCE S256；精确 ephemeral `127.0.0.1` loopback + state/nonce；禁 WebView/implicit/plain/secret/`localhost`；API 直接验证 audience=`https://api.yijie.ai` 的 RS256 access JWT，以 `(issuer, subject)` 映射 user；无 opaque API session | 使用标准原生应用登录流；不自建密码和 API session/token authority | 段成威 | Accepted / A1 |
| DEC-006 | 凭证生命周期与 Desktop 原生边界 | LocalStorage / cookie / memory+OS secure storage | access token 仅 Rust 内存；refresh token 仅 macOS Keychain `ai.yijie.desktop.auth`；10 分钟 access、30 天 idle/90 天 absolute refresh、旋转与 reuse detection；logout 撤销 refresh、删 Keychain 并清空内存/context；WebView 仅能调用固定 API HTTPS origin 上的 `listMyTenants`/`getMyCapabilities`，Rust 内附加 bearer，token 不跨 IPC，不提供通用 native proxy | 最小化凭证驻留与暴露，把刷新/撤销交给 IdP，同时避免 privileged Rust transport 成为 confused deputy | 段成威 | Accepted / A2；本地 Keycloak family-reuse 证据受限，完整验证留在 S7/G5 |
| DEC-007 | 活动租户 | 客户端任意 tenant / token 固定 / 逐请求选择并验证 | 必需 `X-Yijie-Tenant-ID`；它只是选择提示，API 每次验证 user/tenant/membership；0 个进入 recovery、1 个自动选、多个必须用户选，切换 abort+epoch+clear 后原子加载；v1 不持久化 last tenant，重启重选 | 无服务端 active-tenant session，避免把客户端 tenant 当授权事实 | 段成威 | Accepted / A3 |
| DEC-008 | Settings 与根路由 | 整页受 capability 控制 / core 常显 | Settings core/recovery 常显；`/` 在 ready 后选择首个允许入口 | 零权限、错误或被撤权时仍有 retry/logout/recovery | 段成威 | Accepted / A5 |
| DEC-009 | 现有 Tasks API | 本需求静默加 auth / 独立 breaking 轨 / 双隔离 | FEAT-125 不改 Tasks wire 或默认 API profile；本地 `feat-125-local-lab`/未来获批宿主 profile 不注册 task handlers，且 ingress 拒绝；由 FEAT-126 独立改造 | 避免破坏匿名 consumer，也不让旧 Tasks 随权限 API 上线 | 段成威 | Accepted / A6 |
| DEC-010 | Contract 版本与影响 | additive 0.3 / semantic 0.3 / breaking 1.0 | semantic 0.3 | 新 operation 首次建立身份、租户和权限语义；既有 operation 不变且被隔离 | 段成威 | Accepted / A6 |
| DEC-011 | RBAC v1 | deny/allow、单/多角色、动态策略 | PostgreSQL allow-only、deny-by-default、多角色 union；`tenant_owner` 全 7 个点号 key，`tenant_member` 仅 `task.create`/`task.read`；user/tenant/membership 为 `active\|suspended` | 最小可解释、可审计并保持租户约束 | 段成威 | Accepted / A4 |
| DEC-012 | 数据与审计 | 无持久化 / session store / PostgreSQL expand | PostgreSQL expand；`authorization_revision` int64、wire 范围 `1..9007199254740991`、投影最长 5 分钟；无 Redis 权限缓存、无 sessions 表；授权写与通用 append-only audit 同事务 | PostgreSQL 是唯一事实源，失败整体回滚 | 段成威 | Accepted / A4 |
| DEC-013 | Public API 错误 | 复用任意 HTTP 状态 / 固定安全语义 | 仅 400/401/403/500/503；不使用 409；200-empty 表示合法零权限 | consumer 可稳定 fail-closed 且不混淆无权限与依赖故障 | 段成威 | Accepted / A3、A4 |
| DEC-014 | 当前无云资源时如何完成工程集成 | 等待云资源 / HTTP mock / 本地类生产环境 | G3-NP-LOCAL：loopback-only Keycloak + 专用 PostgreSQL + Caddy HTTPS + synthetic data；IdP/API 为 `localhost` 独立端口；Desktop 显式 CA pin 与 Keychain issuer/client/environment binding | 不等待云资源，同时保留真实 OIDC/TLS/RBAC/隔离语义；禁止 mock 或 insecure TLS 冒充集成 | 段成威 | Accepted / A7；offline ready/core online/final gates PASS |
| DEC-015 | S7 外部前置暂不可得时是否阻断后续业务开发 | 无限继续本地模拟 / 完全阻断业务 / 分离本地工程与生产激活里程碑 | `Local Engineering Baseline Complete / Production Activation Blocked`；冻结 S7 到真实部署准备，允许首页/聊天/Tasks 使用合成身份与权限继续开发；flags 默认关闭 | 当前无生产资源、生产 IdP 或 Apple 签名能力；现有契约/API/consumer/local 安全基线足以支持业务编码，但不足以宣称生产完成 | 段成威 | Approved 2026-08-01；不改变 ADR/契约；G4/G5/G6 保持未通过 |

段成威已于 2026-07-31 明确批准 A1—A6。G1 需求/架构决策与 G2 设计门通过；2026-08-01
已执行并完成获特别授权的 S1/S2 Contracts candidate；段成威已于 2026-08-01 通过 G2A，
S3 API foundation 已推送为 `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`；S4 provider 已推送并
远端核验为 `360a526b679147472e7cc82ca7ac9db9d18a371d`。S5A Desktop native boundary 已推送并
远端核验为 `3798c67d260237928730758c7ec4c1fbe6fcf7d2`，本地门禁与结构化审查开放
P0/P1/P2=0。本地 IdP/issuer/client/JWKS 已由 A7 固定；生产 IdP、域名/TLS 与 secret
配置仍属于 G5 前置。G3-NP-LOCAL 的静态实现、仓内门禁（Infra 71/71 +
lint/Compose/shell/diff）、local stack 与 exact realm/two clients/canonicalized scope sets/
explicit `userinfo.token.claim=false` mapper/strict managed `data_classification` user profile/
two fixed users/password reset/refresh revocation `invalid_grant` live conformance、
HTTPS synthetic user provisioning、offline ready 与 synthetic API bootstrap 已完成。API
local-only 显式 CA PEM + lowercase SHA-256 pin 已通过结构化审查（P0/P1/P2=0），最终 core
online 与三仓门禁 PASS，因此 G3 PASS；随后 S5B 已单独批准、完成并远端核验。
S7 已留下真实 blocker 证据，段成威随后批准 DEC-015：当前停止扩展 S7并登记本地工程基线
完成；生产 IdP、Apple 签名/Keychain、refresh family、2×2 bearer/performance 与生产运维证据
转为真实部署前强制恢复项，不作为当前业务代码开发的前置。

## 2. ADR 判定

- 是否改变仓库职责、依赖方向、公共契约、安全边界或既有 Accepted ADR：是。它首次把
  Public API 身份、活动租户、RBAC、Desktop 凭证和 fail-closed 边界连接成生产链路。
- 结论：安全/架构 ADR 已 Accepted，路径：
  `yijie/docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md`。
- ADR 固定：系统浏览器 Code + PKCE S256、API 直接验证 IdP JWT、凭证生命周期、
  operation-scoped Rust authenticated transport、`X-Yijie-Tenant-ID`、RBAC 数据权威、
  bootstrap、审计、Tasks 双隔离/FEAT-126 与 Infra/CSP 责任。
- 架构 Owner：段成威。
- 当前状态：Accepted；G1/G2/G2A Passed；S1—S6 complete and remote verified；G3-NP-LOCAL
  PASS；Local Engineering Baseline Complete。S7 已执行到真实 blocker 后冻结，真实部署准备时
  恢复；生产激活仍需完整 S7/G4/G5/G6。

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
| R-010 | 现有 Tasks 匿名/跨租户风险随 API 一同上线 | high | critical | 默认 legacy profile/wire 不变；FEAT-125 local/未来获批宿主 profile 不注册 task handlers + 对应 ingress 拒绝双隔离；FEAT-126 才修改 auth/tenant contract | 独立验证获批宿主 profile 未注册 handlers；从 internet、Desktop、untrusted network 三来源负测 | 阻断生产或关闭整个 API 暴露 | 段成威 | low-medium |
| R-011 | floating contracts 产生 wire drift | high | high | exact tag/SHA/digest/generator + drift CI | clean regenerate | 回退到 pinned artifact | 段成威 | low |
| R-012 | 单人多角色导致自我批准掩盖缺陷 | medium | high | 分离 Codex Planner/Implementer/Reviewer pass，批准证据单独记录 | G4 review | 回到前一 gate | 段成威 | medium |
| R-013 | Rust authenticated transport 被滥用为通用代理或泄漏 bearer | medium | critical | 只暴露两个 operation intent；固定 API HTTPS origin/GET/path；Rust 内附加 bearer；IPC schema 不接受 URL/method/header/body且不返回 token | command allowlist/redirect/IPC fuzz + token scan | disable native commands、撤销 token、feature off | 段成威 | low |
| R-014 | `openidconnect` 传递依赖 `rsa 0.9.10` 命中 RUSTSEC-2023-0071 | low in current verifier-only path | high if private-key operations introduced | S5A 只做 RS256 公钥验签，不含 RSA 私钥签名/解密；锁定依赖树并在 `.cargo/audit.toml` 记录可移除 ignore；禁止引入 private-key path | 每次 `cargo audit` + dependency tree/security review；上游修复监测 | 上游修复后升级并删除 ignore；若范围出现私钥运算立即阻断 | 段成威 | low for S5A candidate；G5 复核 |
| R-015 | 本地 CA 或 local-integration 配置泄漏到生产/扩大信任 | low-medium | critical | local profile 显式开启；仅允许 `localhost`；CA regular-file/no-symlink/权限/大小/digest 校验；默认 WebPKI；local secrets/CA private key ignored | config negative tests、artifact/env/Git scan、启动 fail-fast | 关闭 local profile、清理本地凭证/CA trust、重新登录 | 段成威 | low |
| R-016 | Keycloak native redirect 注册只放宽动态端口时意外放宽 path | medium | high | 必须以真实 authorize request 证明动态端口下仅接受 `/oauth/callback`；禁止 `*` 或任意 path；不满足则 G3 FAIL 并重新评审 provider | offline realm validator + online positive/negative redirect preflight | 保持 exact callback 配置与 drift 负测，不降低 callback 要求 | 段成威 | runtime proof PASS；correct path accepted / wrong path rejected |
| R-017 | API 启动期 JWKS HTTPS 无本地 CA trust | closed | critical | API local-profile-only explicit CA、exact localhost、single PEM/≤64KiB/0400或0600/regular non-symlink、lowercase SHA-256 pin、isolated proxy-free/no-redirect client；default/production fail closed | API startup/readiness + core online | 删除 local env 即安全回退；不修改系统 Keychain | 段成威 | closed；P0/P1/P2=0，P3 测试增强非阻断 |
| R-020 | refresh rotation 后 Keychain save fail 未撤销新 token；非法 refresh response 未撤销当前 token | closed in Desktop `155854cf3662384caa2c8bffe0a47935ef4a70b5` | high | 非法 refresh 先撤销当前 token；rotated token 落盘失败先撤销新 token，再清本地会话；两条故障测试覆盖 exact token | Desktop 全量 Rust/Clippy + fault tests PASS；远端 SHA 已核验；signed lifecycle 仍受 R-021/R-022 阻断 | 保持 feature off；真实部署前复跑 signed lifecycle | 段成威 | `S5A-REV-OPEN-001` resolved and remote verified；不再是 S7 blocker |
| R-018 | Keycloak rotation 被误报为 reuse-revokes-family | high if wording not constrained | high | 本地 config 固定 `provider_limit_documented`；G3 只记录 rotation，不记录 A2 family PASS | 生产恢复时执行 provider auth-lifecycle E2E | 换用满足要求的 provider/补偿控制并重新走安全评审 | 段成威 | deferred production-activation blocker；不阻断本地业务开发 |
| R-021 | pinned Keycloak 26.7 access JWT 缺少已批准 API 契约要求的 `nbf` | high | high | S7 harness 在发送 bearer 前严格校验 `iss/sub/aud/alg/kid/iat/nbf/exp`；不得放宽 API 或伪造 claim | 真实系统浏览器 Code+PKCE/loopback/code exchange 后稳定得到 `not_before_missing`；API 对同 token 返回 401 | 选择原生支持 `nbf` 的获批 IdP，或由段成威另行批准修改身份契约/ADR 后重做 API/provider conformance | 段成威 | open；deferred blocker for resumed S7/G4/G5，不阻断本地业务开发 |
| R-022 | 当前 Mac 无有效 code-signing identity/entitlement，Data Protection Keychain 真机写入失败 | high | high | 只执行隔离 synthetic service 的 ignored smoke；失败后确认无残留；不得降级普通 Keychain、文件或 LocalStorage | macOS error `-34018`；`security find-identity -v -p codesigning` 为 0 | 配置匹配的 Apple Development provisioning/entitlement，生成签名 native candidate 后复跑完整 Keychain/browser/Rust lifecycle | 段成威 | open；deferred blocker for resumed S7/G4/G5，不阻断本地业务开发 |
| R-019 | local bootstrap 误连共享或真实数据库 | high before guard | critical | `feat-125-local-lab` 在任何 DB 访问前锁死 exact issuer、credentialed `postgres://<credentials>@127.0.0.1:5432/yijie_api_feat125_local?sslmode=disable` 结构及固定 tracked 2×2 manifests；错误脱敏 | profile/DSN/manifest 负测 + 空库 inventory + 首次/幂等 bootstrap 对账 | unknown/drift fail closed；禁止写操作 | 段成威 | resolved in API `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34`；dedicated DB runtime proof PASS |

## 4. 威胁建模

| 资产/边界 | 威胁 | 攻击路径 | 服务端控制 | 安全测试 | 残余风险 |
|---|---|---|---|---|---|
| access/refresh credential | 窃取与重放 | LocalStorage、日志、redirect 泄漏 | 系统浏览器、PKCE S256、10 分钟 access、Keychain、refresh rotation/reuse detection、TLS | storage/log/redirect；验证有效 bearer 在到期前的残余重放窗口 | IdP/OS 风险；无 DPoP，access JWT 最长 10 分钟可重放；本地 Keycloak family reuse 未证明 |
| Desktop authenticated transport | confused deputy/SSRF/token IPC | 任意 operation/URL/method/header/body、redirect 越界、command/event 泄漏 | 固定两 GET operations 与 API HTTPS origin/path；Rust 内附加 bearer；IPC 无 token/Authorization 输入 | SEC-005/012 allowlist、redirect、IPC fuzz | 已批准 API origin 或 Rust dependency compromise |
| Principal | 伪造 issuer/subject | 错签名、错误 audience、alg confusion、未知 kid | 严格 issuer/aud/alg/time/JWKS 验证 | auth matrix | IdP compromise |
| active tenant | 越权切租户 | 缺失或伪造 `X-Yijie-Tenant-ID` | header 只作选择提示；user/tenant/membership 每请求验证；repository 显式 tenant | 0/1/多租户、header 与 two-tenant forgery | 管理员错误授权 |
| RBAC tables | 跨租户角色注入 | 跨 tenant role assignment | 复合 FK、事务、最小权限 DB role | DB constraint/integration | DB operator risk |
| capability endpoint | 枚举/缓存/泄漏 | CDN/browser cache、角色结构回传 | no-store、最小响应、rate limit | header/schema/log tests | 肩窥/UI 泄漏 |
| Desktop state | stale/篡改 | 修改 Pinia、迟到 response、离线重放 | UI 非安全边界；epoch/context/expiry | concurrency/E2E | 本地受控设备 |
| business API | IDOR/跨租户读取 | 猜 task ID、绕过 router | 默认 legacy profile 保持兼容；FEAT-125 获批宿主 profile 不注册 task handlers 且对应 ingress 拒绝；FEAT-126 实施 server-side tenant/resource/action check | 宿主 profile handler registration 断言 + internet/Desktop/untrusted network 三来源负测；FEAT-126 direct authorization tests | FEAT-126 完成前不得开放旧 Tasks |
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
| EXC-125-001 | 旧 `/v1/tasks` 尚未迁移到权威身份/租户/RBAC | 仅旧 Tasks handlers 与生产暴露；不覆盖 capability endpoint；默认 legacy profile/wire 保持不变 | 段成威 | A6 | FEAT-126 生产启用或 2026-09-30，取较早者 | 获批宿主 profile 不注册 task handlers + production ingress 拒绝；独立 handler registration 断言 + internet/Desktop/untrusted network 三来源负测 | FEAT-126 完成并生产启用；到期未完成不得开放 Tasks，必须重新审批 |
| EXC-125-002 | `rsa 0.9.10` 暂无修复版本且仅由 `openidconnect 4.0.1` 传递引入 | 仅 S5A RS256 公钥验签 candidate；不覆盖任何 RSA 私钥、签名或解密 | 段成威 | S5A commit、安全矩阵与审查记录 | G5 复核或上游修复可用时，取较早者 | exact lock、`.cargo/audit.toml` 有理由 ignore、每次 audit、禁止 private-key operation | 升级到修复链并删除 ignore；若不能证明 verifier-only 则停止发布 |

## 8. Codex 停止条件

- 未经相应 slice 授权要求越过 S4 修改 Desktop consumer 或生产配置；
  S1/S2 contracts source/generated candidate 可按已批准 G2 计划执行，但不得激活 provider；
- 要求在未重分类时修改既有 Tasks auth/tenant/error 语义；
- 不能从已验证凭证和 membership 导出 user+active tenant；
- 需要把 token/capability 写入前端普通存储或日志；
- 实现拟偏离已批准 migration、复合 FK、`authorization_revision` 或通用 append-only audit；
- 生产 IdP/client/API
  origin/CSP/JWKS/TLS/secret 未在 G5 配置并验证却要求生产启用；
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
| Provider/consumer 实施授权 | 段成威 | G2A Passed；S3/S4 API provider、S5A Desktop native boundary 与 S5B generated consumer/store 均已单独授权并完成；S6+ 与生产激活仍按后续 slice/gate | 2026-08-01 | 用户明确指令；S4 `360a526...`；S5A `3798c67...`；S5B final `f94ac34...` |
| S5A dependency exception | 段成威 | Accepted for non-production S5A candidate；G5 必须重审，禁止扩大到 RSA 私钥运算 | 2026-08-01 | EXC-125-002、Desktop security matrix、`cargo audit` PASS with documented ignore |
| 生产 IdP 与生产配置 | 段成威 | Pending；G5 blocker | 2026-07-31 | production issuer/client ID/domain/TLS/secret 尚未登记 |
| A7 / G3-NP-LOCAL | 段成威 | PASS；最小显式 CA 方案、offline ready、core online 与最终三仓门禁完成；随后 S5B 已单独批准并完成 | 2026-08-01 | local-only CA pin evidence；不修改系统 Keychain/生产配置 |
| 生产环境与激活 | 段成威 | Deferred；本地 G3 PASS 不替代 G5/G6 | 2026-08-01 | A7 明确保留门 |
