# FEAT-164 S4N 深入复审：静态检查通过不等于关闭链完整

2026-10-26（Asia/Shanghai）。Owner已批准40号四文件最小方案、独立r5和Contract First下游安全验证；随后明确要求深入分析未通过原因、修正前再次审计、然后执行。依此暂停后续实现/构建，已启动的资格命令正常结束；本报告完成再次审计并界定下一执行的准确范围。

**结论：lint阻塞已解除，但当前四文件候选还不能晋升。新发现listener终止没有可等待证明，且RPC等待的插入位置需修正；不能把12项静态单元绿色等同r5正常退出/checkpoint通过。** r5 binary没有构建，Contracts/Host/Desktop没有改动，本轮没有真实模型HTTP。

## 三类“未通过”及原因

| 层级 | 当前事实 | 根因/未证明事项 |
|---|---|---|
| 编译与lint | 首次unit编译有两个测试Mutex类型冲突；修正后4项、后续6项分别通过。Clippy连续三次101，熔断/RCA后一次fresh资格已exit0 | 初始设计跨await持tokio MutexGuard；随后Option冗余闭包、crate禁止eprintln。过程原因是未预先完整核对workspace/crate lint；不是模型/数据库/平台故障 |
| Runtime关闭修复 | 当前patch fresh replay、6项新unit＋6项纯RPC gate unit、两package Clippy -D warnings通过 | 只证明已测源码行为。未构建r5、未跑loaded-thread EOF，缺listener任务生命周期证明，不能PASS teardown |
| 整项FEAT164 | 仍IN_PROGRESS | 自然旧K3 App迁移/恢复取消、旧计划重新授权、完整S4/TCONF04/core及日常切换仍缺；新Runtime还会使相应旧来源证据过期，当前真实调用授权0 |

三次lint原日志、时间与修正分析见 `s4n-lint-rca.md` / `s4n-lint-failure-timeline.json`。熔断后没有关闭lint：独立join owner等待日志worker，watch共享结果替代跨await锁；Option::is_some替代冗余闭包；固定错误通过既有tracing stderr层输出，已关闭的日志receiver不再入库。此前成功的Mutex版unit不冒充watch版；只有 `s4n-canonical-source-requalification.log` 的6+6及Clippy对应当前patch。没有第四次机械试错，已先记录RCA/核对完整策略，再执行一次收敛资格。

## 再次审计发现

### R1：listener仍然脱离关闭所有者（实质缺口）

固定来源 `thread_lifecycle.rs:277` 直接tokio::spawn listener，未保存JoinHandle或登记可等待的tracker。它持有conversation、thread manager、outgoing等，能执行已排队的历史/resume/goal查询及idle lifecycle回调；例如 `thread_lifecycle.rs:681–697` 读取StateDbHandle并触发生命周期通知。不能未经证明把所有listener视为无数据库影响的只读展示任务。

`thread_state.rs:120` 的clear_listener发送cancel、清发送端，`clear_all_listeners:424`遍历调用它，**没有await listener退出**。当前四文件patch甚至未覆盖这些spawn入口；StateRuntime.close会阻止新的池获取并等待已借出连接，但不会自动等待尚未开始数据库操作的listener队列。因而可能使尾部工作遇到PoolClosed，或依赖Tokio runtime teardown取消未结束任务。这里是源码证明的生命周期缺口和风险，不是已经观察到用户数据丢失。

当前新测试验证了日志clone/flush/结果、四池受控关闭和有限后台等待，RPC六例只测gate本身；都未建真实loaded-thread listener。这解释了为什么测试全部绿色仍不能证明修复完整。S4M零回合初始化EOF根本不建立会话listener，后续不能只重复该用例收口。

### R2：等待必须放在能让任务完成的位置（顺序风险）

新增 `connection_closed_stdio` 把无限RPC等待放在原connection_closed资源清理之前，而上游原有顺序是有界RPC等待后继续正常连接清理。单纯删超时/前置无限等待可能阻止清理动作解除正在等待的任务；六个gate单元不会发现这种跨对象依赖。本轮没有运行命令进程或制造挂起，**不把源码风险写成已动态复现的死锁**。

修正原则是保留原正常连接清理，完成准入关闭和必要的正常解阻动作后，再加入最终RPC完成屏障；不靠超时假定成功，也不擅自改变command/process终止策略。涉及那些独立管理器自身行为的变更须另报。不能以新的强杀、重复Shutdown、假终态或覆盖历史来解决等待。

### R3：附带遗漏与反例

- 新stdio thread shutdown应在真正终止后移除已完成线程，复用既有remove_thread能力，保持原Manager的成功移除语义；未完成不得提前移除。当前代码仅等待未移除，需纳入修正。
- 各级join结果和日志typed failure不能被转换为成功；StateRuntime.close返回unit不是checkpoint完成证书。
- 旧构建smoke使用TemporaryDirectory，退出时会清理整个测试home；新r5应改用保留完整home/DB/WAL/SHM的正常EOF验证入口。旧smoke不改、不执行于本轮r5。
- in-process由调用者提供共享StateRuntime；禁止把本方案推广成通用析构自动关池。仅独占stdio所有者触发最终关闭。
- 不用松动断言、修改WAL/SQLite策略、主动checkpoint或文件删除补救。旧账本、旧unknown预占、当前候选数据与日常库保持。

## 收敛后的最小范围调整（尚未实施）

推荐保留40号四个实现文件，再**仅增加两个实现文件**：

1. `codex-rs/app-server/src/thread_state.rs`：由现有ThreadStateManager管理每个实例的listener注册/任务跟踪与正常停止等待。复用已有TaskTracker和正常cancel，不设全局static所有者、不改DB/schema/协议。
2. `codex-rs/app-server/src/request_processors/thread_lifecycle.rs`：将已有listener spawn登记到上述所有者；无新listener业务逻辑，不改变正常事件处理顺序。覆盖所有调用方已有的ThreadStateManager引用，避免新建另一套listener或仅修改一个启动入口。

合计六个实现文件，相关测试与canonical patch/build/check/manifest文件仍属40号验证范围；不修改core/thread_manager、turn_processor、command/process管理器、权限、模型调用或公共DTO。若事实证明六文件仍不足，停止重新审范围，不能静默扩张。

**准入和等待设计必须成对**：TaskTracker.close本身不禁止新spawn。注册需要与关闭标志原子协调；先关闭新listener准入，等待已开始的注册完成，再发送现有正常cancel，等待listener任务结束。已登记的注册不能在clear快照之后再悄悄启动漏网任务。不得持有MutexGuard跨await，不通过abort结束listener；重复关闭共享完成结果。

stdio最终顺序建议：停止接收新工作 → 原连接正常清理/解除等待 → 最终RPC drain → thread-start后台任务排空 → core会话正常Shutdown/持久化并确认终止、移除已完成线程 → 停listener注册与任务、等待实际退出 → outbound/transport结束 → 日志停止准入/排空/join → await四池close。各阶段确实完成才进入下一阶段；诊断超时保留等待和所有权，不能等同完成。早期错误按已启动资源进行正常清理，不能把未启动阶段假写成已关闭。

## 可证伪验证与执行顺序

先完成本次方案/范围审阅，再允许修改，不在审批期间写第五/第六个文件。

1. 安全单元：listener正常完成、正常cancel、重复关闭、已开始注册与关闭并发、关闭后不接纳；确保没有持锁await，测试使用普通有限任务/通道，不强杀、不造坏库/权限/攻击fixture。增加RPC正常清理后最终等待的顺序检查，不启动外部命令制造阻塞。
2. 保留6项日志/四池/等待及6项RPC检查，fresh replay和同等Clippy。新差异使先前patch资格过期，不借旧PASS。
3. 独立r5 canonical构建后仅一次有区分力的留存home检查：initialize + 原生thread/start/read（零turn、零模型HTTP）+ 正常EOF；确认真实listener退出、四池关闭、进程/句柄释放及副本一致性。出现未回填帧/未知关闭状态即停，保留所有文件；不再自动修改或重跑。
4. Runtime不可变来源/schema比较 → Contracts投影 → Host → Desktop精确pin和安全边界/同源构建；真正App验收锁屏可跳过并记NOT RUN，不能代写PASS。
5. r5未获真实G2V、完整core及日常切换许可；5/5已用、保守14.679001元含14.188544元unknown预占保持。没有额外真实模型调用。

回滚：当前四文件候选尚未提交/构建/激活，原patch、失败日志和资格结果完整留存；r4 binary及所有下游来源未变。新候选失败只停止晋升并保留数据，不降库、不用旧r2 writer，不清WAL。

## 本轮实际执行与等待点

按用户最新要求已经完成扩大只读审计，并让已启动资格命令正常退出；没有启动r5构建、没有实施第五/第六文件。canonical上游字节未改，现有四文件实现仅作为0011候选patch和临时构建源码保留。新增真实模型HTTP为0，没有App/UI、没有进程信号。

当前四文件修改授权仍有效，**六文件调整未批准**。40号明确“超出四文件另报”，加上Runtime AGENTS的核心/patch确认要求，需要Owner确认新增 `thread_state.rs` 与 `thread_lifecycle.rs` 才能完成这条关闭链。请求的是范围调整，不是重问已批准的预算/本地提交。没有把审计发现改成整项通过，也不把文档提交当作实现交付。

本次再审治理复核：claims/strict、元仓lint、53项测试、7份shell语法通过；497份原dirty和7643份原证据/资源/候选及日常数据/制品字节保持。canonical Runtime无diff、新增两文件未改、r5目录尚不存在。已有四文件候选及失败证据完整保留，尚不提交Runtime源码；仅元仓审计与治理记录本地固化。

两份早期unit日志的提交副本仅去除末尾多余空行以满足Git文本检查，原始日志完整保留；前后hash及字节数见s4n-log-normalization.json，未修改任何结果或重跑测试。
