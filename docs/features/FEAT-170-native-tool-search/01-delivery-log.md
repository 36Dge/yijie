# FEAT-170 — 整体实施方案与本轮记录

> 桌面续验更新：同一条真实桌面聊天的完整链路已通过；模型累计9/12次，另获批并完成1次只读联网检索。当前结果见[05桌面验收](05-desktop-chat-e2e.md)。以下费用、GUI未执行等内容保留其先前记录时点语义；其它未完成场景不执行，整体D4保持未通过。

> 当前状态（2026-11-08）：用户后续已授权复审后执行及仅 Kimi 最多 12 次验收。实现与本机启用已完成，实际调用 5 次；完整 D4 尚未通过。当前事实见 [实施记录](03-reaudit-and-implementation.md)、[交付与验证](04-delivery-and-verification.md) 及 feature.yaml。以下保留**方案阶段历史**，“本轮”“仅方案”和 NOT RUN 等描述均指最初规划时点。

> 2026-11-08：仅规划。下列“拟实施”不表示已创建补丁、生成契约、运行测试或授权启用。

## 1. 真实复用链与拟改动

用户意图 → 原生 model-visible tool plan → 同名 tool_search 的 function 适配 → 原生 SearchToolCallParams → 同一 ToolSearchHandler/缓存/BM25 → 原生结果/Code Mode 描述转换 → function_call_output → 已有 exec/ToolRegistry → McpHandler → 原有 Market Gateway/逐次审批 → 工具结果/模型答复。

原生缓存只缓存当前 search_infos 索引，不授执行资格。工具执行继续以当前路由、绑定和权限为准。本期不建立 Host 搜索缓存、调用重试器、自动恢复队列或“已加载工具”数据库。

| 仓库 | 拟修改模块 | 最小边界与前提 |
|---|---|---|
| yijie-codex | 新增顺序补丁，protocol/openai_models、tools/handlers/tool_search、spec_plan、必要输出薄适配及测试 | 原生参数/schema/handler/排序/缓存/执行委托；默认原生路径不变，函数路径仅显式能力启用 |
| yijie-codex | canonical prepare/build/manifest 及 UPSTREAM/CHANGELOG/候选说明 | 保留全部现有补丁和制品；不得覆盖原二进制；独立可复现候选 |
| yijie-contracts | 拟 runtime-tool-search/profile、source.lock、生成/检查/注册及源说明 | 只维护 Runtime 配置投影；公开聊天/审批/问答 API 保持。Runtime schema 未生成前不手写实现 DTO |
| yijie-agent-host | native_tools/kimi目录装配、普通线程config覆盖、Config/环境解析、baseline配对、受管目录升级、相关测试 | 普通聊天目录Kimi单项新能力，进程默认/辅助目录与MiniMax旧值保持；搜索执行不进入Host；保留当前六组工具、问答及上下文能力 |
| yijie-desktop | run-local-demo-fast、sidecar、候选来源冻结/校验 | 原client:dev入口装配；不增加新Home、SQL迁移、capability、IPC或工具搜索页 |
| yijie-connectors | 现有Gateway/generic元数据与scope相关定向验证 | 默认不改产品逻辑；仅实证元数据缺失才修适配；名称和参数权限绑定保持 |
| yijie-skills / infra / API / admin / knowledge / coze | 无产品改动计划 | 仅确认边界和必要既有入口，不把本需求扩成新平台建设 |

这些路径均为实施定位，不在本轮修改。实施前读取最新工作树，尤其 FEAT-169 和上下文浮层相关变更；不得用今天的 HEAD 或候选锁覆盖后来已完成工作。

## 2. 技术依赖顺序

本 Profile 不建立治理切片；以下为一个完整交付的依赖顺序。

1. **基线复核与授权**：Owner审阅本包并明确允许实施；重新核对原生/模型官方协议、六组已集成工具、旁路线程、当前模型配置及运行中的App。Native文件写入前先正常退出开发App。
2. **原生适配**：在隔离编辑材料上形成最小补丁；同名function参数由原生声明生成，输入/输出分支放在同一ToolSearchHandler，解析委托SearchToolCallParams，检索调用同一个search方法；输出用原生typed LoadableToolSpec→ToolSpec/CodeMode描述→JSON函数输出，避免反解析字符串；原生缓存比较键包含transport。暴露限定DirectModelOnly语义，保留原生native分支。
3. **保护边界**：把适配纳入原有input-only空注册表、V2实际父线程MCP继承、direct-only/excluded/hidden规则；保留外部上下文记忆标记、错误配对、取消、原诊断脱敏。
4. **构建与源契约**：canonical独立构建，生成config/model/app-server schema并比较。再建Contracts本地候选投影、来源摘要和生成物，执行适用定向lint/conformance/breaking。新公共wire N/A；若实际发现需要新的事件或跨仓payload则先修改相应权威源，不能先写handler。
5. **Host与入口**：新普通聊天目录复用既有受管目录配方并精确核验；默认目录不开搜索，普通根线程通过既有config.model_catalog_json覆盖选择；Kimi新路径只接受新Runtime，旧模型路径不带新能力。复用已存在的本机鉴权、进程、callback和Gate，不为搜索建立新RPC。
6. **定向验证**：实施02中的普通原生回环、真实Gateway普通合成工具、批准/拒绝、取消、恢复、元数据检索样本。只运行实际受影响筛选；旧攻击/强杀/权限破坏/可执行文件替换测试永久排除。
7. **真实资格与本机启用**：候选可审阅后再申请本包明确Kimi HTTP额度及必要第三方只读范围。先取得完整实际“搜索→exec→批准→调用”证据；然后正常退出并从原client:dev/易界.app启用精确候选，核验旧会话和最终结果。无结果不冒充D4。
8. **独立复审**：实现完成后另做结构化审查，检查本文AC、原生复用、协议、权限、旧历史/回退和未运行项，Owner最终验收。代码提交/推送/签名/发布另行授权。

## 3. 不变量与容易遗漏的情况

- function声明、传入参数、返回item必须成对；错误/取消也沿原call_id，不把function_call配tool_search_output。
- 不能直接调用现有function_input::wrap来处理ToolSearch：该函数只包装Freeform。
- 原生缓存原先只有search_infos维度；新增模式若影响缓存handler的spec/输出，必须同缓存追加transport键，验证来回切换而非仅同模型重复命中。
- ModelInfo已有JsonSchema派生；新增模型能力必须纳入canonical模型schema生成，不能仅用不含ModelInfo的config.schema验证其值。
- 不能因为tools数组少了就认定上下文变小；exec描述也不能包含全部延迟schema。
- 搜索结果定义是metadata，不是调用凭据；历史结果、窗口恢复或工具名相同不能解除新一轮scope检查。
- native专用ToolSearch不属于CodeMode nested tool；函数适配不能意外增加tools.tool_search嵌套或改变direct-only隔离。
- CodeMode名字必须用现有code_mode_name_for_tool_name/定义转换；不要在Host以字符串拼接重新实现命名映射。
- 结果使用原生外部上下文标记；虽然当前自动记忆关闭，也不能把这当成可删除原标记的理由。
- 不满足exec资格的Deferred工具须保持原直接可见或拒绝不一致配置；不能默默隐藏现有可用工具。
- 原生BM25 cache重建按元数据集合；scope撤销后的执行拒绝由原Gateway保证，不能用“搜索缓存没过期”放行。
- 进程默认目录仍关闭搜索；普通根线程用原生config.model_catalog_json覆盖，新目录不放进全局CLI替换。已加载thread/resume可能忽略覆盖，必须冷启动/正常重开及实际声明验证。
- 标题线程、受限草案、Guardian/审核辅助线程不借全局模型能力扩大工具面；缺少证明保持新功能不可达。
- 旧native历史含专用ToolSearch item时不能直接发送给不支持该wire的模型；不删除历史以绕过失败。
- 关闭搜索与回退整个Runtime分开；前向兼容构建关能力是首选，旧binary读回资格未证明就不降级。

## 4. 本轮实际操作

| 操作 | 实际范围 | 结果 |
|---|---|---|
| 治理上下文 | AGENTS、Handbook、Contract First、ADR、项目记忆及FEAT-169 | 只读；确认demo_fast/local四件套和本轮仅方案 |
| 仓库与源码 | 十二仓Git元数据；核心五仓及相关外围入口源码/测试 | 只读；证据与范围列于source-audit.json，不代表全仓运行审计 |
| 官方协议 | Kimi/MiniMax公开Responses文档 | 普通GET；Kimi明确未支持native tool_search类型，新证据已纠正旧建议 |
| 方案写入 | 仅新建FEAT-170-native-tool-search目录 | 四份治理文档与本包引用证据；未修改其它需求或产品代码 |
| 文档检查 | 02中记录的本包结构/链接/声明检查 | 结果以实际输出为准，不运行产品测试 |

## 5. 授权与实际调用

| 类别 | 已授权 | 上限 | 实际 | 边界 |
|---|---|---:|---:|---|
| 本轮源码只读审计与方案落盘 | 是，本轮用户请求 | 本包 | 已进行 | 不改变产品行为 |
| Runtime/Host/Desktop/Contracts实现 | 否，用户明确不执行 | 0 | 0 | 等明确实施指令 |
| 付费模型HTTP | 否 | 0 | 0 | 不借FEAT-169额度；未来建议仅Kimi，另批 |
| 第三方metadata/业务调用 | 否 | 0 | 0 | 未读取凭据、未连接账户 |
| 本机激活/重启/容器生命周期 | 否 | 0 | 0 | 只写未来启用步骤 |
| Git提交/推送/发布 | 否 | 0 | 0 | 保留原有dirty工作树 |

## 6. 评审记录

- 推荐方案：B（原生搜索委托、function wire、现有exec执行）。
- 文档准备者：Codex；不称为独立人工批准。
- Owner方案确认：pending。
- 实施许可：未授予；本轮限制优先于治理脚本“Next”输出。
- D4：NOT RUN；当前未启用tool_search。
- 审查与检查记录见02；发现源漂移时只更新本包事实，不回滚或修复主线程代码。
