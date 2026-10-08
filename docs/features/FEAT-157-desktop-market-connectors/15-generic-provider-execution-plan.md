# 通用 MCP Provider 执行方案

2026-10-08 Owner已明确“根据推荐的通用发现+逐次审批方案做实现执行；遇到阻塞深入解决”。推荐方案1已确认，继续实施，无待定批准。

本方案承接[14代码审计](14-completion-audit-2026-10-08.md)，不是扩大真实验证。**开发中仅Tushare允许真实授权/调用；其余50项采用代码审计和本地协议测试。** 用户以后在产品中主动配置某个服务时，才由该服务自己的正常连接流程发现工具。

## 问题与推荐

当前 Provider/Broker/Gateway 把 Tushare 的服务 ID、daily 名称、单项选集和完整 schema 摘要写成唯一产品执行策略。即使补齐43个OAuth流程，其他服务仍不能调用。为每个服务的每个工具预先写专属归一化适配，会把通用MCP市场变成大量独立工具开发，且依赖逐项取得实时schema。

推荐复用现有Codex客户端和Broker，只把Tushare daily保留为专用策略，增加通用MCP策略。通用工具在用户连接时发现并冻结完整定义；已选择的服务之外始终不可见。每次实际调用都核对冻结定义、参数、当前连接版本、Native scope/实际thread/turn，然后请求一次明确批准；任何未知执行结果都不自动重试。

## Owner 已确认的工具准入语义

现有 Connectors AGENTS.md 要求「工具按只读、低风险写、高风险写和不可逆操作分级，未知工具默认高风险并拒绝」；Provider 源契约还明确只有固定 daily schema 可以执行。这不能靠删除 service ID 判断静默改变。

两种可落地路径：

1. **推荐：通用发现＋保守风险＋逐次批准。** 已确认属于所选固定服务、已通过正常MCP发现/完整schema校验的工具，若没有独立只读策略，则按高风险请求人工单次批准。界面必须明确“尚未确认只读，可能修改外部数据”，展示真实服务、工具和完整参数；参数不能完整展示或身份/定义不完整则拒绝。未经用户实际批准不可执行。无法确认影响范围的不可逆操作仍拒绝，不能拿一次模糊“同意连接”当未来调用许可。
2. **保留逐工具白名单。** 每个可调用工具都必须先有独立风险策略与固定schema来源；尚未登记的工具继续拒绝。这可以继续实施，但不能宣称仅一个Tushare工具已覆盖51项服务的使用需求。

这项选择涉及现有工具准入规则，平台token仍留Connectors/Keyring，Host/Runtime、请求批准模式、账户权限边界及调用预算都不变。方案1也不允许Agent替Owner点击未知服务的真实批准。

## 实施结构

- **服务定义**：Connectors唯一服务注册表，记录固定service ID、transport、资源地址、认证策略、官方来源、配置字段和适配差异；Native仅消费非秘密能力投影，不再散落Tushare判断。参考宿主专属URL标记不能充当易界应用身份。
- **OAuth**：复用固定Codex/rmcp授权状态机、PKCE、callback、Keyring和refresh；将资源/issuer/metadata端点校验与回调生命周期从Tushare策略分离。仅接受固定目录服务的可信发现链，token不跟随任意重定向。过期/取消/迟到回调不保存或恢复能力。
- **自备凭据**：worker直接拥有安全输入和Keyring入口，Native/UI/Host只拿opaque引用。FTShare按官方`FTSHARE_API_KEY`header；其他协议按各自官方配置，不猜Bearer。秘密不进入工具参数/schema/config或历史。
- **本地服务**：Google包固定来源/版本，复用已验证公开字节流桥接和EOF owner；不使用上游强杀launcher。Calendar的文件token持久方式必须改为受支持的安全存储适配，不能把明文文件藏进私有目录充当Keyring。
- **多服务能力**：Broker的一条选集租约持有多条精确ProviderBinding；工具名与service映射无歧义，工具目录/参数schema/风险策略冻结到当前能力。容量不足明确拒绝，不能静默裁剪或开放全部已安装服务。
- **执行**：通用backend复用现有RmcpClient，保留单次HTTP许可及不可自动重发语义；Tushare daily保留既有参数/行情结果归一化。第三方业务差异留Connectors，不进入Host或Codex fork。
- **结果**：官方MCP文本/结构化结果走既有有界投影；无HTML执行。凭据字段及所属凭据值不外传，无法安全呈现时显示对应不可用说明；结果未知不等于未发送/无数据。
- **撤权与恢复**：复用installation/revision/generation、私管道grant和Normal EOF；停用先关新准入，再正常清理；重开只恢复安装意图，重新连接后才可执行。历史只读不复活授权。

## Contract First 与验证

先更新Provider/Broker的源语义、通用工具描述和能力清单，再生成Host/Native消费者，最后替换worker与UI硬编码。新策略用独立profile/版本，旧Tushare回执、固定Runtime与现有正常聊天不改变；候选仅local，不发布。

本地测试按共享机制覆盖：OAuth成功/正常取消、Keyring端口失败、metadata分页与schema变更、多服务名称映射、逐次批准与拒绝、单次许可、结果未知、正常EOF、重开只读。合成MCP服务只用正常协议和进程内实现，不使用攻击/权限破坏/替换二进制/强杀fixture。51条配置逐条做静态对应检查；不运行51次真实接入。Tushare既有真实成功/拒绝作为代表，只有实现变化使旧证据不再适用时才在剩余额度内补必要验证。

当前范围更新：Owner后续移除淘宝闪购及豆蔻医生；Agentic Engine恢复接入，目录49项。本文51项为原计划，当前实现、官方适配与证据以17为准。
