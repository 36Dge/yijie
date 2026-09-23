# FEAT-155 Q-01 — 调度机制与 Codex 复用边界技术决策稿

> 当前决策状态：Q-01～Q-04及D0已接受；16小时获例外；Runtime资格由29解决；防自动空闲睡眠及睡眠后停止发送已由用户排除。以下为原调查、推演与阶段记录，不能用旧pending/仅设计/唤醒保留覆盖[00现行定义](00-feature-brief.md)与[48交付](48-remaining-delivery-report.md)。

> 2026-09-18审计收敛：Host查询仅精确local/demo_fast、owner-only bearer及ID关联；Trace不作授权，Desktop native scope由第三阶段兑现。responding Host实例不表示历史执行generation，缺失保持unknown。睡眠监听/恢复屏障须先于第三阶段自动调度；第四阶段接防空闲睡眠开关。有限计划授权须绑定plan/revision、次数、有效期并在出站前占用，耗尽/到期停止；12次文本是整个FEAT的验收总账，不是无限期产品授权。具体定义见[05](05-phase-1-implementation-plan.md)，用户已授权先修订后实施阶段一。

> 后续状态：2026-09-18用户已接受推荐方案、系统通知延期及超过16小时的安排，见[04](04-owner-approval-and-implementation.md)。随后改为分阶段推进，已授权并完成[前两阶段基础](08-phase-2-implementation-report.md)，停在第二阶段，未进入执行闭环阶段。本页以下保留调查与提议形成时的状态，不继承为产品验证；当前授权/实施状态以04、05和feature.yaml为准。

> 2026-09-18 · Proposed · Owner：段成威 · 仅只读调查与需求设计
> 调查结论已形成，推荐方案已收敛；Owner 尚未批准，Q-01 decision/D0 仍为 pending，实施未授权。本文不是产品实现、运行验证或依赖安装记录。

## 1. 三个明确结论

1. **当前固定 yijie-codex 没有可直接接入的完整计划调度服务。** 已逐项核对固定 stable schema 的87个 ClientRequest method、对应分派/处理源码及持久表类别，未发现计划CRUD、日历规则、到期触发或计划恢复能力。能复用的是原生 thread/turn、审批、结果、结构化输出约束，以及易界已有的持久 outbox、Host操作幂等和加密产品记录。当前 Codex 应用中的定时任务不能当作该 Runtime fork 已提供的API。
2. **推荐 Desktop Rust/native 负责本机计划与投递账本，复用原聊天执行链。** 计划与最小run元数据保存在现有SQLCipher、共用串行worker；成熟时间库计算发生时刻，Tokio只负责等待；原有Coordinator/Host仍负责原生执行与事实保管。不新增API scheduler、Redis、常驻Host、模型工具服务或Runtime patch。新增本地计划职责及必要契约必须批准，不能以“薄适配”名义假装没有新增代码。
3. **PDF主体在该方案上可设计承接，但不是纯UI工作。** 三种“运行于”均有可复用执行基础，需补工作目录、原子关联和后台授权；保持唤醒需要新增macOS原生能力；应用内通知需接线，系统通知可独立延期。完整范围初步估算超过当前12/16小时Demo时间盒，D0前必须明确范围取舍，不能用假卡片或跳过Must收口。

职责扩展另列 [ADR-0020（Proposed）](../../adr/ADR-0020-local-scheduled-task-authority.md)。本文细化推荐方案；原 [00](00-feature-brief.md) 仍是需求入口。若Owner未批准本文中的收窄建议，原Must范围不自动删除。

## 2. 调查方法与证据边界

- 七仓HEAD/分支/远端与上一轮一致；元仓已有未提交FEAT-155四文件，作为前序成果保留；六个相关兄弟仓保持clean。精确基线、源文件SHA-256和完整87个method清单见 [只读审计记录](evidence/q01-source-audit-20260918.json)。hash用于定位所读源码，不是构建/运行资格。
- 核对中央AGENTS、长期记忆、demo_fast手册、Contract First、ADR-0010/0013/0014/0018、当前兄弟仓规则及实现；旧文档与代码不一致时标明实际代码，不把早期“审批未实现”延用为现状。
- 官方资料仅用于区分产品表面、评估成熟组件与平台边界；固定Runtime能力仍以锁定源码/canonical schema为准。没有安装依赖、fetch/切分支、生成契约、访问用户DB/凭据、启动服务或调用模型。
- 只读能证明接口/算法/存储路径存在，不能证明当前Provider结构化输出合规率、打包通知权限、正常睡眠恢复或最终端到端可用。这些列为未来正常验证，不伪称已PASS。

## 3. 复用清单与确切缺口

下表路径相对对应仓库，行号基于审计记录的HEAD；R表示可复用基础，A表示必须新增/适配，N表示不作为本方案机制。

| ID | 事实与源码证据 | 结论 |
|---|---|---|
| R01 | Codex `.yijie/upstream.env` / `UPSTREAM.md:5`固定Runtime0.144.6、rust-v0.144.6、upstream `5d1fbf26c43abc65a203928b2e31561cb039e06d`；checkout HEAD为`6c1ad767…` | 保持固定来源，不升级或改二进制 |
| R02 | Codex `app-server-protocol/src/protocol/common.rs:472–1197`完整ClientRequest枚举；canonical JSON共267文件、87 methods；`app-server/src/message_processor.rs:1008,1025,1138,1238,1256`有thread start/resume/read与turn start/interrupt实际分派（均位于codex-rs下） | 原生执行已存在；没有对应的计划CRUD/到期调度方法 |
| R03 | Codex `codex-rs/app-server/src/request_processors/turn_processor.rs:521`提交`Op::UserInput`；`protocol/v2/turn.rs:140`及stable `v2/TurnStartParams.json:576`含outputSchema | 一次turn可复用，不能把turn当定时器；结构化计划草案可走stable能力 |
| R04 | Host `internal/codex/title.go:175–190,223–230`已有封闭outputSchema及严格校验；普通`session_protocol.go:752`尚未透传该字段 | 复用模式，新增受限“计划草案”契约；标题能力不证明计划模型输出已可用 |
| R05 | Host `internal/session/multimodal.go:100,142,155,175`与`store.go:755,895`持久operation_id/输入摘要、accepted重放、pending/uncertain阻止重投 | 幂等基础存在；必须复用，不能只靠按钮禁用 |
| R06 | Host `session_protocol.go:57`说明clientUserMessageId仅关联；`native_conversation.go:224–249`历史可partial；`native_thread_status.go:9`为只读状态 | 无Runtime端幂等事务；缺历史、idle/notLoaded不证明此前未执行 |
| R07 | Host `store.go:701,722`约束task→session、thread→session；`service.go:312`先Reserve后thread/start再Bind | plan/run与conversation/task不能共用ID；创建响应丢失也存在unknown缺口 |
| R08 | Desktop `database.rs:779–808`加密/迁移，`worker.rs:199–225,243–257`串行repository worker，`database.rs:1702,2099–2214`会话/turn/outbox事务和operation去重（均在src-tauri/src/chat） | 复用同库同worker；不能串两次IPC就宣称计划/run/outbox原子 |
| R09 | Desktop `chat/application.rs:543–631,1569–1597,2068–2096`为Rust Coordinator；`ipc.rs:328–363,7472–7583`在UI context绑定路径启动/恢复 | 执行循环可复用，但要新增native生命周期owner，不额外创建一个outbox消费者 |
| R10 | Desktop `chat/authorization.rs:8,198–246,298–313`上下文最长300秒、绑定清除旧context、检查epoch/revision；`native_auth/runtime.rs:316–339`有native权限投影 | 后台不能长期缓存renderer context，也不能周期bind让UI失效；需独立native调用授权入口 |
| R11 | Desktop `chat/ipc.rs:7851`新会话必传project_id；`0001_chat_core.sql:22–36`项目FK；`application.rs:1690–1696`解析bookmark；`ChatPage.vue:217–218`页面可选择首个项目 | 尚无projectless会话；调度不能隐选用户第一个目录 |
| R12 | Desktop `0014_chat_native_conversation.sql:36–39`单会话active唯一约束；`application.rs:2081–2085`优先恢复首个active会话；`useRuntimePermissions.ts:19–51,78`只轮询当前聊天审批 | 每会话互斥可复用；全局后台容量及独立审批观察尚未接通 |
| R13 | Host `internal/codex/runtime_permissions.go:112,139,167,188–217`现行原生审批；`internal/session/runtime_permissions.go:98`阻止pending approval时新turn；Desktop`runtime_permissions.rs:6`默认Ask | 复用FEAT-152；重启不恢复旧批准回调；FEAT-137永久终止 |
| R14 | Desktop `single_instance.rs:21,73–95`与`lib.rs:122`已有flock；`Cargo.toml`有Tokio1.52.3 time/sync、Tauri2.11.5 | 单实例/等待primitive可复用，不等于持久调度和occurrence去重 |
| A01 | Desktop active源码/直接依赖无RRULE/IANA recurrence接线；Cargo.lock的chrono是传递依赖 | 需明确时间库和规则版本，不能手写时区/DST或拿传递依赖冒充现成实现 |
| A02 | Desktop无IOPM/NSWorkspace唤醒接线、系统notification plugin；`App.vue:23,248–256`仅NNotificationProvider | 原生唤醒/恢复监听和系统通知是新增能力；应用内通知也缺定时事件/去重/跳转 |
| A03 | Desktop `lib.rs:436–443`退出停Workflow/ChatRuntime；未见显式停ChatIpcRuntime coordinator；`sidecar.rs:394–400,1035–1073`部分配置仍含强杀fallback | 新调度须明确正常退出顺序和STOP_PENDING；不能启用/验收强杀路径 |
| A04 | Host `app.go:788–804`无operation查询/会话创建结果查询公开路由；`store.go:943`仅内部查询 | 新增只读投递/创建结果查询契约，不能以read thread替代精确operation恢复 |
| N01 | API `cmd/scheduler/.gitkeep`、Host `cmd/cloud-runner/.gitkeep` | 空占位，没有可接入的后台服务 |

### 3.1 对相似名称的排除

- Codex `core/src/tools/handlers/tool_search.rs:183,223`的automation_update是测试中的外部工具样例；不是本仓调度实现。
- `protocol/src/protocol.rs:2728`的ThreadSource Feature字符串是来源标签。
- `state/migrations/0014_agent_jobs.sql`服务CSV批处理；`ext/goal/src/runtime.rs:359`服务活动goal继续；`app-server/src/current_time.rs:43`是活连接中的时间/sleep。它们都不能提供FEAT-155所需持久计划/时区/到期唯一触发。
- `dynamicTools`在`protocol/v2/thread.rs:127`为experimental，Host当前只注册generate_image；本方案不借图片例外开放任意计划工具。

### 3.2 官方资料支持什么、不支持什么

[官方Scheduled tasks说明](https://learn.chatgpt.com/docs/automations?surface=app)区分每次新聊天与回到原聊天，并说明本地项目运行需要机器和应用在线。这支持产品概念，不公开证明固定fork内有同名调度模块。页面当前的无人值守审批设置也不能覆盖易界已批准的FEAT-152模式。

[官方App Server说明](https://learn.chatgpt.com/docs/app-server)说明thread/turn扩展入口与experimental API门禁。该在线页面持续变化，本包只采用固定0.144.6源码已证实的字段；不据最新文档给旧Runtime发送新method。资料读取日期2026-09-18。

## 4. 唯一推荐架构及备选取舍

```text
Vue 页面/对话草案确认
      ↓ scoped typed command
Desktop native ScheduleApplication（新增本地产品职责）
      ├─ 同一SQLCipher/串行worker：计划、发生槽、run索引、既有聊天outbox
      ├─ 日历库：有限规则 → 下一UTC时刻
      ├─ native生命周期/权限/容量/唤醒检查
      ↓ 复用同一个 ConversationApplication / Coordinator / HostBridge
Agent Host：session映射、operation幂等/只读恢复、原生审批适配
      ↓ 固定 app-server thread / turn
Codex：实际执行、原生ID/状态/内容
      ↓ 原生事实
Desktop既有记录与显示缓冲 → 定时运行索引/重要更新 → 原完整对话
```

| 方案 | 代价与边界 | 决策稿建议 |
|---|---|---|
| A. 固定Runtime内直接复用完整调度 | 当前method/持久化清单无该能力，无法给出真实接入点 | 不作为可交付方案；保持执行原语复用 |
| B. Desktop native最小产品调度适配 | 新增计划职责/日历适配/持久claim/授权和恢复，复用现成加密库与执行链 | **推荐**；只本人本机App存活期间运行 |
| C. API scheduler/常驻Host/云runner | 需要新服务、身份、离线交付、回执与运行位置；Host持有计划违反现有薄适配边界 | 不纳入本期；API计时器也不能唤醒已退出的本地Runtime |
| D. Vue timer / macOS cron/LaunchAgent直接执行CLI | 页面不可靠；OS定时命令绕开产品outbox/审批/生命周期且引入另一个执行入口 | 不采用 |

新增职责：Desktop拥有计划定义、启停和投递账本；Host仍只持映射及必要的幂等恢复元数据；Codex仍裁决Thread/Turn/Item执行事实。日历库负责时间计算，不负责授权或提交。Runtime与用户代码目录不存计划JSON/TOML；不读写本机Codex应用的automations目录来假装集成。

推荐业务实现影响仓收敛为Desktop、Host、Contracts，元仓记录治理；Runtime只读固定来源，API/Infra无需新增服务或配置。后续如该假设被推翻必须重开决策。

## 5. 数据、标识和工作目录

### 5.1 最小数据模型（概念，不是已发布schema）

| 对象 | 拟保管的信息 | 权威与边界 |
|---|---|---|
| Schedule | scoped plan_id、revision、名称/提示词、规则/时区、目标模式、安全工作目录引用、启停、权限意图、下次时刻、成本授权引用 | Desktop SQLCipher；用户确认后保存；不保存bearer/UI context/secret |
| Occurrence | plan_id、schedule_epoch、逻辑槽标识、计划UTC时刻、是否已claim/错过及原因 | Desktop投递账本；不声称是Runtime执行结果 |
| ScheduledRun | run_id、触发来源、原run引用、plan快照、稳定operation_id、conversation/task/session/thread/turn关联、投递状态、原生事实引用 | 不复制消息、reasoning、tool正文或Artifact；状态分投递/执行两层 |
| 已有chat outbox | 提交/中断等已有操作和租约 | 继续由唯一Coordinator消费；不复制成第二队列 |
| Attention | run引用、需要处理/完成/失败的安全摘要、去重键、已读 | 应用内通知，通知失败不改变执行终态 |

`plan_id`、`run_id`、`conversation/task_id`、`session_id`、`native_thread_id`、`native_turn_id`、`operation_id`分工独立。每次新聊天分配新conversation/task；专属/已有模式复用同session并产生新turn。禁止拿plan_id重复当Host task_id。

自动唯一键建议为`(owner, tenant, plan_id, schedule_epoch, logical_slot)`，手动/重跑为`(owner, tenant, request_id)`；一次手动网络重试沿用request/operation，用户明确重跑才生成新run。逻辑槽按本地日历时刻与规则版本命名，DST fold不产生第二槽。计划时间编辑只影响保存之后的未来槽，不能通过改revision重复投递已经消费的过去时刻。

### 5.2 三种运行目标与受管目录

推荐在native提供**明确标识的应用受管工作目录引用**：新聊天使用本应用app-data下独立的定时任务工作区，路径由native生成并校验，UI只显示“易界管理的任务目录”，不能任意传入路径。受管引用是新增来源类型，不能伪装成用户选过的bookmark；沿用scope、路径保护和会话记录，批准后由权威契约定义。此为DEC-155-02，不是已存在projectless能力。

| 模式 | 推荐关联 | 目录与失效规则 |
|---|---|---|
| 每次运行时新建聊天 | claim时同事务创建新的本地conversation/task；Host thread创建只发生在实际投递 | 每会话独立受管目录；保留该聊天历史/产物；删除计划不删除这些目录 |
| 此任务的新聊天 | 第一次实际claim原子懒绑定本地conversation/task引用；Host agent_session_id和Runtime thread_id在后续调用确认后填入，以后沿原会话提交新turn | 同专属会话目录；专属会话删除/不可用则暂停并要求重新选择，不偷偷新建替代 |
| 已有聊天 | 保存明确可访问session_id，运行前重新核验原生可继续性、scope和忙碌 | 沿用其原project/bookmark；失效、无权、legacy缺原生证明、删除中或uncertain则拒绝本次，不改投 |

运行目标选择器是“聊天”选择，不恢复项目“+”或高级入口。对话创建过程中首次首页聊天也不能依赖“第一个可用项目”的隐式目录授权；推荐复用同一种受管引用作为该创建对话的明确默认。已有聊天的权限/文件范围不能被新计划自动扩大。

目录生命周期：随关联聊天保留；本期不递归清理用户文件或做后台孤儿目录删除。系统引用从普通用户项目管理中区分呈现，不能被误认为用户主动选取的经营目录；空间增长列限制，清理另行明确授权。此处不改变已有project删除语义。

目录准备与SQLCipher不是同一事务：先以稳定native资源ID幂等准备/验证受管目录，再进入会话/run/outbox组合事务并重验时刻与授权。目录失败不产生可投递outbox；目录已建而DB尚未提交只留下可识别的应用自有资源，不能因此重复发起模型或删除既有用户目录。本文不承诺跨文件系统与数据库原子性。

### 5.3 事务与删除边界

同一repository worker内新增组合事务：重新验证计划revision/scope/target → claim occurrence → 冻结run输入/权限引用 → 创建或绑定本地会话记录 → 生成原有outbox → 前移next occurrence。事务不含Host agent_session_id或Runtime thread_id的创建确认，后者按稳定task/operation关联补录。现有方法各自开事务，需要内部复用事务函数；不能调用两次独立IPC假装原子。

暂停/编辑/删除与claim在同writer串行裁决。尚未开始出站的claim可在本地事务撤销；已进入sending/已受理属于在途运行，暂停仅停后续，UI明确展示。删除在途计划仍阻断。时间修改取消未发出的旧未来槽，不改已发运行快照。

删除计划保留运行历史/聊天的规则延续00；**删除聊天是另一边界**：先停引用该session的计划/未投递outbox，按ADR-0014清理会话和原生映射，定时索引移除可恢复的native ID/正文派生缓存，仅留不含正文的“目标已删除”墓碑。每次新聊天模式不因一个历史聊天删除而禁止未来的新聊天；专属/已有模式需重新绑定。不得靠计划历史恢复被删会话或延长对话正文保留。计划自身用户确认的提示词属于独立可见资源，删除聊天时须披露仍存在的计划，不将其伪称已被一起删除。

## 6. 时间、错过与容量规则

### 6.1 复用成熟时间计算

推荐依赖候选为Rust [`rrule` 0.14.0](https://docs.rs/rrule/0.14.0/rrule/)，用其RRuleSet/Tz计算发生时刻；它提供受限结果查询并依托时区类型。当前仓未安装/锁定该依赖，未做编译/Provider或平台运行验证；须在实施获准后审核依赖树、锁精确版本/校验及TZ数据版本。若候选库无法满足下面的纯时间检查，重新选成熟库，不手写RRULE/DST引擎。

产品只接受结构化的仅一次/每天/周一至周五/每周所选日及分钟时刻，不接受任意RRULE字符串；native构造受限规则，renderer不成为第二时间解释器。仅一次直接保存一个UTC instant；重复计划保存IANA zone、当地时间、起始边界、规则版本以及计算出的next UTC。

预览与实际触发共用同一native evaluator。DST重复时刻只选择较早的UTC instant一次；不存在时刻跳过并保留原因；工作日不是法定节假日日历。不得依赖设备时区变化隐式改保存的IANA zone。依赖/TZ数据升级时按版本重新预览受影响未来槽，并保留已消费槽的唯一键，不重放历史。

采用有界“求下一次”查询，不从创建日期无限展开所有历史；若候选库接口内部仍全量遍历，必须通过源码/定向检查证明容量上限或更换成熟接口。长时间离线记录一个错过区间及下一个未来时刻，不创建海量run或声称知道每个过去时刻的精确失败原因。

### 6.2 真实时钟与missed定义

- 原生等待使用Tokio timer，但到点以当前UTC墙钟、计划revision和权威记录重新判定；单次等待建议不超过30秒，计划编辑/启停、host generation或scope改变立即唤醒重查。
- **正常延迟容忍候选为60秒**：同一连续awake生命周期中，`scheduled_at ≤ now ≤ scheduled_at + 60s`可claim一次。超过窗口记missed_late；不把每次扫描时已经过去几毫秒的任务全部跳过。
- 正常退出后重开、明确sleep→wake、或无法证明连续awake的时钟大幅跳变：对离线区间内已到期槽不补跑，记录missed/offline或clock_discontinuity，再求严格晚于恢复时刻的未来槽。此规则优先于60秒容忍。
- 墙钟回拨不重跑已消费槽；向前跳过多个周期不补跑风暴。保留last observed UTC与单调时间差用于诊断，使用macOS sleep/wake事件协助判定，不能声称单靠tokio/Instant知道每段睡眠原因。
- 仅一次过期且已明确错过，计划可进入已完成并显示“未执行：错过时间”；没有结果的unknown不算成功，也不自动结束为已完成。用户手动执行是新run，不改原触发事实。

以上数值和策略均为本次明确建议，需随DEC-155-03确认；并非从PDF或既有Runtime发现的默认值。

### 6.3 并发、前台与后台

推荐首期**全局最多一个定时run未结束**；同计划、同session继续互斥，waiting approval和unknown占用该调度槽。自动触发遇忙/目标不可用时记录未执行原因，不无限排队；手动触发给出可重试反馈。

仅限制“定时run数量”不足以证明前台+后台多会话流同时可用：现有Coordinator优先取首个active session，需按DEC-155-04冻结互斥或观察方案。最小候选使用同一native派发预约：任何前台运行/待批准/uncertain存在时不开始定时run；定时run在途时，新前台发送保留草稿并提示先等待或在原对话正常取消，不暗中中断。只在定时run占用时收窄交互，不擅自改普通前台会话之间的既有并发规则。该UX收窄须Owner明确接受；若要求自由前台/后台并发，需扩展同一Coordinator多会话公平观察与审批关联，计入新增工作，不能另起第二执行器。

预约判定还必须包括前台queued、本地未派发outbox、会话创建发送中及已受理尚未写回窗口；所有前台create/submit和定时claim使用同一native原子预约，恢复outbox出站前再次校验。不能先检查当前无running，再让既有dispatch tick把已排队的另一会话发出去。只读源码确认当前流内虽会派发其它outbox，却未并行观察其终态（application.rs:2399–2444,2478–2483），因此该门禁不是假定已有能力。

## 7. 投递、重启恢复和“不重复执行”的准确承诺

候选承诺是：**每个已确认逻辑槽/手动请求最多一次自动投递尝试；不确定即保留unknown并停止自动续投。** 不是端到端exactly-once，也不保证每个计划时刻都实际执行。

| 所处边界 | 恢复/操作规则 | 不允许的推断 |
|---|---|---|
| 保存事务尚未提交 | 没有权威计划，原请求ID安全重试 | 不凭UI toast判保存成功 |
| occurrence/run/outbox已提交，证明尚未出站 | 复用同run/operation；重启按错过窗口取消过期自动槽，未来槽保留 | 不生成新ID重放 |
| Host会话创建调用已出站但响应未确认 | 新增只读按既有task_id查询映射；若Host也只有starting/failed则unknown，保留孤立thread可能性 | 不通过列表名字、最新时间或新建另一个thread补齐 |
| turn提交已出站 | 查询Host同scope/session/operation的持久状态；accepted返回原turn；pending/uncertain不重新调用Runtime | 不把HTTP超时当未执行 |
| 有已确认native turn | 沿现有read/resume/原生通知保管状态；冷历史partial保持来源与缺失说明 | 不用正文比对或猜ID补齐 |
| 无法确认旧operation是否执行 | run进入需处理、计划暂停后续触发；保留账本和安全诊断 | 不因Runtime idle/notLoaded或read找不到而清除风险 |
| 明确终态 | 原生事实更新执行结果并释放预约；原生turn与各tool状态分别保留 | 不靠计时器或模型“完成了”裁决业务成功，也不凭单个tool失败把最终run强改failed |

Host已持久pending/accepted/uncertain和输入摘要，但缺公共查询接口。推荐增加只读、scoped、版本化的结果读取：会话创建按既有task_id读取映射，turn投递按session/operation_id读取；包含Host instance/epoch、是否映射完整和稳定错误，不暴露提示词或允许查询别人的ID。现有StartSession没有创建operation_id，本稿不虚构该字段；若以后引入，必须同时扩展创建写入契约与持久关联，不能只加查询。查询只能呈现已知事实，不能凭恢复需求自动把uncertain改accepted。旧接口保持现有幂等解释，不增加自动重发语义。

运行结果呈现原生turn结果，并保留失败/未完成tool的可见事实；“turn completed”不自动等于用户业务目标成功，单个失败tool也不自动决定整次run失败。首期不增加业务成功分类器；详情说明结果来源，由用户查看完整对话评估业务结论。

unknown的解除分为执行预约和历史结果两件事。只有原生终态、正常中断确认，或旧受管Host/Runtime generation已经正常关闭且新generation的当前执行/待审批门禁通过，才允许释放执行预约；用户确认本身不能证明旧运行已停。历史结果仍可保留unknown，用户在阅读已知对话和重复效果风险后可确认恢复未来计划或新建手动run；确认不改写旧事实为PASS。只改enabled而未满足执行门禁时，UI仍显示需处理且禁止投递。

新App生命周期先完成single-instance/native identity/DB/Host readiness与未决操作恢复，再启动计划扫描。计划的enabled状态可恢复，但未完成恢复的计划留需处理；不复制Runtime历史重建一套执行状态机。

## 8. 授权、审批、费用与生命周期

### 8.1 两种授权不能混用

- UI管理命令仍用既有短期WebView context；定时触发使用新建的native-only scoped调用入口，从当前authority取得owner/tenant/revision并校验计划、能力和目标。每次claim及出站前复核，不落盘bearer或复用过期UI context，不绕过AuthorizedConversationApplication直调DB写入口。
- `schedule.read`保持只读；候选能力为独立的读取、管理及运行三类，由Contracts定义，不把字符串写进native local profile就当业务授权已经完成。public/production仍不启用本地调度例外。
- 首期自动计划推荐固定Ask；新会话从Ask开始，已有会话若当前为Auto/Full则显示不满足自动运行条件，由用户在既有入口主动改回或改目标。调度器不切换会话模式，不把旧Full确认当未来所有自动run批准。支持其它自动模式须另行明确批准和风险界定。
- 保存计划只授权按显示时间/内容/目录启动任务；原生命令/文件/MCP批准仍逐请求处理。新增native只读观察未结束run的pending审批并发needs_attention，用户进入完整对话走现有批准/拒绝。请求过期、进程重启、写回失败保持真实unavailable，不保存旧批准回调继续执行。

### 8.2 成本与外部副作用

本轮所有产品调用预算仍为0。未来启用自动运行必须有明确作用于该计划或该次验收的预算/期限；没有预算则阻断执行。每个逻辑run在出站前原子占用一次额度；unknown不退还，重复网络请求不重复扣同逻辑run；手动重跑新增扣账。

逻辑run上限不等于模型HTTP次数、工具费用或金额硬上限：Runtime/Provider可能有内部重试，不能把run计数伪称账单精确控制。首期只允许已批准的有限次、有限期限合成/公开只读验证；若要求长期无人值守费用硬限或真实商家写入，另行补provider/工具预算与权限治理。创建对话自身也消耗模型额度，不与计划执行预算混账。

### 8.3 正常停止与保持系统唤醒

必须在可取消的退出请求阶段（ExitRequested或等价受管入口）先接管退出，不能等到现有不可逆RunEvent::Exit才开始保证恢复。拟顺序：拦截退出并关闭新claim/提交预约 → 持久化当前投递事实并停止唯一Coordinator新派发 → 释放awake assertion/平台观察 → 正常停止受管Host/Runtime → 成功后允许最终Exit并关闭DB。任何一步结果不明进入STOP_PENDING，保留原生进程及安全提示/恢复入口，不进入最终退出、不强杀、不删库、不替换二进制；既有某些sidecar配置的forceful fallback不得成为本功能有效退出路径。

已只读核对缓存的Tauri2.11.5 `src/app.rs:81–94,225`存在ExitRequested/prevent_exit，来源hash见审计JSON；restart特殊退出码不能依赖该拦截，未来更新/重启必须先完成同一正常停止流程。本轮未调用退出/重启或编译依赖。

窗口隐藏/最小化可不依赖页面显示，但“关闭最后窗口后仍运行”当前无产品承诺；文案以App仍运行且native服务ready为准，不新增托盘保活、LaunchAgent或开机自启。

macOS保持唤醒采用平台受管assertion，默认关闭，每次App重开关闭；只防止App存活期间的自动空闲休眠，关掉或退出释放，不修改系统永久电源设置。[Apple QA1340](https://developer.apple.com/library/archive/qa/qa1340/_index.html)明确区分idle与用户手动/合盖等睡眠，并给出IOPM assertion创建/释放及sleep/wake通知。它不能承诺唤醒关机设备或阻止手动睡眠；本文方案也不这样承诺。该文档是官方归档资料，实际打包/目标系统验证仍未执行。

## 9. 通过对话创建：最小原生复用方案

推荐流程：预填首页 → 用户发送 → 既有Codex对话在受限计划草案模式下使用stable outputSchema → native严格校验 → 展示草案/缺参问题 → 用户确认 → 与手动表单调用同一保存事务。

- schema由Contracts冻结，Host只接受受管schema ID/版本，不能让renderer注入任意schema/config。输出仅允许“需澄清”或“候选计划”；时间和目标必须经native校验/用户选择，模型不能提供scope、批准或受管目录原始路径。
- 复用普通thread/turn及现有内容保管。计划草案卡片作为对该次真实结果的独立产品投影，不重写native消息、不伪造assistant执行item；绑定来源session/turn及草案revision，重复确认同一草案最多保存一次。
- 多轮澄清与手动调整都只修改草案。目标选择必须解析为可访问的稳定ID；在保存前展示名称、提示词、频率/时区、下一次、运行于、工作目录说明、Ask和预算意图。
- Host普通turn目前没透传outputSchema，须先扩展受限契约和adapter。标题模块是可参考实现；其effort=none与当前high/raw模型路径不同，真实计划schema合规率未验证。无效/partial结果明确“未创建”，保留聊天及可手动修正表单，禁止解析任意自然语言后自动保存。
- 若Provider能力验证不通过，保留手动创建可用只能算降级，不能将AC-002判PASS；必须调整需求或更换经批准的方案。新增experimental dynamic tool/新MCP server是更大备选，不是本稿默认路径。

## 10. Q-02～Q-04 的收敛建议与范围代价

| 事项 | 当前证实程度 | 推荐取舍 | 新增工作/限制 |
|---|---|---|---|
| Q-02 三种运行于 | 现有create/enqueue/read/resume可复用，无projectless/原子计划绑定 | 保留三模式；默认计划专属聊天；新聊用明确受管目录，已有聊沿原目录 | 数据关联、lazy bind、删除失效、模式/工作目录提示均必做，不能只换label |
| 重跑 | 原生可产生新turn，不能复活旧run | 使用当前已保存配置，确认与历史差异，产生新run | 独立计费/审批/幂等；旧计划删掉后不重跑 |
| Q-03 四状态 | 仅PDF产品标签，没有现成schedule enum | 筛计划当前生命周期；run结果另列。一次计划终态/明确错过且无未来槽才已完成；unknown暂停需处理 | 删除计划历史保留于全部状态；原生tool失败不可被“已完成”覆盖 |
| Q-04 保持唤醒 | 平台可支持，当前未接线 | macOS首期保留，默认关闭，作用域仅本App生命周期 | 新IOPM封装、恢复事件、错误/释放与正常睡眠验证 |
| 重要更新应用内通知 | NNotificationProvider存在但无业务接线 | 必须接通持久needs_attention/完成/失败与运行跳转；去重 | 不依赖打开某聊天才能发现审批；不把任意模型文本当重要性判定 |
| macOS系统通知 | Tauri官方插件有Rust入口和权限流程，当前未集成 | 建议首期延期，只承诺应用内重要更新；若Owner要求同步交付，独立补范围 | 插件精确版本、权限拒绝降级、打包应用、点击路由与锁屏隐私验证；拒绝权限不阻止任务 |

[Tauri通知官方文档](https://v2.tauri.app/plugin/notification/)证明插件需安装、初始化并检查/请求权限，不证明当前易界已实现；不开放完整默认通知能力给所有WebView。系统通知延期是待批准范围建议，PDF图4未指定通知介质，D0需明确最终文案。

### 10.1 代价估算与16小时边界

以下是基于源码缺口的初步工作量区间，不是已用工时或交付承诺；不计等待Owner/外部预算的时间。

| 工作 | 估算 |
|---|---:|
| Source-first边界、计划/run同库事务、managed workspace与迁移/回退 | 5–8小时 |
| 原生生命周期、授权/预算、Host恢复查询、并发预约 | 5–8小时 |
| 对话草案、三模式、管理页/历史/详情与统一UI | 6–10小时 |
| macOS唤醒/应用内通知、正常focused与fresh验收修复 | 4–6小时 |
| 合计（系统通知延期） | **20–32小时** |
| 若新增系统通知 | 另约2–4小时，取决于打包/权限反馈 |

完整PDF候选不能负责任地承诺12/16小时内闭环。**不修改现有timebox、不把20–32小时当自动延长授权。** 推荐先确认本技术方向，再由Owner选择：

- 保持当前完整范围：在进入实施前明确重定交付范围/时间约束，必要时按治理拆为独立用户结果的需求；当前不创建新编号、不自动切换Profile或加大时间盒。
- 严守单个12–16小时：可候选缩为“手动配置、每天/每周、每次新聊天、记录/完整对话、应用内提示”；对话创建、专属/已有聊天、保持唤醒等移入明确后续需求。这会改变AC-002/004/010和PDF图示，必须显式批准，当前不删任何Must；权限、持久化、幂等与真实运行不可裁剪。

本轮推荐保留完整设计便于判断，同时将**范围与时间盒不匹配**列为D0阻断，避免实现中途才发现必须削减主流程。

## 11. 契约、迁移与回退的具体边界

### 11.1 拟新增边界清单

| 边界 | 权威与producer/consumer | 必须冻结的语义 |
|---|---|---|
| 页面↔native计划/记录/预览/确认 | Desktop-owned私有typed IPC封套/投影组合Contracts共享领域类型；Desktop native provider、Vue consumer | scope、revision、target/workspace来源、状态分层、分页/时间、幂等、确认与稳定错误 |
| 计划草案模式/结果 | 固定Runtime outputSchema；易界受管schema及Host投影归Contracts | schema ID/version、clarify/proposal、来源turn、无保存副作用、严格拒绝无效结果 |
| native↔Host创建/turn结果只读查询 | 易界Host HTTP/shared schema；Host provider、Desktop consumer | operation/task/session查询授权、known/unknown/instance、原生关联和错误，不重发 |
| native调度授权/权限 | 易界能力与调用context源；native authority/Host消费者 | read/manage/run分离、Ask基线、fresh revision、expiry、拒绝语义 |
| SQLCipher新表/约束 | Desktop migration source私有 | scoped唯一键、plan/run/outbox原子性、版本/checksum、删除边界、旧数据可读 |
| app/native lifecycle | Desktop自身与Host受管生命周期契约 | 单一owner、关闭顺序、STOP_PENDING、无强杀、平台能力失败 |

2026-09-18在21规划时明确既有分层：Desktop私有封套/UI投影沿用[FEAT-126已接受IPC权威](../FEAT-126-public-task-authorization-hardening/04-contract-change-plan.md)，共享计划/执行payload及Host边界仍归Contracts。这不是新的免审例外；跨进程仍做影响分类、唯一源、同源生成与兼容校验。若出现兄弟仓消费者，先回共享源治理。

不新增公共API scheduler、队列topic、数据库服务或Runtime方法；不手写公共DTO，不绕开生成/同源conformance。native进程内领域类型不强塞公共Contracts，跨版本IPC/跨仓payload则按源治理。

### 11.2 breaking风险已得到具体解释

当前SQLCipher latest=15，`migrations.rs:124–127`对高于支持版本的DB fail closed。若计划表进入同库新migration（示意v16，实际编号以实施时catalog为准），旧binary会拒绝整个Chat库，**新增表并不代表旧版可回退**。受管workspace来源、新IPC变体/能力也可能被严格旧consumer拒绝。因此本Feature维持breaking审查，当前文档变更仍none。

建议先形成能读新增格式但不启用调度的兼容reader/回退候选，再启用writer；回退是停止新claim/功能并使用兼容reader，不对用户库执行down migration、删表、复制恢复或重置。不改旧migration/checksum，不先在日常用户DB上试错；source-first后先安全合成数据正常前向验证。若涉及重要用户数据或不可逆迁移，按项目升级条件进入production_hardened或独立明确治理，不能仅凭local标签批准。

未来顺序：Proposed决策获批与D0 → Contracts权威源/固定Runtime投影核对 → 兼容reader与Host只读恢复/草案支持 → native计划与UI → 默认关闭的能力检查 → 获准的真实验收。每步是依赖顺序，不建生产治理切片，不提前生成实际契约。

## 12. 决策清单与后续验证条件

| DEC | 需要Owner确认的实质决定 | 本稿推荐 |
|---|---|---|
| DEC-155-01 | 计划数据与触发职责 | Desktop native+现有SQLCipher，Host薄适配，Runtime固定 |
| DEC-155-02 | 无项目UI下的执行目录 | 明确的native受管workspace来源，新聊天默认受管目录，已有聊天沿原引用 |
| DEC-155-03 | 时间库/错过/时区策略 | rrule0.14.0候选、有限规则；60秒正常延迟窗口，sleep/退出不补跑，DST重复一次/缺失跳过 |
| DEC-155-04 | 并发、unknown和前台交互 | 全局1个定时run，明确前后台预约；unknown不自动重投，需处理后恢复未来 |
| DEC-155-05 | 自动授权、审批与成本 | native fresh授权、首期Ask、按计划有限预算、不代答批准 |
| DEC-155-06 | 对话创建机制 | stable outputSchema草案→用户确认→同源保存，不增加实验tool服务 |
| DEC-155-07 | native平台能力 | 保留macOS生命周期内防空闲睡眠；应用内重要更新，系统通知首期延期建议 |
| DEC-155-08 | 持久化和回退 | 同库原子扩展、兼容reader先行、forward repair；不回退旧binary写高版本库 |

当前状态：这些推荐已足够形成可审阅决策，**不再把Q-01笼统写成“尚不知放在哪里”**；尚缺的是Owner对新增职责/约束的选择，而不是本轮应继续无限搜索。Q-02—Q-04已有对应候选，仍保留pending直到明确确认；D0还需处理20–32小时与16小时上限的范围冲突。

实施后的必要验证（本轮全部NOT RUN）：成熟时间库纯数据DST/时区/边界用例；原子claim/operation相同及冲突；同目标/前后台预约；正常退出重开与Host实例改变；真实Provider草案合规与无效拒绝；原生批准/拒绝；受管目录与删除边界；正常sleep/wake及assertion释放；兼容reader/合成数据前向迁移；一次真实未来时刻触发并覆盖全部Must。只用正常、安全流程，不注入攻击资源、破坏权限、强杀或伪装二进制。

**本轮完成定义：只读证据、唯一推荐方案、范围代价、Proposed ADR及需求状态同步。功能和兼容性验收仍未执行，不能把该定义替换为D0/D4通过。**
