# FEAT-170 — 原生 tool_search 接入与启用方案

> 桌面续验更新：同一条真实桌面聊天的完整链路已通过；模型累计9/12次，另获批并完成1次只读联网检索。当前结果见[05桌面验收](05-desktop-chat-e2e.md)。以下费用、GUI未执行等内容保留其先前记录时点语义；其它未完成场景不执行，整体D4保持未通过。

> 当前状态（2026-11-08）：用户后续已授权复审后执行及仅 Kimi 最多 12 次验收。实现与本机启用已完成，实际调用 5 次；完整 D4 尚未通过。当前事实见 [实施记录](03-reaudit-and-implementation.md)、[交付与验证](04-delivery-and-verification.md) 及 feature.yaml。以下保留**方案阶段历史**，“本轮”“仅方案”和 NOT RUN 等描述均指最初规划时点。

> `demo_fast` · `local` · 2026-11-08 · **仅方案，未实施、未启用**

## 1. 请求、授权与交付边界

用户要求审计易界所有相关仓库，形成原生 `tool_search` 接入及启用方案，能够复用的原生能力必须复用；本轮明确“仅落方案，不做执行”。因此本包只记录源码事实、推荐设计、验收与启用门槛。Owner、技术负责人、Reviewer、发布负责人均为段成威。

本次文档修改的 `contract-impact = none`；下文实施目标按最高风险 **breaking** 规划：模型可见工具从直接暴露改为延迟发现，涉及提供方 wire、模型目录和旧会话重放，尚无方向兼容实证，不能称为纯 additive。

方案材料完整性、D0 文档检查、Owner 方案确认、实施授权、真实模型额度和 D4 可用结论分别记录。D0 文档检查通过不允许突破本轮“仅方案”。本包不继承 FEAT-169 的 D4、40 次额度、后续 8 次额度或其余额。

- 目标用户：使用易界本机聊天及已有连接器的用户。
- 用户结果：模型根据任务调用 `tool_search` 找到当前可用工具的定义，再经现有原生执行与审批完成任务；减少初始模型上下文中的完整工具定义。
- 推荐首批：**Kimi K3.1 Pro，普通根聊天，当前选中的有效 MCP 连接器**。MiniMax M3 保持当前直接暴露路径；兼容设计保留，但不能用 Kimi 结果为其启用背书。这是本包推荐范围，尚未获得 Owner 对方案的确认。
- 不做：市场全局搜索、自动安装/启用/勾选连接器，搜索文件/网页/知识库，新工具商店或设置页，新的权限/审批/记忆/调度平台，V1 多代理，变更自动压缩策略，启用其它原生工具，新增依赖/模型/外部服务，公开或签名发布。
- 本轮不改 Runtime/Contracts/Host/Desktop/Connectors 实现，不生成 SDK，不构建或启动应用，不读取供应商凭据，不执行业务工具、模型验收、提交或推送。

本包独立于 [FEAT-169](../FEAT-169-native-tool-integration/00-feature-brief.md)，不会将已完成六组工具改成新的未完成状态。最新 FEAT-169 实现及 UI 边界以其 [06 执行记录](../FEAT-169-native-tool-integration/06-user-input-context-execution.md)为准；后续上下文浮层等并行改动也不属于本包。

## 2. 审计基线、方法与仓库覆盖

审计对象为当前工作树及已选择的本地 Runtime 候选，不把 dirty HEAD 当成实现的不可变提交。十二仓 branch、完整 HEAD、origin、已有改动路径和关键源码摘要见 [源码审计记录](references/source-audit.json)。没有执行产品测试；下列测试名称仅表示读到了覆盖意图。

- 固定上游：`rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d`。
- 当前 Runtime 候选指针：`interaction-tools-v1/038d498bda0d4cb8899e15ea81dfa777b6928adc0e389aebf5e20b3038332086/aarch64-apple-darwin`；本轮仅读取其指针/manifest。
- 原 `native-tools-v1` 候选和 0020/0021，现 0022 问答/上下文适配均是保留基线。
- 入口：Desktop `pnpm client:dev` / 原“易界.app”，脚本 `scripts/run-local-demo-fast.sh` 选择匹配的 Runtime/Host 来源。当前入口还消费其它正在演进的本地投影，实施前必须重新冻结实际基线。

| 仓库 | 核对位置与结论 | 预计实施影响 |
|---|---|---|
| yijie | repos.yaml、治理手册、Contract First、ADR-0017/0018/0021、安全边界与 FEAT-169 | 本包方案、后续证据 |
| yijie-codex | 原生 handler、spec/router、MCP exposure、Code Mode、输出/历史/记忆标记、配置及补丁链 | 最小原生传输适配与相关定向测试；不重写搜索 |
| yijie-agent-host | provider/chat_models/kimi_k31_candidate/native_tools、Runtime 严格配对、Market 准入/审批、受限线程 | 按模型配置能力及候选校验；无搜索 handler/索引/新反向 RPC |
| yijie-contracts | runtime-native-tools、runtime-interaction-tools、生成/同步器、支持基线和 Native6 | 新独立 Runtime 配置投影及来源；推荐方案不新增公开聊天事件 |
| yijie-connectors | worker Gateway、Broker visible_tools、generic definitions、providers 发现 | 复用现有目录/冻结 schema/逐次审批；只对证实的元数据适配缺口修改 |
| yijie-desktop | 开发入口、sidecar、候选冻结、现有连接器选择/审批/活动展示 | 精确候选装配；推荐方案不新增 UI/IPC/存储格式 |
| yijie-skills | 技能/专家资产入口及工具使用说明搜索 | 无直接 tool_search 接入点；保持原生技能发现，不批量改技能正文 |
| yijie-infra | workflow-session 生命周期、local 运行边界 | 复用正常启动/退出，不加服务、容器、端口或搜索数据库 |
| yijie-api | 本地 Chat 免登录边界、API 服务源码及 Runtime 关键词检索 | 本方案不进入云任务/审批主状态，不增加 API |
| yijie-admin-web | 管理端边界及 src 检索 | 无本机模型工具装配职责，不修改 |
| yijie-knowledge | RAG 职责与 internal 检索 | BM25 工具元数据检索由 Runtime 拥有，不接 RAG |
| yijie-coze | 工作流后端/前端相关关键词检索及入口 | 当前工具搜索不经过 Coze；不改工作流搜索/模型/节点 |

外围仓库的只读范围用于确认职责与排除依赖，不声称审计了其全部业务或取得运行验收。

## 3. 已证实事实、未知与纠正

| ID | 类型 | 证据与结论 | 设计影响 |
|---|---|---|---|
| F01 | Fact | `core/src/tools/handlers/tool_search.rs` 已有 ToolSearchHandler、BM25、默认 limit、缓存按 search_infos 变化重建 | 不新增搜索算法、索引库、Host 缓存目录或远端检索服务 |
| F02 | Fact | `spec_plan::search_tool_enabled` 同时检查 supports_search_tool 与 provider namespace_tools；append_tool_search_executor 还要求非空 Deferred search_info | 开能力不等于每轮都显示工具；无目录时不暴露搜索 |
| F03 | Fact | Host provider.go 设置 supports_search_tool=false；chatModelCatalog→kimiK31Catalog→nativeToolsCatalog 没有改此值，测试要求仍为 false | 修改应按已验证模型逐项进行，不能同时给两个目录无条件翻转 |
| F04 | Fact | features::ToolSearch/ToolSearchAlwaysDeferMcpTools 标为 Removed，加载器忽略旧键 | 不恢复或写入旧 features.tool_search 开关 |
| F05 | Fact | 原生 ToolSpec::ToolSearch、ToolSearchCall、ToolSearchOutput 为专用 wire；handler 仅接受 ToolPayload::ToolSearch | function 同名工具不能直接原样转交 handler；输入与输出都需要适配 |
| F06 | Fact | 上游 search_tool 测试要求结果定义留在 tool_search_output 历史，而非追加到下一次 tools 数组 | 不能以“搜索后重新注入工具”冒称已复用的原生行为 |
| F07 | Fact | Kimi 当前官方 Responses 文档明确列出 function、namespace、custom（仅 apply_patch）、web_search，其他类型不支持 | 原样发 type=tool_search 不属于当前官方支持协议；撤回上轮仅列为“未知、先打开探测”的宽泛建议 |
| F08 | Fact | 原生 Code Mode 构建把 Deferred 工具加入 nested registry，但不把完整定义加入 exec 提示；现有测试覆盖找到并调用延迟工具 | 可复用 exec 调用搜索命中的 MCP，无需维护已加载工具集合或动态注入器 |
| F09 | Fact | 原生 ToolSearch spec 不被转换为 Code Mode nested function；0020 function_input::wrap 只处理 Freeform | 不能直接重用 freeform 包装函数；薄适配沿原委托模式，保留 search 的直接调用边界 |
| F10 | Fact | MCP exposure 开启搜索后将当前可见 MCP 转 Deferred；普通 MCP 不要求 features.apps/plugins=true | 不打开 Apps/Plugins/ToolSuggest，也不把市场全部安装项变成当前可检索项 |
| F11 | Fact | Gateway tools/list→Broker visible_tools 依赖有效 lease 和当前选择；generic 工具名为稳定哈希，原服务/工具名保留于标题与描述 | 复用已有目录；检查元数据质量及授权撤销，而非另造工具目录 |
| F12 | Fact | BM25 使用 Language::English；中文服务/描述可能存在 | 中文查询命中质量需要专门验收，不能直接承诺跨语言语义搜索 |
| F13 | Fact | 搜索记录可能留原生 rollout；原生特殊 item 与 ToolOutput 标记会影响 disable_on_external_context 记忆保护 | 输出改为 function 后必须保留此语义；不能把搜索元数据当可信指令或宣称不落盘 |
| F14 | Fact | stable ThreadItem 与易界 Native6 没有独立 toolSearch 展示变体；已有工具 UI 接收真实 MCP 生命周期 | 本期沿用整轮进行中和实际执行工具卡，不伪造搜索状态/数量，不新增跨仓事件 |
| F15 | Fact | Host普通线程经StartThread/SwitchThread合并原生config；标题走独立临时thread/start。【复审纠正F15】ThreadManager共享进程模型管理器；线程Config携带目录但原生产路径不应用搜索字段，只有test_support优先选择目录。实施已补最小生产覆盖（见03）；已加载thread/resume可能忽略config覆盖 | 新目录仅绑定受信普通聊天；不能全局启用后依赖标题提示词禁止；激活需正常重开及读回验证 |
| U01 | Unknown | 推荐的 function + Code Mode 适配尚未实现、未对供应商实测 | 本轮不宣称可用；以原生回环及授权后的 Kimi 真实链路为启用条件 |
| U02 | Unknown | MiniMax M3 未完成新路径模型验收；官方 create-response 页不能证明 native tool_search 支持 | 推荐首批不启用 MiniMax；若 Owner 扩大范围，单独登记兼容证据及额度 |
| U03 | Unknown | 中文业务任务是否能借原始工具名/参数词稳定命中；大型真实目录的负载 | 建立普通合成/公开描述定向样本；不先换搜索引擎或新增 embedding |
| C01 | Conflict | 部分 AGENTS/README 仍写“连接器全未接通”历史状态，ADR-0021 追加及当前 generic/Gateway 已有实现 | 以本轮代码、最新 Accepted 决策与实际资格区分；不顺便重写旧文档 |

外部资料仅进行了公开网页 GET：

- [Kimi Responses API](https://platform.kimi.com/docs/api/responses)，查阅 2026-11-08，“工具调用 Tool Use”与 tools 参数；支持的工具类型不含 tool_search。文档说明不等于本次实测。
- [MiniMax Create Response](https://platform.minimax.io/docs/api-reference/responses-create)，同日查阅；页面未说明 native tool_search 支持。缺少说明不证明服务端绝不支持，亦不足以启用。

## 4. 推荐设计与取舍

### 4.1 决策

| 方案 | 优点 | 问题 | 结论 |
|---|---|---|---|
| A 原样声明 native tool_search 专用协议 | 原生原样、改动少 | 与当前 Kimi 官方类型范围不符，无法作为当前推荐落地路径 | 保留上游默认路径供已兼容 Provider 使用，不对 Kimi 打开 |
| B 原生检索 + 标准 function 适配 + 已有 Code Mode 执行 | 复用 BM25/缓存/目录/执行/审批；无新装载状态；与当前易界 exec 配置相配 | 需要窄 Runtime 输入/输出适配及真实模型资格 | **推荐** |
| C function 搜索后动态注入匹配工具到下一次 tools | 可以尝试直接调用命中工具 | 需额外处理加载集合、旧历史、撤权、压缩与并发，现有 Code Mode 已能覆盖 | 本期不选；B 失败时不静默改为 C 或扩大范围 |

推荐范围只提供一条完整路径：模型直接调用同名 `tool_search` → Runtime 原生 BM25 → 返回定义及原生生成的 exec 调用说明 → 模型调用 `exec` → 同一原生 MCP handler → 已有 Host/Gateway 绑定和审批 → 工具结果 → 模型回答。命中仅是发现，不是装载授权；执行资格仍在每次真正调用时校验。

### 4.2 Runtime 最小适配

1. 以完成中的当前 canonical 候选为基线，另建可重放补丁和独立构建制品。沿用现有 prepare/build/manifest 模式，不直接改 upstream `codex-rs/`、不手改生成 workspace、不覆盖已验收 binary。补丁序号实施前重新核对，不在方案阶段抢占其它任务编号。
2. 用一个可选、默认原生路径的**模型传输能力字段**明确区分 native 与 function-code-mode。建议命名 `tool_search_transport`，值 `native | function_code_mode`；名称/枚举须先在 Runtime ModelInfo 源类型定义，再使用其已有 JsonSchema 派生生成候选模型 schema，不能先在 Host 临时杜撰。当前构建器主要导出 config/app-server schema，模型 schema 需要纳入该 canonical 生成链，不能假定已存在独立导出物。沿用 supports_search_tool 为发现可用性，不把它误称为提供方原样支持专用 wire 的证明。
3. function-code-mode 仅在普通根线程、Code Mode 实际可用、function_input 已开、当前模型已资格化、namespace 能力符合要求时允许；该兼容分支沿用原生 session_source 判定拒绝非根代理暴露，不改变其它Provider原生路径。资格缺失时不激活延迟暴露，保持既有直接工具路径；启动配置不一致须在模型 HTTP 前拒绝，不能隐藏所有 MCP 后留下不可用搜索。
4. 将原生 create_tool_search_tool 的说明、query/limit 参数 schema 机械投影为同名 function 声明；不重写一份参数协议，不换名称伪装业务 MCP。按原生直接调用边界暴露，防止普通 function 形式意外进入 ALL_TOOLS 或被 CodeModeOnly 隐藏。
5. 在**同一个 ToolSearchHandler** 内增加薄传输分支：function 分支解析原生 SearchToolCallParams，复用原 ToolPayload::ToolSearch 的参数处理与同一个 search 方法；不另建搜索 handler/算法。query 空值/limit=0、默认8条、排序/合并/缓存沿原生实现。外层原 function call_id/payload 保留，用于正常、错误、取消答复配对。
6. 将原生检索结果投影为普通 function_call_output；结果仍从原生 search 返回的 Vec<LoadableToolSpec> 取得；在丢失静态类型前复用 ToolSpec::from、augment_tool_spec_for_code_mode/名字转换及 JsonToolOutput，按所选传输返回。无需反向解析一段模型字符串来重建 schema。工具正文/参数保持原生事实，只补原生生成的 exec 使用说明；不在 Host/Skills 维护另一份工具说明。function 请求的结果不能输出 tool_search_output，也不能同时双写两类 output。
7. 返回的工具通过既有 CodeMode nested registry 执行。不得扩大 excluded_tool_namespaces、direct_only_tool_namespaces 或 Hidden 策略；不满足 CodeMode 执行资格的工具不能被本路径延迟隐藏。实施应复用现有暴露枚举/策略，保持这类工具原直接可见或拒绝不一致配置，而非解除限制。
8. 保留原生 external-context/记忆保护：成功结果可复用 JsonToolOutput::with_external_context，验证错误/取消分类无丢失；generate_memories=false 及其它既有策略保持。诊断与日志不额外记录完整查询、参数 schema、结果目录或凭据；模型所需定义仍按原生会话规则处理。
9. 原生缓存当前只比较 search_infos。增加模型传输模式后，若缓存的handler携带spec/输出模式，必须将 transport 纳入**同一原生缓存**的比较键，防止切换模型后复用错误声明/输出；不新建Host缓存，不把授权放入索引。
10. 原生特殊协议路径继续使用既有 ToolSearchCall/Output 及规范测试，不因 Kimi 适配全局替换。旧历史不改写；新 function 路径形成普通原生 FunctionCall/Output 对。若发现已有历史携带此 Provider 不支持的专用 item，必须在发送前明确阻断/提示，不删除历史或静默重放业务。

以上是有明确复用点的设计，不代表函数包装器已存在。最早实现验证必须证明完整定义能够经 function 输出交给模型，并由原生规范化名字精确调用 exec 目标；只证明“搜到字符串”不算通过。

### 4.3 Host、Contracts、Connectors、Desktop

- **Host**：基于既有受管目录生成一个精确来源的普通聊天能力目录，只覆盖已资格化的 Kimi 条目，MiniMax 条目保持原值；**进程默认目录仍关闭搜索**。仅由受信普通聊天创建/冷恢复路径通过原生 thread/start、thread/resume 的 config.model_catalog_json 指向该目录，标题/受限草案等辅助路径保持旧目录，不靠prompt隔离。原生每线程Config/model manager机制复用；热加载thread/resume可能忽略配置，因此启用先正常重开，并验证真正生效的工具声明，不只检查发出的config。加入精确候选/能力组合检查，复用受管文件 preflight 和允许的旧目录升级规则，不覆盖任意用户 config。无需新搜索 HTTP endpoint、app-server reverse handler、bbolt 表、索引或工具调用代理。
- **Contracts**：Runtime 先形成候选和 canonical config/model schema，再建立独立 `compatibility/runtime-tool-search` 候选投影（拟定路径）。固定现有六组功能的基线、补丁链、模型级 transport、来源摘要、生成器及停用策略；Host/Desktop 从同源生成物消费。方案阶段不创建该真实契约 family。现有 public HTTP/SSE/Native6、问答和上下文浮层契约保持。
- **Connectors**：复用 tools/list、visible_tools、当前选集、冻结 schema 和 Gateway。原工具名/title/description/参数名应能进入原生搜索材料；只修证实会丢失这些材料的适配缺口，不人工给每个供应商建第二目录，不自动调用未选中服务获取目录。
- **Desktop**：仅扩展既有开发入口/sidecar 的精确候选选择与来源校验。仍通过普通聊天、原连接器选择和审批交互使用，无新的工具设置页、Tauri 权限或 renderer→Runtime 通道。实施后启用操作必须正常退出 App，再从原入口重开；不触发 watcher 强制终止。
- **Skills/专家**：不批量改正文、不加入“任何任务都必须搜索”的提示。仅工具说明中解释发现和 exec 调用方式；业务技能仍按原机制按需读取。

## 5. 主流程、状态与用户体验

1. 用户从原开发入口进入聊天，保持原身份/Homes、已有连接器选择及权限模式。
2. 当前轮原生构建出可执行工具集合；只有被纳入有效当前集合、且能经本兼容路径执行的延迟工具进入 BM25。
3. Kimi 按任务需要直接调用 tool_search；搜索只查本地已加载的元数据，不执行被搜索业务工具，不额外发起专用检索模型请求。
4. 无命中则原样返回空结果，模型可基于已有上下文解释缺少工具，或做一次有依据的关键词调整；不自动安装/授权、重复无限搜索或拿其它服务替代已选服务。
5. 有命中则获得定义，经 exec 调用原 MCP；实际调用按现有逐次批准/拒绝流程继续。搜索不消耗一次业务批准，也不能制造批准。
6. 用户看到原真实工具活动和结果。新增的搜索/后续推理可能增加模型 HTTP 次数，因此“本地检索”不等于整轮免费。

| 状态 | 推荐用户可见行为与内部约束 |
|---|---|
| idle | 原聊天输入区；没有独立搜索按钮、开关或空卡片 |
| loading | 继续显示原生整轮执行状态；无搜索生命周期事件时不伪造“正在搜索”条目 |
| success | 显示真正执行的 MCP 工具和最终答复；搜索命中不显示为业务执行成功 |
| empty | 无目录时不声明工具；有目录无命中时返回空结果，模型如实解释或调整关键词 |
| permission denied | 搜索无执行授权；MCP 拒绝沿现有审批/错误 UI 显示，不自动换成另一连接器 |
| error/partial | 参数错误沿原生工具错误；结果超限不得截成不可解析 JSON 或伪称完整；Provider 错误沿原有轮次失败 |
| timeout/retry | 保持现有请求和流重试配置；未知业务结果不重发。用户显式新请求才能重新执行业务；重新搜索只改变发现结果 |
| cancel | 复用原生 turn/interrupt、Code Mode 取消及 Gateway 撤销；不强杀、不恢复未完成业务 |
| concurrent | 结果依赖当前线程的集合和原生缓存；各会话不共享 Host 私有搜索状态，不串选集 |
| resume/model switch | 空闲时切换；下一轮按新模型与当前选集重新建原生路由，旧结果只作历史，不是能力 |
| compact/new_context | 沿已确认自动摘要/显式新窗口策略；丢失工具说明后重新发现，不恢复隐藏“已加载工具”状态 |

本期无新增组件、CSS、tooltip、交互控件，故不新增视觉稿。后续客户端核验仍检查现有审批/活动在亮暗主题和1180×760可用，不为本次强制全量 UI 回归。独立检索卡片若另被要求，需要先核对 canonical 事件并新评审，不能借本包直接加展示变体。

## 6. Must AC 与追踪

| AC | 可判定的目标 | 方案/验证对应 |
|---|---|---|
| AC-001 | 原生检索被实际委托；无第二索引、搜索器、目录或执行引擎 | 4.2；T01/T02 |
| AC-002 | Kimi 的 tool_search 声明/调用/返回均为支持的 function 形状；命中工具可经现有 exec 成功调用 | 4.2/5；T03/T04/T12 |
| AC-003 | 无目录不暴露；空结果如实为空；当前有效目录变化后原生索引更新，中文/英文命中达既定小样本标准 | 3/4.3；T02/T05/T06 |
| AC-004 | 执行仍绑定当前 scope/选集/thread/turn/工具/参数与审批；正常拒绝后业务调用0次 | 4.3/5；T07/T08 |
| AC-005 | 取消/重试/并发/旧会话/模型切换/压缩/新窗口不重放业务，不把旧搜索结果作为资格 | 4.2/5；T09/T10 |
| AC-006 | 原六组工具、V2继承策略、input-only、标题/审核辅助线程及外部上下文记忆保护保持 | 4.2；T08/T11 |
| AC-007 | 提供方协议、Runtime schema、配置投影、Host/Desktop来源精确配对，旧路径可保留 | 4.3/7；T01/T13 |
| AC-008 | 原入口正常退出/重开后 Kimi 实际启用，普通聊天完成发现→审批→调用→结果，未资格模型保持旧路径 | 5/7；T12/T13 |
| AC-009 | 初始请求不包含完整延迟工具 schema；只回传命中定义，普通限定目录的检索开销可接受，错误/日志无额外敏感泄漏 | 4.2/8；T06/T14 |

全部 AC 当前均未执行；用例、样本和真实验收额度建议见 [02 验证方案](02-verification.md)。

## 7. 契约、兼容、启用与回退

- 实施分类 breaking，Owner 为段成威；Runtime 是协议 producer，Host/Contracts 维护配置投影，Desktop 是配对启动 consumer，模型 API 是外部 wire consumer，Connectors 是被发现工具的既有执行边界。
- source-first：官方协议/原生源码 → 窄 Runtime 候选及 canonical schema → Contracts 新投影/示例/生成/检查 → Host 受管配置及配对 → Desktop 原入口 → 本地回环 → 获批 Kimi 验收 → 明确本机启用。
- 当前 fallback 为 Contracts `c24d73fde83a01b5dd2a9ded8defb5bbef34e311`，现有发行支持基线 `f16a497e1377f45747f8ff9292b4b60cf2027f88` 及登记窗口保留。实施按真实改动执行适用的定向比较，不把仅 HEAD 比较或新 family 不存在当成兼容证明。
- 模型目录逐项启用，不在一次 HTTP 失败后自动换协议/模型或重发请求；能力资格在候选验收时确定。
- 新配置只发给精确新 Runtime；旧 Host/Runtime 不接新字段。无公开响应变体，不要求旧 Desktop 解码新搜索 Item。配置开关关闭时，保留原 native/interaction 六组配对能力。
- 旧→新：读取旧普通 Function/MCP 历史，按当前模型建路由，不要求重写聊天；resume 不能复活撤销的 lease。
- 新→关闭搜索：推荐保留新 reader 和兼容适配代码，只关闭模型发现能力，正常结束活动轮次后重开。普通 FunctionCall/Output 历史保持可读。
- 回到旧二进制：先做离线正常副本重放/读回证据；仅认为通用 item schema 相同不构成充分回退证明。若不能证明旧提供方请求可读，保留前向兼容构建，不降库、不删 rollout、不恢复旧数据库副本覆盖日常数据。
- 无新数据库表、migration、向量库或 durable search cache；`persistence_change=replay` 只标识原生工具调用/结果历史的解释与模型切换兼容需要验证。
- 不改既有 ADR 职责边界；若实施需要 Host 搜索器、全市场授权、自动加载未选连接器或新的跨仓主状态，停止并重新评审，不能宣称本方案已批准。

## 8. 性能、安全和非目标边界

- 原生检索默认 limit=8；结果取原生规则，不建立另一层排序。普通测试目录24项、接近现有上限的合成目录用于观测延迟/输出大小；不制造危险归档、攻击载荷或权限故障。
- 中文业务任务样本同时含中文描述、原工具名和常见参数词。先验原生 BM25；不因英语分词就擅自加翻译模型/embedding。低召回时保留失败证据，先修元数据丢失和原生搜索指引；需要新算法即回到方案评审。
- 同时比较初始工具声明与 exec 描述，不能只看 tools 数组减少却把全目录塞入 exec 说明。只报告实际 provider usage 或字节/定义数，不编造 Token 节省百分比。
- 工具描述与检索结果属于不可信外部内容，不能升格为 system/developer 指令；保留原生外部上下文标记。
- 源目录已含的工具说明可能进入模型与原生 rollout。Host/Desktop 不增加搜索结果业务存储；诊断只记录事件类型、耗时/数量和安全失败码，避免完整 query/schema/结果副本。
- 当前权限范围与 Connector Keyring 边界保持。实际账户、metadata联网、模型请求和业务调用各自记录额度；模型授权不自动授权第三方操作。
- 完整性能基准、多租户、云端公开 API、安全攻击专项和发布加固不在本地 Demo 范围；进入 public/production 另立相应门禁。

## 9. 评审项、停止条件与下一阶段

推荐决策已写完整，**Owner 方案确认及实施授权均 pending**：

1. 采用 B：原生 BM25 + function-code-mode 最小适配，不新建索引/动态注入器。
2. 首批 Kimi 普通根聊天启用；MiniMax 不借 Kimi 证据启用。
3. 本期不增加搜索专属 UI，复用现有执行/审批/结果展示。

本轮不请求付费或启用批准，因为还没有实现可验收候选。后续收到明确实施指令后才按 [01](01-delivery-log.md) 整体实施；真实调用前另提交具体短用例和本任务额度。

30分钟无新事实读完整链路；90分钟同阻塞核对协议/原生函数桥，不反复翻开关；非核心验证120分钟上限；核心240分钟仍不能完成检索到调用则收敛单连接器用例并报告；实施工时16小时仍未D4必须重新定范围。时间盒不能把未启用或仅返回工具名视为完成。
