# Codex Runtime Upgrade

## 流程

1. 拉取上游 Codex tag；
2. 更新 `yijie-codex`；
3. 应用易界 patch；
4. 执行 runtime compatibility tests；
5. 更新 `CHANGELOG.yijie.md`；
6. 通知 `yijie-agent-host` 做兼容性验证；
7. 发布 runtime build。

## 原则

升级不得把跨境电商业务逻辑写入 Runtime 内核。
