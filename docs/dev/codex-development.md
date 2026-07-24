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
任何功能、修复或重构都先按 `docs/dev/contract-first.md` 标记
`contract-impact = none | additive | semantic | breaking`；语义变化不能因为 DTO
形状未变而判定为 `none`。

## 禁止行为

- 生成真实 token、secret、cookie；
- 把密钥写入代码或文档；
- 绕过审批策略；
- 在 `yijie-codex` 中写业务逻辑；
- 在 `yijie-agent-host` 中重建完整 agent platform；
- 未更新 contract 就修改接口；
- 在契约形成不可变引用、当前下游 PR 完成精确 pin 前合并该实现，或违反输入/输出方向提前启用；
- 从 dirty/floating sibling 制作发布产物，或把被跳过的跨仓检查声称为已通过；
- 将真实商家数据写入 fixtures。
