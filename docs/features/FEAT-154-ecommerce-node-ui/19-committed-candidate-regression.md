# FEAT-154 已提交版本构建、激活与定向回归

> 2026-09-16 · **本轮五步已执行；定向回归通过，完整D4仍未完成。** 截图导出缺口已如实登记。

## 1. 范围与当前候选

用户授权执行原稿保护/正常停止、Coze标准构建与登记、服务及Desktop启动、当前外观1180×760定向回归、候选与证据更新。`contract-impact=none`：本轮未修改业务仓源码、公共协议或持久化/部署语义，只构建并激活[18](18-local-commit-baseline.md)的已提交基线。整个FEAT-154仍只注册30节点、展示画布和页面配置；试运行可点击，仅前端提示，无节点接口调用、业务处理或模拟结果。

| 身份 | 实际值 |
|---|---|
| Coze提交 | `144e4c259a5460fed57fc280f2439cbbf9a18539` |
| Coze源码摘要 | `3b1e71a727d8179238bf85cdef1fca85da05fbd14f912b7597983bdf08f28d37` |
| Contracts源提交 | `db4458fe94572c4df41a114005d54a049bb79b1f`；三个消费者精确固定 |
| 编辑器manifest SHA-256 | `b90096c02c9dd6b332344eafc1e817fa717db7f764e245bcc70c19df6ae7a06c` |
| 编辑器资产 | 385项，45,568,238字节 |
| 新激活epoch | `84966cf7-bf7d-479d-a1e5-5abf81717be7` |
| Desktop提交 | `4a8a67bec4903624ca98a1098572fa26f3a20849` |
| Desktop可执行文件SHA-256 | `fd52d1b413ac108fdf6482e573cabb2575b9446ede4438a29c07c259eba2488f` |
| 当前资格 | 浅色1180×760定向回归PASS；AC-009 pending、D4 NOT RUN |

完整源/消费者锁、镜像ID和启动来源见[候选](evidence/committed-candidate-regression/candidate.json)、[激活与服务状态](evidence/committed-candidate-regression/ui-after-runtime.json)、[Desktop构建与尺寸](evidence/committed-candidate-regression/desktop-activation.json)。新候选替代此前运行的f608构建；旧R2/f608证据作为历史保留，不改名冒充本轮资格。

## 2. 正常停止、构建与启动

- 开始时七仓HEAD/分支/远端与本地提交收据一致、工作区干净，15个主题保护文件相同。旧App正常重连后显示原三节点及“已保存”；私有只读核对无未解释在途状态。[基线](evidence/committed-candidate-regression/workspace-before.json)、[停止前状态](evidence/committed-candidate-regression/pre-stop-runtime.json)。
- 通过原生UI发送Cmd+Q后旧App及启动器PID消失。退出后的AX读取超时，原exec句柄不可用，因此不推定App数值退出码。Infra `make workflow-stop`退出0，所有记录容器退出0、无pending stop/child，数据卷保留。[正常停止](evidence/committed-candidate-regression/normal-stop-observation.json)。
- Coze canonical build成功：126条既有类型诊断保持、新增0；现有安装凭据与精确依赖检查通过，未新增依赖或改写源码。385项资产通过既有CSP审阅检查，无需新增审核声明；3项CSP聚焦检查通过。[构建完整输出](evidence/committed-candidate-regression/editor-build.txt)、[CSP](evidence/committed-candidate-regression/editor-csp-check.txt)。
- Infra按`workflow-editor → workflow-build → workflow-up`登记、构建并启动，三个消费者锁和canonical bundle检查均通过；六项主服务健康、宿主就绪。Desktop通过正常packaged入口标准构建后启动，初始1180×780；原生拖动底边至1180×760并由应用诊断确认。[登记](evidence/committed-candidate-regression/editor-register.txt)、[服务构建](evidence/committed-candidate-regression/service-build.txt)、[启动](evidence/committed-candidate-regression/service-up.txt)、[Desktop日志快照](evidence/committed-candidate-regression/desktop-launch.txt)。
- 启动前后所有非审计业务事实一致；仅增加既有EnsurePrincipal的正常审计1条。没有重放节点、改写业务状态或做数据副本还原。[启动比较](evidence/committed-candidate-regression/startup-persistence-comparison.json)。

## 3. 真实界面回归结果

| 项目 | 实际结果 |
|---|---|
| 目录与键盘添加 | 原面板30中文节点/5分组完整；命中、无结果、更换关键词恢复；Tab焦点可见、Enter添加通过 |
| 05复杂表单 | 数组行、合成多行说明、对象默认值、下界0.1；小数1.2.3错误保留并可修正为0.15；侧栏长表单可滚动 |
| 独立实例/切换 | 05-A与05-B独立；第二实例初始列表为空；切回原实例仍是A和原多行/类目内容；关开侧栏保留 |
| 15可选布尔 | 初始未选择→明确否→清除回未选择；条件分组展开与代表内容填写通过；输出为只读定义 |
| 自然到期与重连 | 三次自然到期，正常重连保留名称、设计及已填字段；最后一次仍保留撤销恢复的05-B，未注入故障或改时钟 |
| 试运行 | 节点按钮和面板按钮可点击，均提示“暂未接入试运行，当前仅展示节点配置。”；无结果，前后全部私有事实和审计完全相等 |
| 删除/撤销 | 取消删除保留；确认删除05-B后，聚焦画布并Ctrl+Z恢复原实例及B值；未将未聚焦画布时无效果的尝试记为通过 |
| 离开/恢复 | 返回触发页面保护，继续编辑保留；Esc取消恢复保留；明确恢复原稿保留进入设计前未保存名称，再只撤回测试名回到“已保存” |

[逐项观察](evidence/committed-candidate-regression/ui-observations.json)记录实际值及限制。整轮UI前后非审计事实一致；正常bootstrap/read因三次重连增加9条审计，试运行两次点击的审计增量为0。[UI比较](evidence/committed-candidate-regression/ui-persistence-comparison.json)、[试运行比较](evidence/committed-candidate-regression/trial-comparison.json)。

本轮核对30目录，实际填写05/15代表表单及两个05实例；截图快捷键尝试中还临时添加了01，最终一并恢复。没有在新候选重做全部30表单、634字段人工输入、引用失效全路径、Redo或30项完整键盘遍历；这些范围不冒称本轮通过，原R2/f608历史证据仍按其版本保留。

## 4. 截图与恢复现场

真实截图已由原生工具显示，包括目录焦点、复杂表单、到期后字段保留及原稿恢复。**本地图片导出0张**：系统快捷键未生成文件，直接打开系统Screenshot.app的工具读取超时；没有改截图偏好或显示设置。详见[截图登记](evidence/committed-candidate-regression/screenshot-ledger.json)。审阅者可核对文字、原生尺寸、来源与数据证据，但本包仍不足以独立重查这些画面的历史视觉效果；不使用D0示意或虚构图片路径替代。

结束时四个临时电商实例全部移除，原Start/Text/End、两条连线、原名称与“已保存”恢复；主导航恢复展开，窗口恢复1180×780，新App和六项服务保留运行。系统外观与显示空间不变。原稿和旧用户主题未被覆盖；本轮文档/证据未另行提交或推送。

## 5. 资格结论

本轮已完成用户授权的构建、激活、定向回归及证据更新；源码实现完成。1440×900继续NOT RUN，暗色按用户决定延期，历史/本轮截图导出缺口保留。**AC-009仍pending，完整D4仍NOT RUN**；本轮不是全部Must的一次fresh D4。

后续只有在允许的目标尺寸与暗色验收条件齐备后，才安排同一候选的完整Must真实验收。无需为本轮通过重复开发节点接口或业务逻辑。文档、来源、保护文件与最终检查见[收口检查](evidence/committed-candidate-regression/final-checks.json)。
