# 易界项目 Codex 长期协作记忆

## FEAT-164 旧 daily-source 已安全清理（2026-10-28）

当前清理后态以[78](../features/FEAT-164-kimi-k31-pro-migration/78-old-daily-source-retirement.md)为准。Owner已明确授权审计、精确列清单后清除；旧`yijie/.local/daily-source/20261027-01`及8个worktree已正常移除，无force/prune。完整75,547项归档独立恢复完全一致、五仓bundle重新独立恢复/fsck通过；归档在`yijie/.local/daily-source-retirement/20261028-01/`，保留原Git引用、12原仓、原工作、账本和预占。旧来源如需回退须从归档恢复并重新注册/审定，旧.git指针不能复用，不能覆盖日常库。

原主目录generation20261028-02和`pnpm daily:open --generation 20261028-02`不变；清理后19项来源、1410项输入/制品、正常/暂停D5绑定只读检查通过，三个活动日常Home的5,629个普通文件逐项保持。本轮未启动App、未探测workflow、未调用模型；锁屏UI跳过及原接受替代/移除范围不变。下方76的“旧daily-source保留”仅表示此次清理前历史状态。

## FEAT-164 原主工作目录构建运行完成（2026-10-28）

当前以[76](../features/FEAT-164-kimi-k31-pro-migration/76-primary-workspace-execution.md)、[77](../features/FEAT-164-kimi-k31-pro-migration/77-primary-system-quit-root-cause-and-plan.md)及[当前矩阵](../features/FEAT-164-kimi-k31-pro-migration/current-acceptance-matrix.md)为准。原CrossBSD/yijie-desktop实际源码Desktop24a231f、Connectors8e62101，generation20261028-02，仓内`pnpm daily:open --generation 20261028-02`正常启用Kimi，追加`--pause-kimi`暂停；不转调daily-source，不重建已缺失的桌面.command。原WIP501项已恢复核验，254源码在五仓retained/primary-wip-20261028-01保护提交及bundle，4缓存独立保全；当前主目录选择已审FEAT164基线，未采纳其它需求不自动启用。旧daily-source/原仓/新归档/bundle保留，本轮无目录清理。

三轮新来源真实服务/模型目录、正常退出和完整数据后态通过；修复Desktop标准Quit AppleEvent绕过ExitOwner的缺口，Runtime核心/补丁不改。活动WAL/SHM0，App最后停止，旧历史/授权、七账本/两预占保持，新增模型HTTP0、不推送。Mac锁屏使App历史界面观察按Owner指示跳过，不记PASS；既有never-sent接受替代、完整App正向取消NOT RUN与永久排除项保持。初始generation01退出失败及完整WAL副本保留，后续修复不改写原结果。下方旧入口和阶段状态均按历史时点解释。


## FEAT-164 D5恢复收口完成（2026-10-27）

Owner要求恢复后，按[69最终收口](../features/FEAT-164-kimi-k31-pro-migration/69-d5-resumed-final-closure.md)完成68剩余事项：修正G5历史措辞，Accepted ADR精确Feature scope限定的最终57测试、claims/strict/G6/lint/7Shell均通过；500原dirty/混合memory原文/7账本与六源制品、两个入口、原日常文件及最终sealed一致。App无活动进程，0新增App/模型/workflow操作、无数据库API打开；workflow ready仍仅指67观察时点，不自动恢复。D5及ADR-0022个人本机范围完成，入口为桌面易界 AI.command，暂停入口须先正常退出再切换。仅本地固化本需求差异、不推送；Runtime/已签名App/旧备份不改。以下68暂停状态保留为历史，不再是当前任务状态。

## FEAT-164 暂停于D5最终治理收口之前（2026-10-27）

用户要求记录并暂停。以[68暂停记录](../features/FEAT-164-kimi-k31-pro-migration/68-paused-state-20261027.md)为最新恢复入口：D5三轮启用/暂停/恢复及正常退出、完整后态审计已通过，App最后已正常退出，入口保留；0新增模型HTTP，旧改动/账本/预占保持。元仓HEAD7a2b7c3、Desktop39b0fbe；当前索引为空，收口差异未提交。

最后Feature scope限定修正仅完成focused检查；全量最终治理/G6、保护复核、证据索引和本地提交未执行。feature.yaml G5当前措辞尚有启用前残留待修正，G6=pass为观察结论草稿，不能声称最终命令已通过。原FEAT-163混合memory块与无关dirty不得混入提交。暂停不启停workflow、不再测试或调用模型，恢复后先读68再继续收口；不得把下一节D5完成表述理解为所有最终治理提交已完成。

## FEAT-164 D5个人本机交付已完成（2026-10-27）

当前权威[67](../features/FEAT-164-kimi-k31-pro-migration/67-d5-entry-and-activation-implementation.md)。Owner明确批准ADR-0022限定个人Mac固定Native身份免登录、完整权限/计划授权/G0—G6保留，随后D5完成。Desktop39b0fbe仅部署helper/receipt/installer/tests/docs；Native/renderer与D4逐字相同，Runtime11fd/r5未改。新App e13a3aa7、receipt f5cf6b8f，119文件1228输入；13激活/7短期回归/19生成及canonical构建通过。

桌面`易界 AI.command`正常入口默认K31可用；`易界 AI（暂停 Kimi）.command`为同源兼容暂停入口，先正常退出再切换。schema2固定原Home/receipt/Owner/D4/预检，不再每日过期；schema1 D3/D4门禁保持。workflow继续existing-ready-only，当前6healthy；日后停机不能擅自隐式迁移/恢复。旧App、原dirty和备份不覆盖。

真实启用→暂停回退→同入口恢复3轮、3次正常退出0，数据/锁/活动WAL0均通过；最终17,397文件/522,400,556字节完整副本。67Native表/Host所有值/Runtime业务行与rollout保持，仅正常日志585及3次metadata probe/停止代际增量。模型0、非模型metadata9，无业务工具。500原dirty、混合memory、7账本/两预占、累计13/45元cap/29.740299保守累计保持。

G4/G5在激活前按限定本机范围通过，G6/D5依据实际观察完成；新local G5/G6必须引用实际Accepted ADR和当前Feature scope标记，不能改成public或借其它需求批准。FEAT-164当前批准的本机交付范围完成，App审计后正常退出，入口仍启用。未来public/cloud/多人/签名发布另行批准；不新增模型验收额度。58安全替代保留，完整App正向never-sent仍NOT RUN；搜索答案/外观专项排除。仅本地提交，不推送。

## FEAT-164 D4阻塞已修复并通过（2026-10-27）

当前权威[66](../features/FEAT-164-kimi-k31-pro-migration/66-d4-blockers-fixed-and-restricted-start-passed.md)。Owner批准65恢复依赖，并要求本轮修复全部D4阻塞。原Docker/四停止态volume备份/canonical recover-up完成、6healthy。首轮App正常退出后定位format5超过reader4及submitted误排队；Contracts d5792d6→Desktop71e39c4只读archive修复，Hosta3d8767/Runtime11fd450-r5未改。新App b8d68436、receipt3437292d，119文件1226输入；88前端/Native真实副本/19生成/Clippy等通过。

第二轮fresh D4已通过8会话11回合/原答案终态/文件差异命令/2附件/删除计划历史与禁重跑，K31暂停、K3退役禁发；正常退出0、锁句柄释放、活动WAL/SHM不存在，历史备份WAL不动。完整后态17,394文件，67Native表及Host所有业务值保持、Runtime业务库不变日志正常追加。两次App各3次Shopify metadata请求，模型0、无业务工具；累计13/45元cap/29.740299保守累计/两预占和7账本保持。

D4 PASS、D5未授权/未执行；下一步以71e39c4候选收口D5长期入口/解除Kimi暂停与workflow责任的具体授权，以及F61-03 local G5/G6，不能把短期D4绑定当长期许可。原dirty及已签名App不覆盖；不重跑D3、不降级SQL41、不用reader4开format5。58接受/Owner排除范围保持，完整App正向never-sent仍NOT RUN。仅本地提交，不推送。

## FEAT-164 D4已获批，启动前停于workflow依赖（2026-10-27）

当前权威[65](../features/FEAT-164-kimi-k31-pro-migration/65-d4-preflight-and-workflow-restart-boundary.md)。Owner批准64后D4受限启动/历史检查/正常退出，Kimi暂停、0模型调用、不进D5。已核六源/119文件1216输入/同回执、D2与D3完整sealed及原17,397文件、SQL41/Host10/四Runtime库/8映射/全模型零派发/同一锁；原数据保持。App启动0、D4绑定未生成，历史UI/退出后态NOT RUN。

workflow失败在all_containers；原Docker Desktop/backend未运行，固定socket不存在，只有privileged网络helper。旧state ready不代表当前ready，容器现场UNKNOWN，未认定exit255或服务故障。未打开Docker、未workflow-up/recover、0模型/商家调用，无Runtime修改。65列明最小依赖恢复：正常开原Docker→只读核原服务身份；若全部停止且匹配，新的recovery计划/四volume完整copy/原依赖和业务审计/正常停止，再同源canonical up（既有幂等迁移、epoch/凭据轮换），ready后继续已批D4。新增范围已询问待答，不复用63旧恢复ID或旧备份，不绕过ready，不进D5。旧dirty/账本/预占保留，仅本地提交。

## FEAT-164 D3一次维护完成，停止于D4之前（2026-10-27）

当前权威[64](../features/FEAT-164-kimi-k31-pro-migration/64-d3-controlled-migration-and-post-state-audit.md)。Owner批准63后一次D3；先核候选841/a3、119文件1216输入、完整D2原17,389文件及同一App锁/无句柄，真实副本SQL37预检全清。canonical维护恰好一次退出0，原日常Native SQL37→41。没有GUI/Host/Runtime/worker启动、没有模型HTTP或Runtime核心/补丁修改，D4明确未授权/执行。

后态17,397文件完整sealed与inspection；SQL41/71表integrity/FK正常，67旧业务表全部旧行一致，迁移记录37原行保留+4，3新表为空。8会话映射、25grant/6消费、7run、6deleted计划及原退款/回执保持；原Host/Runtime/Provider Key与四份WAL逐文件不变。D2 sealed及Native内部备份均核验，未手工checkpoint、删/截WAL或恢复旧库。私有审计feat164-d3-migration-audit-20261027，内部backup01a17ba4-baff-78a0-8e36-6dc3aa81d14c。

一次D3许可已消费，不能重跑或启动D4；下一步独立批准D4后重验后态/实例锁/零派发/workflow ready并保持Kimi暂停。旧SQL37构建不可直接开当前SQL41，回退需另行明确完整数据组与范围，不自动覆盖DB。D5长期入口及local G5/G6未收口；58接受/排除范围保持。旧dirty、混合memory、7账本/两预占保留，累计13次、本轮0，仅本地提交不推送。

## FEAT-164 D3前阻塞已解除，新候选准备完成（2026-10-27）

当前权威[63](../features/FEAT-164-kimi-k31-pro-migration/63-pre-d3-blockers-fixed-and-ready.md)。Owner要求执行解决所有D3前阻塞，Host a3d8767精确旧catalog前身，Desktop实现3219113/来源冻结841f7c7共用结清SQL修复误拦。原已消费次数/授权/旧v1/trust保持，Runtime r5/核心/补丁未改。新daily App4f7adca/receipt0e6fe81（119文件1216源码），canonical prepare-only及同回执通过，目录feat164-d3-ready-candidate-20261027；未创建数据Home或启动App。

6纯值＋Rust副本1＋自然SQL29/37四组合＋Host12子项＋严格静态检查及最终19来源通过。首次Native0项不算PASS；来源两次失败及第三元数据过期作废，RCA后完成提交固定六源再一次串行通过。完整日志保留，不用退出码造绿。

workflow原厂Docker正常启动后发现3个旧255退出；既有recovery efeb4606-28c2-4fef-b327-04c56ad9d7a9先四volume备份，原容器恢复/存储核验/正常停止，再canonical up。六primary现健康且鉴权/editor ready，业务事实不变，两次正常principal审计追加；Docker/workflow保持运行。原失败状态、备份/凭据快照保留，没有强杀/删卷或Infra/API/Coze改源码。

D3_PRECONDITIONS_READY；原17,389日常文件及D2 sealed保持，原Native仍SQL37，无实际D3/D4、无模型HTTP、无D3伪批准绑定。下一步单独明确D3一次维护，先验数据freshness/同一锁/制品；D5长期入口及local G5/G6仍独立。旧dirty、7账本/两份预占、Owner排除/替代保持；仅本地提交不推送。

## FEAT-164 D2已完成：完整备份与三项准入阻塞（2026-10-27）

最新权威[62](../features/FEAT-164-kimi-k31-pro-migration/62-d2-cold-backup-readonly-results-and-blockers.md)。Owner已明确批准61的D1正向组合、D2工具及整个D2。独立Desktop工具提交b54ea001ac5a5530246d30320f024ffb8df94227（9测试/工具/说明文件）；D1组合7、D2 Python4、Go1、lint/docs通过。原b789 daily App/receipt保持，未重建或启动。

D2已执行：同一正常App锁、无项目进程/句柄，完整App树/原Host/Runtime/两provider key冷备份17,389文件476,337,115字节，再复制inspection；原文件/封存保持。真实Native SQL37、Host10、四Runtime库integrity与8条映射/rollout完整。原WAL均非零但完整保留，不手工checkpoint。私有完整数据在feat164-d2-audit-20261027/cold-backup-01，不进Git。

下一阶段NO_GO：B01 6个occupied=1 grant均已terminal/completed且release、无reservation，是历史已消费额度被维护谓词误拦，不能清零；B02旧catalog仅Kimi base_instructions与冻结current不符，匹配原dirty FEAT163指令，不能改原文件或混入整需求；B03 workflow state仍ready但Docker无进程/socket ECONNREFUSED，真实ready未验证，不自动up。下一步先明确这些最小修正/依赖范围，D3—D5仍未授权。长期D5和local G5/G6冲突未改，已接受替代/排除保持。

本轮0模型HTTP、无原库数据库API open/迁移、无服务启动或Runtime修改。原dirty、账本/两份预占保留，仅本地提交不推送。D2调查完成不等于迁移准入通过，不重复已失败workflow探测或改数据造绿。

## FEAT-164 全目标复审与下一步方案（2026-10-27）

当前审计权威[61](../features/FEAT-164-kimi-k31-pro-migration/61-current-implementation-audit-and-completion-plan.md)，D1实际结果仍60。当前Desktop b789d5c、daily App944b6b2/receipt490e35d仅prepare-only；58已接受S1—S4与final、安全替代及完整App正向取消NOT RUN保持，不重跑已排除项。当前矩阵已统一来源，旧59/60按原时点解释。

新增明确未完项：D1真实load_binding私有文件/receipt/Home正向组合证据；D5短时24h/零派发记录尚非长期日常入口；production_hardened+local的G5/G6与validator强制public冲突；D2只读inspection reader及workflow依赖资格尚待准备。当前无已证实新Runtime核心缺陷。推荐先有限离线补证/工具准备及D5/治理具体方案，再批准D2。不能伪造D4记录借helper做D2，不自动workflow-up；Host临时spool正常退出会清理，备份不能承诺恢复临时密文。

本轮只审计/文档，0模型HTTP，无日常数据或凭据/服务访问，不实施代码或D2—D5。G4/G5/G6仍pending，不改exposure造绿、不降Profile、不把受控验证等于正式启用。旧dirty、7账本及两份预占保留，仅本地提交不推送。下一步不是直接维护/启动；长期入口/全局门禁的新范围先具体确认。

## FEAT-164 D1完成：日常部署绑定及只读ready离线合格（2026-10-27）

当前权威[60](../features/FEAT-164-kimi-k31-pro-migration/60-d1-daily-binding-and-offline-qualification.md)。Owner已批准59仅D1，Desktop独立提交b789d5c8147fde9890d49b67c6ecb191473793db，恰好6文件。制品目录不再生成Host/Runtime数据Home，D3/D4/D5执行必须使用原Home部署绑定和exact receipt；daily只核验既有workflow ready，不再workflow-up/状态写入。无Runtime/Native/SQL/Infra修改。

61入口＋3profile、19来源、lint/docs与新canonical prepare-only、prepare-only --reopen均通过。原18个入口测试失败是截取脚本漏fixture初值/旧文案，已仅同文件修正，原日志保留。新daily App119文件SHA944b6b238b7f7b0f36cfab2be358d83b9be044587cc37a3ea5a161fc68b40015；receipt490e35d8e5214d1dddd84def050edf093cdd9f2f7aa9edd5fb83076ebb3c9fc3，目录feat164-d1-candidate-20261027。prepare-only未读绑定/真实凭据，未创建数据Home、未启动App/workflow。

D1 PASS_OFFLINE、CUTOVER-01/03离线修复；D2—D5仍未授权，实际日常状态/首次启动未知，G4不从prepare-only自动晋升。58原accepted local/final与never-sent安全替代保留，完整App正向取消仍NOT RUN；搜索质量及外观专项OWNER_EXCLUDED。下一步必须先获D2完整冷备份/第二副本只读预检授权，不直接维护或启动，不重跑模型回合。

本轮0真实/0本机模型HTTP，无日常库访问。旧500dirty＋混合memory、7账本/快照、360旧App/receipt保持；累计真实13、45元cap/29.740299保守累计、两份14.188544预占保留。仅本地提交、不推送，Runtime核心/补丁仍先方案。

## FEAT-164 S4AF：日常切换方案已收敛，执行尚未授权（2026-10-27）

当前权威[59](../features/FEAT-164-kimi-k31-pro-migration/59-daily-cutover-minimal-plan-and-authorization.md)。本轮仅源码/58证据/制品审计和方案落盘，不访问、枚举、hash、备份、预检、迁移或启动日常数据/App；0真实/本机模型HTTP，无Runtime核心/补丁或产品修改。

新发现CUTOVER-01 P1：daily K31 launcher把Host/Runtime Home改为候选.local/feat164-daily，而Native仍读com.yijie.ai/demo-fast-v1；Native仅isolated分支重写Home。不能直接启动当前c29f7e0日常候选。维护命令合并backup/preflight/写迁移，其内部5文件不是完整多存储备份。正常launcher的workflow-up在停止态会迁Coze/API；workflow-status也写state且false ready不保证非零exit。K31暂停不阻止MiniMax自动计划，首次App启动还有Host/Runtime写迁移。

当前G4重新pending、implementation active、日常NO_GO；58本地S1—S4/final及Owner never-sent替代保持历史已接受范围，完整App正向取消仍NOT RUN，不反复补试。搜索质量和外观专项OWNER_EXCLUDED。日常现场schema/Home/占用/计划/workflow状态未知，不拿原R1隔离库事实代入。

推荐下一步仅D1：批准Desktop launcher/receipt两文件＋新增daily-deployment.py、既有入口测试及两文档的部署绑定/既有workflow只读ready修正，合成验证和新prepare-only。不改Native command/schema、Infra或Runtime。D1当前只是方案，未批准实施。其后独立D2完整冷备份/副本只读预检→D3一次Native维护→D4首次受限启动/正常退出→D5确认日常启用；真实模型请求全部仍0，后续数据动作不从方案确认自动继承。

原500dirty＋混合memory、7账本/快照保持。累计真实13、45元cap、29.740299保守累计和两份14.188544预占不变。本轮只本地治理提交、不推送；不复位unknown/grant、不覆盖旧或已签名App、不降库/删WAL/强杀。

## FEAT-164 S4AE：Owner接受安全替代，本地代码与验收收口（2026-10-27）

当前权威[58](../features/FEAT-164-kimi-k31-pro-migration/58-owner-accepted-substitute-and-final-closure.md)。Owner明确接受57号never-sent正常Native持久取消/重开及生产消费链的安全分层替代；完整App正向取消原执行仍NOT RUN，不再安排该项补试。原unknown缺Host回执，保留未决/禁发/明确恢复安全拒绝为正确结果，不重复点击、不清空或换operation。

587个历史证据引用、12私有事实、六干净来源及三套119文件App只读核验一致。S1—S4 G3、TCONF04、三项适用final与G4通过；旧来源/时间及raw失败保持，非新一次全范围E2E。Desktop ea/Host4f/Contractsc5/Runtime11fd-r5/Connectorscc56/Skills595不变；测试4e1仅3测试/说明文件。本轮产品/Runtime/patch零修改，0真实/0本机模型HTTP。

累计真实13、45元cap、29.740299保守累计和两份14.188544预占全部保留。12441保护文件、500既有dirty和7账本核验；混合memory仅此段。无项目服务/交接待答，仅本地治理提交、不推送。搜索质量与亮暗/键盘/最小窗口仍OWNER_EXCLUDED。

feature保持active、implementation为accepted local code complete；日常候选只prepare-only，日常库未打开/迁移，G5/G6及发布pending。下一步若需日常切换，先明确目标identity、完整备份/正常停止/只读预检/显式维护/启动和回退范围并获授权；当前禁止执行。新Runtime核心/补丁仍先方案确认。不能把局部替代接受写成完整App执行或整体已部署。

## FEAT-164 S4AD：自然unknown安全拒绝与保留取消正例（2026-10-27）

最新[57](../features/FEAT-164-kimi-k31-pro-migration/57-natural-unknown-and-safe-delivery-verification.md)。当前ea/Host4f/Runtime11fd-r5新原R1 identity App4b0ec55/119文件，正常构建重开/退出。自然f38666dc是Native有v2 unknown、Host无回执，源于35号旧Host purposeOrdinary拒绝（缺陷已修），不能当缺Native意图或never-sent；实际App读历史禁发/一次明确恢复拒绝/重读保持通过。不要再次恢复同一缺回执操作、换ID或清空。另一queued是旧input-only草案，无普通delivery proof；刷新不重发。

测试工作树feat164-s4ad-tests-20261027/Desktop4e1f1f980d148a6b46e21e68eb508caa4da5dae4仅3测试/说明文件。正常Native入队→claim未发送→cancel→重开同回执1PASS/0ignored，实际输出消费到生产parser/composable/control1PASS；完整DB保留。fmt/strict Clippy/lint/build/docs通过，产品/Core/Patch零改。完整App never-sent正向仍NOT RUN，下一步审阅安全分层替代证据的明确接受边界，不造故障/改库获得样本；自然unknown安全拒绝已观察，不再笼统列未验。

0真实/0本机HTTP，累计13、45元cap、29.740299及两份14.188544预占/7账本保持。原库69表旧行保持，计划2表仅正常paused时间槽/next/cursor变化，旧正文/授权/grant/run/意图不变；Host14条仅updated_at，四库自然WAL0。6790活动数据外文件/500原dirty保护；raw全行不等与字段复核均保留。全部服务停止，无交接待答。56日常prepare-only候选仍未启动/迁移。搜索答案质量/外观专项已排除，Runtime核心/补丁先方案，仅本地无推送。

## FEAT-164 S4AC：当前证据与日常prepare-only（2026-10-27）

最新[56](../features/FEAT-164-kimi-k31-pro-migration/56-current-evidence-business-state-and-daily-prepare.md)。产品/Core/Patch零改；当前Desktop ea8763d/Host4f966e8/Contractsc5d1383/Runtime11fd-r5/Connectorscc56/Skills595。501旧证据hash和310业务文件绑定，22前端＋38Host＋33Native＋5计划＋3日常入口＋19来源通过。实际S4AA c98 App产品与ea相同：重开菜单、旧迁移/中断/继续历史、关闭计划、真实图片/工具、18来源partial通过，未发送/授权；0真实/0本机HTTP。正常退出，71表旧行/四库WAL0，全部服务停止。

新日常候选feat164-s4ac-daily-candidate-20261027：canonical prepare-only和只读receipt通过，119文件/App c29f7e07942038d4c3849ef3a711ed4b501d17daab1478329ba5de6b6321a4d0；未启动、不打开/迁移日常库。旧候选不覆盖，6673保护文件/500原dirty/7账本保持。真实累计13、cap45、29.740299估算及两份14.188544预占不动。

S4绑定已补，完整S4/TCONF04/core和业务状态final仍NOT RUN具体unknown/never-sent完整App链；安全组件/Native通过不冒称App自然观察。teardown PASS。下一步优先复审原隔离库自然unknown的当前兼容只读入口，不清空/制造never-sent；日常切换需具体数据动作授权。搜索答案正确性和外观专项继续OWNER_EXCLUDED，禁止再安排；不新增真实模型调用，Runtime核心/补丁先方案。审计reader误用副本文件名已纠正，只有记录脚本小错误，无产品失败/开放熔断。仅本地无推送，无交接待答。

## FEAT-164 S4AB：v3测试已修复，搜索答案质量已由Owner移出（2026-10-27）

最新[55](../features/FEAT-164-kimi-k31-pro-migration/55-v3-test-and-search-grounding-root-cause.md)。Owner最终明确“搜索答案尚未通过”不作为FEAT164需求、从需求移除：搜索答案正确性/本轮官方页面命中与能否确认的质量判定记OWNER_EXCLUDED，不延期、不计PASS、不再补试/增加检索工具/为此改Runtime。原模型身份、sources传递、协议事实、Key/审批/预算、历史/清理保留。不要再把该质量问题列为S4/final阻塞或拿旧待办继续真实搜索。

Desktop ea8763dfc40466e9b808a1b39afad71dbff1ac56在feat164-s4ab-qualification-20261027，只修1测试文件：typed v4 IPC正例、拒绝v3/v5、unsupported持久示例5，实际v3/v4由Rust reader独立通过。28前端+2client（23未选）+1Native/19来源/lint通过；产品/生成/依赖未改，statusSource可选不是旧失败原因。实际App仍S4AA c98eddf/Host4f966e8/Runtime11fd-r5，SHA179dbd187220694d4666af5822466572f3b245a911501991cb0194f4308db195/119文件不动。

本轮授权45元，Owner先1→2→3次，实际3/3已用、累计13；前两仅搜索工具声明、无搜索/最终文本，第三恢复原工具声明有无法确认答复、仍无搜索。三次HTTP200/completed不作质量PASS。官方完整Responses定义证实自动服务端检索、tool_choice仅auto、external_web_access被忽略；内部未触发原因未知，不归咎Runtime字段丢失。三轮结果和原始失败保留。

计量工具d4050044d2c6a77ab3ba00907b650126dc5db0f8/schema6，第三工具92ef0411a6e98f36886f2b7a2017e40fe2d21340/schema7，45/49离线项通过。新search及search-third独立账本，旧四账本逐字保持、前12行完整继承，旧第1/10笔14.188544各自预占不释放。最新估算加预占29.740299元，非精确账单；schema7 halted/stopped_normally，授权次数用完，不以余款再调用质量任务。3次App正常⌘Q exit0，四库各WAL0/integrity，71表旧行保持；最新一轮后额外UI重开未执行，不假称PASS。App/meter已停止，无待答交接。

497原dirty、6498活动库外保护文件、旧App119文件保持；FEAT163混合memory独立未提交。原工具新增__pycache__为本轮导入缓存，保留未提交，tracked源码未改。审计目录feat164-s4ab-audit-20261027。下一步只收口仍在范围的来源/核心业务状态与日常prepare-only/具体切换清单；日常数据操作及新Runtime core/patch仍须对应授权。仅本地提交、不推送，不恢复已移除外观/键盘/最小窗口或搜索答案质量。

## FEAT-164 S4AA：来源误删修复与离线验收完成（2026-10-27）

最新[54](../features/FEAT-164-kimi-k31-pro-migration/54-search-source-component-fix-and-offline-verification.md)，前序真实结果见[53](../features/FEAT-164-kimi-k31-pro-migration/53-real-functional-results-and-search-source-fix-plan.md)。Owner已批准53最小安全范围；Contracts c5d138374c102f1a8a11e328a869ec8f91724efd→Host 4f966e8ea810d5b094d0b797d291955d6c774844→Desktop c98eddfafb789520b4939bdca95bf8b27f28b7b6在feat164-s4aa-qualification-20261027，仅本地提交。只把来源URL opaque检测限定URI组件，先分原始结构再解码；全局脱敏、其它拒绝规则、Runtime/core/patch/schema不改。

7顶层Host/25URL样例、5契约、6入口、19来源及native-process不可变检查通过；renderer20通过。额外FEAT132旧样例v3接受/v4拒绝与当前权威不符，基线未变；保留27/28结果，未扩范围改旧测试或放宽validator。新canonical App SHA179dbd187220694d4666af5822466572f3b245a911501991cb0194f4308db195，119文件，20Runtime→18Host/SQL/UI、2保守隐藏/partial；任务01a17910-bf4e-7142-af4a-04791d73cae1 completed。同构建重开0补发，两次正常⌘Q exit0，四库WAL0/integrity，71表旧行全保留。fixture正常shutdown204/exit0，无活动App/meter/待答交接。修复期1本机/0真实；审计目录feat164-s4aa-audit-20261027。

此前S4Z已用4真实HTTP、累计10：图片1正确/函数及回灌2通过/搜索1传输completed20sources但内容正确性INCONCLUSIVE；真实App同构建重开0请求，已正常停止。不要再按52/handoff旧余4次续发。四账本相对S4AA开始逐字不变；旧14.188544预占和新search同额预占保持，29.343192是保守估算，非精确账单。当前修复授权0新增真实，不因泛模型授权重发搜索。497dirty及6498保护文件保持，FEAT163不混入提交。

整项目标仍活动K3全面换K31、保留原历史/授权/MiniMax；S1—S3绑定原有效证据，S4及完整final未完成。下一步收口S4/最终业务状态，最小修正旧v3测试样例并在新Host上做日常候选prepare-only资格，再具体审阅真实日常切换清单。日常库打开/迁移/激活仍未授权，不改旧daily包；新增Runtime core/patch仍先确认方案。外观/键盘/最小窗口已永久移除，不能恢复。所有旧来源失败/备份/账本保留，不强杀/删WAL/手工checkpoint。

## FEAT-164 S4Y：隔离App复验通过子集，等待窗口交接（2026-10-27）

最新[52](../features/FEAT-164-kimi-k31-pro-migration/52-isolated-app-functional-qualification-and-handoff.md)，续办先读feat164-s4y-audit-20261026/handoff.json。Desktop 54e961842cb7abe7234e3d643142e99f266ec833在ec1ab63上只将已有cfg(test)模块移到末尾，生产文字和断言逐字一致；Clippy lib/bins/tests -D warnings/原reader测试/19source/canonical均通过。App SHA879568b9ff61530806d63aaa6068053e98f1d68b1fc6506a48adecc4035c6b8a，119文件；日常ec1候选保持未激活。

新隔离App图片＋HTML/SVG工具回灌/预览、MiniMax两任务completed，4次本机HTTP、真实0；首次正常⌘Q exit0、71表旧行保持、四库WAL0/integrity。第二次同构建已重开，但用户在模型菜单操作，异步窗口交接问题待回复；不要继续抢操作或把历史详情未检写成PASS。App session70340有意留开，Host/Runtime受管；不是全部停止。fixture及真实meter都已正常停止。

工具a35e619e297c793ebb6cfb08730ab558f2924356单独checkout feat164-s4y-tools-20261026/Desktop，38独立测试/docs通过；schema5保留图片/搜索/函数回灌，原schema1-4不改。g2v-real-budget-ledger-functional.json绑定旧r5完整前6行、当前App/r5及30元，0/4新增，stopped_normally未耗槽。4次是本轮自行收紧的执行上限，来源仍Owner必要功能调用/搜索图片授权，不需再索预算。原三账本/14.188544预占逐字保持。搜索一旦发生完整新预占保留并停止，不伪精确账单。

用户交回窗口后先核对当前同一App和ledger6行，启动同一meter及控制文件（路径在handoff，不打印内容），先核验旧合成任务重开，再按图片1/函数回灌约2/搜索最后的序列至多4HTTP、失败即停。不要重建/补额、移除搜索、重复42或恢复外观专项。真实日常库仍不允许打开/迁移，Runtime core/patch仍先方案。整项S4/final未完成，仅本地提交无推送。6554保护文件/497原dirty及混合memory保持，缺依赖环境修正和初次失败保留。

## FEAT-164 S4X：日常候选离线准备完成（2026-10-26）

最新[51](../features/FEAT-164-kimi-k31-pro-migration/51-daily-candidate-implementation-and-offline-verification.md)。Owner批准50的8实现文件及测试文档、明确“不迁移日常库”。新目录feat164-s4x-daily-candidate-20261026/Desktop ec1ab631d76d2f6ba2c74e25eaac1ea60339dfb4共12文件；显式daily prepare-only/维护、精确compiled identity与flags、完整workflow/market/expert/media、独立回执实现。原主树fd0c575/100dirty未覆盖，Runtime/core/patch零改。

SQL29/37隔离与daily四组合、S2 32/S3 5、Node8/identity2/feature-off1、19来源、产品Clippy、lint/docs及canonical日常prepare-only通过；119文件App edf9a13820819aaeb260d216cddeb7e5291214be7cc17b76c6f67764a5f227d4，同源receipt c4401b7ebf04f997bdd4a704dca3070a5c1d14d5b94616704aeb96a270f4d657。SQL37配置和缺旧checkout的失败/RCA保留；扩展全测试Clippy仍FAIL_BASELINE native_conversation_storage.rs items_after_test_module，不假称全量CI通过。

新App未启动，真实日常库未连接/解密/迁移，模型0；11953原文件/498原dirty核对保持、六来源干净、无活动项目服务。旧三账本/14.188544预占/30元保持。S1-S3/G2V/teardown仍绑定旧9f隔离App42a23cf，不自动继承daily候选；本轮OFFLINE_PREPARED_NOT_ACTIVATED，完整S4/final未完。下一步优先以新源码固定隔离identity补适用业务资格，再具体呈报真实日常备份/只读预检/维护授权；禁止直接启动daily App试错、放宽occupied guard或回写旧库。外观三专项仍移除，必要模型功能授权不需重复索批，但本阶段仅离线。仅本地提交，不推送。

## FEAT-164 S4W：S1—S3收口、日常候选实现已批准（2026-10-26）

最新[50](../features/FEAT-164-kimi-k31-pro-migration/50-slice-evidence-closure-and-daily-deployment-plan.md)。76项定向检查通过（S1 11/S2 60/S3 5），当前同源暂停App Kimi禁用、MiniMax可选、历史42可读，0模型尝试；正常退出/71表旧行/4库WAL0。S2真实Native→Host→r5边界1次MiniMax合成，正常重启/取消零POST，完整home保留。Host f97d2216001e78df02e93c972a6aec2e1d772f58仅一个测试保留逻辑，299非测试产品文件仍等于8cd，App/Runtime不改。317项旧证据hash核对通过。

S1/S2/S3 G3实际PASS；S4仍缺完整TCONF04/供应商非文本/完整unknown GUI，不能把每个UI未决形态写成已观察。代表性旧App迁移/取消/计划纵向来源46已与当前源码逐字绑定；不是新binary重跑迁移或一次fresh全部场景。49真实r5资格与正常teardown保持；真实HTTP新增0、旧三账本/预占保持，必要功能调用授权不撤销。

日常集成18文件只读预检发现runtime-chat-models.candidate.json来源锁与原dirty9154冲突，仅metadata base_commit；不手改生成物或覆盖原工作区。Owner已明确“批准实现及离线验证，不迁移日常库”，批准50列明8个Desktop实现文件及测试文档在新隔离目录实施，无Runtime核心/补丁修改。日常实际开库/迁移/启动仍需后续具体产物/备份/预检批准。外观三专项仍移除。

## FEAT-164 S4V：r5真实资格通过与日常切换边界（2026-10-26）

最新[49](../features/FEAT-164-kimi-k31-pro-migration/49-r5-real-qualification-and-daily-cutover-boundary.md)。Owner明确“需要调用就直接调用，无需精确计算”，必要真实功能验证已授权，不再以精确查价或旧5次耗尽重复询问。先最小1次：实际K3.1/max HTTP200答42/完成，保存、同构建重开0补发，两次正常退出；4Runtime库WAL0/integrity、71表旧行全部保持。App仍9f media42a23cf，Host8cd/Runtime11fd-r5不变。

工具92cbe3d78fef499f9f1904727b1a5a48be632218仅4计量/oracle文件，34Python＋10分类控制通过；独立r5账本保留原5行/两旧账本和14.188544预占。累计6次，历史估算14.795856元，不是当前精确价格；30元约束保持。schema4单slot用完正常停止；不把停止误读为Owner撤销后续必要功能验证授权。首次SQL观察读错旧chat_messages占位，改读原生agentMessage/views后只读通过，无产品改动或补发。

G2V改绑r5真实结果，旧r4/S1 PASS不自动继承；teardown正常适用范围PASS，完整core/业务状态仍按49具体缺项。日常库未开放/迁移，不能用环境开关绕过两个隔离identity、predecessor或workflow边界；下步先日常部署兼容具体diff/评审，再明确日常备份和受控维护授权。新Runtime核心/补丁仍先确认。亮暗/键盘/最小窗口已移除，禁止重新安排。原497dirty及71457保护文件保持，项目服务全部正常停止，仅本地提交不推送。

## FEAT-164 S4U：保留状态验证完成，Owner移除外观专项（2026-10-26）

最新[48](../features/FEAT-164-kimi-k31-pro-migration/48-retained-runtime-qualification-and-scope-update.md)。Host测试提交7bf43fe0b18188e71442611b781ed87811911cde仅3测试cleanup/目录放置＋新保留入口/说明，其余492tracked保持，产品pin仍8cd6bcc，Desktop9f5814f/Runtime11fd-r5及原App不改。12Runtime检查/38loopback、10完整home/40库WAL0/integrity ok，另4来源＋10Host领域＋22前端业务状态＋5配置通过；真实0。数据在feat164-s4u-audit-20261026/retained-run-1，禁止清除。不要再重复同组38请求或改Runtime核心来消除已关闭缺口。

Owner明确从FEAT164移除App亮暗、键盘/焦点和最小窗口专项验收，非延期、非PASS、不得再作门槛。收到指令时仅只读看到原浅色，未切外观/未验键盘窗口；候选正常⌘Q exit0、fixture正常停、0请求，SQL旧71表行保留/仅正常停止行新增，四库WAL0。业务模型状态/恢复/取消仍属功能要求；feature保留治理槽并明确排除项，不伪造ui_change=none。

整项IN_PROGRESS；下一步收敛剩余时序/源绑定及适用final，r5真实G2V与日常cutover无授权，不新增付费调用。5/5、30元cap、14.679001含14.188544预占及旧账本保持。全部项目服务已停止，仅本地提交不推送；旧工作区保留，主Host未快进。

## FEAT-164 S4T：当前media App限定验收完成（2026-10-26）

最新[47](../features/FEAT-164-kimi-k31-pro-migration/47-current-media-app-and-retained-state-qualification.md)。S4S治理e137722本地固化；本轮产品/Runtime/补丁零修改，Desktop9f5814f/Host8cd/Contracts ca06/Runtime11fd-r5/Connectors cc56/Skills595保持，独立s4t-media canonical App42a23cf…、119文件及同构建回执通过。

实际App专家可视化资源正常安装/绑定、HTML与SVG发布预览、PNG输入、MiniMax共存和正常重开通过；3任务5loopback，真实0。两次⌘Q exit0，进程/端口/句柄释放，四Runtime库WAL0/integrity ok；重开0补发。71表全部旧行及原计划/grant保持。资格skills日志正常追加1安装，旧7条重建字节匹配原SHA；其余42097保护文件和494非自有dirty保持，混合memory原内容匹配；严格保护首次FAIL单列RCA，不假称日志全字节不变。

旧5/5、30元cap、14.679001含14.188544预占及日常库/原SQL41候选保持。全部服务正常停止，无待答UI。整项IN_PROGRESS、三个final NOT RUN。下一步优先审并实现仅测试生命周期的Runtime home保留入口，再复验当前r5辅助/子代理/压缩和完整TCONF；现有成功RemoveAll runner本轮未跑。若需Runtime核心/patch先报最小方案；无新真实调用/日常切换/推送。私有证据在feat164-s4t-audit-20261026，不重复已通过S2/S3和本轮任务。

## FEAT-164 S4S结果已收口，S4T恢复执行（2026-10-26）

Owner18:01暂停后明确恢复。先读[46](../features/FEAT-164-kimi-k31-pro-migration/46-independent-legacy-app-qualification.md)及当前验收矩阵；原paused-handoff保留历史含义。最终Desktop9f5814f在s4s-candidate工作树，旧producer54921df在s4s-qualification；Contracts ca06d09/Host8cd6bcc仅旧来源元数据，Runtime11fd/r5及Host产品binary不变。主仓未快进，原dirty保留。

自然旧App→compiled29/41维护→最终App原thread切换/继续/正常停止/继续、旧计划审阅新模型保存paused/新单次grant/完成及同构建重开取得限定证据。5次loopback（旧K3一、新K31四），真实0；两次最终正常退出四库WAL0/integrity ok。新一轮恢复审计新增模型0。原unknown/消耗grant与5/5、30元cap、14.679001含14.188544预占保持。

恢复已核验497原dirty（排除本任务记忆插入）、8482保护文件、六干净来源和42bundle文件。46/08/feature.yaml/索引收口按实际验证记载；不能把源绑定迁移说成最终binary fresh29迁移或完整final通过。当前继续S4/TCONF04与三个final，未决/never-sent App缺项仍列出；日常迁移/新真实调用关闭，Runtime核心/patch先报方案。保留全部失败日志、旧构建与暂停记录，不重复已通过S2/S3模型回合。


## FEAT-164 S4R：受控旧隔离库入口已实现（2026-10-26）

最新权威[45](../features/FEAT-164-kimi-k31-pro-migration/45-controlled-isolated-migration-entry.md)。增量semantic，仅Desktop私有维护入口：同一canonical App明确参数、既有单实例锁、固定FEAT164 identity/根、lsof无句柄、正常静止和原始加密快照，再调用既有migration到38及正常Repository open到41/退役，随后退出；auth/worker/Host/Runtime/UI均不启动。普通旧库guard、日常拒绝、原权限/授权保持。只准入自然资格已完成的SQL29/37，不接受任意数据路径，不清理unknown/占用、不退款、不重发、不手工checkpoint/WAL操作。

当前实现保留在feat164-s4r-qualification-20261026/yijie-desktop：8dcf7a678f02c9bfa74dbf8cea4dff4e7bd2ae00 + bc3b097edf56779a1cfd273063df6d8f4a9c6019。主工作区三处源码已有其它需求dirty，因此未快进/应用补丁，主Desktop HEAD仍fd0c575；后续必须读取隔离候选而非误称主库已有新入口。Runtime11fd/r5、Contracts5b5dad、Host产品894671b和旧S4P App不变。

SQL29/37自然API产生样本：held拒绝原字节保持，review实际29/37→41、原备份一致、旧ledger及9事实表/3模型身份行保持、重复/正常重开通过；feature-off、路径/日常identity、正常锁争用拒绝通过。fmt、产品lib/bins Clippy、docs及最终19来源通过，ordinary canonical构建42文件/同源回执通过。不是完整App/G3/final。

实际compiled禁用/daily配置早期拒绝；无模型Key的canonical维护入口正常抵达原SQL41库，因1条非ready模型选择拒绝（另有2份occupied grant；pending outbox=0）。5522原文件保持，新增私有快照/停止记录8文件，UUID01a17722-6db5-7173-9409-6d053287c982。该库无需再次结构迁移，不为了通过门禁清空记录。首次依赖配置/普通prepare Key预检失败及后置归因误假设均保留；只修新维护模式Key预检，无自动真实重试。

真实模型与loopback模型新增均0；5/5、30元cap、14.679001保守累计和14.188544预占保持。497原dirty与旧证据/制品/日常数据保护，仅本地无推送；原始日志/新构建回执/私有副本在feat164-s4r-audit-20261026。无活动服务或待答。下一步沿原请求只读厘清1个选择/2份占用，再安排独立旧数据的同源App S2/S3纵向；不擅自扩大日常迁移、核心/patch或付费调用。

## FEAT-164 S4Q：自然旧K3与计划离线资格（2026-10-26）

最新权威[44](../features/FEAT-164-kimi-k31-pro-migration/44-natural-legacy-migration-and-plan-qualification.md)。S2真实旧Runtime正常生成历史，当前r5 loaded旧身份经实际Host SwitchThread迁移，同thread K3.1/max、普通流式interrupt、正常重启/恢复通过；首次fixture等待断连超过其正常Shutdown期限FAIL保留，有限响应修正后PASS。两次共8 loopback，真实0；四库WAL0/只读完整性ok，原历史上下文保持。

S3默认API自然产生两份SQL29计划/授权/占用。首次candidate正常open被既有SQL<38 guard拒绝、原文件保持；这是22号保留的产品准入门禁，不能再把缺项只归为App无旧记录。没有移除guard。独立test通过既有migration函数显式29→38后，candidate open38→41、退役、显式新模型保存paused、新grant、never-sent取消和重开通过；5阶段0skip/0模型，原29条migration ledger、旧grant/run/outbox等保留，旧occupied=1不退款。领域PASS不等于App旧库准入/完整S2/S3通过。

仅测试提交Host d49c005f8e533e1251179bb2319f6e3e2ec2db08、Desktop fd0c575e4465dea6bb72ec9681248f664000551b；产品来源仍894671b/b6f0ad7，Runtime11fd/r5和Contracts5b5dad不变，S4P原App119文件保持，无需改核心/patch。Go race/vet、Rust fmt、产品lib Clippy通过；strict test Clippy仍被既有native_conversation_storage.rs:46排布错误阻断，未压制warning。所有失败与后续修正分别留存。

本轮未开App、未修改候选或日常数据；497原dirty、旧账本/14.188544预占保持，5/5、30元cap和14.679001保守累计不变，仅本地无推送。下一步优先具体审定旧隔离库的显式准入/正常静止/兼容reader/回退边界，再补同源App的旧线程与旧计划纵向；不可把测试expand接到所有启动或删除白名单。S4/TCONF04/全部final/日常切换未完成，Runtime新范围仍先报确认。证据与保留数据在feat164-s4q-audit-20261026；无活动服务/模型调用/用户待答。

## FEAT-164 S4P：App未就绪已定位并最小修复（2026-10-26）

最新权威[43](../features/FEAT-164-kimi-k31-pro-migration/43-app-readiness-root-cause-and-minimal-fix.md)。S4O无凭据media环境自动进入provider-only，Native剥离模型/计划配置，实际App候选Host schema11/base10缺v2 reader资格而正常拒绝；不能依据空资格host-home推断Host未启动（Native会改指App数据目录）。只读IPC健康ok/auth signed_in、前端context阶段chat_host_not_ready、实际副本ErrModelUnavailable已证明；不是继续修改Runtime的理由。

已复审后仅Desktop launcher加5行拒绝错误候选启动，prepare-only仍可无凭据构建，提交b6f0ad7c5181e7ea488c019a1eccd76396eab16e。Runtime11fd/r5 SHA283d12e…、Host894671b binary1d880cb…及其实现不变；Contracts5b5dad、Connectorscc56cda、Skills595c927保持。新独立构建在feat164-s4p-qualification-20261026。19generation、无效启动预检与canonical media构建通过；首个generation缺嵌套工具依赖已修配置并保留失败日志。

现有本机fixture正确装配后，两次实际App ready、原42/50/8历史和关闭计划可读，旧不确定草案保持禁发/勿重发。两次⌘Q exit0，App/Host/Runtime/worker/adapter、监听/句柄释放；四库自然WAL0、完整副本integrity ok。真实/本机模型HTTP均0，fixture已正常停，无活动进程或待答。SQL71表70相同，仅加2正常停止行，全部旧行保持；Host115键全保留，14 updated_at正常resume更新，其它字段/操作不变，原bytewise FAIL不改写，字段审计单列。

原工作区497dirty、旧证据/制品/日常数据保护；候选完整before/after留存，DB正常元数据与WAL处理如实记录不冒称全文件不变。两旧账本、5/5、保守14.679001元含14.188544元unknown预占、30元上限保持。没有新增Runtime/patch修改、日常迁移、push/tag/release。整项IN_PROGRESS，后续推进当前r5的自然旧K3已加载线程迁移/恢复取消、旧计划重新审阅授权、S4/TCONF04/core/全部final；r5真实G2V未授权未执行，不继承r4 PASS。不要重复已收口的错误启动配置或旧141项替代剩余场景。

## FEAT-164 S4O：六文件r5实现与限定关闭资格（2026-10-26）

Owner已在必要性复审后批准41号；新增范围是两个既有文件，非新Runtime产品模块。已按六文件0011补丁实现，canonical上游codex-rs逐字未改。Runtime11fd450→Contracts5b5dad9→Host894671b/Connectorscc56cda→Desktopc76558e，Skills595c927保持；本地提交无推送。当前权威[42](../features/FEAT-164-kimi-k31-pro-migration/42-r5-shutdown-implementation-and-qualification.md)。

r5 SHA283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e；9关闭/listener/log+6RPC、Clippy、源验证通过；一次保留home的零turn loaded-thread/start/read/EOF正常exit0，四库WAL字节0，完整副本只读integrity均ok。无手工checkpoint/WAL清理/强杀。完整make test仍阻在既有100644 build-input-only.sh执行位，不修改旧权限。269schema与r4相等；19generation第三次PASS，两个前序来源配置错误已分析并保留；4组合来源、media App canonical构建及只读同构建回执PASS。

实际App本轮未锁屏：无凭据canonical启动后本地服务未就绪，任务记录不可用，根因UNKNOWN；不能因窗口打开/编译通过判App可用。无重试/消息；CUA正常⌘Q、exit0，5528候选文件保持，未证明Host/Runtime激活。下一步零模型先审Native启动配置/装配及标准本机fixture，再补r5 Host/App纵向；不因未就绪直接扩Runtime。没有活动App/检查/待答交接。

原497dirty及7643保护文件保持；Connectors混合source.lock仅新增本次wrapper，旧未提交sourceCommit仍完整保留且未混入提交。两旧账本、5/5、保守14.679001元含14.188544元unknown预占、30元cap不变；真实新增0。r4 G2V/视觉按原来源保留不继承r5。S2/S3自然旧K3、S4/TCONF04、完整core/teardown及日常cutover仍缺。当前App/Runtime/worker新输出保留在feat164-s4o-qualification-20261026及Runtime独立r5；原始失败/成功日志在feat164-s4o-audit-20261026，不能重建覆盖。

## FEAT-164 S4N深入复审待扩范围（2026-10-26）

Owner已明确批准40号四文件Runtime最小修复、独立r5、必要Contract First下游和零真实模型验证。后又要求深入分析失败、再次审计方案后执行。当前权威[41](../features/FEAT-164-kimi-k31-pro-migration/41-shutdown-plan-deep-review.md)：三次Clippy失败已熔断/RCA，一次fresh重资格6新unit＋6RPC及Clippy通过；但新审计发现listener直接spawn无join/跟踪，clear仅发cancel，及前置RPC无限等待的顺序风险。不能因此构建或晋升四文件候选。

推荐六文件范围：原app-server/lib、message_processor、thread_processor、state/log_db加app-server/thread_state和request_processors/thread_lifecycle。仅新增listener每实例注册/任务跟踪与正常等待；保留in-process共享所有权。**新增两文件未批准，尚未修改**；需要明确范围确认，不继承泛授权静默扩张。Runtime现有Makefile/0011/r5脚本为本轮未提交候选，临时源码在feat164-s4n-audit-20261026/runtime-source；四文件patch快照已保留。r5未构建，Contracts/Host/Desktop未改，旧r4及当前App保持，真实新增0。新r5 EOF验证必须保留完整home，不能用自动删TemporaryDirectory的历史smoke。

6+6静态资格不是真实loaded listener/checkpoint/完整teardown PASS。S2/S3/S4/core/日常cutover缺项及两份账本、5/5、14.679001元保守账与14.188544元预占不变。无运行中的检查/Runtime或UI交接。收到新增范围批准后先完成41号安全单元及fresh源码资格，再独立r5/原生零turn loaded-thread EOF，失败即停；不得机械重跑/强杀/清WAL。

## FEAT-164 S4M正常关闭审计与待确认方案（2026-10-26）

最新权威[40](../features/FEAT-164-kimi-k31-pro-migration/40-runtime-shutdown-audit-and-minimal-plan.md)。Owner授权先审计，核心/补丁必须先确认。本轮未修改产品、Runtime、补丁或binary；19固定源码/10现有patch/6依赖核对，独立空home一次initialize/initialized/正常EOF，真实模型0。退出exit0、非强制；state/goals/memories留有nBackfill0 WAL，logs此次无WAL；四库完整副本mode=ro integrity_check均ok，原候选/日常库/旧账本逐字保持。

候选根因是stdio进程未调用StateRuntime.close，日志inserter无显式shutdown/join且全局sender保留；线程排空超时亦不能视为写入者退出。推荐仅独占stdio所有者等待生产者、关闭日志准入并排空/join、await已有四池close；不主动checkpoint、不删/截断WAL、不改schema。具体四文件面、独立r5及必要Contract First下游更新见40，**待Owner明确批准，尚未实施**。若需更广core/shared/in-process改动停止另报。

r4与当前S1/G2V/视觉子集历史结论保持；S2/S3自然旧K3纵向、S4/TCONF04/core与teardown仍未完成。r5若获准会使相关r4证据过期，不自动继承真实G2V；5/5请求额度耗尽，保守14.679001元含unknown预占14.188544元不变。无活跃审计Runtime，无UI操作/待答交接；锁屏项目可跳过，日常切换和推送未授权。不要反复跑原141项代替新假设验证。

## FEAT-164 S4L证据收口，真实次数耗尽，checkpoint仍待核实（2026-10-26）

最新权威[39](../features/FEAT-164-kimi-k31-pro-migration/39-evidence-binding-and-final-verdicts.md)、feature.yaml及s4l证据。Owner确认38并授权零真实模型收口S1—S4/三个final，锁屏可跳过；此次桌面可用未跳过。保持EA9 Desktop、090c2db Host、1b357cc Contracts、a28130a r4、7ea3df4 Connectors、595c927 Skills，同一canonical bundle，无产品/Runtime/SQL改动，contract-impact=none，整项breaking保持。

当前来源一次安全复验：S1 11、S2 57、S3 5、S4 24、S4b 9、S4e 7、renderer18、verdict10，共141项＋4source通过，0skip；S4 headless42本机HTTP、App4本机HTTP，真实新增0。旧r2/S1/S2/S3字段已重绑当前真实证据，旧manifest/raw logs保留。S1独立证据收口；S2/S3完整自然旧K3 App迁移/取消/重新授权及S4完整TCONF04仍缺，不因元数据完整而直接判PASS。

App本轮Kimi会话01a17447-527f-7123-ab85-942f28a8e7ff是completed/interrupted/completed；暂停开关下Kimi明确不可用，显式MiniMax会话01a1744b-c762-70c2-b1ac-7a24fa81b5a3 completed。旧unknown只读未恢复、旧计划查看/取消未授权。三次正常退出、重开0补发，App/Host/Runtime/worker/adapter/端口/数据库句柄均释放。浅色已恢复，无UI交接待答。

三个final分别：core NOT RUN（完整范围缺项）；当前可达模型/状态/计划表单、键盘/焦点、1180x760亮暗视觉PASS，axe未跑且不声明完整WCAG；teardown NOT RUN（资源释放通过但Runtime checkpoint未收口）。正常退出后runtime logs_2/state_5/goals_1 WAL非空、nBackfill0；完整DB/WAL/SHM副本只读integrity_check均ok，原文件未改。不要删除WAL、手工checkpoint、强杀或把可读性当checkpoint完成。下一步先零调用收敛StateRuntime/pool正常关闭责任，若需新核心/补丁范围先提出具体最小方案。

原真实schema2 SHA2dbd19be2a8bda267437bcf0330fff1af122778388d6e3df965291ec840b7dcf和schema3均逐字保持；累计5/5已耗尽，保守14.679001元含14.188544元unknown预占。38号当前真实文本G2V仍有效，不再新增付费请求或补额。日常cutover未授权未执行。保留497原dirty、1438旧证据、日常库与旧产物；仅FEAT164本地提交、不推送，FEAT163保持独立。

2026-10-08 Sorftime 最新状态：Owner已填密钥，但两条19:19/19:20元数据初始化仍unavailable。审计发现通用HTTP迁移漏带旧链路已验证有效的User-Agent；已补真实yijie-mcp-worker/0.1.0及受限HTTP阶段/状态码诊断，未伪装旧客户端、未改固定Codex。63本地测试/lint/标准App构建通过，说明已左对齐。新worker da3c31537e6be46bb826a2ec44b0541456cbbf2810772aabbba5df1023400f81。尚未真实复验，已申请仅1次连接/发现、0模型/0业务；因先前失败不自动重发，等待用户答复。Keyring已有用户保存密钥，不要再要求重填/卸载或读取密钥。详见FEAT-157/21及sorftime-user-agent-20261008证据。

2026-10-08 19:19 Sorftime 最新续办：Owner 要求明确本机钥匙串/不传易界云端文案并重启重填。已更新文案、62测试/lint通过，标准App重启；以产品正常卸载/重装清理旧连接配置，新安全页已打开，等待Owner本人填写Account-SK并保存。不要读取密钥。此前Owner操作留下两次metadata_initialize unavailable、HTTP状态缺失，未判定原因。此轮agent模型/外部发现/业务调用仍0；Owner明确授权本次重新填写后的单次尝试，失败不自动重发。状态以FEAT-157/evidence/sorftime-market-live-20261008/ledger.json为准。

2026-10-08 Sorftime 最新决定（覆盖下方 OAuth 待确认记录）：Owner 已确认无一键 OAuth，接受手工复制 Account-SK，要求重做正式产品视觉。专用安全页已实现：沿用易界 tokens/原 SVG，单密钥字段、获取入口、保存并连接/取消，去掉 Header/Bearer/旧链路说明。62 worker 测试、lint 和亮暗/窄屏 CUA 检查通过；标准构建已实机验证新页面与正常取消同步，修复 Chrome 原 no-referrer 导致 Origin:null 的共享表单问题；精确 Origin/nonce 校验保留。App 留在 Sorftime 详情且无待处理配置，继续真实验收须用户输入 Account-SK；见 FEAT-157/21。保留原 Keyring/固定端点/逐次审批，真实业务验收额度另记，当前本轮 UI 工作未新增模型/供应商调用。

2026-10-08 Sorftime最新体验确认：Owner期望官方账号登录→授权给易界→返回连接，与Tushare一致。现有Account-SK/Bearer配置未满足该体验，不能仅改按钮/枚举冒称OAuth。本轮仅查代码与公开官方文档；公开教程仍是密钥方式，未查到第三方OAuth接入文档，须确认官方OAuth/合作授权能力后复用现有框架。不要擅自实现另一种密钥替代体验或抓取Cookie。真实验收仍暂停，之前已授权2模型/2连接发现/1只读业务额度未由本轮消耗。详见FEAT-157/20末尾。

2026-10-08 Sorftime真实验收已由Owner明确暂停：已授权本轮最多2轮Kimi-K3、2次连接/工具发现流程、1次product_detail只读查询（B07H9PZDQW，US），一次批准与一次拒绝；失败不重发、不充值订阅，密钥须用户在本机安全页输入。当前使用量全部0；尚未安装Sorftime、未打开配置页、无外部请求在途。仅查看窗口并创建台账，点击详情被用户操作保护拒绝后未继续；暂停前未输入凭据。后续仅在Owner明确继续后恢复，沿用此轮授权与零用量，不混用已耗尽的旧FEAT-157额度。台账：FEAT-157/evidence/sorftime-market-live-20261008/ledger.json。

2026-10-08 FEAT-157最新续办：Owner将FastMoss迁入跨境电商；目录revision7，总58项，跨境10/行业16。标准worker/App已重建，同构建Native窗口分类、搜索、FastMoss/Sorftime详情及聊天管理入口已通过；原锁屏窗口复验缺项关闭。17项前端、1项Native目录及Go目录检查通过，无外部/模型调用。本扩展仍未提交推送，App保留在跨境目录。详见FEAT-157/20和fastmoss-window-recheck.json。

2026-10-08 FEAT-157跨境扩展最新：9项新增完成，目录revision6/58项/7分类，Shopify明确Global Catalog。Sorftime按Owner决定统一市场配置/启用/聊天选择/逐次批准，旧弹窗/密钥环境handoff/专用执行已退役；旧历史与原生trust迁移、通用线程锁保留。34契约/59worker/40+2Native/69前端专项及Host/固定Runtime正常重启通过；canonical App曾确认58目录与9应用，最终512工具容量重建成功后Mac锁屏，未再操作最终窗口。没有新增外部或模型调用，原额度仍耗尽；未提交推送本扩展，原49项Git授权已经执行完毕。实现/证据详见FEAT-157/20。保持用户原有UI/启动器改动，严禁强杀或故障/攻击注入。

## 文档状态

- 状态：Accepted
- Owner：段成威
- 最后更新：2026-09-24
- 适用范围：`yijie` 多仓项目的需求起草、调查、设计、实现、验证、评审与发布协作

## FEAT-155 当前交付权威（2026-09-24）

本机隔离候选D4及获明确授权的五仓本地版本固化完成。最终Runtime `fb79b1d53501ec90084b584af5fdbe221c7a25aa` → Contracts `54be9314dce5319b049dc0a236800fd1a1fdd7a1` → Host `56e9a924454e850bd181c452c35078b3e0a36954` → Desktop `be15d237fc0422f6072d0b6ec6d668b49d4c692e`；元仓由包含报告的Git提交定位。原生回归发现的已释放旧interrupt重复claim已最小修复，132项复验及最终canonical正常启动/重开通过。详见[50关闭报告](../features/FEAT-155-desktop-scheduled-tasks/50-local-version-freeze-and-closure-report.md)。后续已明确授权全部仓库提交并普通推送，当前远端同步见[51](../features/FEAT-155-desktop-scheduled-tasks/51-remote-delivery-2026-09-24.md)；没有tag、合并或产品发布。全仓make lint仍被既有Skills HEAD不匹配阻断，不宣称全仓CI通过。

持续边界：本地计划同一SQLCipher/worker，复用Coordinator/outbox与Codex执行、审批、历史；草案采用已核实的input-only原生扩展。普通SQL15/Store5、显式隔离候选26/6，无日常库迁移。有限自动授权和单次许可分开，历史不重发，未知不伪终态。用户明确移除防自动空闲睡眠与睡眠后停止发送，系统通知延期；不擅自恢复这些需求或扩大为云调度。真实文本13/14、余1；本次固化付费与本机请求均0，不以余量扩大验收。

## FEAT-132 当前权威（2026-09-09）

用户已授权将 FEAT-132 改为“Codex 原生对话机制接入与视图适配”，删除自建 reducer、hydrate/reconcile、正文对账、身份猜测与自动封口；不得迁移或换名保留。Codex 决定执行事实，Desktop 保存加密产品记录，Native 仅一处显示缓冲；旧记录只读。

当前实施已授权并完成本地源码提交，最终 contract-impact=breaking，必须版本化迁移旧消费者。Desktop migration 14 / Host schema 5 都不允许无兼容方案降级写入。固定 Runtime/FEAT-136 产物不变，FEAT-137 永久退役，FEAT-152 权限语义不变。

原 D4 不继承。本次已固定 Contracts 6f632f155eacdaf93df0e0b00b5dab9e369c5442、Host 9e9d317f7e4ecff5f8aeec94fa467f9bede32139、Desktop 5e6ada73ed8b9d49dde51e4b6659ce5337304a6e；FEAT-152来源阻塞已解除，FEAT-137永久退役。用户明确授权本地提交、必要修复及25次文本/3次图片预算；实际19次文本、1次图片，临时权限模式已恢复请求批准。真实canonical启动/附件/命令/三种权限模式/原生中断/退出重启/Artifact验收通过，十项AC与local D4均PASS；未推送或发布。详见[最终验收](../features/FEAT-132-desktop-conversation-domain-state-machine/02-verification.md)。

2026-09-09日常入口收尾已通过：Desktop当前为c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b，包含单独提交的权限弹窗UI、说明修正及旧清理记录的只读历史修复；Contracts/Host来源不变。普通canonical入口沿用原Host Home和app-data，8条原Host映射及最后Turn身份/状态保持一致，旧附件历史与Artifact正常重开。本轮未增加模型调用，历史清理未完成、附件过期及隔离Host缺少映射仍如实保留。详见[日常入口报告](../features/FEAT-132-desktop-conversation-domain-state-machine/05-daily-entry-verification-2026-09-09.md)。

用户随后明确授权所有仓库审计、提交与推送；上述验收报告中的“未推送”是当时的历史状态。本次同步现有工作分支，修正Contracts/Host说明，源码consumer pin保持不变；Desktop CI来源/目录布局和Host旧测试断言仍列为合并前事项，不能把Git推送等同完整CI或发布通过。详见[多仓审计与同步记录](workspace-git-sync-2026-09-09.md)。

## FEAT-134 当前权威（2026-09-09）

FEAT-134已按用户确认任务收敛为FEAT-132 native v7之上的流式/过程展示：summary与raw按原生类别/索引分开，Item availability及安全诊断可见，UI busy仅由当前有效订阅观察驱动，Turn结束不封口Item。旧v4/v5历史及资源适配保留，无调用发布残留及冲突测试已清理。原2026-08-29 D4完整归档，本次八项AC与local D4通过。

当前本地提交：Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3、Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b、Desktop 6e5047d1c23041c46dd495ddb89e24c7e4db5d47。native Contracts源仍固定6f632f…；Desktop权限消费者及CI改用真实Host提交，42项来源校验通过。CI目录布局已修正，但本轮不推送，不代表远端CI/合并/发布通过。

普通canonical入口使用原app-data/Host Home，两次正常启动/退出，既有历史/附件/Artifact/权限入口复查通过，8条原Host映射及原生终态未变；233项前端定向测试及Host/Native/SQLCipher验证通过。本轮模型请求0，不转用FEAT-132或原FEAT-134预算。原生缺阶段/冷历史不完整、Command完成后展示输出、附件过期、清理未完成和隔离任务无Host映射等限制仍保留。详见[FEAT-134最终验收](../features/FEAT-134-desktop-streaming-progress-final-response/02-verification.md)。

## FEAT-131～136 一致性审计（2026-09-09）

FEAT-134 四个本地提交在用户“授权执行”后已按 Contracts → Host → Desktop → 元仓顺序普通推送，远端 SHA 相等；精确 SHA 的 Actions 查询均无运行，CI NOT RUN。没有合并、tag 或部署。本轮新增修改没有混入这四个提交。最新状态以 [FEAT-134 远端记录](../features/FEAT-134-desktop-streaming-progress-final-response/04-remote-delivery-2026-09-09.md) 为准。

FEAT-136 现状审计确认：命令执行和最终输出来自 Codex，Desktop 复用 FEAT-132 native v7/唯一缓冲/SQLCipher；Host native 主动不传 Command delta 正文，等待 aggregatedOutput 后安全投影。旧 v5 有真实兼容路由和容量计数，不能整包删除。审计发现的目录标签、输出完整性、空输出与历史 running 文案问题已按[执行方案](../features/FEAT-136-desktop-command-tool-items/03-native-command-audit-and-plan-2026-09-09.md) 实施并取得本次八项 local D4 PASS；真实3/10文本、0图片，两条 Command 成功/失败及正常重开通过。本次交付收尾已另获明确授权，Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688 → 元仓 4e6645574fdfe7d29f7c551564bf807cf8222d48 已普通推送且远端 SHA 相等；两提交 CI 未触发，NOT RUN。详见 FEAT-136 的 04-delivery-closure-2026-09-09.md。原验收 base commit 与逐文件 SHA-256 保留；原 2026-08-30 五项 Command D4 保持历史语义，Tool当时仍属FEAT-144 blocked / NOT RUN；其后续本地交付见下方FEAT-144当前权威，不改写FEAT-136历史范围。

六项需求已补充当前依赖与证据适用范围，能力矩阵修正为当前 native 事实。后续不恢复 ConversationState/reducer、正文对账、身份猜测、自动封口或历史重建；日常 app 与原 stable 隔离数据、FEAT-152 与已终止 FEAT-137 分开记录。详见[整体一致性复核](../features/FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。审计阶段模型调用为0，授权后的FEAT-136实施验收为3/10文本、0图片。

## FEAT-144 当前交付权威（2026-09-11，本地验收、AC-004用户排除）

远端交付更新：用户明确授权的22个提交已按Contracts→Host→Desktop→元仓普通推送；远端完整SHA分别为811f38d6b104fa18477107e7ac91a85e19c445d1、0e47766f494977c94bfea0e89cfbdf45a7fafa2b、5964e2f7c31ea298f801df02086abbc8d6676b91、2febf02b2e9ad21d3996c108a9ac8d0a0c551db5，逐仓核对一致。Desktop包含已告知并授权的首页动画祖先与CI两ref修正；D4产品源码仍为7abf89e8。三种GitHub检查查询均0条，CI NOT RUN。新增结果记录仅本地提交，不自动突破22个提交推送范围；详见[26](../features/FEAT-144-desktop-real-tool-producer-items/26-remote-delivery-2026-09-11.md)。

固定Runtime0.144.6原生元数据连接阻塞已关闭：操作7初始化ready、操作8返回97工具/Sorftime MCP1.1.6；无query URL、原生bearer_token_env_var引用及真实User-Agent codex-mcp-client/0.144.6。连接技术依据保留13；当前范围/预算权威为[15用户决策](../features/FEAT-144-desktop-real-tool-producer-items/15-owner-scope-and-business-budget-2026-09-10.md)及分账台账。本地验收以[24最终报告](../features/FEAT-144-desktop-real-tool-producer-items/24-final-native-decline-and-delivery-2026-09-11.md)及分账台账为准，远端交付以上方26为准，不重复消耗额度验证同一连接。

原操作1–3及6的HTTP400/request error失败历史保留。两版实际二进制对普通localhost服务的初始化观测除真实版本外一致，固定版缺User-Agent；仅补真实UA后固定版远端成功，足以确认该原生配置可用，不等于证明服务端唯一拒绝规则。操作4/5的本地Codex0.153.4对照仍为历史证据。固定binary SHA 4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d不变；未升级/修改/替换Runtime或安装ZIP bridge。

product_detail及asin/amz_site输入schema当前由固定操作8确认，asin必填、US显式传入；只启用该单工具。enabled_tools不限制参数，审批要呈现原生tool_params中的实际ASIN/站点；参数不明或越界拒绝，不从助手正文推定授权。首期只读US公开商品查询，无商家写入，不承诺服务端幂等或免费。

结果采用原生text块/稳定索引、最多32个原始content条目和既有256KiB UTF-8容量、复用既有完整文本脱敏后纯文本展示。safeNativeText仅NUL/容量处理，不能冒称脱敏。未返回outputSchema/annotations或progress不补造，也不独立阻断该展示设计；没有可展示文本不代表商品无数据。status/availability/诊断/busy分离，原生failed即使error=null也不改completed。

[12契约与reader方案](../features/FEAT-144-desktop-real-tool-producer-items/12-independent-contract-and-reader-plan-2026-09-10.md)已细化：Contract First；兼容reader/格式版本拒绝先于新producer写入；未知格式用本地recordDiagnostics定位，不生成NativeView或触发冷读补建；DB user_version过高仍整体拒绝。schema15 expand migration已实现并通过合成数据前向验证，旧JSON/历史migration不改，回滚仅到已验证兼容reader，不复制用户DB。

秘密首期只存受管进程内存，正常重开重新输入；原生shell_environment_policy.exclude需核对set和实际执行环境不重注入。稳定elicitation空form按request/thread/可信turn关联，原生accept/decline/cancel/resolved处理，无itemId不猜卡片；其它未支持请求继续拒绝。FEAT-152语义不变，FEAT-137永久退役。

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。实际thread响应/配置与Prompt已验证；20的配置阻塞已修复，当前E已获当场确认，模式切换和正常重开通过；原生Prompt不复用Auto批准缓存。

用户已明确“不做业务失败场景的验证，跳过这个逻辑实现”：AC-004/F144-S03从当前Must范围移出，标OWNER_EXCLUDED/NOT RUN，原编号不复用、旧四文件逐字归档、不算PASS。不新增Sorftime业务错误字段、分类器、失败专用分支或样本；已有原生failed与通用安全处理仍如实保留。无需再索取官方正常失败条件，不用成功/空结果或权限拒绝替代业务失败通过。



当前产品来源：Contracts `811f38d6b104fa18477107e7ac91a85e19c445d1` → Host `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` → Desktop `7abf89e84ffcbe56360d8c9943390e0640d9e239`，此处为24本地验收时固定的产品来源；后续CI提交及实际远端位置以上方26为准。本次文档提交由Git记录定位，不填造自身SHA。最低兼容reader仍为 `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`，Runtime未改，源契约/来源门禁保留。

第二个启动阻塞来自旧B queued/null-native-Turn和failed v1出站被当成活跃执行。新增独立只读原生当前状态端点，复用thread/read(includeTurns=false)；Desktop严格核对原失败投递及无待派发出站，原生idle/notLoaded后再次只读复核。旧记录不改、不补发、不封口；notLoaded不证明过去未执行。旧history/迁移/权限wire不变，未知/active/systemError/缺能力仍拒绝。详见23。

E真实成功/数据对照/模式停用及auto/full/ask保留Host ccd815ff/Desktop a5975f48的实际来源；十二相关文件逐字不变确认适用。F在最终提交实际点击原生Prompt拒绝，审批rejected，唯一Tool failed/0ms/result=null而Turn completed；模型不重试、不使用旧数据，普通canonical正常退出重开F/E通过。没有把不同提交/进程的证据说成一次全量实跑；按用户指定“修复后拒绝复验，再收尾”完成证据组，最终strict/D0/D4已实跑PASS，机器输出见24。

九项活动AC已有实际证据，AC-004保持OWNER_EXCLUDED/NOT RUN。累计文本9/13、元数据14/20（拒绝本轮2/5）、业务2逻辑调用保守扣4/10、图片0；精确历史业务HTTP次数未知，保守扣账不返还。F新增业务0，最后的原生只读核验和普通重开无模型/MCP调用；应用、Host、Runtime和计数器均正常退出。没有等待隐藏输入或预算批准；实际22个提交推送已完成，无tag/部署。

保留旧B结果不确定、Tool正文partial脱敏、冷历史/phase/plan/reasoning/outputSchema/annotations/progress缺失、Command完成后输出、旧附件过期/清理未完/隔离Host映射缺失。剩余额度不自动转用；后续工作重新核对实际来源和台账，不从旧记录自动续跑。

## 1. 单人开发角色默认值

易界当前采用“段成威一人使用 Codex 开发”的工作模式。除非段成威针对某个需求明确指定其他人，新 Feature Package 和交付文档默认使用以下角色：

| 角色 | 默认负责人 |
|---|---|
| 需求负责人 | 段成威 |
| Product/Design 决策人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |

Codex 起草新需求包时应直接填入这些默认值，不重复询问。某个需求存在临时协作者、外部评审人或专门 Owner 时，以段成威在该需求中的最新明确指令覆盖默认值。

同一人承担多个角色不表示适用 Profile 的确认可以伪造：

- `production_hardened` 的需求确认、技术批准、代码评审和发布批准仍是不同动作，必须分别记录真实日期与结论。
- `demo_fast` 至少分别记录 D0 产品/UX确认、D4 真实可用结论，以及条件性的付费/破坏性/公开操作批准。
- Reviewer 为段成威时，不得把 Codex 自己的总结描述为“独立人工评审”。
- Codex 必须在实现完成后执行一次与实现阶段分离的结构化审查，主动寻找错误假设、回归、权限、兼容、测试与回滚缺口；最终批准仍由段成威作出。
- 高风险安全、资金、数据删除、生产迁移或不可逆架构决策即使由同一人负责，也不得降低确认、验证、审计和回滚要求。

## 2. Codex 与段成威的职责边界

Codex 默认负责：

- 调查当前代码、文档、测试、Git 状态和多仓影响；
- 起草需求、验收标准、影响评估、决策选项和风险；
- 给出有证据的推荐方案及取舍；
- 起草契约、技术设计、测试计划、实施切片和验证证据；
- 在获得适用门禁后实现、测试、审查和整理交付材料；
- 如实报告失败、未执行项、假设、未知项和残余风险。

段成威负责：

- 最终确认用户价值、范围、优先级和业务语义；
- 最终确认产品、设计、技术、安全和生产决策；
- 审阅 Codex 的候选方案、代码和验证证据；
- 明确授权提交、推送、发布、迁移和外部写操作。

Codex 不得虚构段成威已经批准尚未展示或尚未确认的内容。段成威明确授权“由大模型自行构思/定稿”时，Codex可以选择推荐方案并写成候选决策，但仍要说明理由、影响和验证方式。

## 3. 每次需求起草前的强制高质量协议

Codex 在输出需求结论或开始修改文件前，必须完成以下检查。不能用“快速总结”代替真实调查。

### 3.1 加载上下文

1. 读取本文件、当前作用域的 `AGENTS.md`、Feature Delivery Handbook 和已有 Feature Package。
2. 读取用户本轮请求、附件、视觉稿、已确认决策和前序未完成事项。
3. 从 `repos.yaml` 确认可能受影响的仓库；进入仓库后重新读取该仓规则。
4. 检查相关仓库的 branch、完整 HEAD、remote 和 `git status`，保护已有改动。

### 3.2 核对工程事实

1. 找到真实入口、路由、调用链、状态管理、持久化、权限、测试、构建和发布入口。
2. 阅读相关源码、测试、设计 Pattern、ADR、安全和契约文档，不根据文件名或聊天印象猜实现。
3. 明确区分：
   - Fact：已有代码、命令输出或用户明确确认；
   - Assumption：为继续推理采用、但尚未确认的前提；
   - Unknown：必须调查或由段成威决定的事项；
   - Conflict：代码、设计、需求或 ADR 之间的不一致。
4. 对可能随时间变化的外部事实使用当前权威来源验证，不依赖旧记忆。

### 3.3 完整推演需求

起草时至少推演：

- 目标用户、问题、价值、主流程与明确非目标；
- success、loading、empty、error、permission denied；
- 超时、取消、重试、重复、并发、部分成功和恢复；
- 认证、资源授权、租户隔离、secret、PII、日志和审计；
- 数据生命周期、持久化、migration、兼容和回滚；
- 性能、可访问性、主题、最小窗口和可观测性；
- 外部副作用、审批、费用、生产账户和不可逆操作；
- 公共契约、Runtime、第三方、模型或 AI Eval 是否受影响。

`demo_fast` 仍需推演这些场景以避免逻辑和 UI 空洞，但可以把不影响本地正常使用的性能、完整安全
专项、韧性、migration、可访问性和生产观测明确登记为延后；`production_hardened` 逐项写
`N/A + 理由`，不能静默省略。

### 3.4 形成高质量决策

1. 对重要未知项给出 2—3 个真实可行方案、取舍和推荐理由。
2. `demo_fast` 优先选择逻辑完整、交互清晰、依赖最少、能最快通过真实服务的方案；`production_hardened` 优先选择可维护、可测试、可回滚且不扩大权限/契约范围的方案。
3. 段成威已经授权 Codex 自行决定时，使用最佳工程判断推进，并把决定、理由、兼容和回滚写入文档。
4. 只有会实质改变目标、安全、数据、成本或不可逆架构的缺失信息才停止请求确认；其余问题给出推荐默认值并继续。
5. 不因赶进度降低当前 Profile 的 Must AC、Contract First、secret/PII、服务端授权、审批/审计和真实服务标准；Demo 可按已声明边界延后非必要生产加固，不能把延后项写成 PASS。

### 3.5 建立可追踪交付链

`production_hardened` 必须能追踪：

```text
用户价值
  → 业务规则
  → 验收标准
  → 技术设计
  → 测试用例
  → 实施切片
  → 验证证据
  → 发布与回滚
```

`demo_fast` 使用更短链路：

```text
用户结果 → 业务规则/UI 状态 → Must AC → 整体实现 → 真实服务 fresh run → Artifact/限制
```

Codex 完成需求草案后必须自检：

- 是否存在相互冲突的 Must 规则；
- 每条验收标准是否可判定、可测试；
- 是否把假设写成事实或把候选写成批准；
- 是否遗漏失败、权限、持久化、兼容和回滚；
- 是否错误扩大到用户没有要求的业务能力；
- 当前 Gate 状态是否与真实文档和验证证据一致。

## 4. 开发与门禁原则

- 新需求默认 schema v3 `demo_fast + local`：D0 后整个需求连续实现，不建立治理切片；实现结束立即启动真实服务，有 Bug 就修复、重启、复测，直到一次 fresh run 中全部 Must AC、真实 happy path 和代表性 failure/retry 通过 D4。
- `demo_fast` 默认目标 12 小时、硬停止 16 小时。`exposure: public` 在首次对外访问前补 DP；出现付费用户、SLA、多租户/PII、重要持久数据、不可逆 migration、合规或生产责任时建立显式 `production_hardened`。
- `production_hardened` 保留原规则：G0/G1/G2 前不开始正式实现；`contract-impact != none` 完成适用 G2A；provider/consumer 大规模实现等待 G2V；按 per-slice G3→G4→G5→G6 推进。
- 两种 Profile 都必须 source-first：先确定并修改契约权威源，再生成/验证和更新下游；不得复制影子 DTO。Demo 本地 sibling 结果不冒充不可变 tag、发布兼容或生产批准。
- 测试、构建、视觉检查、集成、生产 smoke 和发布状态只根据真实命令与环境证据填写。
- commit、push、tag、发布、生产迁移和外部写操作仍需要段成威的明确授权。

### 4.1 production_hardened 三次失败熔断

当同一命令、门禁、runtime 阶段、稳定错误码或实质相同的失败条件连续出现三次时，Codex
必须停止机械重试以及“改一点—再验证”的惯性循环。即使此前获准多次重试，第三次同点失败后
也必须先进入深度反思；重复执行相同命令不能算作新增证据，不能以“再跑一次可能会绿”代替
根因分析。

进入深度反思后必须：

1. 汇总三次失败的时间线、完全相同与发生变化的证据、已做修改及每次修改为何没有触及根因；
2. 重新区分 Fact、Assumption、Unknown 和 Conflict，撤回已被证据否定的判断，不把稳定
   failureCode 的命名直接当成已证明的根因；
3. 从局部症状扩展到完整调用链和状态生命周期，允许扩大只读搜索/审计范围至受影响仓库、
   路由、权限、状态管理、构建配置、runtime、平台行为、测试 harness、规范和门禁，寻找所有
   重试共同依赖的不变量；
4. 明确区分实现缺陷、harness/观测缺陷、环境或平台缺陷、规范/门禁矛盾及数据/时序竞态；
5. 形成按证据排序、可证伪的根因假设，为每个假设列出最小区分证据，并只推荐一个下一步
   诊断或最小修复；
6. 复核安全、权限、契约、持久化、cleanup 和用户已有工作树，确保扩大审计范围不等于扩大
   写入或实施授权；需要新写入范围、外部副作用或新的真实 runtime 时，先取得明确授权；
7. 在根因未收敛前，不提交、不更新 PASS/门禁状态、不启动依赖该门禁的后续切片，也不通过
   绕过 production 路径、放宽断言或把失败分类改名来制造绿色结果。

深度反思的输出至少包含：当前真正卡住的最早阶段、三次失败证明了什么和没有证明什么、
此前方法的错误假设、扩大审计后的候选根因、区分候选所需的最小证据，以及推荐方案的停止
条件和回滚。修复完成后优先执行 focused 静态验证，再在单独授权下执行一次有区分力的真实
验证；不得重新进入无上限的验证—修复循环。

### 4.2 demo_fast 调试时间盒

- 30 分钟没有新事实：停止猜测式补丁，检查真实日志和完整调用链；
- 90 分钟同一核心阻塞：采用最简单方案、关闭非核心花活或提出一个 workaround；
- 非核心测试/harness 累计 120 分钟：登记限制并降级，不继续阻断业务结果；
- 核心结果 240 分钟仍不可用：更换架构、缩小 MVP 或请求一个关键决定；
- 总工时达到 16 小时仍未 D4：停止扩建流程并重新定范围。

时间盒不允许“重跑到绿”、隐藏失败或降低 Must AC。每轮修复必须基于新增事实，D4 仍要求一次真实
fresh run 完整通过。

## 5. 长期记忆的使用边界

本文件记录稳定的协作偏好和角色默认值，不替代对当前代码与环境的调查：

- 当前实现、版本、仓库状态、API、依赖和生产环境必须每次重新验证。
- 最新的用户明确指令优先于本文件中的默认值。
- Feature Package 是单个需求的权威交付记录；本文件不能替代需求内的具体决策和证据。
- 如果工作方式发生长期变化，应更新本文件的状态、日期和变更内容，不依赖聊天历史维持隐含规则。

## 6. 本地优先开发与生产安全补齐

本节保留 FEAT-125 等历史 `production_hardened` 包的里程碑语义。2026-08-23 之后的新本地需求默认
直接使用 `demo_fast + local`，不再为本地 Demo 机械建立 G0–G6；历史 v1/v2 Gate 状态不因新默认而重写。

易界当前允许在尚未购买云资源、未准备生产 IdP 和签名发布能力时，把安全基础需求登记为
`Local Engineering Baseline Complete / Production Activation Blocked`。该状态只表示契约、
服务端领域能力、consumer、默认关闭策略及本地合成验证足以支撑后续业务代码开发，不等于
Code Complete、Production Ready、Delivery Complete 或发布授权。

进入该状态后：

- 可以继续开发首页、聊天、Tasks 等业务功能，并使用本地合成 identity、tenant、RBAC 和
  capability 数据验证流程；
- 每个新业务需求仍须建立自己的需求包并通过适用的 G0/G1/G2/G2A、测试与结构化审查；
  FEAT-125 本地基线只解除对生产身份环境的等待，不是跳过后续需求门禁的通行证；
- 身份与权限 feature flag 必须继续默认关闭，业务 API 的服务端授权、租户隔离和审计要求
  不得用前端投影、mock 或本地里程碑替代；
- 未完成的真实 IdP、签名 Keychain、跨仓 bearer、refresh-family、性能、监控、部署和回滚
  证据必须作为可追踪的生产激活阻断项保留，不得写成已接受风险或 PASS；
- 当段成威决定真实部署整个 yijie、购买/准备服务器数据库公网资源、选择生产 IdP，或准备
  Desktop 签名发布时，必须先恢复完整生产级身份安全链路，复跑对应 S7/G4/G5/G6，之后
  才能打开 feature flag、创建 release tag 或进行生产激活。

FEAT-125 是该策略的首个实例：本地工程基线完成，S7 冻结到真实部署准备阶段；FEAT-124
G4-001 与 FEAT-126 的 Tasks 服务端资源授权仍按各自生产门禁保持开放/阻断。

## 7. 变更记录

- 2026-07-30：建立单人开发角色默认值和需求起草前的强制高质量协议。
- 2026-08-01：增加本地优先里程碑规则；FEAT-125 本地工程基线完成后允许继续业务开发，完整生产级身份安全链路在真实部署前强制补齐。
- 2026-08-22：增加“三次同点失败后强制深度反思”规则；停止机械重试，扩大只读审计范围并以可证伪证据寻找根因后，才允许提出下一步诊断或修复。
- 2026-08-23：依据 ADR-0017 建立双 Profile；新需求默认 `demo_fast + local`，以产品/UX完整、整体实现、时间盒和真实服务 D4 闭环为准；公开 Demo 增加 DP，生产加固保留原 G0–G6 与三次失败熔断。


历史阶段检查点（已由24最终报告取代）：当时FEAT-144检查点以[20实际D4与权限重启阻塞](../features/FEAT-144-desktop-real-tool-producer-items/20-d4-permission-restart-blocker-2026-09-10.md)为准。Contracts db54c617c65db5431b950eb297ba148a43a8e600、Host 635846f72ef4b0d940798215e7b79d58aed6c591、Desktop 95afd425fd5b55ada9f13b43421ad2c06830dc5c；最低reader 25b004fbd5a4dcf642a503d302c21a7d6e3b817f先于writer固定。均仅本地提交，Runtime未改、FEAT-137永久退役、FEAT-152语义不变。

普通canonical使用现有app-data和日常Host Home完成真实Sorftime查询、原生Prompt正常拒绝、返回值对照及UI/旧历史检查。用户已授权本次临时auto/full并恢复ask，但auto触发旧Runtime正常退出后，Codex原生projects信任记录与Host精确受管模板冲突，重启被拒绝；权限仍ask，full未尝试。所有进程已正常退出，没有等待输入。Tool事实已存SQLCipher，普通Tool重开尚未验证；D4未通过，AC-004仍用户排除。先审定原生信任记录与受管配置兼容，不忽略/删除projects，不换Home掩盖问题，不放宽门禁。元数据10/10、模型4/8、业务1逻辑调用保守扣2/10、图片0；重连另需元数据授权，不转用额度。

历史阶段检查点（已由24最终报告取代）：FEAT-144最新续办：用户明确授权修复原生项目trust/受管配置兼容并验证重开、权限切换，另增10次元数据，累计上限20/已用10。固定0.144.6 app-server不支持命名profile，但原生-c覆盖与base项目trust在无凭据、无MCP/模型的正常thread/start、EOF重启测试通过；现有配置精确模板前缀已核对，拟分离Host受管安全模板与Codex原生trust尾部并保留原字节。方案见21；go-toml/v2@v2.4.3已获用户明确授权并验证固定源码校验和；Host修复65f7b3212fbeb62b3b828cc1ca8997076f1f6b29、Desktop pin c784d842b59c063b4f357fce8445d9edb808370f已本地提交，无调用集成和来源检查通过，开始普通canonical验证。业务保守2/10、模型4/8、图片0不变，本地提交授权沿用、推送未授权。

历史阶段检查点（已由24最终报告取代）：FEAT-144继续执行检查点：最新Host ccd815ff63542674daa80172a1c71ac7478edd0f、Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961；普通canonical已使用同一用户数据正常启动/重开B任务的两条Tool，并正常退出。root config只保留两条trust原始字节，受管模板独立精确校验。当前Sorftime标准构建完成、系统隐藏输入等待用户，未启动新的MCP操作；计数器沿用4/8，元数据10/20、业务保守2/10、图片0。不要用CUA getApp在未启动/已退出时复活无环境应用；退出后通过ps或应用清单确认。下一步用户隐藏输入→正常真实连接/Prompt→取得当前UI权限切换当场确认→auto/full/ask及正常重开，按台账控制，不自动追加预算。

历史阶段检查点（已由24最终报告取代）：当时配置兼容阻塞已关闭：当前Host ccd815ff63542674daa80172a1c71ac7478edd0f、Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961。新E真实Tool completed/414ms，原生返回三字段对照通过；Sorftime正常停用、auto/full/ask、原数据canonical退出重开均PASS。累计元数据12/20、模型7/8、业务2逻辑调用保守扣4/10、图片0；应用与计数器均已正常退出。D4尚未关闭：当前来源下的原生Prompt正常拒绝未复验，不能继承旧B结果；已申请最多追加2次文本，未获授权不调用。AC-004始终用户排除。 详见22。
