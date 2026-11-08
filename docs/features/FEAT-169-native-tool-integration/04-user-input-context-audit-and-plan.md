# request_user_input 与上下文工具：源码审计及实现方案草案

状态：源码审计完成，上下文策略 A 已由用户确认；用户已于 2026-11-08 明确恢复，接入、定向验证及原入口加载已完成，结果见 [06 执行与验证记录](06-user-input-context-execution.md)。历史暂停入口见 [05 暂停交接](05-user-input-context-pause.md)。沿前面的原生工具审计继续，截图只作为结论线索及 UI 参考。当前范围严格限定为 request_user_input，以及 get_context_remaining / new_context；前面四组工具保持，不顺带接入其它工具。

## 一、审计依据

固定 upstream rust-v0.144.6；当前已激活的 0020 + 0021 本地 Runtime 源码 ID 为 dfa05c556627e781a1cd1386c17f773a7a67012feeee7525268e8889ad2473a6。核对源码、该制品生成的 canonical schema、Host 分发、Desktop 原生鉴权/Bridge 及现有状态展示。

此外通过同一真实 Runtime、普通合成输入和本地 HTTP 响应，运行了七类能力探针，共 14 次回环请求、0 次供应商调用。完整摘要见 [原生探针](references/user-input-context-native-probe.json)。它证明原生能力与行为，不是尚未实现的易界交互验收。

## 二、源码事实及接入缺口

| 项目 | 已核实事实 | 影响 |
|---|---|---|
| Default 模式 | 原生会声明 request_user_input，但默认只允许 Plan；探针确实返回 unavailable in Default mode | 配置必须允许 Default，不能只做一个 UI |
| 自由输入 | Protocol 的 options 可缺省，但现工具 schema 要求 options，normalize 又拒绝空选项；自由输入探针实际被拒绝 | 要在原生声明/参数归一化处做最小补齐，不在 Host 假造选项 |
| 敏感输入 | Protocol 已有 isSecret，现工具 schema 没有完整开放；原生 TUI 遮罩输入与历史显示 | 工具声明需与已有协议能力对齐，客户端使用原标记 |
| 敏感数据去向 | 合成 isSecret 回答仍进入模型输入，也存在于原生 rollout；本探针 stderr 无该合成值 | 遮罩不是加密、不落盘或凭据保险库承诺；不能另造一套凭据管理能力 |
| 原生等待 | Session 内已有 oneshot waiter、回调和取消；非根代理调用被原生拒绝 | Host 承接反向请求，保留原线程/轮次/调用/请求身份，不另造执行调度 |
| 反向协议 | item/tool/requestUserInput 在当前 stable schema 中已存在，params/response schema 位于生成目录根部；experimentalApi=false 的探针成功收到并回复回调 | 不因为源码注释写 EXPERIMENTAL 就打开所有 experimental API |
| 超时 | 原生工具参数支持 60–240 秒范围，归一化负责夹限；Session 不自行倒计时。TUI 当前使用固定 60 秒宽限 + 60 秒倒计时，并在用户交互后暂停 | 新客户端必须明确自己的可选超时策略，不能误称 Runtime 已自动处理 |
| 跳过与取消 | 空 answers 得到原生空答复并继续；turn/interrupt 得到 interrupted，语义不同 | 跳过不能变成“同意”，关闭问题不能冒充停止任务 |
| 剩余上下文 | get_context_remaining 直接使用原生 context_window_token_status，可返回未知 | 不另算 token，不用 rollout_budget 替代，未知不显示成 0 |
| 新窗口 | new_context 请求原生新窗口；token_budget compaction 分支跳过模型摘要，重建 initial context | 不包装为普通压缩，也不在 Host 生成摘要 |
| 开关副作用 | 原生 token_budget 同时影响自动触阈值及手动 compaction，不仅注册两个工具 | 必须先确定产品上下文策略 |
| 任务/技能/专家/历史 | 探针中原任务文本和显式技能正文在新窗口后消失，静态 base instructions 仍在；thread/read 仍读到原用户文本及 contextCompaction 记录 | 历史可读不等于模型仍记得。实际专家/技能资产还须经过易界装配验证 |
| 任务恢复依赖 | 初始上下文会尝试 notes.thread_hint；当前接入未配置该 notes 服务。原生 update_plan 发 PlanUpdate 事件，并不能直接据此承诺跨窗口保留任务 | 不补造 notes 服务、任务记忆库或自动复活机制；不误读上游测试中“新窗口后新调用的 update_plan”为旧计划自动保留 |

关键源码：

- yijie-codex/codex-rs/protocol/src/request_user_input.rs
- yijie-codex/codex-rs/core/src/tools/handlers/request_user_input.rs、request_user_input_spec.rs
- yijie-codex/codex-rs/core/src/session/mod.rs：request_user_input、notify_user_input_response、start_new_context_window、build_initial_context
- yijie-codex/codex-rs/app-server/src/bespoke_event_handling.rs：on_request_user_input_response
- yijie-codex/codex-rs/tui/src/bottom_pane/request_user_input/mod.rs、render.rs；history_cell/request_user_input.rs
- yijie-codex/codex-rs/core/src/tools/handlers/get_context_remaining.rs、new_context_window.rs
- yijie-codex/codex-rs/core/src/compact_token_budget.rs、session/turn.rs、tasks/compact.rs
- yijie-codex/codex-rs/core/tests/suite/token_budget.rs：new_context_tool_starts_new_window_before_follow_up
- yijie-agent-host/internal/codex/session_protocol.go、protocol.go
- yijie-desktop/src-tauri/src/chat/ipc.rs、application.rs、host_bridge.rs

## 三、推荐实现边界

### 1. Runtime

复用 RequestUserInputHandler / Session 原等待通道 / 原生响应协议。仅补齐现有 options 可选和 isSecret 能力在工具声明、归一化中的缺口；补边界校验（1–3 题、唯一问题 ID、合理长度），无效参数直接由原生工具报错，不送一张不能回答的卡片。

只允许根线程提问；Default 开启、Plan 保持原有支持。沿用 request_user_input 的 DirectModelOnly 约束，避免放进 Code Mode 后形成嵌套等待；input-only、标题、审核辅助执行面不获得提问能力。

上下文工具直接使用既有 handlers、token 计算及原生窗口切换。不得在 Host/Desktop 另算预算、重写窗口、总结历史或重建任务。

### 2. Contracts / Host

canonical Runtime schema 先行，再生成公共问答契约与 Go / Rust / TypeScript 消费类型。新增独立问答接口，不修改“批准/拒绝”接口为问答接口。

Host 仅保留当前进程的有界待答回调及短期提交回执。每项绑定 Runtime generation、threadId、turnId、itemId、原 JSON-RPC requestId、对外不透明 request ID。通过现有会话映射和身份校验定位；只回复原请求。问题 ID/回答范围必须与原问题一致，终态后拒绝晚到回答。

提交采用操作 ID 与内容指纹去重；写回原生通道成功后才返回“已发送”。断连后不自动换轮次重投。取消、turn 完成、serverRequest/resolved、Runtime 退出分别收束等待，不伪造答案。回答不写入 Host 业务库、SSE 普通消息或诊断日志。

原生 Runtime 会话持久化按既有机制处理。isSecret 不作为平台 token/密码配置入口；此类配置仍走已有安全连接器流程。界面必须说明回答会提供给模型，不能宣称密文传输之外的“不落盘”保证。

### 3. Desktop / UI

复用已有 Rust command 请求信封、鉴权、会话映射和 HostBridge，增加明确问答读/答/交互通知入口。Vue 只负责展示和输入；业务校验与 I/O 留在对应层。

参考图的主体布局：聊天输入框上方显示独立问题卡片，头部问题标题、多题页码、前后切换、关闭；正文显示原问题；选项按编号排列，同时允许自由输入；底部跳过、下一步、最后发送。推荐项只做标记，不预选、不自动提交。

- 无选项：直接显示自由输入区。
- 多题：本地保存本组未发送草稿，前后切换不丢输入；最终一次回复原生请求。
- 敏感输入：默认遮罩、显式显隐；不写 localStorage、聊天草稿持久层、错误日志。提交/取消/切换会话后清除敏感草稿；回执只显示已填写，不回显答案。
- 跳过：该题空答复；关闭：明确“关闭并跳过本组”，未发送草稿不冒充已提交。停止整个任务仍调用原生 turn/interrupt。
- 网络或提交失败：保留待确认状态，先查回执，不静默重放答案。
- 未绑定 Runtime 的新会话返回无待答，不为查询自动创建线程。
- 不把截图里的语音图标当作已存在能力；当前若没有可复用语音链路，本次不新增语音服务。
- 保持键盘操作、IME、亮/暗主题、1180×760 最小窗口；长问题内部滚动，操作区保持可见。

### 4. 可选超时策略

无 autoResolutionMs 时一直等待，直到明确答复或原生取消。提供该参数时，以原生归一化后的时长显示可选倒计时；用户首次实际交互后暂停。超时只返回原生空 answers，不选择推荐项，不授权任何操作。敏感输入不自动提交。

倒计时/暂停由客户端适配层统一协调，保证页面切换、刷新和并发窗口不会产生两份回答；它不替代 Runtime 的等待与取消。正常停止任务后，已结束的问题不能复活。

## 四、已确认的上下文策略

建议 A：保留原有自动摘要压缩，只让显式 new_context 走原生新窗口路径。需要最小 Runtime 配置/分流适配；两条处理路径都复用原生实现，不新建压缩器。用户已明确选择此项。

可选 B：完整使用原生 token_budget，明确接受显式 new_context、自动触阈值和该模式下的 compaction 都开启不摘要的新窗口。

无论哪种，都不能承诺新窗口自动保留任务原文、已读取技能正文或过去工具结果；不顺带启用 notes 服务，不在 Host 造恢复数据。模型使用指导必须把 new_context 与普通压缩区分，不能用它无准备地延续依赖旧消息的任务。保留哪些原生配置、权限、技能目录/使用说明、专家 base instructions，以及哪些内容必须重新读取，全部以验证结果为准。

UI 对原生 contextCompaction 事件采用不会误导的上下文处理状态；不能仅凭这个共同事件类型断言已摘要。历史保存、窗口切换成功和当前模型可见内容分别验证。

## 五、验收门槛

1. 原生 Default 模式问答真实反向请求；选择、自由输入、多题、遮罩、跳过、关闭、取消、可选超时与交互暂停。
2. 回答严格回到原请求；重复提交不重复写回；已结束/旧进程请求不能回答；切换会话不会错投。
3. 普通合成敏感值不出现在 Host/UI 持久层、错误或诊断日志；原生会话保留事实如实记录，不把遮罩当加密。
4. get_context_remaining 的数值或 unknown 来自原生；与 rollout_budget 明确区分。
5. new_context 确实产生新窗口且不调用摘要；按照所选策略验证自动阈值路径；原聊天历史仍可读、文件状态保持。
6. 用真正的易界技能/专家装配验证重建内容，不能用单一标记存在代替技能正文、任务或权限完整性。
7. 检查此前四组工具、审核辅助线程、input-only 仍保持既定边界；只做相关定向测试。
8. 原有开发入口正常退出/重开后核验就绪和 UI，不强杀、不造攻击 fixture、不改权限制造故障。

本阶段真实供应商验收额度为 0，不挪用前一阶段余额。若实施后确需真实验收，另按本阶段具体用例申请额度，模型仍仅 Kimi K3.1 Pro。

本方案先完成源码和实际 Runtime 探针审计，再由用户确认上下文策略。按“原生候选→源契约/生成物→Host→Desktop→定向验收”顺序实施。

## 恢复执行与契约影响（2026-11-08）

用户已恢复执行。最高 `contract-impact = breaking`：0022 补齐原生自由输入/遮罩并收紧问题合法性边界，新增配对问答消费者，旧客户端不具备回调承接能力。通过独立 interaction-tools 候选和默认关闭的精确配对开关扩展；不替换旧 native-tools 投影，旧会话仍经原生 resume/历史读回。Runtime schema 先行，Contracts 源及生成检查后才接 Host/Desktop。当前本地候选 fallback 为 Contracts `c24d73fde83a01b5dd2a9ded8defb5bbef34e311`，旧支持窗口保留；无 commit/tag/发布授权。Owner 为段成威，Runtime/Host 为 producer，Desktop 为问答 consumer。回退须先正常结束活动问答、退出 App，再回到原四组配对版本；不得把未答请求恢复成新请求或自动重放。
