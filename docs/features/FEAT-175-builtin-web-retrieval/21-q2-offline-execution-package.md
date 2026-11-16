# FEAT-175 Q2离线执行包与真实执行交接

本页记录离线准备与交接。专属接线见[23](23-q2-meter-and-native-execution.md)，随后获准的首轮真实Q2已停批，结果见[24](24-q2-first-live-result.md)。下文零授权表是准备阶段快照，不能覆盖真实账本。 操作说明见[Host准备包](../../../../yijie-agent-host/docs/feat175-q2-preparation.md)。

## 冻结任务

权威输入为[cases.json](../../../../yijie-agent-host/internal/codex/testdata/feat175-q2/cases.json)，Kimi K3.1 Pro max与MiniMax M3 high各执行六类一次，总计12；不是12个HTTP，也不替代Q3的96任务。

| ID | 自然任务 | 首次预期 |
| --- | --- | --- |
| Q2-01 | 12件×8箱的普通计算 | 无外部检索 |
| Q2-02 | Python当前稳定版、日期及官方来源 | 原生hosted |
| Q2-03 | Shopify两种API限流研究，限定官方站点与日期 | Pro，保留sites和time_window |
| Q2-04 | 5个文档标题／链接，不读正文 | Basic，limit=5，include_content=false或省略 |
| Q2-05 | 3篇WebP资料正文采集 | Basic，limit=3，include_content=true |
| Q2-06 | 明确读取指定RFC网址 | Fetch，URL符合原请求 |

提示不点名工具。当前普通聊天有效base/developer指令和模型目录由[静态快照](../../../../yijie-agent-host/internal/codex/testdata/feat175-q2/effective-profile.json)记录；其值由实际Host装配函数产生，不是手写模型配置，也不是已收到的供应商wire。正式执行仍需记录实际请求、工具表和usage。

## 离线检查

在yijie-agent-host运行`bash scripts/check-builtin-web-q2.sh`。它核对同源SDK、重新计算静态profile、核对来源摘要并运行离线评分测试；不启动Runtime或外部服务；费用单元测试使用普通loopback HTTP。

评分入口为`node scripts/feat175-q2.mjs score EVIDENCE.json`，输入结构示例见[明确合成的首次错误样本](../../../../yijie-agent-host/internal/codex/testdata/feat175-q2/example-synthetic-first-error.json)。它展示“Basic后补Pro”仍为首次失败，另11个未执行任务仍记MISSING，不输出伪造的Q2通过。

来源锁固定Runtime制品、canonical ThreadItem schema、当前Host配置／指令实现和评分器。改变模型、工具表、指令或相关代码必须重新审阅适用性；真实运行开始后不覆盖旧版本、旧输入和失败证据。

## 记录与评分要求

只根据原生item/started顺序识别首次动作，completed只更新同一Item。不能从最终回答或Code Mode文本推测调用；正常tool_search发现不算外部检索。MCP server／tool身份不能在同一Item中改变。

每个任务绑定原始提交提示SHA及thread/turn；合法子任务按原生thread/read父子关系和turn/started归入该任务，检索和费用都不能遗漏。未归属、缺开始顺序、缺结束或hosted可见性不完整时不判通过。

每模型分母固定6任务；独立检索类额外hosted分母为4。query相关性需要人工审阅；参数、路由、执行状态、证据质量及后续恢复分别记录。评分器只提供审阅材料，不自动提升Q2或生产门禁。

合成MCP结果可能导致模型继续补充证据。须区分预期MCP之前的hosted和收到合成材料后的调用，不能把后者直接外推成产品重复率；事件顺序本身也不能证明供应商自动预检索的原因。Q2不应用Q3的95%／5%稳定性结论。

## 真实执行交接

[未授权预算表](../../../../yijie-agent-host/internal/codex/testdata/feat175-q2/authorization-not-granted.json)已绑定冻结包摘要。拟用上限为12任务、48个模型HTTP、每模型24／每任务4，本地MCP每任务4；真实Basic／Pro／Fetch REST为0。hosted观察停止阈值24不是供应商单HTTP内部的计费硬上限。

实际允许的模型HTTP、hosted、REST及金额仍全部为0；没有替用户填写正数金额或沿用旧任务余量。真实执行需要当前资费／金额约束、精确模型及凭据来源资格、FEAT-175专属meter模式及正常EOF验证。复用现有两模型计量和原生token／rollout／Goal能力，不新增推理调度／Token累计器。

离线评分工具仍没有live mode；后续专属计量与原生执行入口已完成本机资格，当前缺明确费用授权和真实供应商协议证据，详见23。真实授权后才可开始Q2；默认描述共存若出现结构性冲突，应停止相关验证并保留首次失败，不能通过加工具名提示或删失败样本制造通过。
