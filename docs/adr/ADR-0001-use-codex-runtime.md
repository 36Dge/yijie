# ADR-0001: 使用 Codex Runtime 作为易界 AI 的 Agent Runtime 内核

## 状态

Accepted

## 日期

2026-07-04

## 背景

易界 AI 需要具备任务执行、上下文管理、工具调用、状态管理和可观测性等 Agent 能力。团队决定不从 0 自研完整 Agent 平台。

## 决策

采用 Codex Runtime 作为易界 AI 的 Agent Runtime 内核。易界维护 `yijie-codex` fork，并通过薄适配层 `yijie-agent-host` 连接业务系统与 Runtime。

## 备选方案

自研 `yijie-agent-platform` 可以获得更强控制力，但成本高、周期长，容易偏离跨境电商业务价值。

## 影响

- 必须独立维护 `yijie-codex`；
- 必须维护 Codex 上游同步和 patch 策略；
- 领域能力放入 `yijie-skills`、`yijie-connectors` 和 `yijie-knowledge`；
- 不允许把业务逻辑写入 Codex 内核。

## 风险

上游变更可能带来兼容性风险，需要 runtime compatibility tests。

## 后续动作

- [ ] 创建 `yijie-codex` fork；
- [ ] 定义上游同步流程；
- [ ] 定义 Runtime 兼容性测试。
