# Security Model

## 目标

保护平台 token、商家经营数据、买家 PII、财务数据和高风险店铺操作。

## 边界

- Desktop 不持久化平台 access token；
- API 管理租户、权限、授权状态和审批任务；
- Connectors 管理 token vault 和外部 API 调用；
- Agent Host 只做策略检查和工具请求，不直接持有平台 token；
- Codex Runtime 只通过 MCP 工具间接完成任务。

## 默认策略

默认拒绝高风险写操作，必须经过审批策略明确放行。
