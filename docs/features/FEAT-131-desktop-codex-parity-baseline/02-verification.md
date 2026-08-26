# FEAT-131 Demo 验证

> Verification status: `PARTIAL`
> Automated verification time: `2026-08-26T13:07:39+08:00`
> D4 status: `BLOCKED`；当前隔离 canonical startup 已 PASS，但当前 entry 的 real smoke 因授权额度已用而 NOT RUN；版本专属 Codex Desktop UI 参考证据仍待人工补采。

## 1. Focused 与全量检查

| Repository/CWD | Command | Exit | Result | 真实结果 |
|---|---|---:|---|---|
| yijie | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-131-desktop-codex-parity-baseline` | 0 | PASS | D0 direct package gate PASS；最终文档更新后复验 |
| yijie | `pnpm lint && pnpm test` | 0 | PASS | lint PASS；48 tests PASS |
| yijie | `pnpm feature:audit` | 0 | PASS | 已提交 Feature packages 通过并保留既有 legacy warning；当前未跟踪 FEAT-131 由 direct D0 gate 验证 |
| yijie-desktop | `pnpm exec vitest run tests/feat-131/chat-event-replay-harness.test.ts scripts/check-feat131-replay-boundary.test.mjs` | 0 | PASS | 2 files / 41 tests PASS |
| yijie-desktop | launcher/config + consumer pin focused checks | 0 | PASS | launcher/contract 2 files / 11 tests PASS；`pnpm generate:check` 确认 10 pins complete；Rust `cargo check` 与 owner-only key-file 正向 focused test 1/1 PASS |
| yijie-desktop | `make lint` | 0 | PASS | generate check、ESLint、Vue TypeScript、Cargo fmt 与 Clippy PASS |
| yijie-desktop | predecessor revision `make test` | 0 | HISTORICAL PASS | stable identity/isolation 最终增量之前：frontend 75 files / 594 tests；Rust 265 passed / 3 ignored。最终增量后不再执行包含权限/故障负向 fixture 的整套 Rust tests，改用安全编译/focused/build 验证 |
| yijie-desktop | current stable build + final dist boundary scan | 0 | PASS | `tauri:build:demo-fast:stable` 与 production build PASS；仅有既有 >500 kB chunk warning；30 个 production 文件无 fixture/harness canary |
| yijie-codex + yijie-contracts | repository-owned schema hash、HEAD/status 与 manifest SHA-256 对账 | 0 | PASS | Runtime HEAD/worktree/267 schemas/tree hash和 compatibility manifest 与实施前精确一致 |

predecessor revision 的一次完整测试中，既有 `YjChartCard` observer 时序断言偶发失败；该文件与 FEAT-131 无依赖，单文件有界复跑 3/3 PASS，随后当时完整 `make test` PASS，未修改无关代码。最终 stable isolation 增量由当前 focused Vitest、`cargo check`、安全正向 Rust test、stable build 和 dist scan 绑定；没有为追求全绿去执行权限破坏或故障注入测试。

## 2. Canonical 启动、真实 Smoke 与正常退出

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | `pnpm tauri:demo-fast:stable` → `/readyz` → `/v1/status` | isolated `com.yijie.ai.feat131-stable` + `.local/feat131-stable` | 最终代码 freshly built `易界 AI FEAT-131.app`；两次均 `/readyz=ready`，status 为 Runtime `0.144.6`、MiniMax-M3、`experimental_api=false`；安全 UI 自动化可读取 | PASS |
| Current real happy path | 当前隔离 App 只验证 startup/status，不打开项目、不提交 prompt | isolated canonical + fixed Runtime + MiniMax text Provider | 用户批准的一次额度已被 predecessor submission 保守记作使用；当前 entry 不再发送，故 `NOT RUN` | NOT RUN |
| Predecessor submission observation | 旧 `com.yijie.ai` entry 只提交一次已批准固定 prompt；不重试 | predecessor app/data + fixed Runtime + MiniMax | 本地会话与用户消息出现，但一直 queued/“状态已更新”；无 streaming/assistant/terminal。聚合为 `thread_started=0`、`turn_started=0`、`assistant_delta=0`、`turn_completed=0`，是 pre-Runtime failure，不是当前 canonical real smoke | FAIL |
| Representative failure/retry | safe GS-012 resync 与 GS-013 sequence-gap replay；真实服务只允许正常 lifecycle | test-only memory transport + predecessor observation | synthetic raw events 已通过生产 parser/store；predecessor submission 停在 Host session/Runtime thread 绑定前，未自动重试或恢复，不能升级为 real-runtime recovery PASS | PARTIAL |
| Normal shutdown | App 自身 `Cmd-Q`，随后检查端口与 owned processes | current isolated canonical App | 当前代码两次均 App、Host、Runtime 正常退出；18081/1420 释放；无 owned process 残留。只证明正常路径，未用故障注入验证 Host latent fallback | PASS |

### 2.1 Canonical 入口

```bash
cd ../yijie-desktop
pnpm tauri:demo-fast:stable
```

该入口是 `demo_fast` 的隔离 stable 验证入口：

1. 只接受精确参数 `--stable-api-only`，非法或多余参数在 preflight 前 fail closed；
2. 清除 ambient Provider、direct key/key-file 与图片开关，再设置固定 MiniMax Provider、owner-only key file 和 image dynamic tool disabled；
3. freshly build `com.yijie.ai.feat131-stable` / `易界 AI FEAT-131.app`，使用独立 Desktop app-data 与 `.local/feat131-stable` Host/Codex home；
4. stable-only second instance 非零 fail closed；默认 `pnpm tauri:dev`/`pnpm tauri:demo-fast` 的命令、图片模式、数据根与第二实例 `return` 行为保持不变；
5. stable Desktop supervisor 不使用 `kill_on_drop/start_kill`；但未修改 Host，其 Runtime Manager 仍有 timeout/protocol/startup failure `Process.Kill()` fallback，且 Desktop exit callback 不把 cleanup-incomplete 传播为 launcher 非零状态。因此异常路径必须报告限制，不能宣称整链保证。

### 2.2 单次真实 submission 的证据边界

- 用户明确批准最多 1 次 Provider/模型调用；predecessor entry 实际只点击一次“发送任务”，失败后没有重试，当前隔离 entry 未发送。
- Runtime 聚合没有 thread/turn/delta/terminal 事件，因此没有证据确认请求到达 Runtime 或 Provider，也不能确认是否产生计费；不能据此断言 Provider 侧绝对没有收到任何请求。
- UI 截图包含侧栏既有会话标题，未作为证据复制或提交，避免泄露用户数据。
- predecessor 本地待发送会话没有被删除或篡改。它可能在 default `com.yijie.ai` 正常启动时依据既有 outbox 行为恢复；再次启动默认入口前应由 Owner 决定。当前 canonical identity/data roots 与之隔离。

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | PASS | `references/codex-desktop-build-metadata.md` 精确记录 version/build/freeze time/environment；无法自动读取的 UI 字段明确为 `reference-unobserved` |
| AC-002 | PASS | `03-capability-matrix.md` + `references/runtime-freeze-evidence.md`；fork/upstream/version/schema/experimentalApi 精确冻结 |
| AC-003 | PASS | `04-golden-scenarios.md` 与 `scenario-catalog.json` 包含 `GS-001`–`GS-013`；replayed/covered variants 精确绑定 |
| AC-004 | PASS | 31 项 `CAP-*` 仅使用四类 primary classification，并记录 delivery lane、blocker 与 Owner Feature |
| AC-005 | PASS | fail-closed fixture parser 与 34 个完整-fixture negative canaries 覆盖路径、身份、凭据、prompt 与商家字段 |
| AC-006 | PASS | 真实 Desktop parser/store replay 可重复；production build 后 30 文件 boundary scan PASS |
| AC-007 | PASS | drift test 保留 26.818.61809/7019 frozen baseline；禁止静默覆盖 |
| AC-008 | PASS | Runtime 实施前后 HEAD、clean status、267 schema、tree SHA-256 与 Contracts manifest SHA-256 精确一致 |
| AC-009 | PASS（收窄边界） | 隔离 config/launcher、stable-only second-instance、Provider/Desktop-cleanup focused checks + 当前 `/v1/status` + `com.yijie.ai.feat131-stable` 正常启动/Cmd-Q；明确不包含 Host Runtime fallback 保证 |

这些 AC 证明 FEAT-131 基线资产和 stable canonical 入口已经实现；它们不替代 real happy path、人工参考证据和 Owner freeze，因此 D4 仍不通过。

## 4. 参考证据与 UI 结果

- Yijie 生产 Chat UI：本 Feature 无修改；这次 Yijie App smoke 不是 Codex Desktop 参考证据。
- Codex Desktop 版本专属截图/录屏：Computer Use 安全边界拒绝读取当前 Codex App；未用系统截图或其它旁路绕过。人工采集要求见 `references/manual-capture-checklist.md`。
- Test-only replay：GS-001 streaming/completed、GS-012 resync/recovery、GS-013 sequence-gap/missing-delta recovery 为 `synthetic: PASS`。
- Real-runtime：当前 canonical GS-001 `NOT RUN`；predecessor submission 在 Runtime 前失败，只登记为 pre-runtime observation。其余真实场景保持 `NOT RUN`、`PARTIAL` 或 `BLOCKED`。
- Runtime：严格只读；没有 fetch/pull/rebase/build/generate/edit/replace。

## 5. Diff、契约与边界

- `yijie`：新增 FEAT-131 Feature package。
- `yijie-desktop`：新增 test-only fixture/harness/boundary scanner；新增隔离 stable launcher/config/identity/data roots；新增 stable-only second-instance fail-closed 分支；Sidecar 解耦既有 MiniMax 文本 Provider 与图片 dynamic tool，并收窄 Desktop supervisor cleanup；刷新 Sidecar 与 `lib.rs` Desktop-local consumer pins。
- `yijie-codex`：保持 `develop@0ce5902ed400866be0196886bb78f693a004d68d` clean，并有意保持落后 `origin/develop` 1 commit。
- `yijie-contracts` 与 `yijie-agent-host` repository：无修改；公共 wire/Host API/Runtime schema 无变化。
- `contract-impact=additive` 仅指 Desktop-local closed launcher/config/identity、stable-only instance 分支、既有 Provider/Desktop cleanup 投影和 consumer pins；不把 fixture 或实现扩展提升为公共契约。
- 独立增量复审无 P0，但因 Host Runtime 强制 fallback 与 cleanup-incomplete 不向 launcher 传播而保持 `PARTIAL`；发现项在 `feature.yaml.verification.diff_review` 如实保留。

## 6. D4 与结论

- D0 package、实现、current focused/compile/build、Runtime freeze：PASS；predecessor full test 历史 PASS 不冒充最终增量的 full-suite 绑定。
- Canonical stable startup / `experimental_api=false`：PASS。
- Current canonical real happy path：NOT RUN；授权已由 predecessor submission 使用。predecessor failure 位于本地事务之后、成功 Host session/Runtime thread 绑定之前；本 Feature不越界修改生产 orchestration。
- Codex Desktop version-specific reference evidence：`reference-unobserved`，待人工采集。
- Representative real failure/recovery：PARTIAL。
- 当前 Feature：`active` / verification `PARTIAL`；D4 `BLOCKED`，不得宣称 baseline 已由 Owner 冻结。
- 最终实际执行 D4 validator，exit 1；精确拒绝项为 `feature.status must be usable for D4`、`verification.status must be PASS for D4`、`verification.real_smoke.status must be PASS`、`verification.representative_failure.status must be PASS`、`verification.diff_review.status must be PASS`。没有把预期拒绝改写为 PASS。
- Exposure 为 `local`，DP/public readiness 不适用；未 commit、push、tag、merge、发布或部署。
