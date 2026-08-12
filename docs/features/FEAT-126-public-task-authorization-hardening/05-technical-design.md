# FEAT-126 技术设计（DESIGN-126-021 Complete / LIA-126-036 Two-stage Corrective Authorized / G3 Partial）

> 本文产品/架构设计保持G2 Passed。DEC-126-057已接受S10BF1 Closure并关闭`S10B-BLK-005`；Owner随后单独授权并消费LIA-126-020/S10B-R5。R5的S10B-001通过，但S10B-002在API readiness前因runtime service-profile authority不一致而fail closed；DEC-126-058 Option A已Accepted并拒绝R5 Closure，Owner随后单独授权、消费LIA-126-021/S10BRP1。Owner于2026-08-06批准DEC-126-059 Option A，S10BRP1 Closure Passed并关闭`S10B-BLK-006`；API/Infra已形成clean local checkpoints。LIA-126-022/S10B-R6随后被正式消费，但在S10B-001 image resolver阶段以`preflight_image_resolver_failed`停止；S10B-002–012未运行。DEC-126-060/061 Option A均已Accepted；LIA-126-023/S10BEP1 repository implementation、2026-08-09的S10BEP1-014 isolated live验证及Infra/Governance全量门禁均PASS。Owner通过DEC-126-062接受Corrective Closure并关闭`S10B-BLK-007`，随后通过DEC-126-063仅形成Infra/Governance本地clean checkpoints。G3保持Partial，fresh R7、S11/MiniMax、默认flag activation与远端动作仍未授权。
> 本文产品/架构设计保持G2 Passed。DEC-126-057已接受S10BF1 Closure并关闭`S10B-BLK-005`；Owner随后单独授权并消费LIA-126-020/S10B-R5。R5的S10B-001通过，但S10B-002在API readiness前因runtime service-profile authority不一致而fail closed；DEC-126-058 Option A已Accepted并拒绝R5 Closure，Owner随后单独授权、消费LIA-126-021/S10BRP1。Owner于2026-08-06批准DEC-126-059 Option A，S10BRP1 Closure Passed并关闭`S10B-BLK-006`；API/Infra已形成clean local checkpoints。LIA-126-022/S10B-R6随后被正式消费，但在S10B-001 image resolver阶段以`preflight_image_resolver_failed`停止；S10B-002–012未运行。DEC-126-060/061 Option A均已Accepted；LIA-126-023/S10BEP1 repository implementation、2026-08-09的S10BEP1-014 isolated live验证及Infra/Governance全量门禁均PASS。Owner通过DEC-126-062接受Corrective Closure并关闭`S10B-BLK-007`，随后通过DEC-126-063仅形成Infra/Governance本地clean checkpoints。Owner继续接受DEC-126-065 Option A并授权LIA-126-025/S10BO1；四仓repository corrective、S10BO1-001–014及全部实现/Governance门禁PASS，DEC-126-066现已接受Corrective Closure并关闭`S10B-BLK-008`。G3保持Partial，isolated live、fresh R8、S11/MiniMax、默认flag activation与远端动作仍未授权。
> 后续LIA-126-024/S10B-R7已单独授权和消费；§38保留S10B-001 PASS、S10B-002 fail-closed及当时`S10B-BLK-008 Open`的历史事实。§39–§40完成设计、实现与全量门禁，DEC-126-066只接受repository Corrective Closure，不构成fresh R8、G4或G6证据。
> DEC-126-067随后只授权local clean checkpoint closure：API、Host、Desktop、Infra及Governance本地checkpoint已形成；Contracts/Runtime不变。该checkpoint不构成isolated live、fresh R8、G4或G6证据。

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
| Vue | S8B只消费真实S8A store；production source禁止mock transport | LIA-126-006已按此边界实现；fake transport仅存在test harness，production bundle扫描无mock/harness |

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

Owner已接受DEC-126-030/031/032/033；LIA-126-005 / S8B0 Closure Passed。S8B仍须单独授权，不得自动进入。

### 2.4 DESIGN-126-006 — S8B0 UI Integration Readiness（Accepted / Implemented Candidate）

状态：DESIGN-126-006/DEC-126-032已获Owner接受，LIA-126-005已在`yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85`关闭以下S8B0集成缝隙，DEC-126-033已接受其Closure。完整S8B Vue UI已在`35f27447398529cca4dec85fa1f67e779c7a7cbd`实现，并由DEC-126-034接受Closure。

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
- Schema、Rust serde/registry、TS validator/client/store及fixed fixtures已按单独LIA-126-005完成；所有flags继续off，DEC-126-033 Accepted也不自动启用。

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
- 技术负责人：段成威 — G2/G2A Re-review Passed；DEC-126-023–055 Accepted；S4–S9及S10E/P1/P2F/P3/S10BP1/S10BR1/S10BM1/S10BD1 Closure Passed；LIA-126-016/S10B-R3 Closure Fail；S10B-R4/S11 Unauthorized。
- 安全/数据 Owner：段成威 — ADR-0013/0014/0015/0016与DEC-126-005/006/007/011/012/014/015/016/017 Approved；Q-006/Q-007/Q-008/Q-009/Q-010/Q-015/Q-016 Resolved；Pattern Accepted。
- 当前结论与日期：2026-08-05 G2/G2A保持Passed，S4–S9与S10E/P1/P2F/P3/S10BP1/S10BR1/S10BM1/S10BD1 Closure Passed、BLK-001–005及S10B-BLK-001–004 Closed；LIA-126-016仍为S10B-R3 Closure Fail。DEC-126-055 Accepted，G3 Partial。S10B-R4/S11、MiniMax、默认flag启用与追加远端动作继续禁止。

## 15. S8B Vue projection implementation

```text
YjAppShell fixed Chat sidebar
  -> ChatSidebarTree
     -> authoritative Pinia session/project actions
  -> ChatPage /chat | /chat/:sessionId
     -> ChatComposer (pure text + project + read-only policy)
     -> ChatReasoningDisclosure (literal raw text)
     -> useChatScroll (48px follow / 160px control)
     -> stable readiness/error/cleanup projections
```

- 页面不持有owner、tenant、bearer、SQLCipher key、canonical project path、Host/Runtime ID或raw wire；authority/context继续由Rust和Pinia生命周期绑定。
- 新建与回复统一通过store action；sequence gap、stale selection、late event、restart/resync、delete/interrupt race继续由Accepted reducer处理，Vue不复制第二状态机。
- reasoning历史按turn展开后懒加载；live reasoning流式展开；terminal/incomplete/unavailable明确区分，所有正文使用`white-space: pre-wrap`文本节点。
- 删除确认不乐观移除；store的`DeleteDisposition`仍是唯一导航依据。项目只有pin/remove，session只有select/rename/pin/delete。
- Chat active时App Shell固定展开且不展示sidebar toggle，避免引入需求明确排除的显示/隐藏功能；200% zoom等价视口使用窄sidebar和纵向滚动保持操作可达。
- 测试视觉harness位于独立test Vite root，仅挂载生产组件/真实Pinia与固定合成投影；production entry和bundle均不可达。

## 16. DEC-126-035 remote state 与 LIA-126-007/S9 实际设计

- Remote state：DEC-126-035已接受五仓精确可达事实；S9两个新checkpoint仅本地且未push。远端可达不是runtime pin，也不构成merge/release/activation。
- Eval authority：Host仓维护`feat126-title-raw-v1`版本化合成dataset manifest与deterministic fake-provider runner；Desktop只消费exact event corpus验证下游链，不形成第二套provider语义。
- Dataset freeze：200 multilingual、50 adversarial、holdout=50（20%）；runner在执行前校验manifest/dataset/split/schema/runner/generator/fixtures SHA-256，漂移即停止。
- Title metrics：`title-v1` strict schema/sanitizer 100%，labeled semantic success≥95%，late result overwrite=0，injection/HTML/control/secret/extra action=0。
- Raw metrics：具体非空plaintext、sequence/item/content-index连续、delta/final snapshot对账；missing/gap/invalid/oversize为Gate FAIL；no execution/no-log/no-bbolt/no-telemetry/no-audit-body为0泄漏。
- 实际结果：title schema/sanitizer 250/250、语义200/200、unsafe拒绝50/50；raw valid 210/210、四类负例40/40；Desktop decoder/reducer/SQLCipher restart/history/delete与Vue plaintext projection通过。
- 授权停止线：S9已耗尽授权；DEC-126-036已接受但不自动授权S10。MiniMax、flags、production行为、central/private wire和远端动作仍禁止。

## 17. DESIGN-126-007 — S10A Local E2E Readiness & Test Profile（Accepted by DEC-126-037）

### 17.1 目标、基线与影响

S10A只冻结未来S10B的进程编排、隔离边界、证据格式和停止条件。`contract-impact = none`：本轮不修改HTTP/SSE/private IPC/Runtime、schema、默认配置或production行为，用户可观察行为不变。

| Component | 固定完整SHA | 分支 | S10A开始状态 |
|---|---|---|---|
| Governance | `276f88718eb4146ff5d82cc88a04548d3e1ce1d0` | `feat/feat-126-foundation-closure` | clean / exact |
| Contracts | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | `feat/feat-126-content-free-candidate` | clean / exact |
| API | `a64f9f591fb594818c1778e30c6941e2574b3264` | `feat/feat-126-foundation-closure` | clean / exact |
| Host | `8707dea552cff74121b89aa8045f27da2c8c9378` | `feat/feat-126-foundation-closure` | clean / exact |
| Desktop | `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb` | `feat/feat-126-foundation-closure` | clean / exact |
| Runtime | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | `develop` | clean / exact |

Runtime现有artifact为`codex-cli 0.144.6`，binary SHA-256=`1ef4f1daba0c5ac267e9bf661d129c3dfc59ffe5cd9ab7767b22a1e9508df1fe`，manifest SHA-256=`2560a3171625765b0a62c685950e0c5df3cebfbe2b00635d3a13db2354276682`，target=`aarch64-apple-darwin`。S10A只执行`--version`与摘要校验，没有启动app-server。

### 17.2 当前环境与代码停止事实

| ID | 只读事实 | 对S10B的影响 | 处置 |
|---|---|---|---|
| S10A-BLK-001 | S10A历史观察为`docker compose`不可用；S10P0定位stale link，S10E完成discovery/profile/migration/identity/TLS/no-log/cleanup | isolated PostgreSQL + Keycloak + Caddy拓扑已可复验 | **Closed by DEC-126-039**；不等于S10P1/S10B授权 |
| S10A-BLK-002 | Host只接受空provider或`minimax`；`StartThread`在MiniMax未配置时fail closed，MiniMax base URL硬编码为`https://api.minimaxi.com/v1` | 固定fake Responses provider无进程级注入面；S9 in-process runner不是真实Host→Runtime provider | 触发provider-config停止条件；不使用MiniMax/真实key绕过 |
| S10A-BLK-003 | Desktop sidecar使用`env_clear()`，并把Host raw/title/cleanup三个flag设为`false`；stdout/stderr丢弃到null | 父进程临时exact-true不会到达Host child，且无法生成Host日志/进程证据 | 触发private deployment-interface停止条件；不“假开启” |
| S10A-BLK-004 | S10P2源码已把Chat DB/receipt/native-auth切到run-derived test namespace，独立gate、manifest、exact inventory与cleanup已通过仓内门禁；但本机没有Apple Development identity/profile/entitlement，Protected Data写入返回required entitlement missing | DEC-126-042判定Local-only目标不应被native signing阻断；LIA-126-011完成严格file backend实现与验证 | **CLOSED by DEC-126-043 Option A**；signed proof保持Deferred Native Hardening / NOT RUN |
| S10A-BLK-005 | 历史盘点时Desktop chat流使用本地UUID作task/session ID并调Host `/v1/tasks/{id}/agent-sessions`；`/v2/tasks`只有generated types，无consumer call | LIA-126-012/S10I已补齐并验证“Desktop新建→Public Tasks/PostgreSQL→Host”真实主链 | **Closed by DEC-126-045**；不等于S10B授权 |
| S10A-LIM-001 | title v2因固定Runtime无法capability-disable tools而必定fail closed | S10只能验证deterministic fallback + user rename precedence，不能声称model title E2E | 不阻断fallback用例；title flag必须false |

结论：五项历史readiness blocker均已关闭：DEC-126-039关闭BLK-001，DEC-126-040关闭BLK-002/003，DEC-126-043关闭BLK-004，DEC-126-045关闭BLK-005。Owner随后单独批准并正式执行LIA-126-008；执行发现的`S10B-BLK-001/002`已由DEC-126-048/050关闭。当前`S10B status = EXECUTED / BLOCKED / CLOSURE FAIL`，直到另行授权的fresh rerun通过；该状态不回退G2/G2A或已接受Closure，G3仍Partial。

### 17.3 PostgreSQL / OIDC 方案比较

| 方案 | 能力 | 优点 | 代价/风险 | 当前结论 |
|---|---|---|---|---|
| A. 补齐Compose v2，使用`yijie-infra`显式local profile | loopback PostgreSQL 16 + dedicated `yijie_api_feat125_local` + pinned Keycloak/Caddy/TLS/CA + synthetic identities | 拓扑、issuer、JWKS、CA、端口与清理责任已有权威runbook | 需单独批准安装/enable plugin；可能下载镜像、创建volumes；停止不删volume | **推荐**；当前未具备，S10A不执行 |
| B. 已存在的隔离PostgreSQL | 只在empty dedicated DB、migration、loopback、synthetic-only时解决API DB | 若已由Owner维护，无需再启容器 | PostgreSQL不提供Keycloak/JWKS/Caddy/CA/bearer lifecycle；当前5432也无listener | **当前不可用，且单独不足以支撑S10**；必须同时有等价exact local IdP/TLS profile |

禁止复用个人/真实数据库、手工insert授权状态、关闭permission projection/JWKS或跳过migration。

### 17.4 未来process manifest（冻结候选，当前不运行）

S10B必须在owner-only `RUN_ROOT=$(mktemp -d "${TMPDIR%/}/feat126-s10b.XXXXXX")`下建立`bin/pid/log/evidence/codex-home/host-home/desktop-app-data/project`，全部目录`0700`。真实路径不得写入治理证据，只记录role、owner/mode检查和SHA-256。

| Order | Process/resource | 固定命令/控制面候选 | Port | Ready | Stop/cleanup |
|---:|---|---|---:|---|---|
| 0 | provenance | 六仓`rev-parse HEAD`/`status --short`；Runtime digest；Compose preflight | none | exact SHA/tool manifest | 任一diff即停止 |
| 1 | dependencies/IdP | Infra `make dev-up && make feat-125-local-api-db && make feat-125-local-up && make feat-125-local-status` | PG 5432；OIDC 8443；API edge 9443 | health + CA/realm conformance | `make feat-125-local-stop` + `make dev-down`；保留volume |
| 2 | migration/bootstrap | API `YIJIE_API_POSTGRES_DSN=<ignored DSN> make migrate-up`；四个tracked synthetic manifest逐一`make bootstrap-nonprod-authz BOOTSTRAP_PROFILE=feat-125-local-lab INPUT=<manifest>` | DB only | migration status + exact inventory/revision | 不手工回写schema |
| 3 | API | `go build -trimpath -o <RUN_ROOT>/bin/yijie-api ./cmd/api-server`；以local-lab profile、port 18080、permission/secure Tasks exact true、pinned issuer/JWKS/CA/DSN启动 | 18080 | `/healthz` + `/readyz` + signed synthetic auth | process-group SIGTERM，10s deadline |
| 4 | fake Responses | 后续批准的versioned loopback HTTP runner；当前**无命令** | reserved 18082 | health + fixture manifest hash | 记录call count/category only |
| 5 | Host binary | `go build -trimpath -o <RUN_ROOT>/bin/yijie-agent-host ./cmd/desktop-host`；Host由Desktop supervisor启动 | 18081 | health/ready + spawn nonce/version | BLK-002/003已由DEC-126-040关闭；首次S10B在更早bootstrap gate停止，Host未启动 |
| 6 | Desktop + Runtime child | Desktop以UI/native-auth/chat/host临时exact true及临时路径执行`pnpm tauri dev`；Host启动pinned Runtime | Vite 1420/1421；Host 18081 | closed readiness=`ready`，Runtime version/SHA exact | Desktop process-group SIGTERM；确认无残留child |

端口全部loopback；任一端口已被占用即fail closed，不随机漂移。process manifest记录role、PID/PPID、binary SHA-256、start/end monotonic time、port、ready摘要、exit code和cleanup result；不记录env value、bearer、DSN、DB key、正文或真实路径。

### 17.5 临时test profile

- Desktop：`VITE_YIJIE_CHAT_LOCAL_UI_ENABLED`、`YIJIE_CHAT_LOCAL_ENABLED`、`YIJIE_CHAT_LOCAL_HOST_ENABLED`、owner/tenant、Host binary/port/home、Codex binary/manifest/home，以及`YIJIE_DESKTOP_*` native-auth issuer/endpoints/client/API-origin/CA pin。
- API：`YIJIE_ENV`、`YIJIE_API_SERVICE_PROFILE`、`YIJIE_API_PORT`、PostgreSQL/Redis、permission/secure Tasks、issuer/JWKS/local CA path+SHA。
- Host：`YIJIE_ENV`、Host port/home/nonce、Codex binary/manifest/home、Host v2 raw/title/cleanup flags。fake provider只能用经批准的test-only loopback closed config，不得复用`YIJIE_MINIMAX_API_KEY*`。

所有boolean只有字符串`true`生效，只注入本次子进程，不写`.env`、CI、默认dev/build配置。退出后扫描tracked/untracked config与process，必须证明defaults仍off；证据只记录变量名和`set/unset`，不记录值。

### 17.6 S10B E2E 与content-free证据

| Test ID | 输入类别 | 预期状态 | 证据 | 失败类别 |
|---|---|---|---|---|
| S10B-001 | provenance/startup | exact SHA/version/nonce/ready，loopback only | process/readiness manifests | environment/process/readiness |
| S10B-002 | synthetic plain-text create | 项目→content-free Public Task→local session→conversation，仅1 session/turn | control-plane counts/hashes | chain/auth/duplicate |
| S10B-003 | assistant + valid raw stream | sequence/index/final exact，UI plaintext | event counts/final hashes/UI state | sequence/projection |
| S10B-004 | incomplete/interrupt | answer/reasoning终态一致，incomplete不冒充complete | state/count/hash | terminal mismatch |
| S10B-005 | history/page/restart | SQLCipher 20/50分页，restart/resume/resync | schema/page/cursor hashes | persistence/resync |
| S10B-006 | fallback title/rename/pin/sort | deterministic fallback；user rename永远优先 | source enum/count/order hash，无title文本 | title/order |
| S10B-007 | gap/reconnect/race | closed recovery/resync，无late commit | operation/cursor/outcome | race/resync |
| S10B-008 | permanent delete | Desktop/Host/Runtime/receipt清理，restart后不可读 | per-surface counts/receipt hash | cleanup/residue policy |
| S10B-009 | Public Tasks boundary | request/response/PostgreSQL/audit无正文/title/path | denylist hit counts + row hashes | data-boundary violation |
| S10B-010 | sink leakage | log/bbolt/audit/telemetry/URL/process output canary=0 | scanner/pattern hash/hit count | leak detected |
| S10B-011 | perf/capacity/fault | 达到06文档阈值，超限fail closed | timing/count/limit | performance/capacity |
| S10B-012 | final cleanup/default-off | 无listener/PID，temp清理，tracked defaults off | cleanup/config scan hashes | cleanup/default-on |

每个case只保存run ID、baseline IDs、fixture hash、时间、计数、枚举、布尔断言、耗时和失败分类。prompt/assistant/raw/title、secret、DSN、bearer、DB key、真实路径不得进入证据。canary只保留pattern SHA-256和hit count；命中即停止。

### 17.7 决策与授权出口

- DEC-126-037当时采用方案C并`HOLD S10B`；五项blocker关闭后，Owner于2026-08-05另行批准并执行LIA-126-008。该授权已在bootstrap停止条件处消费，不再授权纠偏或重跑。
- 先另行设计和授权S10P Test Profile/Chain Corrective，仅解决BLK-002–005：fake Responses进程注入、Desktop sidecar flags/log/PID、test-only Keychain/app-data namespace和Public Tasks content-free orchestration。它们可能修改production config/private IPC/业务编排，必须重走contract-impact审查，不能在S10A静默实现。
- BLK-001–005已分别由DEC-126-039/040/043/045关闭。LIA-126-008执行发现的S10B-BLK-001/002已由DEC-126-048/050关闭。不得省略profile、手工造状态、复用旧run volume或自动重跑S10B；fresh rerun仍需新审批。

## 18. DESIGN-126-008 — S10P0 Test Profile & Main-Chain Corrective（DEC-126-038 Accepted）

### 18.1 评审边界、基线与结论

S10P0仅作只读源码/环境盘点、设计冻结和治理文档更新；`contract-impact = none for this review`。本评审没有安装软件、启动进程/容器、打开flag、读写Keychain/数据库、修改业务源码或远端写入。

| Component | 固定完整SHA | 分支 | S10P0开始状态 |
|---|---|---|---|
| Governance | `0ceb04765f46a3ef1b992d859c3d1c6a83b43cfb` | `feat/feat-126-foundation-closure` | clean / exact |
| Contracts | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | `feat/feat-126-content-free-candidate` | clean / exact |
| API | `a64f9f591fb594818c1778e30c6941e2574b3264` | `feat/feat-126-foundation-closure` | clean / exact |
| Host | `8707dea552cff74121b89aa8045f27da2c8c9378` | `feat/feat-126-foundation-closure` | clean / exact |
| Desktop | `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb` | `feat/feat-126-foundation-closure` | clean / exact |
| Runtime | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | `develop` | clean / exact |

历史时点：DEC-126-037 Option C、S4–S9 Closure Passed与G3 Partial保持不变；DEC-126-039当时只关闭BLK-001，LIA-126-008仍为`Blocked Draft`。随后S10P1/P2F/P3逐项授权并接受Closure，Owner最终于2026-08-05单独批准LIA-126-008；S11和所有default activation仍须另行授权。

### 18.2 S10A-BLK-001：Compose/隔离身份环境

只读检查证明：Docker CLI `29.6.1`存在，当前用户CLI plugin entry是指向已失效AppTranslocation目标的symlink；Docker Desktop application bundle内的相对位置`Contents/Resources/cli-plugins/docker-compose`实际存在，版本`v5.3.0`，SHA-256=`2642b6354b323be90cf28460ac186499fbc85381b9ce5e6681fdefb2d0a7d265`。治理证据不记录当前用户的绝对路径或旧symlink target。直接调用该二进制的`version`、`config --no-interpolate --quiet`、`config --profiles`、`config --services`和`up --help`均通过；没有连接daemon或改变容器/镜像/volume。Docker官方的[Compose安装概览](https://docs.docker.com/compose/install/)将Docker Desktop列为macOS推荐获取方式，[Compose FAQ](https://docs.docker.com/compose/support-and-feedback/faq/)说明2025年发布的Compose v5使用同一`docker compose`命令且与v2功能等价；手动plugin安装文档只面向Linux。

| 方案 | 优点 | 风险 | 结论 |
|---|---|---|---|
| A. 下载/安装独立Compose v2 | 表面满足旧runbook版本用词 | macOS非官方推荐plugin安装路径，引入第二份二进制与新下载信任 | 拒绝 |
| B. 恢复Docker Desktop bundled plugin发现 | 无下载，可固定version/hash，与现有script的`docker compose`一致 | 需修改用户级symlink，必须可恢复且单独授权 | **唯一推荐** |
| C. 永久绕过CLI直调absolute binary或复用已有PostgreSQL | 不改symlink | scripts/make不同路；PostgreSQL不提供IdP/TLS/CA，且当前无等价listener | 拒绝 |

未来S10E必须先把旧symlink移到run-scoped owner-only backup，再建立指向上述精确Docker Desktop二进制的新symlink；修复后重跑version/hash/config/features。任一值漂移即停止；回滚删除新link并原子恢复备份，不修改Docker Desktop app或系统目录。

S10E不得复用普通`yijie_postgres_data`、`yijie_api`或任何现有数据库。已接受实施方案使用新的exact `feat-126-s10` Compose profile，不声明固定`container_name`，以canonical run UUID派生Compose project/resource名；只包含：

- API PostgreSQL和Keycloak PostgreSQL：`postgres:16.13-alpine@sha256:4e6e670bb069649261c9c18031f0aded7bb249a5b6664ddec29c013a89310d50`；
- Keycloak：`quay.io/keycloak/keycloak:26.7.0@sha256:0f198be292568439d700cdbfb893e69a6009bb43a94a06a945b1d3d506c76b13`；
- Caddy：`caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648`；
- 四个run-scoped volume：API DB、Keycloak DB、Caddy data、Caddy config。Redis/pgvector不在FEAT-126 S10运行链，不启动。

API DB从空库跑全部current migration；Keycloak只导入固定synthetic realm/user matrix。Caddy只绑定loopback 8443/9443，CA私钥保留在run volume；只把公开CA certificate导出到owner-only run root，API使用已有local-profile CA path+hash校验，Desktop使用显式CA配置，不写macOS系统/用户trust store。若本地缺少任一固定digest镜像，S10E必须报告精确缺口；未被S10E授权明确包含时不得pull。

### 18.3 S10A-BLK-002/003：Host fake Responses与Desktop child profile

Host线上默认仍只接受`minimax`/`MiniMax-M3`，默认base URL、key读取与Runtime pin均不改。S10P1候选只在以下条件全部成立时进入test transport：

```text
YIJIE_FEAT126_S10_TEST_PROFILE_ENABLED=true
YIJIE_FEAT126_S10_RUN_ID=<canonical non-zero UUID>
YIJIE_FEAT126_FAKE_RESPONSES_BASE_URL=http://127.0.0.1:18082/v1
```

URL必须精确为`http`、IP literal `127.0.0.1`、固定port 18082、path `/v1`，不得含userinfo/query/fragment或DNS hostname；任一非loopback值、未设run ID、同时出现MiniMax key、非local environment或单独设置子开关都fail closed。此profile继续使用on-wire provider/model identity `minimax`/`MiniMax-M3`，但Host写入managed CODEX_HOME的test-only provider config使用上述base URL、`wire_api=responses`、`requires_openai_auth=false`且不声明`env_key`；Runtime现有custom provider能力足够，不改pin。

fake HTTP authority仍由`yijie-agent-host`维护，只消费S9已锁定`feat126-title-raw-v1`fixture/manifest，对loopback提供`/healthz`与`POST /v1/responses`。它必须校验request上限、固定model/input category、调用次数和run ID，只记录fixture ID/hash、计数与稳定failure class，不记录request/response正文。不需要真实或合成API key。

Desktop supervisor保留`env_clear()`，只在同一exact test profile/run ID下向Host child增加closed allowlist：上述3个test变量、已有binary/manifest/home/port/instance nonce，以及
`YIJIE_AGENT_HOST_V2_RAW_REASONING_ENABLED=true`、`YIJIE_AGENT_HOST_V2_CLEANUP_ENABLED=true`、`YIJIE_AGENT_HOST_V2_TITLE_ENABLED=false`。title因固定Runtime无法能力级禁用tools而继续强制off。父进程只能从Rust验证过的run manifest得到路径/端口；WebView不接触flag、PID、Host/Runtime ID或路径。

Host stdout/stderr不再丢到null，而写入Rust在run root内创建的owner-only regular files（directory `0700`、file `0600`、no symlink/hardlink）。Desktop记录child PID/PPID、binary hash、nonce、start/end/exit到content-free manifest；不写env value、project path或正文。本方案不需新增/修改Tauri command、event、cursor或error；如S10P1实现时发现必须修改private IPC，立即停止并另提schema。

### 18.4 S10A-BLK-004：test-only Keychain/app-data

S10P2只在`YIJIE_FEAT126_S10_TEST_PROFILE_ENABLED=true`与独立`YIJIE_FEAT126_S10_SECURE_STORAGE_ENABLED=true`同时exact成立时接受与18.3相同的canonical run UUID；缺失/`false`保持S10P1/生产默认namespace，拼写错误或孤立子开关fail closed。不接受WebView或shell任意指定Keychain service/account。Rust内部由run ID派生并限长：

```text
com.yijie.ai.test.feat126.<run-id>.chat-db / default-v1
com.yijie.ai.test.feat126.<run-id>.chat-receipt / default-v1
com.yijie.ai.test.feat126.<run-id>.native-auth / refresh-token-family-v2
```

test namespace禁止native-auth legacy account fallback，防止读取真实`refresh-token-family`。`RUN_ROOT`是Rust校验的absolute、canonical、owner-only `0700`、non-symlink directory；Desktop app-data/Chat SQLCipher、Host Home、CODEX_HOME、receipt HMAC、native auth和临时项目都必须在同一run manifest中绑定该run ID。

启动前后inventory只检查上述三个精确service/account的`present/absent/schema-valid`，不枚举整个Keychain、不读取或hash secret。证据是namespace descriptor与status tuple的SHA-256；启动前必须全absent。正常退出顺序为Desktop→Host/Runtime→关闭SQLCipher→只删精确test Keychain items→再删run root；missing item幂等成功，任一namespace/run ID不一致则停止而不删。异常退出依赖owner-only cleanup manifest重试，绝不读/覆盖/删除无该run ID的现有Keychain条目。

S10P2是Desktop-private deployment/storage interface的additive改动，不改SQLCipher business schema、central contracts或private IPC。default profile的固定service/account行为保持不变，且受exact test profile的双重门禁。

### 18.5 S10A-BLK-005：Desktop→Public Tasks→Host主链

`29317b6426578749dc698fc2ad32b986ee5c8e9f`已能表达本主链的create/read、UUID `Idempotency-Key`、closed `TaskContentReferenceV2`与stable content-free error；无需修改central contract。它也明确声明permanent delete不在candidate内。DEC-126-038已接受对DEC-126-014“运行独立”部分的窄修正：会话正文/标题/路径仍绝对local-first且不上传，但每个新会话在Host start前必须成功创建一条content-free control-plane Public Task。

#### Authority与持久化

SQLCipher新schema候选`v5`增加`chat_public_task_bindings`，以`session_id`主键/FK cascade，只保存：

- 独立生成的`client_reference_id`（不等于local session/operation/path/body hash）；
- Desktop `create_operation_id`，同时作Public `Idempotency-Key`与Host trace operation ID；
- server返回后的`public_task_id`；
- closed state `pending|inflight|bound|blocked_auth|retry_wait|denied|failed`、attempt/lease/next retry/stable error code/timestamps；
- 不存bearer、prompt/message/raw/title/path、provider数据或HTTP body。

local session ID是Desktop唯一UI/history authority；Public task ID是API/PostgreSQL authority；Host的`task_id`必须精确使用已绑定的Public task ID；Host request trace使用同一`create_operation_id`。owner/tenant/capability由Rust的active native-auth context绑定并在每次调用前重验；bearer只由`NativeAuthRuntime`内部获取，不进SQLCipher/outbox/WebView/log。API 201响应的tenant必须匹配scope，creator必须匹配Rust-bound owner，input reference必须逐字段匹配，否则protocol fail closed。

#### 幂等、失败、恢复与删除

create transaction先写local session/user message、binding和已有create outbox；coordinator先POST `/v2/tasks`，只有binding=`bound`后才解析bookmark并启动Host。transport/503/500/unknown outcome使用相同idempotency key与canonical request重试；401进`blocked_auth`并等待同owner/tenant重登录；403进`denied`；400/409/schema mismatch进terminal `failed`；201返回后原子bind Public task ID。应用重启时只在同owner/tenant/revision重验后恢复pending/inflight/retry，不猜测unknown outcome。

delete-vs-create由现有session lease串行。删除开始后任何late Public Task响应都不得触发Host start；Desktop/Host/Runtime完成清理后级联删除本地binding/outbox。由于contract没有Public Task delete，API/PostgreSQL中已创建的content-free row和audit/idempotency retention依provider策略保留，不计入DEC-126-006的Desktop/Host/Runtime物理删除承诺。Owner已通过DEC-126-038接受这一限制；未来若要求Public row同删，必须重开G2A delete contract评审。

#### Desktop-private closed projection（shape已由DEC-126-038接受，实施未授权）

现有`ChatSession`和7个chat event variants无法稳定表达异步control-plane状态；不得让Vue从`queued`或readiness猜测。S10P3因此是`additive Desktop-private IPC impact`，提交不改现有22个command/7个event语义的窄方案：

```text
command: chat_get_session_control_plane_v1
request: { schemaVersion: 1, requestId, contextId,
           payload: { sessionId } }
response.data: { sessionId,
  state: pending|bound|blocked_auth|retry_wait|denied|failed,
  issueCode: null|chat_unauthenticated|chat_capability_denied|
             chat_temporarily_unavailable|chat_conflict|chat_protocol_error,
  retryable: boolean,
  recovery: none|sign_in|retry|resync }

channel: yijie.chat.control-plane.event.v1
event: { schemaVersion: 1, sequence, sessionId,
  state, issueCode, retryable, recovery }
```

两个object都`deny_unknown_fields`/closed，`sequence`在Rust侧单调，gap/duplicate/stale context强制command resync；不包含Public task/client reference/operation/owner/tenant/Host ID、path、body或raw wire。Rust serde、JSON Schema、golden corpus、TS validator/client/Pinia authoritative reducer和UI稳定文案必须同一切片实现；Vue仍只调Pinia action。任何超出上述schema的需求先停止并重新审批。

### 18.6 切片影响、门禁与退出条件

| Slice | 关闭blocker | Contract-impact | Production/default-off | 必须证据 | 回滚 |
|---|---|---|---|---|---|
| S10E | BLK-001 | deployment/Infra config only；central/private wire none | 新profile显式选择，普通`dev-up`不启动 | Compose version/hash/config，digest images，run-scoped project/volume，migration/identity/TLS/no-real-data/cleanup | 恢复plugin link，只停本run project，不删未列入manifest的volume |
| S10P1 | BLK-002/003 | additive Host/Desktop private deployment config；IPC/central/Runtime none | master exact-true + local + run ID三重门禁；default MiniMax不变 | fake protocol/oversize/nonloopback/key-conflict，child env/log/PID/nonce，no-log，crash/restart/default-off | 关闭master profile，恢复Host默认config和null/no-start路径 |
| S10P2 | BLK-004 | additive Desktop-private storage/deployment interface；DB schema/IPC/central none | master与secure-storage必须分别exact `true`；任一缺失/false使用原固定namespace | pre/post exact inventory，wrong run ID，legacy-no-fallback，abnormal-exit/restart/cleanup/no-real-item-access，signed Protected Data write/read/delete | 只删manifest中本run items和run root，默认namespace不动 |
| S10P2F（LIA-126-011实施/DEC-126-043 Accepted） | Local-only BLK-004 Closed | `semantic` Desktop-private test storage/deployment；central contracts/G2A N/A | S10 master与`YIJIE_FEAT126_S10_EPHEMERAL_SECRET_BACKEND_ENABLED`必须分别exact `true`；任一缺失/false完全保持当前Protected Data默认 | 三个CSPRNG synthetic secrets、same-run restart、cross-run、wrong owner/mode/nlink/symlink/manifest、partial write/crash/recovery、no-log/process-output/evidence、exact cleanup/default-off均PASS | 关闭独立flag即回到当前Protected Data路径；只unlink匹配manifest的三个test files和run root；不承诺法证擦除 |
| S10P3 | BLK-005 | semantic Desktop orchestration + SQLCipher v5 + additive private command/channel；central wire none | Chat flags仍default-off；API secure Tasks只在local profile exact true | schema/serde/TS conformance，auth/tenant/revision，idempotency/unknown/restart/race，Public DB/no-log/migration/cascade/retained-row disclosure | flag off；forward migration保留；停coordinator；不删或猜测Public row |

DEC-126-038–052已由Owner接受；S10E/S10P1/S10P2F/S10P3/S10BP1/S10BR1/S10BM1 Closure Passed，详见§19/20/23/24/27/28/30，BLK-001–005及S10B-BLK-001/002/003 Closed。LIA-126-014 fresh S10B-R2在S10B-001 migration wrapper candidate门禁处fail closed；该历史Closure Fail不变。LIA-126-016必须在clean Governance SHA形成后单独审批。

### 18.7 安全、migration、restart、cleanup与race矩阵

| 类别 | 必测情形 | Gate |
|---|---|---|
| closed config | master false/missing/typo，run ID invalid，nonloopback/hostname/redirect/proxy，MiniMax key与fake同时存在 | 全部fail closed；默认行为逐字段不变 |
| no-log | synthetic prompt/raw/title/path/token/DB-key canary扫Host/Desktop/API logs、bbolt、audit、URL、process output和evidence | 正文/secret/path命中数`0` |
| migration | clean v5、populated v1–v4→v5、重复启动、只读/满/损坏/wrong-key，FK/cascade/foreign_key_check | 无正文进binding，失败不绕过/不降级 |
| restart | Public create前、request inflight、201后未bind、bind后Host未start，Keychain cleanup中断，child崩溃 | 同operation恢复，无重复Public/Host session，无真实namespace触达 |
| race | create-vs-delete、logout/tenant/revision-vs-retry、late 201、Host start-vs-delete、同run ID重启/异run ID并发 | 只有Rust authority能推进；delete后不启Host；cross-run/cross-tenant零可见 |
| cleanup | normal/abnormal exit，missing item/volume，manifest mismatch，stale PID/listener，Public row retention | 只处理manifest target；无残留process/port/test Keychain；Public retained row仅closed fields |

### 18.8 审批出口

Owner已批准DEC-126-038方案B并接受DEC-126-039/S10E Closure，只关闭BLK-001。后续仍须按`S10P1 → S10P2 → S10P3 → LIA-126-008/S10B`逐项单独授权和接受Closure；不允许并跳。

## 19. S10E Compose/Isolated Identity Environment 实际实现（DEC-126-039 Accepted）

### 19.1 Source与运行边界

- Infra authority：本地分支`feat/feat-126-s10e`，checkpoint `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf`，parent `f040492e7c4af4aa7cc94a343140c58befae3af2`；worktree clean、未push。
- private deployment interface为additive：新增显式`feat-126-s10` profile、runbook、secret/static/runtime validators；普通`dev-up`不会启动该profile。central contracts、API/Host/Desktop业务源码、private IPC、Host/Public Tasks wire与Runtime pin均未修改。
- Compose discovery只修复当前用户级link：旧stale link进入owner-only `0700`备份，新的link指向Docker Desktop bundled Compose `v5.3.0`；固定size=`30,780,320`、SHA-256=`2642b6354b323be90cf28460ac186499fbc85381b9ce5e6681fdefb2d0a7d265`。未修改Docker Desktop application或系统目录。
- 所有镜像均从本地exact digest解析，`up --pull never`；没有pull/download。PostgreSQL exact content只补了固定`16.13-alpine`本地tag，使digest-qualified reference可被Compose fail-closed解析。

### 19.2 隔离拓扑

- 每个canonical UUIDv4 run派生独立Compose project、owner-only ignored run root、四个named volumes和四个networks；不设置`container_name`，不复用普通/FEAT-125 DB或volume。
- API PostgreSQL只发布`127.0.0.1:5432`；它同时加入private DB network和project-scoped host bridge，因为Docker Desktop不会为internal-only network建立host publisher。仍不使用host network、shared external network或非loopback bind。
- Keycloak DB无published port；Keycloak只在identity/proxy internal network；Caddy只发布`127.0.0.1:8443/9443`，read-only root、drop all caps后仅保留`NET_BIND_SERVICE`，不安装系统/用户CA trust。
- secret为五个互异256-bit值、owner-only regular file `0600`；runtime verifier不读取/输出container env，只在进程内比对exact secret是否进入container logs。

### 19.3 失败、恢复与接受证据

一次初始诊断run因ad-hoc rendered Compose输出展开了synthetic API DB credential，被整轮判为无效。它未进入source/Git/governance；该run立即停止并移除containers/networks，credential弃用。新的fresh run重新生成secret和全部接受证据，避免用“后补扫描”掩盖污染。

fresh run证据：四服务healthy；exact image/label/security/network/volume/port inventory PASS；public CA单证书且无private key；OIDC issuer精确为`https://localhost:8443/realms/yijie-local`；Caddy legacy Tasks边界返回404；两名synthetic users连续两次provision一致；固定API `a64f9f591fb594818c1778e30c6941e2574b3264`从empty DB应用`00001–00004`到v4，第二次migration为no-op；candidate files与container logs中generated credential命中为0。

停止后两次run均为0 container、0 network、0 `5432/8443/9443` listener。因没有volume/secret删除授权，八个project-scoped named volumes与两个owner-only ignored run root保留；未执行`down --volumes`、volume rm或prune。污染run root含`0600 REJECTED` marker，Compose start/config/export、provision、migration与runtime verification均fail closed，仅status/stop可用于围堵。它们不是活动服务，但在Owner另行精确授权清理前必须保留并披露。

DEC-126-039已按方案A接受S10E并关闭BLK-001。该接受不自动授权S10P1、S10P2、S10P3、S10B、S11、MiniMax、flag activation或任何远端动作。

## 20. S10P1 Host Fake Provider与Desktop Child Test Profile实际实现（DEC-126-040 Accepted）

### 20.1 Source与contract-impact

- Host checkpoint：`yijie-agent-host@e0a8d3d29a335571d1654d95e1e262c240755674`，parent `8707dea552cff74121b89aa8045f27da2c8c9378`；Desktop checkpoint：`yijie-desktop@fba934c524852719904657d0a4155142040e7285`，parent `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb`。两者均在`feat/feat-126-foundation-closure`、clean、仅本地、未push。
- `contract-impact = additive private test deployment configuration`。没有新增或修改Tauri command/event/cursor/error、TypeScript validator、Vue、central contracts、Public Tasks/Host wire、数据库schema或Runtime pin。
- default路径逐字段保持：test master缺失或不为exact `true`时 subordinate变量fail closed；Host原MiniMax配置和Desktop原raw/title/cleanup=false、stdout/stderr=null路径不变；`.env`、CI、默认开发/构建配置未改。

### 20.2 Host test-only fake Responses

- 只有`YIJIE_FEAT126_S10_TEST_PROFILE_ENABLED=true`、canonical non-zero run UUID、`YIJIE_ENV=local`、exact `http://127.0.0.1:18082/v1`、raw/cleanup=true且title=false同时成立才启用；hostname、非loopback、端口/path/query变化、父PID/log manifest不匹配、MiniMax key/provider共存全部拒绝。
- managed临时CODEX_HOME继续以`minimax`/`MiniMax-M3`作为固定Runtime所需on-wire identity，但`requires_openai_auth=false`、无`env_key`、无Authorization；只附带run ID和固定fixture ID header，因此不会读取真实或合成MiniMax key。
- `yijie-agent-host`新增唯一fake HTTP authority，嵌入并校验S9 `feat126-title-raw-v1` manifest/dataset SHA；loopback handler只接受bounded JSON/stream/fixed model/input category/call cap，提供complete、incomplete、HTTP error、disconnect与oversize固定行为。Snapshot只含fixture ID、dataset SHA和接受/拒绝计数。
- 固定Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`实际完成一次合成turn：assistant delta、raw reasoning delta/final、item completed、turn completed和thread delete全部通过；调用MiniMax/外部网络次数为0。

### 20.3 Desktop child profile与进程证据

- Rust supervisor保留`env_clear()`，只向Host child传递批准的local/port/Home/Runtime artifact、instance nonce、test master/run ID/fixed loopback、parent PID、run-scoped log/process manifest及raw=true、cleanup=true、title=false。allowlist中不存在MiniMax key、bearer、SQLCipher key或WebView authority。
- `RUN_ROOT`、Host Home、CODEX_HOME和日志目录必须absolute canonical、non-symlink、当前owner且目录`0700`；child stdout/stderr文件为`0600`、各最多256 KiB，超额继续drain但只记`truncated=true`。
- `process.json`只含schema、run ID、role、PID/PPID、Host binary SHA、instance nonce、start/end、closed state/exit、字节数和truncation；原子临时文件使用唯一UUID，crash遗留不会阻断下一次更新。manifest不含路径、env value或正文。
- readiness同时核对本次child PID（Host通过parent PID校验）、run ID（Host test config）、instance nonce（health/ready header）；旧nonce、旧port、端口占用、非法run root、活跃stale PID均fail closed。Desktop在spawn前先写`prepared` evidence；Host test profile每100ms校验父PID，Desktop被强制终止后Host主动退出，下一次启动再把stale evidence闭合。正常stop、spawn失败、启动超时、unexpected exit、Desktop restart与同supervisor重启均有测试。

### 20.4 Closure判定与剩余边界

Host contract-check/lint/vet/shell、全量`go test -race -cover ./...`、build和固定Runtime集成通过；Desktop generated-contract check、ESLint/vue-tsc/fmt/clippy、165/165 TypeScript、101/101 Rust（另1个既有且未执行的Keychain integration）、Vite build、Rust build和真实Desktop→Host→固定Runtime child启动通过。raw/secret/path/bearer/database-key在已覆盖Host log、bbolt、Desktop child stdout/stderr、process output和evidence中命中为0。

因此S10P1授权范围内没有剩余P1；Owner已正式接受DEC-126-040，S10P1 Closure Passed，BLK-002/003 Closed。该决定当时未触碰BLK-004/005；后续结果见§21–25。S10P3 Closure后来通过，LIA-126-008也已单独批准；S11仍未授权。

## 21. S10P2 Test-only Secure Storage实际实现（DEC-126-041 Option B Accepted / Closure HOLD）

### 21.1 Source与默认兼容

- Desktop本地checkpoint：`c863b2ab30d185201bff5736a308d7078ee5dc68`，parent=`fba934c524852719904657d0a4155142040e7285`，分支`feat/feat-126-foundation-closure`，未push。
- `contract-impact = additive Desktop-private storage/deployment interface`。未修改SQLCipher business schema、Tauri command/event/cursor/error、TypeScript/Pinia/Vue、central contracts、Public Tasks/Host wire、API、Host或Runtime pin；Cargo/pnpm依赖与lockfile未改。
- 独立`YIJIE_FEAT126_S10_SECURE_STORAGE_ENABLED`只在S10P1 master也为exact `true`时生效；默认、`false`或master-only均继续使用`com.yijie.ai.chat-*`和`ai.yijie.desktop.auth`，不会因S10P1自动访问Keychain。

### 21.2 Run manifest、namespace与cleanup

- Rust从canonical non-nil lower-case UUID派生三条固定后缀namespace；native-auth test store根本不构建legacy entry，因此legacy读取/修改/删除路径计数为0。
- `RUN_ROOT`必须位于canonical临时目录之下且为当前owner、`0700`、non-symlink；固定创建`desktop-app-data/host-home/codex-home/project/secure-storage`。Chat SQLCipher只取run-scoped app-data，sidecar要求Host/CODEX Home精确匹配，项目选择/重验只能命中同run project。
- manifest为`0600`、closed schema，保存run ID、owner UID、目录role、namespace descriptor SHA、phase、Desktop PID与recovery count；不保存secret、真实路径或service/account正文。wrong owner/run/schema/path、symlink、mode、活跃同run PID均fail closed。
- inventory调用Protected Data store的exact `service+account` attribute search，只返回三条role的`absent|present`和namespace-schema-valid；不全量枚举、不调用`get_secret`、不hash secret。正常业务store才读取并严格解码自身合成secret。
- cleanup先验证manifest和Desktop PID已停止，阶段转`cleanup_pending`，逐条exact existence-check/delete；missing幂等成功，中断可同run重试，全部absent后标记complete并删除唯一run root。manifest mismatch时delete调用数为0。

### 21.3 Native proof停止事实

仓内fake backend覆盖pre absent、同run恢复、异run隔离、stale PID、cleanup中断/重试、missing item、manifest mismatch拒删、精确root删除和content-free evidence。一次沙箱外随机Protected Data probe只访问三条run-derived tuple；pre/post均为absent，cleanup完成且临时root已删除，但首次`set_secret`返回`A required entitlement isn't present`。本机`security find-identity -p codesigning`为`0 valid identities found`。

该失败不是生产源码降级或把普通文件当作Keychain等价物的理由。DEC-126-041当时接受Option B：接受源码checkpoint与仓库证据，但native S10P2 Closure保持HOLD。随后DEC-126-042把该原生证明转为Deferred Native Hardening，DEC-126-043接受另行授权的S10P2F Closure并关闭Local-only BLK-004；原生失败事实仍保留，且该接受不授权进入S10P3/S10B。

### 21.4 Native signing preparation现状与停止边界

- Desktop canonical bundle identifier固定为`com.yijie.ai`；当前仓库没有macOS entitlements或embedded provisioning profile。
- 本机`security find-identity -v -p codesigning`返回`0 valid identities found`，`profiles show -type provisioning`返回没有已安装profile；active developer directory仅为Command Line Tools，不能使用Xcode automatic signing。
- Protected Data store的本地依赖文档明确要求客户端由provisioning profile签名；未签名CLI出现`-34018 / required entitlement missing`是预期fail-closed行为。
- 目标access group必须从获批profile的Application Identifier Prefix/Team Identifier导出，并精确匹配`<prefix>com.yijie.ai`；在profile不存在时禁止猜测prefix、生成通配组或使用foreign/default group。
- 准备完成的退出证据必须同时包含：profile未过期且bundle/team匹配、signed temporary app/harness的embedded profile与effective entitlements匹配、只启动run-scoped synthetic matrix、三条item create/read/restart/read/delete成功、post inventory全absent、default/legacy/foreign访问修改删除均为0。
- 本次准备盘点没有新建证书、CSR、profile、entitlements文件或Keychain item，没有修改Desktop源码/配置，原生write attempt仍为2。签名材料需要具备Apple Developer Team权限的Owner在系统外部提供或安装后才能继续。

## 22. Local-only Ephemeral Secret Backend调整（DEC-126-042 Accepted）

### 22.1 决策边界与影响分类

- `contract-impact = semantic`：已接受的调整改变S10本地test profile中三个secret的存储解释和BLK-004退出条件，但不改变production/default行为、公共wire、private IPC、SQLCipher业务schema或跨仓持久化格式。
- central G2A：`N/A`。`yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f`、Public Tasks/Host wire、Runtime pin、API与TS/Vue均不变；权威源是Desktop-private test deployment/storage配置和本Feature Package的安全决定。
- DEC-126-041保持历史Accepted：其source checkpoint与原生失败事实不被改写。DEC-126-042已把signed proof从Local-only blocker移为`Deferred Native Hardening`；不得写成已通过、豁免或文件backend的等价证明。
- DEC-126-042当轮只登记安全/G2设计；Owner随后单独授权LIA-126-011。该实施严格限定为Desktop Rust test-only backend与测试，没有修改Keychain、跨仓协议、TS/Vue或默认配置，也未授权S10P3/S10B。

### 22.2 Backend选择与双门禁

推荐Option A：Rust-only、run-scoped ephemeral file secret backend。legacy/default Keychain会触碰真实用户域，固定或run-ID派生secret不可保密，环境变量正文可能扩散到child/process evidence，纯内存又不能覆盖Desktop同run重启；因此这些方案均拒绝。

已接受的backend设计只在以下条件同时成立时启用：

1. `YIJIE_FEAT126_S10_TEST_PROFILE_ENABLED == "true"`；
2. `YIJIE_FEAT126_S10_EPHEMERAL_SECRET_BACKEND_ENABLED == "true"`；
3. canonical non-nil lower-case run UUID、既有fixed loopback fake-provider context与run root校验全部通过。

任一flag缺失、为`false`或非exact值时不得创建或读取ephemeral文件；默认/生产继续使用当前Protected Data Keychain路径。独立flag不得进入`.env`、CI、默认开发配置或build default；WebView、TypeScript、shell与Host child不得提供文件名、路径或secret正文。

### 22.3 文件、secret与manifest格式

- 每个run只允许三个固定role：`chat_sqlcipher`、`receipt_hmac`、`native_auth`。Chat/receipt各使用OS CSPRNG生成的32-byte secret；native-auth使用现有严格serializer生成仅含合成local-test refresh family的opaque bytes，token部分由CSPRNG生成。禁止常量、run-ID派生、共享seed和真实账户数据。
- run root必须位于OS canonical temporary root之下，属于当前effective UID、mode `0700`、非symlink；secret directory同样为`0700`。三个role映射到closed固定basename，路径只由Rust从已验证run root构造。
- 每个secret file以`create_new/O_EXCL`、`O_NOFOLLOW`和mode `0600`创建；写入后`sync_all`，读取前重新检查regular file、owner、mode、`nlink == 1`、canonical parent和精确长度/serializer schema。已存在但不合格、partial write或role重复一律fail closed，不静默重生。
- manifest不保存secret、secret hash、真实绝对路径或用户数据；只保存schema version、run ID、owner UID、固定role/basename、phase、PID/recovery count和content-free状态。evidence只允许role、present/absent/schema-valid、计数、布尔值和manifest/fixture摘要。
- 文件是Local-only合成测试材料，不声称等价于Keychain、Secure Enclave或生产secret protection；普通unlink不承诺清除SSD、swap、OS backup或第三方副本。

### 22.4 生命周期、重启与cleanup

1. 首次启动：验证双flag、run root和manifest；三个role全部absent才逐个CSPRNG生成并持久化。若中途失败，manifest进入`cleanup_pending`，本run不得继续启动业务链。
2. 同run重启：manifest、run ID、owner、role、文件元数据和schema全部匹配时读取同一secret，使SQLCipher历史、receipt验证和合成native-auth可恢复；任何缺失/漂移都fail closed，不生成替代key。
3. cross-run：不同run root与manifest完全隔离；一个run不能解析、读取、覆盖或删除另一run的文件。活跃PID或session lease冲突时拒绝并发启动。
4. cleanup：先停止Desktop，再停止Host/Runtime，关闭SQLCipher handle；manifest转`cleanup_pending`后只unlink列出的三个exact files。missing幂等成功，foreign owner/mode/nlink/symlink/basename/manifest不匹配时停止且delete count为0。
5. cleanup恢复：异常退出后仅同run、同owner、无活跃PID且manifest完整时继续；三个files全absent后标记complete，再删除已验证为空的run root。不得递归清理未知文件或目录。

### 22.5 Docker与宿主机职责

- PostgreSQL、Keycloak、Caddy和API等依赖可由已接受的S10E隔离Docker profile运行。
- Desktop GUI、Agent Host和固定Runtime按当前设计在macOS宿主机/子进程运行；不把Desktop或macOS Keychain伪装成Docker服务。
- ephemeral backend只为宿主机Desktop test profile提供合成secret；Docker volume、container secret、真实Keychain和真实用户数据均不作为fallback。
- 模型继续固定fake provider；MiniMax、外部模型、真实key与真实数据调用数必须为0。

### 22.6 BLK-004现行退出与Deferred Native Hardening

LIA-126-011已完成以下实现证据：双flag/default-off、CSPRNG生成、same-run Desktop restart恢复、cross-run隔离、wrong owner/mode/nlink/symlink/manifest/partial-file fail-closed、crash与cleanup重试、三个exact file post-absent、production/default路径不变，以及secret/path在source之外的logs/process output/evidence/WebView/bundle命中为0。Owner已接受DEC-126-043 Option A，Local-only BLK-004现为Closed。

Apple signed Protected Data lifecycle转为`Deferred Native Hardening`，在未来准备Desktop签名发布或production activation前强制恢复并通过；它不计入当前Local-only G4/G6 PASS证据，也不得被表述为已验证、已豁免或文件backend的等价替代。

### 22.7 S10P2F单独实施授权（LIA-126-011已执行）

Owner单独授权的允许范围仅为Desktop Rust test-only secret backend、其unit/integration/fault tests及FEAT-126治理证据；禁止修改central contracts、Public Tasks/Host wire、private IPC、Tauri commands/events、TS/Pinia/Vue、SQLCipher业务schema、API、Host、Runtime pin、依赖默认值或production路径。实施只使用合成secret、临时目录和本地checkpoint；未安装Xcode、未访问Keychain、未启动S10P3/S10B、未push/merge/tag/publish/deploy。

停止条件：若实现需要让WebView/shell指定secret路径、把secret传给Host/container、改变现有serializer/DB schema/IPC、修改production/default选择逻辑，或无法在不枚举/读取真实Keychain的情况下证明default路径未触碰，立即停止并提交新的安全/G2缺口。

## 23. S10P2F实际实现（DEC-126-043 Option A Accepted）

### 23.1 Source、选择器与兼容边界

- Desktop checkpoint：`46107eec1e9cba0257252cae8678a4233ef20036`，parent=`c863b2ab30d185201bff5736a308d7078ee5dc68`，branch=`feat/feat-126-foundation-closure`，仅6个Rust文件，clean、local-only、not pushed。
- `ephemeral`只有master与独立flag均为exact `"true"`、canonical run UUID与现有S10 run manifest一致时才可选择。独立secure-storage selector与ephemeral selector同时为true会fail closed；missing、`false`、`TRUE`、`1`和孤立flag均保持既有Protected Data路径。
- protected manifest保持schema v1和既有输出；ephemeral使用closed schema v2。没有新增Cargo/pnpm依赖，没有改SQLCipher业务migration、IPC、TS/Vue、Host/API/Runtime或central contracts。

### 23.2 Secret envelope与文件系统不变量

- 三个role/basename由Rust固定，WebView、shell与Host无指定权。Chat SQLCipher与receipt HMAC均为32-byte OS CSPRNG；native-auth沿用严格`StoredRefreshToken` JSON serializer，token只使用合成随机值并限制`LocalIntegration`环境。
- 创建使用`create_new`（O_EXCL）、O_NOFOLLOW、O_CLOEXEC与0600；目录为0700。每次读、覆写和删除都复验canonical parent、regular file、effective UID、0600、`nlink == 1`、inode/device一致性，以及magic/version/role/length/schema。
- 已存在但损坏的文件不会被静默重生；partial、symlink、hardlink、错误mode、unknown entry、manifest mismatch与foreign/cross-run均fail closed。更新原文件前先验证现有envelope，不产生多余secret temp file。

### 23.3 生命周期、恢复与cleanup实现

- 首次启动创建三个exact files；同run重启读取相同secret，真实SQLCipher reopen与native-auth rotate/restart fixture通过；不同run不得读取、写入或删除对方文件。
- active PID lease、目录或manifest异常时cleanup删除计数为0。正常cleanup先验证全部exact targets安全，再逐个unlink；missing幂等，unknown entry阻断；最终只用非递归`rmdir`删除已验证为空的known directories/run root。
- 一次sandbox-only SQLCipher诊断在macOS backup-attribute限制处失败并留下合成临时run；随后使用正确manifest run ID与受控cleanup恢复，最终`feat126-s10p2f-*` matching root count=0。没有递归删除，也没有真实数据。

### 23.4 Closure结果与停止边界

授权范围内P1为0，S10P2F-001–012与全仓门禁证据见`06-test-plan.md`和`08-verification-report.md`。Owner已接受DEC-126-043 Option A，S10P2F Closure Passed并关闭Local-only BLK-004；G3仍保持Partial。该接受不授权S10P3/S10B/S11。Apple signed Protected Data生命周期仍为`Deferred Native Hardening / NOT RUN`，文件backend不构成其PASS、豁免或生产等价替代。

## 24. LIA-126-012 / S10I执行结果与S10P3 Closure

### 24.1 Desktop candidate已实现的边界

- SQLCipher forward-only schema v5新增content-free Public Task binding/outbox状态；仅保存local/public/operation ID、authority revision、closed state、lease/retry/error enum与时间，不复制prompt/message/assistant/raw/title/path。
- Rust native authority使用既有`NativeAuthRuntime`调用固定contract的`POST /v2/tasks`；同一create operation复用UUID idempotency key，只有201响应的tenant/creator/reference全部匹配并原子bind后才允许Host start。
- unknown/timeout/409/restart、logout/tenant/revision、create/delete/interrupt/Host-start race由持久化状态机处理；本地删除级联清binding，已创建Public row按DEC-126-038保留。
- additive private projection固定为`chat_get_session_control_plane_v1`与`yijie.chat.control-plane.event.v1`；WebView只见closed状态和稳定issue/recovery，不见Public ID、bearer、owner/tenant authority、路径、Host/Runtime ID或raw wire。
- fixed contract candidate足以表达上述request/response/idempotency/error；central contract、API/Host wire与Runtime pin无需改变，G2A重审为N/A。

### 24.2 仓内证据

Desktop TypeScript 30 files / 167 tests、generate-check、lint和production build通过；Rust在宿主权限下129 pass / 0 fail / 3明确ignored，`cargo fmt`与`clippy -D warnings`通过。migration覆盖populated v1/v2/v3/v4→v5、重复启动、只读/损坏；fake transport覆盖closed request/response/error、authority/idempotency/restart/race/no-log。第一次沙箱内Rust运行因临时SQLCipher、loopback和macOS bookmark权限产生环境性失败，不计为产品回归；同一代码在受控宿主权限下全绿。

### 24.3 DEC-126-044 / S10I：真实OIDC claim纠偏

Owner接受DEC-126-044 Option A并只授权S10I。`yijie-infra@8d7c84dc963141931c6c5d3c3aded3218247df0b`在Desktop public client增加Keycloak内置`oidc-usersessionmodel-note-mapper`，把numeric user-session note `AUTH_TIME`投影为access-token `nbf`。static realm validator与live provisioner要求exact audience + dynamic nbf两个mapper；缺失、额外、静态hardcoded或配置漂移均fail closed。

API `verifier.go`和required claims未改；未使用静态`nbf=0`、script mapper、手工bearer、备用signer、curl或mock。该变化只属于default-off、synthetic-only S10E identity profile，不改变central contracts、Public Tasks/Host wire、Runtime pin或production/default identity行为，G2A重审为N/A。

### 24.4 真实main-chain复验

fresh run `90dc0dd9-140d-4ec0-b918-e24faab98aeb`使用exact-digest PostgreSQL/Keycloak/Caddy、合成用户与API migration v4。Desktop production Rust authority完成标准Authorization Code + PKCE，access token含numeric `nbf`；unchanged API verifier接受capability与content-free `POST /v2/tasks`。随后Public binding先于Host start落库，本地session删除完成，Public Task row按DEC-126-038保留。

隔离PostgreSQL content-free汇总为：`task_rows=1`、`closed_input_rows=1`、task forbidden/path rows=`0/0`；`audit_rows=5`、audit forbidden/path rows=`0/0`；`idempotency_rows=1`。API与四个容器/网络已停止，named volumes按既定删除边界保留；MiniMax、Keychain、真实数据、默认flag与远端写入均为0。

### 24.5 DEC-126-045 Closure Review结论

S10P3实现已保存为本地Desktop checkpoint `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；S10I保存为本地Infra checkpoint `8d7c84dc963141931c6c5d3c3aded3218247df0b`，均未push。Owner于2026-08-05批准DEC-126-045 Option A，接受S10P3 Closure并关闭BLK-005；Owner随后另行批准并已执行LIA-126-008。S10B在S10B-001新增bootstrap profile/DB-name blocker并fail closed，G3继续Partial；S11、MiniMax、activation与远端动作仍未授权。

## 25. LIA-126-008 / S10B执行授权边界

- 授权：仅执行§17.6冻结的`S10B-001`至`S10B-012`，固定Contracts/API/Host/Desktop/Runtime/Infra完整SHA，先复核工作树与本地进程/端口，再启动本run资源。
- 环境：owner-only临时run root、canonical UUID、S10E隔离PostgreSQL/Keycloak/Caddy/API、宿主机Desktop/Host/fixed Runtime、fixed fake Responses、synthetic identity/tenant/project；仅子进程临时exact-true，退出后defaults必须仍为false。
- 证据：只保留content-free PID/SHA/nonce/port/count/hash/state/duration/failure class；正文、raw/title、secret、DSN、key与真实路径不得进入治理材料。
- 停止：任何baseline漂移、非loopback、真实namespace访问、migration绕过、序列/终态/持久化/删除不一致、泄漏、stale process或cleanup/default-off失败立即终止本run并提交失败分类，不得弱化断言。
- 排除：不调用MiniMax/外部模型，不使用真实数据/项目/Keychain，不改contracts/API/Host wire/private IPC/Runtime pin，不进入S11，不push/merge/tag/publish/deploy或默认启用。
- 退出：完成后提交独立S10B Closure Review；未获Owner接受前G4/G6仍Pending。

## 26. LIA-126-008 / S10B首次正式执行结果（DEC-126-046 Accepted Option A）

- Run：canonical UUIDv4 `9b9d455f-0500-4dd0-a008-d5a862bf6f20`；七仓SHA/worktree、Runtime binary/manifest、Compose v5.3.0与固定端口preflight均通过。
- 环境：exact-digest PostgreSQL/Keycloak/Caddy四容器健康；TLS/OIDC/Tasks denial与runtime inventory通过；2个reviewed synthetic users provision完成；API migration到v4。
- 停止事实：Infra authority把API数据库固定为`yijie_api_feat126_s10`，而API `BOOTSTRAP_PROFILE=feat-125-local-lab`在任何数据库访问前只接受`yijie_api_feat125_local`。因此四份tracked synthetic authorization manifests均被profile validation拒绝。
- 安全处置：没有移除profile、改用generic lane、手工建库/插行或复用旧volume。数据库复核为migration `4`、users/tenants/memberships `0/0/0`；API、fake provider、Desktop、Host和Runtime未启动。
- Cleanup：四个容器和四个run network已停止/移除；临时binary root已删除；固定端口未观察到listener。四个project-scoped named volumes与Infra owner-only ignored run record按既定删除边界保留。
- 判定：`S10B-001 = FAIL (environment/bootstrap-profile)`；`S10B-002–012 = NOT RUN`；`S10B-BLK-001 = OPEN`；S10B Closure Fail，G3 Partial、G4/G6 Pending。
- Owner已接受DEC-126-046 Option A：认可上述fail-closed事实，但不接受S10B Closure；S10B-BLK-001保持Open，不授权直接修复、重跑S10B或进入S11。

## 27. DESIGN-126-009 — S10BP0 Closed Synthetic Bootstrap Profile Corrective

### 27.1 评审边界与contract-impact

- 本轮只有只读源码盘点、设计冻结与治理文档更新；API、Infra及其他业务源码未修改，容器/服务未启动。
- `central-contract impact = none`，G2A重审为N/A。拟议变化只是在API与Infra之间增加一个local synthetic bootstrap deployment/security profile；Public Tasks HTTP wire、API verifier、Desktop private IPC、Host wire、Runtime pin与数据库业务schema均不变。
- `feat-125-local-lab`的profile常量、issuer、`yijie_api_feat125_local` DSN规则、四份manifest字节与既有测试必须逐字节/行为兼容。API空profile的generic nonproduction兼容路径也保持不变；FEAT-126的fail-closed要求由新的Infra权威入口保证，不得把generic lane暴露给S10调用者。

### 27.2 Closed profile权威

唯一候选名称为`feat-126-s10-local-lab`，只接受下列closed tuple：

| 字段 | 唯一允许值/约束 |
|---|---|
| Environment | `YIJIE_ENV=nonproduction` |
| Issuer | `https://localhost:8443/realms/yijie-local` |
| DSN scheme/host | `postgres://`，host精确`127.0.0.1:5432`；`localhost`、IPv6、其他端口拒绝 |
| DSN database/query | `/yijie_api_feat126_s10`且query精确只有`sslmode=disable`；额外/重复/编码变体/fragment拒绝 |
| DSN credentials | user/password均非空；错误输出不得包含DSN或password |
| Manifest authority | 仅现有`config/nonproduction/feat-125-local-lab/`下四个reviewed JSON的显式路径及其固定subject、user ID、tenant ID/name、role、actor、`synthetic_only`分类 |

不复制或改名manifest，不使用glob发现新增文件，不允许caller传profile/manifest/issuer/DSN覆盖。错误profile、generic/空profile、错误数据库/issuer/user/tenant/name/role/actor/query/host必须在数据库访问前fail closed。

### 27.3 校验与调用顺序

API命令按以下顺序执行：`ValidateExecutionProfile → open/decode all four manifests → ValidateExecutionMatrix → RequireCurrent migration → open database/schema → one serializable batch transaction`。

Infra权威命令在spawn CLI前完成canonical run UUID与未拒绝run校验、固定API完整SHA/clean worktree、四个显式tracked regular path及secret file权限校验。API-owned empty verifier证明migration v4与全空authority；命令内部固定profile并分别执行首次/幂等两个四-manifest atomic batch，调用者没有generic或自选manifest入口。

### 27.4 Fresh database、幂等与原子性

- 仅允许fresh isolated `yijie_api_feat126_s10`且migration exact v4；缺migration或非fresh authority立即失败，不通过手工SQL补状态。
- 首次执行四份manifest后应精确得到2 users、2 user identities、2 tenants、4 memberships与4 membership-role assignments；两租户authorization revision均为3。
- 同一四份manifest第二次执行必须全部`state_changed=false`、revision保持3，累计8条content-free `authorization.bootstrap` audit；审计只保存revision/diff分类，不保存issuer/subject/manifest正文。
- 每个四-manifest pass的全部状态与4条success audit位于同一serializable transaction。validation、migration、conflict、success-audit或commit失败不得留下partial user、tenant、membership、role、assignment或audit；unknown commit以4个exact request audit共同reconcile。

### 27.5 S10BP1测试与回滚矩阵

| 类别 | 必须验证 |
|---|---|
| Positive | 四份manifest、exact counts/revisions、第二遍幂等、content-free audit |
| Authority negative | feat125/任意DB、`localhost`、错误端口、额外query、错误issuer、空/generic/未知profile、未知manifest、tuple/role/actor漂移、缺migration |
| Ordering | profile失败时manifest-open=0、DB-connect=0；manifest失败时DB-connect=0；Infra wrapper错误时API CLI spawn=0 |
| Atomicity | 每种中途失败后的users/tenants/memberships/assignments无partial增量；failure audit符合既有事务边界 |
| Security | DSN/password/token/manifest正文/真实路径日志与process output命中0；只保存计数、revision、枚举和hash |
| Regression | `feat-125-local-lab`全部既有profile/manifest/integration测试继续通过；generic API兼容路径不变 |
| Cleanup | 失败run停止其容器/网络；named volumes继续按既定边界披露，不静默删除或回退旧volume |

### 27.6 实施切片与停止条件

`LIA-126-013 / S10BP1`已按以下边界实现：

1. API增加新closed profile常量/validator分支、CLI usage与正负/顺序/回归测试；不得改现有profile分支或generic语义。
2. Infra增加一个run-scoped权威bootstrap命令，内部固定新profile和四个显式API manifest路径，先验migration v4，再执行并生成content-free count/revision/audit摘要；不得新增通用bootstrap入口。
3. 已提交且Owner后来接受DEC-126-048 S10BP1 Closure Review；该接受不能自动重跑S10B，完整fresh S10B仍需再次单独授权。

立即停止条件：需要修改central contracts、auth verifier、Public Tasks/Host wire、Desktop IPC、Runtime pin、migration/schema、现有manifest、`feat-125-local-lab`或generic compatibility lane；需要手工SQL、generic bootstrap、caller-selected manifest、旧volume fallback或任何正文/secret证据。

Owner已批准DEC-126-047并授权LIA-126-013，随后正式接受DEC-126-048 Option A：`S10BP1 Closure Passed / S10B-BLK-001 Closed / G3 Partial`。API/Infra门禁与atomic matrix通过；fresh DB以本机已存在、digest精确匹配的pinned image ID启动，因为既有S10E helper的tag@digest inspect曾fail closed。该独立缺口随后按DESIGN-126-010/DEC-126-049处理并由DEC-126-050接受Closure；未重跑S10B。

## 28. DESIGN-126-010 — Exact Repository-digest Image Availability Corrective

### 28.1 问题与决策

S10BP1复验时，Docker 29.6.1本地inventory已包含PostgreSQL固定digest，但`docker image inspect version-tag@digest`仍曾返回`No such image`。重启Docker后同一命令恢复成功，确认这是本地引用索引的状态敏感兼容问题，而不是镜像内容缺失。继续把该lookup当作唯一availability gate会产生假阴性；删除preflight又会削弱启动前fail-closed边界。

DEC-126-049采用以下closed方案：

1. `docker-compose.local.yml`与`FEAT_126_S10_IMAGES`中的`version-tag@digest`继续是唯一配置authority，四个service pin和digest逐字节不变。
2. 新preflight从该authority解析并去重三个`repository@digest`内容身份；不得接受无tag、无digest、非SHA-256或冲突version tag。
3. 对每个内容身份调用无shell的`docker image inspect repository@digest`，要求valid image ID、exact RepoDigests membership，并在Docker提供descriptor时要求descriptor digest精确相等。
4. 任一missing、malformed、冲突、RepoDigests mismatch、descriptor drift、Docker错误或非JSON输出均fail closed；错误不回显inspect原文。
5. 通过后仍由Compose使用原`version-tag@digest`和`--pull never`启动；不得floating tag fallback、`docker pull`、手工image ID或第二套pin清单。

该变更只影响yijie-infra local deployment/security helper，central contracts、API/Host/Desktop/Runtime、数据库schema、Public Tasks/private IPC wire均不变，contract impact=`none`且G2A=N/A。

### 28.2 实施与验证边界

新增`verify-feat-126-s10-images.mjs`并由accepted `feat-126-s10-compose.sh up`调用；自动化覆盖authority解析/去重、malformed、RepoDigests mismatch与descriptor mismatch，并继续静态证明`--pull never`、无image pull、无volume删除和无trust安装。

fresh compatibility run `ae1c892a-4819-40bc-9ce9-d72f6ea2fcd7`只启动S10E四个隔离依赖：preflight核验3个exact repository digest，Compose未pull，PostgreSQL/Keycloak/Caddy四服务全部healthy。随后权威stop移除4 containers与4 networks；四个project-scoped named volumes及owner-only ignored run record按既定边界保留。本run没有启动API、Desktop、Host、Runtime或fake provider，不是S10B重跑，也不构成G4/G6证据。

DESIGN-126-010与DEC-126-049已由Owner“单独评审并修复”指令接受；实现和验证形成DEC-126-050 Closure Review，Owner现已正式接受Option A并关闭S10B-BLK-002。该接受不自动授权重跑S10B或进入S11。

## 29. LIA-126-014 / S10B-R2 fresh preflight执行结果

### 29.1 冻结候选

本轮先把所有已批准且未提交的FEAT-126变更形成仅本地checkpoint，未push：Governance `9db41b03072f5d427c61fa832d22e94f3e8ce02c`、API `c5f334e88d54d9e04f388d0349f4f5925124abd6`、Host `e0a8d3d29a335571d1654d95e1e262c240755674`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`、Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、Infra `597acb34588cc519d2482bffbf4fb3298bacc734`。checkpoint后三仓工作树均clean；Governance package/strict/G2A/YAML/lint/test、API lint/race tests、Infra 85/85与Compose validation均通过。

### 29.2 fail-closed事实

fresh run ID为`4ffa07b9-6e4c-45d4-b5d5-3b3be5d7d818`。在创建run root、secret、Docker资源或连接数据库之前，权威`make feat-126-s10-api-migrate`调用的`feat-126-s10-api-migration.sh`要求API HEAD精确等于历史`a64f9f591fb594818c1778e30c6941e2574b3264`；当前S10BP1 closed bootstrap实现只存在于已冻结的`c5f334e...`，因此门禁以`unexpected yijie-api commit`拒绝。退回旧API会丢失closed profile，绕过wrapper或直接运行migration会破坏accepted no-bypass authority，均未执行。

S10B-001判定为`FAIL / baseline-deployment-authority mismatch`，S10B-002–012均`NOT RUN`。run root、container、network、volume、API、Desktop、Host、fake provider、Runtime和模型调用均为0；无需清理业务数据。

### 29.3 新blocker与纠偏候选

历史`S10B-BLK-003`为migration wrapper与bootstrap wrapper没有共享同一显式完整API SHA authority。Owner已接受DEC-126-052方案A与LIA-126-015/S10BM1 Closure；实现见§30，blocker现已Closed。不得只替换硬编码、使用浮动branch、caller自选generic profile、退回旧API或直接执行migration；fresh rerun仍需单独授权。

## 30. LIA-126-015 / S10BM1 shared API candidate authority

### 30.1 唯一authority与顺序

`make feat-126-s10-api-migrate`与`make feat-126-s10-api-bootstrap`现在都强制接收同一完整小写40字符`API_SHA`，并在读取run secret或访问PostgreSQL前调用唯一`feat-126-s10-api-candidate.mjs`。helper先验证canonical UUIDv4、owner-only且canonical的run root、API工作树HEAD精确等于caller SHA且worktree clean；随后在run root以`O_EXCL`/`O_NOFOLLOW`等价的create-new语义写入0600 `api-candidate-authority.json`。closed document只允许`schema_version`、`run_id`和`api_full_commit`三个字段。

首次命令建立authority，后续命令只能复用完全相同的run ID与API SHA。missing/short/wrong SHA、dirty worktree、candidate drift、corrupt/extra-key document、wrong owner/mode、symlink、hardlink、noncanonical root全部fail closed；失败发生在secret文件读取与数据库访问之前。没有branch/floating identity、第二套hardcoded pin、repository path、DSN、credential、manifest正文或conversation正文进入authority。

### 30.2 兼容与contract impact

这是对FEAT-126私有本地deployment helper的有意breaking收紧：旧的migration两参数调用不再兼容并会fail closed；仓库Make target与runbook在同一checkpoint中同步要求`API_SHA`。central source contract、Public Tasks/Host/private IPC wire、数据库业务schema、Runtime pin、production/default配置和现有`feat-125-local-lab`语义均未改变，因此central G2A impact为`none`。

### 30.3 证据与停止边界

本地checkpoint为`yijie-infra@bb96333df908d6fea72ec0a1f57a64477c2428e4`。Infra validate/lint/test、87/87自动化、Node/shell syntax与diff检查全部PASS；同run复用、wrong/drift/dirty、mode/hardlink/symlink负向矩阵已覆盖。执行未启动container/service/API/Desktop/Host/Runtime，未读取secret/DB/Keychain，未调用模型、处理真实数据、启用默认flag或写远端。

DEC-126-052 Option A已接受S10BM1 Closure并关闭`S10B-BLK-003`，但该接受不是S10B证据。Accepted治理overlay随后形成clean checkpoint `441663faf7d505015f03d572c8e9f30b3ba1a2df`，Owner再单独批准`LIA-126-016 / S10B-R3`：只允许一次fresh S10B-001–012，任一失败立即停止，不进入S11或MiniMax。该授权后来已消费，结果见§31。

## 31. LIA-126-016 / S10B-R3 immutable-image preflight结果

fresh run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5`完成七仓exact-clean、Compose 5.3.0、Docker 29.6.1、端口、ignored secret init与Compose config预检后，accepted image verifier在Compose `up`前返回`required immutable image is unavailable locally`。没有container/network/volume/listener被创建，S10B-001判定FAIL，002–012未运行；run被标记`REJECTED`并执行exact stop。

Owner通过DEC-126-053 Option A接受该fail-closed事实、拒绝S10B-R3 Closure并保持`S10B-BLK-004` Open，同时校正根因：失败事实不能证明Docker 29.6.1永久无法解析`repository@digest`。现有verifier把Docker CLI/endpoint/permission/daemon/image/reference失败压成同一错误；正确pin在Docker capability可用时已只读解析成功，containerd reference metadata状态仅是待复验因素，不得写成已确认Docker bug。

## 32. DESIGN-126-011 — Docker Execution Capability & Immutable Image Resolver Corrective

### 32.1 评审范围与contract impact

- S10BD0只执行只读源码/环境盘点和治理文档更新；未修改`yijie-infra`、API、Host、Desktop、Runtime或contracts源码，未启动Docker Desktop、container、服务或S10B。
- 本轮文档变化`contract-impact=none`：不改变跨进程、跨仓、持久化或Runtime行为。
- 拟议`LIA-126-017 / S10BD1`会改变FEAT-126本地verifier的失败分类、校验顺序并增加可清理的test-only resolver probe，故按最高风险归类为local deployment-interface `semantic`。central contracts、Public Tasks/Host/private IPC wire、数据库业务schema、Runtime pin和production/default配置不变，central G2A=`N/A`。
- 唯一配置authority仍是`FEAT_126_S10_IMAGES`及Compose中的原始`version-tag@digest`；不得建立第二套pin、接受floating tag、使用image ID绕过或放宽`--pull never`。

### 32.2 已确认事实与诊断边界

当前`inspectLocalDigest`把`spawnSync`的任意`error`或非零status统一转换为`required immutable image is unavailable locally`，没有先证明Docker daemon/socket可达，也没有保存closed failure class。S10BD0只读差分得到：

1. 在Docker endpoint不可达的执行上下文中，verifier返回上述generic image error；同上下文`docker version`实际显示`desktop-linux`指向的socket不存在。
2. 本次评审前的只读获准上下文中，正确PostgreSQL pin `sha256:4e6e670bb069649261c9c18031f0aded7bb249a5b6664ddec29c013a89310d50`曾由`repository@digest`与`version-tag@digest`成功解析，Id/RepoDigests/Descriptor一致；未pull、retag或重启。
3. 因此capability失败时不得生成image缺失结论；capability成功后的reference状态仍须按独立类别验证。没有官方或本地充分证据把现象定性为Docker 29.6.1永久缺陷。

### 32.3 capability-first状态机

未来S10BD1必须在同一Node进程环境、同一Docker context中按以下顺序执行：

1. `docker_cli_probe`：无shell调用固定Docker CLI；ENOENT/exec错误归类`docker_cli_unavailable`。
2. `docker_server_probe`：读取容量受限的Server version/info投影；权限/策略拒绝归类`docker_permission_denied`，endpoint/socket缺失、daemon停止或超时归类`docker_daemon_unavailable`。此步失败后image inspect/create调用次数必须为0。
3. `image_identity_probe`：只消费原始Compose `version-tag@digest`及其派生的expected repository/digest；任何失败均为closed code，不输出原始stderr、context endpoint、socket/path、token或环境变量。
4. `runtime_resolver_probe`：仅在全部identity通过且Owner单独授权S10BD1时执行；使用原始pin与`--pull=never`创建但不启动probe container，随后精确reconcile/删除。

稳定failure classes冻结为：`docker_cli_unavailable`、`docker_permission_denied`、`docker_daemon_unavailable`、`image_not_found`、`image_reference_unresolved`、`image_identity_invalid`、`image_repository_mismatch`、`image_digest_mismatch`、`image_platform_mismatch`、`inspect_payload_invalid`、`resolver_probe_failed`、`resolver_probe_cleanup_incomplete`。治理证据只保存class、pin的reviewed hash/短摘要、计数与PASS/FAIL，不保存原始stderr或主机路径。

`image_not_found`与`image_reference_unresolved`的诊断规则为：原始exact ref返回not-found后，仅允许对同一authority的`repository:version-tag`做read-only诊断，不作为PASS fallback；tag也不存在则为`image_not_found`，tag存在且其Descriptor/RepoDigest仍精确等于pin则为`image_reference_unresolved`，tag内容漂移则按digest/repository mismatch失败。

### 32.4 immutable identity Gate

每个唯一原始`version-tag@digest`都必须满足：

- `Id`为完整`sha256:<64 lowercase hex>`；
- `Descriptor.digest`必须存在并精确等于pin，不再以缺失descriptor作为可接受分支；
- `RepoDigests`必须包含从同一pin派生的exact `repository@digest`；
- repository归一化后必须等于配置authority，不接受镜像ID、别名仓库或不同registry替代；
- `Os=linux`，`Architecture`必须等于已验证Docker server architecture；当前本机候选为`arm64`，但实现从server capability读取而非硬编码；
- 输出必须为单个、容量受限、无换行的closed JSON object；空、多行、oversize、extra process output或非法JSON均fail closed。

bounded retry不能改变failure结果：同一快照最多允许一次立即重复用于判定state stability；两次结果不一致归类`image_reference_unresolved`并停止，不通过sleep/restart/pull修复现场。

### 32.5 no-pull resolver probe与精确清理

S10BD1候选probe对三个唯一pin逐一执行，且不启动container：

- 名称与labels绑定canonical test run UUID、`ai.yijie.feature=FEAT-126`、`ai.yijie.slice=S10BD1`和唯一pin index；已有同名对象立即停止，不删除。
- 使用`docker create --pull=never --network none <exact version-tag@digest>`；不传业务secret、端口、Host mount、privileged或capability。
- 根据已验证inspect payload中的`Config.Volumes`为每个绝对destination显式使用tmpfs覆盖，避免PostgreSQL/Caddy image声明volume产生anonymous volume；未知、相对、重复或危险destination在create前拒绝。
- create返回后核对container Image ID、labels、name、`State.Status=created`、network/port/host-mount为空；从未执行`docker start`。
- 成功、失败和unknown outcome都先按exact name查询；只有ID/name/labels/run/pin全部匹配才允许`docker rm`。身份不匹配时删除数必须为0并返回`resolver_probe_cleanup_incomplete`。
- pre/post inventory要求本probe container、anonymous volume、network与listener增量均为0；不删除S10E保留named volumes或任何非本run对象。

该probe只证明本机Docker resolver能在no-pull条件消费Compose exact pin，不证明四组件ready或S10B/G4通过。

### 32.6 S10BD1测试、回滚与退出

S10BD1至少覆盖：CLI missing、socket/endpoint missing、permission denied、daemon timeout、image missing、tag存在但exact ref unresolved、invalid/oversize JSON、Id/RepoDigest/Descriptor/repository/OS/architecture drift、两次快照不一致、create失败/响应丢失/同名冲突、tmpfs覆盖、identity mismatch时零删除、精确cleanup与`--pull never`静态扫描。capability负向必须断言image/create调用为0，日志/证据的endpoint/path/secret/raw stderr命中为0。

回滚只允许移除新capability/classifier/probe调用并恢复accepted S10BR1 helper，同时继续HOLD S10B；回滚不能通过pull、retag、Docker restart、store切换、prune、floating tag或删除volume获得绿色结果。

`LIA-126-017 / S10BD1`范围仅限`yijie-infra`本地verifier、测试、FEAT-126 runbook与`yijie`治理文档。Owner先单独批准，后又明确指令开始并消费该授权。实现已形成Infra clean checkpoint `2a643caef210e32cab80242ede46b96927b2097a`，逐类测试、可清理live probe、no-pull/no-log/cleanup证据已完成。DEC-126-055 Option A已接受Closure；任何fresh S10B-R4仍须另行授权，不得自动重跑。

## 33. S10BD1 implementation result / DEC-126-055 Accepted

### 33.1 实现

- verifier在任何image inspect/create前，于同一Node进程和Docker context执行CLI/server capability检查，并把失败闭合为DESIGN-126-011冻结的12类之一；raw stderr、socket、环境正文和secret不出现在对外结果。
- identity authority仍只来自Compose原始`version-tag@digest`；逐项校验Id、mandatory Descriptor digest、RepoDigests、repository、Linux与daemon architecture，两次快照必须稳定。tag-only查询仅区分missing与unresolved，不产生PASS。
- resolver只在capability/identity全PASS后执行`docker create --pull=never --network none`；container永不启动，image声明volume全部tmpfs覆盖，name/label/run UUID/pin必须exact。unknown outcome先按exact name reconcile，foreign/mismatch删除数为0。

### 33.2 不可变证据

- 执行治理基线：`yijie@075a5051b538ce8f28834db70de8f4f544ce4484`；Infra实现：`yijie-infra@2a643caef210e32cab80242ede46b96927b2097a`；Contracts/Runtime pins分别保持`29317b6426578749dc698fc2ad32b986ee5c8e9f`与`3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`。
- S10BD1-001–012为12/12 PASS；Infra全量99/99、validate、lint、shell、security/no-log与diff均PASS；Compose pins和`--pull never`未改变。
- exact-commit live run `12600000-0000-4000-8000-000000000055`在Docker Desktop 4.82.0 / Engine 29.6.1 / linux-arm64验证3个immutable identities与3个no-start probes；未pull。后置S10BD1 labeled containers、running containers、networks、volumes均为0，Docker Desktop恢复执行前停止状态。

### 33.3 Gate

实现侧P1为0；Owner已接受DEC-126-055 Option A，S10BD1 Closure Passed并关闭`S10B-BLK-004`。该接受不自动授权S10B-R4、S11、MiniMax、feature activation或远端动作。

## 34. LIA-126-019 / S10BF1 Host-owned fake readiness与单一preflight

### 34.1 Authority与contract impact

Owner已接受DEC-126-056 Option A并单独授权LIA-126-019。Host是dataset/case/digest的唯一authority：`FrozenReadinessAuthority`从已锁定的S9 bundle读取`dataset_id`、固定case和dataset SHA；test-only health与probe使用显式`fixture_case_id`，不再输出歧义字段。probe只接受canonical run UUID和固定`127.0.0.1:18082/healthz`，自行附加run/case header，禁止redirect、proxy、hostname、query、unknown field、oversize或identity drift。

Infra新增唯一`make feat-126-s10b-preflight`入口。调用者只提供fresh run UUID与七个完整候选SHA；不存在dataset、fixture或endpoint参数/env/Make变量。runner从固定sibling repos校验exact clean候选，依次组合accepted resolver、S10E、TLS/OIDC、synthetic identity、migration/bootstrap、API health/readiness和Host probe，并只接受Host返回的closed projection。它不复制第二套case/dataset常量，也不构造fake请求header。

该变更只影响private test/deployment tooling，分类为`semantic`；central contracts、Public Tasks与Host业务wire、Desktop private IPC、SQLCipher/PostgreSQL业务schema、API/Desktop/Runtime行为及Runtime pin均未改变，G2A=N/A。fake health是test-only private probe surface，不是生产Host API。

### 34.2 自动化与fresh组合预检

- Host checkpoint：`1ca4ee555586e5243f7101b9fe056c6fa117a560`。Host全量race/coverage、lint/vet、contract snapshot PASS；authority、exact endpoint/run、unknown/oversize、dataset-as-case、digest drift测试PASS。独立loopback live probe返回`dataset_id=feat126-title-raw-v1`、`fixture_case_id=normal-000`和锁定dataset SHA。
- Infra checkpoint：`5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`。Infra validate/lint、103/103 tests、Node/shell/diff PASS；测试证明单一Make入口、七SHA authority、无operator fixture/dataset输入、closed projection和全组合gate。
- fresh run：`ed22fc82-4837-4a3e-a60e-7f7c8ab6f3f4`，Governance执行基线`db12fe6ce4a8c1f84ac90781191d8a1b26dbcc4d`。resolver、fresh dependencies、TLS/OIDC、2个synthetic users、migration v4、closed bootstrap、API health/ready、Host-owned fake readiness及generated-secret日志扫描全部PASS。
- content-free summary模式`0600`，SHA-256=`8198442e1c8f28a28c01fe0807b10fa0c7485ef6f808b0a24ead75a04e36f7d9`。API/fake已停止，container/network/listener均0；四个run-scoped named volumes和ignored run record按既定边界保留；Docker Desktop恢复执行前停止状态。

### 34.3 Closure与停止边界

上述只证明S10BF1 corrective与`S10B-001 combined preflight`，不证明S10B-R5、真实Vue对话链或G4。`s10b_r5_executed=false`；S10B-002–012、S11、MiniMax、真实数据/Keychain、default activation和远端动作均未执行。Owner已接受DEC-126-057 Option A，S10BF1 Closure Passed且`S10B-BLK-005` Closed；该接受只关闭该blocker，fresh S10B-R5仍须单独明确授权。

## 35. LIA-126-020 / S10B-R5 runtime-profile authority finding

- 唯一S10B-001 authority仍为Infra `make feat-126-s10b-preflight`，其闭合输入仅包含fresh run ID和七仓完整SHA；本次summary SHA-256为`b3e4b833283bf0102edfc4100cd0339002d769d839b7903a2a4426c531b6b1f8`。
- preflight内部使用`YIJIE_API_SERVICE_PROFILE=feat-125-local-lab`；API runtime validator目前也只支持这一runtime service profile。
- `feat-126-s10-local-lab`只存在于synthetic bootstrap authority，不等同于API runtime service profile。R5冻结要求后者，因此不能把bootstrap profile的成功推导为002–012 runtime authority成立。
- 正确设计方向是建立一个closed FEAT-126 runtime service profile，并让preflight与continuation从同一machine-readable authority派生；必须保持issuer、loopback DSN、synthetic-only identity、numeric `nbf`、content-free Public Tasks及default-off语义。
- 本次没有修改API/Infra/Host/Desktop/contracts/Runtime。任何corrective必须单独设计、分类、测试、授权；不得在R5现场补丁或复用旧profile继续。

## 36. DESIGN-126-012 — Closed API Runtime Profile Authority

### 36.1 决策与授权

Owner于2026-08-06明确要求“API runtime正式增加closed `feat-126-s10-local-lab`支持，并让preflight与后续完整链统一消费这一profile；不能只改字符串或绕过校验”。该指令接受DEC-126-058 Option A并单独授权、消费LIA-126-021/S10BRP1；不是S10B rerun授权。

### 36.2 API closed profile

`yijie-api`新增独立`ServiceProfileFeat126S10LocalLab`，并以API已有`nonprodbootstrap.ValidateExecutionProfile`作为environment、issuer和专用PostgreSQL DSN的authority。profile只有在以下条件全部满足时才通过：

- `YIJIE_ENV=nonproduction`；
- permission projection与secure tasks环境值均为exact `true`；
- DSN精确指向`127.0.0.1:5432/yijie_api_feat126_s10?sslmode=disable`且user/password非空；
- issuer/JWKS为冻结local realm端点；local CA path无首尾漂移且SHA-256为64位lowercase hex；
- API port是canonical TCP port。

通过后API只绑定`127.0.0.1`，使用pinned local CA client，暴露既有access/secure v2 handlers并继续隔离legacy `/v1/tasks`。`IsClosedLocalLabServiceProfile`统一上述server/route规则。既有default与`feat-125-local-lab`验证分支、错误和可观察行为保持不变，不能借新profile放宽旧路径。

### 36.3 Infra单一authority与continuation

`yijie-infra/scripts/feat-126-s10-api-runtime-profile.mjs`定义唯一closed、versioned authority，固定environment、service profile、API/DB loopback地址与端口、数据库名、issuer/JWKS和两个gate。它：

1. 拒绝missing/extra/drift字段；
2. 只从受控password、CA path与CA digest构建API child environment；
3. 由唯一S10B preflight直接导入并把同一`api_runtime_authority`写入content-free summary；
4. 通过`readApiRuntimeAuthorityFromPreflightSummary`要求canonical run ID、schema v1、`status=passed`和`scope=S10B-001-combined-preflight`完全匹配；
5. preflight对已构建API binary执行启动前双快照，将SHA-256写入closed summary的`api_binary_sha256`；
6. 提供唯一`make feat-126-s10b-api-continuation`：只接收canonical run ID与七仓完整SHA，从固定run目录读取owner-only 0600 summary/secrets、CA与preflight-built API binary，安全open/hash并要求summary digest及dev/inode/mode/size/mtime二次快照一致，强制summary reader→builder后才启动foreground child；
7. 拒绝shell复制env、caller指定profile/endpoint/database/issuer/gate/binary/path/secret、错误七SHA、artifact权限/link/size/digest/identity漂移或复用FEAT-125 profile；child raw output只计容量不落证据，launcher转发signal和exit code。

launcher已通过真实harness子进程验证：child收到`feat-126-s10-local-lab`、`nonproduction`和port `18080`，退出码被原样传播；6类summary/override/artifact负向与binary digest drift均在spawn前停止。它只启动API child，不启动Compose或其它组件，因此不宣称S10B-002–012已消费或通过。

### 36.4 Contract、安全与回滚

- `contract-impact=semantic`，范围仅为private FEAT-126 local deployment interface；central contracts、Public Tasks/Host wire、Desktop IPC、业务schema和Runtime pin不变，G2A=N/A。
- profile投影不含password、token、DSN正文或真实路径；错误保持closed/content-free。
- API与Infra候选分别基于`c5f334e88d54d9e04f388d0349f4f5925124abd6`和`5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`；Accepted clean local checkpoints分别为API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`与Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`，均未push。Governance将以本次文档收口commit形成clean local checkpoint，并在commit后记录完整SHA。
- 回滚必须成组撤销API profile与Infra authority并继续HOLD S10B；不得只撤一侧、改用floating profile或放宽validator。

### 36.5 Closure结论

API `make lint`、`make test`通过；Infra `pnpm validate`、`make lint`、`make test`与113/113测试通过，包括launcher真实child、6项负向矩阵与binary drift binding。Owner已批准DEC-126-059 Option A，S10BRP1 Closure Passed且`S10B-BLK-006` Closed。该结论不是S10B-002–012或G4证据。

### 36.6 LIA-126-022 / S10B-R6 授权边界

- 状态：`Consumed 2026-08-06 / Executed-Blocked / R6 Closure Rejected`；DEC-126-060 Option A已Accepted，`S10B-BLK-007`保持Open。
- 固定候选：Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`；Governance以本次clean checkpoint的完整HEAD为准。
- 执行必须建立fresh canonical run UUID、fresh volume/run root/token/数据库与应用状态，并严格消费既有单一preflight/continuation authority完成S10B-001–012。
- 任一SHA、authority、identity、migration、E2E、content-free、no-log、cleanup或default-off断言失败立即fail closed，不现场修复、继续或直接重跑。
- 不授权S11、MiniMax/外部模型、真实数据/Keychain、业务源码修改、default activation、push、merge、tag、publish或deploy。

## 37. DESIGN-126-013 — Closed Resolver Error Propagation

### 37.1 评审边界与工程事实

- 本次只读评审固定Governance `d5d05a137338e4d72cf69173073fe49858a9a6e3`与Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`；Infra工作树干净，未执行resolver、Docker create或S10B。
- resolver已有12个权威leaf class：`docker_cli_unavailable`、`docker_permission_denied`、`docker_daemon_unavailable`、`image_not_found`、`image_reference_unresolved`、`image_identity_invalid`、`image_repository_mismatch`、`image_digest_mismatch`、`image_platform_mismatch`、`inspect_payload_invalid`、`resolver_probe_failed`、`resolver_probe_cleanup_incomplete`。
- 唯一父preflight的通用`runCommand()`只观察子进程退出码，并把所有resolver失败折叠成`preflight_image_resolver_failed`；子stderr没有进入父错误或REJECTED证据。
- `contract-impact=semantic`，仅覆盖private FEAT-126 local deployment interface的失败语义与证据投影。central contracts、Public Tasks/Host wire、Desktop IPC、业务schema、Compose pins和Runtime pin均不变，central G2A=`N/A`。

### 37.2 方案比较

| 方案 | 结论 | 取舍 |
|---|---|---|
| A. versioned closed child result + strict parent projection | **推荐** | 保持child进程隔离与唯一preflight；可方向性测试12个leaf class、phase和cleanup；需要成组修改resolver/parent/tests |
| B. parent直接import resolver并捕获typed error | 不推荐 | 代码较少，但不再验证真实child CLI/exit/output边界，独立Make调用与父路径可能再次漂移 |
| C. 从当前human stderr提取最后一个token或直接重试 | 拒绝 | 文本不closed/versioned，Make包装和raw stderr可能污染或泄漏；重试不能恢复R6丢失的事实 |

### 37.3 唯一权威与closed result v1

1. `verify-feat-126-s10-images.mjs`继续是Docker leaf class、phase、target与result validator的唯一权威；parent以namespace import消费并先执行`validateResolverProtocolExports`，不复制第二套枚举；old child缺少协议exports时映射parent-only `preflight_image_resolver_result_invalid`。
2. parent仍只能从`make feat-126-s10b-preflight`进入；operator输入仍只有canonical run UUID和七仓完整SHA。parent内部用固定`process.execPath`、固定脚本路径和固定`--closed-result-v1`调用child，不接受env/Make变量指定mode、path、target、phase或failure class。
3. 既有`make feat-126-s10-verify-images`与无flag CLI保持原有human-readable成功/失败行为，保证old parent→new child仍走旧通道；closed mode只供同commit parent消费。closed envelope和evidence通过后，parent先重跑只读`feat-126-s10-config`（复验Compose 5.3.0、secret、REJECTED guard和rendered config），再从同一Compose profile/service authority构造固定`up --pull never`调用，避免再经human `up`路径重复执行resolver；该顺序由测试锁定。
4. closed mode只向stdout写一行UTF-8 JSON并保持stderr为空，且必须有单个末尾LF；最大2048 bytes、总spawn buffer 4096 bytes、总timeout 120 seconds。NUL、CR、多行、empty、duplicate JSON key、extra/missing key、unknown enum、错误run ID或状态/exit-code不一致全部fail closed。
5. 成功variant exact keys：`schema_version=1`、`status=passed`、`run_id`、`image_count=3`、`probe_count=3`。
6. 失败variant exact keys：`schema_version=1`、`status=failed`、`run_id`、`failure_class`、`phase`、`target`、`cleanup_state`。
7. `target`只允许`docker|postgres|keycloak|caddy`；它是Compose权威pin的content-free类别，不携带repository、tag、digest、container ID或路径。
8. `phase`只允许`capability|identity_parse|identity_inspect|identity_validate|identity_stability|probe_precheck|probe_create|probe_reconcile|probe_validate|probe_cleanup`。
9. `cleanup_state`只允许`not_applicable|absent|removed|incomplete|unknown`；它只描述本run probe资源处置状态，不授权父进程删除资源。每个failure class绑定显式合法tuple，不接受phase/target/cleanup的笛卡尔积；validation leaf在owned cleanup成功后使用`probe_validate/.../removed`，opaque cleanup故障归一化为`resolver_probe_cleanup_incomplete`。

### 37.4 Parent映射、证据与停止语义

- 已验证leaf映射为`preflight_image_resolver_<leaf>`并作为既有REJECTED v1的`failure_class`；因此REJECTED继续只有`schema_version/run_id/failure_class`三个字段，不把路径、命令、raw stderr或完整child payload复制到顶层。
- parent把已验证child envelope以create-new、0600写入固定`preflight-evidence/image-resolver-result.v1.json`；写入失败视为`preflight_image_resolver_evidence_failed`，不得继续dependencies。
- parent-only protocol class固定为：`preflight_image_resolver_process_failed`、`preflight_image_resolver_timeout`、`preflight_image_resolver_result_invalid`、`preflight_image_resolver_result_oversize`、`preflight_image_resolver_evidence_failed`。不得把raw spawn error、signal、socket、image pin或stderr拼进错误。
- 只有`status=passed`、exit 0、stderr empty、counts exact、证据成功落盘后，才允许把`images`加入completed并进入dependencies。任何failure variant或protocol class都立即停止S10B-001。
- `resolver_probe_cleanup_incomplete`、`cleanup_state=incomplete|unknown`或protocol timeout只记录并停止；parent不得猜测归属、批量remove、pull、retag、prune、切换store或重启Docker。

### 37.5 兼容、安全与回滚

| 组合 | 结果 |
|---|---|
| old parent + old child | 现有generic失败行为不变 |
| old parent + new child | old parent仍调用默认Make/human mode，行为不变 |
| new parent + new child | closed v1通过，leaf/phase/target/cleanup可复验 |
| new parent + old child | closed mode或shape不匹配，`preflight_image_resolver_result_invalid`，不得误判PASS |

- child envelope、parent REJECTED和治理证据禁止secret、DSN、token、Docker socket、真实路径、raw command/stderr、image reference/digest和container ID；只允许run ID、closed enum、计数和hash。
- Compose中的原始`version-tag@digest`、`--pull never`、network none、tmpfs覆盖、foreign resource delete=0与现有S10BD1权威全部保持。
- 回滚必须成组撤销parent closed invocation与child closed mode；旧human Make通道继续可用，但回滚后S10B保持HOLD。已产生的ignored v1 evidence可保留，不由continuation消费。

### 37.6 S10BEP1实施与退出

- 后续切片为`LIA-126-023 / S10BEP1 Closed Resolver Result Propagation Corrective`；Owner于2026-08-08另行授权并已消费。
- 实施只能修改Infra resolver、parent preflight、对应tests与Infra文档；不得修改API、Host、Desktop、Runtime、contracts、business wire/schema、Compose pins或默认feature flags。
- Closure必须通过S10BEP1-001–014、Infra validate/lint/full tests、no-log/diff、一次单独的exact no-start live resolver验证及资源归零；该live验证不是S10B-R7。
- Owner已通过DEC-126-062接受corrective Closure并关闭BLK-007；DEC-126-063已仅形成clean Infra/Governance checkpoints。fresh S10B-R7仍须后续单独授权；MiniMax、S11与真实数据继续未授权。

### 37.7 LIA-126-023实施状态

- child closed mode、同源validator/allowlist、12 leaf上下文、合法tuple与cleanup leaf保留、parent namespace protocol guard/fixed spawn/timeout/buffer、duplicate-key/末尾LF framing、leaf映射、0600 evidence、固定依赖启动参数与old/new兼容已在Infra工作树实现；默认human Make/Compose pin未改，parent不会二次调用human resolver。
- Infra `pnpm test`为128/128 PASS，`pnpm validate`、targeted 34/34、Node syntax、diff、完整`make lint/test`与Compose语义尾门禁PASS；自动化覆盖S10BEP1-001–013并复用原S10BD1-001–012回归。
- 2026-08-09在Docker client/server 29.6.1、Compose 5.3.0及daemon access均通过后，仅调用一次导出的parent resolver。canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`返回exact passed v1 envelope（3 identity/3 probe）；0600 evidence SHA-256为`e13f633fb331e3b0c0d08f22e16f7126980555ae849a73766a7bcc2259be6b34`，仅含五个success字段且无log/敏感payload。
- run级container/network/volume/listener前后均为0，daemon仍为6 containers/0 running/6 images，三项exact image Id/RepoDigest/platform前后逐项一致；没有pull或服务启动。Governance default/strict/G2A/YAML/lint/test/diff全PASS。
- DEC-126-062已接受S10BEP1 Corrective Closure并关闭BLK-007；DEC-126-063形成Infra checkpoint `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`及包含该决策的Governance本地checkpoint。S10B-R7、MiniMax、Keychain、真实数据、feature activation或远端动作均未执行；`s10b_r7_executed=false`，G3保持Partial、G4/G6 Pending。

## 38. LIA-126-024 — S10B-R7执行事实与四组件orchestrator缺口

### 38.1 已消费authority与S10B-001

- 固定七仓exact/clean、Docker client/server 29.6.1、Compose 5.3.0与daemon access全部通过；唯一fresh canonical run为`d553e6ea-e10f-4470-b357-a41807d6fb06`。
- 唯一`make feat-126-s10b-preflight`完成resolver 3 identity/3 no-start probe、fresh四依赖、TLS/OIDC、synthetic users、migration v4、closed bootstrap、API health/readiness、Host-owned fake readiness与content-free log gate，故S10B-001为PASS。summary SHA-256=`de994e3dd155e13ab27d7bb9c8645e4807e050b88fc9b300bdf62bd000612b80`，resolver evidence SHA-256=`c424a4e8e0deb405c713bc689821973f2d99b91f9ef5826d44a88e16a0177e9e`。
- summary绑定dataset `feat126-title-raw-v1`、fixture `normal-000`、dataset digest `523609b44fd244fff18b930c992375999276c2e0d5786efadfd8858ec623b308`与API binary digest `533ef53fab18ca6cd5c8882b707c50a52a14a9ae7b66680d70323157f6ab0469`；不保存prompt、assistant、raw或title正文。

### 38.2 S10B-002 fail-closed边界

- Infra已提交的`make feat-126-s10b-api-continuation`只启动固定API前台child；其runbook明确声明“不启动Compose或其他组件”，因此它不是S10B-002–012四组件编排入口。
- §17.4 process manifest仍是“冻结候选，当前不运行”，七仓没有versioned executable把same-run API、fake、Desktop supervisor、Host、pinned Runtime、ephemeral secret backend、exact-true flags、S10B-002–012顺序、content-free evidence和cleanup绑定成单一authority。
- 在此事实下调用API-only launcher再人工拼接其余命令会新造第二套authority，并违反一次授权“任一步失败立即停止、不续跑、不现场修复”。因此S10B-002在任何continuation/业务进程启动前`FAIL-CLOSED`；S10B-003–011 `NOT RUN`，S10B-012只执行abort cleanup subset且整体仍为`NOT RUN`。

### 38.3 安全、清理与后续设计门禁

- `make feat-126-s10-stop`只处理本run Compose project并保留4个named volumes。终态run container/network/process/listener均0，daemon恢复`6 containers / 0 running / 6 images`；owner-only ignored run root、binary/cache/evidence与4 volumes保留，无prune或volume删除。
- 8个允许的日志/证据文件对5个生成secret、664个冻结payload值、bearer、DSN与private-key marker全部0命中；`api-continuation.log`不存在，因为continuation未启动。
- Governance package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`全部PASS。
- `s10b_r7_executed=true`，但R7 Closure不成立。新`S10B-BLK-008`只描述完整四组件orchestrator缺失，不回退S10BEP1或BLK-001–007 Closure。
- Owner已接受DEC-126-064 Option A：接受R7 fail-closed事实、拒绝R7 Closure并保持`S10B-BLK-008 Open`。本次随后只执行DESIGN-126-014只读设计评审；corrective实施与fresh R8仍须再次分别授权，不能自动开始。

## 39. DESIGN-126-014 — Closed Four-component S10B Orchestrator

### 39.1 评审边界与影响分类

- Owner接受DEC-126-064 Option A后，仅授权`S10B-BLK-008`四组件orchestrator设计评审。本节来自Governance、Infra、API、Host、Desktop与Runtime源码/入口的只读核对；未启动Docker、API、fake、Desktop、Host或Runtime，未打开flag、访问Keychain/真实数据、修改实现仓库、commit或执行远端写入。
- 本轮文档评审`contract-impact=none`：没有改变任何跨进程、跨仓、跨版本或持久化边界的可观察运行行为。
- 未来corrective按最高风险分类为`semantic`，仅限private local test/deployment interface与独立的Desktop test-driver IPC。Public Tasks/Host既有业务wire、central contracts/SDK、SQLCipher业务schema、Runtime pin、production/default配置均不变；central G2A=`N/A`。若实施发现必须改变上述公共或持久边界，立即停止并重新分类，不能沿用本设计授权。

### 39.2 已确认的工程事实

| Owner | 当前能力 | 缺口 |
|---|---|---|
| Infra | `make feat-126-s10b-preflight`是唯一S10B-001入口；绑定run ID、七仓SHA、resolver、依赖、identity、migration/bootstrap、API/fake readiness与summary，并在返回前停止API/fake/Compose | 没有S10B-002–012状态机；`feat-126-s10b-api-continuation`只启动API，且没有依赖/fake/Desktop authority |
| Desktop | `SidecarSupervisor`使用`env_clear()`、run/nonce/port readiness与owner-only Host process evidence启动/停止Host；ephemeral secret backend按run绑定 | 只有Vitest/Rust测试和secure-storage示例；没有Playwright、tauri-driver、WebDriver或真实Vue/Pinia/Tauri E2E入口；native auth仍通过外部浏览器authorization-code/PKCE，项目选择仍走native picker |
| Host | Desktop child启动Host；Host `codex.Manager`校验固定Runtime artifact并通过stdio启动/关闭Runtime；fake支持complete/incomplete/http-error/disconnect/oversize | Runtime child没有对orchestrator可消费的PID/PPID/manifest证据；fake health不绑定mode/generation/call cap，不能证明当前case所需fault authority |
| API | closed `feat-126-s10-local-lab` profile与bootstrap verifier已存在 | 没有S10B专用、API-owned的Tasks/audit/idempotency content-free verifier；Infra不得用ad hoc SQL替代业务Owner证据 |
| Runtime | 固定artifact/manifest由Host验证，现有app-server stdio满足业务链 | 不应由Infra直接启动或修改；Runtime进程身份必须由Host authority投影 |

结论：BLK-008不能通过扩写runbook或人工shell解决。完整corrective至少涉及Infra、API、Host与Desktop；Contracts和Runtime源码不应修改。Desktop test-driver与API verifier是实现前置，不是可在R8现场补齐的测试便利项。

### 39.3 唯一operator authority与进程所有权

未来唯一operator入口固定为：

```text
make feat-126-s10b-orchestrator \
  RUN_ID=<canonical UUIDv4> \
  GOVERNANCE_SHA=<full> CONTRACTS_SHA=<full> API_SHA=<full> \
  HOST_SHA=<full> DESKTOP_SHA=<full> RUNTIME_SHA=<full> INFRA_SHA=<full>
```

- 除canonical run ID与七个full SHA外不接受path、port、profile、flag、binary、fixture、fake mode、case、resume、retry或cleanup override；同名环境变量存在即fail closed。入口自行派生run root、固定端口、artifact位置、case顺序和内部nonce。
- 单入口内部调用并验证现有唯一preflight；只从同run的0600 summary与resolver evidence继续，要求`status=passed`、cleanup passed、七仓SHA、API binary digest、dataset/fixture和run ID完全一致。operator不得先手工跑preflight再调用continuation。
- 权威父子关系固定为`Infra orchestrator -> API continuation / fake / Desktop`，`Desktop -> Host`，`Host -> pinned Runtime`。Infra不得直接启动Host或Runtime；Desktop/Host不得启动API、fake或Compose。
- preflight成功返回后，orchestrator必须通过共享的固定Compose authority重新校验并启动同run retained volumes上的依赖，再启动API、对应case的fake与独立non-publishable Desktop test build。现有API-only launcher可重构为内部受控child，但其窄default CLI兼容行为保持。
- Desktop test build必须由exact Desktop SHA生成并记录binary/frontend digest；只有编译期`feat126-s10-driver`与运行期master/run/ephemeral/driver四重闭合条件同时成立才包含并启用driver。普通Desktop build不注册driver command/event，默认bundle、`.env`、CI与production配置不含该能力。

### 39.4 Desktop真实主链与新增private test control

- 仅靠当前源码无法自动完成真实Vue/Pinia/Tauri链。corrective必须增加Desktop-owned、test-build-only closed driver：WebView侧调用真实production Pinia actions与现有Tauri chat commands，实际挂载生产Vue组件并以`textContent`/closed store projection检查UI；禁止mock client、直接调用Rust application service代替Vue/Pinia或向WebView暴露bearer/tenant authority。
- driver与Infra之间使用run-root内owner-only AF_UNIX control channel；frame固定schema version、run ID、内部nonce、monotonic sequence、closed message kind与content-free fields，设长度/数量/timeout上限。允许的消息只包括component ready、fixed fake-mode transition、planned restart checkpoint、case result和abort；禁止任意command、path、SQL、URL、env或payload输入。
- native auth使用同一local Keycloak authorization-code+PKCE链，但test build增加closed synthetic browser agent；Infra从现有secret authority派生仅含固定synthetic user identity的0600 credential file，Desktop只在same-run profile下读取并在内存中使用，禁止password grant、手写bearer或把credential传入WebView/evidence。
- native project picker在test build中只能投影run manifest内固定`project`目录，仍经过Rust canonical path/bookmark/scope校验；不弹人工dialog，不允许operator指定其它路径。
- planned Desktop restart属于S10B-005固定状态转换：orchestrator保持存活，Desktop先关闭Host/Runtime和数据库并写closed checkpoint后退出，随后由同一orchestrator重新启动同一binary/run。它不是失败后的resume/retry；任何非预期退出直接进入abort。

### 39.5 Closed state machine、case顺序与no-retry

状态机唯一合法主路径为：

```text
created -> preflight_running -> preflight_passed -> dependencies_ready
-> api_ready -> fake_ready -> desktop_ready -> host_ready -> runtime_ready
-> s10b_002 -> s10b_003 -> s10b_004 -> s10b_005_planned_restart
-> s10b_006 -> s10b_007 -> s10b_008 -> s10b_009
-> s10b_010 -> s10b_011 -> cleanup -> closed_pass
```

- 任一Gate失败或任何unexpected process exit只能转`aborting -> cleanup_passed|cleanup_incomplete -> closed_fail`；不存在case skip、reorder、continue-on-error、manual correction或自动retry。
- fake complete/incomplete/disconnect/oversize等模式由固定case表驱动。每次mode transition必须停止旧fake、证明listener释放、启动新generation并通过Host-ownedclosed health（run/mode/generation/call cap），不得接受operator env覆盖。
- bounded readiness poll只观察同一已启动identity，不重新spawn、不改配置，不算retry。S10B-007/011中的interrupt、disconnect、restart、capacity fault必须在case表中预声明；其它crash一律失败。
- 已存在run root时同一入口只允许验证authority并执行reconciliation-only cleanup，随后返回`existing_run_reconciled`失败类；绝不恢复case执行。下一次功能执行必须使用新run ID和新授权。

### 39.6 Identity、evidence与数据边界

- Infra-owned manifest记录dependencies、API continuation/API、fake和Desktop；Desktop-owned manifest记录Host；Host-owned manifest记录Runtime。每个process evidence必须包含schema/run/role、PID/PPID、binary SHA-256、start identity、closed state、exit/cleanup，以及适用的port/nonce/profile或manifest digest；禁止路径、argv、env value和正文。
- API continuation必须投影实际API PID/PPID/binary/profile digest/port；fake必须投影mode generation；Desktop必须投影test-build digest/driver nonce；Host继续投影spawn nonce；Runtime由Host投影PID/PPID、binary/manifest digest、reported version与stdio transport。listener owner必须与manifest identity一致；PID复用或identity不确定时禁止kill并判cleanup incomplete。
- 新增API-owned `verify-feat126-s10-e2e` closed verifier，使用同一profile/DSN authority只输出Tasks/audit/idempotency的计数、枚举和canonical hashes，负责S10B-009正文/title/path denylist。Infra只调用并验证结果，不复制业务SQL。
- orchestrator state、component manifests、case results与final closure全部使用create-new/no-follow、owner-only 0700/0600、single-link、bounded-size和versioned closed JSON；中央state只有orchestrator可写，component Owner只能写自身manifest。
- 每个case后及final cleanup后扫描API/fake/Desktop/Host/Runtime output、Host bbolt、Desktop evidence、Public Tasks verifier结果和orchestrator artifacts。扫描集包含5个generated secret、synthetic credential、固定prompt/assistant/raw/title/project canary、bearer/DSN/private-key marker；证据只保留scanner version、pattern-set digest、file/row count和hit count，任一意外命中立即abort。

### 39.7 Cleanup、crash containment与回滚

1. 正常或失败退出均按Desktop driver quiesce -> Desktop stop -> Host shutdown -> Runtime stdin close/kill deadline -> fake -> API continuation/API -> exact Compose stop顺序执行；随后验证固定listener、run PID/process-group、container和network为0。
2. ephemeral secret backend只由Desktop-owned exact cleanup处理；named volumes继续保留。orchestrator不得调用`down --volumes`、`docker volume rm`、prune或删除foreign/unknown PID/resource。
3. API/fake/desktop child均绑定orchestrator parent watchdog与独立run process group；Desktop已有Host parent watchdog保留，Host Runtime shutdown保持。orchestrator异常消失时child先自停；再次调用同run入口只做精确reconcile，不执行用例。
4. rollback以仓为单位撤销Infra orchestrator、API verifier、Host runtime/fake evidence和Desktop test driver；现有preflight、API-only launcher、business wire/schema、Runtime pin和default-off路径保持可用。回滚后`S10B-BLK-008`重新成为显式HOLD，不得退回人工拼接。

### 39.8 验收与下一决策

- repository corrective至少通过：closed state/shape/framing/override/old-new compatibility；Desktop production-build driver-absent与test-build真实Vue/Pinia/Tauri driver；OIDC/project binding；API verifier；Host Runtime/fake manifest；process crash/PID reuse/parent death；planned restart；no-log；exact cleanup；各受影响仓全量lint/test/build与Governance门禁。
- isolated live closure只能验证orchestrator startup/abort containment且必须记录`s10b_r8_executed=false`；不得在corrective Closure中顺带运行S10B-002–012。完整fresh R8仍需新的单次Owner授权。
- 设计评审记录完成后的Governance default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`首轮及证据登记后复跑均PASS。
- `DESIGN-126-014 = COMPLETE`，但`S10B-BLK-008`仍Open。`DEC-126-065`提交Owner评审：推荐Option A接受本设计并另行授权`LIA-126-025 / S10BO1`四仓repository corrective；该决定不得自动授权isolated live closure、fresh R8、S11、MiniMax、default activation、真实数据、commit或远端写入。

## 40. LIA-126-025 / S10BO1 Repository Corrective

### 40.1 Owner disposition与契约影响

- `DEC-126-065 Accepted Option A`；Owner只授权Infra、API、Host、Desktop的repository corrective，不授权Docker live、isolated live、fresh R8或后续阶段。
- `DESIGN-126-014 Complete`，`DEC-126-066 Accepted / LIA-126-025/S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed`。
- contract-impact=`semantic`，范围仅为private FEAT-126 local test/deployment interface与non-publishable Desktop test-driver IPC。central contracts、Public Tasks/Host既有业务wire、durable schema、Runtime pin、Compose pins和production/default配置均不变；central G2A=`N/A`。

### 40.2 实现结果

- Infra提供唯一`make feat-126-s10b-orchestrator`入口，仅接受canonical run ID和七仓exact SHA，内部消费same-run preflight并拥有closed S10B-002–012 state machine；existing run只能reconcile cleanup，不能resume。
- Desktop以非默认Cargo feature提供真实Vue/Pinia/Tauri test driver、synthetic authorization-code + PKCE agent、fixed project projection和test-driver IPC；普通production build不编译或注册该driver。
- Host提供private runtime evidence和fake `/healthz/v2`，覆盖PID/PPID/binary/manifest SHA、nonce、profile、mode/generation/call-cap；既有public/default wire保持不变。
- API提供只读、API-owned content-free Tasks/audit/idempotency verifier，固定输出count/enum/canonical hash/denylist hit count，不投影正文、title、path、secret、bearer、DSN或固定payload。
- 所有权链保持Infra→Desktop→Host→Runtime；Infra没有直接启动Host或Runtime的代码路径。

### 40.3 验证与未闭合项

- Infra `pnpm test` 142/142 PASS，S10BO1-001–014 targeted matrix 14/14 PASS。
- API、Host新增针对性测试与lint/build PASS；Desktop frontend lint、167 tests、build、默认Rust build、feature build及driver tests 2/2 PASS。
- Governance default、strict、G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`在本节登记后最终复跑均PASS。
- 最终能力前置PASS：Docker client/server `29.6.1`、Compose `5.3.0`、daemon、loopback、0700/0600临时文件、subprocess、native bookmark及SQLCipher/file-security测试均通过。
- API与Host完整lint/race/build PASS；Desktop为30个TS文件/167 tests、Rust 129 PASS/3明确ignored、production build、default build/clippy、feature build/clippy、driver 2/2及production bundle driver-absent PASS；Infra validate/lint/test、Compose semantic、142/142及独立S10BO1 14/14 PASS。
- Desktop首次默认clippy暴露`run_id`与`validate_fixed_project`仅由feature driver消费却无同源cfg；Owner随后单独授权最小`contract-impact=none`修复，在两个方法上增加`#[cfg(feature = "feat126-s10-driver")]`，未改变运行语义并通过上述全套回归。
- DEC-126-066已接受Corrective Closure并关闭`S10B-BLK-008`；G3保持Partial，G4/G6 Pending，完整fresh S10B-001–012仍未PASS。
- isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用、prune、volume删除、commit、push及其它远端写入仍未授权。

### 40.4 DEC-126-066 Owner接受边界

- Owner确认能力前置、API/Host/Desktop/Infra全量门禁、S10BO1-001–014和Governance证据PASS，接受LIA-126-025/S10BO1 Corrective Closure。
- `S10B-BLK-008 Closed`只表示四组件orchestrator repository corrective达到关闭条件；不表示isolated live或完整fresh S10B E2E已经执行。
- G3保持Partial、G4/G6 Pending；决策后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`均PASS，任何后续live、fresh R8或提交/远端动作仍需独立授权。

### 40.5 DEC-126-067 Local Clean Checkpoint Closure

- Owner单独授权并消费DEC-126-066后的local checkpoint closure；执行前七仓HEAD与scope精确匹配，Contracts/Runtime clean。
- API checkpoint=`451940b282d8dd3e232ed414bd44b0677897f4c4`，Host checkpoint=`c5939b4d8b5ebc318a7beeb49b20f343802e59b9`，Desktop checkpoint=`d51e435cb8ea224e69f9707831ee71022d0a7b6e`，Infra checkpoint=`0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c`；Governance为包含DEC-126-067的本地commit。
- checkpoint前API/Host/Desktop/Infra全量门禁、S10BO1 14/14、Governance全门禁及七仓`git diff --check`均PASS；治理更新后Governance门禁再次PASS。
- `S10B-BLK-008 Closed`、G3 Partial、G4/G6 Pending保持不变；isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认启用及所有远端写入仍未授权。

## 41. DESIGN-126-015 S10BO2 Startup/Abort Bootstrap

### 41.1 Authority and ownership

- DEC-126-068接受Option A：Infra只启动依赖、API、fake和Desktop；Desktop启动Host，Host启动Runtime。Infra不得直接启动Host/Runtime。
- Desktop non-publishable feature build注册实际bootstrap；production build不导入、注册或打包driver。bootstrap执行真实synthetic authorization-code + PKCE、same-run trusted tenant bind、native project bookmark和实际opaque project ID。
- Vue/Pinia/Tauri链路固定为`login -> register project -> bind -> revalidate -> requestLocalRecovery -> Host ready -> Runtime ready`；S10B-002–011业务case继续硬禁止。

### 41.2 Closed control and containment

- Infra与Desktop仅通过继承匿名FD3/FD4交换bounded、versioned、single-line NDJSON；frame严格拒绝unknown field并绑定run ID、nonce和单调sequence。
- EOF、abort或parent death沿Desktop -> Host -> Runtime停止，再由Infra清理Desktop、fake、API与Compose；existing run只允许exact reconcile，禁止resume、continue、retry、reorder或skip。
- PID/start identity不确定、PID reuse或cleanup outcome unknown时不得signal未知进程；状态保持fail closed。证据保持0700/0600、content-free、no-log和named-volume retention。

### 41.3 Implementation result

- Desktop checkpoint `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`，Infra checkpoint `0fed8187d6051c011e67142d90feff89de326cfe`；Contracts/API/Host/Runtime本轮源码未修改。
- Desktop 174/174 TS、default Rust 134 PASS/3 ignored、feature Rust 143 PASS/3 ignored、driver TS 7/7、driver Rust 6/6及production driver-absent PASS。Infra 162/162与S10BO1/S10BO2 34/34 PASS。
- `DESIGN-126-015 Complete`；Owner已接受`LIA-126-026/S10BO2 Corrective Closure`并关闭`S10B-BLK-009`。没有Docker/isolated live，`s10b_r8_executed=false`，G3 Partial、G4/G6 Pending。
- contract-impact=`semantic`，仅private local deployment/test与non-publishable driver IPC；central contracts/G2A=N/A。
- Closure接受仅覆盖repository corrective及其门禁证据；不授权isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、commit或远端写入。
- Owner决定登记后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`首轮及证据回填后最终复跑均全部PASS。

## 42. S10BO2 Isolated Live Fail-Closed Record

### 42.1 Execution boundary

- LIA-126-027只授权一次startup/abort live，未授权S10B业务case或fresh R8；canonical run为`b68804f0-aaf9-4da4-95e1-aa3b605bfada`。
- 七仓SHA/clean、Docker 29.6.1、Compose 5.3.0、daemon及四项本地能力全部PASS；失败不是环境能力阻断。

### 42.2 Failure projection

- `executePreflight`调用子Make时只传`RUN_ID` argument；七仓SHA以`FEAT126_S10B_*`环境名存在，但Make target的前置检查要求`GOVERNANCE_SHA`、`CONTRACTS_SHA`、`API_SHA`、`HOST_SHA`、`DESKTOP_SHA`、`RUNTIME_SHA`、`INFRA_SHA`，因此在run root建立前立即拒绝。
- cleanup初始context将`composeAttempted`固定为true；preflight尚未创建run时仍调用`feat-126-s10-stop`，其失败设置cleanup unknown。state machine按cleanup优先覆盖primary failure，最终仅投影`orchestrator_cleanup_unknown`。
- run root与五进程证据不存在，existing-run reconcile无法建立完整身份authority；禁止手工命令拼接、manual kill、retry或复用run ID。

### 42.3 Closure state

- project container/network/volume=0；六个固定listener=0；daemon恢复6 containers/0 running/6 images。该观测不等同于精确process/no-log Closure，因为证据根不存在。
- Desktop复验174/174 TS、default 134/0/3、feature 143/0/3、driver TS 7/7、Rust 6/6及production driver-absent PASS；Infra 162/162与targeted 34/34 PASS。
- isolated live Closure FAIL；`b68804f0-aaf9-4da4-95e1-aa3b605bfada`永久不可重试、续跑或复用；Owner已接受LIA-126-028/S10BO3 Corrective Closure并关闭`S10B-BLK-010`；`S10B-BLK-009 Closed`、G3 Partial、G4/G6 Pending、`s10b_r8_executed=false`保持。
- Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax和`git diff --check`首轮及本条证据回写后的最终复跑均PASS。

## 43. DESIGN-126-016 S10BO3 Failure-safe Orchestrator Closure

### 43.1 Authority and attempt consumption

- Orchestrator只接收canonical run ID与七仓exact SHA；同一authority在嵌套Make边界转换为固定`GOVERNANCE_SHA`、`CONTRACTS_SHA`、`API_SHA`、`HOST_SHA`、`DESKTOP_SHA`、`RUNTIME_SHA`、`INFRA_SHA` assignments，不从第二环境命名空间重建。
- canonical run ID在任何执行前写入`.orchestrator-attempts/<run>.attempt.v1.json`；0700真实目录和0600 create-new canonical JSON为强制条件。marker绑定owner PID/PPID/start identity、binary/script SHA与七仓SHA；failure/closure绑定marker digest且不可覆盖。
- 已存在attempt只进入reconcile，拒绝script/binary drift、active owner、缺失或不一致failure/closure；不会resume preflight、startup、abort或业务case。

### 43.2 Failure projection

- child preflight失败只接受一行closed JSON，或该行后跟唯一精确Make `Error 1` trailer；其它stderr、额外行、CRLF、oversize、未知字段或非canonical结果统一拒绝。
- `composeAttempted`只表示启动尝试发生；`composeCleanupRequired`单独决定是否调用Compose cleanup。依赖spawn前先设置cleanup eligibility，从而覆盖partial startup unknown outcome。
- 原始preflight/startup/abort failure始终是primary；cleanup、no-log、evidence write与parent death分别持久化并出现在最终closed envelope，不得覆盖primary。

### 43.3 Evidence, reconcile and cleanup

- preflight在partial owner-only run root上补齐受保护的`logs`与`preflight-evidence`目录并写closed failure evidence；未建立run root时使用attempt-only evidence，不能伪装成完整run artifacts。
- cleanup scopes固定为`pre_run_absence`、`preflight_artifacts`、`run_artifacts`；no-log scopes固定为`attempt_only`、`preflight_artifacts`、`run_artifacts`并带coverage/file count。四个named volumes按exact before/after name set验证且永不删除。
- phase决定required/possible process roles。Desktop可能已启动Host/Runtime的phase若缺少完整descendant identity，只能保持cleanup unknown；PID reuse、binary/start identity不确定、listener或Docker inventory unknown均不得signal未知进程或声明PASS。
- `s10b_r8_executed=false`为marker、failure、closure与成功projection的固定字段；S10B-002–011业务case仍硬禁止。

### 43.4 Verification and scope

- S10BO3-001–020覆盖authority forwarding、strict frame/trailer、primary/secondary precedence、single-use ledger、artifact tamper、digest binding、pre-run no-log、phase role、volume set、partial dependency/root、unknown inventory、no-resume、immutable success closure、failure-class binding、Compose log leak rejection、API/fake boundary immutability、marker-only reconcile及Host/Runtime persisted evidence。
- Infra Node syntax、`pnpm validate`、`make lint`、full `make test` `186/186 PASS`、四个targeted文件 `65/65 PASS`和`git diff --check` PASS；未执行Docker live、isolated live或fresh R8。
- contract-impact=`semantic`，仅private local deployment/test interface；central contracts、业务wire、durable schema、Runtime源码/pin、Compose pin与default flags无变化，G2A=N/A。
- Owner已接受`LIA-126-028/S10BO3 Corrective Closure`并关闭`S10B-BLK-010`。该接受仅覆盖repository corrective；不构成isolated live、fresh R8、完整S10B-001–012、G4或G6证据。后续任何isolated live仍需新的clean checkpoint和单独一次性授权。

## 44. DEC-126-070 S10BO3 Checkpoint Manifest

- Infra corrective以五个已评审文件形成local clean checkpoint `91f7ec03372b1528abb93818abfad432a83327c4`；该提交不改变Compose pin、central contracts、Runtime、default flags或业务wire。
- Governance checkpoint是包含本节、Infra精确SHA和全部门禁证据的本地commit；其精确SHA在commit形成后外部报告，避免不可实现的commit自引用。
- Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`、Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`与Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`保持clean/unchanged。
- 此checkpoint只固化repository corrective，不产生新的runtime evidence；G3 Partial、G4/G6 Pending及`s10b_r8_executed=false`不变。

## 45. LIA-126-029 Process-Identity Failure Record

- 第二次startup/abort isolated live只消费run `8b94dc6d-5984-4579-9e0c-bed43a4b872f`，未授权fresh R8或业务case。
- Make以相对`node`启动；Darwin `ps comm=`只提供`node`，无法满足orchestrator要求的absolute executable identity，因此在attempt marker、preflight与run root前返回`orchestrator_process_identity_unknown`。
- 旧claim顺序先解析process identity、后创建attempt marker；所以此失败没有run-scoped ledger、failure、no-log或cleanup证据。零container/network/volume/listener只是一项外部观测，不得升级为正式Closure。
- Public Tasks、conversation、turn与provider调用全部为0，`s10b_r8_executed=false`；该run永久不可重试、续跑或复用。

## 46. DESIGN-126-017 Absolute Node and Preclaim Authority

### 46.1 Canonical process identity

- `make feat-126-s10b-orchestrator`在同一recipe shell中用`command -v node`取得路径，要求其以`/`开头，并用该绝对路径执行orchestrator。
- Orchestrator仍以实际PID/PPID/start identity与binary SHA-256建立最终attempt marker；absolute launcher只关闭macOS `comm=node`歧义，不放宽identity validator。

### 46.2 Preclaim before fallible identity inspection

- 0700 attempt目录中先以`O_EXCL|O_NOFOLLOW`创建0600 canonical `<run>.preclaim.v1.json`，字段仅为run、七仓SHA、PID/PPID、reserved状态与`s10b_r8_executed=false`。
- 只有preclaim创建成功后才检查absolute process identity和script digest。marker成功后同时绑定preclaim PID/PPID与SHA-256；preclaim failure文件必须不存在。
- marker前失败以create-new 0600 `<run>.preclaim-failure.v1.json`持久化，内容仅含run、failure class、preclaim digest、failed状态与`s10b_r8_executed=false`。写证据失败保持原primary并投影evidence secondary。
- 已有terminal failed preclaim直接返回`orchestrator_existing_preclaim_failed`；并发claim等待同一marker/failure，有界等待后以`orchestrator_preclaim_incomplete`停止。任何路径都不resume、retry或进入preflight/业务case。

### 46.3 Compatibility, no-log and scope

- 新preclaim加入attempt-only、preflight-artifact与run-artifact no-log文件集合及file-count coverage；legacy marker-only attempt继续兼容读取/reconcile。
- Corrective只改Infra Make/orchestrator/tests四文件；central contracts、业务wire、durable schema、Runtime source/pin、Compose pin与default flags不变，contract-impact=`semantic` private interface，G2A=N/A。
- Infra `make test` `188/188`、四文件targeted `67/67`、Node syntax、`pnpm validate`、`make lint`、Compose semantic、absolute Node self identity与diff均PASS；未执行新live。

## 47. DEC-126-072 Checkpoint Manifest

- Infra local clean checkpoint=`c7edbc344daecb84553efafe86dfe335a5c0c72d`，包含四个reviewed corrective文件，未push。
- Governance checkpoint是包含本节和Infra精确SHA的本地commit；Contracts/API/Host/Desktop/Runtime保持既定clean SHA。
- 此checkpoint不产生新的runtime evidence。获得新的Governance SHA与另一份isolated-live一次性授权前不得再次执行live；fresh R8和业务case仍未授权。

## 48. LIA-126-031 Offline Root-Cause Record

- run `056a4dab-6afc-45ff-bfff-d1fcc67d2394`已形成0600 preclaim、attempt与failure；primary=`orchestrator_control_eof`，phase=`desktop_spawned`，process roles仅`api/fake/desktop`，Host/Runtime/readiness/abort evidence不存在。
- canonical Infra root是`yijie-infra/environments/local/generated/feat-126-s10/<run_id>`；Desktop旧`validate_run_root`只允许macOS temp root，因此feature Desktop在控制frame前退出。
- runtime scan完成并记录`hit_count=1`与known scope；旧closure truth table拒绝failure class与known scope同时存在，导致closure write被`orchestrator_attempt_evidence_invalid`拒绝。
- v1 scan没有命中来源/规则指纹，且containers已删除；离线审计不能恢复准确类别。该unknown不得以读取retained volume内容、猜测或模拟结果补齐。
- business boundary证据证明API before/after摘要相同、fake accepted/rejected calls均为0、`s10b_r8_executed=false`。四个retained volumes只读inspect后保持原样。

## 49. DESIGN-126-018 Minimal Corrective

### 49.1 Desktop canonical ephemeral run root

- `validate_profile_run_root`先复用owner/mode/no-symlink/canonical directory校验，再允许原有temp child。
- repository root例外编译期绑定`feat126-s10-driver`，运行期绑定`EphemeralFile`、canonical UUIDv4及精确`yijie-infra/environments/local/generated/feat-126-s10/<run_id>` suffix。
- prepare、inventory与所有root deletion路径复用同一profile validator；Protected Data Keychain与default build不接受repository例外。

### 49.2 Failure closure and content-free no-log v2

- failed closure/reconcile的cleanup与no-log各要求至少一个failure class或known scope；允许completed operation同时保留known scope与validation failure，仍拒绝两者均null。
- `runtime-log-scan.v2`对命中的container identity set和closed rule-name set去重、排序后写SHA-256；空命中必须绑定empty-set digest，非空命中必须绑定两个非空set digest。
- evidence只包含counts与digests；不写raw content、token、secret、业务文本、path或规则名称。validator兼容历史v1，旧run保持原样。

## 50. DEC-126-074 Checkpoint Manifest

- Desktop local clean checkpoint=`9771da11c47406e45526dea104f3d7de05701fba`；Infra local clean checkpoint=`61062143fa3c81b90792ec6f48aea7d6408ed06d`；均未push。
- Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`与Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`保持clean/unchanged。
- Governance checkpoint包含本节和两个实现SHA；其精确SHA在commit后报告。此checkpoint不产生live证据，失败run与四个retained volumes不变。

## 51. DESIGN-126-019 Unified Startup-Surface Corrective

### 51.1 Desktop ready boundary

- feat126_s10_driver.rs 维护 ready-resolution 原子边界和 closed startup-failure allowlist；native bootstrap、app-data/Tauri setup、control-monitor 初始化及 driver 阶段失败只发送一次受限 startup_failed frame（run ID、nonce、sequence、kind、failure class）。
- lib.rs 在 driver 构造或 Tauri setup 失败时从受信环境发送受限 leaf；start_control_monitor 及 Tauri run 返回错误在 component_ready 前投影为 startup failure。成功写出 component_ready 后标记 startup 已解决，abort 或迟到错误不得重新打开 startup 阶段。
- s10b-driver.ts 按 stage 将未知异常归类为 closed failure class 并丢弃 native 错误正文；main.ts 包住 root/bootstrap 入口，保证 ready 前初始化失败走同一 fail-closed 路径。Frontend 仅可向 Tauri 发送 allowlisted class。
- Rust 和 TS allowlist 必须同源对齐，至少包含 driver_control_monitor_invalid；unknown class、malformed frame、错误 run/nonce 或多余字段均不能穿越 FD4。默认构建和 Protected Data Keychain 路径不启用该例外。

### 51.2 Infra frame/child ordering

- validateStartupFailureControlFrame 先验证 authority 形状，再验证 frame；任何 null、extra key、错误 UUID、sequence 或 allowed-kind 集合都映射为单一 closed invalid leaf，不能触发 TypeError 或把外层 EOF 当作 primary。
- Desktop FD4 reader 以有限缓冲和 child lifecycle 协同：先消费已到达的完整 frame，再处理同一 tick 的 child exit；合法 startup_failed 优先作为 primary，只有 FD4 确实无合法 frame 时才使用 orchestrator_control_eof fallback。无 startup continuation、retry、resume 或业务 case。
- primary failure、secondary cleanup/no-log/closure 状态和 single-use attempt ledger 沿用既有 content-free envelope；startup failure 仍进入 canonical one-shot cleanup/closure 流程，但不会启动未到达的 ownership 阶段。

### 51.3 Runtime log authority and classification

- runtime source listing 必须返回且严格验证四个 closed service roles：feat126-s10-api-db、feat126-s10-keycloak-db、feat126-s10-keycloak、feat126-s10-caddy；每项同时匹配 run-derived project、FEAT-126、S10E、canonical run ID 和 synthetic-only data classification。unknown、duplicate、missing、extra 或 foreign labels fail closed。
- source digest 使用稳定 compose:<service_role> origin 并按 ASCII deterministic sort；container ID 仅用于读取日志，不进入 stable source identity，因此临时 ID 轮换不改变 source digest。命中摘要绑定去重后的 origin set、rule set 及 origin-rule pair set。
- schema v3 reader 必须保持 v1/v2 正向读取；hit_count=0 强制三组 hit 摘要均为 SHA-256(empty set)，非空命中必须存在对应的非空集合和 pair 绑定。evidence 只含 counts/digests。
- no-log 扫描使用 JSON/value-aware 分类：无内容的 health/ready 结构和空 argv 通过；token、secret、DSN、private key、绝对本机路径及未分类高风险值失败。规则名称只参与 digest，不写入 evidence 正文。

### 51.4 Scope and rollback

- Product scope closes over four Desktop files listed above plus their targeted test; Infra closes over the existing orchestrator and S10BO2/S10BO3 tests. Contracts/API/Host/Runtime files are explicitly out of scope.
- contract-impact=semantic is private deployment/test only; central G2A is N/A. No Docker, real process, isolated live, fresh R8, business case, S11, MiniMax, Keychain, real data or remote action is part of this corrective.
- Rollback is per repository and must remove the paired Desktop/Infra authority together; do not restore relative Node, temp-only root validation, race-prone EOF projection or broad value-blind no-log rules. Implementation checkpoints are Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd` and Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`, both local clean/not pushed. Repository tests, targeted matrices, syntax, build, clippy, validate and diff gates passed. The Docker-backed Compose semantic wrapper was not retried under the original no-Docker corrective authorization after discovery exit 125; a later config-only authorization completed direct Compose config plus Infra `make lint/test` with `192/192` and semantic validation PASS, without lifecycle or live actions. DEC-126-076 accepts the Corrective Closure and closes the environment-bound Compose gap; the real Tauri `AppHandle/setup` direct fixture remains P2/live, so G3 stays Partial and G4/G6 Pending.

## 52. DEC-126-076 Owner Acceptance Boundary

- Owner接受DESIGN-126-019 / LIA-126-033 repository Corrective Closure；该接受不新增或修改public contract、Host wire、durable schema、Runtime pin、Compose pin或default behavior，`contract-impact=none` for this governance disposition。
- 真实Tauri `AppHandle/setup` direct fixture仍属于P2/live；repository evidence不能替代真实startup、ownership、readiness、abort或cleanup证据。
- 后续isolated-live必须基于包含DEC-126-076的新Governance checkpoint及其余六仓精确clean SHA取得独立一次性授权；本记录不授权fresh R8或业务case。

## 53. DESIGN-126-020 Startup Durability and Explainable No-Log Closure

### 53.1 Desktop startup terminal

- Native bitmap记录setup entry、`AppHandle` available、page-load started/finished、frontend bootstrap和first driver IPC；50秒watchdog只投影closed failure class，不携带panic值、path、token、secret、日志正文或业务内容。
- setup panic由content-free guard封闭；timeout、page-load未完成、frontend未bootstrap及first IPC缺失均映射唯一`startup_failed`。first-terminal-wins，`startup_failed`或`abort_complete`写入后flush并关闭FD4，再允许child exit。
- real Tauri mock `AppHandle/setup` fixture仅运行Desktop本地测试进程，不启动网络、Docker或业务调用。该fixture证明repository setup wiring，不替代真实isolated-live AppHandle/WebView lifecycle。

### 53.2 Infra immutable failure observation

- `runStartupAbortFlow`在进入abort、business boundary和cleanup之前对primary observation执行一次且仅一次持久化；持久化失败作为secondary evidence failure，不触发retry。
- `desktop_starting`/`desktop_spawned`允许API/fake/Desktop exact known scope承载timeout、EOF、frame-invalid/order-invalid、API/fake/Desktop early-exit及closed Desktop startup leaf，即使Host/Runtime尚未启动；unknown scope或额外descendant仍fail closed。
- FD4完整frame对同tick Desktop exit拥有优先级；failure/closure继续绑定run ID、七仓SHA、attempt/preclaim digest及`s10b_r8_executed=false`。

### 53.3 Caddy structured-log classification

- runtime-log-scan保持schema v3与exact Docker authority。Caddy `request`、headers和response headers按nested value-aware方式递归；`/healthz`/`/healthz/v2`等公开健康元数据不构成命中，真实敏感header/value仍失败。
- evidence仅写origin/rule/field-class及origin-rule-field-class集合的稳定SHA-256、counts和状态；不写字段名、值、路径、日志正文或业务内容。legacy v3读取保持兼容。

### 53.4 Accepted boundary

DEC-126-077接受DESIGN-126-020 / LIA-126-035 Corrective Closure并关闭`S10B-BLK-013`。Desktop=`713bd5a2985c491db5d6cfc3e31f8f509994427d`，Infra=`222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`；G3仍Partial，G4/G6 Pending。下一次isolated-live必须另行授权并使用包含DEC-126-077的新Governance SHA。

## 54. DESIGN-126-021 Production Assets and Runtime-log-scan v4

### 54.1 Production asset authority

- Canonical Desktop build invocation is `cargo build --features feat126-s10-driver,tauri/custom-protocol` through one closed helper.
- The helper accepts only the exact ordered feature vector and fails closed otherwise. `TAURI_CONFIG` and run-root `frontendDist` remain bound to the exact clean Desktop authority.
- Semantic tests must prove no `pnpm/npm/yarn dev|serve`, `devUrl`, `localhost:1420/1421` or `127.0.0.1:1420/1421` dependency. Validation itself may not start a real Desktop/Tauri process.

### 54.2 v4 evidence shape

- Writer emits only `schema_version=4` with the 14 exact keys listed in the contract plan.
- Two new digests bind the unique sorted reason-class set and the unique sorted `[origin, rule, fieldClass, reasonClass]` tuple set.
- Reason classes are a closed six-value authority: `literal_authority_match`、`local_machine_path_value`、`sensitive_nonempty_value`、`unclassified_context_value`、`unclassified_caddy_system_value`、`unstructured_pattern_match`。
- The digest input is unique values sorted by stable ASCII order and joined with LF. Zero hits hash the empty string; positive hits may not retain an empty-set digest for any applicable hit dimension.
- Caddy approval is origin-aware and value-aware for a closed system metadata allowlist. Unknown keys/values/shapes remain `unclassified_caddy_system_value` and fail closed.
- Evidence never includes the raw origin input, field name, field value, path or log row. Exact Docker labels, four closed service roles and canonical source-set digest remain unchanged.

### 54.3 Compatibility and checkpoint ordering

- Validator reads v1, v2, both v3 shapes and v4 by exact-key version dispatch; writer never emits an older version.
- Phase 1 edits and commits Governance only from exact HEAD `5da2d93b7c4e3ee9884b0fedb04261b5aaf65f92`; Infra remains at HEAD `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1` with its four expected dirty corrective files unchanged.
- Phase 2 begins only after Governance is clean. It resumes that same Infra diff, finishes config-only/static gates and independent review, then creates one Infra local checkpoint. No live authorization is implied.
