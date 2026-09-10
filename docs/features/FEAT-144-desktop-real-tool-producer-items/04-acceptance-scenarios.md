# FEAT-144 Sorftime真实MCP验收设计（未执行）

2026-09-10。固定Runtime接入已验证，元数据8/10；用户已排除AC-004/F144-S03业务失败实现/验证，余额充足并授权10次业务请求，已用0。当前依据见[15](15-owner-scope-and-business-budget-2026-09-10.md)；以下产品场景仍未执行。

## 准备与业务样本

product_detail只查询单个公开ASIN，显式amz_site=US。候选B07H9PZDQW有公开出处但不保证Sorftime有数据。原生文本块投影不依赖outputSchema；不因取不到失败样本而阻塞本期。

业务10次上限包含原生重发；一次逻辑调用最多2次tools/call须提前预留，不足不启动，保守上界不可自动返还。元数据8/10独立，模型/图片未授权。真实调用只用于有意义的成功验证，不寻找/制造业务失败，不扩大工具或数据范围。

被排除的业务失败场景与保留的既有安全边界分开：不新增失败分支或业务错误分类；正常缺参数/原生Prompt拒绝仍属于输入/权限回归，不把它算作AC-004通过。历史范围与原文已归档，D4仅评价剩余9项Must和适用的通用检查。

## 场景矩阵

| 场景 | 未来操作 | 判定与限制 | AC |
|---|---|---|---|
| F144-S01安全接入与发现 | 复用操作7/8诊断证据；先做产品白名单/schema/秘密隔离定向核验，必要的产品初始化与发现按16单独编排额度 | 只开放核实的单详情工具；不安装bridge/自写MCP客户端，不把发现算业务成功 | 001/007/009 |
| F144-S02真实成功 | 现有项目Composer请求指定US公开ASIN；原生审批后调用 | 真实McpToolCall ID/status/安全参数/结果/适用duration；助手摘要与真实结果独立核对，缺失保留；不能只凭completed通过 | 002/003 |
| F144-S03真实正常失败（用户排除） | 不实施、不执行 | OWNER_EXCLUDED / NOT RUN；原要求归档，不计PASS，不被其它场景替代 | 004（已移出Must） |
| F144-S04空数据与恢复 | 自然无数据/安全合成返回，随后新的明确有效查询 | availability/empty与status分开；不自动补发、扩查询或推演失败；合成不冒称真实远端 | 003/007 |
| F144-S05生命周期与来源 | 普通Item/Turn结束、缺字段、连接缺口、重复、跨会话定向测试 | 唯一缓冲，不串项/对账/封口；历史/订阅不明不busy，thread/read不冒称亲历started/completed；0progress合法 | 005 |
| F144-S06正常重开 | canonical正常退出并重开同一已保存Tool记录 | 观察事实、原生ID/终态/安全结果保持；原生冷读分来源、不猜合并；旧历史仍可读，兼容reader先于新写入 | 006/009 |
| F144-S07原生权限与秘密 | 必要MCP请求/响应薄适配测试及正常审批交互 | 稳定 elicitation 空表单，按 request/thread/可信 turn 关联；无原生 itemId 不猜 Tool 卡，accept/decline/cancel/resolved 原生处理；一般表单/URL/requestUserInput 拒绝，不设Approve；密钥不进模型/shell/日志/DB/CLI，未证安全阻塞 | 007/009 |
| F144-S08界面和回归 | tool卡、light/dark、1180×760、200%、键盘/折叠/复制，原数据切换 | 只复制安全文字，执行/availability/busy分开；Composer/Command/附件/Artifact/FEAT-152不回归 | 008 |
| F144-S09来源与复用 | Contracts→兼容reader→Host/Desktop激活检查及分离审查 | 原生MCP/缓冲/SQLCipher/历史复用，真实版本/pin；旧schema不原地扩字段，不改Runtime/137或权限策略 | 009/010 |

## 正常入口与停止条件

未来使用pnpm tauri:demo-fast:app，普通com.yijie.ai身份、原app-data与Host Home；先让旧活跃Turn正常结束再正常退出，不复制DB/凭据。Sorftime配置限受管本地会话，不覆盖用户个人Codex全局配置，也不宣称自动限制其它无关配置；真实可见工具范围先核对。

必须分别验证：原生Tool执行事实、实际业务可用结果、模型摘要忠实性、持久来源和权限。自然中断/重连若未出现就记录NOT OBSERVED，不能故障注入。元数据重试不等于新Item；业务HTTP尝试与Item数/模型请求数不是同一台账。

凭据安全、MCP审批承接、schema/来源、预算或旧数据兼容不能确认时停止对应步骤。工具发生schema漂移、未知身份或非白名单调用时拒绝，不通过prompt/客户端推断绕过。禁止攻击fixture、强杀、权限破坏、二进制替换、坏key/断网/耗尽额度制造错误。

剩余9项Must、真实成功、正常重开及保留的既有输入/权限回归完成后才可评价D4；AC-004及业务失败实现/验证已排除，不计入通过数量。原MCP历史、内置备选及FEAT-136的旧PASS不继承。

兼容方向的具体设计与测试准备见[12](12-independent-contract-and-reader-plan-2026-09-10.md)：包括保持原生status事实、版本化reader、单条未来格式不阻断其它历史，以及旧binary版本拒绝。所有新增产品断言尚未执行；本地健康MCP报文比较仅用于诊断，不能替代F144-S02或D4。

## 原生权限模式定向验收补充

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。详见13。

核对实际thread响应/配置及正常模式切换时工具失效；不能仅凭UI隐藏或权限标签PASS。原生Prompt不缓存为后续调用授权；手工取样RPC不算此产品审批验收。当前NOT RUN。
