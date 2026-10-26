# FEAT-164 需求、交互与验收

本需求已获Owner授权实施；本文件仍是整项验收目标。全部AC在已接受的本地实现与验收范围内PASS，逐项证据见[当前验收矩阵](current-acceptance-matrix.md)和58；日常迁移/启用与发布未执行，不能把代码完成等同日常切换完成。

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

未启用的子代理/记忆/review入口只证明保持禁用，不为验收扩权。实际启用组合未调查，不能先写N/A。普通本机provider可验证长上下文路由，但不冒称供应商能力/真实质量通过。FEAT-163的进度和空操作问题保持独立未关闭。
