# FEAT-128 发布、灰度与回滚 Runbook

## 1. Release Manifest

当前 G2/G2A 已获 Owner 批准；Contracts `0.4.0` local candidate、Host S3 与 Desktop S4/S5 已形成不可变本地
commits，并通过 G3 slice gate；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B 已作为独立本地切片 PASS。S8-READINESS
与 S7-SPEC-RECONCILIATION 已形成 Pattern 1.3.0 docs evidence，但尚没有 S8 command/schema/renderer、production
vertical、tag、E2E、签名制品或部署。

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| Governance package | G3 S3/S4/S5 + S6/S7 separate PASS + S8 readiness docs | 本次 `yijie` 文档提交 | N/A | N/A | local workspace |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | source digests in feature.yaml | locked generators | not deployed |
| Agent Host S3 | local source candidate; flags off | `4017785adb08e1114781d3d844e9a10a683fa933` | N/A source commit | Contracts `ea48fe...` | not deployed |
| Desktop S4 | local source candidate; flag off | `09220dd8319cfb8ec0c4d1531514bb5169107983` | 10 implementation file pins in Desktop lock | Contracts `ea48fe...` | not deployed |
| Desktop S5 | local UI foundation; no renderer | `7548ea8aeacfd7274f1107786ce48ddc6789cd45` | N/A source commit | same immutable pin | not deployed |
| Desktop S6 readiness Pattern 1.1.0 | docs-only Accepted boundary | `2b854b40379a207c19bf37fc5bc64266553c5df1` | N/A | same immutable pin | not implemented/deployed |
| Desktop S6A/S6B | local independent source slices；not in G3 | S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S6B `4a8dce6a6526e37052941f6dbb921ba2486e109f` | source commits | same immutable pin | not deployed |
| Desktop S7 readiness Pattern 1.2.0 (historical) | docs-only Accepted boundary；READY FOR S7F ONLY at capture | `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` | N/A | same Contracts pin/tree；S7 later separate PASS | not deployed |
| Agent Host S7F | local strict-local fixture conformance；not in G3 | `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | source commit | same Contracts pin/tree | not deployed |
| Desktop S7A/S7A-REPAIR/S7B | local independent source slices；not in G3 | S7A `22b91c5a258458c87f1ac96c06bf39d1af97358f`; repair `34991d8967de9aa2197ab2e8b9b49347774df7a5`; S7B `366186b601144bdc2bc87a2cef3075b74f1e8f19` | source commits + default-off smoke harness | same immutable pin | not deployed |
| Desktop S8 readiness Pattern 1.3.0 | docs-only Accepted boundary；READY FOR S8A ONLY | `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` | N/A | same Contracts/Host/Desktop implementation pins | not implemented/deployed |

## 2. 发布前提

- [ ] G4 Code Complete 通过并有段成威批准
- [ ] Contracts `0.4.0` source/generated commit、双基线 breaking、semantic review 和下游 exact pin 完整
- [ ] Release artifact 来自干净不可变 source，签名/公证方案存在
- [ ] Config、secret、CSP、native save 权限、容量与磁盘准备完成
- [ ] v8 migration/备份/roll-forward 在类生产签名 Desktop 演练
- [ ] Dashboard、告警、Runbook、费用预算和 provider capability 证据存在
- [ ] Feature flags 默认关闭且每个 kind 有独立 kill switch
- [ ] 真实 Go/No-Go 批准形成

当前本地-only范围不要求完成生产前提，但也不能将其标记为通过或据此进入 G5/G6。

## 3. 合并、部署、迁移与启用顺序

| Order | Action | Component/Environment | Operator | Preconditions | Verification | Rollback point |
|---:|---|---|---|---|---|---|
| 1 | approve design/G2 | feature package + Pattern | 段成威 | 00-07 review | G2 APPROVED + Pattern Accepted | reopen G2；no implementation |
| 2 | merge immutable contract candidate | yijie-contracts | Contracts Owner | G2 approved, full checks/review | tag/ref/digests/generators | do not pin downstream |
| 3 | merge Host provider with flags off | Agent Host | Runtime Owner | exact contract pin | producer/resource conformance | v1/v2 only |
| 4 | merge Desktop native consumer with flags off | Desktop | Client/Data Owner | Host conformance, migration review | Rust/TS/build/history/security | old UI, v8 data read-only |
| 5 | S6A native image boundary | Desktop local source | Client/Security/Data Owner | S5 + S6 readiness | PASS at `8b99849d...` | remove exact commands/scheme/CSP delta；SQLCipher unchanged |
| 6 | S6B image renderer | Desktop local source | Product/Client Owner | S6A immutable PASS | PASS at `4a8dce6a...`；runtime visual later | disable renderer；S5 metadata shell remains |
| 7 | S7F canonical video fixture conformance | Host local source | Runtime/Technical/Security Owner | Pattern 1.2.0 + current immutable Contracts resource | exact raw digest/boxes/manifest + Host full gates | revert S7F；keep video renderer off |
| 8 | S7A native video Range/save boundary | Desktop local source | Client/Security/Data Owner | S7F immutable PASS + separate authorization | Rust/TS RED/GREEN + full Desktop gates | remove isolated commands/schema/scheme/media-src |
| 9 | S7A-REPAIR lifecycle | Desktop local source | Technical/Security/Data Owner | real runtime root cause + separate repair authorization | >=128 Range unit + 76 Range WebView metadata/playback/seek, 404=0 | disable S7B/video capability or roll back the complete video chain；64-request failure may only be reproduced in isolated historical tests, never restored as operative runtime behavior |
| 10 | S7B video renderer | Desktop local source | Product/Client Owner | repaired S7A immutable PASS + separate authorization | component/axe/runtime seek/visual + full gates | disable renderer；metadata shell remains |
| 11 | S8A bounded file preview/save boundary | Desktop local source | Product/Technical/Security/Data Owner | Pattern 1.3.0 + separate coding authorization | Rust/TS RED/GREEN + full Desktop gates | remove exact file commands/schema/client；S5 shell remains |
| 12 | S8B file renderer/search/save UX | Desktop local source | Product/Client Owner | S8A immutable PASS + separate authorization | component/axe/security/visual + full gates | disable file renderer；S8A may remain closed |
| 13 | S9 report renderer | Desktop local source | Product/Client/Security Owner | S8B + report readiness | schema/component/axe/visual | metadata shell remains |
| 14 | enable synthetic local profile | isolated local | 段成威 | S3-S9 + E2E | deterministic smoke/visual | disable profile, clean staging |
| 15 | decide local G4 | source candidates | 段成威 | review findings closed | 08 evidence | remain implementation pending |
| 16 | prepare real provider/release | future environment | 段成威 | separate fee/provider/production approval | fixed Eval/smoke/metrics | per-kind kill switch |

代码合并、部署、migration、synthetic activation、真实 provider activation 和 production release 是不同动作。

## 4. Feature Flag

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `YIJIE_AGENT_HOST_V3_ARTIFACTS_ENABLED` | off | Host v3 route/resources | exact pin + S3 tests 后本地设 exact true | false/restart Host | 段成威 |
| `YIJIE_CHAT_ARTIFACTS_V3_ENABLED` | off | Desktop native transfer | exact pin + S4 migration/consumer tests 后本地设 exact true | false/restart Desktop；已存 metadata 只读 | 段成威 |
| `YIJIE_FEAT128_SYNTHETIC_ENABLED` + `YIJIE_FEAT128_SYNTHETIC_MANIFEST=feat128-artifact-v1` | off | exact local Host producer profile | `YIJIE_ENV=local` + fixed manifest + no real provider | unset/false and clear staging | 段成威 |
| image real capability | off/not defined | MiniMax/Runtime image only | separate paid/provider gate | independent image off | 段成威 |
| video/file/report real capability | off/not defined | per kind | future producer-specific approval | independent kind off | 段成威 |

关闭 master flag 后继续 v1/v2 文本流；已持久化 Artifact 只读保留至过期/删除，不自动删除用户已另存的外部文件。

## 5. Migration/Backfill

| Phase | Command/job | Batch/lock controls | Validation | Pause/resume | Recovery |
|---|---|---|---|---|---|
| Expand v8 | Desktop embedded migration runner at `09220dd8319cfb8ec0c4d1531514bb5169107983` | single local DB transaction + checksum | populated v1-v7 fixtures、user_version、FK PASS | app startup fail closed | restore pre-v8 encrypted backup or v8 roll-forward |
| Backfill | N/A；旧消息无 Artifact | N/A | reader returns empty list | N/A | N/A |
| TTL cleanup | Desktop maintenance + Host staging TTL | bounded items/bytes per pass | content/cache/WAL/staging inaccessible | resumable typed receipt | retry/repair; do not claim delete complete |

不得对 v8 数据库手写 down migration。旧 Desktop 需要完整迁移前加密备份。

## 6. 灰度计划

| Stage | Scope/tenant/% | Observation window | Success criteria | Stop threshold | Decision owner |
|---|---|---|---|---|---|
| Synthetic internal | one synthetic tenant/local machine | one complete test run + reopen | all AC automated, no canary leak, resource counters return zero | any integrity/path/token/body leak, duplicate terminal, crash/OOM | 段成威 |
| Local manual candidate | one authorized local user, synthetic data only | manual matrix session | image/video/file/report UI, save, history, a11y recorded | P1/P2 UX/security issue or ambiguous capability | 段成威 |
| Real provider local | image only if separately approved | fixed small-call window | fixed capability/Eval/cost thresholds | unbounded cost、provider drift、wrong media/integrity | 段成威 |
| Production canary/expand | N/A current scope | not designed | not defined | not defined | 段成威 |

## 7. Smoke

| Smoke ID | 用户路径 | 输入/租户 | 预期 | 避免真实副作用方式 |
|---|---|---|---|---|
| SMOKE-128-001 | text streams while image started -> progress -> completed -> local ready -> lightbox/save | synthetic tenant/1x1 PNG | stable announced placeholder, verified transfer, preview, atomic save | local fixture + temp destination |
| SMOKE-128-002 | video announced/progress -> controls/range/save | frozen 1,642-byte canonical MP4；WebM unsupported | no autoplay, single-range seek/controls/fallback | fixed local bytes；no external footage |
| SMOKE-128-003 | plain/JSON/CSV + PDF/XLSX unsupported-inline | Desktop-private synthetic files | exact bounded projection/search + metadata/native-save fallback；Markdown deferred | no system app launch；no public fixture drift |
| SMOKE-128-004 | report metrics/table/chart/unknown section | synthetic report v1 | structured render, text summary, no HTML/network | closed local JSON |
| SMOKE-128-005 | duplicate/gap/restart/reopen/TTL/delete | synthetic events/temp DB | idempotent/resync/history/physical cleanup | fake clock + temp SQLCipher/Host home |
| SMOKE-128-006 | provider capability unavailable | normal local config | no real generation UI/event; text remains | real provider call disabled |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| Artifact visible/transfer success | local test log/metrics candidate | not established | all deterministic fixtures pass | any silent loss/integrity error | Runtime/Client Owner |
| Event error/latency | local typed counters | not established | p95 visible <300ms target | p95 >=1000ms or sequence corruption | Client Owner |
| Staging/storage/memory | local resource counters | not established | below approved limits | 90% capacity, >3x preview memory, crash/OOM | Runtime/Data Owner |
| Security/redaction | canary scan | unauthorized/path/token/raw-error 0 hits；authorized bounded marker open-only | exact lifecycle | any unauthorized hit or authorized marker after close | Security Owner |
| AI quality/cost | N/A synthetic | cost 0 | N/A | any unapproved real call | Product/Release Owner |

当前没有生产 dashboard、告警或 SRE 值班，这些项目不构成 G5 证据。

## 9. 回滚决策

```text
触发停止阈值
  -> 关闭受影响 kind 或 master flag
  -> 停止新的 producer/transfer，不删除证据
  -> 判断 Desktop DB 是否已升级到 v8
  -> 未升级：回退应用/Host candidate
  -> 已升级：保持 v8 reader roll-forward；需要旧应用时恢复迁移前加密备份
  -> 清理 Host staging/opaque preview handles/temp files
  -> 复验 v1/v2 text、history、TTL、integrity 与 redaction
```

| Trigger | Immediate action | Code rollback | Data action | Verification | Escalation |
|---|---|---|---|---|---|
| v1/v2 regression | master flag off，停止 v3 | revert Host/Desktop candidate | keep v8 data read-only | v1/v2 equality/full suites | Contracts Owner |
| integrity/path/token/body leak | all Artifact flags off | isolate offending slice | delete staging/cache after evidence；rotate bearer if exposed | canary/log/DB/DOM scan | Security Owner |
| crash/OOM/media decode issue | affected kind off | renderer/native roll-forward fix | retain authority bytes but disable preview | boundary/performance tests | Client Owner |
| migration/cleanup failure | block app/close decision | v8 roll-forward fix | restore backup only if approved | reopen/WAL/forensic cleanup | Data Owner |
| provider cost/capability drift | real kind off immediately | revert provider config/adapter | no cloud data assumed | zero new calls + fixed capability test | Product/Release Owner |

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Local disable | unset or set the three exact Host/Desktop Artifact flags above to `false`, then restart local Host/Desktop | local owner | no new v3 producer/transfer; v1/v2 text and persisted metadata reader remain | future 08/local smoke log |
| Local validation | commands in `06-test-plan.md` | developer | exact PASS/FAIL exits | `08-verification-report.md` |
| Deploy | N/A；当前没有部署平台 | release owner | not executed | NOT RUN |
| Production rollback | N/A；当前没有 production artifact/environment | release owner | not executed | NOT RUN |

不编造生产命令、secret、tag 或 release controls。

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| 2026-08-20 | S6 readiness stage | S4 v8 + S5 shell；no S6 code/config at that time | preview/save threat-model and rollback walkthrough only | DESIGN PASS；runtime drill NOT RUN | S6A/S6B later implemented；signed/local bundle drill remains |
| 2026-08-20 | S7 readiness stage | S6B `4a8dce6a...` + Pattern 1.2.0；no S7 code/config | fixture/Range/save/CSP/resource-release threat model and rollback walkthrough | DESIGN PASS；runtime drill NOT RUN | first run S7F；S7A/S7B and Tauri playback/seek drill wait |
| 2026-08-21 | S7 implemented chain | S7F `1045dd...` + S7A `22b91c...` + repair `34991d...` + S7B `366186...` | real default-off WebView metadata/playback/seek + request-lifetime repair drill | 76 Range/76 partial、404=0、metadata/playback/seek PASS | production Chat vertical/manual visual/performance still S10 |
| 2026-08-21 | S8 readiness stage | Pattern 1.3.0 `4929a73a...`；no S8 code/config | bounded projection/native save/data-lifecycle/rollback walkthrough | DESIGN PASS；runtime drill NOT RUN | first run S8A；S8B waits；Markdown/G4 blocked |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Product/Design/Technical/Security/Data/Release | 段成威 | current Codex task and repository review | 所有阶段最终决策；角色动作分别记录 |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G2 design | 段成威 | APPROVED for Contracts S1/S2 only | 2026-08-20 | 03 §2B + 00-07 + Pattern 1.0.0 Accepted |
| G2A local candidate | 段成威 | APPROVED | 2026-08-20 | Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b` + Host/Desktop exact pins；generate/lint/test/build、双 breaking 与 consumer conformance PASS |
| S6 readiness | 段成威（Product/Technical/Security/Data） | APPROVED FOR S6A CODING ONLY；S6B WAITS FOR S6A PASS | 2026-08-20 | 03 §2C + 05/06/07 + Desktop Pattern 1.1.0 `2b854b40379a207c19bf37fc5bc64266553c5df1` |
| S7 readiness (historical) | 段成威（Product/Technical/Security/Data） | READY FOR S7F ONLY；S7A/S7B WAIT at capture | 2026-08-20 | 03 §2D + Pattern 1.2.0；S7F/S7A/repair/S7B later separate PASS |
| S8 readiness | 段成威（Product/Technical/Security/Data） | READY FOR S8A ONLY；Markdown deferred/AC-005 PARTIAL；S8B WAIT | 2026-08-21 | 03 §2E + 05/06/07 + Desktop Pattern 1.3.0 `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` |
| G4 local candidate | 段成威 | NOT REQUESTED | N/A | S8A/S8B/S9-S11 and full AC/E2E/review incomplete；Markdown unresolved for full AC-005 |
| Go/No-Go production | 段成威 | N/A current scope / not approved | N/A | no production plan |
