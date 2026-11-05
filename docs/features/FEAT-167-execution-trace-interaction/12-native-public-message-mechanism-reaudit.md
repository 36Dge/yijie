# 公开 assistant 消息：Runtime 后端机制复审

> 当前交付与验收结论见 [13-public-progress-native-delivery.md](13-public-progress-native-delivery.md)。本文保留此前审计/实施时点的历史记录；旧额度、待审、暂停和未完成状态不代表当前状态。

2026-11-05。`contract-impact = none`（本次仅源码/公开消息记录复审、文档和
测试用量账本纠正；未改变产品执行、协议、数据或启用新能力）。后续显式阶段
适配至少是 semantic，涉及不兼容风险时按 breaking 评审；尚未实现或批准。

本次新增真实模型调用 0 次，无构建、UI 操作、数据库写入或迁移，无新增核心
补丁。原工作树保持；不清库、不包含 diff。已有真实额度各 24 用户轮，实际
各用了 N01 App 1 轮、N02 wire 核对 1 轮，合计各 2 轮。没有把剩余额度当作
继续试错的理由。

## Owner 最新目标与截图事实

多数实质任务应有任务特定开场与真实、有信息增量的中途沟通；非常简单的对话、
只要结果或受限格式可以直接回答。结果就绪及时交付，不强制每轮三条消息，
不把详细介绍/比较的失败样本事后改列为简单例外。Skills 默认显式与隐式均
支持，原生加载不变。

最新截图四个红框匹配三条原生 assistant Message：前两个框是同一个 Item 的
两个 Markdown 段落，其余两框各一个 Item。三条 phase 全为 commentary，
内容与图中所示一致，不是工具日志自动改写成的进展说明。

## 后端链路事实

1. `core/src/session/mod.rs:599`：base 优先级为显式配置、历史、模型默认。
   Host 已通过 developer 注入 v3；不能因为 fork 了 Runtime 就假定使用相同
   模型默认 prompt。Skills、权限和业务规则继续分层。
2. `core/src/client.rs:829`：组装 Provider 请求，包含原始历史、指令与工具。
   非 OpenAI 分支只清理内部 passthrough，不删除 assistant phase。本地 Runtime
   源码相同不意味着它调用的服务端模型和输出协议行为相同。
3. `codex-api/src/sse/responses.rs:329/433`：将 SSE 的消息/delta/完成信息映射为
   ResponseEvent。phase 描述消息语义；end_turn 是响应完成中的独立可选字段。
   未根据自然语言猜阶段。
4. `core/src/stream_events_utils.rs:313`：工具调用设置 needs_follow_up 并执行；
   普通 Message 生成 AgentMessage 的 started/delta/completed，完成单条消息不
   等于结束当前响应。`core/src/session/turn.rs:2279` 单独处理 end_turn=false。
5. `core/src/session/turn.rs:298`：正常执行循环合并 pending input，必要时继续
   同一 turn；没有“任意 commentary 自动再请求一次模型”的通用规则。
6. `app-server-protocol/src/protocol/event_mapping.rs:359`：发原生消息生命周期。
   Host Native6/SSE13 → Desktop Native 先提交再发布 → IPC6 → UI 公开消息独立
   展示、工具连续分组。前端不能生成上游没有的正文和进展。
7. 原始 ResponseItem 保留在模型历史；公开事件还用于 thread/read 与展示重开。
   两个闭环必须分别验证。重建历史 ID 可为 item-N，不强求等于 live Provider ID。

以上 Rust 路径均相对于 `yijie-codex/codex-rs`，同时核对当前候选补丁链。
安装版编译 JS 只作为前端证据，不能代替后端源码；本轮重核 app.asar SHA 未变。

## 新补核的原生扩展点

- **Stop hook**：`core/src/hook_runtime.rs:298` 接收 last_assistant_message；
  `turn.rs:374` 在正常结束点，获得 should_block 和非空 continuation_fragments
  后记录输入并 continue。无需自造 Host 循环。但它没有内置公开进展生成策略。
  当前 Host 的受管 provider 与 market isolation 明确关闭 hooks；不得直接开关
  绕过这项配置/安全边界，也不能将其伪装为供应商 end_turn=false。
- **TurnItemContributor**：`ext/extension-api/src/contributors.rs:292` 可处理
  已解析 Item。流式 OutputItemAdded 路径使用 Skip，完成态才运行 contributor；
  单在完成态改正文或 phase 不能证明实时、重开与模型历史一致。
- **流式解析器**：`utils/stream-parser/src/assistant_text.rs:20` 处理 memory
  citation 与 plan markup，没有通用公开进度帧或自动生成有意义开场的模块。
- **pending input/mailbox**：真实新输入也能续行。commentary 的 mailbox 边界
  可接收待处理消息；unknown 的保守延迟不等于将原 phase 改写为 final。
- **Goal/预算/补答**：各有独立职责。不得为播报自动创建 Goal、另造预算或
  把已有两次 answer-only 恢复用作固定阶段调度。

## 根因与证据强度

N01 已证明当前默认生成未达目标：Kimi 合并开场/正文，MiniMax 仅预告而未交付。
N02 只用于区分“提供方发了但解析丢了”与“原响应没有”：两家终态公开 Item
ID/正文 SHA 与 Native 一致，原响应各只有一条公开消息，未发 phase/end_turn，
没有工具。output_count=2 是 reasoning + message，不是两条公开消息。

最早缺口是当前提供方输出与 Runtime 消费之间的生成契约。原生正常流 fixture
通过只证明 Runtime 能消费这些事件，不能证明真实模型一定产生。不能把缺少
phase 单独说成所有续行失败的原因；同响应多消息、工具、pending input 和
Stop hook 也属于原生可继续路径。

公开 API 文档没有发现可据此开启 phase/end_turn 的明确设置；这不证明两家
永远不支持，也不能据此断言所有工具任务失败。没有获得 OpenAI 私有服务端
源码；模型阶段行为的服务端实现边界应如实保留，不能用推测伪装为 Rust 事实。

MiniMax “我按……来写……”是已有 process_only 完成保护的真实漏判。可以在
已批准最小写作预告修复范围内处理最终交付，但不能靠不断加词实现独立进展。

## 后续修正的评审边界

推荐评审限定 Provider 的显式消息阶段适配候选：每条实际模型消息自带明确
过程/结果声明，Runtime 在原生解析链规范化并复用已有 run_turn；每个真实
Message 仍只有一个公开 Item，不按段落拆分，不从推理中生成进度。简单对话
可以直接 final，长任务按真实里程碑沟通。

原始 Provider phase/正文保留，适配语义必须可追溯；未知消息不能猜写 phase。
若采用正文中的内部传输声明，需要 Runtime 在流式首字与完成态统一消费，
不能泄漏到用户界面或只依赖完成态 contributor；下一次模型输入与重开也必须
各自可证。不能伪造原生 end_turn=false。方案未定稿为已实现协议，不启用
新核心补丁、不增加测试调用，直到最小权威源设计和核心变更范围审定。

完整可阅读报告、21 处源码快照和截图证据：
`/Users/jack/.codex/visualizations/2026/11/03/01a19f3c-608f-7090-8af9-7a63c92bfbf2/public-progress-native-mechanism-20261105/`。
既有测试原证据与已纠正用量账本：工作区
`.local/diagnostics/2026-11-04-public-progress-v3/`。

当前结论为 **机制审计完成，生成目标未完成**。不得把此文、既有测试或旧 Feature
的 local_verified 状态当成本增量 M01–M14 全部通过；原 26 项受影响交互标准
与正式门禁继续逐项验证。

## 2026-11-05 批准后实施与 r2 修复状态

Owner 后续明确批准上述第 5 节限定适配候选。前文“待评审”是批准前审计时点，
不能作为当前未授权的依据。实际实现仍保持原始 Provider 记录、原生 Item 身份、
既有循环/预算/取消/权限、简单对话直接 final；没有 Host 执行循环或数据迁移。

r1 C-N01：Kimi 只给有效 final 声明和正文，无开场/中途；MiniMax 把开场、第二个
final 声明及完整答案写进一条 Item。r1 后者发生控制行泄漏、错误续采样和随后
补答。两轮均不算生成目标通过，失败记录保留，每家累计 3/24 用户轮。

r2 已修复多声明校验、流式控制行消费和保存历史的只读阅读清理；一条真实
Item 不拆分，原始文本/phase 不回填。Host 明确一次响应只写一条当前公开消息，
避免整轮脚本；不强制每任务固定三段。新 Runtime 原生回环验证混合样本一条
Item、一次请求、完整结果、unknown 阶段，正常续行和重开亦通过。

当前来源：Runtime `bab24532581249880a5c656f8f2a2ddb50d35836` → Contracts
`486bce5f653bdc67a19a6698e87ad4cca0a21105` → Host
`d0bf442f11853f9ca46248379d7094aca2d529cc` → Desktop
`9ca4e9e3cde764ed5d84fff7d9c3513cef915f9d`；Connectors 仅补充相同上游库树的
wrapper 来源 `578502e3218d85b38e5dace6fb1893478a934a95`。均仅必要本地提交，未推送。

Runtime schema 269 份不变；核心 10+7、解析 29、真实 Runtime/Host 普通回环、
Native 保存重开、前端 63、来源 5、lint/build/Clippy/文档检查通过。当前 8 会话、
11 轮，原候选前 6 会话/9 轮记录逐行摘要全保持，SQL45 不变。修复期间零付费调用。

Mac 再锁定，r1 客户端仍空闲运行；r2 沿正常退出和 canonical start-ui 激活、
历史界面验收等待解锁。新指令的真实提供方遵循、生成覆盖率及 M01–M14 全部
达标仍未完成，旧 FEAT137 两项全仓检查限制仍保留。动态状态以报告目录中的
`implementation-progress.html`、`implementation-status.json` 和验收矩阵为准。
