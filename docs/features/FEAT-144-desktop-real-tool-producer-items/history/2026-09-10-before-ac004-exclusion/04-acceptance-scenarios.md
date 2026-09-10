# FEAT-144 Sorftime真实MCP验收设计（未执行）

2026-09-10。固定Runtime操作7/8已完成原生初始化/列举，8/10次元数据操作，模型/业务/图片0，连接阻塞关闭。当前依据见[13](13-connection-closure-and-d0-review-2026-09-10.md)。以下产品场景均未执行；D0仍待安全普通失败方案；计费和具体预算在业务激活前确认，产品实施与真实D4分别等待适用授权。

## 准备与业务样本

固定Runtime原生发现已确认product_detail及asin/amz_site，首期显式US；不重复试连。只读查询用途已明确，发现返回本身不能证明幂等/错误/计费；不从其它工具推断输出字段、错误或计费。候选公开US ASIN B07H9PZDQW只证明公开出处，尚未证明Sorftime有数据。原生文本块有界投影不依赖outputSchema；可选取样见14，需新业务授权，不触碰卖家账户。

正常失败样本必须满足实际schema、由服务说明可引发普通业务错误。不得假设不存在ASIN必然failed；空结果/completed单独记录。没有安全可触发原生failed时不强行构造或降低AC。可用正常缺失必填输入验证澄清/本地拒绝，但那不是远端MCP失败D4。

建议10次模型Responses、3个逻辑MCP业务调用、最多6次tools/call尝试（保守包括404重发）；元数据初始化/发现原生重试的计费与计量需先确定再批准。当前元数据累计授权10次、已用8次、剩余2次；模型/业务额度0，无密钥/秘密URL写盘、不借FEAT-136剩余额度。

D0与D4分开：固定Runtime原生连接已通过；D0仍缺安全正常失败方案，账户计费/具体预算在业务激活前确认；产品实际成功/失败/重开在后续D4验证，不提前继承PASS。首期秘密仅存内存；原生exclude必须同时核对set不能重注入，真实审批参数来自原生tool_params，enabled_tools不代表已限制US/ASIN，正常重开重新输入，历史读取不依赖再次调用Sorftime。

## 场景矩阵

| 场景 | 未来操作 | 判定与限制 | AC |
|---|---|---|---|
| F144-S01安全接入与发现 | 空ephemeral线程原生startupStatus为ready后另计status列举，验证白名单/schema和秘密隔离 | 只开放核实的单详情工具；不安装bridge/自写MCP客户端，不把发现算业务成功 | 001/007/009 |
| F144-S02真实成功 | 现有项目Composer请求指定US公开ASIN；原生审批后调用 | 真实McpToolCall ID/status/安全参数/结果/适用duration；助手摘要与真实结果独立核对，缺失保留；不能只凭completed通过 | 002/003 |
| F144-S03真实正常失败 | 执行服务支持的普通业务失败条件 | Runtime真实failed和安全错误；空数据completed不算；无安全样本则该Must未通过，不以Command替代 | 004 |
| F144-S04空数据与恢复 | 自然无数据/安全合成返回，随后新的明确有效查询 | availability/empty与status分开；不自动补发、扩查询或推演失败；合成不冒称真实远端 | 003/004/007 |
| F144-S05生命周期与来源 | 普通Item/Turn结束、缺字段、连接缺口、重复、跨会话定向测试 | 唯一缓冲，不串项/对账/封口；历史/订阅不明不busy，thread/read不冒称亲历started/completed；0progress合法 | 005 |
| F144-S06正常重开 | canonical正常退出并重开同一已保存Tool记录 | 观察事实、原生ID/终态/安全结果保持；原生冷读分来源、不猜合并；旧历史仍可读，兼容reader先于新写入 | 006/009 |
| F144-S07原生权限与秘密 | 必要MCP请求/响应薄适配测试及正常审批交互 | 稳定 elicitation 空表单，按 request/thread/可信 turn 关联；无原生 itemId 不猜 Tool 卡，accept/decline/cancel/resolved 原生处理；一般表单/URL/requestUserInput 拒绝，不设Approve；密钥不进模型/shell/日志/DB/CLI，未证安全阻塞 | 007/009 |
| F144-S08界面和回归 | tool卡、light/dark、1180×760、200%、键盘/折叠/复制，原数据切换 | 只复制安全文字，执行/availability/busy分开；Composer/Command/附件/Artifact/FEAT-152不回归 | 008 |
| F144-S09来源与复用 | Contracts→兼容reader→Host/Desktop激活检查及分离审查 | 原生MCP/缓冲/SQLCipher/历史复用，真实版本/pin；旧schema不原地扩字段，不改Runtime/137或权限策略 | 009/010 |

## 正常入口与停止条件

未来使用pnpm tauri:demo-fast:app，普通com.yijie.ai身份、原app-data与Host Home；先让旧活跃Turn正常结束再正常退出，不复制DB/凭据。Sorftime配置限受管本地会话，不覆盖用户个人Codex全局配置，也不宣称自动限制其它无关配置；真实可见工具范围先核对。

必须分别验证：原生Tool执行事实、实际业务可用结果、模型摘要忠实性、持久来源和权限。自然中断/重连若未出现就记录NOT OBSERVED，不能故障注入。元数据重试不等于新Item；业务HTTP尝试与Item数/模型请求数不是同一台账。

凭据安全、MCP审批承接、schema/来源、预算或旧数据兼容不能确认时停止对应步骤。工具发生schema漂移、未知身份或非白名单调用时拒绝，不通过prompt/客户端推断绕过。禁止攻击fixture、强杀、权限破坏、二进制替换、坏key/断网/耗尽额度制造错误。

十项Must全部满足且真实成功、正常failed、正常重开均完成后才能MCP D4 PASS；如果服务只返回空数据而无failed，保留未通过状态并明确限制。原MCP历史、内置备选及FEAT-136的旧PASS不继承。

兼容方向的具体设计与测试准备见[12](12-independent-contract-and-reader-plan-2026-09-10.md)：包括原生failed/result存在/error=null、版本化reader、单条未来格式不阻断其它历史，以及旧binary版本拒绝。所有新增产品断言尚未执行；本地健康MCP报文比较仅用于诊断，不能替代F144-S02/S03或D4。

## 原生权限模式定向验收补充

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。详见13。

核对实际thread响应/配置及正常模式切换时工具失效；不能仅凭UI隐藏或权限标签PASS。原生Prompt不缓存为后续调用授权；手工取样RPC不算此产品审批验收。当前NOT RUN。
