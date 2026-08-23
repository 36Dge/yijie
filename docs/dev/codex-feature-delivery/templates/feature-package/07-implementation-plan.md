# {{FEATURE_ID}} 原子实施计划

## 1. 实施原则

- 一次只完成一个可独立验证的行为；
- 先建立失败证据，再做最小实现；
- 不夹带无关重构、依赖升级或全仓格式化；
- 每个仓库独立分支、提交、PR 和验证；
- 范围或语义变化时回到需求/设计，而不是静默扩张。
- 大规模实现前先通过适用 G2A、Harness Qualification 与 G2V；
- G3 只对单个 slice 判定，不使用手写聚合状态覆盖证据。

## 2. 依赖 DAG

```text
TBD contract/G2A
  → TBD harness qualification
  → TBD G2V production walking skeleton
  → TBD vertical slice S1
  → TBD vertical slice S2
  → TBD final E2E / activation
```

## 3. 实施切片

| Slice | Type | 主要意图 | AC | Repository(s) | 允许修改 | 禁止修改 | Prerequisites | Required evidence | 验证命令 | Freshness invalidation | 回滚 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VS1 | vertical_skeleton | TBD | AC-001 | TBD | TBD | TBD | G2/G2A/HQUAL | local + boundary + vertical | TBD | contract/runtime/platform/harness/bootstrap/commit change | TBD |
| S1 | implementation | TBD | AC-001 | TBD | TBD | TBD | G2V/VS1 | local + boundary + vertical | TBD | prerequisite or covered reference change | TBD |

必须先完成真实平台、production bootstrap 的最小 Walking Skeleton 并通过 G2V，再按纵向切片扩展；
mock 必须位于明确端口后且不可进入 production bootstrap 或 G2V/final E2E 证据路径。

## 4. 跨仓顺序

| 阶段 | Repository | Branch/base full SHA | 输出 | 下游 Pin | Owner |
|---|---|---|---|---|---|
| Contract | TBD | TBD | version/full commit/digest/generator | TBD | TBD |
| Provider | TBD | TBD | TBD | TBD | TBD |
| Consumer | TBD | TBD | TBD | TBD | TBD |
| Activation | TBD | TBD | TBD | TBD | TBD |

## 5. Migration 实施序列

| Phase | 代码/数据动作 | 兼容要求 | 验证 | 停止/回滚点 |
|---|---|---|---|---|
| Expand | TBD | TBD | TBD | TBD |
| Backfill | TBD | TBD | TBD | TBD |
| Switch | TBD | TBD | TBD | TBD |
| Contract | TBD | TBD | TBD | TBD |

无数据库变化：`N/A + 理由`。

## 6. 每个 Codex 任务的固定 Context

```text
Feature ID / Slice ID:
角色：Planner / Implementer / Tester / Reviewer
当前 Repository、Branch 与 Base Full SHA:
权威输入路径与不可变版本:
目标及对应 AC:
允许修改目录:
禁止修改目录:
真实验证命令:
证据输出位置:
停止条件:
最终报告格式:
```

## 7. Commit/PR 计划

| Commit/PR | 单一目的 | Files/Repo | Test evidence | Cross-link |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## 8. Slice 完成记录

| Slice | Prerequisites | Full commit(s) | Local evidence | Boundary evidence | Vertical evidence | Structured freshness | Review | G3 Status |
|---|---|---|---|---|---|---|---|---|
| S1 | TBD | TBD | NOT RUN | NOT RUN | NOT RUN | STALE / TBD | TBD | Pending |

一个 slice 可记录多个 `{repository, full_sha}`。freshness 中的 commits 必须精确覆盖当前 slice 与
所有 transitive prerequisite slices；contract/fixture refs、harness commit/digest、平台或 production
bootstrap 任一不一致都视为 STALE。local/boundary/vertical evidence 分别记录 exact command、
environment、exit code、ISO 时间与唯一 verification marker；required evidence 为
`NOT RUN/FAIL/STALE` 时，G3 必须拒绝 PASS。

## 9. 三次同类失败熔断与 RCA

| Incident | Fingerprint | Attempts | Breaker | RCA path | 扩大只读审计范围 | 唯一获批下一动作 |
|---|---|---:|---|---|---|---|
| RCA-001 | TBD | 0 | armed | N/A | TBD | TBD |

第三次同类失败后 breaker=`RCA_REQUIRED`；禁止第四次尝试或继续局部补丁。RCA 必须区分
Fact/Assumption/Unknown/Conflict 与 product/harness/platform/gate，并保留全部历史失败。每轮 RCA
以 append-only cycle 记录 expanded scope、候选根因、区分证据、Owner 批准的单一动作和最多一次
post-RCA attempt；若该次仍为同类失败，立即重新熔断。

## 10. 变更控制

以下变化必须回跳：

| 变化 | 回到 |
|---|---|
| 用户行为/AC 变化 | `01-requirements.md` |
| 仓库/边界变化 | `02-impact-assessment.md` |
| 风险/权限变化 | `03-decisions-and-risks.md` |
| 状态/接口语义变化 | `04-contract-change-plan.md` |
| 数据/架构变化 | `05-technical-design.md` |
| 测试阈值变化 | `06-test-plan.md` |

## 11. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 技术负责人 | TBD | Approve/Reject | TBD |
