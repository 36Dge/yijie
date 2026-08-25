# FEAT-128 发布、灰度与回滚 Runbook

## 1. Release Manifest

当前 G2/G2A 已获 Owner 批准；Contracts `0.4.0` local candidate、Host S3 与 Desktop S4/S5 已形成不可变本地
commits，并通过 G3 slice gate；S6-S9B-R 已作为独立本地切片 PASS。S10-READINESS/Pattern 1.6.0 当时只批准
S10A；S10A/S10B/S10C 后续已分别形成 G3 外独立 PASS。
Pattern 1.7.0 历史上仅给出 `READY FOR S10D-H ONLY`。
S10D-H 后续已有 Host/Desktop 实现提交，但 runtime smoke 未通过并已按用户指令暂停；S10D-V/S10E 未运行。
2026-08-23 新增真实图片 S12 范围与最多 5 次付费验证授权；S12A schema v2 governance/G2 已完成，S12B-F 未实现，
S12 campaign 账本 used `0/5`、reserved `0`。此前 standalone `image-01` 成功 probe 只是一条未限定历史观察，
不经过 yijie 链路且不进入该 campaign。
production vertical、合格真实图片证据、tag、E2E、签名制品与部署均不存在。

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| Governance package | active schema v2；S12A governance/G2 PASS；historical G3 S3/S4/S5 + separate PASS records | WORKTREE；本次 commit pending | N/A | 04A/S12 graph/H fuse machine-bound；G2A pending，G2V blocked | local workspace |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | source digests in feature.yaml | locked generators | not deployed |
| Agent Host S3 | local source candidate; flags off | `4017785adb08e1114781d3d844e9a10a683fa933` | N/A source commit | Contracts `ea48fe...` | not deployed |
| Desktop S4 | local source candidate; flag off | `09220dd8319cfb8ec0c4d1531514bb5169107983` | 10 implementation file pins in Desktop lock | Contracts `ea48fe...` | not deployed |
| Desktop S5 | local UI foundation; no renderer | `7548ea8aeacfd7274f1107786ce48ddc6789cd45` | N/A source commit | same immutable pin | not deployed |
| Desktop S6 readiness Pattern 1.1.0 | docs-only Accepted boundary | `2b854b40379a207c19bf37fc5bc64266553c5df1` | N/A | same immutable pin | not implemented/deployed |
| Desktop S6A/S6B | local independent source slices；not in G3 | S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S6B `4a8dce6a6526e37052941f6dbb921ba2486e109f` | source commits | same immutable pin | not deployed |
| Desktop S7 readiness Pattern 1.2.0 (historical) | docs-only Accepted boundary；READY FOR S7F ONLY at capture | `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` | N/A | same Contracts pin/tree；S7 later separate PASS | not deployed |
| Agent Host S7F | local strict-local fixture conformance；not in G3 | `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | source commit | same Contracts pin/tree | not deployed |
| Desktop S7A/S7A-REPAIR/S7B | local independent source slices；not in G3 | S7A `22b91c5a258458c87f1ac96c06bf39d1af97358f`; repair `34991d8967de9aa2197ab2e8b9b49347774df7a5`; S7B `366186b601144bdc2bc87a2cef3075b74f1e8f19` | source commits + default-off smoke harness | same immutable pin | not deployed |
| Desktop S8 readiness Pattern 1.3.0 | historical docs-only Accepted boundary；READY FOR S8A ONLY at capture | `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` | N/A | same Contracts/Host/Desktop implementation pins | no implementation at readiness；later S8A/S8B not deployed |
| Desktop S8A/S8B | local independent source slices；not in G3 | S8A `bf5452f7fde24d1391845deaba17ec1135716c62`; S8B `4d0238b1906f02d319f47f5e55cdc023485ef07a` | source commits | same immutable pin | not deployed |
| Desktop S9 readiness Pattern 1.4.0 | historical docs-only Accepted boundary；READY FOR S9A ONLY at capture | `b6f7401c79d5b2356bc45468f14d7fdbb17a855c` | N/A | same Contracts/Host/Desktop implementation pins | S9A later implemented；not deployed |
| Desktop S9A | local independent native report boundary；not in G3 | `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` | source commit | same public Contracts/Host pin；Desktop SHA-only checker refresh | not deployed |
| Desktop S9B readiness Pattern 1.5.0 | historical docs-only Accepted boundary；READY FOR S9B-D ONLY at capture | `630c3c8d55a2617499f51bd5bed263b819aaf084` | N/A | same Contracts/Host/Desktop implementation pins | D/R later implemented；not deployed |
| Desktop S9B-D/checker repair/S9B-R | local independent slices；not in G3 | `0a36ca7c54460d22ea6b3228832a57f05f0bde68`; `aec0f8a05ba7534132cbb4f46be64e333d7e9024`; `6bcc2a6bfb4db76398ecf5483c688475477f08ed` | source commits/test-only harness | same public pins | not deployed；production vertical NOT RUN |
| Desktop S10 readiness Pattern 1.6.0 (historical) | docs-only Accepted boundary；READY FOR S10A-LOCAL-PROFILE ONLY at capture | `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` | N/A | same Contracts/Host/Desktop pins | S10A-E not implemented at capture；A-C later separate PASS；not deployed |
| Host/Desktop S10A + Desktop S10B/S10C | local independent slices；not in G3 | Host `0debd877a4afe1bf2da8c988caeb1124d0fa7272`; Desktop `f4a3d42ad837ecdc8a8ba4198b269d4717285791`/`f787d70b4cfb51cde76bdce047ba630f4b7b1250`/`86f02b4def4d07f76d66ebdafafda5a9bb75035c` | source commits | same public Contracts/Host pins | not deployed；production vertical NOT RUN |
| Desktop S10D readiness Pattern 1.7.0 | historical docs-only boundary；READY FOR S10D-H ONLY at capture | `8afdc996c11bbad2d275eb8b86a0f6b82ca5da52` | N/A | same Contracts/Host/Desktop pins | H later failed/paused；V/E not implemented/deployed |
| Host/Desktop S10D-H failed candidate | local implementation；smoke FAIL/PAUSED；not a release candidate | Host `09d83cce5f2937db1cbe3afa36cc5461ea671574`; Desktop `997345d87a5daa073c480769d57b4e59c3dfefcb` | no qualified PASS digest | historical Pattern 1.7.0 only | not deployed；do not resume from this Runbook |
| S12 real-image governance | S12A schema v2/G2 PASS；S12B-F implementation NOT RUN | 本次 `yijie` 文档工作树；提交未形成 | S12 campaign ledger used `0/5`、reserved `0`；standalone probe unqualified | Runtime compatibility candidate not formed；G2A pending | not deployed；real image flag undefined/off |

## 2. 发布前提

- [ ] G4 Code Complete 通过并有段成威批准
- [ ] Contracts `0.4.0` source/generated commit、双基线 breaking、semantic review 和下游 exact pin 完整
- [ ] Release artifact 来自干净不可变 source，签名/公证方案存在
- [ ] Config、secret、CSP、native save 权限、容量与磁盘准备完成
- [ ] v8 migration/备份/roll-forward 在类生产签名 Desktop 演练
- [ ] Dashboard、告警、Runbook、费用预算和 provider capability 证据存在
- [ ] Feature flags 默认关闭且每个 kind 有独立 kill switch
- [ ] Runtime dynamic-tool/reverse-call compatibility contract、Host fake-provider 与 packaged secret handoff 全部通过
- [ ] 付费验证账本逐次记录且累计不超过 5 次 HTTP send attempts；`n=1`，成功最多 5 张；失败/timeout/outcome-unknown 仍占 attempt 且不自动重试
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
| 13 | S9A bounded report projection/canonical JSON save | Desktop local source | Product/Technical/Security/Data Owner | Pattern 1.4.0 + separate coding authorization | consumer differential + Rust/TS RED/GREEN + full Desktop gates | remove report commands/schema/client；metadata shell remains；不得恢复错误 contract interpretation |
| 14 | S9B-D dependency/theme/closed adapter/card | Desktop local source | Product/Technical/Security/Data Owner | Pattern 1.5.0 + separate S9B-D authorization | exact dependency/integrity/license/import/bundle + theme/adapter/card/axe/visual/full gates | remove dep/3 lock nodes/notice/theme/tokens/adapter/card/checker；S9A unchanged |
| 15 | S9B-R report renderer/canonical-save UX | Desktop local source | Product/Client/Security Owner | S9B-D immutable PASS + separate S9B-R authorization | component/axe/security/visual + final bundle/full gates | remove renderer/Shell/List wiring；S5 metadata + S9A save remain |
| 16 | S10A exact keyless local profile | Host/Desktop test/config | Technical/Security Owner | Pattern 1.6 + separate auth | real Host session/turn/v3 GET/ACK；zero provider/non-loopback；cleanup | delete profile/mapping/runner；restore mutex |
| 17 | S10B single-v3 native live | Desktop native/private | Runtime/Client/Data Owner | S10A immutable PASS | atomic cursor/replay/private invalidation | flag off→single v2；rows read-only |
| 18 | S10C production page | Desktop TS/Vue | Product/Client/Security Owner | S10B immutable PASS | v3 history/store/page/four clients/axe | unmount list/clear store；v2 UI remains |
| 19 | record S10D-H failed candidate and keep paused | governance only | 段成威 | Host/Desktop current heads + available failed smoke facts | no false PASS；no new execution | preserve failed heads/evidence；do not close H |
| 20 | S12A migrate legacy v1 governance to schema v2 | yijie docs only | 段成威 | recover exact H attempt/RCA ledger from evidence | v2/default/G2 checks；04A + breaker + slice graph | revert docs migration if facts cannot be recovered |
| 21 | S12B Runtime tool compatibility candidate | yijie-contracts + Host conformance | Contracts/Runtime Owner | S12A G2 | reverse `item/tool/call` fixtures、generate/breaking/review/exact pin | do not repin consumers |
| 22 | S12C Host fake-provider implementation | Agent Host | Runtime/Security/Data Owner | S12B G2A + frozen fake-harness design/EXPECTED RED | T2I/I2I/no-call、failures、idempotency、cleanup；zero external call；形成 qualified fake harness/G2V | real-image flag off；remove adapter/router |
| 23 | S12D consumer repin + packaged secret handoff | Host/Desktop | Runtime/Client/Security Owner | S12C immutable PASS | full gates、owner-only secret canary、unchanged image consumer | rollback handoff/pin；persisted Artifact read-only |
| 24 | S12E bounded paid probe | isolated Host/Runtime | 段成威 | S12D PASS + explicit start | planned slots P1-P2 T2I/I2I；planned total 4、hard max 5；reserved/used content-free ledger | image kill switch；no retry on unknown outcome |
| 25 | resolve real-Tauri overlap with paused S10D-H | governance + isolated local only if authorized | 段成威 | exact failure ledger migrated + RCA/authorization | H immutable PASS，或 v2 Owner-approved non-borrowing H-IMG-VERTICAL exception | keep H paused on any unclassified/repeated failure；never delete ledger |
| 26 | S12F real Tauri T2I/I2I vertical | isolated local | 段成威 | S12E PASS + order 25 resolved + qualified image harness | planned slots P3-P4 分别覆盖 T2I/I2I；M3→tool→provider→Artifact→Desktop、history/preview/save/teardown | image kill switch；clear input/intermediate；ready staging仅按 ACK/TTL/session delete/restart authority |
| 27 | S10D-V/S10E | isolated local | 段成威 | H immutable PASS + separate authorization；image-harness exception 不满足该前提 | full four-kind/security/performance matrix | retain prior immutable layers only |
| 28 | decide local G4 | source candidates | 段成威 | all required slices + independent review + Markdown decision | 08 evidence | remain pending |

代码合并、部署、migration、synthetic activation、真实 provider activation 和 production release 是不同动作。

## 4. Feature Flag

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| `YIJIE_AGENT_HOST_V3_ARTIFACTS_ENABLED` | off | Host v3 route/resources | exact pin + S3 tests 后本地设 exact true | false/restart Host | 段成威 |
| `YIJIE_CHAT_ARTIFACTS_V3_ENABLED` | off | Desktop native transfer | exact pin + S4 migration/consumer tests 后本地设 exact true | false/restart Desktop；已存 metadata 只读 | 段成威 |
| `YIJIE_FEAT128_SYNTHETIC_ENABLED` + `YIJIE_FEAT128_SYNTHETIC_MANIFEST=feat128-artifact-v1` | off | exact local Host producer profile | `YIJIE_ENV=local` + fixed manifest + no real provider | unset/false and clear staging | 段成威 |
| `YIJIE_FEAT128_S10_TEST_PROFILE_ENABLED` | off | exact S10 test-only combination | compile-time harness + FEAT126 fake profile + all exact local/owner/parent/zero-key conditions | unset/false；stop children；delete run root | 段成威 |
| planned `YIJIE_AGENT_HOST_REAL_IMAGE_ENABLED` | off；名称在新 G2 冻结后方可落代码 | MiniMax/Runtime image tool registration and calls only | S12B-D PASS + Host-only Key + bounded ledger；S12E/F 才可 exact true | false/restart Host；停止新注册/调用，取消 pending local context | 段成威 |
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
| Real provider local | image only；bounded authorization exists | one-call-at-a-time window；planned 4、hard max 5 | S12E + S12F 各一次 T2I/I2I、no-call、Artifact/history/cleanup；reserved/used ledger exact | used+reserved >5、unknown outcome retry、provider drift、wrong media/integrity、secret/content leak | 段成威 |
| Production canary/expand | N/A current scope | not designed | not defined | not defined | 段成威 |

## 7. Smoke

| Smoke ID | 用户路径 | 输入/租户 | 预期 | 避免真实副作用方式 |
|---|---|---|---|---|
| SMOKE-128-001 | text streams while image started -> progress -> completed -> local ready -> lightbox/save | synthetic tenant/1x1 PNG | stable announced placeholder, verified transfer, preview, atomic save | local fixture + temp destination |
| SMOKE-128-002 | video announced/progress -> controls/range/save | frozen 1,642-byte canonical MP4；WebM unsupported | no autoplay, single-range seek/controls/fallback | fixed local bytes；no external footage |
| SMOKE-128-003 | plain/JSON/CSV + PDF/XLSX unsupported-inline | Desktop-private synthetic files | exact bounded projection/search + metadata/native-save fallback；Markdown deferred | no system app launch；no public fixture drift |
| SMOKE-128-004 | report metrics/table/chart/unknown section | synthetic report v1 | S9A bounded projection/canonical save；S9B fixed chart + accessible table、no HTML/network | closed local JSON；reusable S9 PASS；production vertical NOT RUN |
| SMOKE-128-005 | duplicate/gap/restart/reopen/TTL/delete | synthetic events/temp DB | idempotent/resync/history/physical cleanup | fake clock + temp SQLCipher/Host home |
| SMOKE-128-006 | provider capability unavailable | normal local config | no real generation UI/event; text remains | real provider call disabled |
| SMOKE-128-007 | MiniMax-M3 对明确海报请求选择 image tool | approved synthetic prompt；no reference | exactly one `image-01` call and one ready provider-provenance image Artifact | S12C 使用 loopback fake；S12E/F 才消费 1 次额度 |
| SMOKE-128-008 | 当前轮单张人物参考图 + 保持人物一致性请求 | approved local PNG/JPEG `<10,000,000` bytes | exactly one `subject_reference` Data URL call and ready image Artifact | 禁止 URL；Host provider 副本仅短期内存；S12E/F 才消费 1 次额度 |
| SMOKE-128-009 | 普通问答、零图/多图 I2I、取消与 provider error | local deterministic cases | zero unintended call；stable content-free failure；no partial ready Artifact | fake counter + canary；不消费付费额度 |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| Artifact visible/transfer success | local test log/metrics candidate | not established | all deterministic fixtures pass | any silent loss/integrity error | Runtime/Client Owner |
| Event error/latency | local typed counters | not established | p95 visible <300ms target | p95 >=1000ms or sequence corruption | Client Owner |
| Staging/storage/memory | local resource counters | not established | below approved limits | 90% capacity, >3x preview memory, crash/OOM | Runtime/Data Owner |
| Security/redaction | canary scan | unauthorized/path/token/raw-error 0 hits；authorized bounded marker open-only | exact lifecycle | any unauthorized hit or authorized marker after close | Security Owner |
| AI routing quality | fake-provider call counter + eval set | not established | explicit T2I/I2I exactly once；ordinary chat zero | any unintended call or wrong mode/reference | Product/Runtime Owner |
| Image provider cost | Host content-free durable campaign ledger | S12 campaign used `0/5`、reserved `0`；standalone probe另列 | campaign ID fixed；P1-P4 固定 stage/mode；S12E/F 对同一 authority 做 slot CAS；repair R1绑定原失败+one-shot Owner authorization/RCA；`n=1` | 第二/重置账本、wrong stage/mode、duplicate slot、repair 挪作新场景、任一分类超额、total sixth attempt、auto retry、unattributed/unknown-outcome repeat | Product/Release Owner |
| Image provider integrity | Host typed counters/canary | not established | HTTP + `base_resp.status_code=0` + exactly one validated PNG/JPEG result | malformed/oversize/non-image/base64/raw-response leak | Runtime/Security Owner |

当前没有生产 dashboard、告警或 SRE 值班，这些项目不构成 G5 证据。

## 9. 回滚决策

```text
触发停止阈值
  -> 关闭受影响 kind 或 master flag
  -> 停止新的 producer/transfer，不删除证据
  -> 判断 Desktop DB 是否已升级到 v8
  -> 未升级：回退应用/Host candidate
  -> 已升级：保持 v8 reader roll-forward；需要旧应用时恢复迁移前加密备份
  -> 清 input/intermediate/opaque preview handles/temp files；ready Host staging 仅按 ACK/24h TTL/session delete/restart authority 清理
  -> 复验 v1/v2 text、history、TTL、integrity 与 redaction
```

| Trigger | Immediate action | Code rollback | Data action | Verification | Escalation |
|---|---|---|---|---|---|
| v1/v2 regression | master flag off，停止 v3 | revert Host/Desktop candidate | keep v8 data read-only | v1/v2 equality/full suites | Contracts Owner |
| integrity/path/token/body leak | all Artifact flags off | isolate offending slice | delete staging/cache after evidence；rotate bearer if exposed | canary/log/DB/DOM scan | Security Owner |
| crash/OOM/media decode issue | affected kind off | renderer/native roll-forward fix | retain authority bytes but disable preview | boundary/performance tests | Client Owner |
| migration/cleanup failure | block app/close decision | v8 roll-forward fix | restore backup only if approved | reopen/WAL/forensic cleanup | Data Owner |
| provider cost/capability drift | real kind off immediately；停止后续外发 | revert provider config/adapter | 清本地 input/intermediate；已发送 prompt/参考图的 provider retention/deletion 为 UNKNOWN，按执行前复核的官方政策与 incident 流程处置 | zero new calls + fixed capability test；不声称本地回滚删除 provider 数据 | Product/Release Owner |
| MiniMax timeout/unknown outcome | stop this scenario；do not retry automatically | keep adapter off pending review | discard uncommitted buffer/current-turn reference；retain content-free ledger state | ledger shows `outcome_unknown` and call count unchanged thereafter | Product/Release Owner |
| image Key/provider raw leak or input content outside allowlist | image flag off；stop Host/Runtime/Desktop harness；rotate Key if exposure possible | remove secret handoff/router/adapter | clear ephemeral reference/provider intermediate after evidence；ready staging 仅按 incident evidence/deletion authority 处理 | Key/header/provider raw boundary scan；prompt/reference only in authorized user-turn/Runtime input/Host request，not result/event/log/evidence | Security/Data Owner |
| S9B dependency/integrity/license/bundle drift | stop S9B-D，keep report UI unconnected | remove exact dependency/three lock nodes/notice/theme/adapter/card | no report data change；S9A SQLCipher/canonical save retained | lock/integrity/license/import scan + raw/gzip budget + full Desktop gates | Technical/Security/Data Owner |
| chart init/instance leak or a11y failure | table-only fallback，disable chart enhancement | remove/disable YjChartCard and later renderer integration | projection remains component-local only；clear/dispose/disconnect | lifecycle/axe/visual/memory + close zero-hit | Product/Client/Security Owner |
| S10 test profile escape/key/network | stop all children；close ports | remove S10A profile/mapping/runner | preserve content-free evidence then delete owner-only run root | zero key/provider/non-loopback + no child/listener/WAL/spool/temp | Technical/Security Owner |
| v3 cursor/Artifact divergence | Artifact flag off；single v2 active stream | revert S10B private channel/coordinator | retain SQLCipher rows read-only；do not delete or weaken state | crash/replay/gap/stream-change/history differential | Runtime/Client/Data Owner |
| page authority/stale projection | unmount Artifact list；clear ArtifactStore | revert S10C page/history/event wiring | native authority rows remain | logout/rebind/tenant/session/delete/stale zero-hit | Product/Client/Security Owner |
| S10D harness escape/control/cleanup failure | stop Desktop/WebContent/Host/fake；keep D-V/E closed | remove H feature hooks/module/controller/runner/checker | preserve S10A-C authority；delete owner-only run root after content-free failure record | no mock/store/DB/spool seed；ports/PIDs/WAL/SHM/spool/temp/canary zero-hit | Technical/Security/Data Owner |

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Local disable | unset or set the four exact Host/Desktop/S10 Artifact flags above to `false`, then restart local Host/Desktop | local owner | no new v3 producer/transfer; v1/v2 text and persisted metadata reader remain | future 08/local smoke log |
| Local validation | commands in `06-test-plan.md` | developer | exact PASS/FAIL exits | `08-verification-report.md` |
| Paid image validation | only the frozen S12E/F runner after all prerequisite commits and Owner start | 段成威 | one content-free ledger entry per attempted provider call；hard max 5 | `08-verification-report.md` image evidence markers |
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
| 2026-08-21 | S8 implemented chain | S8A `bf5452f...` + S8B `4d0238b...` | bounded file projection/save + renderer/search component evidence | native/component PASS；runtime/page visual NOT RUN | production Chat vertical/manual visual/performance still S10；Markdown partial |
| 2026-08-21 | S9 readiness stage | Pattern 1.4.0 `b6f7401c...`；no S9 code/config/dependency | report conformance/projection/unknown/chart/save/export/lifecycle/rollback walkthrough | DESIGN PASS；implementation/runtime drill NOT RUN | first run S9A；S9B waits/blocked on ECharts；G4 pending |
| 2026-08-21 | S9A implemented | S9A `232ea6ce...` | consumer differential + private projection/canonical JSON save RED/GREEN and full gates | native PASS；renderer/chart NOT RUN | S9B readiness/dependency/theme/renderer remained |
| 2026-08-21 | S9B readiness stage | Pattern 1.5.0 `630c3c8...`；no package/lock/code/config | exact registry/license/import/bundle/theme/adapter/a11y/lifecycle/D-R rollback walkthrough | DESIGN PASS；S9B-D/R implementation NOT RUN | first run D only；R waits D immutable PASS；production vertical/G4 pending |
| 2026-08-21 | S9B implemented chain | D `0a36ca7...` + checker `aec0f8a...` + R `6bcc2a6...` | dependency/theme/adapter/card + ready-report component/security/visual | separate PASS；test-only 18-case browser matrix | production Chat/Tauri vertical still S10 |
| 2026-08-22 | S10 readiness stage | Pattern 1.6.0 `c1095eeb...`；S10A-E no code | keyless profile、single-v3/atomic cursor、private invalidation、page/vertical/sec-perf rollback walkthrough | DESIGN PASS；implementation NOT RUN | first run S10A only；B-E wait immutable predecessor |
| 2026-08-22 | S10D readiness stage | S10A/B/C separate PASS + Pattern 1.7.0 `8afdc996...`；no H/V/E code | production-path audit、H/V split、fresh-build/control/evidence/cleanup rollback walkthrough | DESIGN PASS；READY FOR S10D-H ONLY；runtime NOT RUN | first run H only；V/E wait immutable predecessor |
| 2026-08-23 | S10D-H failed implementation stage | Host `09d83cce...` + Desktop `997345d8...` | failed-smoke facts reviewed；no rerun | FAIL/PAUSED；no complete PASS；latest known class `runtime_axe_serious_critical` | exact attempt/RCA ledger must be recovered before resume or v2 claim |
| 2026-08-23 | S12 real-image design stage | docs-only；provider code absent；S12 campaign used `0/5`、reserved `0`；standalone probe unqualified | Runtime/Host/Desktop architecture、official API、budget/secret/rollback walkthrough | DESIGN RECORDED；IMPLEMENTATION/QUALIFIED-PAID/REAL-TAURI NOT RUN | first S12A governance migration；S12B-F wait |

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
| S9 readiness | 段成威（Product/Technical/Security/Data） | READY FOR S9A ONLY；canonical JSON save only；S9B WAIT/BLOCKED ON ECHARTS | 2026-08-21 | 03 §2F + 05/06/07 + Desktop Pattern 1.4.0 `b6f7401c79d5b2356bc45468f14d7fdbb17a855c` |
| S9B readiness | 段成威（Product/Technical/Security/Data） | READY FOR S9B-D ONLY；accessible table authoritative；unit/source/time range honestly unavailable；S9B-R waits | 2026-08-21 | 03 §2G + 05/06/07 + Desktop Pattern 1.5.0 `630c3c8d55a2617499f51bd5bed263b819aaf084` |
| S10 readiness | 段成威（Product/Technical/Security/Data） | READY FOR S10A-LOCAL-PROFILE ONLY；S10B-E WAIT/NOT RUN | 2026-08-22 | 03 §2H + 05/06/07 + Desktop Pattern 1.6.0 `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` |
| S10D readiness | 段成威（Product/Technical/Security/Data） | READY FOR S10D-H ONLY；S10D-H/V、S10E NOT RUN | 2026-08-22 | 03 §2I + 05/06/07 §26 + Desktop Pattern 1.7.0 `8afdc996c11bbad2d275eb8b86a0f6b82ca5da52` |
| S10D-H execution state | 段成威 | FAIL/PAUSED；不得关闭、续跑或描述成 PASS | 2026-08-23 | Host `09d83cce...` + Desktop `997345d8...` + `08-verification-report.md#EV-128-S10D-H-FAIL`（incomplete failure index，不是 v2 PASS evidence） |
| S12 real-image scope/eval budget | 段成威 | 文生图+单人物参考图生图纳入 FEAT-128；中国区 `image-01`；最多 5 次 S12 campaign 付费验证；生产未批准 | 2026-08-23 | 00-07、04A 与 `08-verification-report.md#EV-128-IMG-SCOPE-20260823`（Owner decision index，不是 v2 PASS evidence） |
| G4 local candidate | 段成威 | NOT REQUESTED | N/A | S10D-H/S10D-V/S10E/S11 and full AC/E2E/review incomplete；Markdown unresolved for full AC-005 |
| Go/No-Go production | 段成威 | N/A current scope / not approved | N/A | no production plan |
