# 工作流节点面板独立调整

> 2026-09-17 · **四项实现与本地UI回归完成，未提交。** **本轮四项不属于 FEAT-154 需求包。**

## 范围与来源

用户明确要求实现目录拖入、稍加深“添加节点”底色、每个节点独立图标、字体与字号适配现有主题；随后要求复用 `yijie-coze` 内 Coze 现有交互机制。四项完成后再继续 FEAT-154 收口，不把四项加入其需求或 AC。

`contract-impact=none`：改动只在同一编辑器进程内的目录拖放与展示，复用原节点创建、身份生成及页面草稿隔离。跨进程消息、公共协议、持久化/重放、API/业务逻辑及部署语义均不变；没有新增依赖或原生命令。[工作区基线](evidence/workspace-before.json)、[授权](evidence/authorization.json)。

开始时7仓HEAD保持前次记录；Coze已有暗色图标及CSP审阅2个未提交文件，元仓已有21/22验收记录及状态更新。本轮保留这些成果；没有自动提交或推送。

## 实现

- **目录拖放**：首先修复Coze HTML5拖动源DOM被Tooltip条件切换替换及collector副作用，保留该修复；508f61候选实际拖入仍未创建，未记通过。最终本地目录改接仓内Coze/Flowgram `PlaygroundDrag` 鼠标跟踪，仍用 `WorkflowEditService.addNode → WorkflowCustomDragService.dropCard → LocalWorkflowDocument` 创建、定位和保护原稿。适配层只增加6px点击阈值、目录拖影、画布落点和取消/只读检查；非本地目录继续原HTML5链路。没有另建坐标引擎、图节点插入方法或后端调用。
- **独立图标**：为30节点分别选择30个 Lucide 图形，静态导出自项目现用 `@lucide/vue` 1.27.0，保留完整许可证、来源与SVG摘要；目录、卡片及侧栏共用目录定义和主题渲染。没有引入Vue运行时或新的依赖。[来源表](evidence/icon-provenance.json)。
- **字体/字号**：本地入口的独立CSS覆盖目录中写死的字体，使用系统无衬线及中文回退；节点/搜索14px、分组13px，沿用主题文字色。
- **按钮底色**：“添加节点”品牌色透明度由0.12适度增加至0.24，悬停0.30、按下0.36。修改限制在本地入口新样式，已有FEAT-153主题文件保持原字节。

## 验证与交付

聚焦草稿/注册21项通过；新增DOM、生命周期、权限及图标4项、Coze鼠标适配5项通过。测试初次加载路径错误已修正，原失败日志保留。治理lint和源保持检查通过。当前候选586e23d3：用户真实手动拖入成功；随后鼠标点击新增独立实例、分别填写A/B并切换保留、正常重连、原生键盘移动、30目录逐项Tab及Shift+Tab/Enter/Esc通过。浅/暗色目录、卡片和侧栏字体/图标及按钮状态检查通过。试运行前后全部事实含审计完全相等。8张真实JPEG已归档并逐张记录校验值。自动工具拖动未能确认，取消/越界拖放与失焦以正常单元测试补充，不冒称这些分支全部真实手工操作通过。

本轮正常退出：发现页面配置与前次原稿不同后，用户明确授权“直接退出，不保留”；通过 App Cmd+Q 正常退出，再执行标准 `make workflow-stop`，原数据卷保留。[正常停止](evidence/normal-stop.txt)。

## FEAT-154 收口边界

四项完成后继续FEAT-154最终验收。用户在本轮明确授权临时修改显示缩放，此前拒绝已更新；须记录原1512×982/浅色设置并在整个任务结束后恢复。FEAT-154须在同一最终候选完成全部Must及四种主题/尺寸组合，不能将较小窗口换算为目标尺寸或伪造D4。四项自身仍不加入FEAT-154需求或AC。

### 原生操作限制的处理

首候选启动后曾出现后台窗口中的空白/过期截图：Web Inspector只读检查确认Start/Text/End及两条连线已实际渲染，未发现对应运行错误。通过原生Window菜单“易界 AI”（makeKeyAndOrderFront）恢复主窗口前台，关闭并重开目录后布局正常。用户也明确回复已将App放在前台。仅修复HTML5源生命周期后的实际拖入未添加节点，故继续接入现有Coze鼠标拖动机制，不把该轮记为通过。

## 本轮结果与来源

- [当前候选](evidence/mouse-candidate.json)：manifest `586e23d360480e758921366a318d980f01d06aa3d4f917366cbc1af7a5d145e2`，App PID36779，原生1180×760；标准构建/来源锁/CSP通过，126条继承类型诊断，新增0。
- [真实观察](evidence/native-observations.json)、[截图清单](evidence/screenshot-ledger.json)：8张原生JPEG原字节，01是HTML5旧尝试，其余为当前Coze鼠标候选。源文件/截图没有编辑重绘。
- [浅色目录](evidence/04-light-catalog-top.jpg)、[暗色目录](evidence/06-dark-catalog-top.jpg)、[浅色独立实例](evidence/03-light-independent-instances.jpg)、[暗色表单](evidence/08-dark-node-form.jpg)。
- [数据相等性](evidence/persistence-comparison.json)、[试运行窄区间](evidence/trial-comparison.json)。用户原页面按其明确“直接退出，不保留”授权丢弃；本轮测试后已恢复原Start/Text/End及两连线、原名称和“已保存”。外观和窗口的最终恢复随随后D4连续工作完成。
- 全部改动仅在Coze；元仓为独立说明与证据。Contracts/API/Desktop/Infra/Host源码不改，消费者锁不变。已有15个主题保护文件原字节不变。`themed-node-icon.tsx`与CSP审阅文件包含前序待提交的FEAT-154改动，本轮增量及前序提交归属需分别审阅；没有提交/推送。

## 连续任务最终恢复

随后FEAT-154在同一候选完成最终本地验收，见[23](../../features/FEAT-154-ecommerce-node-ui/23-final-d4-qualification.md)。已恢复原稿、默认1512×982、浅色及1180×780。四项仍独立归属；本轮源码与记录未提交、未推送。
