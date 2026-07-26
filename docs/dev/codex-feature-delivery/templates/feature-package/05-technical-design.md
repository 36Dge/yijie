# {{FEATURE_ID}} 技术设计

## 1. 设计摘要

- 要解决的问题：TBD
- 选择的方案：TBD
- 关键约束：TBD
- 明确不做：TBD

## 2. 组件职责与依赖方向

| Component/Repository | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

```text
TBD client
  → TBD API/host
  → TBD domain/connector
  → TBD storage/external boundary
```

## 3. 关键时序

### 正常路径

1. TBD

### 失败、取消与恢复

1. TBD

## 4. 状态模型

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 非法处理 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

必须覆盖加载、空态、失败、超时、取消、断线、重试、重复、乱序和终态。

## 5. 领域模型与不变量

| Entity/Value | Owner/tenant scope | ID/幂等键 | 不变量 | 生命周期 |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## 6. 数据与 Migration 专项

- 是否涉及数据库/缓存/持久化：TBD
- 结论：TBD；不涉及时写 `N/A + 理由`

| Phase | Schema/Data change | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | TBD | TBD | TBD | TBD | TBD |
| Backfill | TBD | TBD | TBD | TBD | TBD |
| Switch | TBD | TBD | TBD | TBD | TBD |
| Contract | TBD | TBD | TBD | TBD | TBD |

不得在同一不可回退发布中同时删旧字段、迁全量数据并硬切全部调用方。

## 7. 一致性与韧性

- 事务边界：TBD
- 并发冲突：TBD
- 幂等：TBD
- 超时/取消：TBD
- 重试/退避/上限：TBD
- 限流/熔断/降级：TBD
- 部分失败与补偿：TBD
- 资源释放：TBD

## 8. 安全设计

- 认证入口：TBD
- 资源级授权：TBD
- 租户隔离：TBD
- 输入验证：TBD
- Secret/token 边界：TBD
- PII/日志脱敏：TBD
- 高风险审批：TBD
- 审计：TBD

## 9. 可观测性

| Signal | 名称/字段 | 成功基线 | 告警阈值 | Runbook 动作 |
|---|---|---:|---:|---|
| Metric/Log/Trace/Audit | TBD | TBD | TBD | TBD |

跨服务至少关联适用的 `trace_id`、`request_id`、`tenant_id`、`user_id`、`task_id` 和 session/thread ID。

## 10. 性能、容量与成本

| 项目 | 基线 | 目标/上限 | 测试方法 | 降级 |
|---|---:|---:|---|---|
| TBD | TBD | TBD | TBD | TBD |

## 11. 配置、Feature Flag 与部署

- Flag：TBD
- 默认值：TBD
- 安全关闭行为：TBD
- 配置验证：TBD
- 新旧版本共存窗口：TBD

## 12. AI 功能专项

- 是否改变 prompt/model/retrieval/tool schema：TBD
- 固定版本：TBD
- 结构化输出 Schema：TBD
- 无答案/拒答：TBD
- 提示注入和越权工具控制：TBD
- Eval 计划引用：TBD
- 非 AI 功能写 `N/A + 理由`。

## 13. 方案比较

| 方案 | 优点 | 缺点 | 风险 | 结论 |
|---|---|---|---|---|
| A | TBD | TBD | TBD | TBD |
| B | TBD | TBD | TBD | TBD |

## 14. ADR 与批准

- ADR：TBD
- 技术负责人：TBD
- 安全/数据 Owner：TBD
- 结论与日期：TBD
