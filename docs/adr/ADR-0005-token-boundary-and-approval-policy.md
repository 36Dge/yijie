# ADR-0005: Token 边界与审批策略

## 状态

Accepted

## 日期

2026-07-04

## 背景

易界 AI 会连接卖家店铺和外部平台 API。平台 token、PII 和高风险写操作必须有明确安全边界。

## 决策

平台 token 只存在于业务后端或连接器安全边界内。Codex Runtime 和 Skills 不直接持有 token。高风险操作必须经过 Agent Host 策略检查、API 审批任务和桌面端审批卡片。

## 备选方案

让 Runtime 直接持有 token 能减少调用链路，但安全风险过高。

## 影响

- Connectors 负责 token vault、refresh、rotation；
- Agent Host 负责策略检查和工具调用审批；
- Desktop 展示审批卡片；
- Audit log 记录完整链路。

## 风险

审批体验可能影响效率，需要按风险等级优化默认策略。

## 后续动作

- [ ] 定义 approval policy；
- [ ] 定义 audit log schema；
- [ ] 定义高风险工具清单。
