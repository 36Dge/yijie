# FEAT-162 Search / Fetch 真实最小验收通过

2026-10-24，Asia/Shanghai。**本次目标已完成：复用客户端已有Kimi API Key，通过真实产品worker及现有Broker/Gateway，Search与Fetch各调用一次并成功。模型调用0次，没有供应商重试。**

## 实际结果与次数

| 项目 | 输入/动作 | 实际供应商请求 | 结果 |
|---|---|---:|---|
| 正常拒绝 | 对固定IANA URL的Fetch提案作reject/decline | 0 | PASS；call_admission=rejected，未出现web_http_send |
| Search Basic | IANA example domains；limit=3 | 1 | HTTP200；3条标题、URL、摘要结果，truncated=false；553ms |
| Fetch | https://www.iana.org/help/example-domains | 1 | HTTP200；标题Example Domains，751字符Markdown，truncated=false；4395ms |
| 模型推理、/models、余额及其他Kimi接口 | 未调用 | 0 | 保持约束 |

Search实际返回Example Domains、IANA-managed Reserved Domains、Instructions and Guides三项，全部具有标题、URL及非空摘要。Fetch正文包含示例域名用于文档说明、不可注册或转让等关键事实，与指定IANA公开页面一致。结果经过当前canonical输出schema校验，MCP text与structuredContent一致，均处于65536字节预算内。

本次正式验收一次运行内依次完成拒绝、Search、Fetch；每项批准使用当前call identity和单次批准，HTTP发送许可仅消费一次。两次HTTP200及非空数据各按官方¥0.01/次核算，合计**¥0.02**，符合用户预算。未调用账户余额或账单接口，因此这是依据官方公开单价和实际成功次数的费用核算，不冒充账户账单读数。价格依据：https://platform.kimi.com/docs/pricing/websearch 。

## 查明并修复的原因

此前两个阻塞均来自验收启动/客户端，而非Kimi Key或Search/Fetch适配器：

1. Go启动命令的GOSUMDB=off阻止自动工具链校验。测试启动脚本已改为使用正常校验解析出的官方Go1.26.5，再固定该bin/go、GOTOOLCHAIN=local，保留GOSUMDB=sum.golang.org；不修改用户全局配置。
2. 验收客户端将rmcp正常的空SSE priming事件错误地作为JSON解析。rmcp1.8.0的server_side_http.rs明确以空data发送预热事件，session默认启用；使用该正常协议片段的单元测试先复现失败，再修正为空事件不进入JSON-RPC解码，测试通过，真实worker握手恢复。
3. 握手恢复后，扩展的本地拒绝预检暴露另一个测试客户端问题：rmcp为请求自动附加progressToken，直接交给闭集业务metadata解码会拒绝。已有Codex rmcp客户端的restore_context_meta会移除此协议字段。测试入口按现有实现移除progressToken，再用原生成ElicitationMetadata严格校验，其余校验和批准不放宽；Codex内核没有改动。

随后无真实凭据的本地预检完整通过：初始化、固定工具目录、正常拒绝、零供应商请求及正常EOF。正式验收再次使用已有真实模型Key，并重复验证拒绝零发送后才批准两次业务调用。局部排障的失败日志保留，不把本地修复验证算成付费重试，也没有重放任何已发出的供应商请求。

## 凭据、进程与范围

Key继续由原Host loadKimiAPIKey从客户端既有安全来源读取，经原匿名FD3快照传给产品worker；没有要求用户重复填写，没有输出或另存Key。未绕过批准、不直接curl、不建立Agent循环、不替换产品worker或Runtime、不运行无头浏览器。只修改opt-in验收测试客户端和启动脚本，contract-impact=none。

产品worker SHA256仍为`ebf7c834c95f4614365981aa7b99d04dcff37eb4d709cf4f84d0b04a8e073404`。正式测试退出0，worker正常EOF退出已确认，无App/Host/worker残留；Runtime工作区干净且HEAD保持`9154f27d0cdb526a5f5ba0913fe3e2448014b4a1`。7仓diff检查通过，没有提交、推送或发布。本轮一次性额度已用完并关闭，不能重用记录或追加请求。

本次证明现有Key对两项工具的真实访问、规范化结果、MCP封装和正常批准/拒绝链有效。测试使用合法的确定性协议身份，没有模型回合；不将本次结果扩称为真实Native UI对话、模型自动选工具、结果历史重开或完整D4通过。

## 证据

- `evidence/live-minimal-round3-result.json`：正式结果、逐调用发送次数、HTTP200、耗时、字段检查及最小公开结果元信息。
- `evidence/live-minimal-round3-authorization.json`：授权范围、测试源码摘要和用量结束记录。
- `evidence/live-minimal-round3-run.log`：正式go test通过记录。
- `evidence/live-minimal-round3-preflight-result.json`、`live-minimal-round3-preflight-02.log`：无真实Key预检通过及拒绝零发送。
- `evidence/live-minimal-round3-parser-before.log`、`live-minimal-round3-parser-after.log`、`live-minimal-round3-preflight-first-result.json`：普通协议复现及修复过程；旧失败记录未覆盖。
- `evidence/live-minimal-round3-workspace.json`：各仓状态、Runtime边界和正常退出。

原始测试结果仅保留于本次私有测试目录，公开验收证据省略完整正文和摘要，只保留必要元信息及摘要校验值。原结果SHA256：`539a44663bcf5aa88417fa355794baf175ba810767081e8cca83dce7fc77548b`。
