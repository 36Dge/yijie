# 易界 Web Search 设计与运行机制审计

审计日期：2026-11-15，Asia/Shanghai。范围：当前工作树、当前运行的本地开发客户端及供应商当日官方文档。

`contract-impact = none`：本次只审查和记录事实，不修改产品代码、配置、协议、数据库、构建制品或运行中服务。未提交、推送、重启或发起付费模型／搜索调用。

## 1. 结论

1. **易界已复用 Codex 原生网页搜索能力。** 普通对话没有全局关闭 `web_search`；未显式配置时，固定 Runtime 默认 `cached`。当权限 profile 为 Disabled（完全访问）且约束允许时，每轮可提升为 `live`。`cached` 是供应商托管搜索模式，不表示读取本机缓存，也不代表无网络或免费。
2. **当前有效选中 `kimi-web` 且 Broker prepare 成功后，两个模型都会被覆盖为 `web_search=disabled`。** 此时网页检索交给连接器的三项 MCP 工具。不是所有普通对话都关闭，也不是只对 Kimi 关闭。
3. **Kimi K3.1 Pro 的 Responses API 明确支持服务端 `web_search`；MiniMax 官方 Responses 服务也提供此能力（Beta）。** 两者都需要请求显式声明工具，不能把裸模型推理或只配置 API Key 等同于联网。MiniMax 最新工具文档示例已改为 M3.1 Flash；结合仍支持 M3 的 Responses 接口文档，可以确认接入通道与服务能力，但本次没有证明 `MiniMax-M3 + 当前账户 + 当前 endpoint` 的实际搜索成功。
4. **Basic、Pro、Fetch 是 Moonshot 的三个独立 REST API，而非原生搜索在易界中的三个必经阶段。** 它们共用一个 `kimi-web` 连接器、现有 Kimi Key 和相同审批链；MiniMax 作为推理模型也可以调用这套 Kimi 工具。
5. **Basic／Pro／Fetch 的分工由工具描述引导模型选择，并非 Host 的确定性中文意图分类器。** REST adapter 根据已选工具名确定端点；不在错误后自动换接口或增加一次抓取。

## 2. 证据范围与当前运行状态

当前审查的仓库 HEAD：`yijie 25d42ba`、`yijie-agent-host 8b6d7af`、`yijie-connectors 37552be`、`yijie-codex 5c64ed3f03`、`yijie-desktop eefb2ac`、`yijie-contracts 2592f5d`。除 Runtime 仓外，多仓存在用户原有未提交修改；审计依据包含这些修改，不将 HEAD 单独当成完整运行来源。

只读进程检查确认日常开发 App、Host、worker、Runtime 正在运行。检查时 PID 分别为 26036、26044、26048、26050。构建记录为 [startup-build.json](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/development/startup-build.json)。

| 核对项 | 结果 |
| --- | --- |
| Runtime | `codex-cli 0.144.6`；上游 `rust-v0.144.6 / 5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| 运行 Runtime SHA-256 | `e03bdbd2b4167022ee85c2df86dacff1a0a5c082321a9aa19875b29136a96cf5`，与 manifest 和启动回执一致 |
| Runtime 补丁 | manifest 记录 25 项，逐项与当前补丁文件摘要一致；包含来源投影、K3.1 适配、检索执行约束、工具发现等补丁 |
| Host SHA-256 | `c82c78520251e4e9f203eccf7390ae094e8d4539409ef6226a8bac5673066017`，与启动回执一致 |
| worker SHA-256 | `0d0e06815beb23fdbebb56a51c899ba226c7114f342ac21f2f6557101064cb50`，与启动回执及 current.json 一致 |
| 关键源码 | Host 的 market_turns、title、chat_models、kimi_k31_candidate、expert_instructions、session_protocol、tool_search；worker 的 broker、gateway、kimi_web、kimi_web_content、web_retrieval_generated；Native 的 connectors/startup，共 13 项与启动时源码摘要一致 |
| 原生搜索全局设置 | 实际 Runtime 命令行与受管 TOML 未显式覆盖 `web_search`；未启用 `standalone_web_search` |
| 模型接口 | Kimi：`https://api.moonshot.cn/v1`；MiniMax：`https://api.minimaxi.com/v1`；均 `wire_api=responses` |

受管配置见 [Kimi 配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/demo-fast/codex-home/yijie-chat-models-v2.toml) 和 [MiniMax 配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/demo-fast/codex-home/yijie-runtime-v1.toml)。只提取配置白名单字段，没有输出任何 Key。

上述检查证明当前程序与关键实现相符，不等于证明任意当前聊天都已选中连接器。每轮有效配置仍受 thread 的选集、专家、权限和 cwd 配置层影响。当前受管目录仅发现 5 个可读 rollout，合计 6 个 K3.1、1 个 M3 turn context，没有 `web_search_call`；这个小样本不能用于否定历史联网能力。Desktop 使用 SQLCipher，普通只读 SQLite 查询不可读取会话库，未尝试解密或修改，因此没有以数据库检查冒充当前 UI 选集确认。

## 3. 原生搜索：配置、请求、事件与显示

### 3.1 开关实际如何生效

固定 Runtime 的配置顺序是显式 `web_search` → 旧 feature 开关 → 默认 `cached`。每轮还结合权限约束决定最终模式。依据：[默认值与优先级](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/config/mod.rs:2451)、[默认 cached](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/config/mod.rs:3409)、[每轮权限解析](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/config/mod.rs:2807)。

| 情形 | 原生 hosted web_search | Kimi REST 工具 |
| --- | --- | --- |
| 普通聊天，未选中 kimi-web | 保留原生配置，通常 cached；完全访问可转 live | 不因已安装或已有 Key 就自动调用 |
| 本轮有效选中 kimi-web，prepare 成功 | 显式 disabled，Kimi 和 MiniMax 都如此 | 通过当前租约暴露，模型提议后仍须审批 |
| 清空 kimi-web 选集 | Host 不再写 disabled；正常 resume 重读普通 cwd 配置 | 当前轮不再获得该连接器工具 |
| 切模型但仍保留 kimi-web | 仍 disabled | 仍使用 Kimi Key 调用 Moonshot REST |
| 选集、授权、安装版本或 prepare 无效 | 返回错误，不静默退回原生搜索 | 不准入 |
| 有效专家角色 | expertThreadConfig 最终覆盖为 disabled | 是否可用仍看专家及当前选集策略 |
| 计划生成草案 input-only | disabled，工具面为空 | 不暴露 |
| 辅助标题生成 | 未显式关闭，见第 7 节的配置缺口 | 不复用普通聊天的 market prepare |

核心代码：[连接器覆盖](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_turns.go:121)、[start 合并](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:584)、[resume 合并](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:681)、[专家覆盖](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/expert_instructions.go:82)、[草案限制](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/scheduled_draft.go:92)。

### 3.2 原生搜索请求链

```text
Desktop 用户消息及当前模型／权限
  → Host thread/start 或 thread/resume 配置
  → Codex 根据有效模式构造 hosted ToolSpec::WebSearch
  → POST 供应商 /v1/responses，tools 内含 type=web_search，tool_choice=auto
  → 供应商云端判断是否检索、执行检索、将结果交给模型
  → web_search_call + assistant 响应
  → Runtime 原生 item → Host 事件／历史投影 → Desktop 搜索卡片
```

`cached` 生成 `external_web_access=false`；`live` 生成 true；`disabled` 不产生该工具。它们是 Runtime 发出的协议值；不能未经验证就假定第三方供应商完整实现了 OpenAI 的缓存／实时语义。依据：[hosted_spec](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/tools/hosted_spec.rs:14)。

这不是易界主动调用 OpenAI 搜索服务。当前 custom Responses provider 保留 hosted search 能力；独立 `web.run` 扩展另受 provider 与 feature 条件限制，不能和本链混用解释。依据：[hosted 工具注册](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/tools/spec_plan.rs:292)、[独立扩展限制](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/ext/web-search/src/extension.rs:39)。

原生 hosted 搜索在供应商内部发生，不经过 Kimi REST adapter 的逐次批准和一次 HTTP permit。`read-only`／`never` 主要约束本地执行，不能替代 `web_search=disabled`。Kimi 的服务端检索可能先于模型选择连接器工具发生，这正是 Host 必须在发模型请求前移除原生搜索声明的原因。

### 3.3 来源展示不等于正文抓取或逐句引用

运行补丁 0006／0007／0008 在 **K3.1 且请求确实包含 web_search** 时添加 `include=["web_search_call.action.sources"]`；不会给无搜索请求或 MiniMax 自动添加同一 include。0008 同时避免向 Kimi 发送不兼容的 `reasoning.encrypted_content`。

依据：[来源请求补丁](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0006-native-web-search-sources.patch:166)、[K3.1 模型适配](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0007-feat-164-kimi-k31-pro.patch:20)、[include 适配](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0008-feat-164-kimi-responses-include.patch:4)。

Host 读取可选 sources，做 URL／标题校验和去重，最多检查前 32 项；不制造缺失来源。Desktop 显示真实搜索 Item，同查询不同 Item 的重复搜索也保留。搜索来源列表不证明模型读取了整页，也不能自动证明某个回答句子与某条来源对应。依据：[Host 投影](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/native_process.go:55)、[来源上限](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/native_process.go:119)、[重复搜索显示](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/domain/web-search-presentation.ts:37)。

### 3.4 tool_search 是第三件事

`supports_search_tool` 和 FEAT-170 的 `tool_search` 用于发现 MCP 工具，不用于搜索互联网。目前普通聊天可为 Kimi 使用 `supports_search_tool=true / function_code_mode` 的目录，MiniMax 仍为 false；这不意味着 MiniMax 的 `web_search` 关闭。标题等辅助会话保留另一套工具发现目录，也不等于关闭了 hosted 网页搜索。依据：[目录覆盖](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/tool_search.go:13)、[普通线程选择目录](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/tool_search.go:67)。

## 4. 两个模型的官方云端联网能力

| 对象 | 当日官方证据 | 本次结论边界 |
| --- | --- | --- |
| Kimi K3.1 Pro | Responses API 的 web_search 示例明确指定 kimi-k3.1-pro，搜索在服务端完成 | 支持。请求须声明工具；同一模型的快速开始页仍提示搜索正在更新，不建议近期生产使用 |
| MiniMax 服务／M3 接入通道 | Server Tools 文档明确支持 Responses 与 Anthropic Messages 的 web_search，标注 Beta；Responses 文档仍描述 M3 参数 | 平台有内置云端联网，易界 M3 使用支持该工具类型的 Responses 通道并会声明工具。最新工具示例是 M3.1 Flash，本次未实测 M3，因此不将服务能力推断写成当前 M3 账号成功验收 |
| Moonshot 三项 REST 工具 | 官方 Basic／Pro／Fetch 独立 API | 独立于推理模型选择；M3 调用它们也使用 Kimi 凭据和 Moonshot 服务 |

官方来源（2026-11-15 核对）：[Kimi Responses API](https://platform.kimi.ai/docs/api/responses)、[K3.1 Pro 限制说明](https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart.md)、[MiniMax Server Tools](https://platform.minimax.cn/docs/guides/server-tools)、[MiniMax Responses API](https://platform.minimax.cn/docs/api-reference/responses-create)、[Kimi 三项 API 分工](https://platform.kimi.ai/docs/guide/best-practices-for-web-search)。

不能用 MiniMax 老 `MiniMax-Text-01 / chatcompletion_v2` 的搜索示例替代 M3 的 Responses 证据，也不能把 MiniMax MCP 套餐搜索当成本项目已经接入的搜索实现。这里的“内置”指供应商托管工具，不指模型参数天然实时更新。

## 5. Basic／Pro／Fetch 何时启用

这三个接口应分别称作 Basic、Pro、Fetch，不是三个都属于 Basic。

| MCP 工具 → REST | 模型应选择的任务 | 易界发送参数 | 返回与时限 |
| --- | --- | --- | --- |
| kimi_web_search → POST /v1/tools/search | 只列标题／摘要／链接、找官网；无站点／日期限定且不做问答分析 | text_query；limit 默认 5、1–20；include_content 默认 false；timeout_seconds=10 | 标题／URL／摘要；本机最多 15 秒，受剩余租约约束 |
| 同一 Basic，include_content=true | 用户明确需要采集正文自行加工 | 同上，显式 include_content=true；timeout_seconds=30 | 增加 text、content_status、dropped_results；发送前必须有完整 35 秒执行预算 |
| kimi_web_search_pro → POST /v1/tools/search_pro | 联网问答、事实核查、研究、总结、RAG；没有过滤条件也优先 Pro | text_query；limit 默认 5、1–20；timeout_seconds=30；只传用户明确要求的 sites（最多 5、OR）／time_window | 按网页关联的 chunks／score，以及站点、日期、authority 等；完整 35 秒预算；片段不等于全文 |
| kimi_web_fetch → POST /v1/tools/fetch | 用户明确要求读取已知公开 URL，或需要进一步核对搜索结果页当前正文 | 仅 url | 标题与 Markdown；本机最多 15 秒，受剩余租约约束；不承诺登录态、JS 控制或历史快照 |

权威描述与预算：[tools.json](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/compatibility/web-retrieval/tools.json:8)。实际参数映射：[Arguments::body](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:127)。

例如“列 5 个官网链接”应选 Basic；“查这些规则并比较差异”应选 Pro；“读取这个 URL 的全文”应选 Fetch。代码没有强制每次先 Basic 再 Pro 或 Fetch；Pro 结果也不会触发 adapter 自动逐页 Fetch。模型选择仍可能偏离描述，历史 Alpha 曾出现纯列表误选 Pro。

### 5.1 从本地准备到实际付费请求的分界

1. **安装／准备。** Native 创建默认安装；启动恢复通过既有 enable/probe 链处理，保留后续显式停用／卸载。Host 复用已加载的 Kimi 模型 Key，用匿名 FD3 启动管道给 worker；不额外要求第二份 Key。Probe 只检查本地凭据快照和 canonical 工具定义，不访问 /models、余额或三个 REST 端点。`ready/connected` 不是供应商鉴权或余额验证。
2. **本轮选用。** 用户在会话选中连接器；全局安装／启用与本轮选集不同。Native 冻结服务引用、安装 generation/revision 和选集摘要。非空选集要求 ask 模式；仅换成 MiniMax 模型不会取消已选 Kimi 工具或换掉它的凭据。
3. **Host prepare。** 校验当前 scope、snapshot、服务绑定；worker prepare 成功取得 lease/capability 后，将 loopback MCP Gateway 写进 thread 配置，并关闭原生搜索。新 prepare 成对携带 webRetrievalVersion=0.3.0、mcpToolTimeoutMs=60000；失败直接返回错误。
4. **工具发现及提议。** Codex 使用原生 MCP 机制发现工具。Kimi 在普通聊天的 tool_search 配置下可先延迟发现再加载；发现工具不执行搜索、不提供审批。模型按描述决定具体工具和参数，tool_choice 保持 auto。
5. **逐次审批。** Gateway 绑定真实 thread/turn，冻结参数与 schema 摘要；使用原生 MCP elicitation 和 Host/Native 对同一 call 的决定。Broker 必须同时看到原生接受和 Approved 状态，才能消费执行许可。当前代理的 default_tools_approval_mode=approve 只消除重复的前置工具确认，不免除这条业务调用审批。
6. **一次实际请求。** worker 串行复查取消、期限、参数和凭据；一次性 permit 在唯一 POST 前消费。固定目标是 api.moonshot.cn 的三个端点，目标网页 URL 只是 Fetch 参数，本机不直接爬取网页。
7. **返回与续答。** 校验并归一化供应商返回 → 相同语义的 MCP 文本 JSON 与 structuredContent → 原生 MCP item/工具结果回灌 → 当前推理模型继续回答。Desktop 使用 WebRetrievalResult 展示；不伪装成原生 web_search sources。需要再 Fetch 就是另一项工具提议与审批。

证据：[Native 启动恢复](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/connectors/startup.rs:25)、[默认安装](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/connectors/store_builtin.rs:5)、[Key 管道](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/marketbroker/model_credential.go:14)、[Host prepare](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_turns.go:56)、[代理审批配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_turns.go:112)、[Gateway elicitation](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/gateway.rs:162)、[双状态准入](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/broker.rs:1044)、[唯一发送点](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:410)、[UI 结果选择](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/components/chat/MarketChatActivity.vue:95)。

## 6. 时限、失败、重试及结果边界

Pro 和 Basic 正文模式设置双截止：

```text
D = min(lease 截止, call 创建时刻 + 最大审批 TTL, prepare 时刻 + 60 秒)
A = D − 35 秒 HTTP 执行预算 − 2 秒审批投递余量
```

首次调用在理想情况下也只有从 prepare 算起最多约 23 秒的审批机会；模型生成、MCP 初始化、工具发现和排队均会消耗它。若创建 call 时已经到 A，则不创建审批、不发送外部请求；及时批准后仍可执行至 D。发送前余量不足完整 35 秒也不发请求。不是“用户看到按钮以后一定有 23 秒”。默认 Basic 和 Fetch 不使用这套完整 35 秒预算，保留 min(剩余时长,15 秒)。依据：[prepare 时钟](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/broker.rs:490)、[双截止](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/broker.rs:979)、[发送前预算检查](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:295)。

adapter 显式设置 reqwest retry::never()、redirect::Policy::none()；没有后台刷新、自动重试、接口切换或自动链接抓取。取消后已发请求仍可能收费；完成前正常保留有界请求 owner，不强杀进程。依据：[HTTP 客户端](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:175)、[关闭流程](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:230)。

上游原始响应最多 1 MiB；完整 MCP 封包（包含重复的 text JSON 与 structuredContent）最多 65536 字节。正文／摘要只在 UTF-8 边界裁剪，不截断 URL；正文模式使用 available/unavailable/truncated 及 dropped_results。原始空搜索是成功空列表；全部页无效是 invalid_response；空 Fetch 正文是 no_content。客户端过滤或截断后为空，不代表供应商没有计费。依据：[归一化与封包预算](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:509)、[正文模式](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web_content.rs:109)。

“REST adapter 不重试”不能扩展到模型请求：当前 Kimi 明确 request_max_retries=0、stream_max_retries=0；当前 MiniMax 受管配置及进程启动参数没有同样的覆盖，继承 Runtime 的请求最多 4 次重试、流重连最多 5 次默认上限（只在相应错误条件触发，不是每轮固定执行）。因此供应商 hosted 搜索的费用和重试边界不能照搬 REST 一次许可。依据：[MiniMax 配置生成条件](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/provider.go:267)、[Runtime 默认重试值](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/model-provider-info/src/lib.rs:26)、[解析方法](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/model-provider-info/src/lib.rs:301)。

Host 指令还要求尊重选中检索服务，不为同一信息需求混用 native 与 connector，不用 curl/脚本绕过；首个检索失败须说明证据与影响。Runtime 的 0012 检索执行补丁也识别原生搜索和三个 Kimi 工具。这里不存在“Pro 失败就自动换原生搜索”的正式回退链。依据：[运行指令](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/runtime_permissions.go:17)、[失败规则](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/web_retrieval_instructions.go:4)、[执行补丁](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0012-web-retrieval-execution-guard.patch:186)。

## 7. 审计发现与处理优先级

| 发现 | 影响与证据 | 建议（本次未实施） |
| --- | --- | --- |
| P2：标题生成缺少硬配置隔离 | GenerateTitle 只写“Do not call tools”，未写 web_search=disabled 或 input_only；临时 cwd、read-only 和 ephemeral 均不等于关闭 hosted 搜索。现有 surface 测试的 title 分支仅返回标题，不断言工具表。静态链路表明不能保证标题请求零联网；未证明实际发生了额外搜索或计费 | 若标题职责仅为文本摘要，应复用原生禁搜索配置，并用普通 loopback 请求检查实际 tools；不靠提示词保证 |
| P2：Pro／Basic 正文窗口受模型耗时挤压 | prepare 在模型请求前，A 最迟为 prepare+23 秒；历史 Alpha 的 E6 已因此在审批前过期 | 设计时单独评估模型时间、审批时间与执行时间，按现有契约治理改进；不能只改 UI 倒计时 |
| P2：两种模型重试策略不同 | Kimi 显式零重试，MiniMax 当前继承 4/5 默认值；原生 hosted 搜索不走单次 REST permit | 明确产品层两条链的成本／重试承诺，增加正常响应与可恢复错误的非破坏性证据 |
| 文档滞后 | Host 文档仍写仅 K3.1 选连接器时关闭搜索、切模型恢复；实际实现无模型限制，测试覆盖 MiniMax 仍选 connector 时关闭原生搜索。早期 Basic/Pro 文档的“未实测”也已被后续 Alpha 记录更新 | 同步当前生效矩阵与历史证据范围，避免照抄较早章节 |
| 来源资格有边界 | Kimi 请求显式 sources，MiniMax 没有同样的 include 适配；sources 仍是可选字段，缺失不能直接判定未搜索。Alpha 不核对回答质量／引用关系／账单 | 分开验收调用成功、来源返回、逐句证据支持和费用；不将搜索卡片视为质量验收 |

标题证据：[GenerateTitle](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/title.go:125)、[现有 title 测试分支](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/feat164_surfaces_integration_test.go:118)。文档对照：[旧 Host 说明](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/docs/feat162-basic-pro-local.md:11)、[当前双模型测试矩阵](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_search_routing_test.go:154)。

## 8. 验证结果与未执行项

本次执行以下三个无外部请求、无进程故障注入的配置测试，全部 PASS：

```text
go test ./internal/codex -run '^(TestFEAT162SelectedRetrievalConfig|TestFEAT158ExpertWebSearchOverridePreservesOrdinaryConfig|TestToolSearchCatalogPreservesOtherCapabilities)$' -count=1 -v
```

它们分别核对选集条件覆盖、专家覆盖不污染普通配置、工具发现目录不改动其他模型能力。它们不证明真实供应商联网、当前 UI 选择或端到端执行成功。

已有真实证据：2026-10-30 FEAT-162 的 E1—E7 累计 Alpha 已通过，覆盖 Basic 摘要、Pro、Fetch、Basic 正文、跨回合 Basic→Fetch、无筛选 Pro、同回合 Pro→Fetch。它跨三个 generation，保留此前 E1/E6 和额外调用失败；只核对必要工具成功及回答可见，没有验收回答质量、来源对应或费用对账，也不是同一 fresh run 的严格 D4。依据：[43 号关闭记录](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/docs/features/FEAT-162-kimi-web-retrieval/43-alpha-results-and-closure.md:1)、[44 号复审](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/docs/features/FEAT-162-kimi-web-retrieval/44-alpha-final-reaudit.md:1)。

未执行：当前账户真实模型／Basic／Pro／Fetch 请求、当前 UI 选集操作、供应商账单核对、全量回归、服务重启或构建；因此不声称当日供应商可用性和端到端质量已通过。用户禁止的强杀、可执行文件替换、权限破坏和攻击 fixture／注入测试均未执行；本审计不依赖这些行为，也不将未测路径记为通过。
