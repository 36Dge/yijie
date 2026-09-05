# FEAT-131 整体实现与调试记录

> 当前范围修订（2026-09-05）：FEAT-137 已由 Owner 永久终止且未完成验收，未来不重启。CAP-019 / GS-005 为 `owner-terminated-unaccepted`，不再属于 active 交付范围；现行 active 范围排除 FEAT-137/138。下文旧 active 范围及 FEAT-137 source PASS 为历史记录，不构成审批可用或 D4 PASS。最终权威见 [FEAT-137 永久终止记录](../FEAT-137-desktop-approval-interaction/03-termination.md)。

## 1. 整体实现方案

- 参考策略：固定 `codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`。后续 Feature 依据 Owner 范围、Yijie UI 规范、固定 Runtime/Host 能力和工程判断实现 Codex 风格近似体验，不追求版本专属或逐像素一致。
- 事实链：固定 `yijie-codex` manifest/schema → `yijie-contracts` compatibility manifest → 当前 Host mapper → Desktop strict wire parser/store → test-only replay snapshot。
- 跨层顺序：固定 Runtime 身份与产品范围 → 建矩阵/场景 → 落 test-only fixture/harness → 做敏感数据与 production bundle 隔离 → focused/full/build → canonical local smoke → Runtime 前后对账。
- Contract First：`contract-impact=additive`；不创建或变更公共 wire schema。增量只包含 Desktop-local closed launcher/config/identity、stable-only second-instance 分支、既有 MiniMax Provider/Desktop cleanup 投影与对应 implementation SHA pin。
- 明确不做：不修改 Runtime、Host/Contracts、生产 UI/route/Tauri command，不开启实验 API，不做 public/production 加固，不通过破坏性手段制造失败。

本 Profile 不建立治理切片。FEAT-131 只交付后续 active FEAT-132–137、FEAT-139–144 共用的近似设计策略、能力边界、场景和验证入口；FEAT-138 只保留取消记录，FEAT-144 承接 CAP-017 / GS-004，完整 Epic 目标仍需后续 active Feature 实现。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| yijie | `docs/features/FEAT-131-desktop-codex-parity-baseline/` | 建立 demo_fast Feature Package、近似参考策略、固定 Runtime 身份、38 项能力矩阵、13 个黄金场景和验证索引 | 为 active FEAT-132–137、FEAT-139–144 提供同一治理基线；FEAT-138 仅保留取消记录 |
| yijie-desktop | `tests/feat-131/`、`tests/fixtures/feat-131/` | 新增 test-only raw-event harness、13 场景 catalog 与 safe synthetic replay；catalog 绑定 reference policy ID | 让 fixture 经过真实 `createChatStore`/wire parser，并把推测依据与真实 Runtime 证据分开 |
| yijie-desktop | `scripts/check-feat131-replay-boundary.mjs` | 扫描 production dist，阻止 fixture、harness、canary 和 catalog 进入 bundle | 保证测试资产不成为生产实现 |
| yijie-desktop | stable launcher/config/Sidecar | 新增 `pnpm tauri:demo-fast:stable`，使用独立 bundle/app-data/Host home、MiniMax 文本 Provider、关闭图片动态工具并固定 `experimentalApi=false` | 提供不污染默认数据且可复验的 canonical Desktop local 入口 |
| yijie-codex | 无修改 | 保持固定 commit、schema tree 与 Runtime `0.144.6` | 满足 Runtime 不修改、不升级硬约束 |

## 3. 关键决策与调试日志

| 日期 | 事实/决定 | 处理 | 结果 |
|---|---|---|---|
| 2026-08-26 | 当前 Host projection 只覆盖有限 methods/notifications | 区分 Runtime schema 存在、Host supported projection、实现扩展与 Desktop 当前 UI | 能力矩阵不再把“schema 有定义”误写成“产品可用” |
| 2026-08-26 | safe fixture 必须证明重复性、敏感数据边界与 production 隔离 | 使用 fail-closed parser、完整 fixture canary、variant 精确绑定和 dist boundary scanner | synthetic replay 可复验，且不冒充 real-runtime |
| 2026-08-26 | default `demo_fast` 的图片工具开关与文本 Provider 转发耦合 | 增加 closed `--stable-api-only`，独立设置既有 MiniMax 文本 Provider，并关闭图片 dynamic tool | canonical status 实测 Runtime `0.144.6`、MiniMax-M3、`experimental_api=false` |
| 2026-08-26 | 未注册 dev binary 不能作为可靠的 macOS App 验证对象 | stable 入口构建并启动独立注册的 debug `.app` | canonical App 可启动、读取 readiness/status 并正常退出 |
| 2026-08-26 | Owner 授权最多一次真实 Provider/模型 submission | predecessor 入口只提交一次安全纯文本 prompt，失败不重试 | 本地出现用户消息，但 Runtime 聚合无 thread/turn/delta/terminal；按 pre-runtime FAIL 记录，未确认计费 |
| 2026-08-26 | predecessor 与 default demo_fast 共用 app-data/outbox | stable 入口改用独立 identifier、Desktop app-data 与 `.local/feat131-stable` Host/Codex home | canonical 不恢复旧 pending outbox；旧数据未删除或篡改 |
| 2026-08-26 | stable Desktop supervisor 的正常清理边界需要收窄 | stable Provider 模式不使用 Desktop 层 `kill_on_drop/start_kill`；只验证正常 `Cmd-Q` | 正常退出 PASS；未修改 Host，也不外推异常 cleanup 保证 |
| 2026-08-26 | stable second instance 原本可能 exit 0 | 仅 stable branch 对 AlreadyRunning fail closed；默认入口保持原行为 | canonical 启动结果不会误报 |
| 2026-08-27 | Owner 取消逐版本人工证据与完全一致门槛 | 建立 `owner-approved-inference` policy；不再建立 Codex Desktop version/build Freeze、补采清单或 drift gate | 缺少参考媒体不再阻塞后续开发，且实现只能声明 Codex-inspired approximation |
| 2026-08-27 | Owner 撤回此前提供的全部人工材料 | 删除仓库内媒体副本、manifest、hash 清单和派生场景记录；不在文档、catalog 或测试中保留其内容、身份或观察结论 | 撤回材料不再参与设计、验收或回归；此前关于单张材料处理方式的中间判断一并失效 |
| 2026-08-27 | Owner 保留原 7 项主动排除，并新增排除 GS-006 | 语音、模型版本信息、模型推理强度信息、分享、切换置顶摘要、显示侧边面板、分支到新聊天、File modification & Diff 均标为 `intentional product difference` | 后续 Feature 不得把 8 项当成待实现缺口；FileChange 审批也不纳入 GS-005 |
| 2026-08-27 | Owner 授权 canonical stable 入口发送一次无敏感信息真实文本 prompt，失败最多重试两次且禁止工具调用 | 同时执行 `yijie-agent-host` 更严格的最多 2 次短请求总上限；计入 predecessor 一次 submission 后，本次只剩一次可执行请求 | clean detached HEAD freshly built App 首轮完成并精确返回 `FEAT-131_SMOKE_OK`；未调用工具、未读取/修改文件、未重试；完成后 status 仍为 ready/`experimental_api=false`，Cmd-Q 正常清理 |
| 2026-08-27 | D4 需要一个真实代表性 failure/retry，synthetic replay 不能替代 | 不发送 Provider 请求、不做故障注入：首实例 ready 时启动同一 stable bundle 第二实例，再核对首实例健康；正常退出后从 canonical 入口重启 | 第二实例 exit 1 且稳定报 already running；首实例保持 ready，canonical retry/restart 再次 ready，最终正常退出并清空端口/owned processes |
| 2026-08-27 | 独立 diff review 发现 legacy v1/version/build canary 未被 boundary scanner 覆盖 | scanner 同时加入 v1、v2、旧 version/build 与当前 policy canary；重跑 focused 41 tests、35-file dist scan 与 diff check | P2 已修复；FEAT-131 scoped code/test diff 无 P0–P3；并行 FEAT-150/Store 改动排除且未触碰 |
| 2026-08-29 | Owner 正式取消并排除 FEAT-138 | FEAT-138 不建立正式 Feature Package、不实施、不执行 D4；CAP-022/GS-006 继续保留为 `owner-excluded` 负范围哨兵 | Epic active scope 改为 FEAT-131–137、FEAT-139–143；FEAT-128 Artifact authority 与最终回归不受影响 |
| 2026-08-30 | Owner 批准 FEAT-136 Command 收口并拆分 CAP-017 / GS-004 | 保留 2026-08-29 当时的 12-active 历史行；新增唯一 FEAT-144 D0，更新 capability/scenario/evidence authority 与 final Runtime re-freeze | 当前 Epic active scope 为 FEAT-131–137、FEAT-139–144；FEAT-144 blocked / Tool D4 NOT RUN |

调试规则：30 分钟无新事实则停止猜测式补丁；90 分钟同一阻塞则简化方案；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP。

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 创建本地 FEAT-131 分支 | `yijie`、`yijie-desktop` | 当前用户 / 2026-08-26 | 2 | 2 | 已创建并切换；本轮 scope amendment/verification 未新增 commit/push |
| Provider/模型 submission（历史） | MiniMax-M3 via predecessor Yijie Desktop entry | 当前用户 / 2026-08-26T12:22:54+08:00 | 1 | 1（UI submission） | 未观察到 Runtime thread/turn；未确认 Provider 计费；作为仓库总上限的第 1 次保守计数 |
| Provider/模型 submission（当前 canonical） | MiniMax-M3 via `pnpm tauri:demo-fast:stable` | 当前用户 / 2026-08-27 | 首次 + 失败最多 2 次重试 | 1（首轮成功） | 精确返回 `FEAT-131_SMOKE_OK`，无工具调用、无重试；与历史 submission 合计达到仓库更严格的 2/2 上限，不再调用 |
| 破坏性操作/生产写入 | N/A | N/A | 0 | 0 | N/A |

## 5. 已知限制

- 本 Feature 没有也不需要 Codex Desktop 人工参考媒体；所有布局与交互目标是 Owner 允许的工程推测，不可描述为版本实测事实或完全一致。
- 当前 Desktop wire 只能回放 assistant、reasoning、turn、cleanup、resync 和 context 事件；Command、Tool、Approval 与 Steer 不在本 Feature 扩展，FileChange/Diff 已主动排除。
- `yijie-codex` 本地 `develop` 落后远端 1 个提交；这是固定条件，不允许 pull/rebase/sync 到较新版本。
- canonical `experimentalApi=false` real smoke 已首轮 PASS，GS-001 安全文本 happy path 精确返回 `FEAT-131_SMOKE_OK`；这不证明尚未实现的 Tool、Command、Approval、Steer、长对话或视觉行为。
- 当前成功 submission 可能产生 Provider 计费；predecessor 与当前请求合计达到仓库更严格的 2/2 短请求上限。旧 `com.yijie.ai`/default demo_fast 数据可能包含 pending outbox，未获删除授权所以保持原状；canonical stable 已隔离，不读取该 outbox。
- Host Runtime Manager 的 shutdown timeout、protocol failure 和 startup abort 仍存在 `Process.Kill()` fallback；本 Feature 不修改 Host，也不以故障注入验证。正常 `Cmd-Q` 只能证明正常路径。
- Desktop exit callback 未把 cleanup-incomplete 传播为 launcher 非零状态；本次 normal-exit 结合端口/owned-process 清空为 PASS，但不能外推异常退出保证。
- 近似策略固定不等于 Epic 已完成；生产对话行为仍由 active FEAT-132–137、FEAT-139–144 分阶段交付，FEAT-138 不承担实现责任；FEAT-144 当前 blocked / NOT RUN。
