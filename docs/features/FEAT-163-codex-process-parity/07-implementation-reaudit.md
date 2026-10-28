# FEAT-163 实现复审（2026-10-24）

状态：实施中。用户要求逐入口审计并直接修复遗漏，已撤回上一轮整体D4完成结论。真实旧日志保留，文档门禁不作为产品证据。

## 本轮已发现并修复

| 问题 | 原因、修复与证据 |
|---|---|
| 图像工具会话重开丢指令 | Start单独拼接而Resume没有拼接。提取既有threadDeveloperInstructions给两者共用，baseInstructions保持同一permissionInstructions，仍只在Start注册原动态工具。RPC前测image/image+connector失败，修复后Kimi和MiniMax两种配置各5组合通过。 |
| 图像附加指令冲突 | 支持普通原生工具的会话仍写着read-only和“only permitted tool”。有Runtime权限或连接器上下文时限定为“only permitted dynamic tool”，不改变实际权限、审批或工具注册。旧受限模式继续原限制。 |
| 无信息抓取收敛证据不足 | 原23命令/7唯一参数与新4个不同空curl不能混为同一问题。保留真实执行和完整反馈，在原permissionInstructions要求检查HTTP错误/stderr/实际进程退出码、无信息时重新判断方法并及时交付，不新增去重/重试循环。旧受管目录精确字节保留于原升级门禁。新指令效果待真实回合。 |
| 文件结果误报空答 | completed且有明确fileChange变更时算可展示交付；failed/declined/inProgress及仅commentary不算。前测1失败，修复后通过；不改Runtime终态。 |
| 同轮草案重复显示 | 既有structured-answer slot曾对每条unknown/final消息重复挂载。仅在最后一个结果位置显示一份原校验入口；公开commentary不受影响，raw JSON仍不显示。前测2张，修复后1张。 |
| 冷历史完全不分段 | 原代码只允许native_observed。现在明确commentary和可确认工具终态可复用同一阅读分组；不改incomplete、phase、liveObserved或持久数据。缺状态的搜索/未知记录不冒称完成。前测无组，修复后有组。 |

另修正两项旧测试假设：并发重复提交受现有modelOperationMu串行保护，旧测试在释放第一调用前同步等待第二调用而自锁；改为正常并发等待原回执，确认Runtime调用仍1次。旧测试用正常SIGINT取消，无强杀、无Runtime/用户App进程被杀。草案测试误要求tool_choice=none，而固定Runtime client.rs实际总是auto；现验证真实空工具列表、原input-only receipt、0 MCP请求及正常重开，未放宽产品限制。

## 合约及复用边界

本轮最高分类semantic：修正既有Runtime base/developerInstructions组合及受管私有catalog正常升级，使用固定canonical已有字段，无新RPC字段、事件、权限或数据表。UI只是原Timeline/分组/slot选择，无持久格式变化。公共Contracts v5/v12及Runtime二进制不改。上一轮完整功能的breaking/replay分类仍保留，不以本轮分类倒改历史。

原catalog升级仅接纳精确已知旧字节，未知用户修改仍拒绝；正常重新启动验证。降回不认识新受管字节的旧Host会封闭拒绝，不擅自擦除目录或改写来源。仅本地候选，无Git提交/发布。

## 入口矩阵（每项单列证据等级）

S=源码路径；N=普通组件/内存RPC；L=真实固定Runtime+声明的本地Provider样本；R=真实付费Kimi。N/L不能冒充R。

| 入口 | 实际路径与本轮证据 | 仍需注明的边界 |
|---|---|---|
| 普通/有项目/无项目 | ChatPage createSessionWithResult→Host StartThread，项目只影响cwd；两种模型RPC、页面/store N，上一轮普通和项目R | 本轮修改后的R待补 |
| 续聊/模型切换 | ResumeThread复用同一指令组合；SwitchThread仍read/unsubscribe/resume，无新增turn；两模型RPC N，真实Runtime正常EOF/重开/续聊L | 当前Kimi新版本重开R待补 |
| 附件/看图 | 同StartTurnV2有序输入、接收回执及重开重复提交N；不改permissionInstructions | 本轮只授权文本文件，不含付费图片理解 |
| 图像/Artifact | 图像指令冲突与resume已修，原generate_image注册及意图边界保留；原Artifact展示+文件交付组件N | 未真实调用收费产图，业务工具资格不冒称通过 |
| 专家 | 完整普通基础指令+已验证role/index，工具配置原expertThreadConfig；RPC及原专家N | 本轮选已存在专家做Kimi进度R待补，不增加专家能力 |
| 技能 | 已有Skill资源/用户引用→原输入与Runtime工具链；chat-skills、页面/store N | 具体Skill必须记录实际选择，不能仅因界面相同声称全部技能R |
| 连接器 | 已有MarketPrepared配置合并及权限/回执，同公开消息链；RPC及选择/续聊/回执N | 本轮不调用外部连接器、不借用FEAT-162 |
| 计划草案 | **独立input-only/严格JSON路径**，不是普通permissionInstructions。Start/Resume相同canonical schema，工具关闭，独立校验；真实Runtime两次本地请求及重开L | 保留结构化边界，不强插普通前言破坏JSON；真实MiniMax资格未在本轮验证 |
| 已保存计划的执行 | 已有聊天提交与结果阅读链，调度器不改；与草案入口分开记录 | 不创建真实计划、不执行用户截图删除任务 |

## 重开、重复执行和消息缺失

- 有SQLCipher已观测记录：沿原NativeDisplayBuffer/commit_native_view/recovery_views恢复。已有存储测试明确冷read不能覆盖完整observed消息、命令或状态；本轮仍须正常App重开实测。
- 只有Runtime旧式历史：真实固定Runtime重开后thread/read返回historyMode=legacy，保留commentary/final正文，但省略命令条目，ID也可能重建。不能由前端补造。完整工具冷恢复未通过，旧证据不可写成全量PASS。
- 固定Runtime虽声明experimental historyMode=paginated，但thread-store/src/local/create_thread.rs:15及read_thread.rs:145明确reject_paginated_history_mode，当前本地store不可用，不能当已有可开启机制。完整工具冷恢复不能靠Host/UI补造；若后续要求在本地显示记录完全缺失时也恢复全部工具，需另行形成可用Runtime候选及canonical/Contracts读写方向验证。正常已保存记录继续复用既有SQLCipher机制，不另造日志解析器。
- 真实Runtime本地样本实际执行cat note.md，顺序为公开进度→command→final；每个结果出现在下一请求，正常重开读取不发模型请求；续聊再执行是明确新用户回合，不是重复通知引发执行。
- 同operationId接受重放、正常重开接受重放、并发重复各确认原回执且Runtime调用1次；模型自主重复同参数与传输重复是两类问题，不能互相替代验收。
- 原截图没有Provider原始事件，历史缺消息唯一根因无法追溯。新的真实回合对照Provider消息hash、Runtime公开消息及UI，保留phase unknown，不把reasoning改名为commentary。

## 本轮检查与证据

- `reaudit-host-before.log`、`reaudit-ui-before.log`、`reaudit-ui-more-before.log`保留修复前失败。
- `reaudit-host-entry.log`：9个顶层定向检查，含两模型各5条start/resume组合、旧模式、目录升级、专家、草案及模型切换。
- `reaudit-host-session-final.log`：7个普通Host检查通过，覆盖附件有序映射、并发/重开回执、模型快照、Market续聊和reasoning配置；先前挂起日志保留。
- `reaudit-real-runtime-final.log`：2个真实Runtime本地fixture检查通过，6次本地HTTP、0外部调用；**完整工具冷恢复单列未通过，不因这两个测试绿而改为PASS。**
- `reaudit-ui-entry.log`：9文件320PASS、2原有skip；组件前测72PASS；新增fixture先出现index/command字段类型错误，已修正；lint-final-2、Host vet、design docs build通过。
- 正式App canonical重建、3回合R、正常重开/最终差异审阅：进行中，完成后追加本节。

## 预算与续办

用户明确授权再增加最多3回合，总用户回合上限10；累计HTTP40、每次输出8192、联网动作20不变。本轮开始前已用7回合/17HTTP/10联网；禁止付费产图/外部连接器/FEAT-162。机器台账paid-call-ledger与user-turn-ledger已更新；meter独占期间不手改其台账。

下一步按冻结源码重建诊断App，做跨入口本地任务、正常重开续聊、联网研究三轮，逐次登记；到任一上限停止。结束后正常退出meter，恢复日常无代理App，更新02、04、feature.yaml和长期记忆。最终仍区分已证实机制、受限场景R与未覆盖入口，不再写“每次对话全部通过”。

## 真实第8回合及新增现场修复

第8回合选择现有“数据报告可视化专家”、已安装“发票生成”技能和两份普通CSV附件。用了HTTP18–20，共3请求/6命令/0联网。两段公开消息的Provider与Runtime hash完全一致，6份工具结果全部出现在后续请求，无重复参数，1次附件文件查找为空。UI在运行中显示了两段正文和淡色工具段。

**该回合交付失败，不是PASS**：HTTP20返回response.incomplete/max_output_tokens。发出的max_output_tokens为8192，Provider usage却报告8195，按真实值登记，不抹平为8192；没有再提高上限。任务269607ms后失败，未生成交付文件，UI保留内容和失败状态。

现场还发现并修复：专家的空managed连接器绑定触发空“工具调用记录”面板，改为仅真实选择/历史选择/审批/工具/错误显示，真实审批及结果保留；过程文字取消多余答案操作栏；failed/interrupted的phase unknown末条只称“模型消息”，不暗示正式回答。相关149项及最后48项前端检查通过，lint-final-4通过。将正常重建后再续办第9回合；不会把后续成功覆盖第8失败。

当前meter exec37640，仍使用同一累计台账；第8已落账，8/10回合、20/40HTTP、10/20联网，无在途。App已Cmd-Q正常退出，exec62124退出0，当前canonical诊断重建exec14843。此前macOS出现一次“上次重新打开窗口异常退出”提示，选择正常Reopen并进入就绪；未制造异常、未强杀，原因未凭提示归因。重开前后检查应以本次正常退出证据为准。

## 并行构建协调检查点

11:39起“分析 Web Search 与 Fetch 支持”在同一工作区实施用户另行授权的Kimi模型Key复用，更新market-provider/market-host/market-broker-control及专家派生源。build-3在market-host Rust生成物、build-4在experts JSON Schema生成物被canonical门禁阻断；随后比对确认为对方进行中的共享源变动，不是FEAT-163单方面漂移，不手改hash或回滚。

用户明确回答“允许发送协调消息”，已仅向该线程发送一次协调消息：对方先完成共享源/生成物和自己的无HTTP配置验收，在FEAT-162原续办记录留下可交接检查点，本任务暂缓共享App构建。无派发子代理、无Git变更、无替对方执行收费调用。为防交叉使用，FEAT-163 meter37640已正常Ctrl-C结束；再次启动时沿同一20请求累计台账，不重置计数。App本任务已正常退出，下一次启动前确认对方状态。

待交接前可独立完成本轮差异审阅、UI定向回归、文档矩阵；第9/10回合仍未发送，8/10回合、20/40HTTP、10/20联网、在途0。

补充边界：completed且可展示的partial文件变更（例如大diff省略部分内容）仍算交付，不能因安全投影不完整误报无产物；unavailable和空changes不算。复用同一hasDeliverable判断，增加partial普通回归。

## 文件编辑机制复审补充

既有第3回合真实证据为shell heredoc创建文件、native_file_change_observed=false；第4/6回合只有用户明确指定apply_patch才验证原生补丁。固定model catalog的apply_patch_tool_type为null，但原exec_command已有apply_patch拦截，不能因此宣布自然文件任务全量对齐。固定Codex prompt.md:132已有使用apply_patch编辑文件的原则，本轮把它补回同一个permissionInstructions：编辑及小文本创建优先原生补丁，没有独立工具则沿现有exec_command入口调用；真正需要格式生成/转换时仍可用程序，不从stdout伪造fileChange。

不改工具schema/模型catalog工具类型、不新增工具或Runtime代码。已激活过的复审旧指令字节作为第二个已知catalog版本加入原preflight门禁，正常升级测试覆盖两种旧版本。后续第9回合不在用户文本中显式指定apply_patch，用实际结果验证默认指引是否有效；仍不得承诺模型每次必选同一种工具。

## 最终诊断构建与解锁等待

FEAT-162已正常完成、退出并交接共享窗口；本任务刷新当前Host冻结，canonical build-5 PASS（含最新文件指引与UI修复）。完整来源回执另存reaudit-final-diagnostic-launch-receipt.json。CUA在选择App时报告Mac锁屏并无法自动解锁，已请求Owner手动解锁。第9/10回合尚未发送，8/10回合、20/40HTTP、10/20联网、无在途；meter93410和App26892保留待正常验证。此次构建成功不等同新UI/模型验收成功。

等待手动解锁期间已正常Ctrl-C结束meter93410，退出0；未发送后两轮、未强停App。App26892保留，解锁后先核对其就绪状态和第8历史，随后以同一台账重启meter再发第9/10轮。最新前端lint-final-5、五仓diff --check和文档strict current-3 PASS。五仓HEAD未变、基线文件无缺失，Runtime工作区无变化；当前差异快照reaudit-diff-review-current.json同时记录并明确排除他任务共享变更的归属。

## 解锁后的真实复验结论（第9、10回合）

Owner解锁后，最新诊断App服务正常。重开第8轮保留2段公开正文、6条真实命令、2段活动和失败状态，空连接器面板已消失，HTTP20→20。末条phase未知消息仍受“末条保护”而保持可见，标签是模型消息；不能凭内容猜成final或私自重写phase。正常历史冲突提示保留观测事实。

第9轮在同一专家/技能会话续办精简文件任务，用户没有指定apply_patch。实际HTTP21开始后137262ms终止，0公开消息、0实际命令执行、0文件交付。模型确实选择exec_command内的apply_patch，但Provider达到输出额度，function arguments JSON被截断；Runtime拒绝解析，未派发补丁。Provider返回incomplete/max_output_tokens，发出8192而报告8195，原值保留。原生补丁默认选择有证据，成功执行及长任务进度**没有通过**。parse失败结果已记入Runtime；终止后没有后继模型请求，不能把“没有下一请求接收结果”误诊成持续循环里的反馈丢失。

第10轮普通入口、无专家/连接器选集，原题“全面对比苏州与杭州两个城市？”89979ms完成，2HTTP、2原生搜索、1公开进度+最终答案；所有公开正文hash与Provider一致，唯一工具结果在下一请求完整回传。但它执行了1次sleep 1空操作，用来等待/触发下一响应，**AC-004仍失败**。Runtime base instructions与两次Provider instructions的SHA完全一致，并确认包含preamble、禁止dummy wait和内置检索结果已可用的规则；因此本例不是这些指令漏传，也不是前端隐藏。没有相同参数重复派发，但“无重复”不能替代“无无效执行”。

证据：reaudit-eighth-reopen-check.json、reaudit-turn-9-diagnosis.json、reaudit-turn-10-diagnosis.json、reaudit-tenth-instruction-provenance.json和对应AX/截图。原题能回答不能覆盖专家失败和sleep空调用。

额度最终10/10用户回合、23/40HTTP、12/20联网（8原生搜索+4旧shell抓取）。22请求已知input299186/output38854/total338040，HTTP16用量未知；HTTP20/21报告8195均不抹平。无在途，meter98234与诊断App26892均正常退出0。没有第11回合授权。正在canonical恢复无代理日常App，结果随后追加。

## 下一轮可执行续办顺序（不另建机制）

1. 先读04最新进程/预算与本节真实失败，不重跑已通过的静态检查、不用原题成功覆盖失败。第11回合须Owner新增明确授权；HTTP和联网仍有剩余额度不代表用户回合可超限。
2. 优先审计现有模型配置和有效指令组合：Host internal/codex/chat_models.go的固定Kimi max profile、permissionInstructions、Start/Resume/expertBaseInstructions，及Runtime实际Responses预算与公开消息行为。HTTP21失败发生在诊断8192上限内，不能推断日常无该覆盖时也必然失败；亦不能为通过验收偷偷增大已授权上限或降低固定profile。
3. 如配置/指令需要调整，继续走现有runtime-chat-models权威源、受管catalog精确旧字节升级和原Start/Resume配置，不另建preamble模型、定时“我正在…”生成器、Host重试循环或工具替身。当前固定Runtime已经传递公开消息，缺Provider消息时不得用reasoning冒充。
4. 对sleep空操作，先复核固定Runtime/Provider原生web_search可用方式和结果是否可继续读取；当前一份完整feedback与禁止空工具指令都已到达。不要把前端隐藏sleep视作修复，也不要增加按命令字符串静默去重/阻断，因为合法文件任务与等待任务仍需要原工具语义。可复用的已有原生能力优先；若确无适用机制，明确提出具体兼容变更及验证，不能宣称prompt追加已保证消除。
5. 在获新额度后，用相同业务任务验证专家长任务的及时公开进度及完整交付、普通研究无dummy，再正常退出/重开；保留Provider→Runtime hash和call/output/next-request证据。严格区分失败重试的新用户回合与幂等重放，不能自动追问消耗额度。
6. 正常已观测历史用原SQLCipher恢复；仅Runtime legacy历史缺工具记录的限制继续保留。paginated本地store当前不支持，不能随意打开或另写rollout解析恢复器。

本次复审及确定代码遗漏修复已落地，但整体FEAT-163仍FAIL/in_progress，未签署D4完成。

## 日常恢复与最终检查点

canonical日常build及服务就绪PASS，exec83289、PID98651保留打开，meter98234退出0。与诊断回执的inputs仅verification base URL环境hash不同，Host/Runtime/worker完全一致。日常正常重开第8/9失败和第10进度/两个搜索/sleep/答案均保持；Runtime task_started仍专家2/普通1，没有新增回合。见reaudit-daily-restoration-reopen.json及daily截图。AC008普通已保存恢复PASS；仅Runtime冷工具恢复仍独立未通过。本轮实际额度与最终续办以04为准。
