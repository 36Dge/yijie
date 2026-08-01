# FEAT-125 契约与兼容变更计划

## 1. Contract Impact 结论

- 分类：`semantic`。
- 理由：新增两个 operations 在结构方向上兼容，但它们是 Yijie Public API 首次定义正式用户认证、
  活动租户和权限投影；auth/scope/error/cache 语义必须按 semantic/security 评审。
- 边界：`openapi/public/public.yaml#listMyTenants` 与
  `openapi/public/public.yaml#getMyCapabilities`，producer 为 `yijie-api`，primary
  consumer 为 `yijie-desktop`；两个 operation 必须进入同一 0.3.0 candidate。
- 业务/安全语义是否变化：是，新 operations 建立身份与租户信任边界；现有 operation
  顶层 `security: []` 和请求/响应语义保持不变。
- 计划版本：`0.3.0`，计划不可移动 tag：`contracts-v0.3.0`。
- 重分类条件：若同一交付给既有 `/v1/tasks` 强制加 auth、改义/移除 request
  `tenant_id` 或改变既有错误，使旧匿名调用失效，则归为 `breaking` 并重新定版本。

## 2. 权威源与责任

| 契约/边界 | 权威源类别 | 仓库与路径 | Owner | Producer | Consumers |
|---|---|---|---|---|---|
| Tenant-selection HTTP operation | central contract | `yijie-contracts/openapi/public/public.yaml#listMyTenants` | 段成威 | yijie-api | yijie-desktop、unknown-public |
| TenantSelectionList schema | central contract | `openapi/public/public.yaml#/components/schemas/TenantSelectionList` | 段成威 | yijie-api | generated Go/TS clients |
| Capability HTTP operation | central contract | `yijie-contracts/openapi/public/public.yaml#getMyCapabilities` | 段成威 | yijie-api | yijie-desktop、unknown-public |
| CapabilityProjection schema | central contract | `openapi/public/public.yaml#/components/schemas/CapabilityProjection` | 段成威 | yijie-api | generated Go/TS clients |
| ErrorResponse | existing central contract | `public.yaml#/components/schemas/ErrorResponse` | 段成威 | yijie-api | all Public consumers |
| Authentication scheme | central contract + security ADR | `public.yaml#/components/securitySchemes/userBearer`（direct IdP RS256 JWT） | 段成威 | external IdP/yijie-api | Desktop |
| RBAC/membership | private DB/domain | yijie-api migration + authorization module | 段成威 | yijie-api | yijie-api only |
| Navigation mapping | consumer policy | yijie-desktop domain/navigation | 段成威 | Desktop domain | AppShell/router |
| G3-NP-LOCAL deployment interface | owning service/infra config + ADR-0012 A7 | `yijie-infra` local profile、`yijie-api` service profile、`yijie-desktop` local-integration config | 段成威 | Infra/API/Desktop | local operator/test harness |

生成物、SDK、handler 类型、Pinia state、fixture 和数据库行都不是第二权威源。

本轮 A7 不修改上述 Public OpenAPI source 或 0.3.0 candidate。新增的本地服务、端口、CA
配置、bootstrap issuer pin、Tasks handler registration profile 与 Keychain envelope 属于
deployment/private-persistence interface；它们沿用本需求最高风险 `semantic` 分类，证据为
精确配置/镜像 pin、负向 validator、数据兼容与受影响 API/Desktop/Infra 验证，而不是伪造
新的 contracts tag 或 generator。

## 3. 语义设计

### 请求

- Tenant selection：`GET /v1/me/tenants`，operationId `listMyTenants`，tag `Access`。
  它只要求 direct IdP RS256 bearer JWT，不接受也不读取 `X-Yijie-Tenant-ID`、request body、
  query、pagination 或 sorting；用于在 0/1/多 active membership 情况下建立选择列表。
- Capability projection：`GET /v1/me/capabilities`，operationId `getMyCapabilities`，tag
  `Access`。
- 无 request body、query、pagination、sorting 或幂等键；必须携带 UUID 格式的
  `X-Yijie-Tenant-ID` header。
- `X-Yijie-Tenant-ID` 只是客户端提供的不可信租户选择提示，不是授权事实；API 必须用
  已验证 JWT Principal 对该 tenant 执行 membership/status 检查。缺失或格式非法返回 400，
  membership/status 拒绝返回 403。
- 已批准 operation-level `userBearer`，`bearerFormat: JWT`。Desktop 直接从外部 IdP
  获取 RS256 JWT；API 严格验证 issuer、audience、RS256 signature、`exp`/`nbf`、`kid`
  与 JWKS rotation。本需求不使用 cookie、opaque API session 或 yijie-api 签发的 token。
- IdP access JWT 最大有效期为 10 分钟。refresh credential 撤销或重用检测只保证下一次
  refresh 失败，不承诺使已签发 access JWT 即时失效；已签发 JWT 最迟在自身 expiry 后
  失效。内部 user suspension 或 membership/status suspension 必须由 API 实时返回 403。
  本地 Keycloak 仅形成 rotation/旧 refresh 失效证据，未证明 reuse 自动撤销整个 family；
  `provider_limit_documented` 继续阻断 S7/G5，G3 不得把它写成 A2 完整 PASS。
- 现有全局 `security: []` 和旧 operations 保持不变。
- 现有 `/v1/tasks` wire contract 与默认 API profile 保持不变；本地
  `feat-125-local-lab` 和未来获批的生产宿主 profile 必须不注册 handlers，并分别由 Caddy/
  production ingress 拒绝，不能把 capability projection 误称为 Tasks 授权。
  该临时例外在 FEAT-126 生产启用或 `2026-09-30` 中较早者到期；到期仍未完成时不得开放
  Tasks，必须继续隔离并由段成威重新审批。

### 响应/事件

Tenant selection 成功响应：

```json
{
  "tenants": [
    {
      "tenant_id": "019c0123-4567-7abc-8123-456789abcdef",
      "display_name": "Synthetic Tenant"
    }
  ]
}
```

- `tenants` required、允许为空，只包含 JWT Principal 当前 active memberships；不得包含
  suspended/revoked membership、角色、capability、外部 subject 或其它租户元数据。
- 每项 `additionalProperties: false`，且只包含 required `tenant_id`（UUID）与
  `display_name`（string，1—200 字符）。`display_name` 仅用于展示，不参与授权。
- 0 项：Desktop 保留 Settings core/recovery，不调用 capability endpoint；1 项：可自动选择；
  多项：要求用户明确选择。选择后才把 tenant UUID 作为 `X-Yijie-Tenant-ID` 发送给
  capability endpoint，API 仍须重新验证 membership/status。
- 200、401、403、500、503 均必须 `Cache-Control: no-store`。Tenant list 无 tenant input，
  因此不返回 tenant header 相关的 400；JWT missing/invalid/expired 返回 401，内部 user
  suspension 返回 `403 user_access_denied`，membership/JWKS 存储不可用返回
  `503 authorization_unavailable`；未预期失败返回 `500 internal_error`。

Capability projection 成功响应：

```json
{
  "schema_version": 1,
  "tenant_id": "019c0123-4567-7abc-8123-456789abcdef",
  "authorization_revision": 42,
  "expires_at": "2026-07-31T12:05:00Z",
  "capabilities": [
    "schedule.read",
    "task.create",
    "task.read"
  ]
}
```

- `schema_version`：int32，第一版只允许 1。
- `tenant_id`：UUID，是 membership/status 验证通过后的 `X-Yijie-Tenant-ID` 回显证据，
  绝不能直接成为客户端授权事实。
- `authorization_revision`：required int64，minimum 1，maximum
  `9007199254740991`（JavaScript `Number.MAX_SAFE_INTEGER`）；服务端签发的授权快照修订号，
  只用于诊断、刷新和 stale 检测，不暴露内部规则，也不能作为授权凭证。生成的
  TypeScript consumer 使用安全整数 `number` 并在边界校验该上限，不把超界 int64 静默
  舍入。
- `expires_at`：RFC 3339 date-time；不得晚于响应签发时间 5 分钟。
- `capabilities`：required、可为空、unique、最多 256 项、服务端字典序输出；consumer
  不依赖顺序并再次去重。
- capability item：开放字符串，长度 3–128，pattern
  `^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)+$`。
- 已批准的首版 vocabulary 恰好为七个点号 capability：`task.create`、`task.read`、
  `store.read`、`workspace.use`、`schedule.read`、`plugin.read`、`knowledge.read`。
- Settings core 不使用 capability；它在 ready、零权限和错误恢复状态均保留最小的
  retry/logout/recovery 入口。不得新增或推断 `settings.read`。
- 不返回角色、菜单文案、排序、disabled、策略表达式、token 或外部 subject。
- 未知 capability 必须被旧 Desktop 忽略；未知 response 字段按 OpenAPI consumer
  兼容策略容忍。

Capability projection 错误与 header：

| HTTP | code | 语义 | 必需 header |
|---:|---|---|---|
| 200 | N/A | 有效身份+租户；capabilities 可为空 | `Cache-Control: no-store` |
| 400 | `invalid_tenant_context` | required `X-Yijie-Tenant-ID` 缺失或不是 UUID | `Cache-Control: no-store` |
| 401 | `unauthorized` | access JWT 缺失、非法或过期，不区分泄漏原因；不承诺 refresh 撤销会即时撤销已签发 JWT | `Cache-Control: no-store`、`WWW-Authenticate` |
| 403 | `tenant_access_denied` | 身份有效但 membership/tenant 状态拒绝 | `Cache-Control: no-store` |
| 500 | `internal_error` | 未预期内部失败 | `Cache-Control: no-store` |
| 503 | `authorization_unavailable` | JWKS/IdP key 或 RBAC 存储不可用，必须 fail-closed | `Cache-Control: no-store`；可选 `Retry-After` |

错误继续复用既有扁平 `{code,message}`，不在本需求引入新 envelope。有效零权限必须是
`200 + []`，不能返回 403；授权依赖故障不能伪装为 `200 + []`。

### 审批与审计

- 读取 projection 不需要高风险逐次审批，但必须通过 authn/membership。
- 必需脱敏信号：request/trace、内部 user、tenant、`authorization_revision`、结果状态、延迟。
- 不记录 token、完整 capability、外部 subject、角色图或 SQL。

## 4. 兼容方向

```text
新增 endpoint：provider 先实现，consumer 后调用
新增 capability response value：旧 consumer 先证明 unknown-ignore，provider 后返回
删除/改名 capability：consumer 先双读/别名迁移，provider 后停止旧 key
修改既有 Tasks auth/tenant：由 FEAT-126 重新分类并走独立 expand/migrate/switch
```

| Version combination | Request | Response/Event | Expected | Test |
|---|---|---|---|---|
| old API + new Desktop | endpoint 不存在 | 404/unsupported | Desktop feature flag 保持 off，不发布依赖路径 | consumer old-provider test |
| new API + old Desktop | 旧 Desktop 不调用新 endpoint | 新 response 不被读取 | 既有行为不变；API 先部署安全 | regression |
| new API + new Desktop | 先用 JWT GET tenants，再用 JWT + required `X-Yijie-Tenant-ID` GET capabilities | tenant list + v1 projection | 0/1/多租户选择后正常投影或稳定错误 | cross-repo conformance |
| new API adds unknown capability + old FEAT-125 Desktop | request 不变 | unknown string | 忽略未知值且不显示新模块 | unknown-value test |
| API rolled back after Desktop release | endpoint 缺失/5xx | 无有效 projection | Desktop fail-closed、retry/logout；不能显示全部 | rollback E2E |

## 5. 支持基线与 Breaking Check

| Baseline version | Full commit | Support window | Check command | Result/evidence |
|---|---|---|---|---|
| contracts-v0.2.0 | `f16a497e1377f45747f8ff9292b4b60cf2027f88` | supported | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | PASS 2026-08-01：oasdiff/Buf/AsyncAPI/JSON Schema 无 breaking |

不得继续使用 v0.2.0 首版发布前的 fallback。`docs/supported-baselines.md` 已在 S2 修正
旧“本轮未 push”文案；远端 annotated tag object `c6e8577...` 已复核 peeled 到
`f16a497...`，没有改变 0.2.0 语义。

## 6. Generator 与下游 Pin

| Consumer | Contract version/tag | Full commit | Digest | Generator/version | Owner |
|---|---|---|---|---|---|
| yijie-api candidate | 0.3.0 candidate | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | source `7bd40dd1c5a53cc1dcd317e3a64bf7189170fd7f575b25bb07f0eb243d0319ed` / Go `01d31efc1b1c3fb69e18c853d67ea12cdc313c2709f2a02d02e2a01b6ff4d253` | oapi-codegen v2.7.2 | 段成威 |
| yijie-desktop candidate | 0.3.0 candidate | 与 API 相同 | source `7bd40dd1c5a53cc1dcd317e3a64bf7189170fd7f575b25bb07f0eb243d0319ed` / TS `77babb215608c6ace4468d37b72fc8e43f5758231c7807a4301063cb156ae8e0` / tarball `43a54d7f9f01edd6b50adcebb8c3b4b645dab7ec8cf4aafe20b62d7d98718565` | openapi-typescript 7.13.0 / approved wrapper | 段成威 |
| yijie-api release | contracts-v0.3.0 | tag 解析完整 SHA | 验证与 candidate 相同 | 同 candidate | 段成威 |
| yijie-desktop release | contracts-v0.3.0 | tag 解析完整 SHA | 验证与 candidate 相同 | 同 candidate | 段成威 |
| yijie-agent-host | contracts-v0.2.0 | `f16a497...` | 既有固定值 | oapi-codegen v2.7.2 | Agent Runtime Owner |

API floating sibling generate 已在 S3 被 exact pin + generate-drift CI 取代；Desktop 的
placeholder generate 与 generated adapter 已由 S5B exact lock/generator 取代；仍不允许用手写影子 DTO 或
floating sibling 例外代替。

## 7. Fixtures 与 Conformance

| Fixture | 唯一权威位置 | Producer test | Consumer test | 结果 |
|---|---|---|---|---|
| tenant-list-v1-empty.json | yijie-contracts/tests/fixtures/public/access/ | active memberships only | Settings core/recovery | Contract + API producer conformance PASS；consumer NOT RUN |
| tenant-list-v1-single.json | 同上 | tenant id + display name only | auto-select then projection | Contract + API producer conformance PASS；consumer NOT RUN |
| tenant-list-v1-multiple.json | 同上 | no role/capability leakage | explicit selection | Contract + API producer conformance PASS；consumer NOT RUN |
| capability-v1-ready.json | yijie-contracts/tests/fixtures/public/access/ | API response validation | Desktop generated decoder | Contract + API producer conformance PASS；consumer NOT RUN |
| capability-v1-empty.json | 同上 | 200-empty | Settings core-only navigation | Contract + API producer conformance PASS；consumer NOT RUN |
| capability-v1-unknown.json | 同上 | schema-valid open value | unknown-ignore | Contract validation PASS；consumer NOT RUN |
| six public access error fixtures | 同上 | 400/401/403/500/503 stable codes | error adapter/state machine | Contract + API producer/fault conformance PASS；consumer NOT RUN |

Feature 目录只引用这些 fixture，不复制 JSON。

## 8. 合并、部署、启用与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | 登记已批准的 A1—A6，固化 ADR、scope、vocabulary、错误和 Tasks isolation | yijie / 段成威 | G1/G2 passed 2026-07-31 | 保持全链未实现 |
| 2 | 创建 0.3.0 source+generated candidate | yijie-contracts | Complete：S1 `ab5e71db6e4d61eb9c761446066142de2edbb444` | 回退 contracts commits |
| 3 | generate/lint/test/build/pack/baseline+人工 semantic review | yijie-contracts | Complete：S2 local `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 不晋升 G2A |
| 4 | 推送最终 candidate full SHA | yijie-contracts | Complete 2026-08-01；origin/develop = `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 保留 0.2.0 |
| 5 | API exact pin、migration、provider 非生产实现 | yijie-api | Complete/remote：S3 `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` + S4 `360a526b679147472e7cc82ca7ac9db9d18a371d`；structured review PASS | flag default off；无生产配置，app rollback + retain expand schema |
| 6 | Desktop native OIDC/Keychain 与 operation-scoped transport | yijie-desktop | Complete/remote：S5A `3798c67d260237928730758c7ec4c1fbe6fcf7d2`；local security matrix + structured review PASS | native flag default off；撤销/删除 Keychain family；不发布 |
| 7 | 建立 G3-NP-LOCAL 并通过 offline ready/online preflight | Infra+API+Desktop | PASS：API local-only explicit CA PEM + lowercase SHA-256 pin、exact issuer/JWKS、isolated proxy-free/no-redirect client、静态/最终门禁、local stack、专用 DB/bootstrap、offline ready 与 core online（discovery/JWKS/callback、health/ready、两个 401、Tasks edge/direct 404）全部通过；公共 wire/contracts 变更 N/A，属于 semantic deployment trust | 全部 local flags off、停止精确本轮宿主 API并清其环境，再停止 local profile；不改变 default profile/production |
| 8 | Desktop exact pin、generated adapter/store；fail-closed UI 留 S6 | yijie-desktop | S5B exact pin/generated adapter/store 已在 `5c4600f...` PASS；S6 UI pending | feature off；不发布 Desktop |
| 9 | API/Desktop candidate conformance 与两租户 E2E | 三仓 | full SHA/digest equal | 修复后重测 |
| 10 | 创建不可移动 contracts-v0.3.0 | yijie-contracts | 同一 candidate 已验证 | 不移动 tag |
| 11 | 两端验证 tag provenance 并切 release pin | API/Desktop | digest 不变 | 回退未发布 consumer |
| 12 | API provider first，Desktop 灰度 | release owner | G5 approval | flag off / safe rollback |
| 13 | 登记 supported baseline 并复跑 FEAT-124 G4 | yijie/contracts | 观察通过 | G4 保持 blocked |

## 9. 实际检查证据

| 检查 | Command | CWD | SHA/版本 | Exit code | 结果 | 证据位置 |
|---|---|---|---|---:|---|---|
| current remote/tag provenance | `git ls-remote origin ...` | yijie-contracts | v0.2.0 | 0 | PASS 2026-08-01 | tag object `c6e8577...`→`f16a497...` |
| candidate Public source digest | `shasum -a 256 openapi/public/public.yaml` | yijie-contracts | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 0 | PASS | `7bd40dd1c5a53cc1dcd317e3a64bf7189170fd7f575b25bb07f0eb243d0319ed` |
| generate | `make generate` | yijie-contracts | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 0 | PASS | generated Go/TS current |
| lint/test/build/pack | repository commands | yijie-contracts | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | 0 | PASS | Node 16/16、Go PASS、tarball `43a54d7f9f01edd6b50adcebb8c3b4b645dab7ec8cf4aafe20b62d7d98718565` |
| breaking | baseline command above | yijie-contracts | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` vs `f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | PASS | no breaking in all four check families |
| semantic equality | Node structured comparison | yijie-contracts | candidate vs v0.2.0 | 0 | PASS | old paths/schemas/security/servers unchanged；Runtime projection only bundle version changed |
| API exact source/generated pin | `make generate-check` | yijie-api | contracts `9ec34abd...` / oapi-codegen v2.7.2 | 0 | PASS | source `7bd40dd...`；API types `a1801a...`；CI exact checkout |
| producer conformance | canonical fixtures + handler/fault/integration tests | yijie-api | `360a526b679147472e7cc82ca7ac9db9d18a371d` | 0 | PASS | 0/1/multiple tenants、ready/empty、400/401/403/500/503、no-store/challenge/retry、2×2 DB projection |
| Desktop native auth/transport boundary | `make lint/test/build`、docs/native build、npm/cargo/license audits、structured review | yijie-desktop | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | 0 | PASS | exact loopback/PKCE/state/nonce、Keychain lifecycle、fixed two GET operations、zero token IPC/generic proxy；真实 provider/cross-repo NOT RUN |
| consumer conformance | `pnpm generate:check` + canonical fixture/fault/concurrency/security tests | Desktop | `5c4600f8308d55be5596e7c45215e88c7411f286` | 0 | PASS | exact contracts `9ec34abd...`；generated TS `77babb...`；80 frontend tests；S7 cross-repo still NOT RUN |

## 10. Consumer Owner 评审

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| yijie-api / 段成威 | G2A/S4 approved；exact pin、foundation、endpoints 与 producer/fault conformance committed/reviewed/remote verified | 2026-08-01 | `360a526b679147472e7cc82ca7ac9db9d18a371d`；staging/cross-repo remains S7 |
| yijie-desktop / 段成威 | S5A native OIDC/Keychain/operation-scoped transport 与 S5B exact generated consumer/store 均 approved、reviewed、remote verified | 2026-08-01 | S5A `3798c67d...`；S5B `5c4600f8308d55be5596e7c45215e88c7411f286`；consumer conformance PASS；S6/S7 NOT RUN |
| unknown-public / 段成威 | Conservative structural/semantic compatibility PASS | 2026-08-01 | all existing Public operations/schemas unchanged |
| yijie-agent-host / Runtime Owner | Regression comparison PASS；no migration | 2026-08-01 | projection identical except bundle version；Host remains v0.2.0 |
