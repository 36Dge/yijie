# {{FEATURE_ID}} 契约与兼容变更计划

## 1. Contract Impact 结论

- 分类：`TBD`（`none | additive | semantic | breaking`）
- 理由：TBD
- 边界：TBD
- 业务/安全语义是否变化：TBD

如果分类为 `none`，仍需填写第 1、2、9 节并说明其余各节 `N/A` 的理由。

## 2. 权威源与责任

| 契约/边界 | 权威源类别 | 仓库与路径 | Owner | Producer | Consumers |
|---|---|---|---|---|---|
| TBD | central contract/private DB/runtime/third-party | TBD | TBD | TBD | TBD |

生成物、SDK、fixture、快照、handler 类型和数据库行都不能成为第二权威源。

## 3. 语义设计

### 请求

- 字段、默认值与约束：TBD
- 认证、租户、权限：TBD
- 幂等、分页、排序：TBD

### 响应/事件

- 字段、单位与空值：TBD
- 错误码/错误结构：TBD
- 顺序、重复、乱序和未知 variant：TBD

### 审批与审计

- 审批语义：TBD
- 必需审计字段：TBD

## 4. 兼容方向

```text
新 request/input：provider 先接受，consumer 后发送
新 response/output/event：consumer 先容忍，producer 后发出
breaking：expand/新版本 → 迁移 consumers → 切换 → 观测 → cleanup
```

| Version combination | Request | Response/Event | Expected | Test |
|---|---|---|---|---|
| old producer + new consumer | TBD | TBD | TBD | TBD |
| new producer + old consumer | TBD | TBD | TBD | TBD |

## 5. 支持基线与 Breaking Check

| Baseline version | Full commit | Support window | Check command | Result/evidence |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

没有已发布基线时，使用治理目录登记的 fallback 完整 commit；禁止零基线放行。

## 6. Generator 与下游 Pin

| Consumer | Contract version/tag | Full commit | Digest | Generator/version | Owner |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

不得从 dirty worktree、floating sibling 或可移动引用构建发布产物。

## 7. Fixtures 与 Conformance

| Fixture | 唯一权威位置 | Producer test | Consumer test | 结果 |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

Feature 目录只引用 fixture；不要复制出第二套权威测试事实。

## 8. 合并、部署、启用与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD |

## 9. 实际检查证据

| 检查 | Command | CWD | SHA/版本 | Exit code | 结果 | 证据位置 |
|---|---|---|---|---:|---|---|
| generate | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| lint | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| test | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| breaking | TBD | TBD | TBD | TBD | NOT RUN | TBD |
| conformance | TBD | TBD | TBD | TBD | NOT RUN | TBD |

## 10. Consumer Owner 评审

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| TBD | Approve/Reject | TBD | TBD |
