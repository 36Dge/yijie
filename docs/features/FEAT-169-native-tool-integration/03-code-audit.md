# 四组原生工具接入复审（2026-11-08）

本轮沿固定原生源码、0020 接入补丁、Host、Contracts、Desktop 的实际调用链重新审计，范围仅 V2 多代理、apply_patch、Code Mode exec/wait、四个 memories 工具。发现并修复三类接入遗漏；没有新增其他工具或另造执行/审批引擎。

本轮修正属于 semantic（恢复既定的权限归属与命名空间策略）；FEAT-169 整体继续采用 breaking 判定，因为前次 Native6 新枚举仍需消费者配对。原 0020 补丁不改写，新增 0021 审计补丁，旧候选制品保留。

| 问题 | 实际影响 | 修复 |
|---|---|---|
| P1：子代理自动审核拒绝后的人工接管使用根 threadId，且依赖 thread/started 缓存才能归根 | 可能把原子任务的授权写进根会话；没有观察到子线程启动事件或原轮次已结束时，审批归属不完整 | 使用原生 thread/read 的 parentThreadId 与原轮次核验归属；后台异步读取避免阻塞 stdio reader；展示关联根会话，原生 approveGuardianDeniedAction 始终发送原子 threadId。允许已结束的被拒绝轮次登记人工授权，不伪造其仍 active |
| P1：子代理 MCP 隔离条件只看重载后的子配置 | 子角色配置改变 feature/继承字段时，可能偏离父轮次“不继承 MCP”的约束 | 按实际 V2 父轮次及父/子较严格的继承选项限制，并把禁止继承继续传给下一代；仍使用原生受约束配置和原生 spawn/resume |
| P2：函数别名转换丢失逻辑命名空间 | Code Mode 的 excluded_tool_namespaces/direct_only_tool_namespaces 对已转换的 memories 名称失效 | 给原生 Runtime 接口保留逻辑命名空间元数据，既有原生曝光/排除规则使用该元数据；函数别名、执行器与调用流程不变 |

同时删除 Host 的 nativeOwners 子代理树缓存。Host 只保留自己已创建/恢复的根线程授权凭据，以及每条审批的不可变展示归属；代理树、调度、消息、驻留、恢复均由原生 Runtime 拥有。原生线程删除后撤销对应根凭据。

## 原生复用核对

| 工具组 | 原生权威与实际执行 | 易界适配范围 |
|---|---|---|
| V2 六工具 | core/tools/handlers/multi_agents_v2、AgentControl、AgentRegistry、原生 mailbox/residency | 固定 V2 配置、提供方函数名/明文输入适配、审批归属与活动展示；没有另建调度器或代理注册表 |
| apply_patch | 原生 parse_patch、verify_apply_patch_args、ApplyPatchRuntime、ToolOrchestrator、原生文件变更事件 | JSON input 解包与原生 FileChange 的展示投影；无 Host 补丁解析器或文件修改器 |
| exec/wait | 原生 CodeModeExecuteHandler、CodeModeWaitHandler、code_mode_service/V8、原生嵌套工具调度 | JSON input 解包、函数别名保留策略信息；无第二套 JS 执行器或权限通道 |
| memories 四工具 | ext/memories 原生工具、LocalMemoriesBackend、原生路径/文件名/追加写规则 | 声明及配置接入；无 Host 记忆库、搜索器或重复写入器。自动生成、整理、剪枝仍关闭 |

## V2 与旧会话语义

- 新建和恢复的普通会话使用 V2。旧 V1/Disabled 记录不改写，不重新启用 V1 工具。
- input-only 与原生审核辅助线程保持禁止多代理，不被 V2 升级开关打开。
- 原生 list_agents 列当前运行中的代理。正常结束进程后，旧子代理只保留历史，不自动复活或自动执行。恢复旧会话后，通过 V2 新建子任务继续工作；本轮没有在 Host 补造冷启动代理树。
- 原生 approveGuardianDeniedAction 仅在原线程注入“该具体操作已获准”的上下文，不启动新轮次。用户明确继续后再由原生机制尝试；本轮没有实现自动重放。

补验最初对“冷启动复活旧子代理”和“允许后立即执行”的期望与上述原生源码语义不符。已据 AgentControl live_agents、ensure_v2_agent_loaded 的驻留语义，以及 session/handlers::approve_guardian_denied_action 的 inject_no_new_turn 行为校正验收；失败日志保留，未通过改造 Runtime 来迎合错误预期。

## 验证

- 原生 Rust：6 个 native_tools_ 定向用例通过，含函数别名的命名空间策略、父轮次 MCP 约束；见 yijie-codex/.local/native-tools/audit-unit.log。
- Host/Session：19 个顶层定向 Go 用例（含子例）通过 go test -race；真实 Kimi 用例按本轮无调用策略跳过，包含 V2 六工具、Ask 子审批、真实原生 AutoReview 拒绝→人工授权→显式继续、旧 V1/Disabled 恢复、旧 V2 历史与新子任务审批、原生补丁拒绝、Code Mode 等待/取消、四个记忆工具与重开、input-only、真实市场组件启动。受控本地 HTTP 提供普通响应，不调用供应商。
- AutoReview 用例检查授权只出现在原子线程，根会话无该授权；审核辅助线程无 V1/V2 工具；授权本身不写文件，明确继续后原生执行器才写入普通临时文件。
- Host 定向 vet、canonical Runtime 构建及配置/schema 生成、Contracts 生成/同步检查、原开发入口源码配对检查通过。未运行无关全量用例或用户禁止的测试。
- Kimi 真实调用仍保持前轮 19/40；本轮无需新增付费请求。MiniMax 实际验收为 0，严格遵守用户限定。

新 Runtime 源码 ID：dfa05c556627e781a1cd1386c17f773a7a67012feeee7525268e8889ad2473a6。
Binary SHA-256：7a4f7f4eb051f7a184bad2a9d75b9845cda271228586ad60fb8e735f5fdd4a64。
stable app-server schema 仍为 271 文件，树摘要 79b27b23a58249dc700567c4c0c824c222bbf4c5b81b894dea5fe8d84f34eb78；没有新增原生 wire 字段。

详细日志：yijie-agent-host/.local/native-tools-audit-final.log、native-tools-audit-vet.log；Runtime 构建日志 yijie-codex/.local/native-tools/audit-build.log。真实 AutoReview 流程是原生 Runtime + 受控本地 reviewer 响应，不能称为真实 Kimi 的审核决策。

用户已正常退出，原 pnpm client:dev 入口已加载 dfa05c… 新候选；实测 /readyz 返回 200 ready，Skills、专家、连接器启动正常。就绪证据见 references/audit-readiness.json。未提交或推送 Git，未修改原用户 UI/AGENTS 改动，未重置数据库或改写原聊天历史。
