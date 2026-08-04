# FEAT-126 测试与 Eval 计划

> 本文定义什么证据可以证明FEAT-126达到DEC-126-022的Local Runtime Ready。DEC-126-023/024完成G2A重审，DEC-126-025登记sole candidate与checkpoint远端ref并恢复LIA-126-002，仅执行S4–S6 Corrective Closure。
> DEC-126-026/027/028/030/031/033/034已关闭S4–S8B；DEC-126-035已接受远端事实，DEC-126-036已接受LIA-126-007 / S9 Closure。DESIGN-126-007/DEC-126-037方案C、DESIGN-126-008/DEC-126-038方案B、S10E/DEC-126-039及S10P1/DEC-126-040均已接受并继续HOLD S10B；BLK-001/002/003已关闭。DEC-126-041历史决定继续Accepted，S10P2 Closure HOLD与BLK-004 Open不变。DEC-126-042现仅是Local-only调整候选：如未来被Owner安全/G2接受，可在另行授权的S10P2F中用double-exact、run-scoped ephemeral file backend证明本地合成secret生命周期，Apple signed Keychain则转为Deferred Native Hardening。本轮不安装Xcode、不访问Keychain、不执行S10P2F/P3/B/S11，不调用MiniMax，
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
| AC-048 | exact-off UI gate | UI-GATE-001–010 | config/router/bundle | missing/empty/TRUE/1/false/true truth table、nav/route/deep-link/loader | production build + memory router | only exact true registers surfaces；default bundle no Chat component instantiation |
| AC-049 | dynamic route与permission lifecycle | UI-AUTH-001–012 | router/store/race | `/chat/:id` read guard、deleted/foreign/denied/stale、tenant/revision/logout/expiry | production Pinia + fake client harness | no exact-path bypass、old scope flash or late commit |
| AC-050 | project/session/cleanup store consumption | UI-STORE-001–012 | Pinia integration | pick/revalidate、append paging/cursor invalid、cleanup complete/incomplete/navigation | real reducer + fixed fake ChatClient injection | dedupe/order/clear/reload/closed disposition；Vue never calls client |
| AC-051 | readiness/storage closed projection | IPC-READY-001–016 | schema/Rust/TS/fault | Host/Runtime states、nonce/version、start retry、read-only/full/corrupt/migration、check/use race | fixed serde/TS fixtures + fake Host/temp SQLCipher | schema equality、Rust-owned start、stable issue/recovery、no sensitive detail |
| AC-052 | production path真实性 | BUNDLE-001–006、UI-REAL-001–006 | bundle/component | fake transport imports、`sampleTasks` imports、production component/store mounting | Vite production build + dependency graph | fake only test harness；sample absent from production task route；0 production dependency addition |

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
| Dataset | `feat126-title-raw-v1`：200 synthetic multilingual normal + 50 injection/adversarial；train=200/holdout=50 |
| Model/provider | deterministic fake provider；固定Runtime/Host基线；MiniMax/外部provider调用=0 |
| Title prompt/schema | `title-v1` + strict `{title:string}`；first user input≤8KiB；post-parse NFC plain single-line title 1–40 grapheme |
| Runner | Host唯一权威Go test runner；摘要锁覆盖manifest/schema/dataset/split/runner/generator/fixtures；no real user data |
| 结构通过率 | PASS 250/250；unsafe title拒绝50/50 |
| 任务成功率 | PASS 200/200（100%，阈值≥95%） |
| 人工覆盖优先 | PASS；late model覆盖用户title=0 |
| Prompt injection | PASS；HTML/control/system-prompt/secret leakage=0；extra action=0 |
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
| Title/reasoning Eval dataset | `yijie-agent-host/internal/session/testdata/feat126-title-raw-v1/` | internal synthetic | 250 invented prompts，versioned SHA-256 lock与固定split | Host唯一runner；Desktop消费exact SSE/consumer fixtures |
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
| FIX-126-RAW-001 | synthetic raw text deltas + complete/incomplete/unavailable finalized fixtures | SOURCE + HOST + DESKTOP RUST + VUE S8B PASS | Host closed v2 mapping、content-index/final snapshot/caps/partial规则；Desktop strict SSE/domain、coalesced cursor、terminal reconciliation、redacted Debug与Vue纯文本展开/折叠渲染 | 不构成四组件E2E；S10A已评审，S10B仍未授权 |
| FIX-126-RAW-002 | malformed status/reason/index/oversize + closed-union assertions | SOURCE + HOST + DESKTOP UI SAFETY PASS | invalid/oversize转explicit unavailable；raw canary不进Host logs/bbolt；Vue不使用`v-html`且只消费容量受限projection | contracts negative + Host race/unit/no-log + S8B production-component assertions；S9 Eval与S10 E2E仍待授权 |
| FIX-126-RAW-003 | accepted SQLCipher history/delete path | S6 FOUNDATION PASS / E2E NOT RUN | terminal事务、wrong-key、secure_delete、WAL truncate、DB canary absence与FK cascade已测；live stream/restart全链路待S10 | Desktop Rust synthetic SQLCipher tests；不构成G4 evidence |
| FIX-126-IPC-001 | closed command/response/error/cursor golden与unknown-field negatives | S8A Closure Passed | 20/20 command contract refs、closed request/response/error、opaque cursor与Rust/TS fixture equality | 不证明Vue或四组件E2E；DEC-126-031 Accepted |
| FIX-126-IPC-002 | assistant/reasoning append、terminal、cleanup、resync/context-invalidated与gap/overflow序列 | S8A PASS | 7/7 event variants、UTF-8 byte caps、duplicate/gap/backpressure/resync和listen-only capability | 不证明真实Runtime多进程delivery；S10仍待授权 |
| FIX-126-IPC-003 | A→B stale、logout/revision expiry、restart、interrupt/delete/project races | S7C + S8A PASS | newest tenant bind、context invalidation、late response/event drop、restart cleanup resync、delete-vs-turn与remove-vs-send已测 | 不能替代Vue/四组件E2E；S8B/S10仍待授权 |

### 10.2 DESIGN-126-006 S8B0/S8B fixtures（S8B0 PASS / S8B本地候选PASS）

| Fixture/Test set | 内容 | Production rule | 当前状态 |
|---|---|---|---|
| `FIX-126-UI-GATE-001` | six-value env truth table、nav/routes/lazy loader spy | only exact true；no default env/CI/build activation | S8B0 PASS / DEC-126-033 Accepted |
| `FIX-126-UI-AUTH-001` | create/read route meta、deleted/foreign/denied/stale、tenant/revision/logout sequencing | Rust action/resource check remains authoritative | S8B0 PASS / DEC-126-033 Accepted |
| `FIX-126-UI-STORE-001` | pick/revalidate、session append paging、cursor invalid、cleanup complete/incomplete disposition | use production Pinia reducer；fake client only dependency injection in tests | S8B0 PASS / DEC-126-033 Accepted |
| `FIX-126-IPC-READY-001` | two new command request/response golden、unknown fields/enums、auth/expiry/operation retry | schema↔Rust serde↔TS validator exact；20个旧命令与7个events语义不漂移，总命令22 | PASS under LIA-126-005 |
| `FIX-126-UI-A11Y-001` | light/dark、1180×760、200% zoom、reduced-motion、keyboard、IME、focus/menu/dialog、48/160 scroll、reasoning、axe/snapshot/VoiceOver | production components + real Pinia reducer；test-only harness；`axe-core@4.10.3` fixed devDependency with audit/lock evidence | S8B automated/browser portions PASS；VoiceOver checklist only，人工未执行 |

## 11. 实际执行与未来计划

| 层级 | Repository/CWD | Command | 环境依赖 | 预期时长 |
|---|---|---|---|---|
| source contract | yijie-contracts | `make generate && make lint && make test && make build && pnpm pack:sdk` | Node 26.0.0/pnpm 11.9.0/Go 1.26.5 | RUN 2026-08-02；PASS，27/27，SDK local only |
| breaking | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | sole supported baseline | RUN 2026-08-02；PASS + legacy wire equality PASS |
| API unit/integration | yijie-api | `make generate-check && make test && make lint`；隔离PostgreSQL上`make migrate-up/status && make test-integration` | Go 1.26.5 + synthetic PostgreSQL 127.0.0.1:55432 | RE-RUN 2026-08-03；PASS；migration 1–4与race integration通过，临时实例停止并清理；并行fixture的information_schema断言已限定`current_schema()` |
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
| Accepted checkpoints / remote reconciliation | yijie/API/Host/Desktop/contracts | repository gates + scope/no-log/diff + owner-authorized candidate push；`git ls-remote` + exact-branch temporary clean clone | synthetic/fake/temp only；remote verification is read-only | RUN 2026-08-03；PASS；remote exact `650254b…139fa`、`a64f9f5…3264`、`3e8df02…f3d9`、`35f2744…7cbd`、`29317b6…e9f`；all clean clones，develop/Draft PR/merge/tag/publish/deploy未改变；DEC-126-035 Accepted |
| S8B0/S8B conformance | yijie + yijie-desktop | DESIGN-126-006/DEC-126-032 + schema/Rust/TS/router/store/Tasks + production Vue/unit/axe/browser/security/bundle/package/strict/G2A/YAML/lint/test/build/diff | fake/fixed/temp only；no runtime provider | DEC-126-033/034 Accepted；S8B Closure Passed at `35f2744…7cbd`；VoiceOver人工项保留到S11/G6 |
| S10A readiness/test-profile review | yijie governance + affected repos read-only | exact SHA/worktree/tool/port/source inventory；DESIGN-126-007/DEC-126-037/LIA-126-008 draft | no component startup/provider/flag/Keychain write | COMPLETE / DEC-126-037 ACCEPTED OPTION C；HOLD；5 blockers recorded；not E2E |
| Local four-component E2E/security/perf/eval | affected repos | exact orchestration in DESIGN-126-007; only after all blockers close and LIA-126-008 becomes approvable | local PostgreSQL/temp homes/DB/pinned Runtime/fake provider | S10B NOT RUN — blocks G4/local G6；does not affect accepted G2/G2A/S4–S9 |
| LIA-126-007 / S9 fake-provider Eval | Host authority + Desktop consumer | versioned runner、exact dataset hash/split、title schema/semantic与raw sequence/final/no-log/injection gates | fixed fake provider、fixed pins、synthetic data only | RUN 2026-08-04 / PASS；DEC-126-036 Accepted；不调用MiniMax、不启用flag、不进入S10 |

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
| 测试/技术 Owner | 段成威 | DEC-126-036–041已Accepted并HOLD LIA-126-008；DEC-126-042仅为待接受的设计候选，不授权S10P2F/P3/B/S11/MiniMax/flag activation或完整E2E | 2026-08-04 |
| 安全/数据 Owner | 段成威 | 当前DEC-126-041下BLK-004/005仍阻断S10B；如未来接受DEC-126-042，BLK-004须由另行授权的S10P2F完整ephemeral lifecycle/no-log/cleanup矩阵关闭，signed Keychain只能登记为Deferred Native Hardening，不得写成PASS或等价代替 | 2026-08-04 |
| Runtime/模型 Owner | 段成威 | DEC-126-021 HOLD与DEC-126-022 Local-only已Accepted；先用fake provider/fixtures，raw reasoning须具体显示并持久化/删除；历史MM-126-001/002不重跑，未来一次local smoke仅可另行提交审批 | 2026-08-02 |

## 14. LIA-126-006 实际结果

| 层级 | 命令/证据 | 结果 |
|---|---|---|
| Vue/TS unit + store integration | `pnpm test` | PASS：29 files / 164 tests；覆盖composer/IME/reasoning/stream/48/160/menu/delete/cleanup/deep-link/stale/restart稳定投影 |
| Type/lint | `pnpm lint` | PASS：ESLint 0 warnings + `vue-tsc --noEmit` |
| Production build | `pnpm build` | PASS：4625 modules；test harness和axe不在bundle |
| axe | production `ChatPage` + real Pinia，`axe-core@4.10.3` | PASS：0 serious/critical；happy-dom不承担color contrast布局判断 |
| Rust regression | `cargo test --manifest-path src-tauri/Cargo.toml` | PASS：95 passed / 0 failed / 1既有isolated Keychain ignored；首轮sandbox OS-denial不计产品失败，unchanged suite在允许loopback/temp权限环境全绿 |
| Dependency audit | `pnpm audit --audit-level high` | PASS：No known vulnerabilities；axe为exact devDependency，production dependency 0新增 |
| Browser visual/a11y | test-only harness；1180×760 light/dark、590×380 200%-equivalent、dialogs/focus | PASS：无横向overflow，主要操作纵向可达，permission/delete触发器focus恢复，正文/reasoning无HTML children |
| Security/boundary | `git diff --check` + source/bundle/no-log/path/secret/flag scans | PASS：无direct client/invoke/v-html、无enabled flag、无secret/path/raw-wire/test artifact production leak |

VoiceOver：仅完成并提交人工清单，未声称由真人执行；DEC-126-034将其接受为保留到S11/G6的人工项。完整fake-provider Eval、四组件E2E和Owner local G6分别保留在S9/S10/S11，不能用本节结果替代。

## 15. LIA-126-007 实际结果

| Gate | 结果 |
|---|---|
| Dataset/split | PASS：250 cases；normal=200、adversarial=50、train=200、holdout=50；schema与SHA lock自校验 |
| Title | PASS：schema/sanitizer 250/250；semantic 200/200；unsafe rejected 50/50；late overwrite/leak/extra action=0 |
| Raw | PASS：valid 210/210；negative 40/40（gap/invalid/missing/oversize各10）；delta/final exact |
| Host security | PASS：raw body进入log/bbolt=0；contract-check、race/coverage、lint/vet、build、diff均通过 |
| Desktop lifecycle | PASS：exact fixture hash、production SSE decoder、authoritative reducer、terminal SQLCipher、restart/history、user-title priority、cascade delete |
| Desktop UI/security | PASS：production Vue组件literal plaintext；script/link=0；fixture/canary不进入production bundle；TS/Rust全量门禁通过 |
| Flaky分类 | 首次Rust full run有1个既有cleanup test使用stale `now`的跨秒波动；该文件不在S9 diff，单测与第二次full run均PASS；不豁免、不改production源码 |

DEC-126-036已接受；S10A只读评审不等于四组件E2E，S10B仍须关闭blocker并另行明确授权。

## 16. DESIGN-126-007 / S10A Readiness Review 结果

### 16.1 只读环境结果

| Check | Result | 判定 |
|---|---|---|
| 六仓分支/SHA/worktree | 全部与Owner固定值精确相等，clean | PASS |
| Runtime artifact | version 0.144.6；binary/manifest SHA-256与manifest一致 | PASS（未启动app-server） |
| Docker/Compose | Docker 29.6.1；用户plugin symlink已可恢复地修复到固定bundled Compose v5.3.0；S10E profile/static/runtime/migration/TLS/cleanup验证PASS | `S10E CLOSURE PASSED / BLK-001 CLOSED` |
| 当前服务 | 5432/6379/8080/18080/1420未观察到listener | no existing isolated stack |
| fake provider process profile | S10A时不可表达；LIA-126-009现已实现exact-master/fixed-loopback/keyless Responses profile并通过固定Runtime turn | `CLOSED BY DEC-126-040` |
| Desktop child flags/logs | S10A时不可表达；LIA-126-009现已实现closed allowlist、raw/cleanup=true、title=false、bounded owner-only logs和PID/run/nonce evidence | `CLOSED BY DEC-126-040` |
| secure local storage isolation | Chat/native-auth Keychain namespaces fixed | `SECURE_STORAGE_NOT_ISOLATED` |
| Public Tasks main-chain consumer | Desktop无`/v2/tasks` production call | `CHAIN_NOT_CONNECTED` |

### 16.2 冻结E2E矩阵

S10B必须以`S10B-001–012`作为同一run的不可分割矩阵：provenance/startup；项目选择与content-free task create；assistant/raw valid与incomplete对账；SQLCipher分页/restart；fallback title/user rename/pin/sort；interrupt/gap/reconnect/resync；Desktop/Host/Runtime物理删除与receipt；Public Tasks/PostgreSQL正文零命中；log/bbolt/audit/telemetry/URL/process-output泄漏零命中；performance/capacity/fault；最终无PID/listener且default-off。详细输入类别、证据与失败分类见`05 §17.6`。

### 16.3 证据规则

- process manifest必须含role/PID/PPID/binary SHA/port/nonce-ready摘要/start-end/exit/cleanup，不含argv secret或env value。
- case证据只含baseline ID、fixture hash、计数、枚举、布尔断言、耗时和失败分类。不保存prompt/assistant/raw/title、bearer/DSN/key或真实路径。
- 安全扫描只保存scanner version、pattern SHA-256和hit count；任一非预期命中为Gate FAIL。
- 任一用例使用mock Vue、单仓fixture、手工数据库状态或独立API curl替代真实主链，整个S10B不得声称PASS。

### 16.4 LIA-126-008 / S10B 单独授权建议（Blocked Draft）

**当前推荐：不批准执行。** 下列前置须全部关闭并回填新checkpoint与逐仓门禁：

1. DEC-126-039已接受S10E Closure并关闭BLK-001；
2. Host受审查的test-only loopback fake Responses已由LIA-126-009实现并验证，DEC-126-040已正式关闭BLK-002；
3. Desktop sidecar child allowlist、raw/cleanup exact-true、content-free log/PID evidence已实现并验证，DEC-126-040已正式关闭BLK-003；
4. Desktop Chat/native-auth使用test-only Keychain namespace与isolated app-data，不触碰真实条目；
5. 真实Desktop create action有content-free `/v2/tasks`编排，并与同一local session/Host operation可追踪，无正文上传。

DEC-126-037已接受`HOLD`。前置关闭前，LIA-126-008状态保持`Blocked Draft / NOT AUTHORIZED`；G3 Partial、G4/G6 Pending。

## 17. DESIGN-126-008 / S10P0 corrective 测试冻结

S10P0本身只运行了只读环境/源码检查与治理门禁。DEC-126-038已接受；S10E随后完成并获DEC-126-039接受，S10P1随后按LIA-126-009完成并获DEC-126-040接受。下表继续作为S10P2/P3及最终S10B的冻结门禁：

| Slice | 正常路径 | 安全/负向 | migration/restart/race | 退出Gate |
|---|---|---|---|---|
| S10E | bundled Compose v5.3.0 version/hash/config；四个digest-pinned services ready；empty API DB migration；synthetic OIDC/TLS/CA | stale/foreign symlink、mutable tag、旧volume/DB reuse、非loopback port、镜像缺失 | 重复profile prepare/status/stop；run project/volume清单不串run | plugin可恢复；无真实DB/Keychain；无未列入manifest的删除 |
| S10P1 | fake `/v1/responses`→fixed Runtime→Host raw/cleanup；nonce/PID/log | master false/typo、nonloopback URL、userinfo/query/redirect/proxy、fake+MiniMax key同存、oversize/unknown fixture | Host/Desktop/fake任意崩溃与重启；child effective env与default-off scan | external call=0；title=false；body/secret/path log hit=0；不改IPC/Runtime pin |
| S10P2 | 三个run-derived Keychain item创建/使用/删除；app-data/Host/CODEX home同run | 不枚举Keychain；legacy account不fallback；foreign/malformed run ID、symlink/root mode错 | Desktop崩溃、cleanup中断、missing item、同run恢复、异run并发 | pre absent/post absent；真实namespace access/delete=0；manifest mismatch不删 |
| S10P3 | local session transaction→content-free create→bind public ID→Host start→turn；closed UI projection | 400/401/403/409/500/503、response tenant/creator/reference mismatch、body/path/title canary，cross-scope ID | v1–v4→v5、重复启动、inflight/unknown/late 201、logout/tenant/revision、create-vs-delete/Host-start | schema/serde/TS/golden全绿；同op无重复Public/Host；PostgreSQL/audit正文=0；retained Public row仅closed fields |

S10P3 private IPC conformance必须锁定`chat_get_session_control_plane_v1`和`yijie.chat.control-plane.event.v1`的closed corpus；Rust、JSON Schema、TypeScript validator、client、Pinia reducer和页面稳定投影必须在同一checkpoint中通过。未知field/state/error、sequence gap、duplicate、stale selection/context必须fail closed/resync，Vue不得收到Public task/client reference/operation/owner/tenant/Host ID或raw HTTP body。

Public Tasks删除验收要同时证明两件事：（1）Desktop/Host/Runtime和本地binding已按DEC-126-006清理；（2）由于`29317b...`无delete operation，PostgreSQL的Public Task row仍存在且仅包含closed content-free fields。DEC-126-038已接受第（2）项边界；不得把它隐藏为“全表面物理删除”，未来若改变该要求必须重开G2A。

## 18. S10E实际测试结果（DEC-126-039 Accepted）

| Gate | 方法 | 结果 |
|---|---|---|
| Compose discovery | v5.3.0 version、binary size/SHA-256、config no-interpolate/quiet、profiles/services、`up --wait` capability | PASS；旧link有owner-only可恢复备份 |
| Static/profile | Infra `pnpm validate`、Node tests、`bash -n`、`git diff --check` | PASS；80/80 tests；default-off、exact images、loopback ports、closed labels/volumes/networks |
| Image/source | exact local digest inspect；`up --pull never`；Infra/API fixed SHA与clean worktree | PASS；download/pull=0；central contracts/Runtime/业务源码变化=0 |
| Runtime topology | content-free runtime verifier检查4 containers、health、image、run labels、no-privileged/no-host-network/no-docker-socket、4 networks/4 volumes及published ports | PASS |
| Identity/TLS | public CA file mode/single-cert/no-private-key；OIDC discovery issuer；两次synthetic user provisioning；Tasks denial | PASS；issuer exact；provision 2+2 idempotent；Tasks HTTP 404 |
| API migration | API `a64f9f…3264` migration against dedicated empty DB；立即重复 | PASS；00001–00004→v4；second run no-op |
| no-log/no-source-secret | fresh run generated values精确扫描container logs；两次run secret扫描candidate tracked/untracked files | PASS；hit=0 |
| contaminated-run handling | 初始diagnostic run因process output展开synthetic DB credential被整轮拒绝；fresh run重建证据；旧run写入owner-only `REJECTED` marker | PASS；污染值未进入source/Git/docs，不计入接受证据；config/provision/migration/verify均fail closed |
| stop/cleanup | 两个exact project停止；container/network/listener inventory；禁止volume delete/prune | PASS；active=0；八个named volumes和两个owner-only ignored run root按未授权删除边界保留 |

本表只证明S10E环境切片，不证明Host fake provider、Desktop child profile/Keychain/Public Tasks主链或四组件E2E。DEC-126-039不授权S10P1；S10B继续HOLD。

## 19. S10P1实际测试结果（DEC-126-040 Accepted）

| Gate | 方法 | 结果 |
|---|---|---|
| Host closed config | exact master/run UUID/fixed loopback/local/raw+cleanup/title=false；nonloopback、错port/path/query、missing/expired run、MiniMax key共存、父PID/log目录/manifest校验 | PASS；全部负向fail closed；默认MiniMax回归PASS |
| fake Responses protocol | frozen fixture SHA校验；bounded request/model/input/call cap；complete/incomplete/http-error/disconnect/oversize | PASS；request正文不反射；content-free counters only |
| fixed Runtime turn | Host manager→fixed Runtime artifact→`127.0.0.1:18082/v1`；assistant/raw delta/final、completed和thread delete | PASS；1 accepted/0 rejected；外部模型调用0 |
| Host repository | `make lint`、`make contract-check`、`make test`、`go build`、`git diff --check` | PASS；app 68.7%、codex 71.0%、fake 79.8%、security 71.7%、session 77.6% coverage；race PASS |
| Desktop closed child profile | `env_clear` allowlist、exact profile、run root ownership/mode、raw/cleanup/title、PID/run/nonce readiness、wrong nonce/port/crash/restart/stale evidence | PASS；非法/过期/冲突全部fail closed |
| child logs/evidence | directory 0700、files 0600、每stream 256 KiB cap、truncation、content-free process JSON、unique atomic temp | PASS；正常stop、spawn/crash/timeout/restart均稳定 |
| real child startup | production supervisor code→临时Host binary→fixed Runtime；Host health/ready nonce，stop/manifest | PASS；`RuntimeReady`后正常stop；未启动fake turn，故不是S10B或四组件E2E |
| Desktop repository | generated contract check、lint/type/fmt/clippy、`make test`、Vite build、Rust build、`git diff --check` | PASS；TS 30 files/165 tests；Rust 101 pass/0 fail/1既有Keychain ignored |
| security/no-log | synthetic raw、secret/key names、temporary paths、bearer/DB-key patterns扫Host session tests、bbolt、child stdout/stderr、process evidence和process output | PASS；hit=0；Keychain access=0；真实数据=0 |
| scope/default-off | diff检查`.env`/CI/build config、IPC/TS/Vue/contracts/wire/schema/Runtime pin | PASS；仅Host private fake transport/fixtures/tests及Desktop Rust child profile；默认flags未启用 |

结论：Owner已按DEC-126-040方案A接受S10P1 Closure并关闭BLK-002/003。该结论不覆盖BLK-004/005，不授权S10P2/P3/S10B/S11，也不构成G4/G6证据。

## 20. S10P2实际测试结果（DEC-126-041 Option B Accepted / Closure HOLD）

| Gate | 方法 | 结果 |
|---|---|---|
| source/default-off | 双exact gate truth table；default namespace常量回归；diff扫描`.env`/CI/build defaults | PASS；master-only、缺失、false不启用S10P2；typo/orphan fail closed |
| namespace/legacy | canonical UUID派生三service；native-auth test store不构建legacy entry | PASS；三service互异且含run ID；legacy account access/update/delete代码路径=0 |
| run binding | app-data、Chat SQLCipher、Host Home、CODEX_HOME、project、manifest固定role | PASS；wrong home/project、non-temp root、symlink、mode错误拒绝 |
| inventory/evidence | fake exact backend + macOS exact attribute search | PASS；只查3组tuple；evidence只含role/state/schema-valid与descriptor/status SHA；secret/path/service正文=0 |
| recovery/race | pre-present拒绝、stale PID恢复、same-run retry、cross-run disjoint、cleanup interruption/missing/mismatch | PASS；mismatch delete=0；中断后phase持久化并可重试；只删validated root |
| Desktop repository | `make lint/test/build`、`cargo build --all-targets`、full Rust outside sandbox | PASS；165/165 TS；113/113 Rust，另2个signed Keychain probes ignored；fmt/clippy/build/generated-contract PASS |
| dependency/security | offline RustSec、online pnpm audit、source/bundle/no-log/diff扫描 | RustSec 0 unallowed vulnerabilities/17 allowed warnings；production依赖/lockfile本轮0变更；pnpm报告既有dev-tool `brace-expansion 5.0.8` high，需独立依赖修复；新Rust路径无日志sink，frontend bundle无gate/namespace |
| native Protected Data | 随机run三tuple、沙箱外显式ignored probe；结束后exact inventory与root清理 | **BLOCKED**：pre/post全absent、cleanup PASS；首次写返回required entitlement missing；本机0 signing identities |

判定：DEC-126-041已接受Option B和仓内实现，但`create/use/restart/delete`真实Protected Data生命周期未完成，故S10A-BLK-004不能关闭，S10P2 Closure保持HOLD。批准后的准备盘点确认bundle=`com.yijie.ai`、有效codesigning identity=0、installed provisioning profile=0、仓库entitlements/profile=0；没有新增Keychain write attempt。退出条件仍是提供匹配bundle/team/access-group的Apple Development identity/provisioning，在不改业务源码/namespace的情况下完成三条合成item的write/load/restart/delete，并证明post absent、default/legacy/foreign访问与删除均0。此前不得进入S10P3或S10B。

## 21. DEC-126-042 / S10P2F 测试候选（DESIGN ONLY）

DEC-126-042未被Owner接受，S10P2F也未授权。下表只冻结未来实施必须通过的证据；本轮不创建secret文件、不读写Keychain、不启动Desktop/Host/Runtime。

| Test ID | 场景 | PASS条件 |
|---|---|---|
| S10P2F-001 | master与ephemeral独立flag的missing/empty/false/TRUE/1/true真值表 | 只有两者均exact `true`且run UUID/root合法才可进入file backend；其它组合不得创建/读取文件，production/default仍是Protected Data Keychain |
| S10P2F-002 | 首次三role生成 | Chat SQLCipher、receipt HMAC、native-auth均由OS CSPRNG生成，三者不相等、非固定值、非run-ID/seed/env派生；evidence不包含secret/hash |
| S10P2F-003 | owner-only创建 | root/secret dir=`0700`，file=`0600`；`create_new/O_EXCL`与`O_NOFOLLOW`生效，owner、regular file、`nlink == 1`、canonical parent和schema/length均通过 |
| S10P2F-004 | symlink/hardlink/wrong owner/mode/path/partial file/role duplicate | 全部fail closed；不读、不替换、不删除，不静默重生secret |
| S10P2F-005 | 同run Desktop重启 | SQLCipher历史、receipt校验和合成native-auth均使用原三secret恢复；manifest/owner/schema漂移时fail closed |
| S10P2F-006 | cross-run与并发run | run A/B无法解析、读取、覆盖或删除对方文件；活跃PID/session lease冲突时拒绝 |
| S10P2F-007 | crash、部分创建、cleanup中断、同run重试 | phase可恢复；partial状态不进入业务链；missing item幂等成功，不发生跨run删除 |
| S10P2F-008 | 精确cleanup | Desktop→Host/Runtime→SQLCipher句柄按序停止后，只unlink manifest的三个exact files；post inventory全absent，verified empty root才可移除，未知文件不递归删除 |
| S10P2F-009 | no-log/no-output/no-WebView | secret及其全文在logs、process output、evidence、Git、bundle和WebView命中均0；真实路径不进治理证据 |
| S10P2F-010 | production/default回归 | 独立flag未设时Desktop当前行为逐字节/逐分支不变；`.env`/CI/build default不设`true`；不产生file-backend artifact |
| S10P2F-011 | Docker/宿主边界 | PostgreSQL/Keycloak/Caddy/API可使用隔离Docker profile；Desktop/Host/Runtime仍在宿主机；不把macOS Keychain或Desktop伪装成container service |
| S10P2F-012 | signed native状态披露 | Apple signed Protected Data标记`Deferred Native Hardening / NOT RUN`，不写成PASS、waived或与file backend等价，并在production/signing activation前重新成为强制门禁 |

候选Local-only BLK-004只能在DEC-126-042 Accepted、S10P2F被单独授权、上述12项及Desktop全量lint/test/build/security/diff全部PASS并获Owner Closure接受后关闭。任一失败或需改private IPC/TS/Vue/SQLCipher业务schema/central contracts/Host/API/Runtime，必须停止并重开安全/G2评审。
