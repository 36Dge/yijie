# FEAT-125 交付总结与关闭记录

> 当前已到 S4 API producer + S5A Desktop native boundary + S5B consumer/store remote candidate
> 阶段，不是业务功能交付完成记录。S1—S5B 已推送并远端核验；G3-NP-LOCAL 三仓静态实现/门禁、
> local stack/live realm、HTTPS synthetic user provisioning、offline ready、synthetic API bootstrap 与
> core online 已完成。因此 G3-NP-LOCAL PASS；S5B generated consumer/store 已单独批准、
> 完成并远端核验；S6 UI、S7 E2E、发布和生产栏位继续保持 `NOT RUN / Not
> delivered`。

## 1. 最终结果

- 用户可观察行为：尚未变化；Desktop 仓当前为 S5B
  `5c4600f8308d55be5596e7c45215e88c7411f286`，
  但 native flag 默认关闭且没有 S6 UI
  接线；FEAT-124 业务界面 candidate 仍以 `be01cc2d0a1c9c4b057de616be201a4843d0a035` 为阻断基线。
- 原目标是否达成：部分；已完成 A1—A7、S1/S2 Contracts remote candidate、S3 API
  foundation、S4 tenants/capabilities HTTP producer、S5A system-browser OIDC/native boundary，
  以及已提交并远端核验的 G3 local CA/Keychain binding、bootstrap、Infra local profile 和完整
  dedicated API/core-online 链，以及 S5B Desktop generated consumer/store。尚无 S6 UI、S7 完整 auth lifecycle、
  跨仓业务 E2E 或生产链路。
- 最终范围与非目标：见 00—07；G1/G2 于 2026-07-31 Passed，G2A 于 2026-08-01 Passed。
- 交付状态：`S1—S5B Remote Verified / G3-NP-LOCAL PASS / S6+ Pending / Not delivered`。
- FEAT-124：G4-001 继续 Open，不得关闭。

## 2. 实际发布版本

| Component | Environment | Version/tag | Full commit | Artifact digest | Contract version/pin |
|---|---|---|---|---|---|
| yijie-contracts | repository remote candidate | 0.3.0 candidate；no release/tag | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | source `7bd40dd...`；tarball `43a54d7...` | candidate 0.3.0；supported release 仍 v0.2.0 |
| yijie-api | repository remote candidate / local test | S4 commit；no release | `360a526b679147472e7cc82ca7ac9db9d18a371d`；origin/develop verified | generated `a1801a...`；migration `51c4ced9...` | exact candidate `9ec34abd...` / oapi-codegen v2.7.2；feature flag false |
| yijie-desktop | repository remote candidate / local native test | S5B commit；no release | `5c4600f8308d55be5596e7c45215e88c7411f286`；origin/develop verified | generated TS `77babb21...`；pnpm lock `d80424b8...`；unsigned debug `.app/.dmg` only | native flag false；S5B exact contract pin/consumer complete；S6 UI absent |
| yijie-api G3-NP-LOCAL | repository commit / no release | exact local profile/dedicated DB/tracked bootstrap/service-profile/explicit-CA implementation | `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34`；origin/develop verified | Git commit | exact contracts `9ec34abd...` |
| yijie-desktop G3-NP-LOCAL | repository commit / no release | local CA/Keychain environment-binding baseline | `446b4d608546fca8f53f4582201d6b43ef6f762d`；origin/develop verified | Git commit | superseded by S5B candidate `5c4600f...` |
| yijie-infra G3-NP-LOCAL | repository commit / no deployment | pinned local-lab/dedicated API DB/preflight implementation | `298192e386a7f7b81e8f0f8fe733c1f79f096ab4`；origin/develop verified | pinned image digests；public CA `07a3bb2ef51a5b559fe42b423339f6c886c5e17903b1cf2d8ca26bf1b5574650` | 71/71 tests + lint/Compose/shell/diff PASS；exact implementation refs verified |
| database | dedicated local PostgreSQL 16 DB `yijie_api_feat125_local` | empty inventory + goose migration 1→2 + tracked synthetic bootstrap；not deployed | API `faeb78019d...` | migration `51c4ced9...` | final users2/identities2/tenants2/memberships4/roles4/role_permissions18/role_bindings4/tasks0；8 synthetic-only audits；no session/real seed/shared DB evidence |

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| AC-001/003/004/013/015/020 S3 foundation | PARTIAL PASS | JWT/JWKS、identity/tenancy/RBAC、2×2 matrix、migration integration | none |
| AC-014 contract candidate/pin | CONTRACT + API PIN PASS / Desktop pending | S1/S2 gates + S3 exact source/generated/generator checks | none |
| S4 API producer slice | PASS | `/v1/me/tenants`、`/v1/me/capabilities`、header 逐请求验证、稳定错误、revision、metrics recorder、canonical conformance/fault tests | none；flag default false |
| S5A Desktop native boundary | LOCAL SLICE PASS | committed S5A：system-browser OIDC、exact loopback、PKCE/state/nonce、Rust-memory access、Protected Data Keychain refresh lifecycle、two fixed GET operations；37 frontend + 27 Rust tests | none；full browser/provider/provisioned Keychain NOT RUN；flag default false |
| G3-NP-LOCAL static/offline commits | PASS / REMOTE VERIFIED | API generate/lint/race unit+integration/module/diff PASS（nonprodbootstrap integration 83.2%）+ exact local DB guard/dedicated empty DB migration/tracked bootstrap first+idempotent/inventory/audit/revision；Desktop 37 frontend + 36 Rust/local CA+Keychain binding/401-refresh race fix；Infra 71/71 + lint/Compose/shell/diff PASS；three containers healthy；read-only-before-mutation exact realm/two clients/canonicalized scope sets/explicit `userinfo.token.claim=false` mapper/strict managed `data_classification` user profile（omitted field = unmanaged disabled under Keycloak 26.7 REST）/two fixed users/password resets/refresh revocation `invalid_grant` over pinned HTTPS；final offline ready PASS | API/Desktop/Infra full commits remote verified；no release artifact or production evidence |
| G3-NP-LOCAL dedicated API/online | PASS | exit 0 | strict local-only CA pin；discovery/JWKS/callback、health/ready、两个 unauth 401、Tasks edge+direct 404 PASS |
| S5B Desktop consumer/store | PASS | Desktop `5c4600f8308d55be5596e7c45215e88c7411f286` | exact generation drift、canonical contract/fault/concurrency/security；80 frontend + 36 Rust tests；all gates/review/remote verification PASS；feature off |
| remaining AC/NFR | NOT RUN | S6 Desktop UI、S7 cross-repo and production slices pending | none |

## 4. 生产 Smoke 与观察

| Check/Metric | Window | Baseline | Actual | Threshold | Result |
|---|---|---:|---:|---:|---|
| capability success/error/latency | no deployment window | process-local recorder unit-tested only | N/A | G5 candidate | NOT RUN |
| tenant/context mismatch | none | 0 target | N/A | 0 | NOT RUN |
| unauthorized DOM/route/API | none | current G4-001 open | N/A | 0 | NOT RUN |

## 5. 安全与审计抽查

| 项目 | Trace/request/task/session 标识 | 结果 | Evidence |
|---|---|---|---|
| 授权/租户/审计/脱敏 | synthetic S3/S4 + local G3 + Desktop S5B candidates | PASS for foundation/producer/native boundary/bootstrap/consumer store：fail-closed reads、cross-tenant FK、逐请求 membership/RBAC projection、稳定错误、token IPC/transport allowlist、revision/expiry/context 与并发 stale-response 防护；S6 UI/cross-repo pending | 08 verification report + Desktop/Infra owning-repo evidence |

## 6. 发布事件、回滚与数据状态

- Incident/异常：N/A；未部署。
- 是否触发停止或回滚：否；没有可回滚 FEAT-125 artifact。
- 数据/队列/缓存最终状态：专用 `yijie_api_feat125_local` 保留 2 users × 2 tenants 合成
  auth/RBAC 与 8 条 bootstrap success audits（4 changed + 4 unchanged），tasks=0；旧 shared
  DB 演练已标记 superseded，不作为当前 G3 证据；未触碰 staging/production，未新增
  session/cache，未写真实数据。未经单独授权不删除这些本地证据。
- 回滚路径当前是否仍有效：G3 candidate 可回到 S4 base
  `360a526b679147472e7cc82ca7ac9db9d18a371d`，expand schema 与本地合成 audit 按设计保留并
  roll-forward，destructive down 明确拒绝。当前因 CA blocker 没有启动 G3 宿主 API；未来
  runtime 回滚必须先停止精确绑定 `127.0.0.1:18080` 的本轮宿主 API 并清 local env，再停止
  local Compose，不得停止其它用户 API 进程或启动 default profile 充当替代。生产回滚尚未演练。

## 7. 未验证项、已知限制与接受风险

| Item | 影响 | Owner | 批准 | 截止/复查 |
|---|---|---|---|---|
| direct IdP JWT/native auth/tenant/RBAC | API S3/S4 + Desktop S5A/S5B + G3 live realm/offline/discovery/JWKS/callback PASS；API local-only explicit CA pin implemented，core online PASS；browser/bearer/Keychain/cross-repo 未验证 | 段成威 | G2A/S3/S4/S5A/S5B/A7 approved；G3 passed | S6 UI→S7/G5 |
| migration/bootstrap/audit | expand migration/rehearsal + local synthetic bootstrap first/idempotent/audit/revision PASS；production writer/admin control absent | 段成威 | S3/A7 local | S7/G5 |
| contracts v0.3.0 downstream pin | API 与 Desktop exact pin PASS；immutable tag 尚未形成 | 段成威 | G2A/S5B Passed | S8 tag/release |
| API/Desktop implementation | API producer、Desktop S5A native boundary 与 S5B generated store 为 remote candidates；S6 UI 与生产链路未实现 | 段成威 | S4/S5A/S5B approved；其余 Pending | S6/G4 |
| Tasks 双重隔离与 FEAT-126 | A6 已批准；default legacy profile/wire unchanged；local host profile+Caddy static deny PASS 且 Caddy 健康；online edge/direct 404 PASS；FEAT-125 不提供资源级授权 | 段成威 | Approved temporary exception | G3 online + G5 host profile/ingress；FEAT-126 生产启用或 2026-09-30 较早者 |
| G3 local IdP/infra | local vendor/issuer/client/JWKS/TLS/API origins 已固定；static gates/local stack/live realm/HTTPS user provisioning/offline ready/discovery/JWKS/callback PASS；API local-only explicit CA pin implemented，core online PASS | 段成威 | A7 scope only；G3 PASS | retain for S7；not production evidence |
| Provider refresh family | local Keycloak proves rotation but not automatic reuse-revokes-family | 段成威 | `provider_limit_documented`；not an exception PASS | S7/G5；不阻断 S5B implementation |
| production IdP/infra | production vendor/issuer/client/JWKS/DNS/TLS/API origin/CSP/control plane undetermined | 段成威 | Not approved | G5 |
| `rsa 0.9.10` advisory | S5A 仅使用 RS256 公钥验签；`RUSTSEC-2023-0071` 无修复版本并有 scoped ignore | 段成威 | EXC-125-002 candidate-only；G5 重审 | G5 或上游修复，取较早者 |

当前只有两项已批准的有边界临时例外：A6/EXC-125-001 只允许 legacy Tasks 保持不可达，不允许
对外暴露或宣称已有资源级授权；EXC-125-002 只允许 S5A candidate 的 RS256 公钥验签依赖，
不允许 RSA 私钥运算且必须在 G5/上游修复时重审。其余实现、集成和发布风险继续阻断对应
gate。Keycloak `provider_limit_documented` 是未验证限制，不是第三个 PASS 例外；API JWKS
CA trust 也是待批准 blocker，不是已接受风险。

## 8. 后续清理

| Issue | 内容 | 触发条件 | Owner | 截止 |
|---|---|---|---|---|
| CLEAN-001 | 删除旧 Desktop optional/default visibility 接口 | 新 total policy 完成并兼容验证 | 段成威 | S6 后 |
| CLEAN-002 | 移除 candidate SHA provenance，切不可移动 tag | tag/digest verification PASS | 段成威 | S8 |
| CLEAN-003 | 评估 capability alias/deprecation | 未来 key 改名/删除 | 段成威 | future feature |
| CLEAN-004 | 以 FEAT-126 完成 Tasks resource-level auth/tenant hardening 并移除临时隔离例外 | FEAT-126 生产启用；若未完成则保持 Tasks 阻断并重新审批 | 段成威 | FEAT-126 生产启用或 2026-09-30 较早者 |
| CLEAN-005 | 删除 flags/双轨 | 全部 consumers 迁移且生产观察完成 | 段成威 | G6 后 |

## 9. 文档与运维交接

| Artifact | Final path/link | Owner | Updated |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-125-authoritative-permission-projection/` | 段成威 | 2026-08-01 |
| Security/architecture ADR | `yijie/docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md` | 段成威 | Accepted 2026-07-31；A7/status addendum 2026-08-01 |
| Public API/release docs | `yijie-contracts/openapi/public/public.yaml` + `docs/releases/contracts-v0.3.0.md` | 段成威 | remote candidate 2026-08-01 |
| API producer docs | `yijie-api` owning-repo docs/tests | 段成威 | S4 remote candidate 2026-08-01 |
| Desktop S5A security matrix | `yijie-desktop/docs/security/FEAT-125-S5A-security-matrix.md` | 段成威 | S5A remote candidate 2026-08-01 |
| G3 generic runbook | `yijie-infra/docs/feat-125-nonproduction.md` | 段成威 | remote preparation `2f01f22...` |
| G3-NP-LOCAL runbook | `yijie-infra/docs/feat-125-local-lab.md` + local profile/validator/preflight scripts | 段成威 | Infra `298192e386...` remote verified；offline ready/core online PASS |
| Desktop S5B consumer evidence | `yijie-desktop/docs/security/FEAT-125-S5B-consumer-matrix.md` | 段成威 | `5c4600f8308d55be5596e7c45215e88c7411f286` remote verified；S6/release runbook not created |
| FEAT-124 G4 report | existing FEAT-124 `08-verification-report.md` | 段成威 | G4-001 remains open |

## 10. 复盘

- 做得有效的流程：先扫描四仓真实状态，再分别从 Contracts、API、Desktop 审核推荐方案；
  没有把“创建 endpoint”误写成可直接开工。
- 出现的返工/缺陷：现有 FEAT-124 需求曾假设“已有权限投影”，而仓库事实表明并不存在。
- 根因：需求层的未来依赖没有在 G2 前验证真实 provider/consumer call chain。
- 要沉淀的改进：任何 Must 权限 UI AC 必须在 G2 提供权威 Principal、tenant、policy
  source、production wiring 和 direct API enforcement 证据；纯 resolver 测试不足。

## 11. 关闭批准

| Gate | Owner | Decision | Date | Evidence |
|---|---|---|---|---|
| G3-NP-LOCAL | 段成威 | PASS | 2026-08-01 | strict explicit CA pin、offline ready、core online 与最终三仓门禁 PASS；随后 S5B complete |
| G6 Delivery Complete | 段成威 | Not approved / feature open | 2026-08-01 | S1—S5B remote；G3 passed；S6—S8/G4/G5/G6 Pending |

- 正式关闭时间：N/A。
