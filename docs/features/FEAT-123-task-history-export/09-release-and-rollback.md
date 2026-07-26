# FEAT-123 发布、灰度与回滚 Runbook

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin/generator | Environment |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 2. 发布前提

- [ ] G4 Code Complete 通过
- [ ] Release artifact 可追溯且来自干净不可变 source
- [ ] Config、secret、权限和容量准备完成
- [ ] Migration/回填已在类生产环境演练
- [ ] Dashboard、告警与 Runbook 已存在
- [ ] Feature Flag 默认安全
- [ ] 回滚责任人在线
- [ ] 真实变更批准已取得

## 3. 合并、部署、迁移与启用顺序

| Order | Action | Component/Environment | Operator | Preconditions | Verification | Rollback point |
|---:|---|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD |

代码合并、部署和功能激活是三个独立动作，不得混为一谈。

## 4. Feature Flag

| Flag | Default | Scope | Enable steps | Kill switch | Owner |
|---|---|---|---|---|---|
| TBD | off/on | TBD | TBD | TBD | TBD |

## 5. Migration/Backfill

| Phase | Command/job | Batch/lock controls | Validation | Pause/resume | Recovery |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

无数据库变化：`N/A + 理由`。

## 6. 灰度计划

| Stage | Scope/tenant/% | Observation window | Success criteria | Stop threshold | Decision owner |
|---|---|---|---|---|---|
| Internal | TBD | TBD | TBD | TBD | TBD |
| Canary | TBD | TBD | TBD | TBD | TBD |
| Expand | TBD | TBD | TBD | TBD | TBD |

## 7. Smoke

| Smoke ID | 用户路径 | 输入/租户 | 预期 | 避免真实副作用方式 |
|---|---|---|---|---|
| SMOKE-001 | TBD | TBD | TBD | TBD |

## 8. 观测与告警

| Signal | Dashboard/query | Baseline | Continue threshold | Stop/Rollback threshold | Owner |
|---|---|---:|---:|---:|---|
| 业务成功率 | TBD | TBD | TBD | TBD | TBD |
| 错误率/延迟 | TBD | TBD | TBD | TBD | TBD |
| 资源/队列 | TBD | TBD | TBD | TBD | TBD |
| 安全/审计 | TBD | TBD | TBD | TBD | TBD |
| AI 质量/成本 | TBD | TBD | TBD | TBD | TBD |

## 9. 回滚决策

```text
触发停止阈值
  → 停止扩量
  → 关闭 Feature Flag / 隔离流量
  → 判断仅回退应用是否安全
  → 回退制品或执行 roll-forward
  → 校验数据、队列与审计
  → 重新 smoke 并持续观察
```

| Trigger | Immediate action | Code rollback | Data action | Verification | Escalation |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 10. 可执行命令与权限

| Purpose | Exact command/control plane action | Required role | Expected output | Evidence location |
|---|---|---|---|---|
| Deploy | TBD | TBD | TBD | TBD |
| Disable | TBD | TBD | TBD | TBD |
| Rollback | TBD | TBD | TBD | TBD |

命令必须来自实际平台并经发布负责人确认；Codex 不得编造生产命令或 secret。

## 11. 回滚演练

| 日期 | Environment | Artifact/data versions | Steps | Result | Gaps |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | NOT RUN | TBD |

## 12. 沟通、职责与批准

| Role | Person | Contact path | Responsibility |
|---|---|---|---|
| Commander/Release/SRE/Business | TBD | TBD | TBD |

| Approval | Approver | Decision | Time | Evidence |
|---|---|---|---|---|
| Go/No-Go | TBD | TBD | TBD | TBD |
