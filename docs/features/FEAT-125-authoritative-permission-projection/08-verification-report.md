# FEAT-125 验证证据与独立审查报告

> 本文件记录 2026-07-31 的需求/设计基线，以及 2026-08-01 的 S1/S2 Contracts、S3/S4
> API、S5A Desktop 和当前 G3-NP-LOCAL 提交证据。结论是 `G3-NP-LOCAL PASS`：API/Desktop/Infra 静态实现与仓内门禁、专用 `yijie_api_feat125_local` 空库
> migration 1→2 与 tracked 2 users × 2 tenants synthetic bootstrap/inventory、
> Keycloak/PostgreSQL/Caddy 健康启动、Infra 71/71 + lint/Compose/shell/diff、exact
> realm/two clients/canonicalized scope sets/explicit `userinfo.token.claim=false` mapper/strict
> managed `data_classification` user profile/two fixed users/password resets/refresh revocation
> `invalid_grant` live conformance、固定 HTTPS 置密和 final offline ready 已完成。API 仅在
> `feat-125-local-lab` 使用严格显式 CA PEM + lowercase SHA-256 pin，未修改系统 Keychain；
> core online 的 discovery/JWKS/callback、API health/ready、两个 unauthenticated `401` 与
> Tasks edge/direct `404` 全部 PASS。随后 S5B 已单独批准、完成并远端核验；feature 仍关闭。
> S6 亦已远端核验。S7 已实际执行，但结论为 `BLOCKED`：真实系统浏览器 Code+PKCE 与
> exact loopback 到达 access-JWT 验证后，Keycloak 26.7 token 缺少批准契约要求的 `nbf`；
> Data Protection Keychain smoke 同时因缺少签名 entitlement 返回 macOS `-34018`，本机
> code-signing identities 为 0。未降低 API/JWT/存储安全约束，2×2/performance 未被伪报为 PASS。
> 段成威据此批准当前状态为 `Local Engineering Baseline Complete / Production Activation
> Blocked`：S7 冻结到真实部署准备，允许使用合成身份/租户/权限继续首页、聊天和 Tasks
> 业务开发；所有权限 flags 默认关闭，G4/G5/G6 与生产发布仍未通过。

## 1. 验证上下文

| Repository | Branch | Verified full commit | Worktree/remote | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| yijie | develop | governance base `7c3d6ff4b0a9596f0f270403f5dbd50e1401501b` | 本报告所属治理提交的最终 SHA 由 Git 历史与交付 handoff 登记，不自引用 | Git/Bash | 2026-08-01 |
| yijie-contracts | develop | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | clean；origin/develop verified equal | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 2026-08-01 |
| yijie-api | develop | `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | clean；`origin/develop` verified equal | Go 1.26.5 / PostgreSQL 16 | 2026-08-01 |
| yijie-desktop | develop | `155854cf3662384caa2c8bffe0a47935ef4a70b5` | clean；origin/develop verified equal；precommit candidate `a1718bb0900a...` | Vue 3/Tauri 2/pnpm 11/Rust | 2026-08-01 |
| yijie-infra | develop | `f040492e7c4af4aa7cc94a343140c58befae3af2` | clean tracked worktree；origin/develop verified equal；precommit candidate `2595b01baa9d...`；ignored local runtime files retained | Node 26 / pnpm 11 / Docker Compose | 2026-08-01 |

G3 与 S7 提交前都使用 `candidate:<base-full-sha>:<deterministic-tree-sha256>` 防止把 base
HEAD 误称为本轮实现。S7 两个 reviewed trees 已原样形成上表完整提交、推送并经
`git ls-remote` 核验；外部 blocker 结论不因提交而变成 PASS。

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
| S0 / A1—A7 approval | N/A | 段成威逐项批准 direct JWT、native auth、tenant、roles、route、Tasks exception 与 local-lab scope | N/A | PASS | G1/G2 Passed 2026-07-31；G2A/A7 scope approved 2026-08-01 |
| S1 / contract source | `ab5e71db6e4d61eb9c761446066142de2edbb444` | TDD 失败→Public OpenAPI/fixtures/tests/generated SDK→generate/lint/test/build | 0 | PASS | 19 files；新 access projection contract 形成；Runtime methods/transport/security 未变 |
| S2 / final candidate | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | pack + baseline breaking + structured Public/Runtime semantic review + provenance/digest | 0 | PASS | candidate complete；`origin/develop` 已核对同一完整 SHA；未 tag |
| S3 / API foundation | `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf` | TDD red→exact pin/expand migration/RS256 JWT/JWKS/identity/tenancy/RBAC→all S3 gates | 0 | PASS | remote SHA verified；no production values or activation |
| S4 / API producer | `360a526b679147472e7cc82ca7ac9db9d18a371d` | TDD red→tenant/capability endpoints、atomic projection、stable faults/headers、metrics→all S4 gates | 0 | PASS | canonical producer conformance；flag default false；no production values/activation；remote verified |
| S5A / Desktop native auth+transport | `3798c67d260237928730758c7ec4c1fbe6fcf7d2` | system-browser OIDC、exact loopback、PKCE/state/nonce、Keychain lifecycle、two fixed authenticated operations→security matrix/all gates | 0 | PASS | native flag default false；no S5B/UI/Tasks/production values；remote verified；real provider/provisioning NOT RUN |
| S5B / Desktop contract consumer+store | final `f94ac343881b0f7df59c0f5f4169372e612fd019` | exact candidate/generator→generated TypeScript/fixed adapter→0/1/multiple tenant domain state→revision/expiry/context validation→memory fail-closed store→all gates | 0 | PASS | implementation `5c4600f...` + CI fixes `942df58...`/`f94ac34...`；12 frontend files/80 tests + 36 Rust tests；S5B-REV-001—006 resolved；GitHub Actions `30695055988` PASS；feature off；no S6/UI/Tasks/Rust lifecycle/production values；remote verified |
| G3-NP / generic preparation | `yijie-infra@2f01f22b46f313f8ff0b9973e417f7ccae654318` | strict safe template/ready validation + bounded online preflight tests + local Compose/migration/API flag-off smoke | 0 | PREPARED | historical 19 tests/migration 2/health/ready/flag-off 404 PASS；remote verified；not G3-NP-LOCAL PASS |
| G3-NP-LOCAL / static+offline+bootstrap | verified full commits above | pinned images/profile/config、strict validators、API exact local issuer/dedicated DB/tracked 2×2 guard + audited bootstrap、Desktop CA+Keychain environment binding；owning-repo gates；local up/status/provision/prepare/ready | 0 | PASS / REMOTE VERIFIED | API/Desktop gates and Infra 71/71 + lint/Compose/shell/diff recorded below；containers healthy；exact Keycloak realm/client/scope-set/explicit mapper/strict user-profile/two-user/password-reset/refresh-revocation conformance over pinned HTTPS and final offline ready PASS；dedicated API DB empty inventory/migration 1→2/fixed first+idempotent bootstrap/inventory/revision/audit PASS |
| G3-NP-LOCAL / API startup+online preflight | exact trees committed by the verified full SHAs above | dedicated API startup/readiness + local online preflight | 0 | PASS | strict explicit CA pin；TLS/discovery/JWKS/callback、health/ready、两个 401、Tasks edge+direct 404 PASS；no system trust mutation |
| S6 / Desktop UI policy wiring | implementation `cf0e080e4cf2fa10e1394aead67c669574714a4d`；final `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` | default-off total policy→lazy route guard→AppShell/Settings recovery→DOM/AX/router/browser/Tauri gates | 0 | PASS / REMOTE VERIFIED | 18 frontend files/113 tests + 36 Rust；S6-REV-001—005 resolved；no Tasks/Rust lifecycle/production change |
| S7 / cross-repo bearer+Keychain | Desktop `155854cf...` / Infra `f040492e...`；API `faeb78019d...` | real system-browser Code+PKCE/exact loopback；strict access JWT；isolated Data Protection Keychain；refresh fault cleanup；all owning-repo gates | mixed | BLOCKED / FROZEN / REMOTE VERIFIED | refresh cleanup + offline/online PASS；access JWT fails `not_before_missing` before tenant calls；Keychain fails `-34018` with 0 signing identities；2×2/perf NOT RUN；no release/tag |
| S8 / release | N/A | requires S7 PASS + G5 approval | N/A | NOT RUN | no tag/release changes |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-PACKAGE | yijie | `check-feature-package.sh --gate G2 <feature-dir>` | Bash | 0 | PASS | 2026-08-01：required 12 files；G2 scope 无模板未完成标记；不代表 G4/G5 通过 |
| V-STRICT | yijie | `check-feature-package.sh --strict <feature-dir>` | Bash | 0 | PASS | 12 份需求包文件无模板变量或未完成标记 |
| V-DIFF | yijie | `git diff --check` + status/scope checks | Git/rg | 0 | PASS | 本轮仅 FEAT-125 00—10/feature.yaml 与 ADR-0012 的 G3-NP-LOCAL evidence/status 更新；最终提交前仍须复跑 |
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
| V-DESKTOP-INSTALL | yijie-desktop | `pnpm install --frozen-lockfile` | pnpm 11 | 0 | PASS | S6 exact lockfile install；no peer failure |
| V-DESKTOP-LINT | yijie-desktop | `make lint` | ESLint/Vue TSC/rustfmt/Clippy `-D warnings` | 0 | PASS | S6 frontend + unchanged Rust boundary clean |
| V-DESKTOP-TEST | yijie-desktop | `make test` | Vitest/Cargo | 0 | PASS | S6 frontend 18 files/113 tests；Rust 36 tests + doc-tests |
| V-DESKTOP-BUILD | yijie-desktop | `make build` + `pnpm docs:build` + `pnpm tauri:build --debug` | Vite/VitePress/Tauri macOS | 0 | PASS | production web/docs；lazy business chunks；debug `.app` + aarch64 `.dmg` |
| V-DESKTOP-AUDIT | yijie-desktop | `pnpm audit --audit-level high` + `cargo audit --file src-tauri/Cargo.lock` + JS license scan | npm/RustSec/pnpm | 0 | PASS | npm 0 known；Rust 0 vulnerabilities/17 allowed warnings；11 license groups/no prohibited group |
| V-DESKTOP-S6-BROWSER | yijie-desktop | real Vite browser flag-off + flag-on unavailable; route/collapse/reload/layout/log checks | in-app browser 1280×720 | 0 | PASS | `/`/`/chat` fail closed to Settings；protected links/input=0；72px persists；no overflow or browser error/warn |
| V-DESKTOP-S5A-REVIEW | yijie-desktop | structured review：scope→OIDC→token lifecycle/concurrency→Keychain→IPC/HTTP→dependencies/failure | Codex separated review pass | 0 | PASS | 6 类 findings resolved；最终开放 P0/P1/P2=0；EXC-125-002；真实 IdP/provisioning NOT RUN |
| V-INFRA-TEMPLATE | yijie-infra | `pnpm validate:feat-125-template` | Node 26 / yaml 2.9.0 | 0 | PASS | historical generic nonproduction template evidence：保留域名、public-client placeholder、合成数据、三端 flags false |
| V-INFRA-TEST | yijie-infra | `pnpm test` | Node test runner | 0 | PASS | historical generic preparation：19/19；remote commit `2f01f22...`；不代表 local runtime PASS |
| V-G3-MIGRATION | yijie-api + local PostgreSQL | `make migrate-up && make migrate-status` | Go 1.26.5 / PostgreSQL 16 | 0 | PASS | migration `00002_expand_identity_tenancy_rbac.sql` applied；schema version 2 |
| V-G3-FLAG-OFF | yijie-api + local dependencies | temporary `YIJIE_ENV=nonproduction` server, API/Desktop projection flags false；GET health/ready/tenants | Go / curl | 0 | PASS | health database connected、ready；`GET /v1/me/tenants`=`404`；server stopped after smoke |
| V-G3L-API | yijie-api `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | `make generate-check CONTRACTS_DIR=../yijie-contracts`、`make lint`、`make test`、`make test-integration`、`go mod verify`、`git diff --check` | Go 1.26.5 / PostgreSQL 16 | 0 | PASS | exact contract pin；local DB/tracked-matrix guard、bootstrap/service-profile/startup bind、reconciliation/fault gates PASS；coverage bootstrap CLI 32.4%、nonprodbootstrap unit 34.3% / integration 83.2%、authn 83.8%、authorization Postgres 76.2%、Tasks Postgres 76.9%；提交前 exact tree 门禁通过，提交后 remote SHA verified |
| V-G3L-DB | yijie-infra + local PostgreSQL | `make feat-125-local-api-db` + pre/post read-only inventories | PostgreSQL 16 | 0 | PASS | exact `yijie_api_feat125_local`；migration 前 public tables=0；migration 1→2 PASS；bootstrap 前 users/identities/tenants/memberships/role_bindings/audits/tasks 均 0 |
| V-G3L-BOOTSTRAP | yijie-api final profile + dedicated local DB | four tracked synthetic manifests with explicit `BOOTSTRAP_PROFILE=feat-125-local-lab`, then exact idempotent reruns | API bootstrap CLI / PostgreSQL | 0 | PASS | manifest SHA-256：user-a/tenant-a `321e323a4b717599fff612477055a558e0fdb96d9a4ce3bcbc57a3400555aa2e`、user-a/tenant-b `a1c2914f909ef3fe76878e766fe4d532bd72f690e92d44d5cc310193f3949154`、user-b/tenant-a `d8d91821d927935bb1f6c96eb070a3ac7614b05838225d6967c2c27ea0f13ece`、user-b/tenant-b `6d7e81b1f52ccd21fbd600d4407874fbb2a471f399655c6f3fcf6ad3ea876f2b`；first runs `state_changed=true`, revisions 2/2/3/3；second runs all false/revision 3/diff `[]`；final users2/identities2/tenants2/active memberships4/roles4/role_permissions18/role_bindings4/tasks0；audits 4 changed + 4 unchanged, all `synthetic_only` |
| V-G3L-DESKTOP | yijie-desktop `446b4d608546fca8f53f4582201d6b43ef6f762d` | `make lint`、`make test`、`make build`、`pnpm docs:build`、`pnpm audit --audit-level high`、`cargo audit --file src-tauri/Cargo.lock`、`pnpm tauri:build --debug` | pnpm/Rust/Tauri/macOS | 0 | PASS | frontend 9 files/37 tests；Rust 36 + doc-tests；local CA/Keychain environment binding and rejected-401/refresh compare-and-clear security gates PASS；debug app/dmg unsigned；signed Keychain/browser E2E NOT RUN；remote SHA verified |
| V-G3L-INFRA | yijie-infra `298192e386a7f7b81e8f0f8fe733c1f79f096ab4` | `make lint`、`make test`、Compose config、zsh syntax、`git diff --check` | Node 26 / pnpm 11 / Docker Compose | 0 | PASS | 71/71 tests + lint/Compose/shell/diff PASS；pinned assets/config/profile/preflight、dedicated API DB preparation/exact profile guard、both unauth endpoints/Tasks boundaries、read-only-before-mutation live Keycloak conformance/profile-drift test、secret no-clobber/rollback safety 与 trust-helper CA binding validation PASS；remote SHA verified |
| V-G3L-LOCAL-UP | local Keycloak/PostgreSQL/Caddy | `make feat-125-local-up` + `make feat-125-local-status` | Docker Compose | 0 | PASS | three dedicated services healthy on loopback-only published ports；no existing shared services or volumes stopped/deleted |
| V-G3L-PROVISION | local Keycloak through Caddy | `make feat-125-local-provision-users` | Node/HTTPS | 0 | PASS | before any mutation, read-only checks proved exact realm/clients、full two-user inventory 及 core/attribute state；profile migration was allowed only from exact default profile + empty attributes，unexpected profile/attributes fail before PUT/reset；final canonicalized scope sets、explicit `userinfo.token.claim=false` audience mapper、strict managed `data_classification` user profile（omitted field means unmanaged disabled under Keycloak 26.7 REST）与 exactly two fixed identities conformed；password resets/HTTPS provisioning PASS；admin refresh revocation returned `invalid_grant`；credentials not printed/committed |
| V-G3L-OFFLINE-READY | local Infra + exact API/Desktop trees | `make feat-125-local-prepare ...` + `make feat-125-local-ready ...` using final reviewed refs | Docker/Node/X.509 | 0 | PASS | public CA `07a3bb2ef51a5b559fe42b423339f6c886c5e17903b1cf2d8ca26bf1b5574650`, 627 bytes, owner `jack`, mode `0600`；single-PEM/path/digest, loopback DNS/origins, exact refs, pinned images/config/profile and no-insecure/no-secret policies passed；trees now equal committed SHAs |
| V-G3L-RUNTIME-ONLINE | local Keycloak/Caddy/API | `make feat-125-local-online ...` using final reviewed refs | Docker/Node/HTTPS | 0 | PASS | discovery/JWKS、exact callback accept/wrong-path reject、health/ready、两个 unauth 401、Tasks edge/direct 404 PASS；trees now equal committed SHAs |
| V-S7-DESKTOP | yijie-desktop `155854cf3662384caa2c8bffe0a47935ef4a70b5` | `make lint && make test && make build` | pnpm/Rust/Tauri | 0 | PASS | generation pin clean；113 frontend tests；38 Rust PASS + 1 intentional ignored；Clippy `-D warnings`/build PASS；refresh cleanup fault tests PASS；remote verified |
| V-S7-INFRA | yijie-infra `f040492e7c4af4aa7cc94a343140c58befae3af2` | `make lint && make test` | Node 26 / Docker Compose | 0 | PASS | 76 tests；Keycloak `basic/sub`/synthetic-name reconciliation、CA user-domain trust verification、strict bearer harness assets PASS；remote verified |
| V-S7-API | yijie-api `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | `make lint && make test && make test-integration` | Go 1.26.5 / PostgreSQL 16 | 0 | PASS | vet、race unit、integration PASS；worktree clean |
| V-S7-PREFLIGHT | yijie-infra + local stack/API | exact candidate double-sample；`make feat-125-local-ready`；`make feat-125-local-online` | Node/Docker/HTTPS | 0 | PASS | Desktop candidate digest stable；local-lab ready + discovery/JWKS/callback/health/ready/unauth 401/Tasks 404 PASS |
| V-S7-BEARER | cross-repo real local OIDC | `make feat-125-s7-bearer-matrix` | system browser + pinned Keycloak/Caddy/API | non-zero expected blocker | BLOCKED | user-a real Code+PKCE/exact callback/code exchange；ID token and access JWT RS256/issuer/subject/exact audience reached；access token lacks required `nbf` and is rejected before tenant API calls；refresh revoked；2×2/perf NOT RUN |
| V-S7-KEYCHAIN | yijie-desktop/macOS | ignored isolated Keychain smoke + `security find-identity -v -p codesigning` | Data Protection Keychain | non-zero expected blocker | BLOCKED | write fails `-34018: A required entitlement isn't present`；0 valid identities；no smoke/production credential persisted |
| V-S7-CA-CLEAN | yijie-infra/macOS | exact fingerprint `make feat-125-local-untrust-ca`；then `make feat-125-local-ca-status` | user login Keychain trust settings | remove=0；status=non-zero expected | PASS | exact SHA-1 trust entry removed；no broad certificate/Keychain deletion；API explicit CA pin unchanged |

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
| Consumer conformance | exact candidate `9ec34abd...` + generated TS `77babb...` | Desktop generated adapter/store canonical/fault/concurrency/security tests | PASS | S5B final `f94ac34...` remote verified；cross-repo remains S7 |
| Agent Host/Runtime regression | Agent Host remains v0.2.0 | structured manifest comparison | CONTRACT PASS / integration deferred | Runtime semantics unchanged；真实部署前恢复 S7 集成 |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-001/003 | access handlers + `internal/platform/authn` + identity mapping | SEC-001/004/007 | exact-single aud、RS256/claims/TTL/key rotation、duplicate header、401/403/503 conformance | API PRODUCER PASS |
| AC-004 | canonical tenant header + atomic active user/tenant/membership/RBAC query | SEC-002 | 400 invalid、403 denied、2×2 PostgreSQL integration | API PRODUCER PASS |
| AC-002/005 | tenant discovery/projection endpoints + stable HTTP faults | API/RES | canonical 0/1/multiple、ready/empty、400/401/403/500/503 fixtures | API PRODUCER PASS |
| AC-006/007/011/012 | Desktop generated permission client/store | DESK/RES/SEC | exact generated types、fixed operations、canonical fixtures、0/1/multiple、revision/expiry/context、concurrency/fault/security | S5B PASS |
| AC-008—010 | Desktop nav/router/AppShell/Settings recovery | DESK/A11Y | total capability projection；allowed-published link、allowed-unpublished disabled “即将开放”、denied DOM/AX absence；denied deep-link loader call=0 | S6 LOCAL PASS |
| AC-013/015 | endpoint auth + tenant/RBAC authority；Tasks isolation/cross E2E pending | SEC-002/003/E2E-001 | API endpoint + 2×2 DB matrix PASS；local host profile/Caddy online edge+direct 404 PASS；cross-repo NOT RUN | PARTIAL |
| AC-014 | v0.3.0 source/generated candidate + exact provenance | CT-002/SUP-001 | S1/S2 contract gates + API and Desktop exact pin/drift | CONTRACT+API+DESKTOP PIN PASS |
| AC-016 | FEAT-124 verification report | REV-001 | FEAT-125 incomplete | NOT RUN |
| AC-017/018 | Desktop native system-browser OIDC、exact loopback、state/PKCE/nonce、Keychain/token lifecycle、operation-scoped authenticated transport | OIDC-001/SEC-005/011/012 | S5A baseline + G3 local CA/Keychain binding/401-refresh race fix；S7 真实 code+PKCE 已到达 access JWT 校验，但 provider 缺 required `nbf`；Data Protection Keychain 因 `-34018`/0 signing identities 阻断；family reuse 未证明 | STATIC CANDIDATE PASS / S7 EXECUTED BLOCKED |
| AC-019/020 | exact 7-capability/2-role matrix + root/deep-link policy | API-004/E2E/DESK | API DB/bootstrap 2×2 PASS；Desktop root `task.create→/chat`、`task.read→/tasks`、else `/settings` 与 denied lazy guard PASS；S7 live matrix 未越过 JWT/Keychain 前置 | PARTIAL / S7 BLOCKED |
| AC-021 | ingress deny + approved host service profile handler non-registration + Desktop non-use | SEC/DEPLOY/E2E | local `feat-125-local-lab`/Caddy online edge+direct 404 PASS；default legacy profile unchanged | LOCAL G3 PASS / production pending |
| AC-022 | local environment integrity | G3L-001—007 | pinned/config/static gates + dedicated API DB empty inventory/migration/tracked bootstrap + local dependencies/live realm/HTTPS provisioning/offline ready PASS；core online discovery/JWKS/callback、health/ready、两个 401、Tasks edge/direct 404 PASS | G3 PASS |
| NFR-001/002/006/007 | fail-closed endpoints、tenant FK、exact pin、secret-free diff | SEC/DB/SUP | S3/S4 unit/integration/drift/audit | API PRODUCER PASS |
| NFR-003—005/008 | endpoint fault recorder、Desktop native auth/transport security；staging perf pending | mapped in 06 | S4 faults + S5A native security + S6 browser/component accessibility PASS；staging perf/cross-repo NOT RUN | PARTIAL |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| E2E | API→Desktop | `tenant_owner`（7 capabilities）/`tenant_member`（仅 task.create/task.read）×2 tenants | BLOCKED before 2×2 calls | S7 real system-browser/code+PKCE reached strict access-JWT validation；provider omitted required `nbf` |
| Native auth/security | exact `/oauth/callback`、state/PKCE、ID-token nonce、10m access、single-flight refresh、Keychain rotation/reuse、固定两 GET operations、zero token IPC/generic proxy | S5A local mocks/unit + G3 CA/Keychain binding + S7 real-browser/isolated Keychain smoke | STATIC PASS / S7 BLOCKED | code+PKCE reached access JWT；signed Keychain smoke failed `-34018` with 0 signing identities；provider refresh family still unproven |
| Security/tenant | API access-JWT verifier、JWKS、identity/active membership、atomic RBAC projection | generated RSA keys + PostgreSQL 16；local Keycloak/Caddy HTTPS healthy；dedicated API ready | S4 API PRODUCER + G3 live realm/offline ready/discovery/JWKS/bootstrap PASS | API startup/readiness and Tasks edge/direct isolation PASS；signed bearer lifecycle remains S7/G5 |
| Failure/resilience | 400/401/403/500/503、no-store/challenge/retry、dependency faults | canonical/fake dependency matrix | S4 API + S5A transport + S5B adapter/store fail-closed PASS | cross-repo remains S7 |
| Migration rehearsal | 00001→expand/rollback metadata + synthetic bootstrap | PostgreSQL 16 local | PASS | existing task/audit retained；generic locator/append-only/FK/down refusal + bootstrap first/idempotent/audit/revision verified；production bootstrap remains G5 |
| Performance | projection 50 RPS candidate | staging | NOT RUN | S7 |
| AI Eval | no AI behavior | N/A | N/A | scope |
| Visual/accessibility | hidden/disabled/recovery | component DOM/AX + Vite browser 1280×720 + Tauri debug build | S6 LOCAL PASS | flag off/on-unavailable fail closed；72px persisted；no overflow/error log；ready role matrix covered by component tests；signed native E2E remains S7 |

## 8. Diff 与制品完整性

- [x] `git status` 已逐仓复核；Contracts、API、Desktop、Infra clean/equal remote，yijie 仅有本轮 FEAT-125/ADR 收口文档
- [x] 实现仓提交前 tracked + untracked diff whitespace 检查通过；三个实现仓提交后 clean
- [x] diff/status 范围复核：yijie 仅 FEAT-125/ADR；Infra 为 G3 local profile/validator/preflight/runbook；API 为 bootstrap/issuer/service-profile/loopback bind；Desktop 为 local CA/Keychain environment binding；Contracts 与 Tasks wire 未改
- [x] 三个实现仓的 deterministic candidate exact trees 已形成新完整提交；未把 base HEAD 误称为本轮实现 SHA
- [x] API `faeb78019d...`、Desktop `446b4d6085...`、Infra `298192e386...` 已推送并由 `git ls-remote` 核验
- [x] 生成物来自锁定 generator：openapi-typescript 7.13.0 / oapi-codegen 2.7.2，重生成漂移检查 PASS
- [x] Go module/lock 变化仅为 exact oapi-codegen v2.7.2 tool 与 jwx v3.2.0/httprc v3.0.6 及其解析依赖；advisory/license 已审计
- [x] migration v2 digest `51c4ced9...`；00001 upgrade/append-only/composite FK/expand-only rehearsal PASS；无真实 seed/session 表
- [x] 新增 3 个 contract tests 与 12 个 fixture；无 `.skip`、`.only`、弱化断言或关闭门禁
- [x] S5A lock digests：`src-tauri/Cargo.lock`=`94b1ee21ed1bd9e4e97528622971da9241c43c4e497181ec83f77f2da6a5b973`；`pnpm-lock.yaml`=`aaa0a300afb760c0a768aebefcf338bdbbb66dd6a62a3a907d456d0246fedc0c`
- [x] S5A dependency exception EXC-125-002 已限定为 `openidconnect→rsa` 的 RS256 公钥验签路径；无 RSA 私钥/签名/解密，G5 或上游修复时必须重审/移除
- [x] S5B exact contract lock=`9ec34abd6e7dfb5a23b0154d467694167224ebbb`；source=`7bd40dd1...`；generated TypeScript=`77babb21...`；generator=`openapi-typescript 7.13.0` + isolated TypeScript `5.9.3`
- [x] S5B Desktop final `f94ac343881b0f7df59c0f5f4169372e612fd019` 已推送并由 `git ls-remote` 核验；它是 S6 基线；S6 只改前端 UI/nav/router/store initialization/tests/docs/package lock，未改 Tasks/Rust lifecycle/contracts generated/production config
- [x] S5B GitHub Actions run `30695055988` 对 final SHA 完整执行并 PASS；exact contracts checkout、Desktop-only test discovery、build、native bundle 与 audits 均通过
- [x] S6 implementation `cf0e080e4cf2fa10e1394aead67c669574714a4d`、final `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` 已远端核验；`pnpm-lock.yaml`=`649b6c2c...`；debug DMG=`207757ad...`
- [x] 历史 generic G3 template digest `b7d1eb27...`、validator `2e59197e...`、online CLI `1b541ab9...`、runbook `f819fa2f...` 仍可追溯；当前 G3-NP-LOCAL 使用远端完整提交且不伪造 image/CA/runtime digest
- [x] Compose profile namespace `feat-125-local`、API service profile `feat-125-local-lab` 与 Desktop auth environment `local-integration` 保持三个不同边界；文档不再互相混称
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

结构化 G3 generic preparation 历史 review findings：

| Finding | Severity | 结论 | 修复/证据 |
|---|---|---|---|
| G3-REV-001 | P1 | 初版 online preflight 只读 JWKS，未证明 discovery issuer/endpoints 与获批配置一致 | 增加 discovery exact-match，并要求 code、PKCE S256、RS256；drift 负测 PASS |
| G3-REV-002 | P2 | 初版 256 KiB 上限在 `arrayBuffer()` 后检查，超大响应可能先占用无界内存 | 改为 ReadableStream 分块读取，超过 256 KiB 立即 cancel；负测 PASS |
| G3-REV-003 | P2 | 初版 health/ready 只要求 JSON object，错误服务或 production endpoint 可能误通过 | health 必须精确识别 `yijie-api`、`nonproduction`、DB connected/status ok，ready 必须为 ready；production 负测 PASS |

Generic preparation review 后开放 P0/P1/P2 findings = 0；该结论只对应已提交的供应商中立
准备层，不覆盖当前 G3-NP-LOCAL candidate。

结构化 G3-NP-LOCAL closeout findings：

| Finding | Severity | 结论 | 处理/证据 |
|---|---|---|---|
| G3L-BLK-001 | P1 / closed historical blocker | API projection startup 原使用默认 HTTPS client 拉取 JWKS | local-only explicit CA PEM + lowercase pin、strict file validation、isolated client；offline/core online PASS，未修改系统 Keychain |
| G3L-REV-001 | P1 / resolved | Desktop 第二次 `401` 清理可与并发 refresh 竞态，已退出后可能重写 Keychain | 在同一 `refresh_lock` 下按 rejected access token compare-and-clear；新 token 不被旧请求删除；2 条定向并发测试和 Rust 36-test suite PASS |
| G3L-REV-002 | P1 / resolved | 持久 Keycloak DB 中 realm/client/scope/mapper/user-profile/user 漂移可绕过仅首次 import，或在完整只读核验前被 provisioner 改写 | 任何 mutation 前经 pinned HTTPS 核验 exact realm/clients、full two-user inventory/core/attribute state；仅 exact default profile + empty attributes 可迁移，unexpected profile/attributes 在 PUT/reset 前 fail closed；最终 canonicalized scope sets、explicit `userinfo.token.claim=false` audience mapper、strict managed `data_classification` user profile（Keycloak 26.7 REST 中 omitted field = unmanaged disabled）与 exactly two fixed users、password reset、refresh revocation `invalid_grant`、profile-drift 负测和真实 live conformance PASS |
| G3L-REV-003 | P2 / resolved | PostgreSQL commit 已成功但确认丢失时，bootstrap 可能追加与 success 矛盾的 failure audit | 区分确定 rollback 与未知 outcome；按 exact request ID/预期 audit 对账，无法确认时返回稳定 `outcome unknown` 且不写矛盾 audit；fault/integration tests PASS，nonprodbootstrap integration coverage 83.2% |
| G3L-REV-004 | P2 / resolved | secrets 文件丢失/损坏时 `stop/status` 也被阻断 | 仅 `up` 要求并校验 secrets；`stop/status/export-ca` 不解析 credential；回滚安全定向测试 PASS |
| G3L-REV-005 | P2 / resolved | 并发 secrets 初始化可覆盖，校验后重新 `source` 路径存在 TOCTOU | 以 atomic hard-link no-clobber 发布；Node 一次严格解析并在内存 Map 中消费，不执行 shell source；并发/格式/权限负测 PASS |
| G3L-REV-006 | P3 / resolved | 未来 macOS trust helper 原未复用严格 CA 校验 | 任何 install/status/remove 前均校验 owner/mode/64 KiB/single CA PEM/渲染配置 SHA-256 pin；helper 本轮仍未执行、不计入 G3 PASS |
| G3L-REV-007 | P3 / resolved | 文档仍保留修复前的 Desktop/Infra 测试数 | 最终稳定工作树复跑并统一登记 Desktop frontend 37 + Rust 36、Infra 71/71；Infra lint/Compose/shell/diff 同步 PASS |
| G3L-REV-008 | P1 / resolved | local bootstrap 只校验 nonproduction/非空 DSN，可能误连共享或真实数据库；ignored manifests 也不能进入候选 provenance | `feat-125-local-lab` 在 DB 访问前锁死 exact issuer、credentialed loopback `yijie_api_feat125_local` DSN 结构与四份 tracked 2×2 tuple；unknown/drift/no-credential fail closed 且不泄漏 DSN；专用空库 migration/inventory/首次+幂等 bootstrap 对账 PASS |
| G3L-LIM-001 | deferred production S7/G5 blocker | Keycloak 可证明 rotation，但现有 provider 证据不证明 reuse 自动撤销整个 token family | 固定 `provider_limit_documented`；不阻断本地业务开发，不得写成 A2/S7/G5 PASS |
| G3L-DOC-001 | documentation correctness | Compose `feat-125-local`、API `feat-125-local-lab`、Desktop `local-integration` 原容易被混称；默认 API profile 仍保留 legacy Tasks wire | 文档统一按各自 namespace 命名；只宣称 local host profile 不注册 Tasks，online edge/direct 404 PASS |
| G3L-DOC-002 | rollback safety | 仅停止 containers 不会停止运行于宿主的独占 API，可能残留 projection/local issuer 环境 | 回滚明确先停止 `127.0.0.1:18080` 宿主 API、清 local env，再停止 Compose；不得停止其它用户宿主 API 进程 |
| G3L-PROV-001 | provenance / resolved | dirty worktree 的 base HEAD 不能登记为本轮完整 SHA | 提交前使用 `candidate:<base>:<tree-digest>`；提交后已替换为 API `faeb78019d...`、Desktop `446b4d6085...`、Infra `298192e386...` 并远端核验 |

结构化复审发现的 3 个 P1、3 个 P2 和 2 个 P3 实现/证据问题均已修复并复验；
API G3 可修复 P0/P1/P2 开放数为 0；`G3L-BLK-001` 已关闭，P3 测试增强不阻断。
历史 Desktop P2 `S5A-REV-OPEN-001` 不属于 G3 PASS；已在 Desktop `155854cf...` 修复、复验并远端核验。

结构化 S7 review findings：

| Finding | Severity | 结论 | 处理/证据 |
|---|---|---|---|
| S5A-REV-OPEN-001 | P2 / resolved in `155854cf...` | invalid refresh 未撤销当前 token；rotated token Keychain save failure 未撤销新 token | 两条路径统一 revoke+clear fail closed；两条 exact-token fault tests；Desktop 全门禁与 remote SHA PASS |
| S7-INT-001 | blocker / provider compatibility | Keycloak 26.7 access JWT 缺少 API/ADR 已批准的 required `nbf` | strict harness 在 bearer 使用前拒绝 `not_before_missing`；未修改 API、契约或关闭验证；需要获批兼容 IdP 或另行审批契约变更 |
| S7-INT-002 | blocker / native signing | 当前 Mac 没有匹配 entitlement/code-signing identity，Data Protection Keychain 无法建立真实 item | isolated smoke `-34018`；0 valid identities；需签名/provisioned native candidate 后复跑 |
| S7-INT-003 | blocker / provider lifecycle | pinned Keycloak 仍只证明 rotation，不证明 reuse 自动撤销 family | 保持 `provider_limit_documented`，不得作为 S7/G5 PASS |
| S7-REV-001 | P1 / resolved | 初始 Keycloak client 缺内建 `basic` scope，access JWT 没有 `sub`；synthetic users 缺姓名会触发首次登录 profile update | exact built-in scope/mappers 与 legacy migration fail closed；fixed names + drift tests；真实 code flow 已越过 `sub`/profile blocker |
| S7-REV-002 | P1 / resolved | macOS trust helper 将 admin trust domain 与 user Keychain 混用，且只检查证书存在会产生 false PASS | 改为 user-domain trust；同时核验 exact cert fingerprint 与 trust-settings entry；有/无 trust 回归测试和 live status PASS |
| S7-CLEAN-001 | cleanup / complete | 浏览器联调所需 local CA user trust 不应在阻断后遗留 | 按 exact SHA-1 删除唯一 trust entry；删除命令 exit 0，随后 status 按预期非零；未删除其它证书或 Keychain 项 |

S7 review 后本轮实现开放 P0/P1/P2 finding = 0；上述三个 blocker 是未满足的 provider/签名
前置，不是已接受例外。S7/G4/G5 继续关闭。

结构化 S5B review findings：

| Finding | Severity | 结论 | 修复/证据 |
|---|---|---|---|
| S5B-REV-001 | P1 / resolved | generator workspace 若使用 root TypeScript 6 会越过 openapi-typescript peer 范围 | 隔离 generator workspace 并固定 TypeScript 5.9.3；frozen install/generate drift/peers PASS |
| S5B-REV-002 | P2 / resolved | 调用前已取消的 operation intent 仍可能触发 native request | pre-aborted signal 在 invoke 前 fail closed；定向负测 PASS |
| S5B-REV-003 | P2 / resolved | 相同 revision 但 capability 集变化可能绕过 rollback-only 检查 | 同 revision 必须保持 canonical known capability set 一致；drift 负测 PASS |
| S5B-REV-004 | P2 / resolved | 仅使用 `Date.parse` 会接受被规范化的非法日期 | 强制严格 RFC3339 日历往返校验、未来且不超过 5 分钟；日期/expiry 负测 PASS |
| S5B-REV-005 | P1 / resolved | 首次远端 CI 的脚本级 contracts 变量被 Makefile 默认路径覆盖 | workflow 使用正式 `CONTRACTS_DIR=.contracts-source` 输入；exact checkout 检查在 CI PASS |
| S5B-REV-006 | P1 / resolved | 仓内 contracts checkout 被 Vitest 默认发现，误执行未安装依赖的 Contracts tests | Desktop test command 排除 `**/.contracts-source/**`；本仓 12 files/80 tests 保持 PASS |

S5B review 后开放 P0/P1/P2 findings = 0；结构化复审未冒充独立 G4。

## 9. 独立 Review Findings

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| G1-001 | P1 / local boundaries resolved, integration pending | Contracts/API/Desktop auth scan | 原基线无可信身份或活动租户 | API S3/S4、Desktop S5A/S5B 与 G3 local config/offline/core online PASS；跨仓链路仍待 S7 | S7 |
| G1-002 | P1 / release control | API Tasks handler/repository/migration | legacy Tasks 仍无资源级授权，不能随 FEAT-125 暴露 | A6：默认 legacy profile/wire 不变；local host profile+Caddy static deny rules PASS 且 Caddy 健康，但 online edge/direct 404 PASS；生产宿主 profile/ingress 待 G5，资源授权由 FEAT-126 完成 | G3 online/G5/FEAT-126 |
| G1-003 | P2 / FEAT-124 blocking | Desktop AppShell/nav/router | default `{}` + missing→visible、无 guard | S6 已删除 optional/default projection、完成 total policy/lazy guard并远端核验；等待 S7/独立 G4 关闭验证 | S7/FEAT-124 G4 |
| G1-004 | P2 / delivery blocking | API/Desktop generation | floating sibling 与 placeholder generate，无法追溯 wire | API S3 与 Desktop S5B 均已固定 exact source/generated SHA+generator+CI drift | Closed in S5B；S7 复用 |
| G1-005 | P2 / write-path pending | API database/audit | 无 RBAC tables；audit resource FK 只支持 task | S3 migration + S4 atomic projection + G3 synthetic bootstrap first/idempotent/audit/revision PASS；production writer/admin path remains later | S7/G5 |

- Reviewer 是否独立于实现上下文：设计阶段采用 Contracts、API、Desktop 三个并行只读
  reviewer pass；本轮按六维清单重新读取最终 implementation diff 并完成 structured review。由于仍在同一
  Codex 任务内，它不冒充最终独立 G4；G4 继续 Pending。
- P0/P1 G3 阻断已清零；G3L-BLK-001 已关闭。Desktop P2
  `S5A-REV-OPEN-001` 已在 Desktop `155854cf...` 修复；`S7-INT-001/002/003` 作为真实部署前
  恢复 S7 的强制阻断项保留，当前本地业务开发不受其阻断。
- P2 例外批准：无；不允许用例外关闭 FEAT-124 G4-001。

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| direct JWT/native auth/tenant | S7 real browser/code exchange reached access JWT validation；Keycloak token lacks required `nbf` | high | before real deployment: approved IdP with conformant access JWT, then rerun full 2×2 | 段成威 | deferred production blocker；not local business-dev blocker |
| RBAC/migration/audit | S3 migration + S4 projection + G3 synthetic bootstrap first/idempotent/audit/revision PASS；生产 writer/admin path 未实现 | high | S7/G5 production-control evidence | 段成威 | yes |
| API producer | endpoint/conformance/metrics recorder 已远端核验；staging/performance/exporter 未验证 | high | S7/G5 | 段成威 | yes |
| Desktop consumer | S5A—S6 已远端核验；refresh fault cleanup candidate PASS；signed Keychain smoke `-34018` | high | before real deployment: signed/provisioned native candidate + full S7 rerun | 段成威 | deferred production blocker；not local business-dev blocker |
| G3 local runtime | local issuer/client/JWKS/API origins、explicit CA pin、offline ready 与 core online PASS | low | N/A；G3 complete | 段成威 | no |
| Tasks 双隔离/FEAT-126 | default legacy profile/wire unchanged；local host profile/Caddy static deny PASS but online 404 PASS；production isolation not implemented | critical | G3 online local 404；G5 approved host profile/ingress evidence；FEAT-126 production enablement before deadline | 段成威 | yes |
| Provider refresh family | local Keycloak proves rotation but not automatic reuse-revokes-family | high | resumed S7 auth-lifecycle against selected provider or approved compensating/provider change | 段成威 | deferred production blocker；not local business-dev blocker |
| Provider `nbf` compatibility | Keycloak 26.7 access JWT omits required claim even though code flow/RS256/audience/sub pass | high | before deployment select conformant provider or separately approve ADR/contract/API change | 段成威 | deferred production blocker；not local business-dev blocker |
| Native signing entitlement | current host has 0 valid code-signing identities; Protected Data Keychain returns `-34018` | high | Apple Development provisioning/entitlement and signed native candidate | 段成威 | deferred production blocker；not local business-dev blocker |
| Production IdP/infra/signing | local A7 values fixed；production issuer/client ID/JWKS、DNS/TLS/API origin/CSP/control plane remain undefined | high | G5 production plan+evidence | 段成威 | yes |
| Desktop RSA dependency advisory | `openidconnect 4.0.1`→`rsa 0.9.10` 无修复版本；当前仅公钥验签 | medium if scope drifts | EXC-125-002；每次 audit；G5/上游修复时移除 | 段成威 | yes for production review |

## 11. 结论

- Local Engineering Baseline Complete：是；允许在合成数据、flags 默认关闭和服务端安全边界不降级的前提下继续业务开发。
- Production Code Complete / Activation Ready：否；G4/G5/G6 均未通过。
- 验证人：Codex（需求/设计只读审核）；业务/技术/安全 Owner 为段成威。
- 日期：2026-08-01。
- 结论依据：A1—A7 已由段成威批准，G1/G2 于 2026-07-31 Passed，G2A 于 2026-08-01
  Passed；S1/S2 已在
  2026-08-01 形成 candidate `9ec34abd...` 并通过生成、全门禁、breaking check 和
  semantic review，且 origin/develop 已核对为同一完整 SHA。S3 API exact pin、migration、
  authn/identity/tenancy/RBAC 已推送为 `fff0cbcba601181058ac3ab9151d2d7bbe06dcbf`。S4 API
  producer 已通过全部门禁/结构化审查并远端核验为
  `360a526b679147472e7cc82ca7ac9db9d18a371d`。S5A Desktop system-browser OIDC、exact
  loopback、PKCE/state/nonce、Keychain token lifecycle 与 operation-scoped transports 已通过
  全部门禁/安全矩阵/结构化审查并远端核验为
  `3798c67d260237928730758c7ec4c1fbe6fcf7d2`。当前 G3-NP-LOCAL 三仓实现已远端核验为
  API `faeb78019d...`、Desktop `446b4d6085...`、Infra `298192e386...`：全部仓内门、local stack/live realm、HTTPS synthetic user
  provisioning、offline ready 和 synthetic API bootstrap PASS；online preflight 实际执行，trusted
  core online 中 discovery/JWKS/callback、API readiness、
  两个未认证 401 与 Tasks edge/direct 404 PASS。G3 为 PASS。S5B Desktop exact pin、generated
  adapter 与内存 fail-closed store 已通过全门禁和结构化审查，并远端核验为
  `f94ac343881b0f7df59c0f5f4169372e612fd019`。S6 UI final
  `688fb72ddf3f9c8ba0f8edea55a0c3f66cdf364c` 已远端核验。S7 已执行：Desktop
  `155854cf3662384caa2c8bffe0a47935ef4a70b5` 与 Infra
  `f040492e7c4af4aa7cc94a343140c58befae3af2` 的全部仓门与 offline/online preflight PASS，
  两个 origin/develop SHA 已核验，历史 refresh cleanup P2 已修复；
  真实浏览器 Code+PKCE/exact callback/code exchange 到达 access JWT 后，因 Keycloak 26.7
  缺 required `nbf` fail closed；正式 Data Protection Keychain 因 `-34018` 与 0 signing identities
  无法运行，provider family reuse 仍未证明。因此 S7 以真实 `BLOCKED` 证据冻结、
  2×2/performance=`NOT RUN`；真实部署准备时必须恢复；
  S8/生产配置/激活继续禁止。
  FEAT-124 G4-001 继续阻断，直到 FEAT-125 producer/consumer/E2E 与独立 G4 证据完成。
