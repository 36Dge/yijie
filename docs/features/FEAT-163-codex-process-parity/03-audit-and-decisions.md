# FEAT-163 复审、事实与决策

日期：2026-10-24。范围：重新审计前两轮分析/方案，冻结可执行边界。文档里的源码为当前工作区事实，不冒称全部已提交或正在运行的包与源码完全一致。

新增参考图修订见[05](05-tool-activity-reference.md)：工具活动必须保留淡色分段摘要与本段展开明细，不能全部移入技术详情；现有v4对文件动作/变更/App字段不足，已纳入版本化安全投影计划。以下历史消息缺失审计结论继续有效。

## 1. 本次审计纠正的风险

| 原方案可能被误读的地方 | 修正后的执行要求 |
|---|---|
| Runtime已有支持，所以改optional为must即可 | Runtime支持、有效指令、Provider实际输出、跨层传递、UI实时显示必须联合证明；提示词不是结果保证 |
| 没有commentary是模型的问题，因此UI通过即可收尾 | Provider无公开进度只能定位失败层；AC-002仍未通过，不能降级成日志展示需求 |
| completed.output可能有答案，所以预先补全量output | 先取得对应Provider证据；只评估真实且身份一致的缺失消息；不能重放工具或二次完成 |
| phase=null要等终态再显示 | 正文到达立即显示；仅复用已有只读布局兼容，不写回猜测phase |
| 一出现assistant文字就收起过程 | 仅显式非空final或真实Turn终态触发默认折叠；用户选择优先；null不自动判final |
| 无assistant正文统一判Runtime failed | 原生shell/compact可合法无正文；普通问答未交付和原生生命周期分开 |
| 相同参数去重能解决重复执行 | 同call_id重放与新call_id重复决策不同；正常轮询/重复验证不能一律拦截 |
| 摘要相同说明同一事件重复 | 不同Item可以内容相同；传输去重依身份，内容折叠只影响详情阅读 |
| 60秒或180ms是Codex端到端标准 | 未测得此标准；180ms是本地现有显示游标追赶目标，不含Provider/网络/工具时间 |
| FEAT-162能顺带解决进度 | 仅候选检索改进；工具更有效也不能代替原生进度/最终答案/时序验收 |
| 只测城市题就覆盖每次对话 | 入口和状态矩阵全部适用，短答/续聊/工具/长任务/恢复不能省略 |

## 2. 已核实事实（F）

### F01 — 精确问题回合

用户问“全面对比苏州与杭州两个城市？”。Runtime thread `01a16978-11b8-7683-9878-8f4effb0fb71`，turn `01a16978-1202-7fa2-98f5-ee441cd2fe13`。274207ms；13 web_search_call、23 exec_command及23对应输出、10 reasoning，0 assistant message；末行114的task_complete.last_agent_message=null。

23次执行只有7种命令：两个统计局curl/head各5次；两个统计局curl/grep GDP/head各5次；ArticleTitle读取1次；两个市政府替代URL各1次。结果为首页HTML共6次、403共5次、空输出12次，全部exit0。命令是正常引号，不是嵌套JSON转义造成的URL错误。10条summary只有2种内容，每种5次；只记录摘要指纹结论，不在本包复制推理正文。

本地原始记录路径、文件哈希在[evidence/planning-baseline.json](evidence/planning-baseline.json)。原始rollout不复制到文档或生产UI。日志可能随用户正常删除历史而消失，不能要求恢复/补造该历史。

### F02 — 原生机制已支持

源码锚点（相对CrossBSD）：

- `yijie-codex/codex-rs/protocol/src/models.rs:893`：MessagePhase明确Commentary/FinalAnswer/None未知。
- `yijie-codex/codex-rs/models-manager/prompt.md:33,175`：preamble及长任务公开进度要求。
- `yijie-codex/codex-rs/core/src/event_mapping.rs:123`：phase进入AgentMessage；`app-server-protocol/src/protocol/v2/item.rs:830`继续保留。
- `yijie-codex/codex-rs/core/src/session/mod.rs:614`：显式base优先于历史base和模型默认指令。
- `yijie-agent-host/internal/codex/runtime_permissions.go:18`：Public progress messages are optional；本轮session_meta确认其实际生效。
- `yijie-agent-host/internal/codex/session_protocol.go:545,625`：start/resume覆盖base。
- `yijie-agent-host/internal/codex/chat_models.go:92`：Kimi目录基础指令也被简化；不能假设移除Host覆盖即完全恢复原生沟通要求。

官方参考：[Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)、[app-server](https://learn.chatgpt.com/docs/app-server)。以固定本地版本为实施权威，不能顺手复制最新文档新增枚举。

### F03 — 现有Host/Desktop支持公开消息但阅读布局错误

- Host `internal/session/native_conversation.go:82`保留消息text/phase，reasoning独立保留。
- Desktop `src/domain/conversation-view.ts:410`、`conversation-timeline.ts:410`已有commentary/final/unknown分类。
- `src/domain/conversation-process.ts:84`和`ChatTurnGroup.vue`把活动组织成计数及逐项展开；`repeatedSummaryItems`产生重复摘要标签。
- Host `internal/session/feat136_projection.go:406`将命令缩成通用安全标签；不能在前端据此声称识别了curl目的。
- Native `native_conversation.rs:82`是单一显示缓冲；`application.rs:2921`先commit后publish；SQLCipher保留现有事实/视图。

### F04 — 结束和无正文并存，不足以归因

Runtime `codex-api/src/sse/responses.rs:433`当前completed路径不全量回放output；`core/src/session/turn.rs:2279`可在无后续工作时结束；`tasks/mod.rs:769`允许last_agent_message=None。合法用户shell和compact也存在Ok(None)，所以不能全局改completed含义。

当前样本没有Provider边界完整证据，不能直接判定Provider未生成、Runtime吞消息或某补丁必须实施。0005只处理空function arguments并维护顺序；它不是通用message恢复器，还可能影响后续消息到达时机，需独立测时。

### F05 — 先前失败不能再被忽略

[2026-10-23双来源报告](../../dev/dual-progress-resume-20261023.md)记录：强制先给独立进度后，出现9次echo、10次搜索、0答案并正常中断。之后一些短回合有答案但0独立公开进度。它们不能继承为本任务通过。

### F06 — 诊断与工具回灌已有实现

Host `scripts/responses_stream_observer.py`已经记录request中的call/output身份、长度、hash和response中added/done/completed的Item摘要。它按stage覆盖快照，缺逐Item重复次数/时序；数组output只有数量。`chat-model-smoke-meter.py:181`改写max_output_tokens至8192；不能冒称请求透明。

Runtime `core/src/session/turn.rs`、`tools/parallel.rs`及`context_manager/history.rs`已有原生call/output/next request。UI安全投影不在tool→model结果返回链。内部success不是独立wire成功标志，模型理解依赖真实output正文。暂无查证可直接启用的通用无效重复guard。

## 3. 尚未解决的问题（U）与最小证据

| ID | 未决问题 | 最小区分证据 | 禁止的跳步 |
|---|---|---|---|
| U01 | 历史回合Provider输出已缺证；后续是否复现同类公开消息/最终答案缺失 | 新授权回合各SSE阶段的类型、身份、字节数/hash、terminal原因；只证明该新回合 | 不据rollout零消息断言Provider零生成，不用新成功追溯证明历史回合 |
| U02 | 历史工具请求边界缺证；后续同类任务结果是否真正进入下一Provider请求且可理解 | 新回合call_id关联、规范化/截断后output摘要、下一请求input摘要 | 不以本地历史存在替代真实请求证据，不把新回合证据倒填旧回合 |
| U03 | 是否有缓冲导致commentary终态才可见 | Provider、parser、app-server、Host、Native、DOM各层相对时间 | 不以最终正文hash一致替代实时性 |
| U04 | 当前包与正在运行来源是否一致 | canonical receipt、Runtime manifest、有效配置与指令哈希 | 不以HEAD或源码存在推定当前包 |
| U05 | 各入口是否覆盖同一沟通基础 | start/resume/switch/expert/structured实际组合与调用路径矩阵 | 不只测新建普通聊天 |

## 4. 本次推荐决策

采用“原生链路复用、证据决定最小修复、同一Timeline阅读改造”。不采用另建进度总结模型（增加成本和来源混淆）、只做UI降噪（无法满足目标）、默认全量Runtime升级（现有能力已足够且扩大兼容范围）。

D01：长任务真实公开进度和正式交付是硬目标，不因Provider行为或工程困难降为可选。

D02：优先保留当前协议和存储；条件性Runtime修复须有对应U01/U02/U03断点证据、精确范围、source-first和实际授权，不能把方案分支视为补丁已批准。

D03：无phase使用现有只读布局，原始phase永远不猜填；对消息内容来源与UI位置分别描述。

D04：重复无效执行先修结果闭环和有效规则；没有原生guard证据就不发明“复用guard”。若仍失败，状态保持未达标并给出具体下一项兼容/配置选择，不原样重跑、不静默缩目标。

D05：截图1是用户确认的视觉参照；不能把不可见的Codex桌面私有实现说成已复刻，也不要求不同模型逐字相同。比较的是过程语义、时序、交互和完整交付。

D06（新增参考图）：复用现有processActivityGroups及activityChoices做分段工具摘要，明细属于对应段而非统一诊断入口。文件动作及App信息取Runtime已有结构化字段，当前下游丢失处按05版本化补齐；不解析任意命令猜动作、不让模型生成标签、不把每个action变成一次新执行。

D07（新增字段事实）：原先semantic/持久不变的规划范围修正为完整投影按breaking/replay保守审查。新增展示所需字段已在固定Runtime及canonical schema内，不据此新增Runtime patch；消息缺失补丁仍按D02取证。文件增删统计必须区别add/delete内容与update unified diff，未知不填0。

这些是推荐实施决策，不代替用户尚未给出的实施、付费、Runtime补丁或Git操作授权。后续改变D01/目标/Must需保留原记录并引用用户明确决定。
