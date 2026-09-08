# FEAT-132：Codex 原生对话机制接入与视图适配

2026-09-08 调整版，用户已授权实施。原编号和目录保留。原实现及原 D4 仅属于 [历史版本](history/2026-08-27/00-feature-brief.md)，不能作为本次验收结果。

2026-09-09：本次调整 D4 PASS，十项 Must AC 已通过；固定来源与真实证据见 [最终验收](02-verification.md)。

## 目标与范围

Codex 原生 Thread / Turn / Item 决定执行身份、phase、生命周期、最终内容和结果。易界只保留鉴权、关联、安全投影、传输、一个可丢弃的 Native 显示缓冲、加密产品记录和 Vue 展示交互。

删除旧 FEAT-132 reducer、hydrate/reconcile、正文前缀对账、Item 身份猜测和自动封口。不得把这些职责移到 Host、Rust、数据库或另一个服务。投影异常、断线、容量限制只影响可用性，不能伪造 Runtime failed、释放 busy 或自动重发。

本地提交（queued/submitted/failed/uncertain/cancelled）、原生执行、显示同步和权限审批分别保存。未到达 Runtime 的请求仍属于 outbox。

## 已授权设计

采用“Codex 原生协议驱动 + 单一展示适配 + 原生事实加密保存”。详见 [实施与来源说明](03-native-protocol-adjustment.md)。

- Runtime 0.144.6，沿用 FEAT-136 保留产物；不修改核心、补丁、二进制或实验 API。
- 原生历史来自 thread/read(includeTurns=true) / resume；不读取或解析 rollout，不复制 ThreadHistoryBuilder。
- 最终 Item 替换显示缓冲；Turn 完成不能替未完成 Item 补造结果。
- 每 Turn 使用一个明确来源的 Item 集合。实时与冷历史不按正文、ordinal、位置或 phase 合并。
- 保存已观察原生事实及来源；已观察 failed 不能被冷历史 completed 覆盖。能力不足时显示“不完整”。
- 原有记录为只读 legacy archive；仅有 Runtime ID / event ID 不构成原生来源证明。
- 保留 SQLCipher、Keychain、scope、选择 epoch、outbox、附件、Artifact、Command、Composer 和 FEAT-152 权限语义。

## 实施与验收边界

本次为已做本地提交、未发布的多仓开发候选，contract-impact=breaking，Desktop migration 14、Host bbolt schema 5 均前向迁移。旧发布 HTTP/SSE 保留单向兼容投影；新 Native 走 v7。正式激活顺序为 Contracts 固定来源 → Host 固定来源 → Desktop 固定来源 → 正常生命周期和真实验收。

切换前必须在旧版正常结束活跃 Turn，再正常退出。没有新来源证明的旧活跃行保持不可自动接管，不能强杀、伪造结束或猜测绑定。

验收标准沿用户任务书的十项 Must AC。定向测试、构建、独立审查与缺口见 [验证记录](02-verification.md)。本次 paid budget=0；真实模型 D4 未执行。不得沿用 2026-08-27 授权额度或结果。

推送、部署、发布、新 Tool 能力、FEAT-137 重启和 FEAT-152 权限语义调整均不在本次范围内。

2026-09-09 用户已明确授权本地提交及必要修复提交。实际来源、隔离验证与 D4 预算见 [当前推进记录](04-source-freeze-and-d4-2026-09-09.md)。
