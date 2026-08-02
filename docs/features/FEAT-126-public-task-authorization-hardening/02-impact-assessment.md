# FEAT-126 现状扫描与影响评估

## 1. 调查基线

初始扫描时间：2026-08-01；G2 补充扫描：2026-08-02，Asia/Shanghai。所有 sibling 仓库只读；未 fetch、checkout、generate 或修改。

LIA-126-002于2026-08-02进行了第二轮跨仓审查并建立仅本地WIP checkpoint。该审查发现S4–S6存在未覆盖P1，因此三者均调整为`Conditional / Corrective Closure Required`；同时确认Public Tasks canonical `conversation input.text` fixture与content-free数据边界冲突，已按停止条件暂停实现并提交DEC-126-023/G2A复审。

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
| yijie-contracts | 公共 wire 权威源 | prior G2A candidate remote-available；DEC-126-023 re-review required；Draft PR merge HOLD | Public Tasks versioned hardening + Agent session-event v2 + Host title/cleanup/events operations | platform-team | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`保持immutable/remote-available，但其arbitrary `input`与canonical `conversation input.text` fixture不满足content-free-only边界；不得继续作为S4实现依据，等待Owner决定是否形成新candidate |
| yijie-api | Public Tasks provider | direct future | bearer、tenant/resource auth、list/mutate/delete/审计 | backend-team | auth middleware/application/repository/migration/tests |
| yijie-agent-host | Runtime adapter | direct future | Desktop lifecycle、versioned raw-reasoning projection、cleanup/title operation 候选 | agent-runtime-team | 先走 Runtime/contract candidate；正文不进logs/bbolt，不持有业务主 DB |
| yijie-desktop | 产品 consumer/local data owner | direct future | UI、native picker、local DB、sidecar transport、states | client-team | Pattern/contract pin/Tauri/domain/store/components/E2E |
| yijie-infra | route/profile activation | indirect future | legacy isolation、flag、host/ingress、observability | devops-team | 默认关闭、双轨 route 与 smoke |
| yijie-codex | canonical Runtime | conditional | stable Runtime已有delete/name/summary/raw reasoning/outputSchema；MiniMax title单样本PASS，MM-126-002证明raw事件存在；当前缺口在Host bridge、raw conformance/caps/completion与title Eval | agent-runtime-team | 预期先不改Runtime source；raw feature flag默认off；仅exact-pin conformance失败时再提候选并重审 |
| yijie-admin-web | Admin app | none | 本期仅 Desktop；source scan未发现Public Tasks active consumer | admin-platform-team | Q-010 repo-local inventory complete；未来接入只允许v2 pin |
| yijie-skills | AI capability | none | 纯文本通用 turn，不新增 skill/tool | ai-product-team | N/A |
| yijie-connectors | 平台适配 | none | 无平台调用或副作用 | integration-team | N/A |
| yijie-knowledge | RAG | none | 无检索/embedding | data-ai-team | N/A |

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

以下是仓库真实入口；LIA-126-001已运行API、Host、Desktop的既有门禁，但LIA-126-002复审证明这些绿色结果未覆盖当前P1。S4–S6不再记为Complete，完整本地链路与S7–S11均未启动。

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
3. Contracts既有candidate曾通过G2A且保持immutable；DEC-126-023现要求重新评审其`input`数据边界。DEC-126-021仍保持Draft PR/HOLD，远端红色CI继续只阻断merge。
4. LIA-126-001形成了Public Tasks、Host v2与Desktop local repository/sidecar基础；LIA-126-002将S4–S6统一降为Conditional并在contract conflict处暂停。所有flags/routes仍默认关闭，S7–S11继续禁止。
5. 下游只固定完整SHA或已核验本地投影；先实现consumer tolerance，再启用本地provider新events；浮动branch不得作为契约身份。
6. 完成security/migration/resilience/visual、四组件本地E2E和结构化审查后，提交Owner本地G6验收；不讨论线上activation。
7. 如未来需要把源码纳入共享`develop`，必须先修复dependency audit、取得远端全绿CI并另行审批merge；merge不等于部署。

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
