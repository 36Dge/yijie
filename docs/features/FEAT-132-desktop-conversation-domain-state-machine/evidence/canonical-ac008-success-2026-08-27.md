# FEAT-132 canonical AC-008 成功证据

> 记录时间：2026-08-27T17:43:32+08:00  
> 入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`  
> 方法：操作 Desktop 可访问界面、只读健康接口，并在应用正常退出后只读核对 canonical 专属 Runtime state/rollout；不读取或写入目标项目文件，不向 Agent 暴露工具，不执行自动重试。

## 授权与调用计数

- Owner 在首次独立授权已经 1/1 消费之后，又明确授权 **最多 1 次** canonical 无敏感纯文本 prompt；禁止工具调用和文件读写，不自动重试。
- 两次彼此独立的 FEAT-132 授权累计上限为 2，累计应用 submit 为 2/2。首次 submit 的 queued 失败继续保留为历史，不改写为成功。
- 本轮发送内容只要求固定单行回复 `FEAT-132-STATE-MACHINE-OK`，不含业务数据、PII、secret 或项目文件内容。
- 提交前一次 `RETURN` 自动化键名在 Computer Use 服务端被拒绝，应用界面、路由、输入值与发送按钮均保持原样，因此没有到达应用 `submit()`，也不计为应用 submit。随后只点击一次已启用的“发送任务”按钮；没有第二次应用 submit。

## Preflight 与固定边界

- canonical fresh run 使用有效项目 `.feat131-smoke.erXl1B`；项目目录存在且权限为 `0700`。
- 提交前新建任务页为 `ready`：输入框可编辑，空输入时发送按钮 disabled，填入获准文本后按钮 enabled。
- `/readyz` 返回 `runtime_state=ready`、`status=ready`。
- `/v1/status` 返回 Runtime `0.144.6`、Provider `minimax`、模型 `MiniMax-M3`、transport `stdio`、`experimental_api=false`。
- Runtime、Contracts、Host 冻结仓库保持 clean；Desktop `src-tauri` 无差异。

## 唯一真实 Turn 结果

- 唯一新 session：`01a04297-890b-7aa0-99db-b431829f67f1`。
- 点击一次发送后路由切换到该 session；生产路径从 ready 进入 active Turn，并在 1.5 秒 AX 采样前完成。AX 没有单独采到瞬时 `in_progress` 帧，终态直接观测为 `completed`；下节的同一次真实 Runtime rollout 已补证 `TurnStarted → TurnComplete`。
- 当前历史恰好 1 条 user message 和 1 条 assistant message；assistant 正文严格为 `FEAT-132-STATE-MACHINE-OK`。
- 没有工具卡片、工具调用、文件读写、审批 UI、Artifact 或 Diff。
- 切换到历史旧任务后再选择该 session，路由恢复为同一 session，仍恰好 1 条 user + 1 条 assistant，终态仍为 completed，没有重复消息。

## Runtime lifecycle 只读补证

应用正常退出后，对 canonical 固定目录 `.local/feat131-stable/codex-home` 做只读核对：

- `state_5.sqlite` 以 SQLite readonly/query-only 打开；该 canonical home 中恰好 1 个 thread：`01a04297-895a-7071-bffb-22d4c8d9cd3f`，cwd 为本次有效项目，模型为 MiniMax-M3，rollout 指向 `rollout-2026-08-27T17-40-22-01a04297-895a-7071-bffb-22d4c8d9cd3f.jsonl`。
- 只用 `jq` 投影事件类型、时间、turn ID 与“固定文本是否精确匹配”的 boolean，不输出其他正文。结果为 `user_prompt_match=true`、`assistant_reply_match=true`。
- 同一 rollout 在 `2026-08-27T09:40:22.553Z` 记录 `task_started`，在 `2026-08-27T09:40:23.998Z` 记录 `task_complete`；两者 turn ID 均为 `01a04297-8992-75f3-9b2c-ccf97864a4a7`。
- 固定 Runtime `codex-rs/protocol/src/protocol.rs` 明确定义 v1 rollout 的 `task_started` 即 `TurnStarted`；regular Turn 在 `codex-rs/core/src/tasks/regular.rs` 内联发送该事件。固定 Host `internal/session/service.go` 只接受 status 归一化为 `in_progress` 的 `turn/started`，并发布 `turn.started`、`payload.status=in_progress`。因此这条真实 trace 证明本轮确实经过 `in_progress`，不是用 reducer 合成结果代替真实运行。
- 脱敏类型计数为：`task_started=1`、`user_message=1`、`agent_message=1`、`task_complete=1`、`token_count=1`，所有 `response_item` 都是 `message`，tool/function/command/file/approval 类型事件计数为 0。
- rollout SHA-256：`9c8d6c7639c2516228aca389a23c3b2152d34b18ee1061308e810ffcf80aa021`。完整 rollout 保留在 canonical Runtime home，不复制进 Feature Package。

## 正常退出

- 通过应用自身菜单 `Quit 易界 AI FEAT-131` 正常退出，没有强杀或故障注入。
- canonical launcher 退出码为 0；App PID `66026`、Host PID `67141`、Runtime PID `67143` 均已退出。
- `127.0.0.1:18081` 与 `127.0.0.1:1420` 均无监听者。

## 结论

AC-008 的真实普通文本 `ready → in_progress → completed`、终态历史与重开幂等均通过；本证据支持 `real_smoke=PASS`。证据明确区分 AX 直接画面与同次 Runtime 持久化 lifecycle trace，不伪造截图或状态。
