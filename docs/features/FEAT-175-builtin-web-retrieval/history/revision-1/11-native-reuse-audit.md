# FEAT-175 原生复用与缺口审计

2026-11-15，只读源码审计。当前工作树与相关源摘要见 references/source-evidence.json；未运行产品。当前固定 Runtime 为 0.144.6，上游 5d1fbf26c43abc65a203928b2e31561cb039e06d，现行补丁链已包含 tool_search／检索 guard；不将未接入能力误判为 Runtime 不支持。

## 能力清单

| ID | 实际源码证据 | 事实与设计决定 |
| --- | --- | --- |
| S01 | [配置默认](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/config/mod.rs:3409) | 原生默认 cached；模式解析、权限配置已存在，Host 不重写搜索模式引擎 |
| S02 | [hosted 工具计划](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/tools/spec_plan.rs:292) | hosted spec 与普通 MCP 均由原生工具计划构建；不是本地执行 REST 的同一能力 |
| S03 | [MCP 配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/config/src/mcp_types.rs:160) | enabled、required、enabled_tools、tool_timeout_sec、default/per-tool approval 均已存在 |
| S04 | [只读审批判定](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/mcp_tool_call.rs:2163) | auto＋非 destructive＋readOnly 可默认执行；不用永久 approve 或制造批准 |
| S05 | [pre-call 审批](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/mcp_tool_call.rs:1203) | 原生先决定是否询问，允许后才进入实际 execute；可将用户等待置于供应商执行之前 |
| S06 | [有效时间计时](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/rmcp-client/src/rmcp_client.rs:181) | active_time_timeout 在 elicitation pending 时暂停，而非固定墙钟总期限 |
| S07 | [elicitation pause guard](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/rmcp-client/src/elicitation_client_service.rs:70) | 真实 create_elicitation 自动 enter/drop 暂停状态；不是仅有未使用类型 |
| S08 | [实际 tools/call](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/rmcp-client/src/rmcp_client.rs:599) | 调用进入原生 run_service_operation；重试分类只为 tools/list，不能认为 tools/call 已自动重试 |
| S09 | [Host 反向入口](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:315) | 非市场 elicitation 当前直接 decline；需要薄的标准协议／UI 消费，不改 Runtime |
| S10 | [回调生命周期](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/protocol.go:332) | Server request 使用 Client requestContext；不是通用 30 秒 RequestTimeout 自动覆盖所有审批 |
| S11 | [旧 Broker 截止](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/broker.rs:979) | 新正文模式 D 受 prepare+60s 限制，A=D−35s−2s；这是本次要从内置路径移除的约束 |
| S12 | [现有 REST adapter](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:127) | 工具名确定 endpoint／参数；已有禁重试、正文预算和归一化，复用而非重写 |
| S13 | [现有工具权威](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/compatibility/web-retrieval/tools.json:8) | 旧描述要求普通问答优先 Pro，与本需求冲突；三工具名称和结果可保留 |
| S14 | [名称识别约束](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0012-web-retrieval-execution-guard.patch:201) | 原生检索 guard 匹配三个稳定工具名后缀；仅更换 server namespace 仍可识别 |
| S15 | [专家禁用](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/expert_instructions.go:82) | 任意非空角色统一 disabled；移除此条件，保留实际限制与媒体选源 |
| S16 | [Kimi 工具发现目录](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/tool_search.go:13) | 已有模型作用域配置／BM25／Code Mode 路径；MiniMax 仍使用既有直接工具方式 |
| S17 | [应用内置 MCP 先例](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/media_generation.go:25) | 自动装配、leaf config、MiniMax namespace 适配和 per-tool policy 可作为模式；不把媒体业务代码复制到网页领域 |
| S18 | [既有网页 renderer](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/components/chat/MarketChatActivity.vue:95) | 结果组件目前位于市场活动下；新普通 MCP 表面需实际接线 |
| S19 | [native MCP 投影](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/native_mcp.go:19) | 已有真实 Item 到显示数据的边界，不应建立独立网页工具事件生命周期 |
| S20 | [turn/start 参数](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/turn.rs:68) | 不能杜撰逐轮 task-intent 或任意 config 字段；通用配置在 thread/start/resume，需沿已验证生命周期使用 |
| S21 | [API 开关与边界](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-api/internal/app/app.go:139) | 既有身份代码有本地实验资格约束，public-ready 必须重新验明，不能从目录存在推定生产可用 |
| S22 | [当前凭据快照](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/marketbroker/model_credential.go:14) | 旧工具复用本机模型 Key，不满足新用户无搜索 Key；新内置路径改为服务端运营凭据 |

## 最大复用的实际含义

复用 Runtime 的配置加载、工具集合、MCP transport、tool_search、Code Mode、原生批准、取消、item 和回灌。Host 只装配与投影；Connectors 执行供应商协议；API 拥有产品身份／费用事实。没有新的 Host planner、搜索意图模型、工具缓存、MCP 调度器、审批决定状态机或模型补答循环。

原生工具发现支持不等于自然语言路由确定。独立 web.run 扩展也受 provider 条件限制，不是可直接将 Kimi REST URL 填进去的通用搜索引擎。三项工具名称保留保证已有 guard 有效；其他字段仍需新消费者 conformance。

## Fact / Assumption / Unknown / Conflict

- Fact：用户确认托管／自动只读；上述配置、暂停计时和 helper 在固定源码存在；Host、UI、凭据入口有明确接线缺口。
- Assumption：正常易界产品会话是公开服务身份入口；本期不另做完全匿名补贴。若产品需无任何 App 身份，访客资格须另审。
- Unknown：公开身份激活基线、真实云延迟和限额、双模型路由评测结果；当前没有新的运行证据。
- Conflict：旧专家 blanket 禁用和旧 Pro 普通问答优先描述与新需求冲突；旧市场强制选择／审批与内置体验冲突；已在方案中明确替代范围。

## 官方外部依据

- [Kimi Responses API](https://platform.kimi.ai/docs/api/responses)：服务端可在模型工具选择前决定检索，解释默认并存的排他限制。
- [Kimi 检索最佳实践](https://platform.kimi.ai/docs/guide/best-practices-for-web-search)：三独立 API、Pro filters/chunks、Fetch 正文能力。
- [Kimi 定价](https://platform.kimi.com/docs/pricing/websearch)、[MiniMax 定价](https://platform.minimax.cn/docs/pricing/overview)：2026-11-15 在本聊天已读取官方当前页面；价格不等于本期费用授权。
- [MiniMax Server Tools](https://platform.minimax.cn/docs/guides/server-tools)：云端 web_search 为 Beta；M3 当前账号真实资格不由文档阅读代替。

没有访问用户 Keychain、模型 Key、生产账户或第三方付费端点。仅源码／文档阅读，不把静态审计写成运行通过。
