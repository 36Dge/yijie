# FEAT-144 当前审计与Sorftime接入决策

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。


> 恢复后的最新结论：3/5次原生发现，第3次初始化HTTP400，未取schema；已正常退出，剩余2次不自动追加。见[08](08-discovery-results-2026-09-10.md)。下文保留该阶段历史范围。
> 后续更新：官方已确认无query的Authorization Bearer支持，用户已授权5次测试；最新原生发现方案、计数口径及未执行状态见[06](06-header-auth-and-discovery-budget-2026-09-10.md)。本文保留此前核验结论与证据范围。
2026-09-10，初始需求审计。安全/审批前置结论以随后 [D0 核验](05-d0-preflight-2026-09-10.md) 为准：query-only 发现已有明确日志阻塞，稳定 elicitation 与兼容方案设计已明确，未实施。用户最新提供真实sorftime streamableHttp配置，覆盖此前无真实producer时的内置工具备选；密钥从未写入本需求包。本记录是当前权威，原MCP包和未实施内置备选分别保留在history。

## 完整审计信息必须保留

原FEAT-144从FEAT-136拆出CAP-017/GS-004，目标为真实MCP接入、开始/进度/结果/失败、安全展示、唯一记录与正常重开；8AC全pending、D0 BLOCKED、实现/D4 NOT RUN、额度0。此前缺少工具、价值/入口、producer所属、参数/数据/访问/副作用、成功失败和预算决策。通用卡片或合成schema不能证明真实产品Tool。

用户委托模型定稿并强调所有可复用Codex机制必须复用、只落需求。模型先选view_image为无外部服务备选，尚未实施；用户随后给Sorftime配置，故本期转回真实MCP单商品查询。CAP-017/GS-004为本期未完成目标，不再延期给内置样板，不用ImageView/Command/图片生成替代。

## 当前固定来源和并发

元仓6f12939aa85f8a9c1f55e89f1018c60501a2f494；Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3；Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b；Desktop8bfa5ca284fddb86d7cdd2a406c5041c49367688；Codex6c1ad767f0997845b8258a1c452fd4eb7577579f。五仓分支chore/retirement-baseline-20260905。native Contracts pin6f632f155eacdaf93df0e0b00b5dab9e369c5442、权限Host pin f4cf01bd6f7e9f37792ef743d44f0ce10527c10b，均不改。

冻结Runtime build b2b20e2fc4a0c94834f34d8cc459e488a1b56277 /0.144.6 /experimental_api=false；到当前HEAD的codex-rs子树零差异，不重建、不启用历史137patch。Desktop初始10个并发路径及其后自然变化见evidence/requirements-audit-2026-09-10.json，本轮仅写元仓，不覆盖其内容。原MCP四文件与元仓基线逐字相等。

## 事实与源码

路径相对CrossBSD，行号供定位，实际以固定来源为准。

| 事实 | 源码/依据 | 约束 |
|---|---|---|
| 原生McpToolCall有id/server/tool/status/arguments/result/error/duration | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs:301；core/src/mcp_tool_call.rs:876 | Codex是身份与执行事实权威 |
| Host native MCP仅通用标签/参数隐藏/结果接收、恒partial，未投Tool错误/耗时 | yijie-agent-host/internal/session/native_conversation.go:168 | 本期补安全适配，不造执行器 |
| Desktop伪填旧DTO来源、unknown身份、空progress/error，卡片历史busy有落差 | yijie-desktop/src/domain/conversation-view.ts:375；ChatToolItem.vue:38 | 原生专用只读模型，保留真实来源/缺失 |
| 通用Tool测试是手工execution，非真实producer证据 | yijie-desktop/src/components/chat/ChatToolItem.test.ts:46 | 新真实D4不能继承旧测试结论 |
| MCP progress有协议，无已证实app-server发送点；native未接 | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/mcp.rs:214；rmcp-client/src/logging_client_handler.rs:61；Host native_conversation.go:318 | 0进度合法，不轮询/补步骤 |
| Legacy保存McpToolCallEnd，原生builder恢复MCP | yijie-codex/codex-rs/rollout/src/policy.rs:102；app-server-protocol/src/protocol/thread_history.rs:787 | 使用thread/read/resume，不套Command/ImageView冷历史结论 |
| 唯一缓冲/完整替换/SQLCipher保存已具备 | yijie-desktop/src-tauri/src/chat/native_conversation.rs:132；native_conversation_storage.rs:82；application.rs:2218 | 必须复用，不重建 |
| NativeItem deny_unknown_fields，单个view反序列化失败导致DatabaseUnavailable | yijie-desktop/src-tauri/src/chat/native_conversation_generated.rs:2；native_conversation_storage.rs:33、55的native_views | 兼容reader先于新字段写入，旧8bfa不是已证明回滚基线 |
| Connectors最小HTTP骨架；Skill MCP示例占位 | yijie-connectors/internal/app/app.go:30；yijie-skills/plugins/amazon-listing-optimizer/mcp/servers.toml:1 | 不据此新建Sorftime代理/SDK；外部服务是现成producer |
| 原生HTTP MCP配置url、bearer_token_env_var、env_http_headers；无url_env_var | yijie-codex/codex-rs/config/src/mcp_types.rs:378、448 | 不假造环境插值字段，不擅改query鉴权 |
| thread/start.config支持内存override | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/thread.rs:94；app-server/src/config_manager.rs:233；Host session_protocol.go:509 | 可作受控适配入口，但秘密全链路安全尚未证明 |
| enabled_tools/disabled_tools为原生过滤 | yijie-codex/codex-rs/codex-mcp/src/tools.rs:81 | 只启用核实后的单详情工具，不放开全部 |
| 原生超时配置startup_timeout_sec/tool_timeout_sec | yijie-codex/codex-rs/config/src/mcp_types.rs:184 | 候选启动30秒/调用60秒，用已有配置，不写新超时器 |
| 原生MCP审批requestUserInput/elicitation，Host仅接Command/FileChange/Permissions | yijie-codex/codex-rs/core/src/mcp_tool_call.rs:1321、1363；Host runtime_permissions.go:181、session_protocol.go:292 | 必须先补薄请求/响应适配，未支持保持拒绝，不能设Approve绕过 |
| 初始化/发现有原生瞬态重试，tools/call遇session404可恢复重发一次 | yijie-codex/codex-rs/rmcp-client/src/streamable_http_retry.rs:23；rmcp_client.rs:940 | 不声称MCP零重试，费用/幂等据此规划 |
| 默认shell环境可能继承秘密变量 | yijie-codex/codex-rs/config/src/types.rs:943；Host runtime.go:928 | 原生exclude显式排除秘密，不把KEY/TOKEN命名当安全保证 |

## 服务资料与选型依据

用户事实：服务名sorftime，传输标签streamableHttp，无秘密origin为https://mcp.sorftime.com；用户提供query-key凭据。这里只记录引用，不保存密钥、完整秘密URL或密钥哈希。本轮未initialize、tools/list、tools/call。

公开资料于2026-09-10只读查阅：

- [Sorftime官方MCP介绍](https://www.sorftime.com/en-US/mcp)：说明产品查询能力和streamableHttp接入；页面搜索索引可读，直接打开曾超时，不据此声称服务不通。
- [工具维护者发布的矩阵](https://github.com/DannylydST/sorftime-seller-agent/blob/main/references/tool-matrix.md)：列出product_detail及其它工具；仅用于候选选择，不是本账户实时manifest或授权证明。

首选单ASIN详情，因输入范围小、无批量/写入意图、结果易核对。product_search/评论/趋势链增加调用和结果量，get_time只能证明连通，均不作为本期业务成功替代。精确工具名、大小写、参数键/约束、输出结构、只读注解和费用必须以服务实际发现及正式说明确认；不安装该公开仓库的bridge，不照抄其自动注册/调用指令。

## 安全配置与权限决策

1. 原生MCP由Codex连接和执行；Host只负责既有配置/秘密/权限边界的必要适配，Desktop只展示。Sorftime传输凭据与商家平台OAuth/卖家token分开，不让模型或shell获取。
2. 优先取得 Sorftime 正式 Authorization header 方式，再审计无 query 的原生内存 mcp_servers.sorftime.http_headers.Authorization；不假设任意 header 会跳过 OAuth 探测。环境变量只作为另行证明隔离后的备选。当前 query-key 不能猜测转换；没有原生 url_env_var。
3. 初审曾提出 query-only 候选为秘密存储→Host内存→原生thread/start/resume.config→受保护stdio；D0 已证明该候选存在原生日志阻塞，当前不可激活，见05。不能落CLI/TOML/SQLCipher/bbolt/日志，不能创建MCP代理或改Runtime。已有部分HTTP日志去query/错误去URL只证明局部，必须审核config/read、会话保存、调试、OAuth、错误和所有日志出口；未证安全则保持激活阻塞。
4. 环境变量路线用原生shell_environment_policy.exclude明确排除秘密，并验证所有模型可用执行环境；不改用户个人Codex全局配置，不把秘密放普通环境文件。具体安全存储/注入适配需实施前固定，不假称现有Sorftime入口已实现。
5. 精确原生enabled_tools白名单，只选被核实详情工具；按原生Prompt审批。readOnlyHint只作风险信息，不当授权；未知工具/请求类型拒绝。本期选默认稳定 elicitation 空表单，排除实验 requestUserInput/URL/一般表单；薄适配须保留 request ID/thread/可信 turn、原生动作和撤销/失效，不猜 Tool Item 关联，不新增审批裁决器、超时推演或永久授权。
6. FEAT-152现有三模式语义不变，FEAT-137永久退役；新增支持MCP请求类型属于本期权限适配影响，不能错误填写auth_permission_change=none。不放宽为Approve/完全访问来通过验收。
7. Sorftime只接收被核实schema内的US/ASIN参数，不发送项目文件、用户正文历史、账户/订单/买家PII。服务结果是不可信数据，不能当系统指令或权限授予；不跟随其中URL执行额外工具。

## Contract First、保存兼容与清理

本轮文档实际contract-impact=none；未来功能按breaking保守治理：新增安全MCP身份/结果/错误、原生审批面及持久字段不能原地扩闭合schema。具体版本/路由依据当前MCP所需字段重新定，旧view_image的v8候选不自动继承。

先Contracts冻结原生安全字段/版本和旧消费者行为，再Host/Desktop形成并固定兼容reader，之后才激活新MCP投影和写入。旧v7/旧history在保留兼容窗内维持原语义；旧端不能读新字段时明确版本拒绝并保留旧历史，不让一条新Tool使整批历史失败。不改历史migration、不删新事实“回滚”；若必须新增DB变更，先重新判定并记录，默认无新表/新保存器。

唯一NativeDisplayBuffer完整对象替换、原生身份、入口去重、SQLCipher和thread/read/resume强制复用；所有MCP结果字段来自原生完整Item或经过明确schema的安全投影。移除当前native→旧DTO的虚构开始来源/unknown丢标签/error空值等不忠实逻辑；不复制第二份状态机或对账器。旧v4/v5真实DTO/IPC/表/reader/资源helper保留其兼容职责。

UI状态分为原生执行结果、内容availability和当前busy；thread/read历史仅表达读取结果，不冒称观察过生命周期。unknown、容量、脱敏或保存失败不改Runtime terminal。真实failed无安全具体原因时只显示固定错误文案，空数据/completed不能压成failed。阶段/进度缺失不造步骤。

## 前置条件与D0状态

P144-01：受权发现确认实际product_detail或等价单详情工具、输入/输出schema、只读幂等、费用和普通错误；当前NOT RUN。
P144-02：当前 BLOCKED。D0 深查发现 query URL 可经 OAuth 探测/正常错误进入独立持久日志；不能用 RUST_LOG=off 或仅内存 override 判安全。优先取得服务正式 Authorization 支持说明，再审计无 query 的原生 header 路径。
P144-03：DESIGN COMPLETE / implementation NOT RUN。选默认稳定 MCP elicitation 空表单确认，按原生 request/thread/turn 关联，不猜 Tool Item；Contracts→兼容 reader→新 producer，完整设计见05。未编码本身不阻断 D0。
P144-04：授权边界 DESIGN COMPLETE，当前授权/调用仍0。元数据发现另批，模型/业务费用和实施在后续阶段批准；未来额度尚未批准不是 D0 失败理由。

服务来源和首期业务推荐已经明确，P144-01/02 的安全、真实 schema/费用/普通失败依据仍阻断规划；不要求先实现产品来解除 P144-03。本轮D0保持BLOCKED，不通过字段改绿掩盖。需求可以完整落盘，后续先安全核验这些条件再进入适用实现/验收；不要求本轮连接服务。

## 预算与失败

建议最多10次模型Responses，最多3个逻辑业务调用；每次保守预扣2个tools/call尝试，预留总6次，包含原生404恢复。元数据initialize/tools/list有自身重试，计费与可观测性先确认再单独授权，不宣称免费/零重试/已建计量器。无法证明累计不超预算就不启动真实验证。

正常失败只使用服务正式说明、符合实际inputSchema的普通业务无效条件，不使用攻击、坏key、断网、禁权限或额度耗尽。空数据若原生completed则作为独立empty验收，不冒称failed；没有安全自然失败样本时保留Must未通过。完整MCP D4不由Command或模型口述代替。

## 分离审查的通用修正

原生completed与业务可用结果分别验收；实时/保存观察/thread-read来源分开；兼容reader先于新字段写入；配置不等于注册成功；0progress合法；唯一原生机制强制复用。原内置备选的专属限制留历史，不混入当前MCP AC。最终本轮文档审查和门禁见02-verification.md。
