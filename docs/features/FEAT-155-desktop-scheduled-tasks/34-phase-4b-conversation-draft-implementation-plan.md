# FEAT-155 · 下一步执行方案：4B 对话创建与草案确认闭环

> 实施中的第二次修订：第二次真实请求仍返回旧问答格式，native 拒绝保存。只读 rollout 证明旧 developer 消息没有更新；固定 Runtime 源码和本机旧配置→正常退出→resume 组合验证证明，稳定 `baseInstructions` 可在恢复后进入每次 Provider 请求。因此同源 schema 改由受限线程的 baseInstructions 提供，developerInstructions 仅保留不执行的用途约束；不修改 Runtime 或原历史。用户随后明确“再授权2次调用额度”，本批上限从3增至5，仍计入原总额12；原两次请求保留，禁止重置台账。以本段覆盖下文原3次上限和先前 developerInstructions 方案。

> 2026-09-19 实施修订：用户已授权仅实施本方案。首个真实请求 HTTP 200，但 Provider 返回 `action/questions` 对象且没有 phase；原生拒绝确认，计数为 1/3。为完成同一创建闭环，Host 在原有 `outputSchema` 之外，把同源 canonical schema 原样加入受限 developer instructions。原生预览允许唯一完整、严格 schema 合法的无阶段 agentMessage，但仍要求精确受限用途/binding、同一成功 completed turn；不改写原 phase，明确 commentary 不作为候选，多个答复、partial、失败及错误格式继续拒绝。UI 对无阶段答复提供来源校验入口，不自行解释正文。该调整属于本批 semantic 范围，不修改 Runtime、公共协议、输出 schema、数据库版本或执行权限；在剩余两次真实请求前完成定向验证。以下“只接受 final_answer”是规划时的旧证据，执行以本段限定为准。

2026-09-19。用户本轮要求“给出下一步执行方案”。**建议下一次只实施 4B：对话预填、受限草案对话、摘要确认及暂停计划保存，并用少量真实文本验证这条完整用户路径。** 本轮仅调查、方案审查与文档更新，产品代码、服务和调用均未开始。

起点为[33：4A 实施报告](33-phase-4a-management-ui-implementation-report.md)。管理页和手动保存已接通，Runtime 受限能力及原生装配已有证据；目前还没有可用的对话创建 UI，真实 Provider 的草案输出也未验证。4B 直接补齐第二种创建方式，完成后报告停止。计划启用、手动运行、自动触发、独立重跑、完整运行详情/定位、防空闲睡眠和应用内重要更新另批完成；原十项 Must 不缩减，系统通知继续延期。

## 1. 选择与边界

| 方案 | 判断 |
|---|---|
| 只做 Provider 命令行探测 | 可以验证模型，但不能证明真实 UI、草稿保护、来源确认和同源保存；不单独作为下一批交付。 |
| **接通对话创建，再经相同 UI 做限额真实验证** | 复用已有草案执行和管理表单，形成一个用户可用结果；推荐。 |
| 同时开放启用、自动执行、重跑与电源能力 | 涉及尚未装配的运行 authority、后台生命周期和平台证据，混合多个独立边界；本批不纳入。 |

包含 Desktop 页面与必要的私有只读契约、Host 最小验收计数接线、来源查证、确认保存、正常重开及定向验证。不新增 Runtime 补丁、公共 Host API、SQL24/Store7、通用草稿持久化、第二执行器或通用计费系统。不把已有普通聊天改成受限用途，不把受限草案当定时执行目标。

保持普通 **SQL15 / Store5**、显式候选 **SQL23 / Store6**；候选数据根仍为 `demo-fast-scheduled-candidate-v1`。不迁移日常库、不启用 experimental、不更换 Provider/模型、不修改用户权限模式、不提交/推送/发布。新保存计划一律 paused、无执行 grant、无 scheduled run。

## 2. 源码复核与需要补齐的前提

| Fact（当前源码） | 对实施的约束 |
|---|---|
| `ScheduledTasksPage.vue` 的“对话创建”仍 disabled；`ChatPage.vue` 的 submit 仅走普通 create/turn | 在既有 `/chat` 入口和 ChatPage 增加明确的草案创建模式，复用聊天展示；发送必须使用已有 scheduled draft IPC。 |
| `App.vue` / `chat-permission-lifecycle.ts` 已支持管理 context 向完整聊天 context 升级；`local_host_bridge()` 仅取缓存，capabilities 查询不启动 Host | 通过同一 App 协调点完成聊天准备；不能让页面自行 bind，也不能靠反复读 capability 启动服务。 |
| native 已有 `draft_conversation()`，普通 enqueue 和 permission change 会拒绝草案；renderer 的会话摘要没有这项用途事实 | 需要最小原生用途读取。冷启动、侧栏打开及深链都先识别用途；URL 模式和标题不作为授权依据。 |
| `find_draft_source()` 仅按 conversation_id + local_turn_id 查找；`submit_draft()` 已按 scope + request_id 保存来源和幂等 digest | 首次提交丢回执时还没有这些返回 ID；补原请求只读回查，不能换 request_id 或按文本猜会话。 |
| `preview_draft()` 只接受精确 native binding、完整 final_answer 和 completed 事实；已确认来源返回 plan_id | UI 只消费该候选/澄清结果，不自行解析助手正文并保存。确认不确定可按 source 查证，再读当前计划。 |
| `confirm_draft()` 在同库事务绑定 source、确认 digest 和唯一 plan；`ScheduledPlanForm` 目前只接收 PlanView | 复用字段编辑和 native 时间/目标查询，增加草案初值与确认用途；不能伪造 PlanView，也不能改走普通 save 创建第二份计划。 |
| `continue_draft_source()` 与最后 POST 准入保留 attempted、generation、scope 和当前 UI 授权检查 | “回答澄清”是新请求/新 turn；“继续原请求”只适用于可信恢复后从未尝试的原 turn，二者不能共用重试按钮。 |
| 统一 worker 只安装 draft authority；manual/automatic authority 仍未装配 | 草案 ready 不能解锁计划执行。保存确认不能顺便授额度或开启调度。 |
| Host `permissionVerificationConfig()` 仅被普通 session_protocol 调用；`scheduledDraftStartParams()` 未接入此计数配置 | 不能假设环境变量已覆盖草案。真实调用前，将既有固定计数通道的 Provider 地址与零重试设置接到受限 start/resume；不继承自动审查 policy。 |

Assumption：既有标准 Provider 凭据与候选产物在实施时仍可用，需由 canonical 预检核实，不读取或输出凭据。Unknown：真实 MiniMax 的澄清/候选输出质量与该完整 UI 路径，留本批实际验证。Conflict：4A 的三项既有 ChatPage 显示断言失败仍在；涉及的新草案展示必须重新验证，不能继承“非新增”结论来忽略新的失败。

本轮文档 **contract-impact=none**。未来 4B 整体按 **semantic** 审查：验收配置将覆盖草案、renderer 根据原生用途选择既有发送语义；新增独立只读命令本身 additive。普通受支持会话行为必须保持，发现不兼容时在实施前升级 breaking 并修订方案，不能直接改旧闭合 DTO。

## 3. 实施顺序与完成标准

| 顺序 | 实施内容 | 完成标准 |
|---|---|---|
| 1 | 私有用途读取、草案原请求回查及计数设计 | 源先生成/校验；旧 24 个 scheduled 命令和旧 chat 响应保持；草案真实出站受同一计数上限约束。 |
| 2 | 对话入口、预填保护与共享启动 | 点击只预填；保留/替换由用户选择；无自动创建/发送；management → chat 使用同一 context 协调和候选 Host。 |
| 3 | 受限草案发送、澄清与原生展示 | 首次创建独立受限会话，后续回答复用该会话；普通发送、附件、目录选择和权限切换不进入草案链。 |
| 4 | 摘要编辑、确认与恢复 | native 候选绑定 source/digest；用户确认后唯一保存 paused；不确定先查证，重开不重发，返回管理页为同一计划。 |
| 5 | 零调用检查及原生 UI 预检 | 普通聊天/管理不回归；真实预填、取消、亮暗、最小窗口和键盘可用；计数接线先经正常本机组合检查。 |
| 6 | 最多 3 次真实文本验证、审查和报告 | 取得真实澄清/候选、确认保存及正常重开证据；失败和未执行项如实记录，报告后停止。 |

## 4. 最小契约与权限

只补两个局部只读入口，名称可在源评审时按现有命名规范定稿：

1. **会话用途查询**（建议 `chat_get_session_purpose_v1`）：归 Desktop `src-tauri/schemas/chat-ipc-v1.schema.json`。复用既有 context、request、session 读封套与错误，要求 `task.read` 和原生 scoped session 存在性，返回封闭的 ordinary / scheduled_plan_draft 用途事实。不能额外要求 `schedule.read` 才能读取普通聊天的用途，否则会改变普通聊天权限。SQL15 经资源校验后明确不存在草案表；候选未知格式/用途或不可访问均返回对应不可用错误，不能默认 ordinary。读取不启动 Host、resume 或排队。不暴露目录、配置、凭据或源正文。
2. **草案提交回执查询**（建议 `schedule_read_draft_submission_receipt_v1`）：归 `scheduled-task-ipc-v1.schema.json`，按原 request_id 与 native scope 查询已有 sources 表。闭合区分“已观察提交”“尚未观察”“来源已删除”；已观察复用 DraftReceipt，删除状态不能伪造已清除的 conversation/turn ID，已有 plan 仅按真实绑定引用。零行不是提交失败。需要有效 schedule 读取授权，不调用 Host、不补写 outbox。原管理 mutation receipt 仍只处理 save/pause/delete。

先确定权威 schema，再由 native provider、严格 validator、typed client 和 UI 依次接入。scheduled 继续使用原 generator；chat 新投影使用最小同源派生与 Rust/TS conformance，不顺带迁移整套旧聊天 DTO。旧封闭响应不加字段；共享 Candidate、Clarification、PlanDefinition、DraftReceipt 引用原源，不手写影子定义。两查询直接读已有表，**无新迁移**。

重开草案：从真实 session 用途及当前读取的 local turn ID 调用既有 `schedule_find_draft_source_v1`，再读 preview。只查询当前选定来源，历史来源按用户选定的真实轮次按需读取，不全文扫描、不以名称/内容关联。无 schedule 读取权时仍可按 task.read 看允许的聊天历史，但不暴露或启用草案管理动作。

## 5. 页面、发送与确认

管理页“通过对话创建”交接一次性的本 scope 内存意图，进入既有新任务输入框，预填已批准引导词：`请帮我创建一个定时任务，每【时间间隔】在【时间/时区】执行【具体跨境电商任务】。` 不把正文放 URL、localStorage 或日志。路由模式只表达用户进入意图；已有会话用途必须以 native 查询为准。

已有未发送文本/附件时默认保留并取消切换；用户明确选择替换后只替换该目标输入，不拼接原正文、不删除其它会话附件。普通会话中发起计划创建时，只交接用户明确选定的文本到独立受限会话，不自动复制历史、附件、项目、MCP/skills 或秘密。复用 4A 离页保护，覆盖 mode/route 更新和返回管理页，不能仅处理组件卸载。scope/撤权清除未提交输入；预期的同 scope 启动升级需与交接顺序协调，不能误清已确认预填，也不能跨权限保留。

采用既有 ChatComposer、ChatTimeline、Naive/Yj 组件及 2.1.0 tokens，新增模式提示“创建定时任务草案，确认后才会保存”。该模式只接受文本，不显示可用的附件/工作目录/普通权限切换操作；不修改全局 Ask/Auto/Full。通过原 App/chatStore 完成执行准备后读取 draft capability，缺资格显示原因和恢复入口。管理本身仍不依赖 Host。

首次明确发送调用 `schedule_submit_draft_v1`，不传 conversation_id；回执给出真实会话后进入相应 ChatPage。后续回答澄清使用同一受限 conversation_id，但新的 request_id/source/turn。常规聊天发送路径仍由 native guard 禁止对草案写入；草案提交不能以路由伪装普通会话通过。UI 复用原 native 事实缓冲/订阅/历史，不建立第二套正文或终态状态机。经 native 校验的该轮 final_answer 用澄清或摘要卡呈现，不要求用户理解内部 JSON；原事实和轮次关联保持，未验证文本不能伪装成摘要卡。

候选卡只来自 `schedule_preview_draft_v1`：

- needs_clarification：展示问题和缺失项，由用户发送下一轮；不自动补默认值冒充澄清完成。
- candidate：打开共用表单，展示/可修改名称、任务内容、四频率、时区及三种目标，调用已有 native 时间预览。模型给出的 existing_chat_label 仅是说明，必须由用户从 scoped 目标列表选择真实 ID；不按同名自动绑定。
- unavailable：展示当前可信的排队/处理中/无法确认信息；没有状态证据时显示尚未确认，不能无限显示“正在生成”，也不能把无输出当失败或可重发。允许只读刷新及安全离开。
- confirmed：按 plan_id 读取当前计划并提供“查看定时任务”；计划已编辑/删除时如实显示，不恢复旧快照或复活计划。

确认按钮调用原 `schedule_confirm_draft_v1`，绑定 source_id、source_digest 和用户审阅后的完整 definition；native 提交时重新校验。不能调用普通 save 绕开来源唯一约束。取消不保存；脏表单默认继续编辑；确认后管理页显示同一 paused 计划，不显示“已启用/已安排执行”。过期一次性时间重新审阅，不能静默移到未来。

## 6. 不确定结果与正常恢复

| 情况 | 行为 |
|---|---|
| 首次 submit 没有返回 receipt | 同 scope 内存保留原 request_id 和原文本；先只读查询原请求。已观察则绑定原 source；尚未观察仍不当失败，用户可继续查询或明确以完全相同 ID/内容重试；不自动再投。 |
| 草案已受理，执行状态不明 | 原 conversation/turn/source 只读恢复；create/turn attempted 后不因 timeout、租期或重开重发。 |
| 已恢复原会话，原 turn 从未尝试 | 用户可明确“继续原请求”，沿既有 continue 与最后 POST 重验；只在 native 证明可继续时执行，不新建 source 或扣作另一份逻辑任务。 |
| 已有受限澄清，需要补充文本 | 用户明确提交新 turn；与继续未尝试原 turn 分开。旧结果与来源不改。 |
| 确认保存回执不明 | 先 preview 原 source，confirmed 后读同 plan；未确认可用原 request_id、source/digest/definition 显式重试。禁止先普通 save 兜底。 |
| context 正常到期、撤权或换 scope | App 统一恢复当前授权；到期期间同 scope 的已发动作只保留查证所需内存。撤权/换 scope 清除或隔离；迟到响应不得写入新页面。 |
| 正常重开、源聊天删除或冷空历史丢失 | 从真实会话/轮次重发现来源；不自动 submit/continue。保留未知/已删除事实；已确认计划按现有规则保留，不能新建替代 thread 伪装恢复。 |

读取采用有界请求、取消和已有事件驱动的刷新；若短轮询则有期限并在离页/失效时停止。关闭页面不等于取消已发 native 操作；运行停止沿原生 interrupt，不能杀进程。禁止无证据自动补消息、封口或制造终态。计划 grant/run 数本批新增应为 0，但草案正常会新增 conversation/turn/source/outbox，不能误把“零计划执行”验成“零草案记录”。

## 7. 真实 Provider 与额度

既有授权为**最多 12 次真实文本，已用 0；图片、商家/MCP 外部调用 0**。建议本批最多使用 **3 次实际 Provider 请求**，从原总额扣除，最多用满后保留至少 9 次用于后续执行/恢复/最终验收。不是新增额度。本轮规划使用 0 次。

先完成零调用检查，再经同一 canonical 候选 App 做真实验证；不另造 CLI 产品路径或假 Provider 结果。复用 Host `scripts/permission-smoke-meter.py` 的固定 `127.0.0.1:18083/v1` 验收通道，固定转发到既有 MiniMax-M3 Responses 服务；单批 ledger limit=3，跨正常重开沿用同一 ledger，不能重置或新建账本绕过上限。转发前扣数，失败/状态不明也占额度。台账只记 ID、计数和安全结果，正文与 key 不进入记录。

Host 最小修正只给草案 start/resume 合入经 native 验证的计数 Provider 地址、request/stream retries=0；共享普通路径的受管计数投影，**不合入 `auto_review.policy`，不改变 input_only/never、工具集合、MCP/skills 或受限工作目录**。不能从 renderer 注入 config。计数配置生效但服务不可用时不得退回直连；ordinary 非验收路径保持。这是计数通道接线，不建立新的产品权限模式或计费平台。

Host 源改动后审阅精确差异，再同步 Desktop `scheduled-host-build.candidate.json` 文件集/hash 并跑原校验；不能仅刷新 hash 掩盖其它源码变化，未涉及的起点文件需逐字核对。Runtime binary/manifest、公共 wire 和原 FEAT-152 提交引用保持。没有证据证明实际草案请求进入计数通道前，真实 Provider 继续 NOT RUN。

推荐真实路径：第一轮用正常合成任务明确缺少时间/时区，观察真实澄清；第二轮补齐字段，观察同一受限会话产生合法候选，编辑确认保存后正常退出/重开、查回同一 plan。第 3 次只用于有明确诊断的必要修正复验，不预定为机械重试。若模型输出不符合要求，原样记录安全错误、保留草稿并允许用户修正；不能靠放松 schema、截取任意 JSON、切普通聊天或自动循环生成来获得通过。三次用尽仍未闭环则报告具体阻塞和已交付部分，不宣称 4B 验收完成、不自动动用剩余 9 次。

## 8. 验证、交付与后续

1. 新旧私有 IPC 的 Rust/TS/schema conformance；普通 SQL15、候选 SQL23 正常读取/重开；旧迁移逐字保持。用途读取覆盖 task.read 但无 schedule.read 的普通用户；新来源查询覆盖原请求、未知及正常删除。
2. 前端检查预填不发送、已有文本/附件默认保留、路由/侧栏/深链用途识别、迟到响应、澄清新 turn、确认唯一及 source/digest 变化。只读回查、正常授权到期和用户取消/恢复用声明式组合验证，不主动制造网络故障。
3. Native/Host 定向检查：旧 create/turn 不误接草案、普通权限不改、无 implicit dispatch；原请求重复、确认重复和正常删除保持幂等；计数 config 在 start/resume 有效、缺失通道无直连，旧普通路径保持。使用正常临时库与本机 HTTP 声明式样例，和真实证据分开标记。
4. 按受影响仓运行 lint、类型/build、fmt、clippy、定向 Rust/Go race 检查与设计文档构建；已知三项 ChatPage 断言单独对照记录，修改波及的真实路径必须验证。不恢复 FEAT-137，不跑强杀、权限破坏、恶意资源/攻击 fixture；跳过项列原因和影响，不宣称 full-green。
5. 真实 canonical 原生 UI：亮/暗、1180×760 及实际内容视口、键盘/焦点、入口预填/取消、两轮澄清候选、表单确认、同 ID 管理卡、正常重开和原来源查证。零调用 UI 项先完成；第三次不是必须消耗。原生计数与产品库只读聚合核对草案产生、计划唯一、paused、grant/run=0，保留原墓碑和历史，不 seed 用户库。
6. 主任务完成与实施分离的结构化自审并报告：源码与契约、合成检查、真实 UI/Provider、计数、正常停止及剩余限制分别列出。全部 owned 进程正常退出；无法安全退出则保留所有权并报告，不强杀。

本批主要推进 AC-002，并回归 AC-001/003/007/010 的相关交互；不把局部证据等同十项 Must 同次 fresh run 或 D4。**4B 报告后停止。** 后续建议依次接计划有限授权/执行控制与完整历史，再完成电源/应用内更新及余下真实验收；具体下一批届时按源码和剩余额度规划。

## 9. 本轮方案审查记录

主任务完成只读源码复核和单独的反向场景审查，未调用子代理、未冒称独立人工批准。已将首次回执丢失、native 用途缺失、管理 context 不启动 Host、普通聊天权限兼容、确认表单复用、草案计数未接通和冷历史限制纳入方案。无需新数据库/Runtime 决策；Provider 真实能力仍为待验证事实。

本轮仅元仓方案/状态文档变更；五仓起点和最终文件校验、文档检查见[方案审查证据](evidence/phase-4b-plan-review-20260919.json)。检查结果以该证据实际记录为准，不构成 4B 实现或真实 Provider 通过。

方案检查结果：strict D0、元仓 lint、50/50 治理测试、Shell 语法、文档空白与 143 个本地链接通过；四个产品仓起点文件逐字保持，五仓 HEAD/branch/remotes 不变。首版链接检查器未解码旧 PDF 链接的 `%20` 而误报，修正检查器后通过，未修改 PDF 或原链接。当前没有未处理的方案定义阻断；Provider 资格与执行结果仍待实施验证。
