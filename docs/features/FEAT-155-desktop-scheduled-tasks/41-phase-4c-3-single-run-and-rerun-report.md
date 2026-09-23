# FEAT-155 · 4C-3 单次执行授权与独立重跑实施报告

2026-09-23。按用户明确授权实施[40方案](40-phase-4c-3-single-run-and-rerun-plan.md)。**代码与真实重跑闭环已完成；原生弹层、暗色与焦点的视觉验收仍未收口，不能宣布4C-3全部通过。** 本轮报告后停止，不进入历史时钟、电源、通知或下一批；FEAT-155整体Must与D4仍未完成。

## 实现与兼容

| 项目 | 实现结果 |
|---|---|
| 最小私有契约 | grant无关的`RerunReview`复用既有历史快照与当前配置摘要；新增单次用途确认封套、`single_run`准入及single_grant/rerun只读回执。Rust/TS、resolved schema、strict validator和27个command同源生成。 |
| SQL25 | 只增加单次grant用途/格式/原run关联，复用原grant的次数与期限；旧记录不回填、旧迁移不改。普通SQL15/Store5保持，明确隔离候选为25/6；无日常库迁移。未知用途版本拒绝执行，历史仍可读。 |
| 授权独立 | 新单次grant不更新计划授权指针，不修改计划状态、下次时间、自动额度或未来槽。enabled/paused/completed均可明确申请一次；deleted、目标失效、忙碌和未释放unknown仍阻挡。 |
| 原生许可 | 用途绑定manual或指定原run的rerun；次数固定1、最长10分钟，并受当前UI context、权限revision、Host nonce、生命周期epoch和计划版本约束。确认、预约、claim、实际POST重验；持久回执和同ID重试不重建当前进程许可。 |
| 执行和恢复 | 复用同一worker、原Coordinator及run/聊天/turn/outbox/额度组合事务。重跑生成新run/请求/操作/轮次并记录original_run_id；有效新rerun不会被历史清理误取消。完整never才取消/退款/释放，attempted只读恢复、不重投；最后一份已占额度可完成原create→turn。 |
| UI | 已开启、暂停、已完成计划可立即运行；执行记录及详情可审阅后独立重跑。展示原/现名称、内容、规则和目标差异、当前状态、Ask与一次许可；未知先查证，同一payload明确重试。结果按新run定位精确对话与轮次。 |

`contract-impact=breaking`，按40方案保守分类：现役私有预览及准入解释改变。公共Contracts/Host wire和固定Runtime不变；同包前后端与SQL25 reader配套使用，不声称旧独立客户端兼容。产品修改仅在Desktop；Host、Contracts、Runtime与本轮起点逐文件摘要一致。固定Runtime SHA-256沿用`bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`，没有替换、伪装或补丁新增。

## 验证证据

[检查索引](evidence/phase-4c-3/checks.json)、[原生UI观察](evidence/phase-4c-3/native-ui.json)、[源码与范围审查](evidence/phase-4c-3/workspace-review.json)、[最终只读账本](evidence/phase-4c-3/ledger-final-read-only.log)。本任务实施后另行反向复核，不冒称独立人工或子代理批准。

| 检查 | 结果与限度 |
|---|---|
| 原生定向 | 最终124项FEAT-155回归全部通过；4C最新17项及未知用途版本1项也通过，均包含在最终回归中。覆盖旧格式/旧聊天重开、三目标组合事务、授权独立、去重、最后一额、并发、失效与恢复。重叠测试不累加计数。 |
| 契约 | 68个实际原生交换、27个命令通过native/strict AJV/TS一致性；生成检查通过。证据来自实际producer输出，没有手写预期payload代替。 |
| 前端 | 最终8文件35项定向检查通过，包含无grant/Host冷态只读重跑预览、completed立即运行、稳定ID、未知回执及原payload重试；lint/类型检查通过。 |
| 静态与构建 | fmt、all-targets clippy `-D warnings`、设计文档构建、canonical packaged App构建通过。真实App使用原Host、固定Runtime、同库worker和Coordinator。 |
| 本机原生流程 | 声明式本机Provider共2次、0真实请求；enabled专属聊天分别完成立即运行与从旧automatic记录独立重跑，结果定位第3轮；原两轮保留。 |
| 真实闭环 | 1次真实文本，HTTP200、native completed，新建不同聊天并准确定位第1轮；自动计划授权及额度独立。正常暂停、退出、重开，无额外请求。 |
| 视觉 | 未通过完整验收，具体未决项见下节；不能用AX能点击、单元测试或4C-2历史截图替代本批弹层视觉检查。 |

初次原生回归122通过、1失败：旧manual测试仍按旧预览中的grant_id解码，随后更新新预览调用并保留SQL25之前候选rerun禁发边界；最新定向通过。最早专属目标合成fixture尚无可信已创建聊天，正确触发busy，随后修正fixture；实际专属目标由组合与本机流程覆盖。最早前端扩展检查5项因fixture缺少新required capability失败，修正后35项通过。失败日志保留，不算作通过。

标准`pnpm test`因既有Contracts tracked changes保护在生成检查阶段阻断，没有进入全量Vitest，未绕过或清除用户改动。全量Rust未执行：历史`sidecar::distinct_test_profile_lifecycles_record_content_free_child_crash_evidence`使用故障可执行脚本，`feat126_secure_storage::symlink_wrong_mode_and_non_temp_roots_fail_closed`包含权限/路径故障，与用户长期条款冲突；采用安全FEAT-155定向测试。旧ChatPage显示断言未作为本批修复范围；不能宣称全仓测试通过。

## 单次额度与真实关联

从既有合成历史run `01a0ca0a-cad7-7153-b65d-12f205b48826` 发起重跑。先经正常UI修改当前名称/纯文本内容，再明确未来自动许可1次（2026-09-24 00:55 Asia/Shanghai，截止01:05），核对原/现差异后确认一次重跑。

- 新run：`01a0cc09-ad69-7aa3-a7aa-2013c3da4587`；原run关联精确，旧历史未覆盖。
- 单次grant：`01a0cc09-ad5e-7ff1-90a5-edfb3ebe0448`，占额1、未退款；turn operation：`01a0cc09-ad69-7aa3-a7aa-2025741f24f3`。
- 新conversation：`01a0cc09-ad6a-7041-bdf5-0e36b511c29c`；local turn：`01a0cc09-ad6a-7041-bdf5-0e5611018757`。
- 自动grant：`01a0cc09-4014-7291-9384-db60f7216b34`；单次事务前后保持同一grant、占额0、plan revision5及同一未来槽。最后人工明确暂停才变为revision6。

[只读不变量比较](evidence/phase-4c-3/checks/ledger-invariants.json)核对本机/真实两个计划的自动指针、额度、下次时间与槽未受单次事务改变；旧run/grant/binding/recovery/outbox事实保持。[Provider台账](evidence/phase-4c-3/provider-ledger.json)从累计9开始，批次硬限始终1，实际1；**累计10/12，剩余2次**。图片、商家及MCP外部调用0。Provider准入时刻`2026-09-23T02:13:01Z`仅是验证台账时间，不伪造为产品历史时钟。

UI已打开精确新聊天，展开可读“4C3 独立重跑验证通过”。Provider未提供可用phase，继续显示“未分类模型消息/显示内容不完整”，没有伪造最终回答或业务成功状态。

两份验收计划均已通过UI明确暂停，最终revision6；[正常重开比较](evidence/phase-4c-3/checks/reopen-comparison.log)确认整个只读输出一致、真实请求仍1、预约0。应用与两个验证服务均正常退出，无强杀、系统时钟变更、故障权限或危险fixture。

## 未收口的视觉项与停止点

**UI-4C3-01尚未解决。** CUA可访问性树能读取手动/重跑确认框全部内容，确认、取消、Escape及后端结果可核对；但多次截图持续显示底层页面、不显示弹层，正常重开、Raise和Window菜单激活后仍如此。暗色切换时截图中shell变暗，卡片仍是浅色且元信息对比不足。当前未得到足够证据区分产品渲染故障和工具捕获异常，不能将它称为纯工具问题。

已请求用户将候选窗口置前确认弹层可见性，报告时尚无答复。最小窗口底层布局可读；本批弹层滚动、亮暗一致性、取消默认焦点及关闭后的焦点返回**未通过视觉验收**。系统外观已恢复原浅色。没有为了通过截图检查更改应用安全边界或扩展到全局主题重构。

后续应先复核此项真实可见性并定位必要的最小修正，然后才能将4C-3标为全部验收通过；这不需要追加模型调用。当前实现与真实执行证据已保存，**停止于4C-3，未自动进入下一批**。普通15/5、候选25/6保持；未提交、推送、部署或迁移日常库。回退先关闭新确认/claim并正常停机，保留SQL25兼容reader、用途关联与历史，不降级写库或删除新表。
