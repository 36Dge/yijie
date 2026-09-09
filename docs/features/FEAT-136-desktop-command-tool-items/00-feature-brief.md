# FEAT-136 — 基于 Codex 原生事实的 Command 执行 Item

日期：2026-09-09；demo_fast / local。用户已审阅前置方案并授权执行。本次调整复用 FEAT-132/134，不修改 Runtime、跨进程协议、数据库或权限。**本次八项 Must 已满足，local D4 PASS；Desktop 已固定为 8bfa5ca284fddb86d7cdd2a406c5041c49367688，元仓提交与远端同步另记交付记录。**

## 用户目标与范围

用户可以准确读取 Command 执行结果、安全输出和历史记录，区分原生失败、合法空输出、信息不完整及未观察到结束记录。Command 执行器、身份、status、exitCode、durationMs 和聚合输出由 Codex 提供，Host 做必要安全投影，Desktop 只读适配。

- 复用 native v7、NativeDisplayBuffer、thread/read/resume、SQLCipher 原生事实保存与旧档案读取。
- 原生展示和旧 v5 投影分开；不伪填旧 source event、cwd 结构、retention 或截断原因。
- 原生完整 Item 直接替换；Turn 结束不封口 Command，界面停止错误忙碌提示。
- 继续只展示已有安全最终输出，不启用原始 delta 或新累积器。
- 允许安全复制、键盘折叠与独立 aria-live；零值和空字符串不丢失。
- 真实 Tool 由 FEAT-144 承接；不新增 producer、注册、progress 或错误字段。

## 实际入口与职责

`Codex native notifications → Host native safety projection → NativeDisplayBuffer → SQLCipher → ConversationView → ChatCommandItem`。

普通 canonical 为 `pnpm tauri:demo-fast:app`，使用 `com.yijie.ai`、现有 app-data 与原 Host Home。旧 stable 隔离数据不冒充普通 Host 映射；没有可信绑定的旧任务不自动续跑、补发或猜测接管。

Host native 对 Command delta 只发 `command_output_pending_final` 诊断，收到原生完整 Item 后投影 Codex aggregatedOutput。这是已明确的分片脱敏/单一缓冲边界，不是 Runtime 没有流式输出能力。缺失冷历史仍如实披露，不复制 HistoryBuilder、解析 rollout 或开启实验历史。

## 八项 Must AC

| AC | 可判定结果 |
|---|---|
| AC-001 | 按原生身份、status、exit/duration 展示，保留 0；失败码只映射显式 status，不改事实 |
| AC-002 | 完整 Item 直接替换更长/不同/空输出；未见 started 的 completed 也不被丢弃，无正文对账 |
| AC-003 | Turn 结束、历史或连接不明时不误报 busy，保留 Item 状态与缺结束记录 |
| AC-004 | cwdLabel、null、空输出、partial 可区分，不伪造截断原因或把失败空输出说成成功 |
| AC-005 | 只显示/复制已有安全输出，保持会话诊断范围，不产生永久等待误报 |
| AC-006 | SQLCipher 正常重开保留来源/身份/终态，冷历史不覆盖，旧 Command 档案可读 |
| AC-007 | 定向测试与 canonical 启动/切换/退出重启、light/键盘/aria-live/200%、附件/Artifact/Composer/FEAT-152 无定向回归 |
| AC-008 | 无新引擎、累计或历史重建；删除/保留有引用依据，历史及 Tool 限制真实记录 |

这些 AC 是本次原生调整的验收，状态见 feature.yaml 和 02-verification.md。原 2026-08-30 五项 Command D4 四文件完整归档于 history/2026-08-30，日期、源提交、prior 3/3 FAIL、fresh 1/5 PASS 不覆盖或继承。

## Contract First 与授权

contract-impact=none：纯进程内展示及必要布局修复；现有 Host wire/private IPC/schema/migration/Runtime/权限均不改。原 Contracts/Host pin 保持；不存在因文档提交必须机械 repin 的要求。

FEAT-137 永久退役，FEAT-152 为独立原生权限功能，不继承 FEAT-137 source PASS。既有 v4/v5 reader/资源适配仍保留。原 FEAT-142/143 后移职责与 dark/精确 1180×760 未执行范围继续保留，不补写 PASS。

用户另行批准本次最多 10 次 MiniMax-M3 文本请求（含标题、审批审查和自动重试），实际 3 次；图片 0 次，旧额度没有转用。用户于本次交付收尾确认“授权”，明确覆盖已核验的 Desktop → 元仓提交、普通推送和必要的交付结果补充提交；不更新无变化的 pin，不强推、不打 tag、不部署。所有测试均为正常非破坏性操作，不复制用户数据库或凭据。

完整源码证据、删除/保留决策与执行步骤见 [审计方案](03-native-command-audit-and-plan-2026-09-09.md)。
