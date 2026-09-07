# S3 原生自动审核兼容性核对

范围为固定 retained FEAT-136 Codex 0.144.6、MiniMax-M3、中国站 Responses API、canonical local/demo_fast。核心源码只读，未升级 Runtime 或改供应商。

## 无付费前置核对

- `codex-rs/model-provider/src/provider.rs` 的默认审核模型名是 `codex-auto-review`。
- `codex-rs/core/src/guardian/review.rs` 中 `guardian_review_session_config` 先查模型目录和可选 override；目录无默认审核模型且无 override 时，回退到当前任务模型。
- Host 的 `miniMaxModelCatalog` 及实际受管 catalog 仅列出 MiniMax-M3，没有 auto_review override。因而预期使用 MiniMax-M3，而不是假定 MiniMax 提供名为 codex-auto-review 的模型。
- `guardian/review_session.rs` 中 `build_guardian_review_session_config` 克隆父 Config，继承供应商、base_url 和认证配置；把自身限制为只读/never，并把 request/stream retry 改为 1。不能以主会话的零重试断言审核子会话也零重试。
- 验证父 Config 的 MiniMax URL 为固定计数器 `http://127.0.0.1:18083/v1`；原生审核继承该地址。计数器仅原样转发到 `https://api.minimaxi.com/v1/responses`，每次转发前记账，包含子请求与重试。
- 追加授权仅使累计硬上限 10 → 15，原有 6 条请求不删除。新增记录只保存受限模型名、结构化输出布尔标记、固定目的地址、时间和 HTTP 状态；不保存提示词、输出正文或凭据。

## 人工接管的原生语义

`thread_approve_guardian_denied_action_inner` 调用原生 `Op::ApproveGuardianDeniedAction`。`core/src/session/handlers.rs` 的 `approve_guardian_denied_action` 只接受 denied 事件，把具体 action 的批准作为 developer context 通过 `inject_no_new_turn` 注入，不直接执行工具、不自行开启下一轮。

Host 已有候选只转换 app-server camelCase 到原生 GuardianAssessmentEvent 的 snake_case，并保留原始 action 内容；决定绑定当前任务及原请求。UI 区分批准和执行，已结束回合需要用户继续任务。既有单元测试覆盖事件投影和拒绝不产生模型调用。

本轮没有自然发生的自动拒绝，未实际调用人工接管批准分支。以上不构成该分支 E2E 通过证明；没有伪造拒绝通知或制造危险操作去获得某种结果。

## 真实观测

见 `runtime-observations.json` 和 `provider-requests.json`：

- 父会话 `01a0797c-6d7a-7623-8951-b4564547f0a2` 的第一轮为 workspace-write/on-request/auto_review。
- 原生 guardian 会话 `01a0797c-a58d-7471-8c06-f61cdd013bdd` 的来源是 `subagent.other=guardian`，模型 MiniMax-M3，供应商 minimax，沙箱 read-only，审批 never。
- 原生审核实际返回 `{"outcome":"allow"}`。对应第 8 个 HTTP 请求含结构化输出；父请求为 7，工具后的回复为 9，三者均经计数器完成。
- 完全访问的第 2 轮为 danger-full-access/never/user；切回请求批准的第 3 轮恢复 workspace-write/on-request/user，network_access=false。

这些数据从正常 Runtime rollout 中只选取元数据、回合权限和审核 outcome；没有复制整份对话或审核提示词作为证据。
