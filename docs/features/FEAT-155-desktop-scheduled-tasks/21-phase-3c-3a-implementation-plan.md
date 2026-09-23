# FEAT-155 下一步执行方案：3C-3A 原生管理查询、确认边界与最小 typed IPC

实施接续：用户随后明确授权本方案，本批已完成并停止，实际结果与限制见[22报告](22-phase-3c-3a-implementation-report.md)。以下保留授权前方案记录。

2026-09-18。用户要求“给出下一步执行方案”。本轮仅只读调查、保存方案与需求包校验，不开始实现。起点是[20：3C-2实施报告](20-phase-3c-2-implementation-report.md)；原产品目标和授权仍以[00](00-feature-brief.md)、[04](04-owner-approval-and-implementation.md)和[ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)为准。

## 1. 建议下一次只实施3C-3A

**先把现有候选能力整理成页面可安全调用的原生查询和明确确认接口，完成零真实调用验证后停止。** 3C-3分为A、B两批：本批A为管理/查询/typed IPC，后续B再接固定outputSchema草案及确认保存来源。第四阶段仍负责页面、交互、重要更新显示、防空闲睡眠与真实激活/验收。

这是原3C-3工作内的顺序拆分，不增加功能，也不缩减两种创建、三种运行于或本机唤醒目标。没有把下一步方案请求当实施授权。

| 可选下一步 | 取舍 |
|---|---|
| 草案与全部IPC同批 | 同时触及Host用途/权限约束、草案完整性与Desktop管理边界；当前存在独立缺口，审查和定位成本较高 |
| **先管理查询与确认IPC，再草案** | 复用已完成的本地事务，先闭合页面/后续草案共同需要的保存、时间与目标边界；本批不用改Host或Runtime，推荐 |
| 直接页面/日常激活 | 尚缺有界历史查询、操作授权适配和原生删除阻断；不具备进入条件 |

本轮文档`contract-impact=none`，无运行行为变化。未来A批按**semantic**管理新增Desktop私有跨进程封套/投影及既有原生管理语义修正，完整FEAT-155仍保持breaking；若实施确需改变受支持的闭合共享字段/枚举、旧请求解释或SQL格式，必须先升级本批影响分类和兼容方案，不能暗中加入迁移。

**本批推荐不新增SQL schema22。** 21已具备plan/hold/run/occurrence/关联事实；新增IPC schema版本不等于数据库版本。普通入口继续schema15、默认禁发；候选21 writer及发送授权仍只能由显式native构造取得，IPC不能迁移或激活。真实平台/Provider资格NOT RUN，全部Must pending、D4 NOT RUN。

## 2. 已核实的事实与前置缺口

[20的来源证据](evidence/phase-3c-2-source-20260918.json)102份业务候选摘要逐项吻合，五仓HEAD/branch/remote与已有dirty条目数保持，Runtime clean。20中的74项专项、19项旧回归和收尾17项是上批结果，本轮没有重跑产品测试。两项只读技术复核分别检查IPC/管理边界与草案依赖，不是独立人工批准。

下列Desktop路径相对`yijie-desktop/`，行号为当前候选：

| 现有事实 | 本批处理 |
|---|---|
| `src-tauri/src/chat/schedules/execution.rs:476–577`已有管理与单条读取；`store.rs:293`列表无分页并排除删除计划 | 增加有界产品查询投影，不直接把内部方法当页面API |
| `execution/preparation.rs:327–345`的manual仅有native授权；读取/重跑预览也没有UI context | 所有renderer调用加当前context和fresh native权限；写入在worker提交处重验 |
| `store.rs:314–360`删除分支无在途run/审批/未释放unknown阻断 | **先补同事务原生删除保护，再暴露命令**；只在UI禁用不合格 |
| `execution.rs:579–599`的check_run最终固定ExecutionNotReady | 不作为新可用性接口或成功预检的来源 |
| `0018_scheduled_local_preparation.sql:45–53`已有真实聊天/local turn关联；`0021_scheduled_triggers.sql:7–19`含无run槽事实 | 查询真实关联及分型历史，不造run、不复制完整对话 |
| `execution/triggers.rs:329–379`已有启用和独立重跑；21已有future_hold | 复用其确认/幂等，明确区分保存、确认grant、启用和执行 |
| `application.rs:2471–2483`、`schedules/recovery.rs:230–233`只持久化needs_attention | 没有新鲜审批来源时只显示需处理/未知，不能据布尔值断言“等待批准” |
| `0017_scheduled_execution_foundation.sql:22–53`无真实起止；NativeTurn无起止，NativeItem.durationMs属单项 | 缺失时间返回明确可用性，不从UUID、消息时间、工具耗时推造运行时间 |
| `docs/chat-native-conversation.md:5`、`scripts/generate-native-conversation.mjs:9–73`已有共享源+Desktop私有IPC组合生成 | 复用权威分层和同源检查，不手写影子PlanDefinition/RunView |

本批支撑AC-003～009的管理、确认、筛选与关联，也给AC-002后续草案提供同一保存边界；不把这些Must提前标PASS。

## 3. 按顺序实施

### 第一步：最小IPC权威与操作语义

共享计划、执行、时间、目标和错误仍以Contracts既有源/生成物为准。新增只由同一Desktop版本消费的命令封套、查询投影和私有错误，建议以`src-tauri/schemas/scheduled-task-ipc-v1.schema.json`为唯一私有源，组合已固定摘要的共享schema，生成Rust/TypeScript与严格validator。此分层已有已接受依据：[DEC-126-029/031](../FEAT-126-public-task-authorization-hardening/03-decisions-and-risks.md)及[FEAT-126私有IPC权威与增量规则](../FEAT-126-public-task-authorization-hardening/04-contract-change-plan.md)。本批沿用该既有Desktop-owned private IPC边界，**不是免除跨进程契约审查**；一旦增加Host/兄弟仓消费或更改共享领域语义，先回Contracts权威源，按provider/consumer方向生成同步。

先冻结版本、request/context ID、分页/筛选、可选值/unknown、幂等、revision和错误，再实现consumer。只定义下表确实消费的能力，不预铺草案或任意操作dispatcher：

| 组别 | 最小范围 |
|---|---|
| 可用性/计划 | 可读取、候选可写与发送未激活的分项资格；有界计划列表/详情，历史所需的删除计划身份 |
| 时间/目标 | native时间预览；有界可访问聊天列表/搜索、明确ID和安全目录来源说明 |
| 历史/详情 | 按计划ID与当前计划状态的分页记录；run与未执行occurrence严格分型；真实聊天/local turn关联和可跳转性 |
| 管理 | 保存/编辑、暂停、删除；request ID/revision与明确错误 |
| 确认/执行 | 有限grant确认、确认并启用、显式manual、rerun预览/明确确认；复用原回执和事务 |

读取不可用不得伪装成“没有计划/记录”。字段/版本/枚举未知明确拒绝或返回声明的不可用结果，不吞掉错误。仍不增加自动tick、强制解锁、独立审批、任意目录准备、SQL/schema/config透传等IPC。

### 第二步：补齐原生管理与UI确认边界

- 每个查询和命令验证当前UI context、native scope及对应read/manage/run能力；context不能替代native权限，renderer不能提供owner/tenant/native authority。
- 管理和显式运行在worker实际提交时再次验证context；不能把现有native-only `prepare_manual`直接注册。查询完成投影前也检查scope/context仍有效，防止账户/context切换后的旧结果被送回新界面。
- 删除与占用检查必须在**同一个worker事务**内按当前plan的未释放run/预约/原出站事实裁决。排队、创建中、待审批和未释放unknown均阻断；可信终态/正常停止已释放的旧unknown不永久阻止删除，也不能因别的plan忙而拒绝删除当前无在途plan。
- 删除不强制取消、清预约、退款或改旧终态；成功只停止未来计划并保留历史/对话。暂停/编辑仍阻止未开始I/O，不强行中断已提交turn。
- Busy使用明确内部错误/现有Execution `ReservationBusy`适配；原PlanError没有Busy时，先明确旧入口到既有`ExecutionNotReady`和新IPC到busy的映射，所有入口复用同一受保护事务，不能漏出无保护旧入口或用StorageUnavailable掩盖业务阻断。
- 保存保持paused；grant-only不启用；启用不生成run/占额；手动/重跑成功回执只表示原本地组合事务已接受。有限确认仍绑定当前定义、目标、次数和期限，重复请求不扣额、不改旧历史。

### 第三步：有界只读投影与时间/目标预览

1. 列表采用固定上限和稳定游标（建议默认20、最大100），由native校验过滤和排序；游标绑定scope/context及查询参数，旧游标失效可明确重查，不允许任意SQL/排序表达式。读查询不依赖Host/Runtime ready，也不触发恢复POST或写状态。
2. 四个产品筛选仍为全部状态、已开启、已暂停、已完成，按已批准的**计划当前生命周期**过滤；删除计划只在全部状态出现。raw state与future_hold/授权失效分开保留。投影优先级固定：Deleted只进全部历史；Completed优先于残留hold；原Paused保持Paused；仅原Enabled因hold或当前授权不足以新建未来run时投影为已暂停并附原因，否则已开启。once完成可能保留budget hold，不能因此错归已暂停。最后一次已预扣run的发送资格与结果始终独立，不能误标“未执行”；不因查询更新持久状态。
3. 历史严格区分运行与未执行槽：busy/missed/offline等没有run时不得创建或虚构run ID/聊天/扣额；已关联run的槽只投影一条记录并附其处置，避免重复列出。尚未到点的planned槽不是执行记录。暂停预览取消不冒充已经执行或业务失败。
4. 查询按真实关联返回conversation/local turn和available/deleted/unavailable原因；打开时仍须现有聊天scope校验。关联被删后仅墓碑，不泄露旧native ID/正文，不跳到其它聊天，不从计划快照重建对话。
5. 时间来源明确：scheduled_at是计划时刻；真实起止/耗时缺失返回unknown/not_started及来源，不能把0当unknown、把消息创建/UUID/终态观察时间或单个工具耗时称为整次执行耗时。这个缺口继续列为最终页面/真实验收前事项，未删除PDF字段要求；先确定可信来源，再决定是否需要后续最小存储扩展。
6. needs_attention只表示需处理；waiting_approval必须有对应会话/turn且有来源和时效的现有审批证据。本批列表不为此强制逐项查询Host，不新增审批状态机。native completed不自动声明商家业务成功，partial/unknown保留。
7. 时间预览只接结构化规则，当前时间取native，复用既有evaluator；不接受renderer的可信now/next_at或任意RRULE。目标列表返回真实可访问ID和用于消歧的安全名称/更新时间，模型标签不能自动选中重名/最近聊天；目录只显示来源说明，不暴露路径/bookmark。区分“可保存目标”和“此刻可启用/运行”，提交时重验，预览不发长期授权。

### 第四步：注册最小typed command与client

按源schema生成/校验后接薄Rust command和typed TS client，复用现有context、错误、请求身份和主应用IPC边界；不提前写页面/store流程或增加临时调试页面。内部进程代次、连续性ticket、Host token、目录路径、原始SQL/Runtime wire不能出现在renderer输入中。

普通`ChatRuntime::database()`及`DatabaseWorker::start`保持原构造：新库和15库不升级，已有21 CompatibleReader不因IPC获得writer/发送权。只读或未激活返回明确状态；command调用本身不能选择候选构造、启动Host或解除发送门禁。

本批以权威查询与命令回执闭环；若需要native变更事件，仅在当前授权context内于提交后发送不含正文的失效提示，丢失/重复后重查。现有`schedule_changed`只是Coordinator唤醒，不当作UI通知。完整重要更新、通知显示/跳转与订阅产品交互留第四阶段，不建立持久通知队列或通用事件平台。

### 第五步：安全验证、报告并停止

| 检查 | 完成标准 |
|---|---|
| 来源与兼容 | 私有源/共享引用/生成Rust/TS/validator和实际native producer一致；未知字段/格式有明确结果；未改旧共享形状时不伪造Contracts新版本 |
| 授权 | 过期、重绑定、scope不符在查询与提交处拒绝；manual不绕UI确认；不可提交native ticket/路径/任意配置 |
| 删除/确认 | 当前plan在途/审批/unknown拒绝删除；可信释放后允许且保留历史；保存/grant/enable/run各自语义、幂等及revision一致 |
| 查询 | 有界分页/稳定排序、同名按ID、删除历史及四状态优先级（含Completed残留hold和最后预扣run）；无run槽不造run，未知时间/审批不造事实 |
| 关联 | 正确本地conversation/turn；删除或权限变化后不可跳转，不恢复正文 |
| 默认关闭 | 普通15不迁移；21兼容reader不写/不发；调用新IPC不激活候选或启动服务 |
| 回归 | 前序自动/手动/重跑、额度、时间、恢复/审批/占用、旧聊天与删除路径保持；必要fmt/clippy、TS lint/build/docs及元仓门禁通过 |

只使用正常临时SQLCipher、原生handler/worker与进程内安全测试；不改日常库/Keychain、不启动真实App/Host/Runtime/Provider，不调用模型。先审查测试行为，跳过用户禁止的强杀、权限故障、攻击fixture与二进制替换。实际失败/修正及未执行项如实记录，不能把合成检查当D4。完成本批报告后停止，不自动进入3C-3B或第四阶段。

## 4. 后续草案批次的已知依赖

3C-3B继续原DEC-155-06，而不是取消对话创建。它将复用A的PlanDefinition、保存、native时间预览及用户明确目标选择；A不提前增加draft ID、source-turn账本、JSON提取、outputSchema透传或草案确认占位接口。

已证实Contracts `jsonschema/scheduled-tasks/plan-draft-v1.schema.json`有封闭clarification/candidate；固定Runtime `app-server-protocol/src/protocol/v2/turn.rs:140–143`支持outputSchema，但Host `internal/codex/session_protocol.go:752–779`尚无传递。Host Ask当前是on-request/workspaceWrite（`runtime_permissions.go:36–45`），**outputSchema只限制最终输出，不等于限制工具或保证只生成草案**。草案批次需先核对受管模式的实际权限/工具、start/resume/turn一致性和普通路由是否可绕过，不升级Runtime或建立Provider旁路来补缺口。

最终草案也不能依赖整个NativeView的available/itemsComplete=true：现有冷历史/视图可能partial。须按精确session/turn、完整且未截断的最终item及可信turn终态定义确认资格；delta、任意自然语言“已创建”、无来源/多final/失败输出都不能保存。B的来源唯一确认与原保存事务再单独落设计；计划保存、有限授权与启用继续分开。真实Provider结构化输出资格留正常产品入口和请求级预算具备时验证。

## 5. 范围与停点

A批实际实现仓推荐仅Desktop与元仓。Contracts源保持只读复用；确有共享域变更才按source-first单独落最小改动。Host/Runtime/API/Infra不改，不加依赖/plugin/CSP、通用调度器或新模型通道。

本批预算仍为零真实文本，累计**0/12**，图片/商家0；不迁移日常库、不提交推送发布。系统通知延期、超过16小时许可和原完整产品目标保持。真实平台/Provider及D4仍NOT RUN。

本轮交付仅本方案和需求记录。下一次若按此实施，完成3C-3A后报告停止；3C-3B与第四阶段均未开始。

最终方案复核已收口两项：私有IPC明确引用FEAT-126已接受权威，并同步00/03及机器状态；有效状态按Deleted/Completed/Paused优先，只有原Enabled的未来触发限制映射暂停，最后预扣run独立。两项只读复核确认无剩余方案阻断，不是独立人工批准。

本轮strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及113处变更文档链接/空白检查实际PASS。102份业务候选摘要、五仓HEAD/branch/remote与已有dirty条目数保持；仅修改8份元仓需求文档，未实现、生成、运行产品测试或使用真实调用。
