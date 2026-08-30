# FEAT-136 — Demo 验证

> 2026-08-30 rebaseline verdict：**D0 PASS / D4 PASS / strict PASS**；Feature **usable**、implementation **complete**、verification **PASS**。该结论只覆盖五条 Command Must；Tool 由 FEAT-144 承接且仍 **blocked / NOT RUN**。

## 1. D0 与 final baseline

| Check | Result | Evidence boundary |
|---|---|---|
| Feature envelope | PASS | schema v3 / demo_fast / local；5 个可独立验收 Must |
| Product/UX | PASS | Command primary user、problem、outcome、flow、7 states 已闭合 |
| Contract classification | PASS | semantic；v5 显式协商；v1-v4 保持不变 |
| Runtime governance | PASS | 原始 `0ce5902…` 保留历史；Owner-authorized minimal patch 后最终冻结 `b2b20e2…` / 0.144.6 |
| Scope split | PASS | Tool→FEAT-144；resilience→FEAT-142；remaining visual/state order→FEAT-143 |
| Safety | PASS | 无强杀、故障注入、权限破坏、binary 替换或攻击 fixture |

Final identities：

| Repository | Commit |
|---|---|
| Runtime | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` |
| Contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` / v0.7.0 |
| Host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` |
| Desktop | `7026b47828961e58854b06c822c9c9e11252260d` |
| Fresh evidence | yijie `3a6b37ee708a71af561929429fdcf778d5667c32` |

- manifest SHA-256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b` / 1475 bytes。
- binary SHA-256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d` / 355676760 bytes。
- final read-only audit：五仓 clean、cross-pins一致、Runtime/manifest version 0.144.6、无真实 Tool producer/registration。

## 2. 证据复用判定

本次是 Owner 授权的治理范围重基线，不是新的产品实现。Runtime、Contracts、Host、Desktop commits 与 stable artifact 自 fresh real run 后均未变化，因此可以把同一 fresh run 复用于其严格子集 Must；无需也不得新增 Provider/模型调用。

| Historical phase | Requests | Verdict retained |
|---|---:|---|
| Prior D4 | 3/3 | FAIL；环境绑定与 missing failed lifecycle 历史保留 |
| RCA | 0 | 根因定位到 Runtime pre-emitter early-denial return |
| Fresh tranche after Owner repair | 1/5 | PASS for current Command Must |
| Current governance batch | 0 | 仅文档、lint、test、audit 与 package gates |

## 3. Current Must 验证

| AC | Result | Fresh evidence |
|---|---|---|
| AC-001 | PASS | completed terminal=1；exit 0；duration 0ms；没有重复或第三个 Item |
| AC-002 | PASS | failed terminal=1；exit 128；duration 0ms；stable `command_failed`；没有重复 |
| AC-003 | PASS | closed safety projection 与 clipboard 不含 raw Runtime、绝对路径、秘密或 wire |
| AC-004 | PASS | 正常关闭重开后 Items=2、completed=1、failed=1；每条一次且不回滚 |
| AC-005 | PASS | light、键盘 focus/展开/折叠、状态文字/图标、aria-live、安全复制、200% |

canonical run 使用 local/demo_fast stable runner、FEAT-134/136 gates、experimentalApi=false、sandbox=read-only、approvalPolicy=never。应用只通过自身正常退出与重开流程；没有断连或故障注入。

## 4. Focused 与 cross-repository 验证

| Layer | Evidence | Result |
|---|---|---|
| Runtime | failed lifecycle regression、artifact provenance、source/diff review | PASS；Owner-authorized canonical started+failed repair |
| Contracts | v5 focused、safe non-archive tests、generation/digests、lint、breaking | PASS；v1-v4 protected |
| Host | lint、FEAT-136 mapper/reconciliation/compatibility、artifact pin、diff review | PASS；clean；无 P0/P1/P2 |
| Desktop | 7 targeted Vitest files / 131 tests；Rust hydration/failed 3/3；typecheck；scoped ESLint；diff | PASS；clean |
| Host→Desktop | exact schema + 11 ordinary fixtures + focused producer/consumer suites | PASS；source conformance only |
| Governance | FEAT-136 D0/D4/strict PASS；FEAT-144 strict structural PASS、D0 semantic BLOCKED；lint/test/audit/shell/diff PASS | FEAT-144 Owner decision pending；Tool D4 不运行 |

## 5. 明确后移且不得伪造的项目

| Item | Current observation | Receiver / impact |
|---|---|---|
| natural replay | NOT OBSERVED | FEAT-142；不影响收窄后的 FEAT-136 Must |
| live event_id / late event | NOT OBSERVED | FEAT-142 |
| unknown/resync real vertical | NOT RUN | FEAT-142 |
| Item started / independent output delta live | 未独立捕获 | FEAT-143 承接完整集成状态顺序；focused tests 不能冒充 live evidence |
| dark | NOT RUN live | FEAT-143 |
| exact 1180×760 | NOT RUN live | FEAT-143；静态配置不冒充 live result |
| real Tool producer / Tool D4 / GS-004 | BLOCKED / NOT RUN | FEAT-144；CAP-017 保持 Epic active scope |

用户消息自身包含 allowlist 文字，因此不声明 whole-WebView literal no-raw PASS；只对 Command 投影、clipboard 与保存的证据作闭合安全声明。

## 6. 最终 verdict

- FEAT-136 current Must：5/5 PASS。
- D0：PASS。
- D4：PASS。
- strict / lint / test / feature audit：PASS。
- Feature：usable；implementation complete；verification PASS。
- FEAT-144：四文件 D0 package 已创建，但 D0 semantic gate BLOCKED；implementation blocked / verification NOT RUN；没有代码实现或 Tool D4。
- Epic：仍 active；没有发布、push、tag、merge 或 Runtime/Provider/model 启动。
