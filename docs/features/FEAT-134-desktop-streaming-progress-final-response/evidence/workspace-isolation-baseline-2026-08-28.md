# FEAT-134 工作区隔离与 Baseline 记录

> Captured: `2026-08-28T11:55:15+08:00` · Scope: 11 sibling repositories · D0 only

> D4 follow-up `2026-08-29`: Contracts/Host 维持各自 immutable commits 且未 push；Desktop 已提交 immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`，工作树 clean、未 push；`yijie` 治理包仍是 FEAT-134 范围内未提交工作树。Runtime clean 固定 `0ce5902ed400866be0196886bb78f693a004d68d`，binary/manifest 匹配且未修改、升级或重编译。临时 probe 源码与 target 残留均为 0，Host 空 probe 目录已删除。最终 TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff 和 #6 final-source canonical UI smoke PASS，review 无 open P0/P1/P2。按 demo_fast 规范 D4=PASS；后续 `yijie` commit 与任何 push 仍需 Owner 授权。

> 授权 ledger：历史 tranche `4/4`；当前 tranche `6/7`、剩余 `1`；Feature 累计 `10/11`。dark theme、Reduce Motion、精确 1180×760 逐项 `WAIVED / NOT REQUIRED`，不是 PASS、未执行、无需恢复、系统设置未变。

## 1. 记录目的

在 FEAT-134 修改任何文件前，固定所有 sibling repo 的 branch、HEAD 与 clean-start 状态，避免覆盖 FEAT-131/132/133 或其他并行 Feature。随后只建立 Owner 授权的 FEAT-134 分支；本 D0 只允许 `yijie` 治理目录产生文件变化。

检查方法：

```bash
git status --short --branch
git rev-parse HEAD
```

分支创建使用：

```bash
git switch -c feat/feat-134-desktop-streaming-progress-final-response
```

未执行 fetch、pull、rebase、merge、reset、checkout 覆盖、stash、stage、commit 或 push。

## 2. 11 仓 clean-start 快照

| 仓库 | 创建 FEAT-134 前分支 | Baseline HEAD | 状态 |
|---|---|---|---|
| `yijie` | `feat/feat-133-desktop-conversation-timeline-item-shell` | `9a8f1d7b49a9b362c03085740f6f8f75c67d5cf7` | clean |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | clean；既有 tracking 状态为 `origin/develop [behind 1]`，未 fetch/pull |
| `yijie-desktop` | `feat/feat-133-desktop-conversation-timeline-item-shell` | `af38353694c3eb045365b7f3450ffc8a95aaf8a1` | clean |
| `yijie-admin-web` | `develop` | `1e5c7783d98210d5ec03408ec9ff7824795d1127` | clean |
| `yijie-api` | `feat/feat-126-foundation-closure` | `451940b282d8dd3e232ed414bd44b0677897f4c4` | clean |
| `yijie-agent-host` | `feat/feat-129-desktop-skill-marketplace` | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | clean / upstream synchronized |
| `yijie-skills` | `develop` | `10c45bec29603b002e861e1499d5b4e684251af5` | clean |
| `yijie-connectors` | `develop` | `2624155f973e3f6121b5648d2d903fe72fee0210` | clean |
| `yijie-knowledge` | `develop` | `3e5682c4dacdc8031b433bfc956909172a8051b6` | clean |
| `yijie-contracts` | `feat/feat-129-desktop-skill-marketplace` | `164b14f609537d727a52326832da04430aecc4ab` | clean / upstream synchronized |
| `yijie-infra` | `feat/feat-126-s10e` | `42671b802d48ce0318abdefeeb01003cdc597825` | clean |

`clean` 表示 `git status --short` 没有 staged、unstaged 或 untracked 条目。没有发现需要继承、暂存、转移或规避的用户改动。

## 3. FEAT-134 分支结果

统一分支名：

`feat/feat-134-desktop-streaming-progress-final-response`

| 仓库 | 创建依据 | 起点 | 创建后文件状态 |
|---|---|---|---|
| `yijie` | Owner 直接授权 | `9a8f1d7b49a9b362c03085740f6f8f75c67d5cf7` | 仅本 Feature 治理目录为新文件 |
| `yijie-desktop` | Owner 直接授权 | `af38353694c3eb045365b7f3450ffc8a95aaf8a1` | clean 空分支 |
| `yijie-contracts` | 只读审计证明 phase/plan semantic gap 后适用条件授权 | `164b14f609537d727a52326832da04430aecc4ab` | clean 空分支 |
| `yijie-agent-host` | 只读审计证明 mapper/version gate 必需后适用条件授权 | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | clean 空分支 |

未为其余 7 个 sibling repo 创建 FEAT-134 分支。尤其没有创建 `yijie-codex` 分支。

## 4. Contracts/Host 分支的审计门槛

Owner 条件是“除非审计证明需要”。以下只读事实满足该条件：

1. 固定 Runtime stable AgentMessage lifecycle 有 `phase=commentary|final_answer|null`；当前 Contracts/Host schema 和 mapper 未投影 phase。
2. 固定 Runtime 有稳定 `turn/plan/updated`；当前 compatibility/schema/Host 均未投影。
3. Contracts v2/v3 有 raw reasoning delta/finalized，但 compatibility manifest 未锁定 corresponding Runtime notification；canonical Host 默认关闭该投影。
4. Desktop 不能从当前单 Assistant append、Turn terminal、正文或到达顺序可靠还原上述语义。

若不创建 Contracts/Host 分支，只能删除 FEAT-134 的 commentary/final 与 plan Must；D0 决定保留这些核心目标，因此需要 source-first 四仓边界。

## 5. D0 精确写入 Allowlist

### `yijie`

允许：

```text
docs/features/FEAT-134-desktop-streaming-progress-final-response/feature.yaml
docs/features/FEAT-134-desktop-streaming-progress-final-response/00-feature-brief.md
docs/features/FEAT-134-desktop-streaming-progress-final-response/01-delivery-log.md
docs/features/FEAT-134-desktop-streaming-progress-final-response/02-verification.md
docs/features/FEAT-134-desktop-streaming-progress-final-response/evidence/workspace-isolation-baseline-2026-08-28.md
docs/features/FEAT-134-desktop-streaming-progress-final-response/evidence/contract-first-capability-matrix-2026-08-28.md
```

不允许：上述目录外的源代码、历史 Feature、ADR、脚本、锁文件、配置或其他文档。

### `yijie-contracts`

D0 允许：仅 branch ref 变化。

D0 不允许：OpenAPI、protobuf、JSON Schema、compatibility、fixtures、tests、version/tag 或任意文件变化。

### `yijie-agent-host`

D0 允许：仅 branch ref 变化。

D0 不允许：mapper、router、feature flag、provider config、contracts snapshot/lock、tests 或任意文件变化。

### `yijie-desktop`

D0 允许：仅 branch ref 变化。

D0 不允许：TypeScript/Vue/Rust、private IPC、FEAT-132 domain/adapter/store、SQLCipher、migration、package/lock、Tauri capability 或任意文件变化。

### `yijie-codex`

不允许创建 FEAT-134 分支或发生任何修改、升级、重编译、替换、schema/pin 变化。固定 Runtime 事实：

- commit `0ce5902ed400866be0196886bb78f693a004d68d`
- upstream `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d`
- schema tree `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`
- stdio / `experimentalApi=false`

## 6. 后续实现的 Provisional Ownership

此表只定义边界，不授权本轮实现。

| 顺序 | 仓库 | 后续允许的职责 | 禁止旁路 |
|---|---|---|---|
| 1 | `yijie-contracts` | negotiated event vNext、compat/OpenAPI/proto/schema/fixture/test | 原地改 v1-v3 closed union；Runtime experimental item plan |
| 2 | `yijie-agent-host` | version-gated mapper、item lifecycle/phase/plan/reasoning、pin | 未经 Contracts 先改 Host wire；在 Host 推测 phase |
| 3 | `yijie-desktop` | private IPC、FEAT-132 authority、SQLCipher、FEAT-133 Timeline composition | 页面读取 raw wire；第二状态机；只改 Vue 伪造语义 |
| governance | `yijie` | package、验证证据、跨仓 pin/claims 记录 | 把 D0 当 D4；覆盖历史 provenance |

## 7. 保护项与停止条件

- FEAT-127 附件 authority、FEAT-128 Artifact authority、FEAT-132 ConversationState authority、FEAT-133 Timeline/clipboard 边界必须继承。
- 八项 Owner exclusions 必须保持，其中 CAP-022 / GS-006 File Modification & Diff 是永久 negative sentinel。
- 发现任何 baseline 外 dirty change：停止、记录 owner/path，不覆盖、不清理、不纳入提交。
- 需要新增依赖、修改 Runtime、启用 `experimentalApi`、直接改旧 contract union、猜 phase/plan/reasoning、改变模型/Provider/reasoning config 或建立第二 authority：停止并请求 Owner 决策。
- 需要真实 prompt/付费调用、破坏性动作或生产写入：必须获得 FEAT-134 独立、精确、可计数的新授权。
- 禁止强杀/故障注入、权限破坏、binary 替换及恶意/攻击 fixture；依赖这些行为的验收记录 `NOT RUN`。

## 8. 提交与发布状态

- `git add` / `git commit`: PASS（Contracts `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`）
- `git add` / `git commit`: PASS（Host final authority `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`，保留其线性 corrective 历史）
- `git add` / `git commit`: PASS（Desktop `7b9daa791635250d0628c9e9f553cf40fab5ad96`；工作树 clean）
- `yijie` governance commit: NOT RUN（仍需 Owner 授权）
- `git push`: NOT RUN
- tag/release/publication: NOT RUN

历史初始 D0 时点只授权分支创建与治理产物；Owner 后续单独授权 Contracts candidate 的 `git add` 与提交，但明确禁止 push。该初始时点治理仓、Host、Desktop 与 Runtime 均未提交。

后续授权更新：Contracts 已提交为 `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`；Host 线性提交历史是 baseline `1b7bfd…` → first implementation `201fd9…` → corrective child/final authority `b9358f…`；Desktop 最终提交为 `7b9daa791635250d0628c9e9f553cf40fab5ad96`。三仓均未 push，Desktop clean；该更新不改变本节记录的 clean-start baseline。Runtime 仍未提交或修改，`yijie` 治理包仍未提交。

## 9. 2026-08-28 Owner 授权修订

Owner 后续明确批准 FEAT-134 在 `demo_fast/local` 使用固定 managed provider reasoning effort=`high` 并启用 Host raw-reasoning projection，分类为 `ai_behavior_change=model`；不得新增强度 UI、修改 Runtime、启用 experimental API 或影响 public/production。历史 tranche `4/4` 保留；当前 tranche `6/7`、剩余 `1`，Feature 累计 `10/11`。每次均为显式授权而非程序自动重试；禁止工具调用、文件读写，Artifact 仅保留 content-free 事实。

Owner 于 `2026-08-28/29` 又明确将 dark theme、Reduce Motion 与精确 `1180×760` 从 FEAT-134 治理门禁移除；三项均为 `WAIVED / NOT REQUIRED`，不是 PASS，无需执行或恢复，系统设置未变。

第四次失败后的历史实现时点仍保持仓库隔离：failed-start repair/recovery 仅修改 Desktop exact-local payload v2 路径。pre-POST Active 以 attempt provenance 隔离 attempt_count=1 suspend 与 attempt_count>1 crash-reclaim bind；post-error Active 直接 bind；两侧回归均 PASS，confirmed failure 与 identity mismatch/non-idle/Err fail-closed 边界不变。v1 exact-local/legacy、Vue、Contracts、Host、Runtime、public/production 均不变；flag=false exact isolation PASS。当时的静态 aggregate/lint/build/fmt/diff 与 `00:34` no-prompt smoke PASS，且 Desktop 尚未提交；该历史事实不覆盖本文顶部和本节记录的最终 Desktop commit。

该授权允许后续按 provisional ownership 进入实现；当时尚未授权 commit 或 push。Owner 随后另行授权 Contracts candidate 的单一提交，记录如下；精确 local high/raw 之外的模型/Provider/config 变化仍触发停止条件。

## 10. 2026-08-28 Contracts 提交授权与结果

Owner 明确授权在 `yijie-contracts` 执行 `git add` 并提交 FEAT-134 Contracts v4 candidate，禁止 push。实际结果：

- branch：`feat/feat-134-desktop-streaming-progress-final-response`
- commit：`3832a6c5e99b2a6365f193280fdb887c8fdbc2de`
- subject：`feat(contracts): add FEAT-134 agent session event v4`
- commit 后工作树：clean
- push/tag/publish：NOT RUN
- canonical prompt：本 Contracts commit 时点未消费；现行状态由后续证据更新为历史 `4/4` + 当前 `6/7`，Feature `10/11`

该完整 SHA 现在是 Host 精确 pin 的唯一 FEAT-134 Contracts authority；不得改用 floating branch、dirty sibling 或虚构 tag。
