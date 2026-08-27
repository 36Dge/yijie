# FEAT-133 Demo 验证

## 1. 当前门禁状态

| Gate | Result | 说明 |
|---|---|---|
| D0 | PASS | 正式 Brief、机器字段、Must AC、隔离记录、strict checker 与 claims audit 均完成 |
| D4 | NOT RUN | 实现、自动化、真实 UI 和代表性失败/恢复尚未开始 |
| DP | N/A | `exposure=local`，不提供公网入口 |

本文件不会把 D0 文档完成写成产品实现完成。D0 验证通过后，8 条 AC 仍保持 `pending`，
`implementation.status=pending`，`verification.status=NOT RUN`。

## 2. D0 Focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie` | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict --gate D0 docs/features/FEAT-133-desktop-conversation-timeline-item-shell` | 0 | PASS：schema v3 semantics 与 D0 产品/UX门禁 | 2026-08-27 |
| `yijie` | `node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs --audit-claims docs/features/FEAT-133-desktop-conversation-timeline-item-shell` | 0 | PASS：D0 声明审计 | 2026-08-27 |
| `yijie` | `pnpm feature:audit -- --base-ref aed49b78f21c264bb13c05c1976f11f7fc14b520` | 0 | PASS：working-tree 12 个 claims，包含未跟踪 FEAT-133；direct checks 另作定点复核 | 2026-08-27 |
| `yijie` | `pnpm lint` | 0 | PASS：10 仓 manifest 与 Contract First governance | 2026-08-27 |
| `yijie` | `pnpm test` | 0 | PASS：48 tests | 2026-08-27 |
| `yijie` | `bash -n scripts/*.sh` | 0 | PASS：Shell syntax | 2026-08-27 |
| `yijie` | wrapper 对 5 个未跟踪文本文件捕获 `git diff --no-index --check /dev/null <file>` 诊断（允许“存在新增 diff”的底层 exit 1），仅在有诊断时失败；随后扫描 whitespace/conflict/placeholder | 0 | PASS：wrapper 无 whitespace diagnostics、冲突标记或未完成占位符 | 2026-08-27 |
| multi-repo | 11 仓 `branch/HEAD/status`、D0 allowlist、关键保护 hash 与 `ChatPage.vue` blob/SHA-256 复核 | 0 | PASS：只有 yijie/FEAT-133 包 untracked；其余 10 仓 clean，ChatPage 未变化 | 2026-08-27 |

未跟踪 Feature Package 不会出现在普通 `git diff --stat`/`git diff --check` 中。D0 范围审阅必须组合：

1. `git status --short`；
2. 包内实际文件清单；
3. 对每个未跟踪文本文件执行独立 whitespace/conflict-marker 检查；
4. strict D0 checker 与 claims audit；
5. 11 仓最终 status 和保护 hash 复核。

## 3. Must AC 状态

| AC | Result | 计划证据/Artifact |
|---|---|---|
| AC-001 | NOT RUN | selector/DOM order/identity tests + canonical history smoke |
| AC-002 | NOT RUN | 安全内容树、良性惰性 markup/text、无可执行节点/隐式导航 tests |
| AC-003 | NOT RUN | disclosure、长度阈值、键盘与 final non-collapsible tests |
| AC-004 | NOT RUN | unknown ViewModel、固定 code、canary 与相邻 Item tests |
| AC-005 | NOT RUN | clipboard success/rejection、live region、焦点与正文快照 tests |
| AC-006 | NOT RUN | empty/loading/error/permission-denied 状态矩阵 + canonical empty/history smoke |
| AC-007 | NOT RUN | a11y/focus tests + light/dark/1180×760/200% zoom/keyboard smoke |
| AC-008 | NOT RUN | FEAT-127 attachment_reference、FEAT-128 artifact_reference 与既有组件集成回归 |

## 4. 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | `cd ../yijie-desktop && pnpm tauri:demo-fast:stable`；核对零登录、ready、Runtime 0.144.6、`experimentalApi=false`，再正常 Quit | Desktop local / fixed Runtime | 当前 D0 未启动 Desktop | NOT RUN |
| Real happy path | 使用 FEAT-132 已存在的无敏感 1 user + 1 assistant 历史和新建空 Thread；不发送新 prompt | canonical stable / existing history | 实现尚未开始 | NOT RUN |
| Representative failure/retry | 安全组件 fixture 覆盖 unknown、permission denied、clipboard rejection、惰性 markup 与外链不自动打开；不强杀/故障注入/破坏权限 | Vue tests / normal lifecycle | 实现尚未开始 | NOT RUN |

FEAT-133 没有新的真实 prompt 授权。FEAT-132 的累计 2/2 授权已经耗尽，不能复用或转移。

## 5. UI 与真实结果计划

- Yijie Artifact：实现后保存脱敏 empty/history、light/dark、1180×760、200% zoom 与键盘焦点证据。
- Codex reference Artifact：不需要、不等待；先前三张人工材料已撤回且不得引用。
- Loading/error/retry：必须证明历史不会被清空、错误不吞掉其他 Item、恢复入口不会越权。
- 最终真实用户结果：实现后必须在一次 fresh canonical run 中按领域顺序展示 Timeline，并通过 8 条 Must AC。
- 最终结论固定为“Timeline 框架局部完成，Epic 尚未完成”；D0 阶段不能提前使用该完成结论。

## 6. 工作区隔离与边界验证

修改前关键基线：

| Authority | Branch/HEAD 或 hash | 状态/约束 |
|---|---|---|
| `yijie` | `aed49b78f21c264bb13c05c1976f11f7fc14b520` | clean-start；D0 只允许 FEAT-133 包 |
| `yijie-desktop` | `f96fe05ca81d6bc7fac97ecbf81bcbab32b8aaa0` | clean；D0 全仓只读 |
| `ChatPage.vue` | blob `ea2c3a1e606d687981d7a11fec3ac7196baa56f9`; SHA-256 `b89e1204864656de800c5d2682100116b2784ebd17b48534b705ba58bb8dfef1` | 本轮不得修改 |
| FEAT-132 domain | SHA-256 `148a3f573f62139175906fb2f5073eab60bc91ceab12135522def56252a99490` | `conversation-state.ts` 只读 |
| FEAT-132 adapter | SHA-256 `834094b683e63e26fddf65ac03475fe7e73097ae3dc3f74ead02574790e273a8` | `chat-conversation-adapter.ts` 只读 |
| FEAT-132 store | SHA-256 `89832e87dccc0f53cf379a85ed3eae6ca3ebaae9e2839aa298a042d33f545f4a` | `chat.store.ts` 只读 |
| Desktop dependencies | `package.json` SHA-256 `8316e5a4013242e7ef1b7e3480c928b2ced1dca6b23eb5e652e2887d4eced7b9`; `pnpm-lock.yaml` SHA-256 `e48e21dd9f40eede7e4116313d72f00cc89d12dcdab7ea12d65c30d7c3e5f687` | 不新增依赖 |
| Desktop `src-tauri` | Git tree `4d59b67cc602f76f0b9603614d0057741c97a109` | D0 只读；FEAT-133 默认不修改 |
| Runtime | `0ce5902ed400866be0196886bb78f693a004d68d`; baseline SHA-256 `57c0f2c77754c3a686511524e20108c977580743af305467d614ebac7c2730ce` | fixed / clean / no build |
| Contracts | `164b14f609537d727a52326832da04430aecc4ab`; manifest SHA-256 `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311` | clean / unchanged |
| Host | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` | clean / unchanged |

完整 11 仓 snapshot 和停止条件见 `evidence/workspace-isolation-baseline-2026-08-27.md`。

## 7. Diff 与限制

- `git status`：PASS；只有 `yijie` 的 FEAT-133 目录为未跟踪改动，其他 10 仓 clean。
- 普通 `git diff --stat` / `git diff --check`：对未跟踪包不具覆盖力，不能据此声称包 diff 已审阅。
- 包文件审阅：PASS；文件清单恰好 5 项，placeholder/whitespace/conflict scan、strict D0 与 claims audit 均通过。
- 产品实现 diff：不存在，完整 diff review 为 `NOT RUN`。
- 已知限制：没有独立 FEAT-133 branch/worktree；本轮不修改 Desktop；没有新依赖；没有真实 prompt；D4 未开始。

## 8. Public Demo（仅 exposure=public）

- 本 Feature `exposure=local`，`public_readiness.required=false`。
- 密钥、公网鉴权、公开输入边界、付费 API 限流与公网 smoke 均为 N/A，不得据此声明 Production Ready。

## 9. 结论

- `D0` 产品/UX可实施：PASS。
- `D4` 本地真实可用：NOT RUN。
- `DP` 公开 Demo 可用：N/A。
- 验证时间：`2026-08-27`。
- 当前事实：正式 D0 治理与工作区隔离记录已通过；Timeline 实现尚未开始，Epic 尚未完成。
