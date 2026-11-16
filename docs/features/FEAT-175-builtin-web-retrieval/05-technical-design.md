# FEAT-175 技术设计

2026-11-15，修订3，推荐候选，未实施。用户已选服务端托管和原生只读自动执行。详细实现与验收以 [15](15-identity-model-readiness.md)、[16](16-expert-policy-implementation.md)、[17](17-native-cancellation-routing-qualification.md) 为准；13／14保留复审背景，18记录完整复审。Runtime零核心变更仍须实际资格支持。

## 1. 四个问题分开处理

1. 产品可用性：工具属于 App 的默认能力，取消市场安装、授权和每个会话勾选前置。
2. 工具组织与选择：复用 Codex MCP／tool_search／Code Mode；完善任务语义，避免 Basic／Pro 都争抢普通问答。
3. 审批与时限：采用原生权限、审批与有效执行时间，移除内置链的市场 Broker 截止。
4. 公开分发：由易界服务端持有 Kimi Key、判断产品身份与额度；不把本机开发凭据方案扩散到其他用户。

不能用“自动选中旧连接器”或“把超时统一加长”同时代替这四层。

## 2. 拓扑与仓库边界

```text
普通聊天／专家聊天
  │
  ├─ Codex 原生 hosted web_search
  │    └─ 当前 Kimi／MiniMax Responses 服务
  │
  └─ Codex 原生 MCP / tool_search / Code Mode
       └─ yijie_web（应用拥有的本机标准 MCP 入口）
            └─ 使用 Native 管理的仅检索委派能力调用公开 API
                 └─ yijie-api：身份、资格、费用准入、审计
                      └─ yijie-connectors：服务端 REST adapter
                           └─ Moonshot Search / Search Pro / Fetch
```

本机 MCP 入口优先复用当前 Host 拥有的 Connectors worker 进程、rmcp HTTP transport、loopback capability 和正常 EOF 生命周期，在同一进程提供独立的 `/builtin-web/mcp` 路径。它是新的应用表面，**不经过市场 Broker 的 selection/prepare/decide_call**。不为网页工具另起 Node/Python runtime，也不把网页客户端塞进 Runtime 内核或 artifact-mcp 媒体模块。

共享进程的启动条件要与市场功能开关解耦：仅启用内置网页服务也能启动所需 worker；不因此扫描、授权或准备其他市场服务。新内置路径不再接收旧模型 Key 的 FD3 快照；旧 FD3 仅服务仍受支持的旧路径。Host 的市场服务器整理不得覆盖随后合并的 yijie_web 配置。

客户端 worker 只做标准 MCP 输入输出与易界产品 API 的适配。主产品 access/refresh token 由 Native AuthService 保有，不能直接转交普通 worker；网页委派的签发／更新／撤销通道尚需源契约和实际接线。供应商 HTTP 在 Connectors 服务端，复用参数构造、校验、截断和错误分类；不能原样全局共享含 serial、permit、cancelled 的旧 Backend。每个 operation 独立状态、同源纯逻辑复用，公开／内部 API 先由 Contracts 定义。

API 不生成搜索计划、不运行 LLM、不管理 Codex turn，不代替 Runtime 判断下一项工具。服务端用量记录是调用与费用事实，不是第二套 Agent 执行历史。

直接远程 MCP 是可行备选。当前 bearer_token_env_var 是进程环境解析，不能假定已支持易界产品短期 Token 的透明更新；auth=chatgpt 也不能代表易界身份。首选已有本机 worker 桥接正常产品会话，避免为 Token 更新重启 Runtime或另弹搜索 OAuth。若 G2V 证明现有产品身份已能静默续期远程 MCP，可以据证据简化；不能仅凭 transport 存在就声称端到端可用。

## 3. Codex 原生装配

Host 在普通 thread/start、正常恢复和模型切换的配置组合点自动装配 mcp_servers.yijie_web。使用原生 config 和精确 leaf merge，不覆盖整个 features 表，也不改其他市场服务器。

示意配置（方案，不会写入用户环境）：

```toml
[mcp_servers.yijie_web]
url = "<Host-owned-loopback>/builtin-web/mcp"
bearer_token_env_var = "YIJIE_WEB_MCP_TOKEN"
enabled = true
required = false
startup_timeout_sec = 10
tool_timeout_sec = 60
default_tools_approval_mode = "auto"
enabled_tools = ["kimi_web_search_pro", "kimi_web_search", "kimi_web_fetch"]
```

本机 capability、产品会话 Token、供应商 Key 是三种不同凭据。Runtime 只得到本机调用 capability，并沿既有受管 env 规则从 shell 环境排除；上游 Key 不进入 MCP、模型、renderer、argv 或 App 资源。

- Kimi 保留已资格化 function_code_mode 的原生 tool_search／BM25／deferred MCP registry。
- MiniMax 保留不启用 tool_search 的现状，沿现有函数 namespace 适配加入 mcp__yijie_web，直接暴露有效工具。
- 工具发现不授予执行权限；服务端资格在实际调用时验证。
- 不全局设置 inherit_mcp_servers=true。子代理遵从既有原生权限／有效 MCP 配置，不扩大所有第三方连接器的继承范围。
- input-only 草案、辅助标题不装配内置工具，并显式关闭 hosted 搜索。用户的 web_search=disabled 只保持其原生 hosted 禁用语义，不被扩张成所有 MCP 的禁网开关；本期不新增另一套全局网络权限系统。

## 4. 专家规则修正

删除 expertThreadConfig 中“role 非空就写 web_search=disabled”的条件。专家角色负责专业说明、资料和业务工具范围，不自动剥夺应用通用网页能力。

默认专家继承有效web_search，也可使用yijie_web；按16号保留data-analyst-pro三个现有版本的网页禁用，脚本自身不联网说明不误禁整个专家。政策根据ResolveExpert验证的精确版本／角色摘要和同源政策数据确定，不解析文本猜权限；未来联网变体另发新版本。

本期只调整网页能力，不改变 WithExpertImageRoute、ImageRoute、LinkFox 及内置图片／视频的专家选择与禁止替代规则。平台私有数据仍需对应连接器授权，网页检索不能替代它。

已加载旧线程可能保留旧配置／指令。复用当前 idle 检查、正常 unsubscribe/resume 与模型切换路径刷新，不在活动 turn 中换工具表。验收检查实际发给供应商的 tools，不只断言 Host map；不改 rollout、不创建新聊天搬移历史、不强制压缩。

## 5. 工具选择稳定性

### 稳定 wire 名称，更新任务语义

| 任务标题 | 稳定 MCP 名称 | 唯一执行映射 |
| --- | --- | --- |
| 研究网页 | kimi_web_search_pro | POST /v1/tools/search_pro |
| 采集来源 | kimi_web_search | POST /v1/tools/search |
| 读取网页 | kimi_web_fetch | POST /v1/tools/fetch |

保留名称是工程取舍：现有 Runtime 检索约束补丁 0012 按这三个名称后缀识别检索。随意改成 research/read_page 会漏掉该原生约束，不能在宣称不改 Runtime 的同时忽略它。界面使用任务标题，供应商和 Basic／Pro 作为必要来源信息。

title、描述、schema 统一从 Contracts 生成。移除旧描述中“普通联网问答直接用 Pro”的冲突规则：普通问答默认 native；Pro 用于研究／核查／总结／限定材料；Basic 用于列表／官网／采集；Fetch 用于明确读取已知 URL。

共享的 Host developer instructions 也需在原唯一组合点更新：当前“没有已选检索连接器就只用原生”的措辞不能继续排斥应用内置工具。仅调整这条网页任务规则，保持一份注入；已明确选择的其他业务／检索服务仍按其适用范围处理，不因它存在就全局禁用网页能力。Skills 不重复拷贝一份工具目录或路由规则。

参数继续封闭：Basic 无 sites/time_window，Pro 仅传用户要求的过滤，Fetch 只接 URL。无效参数在发送前失败，不把 Basic 请求偷偷改成一次 Pro 请求。保留既有生成类型、正文状态和限额。描述包含简洁中英文任务词供原生 BM25 使用，不另造 Host 意图词库、分类模型或工具索引。

### 并存的真实限制

普通聊天不因 yijie_web 已装配就关闭 hosted。原 applySelectedRetrievalConfig 对 kimi-web 选集的覆盖只留给尚在结束的旧市场操作，不继续作用于新内置路径。

Kimi hosted 搜索可能早于模型决定 MCP 工具。固定 TurnStartParams 没有已验证的“先语义分类、再改 hosted 工具表”入口；tool_search 只是工具发现，隐式 Skill 也不能撤销已经发生的供应商检索。

推荐方案保证路径可用、执行映射确定、关键任务选择通过评测，**不承诺任意自然语言输入零额外 hosted 搜索**。这些额外调用和费用必须计入结果。冻结评测不通过时停止交付判定，不无限增加提示词后挑成功样本。

若进一步要求研究／URL 任务绝对禁止 hosted 预检索，需另审两个选项：通过既有明确任务／Skill 输入建立受信结构化任务范围，在 turn 前配置关闭 hosted；或证明缺口后评估最小 Runtime 扩展。不得靠 Host 关键词分类、增加隐藏模型回合、篡改模型响应解决。当前候选选择默认并存及 [06](06-test-plan.md) 的量化验收。

## 6. 审批与时间边界

默认真实注解 readOnlyHint=true、destructiveHint=false、openWorldHint=true、idempotentHint=false，审批模式为原生 auto。当前 Codex 对非 destructive 的只读工具不要求默认确认，符合用户选择；不需要永久 approve 或伪造批准。

内置路径不创建市场 lease，不以安装、probe、prepare 时刻计时；不复制 A/D 双截止或业务 decide_call。

| 阶段 | 权威与初始建议预算 |
| --- | --- |
| 模型思考、工具发现 | 原生 turn／模型机制，不消耗网页 MCP 的执行预算 |
| 原生审批等待（策略确实要求时） | pre-call 审批先于 tools/call；elicitation 期间 active_time_timeout 暂停；无额外 23 秒倒计时 |
| 实际 MCP 操作 | tool_timeout_sec=60，从 tools/call 开始按原生有效执行时间计算 |
| 易界 API 往返 | 初始 45 秒，包含准入、上游 35 秒和结果传递；其中不等待用户审批 |
| Moonshot HTTP | Basic 默认／Fetch 15 秒；Pro／Basic 正文 35 秒；上游 timeout_seconds 保留 10／30 |

初始预算需在部署网络下验收。委派刷新／准入／网络开销也必须计入父操作；发送前剩余不足完整上游预算和余量时明确未派发，不悄悄缩短 Pro。只读工具可能并行，false 的 server parallel 配置不能禁止 readOnlyHint 带来的原生并行；容量不足及时返回 busy，不复用旧全局 serial.lock 堆队列。详见 14 第 3、7 节。

### 当前 Host 仍有一处接入缺口

Host 目前对 mcpServer/elicitation/request 只接受市场 handler，其余 decline。不能因为 Runtime 支持暂停计时就声称内置工具的 prompt 场景已经接通。

需补标准 MCP elicitation 的薄投影：消费 canonical request ID、server、thread/turn、参数展示，接入现有确认组件，再回传到同一请求。审批状态、记住决定、执行与取消仍由 Runtime 维护；只准入应用声明的 yijie_web 与有效线程，未知服务保持原边界。没有 Broker 审批镜像、第二批准或自定义 TTL。

不为绕过缺口全局关闭 tool_call_mcp_elicitation，以免改变其他 MCP 语义。默认 auto 与真实原生确认场景分别验证。

## 7. 服务端托管与费用

完整分发使用正常易界产品身份 → 服务端资格 → 单次外部请求。没有供应商 OAuth，也不让普通用户管理 Kimi Key。

- API 复用已有身份、租户／授权和审计模块；public 生产激活是依赖，不能把 local_demo_direct 固定身份用于公网。
- Kimi Key 仅在 Connectors 服务端秘密存储／进程中，按部署身份注入；客户端持易界会话或有界能力。
- 发送前校验账户资格、额度和并发；具体值由运营配置，不把原生 Token budget 当成人民币账本。
- 沿既有业务存储保存最小调用记录：主体、operation ID、模式、参数摘要、状态、供应商 request ID 与计费判定。不将完整 query／URL／正文写入常规审计。
- 同一主体／租户下 operation ID 原子查重并绑定参数摘要；承诺最多一次派发，不承诺供应商 exactly-once。派发事实先持久化，发送未知不自动再派发／返还免费；重开不得换 UUID 重放旧调用。只读状态／取消和 result_unavailable 规则见 14 第 4 节。
- 不假定普通 MCP meta 含稳定业务 call_id。本机适配器在一次实际 MCP 调用入口分配 operation ID，并保持本次投递身份；不拿 Code Mode cell_id 或工具名冒充原生调用 ID。
- 复用禁重试、禁 redirect、一次请求和有界结果；服务端不调用额外 LLM。

2026-11-15 官方工具单价：Basic ¥0.01、Pro ¥0.015、Fetch ¥0.01；Kimi／MiniMax hosted 搜索公开单价均 ¥0.03，模型 Token 另计。具体费用以当前供应商用量判定，UI 次数不能代替账单。

默认可用不等于无限免费。运营账户、产品身份、域名／TLS／秘密注入、额度政策和支持版本在 G5 前落实；本轮不读 Key、不新开账户、不部署。若产品要求完全匿名且无 App 身份，须另审访客额度；不能将客户端自报设备 ID 当成收费授权。

## 8. 结果、取消与观测

保留原 1 MiB 上游响应、65536 字节完整 MCP 封包、UTF-8 截断、不截 URL、content_status、dropped_results 和空结果语义。API 返回标准化材料，由原生 MCP 回灌与 needs_follow_up 继续生成，Host 不自建总结循环。

上游鉴权失败在新产品路径中表示易界运营服务不可用，不能沿旧工具文案要求用户重配 Kimi Key。产品会话过期、服务资格不足和供应商异常必须分别映射；完整结果封包保持单次 text＋structuredContent，不在代理层重复包裹正文。

当前 WebRetrievalResult 只挂在市场活动下。新入口须把同源 renderer 接到普通 native MCP item，以 server/tool 和已验证 schema 识别；不能仅改服务器名就认为展示自动完成。MCP 材料不写入原生 web_search sources。

观测复用 thread/turn/native item。必要记录包括审批等待、MCP 有效耗时、服务端准入、HTTP、归一化、主要路由、额外 hosted 调用与供应商发送次数；不记录 Key 或完整正文。原生 hosted 费用与易界 REST 费用分开，不承诺在服务端代理账本中已经覆盖外部模型供应商全部费用。

正常停止复用 turn/interrupt，并新增必要的 Host→worker I/O 撤销与远端 operation 取消适配；不能假定丢弃 MCP future 或 HTTP 断开已完成远端取消。按API取消与原子claim的提交顺序判定零发送／可能计费；claim是保守派发授权点，不等于供应商已收到HTTP。派发后有界收尾，迟到结果不进入新 turn。G2V 验明实际传播；正常重开只读历史，不自动重放。不得新增脚本抓取、进程强杀或权限破坏路径。

## 9. 最小扩展边界

目标是原生配置与标准 MCP 适配，Runtime 核心变更目标为零。如果固定构建在 G2V 无法实现承诺，先展示 schema／wire 缺口，再审最小扩展；不能静默换成 Host planner、另一套工具加载器或审批调度器。

跨仓 source-first、旧数据和公开上线顺序见 [04](04-contract-change-plan.md)、[07](07-implementation-plan.md)、[09](09-release-and-rollback.md)。
