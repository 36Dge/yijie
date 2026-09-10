# FEAT-144 最小业务取样备用方案（业务预算已授权，未执行）

2026-09-10。连接已经通过固定Runtime原生元数据验证。本文件是可审查的备用提案，**当前不申请、不执行，不作为D0必经步骤**。13已明确通用原生文本投影；一次成功取样不用于验证已被用户排除的业务失败场景，也不能证明收费规则。仅在出现必须由真实返回确定的具体设计问题时，先说明本次调用能回答什么，使用15中已授权的10次业务额度；后续产品D4使用真实模型Turn及原生审批，不能用此手工RPC替代。

## 明确目标与参数

使用固定Codex0.144.6稳定原生 `mcpServer/tool/call`，仅：

```json
{"server":"sorftime","tool":"product_detail","arguments":{"asin":"B07H9PZDQW","amz_site":"US"}}
```

threadId由本次空ephemeral原生线程提供，不手工构造可信绑定。ASIN是官方包示例和[Amazon US公开商品页](https://www.amazon.com/dp/B07H9PZDQW)中的Gaiam瑜伽垫，只证明有公开出处，未证明Sorftime当前有数据。不换ASIN，不批量、不调用其它工具或get_time，不发送项目文件/历史/账户资料；保留原生必要协议元数据。

## 调用与权限边界

此稳定RPC经 `mcp_processor.rs:455` → `CodexThread::call_mcp_tool` → 原生MCP manager，执行原生enabled_tools/disabled_tools检查。它**不经过模型工具调用前的Prompt审批，也不产生McpToolCall Item**；不能因为配置approval_mode=prompt就声称经过审批。只能在用户明确授权上述具体手工操作之后执行，用于D0结果取样，不能接入产品调用链或替代FEAT-152/Item/D4。

若不接受这个原生手工取样边界，则不运行此方案；改用官方脱敏返回样例，或等后续产品实施/模型预算授权后走真实模型Turn与原生审批。不另写MCP客户端，不自行补审批或伪造Item。

## 分账预算与停止条件

- **本备用操作消耗15授权预算中的最多2次tools/call尝试（1次逻辑product_detail及可能的原生session404重发）；不另增额度，外层不重试。** 不是1次HTTP上限，不声称免费或只扣费一次。
- **模型0、图片0。** 不创建模型Turn，不调用Responses。
- 新连接必要的1次原生初始化记入已有剩余2次元数据额度；初始化内部正常握手/发现/重试/清理按既定口径计算。不额外单独请求status列举来重复核验连通性。
- 失败、空返回或格式不支持都不自动追加请求，不换参数；请求额外输入、认证、URL访问或权限扩大时拒绝并正常清理，不再启动新业务调用；此前已发出的尝试照实计账，不能承诺拒绝后零调用或不扣费。
- 正常unsubscribe/EOF退出；无法正常退出则报告，不强杀。无queryURL，Bearer环境引用和真实0.144.6 User-Agent继续使用；密钥仅隐藏输入和本次受管进程内存，不写命令参数或文件。

## 可交付证据与不能证明的内容

保留原生isError的true/false/缺失区别、content类别/索引/长度、structuredContent是否存在、空/缺失区别及安全展示所需的最小文本样本；不默认将整份原始返回写入需求仓、日志或用户数据库。未知错误只记录安全类别，不据正文关键词制造failed。

这个手工RPC没有原生Tool Item，因此只能报告“RPC返回/原生isError”，不制造completed/failed Item或时间戳，不借此通过AC-002/004/006/007。若返回正常数据，可完善纯文本展示和后续D4样例；空数据仍为单独事实。一次取样不能证明账户扣费规则、幂等保证或稳定的正常失败条件。

当前状态：业务额度由[15](15-owner-scope-and-business-budget-2026-09-10.md)明确授权，**本方案NOT RUN**。已有8/10元数据与业务0/10独立；不是产品编码、migration、模型、提交、推送或Runtime变更授权。
