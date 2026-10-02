# FEAT-156 — 需求包与实施验证记录

2026-10-02（Asia/Shanghai）。**当前结论见§8：最终独立Runtime候选及日常入口验收通过，10项Must均PASS。** §1–§7保留历史失败与阶段结论，不代表当前完成状态。累计授权50次HTTP、4次图片理解；实际44/50、4/4。

## 1. 文档检查（2026-10-02 实际结果）

CWD：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie`。

| 检查 | 命令/方法 | 当前结果 |
|---|---|---|
| 模板与结构 | `bash docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-156-desktop-chat-model-switching` | PASS，exit 0；仅结构/声明校验 |
| 声明真实性 | `node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs --audit-claims docs/features/FEAT-156-desktop-chat-model-switching` | PASS，exit 0；仅结构/声明校验 |
| 元仓lint | `pnpm lint` | PASS，exit 0；11仓清单与中央/兄弟仓Contract First规则存在性校验 |
| 元仓已有测试 | `pnpm test` | PASS，exit 0；50 tests / 50 pass / 0 fail；已审查为文档validator/manifest测试，无禁止的故障/攻击执行 |
| 元仓Shell语法 | `bash -n scripts/*.sh` | PASS，exit 0；只检查语法，未启动脚本服务 |
| 内容完整性 | 四文件AC一致、链接/截图hash、无真实key、无模板标记、状态/范围自检 | PASS；10项AC一致；相对链接存在；PNG 1114×306及SHA-256匹配；无secret-like串/模板/行尾空白 |
| 差异与工作树 | `git diff --check`与status、新增文件全文检查、兄弟仓状态复核 | PASS；元仓仅新增本需求目录；未跟踪文件另做全文与空白检查，不能只凭git diff无输出判定 |

`--strict`检查未完成标记，不代表业务方案获批准。D0检查器要求`product_ux.status=PASS`；本包明确pending，**不把它改PASS来获得绿色**，本轮不运行D0/D4/DP资格检查，也不填产品focused_checks或产品artifacts。用户截图是需求来源，绝不是实现截图。

## 2. 需求编制自检

- 用户U01–U05、截图V01和凭据边界S01均在00映射到规则/AC；附图只作为位置参考，不授执行权。
- 共10条Must，与feature.yaml相同；每条有可观察结果和下表T01–T10。
- 规则覆盖新建、已有、受限草案、empty/loading/error/permission、超时/取消/重试/并发/部分成功/正常恢复。
- 模型选择、原生有效配置与每次已接受请求快照三者分开；未知不能假回退或假成功。
- 新建默认Kimi不覆盖已有MiniMax/旧计划授权；max是精确参数，不是UI文案或xhigh别名。
- 源码事实、推荐默认、尚未验证的原生能力及冲突分表登记；官方资料附链接与读取日期。
- breaking、source-first、上下游激活顺序、旧digest/reader、回滚与秘密边界可追溯。
- 已有Desktop20项改动保留；本轮不写产品、配置、数据库或二进制；不继承历史预算。
- 计划、标题/工具隐含调用计入未来预算，未拓展为模型市场/语音/Coze模型管理。
- 自动化文档检查和Codex交叉复核不冒充独立人工批准或真实E2E。

独立Codex只读复核后已修正文档：仅确定未应用才回退旧模型，部分成功/未知保持待核实；明确计划冲突重审的模型快照来源，区分计划快照变更与聊天临时切回；原生双向切换按目标profile设置effort，不把MiniMax强套max。四文件状态与10项AC一致，未发现阻断落包的剩余矛盾。这是文档复核，不是独立人工批准。

## 3. 起草阶段的验收设计（当时全部 NOT RUN）

本节只是下一阶段的可执行验收设计，**不授权本轮运行**。本地合成测试只保护规则；一次fresh真实服务闭环才可支持D4。

| Test / AC | Given / When / Then 与必要证据 | 当前状态 |
|---|---|---|
| T01 / AC-001 | 新任务、已有聊天、计划草案均进入同Composer；菜单开合/选中/同项/Esc/点外部、方向键/Enter/IME；两主题、1180×760、200%缩放不裁切，发送/停止可达。保存原生截图/键盘记录，不用参考图冒充。 | NOT RUN |
| T02 / AC-002 | 新建显示Kimi/max；A改MiniMax、B仍Kimi，返回A正确；全新C仍Kimi。可信旧MiniMax显示MiniMax，未知旧记录不回填。正常重开保存会话选择，不恢复超出原范围的未提交纯文本草稿。 | NOT RUN |
| T03 / AC-003 | 先固定原生版本核对catalog/effort与同thread正常unsubscribe/resume，零prompt资格验证独立标识；再获额度后同聊Kimi→MiniMax→Kimi，验证三轮用户可见连续事实。记录有效thread/provider/model/effort与脱敏请求ID；模型“我是Kimi”或单独curl成功都不足。 | NOT RUN |
| T04 / AC-004 | 正常提交/执行/待审批/未知/计划预约禁切；同输入同快照保留原operationId，不同模型新意图用新ID；切页迟到回执不改另一会话。参数与outbox原子一致；声明式并发状态及正常UI验证，不制造进程崩溃。 | NOT RUN |
| T05 / AC-005 | 构建当前两模型×文本/图片/文件输入×普通/工具/审批/Artifact能力表。Kimi至少真实文本、可控普通图片理解与一次安全只读本地工具后续；保留现有图片生成独立provider，不默认调用收费图片工具。能力拒绝保留附件，不默默降为文本；MiniMax已有能力做定向回归。 | NOT RUN |
| T06 / AC-006 | 自建无PII有效旧/新记录验证reader与expand，新操作快照可正常读；旧digest/已受理操作查证不重算。canonical正常退出/重开，历史模型不改、无新发送；高版本reader行为明确，回退保留兼容reader与原数据。 | NOT RUN |
| T07 / AC-007 | 正常缺配置/有效scope/无权状态，受管profile映射和key引用审查；仅用无秘密的声明值检查scrub、Runtime注入与所有工具子进程排除。真实key从不作fixture/日志，权限模式与审批沿既有原生路径。 | NOT RUN |
| T08 / AC-008 | 草案选择模型→合法结构候选→确认只保存暂停；三目标预览展示有效模型，grant/run快照一致。旧计划不改默认，模型变更需要重新审阅；已有聊天模型冲突阻止投递，不后台切换；手动/自动/重跑沿原幂等与有限授权。代表性真实执行须纳入单独预算。 | NOT RUN |
| T09 / AC-009 | 在正常未配置Kimi的受管测试配置中显示原因并保留草稿，明确配置后重试恢复；MiniMax须由用户显式改选。鉴权/余额/429/超时/能力不符使用普通声明式响应单测，不耗费接口请求制造错误。未知先查证，正常Stop不伪终态。 | NOT RUN |
| T10 / AC-010 | 同一fresh canonical验收周期运行最终候选，全Must、真实主路径、一个代表性正常failure/retry、focused checks及原生视觉/退出重开有证据；每个请求含标题/工具续推/重试记账。未通过保留失败，不从不同旧运行拼成全部通过。 | NOT RUN |

正式测试命令在实施时根据当前各仓package/Makefile及新增测试入口固定，本包不伪造尚不存在的测试文件/命令。需要Contracts源generate/lint/focused conformance、Host profile/switch/digest回归、Desktop IPC/storage/outbox/UI定向验证；Runtime不改则仅对固定产物做适用原生资格验证，不为满足形式而重编译。

AI行为评估以路由、上下文连续、工具闭环、结构结果可解析、附件处理与错误透明为核心；不把两模型不同文风/速度当失败，不宣称Kimi质量提升。使用非敏感合成内容，验证中涉及真正工具写入仍必须适用原审批与授权。

## 4. 本轮未执行项、原因与影响

| 项目 | 原因 | 影响 |
|---|---|---|
| 产品源码、配置、契约源/生成物、数据库迁移 | 用户只落需求，不执行 | 功能尚不存在，不能宣称可用 |
| Kimi key/余额/模型API、MiniMax调用、标题/图片/MCP | 未获本需求调用授权，预算0 | 凭据资格、额度及真实兼容未知 |
| 固定Runtime原生切换、实际max/工具/图片/草案能力 | 属于后续实现与资格验证 | 源码方案尚非产物行为证明 |
| 应用启动、UI验收、正常退出重开、D4 | 本轮文档范围 | 没有实现视觉或真实服务证据 |
| D0 Owner确认、公共契约批准、提交/推送/发布 | 尚无相应授权动作 | 文档完成不允许自动实施/交付 |
| 频繁/故障强杀、替换/劫持可执行文件、权限破坏、攻击载荷/危险归档 | 用户长期硬性安全条款禁止 | 永不以此验证；只用正常状态与合成普通返回，无法覆盖的极端恢复不宣称通过 |
| 全仓make lint/test/generate及生产专项 | 文档小范围无必要，跨仓可能写文件且含历史不适用测试 | 不作全仓CI/生产质量结论 |

如后续正常停止失败，保留现场、停止相关步骤并报告；不得强杀。新构建仅限已授权范围的canonical可复现输出，不覆盖既有受保护/来源不明二进制。

## 5. 交付结论

- 本轮交付：FEAT-156候选需求包；四份治理文件和一份用户截图参考。
- D0：pending；implementation：pending；全部Must：NOT RUN；D4：NOT RUN；DP：N/A（local）。
- 模型/图片生成/外部MCP业务调用：0；没有真实密钥落入包中。
- 所有未来实现与测试只在新的明确执行指令及适用授权下开始；本次落包后停止。


## 4. Owner授权后的实施与验证（2026-10-02）

用户“开始执行 feat-156 需求”批准本地实施/D0；另明确授权24次两模型HTTP请求、最多2次图片理解、每次输出8192 tokens；图片生成和外部MCP不在额度内。真实调用台账 [paid-call-ledger.json](evidence/paid-call-ledger.json) 当前5次、图片0次，失败请求也计数。

| 检查 | 结果与范围 |
|---|---|
| Contracts模型源 | 3测试通过；model-selection-v1、模型感知路由与Go/Rust/TS生成/同步一致；scheduled-plan/execution/draft schema严格检查通过。采用明确local_worktree_candidate，不伪造commit或改旧不可变锁。 |
| Host规则 | 5项TestChatModel通过；覆盖独立凭据来源、MiniMax旧catalog语义、Kimi max、双Provider计数器、选择revision/原操作重放、旧turn快照；另4项环境/原生权限普通检查通过。 |
| 固定Runtime正常本机服务 | 早期Python原生探针3次本机响应；Host完整受管链4次本机响应，Kimi/max→MiniMax/high→Kimi/max同thread与受限草案通过；均0远程调用，正常EOF/Shutdown退出。 |
| 真实Provider | Host完整链前三次HTTP200且max/high/max，native thread ID保持；两次草案400。精确原因是Kimi Responses不支持tool_choice=none，见交付日志§9与台账。未降档/换模型/自动重发。尚未按用户可见历史核验连续事实，AC-003仍pending。 |
| Native SQL/outbox/计划 | 2项FEAT156测试、13项存储/时间回归、8项计划准备回归通过。首轮ID先预留后物化，模型快照与接受事务一致；旧授权摘要不改，新run冻结profile；迟到读取不覆盖switching。 |
| Frontend focused | 6项新模型client/composable测试、Composer、草案和scheduled client通过；合计6文件96项中91通过、5失败。5失败都在ChatPage既有状态/项目断言；用git HEAD版ChatPage通过只读Vite load hook替换作对照，53项中同名5失败、48通过。未改这些断言或掩盖失败。 |
| 编译静态检查 | pnpm lint、vue-tsc、pnpm build、cargo check --tests、cargo clippy --all-targets -- -D warnings通过；文档pnpm docs:build通过。后续变动需要相应复核。 |
| 全量生成门禁 | pnpm generate:check在公共旧契约的clean-checkout检查停止；不放宽该锁。canonical启动对旧native/Host投影及新candidate来源验证通过；未宣称全量make lint/test通过。 |
| Canonical App | 显式FEAT156本地候选通过canonical脚本构建并启动，使用独立数据目录、端口18087；原18081占用未停止。真实入口可见Kimi默认、两项菜单、max说明；键盘方向/Home/Enter/Esc及输入保留通过，无新增模型调用。正常应用Quit退出0。 |
| 视觉 | 亮色1180×760（Retina截图2360×1520）验证；200%模型/发送可滚动到达，但实测发现Naive浮层坐标重复缩放。修复使用局部定位层抵消zoom，菜单保持应用倍率；修复后的标准构建已完成，但Mac随后锁屏，无法继续视觉复核。暗色尚未验收。 |

禁止项没有执行：未强杀进程、破坏权限、替换/伪装Runtime或注入攻击fixture。已有Host部分单测依赖fake runtime executable，未运行；全量cargo/test脚本含其它未经筛选场景，未声称全量通过。本次只使用标准工具生成项目构建输出；固定input-only Runtime文件未改动。

当前隔离候选可以审阅实现，但日常入口不默认激活模型writer；等待Owner确认Runtime候选后完成精确来源、真实草案/工具/附件/标题/计划/重开、暗色与最终diff/D4。现有AC不删减、不提前标PASS。


实施末段自检补充：发现标题原先未覆盖本次验证计数器，已将模型标题的显式 thread config 同时纳入双Provider固定计数器；真实App未发送过消息，标题真实调用仍0。进一步保留 MiniMax 原catalog支持档位与基础指令，避免新模型层改变旧标题/旧会话默认。新Kimi文件来源增加nofollow、打开后同inode检查和有界读取；仅正常声明式来源测试，无权限破坏或恶意fixture。

当前验证环境：付费计数器已通过正常 Ctrl-C 退出0（全部5个请求已结束），无剩余验收请求；候选App第二次重建后Mac锁屏，无法通过UI正常退出或检查，不强杀进程。Mac解锁后先核对候选App并正常退出，再按最新源重建；不能把已运行的上一构建误认成最后代码版本。Runtime仓保持无变更，最小补丁问题待Owner答复。


最后定向复核：新增模型client/composable、Composer、草案、scheduled client与计划表单6个文件共44项全通过；pnpm lint再次通过。计划模型读取已归入composable，组件不直接访问原生API；关闭功能时不创建额外store依赖。Rust fmt及clippy重新通过；FEAT156两项原生测试再次通过。ChatPage仍按上表保留原5项基线失败。当前源码快照已重新冻结，因Mac锁屏，最终原生视觉及正常退出需在解锁后继续，不能以构建完成代替验收。

## 6. 恢复后的最新验收结论（2026-10-02约19:00）

此前§4和§5为起草及早期实施历史，不代表当前结果。本轮仍未D4；最终整体fresh验收及日常激活尚未完成，Must AC保留pending。最新逐项事实见[evidence/desktop-fresh-observations.json](evidence/desktop-fresh-observations.json)，新增Runtime资格见[evidence/runtime-chat-models-qualification.json](evidence/runtime-chat-models-qualification.json)。

- 原生真实通过：普通Kimi/max→MiniMax/high→Kimi/max同聊天上下文、文件/只读命令、两模型图片、键盘及亮暗/最小窗200%、正常重开无重发、合法input-only草案和确认后关闭保存、正常Stop中断、未配置阻止发送/显式切换/恢复后正确上下文。标题原生既有门禁关闭，没有启用或真实标题请求。
- 本轮修复并验证：Store7草案purpose写入、草案仅暂停确认、已绑定专属聊天当前模型重审、模型冲突事务不占授权且旧grant不能复用、未配置模型的终态历史读取。
- 新前端6项目标模型用例及相关46项PASS；最新显式local环境原生FEAT156五项PASS；fmt/clippy、lint、canonical build、docs build、旧固定clean来源generate:check通过。此前ChatPage同名5项基线失败保留；没有宣称全量测试通过。
- 剩余：旧失败草案的未知create占用执行通道；产品永久删除框已准备，仅待单条删除授权。三目标真实计划执行、日常默认入口激活和最终D4未完成。
- 计数：16/24 HTTP，图片2/2；不再发送图片。原生Stop请求记transport_ended而非完整回复。Synthetic实际11；运行中台账暂7，待meter正常退出后补记4，避免覆盖其内存计数。
- App和额度meter暂保持运行，当前无在途Provider请求；系统外观已恢复浅色。没有任何真实secret写入治理包、Git提交或发布。


## 7. 历史逐项验收与未完成项（2026-10-02，日常入口复核后）

现行入口 `scripts/run-local-demo-fast.sh --packaged` 默认激活双模型，使用原daily数据/18081、SQL29、Host7与已批准chat-models Runtime。模型入口位于发送/停止左侧；新建Kimi K3/max，旧MiniMax会话保持。不是隔离候选opt-in才可见。

| Must | 当前结果 | 实际证据与范围 |
|---|---|---|
| AC-001 入口与视觉 | PASS | 三种Composer共用slot；原生两项菜单/当前勾选/max、方向键/Enter/Home/Esc；亮色1180×760/200%及真实系统暗色100%实测，外观恢复浅色。仅会话内观察截图，无虚构截图文件。 |
| AC-002 默认与会话隔离 | PASS | 日常新聊默认Kimi；只读访问用户旧MiniMax聊天显示MiniMax，返回新建仍Kimi。候选中A/B选择和正常重开历史保持；未知状态不假装选择成功。 |
| AC-003 真实路由与上下文 | PASS | 请求7→8→9同thread两向切换并保留青山；日常21Kimi记住远山，28–30MiniMax仍识别附件7+5和远山，工具失败单独保留；实际参数max/high来自meter而非模型自报。 |
| AC-004 锁定与幂等 | PASS | 真正生成中选择/附件/权限禁用；native outbox快照、改模型不同intent、过期回执/原ID重试、只读历史及无权限入口、已绑定计划冲突有focused验证。不是只靠renderer禁用。 |
| AC-005 输入与原生工具链 | **FAIL** | Kimi文件/命令续推和两模型图片已成功；MiniMax独立原生命令26/27成功且exit0。但原跨模型聊天28/29再次失败，SSE中间Item参数空而最终参数完整，当前Runtime未承接。不能以独立成功覆盖此失败。 |
| AC-006 持久化与兼容 | PASS | SQL28快照、SQL29 managed_chat迁移；旧grant/run/snapshot字节与摘要、FK/trigger保留；reader不降库、writer关闭不派发模型outbox。多次正常Quit/reopen无历史重发。 |
| AC-007 scope/秘密/权限 | PASS | 受管profile闭集、exact runtime pins、Host/Native scope校验；credentials只注入受管Runtime且从工具子环境排除。权限模式/审批回调和原生write-before-ack协议检查通过；无密钥进入文档。 |
| AC-008 草案和三目标计划 | PASS | 请求14草案schema合法且确认关闭；17/18专属聊天Kimi→实际模型冲突拒投→重审MiniMax，旧run保持Kimi；19每次新建，20已有无项目聊天，均native完成。三个测试计划全部off。 |
| AC-009 恢复与停止 | PASS（已覆盖代表场景） | 缺配置保留意图/草稿，显式MiniMax，正常恢复配置请求16保留上下文；请求15正常Stop。日常预算达到24时按真实失败显示，未重发；systemError恢复缺口修复后原模型operation重试成功，0新增HTTP。流式兼容问题归AC-005，仍未解决。 |
| AC-010 最终fresh整体闭环 | **pending** | 当前不能通过D4。必须完成已证实的流式兼容、精确产物投影及最后一轮原生验收；不把不同旧候选局部结果拼成最终通过。 |

### 能力矩阵与边界

| 能力 | Kimi K3/max | MiniMax M3/high |
|---|---|---|
| 原生文本/上下文 | 真模型PASS（7/9/16/21） | 真模型PASS（8/18；日常30保留远山） |
| 图片理解 | 真模型PASS（12） | 真模型PASS（13） |
| 文本附件 | 真实138B附件求和12（10/11） | 日常28–30保留文件与合计12；同轮工具仍FAIL |
| 只读本地命令及续推 | 真模型+native command exit0（10/11） | 独立chat26/27 PASS；跨模型chat28/29 FAIL，不可整体标PASS |
| input-only结构草案 | 真实structured output、tools=[]/auto（14） | profile/路由/权限conformance；未额外声称真实MiniMax结构草案 |
| 审批/权限 | 共用原生链；in-process绑定/回执/模式回归PASS | 同左；未把合成回调标为真实高影响审批 |
| Artifact/图片生成 | 保留原独立provider/反向调用及scope配置；未收费调用 | 同左；非本次替换对象，未声称真实生成验收 |
| 辅助标题 | 原native LoadConfig门禁关闭；配置路由已检查，无真实调用 | 同左 |

### 最后检查事实

- Desktop七项FEAT156原生测试以显式local/model环境和include-ignored执行：7PASS，0ignored。覆盖model outbox、草案claim、三目标与grant冲突、managed_chat和历史迁移。
- 模型client、聊天模型composable、计划模型composable、launcher：canonical excludes下4文件27PASS。新增ChatPage只读/无权限模型入口1PASS。首次省略excludes误收集.local两份旧checkout，2失败；更正命令后通过，没有改旧checkout或断言。
- `cargo fmt --check`、`cargo clippy --all-targets -- -D warnings`、`pnpm lint`及canonical packaged build通过；旧clean来源generate:check、docs:build通过。Host最新TestChatModel及go vet通过；原生权限模式/审批绑定的安全in-process回归通过。
- 新增Host `systemError`切换用例先准确失败，允许已结束错误状态后通过；固定上游thread_status先判运行/审批/input，才可能得到systemError，因此不放宽活动线程。原生正常重开后用原operation完成Kimi切换，历史不重发。当前Runtime二进制未变。
- 原ChatPage全文件基线5失败/48通过，在HEAD页面只读加载对照重现；这不是FEAT156 focused通过或全量CI通过。
- 原20份Desktop未提交改动保留；19份初始hash中16份字节不变，3份为Composer、token、pattern必要增量；未记录初始hash的原chat文档保留原内容，仅追加本需求。五仓diff检查通过，无commit/push/tag。

### 新发现与下一步

请求25的简化API和26/27的独立原生工具参数完整；28/29在原历史准确复现：参数增量分别125/18bytes，与最终响应中的有效JSON对象摘要完全一致，但arguments.done与output_item.done的arguments均0bytes。原生从后者读取空串，工具未执行；30模型报告失败并识别原文件/记号，不把“对话已完成”等同工具已成功。

详见[诊断证据](evidence/minimax-tool-arguments-failure.json)及[具体Runtime候选方案](03-runtime-stream-arguments-proposal.md)。新行为须Owner确认；构建仍独立目录、固定上游、原缓存复用、旧产物保留，不能直接改运行二进制或用Host代理改写响应。当前30/40HTTP、图片2/4，所有已发生调用包括失败与续推均记账；synthetic累计11已在meter正常关闭后补齐。

## 8. 最终候选整体验收（2026-10-02，当前权威结论）

**结论：FEAT-156 的本地实现与 10 项 Must 验收通过。** 依据是最终源码、独立 Runtime0005 产物及同一 canonical 日常验收周期的请求31–44，不以旧候选的局部成功覆盖已发生的失败。历史失败、诊断和中止请求继续保留。这里的 D4 只表示 `demo_fast + local`，不代表全量 CI、生产发布或独立人工评审。

### 审计、批准和最小修复

审计确认主要阻塞是 MiniMax 实际 SSE 的中间完成 Item 参数为空，最终完成响应却含完整参数；不是模型选择器仅改了文案。请求28/29的被动长度/摘要观察确认原因，原生消费路径只读取中间 Item。Owner最新指令明确授权“审计…批准最小修复方案…执行剩余需求”，因此实施03中限定的0005：暂缓空参数工具 Item，终态完成后严格匹配 index/id/call/name/namespace 与参数增量，恢复一次；不满足条件安全拒绝。正常非空路径、input-only空工具集、沙箱、权限和审批继续保留。

独立产物 `.yijie/build/chat-models-stream-args/aarch64-apple-darwin/` 的 binary SHA-256 为 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，manifest 为 `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`。269个stable schema与保留基线逐字节一致。复用原 `codex-rs/target`；没有复制另一套编译缓存，没有修改 canonical 上游子树，也没有覆盖原 input-only、chat-models 两组产物。四个旧hash在最终收尾再次一致。

Contracts精确投影先生成，再同步Host/Desktop；Host消费严格固定新hash。另补齐取消未提交计划草案后新聊天恢复Kimi默认，页面回归先失败后通过。此前Store7、SQL29、systemError终态恢复、只读保护和日常入口默认装配均包含在最终源码中。

### Must AC 最终映射

| Must | 结果 | 最终证据 |
|---|---|---|
| AC-001 入口、菜单和视觉 | PASS | 原生新建/已有/草案共用Composer，入口紧邻发送/停止左侧；菜单两项、max、当前选中、键盘与取消。最终亮/暗100%截图观察；1180×760逻辑窗口、200%滚动后菜单和发送完整可达。恢复浅色、100%、原窗口大小。 |
| AC-002 默认与会话独立 | PASS | 新聊Kimi；主聊Kimi、MiniMax草案各自保持，正常重开可读；取消新草案不会把MiniMax带入新聊。可信旧MiniMax不改写，未知/readonly状态原生校验。 |
| AC-003 两向切换与上下文 | PASS | 最终31 Kimi → 32–34 MiniMax → 39 Kimi，原聊天及native thread保持，均识别“远山”和文件7+5=12；meter记录exact max/high。41/42再验证Kimi工具续推。 |
| AC-004 锁定、快照和幂等 | PASS | 41和43生成中真实模型/附件/权限禁用；停止后恢复。native七项focused覆盖原operation、revision、快照、readonly、目标绑定及grant冲突；新Runtime保持事件顺序和一次交付。 |
| AC-005 文本、图片、文件和工具 | PASS | 35/36两模型图片理解正确；最终原文件事实连续；33 MiniMax只读命令exit0，34续推成功；41/42 Kimi只读命令exit0。审批/Artifact适用原生协议回归通过；收费图片生成与外部MCP按范围未调用。 |
| AC-006 持久化、兼容和正常恢复 | PASS | SQL28/29正式迁移/旧摘要/外键/触发器及reader拒绝降库通过。最终正常Quit/重开保留模型、历史中断和关闭计划，无自动重发。 |
| AC-007 scope、秘密和权限 | PASS | 受管profile闭集、exact产物资格、两层scope/read-only校验及工具子环境排除。最终变更文本secret-like扫描0；原生input-only tools=0/auto，未开放原生工具/沙箱/审批边界。 |
| AC-008 草案、确认和三目标 | PASS | Kimi37与MiniMax44均合法结构草案，tools=0。37确认默认Kimi，明确改MiniMax后保存off；38专属MiniMax、39已有聊天Kimi、40每次新建Kimi均native完成。模型冲突前置拒投0HTTP；重审后旧run仍MiniMax。44只审阅取消，不创建额外计划。 |
| AC-009 正常失败/恢复/停止 | PASS | 同源候选显式空Kimi配置→默认禁发/草稿保留/显式MiniMax→正常恢复受管配置→31真实成功。43使用Stop正常中断、保留部分内容、入口恢复，重开仍中断。没有强杀或故障注入。 |
| AC-010 最终真实整体验收 | PASS | 最终Runtime0005+SQL29+Host7+最终UI源码贯穿31–44及零费资格/视觉/正常重开；无opt-in的原daily数据和18081；最终退出meter环境，恢复日常入口并readyz=ready。 |

证据：[最终fresh周期](evidence/final-fresh-cycle.json)、[逐请求台账](evidence/paid-call-ledger.json)、[Runtime资格](evidence/runtime-stream-arguments-qualification.json)、[最终源码摘要](evidence/source-review-20261002.json)、[历史故障与修复关联](evidence/minimax-tool-arguments-failure.json)。原生截图为本会话内实际观察，没有虚构可下载PNG；用户参考截图仍只作为需求来源。

### 检查和请求口径

- Runtime canonical独立构建通过，4个新增流式用例、全部34个Responses SSE用例、`clippy codex-api --lib`、269schema、重放/反向补丁、正常EOF握手通过。上游原有app-server unused_mut warning保留。
- 真实固定Runtime经Host与本地普通SSE：2次工具生命周期及4次同thread两模型/input-only请求通过，0远程费用；全部本机synthetic累计17次。没有伪造/替换可执行文件。
- Contracts源与consumer确定生成/同步、Host模型/权限/审批定向测试与vet、Desktop七项原生FEAT156、27项模型/计划/launcher及新增只读/取消草案2项、lint/fmt/clippy、canonical打包、`generate:check`、`docs:build`通过。无后续产品源码变更；新增授权只扩大验收计数器已批准tuple到(50,4)。
- 真实HTTP累计44/50、图片4/4、单次上限8192 tokens；工具续推、失败和取消均计数。43是正常Stop导致的transport_ended/BrokenPipe，绝不计为完整模型回复。标题、图片生成、外部MCP均0。余6次未用；meter正常Ctrl-C退出0。
- App通过Cmd+Q正常退出0，随后通过canonical日常入口启动且不带meter覆盖。最终默认Kimi、MiniMax草案选择持久、原主聊中断历史可读、三计划全部off。未新增模型发送。

### 明确保留的限制

1. 原ChatPage全文件5项失败已在HEAD对照重现；这不是本功能focused失败，也不意味着全量CI通过。早期漏掉`.local`排除造成的两份旧checkout误收集已纠正，没有修改旧checkout或断言。
2. 原FEAT155监听context/authorizationRevision时会关闭未提交计划表单，最终验收中遇到过；`ScheduledTasksPage.vue`原有watcher及草案authority刷新逻辑均核对为基线行为。重开审阅可完成操作，保存记录和模型快照未丢失；没有扩大FEAT156去放宽授权刷新。此为已登记的既有交互限制。
3. 未执行用户禁止的强杀、权限破坏、危险/攻击fixture或fake executable历史测试，不对相应极端恢复作通过承诺。图片生成、外部MCP和关闭门禁的标题没有真实验收；适用配置/协议回归与本需求范围已分开记录。
4. 仅本地可用，未提交/推送/打tag/发布；local_worktree_candidate不是生产不可变来源。全量回归和生产加固不在本次D4结论内。

### D4 文档与声明门禁收尾

最终schema validator、`--audit-claims`、`--gate D4`均exit0；元仓lint、50项治理测试及Shell语法通过。首次D4检查命中历史旧阻塞的未完成标记，现已明确说明当时结果不明并补上§17的实际解除事实；没有修改检查器或删掉历史失败。检查器只核对结构和声明，业务通过依据仍为上表真实观察。结果记录在[evidence/d4-checks.json](evidence/d4-checks.json)。

## 9. Owner授权的本地提交审查（2026-10-02）

用户明确“审查并提交 FEAT-156，暂不推送”。本阶段没有新增产品行为、真实模型调用、分支、推送、tag或发布；只修正两处Desktop文档的旧阶段状态、补Host秘密边界说明，并随上游真实提交重新生成Runtime来源投影与Desktop Host构建快照。

| 仓库 | 本地提交 | 范围 |
|---|---|---|
| yijie-codex | `7fd463bcef07f37b0211acd9f62b9f93ea0a4b12` | 12文件：0004/0005、独立构建/资格脚本及文档 |
| yijie-contracts | `1a213ac8383e95ac6ec69363937687904fa3591c` | 35文件：模型源、计划快照/managed_chat、生成物与精确Runtime投影 |
| yijie-agent-host | `a5bd6c2e7a619768eafaa63bcca7f774d1134bd3` | 33文件：受管双Provider、切换/快照/恢复、测试及秘密边界 |
| yijie-desktop | `8da82707909dff00c7833f6f4c32987fe3768ecd` | 67文件：入口/状态/原生持久化/计划模型、来源与必要文档 |

元仓提交包含本记录，避免在内容中伪造自身SHA。详细文件摘要与保留清单见[本地提交审查](evidence/local-commit-review.json)。

Desktop初始20份修改仍全部留在工作区，其中4个混合文件只把FEAT-156内容写入Git index，没有reset或覆盖工作树。16份完全无关文件没有进入本次提交；19份有初始hash的内容全部验证保留，原聊天文档仅按FEAT-156标题分开增量。发送图标样式、流式呈现、耗时和复制时机等原改动未混入。

为验证独立提交，将Git index导出到临时源码目录，复用现有node_modules，不复制Rust缓存。纯暂存版本lint、vue-tsc/build、27项模型/计划/launcher及2项页面回归PASS。该导出没有重复进行真实原生D4，§8的原生观察仍对应当时完整工作树；此处明确区分验证范围。初始pnpm因临时目录位置变化尝试自动同步依赖，在修改前停止；改用已安装pnpm支持的warn模式运行相同依赖，未安装或清空依赖。Contracts7项、lint、确定生成/consumer检查、Host三包TestChatModel和vet、Desktop当前来源generate:check及docs:build均PASS。

Runtime补丁文件的4个单空格行是unified diff必需的空上下文标记，外层git whitespace检查将其识别为新增空格；逐行检查补丁实际新增源码无尾空白，普通文本检查通过，原资格patchhash保持，没有关闭hook或产品门禁。原ChatPage5项基线失败与FEAT155授权刷新表单限制继续保留。新家族的local candidate语义没有因commit自动晋升为production/release。

## 10. 后续全仓推送授权与界面改动提交

Owner随后明确要求推送当前目录所有仓库改动。因此将§9中原先保留的20份Desktop界面修改独立提交为 `b133af65ac5d572b88c4a4f4cbbb30a04c1dc166`，当前FEAT-156提交和界面提交可分别追溯。该批7文件80项普通组件/计时测试、lint及build通过；没有把ChatPage既有5项基线失败改为通过，没有执行禁止的故障/攻击测试。

12仓origin当前分支已逐一读取核对；4个产品仓push成功回执及7个无需变动的仓库见01 §22。元仓本记录与先前需求包提交一起推送，最终逐仓远端SHA在提交后核对。所有原改动均已纳入提交；没有新增模型请求、密钥、缓存、运行二进制、远端强制更新或生产发布。
