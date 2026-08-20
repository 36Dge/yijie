# FEAT-128 发布、灰度与回滚 Runbook

## 1. Release Manifest

当前 G2/G2A 已获 Owner 批准；Contracts `0.4.0` local candidate 与 Host/Desktop exact pin 已形成。尚没有 tag、Host/Desktop 业务实现、签名制品或部署。

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| Governance package | uncommitted design candidate | baseline `3d6988daa7a36b24bb2e86308e4cc7213c967426` | N/A | N/A | local workspace |
| Contracts/Host/Desktop | no FEAT-128 release | N/A | N/A | N/A | not deployed |

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
| 5 | enable synthetic local profile | isolated local | 段成威 | S3-S9 + E2E | deterministic smoke/visual | disable profile, clean staging |
| 6 | decide local G4 | source candidates | 段成威 | review findings closed | 08 evidence | remain implementation pending |
| 7 | prepare real provider/release | future environment | 段成威 | separate fee/provider/production approval | fixed Eval/smoke/metrics | per-kind kill switch |

代码合并、部署、migration、synthetic activation、真实 provider activation 和 production release 是不同动作。

## 4. Feature Flag

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `YIJIE_CHAT_ARTIFACTS_V3_ENABLED` | off | Host + Desktop master | exact pins、migration、consumer/provider tests 后本地设置 | set false/restart local service | 段成威 |
| `YIJIE_ARTIFACT_SYNTHETIC_PROFILE_ENABLED` | off | exact local test profile | `YIJIE_ENV=local` + fixed manifest + no real provider | unset/false and clear staging | 段成威 |
| image real capability | off/not defined | MiniMax/Runtime image only | separate paid/provider gate | independent image off | 段成威 |
| video/file/report real capability | off/not defined | per kind | future producer-specific approval | independent kind off | 段成威 |

关闭 master flag 后继续 v1/v2 文本流；已持久化 Artifact 只读保留至过期/删除，不自动删除用户已另存的外部文件。

## 5. Migration/Backfill

| Phase | Command/job | Batch/lock controls | Validation | Pause/resume | Recovery |
|---|---|---|---|---|---|
| Expand v8 | Desktop embedded migration runner；exact command随实现形成 | single local DB transaction + checksum | populated v1-v7 fixtures、user_version、FK | app startup fail closed | restore pre-v8 encrypted backup or v8 roll-forward |
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
| SMOKE-128-002 | video announced/progress -> controls/range/save | synthetic tiny MP4/WebM | no autoplay, seek/controls/fallback | fixed local bytes |
| SMOKE-128-003 | text/JSON/CSV + unsupported Office file | synthetic files | safe preview caps + metadata/save fallback | no system app launch |
| SMOKE-128-004 | report metrics/table/chart/unknown section | synthetic report v1 | structured render, text summary, no HTML/network | closed local JSON |
| SMOKE-128-005 | duplicate/gap/restart/reopen/TTL/delete | synthetic events/temp DB | idempotent/resync/history/physical cleanup | fake clock + temp SQLCipher/Host home |
| SMOKE-128-006 | provider capability unavailable | normal local config | no real generation UI/event; text remains | real provider call disabled |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| Artifact visible/transfer success | local test log/metrics candidate | not established | all deterministic fixtures pass | any silent loss/integrity error | Runtime/Client Owner |
| Event error/latency | local typed counters | not established | p95 visible <300ms target | p95 >=1000ms or sequence corruption | Client Owner |
| Staging/storage/memory | local resource counters | not established | below approved limits | 90% capacity, >3x preview memory, crash/OOM | Runtime/Data Owner |
| Security/redaction | canary scan | 0 hits required | 0 | any path/token/body/raw error hit | Security Owner |
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
  -> 清理 Host staging/object URLs/temp files
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
| Local disable | unset or set planned Artifact flags to `false`, then restart local Host/Desktop | local owner | no v3 producer; v1/v2 text works | future 08/local smoke log |
| Local validation | commands in `06-test-plan.md` | developer | exact PASS/FAIL exits | `08-verification-report.md` |
| Deploy | N/A；当前没有部署平台 | release owner | not executed | NOT RUN |
| Production rollback | N/A；当前没有 production artifact/environment | release owner | not executed | NOT RUN |

不编造生产命令、secret、tag 或 release controls。

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| 2026-08-20 | design stage | no code/data migration | design walkthrough only | NOT RUN | 需要 v8 candidate、signed/local bundle 与完整加密备份后执行 |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Product/Design/Technical/Security/Data/Release | 段成威 | current Codex task and repository review | 所有阶段最终决策；角色动作分别记录 |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| G2 design | 段成威 | APPROVED for Contracts S1/S2 only | 2026-08-20 | 03 §2B + 00-07 + Pattern 1.0.0 Accepted |
| G2A local candidate | 段成威 | APPROVED | 2026-08-20 | Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b` + Host/Desktop exact pins；generate/lint/test/build、双 breaking 与 consumer conformance PASS |
| G4 local candidate | 段成威 | NOT REQUESTED | N/A | no Host/Desktop implementation |
| Go/No-Go production | 段成威 | N/A current scope / not approved | N/A | no production plan |
