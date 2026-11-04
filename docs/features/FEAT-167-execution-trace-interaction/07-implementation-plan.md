# 实施顺序

## 0 契约固定

Native6/SSE13/IPC6/format6；生成、校验、固定完整commit。

验收：下游锁定且生成一致

## 1 新格式读取

只读6，删除archive5兼容；不增加SQL43或per-turn profile。

验收：旧格式明确拒绝，正常6保存重开

## 2 Host

仅v6/SSE13；原生命令动作、工具上下文、willRetry安全投影及developerInstructions。

验收：路由退役、phase/状态不改写

## 3 Native

SSE13→归并→事务保存6→IPC6；通知作用域保留。

验收：commit-before-publish及跨仓联调

## 4 前端

公开说明分段，连续活动组；内存展开，外层异常/审批，原详情复用。

验收：AC1–AC7单元及组件覆盖

## 5 集成与交付

安全回归、构建、正常清理旧数据、固定入口启动、UI/模型/重开验收。

验收：真实证据逐项列出；禁止测试NOT RUN
