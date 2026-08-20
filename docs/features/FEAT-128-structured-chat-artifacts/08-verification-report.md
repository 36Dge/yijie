# FEAT-128 验证证据与审查报告

> 本报告只记录实际执行或可复核结果。Owner 决策来自用户的直接指令；Codex 负责执行、核对和记录，
> 不把自身描述成独立人工 Reviewer。G2A PASS 只证明契约与 downstream exact pin 已就绪，不证明
> Host/Desktop S3/S4/S5 以外的 type renderer、端到端或真实 provider 能力已经存在。

## 1. 验证上下文

| Repository | Branch | Evidence commit | FEAT-128 实际范围 | 日期 |
|---|---|---|---|---|
| `yijie` | `feat/feat-128-structured-chat-artifacts` | 本文档最终提交 | G2/G2A decisions + S3/S4/S5 G3 governance/evidence package | 2026-08-20 |
| `yijie-contracts` | `feat/feat-128-structured-chat-artifacts` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | S1/S2 authoritative source/generated/fixtures/review | 2026-08-20 |
| `yijie-agent-host` | `feat/feat-128-structured-chat-artifacts` | pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; S3 `4017785adb08e1114781d3d844e9a10a683fa933` | exact pin + local Host v3 lifecycle/staging/resource/synthetic foundation | 2026-08-20 |
| `yijie-desktop` | `feat/feat-128-structured-chat-artifacts` | Pattern `e97b2dabd724af856b4041e23b24437ec2f5dfc3`; pin `96094419d963745529ed0fa246919089e659f20d`; G2A record `35efa1475af4679b5974663593831d07759c3728`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45` | Pattern + pin + SQLCipher/native transfer/history/private IPC + provider-neutral domain/store/generic shell；S6-S9 未开始 | 2026-08-20 |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | read-only Runtime authority | 2026-08-20 |

没有 tag、push、契约发布、真实 provider 调用、云资源、部署或生产流量。Host S3 与 Desktop S4 均默认
关闭；Desktop 没有 type-specific renderer/CSP/save，Host 没有真实 provider producer。

## 2. Gate 时间线

| Gate/Slice | 结论 | Evidence | 授权效果 |
|---|---|---|---|
| G0/G1 | PASS | 00-03、requirements/impact/risks | 进入 G2 review |
| G2/S0 | APPROVED | 03 §2A/2B、04-07、Pattern 1.0.0 Accepted | 只授权 Contracts S1/S2 |
| S1 | PASS | v3 OpenAPI/SSE/report/Proto/AsyncAPI、四 kind fixtures 与负例 | 进入 locked generation |
| S2 | PASS | `ea48fe...`、generate/lint/test/build、双 breaking、semantic review | 允许 S2P exact pin preflight |
| S2P | PASS | Host `dea84d...`、Desktop `960944...` 与两个仓库全量门禁 | 只形成 provenance/conformance，不改变业务行为 |
| G2A | APPROVED | 全部 required evidence 已通过，用户的条件授权生效 | 可按依赖启动 S3、随后 S4 |
| S3 | PASS | Host `4017785...` + full Host gates | 允许按依赖进入 S4；不开放真实 provider |
| S4 | PASS | Desktop `09220dd...` + full Desktop gates | native foundation 完成；不等于 UI/E2E 完成 |
| S5 | PASS | Desktop `7548ea8aeacfd7274f1107786ce48ddc6789cd45` + RED/GREEN focused tests + full Desktop gates | generic domain/store/shell 完成；不等于 type preview 或 E2E |
| G3 S3/S4/S5 | PASS | planned scope、tests/build/docs、diff 与 clean worktrees | 下一计划切片为 S6；G4 仍 pending |
| S6-S11 | NOT RUN | 无对应实现 diff | 不得写成完成 |
| S12 real producers | BLOCKED | 无 provider authority/付费授权 | 保持关闭 |

## 3. Contracts 不可变候选

| Identity | Value |
|---|---|
| Version | `0.4.0 local candidate`；未 tag、未发布 |
| Full commit | `ea48fe190e18afba728712d1e2cc79cda57f581b` |
| Host OpenAPI | `cf72ba8dd6910e8454ad60feeffa5e82583303b441dad78e49910fbdb9f5420f` |
| AsyncAPI source | `e7ea38b310d406bf09441b11ff5e8a8f2931e3b246f99c51be7d10d27ac61090` |
| Session event v3 schema | `87b1284056529bde8314e6cfa6ad1fb27ffefef50ea86033875fda795330939f` |
| Report document v1 schema | `94715e5b821cca686405d06004b805e9eac6d39dc61e19c9fc38925102f79556` |
| v3 Proto | `5021a0342b84cdea0e1dd773728e4c8f013ce7d03377ade18f06f6716a81b70d` |
| Generators | `openapi-typescript 7.13.0`; `json-schema-to-typescript 15.0.4`; `oapi-codegen v2.7.2`; `protoc-gen-es 2.12.1`; `protoc-gen-go v1.36.11` |

Semantic review 位于 `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md`。它明确审查 v1/v2
隔离、`after` cursor、ACK/poster、ordinal、closed enums、report two-stage compatibility、limits、
synthetic/real provenance 与 activation gate。

## 4. 实际命令记录

| Check ID | Repository | Command | Exit | Result | 摘要 |
|---|---|---|---:|---|---|
| Y-PACKAGE | yijie | G3 package check + strict package check | 0 | PASS | S3/S4/S5 G3 structure、template variables 与未完成标记检查通过；不代表 G4 |
| Y-YAML | yijie | unique-key parse `feature.yaml` | 0 | PASS | machine-readable G3 S3/S4/S5 record valid；G4 仍 pending |
| Y-LINT-TEST | yijie | `pnpm lint && pnpm test && bash -n scripts/*.sh` | 0 | PASS | governance + repository tests + shell syntax |
| Y-DIFF | yijie | `git diff --check` | 0 | PASS | 07/08/10/feature.yaml 无 whitespace error |
| C-GENERATE | Contracts | `pnpm generate` | 0 | PASS | locked generated outputs clean，无 warning |
| C-LINT | Contracts | `pnpm lint` | 0 | PASS | sequential post-generate check 通过 |
| C-TEST | Contracts | `pnpm test` | 0 | PASS | Node `39/39` + Go 全部通过 |
| C-BUILD | Contracts | `pnpm build` | 0 | PASS | TypeScript SDK compile 通过 |
| C-BREAK-PUB | Contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | PASS | published `contracts-v0.2.0` compatibility |
| C-BREAK-CAND | Contracts | `./scripts/check-breaking.sh 747cf740f2d91e76e5c1a130e8e009f1efa821b8` | 0 | PASS | FEAT-127 `0.3.0` candidate compatibility |
| C-EQUALITY | Contracts | v1 wire equality against both baselines | 0 | PASS | v1 unchanged；v2 source/fixture equality retained |
| C-POST-COMMIT | Contracts | `pnpm test && pnpm lint` + both breaking commands | 0 | PASS | immutable commit post-check |
| H-SYNC | Host | `make sync-contracts` | 0 | PASS | exact checkout `ea48fe...`；snapshot sync clean |
| H-CONTRACT | Host | `make contract-check` | 0 | PASS | version/full SHA/digests/generated types match |
| H-LINT | Host | `make lint` | 0 | PASS | existing + pin-only diff clean |
| H-TEST | Host | `make test` | 0 | PASS | Go/race/coverage suites pass |
| D-PIN | Desktop | `pnpm generate:check` | 0 | PASS | public/v2/v3 all pin `ea48fe...` |
| H-S3 | Host | `make contract-check && make lint && make test && make runtime-test` | 0 | PASS | v3 dual route、bounded encrypted staging、GET/HEAD/range、ACK/TTL/restart cleanup 与四类 strict-local synthetic |
| D-FOCUSED | Desktop | v3 contract checker tests | 0 | PASS | exact source/fixture + 10 implementation file pins；adapter `implemented` |
| D-LINT | Desktop | `make lint` | 0 | PASS | generate check、ESLint/vue-tsc、fmt/clippy |
| D-TEST | Desktop | `make test` | 0 | PASS | frontend `37 files / 276 tests`; Rust `184 passed, 3 ignored` |
| D-BUILD | Desktop | `make build` | 0 | PASS | application build passes |
| D-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern + S4 architecture record builds |
| D-S5-RED | Desktop | `pnpm exec vitest run src/domain/chat-artifact.test.ts src/stores/artifact.store.test.ts src/components/chat/ChatArtifactShell.test.ts` | 1 | EXPECTED RED | 3 suites 因 S5 module/component 尚不存在而失败；随后才实现 |
| D-S5-FOCUSED | Desktop | same focused Vitest command after implementation | 0 | PASS | 3 files / 19 tests；duplicate、乱序/回退、terminal、history replay、independent failure、expired、无可信百分比与 axe |
| D-S5-LINT | Desktop | `make lint` | 0 | PASS | exact Contracts pin、ESLint/vue-tsc、Rust fmt/clippy 全部通过 |
| D-S5-TEST | Desktop | `make test` | 0 | PASS | frontend `40 files / 295 tests`; Rust `184 passed, 3 ignored` |
| D-S5-BUILD | Desktop | `make build` | 0 | PASS | Vue typecheck + production Vite build |
| D-S5-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | VitePress build；Accepted Pattern 保持可构建 |
| D-S5-DIFF | Desktop | `git diff --check` + staged `git diff --cached --check` | 0 | PASS | 工作树与实际 7-file staged S5 diff 均无 whitespace error |

一次 `pnpm lint` 曾与 `pnpm test` 并行执行，因仓库 `check-generated` 临时替换 generated 目录而产生
瞬时失败；改为仓库要求的顺序执行后通过，且 immutable commit 上再次通过。它是命令并发冲突，
不是产品或契约失败。

## 5. Downstream pin 证据

| Consumer | Pin commit | Pin 内容 | 结论 |
|---|---|---|---|
| Agent Host | pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; implementation `4017785adb08e1114781d3d844e9a10a683fa933` | Contracts `0.4.0` identities + v3 snapshots/types + implementation conformance；`EXC-128-001` | S2P/S3 PASS |
| Desktop | pin `96094419d963745529ed0fa246919089e659f20d`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45` | Contracts source/fixture identities + 10 implementation file digests + validator/exception；S5 consumes parser-approved metadata without changing the pin | S2P/S4/S5 PASS |

Desktop fixture Git tree OIDs：event v3 `21de31ceb65900bcf38bc7fe171de8238dfa30dc`、resources
`f447129c08b9b39231e33698afc3f2fd875d6b14`、Host v3
`8afbe7e88cc89401d9990e08b4b332096b53934e`、report
`3fafff6d702504f7a8a1cd44b4c717f024c88ae8`。

## 6. AC/NFR 当前覆盖

| 范围 | 当前结果 | 说明 |
|---|---|---|
| AC-001/002/006/008/009 contract portions | CONTRACT PASS | lifecycle/report/resource/ACK/version/negative fixtures 已自动验证 |
| AC-011 contract fixture portion | CONTRACT PASS | image/video/file/report 四类 synthetic canonical fixtures 已形成 |
| AC-001/002 S5 UI projection portions | S5 FOUNDATION PASS | 8-state monotonic reducer、four-kind stable identity/order、duplicate idempotency、generic state shell 与 fail-closed conflicts 已单元/组件验证 |
| AC-003/004/005/006 Desktop type renderer behavior | NOT RUN | S6-S9 未开始 |
| AC-007 persistence/history/retention | S4/S5 FOUNDATION PASS | v8 migration、SQLCipher BLOB、metadata history、168h TTL/receipt/delete/reopen + history replay/store dedupe 已验证；跨进程 UI integration 仍待 S10 |
| AC-008 runtime auth/integrity/ACK | S3/S4 FOUNDATION PASS | owner-only Host resource、MIME/size/digest/magic、commit 后 ACK 与 replay 已验证；E2E/error UI 待 S10 |
| AC-009 Host dual route + old/new matrix | PARTIAL PASS | v1/v2 equality/pins + 实际 v3 Host route 均通过；mixed-version E2E 待 S10 |
| AC-010/NFR-002 generic shell portion | S5 FOCUSED PASS | semantic tokens、Naive UI/YjIcon、aria-live/busy/progress/focus、reduced-motion CSS 与 axe component test 通过；visual matrix/performance/runtime evidence 仍待 S10 |
| AC-011 local walking skeleton | PARTIAL | 四类 strict-local Host producer 已实现；Desktop renderer/vertical smoke 未运行 |
| AC-012/real provider | BLOCKED | capability 未证、未授权付费调用 |

## 7. 专项验证状态

| 专项 | 结果 | 后续切片 |
|---|---|---|
| Contract/source/generated/breaking | PASS | 边界漂移则重开 G2/G2A |
| Consumer exact pin/conformance | PASS | S3/S4 使用相同 immutable identities |
| Host v3 auth/range/replay/staging | S3 PASS | S10 仍需跨进程/restart walking skeleton |
| Desktop SQLCipher/transfer/cleanup | S4 PASS | S10 仍需 Host+Desktop integrated lifecycle |
| UI/visual/a11y/performance | S5 generic unit/component/axe PASS；visual/runtime/performance NOT RUN | S6-S10 |
| Local synthetic E2E | NOT RUN | S10 |
| MiniMax/video/file/report real producer | BLOCKED | S12，需单独 authority/eval |
| Deployment/production rollback | N/A current local-only scope; gates NOT PASSED | G5/G6 |

## 8. Review findings closure

| Finding | 原状态 | 当前状态 | Evidence |
|---|---|---|---|
| G2-128-001 Owner/G2 closure | P1 | CLOSED AT G2 | 03 §2A/2B + Pattern Accepted |
| G2-128-002 missing source/immutable pin | P1 | CLOSED AT G2A | Contracts `ea48fe...` + source digests |
| G2-128-003 ACK/poster/retention/report ambiguity | P1 | CLOSED AT S3/S4 | 03-05 frozen semantics + Host/Desktop runtime conformance |
| BLK-128-004 generator/downstream pin | P1 | CLOSED AT G2A | locked generators + Host/Desktop pin commits |
| BASE-128-001 old Contracts lint/test failure | P2 historical | CLOSED | current lint/test and post-commit recheck PASS |
| Host docs stale `0.2.0` pin | P2 | CLOSED | Host pin commit updates README/AGENTS to actual lineage |

G2A 范围没有开放 P0/P1/P2。真实 provider、runtime security/data behavior、visual/a11y/performance 是后续
slice 的未验证范围，未被降级为已接受风险。

## 9. Owner G2/G2A decision capture

- G2：用户明确要求 Codex 分别以 Product/Design、Technical、Security/Data Owner 身份记录
  `APPROVED`，完整 capture 在 03 §2A/2B；UI Pattern 1.0.0 为 `Accepted`。
- G2A：用户明确设定条件——真实 generate、breaking、semantic review 和 immutable pin 完成后才能
  通过。第 3-5 节证据全部满足后，记录为 `APPROVED`。
- 该授权与用户后续明确的 S5 指令已用于按序完成 local-only S3/S4/S5；G3 只对这三个原子切片通过，不允许 real provider、付费调用、
  tag、push、publish、release、production 或直接宣称 G4-G6 通过。

## 10. 残余风险与停止条件

| Item | 当前边界 | 停止/重开条件 |
|---|---|---|
| Host/Desktop cross-process lifecycle | 两端 isolated conformance 已完成 | S10 integration 出现 replay、TTL、ACK 或 scope 偏差时重开对应 slice/G2 |
| Desktop native save/CSP | S4/S5 明确未实现 | 需要 plaintext、wide capability、不同 retention clock 时重开 Security/Data review |
| Synthetic video playability | S3 fixture 只有 deterministic `ftyp/free/mdat` boxes，无 `moov`，只证明 MP4 resource/integrity transport | S7/S10 必须换用可播放且可 seek 的无版权本地 fixture，并完成 WebView controls/range smoke；此前不得声称 video preview PASS |
| Unknown report section | contract 限 `required=false`、128 KiB、depth 8、opaque | renderer 遍历/执行 unknown payload 即阻断 |
| Real MiniMax image | blocked | 固定 capability/API/model、费用与 bounded eval 单独获批 |
| Real video/file/report | blocked | 每 kind 形成 producer/ownership/security contract 后单独评审 |

## 11. 制品与工作树完整性

- Contracts、Host、Desktop S3/S4/S5 feature commits 均为完整 40-character SHA；没有使用 floating branch/tag 作为 pin。
- 每个仓库在提交后重跑关键门禁；最终应保持 clean worktree。
- 生成物来自锁定 source/generator；Feature 目录不复制 canonical payload。
- 没有 `.skip`、`.only`、弱化断言、secret、真实业务数据或付费调用。

## 12. 结论

- G2：`APPROVED`。
- S1/S2：`PASS`，Contracts immutable local candidate 已形成。
- S2P：`PASS`，Host/Desktop exact pin 与 conformance 已形成，业务行为未改变。
- G2A：`APPROVED`。
- S3/S4/S5：`PASS`；G3 对这三个切片为 `PASS`。
- Code Complete：否；S6-S11 尚未开始。
- 当前状态：`G3 PASS for S3/S4/S5 foundations / S6-S11 pending / real providers closed / G4-G6 not passed`。
