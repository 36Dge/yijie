# Knowledge Ingestion Failure Runbook

## 快速判断

- 数据源是否可访问；
- 文档解析是否失败；
- chunking 或 embedding 是否超时；
- vector store 是否可写；
- 知识版本是否成功发布；
- citation 是否生成。

## 原则

政策和规则类知识发布失败时，不允许静默降级为无来源回答。
