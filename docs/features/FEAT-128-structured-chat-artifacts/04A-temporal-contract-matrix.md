# FEAT-128 Temporal Contract Matrix

> 本文自 2026-08-23 起作为真实图片范围的时序设计权威。当前 `feature.yaml` 仍是历史
> `schema_version: 1`；在任何新 G2V/G3 声明前，必须把本文的 Scenario、Invariant、Test ID 与真实
> S10D-H failure ledger 一并迁移到 schema v2。本文中的 `NOT RUN` 不能支持 PASS。

## 1. 适用性与权威源

- 适用结论：适用。该链路跨 Runtime、Host provider side effect、Host durable/ephemeral authority、v3 通知、
  Desktop SQLCipher replay 与 cleanup。
- Runtime authority：固定 yijie-codex 的 `thread/start.dynamicTools`、`item/tool/call` 与
  `dynamicToolCall` item；精确 commit 在 S12B compatibility candidate 中固定。
- Provider authority：MiniMax 中国区图片生成官方指南与 T2I/I2I OpenAPI；访问基线 2026-08-23。
- Artifact authority：yijie-contracts v3 image Artifact、Host staging/ACK 与 Desktop SQLCipher v8。
- Producer Owner：Agent Host；Persistence Owner：Agent Host + Desktop；Consumer Owner：Desktop。

## 2. 六阶段时序

下表严格使用 schema v2 的六个 phase。MiniMax HTTP 是 `producer` 内部子步骤，不另造第七个 provider phase；
Desktop 首次 GET/SQLCipher commit 属于 `persistence`，只有 crash/restart/history reconciliation 才属于 `replay`。

| Phase ID | 前置状态 | 动作 | Durable commit/authority | Notification/consumer | 失败与恢复 |
|---|---|---|---|---|---|
| TMP-128-IMG-001 producer | exact flag、Host Key、active turn、结构化 call 与 authority 合法 | 用 `(thread,turn,call)` + 参数摘要 claim operation；原子取得一个 `reserved_slots`；I2I claim 当前轮唯一图片；accepted/reserved 落账后、首次 network write 前发布 `started`；发送期间只允许无伪百分比 progress；至多一次 POST 固定 China origin/model/base64/n=1；严格校验响应 | operation 先记 `accepted/reserved`；紧邻首次网络 write 前原子转 `sent`、释放 reservation 并不可逆 `used_calls += 1` | started/progress 是 producer live 子事件，不代表 ready；只允许结构化 call 触发，Host 不按文本猜测 | pre-send reject/cancel 释放 reservation 且不增 used；sent 后 success/provider error/timeout/outcome unknown 均已消费；不自动重试 |
| TMP-128-IMG-002 persistence | operation 已 claim；或 provider 输出已通过校验 | ledger 迁移原子写入；decoded bytes 计算 MIME/尺寸/size/SHA 并写 encrypted Host staging；Desktop 首次 GET 后校验内容 | Host manifest + encrypted bytes 先成为 ready authority；Desktop SQLCipher ready BLOB、ACK intent 与 v3 cursor 再原子 commit | provider raw/base64 不进入 Runtime/Desktop；Desktop 只有本地 commit 后才是 local ready | store 失败只清 input/intermediate，不产生 ready；Desktop commit 失败不 ACK，Host ready staging 保留至合法清理条件 |
| TMP-128-IMG-003 notification | Host ready 或稳定失败终态已持久化 | 只有 Host ready commit 后发布 durable `completed`；稳定失败发布 `failed`；Host 回复 Runtime content-free tool result | notification 不是图片 authority；tool result 不保存图片、prompt、参考图或 provider payload | v3 Artifact 与文本共用单一有序 stream；Desktop reducer 幂等合并；Desktop commit 后发 ACK/private invalidation | Runtime reply/终态通知失败不得重发 provider；Host ready 可由 history/resync 恢复 |
| TMP-128-IMG-004 replay | restart、stream gap、history reopen 或 pending ACK；不属于普通 happy path | 从 Host ready authority或 Desktop SQLCipher/cursor/ACK intent 恢复；只重放既有 operation/Artifact | replay 只读取既有 durable state，不创建新付费 identity | history v3/ArtifactStore 恢复同一 Artifact；pending ACK 幂等补发 | `sent` 且结果未知不得补发 provider；无 durable ready bytes 时不得伪造 completed |
| TMP-128-IMG-005 terminal | provider、Artifact、tool、turn 各自达到合法终态 | interrupt/failure 把未终态 Artifact 映射 failed/cancelled；turn terminal 不回退 Artifact | operation ledger 保留最小 content-free terminal/tombstone 到幂等窗口结束 | terminal 单调；Host ready 与 Desktop local ready 分层；ready 只可再到 expired | outcome unknown 不自动重试；late response 丢弃；普通 terminal 不删除仍待 GET/ACK 的 ready staging |
| TMP-128-IMG-006 cleanup | input/intermediate 结束，或 ready authority 达到各自清理条件 | tool/turn terminal、interrupt、pre-send cancel、shutdown 清 current-turn ref、provider JSON/base64/decoded intermediate；Host ready staging 只由 ACK、24h TTL、session delete 或 restart authority 清理；Desktop ready 内容只由 168h retention 或 session delete 清理 | Host 与 Desktop cleanup receipt/状态保持各自既有 authority | 历史仅保留允许的最小 metadata/expired；不删除用户已另存文件 | cleanup 幂等；残留/WAL/spool/handle 未清记 incomplete；不得以普通 terminal/shutdown 提前删除可读取 ready 产物 |

## 3. Scenario

| Scenario ID | Ordered phases | 说明 |
|---|---|---|
| FLOW-IMG-T2I-001 | producer → persistence → notification → terminal → cleanup | 文生图 happy path，一次调用、一个 provider Artifact；普通成功路径不冒充 replay |
| FLOW-IMG-I2I-001 | producer → persistence → notification → terminal → cleanup | 当前 turn 单 PNG/JPEG `subject_reference.character` |
| FLOW-IMG-NO-CALL-001 | producer → terminal → cleanup | 普通文本/看图不调用 provider；台账不增 |
| FLOW-IMG-DUPLICATE-001 | producer → persistence → replay → terminal → cleanup | 新到达 duplicate call 先校验 identity/digest；同参读取既有 operation/result，不二次付费；异参 fail closed |
| FLOW-IMG-CANCEL-001 | producer → persistence → notification → terminal → cleanup | pre-send 与 post-send cancel/timeout 区分；迟到响应丢弃 |
| FLOW-IMG-CRASH-001 | persistence → replay → terminal → cleanup | 仅描述 crash 后恢复：不重复外部调用，依 durable authority 恢复；崩溃前 producer 事实由 ledger 冻结 |
| FLOW-IMG-FAIL-001 | producer → persistence → notification → terminal → cleanup | auth/balance/rate/safety/param/5xx/invalid response 均无伪 ready |

## 4. 顺序与不变量

| Invariant ID | 不变量 | Duplicate/out-of-order | Terminal rule | Crash/restart rule | Fail-closed behavior |
|---|---|---|---|---|---|
| TINV-IMG-001 | 只有 Runtime structured call 能触发 provider；Host 不做文本猜测 | 相同 call identity/参数最多一次外部发送 | no-call 直接完成文本 turn | restart 不补发未证请求 | invalid method/tool/args/authority 不外发 |
| TINV-IMG-002 | 单一 durable campaign `feat128-s12-image-validation-20260823`；`P1=S12E/T2I`、`P2=S12E/I2I`、`P3=S12F/T2I`、`P4=S12F/I2I`、`R1=repair(original_slot_id)`；slot CAS `available → reserved → sent`，aggregate 只由 slot 推导 | 两个 runner/并行进程对同一 slot authority CAS；同参复用、异参或 wrong stage/mode 拒绝；fake HTTP 不增 used | pre-send 原子释放回 available；sent、分类/总计与 R1 authorization 消费同事务；sent 后 outcome unknown 也是已消费终态 | startup 回收 orphan reserved、不补发；sent-without-result 保留 used；restart、新 run root、临时目录删除都不能重置；ledger 缺失/漂移 fail closed | planned cap=4；repair cap=1 且绑定原失败+一次性 Owner authorization/RCA，不能用于新场景；总 hard cap=5 |
| TINV-IMG-003 | Host staging durable ready 必须早于 Artifact completed | duplicate completed 幂等 | failed/ready 单调；late success 不越过 cancel | ready 可重放，未提交 bytes 不可发布 | 任一响应/媒体校验失败清 bytes 并 failed |
| TINV-IMG-004 | Desktop SQLCipher ready+ACK intent+cursor commit 必须早于 ACK | replay 不重复下载已提交同 digest 内容 | local ready 只在 commit 后 | crash 后恢复 pending ACK | digest/scope/revision 不符触发 resync/failed |
| TINV-IMG-005 | Runtime tool result永不含图片、Key、prompt、参考图或 provider payload | duplicate result content-free | tool failure 不覆盖已发布 Artifact terminal | transcript/history 不成为图片 authority | zero-hit canary 失败立即 kill switch |
| TINV-IMG-006 | input/intermediate 与 ready staging 分开清理：前者按 operation/turn 生命周期，后者只按 ACK/24h TTL/session delete/restart authority | cleanup 幂等且不把普通 terminal 当 ready ACK | 用户另存文件不受 cleanup 影响 | restart 清不可恢复 Host ephemeral data；Desktop durable authority仍按 retention | 提前删除 ready staging 或残留/WAL/spool/handle 未清都 fail closed |

## 5. 可执行 Temporal Conformance

| Test ID | Invariant IDs | Producer fixture/driver | Consumer/reader | Exact command | Environment | 当前状态 |
|---|---|---|---|---|---|---|
| TCONF-IMG-001 | TINV-IMG-001, TINV-IMG-002 | fake Runtime dynamic call + fake MiniMax HTTP | Host reverse-request router/ledger | `go test ./internal/codex ./internal/session ./internal/imagegen -run 'Feat128ImageTool' -count=1` | locked Go, zero network/key | NOT RUN |
| TCONF-IMG-002 | TINV-IMG-002, TINV-IMG-003, TINV-IMG-005 | adversarial fake MiniMax responses | Host adapter/Artifact manager | `go test ./internal/imagegen ./internal/session -run 'Feat128ImageProvider' -count=1` | loopback fake HTTP | NOT RUN |
| TCONF-IMG-003 | TINV-IMG-002, TINV-IMG-003, TINV-IMG-006 | delay/cancel/crash fake server | Host ledger/staging cleanup | `go test ./internal/imagegen ./internal/session -run 'Feat128ImageRecovery' -count=1` | temp owner-only root | NOT RUN |
| TCONF-IMG-004 | TINV-IMG-003, TINV-IMG-004, TINV-IMG-005, TINV-IMG-006 | real v3 image Artifact from fake provider | Desktop coordinator/SQLCipher/image client | `cargo test --manifest-path src-tauri/Cargo.toml --features feat128-real-image feat128_real_image` | macOS Tauri, fake provider | NOT RUN；S12D 需实现该 exact target |
| TCONF-IMG-005 | TINV-IMG-001, TINV-IMG-002, TINV-IMG-005 | T2I/I2I/no-call intent dataset | MiniMax-M3 + Runtime dynamic tool | `./scripts/run-feat128-s12e-image-capability.sh` | isolated paid eval, call fuse | NOT RUN；S12E 需实现该 exact runner |
| TCONF-IMG-006 | TINV-IMG-001, TINV-IMG-002, TINV-IMG-003, TINV-IMG-004, TINV-IMG-005, TINV-IMG-006 | real T2I/I2I operations | production ChatPage/Artifact renderer/save/history | `./scripts/run-feat128-s12f-real-image-vertical.sh` | macOS Tauri release-like | NOT RUN；S12F 需实现该 exact runner |

尚不存在的测试命令不会被当作已执行事实；在相应 slice G3 前必须替换为仓库内真实 exact command、完整 commit、
exit code、ISO 时间与 `08-verification-report.md#EVIDENCE-ID`。

## 6. G2V 代表路径

| Harness ID | 覆盖 | 真实平台 | Production bootstrap | 最小代表数据 | 当前状态 |
|---|---|---|---|---|---|
| H-IMG-TOOL-001 | dynamic tool reverse request、fake provider、Artifact publish | Host + pinned Runtime | required；NOT VERIFIED | 一条 T2I、一个 1x1 fake image | NOT RUN |
| H-IMG-PAID-001 | 真实 image-01 capability、错误与 shared campaign ledger | isolated local Host | N/A；release-like Host config NOT VERIFIED | campaign P1-P2：合成 T2I + 单人物 PNG/JPEG I2I；与 S12F 共用同一 durable authority | NOT RUN；S12 campaign used `0/5`、reserved `0` |
| H-IMG-VERTICAL-001 | M3 decision → Host provider → v3 → Desktop | macOS real Tauri | required；NOT VERIFIED | planned slots P3-P4：各一条 T2I 与 I2I turn；repair slot R1 仅供失败修复后复验，发送序号不固定 | NOT RUN |

S10D-H 不属于这些 harness：它是 keyless/synthetic/zero-provider，当前 smoke FAIL 且暂停；不得用它证明真实生图，
也不得用真实生图绕过或关闭它。S12A-D 与 Host-only S12E capability probe 可在 H 暂停时独立推进；S12F
进入 real Tauri 前，schema v2 必须显式记录并解决重叠 blocker：要么 H 在单独授权下形成 immutable PASS，要么
Owner 批准一个不借用 H 证据、仍覆盖 production bootstrap/a11y/teardown 的 H-IMG-VERTICAL exception。两者都不能删除 H failure ledger。

## 7. 失效与 Owner 评审

下列变化使相关证据失效：Runtime pin/experimental capability、dynamic tool schema、MiniMax endpoint/model/API、
provider default/错误语义、ledger/预算/cancel、Artifact contract/pin、Desktop coordinator/persistence/renderer、secret handoff、
harness/production bootstrap 或 fixture digest。

| Owner | 结论 | 日期 | 边界 |
|---|---|---|---|
| Product | SCOPE APPROVED；tests NOT RUN | 2026-08-23 | T2I + 单人物主体参考 I2I；非通用编辑 |
| Technical/Producer/Consumer | DESIGN RECORDED；G2/G2A/G2V NOT RUN | 2026-08-23 | dynamic tool→Host→provider→Artifact；需 immutable compatibility candidate |
| Security/Data | BOUNDED VALIDATION AUTHORIZED；implementation NOT RUN | 2026-08-23 | Host-only Key、最多 5 次、no URL/no retry/content-free evidence |
