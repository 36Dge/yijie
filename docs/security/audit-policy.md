# Audit Policy

## 必须审计

- 外部平台 API 调用；
- MCP 工具调用；
- 高风险操作审批；
- 店铺授权、撤销和 token refresh；
- 管理后台权限变更；
- 知识库版本发布；
- Skill / Plugin 上架和灰度。

## 审计字段

- `trace_id`
- `tenant_id`
- `user_id`
- `task_id`
- `tool_name`
- `approval_id`
- `target_platform`
- `result`
- `created_at`

敏感字段必须脱敏或摘要化。
