# ADR-0020: 本地定时任务权威、Codex 执行复用与正常生命周期

## 最新范围补充（2026-09-23）

用户明确要求实现FEAT-155剩余需求，并指定“防自动空闲睡眠，这个功能现在明确不实现”。DEC-155-07中的该子项因此OWNER_EXCLUDED；系统通知仍延期，应用内重要更新保留。用户随后明确移除“睡眠后停止发送”要求及验收；本轮不新增该能力，不扩展成普通生命周期重构。不是平台能力验收通过，也不扩大退出后运行范围。当前实施以[47定义](../features/FEAT-155-desktop-scheduled-tasks/47-remaining-delivery-plan.md)为准；其下原决定保留历史来源。

## 状态

**Accepted** — 2026-09-18。段成威明确接受推荐方案并授权本地实施，允许超过16小时，接受系统通知延期；2026-09-23另移除防自动空闲睡眠及睡眠后停止发送。授权原文和当前文本验收预算见[04用户确认](../features/FEAT-155-desktop-scheduled-tasks/04-owner-approval-and-implementation.md)。其余未授权的Git提交/推送/发布/生产操作不扩张。

Owner：段成威。关联 [FEAT-155](../features/FEAT-155-desktop-scheduled-tasks/00-feature-brief.md)。调查证据、完整算法边界、方案比较和工作量见 [Q-01技术决策稿](../features/FEAT-155-desktop-scheduled-tasks/03-scheduling-and-codex-reuse-decision.md)。

## 背景

FEAT-155要求两种创建方式、三种聊天运行目标、定时/手动运行、历史和完整对话及应用内重要更新。早期电源子项已按顶部用户决定排除。固定yijie-codex0.144.6的stable method与源码有thread/turn、审批、结构化输出约束，未提供完整日历计划/触发/恢复服务。API scheduler和Host cloud-runner目前为占位。

ADR-0013/0014已明确Desktop本地加密产品数据、Host适配映射和Runtime执行事实的职责；ADR-0018要求local免登录直达和退出时停止受管Host。它们没有自动批准新增计划主状态、后台授权、受管工作目录、平台电源能力或费用策略。不能将这些新增职责包装成“已有Codex定时器”。

## Contract Impact

FEAT-155整体及本轮原生候选均按`breaking`保守审查；同库schema升级、新workspace来源及Runtime精确产物/schema pin需分别验证。最初只读调查为`none`，不代表后续实现无契约影响。DEC-155-09沿Runtime权威源码/稳定schema → Contracts派生投影 → Host消费，保留旧产物和普通路径；本地候选证据不等同发布或生产兼容批准。

## 已接受决策

| 编号 | 拟议决定 |
|---|---|
| DEC-155-01 | Desktop Rust/native拥有本机计划、occurrence和最小run投递账本；共用现有SQLCipher和串行worker。Host仅保留执行映射/幂等恢复，Codex仍决定执行ID/结果；不新增API scheduler/Redis或常驻进程。 |
| DEC-155-02 | 新聊天采用明确标注、native创建/校验的应用受管工作目录引用；已有聊天沿用原项目引用。新增workspace来源由契约定义，不冒充用户bookmark、不隐选首个目录。 |
| DEC-155-03 | 日历计算复用成熟库，候选rrule0.14.0须后续锁定和资格核对；产品只暴露有限频率。正常awake延迟窗口候选60秒，退出/睡眠不补跑，DST重复仅一次、缺失时刻跳过。 |
| DEC-155-04 | 同计划/同会话互斥、全局最多1个定时run未结束。用明确前后台预约避免未证实的多流并发；unknown不自动重投。前台交互收窄或另行扩展多会话观察须Owner选择。 |
| DEC-155-05 | 后台每次派发从native authority重新核权，不缓存renderer context。首期自动计划Ask，不切Auto/Full、不代答审批；需有按计划/验收授权的有限预算与期限。 |
| DEC-155-06 | 对话通过stable outputSchema生成受限计划草案/澄清问题，native严格校验，用户确认后调用与表单同一保存事务。模型不能保存成功自证，不新增experimental工具服务。 |
| DEC-155-07 | 2026-09-23：防自动空闲睡眠及睡眠后停止发送OWNER_EXCLUDED；应用内重要更新保留，系统通知首期延期；不承诺休眠/关机/退出后运行。 |
| DEC-155-08 | occurrence/run与既有outbox在同库同事务衔接，先兼容reader后启用writer；回退保留新格式并关闭新投递，采用兼容候选/forward repair，不降级旧binary写新DB。 |

本地边界仅本人本机、App运行且资源ready，关闭应用/手动睡眠/合盖/关机不保证执行。Vue无计时与数据权威；不得用sleep工具维持长turn充当持久调度。

## 必须保留的不变量

- plan、run、conversation/task、session、native thread/turn和operation各有独立身份；不能把plan_id直接当每次Host task_id。
- 一个已确认逻辑槽/手动请求最多一次自动投递尝试；Runtime无端到端幂等事务，结果不确定则明确unknown并阻断自动续投，不承诺exactly-once。
- Host新增只读创建/投递状态查询只返回已知事实：会话创建按既有task_id、turn按session/operation_id查询；历史partial、idle/notLoaded或缺字段不能证明未执行。用户承认历史结果不确定不能直接释放执行预约，须有原生终态/正常中断或旧受管generation正常关闭等事实。
- 保存计划与未来具体工具批准分离，权限丢失/凭据失效/预算缺失即阻断；FEAT-137永久终止。
- 在可取消退出请求阶段拦截退出，先停止新claim、保管未决事实、停止共享Coordinator、释放平台资源，再正常停止Host/Runtime；无法安全停止则保留进程和恢复入口为STOP_PENDING，不进入最终Exit、不强杀。
- 删除计划不级联删除对话/Artifact；删除聊天仍服从ADR-0014并清理定时索引中的可恢复关联，不能靠计划记录复活正文。
- 不改旧migration、复制用户DB或清空数据试错；涉及重要用户数据或不可逆迁移时适用生产治理升级条件。

## 备选方案

- 直接复用Runtime完整调度：当前固定协议/源码缺该能力，不能作为接入承诺。
- API scheduler或云runner：新增部署/身份/离线交付和运行位置，且不能自动解决本机已睡眠/退出的问题，超出本地最小边界。
- Host持计划主库或保持常驻：与薄适配和现有退出职责冲突。
- Vue timer或OS cron直调CLI：绕开原产品投递/审批/恢复链，不采用。
- 新experimental dynamic tool/MCP服务创建计划：比受限outputSchema草案多一套工具信任/回调/生命周期；仅作为未来独立审议方案。

## 影响与未验证风险

主要实现影响为Desktop、Host、Contracts；DEC-155-09补充最小Runtime原生限制，保持固定上游来源及旧产物，API/Infra本期不新增服务。新native正常退出owner、工作目录来源、后台授权、恢复查询和日历库属于新增职责；电源子项已排除。

只读审计未验证Provider对复杂草案schema的输出质量、rrule依赖组合/DST实际行为、macOS打包唤醒/通知或端到端恢复；全部需在获准实施后安全验证。前后台并发的保守预约会影响发送体验，必须明示。

完整设计最初估20–32小时（不含系统通知），用户已明确批准超过16小时。时间盒不再阻断FEAT-155；除两个明确排除的电源子项外，不缩减其它Must。

## 早期调查动作记录（已由分阶段报告覆盖，不是当前待批准事项）

- [ ] Owner确认DEC-155-01至08，明确Q-02至Q-04及范围/时间盒取舍。
- [ ] 被接受后再同步受影响仓库规则、架构与安全/回退说明，保持已有历史结论。
- [ ] 明确D0和单独实施授权；当前仅允许文档调查。
- [ ] source-first形成实际契约、兼容reader和必要依赖审查，再进行实现。
- [ ] 获准预算和数据范围后完成正常focused/fresh真实验收；不执行用户禁止的故障/攻击注入。

2026-09-18 Owner已明确接受本ADR推荐方案，当前按04确认记录实施；以上调查时的未验证风险继续存在，接受决策不代表D4通过。系统通知延期、16小时例外和实施预算以04为准。


## DEC-155-09：受限草案的最小原生能力（2026-09-19补充）

状态：在本地实施授权内采用。用户在27资格报告后明确要求“最终目标实现并完成feat-155需求”，并“对阻塞的问题做深度思考，实施解决方案，直到解决”。这覆盖解决已查明阻塞所必需的最小Runtime能力、同源契约和Host接入；具体技术方案由Codex在此范围内选择，不冒称用户逐字段审批或独立人工评审。执行定义见[28](../features/FEAT-155-desktop-scheduled-tasks/28-draft-qualification-unblock-execution.md)。它取代此前“Runtime仅只读”的本批限制，不扩大产品范围。

- 同一固定上游`5d1fbf26c43abc65a203928b2e31561cb039e06d`、现役FEAT-126/136两补丁之上新增通用`input_only`限制；不包含定时/电商业务，不恢复FEAT-137，不改变普通Ask/Auto/Full模式。
- 在原生初始化、输入准入、权限更新、工具注册及模型输出处理处落实约束；只保留显式文本、该线程原历史、内部持久化和既有文本Provider。额外指令发现、skills/hooks/plugins/MCP、工具读写和工具网络全部关闭；非文本输出直接失败，不能经工具错误触发额外模型续调。
- `thread/inputOnlyPolicy/read`读取已装载线程的实际策略。Host结合精确二进制/manifest、受管配置、当前generation、thread/cwd及持久用途核验，每次执行重验，正常退出使资格失效，恢复重新取证。
- 使用canonical脚本在项目独立输出目录生成候选，保留原FEAT-136二进制及历史源码/协议。Contracts机械生成Go/schema/pin，Host沿原Manager/stdio/thread/turn消费；不新增Provider产品通道、服务或Runtime实例模型。
- 激活顺序为候选Runtime → 同源Contracts → Host；旧Runtime可继续普通聊天，草案缺证据则拒绝。回退停止草案新生产并保留兼容reader/历史，不降级数据库。此补充不自动激活Desktop或迁移日常库。
- 最终记录分别判定原生限制、Host消费、真实Provider资格、完整产品装配和D4。零真实调用的本机HTTP合成Provider检查只证明原生链路，不能替代真实MiniMax验收。
