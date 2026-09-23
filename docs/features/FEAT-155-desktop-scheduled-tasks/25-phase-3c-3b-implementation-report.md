# FEAT-155 · 3C-3B1 与 3C-3B2 实施报告

2026-09-19。按用户本轮明确授权，连续完成 B1 与 B2 的候选代码、零真实调用组合验证及技术自审，随后停止。执行定义见[24](24-phase-3c-3b-execution-definition.md)。**普通 Desktop 仍 SQL15，普通 Host 仍 Store5；显式候选为 SQL22 / Store6。没有页面、真实激活或日常库迁移。**

本批完成的是候选工程闭环，**真实草案发送仍不可用**：固定 Runtime 的有效命名权限回执是 experimental 字段，stable 链尚不能证明完整策略生效。实际 Manager 明确返回未具备资格并在 Runtime/模型 I/O 前拒绝；没有新增开关绕过该条件。Provider 对固定 outputSchema 的支持、真实平台及 D4 仍 NOT RUN。

## 1. 实现结果

| 步骤 | 已实现行为 |
|---|---|
| B1：共享执行契约 | Contracts 新增固定用途草案的 create/resume/turn/capability 四入口；闭合版本、文本、opaque workspace、operation 与错误，生成 Go/Rust/TS、固定模型 schema、严格校验源和摘要锁。沿原 plan-draft clarification/candidate，不透传任意 schema/config/path/scope |
| B1：Host Store6 | 显式原生 writer 前向迁移；旧记录回填 ordinary，用途/schema/policy/workspace 在 reserve 前登记并保持不可变。普通 reader 读6不降版，不获得草案创建权；未知用途拒绝。普通 resume、v1/v2/permission turn、审批批准和标题生成不能放宽草案用途 |
| B1：固定适配与目录 | 同一 Manager 的 stable start/resume config 和 turn outputSchema；不使用 legacy sandbox 覆盖命名策略。原生受管根可按 opaque ID 只读解析已有 canonical 空目录，start/resume/turn 重验；普通启动没有候选根/writer。实际有效配置资格不明时拒绝，没有第二 Runtime/Provider/队列 |
| B2：SQL22 与提交 | 新增来源、受限会话与确认收据表及删除墓碑；旧1—21迁移不改。文本仍在原聊天，create/turn 仍在原 outbox；首次新建独立受限会话，澄清沿同一受限会话继续。原 Coordinator 检查当前 native 权限、用途和 Host 能力，固定草案接口投递；持久 attempted 标记阻止租期到期或重开重发 |
| B2：可信来源 | scoped source→本地 conversation/turn/operation→native thread/turn 精确关联，只接受完整 final_answer item 与对应 completed 通知。整体展示 partial 可以通过；未完成/失败/中断/多 final/未知格式/缺事实/仅冷历史均不据此推导候选。整段封闭 JSON 解析，拒绝代码围栏和拼接；时间与非空内容继续 native 校验 |
| B2：唯一确认 | 用户确认定义和真实目标 ID 在 native 重验；来源摘要、定义摘要、source→plan、原 save request 与确认收据同事务。换 request ID、重复确认和正常重开均不多建计划；冲突拒绝。未确认源删除即失效，已确认保留幂等墓碑；只保存 paused，无 grant、启用或 run |
| B2：最小 IPC | 新增 submit/preview/confirm 三命令，总数18。复用当前 UI context、native capability/revision、提交期限和 typed client；普通聊天、权限切换与 scheduled existing target 不能把草案会话当普通执行目标 |

关键文件：Contracts `jsonschema/scheduled-tasks/draft-execution-v1.schema.json`、`scripts/generate-scheduled-draft.mjs`；Host `internal/session/scheduled_draft.go`、`internal/codex/scheduled_draft.go`、`internal/app/scheduled_draft.go`；Desktop `0022_scheduled_draft_sources.sql`、`schedules/drafts.rs`、`host_bridge/scheduled_draft.rs`、原 application/worker 及 IPC 源。

未知回执保持未决且不再次 POST。既有 Host mapping/operation 只读查询继续提供恢复证据；本批不把“缺少回执”写成失败终态、成功候选或已经恢复。没有增加独立草案恢复状态机。实际启动中的完整恢复体验仍随入口激活进行真实验证。

## 2. 本轮验证与证据

全部数据是普通临时 SQLCipher/bbolt 或进程内声明式 HTTP/Runtime 接口 fixture。没有启动真实 App、Host、Runtime 或 Provider 进程，没有访问日常数据库或 Keychain。没有强杀、权限故障、攻击 fixture、替换可执行文件或伪造验收；开发编译由项目标准工具完成。

| 检查 | 本轮结果 |
|---|---|
| Rust FEAT-155 专项 | [全专项](evidence/phase-3c-3b/native-suite.log)92/92 PASS；随后增加澄清 follow-up 并收紧 preview 分型，[最终 B1/B2 组合](evidence/phase-3c-3b/native-final.log)7/7 PASS，覆盖最终代码。没有把前序报告数字当作本轮结果 |
| 旧 Desktop 回归 | [19项明细](evidence/phase-3c-3b/regressions.json)PASS：旧迁移/重开、原 outbox、普通聊天、原生历史、正常退出和授权 |
| Host | [定向 race](evidence/phase-3c-3b/host-race.log)包含6项本批测试及4项既有 recovery 测试，全部PASS；[5项普通行为回归](evidence/phase-3c-3b/host-regressions.log)及 scoped go vet PASS |
| 跨仓实际 producer | [Host/Desktop 11份实际值](evidence/phase-3c-3b/wire-conformance.log)通过 canonical 严格检查；[20份 IPC 实际交换](evidence/phase-3c-3b/combined-ipc-producer.json)覆盖全部18命令，Rust/AJV/生成TS检查及既有11份校验对照PASS；原 plan/execution/preparation producer 检查PASS |
| Contracts | 新执行、既有草案和引用闭合测试14/14 PASS；25份 JSON Schema 严格校验、固定 OpenAPI canonical 引用 lint、定向生成/同步、TS编译和生成Go vet PASS；四个登记基线的 breaking 检查均PASS |
| Desktop 工程 | 最终 fmt/clippy（all-targets，warnings=error）、lint/build（有chunk体积提示）、typed client 7/7、定向原生生成/一致性检查PASS |
| 总生成入口 | [真实失败日志](evidence/phase-3c-3b/aggregate-generation.log)：`pnpm generate:check` 在旧 public API 生成器被 `contracts checkout has tracked changes` 保护拒绝。未清理已有改动、未关闭保护。上述本批 leaf 检查另行通过；总入口不标PASS |

四基线：fallback `db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。新草案 family 在这些基线中不存在；自动兼容检查不证明私有数据库可降级、真实权限或 Provider 资格。当前 source lock 为本地候选摘要，不是已发布 tag/pin 或独立 Consumer Owner 批准。

## 3. 发现、修正与结构化自审

- 有效权限证据：查到 activePermissionProfile 属于 experimental，保留实际 Manager 拒发；不把普通 readOnly、prompt 或禁用工具名当作完整隔离证明。继承 MCP/skills、fallback、辅助读根及 Provider 仍需真实资格。
- 兼容恢复：收尾发现普通兼容 reader 不应尝试草案 resume 并阻塞旧聊天，已限定为显式 native candidate authority；无该授权时只保留历史。候选失去 Host 资格时也不影响普通聊天恢复，已定向复验。旧 FEAT-126 私有 Store profile 与新 draft writer 明确互斥。
- 用途与存储：逐入口复核 ordinary/draft、Store5→6 回填与 reader、SQL15/21→22、普通 outbox 筛选及最终发送 guard；旧迁移和固定 Runtime 保持。目录只读解析并重验空目录；未引入用户书签伪造或新执行器。
- 来源与事务：逐项核对 native binding、final/terminal、unknown format、partial view、删除墓碑、确认期限、定义冲突及原 request/source 同事务；preview status 必须和 output 分型一致，已在私有源补齐并复验。
- 生成器：实际 ESM producer 校验暴露 AJV `equal` 运行时 require 未映射；已修生成器的 ESM 依赖并增加未知 runtime require 拒绝，再重新生成和严格复验。未手改产物、未关闭 strict。
- 初轮合成检查修正了 canonical 临时目录引用、clarification 的合法 missing_fields 和测试辅助类型；新增接口 unauthorized 与闭合共享错误对齐。失败与修复未被当作产品真实平台资格。
- 本轮由主代理执行源码自审，没有新增子代理；自审不是独立人工评审。只运行已核对的非破坏性测试集合，没有运行包含禁止行为的历史全量套件。

元仓 strict、D0、audit-claims、lint、50/50治理测试实际PASS；218处本地链接、Shell语法及五仓diff检查PASS。165份业务候选摘要已记录；旧21份migration及Runtime起点5296份文件逐字节保持。D0仍是既有范围设计批准，不代表D4。

## 4. 边界、回退与停止

本批整体 contract-impact=breaking。先共享源/生成，再 Host/Desktop compatible reader，再显式候选 writer；真实 producer 激活须等待有效策略和 Provider 资格。停止候选 producer 后仍保留能读 Store6/SQL22 的 reader，不回写5/15，不删除用途字段，不拿旧二进制打开候选库。所有原有工作区改动保留；无提交、推送、tag、发布或 Runtime 修改。来源清单见[本批摘要](evidence/phase-3c-3b-source-20260919.json)。

本轮文本、图片、商家真实调用均0；文本累计仍0/12。原 PDF 的三种运行目标、单机调度、审批及原生生命周期边界保持；本轮未扩展页面、自动真实激活、防睡眠/唤醒或系统通知。系统通知延期，唤醒仍为原需求后续范围。Must 全量产品验收与D4继续pending/NOT RUN。

**3C-3B1 与 3C-3B2 候选实现完成后停止，不自动进入第四阶段、页面或真实调用。**

后续方案：用户随后要求下一步计划，已只读复核并保存[26](26-phase-3c-3b-3a-qualification-plan.md)。该计划补清 activePermissionProfile 仅是标识、空MCP map的继承语义及后续原生装配差距，不改写本报告的既有检查结果或把候选证据升级为真实资格。
