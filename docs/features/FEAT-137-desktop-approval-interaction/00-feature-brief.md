# FEAT-137 — Desktop 本地 Command 审批交互 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Created: `2026-08-30`
>
> 当前结论：Owner 已于 2026-08-30 明确批准第一阶段安全方案；**D0、Contracts/Host/Desktop component source、v4/v6 authority composition repair 与 clean-tree conformance PASS；fresh D4 已从 canonical stable entrypoint 启动，但真实 approval vertical BLOCKED，真实调用 4/7**。真实请求未形成可操作的 inline approval authority，因此 accept/cancel 与 Feature verification 不得标 PASS。

## 1. 用户问题与真实结果

- 目标用户：在易界 AI Desktop 的本地 demo_fast 会话中，需要明确决定一条受限只读 Command 是否执行的用户。
- 当前剩余问题：Contracts v6、Host authority、Desktop closed consumer/SQLCipher/inline UI 与 canonical v4/v6 authority composition 已完成本地不可变 source slice。真实 D4 中应用、Runtime、Host 与 Provider已启动，但请求分别收敛为无可操作 approval 的拒绝、直接完成、生成失败或跨正常重开持续等待；尚未完成真实 allow/cancel、approval replay/expiry 与 approval-card 人工视觉验收。
- 完成后的真实结果：唯一 allowlisted Git 仓库检查触发真实 approval；用户在对应 Command Item 内选择“允许一次”或“取消本轮”，Host 只响应一次，Runtime 与 Item/Turn 权威结果真实收敛。

本 Feature 仅承接 CAP-019 / GS-005。CAP-020 一般权限/MCP elicitation、CAP-021 `requestUserInput`、FileChange/Diff、平台业务审批和生产审批不属于 FEAT-137。

## 2. Owner 已批准的安全决策

1. 仅 exact `local + demo_fast + FEAT-137 gate` 启用稳定 `on-request`；FEAT-134/136 foundation 必须存在。默认、gate 关闭和非 local 明确保持 `never`。
2. sandbox 永远为 `read-only`；禁止写入、网络、额外权限、sandbox/unsandboxed escalation。
3. 第一阶段只有 `accept once` 与 `cancel current turn`。不提供独立 `decline-and-continue`、session approval、exec-policy/network amendment 或“始终允许”。
4. 唯一 Command 是单一 argv `git rev-parse --is-inside-work-tree`；cwd 必须等于当前 workspace root。禁止 shell wrapper、管道、重定向、环境赋值、多 action 和其它命令。
5. Host 使用固定安全 identity `git_repository_check` 与 allowlisted 摘要，不依赖 Runtime experimental `availableDecisions`，也不把 raw command/cwd/reason 送入 WebView。
6. Pending TTL 为 120 秒。TTL 在 first-writer-wins 竞争中先到时，Host 只向仍在等待的 Runtime request 发送一次 `Cancel`，UI/audit 投影 stable `expired`；若 Runtime、Item 或 Turn 已先清理，则投影 `resolved_elsewhere` 且不再响应。
7. Desktop/SSE 断线立即禁用动作；正常重连只按 Host pending snapshot 对账，不自动批准或离线提交。
8. Pending 只驻留 Host 内存；resolved content-free audit 每 session 最多 128 条并随 session 删除。
9. 审计只含 opaque identities、stable result code、request/resolution timestamps；禁止 command、cwd、reason、secret 和 Runtime wire。
10. Contracts 后续新增独立、显式协商的 v6 approval surface，v1-v5 和现有 Runtime exact-shape manifest 保持不变。
11. Runtime 固定为 `b2b20e2…` / 0.144.6；不修改、升级、替换、重编译、重新 pin 或开启 experimental API。
12. D0 的真实调用额度为 0；Owner 于 2026-08-31 单独授权 fresh D4 最多 7 次真实调用及受限调用层自动重试。approval decision POST 仍严格单次、不得自动重试。本轮实际使用 4/7；没有发出 decision POST，剩余 3 次因 live blocker 未继续消耗。

## 3. 最终冻结输入

| Repository | Commit / version | D0 状态与角色 |
|---|---|---|
| yijie-codex | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` / 0.144.6 | clean；最终冻结 Runtime authority，只读、不修改 |
| yijie-contracts | `2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6` / unpublished v0.7.0 | clean；FEAT-137 v6 local immutable authority；parent `87f94c9…` |
| yijie-agent-host | `118651804b7f5a7849bc68cdf29d88c74a21f8a1` / tree `9ae73d7b6f024bda241071371487a627810c1058` | clean；基于首个冻结 candidate `01c4a406…` 的 TTL/ack 与 late-cleanup 修复 authority |
| yijie-desktop | `27d6c6a2a9f8a9984b47b27143f8c9090815dbd3` / tree `6cefcc7a6deed7924f64ba32b06ac7c084fd654d` | clean；v4 从历史 immutable Git object 验证 source/digest，v6 继续由当前 Host `118651804…` 提供运行实现；无 capability/plugin/CSP/dependency 扩张 |
| yijie | D4 前 authority `061c861fa48e5b4a38696b12abf2322ed0e6d837` | clean preflight；本轮只回填 FEAT-137 四文件，最终治理 commit 在批末记录 |

Contracts source-first 批已在 `yijie-contracts/feat/feat-137-contracts-v6-approval` 创建 local commit `2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6`，tree 为 `0041ca35366ec4718f9937398924983591bd7010`，父提交为 `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb`。提交后 safe generated/build、focused 25/25、安全合规 Node 88/88、Go、lint、双基线 equality/breaking 与 clean-tree authority audit 全部 PASS；v1-v5 和 `agent-host-runtime-v1.json` 保持不变。Host 与 Desktop 首次冻结后的独立复审发现 decision 在截止前 commit、Runtime ack 在截止后到达时可能生成非法时间窗 terminal；Host `118651804…` 已以 commit 时刻作为 decision winner 时间、让 deadline 后 pending cleanup 归并到 TTL winner，并补确定性 race tests与 retained/HTTP window validation。Desktop 随后精确 repin 到该 Host SHA。最终 Contracts→Host→Desktop clean-tree source conformance PASS；发布/tag/push 与 D4 仍未执行，真实调用为 0。

Runtime stable schema 提供 `item/commandExecution/requestApproval` 与 stable response decision enum，但 stable request schema 不包含可依赖的 `availableDecisions`。因此 Host 必须按本 Owner policy 固定投影两个决定，并兼容忽略 Runtime 可能发送的该额外字段；不得把它提升为 stable contract 事实。

## 4. 完整主流程

1. 用户通过 canonical local/demo_fast stable runner 进入实际对话页；exact FEAT-137 gate 关闭时维持既有 `read-only/never`。
2. gate 开启时 Host 在 `thread/start` 和 `turn/start` 显式使用 `on-request/read-only`，并装配受管、精确的单 Command prompt policy。
3. Runtime 发出 stable Command approval reverse request。Host 校验 session/thread/turn/item/request identity、argv、单 action、canonical cwd 和无网络/权限提升事实。
4. 合法请求进入 120 秒内存 pending；非法、未知、FileChange、permissions、MCP 和 requestUserInput 请求立即 fail closed且不产生 Desktop action。
5. Contracts v6 requested event 与 owner-only pending snapshot 仅投影固定 action identity、安全说明、到期信息和 `accept_once/cancel_current_turn`。
6. Desktop 在对应 Command Item 内联显示卡片；提交决定时禁用按钮，不预先显示成功。
7. Host first-writer-wins 地向同一 Runtime request 回应一次。允许一次后 Command 仍只在 read-only sandbox 运行；取消本轮时 Command 不执行并由 Runtime/Turn authority 封口。
8. Desktop 只依据 Host/Runtime resolved 与 Item/Turn terminal 更新结果；断线重连按 Host snapshot 对账。TTL 先到时 Host 单次 `Cancel` 并投影 `expired`；Runtime/Item/Turn 已先清理时投影 `resolved_elsewhere`，旧卡片不可再操作。

## 5. UI 与交互

- 位置：对应 Command Item 内联区域，不使用全局 modal。
- 信息：固定业务动作“检查当前工作区是否为 Git 仓库”、安全 workspace 别名、120 秒有效期和当前状态；不显示 raw cwd、reason、wire 或任意参数回退。
- 主操作：“允许一次”；次操作：“取消本轮”。取消文案必须说明会停止当前 Turn，不使用模糊的“拒绝”。
- 焦点：新审批使用克制 `aria-live` 通知但不强抢焦点；键盘可进入按钮；resolved 后恢复到最近的稳定 Item/Composer 位置。inline approval 不使用 dialog focus trap。
- 安全复制：只复制固定 action label、stable status/result 与适用时间，不复制 command、cwd、reason、secret 或 raw payload。

状态定义：

| State | 行为 |
|---|---|
| Idle / Empty | 没有真实 pending 时不生成审批卡或假问答卡 |
| Pending | 显示固定安全摘要、有效期与两个决定 |
| Submitting | 两个按钮均禁用，等待 Host/Runtime authority |
| Accepted | 只表示本次决定已被权威接受；Command 最终结果仍看 Item terminal |
| Cancelled | 目标 Command 不执行；等待权威 Turn terminal |
| Expired / Resolved elsewhere | 卡片只读，动作禁用，显示 stable 原因 |
| Disconnected | 立即禁用；正常重连后按 Host snapshot 恢复为 pending 或 resolved |
| Permission denied / Version mismatch | fail closed，只显示安全诊断和下一步 |

## 6. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | exact gate 才启用 on-request；其它组合保持 read-only/never | Host config matrix、thread/turn request 与默认回归 |
| AC-002 | 真实 request 绑定完整 identity，在对应 Item 只显示安全摘要与两个固定决定 | Contracts/Host/Desktop conformance |
| AC-003 | 允许一次最多响应一次，Runtime 在 read-only 内继续并由真实 terminal 封口 | race tests + 后续真实 allow vertical |
| AC-004 | 取消本轮最多响应一次，Command 不执行且不伪装 decline-and-continue | cancel correlation + 后续真实 cancel vertical |
| AC-005 | 仅精确 argv/cwd/单 action 可进入 pending；其它命令与权限请求 fail closed | allowlist 与负向 focused tests |
| AC-006 | 重复、迟到、过期和 terminal cleanup 不重复决定或执行；TTL 先胜只单次 Cancel，权威清理先胜则 resolved_elsewhere 且不再响应 | duplicate/stale/expired/resolved_elsewhere/TTL-Cancel/race tests |
| AC-007 | 断线禁用，正常重连按 Host snapshot 对账，不离线批准 | transport/snapshot tests + 安全自然观察 |
| AC-008 | UI、日志、copy、SQLCipher/audit 均无 raw command/path/reason/secret/wire；audit 有界删除 | canary、redaction、retention tests |
| AC-009 | v6 显式协商且 v1-v5 不变；排除能力不生成 UI | generate/breaking/equality/unknown tests |
| AC-010 | 全状态内联、键盘/焦点/状态/aria-live/安全复制与后续视觉条件可验收 | Desktop tests + 后续 D4 manual smoke |

十条 Feature-level Must 继续全部为 `pending`：Host 可独立验证的 gate、wire、pending/decision、TTL、cleanup、redaction 与 v1-v5 compatibility 子项已有 source evidence，但每条仍包含 Desktop、真实 Runtime terminal、正常重连或 D4 条件，不能原子化标为 PASS。

## 7. Contract First 与后续顺序

`contract-impact=semantic`，因为 exact local profile 的 approval policy 和跨进程用户决定语义发生变化；默认与非 local 兼容性必须显式保护。

```text
frozen Runtime stable source/schema（只读）
  → Contracts v6 local immutable authority 2e490dea…（clean-tree audit PASS）
  → Host 118651804… exact gate/policy/pending/single-response/deadline/redaction/audit（clean immutable source PASS）
  → Desktop 918bd26b… v6 closed decoder/reducer/SQLCipher/inline UI（clean immutable source PASS）
  → Contracts→Host→Desktop clean-tree source conformance（PASS）
  → canonical stable entrypoint v4/v6 authority composition repair（PASS；Desktop 27d6c6a2…）
  → fresh real allow/cancel D4（BLOCKED：未形成可操作 inline approval authority）
```

现有 v5 是 closed Command/Tool Item contract，并明确没有 approval action；不得把审批变体塞回 v5，也不得修改 `agent-host-runtime-v1` 的冻结 exact-shape 含义。

## 8. 停止条件与明确非目标

- D0、Contracts/Host/Desktop local freeze、Host TTL/ack repair、v4/v6 authority composition repair 与 clean-tree component source conformance 已完成；canonical build/app/Runtime/Host 可正常启动。
- Fresh D4 使用 4/7 次真实调用后停止：一次无 card 的正常拒绝、一次未产生 approval 的直接 Command 完成、一次生成失败、一次跨正常重开仍等待；没有 accept/cancel decision POST。剩余 3 次不应用于重复同一 blocker。
- 不得绕过、删除或跳过 v4/v6 checker，也不得通过直接调用内部 command、伪造 pending、故障注入或提升权限补证。下一步需单独 RCA canonical live task/approval producer→Host pending→Desktop action authority 链路。
- 如果精确 prompt policy 无法在 `on-request/read-only` 下产生 stable request，保持 capability gap 并停止；不得改用危险 Command、`untrusted` 的潜在 unsandboxed retry、权限提升或 Runtime patch。
- 不实现 FileChange/Diff、CAP-020/021、MCP/平台/生产审批，也不注册或制造其它 producer。
- 只允许应用自身正常启动、停止、关闭和重开；不强杀、不故障注入、不破坏权限、不替换 binary、不使用攻击 fixture。

## 9. D0 verdict

- Product/UX 与 Owner security decision：PASS。
- Feature：active。
- Contracts local immutable authority / clean-tree audit：PASS；`contract.status=PASS`。
- Host v6 consumer pin / mapper / pending / decision / TTL-ack source slice：PASS（immutable clean commit）；Desktop consumer、SQLCipher、inline UI 与 exact repin：PASS（immutable clean commit）。
- Component source implementation/conformance 与 canonical entrypoint repair：PASS；aggregate implementation：BLOCKED（真实 approval authority 未到达 Desktop action UI）。
- Verification / real allow/cancel / D4：BLOCKED after canonical startup；accept_once、cancel_current_turn 与 approval-only Must AC 仍 pending。
- Runtime、Contracts、Host、Desktop：最终 clean；真实调用：4/7，decision POST 0，剩余 3 次未使用。

完成本 Feature 时只能表述为“本地 Command 审批局部完成，Epic 尚未完成；不代表 production approval ready”。
