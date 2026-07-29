# FEAT-124 验证证据与独立审查报告

> 只记录真实执行结果。未执行、被跳过、输出截断或仍在运行的检查必须写 `NOT RUN`，不能推断为通过。

## 1. 验证上下文

| Repository | Branch | Full HEAD SHA | Worktree | Runtime/toolchain | 时间 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 2. Baseline

| ID | CWD | Command | Exit code | Result | 摘要/日志位置 | 历史失败 |
|---|---|---|---:|---|---|---|
| BASE-001 | TBD | TBD | TBD | NOT RUN | TBD | TBD |

## 3. Slice 证据

| Slice/AC | Head SHA | Command | Exit code | Result | Diff/证据 |
|---|---|---|---:|---|---|
| S1 / AC-001 | TBD | TBD | TBD | NOT RUN | TBD |

## 4. 最终命令记录

| Check ID | Repository/CWD | Command | Tool/version | Exit code | PASS/FAIL/NOT RUN | Evidence |
|---|---|---|---|---:|---|---|
| V-LINT | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-TYPE | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-UNIT | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-INTEGRATION | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-BUILD | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| V-GENERATE | TBD | TBD | TBD | TBD | NOT RUN | TBD |

## 5. 契约与版本兼容

| 结论 | Contract version/full commit/digest/generator | Command/Test | Result | Evidence |
|---|---|---|---|---|
| 源结构与生成无漂移 | TBD | TBD | NOT RUN | TBD |
| Supported baseline breaking check | TBD | TBD | NOT RUN | TBD |
| Producer conformance | TBD | TBD | NOT RUN | TBD |
| Consumer conformance | TBD | TBD | NOT RUN | TBD |
| Runtime/第三方兼容 | TBD | TBD | NOT RUN | TBD |

## 6. AC → 实现 → 证据追踪

| AC/NFR | 实现文件/符号 | Test IDs | 实际命令/证据 | 结果 |
|---|---|---|---|---|
| AC-001 | TBD | TBD | TBD | NOT RUN |

## 7. 专项验证

| 专项 | 范围 | 环境/版本组合 | 结果 | Evidence |
|---|---|---|---|---|
| E2E | TBD | TBD | NOT RUN | TBD |
| Security/tenant | TBD | TBD | NOT RUN | TBD |
| Failure/resilience | TBD | TBD | NOT RUN | TBD |
| Migration rehearsal | TBD | TBD | NOT RUN | TBD |
| Performance | TBD | TBD | NOT RUN | TBD |
| AI Eval | TBD | TBD | NOT RUN | TBD |
| Visual/accessibility | TBD | TBD | NOT RUN | TBD |

不适用项写 `N/A + 理由`，不得空白。

## 8. Diff 与制品完整性

- [ ] `git status` 已逐仓检查
- [ ] `git diff --stat` 范围符合计划
- [ ] `git diff --check` 通过
- [ ] 完整 diff 已审阅
- [ ] 生成物来自锁定 generator
- [ ] lockfile/依赖变化有意且已审查
- [ ] migration 与发布顺序一致
- [ ] 无 `.skip`、`.only`、弱化断言或关闭门禁
- [ ] 无 secret、PII、本机路径、调试后门或临时文件

## 9. 独立 Review Findings

| Finding | Severity | 文件/位置 | 触发与影响 | 处理 | 复验 |
|---|---|---|---|---|---|
| TBD | P0/P1/P2/P3 | TBD | TBD | Open | TBD |

- Reviewer 是否独立于实现上下文：TBD
- P0/P1 是否清零：TBD
- P2 例外批准：TBD

## 10. 未验证项与残余风险

| Item | 原因 | 风险 | 补验证条件 | Owner | 是否阻断 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | yes/no |

## 11. 结论

- Code Complete：TBD
- 验证人：TBD
- 日期：TBD
- 结论依据：TBD
