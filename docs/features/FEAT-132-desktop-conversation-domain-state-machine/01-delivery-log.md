# FEAT-132 调整实施记录

2026-09-08。本次用户明确从“只给方案”推进为实施，授权边界为粘贴任务书。原交付日志保留在 [history](history/2026-08-27/01-delivery-log.md)。

1. 只读复核各仓 AGENTS、真实 HEAD、FEAT-132、相关 ADR 和 133/134/135/136/152 消费者；确认固定 Runtime 的原生历史限制。没有修改 yijie-codex。
2. 修订 FEAT-132 及 ADR-0013/0016 的权威边界。原 D4 不继承，新 paid budget=0。
3. 从已有 Runtime RPC/通知定义新增 Contracts 原生安全投影；生成 Go/TS DTO、Desktop 私有 Rust/TS/AJV 边界，记录未发布候选来源。
4. 接通 Host 真实 thread/read RPC → v7 SSE → Native 单一缓冲 → SQLCipher → Vue 完整视图。
5. 添加前向 migration 14、Host schema 5，分离本地提交失败和原生执行状态；实现 coordinator 原生读恢复以及 UI 只读隔离。
6. 删除旧 TS/Rust/Host 内容与状态推断职责、旧数据库派生写入、全局 legacy timeline fallback。旧记录保留只读，附件/Artifact/权限公共能力保留。
7. 执行安全定向测试、来源/生成物检查、构建和独立审查；修复测试暴露的真实问题。没有运行广泛的故障/攻击 fixture 测试集。
8. canonical 预检实际失败：`FEAT-152 Contracts source differs from its committed pin: scripts/generate.mjs`。候选尚未提交/重新 pin；没有绕过来源门禁，没有伪称启动或 D4 成功。

所有源码和文档仍未提交；没有 commit/push/tag/deploy，没有付费调用，没有强杀、权限破坏、危险 fixture 或 binary 替换。
