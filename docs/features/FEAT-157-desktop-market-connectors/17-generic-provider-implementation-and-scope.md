> **2026-10-08 13:20 本地 D4 已验收**：Owner明确回复“接受分阶段证据，完成本地 D4（推荐）”。当前49项（淘宝闪购、豆蔻医生已移除），AC-001–010均已通过；采用Tushare原f8构建真实批准/拒绝与最新ea84构建本地回归，保留各自证据，不合称同构建实跑。D4验收未新增模型或服务调用；后续获准的Git交付见[19](19-git-delivery-2026-10-08.md)，未发布。最终记录见[18收尾矩阵](18-closeout-audit-and-acceptance-matrix.md)及[验收证据](evidence/closeout-verification-2026-10-08.json)。以下早期状态均为历史。

# 通用 Provider 实现与当前范围

2026-10-08。此记录接替16的中间状态；14是实施前审计，不再是当前缺口清单。Owner先移除淘宝闪购，再移除豆蔻医生，并提供Agentic Engine官方资料恢复其接入范围。此前暂缓2项的中间决定已被最新指示取代。

## 范围与架构

活动目录revision 5共49项，六分类数量为2/5/2/14/17/9。原始51项参考材料保留；产品目录、worker注册表、Native和前端投影已移除两项，旧历史不销毁，旧选择不能取得新能力。

当前代码路径为43项标准OAuth发现、1项Tushare专用OAuth/daily、1项Google预注册OAuth、2项固定Header（FTShare/Google Maps）、1项执中固定api_key查询参数、1项AE显式导出Header。代码覆盖不等于49家服务端实连或账号权限已经确认。

Google参考本地包不是易界运行依赖。采用官方[Maps Grounding Lite](https://developers.google.com/maps/ai/grounding-lite)和[Calendar MCP](https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server)，复用Codex HTTP/Keyring。Calendar需要开发者预览资格、自有Web OAuth客户端、API启用和固定本机redirect；默认只读，用户显式勾选才请求事件修改scope，delete_event仍拒绝。配置保存后在同一安全页继续Google授权，不把保存配置当成授权成功。

## Agentic Engine官方资料核对

已读取Owner提供的[MCP使用说明](https://docs.thinkingai.cn/zh/manual/mcp)、[认证与配置手册](https://docs.thinkingai.cn/zh/manual/mcp_integration)、[对外服务介绍](https://www.thinkingai.cn/product/mcp-service/)。前两份主要讲AE作为宿主如何管理MCP及导出到客户端；对外介绍给出stdio API_TOKEN示例，不能据此推断HTTP Bearer。

易界保留参考资料中的固定HTTPS服务地址，在Connectors自有安全页提示用户从AE导出的远程HTTP配置复制认证Header名称和完整值，默认原值，附官方文档入口。秘密直入Codex Keyring，不经Native/Host/模型；保存后仍需完整工具发现和逐次审批。公开页未独立确认该端点的Header字段，故不硬编码mcp-token或API_TOKEN映射。不同端点、多Header、托管stdio配置不自动转换；这属于供应商配置适用条件，未用真实账号验证，也未运行npx示例。

## 通用执行与凭据

Contracts Broker 0.3.0 / Provider 0.2.0 source-first生成。每次调用显示完整业务参数和schema摘要，租约持有精确多服务binding，service与上游名称共同隔离。完整schema使用固定JSON Schema库本地编译，拒绝外部resolver；目录容量、深度和结果有界。未知风险按write逐次审批，明确destructive缺影响策略则拒绝。Broker单次消费和HTTP单次发送许可共同约束，不自动重试业务请求。Tushare专用daily名称、入参和行情归一化保留。

OAuth仅沿所选HTTPS资源的受限发现链获取固定issuer，支持同源metadata路径和多个候选issuer；凭据不跟随重定向。配置页采用worker拥有的一次性nonce、Host/Origin、期限和正常取消。Google client secret只到固定Google token端点，PKCE/state/refresh仍复用rmcp/Codex。执中按官方2026-05手册第13页使用固定api_key查询认证，密钥仅在实际HTTP发送层加入，client/控制面保留无密钥URL。

## 当前验证

- Worker56、Native连接器38、前端专项56、Contracts Broker/Host15项通过；Worker/Native Clippy、前端lint、Native同源检查、目录Go race、Go vet通过。
- 两个普通进程内MCP服务覆盖同名工具隔离、多服务精确ref、拒绝0执行、批准1执行且不可重复消费及正常关闭。
- AE配置页按显式输入保留Header原值，未推断认证格式；Google配置、PKCE/callback/token交换和刷新使用进程内普通协议测试；均无供应商网络或实际Keyring I/O。
- Tushare最终通用链路会话01a119b4-c082-7aa1-95b8-22dd55e16427：批准f88876fb-e265-42e9-be1d-99f130a8d0a7，恰好1次HTTP200，000001.SZ/20260105/close=11.5；拒绝af9b7165-dfc8-4459-a1db-c28b33183628，0次HTTP发送、无重试。
- 真实调用对应worker f8f85fa4bafbc3c8a4745b8d5443891a1332bd063d42bf9043aa3c7153ca6d5f。其后执中适配、移除服务和AE配置指引修改另行标准构建，不篡改已有真实验收制品记录，不重复付费查询。

逐项代码审计和源码摘要见Connectors docs/market-provider-generic-code-audit-2026-10-08.{md,json}。其余48项真实调用均未执行，符合Owner的成本限制；旧诊断不足不再阻塞。原2轮/1查询和追加4轮/2查询额度均已用完，后续不再发模型或业务查询。

## 交付边界

仅隔离local候选，无发布、commit或push。固定Codex Runtime未修改，用户已有店铺及其他并行改动未覆盖。没有强杀、权限破坏、攻击fixture、二进制冒充测试。全仓历史ChatPage 5项legacy失败已有基线复现，未宣称全仓CI通过；SQL33仅用于隔离候选。

Runtime elicitation不含item id，Host故意保持工具结果callRef/service为空，不按工具名伪造关联。审批服务名、原轮次选集和真实结果文本仍可见；普通工具事件“信息不完整”是保守兼容投影，不代表请求执行失败。Tushare只开放daily策略，其他253个工具未开放。

整体D4不由专项通过自动置为PASS：完整Must矩阵和Owner真实可用结论仍按02-verification记录。现有真实证据与后续无付费回归在evidence中分别标注，不把不同构建合称一次fresh run。

最终49项候选worker SHA256：`c39ce878d8bdb0a6356176bbb31acae13ded11d6e8eaecc86c5ae84cc57a2928`。标准应用已启动，实际页面六分类总数49，“豆蔻”与“淘宝”搜索均无结果，AE详情正确。进程归属为应用→Host→该worker。回归日志、App/Runtime摘要及未执行项见[evidence/scope49-local-verification-2026-10-08.json](evidence/scope49-local-verification-2026-10-08.json)。
