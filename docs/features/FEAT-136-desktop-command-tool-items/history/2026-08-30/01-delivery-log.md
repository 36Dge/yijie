# FEAT-136 — Delivery Log

> 2026-08-30 governance rebaseline：Command scope **DELIVERED**；FEAT-136 **USABLE / COMPLETE / PASS**。真实 Tool scope 移至 FEAT-144，后者 **BLOCKED / NOT RUN**。
>
> 本日志保留 prior 3/3 FAIL、RCA 0-call 与 fresh 1/5 PASS 的先后关系，不以后验范围决策重写历史。

## 1. 最终 commit 与 pin 台账

| Repository | Historical authority / baseline | Final frozen commit | 当前状态 |
|---|---|---|---|
| yijie-codex | `0ce5902ed400866be0196886bb78f693a004d68d` / upstream rust-v0.144.6 | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean；Owner-authorized minimal early-denial producer repair；reported 0.144.6；此后冻结 |
| yijie-contracts | immutable first-batch input `3c3000a6fbe2f08ab2131a463a1691e867d661b1` | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean；v0.7.0；精确 repin Runtime provenance |
| yijie-agent-host | base `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean；pin Contracts 与 stable artifact |
| yijie-desktop | base `fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` | `7026b47828961e58854b06c822c9c9e11252260d` | clean；pin Host/Contracts/artifact；canonical stable runner |
| yijie | prior FAIL `be5c1f91bd1c0f1f10878ea279721dac4eab3dc8`；RCA `5b637fc3c0cd10e8294011857764884750435415` | fresh evidence `3a6b37ee708a71af561929429fdcf778d5667c32` + 本次最多一个 governance commit | 只改治理与 Feature 文档 |

Cross-pin 与 artifact 最终审计：

- Host → Contracts `87f94c9…`。
- Contracts compatibility → Runtime `b2b20e2…`。
- Desktop → Host `96b1fa1…` / Contracts `87f94c9…`。
- stable manifest `1cfa2e0…` / 1475 bytes；binary `4efe16d…` / 355676760 bytes。
- manifest 与 Runtime reported version 均为 0.144.6。

## 2. 历史实施与验证时间线

### 2.1 D0、Contracts、Host 与 Desktop

- 建立 schema v3 / demo_fast / local 四文件包，确认 FEAT-138 已正式取消/排除。
- Contracts v0.7.0 定义显式协商 v5，保护 v1-v4；Host 完成 gated mapper/redaction/caps/reconciliation 与通用 Tool 投影；Desktop 完成 closed decoder/reducer、SQLCipher 与 Command/Tool consumer/UI 基础。
- Host→Desktop 对同一 schema 和 11 个普通 fixtures 完成 source conformance。该证据不冒充 live replay 或 real Tool vertical。

### 2.2 canonical entrypoint repair 与 prior D4

- stable runner、sidecar gate 转发、exact artifact/pin preflight 与 focused tests PASS。
- prior D4 使用 3/3 请求：第一次为环境/项目绑定失败；后两次暴露失败 terminal 在 Runtime 前端丢失。prior verdict 保持 FAIL。
- 0-call RCA 将根因定位到 pre-emitter early sandbox-denial return；拒绝由 Host/Desktop 根据模型文本补造 Item。

### 2.3 Owner-authorized Runtime repair 与 fresh tranche

- Owner 单独授权最小 Runtime producer source patch，使 early-denial 路径也发布 canonical started 与 failed terminal；没有替换或伪装 binary。
- Runtime、Contracts、Host、Desktop 形成最终 commits 与 cross-pins，四仓 clean，独立审查无 P0/P1/P2。
- fresh 额度为最多 5 次，实际使用 1 次，无重试；一次请求内只有两个独立 allowlisted 只读 Command。
- 实际 terminal cardinality：completed=1、failed=1；exit 0/128；duration 均为 0ms；stable error `command_failed`。
- 正常关闭、正常重开后 SQLCipher 仍为 completed=1、failed=1；再次正常关闭。
- light、键盘/折叠、状态文字/图标、aria-live、安全复制和 200% PASS。

## 3. 2026-08-30 Owner 原子化重基线

Owner 将 FEAT-136 Must 收窄到 fresh real 已证明的 Command 结果，并把原四类结果拆成五条独立 Must：

| Current AC | Scope | Evidence |
|---|---|---|
| AC-001 | completed terminal 与 cardinality | fresh real PASS |
| AC-002 | failed terminal/cardinality、exit/duration/stable error | fresh real PASS |
| AC-003 | 闭合安全投影与安全复制 | fresh real PASS |
| AC-004 | 正常重开 SQLCipher hydration，各一次 | fresh real PASS |
| AC-005 | light、键盘、状态/aria-live、200% | fresh live PASS |

原八条 Must 的迁移如下：

| Former AC | Preserved result | Receiver |
|---|---|---|
| AC-001 | completed/failed terminal 部分 | FEAT-136 AC-001/002；approval accept_once/cancel与Runtime Cancel形成的declined outcome转FEAT-137 phase 1（immutable source PASS、D4 NOT RUN），独立decline用户动作deferred；完整started/delta状态顺序转FEAT-143 |
| AC-002 | event identity、replay、gap | FEAT-142 |
| AC-003 | terminal cardinality/hydration 部分 | FEAT-136 AC-001/002/004；late/reconciliation resilience 转 FEAT-142 |
| AC-004 | 安全投影/复制 | FEAT-136 AC-003 |
| AC-005 | 真实 Tool lifecycle | FEAT-144 |
| AC-006 | unknown event/resync | FEAT-142；unknown Tool 产品 vertical 转 FEAT-144 |
| AC-007 | Command hydration | FEAT-136 AC-004；Tool hydration 转 FEAT-144 |
| AC-008 | Command 核心 UI | FEAT-136 AC-005；Tool UI 转 FEAT-144；dark/exact size 转 FEAT-143 |

这是 Owner 明示的范围决策，不是对原始 D4 状态的追溯性改写。CAP-017 / GS-004 仍为 active Epic scope，不能标记 N/A 或 excluded。

## 4. 当前验证与治理批边界

| Layer | Result |
|---|---|
| Runtime / Contracts / Host / Desktop final baselines | clean；cross-pins/artifact一致；focused tests与独立复审 PASS |
| Fresh real Command | 1/5；completed+failed；normal hydration；core UI/safety PASS |
| FEAT-136 current Must | 5/5 PASS |
| FEAT-136 D0 / D4 / strict | PASS |
| Real Tool | FEAT-144 blocked / NOT RUN |

本治理批调用额度为 0，不启动 Desktop、Runtime、Provider 或模型，不重跑 Command D4，不执行 Tool D4。只运行文档/治理/static 门禁。

## 5. 保留限制与停止

- natural replay、live event_id、late event：NOT OBSERVED；unknown/resync vertical：NOT RUN；转 FEAT-142。
- Item started 与独立 output-delta live 未捕获；完整集成状态顺序转 FEAT-143。
- dark 与 exact 1180×760 live：NOT RUN；转 FEAT-143。
- real Tool producer/product/security decision：pending；Tool D4 NOT RUN；转 FEAT-144。
- 未触达 FileChange、Diff、审批、写权限、FEAT-138、生产环境或发布。
- 未强杀、故障注入、破坏权限、替换 binary 或使用攻击 fixture。
