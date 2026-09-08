# FEAT-132 原生接入实施与来源说明

日期：2026-09-08，2026-09-09 更新来源固定。用户已授权并完成本地源码提交；未发布、未部署，D4 待真实验证。最新提交和执行状态见 [当前推进记录](04-source-freeze-and-d4-2026-09-09.md)。

## 实际基线

开始时以下仓库均干净，分支均为 `chore/retirement-baseline-20260905`。没有 reset、stash、切换分支或覆盖用户改动。

| 仓库 | 开始 HEAD |
|---|---|
| yijie | 771c0f27a7861feb08480c6fe235051aa02b5215 |
| yijie-contracts | 468aecec53cd708286988a221061a2e5ccd2479d |
| yijie-agent-host | b1bb2975a4f16ada1f95005f4674d3b219a32fec |
| yijie-desktop | 3448784464497adad4b5721133a6d4bdbf319da7 |
| yijie-codex（只读） | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

Runtime 使用保留 FEAT-136 来源 `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`、版本 `0.144.6`；canonical runner 固定 binary SHA-256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`、manifest SHA-256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`。本次不重建或替换这些产物，不启用新的实验 API。FEAT-137 永久退役继续有效。

## 原生复用及删除对照

| 删除的自建职责 | 接替的原生入口 / 现在的消费者 |
|---|---|
| TS ConversationState / ConversationEvent reducer、hydrate/reconcile | Codex thread/start/resume/read、turn/start 与实际通知；Vue 只接收完整 NativeConversationView |
| 按正文/ordinal/phase 猜测 native identity | 原生 threadId / turnId / item.id；本地 Turn/operation UUID 只做业务映射，不充当原生 Item ID |
| 最终正文前缀匹配及冲突裁决 | item/completed 最终对象直接替换；显示草稿可以与最终正文完全不同 |
| ReasoningAccumulator、TurnEventReducer 及其数据库 progress/terminal 写入 | 唯一 NativeDisplayBuffer 追加 Item delta / segment index；SQLCipher 保存安全原生事实和显示副本 |
| Turn 结束时封口所有 reasoning/command/tool | 只消费该 Item 自己的 completed 对象；turn/completed.items 不被视为完整集合 |
| Host v4/v5 生命周期 latch、recovered-start/fallback-failed、reasoning 终态补造 | Host 只投影实际原生快照；异常为非终态 projection_notice / warning |
| 无流或投影失败即写入 failed / interrupted | 显示 availability 与本地 submission_status 独立；只有原生状态可写 execution status |
| 重放旧客户端事件以重建历史 | Runtime thread/read(includeTurns=true)；Manager 通过现有 JSON-RPC client 实际请求；没有客户端 rollout parser |
| 全局旧 timeline rollback / 常驻 fallback | 删除旧开关和 renderer 分支；旧数据在同一 timeline 的只读档案分支展示 |

保留 `conversation-approval.ts` 的审批适配、Artifact 资源协议、UI 列表/选择/草稿与业务 outbox。这些不决定原生 Item/Turn 执行语义。FEAT-152 的模式映射、原生审批回调和权限门禁没有变更。

## 实际调用链与契约

1. `yijie-contracts/openapi/native-conversation/native-conversation.yaml` 定义新增安全边界；`compatibility/agent-host-native-conversation-v1.json` 记录固定 Runtime 方法、通知和 schema digest。
2. `yijie-agent-host/internal/codex/session_protocol.go::ReadThread` 使用现有 `m.request` 请求 `thread/read` 且 `includeTurns=true`，校验返回 thread ID；没有复制历史构建器。thread/start/resume、turn/start/interrupt 沿用现有入口。v2 提交的 clientUserMessageId 仅为 UI 关联，不能替代原生 Item ID，也不是服务端幂等保证。
3. Host `internal/session/native_conversation.go` 关联 task/session/thread/turn，筛选允许字段；`internal/app/native_conversation.go` 提供 bearer 保护的 `GET /v1/agent-sessions/{id}/native-thread` 和 `GET /v7/agent-sessions/{id}/events`。SSE 继续使用 stream_id、sequence、Last-Event-ID、有界 replay 和 no-store。
4. Desktop `host_bridge.rs` 通过已有 Host readiness/token/nonce 访问上述接口；`host_domain.rs` 解码 v7。
5. `application.rs::stream_native_conversation` 是唯一协调器；`native_conversation.rs::NativeDisplayBuffer` 是唯一 delta 追加实现。批量显示最多 50 ms / 16 个事件，最终 Item、计划、Turn 事实立即提交。Vue 与 SQLCipher 不再次追加或对账。
6. `native_conversation_storage.rs` 事务保存事实、来源、显示副本、游标与 revision。`chat_load_native_history_v1` 窄 IPC 与 `chat:native-view:v1` 完整视图事件经现有 authorization/context/subscription 保护。
7. `chat.store.ts` 保留选择 epoch / AbortSignal / subscription / revision 隔离，仅替换完整视图；`conversation-view.ts` 是只读展示映射，`ChatTimeline` 继续承接界面交互。

公共 TS/Go DTO 由 Contracts generator 产生并用 `sync-native-conversation.mjs` 同步。Desktop 私有 schema `chat-native-conversation-v1.schema.json` 联同公共定义生成 Rust、TS、AJV validator。两个 consumer 的 native-conversation.lock.json 现已从真实 Contracts commit 生成，记录 `git-commit`、完整 SHA、`published:false` 和源摘要；不冒充发布 tag。生成/来源检查已接入 Desktop `generate:check` 与 `check:native`；Contracts 和 FEAT-152 的完整 Host 来源锁已按真实提交更新并通过校验。

当前 public wire 将 command/cwd/output/tool 映射为安全 label / text；未知类型保持原生 ID，展示 unavailable。原生错误只保留脱敏 message 与允许的 codexErrorInfo 判别值，不保留额外内部上下文。Command 输出 delta 暂不发送正文，仅报告 pending-final；最终输出来自原生 completed 后整体脱敏，避免 Host 再维护一套文本累积器。此流式 Command 缺口明确保留，不能宣称逐字输出完整。

## 历史、恢复与数据保护

Desktop migration `0014_chat_native_conversation.sql` 新增：

- `chat_native_bindings`：仅新提交收到真实 turn/start 响应后注册 native thread/turn ID 与实际 Host nonce；既有行不回填。
- `chat_native_facts`：安全的实际 item/turn/plan 通知；读恢复另存 source=runtime_read 的快照事实，不反向制造 notification。
- `chat_native_views`：每 Turn 一个带 source、revision、availability 的可丢弃显示副本。
- `chat_turns.submission_status`：新 outbox 请求的本地提交状态。提交失败不制造原生 failed/terminal timestamp；唯一活跃索引允许本地失败后新操作。

所有表仍位于相同 SQLCipher scope、Keychain 及事务/外键删除边界；历史 migration 1–13 不变。没有复制用户数据库，没有修改 SQLCipher/Keychain 密钥策略。删除会级联清除 native facts/views/bindings，附件/Artifact 与外部 Host/Runtime cleanup 继续按原协议处理。

Host bbolt 私有 schema 4 → 5 前向升级；只新增 NativeRevision / NativeTerminalTurnID / NativeTerminalStatus 恢复元数据，不保存对话正文。旧记录缺少这些字段即未证明来源；并发 resume 的旧结果不能覆盖较新的原生变更。

普通 UI 历史读取只读（recover=false）。它不会更新执行状态、抢写 revision 或替换正在消费 SSE 的缓冲。只有协调器确认 Host nonce 已换代，或收到 stream_changed，才用 thread/read 的同一绑定 Turn 结果恢复结束状态。状态来源单独标为 runtime_read，terminalObserved=false，界面显示历史信息不完整；它不是实时 terminal 证据。任何已观察的原生 failed/interrupted/completed 优先，冷历史冲突只影响 availability。

当前 Host generation 即使 replay 缺口也继续消费真实通知；不能用同代冷历史提前结束 SSE/Artifact。Artifact 仍走独立 v3 原生资源链，真实 v3 Turn 完成仅作为资源交付顺序屏障，不参与对话终态裁决。旧 generation 无法恢复 Artifact 交付时明确要求资源 resync。

每 Turn 主 Item 集合选择 observed 或 rebuilt。发生来源切换时替换整个集合，不用不同来源的 ID/text/ordinal/phase 猜测 join。原生失败终态和 Item 集合来源分别记录。旧数据按 legacy_archive 只读，原始正文、reasoning、附件、Artifact 和审批历史保留；本地 display ID 不标为原生 ID。

## 已核实的 Runtime 缺口

固定 Runtime 的 `app-server-protocol/src/protocol/thread_history.rs` / `core/src/rollout/policy.rs` 说明：Legacy history 忽略部分 delta，部分 User/Agent/Reasoning 冷 ID 会成为 item-N，部分 Command/计划/错误不持久化；`turn/completed.items` 可为空且 notLoaded。本地不支持用 paginated history 补足，不能新增实验 API 绕过。

因此正常重启前已观察事实可以准确保留，但未观察/未落盘的最终对象不能保证完整恢复。冷历史有时把原失败重建为 completed；有实时失败证据时保留失败，无实时证据时展示来源和不完整，不能把 reconstructed completed 当完整实时证据。

限额是显示/传输边界：Host event ≤ 1 MiB，history ≤ 8 MiB；Native view ≤ 4 MiB、最多 512 Item；每次私有 history 请求最多 50 Turn，响应分页预算约 7 MiB。超限保留可用内容并标记 partial，不写 Runtime failed。

## 切换、兼容与回滚

本次最终按 breaking 管理：旧 Desktop 对合成生命周期的依赖无法维持行为兼容，必须完成消费者迁移。采用新 v7/versioned private IPC。v1–v6 HTTP/SSE 格式保留为单向兼容投影，移除无原生依据的状态合成属于本次明确授权的语义修正；旧 Desktop 语义消费者必须先退役，不能混用新语义 Host 与仍依赖合成状态的旧 Desktop。FEAT-137 的公开历史格式只读，不意味着重新激活其功能。

正式切换必须：旧应用正常结束所有活跃 Turn → 正常退出 → Contracts immutable source → Host pin/构建 → Desktop pin/构建 → migration → 正常启动验证。当前没有对用户运行中的数据库执行切换。

回滚禁止自动启用旧 reducer，也禁止把 native facts 逆写到旧 body/status 推断格式。Desktop schema 14 和 Host schema 5 都不能交给不认识新 schema 的旧版本继续写入；只能修复向前，或在明确数据兼容方案后由用户管理旧版本及其旧数据库。不得静默复制、降级迁移或删除新记录来制造兼容。未执行任何回滚/发布。

## 独立审查

独立只读 agent 审查了 native authority、来源混合、容量、写入竞争、恢复、Artifact 屏障、UI epoch 与 listener 清理。早期发现并修复 OtherTurn 事实污染、冷视图容量缺口、重复 history 返回、UI 读写竞争、CAS 重建丢 delta 和依赖 UI 才能恢复的问题。最后一轮未发现新的可复现 P1/P2。审查未独立运行测试，也不替代真实 Tauri / FEAT-152 / Artifact D4。

实际验证与未执行项见 [02-verification.md](02-verification.md)。
