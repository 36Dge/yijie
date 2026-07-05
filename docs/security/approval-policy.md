# Approval Policy

## 高风险操作

以下操作必须强制走审批：

- 发布或下架 listing；
- 修改标题、图片、描述、变体；
- 修改价格；
- 修改库存；
- 修改广告预算；
- 暂停或开启广告活动；
- 给买家发送消息；
- 批量操作订单。

## 流程

```text
Codex tool call proposal
  -> yijie-agent-host policy check
  -> yijie-api approval task
  -> desktop approval card
  -> user approve / reject
  -> connectors execute
  -> audit log
```

## 默认规则

未经明确审批策略覆盖的写操作一律拒绝。
