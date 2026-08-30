# FEAT-136 — Desktop Command 与 Tool 执行 Item Demo Brief

> Profile: demo_fast · Exposure: local · Created: 2026-08-29
>
> 当前结论：Owner 授权的 Runtime producer repair、Contracts/Host/Desktop 重固定、独立复审和 fresh Command tranche 均已完成。fresh tranche 使用 canonical local/demo_fast stable 入口，真实 Provider/模型请求 **1/5**，得到且只得到两个 Command Item：一个 completed、一个 failed；正常关闭并重开后 SQLCipher 仍各恢复一次。fresh Command tranche 判定 **PASS**。Tool D4 继续 **BLOCKED / NOT RUN**，因此 FEAT-136 仍为 **active / in progress**，不得标记为完整 D4 或 Feature usable。

## 1. 用户问题、目标与 Epic 关系

- 目标用户：需要在易界 AI Desktop 中理解 Agent 执行过程与结果的本地用户。
- 用户问题：Host/Desktop 起点只显示泛化 Item，无法稳定表达 Command/Tool 的安全摘要、输出、进度、耗时、exit code、失败和拒绝。
- 用户结果：Command 已有真实、闭合、可持久化的 completed/failed 垂直证据；Tool 仍只有 producer-neutral 的稳定投影，不制造真实 producer。
- Epic authority：CAP-016 / GS-003 是 Command Must；CAP-017 / GS-004 是通用 MCP Tool 目标。FEAT-138 已由 Owner 正式取消并排除。

### In scope

- schema v3、demo_fast + local 四文件包与 D0。
- Contracts v0.7.0 的显式协商 AgentSessionEventV5，以及 v1 至 v4 不变量。
- Command started、零到多个 output delta、completed、failed、declined 的安全闭合投影。
- 通用 MCP Tool started、progress、completed、failed 与预留 declined 的 producer-neutral 投影。
- event identity、at-least-once replay、completed reconciliation、caps、redaction、unknown 与 SQLCipher persistence/hydration。
- Host v5 negotiation、Command mapper/redactor/caps、event ID/replay、completed reconciliation 和通用 Tool 投影。
- Desktop v5 closed decoder、event-ID reducer、SQLCipher additive migration、Command/Tool UI、unknown fail-soft 与无障碍状态。
- Owner 授权的 Runtime producer source patch：early sandbox-denial 路径也发布 canonical started 与 failed terminal；版本仍报告 0.144.6。
- canonical runner、stable build、sidecar gate 转发、精确 artifact pin 与对应定向测试。
- fresh Command tranche：隔离、无敏感数据、无 remote 的 Git 仓库，仅一个 benign untracked 文件；只允许一个成功只读形式与一个 missing-ref 安全失败形式。

### Out of scope

- Tool D4；不注册 MCP server、Connector、dynamic tool，不制造 Tool producer。
- FileChange、Diff、patch、审批、写权限、网络/文件系统/shell 权限扩展与 FEAT-138。
- experimentalApi、Command approval reverse request、Artifact 合并或生产发布。
- 强杀、故障注入、权限破坏、binary 替换、攻击 fixture 或其它破坏性验证。
- push、tag、merge、amend、publish、release 或 deploy。

## 2. D0 工程事实与最终本地基线

| Repository | Final local commit | 状态与角色 |
|---|---|---|
| yijie-codex | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean；Owner 授权的 producer patch；reported Runtime 0.144.6 |
| yijie-contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean；unpublished v0.7.0；兼容性精确固定 Runtime |
| yijie-agent-host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean；精确固定 Contracts 与 stable Runtime artifact |
| yijie-desktop | `7026b47828961e58854b06c822c9c9e11252260d` | clean；精确固定 Host/Contracts 并提供 canonical stable runner |
| yijie | `5b637fc3c0cd10e8294011857764884750435415` + 本次唯一 D4 evidence commit | fresh tranche 回填前 clean；仅文档证据变化 |

- 原始实施基线保持可追溯：Runtime `0ce5902ed400866be0196886bb78f693a004d68d` / upstream rust-v0.144.6；Host `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`；Desktop `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51`。
- prior attempt 历史链保持不改写：Contracts `3c3000a6fbe2f08ab2131a463a1691e867d661b1`；Host `83d3163e21579042d2cc21f303e943946ff97eb0`；Desktop core `69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba` 与 entrypoint repair `65ee3062833ef3d185511599d8f3a4018f635369`；yijie D4 FAIL evidence `be5c1f91bd1c0f1f10878ea279721dac4eab3dc8` 与 RCA blocker `5b637fc3c0cd10e8294011857764884750435415`。
- Contracts 第一批唯一输入 `3c3000a6…` 已保留在历史链；最终 `87f94c9…` 只加入 Owner 授权 Runtime repair 后所需的精确 compatibility repin。
- canonical stable artifact：manifest SHA-256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`，binary SHA-256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`；manifest version 与 reported version 均为 0.144.6。
- 五仓最终只读审计 clean，无 P0/P1/P2；交叉 pin 一致。所有 commits 仅本地，未 push/tag/merge/amend/publish。

## 3. Contract 与权威边界

Contract impact 为 **semantic**。v4 是闭合协议，不能原位扩写；FEAT-136 使用显式协商的 v5 schema/proto/channel/route，v1 至 v4 保持原语义。

权威顺序：

1. yijie-codex 0.144.6 canonical source 与 Owner 授权 repair；
2. yijie-contracts v0.7.0 AgentSessionEventV5 JSON/SSE semantic authority；
3. AsyncAPI/OpenAPI 引用该 authority，Protobuf v5 仍通过 JSON-equivalent semantic gate；
4. Host 是唯一 Runtime mapper，不从模型文本制造 producer；
5. FEAT-132 ConversationState 与 Desktop SQLCipher 分别是 UI 状态和已观察历史 authority。

Command 只允许安全 display summary、结构化 workspace-relative/redacted cwd、bounded output、truncation、duration、exit code 和 stable error。禁止 raw command、绝对路径、process identity、Runtime wire 与秘密。Tool 只允许安全 identity、metadata-only arguments/progress/result、duration、stable error 和 truncation；真实 producer 缺失时不得补造。

## 4. 主流程与终态语义

1. canonical local/demo_fast stable runner 开启 FEAT-134/136 gates，保持 experimentalApi=false、sandbox=read-only、approvalPolicy=never。
2. Runtime 为每个真实 Command 发布 canonical lifecycle；Owner repair 使 early sandbox-denial 也先产生 started，再产生 failed terminal。
3. Host 按真实 event_id / turn_id / item_id 投影、脱敏、计数与截断；同 event_id replay 只消费一次，不同 event_id 的相同文本都保留。
4. Desktop closed decoder/reducer 按 item identity 聚合，item.completed 以 bounded snapshot 封口；late event 不改变已封口 Item。
5. Desktop 只持久化安全投影和 authority metadata；正常重开后按稳定 identity hydration，不复制或回滚 terminal Item。
6. Tool 继续停留在 source conformance；等待真实 producer 与 Owner 决策后再单独安排 Tool D4。

## 5. Must 验收状态

| AC | 状态 | 当前证据边界 |
|---|---|---|
| AC-001 | PENDING | fresh real tranche 得到 completed 与 failed 两个终态，exit code、duration、stable error 正确；started/零到多个 delta 的协议与 reducer 由定向测试覆盖，真实命令过快，Item started 与 output delta 未独立观察 |
| AC-002 | PENDING | event-ID 去重、合法重复文本与 gap 恢复的 source conformance PASS；真实 replay 未自然发生，记为 NOT OBSERVED |
| AC-003 | PENDING | completed reconciliation 与 late-event 规则的定向测试 PASS；真实正常重开后两个 terminal Item 各一次、无回滚，真实 event-ID 与 late event 未单独出现 |
| AC-004 | PASS | completed/failed Item 均只显示闭合安全字段；failed 使用 stable `command_failed`；安全复制不含 raw command、绝对路径、秘密或 Runtime wire |
| AC-005 | PENDING | generic Tool contract/source conformance PASS；真实 producer 不存在，Tool D4 BLOCKED/NOT RUN |
| AC-006 | PENDING | unknown identity 与 unknown v5 fail-closed/resync 定向测试 PASS；真实 unknown/recovery vertical 未执行 |
| AC-007 | PASS | SQLCipher migration、mixed history 与 fresh real hydration PASS；重开后 completed/failed 各一条 |
| AC-008 | PENDING | Command live 折叠、键盘、状态文字/图标、aria-live、安全复制、light、200% PASS；dark 与精确 1180×760 live NOT RUN，Tool UI 无 real producer |

FEAT-136 不满足完整 D4：多个 AC 仍 pending，Tool D4 未运行。

## 6. Owner repair 与 fresh Command tranche

- prior attempt 的 3/3 请求用于定位项目绑定与 Runtime pre-emitter lifecycle 缺口；该批保持历史 FAIL。追加 RCA 本身使用 0 次请求。
- Owner 随后明确授权 Runtime producer patch/升级边界，并于 2026-08-30 10:30:59 +08:00 把 fresh D4 额度设为最多 5 次。实现采用 source patch，reported Runtime 仍为 0.144.6；Contracts/Host/Desktop 完成精确 repin、测试与独立复审。
- fresh tranche 只发起 **1 次** Provider/模型请求，无重试、无第 2 至第 5 次请求。Agent 恰好执行两个允许的只读 Command，没有第三条命令。
- 真实 UI 最终恰好出现两个 Command Item：成功项 completed、exit 0、duration 0ms；失败项 failed、exit 128、duration 0ms、stable error `command_failed`。
- v5-only gated 投影可见；不采集或记录 Runtime wire。真实 output delta 因执行过快未单独观察。
- 安全复制 live PASS：复制内容不含绝对路径、秘密、Runtime wire 或 raw command，并保留显式脱敏标记。
- 正常关闭、runner exit 0、正常重开后，SQLCipher hydration 仍为 completed 1 条、failed 1 条；再次正常关闭后端口 idle。
- 正常重连/replay 未自然发生，记录 NOT OBSERVED；未通过断连、注入或伪造制造证据。
- light、键盘折叠、状态文字/图标、aria-live 与 200% 缩放 live PASS。dark 跟随系统设置且未切换；精确 1180×760 未实测。静态配置覆盖 width 1180、height 780、minWidth 1180、minHeight 760。
- Command projection 与安全复制已验证无 raw command/path/secret/wire；整个 WebView 仍含用户自己提交的 allowlist 文字，因此不声明 whole-WebView literal no-raw PASS。

## 7. 停止条件与最终边界

- Fresh Command tranche：PASS，真实调用 1/5，剩余 4 次未使用。
- FEAT-136 D4：未完成；整体 verification 保持 FAIL，Feature active。
- Tool D4：BLOCKED / NOT RUN；没有 MCP/Connector/dynamic-tool 注册或 producer/config 新增。
- FileChange、Diff、审批、写权限、FEAT-138：未触达。
- replay：NOT OBSERVED；dark 与精确 1180×760 live：NOT RUN。
- App/Host 已通过正常流程停止，loopback 端口 idle。
- 只允许再新增一个本地 yijie D4 evidence commit；不得 push/tag/merge/amend/publish。
