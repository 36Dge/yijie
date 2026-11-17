# 晚到终态源码复审与修复

用户要求源码复审并直接修复。`contract-impact=semantic`：修正 Desktop 对既有 SSE13/Native v6 的订阅、释放及展示时机；不新增 wire、Runtime 补丁、审批数据库或迁移。现有 `_meta`、原轮次快照和决定事实仍为关联依据。当前未提交文件已逐仓保存副本、哈希和 diff，证据目录为 `yijie-desktop/.local/market-architecture-verification/2026-11-17-late-terminal-review/`。

## 复审发现与最小方案

1. **P2：读取停止不等于连接释放。** `application.rs` 将 native/artifact 分支禁用后仍持有对应 HostEventStream；另一个流未结束时，已完成/65秒到期的原生连接继续存活。改为独立拥有和释放两个可选流。窗口在首次观察终态时立即锚定，不等持久化/展示结束，不因暂时没有 pending Item 而推迟起算。
2. **P2：并行旧轮反复发布其他轮次事件。** `NativeDisplayBuffer::observe` 对 foreign turn 推进 cursor 后返回 changed，导致旧轮写库/发布，前端又因 terminalObserved 反复 resync；`native_history` 会调用原生 thread/read。改为仅推进传输 cursor，除非出现新的传输诊断，否则不作为本轮内容更新；前端对同一终态后的 Item 更新直接使用原生快照，不重复整轮 resync。
3. **P2：所选历史轮次没有接入晚到事件失效。** `useMarketChat` 的 nativeRevision watcher 只刷新默认轮次。复用现有串行读取队列，在事件失效时按所选原 turn 读 events；保留选择/epoch/revision 防旧回包，不用历史响应覆盖 live approvals。轻量读取跨到新 nativeTurn 时清除旧 tools，避免旧完成结果显示在新轮“最新结果”。
4. **P2：已终止旧轮的普通 SSE EOF 会结束其他观察。** 原代码将所有 EOF 作为协调器错误，导致并行新轮观察被整体丢弃。已知 terminal 后的正常 EOF 仅结束该只读观察，保留未确认事实；活动轮的未知流错误仍沿原有失败策略，不自动重连/重发。

验证只使用普通数据、合法 SSE、正常关闭、受控逻辑时钟和既有安全定向用例；不强杀、不破坏权限、不制造攻击 fixture。重点检查多连接分别释放、退出、传输 cursor 不串轮、历史事件队列合并与旧响应保护、`_meta` 原身份及业务错误语义。结果在实施后补充。

## 实施结果

上述4类 P2 均已修复，改动限于 Desktop：

| 源码位置 | 已完成的修正 |
| --- | --- |
| `src-tauri/src/chat/application.rs` 的 `market_terminal_deadline`、`stream_native_turn` | 第一条终态被观察时即固定单调时钟截止点；Native/Artifact stream 独立释放；Native 结束或窗口届满无需等产物流；已终态的正常 EOF 保持未知结果并正常结束该观察，不使协调器中断其他观察 |
| `src-tauri/src/chat/native_conversation.rs` 的 `observe` | 外轮事件只推进 transport cursor；没有新的传输诊断时返回未改变，不写旧轮视图或重复发 IPC；原轮 Item/状态仍按精确身份过滤 |
| `src/stores/chat.store.ts` 的 `applyNativeView` | 只在终态/原生读取状态变化或新诊断时 resync；晚到 Item 已由 Native snapshot 提供，直接展示，不再重复 thread/read |
| `src/composables/useMarketChat.ts` | 已选历史轮次通过同一个合并读取队列刷新 events；selection/epoch/revision 校验拒绝旧回包；历史读取不覆盖当前 approvals；独立审批修改不会让历史读取的 loading 状态卡住；新 nativeTurn 绑定后不沿用旧完成 tools |

同会话观察键继续为 `(session, frozen local turn)`，没有退回仅按 session 排队；单一 outbox dispatcher 保持。自动刷新仍消费原生通知和原生历史 API，无新轮询器、执行器或结果重建。窗口结束、正常 EOF、缺少结果只结束观察/标注不可用，不写出虚构的 completed/failed。

## 定向验证结果

- **7项 Native 定向测试通过**：65秒截止点（含 pending 投影暂缺/重复事件）、晚到 Item 顺序、外轮 cursor 与原轮状态隔离、既有重叠观察、原选择/代际 `_meta` 校验。
- 其中双流集成用例用实际 `HostBridge` HTTP/SSE 客户端和普通本地协议响应，分别验证 **Item 完成、终态后的正常 EOF、正常 request_stop**：Native 连接先释放、产物连接独立拥有；停止时两条连接释放，原轮保持 interrupted。没有强杀或故障注入。
- **38项相关前端测试通过**，另 **1项 chat store 定向测试通过**（其余171项未执行）；覆盖所选历史晚到更新、事件合并、旧选择回包、独立 live decision、清除旧轮完成结果和抑制重复整轮读取。
- **6项 Host 定向测试通过**：原生 Item 与原始回执、正常重开、冲突链接、业务 isError、事件缓存及并发历史快照。Host 源码没有修改。
- 最终严格 Native lib Clippy（`-D warnings`）、受影响 ESLint、vue-tsc 和六仓 `git diff --check` 通过。前轮已清理的6处 Clippy 告警没有恢复。

主要日志：`native-r2-tests.json`、`native-r2-*.log`、`native-clippy-r2.log`、`market-observation-tests-r2.log`、`chat-store-late-test-r2.log`、`selected-mutation-final.log`、`host-meta-tests.log`、`frontend-eslint-final.log`、`vue-tsc-final.log`。最初测试误用了 store 私有字段、一次局部格式整理造成编译错误，均已纠正并重新验证；失败日志保留，没有计入通过结果。

## 关联与退出复核结论

本轮范围内未发现新的审批绕过或 `_meta` 越界关联路径。Host 仍核对原 thread/turn/tool、operation/selectionDigest 与账本归属；Native 再核对具体原选择 reference、service 和本次 Item 身份。重复 callRef 的冲突链接被省略，原生结果不被改写；许可消费/批准不代表执行成功，isError 保持失败。历史视图只读，不向 live decision 列表提供旧审批。

正常退出路径保留原 request_stop→stopping/lifecycle→等待观察结束；新连接所有权调整只关闭只读 SSE，不发起 Runtime turn/interrupt 或工具重试。普通双流测试确认连接释放；这不是所有 OS、背压、网络故障或高并发压力场景的证明。

## 保留与未执行

- 保留“原生未产生终态就继续未确认”的边界；65秒是额外观察上限，不延长工具许可。已进行中的持久化仍按原正常流程完成，不为了时限取消写入。
- 本轮是源码复审及定向回归，**没有重启易界、没有重新进行 GUI/真实 Runtime 实机验收，也没有调用真实模型或供应商**。正常入口下次启动会按来源检查重新构建 Native；不将前轮实机结果冒称本轮结果。
- 没有执行禁止的进程/权限/攻击故障测试或全量回归；跨版本生产发布与非 macOS 验证未执行。
- 已有未提交文件中仅在本轮相关4个文件上叠加修复（Native两处和 market composable/测试）；其他已有未提交内容哈希不变。另改两个原本干净的 chat store 源码/测试文件。六仓 HEAD 均未变，Codex 工作区干净；未提交、未推送。
- 回滚应撤销本轮局部增量，不能整仓 reset 或覆盖前轮工作。当前基线副本与增量 diff 均在证据目录；无数据库降级、审批重放或二进制替换步骤。
