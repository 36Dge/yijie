# FEAT-144 连接问题收口与 D0 审定

> 阶段历史：本文保留当时连接闭环与D0 BLOCKED依据。用户随后明确排除业务失败场景并授权10次业务请求，当前D0/范围以[15](15-owner-scope-and-business-budget-2026-09-10.md)为准；本文末尾索取失败/计费说明的行动已被该决策替代，不再作为前置。

2026-09-10。用户明确要求同步成功结果、补齐业务依据、审定契约/兼容方案和重跑 D0；D0 通过并另获实施授权后才编码。本轮实际 contract-impact=none，只更新需求和证据，不改产品契约/代码、Runtime、pin 或用户数据。

## 已关闭的连接阻塞

固定 Runtime **0.144.6** 于 `2026-09-10T05:31:24Z` 开始的操作 7 收到原生 `starting → ready`；操作 8 返回 **97 个工具**，服务为 Sorftime MCP 1.1.6，`product_detail` 输入 schema 与操作 5 一致。两项操作共用进程正常 unsubscribe/EOF 退出，exit 0；新增运行文件及输出未检出输入秘密。证据见[成功收据](evidence/fixed-runtime-user-agent-success-2026-09-10.json)、[原生操作8](evidence/sorftime-native-discovery-operation-8-2026-09-10.json)、[固定版本工具schema](evidence/sorftime-product-detail-fixed-schema-2026-09-10.json)。操作7启动事件及时间保存在共用台账。

已验证配置为无 query endpoint、原生 Bearer 环境引用及真实版本 User-Agent：

```toml
[mcp_servers.sorftime]
url = "https://mcp.sorftime.com/"
bearer_token_env_var = "YIJIE_FEAT144_SORFTIME_ACCOUNT_SK"
http_headers = { "User-Agent" = "codex-mcp-client/0.144.6" }
```

这只是接入配置片段，完整受管配置仍需保留原有来源、权限、超时、秘密和插件限制。后续产品实施中 User-Agent 依据被验证的真实 Runtime 版本设置，不伪装其他版本。此次仅在诊断配置验证，没有写入 Host/应用产品配置。

本地线报文差分找到了旧版没有 User-Agent、新版存在该头的事实；固定版本仅通过原生配置补上真实 UA 后成功。因此关闭“固定 Runtime 无法原生初始化”的接入阻塞，记录 **User-Agent 配置修正有效**。不宣称已经取得 Sorftime 服务端/WAF 拒绝规则或唯一内部根因，也不通过移除修正再次制造400。

**累计8/10次原生元数据操作、剩余2次；模型/业务/图片0。** 本轮同步和审查新增调用0，不重复试连。操作7/8的summary是同一进程的共享摘要，其中观察到6个POST跨度，不能将两份summary相加成12次；完整HTTP计数仍unknown。元数据额度不能用于tools/call。

本结论仅证明固定来源原生元数据接入可行；不是 product_detail 业务结果、原生Tool Item、权限UI、canonical 或D4验收。操作1–3及6的失败、操作4/5的0.153.4对照成功分别保留历史范围。动态权威是[台账](evidence/sorftime-discovery-ledger-2026-09-10.json)，旧证据JSON和历史四文件不改写成成功。

## 业务依据与边界

| 事项 | 本次审定 | 依据/限制 |
|---|---|---|
| 工具/输入 | sorftime/product_detail；一个明确公开ASIN，显式amz_site=US | 操作8真实schema；required仍仅asin，不篡改原始schema |
| 产品入口 | 原有项目Composer；实际参数由用户意图及原生Prompt确认 | enabled_tools只限制名称，不能冒称限制站点/ASIN |
| 只读用途 | 单商品资料查询，不选收藏、监控、订阅、批量或写工具 | 原生描述及官方包支持查询用途；不承诺服务不更新缓存/计量 |
| 幂等 | 不承诺结果恒定、服务端去重或重试免费 | 商品数据会变；没有annotations/正式幂等承诺，不补造 |
| 结果展示 | 原生text内容块的有界安全纯文本；具体规则见下文和12 | 不要求outputSchema，不解析中文字段或假造价格单位；实际业务内容尚未取样 |
| 计费 | 模型、逻辑MCP业务操作、可观察tools/call尝试、元数据操作分账 | 官方包有MCP套餐起价，非账户实际价格；工具权重、空/失败/恢复重发如何扣费仍未知 |
| 正常失败 | 保留真实原生failed及安全文案；没有数据不等于failed | 目前未找到product_detail符合范围的普通失败条件，不以坏key/断网/耗尽额度/攻击制造 |

官方包 `SKILL.md:77` 的 MCP 资源包起价只作为包内说明，不将 API/CLI 价格或包内起价当作用户当前账户计费契约。`product_detail`描述支持查询用途，但不能据名称补出readOnlyHint或idempotentHint。包内键值文本解析也不是外部稳定outputSchema。官方公开资料和ZIP审查见[业务依据核验](evidence/d0-business-basis-review-2026-09-10.json)。

原生重试的实现依据已明确：普通暂态重试名单包含initialize、initialized、tools/list，不包含tools/call；已有session收到404时，固定Runtime会重新初始化并再发一次原业务操作。一次逻辑业务调用需保守考虑两次tools/call尝试。正常SSE重连/握手/清理与业务尝试分开，不能承诺全部HTTP总量为1或2，也不能承诺服务端只扣一次。复用原生恢复，不另建重试器。

## 结果与兼容方案的审定补充

新增安全结果扩展选择**原生文本块**，不等待不存在的业务outputSchema：只处理实际type=text且text为string的内容，保留原生content数组索引；不将structuredContent、资源、图片或_meta透传。最多处理32个原生content条目，总文本上限复用现有nativeTextLimit（256 KiB UTF-8），复用现有安全文本/UTF-8截断与已审查的完整文本脱敏helper。容量计算仅针对当次完整对象，不建立跨事件内容累积器。

沿用完整文本脱敏时，应在源契约中准确披露可能隐藏整行的行为；被隐藏/截断/格式不支持分别记录投影诊断。**safeNativeText只做NUL/容量处理，不能单独称为秘密脱敏。** 原始结果及错误不得先入日志后脱敏；真实数据若不能安全展示，availability如实降级，不能据此通过业务成功AC。只显示“服务返回文本”，不激活链接、不执行内容指令、不自动下载资源。

原生result缺失、content空、空字符串text、仅有未支持类型、全部被安全处理省略、存在可展示文本分别保留；“没有可展示文本”不得写成“商品不存在”。原生failed即使result存在/error=null仍failed，不从结果正文重新裁决状态。模型摘要忠实性在D4独立验证。

兼容读取增加独立的本地recordDiagnostics载体：仅关联已知本地session/turn位置和payload格式，包含format_unsupported等安全原因，不伪造NativeView、原生ID或终态；不能让后续native_recovery_views把这类记录误当缺view再冷读补建。数据库版本高于支持版本仍整库拒绝；单条未来payload隔离只适用于数据库版本可读时，不承诺任意未来数据库可读。

facts/views使用明确格式标记，旧记录默认旧格式，保持旧JSON原样；新的前向expand migration与兼容reader先行，旧binary由已有user_version门禁拒绝。回滚只到经验证的兼容reader，不降回不能识别新格式的version14旧binary。详细方向、测试和执行次序在[12](12-independent-contract-and-reader-plan-2026-09-10.md)。本轮只审定实施依据，不执行migration。

审批参数也必须来自原生请求中实际提供的tool_params等有界元数据，不能把审批面板固定写成US或从助手正文猜ASIN。元数据只作呈现，不自行授予权限、不推断Tool Item关联；未能确认本次参数符合已定范围的请求继续拒绝。保持FEAT-152既有模式语义。

### 原生权限模式与激活范围

固定源码 `codex-rs/codex-mcp/src/mcp/mod.rs:79` 及 `core/src/mcp_tool_call.rs:1215` 表明：Never配合full-access会原生自动批准，即使工具配置为Prompt；guardian或permission-request hooks也可能替代人工面板。因此不能把“有Prompt配置”写成“每次必有人确认”。

首期Sorftime只在现有FEAT-152“请求批准”模式且RuntimePermissionsEnabled=true时激活；未知、缺失或不匹配的有效配置不激活。复用Host `internal/codex/runtime_permissions.go:36–55` 的ValidatePermissionMode/permissionPolicy及既有StartTurnV2映射，核对实际配置为approvalPolicy=on-request、approvalsReviewer=user、sandbox=workspaceWrite、networkAccess=false。固定thread/start/resume响应已有这些原生字段；Host目前threadResponse未完整保留，后续只补原生效力薄适配，不新建权限推演表。config/read有效配置还须精确enabled_tools=[product_detail]、该工具approval_mode=prompt、无Approve或未知覆盖，并保留受管hooks/插件隔离，不能有替代本次人工审批的hook/plugin/guardian。不能只根据UI标签断定有效权限。

原生Prompt始终要求工具预审批，且不会命中Auto模式的session/persistent批准缓存（core/mcp_tool_call.rs:1397、:1418、:2182）；无需另建批准缓存或禁用原生机制。每次实际请求的tool_params经有界校验显示给用户，只接受明确的一次US单ASIN查询；单次逻辑调用的原生404重发仍包含在该次操作/预算内，不承诺第二次弹窗。

“帮我批准”“完全访问”保持FEAT-152原语义，本期Sorftime在这些模式不激活；其它已支持工具不被重定义。此限制须作用于原生MCP配置/工具可用性，不能只隐藏UI。已启用Sorftime的会话若要进入其它模式，先正常结束活跃Turn，再使用受支持的原生配置/受管Runtime正常停止与启动路径让Sorftime不再可调用；无法确认失效时停止相应激活/切换步骤并报告，不强杀、不猜测失效、不自动改回权限模式。产品生效核验和正常切换属于后续实施/定向验证，当前只冻结设计。

## 准确的 D0 结论

- 已完成：固定原生接入、真实工具/输入schema、用户入口和最小范围、原生结果展示设计、秘密/审批薄适配设计、版本化契约/reader/回滚方案。
- 不再作为D0阻塞：固定Runtime原生连接、缺少outputSchema/annotations/progress、产品尚未编码或D4尚未运行。
- D0剩余规划缺口：当前AC-004尚无有依据、可执行的正常业务失败方案。若服务没有符合范围的安全条件，应请用户决定如何调整该AC，不能静默用空结果或审批拒绝代替。
- 业务激活前置：账户实际计费、空/失败/恢复重发扣费以及具体预算仍须确认；缺少业务预算或成功样本本身不阻止设计定稿。公开ASIN不代表已知有数据。[14备用取样](14-bounded-native-business-sample-2026-09-10.md)当前不申请/不执行，也不是D0必经步骤。

因此当前D0保持BLOCKED、product_ux=pending、十项Must pending、实现/D4 NOT RUN。不是通过改字段取得PASS，也不要求先完成D4来通过规划。一次成功取样可以核对返回格式，但不能自动证明扣费规则或普通失败条件。

本轮与起草分离的审查已检查原生状态/参数、文本结果、单条格式隔离和数据库版本边界。适用检查真实结果见[本轮门禁](evidence/d0-closure-checks-2026-09-10.json)。后续只有D0通过且另获实施授权，才按Contracts→兼容reader→Host/Desktop原生适配→定向验证→canonical→真实D4推进；模型/业务预算与提交/推送分别按明确授权执行。

## 下一步需要的正式业务说明

优先向Sorftime核实以下具体问题（本任务未代发消息，也不为取得答案发起业务调用）：

1. 对 `product_detail`、单公开ASIN、`amz_site=US`，是否存在不使用坏凭据、不破坏网络、不耗尽额度且符合输入schema的普通业务条件，会返回真正的MCP工具错误？请提供可用参数、脱敏响应示例及 `isError`/协议错误语义。若只返回空content或普通文本，请明确说明，不能把它预定为原生failed。
2. 当前MCP账户中，正常数据、空结果、业务错误、原生会话404恢复重发各如何计费/扣配额？initialize/tools/list及其它元数据请求是否计费？请以此账户和此工具为准，不套用API/CLI或通用起价。

取得可执行失败方案后复核AC-004与场景并重跑D0。若官方确认没有符合范围的安全失败条件，向用户提交AC-004可实现性与范围决策，保留原AC历史；不能自动降低Must或将本地拒绝/空结果写成PASS。计费与具体授权在真实业务激活前落实；不为一个已确定的通用文本展示设计无效申请取样。
