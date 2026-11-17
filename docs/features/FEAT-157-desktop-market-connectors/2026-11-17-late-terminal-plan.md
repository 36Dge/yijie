# 停止后晚到终态与 Clippy 最小修复

已实施；结果、源码修改和未覆盖边界见 [本轮验证记录](2026-11-17-late-terminal-results.md)。

用户已授权本轮实施和定向验证；继续保护现有未提交改动，不提交或推送，不新增 Runtime 补丁/审批数据库。普通本地协议端实机验证沿用已批准的隔离入口，不制造进程、权限或网络故障。

`contract-impact=semantic`：修正 Native 观察订阅的关闭时机及并行观察的身份；wire、审批权限、SQL47、Native 格式6均不变。Clippy 清理本身为 none（返回相同 unit 错误）。

## 源码依据与范围

- 上游固定 `yijie-codex` `5c64ed3f03808639faf7c11674e87636a94ab221` 的 app-server 将 canonical ItemCompleted 独立转为 item/completed；turn/completed 不提供完整 Item 集合。
- 现有 `yijie-contracts/openapi/native-conversation-v6/native-conversation-v6.yaml` 的 SSE13 及 `docs/native-trace-v6.md` 已规定原生事实/独立 Item、无冷历史逐项合并、观察不驱动执行。无新协议或生成物，Contracts/Host/Runtime 实现修改 N/A；本轮是消费现有事实的生命周期修正。
- Host 的 SSE loop 不因 turn terminal 退出，原生投影与 market cache 可接收晚到 Item；Desktop `application.rs` 却在 terminal_observed 后停止 next_stream_event 并返回。Native buffer 和 IPC publish_native 已允许终态轮次继续保存/显示原生 Item。
- 同一 session 的新轮次不能被旧轮收尾阻塞：协调器观察键应从 session 改为冻结的 session+local turn，沿用同一个 outbox dispatcher。

## 最小实现

1. 对已观察到的 yijie_market 开始项，保留同一 SSE，直到实际 item/completed 全部收齐；从首次 turn terminal 起最多65秒（现有 MCP 调用上限60秒，留5秒通知余量）。不延长工具/审批许可，不新增定时 thread/read 或调用重试。
2. 继续使用原 Native buffer、格式6事实保存、IPC、marketNativeRevision 和 Host event snapshot。读到其他轮次只推进原生 cursor，不把其 Item/状态写进原轮次。
3. 正常终态无未完成 market Item 时立即关闭；生命周期停止/挂起仍立即退出。到达界限或流不可用保持原生已知状态及未确认提示，不合成成功/失败。上一轮单次 history fallback 暂保留，作为已有兼容降级而非持续观察来源。
4. 同会话多轮观察固定 context，避免建立任务后再次读取变化的 active turn 导致串轮；旧轮晚到事件不阻塞新轮订阅。
5. 清理 `native_auth/local_service.rs` 六处 unit_arg；只消除无副作用闭包，不改权限、属主、文件大小、单链接、UUID、token 格式、zeroize 校验。顺带将未支持平台分支返回类型统一为已有 `Err(())`，不增加该平台能力。

## 定向验证

- 普通 SSE fixture：turn interrupted 后才返回原始 Item completed；验证真实顺序保留、无伪造 turn success、无二次工具/审批请求。
- 同轮多个 Item、其他轮次 Item、新轮观察和有界关闭；用纯逻辑/受控测试时钟验证时间上限，不调整系统时间或强杀。
- 相关 Native 测试、受影响格式检查、strict Clippy；不执行安全排除清单中的故障/攻击 fixture，不跑全量测试。
- canonical 本地隔离 App + 普通本地 MCP：允许一次后正常停止，等待晚到失败/未知结果自动出现，核对 _meta/原轮次/SQL事实；检查正常新轮仍独立审批，结束后读计数停止。需要模型时沿用已有授权，但本轮可先使用正常协议驱动。

## 兼容、保护与回滚

新 Native 消费已有 Host/Runtime 事件；旧 Native 仍存在旧关闭缺口，但无需升级 wire 或数据库。回滚仅撤销本轮 Native 订阅和 unit_arg 增量，按原入口标准重建；不恢复/删除/改写审批事实，不降级数据库，不复制替换受审计二进制。

本轮前全部六仓的 HEAD、未提交文件哈希、原文件副本及 diff 已保存在
`yijie-desktop/.local/market-architecture-verification/2026-11-17-late-terminal/`。
