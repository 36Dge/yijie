# FEAT-131 整体实现与调试记录

## 1. 整体实现方案

- 真实事实链：本机 Codex Desktop metadata → 固定 `yijie-codex` manifest/schema → `yijie-contracts` compatibility manifest → 当前 Host mapper → Desktop strict wire parser/store → test-only replay snapshot。
- 跨层顺序：冻结身份与证据状态 → 建矩阵/场景 → 落 test-only fixture/harness → 做敏感数据与 bundle 隔离 → focused/full/build → canonical local smoke → Runtime 前后对账。
- Contract First：`contract-impact=additive`；不创建或变更 wire schema。增量只包含 Desktop-local closed launcher/config/identity、stable-only second-instance 分支、既有 MiniMax Provider/Desktop cleanup 投影与对应 implementation SHA pin；原始 fixture 仍不得被 `src/`、Host 或其他仓库消费。
- 明确不做：不修改 Runtime、Host/Contracts、生产 UI/route/Tauri command，不开启实验 API，不做 public/production 加固，不用破坏性手段制造失败。

本 Profile 不建立治理切片。可以按技术依赖顺序编码，但最终以一个完整、可冻结的基线结果统一验收。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| yijie | `docs/features/FEAT-131-desktop-codex-parity-baseline/` | 建立 demo_fast Feature Package、冻结身份、能力矩阵、黄金场景和证据索引 | 为 FEAT-132–143 提供唯一版本化基线 |
| yijie-desktop | `tests/feat-131/`、`tests/fixtures/feat-131/` | 新增 test-only raw-event harness、13 场景 catalog 与 3 个 safe synthetic replay | 让 fixture 经过真实 `createChatClient` 严格 parser 和 `createChatStoreDefinition` reducer |
| yijie-desktop | `scripts/check-feat131-replay-boundary.mjs` 及测试 | 扫描生产 `dist/` 中的 FEAT-131 canary，并对误入 bundle 的测试标记 fail closed | 证明 harness、fixture 与 viewer 没有进入生产 bundle |
| yijie-desktop | `package.json`、`scripts/run-local-demo-fast.sh`、`src-tauri/tauri.feat131-stable.conf.json` 及 focused test | 新增 `tauri:demo-fast:stable`，只接受精确 `--stable-api-only`；freshly build 独立 `com.yijie.ai.feat131-stable` App，并使用独立 `.local/feat131-stable` Host/Codex home | 提供不会恢复 default demo_fast 历史 outbox、可由安全 UI 自动化读取且 `experimentalApi=false` 的 canonical 入口 |
| yijie-desktop | `src-tauri/src/chat/sidecar.rs`、Desktop-local consumer pin | 把既有 MiniMax 文本 Provider 与 FEAT-128 图片 dynamic tool 解耦；stable 模式转发 owner-only key path而不转发图片开关；Desktop supervisor 不使用 `kill_on_drop/start_kill` | 同时满足真实文本 Provider、stable Runtime API 与 Desktop-local 正常清理边界；不宣称 Host 内部 fallback 保证 |
| yijie-desktop | `src-tauri/src/lib.rs`、Desktop-local consumer pin | stable-only instance 遇到已有 Yijie App 时非零 fail closed；默认第二实例仍沿用原 `return` 行为 | 防止 canonical launcher 在 single-instance guard 下空跑并误报成功，同时保持默认入口兼容性 |
| yijie-desktop | `src/`、生产 Chat UI、路由、Tauri command | 无变化 | 本 Feature 不实施对话交互 UI |
| yijie-codex | N/A（只读） | 禁止变化 | Epic 硬约束 |

## 3. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复/决策 | 结果 | 累计耗时 |
|---|---|---|---|---|---:|
| 2026-08-26 | Codex Desktop 应用 metadata 可只读取得，但 Computer Use 拒绝读取当前 Codex App UI | Codex 对自身应用的 UI 自动化存在安全限制 | 不使用系统截图或其他 UI 自动化绕过；版本专属 UI 证据标为 `reference-unobserved`，保留人工采集清单 | 安全边界已明确，D4 参考证据待补 | < 1h |
| 2026-08-26 | 当前 Host compatibility projection 少于固定 Runtime stable surface | Host 只锁定最小 methods/notifications，部分实现路径不等于权威支持 | 矩阵分开 Runtime、locked projection、Desktop 和 implementation extension | D0 能力边界清晰 | < 1h |
| 2026-08-26 | FEAT-131 不需要生产 viewer 或新 reducer | Desktop 已支持注入 Chat transport，真实 parser/store 可由测试驱动 | harness 严格放在 `tests/`，用 canary 做 dist 负向检查 | focused replay 与 dist boundary 均 PASS | < 1h |
| 2026-08-26 | 首版场景分类把部分 schema/实现路径误写为 frozen Runtime 阻断或主动差异 | stable schema、locked Host projection、实现扩展三者混淆 | 逐项回查 schema attribute 与 compatibility manifest；Fork/Archive、plan delta、requestUserInput 改为 `requires Host/Contracts projection`，Artifact renderer 与 Runtime producer 分开记录 | 31 项矩阵分类与 13 场景 catalog 一致 | < 1h |
| 2026-08-26 | safe fixture 可以进入 parser/store，但需要证明重复性、敏感数据边界与 production 隔离 | 单纯 JSON snapshot 不能证明真实 Desktop 消费链或 bundle 边界 | 负向扫描扩至 34 个嵌入完整 fixture 的 canary；catalog `replayedVariants` 与 fixture `coveredVariants` 精确绑定；focused 为 2 files/41 tests | focused PASS；最终 full/build 复验见 `02-verification.md` | < 2h |
| 2026-08-26 | default `demo_fast` launcher 固定打开图片 dynamic tool，单纯设为 false 又会因 Sidecar `env_clear()` 丢失文本 Provider | Desktop Sidecar 把 Provider/key 转发错误地绑定在图片开关上 | 新增 closed `--stable-api-only`，Sidecar 独立解析既有 `YIJIE_MODEL_PROVIDER=minimax` + owner-only key；只有图片模式转发 FEAT-128 flag | canonical status 实测 Runtime `0.144.6`、MiniMax-M3、`experimental_api=false` | < 1h |
| 2026-08-26 | Tauri dev 二进制窗口无法被 Computer Use 绑定 | 未注册的 `target/debug/yijie-desktop` 不是可寻址 macOS `.app` | stable 入口先运行受管 debug bundle build，再执行 `.app/Contents/MacOS/yijie-desktop`；默认开发入口不变 | predecessor `com.yijie.ai` App 可安全读取，Composer/发送按钮可观察 | < 1h |
| 2026-08-26 | 用户授权一次真实 Provider/模型调用 | `paid_calls=true/max_actions=1`；prompt 为无敏感信息且明确禁止工具调用 | 在 predecessor `com.yijie.ai` 入口只点击一次“发送任务”，失败也不重试；不保留含既有会话标题的截图 | 用户消息本地出现，但持续停在“状态已更新”，无 streaming/assistant/terminal | < 1h |
| 2026-08-26 | UI submission 是否真的到达 Runtime/Provider 不可仅凭页面推断 | fixed Runtime 本地 log DB 可做只读聚合，且无需输出正文、路径或 identifier | 只聚合四个事件存在性，结果 `thread_started=0`、`turn_started=0`、`assistant_delta=0`、`turn_completed=0` | 真实 happy path FAIL；没有证据确认发生 Provider 调用或计费，但授权额度按 1 次 UI submission 保守记作已用 | < 1h |
| 2026-08-26 | Desktop supervisor 原有 3 秒后 `start_kill()` fallback 不适合 stable 验证 | stable 验证的 Desktop→Host 层只应正常 SIGTERM；超时需保留 unknown child | stable Provider 模式关闭 `kill_on_drop/start_kill`；实际 Cmd-Q 正常退出 | Desktop 层策略与正常退出 PASS；未修改 Host，不能外推为 App→Host→Runtime 异常保证 | < 1h |
| 2026-08-26 | 独立复审发现 predecessor 与 default demo_fast 共用 app-data/outbox | 唯一失败 submission 可能在以后默认 App bind/coordinator 时自动恢复 | stable 改为独立 identifier、Desktop app-data 与 `.local/feat131-stable` Host/Codex home；保留旧数据不删除 | 当前 canonical 不会恢复旧 outbox；默认入口启动前仍需 Owner 决策 | < 1h |
| 2026-08-26 | single-instance guard 对已有实例原本 `return`/exit 0 | stable launcher 可能未启动当前 App却误报成功 | stable env 精确标记；仅 stable branch 对 AlreadyRunning exit 1，默认分支仍 `return` | stable fail closed；默认第二实例行为保持 | < 1h |
| 2026-08-26 | 当前隔离 canonical 需要重新绑定启动证据 | 旧 `/v1/status` 和 Cmd-Q 不能证明新 identity/root | 对最终代码 freshly build `易界 AI FEAT-131.app`，两次仅做 startup/status/Cmd-Q，不打开项目、不发送 prompt | 两次均 Runtime ready、MiniMax-M3、`experimental_api=false`；正常退出后端口/owned processes 清空 | < 1h |
| 2026-08-26 | 独立复审发现 Host Runtime Manager 仍在 timeout/protocol/startup failure 使用 `Process.Kill()` | 该路径位于未授权修改的 Host，且不能用故障注入验收 | 收窄 AC-009 为 Desktop supervisor 与正常 Cmd-Q；diff review 保持 PARTIAL，登记跨仓风险 | 不伪造整链 cleanup PASS | < 1h |
| 2026-08-26 | 完整 `make test` 中既有 `YjChartCard` observer 时序断言曾偶发失败 | 与当时 FEAT-131 文件无依赖，单文件和随后全量通过 | 当时完整 `make test` 为 frontend 75 files/594 tests、Rust 265/3 ignored PASS；最终 isolation 增量后不再运行会改变权限/注入失败的既有负向 Rust tests，改用 `cargo check` 和安全正向 focused test | predecessor full PASS；current delta compile/focused/build PASS，禁止项明确未重跑 | < 1h |

调试规则：30 分钟无新事实则停止猜测式补丁；90 分钟同一阻塞则简化方案；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP。

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 创建本地 FEAT-131 分支 | `yijie`、`yijie-desktop` | 当前用户 / 2026-08-26 | 2 | 2 | 已从各自干净当前 HEAD 创建并切换；未 commit/push |
| Provider/模型 submission | MiniMax-M3 via predecessor Yijie Desktop entry | 当前用户 / 2026-08-26T12:22:54+08:00 | 1 | 1（UI submission） | 消息未到达 Runtime thread/turn；未确认 Provider 计费，不重试；当前隔离 canonical 未发送 prompt |
| 破坏性操作/生产写入 | N/A | N/A | 0 | 0 | N/A |

## 5. 已知限制

- 当前自动化不能安全读取 Codex Desktop 自身窗口；截图、录屏、窗口尺寸和交互配置的版本专属证据必须由人工按索引补采，不能用推测替代。
- 当前 Desktop wire 只能回放 assistant、reasoning、turn、cleanup、resync 和 context 事件；Command、Tool、Approval、Diff 与 Steer 不在本 Feature 扩展。
- `yijie-codex` 本地 `develop` 落后远端 1 个提交；这是冻结条件，不允许 pull/rebase/sync 到较新版本。
- 当前隔离 stable canonical 入口和 `experimentalApi=false` startup 已完成；当前 entry 的 real smoke 因授权额度已用而 `NOT RUN`。predecessor 的唯一 submission 停在 Host session/Runtime thread 绑定前，GS-001 happy path 尚未完成。
- 没有确认产生 Provider 计费；仍按授权上限不再提交。旧 `com.yijie.ai`/default demo_fast 的本地会话可能按既有 outbox 规则恢复，未获删除授权，因此没有篡改或清除；默认入口再次启动前需 Owner 决策。canonical stable 已隔离，不会读取该 outbox。
- Host Runtime Manager 的 shutdown timeout、protocol failure 和 startup abort 仍存在 `Process.Kill()` fallback；本 Feature不修改 Host，也不以故障注入验证。实际正常 Cmd-Q 均自然退出，只能证明正常路径。
- Desktop exit callback 未把 cleanup-incomplete 传播为 launcher 非零状态；因此异常退出后的端口/owned-process 核验仍是人工步骤，不能仅凭命令 exit 0 宣称 cleanup PASS。
- 基线冻结不代表 Epic 已完成；生产对话行为由 FEAT-132–143 分阶段交付。
