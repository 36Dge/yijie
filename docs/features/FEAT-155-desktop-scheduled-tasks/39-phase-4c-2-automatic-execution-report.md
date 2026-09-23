# FEAT-155 · 4C-2 有限授权、自动触发与暂停闭环实施报告

2026-09-23。按用户明确授权完成[38方案](38-phase-4c-2-automatic-execution-plan.md)的本批范围，**报告后停止**。暂停计划可单独确认有限自动授权，正常退出重开后由原生执行链安排未来任务，并从执行记录定位到原聊天轮次；耗尽或到期不再开启后续运行。未进入独立重跑、完整历史时钟、电源、通知或完整 D4。

## 实现与兼容边界

| 项目 | 本批结果 |
|---|---|
| 私有契约 | source-first 更新 Desktop 私有 IPC，启用封套复用共享 `GrantConfirmation`，增加 `expected_next_at`；新增 enable 原请求观测及 `automatic_consent` 事实。Rust/TS、resolved schema、strict validator 同源生成，确认使用原生执行权限。 |
| 最小 SQL24 | 仅追加可空 `automatic_consent_version`，当前原生确认写 1；旧记录 NULL，不回填，未知版本可读但禁发。不改 SQL21 及旧迁移。普通 SQL15/Store5 保持，明确隔离候选为 SQL24/Store6。 |
| 启用事务 | 原生重算下次时刻并核对已审阅值，截止必须晚于它；revision、有限 grant、未来槽、原回执及新确认标记同事务写入。幂等区分旧/新摘要，旧请求查证或重放不能续额、补标、清除暂停或复活计划。 |
| 分流准入 | manual 保持4C-1一次/10分钟和当前行动许可；automatic 使用持久有限授权、当前 native 权威与本进程连续性；rerun 在入口、claim、实际POST继续拒绝。修正实际发送处额外的手动 Host nonce 检查，使其只约束手动来源，自动仍通过原 Host/epoch/资源/授权校验。 |
| 组合与收尾 | 复用原槽→run→聊天→outbox→额度事务；最后一份已预约额度允许完成原 create→turn，不能重复扣额。手动失效清理不再误取消自动。完整 never 才取消/退款/释放；已尝试操作仅观察，不重投。 |
| 原生重开 | 启动区分有效未来自动意图与待收尾运行；先本地清理和有界时钟恢复，再使用同一 worker、Host、application、唯一 Coordinator。旧历史恢复失败不阻断其他事实和时钟推进；各运行仍由原准入约束。管理只读不启动 Host，没有页面调度 timer 或第二执行器。 |
| 后台边界 | 后台启动不顺带发送普通未发送队列，也不驱动无关附件确认/删除任务；显式原聊天绑定才恢复前台路径。耗尽、过期或未知历史仍可恢复收尾，不因此给旧运行补发送资格。 |
| UI | 显示当前内容、目标、Ask、时区、下次时刻、有限次数和绝对截止。默认1次及下次时间+10分钟；默认焦点取消。回执未知保留原请求，只读查证，明确重试仍使用同一ID/原payload。额度/旧确认等有效暂停原因可见；明确暂停保留在途事实。 |

`contract-impact=breaking` 保守审查，承接38方案对旧候选实际执行资格的收紧。产品修改仅在 Desktop，元仓保存记录。Host、Contracts、固定 Runtime 的源码与本轮开始时一致；没有新增公共 wire、产品依赖、Runtime 补丁或服务。固定 Runtime 二进制 SHA-256 仍为 `bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`。

## 验证结果

[检查索引](evidence/phase-4c-2/checks.json)、[实际 UI 记录](evidence/phase-4c-2/native-ui.json)、[最终只读账本](evidence/phase-4c-2/ledger-final-read-only.log)、[源码与范围审查](evidence/phase-4c-2/workspace-review.json)。本任务在实现后另行复核源码与范围，没有冒称独立人工或代理批准。

| 层次 | 结果 |
|---|---|
| 原生定向 | 117项 FEAT-155 回归通过；最后修正及新增检查后12项4C-1/4C-2检查通过，二者有重叠，不相加。覆盖四频率/DST、有界计算、三目标、共享占用、去重、最后一额、暂停竞态、发送时窗、生命周期恢复及旧格式读取。 |
| 私有契约 | 52个实际原生交换、26个命令通过 native/strict AJV/TS conformance；同源生成检查通过。SQL23→24、旧 NULL/未知标记、旧聊天与回执、候选正常重开均有定向证据。 |
| 前端 | 9文件42项定向检查通过，最后UI修正后5项自动确认检查通过（重叠）。最终 lint/类型检查通过。取消、稳定请求、未知查证、原payload重试、确认冲突和scope变化都有检查。 |
| 构建与静态 | Rust fmt、all-targets clippy `-D warnings`、设计文档构建、canonical packaged App 构建通过；多次正常启动使用同一固定 Runtime 和原 Host。 |
| 普通 Ask 资格 | 固定 Runtime＋真实 Host adapter＋声明式本机 Provider 完成 start/turn、正常停止、resume/turn；2次本机请求、0付费。策略仍为 `on-request / user / workspaceWrite / networkAccess=false`，请求及流重试均为0。 |
| 原生 UI | 亮暗主题、1180×760最小外框、取消默认焦点、Escape及焦点返回、键盘确认、明确暂停和正常重开已核对；恢复原浅色外观。 |

标准 `pnpm test` 已尝试，因既有 Contracts checkout 的 tracked changes 在生成检查阶段失败，未进入全量 Vitest；没有修改锁、清除用户改动或将其报告通过。旧 ChatPage 三项显示断言沿用33/35/37的历史基线，本轮不声称重新全量核验。全量 Rust 测试未执行：例如 `chat/sidecar.rs::distinct_test_profile_lifecycles_record_content_free_child_crash_evidence` 使用伪造退出可执行脚本制造异常，`feat126_secure_storage.rs::symlink_wrong_mode_and_non_temp_roots_fail_closed` 制造权限/路径故障，与用户长期安全条款冲突。本轮采用安全的定向测试、声明式本机服务与正常平台流程，不能据此宣称全仓测试通过。

## 实际自动闭环与费用

先在真实 App、Host、固定 Runtime 上运行本机声明式 Provider，确认原生路径后再使用一次真实文本请求。两个计划均由 UI 手动保存为暂停，再单独有限确认；均在计划时刻前正常退出重开。没有修改系统时钟、睡眠唤醒设置或用手动准备替代重开的原生启动。

| 证据 | 本机原生闭环 | 真实 Provider 闭环 |
|---|---|---|
| 目标 | 专属聊天 | 每次新建聊天 |
| 计划时刻 | 2026-09-23 00:43 Asia/Shanghai | 2026-09-23 00:55 Asia/Shanghai |
| 授权 | 1次，截止00:53 | 1次，截止01:05；约00:47确认，00:49前重开 |
| 返回 | 声明式合成文本；0真实调用 | HTTP200，原生 completed；“4C2 自动执行验证通过” |
| 调度结果 | 1 automatic run、1次扣额、两条原outbox各attempt1 | 同左；到点时应用停留设置页，管理页面未挂载 |
| 后续 | budget hold阻止未来；精确对话可读 | budget hold阻止未来；详情明确“自动触发”，打开精确第1轮 |

真实关联：plan `01a0ca03-f2d1-7dd0-a2ea-7122e07552b1` → run `01a0ca0a-cad7-7153-b65d-12f205b48826` → grant `01a0ca04-36b6-78c2-a9bb-fc0456fabdbb` → turn operation `01a0ca0a-cad7-7153-b65d-130a76985dba` → conversation `01a0ca0a-cad8-72d3-8f56-378c55a5e680` / local turn `01a0ca0a-cad8-72d3-8f56-37a62a56d327`。Provider 台账准入时刻为 `2026-09-22T16:55:00Z`，不是推造的产品历史执行时钟。

[付费台账](evidence/phase-4c-2/provider-ledger.json)从累计8开始，本批硬上限始终1，实际1次且成功；**当前累计9/12，剩余3次**。图片、商家及MCP外部调用均0。没有清零台账、扩大限额或直连绕过计数。

最终只读 SQLCipher 核对：本批2个 automatic run均completed，历史4个manual run不变；每条相关 outbox attempt=1，所有预约释放，reservation=0；每份本批grant占额1且未退款。检查预算有效暂停后，对两份验收计划分别明确暂停，均 revision=3；再次正常退出重开，状态、run、grant和outbox计数不变，无额外Provider请求。最后正常退出应用及计数服务。只读工具使用隔离候选、read-only连接与query_only，不访问或迁移日常库。

## 审查、限制和停止

- 反向复核了旧 NULL/未知 consent、旧回执重放、到期与最后一额、manual清理误伤、普通队列后台漏发、create→turn前再次核权、unknown预约释放及原生启动与管理查询的边界，未发现本批剩余阻断。
- 验证中修复了前端严格预览fixture缺字段、发送处混用手动Host许可、确认后旧暂停提示残留及重复打开时取消焦点问题；修正后重新进行对应检查和实际流程。早期失败日志没有当作通过证据。
- 真实 Provider 缺可用 phase，仍保留“未分类模型消息”及“显示内容不完整”，展开可读真实回复；没有伪造最终回答类型。完整执行时钟、业务成功评估与完整立即执行/独立重跑不在本批完成范围。
- 未制造真实审批、强杀、系统睡眠/时钟故障、危险fixture或权限破坏；审批、忙碌、到期及竞态由合成组合证据覆盖。中途屏幕锁定后仅请求用户解锁，没有尝试绕过系统保护。
- 回退先关闭新确认/claim并正常停止，保留SQL24/Store6兼容读取与历史，不降级写库、删除新列或用旧副本覆盖现状。未提交、推送、部署、签名、公证或发布。

4C-2已收口，FEAT-155整体继续 active，所有 Must 的整体fresh验收和D4仍未完成。**本轮到此停止，不自动推进下一批。**
