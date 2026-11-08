# FEAT-170 — 验证方案与本轮文档检查

> 桌面续验更新：同一条真实桌面聊天的完整链路已通过；模型累计9/12次，另获批并完成1次只读联网检索。当前结果见[05桌面验收](05-desktop-chat-e2e.md)。以下费用、GUI未执行等内容保留其先前记录时点语义；其它未完成场景不执行，整体D4保持未通过。

> 当前状态（2026-11-08）：用户后续已授权复审后执行及仅 Kimi 最多 12 次验收。实现与本机启用已完成，实际调用 5 次；完整 D4 尚未通过。当前事实见 [实施记录](03-reaudit-and-implementation.md)、[交付与验证](04-delivery-and-verification.md) 及 feature.yaml。以下保留**方案阶段历史**，“本轮”“仅方案”和 NOT RUN 等描述均指最初规划时点。

> 仅方案。测试名称、步骤和期望均为未来验收设计；本轮没有运行Runtime、Host、Desktop、Connector或模型验收。

## 1. 用例与 Must AC

| 用例 | 验证方式/普通场景 | 通过判据 | AC | 当前结果 |
|---|---|---|---|---|
| T01 | Runtime适配/来源单元与schema投影 | 同一原生handler/BM25；参数schema同源；默认native不变；精确候选匹配 | 001/007 | NOT RUN |
| T02 | 真实Runtime+普通loopback：无目录、非空目录、正常无命中、目录正常更新 | 无目录不声明；空结果为空；原生cache随新集合更新，且native/function模式切换不复用错误handler；不引入第二索引 | 001/003 | NOT RUN |
| T03 | 提供方请求/响应shape定向测试 | function声明与function_call/output配对；Kimi出站无专用tool_search item；query/limit沿原生类型 | 002 | NOT RUN |
| T04 | 实际CodeMode+普通MCP合成只读工具 | 搜索命中后exec使用原生规范化名称成功；工具schema未再注入tools数组；原结果正常返回 | 002 | NOT RUN |
| T05 | 普通参数/空结果边界 | 空query、limit=0按原生报错；默认limit=8；无匹配不自动授权/安装/执行业务 | 003 | NOT RUN |
| T06 | 固定目录24项与6条中文、6条英文任务 | 12/12约定目标均在默认8条结果中；只以普通词/描述/参数验证；记录遗漏不换算法掩盖；输出JSON完整 | 003/009 | NOT RUN |
| T07 | 同真实Host/Gateway：正常选择、审批批准/拒绝、正常撤销 | 搜索HTTP业务调用0；批准后目标只调用1次；拒绝/撤销后业务0；正确工具/参数/turn绑定 | 004 | NOT RUN |
| T08 | 普通合法双会话、V2子任务与不同执行面 | 各选集不混；普通聊天新目录和标题等默认目录隔离；子任务保持不继承主会话MCP且不获得新兼容搜索；input-only空工具；direct-only/excluded保持；不构造攻击fixture | 004/006 | NOT RUN |
| T09 | 正常turn/interrupt、重复只读搜索、并行不同查询、用户显式后续轮 | 取消真实收束、无业务重放、调用/结果ID各自对应；不以杀进程制造断线 | 005 | NOT RUN |
| T10 | 旧普通会话resume、新路径冷重开、Kimi/MiniMax模型切换、原生compact/new_context | 原历史可读；新轮按当前模型/选集建路由；核对冷恢复配置和已加载resume忽略覆盖的真实行为；无隐藏已加载状态；旧结果不授执行资格 | 005 | NOT RUN |
| T11 | 原六组相关定向回归及记忆标记 | V2/apply_patch/exec/wait/memories/问答/上下文行为保持；普通摘要策略不变；外部上下文保护未丢失 | 006 | NOT RUN |
| T12 | 获批后的真实Kimi+正常客户端原入口 | 同一候选完成真实“搜索→exec→审批→工具结果→回答”，另有无命中或正常拒绝恢复证据 | 002/008 | NOT RUN |
| T13 | 来源生成/同步检查、原入口正常退出重开、前向构建关闭搜索、普通历史读回 | 新候选精确配对；旧路径仍可使用；六组保持；不降库、不删历史、不用新Home掩盖旧数据 | 007/008 | NOT RUN |
| T14 | 相同24工具目录比较开/关请求材料与普通大目录观察 | 开启后初始tools和exec说明均不含完整延迟schema；只回传命中集合；本机24工具热查询10次p95≤100ms（排除模型/IO）；记录实际耗时与字节，不编造token降幅 | 009 | NOT RUN |

12条检索小样本的词表与目标工具须在实施前固定于普通fixture，包含同服务相似工具、不同服务同义用途、中文标题、英文原名、参数词及无结果对照。不以真实商家材料或秘密填充。24工具规模用于核心证明，接近现有上限的目录只作观测，不以未经测量的极限性能承诺阻断Demo。

上游可复用测试定位：`core/tests/suite/search_tool.rs` 的 `tool_search_returns_deferred_tools_without_follow_up_tool_injection`、`tool_search_indexes_only_enabled_non_app_mcp_tools`、`tool_search_matches_mcp_tools_by_distinct_name_description_and_schema_terms`；`core/tests/suite/code_mode.rs` 的 `code_mode_only_guides_all_tools_search_and_calls_deferred_app_tools`。已有测试不能直接证明新增适配通过，执行前检查其完整fixture与清理过程，含用户禁止行为的用例不执行。

本轮AC-001至AC-009全部pending，表中没有任何产品PASS。结构化的方案检查不能折算真实供应商资格。

## 2. 真实验收设计与费用

推荐在实现与安全本地回环完成后，单独申请**最多12次Kimi短模型HTTP请求**，作为可审阅建议而非当前额度：

- 成功链预算4次：搜索、exec调用、必要续行/最终答复；
- 无命中或拒绝后恢复预算3次；
- 历史恢复/启用入口预算3次；
- 诊断修复复验预留2次。

以实际模型HTTP计数，包含子调用、续行和任何压缩请求；禁止超过授权后自动补额度。MiniMax、图片视频、外部商家写操作均为0。原生BM25本身无专用模型调用，整轮仍有推理成本。

本轮付费调用授权0、实际0，第三方metadata/业务授权0、实际0。未来若使用真实连接器做只读验收，需把具体服务、操作、普通数据范围和次数另外列入授权；不能将Kimi预算当第三方调用许可。真实Runtime+合成MCP证明本地协议，真实Kimi证明提供方，完整原入口操作证明产品链；未执行层级不得互相替代。

## 3. 安全排除与验证方式

- 不实施攻击注入、恶意归档、权限/属主破坏、二进制伪装/替换、强杀/故障注入退出。
- 正常参数校验、合法多会话、正常用户拒绝/取消/撤销、stdin EOF及原生中断均可用于后续定向验证。
- 每个拟运行测试先核对真实范围与安全排除清单；不机械执行上游/跨仓全量套件。
- 历史测试若依赖禁止行为，记录“未执行：用户长期安全条款禁止；影响：该故障方式未做动态验证”，采用源码审查和普通状态收束证据，不写PASS。
- 不为本轮文档验证启动应用、停止主任务、切换Runtime或重建容器。

## 4. 本轮文档检查

结果保存在 [plan-checks.json](references/plan-checks.json)。检查仅作用于本包的结构、链接、状态及源码引用，不产生产品运行证据。

| 检查 | 命令/范围 | 结果 |
|---|---|---|
| 标准模板 | new-feature.sh FEAT-170 native-tool-search docs/features | 已创建四件套；未进入脚本提示的实施步骤 |
| 严格结构与D0文档完整性 | check-feature-package.sh --strict --gate D0 本包 | 以plan-checks.json实际结果为准；非Owner批准 |
| 声明一致性 | validate-feature-package.mjs --audit-claims 本包 | 以plan-checks.json实际结果为准 |
| 本地链接、身份、待实施状态 | 只读检查四份文档和引用证据 | 以plan-checks.json实际结果为准 |
| 修改范围 | 本包文件/行尾检查，跨仓Git状态复核 | 仅本包文档写入；其它dirty为已有/并行任务，不操作 |
| Runtime/Go/Rust/Vue/模型测试 | 未调用 | NOT RUN，本轮仅方案 |

## 5. 方案自审结论

- 三个旧粗略结论已细化：旧feature键无效；Kimi官方类型范围排除原样native wire；CodeMode可复用延迟执行能力，因此不需要Host装载器。
- 输出适配同时覆盖call_id、错误/取消、缓存transport维度、canonical模型schema、direct-only、CodeMode名称和外部上下文记忆标记，避免只改工具声明。
- 当前目录范围以已选连接器和有效lease为准；不把“安装”“连接”“搜索命中”当“执行授权”。
- 主线程最新六组工具、上下文浮层和其它dirty未被本包修改。源码引用是查阅时快照，实施前需重验。
- MiniMax未资格化、中文召回、原生function→exec真实模型效果仍列Unknown和验收，不冒充已解决。
- 没有新持久库/新UI/新审批/第二索引；无提交、发布或默认开关变更。
- 方案Owner确认pending，实施pending，所有Must AC pending，D4 NOT RUN，DP不适用。

## 6. 方案阶段交付结论（历史）

**完成的是方案与源码依据，产品接入、测试和启用均未执行。** 后续须先获得明确实施指令，真实验收额度及本机启用按实际可审阅候选另行记录。
