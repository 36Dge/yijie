# FEAT-125 验证证据与独立审查报告

> 本文件记录 2026-07-31 的需求/设计基线，以及 2026-08-01 的 S1/S2 Contracts
> candidate、S3/S4 API provider 与 S5A Desktop native boundary 实现/验证。API 与 Desktop
> native flags 默认关闭；不含 S5B/UI、真实 IdP/正式 Keychain provisioning、部署或生产
> 激活，G3/G4/G5 保持 Pending。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | develop | base/remote `28c6f503f2c66a0dc5964d85cc5865fcb4ae2794` | S5A evidence update expected dirty | Git/Bash | 2026-08-01 |
| yijie-contracts | develop | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | clean；origin/develop verified equal | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 2026-08-01 |
| yijie-api | develop | `360a526b679147472e7cc82ca7ac9db9d18a371d` | clean；origin/develop verified equal | Go 1.26.5 / PostgreSQL 16.14 | 2026-08-01 |
| yijie-desktop | develop | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | clean；origin/develop verified equal | Vue 3/Tauri 2/pnpm 11/Rust | 2026-08-01 |

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
| S0 / A1—A6 approval | N/A | 段成威逐项批准 direct JWT、native auth、tenant、roles、route、Tasks exception | N/A | PASS | G1/G2 Passed 2026-07-31；G2A Passed 2026-08-01 |
| S1 / contract source | `ab5e71db6e4d61eb9c761446066142de2edbb444` | TDD 失败→Public OpenAPI/fixtures/tests/generated SDK→generate/lint/test/build | 0 | PASS | 19 files；新 access projection contract 形成；Runtime methods/transport/security 未变 |
| S2 / final candidate | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | pack + baseline breaking + structured Public/Runtime semantic review + provenance/digest | 0 | PASS | candidate complete；`origin/develop` 已核对同一完整 SHA；未 tag |
| S3 / API foundation | `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` | TDD red→exact pin/expand migration/RS256 JWT/JWKS/identity/tenancy/RBAC→all S3 gates | 0 | PASS | remote SHA verified；no production values or activation |
| S4 / API producer | `360a526b679147472e7cc82ca7ac9db9d18a371d` | TDD red→tenant/capability endpoints、atomic projection、stable faults/headers、metrics→all S4 gates | 0 | PASS | canonical producer conformance；flag default false；no production values/activation；remote verified |
| S5A / Desktop native auth+transport | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | system-browser OIDC、exact loopback、PKCE/state/nonce、Keychain lifecycle、two fixed authenticated operations→security matrix/all gates | 0 | PASS | native flag default false；no S5B/UI/Tasks/production values；remote verified；real provider/provisioning NOT RUN |
| S5B—S8 / generated consumer, UI, integration, release | N/A | outside current authorization | N/A | NOT RUN | no generated permission store/UI/cross-repo/release changes |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-PACKAGE | yijie | `check-feature-package.sh --gate G2 <feature-dir>` | Bash | 0 | PASS | 2026-08-01：required 12 files；G2 scope 无模板未完成标记；不代表 G4/G5 通过 |
| V-STRICT | yijie | `check-feature-package.sh --strict <feature-dir>` | Bash | 0 | PASS | 12 份需求包文件无模板变量或未完成标记 |
| V-DIFF | yijie | `git diff --check` + status/scope checks | Git/rg | 0 | PASS | 本轮仅 FEAT-125 00—10/feature.yaml 与 ADR-0012 的 S5A evidence/status 更新 |
| V-YAML | yijie | Ruby Psych safe parse of FEAT-124/125 feature.yaml | Ruby/Psych | 0 | PASS | both manifests parsed |
| V-META | yijie | `pnpm lint && pnpm test` | repository-pinned pnpm/Node | 0 | PASS | repository manifest、Contract First governance 与 1 个 meta test 通过 |
| V-INSTALL | yijie-contracts | `pnpm install --frozen-lockfile --no-runtime --yes --config.manage-package-manager-versions=false` | pnpm 11.9.0 / Node 26.0.0 | 0 | PASS | 受控网络重试后成功；lockfile 不变；初次 sandbox/offline 重试因缺包失败，未作为最终证据 |
| V-CONTRACT | yijie-contracts | `make generate && make lint && make test && make build && pnpm pack:sdk` | openapi-typescript 7.13.0 / oapi-codegen 2.7.2 / Node 26 / pnpm 11 / Go 1.26.5 | 0 | PASS | generated current 26/26；Node 16/16；Go packages PASS；pack digest stable；首次 full test 发现 compatibility manifest bundle version 未同步，仅修正 0.2.0→0.3.0 后复跑通过 |
| V-BREAKING | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | repo-pinned compatibility toolchain | 0 | PASS | no breaking changes against supported v0.2.0 |
| V-SEMANTIC | yijie-contracts | structured Public + Runtime comparison against `f16a497...` | Node | 0 | PASS | legacy 5 paths/5 schemas/global security/servers unchanged；Runtime 仅 contracts_version 0.2.0→0.3.0 |
| V-DIGEST | yijie-contracts | `shasum -a 256` source/generated/manifest/tarball | shasum | 0 | PASS | 完整 digest 见第 5 节 |
| V-API-PIN | yijie-api | `make generate-check` | Go 1.26.5 / oapi-codegen v2.7.2 | 0 | PASS | exact HEAD `9ec34abd...`、clean tracked source、source `7bd40dd...`、generated `a1801a...` |
| V-API-LINT | yijie-api | `make lint` | gofmt/go vet | 0 | PASS | all cmd/internal Go sources formatted and vetted |
| V-API-UNIT | yijie-api | `make test` | `go test -race -cover ./...` | 0 | PASS | exact-single audience、duplicate auth header、0/1/multiple tenants、ready/empty、400/401/403/500/503、headers/expiry、metrics concurrency |
| V-API-DB | yijie-api | `make test-integration` with isolated local DSN | PostgreSQL 16 / race / integration tag | 0 | PASS | 00001→00002、old rows、append-only、expand-only、cross-tenant FK、2 users×2 tenants atomic projection matrix |
| V-API-AUDIT | yijie-api | `govulncheck v1.6.0 ./...` + direct license read | Go vulnerability DB | 0 | PASS | 0 called/package vulnerabilities；unreferenced x/crypto/openpgp module advisory GO-2026-5932；jwx/httprc MIT、generator Apache-2.0 |
| V-API-S3-REVIEW | yijie-api | structured review：scope→contract→authn→migration/RBAC→tests/CI→dependencies | Codex separated review pass | 0 | PASS | P0/P1/P2=0；S3-REV-001 non-hex full SHA validation fixed+tested |
| V-API-S4-REVIEW | yijie-api | structured review：scope→contract/errors→authn→tenant consistency→lifecycle/metrics→CI/supply chain | Codex separated review pass | 0 | PASS | P1=1/P2=2 resolved；最终开放 P0/P1/P2=0；默认关闭与生产边界保留 |
| V-DESKTOP-INSTALL | yijie-desktop | `pnpm install --frozen-lockfile` | pnpm 11 | 0 | PASS | 2 workspaces；frozen lockfile install |
| V-DESKTOP-LINT | yijie-desktop | `make lint` | ESLint/Vue TSC/rustfmt/Clippy `-D warnings` | 0 | PASS | frontend + Rust native boundary clean |
| V-DESKTOP-TEST | yijie-desktop | `make test` | Vitest/Cargo | 0 | PASS | frontend 9 files/37 tests；Rust 27 tests + doc-tests |
| V-DESKTOP-BUILD | yijie-desktop | `make build` + `pnpm docs:build` + `pnpm tauri:build --debug` | Vite/VitePress/Tauri macOS | 0 | PASS | production web/docs；debug `.app` + aarch64 `.dmg` |
| V-DESKTOP-AUDIT | yijie-desktop | `pnpm audit --audit-level high` + `cargo audit --file src-tauri/Cargo.lock` + Cargo license metadata audit | npm/RustSec/Cargo metadata | 0 | PASS | npm 0 known；RUSTSEC-2023-0071 documented verifier-only ignore；504 third-party packages license metadata present，no prohibited strong license |
| V-DESKTOP-S5A-REVIEW | yijie-desktop | structured review：scope→OIDC→token lifecycle/concurrency→Keychain→IPC/HTTP→dependencies/failure | Codex separated review pass | 0 | PASS | 6 类 findings resolved；最终开放 P0/P1/P2=0；EXC-125-002；真实 IdP/provisioning NOT RUN |
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
| API generated consumer pin | exact candidate + source/generated digest + generator module | `make generate-check` | PASS | S3/S4 clean regenerate |
| Producer conformance | canonical contract fixtures + generated types | API endpoint/fault/integration tests | PASS | S4 remote；staging remains S7 |
| Desktop native boundary | contract operation semantics + fixed Rust command/HTTP allowlist | S5A unit/security/native build | LOCAL PASS | no token IPC/generic proxy；real API/IdP remains S7/G3/G5 |
| Consumer conformance | exact candidate available remotely | Desktop generated adapter/store tests | NOT RUN | S5B/S7 |
| Agent Host/Runtime regression | Agent Host remains v0.2.0 | structured manifest comparison | CONTRACT PASS / integration NOT RUN | Runtime semantics unchanged；S7 仍需真实集成 |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-001/003 | access handlers + `internal/platform/authn` + identity mapping | SEC-001/004/007 | exact-single aud、RS256/claims/TTL/key rotation、duplicate header、401/403/503 conformance | API PRODUCER PASS |
| AC-004 | canonical tenant header + atomic active user/tenant/membership/RBAC query | SEC-002 | 400 invalid、403 denied、2×2 PostgreSQL integration | API PRODUCER PASS |
| AC-002/005 | tenant discovery/projection endpoints + stable HTTP faults | API/RES | canonical 0/1/multiple、ready/empty、400/401/403/500/503 fixtures | API PRODUCER PASS |
| AC-006—012 | planned Desktop permission client/store/nav/router/AppShell | DESK/RES/A11Y | no implementation | NOT RUN |
| AC-013/015 | endpoint auth + tenant/RBAC authority；Tasks isolation/cross E2E pending | SEC-002/003/E2E-001 | API endpoint + 2×2 DB matrix PASS；ingress/cross-repo NOT RUN | PARTIAL |
| AC-014 | v0.3.0 source/generated candidate + exact provenance | CT-002/SUP-001 | S1/S2 contract gates + API exact pin/drift | CONTRACT+API PIN PASS / Desktop pin NOT RUN |
| AC-016 | FEAT-124 verification report | REV-001 | FEAT-125 incomplete | NOT RUN |
| AC-017/018 | Desktop native system-browser OIDC、exact loopback、state/PKCE/nonce、Keychain/token lifecycle、operation-scoped authenticated transport | OIDC-001/SEC-005/011/012 | S5A 27 Rust tests、native build、storage/IPC/scope scan 与 structured review；真实 provider/provisioned Keychain 尚未联调 | LOCAL SLICE PASS / G3/G5/S7 PENDING |
| AC-019/020 | exact 7-capability/2-role matrix + planned root/deep-link policy | API-004/E2E/DESK | API DB 2 users×2 tenants exact matrix PASS；Desktop/cross-repo NOT RUN | PARTIAL |
| AC-021 | planned ingress deny + service handler non-registration + Desktop non-use | SEC/DEPLOY/E2E | no implementation | NOT RUN |
| NFR-001/002/006/007 | fail-closed endpoints、tenant FK、exact pin、secret-free diff | SEC/DB/SUP | S3/S4 unit/integration/drift/audit | API PRODUCER PASS |
| NFR-003—005/008 | endpoint fault recorder、Desktop native auth/transport security；staging perf/UI accessibility pending | mapped in 06 | S4 faults + S5A local native security PASS；staging/S6 outside scope | PARTIAL |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| E2E | API→Desktop | `tenant_owner`（7 capabilities）/`tenant_member`（仅 task.create/task.read）×2 tenants | NOT RUN | S7 |
| Native auth/security | exact `/oauth/callback`、state/PKCE、ID-token nonce、10m access、single-flight refresh、Keychain rotation/reuse、固定两 GET operations、zero token IPC/generic proxy | S5A local mocks/unit + debug native artifact | LOCAL PASS | real IdP/API、正式 Keychain provisioning/签名 App 为 G3/G5/S7 NOT RUN |
| Security/tenant | API access-JWT verifier、JWKS、identity/active membership、atomic RBAC projection | generated RSA keys + local TLS + PostgreSQL 16 | S4 API PRODUCER PASS | Tasks isolation/cross-repo remain S7/G5 |
| Failure/resilience | 400/401/403/500/503、no-store/challenge/retry、dependency faults | canonical/fake dependency matrix | S4 API PASS + S5A token/config/HTTP fail-closed LOCAL PASS | S5B state/cross-repo remains S7 |
| Migration rehearsal | 00001→expand/rollback metadata；bootstrap excluded | PostgreSQL 16.14 isolated schema | PASS | existing task/audit retained；generic locator/append-only/FK/down refusal verified；bootstrap S7 |
| Performance | projection 50 RPS candidate | staging | NOT RUN | S7 |
| AI Eval | no AI behavior | N/A | N/A | scope |
| Visual/accessibility | hidden/disabled/recovery | browser+Tauri light/dark/min | NOT RUN | S6/S7 |

## 8. Diff 与制品完整性

- [x] `git status` 已在最终文档编辑后逐仓复核
- [x] tracked + untracked 文档 whitespace 检查通过
- [x] diff/status 范围复核：本轮 yijie 仅 FEAT-125/ADR evidence 更新；S4 API 与 S5A Desktop owning-repo commits 已分别远端核验；Contracts/Tasks wire 未改
- [x] 完整文档 diff 已审阅
- [x] 生成物来自锁定 generator：openapi-typescript 7.13.0 / oapi-codegen 2.7.2，重生成漂移检查 PASS
- [x] Go module/lock 变化仅为 exact oapi-codegen v2.7.2 tool 与 jwx v3.2.0/httprc v3.0.6 及其解析依赖；advisory/license 已审计
- [x] migration v2 digest `51c4ced9...`；00001 upgrade/append-only/composite FK/expand-only rehearsal PASS；无真实 seed/session 表
- [x] 新增 3 个 contract tests 与 12 个 fixture；无 `.skip`、`.only`、弱化断言或关闭门禁
- [x] S5A lock digests：`src-tauri/Cargo.lock`=`94b1ee21ed1bd9e4e97528622971da9241c43c4e497181ec83f77f2da6a5b973`；`pnpm-lock.yaml`=`aaa0a300afb760c0a768aebefcf338bdbbb66dd6a62a3a907d456d0246fedc0c`
- [x] S5A dependency exception EXC-125-002 已限定为 `openidconnect→rsa` 的 RS256 公钥验签路径；无 RSA 私钥/签名/解密，G5 或上游修复时必须重审/移除
- [x] 本轮文档未写入 secret、PII、本机外部引用、调试后门或临时文件

结构化 S3 review finding：

| Finding | Severity | 结论 | 修复/证据 |
|---|---|---|---|
| S3-REV-001 | P3 | exact-pin lock 原实现只检查 full commit 长度，未显式拒绝非十六进制字符 | `Lock.Validate` 增加 40 位 hex 校验与负测；generate/lint/race/integration 复跑 PASS |

结构化 S4 review findings：

| Finding | Severity | 结论 | 修复/证据 |
|---|---|---|---|
| S4-REV-001 | P2 | 重复 `Authorization` header 原会由 `Header.Get` 取首值，可能与代理解释不一致 | 要求 header values 恰好 1 个；重复头负测返回 canonical 401 |
| S4-REV-002 | P2 | JWT 库 audience option 验证“包含目标值”，未证明契约要求的唯一精确 audience | 解析后强制 `aud == [https://api.yijie.ai]`；多 audience 负测 PASS |
| S4-REV-003 | P1 | JWKS cache 若绑定随后取消的 startup context，可能启动后持续不可用 | 改用服务生命周期 context，shutdown 时 Close/Cancel；全量编译、race、JWKS tests PASS |

S4 review 后开放 P0/P1/P2 findings = 0；以上均在 commit 前关闭，未使用例外。

结构化 S5A review findings：

| Finding | Severity | 结论 | 修复/证据 |
|---|---|---|---|
| S5A-REV-001 | P1 | 401 并发等待者可能在前一请求已轮换后重复 refresh | 加 rejected-token 重检，等待者复用已轮换 access token；并发测试 PASS |
| S5A-REV-002 | P1 | Keychain 删除失败后内存态可能再次读取旧 refresh family | 加 `storage_blocked` 熔断，仅新登录成功落盘解除；故障测试 PASS |
| S5A-REV-003 | P1 | Keychain load/save 失败可能留下服务器端孤儿 refresh token | 失败分支先撤销新 refresh token，再清本地；测试 PASS |
| S5A-REV-004 | P1 | refresh 未轮换/非法响应可能保留旧 family | 同 token、缺 token、非法 response 统一撤销并 fail-closed；负测 PASS |
| S5A-REV-005 | P2 | callback parser 对 issuer/body/transfer-encoding 边界不足 | 加精确可选 issuer、body/transfer-encoding 拒绝与安全 response headers；负测 PASS |
| S5A-REV-006 | P1 / dependency | npm `GHSA-mh99-v99m-4gvg` high advisory | workspace override `brace-expansion=5.0.8`；`pnpm audit --audit-level high` PASS |

S5A review 后开放 P0/P1/P2 findings = 0；RUSTSEC-2023-0071 仅作为 EXC-125-002 的
verifier-only candidate 残余风险，不构成生产批准。

## 9. 独立 Review Findings

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| G1-001 | P1 / local boundaries resolved, integration pending | Contracts/API/Desktop auth scan | 原基线无可信身份或活动租户 | API S3/S4 与 Desktop S5A native boundary 本地/仓内 PASS；真实 IdP、generated consumer/store 与跨仓链路仍待 G3/S5B/S7 | G3/S5B/S7 |
| G1-002 | P1 / release control | API Tasks handler/repository/migration | legacy Tasks 仍无资源级授权，不能随 FEAT-125 暴露 | Design closed by A6：ingress deny + service 不注册 handlers；实施证据待 G5，资源授权由 FEAT-126 完成 | G5/FEAT-126 |
| G1-003 | P2 / FEAT-124 blocking | Desktop AppShell/nav/router | default `{}` + missing→visible、无 guard | Open implementation：S5B/S6 fail-closed 接入 | S7/FEAT-124 G4 |
| G1-004 | P2 / delivery blocking | API/Desktop generation | floating sibling 与 placeholder generate，无法追溯 wire | API side resolved in S3：exact source/generated SHA+generator+CI；Desktop side remains Open | S5B/S7 |
| G1-005 | P2 / write-path pending | API database/audit | 无 RBAC tables；audit resource FK 只支持 task | S3 migration/rehearsal + S4 atomic read projection PASS；bootstrap/write-audit evidence remains later | S7 |

- Reviewer 是否独立于实现上下文：设计阶段采用 Contracts、API、Desktop 三个并行只读
  reviewer pass；本轮按六维清单重新读取最终 staged diff 并完成 structured review。由于仍在同一
  Codex 任务内，它不冒充最终独立 G4；G4 继续 Pending。
- P0/P1 设计阻断是否清零：是；A1—A6 已关闭 G1/G2 设计决策。实现/发布层的
  G1-002 双隔离证据、G1-003/004/005 仍不得越过对应 gate。
- P2 例外批准：无；不允许用例外关闭 FEAT-124 G4-001。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| direct JWT/native auth/tenant | API S4 producer与 Desktop S5A native boundary PASS；真实 provider/provisioned Keychain/跨仓未验证 | critical | S7 + G3/G5 config | 段成威 | yes |
| RBAC/migration/audit | S3 migration + S4 consistent read projection PASS；bootstrap/writer transaction 未实现 | high | S7 | 段成威 | yes |
| API producer | endpoint/conformance/metrics recorder 已远端核验；staging/performance/exporter 未验证 | high | S7/G5 | 段成威 | yes |
| Desktop consumer | S5A native auth/transport 已远端核验；exact pin/generated adapter/store/nav/router 尚未实现 | high | S5B/S6/S7 | 段成威 | yes |
| Cross-repo/staging | 环境/harness 未建立 | critical | S7 | 段成威 | yes |
| Tasks 双隔离/FEAT-126 | A6 已批准但生产隔离未实施；资源级授权不在 FEAT-125 | critical | G5 isolation evidence；FEAT-126 production enablement（不晚于例外期限） | 段成威 | yes |
| Production IdP/infra/signing | vendor、issuer、client ID、JWKS、TLS/CSP 等未定义；audience 已固定 | high | G3/G5 plan+evidence | 段成威 | yes |
| Desktop RSA dependency advisory | `openidconnect 4.0.1`→`rsa 0.9.10` 无修复版本；当前仅公钥验签 | medium if scope drifts | EXC-125-002；每次 audit；G5/上游修复时移除 | 段成威 | yes for production review |

## 11. 结论

- Code Complete：否。
- 验证人：Codex（需求/设计只读审核）；业务/技术/安全 Owner 为段成威。
- 日期：2026-08-01。
- 结论依据：A1—A6 已由段成威批准，G1/G2 于 2026-07-31 Passed，G2A 于 2026-08-01
  Passed；S1/S2 已在
  2026-08-01 形成 candidate `9ec34abd...` 并通过生成、全门禁、breaking check 和
  semantic review，且 origin/develop 已核对为同一完整 SHA。S3 API exact pin、migration、
  authn/identity/tenancy/RBAC 已推送为 `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`。S4 API
  producer 已通过全部门禁/结构化审查并远端核验为
  `360a526b679147472e7cc82ca7ac9db9d18a371d`。S5A Desktop system-browser OIDC、exact
  loopback、PKCE/state/nonce、Keychain token lifecycle 与 operation-scoped transports 已通过
  全部门禁/安全矩阵/结构化审查并远端核验为
  `3798c67d260237928730758c7ec4c1fbe6fcf7d2`。两端 flags 默认关闭，无生产 IdP 配置或
  激活。S5B—S8 的 generated consumer/UI、跨仓集成和发布仍 `NOT RUN`。FEAT-124
  G4-001 继续阻断，直到 FEAT-125 真实 producer/consumer/E2E 与独立 G4 证据完成。
