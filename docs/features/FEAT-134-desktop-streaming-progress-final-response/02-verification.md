# FEAT-134 Verification

> Stage: `D4 PASS` · Canonical evidence: `#5 persistent metadata + #6 final-source UI` · Authorized prompt usage: historical `4/4`, current `6/7`, Feature `10/11`

## 1. 本轮验证结论

当前已完成 D0、Contracts v4、Host producer、Desktop Contract First 主链路、跨层 repeated-finalized 修复与 final-source canonical。#5 提供持久化 content-free 计数和 light/200%/键盘；#6 提供最终源码 processing→completed UI、expanded reasoning/unknown、Composer 恢复和正常清理。两次证据严格分开，最终 review 无 open P0/P1/P2。当前结论：

- Product/UX D0：`PASS`
- 工作区 clean-start 与四仓隔离：`PASS`
- 只读 Runtime / Contracts / Host / Desktop 能力审计：`PASS`
- Contracts v4 source/generated/fixtures/tests：`PASS`（immutable commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`，未 push）
- Host implementation：`PASS`（baseline `1b7bfd…` → initial `201fd9…` → corrective child/final `b9358f…`；未 push；Desktop 精确 pin final SHA）
- Desktop implementation：`PASS / COMMITTED`；immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`，工作树 clean、未 push；TS 835/835、Rust 316 pass/3 ignored、lint/build/fmt/diff PASS
- canonical content-free：`PASS`；历史 tranche 4/4，当前 tranche 6/7、剩 1，Feature 累计 10/11
- CAP-011：`PASS`；#5 raw reasoning item/part=1/1，#6 reasoning expanded
- CAP-010：`PASS（负向 shape）`；AgentMessage `phase=null` 合法映射 unknown；显式 final_answer 正向由确定性 tests 证明
- CAP-012：`PASS（absence/no-fake）`；#5 plan update/step=0/0；稳定 plan 正向由确定性 tests 证明
- final-source UI：`PASS`；#6 processing→completed、reasoning/unknown expanded、Composer 恢复、正常 Cmd+Q 清理
- dark theme：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变
- Reduce Motion：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变
- 精确 1180×760：`WAIVED / NOT REQUIRED`；不是 PASS，未执行、无需恢复，系统设置未变

D4=`PASS` 只表示本地真实 Demo 可用，不等于 Desktop/yijie 已提交、已 push、生产可用或完整 Epic 完成。

## 1.1 Contracts source-first 验证

| 检查 | 状态 | 实际结果 |
|---|---|---|
| `pnpm generate` | PASS | 14 JSON Schema SDK sources，Go/TypeScript/OpenAPI/Protobuf/AsyncAPI 生成物一致，无 schema-name warning |
| `pnpm lint` | PASS | Redocly、Ajv、Buf、TypeScript、Go Vet 全部通过 |
| `pnpm test` | PASS | 56 tests PASS，0 fail；包含 v4 phase/plan/reasoning/artifact/version-isolation、1 MiB fail-closed 与 Runtime shape/pin checks |
| `pnpm build` | PASS | 重新生成并完成 TypeScript build |
| v1 wire equality | PASS | 对 supported `f16a497...`：Public 2 paths、Agent Host 7 paths/reference closure 相等 |
| breaking vs prior candidate | PASS | 对 `164b14f...`：OpenAPI、Protobuf、AsyncAPI、JSON Schema 无 breaking |
| breaking vs supported | PASS | 对 `f16a497...`：OpenAPI、Protobuf、AsyncAPI、JSON Schema 无 breaking |
| Runtime immutability | PASS | 固定 commit/version/schema count/digest 与 `experimentalApi=false` 全部不变；Runtime 工作树未写入 |
| immutable Contracts ref | PASS | `yijie-contracts@3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；提交后工作树 clean，未 tag/publish/push，可供 Host 精确 pin |

详细身份和边界见 `evidence/contracts-v4-source-first-candidate-2026-08-28.md`。

## 1.2 Host v4 projection 验证

| 检查 | 状态 | 实际结果 |
|---|---|---|
| exact Contracts pin | PASS | `0.6.0@3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；lock SHA-256 `c1ae8d7d363269c29a1858142c07a1c6041d9fbd394c126539e12dee767934d9` |
| `make contract-check` | PASS | OpenAPI/compatibility/v1-v4 schema/fixtures/generated DTO 与固定 generator 对账通过 |
| `go test ./... -count=1` | PASS | 所有 Host package 通过；包含 phase/plan/reasoning/15 variants、closed producer、failure policy 与配置隔离 |
| focused race | PASS | `internal/session internal/app internal/codex cmd/desktop-host` |
| `go vet ./...` | PASS | exit 0 |
| `git diff --check` | PASS | exit 0 |
| v1-v3 isolation | PASS | v4-only fields/failures 不进入旧 wire；共享 control request 保持旧 trace 语义 |
| exact local model gate | PASS | 仅 exact local/demo_fast managed provider；fixed high/raw；DynamicTools/public/production/symlink alias fail closed；`experimentalApi=false` |
| immutable Host ref | PASS | baseline `1b7bfd1c…` → initial FEAT-134 `201fd9f8…` → corrective child/final `b9358f06…`；最终工作树 clean，未 push，Desktop 精确 pin final SHA |

详细边界与独立审查修复见 `evidence/host-v4-projection-candidate-2026-08-28.md`。

## 1.3 Desktop Contract First 验证

| 检查 | 状态 | 实际结果 |
|---|---|---|
| `make lint` | PASS | exact v4 pin、ESLint、vue-tsc、cargo fmt 与 cargo clippy all-targets `-D warnings` PASS |
| terminal-repair 前 `pnpm test` | HISTORICAL PASS | 103 个 Vue/TypeScript files、833 tests；不能替代最新修复后的 full rerun |
| terminal-repair 前 `cargo test` | HISTORICAL PASS | 300 pass、3 ignored、0 fail；不能替代最新修复后的 full rerun |
| pre-final-candidate focused/full | HISTORICAL PASS | 既有 TS/Rust/DB 与 TS full/lint/build 只作过渡事实，不外推为最终 payload-v2-only candidate |
| exact flag=false isolation | PASS | `legacy_background_does_not_run_feat134_failed_turn_recovery`；background 不修复或改变 generic failed outbox + queued Turn |
| final candidate aggregate/fmt/diff | PASS | `pnpm test` 835/835；`pnpm lint/build` PASS；`cargo test` 316 passed / 3 ignored / 0 failed；`cargo fmt --all --check` 与 Desktop `git diff --check` PASS；终审无 open P0/P1/P2 |
| `pnpm tauri:build:demo-fast:stable` | PASS | #6 final-source Desktop `2026-08-29 02:02:12`、Host `02:02:39`、Runtime `02:02:40`；fresh UI smoke 与正常 Cmd+Q 清理 PASS |
| `git diff --check` / probe cleanup | PASS | Desktop diff check PASS；临时 probe 源码与 target 残留 0，Host 空 probe 目录已删除；最终 commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`、工作树 clean、未 push |
| Runtime immutability | PASS | `yijie-codex@0ce5902e…` clean；binary/manifest 匹配，未修改、升级、重编译、替换或重新 pin，`experimentalApi=false` |

## 1.4 Canonical content-free 验证

初始 `1` 次、Owner 随后明确增加的 `2` 次重试，以及前三次用尽后另外批准的 `1` 次均已消费（`4/4`）；每次均为 Owner 显式授权，不是程序自动重试。没有工具调用或 Agent 文件/项目读写，治理证据没有保存、复述或哈希 prompt、reasoning、plan、final 正文。

第三次 Host stream 保留到 sequence `87`；Desktop 初始停在 `32`，根因是 parser 错误拒绝 Contracts v3/v4 合法的空 lifecycle `text` snapshot。修复后，同一已接受 Turn 的 retained tail 仅通过生产 v4 GET/reducer/persistence 路径到达唯一 completed terminal；没有新 POST、Provider call 或 prompt。content-free 结果：non-empty raw reasoning、AgentMessage `phase=null`、plan `0/0`、notices empty、outbox done。

这证明 retained-tail production path，不证明 fresh、不间断 UI streaming。第四次失败前的旧进程曾从 SQLCipher hydration 显示 Timeline、第 1 轮和“已完成”，`loading=false`、`streaming=false`；过程记录默认折叠，并在该旧进程通过键盘展开/收起。该 disclosure 操作不作为 corrective 新进程证据。

第四次只提交了额外授权的唯一一次无敏感纯文本 Turn：Desktop Turn queued 后 outbox=`failed`、`attempt_count=1`、`runtime_turn_id` 为空，0 events/items/notices/terminal，cursor 未前进；Host idle 且 `failure_code=turn_start_failed`；Provider 与 Runtime Turn 均未启动。直接持久证据最深只到 `turn_start_failed`；thread-not-found 是由 `22:22` 新 bundle/Runtime 对比 `18:55` 历史 thread，以及旧纯文本 v1 无 resume、Runtime `turn/start` 仅读取进程内 thread manager 的确定性路径得到的高置信推断，不是直接错误日志。

最终 Desktop-only recovery 仅适用于 exact-local payload v2；v1 exact-local/legacy 不变。pre-POST matching Active 按 provenance 分支：claimed `attempt_count==1` 必定不是当前 operation，保持 inflight/queued/runtime NULL、发布 `TurnReconciliationRequired` 且 0 次新 POST；只有 `attempt_count>1` crash-reclaim 才绑定既有 runtime Turn且 0 次新 POST。post-error matching Active 因本调用已 POST 同 operation 而直接绑定。confirmed `turn_start_failed` 才终态化；identity mismatch/non-idle/Err suspend且不伪造 failed。unknown payload version 保持 generic fail。不修改 Vue、Contracts、Host、Runtime、public/production。

最终源码正常退出/清理旧构建后完成 v4 pin、stable debug rebuild 与 `00:34:04/00:34:30/00:34:30` no-prompt startup。最新 AX 只登记 content-free facts：controls 均 present，queued `0`、streaming `0`、completed `2`、stopped `1`、failed `2`、updated `1`；未点击历史正文。这只是 startup/state smoke，不是 fresh corrected successful Turn。不保存、引用、复述任何 prompt/reasoning/plan/final 正文、raw AX 或截图。dark theme、Reduce Motion 与精确 `1180×760` 已由 Owner 设为 `WAIVED / NOT REQUIRED`。详见 `evidence/canonical-v4-content-free-2026-08-28.md`。

上述为历史阶段。#5（首次 finalized-content P2 修复源码）进程为 Desktop `01:49:09`、Host `01:49:34`、Runtime `01:49:35`；持久化 metadata 为 attempts=`1`、outbox=`done`、completed、terminal=`1`、v4 events=`187`、reasoning item/part=`1/1`、plan update/step=`0/0`、phase=`null`，并完成 light、200% zoom、键盘 PASS。

#5 后发现并修复 native 接受 repeated finalized lifecycle、但 `TimelineDelta::Ignored` 未跨 WebView 导致 TS fail-closed 的跨层 P2。#6 final-source 进程为 Desktop `02:02:12`、Host `02:02:39`、Runtime `02:02:40`，fresh task content-free ID `01a0498a-5574-7cf2-9652-14f47b6db9d4`；UI 观察 processing→completed、reasoning/unknown expanded、Composer 恢复，并正常 Cmd+Q 清理。#6 未另取 DB counts，不能继承 #5 的 `187`。全部记录均不含任何正文或正文哈希。

## 2. D0 治理检查

| 检查 | 状态 | 实际结果 |
|---|---|---|
| strict D0 / schema v3 / demo_fast / local | PASS | `check-feature-package.sh --strict --gate D0` exit 0：文档结构、占位符、D0 范围与 schema v3 语义门禁通过 |
| Product/UX fields | PASS | 用户、问题、结果、in/out scope、完整主流程、视觉方向与 idle/loading/success/empty/error/retry/cancel 已定义 |
| Must AC | PASS | 8 条 AC 已定义并在 D4 由 contract/Host/Desktop tests、#5 metadata 与 #6 final-source UI 组合证明 |
| Contract First | PASS | `semantic + expand + durable`，明确 Runtime→Contracts→Host→Desktop authority 和停止条件 |
| Reference policy | PASS | 继承 owner-approved inference；撤回人工材料不进入 provenance |
| Owner exclusions | PASS | 八项 intentional product difference 全部保留，包含 CAP-022 / GS-006 |
| External authorization | PASS | 历史 tranche `4/4`，当前 tranche `6/7`、剩 1，Feature 累计 `10/11`；destructive/production 均为 `false / 0` |
| dark theme | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| Reduce Motion | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| 精确 1180×760 | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| Claims audit | PASS | direct `--audit-claims` exit 0；D0 与 D4 已声明事实均通过 schema v3 语义审计 |
| Governance diff audit | PASS | `pnpm feature:audit -- --base-ref 9a8f1d7...` exit 0，扫描 13 个 Feature Package；5 条 legacy v1 historical-only warning 与 FEAT-134 无关 |

辅助治理检查：

| 命令 | 状态 | 实际结果 |
|---|---|---|
| `pnpm lint` | PASS | 10 个 repository manifest entry 与 central Contract First governance / sibling AGENTS 对账通过 |
| `pnpm test` | PASS | 48 tests PASS，0 fail，包含 schema v3 D0/D4、claims audit、repository audit 与 shell entrypoint tests |
| `bash -n scripts/*.sh` | PASS | exit 0，无 Shell syntax error |
| FEAT-134 placeholder/whitespace scan | PASS | 模板占位标记与 trailing whitespace 无匹配；`rg` exit 1 表示零匹配 |

## 3. 工作区与分支验证

### 3.1 Clean-start

在创建分支前，对 11 个 sibling repo 执行 `git status --short --branch` 与 `git rev-parse HEAD`。所有仓库均无 staged、unstaged 或 untracked 文件；精确事实记录于：

- `evidence/workspace-isolation-baseline-2026-08-28.md`

### 3.2 分支创建

| 仓库 | 结果 | baseline |
|---|---|---|
| `yijie` | PASS | `9a8f1d7b49a9b362c03085740f6f8f75c67d5cf7` |
| `yijie-desktop` | PASS | `af38353694c3eb045365b7f3450ffc8a95aaf8a1` |
| `yijie-contracts` | PASS（审计证明后创建） | `164b14f609537d727a52326832da04430aecc4ab` |
| `yijie-agent-host` | PASS（审计证明后创建） | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` |

四仓分支名均为：

`feat/feat-134-desktop-streaming-progress-final-response`

创建后四仓均从 clean baseline 开始。当前 Contracts v4 已提交为 `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`，Host v4 已提交为 `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`，两仓工作树均 clean；Desktop 从 clean baseline 进入实现，`yijie` 仅有本 Feature 治理目录。没有 push。

## 4. 只读 Contract First 审计

详细矩阵：`evidence/contract-first-capability-matrix-2026-08-28.md`

### 4.1 已验证存在

- 固定 Runtime stable schema 中存在 AgentMessage lifecycle phase 和稳定 `turn/plan/updated`。
- Contracts v1 有 Assistant delta、Item lifecycle、Turn lifecycle、error/warning。
- Contracts v2/v3 有 raw reasoning delta/finalized 和 complete/incomplete/unavailable reason model。
- Host 能投影 v1 lifecycle/delta、v2 raw reasoning，并提供 sequence/event_id/process-local replay。
- FEAT-132 reducer 有按 itemId/block index 的通用 delta 模型、dedupe、sequence/gap 与 authoritative finalBlocks reconciliation 能力。
- FEAT-133 Timeline 已有最终回答、过程 disclosure、notice、安全内容、状态和可访问展示基础。
- Desktop SQLCipher 是对话历史 authority；Host replay 不是 durable history。

### 4.2 已验证缺口

- Current Contracts/Host 没有 AgentMessage phase，commentary/final 不能可靠区分。
- Current Contracts/Host 没有稳定 `turn/plan/updated` projection。
- Runtime schema 允许 AgentMessage phase 为 `null`，provider 不保证稳定产生；即使完成 vNext，仍不能把 null 或 turn terminal 推断为 final。
- Runtime schema 存在 stable plan event 不等于 current provider 会发送；没有 canonical event-shape evidence 时只能支持 absence/no-fake-step。
- compatibility manifest 未锁定 reasoning notification；canonical Host 默认关闭 raw reasoning，managed provider 也未产生可用正文。
- Desktop production live assistant 固定为单 identity，WebView wire 丢失 Item started/completed 和 phase；Turn terminal 一次性封口 Item。
- Desktop snapshot adapter 在没有 reasoning Item 时丢失 Thread 级 unavailable/incomplete metadata。
- error/warning 在 Desktop live projection 被忽略；warning 又只有 thread scope，不能猜 Turn。
- Host replay 仅进程内短窗，无法承担跨重启补回未观察事件的承诺。

### 4.3 分支必要性判定

`PASS`：审计证明如果保留 AC-002 / CAP-010 / CAP-012，必须建立 Contracts 与 Host 的 FEAT-134 分支。仅靠 Desktop 会违反 Contract First 并诱发页面推断。Contracts/Host 分支已按 Owner 条件授权创建；没有修改文件。

## 5. Runtime 不变性

| 项目 | 审计事实 |
|---|---|
| repo/commit | `yijie-codex@0ce5902ed400866be0196886bb78f693a004d68d` |
| upstream | `rust-v0.144.6@5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| schema tree | 267 files / `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` |
| mode | stdio / `experimentalApi=false` |
| D0 result | 没有创建 Runtime 分支，没有写入、构建、替换、同步或 pin 变化 |

## 6. 安全与授权核对

| 项目 | 状态 | 说明 |
|---|---|---|
| FEAT-134 real prompt | AUTHORIZED / CONSUMED | 初始 1 次、Owner 明确增加 2 次重试及额外 1 次，消费 `4/4`；新增 Turn 需新授权 |
| Provider/paid call | AUTHORIZED / CONSUMED | 四次均为无敏感纯文本验证、非程序自动重试；第四次只提交一次且在 Provider 前失败；历史 FEAT-131/132 授权不可转移 |
| destructive operation | NOT AUTHORIZED | `allowed=false / max_actions=0` |
| production write/public release | NOT AUTHORIZED | local demo only |
| 强杀/故障注入 | NOT RUN | 用户级长期安全条款禁止 |
| 权限破坏/binary 替换 | NOT RUN | 用户级长期安全条款禁止 |
| 恶意/攻击 fixture | NOT RUN | 用户级长期安全条款禁止 |

后续代表性失败验证使用正常、非破坏性的 deterministic state fixture。若某项验收只能依赖禁止行为，必须记录未执行项、原因和影响，不能伪造通过。

## 7. 实现与 D4 验证状态

| 活动 | 状态 | 原因与影响 |
|---|---|---|
| Contracts v4 schema/fixtures/tests | PASS | 0.6.0 candidate source/generated/56 tests 与双基线检查通过；immutable commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` 已形成，可供 Host 精确 pin |
| canonical raw-reasoning producer | PASS | #5 reasoning item/part=`1/1`；#6 final-source UI reasoning expanded |
| canonical phase/plan producer | PASS（negative/absence） | phase=`null` 合法 unknown、plan=`0/0` 不伪造；显式 final_answer/plan 正向由确定性 tests 证明 |
| Host mapper/version negotiation/pin | PASS | 线性历史 `1b7bfd… -> 201fd9… -> b9358f…`；final authority 全量门禁 PASS |
| Desktop IPC/domain/DB/Timeline | PASS / COMMITTED | 跨层 repeated-finalized P2 已修复；TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff PASS；immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`、clean、未 push |
| Host/Desktop unit/integration/full tests | PASS | Host immutable authority gates PASS；Desktop final aggregate 835 TS / 316 Rust + 3 ignored，review 无 open P0/P1/P2 |
| canonical startup | PASS | #6 final-source `02:02:12/02:02:39/02:02:40`，zero-login、UI smoke 与正常清理 PASS |
| real streaming prompt | PASS | 历史 4/4 + 当前 6/7；#5 metadata 与 #6 final-source UI 各自提供不混用的 content-free 证据 |
| real reasoning | PASS | #5 raw reasoning item/part=1/1，#6 reasoning expanded；不保存正文或哈希 |
| interrupted/failed live | NOT RUN | Stop action 属于 FEAT-139，且禁止强杀/故障注入 |
| light/200%/keyboard | PASS | #5 canonical 完成三项基线 |
| dark theme | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| Reduce Motion | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| exact 1180×760 | WAIVED / NOT REQUIRED | 不是 PASS，未执行、无需恢复，系统设置未变 |
| D4 strict/claims/diff | PASS | strict D4 与 direct claims exit 0；Desktop commit 已回填，`yijie` 治理包仍未提交，diff review PASS |

## 8. 计划中的安全验证顺序

0. `COMPLETED / CONSUMED 10/11`：历史 tranche `4/4`、当前 tranche `6/7`，剩余 `1`；没有自动重试。
1. Contracts vNext schema、compatibility、OpenAPI/protobuf/JSON Schema、positive/negative fixtures。
2. `COMPLETED / COMMITTED`：Host mapper、version negotiation、item lifecycle/phase/plan/reasoning、sequence/replay、failure policy 和 pin 一致性；immutable commit `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`，只允许已批准的 local fixed high/raw。
3. `COMPLETED / COMMITTED`：Desktop private parser、FEAT-132 ConversationState、reconciliation、SQLCipher migration/hydration、FEAT-133 Timeline 与跨层 P2 修复已提交为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`；clean、未 push。
4. `PASS`：Desktop TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff 与终审。
5. `PASS`：#5 持久化 metadata/light/200%/键盘，#6 final-source UI/Composer/正常清理；证据不混用。
6. `WAIVED / NOT REQUIRED`：dark theme、Reduce Motion 与精确 1180×760 逐项移出门禁；不执行、不恢复、不写 PASS。
7. `D4 PASS`：本地真实 Demo 可用；Desktop/yijie 仓库提交与 push 仍未执行，需 Owner 授权。

## 9. D0 Artifact

- `feature.yaml`
- `00-feature-brief.md`
- `01-delivery-log.md`
- `02-verification.md`
- `evidence/workspace-isolation-baseline-2026-08-28.md`
- `evidence/contract-first-capability-matrix-2026-08-28.md`
- `evidence/contracts-v4-source-first-candidate-2026-08-28.md`
- `evidence/host-v4-projection-candidate-2026-08-28.md`
- `evidence/canonical-v4-content-free-2026-08-28.md`

这些是 Yijie 本地治理 Artifact，不是 Codex Desktop reference evidence。
