# FEAT-131 Demo 验证

> Verification status：`PASS`
>
> Reference policy：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`
>
> Final verification time：`2026-08-27T01:38:36+08:00`
>
> D4 status：`PASS`。Current canonical real smoke、非破坏性代表性失败/恢复检查与独立 scoped diff review 均已完成；人工参考证据已被 Owner 取消，不是 gate。该结论保持 2026-08-27 历史验证事实，不因后续范围调整而重写。
>
> Scope amendment：`2026-08-29`。Owner 正式取消/排除 FEAT-138；完整 Epic 后续只需 active FEAT-132–137、FEAT-139–143 实现。此范围修订不代表重新执行 FEAT-131 D4，也不改变原 PASS 证据。
>
> Governance rebaseline：`2026-08-30`。Owner 将 FEAT-136 收口到 evidence-backed Command Must，并新增 FEAT-144 承接 CAP-017 / GS-004；当前 active 范围为 FEAT-131–137、FEAT-139–144。Owner-authorized minimal Runtime repair 后 final re-freeze 为 `b2b20e2…` / 0.144.6。该更新只同步 matrix/scenarios/evidence，不重跑或改写 2026-08-27 FEAT-131 D4。

## 1. 自动化与静态检查

| Repository/CWD | Command | Result | 真实结果 |
|---|---|---|---|
| yijie | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-131-desktop-codex-parity-baseline` | PASS | schema v3 与 D0 文档/语义门禁 PASS |
| yijie | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D4 docs/features/FEAT-131-desktop-codex-parity-baseline` | PASS | schema v3 与 D4 local real-service/document 语义门禁 PASS |
| yijie | `pnpm lint && pnpm test` | PASS | manifest/Contract governance lint PASS；48 tests PASS |
| yijie-desktop | `pnpm exec vitest run tests/feat-131/chat-event-replay-harness.test.ts scripts/check-feat131-replay-boundary.test.mjs` | PASS | 2 files / 41 tests PASS；policy ID、GS-006 exclusion、parser/store 与 scanner fail-closed 行为已验证 |
| yijie-desktop | targeted ESLint + `pnpm exec vue-tsc --noEmit` | PASS | FEAT-131 harness/test/scanner lint PASS；Vue TypeScript PASS |
| yijie-desktop | `pnpm build && node scripts/check-feat131-replay-boundary.mjs --dist dist` | PASS | production build PASS（仅既有大 chunk warning）；fresh dist 35 files 无 replay/fixture/policy canary |
| yijie-codex + yijie-contracts | HEAD/status、267 schema、tree SHA-256 与 manifest SHA-256 只读对账 | PASS | Runtime/Contracts HEAD clean 且所有固定 hash 精确匹配；未执行 fetch/pull/rebase/build/generate/edit/replace |
| yijie-codex diagnostic | `python3 scripts/check_agent_host_contracts.py` | FAIL（已记录，不归因本改动） | Runtime-side checker 预期的 Host projection 少于未变化 Contracts manifest 中的 skills surface；属于既有 checker/manifest expectation mismatch，详见 `references/runtime-freeze-evidence.md` |

历史实现阶段已通过 launcher/config、`pnpm generate:check`、Rust compile/focused positive test 和 canonical startup；本次 reference policy schema 已按本节重新验证。额外 Runtime diagnostic 的既有 mismatch 不允许通过修改固定 Runtime 来消除，也没有被伪装成 PASS。

## 2. Canonical 启动、真实 Smoke 与正常退出

| Check | Environment/steps | Actual result | Result |
|---|---|---|---|
| Startup/readiness | `pnpm tauri:demo-fast:stable`；isolated `com.yijie.ai.feat131-stable` + `.local/feat131-stable` | 从 clean detached HEAD freshly built；`/readyz=ready`，Runtime `0.144.6`、MiniMax-M3、`experimental_api=false`；正常 `Cmd-Q` 后 App/Host/Runtime 退出且 18081/1420 释放 | PASS |
| Current real happy path | canonical stable App 在 clean detached worktree 提交一次安全纯文本 prompt：禁止工具/文件读写且只允许精确单行输出 | UI Turn 到达“已完成”，模型精确返回 `FEAT-131_SMOKE_OK`，Composer 恢复可发送；没有工具调用、文件读取/修改或重试；完成后 `/v1/status` 仍为 ready/`experimental_api=false` | PASS |
| Predecessor submission | 旧入口只提交一次，失败不重试 | 本地出现用户消息，但 Runtime 聚合为 thread/turn/delta/terminal 均未观察到；只能记为 pre-runtime failure，未确认 Provider 调用或计费 | FAIL（非 current smoke） |
| Representative failure/retry | 首实例 ready 时直接启动同一 stable bundle 的第二实例；核对 fail-closed 与首实例健康；正常退出首实例后从 canonical 入口重启 | 第二实例立即 exit 1 并只输出 `yijie desktop instance is already running`；首实例仍 ready/`experimental_api=false`；退出后 canonical retry/restart 再次 ready，最终正常退出且端口/owned processes 清空 | PASS（real-service safe path） |
| Supplemental recovery/boundary | safe GS-012 resync/recovered、GS-013 sequence-gap/missing-delta replay，以及 legacy/policy production-boundary canary | synthetic raw events 经真实 parser/store 正确收敛；v1、v2、旧 version/build 与 policy canary 均 fail closed | PASS（synthetic，未冒充 real-service） |
| Normal shutdown | App 自身 `Cmd-Q`，随后检查端口和 owned processes | 正常路径 PASS；未通过故障注入验证 Host latent fallback | PASS |

Canonical 入口：

```bash
cd ../yijie-desktop
pnpm tauri:demo-fast:stable
```

该入口只接受精确 `--stable-api-only`，使用独立 bundle/app-data/Host home，保留 MiniMax 文本 Provider，关闭图片 dynamic tool，并以 `experimentalApi=false` 初始化固定 Runtime。stable-only second instance 非零 fail closed。Desktop supervisor 正常路径不使用 `kill_on_drop/start_kill`；Host 内部 Runtime fallback 不在 AC-009 PASS 边界内。

本次 Owner 允许首次请求失败后最多重试两次；仓库治理另有“真实模型最多 2 次短请求”的更严格总上限。predecessor 已保守计作第 1 次，因此 current canonical 只执行第 2 次，且首轮即成功，没有使用重试。该上限现已耗尽，不再发送付费请求。

代表性失败 PASS 来自真实 canonical service 的 stable-only second-instance fail-closed 与随后正常 retry/restart；synthetic parser/store recovery 和 production boundary 只作为补充，不替代 real-service 结果。依据长期安全条款，没有执行强杀、进程故障注入、权限破坏、binary 替换或攻击 fixture；因此没有验证 Host shutdown timeout/protocol failure/startup abort 的异常 cleanup，影响是不能宣称整条 App→Host→Runtime 异常清理保证。

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | PASS | `references/reference-inference-policy.md`、brief、matrix 和 scenario index 固定近似策略、撤回人工材料及 8 项主动排除 |
| AC-002 | PASS | `03-capability-matrix.md` + `references/runtime-freeze-evidence.md` 精确固定 fork/upstream/version/schema/`experimentalApi=false`；另行披露 unchanged checker/manifest expectation mismatch |
| AC-003 | PASS | `04-golden-scenarios.md` 与 `scenario-catalog.json` 保留 `GS-001`–`GS-013`；GS-006 是无 fixture 的 owner exclusion 哨兵 |
| AC-004 | PASS | 38 项 `CAP-*` 使用四类 primary classification；CAP-022 和原 7 项排除均为 `intentional product difference` |
| AC-005 | PASS | fixture provenance 只表示 `synthetic`/`real-runtime`；design basis 通过 policy ID 单独表达；敏感数据 parser fail closed |
| AC-006 | PASS | replay 走真实 Desktop parser/store；production boundary scanner 阻止 test-only 资产进入 bundle |
| AC-007 | PASS | 旧媒体副本及派生记录已删除；catalog/harness 不包含 Codex App version/build、UI Freeze、drift 或补采要求 |
| AC-008 | PASS | 固定 Runtime 与 Contracts checkout 均 clean；HEAD、267 schema、tree hash 与 manifest hash 前后精确一致；可选 compatibility diagnostic 的既有 mismatch 不被当作 drift |
| AC-009 | PASS（收窄边界） | 隔离 stable launcher/config、Provider 与图片开关解耦、`experimentalApi=false` status、正常 startup/`Cmd-Q`；不包含 Host Runtime fallback 保证 |

这些 AC、current real happy path、安全代表性失败/恢复与最终 scoped diff review 共同满足 FEAT-131 的 D4；它们不代表后续生产交互 Feature 或完整 Epic 已完成。

## 4. 参考策略与 UI 结果

- 不采集、不保存、不索引 Codex Desktop 人工截图、录屏、App version/build 或 UI Freeze。此前提供的全部人工材料已撤回，仓库副本和派生记录已删除，任何内容或观察结论都不再参与实现与验收。
- 后续 UI 只需达到 Codex-inspired、信息层级清楚、状态与动作可理解，并符合 Yijie UI 规范；不要求一模一样或逐像素一致。
- `owner-approved-inference` 是设计依据，不是 `real-runtime`、视觉实测或版本专属事实。
- Test-only replay 当前覆盖 GS-001 streaming/completed、GS-012 resync/recovery、GS-013 sequence-gap/missing-delta recovery；只能按实际结果标为 `synthetic`。
- GS-006 File modification & Diff 是 `owner-excluded`：不实现 FileChange/Diff UI、FileChange approval、fixture 或真实验收；既有 Artifact 仍是独立能力，不得包装成 Diff。
- 其余主动排除：语音、模型版本信息、模型推理强度信息、分享、切换置顶摘要、显示侧边面板、分支到新聊天。模型推理强度信息不等于 CAP-011 的用户可见 reasoning summary。
- `yijie-codex` 全程只读；没有升级、修改、重编译、重生成或替换。

## 5. Diff、契约与边界

- `yijie`：FEAT-131 文档与治理基线。
- `yijie-desktop`：test-only fixture/harness/boundary scanner，以及既有隔离 stable launcher/config/identity/data roots。
- `yijie-codex`（2026-08-27 FEAT-131 D4 historical）：当时固定 `develop@0ce5902ed400866be0196886bb78f693a004d68d` 并保持 clean。当前 final re-freeze `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` 的来源与对账见 `03-capability-matrix.md` / `05-reference-evidence-index.md` / FEAT-136，不把后续修复倒写为原 D4 事实。
- `yijie-contracts` 与 `yijie-agent-host` repository：无修改；公共 wire/Host API/Runtime schema 无变化。
- 本次从 UI Freeze 改为 reference policy ID 只改变治理与 test-only metadata，不新增生产行为或公共契约。
- 独立复审先发现 boundary scanner 未覆盖 legacy v1/version/build canary 的 P2；修复后 v1、v2、旧 version/build 与当前 policy canary 均被拒绝，focused 41 tests、35-file dist scan 与 `git diff --check` PASS。
- 最终 FEAT-131 scoped code/test diff 无 P0–P3，diff review `PASS`。并行 FEAT-150/Store 工作明确排除且未触碰；Host Runtime fallback 与 cleanup-incomplete 传播是既有、范围外限制，不计为本 Feature diff finding。

## 6. D4 与结论

- D0 package、scope amendment focused tests、production boundary、Runtime/Contracts 静态对账：PASS。
- Canonical stable startup / `experimental_api=false`：PASS。
- Current canonical real happy path：PASS；精确返回 `FEAT-131_SMOKE_OK`，无工具调用、无重试。predecessor failure 仍单独保留，不冒充成功证据。
- 人工参考证据：`not required`，不是 D4 gate。
- Representative failure/retry：PASS（real-service safe second-instance fail-closed + canonical restart）；Host 异常进程 failure injection `NOT RUN`，原因与影响已披露。
- Diff review：PASS；FEAT-131 scoped diff 无 P0–P3。
- 当前 Feature：`usable` / verification `PASS`；D4 `PASS`。
- Exposure 为 `local`，DP/public readiness 不适用；本轮 scope amendment/verification 未新增 commit、push、tag、merge、发布或部署。
