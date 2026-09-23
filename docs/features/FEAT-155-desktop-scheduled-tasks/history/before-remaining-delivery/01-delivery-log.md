# FEAT-155 需求调查与后续交付记录

2026-09-23当前授权：用户要求实现剩余需求，并明确**防自动空闲睡眠不实现（OWNER_EXCLUDED）**；系统通知保持延期，“睡眠后停止发送”也由用户随后明确排除；应用内重要更新和正常退出/重开保留。执行范围与验收口径见[47实施定义](47-remaining-delivery-plan.md)。当前仍10/14、余4，普通15/5、候选26/6；实现和最终验收进行中。下方旧“唤醒保留”和阶段停止描述属于历史，不覆盖本次明确决定。

2026-09-23当前交付：**4D-1执行记录真实时间与耗时闭环完成，报告后停止**，见[45实施报告](45-phase-4d-1-execution-timing-report.md)。独立只读契约、Host投影、SQL26缓存/有界补读及列表详情已接通；固定Runtime热读/冷读、后台历史补读、亮暗/最小窗口/键盘及正常重开通过。普通15/5保持，候选26/6，日常库未迁移。真实本批0，追加2次授权后累计10/14、余4次；声明式本机Provider2/2。130项原生及28项前端定向检查通过，全量门禁/安全未执行项单列；全部Must/D4未完成，不自动进入下一批。下方旧状态保留历史语义。

2026-09-23下一步方案：建议只实施[44：4D-1执行记录真实时间与耗时闭环](44-phase-4d-1-execution-timing-plan.md)。固定Runtime已有稳定时间字段；拟补独立只读Host查询、候选SQL26时间事实及列表/详情，保持旧聊天协议和执行授权。普通15/5、Host候选6；真实调用0，累计仍10/12余2次。**本轮仅只读调查与方案保存，产品未改、服务未启动、数据库未读取或迁移；4D-1尚未实施，完整Must/D4未完成。** 4C-3已由43收口，下方记录保持历史语义。

2026-09-23当前交付：**4C-3视觉与交互已收口，报告后停止**，见[43收口报告](43-phase-4c-3-ui-closure-report.md)。本轮确认原生弹层及亮暗可见，修正长差异按钮被挤出可视区和详情→重跑焦点交接；最小窗口、键盘、取消无副作用、结果定位和正常重开通过。产品仅一个Vue文件变化，真实及本机Provider请求均0，累计仍10/12余2次；普通15/5、候选25/6，日常库未迁移。41的执行证据与43的UI证据分别保留，完整Must/D4未完成，不自动进入下一批。下方旧阶段记录保持历史语义。

2026-09-23下一步方案：建议只执行[42：4C-3视觉与交互收口](42-phase-4c-3-ui-closure-plan.md)，先定位UI-4C3-01的渲染/捕获差异，再最小修正弹层、暗色或焦点，完成实际原生亮暗/1180×760/键盘与取消无副作用核验后报告停止。普通15/5、候选25/6，真实调用0，累计仍10/12余2次。**本轮仅只读源码复核与方案保存，未实施、未启动服务；4C-3视觉与完整D4仍未通过。** 下方41及更早记录保持历史语义。

2026-09-23当前交付：**4C-3代码及真实重跑闭环已完成，视觉验收待核对，本轮停止。** 见[41实施报告](41-phase-4c-3-single-run-and-rerun-report.md)。单次授权与自动计划独立；私有IPC、候选SQL25、立即运行/独立重跑及精确结果定位已接通。真实文本本批1次成功，累计10/12、余2次；普通15/5、候选25/6，日常库未迁移。确认框截图与可访问性树不一致，暗色捕获也未完整更新，不能宣布视觉或4C-3全部验收通过；等待实际可见性核对。完整Must与D4仍未完成，不自动进入下一批。下方旧阶段结论保持历史语义。

2026-09-23下一步方案：建议只实施[40：4C-3单次执行授权与独立重跑闭环](40-phase-4c-3-single-run-and-rerun-plan.md)。先分离本次单次授权与自动计划授权，再开放已开启/暂停/已完成计划的立即运行及历史差异确认重跑；复用原事务，候选拟SQL25/Host6，普通15/5保持。建议最多1次真实文本，完成报告后停止。**本轮只读调查和方案设计，产品未改、服务未启动、数据库未迁移，实际仍9/12、余3次；完整Must与D4未完成。** 下方阶段记录保持历史含义。

2026-09-23当前交付：**4C-2 有限授权、自动触发与暂停闭环已完成并停止**，见[39实施报告](39-phase-4c-2-automatic-execution-report.md)。SQL24仅追加自动确认标记，旧记录不回填；逐触发原生核权、正常重开后的未来调度、有限确认/查证及暂停已接通。真实自动请求1次成功，累计9/12、余3次；普通15/5、候选24/6，日常库未迁移。定向检查与实际UI闭环通过，全量测试的既有门禁和安全跳过限制在报告单列。独立重跑、历史时钟、电源/应用内更新未推进，完整Must及D4仍未完成。下方旧“当前/下一步”保留历史语义。

2026-09-22下一步方案：建议只实施[38：4C-2有限授权、自动触发与暂停闭环](38-phase-4c-2-automatic-execution-plan.md)。补enable只读回执、逐触发原生准入、正常重开的未来自动装配和有限确认UI；为旧候选不静默激活，推荐最小SQL24追加自动确认版本，旧记录不回填。普通15/5保持，候选拟24/6。建议最多使用剩余4次中的1次真实文本，完成报告后停止；重跑、历史时钟、电源/应用内更新另批。**本轮仅方案，未实现、未启动服务、未调用模型，累计仍8/12、余4次；完整Must与D4未完成。** 下方阶段记录保留其历史语义。

2026-09-22当前交付：**4C-1 有限授权、手动运行与结果定位已完成并停止**，见[37实施报告](37-phase-4c-1-manual-execution-report.md)。仅手动准入、两类回执与普通Ask资格闭合；三种目标均有真实completed，共3次completed、1次传输失败记账；追加授权中仅使用1次，累计8/12、余4次。正常重开与精确轮次定位通过，普通15/5、候选23/6保持；无日常库迁移，不进入自动、重跑、唤醒或通知。完整Must及D4仍未完成。下方旧“当前/下一步”为历史记录。

2026-09-19下一步方案：建议只实施[36：4C-1有限授权、手动运行与结果定位](36-phase-4c-1-manual-execution-plan.md)。先补仅手动原生准入、grant/manual原请求查证和普通Ask资格，再接一次手动确认、失效收尾及原run/对话定位。普通15/5、候选23/6保持；建议最多使用剩余8次中的3次真实文本，完成报告后停止。自动触发、重跑和电源/通知另批。本轮仅只读调查与文档规划，产品代码未改，实际仍4/12，全部Must的整体fresh run及D4未完成。

2026-09-19当前交付：**4B 对话创建与草案确认闭环已完成并停止**，见[35实施报告](35-phase-4b-conversation-draft-implementation-report.md)。真实澄清、候选、编辑确认、唯一暂停保存及正常重开已通过；普通15/5、候选23/6，无执行激活或日常库迁移。真实文本累计4/12、剩余8次；本批追加授权后上限5次，实际用4次。全部Must的整体fresh run和D4仍未完成，不自动进入4C。下方旧“当前/下一步”保留阶段历史。

2026-09-19下一步方案：建议只实施[34：4B对话创建与草案确认闭环](34-phase-4b-conversation-draft-implementation-plan.md)。先补原生用途/原请求查证和草案验收计数，再接预填、澄清、摘要确认与唯一暂停保存；零调用检查后最多使用既有12次额度中的3次文本做真实UI验证。普通15/5、候选23/6，无新迁移或Runtime修改；完成后报告停止。本轮仅规划，四个产品仓未改，实际仍0/12，全部Must及D4未完成。

2026-09-19当前交付：**4A 管理页面与手动保存闭环已完成并停止**，见[33实施报告](33-phase-4a-management-ui-implementation-report.md)。原生暂停保存/编辑/删除、正常重开、亮暗/最小窗口及键盘已验证；普通15/5、候选23/6，模型0/12，无日常库迁移。后续4B未开始；全部Must和D4仍未完成。以下旧“当前/下一步”保留阶段历史。

2026-09-19下一步建议：仅实施[32：4A管理页面与手动保存闭环](32-phase-4a-management-ui-implementation-plan.md)。先补页面必需的查询、共享管理context及管理写回执；为真实创建时间排序推荐最小候选SQL23，旧时间保持未知，普通目标15/Host5及候选Host6保持。交付两Tab、手动保存paused计划和只读历史后报告停止；本轮只读规划，产品代码未改，0/12、全部Must pending和D4 NOT RUN保持。

2026-09-19当前交付：**3C-3B3B原生装配与草案恢复已完成并停止**，见[31实施报告](31-phase-3c-3b-3b-implementation-report.md)。普通15/5、候选22/6及真实文本0/12保持；恢复不自动POST，来源确认只存paused。固定Runtime的冷空历史仍可能不可恢复，真实Provider、页面/唤醒和完整D4留后续。下方旧状态保留阶段历史。

2026-09-19下一步方案：建议只实施[30：3C-3B3B原生装配与草案恢复](30-phase-3c-3b-3b-implementation-plan.md)。新增草案专用只读mapping、统一原生候选与最后POST准入、attempted只读恢复、来源重发现和唯一确认，零真实调用验证后报告停止。本轮只读审查并保存方案，未开始产品实现；29的新候选Runtime资格结论保持，普通15/5、候选22/6、0/12和D4 NOT RUN保持。以下旧“当前/下一步”保留阶段历史。

2026-09-19当前交付：受限草案Runtime资格阻塞已在独立本地候选中解决，见[29实施报告](29-draft-runtime-unblock-report.md)。新增原生input-only限制和stable策略回执，经同源Contracts接入原Host；真实候选的创建、连续文本turn、正常退出重开/恢复与普通会话共存通过。普通Desktop15/Host5、候选22/6保持，日常库未迁移；模型0/12，Provider及完整产品D4仍NOT RUN。下一步回到既定B3B原生装配与草案恢复，再进入页面和最终验收。下方旧“当前/下一步”保留阶段历史。

2026-09-19当前交付：用户授权的3C-3B3A资格调查已收口，结论 **NOT QUALIFIED**，见[27资格报告](27-phase-3c-3b-3a-qualification-report.md)。固定产物/源码/267份stable schema来源吻合；实际配置继承和最终权限/工具证据不能闭合，第三步Host修正条件不成立，保留禁发。11项Host定向race回归及scoped vet通过；未改四个产品仓、未启动真实服务、未迁移日常库、未使用模型额度。DEC-155-09仅建议单独评审最小原生受限能力，未批准或实施；已停止，不自动进入B3B/页面。普通15/5、候选22/6、0/12及D4 NOT RUN保持。以下旧“当前/下一步”均为阶段历史。

2026-09-19下一步建议：仅执行[26：3C-3B3A受限草案执行资格收口](26-phase-3c-3b-3a-qualification-plan.md)，先判定固定Runtime的stable能力能否满足既定边界，再做可证成的最小Host修正；证据不足则交付具体决策并保持禁发。B1/B2结果仍以25为准，本轮没有实施、产品测试或真实调用；普通15/5、候选22/6、文本0/12及D4 NOT RUN保持。

2026-09-19当前交付：本轮授权的3C-3B1与3C-3B2候选实现及零真实调用组合检查完成，见[25实施报告](25-phase-3c-3b-implementation-report.md)。普通Desktop15/Host5，候选22/6；实际Manager因有效策略未具备资格拒绝真实草案发送。已停止，不进入页面/真实激活；0/12、Must pending和D4 NOT RUN保持。下方旧状态为阶段历史。

> 下一步方案：[11契约校验收口](11-phase-3a-contract-closure-plan.md)。本轮仅规划；先消除通用lint失败，收尾报告后停止，再进入3B。

> 当前：前两阶段及本轮授权的3A已实施，3A结果与检查限制见[10](10-phase-3a-implementation-report.md)；已停止，未进入3B/3C。下文先前只读/未实施记录均保留原阶段含义，不代表最新状态。

追加调查入口：[03调度机制与Codex复用边界](03-scheduling-and-codex-reuse-decision.md)与[Proposed ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)。下文§1—6保留初次起草阶段记录；后续Q-01结论与状态以§7及03为准。

## 1. 只读工程事实与仓库基线

按 [repos.yaml](../../../repos.yaml) 识别仓库；已读取元仓 AGENTS、[长期协作记忆](../../dev/codex-project-memory.md)、[交付手册](../../dev/codex-feature-delivery/HANDBOOK.md)的适用 demo_fast 流程、[质量门禁](../../dev/codex-feature-delivery/QUALITY_GATES.md)、[Contract First](../../dev/contract-first.md)、ADR-0017/0018、产品范围，以及所查兄弟仓的规则和相关源码。UI按 Desktop 2.1.0 当前规范，不套用过时的组件未迁移描述。

2026-09-18 初始 Git 检查：以下七仓工作树均 clean；本轮只在元仓新建本包。HEAD 是只读调查时的源码基线，不是 FEAT-155 发布版本、consumer pin 或已获验证的组合。

| Repository | Branch | HEAD | 本需求关系 |
|---|---|---|---|
| yijie | chore/retirement-baseline-20260905 | `2f616f4d24c001812c6279a520ba69ea9875247e` | 本轮唯一写入仓：需求治理 |
| yijie-desktop | chore/retirement-baseline-20260905 | `4a8a67bec4903624ca98a1098572fa26f3a20849` | 未来管理页、native边界、草稿/聊天/历史消费 |
| yijie-agent-host | chore/retirement-baseline-20260905 | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` | 原生执行/审批适配与运行关联；不默认承接业务计划主库 |
| yijie-contracts | chore/retirement-baseline-20260905 | `db4458fe94572c4df41a114005d54a049bb79b1f` | 未来易界共享协议权威/Runtime兼容投影 |
| yijie-codex | chore/retirement-baseline-20260905 | `6c1ad767f0997845b8258a1c452fd4eb7577579f` | 只读核对可复用上游；本包不授权patch/升级 |
| yijie-api | feat/feat-126-foundation-closure | `041f40c69919e81ec72ccee4ea6dbb3ea012142d` | scheduler占位与服务边界调查；是否参与local方案由Q-01决定 |
| yijie-infra | feat/feat-126-s10e | `66b481552eb76d46b00875ac27794ed8e1eb504a` | 条件影响：只有确认新增启动依赖后才参与；当前不改配置 |

各仓 origin fetch/push 为 `https://github.com/36Dge/<Repository>.git`；Codex 另有 upstream fetch `https://github.com/openai/codex.git`、push `DISABLED`。未 fetch/pull/checkout/reset，未改分支/远端。未修改其它 FEAT 的历史、批准或验证结论。

## 2. 真实代码入口与复用清单

下列行号用于本次基线定位；后续若源码移动应按符号重查，不能把本表视为运行验证。

| 编号 | 已观察事实与源码定位 | 需求约束 |
|---|---|---|
| E01 | Desktop `src/navigation/app-nav.ts:72` 定时菜单 disabled；`src/router/index.ts:25,75` 无定时页面 | 是已有导航占位，不是已完成页面；保留FEAT-130导航位置 |
| E02 | Desktop `src/authorization/app-permission-policy.ts:18`、`src-tauri/src/local_profile.rs:38` 与 Contracts `openapi/public/public.yaml:577` 含 schedule.read | 仅能证明读取/导航能力登记；不能代替写/执行授权与实际后端 |
| E03 | Desktop `src/pages/chat/ChatPage.vue:73` 按new/session分开草稿；`:330`后发送才createSession/submitTurn，`:369`进入会话；Router`:101`为/chat/:sessionId | 对话创建只预填，发送沿原链；完整对话跳转复用稳定会话ID |
| E04 | Desktop `src-tauri/src/chat/migrations.rs:34,101,106` schema15及native14/格式15；`database.rs:794`相关数据库读写 | 使用加密产品记录，不能复制明文正文或直接修改旧migration；未来新增元数据需expand/reader兼容方案 |
| E05 | Host `internal/session/store.go:58,70,100` schema5/任务、会话、thread、turn、操作映射 | 原有运行关联可复用；Host AGENTS禁止业务主状态/完整编排平台，不能默认把计划主库放入Host |
| E06 | Host `internal/codex/session_protocol.go:21` 原生thread/start、resume、turn/start、interrupt；`internal/session/service.go:312`沿Runtime启动 | 复用已有执行与正常中断，不造推理内核、不强杀 |
| E07 | Desktop `src-tauri/src/chat/runtime_permissions.rs:6` Ask/Auto/Full；`application.rs:1011,1029`忙碌/待审批限制及Full确认 | 定时不静默提权/自动批准，不恢复FEAT-137 |
| E08 | API `cmd/scheduler/.gitkeep`为空占位；`AGENTS.md:19`明确尚未实现 | 不能将目录名当已存在调度服务 |
| E09 | Codex `.yijie/upstream.env`固定rust-v0.144.6、upstream `5d1fbf26c43abc65a203928b2e31561cb039e06d`、Runtime 0.144.6；canonical schema在`.yijie/schemas/app-server/` | checkout HEAD、upstream固定版本、实际二进制是不同事实；本轮只读锁与源码，未启动/替换二进制 |
| E10 | 在Codex app-server/app-server-protocol/canonical schema搜索automation/cron/rrule/scheduled.task，未找到调度method/持久化模块；仅见测试中的ThreadSource feature字符串；相关文件名检索未见引擎 | “automation”字符串不是调度能力；Codex桌面端工具和fork公开Runtime不能混同；Q-01仍未解决 |
| E11 | Desktop `package.json:33,35,36`：pnpm tauri:dev / tauri:demo-fast均调用scripts/run-local-demo-fast.sh；tauri:demo-fast:app传--packaged | 未来真实入口沿canonical；本轮未执行任何启动命令 |
| E12 | Desktop `src/components/yijie/`现有Page/Header/Section/Tabs/Empty/Icon；`src/components/workflows/WorkflowDeleteDialog.vue`已有弹窗交互样例 | 复用UI组件；工作流删除业务协议不直接复制为定时计划协议 |

关联范围：FEAT-128 负责 Artifact，FEAT-132负责 native 对话事实/唯一显示缓冲/加密记录，FEAT-134/136/144负责过程与命令/工具展示，FEAT-152负责权限模式。保留这些有效边界，禁止新 reducer、正文对账、ID猜测、自动封口。FEAT-138属于已取消的FileChange/Diff，不是本需求前置；FEAT-153/154 Coze工作流与电商节点不等于定时任务能力，不继承它们的D4。

## 3. 后续整体方案（候选，未执行）

### 3.1 真实调用链候选

`定时任务页 / 首页对话创建 → 被确认的计划权威 → 持久计划及已确认的调度触发 → 受管执行边界 → 既有 Host / 固定 Codex thread与turn → 既有 Desktop 对话/Artifact事实 → 最小运行元数据投影 / 执行记录 / 完整对话`。

“计划权威”与“调度触发”的具体进程、存储及API没有被确认，不能直接把图中的箭头当作实现设计。Host只承担已批准执行适配；API是否接入local取决于Q-01，不为定时任务偷偷恢复登录/API依赖或新增常驻服务。

### 3.2 Source-first 与兼容计划

- 本轮文档影响none；未来完整范围按breaking保守评审，理由与重分类条件见00 §6。机器scope反映未来风险，不能拿当前只有文档将整个Feature标none。
- Q-01确认各边界Owner/producer/consumer。已知consumer为Desktop，执行adapter为Host；API为条件producer/consumer，Infra为条件部署边界；Runtime保持固定原生协议。没有公共发布，unknown-public当前N/A，未来public需重新登记。
- 若新增共享计划/运行/tool/IPC/API，先在yijie-contracts建立唯一源，冻结标识、时区、状态、分页排序、幂等键、错误、授权与审计、超时/重复/并发/恢复含义，再生成/验证消费者。只在文档说明候选，不创建影子DTO。
- 原生Codex协议需改变时，必须先调查固定upstream/canonical并取得范围决定，再形成Runtime候选与兼容投影；不得在Host伪造未支持automation method。
- 私有计划/运行元数据选择可逆expand，先兼容reader后启用writer，旧数据新reader及新数据回滚reader都需核对；不得写坏已有schema14/15或Host5。具体schema、版本、保留期限未选定，见Q-01。
- 本地demo可在source-first和适用generate/lint/focused conformance后使用精确记录的sibling候选，不伪造发布tag/consumer批准；新请求provider先就绪、新响应/变体consumer先能读，未经兼容证明不混用新旧版本。

### 3.3 未来依赖顺序

1. Owner确认Q-01—Q-04及候选补全，完成D0；另获执行指令。
2. 冻结权威来源、跨仓边界及必要候选ADR；source-first形成契约与兼容/数据方案。
3. 在选定宿主中接入可复用调度与最小持久元数据，复用Host原生执行、现有权限及正常生命周期。
4. 接通Desktop页面、两种创建、三种目标、卡片/历史/详情/对话跳转及真实唤醒/通知能力。
5. 进行必要focused检查、独立结构化审查；在批准的数据/调用预算下从canonical入口进行一次fresh完整Must验收。
6. 有问题基于新证据修复、正常退出重开与复测；记录真实限制，再判D4。全部作为一个用户结果验收，不建立治理切片。

### 3.4 回退与延后

未来最小回退是停止新调度受理、通过原生方式处理在途运行、正常关闭本Feature入口并保留既有聊天和历史；reader不兼容时不直接降级写旧库，不删除文件/volume或重置用户数据。具体回退版本、计划暂停/恢复和唤醒句柄释放依Q-01/Q-04冻结。

延后到独立公开/生产升级：云调度/多设备、高可用、完整生产负载与恢复矩阵、长期保留策略专项、SLA、运营观测、系统级常驻、全平台系统通知专项。不能延后本地正确保存、权限、去重、真实执行和错误恢复以冒称本包完成。

## 4. 本轮实际改动与调查记录

| Repository | 文件 | 实际变化 | 目的 |
|---|---|---|---|
| yijie | 本目录feature.yaml | draft状态、风险/授权边界、十项pending AC | 机器可读需求登记 |
| yijie | 本目录00-feature-brief.md | PDF逐页追踪、产品/UI规则、歧义与决策 | 需求审阅入口 |
| yijie | 本目录01-delivery-log.md | 只读工程事实、Git基线、未来source-first顺序 | 避免把参考图当现成能力 |
| yijie | 本目录02-verification.md | 文档检查和未来用例、未执行原因/影响 | 区分需求检查与产品验收 |

调查完成于2026-09-18：读取5页PDF（第5页空白），渲染全部页面并目视核对；检查规范、相关源码与七仓Git状态；三个只读子任务分别复核治理、工程、UI。子任务不是独立人工批准。原PDF未改，提取文字/渲染图片仅在仓库外临时目录，未作为产品截图/验收证据。

当前仓库没有统一Feature索引文件；FEAT-155 ID起始未占用，因此只新建本包，不新增无依据的索引或修改其它Feature。

产品调试循环：**NOT RUN**。未实施、未启动真实服务、未做产品验收，没有可记录的产品修复或运行结果。

## 5. 授权与实际调用

| 类型 | 本轮允许 | 上限 | 已用 | 说明 |
|---|---|---:|---:|---|
| 仓库外部模型/商家/付费API验收调用 | 否 | 0 | 0 | 不继承其它Feature预算；对话创建未来验收需另获预算 |
| 创建/启停/删除真实定时任务 | 否 | 0 | 0 | PDF控件描述不是操作授权 |
| 破坏性操作/生产写入/部署 | 否 | 0 | 0 | 保持本地只读调查与需求文档边界 |
| Git提交/推送/分支/远端改变 | 否 | 0 | 0 | 仅工作区文档，无提交 |

## 6. 已知限制与下一状态

- D0 pending：Q-01调度权威/数据/权限/兼容，Q-02目标模式/重跑，Q-03筛选语义，Q-04唤醒/通知均未获得确认。
- implementation pending且未授权；所有AC pending、D4 NOT RUN、DP N/A。
- 未证实完整调度实现，不承诺现成复用或已完成兼容；本包已经把该缺口显式落为实施前阻断。
- 当前交付完成仅指需求材料落盘和文档检查，不是FEAT-155功能完成。

## 7. Q-01只读深入调查与技术决策稿追加

用户进一步授权解决Q-01并形成技术决策稿，继续只读调查/需求设计。本次读取固定schema完整method、handler、持久化、Desktop实际投递/授权/生命周期及官方OpenAI/时间库/平台文档；未读取用户数据库/凭据，未运行Runtime/模型/服务，未安装依赖或改业务源码。

七仓HEAD与§1一致，元仓起始已有FEAT-155四文件未跟踪，六个相关兄弟仓clean；[审计JSON](evidence/q01-source-audit-20260918.json)保留源文件hash、方法清单及四文件更新前hash。

主要新事实：固定stable schema267文件/87方法没有完整调度；Host已有持久operation幂等但无公共查询，Runtime本身没有幂等键；Desktop新会话要求项目目录，UI context最长300秒，原生Coordinator可复用但启动/审批观察依赖UI绑定；同库新schema会令旧reader拒绝打开；唤醒/系统通知尚未接线。

结论已收敛为Desktop native计划权威与SQLCipher同事务投递账本，成熟时间库、固定Runtime、原Chat/outbox/Host执行复用；对话采用stable outputSchema草案经确认保存。Q-02三模式、Q-03状态分层、Q-04唤醒/通知已有明确推荐，仍待Owner确认。新增职责记录为Proposed ADR，未Accepted。

本轮文档改动：新增03和evidence/q01-source-audit-20260918.json、新增ADR-0020及ADR索引；更新00/feature.yaml/本日志/02的调查状态、范围代价与验证计划。没有修改Accepted ADR正文、全局治理、业务仓或十项Must的pending状态。

完整范围估算20–32小时与默认12/16不符，列为D0范围阻断；未改timebox、未删AC、未自动建新需求或选择production_hardened。数据库/平台/Provider风险与未来安全验证条件详见03。

技术复核分离于起草进行：修正本地事务与远端session/thread绑定边界、按既有task查询创建结果、unknown仅凭用户确认不能释放执行预约、在可取消退出阶段处理STOP_PENDING，以及原生turn/tool与业务成功不混判。审查不等于人工接受。

当前：Q-01 investigation complete / proposal ready / approval pending；D0 pending，implementation pending/未授权，全部AC pending、D4 NOT RUN、DP N/A。文档检查结果见02追加记录，未继承任何产品资格。

## 8. 第一阶段实际实施（2026-09-18）

先按审计修订权限职责、实例语义、睡眠恢复依赖及有限授权定义，再按source-first实施独立契约与两类Host只读查询。定向检查、四基线兼容、6项既有链路回归和结构化自审完成；首轮测试参数编译错误及修复均见06。未修改Desktop/Runtime，无用户库迁移、真实服务启动或模型调用。第一阶段完成后停止，不自动进入第二阶段；完整Must/D4仍未验收。

## 9. 第二阶段方案（2026-09-18）

用户要求下一步执行方案，新增[07](07-phase-2-implementation-plan.md)。只读核对确认正常open会自动迁移并清理数据，因此先设计可读上限/允许迁移目标分离；时间候选须先验证，计划/occurrence复用同worker，并包含必要聊天删除关联保护。本轮仅修改元仓方案/状态，不修改Desktop、Contracts或Host，不安装依赖、运行产品测试或迁移数据。第二阶段仍未开始，阶段一来源证据不变。

## 10. 第二阶段实施完成（2026-09-18）

按用户四步范围完成时间资格验证、独立契约、reader/迁移目标分离、计划/occurrence及删除保护。10项native与4项新增schema、4项旧存储回归、四基线检查、Rust静态/前端构建、固定来源旧consumer生成检查通过，详见08。暂停时段分类在自审中修正并复验。日常库未迁移，Host/Runtime无业务修改，未进入第三阶段；模型0/12。

## 11. 第三阶段执行方案（2026-09-18）

用户只要求下一步执行方案。读取现有报告、实际聊天事务/outbox/Host查询/授权/生命周期/计数器，形成[09](09-phase-3-implementation-plan.md)。推荐第三阶段分3A/3B/3C，下一次只实施3A契约、兼容reader和native授权/预约基础，不自动铺开实际投递或UI。

本轮新核实：旧文本v1缺operation ID，定时应复用v2/permission-turn；前台dispatch绕过仅scheduler running检查；定时新聊天不能继承/重置前台draft_mode；STOP_PENDING须保留受管进程观察/停止能力；已有HTTP计数器可复用，但标题/草案等实际路径须证明覆盖。两个只读子任务与主任务交叉复核，不构成人工批准。

五仓HEAD/branch/remote与前序基线一致，前两阶段证据内52份业务候选文件hash全部相等。本轮只写元仓需求文档/状态；不改业务代码、不运行产品测试、不访问用户库、不启动服务或模型，第三阶段实现仍未开始，预算0/12。

## 12. 3A实际实施与停点（2026-09-18）

用户明确授权仅3A。按source-first新增独立execution族和29份Contracts/Desktop改动：schema17兼容reader、有限grant、native管理/运行预检、事务内预约与前台/出站保护。源码与定向结果见10及evidence/phase-3a-source-20260918.json。没有新增依赖、Host/Runtime修改或真实投递。

结构化自审补齐删除处理中占用和实际I/O前inflight/删除状态复核；修正后12项3A加10项前序native通过。原草案/计划/恢复源及migration1—16保持。额外通用Contracts lint在定时源版本注解处失败，已登记而非放宽门禁；新增族独立strict:true检查通过。本轮未用子agent，不冒称人工批准。

完成3A后停止，未进入3B/3C/UI；普通入口仍schema15，仅临时合成库迁移17；模型0/12、图片0、商家0，无用户库访问、提交推送或发布。

## 13. 下一步契约收口方案（2026-09-18）

只读复核73份源摘要均未变，结合两项只读交叉调查形成11。通用validator并未被旧来源锁固定；真实缺口是版本注解注册、canonical引用地址、预注册/逐定义编译及严格条件声明，不能靠跳过源或只验投影收尾。未来收口只改必要checker/源/leaf生成及consumer摘要，不捆绑3B业务。

另记录3B接入前置：当前专属目标回写conversation_id会改变workspace来源及grant摘要，必须先区分稳定授权策略与实际绑定；本轮不修改该逻辑。没有产品代码、生成、测试、服务或模型调用，3A结果和lint FAIL保持。

## 14. 契约收口完成并停止（2026-09-18）

用户明确授权执行11并在完成后停止。本轮复现原FAIL，固定73份前序源及checker文本，再按source-first修复typed注解注册、canonical引用及严格条件声明；封闭仓内resolver保持原引用上下文，三族leaf重生/严格检查/同步通过。Contracts完整pnpm lint现PASS，历史FAIL不改写。

17项契约用例包含240个旧样例判定一致，实际Rust producer、22项native、Host4项安全只读回归及四兼容基线通过。10份生成Rust/TS/Go类型逐字节不变；Desktop本批3文件、Host2文件均是schema/candidate，业务、数据库迁移、旧pin和Runtime不变。原测试一次结构等同断言失败及修正见12；本轮只有结构化自审，未使用子agent或冒称人工批准。

完成报告与来源证据见[12](12-phase-3a-contract-closure-report.md)。普通入口仍schema15，未访问日常库/Keychain，无服务或模型调用、Git提交/推送/发布；3B/3C/UI未开始，Must/D4仍未验收，按用户要求停止。

## 15. 下一步3B-1方案（2026-09-18）

用户要求下一步执行方案。本轮核对收口证据77份候选摘要及五仓HEAD/branch/remote未变，读取当前目标/授权/事务、原project/session格式、恢复/审批和正常退出源码；两项只读技术交叉复核不构成人工批准。仅新增13方案和元仓状态/日志，没有产品修改或检查调用。

推荐3B-1先形成稳定授权策略与实际绑定、明确受管来源、兼容reader及手动同库事务，保留scheduled禁发；3B-2才接恢复/生命周期。采纳幂等顺序审查：当前scope核验后先查已提交request，新请求才校验额度/占用，避免自己的预约挡住重试。manual不推进自动时刻；managed项目隐藏与会话历史读取分开，现有sidebar误标作为激活前接续记录。

完整完成标准、兼容/回退和停点见[13](13-phase-3b-1-implementation-plan.md)。3B实现、schema18迁移、目录/事务验证、服务、模型和UI均未执行；本轮文档contract-impact=none，未来3B-1按breaking评审。文本0/12、图片/商家0，未提交/推送或扩大产品范围。

## 16. 3B-1实施并停止（2026-09-18）

按用户明确授权完成稳定授权/实际绑定分离、schema18兼容及受管目录来源、仅manual的组合事务、删除关联与禁发保护。新请求在一个worker事务中完成run/原聊天outbox/预约/占额；重复请求先查原事实，manual不前移自动时刻。实际源码、失败修正和检查见[14](14-phase-3b-1-implementation-report.md)。

正常迁移模型证明仅延迟外键不能完成父表提交，按SQLite标准事务重建流程保留提交前与结束后的完整性检查及恢复设置；真实临时SQLCipher的旧聊天/书签/grant前向迁移重开通过。独立自审补齐删除事务内重验，原guard保留。最终31项native、10项旧回归及静态/构建通过；Desktop本批11份变化，Contracts/Host/Runtime和旧迁移/依赖/生成类型未变。

本轮未使用子agent。没有启动服务、访问日常库/Keychain、付费调用或Git提交/推送/发布；完成3B-1后停止，3B-2/3C/UI及全部Must/D4仍未验收。

## 17. 下一步3B-2方案（2026-09-18）

用户要求“给出下一步执行方案”。本轮复核81份3B-1候选摘要及五仓基线，读取恢复生成/消费、原生观察与审批、预约/聊天索引、正常退出及平台监听接入点。两项只读技术复核及方案最终定向审查未发现阻断；属于Codex审查，不是独立人工批准。

新增[15](15-phase-3b-2-implementation-plan.md)，推荐下一批完整实施3B-2后报告停止：同源Rust恢复类型与候选19兼容 → 两GET消费 → 原生结果/审批及证据释放 → 单owner退出 → sleep/wake屏障 → 安全检查。当前Host身份不能当历史来源，恢复查询不得要求Runtime ready；占用释放须同步处理静止投影、唯一索引、busy/删除/interrupt等精确关联，保留unknown历史、普通legacy语义及禁止旧操作重发。

本轮文档contract-impact=none，未来3B-2最高breaking；无产品修改/生成/测试或服务调用。定时仍禁发、普通目标15、模型0/12；3C/页面/防空闲睡眠控制保持后续范围。实际平台资格无法经正常零调用入口验证时应如实NOT RUN并保留激活阻断，不搭第二App或强杀凑证据。

## 18. 3B-2实施并停止（2026-09-18）

按用户明确授权完成15的六步源码与安全定向验证。Contracts恢复leaf增加Rust同源消费/严格条件校验并同步两consumer来源；Desktop新增候选19，将unknown历史与有证据的静止占用分开，保留原active索引谓词并接入相关查询/中断/删除。两GET不要求Runtime ready，原native事实与审批链复用；退出/sleep-wake共用epoch和唯一owner，超时保留正常等待，不强杀。

结构化自审补齐permission-turns最终发送屏障、所有可能出站代次的正常停止证据、pending/uncertain回执不能退款，以及停止join取消安全。实际45项native、17项旧回归、4份实际producer、Contracts lint/四基线和Host/Desktop检查通过，失败与修正见[16](16-phase-3b-2-implementation-report.md)。旧1—18迁移及固定Runtime保持；本批96份候选中36份变化，均有摘要记录。

实际App/OS通知、退出链与Provider尚未验证，明确NOT RUN并继续阻断投递激活。普通目标15、定时双层禁发，无日常库/Keychain、模型或商家调用、Git提交推送发布。本轮未使用子agent，完成后停止，未进入3C；Must/D4仍未验收。

## 19. 3C-1下一步方案（2026-09-18）

用户要求下一步执行方案。本轮只读核对3B-2的96份候选、当前源码和canonical入口，摘要、HEAD/branch/remote保持，Runtime clean；两项技术复核分别检查发送闭环和后续自动/草案依赖。旧16的实际检查与平台NOT RUN保留，不将源码PASS推定为可激活。

新增[17](17-phase-3c-1-implementation-plan.md)，推荐下一次只实施受控手动投递接线：候选准入/最小兼容 → 已预约run的授权与额度 → 按来源解析目录及原create/turn衔接 → 同事务接受/错误/恢复 → 零调用组合验证、报告、停止。特别区分本run最后一次已占额度与新增额度，按尝试阶段阻止租期重发，仅豁免精确自占用，仍使用3B-2可信证据释放规则。

普通App目标15和定时双层默认拒绝保持，candidate组合检查不等于真实平台/Provider资格；不创建第二App或调试执行入口。自动/重跑、草案/typed IPC和第四阶段按依赖后续实施，三目标及两种创建Must不变。本轮仅文档，contract-impact=none，没有实施3C、启动服务、访问日常库/Keychain或使用模型额度，文本0/12，图片/商家0。

方案复核修正首次create尚无Host session时的审批前提，避免无法创建的死锁；其余审查重点无必须修改项。元仓strict/D0/audit-claims、lint、50/50治理测试、Shell语法、五仓diff、83处链接/空白检查实际通过，业务候选96份摘要保持；技术审查不是独立人工批准，文档检查不是产品验收。

## 20. 3C-1候选实施并停止（2026-09-18）

按用户授权完成17五步，实际范围、命令、失败修正及限制见[18](18-phase-3c-1-implementation-report.md)。Desktop私有20只增两阶段不含正文错误和native claim证明，普通15及默认禁发保持；实际I/O前经原HostBridge在await后重验并记录attempt。原create成功/精确bound恢复共用事务helper，只有原turn的首次发送；attempted不租期重发，取消/退款以充分native证据为准。

57项FEAT-155（新增12）、19项旧回归、4份实际producer、fmt/clippy及Desktop lint/build/docs build通过；最后修正有效never turn的恢复保留规则并定向复验2项。来源共99份候选，本批Desktop15份变化，旧1—19及Contracts/Host/Runtime保持。

全部检查使用正常临时SQLCipher/协议响应及标准构建，未启动App/Host/Runtime/Provider、访问日常库/Keychain、使用模型额度或进行Git外部操作。真实平台及Provider仍NOT RUN并阻断日常激活，Must/D4未通过；完成后停止，未进入3C-2、草案或页面。

本轮元仓strict、D0、audit-claims、lint、50/50治理测试、Shell语法、五仓diff及96处链接/空白检查均PASS；99份候选、4份producer和19份旧迁移摘要复核一致，HEAD/branch/remote保持，Contracts/Host/Runtime未变。D0仍只表示既有产品/设计批准，不是实际激活或D4通过。

## 21. 3C-2下一步方案（2026-09-18）

用户要求下一步执行方案。本轮核对18结果、99份业务候选及实际源码，两项只读技术复核覆盖自动事务和发送/重跑/生命周期。HEAD、branch、remote保持、Runtime clean，18的旧PASS和平台NOT RUN保持原含义。

新增[19](19-phase-3c-2-implementation-plan.md)，维持17既定的automatic+rerun同批，推荐六步实施后报告停止。关键设计为最终revision/grant/启用原子确认，槽去重与原run/outbox/额度/cursor同事务，内外tick统一连续性恢复，automatic每阶段首次I/O复验窗口，unknown与pending审批区分，重跑确认当前定义而不修改旧记录。必要候选21只补私有事实，旧1—20不改。

当前只文档，contract-impact=none；未生成/修改产品、运行产品测试、启动服务或使用模型。普通15/默认禁发、真实平台/Provider NOT RUN、Must pending和D4 NOT RUN保持。文本0/12、图片/商家0，未进入3C-2实现、草案或页面。

最终方案复核已拆开额度耗尽与授权到期，并闭合内部未来停用后的新确认恢复路径；旧确认不清限制，原run未处置不重授权。同时明确多计划只受当前有效预约限制，不新增同一UTC时刻的永久运行上限。修正后无其余必须修改项；技术复核不是独立人工批准。

本轮strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及93处文档链接/空白检查实际PASS；99份业务候选摘要、HEAD/branch/remote与已有dirty条目数保持。以上仅证明方案/记录一致，不表示3C-2已实施或产品验收通过。

## 22. 3C-2候选实施并停止（2026-09-18）

按用户明确授权完成19六步，结果及失败修正见[20](20-phase-3c-2-implementation-report.md)。私有schema21、显式有限确认启用、原组合事务自动消费、内外统一tick及独立重跑已接入；普通15/默认禁发和旧1—20保持。

本次74/74 FEAT-155 native（新增17）、19/19旧回归与实际producer严格conformance通过；静态、构建及收尾复验记录见20及来源证据。首轮once JSON路径错误、暂停扫描饥饿、busy关闭事实被诊断覆盖等已修正并验证，自审不等于独立人工批准。

仅临时SQLCipher/声明native事件/进程内HTTP和标准构建；真实App/OS/Host/Runtime/Provider、日常库/Keychain、模型及Git外部操作均未进行。文本0/12、图片/商家0；Must仍pending，D4 NOT RUN。报告后停止，未进入3C-3、页面或真实激活。

本轮元仓strict、D0、audit-claims、lint、50/50治理测试、Shell语法、五仓diff及155处本地链接检查均PASS；102份候选、5份原样producer与20份旧迁移摘要复核一致。D0只保持既有产品/设计批准，不代表真实激活或D4通过。收尾17项复验、fmt/clippy及Desktop lint/build/docs build均PASS，当前停点仍为3C-2完成后停止。

## 23. 3C-3A下一步方案（2026-09-18）

本轮只读核对20报告、102份业务候选和native/IPC/草案源码；五仓HEAD/branch/remote及已有dirty条目数保持，Runtime clean。保存[21](21-phase-3c-3a-implementation-plan.md)，建议先实现管理查询/确认IPC，后续3C-3B接受限草案。原生在途删除缺少阻断、manual/read缺UI context包装、历史无分页/完整投影均列为A前置，不以UI禁用或内部native函数直注册代替。

A复用共享源与已有Desktop私有IPC同源模式，推荐不新增SQL22；缺失运行时间/审批依据明确unknown，既有21事实足够本批查询。B的outputSchema并不约束工具，固定受限模式和可信完整最终结果另行收口。本轮还修正feature.yaml残留的“自动/重跑未实施、schema20”说明并补20证据索引，不改旧报告。

本轮未实施、生成或运行产品测试；20的74/19/17结果保持上批含义。普通15/默认禁发、真实平台/Provider NOT RUN、Must pending和D4 NOT RUN不变；文本0/12、图片/商家0，无日常库/Keychain、服务或Git外部操作。两项只读技术复核不等于独立人工批准。

最终方案复核已收口两项：私有IPC明确引用FEAT-126已接受权威，并同步00/03及机器状态；有效状态按Deleted/Completed/Paused优先，只有原Enabled的未来触发限制映射暂停，最后预扣run独立。两项只读复核确认无剩余方案阻断，不是独立人工批准。

本轮strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及113处变更文档链接/空白检查实际PASS。102份业务候选摘要、五仓HEAD/branch/remote与已有dirty条目数保持；仅修改8份元仓需求文档，未实现、生成、运行产品测试或使用真实调用。

## 24. 3C-3A实施并停止（2026-09-18）

按用户明确授权完成21五步，结果见[22](22-phase-3c-3a-implementation-report.md)，来源见[本轮证据](evidence/phase-3c-3a-source-20260918.json)。私有IPC源先行、原生UI/native授权和提交期限、同事务删除保护、有界查询及typed client已接；普通15/默认禁发、候选21保持，无SQL22。

本轮82项FEAT-155专项及收尾12项本批专项、19项旧回归、5项client检查、16份实际IPC交换及严格同源校验、fmt/clippy/lint/build/docs通过。总generate:check受起点Contracts dirty保护阻止，未改保护；定向生成独立PASS。失败修正、安全跳过与未执行边界逐项见22。源码自审不是独立人工审查。文本0/12、图片/商家0，未访问日常库、启动真实服务或提交推送；Must pending、D4 NOT RUN，报告后停止。

## 25. 3C-3B1下一步方案（2026-09-18）

用户要求下一步执行方案。本轮只读核对22的123份业务候选摘要及五仓HEAD/branch/remote，全部吻合；保存[23](23-phase-3c-3b-1-implementation-plan.md)，不开始产品实现。两项技术复核分别检查Host/Runtime受限配置及Desktop来源唯一性，补清目录接线与Store迁移语义后无剩余方案阻断；不是独立人工批准。

推荐B1先完成固定配置/准入定义、共享执行契约、Host不可变用途与Store5→显式候选6兼容、原start/resume/turn适配，再做零调用组合检查并停止。Desktop来源确认/候选22留B2。真实配置/Provider资格仍NOT RUN，不能把outputSchema、Ask或sandbox=readOnly当成纯草案保证。

本轮文档contract-impact=none；未来B1按breaking处理，整体breaking保持。没有生成契约、修改产品代码、跑产品测试或启动服务；普通Desktop15/Host5、默认禁发、文本0/12、图片/商家0及日常数据边界保持。22中的测试结果不冒充本轮复跑。

## 26. 3C-3B1与3C-3B2实施并停止（2026-09-19）

2026-09-19当前交付：本轮授权的3C-3B1与3C-3B2候选实现及零真实调用组合检查完成，见[25实施报告](25-phase-3c-3b-implementation-report.md)。普通Desktop15/Host5，候选22/6；实际Manager因有效策略未具备资格拒绝真实草案发送。已停止，不进入页面/真实激活；0/12、Must pending和D4 NOT RUN保持。下方旧状态为阶段历史。

执行定义见[24](24-phase-3c-3b-execution-definition.md)，实际检查、修复、源码自审、兼容回退和未执行项见25及独立证据目录。当前不以合成证据代替真实有效权限或Provider资格。

## 27. B1/B2后的下一步方案（2026-09-19）

2026-09-19下一步建议：仅执行[26：3C-3B3A受限草案执行资格收口](26-phase-3c-3b-3a-qualification-plan.md)，先判定固定Runtime的stable能力能否满足既定边界，再做可证成的最小Host修正；证据不足则交付具体决策并保持禁发。B1/B2结果仍以25为准，本轮没有实施、产品测试或真实调用；普通15/5、候选22/6、文本0/12及D4 NOT RUN保持。

本轮165份业务候选摘要和五仓HEAD/branch/remote逐项吻合。源码核实空MCP map不会删除继承服务器、profile回执只含标识、stable config/read可作调查入口但不是最终工具/权限证明；实际固定产物来源吻合，CLI --profile限制不等同命名权限配置缺失。另登记原生装配、草案unknown恢复/来源重发现和页面查询差距，未并入本批。两项并行只读技术复核不代表独立人工批准；当前文档变更contract-impact=none。

本轮方案检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法及五仓diff检查均PASS；122处变更文档本地链接有效。仅修改7份元仓需求文档，四个产品仓全部起点文件逐字节保持，五仓HEAD/branch/remote未变；没有产品测试、服务、日常库/Keychain或真实调用。两项只读技术审查的修订已纳入，未发现剩余方案阻断；这不等于真实策略资格通过。

## 28. 3C-3B3A资格调查收口（2026-09-19）

2026-09-19当前交付：用户授权的3C-3B3A资格调查已收口，结论 **NOT QUALIFIED**，见[27资格报告](27-phase-3c-3b-3a-qualification-report.md)。固定产物/源码/267份stable schema来源吻合；实际配置继承和最终权限/工具证据不能闭合，第三步Host修正条件不成立，保留禁发。11项Host定向race回归及scoped vet通过；未改四个产品仓、未启动真实服务、未迁移日常库、未使用模型额度。DEC-155-09仅建议单独评审最小原生受限能力，未批准或实施；已停止，不自动进入B3B/页面。普通15/5、候选22/6、0/12及D4 NOT RUN保持。以下旧“当前/下一步”均为阶段历史。

本轮contract-impact=none，整体FEAT仍breaking；来源、权限/工具矩阵、已执行与未执行项、最小决策和自审见27。本轮与25/26历史证据分开：不把进程内fixture当真实Runtime资格，不把调查完成写成草案可用。三入口I/O前拒发、兼容存储重开和普通路径回归均有新日志；真实协议观察因零外部请求预检未通过而未启动。DEC-155-09不改写Accepted ADR，不扩大现有执行授权。
