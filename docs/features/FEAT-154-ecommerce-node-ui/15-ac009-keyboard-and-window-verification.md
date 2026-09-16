# FEAT-154 AC-009 尺寸与键盘验收

## 范围与当前状态

用户授权执行基线核对、1180×760键盘/焦点、1440×900补验、实际UI问题修复及证据更新。保持系统外观，暗色继续按用户决定延期。整个FEAT-154仍仅注册30节点并展示画布/配置；试运行保持可点击，仅前端提示，不实现节点接口或业务处理。

本轮`contract-impact=none`：仅本地renderer目录的键盘关闭、焦点显示和Tab顺序，以及验收记录；公共协议、持久化、Runtime及部署语义不变。三处问题已修复，最终候选的浅色1180×760键盘/焦点验收通过。1440×900与用户延期的暗色仍NOT RUN，AC-009及完整D4未关闭。

## 基线与正常启动

七仓来源、未提交文件摘要与15个保护文件已保存。R2编辑器manifest `a9317ebc05750d0837f61439cef67e3f8b4dcb76c68692d6e6e9a69482a5814a`与源码/资产/契约锁检查通过。开始时App与Docker未运行；正常启动已有Docker后，原六项主服务和迁移容器均保留退出0，采用canonical `workflow-up`重新启动原数据集，无需异常恢复。App使用既有canonical packaged入口。

证据：[基线](evidence/ac009-verification/workspace-before.json)、[原容器状态](evidence/delivery-package/command-output/ac009-verification/runtime-before.txt)、[首次激活](evidence/ac009-verification/activated-runtime.json)。

## 发现与局部修复

| 项目 | 实际问题 | 修复与范围 |
|---|---|---|
| F1 目录焦点 | 节点按钮可通过Enter添加，但外侧焦点框被拖拽卡片的`overflow:hidden`裁切 | 对本地`role=button`卡片增加内侧焦点框，沿用现有主题变量 |
| F2 目录Esc | 搜索框可Esc关闭，从节点或目录外层容器按Esc不能关闭 | 在本地目录捕获Esc，保留输入法组合和添加中保护；关闭后返回入口焦点 |
| F3 重复停靠 | Tooltip给外层容器加入Tab停靠点，与内层有名称的节点按钮重复 | 仅本地拖拽卡片外层设`tabIndex=-1`，保留节点按钮、拖拽和提示能力 |

F1/F2首轮修复真实App复验通过后，遍历30目录发现F3并继续修正。最终候选从搜索框连续30次Tab恰好依次到达30个节点按钮，无额外无名称停靠点；焦点框清晰、末项自动滚动可见，反向Tab、Esc返回入口、Enter重新打开与添加均通过。初始按AX称为“滚动容器”的无名称焦点，后经固定依赖源码核对为Tooltip外层，原始证据已补充身份说明。没有改用户主题文件、节点定义、字段状态或业务接口。

证据：[原始复现](evidence/ac009-verification/pre-fix-observations.json)、[首轮修复及F3发现](evidence/ac009-verification/focus-order-followup.json)。

## 尺寸与验收边界

- 最终候选浅色1180×760由原生窗口诊断确认；表单正反向Tab、下拉Enter/方向键/Esc、数组添加、多行输入、长表单滚动、分组Enter展开、侧栏键盘关闭保留、名称/恢复弹层Esc取消均实际通过。
- 本次原生Fill仍为1512×875，未达到1440×900。记录的是实际窗口，不推定硬件绝对上限；不使用宽而矮的窗口替代目标尺寸，不改变系统显示/外观设置。
- 暗色为用户延期，NOT RUN；AC-009和完整D4保持未完成。最终D4仍需条件齐备后一次fresh run覆盖全部Must，不拼接不同时期结果冒称通过。
- 全量R2的30节点逐项添加/代表字段证据保留；本轮只复验受影响的目录键盘与代表表单，不冒称634字段均人工填写。

## 安全与原稿

两次构建前App均正常Cmd+Q退出0，服务正常停止0。最终候选已显式恢复原三节点、两条连线、原名称与“已保存”，窗口恢复1180×780，App与服务保留运行。整轮六组业务事实完全相等；节点和面板内试运行前后全部事实（含审计）相等，审计增量0。最终UI轮次因正常初始化及自然重连增加8条审计记录，不是节点业务调用。[数据比较](evidence/ac009-verification/persistence-comparison.json)。

全程不实施强杀、权限破坏、攻击fixture、二进制伪装或数据卷删除；无Git提交推送。

## 最终候选与检查

- epoch：`8d5a65b9-8656-430d-9554-e6ffd490f253`；manifest：`f608fde5478d47d3db3ee75ea4e14a012025a9436af21e1043439b09d5e43526`；385项产物；标准构建/登记/服务与Desktop启动完成。[激活](evidence/ac009-verification/activated-runtime-final.json)。
- 43项聚焦检查、3项CSP检查、源码保护通过。126条原有类型诊断不变，新增0。[聚焦检查](evidence/delivery-package/command-output/ac009-verification/focused-checks-final.txt)、[构建](evidence/delivery-package/command-output/ac009-verification/editor-build-final.txt)、[CSP检查](evidence/delivery-package/command-output/ac009-verification/csp-checks-final.txt)。
- 两次产物变更均审阅原8处调用点，类别、模块、表达式保持；末次上下文仅构建哈希变化。无网络入口或CSP权限扩大。[最终审阅](evidence/ac009-verification/incremental-csp-review-final.json)。
- 最终真实UI证据包含30目录顺序、05数组/对象、24长标题、焦点截图、自然重连、试运行和恢复。截图在本任务原生工具结果中，JSON列出实际操作与原生尺寸，不伪造图片文件路径。[UI结果](evidence/ac009-verification/final-ui-observations.json)。
- 最终文档、七仓、15保护文件及范围检查见[最终核对](evidence/ac009-verification/final-checks.json)。

本轮可执行的浅色最小窗口检查与问题修复已完成。剩余为1440×900及用户后续安排的暗色矩阵；条件齐备后再执行完整D4。

## 2026-09-16 · 用户不允许调整系统显示缩放

大窗口预检已确认当前候选/源码/契约锁一致、六项服务健康，原稿显示“已保存”；系统仍为1512×982默认显示空间，1800×1169选项可用。请求单独确认后，用户明确回复“不允许”。未修改系统显示或主题设置，停止依赖该调整的1440×900验收，不重复请求同一调整。

保留30节点实现及1180×760浅色键盘验收成果；1440×900为NOT RUN，暗色继续延期。此决定仅拒绝系统设置变更，不等于排除AC-009或批准D4，二者保持未完成。来源：[用户决定](evidence/light-large-verification/owner-display-change-decision.json)。
