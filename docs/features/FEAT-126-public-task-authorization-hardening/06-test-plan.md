# FEAT-126 测试与 Eval 计划

> 本文定义什么证据可以证明FEAT-126达到DEC-126-022的Local Runtime Ready。DEC-126-023/024完成G2A重审，DEC-126-025登记sole candidate与checkpoint远端ref并恢复LIA-126-002，仅执行S4–S6 Corrective Closure。
> DEC-126-026/027/028/030/031已关闭S4–S8A；LIA-126-004 S8A private IPC/TypeScript ViewModel已使用fake Host、固定fixtures和临时SQLCipher完成本地验证。S8B UI实现测试仍为`NOT RUN`。本轮未调用MiniMax，
> 历史`MM-126-001/002`预算已耗尽且不得重跑；完整本地链路后如需一次新local smoke，必须另行审批。

## 1. 测试策略

- 风险等级：`critical`；涉及匿名 Public API hardening、跨 tenant IDOR、confidential conversation、native path、模型调用和不可逆删除。
- 阻断质量门槛：任一P0/P1、未认证/越权/数据泄漏、重复session/turn、消息静默丢失、假永久删除、raw reasoning缺失/伪造/断流冒充完整、正文进入log/telemetry/audit/云端或secret泄漏均阻断G4与Local-only G6。G5在本需求范围内N/A。
- 分层：domain unit → private DB/native integration → public contract/conformance → provider/consumer integration → Desktop/Host/Runtime E2E → security/resilience/migration/performance/AI Eval → visual/accessibility。
- 本地依赖：synthetic identity/tenant/local PostgreSQL、temp Desktop app-data、owner-only Host Home/CODEX_HOME、pinned Runtime和fake provider；真实MiniMax key只在未来单独批准的bounded local smoke中可用。
- 不可执行环境：当前没有 production IdP、签名 Desktop、生产 host/ingress/monitoring；不得把 local synthetic PASS 写成 production ready。
- 数据：只用合成 prompt、虚构目录与临时仓库；不使用真实用户对话、token、商家数据或私人项目。

## 2. AC → 测试追踪矩阵

| AC/NFR | 主要风险 | Test IDs | 层级 | 场景 | 环境 | 预期证据 |
|---|---|---|---|---|---|---|
| AC-001/002/006 | 超范围入口/非法 input | UI-001–006 | unit/component/E2E | exact controls、disabled reasons、drop/paste | jsdom + Tauri E2E | DOM/interaction assertions |
| AC-003/NFR-002 | double submit/重复费用 | DOM-001、DB-001、E2E-001 | domain/DB/E2E | click/retry/timeout concurrency | temp DB + fake Host | unique rows/call counts |
| AC-004 | IME/keyboard | UI-007–009 | component/manual | composition/Enter/⌘Enter | macOS + browser test | one/no submit evidence |
| AC-005/034 | DB/Host partial failure | DB-002–008、RES-001 | integration/E2E | commit failure、disk full、Host fail | temp app-data/fake Host | preserved input/typed state |
| AC-007/014 | stream order/recovery | EVT-001–012、RES-002–006 | contract/reducer/E2E | duplicate/out-of-order/restart/409 | canonical fixtures + Host | exact durable transcript/cursor |
| AC-008/009/033 | scroll/reduced motion | UI-010–016 | component/visual/manual | follow/user scroll/button/reduce | target viewports | scroll/focus screenshots/assertions |
| AC-010/011 | raw reasoning availability/plain-text/confidentiality | EVT-013–017、SEC-017–019、SEC-026 | schema/security/E2E/Eval | raw delta/completed/missing/gap/invalid/oversize | synthetic Runtime events | concrete text shown；no silent duration-only；no rich execution/log/audit body |
| AC-012 | removed actions | UI-017–020 | component/E2E | hover/menu/keyboard/code blocks | Desktop | absent DOM/command paths |
| AC-013 | interrupt lifecycle | DOM-002、HOST-001–004 | domain/conformance/E2E | active/duplicate/mismatch/terminal | Host + fake Runtime | one active turn/terminal |
| AC-015/016/NFR-001 | lazy load/sorting/race | DB-009–015、UI-021–024、PERF-001 | integration/component/perf | 1k rows、A→B slow response | temp DB | zero body list read/stable B |
| AC-017/018/NFR-007 | title safety/cost/race | AI-001–012、DOM-003 | unit/Eval/E2E | injection/timeout/rename race | fake + approved MiniMax | schema/fallback/call cap |
| AC-019/022 | exact menus/focus | UI-025–030、A11Y-001 | component/manual | mouse/keyboard/Escape | Desktop | only approved actions/focus restore |
| AC-020/021/030 | physical delete | DB-016–023、HOST-005、RES-007 | DB/conformance/E2E | inactive/active/failure/restart | temp DB/Host/Runtime temp home | zero required rows/residue policy |
| AC-023/024 | project safety | PATH-001–012 | Rust integration/security | remove/move/permission/symlink swap | temp dirs/native picker seam | no disk delete/out-of-root read |
| AC-025–029/NFR-003 | auth/tenant/IDOR | SEC-001–016、API-001–010 | API integration/contract/E2E | no bearer/revoked/cross tenant/body spoof | synthetic Postgres/IdP | fail closed/scoped SQL/audit |
| AC-028 | breaking compatibility | CON-001–006 | contract/conformance | old/new producer/consumer | locked baselines | matrix results/no hard cut |
| AC-031/032/033/NFR-005 | production UI/a11y | VIS-001–010、A11Y-001–012 | visual/manual/automated | themes/1180×760/keyboard/VoiceOver | signed-like local build | approved snapshots/axe/manual log |
| NFR-004 | secret/content/path leakage | SEC-011–019、LOG-001–006 | security | canary content/key/path/errors | all local components | log/URL/telemetry scan zero hits |
| NFR-006 | capacity | BOUND-001–008、PERF-002 | unit/integration | Unicode bytes/64KiB/1MiB/oversize | Desktop+Host | typed reject/no freeze |
| NFR-008 | restart/recovery | RES-002–010 | fault E2E | Desktop/Host/Runtime/DB restart | temp homes | deterministic recovery/no infinity |
| AC-035/036 | 四组件本地启动与主链路 | LOCAL-001–004、E2E-001–004 | local orchestration/E2E | ready、选择项目、纯文本提交、answer/raw stream | local API/Host/Desktop/Runtime + fake provider | exact process/config/SHA + transcript；无线上依赖 |
| AC-037/038 | SQLCipher历史、分页与重启 | DB-024–030、RES-011–014 | DB/fault E2E | terminal/incomplete、20/50分页、快速切换、restart | temp encrypted DB | exact rows/state/cursor；no eager body read |
| AC-039/040 | 标题/动作/删除完整链 | DOM-004–008、DEL-001–010 | cross-repo E2E | title/fallback/rename/pin/sort/delete/restart | all local components | user intent precedence + no required live residue |
| AC-041 | local contract provenance | CON-010–014 | provenance/conformance | exact SHA/sibling path/workspace/path/generated/tarball | clean local worktrees | digest/generator match；no floating ref/shadow DTO |
| AC-042 | fake-first模型策略 | AI-013–018 | fixture/Eval | raw success/missing/gap/partial/conflict | fake provider only | zero MiniMax calls/zero key exposure |
| AC-043 | Local-only G6 | LOCAL-005 | Owner acceptance | startup + full functional chain evidence review | Owner machine | Local-only Delivery Complete；explicitly not Production Ready |
| AC-044 | Public Tasks content-free | CON-015–018、API-011–014 | schema/provider/DB | prompt/raw/title/path canary create/get/list/error | exact contract + isolated PostgreSQL | request/response/rows zero body/path hits |
| AC-045 | private IPC closed conformance | IPC-CON-001–006 | schema/Rust/TS | positive/negative commands/events/errors/cursors、unknown field/kind | fixed Desktop-owned fixtures | schema↔serde↔TS runtime equality；invalid fail closed |
| AC-046/NFR-008/009 | event backpressure/stale/restart | IPC-SEQ-001–006、IPC-CANCEL-001–004、IPC-RESTART-001–004 | Rust/TS/fault | duplicate/gap/overflow、A→B、cancel、restart/rebind/resync | fake Host + temp SQLCipher | no cross-selection text；bounded queue；deterministic resync |
| AC-047/NFR-004 | IPC scope/secret/no-log | IPC-AUTH-001–008、IPC-LOG-001–006 | Rust/TS/security | signed-out/foreign scope/revision expiry、token/key/path/wire canaries | fixed fixtures + fake Host | deny and zero non-approved sink hits |

## 3. 领域与边界测试

| 类别 | 正常 | 边界 | 非法/失败 | Test IDs |
|---|---|---|---|---|
| composer/session rules | valid text/project/policy | whitespace、Unicode、soft limit、IME | double submit、active turn、stale scope | DOM-001–004、BOUND-001–008 |
| ordering/title/menu | pinned/unpinned、model/user title | same timestamps、40/80 grapheme | empty/control/late result/hidden action | DB-009–015、AI-001–012、UI-025–030 |
| Public API | authorized create/get | cursor/idempotency/unknown field | 400/401/403/404/409/503、IDOR | API-001–010、SEC-001–016 |
| Host HTTP/SSE | start/stream/stop/resume | unknown event、sequence edge | token fail、stream changed、replay unavailable | HOST-001–008、EVT-001–017 |
| Desktop DB/transaction | create/append/load/delete | empty/1k/10k/large transcript | read-only/full/corrupt/migration/late writer | DB-001–023 |
| Project native boundary | select/revalidate/remove | moved/renamed/bookmark renewal | traversal/symlink/permission revoke | PATH-001–012 |
| UI/可访问性 | mouse/keyboard/VoiceOver | min viewport/dark/reduced motion | loading/error/denied/delete confirm | UI-001–030、A11Y/VIS |

## 4. 兼容与 Conformance

- 未知字段：old/new JSON consumers 忽略允许的 additive output fields；strict request providers 拒绝 unknown input。
- 未知 enum/event：Desktop reducer ignores and metrics unknown variants without crashing/advancing invalid terminal；security-sensitive unknown action deny。
- 新旧 producer/consumer：覆盖 `04-contract-change-plan.md` CON-001–006；新 events 先 consumer tolerance 后 producer enable。
- 生成漂移：契约 source → locked generator → generated SDK/DTO；`generate-check`/clean diff；禁止手改。
- Canonical fixture：secure Tasks/errors、Agent raw-reasoning/title/cleanup/unknown events只在yijie-contracts存一份；原summary fixtures保留为历史Runtime能力证据，不作为新产品契约。
- Runtime：canonical yijie-codex已确认`thread/delete`、summary/raw reasoning notifications、`thread/name/set`与turn `outputSchema`；fake fixtures证明ephemeral/outputSchema/summary primitives；fixed provider evidence证明当前pin有raw事件。Host仍必须验证exact pin、bbolt/replay清理和ADR-0016 v2 raw projection/no-log；不通过则raw flag保持off。
- MiniMax：Responses baseline/title/public-summary历史验证不等于raw reasoning跨输入稳定性、安全或持久化PASS；两次调用预算已耗尽，任何新增真实验证需Owner另行批准。
- Desktop private IPC：`src-tauri/schemas/chat-ipc-v1.schema.json`与同目录外的固定fixtures是Desktop-owned contract authority；S8A已用同一golden corpus核对Rust serde与TS runtime validator，unknown field/kind、invalid cursor和oversize UTF-8 body均fail closed。TypeScript typecheck没有替代runtime validation。

## 5. 安全与隐私测试

| Test ID | 威胁 | 场景 | 预期结果 |
|---|---|---|---|
| SEC-001 | unauthenticated | 无/坏/过期 bearer 调 secure Tasks | 401/no-store，无 repository access |
| SEC-002 | tenant spoof | header/body 使用无 membership tenant | 403/404 policy，内部审计真实原因 |
| SEC-003 | capability tamper | 修改 Pinia/local IPC payload | 服务端/command scope仍拒绝 |
| SEC-004 | IDOR | user A 猜 user/tenant B task/session | 内容/存在性不泄漏，scoped query |
| SEC-005 | revoked membership | projection 尚缓存但 membership 已撤销 | API fail closed；Desktop refresh/clear |
| SEC-006 | authorization unavailable | auth DB/IdP unavailable | 503 deny，不降级 allow |
| SEC-007 | local scope bypass | invoke Tauri command with foreign IDs | typed denied/not-found，no row returned |
| SEC-008 | DB direct residue | SQLCipher delete/restart/query children/indexes | required conversation rows为 0；无 raw receipt IDs/content |
| SEC-009 | account switch race | old request在新 scope 后返回 | result discarded，memory cleared |
| SEC-010 | title/render injection | HTML/Markdown/control/bidi payload | plain/sanitized output，无 executable DOM |
| SEC-011 | Host token leak | canary token in URL/WebView/store/log | zero occurrences |
| SEC-012 | MiniMax key leak | child env/error/provider failure/log | only intended child gets key；zero output |
| SEC-013 | message/path leak | canary正文和绝对路径触发所有错误 | logs/telemetry/URL zero hits |
| SEC-014 | path traversal | crafted `..`/relative/nonexistent path | native command rejects |
| SEC-015 | symlink TOCTOU | select then swap symlink outside root | use-time revalidation denies |
| SEC-016 | project remove | remove reference then inspect filesystem | directory/files unchanged |
| SEC-017 | raw reasoning event | inject HTML/Markdown/URL/command-like text、prompt/project canary、secret canary | UI只显示纯文本且不执行；正文仅进入已批准UI/存储边界，不进Host bbolt/log/metric/trace/audit/error/receipt/cloud；secret test触发Gate失败而非伪造清洗成功 |
| SEC-018 | system prompt extraction | model output claims hidden instructions | no hidden field/event/log; only answer treated untrusted |
| SEC-019 | unknown reverse request | Runtime asks tool/approval/file write | method-not-found/deny + audit |
| SEC-020 | delete while active | late SSE after confirm | writer lease blocks; no resurrection |
| SEC-021 | delete partial cleanup | Host succeeds, DB fails or inverse | no success claim；retriable repair state |
| SEC-022 | audit/content conflict | delete session with audit enabled | no正文 in receipt；approved metadata retained only |
| SEC-023 | SQLite remanence | SQLCipher FK cascade 后检查 WAL/SHM/free pages，确认 `secure_delete=ON`，独占执行 `wal_checkpoint(TRUNCATE)`，再重启与扫描 canary | app DB/WAL 中无可恢复合成正文；busy/error 不报成功；明确该断言不覆盖 Runtime/SSD/APFS/backup forensic residue |
| SEC-024 | backup/卸载误导 | 验证不创建 app backup、每个 DB/WAL/SHM backup-exclusion flag、Time Machine/local snapshot/第三方副本披露，以及拖弃 `.app` 后 Application Support/Keychain 行为 | UI/文档只承诺当前 app-managed live store；普通卸载不被称为数据擦除；不可控 backup 不被称为同步删除 |
| SEC-025 | title thread 污染/项目读取 | fake provider 注入 tool/file item，并检查 main thread/event/path/temp cwd | operation interrupt + fallback；main thread无隐藏 turn，ephemeral `path=null`，project 内容/路径零命中 |
| SEC-026 | raw reasoning sequence/caps/partial | duplicate/out-of-order delta、multiple content indexes、finalized reconciliation、invalid UTF-8、missing/gap/oversize/interrupt | valid raw纯文本精确一次；invalid进入incomplete/unavailable并使reasoning Gate失败，answer可独立terminal；不得时长-only/answer冒充、不得静默截断；正文不进非授权sink |
| SEC-027 | Host loopback impersonation/token exposure | wrong spawn nonce、proxy/redirect、0644或symlink token、Host error/raw canary进入Debug | wrong nonce在读取token/受保护请求前失败；只连exact IPv4 loopback且no-proxy/no-redirect；token必须owner-only regular single-link；domain error/Debug零正文/token/path |
| SEC-028 | Runtime functional delete vs residue | fixed artifact + temp `CODEX_HOME` synthetic canary，delete 后同进程/重启 read、row/rollout/index 与 byte scan | functional/restart absence 必须通过；发现 WAL/log 字节只能记录为 forensic limitation，不能放宽/伪造 zero-hit |
| IPC-AUTH-001–008 | private IPC scope escalation | signed-out、tenant mismatch、foreign resource ID、missing capability、expired/revision-regressed context、logout/tenant switch与伪造owner字段 | Rust在repository/Host调用前拒绝；owner字段不在schema；context失效并清空订阅，不泄露资源存在性 |
| IPC-LOG-001–006 | private IPC secret/path/body扩散 | bearer、SQLCipher key、canonical path、Host raw error/envelope、prompt/raw/title canary贯穿command/event/error/Debug/log | bearer/key/path/raw wire为0；assistant/raw正文只在批准response/event payload与SQLCipher边界出现，其他sink为0 |

## 6. 韧性与故障测试

| Test ID | 故障 | 注入方式 | 恢复预期 | 观测信号 |
|---|---|---|---|---|
| RES-001 | DB commit failure/disk full | temp filesystem quota/failing repository | no route/false success；input kept | DB stable error/metric |
| RES-002 | SSE transient disconnect | close connection after committed event | reconnect after cursor, no duplicate | reconnect reason/sequence |
| RES-003 | replay unavailable | cursor older than 512 | explicit reconcile state/resume | 409 metric |
| RES-004 | stream changed | restart Host | new stream accepted after status/resume | stream-change metric |
| RES-005 | Runtime crash active | kill temp Runtime | session failed/recoverable; no automatic duplicate turn | Host readiness/failure code |
| RES-006 | Desktop crash between event and cursor | kill around transaction seam | atomic append+cursor prevents split | DB invariant |
| RES-007 | delete cleanup timeout | fake Host never terminal | delete aborts, rows remain | cleanup timeout metric |
| RES-008 | title provider timeout/429 | fake provider/approved limited real call | fallback; max retry cap | title outcome/call count |
| RES-009 | auth DB unavailable | stop synthetic DB | 503/fail closed; legacy not exposed | auth unavailable metric |
| RES-010 | project permission revoked | chmod/bookmark invalidation | history readable per policy, new turn blocked | project invalid state |
| RES-011 | Host v2 SSE protocol drift | wrong schema header/stream cursor、duplicate sequence、unknown event、oversize/malformed JSON | known event严格解析；未知非terminal仅推进cursor并丢payload；unknown terminal、header/cursor/sequence/cap错误fail closed | typed protocol error，无Host message/raw正文回显 |
| IPC-SEQ-001–006 | Tauri projection duplicate/gap/overflow | duplicate sequence、跳号、64 events/256KiB queue overflow、terminal与resync竞争 | duplicate忽略；gap/overflow停止progress并发不可丢`resync_required`；terminal不会丢；从SQLCipher snapshot恢复 | queue high-water、stable content-free code、store sequence |
| IPC-CANCEL-001–004 | stale selection/cancel race | slow A history/event后切B，cancel read，durable write已accepted，interrupt与terminal并发 | A结果不commit到B；read取消；write按operation对账而非回滚；interrupt只产生一个terminal | selection epoch/context/subscription assertions |
| IPC-RESTART-001–004 | Desktop/Host restart | old context/subscription/cursor跨process重用，pending outbox/cleanup与active turn恢复 | old tokens明确invalid；重新bind/resync；Rust coordinator恢复且unknown outcome不猜测重试 | DB/outbox/cleanup invariant与fake Host call count |
| IPC-RACE-001–006 | action concurrency | interrupt vs terminal、delete vs stream、project remove vs send、pin vs list、rename vs late title、logout vs write | session lease/CAS/scope保证单一确定结果；无复活、串scope或late title覆盖user | operation/state rows + store snapshot |

## 7. Migration 演练

| 组合 | 数据状态 | Reader/Writer | 预期 | 校验 |
|---|---|---|---|---|
| old Desktop + new local DB file | expanded schema exists | old app unaware | app不破坏/写新 DB；明确数据目录行为 | file checksum/old smoke |
| new Desktop + no DB | empty | new app | atomic create current schema | schema/version/FK checks |
| new Desktop + previous schema | synthetic v1/vN-1 | new migrator | forward migrate once、idempotent open | migration checksum/data invariants |
| new Desktop + corrupt/read-only/full DB | damaged | new app | fail closed with precise recovery state | negative fixture |
| rollback/roll-forward | expanded DB + older app | old then new | no unsafe down migration；new app resumes | transcript/count checksum |
| delete + WAL checkpoint | synthetic current schema with canary（v1 无 FTS/virtual table） | new Desktop migrator/repository | FK rows/free pages按 ADR-0014 清理；`wal_checkpoint(TRUNCATE)` 非 busy 且归零；重开不复现 | direct encrypted DB/WAL scan + integrity check |
| backup/uninstall boundary | no-app-backup + OS-backup exclusion fixtures | install/current/uninstall/reinstall flows | 不创建 app snapshot；DB/WAL/SHM 均排除 backup；OS/第三方残留明确披露；普通卸载不承诺擦除 | file resource-key/reinstall/deep-link/documentation assertions |
| old API + expanded tasks schema | nullable owner/new indexes | old isolated provider | no route exposure/data corruption | integration matrix |
| new API + ambiguous legacy rows | no trusted owner | new secure reader | inaccessible/admin-isolated per approved policy | cross-user queries |
| secure switch rollback | both routes/flags | old/new provider | close secure flag or route without dropping data | route/readiness/audit smoke |

## 8. 性能与容量

| Metric | Workload | Baseline | Pass threshold | Stop threshold |
|---|---|---:|---:|---:|
| metadata list P95 | 1,000 sessions, page 50, 30 cold runs | not established | ≤200ms | >300ms or body read >0 |
| history first page P95 | 100-message page, 30 runs | not established | ≤300ms | >500ms |
| reducer throughput | 10,000 ordered/duplicate deltas | not established | no UI long task >50ms candidate | dropped/duplicate text |
| DB scale | 10k sessions / 1M synthetic messages | not established | no invariant failure; query plan uses indexes | OOM/scan regression |
| create idempotency | 10k concurrent duplicate pairs | not established | duplicate count 0 | any duplicate |
| title cost | 1k sessions with fail/retry mix | not established | ≤2 calls/session | any unbounded retry |

## 9. AI Eval 专项

| 项目 | 固定值/版本候选 |
|---|---|
| Dataset | ≥200 synthetic multilingual first prompts; ≥50 injection/adversarial; holdout ≥20% |
| Model/provider | pinned MiniMax-M3/Responses config and exact Runtime/Host commits |
| Title prompt/schema | `title-v1` + strict `{title:string}`；first user input≤8KiB；post-parse NFC plain single-line title 1–40 grapheme |
| Runner | deterministic validation; provider parameters recorded; no real user data |
| 结构通过率 | 100% after sanitizer；raw invalid rate separately reported |
| 任务成功率 | ≥95% titles semantically identify first task on labeled set |
| 人工覆盖优先 | 100% late model result cannot overwrite user title |
| Prompt injection | 0 HTML/control/system-prompt/secret leakage; 0 extra actions |
| Raw reasoning | v2 raw delta + finalized reconciliation；固定pin/数据集必须提供非空具体文本；plain-text/no-execution/no-log；missing/gap/invalid/oversize为Gate FAIL，不允许状态/时长冒充；DESIGN-126-003 caps=16KiB/delta、64KiB/part、128KiB/item、256KiB/turn、8 parts/item、8 items/turn；SQLCipher lifecycle/schema与DEC-126-017已Accepted；local source fixtures PASS，业务conformance仍待G4 |
| 延迟与成本 | title 不阻塞主回答；production P95/timeout 在 G4 benchmark 冻结；≤2 calls/session；actual token/cost recorded before G4 |
| 相对基线 | deterministic fallback remains available; enabling model title cannot reduce conversation success |

## 10. Fixture 与测试数据

| Fixture/Dataset | 权威位置候选 | 数据分类 | 合成/脱敏方式 | Consumer |
|---|---|---|---|---|
| Public Tasks auth/error matrix | `yijie-contracts/tests/fixtures/public/tasks-v2/` | internal synthetic | fixed UUID users/tenants/tasks | API/Desktop；source validation PASS，runtime conformance pending |
| Agent raw/title/cleanup events | `yijie-contracts/tests/fixtures/agent/` | internal synthetic | generated safe text/canaries | Host producer、Desktop S7A Rust consumer与S7B application reducer positive/negative assertions PASS；UI/runtime process E2E pending |
| Desktop DB versions/corruption | yijie-desktop test fixtures | internal synthetic | generated temp DB, no user data | Rust repository |
| Project tree/symlink cases | runtime temp directories | internal synthetic | mktemp fixtures only | Tauri path boundary |
| Title/reasoning Eval dataset | future approved yijie-agent-host or eval authority | internal synthetic | invented prompts, versioned hash/split | AI runner |
| Desktop private IPC v1 | `yijie-desktop/src-tauri/schemas/chat-ipc-v1.schema.json` + `src-tauri/fixtures/chat-ipc-v1/` | internal synthetic | fixed opaque UUID/context/cursor和正文/secret/path canaries；无真实token/path | Rust serde/commands/events + TS validator/client/store；DEC-126-031 Accepted，S8A Closure Passed |

### 10.1 本次固定 capability fixture

| Fixture ID | 固定输入/断言 | 结果 | 能证明 | 不能证明 |
|---|---|---|---|---|
| FIX-126-TITLE-001 | existing mock Responses；`thread/start(ephemeral=true)` | PASS | thread pathless/in-memory | MiniMax、Host title op |
| FIX-126-TITLE-002 | existing mock Responses；strict object `outputSchema` | PASS | Runtime 发送 Responses `text.format` strict JSON schema | MiniMax 接受/遵循 title schema |
| FIX-126-TITLE-003 | 两个 turns，仅首 turn带 schema | PASS | `outputSchema` 是 per-turn，不污染后续 turn | title sanitizer/业务幂等 |
| FIX-126-SUMMARY-001 | configured concise summary + mock completion | PASS | Runtime request带 reasoning summary；fixed OpenAI wire 还带 sequential-cutoff hint | MiniMax 是否接受该附加字段 |
| FIX-126-SUMMARY-002 | reasoning item + public summary delta | PASS after default-stack abort/re-run | delta 正确关联 reasoning item ID | Host v2 projection、MiniMax真实事件 |
| FIX-126-RAW-UPSTREAM-001 | existing local mock Responses；`reasoning_raw_content_delta_respects_flag` | PASS | fixed Runtime按flag产生canonical raw text delta | Host v2 mapping、Desktop持久化或MiniMax稳定性 |
| FIX-126-RAW-UPSTREAM-002 | fixed `builds_multiple_turns_with_reasoning_items` history fixture | PASS | completed raw `content[]`进入正确turn/item history | Host/Desktop source contract实现 |
| FIX-126-RAW-UPSTREAM-003 | fixed `splits_reasoning_when_interleaved` fixture | PASS | interleaved reasoning形成独立items而非错误合并 | v2 caps/sequence conformance |
| FIX-126-RAW-UPSTREAM-004 | fixed `marks_turn_as_interrupted_when_aborted` fixture | PASS | aborted rollout产生interrupted turn事实 | SQLCipher explicit-incomplete实现 |
| FIX-126-RAW-001 | synthetic raw text deltas + complete/incomplete/unavailable finalized fixtures | SOURCE + HOST + DESKTOP RUST S7A/S7B PASS；Vue render NOT RUN | Host closed v2 mapping、content-index/final snapshot/caps/partial规则；Desktop strict SSE/domain、coalesced cursor、terminal reconciliation与redacted Debug | yijie-contracts + Host fake Runtime + Desktop fake Host；Vue rendering pending S8 |
| FIX-126-RAW-002 | malformed status/reason/index/oversize + closed-union assertions | SOURCE + HOST PASS | invalid/oversize转explicit unavailable；raw canary不进Host logs/bbolt | contracts negative + Host race/unit/no-log assertions；Desktop UI安全留待S7–S9 |
| FIX-126-RAW-003 | accepted SQLCipher history/delete path | S6 FOUNDATION PASS / E2E NOT RUN | terminal事务、wrong-key、secure_delete、WAL truncate、DB canary absence与FK cascade已测；live stream/restart全链路待S10 | Desktop Rust synthetic SQLCipher tests；不构成G4 evidence |
| FIX-126-IPC-001 | closed command/response/error/cursor golden与unknown-field negatives | S8A Closure Passed | 20/20 command contract refs、closed request/response/error、opaque cursor与Rust/TS fixture equality | 不证明Vue或四组件E2E；DEC-126-031 Accepted |
| FIX-126-IPC-002 | assistant/reasoning append、terminal、cleanup、resync/context-invalidated与gap/overflow序列 | S8A PASS | 7/7 event variants、UTF-8 byte caps、duplicate/gap/backpressure/resync和listen-only capability | 不证明真实Runtime多进程delivery；S10仍待授权 |
| FIX-126-IPC-003 | A→B stale、logout/revision expiry、restart、interrupt/delete/project races | S7C + S8A PASS | newest tenant bind、context invalidation、late response/event drop、restart cleanup resync、delete-vs-turn与remove-vs-send已测 | 不能替代Vue/四组件E2E；S8B/S10仍待授权 |

## 11. 实际执行与未来计划

| 层级 | Repository/CWD | Command | 环境依赖 | 预期时长 |
|---|---|---|---|---|
| source contract | yijie-contracts | `make generate && make lint && make test && make build && pnpm pack:sdk` | Node 26.0.0/pnpm 11.9.0/Go 1.26.5 | RUN 2026-08-02；PASS，27/27，SDK local only |
| breaking | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | sole supported baseline | RUN 2026-08-02；PASS + legacy wire equality PASS |
| API unit/integration | yijie-api | `make generate-check && make test && make lint`；隔离PostgreSQL上`make test-integration` | Go 1.26.5 + synthetic PostgreSQL 127.0.0.1:55432 | RUN 2026-08-02；PASS；迁移v3、creator-private/idempotency/audit集成通过，临时实例停止并清理 |
| Host | yijie-agent-host | `make contract-check && make test && make lint` | Go 1.26.5 + fake Runtime only | RUN 2026-08-02；PASS；race coverage app 67.1%、codex 71.0%、session 77.7% |
| Runtime fake title | yijie-codex/codex-rs | `cargo test -p codex-app-server --test all <exact test> -- --nocapture` for the three `FIX-126-TITLE-*` tests | pinned source；MiniMax/OpenAI keys removed；local mock only | RUN 2026-08-02；3/3 PASS |
| Runtime fake summary | yijie-codex/codex-rs | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all <exact test> -- --nocapture` for two `FIX-126-SUMMARY-*` tests | pinned source；keys removed；local mock only | RUN 2026-08-02；2/2 PASS；one default-stack SIGABRT recorded |
| Runtime fake raw delta | yijie-codex/codex-rs | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all reasoning_raw_content_delta_respects_flag -- --nocapture` | pinned source；keys removed；local mock only | RUN 2026-08-02；PASS |
| Runtime raw history/interleaving/interruption | yijie-codex/codex-rs | `cargo test -p codex-app-server-protocol protocol::thread_history::tests::<exact test>` for three `FIX-126-RAW-UPSTREAM-*` tests | pinned source；fixed fixture only；no provider | RUN 2026-08-02；3/3 PASS |
| Runtime delete fixture | yijie-agent-host/yijie-codex temp home | fixed `codex-cli 0.144.6` isolated harness recorded in `08` | pinned binary；no provider key | RUN 2026-08-02；functional PASS/residue FOUND |
| MiniMax `MM-126-001` title | isolated narrow harness | exactly 1 synthetic title request；pathless ephemeral、strict schema、≤120s | pinned Runtime/Host candidate + owner-only test key | PASS；1 call/0 retry，1,853 ms，strict object + 18-grapheme sanitizer，0 tool/secret leak，temp removed |
| MiniMax `MM-126-002` public summary | isolated narrow harness | exactly 1 synthetic 57-char reasoning request；high+concise、answer≤80 chars、≤120s | same pin/key；title call did not donate retries | FAIL；1 call/0 retry，9,256 ms，answer completed但0 public-summary event；7 raw delta + 1 raw completed part，0 tool/secret leak，temp removed |
| Desktop | yijie-desktop | `make lint && make test && make build` | Node 26.0.0 / pnpm 11.9.0 / Rust 1.95.0；bundled SQLCipher；fake Host | RUN 2026-08-03；PASS；21/21 files、127 TS tests；94 Rust tests（93 pass、1个既有signed Keychain integration ignored）；Clippy/fmt/Vite build PASS；含S7C既有链及S8A schema/serde/TS、auth、event caps/backpressure/cancel、stale selection、tenant/logout、restart/resync/delete cleanup和no-log扫描 |
| Meta docs | yijie | feature checker, YAML parse, `git diff --check` | local shell/Ruby | current package only |
| Local four-component E2E/security/perf/eval | affected repos | exact orchestration and commands must be added by authorized slices before G4 | local PostgreSQL/temp homes/DB/pinned Runtime/fake provider | command/harness absent — blocks G4/local G6；does not affect accepted G2/G2A |

## 12. 通过、失败与 Flaky 策略

- PASS：command completes with expected exit code and assertions; exact SHA/tool/env/evidence recorded。
- FAIL：any blocking assertion or unexpected diff；不得降低断言/关闭门禁。
- NOT RUN：environment/approval/command absent、skipped、output truncated or process incomplete。
- Flaky：quarantine is not acceptance；identify nondeterminism and fix before Gate。
- Snapshot/golden：Design/Product Owner reviews semantic diff in all themes/min viewport；pixel update alone不构成通过。
- Paid/real model：only explicit bounded run；never “rerun until green”；record provider/model/config/call count without key/content。

### 12.1 MiniMax 两次调用的停止/判定规则

- 历史hard cap=2：`MM-126-001` 与 `MM-126-002` 各一次，已经耗尽；二者不得重跑，也不能把本地开发请求伪装成其retry。
- DEC-126-022只允许在完整本地链路后**提交**一次新bounded local smoke审批候选（建议ID `MM-126-003`）；当前未批准、预算为0。只有Owner另行确认exact请求数、数据、key边界和停止条件后才可执行。
- 只用临时 app-data/CODEX_HOME/空 cwd、合成文本、read-only/never、无 project/真实用户数据；完成
  后清理临时目录。key 只进入 intended provider child，输出与证据不得包含 key/完整 request/response。
- Title：valid strict object + sanitizer 1–40 grapheme + terminal + no tool/path/rollout 为 PASS；协议接受但
  refusal/incomplete/invalid 为 DEGRADED/FAIL 并采用 fallback；auth/429/5xx/timeout 记录原结果不重跑。
- Historical summary gate：MM-126-002仍按当时规则为FAIL，不因ADR-0016事后改写。新raw gate要求非空raw、
  sequence/completion一致、纯文本/no-log；缺失或无效为FAIL，不允许时长-only。两次provider预算已耗尽。
- 每次记录 exact Runtime/Host full SHA、model/provider、开始结束时间、latency、HTTP/RPC terminal、usage/
  cost（响应存在时）、脱敏断言与临时目录清理结果。未批准 Host candidate 时只可用隔离 harness，不得
  先修改业务代码“为了验证”。

## 13. 测试计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 测试/技术 Owner | 段成威 | S4–S8A已由DEC-126-026/027/028/030/031接受；S8B、S9–S11/UI/MiniMax与完整E2E仍禁止 | 2026-08-03 |
| 安全/数据 Owner | 段成威 | 当前P1及Public Tasks正文边界阻断closure；既有auth/delete/no-log/migration结果仅作foundation evidence | 2026-08-02 |
| Runtime/模型 Owner | 段成威 | DEC-126-021 HOLD与DEC-126-022 Local-only已Accepted；先用fake provider/fixtures，raw reasoning须具体显示并持久化/删除；历史MM-126-001/002不重跑，未来一次local smoke仅可另行提交审批 | 2026-08-02 |
