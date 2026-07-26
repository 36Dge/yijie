# {{FEATURE_ID}} 原子实施计划

## 1. 实施原则

- 一次只完成一个可独立验证的行为；
- 先建立失败证据，再做最小实现；
- 不夹带无关重构、依赖升级或全仓格式化；
- 每个仓库独立分支、提交、PR 和验证；
- 范围或语义变化时回到需求/设计，而不是静默扩张。

## 2. 依赖 DAG

```text
TBD contract
  → TBD provider
  → TBD consumer
  → TBD activation
```

## 3. 实施切片

| Slice | 主要意图 | AC | Repository | 允许修改 | 禁止修改 | 前置 | 验证命令 | 回滚 |
|---|---|---|---|---|---|---|---|---|
| S1 | TBD | AC-001 | TBD | TBD | TBD | TBD | TBD | TBD |

建议先完成最小 Walking Skeleton，再按纵向切片替换 mock；mock 必须位于明确端口后且不可进入生产路径。

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

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S1 | TBD | TBD | TBD | TBD | Pending |

## 9. 变更控制

以下变化必须回跳：

| 变化 | 回到 |
|---|---|
| 用户行为/AC 变化 | `01-requirements.md` |
| 仓库/边界变化 | `02-impact-assessment.md` |
| 风险/权限变化 | `03-decisions-and-risks.md` |
| 状态/接口语义变化 | `04-contract-change-plan.md` |
| 数据/架构变化 | `05-technical-design.md` |
| 测试阈值变化 | `06-test-plan.md` |

## 10. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 技术负责人 | TBD | Approve/Reject | TBD |
