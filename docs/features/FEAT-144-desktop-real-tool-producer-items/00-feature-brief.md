# FEAT-144 — Sorftime 真实 MCP 工具与原生执行记录

2026-09-11；demo_fast / local。固定Runtime 0.144.6原生元数据接入已通过，无query URL、原生Bearer环境引用和真实版本User-Agent方案不变。用户本次明确排除业务失败场景的实现/验证，并确认余额充足、授权10次MCP业务请求。当前权威见[15范围与预算决策](15-owner-scope-and-business-budget-2026-09-10.md)，连接技术依据仍见13。

当前本地D4保持PASS，九项活动Must满足、AC-004始终用户排除。获本次明确授权后，22个提交已按Contracts→Host→Desktop→元仓普通推送，逐仓远端SHA一致；CI均未触发，NOT RUN。累计文本9/13、元数据14/20、业务2逻辑调用保守扣4/10、图片0，本次新增0。实际来源与远端结果见[26](26-remote-delivery-2026-09-11.md)；本次新增结果记录仅本地提交，不超出22个提交追加推送。

## 目标、工具与入口

首期产品场景定为：用户在现有项目会话中查询**一个 Amazon US 商品的详情**，看到真实 Sorftime MCP 调用、安全参数/结果摘要、原生成功或失败，以及正常重开后的同一记录。原 CAP-017/GS-004 真实 MCP 目标恢复为本期主线，当前本地范围已完成验收证据。

选择服务 sorftime，公共基址 https://mcp.sorftime.com，用户提供的传输标签为 streamableHttp。官方公开资料说明具备产品数据查询；本轮原生返回已确认 product_detail 及inputSchema：asin为必填string，amz_site枚举含US且默认Unknow，首期显式传US。**outputSchema/annotations本次未返回并保持缺失；已确定只读查询用途，服务端幂等保证和具体扣费公式不能推定；用户已确认余额并授权10次业务请求，普通业务失败场景不在本期**，不能把公开仓库的桥接别名、amzSite/amz_site等参数猜成此账户的直接服务schema。

只启用经过核实的单商品详情工具；不默认启用Sorftime全部工具。原生 enabled_tools 精确限制工具名，不能代替ASIN/站点限制；原生审批提供的真实tool_params须有界呈现并确认本次ASIN及US范围，不从模型文字猜测，参数无法确认则拒绝。工具缺失/改名/schema漂移时拒绝激活，不自动换工具。暂不启用搜索、评论批量抓取、收藏增删、监控、导出或其它平台工具。

唯一发起入口为现有“选择项目 → Chat Composer → 正常发送”。用户明确给出US站点和一个公开ASIN，例如“使用Sorftime查询这个US商品的详情，并说明信息缺失”。参数不足先通过正常对话补齐，不扩大查询。模型决定实际工具调用；工具卡只从真实McpToolCall产生，不解析助手正文补卡。

## 五项产品决策

| 决策 | 当前方案 |
|---|---|
| 工具 | sorftime的单ASIN详情查询；product_detail已原生确认，asin/amz_site输入schema由固定Runtime操作8确认；输出采用原生文本块安全投影，余额由用户确认、业务请求上限10次；不实现或验证业务失败场景 |
| 用户问题 | 快速得到指定商品的基础信息和可核对摘要，并知道数据来自哪里、调用是否完成/失败或无数据 |
| 入口 | 原有项目会话Composer，原生MCP配置由Host的受管本地配置适配；无新MCP客户端/直接HTTP业务入口 |
| 访问范围 | 只读Sorftime的US公开商品数据，仅指定ASIN；不上传项目文件、图片、订单/买家/账户资料，不执行商家写操作 |
| 安全验收 | 真实商品成功、安全空结果判别及正常重开；AC-004/F144-S03按用户决定排除，不算PASS；已有权限/来源安全回归保留 |

Sorftime是现成的外部producer；Codex已有MCP协议客户端、发现、调用、身份、生命周期、历史。易界不在Connectors、Host或Runtime重写该服务的执行器，不复制Sorftime公开项目的bridge/SDK来绕过原生链。

## 当前事实与范围纠正

原2026-08-30四文件和D0 BLOCKED/8AC pending完整归档。刚才view_image方案仅为用户提供真实MCP前的未实施备选，已放入history/2026-09-10-builtin-proposal，不是当前主线、不计MCP成功或失败。ImageView、Command和dynamic generate_image都不能替代本次真实McpToolCall证据。

Codex原生McpToolCall有id/server/tool/status/arguments/result/error/duration；实施前Host只投影通用标签、参数隐藏、结果已接收且恒partial，Desktop伪填旧DTO并可能误报历史忙碌。当前实现已按[16实施记录](16-native-implementation-2026-09-10.md)修复这些适配缺口，canonical启动及新Tool重开已完成，D4结果见24，直接保留原生事实，不新造生命周期。

原生progress协议存在，但当前固定app-server生产发送未证实、native通道也未接通。允许0条progress；首期不以持续进度为Must，不新增假步骤、百分比或轮询。只有实际支持并收到原生通知才能显示。Tool冷历史复用thread/read/resume；MCP的Legacy保存规则与Command/ImageView不同，既不保证全部完整，也不一概声称不能恢复。

## 凭据、网络和权限

文档仅保存server名、类型、无秘密origin及秘密引用说明。用户最初提供query-key，随后官方文档确认Bearer，当前已验证无query的原生Bearer路径和真实版本User-Agent，也不把 type:streamableHttp 原样复制为Codex TOML字段。

官方Codex/ClaudeCode文档已确认无query的 https://mcp.sorftime.com/ 与 Authorization: Bearer <Account-SK>。固定Runtime已验证的D0方案为原生 bearer_token_env_var 加 http_headers 中真实版本User-Agent：秘密只经受管输入进入发现Runtime子进程内存，CLI/配置仅变量名；使用临时空ephemeral线程监听原生startupStatus；操作7ready后，操作8单独计工具列举；本轮不重复执行，不启动模型/命令。正式产品的shell环境隔离已按16–20完成适用定向核验，相关文件来源适用性见24；该段临时诊断不替代产品验收。**query-only 内存注入已发现明确日志泄漏路径，当前不得激活**：原生 OAuth 探测/正常 HTTP 错误可能记录完整 URL，SQLite/feedback 日志不受 RUST_LOG=off 全面约束。原生没有 url_env_var，也未发现可解决这些问题的总关闭开关。不得把秘密URL放CLI参数、TOML、模型上下文、日志、SQLCipher、bbolt或版本库；不新建MCP代理藏key，不改Runtime补丁。

环境变量方案也必须验证秘密不传给模型命令：固定Runtime默认shell环境继承不能保证KEY/TOKEN排除，应利用原生shell_environment_policy.exclude显式排除相关变量并覆盖实际执行环境。任何config/session/debug/error/OAuth/日志出口未证安全时，阻塞激活；前期元数据诊断未保存密钥且秘密扫描无命中；本次产品原生配置、真实Prompt和不向模型执行环境继承秘密的定向检查见16–20。未执行通用故障/攻击测试。首期凭据仅存内存；canonical隐藏输入已实现并由用户在相应正常构建后亲自输入，具体路径见16。复用受管sidecar/Runtime环境，不新增持久秘密存储，重开重新输入。原生exclude之后仍会应用set，必须核对无重新注入；详见13。

只允许固定HTTPS Sorftime服务，非任意URL输入；不把query秘密转发其它origin。秘密是MCP传输凭据，不作为工具参数、卖家平台OAuth或模型输入；本地之外的发布仍须独立安全审查。

MCP调用采用Codex原生Prompt审批语义；不能把readOnlyHint/工具名/prompt当授权。实施前 Host 的 FEAT-152 只接 Command/FileChange/Permissions；本次仅新增下述有界原生MCP请求薄适配。本次已明确最小**原生审批请求薄适配设计**：复用默认稳定 mcpServer/elicitation/request 的 Sorftime 空表单确认，按真实 request ID/threadId/可信非空 turnId 显示线程请求面板；原生没有 itemId/结构化 toolName，不能猜 Tool 卡关联。accept/decline/cancel 和 serverRequest/resolved 沿用原生，回调不持久化。一般表单/URL/认证/requestUserInput 不在本期支持，继续拒绝；不启用实验功能。产品薄适配已实施，真实批准与拒绝通过；20所记配置冲突已按21修复，实际连接后的正常停用/切换已按22通过。不得设置Approve、降低模式或复活FEAT-137来跑通；FEAT-152三档权限的既有语义不变。

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。详见13。

## 显示、保存与错误

卡片复用Timeline/Item shell，显示经核实的安全服务/工具身份、参数摘要、结果摘要、原生status及适用duration。保留0、null、合法空结果。result、error、availability分开；原生failed可映射固定安全文案，但不泄漏原始错误或根据结果正文改变status。

实时started/completed、已保存观察、thread/read历史分别标来源。历史读取不冒称亲历started/completed；没有可信活跃Turn/订阅时不忙碌。Turn结束不封口Tool；完整Item直接替换，接受更短/不同/合法空结果，不正文对账。

结果直接复用原生content中type=text且text为string的块，保留原始索引，最多32个原始content条目、合计既有256KiB UTF-8上限；经过既有完整文本脱敏和容量处理后纯文本展示。不解析未知JSON、中文键值或正文猜业务字段/价格单位/成功，也不激活链接或资源。没有可展示文本时只说明该事实，不能推定没有商品数据；真实空结果且原生completed仍保持completed。outputSchema缺失不阻止此展示设计，细节见13。模型最终摘要单独验收，必须与实际安全返回一致并保留缺失，不仅凭item/completed判用户目标完成。

继续使用FEAT-132的唯一NativeDisplayBuffer、SQLCipher原生facts/views与thread/read/resume。改造前旧NativeItem reader带deny_unknown_fields，新字段可能令整批历史报DatabaseUnavailable；本次已**先固定兼容reader基线，再允许新producer写入**，不能假定8bfa5ca旧Desktop自动unknown。私有facts/views已采用显式格式版本及schema15前向expand migration；单条不支持格式通过本地recordDiagnostics隔离，不进入NativeDisplayBuffer或触发冷读补建。高于支持范围的数据库user_version仍整体拒绝，旧JSON不改写，回滚仅到已验证兼容reader；未验证则停止新写入，不删除事实或改旧migration。

## 验收、费用与当前状态

首期公开US ASIN B07H9PZDQW已真实返回数据；原生/data三字段与模型回答一致，见20。用户已取消业务失败场景的实现/验证，不新增业务错误字段扩展、分类器、失败专用流程或失败触发样本；已有原生failed及通用安全处理仍如实保留，不造成功。

当前累计业务2逻辑调用保守扣4/10尝试，元数据14/20，文本9/13，图片0；不同台账不转用。原生正常拒绝未进入业务调用，精确历史HTTP次数仍未知。

本期按breaking保守治理安全Tool字段、权限请求和持久兼容；具体公共wire/私有IPC版本先在Contracts确定，不原地扩旧闭合schema，不机械沿用view_image的v8提议。顺序为源契约 → Host/Desktop兼容reader → MCP配置/原生审批与安全投影 → 唯一显示/保存 → 真实验证；来源受影响才更新真实commit/digest/pin。Codex不改，门禁不放宽。

当前9项活动Must均PASS，AC-007已完成最终来源原生拒绝复验，AC-004为OWNER_EXCLUDED / NOT RUN，编号不复用。原D0 BLOCKED历史保留；当前根据用户范围决策重新审定且D0实跑PASS，不要求先编码或完成D4。通用D4中既有输入/权限拒绝回归保留，不能当成被排除的业务失败验证；真实成功和剩余AC的分次证据、来源及最终检查见02和24。

## 不依赖连接的前期设计（历史，2026-09-10）

用户已确认继续本需求中不依赖连接的工作。已把原生字段复用、新的MCP安全显示扩展、NativeTool只读适配、版本化wire、先行兼容reader及普通定向验证明确写入[12](12-independent-contract-and-reader-plan-2026-09-10.md)。现有durationMs/availability等直接复用；原生failed即使error=null也不能改完成。旧闭合reader不能靠删除deny_unknown_fields兼容。为提供真实旧binary拒绝机制，当时将database_change调整为expand：新的前向格式版本标记migration已按16及用户授权实现并在现有数据正常落至schema15；不改历史0014、不复制数据库。本段前期设计及旧诊断不等于AC通过。


## 当前交付边界

当前本地D4保持PASS，九项活动Must满足、AC-004始终用户排除。获本次明确授权后，22个提交已按Contracts→Host→Desktop→元仓普通推送，逐仓远端SHA一致；CI均未触发，NOT RUN。累计文本9/13、元数据14/20、业务2逻辑调用保守扣4/10、图片0，本次新增0。实际来源与远端结果见[26](26-remote-delivery-2026-09-11.md)；本次新增结果记录仅本地提交，不超出22个提交追加推送。

23保留旧不确定记录并修复启动阻塞；24为分次本地验收，25为推送前范围，26为实际远端交付结果，各阶段来源不混淆。
