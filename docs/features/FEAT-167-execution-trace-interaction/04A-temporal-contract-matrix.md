# FEAT-167 时序契约

本文与 `feature.yaml.temporal_contract_matrix` 使用同一组 Scenario、Invariant 和 Test ID。2026-11-04 的复审修复沿用 Native6 / SSE13 / IPC6 / format6，不新增协议或数据库迁移。初次实施中经用户授权的旧数据清理仅为历史事实；本轮明确禁止再次清库，以下恢复与清理均指正常停止运行资源、正常读取现有新格式数据。

## 权威源与职责

Runtime 的 Item、phase、commandActions、审批和 retry 以固定 `yijie-codex@55b4e51049d6f4fc0af4b35f12832357f5e4ea06` 为准；易界投影以 `yijie-contracts@dfd9012954c716d360f702d6be3bdbdef75e0633` 为准。Host 负责安全事实投影，Desktop Native 负责合并、SQLCipher 事务和 IPC，前端只派生阅读模型。项目 Producer、Persistence、Consumer Owner 均为段成威；本地验证不替代正式 Owner 发布批准。

## FLOW-LIVE-001 — 实时事实到阅读视图

顺序为 `producer → persistence → notification → terminal → cleanup`；中间三个阶段会随原生事件重复执行，terminal 表示已持久化并发布的终态在消费端可见，不表示把原生终态接收延后到其他阶段之后。

| 阶段 | 动作与约束 | 异常和降级 |
|---|---|---|
| producer | Runtime 提供 started / delta / completed 和原生 turn 状态；Host 保留身份、phase、retry，产生 SSE13。命令预览与工具标题只投影允许的已有字段。 | 隐藏内容不伪造工具失败；不创建替代 Runtime 的执行或重试状态机。 |
| persistence | NativeDisplayBuffer 按序号及原生身份更新；完成快照替换草稿，已完成快照不被迟到 delta 覆盖；format6 保存到 SQLCipher。 | 已知恢复窗口内去重；真实缺口和身份冲突保留诊断，不承诺任意乱序的通用 exactly-once。 |
| notification | 事务成功后才发布相应 IPC6 revision；前端由事实生成活动行和连续组。 | 没有持久化成功依据时不得对界面宣称已经保存；常规 command_output_pending_final 不再阻断整轮实时资格，未知诊断保持保守。 |
| terminal | 仅原生 turn 终态决定轮次结束；完成、中断、失败保留真实 Item / 计划状态，不能把剩余步骤勾成成功。 | retry 意图不等于完成；退出码缺失不推断执行成功；末尾可读消息保留，原 phase 不改写。 |
| cleanup | 应用正常退出，沿既有流程停止自有服务和释放资源；调试后恢复固定开发入口。 | 无法正常停止时中止该步骤并报告；不强杀、不替换可执行文件、不清库。 |

## FLOW-REPLAY-001 — 当前格式正常重开

顺序为 `persistence → replay → cleanup`。从已保存 format6 读取事实，经 Native 阅读接口和 IPC6 进入相同前端投影；读取不回填未知命令/标题、不改写 phase，不启动新 turn、不执行工具。旧 V4/SSE11 不恢复，非当前格式仍明确拒绝。

冷历史中的 inProgress 仅作为保存事实，不冒充实时活动。前端对旧 format6 已保存的常规输出策略诊断采用修复后的阅读判断，原事实与 view_json 不回写。关闭应用仍使用正常退出流程，数据保留。

## TINV-001 — 跨阶段不变量

适用场景为 FLOW-LIVE-001 和 FLOW-REPLAY-001，对应原实施索引 S1；验证入口为 TCONF-001。

| 不变量 | 验证与边界 |
|---|---|
| 同 ID 更新、最终快照优先、已知传输序号去重 | NativeDisplayBuffer 正常状态序列与跨仓字节联调；不声明任意冲突自动恢复。 |
| commit-before-publish | 复用既有事务保存后发布路径；跨仓入口核验 SSE decoder、NativeDisplayBuffer、SQLCipher 保存和正常重开。 |
| 只有 turn 终态结束轮次 | Host / Native retry、scope、terminal 和计划回归；普通输出等待不毒化整轮诊断，真实缺口不被清除。 |
| 未知 phase 不改写、末尾可读回答保留 | 前端 A06 / A07 与末尾 commentary 阅读候选测试；候选仅影响布局。 |
| 重开不重发 turn，读取不改既有事实 | Native 读取前后比较 view_json 与事实数量；实机原两会话四轮正常重开，Runtime rollout 字节和启动/完成计数不变。 |
| UI 阅读控制不产生执行副作用 | ActivityEntry 引用原 Item；展开仅发 disclosure 事件，不执行、批准或重放；一次调用允许多条活动行。 |
| 正常 cleanup 保留持久数据 | 调试版正常退出、固定开发入口恢复；未执行清库、迁移或故障注入。 |

## TCONF-001 — 可执行时序符合性

在 `yijie-desktop` 运行 `node scripts/check-native-conversation-integration.mjs`。驱动调用实际 Host 序列化代码，消费实际 SSE decoder 和 NativeDisplayBuffer，经 SQLCipher 保存与正常重开，最后加载实际前端投影。最新结果为 PASS：3 次调用生成 4 条展示行，命令动作与工具标题保留，reasoning 原事实不变但不生成普通工具行，常规输出策略不使 turn 失去实时资格。

本轮日志为 [cross-chain.log](evidence/repair/cross-chain.log)，完整证据名与 SHA-256 以 [日志索引](evidence/repair/log-index.json) 为准。补充验证见 [本轮交付记录](10-reaudit-repair-delivery.md)、[26 项矩阵](evidence/repair/acceptance-v2.json)、[数据保护记录](evidence/repair-data-preservation.json)；原实施证据见 [HOST-NATIVE-001](08-verification-report.md#HOST-NATIVE-001)。

没有执行强杀、权限破坏、二进制替换或攻击注入；没有新增真实提供方回合。故障与审批状态通过正常样例和已有桥接回归验证，不冒充新的真实故障恢复运行。正式 G2V harness 资格及 G4–G6 状态仍按 feature.yaml 保留；本次补齐正文引用不改变批准状态。

## 证据失效与复验

Runtime / 契约 pin、Host 投影、持久化与发布顺序、重开语义、终态解释或前端消费行为改变时，重跑相应符合性及读取验证。仅展示文字或索引修正运行文档检查；不能用文档通过替代运行证据。涉及停止应用时始终使用正常退出，不以故障注入获取证据。
