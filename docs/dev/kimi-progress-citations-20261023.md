# Kimi-K3 公共进度与引用审计（2026-10-23）

状态：分层审计和 1 次真实诊断回合完成；提示词修复未达到独立进度/引用验收目标，不能标记整体 PASS。
用户追加要求先深度审计现有 Runtime 并考虑独立进度方案；下文给出可复用入口和实施边界，
进度来源的产品选择已通过会话澄清问题提出，未把系统说明冒充模型发言。

范围：承接 2026-10-22 的过程展示修复，沿用 local/demo_fast、Kimi-K3/max、完全访问权限。
不伪造 assistant 进度、搜索来源或答案引用；不改写旧会话、原始 phase、审批或执行事实。
本轮用户明确要求继续修复并真实验收，普通同题验收通过产品 UI 发送。

`contract-impact = none`（当前改动）：通过既有 baseInstructions/developerInstructions 更新
普通助手的输出指引；增加现有开发回环计数器的可选脱敏诊断，不改变产品 wire、模型路由、
Runtime 协议、数据库或权限语义。诊断产物仅为本机不可发布验证资料，不被产品消费。
若后续需要扩展 Runtime 或公共投影，先重新分类并走既有 source-first 链路。

## 已确认的链路事实

- 前轮成功回合的 Runtime rollout 只有 1 条 phase 缺省的 assistant 最终消息、1 次网页搜索和
  1 条空摘要 Item。Host/Desktop 没有收到独立公共进度可供展示。该文件已经过 Runtime 解析，
  单靠它不能证明原 Provider 从未提供其它字段。
- 固定 `yijie-codex` 的 `protocol/src/models.rs`：Message 保留可选 phase；`ContentItem::OutputText`
  只有 text；`WebSearchAction::Search` 只有 query/queries；`core/src/client.rs` 默认 include 只有
  reasoning.encrypted_content。因此结构化 annotations 和搜索 sources 目前无完整展示链路。
- Host 原生 AgentMessage 投影保留 text/phase，Desktop 复用原生流及只读布局分类；
  `ChatSafeContent` 保留模型 Markdown 链接的标签与完整地址，但按已有安全边界渲染为 inert 文本，
  不自动打开外网，也不把任意链接说成已核验引用。
- Host 给普通会话显式 baseInstructions，覆盖模型目录默认提示；上一轮只用一句概括性进度要求，
  缺少具体引用约束。提示指引不足是可改进因素，不等同于模型必须遵从或唯一根因。

官方资料（2026-10-23 核对）：
[Kimi Responses API](https://platform.kimi.com/docs/api/responses) 说明 web_search 由服务端执行，
搜索后将结果注入上下文，web_search_call 放在 output 前部；显式 include
web_search_call.action.sources 才额外返回搜索命中的来源。
[Kimi 的 Codex 接入说明](https://platform.kimi.com/docs/guide/codex-kimi) 确认原生 Responses 直连及
内置 web_search，不需要另造协议转换层。Chat Completions 的旧 $web_search 退役说明不是这条
Responses 链路的退役证据，不能混淆。

## 实施和真实验收约束

优先方案是复用现有原生助手消息、网页搜索和 Markdown 文本链路，要求模型给出真实公共进度，
并在事实旁使用实际搜索/阅读得到的具体来源 URL；缺证据时说明未核实，不猜 URL。
不新增第二个推理循环、代理搜索器或由前端拆句生成“进度”。

复用 `chat-model-smoke-meter.py` 与固定 loopback 验证入口，新增 Kimi-only、任务专属 ledger。
上限 8 个 Provider HTTP 请求、每次最多 8192 output tokens、0 图片请求；只执行本题正常验收，
不是复用旧 FEAT-156 付费额度。计数器仍只转发固定 api.moonshot.cn 的 /v1/responses，
无直连兜底和自动重试；响应原字节转发。只记录闭集类型、phase、长度、引用/来源计数和哈希，
不记录请求正文、响应正文、原始思考或密钥。开发计数器对输出 token 作原有上限约束，
因此不称为请求全字节透明。结束后正常关闭并恢复 canonical 直连运行。

Must 检查：真实配置、Provider→Runtime 消息/链接计数对应、实际 UI 分类与来源可读、旧安全边界、
正常退出重开、实际答案引用的可追溯程度。模型不生成的内容不得通过 fixture、seed 或 UI 注入补齐。

证据目录：`CrossBSD/.local/audits/kimi-progress-citations-20261023/`。起始基线已记录所有相关仓库
HEAD/branch/remote/status 与文件哈希；本轮不 commit/push，不修改既有无关脏文件。

## 本轮真实诊断结果

2026-10-23 00:31:06（Asia/Shanghai）从正常 App 新建任务发送同一原题。Desktop session
`01a16473-b1b2-71e0-84f7-5269e9046dd7`，Runtime thread
`01a16473-b1dc-79e0-8411-5ec1bbc822ab`，turn
`01a16473-b23a-71c1-b32d-024315fc53f1`。真实配置为 kimi-k3/max、summary auto、
approval never、danger-full-access。26.062 秒完成，1 个真实 Provider HTTP 请求，0 命令。

Provider 边界被动统计（响应字节原样转发）：

- HTTP 200；新指令 SHA-256 与 Provider 请求 instructions 一致，确认不是仍在使用旧指令。
- 3 个 output Item：web_search_call、空 reasoning summary、assistant message。
- assistant 只有 1 条，phase 为 null；2450 UTF-8 字节；正文 URL 0、annotations 0、url_citation 0。
- web_search_call 的 sources 0；请求 include 仅 reasoning.encrypted_content。
- 587 次 output_text delta；没有独立 commentary Item。
- Runtime 最终 assistant 的 ID 指纹、文本长度与 SHA-256 与 Provider 完全一致。
- 实际 UI 是“已搜索网页”及最终五维答案，没有隐藏一个已存在的公共进度消息或来源 URL。

因此本轮主因可以定位到 Provider 输出，而非 Host/前端漏显；Runtime 缺少结构化来源与注解通道
则是独立的能力缺口。本轮没有 annotations，不能把这次的 0 引用归因为 annotations 被丢弃。
强化指令没有让本轮 Kimi 输出进度和引用，必须保留这一 FAIL 结论，不能把最终回答完成当成修复通过。

计数器已在请求结束后通过正常 Ctrl+C 退出（exit 0）；App 正常退出后使用 canonical 命令恢复
不带验证地址的直连构建。无强杀、无攻击 fixture、无权限破坏、无 Runtime/二进制篡改。

## 独立进度的可复用机制与方案

截图中的中文段落是公开 assistant 进度，不是原始内部推理。工具活动摘要是另一类执行事实；
底部短状态仅凭外观不能当作独立 assistant 消息。

| 原生能力 | 已有链路 | 适用边界 |
| --- | --- | --- |
| assistant commentary | ResponseItem::Message.phase → core AgentMessageItem → ThreadItem::AgentMessage → item/agentMessage/delta、item/completed → Host NativeEvent → Desktop NativeDisplayBuffer/ChatTurnGroup | 最接近 Codex 的目标形式；只显示 Provider 真正产生的公共文字，phase 缺省不强行改成 commentary |
| 模型计划说明 | 原生 update_plan → EventMsg::PlanUpdate → turn/plan/updated.explanation/plan → Host → NativeDisplayBuffer → ChatTurnPlan | 文字确由模型给出，可以用于真正的多步骤任务；不能为刷进度强制制造无意义计划。当前 buffer 只保存最新 plan/explanation，不具备历史说明流水 |
| 执行状态说明 | 既有 turn/item started/completed、approval/error、live observation | 可显示“执行进度：已开始处理／网页搜索已完成”等客观说明，必须明确系统来源；不能写成“我发现了…”或声称完成了尚无证据的核验 |

推荐双来源展示：真实 commentary 按原顺序与工具活动穿插；模型沉默时使用标为“执行进度”的
真实事件说明，解决无反馈等待。两种来源不混成模型发言。已有真实计划 explanation 可保留为
“计划进度”而不改成 assistant。相同事件去重，不靠计时器循环生成话术，不补写冷历史。

不采用：把 reasoning summary 改名为进度；从最终答案拆句冒充中途消息；新增旁路模型请求
自动编进度；执行 echo/true 制造活动；复制 planner/reducer/重建业务状态；改用另一模型假扮 Kimi。

若需要将计划更新和系统进度永久穿插进历史，必须扩展现有 NativeDisplayBuffer 的版本化显示记录，
保存真实事件身份、来源和顺序，沿契约权威先行；不能仅在 Vue 拼出永久 assistant Item。
该扩展对闭合消费端应按 breaking 分类，版本化兼容旧 reader；本轮尚未实施该跨仓扩展。

若产品只接受模型亲自生成的进度文字，应用层不能保证每轮都有：本次原始输出已给出反例。
可以继续利用真正的原生计划说明和模型能力，但不能用系统生成的话术假装解决了该限制。

## 引用的后续实施边界

沿现有 yijie-codex Responses 请求、WebSearchAction、app-server schema 和 Host/Native 投影
补齐 include 与 sources，是正确复用方向；不新造搜索代理或另一个执行引擎。Runtime 变化应以
独立、可重放补丁及新候选构建开始，保留固定旧产物；canonical schema 先于 Contracts 投影，
再由 Host/Desktop 消费。闭合字段需要版本化，不能手改生成物。

搜索命中来源只能标为“搜索来源”，不能自动作为每个答案结论的引用。模型真的输出具体引用时，
保留其原文和关联；没有给出时如实说明。本轮没有任何可展示的 URL，不能根据城市名、查询词、
官网域名或旧会话补造链接。现有 inert URL 安全边界继续保留，点击能力应另走现有安全设计。

## 验证与交付范围

- 被动观察器 3 项普通单测 PASS；脚本 py_compile PASS，未保存正文或凭据。
- Host 权限/专家组合/推理配置/固定验证入口定向测试与 go vet PASS。
- 3 项 Host 原生消息/历史/终态映射测试 PASS。
- 前端正常 Markdown 来源地址保留测试 1 项 PASS，其余未选择的用例未当作通过。
- canonical source candidate 检查、App 标准构建、真实 UI 诊断回合及正常关闭 PASS。
- 真实产品目标“独立进度＋充分引用”仍 FAIL；无新 Runtime、Contracts、前端展示修改。
  当前代码改动限于普通助手指令、既有开发计数器和脱敏观察器，以及构建候选/本审计记录。
- 不运行强杀、权限故障、攻击注入或历史未筛选整套验收；不声称全项目全套测试通过。

关键证据：`ledger.json`、`provider-runtime-comparison.json`、`preflight.png`、
`probe-final.ax.txt`、`probe-expanded.png`、构建与测试日志。
