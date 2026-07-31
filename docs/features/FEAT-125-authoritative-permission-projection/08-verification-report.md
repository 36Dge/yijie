# FEAT-125 验证证据与独立审查报告

> 本文件记录 2026-07-31 的需求/设计基线，以及 2026-08-01 的 S1/S2
> Contracts candidate 实现与审查。API、Desktop、migration、跨仓集成、性能和生产
> 检查仍为 `NOT RUN`；G2A 仍待段成威单独批准。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | develop | `ef0f50e41128c44ea91bf2e581e1fecf14c7b95c` | package creation 后 expected dirty | Git/Bash | 2026-07-31 |
| yijie-contracts | develop | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | clean；local ahead of `origin/develop` by 2 | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 2026-08-01 |
| yijie-api | develop | `2834b412ad565651215bd12458276c4e0d8fecf5` | clean at scan | Go 1.26.5 declared | 2026-07-31 |
| yijie-desktop | develop | `be01cc2d0a1c9c4b057de616be201a4843d0a035` | clean at scan | Vue/Tauri/pnpm repo baseline | 2026-07-31 |

## 2. Baseline

| ID | CWD | Command | Exit code | Result | 摘要/日志位置 | 历史失败 |
|---|---|---|---:|---|---|---|
| BASE-001 | CrossBSD | four-repo `git status --short --branch && git rev-parse HEAD && git remote -v` | 0 | PASS | 4 repos clean/equal before creation | none observed |
| BASE-002 | each repo | `git ls-remote origin refs/heads/develop` | 0 | PASS | remote develop equals local full SHA | none |
| BASE-003 | yijie-contracts | `git ls-remote origin refs/tags/contracts-v0.2.0 'refs/tags/contracts-v0.2.0^{}'` | 0 | PASS | tag object `c6e8577...`→commit `f16a497...` | registry prose stale |
| BASE-004 | yijie-contracts | `shasum -a 256 openapi/public/public.yaml` | 0 | PASS | `a1033e382495dbc1aa7eaac0a49c4de5712e01264d1d26b3e56125c667acf6a4` | none |
| BASE-005 | affected repos | targeted `rg`/file reads | 0 | PASS | auth/RBAC absent；Desktop wiring absent；G4-001 confirmed | expected gaps |

## 3. Slice 证据

| Slice/AC | Head SHA | Command | Exit code | Result | Diff/证据 |
|---|---|---|---:|---|---|
| S0 / design audit | repository baselines above | Contracts/API/Desktop independent read-only audits | N/A | PASS | findings consolidated in 00—07 |
| S0 / package structure | current yijie worktree | `check-feature-package.sh --gate G2` | 0 | PASS | 2026-07-31：required 12 files；G2 scope has no incomplete marker；不代表代码门通过 |
| S0 / A1—A6 approval | N/A | 段成威逐项批准 direct JWT、native auth、tenant、roles、route、Tasks exception | N/A | PASS | G1/G2 Passed 2026-07-31；G2A Pending |
| S1 / contract source | `ab5e71db6e4d61eb9c761446066142de2edbb444` | TDD 失败→Public OpenAPI/fixtures/tests/generated SDK→generate/lint/test/build | 0 | PASS | 19 files；新 access projection contract 形成；Runtime methods/transport/security 未变 |
| S2 / final candidate | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | pack + baseline breaking + structured Public/Runtime semantic review + provenance/digest | 0 | PASS | candidate complete；`origin/develop` 已核对同一完整 SHA；未 tag |
| S3—S8 / provider, consumer, integration, release | N/A | G2A 仍 Pending | N/A | NOT RUN | no API/Desktop/migration/integration/release changes |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-PACKAGE | yijie | `check-feature-package.sh --gate G2 <feature-dir>` | Bash | 0 | PASS | 2026-07-31：文档结构完整且 G2 范围无未完成标记；代码/测试/安全/兼容/生产门仍未运行 |
| V-STRICT | yijie | `check-feature-package.sh --strict <feature-dir>` | Bash | 0 | PASS | 12 份需求包文件无模板变量或未完成标记 |
| V-DIFF | yijie | `git diff --check` + untracked whitespace/marker/status/scope checks | Git/rg | 0 | PASS | FEAT-125 package + ADR-0012 + FEAT-124 G4-001 cross-link only |
| V-YAML | yijie | Ruby Psych safe parse of FEAT-124/125 feature.yaml | Ruby/Psych | 0 | PASS | both manifests parsed |
| V-META | yijie | `pnpm lint && pnpm test` | repository-pinned pnpm/Node | 0 | PASS | repository manifest、Contract First governance 与 1 个 meta test 通过 |
| V-INSTALL | yijie-contracts | `pnpm install --frozen-lockfile --no-runtime --yes --config.manage-package-manager-versions=false` | pnpm 11.9.0 / Node 26.0.0 | 0 | PASS | 受控网络重试后成功；lockfile 不变；初次 sandbox/offline 重试因缺包失败，未作为最终证据 |
| V-CONTRACT | yijie-contracts | `make generate && make lint && make test && make build && pnpm pack:sdk` | openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Node 26 / pnpm 11 / Go 1.26.5 | 0 | PASS | generated current 26/26；Node 16/16；Go packages PASS；pack digest stable；首次 full test 发现 compatibility manifest bundle version 未同步，仅修正 0.2.0→0.3.0 后复跑通过 |
| V-BREAKING | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | repo-pinned compatibility toolchain | 0 | PASS | no breaking changes against supported v0.2.0 |
| V-SEMANTIC | yijie-contracts | structured Public + Runtime comparison against `f16a497...` | Node | 0 | PASS | legacy 5 paths/5 schemas/global security/servers unchanged；Runtime 仅 contracts_version 0.2.0→0.3.0 |
| V-DIGEST | yijie-contracts | `shasum -a 256` source/generated/manifest/tarball | shasum | 0 | PASS | 完整 digest 见第 5 节 |
| V-API | yijie-api | lint/unit/integration/generate/conformance | Go | N/A | NOT RUN | no implementation |
| V-DESKTOP | yijie-desktop | lint/test/build/docs/native/conformance | pnpm/Rust | N/A | NOT RUN | no implementation |
| V-E2E | cross-repo | `tenant_owner`/`tenant_member` × 2 tenants + auth/migration/perf | no harness yet | N/A | NOT RUN | S7 |

## 5. 契约与版本兼容

| 结论 | Contract version/full commit/digest/generator | Command/Test | Result | Evidence |
|---|---|---|---|---|
| 当前 remote candidate | 0.3.0 / `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | git/shasum/ls-remote | PASS | clean local commit；origin/develop verified equal |
| Supported baseline provenance | v0.2.0 / `f16a497...` | ls-remote | PASS | BASE-003 |
| Public source | `7bd40dd1c5a53cc1dcd317e3a64bf7189170fd7f575b25bb07f0eb243d0319ed` | generate/drift + shasum | PASS | `openapi/public/public.yaml` |
| TypeScript generated | `77babb215608c6ace4468d37b72fc8e43f5758231c7807a4301063cb156ae8e0` | generate/drift + shasum | PASS | `sdks/typescript/src/openapi/public.gen.ts` |
| Go generated | `01d31efc1b1c3fb69e18c853d67ea12cdc313c2709f2a02d02e2a01b6ff4d253` | generate/drift + shasum | PASS | `sdks/go/openapi/public/client.gen.go` |
| Runtime manifest | `5d374eb1b3012e08a10f8b8ce629a9ab12bbea6a11de379425cd8feaefdb8ea1` | structured comparison + shasum | PASS | 仅 bundle version 变更；Runtime projection 不变 |
| SDK candidate tarball | `43a54d7f9f01edd6b50adcebb8c3b4b645dab7ec8cf4aafe20b62d7d98718565` | pack twice after final commit | PASS | digest stable；local ignored artifact，未发布 |
| Supported baseline breaking check | `f16a497...` | explicit command | PASS | S2 |
| Producer conformance | exact candidate available locally | API tests | NOT RUN | S4/S7 |
| Consumer conformance | exact candidate available locally | Desktop tests | NOT RUN | S5A/S5B/S7 |
| Agent Host/Runtime regression | Agent Host remains v0.2.0 | structured manifest comparison | CONTRACT PASS / integration NOT RUN | Runtime semantics unchanged；S7 仍需真实集成 |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-001—005 | planned yijie-api direct access-JWT authn、tenant discovery/header、authorization projection | API/SEC/RES | no implementation | NOT RUN |
| AC-006—012 | planned Desktop permission client/store/nav/router/AppShell | DESK/RES/A11Y | no implementation | NOT RUN |
| AC-013/015 | planned tenant/capability endpoint auth + Tasks network/service isolation + cross E2E | SEC-003/E2E-001 | no implementation | NOT RUN |
| AC-014 | v0.3.0 source/generated candidate + exact provenance | CT-002/SUP-001 | S1/S2 contract gates and digests | CONTRACT PASS / API+Desktop pins NOT RUN |
| AC-016 | FEAT-124 verification report | REV-001 | FEAT-125 incomplete | NOT RUN |
| AC-017/018 | planned Desktop native system-browser OIDC、exact loopback、state/PKCE/nonce、Keychain/token lifecycle、operation-scoped authenticated transport | AUTH/DESK/SEC | no implementation | NOT RUN |
| AC-019/020 | planned root/deep-link policy + exact 7-capability/2-role matrix | DESK/E2E | no implementation | NOT RUN |
| AC-021 | planned ingress deny + service handler non-registration + Desktop non-use | SEC/DEPLOY/E2E | no implementation | NOT RUN |
| NFR-001—008 | planned security/reliability/perf/provenance/native-auth | mapped in 06 | no implementation | NOT RUN |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| E2E | API→Desktop | `tenant_owner`（7 capabilities）/`tenant_member`（仅 task.create/task.read）×2 tenants | NOT RUN | S7 |
| Native auth/security | exact `/oauth/callback`、state/PKCE、ID-token nonce、10m access、single-flight refresh、Keychain rotation/reuse、固定两 GET operations、zero token IPC/generic proxy | test IdP+macOS Keychain+test API | NOT RUN | S5A/S7 |
| Security/tenant | API access-JWT verifier、tenant discovery/header、RBAC/IDOR/stale context、Tasks 双隔离 | test IdP+Postgres+production-like ingress | NOT RUN | S3—S7 |
| Failure/resilience | 400/401/403/500/503/timeout/rollback/token-family reuse | candidate matrix | NOT RUN | S4—S7 |
| Migration rehearsal | 00001→expand/bootstrap/rollback | PostgreSQL 16 | NOT RUN | S3/S7 |
| Performance | projection 50 RPS candidate | staging | NOT RUN | S7 |
| AI Eval | no AI behavior | N/A | N/A | scope |
| Visual/accessibility | hidden/disabled/recovery | browser+Tauri light/dark/min | NOT RUN | S6/S7 |

## 8. Diff 与制品完整性

- [x] `git status` 已在最终文档编辑后逐仓复核
- [x] tracked + untracked 文档 whitespace 检查通过
- [x] diff/status 范围只含 FEAT-125、ADR-0012 与 FEAT-124 G4-001 cross-link
- [x] 完整文档 diff 已审阅
- [x] 生成物来自锁定 generator：openapi-typescript 7.13.0 / oapi-codegen 2.7.2，重生成漂移检查 PASS
- [x] lockfile/依赖未变化
- [x] migration 未变化；expand/bootstrap 设计已随 G2 批准，实际 migration/rehearsal `NOT RUN`
- [x] 新增 3 个 contract tests 与 12 个 fixture；无 `.skip`、`.only`、弱化断言或关闭门禁
- [x] 本轮文档未写入 secret、PII、本机外部引用、调试后门或临时文件

## 9. 独立 Review Findings

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| G1-001 | P1 / design resolved | Contracts/API/Desktop auth scan | 原基线无可信身份或活动租户 | Closed at design：A1—A3 批准 direct IdP access JWT、native OIDC 与逐请求 tenant membership；实现/验证待 S3—S7 | G2A/S7 |
| G1-002 | P1 / release control | API Tasks handler/repository/migration | legacy Tasks 仍无资源级授权，不能随 FEAT-125 暴露 | Design closed by A6：ingress deny + service 不注册 handlers；实施证据待 G5，资源授权由 FEAT-126 完成 | G5/FEAT-126 |
| G1-003 | P2 / FEAT-124 blocking | Desktop AppShell/nav/router | default `{}` + missing→visible、无 guard | Open implementation：S5B/S6 fail-closed 接入 | S7/FEAT-124 G4 |
| G1-004 | P2 / delivery blocking | API/Desktop generation | floating sibling 与 placeholder generate，无法追溯 wire | Contract side resolved：exact SHA/digests/generators 已形成；API/Desktop exact pin/drift CI 仍 Open | G2A/S7 |
| G1-005 | P2 / implementation blocking | API database/audit | 无 RBAC tables；audit resource FK 只支持 task | Design approved：expand migration/bootstrap；implementation/rehearsal pending | S3/S7 |

- Reviewer 是否独立于实现上下文：设计阶段采用 Contracts、API、Desktop 三个并行只读
  reviewer pass；尚无实现可做 G4 code review。
- P0/P1 设计阻断是否清零：是；A1—A6 已关闭 G1/G2 设计决策。实现/发布层的
  G1-002 双隔离证据、G1-003/004/005 仍不得越过对应 gate。
- P2 例外批准：无；不允许用例外关闭 FEAT-124 G4-001。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| direct JWT/native auth/tenant | A1—A3 设计已批准但未实现 | critical | S3/S5A auth/security tests + S7 | 段成威 | yes |
| RBAC/migration/audit | A4 与 schema 方向已批准但未实现 | critical | S3 migration rehearsal + S7 | 段成威 | yes |
| Contract candidate G2A | candidate 与远端可用性已完成，但未获单独 G2A 批准 | high | explicit G2A | 段成威 | yes |
| API producer | 尚未实现 | high | S3/S4 conformance | 段成威 | yes |
| Desktop consumer | 尚未实现 | high | S5A/S5B/S6 tests | 段成威 | yes |
| Cross-repo/staging | 环境/harness 未建立 | critical | S7 | 段成威 | yes |
| Tasks 双隔离/FEAT-126 | A6 已批准但生产隔离未实施；资源级授权不在 FEAT-125 | critical | G5 isolation evidence；FEAT-126 production enablement（不晚于例外期限） | 段成威 | yes |
| Production IdP/infra/signing | vendor、issuer、client ID、JWKS、TLS/CSP 等未定义；audience 已固定 | high | G3/G5 plan+evidence | 段成威 | yes |

## 11. 结论

- Code Complete：否。
- 验证人：Codex（需求/设计只读审核）；业务/技术/安全 Owner 为段成威。
- 日期：2026-08-01。
- 结论依据：A1—A6 已由段成威批准，G1/G2 于 2026-07-31 Passed；S1/S2 已在
  2026-08-01 形成 candidate `9ec34abd...` 并通过生成、全门禁、breaking check 和
  semantic review，且 origin/develop 已核对为同一完整 SHA。G2A 仍 Pending，S3—S8 的
  API/Desktop、migration、集成和发布
  均 `NOT RUN`。FEAT-124
  G4-001 继续阻断，直到 FEAT-125 真实 producer/consumer/E2E 与独立 G4 证据完成。
