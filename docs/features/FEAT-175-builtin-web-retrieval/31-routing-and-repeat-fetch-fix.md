# FEAT-175 研究选路与重复 Fetch 的定位及最小修复

2026-11-16。用户要求先定位原因，再做最小产品修复。本轮不新增真实模型或付费搜索调用。`contract-impact=semantic`：调整模型可见的工具指导及 MCP 标准初始化元数据；FEAT-175 整体 breaking 状态保留。输入、结果、错误、权限、费用准入和持久化格式未变，旧市场检索描述也未变。

## 已确认的原因与边界

**研究工具的指导存在重叠。** P03 的真实 `tool_search` 返回了 Basic、Fetch、Pro 三个完整定义。Pro 当时只说适用于研究／比较／证据，Fetch 同时允许读取已选研究来源，缺少冲突时的优先次序。`yijie_web` 命名空间只有原生兜底文案 `Tools in the mcp__yijie_web namespace.`；产品没有提供 MCP `instructions`。这是可以确认并修正的指导缺口，不能把它说成已证明模型全部内部决策原因。

**重复发生在新的模型调用层。** 三个不同的 Code Mode `exec` 调用分别执行同一个 URL，每次都有 `text(r)`，各自创建新的服务端 operation，均返回成功。三份 Markdown SHA-256 完全一致，16,993 字符、459 个换行，`truncated=true`。现有 `normalize_fetch` 对超出结果字节上限的正文截断；Fetch 入参仅有 `url`，没有分页、offset 或可调正文上限。同一页面与同一上限下重读不能补齐后半页。旧描述没有解释这个返回标志的后续处理方式。

实际发现输出只提供输入参数和 `Promise<unknown>`，没有向模型展开 Fetch 的输出 schema；不能依赖输出 schema 中的字段定义来代替模型可见的截断说明。额外确认 `text(r)` 将 MCP 的 `content` 和 `structuredContent` 两份相同数据都打印了出来，扩大了输入上下文；这不是换行解析错误，也不足以单独证明它导致了重复。

**Kimi 的供应商预搜索须单列。** 官方 Responses 说明：声明 `web_search` 后，供应商按输入判断并执行预搜索，发生时在输出前部提供 `web_search_call`。因此 hosted item 先出现不能单独证明模型优先选择了哪一个客户端工具。本次客户端第一个检索工具确实是 Fetch，Pro 为 0，P03 原有未通过结论不变。后续应分别记录供应商检索活动、首个应用检索工具和完整任务结果。[官方 Responses 文档](https://platform.kimi.com/docs/api/responses)

还核对了同页公开 schema：`function_call_output.output` 支持字符串及 `input_text` 数组。当前 Code Mode 输出数组有官方协议依据；本次没有证据支持修改或替换 Runtime 的输出序列化。

## 最小产品变更

唯一执行代码变更是在共享 worker 的 `WebGateway::get_info()` 加入原生 MCP `.with_instructions(...)`。指导来自 Contracts `policy.json`，由原 generator 生成 Go／Rust 常量，再通过原四消费者同步。另更新 Pro／Fetch 的同源工具描述：

- 普通问答通常使用原生搜索；显式研究、比较、正文证据或站点／时间过滤，优先选择 Pro 作为应用检索，并传入 `sites`／`time_window`。查询词里提到站点不能代替过滤参数。
- 纯来源列表使用 Basic；用户明确指定 URL，或 Pro 后仍需要某个已选来源正文时使用 Fetch。
- 成功且截断的结果是可用的部分证据。先使用已返回内容；不足时改用聚焦的 Pro 查询，或说明缺口。相同信息需求下，不能通过原样重复成功的 Fetch 获取尾部。用户明确要求刷新另行判断。
- Code Mode 中优先读取／输出已有 `structuredContent`，保留错误与截断信息，避免重复打印同一份正文。

原生复用依据：固定 Runtime 的 `codex-mcp/src/rmcp_client.rs` 将 MCP `instructions` 转为 `namespace_description`；`core/src/tools/handlers/mcp.rs` 将它用于工具发现和命名空间描述。Kimi 的原生工具发现携带该描述；MiniMax 当前原生模型配置将工具展开为独立函数，分别消费对应的工具描述。因此共同关键规则也保留在 Pro／Fetch 的描述中，没有假设 MiniMax 接收相同的 namespace JSON。

没有增加 Host 意图分类器、搜索调度器、结果缓存或新状态；没有关闭研究会话的原生搜索，也不承诺阻止供应商自动预搜索。MCP 风险注解与原生只读自动执行保持既有语义。

## 定向验证与交付

- 原生协议定位先用原 canonical worker：Kimi 模型侧命名空间仍为兜底说明。初版验证曾错误要求 MiniMax 首次请求也有 namespace；依据实际扁平函数协议修正验证入口，未修改模型配置或 Runtime。
- 标准脚本构建新 worker；复用日常 App 的固定 Runtime `e03bdbd2…`，在两模型配置下验证真实 MCP 初始化／发现及模型侧请求内容。Kimi 命名空间指导和两模型全部三工具描述均匹配同源政策，race 检查通过。合计 5 次本机合成模型 HTTP、2 次正常本机准入拒绝，供应商请求 0。这不证明模型会遵循指导。
- FEAT-175 既有 7 项契约检查和四消费者源／生成一致性通过。与上一批 App 构建相比，7 个输入／结果／HTTP／旧工具源逐字节保持。源码复审只包含政策、generator、一个 worker 接线及原有定向用例；没有扩建 A0 或全量回归。
- 正常 App 的 build-only 装配已通过（`c6557ca4-b1f2-4ba1-9ea5-5f012fc63014`），默认 worker 为已验证的 `89d2ced0…`，Runtime 保持 `e03bdbd2…`。App、队列和模型没有启动；专用服务正常停止，活动委托和非终态检索为 0，历史检索操作仍为 3。详见 `references/routing-fix-result.json`。正式发布、真实模型行为改善、重复 Fetch 是否实际减少均未声明通过。

装配时遇到此前已有的同步生成器等待：只读采样显示 `gofmt` 等待 stdin 读取结束。为完成装配，对 `sync-model-call-surfaces-v2.mjs` 的这一调用改用新建临时普通文件作为 stdin；仍执行原 `gofmt`，并在完成后清理自建临时目录。三个 family 的规范源记录及两消费者来源由原 generator 同步；46 个生成文件逐字节保持，双消费者检查通过。该构建修正不改变产品 wire／持久状态，单项 `contract-impact=none`。没有据此宣称已确定上游 Node 的内部根因或解决其他历史格式工具等待；失败构建记录保留，所有进程退出使用正常停止／中断，没有强杀。

本机原始定位、最小源码 diff、构建与协议日志位于工作区 `.local/feat175-routing-fix-20261116/`。本轮没有付费重跑 P03，也没有消费上批未运行的五项。
