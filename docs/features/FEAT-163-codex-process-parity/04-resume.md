# FEAT-163 续办入口 — 每轮先读

最后更新：2026-10-24。本页是记录，不是自动执行器。

## 当前结论

**本轮复审和已确认代码遗漏修复已落地，但FEAT-163整体FAIL/in_progress，未通过D4。** 用户目标仍是每次对话的处理机制和正式答案前体验对齐Codex，必须复用现有Runtime，不能仅折叠或隐藏日志。最新事实以[02逐项验收](02-verification.md)第10节和[07复审](07-implementation-reaudit.md)末三节为准，旧原题成功不能覆盖本轮失败。

阻断项：专家第8/9回合在授权8192输出上限下未交付；第9回合137秒无公开进度、原生补丁参数被截断且未执行。普通第10回合有进度和答案，但执行sleep 1空操作。真实Provider已收到禁止dummy wait等指令，不能继续用“补了prompt就已解决”作结论。仅Runtime legacy冷历史仍缺工具条目；正常已保存历史恢复通过。

## 当前App与预算

日常无代理App已经canonical重建并就绪：`YIJIE_FEAT156_LOCAL_CANDIDATE=true pnpm tauri:demo-fast:app`，exec83289，启动PID98651，当前保留打开。诊断App26892、meter98234均正常退出0。不要重复启动meter、不要强杀或故障注入。

来源回执：evidence/reaudit-daily-final-launch-receipt.json；恢复与重开：reaudit-daily-restoration-reopen.json。日常/诊断构建只有YIJIE_PERMISSION_VERIFICATION_BASE_URL覆盖hash不同，Host/Runtime/worker来源一致。固定Runtime SHA256 `9766d7e10d25327f0595964a19ad67e1e1c1db0c22e5a65f9af66b547ab316c6`，Runtime源码未改。

**已用10/10用户回合、23/40模型HTTP、12/20联网动作（8原生搜索+4旧shell抓取），无在途。第11回合没有授权，即使HTTP仍有余额也不得发送。** 每请求上限8192，禁止付费产图、外部连接器、FEAT-162额度/调用。22请求已知input299186/output38854/total338040，第16请求正常中断用量未知；第20/21请求Provider报告output8195和incomplete，保留实际值。诊断请求注入了上限，不能声称与日常请求字节相同，也不能据此断言日常无覆盖时必然同样失败。权威台账paid-call-ledger.json、user-turn-ledger.json、budget-summary.json；meter运行时独占其台账。

## 本轮已修复，均复用原链路

- Host：原threadDeveloperInstructions供Start/Resume共用图像附加指令；普通原生工具不再被文案误限制为仅产图。permissionInstructions补全真实检索结果判断及默认native apply_patch指引，受管catalog仅精确已知旧字节正常升级。
- Desktop：completed且可展示的fileChange（含partial）算交付；失败/空变更不算。结构化草案同轮只显示一份；确认过的冷工具事实复用原阅读分组，不改原状态。空managed专家绑定不再产生空连接器面板；真实审批和截断提示仍在。已确认过程文字不附答案操作栏，失败末条unknown称模型消息并保留末条保护。
- 仍沿既有native v5/SSE v12、单一buffer/SQLCipher format5、Timeline分段和展开选择；没有新表、进度模型、执行循环、自动追问或Host命令去重。前轮已有Runtime commandActions/fileChange/appContext投影及hunk统计继续复用。
- 普通并发回执测试解除测试本身的等待死锁；草案真实Runtime测试改为符合固定client的tool_choice=auto+空工具列表，保留input-only限制。

本轮主要文件：Host internal/codex/{session_protocol.go,runtime_permissions.go,chat_models.go,process_parity_audit_test.go,process_parity_integration_test.go,scheduled_draft_integration_test.go}、internal/session/multimodal_test.go；Desktop src/components/chat/{ChatTurnGroup.vue,MarketChatActivity.vue,MarketChatActivity.test.ts,ChatProcessParityAudit.test.ts,ChatProcessPresentation.test.ts}、src/domain/conversation-process.ts及原设计文档。Runtime/Contracts本轮无本任务源码改动；共享FEAT-162变更另归属，不能回滚或混算。

## 实际验证摘要

Host两模型各5种入口Start/Resume等9顶层检查、session7项、原生本地Provider2个集成/6次local HTTP通过；这些不是付费Kimi资格。前端9文件320PASS/2原有skip，现场149及最终50是重叠增量，不相加；lint-final-5、Host vet、设计文档、Native恢复和reader、五仓diff与strict文档检查通过。最终build5和日常恢复build均通过。

重开：第8的2公开消息/6命令/2段分组/失败保持，HTTP20→20；最新日常重开第8/9两轮失败状态、第10进度/2搜索/sleep/答案均保持，Runtime task_started仍专家2/普通1，没有创建新回合。公开消息Provider与Runtime hash相同；第10工具结果下一请求完整回灌。原题城市事实未全面独立核实，不用界面成功证明事实正确。

关键证据：reaudit-turn-9-diagnosis.json、reaudit-turn-10-diagnosis.json、reaudit-tenth-instruction-provenance.json、reaudit-eighth-reopen-check.json、reaudit-daily-restoration-reopen.json及同名前缀AX/截图。只有Runtime冷历史时legacy缺命令且本地store拒绝paginated，不能通过开关或补造恢复。

## 下一步（不可遗忘）

1. 先核对当前App/源码/台账，不重复真实调用。Owner若授权继续付费验证，必须明确新增用户回合及是否维持8192输出上限；剩余HTTP/联网不是自动增回合许可。
2. 按07末节审计已有Kimi profile、有效指令组合与原生Responses预算/搜索机制。若需调整，沿既有模型契约、catalog正常升级、Start/Resume和原工具机制；先完成可审查改动及本地检查再用获批额度验证。不要复制新进度引擎、隐藏sleep、按命令字符串静默去重或自动续问。
3. 专家长任务须实际有及时公开进度及有效文件交付，普通研究须无dummy执行，再做正常重开。失败证据不得被后续成功覆盖。AC001/002/004/006与新版本完整布局覆盖未全部通过，不能宣称每次对话都已对齐。
4. 保留当前所有dirty改动；无Git提交/推送/分支/tag/签名/发布授权。五仓HEAD未变、基线文件无缺失；证据快照reaudit-diff-review-current.json。共享FEAT-162的界面/凭据状态不属于本任务验收。

原方案：[00](00-feature-brief.md)、[01](01-delivery-log.md)、[03](03-audit-and-decisions.md)、[05](05-tool-activity-reference.md)。所有禁止的强杀、攻击fixture、权限破坏和可执行伪装均未执行。
