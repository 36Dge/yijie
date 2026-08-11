# PR 标题

## 背景

说明为什么改。

## 变更内容

-

## Feature Delivery v2

- Feature ID：
- Package 路径（非需求变更写 `N/A + 理由`）：
- Profile：`lite | standard | controlled | N/A`
- Target：`local_engineering | staging | production | N/A`
- 本 PR 目标 Gate / instance：
- Decision ID：
- Approval key ID / attestation payload digest：
- Evidence ID / CI run：
- Change coverage exemption：`N/A` 或 registry 中的精确 ID（不能只写自由文本理由）

`ELIGIBLE` 不等于批准；只有绑定当前 subject、且由受保护 base trust root 验签的有效 `passed` 决策可以作为 Gate 结论。仅写 `actor.type: human` 不能认证身份。历史 v1 包只读，不复制为新需求起点。
CI 会把 base...head 的每个变更路径映射到 v2 Package 的当前 G2 repository/path/base 授权及所需 Gate/head SHA；Feature Package 自身文件单独校验。豁免只认受保护 base policy 中登记的精确文件集合、内容摘要、Owner、批准引用和期限。

## 影响范围

- [ ] yijie-contracts
- [ ] yijie-api
- [ ] yijie-desktop
- [ ] yijie-admin-web
- [ ] yijie-agent-host
- [ ] yijie-codex
- [ ] yijie-skills
- [ ] yijie-connectors
- [ ] yijie-knowledge
- [ ] yijie-infra

## 是否涉及安全

- [ ] token / secret
- [ ] PII
- [ ] 审批策略
- [ ] 高风险工具调用
- [ ] 权限控制
- [ ] 审计日志

## Contract First

<!-- 按 breaking > semantic > additive > none 的最高风险只选一个；当前由 reviewer 审核，PR-body 自动校验尚未接通。 -->

- [ ] `contract-impact: none`
- [ ] `contract-impact: additive`
- [ ] `contract-impact: semantic`
- [ ] `contract-impact: breaking`

### 分类理由

说明是否改变跨进程、跨仓库、跨版本、持久化或重放边界上的形状与语义。

### 契约证据

- 权威源类别（`yijie-contracts | private-storage | deployment | runtime-upstream | third-party | N/A`）：
- 权威源路径：
- 权威源不可变引用（tag / 完整 commit / schema / API version / migration）：
- yijie-contracts PR（非公共 wire 填 `N/A + 理由`）：
- 计划或已发布 tag / 完整 commit：
- 所有适用 breaking 基线与结果（仅公共 wire；尚无发布版本时填已登记 fallback 完整 commit）：
- migration / data / runtime / deployment compatibility（按权威源适用）：
- Owner：
- Producer：
- 已知/登记 Consumers（公开未知填 `unknown-public`）：
- Consumer Owner 逐项评审 / 例外：
- 下游版本 / commit / digest pin：
- 生成物与 conformance：

不涉及时逐项填写 `N/A + 理由`，不能留空或伪造 contracts 引用。公共 wire 契约 PR
合并前可填写计划版本，跨仓交付完成时必须补最终不可变引用。涉及 OpenAPI、Protobuf、
AsyncAPI、JSON Schema、MCP tool、SDK 或 Runtime projection 时列出具体文件。

### 合并与发布

- 合并顺序：
- 部署顺序：
- 兼容窗口 / 迁移 / 弃用：
- 灰度与观测：
- 回滚：

### 临时例外

无例外填写 `N/A`。有例外时必须填写：

- Owner：
- 原因与范围：
- 批准证据：
- 到期日：
- 跟踪 Issue：
- 回滚：
- 补偿 PR / 移除条件：

## 测试

- [ ] Unit Test
- [ ] Integration Test
- [ ] Contract Test
- [ ] Producer / Consumer Conformance
- [ ] Breaking / Runtime Compatibility
- [ ] E2E Test
- [ ] Skill Eval
- [ ] Retrieval Eval

## 发布说明

说明发布版本、migration、灰度、回滚、手动操作和任何尚未执行的跨仓验证。
