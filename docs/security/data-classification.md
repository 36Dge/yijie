# Data Classification

| 等级 | 示例 | 处理要求 |
|---|---|---|
| Public | 公开平台规则、公开文档 | 可公开引用 |
| Internal | 内部配置、架构文档 | 仅内部访问 |
| Confidential | 商家经营数据、订单统计 | 脱敏、审计、权限控制 |
| Restricted | token、PII、财务数据 | 严格加密、最小权限、禁止进入日志 |

Fixtures、demo 和 eval 数据只能使用 Public 或合成数据。
