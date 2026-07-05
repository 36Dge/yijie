# 易界 AI 总体架构

## 定位

易界 AI 是面向跨境电商卖家的 AI native TOB 产品。系统以 Codex Runtime 作为 Agent Runtime 内核，通过业务后端、薄宿主层、跨境电商 Skills、连接器和知识库，把 AI 能力落到选品、合规、Listing 优化、广告投流、物流追踪和经营分析等 SOP 场景。

## 分层

```text
Product Experience Layer
  yijie-desktop
  yijie-admin-web

Business Platform Layer
  yijie-api

Agent Runtime Adapter Layer
  yijie-agent-host

Agent Runtime Kernel
  yijie-codex

Domain Capability Layer
  yijie-skills

Tool Execution Layer
  yijie-connectors

Knowledge Layer
  yijie-knowledge

Contract & Infra Layer
  yijie-contracts
  yijie-infra
```

## 核心原则

- Codex 是 Runtime 内核，不承载跨境电商业务逻辑；
- `yijie-agent-host` 是薄适配层，不重建完整 Agent 平台；
- 平台 token 留在业务后端或连接器安全边界内；
- API、事件和 schema 变更遵循 contract-first；
- 高风险工具调用必须审批、审计、可追踪；
- 知识库回答必须尽量提供来源和版本。

## MVP 闭环

第一条闭环优先验证：

```text
桌面端输入 Amazon 商品链接
  -> API 创建任务
  -> Agent Host 创建 Codex session
  -> Codex 加载 Listing 诊断 Skill
  -> Connectors 抓取公开 Listing 信息
  -> Knowledge 检索平台规则
  -> 生成诊断报告
  -> Desktop 展示结果
  -> Audit log 记录链路
```
