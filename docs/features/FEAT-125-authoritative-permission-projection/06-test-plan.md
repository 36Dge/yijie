# FEAT-125 测试与 Eval 计划

## 1. 测试策略

- 风险等级：High；身份、租户和 RBAC 属于安全关键路径。
- 阻断质量门槛：所有 Must AC 有重复自动证据；P0/P1/P2 安全 finding 为 0；任何默认
  放行、跨租户泄漏、token 泄漏、stale context 或 contract drift 均阻断。
- 类生产依赖：合成 OIDC/test issuer、PostgreSQL 16 隔离 schema、真实 yijie-api
  candidate、Desktop browser/Tauri candidate；禁止真实用户、token、tenant 或经营数据。
- 不可执行环境：具体 IdP 产品/issuer/client ID/JWKS、生产 Secret Manager、TLS/domain、
  签名/公证和生产 ingress 当前不存在；它们是 G3/G5 blocker，必须变为真实环境证据或
  明确阻断，不能推断通过。
- 方法：先 contract fixture 与 failing test，再 provider，再 consumer，最后真实跨仓与
  independent G4；禁止纯 resolver unit 冒充生产接入。

## 2. AC → 测试追踪矩阵

| AC/NFR | 风险 | Test ID | 层级 | 场景 | 环境 | 预期证据 |
|---|---|---|---|---|---|---|
| AC-001/002 | 权限计算错误 | CT-001, API-001 | contract+integration | 有权限与空权限 projection | Contracts+Postgres | schema + RBAC assertions |
| AC-003 | 认证绕过 | SEC-001 | API security | missing/malformed/invalid/expired IdP access JWT；内部 user suspended | test issuer | JWT failures 401；suspended 403；安全 headers |
| AC-004 | 租户越权 | SEC-002 | API integration | `X-Yijie-Tenant-ID` 缺失/非法、membership denied | 2 tenants | 400/403；无 409、无跨租户 capability |
| AC-005 | fail-open | RES-001 | fault integration | JWKS/DB unavailable | controlled faults | 503, no allow |
| AC-006/007 | consumer 兼容 | DESK-001 | contract consumer | unknown field/key/version/malformed/context mismatch | Vitest/fixture | ignore or fail-closed |
| AC-008/009/010 | UI policy | DESK-002 | unit+component+E2E | allowed-enabled、allowed-disabled、denied | Desktop | exact DOM/route assertions |
| AC-011/012 | stale context/tenant discovery | DESK-003, TEN-001 | contract+store concurrency+native restart | A→B、late A、logout、expiry、foreground；`GET /v1/me/tenants` 的 0/1/multiple 与重启 | Contracts+fake clock/server+Tauri | no flash/overwrite；0→recovery、1→auto、multiple→explicit；不持久化 projection/last tenant |
| AC-013 | UI bypass/旧 Tasks 暴露 | SEC-003 | cross-repo E2E | tampered route；独立验证 service config 未注册 handlers；从 internet、Desktop、untrusted network 三来源访问旧 Tasks | staging | projection 不授权业务；handler 不存在且三来源均被 ingress 拒绝 |
| AC-014 | wire drift | CT-002 | CI/conformance | exact SHA/digest/generator | all repos | clean regenerate |
| AC-015 | cross-tenant matrix | E2E-001 | full E2E | `tenant_owner`/`tenant_member` × 2 tenants × 批准 7 keys | staging synthetic | 精确 role union 与 allow/deny |
| AC-016 | linked gate | REV-001 | independent review | fixed candidates + all evidence | yijie | FEAT-124 G4 rerun |
| AC-017 | native OIDC login | OIDC-001 | Tauri+test IdP | 系统浏览器 Code+PKCE S256、精确 ephemeral `127.0.0.1` loopback、唯一 state/nonce、PKCE 与 ID-token nonce 校验 | native candidate + test IdP | 无 WebView/deep-link/implicit/plain/secret/`localhost`/固定端口；非精确 callback 被拒绝 |
| AC-018 | token/Keychain/native transport lifecycle | SEC-011/012 | Tauri+test IdP | access/ID token Rust 内存、Keychain refresh、10m/30d/90d、single-flight、rotation/reuse、logout/Keychain failure；两个 operation-scoped calls | native candidate + test IdP | token 不经 IPC/WebView/普通存储；只允许固定 API origin 与两个 GET operations；generic proxy/任意 URL、method、header 被拒；reuse 撤销 family；失败 fail-closed；清理幂等 |
| AC-019 | root/deep-link policy | DESK-004 | router+component+Tauri | ready 投影分别含 `task.create`、仅 `task.read`、两者皆无；访问 `/` 与 denied deep-link | Desktop | `/chat`→`/tasks`→`/settings` 优先级精确；denied 页面不实例化 |
| AC-020 | exact RBAC vocabulary | API-004, E2E-001 | DB integration+cross-repo E2E | `tenant_owner`/`tenant_member` × 2 tenants | Postgres+API+Desktop | owner 精确 7 点号 key；member 仅 `task.create`/`task.read`；无冒号/隐式 key/跨租户 union |
| AC-021 | Tasks temporary isolation | SEC-003 | config+network security | FEAT-126 未生产启用且未到例外期限 | service+production-like ingress | service config 不注册 handlers；internet/Desktop/untrusted network 均被拒绝；到期自动阻断 |
| NFR-001/002 | security | SEC-004 | property/integration | missing/unknown/concurrent context | all | zero fail-open/leak |
| NFR-003 | reliability | RES-002 | resilience | timeout/cancel/retry/restart | controlled faults | bounded recovery |
| NFR-004 | performance | PERF-001 | load | projection 50 RPS | staging | p95 ≤300ms |
| NFR-005 | accessibility | A11Y-001 | browser/Tauri | error/recovery/hidden item | light/dark/min window | keyboard+AX evidence |
| NFR-006/007 | provenance/privacy | SUP-001 | CI/static scan | pin and secret/log scan | clean repos | no drift/leak |
| NFR-008 | native auth/transport security | OIDC-001, SEC-011/012 | Rust unit+Tauri security | callback/PKCE/nonce/Keychain 与 native operation allowlist/IPC boundary | native candidate + test IdP/API | exact callback；固定两 GET operations；zero token IPC/generic proxy |

## 3. 领域与边界测试

| 类别 | 正常 | 边界 | 非法/失败 | Test IDs |
|---|---|---|---|---|
| 核心业务规则 | `tenant_owner` 全 7 keys、`tenant_member` 前 2 keys、多角色 union | 无角色、256-key contract bound、重复输入 | suspended user/tenant/membership、跨 tenant role | API-001—004 |
| 公共 API | v1 ready/empty | unknown capability、extra field、5 分钟 expiry、`authorization_revision` 1/MAX_SAFE_INTEGER 边界 | revision 0/超 `9007199254740991`、400/401/403/500/503、tenant header 缺失/非法；不得出现 409 | CT-001—005 |
| 数据库/事务 | membership/role/permission read/write+audit | concurrent revision、同名 role 跨 tenant | FK violation、write/audit failure rollback | DB-001—006 |
| 身份提供方 | 系统浏览器 Code+PKCE S256、valid issuer/aud/kid/RS256 | 60 秒 clock skew、key rotation、cached JWKS | WebView/implicit/plain PKCE/client secret/`localhost` redirect、state/nonce mismatch、wrong issuer/aud/alg、unknown kid、nbf/exp | SEC-001/007 |
| Desktop 原生传输 | `listMyTenants`、`getMyCapabilities(tenant UUID)`；固定已批准 API HTTPS origin/GET/path；Rust 内附加 bearer | API 400/401/403/500/503、abort、响应大小/格式边界 | 任意 operation/URL/method/header/body、Authorization 输入、redirect/scheme downgrade、token IPC、通用代理 payload | SEC-005/012 |
| UI/可访问性 | enabled routes、core Settings | empty set、only one capability | loading/error/denied、late response | DESK-001—006 |
| 旧 Tasks 双隔离 | service config 不注册 handlers + ingress deny | capability tamper | handler 被注册，或 internet/Desktop/untrusted network 任一来源可达 | SEC-003；资源级授权由 FEAT-126 验证 |

## 4. 兼容与 Conformance

- 未知字段：Desktop decoder 必须容忍 v1 response 额外字段。
- 未知 enum/event：capability 不是封闭 enum；未知 key 忽略且不创建入口。
- 新旧 producer/consumer：覆盖 old API+new Desktop 安全关闭、new API+old Desktop
  回归、新 API+new Desktop、unknown key+old FEAT-125 Desktop。
- 生成漂移：Contracts regenerate clean；API/Desktop 从固定 candidate 和 tag regenerate
  clean；source digest、bundle digest、generator 一致。
- Canonical fixture：只位于
  `yijie-contracts/tests/fixtures/public/access/`，Feature 文档仅引用。
- Runtime/第三方兼容：Agent Host 继续 0.2.0，需证明既有 Agent Host contract/generated
  projection 除 bundle version provenance 外无语义变化；OIDC test issuer 固定配置。
- 人工 semantic review：认证、tenant、errors、headers、expiry、unknown values、rollback。

## 5. 安全与隐私测试

| Test ID | 威胁 | 场景 | 预期结果 |
|---|---|---|---|
| SEC-001 | 认证伪造 | missing/malformed、bad signature/issuer/aud、非 RS256、exp/nbf/iat、unknown kid、rotation；ID token 冒充 access token | 无可用验证 key 时稳定 401 或安全 503；内部 user suspended 为 403；无 token 泄漏 |
| SEC-002 | 跨租户 | 缺失/非法/伪造 `X-Yijie-Tenant-ID`、A user 选择 B、user/tenant/membership suspended、role assignment 跨 tenant | header 错误 400、授权拒绝 403；projection/DB 无 B 数据；无 409 |
| SEC-003 | 前端绕过/旧 Tasks 暴露 | 篡改 Pinia/route；独立检查 service config handler registration；从 internet、Desktop、untrusted network 三来源探测 `/v1/tasks` | capability 不成为授权票据；service config 未注册 handlers，三来源均被 ingress 拒绝；资源级授权留给 FEAT-126 |
| SEC-004 | fail-open | DB/JWKS timeout、malformed projection、unsupported schema | API/Desktop 均 deny |
| SEC-005 | token/PII 泄漏 | 扫 LocalStorage/SessionStorage/IndexedDB、IPC command/event/result、logs、errors、fixtures、Git diff；检查 Keychain bridge allowlist | access 仅 Rust 内存、refresh 仅 Keychain `ai.yijie.desktop.auth`；无 credential、subject、真实数据 |
| SEC-006 | 缓存泄漏 | browser/proxy revalidation、logout 后 back navigation | no-store；内存清空；无 304/stale reuse |
| SEC-007 | OIDC redirect/JWKS 注入 | WebView/implicit/plain PKCE、public-client secret、`localhost`/非精确 loopback redirect、state/nonce mismatch、动态 issuer/JWKS URL、scheme downgrade | 只允许系统浏览器 Code+PKCE S256 与精确 `http://127.0.0.1:{ephemeral-port}/oauth/callback`；allowlist/TLS validation 拒绝其余输入 |
| SEC-008 | RBAC 写越权 | 未授权 bootstrap/role/membership mutation | 默认拒绝并审计失败 |
| SEC-009 | 审计篡改 | UPDATE/DELETE audit、写成功但 audit 失败 | append-only；事务整体回滚 |
| SEC-010 | capability 语义污染 | 角色名、菜单 key、超长/非法 key、重复 key | schema/domain 拒绝或规范化，绝不默认 allow |
| SEC-011 | token 生命周期/logout | access 10 分钟、剩余不足 2 分钟 single-flight refresh、refresh idle 30 天/absolute 90 天、rotation/reuse、重复 logout | access 只驻内存；refresh 只驻 Keychain；reuse 撤销 token family；logout 撤销 refresh、删除 Keychain 并清 auth/tenant/projection；重复执行幂等 |
| SEC-012 | native authenticated transport 越权 | 枚举未知 operation，注入任意 URL/method/Authorization header/body，篡改 API origin/path，诱导 redirect，检查 IPC output 与错误 | Rust 只允许固定 HTTPS origin 上的 `listMyTenants`/`getMyCapabilities` GET；仅后者接受 tenant UUID；内部附加 bearer；不跟随越界 redirect；IPC 永不返回 token；无通用 proxy |

Direct bearer JWT 没有 DPoP 或 API session replay store：同一仍有效 access JWT 的重复使用
不会被 API 识别为重放失败。安全测试验证它不泄漏、最长 10 分钟到期，且 refresh token
rotation/reuse detection 在 IdP 测试替身中撤销 token family；不得伪造“有效 bearer 会被
立即单次化拒绝”的 PASS。

## 6. 韧性与故障测试

| Test ID | 故障 | 注入方式 | 恢复预期 | 观测信号 |
|---|---|---|---|---|
| RES-001 | PostgreSQL/JWKS unavailable | fake dependency / test container stop | DB 不可用 503；已有未过期 cached JWKS key 时继续严格验签，无可用 key/unknown kid 刷新失败时 503；恢复后 retry 成功 | status counter + latency |
| RES-002 | request timeout/abort | delayed handler + AbortController | old request cancelled；无 stale commit | cancel/mismatch counter |
| RES-003 | tenant A response after switch B | barrier-controlled fake server | A response dropped；B 加载前 protected=0 | context mismatch |
| RES-004 | projection expires | fake clock | 先 clear 后 refresh；失败保持 deny | refresh/error |
| RES-005 | app foreground/restart | lifecycle event/native restart | 重新拉取，不恢复持久 capability 或 last tenant；重启后重新执行 0/1/多租户选择规则 | fetch count/storage scan |
| RES-006 | retry storm | repeated 503 | capped backoff+jitter；logout 可用 | request rate |
| RES-007 | API rollback/missing endpoint | old provider/404 | Desktop permission-unavailable，不显示全部 | unsupported provider |
| RES-008 | partial DB transaction | fail audit insert | role/membership mutation rollback | audit+DB assertions |

## 7. Migration 演练

| 组合 | 数据状态 | Reader/Writer | 预期 | 校验 |
|---|---|---|---|---|
| old app + expanded schema | 已有 00001 tasks/audit data | old API | 启动和既有测试不变 | make test-all |
| new app + empty auth tables | 无 bootstrap | new API | header 缺失 400；合法 header 但无身份/membership 时 403；不默认 owner | integration |
| new app + synthetic bootstrap | 2 users/2 tenants、`tenant_owner`/`tenant_member`、7 keys | new API | 精确矩阵一致、`authorization_revision` int64、审计完整 | DB+E2E |
| concurrent role/membership updates | same revision | new writer | 无 lost update/跨 tenant | concurrency test |
| audit schema upgrade | existing task audit rows + UUID role/membership + text permission key | old/new reader | old rows可读；task-only FK 已解除；resource_id/resource_key CHECK、查找索引和 append-only trigger 有效 | migration integration |
| app rollback after expand | expanded schema retained | old API | 旧 API 正常；不做 destructive down | rollback rehearsal |
| roll-forward | prior failed deploy | fixed new API | 使用同一 schema safely resume | migration status + smoke |

任何需要删表/列或回退真实授权数据的 down migration 默认不执行；已批准策略为 app
rollback + 保留 expand schema + roll-forward。S3 已完成 00001 existing data→00002 expand、
拒绝 destructive down、保留 goose version 2 的自动化演练；bootstrap/old-binary smoke 仍待 S7。

## 8. 性能与容量

| Metric | Workload | Baseline | Pass threshold | Stop threshold |
|---|---|---:|---:|---:|
| projection latency p95 | 50 RPS、2 roles×2 tenants、实际 7-key catalog | S3 建立 | ≤300ms | >500ms |
| projection error | same load, healthy deps | S3 建立 | <0.1% | ≥1% |
| DB query count | single request | S3 trace | 无 N+1；固定上限 | 随 cap/role 线性无界 |
| Desktop active request | rapid foreground/switch | 0 baseline | ≤1/current context | stale commit >0 |
| capability size | 256 unique keys | N/A | contract-valid且受限 | unbounded/截断成功 |

这些数字已在 G2 作为测试目标批准；S4 已加入进程内请求/延迟 recorder，但 50 RPS staging
性能与真实 exporter/dashboard 仍 NOT RUN；G5 必须用类生产数据量建立真实基线后
才能判定 PASS。

## 9. AI Eval 专项

本需求不改变模型、prompt、Skill、Knowledge、retrieval 或 tool schema，因此 AI Eval
N/A。不能用对话主观体验替代身份/RBAC/contract/security 测试。

## 10. Fixture 与测试数据

| Fixture/Dataset | 权威位置 | 数据分类 | 合成/脱敏方式 | Consumer |
|---|---|---|---|---|
| capability v1 ready/empty/unknown/errors | `yijie-contracts/tests/fixtures/public/access/` | Internal synthetic | 固定 UUID、无真实身份 | Contracts/API/Desktop |
| tenant memberships v1 empty/single/multiple | `yijie-contracts/tests/fixtures/public/access/` | Internal synthetic | 固定 user/tenant UUID；0、1、2 个 active membership，无真实身份 | Contracts/API/Desktop |
| OIDC token matrix | yijie-api test-only authn fixtures | Restricted test-only | 本地测试 issuer/key；绝不生产复用 | API |
| RBAC 2×2 matrix | yijie-api integration fixtures | Internal synthetic | 两用户、两租户、`tenant_owner` 全 7 keys、`tenant_member` 仅 `task.create`/`task.read` | API/E2E |
| Desktop delayed responses | yijie-desktop test fake server | Internal synthetic | epoch/context A/B | Store/router |
| migration existing data | yijie-api integration setup | Internal synthetic | 00001 合成 task/audit | DB migration |

测试 token 只能由 test key 运行时生成，不把可用 bearer 字符串提交到仓库。

## 11. 实际执行命令

| 层级 | Repository/CWD | Command | 环境依赖 | 预期时长 |
|---|---|---|---|---|
| contract install/generate | yijie-contracts | `pnpm install --frozen-lockfile && make generate` | Node/pnpm/Go | <5m |
| contract quality | yijie-contracts | `make lint && make test && make build && pnpm pack:sdk` | repo toolchain | <10m |
| contract baseline | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | git baseline | <5m |
| API unit/lint | yijie-api | `make lint && make test` | Go | <5m |
| API DB integration | yijie-api | `make test-all` | PostgreSQL 16 test DSN | <10m |
| API generate drift | yijie-api | `make generate-check` | exact contracts checkout `9ec34abd...` + oapi-codegen v2.7.2 | <5m |
| Desktop quality | yijie-desktop | `make lint && make test && make build` | Node/pnpm/Rust | <10m |
| Desktop docs/native | yijie-desktop | `pnpm docs:build` 加仓库现有 Tauri checks | Tauri/macOS | <15m |
| Cross-repo E2E | test harness location at S7 | S7 提交真实命令后登记 | test IdP+Postgres+API+Desktop | 未建立 |

不存在的 generate-drift、load 或 E2E 命令必须作为对应 slice 的工程产物提交后再执行；
本计划不编造命令。

## 12. 通过、失败与 Flaky 策略

- PASS：命令完成、exit 0、断言与固定 SHA/digest 匹配，且人工 semantic diff 通过。
- FAIL：任一 Must、security、migration、conformance、跨租户或阻断阈值失败。
- NOT RUN：环境缺失、被跳过、输出截断、仍运行或命令尚未建立。
- Flaky：立即标记 FAIL/Investigating；禁止重跑到绿或放宽 timeout/断言。
- Snapshot/golden：生成 diff 与 fixture 必须人工复核身份、tenant、error 和 unknown 语义。
- 测试独立性：每个 tenant/schema/token 独立，cleanup 只删除 test-owned data。

## 13. 测试计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 测试/技术 Owner | 段成威 | G2/G2A/S4 Approved；S1/S2 contract、S3 foundation 与 S4 producer lint/unit/race/integration/drift/conformance PASS；S5+/Desktop NOT RUN | 2026-08-01 |
| 安全/数据 Owner | 段成威 | S3/S4 JWT/JWKS、精确 audience、重复 auth header、原子 projection、跨租户/RBAC 与 govulncheck PASS；生产 IdP/config 和跨仓 E2E NOT RUN | 2026-08-01 |
