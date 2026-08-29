# FEAT-135 Demo 验证

> 当前结论：D0 governance checks `PASS`；实现、真实服务与 D4 全部 `NOT RUN`。

## 1. Focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie` | `check-feature-package.sh --strict --gate D0 docs/features/FEAT-135-desktop-codex-style-composer` | 0 | PASS | 2026-08-29 |
| `yijie` | `validate-feature-package.mjs --audit-claims docs/features/FEAT-135-desktop-codex-style-composer` | 0 | PASS | 2026-08-29 |
| `yijie` | `pnpm lint && pnpm test` | 0 | PASS；10 repository manifests 与 Contract First governance valid；48/48 tests | 2026-08-29 |
| `yijie` | `git diff --check` and placeholder/trailing-whitespace scan | 0 | PASS | 2026-08-29 |
| all scoped repositories | branch/HEAD/status and changed-path negative sentinel | 0 | PASS | 2026-08-29 |

本节的 D0 governance PASS 不会把下方 startup、smoke、Must AC 或 D4 变为 PASS。

## 2. 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | 后续获得独立授权后运行 `cd ../yijie-desktop && pnpm tauri:demo-fast:stable` | Desktop local / `demo_fast` / fixed Runtime / `experimentalApi=false` | 本轮不启动应用 | NOT RUN |
| Real happy path | 后续验证多行、Enter/Shift+Enter/IME、文本/附件、防重复、local durable acceptance、target 清理与焦点 | canonical stable / no tools / no task file access | 本轮不发送真实 prompt | NOT RUN |
| Representative failure/retry | 安全 deterministic fixtures 验证 deny/no-op/throw/mismatch/route race/idempotent retry | Vue/store/native tests / normal lifecycle | 实现尚未开始 | NOT RUN |

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | NOT RUN | 后续 auto-grow/layout tests 与 canonical UI artifact |
| AC-002 | NOT RUN | 后续 Enter/Shift+Enter/IME/duplicate-submit component tests |
| AC-003 | NOT RUN | 后续 FEAT-127 attachment/ordered blocks regression tests |
| AC-004 | NOT RUN | 后续 permission/readiness/limits/authority matrix tests |
| AC-005 | NOT RUN | 后续 operation ID/idempotency/double-submit tests |
| AC-006 | NOT RUN | 后续 explicit submission result、draft retention 和 target race tests |
| AC-007 | NOT RUN | 后续 accepted→queued→terminal Timeline/focus integration tests |
| AC-008 | NOT RUN | 后续 target-scoped draft 与 FEAT-127/128/132/134 protection checks |
| AC-009 | NOT RUN | 后续 action-slot API 与 no-new-control-contract scoped diff |

## 4. UI 与真实结果

- 截图、录屏、Artifact 或脱敏 request ID：本轮没有；D0 不启动应用、不发送 prompt，也不沿用已撤回的人工 Codex 材料。
- Loading/error/retry 是否会困住用户：尚未实现或验证；D0 要求 validating/submitting 可区分、pre-durable failure 保留草稿、恢复条件明确且不越权。
- 最终真实用户结果：`NOT RUN`。目标结果是一个 Codex 风格近似且符合 Yijie Design System 的 Composer，不是版本专属或逐像素复制。
- D4 UI 基线：light/dark、1180×760、200% zoom、键盘、focus 与 reduced-motion 均待验证；FEAT-134 的三项 waiver 不继承。

## 5. Diff 与限制

- `git status`：`yijie` 仅新增 `docs/features/FEAT-135-desktop-codex-style-composer/`；`yijie-desktop`、Contracts、Host、Runtime 均 clean。
- `git diff --stat`：实现 diff 为 0；新治理目录尚未跟踪，因此普通 `git diff --stat` 不显示，changed-path 以 `git status --short` 和文件清单审计。
- `git diff --check`：PASS；治理目录 placeholder/trailing-whitespace scan 也 PASS。
- 完整 diff 审阅：D0 范围只允许本 Feature 治理目录；没有 staged、commit 或 push。
- 已知非阻断限制：文本草稿只保证当前 WebView 生命周期；local durable accepted 不等于 Host/Runtime complete；所有实现和 D4 声明仍为 `NOT RUN`。
- 安全跳过：不执行强杀、故障注入、权限破坏、binary 替换或攻击 fixture；后续失败验证使用正常生命周期和确定性安全状态。

## 6. Public Demo（仅 exposure=public）

- 密钥只在服务端环境/Keychain：N/A，`exposure=local`。
- 鉴权与数据边界：N/A；不改变 public/production。
- 输入/文件大小与超时：N/A；本地仍沿用现有 64 KiB 文本与 FEAT-127 附件限制。
- 付费 API 成本/频率上限：0；本轮未授权真实 prompt。
- 错误不泄露敏感内容：D0 文档只记录 content-free 架构事实。
- 最简恢复方式与公网 smoke：N/A，不提供公网入口。

## 7. 结论

- `D0` 产品/交互/Contract First/隔离：PASS。
- `D4` 本地真实可用：NOT RUN。
- `DP` 公开 Demo 可用：N/A。
- 验证时间：D0 于 2026-08-29 完成；D4 未排期。
