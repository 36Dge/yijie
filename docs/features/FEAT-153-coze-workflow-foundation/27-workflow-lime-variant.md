# 工作流画布模块青柠色阶

2026-09-15，用户要求截图所示工作流画布模块所有青柠稍深、舒适优先，不主动提高饱和度；其他页面不变。`contract-impact=none`：只修改编辑器嵌入文档内的六个颜色原语，不改变组件结构、交互、协议、数据、会话或部署接口。

## 当前色阶：用户指定修订

首轮实际效果确认后，用户认为`#B0DB55`偏暗，明确指定工作流模块改用`#B7F03D`。当前源码采用下表；下文首轮色值、截图和资格记录保留为历史证据，不代表当前候选。

| 状态 | 模块专用色 | RGB |
|---|---|---|
| 默认 | `#B7F03D` | 183, 240, 61 |
| 悬停 | `#B1E83C` | 177, 232, 60 |
| 按下 | `#ABE03C` | 171, 224, 60 |

默认色严格采用用户指定值；悬停和按下分别向既有石墨`#25282B`混合4%、8%，sRGB通道取整。只更新原有iframe局部六个HEX/RGB声明及一行说明注释。PostCSS逐规则对比确认其余声明完全相同，共享44token投影检查通过，原生消费链经过独立只读复核。背景、点阵、淡渐变比例、布局、全局`#C3F35B`及其他页面均保持；`contract-impact=none`理由与首轮一致。[本次源码检查](evidence/workflow-lime-20260915/b7f03d/source-check.json)。

本次观察PID41279打开另一份“FEAT153 青柠轻量验收 0914”（workflow `7685078769316397056`），显示有未保存修改。用户针对这份内容明确选择“放弃这份未保存修改，再退出更新”；已按原生返回确认放弃本地草稿，再Cmd+Q正常退出，并确认进程消失。Infra正常停止返回STOPPED、保留命名卷。

本次标准编辑器build/check、Infra登记/构建/恢复均通过，真实ready为true；标准packaged入口启动新PID48694。manifest SHA256为`b732e7eb505cea4ff5704af8fec99608e2954784818a74f816a21006f3584d6c`，source digest为`396ddeff7705a74ea3584566e7c89e07df663964d7d0ac1c2c4655f3617be9d1`；385项资源摘要与服务入口核对一致，本机凭据未匹配静态资源。[本次激活记录](evidence/workflow-lime-20260915/b7f03d/activation.json)。

真实App浅色1180×780、72%画布缩放核对通过：重开同一已保存流程并显示“已保存”，完整画布和文本侧栏中的图标、引用图标、连线、端口、选中边框与试运行按钮均采用新配色；淡渐变、背景、点阵和白色面板保留。实际返回CSS逐字节匹配本轮产物，包含指定`#B7F03D`。原始截图经嵌入显示ICC在内存转换至sRGB后，主色像素在目标各通道±1取整范围内，背景准确为`#F2F3F5`；截图未修改。证据：[完整画布](evidence/workflow-lime-20260915/b7f03d/canvas.png)、[文本侧栏](evidence/workflow-lime-20260915/b7f03d/text-sidebar.png)、[视觉记录](evidence/workflow-lime-20260915/b7f03d/visual-verification.json)。本次没有保存/运行/发布流程，未声称fresh全主题或完整D4；App与本地栈保持运行，未Git提交/推送。

## 首轮颜色决定与局部范围（历史）

| 状态 | 模块专用色 | RGB |
|---|---|---|
| 默认 | `#B0DB55` | 176, 219, 85 |
| 悬停 | `#AAD353` | 170, 211, 83 |
| 按下 | `#A3CA51` | 163, 202, 81 |

从当前品牌`#C3F35B`向既有石墨`#25282B`分别混合12%、16%、20%，sRGB各通道取整；不是增加饱和度或另换绿色色相。默认色HSV色相约78.95°→79.25°、饱和度62.55%→61.19%、明度95.29%→85.88%。石墨字与默认底色的理论对比约9.25:1，仅为配色计算，不是整页可访问性或实际视觉验收。

只在`yijie-coze/frontend/apps/workflow-local/src/yijie-coze-theme.css`最前加入`html:root, html:root.dark, html:root body`覆盖块，设置brand primary/hover/active的HEX和RGB。显式dark选择器避免生成主题根变量优先级导致遗漏。该CSS只由iframe编辑器入口导入，覆盖本模块的原生图标、连线、端口、选中轮廓、8%标题渐变、按钮、body浮层及交互色阶；不修改共享生成palette或Desktop活跃颜色源，不传播到父页、工作流列表、Chat或其他页面。

模块外Desktop公共重连/历史执行控件保持全局颜色；用户截图内的青柠均来自原生编辑器。错误、成功、警告语义色保持。前轮确认的`#F2F3F5`背景及黑色半透明点阵、节点原生阴影与细边界全部保留。

## 校验与运行状态

静态颜色消费链与iframe导入隔离已独立只读核对；PostCSS解析并对照本轮修改前样式，恰好增加六个原语，其余全部规则不变。44token共享主题投影及diff检查通过，源码摘要见[source-check.json](evidence/workflow-lime-20260915/source-check.json)。未新增镜像测试、依赖、权限或业务调用，未Git提交/推送。

最初观察到PID23462打开`FEAT153 易界主题验收 0914`（workflow `7685061713409867776`），编辑会话已到期并保留未保存草稿。2026-09-15用户针对这份草稿明确选择“放弃未保存修改，再退出更新”。已通过“返回工作流”→“放弃本地内容并返回”→Cmd+Q正常退出，确认进程消失；没有保存这份修改。

随后执行Infra `make workflow-stop`，返回STOPPED并保留命名卷；Coze标准`workflow-editor.mjs build/check`通过，再经Infra `make workflow-editor/workflow-build/workflow-up`登记、构建并恢复，真实ready为true。标准Desktop `run-local-demo-fast.sh --packaged`生成本项目未签名debug App并启动PID33507，没有覆盖其他应用或修改构建门禁。

候选来自Coze HEAD `10faf164d7af194b7697a93cb3c4a6886ddc64b5`加当前19行CSS增量（本次11行色阶与前轮8行背景/点阵）。source digest为`8979a8581c9caf26d3cadbc808ad10df8036f2a0d41ebd53144d479f8da1cfc6`，manifest SHA256为`0c63b9baefb51f21ad1162b6e502718c25d8a64163b0b3aa1f44060b04cebe27`，385个资源共45,316,624字节。TypeScript无新增诊断，126项锁定上游诊断仍保留，不称全量类型清洁。服务入口及实际返回CSS与本轮产物逐字节一致；静态资源未匹配本机工作流凭据。详见[activation.json](evidence/workflow-lime-20260915/activation.json)。

本轮真实App浅色1180×780窗口、70%画布缩放复验通过：正常入口重开上述已保存流程，显示“已保存”；检查完整画布、结束侧栏、文本侧栏，顶部与节点/引用图标、连线、端口、选中轮廓、试运行按钮采用较深青柠，节点与侧栏淡渐变保留。既有键盘焦点是独立状态；鼠标切回普通选中态后没有额外石墨描边。原始窗口截图保留嵌入显示ICC，统计时只在内存转换至sRGB，确认主色`#B0DB55`、背景`#F2F3F5`与白色前景；未修改截图字节。点阵及其缩放逻辑保持前轮声明。

证据：[完整画布](evidence/workflow-lime-20260915/canvas.png)、[结束侧栏](evidence/workflow-lime-20260915/end-sidebar.png)、[文本侧栏](evidence/workflow-lime-20260915/text-sidebar.png)、[视觉与生命周期记录](evidence/workflow-lime-20260915/visual-verification.json)。本次只验配色与激活，没有新建、保存、运行或发布业务流程，不重跑或继承为fresh完整D4，也未宣称暗色全主题与多尺寸复验。App和受控栈保持运行，未Git提交/推送。
