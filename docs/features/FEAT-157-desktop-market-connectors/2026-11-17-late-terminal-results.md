# 晚到终态自动刷新与六处 Clippy 修复结果

2026-11-17。先完成 [最小方案](2026-11-17-late-terminal-plan.md)，再实施和定向验证。`contract-impact=semantic`（Native 订阅生命周期修正），现有 SSE13/Native v6、SQL47 和审批语义不变；Clippy 清理为等价改写。没有提交、推送、Runtime 补丁或新审批数据库。

## 修改

仅修改 Desktop 三个源码文件，Host、Connectors、Contracts、Codex 的前轮源码保持原样：

- `src-tauri/src/chat/application.rs`：turn terminal 后，如果还有已开始的 yijie_market Item，则继续读取**同一原生 SSE**。收到真实 Item completed 后立即结束观察；从首次 terminal 起最多65秒，重复事件不能续期。生命周期停止/挂起仍正常退出。观察任务按 session+冻结的 local turn 区分，旧轮收尾不会阻塞同会话的新轮。
- `src-tauri/src/chat/native_conversation.rs`：只识别原轮已观察到、仍未完成的市场 MCP Item。复用现有 Native buffer、事实保存、IPC 和前端事件失效通知；不从 turn terminal 推断工具执行状态，不把其他轮次 Item 写入本轮。
- `src-tauri/src/native_auth/local_service.rs`：移除无副作用的 unit 错误闭包，六处 `Err(fail())` 改为 `Err(())`；原凭据读取、权限/属主/单链接/大小/UUID/token/zeroize 校验保持。未支持平台分支统一返回同一 unit 错误，未增加平台能力。

保留前轮已有的单次历史降级读取；没有新增历史轮询、审批重发或工具重试。此前约束原生订阅关闭的代码位于 `application.rs`，Host 的原生 EventHub 和 SSE 路由本来就允许 turn terminal 后继续转发 Item completed，因此本轮无需改动 Host/Runtime。

## 定向验证

证据目录：`yijie-desktop/.local/market-architecture-verification/2026-11-17-late-terminal/`。

| 验证 | 结果 | 证据 |
| --- | --- | --- |
| 严格 Native Clippy | 通过，原6处 unit_arg 已清除；没有添加 allow/suppress | `native-clippy.log` |
| SSE 晚到 Item | 先实际发布轮次 interrupted，再送 Item completed；Native 保存 Item failed，轮次仍 interrupted，无重放请求 | `native-terminal-tests-r2.log` |
| 观察窗上限 | 无待完成 Item 不等待；重复事件不延长65秒截止时间；到期结束观察不合成执行状态 | 同上 |
| 多 Item/其他轮次 | 等待每个原轮开始项；其他轮次同名 Item 不能使本轮完成 | `focused-1.log` |
| 既有多会话观察、正常中断 | 均通过 | `focused-2.log`、`focused-3.log` |
| 正常凭据解析与 owner-only 文件读取 | 均通过 | `focused-4.log`、`focused-5.log` |

以上共7项定向 Native 测试通过；不是全量回归。初次新增 SSE fixture 漏了既有必需的 `X-Accel-Buffering: no`，被真实 decoder 拒绝；补齐普通响应后通过，原失败日志保留。没有放宽 decoder 或制造故障以验收。

新增/修改代码已按 rustfmt 整理；application.rs 三处既有格式差异没有顺手改写。六仓 `git diff --check` 通过。未改前端/Host/Runtime 实现，不为本轮重复运行它们的全量测试；非 macOS 编译未执行。

## 普通本地协议端实机验证

使用原 canonical 入口：

```text
python3 -B scripts/development-client.py start-ui --market-acceptance late-20261117
```

独立 Native/Host/Runtime 目录；正常构建产品 worker；普通本地 MCP 和 Responses 驱动。Host/worker 复用原制品，Native 正常增量构建。此次没有调用真实模型或真实连接器供应商；上轮真实模型结果不冒称本轮覆盖。

正常构建 Native SHA-256：`b288820e66bc67f89a28853710fec956050c335b158237108059be7a42c43f8a`。

1. **正常停止后自动刷新通过。** GUI 允许一次慢调用，再点击“停止生成”。先显示已停止/无关联结果；约8秒后自动更新为工具失败和“未取得可验证结果”，同时出现本次批准关联；没有手动刷新、切历史或重开。SQL 的原生事实顺序确实是 `turn/completed(interrupted)` → `item/completed(failed)`，来源为 `runtime_notification`，非历史补写。晚到时仅新增1次 approvals 和1次 events，history/thread_read 增量0。见 `case-late-result.json`、`native-late-arrived.json`。
2. **同会话新轮不被旧轮阻塞，审批独立。** 再批准一次慢调用、正常停止后立即发送新轮 dual 请求。新轮比旧协议请求返回早2489ms开始，有自己的原生轮次和新审批卡；旧轮批准没有被沿用。新轮批准后实际返回文本与独立 JSON，GUI 正确完成。见 `case-overlap-result.json`。
3. **终态关联和留痕。** 两个确实存在的原生终态，其 rollout `_meta["yijie.market.call"]` 与 Host projection 完全相同，并匹配原 thread/turn/operation/selection/ref/decisionId。SQL47 最终保留3组 requested/acknowledged，共6条事实；每个决定均独立。见 `native-correlation.json`、`native-final-closed.json`。
4. **没有持续空闲读取。** 最后一轮结束后，无干预测量61321ms，approvals/events/history/thread_read 的增量全部为0。见 `idle-clean-start.json`、`idle-clean-end.json`。审计脚本在测量窗外进行的显式 history 读取单独保留，不计为产品轮询。

## 如实保留的边界

- 重叠用例中，立即开始下一轮后，旧调用没有可读取的原生终态：Host history 为空，正常退出后再次核对 rollout 仍无该 Item 的结束记录。旧轮维持 interrupted，决定只读且结果未确认；不借用新轮结果，也不以普通协议端已返回推断 Native 成功。这一用例证明隔离/不阻塞，但**不算旧轮晚到终态通过**。修复针对“原生终态已经发出，却因 Desktop 提前断流而漏掉”；不能代替上游生成不存在的终态。
- 自动观察限于已经收到开始事件的 yijie_market Item，最多65秒。超窗、缺少开始事件、真实断流或进程退出仍需要已有显式历史核对，并保持未知状态。未新增 Runtime 补丁、结果重建或后台重试来掩盖这些边界。
- 65秒上限通过确定性逻辑测试验证；没有故意拖垮供应商、破坏权限或强杀进程制造超时/断流验收。生产跨版本发布、非 macOS 构建及这些故障路径不声明通过。

## 保护、清理与回滚

本轮开始前已有的全部未提交文件内容哈希保持不变；六仓 HEAD 未改变，Codex 工作区仍干净。原始 diff/文件副本在 `baseline-files/` 与 `baseline.json`，核对在 `prior-dirty-preservation.json`。日常数据库和密钥文件哈希与本轮前一致；没有对日常 Native 库迁移。

通过 GUI 停用隔离连接器、⌘Q 正常退出 App，启动进程 exit0；普通协议端 inflight=0 后使用自身 stop 接口退出。18081/18083/18085 已关闭，无本轮产品子进程残留。证据和隔离数据保留；没有强杀、权限破坏、二进制替换、提交或推送。

回滚只撤销本轮三个源码文件的增量，保留前轮未提交改动，再按原入口标准重建；不复制覆盖受审计二进制，不降级/删除 SQL47 或 Native 格式6数据，不补发决定或调用。旧 Native 仍能读取既有格式6晚到 Item 记录，但运行时会恢复原有提前关闭缺口，因此回滚不等于缺口消失。
