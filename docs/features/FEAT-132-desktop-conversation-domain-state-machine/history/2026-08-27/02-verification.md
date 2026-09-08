# FEAT-132 Demo 验证

## 1. 当前门禁状态

| Gate | Result | 说明 |
|---|---|---|
| D0 | PASS | Brief、Must AC、Contract First、授权、工作区边界与 reference policy 已落盘并通过 package checker |
| D4 | PASS | 实现、自动化、独立审查、Runtime freeze、canonical readiness 与第二次独立授权的 valid-project real smoke 均完成；首次 queued 失败作为历史保留 |
| DP | N/A | `exposure=local`，不提供公网入口 |

首次独立授权产生的 queued 失败不推翻 AC-001–007，也没有被删除、重放或改写。Owner 随后明确增加
第二份单条授权；fresh valid-project canonical Turn 完成并通过历史重开。Feature、AC-008、verification
与 real_smoke 四个关联字段已原子收口，strict D4 checker 为 PASS。

## 2. Must AC 结果

| AC | Result | 可复核证据 |
|---|---|---|
| AC-001 | PASS | reducer 重放、canonical serialization、snapshot/restart 与 permutation focused tests |
| AC-002 | PASS | interleaved Item delta、稳定本地 identity、adapter 与 Store integration tests；生产路径不再以全 Turn 单缓冲区作为语义 authority |
| AC-003 | PASS | eventId FIFO 去重、sequence duplicate、Item/terminal 幂等，以及 cleanup auxiliary 的 N→N+1、duplicate、gap/resync tests |
| AC-004 | PASS | warning/error 非终态、`turn.completed` 原子封口 Turn/未完成 Item、迟到 delta fail-closed 与 recovery tests |
| AC-005 | PASS | item final equal/superset/regression/divergence、terminal snapshot 原子合并与 resync tests |
| AC-006 | PASS | unknown semantic 固定占位、exact parser 负向测试、malformed routing scope 与 raw canary scan |
| AC-007 | PASS | authorization/context/session/selection/draft epoch、A→B late valid/malformed/create/submit/cleanup、live-first response 与 artifact/draft 回归 |
| AC-008 | PASS | 两次独立授权累计 2/2：首次 queued 失败历史保留；第二次 valid-project canonical 仅一次 submit，session `01a04297-890b-7aa0-99db-b431829f67f1` completed，恰好 1 user + 1 assistant，固定回复正确，切旧任务再重开无重复，且无工具/文件/审批/Diff |

## 3. 修改前基线

| Repository | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| yijie-desktop | `pnpm exec vitest run src/domain/chat-ipc.test.ts src/stores/chat.store.test.ts src/pages/chat/ChatPage.test.ts tests/feat-131/chat-event-replay-harness.test.ts scripts/check-feat131-replay-boundary.test.mjs` | 0 | PASS：5 files / 111 tests | 2026-08-27 |
| yijie-desktop | `pnpm exec vue-tsc --noEmit` | 0 | PASS | 2026-08-27 |
| yijie + yijie-desktop | `git diff --check` | 0 | PASS | 2026-08-27 |

## 4. 最终自动化矩阵

| 范围 | 命令/检查 | Result |
|---|---|---|
| Focused | `pnpm exec vitest run src/domain/chat-ipc.test.ts src/api/chat-client.test.ts src/api/chat-conversation-adapter.test.ts src/domain/conversation-state.test.ts src/stores/chat.store.test.ts src/pages/chat/ChatPage.test.ts tests/feat-131/chat-event-replay-harness.test.ts tests/feat-132/conversation-projection-replay.test.ts scripts/check-feat131-replay-boundary.test.mjs` | PASS：9 files / 170 tests |
| Lint/contract | `make lint` | PASS：public API、Host v2/v3、Skills generate:check、ESLint、vue-tsc、cargo fmt、cargo clippy |
| Full test | `make test` | PASS：84 files / 690 TypeScript tests；265 Rust tests PASS，3 条既有条件测试 ignored，0 failed |
| Build | `make build` | PASS：Vite production build 5287 modules；仅有既有大 chunk warning |
| Docs | `pnpm docs:build` | PASS：VitePress build complete |
| Patch hygiene | `git diff --check`（yijie、yijie-desktop） | PASS |
| Source boundary | scoped diff、排除项 `rg`、raw canary scan | PASS：无 Runtime/Host/Contracts/Rust schema 变更，无 raw payload 泄露，无 Owner 排除功能实现 |
| Feature gate | `check-feature-package.sh --strict --gate D4 docs/features/FEAT-132-desktop-conversation-domain-state-machine` | PASS |

全量 TypeScript 测试出现既有 happy-dom module-load warning，但命令退出码为 0，所有断言均通过；本记录不把 warning 隐藏或误写为失败。

## 5. 代表性安全失败与恢复

只使用无敏感、确定性的 synthetic fixtures，经生产 parser → adapter → reducer → Store 路径验证：

- 重复 eventId 和 sequence 不重复追加正文或终态；
- sequence gap、非法 lifecycle、content/lifecycle mismatch 进入 `recovery_required`；
- cleanup N 后的领域事件 N+1 不产生伪 gap；duplicate cleanup 不重复 refresh，cleanup gap 触发 resync；A 的迟到 cleanup 状态不污染 B；
- unknown item/event 只生成固定脱敏 code，不保存 raw wire；
- 双 active Turn snapshot/event fail closed，不先污染状态；
- snapshot 尚未出现的新 Turn（含 item-first race）按 max+1 成为 latest；历史 ordinal 保持不变；
- A→B 后 A 的 late valid/malformed/create/submit/cleanup 不污染 B；同会话 live-first 后的合法 submit response 仍完成 draft 清理；
- terminal resync 失败时 domain/history/sidebar 保持终态一致，且同 Turn 的 Item 已原子封口；
- 正常 resync/recovery 意图可恢复，普通 warning/error 不提前封口 Turn。

结果：PASS。未强杀进程、未注入故障、未替换 binary、未破坏权限、未使用攻击性 fixture。

## 6. Canonical local readiness

入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`

最终代码 fresh build 后正常进入 `tauri://localhost/chat` 业务页面，composer 可见：

- `/readyz`：`runtime_state=ready`、`status=ready`；
- `/v1/status`：Runtime `0.144.6`、模型 `MiniMax-M3`、Provider `minimax`、transport `stdio`；
- `experimental_api=false`；
- 未输入、未发送 prompt；
- 使用应用自身 `Cmd-Q` 正常退出；App、Host、Runtime 均退出，端口 `18081` 与 `1420` 释放。

最终代码证据：`evidence/canonical-current-code-startup-2026-08-27.md`。历史 readiness 截图
`evidence/canonical-ready-final-2026-08-27.jpeg`（1162×768，SHA-256
`ec97e766f7b707686c837e76cf51aee59419fbbe5a54ce69e71934c30c942006`）采集早于最后一轮代码修复，仅作为界面参考，不单独证明最终 build。

## 7. AC-008 两次独立授权真实 smoke

两份授权彼此独立，每份都只允许一次无敏感纯文本应用 submit，禁止工具调用和文件读写，不自动重试；累计上限 2、已用 2/2。

### 第一次授权：queued 历史失败

- Owner 于 `2026-08-27T15:22:41+08:00` 授权一次 canonical prompt；fresh 启动再次确认 `/readyz=ready`、Runtime `0.144.6`、MiniMax-M3 与 `experimental_api=false`；
- 首个 accessibility button click 没有触发应用 `submit()`：输入未清空、路由未变、没有 session 或 user message，因此不构成一次 Provider/request submit；
- 随后聚焦 textarea 并使用组件明确支持的 Enter，应用 `submit()` 只执行一次，创建 session `01a0421d-10dc-7972-a79e-72f29469cb46`；
- history 始终恰好一条 user、零 assistant；latest Turn 始终为 `queued`，旧 UI 对该状态显示固定回退文案“状态已更新”；
- 全程没有工具、文件操作或审批 UI，也没有观察到 Runtime Turn；
- 原 FEAT-131 临时项目目录已被清理。重建同一路径空目录、经应用 picker 刷新只读 security-scoped bookmark、重选并正常 `Cmd-Q`/canonical reopen 后，同一 operation 仍为 `queued`，消息没有重复；
- 按该份授权的“失败不重试”约束，没有在这份授权内再次 submit；最终使用应用自身 `Cmd-Q` 退出，App、Host、Runtime 与端口 `18081/1420` 全部释放。

失败态证据：`evidence/canonical-ac008-queued-2026-08-27.png`，1162×768，SHA-256
`0472e0a900387966a6d88e4541e71bb78cf3101ab880ab845a407436d7331378`。该记录保持为历史 FAIL。

### 第二次且最终授权：valid-project PASS

- Owner 在当前会话明确授权 canonical 入口**再发送最多 1 次**无敏感纯文本 prompt；禁止工具调用和文件读写，不自动重试；
- fresh canonical 使用有效项目 `.feat131-smoke.erXl1B`，`/readyz=ready`，`/v1/status` 确认 Runtime `0.144.6`、MiniMax-M3、`experimental_api=false`；
- prompt 只要求固定单行 `FEAT-132-STATE-MACHINE-OK`，不含项目数据、路径、PII 或 secret；
- 一个无效 `RETURN` 自动化键名在 Computer Use 服务端即被拒绝，应用状态完全未变；随后只点击一次已启用的发送按钮，因此应用 submit 恰好一次且没有自动重试；
- 新 session 为 `01a04297-890b-7aa0-99db-b431829f67f1`；提交前直接观察 ready，响应在 1.5 秒 AX 采样前完成，终态直接观察 completed；
- 正常退出后只读核对 canonical 专属 Runtime rollout：固定 prompt/reply 精确匹配，同一 Turn `01a04297-8992-75f3-9b2c-ccf97864a4a7` 在 `09:40:22.553Z` 持久化 `task_started`/`TurnStarted`，在 `09:40:23.998Z` 持久化 `task_complete`。固定 Host 强制 `turn/started` 只能以 `status=in_progress` 发布，因而补证真实 `ready → in_progress → completed`，不是用 reducer 合成状态替代真实运行；
- history 恰好 1 条 user 与 1 条 assistant，assistant 严格回复 `FEAT-132-STATE-MACHINE-OK`；无工具、文件、审批、Artifact 或 Diff；
- 切换至历史旧任务后重开该 session，路由、completed 终态与 1+1 历史保持不变，没有重复；
- 通过应用自身菜单 Quit 正常退出；launcher exit 0，App/Host/Runtime 均退出，端口 `18081/1420` 释放。

成功证据：`evidence/canonical-ac008-success-2026-08-27.md`。结论：第二次独立授权的真实普通文本主流程、终态历史和重开幂等通过，AC-008 与 `real_smoke` 为 **PASS**。

## 8. Runtime 与跨仓边界冻结

| Authority | Freeze result |
|---|---|
| yijie-codex | HEAD `0ce5902ed400866be0196886bb78f693a004d68d`，working tree clean，version `0.144.6` |
| Runtime schema | 267 files；tree SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` |
| yijie-contracts | HEAD `164b14f609537d727a52326832da04430aecc4ab`，working tree clean |
| Compatibility manifest | SHA-256 `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311` |
| Desktop Rust/private IPC | `src-tauri` 无 FEAT-132 修改；现有私有投影足以适配本 Feature |
| yijie-agent-host | HEAD `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`，working tree clean，无 FEAT-132 修改 |

FEAT-132 没有修改、升级、重编译、替换或同步 `yijie-codex` Runtime，也没有修改中央 Contracts 或 Host。

## 9. 独立审查

独立只读审查跨多轮进行。除早期 lifecycle divergence、双 active Turn、event ledger 淘汰顺序、无界诊断、itemless terminal snapshot 与 conflict preflight 外，final-delta 审查还发现并推动修复：第 2+ Turn nullable ordinal、cleanup 未消费共享 sequence、create/submit post-response authority race、live-first response 对瞬时 `canSend` 的误判、A→B late cleanup 污染，以及 Turn 终态未原子封口 Item。每项均补了 deterministic regression。

最终结论：最新 scoped diff 未发现剩余 P0–P2；独立复核 focused 6 files / 119 tests、`vue-tsc`、scoped ESLint 与 `git diff --check` 均通过。另一次边界复核确认 Runtime/Contracts/Host clean、`src-tauri` 无 FEAT-132 diff、Owner 排除项未实现、FEAT-150 改动保持原状。审查者均未修改工作区文件。

## 10. 排除项与已知限制

- 不实现语音、模型版本信息、模型推理强度信息、分享、置顶摘要切换、侧边面板、分支到新聊天，以及 GS-006 文件修改与 Diff。
- 当前 Host/Contracts 不投影完整 command/tool/approval lifecycle；领域模型只保留安全 closed discriminants，不宣称生产能力已存在。
- Artifact 仍复用 FEAT-128 authority；不得把它表述为 File modification 或 Diff。
- 工作区包含 FEAT-131 未提交结果和独立 FEAT-150 并行改动；本 Feature 未 reset、stash、覆盖、提交或清理这些内容。

## 11. `queued` 根因补充诊断

应用正常退出后，对 Desktop SQLCipher 数据库与固定 Runtime state 执行了只读、脱敏检查。目标记录为：

- Public Task binding 已 `bound`，但 Desktop session 没有 `agent_session_id/runtime_thread_id`；
- Turn 仍为 `queued` 且没有 `runtime_turn_id`；
- 唯一 `create_session` outbox 已 `failed`，attempt count 为 16；
- Runtime state 没有 thread，也没有 thread-bound 日志。

源码对账确认：失效 security-scoped bookmark 在 Host 调用前产生 `ProjectUnavailable`，错误直接返回后由 lease
反复 claim，最终耗尽 16 次；项目 picker 后续只刷新 bookmark，不会重新激活 failed outbox。因此该失败位于
Desktop bookmark/create-session/outbox 边界，排除 Public Task、Host session、Provider 与固定 Runtime Turn。

详细脱敏证据见 `evidence/queued-root-cause-2026-08-27.md`。没有写数据库、没有输出 key/bookmark/正文，也没有重放目标 operation。

该根因只解释首次历史 operation。后续第二份独立授权使用通过 preflight 的有效项目创建全新 session 并成功 completed；旧 failed outbox 仍未重放，因此成功证据没有覆盖或改写首次失败。

## 12. 结论与下一治理动作

FEAT-132 的实现、自动化、边界审计、final-delta 修复、Runtime freeze 与 canonical readiness 已完成。首次 AC-008 失败已定位为 Desktop 失效 bookmark 与 exhausted create-session outbox；新 create 已加入项目有效性 preflight，旧 failed operation 因缺少 failure provenance 继续不做猜测式重放。第二份明确授权的 valid-project fresh canonical Turn 已 completed，并通过 1+1 历史、重开幂等、无工具/文件/审批和正常退出核验。

因此当前结论为：**FEAT-132 统一状态机局部完成，D4=PASS；整个 Epic 尚未完成。** 下一步按 Epic 顺序进入 FEAT-133；不再为 FEAT-132 发送 prompt。
