# FEAT-175 Q2 专属计量与原生执行接线

本页保留授权前的零费用批次记录。后续已获一次性明确批准并执行真实Q2，停发结果及已消费授权见[24](24-q2-first-live-result.md)。

2026-11-15。用户要求认真审阅后继续下一步。本批完成独立 Q2 验证入口及零费用资格验证；**真实 Q2 仍为 NOT RUN，付费授权仍为 0**。不把“开始执行下一步”解释成撤销先前的零费用约束。

本批 `contract-impact=none`：仅新增不可发布的本机 QA 驱动、费用观察、测试和文档，不改变公共 wire、SDK、产品入口、模型指令或 Runtime。FEAT-175 整体仍按 breaking 治理。S1/Q1 历史证据保留，S2—S5 与公开分发未完成。

## 实现与原生复用

入口是 [feat175_q2_run.py](../../../../yijie-agent-host/scripts/feat175_q2_run.py)，实际模型执行仍由固定 Runtime、现有 Host `Manager`、`StartThread`、`StartTurnV2` 和 `InterruptTurn` 完成。Kimi 继续使用原生 `tool_search → exec → MCP`；MiniMax 保持原生直接函数组织。使用同一份自然语言提示、技术 profile、工具定义及当前指令，不添加工具名提示、不强制 `tool_choice`、不自行做模型选路或重试。

[计量器](../../../../yijie-agent-host/scripts/feat175_q2_meter.py)复用已有 `feat164-budget-meter.py` 的有界 Responses 观察器、凭据读取与脱敏错误分类；复用 Host 的 `kimiK31MeterArguments` 将两家模型的请求／流重试关闭并统一指向本机计量入口。没有复用任何历史任务的授权、账本或固定额度。

旧验收适配器存在删除 `web_search`、重写 `max_output_tokens` 的路径，不能用于此次自然选路资格。新入口逐字转发模型请求体、保留声明及输出上限；只在计量端置换本机 bearer 为供应商 Key。Runtime、Go 驱动与证据配置只收到随机本机能力凭证，不收到供应商 Key。供应商目标封闭为两家中国站 `/v1/responses`，没有 Basic／Pro／Fetch REST 客户端。

六类任务×两个模型，每任务新建 thread，保留原生事件。MCP 使用同源 schema 的明确合成本机材料：Basic 区分标题列表与正文，Pro 返回非空 chunks 并映射请求的站点／日期，Fetch 保留请求 URL；这些 URL 不会被访问。内容来源质量和最终产品重复检索率不能据此验收。

## 准入、费用和停止

| 控制 | 当前执行状态 | 拟议真实 Q2 范围，尚未批准 |
| --- | --- | --- |
| 模型任务 | 仅本机合成 | 12；两模型各 6 |
| 模型 HTTP | 真实 0 | 整批 48、每模型 24、每任务 4；子任务和辅助请求也占用 |
| 本机 MCP | 合成服务 | 每任务 4；不调用供应商 REST |
| hosted 搜索 | 真实 0 | 观察到 24 次后停发；非供应商内部硬上限 |
| 金额 | 0 元 | 建议 20 元软停发阈值；在途响应可能使总额超过阈值 |
| 有效期／重跑 | 无有效付费授权 | 授权最多 24 小时；唯一 authorization_id 只能消耗一次，不自动续跑或重置额度 |

官方公开价格已形成[快照](../../../../yijie-agent-host/internal/codex/testdata/feat175-q2/pricing-snapshot.json)。Kimi 的输入、输出、缓存写入和 hosted 费用，MiniMax 的不同上下文档位及 hosted 费用分别核对。来源为 [Kimi 模型价格](https://platform.kimi.com/docs/pricing/chat)、[Kimi 搜索价格](https://platform.kimi.com/docs/pricing/websearch)、[MiniMax 定价](https://platform.minimax.cn/docs/pricing/overview)。部分 Kimi 表格位于官方 HTML 的嵌入 MDX 中，快照保存来源摘要与提取方式。

费用按实际 terminal usage 作保守上估：Kimi 输入按基础输入＋完整 5 分钟写入计，MiniMax 按较高的标准上下文档位计，均不扣除缓存折扣。1h TTL、priority／未知模型与未定价的 hosted 工具拒绝。该值不是供应商账单，也不是请求发送前已证明的硬金额预占；必须显式接受 `soft_stop_after_observation` 与在途超额，才能启动真实模式。若只批准硬上限，此入口保持关闭，需另做不改变 Q2 请求的硬约束资格。

启动前校验专属授权、包／来源／价格摘要、额度、有效期和新账本；未授权时在读取 Key、监听、启动 Runtime 前拒绝。每个任务重新检查冻结来源及 Runtime 摘要。每次模型发送前预记请求占用；未知结果不退还次数或按零费用处理。完整终态、EOF、模型身份或 hosted 清单缺失即停止继续发送，保留 `outcome_unknown`。

计量器逐任务与原生事件核对 hosted item ID；遗漏、重复或无法对应时立即停批，不等 12 个任务结束才判不完整。子任务归属复用 Host 的原生 ancestry 解析，再用 `thread/read` 确认；未结束子轮次不得流入下一样本。第一次检索选错仍保留，不以补救覆盖。

停止通过计量器停发 → 驱动轮询 → 原生 `turn/interrupt` → `Manager.Shutdown`／正常关闭进行。客户端断开后，已发出的供应商流继续有界读取以收取 usage，不自动重发。无法正常退出记录 STOP_PENDING 并保留现场，禁止强杀。停止新准入不等于撤销供应商已开始的计费。

## 本批验收与复审

机器记录见[本批检查](references/q2-wiring-checks.json)与[工作区保留核验](references/q2-wiring-preservation.json)。

- 13 项 Python 费用／授权／计数／观察与普通 loopback 检查通过；当前零授权会在不存在的凭据路径被读取之前拒绝，未创建运行目录。
- 原有 10 项评分测试、1 项同源 MCP 输入／输出 schema 检查通过；纯 Go profile 与 hosted 对账 2 个顶层检查、5 个子项通过。
- 固定真实 Runtime 完成 12 个本机合成任务、24 个本机模型 HTTP、8 个本机 MCP 调用，原生事件与计量记录对应；不是模型自然选路成绩。
- 独立正常停止场景：首个本机请求收到停发后，原生 turn 变为 interrupted，无后续准入，Runtime 和计量服务正常结束。该场景预期驱动非零退出，单独验收停止链，不伪装成 12 任务成功。

复审修正了四处问题：初始证据目录内的 CWD 会继承 Host 仓库 AGENTS.md，现改为独立临时 CWD；provider 与 Runtime 的 hosted 对账从批后移到逐任务；冻结来源从仅启动检查补为每任务检查；授权消耗按固定 grant ID 保存，修改账本路径／附加字段不能重置同一授权。首轮诊断证据保留，最终来源锁及正常停止场景另行重验。

自然提示包 SHA 保持 `0fbed97c6b772b1d9e9767acee654fcafa721e2452a8ce9592e58b50b6e35ae7`。来源锁从 34 增至 43 项，只增加验证接线／相关 fixture／公开价格依赖；[原 34 项来源锁](references/q2-source-lock-before-wiring.json)保留。当前 cases 文件里的“尚无 live mode”是上一批冻结阶段说明，实际工具入口状态以本记录及专属授权门禁为准；它不是执行授权，不改写已经冻结的提示来迁就结果。

未执行：真实模型／hosted／Basic／Pro／Fetch 调用、真实供应商访问资格、自然选路和重复率评测、S2—S5、日常 App 激活、部署／迁移、提交／推送。真实 Q2 的首批实际请求仍须核对供应商协议／usage，失败即保留并停发，不以官方文档或合成协议冒充实际资格。当前旧 connector selection 指令歧义仍保留在冻结 profile，需由授权后的 Q2 发现真实影响。

下一步只需审批具体真实 Q2 范围；批准后建立本任务专属一次性授权，使用已有合规凭据来源运行。Q2 结论经原始事件、首次动作、参数、人工 query 相关性及账单记录审阅后，再决定是否修正描述／最小配置或进入 B01/S2；不得直接宣称 FEAT-175 已交付。
