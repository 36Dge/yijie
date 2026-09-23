# FEAT-155 第三阶段执行方案：受管执行闭环

2026-09-18最新下一步：建议只实施[23：3C-3B1受限草案执行前提、共享契约与Host用途隔离](23-phase-3c-3b-1-implementation-plan.md)。本轮只读调查与保存方案，未开始实现；推荐Host普通Store5/显式候选6，Desktop普通15/候选21保持，来源唯一确认和候选SQL22留B2，页面和真实激活仍为后续。0/12与Must pending/D4 NOT RUN保持，下方此前状态保留阶段历史含义。

2026-09-18当前交付：用户授权的3C-3A原生管理查询、确认边界与最小typed IPC已完成并停止，见[22实施报告](22-phase-3c-3a-implementation-report.md)。普通schema15/默认禁发、候选21保持，无SQL22；草案3C-3B、页面及真实激活未开始，文本0/12、Must pending、D4 NOT RUN。下方此前“当前/下一步”均为阶段历史。

2026-09-18最新下一步：建议只实施[21：3C-3A原生管理查询、确认边界与最小typed IPC](21-phase-3c-3a-implementation-plan.md)，先补原生在途删除保护和页面共用查询/确认接口，草案受限生成另列3C-3B。本轮只读调查和保存方案，未实施；普通15/默认禁发、真实平台NOT RUN与0/12保持。下方此前“当前/下一步”保留阶段历史含义。

2026-09-18最新交付：用户授权的3C-2候选实现、零真实调用组合检查和技术自审已完成，见[20实施报告](20-phase-3c-2-implementation-report.md)。报告后停止，未进入3C-3/页面或真实激活；普通schema15/默认禁发、Must pending、D4 NOT RUN和文本0/12保持。以下此前“当前/下一步”均保留阶段历史含义。

2026-09-18最新规划：3C-1已完成并停止，下一批按[19](19-phase-3c-2-implementation-plan.md)仅实施自动触发与独立重跑候选；显式启用与grant同事务、连续性/槽时效、unknown未来停用是必要前提。完成后报告停止，草案/UI及真实激活留后续。本轮仅方案，普通15/默认禁发与零真实调用保持；下方旧阶段表述保留历史含义。

2026-09-18最新交付：用户授权17的3C-1已完成候选实现和安全定向检查并停止，见[18](18-phase-3c-1-implementation-report.md)。普通15/默认禁发和真实平台NOT RUN保持，未进入3C-2；下方旧阶段表述保留历史含义。

2026-09-18最新状态：3B-2源码与安全定向检查已完成并停止，见[16](16-phase-3b-2-implementation-report.md)。下一次建议仅实施[17：3C-1受控手动投递接线](17-phase-3c-1-implementation-plan.md)，先闭合现有manual producer，再接自动/重跑、草案及页面；完成后报告停止。本轮只保存方案，3C未实施。真实平台/Provider资格仍NOT RUN，普通15及定时双层默认禁发保持；下方旧状态和早期分批顺序保留历史含义，以17及feature.yaml为当前权威。

2026-09-18当前状态：3B-1已完成并停止，见[14](14-phase-3b-1-implementation-report.md)。下一批按[15](15-phase-3b-2-implementation-plan.md)实施3B-2只读恢复、审批观察、有证据的占用释放和原生生命周期，继续双层禁发，报告后停止；本轮仅规划、尚未开始实现。以下早期“最新/下一步”保留原阶段含义，产品目标未扩张。

2026-09-18后续更新：用户明确要求只实施3A，已完成并停止，实际结果见[10](10-phase-3a-implementation-report.md)；3B/3C未开始。以下保留原方案和当时状态。

2026-09-18最新规划：3A的契约校验已收口，见[12](12-phase-3a-contract-closure-report.md)。下一步推荐按[13](13-phase-3b-1-implementation-plan.md)只实施3B-1目标/目录/手动组合事务，继续禁发；3B-2再接恢复与生命周期。产品范围不变，manual不推进自动occurrence/next-at。当前只保存方案，3B尚未实施。

2026-09-18 · **方案形成时，第三阶段尚未实施。** 用户本轮要求“下一步应该做什么？给出执行方案”。前两阶段结果见[06](06-phase-1-implementation-report.md)、[08](08-phase-2-implementation-report.md)；本轮只读调查并保存方案，不启动服务、迁移数据或调用模型。

## 1. 下一步结论与分批停点

下一阶段是第三阶段“受管执行闭环”，但**下一次实施建议只做 3A：执行契约、兼容 reader、native 授权和共享预约基础**。先证明计划能够被正确授权、去重并与前台互斥，再接实际投递。3A 完成后交付检查结果并停止，不自动继续 3B、3C 或页面阶段。

| 批次 | 结果与依赖顺序 | 完成后停在哪里 |
|---|---|---|
| **3A：执行基础** | source-first 最小契约 → 新格式兼容 reader → 有限授权/预约模型 → 前台提交与出站门禁 | 正常合成数据检查通过；无新增可投递 outbox、无真实会话/Runtime/模型调用 |
| **3B：投递与恢复** | 受管目录 → 同事务三目标/run/原 outbox → Host 查询消费 → 审批观察、正常退出和睡眠恢复屏障 | 人工受控的执行链具备接线条件；自动扫描仍关闭，先做零付费集成检查 |
| **3C：定时与草案接线** | 受控自动触发 → 固定 outputSchema 草案/确认保存后端 → 最小真实集成资格 | 第三阶段报告与未验收项；不自动进入第四阶段 |
| 第四阶段（本方案不实施） | PDF 页面、完整创建/管理/历史交互、应用内重要更新、防空闲睡眠开关及全部 Must 的真实验收 | 全部 AC 经实际验证后才能判定 D4 |

这是用户要求的分步工作安排，不新增生产治理切片。已批准的三种“运行于”、两种创建、权限/恢复要求均保留；系统通知仍延期，超过 16 小时不构成禁止条件。第三阶段完成也不代表完整 FEAT-155 已交付。

## 2. 已核实的起点与具体缺口

本轮文档变更 `contract-impact=none`：仅规划，不改变协议、存储或运行行为。未来第三阶段最高影响仍按 **breaking** 管理：新持久格式、工作目录来源、授权与出站解释均须逐边界 source-first，不把“只加表”当作兼容证明。

本轮复核 Desktop/Contracts/Host 的前两阶段候选文件共 52 份，SHA-256 均与[阶段二来源证据](evidence/phase-2-source-20260918.json)一致。五仓仍在 `chore/retirement-baseline-20260905`，HEAD 如下；这些是已有工作区基线，不是新版本发布 pin。

| 仓库 | HEAD | 当前状态 |
|---|---|---|
| yijie | `2f616f4d24c001812c6279a520ba69ea9875247e` | 已有需求包/ADR 文档改动，本轮仅追加方案 |
| yijie-contracts | `db4458fe94572c4df41a114005d54a049bb79b1f` | 前两阶段未提交候选，保留 |
| yijie-agent-host | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` | 第一阶段未提交候选，保留 |
| yijie-desktop | `4a8a67bec4903624ca98a1098572fa26f3a20849` | 第二阶段未提交候选，保留 |
| yijie-codex | `6c1ad767f0997845b8258a1c452fd4eb7577579f` | clean；固定 Runtime 0.144.6，只读、不升级 |

| 源码事实（行号为本次候选） | 对实施顺序的影响 |
|---|---|
| Desktop `chat/migrations.rs:34,124`：catalog 16，默认迁移目标 15，最高可读 16；`0016_scheduled_plan_foundation.sql` 仅有计划/请求/occurrence | 阶段二不是执行格式的回退 reader；新 run/grant/预约及 outbox 解释需独立兼容验证 |
| `chat/database.rs:1728,2125`：聊天创建/追加各自开事务 | 必须抽取内部事务 helper，组合在一次 SQL 事务中；不能串两个 worker 调用伪称原子 |
| `chat/database.rs:1876,2218` 与 `host_bridge.rs:546`：旧文本 v1 不携可恢复的 operation ID；`:570,604` 的 v2/permission-turn 已携带 | 定时文本复用既有幂等 v2/permission-turn Ask 路径，不走 legacy v1；不全面重构普通聊天 |
| `chat/application.rs:2077,2082,2408`：先 dispatch、只观察首个 active session，流内仍会 dispatch；`database.rs:2381` claim outbox | 预约须覆盖前台 create/enqueue、outbox claim 和真正出站；只看 running 或 recovery_snapshot 不够 |
| `chat/database.rs:8282`：新聊天权限继承前台 draft_mode 并重置它；`application.rs:1881` 出站读取当前 mode | 定时新聊天显式 Ask 且不改前台偏好；出站再次核验，不能沿用 claim 时的旧权限 |
| `chat/application.rs:1690` 创建需 project/bookmark；第二阶段新聊天目标只是 unbound | 须新增明确 native 受管目录引用，不能伪造用户 bookmark 或隐选首个项目 |
| Host `internal/app/scheduled_recovery.go:39,64` 两查询已存在，Desktop HostBridge 尚未消费 | 先接只读恢复，不能以网络重试重新创建/提交补缺失身份 |
| Desktop `lib.rs:436` 只在不可取消 Exit 中 shutdown；`chat/mod.rs:891` 清桥后停 sidecar | 必须提前接管正常退出、停止唯一 Coordinator，并保留 STOP_PENDING 的观察/停止能力 |
| Host `scripts/permission-smoke-meter.py:49–80` 已有转发前落盘的真实请求上限；独立标题 `internal/codex/title.go:121–135` 未传普通验证配置 | 可复用验收计数器，但必须证明新建/resume/草案/标题等实际路径全覆盖，不能把一个 run 当一次 HTTP 请求 |

Desktop 路径均相对 `src-tauri/src/`，migration 相对 `src-tauri/migrations/chat/`。生命周期和执行调查分别做了只读交叉复核；属于 Codex 技术审查，不是独立人工批准。平台监听、草案 Provider 合规率、未来 reader 和出站预算目前仍未验证。

## 3. 下一次只实施 3A

### 3A-1. 最小执行契约先行

在 Contracts 独立定时任务族扩展本批确实消费的类型；复用已冻结时间/目标定义及恢复查询，不预铺完整管理平台 API。

- 明确 run_id、request_id、稳定 operation_id、plan/revision/schedule_epoch、触发来源、历史快照与会话/原生关联的分工。自动槽与手动请求分别去重，重跑是新请求/新 run。
- 分开计划生命周期、投递状态、原生执行结果与 needs_attention；不把 native turn completed 当作业务目标成功，不复制消息/tool/Artifact 正文。
- 冻结有限授权的确认输入/回执：绑定 plan/revision、目标/内容/时间含义、有限次数及到期时间；scope/grant 身份取 native 权威，不能由 renderer 或模型自授。
- 定义受管 workspace 的明确来源与安全引用；existing chat 沿原目录。新增 source 变体只在 reader/provider 就绪后消费，不改旧 bookmark 的解释。
- 定义本批所需稳定错误和可恢复性：revision 冲突、目标失效、权限/授权不足、预约占用、执行未就绪。不可发送的候选不得返回“运行已受理”。
- source → 必要 Rust/TypeScript/Go 投影 → 同源 conformance → consumer；只生成实际需要的语言和边界。私有 SQL/进程生命周期记录留 Desktop，未跨仓消费的内部结构不塞进公共契约。

固定 Runtime canonical schema 不变。后续草案模式/Host 参数适配在真正消费前补其最小源契约，不允许 renderer 传任意 outputSchema/config。

### 3A-2. 兼容 reader 与私有扩展

1. 复核 catalog 后新增下一版本，按当前事实候选为 **17**；不修改 migration 1—16 的字节或 checksum。
2. reader 先理解新增 run、有限 grant、预约与受管目录引用，以及将来 scheduled outbox 的标识/版本。能解码还不够：writer 关闭时，普通 Coordinator 必须识别并暂停未处置的 scheduled outbox，不能误当普通消息派发。
3. 继续分离最高可读版本和允许迁移目标。**普通入口仍以 15 为迁移目标**；只在正常合成临时库前向验证 15→16→17、正常关闭/重开、旧聊天操作与新记录共存。
4. 保留完整 migration ledger 和未知版本拒绝；旧 15/16 reader 不能冒称可回退到 17。阶段三兼容候选须有可恢复的源文件/digest 和标准构建来源；当前不自动提交或制作发布 pin。
5. 日常用户库激活不随本批发生。未来激活须先展示具体 reader/writer、前向迁移和正常停用方案，沿正常入口处理；不复制、重置或降级用户库，也不另建第二套产品数据库掩盖兼容问题。

### 3A-3. native 授权、有限 grant 与共享预约

- 沿现有 native authority/ChatScope 建立独立读取、管理、运行校验；UI 管理仍使用短期 context，后台运行不能缓存 300 秒 context 或持久化 bearer。claim 和实际出站都重新校验当前 authority、revision、目标、Ask、grant 和生命周期。
- 未确认计划仍暂停。grant 到期/耗尽或内容、时间、目标变化后，禁止新投递并要求按现有设计重新确认。逻辑 run 额度与 Provider HTTP 验收总账分开。
- 预约由同一 worker/事务裁决：前台 queued、未发送 outbox、session 创建发送中、accepted 未写回、原生运行、待批准、unknown 均参与判断。最多一个定时 run 未结束；定时预约占用时前台新发送保留草稿。没有定时预约时保留原前台并发规则。
- 同时接前台 create/enqueue、outbox claim 和实际 dispatch 的必要检查。3A 不产生定时可投递 outbox，不能为证明门禁而启动真实运行；用纯领域/普通合成事务覆盖竞态与占用。
- reservation 不因等待超时或用户点确认就释放。释放须有原生终态、正常中断确认，或受管旧 generation 正常关闭及新 generation 门禁事实。Host 响应实例 ID 不能替代历史执行 generation。

3A 只形成上述基础及必要旧聊天适配，不注册可以真实开启调度或绕过授权投递的临时调试入口。

### 3A 完成标准与交付

| 检查 | 可判定结果 |
|---|---|
| 契约 | 同源生成无漂移；普通有效/无效输入、null/缺失字段、错误和权限语义一致；适用基线检查通过 |
| 兼容 | 默认 15 不升级；合成库正常前向迁移/重开；旧聊天保持；新 reader 关闭 writer 时不误派发定时记录 |
| 授权 | scope/revision/target/次数/期限不匹配均拒绝；过期 UI context 不可充当后台授权；不保存凭据 |
| 预约 | queued/创建中/未写回/待审批/unknown 均阻断冲突；重复 request 不多占额度/预约；定时 Ask 不继承或修改前台 draft_mode |
| 副作用 | 不创建真实聊天、可投递定时 outbox 或自动 timer；不启动 Host/Runtime/Provider，不访问用户库；模型仍 0/12 |

交付本批实际报告、源摘要、生成/兼容/定向检查及未执行项；随后停止。不得因 3A 通过而将 run 投递、真实恢复、草案或 AC/D4 标 PASS。

## 4. 后续 3B、3C 的实施顺序

### 3B：同一执行链上的投递与恢复

1. **目录与三目标。** native 用稳定资源 ID 幂等准备应用受管目录，然后入库重验；文件系统准备不冒称 SQL 原子事务。专属聊天首次 claim 懒绑定并复用；每次新聊天分配独立 conversation/task；已有聊天复用明确的本地 conversation ID 及原目录。目录失败不生成 outbox，不做后台孤儿目录清理。
2. **一次组合事务。** 在同一 SQLCipher/worker 内重验 scope、plan/revision/目标/grant/预约 → claim 槽或手动请求 → 固定 run 快照/operation → 创建或绑定本地聊天 → 写原 chat outbox → 唯一预算占用 → 推进 next-at。复用事务 helper，失败整体回滚；远端 session/thread 创建在事务后，不能写成跨进程原子性。
3. **出站闸口。** scheduled 文本走已有 v2/permission-turn Ask，保持同一个 operation；出站前再验所有条件并记录 sending。新聊天显式 Ask、不修改前台 draft_mode；已有/专属会话 Auto/Full 阻断且不静默切换。证明未出站时可以按规则取消并撤销占用；已出站或 unknown 不返还预算、不重发。
4. **只读恢复。** 创建已出站未确认先查原 task 映射；bound 才关联，reserved/missing 保持不确定。turn 已出站查 session+operation，accepted 绑定原 turn，pending/uncertain 不补发。已有原生事实继续由原观察/read 链保存，不重建第二状态机。
5. **审批和删除。** native 观察未结束 run 的审批，不依赖用户打开某聊天；保管可查询的 needs_attention，批准/拒绝仍在既有完整对话，不保存过期 callback。暂停/编辑可撤销未出站动作，已 sending/accepted 只影响未来；删除在途计划按现有决策阻断。删除聊天同时处理引用计划、未出站 outbox、运行关联及墓碑，保留 ADR-0014 的正文清理语义；每次新聊天模式不因一份历史聊天删除而停掉未来计划。
6. **退出与恢复屏障，先于真实投递资格。** native 生命周期 owner 管理唯一 Coordinator。可取消退出先关闭新 claim/发送、持久化事实、停止新派发，再按正常协议关闭 Host/Runtime，处理平台句柄并最终关闭 DB/允许 Exit。STOP_PENDING 保留进程身份、句柄、观察与再次正常停止能力；不得仅阻止 UI 退出却丢掉 child/nonce。Host 自己的退出/超时路径也须检查，不能只关闭 Desktop 的 forceful fallback。
7. **真实 sleep/wake 观察。** 在 App 生命周期监听睡眠/恢复；新启动或恢复先处理不确定操作/时钟区间，再求严格未来时刻。只有 identity、DB、Host ready、预约恢复和连续清醒证明都通过才允许派发。防空闲睡眠的产品开关仍在第四阶段。

3B 先用正常临时数据、进程内接口和安全协议检查验证；普通合成 pending/uncertain 可测决策，不通过断网、强杀、破坏权限或伪装 Runtime 制造异常。自动扫描保持关闭。不能用 idle/notLoaded、当前 Host nonce 或用户同意来消除过去投递的不确定性。

### 3C：定时触发与对话草案后端

- 生命周期等前置项完成后才接 native 等待/唤醒：复用阶段二 evaluator，到点重读权威计划；等待有界，计划变更及时重查。连续清醒最多迟到 60 秒；正常重开、sleep/wake、时钟不连续优先不补跑；忙碌记未执行原因，不无限排队或展开离线历史。
- 手动立即执行/重跑与自动触发共用 3B 的授权/预约/事务/投递链。用户重跑基于当前已保存配置，保留与原快照差异，不能复活旧 run；重复传输仍沿用同请求身份。
- 对话创建使用第一阶段固定 schema，Host 补受限模式适配，沿既有普通聊天 thread/turn 产生 clarify 或 candidate；native 校验时间与目标、解析明确 ID，用户确认后同源幂等保存。partial/无效输出不保存、不解析自然语言冒报“已创建”。首次创建对话也使用明确受管目录，不隐选项目。
- 仅增加第四阶段真实使用所需的 typed command/query 及 native 事件；无任意 SQL/schema/config/路径调试通道。形成记录查询、运行关联和重要更新事实，列表、弹窗、通知显示/跳转由第四阶段消费。

## 5. 验证、预算和正常数据激活

**3A、3B 计划为零模型调用。** 3C 优先完成安全定向和不付费的协议资格；真实 Provider 验证只在请求级计数覆盖、正常停止和正常产品调用路径均可证明时进行。

整个 FEAT 仍最多 **12 次文本 HTTP 请求，当前 0/12**，包括草案、澄清、执行、标题及内部重试；图片和商家/MCP 业务调用均为 0。建议第三阶段最多占用 4 次，至少保留 8 次用于第四阶段同次 fresh run；这是额度内的工作分配，不增加上限，也不保证 4 次能完成所有真实用例。未消耗额度继续保留，任何未知出站保守计数、不返还。

复用现有验收 meter，仅做本需求必要适配：总账连续、转发前持久计数、总上限 12、本批停止阈值可执行；不得通过新账本/重启重置额度。已有脚本的 limit 与历史 ledger 绑定，不能直接改 ledger 数字假装支持分阶段预算。核查新建、resume、普通 turn、草案和标题是否全部受控；标题若确无 production 出站调用，留源码/零调用证据；若候选启用标题，则先补同一验证配置。计数器仅为验收支持，不新增产品计费平台或替换 Runtime。

如果此时尚无正常产品入口完成确认/触发，或计数、日常库激活条件未满足，**不新建旁路测试 App/调试入口硬凑真实验收**：保存具体阻塞，把实际付费验证与相关结论留到第四阶段，标 NOT RUN。合成测试只证明工程行为，不能冒充 D4。后续日常 writer 激活需先形成具体可审查的来源/兼容方案，不能借真实 smoke 擅自迁移日常库。

| 组别 | 核心验证 | 范围说明 |
|---|---|---|
| 事务/重复 | 同槽/请求只一个 run/outbox/扣账；revision 冲突不部分创建；取消未出站与 unknown 区分 | 普通临时库和接口；不故障注入 |
| 三目标 | 专属复用、每次独立、已有沿原目标；Ask 和前台偏好不串用 | 合成关联先验证，三模式真实会话结果在最终验收复核 |
| 恢复/并发 | queued、创建在途、accepted 未写回、pending 审批、unknown；Host 两查询绑定原身份，不重发 | 普通状态构造/安全协议检查，不伪造真实异常发生 |
| 生命周期/时间 | 正常退出重开、实际睡眠恢复先于扫描；连续清醒容忍、DST、时钟变动纯函数检查 | 不改系统时钟、不强杀；实际平台操作仅在有受控服务资格后进行 |
| Provider | 固定 schema 真输出及一个真实未来时刻触发；预算含全部实际请求 | 具备条件才用有限额度；不足/未执行如实登记，全部 AC 留第四阶段 |
| 回归/来源 | 适用源生成/conformance、基线兼容、Rust 静态及定向旧聊天/Host 检查；结构化自审 | 只跑事先审查的安全测试集合，不跑含禁止 fixture 的历史全量测试 |

预期沿用阶段二的 Contracts leaf 检查/安全用例、Desktop Rust fmt/clippy/定向测试，涉及前端类型则做 lint/build；Host 增量做相关 race 测试/lint。先审查测试会做什么再运行，按实际命令与输出记结果，不预填 PASS。对没有覆盖的异常韧性、真实 Provider/平台/UI 结论逐项说明影响。

## 6. 仓库范围与本轮交付

- **Contracts：** 最小共享执行/授权/目录来源及草案适配契约、生成物、相容性与安全用例。
- **Desktop：** 原 SQLCipher/worker/聊天应用/Coordinator/outbox 的必要扩展，native 授权、目录、恢复及生命周期；不建立第二执行器。
- **Host：** 必要草案/受管配置、正常退出与计数覆盖适配；两类查询优先消费既有实现，计划主状态仍不放 Host。
- **元仓：** 分批实际结果、来源、费用和未验收项。Runtime/API/Infra 不新增实现。

本轮只保存本方案及需求包状态/日志；第三阶段业务代码、契约生成、迁移、真实服务、模型、UI 验证均未开始。下一次推荐明确执行 **3A**，完成后先审查和报告，再决定进入 3B；不自动提交、推送、发布或扩大需求。
