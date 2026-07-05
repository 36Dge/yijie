# ADR-0004: API 契约优先

## 状态

Accepted

## 日期

2026-07-04

## 背景

多仓协作下，前端、后端、连接器和 Agent Host 容易重复手写 DTO 和事件结构。

## 决策

所有 HTTP API、事件、工具 schema 和 SDK 变更优先在 `yijie-contracts` 中定义，再由下游仓库实现。

## 备选方案

各仓独立定义 DTO 可以短期加速，但会造成协议漂移和联调成本。

## 影响

- `yijie-contracts` 先于依赖仓发布；
- 生成 TypeScript SDK、Go SDK 和 JSON Schema；
- PR 必须标记是否涉及 contract。

## 风险

早期会增加一点流程成本，需要脚本自动化生成。

## 后续动作

- [ ] 初始化 `yijie-contracts`；
- [ ] 定义 breaking change 检查；
- [ ] 建立 SDK 生成脚本。
