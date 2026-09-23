# FEAT-155 · 4D-1 执行记录真实时间与耗时闭环方案

2026-09-23。本轮只读调查和方案设计，未修改产品代码、启动服务、读取用户数据库或调用模型。建议下一步只实施本方案，完成后报告并停止。4D-1是按用户要求拆出的实施批次，不新增治理切片或改变FEAT-155范围。

## 1. 当前完成位置与本批目标

[41报告](41-phase-4c-3-single-run-and-rerun-report.md)已完成单次授权、独立重跑和真实结果定位；[43报告](43-phase-4c-3-ui-closure-report.md)已关闭弹层、主题、滚动和焦点的验收缺口。4C-3已经收口，不需要再次消耗真实额度证明同一重跑事实。

下一处直接影响原需求AC-009的缺口是：执行记录仍统一显示“未开始/未知”，详情也明确没有可靠执行时钟。下一批让用户看到**该次运行实际何时开始、已结束时耗时多久，以及何种情况下仍未知**；完成、失败、待审批等状态继续来自原生事实，不能由计时推导。

| 本轮源码事实 | 推论与限制 |
|---|---|
| 固定Runtime的canonical `ThreadReadResponse`、`TurnStartedNotification`、`TurnCompletedNotification`中的Turn均包含可缺省/可空的`startedAt`、`completedAt`（Unix秒）及`durationMs`（毫秒），不是experimental字段。 | 无需新增Runtime计时器、升级上游或修改固定二进制；字段存在不等于每个历史turn都有值，实际冷/热读取仍须验证。 |
| Runtime `thread_history.rs`从原生TurnStarted/TurnComplete事实构建这些值；`turn/start`接受回执本身可能没有时钟。 | 读取原生事实，不把接受、排队或请求返回当成开始；不在Host重建rollout。 |
| Host `nativeWireTurn`和`projectNativeTurn`只投影ID、状态、items、error，丢弃上述时间。Desktop `NativeTurn`严格拒绝未知字段。 | 不能直接向既有native-thread v1/v2或SSE v7/v8塞字段。 |
| Host已有`ReadThread`调用稳定`thread/read(includeTurns=true)`，核对thread身份；已有独立只读native-thread-status扩展先例。 | 可以新增独立的最小只读时间查询，复用原受管Runtime和owner-only bearer，不引入第二个执行器。 |
| Desktop管理查询`timing()`只返回`no_execution_clock`，native历史格式1/2与旧SQL迁移已固定。 | 需要明确只读投影、持久来源和typed IPC；不复活已退役的旧聊天计时/reducer，也不改旧native事实格式。 |

源码位置及摘要见[本轮复核记录](evidence/phase-4d-1-plan-review-20260923.json)。固定产物来源仍为[29批次provenance](evidence/draft-runtime-unblock/final-provenance.json)：上游`5d1fbf26c43abc65a203928b2e31561cb039e06d`、`rust-v0.144.6`，候选binary SHA-256 `bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`，canonical schema tree SHA-256 `34d353815dc8d800cb432a876d5b43350511f63b91ad9766f861e8bc8290cc92`。实施时重验该来源；本轮没有运行产物取得新的运行证据。

## 2. 推荐技术路径与取舍

采用 **固定Runtime thread/read → Contracts独立只读时间契约 → Host薄投影 → Desktop同库时间事实 → 管理IPC与页面**。

建议新增本机`native-turn-timing` v1契约族，候选路径为`GET /v1/agent-sessions/{agent_session_id}/turns/{runtime_turn_id}/timing`。一个请求只读一个已绑定turn；Host从现有会话映射取得thread，不接受客户端另传thread、tenant、用户或目录。精确匹配Runtime返回的thread/turn，只返回必要身份、可空时间、来源和可用性，不返回消息、工具正文、cwd或Provider配置。最终字段及错误枚举先冻结在Contracts源并生成，不能在两个消费者各手写一份。

不直接扩展旧native DTO：其closed schema会破坏现有消费者，并牵动聊天SSE与持久格式升级。也不建立Host时间事件流或Host时钟数据库：已有原生历史可读，FEAT-155只需要最小运行元数据。独立只读查询增加一个小接口和一次有界读取，是本批更小的兼容改动；原生历史不可读时明确保留未知，不用Host接收时刻补齐。

本批不会声称实时毫秒秒表。运行开始事实可显示，运行中/待审批的最终耗时显示“尚未结束”；结束后展示Runtime已有`durationMs`。审批等待包含在原生整轮耗时中，不另造“纯模型耗时”。

## 3. 执行顺序与完成标准

| 顺序 | 实施内容 | 完成标准 |
|---|---|---|
| 1 | 核实固定Runtime的时间事实 | 对固定schema/源码完成单位和来源检查；使用声明的本机Provider验证新turn、完成后及正常重开后的原生时间读取。缺值和未物化保持未知；不修改Runtime、不启用experimental。 |
| 2 | 最小只读契约与Host投影 | 新接口同源生成、严格校验，复用现有bearer和thread/read；旧native-thread/SSE字节形状保持。缺失、不可读、超时、身份不匹配均不能触发start/resume或重发。 |
| 3 | 兼容读取与候选SQL26 | reader先支持SQL26，再仅对隔离候选启用新迁移；同一SQLCipher/worker保存时间事实，旧记录无凭空回填，迁移/重开/旧聊天通过。普通入口仍SQL15、Host普通5/候选6。 |
| 4 | 既有观察与有界补读 | 在可信绑定、原生开始/结束观察和正常恢复后补读时间；网络读取不占SQL事务，不阻塞预约释放，不漏掉已释放的终态run。重复/晚到/缺失响应不会清除已有事实，不获得执行资格。 |
| 5 | 列表与详情显示 | 使用运行快照时区显示到秒；未开始、进行中、未知和已知时间准确，耗时来自Runtime；编辑计划/重跑不改旧历史，聊天及turn定位保持。 |
| 6 | 零真实调用组合与原生验证 | 契约、临时库、原生查询/恢复和页面定向检查通过；实际亮暗/1180×760/正常重开可用，Provider分账和正常清理明确，报告后停止。 |

步骤1的真实Runtime协议证据和模拟DTO测试必须区分。可先完成源契约定义，再用生成类型形成验证适配；**必须在SQL writer及页面接线前取得最小原生产物读取证据**。如固定产物不能提供已知时间，停止相应接线并报告具体缺失，不自动扩展为Runtime改造；仅缺旧历史不是阻断，只要新运行闭环可靠且旧记录如实未知。

### A. 时间与错误语义

- Runtime的`startedAt`和`completedAt`保持Unix秒；`durationMs`保持毫秒。客户端按安全整数及日期可表示范围校验；`0`是有效值，不能用truthy判空。缺省/null为未知，非法值为不可用，不截断、不取绝对值。开始、结束、耗时分别表示可用性。
- 执行时间指实际开始，不指计划槽、计划创建、授权、请求接受或本机观察时间。耗时只使用原生duration；不由整数秒差代算毫秒，不累加tool item耗时，不从UUID、消息时间、Provider台账或旧退役表推导。
- started/ended壁钟与duration不强行要求精确相等，秒级舍入和系统时钟变化不能被误判成毫秒等式失败。矛盾或越界数据保留来源诊断，不覆盖已有可信事实；不因此改变运行结果、额度、预约或重投决定。
- 有可信原生开始事实、尚无结束耗时时显示“尚未结束”；缺少结束信息且无法确认仍在执行则显示“未知”。没有开始事实不等于从未开始：只有既有未尝试/未执行槽事实才显示“未开始”；已经尝试且无时钟的记录保持未知。
- 未找到会话/turn、旧Host无端点、历史未物化、Runtime不可读、请求超时、格式不支持分别定义机器语义；不能把404/503或null解释为“没有执行”。所有HTTP响应no-store，诊断不泄露原始输入或内部错误。
- 时区来自该run的计划快照，不跟随后续编辑；旧快照无法解析时明确用UTC并标注。列表和详情使用同一格式化函数，日期/时间到秒、时区及该时刻偏移明确。耗时保留毫秒精度的原始事实，UI可统一显示秒/分钟，短于1秒不能误显为未开始或空白。

### B. 只读接口与采集边界

- Host是原生事实的薄适配者。查询不得start、resume、turn、审批、修改operation或刷新授权；不遍历Runtime目录、不解析rollout、不新增bbolt schema和计划逻辑。API仅在本批明确的local候选能力下使用，沿现有owner-only bearer，不引入公共认证体系。
- 使用现有RPC deadline和消息大小上限（当前默认16 MiB），补读限制turn数量/返回体并精确查找。达到上限返回明确不可用，不能截断后伪称目标不存在；不循环分页、递归扫历史或自动重试到成功。固定Runtime内部读取历史的成本应如实记录，Host限流不能被写成已优化Runtime全量历史读取。
- Desktop先验证management read authority、本地owner/tenant、run→conversation/local turn→Host session/Runtime thread/turn完整绑定；异步返回提交前再验证绑定与删除状态。仅renderer提供run ID，不接受其提供时间或Runtime身份。查询不要求计划仍enabled、自动grant未过期或Host可发送；已完成/暂停计划仍可读取缓存。
- 采集复用原Coordinator的受管读取生命周期：可信绑定/原生观察后合并同一run请求，每个run至多一个并发；终态释放不等待时间查询。恢复/刷新每批最多50条本地候选、最多1个在途RPC，单轮失败不紧循环；详情可显式补读一个run。参数及退避必须在实现前固定并测试，不能用全库遍历实现“后台刷新”。
- 开始/结束到达与Runtime持久化可能存在短暂间隔。每次自动采集最多3次读取（初次及1秒、5秒后的两次补读），每次deadline不超过3秒且不放宽现有RPC上限；耗尽后保留待补事实，等正常恢复或显式详情刷新形成新的有界读取，不由定时循环立即重置预算；正常重开和用户详情刷新有独立补读机会。已释放终态run不能因原recovery候选筛选被永远遗漏；补读集合须来自索引化的缺失时间记录，并具备有界游标，不能只扫描占用中的run，也不能被一个旧缺值记录饿死。
- 退出/睡眠使用既有正常停止及取消流程。时间读取失败不能阻塞退出、开启发送资格或触发重跑；实际发出次数仍由原账本负责。原结果/审批/预约观察继续是唯一状态权威，新时间表不能成为第二套状态机。

### C. 同库兼容和历史真实性

拟新增`0026_scheduled_execution_timing.sql`，只放关联run的时间事实及补读所需最小来源/版本/诊断和索引；不用另一文件数据库。以run唯一键约束，存对应可信Runtime身份并在写回时核对。时间表不新增状态、授权、额度或outbox的第二份权威。

先扩reader最大版本及新表可选读取，旧库缺表返回已定义未知；普通迁移目标保持15。合成库15/25→26、关闭重开、旧聊天/计划/run/outbox/额度/预约逐项保持。只对canonical显式隔离候选迁移至26，Host5/6不变；旧1～25迁移不改，chat native持久format1/2不改。不迁移或读取日常库。

旧run无新行正常表示无缓存，迁移不计算/回填时间。已绑定旧记录可在后续受权只读查询确有Runtime时间证据时保存来源；这不等于凭空回填。已知时间单调补全：缺省/null或暂时不可读不清空旧值；相同重复幂等，冲突不任取最新值，保存有限诊断并展示受影响字段未知。完整原始消息/历史不复制到新表。

已删除聊天的既有时间可以保留为最小运行历史，但不能因此恢复聊天关联或继续向已删除目标查询；缺失目标仍按原语义反馈。独立重跑写新run的时间，不改旧run。新的只读管理查询通过主键/现有分页有界join，不逐行同步访问Host；原筛选、排序和分页语义保持，时间补齐不能导致本批无关的列表排序重定义。

回退只停用时间能力、回退到已支持26的兼容reader构建，不降低user_version、不删除新表。未升级的25 reader面对26应明确拒绝，不能伪称旧可执行程序可直接打开新库。候选writer在reader通过后才启用。

## 4. Contract First与仓库边界

本轮文档`contract-impact=none`。未来本批整体保守按**breaking**评审：独立HTTP端点本身additive/provider-first，但候选SQL26及严格私有管理Timing返回结构改变，旧reader/validator不能直接消费。

| 权威/仓库 | 本批职责 |
|---|---|
| 固定Runtime canonical schema | 原生字段、单位、null及历史语义唯一源；只读参考，源码、patch、产物不修改。 |
| yijie-contracts | 新只读Host契约、Runtime稳定投影说明、生成Go/TS及同源校验、源摘要锁、兼容文档。新family不修改native v1/v2、SSE v7/v8或旧恢复接口，不增加新工具/依赖。 |
| yijie-agent-host | 新GET及最小raw解码/投影，复用受管ReadThread；不新增执行状态或持久库版本。 |
| yijie-desktop | 私有SQL26/reader、绑定核验及有界采集、管理Timing IPC源与生成物、列表/详情。普通聊天native格式和发送机制保持。 |
| yijie | 本方案、实施报告、来源与费用/验证证据，更新当前进度；不改旧失败/通过记录的历史含义。 |

Owner仍为段成威；producer是Host，已登记consumer是Desktop native，renderer仅消费其私有IPC。Runtime规范→Contracts投影→生成consumer/compatible reader→候选writer/UI按此顺序验证。unknown-public当前不适用，本批不发布。本地dirty候选使用完整base commit、逐文件摘要和generator身份，不伪造新不可变commit或覆盖旧发布pin。

实施应执行适用源生成、生成漂移、lint/test及breaking，至少保护当前FEAT-155登记的四个完整比较基线：`db4458fe94572c4df41a114005d54a049bb79b1f`（fallback）、`f16a497e1377f45747f8ff9292b4b60cf2027f88`（supported）、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。实施前再核对supported清单；新端点不存在于旧基线不代表旧族无需回归。新Host/旧Desktop保持旧协议，新Desktop/旧Host降级时间未知并保持原管理/执行边界。独立local leaf生成遵守已有工作区保护，不借机改全仓dirty门禁。

## 5. 验证、预算与停止点

| 验证层 | 必须取得的证据 |
|---|---|
| 契约/Host | canonical单位与null、0值、安全整数、缺失/不匹配/超时；query只发thread/read且不改Host记录，old native端点/SSE保持。纯合成数据直接经函数/进程内HTTP测试，不运行攻击fixture。 |
| Desktop原生 | 身份/授权复验、同库迁移重开、重复/晚到/缺值不抹事实、已释放终态可补读、删除/编辑/重跑关联正确、分页有界。时间采集失败不改变run结果、预约、grant及outbox。 |
| 时间展示 | 秒/毫秒单位、短耗时、UTC与夏令时偏移、旧未知/未开始/已开始/已结束区别，详情与列表一致；不制造本机跳钟故障。 |
| 原生集成 | 固定Runtime与声明的本机Provider完成一次受控运行与独立重跑，核对新旧run时间来源及结果定位；正常退出重开可读持久时间，无旧操作重发。先取得上述最小原生资格，再启用正式候选writer。 |
| 实际UI | canonical App亮暗、1180×760、长时区/时间文本及键盘详情/返回可用；43修正的弹层/焦点不退化，历史未知有明确解释。 |

本批**真实文本0、图片0、商家/MCP外部0**，累计仍10/12、剩余2次。使用无上游转发的声明式本机Provider，最多2次短文本请求（原运行+重跑），在步骤1与最终原生验证之间共享总额和台账；步骤1使用既有SQL25候选的受控手动入口产生首个run并核对原生只读时间；实施后对它验证有来源的补读与UI，SQL26下再验证独立重跑，不为同一证据重复造运行。没有真实Provider验收目标；不得把本机HTTP响应写成真实模型能力验收。失败时先用零调用静态/合成检查修正，不自动增加实际请求次数。

Desktop执行同源IPC检查、lint/类型/构建和受影响原生/前端测试；Host执行lint及审查过的安全测试名单；Contracts执行适用生成、lint、test和逐基线breaking。已有全量Contracts tracked-change保护及历史禁止fixture不绕过；明确区分通过、阻断和未执行，不能拿定向绿色替代全仓通过。测试变化必须验证实际边界，不写只复制实现的测试。

只使用正常开发、原生停止、退出和清理；不强杀、不替换/伪装Runtime或故障可执行文件、不破坏权限、不注入攻击资源。保留已有dirty工作区，标准构建只更新可复现的项目产物。结束时计划暂停、无活动本机请求和遗留测试进程，确认未新增真实调用、未迁移日常库。

完成后保存45实施报告及单独证据索引：当前来源/生成一致性、实际原生时间与UI、正常重开、调用台账、未执行项和影响。本批只关闭AC-009的执行时间/耗时缺口及相关AC-010兼容子项，不宣布整个FEAT-155 D4。

后续仍有卡片操作细节、macOS防自动空闲睡眠、应用内重要更新及全部Must同次fresh验收；系统通知继续按用户决定延期。本批不实现这些项目，不新增云调度、后台守护进程、统计报表、实时秒表或全聊天历史重构。完成后停止，不自动进入下一批，不提交、推送或发布。

## 6. 本轮方案自审

已从AC-009反推事实来源、最小查询、严格旧consumer、同库兼容、终态释放后补读、旧未知、费用与实际验收边界。舍弃直接改闭合native DTO和本机推算时间两种路线，保留固定Runtime原生读取作为唯一来源。本方案是本任务技术自审，不冒称独立人工批准；实际Runtime字段可用性作为实施首项验证，尚未声称通过。

文档检查和四产品仓未改核对结果见[方案复核记录](evidence/phase-4d-1-plan-review-20260923.json)；其通过仅表示方案与治理检查通过，不是实施或产品验收完成。

## 执行结果补记

本方案后经用户明确授权实施；另获2次文本额度追加，累计上限14。本批真实0、本机Provider2/2，普通15/5、候选26/6。具体实现、验收与未执行项见[45实施报告](45-phase-4d-1-execution-timing-report.md)；本方案内10/12和未实施表述为方案保存时的历史记录。
