# FEAT-155 3C-1 实施报告：受控手动投递接线

2026-09-18。用户明确要求按[17方案](17-phase-3c-1-implementation-plan.md)只实施3C-1，完成零调用组合验证后报告停止。本批已完成候选源码和安全定向检查；没有进入3C-2、草案或页面。

**结论：候选手动链已接通，普通入口仍schema15、scheduled默认禁发。** 候选测试经过实际native服务、原worker/Coordinator/HostBridge及进程内HTTP声明响应，不是真实Host/Runtime/Provider或macOS平台验收。真实激活资格继续NOT RUN，全部Must仍pending、D4 NOT RUN。

## 1. 范围与来源

本批`contract-impact=breaking`：新增Desktop私有schema20及native投递/重放解释。旧19 reader不能打开20，因此回退须保留支持20的reader并关闭writer/dispatch，不做降级、删表或日常库迁移。共享HTTP/IPC/JSON Schema及固定Runtime未变，没有新增公共字段、影子DTO、依赖或服务；不需要为私有字段改变Contracts wire。

五仓HEAD、分支与远端保持[16](16-phase-3b-2-implementation-report.md)记录；开工前96份候选摘要逐项吻合。新[来源证据](evidence/phase-3c-1-source-20260918.json)含99份候选，本批仅Desktop的15份文件变化（12份既有文件、3份新增）；Contracts、Host与Runtime源码/来源锁保持，Runtime clean。全部是未提交local candidate，不是发布pin；无提交、推送、分支/远端修改或发布。

## 2. 实现结果

| 项目 | 已实现行为 |
|---|---|
| native候选准入 | 明确的内部`start_schedule_dispatch_candidate`绑定当前NativeAuthRuntime；日常构造、CompatibleReader及单选DispatchFoundation均不具备发送权。没有renderer command、环境变量开关或数据库激活位 |
| schema20 | 仅增加create/turn不含正文错误码及native_claim证明。claim证明由新native事务写入，旧记录默认0；它不能单独赋予发送权。旧1—19迁移字节不改，普通迁移目标15，reader上限20 |
| 授权与额度 | claim与真正I/O前重验当前scope/能力、grant期限/revision、计划revision/epoch/摘要、目标、Ask和关联。发送本run只验证已预约额度，不二次扣额；占满最后一额仍能执行本run，其它新请求拒绝 |
| 互斥 | 只豁免当前run精确关联的reservation、turn、create/start和public-task；其它前台、unknown、删除和待审批继续阻挡；已静止旧interrupt仍不可发送 |
| 目录及三目标 | 原创建路径按native来源解析用户bookmark或受管目录，发送前复验路径及hash。专属聊天首次绑定后复用、每次新聊天保留独立关联、已有聊天保持原session/目录；不换目标或伪造书签 |
| 原执行链 | 同一个Coordinator和HostBridge。scheduled的public-task阶段强制复用原native local适配，文本沿原permission-turns Ask；不走legacy v1、不新增发送器或队列 |
| 最终I/O边界 | Host ready/token/身份await后检查精确会话的执行/审批，再回worker事务重验当前授权、目录和epoch，记录该阶段attempted/sending，最后复验epoch。首次create无Host session时不要求不存在的同会话审批 |
| create恢复 | 精确bound映射与正常create共用原事务helper，完成原create并幂等接续原turn operation。重复恢复不建第二聊天/run、不同步再次扣额；reserved/404不能推进 |
| 尝试/错误/接受 | never不作无意义回执查询；attempted/旧unknown从不租期重POST。原聊天与run接受/错误状态同事务落库。标记前受阻保持未发并有限间隔复验；标记后的错误/未确认保留unknown、占用和额度 |
| 取消与释放 | 有native_claim证据且两阶段均never时，本地claim计数/本地public绑定不冒充出站，可一次取消/退款；旧记录仍需原严格证明。任何attempted/unknown或已远端create均不退款。可信终态/正常停止释放保持3B-2规则 |

请求幂等回执不授予新的出站权。已授权paused计划可显式手动执行；计划编辑、撤销或目标失效阻止后续I/O，旧grant过期不阻止必要的只读恢复。SQL提交与网络POST不是跨进程原子事务；attempt标记后只保守恢复，不通过抹除标记重发。

恢复另区分“create已确认、原turn从未发送且本run授权仍有效”与未知执行：前者保留下一阶段，不因旧Host正常退出就错误静止；发送本身仍须单独取得candidate权限及全部资格。实际已尝试turn的未知历史继续按可信停止证据解除互斥，保留unknown结果和额度。

不含正文错误码属于私有恢复事实，未塞进public-task的bound状态或冒充native终态。普通接受/旧聊天路径保持，自动occurrence、独立重跑、草案、页面、防空闲睡眠开关及系统通知均未加入本批。

## 3. 实际验证

| 检查 | 实际范围 | 结果 |
|---|---|---|
| FEAT-155安全集合 | `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture`，本次输出producer | **57/57 PASS**：新增12项组合检查，前序45项保持 |
| 旧链回归 | 17项exact迁移/聊天/授权存储/native观察/正常关闭检查，加authorization模块2项；完整名称与日志见来源证据 | **19/19 PASS** |
| 最终恢复修正 | `feat155_3c1_mapping`及`feat155_3b2_stopped_unknown`各实际运行1项 | **2/2 PASS**；发生在57项集合之后，覆盖最后的恢复分类修正 |
| Rust静态 | `cargo fmt --manifest-path src-tauri/Cargo.toml --check`；`cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings` | PASS |
| 实际Rust输出 | 未变的Contracts plan/execution/recovery checker，检查本次四份producer | 全部strict conformance PASS |
| Desktop | `pnpm lint`、`pnpm build`、`pnpm docs:build` | PASS；保留既有chunk大小提示 |

新增12项组合检查覆盖：

1. 三目标、专属复用、请求幂等、最后一额、耗尽后拒绝新增run及Ask出站。
2. writer/reader默认禁发，显式native候选之外零POST。
3. pending审批阻挡；正常处理后仍用原操作首次发送、不重新扣额。
4. 已尝试拒绝/404不重投、不退款，保留unknown和私有错误原因。
5. ready await期间睡眠事件关闭资格，保持never且无POST。
6. 原Coordinator实际启动、原生SSE终态同事务释放并正常stop/join。
7. 正常旧代次结束后的bound映射恢复，幂等接续原turn，仅一个POST。
8. ready await期间grant到期，最终原生校验阻止I/O。
9. 编辑、Ask变化、目标失效及其它outbox占用分别阻止claim。
10. 正常20重开不继承内存发送权，15旧聊天前向到20及再重开保持。
11. native claim/本地public绑定后完整never的取消、一次退款和占用释放。
12. 已有用户bookmark项目按原路径/session实际走组合投递链。

所有数据库均为正常临时SQLCipher，token/身份/数据为测试专用合成值；HTTP仅在进程内loopback提供普通协议响应，没有启动真正Host/Runtime/Provider。SSE和原生read是协议组合证据，不是模型运行或真实系统事件证明。没有强杀、权限破坏、攻击注入或可执行文件替换。

本轮未修改Contracts/Host及生成源，因此不重跑未变源的生成、整仓lint、四基线或Host业务测试；16的历史结果保持为历史，不改写为本轮执行。未运行包含用户禁止fixture的历史全量套件，不声称全仓测试通过。

四份本次实际输出分别为[plan](evidence/phase-3c-1-plan-native-producer.json)、[execution基础](evidence/phase-3c-1-foundation-native-producer.json)、[本地准备](evidence/phase-3c-1-preparation-native-producer.json)、[恢复类型](evidence/phase-3c-1-recovery-native-producer.json)。这些输出只证明对应生成类型的一致性，不替代新链组合检查。

## 4. 失败修正与自审

- 初次编译修正目录resolver的chat内部可见性、Admission新增参数及测试内部接口引用；clippy移除多余借用和Copy类型的clone，没有放宽规则。
- 第一轮组合检查发现create请求使用flatten的request_id，本地准入误按嵌套trace读取，已按实际请求类型修正；默认禁发的反向检查始终保持。
- 组合夹具修正native snapshot字段名、恢复404的canonical错误对象及task与conversation不能混同的身份；完成观察改走原恢复/stream链，不把只读UI历史当作完成证明。
- 全集合运行时原Coordinator可能先经正常恢复read完成，导致原SSE专项断言不稳定；该用例改为声明非终态read、再由普通SSE给出终态，确定地验证指定路径，不延长超时掩盖问题。
- producer收集初次未提供recovery专用输出变量，随后checker工作目录也不正确；按原测试输出入口和Contracts工作目录执行后通过，没有重写producer或validator。
- 结构化自审补齐旧静止interrupt的占用解释、never与attempted的错误投影区别、最终目录/请求身份校验、native claim证明及候选public-task强制local路径。最后补“已确认create后的有效never turn不能被旧代次停止证据提前释放”，并完成两项定向复验及all-targets clippy。

本轮未使用子agent；技术自审不等于独立人工批准。保持原授权和用户规定的批次停点，不扩大为自动调度、页面或通用计费/授权框架。

## 5. 未执行项与停点

| 未执行项 | 原因与影响 |
|---|---|
| 真实macOS sleep/wake、窗口退出与Host/Runtime进程链 | 本批不启动App；既有正常入口的平台/数据边界尚未完成实际资格，NOT RUN，继续阻断日常激活 |
| 真实Provider审批、恢复、三目标业务执行 | 本批零真实调用；当前组合测试不能替代Provider与正常产品入口证据，NOT RUN |
| 日常用户库、Keychain及实际writer激活 | 本批只用临时数据，普通入口目标15；不访问、复制、重置或迁移日常数据 |
| 自动触发、重跑、固定草案/typed IPC、页面及唤醒开关 | 后续3C-2/3C-3与第四阶段，本轮未实施；系统通知继续按既有决定延期 |
| 禁止行为的历史测试 | 遵循用户长期安全条款，采用正常合成状态/协议检查，未执行且不冒称通过 |

文本累计**0/12**、图片0、商家接口0；全部Must仍pending、整体FEAT-155仍in_progress、D4 NOT RUN。**3C-1候选实现和定向检查完成后停止，不自动进入3C-2，不解除普通入口禁发。**

本轮元仓strict、D0、audit-claims、lint、50/50治理测试、Shell语法、五仓diff及96处链接/空白检查均PASS；99份候选、4份producer和19份旧迁移摘要复核一致，HEAD/branch/remote保持，Contracts/Host/Runtime未变。D0仍只表示既有产品/设计批准，不是实际激活或D4通过。
