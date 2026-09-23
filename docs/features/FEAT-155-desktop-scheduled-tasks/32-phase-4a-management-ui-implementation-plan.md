# FEAT-155 · 下一步执行方案：4A 管理页面与手动保存闭环

2026-09-19。用户本轮要求“给出下一步执行方案”。**建议下一次只实施4A：管理页面、手动创建/编辑暂停计划及只读记录展示，同时补齐页面必需的最小查询与授权前提。** 本轮仅只读调查、方案审查和文档更新，不开始实现或真实调用。

起点为[31：3C-3B3B交付](31-phase-3c-3b-3b-implementation-report.md)。Runtime资格阻塞已解决，原生候选装配和草案恢复已接通；现在缺少可供用户操作的管理入口。4A完成后报告停止。对话创建完整接线、执行启用/手动/重跑、真实Provider资格、防空闲睡眠和应用内重要更新仍按后续批次完成，不削减原十项Must，不把本批当整项FEAT-155或D4完成。

## 1. 决策与范围

选择管理页和手动保存，是因为现有同库计划、时间计算、目标查询、保存/编辑/暂停/删除及typed IPC已经可复用，能够先交付“进入页面→填写→保存→正常重开看到同一计划”的真实用户结果。先只验证Provider不能补上产品入口；一次铺开全部页面、草案发送、执行激活和电源能力又会混合多个未验证边界。

4A包含：原位导航和路由、两Tab、计划卡片、名称/内容搜索及分页排序、手动表单与三类目标、原生时间预览、保存/编辑/暂停/安全删除、记录只读列表和筛选、原请求回执查询，以及必要的共享授权取得和最小创建时间存储。页面与本地native真实读写接通，不能使用占位client或假成功。

4A不接：对话预填/受限草案发送/确认UI、开启计划、确认运行额度、立即执行、重新执行、自动调度激活、完整对话turn定位、唤醒开关、通知分发、真实Provider调用、日常库迁移及Git发布操作。相关按钮保留阶段不可用状态和面向用户的原因，不调用对应写命令；不画假开关。缺少完整详情/运行功能的AC不标PASS。既有12次文本总额度保持，本批计划使用0次。

## 2. 源码事实与必要修正

| 已核实事实 | 对4A的影响与处理 |
|---|---|
| `src/navigation/app-nav.ts:72`定时项仍disabled，`src/router/index.ts`没有对应路由，业务页面未消费scheduled client | 启用原位置的`/scheduled-tasks`入口并复用现有权限路由，不新增第二套应用或展示专用后端 |
| `schedules/ipc/query.rs:99–116`默认按名称排序且只搜名称；PlanSummary无内容、规则、创建时间 | 最小新增卡片读投影，一页一次native请求，原生做名称/内容搜索和稳定有界分页；不逐卡发详情请求或拉全量到前端排序 |
| `migrations/chat/0016_scheduled_plan_foundation.sql:5–43`没有created_at；`store.rs:523–533`更改规则会改变effective_from | 候选SQL23只补计划真实创建时间；旧行未知，不用effective_from/cursor_at、UUID时间或迁移时间回填 |
| `query.rs:223–234`的record.plan取当前计划，只有detail读取运行snapshot；RecordQuery无search | 历史新读投影从run.snapshot_json取旧名称/内容搜索；当前计划只用于生命周期筛选。未执行槽不冒充具有运行快照 |
| 当前Timing仅unknown/not_started；持久native facts没有完整执行开始时钟 | 本批如实显示“时间未知/未开始”，不推算执行时长；不为了列表展示扩大为执行时钟账本 |
| `chat_bind_context_v1`在返回context前启动Host/恢复会话；`authorization.rs:279`每次bind清旧context | 管理授权取得与聊天执行准备分开，仍用同一NativeAuth/AuthorizationManager和App级context；不能让管理页独立bind撤销聊天，也不能以Host ready作为管理数据可读条件 |
| native生成plan_id；save/pause/delete均写`chat_scheduled_requests`，现有IPC没有按request_id只读回查 | 增加仅覆盖这三类管理写入的scoped回执查询；不扩为grant/draft/run通用回执系统 |
| `worker.rs:291`统一候选未安装manual/automatic authority，分操作capabilities已存在 | 页面逐项使用read/save/manual/automatic/draft资格，保存后真实显示暂停，不将writable或草案ready当作任务可运行 |
| `targets`会返回草案行，但can_save=false；普通目标可能可保存却执行blocked | 草案不可作为“已有聊天”选择；普通受阻目标可以保存暂停配置，但显示阻断原因，不假称可执行 |

本轮文档 `contract-impact=none`。未来4A整体按 **breaking** 保守评审，主要因为候选SQL23对旧binary的可读边界及授权启动语义变化；新增只读命令分别是additive。不得以“只是页面”忽略持久化和跨进程影响。

## 3. 推荐实施顺序

| 顺序 | 实施内容 | 完成标准 |
|---|---|---|
| 1 | 最小查询/回执及共享context设计，源先生成 | 保留21个旧命令的严格响应；新卡片、历史行、管理回执投影同源；管理取得授权不依赖Host就绪，聊天授权不互相失效 |
| 2 | SQL23兼容reader先行，再接候选writer | 1—22迁移不改；临时22→23、重开与旧聊天检查通过；新计划记录真实created_at、旧计划保持NULL；普通目标仍15，Host仍5/候选6 |
| 3 | 导航、路由、两Tab及页面权限/状态 | 原位菜单和深链受schedule.read保护；共享context有效；加载、空态、错误、只读/未开放均可恢复；普通入口不自动迁移 |
| 4 | 手动创建/编辑与卡片管理 | 四频率/时区沿native预览，三目标正确选择；唯一保存paused计划，重开一致；编辑校验revision，暂停/删除沿原事务保护 |
| 5 | 记录只读列表与写回执恢复 | 四个批准状态按计划生命周期过滤，历史任务含删除墓碑；旧run按快照搜索，未知事实明确未知；不确定写入按原request查证，不自动重发 |
| 6 | 定向检查、真实候选UI正常重开、审查与报告 | 亮/暗/最小窗口/键盘及旧聊天导航通过；模型、draft/manual/automatic发送计数0；报告后停止 |

### 3.1 最小私有契约

权威仍为Desktop `src-tauri/schemas/scheduled-task-ipc-v1.schema.json`及现有generator；共享PlanView、PlanSummary、TimeRule、RecordView、错误枚举按原来源复用，不复制影子DTO。不修改Host wire、Runtime协议或outputSchema。

推荐增加三个局部只读命令，命名可在source评审时按现有风格最终固定：

- 计划卡片查询：现有PlanSummary＋有界content_preview＋共享TimeRule＋可选created_at/明确unknown语义及目标显示所需的scoped引用。完整内容仅编辑时取既有detail。默认created_desc，可选created_asc；同一时间按plan_id稳定排序，未知创建时间始终尾排。
- 历史行查询：复用RecordView，附运行快照名称/内容预览及来源标记；运行搜索以原snapshot为准。未执行occurrence只显示已有计划引用和槽位事实，明确无执行快照，不凭当前配置伪造过去执行。手动旧记录没有可信时钟时稳定尾排，不能把`scheduled_at=-1`变成展示时间。
- 管理写回执查询：按当前native scope及原request_id读`chat_scheduled_requests`，只返回“已观察提交/尚未观察”、plan_id与当前计划视图。表中没有原操作种类、提交时间和旧响应快照，不补造这些字段；不适用grant/enable/draft/run回执。

不直接给闭合旧v1 response加字段。新投影与旧21命令并存，旧调用行为保持，新增请求先有native provider再接页面；cursor必须绑定scope、context、搜索、排序和筛选。默认20条、上限沿现有100条，查询变化丢弃旧cursor/迟到响应，不能无限轮询。

### 3.2 创建时间与候选SQL23

这是实现PDF既定“创建时间排序”的最小数据补充，不是为未来新增数据平台。SQL23仅增加计划nullable created_at及必要scope排序索引；native在首次保存同库事务写入时间，后续编辑、暂停、重试及草案确认复用都不得修改它。SQL21/22的既有计划兼容读取时created_at返回未知，不猜测历史创建时间；SQL15没有定时表，仍返回storage_disabled，不伪装成可查询的空列表。

保留LATEST/default=15，最高可读版本扩至23；显式原生候选才选23 writer。检查现有`21..=22`版本判断、候选构造器及草案支持条件，使23能沿用既有能力而不意外启用发送。Host Store保持普通5/候选6，无新迁移；共享PlanView不为私有展示字段升级。

必须先验证临时合成库迁移、ledger/外键、正常重开和旧聊天读取。已有候选22的新reader先可读23，再允许writer；回退保留支持23的reader并关闭writer，不返回不能读23的旧binary，不降版、不复制或迁移日常库。本轮规划不会执行任何迁移。

### 3.3 一个共享授权上下文

沿用App/permissionStore/chatStore的scope、revision、到期与撤销来源，最小拆开“取得/续期native UI context”和“确保Host/Coordinator可执行”。已有有效context由管理页复用；需要重绑时由同一App级协调点完成并同步所有consumer，不能页面各自bind。管理context不能通过renderer声明tenant/capability或延长授权。

推荐先复用/整理既有bind路径的公共授权部分，给管理读取/保存一个不启动Host的取得路径，返回既有context DTO；若确需新私有IPC，先在该既有context权威源定义并生成，而不是手写第二种凭证。旧chat bind/执行入口的sidecar恢复和实际发送准入继续有效，取得context本身不恢复旧outbox、不授manual/automatic/draft动作许可。

scope/revision/到期变化使旧读结果失效，并清除页内数据和未提交编辑输入；已经发出但结果未知的管理动作与未提交表单区分，同scope正常到期重绑期间，仅在内存保留其原request_id和必要原请求用于查证/显式同请求重试。scope切换或实际撤权时清除或严格隔离，不能带入另一个scope。页面卸载只销毁自身请求，不dispose共享context或停止聊天。必须用“聊天→管理→聊天”、深链冷启动、正常到期重绑和Host未就绪的安全场景检查，避免以独立context绕过旧聊天依赖。

### 3.4 页面与表单

复用易界2.1.0 token、YjPage/YjPageHeader/YjTabs/YjEmpty/YjIcon及Naive表单/弹窗；不新加UI库或仿制PDF品牌。保留“我的定时任务/执行记录”、刷新、搜索、创建时间排序；移除订阅/推荐/全部项目。空计划、空记录、无搜索结果、无目标聊天分别解释。

手动表单按已批准字段：名称1—80、内容1—10000、仅一次/每天/工作日/每周、IANA时区、native时间预览、固定此设备、专属聊天/每次新聊天/已有聊天。既有聊天按scoped ID选取，排除草案和删除目标，显示可保存但暂不可执行的原因。不向用户暴露SQL版本、raw JSON、内部路径或授权token。

新建和编辑保存仍沿现有save命令，结果为paused、无grant。卡片清楚显示“已暂停”，可显示计划规则或“启用后预计时间”，不能把预览当已安排的下次执行。开启、立即执行、重跑及对话创建在本批不开放，并给出当前不可用原因；这是阶段边界，不是取消最终能力。已有开启计划可暂停，但不可用本页重新开启。

保存期间禁重入；脏表单关闭默认继续编辑；错误保留输入。编辑冲突保留本地稿并要求重新读取审阅，不自动覆盖。删除默认取消，成功只撤销未来计划、保留历史/聊天，在途/待审批/未释放unknown继续按native拒绝。

新增定时导航不得静默丢掉ChatPage组件内的未发送草稿。4A离开聊天前检查将卸载的全部composerDrafts（包括其它聊天目标的未发送文本），并核对当前未提交附件；使用最小离开确认，说明会放弃的草稿范围，默认留在聊天，只有用户明确放弃才继续。附件沿既有原生草稿规则处理，不趁导航清理其它目标附件；不在本批提前实现4B的跨页草案预填或全局持久草稿系统。

### 3.5 写入不确定与历史事实

一个显式管理动作仅分配一个request_id，保留原输入在当前scope的页面内存。超时、context失效或IPC返回operation_unknown时，不显示失败、不自动再次写入：先重建有效共享context，按原ID只读回查。已观察提交则展示同plan_id的当前视图；未找到仍是尚未确认，提供继续查询，不换ID创建。

用户显式安全重试save/pause/delete时必须复用原ID及完全相同的请求；原native digest/幂等事务负责拒绝冲突和避免复活。页面重载导致原请求上下文丢失时，引导核查计划列表，不按同名猜对应结果，也不把正文放localStorage。回执显示的是当前计划，不冒称原提交时的revision快照。

历史保留“全部状态/已开启/已暂停/已完成”，按批准的计划当前生命周期过滤；运行事实单列，不把turn completed写成业务成功。任务筛选按plan_id，复用有界含删除计划的选择查询；不能从当前已加载的一页记录凑“全部任务”。已删除记录仅按现有批准规则出现在全部状态；unknown/not_started不伪造成开始时间、耗时或结果。

4A只交付列表和必要的已有只读信息；完整执行详情、差异重跑、真实会话/turn定位在4B接续。不存在完整历史时呈现正常空态，不能seed用户库造演示结果或以synthetic运行判Must通过。

## 4. 验证与停止

1. 源先生成、strict Rust/TS conformance，保留旧21命令回归；有变化才运行对应跨仓检查，不借本批升级依赖/Runtime。
2. 自有临时SQLCipher验证15默认、22→23、23重开与兼容读取；新创建时间稳定，旧NULL不回填；保存回执与重复请求唯一，编辑不改历史snapshot，删除不删聊天。
3. 查询检查搜索/筛选交集、同名计划、时间相同、未知尾排、分页边界、旧cursor/迟到回执、被删除/草案目标；用正常数据与授权到期，不做故障/攻击注入。
4. 组件/路由/typed client检查各状态、表单错误/未保存确认、原ID回查、context共享、旧聊天文本/附件保护；不只用snapshot覆盖。
5. 在同一canonical候选入口和独立候选数据上真实操作“建一个暂停计划→编辑→刷新→正常退出/重开→同ID仍存在→删除取消/确认”，同时核对本批新计划无grant、本批动作不新增run/执行outbox/model turn；保留已有候选历史，不要求清空数据库。不得为了零调用绕到第二测试App、伪造二进制或放松产物资格；Provider key仅由既有native路径管理，不读取/打印凭据。真实Host未就绪下的纯管理能力可用正常不启动Host的native组合检查，不能强杀制造故障。
6. 实际检查亮/暗、1180×760外框及内容视口、键盘/焦点/弹窗操作。browser fixture只证明视觉和交互，真实native保存重开单独留证；未执行的运行详情/草案/电源/Provider/Must保持NOT RUN。

本批真实文本0、图片0、商家/MCP外部0，总额度仍0/12。没有日常DB/Keychain、Git提交/推送/tag/发布。测试/原生进程只正常停止；停止超时保留所有权并报告。完成后提交实施报告并停止，不自动执行4B。

## 5. 后续顺序与审查

4A之后：先受控完成Provider草案资格及对话入口/来源确认，再接既有计划执行控制和完整历史定位；最后防空闲睡眠、应用内重要更新和剩余Must真实验收。具体后续执行方案届时按源码及剩余额度制定，不在本次一并实施。系统通知继续延期；冷空历史无法恢复仍按31保留未知，不以重新创建线程绕过。

主代理核对需求、治理、实际源码与候选边界，并进行两项并行只读审查（UI查询/存储、原生授权/回执/验收边界）。发现的创建时间缺失、旧严格响应兼容、管理context依赖Host、按请求回执缺口及历史快照问题已纳入。审查不是独立人工批准；本轮没有产品代码/生成/服务/模型活动。既有D0、16小时例外及完整目标保持，SQL23和最小授权拆分作为本方案建议展示，并未提前实施。

末轮只读审查结论：无剩余方案阻断；已修订SQL15不可用语义、全部composerDrafts离开保护、到期与未知动作的scope内存区分，以及零新增执行与保留旧历史的计数口径。

本轮方案检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法和本地链接检查通过。四个产品仓起点文件逐字节保持，五仓HEAD/branch/remotes不变。详见[只读方案审查证据](evidence/phase-4a-plan-review-20260919.json)；这些检查不代表4A实现或产品验收。

## 2026-09-19 实施结果

用户明确授权后已实施，结果见[33报告](33-phase-4a-management-ui-implementation-report.md)。本页前文保留规划时点；实际候选SQL23，4A报告后停止，不自动进入4B。
