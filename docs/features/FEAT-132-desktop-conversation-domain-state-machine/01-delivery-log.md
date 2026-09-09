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

以上为2026-09-08阶段记录，当时未提交、无付费调用。

2026-09-09：取得明确本地提交与真实预算授权后按 Contracts→Host→Desktop→元仓固定来源。实际 canonical 验收发现并修复 AJV helper、空助手占位历史和流式期间中断分发3个问题；真实发送/附件/Command/权限/中断/退出重启/图片Artifact全部通过。最终19次文本、1次图片，十项AC均PASS，D4关闭；仅本地提交，未push/tag/deploy。详细过程与边界见04-source-freeze-and-d4-2026-09-09.md，最终结果见02-verification.md。

2026-09-09 后续日常入口验证：修正3份说明中的过期验收状态；保留已经单独提交的权限弹窗UI变更。原Host Home普通入口暴露旧清理记录被草稿前置读取阻断的问题，Desktop提交`c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b`复用已有清理权威和撤销订阅流程，恢复只读历史，保留输入拒绝且不重试删除。定向回归及真实旧记录复查通过；详细结果见[日常入口报告](05-daily-entry-verification-2026-09-09.md)。本轮无新增模型调用。
