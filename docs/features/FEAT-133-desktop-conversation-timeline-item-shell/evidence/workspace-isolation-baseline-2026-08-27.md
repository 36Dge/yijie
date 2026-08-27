# FEAT-133 D0 工作区隔离基线

> 捕获时间：`2026-08-27T20:40:31+08:00`
>
> 范围：`/Users/jack/Downloads/Personal_Info/CrossBSD`
>
> 模式：精确 HEAD + clean-start + 路径 allowlist + 保护 hash 的逻辑隔离

## 1. 隔离结论

创建 FEAT-133 scaffold 前，CrossBSD 下登记的 11 个 Git 仓库全部 clean。当前没有新分支、独立 worktree、
stash、commit、push、reset 或 clean 授权，因此本 D0 不虚构 FEAT-133 分支，而是在现有分支上仅允许写入
正式治理包。

创建 scaffold 后，预期且实际的唯一新增状态是：

```text
yijie:
?? docs/features/FEAT-133-desktop-conversation-timeline-item-shell/
```

`yijie-desktop`、`yijie-codex`、`yijie-contracts`、`yijie-agent-host` 与其余 6 个兄弟仓库继续 clean。
本记录只证明 D0 的文件范围，不证明 FEAT-133 产品实现、测试或 D4。

## 2. 11 仓 clean-start snapshot

以下 HEAD 均来自本地 `git rev-parse HEAD`；没有 fetch/pull/rebase，远端是否更新不在本记录声明范围。

| Repository | Branch | Full HEAD | Origin | 初始状态 |
|---|---|---|---|---|
| `yijie` | `feat/feat-131-desktop-codex-parity-baseline` | `aed49b78f21c264bb13c05c1976f11f7fc14b520` | `https://github.com/36Dge/yijie.git` | clean |
| `yijie-admin-web` | `develop` | `1e5c7783d98210d5ec03408ec9ff7824795d1127` | `https://github.com/36Dge/yijie-admin-web.git` | clean |
| `yijie-api` | `feat/feat-126-foundation-closure` | `451940b282d8dd3e232ed414bd44b0677897f4c4` | `https://github.com/36Dge/yijie-api.git` | clean |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | `https://github.com/36Dge/yijie-codex.git` | clean |
| `yijie-contracts` | `feat/feat-129-desktop-skill-marketplace` | `164b14f609537d727a52326832da04430aecc4ab` | `https://github.com/36Dge/yijie-contracts.git` | clean |
| `yijie-infra` | `feat/feat-126-s10e` | `42671b802d48ce0318abdefeeb01003cdc597825` | `https://github.com/36Dge/yijie-infra.git` | clean |
| `yijie-agent-host` | `feat/feat-129-desktop-skill-marketplace` | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | `https://github.com/36Dge/yijie-agent-host.git` | clean |
| `yijie-knowledge` | `develop` | `3e5682c4dacdc8031b433bfc956909172a8051b6` | `https://github.com/36Dge/yijie-knowledge.git` | clean |
| `yijie-connectors` | `develop` | `2624155f973e3f6121b5648d2d903fe72fee0210` | `https://github.com/36Dge/yijie-connectors.git` | clean |
| `yijie-desktop` | `feat/feat-131-desktop-codex-parity-baseline` | `f96fe05ca81d6bc7fac97ecbf81bcbab32b8aaa0` | `https://github.com/36Dge/yijie-desktop.git` | clean |
| `yijie-skills` | `develop` | `10c45bec29603b002e861e1499d5b4e684251af5` | `https://github.com/36Dge/yijie-skills.git` | clean |

## 3. D0 exact write allowlist

只允许以下 5 个路径出现 D0 写入：

```text
yijie/docs/features/FEAT-133-desktop-conversation-timeline-item-shell/feature.yaml
yijie/docs/features/FEAT-133-desktop-conversation-timeline-item-shell/00-feature-brief.md
yijie/docs/features/FEAT-133-desktop-conversation-timeline-item-shell/01-delivery-log.md
yijie/docs/features/FEAT-133-desktop-conversation-timeline-item-shell/02-verification.md
yijie/docs/features/FEAT-133-desktop-conversation-timeline-item-shell/evidence/workspace-isolation-baseline-2026-08-27.md
```

D0 阶段 `yijie-desktop` 写入 allowlist 为空。`ChatPage.vue` 不得修改；该条只冻结当前 D0 阶段，
不把后续经过 scoped review 的最小页面组合预先判定为整个 Feature 的永久非目标。

## 4. 关键保护对象

| Repository / path | Git object / SHA-256 | D0 约束 |
|---|---|---|
| `yijie-desktop/src/pages/chat/ChatPage.vue` | blob `ea2c3a1e606d687981d7a11fec3ac7196baa56f9`; SHA-256 `b89e1204864656de800c5d2682100116b2784ebd17b48534b705ba58bb8dfef1` | 不修改 |
| `yijie-desktop/src/pages/chat/ChatPage.test.ts` | blob `b18c03603c9ad6830e5a222856d7d5182ea3743e`; SHA-256 `547209afbf0bd80ac1d988fd355e597193146fbd0b04ea0c7ef40443b607670e` | 不修改 |
| `yijie-desktop/src/domain/conversation-state.ts` | blob `43f157148c04d65d5a61a29eee17b45cd85df7e2`; SHA-256 `148a3f573f62139175906fb2f5073eab60bc91ceab12135522def56252a99490` | FEAT-132 authority；D0 不修改 |
| `yijie-desktop/src/api/chat-conversation-adapter.ts` | blob `2e4f8a7783f3bc1c9fe9ccd61df7b2046046ec3e`; SHA-256 `834094b683e63e26fddf65ac03475fe7e73097ae3dc3f74ead02574790e273a8` | FEAT-132 adapter；D0 不修改 |
| `yijie-desktop/src/stores/chat.store.ts` | blob `6c099dac788b33b1d5dea0d556511f0dc26ce0c7`; SHA-256 `89832e87dccc0f53cf379a85ed3eae6ca3ebaae9e2839aa298a042d33f545f4a` | FEAT-132 state consumer；D0 不修改 |
| `yijie-desktop/package.json` | blob `b75eb8212c27acaa96f0fff0cc292d6ba9a8eb64`; SHA-256 `8316e5a4013242e7ef1b7e3480c928b2ced1dca6b23eb5e652e2887d4eced7b9` | 不新增依赖/脚本 |
| `yijie-desktop/pnpm-lock.yaml` | blob `1ce005d19942ed2cec6220d2779207b00a422e72`; SHA-256 `e48e21dd9f40eede7e4116313d72f00cc89d12dcdab7ea12d65c30d7c3e5f687` | 不修改 lockfile |
| `yijie-desktop/contracts/agent-host-skills-v1.lock.json` | SHA-256 `700d476571f172ef7d8c357f9ba407d2900b81955cefb8717e57d02651b0fd40` | 不改 contract pin |
| `yijie-desktop/scripts/run-local-demo-fast.sh` | SHA-256 `1819a2e0339febb13cf8f083ebc103c6b34bda44e3dd5ff2f0ecc4e91f9239ab` | canonical launcher 不变 |
| `yijie-desktop/src-tauri` | Git tree `4d59b67cc602f76f0b9603614d0057741c97a109` | D0 全树只读；FEAT-133 默认不修改 |
| `yijie-codex/.yijie/schemas/app-server/baseline.json` | SHA-256 `57c0f2c77754c3a686511524e20108c977580743af305467d614ebac7c2730ce` | fixed Runtime baseline |
| Runtime schema tree | SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` | 使用 FEAT-131 canonical 计算值；不重新生成 |
| `yijie-contracts/compatibility/agent-host-runtime-v1.json` | SHA-256 `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311` | compatibility manifest 不变 |

此外，FEAT-127 attachments、FEAT-128 Artifact components/cache/authority、ChatComposer、Sidebar、
所有 `src-tauri`、Host、Contracts、Runtime 及其余 6 个兄弟仓库在 D0 均为全范围 protected。

## 5. 验证方法

开始和结束均执行：

```text
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1
```

结束时必须满足：

- `yijie` HEAD 与 branch 未变化，status 只包含 FEAT-133 正式包。
- `yijie-desktop` HEAD、branch、status 与上述关键 hash 完全一致；尤其 `ChatPage.vue` 不变。
- `yijie-codex`、`yijie-contracts`、`yijie-agent-host` 的 HEAD 与 status 不变。
- 其余 6 个兄弟仓库继续 clean。
- 包内只包含 allowlist 的 5 个文件；不存在模板 placeholder、冲突标记或未说明的依赖/二进制。
- strict D0 checker 与 claims audit 实际 PASS。

未跟踪文件不会被普通 `git diff --check` 覆盖，因此不能用空 diff 冒充包内容检查。应对包内每个文本文件
单独执行 whitespace/conflict-marker 检查，并用 validator 解析 YAML 与 D0 语义。

## 6. 立即停止条件

- 任一 allowlist 外路径出现 diff/untracked 状态，或未知并行改动出现。
- `ChatPage.vue`、FEAT-132 authority、依赖锁、`src-tauri`、Runtime/Contracts/Host 的 HEAD/hash/status 漂移。
- 实现需要读取 raw wire，修改 FEAT-132 domain/adapter/store、Desktop IPC、Host、Contracts、Runtime、
  `src-tauri` 或持久化才能满足 AC。
- 需要新增 Markdown/UI 依赖、Tauri capability、原生 URL handler 或第二套 authority。
- 触及语音、模型版本、模型推理强度 UI、分享、置顶摘要、侧边面板、分支到新聊天或 GS-006 Diff。
- 需要真实 prompt、付费调用、生产写入、破坏性操作、branch/worktree/stash/commit/push 等新授权。
- strict D0 或 claims audit 不能基于真实文档通过。

发生停止条件时保留现状并报告，不通过 reset、stash、clean、强杀、权限破坏、二进制替换或故障注入
制造“干净/通过”结果。
