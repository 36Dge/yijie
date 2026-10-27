# FEAT-164 需求、交互与验收

> 当前口径：原主工作目录构建/日常入口及正常系统退出资格以[76](76-primary-workspace-execution.md)、[77](77-primary-system-quit-root-cause-and-plan.md)和[当前验收矩阵](current-acceptance-matrix.md)为准。当前源码为原`CrossBSD/yijie-desktop`，generation `20261028-02`；71—74保留为上一来源/清理历史。新来源三轮服务/模型目录/正常退出/数据后态通过，App历史界面因锁屏按Owner指示跳过，未记PASS；既有接受替代和永久移除范围保持。

## 第67/69号D5完成记录（历史，2026-10-27）

以下保留当时原文；其中旧提交、制品和“当前权威”不再代表现行来源。

当前权威[67](67-d5-entry-and-activation-implementation.md)：D5已按Owner明确批准的ADR-0022个人本机范围完成。新日常入口固定Desktop39b0fbe/原Home，默认启用Kimi K3.1 Pro；真实正常启用、暂停回退和同入口再次启用均通过，3次正常退出及完整后态通过。0模型验收调用，原历史/授权/账本/预占及dirty保留，仅本地提交不推送。G4/G5本机就绪与G6实际交付观察分别留证；不授权公网/云端/多人/签名发布。以下66及更早阶段按各自时点解释。

本文件仍是整项验收目标。全部AC在已接受的本地实现与验收范围内PASS，逐项证据见[当前验收矩阵](current-acceptance-matrix.md)及58、66、67；D1—D5个人本机切换现已完成。公开、云端、多人及签名发布不在本次批准范围。完整App正向never-sent仍采用Owner已接受的安全分层替代，不改写为实际执行。

### 第64号时点历史（非当前部署状态）

> 当前日常部署以[64](64-d3-controlled-migration-and-post-state-audit.md)为准：D1/D2及63前置修复保持，一次D3成功后停止，原日常Native已为SQL41，后态完整备份及旧业务行保持核对通过。D4尚未授权/启动，长期D5与local交付门禁口径仍待收口。58本地AC与替代证据保留，存储维护不等于日常启用。

## 业务规则

- BR-01：活动 Kimi 请求精确为 kimi-k3.1-pro；新 profile 不重用旧身份，不自动回退 K3 或 MiniMax。
- BR-02：分离历史已知身份、当前执行身份、目录定义。旧值可读但退役；retired-known 与执行结果 unknown 不混用。
- BR-03：原 operationId、profile、payload/digest 和原始执行事实不可改；经状态机证明的恢复/取消可以改变 delivery state。
- BR-04：旧会话先用新 operationID、旧 expected revision 发起选新模型，再以同 thread unsubscribe/resume 的完整回执提交新选择，最后才允许 turn。只读打开历史不自动切换或生成标题。
- BR-05：thread/read、status、cwd config/read不能证明线程有效 model。回执未确认保持 unknown；明确恢复是重新应用同一新模型配置，不称只读。
- BR-06：worker领取前、发送前检查退役准入；只读历史/回执/恢复查询不受执行禁令阻断；禁止旧操作被自动领取耗尽attempt。
- BR-07：旧Kimi计划通过领域事务暂停、revision提升、有效授权清除、future slots处理；新模型保存后重新授权；原run/grant/snapshot保持。
- BR-08：密钥、权限、逐次工具审批沿用。kimi-web不改名、不另存Key。
- BR-09：零K3出站从明确切换截止点开始；此前隐藏模型工作必须正常收敛。标题、Guardian、工具后续请求及启用的子代理纳入。

## 流程与UI状态

| 场景/状态 | 行为 |
|---|---|
| 新聊天idle | 默认新Kimi，MiniMax保留，沿原选择器/图标 |
| 启动loading | 原模型区域显示准备中；兼容和准入未完成不能发送 |
| empty | 无旧记录直接新身份，不发模型探测 |
| 旧会话idle | 历史保留；首次明确继续时说明后续使用新模型，再完成选择操作 |
| active/待批 | 等待正常结束，用户可按原流程停止；不切换运行中身份 |
| success | 同thread、新revision；收到持久确认后才显示切换完成 |
| 缺凭据/拒绝 | 明确不可用，沿现有配置入口；无第二份Key表单/自动充值 |
| error/unknown | 保留原请求和诊断；不能用新提交绕过仍未结清的旧操作 |
| retry | 完成回执只读返回；未决切换可明确重新应用原目标；业务重发须先安全结清旧操作再新operation |
| cancel | 仅有持久never-sent证明才可无删除地取消；已发/未知继续核对原状态 |
| 旧计划 | 提示模型升级需审阅，保留内容；保存新模型后重新授权 |
| 回退 | 兼容reader保持；仅停止新Kimi执行，MiniMax和历史仍可用 |

统一 ChatModelControl、useChatModels、composer草稿、ChatPage退出草案、计划表单及详情的业务状态文案。Owner于2026-10-26明确移除亮暗、键盘/焦点及最小窗口专项验收，这些项目不再属于本需求验收标准或完成门槛；不修改全局UI框架。

## Owner明确移出的验收项（2026-10-27）

搜索答案正确性（含本轮指定官方文档命中、是否给出确定答案的质量判定）从FEAT-164移除，记OWNER_EXCLUDED；不是延期，也不计为PASS，不再作为AC、S4/G3或最终交付门槛。原始搜索/模型结果与账本保留，不为此补试、增加检索工具或修改Runtime。原AC-008/009保留实际sources按契约传递、原生事实如实呈现、Key/审批/预算保护；不把质量排除解释为删除搜索接线或放宽安全边界。确认与结果见55及evidence/s4ab-owner-scope-exclusion.json。

## Owner接受的安全替代（2026-10-27）

Owner本轮明确接受57号never-sent分层证据：正常Repository API入队/领取且不启动sender，真实持久取消、正常重开和同一回执重放；再以实际Native输出经过生产parser/composable/control验证按钮和消息保持。原完整App/WebView正向取消仍NOT RUN，不删除该事实、不伪造样本。AC-005/010及S4/final使用这项已接受替代；取消证明、原operation、授权、数据保留和unknown不重发的不变量不变。确切授权见evidence/s4ae-owner-acceptance.json；其余完整App主路径仍使用真实既有证据，不由组件替代。

## Must AC追踪

| AC | 可判定行为 | 对应验证 |
|---|---|---|
| AC-001 | 活动目录只有新Kimi/原MiniMax，默认profile/model/max/1M精确 | BR-01；S1；TCONF-164-01；UI |
| AC-002 | 已知旧配置精确升级，保留Home/trust；未知漂移不覆盖，来源未就绪不激活 | S1；TCONF-164-01 |
| AC-003 | 三表原列值/PK/FK/CASCADE/nullable保持，旧migration不改；基础/models/连接器迁移路径可用 | S2；TCONF-164-02 |
| AC-004 | 原thread经新选择operation迁移；lost receipt保持unknown；明确恢复收敛；终态回执不重执行、不回退当前revision | S2；TCONF-164-02 |
| AC-005 | 普通/市场/专家/计划旧请求claim前和send前被阻止；never-sent取消不删chat；已发/未知不自动重发 | S2/S3；TCONF-164-02/03 |
| AC-006 | 旧计划暂停、旧grant失效、future slots收敛；重新授权可执行；历史run/MiniMax计划不变 | S3；TCONF-164-03 |
| AC-007 | 普通/标题/专家/草案/计划/压缩/允许子代理/Guardian出站符合effective身份；退役slug不从辅助入口复活 | S1/S4；TCONF-164-01/04 |
| AC-008 | 文本/图片/工具参数/回灌/原生搜索sources完整；input-only无执行工具；failed/incomplete/取消如实显示 | S4；TCONF-164-04；真实主路径 |
| AC-009 | 网页工具共享Key/审批保持；普通恢复零业务调用；模型/搜索/标题/审批分别计量不越预算 | S4；TCONF-164-04 |
| AC-010 | 同源构建正常启停和重开；模型/退役/恢复业务状态准确；兼容回退读新旧数据、不恢复K3调用；核心、业务状态与正常退出分别给出结论（不含已移除的外观专项） | S4；TCONF-164-04；final E2E |

实际启用组合已完成调查及验证：四组合来源见[28](28-s4-expert-media-auxiliary.md)，标题、input-only草案、专家、允许的子代理、Guardian及显式/自动压缩见[48](48-retained-runtime-qualification-and-scope-update.md)，当前来源绑定见[当前验收矩阵](current-acceptance-matrix.md)。未启用的子代理/记忆/review入口只证明保持禁用，不为验收扩权。普通本机provider可验证长上下文路由，但不冒称供应商能力或跑满1M的真实质量评测通过；FEAT-163的独立进度问题不由本需求关闭。
