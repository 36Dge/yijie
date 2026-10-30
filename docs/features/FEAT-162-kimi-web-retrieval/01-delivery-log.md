# FEAT-162 交付日志

## 2026-10-30 最终：七例Alpha通过并关闭

E1—E7均在真实App观察到应有工具/模式及必要步骤成功、回答可见；E5保留两回合，E7保留单回合Pro→Fetch。未核对质量、来源关系、费用记录。按[43号](43-alpha-results-and-closure.md)和[44号](44-alpha-final-reaudit.md)关闭本期FEAT-162；feature=usable、implementation=complete、acceptance.feature_verdict=PASS。标准历史FAIL与严格D4未通过不被改写。

本轮修复了Alpha观察器响应衔接/续跑承接，以及Contracts纯列表意图的Basic/Pro重叠描述。三次构建均有明确目的，后两次缓存复用约1分39秒/1分41秒。保留08/09、所有旧App/备份/证据和失败记录；本地提交，无推送。App/观察器/本轮owned workflow已正常停止，volume保留；20元软停止未触发，不再自动续跑收费。

以下全部为历史时点记录，旧“当前、最新、暂停、下一步”不覆盖上述已关闭状态。

> 当前验收决定（2026-10-30，澄清后）：Alpha保留E1—E7七个场景，每例调用应有工具并有回答即通过，不核对回答质量、来源关系及费用记录；E4正文模式、E5两回合、E7单回合Pro→Fetch均保留。七例全部通过才可按Alpha关闭FEAT-162。规则见[39号](39-alpha-acceptance.md)，当前七例均NOT RUN，执行继续暂停。

## 2026-10-30 Alpha范围纠正

Owner指出此前误解：七个用例仍在，只放宽每例通过标准。现恢复七个Alpha Must及逐例结果，保留原场景/模式/必要串联，不核对质量、来源关系或费用记录。00、39及feature.yaml已一致更新；22/38标准和旧证据保持。检查见evidence/alpha-seven-case-correction-20261030.json。本轮无构建、App启动或收费，不恢复此前暂停的执行。

## 2026-10-30 已废止的三项Alpha草案（误解，以下仅为历史）

按Owner明确要求，当前22号逐字节保留为38号标准验收；原brief和feature.yaml保存history。新增39号Alpha，当前Must改为AC-A01—A03；对应三工具各成功+回答可见即本期通过。标准质量、来源、费用、复杂串联和通用严格D4不再是本期关闭前置，既有产品实现不改。历史E1失败不能被重写为通过，新Alpha尚未执行。文档一致性检查见evidence/alpha-criteria-change-20261030.json。

以下内容保留此前实施和标准验收事实；旧“必须全部E1—E7/D4才能关闭”的表述已被本次Alpha决定替代。

> 当前状态（2026-10-30）：三项修复及零费用验证完成，源码已本地提交并canonical闭合，无推送。未构建/启动App、未收费；第08/09代及历史证据核对一致。见[36号结果](36-route-cache-zero-cost-results.md)与[37号复审](37-route-cache-final-reaudit.md)。旧E1 FAIL、E2—E7 NOT RUN、D4未通过。


## 2026-10-30 路由、收集、缓存修复与复审

严格D0后完成Host条件路由、Cargo实际产物收集及分组件中间缓存；正常零费用测试、固定Runtime/worker本机集成、来源检查通过。保留产物541800项一致。详细命令/数量/限制见36号与脱敏evidence/route-cache-checks-20261030.json；分离复审见37号。没有App或供应商调用，不是D4。

以下为历史时点记录，旧“当前/最新/恢复”不替代本节。


## 2026-10-29 当前：软预算、精确来源与真实App执行

Owner已明确20元为软停止阈值，允许在途超出后停止，不要求费用硬上界；仅本地提交FEAT-162已批准，不推送。当前v3计量、来源提交和App/Workflow进展见[33号](33-real-app-execution.md)，授权见[evidence/current-authorization-20261029.json](evidence/current-authorization-20261029.json)。真实七例及D4仍待执行。下列历史收费、提交与准入限制按其原时点解释。


## 2026-10-29 — 方案再审后执行与20元授权

先记录28号方案复审，再修全量生成及owner停止适配。Owner明确解除本轮收费禁止并批准20元；实际新增0元、无Git提交/推送。生成/定向验证与过程失败见29号，最终复审见30号；历史日志按当时授权解释。

以下为历史记录，旧“当前/最新/未授权”按原时点理解。


## 2026-10-29 — schema EOF修复与零费用续验

- 旧基线与当前源独立解析自有schema URI，修复5项EOF；九个完整breaking均通过。oasdiff补fail-on ERR，普通收紧样例能实际失败。
- 补齐3项时间边界测试后Kimi27项通过；真实canonical worker由Host持有的5项正常生命周期/race通过，全部正常退出；Desktop44项及有界亮暗/最小窗口/键盘组件预览通过。
- 额外旧全量生成检查失败：旧通用入口仍下载model-selection URI且遗漏当前family输出。已按前态恢复35个原干净生成文件、保全并移除3个本次新输出；原有dirty生成物保持，不宣称全量绿色。
- 26/27及eof-checks记录完整命令、过程失败、剩余项与复审；旧24/25及台账不改。付费0，未提交/推送/激活。


## 2026-10-29 — Basic/Pro 实施与零费用复审

- 用户进一步授权契约、代码、零费用验证及最后审计，禁止付费、Git提交/推送。按Contracts→Connectors→Host→Desktop实施，contract-impact=breaking。
- 已实现三工具、旧lease隔离、新模式A/D、逐页状态/部分结果、源生成UI和独立v2离线计量；canonical观察配置保持严格来源门禁。
- v2付费入口因native硬上界和正常owner停止链未证明而固定关闭；不允许plan自声明解锁。
- 定向检查、canonical worker新generation和前端/设计构建通过。8个完整breaking基线中3通过、5被既有远程$ref EOF阻断，未绕过。
- 详情/命令见24与implementation-checks，最后主代理复审见25。实际供应商/模型HTTP为0，未读真实Key、未启动App、未提交或推送；旧历史不改。

以下是需求修订和更早时点记录。


## 2026-10-29 — 五项缺口与E5交互修订（仅需求文档）

- 用户明确授权将前轮五项发现及E5歧义补齐到需求，按治理同步设计/验收/预算并再审；不实施代码、不执行付费调用。文档contract-impact=none，产品规划仍为breaking。
- 原五项映射为R01计量/真实工具集合等价、R02新旧期限及UI、R03路由覆盖、R04逐来源截断、R05混合质量结果；R06为E5两回合交互。决策、原事实与复审见23，当前细则以22为准。
- 保留旧Basic/Fetch按剩余时间执行；新35秒模式区分A批准截止与D执行截止，冻结2秒投递预留与可信MCP预算前置，不能在批准后越A时误终止。
- 新模式增加content_status/dropped_results，固定逐项舍弃及空/全无效/容量失败语义；默认旧模式不被共用归一化改变。
- E1–E7共7会话/8用户回合，最多17模型、Basic3/Pro3/Fetch3，REST部分0.105元；E5最多4模型。完整预算另含实际模型上界与R_native，241.421224元仅条件小计，不是完整预算。
- 复核官方文档后明确原生搜索在供应商服务端执行；单请求搜索硬上界未取得，当前收费准入未满足，不能发请求后再拒绝来规避费用，不能删工具造路由通过。
- 本轮前态和7份原文件备份已保存；原history、旧报告/evidence与旧台账不改。Desktop已有FEAT-166改动保持，不与本需求混合。
- 最终文档检查与复审结果见02、23及evidence/requirements-reaudit-checks-20261029.json；本轮产品检查/启动/生成/构建/收费均未执行，Git未提交。

以下历史日志按原时点保留，旧次数和预算不代表本轮授权。

## 2026-10-28 — Basic/Pro增量需求复审与落盘（仅文档）

- Owner要求再次审计方案并仍落为FEAT-162。本侧聊只获需求文档写入授权；不继承父线程的实施、提交或收费批准。
- 21号记录13项设计/共享工作区发现及修订，22号冻结三工具、模型选择、Basic正文、Pro筛选/chunks、共用期限、结果上限与计费边界。
- 保留原00及feature.yaml字节快照，新范围使用AC-021至030且全部pending；implementation改为pending，旧20号FAIL与三个关闭台账保持。
- 真实验收补齐Basic正文模式，完整集合为5会话/最多11模型/Basic3、Pro1、Fetch2；工具预算0.065元，模型预算另批。本轮实际供应商调用0。
- D0只作产品/UX与工程边界就绪检查，文档检查执行结果见02和evidence/basic-pro-requirements-checks-20261028.json；不宣称实现、真实路由或D4通过。
- 未修改兄弟仓源码/契约/制品/数据，未启动应用、读取Key或改旧台账；未提交/推送/发布，FEAT-165保持。
- 最后保护检查观察到Contracts/Host/Desktop并行出现FEAT-165相关dirty；第一次整体不变断言因此失败。相关变更不由本轮产生，未覆盖或提交；最终记录分别说明历史证据不变和共享工作区状态差异，实施前需重新对齐来源。

以下历史日志保留原时点语义，最新需求以00、21、22及feature.yaml为准。

## 2026-10-24 — 实施前

- 用户要求保留原生搜索，在Connectors/MCP接入Kimi Search/Fetch；先落完整方案再执行，不做无头浏览器，不改Runtime/Agent循环。
- 用户追加授权目录增加2项；容量62，实际新增一个服务含两工具，共61项。
- 已检查真实源码、官方API、相关仓库规则和工作区，记录baseline与来源摘要。
- `00-feature-brief.md` 完整方案先于产品代码落盘。D0工程内容已齐；不把用户实施授权当作付费/生产/Git授权。
- 实施待开始；外部收费调用0；真实验收NOT RUN。

## 2026-10-24T00:48:43.202509+08:00 — 开始实施

- 完整方案与feature.yaml已通过 `check-feature-package.sh --strict --gate D0`；证据 `evidence/plan-before-implementation.json`。
- 按契约先行、专用REST Backend、Desktop消费分工实施；生成/同步由单一执行者负责。
- 官方models文档确认GET与Bearer认证，未给出单独计费条款；仅作为基础检查，不宣称供应商保证免费或Search/Fetch业务已验证。
- 官方价格当前Search Basic和Fetch均为成功且有数据时0.01元/次；真实调用仍未授权、不执行。

## 实施审查修订

- 独立审查发现固定HTTP client底层reqwest存在默认协议重试。方案第11节先记录最小修订：Connectors直接使用锁内同版reqwest并显式retry::never，不修改Runtime、不升级外部依赖、不做故障注入。
- Contracts formatter正常检查曾等待stdin EOF。仅定向改为真实formatter读取正规临时文件，7项生成结果SHA一致；旧等待进程保留STOP_PENDING，未强杀。

## 本地实现验证与集成准备

- Contracts独立工具与62容量已生成同步；41 JS、5 Go包、Rust 4+7+7、lint/Clippy及source检查通过。7个完整breaking基线3个通过，4个受既有scheduled-plan-draft远程引用EOF影响，不能声称全绿。
- Desktop前端47/47、Native11/11、fmt/Clippy/lint/typecheck/build/docs通过；Host 4包普通命名allowlist race及focused vet通过。
- Connectors最终13项定向检查及5项普通回归、Go两包、Clippy通过；原传输默认重试P1独立复审关闭。
- 原App以Cmd-Q正常退出，ps确认Desktop/Host/worker/artifact子进程均结束。
- 首次Host候选freeze发现experts间接引用market-connectors的来源摘要过期，已由canonical generator/sync更新Desktop/Host/Skills的来源回执，11项专家业务输出字节不变；不改专家内容或政策。
- 首次canonical worker-build成功；资格描述补齐后重新通过canonical来源检查与构建。真实账户调用仍0。

## 专家资源来源级联收尾

- 标准装配暴露旧专家资源 pin 与已正规同步的 Contracts 来源回执不一致；方案第11节先补充仅限本地的来源刷新办法，再实现显式 `--refresh-provenance`。
- 旧 manifest、authority、75个归档与已安装资源先按原 pin 校验；旧 Contracts lock 和 Skills candidate 从 Git HEAD 读取且匹配旧固定摘要。新候选由既有 Skills canonical packager写入新临时目录。
- 完整75项资源元信息、75个归档字节、37个专家版本的内容审校与授权全等后，才以真实新 producer 记录生成 pin，复用原完整验证及安装；普通38项资源和旧73项保留基线未变。
- 新入口与原 `--check` 均通过，6项正常Node测试、ESLint、diff检查通过。审查指出原 `--package` preflight顺序回归，已恢复打包前的原pin/来源/schema校验并再次通过检查；没有通过删除校验或手改摘要绕过门禁。
- 证据见 `evidence/expert-provenance-refresh.json`。该修复不证明专家模型质量，也不新增真实调用。最终App来源回执须包含最后修复后的脚本字节；标准App构建与正常重开由root另行记录。

## 用户要求暂停

- 2026-10-24 用户明确要求“暂停执行，记录状态”，已停止后续诊断、测试、代码和界面操作。
- 最终canonical App编译、打包与来源回执通过；锁屏解除后实际UI显示本地服务未就绪，正常重试一次未恢复，连接器页不可用。编译成功不能视为启动验收通过，feature.yaml已更正startup为FAIL。
- 新连接器尚未安装，未配置密钥，真实供应商/模型调用0。
- 详细暂停记录、构建摘要、未完成项和恢复入口见04-resume.md。App保持现状，没有强杀任何进程。
- 子代理已停止、无运行中命令。暂停前确认Host专家manifest固定摘要仍为旧033689b0…，与新64721b4b…不一致；仅记录为启动失败遗漏候选，未取得本次错误证明，未继续修复。

## 恢复执行

- 用户明确恢复：先核对Host专家摘要、修复本地服务未就绪、完成连接器UI；真实收费API仍禁止。
- 当前进程观察未发现之前App/Host/worker/Runtime或rustfmt等待进程；本任务没有发送停止信号。源码已有变更保持。
- 确认Host固定旧manifest033689b0…而Desktop已64721b4b…；原freeze只记录Host来源字节而缺少与资源摘要的语义核对，拟按正规来源同步补齐。

- Host真实启动配置测试已以同一资源复现旧pin拒绝，并在canonical --sync-host-authority后通过。常量改为生成文件，freeze/build加入来源一致性只读检查，独立复审通过，见evidence/host-expert-authority-sync.json。
- 恢复后的完整启动先因Docker未运行、再因原六个容器退出255被标准脚本拒绝。通过原Docker正常启动及仓库已有recovery-plan/recover入口完成保护副本、数据核对、原服务启动和正常停止，无强杀/删卷/改源码。记录evidence/local-workflow-recovery.json，恢复ID542b525c-8cb9-4bea-aaf2-e3c5cd1e840a。
- 第三次恢复后canonical build正在运行，真实供应商/模型调用仍0。

- 最终canonical build及实际服务就绪PASS，市场61项正常；Kimi新安装、空密钥配置页、取消回传和对话禁用开关PASS。
- Cmd-Q正常退出，所有自有子进程结束；标准--reopen同构建回执及实际安装状态保留PASS。1180x760布局和键盘焦点PASS，窗口已恢复1268x780。暗色无现有UI切换入口，未改系统外观，记录NOT RUN。
- 仅本机新alias Keyring预检，未输入/保存密钥；models/Search/Fetch及模型回合均0。用户要求的本轮本地修复与UI验收完成，D4真实服务验收保持NOT RUN。最终证据evidence/app-resume-ui.json。

## Kimi模型Key复用调整

- 用户明确授权复用现有大模型Kimi Key，免重复填写，并要求方案先行；收费API仍不执行。
- 05-model-key-reuse-plan.md先于本轮产品代码落盘。本轮选择Host已加载Key→私有一次启动管道→Connectors进程内来源，配置阶段零HTTP，启用Probe仍单独执行。
- 记录现有FEAT-163等并行修改，不覆盖；本轮不派发子代理。

- 用户授权模型Key复用：先落05方案，随后provider/broker语义0.5.0及not_configured错误同源生成，Host已有模型快照经匿名启动管道交worker；取消Kimi独立表单和Auth自动Probe。Native/UI只本地绑定，保持未启用。
- 专家来源因provider schema来源摘要变化需再次刷新；generated/schema、75项metadata/archive未变。canonical刷新增加显式成对旧候选证据且以当前pin/authority验证，随后Host authority同步、资源检查和freeze通过。
- 首次真实UI绑定成功且无HTTP；发现静态not_configured提示误盖成功说明，已修正并通过84项前端回归，正在复构建/重开验收。此前首次构建已正常Cmd-Q退出，所有子进程正常结束。
- 最终本地配置UI与同构建重开全部PASS：配置不联网、不出现Key表单；已配置/未启用文案、任务选择禁用、最小窗口与键盘正常；最终Cmd-Q正常退出并释放共享App窗口。真实Kimi HTTP和模型回合均0。06报告、UI/诊断/来源回执及截图已落盘；其他Feature验收未代为声明。
- 收尾辅助broker-qualification编译发现credentials的隐式presentation子模块路径在独立crate root下不可解析；改为同一源码显式相对路径，无行为/依赖变更。编译和14项Kimi回归通过，再走canonical构建更新来源回执；暂未交接共享窗口。
- 收尾模块路径修正的最终canonical构建、真实worker本地绑定、同构建重开及界面确认PASS。最终Cmd-Q已结束所有App/Host/worker进程，源码与生成物稳定，窗口可交接；最新摘要已更新04/06及model-key-reuse-ui.json。
