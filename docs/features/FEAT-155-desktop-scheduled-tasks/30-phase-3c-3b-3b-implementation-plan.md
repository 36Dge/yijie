# FEAT-155 · 下一步执行方案：3C-3B3B 原生装配与草案恢复

2026-09-19。用户本轮要求“给出下一步执行方案”。本轮只读复核源码、保存方案和检查文档，不开始产品实现、服务启动或模型调用。建议下一次只实施本方案，完成后报告停止。

当前起点是[29资格修复结果](29-draft-runtime-unblock-report.md)：精确本地候选的原生input-only与Host消费已验证。尚未接通的是同一Desktop/Host原生候选的启动装配、attempted草案只读恢复与来源重发现。完成这些后，再推进页面与真实Provider验收，避免页面依赖一个只能在构造器中使用的后端。

## 1. 目标与范围

本批交付：在同一个native scope、SQLCipher worker、原Coordinator、受管Host及29的Runtime候选上，闭合“原生装配 → 只读恢复 → 查看可信草案来源 → 显式确认保存paused计划”的后端路径。恢复查询不能自动重发模型请求，恢复绑定不能伪造原发送实例，确认保存不能顺带启用计划。

包含 Contracts 最小恢复源、Host启动/查询、Desktop装配/恢复/最小typed IPC及正常验证；Runtime只消费29精确产物，不再改内核、升级或启用experimental。页面、真实Provider调用、日常库激活、防空闲睡眠、应用内更新和已延期系统通知不在本批。原两种创建方式、三种运行目标和定时/手动执行设计保持。

本轮文档 `contract-impact=none`，不改变产品行为；未来本批按最高风险 `breaking`保守审查：原生候选装配及封闭IPC的能力/恢复解释改变，不能仅因增加GET称整体additive。新增Host只读端点本身为独立additive边界，旧两类恢复查询不改。

## 2. 源码事实与设计裁决

| 事实 | 本批裁决 |
|---|---|
| Host `cmd/desktop-host/main.go:53–121`未传草案Store选项或workspace root；能力存在但正常装配仍不可用 | 补同一入口的原生候选装配，模式选择、scope/受管目录/HostHome在打开存储前核验；普通入口仍Store5，候选6，读取6不降版 |
| Desktop `chat/worker.rs:290–395`有draft/dispatch/trigger三个独立候选构造器；普通`chat/mod.rs`未统一选择 | 收敛为一个原生候选装配方法，复用原worker/Coordinator，不开第二数据库或执行器；读取/保存/手动/自动/草案资格分别计算 |
| 通用mapping GET不含purpose/workspace/schema/policy；POST create在记录缺失时会真实创建 | 新增草案专用只读mapping GET，复用现有Store持久字段；不可用POST模拟查询。operation GET继续复用 |
| `application.rs:1864–1872,2112–2124`草案请求尚未接最后POST准入，token/readiness等待可能发生在旧检查后 | 把草案create/resume/turn接入原发送admission路径，异步准备后重新核对用途/身份/epoch/当前授权，不依赖早先capability检查 |
| `drafts.rs:449`只持久化attempted；来源账本不在run恢复扫描内 | 为草案来源增加有界扫描，复用原恢复观察与组合提交。已尝试操作不清标记、不因租期到期重新进入发送 |
| `chat/mod.rs:591–620,671–701`候选恢复可能直接POST resume | 启动先执行只读恢复；attempted/pending/unknown不能进入自动create/resume/turn。显式继续时才按固定用途重新核验并恢复 |
| `drafts.rs:271–369`预览需要精确绑定、完整final_answer与completed原生事实 | 不把partial冷历史或最后一条assistant文本变成候选；持久事实不足明确不可用/未知，不补造通知 |
| SQL22已有scoped source/session、operation、确认墓碑及原生binding可空来源字段 | 本批优先保持SQL22/Host6；原发送generation缺失时保留unknown/null，不拿回应实例填入。不要为“全都能恢复”预设SQL23或Store7 |

上述是本轮源码事实，不继承25中旧Runtime“仍不具备资格”的当前解释；旧报告保持阶段历史。29的binary与manifest摘要本轮只读复核仍吻合，验证结果不自动等同Provider或产品发送资格。

## 3. 实施顺序和完成标准

| 顺序 | 实施内容 | 完成标准 |
|---|---|---|
| 1 | 最小恢复与能力契约 | 草案专用GET同源生成；私有IPC补来源重发现、分操作能力/原因及未尝试原turn的显式继续；旧公共查询与固定outputSchema不变，strict校验与定向consumer检查通过 |
| 2 | 同一原生候选装配与最终发送准入 | 同scope、同受管根、SQL22/Host6、原Coordinator和29产物贯通；最后POST前重验用途/身份/epoch/授权，撤销不误发；普通入口15/5不迁移、不自动开放发送 |
| 3 | attempted草案只读恢复 | 精确核对task/session/workspace/schema/policy/operation/thread/turn；accepted仅补已证实绑定，pending/uncertain/404/不可读保持未知；恢复扫描中create/resume/turn POST计数为0 |
| 4 | 原生观察、来源重发现与确认闭环 | 复用原订阅/唯一事实缓冲；重开能查回已有source并读取可信候选；显式继续重新核验资格，旧操作不重发；确认重复/并发/重开仍只产生一个paused计划，删除墓碑不复活 |
| 5 | 零真实调用组合验证与报告 | 临时SQLCipher/bbolt、声明式HTTP组合和真实Host/Runtime无模型生命周期分开记录；旧聊天/权限/原outbox回归通过；结构化审查、来源摘要、限制和回退有实际证据，随后停止 |

### 3.1 最小契约定义

推荐新增 `GET /v1/scheduled-plan-draft-sessions/by-task/{task_id}`，仅owner bearer、本地原生受管Host，no-store、无query/body。源放在现有 `draft-execution-v1.schema.json`及`scheduled-plan-draft.yaml`，机械生成/同步Go、Rust、TS和严格校验器，不手写影子DTO。

回执仅包括：固定草案purpose、schema_version、policy_version、task_id、agent_session_id、workspace_id、reserved/bound、可空codex_thread_id，以及可空responding_host_instance_id。字段取自同一bbolt只读快照，先验证持久用途；普通用途明确冲突，缺失不证明从未执行。读取不依赖Runtime ready、目录解析或草案发送资格，不调用原生RPC、不修改记录。Store6现有字段足够，不增加Host存储版本。

Desktop先依据原生scope与受管HostHome/实例关系准入，再比对回执与本地账本。responding_host_instance_id只证明当前响应者，不能证明旧操作来自这个generation。缺少响应者或受管Host关联证据、未知schema/policy、用途/workspace关联不符、身份冲突时，保留原事实并拒绝绑定。

私有IPC沿Desktop `scheduled-task-ipc-v1.schema.json`唯一源：一个只读来源查询按当前scope下的本地conversation/turn查回source；一个只读能力查询（或对现有同类投影作最小版本兼容扩展）分别给读取、保存、手动、自动、草案可用性和原因；一个受限继续命令仅解开“create已证实接受、原turn从未尝试”的来源，行为见3.3。renderer不提交path、任意配置、原生ID或授权凭证；返回可用也不替代提交时重验。所有受影响的封闭响应/命令同时生成并核对Rust/TS，不扩建通用资格平台。

### 3.2 装配与数据边界

原生候选路径沿既有canonical launcher/ChatRuntime/受管sidecar扩展，由native计算scope、受管工作根及存储模式；Host部署参数的唯一源在Host配置说明/校验，Desktop传递相同受管值。不能由WebView参数、普通DB版本或单一环境布尔量直接授予出站资格。29的artifact pin、受管配置、当前generation及原生策略回执仍是必要条件。

先形成并验证统一构造方法及同一真实Host入口接线；本批只以拥有的临时数据执行候选路径，日常入口默认目标保持SQL15/Store5，不读取/迁移日常库或访问Keychain。复用现有可注入key-store及原生构造依赖，不建第二测试App。候选22/6兼容reader保留；候选writer不改变默认开库版本。

读取与恢复不依赖Provider；保存依赖当前native写授权；手动/自动仍保留版本、目标、额度和生命周期校验；草案仍保留用途、目录、fixed schema及29的真实策略检查。本批装配能力不会为已有启用计划开启自动派发，也不会把Host策略ready标成Provider outputSchema已验证。

最后发送准入沿原 `DispatchAdmission` / `admitted_host`扩展草案用途：create/resume/turn完成token/readiness等异步准备后，再核对native scope、workspace、用途、operation、当前Host/Runtime代次、生命周期和授权。claim和最终POST还必须持有本代显式submit/continue产生、绑定source/operation的原生发送资格；重开默认没有，睡眠/停止/授权变化使其失效，观察资格不能替代。create/turn通过最终检查后才持久记录attempted并紧邻实际POST；一旦记录attempted后结果不明，继续保留unknown，不能因“可能没发出”重置。resume只允许显式继续且没有未决提交，不复用过期UI授权。等待期间撤销/睡眠/停止/实例变化须拒绝，原普通聊天/定时run准入继续有效。

### 3.3 恢复与观察不变量

- 按scope、非删除source及原outbox关系有界分页，使用稳定cursor、单轮上限和现有请求超时；复用同一Coordinator生命周期，不另建常驻恢复服务。查询await后在同一worker重新核对版本、删除、授权和原关联，再提交。
- create已尝试：先查草案mapping；reserved、缺失和失败均不再POST create。bound且用途/工作区/版本吻合，只关联返回的session/thread，不默认为后续turn授权。
- turn已尝试：先确认草案mapping，再查原operation；accepted的turn ID必须吻合原操作，不代表终态或可保存候选。pending/uncertain/404/部分历史均不自动重试。恢复只补事实，不推动从未尝试的后续turn发送。
- **恢复create只绑定事实，不排队turn。** 现有`bind_host_session_in_transaction`即使recovered=true也会插入pending start_turn；必须拆开这两个职责。推荐持久hold为“create事实已关联、原start_turn出站尚未创建”，原加密create payload和source/local turn仍保存；不得伪造failed/cancelled或清attempted。原start_turn已存在时仅回查，不能由恢复放回pending；即使它原本pending且turn_attempted=0，也因重开后没有本代显式发送资格而不可claim，不能依赖“不重排”假定不会发送。
- **显式继续只处理未尝试的原turn。** 推荐Desktop私有`scheduled_draft_continue_source`接收source_id及既有原生context，不收路径、身份或替换正文。原生再次查证mapping、用途/版本/workspace、该来源无未决turn且原turn_attempted=0、当前UI/native授权和生命周期有效，才在同一事务复用原加密payload与原operation插入唯一start_turn；原出站若已存在则复用，不重复插入。重复调用只回查原关联或复用尚有效的同代资格；已尝试/unknown不授新资格、不入队，已知回执可幂等返回，未知明确阻断，不能把“继续”变为重跑。澄清后追加用户文本仍沿既有DraftSubmit产生新的source，不改旧历史。
- **无原发送来源的观察也必须精确准入。** `stream_native_conversation`当前仅为scheduled run放行NULL origin；不能把这个例外泛化为“有Runtime ID即可恢复”。新增草案观察资格仅由本轮核对的scoped source + 专用mapping + accepted operation精确组合产生，绑定当前Host及生命周期，失效即重验；沿原订阅与事实缓冲观察，不把临时资格当历史发送generation。
- 已有原发送generation保持；缺失留unknown/null。现有回执和新Host nonce不能填补历史来源，不能借恢复释放未知占用、清attempted或伪造failed/completed。已证实的accepted绑定可复用`bind_started_turn_with_origin`语义，通过窄的非测试恢复入口显式写`None`来源，不调用携带当前nonce的普通受理路径冒充原代。SQL22是否足以表达本批恢复提交必须由定向测试验证；若发现必要持久语义确实缺列，应先记录具体缺口和最小前向迁移评估，不能直接改旧migration或暗加SQL23。
- 启动与只读查看不POST resume；明确继续且未决状态已被可信证据排除后，沿原draft resume重新验证实际策略。普通会话沿原路径，候选不可用不拖住旧历史读取。
- 原生final/terminal事实已持久化时重开直接重用；缺事实保留未知，不用冷历史重建第二套事实。确认仍只保存paused，来源唯一性、摘要、幂等回执和删除墓碑沿B2同库事务；不自动grant、enable或run。

## 4. 验证方案

1. 先运行适用leaf源生成/同步/strict conformance；仅在涉及源变化时运行相关lint和登记基线兼容检查。总生成入口已有dirty保护继续保留，不能清理用户工作区绕过。
2. 临时SQLCipher22/Host6正常写入、关闭、重开；普通15/5及旧聊天读取兼容；同一native构造器的操作资格分开验证。普通路径无草案发送资格、候选目录/版本不符、缺策略证据均在I/O前拒绝。
3. 声明式进程内HTTP fixture验证草案mapping、原operation查询和binding提交，正常格式变体覆盖reserved/bound/accepted/pending/uncertain/缺失；对已attempted恢复及后续Coordinator轮次/SSE内轮询统计POST=0；检查恢复create不会生成可claim的原turn，也检查重开前已经pending但从未尝试的turn不会被后续轮询发送；显式继续只能解开未尝试的唯一operation。通过正常授权撤销/生命周期状态变化检查最后POST保护；不存在故障注入、强杀或伪造二进制。
4. 使用真实构建Host和29固定Runtime，仅做无模型create/read/必要显式resume及正常退出重开；真实文本Provider仍NOT RUN。完整文本投递组合用现有fixture单独验证，不为零调用测试新增Provider绕行入口，不把fixture当真实生成/产品D4。
5. 正常完成事实、来源重发现、重复确认、删除关联以及未知历史验证后，执行旧聊天/权限/原outbox定向回归、必要编译/格式检查和结构化审查。运行检查前核对是否含用户禁止fixture；未执行的全套故障/攻击测试写明原因与影响。

没有充分终态事实的旧unknown会继续unknown；本批不承诺将所有旧草案恢复成candidate，也不为强恢复释放而增加generation账本。

预计完成标准以证据为准，不以新增测试数量或全仓full-green代替用户结果。本批真实文本0次，额度累计0/12保持，图片/商家/MCP外部0；后续Provider验收再从既有总预算中明确分配，不新申请已授权总额度。

## 5. 交付、回退与后续

交付包含源/生成物、最小装配/恢复代码、测试和下一份实施报告；报告分别列合成组合、真实无模型进程证据、Provider未执行及Must仍pending。全程不提交/推送/tag/发布，不改固定候选二进制，不扩大到页面和系统通知。

关闭候选producer后保留SQL22/Store6兼容reader和历史，不降级库、不清空数据。只读恢复失败不自动启动/切换Runtime；正常退出超时保留所有权和恢复状态，不强杀。完成后报告并停止，再进入既定页面与真实验收工作，FEAT-155完整D4仍以全部Must用户路径为准。


## 6. 方案审查记录

本轮主代理源码复核与两项并行只读审查分别核对Desktop装配/恢复和Host契约；不是独立人工批准，没有实现或运行产品测试。审查发现并纳入三项必要约束：最后POST前再次准入、恢复create不得隐式排队turn、NULL原发送来源须专用精确观察资格；末轮还补上“已存在pending未尝试turn需本代显式发送资格”，避免重开后由后续轮询误发。显式继续的持久hold采用原出站未创建与唯一operation表达，优先保持SQL22，不为强恢复释放扩建generation账本。方案的文档门禁、链接和起点文件保护证据另行保存；这些检查不代表本批实现或D4通过。

本轮方案检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、134处本地链接和五仓diff/起点保护均通过。四个产品仓起点文件逐字节未变；仅更新需求文档。详细来源及检查见[只读方案审查证据](evidence/phase-3c-3b-3b-plan-review-20260919.json)。

## 7. 实施接续

用户随后明确批准本方案，3C-3B3B已完成并停止；实际接口命名、检查、限制和原生空历史修正以[31实施报告](31-phase-3c-3b-3b-implementation-report.md)为准。本方案开头的“只读/未开始”保留为规划时点事实。
