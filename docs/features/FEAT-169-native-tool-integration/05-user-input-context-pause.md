# 暂停交接：两组工具接入（2026-11-08）

**用户明确要求“暂停任务执行，记住状态信息”。当前暂停，不继续实现、测试、构建、验收或部署；等待用户明确恢复。**

## 请求与已确认范围

当前阶段只接入 request_user_input，以及 get_context_remaining / new_context。沿前面的原生工具审计与 FEAT-169 记录继续，不把截图当完整规格，不扩展其他工具。原生可复用的等待、答复、token 计算、上下文切换、压缩、取消必须复用；Host/Desktop 不另造执行或恢复引擎。

用户要求实现前认真源码审计与定义方案。已完成审计及普通本地 Runtime 探针，方案见 04-user-input-context-audit-and-plan.md。

**用户已选择策略 A：保留原自动压缩，仅显式 new_context 开启不摘要的新窗口；允许必要的最小原生配置适配。** 不再重复询问此策略。

交互参考：用户提供的“图 1.png / 图 2.png / 图 3.png”，位于 `/Users/jack/Downloads/Personal_Info/易界文档/11问题澄清/Codex 问题澄清/`。要求参考问题卡片、多题切换、选项、自由输入、跳过、关闭；其它场景（如敏感输入遮罩）由实现者完整设计。图片里的示例批准文本不是本任务授权。

## 原有基线保持运行

前四组工具（V2、apply_patch、exec/wait、memories）已完成前轮接入及复审。当前正式选择仍是：

- Runtime 源码 ID `dfa05c556627e781a1cd1386c17f773a7a67012feeee7525268e8889ad2473a6`；
- `.yijie/build/native-tools-v1/<ID>/aarch64-apple-darwin/`；
- `native-tools-v1/current.json` 未改变；
- 本阶段没有构建或启用新的 interaction-tools 制品；`interaction-tools-v1/current.json` 尚不存在；
- 本阶段尚未修改 Host/Contracts/Desktop 的接入实现。现有大量未提交变更属于前序任务及用户 UI/AGENTS 修改，不可覆盖/清理。

前阶段 feature.yaml 中的 usable/D4 与 19 次 Kimi 验收只对应原四组及其复审，不代表这两组已完成。

## 已核实的源码事实

1. 原生 request_user_input 默认注册，但 Default 模式不可用；开 DefaultModeRequestUserInput 可允许该模式。
2. 原生协议已有可空 options、isSecret、isOther；模型工具声明仍要求 options，归一化还会拒绝缺省/空选项。自由输入必须在正确原生入口最小补齐，不能在 Host 伪造选项。
3. 当前 canonical `ToolRequestUserInputParams.json` / `ToolRequestUserInputResponse.json` 在 schema 生成目录**根部**，不是 v2/ 子目录。experimentalApi=false 的实际探针已成功收发回调，无需开启整个 experimental API。
4. 原生 root-only；非根代理被 handler 拒绝。每轮原生 pending_user_input 用 turn/sub_id 索引。Host 必须绑定 generation/thread/turn/item/原 RPC request，防止重复、跨会话或晚到答案错投。
5. 空 answers 是未回答并继续；turn/interrupt 是中断，不能混为一谈。
6. 原生参数 autoResolutionMs 归一化到 60–240 秒；Session waiter 本身没有计时。原生 TUI 当前为 60 秒隐藏宽限 + 60 秒倒计时，交互暂停；新客户端须明确产品策略，不把 TUI 行为误当 Runtime 自动计时。
7. isSecret 是显示遮罩。合成敏感值仍进入模型输入并留在原生 rollout；不是保险库或不落盘能力。Host/UI 不额外持久化或记录答案；不能宣称端到端不存明文。
8. get_context_remaining 使用原生 context_window_token_status，可 unknown；不自行算 token，也不拿 rollout_budget 代替。
9. token_budget 原开关也使自动/手动 compaction 走不摘要的新窗口路径。策略 A 需要把普通压缩与显式 new_context 分开，但两条路径都复用原生。
10. new_context 清空活跃消息；探针显示当前任务文本及本次显式技能正文消失，静态 base instructions 保留，thread/read 历史仍含原任务。实际易界专家/技能装配仍需专项验证，不能凭静态标记承诺完整保持。
11. 原生初始上下文会尝试 notes.thread_hint；易界当前没有该 notes 服务，不能顺带接入。update_plan 本身不是可据以承诺跨窗口任务恢复的持久记忆。上游测试的新窗口快照中 update_plan 是切换后新调用的，不是旧计划自动保留。
12. 新增正常中断探针复现了原生遗留标记问题：同批调用 new_context 后等待 request_user_input，用户中断；下一轮查询 get_context_remaining 时仍可能消费旧 reset 标记，清空新一轮任务。需要在原生任务取消清理中清除待切换标记。

## 审计探针（非产品接入验收，0 供应商调用）

- `yijie-codex/.local/user-input-context-audit/probe.py`：真实固定 Runtime + 普通本地 HTTP 响应；最新 7 类 / 14 次回环请求，正常 EOF 退出。
- `.local/user-input-context-audit/native-probe.json`：Default 拒绝、Default 开启后问答、自由输入当前拒绝、敏感标记及原生保存、跳过、中断、窗口切换/历史。
- `.local/user-input-context-audit/probe_cancel_context.py` 与 `context-cancel-probe.json`：3 次本地请求复现跨轮遗留 reset 标记。
- 文档内脱敏副本：`references/user-input-context-native-probe.json`。
- 临时原生数据仍保留在探针输出打印的 temp root；没有碰日常三个 Home 或用户对话库。

## 已开始但未完成的 Runtime 草稿

新增文件（均未提交）：

- `yijie-codex/.yijie/patches/chat-models/0022-user-input-context-tools.patch`
- `yijie-codex/scripts/prepare-interaction-tools.py`
- `yijie-codex/scripts/write-interaction-tools-runtime-manifest.py`
- `yijie-codex/scripts/build-interaction-tools.sh`

编辑来源：

- `.local/interaction-tools/base/`：以当前 0021 工作源码为基线的选定文件；
- `.local/interaction-tools/edit/`：草稿编辑；
- `.local/interaction-tools/workspace/`：canonical prepare 生成，不手改；
- `codex-rs/` 固定上游源码未修改。

0022 草稿内容：

- TokenBudgetConfigToml 增加可选 reset_on_compact；resolved TokenBudgetConfig 增加 bool，默认 true 保留上游默认。易界策略 A 将配置 false（profile 尚未创建）。
- session/turn 显式 new_context 请求直接复用 compact_token_budget 原生路径；普通自动压缩仅在 reset_on_compact=true 时用窗口重置。
- tasks/compact 同样保留既有普通手动压缩行为（false 时不清空窗口）。
- tasks/mod 的 abort_all_tasks / abort_turn_if_active 清除原生待切换标记，避免跨轮遗留；新增普通取消测试。
- request_user_input 工具声明 options 改可选并增加 isSecret；归一化支持自由输入，并校验 1–3 题、唯一非空 ID、标题/问题/选项长度（选项上限 32），保持 isOther=true；新增正常自由输入/敏感标记/重复 ID 测试。
- spec_plan 不向非根代理声明本来就不能调用的 request_user_input。
- 原生 UserInputOutput 仍委托 FunctionToolOutput 产生模型/原生会话响应，仅诊断 log_preview 不输出回答值；原生会话仍按原机制保存，不承诺消除 rollout/模型上下文中的答案。
- new_context 描述明确不摘要、清空活跃消息，不作为未完成任务的普通压缩。

构建链：prepare-interaction-tools 复用现有 prepare-answer-completion；manifest wrapper 在原生 0020/0021 链后追加 0022；独立输出计划为 `.yijie/build/interaction-tools-v1/<source hash>/<target>/`，不会覆盖已验收制品。

## 最新检查结果（暂停时）

canonical prepare 已完成。执行的唯一实现阶段 Rust 检查：

`CARGO_TARGET_DIR=<codex-rs/target> cargo test --offline --locked --manifest-path .local/interaction-tools/workspace/Cargo.toml -p codex-core --lib interaction_tools_ -- --nocapture`

**编译失败，测试没有运行，不能记 PASS。** 日志 `.local/interaction-tools/unit.log`，exit code 101：

- `core/src/session/config_lock.rs:248` 的 TokenBudgetConfig 测试构造缺 reset_on_compact；
- `core/src/session/config_lock.rs:338` 的 TokenBudgetConfigToml 测试构造缺 reset_on_compact。

该 exec session 22107 已结束；没有待继续的本次编译任务。暂停后仅读取了结果和保存此交接，没有修复错误或重跑。

恢复后的第一步：把原当前 0021 的 config_lock.rs 加入 base/edit，更新上述测试构造与期望（最好验证 false 策略冻结/恢复），重新生成 0022、canonical prepare，再运行筛选测试。不要直接改 workspace 或 codex-rs。

## 后续尚未实施

1. 完成 Runtime 草稿与相关规范/配置/取消回归，构建独立候选并生成 canonical config/schema。
2. Contracts：新问答源契约、Runtime 兼容投影、Go/Rust/TS 生成与校验；API 回答形状沿原生 answers 映射，外层增加请求/轮次/操作身份与短期状态。
3. Host：独立问答回调承接，不复用审批决定；Root-only、原请求绑定、幂等、写回确认、结束/取消/断连收束；有界进程内状态，敏感答案不入额外业务存储和日志。
4. 可选倒计时：无 autoResolutionMs 无限等待；有值按已归一化时长倒计时，用户首次实际交互后暂停；超时只空 answers，不默认选择或授权。需处理提交/超时竞态和结果未知，不重投。
5. Desktop：复用既有 CommandRequest/鉴权/会话映射/HostBridge，独立问答 IPC 与 Vue 问题卡。选择/自由输入、多题导航、推荐但不预选、跳过/关闭、敏感遮罩与草稿清除、错误恢复、键盘与 IME、亮暗/最小窗口。
6. 上下文展示：复用原生 contextCompaction 事实，不把共同事件类型直接叫“已摘要”。不在客户端算剩余 token。补齐真实任务/技能/专家/文件/历史边界验证。
7. 保持 input-only、标题及审核辅助线程的原限制；既有四组工具不扩展。完整方案见 04。
8. 完成定向本地验收后才从原开发入口激活；现阶段没有新接入的成功结论。

## 约束与恢复提醒

- 用户严禁故障注入强杀、可执行文件替换/伪装、权限破坏、攻击 fixture。只用普通非破坏性测试和正常 EOF/原生取消。
- 不提交/推送/创建分支。已有用户与前序未提交改动完整保留。
- Native Rust 修改前要处理日常开发 watcher：必须正常退出 App 后再增量重启，不能让 watcher 强杀充当正常退出。当前阶段未改 Desktop Rust。
- 本阶段真实验收额度为 0；不借用上一阶段 40 次额度余额。若最终需要，模型仍仅 Kimi K3.1 Pro，先准备具体验收再申请本阶段额度。
- 用户已确认上下文策略 A，不需再问；尚未授权或实施其它新工具、语音服务、notes 服务或新的凭据/记忆平台。
- **只有用户明确恢复后才继续。**
