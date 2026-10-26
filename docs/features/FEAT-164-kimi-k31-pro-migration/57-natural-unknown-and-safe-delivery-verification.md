# FEAT-164 S4AD：自然unknown归因、恢复保护与安全取消链

2026-10-27。已完成56号后续：用当前源码构建独立原隔离identity候选，实际读取自然unknown、执行一次明确恢复核对及旧草案刷新；另以正常Native入队和领取阶段验证never-sent取消、重开与相同回执，并用实际Native输出验证生产前端链。**模型HTTP新增0（真实0、本机0），日常库未打开或迁移，Runtime核心/补丁零修改。**

结论分开：自然unknown的安全拒绝已在实际App验证；该记录未恢复为ready。never-sent正向链在Native和实际前端组件中通过，尚非完整App/WebView自然取消演练。S4完整门禁仍pending，不伪造通过。

## 复审结论与本质原因

原隔离库为`com.yijie.ai.feat164-kimi-k31-r1/demo-fast-model-candidate-v1`，SQL41。先确认正常停止/无句柄，完整复制5530文件，所有SQL与bbolt归因均只读完整副本，没有打开日常库。

自然未决会话`01a1739c-aaca-77a0-9ff5-e17edc67b8ae`，原操作`f38666dc-d2d8-4101-b498-eccf3045b6dd`，K31→MiniMax、expected revision1。**Native有format2意图、phase=unknown，Host没有该操作回执。** 早先口述“可能没有Native v2意图”已被本轮事实否定，初步猜测不作为结论。

历史原因已在35号实际复现：Native先通过既有v2模型配置准入并记下派发意图，旧Host仍仅接受purposeOrdinary，拒绝了已完成的市场/专家线程，早于Host操作持久化。Host090c2dbe的配对准入修复已经进入当前4f；本轮无需重新修改Runtime或复制该修复。保留原unknown不是当前Runtime又坏了。

当前`model_recovery::recovery_action`只允许本地prepared且Host无记录时首次发送；本地unknown/dispatched而Host缺回执时必须拒绝。历史归因不能充当新的可信未发送凭据，不能据此清空原操作、换ID或重发。`recoveryAvailable`表示存在可核对的本地v2意图，不保证远端回执足以恢复。

另一条自然queued记录属于input-only定时草案`01a17315-c3f9-7e93-a6f8-56a7b7876520`，不是普通消息。它没有delivery proof；全库现有delivery proof均已有发送尝试，无自然never-sent正例。不得把queued、Host404或缺proof当作未发送，也不能把草案纳入普通取消接口。

## 实际App链

当前源码ea8763d/Host4f966e8/Contractsc5d1383/Runtime11fd-r5/Connectorscc56/Skills595，在新`feat164-s4ad-qualification-20261027`经canonical prepare-only构建再按同一receipt重开；未覆盖旧App。119文件，App SHA `4b0ec55e6903bc6aad790a4715d485456ebf0241d10ff6c99e51d67c6aa65e39`，receipt `bbb09fd92d66f808180ee4d07331596b93650299be642159d4285b9d342fa744`。使用既有本机端点及合成Key，无真实凭据。

1. 原unknown会话四轮历史、正常中断内容和媒体均可读；模型仍K31，发送禁用。
2. 只点击一次“恢复原切换”：显示“原切换尚未恢复，请刷新核对；不会发送新的对话请求。”，未换ID、未变模型、未新增模型请求。
3. 旧input-only草案保持“提交结果待确认”与禁发；点击“刷新草案状态”后仍保留原请求，没有普通取消按钮、没有重派发。
4. 回到原unknown会话，原待核实状态与禁发保持。随后正常⌘Q exit0，fixture正常shutdown204。完整停止副本重新核对，Native原意图/选择、Host操作库、所有投递证明、旧grant/run原样保持；没有新Host操作或模型调用。

这是**PASS_SAFE_REFUSAL**，不是“成功恢复旧unknown”。未恢复为ready正是缺可信回执情况下的正确保护，不重复点击同一失败动作。

## never-sent正向安全验证

本轮唯一代码改动在独立测试工作树`feat164-s4ad-tests-20261027/yijie-desktop`，本地提交`4e1f1f980d148a6b46e21e68eb508caa4da5dae4`，共3文件：delivery/tests.rs、ChatDeliveryControl.retained.test.ts、对应验证说明。产品源码、生成物、schema、依赖、Runtime补丁均不变，增量contract-impact=none；实际App仍ea产品，不伪称重建测试提交App。

新精确opt-in Native测试只调用正常Repository API：新库注册合成工作空间→接受普通消息→正常领取出站队列但尚未启动sender→读取真实never_sent证明→取消→正常关闭/重开→重放同一取消回执。没有向已有库INSERT伪造状态、没有注入故障/断链、没有暂停或杀掉业务进程。原操作ID/输入fingerprint、消息及会话保持，三种dispatch计数均0，取消后不能再次领取。测试目录完整保留，不使用旧Fixture的自动删除。

随后读取这个实际生成的result.json，通过生产chatDeliveryClient解析、useChatDelivery和挂载的ChatDeliveryControl验证：只读刷新不取消；点击取消沿原session/operation；回执验证通过后显示“原消息已保留”，按钮撤下且只取消一次。仅IPC传输以已记录的Native输出重放，明确不是实际Tauri命令/WebView。

Native精确1项PASS/0ignored；前端精确1项PASS/0skip。cargo fmt、严格lib/bins/tests Clippy、pnpm lint、pnpm build和docs:build均通过。未宣称全仓测试通过；以前已通过且未改变的广泛/攻击类套件未重复运行。完整自然App正向never-sent取消仍NOT RUN，不用这两个安全层级冒充。

## 数据与清理复核

本轮发现“71表全部旧行完全不变”这一粗断言不适用，原始差异与后续字段复核分别保留：

- 69张表的全部旧行保持；计划表仅next_at/cursor_at推进。关闭计划跨过旧时间槽，该槽planned→skipped_paused并记录missed_through，另追加未来planned槽，符合schedules/store.rs现有正常时钟处理。
- 计划内容/规则/state/revision/授权指针、全部grant/run/reservation、模型选择与v2意图、投递证明、outbox状态完全保持；没有新运行或授权。正常退出增加1条stopped-generation。
- Host19会话中14条仅updated_at变化，其余字段与所有非session桶逐字相同；原unknown的Host回执仍不存在，未添加或删除任何Host键。
- 四Runtime库自然WAL0、完整副本只读integrity ok；无项目服务/句柄残留。未手工checkpoint、删除/截断WAL、强杀或修改权限。
- 6790份原隔离活动数据外保护文件、500份既有dirty、7份账本/快照逐字保持，混合memory仅精确追加本轮段落。累计真实13、45元cap、29.740299保守累计与两份14.188544预占不动。旧日常候选和S4AC prepare-only119文件保持。

一次读取辅助脚本的相对路径错误在运行前停止，改为绝对路径后执行；只读inventory中“unsettled”命名过宽，最终按实际queued/uncertain和用途重新分类，未把已完成消息误计未决。所有这些属于审计记录纠正，无产品修复或新开放失败熔断。

## 当前门禁与下一步

56中的“自然unknown完整App未观察”缺口现已补为实际安全拒绝证据；不能继续把原f386当作可通过重复尝试结清的待办。可以恢复的v2原操作正向路径仍由既有Native/Host/r5边界证据支撑，不冒称本轮自然unknown恢复成功。

剩余明确边界只有完整App正向never-sent取消未执行：当前自然库无该正例，安全Native+生产消费链替代证据已经可审查。下一步应审阅并明确接受这组安全替代证据的验收边界，或提出具体、正常且不制造故障的App可达方案；不能反复运行相同测试、添加故障注入入口或篡改原库制造样本。完整S4/TCONF04/core及业务状态门禁暂不晋升。当前正常teardown PASS。

日常候选仍为56的prepare-only合格制品，不启动、不打开/迁移日常库。搜索答案正确性、亮暗/键盘/最小窗口专项仍OWNER_EXCLUDED。任何后续Runtime核心/补丁修改先提具体方案。所有提交仅本地，不推送。

证据索引：evidence/s4ad-audit-index.json。完整私有副本与新测试数据保留在feat164-s4ad-audit-20261027，密钥和数据库不提交。

治理校验：audit-claims、strict、元仓lint、53项测试及7份Shell语法通过；S4检查仅按预期报告vertical/TCONF未完整的5项，不绕过门禁。
