# FEAT-163 验收矩阵与证据记录

> 2026-10-24再次复审：旧整体PASS结论已撤回。最新逐入口事实见[07](07-implementation-reaudit.md)。第8真实回合公开消息/反馈可确认，但因输出额度未交付而失败；不得用历史原题成功覆盖。下方第8–9节为上一轮记录，复审完成后追加第10节。

本地候选实施与适用验收已完成。第3节保留预登记清单，第8–9节记录实际覆盖和未运行项；不将未测试的业务工具资格、全仓安全测试或生产发布算作通过。

## 1. 三层验收不能互相代替

1. 原生机制：真实公开assistant消息经现有Runtime工具循环、Host、Native和存储产生并传递。
2. 内容与时序：说明当前工作和真实新进展，在工作期间可见；工具顺序真实；正式结果交付。
3. 前端体验：主线以公开说明穿插淡色可展开的分段工具摘要，本段轻量操作明细与单项详情可查；reasoning/协议诊断另置；流式/折叠/滚动/历史行为正确。

默认0计数标题、0重复摘要卡片只能证明第三层的一部分。模型没发进度、终态才补显、只有日志或系统等待提示，均不能通过整体目标。

## 2. Must结果台账

| AC | 结果 | 必需证据 | 当前证据 |
|---|---|---|---|
| AC-001 | PASS（local适用范围） | 统一入口与指令组合 | Start/Resume/expert追加/技能及连接器配置沿原链；当前普通、项目、续聊真实覆盖；其余入口S/N/C覆盖见第8节，不宣称每个业务工具真实资格 |
| AC-002 | PASS（local适用范围） | 长任务真实公开进度 | 第二回合2段、第三回合3段、第四回合2段，均在正式结果前真实显示；最终短答与单次搜索路径不强造前言 |
| AC-003 | PASS（local适用范围） | 内容/身份/phase/及时性 | Provider/Runtime逐消息hash匹配；Host→SSE→Native→SQLCipher普通字节一致性PASS；真实UI过程期间可见、正常重开仍在。并非每层另采完整真实正文 |
| AC-004 | PASS（local适用范围） | 原生反馈闭环及收敛 | 第二/三/四回合call-output-next-request匹配，无同call重复dispatch或dummy播报；最终原题1搜索0命令。第二次4个不同空curl仍如实保留，不承诺模型永无无效尝试 |
| AC-005 | PASS（local适用范围） | 结果与停止语义 | 城市/CSV/补丁/短答真实结果；第六回合正常停止34.696秒、部分内容保留；无答/phase/Artifact例外与普通错误由组件检查覆盖 |
| AC-006 | PASS（local适用范围） | 分段与具体活动 | 真实读取文件、原生编辑/创建、diff与+2−0统计、分段展开；App上下文由Host/Native/组件普通一致性覆盖，未借用连接器凭据做真实App工具调用 |
| AC-007 | PASS（local适用范围） | 原phase与用户展开选择 | null实时可读；186项及新增57项定向检查；第四回合完成保留展开和焦点；同会话Timeline重挂沿同一page阅读选择 |
| AC-008 | PASS（local适用范围） | 正常重开与隔离 | same-build重开保留3项目轮次、公开进度、文件变更、中断与统计，HTTP17→17；buffer/reader/旧格式/重复通知普通检查PASS |
| AC-009 | PASS（local适用范围） | 流式与布局 | 生产组件流式/选区/滚动/减弱动效测试；真实亮暗1180×760截图，原主题及1268×780恢复；不是所有组合都手动回放 |
| AC-010 | PASS（local适用范围） | 复用、来源与安全 | Runtime源码/二进制不变；native v5版本化投影及旧读者保持；17HTTP/10网络未超限，禁止测试未执行，五仓差异审阅与来源记录 |

## 3. 入口和场景矩阵

类型：R=真实模型/App；N=既有Native普通样例；C=正式组件普通样例；V=正式App视觉；S=静态来源检查。合成样例不得写成R。

| 场景 | 方式 | 必须出现的行为 | 结果 |
|---|---|---|---|
| 无工具短答 | R+C | 正文直接流式可读，无空过程入口/强制前言/人为等待 | NOT RUN |
| 同一聊天追问 | R+N | 每轮独立消息边界、计时、展开；前轮进度不混入 | NOT RUN |
| 一次有效工具任务 | R+C | 任务相关公开文字与工具行正常呈现，详情可查 | NOT RUN |
| 原城市对比问题 | R | 开始说明+得到信息后的推进说明+最终答案；不再无效重复取数 | NOT RUN |
| 不同主题的多步任务 | R | 证明不是城市题专门文案或偶然短路径；同样完成三层目标 | NOT RUN |
| 必要只读命令或普通工具 | R+N | 有真实用途，结果进入后续请求；exit0不被包装为资料验证成功 | NOT RUN |
| 普通/项目/专家/技能/连接器入口 | S+N+适用R | 有效基础指令一致、实际工具权限不变；最少真实覆盖有不同组合的路径 | NOT RUN |
| 附件/看图及已有图像/Artifact生成 | S+N+C+适用R | 复用同一聊天过程；不污染实际结果，不以需要文本答案的规则误报合法产物；外部调用单独记额度 | NOT RUN |
| 结构化结果slot/计划任务共用聊天路径 | S+N+C+适用R | 过程不污染严格final结果；保留已有校验与展示，不扩调度器 | NOT RUN |
| phase=null直接及中途消息 | N+C；真实发生则R | 到达即显示；原phase不写回；后续工具/末条正文不被吞掉 | NOT RUN |
| 显式final非空开始 | N+C；真实发生则R | 正文即时显示、默认收起过程；用户手动展开优先，不为触发此分支猜填phase或换模型 | NOT RUN |
| completed无回答/commentary-only | N+C；真实发生则R | 动画停止、准确未交付提示；不把summary/commentary当final | NOT RUN |
| 合法无正文shell/compact/Artifact | N+C | 原生生命周期保留，不全局判failed或误报普通问答空答 | NOT RUN |
| Item未结束但Turn终态 | N+C | Item事实不补造；技术说明进详情，整体不继续忙碌 | NOT RUN |
| 正常等待/运行/待审批 | N+C+适用R | 仅一个实际等待位，决策入口可达，原scope/流程不变 | NOT RUN |
| 用户正常停止 | R+N | 现有turn/interrupt生效，保留部分正文，立即停止忙碌，不补发 | NOT RUN |
| 自然发生的失败或普通错误样例 | N+C；真实发生则R | 错误及恢复操作准确；不强制制造外部失败，不伪记真实通过 | NOT RUN |
| 正常退出重开 | R+N | 已保存正文/顺序保持，不补模型调用、不重播历史打字 | NOT RUN |
| 冷历史inProgress/切会话/迟到订阅 | N+C | 无实时观察不假称运行；不串消息、不重复执行 | NOT RUN |
| 重复通知/同Item生命周期 | N+C | 按身份更新；不同Item同文本不删除；工具不重复dispatch | NOT RUN |
| 展开/收起/上翻/选区/旧轮定位 | C+V | 用户选择和锚点保留；高度变化不强拉到底；键盘可操作 | NOT RUN |
| 亮暗、1180×760、长查询/代码/表格 | C+V | 无遮挡重叠，详情和完整结果可读，减少动态效果正常 | NOT RUN |
| 分段动作摘要与本段展开 TG-01/02/04/05 | C+N+R | 读文件+命令、编辑+读取+命令混合段正确；消息划分段落；多段独立展开，追加不复位 | NOT RUN |
| 文件变更与统计 TG-02/06 | N+C+适用R | 原生fileChange状态与文件kind正确，新增/删除/更新/移动各口径成立，未知不填0，安全预览可读 | NOT RUN |
| App/工具显示身份 TG-03 | N+C+适用R | 真实appContext或已验证目录映射正确，缺元数据不猜App名；子action不变成重复执行 | NOT RUN |
| 新原生投影与持久reader TG-07/08 | N+适用R | 新旧版本可消费，closed旧端点不被新字段破坏；重开保持新字段，旧历史unknown不补造 | NOT RUN |

TG-01至TG-10的完整判据及对应AC见[05补充验收](05-tool-activity-reference.md)。真实写文件样本只能使用后续获授权的普通任务文件；截图中的删除需求不是本次执行授权。

真实样本应预先登记：原题正常回合至少2次、不同主题多步任务至少1次，并覆盖短答、续聊和正常停止；可在同一聊天组合场景，不能用一次搜索短答代替长任务。未预先获批足够预算则保持NOT RUN，不擅自用旧额度。适用入口若未覆盖，不能把“普通入口通过”泛化为“每次对话已验证”。

同一最终来源版本完成本矩阵适用Must的fresh验证；失败之后只有新增证据/修复才重测对应项，所有早先失败保留。成功样本不能冲销未解释的失败，不允许循环抽样直到碰巧通过。

## 4. 复用现有专项检查

实施前先检查当前测试内容及入口；仅选择正常、非破坏性用例。下列是计划命令/落点，不代表已执行，不可把广泛命令退出0当成禁止场景已验收。

| 仓库 | 现有入口或文件 | 计划检查 |
|---|---|---|
| Runtime | `codex-api` Responses普通解析用例；`core` history/normalization；0005测试 | 公开消息added/delta/done/terminal对应、保持顺序、无重复dispatch、普通路径无新增缓冲 |
| Runtime（仅实际改动时） | 既有`build-chat-model-stream-args.sh`、manifest/schema工具 | 有序patch独立重放、标准构建、canonical schema差异、无凭据stdio/正常EOF；先审脚本安全范围 |
| Host | `scripts/test_responses_stream_observer.py`及现有meter测试 | hash/身份关联、stage次数/时间、truncated、请求配置差异、无敏感正文 |
| Host | `internal/codex/*native_conversation*_test.go`、`runtime_permissions_test.go`、`expert_instructions_test.go` | start/resume/switch/expert组合、phase和消息原文、安全投影 |
| Host | `internal/session/native_conversation_test.go`、`native_process_test.go` | 原生投影、正常重放、来源/状态区别；只运行审过的具体测试名 |
| Host/Contracts | 原native decoder、MCP/command安全投影、版本化native/process conformance | 05字段来自固定canonical；fileChange不再丢成unknown；commandActions数组/安全路径/命令预览/App显示身份有界；diff统计与上游口径一致 |
| Contracts | `pnpm check-generated:native`；适用native/process conformance | 新安全投影及旧v4/v11保持兼容，reader支持矩阵明确；实际改源才运行对应generate/sync；不全仓生成危险fixture |
| Desktop | `ChatProcessPresentation.test.ts`、`ChatNativeStreaming.test.ts`、`ChatTurnGroup.test.ts` | 替换旧计数UI断言，保留真实事实；消息交错/null即时显示/无答/展开规则 |
| Desktop | 原activityChoices/activityMembership/Item组件及新增的最小FileChange显示组件（若确有需要） | 05的TG-01至TG-10；本段明细不全塞技术详情；同Item多个action只算一次执行，展开选择/焦点/键盘不丢 |
| Desktop | `conversation-native-view.test.ts`、`chat.store.test.ts`、Native buffer/storage普通用例 | 同Item更新、终态不封口、revision/订阅隔离、保存及重开 |
| Desktop | `useChatStreamPresentation.test.ts`、`useChatScroll.test.ts` | 单一显示游标、终态追平、历史不重播、折叠后的阅读锚点 |
| Desktop | `pnpm lint`、`pnpm docs:build`、适用来源检查 | 类型/静态规范/设计文档；dirty-source阻塞如实处理，不能伪改pin绕过 |

前端定向Vitest使用现有脚本的全部排除目录：

```bash
pnpm exec vitest run src/components/chat/ChatProcessPresentation.test.ts src/components/chat/ChatNativeStreaming.test.ts src/components/chat/ChatTurnGroup.test.ts --maxWorkers=4 --exclude '**/.contracts-source/**' --exclude '**/.agent-host-source/**' --exclude '**/.skills-source/**' --exclude '**/.local/**' --exclude 'scripts/check-feat128-s10d-h.test.mjs'
```

上式CWD为`yijie-desktop`，运行前仍需审用例。根据实际修改补选store/Native等相关正常用例，不默跑包含故障/攻击fixture的整套测试，也不因该命令通过宣称全部Native已验证。

正式App入口仍为`yijie-desktop`的`pnpm tauri:demo-fast:app`及已有same-build `--reopen`。当前local candidate所需配置从真实launcher和来源锁核实，不从旧聊天复制过期环境变量。构建/退出/启动只在后续授权后执行；使用正常Cmd+Q/停止，不强杀。

## 5. 证据格式与判定规则

每次真实尝试至少保存：attempt ID、时间/时区、源码与build receipt/Runtime manifest身份、model/provider/effort/summary/权限、有效指令和工具面摘要、thread/turn摘要、HTTP请求与费用台账、消息/调用/结果对应、UI关键时间线、结果与未覆盖项。

比较正文hash时应注明层间允许的转换：原始公开文本→安全投影/容量→存储文本→DOM阅读文本。转换被记录且内容未丢失才通过；不能把脱敏/Markdown渲染差异误判为丢消息，也不能拿任意“规范化”隐藏实际缺失。真实输出有容量截断则如实partial，该样本不能证明完整链路。

每个失败填写最早断点、已排除原因、新证据、下一次只做什么；不复制原始推理、密钥或完整私密响应。产品历史不seed、不修饰，不重新执行旧记录来制造before/after。

未执行项目固定包含用户禁止的强杀、权限破坏、可执行替换及攻击注入场景；原因是长期硬性安全要求，影响是这些故障/攻击覆盖不作通过声明。可以用普通合法事件的纯函数样例和正常取消验证相应可见状态，不能谎称已做故障实测。

## 6. 本轮文档检查（非产品验收）

2026-10-24实际执行，CWD为`yijie`（链接检查从CrossBSD读取需求包）：

| 检查 | 结果 | 覆盖限制 |
|---|---|---|
| `check-feature-package.sh --strict docs/features/FEAT-163-codex-process-parity` | PASS，退出0 | schema v3结构/语义和模板完整性；未请求D0/D4门禁 |
| `pnpm lint` | PASS，退出0 | 元仓11项manifest与11仓治理规则存在性，不是业务代码lint |
| `pnpm test` | 50 PASS，0 FAIL | 元仓普通文档治理/manifest测试，无真实模型或产品操作 |
| 对每个`scripts/*.sh`分别执行`bash -n` | PASS，退出0 | 元仓脚本语法，不执行脚本；逐文件检查，避免只解析glob首项 |
| `git diff --check` | PASS，退出0 | tracked差异空白检查；新增文档另做UTF-8/链接/空白核对 |
| 需求包Markdown本地链接 | PASS，0缺失 | 文档链接有效，不证明产品行为 |
| 既有dirty文件指纹对照 | 检出1项工作区漂移，首次检查退出1 | `yijie-desktop/contracts/market-catalog.candidate.json`在规划期间变化；本任务未写该文件，保留现状、不归因、不覆盖，实施S0重新核对 |

本轮只运行这些非破坏性文档检查；产品AC始终NOT RUN。最终内容审阅及基线保护检查结果见[evidence/document-checks.json](evidence/document-checks.json)，不把该文件当产品验收报告。项目记忆新增入口之外的既有内容逐字保留，三张参考图hash一致；不能声称所有兄弟工作树在本轮期间完全未变化。

新增工具分段截图后的文档检查见[evidence/tool-group-document-checks.json](evidence/tool-group-document-checks.json)：strict结构/schema、元仓lint、50项元仓测试、链接/空白与新增参考图hash通过；七个本次核查的源码文件指纹无漂移。两路文档审阅通过，并补best-effort观察范围及patchUpdated/完成快照区别。此前检查和baseline不覆盖改写；所有TG及产品AC仍NOT RUN，不声称整个并行工作区不变。

## 7. 交付结论

- 当前产品实现：NOT STARTED。
- 当前真实模型/检索/商家调用：0；无在途请求。
- D0产品/UX人工批准：未记录；仅需求目标明确。
- D4本地真实可用：NOT RUN。
- DP公开、Git提交/推送、发布：未授权/未执行。

## 2026-10-24 实施首轮（持续中）

- 基线真实原题：`evidence/baseline-diagnosis.json`、`baseline-runtime-summary.json`、`paid-call-ledger.json`、`baseline-complete.png`。公开进度FAIL，最终消息保真PASS；没有工具函数调用，不能验证历史call/output闭环。
- 当前前端：`frontend-activity-check.log` 7文件112PASS；`frontend-lint.log` PASS。首次误匹配历史副本的`frontend-first-check.log`保留，不作为当前结果；后续普通定向日志保留前轮失败。
- Host：`host-focused.log`三包定向PASS；observer6PASS。Contracts新旧普通6PASS，v5 OpenAPI lint PASS/2 unused component提示；生成来源检查`native-authority-check.log`PASS。
- Native：`native-check.log`编译所有tests PASS；`native-cross-repo.log` Host投影字节跨SSE/Native buffer/SQLCipher/正常重开PASS，含fileChange、commandActions、App身份。无模型调用、无破坏性步骤。
- 新版App首次构建`activity-app-build.log`被候选来源漂移门禁拒绝，未启动；正在按现有freeze程序刷新已验证本地来源。产品端到端仍NOT RUN。

- `native-buffer-tests.log`5PASS、`native-reader-tests.log`2PASS、`native-format-tests.log`1PASS。
- `activity-app-build-2.log`构建PASS/真实启动FAIL，失败UI见`activity-startup-before.ax.txt`；普通旧受管目录升级测试`catalog-upgrade-before.log`FAIL→`catalog-upgrade-after.log`PASS。修后真实启动正在构建验证，不提前记PASS。

## 8. 2026-10-24实施实测（持续更新）

- 基线原题：1HTTP/1搜索/0公开进度/1答案，63.482秒。M1有证据，不能泛化到旧截图Provider断点。
- 修改后同题：4HTTP/4原生搜索/4shell HTTP尝试/2公开进度+1答案，178951ms。正文hash及反馈回灌匹配。4条curl无stdout且exit0，说明命令成功不代表资料成功；没有重复call ID或相同参数，无dummy进度工具。历史13搜索23命令仍保留，不改写历史。
- 本地CSV：5HTTP/0联网/6命令/3公开进度+1答案，49.086秒；原输入不变、两产物独立Decimal重算PASS。写文件使用shell heredoc，尚不能证明fileChange；后续复用Runtime已有补丁拦截验证。
- 真实截图/AX与Provider/Runtime摘要：evidence/baseline-*、second-*、third-*，其中third-artifact-check为独立计算结果。没有在产品历史插入fixture。
- 预算至10:32：3/4用户回合、10/40HTTP、9/20网络动作（5搜索+4shell HTTP），无在途。正在申请最多3个附加用户回合以完成短答/停止/最终版本原题；未答复前上限仍4。

| 检查 | 最新结果 | 覆盖/限制 |
|---|---|---|
| Provider observer | PASS 6项 | 普通事件/摘要，不记录原始推理或密钥 |
| Contracts v5生成/校验/普通一致性 | PASS | native-process生成check含v3/4/5；v5 lint只有2未引用类型提示；新旧投影测试 |
| 旧native源相对4个固定baseline | PASS | native-source-compatibility.json逐字节一致；不是全仓生产兼容声明 |
| Host入口/指令/目录升级/原生投影 | PASS | host-focused-2、host-entry-check；managed catalog已知旧字节正常升级，不绕所有权 |
| Frontend定向8文件 | PASS 186，既有skip2 | frontend-final-check-2；消息/null/final/多层展开/正常卸载重挂/流式/选区/页面 |
| Desktop静态与文档 | PASS | frontend-lint-final-2、desktop-docs-build；旧lint-2/final测试类型错误FAIL已修复 |
| Native编译/格式/Clippy | PASS | native-check、native-fmt-check（空输出）、native-clippy -D warnings |
| Native单一buffer/reader/格式 | PASS 5+2+1 | 非破坏性普通用例 |
| Host真实投影字节→SSE→SQLCipher正常重开 | PASS 1 | native-cross-repo含新字段，合成事件而非真实模型 |
| 正式App最终版 | IN PROGRESS | final-app-build；实际补丁/续聊/正常重开/视觉仍待完成 |

前端扩大检查暴露旧等待文案断言：先1FAIL，再3FAIL；按统一中性“正在处理…”更新，原日志保留。阅读展开曾在真实观察间丢失：同会话权威刷新可卸载Timeline，现将原展开选择放在当前页tenant/session内存，不改变执行/权限。已通过真实组件重挂与跨scope隔离测试，最终App待验证。

入口来源矩阵（S静态、N普通用例；不冒称全部真实模型资格）：

| 入口 | 复用链路证据 | 真实覆盖 |
|---|---|---|
| 普通/项目新建 | Host session_protocol StartThread相同permissionInstructions，model catalog Kimi fallback复用常量；同ChatPage/Timeline | 城市无项目+CSV有项目 PASS |
| 续聊/模型切换 | ResumeThread重新应用sessionDeveloperInstructions/BaseInstructions；同Native channel | 第四回合待验；切模型不新增付费验证 |
| 专家 | composeExpertBaseInstructions保留完整ordinary基线并追加verified role/index；三项Host普通测试PASS | NOT RUN，不借用其他Feature资格 |
| 技能/连接器 | 已有上下文/工具配置合并，不替换普通基础指令；公开消息走相同Native view | NOT RUN；未使用FEAT-162凭据 |
| 附件/看图/Artifact | 原turn输入与动态工具路径，允许的附加指令保留普通原则；已有Artifact/reference展示及空文本例外 | 外部产图NOT RUN |
| 计划草案/结构化slot | 原scheduled约束、结果校验及structured-answer slot保持；不会把公开进度放入结果JSON | 普通组件覆盖，真实调度NOT RUN |

全仓历史攻击fixture、权限故障、可执行替换/强杀测试未执行，原因是用户硬性安全规则。全量生产generate/breaking/不可变提交发布不是此次local候选完成声明；本任务仅运行安全定向门禁并记录范围，旧源和旧端点仍保留。

## 9. 最终本地验收与边界（2026-10-24）

最终代码：Host无文件头hunk兼容与Desktop文件详情阅读选择已纳入final-app-build-3。第5短答3秒、无工具；第6正常停止，真实原生补丁+2−0、公开说明与部分内容保留；第7原题29.576秒，约8秒已开始输出答案，1搜索/0命令/1正式助手消息，无独立中途消息。该路径不能伪记为长任务进度样本；长任务消息机制由2/3/4回合及同一原生链的普通回归证明。最后hunk统计补丁未改变消息指令/解析/循环。

同一构建正常Cmd-Q→canonical --reopen后，3个项目轮次、公开消息、文件变更、中断和新行数统计保持，模型HTTP仍17；见reopen-check.json和final-reopened-project.ax.txt。旧版投影中的result.md未知统计没有补写。亮暗最小窗口见visual-check.json，系统浅色与1268×780窗口已恢复。

受限诊断已正常停止。随后使用原canonical脚本移除临时Provider代理，重新构建并正常启动日常App；daily-config-restoration.json证明构建输入只有该环境覆盖的hash变化，源文件/worker来源完全相同，Runtime SHA不变。daily-final-ready.ax.txt证明启动就绪，**未额外发起无预算模型请求**。所有真实调用都由meter注入8192输出上限，不能说它们是无限制生产配置逐字节相同的请求。

总预算见budget-summary.json：7/7用户回合、17/40HTTP、6原生搜索+4shell HTTP尝试=10/20网络动作；16请求有用量：输入198947、输出14346、总213293 tokens。第16请求因正常停止transport_ended，用量未知，不能计0或推算费用。计费金额未取得。没有第8回合，没有借用FEAT-162的连接器凭据。

保留边界：

- 历史原截图缺Provider SSE，无法追溯性证明旧问题是否在Provider/Runtime丢失，不补造历史。当前可见基线支持M1，新增样本反馈完整；不声称证明了所有历史重复的唯一根因。
- 既有Runtime没有可直接开启的通用无收益重复guard。本任务恢复原指令沟通原则、核验原生反馈，未另建Host去重执行器或追问循环。最终样本收敛，不能承诺任何模型永不尝试无效读取。
- 城市事实没有全面独立审核；本Feature验证消息/执行/呈现，不能把UI或exit0当事实正确。
- App上下文使用普通原生样例验证；没有额外真实连接器/专家/产图付费资格。当前统一入口是S/N/C及适用R联合覆盖，不泛化为业务能力全验收。
- 全仓攻击fixture、权限故障、可执行伪装、强杀未执行；生产不可变pin、签名、公证、发布不在本次授权。工作树候选不是发布制品。


## 10. 本轮复审结论：整体未通过

最新实现及失败定位见[07](07-implementation-reaudit.md)，以下逐项结果覆盖前文旧PASS，不把前一版本证据自动升级为本轮完整验收。

| Must AC | 本轮状态 | 证据与未通过点 |
|---|---|---|
| AC-001 全入口统一机制 | pending | Kimi/MiniMax各5种Start/Resume组合及专家/技能/附件/连接器/草案RPC与组件覆盖；草案独立input-only由真实Runtime本地样本确认。真实专家长任务仍失败，不能声称所有入口完整对齐 |
| AC-002 长任务公开进度 | fail | 第8两段进度但未交付；第9持续137秒无公开消息且未交付；第10只有普通检索场景1段进度+答案。缺消息发生在Provider未生成处，不伪造 |
| AC-003 消息保真及时呈现 | pass | 第8/10所有公开正文Provider/Runtime hash一致，真实UI运行中可见；原跨层Host/SSE/Native/SQLCipher普通检查继续适用，未重写unknown phase |
| AC-004 有效工具与反馈 | fail | 第8六份结果完整回传；第10唯一sleep 1结果完整回传但该调用无业务收益。禁止dummy wait的有效指令hash匹配；无相同参数重复不等于无无效执行 |
| AC-005 答案/失败/无文本交付语义 | pass | 第10真实答案；第8/9准确失败、不假报交付，fileChange-only/partial/failed边界组件通过；第6正常停止历史保留。第9的业务交付失败保留于AC001/002/006 |
| AC-006 交错过程及具体工具明细 | pending | 重开第8两段文字与六命令分段保持；前轮原生patch/diff显示及本轮50项边界通过。第9原生patch参数被上限截断，最新默认文件任务成功交付未通过；真实App连接器资格未运行 |
| AC-007 phase未知与展开保护 | pass | 公开未知阶段即时可读，末条保护与failed“模型消息”标签真实可见；组件覆盖结构化草案仅一张、过程操作栏、冷组和用户选择 |
| AC-008 正常重开与隔离 | pass | 第8重开2消息/6命令/失败保持；日常重开第8/9失败及第10进度/2搜索/sleep/答案均保持，task_started仍专家2/普通1，无新回合。仅Runtime冷历史不支持完整工具恢复，独立限制保留 |
| AC-009 流式/布局 | pending | 原组件流式/选区/滚动及前轮亮暗最小窗证据保留；本轮最新App1268×780可读，未把旧截图冒称全部新版本布局验收 |
| AC-010 原生复用与证据边界 | pass | 无Runtime源码/二进制改动、无新执行循环/进度模型/表；当前五仓HEAD未变且原基线文件无缺失，shared FEAT162变更单列归属；严格文档、lint、diff及canonical build5通过 |

本轮定向检查：Host入口9个顶层（含10组合）、session7个、真实固定Runtime本地2个/6次local HTTP；前端9文件320PASS/2原有skip，现场修复149及最终50与前述重叠不能相加；最新lint-final-5、Host vet、design docs、Native恢复/reader各1通过。详见07。禁止的故障/攻击测试未执行，不声称全仓测试通过。

实际累计10/10回合、23/40HTTP、12/20联网（8原生+4旧shell）。22个已知请求input299186/output38854/total338040，第16用量未知。HTTP20/21发送8192但Provider报告8195且incomplete，原值保留；transport completed不等于业务成功。meter正常退出，无第11回合授权。

最新证据：evidence/reaudit-turn-9-diagnosis.json、reaudit-turn-10-diagnosis.json、reaudit-tenth-instruction-provenance.json、reaudit-eighth-reopen-check.json、budget-summary.json。整体FAIL/in_progress，未完成D4。
