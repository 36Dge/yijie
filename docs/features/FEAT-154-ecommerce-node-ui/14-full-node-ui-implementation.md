# FEAT-154 全量30节点 UI 实施与验收

> 后续AC-009目录键盘/焦点修复与当前候选见[15](15-ac009-keyboard-and-window-verification.md)。本文R2逐节点结果保留为该候选历史证据，完整D4仍未完成。

## 当前范围与状态

用户明确要求执行“补齐剩余27节点，完成全量 UI 集成验证”的五步方案。沿用已确认的D0与第2步骨架，整个FEAT-154仅注册节点、展示画布与属性配置；不实现节点接口调用或业务处理。试运行保持可点击，仅显示前端提示，不发送请求、不产生模拟结果。系统外观保持，暗色实测按用户决定延期，NOT RUN。

本轮增量contract-impact=none：只扩展Coze renderer私有目录、控件、页面内字段状态和定义说明。现有bridge、可持久化三节点图、API/引擎、Runtime与部署接口语义均沿用；此前第2步dirty语义和恢复入口的semantic历史不改写。

30目录／634字段已实现，R2标准构建并激活，43项聚焦检查通过。同一R2候选已逐一添加30节点、打开侧栏并填写代表字段，共用交互通过；用户手动拖入05后，已直接核对新增实例与配置隔离。实现完成，完整D4仍NOT RUN：AC-009尚缺1440×900与用户延期的暗色实测。

## 1. 基线

七仓branch/HEAD/remote、既有未提交文件摘要已保存；15个保护文件与原摘要一致。未提交推送或切换分支。详见[本轮基线](evidence/full-ui-implementation/workspace-before.json)。

全量634顶层字段＝299输入＋64独立配置＋271输出。节点09–30的配置对象保留输入身份，按界面分组展示；嵌套UI槽不创造公共业务字段。

## 2. 具体改动

- 以原始三份Markdown的输入、业务配置、输出小节提取字段来源；不导入处理逻辑、平台分支或业务错误码章节。保留相关小节补充说明和输出结构示例，并明确标为定义。
- `catalog-source.ts`由专用可复现源提取脚本生成。`catalog-labels.ts`记录新增577条中文标签；`catalog-children.ts`按原说明提供嵌套UI小表单；`catalog-additional.ts`记录各节点模式、初值、分组和控件。
- 三个原样板保留在`catalog-samples.ts`，总目录合并为30个稳定ID，继续使用唯一私有UI类型及独立实例工厂。
- 共用控件增加小数原文保留和对象默认值深复制；修正样板专用的列表/布尔默认提示，将条件展开与模式提示改由节点定义提供。
- 发布、审核、媒体、监控等字段只提供配置与只读定义；不增加上传、远程预览、审批提交、媒体处理、业务运行或模拟成功。

## 3. 本次实际环境恢复

开始时易界App未运行，Docker daemon不可用。通过已安装Docker Desktop正常启动后，六个原主容器均保留2026-09-15T17:42:46Z附近的退出255，原迁移容器退出0；退出原因未确认，未归因于本次源码修改。[原始状态](evidence/full-ui-implementation/runtime-before.json)。

复用此前已授权的显式恢复入口，新恢复ID `16bee495-cac3-4d0e-b826-ece27226e608`。四份停止数据保护副本共297,810,980字节；启动原依赖、私有只读状态核对、原应用恢复与canonical正常停止均完成，原数据卷保留。没有强杀、删除卷、改写操作终态或重放业务请求。详见[恢复结果](evidence/full-ui-implementation/recovery-result.json)。保护副本不冒称已测试数据库还原。

## 4. 检查与真实验收

- R2共43项聚焦检查PASS：[日志](evidence/delivery-package/command-output/full-ui-implementation/focused-checks-r2.txt)。覆盖全量目录、每节点双实例、634行原文对应、中文嵌套标签、对象默认值、可选布尔、数值编辑、模式隔离、媒体引用、原三节点草稿与消息桥；原生文档依赖的单元替身已在测试内标注，不能代替真实App。
- R2标准构建PASS：126条既有类型诊断不变，新增0；385项产物。3项CSP检查、原调用点增量审阅通过，没有扩大CSP权限或新增网络入口。[构建](evidence/delivery-package/command-output/full-ui-implementation/editor-build-reviewed-r2.txt)、[CSP审阅](evidence/full-ui-implementation/incremental-csp-review-r2.json)。
- Infra canonical登记、构建、启动及Desktop canonical入口已完成。R2 epoch为`754e5e78-9129-4490-a449-016c5b597ca9`，manifest为`a9317ebc05750d0837f61439cef67e3f8b4dcb76c68692d6e6e9a69482a5814a`。[激活证据](evidence/full-ui-implementation/activated-runtime-r2.json)。
- 30节点实际界面PASS：[逐节点矩阵](evidence/full-ui-implementation/ui-r2-node-matrix.json)。每节点点击添加、侧栏、代表字段填写实际完成；不声称634字段均人工逐项输入。634顶层字段来源及明示子项另由源提取、目录审阅与聚焦检查覆盖。
- 当前浅色1180×760布局及长表单滚动PASS。1440×900为NOT RUN：本次正常窗口调整未达到目标，系统Fill原生测得1512×875；1346×850和1512×875的大窗口观察不替代目标尺寸。窗口最终恢复1180×780。尺寸取自原生诊断，截图缩放尺寸不作为逻辑窗口尺寸。[交互及尺寸证据](evidence/full-ui-implementation/ui-r2-shared-observations.json)。
- 暗色：用户决定延期，NOT RUN；完整D4仍NOT RUN。
- 用户禁止的强杀、权限破坏、攻击fixture与二进制伪装：未执行，不声明这些场景通过。

## R1真实界面发现与R2修正

R1实际打开全量目录，完成05/01/02/03/04/06六节点添加、侧栏填写和自然重连；05小数/对象初值已实测。发现部分嵌套项主标签仍为英文机器键，已补充中文展示，原sourcePhrase和UI槽身份保持。修正后43项聚焦检查通过，并在R2完成同一候选全量复验；R1不冒称全部30节点通过。

修正前已显式恢复原三节点及进入设计前的未保存名称，再仅撤回本次测试名称，界面回到“已保存”；App与服务均正常停止，六组业务事实未变。证据：[R1操作](evidence/full-ui-implementation/ui-r1-observations.json)、[R2检查](evidence/delivery-package/command-output/full-ui-implementation/focused-checks-r2.txt)。

## 5. R2实际共用交互与数据结论

- 04重复实例初始空值，新旧分别保留`ui-r2-04-B`与`ui-r2-04`。用户明确回复05拖入“成功”；随后画布直接观察到“选品机会评估_1”，其候选列表为空，新填`ui-r2-05-drag`不改变原05的`ui-r2-05`。自动拖拽此前未成功不记作产品失败，也不替代此次手动成功证据。
- 05对象初值、小数原文错误提示与修正；04默认false；15未选择→否→清除；26文档三种提交模式和纯配置说明均通过。
- 10组装模式条件提示、仅12的标题引用、模式切换保留通过。取消删除12保留内容，确认删除显示引用节点已移除；Ctrl+Z、Ctrl+Shift+Z、再次Ctrl+Z正确恢复节点、`ui-r2-12`及引用。
- 搜索命中／无结果／清空恢复、历史modal打开关闭、取消页面离开、自然到期后正常重连通过。32个电商实例（30种＋04/05重复实例）及已填内容保留。
- 节点试运行与面板内试运行按钮均可点击，只显示未接入提示。前后三份只读快照的全部事实完全一致，审计增量也为0。整轮UI的六组业务事实不变；初始化、自然重连和显式历史读取带来17条审计记录，与业务操作分开计数。[持久数据比较](evidence/full-ui-implementation/ui-r2-persistence-comparison.json)。
- 明确恢复原稿后，原Start/Text/End和两条连线恢复，进入设计前的未保存名称`FEAT154-ALL30-R2原稿`仍保留；只撤回本轮测试名称，回到`FEAT153 原生终验 0913`和“已保存”。没有点击保存或发布；原图哈希、名称哈希、修订和版本均未改变。

## 6. 交付边界与后续

源码实现及30节点核心真实验收完成；AC-001–008、AC-010通过，AC-009保持pending，完整D4未执行。剩余工作为同一候选补齐1440×900及用户允许后的暗色/完整键盘尺寸矩阵；不增加任何节点接口或业务逻辑。

R2 App与本地服务保持运行，原稿恢复；无Git提交、推送或分支切换。元仓lint、50项测试和Shell语法检查已通过；最终文档声明、链接、保护文件及七仓检查见[最终核对](evidence/full-ui-implementation/final-checks.json)。
