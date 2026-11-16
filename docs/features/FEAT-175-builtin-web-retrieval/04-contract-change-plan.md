# FEAT-175 契约与迁移计划

修订3补充：三个前置的具体实现、依赖和验收见 [15](15-identity-model-readiness.md)、[16](16-expert-policy-implementation.md)、[17](17-native-cancellation-routing-qualification.md)，完整复审见 [18](18-revision-3-full-review.md)。本文件的旧概括按这些细则解释；实际实施／资格仍NOT RUN。

## 权威源

| 边界 | 权威与拟变化 | Producer → Consumer |
| --- | --- | --- |
| Codex app-server | 当前固定 Runtime canonical schema；不新造 turn/start 的路由字段 | Runtime → Host |
| 标准 MCP 配置／审批 | 固定 McpServerConfig、McpServerElicitationRequestParams；Contracts 作准确消费投影 | Runtime → Host／Desktop |
| 新内置工具表面 | 拟新增 builtin-web-retrieval family；复用 web-retrieval 0.3 的输入输出定义，补 title／描述、应用错误与暴露资格 | Connectors → Runtime／Host／Desktop |
| 易界公开检索 API | yijie-contracts/openapi/public；封闭工具操作与普通产品身份 | API → 客户端适配器 |
| API→Connectors 执行 | yijie-contracts/openapi/internal 或同源内部协议；单一权威，避免与 MCP DTO 独立演进 | API → Connectors |
| Host→worker 装配 | 当前受管 startup/control 源增加独立 builtin capability，不伪造 selection lease | Host → worker |
| 云端调用／额度状态 | API 私有 storage migration；仅外部返回必要 code／operation ID／状态 | API 内部；公开投影回到 Contracts |
| 旧市场与历史 | 保留现有 schema、已保存 Item／审批／安装记录及 reader | 旧数据 → 新 reader |

S1已创建独立builtin-web-retrieval/1源、public/internal API候选、同源SDK及Host候选摘要，详见19。没有版本tag／不可变发布pin，后续消费者未全部接入。整体impact=breaking；局部新增API为additive，专家blanket修正是semantic，当前只在显式S1候选中生效。

修订 2 必须把执行、只读 operation 查询、尽力取消、仅网页委派／续期／撤销列为完整契约操作。Native 主会话仍为身份 owner；模型 tool arguments 不含委派／身份字段。不能只定义一个 execute POST 就声称刷新、停止与 unknown 恢复已经闭合。具体协议与边界见 [14](14-revision-2-boundaries.md)。

## 形状与语义要求

- 三个稳定 MCP 工具名和外部 REST 参数沿用既有定义；不增加 model/provider/key、任意 endpoint 或账号标识作为模型可填字段。
- 公开服务请求含有限 operation ID、工具枚举与对应封闭参数；身份取自可信产品认证。具体路径和 version 在源契约评审时冻结，不把文档占位直接当已上线端点。
- API 转发标准化 CallToolResult 时沿同一封包预算处理，避免在已有 text＋structuredContent 外再重复包装正文。
- 产品 session_expired、not_entitled、quota_exceeded、busy、upstream_unavailable 与供应商错误区分；上游鉴权失效不能继续显示“请用户重新配置 Kimi Key”。
- 原错误分类、空值／截断／content_status／dropped_results 可复用；应用错误文案和认证归属需独立生成，不手改旧生成文件。
- native MCP 结果类型在当前 renderer 中已有上限，新增展示按明确 server/tool/schema 投影；不将新结果写进 native web_search.sources。
- 同 operation ID 的原子查重、参数冲突、派发前持久状态、终态／unknown／result_unavailable、取消竞争、查重保留窗口及所有层的禁止自动重派发是必要语义。
- 最终 MCP 大小限制包含应用新增元信息；委派不可通过模型参数或 renderer 转交。Host／worker startup 与控制命令须区分 market／builtin feature、独立 capability、账户换代和按 turn 的 I/O 撤销。
- 明确离线专家资源按已评审版本／摘要处理；若需机器可读工具政策，其权威在资源契约，Host 只映射原生配置，不能解析角色文字来猜政策。

## 方向性兼容与切换

1. 新契约／service adapter 先形成可消费引用，部署服务端并完成身份和执行资格，再由新客户端调用。
2. 新 App 的正常聊天／专家使用 yijie_web；不再把旧 kimi-web 安装／勾选当成执行前提。
3. 活动旧 turn／审批正常完成或按用户正常取消；不在活动轮中改配置和授权。
4. 旧 outbox 或接受回执不能静默换端点、身份和费用归属。未发出的旧操作明确标成旧入口不再执行，正常提示用户重新提交；已经发送／unknown 的只查询已有事实，不重发。
5. 旧 kimi-web 安装、停用、卸载和工具历史保持可读；新默认能力不通过伪造安装记录实现。其他服务的 selection digest、授权和回执保持。
6. 删除新市场选用入口前同步所有活动客户端、专家资源和依赖声明。旧 reader 不支持新来源时保留新 reader，不能降库、清记录或重放云端请求。

## 来源与验证

实施时记录 contracts 的完整 commit/tag、生成器、源摘要和各 consumer 精确 pin；本轮只有审计基线。兼容检查应包括支持窗口登记的全部适用基线及当前消费者，不把单一 HEAD 比较冒充全兼容。源先行 → generate／lint／conformance → producer → consumer → 激活；Runtime 若需变化则先 canonical 再兼容投影。

跨仓 Owner 均由段成威负责，不虚构独立人工批准。相关准入、错误、默认、重试和历史语义通过人工评审与正常集成补足结构 checker 覆盖不到的部分。
