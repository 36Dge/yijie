# FEAT-135 工作区隔离与 Baseline 记录

> Captured: `2026-08-29T11:08:27+08:00`；status reconfirmed: `2026-08-29T11:14:43+08:00` · Scope: 11 sibling repositories · D0 only

## 1. 记录目的

在 FEAT-135 修改任何实现文件前，确认 FEAT-134 已收口的 `yijie` 与 `yijie-desktop` HEAD 均 clean，并从这些精确 HEAD 创建同名隔离分支。其余仓库只读记录 branch、HEAD 与状态，不创建 FEAT-135 分支。

使用的只读检查：

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

Owner 授权的分支动作：

```bash
git switch -c feat/feat-135-desktop-codex-style-composer
```

没有执行 fetch、pull、merge、rebase、reset、stash、stage、commit、push、tag 或 release。

## 2. 精确起点与分支结果

统一分支名：`feat/feat-135-desktop-codex-style-composer`

| 仓库 | 创建前状态 | Baseline HEAD | 创建结果 | 当前文件状态 |
|---|---|---|---|---|
| `yijie` | FEAT-134 clean HEAD | `507e84b32de542883499bfafd22f0d8ec9bcab21` | PASS | 仅本 FEAT-135 治理目录为 untracked |
| `yijie-desktop` | FEAT-134 clean HEAD | `7b9daa791635250d0628c9e9f553cf40fab5ad96` | PASS | clean；实现 diff 为 0 |

两个分支都从 Owner 指定的当前 clean FEAT-134 HEAD 创建，没有夹带、覆盖或清理用户改动。

## 3. 11 仓 D0 快照

| 仓库 | 当前分支 | HEAD | D0 状态/处置 |
|---|---|---|---|
| `yijie` | `feat/feat-135-desktop-codex-style-composer` | `507e84b32de542883499bfafd22f0d8ec9bcab21` | 仅新增本治理目录 |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | clean；固定 Runtime，不创建分支 |
| `yijie-desktop` | `feat/feat-135-desktop-codex-style-composer` | `7b9daa791635250d0628c9e9f553cf40fab5ad96` | clean；只创建 branch ref |
| `yijie-admin-web` | `develop` | `1e5c7783d98210d5ec03408ec9ff7824795d1127` | clean；不在范围 |
| `yijie-api` | `feat/feat-126-foundation-closure` | `451940b282d8dd3e232ed414bd44b0677897f4c4` | clean；不在范围 |
| `yijie-agent-host` | `feat/feat-134-desktop-streaming-progress-final-response` | `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` | clean；只读，不创建 FEAT-135 分支 |
| `yijie-skills` | `develop` | `10c45bec29603b002e861e1499d5b4e684251af5` | clean；不在范围 |
| `yijie-connectors` | `develop` | `2624155f973e3f6121b5648d2d903fe72fee0210` | clean；不在范围 |
| `yijie-knowledge` | `develop` | `3e5682c4dacdc8031b433bfc956909172a8051b6` | clean；不在范围 |
| `yijie-contracts` | `feat/feat-134-desktop-streaming-progress-final-response` | `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` | clean；只读，不创建 FEAT-135 分支 |
| `yijie-infra` | `feat/feat-126-s10e` | `42671b802d48ce0318abdefeeb01003cdc597825` | clean；不在范围 |

`clean` 表示 `git status --short` 没有 staged、unstaged 或 untracked 条目。`yijie` 的治理目录是在 clean-start 与分支创建后按本轮授权新增，不属于 baseline 前既有改动。

## 4. D0 精确写入 Allowlist

### `yijie`

允许：

```text
docs/features/FEAT-135-desktop-codex-style-composer/feature.yaml
docs/features/FEAT-135-desktop-codex-style-composer/00-feature-brief.md
docs/features/FEAT-135-desktop-codex-style-composer/01-delivery-log.md
docs/features/FEAT-135-desktop-codex-style-composer/02-verification.md
docs/features/FEAT-135-desktop-codex-style-composer/evidence/workspace-isolation-baseline-2026-08-29.md
docs/features/FEAT-135-desktop-codex-style-composer/evidence/contract-first-capability-matrix-2026-08-29.md
```

不允许：上述目录外的源码、历史 Feature、ADR、脚本、锁文件、配置或其他文档。

### `yijie-desktop`

D0 允许：仅 branch ref 变化。

D0 不允许：TypeScript、Vue、Rust、private IPC、database/migration、FEAT-127 attachment、FEAT-128 Artifact、FEAT-132 domain/adapter/store、FEAT-133/134 Timeline、package/lock、Tauri config/capability 或任何文件变化。

### `yijie-contracts` 与 `yijie-agent-host`

D0 只允许只读审计；不允许创建 FEAT-135 分支，不允许 OpenAPI、snapshot/lock、mapper、router、provider config、fixture、test 或任何文件变化。

### `yijie-codex`

不允许创建 FEAT-135 分支或发生任何修改、升级、重编译、替换、同步、schema/manifest/pin 变化。固定 Runtime：

- branch：`develop`
- commit：`0ce5902ed400866be0196886bb78f693a004d68d`
- `experimentalApi=false`

## 5. Provisional Ownership

此表只规定后续边界，不授权本轮实现。

| 顺序 | 仓库/层 | 后续允许的职责 | 禁止旁路 |
|---|---|---|---|
| 1 | `yijie-desktop` store/application | 把既有 native response 映射为进程内显式 submission result；保留 operation ID、ordered blocks 与 authority | 改 IPC/schema；把 void/no-op 当 accepted；从 UI 猜结果 |
| 2 | `yijie-desktop` page composition | target-scoped WebView 文本草稿、submit race、matching target 清理、焦点编排 | 新 durable draft store；跨 target 清理；post-durable 恢复正文 |
| 3 | `yijie-desktop` `ChatComposer` | auto-grow、max-scroll、键盘/IME、统一 enabled/busy、focus/action slot | 第二提交 authority；新依赖；新 active Turn 控制语义 |
| 4 | `yijie` governance | D1-D4 事实、验证 Artifact、跨层 negative sentinel | 把 D0 当 D4；伪造 canonical 或 Must PASS |

Contracts、Host 与 Runtime 没有 provisional write ownership；矩阵结论是现有 contract 足够。

## 6. 保护项与停止条件

- FEAT-127 attachment authority、FEAT-128 Artifact authority、FEAT-132 ConversationState、FEAT-133 Timeline shell 和 FEAT-134 streaming projection 必须继承。
- Owner 永久排除语音、模型版本、模型推理强度 UI、分享、切换置顶摘要、右侧上下文面板、分支到新聊天与 CAP-022 / GS-006 File Modification & Diff。
- 发现 baseline 外 dirty change：停止、记录 owner/path，不覆盖、不清理、不纳入提交。
- 需要 Contracts、Host、Runtime、private IPC、database/migration、durable/replay 变化：停止，将 `contract-impact` 从 `none` 重分类并申请授权。
- 需要新增依赖、改变模型/Provider/prompt/reasoning、启用 `experimentalApi` 或 active Turn 控制语义：停止并请求 Owner 决策。
- 需要真实 prompt、付费调用、工具/任务文件读写、production/public 写入：必须取得 FEAT-135 独立、精确、可计数授权；FEAT-134 权限不继承。
- 禁止强杀/故障注入、权限破坏、binary 替换及恶意/攻击 fixture；依赖这些行为的验证必须跳过并记录影响。

## 7. 提交与发布状态

- `git add`: NOT RUN
- `git commit`: NOT RUN
- `git push`: NOT RUN
- tag/release/publication: NOT RUN
- canonical startup/prompt: NOT RUN
- Contracts/Host/Runtime FEAT-135 branches: NOT CREATED

Owner 本轮只授权两仓分支创建、D0 治理包、隔离记录和只读 Contract First 矩阵；未授权实现、提交、推送或真实 prompt。
