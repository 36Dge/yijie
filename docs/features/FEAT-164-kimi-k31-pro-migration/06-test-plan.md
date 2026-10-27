# FEAT-164 测试与证据计划

> 当前口径：完成状态、已接受替代、已移除及范围外项目统一见[当前验收矩阵](current-acceptance-matrix.md)。产品交付证据见[67](67-d5-entry-and-activation-implementation.md)、[69](69-d5-resumed-final-closure.md)，文档修正见[70](70-document-scope-reconciliation.md)。历史进度中的“当前”“下一步”仅指原报告时点，不覆盖当前结论或产生新的执行授权。

## 当前D5本机启用与交付完成（2026-10-27）

当前权威[67](67-d5-entry-and-activation-implementation.md)：D5已按Owner明确批准的ADR-0022个人本机范围完成。新日常入口固定Desktop39b0fbe/原Home，默认启用Kimi K3.1 Pro；真实正常启用、暂停回退和同入口再次启用均通过，3次正常退出及完整后态通过。0模型验收调用，原历史/授权/账本/预占及dirty保留，仅本地提交不推送。G4/G5本机就绪与G6实际交付观察分别留证；不授权公网/云端/多人/签名发布。以下66及更早阶段按各自时点解释。

## 第64号历史D3状态（2026-10-27）

以[64](64-d3-controlled-migration-and-post-state-audit.md)和[当前矩阵](current-acceptance-matrix.md)为准：一次D3已完成，原日常Native SQL37→41，后态完整备份/67旧业务表保持审计通过，D3_COMPLETE_STOPPED。没有GUI/Host/Runtime或模型调用；D4未授权/执行，D5和local G5/G6待收口。旧阶段授权及未执行描述仅代表当时状态，不许可重复迁移或自动回退。

## 60号历史D1实施结果（2026-10-27）

当前权威为[60 D1完成与离线资格](60-d1-daily-binding-and-offline-qualification.md)。59号D1已获批并完成六文件Desktop修正、安全测试和新canonical prepare-only/同回执复核；Host/Runtime采用已批准原Home绑定，daily不再隐式workflow-up。真实日常绑定未生成、D2—D5未执行、模型HTTP新增0、Runtime核心/补丁未改。原CUTOVER-01/03已离线修复，日常现场/启动资格仍无授权，G4不自动晋升。58接受的never-sent替代保留，完整App正向取消仍NOT RUN。

下方59及更早“尚未实施D1/原入口缺陷”按当时来源解释，不再作为当前D1未完成项。下一步仅在批准D2后进行完整冷备份和副本只读预检，不顺带迁移或启动。

## 59号历史日常切换边界（2026-10-27，S4AF）

以[59 日常切换方案](59-daily-cutover-minimal-plan-and-authorization.md)为当前部署权威。源码复审发现daily launcher将Host/Runtime Home改至候选新目录、与原Native日常库缺连续性；正常启动还可能隐式workflow迁移及恢复自动计划。日常activation为NO_GO，当前G4重新pending，先提限定部署入口修正及离线资格，尚未获准实施。58的已接受本地S1—S4/final证据与never-sent替代保持，完整App正向取消原执行仍NOT RUN；不是重新跑失败或取消Owner接受。

本轮仅方案和治理，无产品/Runtime改动，无日常数据访问/备份/预检/迁移/启动，无模型调用。阶段顺序为D1入口修正→D2完整冷备份与副本只读预检→D3一次Native维护→D4首次受限启动及退出核对→D5确认日常启用；D1—D5均未自动授权，具体边界见59。以下早期状态按各自时点解释。

## 58号历史已接受范围（2026-10-27，S4AE）

以[58 安全替代接受与最终收口](58-owner-accepted-substitute-and-final-closure.md)、feature.yaml和[当前矩阵](current-acceptance-matrix.md)为准。Owner明确接受57号never-sent正常Native API与生产消费链的安全分层替代；S4/TCONF04及三项适用最终验收按该方式收口，G4为本地代码完成。**完整App正向never-sent取消的原始执行状态仍为NOT RUN**，没有改写为已执行。原自然unknown缺Host回执，安全拒绝重发通过，原记录仍未恢复ready。

本轮仅只读审计和治理更新，真实/本机模型HTTP新增均0；产品、Runtime核心/补丁、来源锁不变。不启动或迁移日常库，日常候选保持prepare-only，G5/G6及正式交付仍pending。搜索答案正确性、亮暗/键盘/最小窗口专项保持OWNER_EXCLUDED，不恢复为待办。以下早期阶段记录按原时间和来源解释；本节覆盖其中过期的推进顺序、预算授权和“当前未通过”描述。

> 最新见[57](57-natural-unknown-and-safe-delivery-verification.md)：原隔离自然unknown的实际App安全拒绝已验证；正常Native入队/领取/取消/重开及真实输出消费链通过，完整App never-sent正向仍未执行。无真实模型调用、无日常迁移，旧账本/预占保持；不再对缺Host回执的原操作重复恢复。

> 当前结论见[56](56-current-evidence-business-state-and-daily-prepare.md)和[当前矩阵](current-acceptance-matrix.md)：当前来源/安全状态/实际历史重开及日常prepare-only已验证，0新增模型HTTP、不迁移日常库；完整unknown/never-sent App链仍NOT RUN，搜索答案正确性与外观专项已移除。下方编号阶段均保留历史含义。

> 当前见[55 测试修复与Owner范围调整](55-v3-test-and-search-grounding-root-cause.md)：旧v3测试已修复，28前端＋2client＋1原生reader＋19来源及lint通过；搜索答案正确性已明确从FEAT164需求/验收门槛移除，记OWNER_EXCLUDED，不计PASS、不再补试。三次真实调用保留，累计13、45元上限，旧账本/两份预占不变；全部服务正常停止，无待答交接。以下旧“质量未决/继续复验”仅为历史，不再作为本需求待办。

> 当前按[50 前三切片收口与日常部署方案](50-slice-evidence-closure-and-daily-deployment-plan.md)：S1—S3的G3已通过，S4完整验收仍缺；Owner已批准8文件日常候选实现及离线验证，明确不迁移真实日常库。此前状态按原阶段解释。

> 当前以[49 r5真实功能与日常边界](49-r5-real-qualification-and-daily-cutover-boundary.md)为准：Owner已明确授权必要真实功能调用且不要求精确查价；本轮1次r5真实42、保存/重开零补发和正常退出通过。旧账本/预占保持，日常迁移未执行；完整core/剩余业务状态仍按明确缺口判定。已移除外观专项不再作为门槛。

> 2026-10-26 Owner明确移除本需求的App亮暗、键盘/焦点和最小窗口专项验收；不执行、不延期、不计PASS、不作为完成门槛。模型选择、退役/恢复/取消、计划授权等业务状态行为与核心/数据/正常退出要求保持。当前实施和剩余项以[48](48-retained-runtime-qualification-and-scope-update.md)为准；下方旧阶段记录保留原时间含义。

> 最新以[45 旧隔离库受控迁移入口](45-controlled-isolated-migration-entry.md)为准：显式维护入口已实施，SQL29/37正常旧数据的拒绝/迁移/备份/重开离线资格通过；普通旧库门禁和日常拒绝保留。当前SQL41候选因1条未就绪选择与2份占用正常拒绝维护，原5522文件保持。实现仅在Desktop隔离commit bc3b097，主工作区未应用；真实/本机模型新增均0，完整App/G3/final仍缺。

> 当前权威见[44 自然旧K3与计划离线验收](44-natural-legacy-migration-and-plan-qualification.md)：r5已加载旧身份经实际Host切换、正常取消/恢复子集通过；自然SQL29计划经显式正式迁移后的退役/重审/新授权/取消及重开通过。旧库App入口仍明确拒绝SQL<38，完整S2/S3纵向未通过。产品/Runtime未改，真实模型0，本机合成8，旧账本与预占保持。以下旧记录按原来源解释。

> 最新按[39 证据绑定与三项最终验收](39-evidence-binding-and-final-verdicts.md)：当前来源141项＋4source和可达App验证通过，新增真实模型0；S1证据收口，S2/S3/S4保留完整纵向缺项。视觉单项PASS；core及Runtime checkpoint完整teardown未通过。两份真实账本、旧预占和日常库保持。以下旧记录按原时间与来源解释。

> 2026-10-26最新续办以[36 当前离线资格与下一步](36-current-offline-qualification-and-next-gate.md)为准：当前S1/S2/S3及S4专家/媒体/辅助/旧线程安全检查通过，产品代码未改；候选无旧K3会话/计划可自然升级。完整G2V/TCONF/final与日常cutover仍缺，新真实HTTP许可0；后续避免反复运行已通过子集。

> 最新续办与整项目标以[35 当前组合与完成差距](35-s4-current-media-and-completion-audit.md)、feature.yaml及S4I证据为准。旧阶段记录保留其原来源和时间；当前仍未切换日常入口，不新增真实模型HTTP。

> S4I结果：Desktop399bb19/Host090c2db配对专家切换、r4媒体/正常中断/图片、同源重开及清理通过；旧unknown仍保留阻断。当前安全子集分组通过不等于完整TCONF/G2V/G3/final。后续按35末节整项执行单推进。

> 当前（2026-10-25，S4f普通App与计划）：Host7927ee7补齐已有v2草案三路由，Desktop277f59e兼容读取原生事实2/3/4；Runtimea28130a r4与Contracts1b357cc保持。同源App验证旧历史、input-only草案、只读恢复零补发、关闭保存、单次执行、取消编辑和正常重开；App模型协议loopback共3次，真实新增0。旧失败请求/事实/账本保留；完整恢复取消、旧模型计划、专家媒体当前组合、平台/G2V/G3/final仍未通过。权威见[32](32-s4-r4-app-plan-acceptance.md)。以下记录保持原来源与时间语义。

> 当前（2026-10-25，方案A原生终态修复）：Runtime r4 a28130a → Contracts1b357cc → Hostb9155a3 → Desktop2fb8989已本地固化。原子代理错误被completed覆盖及冷历史丢失失败已修复；10项核心、269 schema零差异、7项原生/23次本机HTTP证据复核、3辅助/9次与4调用面/6次均通过。新增受管writer标记阻止旧r2候选写入新历史；不改旧历史。全轮50次合成本机HTTP、真实新增0，旧账本/预占保留。App本批仅构建，完整UI/计划/恢复取消/平台/G2V/G3/final仍未通过。最新权威见[31](31-s4-native-terminal-repair.md)及feature.yaml；以下旧阶段保持历史含义。

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S4专家/媒体/辅助续办）：专家pin已按Skills595c927不可变同内容来源修复；Hostcac2d4d、Desktop56f5284、Connectors1f15726已仅本地固化。四组合source、37专家版本安装/解析/重开及专家/媒体/原生辅助调用安全离线验证通过；S2/S3/S4当前源回归通过。完整TCONF-164-04、App/平台/G2V/G3/final仍未完成，真实模型新增0，旧账本/预占保留。最新见[28](28-s4-expert-media-auxiliary.md)及feature.yaml；下方段落保留各阶段历史范围。

> 当前（2026-10-25，S4）：Contracts eddc64f → Host9ffcb6f → Desktop704cfdb/e408047已仅本地固化全调用面接线；安全子集7/4/4/4/5、S2和S3当前源回归通过。完整TCONF-164-04、专家资源/媒体、辅助动态调用、App/平台/G3/final仍未完成；真实模型新增0，旧账本/预占保留。最新见[27](27-s4-call-surface-wiring.md)及feature.yaml。

> 当前（2026-10-25，S3）：Contracts2dd214d / Desktop4d04597已本地固化计划退役、SQL41和授权保护；TCONF-164-03五项、70前端及当前源S2复验通过。App/UI/平台与完整G3仍NOT RUN，真实模型新增0，旧账本/预占保留。最新见[26](26-s3-plan-retirement.md)及feature.yaml；下面旧阶段结论按原来源保留。

> 当前（2026-10-25，S2时序与真实本机边界）：TCONF-164-02五组组合已在Host 57c29ea/Desktop ddc840f干净来源通过；正常Host/Native重开与取消零POST验证完成。平台/UI仍延期、完整S2 G3未过，下一步可离线推进S3。真实模型新增0；详见[25](25-s2-conformance-and-native-boundary.md)及feature.yaml，下面保留阶段历史。

> 当前（2026-10-25，Native恢复接线）：Desktop f341636已完成SQL39新意图、只读查询和显式恢复，定向检查通过；旧pending不回填，已发/未知且404不重发。App未重建，平台UI继续延期。完整S2还缺never-sent证明与取消，G3/final未通过。最新见[23](23-native-model-recovery.md)和feature.yaml，较早记录按原来源保留。

> 当前（2026-10-25，UI延期/S2基础）：Owner允许锁屏所需步骤延期并先推进离线实施，UI仍NOT RUN。Host Store11、v2原回执/显式恢复及带数据SQL升级验证已本地固化；Native恢复接线/never-sent取消、S3/S4与完整G3/final尚未完成。真实模型新增0。最新权威见[22](22-ui-deferral-and-s2-foundation.md)和feature.yaml；下方旧阶段记录仅按其原来源和时间解释。

> 当前S1（2026-10-25）：源实现、local/boundary及canonical构建已完成；本机新Kimi正控通过，暂停/MiniMax/重开及最终清理因Mac锁屏未完成，S1 G3不放行。新增真实模型HTTP为0，旧账本逐字保持。最新来源、未执行项和续办见[21](21-s1-implementation.md)。下方20及更早阶段结论按原来源和时间保留。

## 历史有效状态（2026-10-25，30元单次续验）

| 项目 | 当前结论 |
|---|---|
| 来源与工程门禁 | Runtime r2 / Contracts / Host固定；Desktop40908c7独立固化；G2A及当前Harness PASS |
| 真实G2V | 本次新增唯一HTTP200，正确答复42、usage/保存/重开/无补发/正常清理及组合oracle PASS；r1 FAIL保留 |
| 预算与请求 | 累计30元；仅新增1HTTP已耗尽。旧预占14.188544元＋本次保守0.139590元＝14.328134元；不再新增请求 |
| 已通过历史 | r2 canonical实际App本机合成答复、保存、重开、正常退出；不等于真实模型通过 |
| 尚未完成 | S1—S4、TCONF-164-01—04及三个final；不放行日常库迁移或发布 |
| Git | 仅FEAT-164本地提交已获授权，不推送；保留其它需求改动 |

本轮权威为[20 单次续验](20-budget-resume-and-g2v.md)、feature.yaml和追加后的真实账本。13—19按各自时间与来源保留历史语义。TCONF-164-01—04仍为计划目标，执行前核实selector存在且测试命中数非零。

## 分层验证

| 层级 | 覆盖 | 所需证据 |
|---|---|---|
| Contract | 活动/历史身份、旧header与新执行、封闭enum、market/expert/plan引用、unknown/retired区分、来源锁 | source-first生成diff、lint、逐支持baseline breaking、方向conformance |
| 普通单元 | 配置前身/双文件过渡、CAS/revision、lost receipt状态机、never-sent证明、grant领域更新、claim/send准入 | 审查过的安全allowlist与非零执行数，逐AC结果 |
| 私有迁移 | 旧基础/29/37库正常前向、新库重开；原列/主键/外键/原payload/digest保留；兼容回退reader | 合成数据库正常事务；不复制用户私密库为fixture，不破坏权限 |
| 实际Runtime本机协议 | 新候选start/resume/turn、SSE/function/web sources/图片、previous_model压缩、启用子代理/Guardian路由 | canonical binary和普通本机HTTP server；真实请求解析，明确非供应商资格 |
| G2V | 最小真实App→Host→Runtime→新模型→返回→保存/重开链 | qualified H-F164-LOCAL、精确refs/平台及批准的合成数据真实调用 |
| final core | AC001—009；主聊/标题/专家/草案/计划/工具/图片/搜索/旧历史 | 同一source组合；完整request-call-result关联及正常恢复 |
| 业务状态显示 | AC010；模型选择、退役/暂停、错误与恢复的行为判定 | 不包含Owner已移除的亮暗、键盘/焦点和最小窗口专项，不以未执行这些专项阻塞完成 |
| final teardown | AC004/005/010；正常取消、退出/重开、无在途/重复派发 | 正常EOF/应用退出/实际状态；不能以强杀获得结果 |

## 正常状态案例

1. 空库/新聊天，新身份精确；MiniMax往返保持provider匹配。
2. 已知旧catalog/TOML及可达混合组合正常升级；以普通内存值测试未知配置拒绝，不篡改用户配置造故障。
3. 旧idle会话、已完成回执、已知退役身份、pending/uncertain、missing但不能证明未发分别处理。
4. 通过纯函数/正常协议driver传入“Runtime已回执但Host未提交”等状态，不靠杀进程模拟。
5. 定时plan的paused/enabled、future slot、已占run snapshot、授权digest和旧revision保持/失效符合领域事务。
6. worker启动前/claim前/send前的准入与普通恢复查询并存，退役操作不被反复增attempt。
7. 标题与切换并发的正常顺序、Guardian在auto模式下的模型路由、整个已启用代理图正常收敛。
8. 预算内文本/图片/合法工具/搜索、流式done及completed/failed/incomplete如实显示；无攻击载荷。

## Harness资格和安全替代

H-F164-LOCAL默认禁用；production_bootstrap表示产品canonical启动链，不是生产网络或新权限。需验证product_failure/harness_failure/platform_failure/gate_failure四类结果、正控、正常超时及cleanup、无正文判定。使用普通无副作用返回值、纯状态输入和正常取消验证分类；禁止强杀、二进制替身、权限破坏、危险fixture。不能安全验证的项目列NOT RUN/原因/影响，阻断对应Gate，不伪造例外批准。

## 真实费用与副作用

历史S4K（已被S4V授权更新）：schema3当轮3/3及累计5/5均已用完，当时估算14.679001元、当时没有新增HTTP授权。原schema2与预占保持，下一次付费调用需新明确授权且不得重置账本。下段保留2026-10-25旧schema2的历史范围。

当时批准累计30元、总模型HTTP最多2次（已有1次＋只新增1次），覆盖标题、Guardian、压缩、子代理、工具后续及重试；任何额外HTTP均拒绝。此次只发1个普通文本回合，输出上限8192、原生搜索移除，不使用图片/工具。搜索与图片授权仍保留，但本次不消耗；不得以剩余资金增加调用。旧unknown预占不返还，失败即停。账户资格/余额未知，不自动查账户或充值，不借前序Feature余额。

使用实际预算计量器须先审查其旧model白名单和是否注入max_output_tokens；原始产品请求与预算覆盖测试分开。缺用量按未知，不能按0计；没有cache_write_tokens时不宣称精确费用。失败不自动加额度或更改max档。

## 验收解释

通过阈值是AC全部可判定满足、三个final verdict分别PASS且refs fresh、没有退役请求/历史错写/重复执行/秘密泄露。模型质量仅对获批任务记录结果，不能预先说升级解决FEAT-163。未启用能力不为验收启用，其禁用事实要由effective配置证明。所有相同失败累计三次进入RCA，原记录保留。

## S4g 旧草案状态续办（2026-10-25）

本轮限定验证2项Native状态、1项原writer回归、32前端、lint/fmt/lib Clippy/build/docs及当前App亮暗1180×760。完整通用generate失败/RCA保留，未跑攻击/故障注入和真实模型。见33与s4g证据。

## S4h 生成入口与计划验收（2026-10-25）

本轮19项生成、6项配置测试、S3五项、18前端、当前ordinary App计划审阅/单次授权/重开通过；1次模型loopback，真实0。旧K3产品UI与完整恢复取消/媒体仍单列未验，详见34。

## S4M正常关闭候选验证（待实施）

40号追加四池、日志clone/queue排空、正常stdio等待及same-source重开验证；本轮仅未修改r4的一次零回合EOF和4个只读integrity_check。不得把S4M审计完成改成teardown PASS；真实HTTP授权仍0。
