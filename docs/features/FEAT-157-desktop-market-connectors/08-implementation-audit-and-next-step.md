# FEAT-157 当前实现审计与下一步执行

> 后续进展见 [09 私有 Broker 控制实施](09-broker-control-implementation.md)：本文第4节前两项已完成内部实现与真实 Runtime 本地资格；Native/Host 产品发送与审批接线仍待完成。下文保留本次审计时的事实。

2026-10-07。用户要求“根据当前实现，认真审计实现后，给出下一步执行方案，并开始执行”。本记录承接07，审计与执行均在本地候选工作区进行；整体仍为 active，D4未完成。

## 审计结论

目录、安装管理、生成协议和基础权限不是空页面：Native已有真实SQL事务与幂等回执，UI调用真实Native管理接口。相同scope的权限租期续期保留未确认操作，旧generation不会恢复有效连接。当前非空选集在UI和Native都被阻断，worker仅查询未资格状态，因此没有发现已经激活的市场工具越权执行或平台凭据泄漏路径。

不过，这仍不是51项MCP接通。通用执行控制、Host版本化提交、真实授权、审批投影和结果显示都尚未接线。不能通过把executionAvailable改为true绕过这些缺口。

### 已确认的实现问题

| ID | 级别 | 原问题与影响 | 本轮处理 |
|---|---|---|---|
| A1 | P2 | 卸载IPC尚未返回或返回pending时，模态框同时禁止关闭/Esc/遮罩，且无查询原操作入口，用户无法离开 | 已修。关闭窗口不取消操作；pending/unknown可查询原回执，有权限且cancellable时才提供取消 |
| A2 | P2 | worker查询在等待锁或进入时已经取消，仍可能校验并启动一个进程 | 已修。排队等待响应取消，锁后及spawn前复核ctx |
| A3 | P2 | MarketFoundation.Close只等待旧进程，关闭后查询仍能创建新worker | 已修。Close先永久关闭准入，随后正常等待；STOP_PENDING保留owner，不复活、不强杀 |

定位：Desktop `src/components/connectors/ConnectorMarketView.vue`；Connectors `internal/worker/worker.go` 与 `internal/app/market.go`。修复测试使用普通deferred请求、正常pending状态、预取消和真实canonical worker；没有故障强杀或伪装程序。

### 继续实施前必须补齐的设计

1. **创建操作不等于首轮发送操作。** Native的`create_session_and_enqueue_in_transaction`另生成首轮turn operation。选择摘要必须使用这个真实编号，不能由renderer提前用创建operation计算。首次创建的两个操作必须关联同一冻结快照。
2. **完整请求和选集是两种摘要。** 选集摘要用于跨边界关联；Native完整意图HMAC还需覆盖scope、创建/续轮目标、原始工作空间意图、有序正文/附件、模型和refs。短期context/requestId不进入意图。同operation不同意图冲突；新family不得接管旧outbox/turn/model已经使用的operation。
3. **已有审批是Sorftime专用表面。** Host elicitation目前进入固定Sorftime handler；旧runtime permissions投影也仅支持该单工具。通用market调用要独立版本化，不能扩宽旧枚举或猜最近Tool Item。
4. **空选集与回退必须覆盖全部旧路径。** claim之外，还要隔离耗尽处理、权限恢复、直接dispatch加载、旧writer和resume。支持SQL31但关闭market的新reader保留新记录；真正只支持SQL30的旧binary必须拒读，不能声称任意旧版本可回退。
5. **优先复用现有环境隔离。** 固定Runtime默认继承环境并不安全；Host已实现core/exclude/set-empty的受管配置。新内部数据面能力可复用该机制，不能复用Sorftime平台secret分支，也不能把bearer本身当作工具批准。

原有模型/正文/附件回放已有实际校验，审计没有把它误报成“改正文也成功”的漏洞。新wrapper是在此基础上增加自身归属及完整意图约束。

## 执行方案与当前完成情况

### 1. 修复已确认缺陷 — 已执行

完成A1–A3，保留原管理与worker协议。worker完成通知改为广播，使查询与关闭共同等待同一次正常退出，不争抢退出结果。

### 2. 契约先行，冻结提交选集 — 已执行本地实现

Contracts新增独立`market-selection/1`，复用原SelectionRef与模型ProfileId；旧55定义/9个管理IPC保持。新Native命令为`chat_market_submit_v1`，回执显式标记`local_durable_accepted`，区分submissionOperationId、turnOperationId和localTurnId。摘要编码及共同向量由同一源生成Rust/Go/TS投影；不复制手写wire DTO。

该Native-only family的唯一wire源为Contracts `compatibility/market-selection/wire.schema.json`，命令元数据为共址`native-ipc.json`。它不伪装HTTP API，也不留第二份shadow source；独立source-loader严格核对本地引用，Makefile与Desktop主check均注册检查。迁移源位置后全部生成类型/validator/摘要向量逐字节不变，旧pinned generator未改。

Desktop新增SQL31及`connectors/selection.rs`：

- 原子保存message/outbox、模型、选集快照、Native目录名称快照及回执；首轮的create/turn两个别名不依赖尚未生成的turn outbox外键。
- 复用已有ReceiptKey计算完整意图HMAC；同scope、同意图先回放原回执，不因随后卸载/代际变化重写它。
- 无本family记录但旧操作已占号时明确冲突，不追认旧请求。
- 新权限租期在数据库任务内再次核验并持锁；空选集按普通聊天权限，非空额外要求connector权限。
- 兼容reader隔离已标记的新操作与会话，覆盖claim、耗尽、权限恢复、旧writer、直接dispatch和恢复会话。

**产品执行准入仍关闭。** Host版本化provider尚未实现，当前新命令在新增outbox之前返回execution_unavailable，空选集也不会降级到旧接口；已冻结原回执可以核对重读。测试中的私有存储准入只是验证事务，并不证明服务可执行。UI当前不发送这个新命令，也没有解除非空选集guard。

“原子”范围是message/outbox/模型/selection/receipt数据库记录。复用的projectless工作空间准备仍是独立、幂等的先行步骤；已把可提前判断的陈旧refs检查放在准备之前，但不宣称文件系统创建与SQL事务原子。当前关闭的provider门禁位于该步骤之前，因此普通新请求不会因此创建工作空间。

### 3. 固定内部能力承载方式 — 机制资格已执行，产品接线待做

本轮使用固定实际Runtime进行fresh本地资格：同一进程的MCP可以取得内部bearer，而实际shell_command和exec_command仅返回MARKER_ABSENT。新建config/log/rollout/SQLite及模型输入、原生输出未含随机marker原值；四次Runtime均正常EOF退出。见[环境能力资格](evidence/carrier-qualification/README.md)。run-01观测器错误保留，run-02改用精确原生item完成通知后通过，没有用模型正文代替命令事实。

下一步产品采用最小进程拓扑：**Host直接持有Connectors Rust worker，控制面为独占JSONL管道；worker复用官方rmcp server暴露受限loopback MCP数据面，出站继续用固定Codex库。** 不再增加一个仅做转发的Go Broker进程。平台凭据继续只留Connectors。内部数据面能力按Runtime generation生成，仅注入目标Runtime，精确排除工具环境，并验证有效配置；它不能调用控制面。

### 4. 打通Host/Gateway与审批 — 下一项实际工作

按以下依赖顺序推进，不先打开UI或填写假ready：

1. 将私有控制候选落为正式源：scope/instance/generation绑定、有限租期、prepare/bind/revoke、真实pending-call查询/单次决定，固定容量、超时和EOF语义。
2. 实现worker的独立Broker模式及Host owner。普通EOF先撤销准入，再正常清理；不引入强杀升级。
3. 版本化Host提交复用modelOperationMu、完整输入摘要和accepted/pending/uncertain回执。accepted重放先返回旧Turn，再考虑新能力；模型与选集只做一次合并后的idle/cold-resume变更。
4. 由真实turn/start response或turn/started完成精确绑定；处理通知先到、终态先到和未绑定等待。每个tools/call再核验lease、当前安装generation、支持工具及批准。
5. 通用market审批以独立投影接入既有回调生命周期。metadata只携带callRef，Host查询Broker真实登记的工具和参数摘要；一次批准仅用于同一调用。旧Sorftime语义保留。
6. 补Native版本化dispatcher/历史refs与原生MCP结果投影；上述provider可核验后，最后接UI并开放经过资格化的服务。

### 5. 真实服务接入 — 后续依赖仍保留

OAuth/Keyring、三项未知HTTP凭据规则、Google真实包/token文件与正常退出、淘宝独立接入、供应商支持工具/风险/重试及费用范围继续按05逐项关闭。不能将本地合成MCP lookup或状态查询换算为51项真实资格。真实账号、收费模型和平台业务操作本轮未调用。

## 验证与限制

汇总与文件摘要见 [audit-implementation-checks.json](evidence/audit-implementation-checks.json)，当前前端专项日志见 [audit-ui-tests.log](evidence/audit-ui-tests.log)。

- Contracts：新family JS7、Rust5、Go2及Clippy/TS/source-sync通过；旧三历史兼容基线通过。原fallback的旧scheduled-plan-draft远程schema EOF仍单独保留，不宣称全仓检查全部通过。
- Desktop：Native FEAT157原16项通过，随后新增SQL30→31保留安装/回执/旧ledger的专项通过；原授权2项、模型outbox1项回归通过。Rust格式/Clippy通过。
- Desktop：11个前端专项文件97项通过；lint/build/check:native通过。第一次测试CLI漏掉仓库规定的`.local`排除项，误收集历史副本而失败；恢复canonical排除后只运行当前源码，没有改旧断言换绿。
- 卸载修复的浏览器复核：亮暗1180×760、100/200%下pending正常关闭、详情重开、查询/取消、只读状态通过；另修通用文案为“取消操作”。使用标注的合成状态，截图仅tool trace；Vite与浏览器正常关闭。见[复核记录](evidence/ui-uninstall-audit.md)。
- Connectors：真实canonical worker的race专项、lint和diff检查通过，见该仓`docs/market-owner-lifecycle-verification.json`。
- 原用户三份店铺文件的diff摘要仍为`50ca7a1165be0732b4e74d119340303c39529e5bd40b9845bed0c02d672b4eeb`。
- Native测试仅临时数据库；未启动canonical应用、未迁移用户库、未进行真实外部MCP/OAuth/模型调用；无强杀、权限破坏、恶意fixture或可执行文件替换。未提交、推送或发布。

本轮完成的是审计、已确认缺陷修复以及下一层提交/存储边界的实现。Host/Gateway产品执行链和51项真实资格仍未完成，FEAT-157不能标记完成或D4通过。
