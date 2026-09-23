# FEAT-155 下一步执行方案：3C-3B1 受限草案执行前提、共享契约与 Host 用途隔离

2026-09-18。用户要求“给出下一步执行方案”。本轮只读调查并保存方案，不开始实现。起点为[22：3C-3A实施报告](22-phase-3c-3a-implementation-report.md)，原产品范围和授权仍以[00](00-feature-brief.md)、[04](04-owner-approval-and-implementation.md)及[ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)为准。

## 1. 下一次建议只实施3C-3B1

**先补受限草案生成的契约、配置校验及Host持久用途边界，完成零调用组合检查后报告停止。** 3C-3B内部按依赖分为B1执行前提、B2可信来源与唯一确认保存；这是原草案功能的实施顺序，不增加功能或缩减两种创建方式。

| 路径 | 判断 |
|---|---|
| 直接添加outputSchema并沿Ask执行 | Ask实际允许workspaceWrite；outputSchema仅约束最终消息，不能证明只生成草案，不采用 |
| 整个草案生成与Desktop确认同批 | 同时触及权限配置、Host持久用途、Desktop来源及两仓存储兼容，首要不确定性难以隔离 |
| **B1先执行前提，B2再来源确认** | 先关闭普通路由降级执行和配置回退缺口，再消费可信最终草案，推荐 |

本轮文档`contract-impact=none`。未来B1按**breaking**管理：除新共享执行契约外，Host持久用途需要明确版本隔离；完整FEAT-155原breaking不变。候选不是已批准发布版本，也不是Provider可用结论。

**Desktop普通入口继续schema15、默认禁发；本批不新增Desktop SQL22。Host当前Store schema5，建议新增显式候选6，普通Host仍5；这项私有存储决策单列于下文，不能混淆两仓版本。** B1不接草案页面、Desktop发送/确认入口、真实激活或模型调用。B2再单独收敛Desktop来源账本及候选22。

## 2. 本轮已核实的事实

22来源证据的123份业务候选摘要逐项吻合，五仓HEAD/branch/remote不变；dirty条目为元仓3、Desktop47、Contracts38、Host13，Runtime clean。22中的82项专项、最终12项、19项旧回归等是上批结果，本轮未重跑产品测试。两项并行只读技术复核分别调查Host/Runtime权限和Desktop来源，不是独立人工批准。

以下路径相对表中仓库，均为当前工作树：

| 事实与证据 | 下一步影响 |
|---|---|
| Runtime `codex-rs/app-server-protocol/src/protocol/v2/turn.rs:140`有stable outputSchema；Host `internal/codex/session_protocol.go:752`普通turn未传 | 增加固定草案适配，不开放任意schema透传 |
| Host `internal/codex/runtime_permissions.go:36`的Ask为on-request/workspaceWrite；`title.go:121`的禁工具prompt不是权限控制 | 草案不能直接继承Ask或照搬标题生成的安全结论 |
| Runtime `protocol/v2/thread.rs:93,379`的start/resume config稳定；`core/src/config/permissions.rs:346`支持从空受限文件系统建立命名profile | 可探索固定default_permissions/profile，经配置与协议资格检查后使用；不需升级Runtime |
| Runtime `core/src/tools/spec_plan.rs:683,750`仍注册update_plan/view_image；`tools/handlers/view_image.rs:150`带精细权限读取 | 可允许只更新展示的update_plan；不宣称工具列表为空。view_image必须受文件读取边界约束 |
| Runtime `app-server-protocol/src/protocol/v2/permissions.rs:588`拒绝旧readOnly.access=restricted | 不使用失效的旧配置；普通readOnly全盘可读也不满足受限草案目标 |
| Runtime `core/src/config/mod.rs:3705,4228`存在requirements/profile fallback；`:3744`追加辅助读根，记忆开关可能追加记忆根 | 必须检查有效配置及必要辅助根；仅看到sandbox=readOnly不足以放行 |
| Host `internal/session/store.go:70`的Record无purpose，`:58,214`为Store5及旧版拒读边界 | 请求context中的临时标记不足以保护重开；不能只加可被旧Host忽略的optional字段 |
| Desktop `schedules/store.rs:228`只有caller request_id幂等，`native_conversation_storage.rs:381,400`已有精确item/turn完成事实 | B2可复用事实和保存事务，但须增加来源唯一性；本批不提前做JSON提取/确认 |
| Desktop `schedules/ipc.rs:284`及私有Availability目前上限21 | B2若新增22，须同步21/22兼容读取，不能只加migration |

固定Runtime配置路线是源码支持的候选，**真实固定产物的有效权限及Provider对草案schema的支持仍NOT RUN**。本方案不把静态分析或进程内模拟当作真实平台资格。

## 3. 按顺序实施

### 第一步：冻结受限配置与准入条件

先将草案用途的固定策略、可验证证据及失败条件写清，再改变跨进程行为：

- 使用Host拥有的固定命名profile/default_permissions，无extends；受管空目录及必要Runtime辅助读根逐项列出，无写权限、无网络、无用户项目/记忆/附件读根。既有native受管目录机制可复用，但实际草案引用尚未接线：B1仅定义Host内部已验证的受管目录引用，并在合成检查构造；绝对路径不进入新公共请求，B2再接Desktop实际准备和引用。未接通时返回不可用，不隐选Host Home或用户项目。
- 核对并关闭shell（不能只关unified_exec）、扩权、MCP及资源工具、图片生成、Web、插件/hooks、协作、记忆和Skill继承/初始化等与草案无关的入口。只输入文本，不带文件、图片、Skill或模型路径引用。
- start/resume通过stable config加载同一策略；避免legacy sandbox及turn sandboxPolicy覆盖精细profile。普通Ask/Auto/Full语义保持，不新增第四种用户权限模式。
- 检查配置合并、requirements约束、辅助读根和错误分支。受管配置未知、回退、策略不符或无法证明有效约束时，返回明确不可用，在模型出站前拒绝；不能吞warning后改用普通readOnly/Ask。
- 允许update_plan这类仅展示事件；其存在不代表允许执行用户任务。若无法在固定来源下建立读取/执行边界，停止相关可发送接线并报告证据缺口，不改Runtime、伪装模型元数据、借experimental字段或新增独立Runtime/Provider通道。

本步完成标准是固定策略及配置/协议检查可判定，缺证据明确拒绝；实际产物/平台仍待后续正常入口验证。不得增加仅凭布尔开关跳过这些检查的真实发送入口。

### 第二步：最小共享执行契约先行

复用Contracts `plan-draft-v1.schema.json`的封闭clarification/candidate。新增仅草案用途实际需要的版本化Host入口、固定用途/schema/policy版本、文本输入、operation幂等及闭合错误。不要改变普通turn的既有输入解释或把新用途混进现行FEAT-152权限枚举。

- 仅精确local/demo_fast注册候选能力，保留owner-only loopback bearer和持久资源映射校验；Trace字段不作为身份授权，未知或不适用请求不得转入普通执行路径。
- 权威源归Contracts；Host为provider，Desktop为后续consumer。Runtime canonical仍为底层协议权威；只更新对应兼容投影，固定Runtime源码/二进制不改。
- 不接受任意outputSchema、config、scope、native ID、目录或grant；schema只由Host固定生成/加载，外部引用须保持canonical上下文，不能手写一份近似schema。
- 明确首次创建和澄清follow-up、重复/冲突、accepted/uncertain、未知schema/policy及不可用错误；不得把accepted当草案有效或保存成功。
- 保留原生thread/turn/item与既有流式/历史机制，不另建草案SSE状态机。草案本体是否可信、是否可确认由B2按来源事实判断。
- source-first生成Go/TS及必要Rust消费投影，完成严格校验、方向兼容、实际producer conformance和适用安全基线检查，再接provider。B1为本地候选，不声称tag/pin已发布。

### 第三步：Host持久用途与候选Store6兼容

**推荐决策：Host仅增加不可变执行用途、固定策略/schema版本及原操作关联，不拥有计划主状态。** 该职责是防止同一草案会话经普通入口升级执行；与Desktop计划/run账本分开。

1. 先分离最高可读格式与允许迁移目标，普通入口保持Store5；仅显式候选允许创建/迁移6。临时5→6、正常重开、旧会话和原operation检查通过；日常Host库不迁移。
2. 新草案会话在Runtime创建前，于原reserve事务登记不可变用途；幂等摘要纳入用途及schema/policy身份。不能先创建thread再补用途，也不能把context字符串当持久授权。
3. 5→6时为既有会话逐条回填ordinary用途并保持原语义；6内新记录缺失/未知用途事实明确拒绝，不能自动降级为普通用途。旧Host必须拒读6，不能忽略用途后执行。
4. 所有start/resume、v1/v2普通turn、permission-turn和权限切换入口共同核对持久用途：草案会话只能继续固定草案路径或被拒绝；普通会话不能凭请求标签升级为草案。中断/必要只读历史继续沿原授权链。
5. 候选reader关闭新producer后，仍能识别草案用途并守住发送边界；不得将6写回5或删用途降级。正常停止及未知历史不自动重发。

不新增第二个Host数据库、计划调度服务或执行队列。若复核证明现有同等级持久版本机制已足够，可减小实现，但必须证明旧reader不会忽略用途后放宽执行，不能靠optional字段省略兼容设计。

### 第四步：固定草案adapter接原链

仅在上述源和保护成立后，接同一Host Manager、thread/turn、operation和恢复链：固定schema每轮携带，start/resume及后续turn保持同一受限策略；普通权限context不能覆盖草案配置，配置失败不能fallback成普通任务。

澄清回复仍在同一受限用途会话；完整candidate也只是模型建议，不调用计划保存、grant、启用或run。重复accepted返回原turn，pending/uncertain不重新POST；正常重开沿可信映射恢复，不推测native身份。禁止借标题专用provider或新隐藏测试入口绕开产品调用路径。

本批没有Desktop renderer草案命令、outbox用途改造、草案提取/确认或页面；Desktop消费接线归B2。版本化provider能力先就绪，旧consumer仍沿原路径。

### 第五步：零调用组合验证、技术审查、报告并停止

| 组别 | 完成标准 |
|---|---|
| 源与配置 | 固定schema严格同源，start/resume/turn配置一致；覆盖配置不符/回退/缺证据拒绝，不以prompt或工具名列表冒充权限 |
| 用途与入口 | 原reserve/operation与用途同事务；普通/v2/permission/重开入口均不可放宽草案用途；普通三权限模式回归保持 |
| 幂等与恢复 | 同operation不重复创建/投递；改变用途/schema/policy形成明确冲突；unknown不自动重试；必要只读/正常中断可用 |
| 存储 | 普通Host5不迁移，候选6前向/重开兼容；旧Host拒读6、未知用途拒绝；Desktop仍普通15/候选21，无SQL22 |
| 验证边界 | 普通临时库、纯配置及进程内协议检查，零模型/图片/商家调用；不启动真实App/Runtime/Provider或访问日常数据 |
| 交付 | Contracts leaf generate/strict conformance、安全基线；Host定向Go/race/lint与必要旧回归；源摘要、结构化自审及未执行项逐项记录 |

禁止强杀、权限破坏、攻击fixture、二进制伪装替换。安全集合先核对再运行；不把未执行的真实配置/Provider能力写成PASS。原总`generate:check`受Contracts dirty保护阻止的问题保留，不重置已有改动或关闭检查，不把修复无关public API生成链并入本批。

## 4. B2及后续保留的范围

B2再处理Desktop受限提交来源、精确最终item/turn事实、用户选定真实目标ID、来源唯一确认及同库保存。普通聊天发起计划创建时，须明确进入独立受限用途会话及必要用户上下文交接；不把Host用途不可升级误实现成取消对话创建入口：

- 同一scoped source换request ID或正常重开也最多保存一个计划；plan、原request收据与source→plan关联同事务。不能先save后登记来源。
- 仅完整可信的final_answer item与对应completed终态形成候选；delta、截断、多final、失败/中断、未知格式和仅冷历史终态均不推导成功。整体NativeView partial不应误拒一个本体完整且来源可信的final。
- 模型标签只供消歧，ID由用户明确选择；确认后仍仅保存paused，不自动授权/启用/执行。
- 推荐B2再明确最小Desktop候选SQL22来源账本。无SQL方案仍需原outbox持久用途和native派生唯一key/摘要，不能用内存句柄冒充重开唯一性。无论选哪种，兼容读取及删除墓碑必须同步，旧1—21 migration不改。

页面、重要更新显示、防空闲睡眠、真实候选激活及有计数保护的Provider验收仍为后续。本批预算为零真实文本，累计0/12，图片/商家0；不转用其他需求额度，不把剩余额度自动消耗掉。

**下一次若按本方案实施，完成3C-3B1报告后停止。** B2和第四阶段未开始；本轮方案请求不等于立即实施、迁移日常库或真实调用授权。

本轮两项只读技术复核确认无剩余方案阻断；已补清Host内部目录引用与B2实际接线的分界，以及Store5→6既有会话ordinary回填。配置真实生效仍为后续资格，不因方案审查而标PASS。

本轮实际文档检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及127处变更文档本地链接均PASS。仅修改8份元仓需求文档；四个产品仓全部起点文件逐字节保持，未运行产品测试或真实调用。

后续授权更新：用户明确要求本次连续执行B1与B2，已依[24执行定义](24-phase-3c-3b-execution-definition.md)完成候选实现，见[25报告](25-phase-3c-3b-implementation-report.md)。本文件此前“只B1/未实施”仅保留当时计划历史，最新停点以25及feature.yaml为准。
