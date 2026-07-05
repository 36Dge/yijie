# Codex 开发说明

## 开发前必须读取

Codex 在每个仓工作前必须读取：

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
docs/architecture.md
```

涉及 API 时必须先读取 `yijie-contracts` 中的 OpenAPI、Protobuf 或 JSON Schema。

## 禁止行为

- 生成真实 token、secret、cookie；
- 把密钥写入代码或文档；
- 绕过审批策略；
- 在 `yijie-codex` 中写业务逻辑；
- 在 `yijie-agent-host` 中重建完整 agent platform；
- 未更新 contract 就修改接口；
- 将真实商家数据写入 fixtures。
