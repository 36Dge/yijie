# FEAT-126 现状扫描与影响评估

## 1. 调查基线

初始扫描时间：2026-08-01；G2 补充扫描：2026-08-02，Asia/Shanghai。所有 sibling 仓库只读；未 fetch、checkout、generate 或修改。

LIA-126-002于2026-08-02形成S4–S6 checkpoint并完成Corrective Closure；Public Tasks source冲突已由DEC-126-023/024关闭，`29317b6426578749dc698fc2ad32b986ee5c8e9f`是唯一candidate。DEC-126-026/027/028/030/031/033/034已接受S4–S8B Closure，DEC-126-035已接受远端可达事实，DEC-126-036已接受LIA-126-007的test-only S9 Eval Closure；production行为和flag未改变，S10–S11仍未开始。

| Repository | Rules/read sources | Branch | Full HEAD SHA | Worktree | Toolchain/lock |
|---|---|---|---|---|---|
| yijie | `AGENTS.md`、project memory、Feature Delivery、ADR-0012、FEAT-124/125 | develop | `6c23dc3d9fa0d979948dbb10356fc5929ac2513b` | dirty：既有 FEAT-123 删除 | Node ≥24<27 / pnpm 11.7.0 project policy |
| yijie-desktop | AGENTS/README/SECURITY、Chat/App Shell patterns、源码/Makefile | develop | `155854cf3662384caa2c8bffe0a47935ef4a70b5` | clean | Node ≥24<27、pnpm 11.7.0、Rust 1.95.0、Tauri v2 |
| yijie-api | AGENTS/README/SECURITY、app/Tasks/Auth/migrations/Makefile | develop | `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | clean | Go 1.26.5、oapi-codegen 2.7.2 |
| yijie-agent-host | AGENTS/README/SECURITY、Runtime/sidecar/contracts/session 源码 | develop | `34e94acf293f6daad61c4d42fa47028a2d1318e4` | clean | Go 1.26.5、bbolt 1.5.0、oapi-codegen 2.7.2 |
| yijie-contracts | AGENTS/README/SECURITY、Public/Host schemas、baseline policy | develop | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | clean | Node ≥24<27、pnpm 11.7.0、Go 1.26.5 |
| yijie-infra | AGENTS/README/SECURITY、Makefile/FEAT-125 profiles | develop | `f040492e7c4af4aa7cc94a343140c58befae3af2` | clean | Node ≥24<27、pnpm 11.7.0、Docker Compose v2 required |
| yijie-codex | AGENTS/README/SECURITY、pinned Runtime authority docs/schema | develop | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | clean | pinned codex-cli 0.144.6 candidate |

本机调查工具为 Node `v26.0.0`、pnpm `11.9.0`、Go `1.26.4`、Rust `1.95.0`；其中 pnpm/Go 与部分仓库锁定值不完全一致，因此没有运行业务 baseline，不能据此宣称实现环境 ready。

## 2. 已验证的当前行为

| 事实 | 文件/符号/行号或命令 | 结果 | 类型 |
|---|---|---|---|
| `/chat` 只有本地 textarea | `yijie-desktop/src/pages/chat/ChatPage.vue` | 无发送、store、API 或 Agent 调用 | Fact |
| Accepted Chat Pattern 明确禁止 FEAT-124 入口态发送/网络/持久化 | `docs/design/.../02-chat-workspace.md` §新建任务入口态 | 本需求必须升级 Pattern | Fact |
| 当前 active Chat Pattern 要附件/链接/右侧面板 | 同文档 §活跃会话态 | 与本期极简纯文本冲突 | Conflict |
| `/tasks` 是 `sampleTasks` 静态列表 | `TasksPage.vue`、`src/domain/tasks.ts` | 无真实 list/rename/pin/delete/lazy load | Fact |
| Desktop API client 的 Runtime health 是固定对象 | `src/api/client.ts#getRuntimeHealth` | sidecar 尚未接入 | Fact |
| Desktop 有 `task.create/read` 路由 capability 投影 | `src/domain/permissions.ts`、router tests | 仅 UX/route guard，不是资源授权 | Fact |
| Host 已有 start/resume/turn/interrupt/SSE | `yijie-agent-host/README.md` 与 `api/openapi/agent-host.yaml` | text-only 最小 Runtime slice 存在 | Fact |
| Host bbolt 只存 task→session→thread→turn 映射 | `internal/session/store.go` | 不保存用户/模型正文 | Fact |
| Host SSE 仅进程内 512 events，重启换 stream | `internal/session/events.go`、Runtime Baseline 2 | Desktop 必须另存正文/cursor 并处理 409 | Fact |
| Host 只投影 8 类通知 | `api/compatibility/agent-host-runtime-v1.json` | 没有 reasoning-summary 专用事件 | Fact |
| Host 配置 summary 默认 `none` | `internal/codex/provider.go` | 截图式公开思考内容未验证 | Fact |
| pinned Runtime 同时定义 public summary 与 raw reasoning | app-server README/schema 的 `item/reasoning/summaryTextDelta`、`summaryPartAdded`、`item/reasoning/textDelta`及completed raw content | canonical protocol/source available；Host projection absent；MM-126-002实测7 raw delta + 1 raw completed part | Fact |
| pinned Runtime 已实现 functional hard-delete | app-server `thread/delete` README/source/tests + 2026-08-02 fixed-binary temp-home check | 删除 target/spawned descendants 与 live state并发 `thread/deleted`；同进程/重启不可读，但 Runtime WAL/log 仍有 canary/ID 字节，Host bridge 尚无 | Fact with explicit forensic limitation |
| pinned Runtime 的 `thread/name/set` 只设置调用方提供的名称 | app-server README/schema/tests | 不是模型自动标题生成器；独立 title turn 仍需设计 | Fact |
| pinned Runtime fake-provider fixture 已验证 pathless ephemeral thread、turn-scoped `outputSchema`、summary request 与 delta/item 关联 | 2026-08-02 narrow cargo tests at `yijie-codex@3aa317...`；模型 key 均从环境移除 | 固定 Runtime 能力可作为 ADR-0015 输入；不代表 MiniMax feature compatibility | Fact |
| Host fixed `read-only`/`approvalPolicy=never` | compatibility manifest、Runtime docs | 权限入口不能启用写审批 | Fact |
| MiniMax 使用中国站 Responses wire | `provider.go`: base `/v1` + `wire_api="responses"` | 配置级兼容，真实短 turn 曾通过 | Fact |
| Public OpenAPI 全局 `security: []`，Tasks 无 operation security | `yijie-contracts/openapi/public/public.yaml` `/v1/tasks*` | legacy API 匿名 | Fact |
| CreateTask 需要客户端 `tenant_id` | 同文件 `CreateTaskRequest` | 客户端选择被当作归属输入 | Fact |
| API Get repository 只 `WHERE id = $1` | `yijie-api/internal/modules/tasks/infrastructure/postgres/repository.go#Get` | 存在跨 tenant IDOR 风险 | Fact |
| FEAT-125 local profile 不注册 task handlers | `yijie-api/internal/app/app.go` | 当前补偿控制，不是最终授权 | Fact |
| FEAT-126 被 ADR/FEAT-125 预留 | `ADR-0012`、FEAT-125 00/03/10 | 不能静默改号 | Fact |

## 3. 仓库与组件影响矩阵

| Repository/Component | 职责 | 影响 | 原因 | Owner | 候选未来改动 |
|---|---|---|---|---|---|
| yijie | 多仓治理 | direct now | 创建需求包并维护 ADR/Feature 链路 | 段成威 | 本轮仅本目录；G1 后可能更新关联索引 |
| yijie-contracts | 公共 wire 权威源 | G2A replacement approved and remote-available；prior remote/Draft PR保持HOLD | Public Tasks versioned hardening + Agent session-event v2 + Host title/cleanup/events operations | platform-team | `29317b6426578749dc698fc2ad32b986ee5c8e9f`为唯一candidate并位于`origin/feat/feat-126-content-free-candidate`；`c000a024`仅为历史远端候选。LIA-126-002已单独恢复 |
| yijie-api | Public Tasks provider | direct future | bearer、tenant/resource auth、list/mutate/delete/审计 | backend-team | auth middleware/application/repository/migration/tests |
| yijie-agent-host | Runtime adapter | direct future | Desktop lifecycle、versioned raw-reasoning projection、cleanup/title operation 候选 | agent-runtime-team | 先走 Runtime/contract candidate；正文不进logs/bbolt，不持有业务主 DB |
| yijie-desktop | 产品 consumer/local data owner | direct future | UI、native picker、local DB、sidecar transport、states | client-team | Pattern/contract pin/Tauri/domain/store/components/E2E |
| yijie-infra | route/profile activation | indirect future | legacy isolation、flag、host/ingress、observability | devops-team | 默认关闭、双轨 route 与 smoke |
| yijie-codex | canonical Runtime | conditional | stable Runtime已有delete/name/summary/raw reasoning/outputSchema；MiniMax title单样本PASS，MM-126-002证明raw事件存在；当前缺口在Host bridge、raw conformance/caps/completion与title Eval | agent-runtime-team | 预期先不改Runtime source；raw feature flag默认off；仅exact-pin conformance失败时再提候选并重审 |
| yijie-admin-web | Admin app | none | 本期仅 Desktop；source scan未发现Public Tasks active consumer | admin-platform-team | Q-010 repo-local inventory complete；未来接入只允许v2 pin |
| yijie-skills | AI capability | none | 纯文本通用 turn，不新增 skill/tool | ai-product-team | N/A |
| yijie-connectors | 平台适配 | none | 无平台调用或副作用 | integration-team | N/A |
| yijie-knowledge | RAG | none | 无检索/embedding | data-ai-team | N/A |

### 3.1 DESIGN-126-005前置能力差距盘点（历史基线，2026-08-03）

本表记录DESIGN-126-005形成时的S4–S7B事实输入，用于解释为何必须按S7C→S8A→S8B切分；它不是当前实现状态。其列明的S7C缺口已由DEC-126-030接受，S8A缺口已在LIA-126-004本地候选中实现并通过门禁。

| 能力 | 当前已存在 | 到可用private IPC仍缺少 | 归属切片 |
|---|---|---|---|
| 创建session与提交turn | Rust application已有transactional create、enqueue与create/start outbox dispatch | Rust-bound authorization context、versioned command DTO、coordinator自动派发/结果对账、稳定response/error | S7C coordinator；S8A IPC/store |
| session列表与历史分页 | Rust已有metadata排序和20/50-turn batched history | IPC-safe DTO、opaque scoped cursor、aggregate response cap、取消和stale-selection约束；raw reasoning正文仍需按单turn窄加载 | S8A |
| assistant/raw reasoning流投影 | HostBridge与Rust reducer已有strict wire/domain、coalesced checkpoint和terminal reconciliation | reducer到Tauri event的bounded projection、subscription/sequence、backpressure/resync与restart snapshot；不得透传Host envelope | S7C projection source；S8A bridge/store |
| rename、pin/unpin、interrupt | Rust已有rename和HostBridge interrupt；DB已有`pinned_at`字段/outbox kind | session/project pin mutation、interrupt application orchestration、幂等和授权映射、versioned commands | S7C；S8A exposure |
| project pin/remove | native project list/remove foundation存在，schema有project pin字段 | Rust application pin action、context/scope检查、conversation-safe command；移除与active send竞态规则 | S7C；S8A exposure |
| session物理删除与cleanup状态 | SQLCipher有local cascade helper；Host已有cleanup domain；migration已有job/receipt表 | durable跨Desktop/Host/Runtime deletion saga、lease/retry/receipt/status、active stream exclusion、restart recovery与UI-safe状态 | S7C；S8A exposure |
| restart/reconnect与错误恢复 | durable DB/outbox/cursor、sidecar nonce与Host replay 409基础存在 | Rust coordinator startup recovery、subscription/cursor invalidation、resync snapshot、context rebind、closed stable recovery error；TS store恢复状态机 | S7C；S8A |
| Tauri/TypeScript/Vue consumer | foundation invokes和FEAT-124 textarea存在 | 无conversation invoke/event、无TS runtime validator/client/store/view-model、无真实Vue链路；不得用mock UI冒充 | S8A；S8B仅在其后 |

当前结论：S4–S8A Closure已由Owner接受；DEC-126-033已接受S8B0 Closure。S8B0在S8A的20个命令上新增2个closed readiness/recovery commands，并实现default-off gate、route/lifecycle/store/Tasks接线。完整Chat Vue页面/组件/视觉仍未修改；S8B须另行明确授权。

### 3.2 DESIGN-126-006 S8B0消费就绪盘点（当前事实）

| Surface | 已存在 | 当前缺口/风险 | DESIGN-126-006冻结方向 |
|---|---|---|---|
| UI activation | native `YIJIE_CHAT_LOCAL_ENABLED`与`YIJIE_CHAT_LOCAL_HOST_ENABLED`均exact true才运行；permission UI另有独立flag | 没有Chat UI专属flag；当前`/chat` loader可被实例化 | 新增`VITE_YIJIE_CHAT_LOCAL_UI_ENABLED`，exact true/default false，并同时gate导航、route、deep-link和component loader；任何默认env/CI/build不得设true |
| routes/auth | `/chat`与`/tasks`通过当前permission policy | 只有exact-path lookup；没有`/chat/:sessionId`，动态path可能绕过或错误套用create权限 | route meta固定capability；`/chat`=`task.create`，session深链=`task.read`；Rust仍做resource/action复验；deleted/foreign不枚举 |
| permission lifecycle | permission store有tenant/revision/expiry/logout fail-closed | Chat store尚未由app lifecycle统一bind/clear/dispose | 先dispose旧scope再bind新scope；logout、revision/tenant变化、过期均清正文、取消read、退订并使late结果失效 |
| store consumption | S8A authoritative reducer、真实Tauri client、历史加载与session reload存在 | store未暴露project pick/revalidate；session cursor没有append action；cleanup complete后未完成clear/reload/navigation | S8B0只补view-model消费能力；Vue只调store，不直接调client/invoke；删除返回closed disposition供router使用 |
| readiness/recovery | Rust有sidecar nonce、HostBridge preflight与`chat_host_not_ready` | S8B0已新增closed Host/Runtime/storage readiness与窄化recovery intent；`canSend`只由Rust投影且每次submit仍复验 | private IPC stop condition已按DEC-126-032/LIA-126-005关闭；S8B不得复用旧foundation start command或猜ready |
| local storage UX | Rust内部可区分migration/key/unsafe/unavailable的一部分错误 | private IPC将多类错误压成`chat_storage_unavailable`，无法稳定表达read-only/full/corrupt/migration | 冻结content-free issue/recovery枚举及schema/serde/TS fixture；不暴露path/SQL/key/底层message |
| task records | `/tasks`页面存在 | production `sampleTasks`已删除，页面消费同一Pinia session metadata追加分页；route/nav随UI flag default-off隐藏 | S8B只可继续消费authoritative store；不得恢复sample/mock production path |
| scroll | Accepted Pattern有48/160阈值 | requirements仍留96px冲突 | Pattern 1.0.0优先：follow≤48px、button>160px、`aria-label="滚动到对话底部"` |

Contract impact分类为`semantic` Desktop-private candidate：中央`yijie-contracts@29317b...`、Host/Public Tasks wire与Runtime pin均不变。当前closed IPC gap需要未来修改Desktop schema/Rust serde/TS validators，故本轮按停止条件只提交设计，源码保持checkpoint不变。

## 4. 调用链与数据流

### 4.1 本地对话候选

```text
Yijie Desktop Vue
  → Tauri native project picker + Desktop-owned conversation repository
  → owner-only local HTTP/SSE + Host bearer
  → yijie-agent-host
  → pinned yijie-codex app-server
  → MiniMax China /v1/responses

Desktop local DB
  ← durable user/assistant messages, metadata, cursor/outbox
  ← raw reasoning terminal/explicit-incomplete records per accepted DEC-126-016
Agent Host bbolt
  ← mapping/status only
Runtime CODEX_HOME
  ← canonical thread rollout under separately approved deletion policy
```

### 4.2 Public Tasks hardening

```text
Authenticated consumer
  → user bearer + untrusted tenant selector
  → yijie-api authentication
  → membership/RBAC/resource/action authorization
  → tenant-scoped Tasks repository transaction + audit
  → PostgreSQL
```

| 边界 | 方向 | 权威源 | Producer | Consumers | 失败传播 |
|---|---|---|---|---|---|
| Public Tasks HTTP | request/response | future `yijie-contracts` Public OpenAPI | yijie-api | Desktop + inventory results | stable 4xx/5xx, no raw DB/auth errors |
| Agent Host HTTP | request/response | future contracts Host OpenAPI | Agent Host | Desktop | local 401/409/5xx, fail closed |
| Agent session events | SSE/event | future JSON Schema/AsyncAPI/Proto | Agent Host | Desktop | at-least-once; cursor 409 recovery |
| Runtime app-server | stdio | pinned yijie-codex canonical schema | yijie-codex | Agent Host | candidate-first; unknown requests deny |
| MiniMax Responses | third-party HTTPS | provider official protocol + locked Host config | MiniMax | Runtime | sanitized timeout/limit/provider failure |
| Conversation DB | private durable schema | Desktop migration source | Tauri backend | Desktop current/future versions | migration/read-only/corruption explicit |

## 5. Contract Impact

- 分类：`breaking`（最高风险唯一分类）。
- 理由：Public `/v1/tasks*` 现有匿名且信任 body `tenant_id`；要求 bearer、server-authoritative tenant 与新的拒绝/error 语义会使既有有效匿名 consumer 失败。即使新 chat/session API 采用 additive 路径，最高分类仍是 breaking。
- 公开未知消费者：存在可能；当前 OpenAPI 标为 Public，必须完成 consumer inventory，不能只检查 Desktop。
- 请求方向：先提供 versioned/expand provider 能力，再迁移 consumers；旧路径保持隔离，不在同一 operation 静默改变。
- 响应/事件方向：Desktop 必须先容忍新字段/unknown event，再让 Host 发 reasoning/title/delete variants；事件启用不能早于 consumer pin。
- 支持基线：至少 `contracts-v0.2.0^{commit}` = `f16a497e1377f45747f8ff9292b4b60cf2027f88`，以及在 G2 时仍 supported/deprecating 的全部基线。
- 当前 `9ec34...` 只是 0.3.0 candidate，不是 FEAT-126 契约候选或 release tag。

## 6. 数据与 Migration 影响

| 存储/Schema | Owner | 变化 | 旧数据影响 | 新旧 Reader/Writer | 回填/回滚 |
|---|---|---|---|---|---|
| Desktop conversation DB（ADR-0013/0014、DEC-126-016 Accepted） | client-team | 新 SQLCipher schema：projects/sessions/messages/turns/reasoning records/cursors/outbox/receipt；forward-only checksum migrations | 现有无业务数据；需从空库和损坏/旧 schema 测 | old app 忽略新 DB；new app migration/key/checksum fail closed | driver/protection/backup/delete与reasoning生命周期已冻结；字段/caps/migration仍待G2；不创建静默 backup |
| Agent Host bbolt | agent-runtime-team | cleanup/delete projection、必要状态字段候选 | 既有 mapping 可 orphan | old/new Host 与 Desktop pin 组合 | additive bucket/field；不把正文迁入 Host |
| Runtime CODEX_HOME | Runtime owner | deletion/resume/title isolation 策略 | 既有 thread rollout 可能残留 | 必须以 canonical Runtime schema 验证 | delete capability 或明确 retention/forward cleanup |
| yijie-api PostgreSQL tasks | backend-team | tenant/resource indexes、auth/audit、list/mutate/delete schema 候选 | legacy tenant IDs 需验证 membership/owner | expand provider + versioned route；旧路径隔离 | expand/backfill/switch/contract；物理删与审计分离 |
| audit_logs | backend/security | 新 actions/outcomes/resource scope；禁止正文 | 保留旧记录 | new writer/old reader unknown metadata tolerant | append-only；回滚停止新 action，不删审计 |

## 7. 安全与隐私影响

- 认证：Public API 使用 FEAT-125 bearer verifier；Agent Host 使用 owner-only local token；两者不能互相冒充。
- 资源授权：每个 task/session operation 检查 user+tenant+resource+action；list repository 自带 tenant scope。
- 租户隔离：body/header 是 selector/context，不是证明；local DB 每个 top-level row 带 owner user/tenant scope。
- 数据分类：conversation、title、project path为confidential；raw reasoning可能复述prompt/项目片段，按restricted处理。ADR-0016/DEC-126-016已批准UI展示与SQLCipher历史持久化，但正文禁入logs/telemetry/audit/Host bbolt/云端。
- Secret/token：MiniMax key 留在 owner-only file/Host env；Host token 不进 URL/WebView storage/log。
- 审批：当前无工具执行；permission entry 固定 read-only/deny。未来写审批需独立 threat model/contract/audit。
- 审计字段：request/trace/user/tenant/resource/action/policy revision/outcome/reason，不含 message/path/secret。
- 输入/文件/URL：纯文本 size/Unicode/control-char 校验；非文本拒绝；项目通过 native picker、canonicalize、symlink/权限 recheck。
- 删除：确认、active turn stop、事务级联、Runtime residual verification；不得用 UI 消失冒充删除。

## 8. Runtime、模型与第三方影响

| 依赖 | 固定版本/完整 SHA | 能力是否已验证 | 费用/限流 | Sandbox | Fallback |
|---|---|---|---|---|---|
| yijie-codex Runtime | `3aa317...`; upstream `0.144.6` / `5d1fb...` | text baseline已验证；schema/source已确认delete/name/summary/raw reasoning/outputSchema；exact binary delete已验证；bounded MiniMax title PASS且raw reasoning存在 | N/A | read-only | 保持现有pin；raw flag默认off直到v2 contract/consumer/caps/Eval完成 |
| Agent Host | `34e94...` | 8 events、bbolt mapping、process-local replay 已测试；Desktop integration 未完成 | local | owner-only bearer | entry disabled / diagnostic state |
| MiniMax-M3 | Host locked catalog/config | `/v1/responses` baseline曾通过；`MM-126-001` strict title PASS；`MM-126-002` 在旧summary门槛FAIL但产生7 raw delta + 1 completed raw part | provider cost未返回；两次预算已耗尽 | provider external | title有deterministic fallback；reasoning不得静默时长-only，缺raw则pin不兼容/flag不开 |
| macOS native picker/bookmark | Tauri v2 candidate | S6 已实现并测试 native folder picker、read-only security-scoped bookmark 与 opaque project identity 基础层；完整 Vue 用户流仍属 S7+ | local | OS permission boundary | fail closed，要求重选 |

## 9. 现有测试、构建与发布入口

以下是仓库入口及初始风险基线；DEC-126-026/027/028/030已关闭S4–S7C列明P1，DEC-126-031/033/034已关闭S8A–S8B。LIA-126-007仅增加test-only Host Eval authority与Desktop fixture consumer；完整四组件本地链路和S10–S11仍未启动，feature activation仍禁止。

| 目的 | 真实命令/配置来源 | 作用范围 | 已知限制 |
|---|---|---|---|
| Desktop lint/test/build | `make lint` / `make test` / `make build` | Vue/TS + Rust | 当前本机 Go/pnpm 与锁定值有差异不影响 Desktop，但 sidecar 未打包 |
| Contracts | `make generate` / `make lint` / `make test` / `./scripts/check-breaking.sh <full SHA>` | OpenAPI/Proto/AsyncAPI/JSON Schema | 自动 breaking 不证明 auth/error 语义 |
| API | `make lint` / `make test` / integration targets | Go + PostgreSQL | DB integration 需要明确环境；legacy/default profile 语义不同 |
| Agent Host | `make contract-check` / `make lint` / `make test` / explicit `make runtime-turn-test` | local HTTP/SSE/Runtime | runtime-turn 计费且不在 CI；Desktop E2E absent |
| Infra | repo Makefile local profile/status/smoke | Docker Compose/profile/ingress | 退出 0 不等于 readiness；不能为文档任务启动 |
| Meta package | feature checker + YAML parse + `git diff --check` | 本需求文档 | 只证明结构/语法，不是 Gate 批准 |

## 10. Local-only 交付顺序（仅计划，不授权执行）

### 本地实现与未来合并边界

1. G1 已于 2026-08-01 通过：段成威关闭产品问题 Q-001–Q-005/Q-011–Q-014；批准的产品规则由需求包承接。
2. G2 评审于 2026-08-02 启动：ADR-0013 已冻结 Desktop 数据权威；继续冻结 Desktop Pattern、Public Tasks breaking、Agent Host additive/semantic 契约、SQLite protection/backup 与跨进程删除设计。
3. DEC-126-024批准的sole candidate已精确推送到新专用远端分支；DEC-126-021仍保持旧Draft PR/HOLD，远端红色CI继续只阻断旧PR merge。新分支可达不等于merge、tag、publish、deploy、生产启用或实现完成。
4. LIA-126-001/002形成并关闭了Public Tasks、Host v2与Desktop local repository/sidecar基础；DEC-126-027/028/030/031接受S7A/S7B/S7C/S8A，DEC-126-033/034接受S8B0/S8B，DEC-126-036接受LIA-126-007的S9 test-only Eval。所有flags仍默认关闭；S10–S11、完整四组件E2E和activation继续禁止。
5. 下游只固定完整SHA或已核验本地投影；先实现consumer tolerance，再启用本地provider新events；浮动branch不得作为契约身份。
6. 完成security/migration/resilience/visual、四组件本地E2E和结构化审查后，提交Owner本地G6验收；不讨论线上activation。
7. 如未来需要把源码纳入共享`develop`，必须先修复dependency audit、取得远端全绿CI并另行审批merge；merge不等于部署。

### DEC-126-035 远端影响（Accepted）

- 五仓候选分支已通过`git ls-remote`与临时single-branch clean clone精确复验；所有clone worktree clean。
- yijie/API/Host/Desktop候选SHA分别为`650254b3…139fa`、`a64f9f59…3264`、`3e8df026…f3d9`、`35f27447…7cbd`；contracts仍为唯一`29317b64…8e9f`。
- 五仓`develop`保持既有baseline SHA，Draft PR #1与历史`c000a024`保持不变。
- 影响仅为审计/检出可达性；不扩大运行面、数据面、feature flags、G4/G6或发布面。

### 本地启动与功能验证顺序

1. 使用fake provider/固定fixtures准备本地Runtime与Host测试链，不调用MiniMax；
2. consumer tolerance与Desktop private DB expand；
3. API/Host本地provider/versioned secure operations；
4. Desktop本地consumer与API/Host/Desktop/Runtime四组件ready检查；
5. 完成本地安全、迁移、恢复和删除E2E；Public Tasks legacy route继续隔离。

### 功能启用顺序

1. flags 默认 off；内部合成 identity/tenant 本地验证；
2. read/list/history；
3. create/stream/stop/title；
4. rename/pin/project remove；
5. permanent delete；
6. Owner完成Local-only G6验收；tag、package publish、registry、线上部署、云数据库和真实用户数据均N/A。一次MiniMax local smoke另行审批。

## 11. 阻塞项与 Spike

| ID | 未知项 | 允许的只读/隔离验证 | 禁止副作用 | Owner | 结论 |
|---|---|---|---|---|---|
| SPIKE-126-001 | stable Runtime/MiniMax提供何种reasoning events | fixed-source fake summary fixtures PASS；`MM-126-002` answer completed、0 public-summary、7 raw delta + 1 raw completed part | 不改yijie-codex、不输出/记录正文、0 retry、临时根清理 | agent-runtime-team | Complete for bounded fact：旧ADR-0015门槛FAIL；ADR-0016接受raw产品方向，Q-009 Resolved；跨输入稳定性/安全/caps仍阻断G2/G4 |
| SPIKE-126-007 | raw reasoning历史生命周期 | 比较仅内存与Desktop SQLCipher；复用ADR-0013/0014 authority/delete/backup边界并推演history一致性 | 不创建schema/migration，不写真实/合成reasoning正文 | client-team | Complete：DEC-126-016 Accepted、Q-016 Resolved；DESIGN-126-003/DEC-126-017细节候选已提交；实现安全证据仍待G4 |
| SPIKE-126-002 | Runtime thread/rollout delete 能力与残留 | fixed `codex-cli 0.144.6`/SHA-256 `1ef4…f1fe` 在自动清理的临时 `CODEX_HOME` 创建一个 synthetic thread、设置 canary、调用一次 `thread/delete` 并重启检查 | 无 provider credentials、0 model turn、无 MiniMax、无真实数据；不触碰真实 Runtime Home | agent-runtime-team | Complete for DEC-126-006 evidence：response/event/live row/rollout/restart absence PASS；`state_5.sqlite-wal`/`logs_2.sqlite` 字节残留，故 forensic erase NOT PROVIDED；Host cleanup仍是实现/契约项 |
| SPIKE-126-003 | title generation 的隔离 API | fixed-source fake fixtures PASS；Owner批准的 `MM-126-001` 单次 strict title在 pathless ephemeral/空 cwd 中 completed，18-grapheme sanitizer PASS | 不在用户 thread 插隐藏 turn、不触碰 project cwd；1 call/0 retry；0 tool/secret leak；temp removed | agent-runtime-team | Complete for bounded design/provider evidence；ADR-0015/DEC-126-007 Accepted、Q-008 Resolved；production Eval/Host implementation仍待后续 Gate |
| SPIKE-126-004 | Desktop local DB technology/encryption/bookmark | 临时 Rust 1.95/macOS arm64 `cargo check --locked` 验证 rusqlite 0.40.1 bundled-sqlcipher + rusqlite_migration 2.6.0；review SQLCipher/SQLite/Apple 官方边界 | 不加 repo 依赖、不写真实 project/message | client-team | Complete：build PASS；Refinery 0.9.2 与 rusqlite 0.40.1 `libsqlite3-sys` links 冲突而拒绝；ADR-0014 Accepted/Q-015 Resolved |
| SPIKE-126-005 | Public Tasks consumers/legacy usage | 2026-08-02 source inventory：Desktop无active call；API为不安全legacy provider；Infra仅deny；Host同名route为不同contract；admin/connectors/knowledge/skills无active ref；generated SDK仅artifact。外部因Public OpenAPI按`unknown-public`安全类别处理 | 不开放route、不访问production；不虚构“external=0” | platform-team | Complete：Q-010 Resolved；DEC-126-011/012 Accepted |
| SPIKE-126-006 | Chat/App Shell sidebar information architecture | 已将G1语义、DESIGN-126-003 history/raw states与1180×760/a11y要求写入Desktop FEAT-126 Pattern | 不改业务代码；仅取代Accepted 01/02中的FEAT-126冲突段落；不把临时截图当发布资产 | client-team | Complete / Accepted 2026-08-02 |
| SPIKE-126-008 | S8B0 UI consumption/readiness | 只读盘点后按Accepted DESIGN实现router/nav/permission/chat store/private IPC/pages接线，关闭readiness/storage缺口 | 不改central contract/Host/Runtime；不启用flag或启动provider；不做完整Chat Vue/visual | client-team | DESIGN/DEC-126-032 Accepted；LIA-126-005 complete；DEC-126-033 Accepted / Closure Passed |

## 12. S8B 实际影响差异（LIA-126-006）

| 边界 | 实际变化 | 未变化 | 结论 |
|---|---|---|---|
| Desktop Vue | 新增Chat composer、reasoning disclosure、project/session tree、scroll composable、稳定UI projection和真实页面测试 | 无mock/static production data | 当前切片唯一业务实现边界 |
| App Shell | Chat active时固定展开且不暴露侧栏显示/隐藏；1180×760及200% zoom等价视口下主要操作可达 | 其它页面既有sidebar store仍保留 | FEAT-126排除功能未泄露 |
| Pinia/private IPC | Vue仅调用Accepted authoritative store actions | 22 commands、7 events、cursor/error、Rust domain均未修改 | 未触发private IPC停止条件 |
| 数据/安全 | assistant/raw reasoning仅文本插值；stable readiness/cleanup/error本地化；无路径/secret/raw wire | SQLCipher schema、Host/Public Tasks/Runtime无变化 | 无migration/G2A重审 |
| 依赖 | 新增固定`axe-core@4.10.3` devDependency及lockfile证据 | production dependencies与bundle均无新增 | npm advisory为0；test-only |
| 远端/运行 | Desktop仅本地commit，feature flag unset/false | 无push/merge/tag/publish/deploy/MiniMax/真实数据 | 用户可观察默认行为不变 |

Contract impact for S8B：`semantic`（Desktop-private UI consumer）。它改变default-off候选页面的可观察交互，但不改变任何跨仓/跨进程shape；central feature的最高风险分类仍保持`breaking`，G2A不回退也不重开。

## 13. S9 实际影响差异（LIA-126-007）

| Repository | 实际变化 | 未变化 | 结论 |
|---|---|---|---|
| yijie-agent-host | test-only generator、250条合成dataset、split/schema/lock、deterministic Go test runner、Make target | session/title/reasoning production实现、Host/Public Tasks wire、Runtime pin | Host为唯一Eval authority；local checkpoint `8707dea…c9378` |
| yijie-desktop | vend exact Host SSE/consumer fixtures、authority lock、Rust SQLCipher lifecycle test、Vue plaintext consumer test | private IPC、Rust production domain、Vue production组件、dependencies/lockfiles、flags | 第二套评分标准未产生；local checkpoint `adfdb5b…af9cb` |
| yijie | feature package与DEC-126-036 Closure证据 | contracts/API/Infra/Runtime | governance only |
| 外部系统 | 无调用 | MiniMax、registry、remote Git、production/real data | side effect=0 |

S9自身contract impact为`additive-test-only`；FEAT-126总体仍保持`breaking`，无需G2A重审。

## 14. S10BF1 实际影响差异（LIA-126-019）

| Repository | 实际变化 | 未变化 | 结论 |
|---|---|---|---|
| yijie-agent-host | test-only fake health显式拆分dataset/case；新增Host-owned closed readiness probe与负向测试 | default MiniMax/provider、Host业务HTTP/SSE、bbolt/session、Runtime pin | local checkpoint `1ca4ee5…a560`；操作者不再提供fixture identity |
| yijie-infra | 新增唯一S10B-001组合preflight runner、七SHA/fresh-run/default-off/no-log/cleanup验证与103项回归 | Compose pins、API/Host/Public wire、业务schema、既有S10E命令语义 | local checkpoint `5723ffd…c0c9`；不构造fake header或复制case常量 |
| yijie | DEC-126-056/057 Accepted、LIA-126-019执行与S10BF1 Closure证据 | G2/G2A、S10B-R4失败历史、G4/G6 | governance only；执行基线`db12fe6…cc4d`；BLK-005 Closed；R5未授权 |
| 其它仓库/系统 | 无源码变化 | Contracts/API/Desktop/Runtime pin、MiniMax、真实数据、Keychain、远端Git | side effect=0；S10B-R5未执行 |

S10BF1 contract impact为private test/deployment tooling `semantic`，central G2A=`N/A`。它只消除预检身份与人工编排歧义，不改变产品行为或对外兼容面。

## 15. DESIGN-126-012 / S10BRP1 实际影响差异

| 边界 | 当前候选变化 | 兼容与停止结论 |
|---|---|---|
| API runtime config | 新增正式closed `feat-126-s10-local-lab`分支，复用API-owned bootstrap authority校验专用DSN/environment/issuer，并增加exact flags、JWKS、CA pin、canonical port与loopback限制 | private local deployment语义由错误的FEAT-125 profile切换到专用FEAT-126 profile，故`contract-impact=semantic`；default与FEAT-125路径保持既有行为 |
| API route exposure | 新profile启用既有secure v2 tasks/access projection并隔离legacy `/v1/tasks` | 不新增或修改Public Tasks HTTP wire；仅改变何种closed local profile可启动现有handler集合 |
| Infra authority | 新增唯一versioned `FEAT_126_S10_API_RUNTIME_AUTHORITY`；preflight从其构建child env并把完整closed投影写入summary | 不接受operator profile/endpoint/database/issuer/gate override；drift、extra key或错误run/scope/status fail closed |
| Continuation | 唯一`make feat-126-s10b-api-continuation`从固定run路径读取安全工件，以summary `api_binary_sha256`和安全open前后双快照绑定preflight-built binary，实际调用同一Infra module的runtime env builder与summary reader后启动foreground child | 接口只接收run ID与七仓SHA，拒绝profile/path/secret/binary override与digest/dev/inode/mode/size/mtime漂移；launcher conformance已通过但没有执行S10B-002–012，不把harness写成完整链PASS |
| Central contracts/schema | 无source、generated SDK、Public Tasks/Host wire、Desktop IPC、PostgreSQL/SQLCipher业务schema或Runtime pin变更 | central G2A=`N/A`；唯一contracts candidate仍为`29317b6426578749dc698fc2ad32b986ee5c8e9f` |

父基线仍为API `c5f334e88d54d9e04f388d0349f4f5925124abd6`、Infra `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`和Governance `bcae57085b4fcb21a9d83f2ab08bc6c308228510`。DEC-126-059 Option A接受后形成API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`与Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135` clean local checkpoints，均未push；`S10B-BLK-006` Closed。LIA-126-022仅改变一次fresh local E2E的授权状态，不改变central contracts、wire、schema、Runtime pin、默认行为或生产范围。

## 16. DESIGN-126-018 / LIA-126-032 实际影响差异

| Repository | 实际变化 | 未变化 | 结论 |
|---|---|---|---|
| yijie-desktop | `feat126-s10-driver` + `EphemeralFile`仅接受以canonical UUIDv4绑定的Infra generated run root；cleanup复用同一校验 | default build、Protected Data Keychain、业务IPC、SQLCipher schema、发布bundle语义 | private local test-driver `semantic`；checkpoint `9771da11c47406e45526dea104f3d7de05701fba` |
| yijie-infra | failure closure/reconcile允许“failure class + 已知scope”；runtime no-log v2持久化去重后的命中来源集与规则集SHA-256并兼容v1读取 | Compose pins、业务case、公共wire、真实日志正文、默认flags | private deployment/test `semantic`；checkpoint `61062143fa3c81b90792ec6f48aea7d6408ed06d` |
| yijie | LIA-126-031失败审计、DEC-126-073 corrective与DEC-126-074 checkpoint记录 | central contract source、G2A与产品代码 | governance only |
| Contracts/API/Host/Runtime | 无源码变化 | exact SHA保持既定checkpoint | central G2A=`N/A` |

第三次失败run `056a4dab-6afc-45ff-bfff-d1fcc67d2394`永久不可复用；其四个retained volumes仅只读inspect并原样保留。corrective阶段未执行live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用或远端写入，`s10b_r8_executed=false`。

## 17. DESIGN-126-019 / LIA-126-033 一次性综合corrective影响

| Repository | 最小文件范围 | 语义影响 | 明确不变 |
|---|---|---|---|
| yijie-desktop | 产品文件仅`src-tauri/src/feat126_s10_driver.rs`、`src-tauri/src/lib.rs`、`src/feat126/s10b-driver.ts`、`src/main.ts`；允许同步更新`src/feat126/s10b-driver.test.ts` | `component_ready`前的native、Tauri setup与frontend启动失败投影为一次性、closed、content-free `startup_failed`；`component_ready`成功后该startup终态不可再被failure覆盖 | production/default build、Protected Data Keychain、业务IPC、SQLCipher schema和业务数据流 |
| yijie-infra | `scripts/feat-126-s10b-orchestrator.mjs`及S10BO2/S10BO3 targeted tests | FD4完整frame优先于并发child exit；Desktop leaf成为primary failure，EOF仅为无frame fallback；runtime-log-scan writer升级到v3，绑定exact Docker labels、stable service roles和origin-rule pair digest；no-log改为JSON/value-aware closed分类 | Compose pins、Public Tasks/Host wire、业务case、默认flags、历史evidence字节 |
| yijie | 现有FEAT-126 package内的design/test/verification/release记录 | governance only；本轮结果、checkpoint和SHA在真实执行后回填 | 不改变中央契约或产品源码 |
| Contracts/API/Host/Runtime | 无文件 | 无实现影响 | 精确既有checkpoint保持；若实现发现必须修改任一仓，立即超出本corrective并停止 |

本轮最高影响为`semantic`，但仅限不可发布的Desktop↔Infra private local deployment/test control与evidence interface；central G2A=`N/A`。实施形成Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`与Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`两个local clean/not-pushed checkpoint；Contracts/API/Host/Runtime保持既定SHA且clean。离线阶段未启动Docker容器、真实组件、isolated live、fresh R8、业务case、S11、MiniMax、真实数据、Keychain或远端动作；历史run/evidence/retained volumes保持不变。Corrective Closure为Review Ready / Pending Owner Acceptance。

## 18. DESIGN-126-020 / LIA-126-035 Startup Durability Corrective Impact

LIA-126-034 run `41cdd1c7-e1a6-43ae-ac3a-706ff6989e99`在Desktop已持久化process identity后，60秒内既未产生`component_ready`也未产生closed `startup_failed`；Infra随后因`desktop_spawned` phase/descendant约束拒绝`orchestrator_control_timeout` failure evidence，runtime-log-scan v3又将Caddy structured metadata归入`unclassified_sensitive_field`。该run保持FAIL、永久不可复用，历史evidence与retained volumes未改变。

本轮实现影响仍为`semantic`，且只覆盖不可发布的Desktop↔Infra private local startup/control/evidence interface。Desktop新增content-free native startup stages/watchdog、真实Tauri mock `AppHandle/setup` fixture、first-terminal-wins及FD4 flush/close-before-exit；Infra将immutable primary failure先于abort/business/cleanup持久化，接受pre-ownership API/fake/Desktop known scope，并用nested/value-aware Caddy分类及field-class摘要扩展runtime-log-scan v3。Contracts/API/Host/Runtime/Public Tasks wire、durable schema、Runtime pin、Compose pins和default flags均未改变，central G2A=`N/A`。

Owner通过DEC-126-077接受DESIGN-126-020 / LIA-126-035 Corrective Closure。实现checkpoints为Desktop `713bd5a2985c491db5d6cfc3e31f8f509994427d`与Infra `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`，均local、clean、not pushed；其余实现仓保持既定SHA。该接受不构成isolated-live PASS，G3保持Partial，G4/G6 Pending。

## 19. DESIGN-126-021 / LIA-126-036 Runtime-log-scan v4 Authority Impact

- `contract-impact=semantic`，仅影响不可发布的FEAT-126本地deployment/test evidence接口。`yijie-contracts`、Public Tasks、Host wire、Runtime source/pin、Compose pins、持久业务schema与默认flags均不变，central G2A为N/A。
- Governance权威源先固定runtime-log-scan writer v4、v1/v2/两种v3 reader兼容、exact-key、空集合和reason-class摘要语义；随后才允许恢复已经存在的Infra corrective diff。
- v4 writer比explainable v3只增加`hit_reason_class_set_sha256`和`hit_origin_rule_field_class_reason_class_set_sha256`。evidence继续只保存counts与稳定摘要，不保存字段名、值、路径、日志正文、token、secret或业务内容。
- canonical Desktop production build必须显式使用`feat126-s10-driver,tauri/custom-protocol`，不得依赖`devUrl`、Vite dev server或1420/1421端口。
- 本阶段固定Governance基线`5da2d93b7c4e3ee9884b0fedb04261b5aaf65f92`。Infra基线为`222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`，且允许仅四个既有corrective文件保持预期dirty；该状态不构成基线失败，也不得在Governance阶段修改、暂存或提交。
- 两阶段checkpoint互相独立：先形成Governance local clean checkpoint，再完成Infra剩余门禁、独立只读审查与单一local clean checkpoint。Governance commit不预填尚不存在的Infra新SHA。

DEC-126-079现已接受DESIGN-126-021 / LIA-126-036 Corrective Closure。Infra从父SHA `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`形成local clean checkpoint `ef9984b06c2913b1d7561360b1e3e569cbfd9d4a`，严格包含orchestrator、BO2/BO3 tests和脱敏Caddy fixture四个文件；Contracts/API/Host/Desktop/Runtime均未改变。该接受只关闭repository corrective，不构成isolated-live PASS，G3仍为Partial，G4/G6 Pending。

## 20. DESIGN-126-022 / LIA-126-038 Login-leaf and Caddy Event-shape Corrective Impact

LIA-126-037 run `5a52227e-64cf-4544-9a42-527c512433fe`在`desktop_starting`形成canonical `driver_login_failed` failure/closure。历史Desktop在唯一IPC边界不可逆丢弃内部`NativeAuthError`，因此现有evidence只能证明首个失败位于feature-only synthetic login chain、project registration和Host/Runtime startup之前，不能诚实恢复为某个更细的历史stage leaf。runtime-log-scan v4的单一tuple摘要精确绑定Caddy origin、unclassified rule、structured-unclassified field class和`unclassified_caddy_system_value` reason class；确切分类原因是旧scanner只拥有不完整的字段级Caddy allowlist，无法把观察输入归入closed Caddy 2.11.4 system event authority。privacy-preserving evidence没有保存原始record，所以具体触发record不可恢复；该摘要也不证明敏感值泄漏。

本corrective的最高影响为`semantic`，仅限不可发布的Desktop-to-Infra local startup/control/evidence interface。Desktop把synthetic login的secret authority、authorization start/request/page、form、credential submit/reject、callback、token exchange、session/storage/runtime/concurrency失败闭合为content-free stage leaves；Infra接受并持久化这些leaves，同时用top-level exact event shape解释脱敏Caddy 2.11.4 startup/admin/TLS/reverse-proxy metadata。array/scalar root、unknown key/value和malformed nested access object继续fail closed。中央Contracts、Public Tasks、API、Host、Runtime、durable schema、Compose pins和default flags不变，central G2A=`N/A`。

Owner通过DEC-126-081接受Desktop `b066e8d08b5f80521c87a6505649b1bb3a62d83b`与Infra `cf00b4caacefbd35823dffafb9e23653484bc576`的Corrective Closure。实际Keycloak页面/credential/callback/token exchange、project registration、Host/Runtime ownership/readiness及live Caddy event集合仍必须由下一次isolated-live验证；因此G3保持Partial，G4/G6 Pending。

## 21. DESIGN-126-023 / LIA-126-039–040 Callback and Caddy Storage-cleaning Corrective Impact

LIA-126-039 run `5633d030-9486-4824-bf2c-7f0ee7954b58`在真实Keycloak授权成功后，由Desktop以`driver_login_callback_rejected`终止。离线只读审计确认Keycloak 26.7.0的`session_state`由18个随机字节编码为24字符base64url opaque值，旧Desktop却错误要求canonical UUID。runtime-log-scan v4的唯一Caddy命中对应Caddy 2.11.4/CertMagic 0.25.3 storage-cleaning skip system event；旧Infra缺少该top-level exact event shape。这两项均属于已固定版本的private startup/evidence语义，不涉及真实业务数据或公共wire。

本corrective的最高影响为`semantic`，仅限不可发布的FEAT-126 Desktop/Infra local startup验证。Desktop仅修改`src-tauri/src/native_auth/synthetic_agent.rs`，接受精确24字符base64url session state并继续闭合scheme/host/path/state/issuer/code。Infra仅修改orchestrator、BO3 test及脱敏Caddy fixture，接受exact logger/message/instance/try-again shape和时间关系，未知、cross-shape及非法值继续fail closed。Contracts/API/Host/Runtime、Public Tasks、durable schema、Compose pins与default flags均不变，central G2A=`N/A`。

Owner通过DEC-126-082接受Desktop `475086f1e68bcd1e0820a07b727d741e22a1bf62`与Infra `e4e92ff1c2f7cbb7627917fb0bc04a5c9bd1b2e2`的Corrective Closure。仓库门禁与独立复审无open P0/P1；真实callback continuation、project registration、Host/Runtime ownership/readiness、一次性abort、现场Caddy集合及资源归零仍由下一次isolated-live验证，因此G3保持Partial，G4/G6 Pending。

## 22. DESIGN-126-024 / LIA-126-041–044 Live Caddy System-event Corrective Impact

LIA-126-041、042、043分别消费run `909e7b8b-93e0-4497-adbf-579d7afb90e1`、`7eeb81fa-7969-4b9f-b979-a3ad3ba1a3c8`和`8001b5ae-4916-41fd-81db-0617e862a6c3`。三者都在`desktop_exited`形成`orchestrator_no_log_invalid` failure/closure，process scope包含API、fake、Desktop、Host和Runtime，business boundary PASS且fake accepted/rejected calls均为0。三份runtime-log-scan v4均为四个exact sources、69 rows、单一Caddy unclassified tuple；这些run均已消费、永久不可retry/resume/reuse，不能合并为一个live PASS。

统一离线审计确认影响仍仅为Infra private runtime-log classification semantics。固定Caddy 2.11.4现场系统日志包含与旧脱敏fixture不同但content-free的startup/admin/TLS/reverse-proxy元数据形状。旧closed event authority不能解释这些值，因而按设计fail closed；摘要不证明token、secret或业务内容泄漏。corrective只修改Infra orchestrator、BO3 test和完全脱敏fixture；Contracts/API/Host/Desktop/Runtime及central G2A均不受影响。

DEC-126-083接受Infra `d4749cb31242799d7cb8f566d44bea3c1f085d8a`。BO2/BO3 targeted `51/51`、full `193/193`、`make lint`、Compose 5.3.0 config-only、Node/Shell syntax及diff检查PASS，独立只读审查无open P0/P1。实际live输入仍须由新七仓SHA上的LIA-126-045验证；因此G3保持Partial，G4/G6 Pending。

## 23. DESIGN-126-025 / LIA-126-045–046 Run-artifact No-log Authority Impact

LIA-126-045 run `f07e9f3f-bc8f-4a3d-9da9-b79ba70054b2`已完成真实API、fake、Desktop、Host和Runtime startup、ownership/readiness、business boundary与一次性abort。runtime-log-scan v4为4个exact sources、69 rows、0 hits；business boundary前后API摘要相同，fake accepted/rejected calls均为0。最终failure/closure仅为`orchestrator_no_log_invalid` at `desktop_exited`，scope=`run_artifacts`。该run永久不可retry、resume或reuse，不能因主startup链通过而升级为live PASS。

离线只读审计确认旧scanner把既有closed evidence/log authority中的字段按字段名宽泛判为敏感或不可分类，包括精确startup message、本地JWKS authority、固定retained-volume keys、authorization revision、secret descriptor SHA-256及synthetic secret roles。没有发现实际token、secret、路径或业务内容泄漏。corrective只在字段名与精确值/结构同时匹配时放行；unknown message、非权威JWKS、错误digest/revision/role/volume顺序及unstructured内容继续fail closed。

最高影响为`semantic`，仅限Infra private local no-log classification。runtime-log-scan v4 evidence shape、digest算法、Docker/Caddy authority、central Contracts、Public Tasks、API/Host/Desktop/Runtime wire、durable schema、Compose pins与default flags均不变，G2A=`N/A`。DEC-126-084接受Infra `58dc41f16e1d3411d7170cc2f5b10843a1ad13c5`；G3保持Partial，G4/G6 Pending。

## 24. DEC-126-085 / LIA-126-047 Startup/Abort Closure and Fresh R8 Impact

LIA-126-047 run `7e18d0aa-317e-4fa5-a7a5-a93d7880eb8e`绑定Governance `322fb73774d0392028ea0b32166c8472288c9215`、Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`、Desktop `475086f1e68bcd1e0820a07b727d741e22a1bf62`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`和Infra `58dc41f16e1d3411d7170cc2f5b10843a1ad13c5`，形成canonical success closure。API、fake、Desktop、Host和Runtime的startup、ownership、readiness与single abort均通过；容器、网络、进程、listeners和temporary volumes归零，四个named volumes按协议保留且未读取、挂载或删除。

runtime-log-scan v4为4个exact sources、69 rows、0 hits；整体no-log覆盖31个local files与4个external sources、95 rows、0 hits。API before/after摘要相同，fake accepted/rejected calls为`0/0`，Public Tasks、conversation、turn和provider调用均为0，`s10b_r8_executed=false`。DEC-126-085的Governance处置为`contract-impact=none`，不改变Contracts、Public Tasks、Desktop/Host/Runtime wire、durable schema、Compose pins、default flags或生产状态。

Owner同时授权LIA-126-048一次fresh R8，但该授权只覆盖frozen S10B-001–012、synthetic fixture `normal-000`、loopback fake provider和本地隔离资源。它不授权MiniMax、外部provider、真实数据、Keychain、S11、默认启用或远端操作。执行必须在本Governance checkpoint后绑定新的七仓exact clean SHA，并通过一个实际执行全部case的canonical full-case入口；startup/abort-only入口不能作为替代。若入口不存在、preflight失败或出现任何不确定状态，授权保持未消费或形成单次失败closure，不得人工拼接、重试、resume或复用run ID。

## 25. DESIGN-126-028 Host Opaque Project CWD Durable Impact

本设计的最高影响为`semantic`。wire字段与形状没有变化，但exact FEAT-126 profile下Host private bbolt的跨重启解释从“record中保存canonical absolute CWD”改为“record中保存固定opaque sentinel，并在每次打开后从重新验证的run authority恢复canonical CWD”。因此不能继续以“durable schema unchanged”描述该profile；它是经过Owner批准的private local durable semantic change，中央Public Tasks、Runtime protocol和业务数据schema不受影响。

| Repository | 本轮状态 | 后续corrective影响 |
|---|---|---|
| yijie | 只更新现有FEAT-126 package与`feature.yaml`并形成一个local clean checkpoint | 权威定义marker/version、rehydration、compatibility、contract wording和rollback |
| yijie-agent-host | `78e7e91fc89cff14caeb5eb4da01d7f52a690630`上的预期dirty draft，尚未接受或提交 | private bbolt encoding、exact profile/run-root validation、restart/default/rollback tests；Host contract snapshot只能从权威source同步 |
| yijie-contracts | `e7820395486ad05fab2cd13b5b13f77e33880c14` clean；本轮不修改 | 若恢复corrective时同步OpenAPI文字，必须从`openapi/agent-host/agent-host.yaml`权威source修改并按Contracts门禁生成/验证；不得手改Host snapshot |
| yijie-desktop | `b2ca6b52ef05f46f0224069e5689ac09e95288da`上的预期dirty draft，尚未接受或提交 | 保持当前campaign draft；不得因本设计扩大Public Tasks或业务IPC |
| yijie-infra | `af155ae4eb68a92e967e7f730b975f9558356dda`上的预期dirty draft，尚未接受或提交 | 只消费exact profile/run-root authority并补convergence/rollback fixtures |
| API / Runtime | API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Runtime `0ce5902ed400866be0196886bb78f693a004d68d` clean | 无本设计源码影响；发现需要修改时重新评估范围 |

本Governance checkpoint不接受上述implementation draft，也不将任何门禁标为实现PASS。它不授权Docker lifecycle、isolated-live、canonical R8、MiniMax、业务调用、真实数据/Keychain、default activation或远端动作。

## 26. DESIGN-126-029 Post-checkpoint Review Errata Impact

独立只读review确认DESIGN-126-028方向成立，但原checkpoint存在4个implementation-blocking P1。DESIGN-126-029以`semantic` private durable/deployment impact修正权威，不改变Public Tasks、Host wire shape、Runtime protocol或default产品行为：

- planned restart复用same run ID、canonical run root、project和bbolt store，但每次Desktop lifecycle/Host spawn必须生成fresh canonical instance nonce并验证独立`host/<nonce>` authority；
- metadata除`feat126_cwd_encoding=opaque-project-v1`外必须持久化`feat126_run_id=<canonical UUIDv4>`；open时与run-root basename和profile run ID三方一致，阻断跨run复制/rebind；
- 只有本次调用以exclusive create新建的`sessions.db`可以初始化marker/run ID。任何pre-existing unmarked DB即使empty、曾删除至empty或只剩freelist page也拒绝；
- run root、project、host root/current nonce dir、host-home、codex-home均须在exact profile启动前strict验证owner、non-symlink、canonical equality和精确`0700`，不得靠后续chmod或symlink-following API修复。

本纠正将LIA-126-051 offline实现范围明确为Contracts、Host、Desktop、Infra。Governance先形成clean checkpoint；随后各仓可以在现有dirty draft上继续最小修改、全量门禁、独立review与local commits。Docker lifecycle/live/R8仍不授权。
