# FEAT-144 — Delivery Log

> 当前批次仅完成 D0 package/preflight；D0 exit blocked。没有实现、启动、真实调用或 Tool D4。

## 1. 2026-08-30 — Feature 分配与范围迁移

- 对 CrossBSD 与 Desktop Epic source 执行 Feature ID 唯一性检查；FEAT-144 未被占用，且不使用已取消的 FEAT-138。
- CAP-017 / GS-004 从 FEAT-136 的混合 Command/Tool 范围迁移到本独立 Feature。
- FEAT-136 已存在的 generic Tool contract、Host mapper 与 Desktop consumer/UI 只作为 foundation；不视为真实产品 Tool 或 D4 证据。
- Feature 使用 schema v3 / demo_fast / local，8 个 Must 全部 pending。
- 因真实 producer、产品入口、安全/权限边界与调用额度未决，Product/UX 与 D0 gate 均为 blocked/pending；Feature/implementation 标为 blocked，verification 标为 NOT RUN。

## 2. 当前冻结输入

| Repository | Commit / version | Role |
|---|---|---|
| yijie-codex | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` / 0.144.6 | 最终冻结 Runtime；不得修改 |
| yijie-contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` / v0.7.0 | producer-neutral v5 authority foundation |
| yijie-agent-host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | generic Tool mapper foundation |
| yijie-desktop | `7026b47828961e58854b06c822c9c9e11252260d` | closed consumer/persistence/UI foundation |

候选正常责任边界是 Connector 执行、Skill 声明、Host 加载/投影、Contracts 约束、Desktop 呈现；它不是 Owner 决策，不得在本 D0 中当作已选路线。

## 3. Owner decision checklist

- [ ] 选择真实 Tool 与用户价值。
- [ ] 选择产品入口和 producer repository/owner。
- [ ] 冻结数据分类、允许参数、权限、副作用、网络/文件/账户边界。
- [ ] 冻结成功与代表性安全失败形式。
- [ ] 确认 contract/ADR 影响；若业务 producer 进入 Runtime/Host，取得新的明确授权。
- [ ] 单独授权 fresh real 调用额度与证据 redaction。

## 4. 本批实际执行

| Activity | Result |
|---|---|
| Feature ID uniqueness | PASS |
| Four-file package creation | PASS |
| Schema/strict structural validation | PASS |
| D0 exit gate | BLOCKED / exit 1：`product_ux.status must be PASS for D0`；真实入口和阻断性产品/安全决策未关闭 |
| Code change | NOT RUN |
| App / Runtime / Provider / model startup | NOT RUN |
| Real calls | 0 |
| Tool D4 | NOT RUN |

## 5. Stop conditions

- 不注册或临时配置 MCP/Connector/dynamic tool。
- 不从模型文本、fixture 或 generic projection 补造 producer。
- 不触达 FEAT-138、FileChange、Diff、Command 或写权限扩展。
- 不执行 destructive/fault/attack 验证。
- 本次 D0 package/preflight 后停止；D0 保持 blocked，等待 Owner decision。
