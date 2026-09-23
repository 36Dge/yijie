# FEAT-155 下一步执行方案：3B-2 恢复、审批观察与原生生命周期

2026-09-18。用户本轮要求“给出下一步执行方案”。本轮只读调查并保存方案，未开始3B-2实现。起点为[14：3B-1实施报告](14-phase-3b-1-implementation-report.md)，产品边界沿[09](09-phase-3-implementation-plan.md)及已接受的[ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)。

后续实际状态：用户已明确授权本方案3B-2，源码与安全定向检查已完成并停止，见[16实施报告](16-phase-3b-2-implementation-report.md)。真实macOS/Provider资格仍NOT RUN，定时双层禁发、普通目标15保持。下述“本轮仅方案/未开始”保留制定方案时含义。

## 1. 下一步与停点

**建议下一次只实施完整的3B-2：只读恢复、审批观察、有证据的预约释放和原生退出/睡眠恢复基础。** 以下六步属于同一批次的依赖顺序，不再拆出新的产品范围。完成定向检查、自审和报告后停止，不自动进入3C或第四阶段。

交付结果是：已准备的run有可验证的恢复与占用处置路径，审批沿原聊天观察链处理，正常退出和sleep/wake能关闭新发送资格并保留未确定事实。**scheduled记录在claim和实际出站两处仍禁发；普通入口迁移目标仍15。** 本批不把“观察就绪”当成可执行，不激活自动触发、手动真实投递或新增renderer入口。

本轮文档`contract-impact=none`，只定义未来工作，没有改变行为。下一批最高按**breaking**处理：预计新增Desktop私有schema19及跨版本占用解释；恢复HTTP形状优先保持现有v0.1.0，仅增加同源Rust消费产物。若发现必须改变wire语义，先回权威源登记影响、生成并验证，不在Desktop手写影子DTO。

本批支撑AC-004的目标/占用、AC-005/006的状态与去重、AC-007的删除保护、AC-009的真实关联和AC-010的持久恢复/权限/生命周期；合成检查不能完成这些AC的真实产品验收，全部仍保持pending。

## 2. 已核实的源码事实

本轮复核[3B-1来源证据](evidence/phase-3b-1-source-20260918.json)全部81份候选文件，摘要一致；五仓HEAD、分支、远端保持，Runtime clean。14中的检查是上批实际结果，本轮没有重跑或据此宣称3B-2通过。两项并行只读复核属于Codex技术审查，不是独立人工批准。

下表Desktop路径以`src-tauri/`为基准，行号为本轮候选源码位置：

| 已有事实 | 对下一批的约束 |
|---|---|
| Contracts `scripts/generate-scheduled-task-recovery.mjs:16`当前只生成Go/schema，sync只覆盖Host | 先增加同一leaf的Rust生成、条件校验和Desktop来源锁，不复制HTTP类型 |
| `src/chat/host_bridge.rs:1278,1299`所有authorized request先要求Runtime ready；Host两个恢复GET只读bbolt | 两个精确GET只要求受管Host存活/身份一致及owner认证，不能被Runtime未ready挡住；其它请求保留原readiness |
| `src/chat/database.rs:3706,3808`绑定会保存所传Host nonce；`application.rs:2309`观察要求来源身份 | 当前响应Host身份不能写成历史执行来源，须区分原执行来源和本次读取来源 |
| `application.rs:2095,2431`只有一个Coordinator，但主要观察首个active session，SSE循环也会dispatch | 恢复须按原run精确选择并复用唯一观察链；停止屏障覆盖内外两处dispatch，不能只停外层循环 |
| `execution_guard.rs:13,89`预约、unknown、turn/outbox/public-task都会占用；`workspace.rs:73`另有删除保护 | 删除reservation不足以释放，须统一“有效占用”解释，同时保持历史unknown |
| `migrations/chat/0001_chat_core.sql:109`对queued/streaming/stopping建立单聊天唯一索引 | 只改查询仍不能开始下一轮；新migration需适配有可信静止证据的scheduled行，旧迁移不改 |
| `src/lib.rs:436`只处理不可取消的Exit；`chat/ipc.rs:376`取走Coordinator后消费式stop | 改为ExitRequested先阻止退出、关闭发送，再由持久owner完成正常异步收尾 |
| `chat/sidecar.rs:1077`未知清理会forget句柄并清身份；`:1035`存在超时强杀分支 | 本批正常生命周期保留子进程所有权及nonce，超时继续正常等待，不强杀、不forget |
| `chat/worker.rs:111`最后一个Arc句柄释放才join数据库线程 | 清一个字段不能等同数据库已关闭，必须在所有owner结束后checkpoint/释放 |
| `chat/schedules/time.rs:163`ContinuousAwake只是输入；无原生sleep/wake监听 | 补真实系统观察与连续性证据，不能只比较时钟就声称已接平台 |

Host已有正常停止链：`cmd/desktop-host/main.go:223`先关入口，随后关闭Runtime并在超时后继续等待；`internal/codex/runtime.go:616`关闭stdin并等待真实退出。复用这些能力，不新增shutdown API、不改固定Runtime、不重构Host进程平台。

## 3. 按顺序实施

### 第一步：冻结证据规则、同源消费类型与兼容格式

先列清身份与事实：run、create operation、turn operation、local conversation/turn、Host session、native thread/turn各自独立。计划revision/grant只决定新执行资格；读取已存在run、收尾和恢复使用当前native scope/读取权限，不能因旧grant过期或计划已编辑而停止必要的只读恢复。

Contracts复用`openapi/scheduled-task-recovery/scheduled-task-recovery.yaml`，在既有leaf generator/check/sync增加Rust DTO、严格条件校验、Desktop schema/candidate和来源检查。bound必须有thread，reserved不得有；accepted必须有turn，pending/uncertain不得有。缺失optional与显式null不得混同，未知枚举/多余字段按closed源拒绝。生成器变化后按真实摘要同步Host候选锁，即使Go类型/handler不变；不改旧通用generator或legacy pin。

预计新增**私有schema19**，只记录既有表无法表达的必要事实：

- create与turn分别记录出站尝试及操作身份、当时受管执行代次；必须在可能I/O前持久化。标记一旦写入只能保守认为可能已发送，不能靠超时抹掉。
- 恢复绑定的来源种类及已知原执行来源；当前查询的Host实例仅是读取来源，不补写未知历史。
- 释放证据种类/引用、一次性本地取消退款事实，以及scheduled专用的静止协调投影。只存关联与状态，不复制审批/聊天正文或建立第二份执行队列。

旧1—18迁移字节/checksum保持；新增migration前向调整必要表和active唯一索引，默认未静止。普通15/16/17/18读取不得无条件查询19列，旧18缺少出站证据不能推定从未发送。正常临时SQLCipher验证完整升级、重开、旧grant/聊天/outbox保持；普通入口仍15，候选writer仅显式native构造。回退需保留支持19的reader并关闭新writer/dispatch，不降级或删除数据。

### 第二步：接入两类精确只读恢复查询

只消费已有两个GET，不增加Host恢复业务API：

1. `/v1/tasks/{task_id}/agent-session-mapping`查本地conversation/task对应Host session和thread映射。
2. `/v1/agent-sessions/{agent_session_id}/turn-operations/{operation_id}`查原turn operation回执。

仅`demo_fast + local`、当前native scope、受管Host owner bearer；使用canonical UUID、无请求体/query、no-store和有界JSON读取。沿HostBridge建立两个精确read-only方法：复用受管Host实例/`healthz`检查，不把通用authorized request整体放宽为不需Runtime ready。若响应携带responder nonce，验证其属于当前读取实例，但不解释为历史执行来源。

恢复只能使用本库原run关联的task/session/operation；逐一检查响应身份和已有绑定一致性。不得借Trace、目录名或最近聊天猜ID，不重建聊天，不重投原操作。精确accepted回执可建立原turn的只读观察关联；保留已知原代次，未知来源显式保留，通过受限恢复来源路径进入native read/SSE，不伪造普通提交来源。

| 事实 | 允许的处置 | 不能推出的结论 |
|---|---|---|
| mapping bound且身份吻合 | 绑定原session/thread | turn已发送或从未发送 |
| mapping reserved、404或不可用 | 保留未知、占用和恢复入口 | 重建、退款、释放或重投 |
| operation accepted且身份吻合 | 绑定原turn，继续native read/SSE | 已完成或业务成功 |
| pending、uncertain、404、超时 | 保留原记录和占用 | 租期到期就释放/重发 |
| 身份不一致或未知格式 | 拒绝应用该结果，标明需处理并阻断 | 修补ID后假定成功 |
| 当前Host nonce变化、idle、notLoaded | 作为当前读取事实 | 原执行已停止 |

### 第三步：复用原生事实/审批链，闭合有效占用

恢复观察从本库预约/run选择原会话，不依赖renderer当前打开哪一条聊天。仍使用唯一Coordinator、native buffer和持久化链，不建立第二聊天状态机。保留缺失/部分读取的不确定性；对精确匹配turn的completed/failed/interrupted，在原生事实落库的同一worker事务更新scheduled结果与占用。native completed只表示原生完成，不自动等同卖家业务结果成功。

审批使用当前`runtime_approvals`和既有完整聊天审批UI，不接已退役的FEAT-137 v6实验路径。live approval可能仅有session/thread级归属：可保守阻断并标needs_attention，不能伪称历史turn审批事实。批准/拒绝/回调消失本身都不是run终态，仍须继续观察；不自动批准、不提升Ask、不复用过期UI回调。

**历史结果与当前执行占用分开。** 允许释放的证据仅有：

- 精确匹配原run/native turn的可信终态；释放占用，不退已消耗额度。
- 历史结果仍unknown，但已确认该run对应的原受管执行代次正常结束，且当前代次的执行/审批检查无占用。仅解除互斥，unknown、needs_attention及已扣额度保持；旧代次未知或只看到新nonce不满足条件。
- 完整持久证据证明create和turn均未尝试发送的本地取消。取消旧outbox、run状态、释放和一次退款同事务；任一阶段可能已发送或旧格式缺证据则不走退款。不能仅凭当前禁发代码推断旧记录从未发送。

无证据、未知证据版本、错误关联一律继续占用，不提供“强制完成/释放”入口。租期、用户确认、重启、新Host实例均不能单独作为释放证据。

私有静止投影须精确绑定run、local turn及原操作，仅由可信证据同事务派生，不能由renderer或普通状态写入。新migration替换active唯一索引，使**有证明静止的scheduled行**不再占执行位；普通legacy行仍沿原谓词，无证据的scheduled行仍占用。历史status不伪改为completed/failed/cancelled。

以下位置使用同一有效占用含义：`execution_guard`的turn/outbox/public-task、active context、recovery snapshot、权限busy、interrupt选择、聊天删除检查/claim和schedule workspace删除保护。public-task按原create operation精确关联，不能排除整个conversation。删除既有queued→cancelled逻辑不得改写静止unknown历史，正文清理仍遵守原ADR-0014。

原create/start/interrupt一旦归为静止旧run永久不再派发；现guard对interrupt的豁免须补精确关联保护，避免旧中断误伤下一轮。保留当前真实在途操作的正常中断能力。即使静止后允许后续本地准备，新的run仍须满足授权、目标、session/thread等全部前提，不因解除互斥伪造执行绑定。

### 第四步：一个native owner负责停止与退出

内部生命周期保持最小：`Recovering → ReadyForObservation`；睡眠为`Suspended → Recovering`；退出为`Stopping → Stopped`，超时为`StopPending`并继续正常等待。观察就绪不授予定时派发资格，不为内部状态新增跨仓枚举。

owner持有唯一Coordinator、停止/join任务、受管Host子进程句柄/身份/nonce、系统observer及必要数据库引用。将“请求停止”和“等待完成”分开，不能先take走唯一owner，再让可取消future或Drop abort丢失进行中任务。

1. 在Tauri `ExitRequested`同步`prevent_exit`并关闭新claim/发送，推进生命周期epoch；重复退出请求幂等复用同一收尾任务。
2. 分类并落库已经开始的操作。epoch在claim、每次实际I/O前及跨await后检查，覆盖SSE内部dispatch；已经开始I/O的操作不能被“暂停成功”解释为未执行。
3. 正常停止Coordinator，按现有受管身份正常关闭Host/Runtime并等待真实退出；整合原WorkflowRuntime正常收尾，不借机重做工作流。
4. 超时保留stop任务、子进程身份/句柄、捕获与数据库所有权，进入StopPending后继续观察或再次正常等待。不强杀、不kill-on-drop、不forget子进程，不伪报清理完成。
5. 确认停止后才注销observer、清bridge、checkpoint并释放全部DB worker引用，置exit-ready后允许最终退出。最终Exit仅处理已完成事实。

关闭发送资格不等于立即销毁bridge；Host入口仍存活时可保留必要读取。Host开始正常shutdown后可能关闭HTTP，不能承诺此时继续HTTP恢复；未完成事实持久保留待下一次启动。无法安全退出时保留状态并报告，不强行继续。当前源码无AppHandle.restart调用，本批不新增自动重启承诺。

### 第五步：真实sleep/wake观察与恢复屏障

按固定依赖接入macOS `NSWorkspaceWillSleepNotification` / `NSWorkspaceDidWakeNotification`及notificationCenter，明确主线程注册、回调到native owner、注销和生命周期所有权。Cargo.lock已有transitive `objc2-app-kit 0.3.2`，可按需增加最小direct dependency及Foundation/block相关features，不宣称零依赖变化、不升级整套Tauri。

睡眠通知立即关新发送并推进epoch；唤醒后继续关门，先恢复未知操作、预约及时间连续性，再调用第二阶段有界区间恢复，求严格未来的next_at，不补跑长期离线历史。系统时钟/单调时钟差异只用于保守失连续性补充，不能替代原生事件。测试注入普通时间参数，不修改设备时钟或强制系统休眠。

本批只观察真实睡眠/恢复，不实现设备定时唤醒、OS常驻服务或防空闲睡眠开关。原产品中已接受的本机唤醒/防空闲睡眠控制仍留第四阶段；系统通知延期。

### 第六步：安全验证、自审、报告并停止

| 检查组 | 必须证明的结果 |
|---|---|
| 同源恢复 | Rust生成严格对齐源，bound/accepted条件正确；两个GET不依赖Runtime ready，身份及owner检查保持；缺失/unknown不补投 |
| 格式兼容 | 1—18不改，候选19正常迁移重开；旧聊天/授权/outbox保持，默认15；旧缺证据不自动静止 |
| 结果与互斥 | 精确终态原事务收口；unknown可在可信停止后仅解除占用；无证据/旧legacy仍阻断；同聊天后续turn满足其余前提时可创建 |
| 幂等与防误发 | 重复恢复/释放/取消不重复扣退；旧create/start/interrupt不重发；历史unknown不被删除逻辑改写，scheduled双层禁发保持 |
| 审批 | 当前pending保守阻断，正常处理后继续观察；回调变化本身不充当终态，已有聊天审批/权限回归保持 |
| 生命周期 | 唯一owner、重复退出幂等；StopPending后可正常完成；进程与DB引用不提前丢失；epoch覆盖所有发送位置 |
| 时间与平台 | 普通事件序列验证暂停/唤醒及有界严格未来计算；实际OS observer/正常退出单独列证据，不用纯函数冒充平台验证 |

先审查用例行为，使用普通临时SQLCipher、正常合成事实/HTTP响应、纯状态事件和正常事务检查；不运行含禁止行为的历史全量套件。正常pending/unknown/StopPending输入只验证状态解释，不冒充实际故障或真实Runtime验收。

Contracts执行leaf确定性生成/check/sync、严格源/消费conformance、全仓lint及12登记的适用四基线；Host若仅candidate变化做来源检查和安全只读定向回归。Desktop做相关FEAT-155、原聊天/授权/删除/退出定向检查及fmt/clippy、依赖来源、lint/build/docs build。命令与PASS只能在实际运行后记录，不把历史结果继承为本批通过。

实际macOS退出/sleep-wake检查仅使用已有正常受控运行路径，先证明零模型调用、正常项目构建来源和不接触日常库/Keychain的资格；不造临时第二App、替换Runtime、强制睡眠或强杀来凑验收。若现有入口不能满足条件，明确记**NOT RUN、原因和对实际出站激活的阻断**，保留双层禁发，不以模拟结果通过平台资格。

本批零文本/图片/商家调用；三种目标真实执行、实际Provider恢复/审批及D4继续NOT RUN。报告分别给出代码/合成检查与真实平台资格，不能笼统宣称执行闭环已可激活。元仓strict/D0/audit-claims、lint/test、diff/status与来源摘要收尾，完成后停止。

## 4. 仓库范围与后续依赖

| 仓库 | 3B-2最小范围 |
|---|---|
| Contracts | 现有recovery leaf增加Rust生成/条件校验/Desktop同步与来源；共享语义实际变化时才修权威源，不预铺管理API |
| Desktop | 私有19兼容/证据投影、精确恢复GET、原事实与审批观察、相关占用/删除/中断适配、单owner正常生命周期及sleep/wake监听 |
| Host | 候选来源同步和安全只读检查；现有两GET/正常shutdown复用，暂无业务改写需求 |
| 元仓 | 方案、实际检查/未执行项、来源、状态与停点记录 |
| Runtime/API/Infra | 只读不改，不升级或新增服务 |

3C后续再处理受控实际投递接线、自动occurrence、独立重跑、固定outputSchema草案/确认保存及真实集成资格。任何实际激活仍须先满足本批尚未验证的平台/正常入口资格，不能因3B-2代码报告完成自动放开。受管聊天source-aware标签、页面、应用内更新及防空闲睡眠控制留第四阶段，激活前必要的最小来源展示按13记录接续。

本轮只落方案；旧实施授权不解释为本轮立即开展下一批。未运行生成器、产品测试、服务或模型，未访问日常库/Keychain，未提交/推送/发布或更改分支/远端。文本累计**0/12**、图片0、商家0；允许超过16小时的决定保持，不扩大需求目标。全部Must仍pending，D4 NOT RUN。

本轮方案检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及文档链接/空白检查均实际PASS；81份业务候选摘要保持。最终定向技术复核无必须修改项。这些结果只证明方案和记录一致，不代表3B-2实现或产品验收通过。
