# 聊天删除恢复修复

用户于 2026-10-23 授权修复删除逻辑、运行中阻塞和正常重启后残留；全程非破坏性验证。
本次为 demo_fast/local 修复，不提交、推送或发布，不改权限、密钥、历史 migration 或 Runtime 源码。

contract-impact = semantic：删除准入改为核实当前原生状态，保留现有 v2 wire 和私有存储格式。
权威语义先记录于 `yijie-contracts/docs/agent-session-cleanup-recovery.md`；Host 为 producer，
Desktop 为 consumer。现有 public schema/pin 保持，本地实现不冒称已发布契约。

## 已确认原因

- Host 的 BeginCleanup 只检查持久 ActiveTurnID/State，旧 active 记录在正常重开后仍拒绝删除。
- 普通 ResumeSession 依赖用途与模型准入，不能作为所有专家/连接器会话的删除前置。
- Desktop cleanup 的领取条件和 active stream recovery 排序可能让旧 streaming/uncertain 记录
  无法到达 Host；16 次耗尽后的显式重试也需要保留原 operation，不能从头伪造结果。
- 本轮修复前用户日常聊天已清空。验证仅使用本次创建的合成记录；不恢复旧聊天。

## 实现与验收约束

复用现有删除状态机、原生状态查询/中止、Host 事务 lease、SQLCipher 级联与 checkpoint。
不通过删除数据库文件、修改历史状态为成功、恢复线程重发、强杀进程或替换 Runtime 解决产品问题。

Must AC：已完成会话删除；旧 active/starting + 原生 idle/notLoaded 清理；真正 active 正常中止后
清理；未知/仍 active 保持未完成；并发提交/专家操作不越过删除 lease；同一 operation 重试；
pending/成功 receipt 正常重开；正文/原生事实/附件/outbox/Runtime thread 均不可恢复；相关设置保留。

当前已有未提交改动归前序工作，逐文件保留。单元测试先选择安全用例，正常 Runtime 集成和 canonical
App 重开作为补充；涉及攻击资源、权限损坏、强杀、二进制替换的历史整套测试不执行，不算通过。

## 最终实现

- Host 清理与已有提交/model/expert 锁串行；核对当前原生状态，active 时读取原生当前 turn，
  正常 interrupt 后再次确认。idle/notLoaded 不冒充历史终态，只允许获取删除 lease。
- 事务比较观察时的完整映射，防止观察跨过新提交；pending expert 仍拒绝。进入 cleaning 后
  保留旧 ActiveTurnID，直到确切线程删除确认，最终事务才连同映射移除，避免第二次卡在旧字段。
- Desktop 已绑定会话的旧 queued/streaming/stopping 可交给 Host 核实；待发送/正在派发的操作
  继续阻挡。已冻结且无下一次派发时间的 start_turn 不再误判为可重发操作。
- 删除优先于旧流恢复；已进入删除流程的会话不再被普通恢复重新订阅，因此退避期间也不会
  被无限事件等待饿死。定时预约、授权和后台启动边界保持。
- 显式重试发送原 operation ID，重置有限尝试预算并保留已确认的表面。成功回执有 completedAt
  且三层 complete 后，UI 才移除选择并展示成功。中止尚未确认时展示等待/重试提示。
- 没有 migration、降级、数据库文件重置、历史终态回填或 Runtime 修改。
- 为通过当前 all-targets Clippy，将原 native_conversation_storage 的 42 行既有测试模块原样移到
  文件末尾；生产逻辑不变，没有增加 lint 豁免。

## 验证结果

日志位于工作区 `.local/chat-cleanup-20261023/`，与前一轮用户请求的数据清理证据分开命名。

| 检查 | 结果与覆盖 |
| --- | --- |
| Host 定向 race 回归 | PASS；旧 active/starting 正常重开、真实停止前保留、原生不可用、映射变更、提交锁、确切缺失、已有 cleanup/专家事务约束 |
| Host HTTP v2 producer conformance | PASS；既有请求/响应契约仍匹配 |
| Desktop `cargo test ... deletion_recovery` | 7 PASS；旧运行/不确定记录、显式重试、回执重开、附件级联、退避期间无旧流阻塞 |
| 超一页数量的合成数据 | 25 条会话通过现有 repository/队列全部清理，正常 close/reopen 后列表、正文、outbox、原生事实为空 |
| 前端删除相关回归 | 24 PASS；回执完成前不移除记录、原 operation 重试、轮询/重开状态与错误提示 |
| 固定真实 Runtime 集成 | PASS；使用既有 canonical FEAT-136 0.144.6 产物与普通本地 Responses fixture；正常完成与流式正常中止各一条，真实 thread/delete；正常 EOF 退出重启后 read/resume 均拒绝，Host 映射不存在且回执可重放 |
| 外部模型/商家调用 | 0；最终集成运行只有 2 次本地合成 Provider 请求，无付费调用、商家操作或凭据输出 |
| Host lint / Desktop ESLint + TypeScript | PASS |
| Rust fmt / all-targets Clippy `-D warnings` | PASS |
| canonical 来源检查 | PASS；通过现有 freeze/validator 更新本地源码候选，没有手改 digest 或放宽检查 |
| 元仓 lint/test/shell syntax | PASS；50 tests |

最终 App 构建与重开结果另追加于下方。日常环境已存在用户在前次清理后新建的一条对话，
本次验证保留它；不再清空日常库，不恢复此前 17 条旧会话。

## 验证边界与已知非本次失败

- 当前 ChatPage 扩展检查有一个已有展示断言失败：`does not treat an active empty reasoning Item
  as historical authority loss` 仍期望“正在思考”，而当前过程展示为“执行进度”。文件属于同期流式
  展示修改，本修复未改变该行为，也未修改断言来制造全绿；删除相关 24 项均通过。
- 初次 Vitest 文件名筛选误匹配 `.local` 历史副本，之后使用仓库标准排除目录重新执行。
  历史副本结果不能当作当前源码的验证结论。
- 整套 `make test`/历史 harness 中的攻击归档、权限破坏、进程故障与替换可执行文件项目未执行，
  原因是用户硬性安全要求；影响是本报告不提供那些故障场景或全仓全部测试的通过声明。
- 没有调用真实付费 Provider、没有删除用户新对话来做 UI 验收，没有生产发布/不可变版本固化。
  本地合成 Provider 的真实 Runtime 集成不冒称真实付费 Provider 或完整生产 D4。
- 无法取得可靠原生状态或确认停止时，必须保持未完成并可重试，不能为了“清空成功”隐瞒残留。
- 后台映射已经缺失的历史记录仍沿用既有 `local_history_deleted` 警告；它不证明 Runtime 清理，
  也不会被新的成功判定当作三层清理完成。
- 成功仍仅针对应用管理的活动会话数据，不承诺操作系统快照/第三方备份的法证抹除。

## 部署与回滚

通过原 `run-local-demo-fast.sh --packaged` 重建；仅在正常退出及进程/端口释放后构建。
正常同构建重开使用 `--packaged --reopen`。保留原 App/数据身份、设置、扩展和用户文件。
Host producer 与 Desktop 同包更新；回滚代码保持同一存储格式，旧版可能再次显示旧状态导致的
未完成，但不能重新创建已经删除的正文。未执行 commit/push/tag。

构建过程中另一个已完成的流式展示任务修改了 `src/pages/chat/ChatPage.vue`；同构建重开检查正确
拒绝了与新源码不一致的旧制品。已保留该修改并重新执行 canonical packaged 构建，未改写原回执
或跳过检查。最终活动源码的扩展前端检查仍为 238 PASS / 1 个上述无关展示失败 / 2 skipped。

最终 `final-current-app-build.log` 构建成功，`final-current-app-reopen.log` 确认
`Same-build expert reopen verified`，`/readyz` 返回 runtime ready。Native 窗口正常进入聊天页。
`final-daily-verification.json`：前次清理前的会话数 0、旧 Runtime thread 数 0；保留清理后新建
的 1 条聊天；SQLCipher integrity=ok、foreign_key_check 为空。本次修复没有清空或改写该新聊天。
