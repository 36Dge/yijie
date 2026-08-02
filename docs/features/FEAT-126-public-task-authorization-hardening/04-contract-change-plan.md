# FEAT-126 契约与兼容变更计划

> 本文设计已于2026-08-02通过G2和G2A。唯一source-contract candidate为immutable commit `c000a0245acb5c3f7ead5d2a877fb60c281c588c`。DEC-126-021已接受HOLD：Draft PR #1保持Draft，远端CI红灯只阻断merge；LIA-126-001随后仅授权并完成S4–S6本地基础消费/实现。tag/package publish/registry/线上部署仍为N/A，S7–S11仍待另行授权。

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
| WebView↔Rust commands | private published IPC | future yijie-desktop command/schema source | client-team | Tauri Rust | Vue/TypeScript |
| conversation DB | private durable schema | future Desktop migrations | client-team | Tauri Rust repository | current/future Desktop versions |
| MiniMax Responses | third-party | provider official protocol + locked Runtime config | provider/runtime owner | MiniMax | yijie-codex |

生成 DTO、SDK、handler types、DB rows、Vue stores、Host bbolt 和 examples 均不得成为第二权威源。

## 3. 语义设计

### 3.1 Secure Public Tasks 请求候选

- 当前 `/v1/tasks` 仍是匿名、body `tenant_id` 归属语义，且 local FEAT-125 profile/ingress 主动双重隔离；本设计不得把“已隔离”误写为“已迁移”。
- 使用 `Authorization: Bearer <user token>`；token 只在 native/service transport 层存在。
- 使用严格 `X-Yijie-Tenant-ID` 作为 untrusted selector；API 独立验证 principal、active membership 与 tenant scope。
- Create request 移除权威 `tenant_id`。若迁移期暂保留，只允许与 verified scope 精确一致且不参与授权；最终删除。
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

### 3.5 Desktop IPC/private DB 候选

- Vue 只传 opaque project/session IDs 与经长度校验文本，不传任意 SQL、token 或任意 filesystem path。
- Rust command 返回稳定 typed error，不返回原始 path/DB/provider error。
- private DB source 维护 schema version、migration checksum、FK/unique/index constraints；所有 top-level reads 带 owner user+tenant scope。DESIGN-126-003 固定 `0001_chat_core` 与 `0002_chat_reasoning_v2` 两个 forward-only migration；旧 app 只读/忽略其不支持的新 private schema，不执行 down migration，新 app 对 future version/checksum drift/`foreign_key_check` failure fail closed。
- delta 只在 Desktop 内存 reducer 聚合；finalized 或受控 interruption 以一个 SQLCipher transaction 更新 `chat_turns.reasoning_status/reason_code` 并替换对应 reasoning item/parts。history session list 不读取正文；turn page 默认 20、最大 50，只批量返回 reasoning metadata；用户展开时一次加载单 turn raw body，最大 256 KiB，避免 N+1。
- session 永久删除返回按 data surface 分项的 completion；只要 Host/Runtime required cleanup 或 Desktop `wal_checkpoint(TRUNCATE)` 未完成，UI 不显示全部成功。成功语义仅为当前 app-managed live stores 不可重新打开/resume，不得升级为所有磁盘痕迹抹除。

### 3.6 审批与审计

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
| current 0.3.0 candidate | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`（parent `9ec34abd6e7dfb5a23b0154d467694167224ebbb`） | immutable remote-available candidate, not release baseline | semantic diff + candidate migration review + post-commit and clean-clone gates + Draft PR remote CI | SOURCE/CLEAN-CLONE PASS；REMOTE CI FAIL on dependency audit；DEC-126-018/019/020 Accepted，G2A Passed；唯一candidate；PR #1 merge blocked，未merge/tag/发布/pin |

结构性 checker 预计会把直接修改既有 Tasks auth/request 标为 breaking；采用 versioned expand 后仍必须人工审核 auth、error、default、tenant 和 idempotency 语义。

## 6. Generator 与下游 Pin

| Consumer | Contract version/tag | Full commit | Digest | Generator/version | Owner |
|---|---|---|---|---|---|
| yijie-api Public Tasks | `0.3.0 immutable remote candidate` | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | Public source `c7ab2577…998b`；Go generated produced | oapi-codegen 2.7.2 | backend-team / 段成威 |
| yijie-desktop Public API | `0.3.0 immutable remote candidate` | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | Public TS `d3493a79…03b` | openapi-typescript 7.13.0 | client-team / 段成威 |
| yijie-agent-host Host/events | `0.3.0 immutable remote candidate` | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | Host `d3bb9f33…2c71`；event JSON `b7a6494f…f424`；Proto `a18c08df…f383` | oapi-codegen 2.7.2 + Buf 1.71.0 + JSON Schema generator | agent-runtime-team / 段成威 |
| yijie-desktop Host/events | `0.3.0 immutable remote candidate` | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | Host TS `6eeb8a77…bed4`；SDK tarball `334db014…9404` | locked contracts generators | client-team / 段成威 |

Final G2A 所需的 version、full commit、per-source SHA-256、SDK digest 和 generator identity 已回填如下。DEC-126-020 clean clone从专用远端branch复验了相同摘要。LIA-126-001下的API、Host、Desktop均已用锁文件/生成检查固定同一完整SHA；未使用浮动branch或影子DTO。实际下游生成摘要见`08-verification-report.md`。

| Artifact | SHA-256 |
|---|---|
| Public OpenAPI | `c7ab2577b26a0776a7c204d3b9ee38b424cbaf0b9b0dc33d99a6806dfced998b` |
| Agent Host OpenAPI | `d3bb9f33f89f03b7a2cd124e5528d3fbf72e0b88b35711d2d295f8e6959d2c71` |
| Agent session AsyncAPI | `17dc8f7042570c63140de8f388872a7b77668051e9080ecec662d2e284559248` |
| AgentSessionEventV2 JSON Schema | `b7a6494f58e274964ef5520c790f3891836c2f2cf69391ce67e5cfa00211f424` |
| AgentSessionEventV2 Protobuf | `a18c08df2e2805147768e9e1b7eed4f97e4b7d0aebde5b59170c7ff248f1f383` |
| Public generated TypeScript | `d3493a79ade649a17a78573ae0f9da3fa261f76c4472a151fbabd7056614d03b` |
| Agent Host generated TypeScript | `6eeb8a77615095aa51daa74e9dc7a84006808381b46b778324d30a375742bed4` |
| AsyncAPI bundle | `f6b0e7d25b399d1fd4bf42f080fc5a379f21422482f3251b3087aeade5b65ac5` |
| SDK tarball | `334db01424e5038ac8d5431c32fa5a08ee3e3f6febeed0ad1639e325add29404` |

## 7. Fixtures 与 Conformance

| Fixture | 唯一权威候选位置 | Producer test | Consumer test | 结果 |
|---|---|---|---|---|
| secure task create/get/error | `yijie-contracts/tests/fixtures/public/tasks-v2/` | yijie-api handler/conformance | Desktop transport parser | source + API producer PASS；Desktop runtime consumer留待S7 |
| tenant/IDOR deny matrix | contracts security fixtures + API synthetic DB fixture | yijie-api integration | Desktop error mapping | API auth/tenant/permission/creator-private/404与PostgreSQL integration PASS；Desktop error mapping留待S7 |
| Host raw-reasoning/title/cleanup | `tests/fixtures/agent/session-event-v2/` + `tests/fixtures/agent/host-v2/` | Host exact raw mapping/caps/finalized/no-log serialization | Desktop reducer/dedupe/plain-text/SQLCipher history/unavailable Gate | Host producer/no-log/fake Runtime与Desktop SQLCipher terminal/cascade基础 PASS；reducer/UI留待S7–S8 |
| unknown event/field | closed v2 schema negative assertions；future consumer compatibility fixture | producer emit disabled | Desktop tolerant parser | source closed-union rejection PASS；consumer tolerance NOT RUN |
| Desktop private DB migrations | yijie-desktop embedded SQL + checksum ledger | Rust repository migration | current/future/drift/wrong-key/scope/cascade tests | PASS for S6；已执行数据库不支持down migration，按forward-only修复 |

Feature 包只引用上述唯一权威位置，不复制业务 fixtures。

## 8. Local-only 消费、实现、启动与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | 批准需求、Pattern、ADR 与具体 contract design | yijie/Desktop / 段成威 | G1/G2 approval | 保持当前文档状态 |
| 2 | Runtime capability candidate（仅需要时） | yijie-codex / runtime owner | canonical schema tests | 不升级 runtime pin |
| 3 | 保持source candidate/fixtures/generators不可变且PR为Draft | yijie-contracts | DEC-126-018/019/020/021 | 不merge、不tag、不publish；保留exact SHA |
| 4 | consumer tolerance/private DB expand本地draft | Desktop | LIA-126-001 + exact SHA/核验本地投影 | Complete for S6；flag off / rollback local app |
| 5 | secure Public provider + Host provider本地draft | API/Host | LIA-126-001 + provider conformance/security | Complete for S4/S5；local route/feature flags off |
| 6 | Desktop behavior/UI本地draft | Desktop | provider + consumer matrix | disable local chat feature |
| 7 | API/Host/Desktop/Runtime本地构建、启动与完整E2E | all local | security/delete/resilience/eval/fake provider | stop local processes；保留FEAT-125生产隔离 |
| 8 | Owner Local-only G6验收 | all local | AC-001–043适用项与真实证据 | 不声明Production Ready |
| 9 | 可选未来merge审批 | Contracts及受影响仓 | local E2E + dependency audit修复 + remote CI全绿 + Owner单独批准 | 保持feature branches/Draft PR |

本期不创建`contracts-v0.3.0` tag、不publish SDK/package、不配置registry、不迁移线上流量、不做生产灰度/启用或legacy生产清理。未来如产生线上意图，必须重开生产轨与G5。

## 9. 实际检查证据

| 检查 | Command | CWD | SHA/版本 | Exit code | 结果 | 证据位置 |
|---|---|---|---|---:|---|---|
| generate | `make generate` | yijie-contracts | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | 0 | PASS；29 generated files current；no drift | immutable local commit；no tag/pin |
| lint | `make lint` | yijie-contracts | Node 26.0.0 / pnpm 11.9.0 / Go 1.26.5 | 0 | PASS | Redocly/JSON Schema/Buf/TS/Go vet |
| test/build/pack | `make test && make build && pnpm pack:sdk` | yijie-contracts | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | 0 | PASS；Node 27/27、Go PASS、SDK digest `334db014…9404` | synthetic fixtures only；no provider |
| breaking | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | yijie-contracts | sole supported baseline | 0 | PASS；legacy Public 2 paths/Host 7 paths equality PASS | automatic + semantic v1 check |
| conformance | source-schema fixtures and operation assertions only | yijie-contracts | `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | 0 | source-level 11/11 PASS；provider/consumer runtime NOT RUN | no business code/pin；blocks G4, not misreported as implementation |
| Draft PR remote CI | GitHub Actions run 30741466028 / job 91479562558 | yijie-contracts PR #1 | exact head `c000a0245acb5c3f7ead5d2a877fb60c281c588c` | 1 | FAIL；generate/diff/lint/test/pack PASS，`pnpm audit`命中`brace-expansion 2.1.2` high；`govulncheck`与`origin/main` breaking skipped | merge blocked；candidate未改manifest/lockfile；no rerun/waiver/fix/push |
| Runtime fake title capability | `cargo test -p codex-app-server --test all <test> -- --nocapture` for `thread_start_ephemeral_remains_pathless`、`turn_start_accepts_output_schema_v2`、`turn_start_output_schema_is_per_turn_v2` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS | local mock Responses only；keys removed；no source diff |
| Runtime fake public-summary capability | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all <test> -- --nocapture` for `configured_reasoning_summary_is_sent`、`reasoning_content_delta_has_item_metadata` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS after one documented default-stack abort | local mock Responses only；no MiniMax |
| Runtime fake raw delta | `RUST_MIN_STACK=33554432 cargo test -p codex-core --test all reasoning_raw_content_delta_respects_flag -- --nocapture` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 | PASS | local mock Responses only；keys removed；no MiniMax/source diff |
| Runtime fixed history raw/reconciliation primitives | `cargo test -p codex-app-server-protocol protocol::thread_history::tests::<test>` for `builds_multiple_turns_with_reasoning_items`、`splits_reasoning_when_interleaved`、`marks_turn_as_interrupted_when_aborted` | yijie-codex/codex-rs | `3aa317ce...` / 0.144.6 | 0 each | PASS 3/3 | fixed fixtures only；no MiniMax/source diff |
| MiniMax bounded title/public-summary historical gate | isolated harness；`MM-126-001/002`各一次、request/stream retry=0 | fixed Runtime + Host candidate config | Runtime SHA-256 `1ef4f1…8df1fe`；Host `34e94acf…` | 0 | title PASS / public-summary FAIL | budget exhausted；MM-126-002同时证明raw事件存在，但不是新raw contract/conformance PASS；不得重跑 |

## 10. Consumer Owner 评审

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| yijie-desktop / 段成威 | Approved for source-contract readiness；G2A Passed | 2026-08-02 | generated Public/Host/event shapes + future private DB consumer；DEC-126-018/019；实现另行授权 |
| yijie-api / 段成威 | Approved for source-contract readiness；G2A Passed | 2026-08-02 | creator-private/auth/idempotency/error semantics；DEC-126-018/019；实现另行授权 |
| yijie-agent-host / 段成威 | Approved for source-contract readiness；G2A Passed | 2026-08-02 | raw/title/cleanup v2、caps/no-durable-raw与Runtime authority；DEC-126-018/019；实现另行授权 |
| unknown Public API consumers | Safe compatibility category accepted | 2026-08-02 | Q-010 Resolved；不声明为零；DEC-126-011 window Accepted |
