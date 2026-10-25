# FEAT-164 当前组合与整项完成差距

## 整项目标与当前边界

整项交付是所有活动Kimi调用使用`kimi-k3.1-pro` / `kimi-k3-1-pro-max-v1` / max / 1048576，并从切换截止点起禁止旧K3出站；旧会话、请求、计划、授权和历史仍按原身份保存。专家、标题、草案、计划、工具回灌、图片、搜索、压缩、启用的子代理和Guardian均属于调用图，不能只验证新聊天。完成还要求正常恢复/退出/重开、可访问UI、兼容暂停回退及最终日常切换条件。

当前仍是独立候选，不是日常入口已替换。用户持续授权安全离线实施、必要修复、仅FEAT-164本地提交、不推送。真实HTTP新增0；累计30元、2/2已用、14.188544元unknown预占及14.328134元保守上界不变。候选原数据只通过正常App流程使用，事前完整副本仅用于只读审计，不作为降库或伪造旧状态的fixture。

## S4I 来源缺口及修复

初次准备将public-api-generator依赖误认为属于Contracts，新空目录准备停止；核对后仅移除本轮空目录，按Desktop实际路径链接已安装包，无生成/构建/模型调用。初次canonical media构建随后在Worker来源预检拒绝：Connectors `1f15726`的兼容名单只有Runtime r2 `074417e5`，未登记当前r4 `a28130a`。原S4h是ordinary生成子集，不覆盖Worker构建，不能据其PASS推定media可用。

核对原固定库`7fd463b`、r2与r4的`codex-rs`树均为`755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41`。最小修复为Connectors `7ea3df41818fd69f4736722d01f0686d584d1a71`仅追加r4完整commit到白名单；仍逐项拒绝未知HEAD、库树/工作区/依赖/Rust版本偏离。原工作区另一个需求的sourceCommit `9154f27...`逐字保留，未混入提交。Desktop `4398ddf1d5fc2cb16291764c2ca7595ec188ad15`同步两个显式检查器的精确来源，按既有generator更新独立catalog来源记录；60项catalog原字节不变，旧默认锁不改。

该修复`contract-impact=semantic`，属于已批准范围内私有构建来源兼容；没有改变公共wire、库源码、执行权限或依赖，整体breaking仍保持。6项检查器测试、ESLint、Worker来源校验和修正来源后的19项生成检查均通过。失败日志保留，不复写为PASS。新构建仍使用canonical脚本和新输出目录，旧bundle保留；具体结果续记于下文。

## 全部验收条件的证据账

下表区分工程实现、已有证据和仍需验证的产品行为。历史证据只按其原来源有效；并非本轮统一fresh run，所有Must AC仍pending，不能把多批子集拼成完整Gate。

| 条件 | 已有实现与证据 | 关单缺口 |
|---|---|---|
| AC-001 活动身份 | S1目录/profile/max/1M、当前v2投影及App普通新Kimi；19项来源检查 | 当前配对App新任务/显式往返已通过；最终活动入口切换，不能保留可执行旧K3默认分支后称已替换 |
| AC-002 配置保留 | S1精确前身、Home/trust保持；S4E新增writer标记阻止旧writer | 固定最终组合freshness及获准的日常升级核验 |
| AC-003 数据保留 | S2带数据15/29/37/38/39/40迁移与PK/FK/旧事实；S3 SQL41；候选历次只读比较 | 最终版本的适用迁移矩阵与日常库操作资格；不修改旧migration |
| AC-004 原thread切换 | S2 Native/Host/Runtime原operation回执/显式恢复；S4E旧loaded父子正常迁移 | 自然可达App旧K3/未决切换流程；没有数据就记未验，不改库制造 |
| AC-005 退役与取消 | S2 claim/send守卫、never-sent取消零POST；S4G实际attempted草案保持unknown且不重发 | App正常中断/后续已通过；其它可达的取消路径；never-sent领域证据不能冒称App演练 |
| AC-006 计划授权 | S3五项；S4H旧配置拒绝、取消审阅、保存paused、独立单次grant/run与重开 | 当前组合草案退出/重进已通过；真实旧K3计划App路径及最终freshness |
| AC-007 全调用图 | S4E原生终态/冷历史、旧父子与自动压缩；标题/Guardian/草案/计划调用身份 | 当前r4专家/媒体App及paused切换已通过；全调用面证据统一核对；不为测试启用禁用能力 |
| AC-008 内容与状态 | S4普通协议、input-only、工具/图片/搜索结构；r4 failed/interrupted真实原生事实 | 当前App媒体预览导出、正常停止/继续已通过；真实供应商图片/搜索/工具能力仍未验证 |
| AC-009 权限计量 | 共享Key引用、原审批链、恢复零调用、累计预算保留；本机路由覆盖辅助调用 | 最终完整组合计量/恢复核验；不得从30元余额推导新HTTP许可 |
| AC-010 完整交付 | canonical正常启停/重开、S4C亮暗最小窗口、暂停Kimi/MiniMax兼容回退 | 当前配对来源的重开/正常清理已通过；独立final三项；真实G2V、Gate及日常激活仍未完成 |

## 平台适用性纠正

本需求manifest登记的平台始终是macOS aarch64；Desktop仓职责明确为Mac客户端，Host固定Runtime支持目标为aarch64-apple-darwin。此前多处泛称“跨平台/其它平台未完成”，没有列出受支持的其它目标，不能据此无期限扩展需求。Windows、Linux及Mac Intel本轮记N/A（当前产品/Runtime支持范围外），不冒称通过，也不新增移植任务。Mac当前组合的App/UI、持久数据和清理要求仍全部适用；平台范围纠正不消除这些缺口。

## 可执行的收尾顺序

1. 先完成本轮当前r4 media构建、专家/媒体、正常停止/后续、同源重开及paused兼容；发现旧K3活动默认值则按最小范围修复和复验。
2. 按上述AC核对来源与安全可执行的现有测试，形成完整TCONF范围清单；真实服务与App未验项保持未验，禁止项明确原因和影响。旧日志与账本保留，不靠扩大harness制造完成感。
3. 安全离线工作全部具体化后，仅对必要的真实G2V/供应商验证和日常激活提出有明确次数、成本和数据影响的最后批准。当前没有这些新增授权，不能先调用或迁移。
4. final core、visual、teardown分别判定；最终以日常活动模型更换且历史/授权安全保留为完成目标，不以某个局部子集或本地提交数量为完成目标。

## 草案退出的实际回归与修复

当前media App正常进入“通过对话创建”时为K3.1，退出到新任务、再进入时实际显示“Kimi-K3（已退役）”且发送禁用。未发任何请求，原计划未改。定位到ChatPage退出草案watcher在共享composer分支写死旧profile；ordinary不走此分支，因此此前普通App验收没有覆盖。保留实机截图、原AX与修复前1FAIL回归，正常⌘Q退出0后才更改源码。

Desktop `7599c861cfce1aabfae3a3b50c95d563ac812747`仅将这处赋值改为已有`defaultModelProfile`，并补真实组件路由生命周期测试。该修复contract-impact=none：仅内存新草稿默认值，不修改已接受operation、历史、计划存储、wire或权限。候选回归1PASS、原非候选丢弃流程1PASS、相关模型/表单8PASS和ESLint通过；单一filter中的其它75项明确未运行，不伪称全ChatPage套件。回归同时验证普通聊天已选MiniMax不被草案退出改写，且没有select IPC。修复前App另存审计副本，最终canonical重建完成后按同源窗口复验；不靠截图或断言更改取得PASS。

## 专家历史切模型的真实缺口

7599c86/r4实际专家任务完成HTML/SVG发布、预览及两项导出字节一致；正常持续SSE经App停止后原生interrupted、部分文字保留，明确下一轮完成；PNG附件正控观察到1个input_image，合计6次loopback。亮暗最小1180×760检查通过，浅色已恢复。首次深色截图处于系统切换瞬间仍为浅色，该原图保留，不当作深色证据；有效深色为` s4i-min-dark-settled.jpg`。

同源paused重开后四轮/媒体/图片均可读，Kimi非空输入禁发，模型请求增量0。但对同一专家线程明确选择MiniMax失败，不能沿用旧ordinary PASS声明回退成功。正常只读刷新不发请求。App正常退出后，immutable SQLCipher副本核对：Kimi/ready/revision1，0个模型切换operation，4个市场投递全部accepted，专家ready；没有新unknown或可重发请求。最早阻断确认为Native `model_recovery::idle`调用legacy session排除器，任何市场/专家历史都被拒绝，早于持久化意图。

Desktop `54556bf3774bf04d4c1b92a02a2c7aa7f1e0478b`最小接通既有v2路径，contract-impact=semantic，遵守已批准S4身份迁移设计及既有Models/market/expert v2契约，无新wire/schema。legacy业务派发排除器保持；仅模型切换的v2事务改为核验市场投递已接受或具有既有cancelled_never_sent证明，未决/缺记录/未分类blocked仍拒绝。保留scope、turn/outbox、草案/计划、专家绑定、原请求与最终dispatch重验。SQL NULL issue_code按未知拒绝，不借空值取得许可。

修复前真实App拒绝与Native 1FAIL均保留。5项模型恢复（含8种市场状态、配置派发前重新核验）、12项原派发取消回归、Clippy和fmt通过。只使用正常临时SQLCipher与协议样本，无强杀、权限破坏、恶意fixture或真实模型请求。旧候选数据不直接改写；该同一专家thread的App复验未通过，后续真实结果见下节。

## Native/Host 配对准入与未决保护

54556bf修复后的同线程实机复验进入Native配置派发，但Host仍有`purposeOrdinary`限制；市场/专家实际记录为`purposeMarket`。Native原operation `f38666dc-d2d8-4101-b498-eccf3045b6dd`现为unknown，目标MiniMax、expected revision1；Host没有该operation回执。旧4轮历史/媒体保持。缺记录不证明未派发，因此不清除、不换ID、不自动或手动重发该操作；后续正向验证必须用独立新合成线程。`s4i-paused-fixed-selection.ax.txt`是失败证据，文件名中的fixed不能作为成功判定。

Host `090c2dbeeeceb0fc87e576d8e13f5c339bf106f0`在原Models v2实现中补齐settled market准入：MarketEnabled、持久scope/local-session、原expertBindingRuntime能力必须具备；保留idle/审批/未决market/expert/model/版本校验。先复用ClearMarketConfiguration撤销旧lease并关闭继承MCP，再以当次解析的专家资源及显式目标profile配置原thread；不调用PrepareMarket/BeginMarketTurn、不授新业务grant。后续业务仍走原Native授权与快照。普通、草案和未知purpose的边界不放宽；原unknown缺回执仍拒绝恢复。没有公共wire/schema/Runtime变更，contract-impact=semantic，整体breaking不降级。

12个Host定向测试/子测试及go vet通过，覆盖活动拒绝、paused→MiniMax、cleanup→switch、0业务turn增长、旧快照保持、终态只读重放。Desktop `399bb19d4c2066675f3f73b61ee6b8f59ee489c6`按canonical脚本锁定该Host；当前19项生成来源检查全部通过。

首次配对canonical构建在gofmt标准输入等待超过5分钟，未启动App。只读sample记录gofmt等待read、Node等待同步子进程；对已核对PID的构建子进程仅一次正常SIGINT，整条wrapper退出1。相同Go1.26.5/Node26的单项生成检查随即正常通过；根因仍未确定，不声称已定位工具链缺陷。一次独立日志的canonical重试成功（s4i-paired-retry-app-build-result.json），失败日志保留。没有强杀、程序替换、注入故障、源码/锁绕过或模型调用。

## 当前配对 App 验收结果

最终来源为Desktop399bb19、Host090c2db、Contracts1b357cc、Runtimea28130a、Connectors7ea3df4、Skills595c927。新建独立专家线程`01a173c3-2435-7e10-b778-52dcacdea4e8`，原ready专家与安全工作空间保持。第一轮实际出站K3.1/max，完成；正常⌘Q后同构建以Kimi-paused重开，历史可读/Kimi禁发，明确选MiniMax成功且模型HTTP增量0。下一轮实际MiniMax/high，完成。再次正常退出/同构建重开后两轮仍在，明确选择K3.1成功且0模型HTTP。最终SQLCipher为K3.1/ready/revision3，两条model operation均committed、两条market submission均accepted，专家ready。

原媒体线程仍unknown/revision1，原operation ID/目标/expected revision/阶段完全一致；四轮历史、两项媒体、输入图片和中断部分文字可读，发送禁用。新线程的成功不结清旧unknown，不以Host缺记录重发。已有conversation_warning泛化文案和空工具记录面板仍可见，未隐藏或冒称修复；其进度展示问题归FEAT-163，后续评审继续可见。

本轮App合计8次loopback（7次Kimi、1次明确选择后的MiniMax），0拒绝、0外部请求。读历史、模型切换和重开不新增模型HTTP。当前App/Host/Runtime与fixture均正常退出，18083/18086无监听；外观恢复浅色。图片/HTML/SVG只证明产品协议、展示与导出链，不能据此认定真实供应商能力。

## 当前来源的安全一致性与审查

原S4脚本已实际执行Host7、真实Runtime4/6次loopback、Native4，均通过且0skip。随后因调用者临时PATH遗漏已安装pnpm而停止，renderer尚未启动，原result保持IN_PROGRESS和实际三组结果。修正调用环境后仅执行剩余原命令：前端4、candidate-profile5通过。没有重复前三组或改脚本断言；组合24项通过的边界仍是原脚本声明的safe subset，不冒称完整TCONF-164-04一次运行通过。事实见s4i-conformance与s4i-conformance-remaining。

与实现分离的复审检查了：Native模型配置门禁不借legacy业务路径授执行权；accepted/有效cancelled_never_sent可达而missing/unknown/NULL标记拒绝；intent与dispatch双重核验；Host先撤旧lease/关闭继承MCP，再配置同thread，保留专家资源与未决工作检查；原终态回执只读、404不证明未发；默认模型复位只影响新草稿；Worker仅接纳已证明库树相同的完整wrapper。未发现本轮修复的新增阻断缺陷。真实App暴露的两层旧排除器均有修前失败与修后证据；这不等于独立人工Owner审查、完整源码无缺陷或全Gate通过。

只读保护审计：496项原dirty文件在扣除本轮专属差异后逐字一致；1118旧证据、154资源、7日常数据库、287旧bundle文件与5523候选备份文件未变；索引空、分支/remote未改。原计划/grant/run/selection共6条、旧失败草案、6条旧原生事实及原unknown操作不变。候选当前bundle与canonical receipt匹配。旧真实账本与14.188544元预占不改，新增真实HTTP0。证据为s4i-data-audit.json、s4i-preservation-audit.json、s4i-cleanup.json。

## 整项剩余执行单

| 顺序 | 下一步及判定 | 当前边界 |
|---|---|---|
| 1 | 将S1—S4领域/Runtime/App证据按当前最终来源逐项复核，补全TCONF-164-04覆盖表与适用迁移/取消路径；新增源码时只重验受影响链 | 安全离线可继续；不重跑已证明无变化的全部套件，不新增为过门禁而造的harness |
| 2 | 处理可达的旧K3 App迁移/恢复/never-sent取消与旧计划路径；没有自然数据的项目需明确安全替代证据和Owner接受边界 | 不改库制造、不给旧unknown换ID、不用新线程替代旧操作恢复 |
| 3 | 对最终来源执行最小真实G2V及必需供应商协议资格，记录图片/搜索/工具是否执行及actual usage | 当前2/2模型HTTP已耗尽；虽30元仍有余额，也必须有新的明确HTTP次数及成本上限才可执行 |
| 4 | 分别完成final core/visual/teardown，满足freshness后再进行明确批准的日常入口cutover | 当前日常数据库/入口尚未改；旧构建作为历史及兼容资料保留，不容许降级writer |

当前整项仍IN_PROGRESS，S4/G3、G2V及final不放行。用户目标是最终活动Kimi全面替换并安全保留历史，不是增加子集PASS数量；本轮关闭了真实发现的模型默认值与专家配置准入缺口，剩余项按上表推进。未执行危险/恶意fixture、权限破坏、程序替身或强杀测试；对应故障资格不以其它成功案例代替。

治理初检发现S4I证据只写HTML anchor、缺少验证器要求的唯一evidence注释，claims退出1；按既有格式补齐标记后claims与strict通过。实际G3/S4仍退出1，原因是未完成的前置slice、边界/纵向、完整TCONF和freshness，并未放宽门禁。元仓lint、53项测试与7个Shell语法检查通过。
