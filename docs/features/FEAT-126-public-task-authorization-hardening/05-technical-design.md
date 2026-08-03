# FEAT-126 技术设计（S4–S8A Closure通过，S8B0 Closure候选，G3 Partial）

> 本文产品/架构设计保持G2 Passed。`29317b6426578749dc698fc2ad32b986ee5c8e9f`为唯一source-contract candidate。DEC-126-026/027/028/030/031已接受S4–S8A Closure；DESIGN-126-006/DEC-126-032已接受，LIA-126-005只授权的S8B0已形成仅本地Closure候选。G3仍Partial；DEC-126-033尚待Owner，S8B及S9–S11、完整Vue UI、MiniMax、flag activation与新增远端/发布动作仍未授权。

## 1. 设计摘要

- 问题：把 FEAT-124 的本地 textarea 变为安全、durable、纯文本的本地对话，并关闭 FEAT-125 留下的 Public Tasks 授权债务。
- 候选方案：两个受同一本地完成门禁管理的轨道。
  - 产品轨：ADR-0013 Accepted 的 Desktop Rust-owned embedded SQLite repository + native project reference + owner-only Agent Host HTTP/SSE + pinned Runtime/MiniMax。
  - 安全轨：Public Tasks versioned/expand auth/tenant/resource hardening；不存 conversation message body，未完成前 legacy routes 继续双隔离。
- 关键约束：raw reasoning只作为不可信纯文本投影；正文不进入 yijie-api/Host bbolt/log/telemetry/audit；token/path不暴露给WebView；标题生成不污染user thread；物理删除必须可证明。
- 明确不做：文件/图片/工具/云同步/模型选择/真实可写审批/生产激活。

### 1.1 Local-only Operating Profile

- 目标：在Owner本机启动`yijie-api`、`yijie-agent-host`、`yijie-desktop`与固定`yijie-codex` Runtime，使用本地合成身份/租户和fake provider完成完整E2E。
- 契约：`29317b6426578749dc698fc2ad32b986ee5c8e9f`是唯一source-contract candidate并已远端可达；`c000a0245acb5c3f7ead5d2a877fb60c281c588c`仅保留为immutable历史remote candidate。已恢复的LIA-126-002要求S4–S6只消费该完整SHA或其已核验投影；远端branch仅提供可达性，不能替代不可变SHA身份。
- 分发：`contracts-v0.3.0` tag、SDK/package publish和registry均N/A；本地生成物或已核验tarball不等于已发布制品。
- 生产：线上部署、生产灰度/启用、云数据库和真实用户数据均N/A；G5不适用，Local-only G6不代表Production Ready。
- 模型：实现/回归先用fake provider和固定fixtures；本文档调整不调用MiniMax，完整本地链路后的一次bounded smoke需Owner另行批准。

## 2. 组件职责与依赖方向

| Component/Repository | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| Vue Chat UI / Desktop | 状态渲染、可访问交互、selection token | typed store state/user intent | narrow commands | SQL、token、任意 path、授权决定 |
| Tauri Chat Commands / Desktop | identity scope binding、validation、transaction/outbox/project bookmark | opaque IDs/text/user intent | typed domain result/error | provider raw API、公共授权 authority |
| LocalConversationRepository / Desktop | schema migration、metadata/history、cursor/outbox、physical cascade | scoped domain commands | durable records | Runtime thread authority、cloud sync |
| Native ProjectRepository / Desktop | native picker、canonicalize/bookmark/revalidate | user-selected directory | opaque project ID + safe display | 上传/删除项目文件 |
| SidecarSupervisor + HostBridge / Desktop Rust | package/start/nonce-bound ready/owner-token/exact loopback HTTP/SSE/shutdown；strict wire→domain | approved binary/config + Host wire | typed Host session/turn/reasoning/cleanup domain | 直接调用 Runtime、Key/path/raw token 暴露给 Vue；S7A不提供Tauri command |
| ConversationApplication / Desktop Rust | transactional session/message/outbox、Host dispatch、strict event reducer、history pagination、title precedence | repository + typed Host domain | Rust-only application projections/terminal records | Tauri/WebView API、Vue state/render、title Host invocation、feature activation |
| yijie-agent-host | thread/turn adapter、event projection、mapping/status、approved cleanup/title op；G2A候选可保留30天content-free cleanup operation receipt | local bearer + task/session/turn | sanitized HTTP/SSE | conversation business DB、tenant authority、raw body/title/path receipt |
| yijie-codex | canonical app-server Runtime | stable stdio requests | canonical responses/events | Yijie business policy/storage |
| MiniMax | model generation | text/prompt via Runtime | answer/raw reasoning events when emitted | Yijie authorization |
| yijie-api | secure Public Tasks control plane | bearer + tenant selector + metadata | authorized task/errors/audit | local conversation body/history |
| yijie-contracts | wire authority | reviewed schemas | generated artifacts/fixtures | runtime canonical/private DB authority |

```text
Vue intent
  → Tauri command (scope + validation)
  → Local DB transaction/outbox
  → SidecarSupervisor → Agent Host → Codex Runtime → MiniMax
  ← SSE allowlisted events ← Runtime
  → Local DB append → Vue store/render

Public Tasks security track:
authenticated client → secure versioned API → identity/tenant/authz → scoped repository + audit
```

### 2.1 S7A Rust Host Bridge冻结结果

- `HostBridge`只能由本次`SidecarSupervisor`产生的`HostConnection`构造；origin固定为`http://127.0.0.1:<port>`，client禁用系统代理和redirect。
- 每次受保护HTTP/SSE前先请求`/readyz`，要求`X-Yijie-Host-Instance-Nonce`精确匹配spawn UUID、`Cache-Control: no-store`、严格JSON与`runtime_state=ready`。
- bearer只在Rust中从Host home的`api-token`读取：`O_NOFOLLOW|O_CLOEXEC`、regular file、当前euid、单硬链接、group/other无权限、≤1KiB、43字符base64url；token/path不进入领域错误、Debug、Tauri或WebView。
- 请求面只覆盖现有start/resume/get session、纯文本turn、interrupt、cleanup和v2 events；不提供title method，避免固定Runtime无法能力级禁用tools时被误调用。
- v2 SSE要求schema response header、stream UUID、canonical cursor和严格递增sequence；已知event严格解析，未知非terminal event只推进delivery cursor并丢弃payload，未知terminal/畸形/cap越界fail closed。
- 该切片是现有Host contract的additive local consumer；未修改`yijie-contracts@29317b...`、Host producer、Tauri invoke列表或Vue源码，所有flag仍为false。

### 2.2 S7B Rust Application Orchestration冻结结果

- schema v3仅增加私有唯一/ready索引；session、首条user message与create-session outbox在一个SQLCipher事务创建，同一operation+同一payload幂等返回，payload冲突拒绝。
- outbox以30秒lease恢复pending/过期inflight，最多16次；Host明确接受turn后将记录挂起且不自动重放，transport/结果未知时fail closed，避免重复模型调用。
- reducer严格绑定task/session/thread/turn/stream/event/sequence；精确重复忽略，gap或identity mixup拒绝。assistant与cursor按16 events或50ms合并checkpoint；terminal在单事务提交assistant、reasoning、cursor和outbox。
- raw reasoning在内存按既定caps聚合；completed snapshot为权威。冲突、受控中断或缺失分别落`incomplete/protocol_error`、validated-prefix incomplete或`unavailable/reasoning_not_emitted`，不伪造正文。
- session列表只读metadata并按pinned/activity/stable ID排序；history按turn分页，默认20/最大50，messages/reasoning metadata批量装配，raw正文仍通过既有窄加载边界读取。
- title采用model/fallback/user来源与CAS：人工rename取消job并永远覆盖迟到模型结果；模型结果NFC/plain/no control/bidi/HTML-like且≤40 grapheme，总尝试上限2。固定Runtime不能禁用tools，因此S7B不派发title Host operation，title flag继续关闭。
- 本切片未新增Tauri command/invoke或Vue源码，不修改Host/Public Tasks wire和唯一source candidate；属于私有durable/application semantic change。

### 2.3 DESIGN-126-005 — Desktop IPC/ViewModel Contract（S8A Accepted）

状态：DESIGN-126-005/DEC-126-029、DEC-126-030/031 Accepted；S8A Closure Passed，G3仍Partial。已创建private schema/fixtures、Rust DTO/commands/events和TypeScript validators/client/store；没有修改Vue页面/组件/路由/样式，也没有启用feature flag。

#### 2.3.1 Current gap与目标边界

| Surface | DESIGN-126-005目标 | S8A本地结果 |
|---|---|---|
| ConversationApplication | 只在authorized facade之上增加窄IPC adapter，不把协调、identity或retry责任交给WebView | PASS：DB-only读与resync可离线使用；需要Host的durable writes在写入前fail closed；coordinator仍在Rust |
| Tauri invoke | 只增加versioned、closed、scope-bound conversation commands/events | PASS：20个`*_v1` private commands；旧unversioned project invokes从handler移除；event仅允许WebView listen/unlisten |
| Streaming | Rust将受控state投影为单一bounded event channel，WebView永不接触Host wire | PASS：`yijie.chat.event.v1`、closed 7-kind envelope、sequence/caps/backpressure/resync/context invalidation |
| TypeScript | fixed fixtures建立validator/client/store，负责selection与UI state而非业务重试 | PASS：strict validators、真实Tauri transport client、单一authoritative Pinia reducer、stale/restart/race tests |
| Vue | S8B只消费真实S8A store；production source禁止mock transport | 未授权/未修改；S8A没有页面、组件、路由、样式diff |

#### 2.3.2 Authority与authorization context

- authoritative private IPC source为Desktop-owned `src-tauri/schemas/chat-ipc-v1.schema.json`；20个command contract ref、7个互斥event variant与closed payload definitions由Rust/TypeScript双端测试核对，golden fixtures再验证实际serde/parser投影。schema、fixtures与validators只属于S8A，不复制到central contracts。
- Rust-only `ChatAuthorizationContext`由`chat_bind_context_v1`建立。WebView只提供untrusted tenant selector；Rust向native auth authority取得最新projection并验证signed-in、tenant、revision、expiry，再与固定local `ChatScope`相交。owner identity不进request/response，不能由WebView选择。
- `contextId`为随机UUID、最多5分钟且不晚于authority expiry；绑定auth generation、tenant、owner scope与process epoch。logout、tenant切换、capability revision回退/expiry、app restart均使其失效；先同步清空TS store，再发`context_invalidated`。
- Desktop local action policy：`task.read`允许list/history；`task.create + task.read`允许create/send/rename/session pin/interrupt/delete；项目选择/revalidate/pin/remove另需`workspace.use`。每个command仍需resource owner+tenant check；unknown command/action或foreign opaque ID拒绝。本地policy不新增或模拟Public Tasks capability。

#### 2.3.3 Command、response、cursor与error

完整command allowlist和closed envelope见`04-contract-change-plan.md §3.5`。关键规则如下：

- request=`{schemaVersion:1, requestId, contextId, payload}`；bootstrap bind唯一省略`contextId`并只含untrusted tenant selector；write额外要求`operationId`。response=`{schemaVersion:1, requestId, data}`。全部object/union closed；UUID和字符串在Rust与TS runtime同时校验。
- WebView只能传opaque project/session/turn ID、分页cursor、bool pin intent及已验证长度的纯文本。禁止owner/user/tenant authority值、canonical path、Host/Runtime ID、SQL、bearer/key、provider config和raw Host payload。
- cursor是≤256-byte随机opaque、server-side解析且绑定context/query/process epoch的token，最多10分钟；restart、unknown、scope/query不匹配或过期返回`chat_cursor_invalid`，不能fallback offset或猜测DB row key。
- stable error shape固定为`{schemaVersion, requestId?, code, retryable, recovery, retryAfterMs?}`。`code` closed allowlist：`chat_unauthenticated`、`chat_context_invalid`、`chat_capability_denied`、`chat_resource_not_found`、`chat_project_invalid`、`chat_cursor_invalid`、`chat_request_invalid`、`chat_request_cancelled`、`chat_conflict`、`chat_turn_active`、`chat_host_not_ready`、`chat_storage_unavailable`、`chat_protocol_error`、`chat_limit_exceeded`、`chat_cleanup_incomplete`、`chat_temporarily_unavailable`。error不含自由文本/detail；Vue以code本地化。
- session list最大50项/512KiB；history默认20/最大50 turn且总响应≤4MiB；raw reasoning一次单turn≤256KiB；resync最多1MiB assistant + 256KiB reasoning。单条user/assistant durable正文仍服从现有1MiB hard cap和64KiB产品soft cap策略。

#### 2.3.4 Event sequence、backpressure与projection safety

- 唯一channel为`yijie.chat.event.v1`；event绑定`subscriptionId/contextId/sessionId/turnId?`，以十进制字符串携带严格递增`projectionSequence`，避免JavaScript整数精度丢失。
- kind只允许`assistant_append|reasoning_append|turn_state|turn_terminal|cleanup_state|resync_required|context_invalidated`。projection不能含Host envelope/message/error/ID、Runtime thread/item ID、canonical path、token/key或其他session内容。
- assistant/reasoning只投影Unicode-valid plain text；不渲染为HTML/Markdown。assistant append≤64KiB、reasoning append≤16KiB；reasoning身份只用Desktop local item ordinal和content index。
- 每subscription queue≤64 events或256KiB，连续append可在caps内合并，向WebView最多20Hz。overflow/drop/gap立即停止progress并投递不可丢的`resync_required`；terminal/context-invalidated同为不可丢。TS发现duplicate时忽略，发现gap、context/subscription/session mismatch时丢弃未提交projection并resync。

#### 2.3.5 Cancellation、stale selection与restart

- read/subscription可由request ID取消；Rust接受后的durable write不能被cancel回滚。write结果以operation ID查询/恢复；停止生成是独立interrupt command。
- store维护`contextId + subscriptionId + selectionEpoch`。选择A→B、logout或context更新时先同步清空旧正文与pending view state，再取消旧read/订阅；late A response/event一律不能commit到B。
- S7C coordinator独占outbox dispatch、Host subscribe/reconnect、interrupt/delete saga与startup recovery。WebView不能触发低层dispatch/retry或自己合并Host cursor。
- app/sidecar重启后旧context、subscription和cursor失效；S8A重新bind，S7C从SQLCipher恢复outbox/active turn/cleanup状态并生成resync snapshot。Host 409 replay loss进入`resync_required`/reconcile，不能把本地buffer和新stream猜测拼接。

#### 2.3.6 S7C/S8A/S8B授权顺序

1. `S7C`：只允许Desktop Rust补session/project pin、interrupt、跨表面delete/cleanup status、Rust authorization context、background coordinator与restart/resync projection source；不新增Tauri invoke/event、TypeScript或Vue。
2. `S8A`：在S7C Closure后，增加authoritative IPC schema/fixtures、窄Tauri commands/event bridge、TypeScript runtime validators/client及Pinia store/view-model；不修改Vue页面、视觉、route activation或feature flag。
3. `S8B`：在S8A Closure后，按Accepted Pattern实现Vue页面、interaction、visual/a11y及visual tests；只使用真实S8A store，mock transport仅限test harness，不能存在于production path。feature activation仍需独立批准。

Owner已接受DEC-126-030/031及DEC-126-032；LIA-126-005已完成S8B0本地候选。DEC-126-033 Closure Review尚待批准，S8B不得提前进入。

### 2.4 DESIGN-126-006 — S8B0 UI Integration Readiness（Accepted / Implemented Candidate）

状态：DESIGN-126-006/DEC-126-032已获Owner接受，LIA-126-005已在`yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85`关闭以下S8B0集成缝隙并提交DEC-126-033。完整S8B Vue UI仍未授权。

#### 2.4.1 Default-off gate与route authorization

- `VITE_YIJIE_CHAT_LOCAL_UI_ENABLED`只在值exact等于`true`时开启，缺失、空、`TRUE`、`1`或其它值均为false。它与native `YIJIE_CHAT_LOCAL_ENABLED`、`YIJIE_CHAT_LOCAL_HOST_ENABLED`及authoritative permission状态分别承担UI可达、Rust domain/DB、sidecar和授权职责，不得互相隐式开启。
- flag=false时不生成Chat/Tasks导航项、不注册`/chat`或`/chat/:sessionId`业务route（或在loader之前立即安全重定向）、不调用lazy component loader、不bind Chat store、不启动Host。`.env*`、CI、Vite default/dev/build配置都不得写true。
- route以meta而不是exact path map声明capability：`/chat`要求`task.create`；`/chat/:sessionId`要求`task.read`。每个mutation仍以Rust context `allowedActions`和resource scope复验。session参数只接受opaque UUID，不能成为DB/Runtime ID。
- 深链结果：未登录/context invalid→permission recovery；缺capability→`/access-denied`；not-found/deleted/foreign统一generic unavailable后replace到`/chat`，不得泄露存在性；stale selection先取消read、退订、清正文、resync，若新scope仍存在才恢复。

#### 2.4.2 Permission与Chat lifecycle

App-level integration adapter监听permission store的`phase/tenant/revision/expiry`，而不是由页面各自bind。状态顺序固定：`permission not ready/logout/expiry`→同步clear正文和selection→取消read/退订→dispose context；`tenant/revision changed`→完成旧dispose→以当前selector调用一次`chat.bind`；较慢旧bind由generation拒绝。页面unmount只释放页面局部focus/scroll，不得擅自销毁仍属同scope的authoritative store；app logout必须销毁。

#### 2.4.3 Pinia consumption additions

- 暴露store-owned `pickProject`、`revalidateProject`，成功后刷新安全project DTO；Vue不得接触bookmark/path或直接调用client。
- 增加`loadMoreSessions`：使用当前`nextCursor`，按`sessionId`去重并追加，保留server pinned/activity稳定顺序；context/generation变化丢弃旧页，cursor invalid从首页reload。
- `deleteSelected`继续使用stable operation ID并返回closed `DeleteDisposition={state,nextSessionId?}`。`complete`时store清除被删session的history/live/reasoning/cleanup/selection，reload sessions/projects并选择Rust返回/排序后的相邻opaque session；无剩余则返回`/chat`。`pending/incomplete`保持status和当前安全metadata，禁止UI先移除冒充成功。
- `/tasks`与App Shell session树使用同一metadata page/store；production `sampleTasks`不得被import。若真实接线未完成，route/nav保持default-off而不是显示样例。

#### 2.4.4 Readiness、start/retry与storage projection停止条件

S8A `phase=ready`只证明context/list加载完成，不证明本次Host child、spawn nonce、Runtime protocol和SQLCipher writer均ready。现有20-command schema也没有UI可消费的closed readiness。因此DESIGN-126-006触发用户规定的停止条件：本轮不改源码，候选shape见`04-contract-change-plan.md §3.6`。

- `chat_get_local_readiness_v1`只读返回Host/Runtime/storage/lifecycle、`canSend`、stable issue/recovery；每次发送仍由Rust submit command再次权威校验，避免check/use race。
- `chat_request_local_recovery_v1`只接受`start_or_retry`和stable operation ID；Rust coordinator独占binary/env/token/loopback/start/backoff。Vue不能调用旧`chat_start_local_host`或自行循环。
- storage issue稳定区分`read_only|full|corrupt|migration_failed|unavailable`，但只投影content-free code与受控recovery，不回显路径、SQL、key或SQLite/Host message。corrupt/migration失败保持writer关闭，不自动破坏性修复。
- Schema、Rust serde/registry、TS validator/client/store及fixed fixtures已按单独LIA-126-005完成；所有flags继续off，DEC-126-033通过也不自动启用。

#### 2.4.5 Scroll、a11y与后续切片

- Accepted Pattern 1.0.0优先：距离底部≤48px跟随；>48px不抢滚动；>160px或有未读显示按钮；按钮`aria-label="滚动到对话底部"`。reduced-motion下即时滚动。
- S8B0只做gate/router/lifecycle/store/readiness/cleanup/tasks integration及其非视觉测试；S8B才实现真实Vue App Shell/session树/composer/conversation/reasoning/menu/dialog/visual/a11y。S9为fake-provider Eval，S10为临时test profile四组件E2E，S11为Owner G6；每段另行授权。
- 未来S8B测试必须使用生产Pinia reducer和production components；fake ChatClient只能由test harness注入且通过bundle deny测试。覆盖light/dark、1180×760、200% zoom、reduced-motion、keyboard、IME、focus restore、menus/dialogs、scroll/reasoning、axe、visual snapshot与VoiceOver人工记录；如需devDependency必须固定版本、提供audit/lockfile证据，production dependency不得新增。

## 3. 关键时序

### 3.1 新建与首 turn

1. Router/store 从 FEAT-125 authoritative projection确认 UX capability；Tauri command 仍绑定 current user/tenant scope。
2. Native project repository revalidates bookmark/canonical directory; Host/Runtime readiness must be ready。
3. `create_session_and_enqueue` 生成 local session ID、client operation ID、local task UUID，在单事务写 session、user message、pending outbox；正文不发送到 Public Tasks DB。
4. Vue 仅在 commit 成功后进入 `/chat/:sessionId`。
5. Sidecar client 用 local task UUID 创建 Agent session；Host canonicalizes cwd and starts persistent Runtime thread。
6. Outbox starts text turn with request/trace correlation；Host response binds turn ID；Desktop subscribes SSE。
7. Desktop reducer validates session/stream/sequence/event ID，以批量checkpoint持久化assistant/cursor；raw-reasoning在Rust内存聚合，并在terminal对账或受控中断时按DEC-126-016单事务持久化。S8未来只负责把已验证projection按纯文本渲染。
8. 唯一 terminal event closes turn/outbox，updates `last_activity_at`；独立 title job 在首个有效 answer 后触发。

### 3.2 后续 turn

1. Validate current scope/project/active lock and persist user message + outbox。
2. Start turn once；network retry reuses operation ID；409 active maps to current state reconcile。
3. Stream/persist; stop uses interrupt and waits terminal。

### 3.3 历史懒加载

1. `list_sessions(scope, cursor, limit)` only returns metadata/title/status/project reference。
2. UI selection increments selection generation/cancels prior request。
3. `load_messages(scope, session, before, limit)` verifies ownership then returns one page；stale generation cannot commit UI state。
4. Runtime resume is required only to continue, not to display locally persisted history。

### 3.4 永久删除

1. UI shows exact session and irreversible scope; user confirms once。Rust generates an idempotent deletion operation ID and stores a content-free deletion job/receipt outside conversation rows。
2. Acquire a durable deletion lease and block every writer/outbox retry for this session；a duplicate request resumes the same operation rather than creating a second delete。
3. If a turn is active, call interrupt and wait for the unique bounded terminal event；timeout or uncertain terminal aborts cleanup and keeps the session visible as `delete_failed`。
4. Verify this session exclusively owns the mapped Runtime thread tree；any cross-session/shared descendant mapping aborts。Host calls stable `thread/delete`, which also covers spawned descendants, verifies response/`thread/deleted` outcomes, then clears bbolt mapping and in-memory replay state。Project directories are never a delete target。
5. Only after required external surfaces are proven absent, Desktop opens one SQLite transaction with FK enforcement and cascades messages/turns/summaries/cursors/outbox/session。External-first ordering prevents local success from hiding a recoverable Runtime thread。
6. Desktop verifies `secure_delete=ON`, runs `PRAGMA wal_checkpoint(TRUNCATE)` in an exclusive maintenance step and treats busy/error/non-truncated WAL as incomplete。Only then finalize a content-free receipt：operation ID、keyed scoped-session hash、surface outcome bits、stable outcome code、timestamps/schema version；不含 raw session/thread ID、title/message/reasoning/path。
7. Any partial result remains retryable/repairable。Host/Runtime cleanup uncertainty or SQLite checkpoint failure must not remove the item from UI or claim “永久删除完成”。

跨进程不存在分布式事务；删除 job/receipt 是恢复控制，不是 soft-delete 会话记录。pending 加密 job
只暂存重试所需 technical IDs；完成后 raw IDs 被移除，receipt 候选保留 30 天再以 secure-delete +
checkpoint 清理。完成态只证明当前 Yijie app-managed live stores 不可重新打开/resume；Runtime 隔离验证
已发现 WAL/log 字节残留，因此不得承诺 SSD/APFS/Runtime log/OS backup 的法证抹除。上述候选需
该边界已由 ADR-0014/DEC-126-006 于 2026-08-02 接受；G2/G2A已通过，但仍需后续实现验证，不得把设计批准写成已实现保证。

### 3.5 Public Tasks hardening

1. Auth middleware validates bearer into internal Principal。
2. Tenant service parses selector and verifies active membership；authorization service checks action。
3. Handler builds server-owned command with principal/tenant/request/trace/idempotency；client tenant never grants access。
4. Repository query/write always scopes tenant and required owner/resource；data mutation + audit share transaction。
5. Stable response/error no-store；legacy route remains isolated until version migration evidence。
6. Consumer inventory采用条件分支：任何 supported/unknown external consumer 都要求 protected versioned expand→migrate→observe→major retirement；只有 Owner 证明 v1 从未发布且无 supported consumer，才评审同路径 pre-release replacement。

### 3.6 隔离标题与 raw model reasoning（ADR-0015 + ADR-0016 Accepted）

标题链路与主 conversation 完全分开：

```text
first answer terminal
  → Desktop checks title_source != user and one idempotent title job
  → Host /v2/.../title-generations (first user text only, max 8 KiB)
  → empty temporary cwd + Runtime thread/start(ephemeral=true)
  → turn/start(title-v1, strict outputSchema)
  → validate JSON/NFC/plain single line/1–40 grapheme
  → unsubscribe + clear Host correlation
  → Desktop compare-and-set title only while title_source != user
  ↘ timeout/refusal/incomplete/schema/tool/unknown → deterministic local fallback
```

- Host 必须断言 ephemeral response `thread.ephemeral=true`、`thread.path=null`；否则取消 operation 并降级。
- Title Runtime 事件不得进入主 session stream。任何 command/tool/approval/file-change item 都触发 interrupt、
  `title_output_invalid` 与 fallback；临时 cwd 不含用户 project/environment。
- ephemeral thread 不写 rollout，canonical `thread/delete` 对它返回 invalid request；完成后使用 unsubscribe/
  correlation cleanup，不能制造 delete 成功证据或用 persistent title thread 代替。
- Desktop 以 `(session_id, operation_id)` 保证单次 job；首次确定失败可由受控 retry 创建第二个 attempt，
  总 provider call hard cap=2。unknown outcome、人工 rename、session delete/cancel 均不 retry。

ADR-0016 已取代 public-summary-only 链路。raw reasoning 采用 versioned v2 显式投影：

```text
Runtime reasoning textDelta ─→ item.reasoning_text.delta {content_index, delta}
Runtime reasoning item/completed raw content ─→ item.reasoning_text.finalized {status, contents, reason_code?}
Host logs/bbolt/metrics/audit/error body ─X raw reasoning正文
Desktop ─→ plain-text “模型推理记录” + explicit incomplete/unavailable state
```

- v2 exact contract 只增加 `item.reasoning_text.delta` 与 `item.reasoning_text.finalized`。delta payload
  为 closed `{content_index,delta}`；finalized payload 为 closed `{status,contents,reason_code?}`，其中
  `status=complete|incomplete|unavailable`，`contents[]` 是索引升序、唯一且连续的
  `{content_index,text}`。stable reason只允许`reasoning_not_emitted`、`turn_interrupted`、`stream_gap`、
  `runtime_error`、`limit_exceeded`、`protocol_error`、`host_shutdown`。v2 turn以0个reasoning item到达
  `turn.completed`时，只在turn级记录`unavailable/reasoning_not_emitted`，不伪造item ID或正文。
- Desktop key 为 `(turn_id,item_id,content_index)`，按 event ID 去重并验证 stream-local sequence；delta
  只进入内存。Runtime completed `ThreadItem::Reasoning.content[]` 是权威快照，finalized 到达时替换而非
  追加 buffer；complete 必须精确对账，partial/中断/gap/conflict 显式 incomplete，无可用正文为 unavailable。
  answer 可独立 terminal，但不得用 answer、伪造文本或状态/时长冒充 reasoning 验收通过。
- caps 以 UTF-8 bytes 计算：每 delta 16 KiB、每 part 64 KiB、每 item 128 KiB、每 turn 256 KiB；
  每 item 最多 8 parts、每 turn 最多 8 reasoning items。Host 既有 1 MiB/event hard limit不变；超限
  必须 `limit_exceeded`，不允许静默截断。
- UI使用纯文本节点，不执行HTML/Markdown/URL/命令/tool/approval；标注“模型推理记录”，不承诺完整、
  稳定、准确或等同模型全部内部思维。正文不得进入Host/Desktop logs、metrics、trace、audit、receipt、
  bbolt或provider error；content-free观测只记录count/bytes/duration/status/reason。
- 当前v1 event schema是closed union。raw variants必须由v2 schema + `event_schema_version=2` negotiation
  提供；先升级Desktop consumer，再打开Host producer。原public-summary variants未形成source contract，
  不继续发布。
- DEC-126-016已批准历史生命周期，DESIGN-126-003进一步冻结实现前设计：Desktop仅在finalized或受控
  interruption时以一个SQLCipher transaction写turn状态、item和parts；unexpected crash没有finalized时
  不从delta猜造正文。session list不读正文；history默认20/最大50 turns，仅批量读取reasoning metadata；
  展开时一次按turn加载raw body，最大256 KiB。session删除经turn→reasoning items→parts FK cascade。

## 4. 状态模型

### 4.1 Session/turn state

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 非法处理 |
|---|---|---|---|---|---|
| none | local create committed | valid scope/project/text | queued | session/message/outbox durable | validation/DB error, no route |
| queued | Host session bound | one pending op | ready | save agent/thread IDs | idempotent reconcile |
| queued/ready | turn accepted | no active turn | streaming | bind turn/stream | 409 reconcile; other error retryable/terminal |
| streaming | message/raw-reasoning delta | valid stream/sequence/item | streaming | 内存dedupe append + cursor；terminal对账或显式incomplete时写SQLCipher | unknown allowed；raw malformed/incomplete marks reasoning unavailable and fails its Gate |
| streaming | interrupt requested | matching active turn | stopping | call Host interrupt | duplicate stop idempotent |
| streaming/stopping | terminal completed | exactly one terminal | completed | close outbox, activity/title job | later event ignored/audited |
| streaming/stopping | terminal interrupted | exactly one terminal | interrupted | preserve partial result | later event ignored |
| any non-deleted | retryable failure | bounded policy allows | failed_retryable | store stable code | no automatic duplicate turn |
| any non-deleted | delete lease | exact confirm | deleting | block writers/stop active | concurrent actions conflict |
| deleting | all required cleanup + DB commit | approved surfaces complete | deleted | no recoverable local row | partial result abort/forward repair |

### 4.2 UI state

必须覆盖：`auth_loading`、`permission_denied`、`runtime_not_ready`、`entry_empty/ready/submitting`、`list_loading/empty/error/ready`、`history_loading/not_found/error/ready`、`streaming/stopping/completed/interrupted/failed`、`db_read_only/full/corrupt/migration_failed`、`deleting/delete_failed`。

## 5. 领域模型与不变量

| Entity/Value | Owner/tenant scope | ID/幂等键 | 不变量 | 生命周期 |
|---|---|---|---|---|
| ChatProject | OS user + app user + tenant | local UUID; canonical identity/bookmark | no raw path to Vue/log; remove != delete directory | add→pin/use→remove |
| ChatSession | app user + tenant | local UUID; optional public task ID; unique Agent session | exactly one project reference snapshot；exclusively owns one Runtime thread tree；no soft delete | create→active/history→physical delete |
| ChatMessage | session | UUID + client operation ID + sequence | immutable role/content after commit; no user edit | pending→committed/failed→cascade delete |
| ChatTurn | session | operation ID + Runtime turn ID | at most one active; exactly one terminal | queued→streaming→terminal→delete |
| ModelReasoningRecord | turn | item ID + content index/sequence | fixed Runtime raw text only；plain-text/untrusted；completed snapshot authoritative；caps/fields/failure semantics fixed by DESIGN-126-003；no-log/telemetry/audit body | streaming in memory→finalized/incomplete SQLCipher transaction→session cascade delete |
| EventCursor | session | stream ID + sequence/event ID | monotonic per stream; event ID unique | update→stream change→delete |
| OutboxOperation | session | unique operation ID | retries reuse payload identity; terminal closes once | pending→inflight→done/failed→delete |
| PublicTask | verified tenant + creator/resource policy | server UUID + idempotency key | tenant/creator server-derived; all access scoped | create→lifecycle→authorized delete/retention |

## 6. 数据与 Migration 专项

- 涉及持久化：是；ADR-0013 已接受 Desktop embedded SQLite authority，并计划扩展 API Tasks ownership/auth indexes/audit。
- 已批准边界：DEC-126-005/014；只冻结 authority、存储职责与 no-double-write/no-cloud-sync。
- 已批准设计：ADR-0014/DEC-126-006 Accepted，Q-006/Q-015 Resolved；不等于实现授权。
- 已提交批准：DESIGN-126-003/DEC-126-017、DEC-126-011/012 与 Chat/App Shell Pattern；Owner 接受前继续阻断 G2。

### 6.1 存储职责冻结（ADR-0013）

| 存储 | 本期权威职责 | 明确不负责 | FEAT-126 状态 |
|---|---|---|---|
| Desktop embedded SQLite/SQLCipher | 本地 projects/sessions/messages/turns/raw reasoning records/cursors/outbox/title/delete job/receipt | Public Tasks/RBAC、Runtime rollout、云同步 | ADR-0013/0014与DEC-126-016/017 Accepted；S6 foundation implemented/tested，完整 UI/E2E 仍属 S7+ |
| yijie-api PostgreSQL | Public Tasks、identity/tenant/RBAC、server audit | conversation body/raw reasoning/local path | existing server authority；S4 secure Tasks foundation implemented/tested，默认关闭 |
| Redis | 未来明确需要时的 cache/rate limit/idempotency/short coordination | durable truth、conversation body、RBAC truth | not used by FEAT-126 v1 |
| PostgreSQL + pgvector | Knowledge/RAG 的 embedding/vector retrieval | 普通聊天历史与 FEAT-126 标题/raw reasoning | out of scope |
| Agent Host bbolt | task/session/thread/turn mapping 与 adapter state | business history/title/body | cleanup surface only |
| Runtime CODEX_HOME/state | canonical thread/rollout/runtime metadata | Desktop history/list authority | cleanup surface only |

### 6.2 Desktop private schema 候选

| Table | 关键字段/约束 | 备注 |
|---|---|---|
| `chat_schema_migrations` | version, name, sha256, applied_at | `user_version` execution + embedded checksum ledger |
| `chat_projects` | id, owner_user_id, tenant_id, safe_name, encrypted/bookmark_ref, pinned_at, last_used_at, removed_at | unique scoped canonical identity；path 不暴露给 Vue |
| `chat_sessions` | id, owner_user_id, tenant_id, project_id, title, title_source, title_job_status, pinned_at, created_at, last_activity_at, agent/thread refs | no `deleted_at`; physical delete only |
| `chat_messages` | id, session_id FK cascade, turn_id, role, content, status, ordinal, created_at | unique(session, ordinal), immutable content |
| `chat_turns` | id, session_id FK cascade, operation_id unique, runtime_turn_id unique nullable, status, terminal_at, reasoning_status, reasoning_reason_code | partial unique active turn per session；reasoning status `pending/complete/incomplete/unavailable` |
| `chat_reasoning_items` | turn_id FK cascade, item_id, item_ordinal, status, reason_code, total_bytes, finalized_at_ms | PK(turn_id,item_id), unique(turn_id,item_ordinal)；restricted metadata；unavailable 可为 0 parts |
| `chat_reasoning_parts` | turn_id, item_id, content_index, text, byte_count | composite FK→items ON DELETE CASCADE；PK(turn_id,item_id,content_index)；raw body SQLCipher only |
| `chat_event_cursors` | session_id PK/FK cascade, stream_id, sequence, event_id | monotonic update transaction |
| `chat_outbox` | operation_id PK, session_id FK cascade, kind, state, attempt_count, next_attempt_at, payload_version | payload protected; bounded retry |
| `chat_deletion_jobs` | operation_id PK, encrypted retry IDs, surface state, requested_at | conversation rows外；完成后压缩/清除 technical IDs |
| `chat_deletion_receipts` | operation_id PK, keyed_session_hash, surface bits, outcome, timestamps, schema_version | 无正文/path/raw IDs；候选 30 天 retention |

Indexes include `(owner_user_id, tenant_id, pinned_at DESC, last_activity_at DESC, id DESC)` for sessions and scoped project sort. SQL/logging must not include content/path.

### 6.3 DESIGN-126-003 SQLCipher schema、聚合与分页冻结

候选 migration `0002_chat_reasoning_v2` 在 `0001_chat_core` 之后原子创建/变更下列结构；这是设计冻结，
不是实际 migration 文件或实施授权：

```sql
ALTER TABLE chat_turns ADD COLUMN reasoning_status TEXT NOT NULL DEFAULT 'pending'
  CHECK (reasoning_status IN ('pending','complete','incomplete','unavailable'));
ALTER TABLE chat_turns ADD COLUMN reasoning_reason_code TEXT;

CREATE TABLE chat_reasoning_items (
  turn_id TEXT NOT NULL REFERENCES chat_turns(id) ON DELETE CASCADE,
  item_id TEXT NOT NULL,
  item_ordinal INTEGER NOT NULL CHECK (item_ordinal BETWEEN 0 AND 7),
  status TEXT NOT NULL CHECK (status IN ('complete','incomplete','unavailable')),
  reason_code TEXT,
  total_bytes INTEGER NOT NULL CHECK (total_bytes BETWEEN 0 AND 131072),
  finalized_at_ms INTEGER NOT NULL,
  PRIMARY KEY (turn_id, item_id),
  UNIQUE (turn_id, item_ordinal),
  CHECK ((status = 'complete' AND reason_code IS NULL AND total_bytes > 0)
      OR (status = 'incomplete' AND reason_code IS NOT NULL AND total_bytes > 0)
      OR (status = 'unavailable' AND reason_code IS NOT NULL AND total_bytes = 0))
);

CREATE TABLE chat_reasoning_parts (
  turn_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  content_index INTEGER NOT NULL CHECK (content_index BETWEEN 0 AND 7),
  text TEXT NOT NULL,
  byte_count INTEGER NOT NULL CHECK (byte_count BETWEEN 1 AND 65536),
  PRIMARY KEY (turn_id, item_id, content_index),
  FOREIGN KEY (turn_id, item_id)
    REFERENCES chat_reasoning_items(turn_id, item_id) ON DELETE CASCADE
);
```

- SQLite `length(TEXT)` 不能作为 UTF-8 byte 上限；Rust 在入库前执行 `text.as_bytes().len()`、part/item/turn
  累计和最多 8 items/8 parts 检查，DB checks只做第二层约束。`reason_code` 同样由Rust closed enum校验。
- reducer 不逐 delta 写库。每个 event先做 event ID/stream sequence验证，在内存按 item/index聚合；finalized
  快照对账后以一个 transaction替换该turn的items/parts并更新`chat_turns.reasoning_*`。controlled interrupt
  可把已验证前缀写为incomplete；Host/Desktop意外崩溃无finalized时不猜造raw正文，恢复后标unavailable。
- session metadata page固定最大50且不join message/reasoning正文。history命令使用opaque cursor，默认20、最大
  50 turns，并在同一批次返回reasoning item metadata；raw正文仅在用户展开某turn时由scope-checked Rust
  command一次加载，单turn不超过256 KiB。禁止逐item N+1查询或预取其它session正文。
- `0001_chat_core`/`0002_chat_reasoning_v2` 均为embedded、checksum-locked、forward-only migration；旧app
  不写其不支持的新schema，不做down migration。future DB version、checksum drift、migration或
  `foreign_key_check` failure均fail closed；恢复只允许rollback app、forward repair或用户确认reset。
- 删除链固定为 `chat_sessions → chat_turns → chat_reasoning_items → chat_reasoning_parts` FK cascade；事务后
  验证目标计数为0与`foreign_key_check`，再按ADR-0014执行`secure_delete=ON`和
  `wal_checkpoint(TRUNCATE)`。receipt不含item ID、正文、digest或raw thread/session ID。

### 6.4 SQLite implementation freeze（ADR-0014 Accepted）

- Driver：精确锁定 `rusqlite 0.40.1`，关闭默认 features，启用 `bundled-sqlcipher,uuid,limits`；
  migration 锁定 `rusqlite_migration 2.6.0`。临时 Rust 1.95/macOS arm64 locked build PASS；
  Refinery 0.9.2 因只兼容 rusqlite ≤0.39 且 `libsqlite3-sys` native `links` 冲突而拒绝。
- Execution：Rust repository worker 上单一 serialized writer + 有限 readers；同步 DB work 不阻塞
  Tokio/UI；不使用 Tauri SQL plugin/SQLx，不向 Vue 暴露 path/SQL/key。
- Migration：embedded numbered forward-only SQL，以 `user_version` 执行；`up_with_hook` 在同一原子
  transaction 写 `chat_schema_migrations` SHA-256 ledger；checksum drift、future DB version、migration/
  `foreign_key_check` failure 均 fail closed。无 silent backup/down migration，只做 rollback-in-place、
  forward repair 或经用户确认的 destructive reset。
- File/key：bundle identifier `com.yijie.ai` 解析的 Tauri `app_data_dir/chat/` 为专用 dir `0700`，
  DB/WAL/SHM `0600`；open 前校验
  owner/mode/regular/non-symlink/link-count。Keychain service `com.yijie.ai.chat-db` account `default-v1`
  保存随机 32-byte key；`sqlite3_key_v2` raw key 必须为第一操作，buffer zeroize；existing DB 丢 key
  fail closed，不静默生成替代 key。`cipher_memory_security=ON`。receipt keyed hash 使用独立 Keychain
  service `com.yijie.ai.chat-receipt` 的 32-byte key 做 HMAC-SHA-256，不复用 DB key。
- 每 connection 验证 `foreign_keys=ON`、`journal_mode=WAL`、`synchronous=FULL`、macOS
  `fullfsync=ON`/`checkpoint_fullfsync=ON`、`secure_delete=ON`（不使用 FAST）、`busy_timeout=5000`、
  `wal_autocheckpoint=1000`、`journal_size_limit=1048576`、`trusted_schema=OFF`。v1 不使用 FTS/
  virtual table。每次成功删除前独占执行并验证 `wal_checkpoint(TRUNCATE)`；busy/error 即 incomplete。

### 6.5 Backup 与 uninstall 限定语义（ADR-0014 Accepted）

- v1 不创建 app-level DB backup/export/snapshot/cloud sync/iCloud container；chat dir 及每次 create/rename
  的 DB/WAL/SHM 设置并复核 `isExcludedFromBackupKey=true`。
- 该标记不能回收既有 Time Machine local snapshot、第三方/APFS snapshot、用户副本或 SSD/file-system
  history。删除成功只表示当前应用受控 live store 不可重开/resume，不表示所有磁盘痕迹已擦除。
- 拖拽 `.app` 到废纸篓只移除 bundle；Application Support 与 Keychain 可能保留，同签名重装可能
  重新打开 DB。FEAT-126 不把普通卸载当数据擦除；全量本地清理属于后续独立 feature。

### 6.6 API schema candidate

- DEC-126-012候选要求v2 `created_by_user_id`只由verified principal派生，并添加tenant/user FK与
  `(tenant_id,created_by_user_id,id)` composite index；普通role不隐式跨creator授权，未来只接受显式
  `task.read_all`/`task.manage_all` capability。
- Legacy rows with no trustworthy creator must not be assigned by guess；NULL-owner row默认隔离，只有独立授权的映射或删除流程才能处置。
- Audit adds actions/outcomes/resource identifiers without message content。

### 6.7 Expand/migrate/switch/contract

| Phase | Schema/Data change | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | create versioned local DB/tables; add nullable API owner/indexes/new route | old Desktop ignores new DB; legacy route isolated | new code handles empty/old DB | empty/old/read-only/corrupt fixtures | rollback app, keep data/flags off |
| Backfill | local N/A from no data; API legacy owner policy per explicit decision | old provider continues isolated lane | new provider rejects ambiguous legacy rows | counts/tenant-owner invariant | pause batches; forward repair |
| Switch | enable secure route and Desktop slices in staged flags | old consumer not routed | new consumer pinned | old/new matrix + canary | disable flag/route; no schema drop |
| Contract | retire legacy operation/columns only after inventory/observation | unsupported old consumer fails by declared policy | new only | production metrics/audit | roll-forward versioned lane; no unsafe down migration |

## 7. 一致性与韧性

- 事务边界：local create/message/outbox one transaction；assistant message/cursor按批准策略coalesced transaction；raw delta仅内存、finalized/controlled interruption单transaction；physical cascade one transaction；API mutation+audit one transaction。
- 跨进程一致性：outbox/saga，不做 distributed transaction。每个 step 幂等并保存 external IDs。
- 并发：per-session active-turn lease；selection generation；DB unique constraints；delete lease blocks writers。
- 幂等：client operation ID、API idempotency key、Host task/session uniqueness、Runtime turn ID、event ID/sequence。
- 超时/取消：DB commands bounded；Host HTTP timeout；SSE reconnect；interrupt bounded terminal wait；title deadline 是 G4 benchmark 前候选值且不阻塞主回答，MiniMax 两次审批验证使用每请求 120s hard timeout。
- 重试：network/503 bounded exponential jitter；validation/auth/delete unknown result不自动；title最多 1 次 retry。
- 限流/熔断：Host/provider not-ready disables send；title independent budget；stream slow consumer reconnect。
- 部分失败：durable local queued state + explicit retry；不回滚已保存用户文本；orphans 可检测/修复。
- 资源释放：route/session switch aborts readers/SSE；app shutdown stops readiness, flushes DB, graceful Host then hard timeout。

## 8. 安全设计

- 认证入口：FEAT-125 user bearer for Public API；owner-only Host bearer for loopback；Tauri command binds active identity snapshot。
- 资源级授权：Public API每操作检查；private commands每读写匹配 owner+tenant；前端 hidden/disabled 不作为控制。
- 租户隔离：tenant selector untrusted；repository scope强制；switch clears/cancels before fetch。
- 输入验证：UTF-8/non-whitespace/soft+hard size、control chars、title sanitation、strict JSON/unknown field rules。
- Path：only native picker/bookmark；canonicalize and revalidate symlink/permissions at use；Vue receives opaque ID。
- Secret/token：Key/Host token stay Rust/Host owner-only storage/env；no WebView/localStorage/URL/log。
- Renderer：sanitized Markdown allowlist；external URL opening follows existing policy；no executable HTML；no copy action toolbar。
- PII/日志：content/path never logged；stable IDs可经脱敏策略记录；raw provider/DB errors mapped。
- 高风险审批：本期 fixed read-only/deny；delete explicit confirm；unknown reverse request deny。
- 审计：Public API append-only；local deletion receipt已由ADR-0014/DEC-126-006冻结为content-free、成功后30天保留，始终无正文。

## 9. 可观测性

| Signal | 名称/字段 | 候选成功基线 | 候选告警/停止阈值 | Runbook 动作 |
|---|---|---:|---:|---|
| Metric | `chat_session_create_total{outcome}` | success ≥99% synthetic | duplicate >0 或 persistence failure >1% | disable create, inspect DB/Host |
| Metric | `chat_turn_latency_ms` / `time_to_first_delta_ms` | establish in test | P95 > approved provider budget | degrade/title off, provider check |
| Metric | `chat_sse_reconnect_total{reason}` | stream-change rare | replay loss/loop spike | stop auto retry, resume/reconcile |
| Metric | `chat_history_load_ms` | P95 targets in NFR | threshold breach/N+1 body read | page/index query review |
| Metric | `chat_delete_total{surface,outcome}` | all required surfaces success | cleanup incomplete >0 | block success UI, forward cleanup |
| Security | `task_authorization_total{action,outcome,reason}` | expected denies only | cross-tenant allow >0 | immediate route isolation/incident |
| Audit/Trace | request/trace/user/tenant/task/session/turn IDs | correlation complete | missing scope/IDs | fail request or investigate adapter |

No metric/log label may contain title, message, raw reasoning, project name/path, bearer or provider key。

## 10. 性能、容量与成本

| 项目 | 当前基线 | 候选目标/上限 | 测试方法 | 降级 |
|---|---:|---:|---|---|
| session metadata list | static sample | 1,000 rows P95 ≤200ms, page ≤50 | temp DB benchmark/query plan | smaller page, no body join |
| history first page | none | P95 ≤300ms；default 20/max 50 turns；metadata batch不读raw body | local integration benchmark/query count | page 20, defer raw expand |
| raw reasoning | fixed Runtime primitives、Host bounded v2、Desktop SQLCipher terminal repository及S8A authoritative reducer PASS；Vue rendering未实现 | 16KiB/delta、64KiB/part、128KiB/item、256KiB/turn；8 parts/item、8 items/turn | fake events + SQLCipher temp DB/fault benchmark；S8B visual/a11y later | explicit incomplete/unavailable；no silent truncation |
| input | Host hard 1 MiB | UI soft 64 KiB; hard remains 1 MiB | Unicode/byte boundary tests | block with count/error |
| event durability | process cache only | delta in memory；finalized/controlled interruption单transaction提交；no duplicate | fault injection | pause UI/reconcile |
| title | fixed fake-provider capability PASS；`MM-126-001` 单次 strict title PASS，production quality/stability仍待 Eval | ≤2 calls/session, input≤8KiB, output≤40 grapheme；production timeout在 G4 benchmark 冻结 | fake clock/provider + approved fixed Eval dataset | deterministic fallback |
| DB size | none | establish with 10k sessions/1M messages | synthetic benchmark | paging/retention future feature |

## 11. 配置、Feature Flag 与部署

| Flag | Default | Scope | Safe-off behavior |
|---|---|---|---|
| `VITE_YIJIE_CHAT_LOCAL_UI_ENABLED` | false / candidate not implemented | Desktop nav/router/component/store integration | no Chat/Tasks nav or route/loader/store bind；exact `true` only；不得在env/CI/default build设true |
| `YIJIE_CHAT_LOCAL_ENABLED` | false | Desktop Rust domain/SQLCipher | chat DB/domain unavailable；does not enable UI |
| `YIJIE_CHAT_LOCAL_HOST_ENABLED` | false | Desktop Rust sidecar | no Host child process；does not enable UI |
| `YIJIE_DESKTOP_CHAT_RAW_REASONING_ENABLED` | false | Desktop/Host | raw capability unavailable；不以状态/时长冒充功能通过 |
| `YIJIE_DESKTOP_CHAT_TITLE_MODEL_ENABLED` | false | Host/Desktop | deterministic fallback only |
| `YIJIE_DESKTOP_CHAT_DELETE_ENABLED` | false | Desktop/Host | hide/disable destructive operation with reason |
| `YIJIE_API_SECURE_TASKS_ENABLED` | false | approved service profile | legacy routes remain unregistered/ingress denied |

- 配置验证：unknown/unsafe combinations fail startup/readiness；reasoning/title/delete不能单独绕过 base chat/contract pin。
- 新旧版本共存：contract/DB expand first；no new output before consumer tolerance；legacy Public route remains isolated。

## 12. AI 功能专项

### 12.1 Runtime/MiniMax 能力矩阵

| 能力 | pinned Runtime canonical evidence | 当前 Agent Host | MiniMax/真实 evidence | G2 结论 |
|---|---|---|---|---|
| text thread/turn/resume/interrupt | stable methods/source | 已暴露 4 methods | 2026-08-01 真实短 turn/resume/interrupt PASS | baseline only；不等于 FEAT-126 完成 |
| persistent thread delete | `thread/delete` README/schema/source/v2 tests；固定 `codex-cli 0.144.6` temp-home 验证 response/event/row/rollout/restart absence PASS | v2 cleanup等待`thread/deleted`确认并清除bbolt/v1-v2 replay/in-memory raw；保留30天content-free HMAC receipt | 0 model turn/无 MiniMax；Runtime WAL/log仍可能存在字节残留 | Host foundation PASS；Desktop/Host/Runtime完整saga留待S10；forensic erase仍不承诺 |
| raw model reasoning | canonical `reasoning/textDelta` + completed raw content已存在；raw delta/history/interleaving/interruption fixed fixtures 4/4 PASS；MM-126-002观察到7 delta + 1 raw completed part | v2闭合事件、caps、completed对账与partial/unavailable fake fixtures PASS；正文不落bbolt/log | 旧public-summary门槛FAIL；同时证明单样本raw事件存在，不证明稳定/安全/完整E2E | Q-009/Q-016 Resolved；S5/S6 foundation PASS，UI reducer与完整Gate仍待S7/S9–S10；flag默认off |
| supplied thread name | `thread/name/set` 存在 | 未暴露 | N/A | 只存名称，不是自动标题能力 |
| isolated model title | pathless ephemeral + `turn/start.outputSchema` 与 per-turn-only fake fixtures PASS；ephemeral 不可 `thread/delete` | v2 title operation已实现pathless/ephemeral/provider-model校验、strict schema、事件隔离、40-grapheme sanitizer与内存幂等；flag off | `MM-126-001`历史证据：1 call/0 retry、completed、strict object + 18-grapheme sanitizer PASS、0 tool/secret leak；本轮0调用 | S5 foundation PASS；Desktop precedence/UI与后续Eval仍待S7/S9 |

Owner 批准的两个 MiniMax 合成短请求已各执行一次且 0 retry，总 hard cap=2 已耗尽。执行使用固定
Runtime/Host pin、临时 `CODEX_HOME`/空 cwd/pathless ephemeral thread，title PASS、public-summary在历史门槛下FAIL且观察到raw reasoning；
不得新增第三次调用或以重复计费“跑到成功”为证据。usage/latency/脱敏断言见 `08-verification-report.md`。

- 改变 AI behavior：是；新增title prompt/structured output与raw reasoning display，因此需固定pin、raw availability/content/security Eval。
- Model/provider：当前候选沿用 pinned MiniMax-M3 via Responses；不新增 picker。
- Title schema：strict object `{title:string}`；post-parse NFC single plain-text title，1–40 grapheme，no newline/control/bidi/Markdown/HTML；fixed `title-v1`；first user input≤8KiB and treated as untrusted data。
- Title trigger：first valid terminal answer only；job isolated from conversation thread；same session/job idempotent；人工 rename cancels/ignores model result。
- Fallback：first non-empty user line normalized/safely truncated；generic “新任务”只在无可用文本时使用。
- Reasoning：versioned v2只投影受控raw text delta/finalized reconciliation；纯文本、不可信、不进logs/telemetry/audit；missing/invalid不能静默降级。API/Host/Desktop投影统一锁定`29317b...`；S7A Rust SSE/domain parser与S7B reducer/restart/terminal persistence已通过，Vue纯文本展示仍属S8。
- 无答案/拒答：assistant refusal persists as answer state；title still bounded；不能自动提升 permission/tool。
- 提示注入：adversarial title/reasoning dataset must prove schema/sanitization and no secret/system prompt leakage。
- Eval 引用：`06-test-plan.md` §9。

## 13. 方案比较

| 方案 | 优点 | 缺点 | 风险 | 结论 |
|---|---|---|---|---|
| A. Vue localStorage + direct Host | 快 | confidential data/transaction/migration/token/path 边界弱 | critical | Reject |
| B. Host bbolt 保存全部 conversation | 接近 Runtime | 违反 Host 薄适配职责，业务 schema/租户/UI migration 耦合 | high | Reject |
| C. Desktop Rust SQLCipher + narrow commands + Host mapping | 清晰 authority、事务/懒加载/删除可测、未来 storage port | 新依赖、Keychain/migration/checkpoint 性能需验证 | medium | Selected by ADR-0013；details Accepted in ADR-0014 |
| D. 每 turn 双写 Public API/cloud DB | 早接云 | 违反本期 local-only，双写一致性/隐私/生产依赖显著扩大 | critical | Reject for this feature |

## 14. ADR 与批准

- ADR：现有ADR-0012继续约束Public Tasks；ADR-0013/0014/0015/0016于2026-08-02 Accepted。ADR-0016取代ADR-0015的public-summary-only/raw-drop/时长降级部分；title隔离继续有效。
- Delete/security：DEC-126-006 Accepted，Q-006/Q-015 Resolved；S7C已在Desktop Rust/SQLCipher schema v4实现持久化cleanup job、独立receipt HMAC、原子delete/turn lease、restart coordinator、级联删除/WAL checkpoint与30天content-free receipt；跨四组件E2E仍未执行。
- Runtime/MiniMax：canonical delete/name/summary/raw reasoning/outputSchema已确认；两次历史MiniMax预算已执行，title PASS，MM-126-002在旧summary门槛FAIL且观察到raw事件；Host raw bridge基础已用fake Runtime实现，raw flag默认off，本轮未调用MiniMax。
- Public Tasks：仓内consumer inventory完成，unknown external按safe compatibility category处理，Q-010 Resolved；DEC-126-011/012已Accepted，v1全程双隔离。DEC-126-023/024与Q-017已关闭，`29317b...`从schema层拒绝conversation正文并通过G2A重审；LIA-126-002现已恢复，仅允许关闭S4–S6 P1。
- Desktop Pattern：FEAT-126 Chat/App Shell Pattern已Accepted，只取代Chat 1.1.0/App Shell 2.0.0中的FEAT-126冲突段落。
- 技术负责人：段成威 — G2/G2A Re-review Passed；DEC-126-023–032 Accepted；S4–S8A Closure Passed；S8B0 Closure候选已完成并提交DEC-126-033，S8B与S9–S11 Pending/Unauthorized。
- 安全/数据 Owner：段成威 — ADR-0013/0014/0015/0016与DEC-126-005/006/007/011/012/014/015/016/017 Approved；Q-006/Q-007/Q-008/Q-009/Q-010/Q-015/Q-016 Resolved；Pattern Accepted。
- 结论与日期：2026-08-03 G2/G2A保持Passed，DEC-126-030/031接受S7C/S8A，DEC-126-032接受S8B0设计并授权后形成本地Closure候选。G3仍Partial；DEC-126-033批准前不得开始S8B，且继续禁止S9–S11、MiniMax、flag启用与追加远端动作。
