# Codex 开发说明

## 开发前必须读取

Codex 在每个仓工作前必须读取：

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
docs/architecture/000-overview.md
docs/dev/codex-project-memory.md
docs/dev/codex-feature-delivery/README.md
docs/dev/codex-feature-delivery/HANDBOOK.md
```

在易界项目中起草需求、设计或实施计划前，还必须执行长期记忆中的需求起草前强制高质量协议。新需求先从所属 Git worktree 使用 `docs/dev/codex-feature-delivery/scripts/new-feature.sh` 创建 `schema_version: 2` Package；修改 Package 之外的实现前，必须满足当前 Slice 所需的 G0/G1/G2、逐 Boundary G2C 和有效 Authorization Packet。历史 v1 Package 只读，不得复制为新需求或用旧 G2A 替代 v2 Gate。
默认角色为：需求负责人、Product/Design 决策人、技术负责人、Reviewer 和发布负责人
均为段成威；某个需求有最新明确覆盖时除外。

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
- 复制历史 v1 Package、手工拼装模板，或在 v2 Gate/Authorization 未满足时修改业务实现；
- 在契约形成不可变引用、当前下游 PR 完成精确 pin 前合并该实现，或违反输入/输出方向提前启用；
- 从 dirty/floating sibling 制作发布产物，或把被跳过的跨仓检查声称为已通过；
- 将真实商家数据写入 fixtures。
