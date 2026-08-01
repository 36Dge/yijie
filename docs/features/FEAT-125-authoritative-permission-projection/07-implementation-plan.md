# FEAT-125 原子实施计划

## 1. 实施原则

- 一次只完成一个可独立验证的安全行为；每个 slice 固定 base/full SHA。
- 先建立失败证据，再做最小实现；auth/RBAC 不允许 production mock。
- 先 G1/G2，后 Contracts candidate；先 G2A，后 provider/consumer。
- 不夹带现有 Tasks breaking hardening、依赖升级、Admin UI、Runtime 或全仓格式化。
- 每个仓库独立分支、提交、PR、review 和远端完整 SHA。
- 范围、身份、tenant、错误或 migration 语义变化时回到设计，不静默扩张。
- G1/G2 已批准本计划列明的代码与 expand migration 范围；S1/S2 已完成不可变 Contracts
  candidate，G2A 已于 2026-08-01 通过。S3/S4 API 与 S5A Desktop native boundary 均已
  分别批准、提交、结构化审查、推送并远端核验。G3 通用模板/预检与关闭态基线已提交；
  段成威于 2026-08-01 进一步批准 A7 / G3-NP-LOCAL，以本地 Keycloak、专用 PostgreSQL、
  Caddy、显式 CA 和 synthetic bootstrap 替代当前工程阶段的外部资源前置。当前三仓静态
  实现/门禁、local stack、HTTPS synthetic user provisioning、offline ready、API bootstrap 与
  core online 已完成；API local-only 显式 CA pin 未修改系统 Keychain。G3 为
  PASS；S5B 已单独批准、完成并远端核验，feature 仍关闭；生产
  IdP/config、tag 与激活仍需后续对应 gate/指令。

2026-08-01 段成威批准当前里程碑为 `Local Engineering Baseline Complete / Production
Activation Blocked`：S7 在真实 blocker 证据处冻结，不继续扩展本地模拟。首页、聊天、Tasks
等业务需求可以在 flags 默认关闭且仅使用合成 identity/tenant/permission 数据的边界内继续；
真实部署整个 yijie 前必须恢复 S7 并完成生产级身份安全链路，之后才可进入 G4/G5/G6。

## 2. 依赖 DAG

```text
S0 security decisions + ADR（Complete）
  → G1/G2（Passed 2026-07-31）
  → S1 Contracts source/fixtures/generated candidate（Complete: ab5e71db...）
  → S2 Contracts gates + local final candidate full SHA（Complete: 9ec34abd...）
  → remote candidate availability（Complete: origin/develop = 9ec34abd...）
  → G2A（Passed 2026-08-01）
  ├─→ S3 API exact pin + expand migration + authn/tenancy/RBAC（Complete: fff0cbcba601...）
  │     → S4 API capability endpoint + producer conformance（Complete: 360a526b6791...）
  └─→ S5A Desktop native OIDC/loopback/Keychain + operation-scoped transport boundary（Complete: 3798c67d2602...）
S4 + S5A
  → G3-NP generic template/preflight/local flag-off baseline（Complete: infra 2f01f22...）
  → G3-NP-LOCAL Keycloak/PostgreSQL/Caddy + bootstrap + explicit CA（static/local stack/offline ready/bootstrap complete）
        → API local-only explicit CA pin + API startup/readiness + core online PASS
        → S5B Desktop exact pin + permission client/store（Complete: f94ac343881b...）
          → S6 Desktop nav/router/AppShell/Settings production wiring
S4 + S6
  → Local Engineering Baseline（Complete；business development may continue；flags off）
  → S7 cross-repo security/E2E（FROZEN：真实部署准备时恢复；当前有 `nbf` + signed Keychain/provider family blockers）
  → contracts-v0.3.0 immutable tag + tag provenance
  → API provider first + Desktop canary
  → S8 FEAT-124 G4-001 close + independent G4
```

## 3. 实施切片

| Slice | 主要意图 | AC | Repository | 允许修改 | 禁止修改 | 前置 | 验证命令 | 回滚 |
|---|---|---|---|---|---|---|---|---|
| S0 | 批准 direct IdP JWT、tenant header、RBAC、Desktop native auth、Settings/root route 与 Tasks disposition | all design | yijie | FEAT-125 00—07、ADR-0012 | 业务代码、migration、生产外部注册 | G0 | package check + A1—A6 human approval | 回到 G0/G1 重新评审 |
| S1 | 定义 tenant discovery + capability Public OpenAPI 与 canonical fixtures | AC-001—007/012/014 | yijie-contracts | public OpenAPI、fixtures、contract tests、release draft | 既有 Tasks semantics、Agent Host contract | G2 | make generate/lint/test/build | revert S1 |
| S2 | 固定最终 0.3.0 candidate、生成物与基线证据 | AC-014 | yijie-contracts+yijie evidence | generated SDK、release docs、supported provenance correction | moving tag、dirty sibling | S1 | pack + breaking baseline + diff | 不晋升 G2A |
| S3 | API exact pin、expand migration、direct IdP RS256 JWT Principal、tenancy/RBAC | AC-001/003/004/013/015/020 | yijie-api | pin/check scripts、JWT/JWKS verifier（含固定 audience `https://api.yijie.ai`）、identity/tenancy/authorization modules、migration、tests | opaque Yijie session、client-trusted tenant、Tasks contract change、生产 secret | G2A | make lint/test/test-all + drift | flag off / app rollback |
| S4 | 实现 `GET /v1/me/tenants`、read-only projection、tenant header、稳定错误与 metrics | AC-001—005/013/014/020 | yijie-api | tenant discovery、0/1/multiple membership 结果、`X-Yijie-Tenant-ID` 逐请求校验、`authorization_revision`、`400 invalid_tenant_context`/403、Authorization Service projection、tests | role/menu leak、header 直信、partial projection、fail-open | S3 | API + producer conformance/fault tests | disable endpoints |
| S5A | Desktop Rust native auth + operation-scoped transport boundary | AC-003/012/017/018 | yijie-desktop | `src-tauri` auth modules、Cargo manifests/lock、native opener、精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback` listener、PKCE/state/ID-token nonce validation、10m access + <2m single-flight refresh、Keychain service `ai.yijie.desktop.auth`（30d idle/90d absolute、rotation/reuse-revokes-family）、固定 API HTTPS origin/method/path 的 `listMyTenants`/`getMyCapabilities` transport、tests | deep-link/embedded login、opaque session、Desktop 充当 access-JWT 权威 verifier、token IPC/普通存储、任意 URL/method/header/body、通用 native proxy、非 loopback/错误 path、生产 IdP/API origin 值 | G2A | Rust lint/test + auth/transport security matrix + Tauri smoke | revoke/delete Keychain item、feature off |
| G3-NP-LOCAL | 建立本地类生产依赖并证明 ready | AC-003/013/014/021/022；AC-017/018 完整 E2E 留在 S7 | yijie-infra+yijie-api+yijie-desktop+yijie evidence | pinned Keycloak+dedicated PostgreSQL+Caddy loopback profile；API exact issuer/dedicated DB/tracked 2×2 guard、empty inventory、migration、bootstrap revision/audit；exact native redirect config；local CA/export/pin；`feat-125-local-lab` Tasks no-handler+proxy deny；offline/online preflight；Keychain environment binding | production config/activation、真实/共享数据、insecure TLS、宽泛 redirect、S5B/UI、Tasks wire/default-profile hardening、完整 browser/Rust bearer/refresh/Keychain E2E | S4+S5A+A7；当前 CA trust 需另批 | owning repo gates + dedicated DB inventory/migration/bootstrap idempotency + Docker readiness + TLS/discovery/JWKS/API startup/readiness/unauth 401/redirect/Tasks edge+direct 404 | 停止独占宿主 API；清其 local env；flags/profile off；停止 local containers但保留 volumes；删除 local credential；不动 default API profile/production |
| S5B | Desktop exact pin、generated contract adapter/store | AC-006/007/011/012/014 | yijie-desktop | generate/pin、生成 TypeScript 类型/固定 adapter、tenant discovery、0 tenant→Settings/1 tenant auto/multiple chooser、capability domain/store/tests、operation intent 与 tenant UUID adapter | hand-written wire DTO、读取/传递 access token、LocalStorage token/cap、server-session tenant switch、通用 proxy | G3-NP-LOCAL PASS + separate S5B approval + S4 + S5A | make lint/test/build | keep feature off |
| S6 | Nav/router/AppShell/Settings production wiring | AC-008—012/019 | yijie-desktop | navigation/router/AppShell/Settings recovery/tenant chooser/denied pages/tests/design docs；root 按 `task.create→/chat`、`task.read→/tasks`、else `/settings` | backend policy、未批准 native surface、无条件 `/chat`、实例化 denied protected page | S5B | Desktop quality + browser/Tauri | feature off/roll-forward |
| S7 | 真实部署前恢复：最终 candidate 的 2 roles × 2 tenants E2E、native-auth/security、migration、performance | all Must/NFR | all affected repos | test harness/evidence only + fixes in slice scope | skip/only/weaken assertions；用前端布尔假装权威 E2E | Local Engineering Baseline + production IdP/signing resources | full matrix | no tag/release |
| S8 | Tag/provenance、provider-first release evidence、FEAT-124 G4 | AC-016 | contracts/API/Desktop/yijie | release docs/pins/evidence/FEAT-124 report | move tag、提前关闭 G4 | S7 PASS + G5 approval | tag digest + smoke + independent G4 | stop rollout/keep G4 blocked |

S0/G1/G2 已批准 direct IdP JWT、native opener、精确 ephemeral loopback listener、Rust
token memory、macOS Keychain 与对应最小依赖方向。S3/S5A 实现时仍须锁定 exact dependency
版本并完成 advisory/license/audit。超出该清单的 Tauri plugin/capability/command、任意
URL opener、非 loopback listener、WebView token、生产 IdP/API origin/CSP 或 yijie-infra
变更必须回到 scope approval；access JWT audience 已固定 `https://api.yijie.ai`，具体生产
生产 IdP vendor、issuer、client ID、JWKS、domain/TLS/CSP 保持 G5 决策；本地值由 A7 固定。
本地 Keycloak 仅能形成 rotation 证据，reuse-revokes-family 是恢复 S7/G5 时的生产激活
blocker，不阻断当前本地工程基线与后续业务代码开发。

## 4. 跨仓顺序

| 阶段 | Repository | Branch/base full SHA | 输出 | 下游 Pin | Owner |
|---|---|---|---|---|---|
| Governance | yijie | develop / `ef0f50e...` | approved feature+ADR | all PRs link Feature | 段成威 |
| Contract | yijie-contracts | develop / base `5320c302...` → remote `9ec34abd...` | 0.3.0 candidate SHA/digest/generators；origin/develop verified | API/Desktop exact SHA | 段成威 |
| Provider | yijie-api | develop / S3 remote `fff0cbcba601...` → S4 remote `360a526b6791...` | tenant discovery/projection endpoints、stable faults、metrics、producer conformance；flag off | exact `9ec34abd...` | 段成威 |
| Consumer | yijie-desktop | develop / S6 final `688fb72ddf...` → S7 freeze baseline `155854cf3662384caa2c8bffe0a47935ef4a70b5` remote | native auth/generated store/S6 UI + refresh cleanup complete；local engineering baseline complete；S7 frozen at provider/signing prerequisites | exact contracts candidate unchanged；UI flag default off | 段成威 |
| Nonproduction preparation | yijie-infra | develop / remote `2f01f22b46f313f8ff0b9973e417f7ccae654318` | safe generic template、strict/online preflight、runbook；local migration/flag-off smoke PASS | contracts/API/Desktop fixed full SHA | 段成威 |
| Local production-like environment | Infra+API+Desktop | Infra `298192e386...` / API `faeb78019d...` / Desktop `446b4d6085...`；完整 SHA 见 `feature.yaml` | static implementation/gates + local stack + HTTPS synthetic user provisioning + offline ready + synthetic API bootstrap complete；API local-only explicit CA pin 与 core online PASS | A7 + same contracts candidate；三个 `origin/develop` 已核验 | 段成威 |
| Integration | all | API `faeb780...` + Desktop `155854cf...` + Infra `f040492e...` remote | local baseline recorded；refresh fault fix PASS；bearer/Keychain blocker evidence；2×2/perf deferred until deployment preparation | no planned tag until resumed S7 PASS | 段成威 |
| Activation | contracts→API→Desktop | release manifests | v0.3.0 supported + canary | tag/digest verified | 段成威 |
| Linked review | yijie + Desktop | final Desktop SHA | FEAT-124 G4-001 closed/reviewed | final SHA | 段成威 |

## 5. Migration 实施序列

| Phase | 代码/数据动作 | 兼容要求 | 验证 | 停止/回滚点 |
|---|---|---|---|---|
| Expand | 新 auth/tenant/RBAC 表、复合约束、必要 audit schema | 旧 API 能在 expanded schema 启动 | S3 PostgreSQL 16.14 empty/current + existing 00001 migration PASS | app rollback，保留 expand |
| Bootstrap | 受控幂等命令写 synthetic/staging owner/tenant/roles | 不在 migration 写真实主体 | duplicate/failure/audit | revoke/compensate |
| Switch | provider flag on for internal tenant | old Desktop unaffected；new Desktop still off | API conformance+metrics | provider flag off |
| Consumer enable | Desktop canary 调用 endpoint | API 已部署且兼容 | 2×2 E2E/smoke | Desktop flag off |
| Contract | 第一版不删除旧结构 | rollback window intact | observation | future feature only |

existing Tasks 在 FEAT-125 中执行双隔离而不做契约变更：

1. `yijie-contracts` 不修改既有 Tasks operation、request `tenant_id` 或 error semantics；
2. 默认 API profile 保留 legacy Tasks wire；本地 `feat-125-local-lab` 和未来获批宿主
   profile 不注册对应 handlers，对应 ingress 拒绝 legacy 路由；FEAT-125 Desktop 同时不调用 Tasks；
3. `FEAT-126` 单独完成 consumer inventory、breaking 分类、tenant scope/auth hardening；
4. 临时例外在 FEAT-126 生产启用或 2026-09-30（取较早者）到期；到期未完成不得
   开放 Tasks，必须重新审批，不能以 FEAT-125 投影替代业务 API 授权。

## 6. 每个 Codex 任务的固定 Context

```text
Feature ID / Slice ID: FEAT-125 / Sx
角色：Planner / Implementer / Tester / Reviewer（同一人也必须分离 pass）
当前 Repository、Branch 与 Base Full SHA:
权威输入路径与不可变版本:
目标及对应 AC/NFR:
允许修改目录:
禁止修改目录:
真实验证命令:
证据输出位置:
停止条件:
最终报告格式: diff 摘要、完整 SHA、命令/exit、未验证项、风险、下一 gate
```

每个任务开始必须重读项目 memory、目标仓 AGENTS/README/SECURITY/CONTRIBUTING 和本
Feature 的 00—07；先检查 `git status --short --branch`、branch、remote、full SHA。

## 7. Commit/PR 计划

| Commit/PR | 单一目的 | Files/Repo | Test evidence | Cross-link |
|---|---|---|---|---|
| C0-yijie | FEAT-125 audited package + approved ADR | yijie docs | package G2 + review | FEAT-124 G4-001 |
| C1-contracts | add tenant/capability contracts、fixtures 与 generated SDK | yijie-contracts | generate/lint/test/build | FEAT-125 S1 |
| C2-contracts | finalize candidate/release/baseline evidence | yijie-contracts docs/generated | pack+breaking+semantic review | candidate SHA |
| C3-api | exact contracts pin + authoritative direct IdP access-JWT/RBAC foundation | yijie-api | lint/test/test-all/drift | candidate SHA |
| C4-api | tenant discovery + projection endpoints + conformance/observability | yijie-api | auth/tenant/fault tests | contract operations |
| C5A-desktop | native system-browser OIDC/exact loopback/Keychain/token lifecycle + operation-scoped transport boundary | yijie-desktop Rust/Tauri | auth/transport security、unit、native smoke | approved A1/A2 |
| C-G3-infra | nonproduction public-config contract + offline/online preflight + runbook | yijie-infra | lint/test/template + local migration/flag-off smoke | contracts/API/Desktop full SHA |
| C5B-desktop | exact pin + generated contract adapter + tenant selection + permission store | yijie-desktop | unit/contract/concurrency | candidate SHA |
| C6-desktop | deny-by-default nav/router/AppShell/recovery | yijie-desktop | DOM/router/browser/Tauri | FEAT-124 |
| C7-integration | cross-repo evidence and required fixes | scoped repos+yijie | 2×2/E2E/migration/perf | final candidates |
| C8-release | tag pins/supported baseline/release evidence | contracts/API/Desktop/yijie | provenance+smoke | G5/G6 |
| C9-feat124 | close G4-001 and independent G4 | yijie + fixed Desktop SHA | review commands | FEAT-124 |

用户已授权并完成 S1/S2 的 C1/C2 提交与 push；最终 candidate 已远端核对。S3 C3、S4 C4、
S5A C5A、S5B C5B 与 S6 C6 均已实现、结构化审查、提交、push 并远端核验。S7 C7 已执行到
本地真实 bearer/Keychain 前置并判定 BLOCKED；现按批准的本地工程里程碑冻结，真实部署准备
时恢复。S7 收口实现已提交并远端核验为 Desktop `155854cf3662384caa2c8bffe0a47935ef4a70b5`
与 Infra `f040492e7c4af4aa7cc94a343140c58befae3af2`；tag、部署以及 S8 未执行。

## 8. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | N/A | A1—A6 architecture/security/scope decisions approved；no implementation | package G0 + human approval evidence | three-way design audit complete | Complete；G1/G2 Passed |
| S1 | `ab5e71db6e4d61eb9c761446066142de2edbb444` | Public OpenAPI 0.3.0、fixtures、contract tests、TS/Go generated SDK、release draft | generate/lint/test/build PASS | 新 operations 的 auth/tenant/error/cache/schema 语义审查 PASS | Complete / local commit |
| S2 | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | candidate provenance、supported baseline、SHA/digest/generator 证据 | pack + `f16a497...` breaking check + structured semantic review PASS | 旧 Public paths/schemas/global security/servers 不变；Runtime 仅 bundle version 0.2.0→0.3.0 | Complete / remote verified |
| S3 | `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` | exact pin/CI、migration v2、bounded RS256 JWT/JWKS、identity/tenancy/authorization modules、tests | `make generate-check/lint/test/test-integration` + govulncheck PASS；source/generated/migration digests fixed | six-dimension structured review：P0/P1/P2=0；P3 SHA-format hardening resolved；independent G4 pending | Complete / remote verified |
| S4 | `360a526b679147472e7cc82ca7ac9db9d18a371d` | default-off access endpoints、tenant discovery、atomic RBAC projection、stable errors/headers、revision/expiry、bounded metrics、CI fixture path | generate/lint/race/coverage/PostgreSQL integration/canonical producer+fault conformance/govulncheck PASS | P1 lifecycle context + P2 duplicate Authorization/exact audience fixed；open P0/P1/P2=0；independent G4 pending | Complete / remote verified |
| S5A | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | system-browser OIDC、exact loopback、PKCE/state/nonce/RS256/at_hash、Rust-memory access、Protected Data Keychain refresh lifecycle、two operation-scoped transports、default-off flag | frontend 37 + Rust 27 tests；lint/build/docs/debug `.app/.dmg`；npm/cargo/license/security matrix PASS | 6 类 review finding 已修复；open P0/P1/P2=0；EXC-125-002 限定 verifier-only candidate；independent G4 pending | Complete / remote verified；real IdP/provisioning NOT RUN |
| G3-NP generic preparation | `yijie-infra@2f01f22b46f313f8ff0b9973e417f7ccae654318` | safe template、exact full-SHA pins、strict template/ready validator、bounded read-only online preflight、runbook；existing local Compose dependencies and migration 2 | template validation + 19 tests PASS；PostgreSQL migration/status PASS；nonproduction API health/ready PASS；projection endpoint 404 PASS | 生产/真实数据/secret/activation 均未进入；该外部环境流程已由 A7 的本地工程路径取代，但仍保留为未来选项 | Preparation Complete / remote verified；不等于 G3-NP-LOCAL PASS |
| G3-NP-LOCAL | API `faeb78019d...` / Desktop `446b4d6085...` / Infra `298192e386...` | pinned local images/config、API exact local profile/dedicated DB/tracked-matrix guard + audited/idempotent bootstrap + local Tasks profile、Desktop explicit CA + Keychain environment binding、Infra strict local profile/preflight | API/Desktop gates and Infra 71/71 + lint/Compose/shell/diff PASS；Keycloak/PostgreSQL/Caddy healthy；exact realm + two clients + canonicalized scope sets + explicit `userinfo.token.claim=false` mapper + strict managed `data_classification` user profile（Keycloak 26.7 REST omitted field = unmanaged disabled）+ exactly two synthetic users + password resets + refresh revocation `invalid_grant` conform；dedicated API DB empty inventory/migration 1→2/fixed 2×2 first+idempotent/revision/audit PASS；HTTPS provisioning/final offline ready PASS | API local-only explicit CA pin；core online discovery/JWKS/callback、health/ready、两个 401、Tasks edge+direct 404 PASS；provider family reuse `NOT RUN` in S7/G5；三仓 remote verified | PASS；S5B subsequently approved and complete |
| S5B | final `f94ac343881b0f7df59c0f5f4169372e612fd019`（implementation `5c4600f...`；CI path fix `942df58...`） | exact contract/generator lock、generated TypeScript、fixed adapter、0/1/multiple tenant state、operation intent、revision/expiry/context validation、memory fail-closed store | generation drift + canonical contract/fault/concurrency/security；frontend 12 files/80 tests；Rust 36 tests；lint/build/docs/debug app+dmg/audits/peers PASS | S5B-REV-001—006 resolved；open P0/P1/P2=0；S5A-REV-OPEN-001 remains outside S5B | Complete / remote verified；feature off；no S6/UI/Tasks/Rust lifecycle/production change |
| S6 | implementation `cf0e080e4cf2fa10e1394aead67c669574714a4d`；final `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` | exact default-off UI flag、total capability nav policy、lazy guarded `/chat`/`/tasks`、Settings 0/1/multiple tenant recovery、denied page、foreground refresh | generation drift；18 frontend files/113 tests；36 Rust tests；lint/build/docs/browser/debug app+dmg/npm+RustSec+license PASS | S6-REV-001—005 resolved；open P0/P1/P2=0；real bearer/Keychain/cross-repo remains S7 | Complete / remote verified；no Tasks/Rust lifecycle/production change |
| S7 | Desktop `155854cf3662384caa2c8bffe0a47935ef4a70b5` / Infra `f040492e7c4af4aa7cc94a343140c58befae3af2` | real system-browser Code+PKCE/exact loopback bearer harness；CA trust 修正；Keycloak `basic/sub` 与 synthetic names migration；refresh fail-closed cleanup；isolated Keychain smoke | Desktop lint/test/build PASS（113 frontend、38 Rust PASS + 1 intentional ignored）；Infra lint/test PASS（76 tests）；API lint/race unit+integration PASS；offline/online preflight PASS；bearer fails before API matrix on access JWT `not_before_missing`；Keychain fails `-34018`/0 signing identities | `S5A-REV-OPEN-001` resolved；P0=0；provider `nbf`、signed Keychain、family reuse remain production blockers；两个 origin/develop SHA verified | FROZEN after BLOCKED evidence / remote verified / resume before deployment / no tag or release |
| S8 | N/A | No release/FEAT-124 changes | NOT RUN | N/A | Pending |

## 9. 变更控制

| 变化 | 回到 |
|---|---|
| 用户行为/AC、Settings/default route 变化 | `01-requirements.md` |
| 身份/IdP/session/tenant/仓库边界变化 | `02-impact-assessment.md` + ADR |
| RBAC、审批、审计、secret/CSP 风险变化 | `03-decisions-and-risks.md` |
| security scheme、errors、capability/Tasks 语义变化 | `04-contract-change-plan.md` |
| DB schema、state、TTL、架构变化 | `05-technical-design.md` |
| 测试/SLO/环境变化 | `06-test-plan.md` |
| slice/deploy/rollback 变化 | 本文件与 `09-release-and-rollback.md` |

## 10. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 技术负责人 | 段成威 | Approved A1—A6；G1/G2 Passed，授权按本计划进入 S1；G2A Pending | 2026-07-31 |
| 技术负责人 | 段成威 | 授权执行 S1/S2 并 push；candidate、门禁与远端可用性完成；G2A 仍 Pending | 2026-08-01 |
| 技术负责人 | 段成威 | G2A Passed；固定 candidate `9ec34abd6e7dfb5a23b0154d467694167224ebbb`，授权 S3；不生产激活 | 2026-08-01 |
| 技术负责人 | 段成威 | 授权 S3 push 与 S4 provider；S4 仅 yijie-api endpoints/conformance/metrics，禁止 Desktop、Tasks contract、生产 IdP 配置与激活 | 2026-08-01 |
| 技术负责人 | 段成威 | 授权 S5A；仅 yijie-desktop Rust/Tauri native OIDC/Keychain/operation-scoped transport，完成安全矩阵、结构化审查、全部门禁并 push；禁止 S5B/UI、Tasks、生产 IdP 配置与激活 | 2026-08-01 |
| 技术负责人 | 段成威 | 授权执行 G3 非生产环境准备；完成供应商中立、默认关闭、合成数据模板/预检、本地 migration 与关闭态 smoke；真实 IdP/DNS/TLS/API origin 和 online preflight 不得伪造为通过 | 2026-08-01 |
| 技术负责人 | 段成威 | 批准 A7 / G3-NP-LOCAL：允许 loopback/Docker/synthetic Keycloak、专用 PostgreSQL、Caddy、本地 CA、API bootstrap/Tasks profile 与 Desktop Keychain binding；禁止 insecure TLS、真实数据、生产配置/激活；全部门禁与 offline/online preflight PASS 后才可另行批准 S5B | 2026-08-01 |
| 技术负责人 | 段成威 | G3 收口时点：静态实现/门禁、local stack/live realm、HTTPS synthetic user provisioning、offline ready 与 API bootstrap 已完成；core online 与最终门禁 PASS，登记 G3 PASS；该时点 S5B 仍须单独批准 | 2026-08-01 |
| 技术负责人 | 段成威 | S5B/S6 已远端核验；随后授权 S7 本地 2×2/bearer/Keychain 集成。Tasks 契约、生产配置/激活与 S8 继续禁止 | 2026-08-01 |
| 技术负责人 | 段成威 | 批准 Local Engineering Baseline Complete / Production Activation Blocked；冻结 S7，允许首页/聊天/Tasks 使用本地合成权限继续开发；flags 默认关闭；真实部署前恢复完整生产身份链路和 S7/G4/G5/G6 | 2026-08-01 |
