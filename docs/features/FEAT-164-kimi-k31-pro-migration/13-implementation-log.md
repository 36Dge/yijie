# FEAT-164 实施记录

> 当前（2026-10-25，S4f普通App与计划）：Host7927ee7补齐已有v2草案三路由，Desktop277f59e兼容读取原生事实2/3/4；Runtimea28130a r4与Contracts1b357cc保持。同源App验证旧历史、input-only草案、只读恢复零补发、关闭保存、单次执行、取消编辑和正常重开；App模型协议loopback共3次，真实新增0。旧失败请求/事实/账本保留；完整恢复取消、旧模型计划、专家媒体当前组合、平台/G2V/G3/final仍未通过。权威见[32](32-s4-r4-app-plan-acceptance.md)。以下记录保持原来源与时间语义。

> 当前（2026-10-25，方案A原生终态修复）：Runtime r4 a28130a → Contracts1b357cc → Hostb9155a3 → Desktop2fb8989已本地固化。原子代理错误被completed覆盖及冷历史丢失失败已修复；10项核心、269 schema零差异、7项原生/23次本机HTTP证据复核、3辅助/9次与4调用面/6次均通过。新增受管writer标记阻止旧r2候选写入新历史；不改旧历史。全轮50次合成本机HTTP、真实新增0，旧账本/预占保留。App本批仅构建，完整UI/计划/恢复取消/平台/G2V/G3/final仍未通过。最新权威见[31](31-s4-native-terminal-repair.md)及feature.yaml；以下旧阶段保持历史含义。

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

Owner当前消息明确确认方案并要求实施、保留工作树、遵守安全条款及完成后审计验证。记录时间以evidence/implementation-baseline.json为准；不伪造独立Reviewer或发布批准。

## 当前阶段

G0/G1/G2：用户确认方案并允许实施；执行机器门禁后记录结果。G2A/G2V及S1—S4均未通过。先做业务源契约和最小独立Runtime候选，不提前改Host/Desktop日常执行。整体contract-impact=breaking。

## G2设计具体化

采用独立model-selection-v2 schema、chat-models-v2 family 0.2.0 candidate与/v2/model-chat路由；现有v1源及其consumer不变。Known ProfileId包含旧K3及两活动身份，ActiveProfileId仅新Kimi/MiniMax。Selection新增独立availability，unknown仍表示执行结果不确定；旧operation走独立只读receipt，不能以旧SelectRequest再执行。

Runtime保留0001—0006字节，新增0007仅用于新候选：新slug搜索sources与旧slug出站拒绝，正常工具/SSE补丁沿用。独立构建路径，不覆盖旧binary；上游版本、schema、权限不变。该底层拒绝保护辅助调用，但不能代替Host/Native迁移与worker准入。

## 仍需真实证据的边界

G2A需要真实不可变candidate提交/consumer pin和已生成diff评审；当前没有Git授权，不创造commit或假pin。付费真实G2V及终验需本Feature预算；日常库先有兼容回退资格。所有既有未提交变更按implementation-baseline保留。

## 2026-10-24 源候选完成

- 已新增Contracts独立模型v2源、SDK/离线API bundle/来源锁、普通契约回归与离线基线比较工具。
- 已新增Runtime0007、新构建/manifest入口和独立kimi-k31-pro-r1；真实构建及正常stdio退出通过，原上游/0001—0006/旧制品未改。
- 已从实际制品生成独立runtime-kimi-k31-pro投影，未sync Host/Desktop、未改日常入口或用户库。
- 实现后再次审计修复旧v1回执版本、availability一致性、转发错误声明和SDK枚举重复问题；最终限定检查及7基线离线比较通过。
- 真实失败/未执行项均见08；原breaking入口与Runtime make test没有伪记PASS，Owner审阅与不可变提交仍欠缺。下一步入口14，不提前进入S1—S4。

## 2026-10-25 UI延期后S2基础

Owner明确允许需要解锁的步骤延期并继续离线推进。已实施/本地固化Host3f6b609（14文件）与Desktop83f467b（2文件），仅当前需求专属patch；正常测试与Runtime loopback通过。详情及未完成Native/取消/UI项见22。锁屏项NOT RUN，未提高Gate状态，未新增真实调用/推送。

## 2026-10-25 Native模型恢复

按Owner“审计后开始下一步”实现Desktop f341636（20文件）；Host/Contracts/Runtime不变。只本地提交，真实模型0，现App及日常库不触碰。工程子集检查与缺口见23，完整S2/G3仍未通过。

## 2026-10-25 派发证明与未发送取消

Desktop 2a746c1b39bf1f55f6b317ab570bf93af81ad5dc（23文件）已按专属patch本地提交。SQL40不回填旧记录，普通/市场/专家分别记录claim与发送/注册尝试，保留原内容与模型快照，显式取消仅接受完整未发送证明。工程验证、扩大回归的原有失败、未执行平台项及下一步见24。真实模型新增0，无推送。

## 2026-10-25 S2时序与Native/Host边界

Host 57c29ea03e3de39161a7c28080f9388f00cd1735（2个测试文件）与Desktop ddc840f7ed642216bca4b42ab6327d388aa73084（5个测试/来源文件）仅本地固化。TCONF-164-02组合五组通过，普通临时数据与真实Runtime本机响应，正常重开/原回执/当前选择/取消边界验证见25。无新产品行为、无真实模型调用/推送/日常库或活动App修改；完整G3仍待平台项。

## 2026-10-25 S3 计划退役与授权保护

按Owner明确授权完成source-first、本机领域保护及隔离本地提交：Contracts2dd214d→Desktop4d04597。S3五项精确时序与当前S2五组复验通过，真实模型HTTP0；默认自动回归原基线失败和旧生成器误用如实保留。App/平台/G3不晋升。完整实施、验证、未执行与保留审计见26。

## 2026-10-25 S4 专家资源与辅助调用续办

按Owner明确授权完成专家pin审计与同内容不可变来源、候选专家/媒体接线及原生辅助安全离线验证。最新Host cac2d4d、Desktop56f5284、Connectors1f15726，Skills595c927/Contractseddc64f/Runtime074417e5不改。专属pin和slot保留原资源，原dirty同步脚本不混入提交；process provider meter覆盖原生子代理/Guardian/压缩。具体提交、复现、精确矩阵、边界及下一步见[28](28-s4-expert-media-auxiliary.md)。新增真实模型HTTP为0，完整G2V/G3/final仍不放行；旧账本、预占、活动S1 App与原改动保留。

## S4g 旧草案状态续办（2026-10-25）

继续审计后实施只读uncertain投影及说明/防重复提交，Desktop181885b（10文件）。2 Native+1 writer+32前端、canonical App限定验收通过；0模型请求，正常清理。通用generate三次失败/RCA及首次UI绑定时机问题均保留。见33。
