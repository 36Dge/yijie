# 四类 P2 修复的 GUI 实机验证结果

2026-11-17，按 [本轮计划](2026-11-17-p2-gui-plan.md) 执行。沿用原 canonical 入口和已批准的隔离模式，正常构建/启动易界，实际 GUI 操作批准、停止、历史选择和退出。没有伪造审批、结果、Native 事件或 SQL 行。

## 覆盖结论

主要 GUI 路径通过；不能把下表“未触发”的子分支写成全部实机通过。

| 修复类别 | GUI 实际结果 | 覆盖限制 |
| --- | --- | --- |
| 65秒观察窗与连接释放 | 旧轮没有产生原生终态时，其最后一个 Native SSE 订阅在原生 interrupted 记录后 **65012ms** 释放；正常退出也能提前释放。全部7个 Native、7个 legacy 辅助订阅均已释放 | “Native 已结束但产物流继续等待”的反向次序未由当前普通 GUI 场景自然产生；保留前轮双流集成测试证据 |
| 旧轮不随新轮反复更新/整轮读取 | 新轮运行期间旧轮视图 revision 始终为 **9**，新轮由8变为13；晚到 Item 到来时没有额外 native_history/history/thread_read | 这不是高并发压力或所有乱序组合证明 |
| 历史轮次刷新与旧结果隔离 | 审批前明确选择该轮历史项，批准并停止后仍保持该选择；约 **7285ms** 后真实 Item 自动变为 failed，原批准记录随之关联，没有刷新/重开。新轮待批准时没有沿用旧已完成结果，每次都重新出现独立审批卡 | 精确的旧响应乱序竞态沿用本轮定向测试，GUI 只记录正常交互实际观察 |
| 已终态旧 SSE EOF 不干扰其他观察 | 正常退出 GUI 已验证：仍在收尾观察时 ⌘Q，Native 订阅在原生中断后 **469ms** 释放，原退出流程最终 exit0，全部进程/端口清理 | **Host→Native 服务端主动 EOF、同时另一观察仍运行的分支没有直接 GUI 证据**。当前 Host 正常 turn terminal 不关闭该 SSE；本地 MCP HTTP 完成不是这一 EOF 边界。未通过故障注入或篡改 Host 制造触发；此前普通 SSE 集成测试通过仍单独保留 |

## 实际链路与来源

- 入口：`python3 -B scripts/development-client.py start-ui --market-acceptance review-gui-20261117`；启动前易界已关闭，没有强杀或覆盖运行中的二进制。
- 界面明确显示“本地连接器验收 · 独立数据 · review-gui-20261117”，只安装/启用本地验收连接器；工作空间也是本轮独立目录。
- canonical preflight、来源校验、正常构建均通过；Native SHA-256 为 `22e640e7c159f592eea97d97f9ffd161fa555a08211fb2f8b1a0a3fde445ad9e`。初始 Native PID25446、Host PID25463，均为实际启动进程。
- 使用已有普通 loopback MCP/Responses 驱动，模型推理循环、tool_search、Code Mode/原生 wait、Gateway 和 GUI 为真实产品链路；不把本地协议驱动描述为真实模型推理效果。本轮未发起真实模型或真实供应商业务调用。

## 七次真实本地调用

| 轮次 | 操作 | 可核实结果 |
| --- | --- | --- |
| 1 | dual 基线，允许一次 | serial1；文本＋独立JSON，completed |
| 2 | slow，先选明确历史项，允许一次后正常停止 | serial2；原生晚到 failed，所选历史自动刷新；`_meta` 仍属于原轮 |
| 3 | slow，允许一次后停止，立即开始轮4 | serial3；原生没有可读终态，保留 interrupted/结果未确认；观察窗65秒到期释放 |
| 4 | 独立 dual，重新允许一次 | serial4；completed，不复用轮3审批；旧轮视图未随本轮反复写入 |
| 5 | slow 退出准备，允许一次后停止 | serial5；结果在实际退出前自然返回并显示 failed，**不计作收尾中退出覆盖** |
| 6 | 独立 dual，重新允许一次 | serial6；completed |
| 7 | slow，允许一次、停止后立即 ⌘Q | serial7；退出前仍无关联结果。订阅提前释放，SQL决定保留；未把尚未确认的调用标为成功 |

实际普通 MCP `tools/call` 为7次；本地 Responses 协议请求21次。SQL版本实际为47，保留7个独立决定的 requested/acknowledged 共14条事实。

退出前已在 GUI 展示、且有原生终态的5个 Item，逐项读取 Runtime rollout 的 `_meta["yijie.market.call"]`，与 Host correlation 和原 thread/turn/operation/selection/ref/decisionId 一致。轮3和轮7未获得可读取终态，未补写成功或强行关联。

## 观测口径与证据

本轮仅在既有隔离日志里新增 `native_history`、Native/legacy SSE 建立/释放计数：

- `internal/session/native_conversation.go` 在实际原生 history 读取后计数；
- `internal/app/app.go` 在成功订阅后及 cancel 释放后计数；
- `internal/marketbroker/local_acceptance.go` 保持隔离路径/标签门禁、1MiB上限，只新增固定 kind 白名单。

日志仅含时间与类别，不含参数、标识或凭据，不改变公共接口、审批或执行行为。`legacy_sse` 表示非SSE13辅助流，不声称发生了具体产物传输。定向4项相关 Go 用例通过。Desktop 的 Host 构建候选来源由 canonical 流程自动更新；本轮没有修改四类 P2 的功能实现。

证据目录：`yijie-desktop/.local/market-architecture-verification/2026-11-17-p2-gui/`。主要文件：

- `app-start.log`：正常来源检查、构建、启动及退出记录。
- `case-history-refresh.json`、`case-window-and-isolation.json`、`case-normal-exit.json`：实际数据断言结果。
- `native-correlation.json`、`native-final-closed.json`、`final-native-outcomes.json`：原生结果/决定与保留的未知状态。
- `native-turn-times-final.json`、`peer-r1/protocol.jsonl`、隔离 Host 的 `local-market-reads.jsonl`：实际请求/终态/订阅时间。
- `native-overlap-pending.json`、`native-window-ended.json`：旧轮修订号不变的前后快照。
- `baseline.json`、`diagnostic-increment.diff`、`repos-final.json`、`daily-before.json`、`daily-after.json`：改动与数据保护依据。

65012ms和469ms为原生 interrupted 日志时间到匿名订阅释放时间的差，属于实机测量，不冒称直接读取内部单调计时器。旧轮释放的关联依据为当时其他订阅均已结束、仅该收尾订阅尚存，以及完整建立/释放计数。

## 退出、保护与未覆盖

退出时短暂出现同步提示与 `STOP_PENDING: managed process or database still owned`，随后原 ExitOwner 正常等待/重试清理完成，输出 `normal app cleanup complete`，canonical 入口 exit0；没有强杀。普通协议端在 inflight=0 后使用自身 stop 接口退出，exit0。18081/18083/18085全部关闭，无本轮 Native、Host、worker 进程残留。

日常数据库和密钥文件哈希保持不变。六仓 HEAD 未变，Runtime 工作区干净；本轮前已有修改仅在上述验收计数相关位置和自动生成候选来源上叠加增量，其他已有未提交文件哈希不变。未提交、未推送。隔离数据和连接器安装状态保留，协议端已停止；没有删除验收事实。

除表中两个没有自然触发的子分支外，未进行生产跨版本、高并发压力、真实断流/强杀/权限破坏或攻击测试。供应商调用许可不改变 Host→Native SSE 的实际边界；未用不同边界的 EOF 代替所需证据。
