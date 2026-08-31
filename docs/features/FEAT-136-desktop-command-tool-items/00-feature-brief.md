# FEAT-136 — Desktop Command 执行 Item（Tool 后移）Demo Brief

> Profile: demo_fast · Exposure: local · Created: 2026-08-29 · Scope rebaseline: 2026-08-30
>
> 当前结论：Owner 已按原子结果重基线 FEAT-136。Command scope 为 **usable / implementation complete / verification PASS / D4 PASS**；真实 Tool scope 转移至 FEAT-144。Epic 仍未完成，FEAT-144 仍为 **blocked / NOT RUN**。

## 1. 用户结果与当前 Must

FEAT-136 只交付 CAP-016 / GS-003 中已有 fresh real 证据的 Command 结果：

1. 真实成功 Command 形成且只形成一个 completed terminal，含 exit 0 与 duration。
2. 代表性安全失败 Command 形成且只形成一个 failed terminal，含非零 exit、duration 与 stable error。
3. Command 使用闭合安全投影与安全复制，不暴露 raw Runtime、绝对路径、秘密或 wire。
4. Desktop 正常关闭重开后，SQLCipher 对 completed/failed 各 hydrate 一次，不重复、不回滚。
5. Command UI 在 light 与 200% 下可读，可用键盘展开/折叠，以状态文字、图标和 aria-live 表达结果。

上述五条均由最终产品 SHAs 和 stable artifact 下的 fresh real tranche 支持。原四类结果被拆为五个可独立验收的 Must，以分别保留成功和失败 terminal/cardinality 的证据边界。

## 2. 最终冻结基线

| Repository | Final local commit | 状态与角色 |
|---|---|---|
| yijie-codex | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean；Owner-authorized minimal producer patch；reported 0.144.6；此后冻结，不再修改 |
| yijie-contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean；unpublished v0.7.0；精确固定最终 Runtime |
| yijie-agent-host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean；精确固定 Contracts 与 stable Runtime artifact |
| yijie-desktop | `7026b47828961e58854b06c822c9c9e11252260d` | clean；精确固定 Host/Contracts/artifact，并提供 canonical stable runner |
| yijie | `3a6b37ee708a71af561929429fdcf778d5667c32` + 本次最多一个治理 commit | fresh Command 证据与本次治理文档 |

- 原始冻结基线 Runtime `0ce5902ed400866be0196886bb78f693a004d68d` / upstream rust-v0.144.6 保留为历史。
- Owner 后续仅授权 early sandbox-denial 的最小 canonical started+failed producer source repair，形成当前最终冻结 commit；版本、schema corpus 与协议族没有升级。
- 原始 Contracts 输入 `3c3000a6fbe2f08ab2131a463a1691e867d661b1`、Host/Desktop 原始实施基线及 prior D4/RCA commits 均保留历史，不被重写。
- canonical manifest SHA-256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`（1475 bytes）；binary SHA-256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`（355676760 bytes）。

## 3. Owner 原子化范围决策

| 原 FEAT-136 能力 | 当前归属 | 当前事实 |
|---|---|---|
| completed terminal/cardinality | FEAT-136 AC-001 | fresh real PASS |
| failed terminal/cardinality、exit/duration/stable error | FEAT-136 AC-002 | fresh real PASS |
| 安全投影与复制 | FEAT-136 AC-003 | fresh real PASS |
| SQLCipher hydration | FEAT-136 AC-004 | fresh real PASS |
| light、键盘、状态/aria-live、200% | FEAT-136 AC-005 | fresh real PASS |
| approval reverse request；Runtime Cancel 形成的 declined outcome | FEAT-137 phase 1 | immutable source conformance PASS；真实allow/cancel与D4 NOT RUN；独立decline用户动作deferred，不属于当前Must |
| replay、live event_id、late event、unknown/resync | FEAT-142 | NOT OBSERVED / NOT RUN；不得伪造 PASS |
| 完整 started/output-delta 集成状态顺序 | FEAT-143 | live individual event 未捕获；source tests 仅作基础 |
| dark、精确 1180×760 | FEAT-143 | NOT RUN |
| 真实 Tool producer、产品入口、安全边界、Tool-only AC、GS-004、Tool D4 | FEAT-144 | blocked / NOT RUN |

通用 Tool schema、Host 投影和 Desktop consumer/UI 基础可以保留为 compatibility foundation，但它们不构成 FEAT-136 的产品交付，也不能替代 FEAT-144 的真实 producer 与 D4。

## 4. Command D4 证据边界

- canonical local/demo_fast stable 入口使用 `experimentalApi=false`、`sandbox=read-only`、`approvalPolicy=never`，FEAT-134/136 gates 开启。
- fresh 授权上限为 5 次，实际使用 1 次且无重试；单次请求只产生两个独立 allowlisted 只读 Command。
- Desktop 恰好显示 completed 1 与 failed 1；exit 分别为 0 与 128，duration 均为 0ms，失败 stable code 为 `command_failed`。
- 正常关闭并重开后 Items=2、completed=1、failed=1；再次正常关闭，未通过异常退出制造证据。
- light、键盘折叠、状态文字/图标、aria-live、安全复制与 200% 均通过。
- prior 3/3 FAIL 和 RCA 0-call 是历史；fresh 1/5 PASS 不覆盖它们。

本次治理批不启动 Desktop、Runtime、Provider 或模型，真实调用为 0；D4 结论复用产品 SHAs、cross-pins 与 artifact 未变化的 fresh evidence。

## 5. 未观察项与安全边界

- natural replay、live event_id 与 late event：**NOT OBSERVED**，转 FEAT-142。
- unknown/resync real vertical：**NOT RUN**，转 FEAT-142。
- dark 与 exact 1180×760 live：**NOT RUN**，转 FEAT-143。
- Item started 与独立 output-delta live：执行过快未独立捕获；完整集成状态顺序转 FEAT-143。
- Tool D4：**NOT RUN**；没有注册 MCP/Connector/dynamic tool，也没有制造 producer。
- 不涉及 FileChange、Diff、审批、写权限或 FEAT-138。
- 不强杀、不故障注入、不破坏权限、不替换 binary、不使用攻击 fixture。

## 6. 结论

- FEAT-136 D0：PASS。
- FEAT-136 D4：PASS（仅收窄后的五条 Command Must）。
- Feature：usable；implementation complete；verification PASS。
- CAP-017 / GS-004：仍是 Epic active scope，由 FEAT-144 独立承接，当前 blocked / NOT RUN。
- Epic：未完成；不得把 FEAT-136 的 Command 收口扩写为 Tool 或整体 Epic 完成。
