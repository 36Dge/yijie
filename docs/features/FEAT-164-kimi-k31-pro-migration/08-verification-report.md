# FEAT-164 实际验证记录

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S4专家/媒体/辅助续办）：专家pin已按Skills595c927不可变同内容来源修复；Hostcac2d4d、Desktop56f5284、Connectors1f15726已仅本地固化。四组合source、37专家版本安装/解析/重开及专家/媒体/原生辅助调用安全离线验证通过；S2/S3/S4当前源回归通过。完整TCONF-164-04、App/平台/G2V/G3/final仍未完成，真实模型新增0，旧账本/预占保留。最新见[28](28-s4-expert-media-auxiliary.md)及feature.yaml；下方段落保留各阶段历史范围。

> 当前（2026-10-25，S4）：Contracts eddc64f → Host9ffcb6f → Desktop704cfdb/e408047已仅本地固化全调用面接线；安全子集7/4/4/4/5、S2和S3当前源回归通过。完整TCONF-164-04、专家资源/媒体、辅助动态调用、App/平台/G3/final仍未完成；真实模型新增0，旧账本/预占保留。最新见[27](27-s4-call-surface-wiring.md)及feature.yaml。

> 当前（2026-10-25，S3）：Contracts2dd214d / Desktop4d04597已本地固化计划退役、SQL41和授权保护；TCONF-164-03五项、70前端及当前源S2复验通过。App/UI/平台与完整G3仍NOT RUN，真实模型新增0，旧账本/预占保留。最新见[26](26-s3-plan-retirement.md)及feature.yaml；下面旧阶段结论按原来源保留。

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

## 源候选阶段结论（2026-10-24 历史）

Owner已确认方案并授权实施。G0/G1/G2 pass，G2A及后续Gate/slices pending，整体产品未完成。当前完成的是未激活源契约和独立Runtime候选；Host/Desktop、数据库迁移、实际模型/工具调用、应用切换和三项final E2E均未执行。

## 本次源候选验证

所有结果来自2026-10-24本机实际执行，不继承其它Feature通过。代码版本仍为工作树候选，不能冒充不可变commit。

| 检查 | 真实结果 | 证据 |
|---|---|---|
| 模型v2生成同步、Node契约回归、Rust往返 | PASS；12项Node（含3项保留v1）+2项Rust | [最终回执](evidence/candidate-contract-fixed-results.json)、[日志](evidence/candidate-contract-fixed-01.log) |
| v2 OpenAPI离线bundle Redocly | PASS | [日志](evidence/candidate-contract-fixed-02.log) |
| Contracts `pnpm lint` | PASS；API警告保留，29个JSON Schema、buf、TS、Go静态检查 | [日志](evidence/candidate-contract-fixed-03.log) |
| 新Go包编译和TS类型检查 | PASS；Go无测试文件，只记编译 | [回执](evidence/candidate-contract-fixed-results.json) |
| 独立Runtime来源投影check | PASS；实际binary、manifest、269 schema、patch摘要匹配 | [回执](evidence/candidate-contract-checks.json)、[日志](evidence/candidate-contract-check-02.log) |
| 7个基线离线breaking | PASS；完整比较各baseline已有OpenAPI、Protobuf、AsyncAPI、JSON Schema | [结果](evidence/contracts-breaking-offline-results.json) |
| Runtime canonical构建 | PASS；4项保留SSE、2项sources、3项FEAT-164测试；clippy；release构建；269 schema与保留web-sources候选相同；stdio initialize/initialized及正常EOF退出 | [完整构建日志](evidence/runtime-candidate-build.log) |
| Runtime `make lint`、安全脚本定向测试 | PASS；11项来源兼容、3项正常退出逻辑、2项patch清单 | [回执](evidence/runtime-focused-results.json) |
| Runtime原始上游源码核验 | PASS，canonical subtree保持固定上游原样 | [日志](evidence/runtime-upstream-check.log) |
| 旧input-only/web-sources binary与0001—0006 | PASS，摘要仍匹配保留manifest和HEAD | [保留证据](evidence/runtime-preservation.json) |
| 最终Feature strict、G2、claims | PASS；仅确认当前包与已批准G2，不授予G2A/G2V | [回执](evidence/implementation-governance-fixed-results.json) |
| 工作区与来源保留 | 12仓HEAD保持；9个未修改仓库tracked diff/status相同，8个原产品源码锚点摘要相同 | [工作区](evidence/implementation-workspace-review.json)、[锚点](evidence/preserved-source-anchors.json) |

候选binary SHA-256：`bfb116b7bd79d11ffd593a0bf1b4be681f3081d6705a018a4a69665984e1ebc8`；schema tree：`d8c3265d8923ef4437203c0a2ded954549b4abc0c5079ecd6bcdf7c6da72f11e`。真实来源仍须由后续明确授权的提交固化。

## 失败、修复与未执行项

- 初始严格schema检查发现约束缺少类型/字段声明，已在源修正；原始工具输出保留在会话，未将失败计为通过。
- API原始canonical引用不能由网络取得，离线生成补齐本仓引用及discriminator具名组件；bundle及引用回归通过。
- 二次实现审计发现旧成功回执被投影成v2的风险，已增加原版本SelectionResultSnapshot，直接引用v1/v2权威验证；旧result不加availability、不改schema_version，当前Selection独立查询。
- 补目录一致性时重复加入已存在的activation_required；Rust/Go编译失败已保留在[candidate-contract-checks](evidence/candidate-contract-checks.json)。修复源枚举，并让generator提前拒绝重复值/符号碰撞；重新生成后的最终检查通过，没有手改SDK。
- 原breaking批次有一次baseline拼写错误（exit128）；已按支持清单使用正确完整SHA。另3个baseline因scheduled canonical URL网络解析失败（exit102），原日志和[结果](evidence/contracts-breaking-results.json)保留。独立离线比较的RCA、差异与Owner审查要求见14；不把原入口记成PASS。
- Runtime `make test`在既有`build-input-only.sh`非可执行检查处停止（exit2），该文件HEAD本身为100644，未修改权限。已单独运行安全相关测试和上游核验，不能称全量`make test`通过。见[失败日志](evidence/runtime-fork-tests.log)。
- 新增失败台账时首次文档校验因证据引用不是要求的08锚点而失败；已补真实原失败日志锚点，最终strict/G2/claims通过。原[失败回执](evidence/implementation-governance-results.json)保留，未放宽checker。
- 全量Contracts generate/test未运行：旧生成/测试入口包含本次禁止的攻击fixture路径，且可能重写已有多族工作树生成物。本轮用独立family canonical generate及普通契约测试；完整旧suite覆盖缺口保持，不以限定测试替代全仓通过。
- 日常App/Host/Desktop尚未接入；三表/Host迁移、worker退休准入、计划领域事务、TCONF-164-01—04、G2V和final core/visual/teardown均NOT RUN，不能证明用户端可用。
- 真实模型/业务调用、图片、账户资格、余额及性能质量均NOT RUN，预算为0；长期禁止项未执行。无强杀、权限破坏、攻击载荷、可执行替身或已发布binary覆盖。

## 前轮文档证据（历史）

前轮只做审计落盘时的strict、claims、50项元仓治理测试、文档链接及12仓基线仍保留在evidence；其时“实施未授权/Gate全pending”是历史状态。当前授权以feature.yaml和13为准。文档检查不等于模型、数据或App验收；FEAT-163仍独立FAIL/in_progress。

<a id="E164-RAW-BASELINE-1"></a>
<!-- evidence: E164-RAW-BASELINE-1 -->

原入口失败 1：raw-baseline-35e0949c95d7a59ca5480715c225766dcc822056，2026-10-24T15:37:42.513045+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-35e0949c.log)。

<a id="E164-RAW-BASELINE-2"></a>
<!-- evidence: E164-RAW-BASELINE-2 -->

原入口失败 2：raw-baseline-54be9314dce5319b049dc0a236800fd1a1fdd7a1，2026-10-24T15:37:44.172197+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-54be9314.log)。

<a id="E164-RAW-BASELINE-3"></a>
<!-- evidence: E164-RAW-BASELINE-3 -->

原入口失败 3：raw-baseline-bedf4159b0fa22e24efe6c295f8b0d4845df56b7，2026-10-24T15:37:45.649259+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-bedf4159.log)。

<a id="E164-OFFLINE-RCA"></a>
<!-- evidence: E164-OFFLINE-RCA -->

Owner当前已明确接受候选与离线比较结论；按此授权单次运行bedf4159完整离线基线比较，exit0，原失败不删除。[实际复核日志](evidence/accepted-offline-baseline-recheck.log)。Runtime本地提交57753db451b29a49315ddcb6449ca146171c4de7、Contracts本地提交b0060c8bc4fb924cec14d98b193c32c69482b7b7，双consumer pin已从对应Git对象同步并校验；Go新包仅编译通过，不算行为测试。


<a id="E164-R2-HARNESS-POSITIVE"></a>
<!-- evidence: E164-R2-HARNESS-POSITIVE -->

历史r2本机正控：[实际观测](evidence/g2v-r2-harness-positive.json)、[固定来源](evidence/g2v-r2-provenance.json)。只覆盖当时来源的本机合成路径。

<a id="E164-R2-HARNESS-CONTROLS"></a>
<!-- evidence: E164-R2-HARNESS-CONTROLS -->

历史r2普通四类判定、正常超时和清理：[控制日志](evidence/g2v-r2-harness-controls.log)。未做故障注入或强杀。

<a id="E164-R2-HARNESS-VERDICT"></a>
<!-- evidence: E164-R2-HARNESS-VERDICT -->

历史r2本机无正文判定：[回执](evidence/g2v-r2-harness-verdict.json)。不授予真实G2V。

<a id="E164-UI-OBSERVER-RCA"></a>
<!-- evidence: E164-UI-OBSERVER-RCA -->

追加RCA：原[UI观察事件](evidence/g2v-r1-ui-observer-incident.json)共三次等价观察超时。原始登记07:51与后续10:28记录是记载时间，不能冒充每次发生时间；第三次精确时间未保留，前两次逐事件时间亦未知。原结果DIAGNOSIS_REQUIRED保持。用户正常退出后亲自完成同一候选的合成正控，证明不能仅凭控制器超时认定产品失败。此后将资格工作树置于可观察的正常路径并执行项目标准canonical重建，实际CUA绑定、发送、保存/重开和退出通过，见r2正控。当前可观察性已恢复；唯一底层OS原因未证实，不再机械重复隐藏路径尝试。禁止强杀/替换程序/权限破坏的边界保持；本轮只在标准可见canonical路径继续。

<a id="E164-R1-REAL-FAIL"></a>
<!-- evidence: E164-R1-REAL-FAIL -->

历史唯一真实失败：[原观测](evidence/g2v-real-attempt-01.json)、[旧预算逐字快照](evidence/g2v-real-budget-ledger-before-30.json)、[400审计](19-responses-400-audit.md)。HTTP400/无usage，14.188544元未知预占保留，不改成成功或零费用。


<a id="E164-30-HARNESS-POSITIVE"></a>
<!-- evidence: E164-30-HARNESS-POSITIVE -->

当前40908c7 canonical本机正控PASS：[实际观测](evidence/g2v-30-harness-positive.json)、[固定来源](evidence/g2v-30-provenance.json)。同一合成答复保存/重开保持，fixture共1请求、外部0；App两次及fixture正常退出0，18083/18086释放。

<a id="E164-30-HARNESS-CONTROLS"></a>
<!-- evidence: E164-30-HARNESS-CONTROLS -->

当前固定Desktop来源的四类判定、正常超时/cleanup及真实G2V组合控制：[7项判定](evidence/g2v-30-pinned-verdict-controls.log)、[15项预算控制](evidence/g2v-30-pinned-budget-controls.log)、[命令退出码](evidence/g2v-30-pinned-tests.json)。普通状态和协作取消，不强杀或攻击注入。

<a id="E164-30-HARNESS-VERDICT"></a>
<!-- evidence: E164-30-HARNESS-VERDICT -->

本机Harness判定：[无正文回执](evidence/g2v-30-harness-verdict.json)。真实模型成功还需新oracle与真实UI/账本组合。

<a id="E164-30-REAL-G2V"></a>
<!-- evidence: E164-30-REAL-G2V -->

本次真实续验当前NOT RUN。批准累计30元且只新增1次模型HTTP；授权映射见[封闭授权](evidence/g2v-30-authorization.json)，原账本及预占快照保留。执行后在此追加真实结果，不覆盖原r1失败。


### E164-30-REAL-G2V 追加实际结果

2026-10-25 11:00:34（应用界面时间）发送唯一新增真实回合。HTTP200，response.model为kimi-k3.1-pro，max；唯一response.completed/status=completed，完整流，实际回答42。输入10450、输出55 tokens，无原生搜索/图片。当前计量费上界0.139590元，加旧14.188544元未知预占共14.328134元；不是供应商精确账单。额度次数已耗尽，正常退出后账本halted=true/stopped_normally，重复应用同一授权不会补额或改写账本。

实际[UI/清理观测](evidence/g2v-30-real-observation.json)、[组合判定PASS](evidence/g2v-30-real-verdict.json)、[真实答复](evidence/g2v-30-real-answer.ax.txt)、[重开历史](evidence/g2v-30-real-history.ax.txt)、[截图](evidence/g2v-30-real-answer.png)、[当前账本](evidence/g2v-real-budget-ledger.json)、[授权不能补额](evidence/g2v-30-consumed-resume-check.json)。两次App及计量器均正常退出0，端口释放，没有新增补发。

本次仅通过预算受限的文本纵向可行性；不证明原始默认请求、图片、工具、搜索、S1—S4或三个final。后续仍先落实S1活动身份与退休准入/配置，再依次S2历史恢复、S3计划保护、S4全调用面；按每片Contract First/freshness，不放行日常库迁移或发布。未知原HTTP400的唯一根因仍不宣称已证明。


最终strict/G2V、claims和独立Harness校验均PASS，见[检查回执](evidence/g2v-30-final-checks.json)；[结构化复审](evidence/g2v-30-final-review.json)确认旧行/预占、来源及其它需求保留。原r1 Gate证据字段另以[历史快照](evidence/g2v-r1-vertical-evidence-snapshot.json)保留，不被当前PASS覆盖。


<a id="E164-S1-TCONF"></a>
<!-- evidence: E164-S1-TCONF -->

S1 TCONF-164-01已实现，精确命令实际命中10个普通子例PASS：[独立日志](evidence/s1-tconf-164-01.log)。覆盖冻结前身、双文件组合、trust/旧字节保持、重开、未知内容拒绝、显式活动身份、同代回执和精确effort。普通本机状态，不代表真实模型或全部S1 G3通过。源组合见[当前固定来源](evidence/s1-provenance.json)，S1过程见[21](21-s1-implementation.md)。


<a id="E164-S1-LOCAL"></a>
<!-- evidence: E164-S1-LOCAL -->

S1当前不可变来源的安全定向验证通过：[最终六组检查及退出码](evidence/s1-final-tests.json)、[工作区保留审计](evidence/s1-preservation-audit.json)。Host race/准入/标题/API、Frontend 11项、Native暂停及产品Clippy通过，canonical构建通过。完整make lint/全targets Clippy的原有阻塞保留于21，未关闭检查器或更改无关源码。

<a id="E164-S1-BOUNDARY"></a>
<!-- evidence: E164-S1-BOUNDARY -->

当前固定Runtime及Host的普通loopback组通过，最终一组共4个本机Responses；没有外部请求。[最终日志](evidence/s1-final-host.log)包含新Kimi→MiniMax→新Kimi、已知配置前身与暂停Kimi后MiniMax、退役/缺失身份零发送、历史读取和正常关闭；模型目录及Selection使用既有权威v2 validator。此处为真实Runtime本机边界证据，不写成真实模型答复。

<a id="E164-S1-CONTROLS"></a>
<!-- evidence: E164-S1-CONTROLS -->

当前固定Desktop中的4项分类、正常超时/cleanup控制PASS，见[日志](evidence/s1-harness-controls.log)。不代表App当前剩余清理已完成。

<a id="E164-S1-PLATFORM-BLOCK"></a>
<!-- evidence: E164-S1-PLATFORM-BLOCK -->

新Kimi本机App正控[实际AX](evidence/s1-app-kimi-positive.ax.txt)已完成并正常退出0；以同产物暂停配置重开后Mac锁屏，CUA明确要求用户手动解锁。当前剩余验收和清理NOT RUN，见[平台阻塞及活动会话](evidence/s1-ui-platform-block.json)。不强杀、不猜测UI已通过，等待解锁后继续同候选，无真实模型调用。

<a id="E164-S2-FOUNDATION"></a>
<!-- evidence: E164-S2-FOUNDATION -->
## E164-S2-FOUNDATION：Host恢复与兼容存储子集

2026-10-25，Host3c52898/Desktop189019e，Contracts f2819c6/Runtime074417e r2不变。evidence/s2-host-verification.json、s2-desktop-verification.json记录正常定向检查均退出0；真实Runtime联调仅本机合成。v1结果字节语义、v2四恢复阶段、同ID不自动重配、完整身份回执、其他待处理工作门禁、普通关闭重开、7/8/9/10→Store11和旧reader拒绝、SQL15/29/37/38带数据迁移均有测试。失败迭代和修正见s2-iteration-history.json。

这是已通过的工程子集；Native恢复/取消未接通，S2 local/boundary整体与required平台vertical保持NOT RUN，不标TCONF-164-02/G3 PASS。Owner允许延期锁屏相关验收并先推进离线实现，未执行项仍为事实NOT RUN。无新增真实模型HTTP，旧账本预占不变。

<a id="E164-S2-NATIVE"></a>
<!-- evidence: E164-S2-NATIVE -->

Desktop f341636的Native模型恢复工程子集通过：SQL39原数据保持、旧pending无回填、原绑定及未决工作检查、显式恢复/404规则、终态回执后读取当前Selection、正常私有存储重开与迟到结果保护。候选10项/default5项/前端15项与相关lint/build/source checks见[s2-native-rust-verification](evidence/s2-native-rust-verification.json)、[s2-native-ui-verification](evidence/s2-native-ui-verification.json)，审计范围与缺口见[23](23-native-model-recovery.md)。本机HTTP测试不是App平台验收，无真实模型调用；完整S2仍因业务never-sent取消及平台项未通过。


<a id="E164-S2-DELIVERY"></a>
<!-- evidence: E164-S2-DELIVERY -->

Desktop `2a746c1b39bf1f55f6b317ab570bf93af81ad5dc`的派发证明/显式未发送取消工程子集已完成。新增Rust12项+暂停专项1项、前序candidate10/default5、前端22项、fmt/lint/build/产品Clippy及来源检查通过，见[验证记录](evidence/s2-delivery-verification.json)。扩大ChatPage回归94 PASS/1 FAIL/2 skip，唯一失败在f341636基线复现，不声明全套通过。仅普通临时存储及loopback，新增真实模型HTTP0。原消息/profile/payload、账本预占、活动App及原工作区保留；[隔离](evidence/s2-delivery-isolation.json)、[保留审计](evidence/s2-delivery-preservation-audit.json)。完整S2/G3/TCONF-164-02与平台资格仍未通过，下一步及未执行项见[24](24-delivery-proof-and-cancel.md)。


<a id="E164-S2-TCONF"></a>
<!-- evidence: E164-S2-TCONF -->

TCONF-164-02组合验证PASS：Host `57c29ea03e3de39161a7c28080f9388f00cd1735`、Desktop `ddc840f7ed642216bca4b42ab6327d388aa73084`、Contracts f2819c66、Runtime074417e5 r2。最终两源工作树干净，五组25/2/12/10/1个test/subtest事件均退出0且零skip；[完整命令与结果](evidence/s2-conformance-final/result.json)、[真实Native-Host-Runtime日志](evidence/s2-conformance-final/native-host-boundary.log)、[25范围与剩余项](25-s2-conformance-and-native-boundary.md)。正常Host/Native重开、原回执revision2与当前3分离、取消零POST、最终本机模型HTTP1/外部0。该PASS仅时序/存储/headless边界，不等于App平台、完整S2 G3或final。

<a id="E164-S3-LOCAL"></a>
<!-- evidence: E164-S3-LOCAL -->
## S3 本地实现验证

Contracts2dd214d、Desktop4d04597干净资格来源，计划v2/私有IPC、SQL41领域事务与授权保护完成。5项原生精确测试、70前端、9Contracts、8基线比较、3默认原生路径、lint/Clippy/fmt/前端build和两代源生成核验通过。当前S2五组25/2/12/10/1复验PASS，仅1本机合成响应，真实HTTP0。扩大自动计划回归在ddc840f也同点失败，旧全量生成入口偏差及恢复如实记录于26，不能称全量验收通过。证据见[26](26-s3-plan-retirement.md)、[日志哈希](evidence/s3-log-manifest.json)。

<a id="E164-S3-TCONF"></a>
<!-- evidence: E164-S3-TCONF -->
## TCONF-164-03

`node scripts/feat164-s3-conformance.mjs /tmp/feat164-s3-native-final`，5/5 PASS，source_commit=4d04597cbf40e1aea2c67607c9d441f888223d96、dirty=false。每个模块限定exact selector各命中1项，0 ignored；退休前claim/send屏障、领域授权撤销/未来slot、原run/grant/额度不变、重复开库、显式模型保存/独立新grant、绑定pending、暂停Kimi不阻塞MiniMax、SQL38/39/40→41、实际DatabaseWorker首任务之前退休与正常join覆盖。见[结果](evidence/s3-native-final/result.json)。App/WebView、旧隔离库、完整计划Host/Runtime执行/平台和freshness仍NOT RUN，S3整体G3不放行。

当前G2V因新增scheduled-plan-v2/SQL41来源而回到pending；旧真实成功证据完整保留s3-prior-vertical-feasibility.json，不能扩写旧contract_refs冒称新来源资格。S3/source时序PASS不晋升G2V/G3/final。

<a id="E164-S4-OFFLINE"></a>
<!-- evidence: E164-S4-OFFLINE -->

## E164-S4-OFFLINE

2026-10-25，Desktop e408047 / Host9ffcb6f / Contractseddc64f干净来源。`evidence/s4-conformance-final/result.json`记录Host域服务7、固定Runtime4、Native4、Renderer4、候选组合5；均0skip，最终Runtime6次loopback，真实模型HTTP0。`s4-s2-regression-final`和`s4-s3-regression-final`复验通过。202前端回归、TypeScript/ESLint/fmt/Clippy lib、默认Rust check、go vet及Vite构建通过；产物仅资格树`.local/feat164-s4-web-build`，未重建活动App。

`evidence/s4-source-results.json`：ordinary/market来源PASS；experts/media被既有专家manifest/Native pin不一致阻断。source检查不是完整打包资格。完整TCONF-164-04仍NOT RUN：辅助代理/自动审批/压缩动态路径及当前App/Worker/媒体/平台未跑。不得从安全子集PASS推出S4 G3或产品完成。来源、失败诊断、预算和续办见27。


<a id="E164-S4B-OFFLINE"></a>
<!-- evidence: E164-S4B-OFFLINE -->

2026-10-25最终干净来源Desktop56f5284/Hostcac2d4d/Connectors1f15726/Skills595c927，固定真实r2 Runtime：[S4b最终矩阵](evidence/s4b-qualified-final/result.json)四组合source、资源1、专家/媒体3、辅助4、Native资源1均PASS且0skip；37专家版本安装/解析/重开，13次loopback。原生子代理精确completed、Guardian正常批准复制、显式压缩完成。只计安全离线扩展，不授予完整TCONF-164-04/App/平台资格。

同源[S4回归](evidence/s4b-s4-regression-final/result.json)7/4/4/4/5、[S2回归](evidence/s4b-s2-regression-final/result.json)25/2/12/10/1、[S3回归](evidence/s4b-s3-regression-final/result.json)五项通过。资源[两次复现](evidence/s4b-expert-reproduction.json)、[canonical制品来源](evidence/s4b-build-provenance.json)、[保护审计](evidence/s4b-preservation-audit.json)与[完整说明及未执行项](28-s4-expert-media-auxiliary.md)。首次矩阵s4b-conformance-final属于补强child状态断言前来源，最终权威为s4b-qualified-final，不互相冒充。


<a id="E164-S4C-APP"></a>
<!-- evidence: E164-S4C-APP -->

2026-10-25 S4c：详见[29完整审计](29-s4-canonical-app-ui.md)和[子集判定](evidence/s4c-app-verdict.json)。最终Desktopa0a4743、Hostcac2d4d、Contractseddc64f、Runtime074417e5；专家595c927/Connectors1f15726，所有实际App均由canonical来源校验和构建。3个隔离Desktop修复、42项前端/1项暂停回归、fmt/Clippy/构建PASS。暂停历史零HTTP、明确MiniMax正控、正常重开零补发、专家HTML/SVG、亮暗1180×760与清理通过；10次loopback、真实0。失败构建预检、初次错误测试配置、暂停启动失败与红灯回归日志原样保留；最终不伪造无失败历史。

系统外观和窗口尺寸已恢复，App/fixture均正常退出。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final不放行；[治理门禁](evidence/s4c-governance-results.json)和[工作区保留](evidence/s4c-preservation-audit.json)分别验证文档与不覆盖既有改动，不能代替产品全量资格。

## E164-S4D-OFFLINE

<!-- evidence: E164-S4D-OFFLINE -->

见[30](30-s4-loaded-legacy-compaction.md)、[固定来源结果](evidence/s4d-qualified-independent/result.json)和[总判定](evidence/s4d-verdict.json)。Host验证df06a3c，产品Hostcac2d4d/Runtime074417e5不变；独立子集6个Go PASS、14本机HTTP、0skip。全轮71本机合成HTTP，0真实。仅此子集PASS，已知子代理终态失败不被排除结果覆盖。

## E164-S4D-STATUS-1

<!-- evidence: E164-S4D-STATUS-1 -->

[s4d-cutover-02](evidence/s4d-cutover-02-result.json)实际失败：退役旧子模型被拒绝、零旧HTTP，但原生等待返回completed:null。第一轮catalog前置失败另留`s4d-cutover-01`，不算本指纹。

## E164-S4D-STATUS-2

<!-- evidence: E164-S4D-STATUS-2 -->

[s4d-child-diagnostic](evidence/s4d-child-diagnostic-result.json)同指纹失败；[原始日志](evidence/s4d-child-diagnostic.log)记录3次guard错误、同子send_input后的wait结果与thread/read仅userMessage/completed。此后不再重试该失败场景。

## E164-S4D-RCA

<!-- evidence: E164-S4D-RCA -->

[30的根因及建议](30-s4-loaded-legacy-compaction.md)：native agent状态被TurnComplete覆盖，rollout不持久化Error导致历史丢失失败；需要原生权威修复。正式机器台账记录2次实际同指纹FAIL/armed，另采用保守停止策略；没有Owner批准的核心补丁或RCA复验，不标resolved。S4 blocked，完整TCONF-164-04、G3/final未过。
