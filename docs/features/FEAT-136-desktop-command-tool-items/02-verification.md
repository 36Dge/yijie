# FEAT-136 Demo 验证

> 当前 verdict：Owner-authorized Runtime repair、repin、复审与 **fresh Command tranche PASS**；真实请求 **1/5**。FEAT-136 overall verification 仍为 **FAIL / incomplete**，因为 Tool D4 BLOCKED/NOT RUN，且 replay/unknown/完整视觉等 Must 仍 pending。Feature 保持 active，不声明完整 D4 或 usable。
>
> 本文区分 prior 3/3 FAIL、RCA 0-call、fresh 1/5 PASS；不把 source conformance 或 component tests冒充未观察到的真实 replay/Tool/visual vertical。

## 1. D0 与 authority 检查

| Check | Result | 实际事实 |
|---|---|---|
| Feature envelope | PASS | schema v3 / demo_fast / local；Feature active |
| Product/UX | PASS | 用户、问题、结果、主流程、7 个 UI states 与 8 个 Must AC 已冻结 |
| Contract classification | PASS | semantic；closed v4 使用显式协商 v5，v1 至 v4 不变 |
| Runtime scope | PASS | `runtime_change=runtime`；Owner-authorized producer source patch；reported 0.144.6 |
| Scope exclusions | PASS | Tool producer、FileChange、Diff、审批、写权限、FEAT-138、experimentalApi 与 production 均未进入本批 |
| Safety | PASS | 只用正常启动/退出；无强杀、故障注入、权限破坏、binary 替换或攻击 fixture |
| Git protection | PASS | 五仓 clean；local commits only；无 amend/push/tag/merge/publish |

## 2. Final commit、pin 与 artifact

| Repository | Final commit | Verification |
|---|---|---|
| yijie-codex | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | Runtime repair source与 artifact provenance clean |
| yijie-contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | v0.7.0，兼容性精确指向 final Runtime |
| yijie-agent-host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | Contracts/artifact exact pin，Host focused PASS |
| yijie-desktop | `7026b47828961e58854b06c822c9c9e11252260d` | Host/Contracts/artifact exact pin，Desktop focused PASS |
| yijie | `5b637fc3c0cd10e8294011857764884750435415` + 本次唯一 evidence commit | 只回填四文件包 |

- canonical manifest SHA-256：`1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`，1475 bytes。
- canonical binary SHA-256：`4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`，355676760 bytes。
- manifest version / reported Runtime version：0.144.6。
- cross-pins：Host→Contracts `87f94c9…`，Contracts→Runtime `b2b20e2…`，Desktop→Host `96b1fa1…` / Contracts `87f94c9…`。
- final read-only cross-repo audit：PASS，无 P0/P1/P2；未发现 MCP/Connector/dynamic-tool registration/config 或 Tool producer 新增。

## 3. Source 与 focused 验证

| Layer | Focused evidence | Result |
|---|---|---|
| Contracts | v5 schema/fixtures、safe non-archive tests、scoped generation/digests、lint、v1 equality、双基线 breaking | PASS；v1-v4 不变量保持 |
| Runtime | early-denial lifecycle regression、stable artifact identity/provenance、source/diff review | PASS；canonical started+failed repair成立 |
| Host | lint、FEAT-136 mapper/replay/reconciliation/compatibility tests、artifact pin、diff review | PASS；clean |
| Desktop | 7 targeted Vitest files / 131 tests | PASS |
| Desktop Rust | failed/nonzero reducer→SQLCipher reopen→IPC 2/2；v5 failed fixture 1/1 | PASS，3/3 |
| Desktop static | typecheck、scoped ESLint、diff check | PASS |
| Host→Desktop | exact v5 schema + 11 ordinary fixtures + producer/consumer suites | PASS；source-anchored，不等于 live replay |

未运行会触达预存危险 archive/攻击 fixture 或权限/故障破坏的 broad/composite suites；以上安全定向替代证据不扩写到未覆盖范围。

## 4. Prior attempt 与 RCA 历史

| Phase | Requests | Result |
|---|---:|---|
| Prior D4 Call 1 | 1 | bookmark 绑定到非 Git 空目录；环境/项目绑定失败 |
| Prior D4 Call 2 | 1 | 成功结果形成 completed Item；安全失败结果未形成 failed Item |
| Prior D4 Call 3 | 1 | 再次隔离安全失败；failed lifecycle 仍缺失 |
| RCA | 0 | 首次丢失定位到 Runtime pre-emitter early sandbox-denial return；downstream 无合法 producer 修复点 |

旧 3/3 授权已经用尽，prior verdict 保持 FAIL。历史 commits `3c3000a6…`、`83d3163e…`、`65ee306…`、`be5c1f9…`、`5b637fc…` 保持可追溯，不由 fresh 结果覆盖。

## 5. Owner repair 与 fresh Command tranche

### 5.1 授权与 preflight

- Owner 授权 Runtime producer patch/升级边界，并于 `2026-08-30T10:30:59+08:00` 把 fresh 调用上限设为 5。
- canonical local/demo_fast stable 入口；experimentalApi=false、sandbox=read-only、approvalPolicy=never；FEAT-134/136 gates 开启。
- 使用本任务创建的隔离、无敏感、无 remote Git repo；无 commit，恰好一个 benign untracked 文件，missing ref 预先确认不存在。
- 实际 Provider/模型请求 **1/5**；无重试；未发起第 2 至第 5 次请求。
- 单次请求内恰好执行两个独立 allowlisted 只读 Command；没有第三条或其它命令。

### 5.2 实际 lifecycle 与 cardinality

| Area | Result | 脱敏证据边界 |
|---|---|---|
| Canonical v5 gated projection | PASS | FEAT-134/136 gates 实际开启，v5-only Command projection 可见；未采集 Runtime wire，不声称 wire dump |
| Completed Command | PASS | completed、exit 0、duration 0ms、安全/脱敏 output |
| Failed Command | PASS | failed、exit 128、duration 0ms、stable `command_failed` |
| Command cardinality | PASS | 一个 Provider 请求、两个真实 Command、两个 Item；无第三条命令、无重复 Item |
| Started / output delta live | PARTIAL | Turn generating/progress transition可见；Command 执行过快，Item started 与独立 output-delta event 未直接捕获；协议/mapper/reducer 由 focused tests覆盖 |
| event identity / late event live | NOT OBSERVED | 真实 event_id 与 late event 未单独出现；未注入或伪造 |
| normal replay | NOT OBSERVED | 正常流程没有自然重连/replay；未断连制造 |

### 5.3 Hydration、UI 与安全

| Area | Result | 实际证据 |
|---|---|---|
| Normal shutdown/reopen | PASS | 正常 Cmd+Q，runner exit 0；canonical 重开；再次正常 Cmd+Q，runner exit 0；最终 loopback 端口 idle |
| SQLCipher hydration | PASS | 重开后 Command Items=2，completed=1，failed=1；每条只出现一次，无 terminal rollback |
| Disclosure / keyboard | PASS | Tab 到达 Command Item；Return 展开和折叠；焦点与内容保持 |
| Status / icon / aria-live | PASS | completed/failed 状态文字和图标可区分，live region 提供状态反馈，不只依赖颜色 |
| Safe copy | PASS | UI 显示复制成功；clipboard 不含 raw command、绝对路径、秘密或 Runtime wire，并保留显式脱敏标记 |
| Light | PASS | 当前系统 light 主题下 live 可读 |
| 200% zoom | PASS | AX 明确显示 200%；Items 仍可键盘/AX访问；随后正常恢复 100% |
| Exact 1180×760 | NOT RUN live | 静态配置 width 1180、height 780、minWidth 1180、minHeight 760；没有伪造 exact live 结果 |
| Dark | NOT RUN live | Desktop 跟随 macOS 系统外观；本批未修改系统主题 |
| Whole WebView literal no-raw | LIMITATION | Command projection、copy与四文件证据安全；用户消息自身含 allowlist 文字，因此不声明整页字面 no-raw PASS |

## 6. Host→Desktop 验证矩阵

| Area | Current result |
|---|---|
| Command completed/failed、exit/duration/stable error | fresh real PASS |
| Command started/output delta | focused source PASS；live individual events未独立捕获 |
| Duplicate event identity / legal duplicate text | focused source PASS；natural replay NOT OBSERVED |
| Completed snapshot / late-event seal | reducer/DB focused PASS；real hydration无回滚；live late event NOT OBSERVED |
| Caps/redaction/closed cwd/copy | source/component + fresh real PASS |
| SQLCipher/mixed history/hydration | focused + fresh real PASS，两个终态各一次 |
| Tool lifecycle/progress/result/error | generic source conformance PASS；real Tool BLOCKED/NOT RUN |
| Unknown Tool/event fail-soft/closed resync | focused PASS；real unknown vertical NOT RUN |
| v1-v4 compatibility | PASS |
| FEAT-138 exclusion | PASS；无 FileChange/Diff schema/event/fixture/UI/D4 |

## 7. Must AC 状态

| AC | Result | 当前证据边界 |
|---|---|---|
| AC-001 | PENDING | real completed/failed/exit/duration/stable error PASS；Item started/delta live 未独立观察 |
| AC-002 | PENDING | source event-ID/replay tests PASS；normal replay NOT OBSERVED |
| AC-003 | PENDING | source reconciliation/late-event + real no-rollback hydration；live event-ID/late event NOT OBSERVED |
| AC-004 | PASS | real completed/failed closed safety projection与安全复制 PASS |
| AC-005 | PENDING | generic Tool source PASS；real producer/Tool D4 blocked |
| AC-006 | PENDING | unknown/resync focused PASS；real vertical NOT RUN |
| AC-007 | PASS | real normal reopen后 completed/failed 各一次 |
| AC-008 | PENDING | Command live light/keyboard/200/copy PASS；dark、exact size 与 real Tool UI 未完成 |

## 8. 安全未执行项与影响

- 未强杀、故障注入、破坏权限、替换/伪装 binary 或创建攻击 fixture。
- 未通过断连、重放注入、late-event 注入或伪造制造事件证据；normal replay如实记为 NOT OBSERVED。
- 未更改 macOS 外观；dark live NOT RUN。未伪造 exact 1180×760 live。
- 未执行 Tool D4、MCP/Connector/dynamic tool 注册、生产写、公网访问、FileChange、Diff、审批、写权限或 FEAT-138。
- fresh 1/5 后立即停止，剩余 4 次未使用。
- 影响：fresh Command completed/failed vertical、hydration与核心 UI/安全成立；Tool、真实 replay/unknown/完整视觉仍未完成，所以整个 FEAT-136 D4 gate 必须保持 FAIL。

## 9. 最终结论

- D0：PASS。
- Contracts / Runtime repair / Host / Desktop：source-complete，final pins clean，独立复审 PASS。
- Fresh Command tranche：PASS，1/5 calls，completed 1 / failed 1，normal hydration each once。
- FEAT-136 overall verification：FAIL / incomplete；Feature active，不是 usable。
- Tool D4：BLOCKED / NOT RUN。
- App/Host 已正常停止；无 push/tag/merge/amend/publish。
