# FEAT-133 整体实现与调试记录

> 当前阶段：`D0 PASS` · 实现状态：`pending` · 记录日期：`2026-08-27`

## 1. 整体实现方案

- 参考策略：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`；不采集或等待 Codex Desktop 人工证据。
- 真实调用链：FEAT-132 `ConversationState` → 纯 Timeline selector/ViewModel → Vue Timeline/TurnGroup/ItemShell/SafeContent → 页面组合；组件不接触 raw wire、数据库或原生副作用。
- 跨层顺序：领域能力只读对账 → selector/component tests → Timeline/Item shell → disclosure/clipboard/action events → 最小页面组合 → focused/full checks → canonical no-prompt smoke → 独立审查 → D4。
- Contract First：当前 `impact=none`，因为只消费 FEAT-132 进程内 ViewModel 并派生展示；若缺字段或需改变任何跨进程/持久化语义，立即停止并重新分类，不在 Vue 猜测。
- 内容安全：优先使用受限、类型化内容树，不使用 `v-html`；不新增 Markdown 依赖。若该方案不能满足 AC-002，先取得依赖批准。
- 产品边界：保留 FEAT-127 附件、FEAT-128 Artifact 和既有 Composer/Sidebar authority；不实现八项 Owner 排除能力，尤其不把 Artifact 变成 FileChange/Diff。
- 明确不做的生产加固：public/production、发布、完整安全/性能专项、migration、灰度、Dashboard、签名与公证；这些不影响 `demo_fast + local` D0，但不能被写成 PASS。

本 Profile 不建立治理切片。后续编码可以按技术依赖推进，但最终只以一个完整 Timeline 用户结果统一验收。

## 2. 工作区 clean-start 与逻辑隔离

`2026-08-27T20:40:31+08:00` 重新核对 CrossBSD 11 个 Git 仓库。创建 FEAT-133 scaffold 前全部 clean；创建后只有 `yijie` 出现一个未跟踪 FEAT-133 目录，其他仓库保持 clean。

| Repository | Branch | Baseline HEAD | 初始状态 | D0 结束预期 |
|---|---|---|---|---|
| `yijie` | `feat/feat-131-desktop-codex-parity-baseline` | `aed49b78f21c264bb13c05c1976f11f7fc14b520` | clean | 仅 FEAT-133 包为 untracked/modified |
| `yijie-desktop` | `feat/feat-131-desktop-codex-parity-baseline` | `f96fe05ca81d6bc7fac97ecbf81bcbab32b8aaa0` | clean | clean |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | clean | clean / fixed |
| `yijie-contracts` | `feat/feat-129-desktop-skill-marketplace` | `164b14f609537d727a52326832da04430aecc4ab` | clean | clean |
| `yijie-agent-host` | `feat/feat-129-desktop-skill-marketplace` | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | clean | clean |
| `yijie-admin-web` | `develop` | `1e5c7783d98210d5ec03408ec9ff7824795d1127` | clean | clean |
| `yijie-api` | `feat/feat-126-foundation-closure` | `451940b282d8dd3e232ed414bd44b0677897f4c4` | clean | clean |
| `yijie-infra` | `feat/feat-126-s10e` | `42671b802d48ce0318abdefeeb01003cdc597825` | clean | clean |
| `yijie-knowledge` | `develop` | `3e5682c4dacdc8031b433bfc956909172a8051b6` | clean | clean |
| `yijie-connectors` | `develop` | `2624155f973e3f6121b5648d2d903fe72fee0210` | clean | clean |
| `yijie-skills` | `develop` | `10c45bec29603b002e861e1499d5b4e684251af5` | clean | clean |

本轮没有新 branch/worktree/stash/commit 授权，因此采用路径级逻辑隔离：

- `yijie` D0 allowlist：FEAT-133 的四个正式文件及一个 `evidence/workspace-isolation-baseline-2026-08-27.md`。
- `yijie-desktop` D0 allowlist：空；整个仓库只读。
- `ChatPage.vue` 保护证据：Git blob `ea2c3a1e606d687981d7a11fec3ac7196baa56f9`，SHA-256 `b89e1204864656de800c5d2682100116b2784ebd17b48534b705ba58bb8dfef1`。
- Runtime、Contracts、Host 和其余仓库：全仓只读。
- 普通 `git diff` 不覆盖未跟踪包；D0 范围必须同时用 `git status --short`、实际包文件清单、strict D0 checker 与 claims audit 证明。

完整记录见 `evidence/workspace-isolation-baseline-2026-08-27.md`。

## 3. D0 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| `yijie` | `docs/features/FEAT-133-desktop-conversation-timeline-item-shell/feature.yaml` | 登记 schema v3、scope、8 条 Must AC、Contract First、授权和 D4 计划 | 建立机器可读正式治理包 |
| `yijie` | `00-feature-brief.md` | 冻结背景、目标、非目标、主流程、UI 状态、推荐组件边界、隔离和停止条件 | 让后续实现不依赖聊天历史或旧 Epic 冲突文本 |
| `yijie` | `01-delivery-log.md` | 记录 clean-start、逻辑隔离、决策冲突与当前未实施状态 | 保护多仓工作区并保持事实可追踪 |
| `yijie` | `02-verification.md` | 记录 D0 门禁、未运行 D4 项与后续验证矩阵 | 防止把治理完成误报为功能完成 |
| `yijie` | `evidence/workspace-isolation-baseline-2026-08-27.md` | 保存 11 仓 HEAD/status、关键哈希、allowlist/denylist | 为后续范围漂移检查提供可复核基线 |
| `yijie-desktop` | 无 | 无代码、测试、配置或依赖变化；`ChatPage.vue` 未修改 | 遵守本轮“不要直接修改 ChatPage.vue”和 D0-only 范围 |

## 4. D0 决策与冲突收敛

| 时间 | 事实/冲突 | 决策 | 结果 |
|---|---|---|---|
| 2026-08-27 | 原 Epic 要求 Codex version/build Freeze 与人工证据，Owner 后续撤回全部人工材料 | 以 FEAT-131 `owner-approved-inference` policy 为权威，不引用撤回图片或版本专属观察 | D0 使用 Codex 风格近似目标，不要求逐像素一致 |
| 2026-08-27 | 原 FEAT-133 把 FileChange/Diff 写成 shell 的未来消费者 | GS-006 为永久 Owner 排除；从目标、依赖、验收中移除 Diff，只保留 Artifact authority | 不实现或暗示 FileChange/Diff |
| 2026-08-27 | Chat Pattern 提到右侧上下文面板，Owner 明确排除“显示侧边面板” | 当前 Epic 采用 Owner 最新决定，不新增/恢复侧边面板 | 作为 intentional product difference 登记 |
| 2026-08-27 | FEAT-132 将 progress 归为 Turn lifecycle、error/warning 归为 Turn notice | UI 只读呈现这些语义，不伪造新的 domain Item | `contract-impact=none` 保持可复核 |
| 2026-08-27 | ViewModel 没有保证时间/耗时字段 | header 只显示真实字段；缺失时隐藏，不能在 Vue 推测 | 避免引入影子语义 |
| 2026-08-27 | package.json 没有直接 Markdown renderer/sanitizer 依赖 | 推荐受限类型化内容树；需要依赖时停止并请求批准 | D0 不改 package/lockfile |
| 2026-08-27 | 用户要求先完成正式 D0 和隔离记录，不直接修改 `ChatPage.vue` | 本轮 Desktop allowlist 为空，只改 FEAT-133 治理包 | 实现保持 pending，D4 不提前声明 |

## 5. 调试循环

当前没有产品实现或 runtime 调试。D0 文档门禁如实记录实际命令；若 checker 失败，将只修复治理包事实或结构，不借机修改 Desktop。

| 时间 | 真实现象 | 根因/新证据 | 修复 | 结果 | 累计耗时 |
|---|---|---|---|---|---:|
| 2026-08-27 | FEAT-133 正式目录不存在 | Desktop Epic 文件只是 Draft Brief，不是 schema v3 package | 使用官方 `new-feature.sh` 创建 demo_fast/local scaffold | scaffold 已创建；进入完整 D0 填充 | < 0.1h |
| 2026-08-27 | scaffold 含模板未完成标记 | 官方生成器只提供结构，不提供需求事实 | 依据 Owner 最新决定、FEAT-131/132、Design System 与代码事实补全 | strict D0 与 claims audit 均 PASS；placeholder/whitespace/conflict scan PASS | < 0.5h |
| 2026-08-27 | `feature:audit` 输出固定使用“committed”措辞，但脚本实际枚举当前 working-tree `docs/features` | 当前 12 个目录包含未跟踪 FEAT-133；base ref 用于历史/evolution 对账，不会把当前包排除 | 如实登记 FEAT-133 已被仓库审计覆盖，并保留 direct strict D0 + direct claims audit 作为定点复核 | working-tree 12 个 claims（含 FEAT-133）PASS；direct checks 也 PASS | < 0.1h |
| 2026-08-27 | D0 结束前复核工作区 | 需要同时证明 allowlist、protected hashes 与所有兄弟仓状态 | 精确断言 11 仓 HEAD/status、五文件清单和 ChatPage blob/SHA-256 | 只有 yijie/FEAT-133 为 untracked；其余 10 仓 clean，ChatPage 未变化 | < 0.1h |

调试规则：30 分钟无新事实则回到 FEAT-132→selector→component 单链路；90 分钟同一阻塞则简化方案；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP；16 小时未 D4 则重新定范围。

## 6. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费调用 | N/A | N/A | 0 | 0 | 未授权、未执行；FEAT-132 额度不可转用 |
| 破坏性操作 | N/A | N/A | 0 | 0 | 禁止且未执行 |
| 生产写入 | N/A | N/A | 0 | 0 | 未授权、未执行 |
| branch/worktree/stash/commit/push | 本地 Git | N/A | 0 | 0 | 本轮未授权、未执行；使用逻辑隔离 |

## 7. 已知限制与下一步边界

- 当前只完成 D0 文档与隔离记录；Timeline selector、组件、页面组合、测试、canonical smoke 和 D4 均未实施。
- `yijie` 的 FEAT-133 包保持未提交；`yijie-desktop`、Runtime、Contracts、Host 与其余仓库应保持 clean。
- `ChatPage.vue` 未修改；该限制是本 D0 阶段写入边界，不被扩大解释为整个 Feature 永久不能做最小页面组合。
- 没有新增 Markdown/UI 依赖；若受限内容树不足，需要 Owner 对具体依赖另行批准。
- 不使用真实 prompt、人工 Codex 证据、攻击性 fixture、故障注入、权限破坏、二进制替换或异常强杀。
- D0 完成不等于 Timeline 可用。后续最终结论只能是“Timeline 框架局部完成，Epic 尚未完成”。
