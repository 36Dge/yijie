# FEAT-157 恢复执行与错误诊断

2026-10-08，用户明确要求“继续”，从 [暂停检查点](11-paused-state-2026-10-08.md) 恢复。此前 2 轮 Kimi-K3 文本与 1 次指定 Tushare 读取额度仍按全部使用处理；恢复任务不产生新的调用授权。

本阶段属于既有候选的 semantic 修正，整个 FEAT-157 的最高 contract impact 仍为 breaking。所有 source/consumer 仍是本地候选，不是发布 pin，不提交或推送。

## 本地修正

- 复用暂停前已在 Broker 源契约定义的 `gateway_errors` 三组常量，不在 Provider 另建一套错误事实。只有同一实际 call 在 consume 后仍为 `Rejected` 时返回确定拒绝；明确 Cancelled/Expired/Revoked 且未消耗的调用返回进入外部执行前停止；Consumed、无法取得状态以及后端/结果处理失败均保留 unknown。返回仍使用现有 MCP `isError/content`，不增加影子 DTO，不转发供应商错误原文。
- 补全暂停时未完成的 Worker 调用方和 PermitSlot 适配。阶段诊断只记录固定枚举、时间和 HTTP 状态；HTTP `request` 事件表示即将交给客户端，不等于服务端已收到。保留每次唯一 HTTP 许可和不自动重试，结果解析规则没有放宽。
- Native 无当前 Host 时可返回有作用域的本地 managed/名称快照，不启动 Host 或 Probe；有当前 Host 时，在当前 owner/tenant 与原 agent/thread/turn 校验后可读取历史工具结果。旧 Host nonce 不再使历史观察永久 NotReady。审批仍按当前 nonce 和原调用严格校验，旧批准与旧 grant 不会恢复。
- Host 对无法解析的结果使用已有 `unsupported_result`，避免严格契约校验丢弃已观察的工具记录。Pending Enable 说明改为检查连接和工具，避免误导重新 OAuth。

## 验证与待办

Worker 默认 38 项已通过；资格回归与最终 canonical 装配结果继续补充。Native 3 项观察回归与全目标 Clippy 已通过；Host FEAT-157 market 定向 race 与 vet 通过。Contracts 初次生成因新字段未登记被正确拒绝，随后发现暂停前 Broker 已存在同一语义源，移除本次 Provider 重复定义，统一复用 Broker；不把中间失败记成通过。一次完整 cargo fmt 对派生文件造成格式漂移，已用 canonical sync 恢复并检查；不手改派生物。

最终 Worker 45 项资格回归（覆盖普通 owner 拒绝后业务调用计数为 0、批准后一次读取与重复消费拒绝）和全目标资格 Clippy 通过。Contracts Broker/Host/Provider 共 14 项 JS、2 个 Go 包与 7 项 Rust 验证通过；7 路生成消费已同步。前端领域、观察 composable 和调用展示 3 个文件 16 项通过。canonical worker 为 `d31203bf223564da8a50e7639636a951bbb57cf3b8c96e1f1b83228e3a33f963`，原制品保留；实际 status-only child 查询与正常 EOF 通过（明确传入该 current.json，未带 manifest 的首次命令仅 skip，不计通过）。标准应用包正在由 canonical launcher 重建。

首次真实行情失败原因仍未知；拒绝结果在模型中的改进、带新诊断的实际查询，以及重启后实际 UI 的历史恢复尚需最终应用验证。任何新增模型或行情请求都须先准备具体用例，再取得新的限量授权。D4 尚未完成。

09:12 后标准包实际 UI 验证：原两轮会话可重开，最新工具失败结果恢复，输入区可用；Host 内存中的旧审批没有被伪造恢复。Tushare 显示“连接待恢复”，显式 Enable 操作 `f930ad2c-967d-4f75-b721-f228fa06645a` 使用已保存 Keyring 授权完成 initialize/tools/list/artifact，恢复为已启用。Pending 说明显示正确。原会话已选中 Tushare 并填好新单次查询草稿，发送按钮可用，未发送。该观察证明本地恢复与当前连接，尚不证明一次实际续轮模型请求。

本轮新增金融调用和模型发送均为 0，已请求追加最多 2 轮 Kimi-K3 文本和 1 次相同股票/日期查询，等待明确回复。全量 Desktop lint、Host lint 通过；固定 Runtime SHA 和 Codex 干净状态复核保持。期间 Desktop HEAD 由外部工作推进至 `7c0bf92c5a86a89fbd317482faece8c051f452c8`（店铺页提交），本任务未提交；三个保护文件相对原 `8d74159e…` 基线的 diff SHA 仍为 `50ca7a11…b4eeb`，内容未被覆盖。

09:30 收到用户明确追加授权：**4 轮模型、2 次只读查询**。该批次单独计数，上批 2 轮/1 次额度保持已用。用户同时提供积分权限截图和腾讯文档，要求核查供应商权限是否为失败原因。先核对公开资料与新诊断，不将账号授权成功等同具体数据接口权限，也不假定购买权限即可解决问题。
