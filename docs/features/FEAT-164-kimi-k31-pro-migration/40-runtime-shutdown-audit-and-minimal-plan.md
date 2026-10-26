# FEAT-164 Runtime 正常关闭审计与最小修复候选

2026-10-26（Asia/Shanghai），S4M。Owner确认39号结果，授权先审计、收敛方案，核心或补丁修改必须另行确认。本轮仅审计/零回合验证/文档，本轮 `contract-impact=none`；没有改变产品、持久化或跨仓边界。拟议修复的增量暂定 **semantic，待方向性验证**；整项FEAT-164继续breaking。

## 结论与证据强度

已定位正常退出的两个生命周期缺口：app-server没有调用已有的 `StateRuntime.close().await`；全局日志层保留发送端，而日志插入任务没有显式停止和可等待的完成句柄。可复现现象不依赖App、Host、旧数据或模型调用。推荐补齐进程所有者的关闭顺序，**不引入主动checkpoint命令、不改变WAL模式、不删除/截断WAL**。

这证明关闭链存在缺口，并为未完成checkpoint提供直接机制解释；没有给原进程做运行时插桩，不能宣称已经唯一归因每一份历史WAL，也不能把可读WAL判为损坏或数据丢失。推荐修复的因果效果仍须同源候选正常退出对照验证。

当前来源仍为39号完整六仓集合：Runtime `a28130abb13d0f99a00107cd513a653bae878b77` / r4，Contracts `1b357cce0575c492f3715b316ee5f254051acf80`，Host `090c2dbeeeceb0fc87e576d8e13f5c339bf106f0`，Desktop `ea9b1e499d86bb92eea360a62707027485790e22`，Connectors `7ea3df41818fd69f4736722d01f0686d584d1a71`，Skills `595c927ae101d3d31c234f60565041eee0864680`。没有重新构建、换可执行程序或启用候选App。源码审计逐文件绑定19份固定源码、6份实际本地依赖源码和当前manifest的10个patch；不是只看未打补丁的上游印象。被永久退役的FEAT-137补丁不在r4链中。

## 真实关闭链

以下行号为固定canonical来源；相关overlay不改变所列关闭函数，0001只修改日志筛选。完整片段/hash见 `evidence/s4m-source-audit.json`。

| 层/所有者 | 实际代码事实 | 判断 |
|---|---|---|
| Desktop `lib.rs:585`、`chat/exit_owner.rs:63` | 退出请求由ExitOwner接管，先停Coordinator/workflow，再等Host和本地存储清理；未完成保持StopPending | 不需要由Desktop直接操作Runtime数据库 |
| Host `cmd/desktop-host/main.go:326`、`internal/codex/runtime.go:643` | 停HTTP准入/市场broker，关闭Runtime stdin；有界等待到期转正常持续等待，Runtime未退出不释放管理权 | 延长Host时间不能让已结束的Runtime补做close；现有正常等待机制可以承接修复 |
| Runtime stdio transport `stdio.rs:69` | stdin EOF发布ConnectionClosed | 本轮确认实际走此路径，未发进程信号 |
| app-server `lib.rs:1014,1156` | last_connection_closed → RPC shutdown → connection cleanup drain → background drain → thread shutdown | 前两类等待存在；后两类默认10秒超时后仅警告并继续，不构成所有写入者已退出证明 |
| session `handlers.rs:628` | 正常Shutdown调用live_thread.shutdown排空线程持久化后发ShutdownComplete；`session/mod.rs:807`等待session loop结束 | 会话持久化关闭不等于整个StateRuntime关闭；不得破坏此顺序或提前关池 |
| app-server `lib.rs:1178` | await processor/outbound → cancel transport token/await accept handles（包括remote control）→ otel shutdown → Ok | 没有log queue shutdown/join，也没有state_db.close；process exit=0只证明进程结束 |
| 日志 `state/src/log_db.rs:132,402` | tokio::spawn(run_inserter)的JoinHandle被丢弃；任务持有Arc<StateRuntime>；只有全部sender消失才收None并末次flush | 全局subscriber持有sender clone，不能靠函数局部drop证明任务自然结束；单次flush也不阻止之后继续入队 |
| `StateRuntime::close` `runtime.rs:330` | 依次等待memories、goals、logs和state四个池关闭 | 已有可复用入口，不需要引入数据库迁移/新的checkpoint引擎 |
| `runtime/logs.rs:295` | 仅logs启动维护执行PASSIVE checkpoint | 不负责退出闭环；其余池不因此完成checkpoint |
| SQLx0.9.0 | Pool.close等待连接归还，并等待SQLite worker关闭；worker关闭连接后应答。pool内部丢弃逐连接close错误，API返回unit | 必须await，但不能把unit返回值当作磁盘checkpoint成功回执 |

in-process API的StateDbHandle由调用者传入且可能共享，不能在通用MessageProcessor析构时擅自关闭它。本轮推荐仅由易界使用的**独占stdio app-server进程所有者**执行最终关闭；不扩大到TUI/嵌入式、WebSocket/daemon或强制信号退出策略。远程控制accept task的正常取消/等待保留。已有状态初始化backfill gate是await完成后才返回，不是本次遗漏的后台backfill句柄。

SQLite正常最后连接关闭通常负责checkpoint；WAL本身可能包含已提交内容，存在并不表示损坏。外部读者、持久WAL设置、I/O问题等都可能影响文件形态，不能以“文件一定为空”作为通用断言。此处以本地固定SQLite/SQLx源码为实现依据，并核对[SQLite WAL文档](https://sqlite.org/wal.html)、[连接关闭语义](https://sqlite.org/c3ref/close.html)、[SQLx0.9.0 Pool.close](https://docs.rs/sqlx/0.9.0/sqlx/struct.Pool.html#method.close)。正常SQLite自身关闭清理与手工删除WAL是不同动作；本方案不追加删除命令。

## 一次有区分力的安全验证

实际执行现有r4 binary（SHA `3821bb6063825bdb0e30e367757117f7b3bc9bca84f0275cbdef9e9c660e1e5f`），全新 `feat164-s4m-audit-20261026/credential-free-home`；文件式空认证，无密钥环境，模型地址只指向本机，关闭hooks/plugins/apps/shell snapshot/analytics/feedback/remote control。仅发送initialize/initialized，随后一次正常EOF；没有thread/start、turn/start、工具、标题、辅助请求或Provider重试。真实模型HTTP **0**，未打开用户数据库。初始化成功、exit0，EOF后约0.004秒退出；trace为last_connection_closed、shutdown_forced=false及outbound退出。

| 新审计库 | 正常退出后WAL字节 | mxFrame / nBackfill | 完整副本只读integrity_check |
|---|---:|---:|---|
| state_5.sqlite | 1,322,552 | 321 / 0 | ok |
| goals_1.sqlite | 45,352 | 11 / 0 | ok |
| memories_1.sqlite | 61,832 | 15 / 0 | ok |
| logs_2.sqlite | 无WAL | 不适用 | ok |

这不是修复后的PASS。日志库本次未留WAL，说明不能把所有库/每次退出都写成相同结果。原候选三份WAL的S4L证据保持。S4M新增发现要求验证覆盖**四池**，包括即使业务记忆未启用也会初始化的memories库；这不授权启用记忆功能。

DB+WAL+SHM仅复制到新的完整快照再用mode=ro/query_only检查，原新审计库三类文件检查前后hash一致；未执行PRAGMA checkpoint/VACUUM、强制结束或清空文件。新审计目录及WAL继续保留，不提交数据库。原候选、日常库及两份账本完全未打开写入。详见 `s4m-normal-eof-result.json` 和留存的driver/config。

## 最小方案选择（待Owner确认）

| 方案 | 内容与取舍 |
|---|---|
| 只在末尾flush + close | 改动少，但flush之后仍可能有日志入队；线程10秒超时的未完成写入也可能被关池影响。不能满足本次完整关闭证明，不推荐 |
| **推荐：所有者有序关闭** | 保留正常入站停止/线程持久化顺序，明确写入任务完成，关闭日志准入并排空/join，再复用StateRuntime.close；修复责任边界，无主动checkpoint命令 |
| 暂不修改Runtime | 保留完整DB/WAL作为合法恢复状态，可继续只读审计；当前checkpoint验收持续未完成，不可据此升级teardown为PASS |

推荐补丁暂名 `.yijie/patches/chat-models/0011-feat-164-graceful-state-close.patch`，追加于当前十补丁之后，独立r5候选路径；**文件尚未创建，核心尚未修改**。固定上游、原十patch、历史产物、schema/migration/模型出站/批准策略全部保持。最小行为设计：

1. 在独占stdio进程保留日志停止控制句柄与StateRuntime最终所有权。保持停止新请求、RPC和连接任务排空、会话rollout正常shutdown、outbound与transport完成的先后关系。
2. 复用已有TaskTracker、thread shutdown report及 `wait_until_terminated` 等原生等待能力，将正常stdio关闭的“10秒后警告继续”改为**仅报告仍在清理并保留等待任务**；超时不能取消被等待的关闭future、重复制造Shutdown或宣称写入者退出。只为stdio增加专用内部等待路径，不全局改动其他调用者的有界关闭行为。若发现需修改core/thread_manager等更大共享生命周期，停止并另报范围，不能把它隐含在本次授权内。
3. 为LogDbLayer提供显式、clone共享且幂等的shutdown：关闭receiver准入，排空已经成功入队的Entry/Flush，等待插入任务结束。全局subscriber可以保留，shutdown后的事件不再进该数据库；普通运行的非阻塞try_send/既有满队列丢弃策略及0001隐私筛选不变。不能只drop一个clone、sleep两秒或abort inserter。
4. 明确传播日志排空的结果：当前insert_logs错误被忽略，shutdown不能据此伪报flush成功。仅增加内部结果/固定脱敏诊断，不输出日志正文、SQL、路径、凭据或新增public DTO；不引入模型/网络重试。失败仍保留全部文件，结果不通过。shutdown后继续保留stderr诊断，不向已经关闭的SQLite递归记录错误。
5. 所有生产者及日志任务已正常完成后调用已有 `StateRuntime.close().await`，覆盖memories/goals/logs/state；保持WAL和synchronous NORMAL。close等待期间不超时drop，不注入TRUNCATE/RESTART/FULL/PASSIVE命令，不删文件。不将void返回值映射为checkpoint PASS；通过退出后证据独立判断。
6. 对普通初始化后早返回/错误退出复用同一所有者清理出口，先确认已有任务状态；不修改上游损坏库恢复策略、不主动制造损坏/权限故障。对本轮未覆盖的异常/强制退出不扩权、不声明验收通过。

拟改实现面仅 `app-server/src/lib.rs`、`message_processor.rs`、`request_processors/thread_processor.rs`、`state/src/log_db.rs`，加对应安全单元/集成测试和canonical patch/build/check/manifest治理文件。`StateRuntime.close`主体原则上复用，不改存储schema或SQLx依赖。不在Host/Desktop加外部checkpoint补救；下游只做必要的精确来源更新与安全兼容验证。实现若超出该面、影响共享in-process所有权、需要新公开字段/依赖/数据库策略，应停止重新确认。

## Contract First、验证与停止条件

先形成Runtime最小patch/replay与不可变r5 source → canonical build/schema比较 → Contracts兼容投影与来源锁 → Host精确pin/conformance → Desktop实际media/expert组合pin及同源build → App正常退出/重开。拟议增量semantic是因为正常stdio退出完成条件可观察，JSON形状不变不能写none；若方向性检查发现支持消费者失效则升级breaking。整体FEAT164已是breaking，不降级。269个canonical schema及其digest必须实际比较，不先填写零差异；发生wire差异立即停止重新审方案。

验收分开执行，不能用静态断言或文件大小单独证明关闭：

- **日志所有权**：普通合成日志、多个layer clone仍存活时可正常shutdown，停止边界前已接纳项持久化一次，旧Flush等待者收敛，后续事件不重开池；重复shutdown共享完成结果。用正常有限任务覆盖并发，不通过强杀/坏权限/攻击载荷造错。
- **等待顺序**：普通有限后台任务和会话正常中断/退出，证明未完成写入时不关池，10秒诊断不丢任务；不反复重发业务或Shutdown。纯结果分支可安全单元验证，不破坏数据库来制造错误。
- **四池关闭**：新隔离合成home，在不发模型回合的同样初始化/EOF对照中检查全部四库，等待真实进程退出、无句柄；完整DB/WAL快照只读完整性及已提交记录一致。WAL存在时继续检查活跃帧与主库持久结果，不手工消除。依旧未backfill则保持FAIL/NOT RUN，回到RCA，不追加checkpoint“修绿”。
- **实际下游**：正常loopback文本/原生取消、保存、退出、同源重开零补发，旧操作/unknown/计划授权不变；本轮真正未跑，修复获准后才实施。锁屏时App/UI可延期并如实NOT RUN；不影响无UI源码/EOF检查。
- **兼容**：r4历史由r5读写保持原失败事实；r5不引入新格式的假设须以diff和方向性验证证明。in-process共享句柄不得被stdio关闭路径误关，未修surface不得冒称已验收。

不重跑与新假设无关的141项全量检查充当进展；先focused修复测试、canonical资格及受影响边界，再做必要新鲜组合验证。单次正常EOF对照发现持续问题即停做RCA；累计三次同点失败按长期规则熔断。超时/挂起保留进程和数据，只使用正常退出，不能强杀。

新r5会使涉及Runtime来源的旧r4资格/证据失效；38号真实文本G2V只能保留为r4历史证据，**不能自动重标成r5 PASS**。后续如何完成r5的真实G2V须另审，当前授权仍是0新增模型HTTP，不能因修复或30元上限余额而调用。整项S2/S3自然旧K3 App迁移/计划重新授权、S4完整TCONF04、core最终及日常切换仍在清单，不由本修复替代。

回滚默认停止r5激活、保留其同源兼容reader和全部DB/WAL；无schema/历史写格式变化只有在方向性验证后才能允许退回匹配r4组合。不得回退r2旧writer、降库或复制覆盖用户数据。r4旧制品保留；此方案不授权日常入口切换、推送、发布或真实调用。上游未来提供等价日志join和状态池关闭且全部兼容验证通过后，方可移除该补丁。

## 本轮完成、未执行及确认点

已完成：19份源码/10patch/6依赖来源核对、一次零回合正常EOF复现、4库完整副本只读完整性检查、候选修复与验证/回滚方案。没有产品修复、构建或App验收；无UI操作，锁屏不影响本轮。保护记录与治理检查见s4m evidence。

本轮只更新治理记录并仅本地提交。当前G3/S1及r4视觉子集结论保持；core和teardown仍NOT RUN，S2—S4/完整FEAT164仍IN_PROGRESS。旧账本和14.188544元预占保持，累计5/5真实HTTP已用、保守14.679001元不变。

请Owner确认上述**所有者有序关闭最小方案及四文件实现面、独立r5候选、Contract First必要下游来源更新和零真实模型安全验证**后再实施。确认原因来自本轮用户“涉及核心或补丁修改先提交方案确认”及 `yijie-codex/AGENTS.md`「是否修改Runtime核心…」「是否新增补丁…」须先确认；既有子代理终态修复授权不被扩张。此次不是申请新模型额度或日常迁移。

本轮实际治理检查：claims、strict、元仓lint、53项元仓测试和7份Shell语法均通过。497份既有dirty以及7643份原证据/资源/日常与候选数据/制品文件hash保持；全部Gate/final/Owner approval/freshness/预算字段与071c2c2相等，仅追加待确认审计项。未重跑已知未满足的G4来制造新结论。
