# FEAT-175 B03：原生取消、审批与路由资格

2026-11-15，修订 3。明确实施位置、依赖与可判定验证；没有运行本文件的产品／模型用例。

## 1. 能力分工和允许的增量

| 事项 | 权威／复用 | Host／工具侧允许的增量 |
| --- | --- | --- |
| 何时选工具、tool_search、Code Mode、工具调用／结果回灌 | 固定 Codex 原生 | 声明同源工具，不新增 planner／分类模型／加载器 |
| 只读自动执行／需要确认时询问 | 原生 auto／prompt 与现有权限 | canonical elicitation 薄投影，不能伪造批准或再问 Broker |
| native turn 的开始、停止、终态和 Item | 原生 thread／turn／notification | 依据已有会话索引建立有界 I/O owner，转发停止 |
| HTTP 请求取消与费用记录 | 执行 owner、API／Connectors | 精确 operation 取消、claim 竞争与有界收尾；不制造 native Item |
| 同需失败后重复操作约束 | 现有 Runtime 检索 guard | 保留三个稳定工具名、真实 isError 和来源；不绕 guard 改名 |

不需要把搜索变成子代理平台。主代理可直接调用三工具；子代理沿现有有效 MCP 继承，不能为网页能力全局开放所有第三方连接器。

## 2. 调用归属与生命周期适配

在 Host session 层复用现有媒体入口的 GetByThread、ActiveTurnID、已接受任务 context、专家绑定和 cleanup 检查；新增仅描述正在进行外部 I/O 的 web call registry，不复制图像一轮一次限制。

每个 MCP session 在服务 factory 取得本机随机 session generation，调用使用原始 typed MCP request ID。Host 注册键为 worker generation＋MCP session generation＋typed request ID，并关联真实 thread/turn；对同一登记返回同一个 UUIDv7 operation ID。该注册只用于当前实例的协议去重与取消，不是模型规划／工具调度，也不是永久跨任务 query 去重。

注册前必须确认：当前受管 worker、本机 capability、已接受根会话／允许的原生代理归属、真实 thread/turn、当前专家网页政策及账户 scope。缺绑定只允许借现有模式进行最多 5 秒的有界正常等待；不能从请求字符串创造 root、沿用“最近活跃 turn”或复活过期授权。

Host 使用 turn context 的取消与原生终态通知关闭本地准入，并向 worker 发精确 web_turn_revoke／web_call_cancel。控制命令只是设置 I/O cancellation 和返回 ACK，不在控制 pipe 上等待 35 秒供应商 HTTP；共享 Native／worker 控制交换原 5 秒限制不被改造成业务超时。真实结果仍从 MCP 原调用返回。

本机停止不自动意味着远端停止。worker 在正常取消时尽力发 API operation cancel；API 根据 B01 的 ready／dispatch_committed 竞争返回 cancelled_before_dispatch 或 may_have_dispatched。跨代理断开／无法确认时保持 unknown，迟到结果只归原操作。

真正的安全授权期限仍按已有体系生效，不能为了“完整 HTTP 预算”延长失效身份。已接受 turn 的生命周期、当前服务端权限和工具执行预算分别处理；不把 UI 快照或市场 prepare 的时刻作为网页 HTTP 起点。

## 3. 标准原生审批的精确接线

默认 auto＋readOnly=true 不新增确认。只有原生有效策略要求确认时，消费 mcpServer/elicitation/request 并回复原 opaque request ID：

- 原 market handler 及其他服务策略保持；新增分支只识别当前受管 yijie_web 和已知 native tool-approval 元信息。
- canonical turn_id 是可空字段，并且没有通用 McpToolCall item ID。对本功能，缺失／不匹配活跃 turn 时明确 decline，不能猜测绑定或按 request ID 字符串推导 Item ID。
- 原请求 server、thread/turn、参数展示和可选动作经生成 schema 验证后，使用现有确认组件；只回传 Runtime 实际允许的 accept／decline／cancel 和记忆选项。
- 并发两个相同工具用两个真实 request ID 区分，不能仅按工具名复用批准。UI 可关联到真实 thread/turn 和审批 request，不假造不存在的 Item 关联。
- 拒绝、正常停止、退出／换租户后的晚到确认不能启动 HTTP。Host 不维护另一个批准状态机；仅保有等待原生回复的短期映射。

原生 pre-call 审批发生在 tools/call 前；原生 rmcp 的 active_time_timeout 支持 elicitation 暂停。这些能力继续复用，但不得推断丢弃 future 一定向 MCP 服务发送 CancelledNotification。Host I/O 撤销是应用外部调用所需适配，并由真实 wire 用例验证。

## 4. 候选时间预算与并行

| 阶段 | 起点／边界 |
| --- | --- |
| 模型思考／工具发现 | 原生 turn；不提前创建网页 HTTP 截止 |
| 原生确认 | Runtime 当前请求生命周期；不预占 API／HTTP预算 |
| 实际 MCP | tools/call 开始，60 秒 active time |
| 本机绑定／凭据就绪 | 最多 5 秒；无可用委派则未派发失败，不等待人工登录 |
| 公网 API | 从真正发送产品请求起最多 45 秒；认证拒绝的一次恢复也受当前父预算限制 |
| 服务准入／claim | 有界、无长队列；发送前检查剩余预算，Pro需完整35秒及结果余量 |
| 供应商 HTTP | Basic摘要／Fetch最多15秒；Pro／Basic正文35秒，上游timeout_seconds仍10／30 |

60／45／35 是初始配置候选，验收使用真实时间戳证明组成关系。不能把每层超时依次相加而超出父请求，也不能收到客户端超时后开始另一轮 35 秒请求。父预算不足时返回明确未派发；若 claim 已提交则保守记录可能发送。

只读工具允许原生并行，server supports_parallel_tool_calls=false 不能强制串行。服务端共享纯逻辑与受管 Key 引用，每 operation 的 permit／cancel／deadline 独立。建议主体并发默认 2，运营账户总并发为有限部署配置；容量不足返回 busy，无隐藏队列、无自动重试。

## 5. 资格顺序与停止条件

| 阶段 | 依赖 | 做什么 | 退出条件 |
| --- | --- | --- | --- |
| Q0 源闭合 | Contracts候选、固定 Runtime／依赖、可复现本机产物 | 校验已存在原生配置和新consumer/source-first；检查 secret／UI／退出范围 | 无影子 schema，无任意二进制替换 |
| Q1 零费用真实协议 | Q0；普通本机模型／MCP响应、最小同源本机接线 | 用固定真实 Runtime 验证声明、发现、Code Mode、auto、prompt、停止、并行和结果回灌 | 下述Q1范围全部通过、记录实际wire；云端／分发分项保持NOT RUN，不调用供应商 |
| Q2 小规模真实路由资格 | Q1、明确获准的精确模型profile及独立预算 | 六类各1提示×两模型，共12任务；只检查关键能力与路线可达性 | 两模型各有native及MCP成功；没有结构性路由／取消问题；费用和失败全保留 |
| Q3 完整冻结评测 | Q2、真实云端adapter及另行额度 | 24输入×2重复×2模型，96任务；专家对照另记 | 定义的首次路径、关键任务、额外调用、证据／费用标准全部达标 |
| Q4 新用户分发 | B01/B02及Q3、公开制品资格 | 正常新设备 App 到供应商闭环、正常退出和重开 | 完整 Must 与公开/生产门禁有真实证据 |

Q2 不是 Q3 的小样本替代；96任务也不是96次HTTP的预算上限。Q2 必须在大规模云端／客户端实施前完成，避免最后才发现 hosted 与 MCP 共存不可达。当前全部阶段产品执行 NOT RUN，预算为0。

Q1仅要求N01—N05、N08的原生协议／本机接线部分，以及N07的本机并行隔离、N10的正常本机生命周期；N06／N09可做普通契约状态conformance，但不能计为真实云端事务或恢复通过。允许先实现最小同源适配来证明这些路径，不要求先交付S2—S5。N06／N07的真实服务端claim／多用户隔离在S2补验；全部N项在Q3复验最终产品链，公开carrier／新设备部分在Q4补齐。每项证据标记阶段与覆盖层，不以Q1通过将整项或整个B03最终验收涂绿。

Q2 可以使用已获准本机模型profile和普通合成MCP结果提前验证选择行为，以免等待云端完成才发现模型协议不兼容；合成结果必须标明用途，不能计为真实网页取回。此证据不能代替公开profile资格：Q3／Q4必须重新验证最终支持的产品profile、代理链和真实结果。精确模型版本／工具表／传输能力／Runtime构建／工具描述任一变化均记录证据适用范围，不能挪用旧通过。

模型推理预算优先使用 Runtime 既有 token／rollout／Goal 机制，不在 Host 另造 Token 累计器。它不等于人民币上限；托管搜索与 REST 次数按各自实际记录计入预算。无法约束供应商内部搜索次数时，只能停止新请求准入，不能宣称已经发生的费用被撤回。

若只在改描述后某次成功，不判路线稳定。若固定Runtime实际能力不足，保留失败、停止相关资格，按源码缺口单独评审最小原生扩展；不能退成 Host 分类器、强制供应商 tool_choice 或篡改响应。三次同点失败沿既有复盘规则，不机械重试。

## 6. N01—N10：可判定的原生验收

| ID | 场景 | 判定 |
| --- | --- | --- |
| N01 | 普通／专家inherit／明确disabled、双模型、移除／切换／冷恢复 | 实际provider工具表符合政策，不只检查Host map；旧历史不改写 |
| N02 | 普通只读auto | 真实MCP结果＋最终回答；没有业务Broker审批和虚构批准 |
| N03 | ask＋reviewer=user＋精确prompt，正常等待90秒 | 允许前供应商计数0，允许后有完整执行预算；无记忆批准污染 |
| N04 | 模型先正常等待120秒再调用 | 没有prepare过期；实际call后按预算执行，身份仍有效 |
| N05 | 原生停止／拒绝／晚到确认 | 记录真实MCP取消通知是否发生、Host撤销ACK和API取消状态；不把本地future结束记为远端已停 |
| N06 | cancel与claim正常竞争 | cancel先提交零发送；claim先提交可有一次且明确可能计费，不发送第二次 |
| N07 | 同账号／两账号正常并发，取消一个 | 另一操作不被全局Backend.cancelled或permit影响；无错误串行队列 |
| N08 | 检索之后正常文件计算、合法本地开发服务请求 | 既有guard仍识别三个名称，不因常驻注册阻断正常本地工作 |
| N09 | 弱网络自然出现未知结果／已完成正文不可恢复 | 有事实则记录；无自然样本用普通状态conformance，不制造断网／强杀；旧ID不重发 |
| N10 | builtin-only／market-only／both正常启停及来源资格 | 关市场不关builtin；仅builtin不读旧供应商Key；合法不可用不伪装ready，正常EOF收尾 |

Q1 使用普通有限响应、虚拟时间和正常停止；不用攻击fixture、权限破坏、故障注入或fake executable。需要Native实际窗口的用例在实施后按原入口验证；本轮不启动／重启 App。

## 7. 路由评分与反向取舍

首个有意义外部检索动作（含真实 hosted web_search_call）及其参数单独评分；本地 tool_search 发现不计。先Basic后纠正Pro，或先hosted预检索后Pro，均不能改写首次选择事实。合法预期的Pro→Fetch序列在冻结输入时声明。

每模型48任务，六类每类8项；主要路径候选门槛≥95%，关键明确URL／过滤／纯列表用例全部符合，另逐类报告。额外hosted分母固定为四类独立检索任务32项／模型，候选门槛≤5%；额外REST、失败提议、无效参数零发送和恢复另外计数。正确路线与HTTP／交付／回答质量分别判定。

默认共存是待真实资格支持的推荐。若Q2已显示供应商预检索使任务目标结构性不可达，不继续凭提示词堆砌押注；保留普通问答默认native的目标，并提交明确任务范围或最小原生工具计划扩展的证据方案。不得未审阅就新增模式选择器或隐藏分类模型。

## 8. B03 的完成定义

实现方式、依赖和验收定义在修订3完成；B03的早期可行性前置通过需Q1与Q2真实证据，端到端验收及最终交付还需Q3/Q4。未实施时不把“源码有MCP／pause”写成取消端到端或双模型路线已通过。
