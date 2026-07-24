# ADR-0004: API 契约优先

## 状态

Accepted

## 日期

2026-07-04

## 背景

多仓协作下，前端、后端、连接器和 Agent Host 容易重复手写 DTO 和事件结构。

## 决策

所有 HTTP API、事件、工具 schema 和 SDK 变更优先在 `yijie-contracts` 中定义，再由下游仓库实现。

[`ADR-0011`](ADR-0011-enforce-contract-first-governance.md) 将本决策的“优先”
明确为易界公共边界的强制合并/发布规范，并补充执行边界、权威源特例、合并/部署
顺序和例外机制。现行操作规范见
[`docs/dev/contract-first.md`](../dev/contract-first.md)。

## 备选方案

各仓独立定义 DTO 可以短期加速，但会造成协议漂移和联调成本。

## 影响

- `yijie-contracts` 先于依赖仓发布；
- 生成 TypeScript SDK、Go SDK 和 JSON Schema；
- PR 必须标记是否涉及 contract。

## 风险

早期会增加一点流程成本，需要脚本自动化生成。

## 后续动作

- [x] 初始化 `yijie-contracts`；
- [x] 定义 OpenAPI、Protobuf、JSON Schema 和 AsyncAPI breaking change 检查；
- [x] 建立 Go/TypeScript SDK 和 AsyncAPI bundle 生成脚本；
- [x] 由 ADR-0011 补齐项目级执行门禁。
