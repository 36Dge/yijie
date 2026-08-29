# FEAT-135 Demo 验证

> 当前结论：`D4 PASS` · Desktop immutable commit：`fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` · Verified: `2026-08-29T09:43:32Z`

## 1. Focused 与完整检查

| Repository/CWD | Command | Result |
|---|---|---|
| `yijie-desktop` | `pnpm vitest run src/components/chat/ChatComposer.test.ts src/pages/chat/ChatPage.test.ts src/stores/chat.store.test.ts` | PASS；3 files / 141 tests |
| `yijie-desktop` | `pnpm test` | PASS；104 files / 872 tests；generated Contract pins PASS |
| `yijie-desktop` | `pnpm lint` | PASS；ESLint 0 warning + vue-tsc |
| `yijie-desktop` | `pnpm build` | PASS；Vite production client build |
| `yijie-desktop` | `git diff --check`、clean HEAD、protected-path review | PASS；最终 HEAD clean，FEAT-135 diff 不触及受保护边界 |
| `yijie` | strict D4、claims、lint/test、diff/status | 由本治理收口执行并记录为 PASS |

## 2. 真实服务与 canonical happy path

| Check | Actual result | Result |
|---|---|---|
| final-source build/start | `pnpm tauri:demo-fast:stable` 从 `fc52ef33...` fresh build/start | PASS |
| zero-login direct entry | 无登录页、浏览器或账号密码，直达 `tauri://localhost/chat` | PASS |
| readiness | `/v1/status`: Host `ok`；Runtime ready、0.144.6、MiniMax-M3、managed-stdio、`experimental_api=false` | PASS |
| real submit | Owner 最终确认后发送 1 次无敏感纯文本；无工具、无任务文件读写 | PASS；1/1 |
| local durable behavior | 路由进入新 session，Composer 清空；content-free session ref `01a04ce5-836b-7272-a91e-252d61efd5c6` | PASS |
| terminal result | 当前 Turn content-free 状态为 completed；不保存或复述 prompt/final 正文 | PASS |
| normal cleanup | 使用 Cmd+Q；runner exit 0；App/Host/Runtime 与 18081 listener 均消失 | PASS |

启动后曾为排除桌面自动化焦点陷阱正常 Cmd+Q 并 fresh 重启；重启前没有发生 submit 或 Provider 调用。最终计费/Provider 动作仍精确为 1/1。

## 3. Must AC

| AC | Result | 证据 |
|---|---|---|
| AC-001 | PASS（自动化）；人工视觉 `WAIVED / NOT REQUIRED` | ChatComposer 22/22；auto-grow/max-scroll、actions 正常流、窄布局固定发送列与无新增依赖。Owner 豁免 light/dark、1180×760、200% 等人工视觉复验；不是视觉 PASS |
| AC-002 | PASS | Enter/button 同规则、Shift+Enter、IME、busy/disabled 与 submit 次数测试 |
| AC-003 | PASS | blank、attachment-only、文本+附件、10 个/10 MiB/64 KiB、ordered blocks 与 FEAT-127 回归 |
| AC-004 | PASS | permission/readiness/project/context/session/size/attachment authority fail-closed matrix |
| AC-005 | PASS | duplicate event coalescing、operation reuse/conflict、native/outbox/Item 唯一性 |
| AC-006 | PASS | create/reply accepted、no-op、reject、throw、mismatch、route race 与 matching-target clear |
| AC-007 | PASS | create/reply 焦点测试；accepted→唯一 queued identity→completed/failed/interrupted；terminal 不恢复草稿 |
| AC-008 | PASS | new/session target draft 隔离、切换恢复、late accepted race 与 FEAT-127/128/132/134 保护检查 |
| AC-009 | PASS | `active-turn-action` slot、Stop predecessor fallback、无新增 control IPC/Host/Contracts/Runtime 语义 |

## 4. 代表性 failure/retry

使用正常、确定性、非破坏性测试，不通过强杀或故障注入制造失败：

- pre-durable store no-op/reject/throw：草稿与附件保留，焦点/选择恢复；
- operation mismatch 与 stale target/route race：不清理错误 target；
- duplicate Enter/click：同一 pending intent 只调用一次；
- unchanged canonical input retry：重用 operation ID；内容改变则不复用；
- post-durable failed/interrupted：稳定用户 Item identity 不变，已提交文本/附件不回填 Composer；
- readiness/permission 恢复后可再次提交，不出现死循环或被困状态。

结果：`PASS`。

## 5. UI waiver 与证据边界

- Owner 指令：AC-001 人工视觉复验整体豁免；不再执行 light/dark、精确 1180×760、200% zoom、长输入截图或发送按钮人工可见性检查。
- reduced-motion 另经 Owner 豁免。
- 上述项目均登记为 `WAIVED / NOT REQUIRED`，不是 PASS，也不继承 FEAT-134 证据。
- AC-001 的工程行为仍由先红后绿的组件布局测试和完整 build 保证。
- D4 Artifact 使用 content-free canonical session ref、readiness 状态和正常清理事实；不使用已撤回人工 Codex 材料，不保存 prompt/reasoning/final 正文。

## 6. Diff、保护边界与限制

- `yijie-desktop`：`fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` clean；未 push。
- Contracts：`3832a6c5e99b2a6365f193280fdb887c8fdbc2de` clean；Host：`b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` clean。
- Runtime：`0ce5902ed400866be0196886bb78f693a004d68d` clean；未修改、升级、替换或重编译。
- 未改变 private IPC、database/migration、依赖、FEAT-127 attachment、FEAT-128 Artifact、FEAT-132 ConversationState 或 FEAT-134 streaming semantics。
- 文本草稿不跨应用重启持久化；local durable accepted 与 Host/Runtime terminal 仍是不同事实。
- exposure 为 local，DP/public/production N/A。

## 7. 结论

- D0：PASS
- D4：PASS
- DP：N/A
- Epic：仍未完成；FEAT-135 只完成 Composer 与新 Turn 提交能力
