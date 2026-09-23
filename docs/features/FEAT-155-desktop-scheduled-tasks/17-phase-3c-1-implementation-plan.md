# FEAT-155 下一步执行方案：3C-1 受控手动投递接线

后续实际状态：用户已明确要求按本方案实施3C-1，候选源码/零调用组合检查已完成并停止，见[18实施报告](18-phase-3c-1-implementation-report.md)。必要私有扩展实际为schema20（错误码/native claim证明），普通15和默认禁发保持，真实平台/Provider仍NOT RUN；下述方案形成时状态保留历史含义。

2026-09-18。用户本轮要求“给出下一步执行方案”。本轮只读调查、保存方案和检查文档，不开始实现。起点为[16：3B-2实施报告](16-phase-3b-2-implementation-report.md)，整体目标和授权沿[09](09-phase-3-implementation-plan.md)、[04](04-owner-approval-and-implementation.md)及[ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)。

## 1. 下一批结论与停点

**建议下一次只实施3C-1：把已有手动run接到原聊天投递链，完成候选准入、受管目录、预扣额度校验及发送/恢复组合事务。** 三种“运行于”均覆盖；完成定向检查、自审、报告后停止，不自动进入自动触发、独立重跑、草案或页面。

完成标准是“候选手动链已接通并通过零真实调用的组合检查”。普通App入口仍以schema15为迁移目标，scheduled在claim和实际I/O处默认拒绝；CompatibleReader、新格式可读或恢复就绪均不赋予发送资格。实际macOS/Provider与正常产品入口资格仍未通过，不能把3B-2或本批合成PASS解释为允许激活。

本轮文档`contract-impact=none`，没有改变产品行为。未来本批按最高**breaking**准备兼容审查，影响来自持久投递/重放和授权解释；实现时逐边界说明实际变化，不因wire字段未变就省略审查，也不预先新增不需要的公共字段、API或schema版本。

本批支撑AC-004的三目标与防误发、AC-006的立即执行/幂等、AC-007的删除保护、AC-009的关联和AC-010的执行复用/权限/恢复；它不完成页面、自动调度或真实产品验收，全部Must仍pending、D4 NOT RUN。

## 2. 已核实的起点与选择理由

本轮复核[3B-2来源证据](evidence/phase-3b-2-source-20260918.json)全部96份候选文件，摘要保持；五仓HEAD、branch、remote与16一致，Runtime clean。3B-2的45项native、17项旧路径及平台NOT RUN均保留为上批事实，本轮未重跑产品检查。两项并行只读技术复核不是独立人工批准。

下表Desktop路径相对`src-tauri/src/`，行号为本轮候选：

| 源码事实 | 本批必须解决的事项 |
|---|---|
| `chat/schedules/execution/preparation.rs:269`只有`prepare_manual`；`execution.rs:389`固定manual | 先闭合现存producer，再增加automatic/rerun，避免多条未完成链同时进入outbox |
| `schedules/execution_guard.rs:41,88`分别拒绝scheduled claim与实际出站 | 引入受限native候选准入，不直接删除两处防线 |
| `schedules/execution.rs:188,209`把已占满的grant判Exhausted；`recovery.rs:366`仅guard加尝试标记 | 新增“验证本run已预约额度”的发送检查，不重复扣额，也不误拒自己的最后一次额度 |
| `chat/application.rs:1770`创建路径强取用户bookmark；`schedules/workspace.rs:136`已有按来源解析 | 让原创建路径识别已绑定native受管目录，不伪造用户书签 |
| `schedules/recovery.rs:46–67`候选未携create/turn尝试阶段；`application.rs:2253–2271`可能对未发操作查404 | 按持久尝试事实区分首次发送与未知恢复，不能把正常未发误标为未知 |
| `schedules/recovery.rs:139`映射恢复只写session/thread；`chat/database.rs:3186–3204`正常创建另有原turn接续事务 | bound恢复复用原create→turn事务，保持原operation，不多建聊天/运行或重复创建 |
| `chat/database.rs:2554–2555`旧outbox允许租期回收；`:3715,3885`接受/失败主要处理聊天状态 | scheduled尝试后停止租期重投；接受、错误、未知与run事实同事务收口 |
| `execution_guard.rs:13,101`预约与turn/outbox/public-task均参与占用 | 只豁免本run精确关联的自占用，其它前台、审批、unknown和删除仍阻挡 |
| `schedules/execution.rs:299`确认grant后计划保持paused | 手动执行不能错误要求计划enabled；自动启用属于后续工作 |

三个可选顺序中，直接接自动扫描会扩大上述缺口的触发次数；先做草案会增加创建入口但不能完成执行；**先接手动链**能用现有组合事务、固定operation和三目标，最小地验证原需求的执行基础，因此推荐。三目标、两种创建方式和本机唤醒目标均保留，系统通知继续延期；不因超过16小时削减范围。

## 3. 依赖顺序与完成标准

### 第一步：定义候选准入、尝试阶段和最小兼容变化

沿原native应用服务、唯一Coordinator和HostBridge建立同一发送资格判断。日常构造、CompatibleReader及未知格式默认拒绝；本批只有明确的native候选构造可进入受控组合检查，不能由renderer参数、环境变量开关、数据库某个布尔值或一条调试命令绕过。候选构造只选择检查范围，不替代当前native authority、授权、占用、绑定及生命周期事实。

两个检查位置均保留：claim只选择当前有资格且该阶段从未尝试的记录；实际I/O前在原worker内重验并原子记录尝试。实际发出请求仍经过HostBridge的身份、readiness、权限及epoch检查。复用可测试的实际发送策略，不为测试复制一个始终放行的发送器或第二Coordinator。

先明确当前run、create operation、turn operation、local conversation/turn、session/thread/native turn的对应关系；create与turn分别依据持久`never/not_required/attempted/unknown`事实决策。旧记录缺少证据按unknown处理，不因代码曾禁发就补成never；reader理解版本不等于writer或dispatch有资格。

私有schema19已有证据优先复用。仅当现有字段无法无歧义记录本批必要状态时，新增下一migration（当前候选20），不得改1—19字节/checksum；先兼容reader再writer，验证合成前向迁移、正常关闭/重开及旧聊天/授权/outbox保持。普通迁移目标仍15，回退使用能读新格式但关闭writer/dispatch的候选，不降级数据。

共享执行状态、错误或恢复语义若确需变化，先修改Contracts权威源，再生成、同步、做严格conformance和适用breaking基线；仅native私有状态留Desktop。无必要则保持现有wire与Host业务实现，不手写影子DTO、不预铺自动调度或草案契约。

### 第二步：校验本run的授权、额度和占用

在准备新run与发送已预约run之间分开检查语义：前者要求剩余次数并扣一次；后者必须证明该run已经由同一授权、同一事务占额且未退款，不再要求“还能新增一次”，也不再扣额。

- 两处发送资格均取当前native scope与ScheduleRun能力，检查授权revision/期限、计划revision/schedule_epoch、定义摘要、稳定授权目标与实际绑定、目录来源和当前Ask。禁止缓存旧UI授权、接受renderer自报scope或静默提升权限。
- 最后一个名额已由当前run占用时允许它继续，其它新请求仍拒绝；过期、撤销、编辑、目标失效及授权版本变化仍阻止新I/O。请求幂等回执不能被当成新的发送许可。
- 手动执行可以针对已明确授权的paused计划；不把“paused”本身当作撤销。实际暂停/编辑/删除后的revision、授权或目标变化须生效；已开始的操作保留事实，只读观察不因grant过期或计划变化而停止。
- 只豁免当前run精确关联的reservation、turn、create/start outbox和public-task绑定；其它占用、待审批、删除job或未知关联仍拒绝，不能排除整个聊天或所有scheduled记录。
- 按阶段检查live审批/执行：原生证据确认本run尚无Host session且create为never时，同会话审批查询为N/A，仍须检查其它占用、当前native授权、Ask、目录和Host readiness。已有或恢复到bound的session，turn出站前必须从当前受管Host查询精确会话的执行/审批；身份缺失或读取不充分则不发送。批准、拒绝仍沿完整聊天链；审批列表消失不是终态或发送授权。

明确线性化点：最后一次本库授权/关联重验与attempt标记在同一事务；此前完成目录及必要只读准备，跨await后重验当前事实和生命周期epoch。标记后只进行该原操作的至多一次出站尝试；后续即使epoch变化、请求未确认或本机退出，也保守转恢复，不清标记重试。SQL提交与网络发送不是跨进程原子事务，不能作此承诺。

### 第三步：三目标沿原目录与create→turn链投递

原创建路径按项目的native来源解析：用户项目继续用真实bookmark；受管项目用现有资源ID、已绑定canonical路径和native resolver。文件系统准备后回到同一worker重验，不让renderer传任意路径、不伪造bookmark，也不新增目录清理服务。

三目标都复用已保存run和原outbox：专属聊天首次创建后稳定复用；每次新聊天保持本run唯一关联；已有聊天使用原session/thread及目录。不得为了通过忙碌/权限检查另选聊天、另建run或改变用户目标。

正常create成功和精确mapping bound恢复复用同一内部事务helper：核对原task/create operation/session/thread，完成原create outbox，幂等生成并标记**原turn operation**的outbox。恢复已存在绑定时仅校验一致性；不创造第二个操作、不重复占额。reserved/404/身份不一致不进入下一阶段。

恢复本身只读远端；bound后的原turn只有在持久证据为never且重新满足全部发送资格时，才可作为下一阶段首次发送。它不是重发create或重跑旧turn。create/turn任一已attempted或旧unknown，均禁止以租期回收再POST。

现有demo_fast public-task适配只返回稳定本地client reference，本批保持这一事实；不扩建控制面服务，不调用商家接口。scheduled文本沿现有v2/permission-turn Ask和同一operation，不退回legacy v1；普通聊天路径只作必要兼容适配。

### 第四步：接受、失败、恢复与释放同事务闭合

让原聊天的接受/错误处理同步落下run、outbox和恢复事实；不能分别提交导致一侧认为可重试、另一侧认为已执行。投递状态、native结果、needs_attention和占用继续分开。

| 实际证据 | 本批处置 |
|---|---|
| 尚未进入任何可能I/O阶段，资格已失效 | 保留明确未发事实；符合3B-2全部条件时本地取消、处理原outbox、释放并一次退款 |
| 已记attempted，包括发送后超时、普通错误或结果未写回 | 禁止租期重投；持久记录原因并走原精确恢复，不能靠HTTP状态码、时间或新nonce认定未执行 |
| create已确认bound，turn仍never | 幂等衔接原turn；额度不变，下一阶段发送前重新校验 |
| turn精确accepted | 同事务绑定原native turn、完成投递回执，再沿原native read/SSE观察；不表示运行成功 |
| 操作pending/uncertain/404或读不到充分证据 | 保留原身份、占用、额度及需处理状态；不猜终态、不自动重发 |
| 精确native终态或3B-2认可的正常代次停止/静止证据 | 按既有证据规则释放；同步唯一索引、有效占用、旧中断/删除保护，unknown历史不伪改 |

对明确返回的错误保留具体原因；没有native turn就不能伪造`native_terminal`。本批不新增“人工强制释放”或基于一般错误的退款捷径；若发现协议确有不同的未接受保证，先回源审查，不能在consumer自行推定。已经创建远端会话但尚未发turn，也不满足“两阶段均未尝试”的全额退款条件。

未发送阶段不因无意义的恢复404变成unknown；已尝试阶段也不能因某次404恢复成never。重复回执、重复映射恢复、正常重开均须幂等；已释放旧run不被恢复选择器重新激活，旧create/start/interrupt永久不误发到后续运行。

### 第五步：零调用组合验证、报告并停止

使用普通临时SQLCipher，通过实际native准备服务创建三目标run，再由**原Coordinator和实际HostBridge**消费进程内HTTP的正常声明响应；不手填一条“成功run”代替组合路径。检查明确标为组合/协议证据，不冒充真实Runtime、OS或Provider。

| 检查组 | 完成标准 |
|---|---|
| 正向链 | 三目标；首次create不被尚不存在的session误阻挡；create→原turn、已有聊天直接turn、bound恢复→原turn；每阶段精确一次请求、同一operation、一次占额；accepted后原生事实观察与释放 |
| 授权与自占用 | 自己的最后一次额度可用；新run耗尽拒绝；期限/revision/目标/Ask变化阻止发送；自身关联可识别，其它前台/审批/unknown仍阻挡 |
| 异步与恢复 | 正常受控await期间改变资格或发出sleep/stop事件后不能错误发送；attempted不被租期重派；缺证据仍未知，never不误判；重复恢复/重开不多建、不多扣退 |
| 存储与旧行为 | 默认15和普通reader均零scheduled POST；必要新格式正常迁移/重开；占用、active唯一索引、删除和旧interrupt一致；普通聊天/权限回归保持 |
| 契约与静态 | 有变化的权威源/生成/consumer严格一致；按影响跑fmt/clippy和安全定向检查，必要的lint/build；没有变化的产品部分不无谓重跑 |

使用正常合成状态、时间参数、HTTP响应和正常停止，不强杀进程、破坏权限、攻击注入、替换Runtime或伪装二进制；不运行含这些行为的历史全量套件。测试代码可声明epoch变化和普通错误事实，但不能把这种检查写成真实系统故障验收。

本批真实文本调用为0，累计仍**0/12**，图片/商家接口0。不启动App/Host/Runtime/Provider，不访问日常库/Keychain。完成后交付实际命令、来源摘要、失败与修正、未执行项及默认禁发证据；元仓状态/日志如实同步，随后停止。

## 4. 实际激活前的边界与后续顺序

真实macOS睡眠/恢复、窗口退出和Host/Runtime正常退出，真实Provider审批/恢复，以及三目标在正常产品入口的执行均继续**NOT RUN**。当前canonical launcher尚无本需求已合格的零日常库/Keychain验证入口，计划页面/command及最小受管来源展示也未接通；本批不造调试App、临时后台命令或另一个产品数据库来绕过这些缺口。

实际激活前须在后续方案中落实：同一正常App的入口与数据边界、最小来源展示、原生平台证据、真实调用计数覆盖。已有请求计数器按HTTP请求累计，草案/澄清/执行/标题/内部重试均计入12次总额，不按run计次，不重置台账换取额度；目前其limit不支持0，本批不启动它。09建议第三阶段最多4次、至少留8次最终验收仍是后续预算分配，不构成本批调用。

| 后续批次建议 | 依赖与范围 |
|---|---|
| 3C-2：自动触发与独立重跑 | 依赖本批发送链；显式启用、同库occurrence/run/outbox/额度/next-at事务、连续清醒与迟到规则、忙碌跳过、恢复不补跑；重跑用新request/run/operation、当前配置并保留差异 |
| 3C-3：固定草案与最小typed IPC | 固定outputSchema的源/Host适配、原聊天草案严格校验、用户确认与同源保存；只接第四阶段所需command/query/event，不开放任意schema/config/SQL/路径 |
| 第四阶段及真实激活验收 | PDF页面和两种创建、管理/历史、受管来源展示、应用内更新及防空闲睡眠；满足正常入口/平台/计数资格后按现有12次总预算做真实验证，全部Must实际通过才判D4 |

这是依赖顺序细化，不把3C拆成新增功能，也不自动授权连续实施。自动producer当前尚无enable、到点claim或完整occurrence处置；草案顶层生成和普通turn的outputSchema也未接，不能以现有枚举、纯时间函数或title示例宣称已有能力。

## 5. 仓库范围与本轮记录

| 仓库 | 下一批最小范围 |
|---|---|
| Desktop | native候选准入/已预约run校验、原目录与投递接线、阶段恢复和同事务结果、必要兼容与定向检查 |
| Contracts | 仅在实际共享语义变化时回源、生成、同步和检查；不提前加入自动/草案接口 |
| Host | 优先复用现有创建、Ask、两GET/native观察；只有上述实际契约变化才作必要消费适配 |
| 元仓 | 方案、实际报告、来源、验证与未执行项；当前仅修改这些文档 |
| Runtime/API/Infra | 固定只读，不升级、不新增服务 |

旧实施授权不解释为本轮立即开始3C-1。当前没有产品代码、生成器、产品测试、服务、数据库或模型操作，没有Git提交/推送/发布或改变分支/远端；已有未提交候选全部保留。

本轮方案检查：定向技术审查提出首次create尚无Host session的前置死锁风险，已按阶段明确审批检查并加入正向断言。strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及83处文档链接/空白检查实际PASS；96份业务候选摘要、HEAD/branch/remote及已有dirty条目数保持。以上只证明方案/记录一致，不代表3C-1实现、实际激活或D4通过。
