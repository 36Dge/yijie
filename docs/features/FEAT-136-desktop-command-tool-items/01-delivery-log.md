# FEAT-136 — Delivery Log

> 当前状态：fresh Command tranche **PASS**；FEAT-136 整体仍 **ACTIVE / IN PROGRESS**；Tool D4 **BLOCKED / NOT RUN**。
>
> 本日志保留 prior attempt 与 RCA 历史，不用 fresh 1/5 结果覆盖旧 3/3 FAIL，也不把 Command tranche 扩写为完整 Feature D4。

## 1. 执行边界

- Profile / exposure：demo_fast / local。
- 正常入口：Desktop canonical stable runner；FEAT-134/136 gates 开启。
- 固定运行参数：experimentalApi=false、sandbox=read-only、approvalPolicy=never。
- fresh 请求上限：Owner 允许最多 5 次 Provider/模型请求；实际 1 次，无重试。
- 只允许成功只读形式与 missing-ref 安全失败形式；若出现其它命令则正常停止。
- 禁止 Tool D4、FileChange、Diff、审批、写权限、FEAT-138、强杀、故障注入、权限破坏、binary 替换与攻击 fixture。
- 允许 local commits；禁止 amend、push、tag、merge、publish、release 或 deploy。

## 2. Commit 与 pin 台账

| Repository | Prior authority / baseline | Final local commit | 当前状态 |
|---|---|---|---|
| yijie-codex | `0ce5902ed400866be0196886bb78f693a004d68d` / upstream rust-v0.144.6 | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean；Owner-authorized producer repair；reported 0.144.6 |
| yijie-contracts | 第一批 immutable input `3c3000a6fbe2f08ab2131a463a1691e867d661b1` | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean；unpublished v0.7.0；精确 repin Runtime provenance |
| yijie-agent-host | base `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`；prior D4 `83d3163e21579042d2cc21f303e943946ff97eb0` | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean；pin Contracts 与 stable artifact |
| yijie-desktop | base `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51`；core `69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba`；entrypoint repair `65ee3062833ef3d185511599d8f3a4018f635369` | `7026b47828961e58854b06c822c9c9e11252260d` | clean；pin Host/Contracts/stable artifact |
| yijie | prior D4 FAIL evidence `be5c1f91bd1c0f1f10878ea279721dac4eab3dc8` | RCA blocker `5b637fc3c0cd10e8294011857764884750435415` + 本次唯一 fresh D4 evidence commit | 回填前 clean；只改四文件包 |

Cross-pin 最终审计：

- Host → Contracts `87f94c9…`。
- Contracts compatibility → Runtime `b2b20e2…`。
- Desktop → Host `96b1fa1…` / Contracts `87f94c9…`。
- Host managed artifact 与 isolated final release 同一对：manifest `1cfa2e0…` / 1475 bytes，binary `4efe16d…` / 355676760 bytes。
- manifest version 与 Runtime reported version 均为 0.144.6。

## 3. 批次时间线

### 3.1 D0 与 Contracts

- 建立 schema v3 / demo_fast / local 正式四文件包。
- 确认 FEAT-138 已 Owner-cancelled / excluded，相关 FileChange/Diff 能力不进入 FEAT-136。
- 从固定 Runtime canonical facts 设计显式协商 v5；v1 至 v4 source/route/consumer 语义保持不变。
- Contracts v0.7.0 完成 schema/proto/OpenAPI/AsyncAPI、普通 fixture、生成一致性、lint、safe tests 与 breaking checks，形成 prior immutable input `3c3000a6…`。

### 3.2 Host / Desktop source conformance

- Host 完成 gated v5 negotiation、Command mapper/redactor/caps、event ID/replay、completed reconciliation 与 generic Tool projection，不制造 Tool producer。
- Desktop 完成 v5 closed decoder、event-ID reducer、SQLCipher v10 additive migration、mixed history hydration、Command/Tool UI、unknown fail-soft 与 accessibility。
- Host→Desktop 对同一 schema 与 11 个普通 fixture 完成 source-anchored conformance；该证据不冒充真实 Runtime vertical。

### 3.3 canonical entrypoint gate repair

- stable runner 同步开启 FEAT-134/136 Native/Web gates；非 stable/release 路径清除 ambient FEAT-136。
- stable build 与 sidecar 在清理环境后只转发依赖闭合的 allowlisted gate。
- exact preflight 固定 Contracts/Host commits、Runtime artifact pair 与 v4 不变量。
- repair 定向测试和独立审查 PASS，无 P0/P1/P2。

### 3.4 Prior Command D4（历史，3/3 FAIL）

- Call 1 发现历史 bookmark 指向非 Git 空目录；两个安全只读结果均为非零，归类环境/项目绑定失败。
- Call 2 在同一任务创建的隔离 Git repo 中得到一个成功和一个安全失败结果；Desktop 只有成功 completed Item，失败 lifecycle 缺失。
- Call 3 单独重复安全失败形式；仍无 failed Item/stable error。
- 旧授权 3/3 用尽且停止。App 均正常关闭；没有自动或超额重试。该历史 verdict 保持 FAIL。

### 3.5 Failed lifecycle RCA（历史，0 次请求）

- Runtime canonical 语义本应对非零结果发布 failed terminal。
- 四个既有非零窗口都没有 Runtime Command started/completed notification；首次丢失早于 Host intake。
- 根因定位为 early sandbox-denial 的 pre-emitter return：普通快速非零结果被启动诊断误判后，在 emitter 建立前返回。
- Contracts/Host/Desktop 对合法 failed Item 的语义和消费链均成立；从模型 output 补造 Item 会破坏 authority，明确拒绝该伪修复。
- 当时 Runtime freeze 使 repair BLOCKED；RCA 证据 commit 为 `5b637fc3…`。

### 3.6 Owner-authorized Runtime producer repair

- Owner 单独授权 Runtime producer patch/升级边界，使 early sandbox-denial 路径也发布 canonical started 与 failed terminal。
- Runtime 采用 source patch并补回归；没有 binary 替换、篡改或伪装。最终 source commit 为 `b2b20e2…`，reported version 保持 0.144.6。
- Contracts 精确 repin Runtime provenance，Host pin v0.7.0 与 exact stable artifact，Desktop pin Host/Contracts/artifact。
- Runtime、Contracts、Host、Desktop 定向测试和独立复审通过；四仓 clean，无 P0/P1/P2。
- 未新增 MCP/Connector/dynamic-tool registration/config；Tool producer 仍不存在。

### 3.7 Fresh Command tranche（当前，1/5 PASS）

- Owner 于 `2026-08-30T10:30:59+08:00` 把 fresh 额度提高为最多 5 次。
- preflight 验证 canonical stable artifact、gates、read-only/never 设置、隔离 Git repo、benign untracked 文件和 missing ref 均符合要求。
- 只发起 1 次 Provider/模型请求；没有重试，也没有第 2 至第 5 次请求。
- 单次请求内 Agent 恰好执行两个独立的允许 Command；没有第三条或其它命令。
- Desktop 最终恰好显示两个 Item：
  - completed：exit 0，duration 0ms，安全/脱敏 output；
  - failed：exit 128，duration 0ms，stable error `command_failed`。
- Command 执行过快，Item started 与 output delta 未独立捕获；Runtime/Host/Desktop 定向 lifecycle 测试覆盖该协议路径。
- 正常 Cmd+Q 关闭，runner exit 0；canonical 重开后 SQLCipher hydration 仍恰好两个 Item（completed 1 / failed 1），再次正常关闭后端口 idle。
- natural reconnect/replay 未发生，记录 NOT OBSERVED；未断连、注入或伪造。
- live UI：light、键盘 focus/折叠、状态文字/图标、aria-live、安全复制、200% 缩放 PASS；dark 与精确 1180×760 live NOT RUN。
- 安全复制不含 raw command、绝对路径、秘密或 Runtime wire。整个 WebView 含用户自己提交的 allowlist 文本，因此不宣称 whole-WebView literal no-raw PASS。

## 4. 最终验证与复审

| Layer | Verification | Result |
|---|---|---|
| Runtime | canonical failed lifecycle repair、stable build identity、source/diff review | PASS；clean；无 P0/P1/P2 |
| Contracts | v5 focused、safe non-archive suites、generation/digest、lint、breaking | PASS；clean |
| Host | `make lint`、`make test-feat136`、artifact/compatibility checks、diff review | PASS；clean；无 P0/P1/P2 |
| Desktop | 7 targeted Vitest files / 131 tests；failed lifecycle/hydration Rust 3/3；typecheck；scoped ESLint；diff check | PASS；clean |
| Cross-repo | final SHAs、cross-pins、artifact digest/version、Tool registration inventory | PASS；Tool producer 不存在 |
| Real Command | fresh 1/5；completed+failed；normal reopen/hydration | PASS for fresh Command tranche |
| Real Tool | producer/Owner readiness | BLOCKED / NOT RUN |

## 5. 未执行项、影响与停止

- normal replay：NOT OBSERVED；因此不能把 source event-ID tests 表述为真实 replay。
- dark 与 exact 1180×760：live NOT RUN；静态配置仅覆盖 width 1180、height 780、minWidth 1180、minHeight 760。
- Tool D4：BLOCKED / NOT RUN；AC-005 仍 pending。
- 未执行 destructive/fault/attack/composite archive suites；采用安全定向测试，不伪造覆盖。
- 未触达 FileChange、Diff、审批、写权限、FEAT-138 或生产环境。
- fresh 调用实际 1/5，剩余 4 次未用；fresh tranche 完成后立即停止。
- FEAT-136 仍 active，implementation active，overall verification FAIL；D4 gate 预期不通过，因为 Tool 与多个 Must AC 尚未完成。
