# FEAT-132 canonical queued 根因证据

> 采集时间：2026-08-27T16:37:22+08:00  
> 方法：应用正常退出后，以 SQLCipher raw key 的既有只读能力打开 Desktop 数据库；只查询状态、计数和 presence boolean。未输出 key、bookmark 内容、用户正文、路径正文或 Host/Runtime payload，未写数据库。

## 脱敏状态

- 目标 session：`01a0421d-10dc-7972-a79e-72f29469cb46`。
- Public Task binding：`bound`，`public_task_id` 已存在，authorization revision 为 `1`。
- Desktop session：`agent_session_id` 与 `runtime_thread_id` 均不存在。
- Turn：`queued`，`runtime_turn_id` 不存在，未终态化。
- 唯一 conversation outbox：`create_session / failed / attempt_count=16 / next_attempt_at absent`。
- 项目记录存在、未移除，刷新后的 security-scoped bookmark 长度为 812 bytes；不记录 bookmark 内容。
- 固定 Runtime state 数据库没有 thread，Runtime 日志没有 thread-bound 记录；未观察到 Provider/Runtime Turn。

## 因果链

1. canonical 稳定 App 的持久化项目记录仍指向已被清理的 FEAT-131 临时目录。
2. Public Task control plane 正常完成绑定。
3. Desktop `dispatch_create` 在调用 Host 前解析 security-scoped bookmark；失效目录产生 `ProjectUnavailable`。
4. 该错误沿 `?` 返回，已 claim 的 outbox 保持 `inflight`，等待 30 秒 lease 到期。
5. coordinator 反复 claim，attempt 增加到 16；数据库随后把 outbox 置为 `failed`，但关联 Turn 仍是 `queued`。
6. 重建同一路径并由 picker 刷新 bookmark 只更新项目记录，不会重新激活已经 `failed` 的 outbox；正常重启也不会 claim 它。

因此，失败点确定在 Desktop bookmark/create-session/outbox 边界，位于 Host session、Codex Runtime Turn 和 Provider 调用之前；不是 `yijie-codex` Runtime 问题。

## 安全边界与处置

- 未自动重启目标 failed outbox。现有记录没有持久化 failure provenance；accepted-but-response-lost 的 Host transport failure 也可能呈现“无本地 Host mapping”的相似形态，通用代码不得猜测后重放。
- 当前一次性 prompt 授权已经用完；本轮不再次 submit，也不通过数据库写入恢复该 operation。
- FEAT-132 已完成新会话项目有效性 preflight、nullable/max+1 Turn ordinal、cleanup shared-sequence/late-response、create/submit post-response guard 与 Turn 终态 Item sealing，并通过 focused/full tests 和最终独立复核。
- 目标 failed operation 仍不重放；真实 AC-008 仍需 Owner 新授权的一次全新 valid-project 普通文本 smoke。
- 更完整的 outbox lease 归还、带 provenance 的可恢复等待态和 exhausted outbox 终态投影，应按 source-first 另行治理；unknown Host transport 必须继续 fail closed。

## 2026-08-27 后续处置

- 本文保持为首次独立授权 session `01a0421d-10dc-7972-a79e-72f29469cb46` 的历史失败与根因证据；该 failed outbox 没有被重放、删除或改写。
- Owner 后续另行明确授权最多 1 次 valid-project canonical 纯文本 smoke。全新 session `01a04297-890b-7aa0-99db-b431829f67f1` 已 completed，历史恰好 1 user + 1 assistant，重开无重复，且无工具、文件或审批。
- 因此本文第 30–32 行描述的是当时的授权与停止条件，不再代表 FEAT-132 的最终门禁状态；最终成功事实见 `canonical-ac008-success-2026-08-27.md`。
