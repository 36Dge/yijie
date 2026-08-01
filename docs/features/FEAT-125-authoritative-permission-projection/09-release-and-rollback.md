# FEAT-125 发布、灰度与回滚 Runbook

> 本 Runbook 是候选计划，不是部署授权。A1—A6 已批准 direct IdP RS256 JWT、required
> `X-Yijie-Tenant-ID`、RBAC/Settings core 与 Tasks isolation 边界；S4 API producer 与 S5A
> Desktop native boundary 已远端核验但默认关闭，尚未进入 staging/production。具体 IdP
> provider、issuer/client/JWKS、生产平台、domain、
> secret、命令和 artifact 尚未形成，G3/G5 前必须固定并替换为真实、经段成威确认的配置
> 与控制面操作。

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| yijie-contracts | 0.3.0 candidate；planned `contracts-v0.3.0` tag | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | source `7bd40dd1c5a53cc1dcd317e3a64bf7189170fd7f575b25bb07f0eb243d0319ed`；TS `77babb215608c6ace4468d37b72fc8e43f5758231c7807a4301063cb156ae8e0`；Go `01d31efc1b1c3fb69e18c853d67ea12cdc313c2709f2a02d02e2a01b6ff4d253`；tarball `43a54d7f9f01edd6b50adcebb8c3b4b645dab7ec8cf4aafe20b62d7d98718565` | openapi-typescript 7.13.0 / oapi-codegen 2.7.2 | origin/develop verified；tag/publish pending |
| yijie-api | S4 remote candidate；no release | `360a526b679147472e7cc82ca7ac9db9d18a371d`；origin/develop verified | generated types `a1801a...` | exact contracts `9ec34abd...` / oapi-codegen v2.7.2 | local producer/conformance/fault PASS；flag off；staging/production NOT RUN |
| yijie-desktop | S5A remote candidate；no release | `3798c67d260237928730758c7ec4c1fbe6fcf7d2`；origin/develop verified | Cargo lock `94b1ee21...`；pnpm lock `aaa0a300...`；debug artifact unsigned/unpublished | S5A has no generated contract pin；S5B must pin exact `9ec34abd...` | local native/security gates PASS；real IdP/API、sign/notarize、staging/production NOT RUN |
| DB schema | goose v2 expand candidate | yijie-api `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` | `51c4ced9b6e6fa447326c29ead582e0568541e7ffca7084ae706d71ad4cb3bc9` | N/A | local PostgreSQL 16.14 PASS；staging/production NOT RUN |
| yijie evidence | FEAT-125 / FEAT-124 G4 | final docs SHA | N/A | final manifests | governance |

## 2. 发布前提

- [x] G1 A1—A6 identity/JWT/tenant/RBAC/Settings core/Tasks isolation 决策由段成威批准（2026-07-31）
- [x] G2 semantic contract 与跨仓设计由段成威批准（2026-07-31）
- [x] S1/S2 已形成本地 0.3.0 candidate，并通过 generate/lint/test/build/pack、
      supported-baseline breaking check 与 structured semantic review（2026-08-01）
- [x] final candidate 已 push 且能从远端以完整 SHA 获取（2026-08-01）
- [x] G2A contract candidate、生成物与 S3 API foundation 由段成威批准（2026-08-01）
- [x] S3 API `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` 已 push 且远端完整 SHA 核验一致
- [x] S4 API producer 已由段成威批准；`360a526b679147472e7cc82ca7ac9db9d18a371d`
      通过 slice 结构化审查、全部门禁和 producer conformance/fault tests，已 push 并远端核验；未发布
- [x] S5A Desktop native boundary 已由段成威批准；`3798c67d260237928730758c7ec4c1fbe6fcf7d2`
      通过 OIDC/loopback/Keychain/IPC/transport security matrix、全部门禁和结构化审查，已 push
      并远端核验；native flag 默认 false；S5B/UI、真实 IdP/API、正式 Keychain provisioning 未执行
- [ ] G4 Code Complete 通过，P0/P1/P2 security findings 为 0
- [ ] Release artifact 来自干净、远端可获取、不可变 source
- [ ] v0.3.0 tag 解析到已做 API/Desktop conformance 的同一 candidate；digest 不变
- [ ] IdP、TLS/domain、JWKS、Secret Manager、API origin、CSP 与最小权限准备完成
- [ ] IdP access JWT 配置强制 RS256 且最大有效期不超过 10 分钟；refresh revoke/reuse
      在下一次刷新失败，runbook 不宣称已签发 access JWT 被即时撤销
- [ ] Migration/Bootstrap 在类生产 synthetic 环境演练
- [ ] Dashboard、告警、runbook、on-call/rollback 责任人存在
- [ ] API/Desktop feature flags 默认安全关闭
- [ ] 现有 `/v1/tasks` 与 `/v1/tasks/*` 已通过 production ingress 拒绝和 handler
      不注册/关闭完成双隔离，并有外部负向验证；wire 保持不变，FEAT-126 已登记；
      临时例外在 FEAT-126 生产启用或 2026-09-30 中较早者到期
- [ ] Desktop 签名、公证、更新渠道及回滚制品已验证
- [ ] 真实 Go/No-Go 批准已取得

## 3. 合并、部署、迁移与启用顺序

| Order | Action | Component/Environment | Operator | Preconditions | Verification | Rollback point |
|---:|---|---|---|---|---|---|
| 1 | 合并/push final contracts candidate | contracts | 段成威 | S2 checks PASS | remote SHA/digest | remain on v0.2.0 |
| 2 | 非生产 API/DB consume candidate | staging | 段成威 | G2A | migration+producer tests | app rollback/flag off |
| 3 | 非生产 Desktop consume candidate | staging/native | 段成威 | provider ready | consumer+2×2 E2E | do not release |
| 4 | 创建不可移动 v0.3.0 tag | contracts | 段成威 | candidate E2E PASS | tag→same SHA/digest | never move tag |
| 5 | API/Desktop 切 tag provenance | repos | 段成威 | tag verified | regenerate clean | retain candidate commit |
| 6 | 生产 expand migration | production | approved operator | rehearsal+backup/runbook | schema/status | pause/roll-forward |
| 7 | 对 `/v1/tasks`、`/v1/tasks/*` 启用 ingress 拒绝和 handler 不注册/关闭双隔离 | production | approved operator | FEAT-126 已登记；wire 不变；例外到期为 FEAT-126 生产启用或 2026-09-30 较早者 | 外部路径与服务内路由负向 smoke | 到期未完成不得开放 Tasks，保持隔离并重新审批 |
| 8 | 部署 API provider，flag off | production | approved operator | dependencies healthy + Tasks 双隔离 PASS | health/auth smoke | rollback API；保持 Tasks 隔离 |
| 9 | 对 internal tenant 开 API flag | production | 段成威 | metrics ready | projection/security smoke | flag off |
| 10 | 发布 Desktop canary，consumer flag scoped | canary | 段成威 | provider stable | UI/direct API smoke | stop rollout/flag off |
| 11 | 分阶段扩量并观察 | production | 段成威 | thresholds green | dashboards/audit | stop/rollback |
| 12 | 登记 supported baseline | contracts/yijie | 段成威 | rollout evidence | provenance registry | do not deprecate 0.2.0 |
| 13 | 更新 FEAT-124 candidate 并独立复跑 G4 | yijie/Desktop | Codex Reviewer + 段成威 | FEAT-125 G4 evidence | G4 report | keep finding open |

## 4. Feature Flag

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `YIJIE_API_PERMISSION_PROJECTION_ENABLED` | false | process environment；tenant 灰度控制面待 G5 | config validation→internal tenant→canary | set false；endpoint 不注册 | 段成威 |
| `YIJIE_DESKTOP_NATIVE_AUTH_ENABLED` | false | S5A process environment | G3 config validation→native test→S7 | false + revoke/delete Keychain family + clear memory | 段成威 |
| Desktop authoritative permission consumer/UI flag（S5B/S6 固定） | off / name pending | build/channel/user cohort | provider smoke→canary manifest | protected items=0 + recovery only | 段成威 |

Kill switch 禁止切回静态全显示、默认 `{}` 或硬编码 admin。若 API 关闭而 Desktop 已发布，
Desktop 必须进入 permission-unavailable 并保留 retry/logout，不显示受保护模块。

## 5. Migration/Backfill

| Phase | Command/job | Batch/lock controls | Validation | Pause/resume | Recovery |
|---|---|---|---|---|---|
| Expand schema | `go run ./cmd/migrate up` / `make migrate-up`；goose v2 | goose lock/short DDL；无真实 data seed | version+tables+constraints；S3 local rehearsal PASS | deployment job control | app rollback，schema retained；down 明确拒绝 |
| Synthetic/staging bootstrap | 由批准的幂等 CLI 固定 | one tenant/user per invocation | audit+repeat run | stop safely | revoke/compensate |
| Production bootstrap | 真实命令尚未批准 | explicit environment/actor/confirmation | tenant/user/role/audit smoke | one object at a time | revoke/roll-forward |
| Contract cleanup | first release N/A | N/A | N/A | N/A | 后续独立 feature |

不得在 migration 中写真实用户、真实 tenant 或通用默认管理员。生产命令不存在时，G5
保持 Blocked；Codex 不编造控制面命令或 secret。

## 6. 灰度计划

| Stage | Scope/tenant/% | Observation window | Success criteria | Stop threshold | Decision owner |
|---|---|---|---|---|---|
| Internal | 单个 synthetic/internal tenant | ≥30 min candidate | E2E/smoke 全过，0 leak/fail-open | 任一 auth/context mismatch | 段成威 |
| Canary | 受控真实测试 cohort；比例在 G5 固定 | ≥24 h candidate | 400/401/403/503 与 latency 在基线内 | security finding、5xx≥1%、p95>500ms | 段成威 |
| Expand | 分阶段比例，G5 固定 | 每阶段 ≥24 h candidate | 无 stale/跨租户、支持量正常 | 任一跨租户或 error spike | 段成威 |
| Full | 批准用户范围 | ongoing | SLO/审计持续达标 | runbook trigger | 段成威 |

真实 tenant 数量/比例与窗口必须在 G5 依据环境容量批准；这里的 candidate 阈值不是
生产 Go/No-Go 证据。

## 7. Smoke

| Smoke ID | 用户路径 | 输入/租户 | 预期 | 避免真实副作用方式 |
|---|---|---|---|---|
| SMOKE-000A | JWT 用户无 active membership | synthetic zero-tenant user | `/v1/me/tenants` 返回空列表；只保留 Settings core/recovery | 合成身份 |
| SMOKE-000B | JWT 用户只有一个 active membership | synthetic single-tenant user | tenant list 只含 id/name，自动选择后携带 header 拉 projection | 合成身份 |
| SMOKE-000C | JWT 用户有多个 active memberships | synthetic multi-tenant user | 显示选择器；选择前不拉 projection，选择后 API 再验 membership | 合成身份 |
| SMOKE-001 | 有 task.create 打开 `/` | synthetic allowed tenant | 到 /chat，只有允许项 | 本地输入不提交业务 |
| SMOKE-002 | 只有 task.read 打开 `/` | synthetic restricted tenant | 到独立 `/tasks` 页面；chat hidden；不调用隔离的 `/v1/tasks` API | 合成空 task view |
| SMOKE-003 | 零 capability | synthetic zero-role | Settings/recovery only | 无写操作 |
| SMOKE-004 | 有未发布模块 capability | synthetic role | item disabled“即将开放” | 无 route/调用 |
| SMOKE-005 | tenant A→B | two synthetic tenants | 先清空，B 投影正确，无 A flash | delayed response harness |
| SMOKE-006 | 400/401/403/503 | missing/invalid tenant、fault/test identities | 正确 recovery，protected=0 | test issuer/fault flag |
| SMOKE-007 | 篡改 route/direct API | synthetic denied user | capability API 由 JWT+membership 拒绝；Tasks path 由 ingress+handler 双隔离拒绝 | 只读/合成 resource |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| projection success/error | G5 建立真实 dashboard | staging/canary | candidate 5xx<0.1% | ≥1%/5min |
| latency | p50/p95/p99 | staging | p95≤300ms candidate | >500ms/5min |
| auth/tenant denial | status+reason without high cardinality | canary | 与测试 cohort 预期一致 | invalid-context spike |
| context mismatch/stale | Desktop telemetry（若获批）/test signal | 0 | 0 | >0 |
| DB/resource | pool/query/lock | staging | within capacity | saturation/lock timeout |
| security/audit | audit completeness/forbidden direct calls | 100% writes audited | no leak/bypass | any leak/bypass |

S4 已提供进程内、低基数 recorder（request count/duration 与 authorization denial）；尚无
exporter、dashboard 或告警接线。不得以进程内单元测试信号推断部署成功；G5 必须选择获批
的观测后端并验证真实查询。

## 9. 回滚决策

```text
触发停止阈值
  → 停止 Desktop 扩量
  → 关闭 Desktop/API feature flags（保持 fail-closed）
  → 判断 API endpoint 是否仍被已发布 Desktop 依赖
  → 优先 roll-forward；只有兼容时回退 API/DB app
  → 校验 JWT credential context、tenant membership、audit 和 protected UI
  → synthetic smoke + 持续观察
```

| Trigger | Immediate action | Code rollback | Data action | Verification | Escalation |
|---|---|---|---|---|---|
| 跨租户/fail-open/token leak | stop rollout、flags off、撤销相关凭证 | rollback/roll-forward security fix | 保留审计，隔离受影响 membership | SEC/E2E+log review | 段成威 |
| auth/JWKS/DB outage | Desktop protected=0、API deny | 回退 provider only if endpoint compatibility remains | no destructive data rollback | 503/recovery smoke | 段成威 |
| Desktop stale/route bypass | stop Desktop channel/flag off | roll-forward preferred | clear process/JWT-derived permission state | nav/route/direct API | 段成威 |
| migration failure | pause deploy | old app on expanded/partial safe state | follow approved migration recovery | schema status+old app smoke | 段成威 |
| contract/digest drift | stop tag/release | return to fixed candidate | none | regenerate+digest | 段成威 |
| API endpoint rollback after Desktop release | stop consumer rollout | avoid removing endpoint; deploy compatible fix | none | old/new matrix | 段成威 |

回退 Desktop 到 `be01cc2d...` 会重新产生 FEAT-124 G4-001；它只能作为紧急安全回退，
不能被称为满足 FEAT-124，且 G4 必须重新 Blocked。优先提供带 fail-closed 的 roll-forward
制品。

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Contract checks | 见 06-test-plan 第 11 节仓内命令 | repository maintainer | exit 0 + clean diff | S2 evidence |
| API producer checks | `make generate-check`、`make lint`、`make test`、`make test-integration`、`go mod verify`、`govulncheck ./...` | repository maintainer | exit 0；canonical conformance/fault fixtures PASS | S4 evidence |
| Desktop S5A checks | `make lint`、`make test`、`make build`、`pnpm docs:build`、`pnpm tauri:build --debug`、npm/cargo/license audits | repository maintainer | exit 0；37 frontend + 27 Rust tests；debug `.app/.dmg`；security matrix PASS | S5A `3798c67...` + owning-repo security matrix |
| Desktop S5B—S7 checks | 见 06-test-plan 与后续 owning-repo commands | repository maintainer | exit 0 | S5B—S7 evidence |
| Deploy | N/A：生产控制面尚未选择 | approved release role | G5 前必须登记 | release manifest |
| Disable | N/A：真实 flag/config backend 尚未批准 | approved operator | G5 前必须登记 | runbook |
| Rollback | N/A：artifact/deploy platform 尚未批准 | approved operator | G5 前必须登记 | rehearsal |

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| 2026-08-01 | isolated local PostgreSQL 16.14 | contracts `9ec34abd...`；API `fff0cbcba601...`；schema 00001→00002 | migrate existing task/audit→validate tables/catalog/FKs/append-only→reject down and retain v2 | PASS / data rehearsal only | old binary smoke、bootstrap、staging/platform deployment remain NOT RUN |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Commander/Requirement/Technical/Security/Release | 段成威 | 当前 Codex 任务与仓库评审记录 | 决策、Go/No-Go、回滚 |
| Planner/Implementer/Tester/Reviewer | Codex（按 slice 分离上下文） | Feature evidence | 起草、实现、复验、独立 finding |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G1/G2 | 段成威 | Approved A1—A6 | 2026-07-31 | 用户批准记录、03 与 05 的已批准决策 |
| G2A | 段成威 | Passed；固定 `9ec34abd...` 并授权 S3，不生产激活 | 2026-08-01 | 用户批准记录、04/08 contract/API evidence |
| S4 | 段成威 | Approved API producer only；禁止 Desktop/Tasks/生产 IdP 与生产激活 | 2026-08-01 | 用户批准记录、API `360a526b679147472e7cc82ca7ac9db9d18a371d`、08 S4 evidence |
| S5A | 段成威 | Approved Desktop Rust/Tauri native auth/transport only；禁止 S5B/UI、Tasks、生产 IdP 配置与激活 | 2026-08-01 | 用户批准记录、Desktop `3798c67d260237928730758c7ec4c1fbe6fcf7d2`、owning-repo security matrix、08 S5A evidence |
| Go/No-Go | 段成威 | Pending | G5 后 | final manifest/runbook/rehearsal |
