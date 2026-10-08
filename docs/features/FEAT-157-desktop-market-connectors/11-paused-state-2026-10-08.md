# FEAT-157 暂停检查点

用户于 2026-10-08 02:19（Asia/Shanghai）明确要求：“记住当前任务执行状态，暂停执行。”本记录用于下次显式恢复，不是完成或 D4 验收结论。

## 暂停边界

- 停止后续实现、生成、构建、测试及外部请求；已开始的普通命令只等待自然结束，不强杀。
- 当前标准易界应用保留运行，不再操作其界面。应用 PID 69579，worker PID 1127；这些 PID 仅为暂停时快照，下次必须重新检查，不能直接复用。
- 标准启动会话为工具 session `44029`，日志 `/tmp/feat157-app-run-20261008-daily.log`。未提交、推送或发布。
- 两轮 Kimi-K3 文本对话额度已全部使用；获准的一次 Tushare 读取因结果阶段不明，保守视为已使用。**不得因恢复任务而重置额度或自动重发。** 后续真实调用需新的明确授权。

## 已确认的真实结果

1. 既有 OAuth 操作 `62a7c0e8-1e5a-436c-a774-808baa0fe783` 完成 token 200、Keyring 保存、初始化及 254 项 tools/list；没有读取或输出原始凭据。
2. 新 daily-v1 标准应用包启动成功，readyz 200。当前实际 worker SHA：`0aacce914f889a822fcc9e3774af273d77eef03b66f1c782309b2d259c371cfa`。
3. 显式 Enable 操作 `d2ed9a82-70da-4484-86cb-b5aa7fd9d74a` 复用已有 Keyring 授权，39.322 秒完成。daily schema 摘要仍为 `ec10409543d1ae690de2b5da5893a0e69387cdd5a398f976fb04d187fc632ae1`，资格检查通过。未重新进行 OAuth/DCR。
4. 真实 UI：已安装开关 on；店铺右侧连接器入口可以选择 Tushare；输入框出现标签；管理页往返保留正文与选集。
5. 用户明确授权最多 2 轮 Kimi-K3 文本对话、1 次 `000001.SZ / 20260105` 只读查询，使用现有额度，不充值、不订阅、不自动重发。
6. 第 1 轮 02:09:26 提交，出现正确参数的实际审批；批准后返回“Connector call did not produce a verified result. No automatic retry was made.”，28 秒结束。**没有得到可信行情数据，不计业务成功。** Runtime 收到正常 MCP `isError:true`，现有安全证据不足以确认业务 HTTP 是否发出或具体失败阶段。
7. 第 2 轮 02:11:21 同会话提交，UI 点击拒绝后显示“已拒绝”，32 秒结束。但模型得到相同通用错误，无法区分拒绝与执行失败。这是已确认的错误语义缺陷。

本地会话：`01a1178e-53f2-7db2-9ed1-6f2bd58c8ec9`；实际 Runtime thread：`01a1178e-5424-7692-86f2-77e0f7af15a0`；首轮 Runtime turn：`01a1178e-544c-78b2-ba99-78a6f26069bb`。模型回答中的“已执行一次”“无数据”不作为供应商执行或空结果证据。

实际 Host Home：`/Users/jack/Library/Application Support/com.yijie.ai/demo-fast-model-candidate-v1/host`。安全供应商诊断位于其 `market-worker/library-home/diagnostics/provider/`；元数据证据位于 `market-worker/library-home/qualification/tushare/`。禁止读取 Keyring、原始 token、凭据或原始供应商响应来补造证据。

## 暂停时修复状态

- **已完成、尚未加载到当前应用**：Pending Enable 的配置说明改为“正在检查连接与支持工具，请等待本次启用结果。”。仅 `src/domain/market-connectors-ui.ts` 与对应测试；10 项目标测试、ESLint、TypeScript、diff 检查通过。
- **已完成、尚未重新装配**：Host `internal/session/market_observe.go` 将不在契约枚举内的 `result_unavailable` 改为已有 `unsupported_result`，防止已观察工具记录被严格校验丢弃。`market_submit_test.go` 增加普通不支持结果容器的回归；两项定向 race 测试已自然完成并通过（session 10357）。不推断其就是首次真实调用失败原因。
- **进行中，暂停后须先核对代理最终报告与 diff**：Contracts 先定义安全错误说明/常量，Worker 区分确定拒绝、准入未执行和已进入后端但结果不明；补有限固定枚举诊断。不得把通用 `ApprovalInvalid` 等同用户拒绝，不得放宽结果解析来假造成功。
- **进行中，暂停后须先核对代理最终报告与 diff**：Native `observe.rs` 的旧 Host nonce 使重启后的 managed 会话永久 NotReady，阻断续聊。拟修复为无 Host 时返回有作用域的 durable managed/selectionDisplay；存在当前 Host 时允许校验 owner/tenant/agent/thread/turn 后读取旧工具历史，审批与新执行仍必须当前权限，不能恢复旧 grant。source-first 方案尚在协调，不把方案当成已落地。
- 两次尝试离开重开会话被界面工具的用户操作保护拒绝，已停止 UI 操作。真实历史重开验收未通过；当前审批仅保存在 Host 内存，不能伪造重启后的审批事实。

暂停回报补充：

- Worker 代理已停止且无运行命令。仅 `worker/src/tushare_oauth.rs`、`worker/src/daily.rs` 增加了业务诊断中间代码；Gateway 拒绝/未知分流、新 execute 参数/PermitSlot 调用方与测试适配均未完成，**当前 Worker 源码尚未编译，不能直接打包**。上一完整产物仍为 `0aacce…71cfa`，运行中应用未动。Connectors 两份验证文档只更新到 fresh Probe，通过主检查点补充后续额度事实。
- Desktop 代理已停止且无运行命令。Native `observe.rs` 尚未修改，未启动新测试；允许旧 turn 只读 tools 的最终方案仍需与 Contracts 确认。已经完成的纯文案补丁保持原状。
- Contracts 代理已收到暂停指令，随后中断其仍活动的代理回合，以停止继续工作；未强杀任何系统进程。最终源契约/生成物同步状态尚未收到完整回报，恢复时必须先检查 diff 与同源校验，不能假定该阶段已经完成。

## 恢复后的顺序

1. 先读本检查点、`10-product-execution-and-tushare.md` 和三位代理最终暂停报告，检查所有仓的 dirty 状态，确认哪些生成/源码/测试尚未完成。
2. 完成 source-first 错误语义、Worker 安全阶段诊断、Native 历史观察与续聊恢复，做正常非破坏性本地验证；不改固定 Codex Runtime。
3. 源码一致性检查通过后重新 canonical freeze。使用应用自身正常退出流程；无法安全退出时停止该步骤并报告，禁止强杀。
4. 通过原 canonical `tauri:demo-fast:app` 重建加载补丁，核对已保存授权的恢复、历史与 UI。不得覆盖来源不明/已签名/非本项目的二进制。
5. 把修复后的具体真实查询验收准备好，再请求新的限量调用授权。既有 2 轮/1 次额度已耗尽；目前 D4 与真实金融查询 happy path 仍未完成。

固定 Runtime SHA 保持 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，Codex 仓保持干净。用户原有三个店铺文件 diff SHA 保持 `50ca7a1165be0732b4e74d119340303c39529e5bd40b9845bed0c02d672b4eeb`；恢复时重新核对，不覆盖。
