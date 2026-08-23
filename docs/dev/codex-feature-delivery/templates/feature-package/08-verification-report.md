# {{FEATURE_ID}} 验证证据与独立审查报告

> 只记录真实执行结果。未执行、被跳过、输出截断或仍在运行的检查必须写 `NOT RUN`，不能推断为通过。

`feature.yaml` 中的证据引用必须写成 `08-verification-report.md#<EVIDENCE-ID>`。每条被引用证据在本文
必须精确出现一次下列 marker，后接环境、命令、exit code、完整不可变引用和 content-free 摘要：

```text
<!-- evidence: <EVIDENCE-ID> -->
### Evidence <EVIDENCE-ID>
```

不得引用表格行号、任意文字或可漂移日志 URL 来代替唯一 marker。
机器门禁以 `feature.yaml` 中结构化的 command、environment、exit code、commit/pin、harness 与
freshness 字段为权威；本文 marker 是唯一的人类叙述索引，不能用 prose 把 `NOT RUN/FAIL/STALE`
提升为 PASS，也不能覆盖结构化字段冲突。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 2. Baseline

| ID | CWD | Command | Exit code | Result | 摘要/日志位置 | 历史失败 |
|---|---|---|---:|---|---|---|
| BASE-001 | TBD | TBD | TBD | NOT RUN | TBD | TBD |

## 3. Slice 证据

| Slice/AC | Prerequisites | Full commit(s) | Local evidence | Boundary evidence | Vertical evidence | Structured freshness | G3 Result |
|---|---|---|---|---|---|---|---|
| S1 / AC-001 | TBD | TBD | NOT RUN | NOT RUN | NOT RUN | STALE / TBD | NOT RUN |

required evidence 为 `NOT RUN/FAIL/STALE`、harness 未 qualified 或覆盖引用与当前 commit/pin 不一致时，
该切片不得记为 PASS。

## 4. Runtime Harness Qualification 与 G2V

| Harness ID | Full commit/digest | Real platform | Production bootstrap | Positive/negative controls | Timeout/cleanup | Failure taxonomy | Result | Evidence |
|---|---|---|---|---|---|---|---|---|
| H-VERTICAL-001 | TBD | TBD | yes/no | TBD | TBD | product/harness/platform/gate | NOT RUN | TBD |

| G2V Check | Representative data | Critical production path | Command/environment | Commit/harness refs | Result | Freshness | Uncovered risk |
|---|---|---|---|---|---|---|---|
| Minimal vertical | TBD | TBD | TBD | TBD | NOT RUN | STALE | TBD |

无法唯一分类的 harness 结果为 `DIAGNOSIS_REQUIRED`，不得猜成 product failure 或 G2V PASS。

## 5. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-LINT | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-TYPE | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-UNIT | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-INTEGRATION | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-BUILD | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-GENERATE | TBD | TBD | TBD | TBD | NOT RUN | TBD |

## 6. 契约与版本兼容

| 结论 | Contract version/full commit/digest/generator | Command/Test | Result | Evidence |
|---|---|---|---|---|
| 源结构与生成无漂移 | TBD | TBD | NOT RUN | TBD |
| Supported baseline breaking check | TBD | TBD | NOT RUN | TBD |
| Producer conformance | TBD | TBD | NOT RUN | TBD |
| Consumer conformance | TBD | TBD | NOT RUN | TBD |
| Runtime/第三方兼容 | TBD | TBD | NOT RUN | TBD |

## 7. Temporal Contract Conformance

| Invariant/Test ID | Producer → commit → notify → replay → terminal → cleanup | Command | Result | Evidence/freshness |
|---|---|---|---|---|
| TINV-001 / TCONF-001 | TBD | TBD | NOT RUN | TBD |

## 8. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-001 | TBD | TBD | TBD | NOT RUN |

## 9. 最终 E2E 独立 Verdict

| Verdict | 范围 | 环境/版本组合 | Commit/harness refs | 结果 | Freshness | Evidence |
|---|---|---|---|---|---|---|
| core_vertical | production bootstrap、用户操作、跨组件/durable 链路、最终用户结果 | TBD | TBD | NOT RUN | STALE | TBD |
| accessibility_visual | axe、键盘、焦点、视口、主题、截图 | TBD | TBD | NOT RUN | STALE | TBD |
| teardown | process/connection/WAL/spool/temp/listener/handle/run-root cleanup | TBD | TBD | NOT RUN | STALE | TBD |

一项 PASS 不得覆盖另一项 `FAIL/NOT RUN`；只有无 UI 等真实不适用场景才能记录 `N/A + Owner 理由`。

## 10. 其他专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| Security/tenant | TBD | TBD | NOT RUN | TBD |
| Failure/resilience | TBD | TBD | NOT RUN | TBD |
| Migration rehearsal | TBD | TBD | NOT RUN | TBD |
| Performance | TBD | TBD | NOT RUN | TBD |
| AI Eval | TBD | TBD | NOT RUN | TBD |
| Visual/accessibility | TBD | TBD | NOT RUN | TBD |

不适用项写 `N/A + 理由`，不得空白。

## 11. Failure Ledger 与三次熔断/RCA

| Incident | Fingerprint | Attempt 1 | Attempt 2 | Attempt 3 | Breaker | RCA cycle(s) | Product/Harness/Platform/Gate | Owner-approved next action |
|---|---|---|---|---|---|---|---|---|
| RCA-001 | TBD | TBD | TBD | TBD | armed/RCA_REQUIRED | TBD | TBD | TBD |

达到第三次后不得存在未获 RCA/Owner 批准的后续尝试。每个 RCA cycle 追加 expanded scope、候选根因、
区分证据、单一授权和最多一次结果；该次同类失败立即重新熔断。失败记录只追加，不删除、不改名清零，
也不得回写成“从未发生”。

## 12. Diff 与制品完整性

- [ ] `git status` 已逐仓检查
- [ ] `git diff --stat` 范围符合计划
- [ ] `git diff --check` 通过
- [ ] 完整 diff 已审阅
- [ ] 生成物来自锁定 generator
- [ ] lockfile/依赖变化有意且已审查
- [ ] migration 与发布顺序一致
- [ ] 无 `.skip`、`.only`、弱化断言或关闭门禁
- [ ] 无 secret、PII、本机路径、调试后门或临时文件

## 13. 独立 Review Findings

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| TBD | P0/P1/P2/P3 | TBD | TBD | Open | TBD |

- Reviewer 是否独立于实现上下文：TBD
- P0/P1 是否清零：TBD
- P2 例外批准：TBD

## 14. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | yes/no |

## 15. 结论

- Code Complete：TBD
- 所有 required per-slice G3 是否 PASS/fresh：TBD
- core/accessibility-visual/teardown 是否分别 PASS：TBD
- 是否存在开放 RCA_REQUIRED：TBD
- 验证人：TBD
- 日期：TBD
- 结论依据：TBD
