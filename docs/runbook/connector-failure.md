# Connector Failure Runbook

## 快速判断

- 平台 API 是否限流；
- token 是否过期；
- permission scope 是否缺失；
- 外部平台是否返回临时错误；
- 高风险操作是否缺少审批。

## 记录

排查时记录 `trace_id`、`tenant_id`、`tool_name`、平台错误码和脱敏后的请求摘要。
