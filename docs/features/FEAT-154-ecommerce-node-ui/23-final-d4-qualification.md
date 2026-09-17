# FEAT-154 最终 D4 验收

> 2026-09-17 · **实现与本地真实验收完成。** 当前候选 `586e23d3`；D4门禁PASS，结果见末节。源码及本轮记录尚未提交，无推送。

## 1. 范围与候选

本轮承接用户要求：先完成四项独立节点面板调整，再完成FEAT-154收口。拖入、按钮底色、30个独立图标及字体调整单独记录于[独立交付](../../dev/workflow-node-panel-adjustments-2026-09-17/README.md)，不加入FEAT-154需求或AC。全程保持30节点纯UI；没有节点业务处理、API调用、素材I/O或模拟运行结果。

用户本轮明确授权临时改变显示缩放，此前拒绝已被更新。实际从默认1512×982切换1800×1169，取得原生1440×900；结束恢复默认显示、浅色、1180×780和原导航。[授权](evidence/final-d4-20260917/authorization.json)、[原生尺寸](evidence/final-d4-20260917/window-geometry.json)。

`contract-impact=none`：本轮最终验收没有再修改源码；已有候选的协议、消费者锁、持久化和运行语义保持。D4结论限于demo_fast/local纯UI范围，接口接通不属于通过条件。

| 身份 | 实际值 |
|---|---|
| 编辑器manifest | `586e23d360480e758921366a318d980f01d06aa3d4f917366cbc1af7a5d145e2` |
| Coze基础提交 | `6d5b309519c2c027fee4a37a107f15c56d554645`，包含明确记录的未提交调整 |
| source digest | `c226f744f587b85f01b31362416d2b946a7c9bf17c86e54a3b7944d75ee03392` |
| 运行epoch | `9bb04654-0186-44ba-9467-165fd035bfba` |
| Desktop | PID36779；binary SHA `feb95f72f020e58db1c8d614a4baa81b4d7211cbca5d5310fe5106b041aff9b1` |

标准构建、精确CSP审阅、登记和服务/客户端启动见[候选](../../dev/workflow-node-panel-adjustments-2026-09-17/evidence/mouse-candidate.json)。385资产、126条继承类型诊断、0条新增；最终[编辑器来源检查](evidence/final-d4-20260917/editor-check-final.json)通过。六个主服务健康，无未决停止或恢复，[最终运行状态](evidence/final-d4-20260917/runtime-final.json)。

## 2. 本轮真实操作与 Must 结论

全部操作连续发生在同一App启动、同一工作树产物和epoch中；独立调整回归阶段先完成同类A/B实例及用户手动拖入，再恢复原稿进入全30节点阶段。没有拼接旧候选20/21/22的结果冒称本轮通过。

| AC | 结果 | 本轮证据与实际覆盖 |
|---|---|---|
| AC-001 | PASS | 30个完整名称逐项搜索/添加，匹配结果唯一；错误关键词显示“暂无相关结果”；清空及Esc关闭正常 |
| AC-002 | PASS | 30节点均实际添加、打开侧栏并填写代表字段；同候选A/B实例切换不串值；用户手动拖入成功；键盘删除、撤销和重做通过 |
| AC-003 | PASS | 01–08字段源映射、类型/必填/枚举/建议默认逐项程序核对；实际填写嵌套SKU、市场、金额；整数12.5显示格式提示，改0后提示消失 |
| AC-004 | PASS | 09–30均实际添加和代表字段填写，覆盖文本说明、结构化对象、素材引用；634顶层字段与明示子项由源检查完整核对，不声称手工修改了全部634字段 |
| AC-005 | PASS | 03/08/10/15/17/22/26/30中文字段与分组均实际打开；05列表子项、22配音配置及只读输出滚动；输出只显示定义 |
| AC-006 | PASS | 切换/关闭侧栏及历史后保留；离开选择继续编辑；恢复弹层Esc取消；恢复原稿保留进入前未保存名称，随后改回原名称并显示已保存 |
| AC-007 | PASS | 节点与工具栏试运行均可点击，只显示未接入提示；窄区间所有数据库事实连同审计完全相等；不点击历史中的旧版本实际执行 |
| AC-008 | PASS | 错误搜索、未填写、空列表、普通整数错误修正、自然会话到期正常重连、失效引用和恢复取消均有实际结果；未制造故障 |
| AC-009 | PASS | 浅/暗色1180×760及1440×900实际检查；原生尺寸确认，长表单/目录滚动、可见焦点及Tab/Shift+Tab/Enter/Esc；矩阵见下 |
| AC-010 | PASS | canonical Desktop真实入口；原三节点及两连线保留并恢复；源码/资产/契约锁一致，54项聚焦检查通过 |

[30节点逐项结果及操作事件](evidence/final-d4-20260917/native-observations.json)、[完整字段源检查](evidence/final-d4-20260917/source-fields.txt)、[54项聚焦检查](evidence/final-d4-20260917/focused.txt)。独立实例和手动拖入来源为同候选[真实记录](../../dev/workflow-node-panel-adjustments-2026-09-17/evidence/native-observations.json)，其中拖入由用户明确回复“已出现新节点”，随后实际观察到新节点。自动拖动没有成功，不冒称自动化验证通过。

代表共用交互细节：05新增候选商品子项，标识`D4-CANDIDATE`；通过Down/Enter将指标观测切到页面引用并选择01的`rejected_sources`定义。键盘Delete删除01后显示“引用节点已移除”，Cmd+Z恢复、Cmd+Shift+Z再次移除、Cmd+Z恢复，引用及子项值保持。01的`0`、布尔关闭、清除、空列表分别可区分；08金额`12.50`与折扣`0`保留；22语速`1.25`、15模式`D4-LOCALIZATION`保留。

**限制按事实保留**：额外原生菜单删除取消复验依用户决定跳过；本轮不将该路径记PASS，删除/撤销/重做用正常键盘，取消覆盖目录、历史、恢复和页面离开。取消拖动/越界/失焦分支由正常聚焦单元测试补充，未冒称全部手动触发。强杀、攻击注入和故障制造均NOT RUN/PROHIBITED。以上不扩大既定Must范围，也不改变纯UI边界。

## 3. 四种外观与尺寸

| 外观／逻辑窗口 | 实际检查 | 截图 |
|---|---|---|
| 暗色1180×760 | 全30节点基础操作，复杂列表、引用键盘和离开弹层 | [引用与焦点](evidence/final-d4-20260917/01-dark-small-reference.jpg)、[离开确认](evidence/final-d4-20260917/02-dark-small-leave-confirm.jpg) |
| 暗色1440×900 | 长表单、语速、Tab/Shift+Tab、只读输出、目录及Esc | [配音表单](evidence/final-d4-20260917/03-dark-large-voice-form.jpg)、[只读输出](evidence/final-d4-20260917/04-dark-large-readonly-outputs.jpg)、[目录](evidence/final-d4-20260917/05-dark-large-catalog.jpg) |
| 浅色1440×900 | 金额/零值/布尔、普通格式修正、列表、目录、键盘 | [金额](evidence/final-d4-20260917/06-light-large-price-fields.jpg)、[零和false](evidence/final-d4-20260917/07-light-large-zero-false.jpg)、[目录](evidence/final-d4-20260917/08-light-large-catalog.jpg) |
| 浅色1180×760 | 本地化长表单和可见焦点、试运行弹层、恢复原稿 | [键盘焦点](evidence/final-d4-20260917/09-light-small-localization-keyboard.jpg)、[试运行提示](evidence/final-d4-20260917/10-light-small-trial-notice.jpg) |

本轮12张原生JPEG原字节归档，长度/CRC32/SHA256核对，未编辑或重绘；截图栅格可能缩小，逻辑尺寸以原生日志为准。[截图清单](evidence/final-d4-20260917/screenshot-ledger.json)。加历史21/22的9张，FEAT-154累计21张；四项独立调整的8张单独存放。历史轮次不能导出的缺口仍保留原结论。

## 4. 恢复、数据与交付

在进入30节点设计前，先将原工作流名临时改为`FEAT154 D4 原稿保护 0917`但不保存。恢复原草稿后只有开始/文本处理/结束，临时名称及“有未保存修改”仍在，证明进入前原稿修改未被覆盖：[原稿保护](evidence/final-d4-20260917/11-original-unsaved-draft-preserved.jpg)。随后仅把名称改回`FEAT153 原生终验 0913`，页面恢复“已保存”；没有保存测试配置到后端。[最终现场](evidence/final-d4-20260917/12-original-environment-restored.jpg)。

默认显示1512×982、浅色、1180×780、展开导航均恢复。临时文本编辑正常退出，App及服务正常运行。所有非审计存储事实前后相等；操作结束时审计增加18条；归档后最后一次正常重连再增加3条，总计21条，均为正常读取/历史/重连。试运行窄区间审计1515→1515且所有事实相等：[数据比较](evidence/final-d4-20260917/persistence-comparison.json)。

7仓HEAD不变，Contracts/API/Desktop/Infra/Host源码工作区保持，15个受保护主题文件及4份需求源资料原字节不变。已有Coze及元仓未提交成果保留；本轮不提交、不推送、不公开部署。

## 5. 门禁与关闭

本轮实现和真实Must验收完成后，将`feature.status`置`usable`、AC-009置`pass`、`verification.status`置`PASS`并填写实际验证时间。门禁是对真实证据的结构核验，不替代UI操作，也不是新增人工批准。

- [严格文档检查](evidence/final-d4-20260917/meta-strict-final.json)
- [完成声明审计](evidence/final-d4-20260917/meta-claims-final.json)
- [D4门禁](evidence/final-d4-20260917/d4-gate-final.json)
- [最终完整性与来源核对](evidence/final-d4-20260917/final-checks.json)

FEAT-154在本地纯UI范围收口；业务接口和节点处理继续在范围外。提交属于后续独立操作，当前仍未提交。
