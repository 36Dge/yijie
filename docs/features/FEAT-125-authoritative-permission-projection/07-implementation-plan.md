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
  分别批准、提交、结构化审查、推送并远端核验。S5B+、生产 IdP 注册/config、tag 与部署
  仍需后续对应 gate/指令。

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
        → S5B Desktop exact pin + permission client/store
          → S6 Desktop nav/router/AppShell/Settings production wiring
S4 + S6
  → S7 cross-repo security/E2E against final candidate
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
| S5B | Desktop exact pin、generated contract adapter/store | AC-006/007/011/012/014 | yijie-desktop | generate/pin、生成 TypeScript 类型/固定 adapter、tenant discovery、0 tenant→Settings/1 tenant auto/multiple chooser、capability domain/store/tests、operation intent 与 tenant UUID adapter | hand-written wire DTO、读取/传递 access token、LocalStorage token/cap、server-session tenant switch、通用 proxy | G2A + S4 staging + S5A | make lint/test/build | keep feature off |
| S6 | Nav/router/AppShell/Settings production wiring | AC-008—012/019 | yijie-desktop | navigation/router/AppShell/Settings recovery/tenant chooser/denied pages/tests/design docs；root 按 `task.create→/chat`、`task.read→/tasks`、else `/settings` | backend policy、未批准 native surface、无条件 `/chat`、实例化 denied protected page | S5B | Desktop quality + browser/Tauri | feature off/roll-forward |
| S7 | 最终 candidate 的 2 roles × 2 tenants E2E、native-auth/security、migration、performance | all Must/NFR | all affected repos | test harness/evidence only + fixes in slice scope | skip/only/weaken assertions；用前端布尔假装权威 E2E | S4+S6 | full matrix | no tag/release |
| S8 | Tag/provenance、provider-first release evidence、FEAT-124 G4 | AC-016 | contracts/API/Desktop/yijie | release docs/pins/evidence/FEAT-124 report | move tag、提前关闭 G4 | S7 PASS + G5 approval | tag digest + smoke + independent G4 | stop rollout/keep G4 blocked |

S0/G1/G2 已批准 direct IdP JWT、native opener、精确 ephemeral loopback listener、Rust
token memory、macOS Keychain 与对应最小依赖方向。S3/S5A 实现时仍须锁定 exact dependency
版本并完成 advisory/license/audit。超出该清单的 Tauri plugin/capability/command、任意
URL opener、非 loopback listener、WebView token、生产 IdP/API origin/CSP 或 yijie-infra
变更必须回到 scope approval；access JWT audience 已固定 `https://api.yijie.ai`，具体生产
IdP vendor、issuer、client ID、JWKS、domain/TLS/CSP 保持 G3/G5 决策。

## 4. 跨仓顺序

| 阶段 | Repository | Branch/base full SHA | 输出 | 下游 Pin | Owner |
|---|---|---|---|---|---|
| Governance | yijie | develop / `ef0f50e...` | approved feature+ADR | all PRs link Feature | 段成威 |
| Contract | yijie-contracts | develop / base `5320c302...` → remote `9ec34abd...` | 0.3.0 candidate SHA/digest/generators；origin/develop verified | API/Desktop exact SHA | 段成威 |
| Provider | yijie-api | develop / S3 remote `fff0cbcba601...` → S4 remote `360a526b6791...` | tenant discovery/projection endpoints、stable faults、metrics、producer conformance；flag off | exact `9ec34abd...` | 段成威 |
| Consumer | yijie-desktop | develop / base `be01cc2d...` → S5A remote `3798c67d2602...` | native auth boundary complete；generated adapter/store/UI pending | same contracts candidate in S5B | 段成威 |
| Integration | all | fixed candidates | conformance/E2E/perf evidence | planned tag resolves same SHA | 段成威 |
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
2. production public ingress 拒绝 legacy Tasks 路由，且 `yijie-api` 服务不注册对应
   handlers；FEAT-125 Desktop 同时不调用 Tasks；
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
| C5B-desktop | exact pin + generated contract adapter + tenant selection + permission store | yijie-desktop | unit/contract/concurrency | candidate SHA |
| C6-desktop | deny-by-default nav/router/AppShell/recovery | yijie-desktop | DOM/router/browser/Tauri | FEAT-124 |
| C7-integration | cross-repo evidence and required fixes | scoped repos+yijie | 2×2/E2E/migration/perf | final candidates |
| C8-release | tag pins/supported baseline/release evidence | contracts/API/Desktop/yijie | provenance+smoke | G5/G6 |
| C9-feat124 | close G4-001 and independent G4 | yijie + fixed Desktop SHA | review commands | FEAT-124 |

用户已授权并完成 S1/S2 的 C1/C2 提交与 push；最终 candidate 已远端核对。S3 C3、S4 C4
与 S5A C5A 均已实现、结构化审查、提交、push 并远端核验。PR、tag、部署以及 S5B+ 未执行。

## 8. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | N/A | A1—A6 architecture/security/scope decisions approved；no implementation | package G0 + human approval evidence | three-way design audit complete | Complete；G1/G2 Passed |
| S1 | `ab5e71db6e4d61eb9c761446066142de2edbb444` | Public OpenAPI 0.3.0、fixtures、contract tests、TS/Go generated SDK、release draft | generate/lint/test/build PASS | 新 operations 的 auth/tenant/error/cache/schema 语义审查 PASS | Complete / local commit |
| S2 | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | candidate provenance、supported baseline、SHA/digest/generator 证据 | pack + `f16a497...` breaking check + structured semantic review PASS | 旧 Public paths/schemas/global security/servers 不变；Runtime 仅 bundle version 0.2.0→0.3.0 | Complete / remote verified |
| S3 | `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` | exact pin/CI、migration v2、bounded RS256 JWT/JWKS、identity/tenancy/authorization modules、tests | `make generate-check/lint/test/test-integration` + govulncheck PASS；source/generated/migration digests fixed | six-dimension structured review：P0/P1/P2=0；P3 SHA-format hardening resolved；independent G4 pending | Complete / remote verified |
| S4 | `360a526b679147472e7cc82ca7ac9db9d18a371d` | default-off access endpoints、tenant discovery、atomic RBAC projection、stable errors/headers、revision/expiry、bounded metrics、CI fixture path | generate/lint/race/coverage/PostgreSQL integration/canonical producer+fault conformance/govulncheck PASS | P1 lifecycle context + P2 duplicate Authorization/exact audience fixed；open P0/P1/P2=0；independent G4 pending | Complete / remote verified |
| S5A | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | system-browser OIDC、exact loopback、PKCE/state/nonce/RS256/at_hash、Rust-memory access、Protected Data Keychain refresh lifecycle、two operation-scoped transports、default-off flag | frontend 37 + Rust 27 tests；lint/build/docs/debug `.app/.dmg`；npm/cargo/license/security matrix PASS | 6 类 review finding 已修复；open P0/P1/P2=0；EXC-125-002 限定 verifier-only candidate；independent G4 pending | Complete / remote verified；real IdP/provisioning NOT RUN |
| S5B | N/A | No Desktop permission client/store changes | NOT RUN | N/A | Pending |
| S6 | N/A | No Desktop changes | NOT RUN | N/A | Pending |
| S7 | N/A | No integration changes | NOT RUN | N/A | Pending |
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
