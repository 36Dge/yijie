# FEAT-144 不依赖外部连接的契约与兼容设计

2026-09-10。用户确认：连接问题若仍不能解决，记录问题并继续 FEAT-144 中不依赖连接的后续工作。本轮完成源码审计和下列实施依据，**没有实施产品代码、migration、契约生成或新字段写入**；D0/实施授权边界继续保留。本文件不是已通过的产品验收。

当前更新：固定Runtime已原生接入；用户按[15](15-owner-scope-and-business-budget-2026-09-10.md)排除业务失败场景实现/验证、确认余额并授权10次业务请求。以下保留原生成功/展示/安全/兼容设计，移除独立业务失败扩展；原D0阻塞和旧AC要求留在历史，不作为当前实施前置。本轮仍仅设计，无产品代码或migration。

## 已有字段复用与最小缺口

| 事实 | 现状 | 后续实施决定 |
|---|---|---|
| 原生 Item 身份/status | NativeItem 已有 id/type/status | 原样复用；MCP 仅原生 inProgress/completed/failed，不从审批或 Turn 造 declined/interrupted |
| 内容 availability | 已有独立字段，但 Host MCP 恒 partial | 根据实际可展示内容和明确限制投影，不能替代原生执行结果 |
| durationMs | 契约和 Host decoder 已有，MCP 分支未传 | 直接使用合法原生值，保留 0，缺失不推算；无需新耗时机制 |
| argumentsSummary | 已有字段 | 只取实际参数中的单个公开 ASIN 与显式 US，校验后显示，不公开任意原始参数 |
| resultSummary | 现有契约限定 metadata only | 保留元数据用途，不能悄悄改为任意业务正文 |
| 工具身份 | 原生 server/tool 存在；Host 没有 server decoder，Desktop 由通用标签虚填 identity | 新版本增加有界原生 server/tool 身份；未知保持缺失，不把标签当注册身份 |
| 原生错误 | 已有原生status及通用安全文案 | 复用已有事实处理；按用户决定不新增MCP业务error字段、错误分类或专用失败分支 |
| 投影诊断 | availability 缺 Item 级原因 | 新版本增加有限显示字段/原因码，明确不是 Codex 原生错误码 |
| 安全结果 | 原生 content[]/structuredContent/_meta，现仅“结果已接收” | 独立的安全结果扩展；不复用桥接器猜字段/改参数/文本化错误 |
| progress | 协议声明存在，真实生产未证实 | 首期允许 0，不新增步骤、百分比、轮询或缓存累计器 |

源码依据：Contracts `openapi/native-conversation/native-conversation.yaml:124`；Host `internal/session/native_conversation.go:18`、`:168`；Codex `app-server-protocol/src/protocol/v2/item.rs:301`、`v2/mcp.rs:131`；Desktop `src/domain/conversation-view.ts:368`。

重要区别：Codex core 根据远端 `isError=true` 将原生 Item 标为 failed；该 Item 可以同时 result 存在而 error 为 null。app-server 的 McpToolCallResult 本身不再暴露 isError，**Host/Desktop必须保留原生 status，不因 error=null 改成 completed，也不从正文恢复或猜 isError**。依据 `yijie-codex/codex-rs/core/src/mcp_tool_call.rs:918`。

## 新契约的范围

采用新版本的封闭 MCP 显示扩展，字段名在 Contracts 源变更时最终冻结，语义已固定：

- identity：有界 server/tool，只有可信原生值才存在；不从时间/正文补身份。
- 业务error扩展移出本期：沿用原生status与已有安全呈现，不新增业务错误字段/专用失败流程；不吞错或把原生failed改成completed。
- diagnostics：有限字段名和显示原因，如结果格式不支持、内容省略、容量限制；与 status 分离。
- result：区分原生结果未提供、明确空内容、存在但当前格式未支持、存在可展示内容。JSON 中 0/null/空字符串不得被 truthy 判断吞掉。业务字段、单位和样本尚无充分依据，不预填价格/销量等字段。

禁止原样公开 arguments、error、任意 structuredContent、_meta、返回 URL/图片/资源内容。包内中文键值解析只是资料线索，不作为已知 outputSchema。未知格式可安全表示“不支持”，但不能因此通过真实商品成功 AC。

### 原生文本结果的具体规则

`McpToolCallResult.content` 是固定协议已有的内容块数组。首期新增结果扩展仅投影其中实际 `type="text"` 且 `text` 为字符串的条目，保留原生数组 `contentIndex`，展示标识由原生 Item ID、结果内容类别和该索引组成。不能先过滤再重新编号，也不把多个块拼成一段后猜切分；每次完整 Item 到达直接替换当次结果。

- 最多检查前32个原生 content 条目，总安全文本上限复用 Host 现有 `nativeTextLimit`（256 KiB，UTF-8字节）。跳过的格式仍占原生索引；条目数超限和文本容量超限分别诊断。计数仅针对当前完整对象，不复用旧Delta累积器或建立跨事件预算状态。
- 复用 `feat136_redaction.go` 的完整文本 `redactV5CommandText` 及其既有安全分类，随后复用 `safeNativeText`/`truncateV5UTF8` 的有界输出处理。保留既有transport消息上限；不能先截断原始行再脱敏，以免切断秘密特征。`safeNativeText`只处理NUL/容量，不能单独称为秘密脱敏；输入校验仍须覆盖原始文本中的NUL及不支持形状。
- 完整文本helper会规范化控制字符，并可能将含URL、路径、凭据特征等的整行替换为固定标记；新源契约必须披露这一显示损失。实际发生的安全处理、截断、未支持格式使用独立投影原因，不能只看结果正文是否含标记就认定曾有秘密或修改原生状态。不得为提高商品展示率放宽既有规则；也不宣称该helper能识别全部语义性敏感信息。
- 卡片标题为“服务返回文本”，使用纯文本节点；不激活返回链接、不执行正文指令、不自动下载图片/资源，不把 `structuredContent`、`_meta` 或任意JSON序列化成正文兜底。模型摘要与实际返回的忠实性另在D4核对，安全处理后的片段不冒充完整商品数据。

结果可用性必须分别保留：result未提供/null、明确空content、实际空字符串text、仅有未支持格式、内容被安全处理省略、存在安全可展示文本。空字符串是已提供的文本条目；仅有structuredContent时记“存在未支持内容”，不能写成空商品结果。没有可展示文本只能提示当前可用性，不能推断“商品不存在”；不解析正文中的错误词或空值标记裁决completed/failed。原生字段中的0/null/空值保留其存在性，未支持字段不得通过透传来满足该要求。

依据当前闭合 schema 推导的新版本候选为 native-conversation v2、SSE v8、native-thread v2；这是本次 MCP 新字段需要的版本方案，不继承早期 view_image 提案的通过结论。旧 v7/v1 保持原语义，两个投影不能各自维护生命周期。所有活跃新对话仍只有一个 NativeDisplayBuffer。

Desktop 采用与现有 Native Command 同样的只读适配形状：`ConversationNativeToolExecution` 包含原生 source、lastMethod 和 item。旧 ConversationToolExecution 留作旧历史兼容；删除新链路中虚填 startedSource、lastSource、空时间戳、unknown identity 和 progress 的转换。卡片 busy、默认展开和执行文案复用 `conversation-timeline.ts:481` 的可信活跃 Turn 判断，不回写 status。

原生 elicitation 薄适配设计继续按 10 执行：只承接当前允许的 Sorftime Prompt 空 form，按 request/thread/可信 Turn 定位，没有原生 itemId 不猜 Tool 卡；accept/decline/cancel/resolved 原生处理，回调不落库。该权限请求边界与显示扩展在 Contracts 分别治理，不能把 UI 点击视为自行放行权限。

`enabled_tools=["product_detail"]`只限制工具名称，不限制其ASIN或站点。审批面板必须从本次原生请求实际提供的有界 `tool_params` 显示参数，不能固定写US、套用上次参数或解析助手正文猜ASIN。固定源码 `core/src/mcp_tool_call.rs:1786` 把原生实际参数写入该元数据；元数据只作安全呈现，不自行构成授权、不恢复工具身份或Item关联。只接受用户通过原生Prompt确认的一次明确US单公开ASIN查询；参数缺失、形状不受支持、超出已定范围或不能确认本次范围时拒绝，不靠prompt承诺或工具名补齐。原生请求绑定/生命周期与FEAT-152模式不变，一般表单、URL、实验requestUserInput继续拒绝。

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。详见13。固定原生Prompt不复用Auto批准缓存；生产threadResponse仍需保留原生有效权限字段，不能把现有配置集成测试当作产品生效验证。模式切换需先结束活跃Turn、确认原生工具已失效，否则停止对应步骤，不只隐藏UI。

[14](14-bounded-native-business-sample-2026-09-10.md)的稳定手工 `mcpServer/tool/call` 是业务额度内的备用取样方案，不经过模型Prompt、也不产生原生McpToolCall Item；它不能进入产品调用链，不能把其 `isError` 合成Item状态或用于通过AC-002/006/007。

## 兼容 reader 与回滚

当前 Rust 生成 DTO 使用 deny_unknown_fields，前端 AJV 也封闭；`native_conversation_storage.rs:33–55` 中单条 view_json 解析失败会使整个批次 DatabaseUnavailable。仅声称“先 reader”不够，必须处理以下方向：

1. 新 reader 按明确持久格式标记分派旧格式与当前新格式，分别严格校验，不全局关闭未知字段检查。新migration为facts/views分别增加版本标记，旧记录默认旧格式；不重写现有fact_json/view_json，不由字段内容猜版本。数据库schema版本与payload格式版本分别维护。
2. 当前数据库版本受支持、记录有可校验的版本标记但payload格式较新时，保留SQLCipher中原记录，将本地读取结果分为可读views和并行的 `recordDiagnostics`。诊断仅含已校验scope下的本地session/turn位置、payload格式和固定 `format_unsupported` 原因；不构造NativeView、Runtime ID、Item、执行状态或结束时间。worker、IPC及前端读取结果须一并承接该载体；涉及跨边界的形状先由适用源契约治理，不能手写影子DTO。
3. 含 `format_unsupported` 的本地turn必须从同次 `native_recovery_views` 的缺view冷读补建及恢复写入路径排除；不能把已保存但暂不可读的记录当成缺失记录。调用方不得据此续跑、补发或覆盖原记录；其它可读历史继续正常返回。已知格式的损坏/解析错误及数据库错误不伪装成未来格式，保留其适用错误处理，不关闭校验。
4. 新写方在 reader 基线完成验证前不能写新格式。facts/views 的所有实际读写、worker/IPC和恢复入口都要核对；版本标记与payload在同一事务内写入。不能只改前端DTO，或只给view_json加标记而遗漏fact_json后宣称兼容。
5. 旧 binary 也必须能被已有门禁明确阻止误读新格式。当前数据库版本 14、view_json 无格式标记；同为版本14的旧 binary 不知道新字段，仅有文档禁止回滚无法提供机器保护。

推荐候选是 **一条新的前向格式兼容 migration**：增加明确版本标记并复用 `migrations.rs:119–127` 的高版本拒绝机制，先随兼容 reader 落地，再允许新写入。不改旧0014、不重写旧历史、不复制用户数据库、不另建存储链。回滚目标是已验证兼容的新 reader 基线，不能回滚至不识别新格式的旧 binary；旧历史仍由兼容 reader 正常访问。

数据库 `user_version` 高于当前binary支持值时仍整库拒绝打开/迁移；单条未来payload隔离仅在数据库版本可读时适用。不能为了展示其余历史绕过高版本门禁，也不承诺任意未来migration可读。启用新writer前记录兼容reader最低完整来源；回滚保留新数据库和原事实，只能启动这一已验证基线或更新的兼容版本，不能降回version14旧binary或用删除新事实完成降级。

因此未来实施的 `database_change` 从无条件 none 调整为 **expand（候选设计，未实施）**；不能把这个设计写成已授权执行数据库迁移。本轮没有新增数据库文件或变更用户数据。若后续选择完全不做 migration，必须先另给等效、可验证的旧 binary 拒绝机制，不能保留未兑现的回滚承诺。

## 可独立准备的定向验证

| 检查 | 普通安全数据与断言 | 当前状态 |
|---|---|---|
| 新旧源契约方向 | 旧 v7/v1 样例不变；新扩展只由新 reader 接受 | 设计完成，未生成/执行 |
| Item 投影 | 原生成功Item、零耗时/缺耗时、完整对象保真；不新增业务失败场景测试 | 设计完成，未实施新投影 |
| 文本与容量 | 原生索引经未知块/空块仍稳定；32条目/256KiB、完整行脱敏、Unicode截断及省略原因；不将无文本判成无商品 | 设计完成，未实施；普通合成内容，不用攻击fixture |
| 完整替换 | 普通多 Item/Unicode；更短、不同、空的完整对象替换，不对账 | 复用既有缓冲；本次新增MCP断言未执行 |
| 展示 busy | 已结束Turn中的inProgress Item、冷历史、订阅缺口均不误报执行中 | 设计完成，未改卡片 |
| 持久方向 | 自建普通合成SQLCipher数据，受支持DB内旧/新/未来payload混合；recordDiagnostics不伪造NativeView，未知记录不进入缺view补建/恢复写入 | 待兼容reader；不复制用户DB或故障注入 |
| 正常重开/旧端拒绝 | 正常关闭、重开，新格式来源保持；较旧binary按DB版本拒绝；回滚至兼容reader仍可读 | 待实施；不能假称当前已通过 |
| 审批参数 | 实际tool_params中的本次US/单ASIN供原生Prompt确认；缺失/越界不以固定UI或助手正文补齐，手工RPC不冒充审批链 | 设计完成，未实现产品适配 |
| 相关回归 | Composer、Command、附件、Artifact、FEAT-152 | 后续按实际改动定向执行 |

本期顺序固定为 **Contracts 源与生成物 → 兼容 reader/版本拒绝 → 固定 reader 最低来源 → Host 新投影与 Desktop 新写入 → canonical → 真实 D4**。原生文本投影不等待业务outputSchema；AC-004业务失败场景已按15由用户明确排除，不再要求实现或验证；业务10次已授权，模型预算另行确定。D0按调整后范围重跑，真实成功与剩余9项Must在之后D4验证。排除不算PASS。

## 本轮完成的既有基线检查

[实际检查记录](evidence/independent-native-baseline-checks-2026-09-10.json)：Host原生thread/read及Item/Turn独立性定向检查通过；Desktop Native展示6项通过；SQLCipher原生事实正常重开/冷历史冲突、schema13前向迁移不回填原生历史各1项通过。Go初次关闭校验数据库导致工具链核验拒绝，移除GOSUMDB覆盖、保留正常checksum校验及GOPROXY=off后通过。没有改门禁或下载依赖源码。

这些结果验证已有FEAT-132基础能力；上表的新契约、新格式reader和FEAT-144产品断言仍未执行，不能自动继承PASS。前轮分离审查结论保留其当时范围；本轮再次审查后补齐了文本块、记录诊断与冷读排除、DB/记录版本及实际审批参数的设计缺口，不把设计审查称为独立人工批准或产品通过。
