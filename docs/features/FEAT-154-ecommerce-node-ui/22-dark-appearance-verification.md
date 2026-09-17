# FEAT-154 暗色验收与媒体图标修复

> 2026-09-16—17 · **暗色1180×760本轮验收通过，1440×900浅／暗色未执行，完整D4仍未通过。** 当前候选包含2个未提交Coze文件；本轮及21的元仓文档/证据未提交。

## 1. 授权与边界

用户要求“继续执行 406 条件，暗色开始验收”，按继续步骤4–6及开始暗色实测执行。此前暗色延期已被本次授权更新；通过原生系统设置临时切换深色，完成后恢复最初选中的浅色。**系统显示缩放的拒绝仍有效**，只读核对默认1512×982，未切换显示选项。额外原生菜单/删除/撤销复验仍按用户此前决定跳过，不重试该轮卡住的操作。

`contract-impact=none`：本轮只有本地SVG图标着色修复、标准构建及真实UI验收；无公共协议、持久化、跨进程状态、部署接口或业务执行变化。全部30节点仍仅注册、画布展示、属性配置和页面内交互。试运行保持可点击、仅前端提示，无节点接口或业务处理。授权及初始来源见[范围记录](evidence/dark-verification/authorization-and-scope.json)、[工作区基线](evidence/dark-verification/workspace-before.json)。

## 2. 实测发现与修复

**DARK-01：17–22图片与视频节点图标在暗色背景上接近黑色。** 原目录使用`icon-image-overlay.svg`，其中`currentColor`作为外部`img`加载时不会继承宿主前景色，目录、卡片及侧栏缺少对应的主题渲染映射。

在`themed-node-icon.tsx`增加原SVG导入和现有`text`类前景色映射，共2行。复用已存在的本地图标组件及主题变量，保留原SVG图形和图标URL；非localAdapter渲染路径不变。15个受保护主题文件不改写。修复原因、文件及原SVG摘要见[问题记录](evidence/dark-verification/finding-and-fix.json)。

| 真实证据 | 内容 |
|---|---|
| [01 修复前暗色目录](evidence/dark-verification/01-catalog-before-fix.jpg) | b17候选媒体图标接近黑色；保留失败现场 |
| [02 修复后暗色目录](evidence/dark-verification/02-catalog-dark-fixed.jpg) | de585候选6个媒体图标可辨，末项目录焦点与滚动可见 |
| [03 暗色图片表单](evidence/dark-verification/03-image-form-dark.jpg) | 卡片/侧栏图标、双行输入及焦点 |
| [04 暗色对象表单](evidence/dark-verification/04-object-values-dark.jpg) | 最小样本量0、下界0.1/上界0.95、清除按钮焦点 |
| [05 暗色长名称](evidence/dark-verification/05-long-name-dark.jpg) | 24长标题省略、完整描述、输入值及焦点 |
| [06 暗色离开确认](evidence/dark-verification/06-leave-confirm-dark.jpg) | 提示内容及取消/离开入口，无重叠 |
| [07 浅色回归](evidence/dark-verification/07-image-form-light-regression.jpg) | 恢复浅色后原图形、现有青柠主题及配置保留正常 |

浅色颜色沿用用户已有青柠主题；不新增“全页WCAG对比度通过”的结论。

## 3. 标准构建与当前来源

旧App恢复原稿后正常Cmd+Q退出，全部工作流容器通过`make workflow-stop`正常退出0。随后canonical编辑器构建触发现有静态CSP精确字节审阅门禁，未绕过：完整AST核对各类调用身份、表达式、分类上下文与URL字面量来源不变，3个审阅分块变化，2处上下文仅生成哈希不同。更新精确审阅记录后重建通过。原始失败与后续通过均保留。

| 项目 | 当前记录 |
|---|---|
| Coze基础HEAD | `6d5b309519c2c027fee4a37a107f15c56d554645`，含本轮2个未提交文件 |
| 实际source digest | `fed130babaa4fe0264c0774c7dc3c316db4e1e6a046b3f98d8e7e092d34690ba` |
| manifest SHA-256 | `de585dcc9bfa76a599818d167db83588fc32ed4003c40f017b5983082c931f4c` |
| 激活epoch | `c864d4c5-5ac5-42b4-8608-785de7a1b66e` |
| 资产 | 385项，45,568,463字节 |
| Desktop源码HEAD | `4a8a67bec4903624ca98a1098572fa26f3a20849` |
| Desktop二进制SHA-256 | `5f845b416fcd330f9561bd3259bd1488decdfb72c6a5d62856802001d8f11ffb` |
| 实际App进程 | 15168，canonical `pnpm tauri:demo-fast:app` |
| Contracts源 | `db4458fe94572c4df41a114005d54a049bb79b1f`，三消费者锁未改 |

manifest的source_commit为基础HEAD，source_digest绑定实际含修改工作树，**不能称本轮修复已提交**。完整来源见[最终候选](evidence/dark-verification/candidate-final.json)。通过Infra标准登记/build/up和Desktop标准packaged增量构建启动；Coze来源摘要变化，按canonical重新登记镜像，未手改镜像来源记录。

[正常停止](evidence/dark-verification/normal-stop.txt)、[首次构建门禁](evidence/dark-verification/editor-build.txt)、[AST审阅](evidence/dark-verification/csp-comparison.json)、[重建通过](evidence/dark-verification/editor-build-reviewed.txt)、[登记](evidence/dark-verification/editor-register.txt)、[服务构建](evidence/dark-verification/services-build.txt)、[服务启动](evidence/dark-verification/services-up.txt)、[Desktop日志](evidence/dark-verification/desktop-launch.txt)。

## 4. 修复后真实验收范围

同一de585候选，原生窗口实测1180×760，实际完成：

- 30目录连续Tab逐一到达，有名称、无额外停靠；末项自动滚动、Shift+Tab、Esc关闭返回入口、Enter重开/添加。6个媒体图标均清晰；[实际焦点序列](evidence/dark-verification/final-native-observations.json)。
- 17图片节点：多行文字、正反向Tab焦点、来源图片新增行与引用标识`dark-image-ref-A`；平台下拉可见，方向键/Enter选择TikTok Shop，Esc关闭；分组控件、Shift+Tab到关闭按钮并Enter关闭，重开保留多行/引用/平台配置。
- 05选品节点：最小样本量20→0、对象下界0.05→0.1，上界0.95保持；清除按钮焦点、长表单滚动、只读输出标签与说明。自然到期后正常重连，数值仍保留，无故障或时钟注入。
- 24长名称：侧栏省略标题并保留完整描述，代表输入`dark-ip-24`；展开导航后工具栏和表单仍可操作。恢复侧栏收起时捕获不含任务列表的截图。
- 暗色历史弹层、Tab/Shift+Tab与Esc关闭、离开取消、恢复确认弹层Esc取消；表单配置保持。未执行历史版本。
- 节点和面板试运行均只显示“暂未接入试运行，当前仅展示节点配置”；无模拟结果。恢复浅色后复验受影响媒体图标，随后显式恢复进入前原稿。

本轮为AC-009最小暗色窗口及图标修复的代表范围；不是全部30表单、634字段逐一人工填写，不把21之前的Must结果拼接为本轮完整D4。额外原生菜单/删除/撤销复验仍跳过。部分原生AX定位/焦点快照短暂不一致，以新读状态与可见画面核实，未将无效点击当作通过。

## 5. 数据、外观和截图收口

整任务和修复后UI的全部非审计事实相等；API资源21/操作130、Coze工作流17/执行36/操作117/节点执行108均保持。修复后UI增加8条正常列表/读取/bootstrap/历史审计；两处试运行窄区间**全部事实含审计完全一致，增量0**。见[数据比较](evidence/dark-verification/persistence-comparison.json)。这是私有事实核对，结合调用链及实测支持纯UI结论，不冒称全流量抓包。

已恢复原名称`FEAT153 原生终验 0913`、Start/Text/End两连线及“已保存”；恢复导航展开、1180×780窗口及原浅色外观。App及六项健康服务保留运行。原生窗口zoom仅测得1512×875，不等于1440×900，也不推定硬件绝对上限。[窗口与外观记录](evidence/dark-verification/window-and-appearance.json)。

本轮7张真实截图（修复前1张、修复后暗色5张、浅色1张），加21的2张共9张。截图来自CUA原生JPEG字节，经临时本地TextEdit纯文本转存、解码后核对字节数/CRC32、SHA-256及像素尺寸，未编辑或重绘；精确捕获时间未由工具提供，归档时间单列。临时TextEdit已正常退出。[截图清单](evidence/dark-verification/screenshot-ledger.json)。历史21之前0张本地导出缺口保留。

## 6. 验收结论与待办

45项正常聚焦、3项静态CSP检查、标准构建与源/消费者检查通过；126条既有类型诊断，新增0。文档严格检查、声明审计、元仓50项测试、源码/保护/证据摘要检查及实际D4门禁结果见[最终检查](evidence/dark-verification/final-checks.json)。

| 项目 | 状态 |
|---|---|
| 暗色1180×760上述代表范围 | PASS |
| 媒体图标暗色修复及浅色回归 | PASS |
| 浅色1440×900 | NOT RUN，显示缩放仍未获允许 |
| 暗色1440×900 | NOT RUN，暗色已获允许，但目标尺寸仍不可达 |
| AC-009 | pending，仅大窗口两种外观待补 |
| 完整D4 | BLOCKED；条件齐备后在同一最终候选完成全部Must fresh run并通过门禁 |
| 本轮提交 | NOT RUN；Coze图标/CSP审阅2文件及元仓记录待提交；21未提交证据保持 |

没有修改显示缩放、排除AC、推定豁免或关闭需求，也没有强杀、权限破坏、攻击fixture、二进制伪装、数据卷删除或推送。
