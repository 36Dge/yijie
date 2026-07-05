# ADR-0008: RAG 知识服务独立边界

## 状态

Accepted

## 日期

2026-07-04

## 背景

跨境电商平台规则、法律政策、物流、税务和禁限售知识更新频繁，且需要 citation、版本和 freshness 管理。

## 决策

知识抓取、清洗、chunking、embedding、索引、检索、rerank、citation 和 eval 放入 `yijie-knowledge`。

## 备选方案

把知识检索放入 API 或 Skills 会简化早期调用，但会混淆业务状态和知识版本。

## 影响

- Knowledge 独立管理数据源和版本；
- API 只注册知识库版本和任务元数据；
- Skills 通过 Agent Host 或工具调用使用检索结果。

## 风险

检索质量需要 eval 数据集和人工评估持续校准。

## 后续动作

- [ ] 定义 source、document、chunk 和 citation schema；
- [ ] 定义 retrieval eval。
