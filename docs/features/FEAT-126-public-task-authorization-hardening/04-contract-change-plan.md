# FEAT-126 契约与兼容变更计划

> 本文central contract设计已通过G2/G2A重审。DEC-126-034已接受S8B Closure，DEC-126-035已接受远端事实；LIA-126-007/S9只增加test-only dataset/runner/consumer fixtures，不修改central source、22个commands、7个events、Host/Public Tasks wire或Runtime pin。旧`c000a024`、Draft PR #1和各`origin/develop`保持不变。

## 1. Contract Impact 结论

- 分类：`breaking`。
- 最高风险理由：现有 Public Tasks允许匿名请求并把body `tenant_id`当归属；安全目标要求bearer、权威tenant/resource/action checks、新拒绝/error/cache semantics，旧有效consumer会失败。Agent session event v1同样是`schema_version=1` closed `oneOf`；直接加入raw-reasoning variants会使严格旧consumer校验失败。
- 边界：Public Tasks HTTP、Agent Host local HTTP/SSE、Runtime canonical stdio、Desktop WebView↔Rust commands、Desktop private DB migration。
- 业务/安全语义变化：是；涉及身份、租户、所有权、删除、排序、流式重放、审批显示与restricted raw model reasoning。
- 兼容策略：Public Tasks 根据 consumer ownership 走条件分支；存在任何 supported/unknown external consumer 时必须 versioned expand/migrate，只有 owner 证明旧 `/v1/tasks` 从未发布且无支持消费者时才可评审同路径 pre-release replacement。Agent events 新建 v2 权威 schema，通过 `event_schema_version=2` 明确 negotiation，v1 默认不产生新 variant；先升级 consumer tolerance，再启用 Host producer。private DB 使用版本化 migration；现有 Runtime 已有目标协议能力，优先保持 pin，不预设 Runtime source change。

## 2. 权威源与责任

| 契约/边界 | 权威源类别 | 仓库与候选路径 | Owner | Producer | Consumers |
|---|---|---|---|---|---|
| Secure Public Tasks HTTP | central contract | `yijie-contracts/openapi/public/public.yaml#/paths/~1v2~1tasks*` local candidate | platform-team | yijie-api | yijie-desktop + unknown-public category |
| Agent Host local HTTP | central contract | `yijie-contracts/openapi/agent-host/agent-host.yaml` | platform-team/agent-runtime-team | yijie-agent-host | yijie-desktop |
| Agent session events | central contract | `jsonschema/agent/session-event-v2.schema.json` + AsyncAPI + `yijie.events.v2` Proto local candidate | platform-team | yijie-agent-host | yijie-desktop |
| Runtime app-server | runtime canonical | pinned yijie-codex app-server schema | agent-runtime-team | yijie-codex | yijie-agent-host |
| WebView↔Rust commands/events | private Desktop IPC | DESIGN-126-005；`yijie-desktop/src-tauri/schemas/chat-ipc-v1.schema.json`为source，Rust serde DTO与TS runtime validators由golden conformance绑定 | client-team | Tauri Rust | TypeScript store/view-model；未来Vue |
| conversation DB | private durable schema | future Desktop migrations | client-team | Tauri Rust repository | current/future Desktop versions |
| MiniMax Responses | third-party | provider official protocol + locked Runtime config | provider/runtime owner | MiniMax | yijie-codex |

生成 DTO、SDK、handler types、DB rows、Vue stores、Host bbolt 和 examples 均不得成为第二权威源。

## 3. 语义设计

### 3.1 Secure Public Tasks 请求候选

- 当前 `/v1/tasks` 仍是匿名、body `tenant_id` 归属语义，且 local FEAT-125 profile/ingress 主动双重隔离；本设计不得把“已隔离”误写为“已迁移”。
- 使用 `Authorization: Bearer <user token>`；token 只在 native/service transport 层存在。
- 使用严格 `X-Yijie-Tenant-ID` 作为 untrusted selector；API 独立验证 principal、active membership 与 tenant scope。
- Create request 移除权威 `tenant_id`。若迁移期暂保留，只允许与 verified scope 精确一致且不参与授权；最终删除。
- **LIA-126-002发现的阻断冲突**：历史candidate把`CreateTaskV2Request.input`与`TaskV2.input`定义为`additionalProperties:true`，canonical fixture使用`task_type=conversation`和`input.text`，response继续回显。它不能证明prompt/message/raw reasoning/title派生正文/项目路径不会进入Public Tasks或PostgreSQL。DEC-126-023方案C已接受，旧`c000a024`未amend。
- 新source已冻结为closed、content-free `task_type=conversation`与`TaskContentReferenceV2(schema_version=1, content_mode=local_only, opaque UUID)`；request/success不含title/result/error正文，v2 error body只含closed code。replacement完整commit `29317b6426578749dc698fc2ad32b986ee5c8e9f`已由DEC-126-024批准为唯一candidate；该批准不自动恢复S4，LIA-126-002须另行明确授权。
- 明确 task ownership。推荐 `created_by_user_id` 由 verified principal 写入，不由 client 提供。
- operation 至少覆盖 create/get；list/rename/pin/delete 只有在决定由 Public API 管理 metadata 时才进入该契约。本地-only 操作不得伪造为 public capability。
- 资源操作调用 `AuthorizationService.Check(user, tenant, resource, action)`；unknown action 默认拒绝。
- Create、rename、pin、delete 等写请求必须有 bounded idempotency/request ID；永久 delete 不自动 retry。
- List 候选 cursor pagination，排序为 pinned/last activity/stable ID；禁止 offset 导致并发漂移，具体字段在 G2 冻结。

### 3.2 Public Tasks 响应/错误候选

- 成功响应不返回 secret、message body 或授权内部原因；`Cache-Control: no-store`。
- 稳定错误：`400 invalid_request/invalid_tenant_context`、`401 unauthenticated`、`403 access_denied`、`404 task_not_found`（防存在性策略）、`409 conflict/idempotency_conflict/active_turn`、`503 authorization_unavailable`。
- 未授权 resource ID 的 403/404 策略必须对同一 caller 不产生可枚举差异；审计保留真实内部分类。
- Task response 的 tenant/user 字段是已验证 context，不是下游授权票据。

### 3.3 Agent Host 请求/响应候选

- 现有 start/resume/turn/interrupt 保持；Desktop 不发送 user-selectable reasoning effort。
- pinned Runtime canonical app-server 已有 `thread/delete`，source/tests 表明它删除目标 thread、spawned descendant rollouts 与 associated state，并发出 `thread/deleted`。2026-08-02 exact binary/temp `CODEX_HOME` 验证确认同进程/重启不可 read、state row/rollout/index 清除；同时在 Runtime WAL/log 发现 canary/ID 字节，因此该方法只证明 functional live-store delete，不证明 forensic erase。每个 Desktop session 必须独占一个 Runtime thread tree；Host 在检测到另一 session/shared mapping 指向该树时中止。候选 `POST /v2/agent-sessions/{id}/cleanup-operations` 桥接 stable method，清除 mapping/in-memory replay，按Runtime tree/Host mapping/Host replay返回幂等分表面结果和稳定`cleanup_incomplete`；不得用空204或RPC成功冒充所有表面完成。为处理mapping清除后成功响应丢失，Host另留30天content-free operation receipt（operation ID、keyed session hash、surface outcomes、timestamps/schema version；无raw session/thread ID/正文/title/reasoning/path）；它不是业务mapping或第二份Desktop receipt权威。
- Runtime 的 `thread/name/set` 只保存调用方提供的名称，不生成标题。Accepted ADR-0015 要求独立 Host title-generation operation：Desktop 提交 `operation_id`、session/task correlation 与首条用户文本；Host 在空临时 cwd 创建 `ephemeral=true` pathless Runtime thread，固定 `title-v1` prompt 与 turn-scoped strict `{title:string}` `outputSchema`，拒绝工具/reverse request，完成后 unsubscribe 并清除 Host correlation。ephemeral thread 不产生 rollout path且 canonical Runtime 不允许 `thread/delete`，不得伪报 delete。parse 后执行 NFC/单行/control+bidi+HTML/Markdown/40-grapheme validation；未知结果不自动 retry，最多初次 + 1 次确定失败重试，人工标题优先。`MM-126-001` 单次 strict title PASS，但不替代 production Eval。
- G2 contract candidate 精确形状为 `POST /v2/agent-sessions/{agent_session_id}/title-generations`。strict request 只含 `operation_id` UUID、可选 trace/request correlation 与 `input`（首条用户文本在 UTF-8 边界截至 8 KiB）；同步结果只返回 `{operation_id,title}`，不返回 prompt、raw provider response 或 ephemeral thread ID。稳定错误使用 `invalid_request`、`session_not_found`、`title_operation_conflict`、`title_generation_unavailable`、`title_output_invalid`；相同 operation+input 可返回缓存的进程内结果，相同 operation+不同 input 必须 409，未知网络结果不得自动换 operation 重试。该 endpoint/schema 只有 Owner 批准和 G2A source-contract slice 后才能建立。
- 候选新增 history reconciliation 能力仅在 Runtime canonical schema 支持并批准时引入；否则 local DB 是正文展示权威且 replay gap 为阻断风险。
- 所有 local Host operations 继续 owner-only bearer、loopback、no-store；trace/tenant/user 是 correlation，不替代 Public API auth。

### 3.4 Agent session event 候选

- DESIGN-126-003/DEC-126-017 冻结 closed v2 候选。保持现有 envelope 语义：`schema_version=2`、event/stream ID、stream-local monotonic `sequence`、occurred_at、task/session/thread/turn/item IDs、terminal、payload；`turn_id`/`item_id` 对两个 raw variant 必填，`terminal=false`。
- v2 只新增两个 raw variant，request/response 均 `additionalProperties=false`：
  - `item.reasoning_text.delta`：payload 精确为 `{content_index, delta}`；`content_index` 是 `0..7` 整数，`delta` 是非空有效 UTF-8，单 event 最多 16 KiB。它只用于低延迟内存展示，不是 durable truth。
  - `item.reasoning_text.finalized`：payload 精确为 `{status, contents, reason_code?}`；`status` 为 `complete | incomplete | unavailable`；`contents` 是按 `content_index` 升序且索引唯一/连续的 `{content_index,text}` 闭合数组。`complete` 要求至少一个非空 part 且无 `reason_code`；`incomplete` 要求至少一个可用非空 part 且必须有 reason；`unavailable` 要求空数组且必须有 reason。
- stable `reason_code` closed enum：`reasoning_not_emitted`、`turn_interrupted`、`stream_gap`、`runtime_error`、`limit_exceeded`、`protocol_error`、`host_shutdown`。协商v2的turn若到`turn.completed`仍为0个reasoning item/finalized，Desktop在turn级写`unavailable/reasoning_not_emitted`，不伪造item ID/body。unexpected Desktop crash若没有收到finalized/受控interruption，不得从delta buffer猜造durable record；重开后按turn state显示`unavailable`。
- 固定容量：每 turn 最多 8 个 reasoning items；每 item 最多 8 个 parts；单 part 最多 64 KiB；单 item 最多 128 KiB；单 turn 最多 256 KiB；Host 既有单 event 1 MiB hard limit 继续生效。所有大小按 UTF-8 bytes 计算。任一上限超过即发显式 `limit_exceeded` finalized 或使 reasoning Gate FAIL，禁止静默截断、丢 part 或用 answer 冒充。
- Runtime canonical `item/reasoning/textDelta` 映射 delta；completed `ThreadItem::Reasoning.content[]` 是 finalized `contents` 的唯一权威。Host 只在进程内聚合，不把正文写入 bbolt/replay/log/metric/trace/audit/error；不得透传完整 Runtime item/provider response。
- Desktop 以 `event_id` 去重、按 `(stream_id,sequence)` 验证有序性、按 `(turn_id,item_id,content_index)` 拼接。finalized `contents` 替换而非追加 delta buffer；完全一致为 `complete`，可用前缀但中断/gap/冲突为 `incomplete`，无可用正文为 `unavailable`。answer terminal 与 reasoning 状态相互独立。
- v1 继续只返回既有 8 variants；new Desktop 先支持并显式协商 `event_schema_version=2`，Host producer 默认关闭，只有 v2 协商成功才发送 raw variants。原 public-summary variants 未形成 source contract，不再作为 FEAT-126 候选发布。
- 新 title/cleanup 结果若通过 events 传递，采用独立 variant，不重载 `item.completed` 既有语义。
- 至少一次交付；consumer先解析envelope。future unknown variant只记录content-free metric并推进delivery cursor，避免replay loop；但不得推进business terminal、创建正文或执行动作。
- terminal turn 仍只有一个；warning/error 不自动结束 turn。

### 3.5 Desktop IPC/private DB（S8A Accepted implementation）

- 所有私有IPC对象均为`schemaVersion: 1`、camelCase、closed object/union；未知字段、未知command/event kind或越限值fail closed。authoritative JSON Schema、Rust serde DTO、TypeScript类型及运行时validator由固定fixtures和allowlist/ref测试证明同形，禁止手写宽松影子DTO。该私有IPC不进入`yijie-contracts@29317b...`，不改变G2A source identity。
- Rust建立`ChatAuthorizationContext`：`chat_bind_context_v1`只接受不可信tenant selector，Rust调用native auth authority复验signed-in、tenant membership、capability revision/expiry，并绑定本地`ChatScope`。owner user identity只来自Rust-owned authority，永不接受/回显WebView值。成功只返回随机opaque `contextId`、`expiresAtEpochSeconds`和allowlisted `allowedActions`；不返回tenant/owner/revision。context最多5分钟且不超过权威projection expiry，logout、tenant切换、同revision重新绑定、revision回退/到期立即使旧context失效并清空订阅。
- Local-only action policy固定为：list/history需`task.read`；create/send、rename/session pin、interrupt和delete需`task.create + task.read`；project choose/revalidate/pin/remove另需`workspace.use`。这是Desktop local conversation policy，不给Public Tasks增加新action，也不允许UI capability取代Rust检查；unknown action、foreign ID或scope mismatch一律拒绝。
- command名固定为：`chat_bind_context_v1`、`chat_list_projects_v1`、`chat_pick_project_v1`、`chat_revalidate_project_v1`、`chat_create_session_v1`、`chat_submit_turn_v1`、`chat_list_sessions_v1`、`chat_load_history_v1`、`chat_load_reasoning_v1`、`chat_rename_session_v1`、`chat_set_session_pinned_v1`、`chat_set_project_pinned_v1`、`chat_remove_project_v1`、`chat_interrupt_turn_v1`、`chat_delete_session_v1`、`chat_get_cleanup_status_v1`、`chat_subscribe_session_v1`、`chat_resync_session_v1`、`chat_cancel_request_v1`与`chat_unsubscribe_session_v1`。现有unversioned foundation invokes不得作为S8真实conversation链继续扩散；内部迁移/移除另行测试。
- 普通request envelope精确为`{schemaVersion, requestId, contextId, payload}`；bootstrap `chat_bind_context_v1`是唯一例外，精确为`{schemaVersion, requestId, payload:{tenantSelector}}`且成功后才取得`contextId`。`requestId/contextId`为UUID，write payload另含client-generated UUID `operationId`并服从Rust持久幂等。请求不得含owner/user ID、canonical path、Host bearer、SQLCipher key、Host/Runtime ID、provider/model/effort、任意SQL或Host原始payload。响应精确为`{schemaVersion, requestId, data}`，只返回stable UI DTO与opaque resource ID。
- stable error精确为`{schemaVersion, requestId?, code, retryable, recovery, retryAfterMs?}`；`recovery`仅允许`none|sign_in|rebind_context|request_permission|fix_request|reload|resync|retry|start_host|wait_cleanup|reduce_input|reselect_project`，`retryAfterMs`为0..60000。`code`来自DESIGN-126-005 closed allowlist（auth/context/capability/resource/project/cursor/request/cancel/conflict/turn/host/storage/protocol/limit/cleanup/temporary）；不得返回message/detail、path、SQL/provider/Host body、token或正文。未来Vue只把code映射为本地化文案，不能显示Host原始错误。
- pagination cursor是Rust生成的opaque base64url string，最多256 bytes，绑定context、scope、query和process epoch，最多10分钟；进程重启、scope变化、篡改或过期返回`chat_cursor_invalid`并要求从首页重载。session页最多50项/512KiB；history默认20、最多50 turn且总响应最多4MiB（至少允许1个符合单turn上限的record）；reasoning正文一次只加载单turn、最多256KiB；resync snapshot最多包含1MiB assistant文本和256KiB raw reasoning。
- 唯一Tauri event channel为`yijie.chat.event.v1`。closed envelope包含`schemaVersion`、`subscriptionId`、`contextId`、`sessionId`、可选`turnId`、十进制字符串`projectionSequence`、UUID `eventId`、`kind`与closed `payload`。kind仅为`assistant_append`、`reasoning_append`、`turn_state`、`turn_terminal`、`cleanup_state`、`resync_required`、`context_invalidated`；Host envelope/message/ID/sequence/error不得透传。reasoning只含local item ordinal、content index和validated plain text。
- 单subscription Rust队列最多64 events或256KiB，连续append在上限内合并并最多20Hz投递；单assistant append≤64KiB、reasoning append≤16KiB。overflow/drop/gap后停止普通progress，投递不可丢的`resync_required`；`turn_terminal`与`context_invalidated`同样不可丢。Tauri event无ack，因此TS store要求sequence精确连续，duplicate可忽略，gap/mismatch必须丢弃增量并调用`chat_resync_session_v1`。
- 每个read/subscription request都可由request ID取消；Rust接受后的durable write不能被`chat_cancel_request_v1`回滚，UI改用operation ID查状态。停止生成只能调用interrupt。TS store维护`contextId + subscriptionId + selectionEpoch`，切tenant/session时同步清内存并取消旧读；任何late response/event不满足三元绑定都丢弃。WebView永不直接调用outbox dispatch或Host retry。
- Desktop/Host进程重启使context、subscription和process-bound cursor失效；Rust S7C coordinator从SQLCipher恢复pending/expired outbox、active turn、cleanup operation与last cursor，unknown outcome继续fail closed。S8A store重新bind并通过新subscription/resync从Desktop权威历史及content-free cleanup状态恢复；Host replay 409不允许猜测拼接，必须进入明确reconcile/resync状态。
- private DB source 维护 schema version、migration checksum、FK/unique/index constraints；所有 top-level reads 带 owner user+tenant scope。DESIGN-126-003 固定 `0001_chat_core` 与 `0002_chat_reasoning_v2` 两个 forward-only migration；旧 app 只读/忽略其不支持的新 private schema，不执行 down migration，新 app 对 future version/checksum drift/`foreign_key_check` failure fail closed。
- delta 只在 Desktop 内存 reducer 聚合；finalized 或受控 interruption 以一个 SQLCipher transaction 更新 `chat_turns.reasoning_status/reason_code` 并替换对应 reasoning item/parts。history session list 不读取正文；turn page 默认 20、最大 50，只批量返回 reasoning metadata；用户展开时一次加载单 turn raw body，最大 256 KiB，避免 N+1。
- session 永久删除返回按 data surface 分项的 completion；只要 Host/Runtime required cleanup 或 Desktop `wal_checkpoint(TRUNCATE)` 未完成，UI 不显示全部成功。成功语义仅为当前 app-managed live stores 不可重新打开/resume，不得升级为所有磁盘痕迹抹除。

### 3.6 DESIGN-126-006 Desktop-private readiness extension candidate

现有20个S8A commands与7个`yijie.chat.event.v1` variants保持原shape和语义；本候选不静默扩展event channel，也不改变central contracts。只新增两个closed Desktop-private command：

| Command | Request payload | Response data | Side effect/authority |
|---|---|---|---|
| `chat_get_local_readiness_v1` | `{}`；普通context-bound request envelope | `{lifecycle,host,runtime,storage,canSend,issueCode,retryable,recovery,retryAfterMs?}` | read-only；Rust按本次process nonce、Host preflight、Runtime ready与SQLCipher状态计算；不返回endpoint、PID、path、version原文或底层错误 |
| `chat_request_local_recovery_v1` | `{operationId,intent:"start_or_retry"}` | 同一readiness projection | Rust验证context/capability与stable operation ID后，由Rust coordinator负责start/retry/backoff；WebView不能指定binary、URL、token、cwd、env或任意action |

- `lifecycle`: `starting|ready|blocked|recovering`；`host`: `starting|ready|unavailable`；`runtime`: `starting|ready|unavailable|version_mismatch`；`storage`: `ready|read_only|full|corrupt|migration_failed|unavailable`。`canSend=true`当且仅当Host、Runtime、storage均ready且context仍有效。
- `issueCode`仅允许`null|chat_host_starting|chat_host_unavailable|chat_runtime_starting|chat_runtime_unavailable|chat_runtime_version_mismatch|chat_storage_read_only|chat_storage_full|chat_storage_corrupt|chat_storage_migration_failed|chat_storage_unavailable`；不含message/detail。
- 新增recovery allowlist仅为`none|retry|start_or_retry|free_space|repair_or_restore|restart_app|rebind_context`；Vue本地化固定文案，不能执行任意命令。对storage corrupt/migration failed不自动写修复；保持writer关闭并引导受控恢复。
- 本extension必须同步更新Desktop-owned JSON Schema、Rust `deny_unknown_fields` serde DTO、command registry/capability、TypeScript exact validator/client/store与golden fixtures。旧20 commands/7 events的fixture equality必须继续PASS；新命令必须有unknown-field/enum/size/auth/expiry/revision/no-log/duplicate operation/restart测试。
- 这是本次盘点触发并已由DEC-126-032/LIA-126-005关闭的private IPC停止条件与`semantic` Desktop-private contract。实现固定为两个closed commands；旧`chat_start_local_host`未进入TypeScript/Vue，S8B不得轮询裸command或猜测ready。

### 3.7 审批与审计

- 本期 permission entry 是 fixed policy projection，不是写审批 command。
- 未覆盖的工具/文件/platform write reverse request 继续 method-not-found/deny。
- 必需审计：request/trace、internal user、tenant、resource/action、policy/authorization revision、outcome、stable reason、timestamp；不含消息/raw reasoning/title/path/token/key正文。

## 4. 兼容方向

```text
Public Tasks breaking:
  completed repo-local inventory + safe unknown-public classification
    → secure /v2/tasks expand provider → migrate/pin known consumers → observe
    → keep /v1/tasks host-profile + ingress denied throughout migration
    → retire v1 after ≥30 calendar days + ≥2 Desktop release candidates
       + owner attestation + zero approved/authenticated v1 use

Agent Host new output/events:
  publish session-event v2 contract + fixtures
    → Desktop explicitly negotiates event_schema_version=2 and tolerates unknown
    → deploy Host v2 producer disabled (v1 remains default)
    → enable raw-reasoning/title/cleanup flags independently
```

| Version combination | Request | Response/Event | Expected | Planned test |
|---|---|---|---|---|
| old Public provider + new consumer | new secure operation unavailable | old Task shape | consumer remains flag off; no fallback to anonymous route | CON-001 |
| new Public provider + old consumer | old route still isolated/explicit compatibility lane | old supported response only | no silent auth semantic switch; traffic denied or stays approved legacy lane | CON-002 |
| new provider + new consumer | bearer + verified tenant + scoped action | secure errors/no-store | success/deny per principal | CON-003 |
| old Host + new Desktop | no raw-reasoning/cleanup/title op | only existing8 events | reasoning capability不满足，FEAT-126 raw flag/发布Gate保持关闭；不得时长-only冒充PASS | CON-004 |
| new Host + old Desktop | no v2 negotiation | v1 existing8 variants only | old consumer never receives raw-reasoning variants | CON-005 |
| new Host + new Desktop | `event_schema_version=2` + fixed requests | exact raw-reasoning variants/title/cleanup results | full approved behavior；纯文本、sequence/completion、no-log和missing-raw Gate fixtures pass | CON-006 |
| old Desktop + expanded local DB | old app ignores DB/new fields | N/A | no corruption; rollback app does not write unsupported schema | MIG-001 |
| new Desktop + old/empty DB | migration on open | typed result | forward migrate or fail closed | MIG-002 |

### 4.1 Public Tasks consumer inventory 与冻结条件

| Consumer surface | 2026-08-02 只读发现 | 冻结结论 | 迁移/退休处理 |
|---|---|---|---|
| yijie-desktop | generated `createTask/getTask` SDK artifacts 存在；唯一非生成引用只使用 types，未发现 active create/get call | no active repo-local consumer observed | 新 v2 consumer 后续按 immutable contract pin 引入；不得 fallback v1 |
| yijie-api | 默认 profile 注册匿名 POST/GET handlers；请求 body `tenant_id` 被信任，GET query 仅按 task ID；FEAT-125 local lab 不注册 | insecure legacy provider, not consumer | v1 保持隔离；新建 v2 auth/tenant/creator-scoped provider |
| yijie-infra | Caddy 与 local profile deny `/v1/tasks` 及子路径；无业务消费 | compensating isolation only | v1 迁移期持续双隔离；deny hit 只作安全信号，不算 supported consumer |
| yijie-agent-host | `/v1/tasks/{task_id}/agent-sessions` 是 owner-only local Host contract | different surface, not Public Tasks consumer | 不迁移为 Public Tasks consumer |
| yijie-admin-web/connectors/knowledge/skills | source scan 未发现 Public Tasks active references | no active repo-local consumer observed | 若未来接入只能使用 v2 pin |
| yijie-contracts generated SDKs | 多语言生成物含 operation | artifact, not runtime consumer evidence | 随 source contract 正常再生成，不计消费窗口 |
| external/public | repo 内无法证明不存在；OpenAPI 明确 Public | `unknown-public` safe compatibility category | 始终走 versioned expand；退休须 owner attestation、可用 release/traffic inventory 与完整窗口，不需/不得虚构“零外部”结论 |

Q-010 在本轮以“仓内 inventory 完成、未知外部不假定为零、默认 versioned expand 与明确窗口”关闭。
DEC-126-011/012已于2026-08-02 Accepted。legacy `/v1/tasks*`在expand、migration、observation与
retirement全过程保持双隔离。

## 5. 支持基线与 Breaking Check

| Baseline version | Full commit | Support window | Planned check command | Result/evidence |
|---|---|---|---|---|
| `contracts-v0.2.0` | `f16a497e1377f45747f8ff9292b4b60cf2027f88` | supported until explicitly changed | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | PASS 2026-08-02；OpenAPI/Buf/AsyncAPI/JSON Schema无breaking；修复v2 error schema隔离后无v1 enum warnings |
| all G2A-time supported/deprecating baselines | only the row above per `docs/supported-baselines.md` | per registry | one check per full commit | PASS；无其它supported/deprecating baseline |
| prior 0.3.0 candidate | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`（parent `9ec34abd6e7dfb5a23b0154d467694167224ebbb`） | immutable remote-available historical candidate, not release baseline | historical semantic/clean-clone gates + LIA-126-002 data-boundary review | historical SOURCE/CLEAN-CLONE PASS；REMOTE CI FAIL；arbitrary `input`问题由DEC-126-023 replacement修复；旧commit/PR仍未修改/merge/tag/发布/pin |
| DEC-126-023 replacement | `29317b6426578749dc698fc2ad32b986ee5c8e9f`（parent `c000a0245acb5c3f7ead5d2a877fb60c281c588c`） | sole source-contract candidate, immutable remote-available, not release baseline | post-commit generate/lint/test/build/pack + supported baseline breaking + v1 reference closure + fixture/schema/SDK conformance | PASS；remote branch SHA精确匹配；DEC-126-024/025 Accepted；未merge/tag/publish或启用 |

结构性 checker 预计会把直接修改既有 Tasks auth/request 标为 breaking；采用 versioned expand 后仍必须人工审核 auth、error、default、tenant 和 idempotency 语义。

## 6. Generator 与下游 Pin

| Consumer | Contract version/tag | Full commit | Digest | Generator/version | Owner |
|---|---|---|---|---|---|
| yijie-api Public Tasks | `0.3.0 local replacement candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | Public source `c8d9e674…354b`；Go `c3d6e58e…c697` | oapi-codegen 2.7.2 | backend-team / 段成威；runtime conformance待后续授权 |
| yijie-desktop Public API | `0.3.0 local replacement candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | Public TS `e84b70be…b678` | openapi-typescript 7.13.0 | client-team / 段成威；runtime conformance待后续授权 |
| yijie-agent-host Host/events | `0.3.0 local replacement candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | Host `d3bb9f33…2c71`；event JSON `b7a6494f…f424`；Proto `a18c08df…f383`（unchanged from parent） | oapi-codegen 2.7.2 + Buf 1.71.0 + JSON Schema generator | agent-runtime-team / 段成威；runtime conformance待后续授权 |
| yijie-desktop Host/events | `0.3.0 local replacement candidate` | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | Host TS `6eeb8a77…bed4`；SDK tarball `21b17b50…b082` | locked contracts generators | client-team / 段成威；runtime conformance待后续授权 |

DEC-126-024所需的version、full commit、per-source SHA-256、SDK digest和generator identity已回填并复验。DEC-126-025确认replacement远端ref精确匹配，但没有为它创建新PR或运行远端CI；API、Host、Desktop checkpoint仍锁旧SHA，现按已恢复的LIA-126-002切换到sole candidate并补runtime conformance。实际证据见`08-verification-report.md`。

| Artifact | SHA-256 |
|---|---|
| Public OpenAPI | `c8d9e6742802e0f0392ea8221a5fdd028f76107df893ab4c531da75f9e9e354b` |
| Agent Host OpenAPI | `d3bb9f33f89f03b7a2cd124e5528d3fbf72e0b88b35711d2d295f8e6959d2c71` |
| Agent session AsyncAPI | `17dc8f7042570c63140de8f388872a7b77668051e9080ecec662d2e284559248` |
| AgentSessionEventV2 JSON Schema | `b7a6494f58e274964ef5520c790f3891836c2f2cf69391ce67e5cfa00211f424` |
| AgentSessionEventV2 Protobuf | `a18c08df2e2805147768e9e1b7eed4f97e4b7d0aebde5b59170c7ff248f1f383` |
| Public generated TypeScript | `e84b70be6505dc5c0fc1e4702018fad2839e1a3fe74d7730883151e49928b678` |
| Public generated Go | `c3d6e58ee37157aaeeb7f9dbaf216881ba2ef3057a01f74c169a28467f3fc697` |
| Agent Host generated TypeScript | `6eeb8a77615095aa51daa74e9dc7a84006808381b46b778324d30a375742bed4` |
| AsyncAPI bundle | `f6b0e7d25b399d1fd4bf42f080fc5a379f21422482f3251b3087aeade5b65ac5` |
| SDK tarball | `21b17b50ee265e1ebbd7a5248880c7874c88def65c538f1216d0413e85fab082` |

## 7. Fixtures 与 Conformance

| Fixture | 唯一权威候选位置 | Producer test | Consumer test | 结果 |
|---|---|---|---|---|
| secure task create/get/error | `yijie-contracts/tests/fixtures/public/tasks-v2/` | yijie-api handler/conformance | Desktop transport parser | source + API producer PASS；Desktop runtime consumer留待S7 |
| tenant/IDOR deny matrix | contracts security fixtures + API synthetic DB fixture | yijie-api integration | Desktop error mapping | API auth/tenant/permission/creator-private/404与PostgreSQL integration PASS；Desktop error mapping留待S7 |
| Host raw-reasoning/title/cleanup | `tests/fixtures/agent/session-event-v2/` + `tests/fixtures/agent/host-v2/` | Host exact raw mapping/caps/finalized/no-log serialization | Desktop Rust strict SSE/domain/application reducer + future UI plain-text rendering Gate | Host producer/no-log/fake Runtime、Desktop SQLCipher terminal/cascade、S7A parser与S7B reducer/restart/fake Host integration PASS；Vue rendering留待S8 |
| unknown event/field | closed v2 schema negative assertions；future consumer compatibility fixture | producer emit disabled | Desktop tolerant parser | source closed-union rejection PASS；S7A仅接受未知非terminal event、丢弃payload并推进cursor，未知terminal fail-closed；UI NOT RUN |
| Desktop private DB migrations | yijie-desktop embedded SQL + checksum ledger | Rust repository migration | current/future/drift/wrong-key/scope/cascade tests | PASS for S6；已执行数据库不支持down migration，按forward-only修复 |
| Desktop private IPC v1 | `src-tauri/schemas/chat-ipc-v1.schema.json` + `src-tauri/fixtures/chat-ipc-v1/` fixed corpus | Rust serde/command/event projection | TS runtime validator/client/store/view-model | S8A Closure Passed：20/20 command request/response refs、7/7 event variants、closed payloads、golden fixtures、capacity/auth/restart/race tests；DEC-126-031 Accepted |

Feature 包只引用上述唯一权威位置，不复制业务 fixtures。

## 8. Local-only 消费、实现、启动与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | 批准需求、Pattern、ADR 与具体 contract design | yijie/Desktop / 段成威 | G1/G2 approval | 保持当前文档状态 |
| 2 | Runtime capability candidate（仅需要时） | yijie-codex / runtime owner | canonical schema tests | 不升级 runtime pin |
| 3 | 保持source candidate/fixtures/generators不可变且PR为Draft | yijie-contracts | DEC-126-018/019/020/021 | 不merge、不tag、不publish；保留exact SHA |
| 4 | consumer tolerance/private DB expand本地draft | Desktop | LIA-126-001 + exact SHA/核验本地投影 | Complete for S6；flag off / rollback local app |
| 5 | secure Public provider + Host provider本地draft | API/Host | LIA-126-001 + provider conformance/security | Complete for S4/S5；local route/feature flags off |
| 6 | S7C Rust actions/delete/interrupt/coordinator本地draft | Desktop Rust | DEC-126-029 Accepted + separate S7C authorization + S7B Closure | Complete/DEC-126-030 Accepted；flags off |
| 7 | S8A private IPC + TS store/view-model本地draft | Desktop Rust/TS | S7C Closure + LIA-126-004 + fixed IPC fixtures | DEC-126-031 Accepted / S8A Closure Passed；无Vue/route activation |
| 8 | S8B0 default-off gate、route/lifecycle/store/readiness integration | Desktop Rust/TS integration | DEC-126-032 Accepted + separate S8B0 authorization；fixed private fixtures | flag remains false；no visual Chat page |
| 9 | S8B真实Vue交互/视觉/a11y本地draft | Desktop Vue | S8B0 Closure + separate S8B authorization + Accepted Pattern | disable local chat UI flag；不得fallback mock transport |
| 10 | S9 fake-provider title/raw reasoning Eval | Desktop/Host/Runtime test harness | S8B Closure + separate S9 authorization | no MiniMax；keep flags off |
| 11 | S10临时test profile四组件本地E2E | all local | S9 pass + separate S10 authorization | stop local processes；delete temp data；不改变默认config |
| 12 | S11 Owner Local-only G6验收 | all local | AC-001–052适用项与真实证据 | 不声明Production Ready |
| 13 | 可选未来merge审批 | Contracts及受影响仓 | local E2E + dependency audit修复 + remote CI全绿 + Owner单独批准 | 保持feature branches/Draft PR |

本期不创建`contracts-v0.3.0` tag、不publish SDK/package、不配置registry、不迁移线上流量、不做生产灰度/启用或legacy生产清理。未来如产生线上意图，必须重开生产轨与G5。

## 9. 实际检查证据

| 检查 | Command | CWD | SHA/版本 | Exit code | 结果 | 证据位置 |
|---|---|---|---|---:|---|---|
| generate | `make generate` | yijie-contracts | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | 0 | PASS；29 generated files current；post-commit no drift | local replacement；no remote/tag/pin |
| lint | `make lint` | yijie-contracts | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 0 | PASS | Redocly/JSON Schema/Buf/TS/Go vet |
| test/build/pack | `make test && make build && pnpm pack:sdk` | yijie-contracts | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | 0 | PASS；Node 27/27、Go PASS、SDK digest `21b17b50…b082` | synthetic fixtures only；no provider |
| breaking | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` + `pnpm check:v1-wire <full-baseline>` | yijie-contracts | sole supported baseline | 0 | PASS；legacy Public 2 paths/Host 7 paths及reference closure equality PASS | automatic + repeatable semantic v1 check |
| conformance | source-schema fixtures and operation assertions + S7A–S8A local consumer/application/IPC adapter | yijie-contracts + Desktop Rust/TS | `29317b6426578749dc698fc2ad32b986ee5c8e9f` | 0 | Public Tasks定向3/3、全仓Node 27/27、generated TS/Go current；S7A wire/domain、S7B/S7C application和S8A schema↔serde↔TS/store conformance PASS；full process runtime E2E NOT RUN | no source-contract mutation/pin/activation；blocks G4, not misreported as code complete |
| Draft PR remote CI | GitHub Actions run 30741466028 / job 91479562558 | yijie-contracts PR #1 | exact head `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | 1 | FAIL；generate/diff/lint/test/pack PASS，`pnpm audit`命中`brace-expansion 2.1.2` high；`govulncheck`与`origin/main` breaking skipped | merge blocked；candidate未改manifest/lockfile；no rerun/waiver/fix/push |
| Runtime fake title capability | `cargo test -p codex-app-server --test all <test> -- --nocapture` for `thread_start_ephemeral_remains_pathless`、`turn_start_accepts_output_schema_v2`、`turn_start_output_schema_is_per_turn_v2` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS | local mock Responses only；keys removed；no source diff |
| Runtime fake public-summary capability | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all <test> -- --nocapture` for `configured_reasoning_summary_is_sent`、`reasoning_content_delta_has_item_metadata` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS after one documented default-stack abort | local mock Responses only；no MiniMax |
| Runtime fake raw delta | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all reasoning_raw_content_delta_respects_flag -- --nocapture` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 | PASS | local mock Responses only；keys removed；no MiniMax/source diff |
| Runtime fixed history raw/reconciliation primitives | `cargo test -p codex-app-server-protocol protocol::thread_history::tests::<test>` for `builds_multiple_turns_with_reasoning_items`、`splits_reasoning_when_interleaved`、`marks_turn_as_interrupted_when_aborted` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS 3/3 | fixed fixtures only；no MiniMax/source diff |
| MiniMax bounded title/public-summary historical gate | isolated harness；`MM-126-001/002`各一次、request/stream retry=0 | fixed Runtime + Host candidate config | Runtime SHA-256 `1ef4f1…8df1fe`；Host `34e94acf…` | 0 | title PASS / public-summary FAIL | budget exhausted；MM-126-002同时证明raw事件存在，但不是新raw contract/conformance PASS；不得重跑 |

## 10. Consumer Owner 评审

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| yijie-desktop / 段成威 | Replacement source approved；LIA-126-002 consumer projection closure resumed | 2026-08-02 | closed content-free DTO/fixtures generated；S6 runtime transport仍限Rust foundation，不进入UI |
| yijie-api / 段成威 | Replacement source approved；LIA-126-002 producer conformance resumed | 2026-08-02 | schema从权威源强制拒绝正文；S4 provider conformance必须在Closure Review真实回填 |
| yijie-agent-host / 段成威 | Host/event source review有效；LIA-126-002 projection closure candidate complete | 2026-08-02 | raw/title/cleanup形状不变；S5列明P1本地证据已关闭并等待DEC-126-026，flags保持off |
| unknown Public API consumers | Safe compatibility category accepted | 2026-08-02 | Q-010 Resolved；不声明为零；DEC-126-011 window Accepted |

## 11. LIA-126-006 Desktop-private consumer conformance

| 检查 | 结果 | 解释 |
|---|---|---|
| Vue direct boundary scan | PASS：Chat页面/组件无`chatClient`、raw`invoke`、Host调用或`v-html` | Vue只消费authoritative Pinia actions与validated projections |
| IPC/Rust diff stop condition | PASS：LIA-126-006 commit无`src-tauri`、schema、client/store wire shape修改 | 22个commands、7个events、cursor/error及authority binding保持S8B0 Accepted语义 |
| Plain-text projection | PASS：assistant/raw reasoning使用Vue插值；浏览器检查正文容器HTML后代为0 | 不引入Markdown/HTML执行语义 |
| Central contract identity | PASS：仍为`29317b6426578749dc698fc2ad32b986ee5c8e9f` | 不形成新G2A candidate或downstream floating pin |
| Production bundle | PASS：test harness、`axe-core`、synthetic fixture与test global不存在于`dist/` | test-only依赖不改变发布consumer |

S8B切片contract impact为`semantic Desktop-private`，不改变central feature总体`breaking`分类。若后续UI需要新command/event/error/cursor或让WebView猜Host/Runtime状态，必须停止并重新进入private IPC设计评审；本轮没有触发该条件。

## 12. LIA-126-007 Eval fixture conformance

- Host `desktop-events.sse`与Desktop vendored副本SHA-256均为`e8c2d5ebca2182b7b07ad30761c07b5986139f2ff8ec9bbbf9b4ecaae6d6a0e6`。
- Host `desktop-consumer.json`与Desktop vendored副本SHA-256均为`5ad29b750693ecf95a0cabab4fe7c2ada6f6dbb9b10f9f99c3d5c25654d32cf1`。
- Desktop authority lock固定Host local checkpoint `8707dea552cff74121b89aa8045f27da2c8c9378`；Rust test在消费前重算摘要并fail closed。
- S9没有生成新的central/private IPC/wire contract；它只验证Accepted producer/consumer语义，因此不形成第二个source candidate。

## 13. DESIGN-126-011 / S10BD1 deployment-interface impact

- S10BD0只是文档与只读调查，`contract-impact=none`。
- 已实施的S10BD1改变FEAT-126本地Docker preflight的执行顺序和失败语义，并增加test-only create/remove resolver probe，按部署接口最高风险归类为`semantic`；权威源为`yijie-infra`的Compose model、verifier、helper与测试，不进入`yijie-contracts`。
- central source candidate继续固定`29317b6426578749dc698fc2ad32b986ee5c8e9f`；Public Tasks HTTP、Host SSE、Desktop private IPC、SQLCipher业务schema与Runtime pin均不变，因此central G2A重审为N/A。
- 唯一consumer是同仓FEAT-126 S10E/S10B本地helper；成功路径仍消费原Compose `version-tag@digest`与`--pull never`。变化只把CLI/permission/daemon/image/reference/platform错误闭合分类，并在单独授权时增加实际no-pull resolver证明。
- 兼容/回滚：仓库caller与tests须在同一checkpoint更新；回滚可移除新classifier/probe并继续HOLD S10B，不能以pull、retag、Docker restart、floating tag、image-store切换或volume删除替代。
- 状态：DESIGN-126-011 complete；DEC-126-054/055 Option A Accepted；LIA-126-017已消费。Infra checkpoint=`2a643caef210e32cab80242ede46b96927b2097a`，S10BD1-001–012、99/99全量与exact-commit live no-start resolver均PASS；S10BD1 Closure Passed，`S10B-BLK-004` Closed。

## 14. DEC-126-055 compatibility conclusion

- central contracts、Public Tasks/Host wire、Desktop private IPC、SQLCipher业务schema与Runtime pin无diff；唯一source-contract candidate仍为`29317b6426578749dc698fc2ad32b986ee5c8e9f`，central G2A=`N/A`。
- private deployment interface的consumer已与verifier在同一Infra checkpoint原子更新；Compose原始`version-tag@digest`、repository pin和`--pull never`均未改变，也没有第二pin authority、floating tag或image-ID bypass。
- Owner已接受Option A、S10BD1 Closure并关闭`S10B-BLK-004`。该接受只证明纠偏切片，不能推导S10B-R4、S11、feature activation、发布或部署授权。

## 15. DESIGN-126-012 / LIA-126-021 deployment-interface conformance

- 影响分类：`semantic`，仅限FEAT-126 private local deployment interface。R5 preflight曾以FEAT-125 runtime profile启动API；纠偏后专用FEAT-126 runtime profile成为唯一允许的S10 API process语义。
- 权威源：API对profile的closed validation位于`yijie-api`；跨preflight/continuation的唯一machine-readable authority、environment builder与summary reader位于`yijie-infra`。两者是受影响方实现，不创建新的`yijie-contracts`源或影子公共DTO。
- API兼容：default与既有`feat-125-local-lab`分支、错误语义和route isolation保持不变；新profile要求exact `nonproduction`、双exact flags、专用loopback DSN、issuer/JWKS、CA path/pin与canonical port，并同样隔离legacy `/v1/tasks`。
- Infra兼容：preflight不再硬编码或接受caller profile；authority closed keys/value漂移、extra key、wrong run/status/scope均fail closed。未来完整链必须从同一reviewed Infra commit消费builder和preflight summary reader，禁止shell重建。
- Central contracts：Public Tasks request/response、Host HTTP/SSE、Desktop private IPC、PostgreSQL/SQLCipher业务schema与Runtime pin均无变化；sole candidate仍为`29317b6426578749dc698fc2ad32b986ee5c8e9f`，central G2A=`N/A`。
- 当前证据：API `make lint/test`与Infra `pnpm validate`、`make lint/test`、113/113测试通过；preflight以双快照生成summary `api_binary_sha256`，唯一continuation launcher安全open并复核digest及dev/inode/mode/size/mtime，再证明同run summary reader→builder→固定API child；6类负向与binary drift在spawn前fail closed。DEC-126-059已接受并关闭`S10B-BLK-006`；immutable local checkpoints为API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`。没有执行S10B-002–012，central G2A仍为N/A。
- 回滚：保持本地flags关闭并继续HOLD S10B；若撤销候选，API/Infra必须作为一组回到各自父基线，不能保留只有一侧的profile/authority，也不能回退到FEAT-125 profile冒充FEAT-126。

## 16. DESIGN-126-018 Private Deployment/Test Compatibility

- 本轮最高影响仍为`semantic` private local deployment/test interface：Desktop test driver的run-root authority和Infra failure/no-log evidence shape同步收紧。
- Desktop repository-root例外只有在`feat126-s10-driver`编译、`EphemeralFile` backend、canonical UUIDv4与精确Infra generated suffix同时满足时成立；default与Protected Data Keychain不接受该例外。
- Infra `runtime-log-scan.v2`新增`hit_origin_set_sha256`与`hit_rule_set_sha256`，不持久化日志正文、路径、token、secret或规则文本；reader继续接受历史v1 evidence。
- Public Tasks HTTP、Host SSE、Desktop业务IPC、PostgreSQL/SQLCipher durable schema、Runtime source/pin与Compose pins无变化；sole central candidate仍为`29317b6426578749dc698fc2ad32b986ee5c8e9f`，G2A=`N/A`。
- Desktop `9771da11c47406e45526dea104f3d7de05701fba`与Infra `61062143fa3c81b90792ec6f48aea7d6408ed06d`必须作为同一新checkpoint manifest消费；旧失败run只保留审计，不得由新reader resume或升级为PASS。
