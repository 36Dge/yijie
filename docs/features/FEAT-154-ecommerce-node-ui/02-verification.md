# FEAT-154 需求文档验证

当前统一状态见[16](16-delivery-status-and-evidence.md)，最终候选与验收见[23](23-final-d4-qualification.md)。前序记录均按当时状态保留。

## 1. 范围与当前状态

当前FEAT-154已完成实现与最终本地真实验收：30节点／634顶层字段，AC-001–010通过，feature=usable、verification=PASS，D4证据见[23](23-final-d4-qualification.md)。当前manifest586e23d3，来源绑定含未提交独立UI调整的实际工作树；同一候选完成全30节点、共用交互及浅/暗色1180×760和1440×900。12张新真实截图归档；原稿、默认显示、浅色及1180×780恢复。本轮改动和记录未提交，无推送。四项独立节点面板调整不计入本需求。

## 2. 需求草案首次文档检查（历史）

以下命令于2026-09-15在元仓执行，均退出0；[原始命令输出](evidence/document-checks.json)保存真实结果。

| 检查 | 实际结果 | 证明范围 |
|---|---|---|
| check-feature-package.sh --strict 本需求目录 | PASS | 4个核心文档及schema v3结构、模板标记；未运行D0/D4门禁 |
| validate-feature-package.mjs --audit-claims 本需求目录 | PASS | 无虚构完成状态；pending/NOT RUN保持 |
| pnpm lint | PASS | 11个子仓清单与中央/兄弟仓Contract First规则存在性 |
| pnpm test | PASS，50项 | 元仓文档治理/manifest正常测试；不是30节点产品测试 |
| bash -n scripts/*.sh | PASS | 元仓Shell语法，未执行服务脚本 |
| 来源/字段/链接/工作区检查 | PASS | 4份资料逐字节一致，30节点/68节/634顶层字段，摘录逐字核对，包内链接解析；15个既有文件摘要保持 |
| 独立文档复核 | 无阻断问题 | 17–30字段及00/03/05/feature.yaml范围一致；不是Owner批准 |

详细证据：[内容完整性](evidence/requirements-integrity.json)、[工程源码来源](evidence/code-facts-sources.json)、[前后工作区](evidence/workspace-after.json)。检查时6仓分支/HEAD/远端不变，5个兄弟仓状态不变；元仓只新增FEAT-154目录。

## 3. 首次需求阶段的产品验证（历史，当时全部未执行）

| 项目 | 状态 | 原因及影响 |
|---|---|---|
| UI源码/构建 | NOT RUN | 用户仅落需求；没有30节点实现产物 |
| 正常Desktop启动/30节点fresh UI流程 | NOT RUN | 本次未启停App或服务，产品可用性未验证 |
| 主题/尺寸/键盘及恢复 | NOT RUN | 已定义验收步骤，未作产品实测 |
| 新节点无业务请求、原草稿保护 | NOT RUN | 需未来实现后检查调用链和真实交互 |
| 节点业务处理/模型/API/上传/发布 | NOT RUN / OUT OF SCOPE | PDF明确排除，不能作为通过条件 |
| 强杀、权限故障、binary伪装、攻击fixture | NOT RUN / PROHIBITED | 用户永久禁止；不声称这些场景或全仓通过 |
| Git提交/推送、公开/生产 | NOT RUN | 本次无此工作范围 |

## 4. Must AC（当前结论以23为准）

23在同一当前候选完成全部Must；字段完整性采用源映射检查，实际UI覆盖全30节点及代表复杂控件，详细证据与安全验证限制见23。

| AC | 状态 | 验证对象 |
|---|---|---|
| AC-001 | PASS | 逐项对照 04，清空/命中/无结果搜索与源码复用核对 |
| AC-002 | PASS | 逐节点实际点击；两份同类配置互不影响；拖动/删除/取消正常 |
| AC-003 | PASS | 对照 04 全部字段行，默认值逐项审阅，普通格式错误修正 |
| AC-004 | PASS | 对照 04 全部字段及嵌套描述，覆盖模式、平台展示、列表/对象/媒体引用 |
| AC-005 | PASS | 审阅复杂节点 3/8/10/15/17/22/26/30；输出无伪造结果或状态 |
| AC-006 | PASS | 正常切换、关闭、取消离开/明确放弃；原草稿及历史不被覆盖 |
| AC-007 | PASS | 调用链与正常 UI 请求观测，受限入口无新增请求；既有初始化读请求单独记账 |
| AC-008 | PASS | 正常输入、清空搜索、前端重试和取消；不注入故障或攻击 |
| AC-009 | PASS | 主题/尺寸截图；Tab/Enter/Esc、侧栏滚动、长名称/数组/对象检查 |
| AC-010 | PASS | 最终 diff、正常入口 UI fresh run、聚焦构建检查；禁止项 NOT RUN，外部调用 0 |

## 5. 需求与D0阶段结论（历史）

需求文档结果与真实产品资格分别记录；30节点、634顶层字段行和68小节可追踪。当前D0产品/UX已由用户确认，机器门禁结果见第7节；未实施，D4 NOT RUN，DP不适用。

## 6. 第1步接入方案确认前检查（历史，2026-09-15）

用户已明确确认纯前端退出边界：页面离开确认，关闭应用不保证保留。具体方案见[07](07-integration-design.md)，注册/状态/控件独立复核中发现的恢复顺序、静态端口和dirty模型显式重载问题均已修正，复核无剩余阻断。

| 检查 | 实际结果 | 范围 |
|---|---|---|
| 关键源码审阅与摘要 | 28个文件已记录 | 三仓源码，只读；不是构建/运行 |
| --strict、--audit-claims、git diff --check | PASS | 文档结构/完成声明/已有tracked差异空白检查 |
| pnpm lint / pnpm test / bash -n scripts/*.sh | PASS / 50项PASS / PASS | 本轮元仓正常检查，非产品测试 |
| 静态交互示意 | PASS | 同类实例不串值、false保留、模式初始空值及切换保留、搜索空态/取消离开、浅暗窄幅；非Coze App |
| 6仓Git身份与状态、15个已有文件 | 不变 | 只写本需求文档与示意；主题/原始资料保持 |
| 完整D0 Owner确认 | pending | 具体方案已完成，等待实际确认，不虚构批准 |
| D0机器门禁 | NOT RUN | 收到具体方案确认后才设置product_ux状态并执行 |
| 第2步实现、契约生成、工作流构建、App/服务启停、D4 | NOT RUN | 本轮没有实施这些工作 |

证据：[源与消费者](evidence/step1-design-20260915/source-audit.json)、[元仓检查输出](evidence/step1-design-20260915/meta-checks.json)、[示意检查](evidence/step1-design-20260915/design-preview-checks.json)、[文档与工作区](evidence/step1-design-20260915/document-integrity.json)。静态示意仅辅助审阅，字段完整性以04/09为准；28文件源码兼容结论不等于运行符合性通过。

## 7. D0确认与机器门禁通过（第1步结论）

段成威明确回复“确认这份方案”；对应review-candidate中列出的具体设计及示意摘要已逐项核对一致。实际确认时间见[Owner记录](evidence/step1-design-20260915/d0-owner-confirmation.json)。

随后在元仓执行：

```sh
bash docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-154-ecommerce-node-ui
```

退出0，输出“D0范围与语义门禁通过”；[原始门禁结果及输入摘要](evidence/step1-design-20260915/d0-gate.json)。**D0产品/UX确认及机器门禁均PASS，第1步完成。**第6节pending/NOT RUN为确认前历史，不代表当前状态。

product_ux=PASS，design_checkpoint已确认；feature仍draft表示尚未进入实施，implementation=pending，10项产品Must均pending，contract生成/实施与D4仍NOT RUN。第2步未开始，没有业务代码修改、App/服务启停或Git提交推送。只读复核确认15个已有文件、设计附件和五个兄弟仓状态保持。

## 8. 第2步首次实施检查（历史）

用户已明确授权第2步实施。共用框架及01/10/17共57字段代码已落地：Coze47项聚焦测试、Contracts16项、Desktop23项、元仓50项均通过；canonical类型检查新增诊断0，126条原上游诊断完整保留。15个保护文件与六仓分支HEAD保持。

实际Desktop与D4仍NOT RUN：既有Coze/MySQL容器退出137，唯一一次正常停止检查返回2；没有绕过恢复、更新dist或激活产品。完整结果、测试边界和下一步见[11实施记录](11-step2-implementation.md)。第7节“第2步未开始”仅是当时D0确认阶段的历史状态。

## 9. 恢复与三样板验收收口（历史）

用户已授权五步恢复及样板验收。旧环境恢复已完成，原数据保持并正常退出；新候选实际激活，三个样板核心交互复验通过。用户最新回复“保持系统外观，暗色实测留到后续”，已记录[延期决定及第2步收口](evidence/recovery-execution/dark-theme-deferral-and-step2-closure.json)。第2步完成，暗色真实App验收保持NOT RUN，完整AC-009和D4仍待验收。

第8节的环境阻塞已解决，其NOT RUN为早期记录。当前结果以[13执行记录](13-recovery-and-sample-verification.md)为准；本次仅同步文档，运行时结论引用既有R7证据。整个FEAT-154保持纯UI范围，试运行入口可点击，仅作前端提示，不调用接口。

本次收口的文档结构严格检查、完成声明审计、元仓lint、50项元仓测试及全部元仓Shell脚本语法检查均通过；git diff空白检查退出0（仅覆盖tracked差异）。[实际命令与输出](evidence/recovery-execution/step2-closure-document-checks.json)。这些是文档治理检查，不代表新增产品实测或完整D4通过。

## 10. 全量R2实施与验收（历史）

30节点／634字段源码完成，43项聚焦、3项CSP检查及canonical构建通过，126条原有类型诊断不变、新增0。385项产物按canonical流程登记激活，epoch `754e5e78-9129-4490-a449-016c5b597ca9`。

同一R2候选逐一添加30节点、打开侧栏和填写代表字段；搜索、05手动拖入、04/05实例隔离、模式/引用、删除取消/撤销/重做、自然重连、历史、取消离开与恢复原稿均通过。试运行入口保持可点击，仅前端提示；试运行前后全部存储事实（含审计）相等，整轮六组业务事实不变。原稿已恢复到“已保存”。

当前浅色1180×760实测通过；1440×900尚未达到，本次Fill仅测得1512×875，不能代替目标。暗色由用户明确延期，完整键盘与主题尺寸矩阵待补验。因此AC-009 pending、完整D4 NOT RUN，不关闭全需求。

证据：[14当前完整记录](14-full-node-ui-implementation.md)、[30节点矩阵](evidence/full-ui-implementation/ui-r2-node-matrix.json)、[共用交互](evidence/full-ui-implementation/ui-r2-shared-observations.json)、[数据比较](evidence/full-ui-implementation/ui-r2-persistence-comparison.json)、[最终检查](evidence/full-ui-implementation/final-checks.json)。

## 11. AC-009当时外观补验与修复（历史）

用户明确授权执行尺寸/键盘五步方案。已核对R2来源与15保护文件，原容器正常退出0后按canonical重新启动。真实1180×760检查发现目录焦点裁切、Esc退出和重复Tab停靠三处问题，局部修复后经标准流程重新构建/激活。

最终候选manifest `f608fde5478d47d3db3ee75ea4e14a012025a9436af21e1043439b09d5e43526`，epoch `8d5a65b9-8656-430d-9554-e6ffd490f253`。30次Tab依次到达30个目录按钮，无额外无名称停靠；正反向Tab、Enter/Esc、焦点、数组/对象、长表单滚动、弹层取消、侧栏保留、长标题、自然重连和恢复原稿通过。43项聚焦、3项CSP和标准构建通过，新增类型问题0。试运行前后全部存储事实（含审计）相等，整轮六组业务事实不变。

本轮浅色1180×760范围PASS；1440×900仍未达到（Fill实测1512×875），暗色按用户决定延期。AC-009 pending、完整D4 NOT RUN。没有将R2全量结果与本轮补验拼成最终D4。

证据：[15执行记录](15-ac009-keyboard-and-window-verification.md)、[最终UI](evidence/ac009-verification/final-ui-observations.json)、[数据比较](evidence/ac009-verification/persistence-comparison.json)、[最终检查](evidence/ac009-verification/final-checks.json)。

## 2026-09-16 · 用户不允许调整系统显示缩放

大窗口预检已确认当前候选/源码/契约锁一致、六项服务健康，原稿显示“已保存”；系统仍为1512×982默认显示空间，1800×1169选项可用。请求单独确认后，用户明确回复“不允许”。未修改系统显示或主题设置，停止依赖该调整的1440×900验收，不重复请求同一调整。

保留30节点实现及1180×760浅色键盘验收成果；1440×900为NOT RUN，暗色继续延期。此决定仅拒绝系统设置变更，不等于排除AC-009或批准D4，二者保持未完成。来源：[用户决定](evidence/light-large-verification/owner-display-change-decision.json)。

## 13. 交付证据与提交准备（2026-09-16）

本轮只整理资料，未重做产品运行/界面验收。33份完整日志脱敏归档，38份中间/重复原始日志保留本地；原日志不改写，当前报告和feature.yaml引用已修复。真实App历史截图无法从既有记录导出，明确登记0张可导出文件；3张静态D0图不作真实截图。R2全量与AC-009 final定向回归分开记录。

逐仓文件归属、FEAT-153主题依赖、生成物来源、待授权提交顺序已列于[17](17-cross-repository-commit-plan.md)。[本轮实际检查](evidence/delivery-package/package-checks.json)记录文档、归档、链接及保护结果；它不把AC-009或D4变为通过。未提交推送，未启停服务，未改变系统显示或外观。

## 14. 逐仓本地提交与固定来源（2026-09-16）

用户授权并在中断后要求继续执行。FEAT-153主题、Contracts权威源、API/Coze/Desktop消费者与实现、Infra已分别提交；元仓需求及证据由包含本文的M1提交记录。完整SHA和检查见[18](18-local-commit-baseline.md)。三份consumer lock增加实际Contracts源提交；Coze暂存检查另修正一个末尾LF，无业务行为改变。

本轮通过Contracts16项、Coze43项及既有CSP3项、Desktop23项、恢复9项及生命周期13项检查，相关lint/源与消费者一致性通过。元仓检查及来源资料原文whitespace登记见[evidence/local-commits/meta-final-checks.json](evidence/local-commits/meta-final-checks.json)。未重建/激活产品；历史R2及AC-009的App资格不移植到新源码提交。AC-009 pending、D4 NOT RUN、暗色延期和显示设置拒绝均保持。

## 15. 已提交候选构建激活与定向回归（2026-09-16）

本轮正常停止旧环境后，已从18记录的提交完成Coze标准构建、三消费者锁检查、Infra登记/build/up和Desktop canonical packaged启动。新manifest/epoch见[19](19-committed-candidate-regression.md)。当前浅色1180×760的30目录、05/15代表表单、独立实例、画布焦点撤销、自然重连、试运行提示、取消离开及恢复原稿均通过；不冒称全部30表单、634字段或完整D4重新验证。

试运行前后全部私有事实相等、审计增量0；UI整轮业务事实不变，正常重连增加9条bootstrap/read审计。原三节点与名称已恢复“已保存”，导航展开及1180×780恢复。真实截图在原生工具中显示但未能导出本地文件，0张导出及具体尝试已登记。1440×900与暗色继续NOT RUN，AC-009 pending、D4 NOT RUN保持。全部新证据位于evidence/committed-candidate-regression，最终检查见该目录final-checks.json。

## D4首轮缺陷与修复后复验状态（历史，2026-09-16）

用户追加要求继续D4。19五步收口后开启新序列，01–08代表字段检查通过，09完整名称搜索复现失败；本地匹配空格处理已修复，45聚焦检查/3 CSP检查、标准构建登记及新App启动通过。当前manifest为77878acf…，含4个未提交Coze修复/测试/审阅文件。新候选UI复验因Mac锁定暂停，已请求手动解锁；当前不能声明搜索修复已通过真实UI或D4通过。具体边界、证据和恢复点见[20](20-d4-current-environment.md)。

## 2026-09-16 · 当前环境共用复验与提交收口

上节锁屏暂停属于历史；用户解锁并继续授权剩余工作后，同一77878acf候选的30节点、搜索、双实例、普通格式错误、删除取消、引用失效/撤销/重做、历史、试运行无调用、可选布尔/键盘、发布模式、离开取消和恢复原稿完成。原名称及三节点两连线回到“已保存”，窗口1180×780恢复。全轮非审计事实相等，试运行窄窗口全部事实/审计相等。Coze修复已提交6d5b309519c2c027fee4a37a107f15c56d554645；元仓证据随本节归档，无推送。1440×900与暗色继续NOT RUN，截图本地导出0张，AC-009 pending、完整D4未通过。具体结果和工具限制见[20](20-d4-current-environment.md)。

## 2026-09-16 · 已提交来源对齐与真实截图归档

用户授权对齐6d5b3095编辑器并继续执行。标准显式恢复已独立核实正常退出0，历史137保留；canonical重建、检查、登记、原镜像复用启动和Desktop标准增量构建完成。当前manifest b17f052d…、epoch 4b160abe-3fee-459e-971b-78d39421df0d；385项资产字节与20候选一致，仅manifest来源提交对齐。

本轮浅色1180×760目录、完整名称搜索、05零值/对象/焦点、正常重连、两处试运行提示、离开取消及恢复原稿定向回归通过。全部非审计事实不变；试运行全部事实含审计相等。原稿已保存、导航和1180×780恢复。真实截图原字节归档2张，历史0张缺口保持。窗口正常zoom仅达1512×875；未改系统显示或主题，1440×900与暗色仍NOT RUN，AC-009 pending、D4 BLOCKED。本轮无源码修改、无新提交或推送；新增文档/证据尚未提交。当前候选、截图、检查与剩余条件见[21](21-editor-source-alignment.md)。

## 2026-09-17 · 暗色最小窗口验收与媒体图标修复

用户已要求开始暗色验收，临时切换系统深色后发现17–22媒体图标低对比问题；用既有本地图标组件和主题变量修复，原SVG/图标URL保持。正常停止后完成精确CSP审阅、canonical重建/登记/build/up及Desktop启动；当前de585dcc候选含2个未提交Coze文件，基础HEAD6d5b3095，实际source digest与完整身份见[22](22-dark-appearance-verification.md)。

同一候选的暗色1180×760目录30项键盘、17媒体/多行/下拉/侧栏保留、05零值/对象/输出/重连、24长名称、历史与离开弹层以及试运行提示通过；浅色受影响图标回归通过。原稿、导航、1180×780窗口和原浅色均已恢复，业务事实保持，试运行所有事实含审计相等。本轮7张真实截图归档，含修复前1张、修复后暗色5张、浅色1张；加21共9张。

暗色1180×760本轮范围PASS；浅/暗色1440×900仍NOT RUN（默认显示不改，正常zoom实测1512×875），AC-009 pending、D4 BLOCKED。暗色已经实际验收，不再作为整体“用户延期未执行”；剩余为大窗口两种外观及最终完整Must fresh run。本轮修复及元仓证据未提交，21已有未提交成果保持，无推送。

## 2026-09-17 · 最终D4收口

当前FEAT-154已完成实现与最终本地真实验收：30节点／634顶层字段，AC-001–010通过，feature=usable、verification=PASS，D4证据见[23](23-final-d4-qualification.md)。当前manifest586e23d3，来源绑定含未提交独立UI调整的实际工作树；同一候选完成全30节点、共用交互及浅/暗色1180×760和1440×900。12张新真实截图归档；原稿、默认显示、浅色及1180×780恢复。本轮改动和记录未提交，无推送。四项独立节点面板调整不计入本需求。
