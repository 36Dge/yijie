> 最新状态：2026-10-24按用户要求再次复审，整体完成结论已撤回；以[07实现复审](07-implementation-reaudit.md)和04续办为准，以下前轮完成措辞仅为历史。

> 状态更新（2026-10-24）：用户已授权按本方案实施及有限真实调用。原规划措辞为历史背景，以04续办和02最新实测为准；本地适用验收已完成，范围与限制见02第9节。

# FEAT-163 — Codex 原生处理过程与前端体验对齐

> 2026-10-24 · demo_fast / local · 已按用户授权实施并完成本地适用验收；无提交或发布。
> **续办入口：[04-resume.md](04-resume.md)。** 本文件冻结目标；[01](01-delivery-log.md)定义执行步骤；[02](02-verification.md)定义验收；[03](03-audit-and-decisions.md)解释复审结论；[05新增工具分段参考](05-tool-activity-reference.md)补充分段展开与原生字段缺口。

## 1. 用户目标与不得缩减的范围

用户原话：**“易界的每次对话，在答案正式输出之前，易界的处理过程与前端显示与 codex 一致。”**

用户追加硬要求：**“能复用现有 runtime 机制的必须复用。”** 初始阶段先审计并落成方案；用户随后明确授权实施，实际进展以04和02为准。

目标包含同一条完整链路：真实公开进度的产生 → 原生执行和工具结果回传 → 消息及时传递 → 前端按真实顺序呈现 → 正式结果正常交付 → 重开后完整回看。不得缩减为隐藏日志、减少计数、改几个标题或让截图看起来清爽。

“每次对话”是所有现有会话入口采用一致机制和呈现规则。无工具短问答可以直接流式回答；需要工具或多步处理的任务应有任务相关的公开过程说明。不强制每轮固定三段话，不设置人为最短等待，不用短问答例外豁免长任务。

覆盖普通新建、现有会话续聊、有项目/无项目，以及已支持的附件/看图、图像或Artifact生成、技能、专家、连接器和结构化结果入口。各入口实际工具权限和结果校验仍沿原机制，不新增这些能力。计划任务使用聊天链路时验证公共基础指令组合不回退，但不改调度器。不存在或未启用的入口如实登记，不能冒称全产品验证。

不包含：重写 Agent 平台、替换模型、默认升级 Runtime、另建搜索/抓取服务、纠正全部城市数据、扩展任意多 Chat 窗口、重新执行或改写旧历史、公开发布。

## 2. 已有 Runtime 能力与唯一复用链路

当前审计的固定 Runtime 为 Codex 0.144.6 系列，已有以下能力；版本差异不是“缺少 commentary”的证据：

| 已有能力 | 现有源码锚点（CrossBSD 相对路径） | 本需求处理 |
|---|---|---|
| 工具前 preamble、长任务 progress 指令 | `yijie-codex/codex-rs/models-manager/prompt.md`：Preamble messages / Sharing progress updates | 在已有有效指令组合中恢复对应通用沟通原则，不另造进度工具 |
| Commentary / FinalAnswer / phase unknown | `yijie-codex/codex-rs/protocol/src/models.rs`：MessagePhase | 原样传递，不给 null 猜填 phase |
| AgentMessage 与独立 Reasoning | `yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs` | 公开助手消息与推理摘要分开，不互相改名 |
| 原生工具循环及 call/output 历史 | `core/src/session/turn.rs`、`context_manager/history.rs`、`tools/parallel.rs` | 在此链路查缺口，不在 Host 建第二个循环 |
| Host 原生投影与安全处理 | `yijie-agent-host/internal/session/native_conversation.go`、`native_process.go` | 同一身份/正文/顺序的安全投影，不生成研究结论 |
| Native 单一显示缓冲与事务保存 | `yijie-desktop/src-tauri/src/chat/native_conversation.rs`、`native_conversation_storage.rs` | 保留唯一缓冲、先提交再发布、现有 cursor/revision 规则 |
| 现有阅读、流式和滚动组件 | Desktop `conversation-view.ts`、`conversation-timeline.ts`、`ChatTurnGroup.vue`、`useChatStreamPresentation.ts`、`useChatScroll.ts` | 在原组件内改阅读组织，不建状态机/第二条打字队列 |

唯一产品链路：

```text
Provider 原生助手消息 / 工具调用
→ Codex Responses 解析、原生 Turn 循环、工具执行与历史
→ app-server item/* 和 turn/*
→ Host 原生安全投影
→ Desktop NativeDisplayBuffer
→ SQLCipher commit_native_view → publish_native
→ 现有 store / ConversationView / Timeline / ChatSafeContent
```

Runtime 支持 commentary 不等于自动代模型写 commentary。输出指令、Provider 事件、Runtime 解析及 UI 必须联合通过。不得另加模型总结器、systemProgress 原生条目、Host 自动追问、旁路补答案或前端定时编造文字。

## 3. 目标交互与完整状态

主过程由真实公开助手文字和淡色、可独立展开的本段工具摘要交错组成。正文继承现有字体、间距、主题和 Markdown；摘要辅助说明活动，不抢占阅读主线。保留现有整轮耗时/展开入口，同时保留每段工具的独立展开。正常成功不逐行堆叠边框、绿色勾选及右侧“已完成”。展开本段能看具体文件动作、命令安全片段、App/工具和文件变更；单项还能查看输出或变更详情。reasoning、重复摘要和协议诊断另入技术详情，**不能把全部工具明细统一挪到技术详情区**。详见05。

| 状态 | 行为 |
|---|---|
| idle | 等待输入，没有虚构过程 |
| loading，尚无正文 | 仅一个基于真实活跃观察的等待位；不把等待文案当模型进度 |
| 公开消息到达 | 立即沿原流式正文组件显示，保留原文和时序；不等整轮结束 |
| 工具活动 | 按原生 action/type形成本段淡色动作摘要，可包含读取/编辑文件、命令及App/工具；展开只显示本段明细，查询/页面/文件及命令安全预览取真实字段 |
| 长任务执行 | 公共说明解释处理方向、新发现或限制及下一步；不只统计工具次数 |
| 显式 final_answer 非空首段到达 | 答案立即可读；未手动选择时默认收起过程，不等 turn/completed |
| phase=null | 正文立即可读，沿已有只读布局兼容与末条保护；不改 phase，不仅因收到正文就判定 final 或提前收起 |
| 真实 Turn 终态 | 停止 busy 与积压显示动画；未手动选择时可收起过程，保留末条可读回答 |
| 用户手动展开/收起或操作焦点 | 用户选择优先于新增 delta、工具完成、最终答案及整轮完成的默认折叠；保持键盘焦点 |
| completed 且普通问答无可读结果 | 显示一条准确的未收到可显示回答提示；commentary-only 不冒充 final；合法 shell/compact/Artifact 结果不一概误报 |
| failed / interrupted | 复用原失败或中断状态和部分正文，不再叠加同义无回答警告，不补发 |
| reasoning 缺结束事件 | 真实最后状态保留在详情；Turn 结束后不继续动画，不伪造 item/completed |
| 待审批/决策提交/核对失败 | 现有审批入口与状态保持可见、可操作；过程收起不隐藏待处理事项 |
| 断连/不可用/冷历史 inProgress | 使用已有同步可用性说明；没有有效实时观察不假称仍运行，不自动重发 |
| retry | 仅沿已有明确用户操作和幂等回执路径；不能新增自动追问、换模型或新 Turn |
| 正常重开/续聊 | 原消息、顺序及已观察事实恢复，历史不重播打字；新一轮独立计时与展开 |
| 上翻/选区/旧轮次定位 | 不被流式更新及折叠高度变化强拉到底 |
| 亮暗主题/最小窗口/减少动态效果 | 继承现有 tokens 和降级逻辑，1180×760 无重叠；完整内容在详情可读 |

主线不显示“网页搜索 N 次·命令 N 条”总览、“重复摘要（原始记录）”卡片和普通生命周期诊断长列表。该规定只证明阅读层降噪，不能单独证明机制对齐。

## 4. 冻结的十项 Must AC

| AC | 用户结果与通过条件 | 证据要求 |
|---|---|---|
| AC-001 | 所有现有会话入口沿统一原生链；短答、工具任务、长任务及续聊使用同一呈现规则 | 入口矩阵、指令/工具面来源、实际场景覆盖；不能只测一题 |
| AC-002 | 真实长任务在正式答案前有处理方向说明，获得新信息后有实际推进说明；内容来自原生公开助手消息 | 固定 Kimi 配置的真实消息与 UI 时间线；0 公开进度不得 PASS |
| AC-003 | 消息身份、原 phase、内容和顺序跨层保持；进度在工作期间显示，而非终态回填 | Provider/Runtime/Host/Native/UI 的关联摘要、到达时间及画面 |
| AC-004 | 工具结果进入下一请求，执行次数与原生调用对应；原题不再反复进行无信息增益的相同读取 | call/output/request 证据；零 dummy 播报工具；新调用与事件重放分开检查 |
| AC-005 | 普通问答最终交付可读答案；空答、失败、中断如实显示，合法无文本任务不被全局改 failed | 真实问答最终正文、普通生命周期样例；不把 completed 等同已交付 |
| AC-006 | 公开说明穿插淡色可展开的分段工具摘要；展开有真实文件/命令/App/变更明细，单项详情可查；技术诊断另置，审批可见 | 正式组件与正式App，含05的TG-01至TG-10适用场景；静态干净截图不足以证明AC-002 |
| AC-007 | phase=null 到达即显示；显式 final 与终态折叠规则正确；手动选择优先，末条答案不被吞掉 | 现有兼容路径普通样例、真实入口、焦点/滚动检查 |
| AC-008 | 正常关闭重开、切会话、重复通知和迟到订阅保持内容/顺序/隔离，不补造历史、不重复执行 | 现有缓冲/存储/订阅专项，正式 App 正常重开 |
| AC-009 | 流式、选区、滚动、亮暗主题与1180×760可读；无额外进度动画队列 | 原组件检查及正式 App 视觉记录；180ms仅为现有到达后显示追赶目标 |
| AC-010 | 复用和证据门槛落实；适用契约检查完成；安全非破坏性验证及预算记录真实 | 差异审阅、来源/兼容证据、全部失败保留、授权台账 |

通过必须是十项联合成立。Provider 没产出、单测已能显示、工具列表已折叠、换成一次搜索短题、只剩系统等待提示，均不能豁免 AC-002/003/004/005。样例通过不等于真实模型通过。真实问题未发生时不能写“真实通过”。

AC-002要求真实公开assistant消息及其任务意义和时序，不强制Provider必须发出某个phase字符串。phase=null可沿已验证的原生兼容路径满足用户体验，但证据必须标明phase unknown、保持原文/身份/顺序且结果独立可读；不能将其写回成已证实的commentary/final_answer，也不能用系统文案代替。

## 5. 仓库、契约与并行边界

规划审计阶段仅写 `yijie` 文档与参考图，分类为none。后续用户授权实施，实际跨仓安全投影与持久reader按breaking/replay完成；不改变权限。新截图审计已确认文件动作/变更/App字段消费缺口，计划中的安全投影版本和持久读取按 **breaking/replay** 保守审查；在S2冻结具体版本与兼容方案，不把本轮文档分类当未来代码分类。

现有native history v4 / SSE v11足够表达基础公开消息、phase、推理、普通工具和搜索，但没有完整消费Runtime已有的commandActions/fileChange/appContext。新增图的完整目标需要沿原native conversation家族补版本化安全投影和持久reader，不能原地给封闭v4塞字段，也不能以unknown永久代替。默认不新增数据库表、不保存分组结果、不造系统进度事件。纯UI分段仍可为none；完整字段接入及旧读者兼容按05执行。

Runtime边界权威：固定Runtime canonical schema → Contracts兼容投影 → Host → Desktop。上述活动字段已存在于固定canonical schema，无需为消费它们先升级/重建Runtime；若消息缺失另有已证实Runtime缺陷才进入原补丁分支。新输出必须等兼容reader就绪再激活。旧数据不补写，回滚不能降级写入不兼容格式。

FEAT-162规划初审时只有检索研究证据；本次补图核查已见跨仓检索相关改动，其实现/授权/验收并非本轮审计范围。它不自动成为本需求已完成或已批准的前置。若未来消费其工具，单独核对接口、工具面、指令哈希、预算与依赖版本。真实curl是原生执行，不得先叫成“桥接命令”再隐藏。

## 6. 授权与停止边界

- 当前授权：方案实施、跨仓代码与生成、普通验证、canonical构建/正常启动退出，以及最多7回合/40HTTP/每请求8192输出token/20网络动作。
- 未授权：Git提交/推送/分支/tag/发布，及第8模型回合。实际7回合/17HTTP/10网络，诊断已正常停止。
- 后续明确实施授权只解锁其覆盖范围；付费预算及 Runtime 补丁范围据实际用户决定记录，不能把旧任务额度当可用授权。
- 复用正常停止、退出、EOF及清理。禁止强杀制造异常、权限破坏、可执行文件伪装、恶意资源或攻击注入；不合规旧测试不执行并注明影响。
- 30分钟无新事实停止猜测补丁；90分钟同一阻塞扩大有区分力的诊断；120分钟非核心验证不继续挤占核心；240分钟核心阻塞提出具体技术选择；16小时未完成时重新评估。不得为时间盒降低上述目标，缩范围需用户明确决定。

## 7. 参考与当前状态

- [Codex目标截图](evidence/reference-codex.png)
- [Codex分段工具摘要与展开明细截图](evidence/reference-codex-tool-groups.png)及[对应补充规范](05-tool-activity-reference.md)
- [易界活动列表截图](evidence/reference-yijie-activity-list.png)
- [易界重复摘要截图](evidence/reference-yijie-repeated-summary.png)
- [起始源码/工作区/参考图哈希](evidence/planning-baseline.json)
- [复审依据与决策](03-audit-and-decisions.md)

当前：本地实施及适用验收完成；正式记录与限制见02第2/8/9节及04。文档门禁不替代真实证据或生产批准。
