# FEAT-164 实施计划与当前门禁

> 最新以[45 旧隔离库受控迁移入口](45-controlled-isolated-migration-entry.md)为准：显式维护入口已实施，SQL29/37正常旧数据的拒绝/迁移/备份/重开离线资格通过；普通旧库门禁和日常拒绝保留。当前SQL41候选因1条未就绪选择与2份占用正常拒绝维护，原5522文件保持。实现仅在Desktop隔离commit bc3b097，主工作区未应用；真实/本机模型新增均0，完整App/G3/final仍缺。

> 当前权威见[44 自然旧K3与计划离线验收](44-natural-legacy-migration-and-plan-qualification.md)：r5已加载旧身份经实际Host切换、正常取消/恢复子集通过；自然SQL29计划经显式正式迁移后的退役/重审/新授权/取消及重开通过。旧库App入口仍明确拒绝SQL<38，完整S2/S3纵向未通过。产品/Runtime未改，真实模型0，本机合成8，旧账本与预占保持。以下旧记录按原来源解释。

> 最新深入复审见[41 关闭方案再审](41-shutdown-plan-deep-review.md)：RCA后6项新unit＋6项RPC及Clippy通过，但listener无退出回执、RPC屏障顺序待修正。四文件候选未晋升；建议仅扩展thread_state/thread_lifecycle两文件，**待新增范围批准**。r5未构建，真实新增0。

> 最新续办见[40 Runtime正常关闭审计与最小方案](40-runtime-shutdown-audit-and-minimal-plan.md)：单次零回合EOF复现未回填WAL，4库只读完整性ok；已收敛所有者排空日志并await四池关闭的候选。**核心/patch尚未修改，待Owner确认**；teardown/core及整项状态不变，真实新增0。

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

## 当前有效状态（2026-10-25，30元单次续验）

| 项目 | 当前结论 |
|---|---|
| 来源与工程门禁 | Runtime r2 / Contracts / Host固定；Desktop40908c7独立固化；G2A及当前Harness PASS |
| 真实G2V | 本次新增唯一HTTP200，正确答复42、usage/保存/重开/无补发/正常清理及组合oracle PASS；r1 FAIL保留 |
| 预算与请求 | 累计30元；仅新增1HTTP已耗尽。旧预占14.188544元＋本次保守0.139590元＝14.328134元；不再新增请求 |
| 已通过历史 | r2 canonical实际App本机合成答复、保存、重开、正常退出；不等于真实模型通过 |
| 尚未完成 | S1—S4、TCONF-164-01—04及三个final；不放行日常库迁移或发布 |
| Git | 仅FEAT-164本地提交已获授权，不推送；保留其它需求改动 |

本轮权威为[20 单次续验](20-budget-resume-and-g2v.md)、feature.yaml和追加后的真实账本。13—19按各自时间与来源保留历史语义。TCONF-164-01—04仍为计划目标，执行前核实selector存在且测试命中数非零。

## 门禁和技术依赖

G0/G1/G2审阅 → 实际业务契约源与适用G2A → 安全Harness资格 → 最小G2V → S1 → S2 → S3 → S4 → 三项final E2E/G4。G5/G6仍受local exposure及独立发布批准约束。

G2前不进行产品实施。G2/G2A之后允许的只是受限契约/垂直候选，不授权大规模分层实现。Runtime权威例外必须保留：最小Runtime候选先产生自己的canonical来源，Contracts随后投影；不能为满足业务Contract First伪造尚不存在的Runtime digest。该候选只用于资格验证，不能提前替换日常App。

## 切片

| Slice | 行为/AC | 未来改动仓库 | 前置 | required证据/回退 |
|---|---|---|---|---|
| S1 | 新活动身份、受管配置、独立候选/激活与退役准入骨架；AC001/002/007 | Contracts/Runtime/Host/Desktop | G2/G2A/G2V | local+boundary+vertical，TCONF-164-01；未激活时保持旧环境，不覆盖旧binary |
| S2 | reader/三表/Host状态迁移、模型选择与显式恢复、普通/市场never-sent安全取消；AC003/004/005 | Contracts/Host/Desktop | S1 | 同上，TCONF-164-02；兼容reader保持，无降库 |
| S3 | worker接管前保护、计划领域退役/重新授权及历史run；AC005/006 | Contracts/Host/Desktop | S2 | 同上，TCONF-164-03；暂停新派发、保留原run恢复 |
| S4 | 全实际调用面、UI、同源打包、正常退出/重开/兼容回退；AC007—010及全部回归 | Runtime/Contracts/Host/Desktop；Connectors回归 | S3 | 同上，TCONF-164-04及三个final独立判定；单独关新Kimi，MiniMax/历史可用 |

每片status=pending，commits为空，所有local/boundary/vertical=NOT RUN。源实现以本包职责为限，不混入FEAT-162/163补救、无关重构或旧证据批量改名。

## 具体序列

1. 再读本轮授权、各仓规则、dirty基线；范围和版本审阅后固定source-first依赖及全部consumer。
2. 权威模型源实现三层身份及版本兼容，刷新全部引用的生成物/validator/来源锁；不是手改派生物。
3. canonical最小Runtime修订及独立路径/manifest，验证旧input-only权威和当前web-sources schema；更新实际launcher路径与所有pins。
4. 完成兼容reader/版本握手和停派发能力，不让新Host启动时隐式激活；受管双文件过渡组合精确识别。
5. 先用普通合成旧库验证表约束、数据和恢复。日常迁移前必须有可读新旧数据的回退构建与明确操作许可。
6. 经正常应用流程收敛所有旧主聊/标题/审核/草案/子代理，确认无受管在途；不强杀，不启动旁路模型。
7. 在worker接管前迁移schema/分类旧身份/装准入；计划通过领域事务暂停撤授权。unknown保留，未结清不得派发。
8. 明确cutover；新聊天/标题等新任务允许新model，旧会话首次继续先完成新模型选择operation；旧计划保存后重新授权。
9. 按独立预算运行获准的真实验收，检查出站/流式/历史/计划/恢复；失败回滚到兼容组合或前向修复。

## 来源冻结及Git

Runtime → Contracts runtime projection → Host runtime constants/candidate → Desktop实际功能组合选择的artifact-media / experts / chat-model Host build candidate → canonical打包/运行receipt。模型业务源与consumer生成先完成；最终freeze必须绑定当前所有启用契约/专家/资源来源，覆盖experts=true且artifact_media=false的独立分支。

用户已授权仅本地固化FEAT-164及必要验证治理记录；按专属路径/差异逐仓提交，不混入FEAT-162/163。不新建branch、PR、推送、tag或发布；构建从固定提交的干净资格工作树产生。实际SHA产出后登记。

## 证据失效与停止

每个G3单片评定，commits覆盖自身和transitive前置，contract/fixture/harness/platform/bootstrap引用精确。任一变化使相关证据STALE。三次等价失败按fingerprint累计，进入append-only RCA，收敛唯一下一动作后才可在授权下重试；禁止第四次机械尝试。

设计变更回跳01/03，契约与语义回04/04A，数据/恢复回05，验证阈值回06。当前方案与实施已获Owner确认；G2A、当前Harness及预算受限文本G2V已通过。判定与预算恢复、本次唯一真实请求及正常重开已完成；S1—S4仍须逐片实施和新鲜证据，不能借用本次通过。后续代码改变使相应来源证据过期，追加真实模型请求须另有明确额度。

## S4g 旧草案状态续办（2026-10-25）

下一步的旧失败草稿状态修复已本地固化181885b，真实历史UI及只读保留通过；完整恢复取消/旧计划重授权、专家媒体组合及G3仍pending。通用生成入口先读s4g RCA，不机械重试。

## S4h 生成入口与计划验收（2026-10-25）

生成入口RCA修正后的首次19项通过，旧FAIL保留。当前计划模型变更后旧配置拒绝、重新审阅保存paused和独立单次授权已在App验证；后续转当前专家/媒体组合及完整恢复取消，见34。

## S4O 实施状态（2026-10-26）

Owner已在必要性复核后批准41号六既有文件范围，0011/r5及必要下游来源已本地固化；限定loaded-thread正常EOF与四池关闭通过。19项来源检查、四组合来源和canonical App构建通过；App首次无凭据启动未就绪，正常退出且原数据保持。下一步先零模型排查Native启动配置，随后补r5 Host/App纵向；不扩大核心、不要重跑旧141项替代新证据。详见[42](42-r5-shutdown-implementation-and-qualification.md)，整项未完成。

## S4P App就绪收口（2026-10-26）

S4P已定位provider-only装配与schema11 reader不匹配，仅Desktop启动预检5行修复；Runtime/Host实现保持。正确本机配置的App两次ready/只读历史/正常退出及四库WAL0通过。下一步推进当前r5的S2/S3纵向和S4余项，不再扩Runtime解决已收口的启动问题。详见[43](43-app-readiness-root-cause-and-minimal-fix.md)及s4p-final-review证据。
