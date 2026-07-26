# FEAT-123 现状扫描与影响评估

## 1. 调查基线

| Repository | Rules read | Branch | Full HEAD SHA | Worktree | Toolchain |
|---|---|---|---|---|---|
| TBD | AGENTS/README/SECURITY/... | TBD | TBD | TBD | TBD |

## 2. 已验证的当前行为

| 事实 | 文件/符号/行号或命令 | 结果 | 事实/推断 |
|---|---|---|---|
| TBD | TBD | TBD | Fact |

## 3. 仓库与组件影响矩阵

| Repository/Component | 职责 | 影响 | 原因 | Owner | 预计改动 |
|---|---|---|---|---|---|
| TBD | TBD | direct/indirect/none | TBD | TBD | TBD |

对判定为 `none` 的相邻仓库，也应记录排除理由。

## 4. 调用链与数据流

```text
TBD producer
  → TBD boundary
  → TBD consumer
  → TBD storage/external service
```

| 边界 | 方向 | 权威源 | Producer | Consumers | 失败传播 |
|---|---|---|---|---|---|
| TBD | request/response/event | TBD | TBD | TBD | TBD |

## 5. Contract Impact

- 分类：`TBD`（`none | additive | semantic | breaking`）
- 选择最高风险分类的理由：TBD
- 是否存在公开未知消费者：TBD
- 请求方向兼容：TBD
- 响应/事件方向兼容：TBD
- 支持基线：TBD

`none` 不是默认值；必须证明没有改变跨进程、跨仓、跨版本、持久化或重放边界的可观察行为。

## 6. 数据与 Migration 影响

| 存储/Schema | Owner | 变化 | 旧数据影响 | 新旧 Reader/Writer | 回填/回滚 |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 7. 安全与隐私影响

- 认证：TBD
- 资源级授权：TBD
- 租户隔离：TBD
- 数据分类与脱敏：TBD
- Secret/token：TBD
- 高风险审批：TBD
- 审计字段：TBD
- 输入/文件/URL 风险：TBD

## 8. Runtime、模型与第三方影响

| 依赖 | 固定版本/完整 SHA | 能力是否已验证 | 费用/限流 | Sandbox | Fallback |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## 9. 现有测试、构建与发布入口

| 目的 | 真实命令/配置来源 | 作用范围 | 已知限制 |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 10. 初步交付顺序

### 合并顺序

1. TBD

### 部署顺序

1. TBD

### 功能启用顺序

1. TBD

## 11. 阻塞项与 Spike

| ID | 未知项 | 允许的只读/隔离验证 | 禁止副作用 | Owner | 结论 |
|---|---|---|---|---|---|
| SPIKE-001 | TBD | TBD | TBD | TBD | Open |
