# FEAT-154 D4 当前环境验收与搜索修复

> 2026-09-16 · **当前环境复验已完成，完整D4未通过。** 同一修复候选的30节点与共用交互通过；AC-009的1440×900及暗色继续NOT RUN。

## 1. 授权、范围与前序结果

用户在[19已提交候选构建与定向回归](19-committed-candidate-regression.md)执行期间明确要求“执行完毕上述任务后，继续执行D4”。19的五步已收口，[最终检查](evidence/committed-candidate-regression/final-checks.json)通过；之后另起D4真实序列，不将历史R2、f608或19定向结果拼作本轮全部Must通过。

本次修复的`contract-impact=none`：仅统一电商目录的本地搜索字符串匹配，不改变公共消息、接口、持久化、执行或部署语义。30节点仍纯UI，试运行可点击且仅前端提示。此前不允许修改系统显示、暗色延期的决定保留；1440×900与暗色仍NOT RUN，AC-009未获得豁免。

## 2. 第一轮实际结果与发现

在19的b90096c候选，正常从工作流列表进入原稿，原生窗口调整为1180×760，仅在页面内设置未保存名称标记。目录30项/5分组、命中/无结果/清空/Esc路径已操作；01–08逐节点添加、打开侧栏和代表字段回显通过，03–08另检查输出区域与滚动，03展开只读输出，08确认零金额及可选布尔“否”。两次自然到期后正常重连，无故障或时钟注入。

进入09时发现：输入目录完整显示名`Listing 综合诊断`得到“暂无相关结果”，短词`综合诊断`可以命中；完整名用明确纯文本粘贴再次复现，字符核对为ASCII空格。根因是原NodeList去掉输入中的空格，而搜索候选名称保留空格。该问题属于AC-001实际缺陷，第一轮不算D4通过。完整记录见[首轮结果](evidence/d4-current-environment/attempt1-result.json)。01–08不是全部30节点验收，不能扩大结论。

原稿已恢复`FEAT153 原生终验 0913`、Start/Text/End及两条连线、“已保存”，没有点击保存或发布。Cmd+Q正常退出App，原launcher会话返回0；`workflow-stop`返回0，记录容器正常停止、保留卷。详情见[修复与正常停止](evidence/d4-current-environment/search-fix-source-review.json)。

## 3. 修复、检查与新候选

- Coze新增本地匹配函数，对候选词与关键词对称处理ASCII空格和大小写；只用于电商静态目录，原远端搜索分支不变。
- 两项回归测试覆盖30个实际显示名、Listing/SEO空格、大小写、描述/目录ID/字段别名及无结果恢复。共45项聚焦检查通过，源码保护检查通过，126项既有类型诊断保持、新增0。
- 首次标准构建在产物静态审阅检查处退出1：三个变更分块的精确校验值需要复审。完整AST调用身份集合及八处变更分块调用上下文保持，仅构建哈希不同；审阅精确字节后第二次canonical构建通过，3项CSP检查通过。没有降低运行时CSP、权限或部署预算。
- Infra按登记→构建→启动完成，六项服务健康。Desktop标准packaged构建启动；仅正常启动增加1条既有principal审计，业务事实全部相同。

| 当前身份 | 实际值 |
|---|---|
| Coze基础提交 | 构建时`144e4c259a5460fed57fc280f2439cbbf9a18539`加4文件；现已提交为`6d5b309519c2c027fee4a37a107f15c56d554645` |
| 源码摘要 | `39000526e47f09e2bbf0403a8a87d940733e1532e695efe5033dff6c5d211fad` |
| 编辑器manifest | `77878acf3629b5555ab74483a8c4018da3f6d862425d80aaba40bd0562dcb308` |
| run_epoch | `21c88100-ca6e-4ebb-a1c6-4d1a2ec37110` |
| Desktop binary SHA-256 | `9130eb7be07f4a4ffb0e54e5511b052c1557fa92406ed70ea7d36f555526a742` |
| App进程 | `47333`；canonical launcher会话`39209`保留运行 |

[当前候选与各仓](evidence/d4-current-environment/attempt2-candidate.json)、[聚焦检查](evidence/d4-current-environment/search-fix-focused.txt)、[静态审阅](evidence/d4-current-environment/search-fix-csp-comparison.json)、[构建](evidence/d4-current-environment/search-fix-editor-build-reviewed.txt)、[启动比较](evidence/d4-current-environment/search-fix-startup-comparison.json)。候选在提交前从父提交加精确4文件构建；4文件现已形成[本地提交](evidence/d4-current-environment/search-fix-local-commit.json)。没有重写原manifest或冒称提交后重建；构建与新提交的内容对应由精确文件摘要核对。

## 4. 验收边界

首次选择新App时曾因Mac锁定暂停；用户随后已解锁，第6节记录同一候选的续验结果。锁屏不再是当前阻塞。真实截图只有原生工具内显示，本地导出0张，保留证据缺口；不以静态预览替代。

用户不允许修改系统显示，暗色延期；1440×900与暗色仍NOT RUN，AC-009未获豁免。即使当前浅色1180×760序列全部通过，也不能把完整D4标PASS。Coze修复已本地提交；元仓证据随本次收口提交，未推送。App和服务保留运行。

## 5. 收口检查与门禁执行

[当前文档/来源/证据检查](evidence/d4-current-environment/progress-checks.json)通过。首次实际执行D4文档门禁时发现历史检查清单仍用路径字符串，缺少门禁要求的逐项仓库、命令、退出码及状态；已按真实命令收据补成结构化记录，历史链接另行保留。该修正只补齐检查记录，不把锁屏阻塞、AC-001复验或AC-009改为通过。首份输出[保留](evidence/d4-current-environment/d4-gate-at-lock.txt)，修正后的实际门禁结果见[当前D4检查](evidence/d4-current-environment/d4-gate-current.txt)。

## 6. 同一修复候选的实际验收结果

[全量30节点矩阵](evidence/d4-current-environment/attempt2-node-matrix.json)：完整名称搜索、逐节点添加/打开侧栏、代表字段填写、关闭重开保留、滚动/展开只读输出通过。没有把634行来源核对冒称634字段均人工输入。07/11/17/19/23的AX截断通过实际截图与滚动核对。

[共用交互最终结果](evidence/d4-current-environment/attempt2-shared-results.json)：

- 05双实例、对象默认值隔离、多行内容、零值及小数保留；1.2.3错误原文保留，修正0.15恢复。
- 删除取消、引用来源移除提示、Ctrl+Z/Ctrl+Shift+Z及再次撤销通过。A配置恢复；另按实际A指标观测→B待确认候选方向完成删除B/重连/撤销/引用重新有效的闭环。
- 历史弹层打开关闭保留A内容及引用，没有执行历史版本。节点和面板试运行均只显示前端提示；[窄窗口比较](evidence/d4-current-environment/final-trial-comparison.json)所有私有事实相等，审计增量0。
- 15可选布尔未选择→否→清除恢复；Tab、Shift+Tab、Enter清除及可见焦点通过。26三个提交模式展示，选择PUBLISH后条件说明明确仅填写配置、不执行发布；取消离开与自然重连后值保留。
- 返回工作流确认后继续编辑保留页面；恢复原稿确认的继续配置路径保留节点。最终明确恢复移除全部临时电商节点，原Start/Text/End及两条连线恢复，进入设计前的未保存名称保留；仅撤回测试名称后回到“FEAT153 原生终验 0913”“已保存”、保存禁用。未点击保存/发布。最终原生截图确认无残留弹层，窗口恢复1180×780、导航展开。

原生菜单/AX定位曾间歇未生效，重新读取完整AX并使用暴露的Raise操作后继续完成；不据自动失败判定产品缺陷。补验时目录尚未关闭导致额外添加一份16测试实例，最终恢复已一并移除；未保存或执行。未成功的拖动尝试不计作当前候选新增拖动通过，历史手动成功证据单列。

## 7. 数据、证据与交付结论

[整轮只读比较](evidence/d4-current-environment/final-persistence-comparison.json)确认原图、版本、操作、执行等全部非审计事实相等；正常读取、历史与重连产生的审计单独计数。六项服务健康，manifest、epoch和Desktop二进制仍为第3节同一候选。原稿恢复后App/服务保留运行。

[截图清单](evidence/d4-current-environment/final-screenshot-ledger.json)记录原生工具内实际观察场景，本地导出0张；该离线图像复核缺口保留。当前浅色1180×760共用复验完成，AC-009的1440×900和暗色按用户决定继续NOT RUN，完整D4不能关闭。

Coze搜索修复本地提交为`6d5b309519c2c027fee4a37a107f15c56d554645`，4文件与修复构建/45聚焦测试/3 CSP测试对应。元仓需求和19/20两轮证据由包含本节的提交归档；可用`git log -1 --format=%H -- docs/features/FEAT-154-ecommerce-node-ui/20-d4-current-environment.md`解析实际元仓提交。无push、tag、生产部署或系统外观/显示修改。

## 8. 最终门禁与用户后续指示

用户随后明确要求先跳过原生菜单受阻的验收。本轮不再追加该菜单的重复操作；该指示之前已经实际观察到的删除/撤销/引用恢复结果保留，不把后续跳过记作新增通过。界面恢复和其余复验已在该指示前完成。

[最终D4门禁](evidence/d4-current-environment/d4-final-current-environment.txt)实际退出1：AC-009仍pending，因此feature仍in_progress、verification为BLOCKED且没有完整验收时间。当前真实smoke和代表性普通失败恢复已PASS，未为了过门禁改写剩余AC。元仓lint、50项测试、Shell语法、严格文档与声明检查通过；最终来源/保护/证据核对见[收口检查](evidence/d4-current-environment/final-checks.json)。

暂存区`git diff --cached --check`返回2，仅归档日志保留的末尾空格/末尾空行；逐项与文件归属见[日志格式审阅](evidence/d4-current-environment/staged-log-whitespace-review.json)。未改写原始输出，不冒称零告警；源码及需求文档没有此类例外。
