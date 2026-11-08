# 原生问答与上下文工具：实现质量复审

2026-11-08。用户要求复审 request_user_input、get_context_remaining/new_context 的真实落地质量。

**结论：原生能力接入和主流程有效；问答适配仍有4项P2问题，不能认定异常恢复与权限边界已经完整。** 本轮为只读审计，`contract-impact = none`：没有修改产品代码、契约语义、配置或运行中的应用。仅新增 ignored `.local` 审计用例/日志与本报告；未提交、推送、重启或调用付费模型。

## 审计对象与基线

- 审计当前工作树，包含后续上下文用量/整理状态展示；不重做其它工具的接入。
- 当前实际 Runtime 为 `tool-search-v1/fac52ad79cc7e0a379fc597a7ecfcee573205d38a60c9d0ed3a2e96871ab0f45/aarch64-apple-darwin`，继承本需求0022补丁。没有用旧候选的通过结论替代当前版本检查。
- 当前 readyz=200，真实进程参数包含 `features.default_mode_request_user_input=true`、`features.token_budget.enabled=true`、`features.token_budget.reset_on_compact=false`、`tools.experimental_request_user_input.enabled=true`。
- 当前配对构建来源检查通过；源文件摘要和复现结果见 `references/user-input-context-reaudit.json`。

## 确认的问题

### RUI-01 / P2：只读权限可以暂停问答超时

位置：Desktop `src-tauri/src/chat/application.rs:5790`、`ipc.rs:10500`；Host `internal/codex/user_input.go:271`。

`user_input_request` 只有 action=answer 使用 SubmitTurn，其余动作均按 ReadSessions 鉴权。touch 经公开Tauri command进入该分支，再POST到Host，将pending请求的timeout_paused设为true、清除deadline并停止timer。ReadSessions只需task.read，SubmitTurn需要task.read+task.create；数据库查询只验证owner/tenant，未补充写权限。因此拥有同一资源只读权限的上下文，可以改变模型等待期限。

影响限于问答等待状态，未发现它能直接授予命令或MCP执行权限。正常UI的disabled不是Native权限边界。

建议：read保留ReadSessions；touch与answer使用既有提交/交互权限，并增加只读权限不能发出touch POST的定向验证。无需新增审批体系或执行权限。

证据类型：完整源码权限调用链确认；没有在用户当前应用里实施越权操作。

### RUI-02 / P2：回执过期后，旧问题会卡在无法恢复的重试状态

位置：Host `internal/codex/user_input.go:65`；Desktop `src/composables/useUserInput.ts:45`、`src/api/user-input-client.ts:18`、`src-tauri/src/chat/host_bridge.rs:2085`、`application.rs:3368`。

Host会在10分钟后或容量清理时移除终态回执。如果客户端错过终态，下一次snapshot已经没有该待答请求，但客户端仍拿旧request_id查询。404被通用Bridge错误解析、application映射和前端catch折叠成不可区分的服务错误，current仍保留pending，connected=false。后续“重新读取”重复同样的404，发送/跳过/关闭按钮都被禁用；只能依靠切换聊天或重开界面清掉本地状态。

建议：贯通现有问答契约的not_found/conflict/unavailable，区分确定不存在与临时连接故障；在权威snapshot无此待答项、原回执明确不存在时移除旧表单并保留“无法确认历史结果”的说明，不能重发答案或虚构answered/cancelled。

证据类型：普通缺失回执用例已复现；连续refresh后仍为pending。

### RUI-03 / P2：迟到响应可以回退已完成的问答状态

位置：Desktop `src/composables/useUserInput.ts:67`、`:55`。

用户第一次编辑触发touch，同时很快发送回答。answer先返回answered时，迟到的touch只检查会话epoch和request_id，没有检查mutation版本或终态，能够把answered覆盖成旧pending，重新显示问题并清掉成功提示。另一个已复现路径是旧poll失败在成功答复后才到达，catch没有验证mutation，覆盖成功后的连接/错误状态。

建议：所有异步成功和失败路径统一检查请求代次；旧touch/poll不能回退已知终态；保留原请求ID和操作ID，不通过重发来恢复。

证据类型：两项合法响应乱序用例均失败，分别观测到answered→pending和成功后出现旧同步错误。

### RUI-04 / P2：轮次结束与提交准入之间存在竞态

位置：Host `internal/codex/runtime.go:926`、`runtime_permissions.go:467`、`user_input.go:289`、`:382`。

通知处理先更新activeTurns，再调用独立的问答收尾。两个锁边界之间，HTTP提交可以看到仍为pending的问答项；AnswerUserInput没有重新核对当前活动轮次，于是将其置为submitting。随后收尾又跳过submitting，原生通道写回成功后回执成为answered，即使Host已经知道原轮次结束。

原生RPC ID仍绑定旧请求，未复现答案投递到其它线程/新轮次。问题是结束后的提交准入与回执状态不准确；写入stdin也不等于模型实际采用了答案。

建议：让轮次/请求终结与提交准入按一致锁顺序形成原子边界；保留正常提交后的serverRequest/resolved与写回确认竞态处理，但不能把尚未获准的晚到提交提升为已提交。

证据类型：使用完整合法turn/completed通知及生产处理函数的确定性交错，实际得到`closed native turn accepted an answer, receipt state=answered`。这是内存状态机并发复现，不是对运行应用抢时序、强杀或故障注入。

## 复现与回归结果

| 检查 | 本轮结果 | 说明 |
|---|---|---|
| 新增前端边界用例 | 3 FAIL | RUI-02一项、RUI-03两项；使用生产composable和普通响应/错误 |
| 新增Host轮次结束交错用例 | 1 FAIL | RUI-04；生产处理函数、普通合法事件，无进程操作 |
| 当前Runtime的问答/旧会话/上下文/专家技能与input-only | 4 PASS | 实际固定fac52…Runtime与普通本地provider；测试专用source overlay仅令配置匹配当前ToolSearchEnabled，未替换产品逻辑或Runtime可执行文件 |
| 原Host问答状态机与HTTP | 5个顶层用例 PASS | 含原3个暂停/超时/跳过子场景；race启用 |
| 前端问答与关联上下文展示 | 19 PASS | 7个相关测试文件；类型检查通过 |
| Native上下文策略 | 3 PASS | 自动摘要、普通手动摘要、显式无摘要窗口 |
| Native剩余上下文 | 4 PASS | 数值、unknown、prefix、Code Mode结构化结果 |
| 新问答契约 | 4 PASS | 同源/语义样本；生成、消费者同步和配对来源检查通过 |
| 真实供应商调用 | 0 | 未借用前阶段剩余额度，未调用Kimi或MiniMax |

复现命令：

- Desktop：`pnpm exec vitest run --config .local/user-input-audit/vitest.config.mjs`。
- Host：固定Go工具链、offline模式，`go test -race -timeout 0 -overlay <repo>/.local/user-input-audit/overlay.json ./internal/codex -run '^TestAuditUserInputAfterNativeTurnClosed$' -v`。
- 原有用例在相同产品源码下仍通过，说明通过清单没有覆盖上述边界，不能由主流程通过推导为无缺陷。

## 确认正确的部分

- request_user_input执行仍委托原生handler/Session等待与响应；Host保存原RPC的临时适配状态，没有另建Agent执行引擎。
- 原生问题/答案协议是权威，公共类型和校验由同源生成；问答与审批接口分离，回答不是权限批准。
- 敏感输入有遮罩与本地清理；原生rollout仍保留模型输入的事实已说明，没有宣称加密保险库或不落盘。
- get_context_remaining继续调用原生tokens_until_compaction；unknown没有被替换成0，也没有借rollout_budget计算。
- new_context与普通压缩正确分流，均复用原生；原会话历史与工作区文件不因开新上下文而删除。当前任务消息及已展开技能正文不保证留在新上下文，实际专家base指令/索引保留的边界有回环证据。
- 后续上下文圆环使用原生最近一次usage与同一事件的有效容量；“上下文已更新”中性文案未冒充摘要成功。只读历史恢复不是新的token计数器。

## 质量判断与未执行项

主功能已落地，来源、配置与正常调用链可信；剩余问题集中在问答的异常恢复、并发收尾及一个只读权限入口。建议先修RUI-01/RUI-02，再统一收束RUI-03/RUI-04，并把复现用例纳入正式回归。

未进行新的付费模型验收、完整原生GUI问答操作、全量回归或用户禁止的测试。当前start-ui已具备后续文档中的实际App绑定证据，不能沿用“永远无法绑定”的解释；修复后应补一次实际窗口内的问答与取消闭环。此前Kimi4/8次是历史验收，不计入本次新通过结果。

本轮没有修改或重启运行中的易界，没有覆盖其他会话/仓库的未提交工作。
