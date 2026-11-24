# 聊天中显式选用连接器

2026-11-23，FEAT-157 本地开发客户端。用户确认，聊天框的选择表达当前对话要使用哪些服务。单选时，匹配的步骤优先交给所选服务。多选时，按任务分工使用相关服务。

2026-11-24 补充。发送时勾选的连接器等同于用户在这条消息里点名，识别指代时优先于历史话题。单选后问“我如何使用这个连接器”，应点名当前服务，按它实际开放的能力说明用法。仅询问用法无需发起业务调用。多选时按当前问题匹配，仍无法确定“这个”指谁才询问用户。清空选择后，先前勾选的服务只作为对话历史。

## 链路审计

| 环节 | 实际行为 |
| --- | --- |
| 对话选择 | 管理页启用服务后，用户在聊天框另行勾选。桌面端按对话保存选择。发送成功后，新任务将选集转入新会话，每次发送读取当时的选择。[当前交互](../../../../yijie-desktop/docs/design/docs/design/05-patterns/02-chat-workspace.md#连接器当前对话选用与全局管理2026-11-23-更新) · [发送入口](../../../../yijie-desktop/src/pages/chat/ChatPage.vue) |
| 提交与派发 | Native 校验安装引用、版本与权限，将选集与内容、模型、操作编号一并冻结。派发时将引用解析为服务 ID。Host 重读已受理操作的原回执，新操作通过 Worker 准入后建立当前轮次的网关。[提交](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs) · [派发](../../../../yijie-desktop/src-tauri/src/chat/connectors/dispatch.rs) · [Host 受理](../../../../yijie-agent-host/internal/session/market_submit.go) |
| 模型选工具 | Worker 仅提供该次选集中已就绪服务的工具。MiniMax 使用直接函数，Kimi 支持原生工具发现。原有优先指令覆盖信息检索。19:37 的二维码任务只选了草料，Host 已受理，Runtime 列出 63 个市场工具，模型随后直接在本地安装依赖并制码。草料业务调用为零。[工具发现](../../../../yijie-connectors/worker/src/broker.rs) · [原检索规则](../../../../yijie-agent-host/internal/codex/runtime_permissions.go) |
| 调用、执行与结果 | 模型发起 MCP 请求后，Gateway 核对 thread、turn、工具和参数。Worker 依据该笔原生决定消费许可并访问供应商。Host 按调用和轮次关联回执，桌面端展示实际结果或失败。[Gateway](../../../../yijie-connectors/worker/src/gateway.rs) · [回执关联](../../../../yijie-agent-host/internal/session/market_correlation.go) |

## 方案审计与验收要求

1. 每轮向模型明确当前选中的服务 ID。数据源取自 Host 已验证、与冻结选集逐项对应的服务绑定。模型可由 ID、工具描述和现有发现机制识别相关操作。用户名、安装引用、凭据引用、网关地址和供应商文本均不属于名单。
2. 单选且有合适工具时，先调用该服务。多选时，按步骤匹配服务能力，重叠能力选一个即可，只有任务明确需要多个来源时才重复同一查询。无关步骤、结果校验及文件排版可继续用普通工具。服务不可用、拒绝或结果不确定时说明实际情况，改用其他方法完成同一步骤前尊重用户选择。原生审批、拒绝和取消继续生效。
3. 复审发现，旧对话恢复时开发指令可留在历史里。选集属于当前请求，因此复用固定 Runtime 的 `thread/start` 和正常卸载后的 `thread/resume` 的 `baseInstructions`，与既有专家组合。重新选择、清空、切模型均以本次准备结果为准。用户消息正文保持原文。网关持有真实调用权，模型按具体任务匹配，Host 无需新建分类器或执行器。
4. 离线检查覆盖单选、多选、无关步骤的规则、清空和跨模型恢复，以原生 Runtime 发给本地模型端的请求核对组装。用已授权的一个真实 MiniMax 对话验收草料，正文只描述任务，从实际调用与交付回执判断结果。多选与单服务真实调用的证据分别记录。

`contract-impact = semantic`。变化是 Host 对现有用户选择的模型指令映射。所有数据走原有选集、原生模型请求和 MCP 接口。兼容基线为 Host `d9857e71a0fb56db620332142d5b9009e10e3d83`、Contracts `1fe3b17bb6f1bc4be48f6988035639606e972c9c` 和固定 Runtime 仓 `ba36804266f61a23b665fd3a6efde3c4992e3561`。旧记录可原样读取。回滚时恢复原 Host 指令组装并通过开发入口正常重启。

## 实现与定向验证

Host 在 Worker 接受本轮选择后提取服务 ID，按名称排序、去重，以相同方式组装新对话和恢复对话的当前指令。显式清空会向模型说明早先选集已成为历史。具体的服务操作、输入参数和执行结果仍由当前网关提供。[选择与准入](../../../../yijie-agent-host/internal/codex/market_turns.go) · [新建与恢复](../../../../yijie-agent-host/internal/codex/session_protocol.go)

| 验证面 | 本机结果 |
| --- | --- |
| 桌面选择 | 13 项通过，覆盖同一聊天选择和取消、两个聊天隔离、断连恢复、双选及移除。 |
| Host 与固定 Runtime | 11 项 Go 定向测试通过，包括四次模型请求中从普通会话到双选、缩为单选并搭配专家、清空的实际输入检查。七次检索回环覆盖首次与续轮、重新选择和跨模型切换。另验原生发现、Gateway 拒绝零外发、已受理操作重读、取消和回执关联。`go vet ./internal/codex` 通过。早期一次使用不配对的 Runtime 运行旧配置测试，来源校验拒绝启动。随后按当前与旧基线各自登记的制品复跑。 |
| 多服务 Gateway | Worker 定向用例通过。同一租约中的两项本地协议服务，实际调用对应操作的服务一次，另一项零次。该用例覆盖工具分发与单次审批。模型自主选择多服务的线上表现尚无本轮实测。 |

## 草料真实验收

北京时间 20:26:48 至 20:33:14，通过标准入口更新后的日常客户端完成一个 MiniMax-M3 对话回合。聊天框单选草料，正文仅要求为百度网址创建一个静态码并交付一页 PDF。Native、Host 受理和工具执行回执中的选集摘要一致。模型首个工具调用为草料 `static_qrcodes_create`，同时发起的本地命令只检查 PDF 排版环境。通过「允许一次」后，Worker 消费一次许可，向草料发出一次业务请求，得到 HTTP 200、成功状态、静态码 ID 和图片地址。

本轮下载草料返回的码图，使用已有 Python 做 PDF 排版，新增软件包为零。中间版 PDF 渲染时缺少码图，模型在同一回合重新嵌图。最终产物「百度静态二维码.pdf」已提交，桌面端确认收到。独立检查得到一页 A4，嵌入图像与草料原图的 400 × 400 像素逐一相同；Poppler 渲染后由 macOS Vision 识别到一个二维码，内容为 `https://www.baidu.com`。[脱敏验收证据](evidence/2026-11-23-selected-connector-routing.json)

## 2026-11-24 微博切换到 Tushare 的修复记录

**真实客户端的连接器指代验收通过。** 当天 12:04 的原始故障中，桌面端只提交了 `tushareMcp`，Host 回执摘要一致。MiniMax-M3 仍按上一轮微博话题检索并作答。原始 Runtime 轮次为 `01a20bba-45a2-7b80-af19-cfff33b0aa9e`。

Host 从本轮已核验的选择中提取公开服务 ID。除更新基础指令外，还在提交用户消息前通过固定 Runtime 的稳定方法 `thread/inject_items` 写入一条简短的开发者上下文，标明这条消息显式选用了哪些服务。选择与用户原文各自保存，下一轮重新记录当时的选择，包括显式清空。Host 在同一把线程操作锁内依次提交上下文和 `turn/start`。这条上下文只标识本轮选择，实际执行继续由网关和原生权限控制。`contract-impact = semantic`。[上下文生成](../../../../yijie-agent-host/internal/codex/market_turns.go) · [发送入口](../../../../yijie-agent-host/internal/codex/session_protocol.go)

| 检查 | 结果 |
| --- | --- |
| 固定 Runtime 发往本地模型端的请求 | 新增用例在只更新基础指令的版本上失败，修复后通过。用例同时检查旧微博回复仍在历史中，新选择出现在旧回复和当前用户消息之间，用户消息仍为原句。也覆盖普通会话、多选、与专家指令组合及清空选集。[回归用例](../../../../yijie-agent-host/internal/codex/market_search_routing_test.go) |
| 相邻行为与静态检查 | `TestFEAT162SelectedRetrievalConfig`、`TestFEAT162SelectedRetrievalRuntime`、`TestFEAT157MarketNewTurnAcceptedReplayContinuationAndModelClear` 和 `go vet ./internal/codex` 通过。检索回环使用配对的 `native-public-messages-r3` 制品，显式提及用例使用配对的 `tool-search-v1` 制品。 |
| 首次真实客户端验收 | 北京时间 13:51 单选微博，13:52 改为只选 Tushare。两个 Host 回执均受理，市场工具由 75 个变为 1 个，但第二轮回复仍介绍 `weibo_*`。这一版只在基础指令中说明选集优先。 |
| 修复后的真实客户端验收 | 正常重启后打开原聊天。14:03:59 单选微博提问，回答微博开放平台能力。14:05:35 取消微博、单选 Tushare，原样发送“我如何使用这个连接器”。14:05:54 回复说明如何使用 `tushare_daily`、`ts_code` 和 `trade_date`。四轮共用一个 Runtime 线程。两次复测的桌面选集摘要均与 Host 受理回执一致，原句与客户端消息记录一致。[客户端和执行回执](evidence/2026-11-24-connector-mention-client.json) |

最后一轮虽然只询问用法，模型仍在完全访问模式下实际查询了一次示例行情。Runtime 与 Worker 的调用引用一致，目标为 `tushareMcp.tushare_daily`，供应商返回 HTTP 200。该轮微博业务调用为 0 次。
