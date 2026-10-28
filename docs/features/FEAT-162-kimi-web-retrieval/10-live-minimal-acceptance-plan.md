# FEAT-162 真实 Search / Fetch 最小验收方案（已确认，本次执行已停止）

制定日期：2026-10-24，Asia/Shanghai。原提案状态为PROPOSED；用户随后明确确认。唯一一次启动在Go工具链校验阶段失败，当前为STOPPED_BEFORE_TEST_ENTRY，详见11报告。本次授权已关闭，不自动重试。

以下保留提案时记录：当前用户仅要求方案；本轮只读取本地实现和公开官方网页，未读取密钥值、未启动App/worker、未调用任何Kimi账户接口。此文档不修改feature.yaml中的paid_calls:false。

## 范围与执行方式

验收当前Kimi凭据是否能访问两个REST接口，以及现有Connectors适配器能否返回约定的搜索列表和正文。沿用客户端已有模型凭据加载及Host→worker启动快照，不另填、复制保存或输出API Key。

采用无模型的定向连接器验收，复用当前canonical产品worker、Broker/Gateway及正常批准校验；不发送聊天/Responses请求，不触发原生搜索、Search Pro、/models或余额查询。需要的定向测试驱动在用户确认后准备并先检查调用预算；它只发固定测试请求，不重建Agent循环、不改Codex内核、不绕过现有审批。现有qualification-only替代worker不能作为真实供应商执行入口。若无法在上述边界内驱动产品worker，停止并报告，不擅自改为模型对话验收或直接curl读取密钥。

本方案只证明工具边界真实可用，不声称模型会正确选择工具、App完整审批对话/结果历史或整体D4通过。

## 固定操作和预算

| 顺序 | 操作 | 固定输入 | Kimi供应商HTTP额度 |
|---|---|---|---|
| 1 | 正常拒绝门禁 | 提交Fetch提案并拒绝，确认未进入HTTP发送 | 0 |
| 2 | 批准一次Search Basic | query=`IANA example domains`，limit=3；现有adapter固定include_content=false、timeout_seconds=10 | 最多1 |
| 3 | 批准一次Fetch | url=`https://www.iana.org/help/example-domains` | 最多1 |

总计3次本地工具提案，其中1次拒绝、2次批准；真实供应商请求最多2次（Search1、Fetch1）。模型推理、/models、余额接口、Search Pro及其他收费工具全部0次。仅使用公开资料，不提交私人文件、商家数据或登录态网页。Fetch不自动追随Search结果，目标URL预先固定，两个用例可分别判定。

## 当前价格与预计费用

2026-10-24核对[Kimi官方联网搜索定价](https://platform.kimi.com/docs/pricing/websearch)：Search Basic为人民币0.01元/次，Fetch为0.01元/次。官方规则为HTTP200且Search结果非空/Fetch正文非空白时收费；失败或无结果/正文不计费。不能仅因本地超时或取消推断供应商未完成计费。

两项都成功预计总计**¥0.02（2分钱）**，没有模型token费用。拟申请本轮费用预算¥0.02、真实HTTP次数上限2；不申请任何重试额度。执行前重新核对公开单价，涨价或计费规则变化超过预算即停止重新确认。实际金额以供应商账单为准；不把公开单价计算当作已核对账号账单，不通过额外账户API验证扣款。

接口来源：[Search Basic](https://platform.kimi.com/docs/api/tools-search)、[Fetch](https://platform.kimi.com/docs/api/tools-fetch)。正文对照采用[IANA公开原文](https://www.iana.org/help/example-domains)，应包含示例域名的文档用途及不可注册/转让等内容，不规定搜索结果排名。

## 通过标准

1. 拒绝提案不产生Kimi HTTP发送；没有获取任何可重用批准或关闭审批。
2. Search恰好一次POST；HTTP200；规范化结果为1–3项，所有项具备title/url/snippet字段，至少一项标题和摘要非空、HTTP(S) URL有效且与IANA示例域名相关；truncated字段为布尔值，不把空列表当作本次业务成功。
3. Fetch恰好一次POST到固定Fetch接口；返回目标URL、非空标题和非空Markdown。正文与公开IANA页面关键事实一致（示例域名用于文档说明，不可注册/转让），不是错误页/登录页；短页面应truncated=false，不伪造正文。
4. 结果经过当前canonical输入/输出校验和MCP封装，text及structuredContent语义一致、整体在65536字节预算内；调用仍受已有scope、单次批准和超时约束。
5. 记录操作ID、HTTP发送次数、固定诊断阶段、HTTP状态/安全错误、耗时和结果字段检查；不记录Key或Authorization头。保留公开结果的最小必要证据，正常EOF/退出清理。

## 停止条件

- 任一步401/403、限流、超时、不可提取正文、响应格式错误或结果不确定：记下该项失败/阻塞并停止本轮，不重试、不换Key、不充值、不改目标或提高额度。已发送请求计入次数预算，按可能计费保守记账。
- 请求即使已发送但结果未知，也不自动补发。重复工具提案不额外批准；若发现预算计数或批准门禁不能可靠约束发送，先停，不执行付费请求。
- 无模型来源则在本地停止，不弹出连接器密钥表单。
- 禁止所有强杀、权限破坏、二进制替换/伪装和攻击性fixture；不做异常注入测试。

## 待确认范围

用户确认需覆盖：继续复用现有Kimi模型Key；正常拒绝提案1次（供应商0请求）；真实Search Basic最多1次和Fetch最多1次；预计/批准预算¥0.02；模型调用0次；失败停止、重试需另行确认。确认只授权本方案，不包含后续模型驱动端到端验收或完整D4。
