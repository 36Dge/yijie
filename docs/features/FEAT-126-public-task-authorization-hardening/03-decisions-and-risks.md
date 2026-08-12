# FEAT-126 决策、风险与安全预审

## 1. 决策状态约定

- `Recommended`：Codex 根据当前代码和用户需求给出的候选，尚未得到段成威批准。
- `Ready for Owner Approval`：设计事实、边界和候选文本已完成，可由段成威作接受/退回决定；仍不是Accepted或实现授权。
- `Accepted`：段成威留下明确结论和日期后可作为后续设计输入；不自动授权实现。
- `Open`：不影响继续完善文档，但标注的 Gate 之前必须关闭。

## 2. 关键决策

| Decision ID | 问题 | 可选方案 | 推荐选择 | 理由 | Owner | 状态 |
|---|---|---|---|---|---|---|
| DEC-126-001 | FEAT-126 编号冲突 | 对话迁新 ID / 安全责任迁号 / 合并安全纵向需求 | 保留 `public-task-authorization-hardening` slug，合并对话产品轨与安全轨 | 不破坏 ADR-0012/FEAT-125 例外追踪；新建任务与 Tasks 授权是同一 release safety boundary | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-002 | 项目/工作区含义 | 本地目录 / 业务 workspace / 新 cloud entity | 本期为 native picker 选择的本地目录引用，首次 turn 必选 | 对齐 Host `cwd`，不引入 cloud entity；`workspace.use` 只作 capability，不证明路径权限 | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-003 | 权限审批入口 | 可编辑策略 / 状态入口 / 移除 | 本期保留只读状态入口，显示 fixed read-only/deny；不提供提升 | 当前 Host `approvalPolicy=never` 且 reverse requests 拒绝，真实审批会显著扩大安全范围 | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-004 | Chat 侧栏 | 删除全局 toggle / 禁止二级 toggle / 固定新 rail | 不新增 Chat 二级 toggle；保留 FEAT-124 全局 240/72；G2 Pattern 候选据此固化 | 对用户“无显示/隐藏”采取最小破坏解释，避免静默推翻 App Shell | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-005 | 本地数据权威 | Web localStorage / Host bbolt / Desktop Rust SQLite | Desktop Rust-owned、版本化 SQLite；Vue 经窄 Tauri commands 访问 | 正文是 Desktop 业务数据，Host 明确不是业务数据库；localStorage 不适合 confidential durable data | 段成威 | Accepted 2026-08-02 / ADR-0013；driver/protection/backup已由ADR-0014冻结；不授权实现 |
| DEC-126-006 | 物理删除边界 | 仅 DB 行 / DB+Host / DB+Host+Runtime | 先清理 session 独占 Runtime thread tree（含 spawned descendants）与 Host bbolt/replay，再事务删除 Desktop rows并验证 `secure_delete=ON` + `wal_checkpoint(TRUNCATE)`；跨 session mapping中止；成功只留 30 天 content-free receipt，项目目录不删；只承诺 app-managed live store 不可恢复，不承诺所有磁盘字节抹除 | 避免“UI 消失”假删除与误删共享 thread；隔离验证证明 functional delete，但 Runtime WAL/log 有字节残留 | 段成威 | Accepted 2026-08-02 / ADR-0014；不授权实现 |
| DEC-126-007 | 模型标题 | 主 thread 隐藏 turn / pathless ephemeral 模型 operation / 本地启发式 | 采用 ADR-0015：独立 Host operation 在空临时 cwd 使用 `ephemeral=true` Runtime thread、`title-v1` strict turn `outputSchema`；不接入 user thread/project/events，结果经 40-grapheme plain-text validation，人工 rename 优先，失败 deterministic fallback，最多初次 + 1 次确定失败重试 | fixed fake-provider fixtures 已证明 ephemeral pathless 与 turn-scoped structured output；`MM-126-001` 单次 MiniMax strict title PASS；隔离对话语义并限制成本/注入面 | 段成威 | Accepted 2026-08-02 / ADR-0015；Q-008 Resolved；不授权实现 |
| DEC-126-008 | 思考过程（旧结论） | raw CoT / public summary / 仅时长 | 只投影 provider/Runtime 明确允许公开的 summary/阶段；无内容时仅状态/时长 | 原 G1 安全边界 | 段成威 | Superseded 2026-08-02 by DEC-126-015 / ADR-0016；历史决策保留 |
| DEC-126-009 | session 排序 | created / updated / last activity | pinned group + `last_activity_at DESC` + stable ID；rename 不触发 activity | “倒序”可判定且不因改名扰动列表 | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-010 | 项目移除 | 删除目录 / 级联删 session / 移除引用 | 只移除可选引用；目录和历史 session 保留 | 最小破坏、符合“移除”而非“删除” | 段成威 | Accepted 2026-08-01 / G1 |
| DEC-126-011 | Public Tasks compatibility | 同路径硬切 / versioned expand / 永久隔离 | 新建受保护 `/v2/tasks`，先 expand provider、迁移已知 consumer、观察，再退休 `/v1/tasks`；迁移全程 v1 保持 Host profile + ingress 双隔离。退休窗口至少 30 个自然日且跨 2 个 Desktop release candidates，并要求 owner attestation 与 0 次 approved/authenticated v1 use | 仓内 inventory 未发现活跃 consumer，但 Public OpenAPI 使未知外部 consumer 不能被证明为零；versioned expand 是唯一不依赖“无人使用”假设的安全分支 | 段成威 | Accepted 2026-08-02 / G2；Q-010 Resolved；不授权业务实现 |
| DEC-126-012 | Task 所有权 | tenant-wide / creator-private / role-based mixed | v2 初始 creator-private；`created_by_user_id` 只能由 verified principal 派生。普通 role 不隐式获得跨 creator 读取；未来仅显式 `task.read_all`/`task.manage_all` capability 可扩展。无法可信归属的 legacy NULL-owner rows 隔离，不猜测回填 | 防同租户 IDOR并把高权限扩大变成可审计的显式授权；旧数据不因迁移被错误归属 | 段成威 | Accepted 2026-08-02 / G2；不授权业务实现 |
| DEC-126-013 | 视觉语言 | 像素复刻 Codex / 自创 / 融合易界 Design System | 以易界 token/Accepted Pattern 为权威，吸收 Codex 信息层级、macOS 克制和 Linear 密度 | 保持品牌一致、生产可维护与无障碍 | 段成威 | Accepted 2026-08-01 / G1；FEAT-126 Pattern Accepted 2026-08-02 / G2 |
| DEC-126-014 | 本地产品轨与 Public API 的运行关系 | 对话每次先写 Public Task / local-only 独立 / 双写 | 本期 conversation data 与 session lifecycle local-first；Public Tasks hardening 是同 feature 的独立 release-blocking 安全轨，不上传 message body | 满足“暂存本地 DB”，避免跨 DB 双写与 prompt 云持久化 | 段成威 | Accepted 2026-08-02 / ADR-0013；Public Tasks release design已由DEC-126-011/012/018冻结；不授权实现 |
| DEC-126-015 | 模型推理展示 | public summary only / raw reasoning / 仅状态时长 | 展示固定Runtime/model实际返回的raw reasoning纯文本，标注“模型推理记录”；不保证完整/稳定/真实内部思维，不进日志/遥测/审计；无raw或流无效则能力验收失败，禁止静默时长-only | Owner要求必须显示具体推理文字；MM-126-002已证明当前pin提供raw事件但无public summary | 段成威 | Accepted 2026-08-02 / ADR-0016；取代DEC-126-008展示部分；不授权实现 |
| DEC-126-016 | raw reasoning 生命周期 | 仅当前内存 / Desktop SQLCipher历史持久化 / Runtime rollout作为历史 | 流式阶段由Desktop内存reducer展示；terminal对账后或中断为显式incomplete时写入SQLCipher独立reasoning records，随session历史懒加载和FK cascade物理删除；不写Host业务DB/日志/云端，不依赖Runtime rollout | 与既有历史权威一致；复用ADR-0013/0014加密、backup披露和删除边界；避免重开后同一turn内容消失 | 段成威 | Accepted 2026-08-02；Q-016 Resolved；细节由DEC-126-017候选承接，不授权实现 |
| DEC-126-017 | raw reasoning v2 与 SQLCipher 细节 | 直接透传 Runtime item / 每 delta 落库 / closed v2 projection + terminal coalesced commit | 采用 DESIGN-126-003：v2 仅新增 `item.reasoning_text.delta` 与 `item.reasoning_text.finalized`；completed raw `content[]` 为权威快照。Desktop 以内存按 event/sequence/item/content index 聚合，仅在 finalized/受控中断时单事务写 `chat_turns` reasoning 状态、`chat_reasoning_items` 与 `chat_reasoning_parts`；固定 delta/part/item/turn caps、显式 incomplete/unavailable、20/50 turn history 分页与 session FK cascade | 不让 closed v1 consumer 接收未知 variant；避免逐 delta 写放大和重复拼接；可表达 partial、缺失、过限、重启与物理删除，且不把正文扩散到 Host durable surfaces | 段成威 | Accepted 2026-08-02 / G2；DESIGN-126-003 complete；不授权业务实现 |
| DEC-126-018 | G2A source contract shape 与候选版本归属 | 改写既有v1 / 新建独立0.4分支 / 在未发布0.3.0 candidate上versioned expand | 接受当前source shape：在未发布`0.3.0 candidate`新增secure Public Tasks v2、Host v2 title/cleanup/events与AgentSessionEventV2；v1 wire保持不变。Host cleanup为解决“已删mapping但成功响应丢失”，另留30天content-free operation receipt（operation ID、keyed session hash、分表面结果、时间/schema version；无raw ID/正文/path）。按批准后的shape形成immutable source/generated commit并复验digest；未通过最终G2A前不得tag、pin、消费或开始业务编码。如FEAT-125需要先独立发布，pin前再评审拆分版本 | 当前仓库已处于未发布0.3.0 candidate，版本化expand避免硬切；content-free receipt使清理可幂等重试而不保留mapping/正文；source/generated/fixtures/SDK及全部支持基线门禁已通过 | 段成威 | Accepted 2026-08-02 / source shape；已授权形成immutable candidate commit；不授权业务实现 |
| DEC-126-019 | 最终 G2A source-contract readiness | 通过 / 退回契约修改 / 要求先远端发布再评审 | 批准`yijie-contracts@c000a0245acb5c3f7ead5d2a877fb60c281c588c`为FEAT-126唯一source-contract candidate：提交后generate/lint/test/build/pack、支持基线breaking及v1 wire equality均PASS，摘要稳定；后续consumer只能固定该完整SHA。G2A批准不授权push/tag/merge、业务编码或生产启用；远端可用性与明确实现指令仍是启动下游切片的操作前置 | DEC-126-018已Accepted；不可变提交把source/generated/fixture/docs绑定为同一可复验对象。批准时commit仅本地、`develop`领先`origin/develop` 1个提交，这不改变source shape判断，但在远端可用前其他环境不能消费，必须明确披露 | 段成威 | Accepted 2026-08-02 / G2A Passed；唯一candidate已确认；本决定本身不授权远端写入、pin、业务编码或生产启用；后续仅DEC-126-020单独授权专用branch push |
| DEC-126-020 | source-contract remote availability | 直接移动`origin/develop` / tag或发布 / 专用远端候选分支 | 仅把唯一candidate完整SHA推送到`refs/heads/feat/feat-126-contract-candidate`，保持`origin/develop`不变；在临时clean clone验证HEAD、generate无漂移、lint/test/build、支持基线breaking、v1 wire equality和九项摘要；不merge、tag、发布、downstream pin或编码 | 把远端可消费性与共享分支合并/版本发布解耦；完整SHA提供不可变身份，专用branch只保证对象可达。clean clone能排除本地未提交文件或缓存造成的假PASS | 段成威 | Accepted and Executed 2026-08-02；remote SHA精确匹配，clean clone PASS，`origin/develop`保持`9ec34abd6e7dfb5a23b0154d467694167224ebbb`；临时目录已移入废纸篓 |
| DEC-126-021 | 固定候选 Draft PR 的 merge readiness | CI红灯仍merge / 重跑或豁免audit / 保持Draft并修复依赖后以新候选复验 | **HOLD，不批准当前merge**：保留PR #1与head `c000a0245acb5c3f7ead5d2a877fb60c281c588c`不变，不重跑、不豁免。未来只有本地跨仓E2E通过、dependency audit修复、远端CI全部绿色且Owner另行批准时才可merge | PR #1的generate/diff/lint/test/SDK pack通过，但`pnpm audit --audit-level high`因锁定的传递依赖`brace-expansion 2.1.2`（GHSA-mh99-v99m-4gvg，patched `>=2.1.3`）失败，后续`govulncheck`和`origin/main` breaking被跳过。候选未改`package.json`/`pnpm-lock.yaml`，因此不是契约diff新增依赖；但红色门禁仍阻断merge。该失败不回退已批准的G2/G2A，也不阻断未来明确授权的本地draft实现 | 段成威 | Accepted 2026-08-02 / HOLD；Draft PR保持不变；当前不批准merge |
| DEC-126-022 | FEAT-126交付模式与本地契约消费 | 生产发布型 / 本地可运行但仍强制tag/publish / Local-only Delivery | 采用**Local-only Delivery Strategy**：目标是在Owner本机完成API/Host/Desktop/Runtime构建启动和完整本地E2E；明确授权的本地draft consumer只固定当期唯一完整SHA（当前由DEC-126-024更新为`29317b6426578749dc698fc2ad32b986ee5c8e9f`），可用已核验sibling path、workspace/path dependency、生成SDK或已核验本地tarball，浮动branch不能作为不可变身份。merge不再是开始本地draft实现的前置，但仍须满足DEC-126-021并单独审批；本期tag/package publish/registry/线上部署/生产灰度/生产启用/云数据库/真实用户数据均N/A。先用fake provider/fixtures；本地链路完成后最多一次MiniMax local smoke另行审批 | 单机开发无需为本地运行引入registry与生产发布成本；完整SHA和本地制品足以保持可复验。把merge与deployment解耦既允许稳定候选上的本地draft实现，又不绕过远端红灯。G5明确N/A，G6只表示本需求范围内Local-only Delivery Complete，不冒充Production Ready；未来产生线上意图必须重开生产轨 | 段成威 | Accepted 2026-08-02；contract identity由DEC-126-024更新；slice授权后续已由DEC-126-026/027推进到S7B；MiniMax及S8–S11仍未授权 |
| DEC-126-023 | Public Tasks `input` 与本地会话数据权威冲突 | A. 保留`c000a024`并允许任意task input/正文；B. 保留`c000a024`但只约束Desktop不调用；C. 以新commit取代候选，将v2 request/response/fixtures收窄为content-free metadata/reference | **采用C并暂停S4–S11**：`c000a024`保持不可变且不追加push；在本地新分支形成replacement candidate，使prompt、message、raw reasoning、title派生正文和项目路径不能进入`/v2/tasks`或PostgreSQL，只允许closed、content-free metadata/reference；重新生成SDK、更新fixture、做supported-baseline breaking/semantic review并取得新的完整SHA和G2A批准 | immutable source在`CreateTaskV2Request.input`和`TaskV2.input`上使用`additionalProperties:true`，权威fixture以`task_type=conversation`携带`input.text`并在response回显；这与ADR-0013/DEC-126-014及LIA-126-002“正文不得进入Public Tasks/PostgreSQL”直接冲突。仅在provider里私自拒绝`text`会收窄已批准wire语义并造成契约漂移 | 段成威 | Accepted 2026-08-02 / 方案C；Q-017 Resolved；replacement candidate已形成并由DEC-126-024批准；LIA-126-002继续暂停 |
| DEC-126-024 | content-free replacement source-contract最终G2A readiness | 批准新candidate / 退回shape或证据 / 要求先远端可用 | **批准**`yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一source-contract candidate：其parent精确为`c000a024`且未amend旧提交；Public Tasks v2 request/success/error仅保留closed、content-free discriminator/reference/metadata，移除title与任意result/error正文；fixtures及TS/Go SDK同步。post-commit generate/lint/test/build/pack、支持基线breaking、Public Tasks v1 2 paths与Host v1 7 paths reference-closure equality、schema/fixture conformance和摘要复验全部PASS。本批准不授权恢复LIA-126-002、修改业务源码、远端写入、push/merge/tag/publish/deploy、MiniMax或S7–S11 | 新candidate完整commit可复验且worktree clean；Public OpenAPI=`c8d9e674…354b`、TS=`e84b70be…b678`、Go=`c3d6e58e…c697`、SDK tarball=`21b17b50…b082`。旧`c000a024`仅保留为历史远端候选，Draft PR #1与远端保持不变；下游runtime conformance因明确禁令未运行，不能把source-level PASS冒充实现证据 | 段成威 | Accepted 2026-08-02 / G2A Re-review Passed；LIA-126-002仍暂停，恢复Foundation Corrective Closure须另行明确授权 |
| DEC-126-025 | Remote State Reconciliation与LIA-126-002恢复边界 | 把已发生push视为发布/实现完成 / 回退远端分支 / 只登记不可变远端可达并恢复S4–S6纠偏 | **采用第三项**：登记`29317b6426578749dc698fc2ad32b986ee5c8e9f`位于`origin/feat/feat-126-content-free-candidate`；登记yijie/API/Host/Desktop各checkpoint分支远端SHA与本地精确相等；`origin/develop`、旧`c000a024`、Draft PR #1、merge/tag/publish/deploy均不变。单独恢复LIA-126-002，只允许S4–S6 Corrective Closure；不进入UI/S7–S11，不调用MiniMax，不启用flag，不追加远端push | 远端对象可达仅解决跨环境检出与审计，不代表contract merge、下游conformance、Code Complete或生产启用。把恢复范围绑定S4–S6可在稳定source上关闭P1，同时维持consumer/UI与激活门禁 | 段成威 | Accepted 2026-08-02 / In Progress；文档校正先于业务diff，Closure Review前不追加远端动作 |
| DEC-126-026 | LIA-126-002 Foundation Corrective Closure | 接受S4–S6 closure并进入S7A单独授权 / 退回指定P1 / 扩大到S7/UI | **采用第一项**：S4完成content-free审计矩阵、nil-tenant映射、24h幂等保留/清理、只读生成漂移门禁和`29317b...`运行时conformance；S5完成持久化cleanup operation、cleanup/turn lease、session-scoped title幂等与owner-only cwd、receipt expiry、v2 schema header、instance nonce及raw no-log/bbolt canary；S6完成terminal reasoning与聚合一致性、joined history读取、级联/foreign-key校验、migration负向矩阵和Host-live/Runtime-ready分层。所有列明P1由本地fake/fixed/临时环境证据关闭；Owner另行授权S7A仅实现Desktop Rust Host Bridge/Domain | 三仓完整本地门禁及隔离PostgreSQL集成测试通过；契约锁统一为`29317b...`。S7A只允许owner-only bearer/token读取与注入、exact loopback HTTP/SSE、Host instance nonce/readiness、v2 schema/cursor及typed domain adapter；不改Vue/S8，不调用MiniMax，不启用flag，不远端写入或merge/tag/publish/deploy | 段成威 | Accepted 2026-08-02 / LIA-126-002 Closure Passed / S7A Authorized |
| DEC-126-027 | S7A Desktop Rust Host Bridge/Domain Closure Review | 接受S7A并单独评审后续Rust application slice / 退回指定Rust P1 / 扩大到UI或激活 | **接受第一项**：S7A仅在Desktop Rust新增由`ChatRuntime`持有的Host client/domain；每次受保护调用先以spawn nonce复验`/readyz`，transport固定`http://127.0.0.1`、no-proxy、no-redirect；bearer只从owner-only regular single-link `api-token`以`O_NOFOLLOW`读取；严格映射session/turn/cleanup和v2 schema/cursor/SSE，未知非terminal event只推进cursor并丢弃payload，所有Debug/error均不回显token、路径、正文或Host message。没有新增Tauri command/invoke或Vue diff，所有flags保持false | Desktop门禁及canonical reasoning/fake Host/security/fault证据通过；S7A是现有Host wire的additive local consumer，不修改`29317b...`或producer。Owner接受closure并单独授权S7B Rust application orchestration；G3保持Partial，Vue UI/S8仍未授权 | 段成威 | Accepted 2026-08-03 / S7A Closure Passed / S7B Authorized |
| DEC-126-028 | S7B Desktop Rust Application Orchestration/Domain Closure Review | 接受S7B并保持G3 Partial / 退回指定Rust P1 / 扩大到Vue UI或feature activation | **接受第一项**：采用SQLCipher schema v3 additive indexes与事务性session/message/outbox；create/turn幂等，outbox lease可恢复且最多16次，Host已接受turn后暂停自动重试，transport unknown outcome fail closed；严格event/stream/sequence reducer按批checkpoint并在terminal单事务提交assistant、reasoning、cursor与outbox；历史按turn稳定分页20/50并批量装配；model/fallback/user title采用CAS、人工标题永远优先、模型调用上限2。所有含正文/标题/项目/raw的Debug投影均redact | Desktop `make lint/test/build` PASS：113 TS tests；79 Rust tests中78 pass、1个既有signed Keychain integration ignored。覆盖10,000 ordered deltas、duplicate/gap/mixup、restart cursor、snapshot conflict、missing/incomplete reasoning、migration v1/v2、outbox expiry/recovery、title race，以及合成bookmark+fake TCP Host→SSE→SQLCipher完整Rust应用链；MiniMax/provider call为0。未新增Tauri command/invoke或Vue source，flags保持off，Host/Public Tasks wire与唯一candidate不变 | 段成威 | Accepted 2026-08-03 / S7B Closure Passed / G3 Partial |
| DEC-126-029 | Desktop private IPC/ViewModel contract与后续切片顺序 | 直接授权Vue/S8 / 一次性实现IPC+UI / 采用DESIGN-126-005并按S7C→S8A→S8B逐段授权 | **采用第三项**：接受DESIGN-126-005的private IPC v1。Rust生成并绑定短期`contextId`，WebView不提交owner identity且不接触Host bearer、SQLCipher key、canonical project path、Host/Runtime ID或原始wire；commands/responses/events/cursor/errors均closed/versioned，assistant/raw reasoning只以validated、capacity-bounded纯文本投影进入Vue。sequence gap、backpressure overflow、取消、stale selection、logout/tenant切换与进程重启统一fail closed/resync。先单独实现S7C Rust actions/delete/interrupt/coordinator，再实现S8A Tauri+TS store/view-model，最后实现S8B Vue/visual/a11y；生产链不得以mock UI替代 | 当前`ConversationApplication`无Tauri invoke/event，pin/delete/interrupt/restart orchestration不完整，TS也无conversation client/store。直接做Vue会把身份、重试、stream与删除语义推入不可信WebView或形成第二套状态机。私有IPC是Desktop-owned contract，不修改中央`yijie-contracts@29317b...`或Runtime pin。Owner已接受设计，并另行以LIA-126-003只授权S7C；S8A/S8B分别等待前置Closure | 段成威 | Accepted 2026-08-03 / DESIGN-126-005 Accepted / LIA-126-003 S7C Authorized / G3 Partial |
| DEC-126-030 | S7C Desktop Rust Actions/Coordinator Closure Review | 接受S7C并保持G3 Partial / 退回指定Rust P1 / 扩大到S8A或UI | **Owner接受第一项**：接受LIA-126-003 S7C。Rust侧使用300秒opaque authorization context、tenant/revision/capability fail-closed与authorized facade；session/project actions幂等且remove-vs-turn由单SQLCipher worker串行；interrupt和delete使用稳定operation ID；schema v4持久化cleanup job、独立Keychain receipt HMAC、delete/turn原子lease、restart recovery/background coordinator、级联删除+WAL checkpoint及30天content-free receipt；live/history assistant/raw只通过bounded redacted Rust projection source提供 | Desktop `make lint/test/build`全绿：113 TS，88 Rust中87 pass/1既有Keychain ignored。覆盖fake Host create/stream/cleanup、cleanup complete/incomplete typed domain、v1/v2/v3→v4、重复启动、restart、operation retry、delete-vs-turn race、cascade/FK/WAL、receipt expiry、auth revision/logout和raw no-log canary。Owner接受Closure并单独授权LIA-126-004/S8A，不自动授权S8B | 段成威 | Accepted 2026-08-03 / S7C Closure Passed / LIA-126-004 S8A Authorized / G3 Partial |
| DEC-126-031 | S8A Desktop IPC与TypeScript ViewModel Closure Review | 接受S8A并保持G3 Partial、另行评审S8B / 退回指定P1 / 扩大到Vue或feature activation | **Owner接受第一项**：接受LIA-126-004 S8A。Desktop注册20个versioned private commands与单一listen-only event channel；Rust从native auth绑定300秒opaque context、tenant/revision/capabilities及server-side cursors，command/event均复验；JSON Schema、serde和TypeScript runtime validators冻结closed request/response/event/error；生产client使用真实Tauri transport，Pinia采用单一authoritative reducer并对gap、overflow、取消、stale selection、tenant/logout、restart统一丢弃或resync | Desktop `make lint/test/build`全绿：127 TS；94 Rust中93 pass/1既有Keychain ignored。覆盖20/20 command ref和7/7 event variant、unknown field、UTF-8 byte caps、authority expiry/revision/same-revision rebind、newest tenant bind、duplicate/out-of-order/backpressure、read cancel、A→B late response、restart cleanup resync、delete/interrupt race。secret/path/raw-wire/no-log扫描与Vue目录diff扫描PASS；Host/Public Tasks wire、contracts/Runtime pin、flags、MiniMax和远端均未改。S8B仍需单独授权 | 段成威 | Accepted 2026-08-03 / S8A Closure Passed / G3 Partial；不授权S8B |
| DEC-126-032 | S8B0 UI Integration Readiness与private IPC停止条件 | A. 让Vue复用裸start command并从错误猜ready；B. 直接做完整S8B页面；C. 接受DESIGN-126-006并先单独实现default-off S8B0 integration | **Owner接受C**：冻结exact-true/default-false的`VITE_YIJIE_CHAT_LOCAL_UI_ENABLED`，route/capability/deep-link、permission bind/dispose、Pinia project/paging/cleanup、Tasks真实metadata/default-off和48/160滚动契约。新增`chat_get_local_readiness_v1`与`chat_request_local_recovery_v1` closed commands；Rust独占process start/retry；新增content-free storage issue/recovery codes及schema/serde/TS fixtures；现有20 commands与7 events不静默改义 | Owner在接受本决定后另行给出LIA-126-005，只授权S8B0 source；S8B0不做完整Vue视觉页面。S8B、S9、S10、S11继续逐切审批；flag始终off | 段成威 | **Accepted 2026-08-03 / LIA-126-005 S8B0 Authorized / G3 Partial**；不授权S8B |
| DEC-126-033 | S8B0 Closure Review | 接受S8B0并保持G3 Partial、另行评审S8B / 退回指定P1 / 扩大到完整Vue UI或activation | **Owner接受第一项**：本地checkpoint`yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85`实现exact-off gate、受保护`/chat`/`/chat/:sessionId`/Tasks route与lazy loader、permission→chat dispose-before-bind lifecycle、authoritative store project/paging/readiness/cleanup navigation、真实session metadata Tasks接线，以及Rust-owned closed readiness/recovery/storage probe。private IPC命令由20增至22，既有20个命令语义和7个event variants不变 | Desktop 135/135 TS、95/95 Rust（另1既有Keychain ignored）、generate/lint/type/build/fmt/clippy全绿；read-only/full/corrupt/migration、auth/expiry/race、default-off loader、send readiness、paging dedupe、delete disposition和no-log边界有证据。未修改完整Chat Vue页面/视觉样式，未启用flag，未调用MiniMax，未改central contract/Host/Runtime pin，未远端写入。接受本Closure不自动授权S8B | 段成威 | **Accepted 2026-08-03 / S8B0 Closure Passed / G3 Partial**；S8B仍未授权 |
| DEC-126-034 | S8B Vue UI Closure Review | A. 接受S8B并保持G3 Partial、之后单独评审S9；B. 退回指定Vue/a11y P1；C. 扩大到flag activation、MiniMax或四组件E2E | **Owner采用A**：接受LIA-126-006本地checkpoint`yijie-desktop@35f27447398529cca4dec85fa1f67e779c7a7cbd`的真实`/chat`/`/chat/:sessionId`页面、App Shell项目/session树、纯文本composer、assistant/raw reasoning、session/project菜单、delete/cleanup closed navigation、48/160滚动与production-grade light/dark/a11y；继续保持flag off和G3 Partial | 29/29个TS测试文件、164/164 tests、axe 0 serious/critical、Vite production build、Rust 95/95（另1既有ignored）、npm audit 0 known vulnerabilities；浏览器1180×760 light/dark、200% zoom等价视口、permission/delete焦点恢复和plaintext DOM检查PASS。无IPC/Rust/contracts/Host/Runtime/MiniMax/远端变化。VoiceOver人工清单已提供但不伪称已人工执行，保留到S11/G6 | 段成威 | **Accepted 2026-08-03 / S8B Closure Passed / G3 Partial**；不自动授权S9/S10/activation |
| DEC-126-035 | Owner授权push后的Remote State Reconciliation | A. 将远端可达误写为merge/release完成；B. 回退已授权push；C. 只登记精确remote refs/clean clones并保持全部Gate与activation边界 | **Owner接受C**：登记yijie/API/Host/Desktop accepted checkpoints及sole contracts candidate；五仓候选/develop refs和临时clean clone均精确PASS | 远端可达只提高检出/审计能力；不改变`origin/develop`、Draft PR #1、candidate identity、G3/G4/G6、flags、merge/tag/publish/deploy | 段成威 | **Accepted 2026-08-04**；另行授权LIA-126-007/S9，不授权S10–S11 |
| DEC-126-036 | LIA-126-007 / S9 fake-provider Eval Closure Review | A. 接受S9并保持G3 Partial、之后单独评审S10；B. 退回指定Eval P1；C. 扩大到MiniMax/flag/四组件E2E | **Owner接受A**：接受Host唯一版本化authority、250条锁定合成dataset、title/raw逐指标PASS，以及Desktop exact fixture→reducer→SQLCipher→restart/history/delete→plaintext Vue链；接受两个仅本地checkpoint，保持所有production source/wire/flags不变 | 摘要锁、逐仓全量门禁与no-log/bundle证据均通过；一次既有cleanup test跨秒波动已由单测和第二次full rerun归类，不在S9 diff。S9不能替代S10多进程E2E | 段成威 | **Accepted 2026-08-04**；G3 Partial，不授权S10 |
| DEC-126-037 | S10A Local E2E readiness与LIA-126-008是否可授权 | A. 忽略缺口直接启动S10B；B. 用S9 runner/独立curl/单仓fixture代替四组件；C. 接受DESIGN-126-007但HOLD S10B，先关闭test-profile/chain缺口 | **Owner接受C**：Compose v2缺失；Host只能以硬编码MiniMax配置启动可创建thread的Runtime；Desktop sidecar清空env并强制raw/title/cleanup=false、丢弃child输出；Chat/native-auth Keychain namespace固定；Desktop实际未消费Public Tasks `/v2/tasks`。因此LIA-126-008保持Blocked Draft，先单独设计S10P corrective与环境准备 | 上述缺口分别触发用户冻结的environment、provider config、private deployment interface、secure-storage与production orchestration停止条件。直接启动要么会调MiniMax/碰真实Keychain，要么只能得到虚假的“已开flag”或空Tasks表证据。HOLD不回退S4–S9 Closure、G2/G2A或Local-only战略 | 段成威 | **Accepted 2026-08-04 / Option C / HOLD**；S10B未授权 |
| DEC-126-038 | S10P0 corrective的唯一实施路径与Public Task删除限制 | A. 安装独立Compose v2、保持Public Tasks独立；B. 修复Docker Desktop自带Compose发现链，按S10E→S10P1→S10P2→S10P3单独授权；C. 复用已有DB/Keychain并用curl补证据 | **Owner接受B与DESIGN-126-008**：S10E只修复当前用户的stale Compose plugin link，固定Docker Desktop内置Compose v5.3.0及SHA-256，并使用独立、digest-pinned PostgreSQL/Keycloak/Caddy profile；S10P1增加exact-true/loopback-only fake Responses与Desktop child allowlist；S10P2以canonical run UUID派生test-only Keychain/app-data namespace；S10P3使Desktop在Host start前先幂等创建content-free Public Task，持久化local session/public task/Host operation mapping。为稳定展示control-plane pending/denied/retry/failed，采用新的Desktop-private closed command/channel schema | 本机Docker Desktop已包含可执行Compose v5.3.0，故缺口是失效symlink而非缺少二进制；Docker官方说明v5与v2在`docker compose`下功能等价。Owner同时接受删除边界：session删除只删Desktop/Host/Runtime及本地mapping，PostgreSQL中content-free Public Task行保留；不得静默扩展`29317b...`。本批准仅冻结设计，不授权任何corrective实现 | 段成威 | **Accepted 2026-08-04 / Option B**；S10E/S10P1/P2/P3/S10B仍未授权 |
| DEC-126-039 | 单独授权的S10E Compose/Isolated Identity Environment Closure Review | A. 接受S10E Closure并仅关闭BLK-001；B. 指定Infra/identity/migration/cleanup P1后退回；C. 把接受扩大为S10P1或S10B授权 | **Owner接受A**：接受本地Infra checkpoint `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf`、可恢复Compose discovery修复、exact-digest/default-off profile、隔离API/Keycloak数据库、synthetic identity、public-CA-only TLS、API migration v4、runtime/no-secret-log与停止后清理证据 | 初始诊断run因合成DB credential被展开到process output而判无效并停止；最终fresh run重新生成全部合格证据。当前零S10E容器/网络/listener；八个project-scoped named volumes及两个owner-only ignored run root按未授权删除边界保留，污染run由`REJECTED` marker强制fail closed。接受只关闭BLK-001，不改变G3 Partial、LIA-126-008 HOLD、flags、S10P1/P2/P3/S10B/S11或远端/发布边界 | 段成威 | **Accepted 2026-08-04 / Option A / S10E Closure Passed / BLK-001 Closed**；不授权S10P1或S10B |
| DEC-126-040 | LIA-126-009 / S10P1 Host Fake Provider与Desktop Child Test Profile Closure Review | A. 接受本地S10P1 Closure并关闭BLK-002/003；B. 指定Host/Desktop P1后退回；C. 将接受扩大到S10P2或S10B | **Owner接受A**：接受Host `e0a8d3d29a335571d1654d95e1e262c240755674`与Desktop `fba934c524852719904657d0a4155142040e7285`本地checkpoint。Host仅在exact master+canonical run ID+fixed loopback同时成立时生成keyless Responses配置，并以S9 fixture authority提供complete/incomplete/error注入；Desktop保留`env_clear()`并只传closed child allowlist，raw/cleanup=true、title=false，owner-only日志有256 KiB上限，spawn前content-free evidence、父进程watchdog、PID/run ID/nonce/readiness与crash/restart均fail closed | 固定Runtime的assistant/raw实际流式测试、真实Desktop→Host→固定Runtime child启动、Host race/coverage、Desktop 165 TS + 101 Rust（1既有Keychain ignored）、lint/build/no-log均PASS；MiniMax/external/Keychain/real-data/remote write均0。没有修改private IPC、central contracts、Host/Public Tasks wire、DB schema或Runtime pin。Owner正式关闭BLK-002/003；BLK-004/005和S10B HOLD不变，本决定不授权S10P2/P3/S10B | 段成威 | **Accepted 2026-08-04 / Option A / S10P1 Closure Passed / BLK-002/003 Closed**；不得进入S10P2/P3/S10B |
| DEC-126-041 | LIA-126-010 / S10P2 Test-only Secure Storage Closure Review | A. 接受实现并关闭BLK-004；B. 接受本地实现checkpoint但保持Closure HOLD，待Apple Development signed bundle完成三条Protected Data Keychain读写删；C. 用普通文件、默认Keychain或mock inventory豁免原生证据 | **Owner接受B**：接受Desktop `c863b2ab30d185201bff5736a308d7078ee5dc68`的独立exact-true secure-storage gate、canonical run manifest、三条run-derived service/account、native-auth无legacy entry、Chat app-data/Host Home/CODEX_HOME/project同run绑定、exact attribute-only inventory、crash/retry/manifest-mismatch/cross-run与精确cleanup；公共wire、SQLCipher schema、private IPC、TS/Vue、contracts与Runtime pin均未改；接受不等于S10P2 Closure Passed | 仓内12项S10P2测试、Desktop 165 TS + 113 Rust、lint/build/clippy与default-off/no-log通过；原生probe的pre/post inventory均absent且临时root已清理，但写入返回`A required entitlement isn't present`。批准后签名准备复核确认bundle=`com.yijie.ai`、0 valid signing identities、0 installed provisioning profiles、无可用Xcode自动签名环境；Team/ApplicationIdentifierPrefix不可凭空构造，故未增加Keychain写入。`pnpm audit`的既有dev-tool公告仍独立处理 | 段成威 | **Accepted 2026-08-04 / Option B / SOURCE CHECKPOINT ACCEPTED, CLOSURE HOLD / BLK-004 OPEN**；只允许准备匹配签名材料并重跑native matrix，不授权S10P3/S10B |
| DEC-126-042 | Local-only S10是否继续以Apple signed Protected Data证明阻断本地E2E | A. **推荐**：只为double-exact S10 test profile增加run-scoped ephemeral file secret backend，并把signed Keychain移为Deferred Native Hardening；B. 维持DEC-126-041并安装Xcode/签名材料；C. 使用legacy/default Keychain、固定/run-ID派生/env secret或mock绕过 | **Owner正式接受A**：Local-only目标是隔离Docker依赖加宿主机Desktop/Host/Runtime的合成E2E，不是签名发布。backend只保存Chat SQLCipher、receipt HMAC、native-auth三个随机合成secret；canonical run UUID、0700 root、0600 create-new/O_EXCL/O_NOFOLLOW文件、owner/nlink/canonical校验、同run重启恢复、cross-run隔离、manifest-bound精确cleanup；production/default仍只允许Protected Data Keychain | `contract-impact=semantic`（Desktop-private local-test storage/deployment semantics与BLK-004退出条件）；central G2A=N/A，因为HTTP/SSE/IPC、contracts、SQLCipher业务schema、API/Host/Runtime与production/default均不变。DEC-126-041作为历史Accepted/source checkpoint保留；Local-only BLK-004退出改为S10P2F Closure。不得把文件backend写成生产安全或native Keychain PASS | 段成威 | **Accepted 2026-08-04 / Option A / SECURITY-G2 DESIGN ACCEPTED**；当时不授权S10P2F，后来DEC-126-043接受其Closure并关闭BLK-004；仍不授权S10P3/S10B |
| DEC-126-043 | LIA-126-011 / S10P2F Local-only Ephemeral Secret Backend Closure Review | A. **推荐**：接受Desktop `46107eec1e9cba0257252cae8678a4233ef20036`及S10P2F-001–012证据，仅关闭Local-only BLK-004；B. 指定S10P2F范围内P1并退回；C. 扩大为S10P3/S10B授权或把native hardening写成PASS | **Owner接受A**：double-exact selector、schema-v2 closed manifest、三个固定role的OS CSPRNG secret、0700/0600、create-new/O_EXCL/O_NOFOLLOW、owner/mode/nlink/inode/device/canonical/role/length、same-run SQLCipher/native-auth恢复、cross-run/lease/fault fail-closed和exact non-recursive cleanup均已实现；production/default Protected Data与manifest v1不变 | 19/20 targeted通过（1项signed native ignored）；全量Rust 124 pass/2 signed-native ignored；TS 165、generate/lint/build、fmt/check/clippy、RustSec/no-log/bundle/diff均通过。0 Keychain/MiniMax/真实数据/远端写入；Apple signed证明仍`Deferred Native Hardening / NOT RUN`。`pnpm audit --prod`一项既有moderate PostCSS与17项允许的既有RustSec warning独立登记，不是本Rust slice新增P1 | 段成威 | **Accepted 2026-08-04 / Option A / S10P2F Closure Passed / Local-only BLK-004 Closed**；不授权S10P3/S10B/S11 |
| DEC-126-044 | LIA-126-012真实Desktop→Public Tasks链因OIDC `nbf`不兼容而停止后如何继续 | A. **推荐**：单独评审并修正S10E Keycloak token profile，使标准Authorization Code + PKCE access token生成numeric `nbf`，保持API verifier不变；B. 放宽API必需`nbf`；C. 用手工签名bearer、mock signer或curl绕过真实native flow | **Owner接受A并单独授权S10I**：保持API `iss/sub/aud/iat/nbf/exp` required-claim verifier不变；只在本地S10E Desktop public client用Keycloak内置user-session-note mapper把numeric `AUTH_TIME`投影为access-token `nbf`；禁止静态`nbf=0`、script mapper、手工bearer、mock signer和curl替代 | Infra `8d7c84dc963141931c6c5d3c3aded3218247df0b`提供static/live mapper conformance；fresh S10E run的标准Authorization Code + PKCE token含numeric `nbf`，真实Desktop Rust authority完成capability、Public create/bind、本地delete并保留content-free Public row。API/contract/Host/Runtime pin均未改 | 段成威 | **Accepted 2026-08-04 / Option A / S10I Executed / S10P3-BLK-001 Resolved in evidence**；不授权S10B |
| DEC-126-045 | LIA-126-012 / S10P3 Closure Review | A. **推荐**：接受Desktop/Infra本地checkpoint与真实identity/Public Tasks证据，仅关闭BLK-005；B. 指定S10P3范围内P1并退回；C. 扩大到S10B/S11/activation/remote write | **采用A**：接受Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Infra `8d7c84dc963141931c6c5d3c3aded3218247df0b`、unchanged API verifier、standard native OIDC numeric `nbf`、Public-bind-before-Host、本地删除/Public row保留及PostgreSQL/audit正文/路径零命中 | fresh run `90dc0dd9-140d-4ec0-b918-e24faab98aeb`完成后API与四个隔离容器/网络已停止，named volumes按既定边界保留。MiniMax、Keychain、真实数据、默认flag、远端写入均为0；central G2A N/A。仅关闭BLK-005并接受S10P3 Closure，G3继续Partial，S10B继续HOLD | 段成威 | **Accepted 2026-08-05 / Option A / S10P3 Closure Passed / S10A-BLK-005 Closed**；不自动授权LIA-126-008/S10B、S11、MiniMax、activation或远端写入 |
| DEC-126-046 | LIA-126-008 / S10B首次正式执行在bootstrap前置失败后的处置 | A. **推荐**：接受fail-closed执行事实并登记`S10B-BLK-001`，单独设计/授权一个与`yijie_api_feat126_s10`匹配的closed synthetic bootstrap profile后重跑同一完整矩阵；B. 省略`BOOTSTRAP_PROFILE`使用generic lane；C. 手工建`feat125`数据库/插入授权或复用旧run volume | **Owner接受A**：run `9b9d455f-0500-4dd0-a008-d5a862bf6f20`的exact-digest依赖、TLS/OIDC、2个synthetic users、API migration v4均通过；但权威Infra DB固定为`yijie_api_feat126_s10`，API `feat-125-local-lab` profile在数据库访问前只接受`yijie_api_feat125_local`，四份tracked manifest因此全部fail closed。未使用generic profile、手工状态或旧volume绕过 | 数据库复核为migration=4、users/tenants/memberships=`0/0/0`；API/Desktop/Host/fake/Runtime未启动，S10B-001 FAIL、002–012 NOT RUN。容器/网络已停止，临时binary root已删除，4个project-scoped volumes和owner-only ignored run record按既定边界保留。0 MiniMax/Keychain/真实数据/默认flag/远端写入 | 段成威 | **Accepted 2026-08-05 / Option A / S10B CLOSURE REJECTED**；当时S10B-BLK-001 Open，后来由DEC-126-048关闭；仍不授权rerun或S11 |
| DEC-126-047 | S10B-BLK-001应采用何种closed synthetic bootstrap纠偏 | A. **推荐**：新增`feat-126-s10-local-lab`，精确绑定`YIJIE_ENV=nonproduction`、issuer与`127.0.0.1:5432/yijie_api_feat126_s10?sslmode=disable`，复用现有四份reviewed manifests；由Infra无参数选择地调用；B. 放宽`feat-125-local-lab`数据库规则或通用profile；C. 手工SQL、caller-selected manifest/profile或旧volume fallback | **Owner接受A**：DESIGN-126-009证明API已按profile→manifest→migration/DB顺序fail closed；新profile只增加FEAT-126本地deployment/security authority，现有`feat-125-local-lab`、generic compatibility lane与四份manifest字节均不变。Infra入口内部固定profile和四条显式路径，缺失/generic/wrong authority在CLI或DB前拒绝 | central contract impact=`none`，G2A N/A。S10BP1须在fresh migration v4数据库验证2 users/2 identities/2 tenants/4 memberships/4 assignments、重复执行8条content-free audit、rollback无partial state、feat125全回归和secret/DSN/token日志0命中 | 段成威 | **Accepted 2026-08-05 / Option A / DESIGN-126-009 Accepted / LIA-126-013 NOT AUTHORIZED**；不得实现、启动服务、重跑S10B或进入S11 |
| DEC-126-048 | LIA-126-013 / S10BP1 Closure Review | A. **推荐**：接受bootstrap纠偏、关闭`S10B-BLK-001`，同时登记独立`S10B-BLK-002`并继续禁止rerun；B. 指定S10BP1范围内P1退回；C. 把本验证直接写成S10B/G4 PASS | **Owner接受A**：API exact profile/ordered matrix/atomic batch/closed verifier与Infra fixed-SHA/four-path/two-pass权威入口完成；feat125/generic/manifest/central wire/schema/verifier未改。Fresh DB因既有S10E `docker image inspect tag@digest`在Docker 29.6.1曾拒绝已存在exact digest，改以同一pinned image ID启动单一临时PostgreSQL；未修改S10E脚本 | API全量与fresh-v4 exact matrix/atomic rollback PASS；Infra 83/83和security gates PASS；临时资源清理。Bootstrap slice P1=0；image-reference precheck作为独立future S10B环境P1保留 | 段成威 | **Accepted 2026-08-05 / Option A / S10BP1 Closure Passed / S10B-BLK-001 Closed**；S10B-BLK-002仍Open，不授权rerun/S11 |
| DEC-126-049 | S10B-BLK-002 的本地immutable-image availability应如何兼容Docker 29状态敏感引用索引 | A. **采用**：保留Compose唯一`version-tag@digest`authority，preflight从其派生唯一`repository@digest`并核验本地RepoDigests/descriptor，随后仍以`--pull never`启动；B. 删除preflight只依赖Compose；C. floating tag、自动pull或手工image ID | **Owner本次“单独评审并修复”授权采用A**：`repository@digest`是稳定内容身份，version tag继续保留可读版本语义；verifier只读取现有`FEAT_126_S10_IMAGES`，不复制第二套pin，不输出inspect原文，不调用pull | 复验确认本机三个exact digest存在；Docker重启后原`tag@digest` lookup恢复，证明问题是状态敏感而非镜像缺失。方案A同时覆盖失败与恢复状态，保持digest/no-pull/fail-closed。contract impact=`none`，仅local Infra deployment/security helper | 段成威 | **Accepted 2026-08-05 / Option A / DESIGN-126-010**；只授权BLK-002 corrective，不授权S10B rerun/S11 |
| DEC-126-050 | S10B-BLK-002 Corrective Closure Review | A. **推荐**：接受exact repository-digest verifier、自动化负向矩阵与一次fresh no-pull四依赖启动/停止证据，关闭BLK-002；B. 指定Infra P1退回；C. 将验证扩展为S10B/G4 PASS | **Owner接受A**：新增test-only/local Infra verifier并由accepted helper调用；malformed/conflicting/missing/mismatch/descriptor drift均fail closed；无floating tag、pull、volume delete或Compose pin变化 | Infra 85/85测试、validate/shell/diff与live verifier PASS；fresh run `ae1c892a-4819-40bc-9ce9-d72f6ea2fcd7`在`--pull never`下四服务healthy，随后容器/网络清零，四个run volumes和owner-only ignored record按边界保留。未启动API/Desktop/Host/Runtime，不是S10B重跑 | 段成威 | **Accepted 2026-08-05 / Option A / S10BR1 Closure Passed / S10B-BLK-002 Closed**；G3 Partial、G4/G6 Pending；不授权S10B rerun/S11 |
| DEC-126-051 | LIA-126-014 / S10B-R2 preflight failure处置 | A. **采用**：接受fail-closed事实、不接受S10B-R2 Closure，保持`S10B-BLK-003` Open；单独纠正migration/bootstrap显式完整API SHA authority后再申请rerun；B. 直接把wrapper硬编码更新到当前API SHA；C. 绕过wrapper、退回旧API或直接运行migration | Owner采用A。Infra accepted migration wrapper仍硬编码旧API `a64f9f...`，而本轮closed bootstrap候选必须为`c5f334e...`；wrapper在secret、run目录、Docker和数据库访问前拒绝。B会在下一候选再次漂移；C破坏clean/exact authority与no-bypass边界 | fresh run `4ffa07b9-6e4c-45d4-b5d5-3b3be5d7d818`仅执行migration preflight即返回`unexpected yijie-api commit`；run root、container、network、volume、API/Desktop/Host/fake/Runtime均为0。未现场修复或重跑 | 段成威 | **Accepted 2026-08-05 / Option A / fail-closed fact accepted / S10B-R2 Closure Rejected**；其历史BLK-003随后由DEC-126-052关闭；不授权S11 |
| DEC-126-052 | LIA-126-015 / S10BM1 API Candidate Authority Corrective Closure Review | A. **采用**：接受共享run-scoped完整API SHA authority、兼容性披露、87/87门禁与Infra本地checkpoint，关闭`S10B-BLK-003`，但不把corrective写成S10B证据；B. 指定Infra P1退回；C. 直接授权S10B rerun/S11 | Owner采用A。migration与bootstrap调用同一authority helper；canonical run root中以create-new/O_EXCL/O_NOFOLLOW创建0600 closed document，仅含schema version、run ID和full API commit。旧migration两参数调用有意fail closed，Make caller/runbook同步更新；missing/short/wrong/dirty/drift/corrupt/mode/owner/symlink/hardlink均在secret/DB前拒绝 | Infra `bb96333df908d6fea72ec0a1f57a64477c2428e4`；validate/lint/test全绿、87/87，Node/shell/diff PASS；无container/service/secret/DB/API/Desktop/Host/Runtime/model/Keychain/remote动作。private local helper为breaking；central contract/wire/schema/default/G2A none | 段成威 | **Accepted 2026-08-05 / Option A / S10BM1 Closure Passed / S10B-BLK-003 Closed**；不自动授权rerun/S11 |
| DEC-126-053 | LIA-126-016 / S10B-R3 immutable-image preflight failure处置 | A. **采用**：接受本次fail-closed事实、不接受S10B-R3 Closure，保持`S10B-BLK-004` Open并单独评审Docker execution capability与immutable resolver；B. 现场pull/retag或重启Docker后直接重跑；C. 绕过verifier或放宽`--pull never` | **Owner接受A并校正根因**：现有证据不支持“Docker 29.6.1永久无法inspect `repository@digest`”。已确认accepted verifier把Docker CLI缺失、socket/daemon不可达、permission denied、image missing和reference resolver错误全部压成同一`image unavailable`；Docker capability可用时正确PostgreSQL pin曾只读重复解析成功。containerd reference metadata状态仍是待复验因素，不写成已确认Docker bug | run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5`仍在任何container创建前停止；S10B-001 FAIL、002–012 NOT RUN；owner-only `REJECTED`、exact stop、container/network/volume/listener=0；ignored run root/secret record保留。失败事实与根因分类分离 | 段成威 | **Accepted 2026-08-05 / Option A / S10B-R3 Closure Rejected / S10B-BLK-004 Open**；只授权S10BD0设计，不授权纠偏、重跑、S11或远端动作 |
| DEC-126-054 | S10B-BLK-004应如何关闭Docker capability与immutable image resolver假阴性 | A. **采用**：先做同进程Docker capability probe，再按closed/content-free failure class执行原始Compose `version-tag@digest`身份校验，并以单独授权、可精确清理的`docker create --pull=never`验证实际resolver；B. 只增加重试/重启Docker；C. 删除preflight或允许pull/floating tag | **Owner接受A**。capability失败时禁止下结论为image missing；capability成功后要求exact Id、Descriptor digest、RepoDigests、repository、OS/architecture。runtime probe只创建不启动、使用run-scoped name/label、`--network none`并以tmpfs覆盖image声明volume，unknown outcome先reconcile再精确清理；不得删除非本probe资源。B掩盖状态问题，C削弱immutable/no-network边界 | S10BD0文档本身`contract-impact=none`；拟议S10BD1改变local verifier失败/顺序和增加test-only probe，属于local deployment-interface `semantic`，central contracts/G2A=`N/A`。Owner随后单独批准LIA-126-017，但明确本轮不得自动开始实施；Closure后仍需clean Infra/Governance checkpoint和新的S10B-R4授权 | 段成威 | **Accepted 2026-08-05 / Option A / DESIGN-126-011 Accepted / LIA-126-017 Approved-Held-Not-Started / S10B-BLK-004 Open** |
| DEC-126-055 | 是否接受LIA-126-017 / S10BD1 Closure并关闭S10B-BLK-004 | A. **采用**：接受exact-clean实现、S10BD1-001–012、全量Infra与exact-commit live resolver证据，关闭BLK-004；B. Hold并要求额外content-free证据但不改候选；C. 拒绝Closure并保持blocker | **Owner接受A**。Infra `2a643caef210e32cab80242ede46b96927b2097a`对原始Compose pin完成capability-first分类、Id/Descriptor/RepoDigests/repository/platform校验与受控no-start resolver；live run验证3个identity/3个probe，后置container/running/network/volume均0，Docker恢复执行前停止状态 | 只改变private local deployment verifier的语义；central contracts、wire、业务schema、Runtime pin、production/default均不变，G2A N/A。接受只关闭BLK-004，不能自动进入S10B-R4 | 段成威 | **Accepted 2026-08-05 / Option A / S10BD1 Closure Passed / S10B-BLK-004 Closed / S10B-R4 Unauthorized** |
| DEC-126-056 | LIA-126-018 / S10B-R4在fake-provider readiness fixture身份不一致后的处置 | A. **采用**：接受fail-closed事实、不接受S10B-R4 Closure、保持新`S10B-BLK-005` Open，并另行实现单一machine-readable fixture/orchestrator authority；B. 把header改为`normal-000`并继续同一run；C. 放宽/删除fixture identity校验 | **Owner接受A并单独授权LIA-126-019/S10BF1**。R4的正确run ID与错误case identity被fake server 403拒绝；不得现场改header或续跑。S10BF1仅允许Host-owned探针与Infra单一preflight runner，不授权S10B-R5 | R4 run `96a0a80d…c4c`的失败和清理事实保持不变；S10BF1候选见DEC-126-057。contract-impact对R4记录为`none`，对corrective为private test/deployment tooling `semantic`，central G2A=N/A | 段成威 | **Accepted 2026-08-05 / Option A / S10B-R4 Closure Rejected / LIA-126-019 Authorized and Consumed / S10B-BLK-005 Open** |
| DEC-126-057 | 是否接受LIA-126-019 / S10BF1 Closure并关闭S10B-BLK-005 | A. **采用**：接受Host-owned authority/probe、Infra唯一runner、S10B-001组合预检及清理证据，关闭BLK-005；B. 指定S10BF1 P1退回；C. 把本次corrective冒充S10B-R5/G4 PASS | Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`把health/probe字段明确拆成`dataset_id`与`fixture_case_id`，探针内部生成header且拒绝endpoint/identity漂移；Infra `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`只有一个runner，不接受dataset/fixture输入 | fresh run `ed22fc82-4837-4a3e-a60e-7f7c8ab6f3f4`通过七仓SHA、resolver、依赖、TLS/OIDC、identity、migration/bootstrap、API health/ready、Host-owned fake readiness与secret scan；summary SHA-256=`8198442e…f7d9`；API/fake/container/network/listener=0，4 volumes按边界保留，Docker恢复停止，`s10b_r5_executed=false` | 段成威 | **Accepted 2026-08-05 / Option A / S10BF1 Closure Passed / S10B-BLK-005 Closed / S10B-R5 separately unauthorized** |
| DEC-126-058 | LIA-126-020 / S10B-R5 runtime-profile authority失败处置 | A. **采用**：接受fail-closed事实、不接受R5 Closure、保持`S10B-BLK-006 Open`，单独建立closed FEAT-126 API runtime profile及preflight/continuation共享authority；B. 复用FEAT-125 profile；C. 放宽profile校验 | **Owner以最新明确执行指令接受A并单独授权/消费LIA-126-021/S10BRP1**：API必须正式增加closed `feat-126-s10-local-lab`；Infra preflight与后续完整链必须消费同一machine-readable authority，不能只替换字符串、shell重建或绕过校验 | R5历史保持S10B-001 PASS、002 fail closed、003–012 NOT RUN；该接受只授权corrective，不是fresh rerun。纠偏属于private local deployment `semantic`，central contracts/wire/schema/Runtime pin无影响，G2A N/A | 段成威 | **Accepted 2026-08-06 / Option A / R5 Closure Rejected / LIA-126-021 Authorized and Consumed / S10B-BLK-006 Open** |
| DEC-126-059 | LIA-126-021 / S10BRP1 Closed API Runtime Profile Authority Closure Review | A. **采用**：接受API/Infra候选与仓内验证，关闭BLK-006并形成clean local checkpoints；B. 指定S10BRP1 P1退回；C. 把corrective直接写成S10B/G4 PASS | API正式支持专用profile并严格冻结nonproduction、双exact flag、专用DSN、issuer/JWKS、CA pin、canonical port、loopback、legacy v1隔离；FEAT-125行为不变。Infra以单一closed authority构建preflight child env，把authority与`api_binary_sha256`写入summary；唯一continuation launcher实际消费同run summary、reader、builder并复核fixed binary digest/identity，无operator override | **Owner接受A**。API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`为clean local checkpoints；API gates与Infra 113/113 PASS。Closure接受只关闭BLK-006，不是S10B-002–012或G4证据 | 段成威 | **Accepted 2026-08-06 / Option A / S10BRP1 Closure Passed / S10B-BLK-006 Closed**；Owner另行授权LIA-126-022/S10B-R6，但本轮未消费 |
| DEC-126-060 | LIA-126-022 / S10B-R6 image-resolver fail-closed处置 | A. **采用**：接受单次授权已消费和fail-closed事实，拒绝R6 Closure，保持`S10B-BLK-007 Open`；单独设计父preflight对子resolver closed class与content-free诊断证据的无损传播，之后再分别审批纠偏与fresh run；B. 以只读image inspect成功直接把S10B-001判PASS；C. 直接重跑resolver/R6 | R6七仓exact/clean与Docker capability通过；S10B-001在resolver返回`preflight_image_resolver_failed`后停止。事后只读检查证明三项冻结镜像的Id/Descriptor/RepoDigest/OS/arch精确匹配，但不能证明no-start create/validation/cleanup通过。现有父runner丢弃子进程closed stderr并只保留步骤级失败，无法区分`image_*`、`resolver_probe_failed`或`resolver_probe_cleanup_incomplete`，直接修复或重跑会绕过一次性停止条件 | run `28afba8b-573a-46ec-b9d1-8a635c7b9cf0`；S10B-001 FAIL、002–012 NOT RUN；container/network/volume/listener=0；owner-only run root保留2个ignored 0600文件，REJECTED SHA-256=`7c7c5f61d03614f41dec86fd051bda8668bebf208ff53349fe5535ba5f765e11`，secret→REJECTED hits=0。`contract-impact=none` for execution/governance；未来错误投影纠偏预计为private deployment-interface `semantic`、central G2A N/A | 段成威 | **Accepted 2026-08-06 / Option A / S10B-R6 Closure Rejected / S10B-BLK-007 Open**；不自动授权纠偏、fresh R7、S11或MiniMax |
| DEC-126-061 | DESIGN-126-013 / S10BEP0 resolver错误透传方案 | A. **采用**：child提供内部专用closed result v1，parent复用同源validator、严格校验并映射leaf class，同时落0600 content-free evidence；默认Make/human CLI保持；B. parent直接import resolver并捕获typed error；C. 抓取human stderr或直接重试 | Owner于2026-08-08以继续执行指令接受A，并单独授权/消费LIA-126-023。A保留真实child process/exit/output边界和唯一preflight，可复验12个leaf、phase/target/cleanup及old/new兼容；parent仍只接收run ID与七仓SHA，不增加operator override | Infra repository implementation、128/128 tests与static validate PASS；2026-08-09在Docker client/server 29.6.1、Compose 5.3.0及daemon access通过后，S10BEP1-014 canonical run `624bd64c…4657`完成3 identity/3 no-start probe、closed parent、no-log与资源归零，Infra/Governance门禁全绿，`s10b_r7_executed=false`。`contract-impact=semantic`仅限private local deployment interface；central G2A=N/A | 段成威 | **Accepted 2026-08-08 / Option A / LIA-126-023 Consumed / S10BEP1-014 PASS / Closure later accepted by DEC-126-062 / BLK-007 Closed** |
| DEC-126-062 | LIA-126-023 / S10BEP1 Corrective Closure Review | A. **采用**：接受repository corrective、S10BEP1-014 isolated live与全量Infra/Governance证据，关闭`S10B-BLK-007`；B. Hold并指定额外content-free证据；C. 拒绝Closure并保持blocker | **Owner明确接受A**。closed parent exact v1、3 identity/3 no-start probe、0600五字段evidence、no-log、三项exact image identity前后一致、container/network/volume/listener归零及所有门禁均PASS；决策登记后Governance default/strict/G2A/unique-key YAML/lint/test/shell/diff复跑PASS；`s10b_r7_executed=false` | 本决定仅接受corrective Closure并关闭BLK-007；`contract-impact=none` for governance disposition。G3保持Partial，G4/G6 Pending；不形成clean checkpoint，不授权fresh R7、S11、MiniMax、activation、真实数据、commit/push或其他远端写入 | 段成威 | **Accepted 2026-08-09 / Option A / S10BEP1 Corrective Closure Passed / S10B-BLK-007 Closed** |
| DEC-126-063 | DEC-126-062后Local Clean Checkpoint Closure | A. **采用**：仅在范围与门禁通过后形成Infra/Governance两个本地clean checkpoints；B. 保持dirty候选；C. 同时启动fresh R7 | **Owner明确采用A**。七仓候选范围/clean状态与冻结SHA复核通过；Infra validate、128/128、targeted 34/34、完整make lint/test、Compose semantic、Node/Shell/diff及Governance default/strict/G2A/YAML/lint/test/shell/diff均PASS | Infra checkpoint=`0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；Governance checkpoint为包含本决策的本地commit。仅授权这两个local commits，不授权push/远端动作或fresh R7；G3 Partial、G4/G6 Pending不变 | 段成威 | **Accepted 2026-08-09 / Local Clean Checkpoints Formed / Fresh R7 Not Authorized** |
| DEC-126-064 | LIA-126-024 / S10B-R7 Fail-closed Disposition | A. **采用**：接受单次授权已消费及S10B-001 PASS/S10B-002 fail-closed事实，拒绝R7 Closure，保持`S10B-BLK-008 Open`，先单独冻结完整四组件S10B-002–012权威orchestrator，再分别审批corrective与fresh R8；B. 以API-only continuation配合人工命令拼接继续本run；C. 把preflight PASS直接视为完整S10B/G4 PASS | R7固定七仓、Docker/Compose/daemon gate与唯一preflight均PASS；但Infra runbook明确唯一continuation“只启动API且不启动Compose或其他组件”，治理process manifest仍标记“冻结候选，当前不运行”，七仓没有单一可执行入口同时绑定Desktop/Host/Runtime/API、same-run manifest、case顺序、content-free evidence与cleanup。B/C都会绕过已批准的唯一authority和失败即停边界 | Owner接受A并只授权后续DESIGN-126-014只读设计评审。run `d553e6ea-e10f-4470-b357-a41807d6fb06`的S10B-001 PASS/002 FAIL-CLOSED/003–011 NOT RUN/012 abort subset事实保持；`s10b_r7_executed=true` | 段成威 | **Accepted 2026-08-09 / Option A / R7 Closure Rejected / S10B-BLK-008 Open / DESIGN-126-014 Review Authorized**；不授权corrective、fresh R8、S11、MiniMax、activation、commit或远端动作 |
| DEC-126-065 | DESIGN-126-014 Closed Four-component S10B Orchestrator | A. **推荐且已接受**：接受设计并授权`LIA-126-025/S10BO1`四仓repository corrective；B. 接受设计但继续HOLD implementation；C. 只在Infra拼装现有API launcher与人工Desktop命令 | 只读评审确认进程authority必须保持Infra→Desktop→Host→Runtime所有权链；现有Desktop没有真实Vue/Pinia/Tauri自动化入口，native auth/project picker不可确定自动驱动，Host没有Runtime child manifest/fake mode generation，API没有Tasks/audit/idempotency closed verifier。C仍会制造第二authority且无法证明case/evidence/cleanup | DESIGN-126-014冻结单一Make入口、仅run ID+七SHA输入、same-run preflight consumption、closed state machine、test-build-only Desktop driver/PKCE synthetic agent、API-owned verifier、Host-owned Runtime/fake证据、no-log与crash/reconcile/cleanup；已实施变更`semantic`仅限private local test/deployment与Desktop test IPC，central G2A=N/A | 段成威 | **Accepted 2026-08-09 / Option A / LIA-126-025 Corrective Closure Review Ready / Pending Owner Acceptance / S10B-BLK-008 Open**；不得自动isolated live、fresh R8、commit或远端动作 |
| DEC-126-066 | LIA-126-025 / S10BO1 Corrective Closure Acceptance | A. **Owner采用**：接受能力前置、四仓全量门禁、S10BO1-001–014与Governance证据，关闭`S10B-BLK-008`；B. Hold并要求额外repository evidence；C. 拒绝Closure | Docker client/server 29.6.1、Compose 5.3.0、daemon、loopback/native能力PASS；API/Host完整lint/race/build，Desktop 167 TS、129 Rust/3 ignored、default/feature clippy/build、driver 2/2与driver-absent，Infra validate/full lint/test/Compose semantic/142及S10BO1 14/14全部PASS | **Owner接受A**。只关闭orchestrator repository corrective blocker；不把repository Closure冒充fresh S10B-001–012、G4或G6。G3保持Partial，isolated live/fresh R8仍需独立授权 | 段成威 | **Accepted 2026-08-09 / S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed / G3 Partial / G4/G6 Pending** |
| DEC-126-067 | DEC-126-066后Local Clean Checkpoint Closure | A. **Owner采用**：全量门禁复验后仅形成API/Host/Desktop/Infra/Governance五个本地checkpoint；B. 直接isolated live；C. 直接fresh R8 | A把已接受corrective固化为可由后续精确SHA复验的clean source，同时保持Contracts/Runtime不变；B/C缺少单独一次性授权且越过当前checkpoint边界 | API `451940b2…f4c4`、Host `c5939b4d…59b9`、Desktop `d51e435c…7b6e`、Infra `0b05ab32…c25c`与包含本决定的Governance本地commit；所有pre-commit及post-update Governance门禁PASS，不push | 段成威 | **Accepted 2026-08-09 / Local Clean Checkpoints Formed / S10B-BLK-008 Closed / G3 Partial / G4/G6 Pending**；isolated live、fresh R8及远端动作未授权 |
| DEC-126-076 | DESIGN-126-019 / LIA-126-033 Corrective Closure Owner Acceptance | A. **Owner采用**：接受Desktop/Infra clean checkpoints、targeted/full gates、独立审查和Compose semantic证据，关闭environment-bound gap；B. Hold并要求额外repository evidence；C. 把repository证据冒充isolated-live PASS | Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`、Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`均clean/local/not pushed；Desktop TS `178/178`、Rust default `134/3 ignored`、feature `149/3 ignored`、targeted各`11/11` PASS；Infra targeted `50/50`、full `192/192` PASS；独立review无open P0/P1；Compose 5.3.0 direct config、Infra `make lint/test` `192/192` PASS且无lifecycle/live | **Owner明确采用A**。DESIGN-126-019 Complete；LIA-126-033 Corrective Closure Accepted；environment-bound Compose gap Closed。真实Tauri `AppHandle/setup` direct fixture仍为P2/live；G3 Partial、G4/G6 Pending；后续isolated-live必须基于新七仓精确SHA另行一次性授权 | 段成威 | **Accepted 2026-08-12 / Corrective Closure Accepted / G3 Partial / G4/G6 Pending / s10b_r8_executed=false** |

## 3. ADR 判定

- 是否改变既有 Accepted ADR：不削弱 ADR-0012；Accepted DEC-126-001 保留其 FEAT-126 安全责任。若未来改成迁号，必须重开 G1、形成新 Accepted ADR 并同步全部 FEAT-125 引用。
- 是否改变跨仓职责/数据权威：是。ADR-0013 已接受 Desktop embedded SQLite 为 confidential conversation authority，并明确 PostgreSQL/Redis/pgvector/bbolt 的非替代职责；ADR-0015 冻结隔离标题，ADR-0016/DEC-126-016 冻结 Host raw-reasoning展示与Desktop SQLCipher历史权威。DESIGN-126-003/DEC-126-017现已提交 exact v2/schema/caps候选；Public Tasks ownership/auth由DEC-126-011/012提交批准。
- 是否改变 Accepted Design Pattern：是。Chat 1.1.0 的 active state 要附件/右侧面板，App Shell 2.0.0 有全局收起；必须在代码前形成新候选版本并由段成威接受。
- ADR/Decision 结论：ADR-0013/0014/0015/0016与DEC-126-011/012/016–076均已Accepted；DESIGN-126-019 Complete，Owner已接受LIA-126-033 Corrective Closure并关闭environment-bound Compose gap；真实Tauri `AppHandle/setup` direct fixture保留为P2/live，G3 Partial、G4/G6 Pending。
- G2A/local 结论：`29317b6426578749dc698fc2ad32b986ee5c8e9f`仍是唯一source-contract candidate；远端候选/develop/Draft PR不变。该bootstrap deployment/profile缺口不改变central contract，G2A重审为N/A；S10BO3 Corrective Closure已接受，但完整fresh S10B仍未PASS；G3 Partial、G4/G6保持Pending，所有默认flags关闭，S11未授权。
- 架构 Owner：段成威。

## 4. 风险登记

| Risk ID | 风险事件/触发条件 | 概率 | 影响 | 预防控制 | 检测 | 恢复/回滚 | Owner | 残余风险 |
|---|---|---:|---:|---|---|---|---|---|
| R-126-001 | 纯 UI 上线但 legacy Tasks 仍匿名/可 IDOR | high | critical | 同 feature 保留 security track；routes/flags 默认隔离 | unauth/cross-tenant security E2E | 关闭 flags、保持 host+ingress 双隔离 | 段成威 | low after hardening |
| R-126-002 | UI permission entry 被误解为已授权写操作 | high | critical | fixed read-only/deny；服务端独立 check；清晰文案 | policy tamper/reverse request tests | 禁用入口/Host operations | 段成威 | low |
| R-126-003 | 跨 tenant/user 本地 history 闪现或被深链读取 | medium | critical | composite owner/tenant scope、切换先清空、command-level checks | account/tenant switch E2E | 锁 DB、清内存、禁用 history | 段成威 | low-medium |
| R-126-004 | SSE 重复/乱序/重启造成重复或缺失文本 | high | high | event ID/stream/sequence、transaction append、outbox、resume reconciliation | fault injection + DB assertions | 显示恢复态、重放/前向修复 | 段成威 | medium until history API |
| R-126-005 | 用户把应用功能删除误解为 Runtime/SSD/OS backup 的法证抹除 | high | critical | ADR-0014 限定成功文案；required live surfaces 全完成；排除 app backup/尽力排除 OS backup | restart/deep-link/DB+WAL+log canary 与 backup/uninstall 文案测试 | flag off、同 operation forward cleanup；披露不可控副本 | 段成威 | medium-high；Runtime WAL/log 与 OS/第三方备份不可由本功能保证 |
| R-126-006 | project path traversal/symlink race 越出选择目录 | medium | critical | native picker、canonical path、bookmark、open-time recheck、read-only | symlink/permission mutation tests | 撤销引用、要求重选 | 段成威 | low-medium |
| R-126-007 | raw reasoning复述prompt/项目片段/敏感信息，并扩散到日志、遥测、DB backup或错误投影 | high | critical | ADR-0016显式产品披露；只在versioned v2投影；纯文本渲染；日志/遥测/审计正文禁写；DEC-126-016要求SQLCipher+session FK cascade+backup限定披露；DESIGN-126-003限制16KiB delta/64KiB part/128KiB item/256KiB turn | raw-negative fixtures、secret canary、log/crash/DB/backup/delete scan、consumer conformance | 关闭reasoning flag；删除受控DB内容并checkpoint；不能承诺清除OS/SSD/backup痕迹 | 段成威 | high until G4 implementation/security evidence passes |
| R-126-008 | title generation prompt injection、超长/HTML 或无界费用 | medium | high | pathless ephemeral thread、untrusted delimiter、strict object schema、NFC/plain-text validation、人工标题优先、总调用 cap=2 | adversarial Eval + call count/ephemeral path assertions | deterministic fallback、disable title job | 段成威 | low after ADR-0015 approval/MiniMax validation |
| R-126-009 | 物理删除与 active stream 并发产生孤儿/复活 | medium | critical | stop→terminal→single DB transaction；FK cascade；writer lease | concurrency/fault tests | transaction rollback、repair orphan | 段成威 | low-medium |
| R-126-010 | local DB migration/磁盘满导致静默丢消息 | medium | high | versioned migrations、WAL/error checks、durable commit before UI success | disk-full/corrupt/read-only tests | fail closed、backup/forward repair | 段成威 | medium |
| R-126-011 | 同路径 Public API 硬切破坏未知 consumer | high | high | inventory + versioned expand + supported baseline checks | old/new conformance matrix | 保持旧 route 隔离/rollback flag | 段成威 | medium until inventory |
| R-126-012 | local/cloud 被误当“改配置”造成重复/丢失/冲突 | medium | high | storage port 只解耦实现；云同步另 feature/contract/migration | future migration rehearsal | 不启用 cloud adapter | 段成威 | low this feature |
| R-126-013 | sidecar/key/token 进入 WebView 或日志 | medium | critical | Tauri Rust owns token/child process；narrow commands；no URL/storage | secret canary/log scan | shutdown Host、rotate local token/key | 段成威 | low-medium |
| R-126-014 | 需求过大导致 UI 与安全跨仓同时硬切 | high | high | contract-first DAG、small slices、independent flags、G2A | slice diff/gate review | stop at last safe flag-off slice | 段成威 | medium |
| R-126-015 | 把“候选未引入依赖变化”误当成可以忽略远端audit红灯 | medium | high | 必需CI不得豁免；固定PR/SHA；依赖修复使用新候选并重跑完整门禁 | PR check conclusion、audit advisory、head SHA与skip steps核对 | 保持Draft、不merge；修复后重新确认candidate和merge批准 | 段成威 | low only after green full CI and Owner approval |
| R-126-016 | 把Local Runtime Ready或Local-only G6误写成Production Ready/已发布 | medium | critical | DEC-126-022明确G5 N/A、无tag/publish/deploy；UI/服务flags仅本机合成环境；未来上线必须重开生产轨 | gate文案、artifact/tag/registry/infra检查、Owner本地验收记录 | 保持无生产路由/凭据/真实数据；撤销错误声明并重开G5 | 段成威 | low while local-only boundary is enforced |
| R-126-017 | Public Tasks arbitrary `input`使conversation正文进入PostgreSQL或response | high | critical | DEC-126-023方案C；closed contract schema/fixture与ADR-0013同向；provider/consumer conformance；route保持off | replacement canonical fixture、generated DTO、repository payload scan | source mitigation与G2A重审已在`29317b...`完成；S4 runtime conformance与negative payload tests PASS | 段成威 | mitigated in source and local provider closure；activation remains off |
| R-126-018 | Desktop连接错误loopback实例、跟随proxy/redirect或泄漏Host bearer/raw/path | medium | critical | exact IPv4 loopback、no-proxy/no-redirect、per-call spawn nonce preflight、`O_NOFOLLOW` owner-only token、redacted typed domain；S7A不暴露Tauri command | wrong nonce/token mode/symlink/bearer/error/raw canary、schema/cursor/unknown-event fake Host tests | 丢弃S7A local diff、保持sidecar/chat flags off；旋转本地Host token | 段成威 | low for Rust transport；WebView/application E2E remains future |
| R-126-019 | outbox重复派发、事件乱序或标题竞态造成重复模型调用、历史分叉或人工标题被覆盖 | high | critical | operation幂等；recoverable lease/max16；accepted turn不自动重放；unknown outcome fail closed；strict cursor/identity reducer；terminal原子提交；user-title CAS优先；正文Debug redaction | duplicate/gap/mixup/restart/10k delta、outbox expiry、fake Host integration、late title与no-log canary | 标记outbox failed/incomplete并保持flags off；不猜测重发未知结果；前向修复本地DB | 段成威 | low for Rust S7B candidate；WebView/真实四组件E2E仍未运行 |
| R-126-020 | WebView伪造tenant/owner/resource，或取得Host bearer、DB key、项目真实路径/原始Host wire | medium | critical | Rust-bound短期context、command capability/resource复验、opaque IDs、closed DTO、secret/path/raw-wire denylist | IPC auth negative matrix、foreign ID、logout/revision expiry、secret/path/wire canary与no-log scan | context立即失效、清空store、停止订阅、保持feature flag off并旋转本地token/key（如实际泄漏） | 段成威 | low for S8A local conformance；process E2E仍待S10 |
| R-126-021 | Tauri event无背压或late event在切换/重启后写入错误session，导致内存放大或跨scope正文闪现 | high | critical | per-subscription 64 events/256KiB queue、20Hz合并、严格sequence/context/subscription/selection epoch、overflow/gap强制resync | fixed event fixture、10k delta、A→B race、queue overflow、restart/reconnect/fake Host fault tests | 丢弃stale projection、发`resync_required`、从SQLCipher重新加载受控snapshot | 段成威 | low-medium after S8A store PASS；真实process/UI E2E仍待S8B/S10 |
| R-126-022 | UI flag只隐藏导航但深链/loader仍可实例化，或Vue从旧command/错误猜Host/Runtime ready而错误发送 | high | critical | 独立exact-true/default-off gate覆盖nav/route/deep-link/loader；route capability；Rust closed readiness/recovery；页面只调store | flag truth-table、route lazy-loader spy、deep-link auth、schema/serde/TS readiness fixtures、ready/send race | 保持flag off；丢弃S8B0 checkpoint并回到S8A；清空旧context/store | 段成威 | low after S8B0 local gates；真实S8B组件与S10进程链仍待验证 |
| R-126-023 | 将S9 in-process fake runner或独立curl冒充Host→Runtime→Desktop→API多进程E2E | high | critical | DESIGN-126-007 process manifest、父子PID/nonce/SHA、同一run ID和真实production components；禁止mock Vue/单仓fixture冒充 | S10B-001–003 + process tree/readiness/route evidence | HOLD S10B；先形成可启动fake HTTP provider与实际Public Tasks consumer | 段成威 | **open / blocks S10B, G4, G6** |
| R-126-024 | 临时flag被Desktop sidecar强制改回false，但证据仅记录父进程env而误报已开启 | high | critical | child effective-env allowlist、route/readiness probe与flag-exit scan；不依赖shell声明 | child manifest + raw/cleanup route conformance + default-off scan | HOLD；修复受审查的test-profile注入面 | 段成威 | **open / blocks S10B** |
| R-126-025 | S10使用固定Keychain namespace触碰真实DB/auth密钥或留下本机条目 | medium | critical | master与独立secure-storage两个exact-true gate、run-derived三namespace、owner-only app-data、exact attribute-only inventory、明确cleanup owner | S10P2 unit/race/default-off + signed future native lifecycle（不记录secret） | 只按匹配manifest删除本run exact tuples；mismatch停止；失败probe已确认post absent并清除临时root | 段成威 | **historical native source controls implemented；native write/read/delete remains Deferred / NOT RUN；Local-only BLK-004 closed by DEC-126-043** |
| R-126-026 | 把空Public Tasks表当成content-free集成PASS，掩盖Desktop根本未调`/v2/tasks` | high | critical | 同一user action/run ID必须产生closed create/get/audit/DB证据；body/title/path denylist零命中 | S10B-002/009 + scoped row/audit counts/hash | HOLD；单独评审content-free orchestration实现 | 段成威 | **open / blocks S10B, G4, G6** |
| R-126-027 | 用户删除本地session后误认Public Tasks/PostgreSQL也已物理删除 | medium | critical | DEC-126-038 Accepted：`29317b...`不提供permanent delete；本地cleanup删Desktop/Host/Runtime与mapping，Public Task只保留content-free control-plane metadata；UI/文档不承诺全盘或PostgreSQL擦除 | S10P3 delete-vs-create/unknown-outcome/restart矩阵；fresh real run中PostgreSQL denylist=0且保留row只有closed fields | 若未来改变为Public Task行同删，停止并重开G2A delete contract评审 | 段成威 | **Mitigated / implementation evidence accepted by DEC-126-045** |
| R-126-028 | S10E诊断命令展开secret，或未获授权删除project-scoped volume导致证据污染/数据损失 | low | high | Compose config只用`--no-interpolate --quiet`；runtime verifier在进程内检查并只输出content-free结果；任何展开credential的run整轮作废并fresh run；volume删除单独Owner审批 | generated-secret→candidate files/runtime logs精确扫描；stop后container/network/listener=0；保留volume计数 | 停止污染run、弃用credential、保留精确资源manifest；不执行`down --volumes`/prune；另行审批后才删除确切volume/run root | 段成威 | **controlled / 8 volumes and 2 owner-only run roots intentionally retained pending separate cleanup authority** |
| R-126-028 | 为绕过stale Compose link而下载未固定二进制、复用普通volume或启动mutable image tag | medium | critical | 只允许Docker Desktop bundled Compose v5.3.0完整路径+摘要；修复前备份旧symlink；新`feat-126-s10`profile只用digest-pinned PostgreSQL/Keycloak/Caddy与run-scoped volumes，不复用`yijie_postgres_data` | version/hash/config/features、image digest、Compose project/volume inventory、退出后listener/resource diff | 恢复旧symlink；停止本次Compose project；不删未在run manifest的volume | 段成威 | **design frozen / implementation not authorized** |
| R-126-029 | test-only文件密钥被误启用到默认/生产、被symlink/权限漂移替换、写入日志/备份或跨run复用 | medium | critical | S10 master与独立ephemeral flag均须exact `true`；只允许canonical temp root、0700目录、0600 create-new/O_EXCL/O_NOFOLLOW文件、owner/nlink/canonical/role/manifest校验；CSPRNG生成且禁止固定/run-ID派生/env正文；production/default只走Protected Data Keychain | gate truth table、wrong owner/mode/nlink/symlink/manifest/cross-run/restart/crash/cleanup矩阵；source/bundle/log/process-output/evidence secret canary；退出后exact inventory | 任一不匹配fail closed且不读不删；关闭独立flag回到Protected Data默认；只按匹配manifest unlink三个synthetic文件并披露不承诺法证擦除 | 段成威 | **LIA-126-011 + DEC-126-043 Closure PASS；Local-only BLK-004 Closed；native hardening remains unverified/Deferred** |
| R-126-030 | Docker本地引用索引重启/迁移后无法用`version-tag@digest`做availability lookup，导致已存在exact image仍被误判缺失 | medium | high | Compose继续固定`version-tag@digest`；preflight只从同一authority派生`repository@digest`，核验RepoDigests/descriptor且`--pull never` | malformed/conflict/missing/digest drift单测；live exact verifier与fresh four-dependency up/stop | fail closed且不pull；保持S10B HOLD，回退仅移除新verifier调用并恢复旧helper | 段成威 | **mitigated / DEC-126-050 Accepted / S10B-BLK-002 Closed；full S10B仍未重跑** |
| R-126-030 | S10E真实Keycloak token与API JWT必需claims漂移，导致仓内transport全绿但真实Public create始终401 | high | critical | identity/API claim compatibility必须由真实Authorization Code + PKCE token证明；禁止放宽verifier、静态nbf、手工bearer、独立curl或fixture代替；修正方案固定为Keycloak内置动态mapper | DEC-126-044/S10I static+live mapper conformance；标准Authorization Code + PKCE access token numeric `nbf`；unchanged API capability/Public create；PostgreSQL content-free与retained-row | mapper/profile drift立即fail closed并停止S10B；停止本run进程，保留隔离volumes | 段成威 | **Mitigated / S10P3-BLK-001 resolved / evidence accepted by DEC-126-045** |
| R-126-031 | Infra migration wrapper把已接受的API候选身份硬编码为旧SHA，导致后续closed bootstrap checkpoint无法进入fresh S10B | high | critical | migration与bootstrap必须消费同一run-scoped closed authority中的显式完整API SHA并在secret/DB前校验clean exact worktree；不得维护两套硬编码pin | CLI/Make正负矩阵：missing/short/wrong/dirty拒绝；exact same SHA成功；candidate drift、corrupt document、mode/owner/symlink/hardlink拒绝；Infra/feat125回归 | fail closed、container/service start=0；LIA-126-015只形成corrective checkpoint，不自动重跑 | 段成威 | **Mitigated / DEC-126-052 Accepted / S10B-BLK-003 Closed / Infra `bb96333d...`** |
| R-126-032 | Docker execution capability未先验证且verifier把CLI/socket/daemon/permission/image/reference失败统一映射为“镜像不可用”，可能把环境不可达或containerd状态问题误判为digest缺失 | high | critical | DESIGN-126-011：同进程capability-first；closed failure classes；原Compose pin的Id/Descriptor/RepoDigests/repository/platform校验；受控no-pull create/remove resolver probe；保留exact pin与`--pull never` | S10BD1-001–012覆盖无CLI/daemon/permission、missing/unresolved、payload、identity/platform drift及unknown outcome/foreign cleanup；全量99/99；exact-commit live验证3 identity/3 probe并归零 | 保留R3 `REJECTED`历史；不自动pull/retag/restart/switch store；probe资源身份不匹配时删除数为0；fresh E2E仍须Owner另批 | 段成威 | **Mitigated / DEC-126-055 Accepted / S10BD1 Closure Passed / S10B-BLK-004 Closed** |
| R-126-033 | S10B没有单一machine-readable编排authority时，S9 dataset bundle ID与Host请求fixture case ID可能被人工混用，导致环境健康但fake readiness错误或不同执行者产生不同请求 | high | critical | Host内部冻结dataset/case/digest并生成请求header；对外closed readiness分别命名`dataset_id`与`fixture_case_id`；Infra只消费Host探针且不提供identity输入；不一致在Host/Desktop启动前fail closed | Host authority/endpoint/run/payload/dataset/case/digest负向；Infra seven-SHA、single-runner、no-operator-input、组合preflight、default-off/no-log/cleanup；fresh live probe | LIA-126-019实现与组合预检已通过；DEC-126-057 Option A接受Closure并关闭blocker。S10B-R5仍未执行且须单独授权 | 段成威 | **Mitigated / DEC-126-057 Accepted / S10B-BLK-005 Closed** |
| R-126-036 | 唯一S10B父runner把子resolver的closed失败类别折叠为步骤级`preflight_image_resolver_failed`，导致无法判断image identity、probe create、probe validation或cleanup哪一项失败 | high | critical | DEC-126-061/LIA-126-023已实现child closed result v1、parent同源validator、mapped leaf class与0600 evidence；保留run绑定/容量并禁止raw stderr、socket/path或command payload | S10BEP1自动化、S10BD1回归及S10BEP1-014 isolated live 3 identity/3 probe已通过；证据为exact五字段0600文件且资源归零 | DEC-126-062接受Corrective Closure并关闭BLK-007；DEC-126-063形成clean checkpoints并保留R6 REJECTED历史。fresh R7仍须Owner单独授权 | 段成威 | **Mitigated / DEC-126-063 Accepted / S10BEP1 Checkpoints Clean / S10B-BLK-007 Closed** |
| R-126-037 | S10B-001单一preflight与API-only continuation之间缺少完整四组件S10B-002–012可执行orchestrator，人工拼接可能造成run/profile/PID/evidence/cleanup authority漂移并误报G4 | high | critical | DEC-126-064/065 Option A已接受；DESIGN-126-014与LIA-126-025实现Infra单入口、仅run ID+七SHA输入、same-run summary、Infra→Desktop→Host→Runtime所有权、test-build-only真实Vue/Pinia driver、API verifier、Host Runtime/fake manifest、closed state/no-retry/evidence/no-log/crash cleanup | Docker/Compose/daemon、loopback/native文件与子进程能力PASS；S10BO1-001–014 targeted matrix 14/14、API/Host/Desktop/Infra全量lint/test/build及Governance门禁PASS | 保留R7 preflight证据与4 volumes；不执行人工shell拼接、现场修复、续跑或复用授权；DEC-126-066仅接受repository Corrective Closure，isolated live与fresh R8仍须分别授权 | 段成威 | **Mitigated / DEC-126-066 Accepted / S10BO1 Corrective Closure Passed / S10B-BLK-008 Closed / G3 Partial / G4 and local G6 Pending** |

## 5. 威胁建模

| 资产/边界 | 威胁 | 攻击路径 | 服务端/原生控制 | 安全测试 | 残余风险 |
|---|---|---|---|---|---|
| Public Tasks | spoofing/IDOR | 无 bearer、伪 tenant、猜 UUID | Principal + tenant scope + AuthorizationService + scoped query | SEC-001–006 | unknown consumers |
| Local DB | information disclosure | 切 tenant、直接 Tauri invoke、复制 DB | Rust-owned narrow commands、owner-only app data、row scope | SEC-007–010 | OS account compromise |
| Agent Host token/key | credential theft | WebView storage/log/URL/child env inheritance | Rust only、0600/0700、redaction、env allowlist | SEC-011–013 | same-user malware |
| S10 test-only ephemeral secrets | disclosure/tamper/cross-run confusion | 双flag误配、symlink/hardlink、错误owner/mode、partial write、manifest替换或cleanup越界 | Rust-only随机合成secret、canonical run root、0700/0600、O_EXCL/O_NOFOLLOW、nlink=1、manifest role绑定；WebView/shell只见closed状态 | default-off、restart/cross-run、wrong-mode/owner/symlink/nlink、crash/cleanup/no-log测试 | same-user privileged malware与OS/backup残留；仅Local-only synthetic data，native production proof仍Deferred |
| Project directory | path traversal/TOCTOU | crafted path、symlink swap、stale bookmark | native selection、canonicalization、open-time revalidation | SEC-014–016 | OS-level changes |
| Model input/output | prompt injection/content injection | prompt asks title HTML or expose internal data | no tools/write、schema/sanitize、safe renderer | AI-SEC-001–005 | model content risk |
| Reasoning boundary | confidential/restricted model output leak or execution | raw reasoning event/provider error | ADR-0016 raw-only versioned contract、纯文本、不执行HTML/链接/命令、正文不进logs/metrics/audit、flag default off | SEC-017–019 + future raw conformance | provider-specific variance and semantic secrets remain |
| Permanent delete | repudiation/data remanence | incomplete cascade、late event、Runtime WAL/log、backup | confirmation、active lock、Desktop/Host/Runtime saga、SQLCipher secure-delete/checkpoint、限定 receipt/文案 | SEC-020–024 | forensic/OS backup residue explicitly out of guarantee；ADR-0014 Accepted |
| SSE | replay/tamper | duplicate/out-of-stream event | bearer、session binding、stream/sequence/event ID | SEC-025–027 | process restart gap |

必须检查但当前不适用：SSRF（无 URL fetch）、平台资金/订单副作用（无 connector/tool）、文件上传病毒（非文本输入被拒绝）。这些不是永久豁免；范围变化即重新评估。

## 6. 数据生命周期

| 数据类别 | 收集 | 使用 | 存储 | 共享 | 保留 | 删除 | 审计 |
|---|---|---|---|---|---|---|---|
| 用户/模型正文 | 明确发送/stream | 对话展示与恢复 | Desktop local DB；Runtime 自有 rollout | MiniMax 处理；不写 yijie-api DB | 至 session 永久删除 | DB transaction + approved Runtime cleanup | 不记录正文 |
| raw reasoning | Runtime raw reasoning event/completed content | 展示具体“模型推理记录” | Desktop SQLCipher独立records；terminal/显式incomplete落库；不得用localStorage/Host log/Runtime rollout替代 | 不额外共享；不进云端/日志/遥测/审计正文 | 同session | FK cascade + ADR-0014 checkpoint/限定披露 | 仅event/bytes/duration/status/outcome，不含正文 |
| title | model/fallback/user | 列表与路由标题 | Desktop local DB | 不进Public Tasks/PostgreSQL；当前Desktop也无`/v2/tasks` consumer | 同 session | cascade | source/version/outcome |
| project reference | native picker | cwd 与列表 | app data/bookmark | Host 只收 canonical cwd | 至移除/卸载 | revoke/remove；目录不删 | ID/outcome，无 path |
| mapping/cursor | Host/Runtime | resume/dedupe | Host bbolt + Desktop DB | local processes | 同 session | cleanup/delete | IDs/outcome |
| security audit/deletion receipt | authority/Desktop/Host cleanup candidate | 追责/删除恢复控制 | append-only API audit；Desktop encrypted job/receipt；Host独立content-free operation receipt只为丢失响应幂等 | authorized local owner only | receipts 候选30天 | 正文随session删除；receipts到期物理删除/适用checkpoint | 无正文/title/path/raw session/thread ID；仅keyed hash/surface outcome |

## 7. 高风险操作、审批与审计

| 工具/操作 | 用户意图 | 参数/影响范围 | 审批人/有效期 | 默认行为 | 审计字段 |
|---|---|---|---|---|---|
| text turn | 点击发送/`⌘Enter` | 当前 session + text + project | 当前用户 / 单次 | allow only if all checks pass | IDs/scope/model/outcome，不含 text |
| interrupt | 点击停止 | 当前 active turn | 当前用户 / 单次 | deny non-active/mismatched | session/turn/outcome |
| rename/pin | 菜单动作 | 单 session/project metadata | 当前用户 / 单次 | deny cross-scope | resource/action/outcome |
| permanent delete | 二次危险确认 | 单 session 及列明的 data surfaces | 当前用户 / 单次短有效期 | deny on active/cleanup uncertainty | scope/counts/outcome，无正文 |
| project remove | 确认移除引用 | 单 project reference | 当前用户 / 单次 | 不删目录/history | project ID/outcome |
| tool/file/platform write | 无本期意图 | N/A | N/A | deny | rejection reason |

## 8. 临时例外

| Exception ID | 原因 | 范围 | Owner | 批准证据 | 到期日 | 补偿控制 | 移除条件 |
|---|---|---|---|---|---|---|---|
| EXC-125-001（继承，不新增） | legacy `/v1/tasks` 尚未权威授权 | legacy handlers/production exposure | 段成威 | FEAT-125 A6 / ADR-0012 | FEAT-126 生产启用或 2026-09-30，取较早者 | approved host profile 不注册 + ingress deny | FEAT-126 hardening 生产启用 |

本包不创建新的安全例外。到期未完成时保持 Tasks 阻断并重新审批，不能自动延期。

## 9. Codex 停止条件

- 后续范围变更试图推翻 DEC-126-001 时，必须重开 G1 并先处理 Feature ID 与 ADR 引用；
- 需要修改 Accepted ADR/Pattern 而未获得对应 Gate 的明确批准；
- 需要再次修改/删除远端候选branch、移动`origin/develop`、merge、tag、publish或启动本地业务切片，但没有Owner另行明确授权；
- PR #1远端CI仍为红色，或`govulncheck`/`origin/main` breaking仍因前序失败未执行，却试图merge、waive、rerun或把本地门禁冒充完整远端CI；
- 试图修改历史`c000a0245acb5c3f7ead5d2a877fb60c281c588c`、追加push到固定candidate branch，或把唯一candidate `29317b6426578749dc698fc2ad32b986ee5c8e9f`的批准误解为远端写入、业务实现或LIA自动恢复授权；
- 试图把浮动branch当作契约身份、把本地路径投影当作第二权威源，或在LIA-126-001范围外修改Runtime/Infra及S7–S11业务代码；
- 试图把Local Runtime Ready当成线上部署/Production Ready，或在没有新审批时调用MiniMax、配置registry、接入云数据库/真实用户数据；
- 后续consumer试图固定非当前唯一`29317b6426578749dc698fc2ad32b986ee5c8e9f`候选，或未核对已批准digest；
- 契约权威源、supported baseline、consumer inventory 或 Runtime canonical capability 不可用；
- 需要真实生产 secret/account、付费请求、真实用户对话/项目或生产数据库；
- 工作区出现无法归属的新改动，或需要覆盖 FEAT-123 既有删除；
- 测试只能通过展示 raw chain-of-thought、绕过 auth、降低断言或手改生成物；
- 任一切片超出批准仓库/文件/feature flag 范围。

## 10. 批准记录

| 范围 | 决策人 | 结论 | 日期 | 证据 |
|---|---|---|---|---|
| 原始需求建档/G0 | 段成威 | Requested / G0 Passed | 2026-08-01 | 本轮用户请求 |
| 产品范围、编号与交互语义 | 段成威 | Approved；G1 Passed | 2026-08-01 | 用户明确同意推荐方案；DEC-126-001–004/008–010/013 Accepted，Q-001–Q-005/Q-011–Q-014 Resolved |
| 本地数据权威/local-cloud 边界 | 段成威 | Approved narrow decision；G2 仍未通过、无实现授权 | 2026-08-02 | DEC-126-005/014 + ADR-0013 Accepted；Q-007 Resolved |
| SQLite protection/backup 与物理删除 | 段成威 | Approved；G2 仍未通过且不授权实现 | 2026-08-02 | ADR-0014/DEC-126-006 Accepted；Q-006/Q-015 Resolved；fixed Runtime/delete + Rust dependency evidence |
| 隔离标题技术方案 | 段成威 | Approved；G2 仍未通过、无实现授权 | 2026-08-02 | ADR-0015/DEC-126-007 Accepted；Q-008 Resolved；fixed Runtime/fake-provider fixtures PASS |
| MiniMax feature 合成验证 | 段成威 | Approved bounded run 已完成；title PASS，public-summary 旧门槛 FAIL；同时观察到 raw reasoning；两次预算耗尽、不得重跑 | 2026-08-02 | MM-126-001/002；历史证据不改写；后续 raw 方向由 ADR-0016 承接，Q-009 Resolved |
| Raw reasoning产品语义 | 段成威 | Approved；展示raw reasoning纯文本，不保证完整/稳定，不进logs/telemetry/audit；缺raw阻断功能Gate，不静默时长降级；G2仍未通过 | 2026-08-02 | ADR-0016/DEC-126-015 Accepted；Q-009 Resolved；不追加模型调用 |
| Raw reasoning持久化 | 段成威 | Approved；Desktop SQLCipher历史持久化、懒加载并随session物理删除；G2仍未通过 | 2026-08-02 | DEC-126-016 Accepted、Q-016 Resolved；不授权schema/代码 |
| DESIGN-126-003/raw v2与SQLCipher细节 | 段成威 | Approved；设计冻结，未实现 | 2026-08-02 | DEC-126-017 Accepted；fixed fake-provider/Runtime fixtures 4/4 PASS |
| 安全/Public Tasks | 段成威 | Approved；DEC-126-011/012 Accepted | 2026-08-02 | Q-010 Resolved；未知外部consumer按安全兼容类别处理，不声明为零 |
| Chat/App Shell Pattern | 段成威 | Approved / Accepted；取代现有Pattern中FEAT-126冲突段落 | 2026-08-02 | `yijie-desktop/docs/design/docs/design/05-patterns/12-feat-126-chat-app-shell-candidate.md` |
| G2 Closure总评审 | 段成威 | Passed；允许进入G2A source-contract candidate评审，仍不授权业务编码 | 2026-08-02 | Owner明确批准DEC-126-017、DEC-126-011/012和Pattern并宣布G2通过 |
| G2A source contract shape | 段成威 | Approved；DEC-126-018 Accepted并授权immutable candidate commit | 2026-08-02 | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`；post-commit gates PASS |
| G2A final source-contract readiness（历史） | 段成威 | Approved / Passed at DEC-126-019；后由DEC-126-024重审取代current identity | 2026-08-02 | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`仅保留为历史远端候选；不授权push/tag/merge、downstream pin、业务编码或生产启用 |
| Source-contract remote availability | 段成威 | Approved / Complete；仅专用candidate branch | 2026-08-02 | DEC-126-020；remote SHA匹配、clean clone全部门禁与摘要PASS；`origin/develop`未移动；无merge/tag/发布/pin/编码 |
| Source-contract Draft PR与CI观察 | 段成威 | Approved scope / Executed；PR #1固定历史candidate，CI已到终态并回填 | 2026-08-02 | Draft PR `develop <- feat/feat-126-contract-candidate`；head精确匹配旧`c000a024`；run 30741466028在dependency audit失败；未重跑/豁免/修复/push/merge |
| Source-contract merge readiness | 段成威 | Approved DEC-126-021 / HOLD；当前不批准merge | 2026-08-02 | CI red；`brace-expansion 2.1.2` high；`govulncheck`与`origin/main` breaking skipped；不回退G2/G2A |
| Local-only Delivery Strategy | 段成威 | Approved / DEC-126-022 Accepted；交付目标改为Local Runtime Ready | 2026-08-02 | tag/publish/deploy/G5均N/A；G6为Owner本地验收；业务编码与一次MiniMax local smoke仍分别待批准 |
| Local Implementation Authorization | 段成威 | LIA-126-001–007已完成S4–S9并被接受；S10E/P1/P2F/P3/S10BD1已接受；三次S10B均fail closed；S10B-BLK-001–004 Closed | 2026-08-05 | DEC-126-055接受S10BD1 Closure；不含S10B-R4、MiniMax、S11、default activation或远端动作 |
| Public Tasks input / G2A re-review | 段成威 | DEC-126-023/024 Accepted；Q-017 Resolved；G2A Re-review Passed | 2026-08-02 | `29317b6426578749dc698fc2ad32b986ee5c8e9f`为唯一candidate；`c000a024`仅为历史远端候选；后续由DEC-126-025恢复LIA-126-002 |
| Remote State Reconciliation / LIA resume | 段成威 | DEC-126-025 Accepted；远端事实已核对；LIA-126-002仅S4–S6恢复 | 2026-08-02 | exact remote refs；旧PR/develop/merge/tag/publish/deploy不变；S7–S11/UI/MiniMax/追加push禁止 |
| LIA-126-002 Closure Review / S7A Authorization | 段成威 | DEC-126-026 Accepted；S4–S6 Foundation Corrective Closure通过；单独授权S7A Desktop Rust Host Bridge/Domain | 2026-08-02 | S8/UI、MiniMax、flag activation、远端写入、merge/tag/publish/deploy继续禁止 |
| S7A Closure Review | 段成威 | DEC-126-027 Accepted；S7A Closure Passed；G3保持Partial并单独授权S7B Rust application domain | 2026-08-03 | exact loopback+nonce+owner token+typed v2 SSE/domain；无Tauri/Vue接口、无flag/MiniMax/远端动作 |
| S7B Closure Review | 段成威 | DEC-126-028 Accepted；S7B Closure Passed；G3保持Partial | 2026-08-03 | durable outbox、strict/coalesced reducer、batched history、title CAS；113 TS + 78/79 Rust pass；无Tauri/Vue接口、无flag/MiniMax/远端动作 |
| Desktop IPC/ViewModel Contract Review | 段成威 | DESIGN-126-005 + DEC-126-029 Accepted；LIA-126-003与LIA-126-004依次授权S7C/S8A | 2026-08-03 | 当时冻结private IPC v1与S7C/S8A/S8B顺序；S8B后来已由DEC-126-034接受，不改写该历史授权边界 |
| S7C Closure Review | 段成威 | DEC-126-030 Accepted；S7C Closure Passed；G3保持Partial | 2026-08-03 | 300s Rust auth context/facade、actions/interrupt、SQLCipher v4 cleanup、receipt HMAC、coordinator/restart/resync；113 TS + 87/88 Rust；无Tauri/TS/Vue/flag/MiniMax/远端动作 |
| S8A Closure Review | 段成威 | DEC-126-031 Accepted；S8A Closure Passed；G3保持Partial；不授权S8B | 2026-08-03 | 20 private commands、closed schema/fixtures、Rust event bridge、TS client/store；127 TS + 93/94 Rust；无Vue/flag/MiniMax/central pin/远端动作 |
| S8B0 UI Integration Readiness Review | 段成威 | DESIGN-126-006完成；DEC-126-032 Accepted | 2026-08-03 | UI gate/route/lifecycle/store/tasks/scroll方案及private IPC stop condition获批；随后单独LIA-126-005 |
| S8B0 Implementation Authorization | 段成威 | DEC-126-032 Accepted；LIA-126-005只授权S8B0，S8B仍禁止 | 2026-08-03 | default-off gate、route/auth/lifecycle、store consumption、readiness/storage private IPC与Tasks真实metadata/default-off；不启用flag、不开发完整Vue visual page |
| S8B0 Closure Review | 段成威 | DEC-126-033 Accepted；S8B0 Closure Passed，G3仍Partial；不自动进入S8B | 2026-08-03 | Desktop `5dab02a1…34d85`；135 TS、95/96 Rust（1既有ignored）、full lint/test/build/fmt/clippy；flag off/no MiniMax/no remote |
| S8B Implementation Authorization | 段成威 | LIA-126-006 Approved；只允许Vue页面/交互/视觉/a11y，不授权activation、S9–S11或IPC/Rust/central边界变化 | 2026-08-03 | Owner当前明确指令 |
| S8B Closure Review | 段成威 | Accepted；DEC-126-034采用方案A，S8B Closure Passed，G3仍Partial；不自动授权S9/S10/activation | 2026-08-03 | Desktop `35f2744…7cbd`与29个TS测试文件/164 tests、axe、build、Rust、audit、browser/security evidence；VoiceOver人工项保留到S11/G6 |
| DEC-126-035 Remote State Reconciliation | 段成威 | Accepted；只接受精确远端可达事实并保持Gate/发布边界 | 2026-08-04 | 五仓`ls-remote`+临时clean clone PASS；develop/旧PR/sole candidate不变；治理checkpoint `1e7a312…6353`不push |
| LIA-126-007 / S9 Authorization | 段成威 | Approved / Executed；仅test authority/fixtures/harness与本地checkpoint | 2026-08-04 | 固定pins、250条合成dataset、title/raw/no-log/injection Gate；0 MiniMax/flag/S10/远端动作 |
| DEC-126-036 S9 Closure Review | 段成威 | Accepted；Owner接受方案A并保持G3 Partial | 2026-08-04 | Host `8707dea…c9378`、Desktop `adfdb5b…af9cb`；逐指标和逐仓门禁PASS；不授权S10 |
| S10A Readiness & Test Profile Review | 段成威 | DEC-126-037 Accepted / Option C；继续HOLD S10B | 2026-08-04 | DESIGN-126-007、Compose/provider/sidecar/Keychain/Public Tasks五项blocker；LIA-126-008仍Blocked Draft；未启动进程/flag或修改业务码 |
| S10P0 Corrective Design Review | 段成威 | DEC-126-038 Accepted / Option B；未批准任何corrective切片 | 2026-08-04 | DESIGN-126-008、S10E/P1/P2/P3影响/测试/回滚、closed private projection与Public row retention限制 |
| S10E Compose/Isolated Identity Environment | 段成威 | DEC-126-039 Accepted / S10E Closure Passed / BLK-001 Closed | 2026-08-04 | Infra `99e50d8…6baf`；Compose v5.3.0 discovery、exact-digest/default-off profile、migration v4、synthetic OIDC/TLS、runtime/no-log/rejected-run/cleanup PASS；不授权S10P1或S10B |
| LIA-126-009 / S10P1 Closure Review | 段成威 | DEC-126-040 Accepted / S10P1 Closure Passed / BLK-002/003 Closed | 2026-08-04 | Host `e0a8d3d…5674`、Desktop `fba934c…7285` local only；S10P1范围P1为0；不授权S10P2/P3/S10B、MiniMax、Keychain、flag activation或远端动作 |
| LIA-126-010 / S10P2 Closure Review | 段成威 | DEC-126-041 Option B Accepted；historical native source checkpoint/HOLD；Local-only successor later closed BLK-004 | 2026-08-04 | Desktop `c863b2a…5dc68` local only；仓内门禁PASS；0 signing identities/profiles；native remains Deferred/NOT RUN；不授权S10P3/S10B |
| DEC-126-042 / Local-only Secure Storage Adjustment Review | 段成威 | Accepted / Option A / Security-G2 Design Passed | 2026-08-04 | double-exact ephemeral file backend与Local-only退出条件已接受；central G2A=N/A；DEC-126-043后来关闭BLK-004；不安装Xcode、不访问Keychain |
| LIA-126-011 / DEC-126-043 S10P2F Closure Review | 段成威 | Accepted / Option A / S10P2F Closure Passed / Local-only BLK-004 Closed | 2026-08-04 | Desktop `46107ee…0036` local only；6个Rust文件；targeted 19 pass/1 native ignored，全量124 pass/2 native ignored，TS 165；0 Keychain/MiniMax/real data/remote write；不授权S10P3/S10B/S11 |
| LIA-126-012 / DEC-126-044 / DEC-126-045 | 段成威 | S10P3 + S10I executed；real main chain PASS；S10P3 Closure Passed / BLK-005 Closed | 2026-08-05 | Desktop `ed9eb14…b78c`、Infra `8d7c84d…df0b` local-only；numeric nbf + unchanged API + Public bind/delete-retention PASS；环境已停止、volumes保留；DEC-126-045不授权S10B |
| LIA-126-008 / S10B execution | 段成威 | DEC-126-046 Option A Accepted；接受fail-closed事实，不接受S10B Closure；DEC-126-048/050后续关闭BLK-001/002 | 2026-08-05 | S10B-001 FAIL、002–012 NOT RUN；fresh重跑未授权；不授权S11/MiniMax/default activation/远端动作 |
| DESIGN-126-009 / DEC-126-047 | 段成威 | Option A Accepted；S10BP0 closed FEAT-126 bootstrap设计通过；随后Owner另行授权LIA-126-013 | 2026-08-05 | profile/DSN/issuer/四manifest/validation ordering/v4/idempotency/rollback/no-log矩阵已冻结；该设计批准本身不授权S10B/S11 |
| LIA-126-013 / DEC-126-048 | 段成威 | S10BP1 implemented and verified；Owner Accepted Option A | 2026-08-05 | Closure Passed、BLK-001 Closed；API/Infra仅本地未提交；fresh-v4 exact matrix、atomic rollback、feat125/generic regression、content-free evidence PASS；S10B未重跑，S11未授权 |
| DESIGN-126-010 / DEC-126-049/050 | 段成威 | exact repository-digest corrective accepted、implemented并由Owner接受Closure | 2026-08-05 | Infra 85/85 + fresh no-pull dependency up/stop PASS；BLK-002 Closed；S10B未重跑，S11未授权 |
| LIA-126-014 / DEC-126-051 | 段成威 | fresh S10B-R2授权已消费；migration preflight fail closed；Owner接受失败事实并拒绝Closure | 2026-08-05 | checkpoint：Governance `9db41b0...`、API `c5f334e...`、Infra `597acb3...`；run `4ffa07b9...`未创建资源；`S10B-BLK-003` Open；不授权rerun/S11 |
| LIA-126-015 / DEC-126-052 | 段成威 | Owner单独授权migration/bootstrap共享完整API SHA authority corrective；Infra实现/验证完成并接受Closure | 2026-08-05 | Infra `bb96333df908d6fea72ec0a1f57a64477c2428e4`；87/87 + validate/lint/shell/Node/diff PASS；0 runtime resource；BLK-003 Closed；不自动授权rerun/S11 |
| LIA-126-016 / S10B-R3 | 段成威 | Owner在DEC-126-052 Accepted与clean Governance checkpoint后单独批准一次fresh S10B-001–012；已执行并消费 | 2026-08-05 | run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5`；S10B-001 immutable-image preflight FAIL；002–012 NOT RUN；`S10B-BLK-004` Open；0 container/network/volume/listener/model/remote write；DEC-126-053已接受失败事实并拒绝Closure |
| DESIGN-126-011 / DEC-126-054 / S10BD0 | 段成威 | Owner随DEC-126-053只授权read-only capability/resolver设计；DESIGN-126-011完成，DEC-126-054 Option A已Accepted | 2026-08-05 | current daemon/socket-unavailable差分证明generic verifier误分类；S10BD0退出时尚未批准LIA-126-017，后续状态由下一行取代；未启动Docker、container或S10B，未修改Infra源码 |
| LIA-126-017 / S10BD1 | 段成威 | Owner先单独批准，随后以明确执行指令开始并消费；实现与验证完成，提交DEC-126-055 Closure候选 | 2026-08-05 | Governance执行基线`075a5051…4484`；Infra `2a643cae…97a`；S10BD1-001–012与99/99 PASS；live `12600000-0000-4000-8000-000000000055`验证3 identity/3 no-start probe、资源归零、Docker恢复停止；BLK-004在Owner接受前仍Open |
| DEC-126-055 / S10BD1 Closure Review | 段成威 | Accepted / Option A / S10BD1 Closure Passed / S10B-BLK-004 Closed | 2026-08-05 | 接受不授权S10B-R4/S11/MiniMax/activation/remote write；G3仍Partial |
| LIA-126-018 / S10B-R4 | 段成威 | Explicitly Authorized Once / Consumed / Executed-Blocked / Closure Fail | 2026-08-05 | run `96a0a80d-27d4-4022-a470-4a7f004d9c4c`；S10B-001 fixture identity 403；002–012 NOT RUN；S10B-BLK-005 Open；无修正/重跑 |
| DEC-126-056 / S10B-R4 disposition | 段成威 | Accepted / Option A / LIA-126-019 separately authorized | 2026-08-05 | 接受fail-closed事实、拒绝Closure；只授权S10BF1，不自动授权S10B-R5、S11或MiniMax |
| LIA-126-019 / S10BF1 | 段成威 | Consumed / Implemented / Closure Passed | 2026-08-05 | Host `1ca4ee5…a560`、Infra `5723ffd…c0c9`；fresh `ed22fc82…f3f4`通过单一S10B-001组合预检；summary `8198442e…f7d9`；未执行R5 |
| DEC-126-057 / S10BF1 Closure Review | 段成威 | Accepted / Option A / S10B-BLK-005 Closed | 2026-08-05 | 只关闭S10B-BLK-005；fresh S10B-R5仍须另行明确授权 |

### DEC-126-034 残余风险判定

- VoiceOver：人工清单已形成，但当前没有人工执行记录；不得写成VoiceOver已通过。DEC-126-034接受其为非阻断残余项，保留到S11/G6 Owner本地验收，不扩大为S9/S10实现授权。
- 组合链：当前证明真实Vue组件消费真实Pinia reducer，未证明四进程链；该缺口归S10B并继续阻断G4/G6，不回退已接受的S8B单仓Closure。
- feature activation：flag继续unset/false，默认用户行为无变化；开启、test profile与完整E2E均需后续单独授权。
- 依赖：`axe-core@4.10.3`为exact devDependency，npm audit为0且production依赖/bundle扫描不存在；若未来升级须重新audit和lockfile评审。

### DEC-126-035 Accepted / LIA-126-007 实际边界

- DEC-126-035已接受远端事实校正，不重新评审已接受的S4–S8B实现。
- LIA-126-007选择`yijie-agent-host`作为versioned fake-provider Eval dataset/runner authority；Desktop只消费锁定事件fixture并验证reducer、SQLCipher和plaintext projection。
- `feat126-title-raw-v1`实际为200多语言普通样本、50 injection/adversarial、holdout=50；manifest/dataset/split/schema/runner/generator/fixtures均由SHA-256 lock fail closed。
- title Gate实际PASS：250/250结构、200/200语义、50/50 unsafe拒绝；late overwrite、extra action和泄漏均0。
- raw Gate实际PASS：valid 210/210、四类负例40/40；HTML/Markdown执行、Host log/bbolt和Desktop production bundle正文泄漏均0。
- DEC-126-036已由Owner接受；该决定不调用MiniMax、不修改production Host/Desktop业务源码或任何契约/Runtime pin，也不授权进入S10。

## 11. DEC-126-058 — S10B-R5 Fail-closed Disposition（Accepted）

| 项目 | 结论 |
|---|---|
| 状态 | `Accepted 2026-08-06 / Option A / R5 Closure Rejected / LIA-126-021 Authorized and Consumed` |
| 事实 | LIA-126-020已消费。fresh run `24ae14b7-46d1-4fd5-a7ac-a30932586ad6`的唯一`make feat-126-s10b-preflight`通过，S10B-001为PASS；继续S10B-002时，在API readiness与任何业务数据创建前发现runtime profile authority不一致，随即停止；S10B-003–012 NOT RUN |
| 根因 | accepted preflight以`feat-125-local-lab`启动API；Owner冻结的R5完整链要求`feat-126-s10-local-lab`；当前API runtime service-profile validator仅暴露前者。bootstrap profile虽然支持FEAT-126，但不是runtime service-profile authority，二者不能静默等同 |
| Option A（推荐） | 接受fail-closed事实但拒绝R5 Closure；保持`S10B-BLK-006 Open`；单独设计并授权closed FEAT-126 API runtime profile corrective，使组合preflight和002–012 continuation共享同一authority；之后再申请fresh run |
| Option B（不推荐） | 把`feat-125-local-lab`视为R5隐式兼容authority并继续；会绕过冻结基线且掩盖profile语义分裂 |
| Option C（不推荐） | 弱化/删除runtime profile校验；会扩大本地测试入口并破坏fail-closed边界 |
| Contract impact | 本次执行与治理记录为`none`；未来纠偏预期仅为private local deployment semantic，若发现central contract影响必须停止并重开G2A |
| 禁止 | LIA-126-021只允许API/Infra corrective与治理；不重跑S10B、不进入S11、不调用MiniMax、不启用默认flag、不push/merge/tag/publish/deploy |

风险`R-126-035`已由DEC-126-059关闭：组合preflight与唯一continuation launcher共享closed runtime authority，并由同run summary、七仓SHA与`api_binary_sha256`约束。该Closure不证明完整E2E；剩余风险转由LIA-126-022/S10B-R6的fresh execution、content-free/no-log与cleanup门禁控制。

## 12. DEC-126-059 — S10BRP1 Closure Review（Accepted）

| 项目 | 结论 |
|---|---|
| 状态 | `Accepted 2026-08-06 / Option A / S10BRP1 Closure Passed / S10B-BLK-006 Closed` |
| Option A（推荐） | 接受DESIGN-126-012与LIA-126-021候选实现/仓内验证，关闭`S10B-BLK-006`；随后先形成API、Infra、Governance clean local checkpoint并记录完整SHA，再单独评审fresh S10B授权 |
| API证据 | `feat-126-s10-local-lab`是正式closed runtime profile；环境、双exact flags、DSN/issuer/JWKS/CA/port/loopback与v1隔离全部fail closed；FEAT-125与default路径不改义；`make lint`、`make test` PASS |
| Infra证据 | 单一versioned authority构建preflight API child env，并把authority及双快照得到的`api_binary_sha256`写入summary；唯一continuation入口只接收run ID与七仓SHA，从固定run路径安全读取工件，强制同run summary reader→builder，并复核binary digest与dev/inode/mode/size/mtime后启动固定API child；override与summary/SHA/artifact/binary drift被拒绝；`pnpm validate`、`make lint`、`make test`及113/113 PASS |
| Checkpoints | API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`；Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`；均clean local/not pushed |
| 未证明 | 没有启动Docker、API/Host/Desktop/Runtime，没有执行S10B-002–012，没有真实Vue对话或G4证据 |
| Contract impact | `semantic`仅限private FEAT-126 local deployment interface；central contracts、Public Tasks/Host wire、Desktop IPC、durable业务schema与Runtime pin无变化，central G2A=`N/A` |
| 边界 | 本决定关闭BLK-006但不完成G4/G6。Owner以同一后续指令另行授权LIA-126-022/S10B-R6；该授权尚未消费，且不包含S11、MiniMax、feature activation、push/merge/tag/publish/deploy |

## 13. LIA-126-022 — S10B-R6 Fresh Local E2E Authorization

| 项目 | 结论 |
|---|---|
| 状态 | `Consumed 2026-08-06 / Executed-Blocked / R6 Closure Rejected by DEC-126-060` |
| 固定候选 | Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`；Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`；Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`；Governance为本次批准形成的clean checkpoint HEAD |
| 范围 | 一次fresh S10B-001–012；canonical新run UUID、fresh隔离资源、synthetic identity/data、fake provider、test-only ephemeral secret backend与临时exact-true flags |
| 未授权 | 授权已消费且不得重用；不调用MiniMax/外部模型，不使用真实数据/Keychain，不现场改源码/contract/wire/schema/pin，不进入S11，不push/merge/tag/publish/deploy |
| 停止 | 任一基线、authority、binary digest、identity、migration、E2E、content-free、no-log、cleanup或default-off失败即终止；不得现场修复、续跑或直接重试 |

## 14. DEC-126-060 — S10B-R6 Fail-closed Disposition（Accepted）

| 项目 | 结论 |
|---|---|
| 状态 | `Accepted 2026-08-06 / Option A / R6 Closure Rejected / BLK-007 Open` |
| 执行事实 | LIA-126-022已消费；run `28afba8b-573a-46ec-b9d1-8a635c7b9cf0`在唯一S10B-001 preflight的image resolver步骤失败；S10B-002–012 NOT RUN |
| 可确认 | 七仓完整SHA/clean、Docker daemon/Compose capability、端口、secret init与Compose config先行通过；三个exact image的只读Id/Descriptor/RepoDigest/linux-arm64匹配 |
| 不可确认 | 父runner未保留子resolver leaf class；no-start create/validation/cleanup哪一步失败未知，不得从image inspect PASS推导resolver PASS |
| 接受处置 | 接受fail-closed事实但拒绝R6 Closure；保持`S10B-BLK-007 Open`。错误分类/证据传播设计、纠偏实施和fresh R7继续分别授权，本决定本身不启动任何一项 |
| 安全与清理 | container/network/volume/listener=0；run root 0700，2个ignored 0600文件；REJECTED hash `7c7c5f61…5e11`；secret evidence hits=0；MiniMax/Keychain/真实数据/业务进程/远端动作=0 |

## 15. DEC-126-061 — Closed Resolver Result Propagation（Accepted）

| 项目 | 结论 |
|---|---|
| 状态 | `Accepted 2026-08-08 / Option A / LIA-126-023 Separately Authorized and Consumed` |
| Option A（推荐） | resolver提供内部专用closed result v1；parent通过同一module导出的validator/allowlist消费，映射12个leaf class并保存固定0600 evidence；默认Make/human CLI不改义 |
| Option B | parent直接import并调用resolver函数；能保留typed error，但失去真实child process/exit/framing验证，未来独立CLI容易再次漂移 |
| Option C | 解析human stderr或直接重试；拒绝，因为文本可能受Make包装/本地化/路径污染且不versioned，重试不能补回R6证据 |
| Closed shape | success exact五字段；failure exact七字段；phase、target、cleanup均closed enum；stdout一行≤2048 bytes、stderr empty、exit/status严格一致、120秒timeout |
| Parent evidence | REJECTED保持v1 exact三字段，`failure_class=preflight_image_resolver_<leaf>`；validated child envelope另以create-new 0600写入固定ignored evidence；protocol错误只使用五个parent-only closed class |
| 安全 | 禁止secret、DSN、token、socket、真实路径、image pin/digest、container ID、command和raw stderr；cleanup incomplete/unknown只停止，不授权parent删除资源 |
| Contract impact | `semantic` only for private FEAT-126 local deployment interface；central contracts、business wire/schema、Compose pins和Runtime pin不变，G2A=N/A |
| 下一门禁 | DEC-126-063已形成Infra/Governance本地clean checkpoints；fresh R7、S11/MiniMax仍分别未授权 |

## 16. LIA-126-023 — S10BEP1 Corrective Execution

| 项目 | 结论 |
|---|---|
| 状态 | `Consumed / Repository Implemented / S10BEP1-014 Isolated Live PASS / DEC-126-062 Accepted / Corrective Closure Passed / BLK-007 Closed` |
| 授权解释 | Owner连续“继续执行”指令按本任务已声明边界，先接受DEC-126-061 Option A，再单独授权执行下一推荐corrective；不包含fresh R7、S11、MiniMax、activation或远端写入 |
| 实现 | resolver新增固定`--closed-result-v1`，同源12 leaf与显式合法phase/target/cleanup tuple validator；parent以namespace protocol guard固定Node/script/timeout/buffer调用，严格校验UTF-8、单末尾LF、duplicate-key/framing/exit/stderr/run binding，映射leaf并create-new写0600 evidence；closed resolver后重验只读Compose config，再走固定profile/services的`up --pull never`，默认human Make/Compose pin保持 |
| 通过证据 | Docker client/server 29.6.1、Compose 5.3.0与daemon access PASS；canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`返回exact passed v1 envelope，3 identity/3 no-start probe；0600 evidence SHA-256=`e13f633fb331e3b0c0d08f22e16f7126980555ae849a73766a7bcc2259be6b34`且仅五个success字段；无log/secret/path/image/container payload；三项exact image Id/RepoDigest/platform前后逐项一致且全局image count均为6，container/network/volume/listener=0；Infra 128/128、targeted 34/34、validate、`make lint/test`及Governance default/strict/G2A/YAML/lint/test/diff全PASS |
| 后继checkpoint | DEC-126-063仅形成Infra/Governance本地clean checkpoints；Infra=`0842ff2dcf9be6fce7aa6b19adbb6ea475607136`，Governance为包含DEC-126-063的本地commit。S10B-R7、S11、MiniMax、activation与远端动作均未执行 |
| 结论 | DEC-126-062已接受S10BEP1 Corrective Closure并关闭`S10B-BLK-007`；G3保持Partial、G4/G6 Pending；`s10b_r7_executed=false`，fresh R7未授权 |

## 17. DEC-126-062 — S10BEP1 Corrective Closure（Accepted）

| 项目 | 结论 |
|---|---|
| Owner决定 | 接受LIA-126-023/S10BEP1 Corrective Closure；确认S10BEP1-014 isolated live、Infra全量门禁和Governance门禁PASS |
| Blocker | `S10B-BLK-007 Closed`；`S10B-BLK-001–007`现均Closed |
| 保持状态 | G3 Partial、G4/G6 Pending；S10B-002–012仍无完整PASS run |
| 未授权 | fresh R7、S11、MiniMax、feature activation、真实数据、commit、push及其他远端写入 |
| Contract impact | `none` for governance disposition；private deployment corrective的既有`semantic`分类不变，central G2A=N/A |
| Post-decision gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS |

## 18. DEC-126-063 — Local Clean Checkpoint Closure（Accepted）

| 项目 | 结论 |
|---|---|
| Owner决定 | 仅执行DEC-126-062后的local clean checkpoint closure；不得执行fresh R7 |
| 范围核对 | Contracts/API/Host/Desktop/Runtime clean且SHA分别保持`29317b6…e9f`、`d1c72b2…a34`、`1ca4ee5…560`、`ed9eb14…b78c`、`3aa317c…d6f`；Infra仅5个S10BEP1 corrective文件，Governance仅9个FEAT-126文件 |
| 提交前门禁 | Infra validate、128/128、targeted 34/34、完整make lint/test、Compose semantic、Node/Shell/diff PASS；Governance default/strict/G2A、unique-key YAML、lint/test、checker Shell及diff PASS |
| Clean checkpoints | Infra=`0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；Governance=包含本决策的本地commit；两个worktree提交后必须clean |
| Contract impact | checkpoint governance=`none`；corrective既有`semantic`仅限private local deployment interface，central contracts/G2A仍N/A |
| 未授权 | fresh R7、S11、MiniMax、feature activation、真实数据、push、merge、tag、publish、deploy及其他远端写入；不得prune或删除volume |
| 保持状态 | `S10B-BLK-001–007 Closed`；G3 Partial、G4/G6 Pending；完整S10B-001–012仍未PASS |

## 19. LIA-126-024 / DEC-126-064 — S10B-R7 Owner Closure Review（Accepted Option A）

| 项目 | 结论 |
|---|---|
| 授权状态 | `LIA-126-024 CONSUMED 2026-08-09 / EXECUTED-BLOCKED / R7 CLOSURE NOT ESTABLISHED` |
| 固定候选 | Governance `3d82cda4c3c06928e0111bc1697b0153e8ef76a2`；Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`；Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`；Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；执行前及治理编辑前均exact/clean |
| 执行事实 | Docker client/server `29.6.1`、Compose `5.3.0`、daemon access PASS。canonical run `d553e6ea-e10f-4470-b357-a41807d6fb06`的唯一preflight PASS；summary SHA-256 `de994e3dd155e13ab27d7bb9c8645e4807e050b88fc9b300bdf62bd000612b80`，resolver evidence SHA-256 `c424a4e8e0deb405c713bc689821973f2d99b91f9ef5826d44a88e16a0177e9e` |
| 停止事实 | `S10B-002 FAIL-CLOSED`：已提交的唯一continuation只启动API，治理process manifest不是可执行authority，七仓没有完整四组件orchestrator。API continuation、Host、Desktop、Runtime及业务case均未启动；003–011 NOT RUN；012仅完成abort cleanup subset |
| 安全/清理 | 8个允许的日志/证据对5个生成secret和664个冻结payload值命中0；bearer/DSN/private-key命中0。run container/network/process/listener均0，4个named volumes与owner-only ignored run root保留，daemon=`6 containers / 0 running / 6 images`，无retry/prune/volume deletion |
| Governance gates | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及`git diff --check`全部PASS |
| 状态 | `s10b_r7_executed=true`；`S10B-BLK-008 Open`；G3 Partial、G4/G6 Pending；contract-impact=`none` for execution/governance，central G2A unaffected |
| Owner决定 | DEC-126-064 Option A Accepted：接受fail-closed事实但拒绝R7 Closure；保持`S10B-BLK-008 Open`，只单独授权DESIGN-126-014设计评审。不得以API-only launcher或手工命令拼接续跑 |
| 禁止 | 不自动corrective或fresh R8；不执行S11、MiniMax、真实数据/Keychain、default activation、commit、push、merge、tag、publish、deploy或其他远端写入 |

## 20. DESIGN-126-014 / DEC-126-065 — Orchestrator Design Review

| 项目 | 结论 |
|---|---|
| 评审范围 | 只读检查Infra/API/Host/Desktop/Runtime真实启动、ready、native auth/project、process evidence与cleanup入口；只更新FEAT-126九个治理文件 |
| 设计选择 | 一个Infra-owned operator entry，输入仅canonical run ID与七仓full SHA；内部消费same-run preflight；Infra启动依赖/API/fake/Desktop，Desktop唯一启动Host，Host唯一启动pinned Runtime |
| 必需corrective | Infra closed orchestrator；Desktop non-publishable test build与真实Vue/Pinia/Tauri driver、synthetic PKCE/project binding；Host Runtime child与fake mode-generation evidence；API-owned Tasks/audit/idempotency verifier |
| State/evidence | 固定S10B-002–012顺序、planned restart显式状态、unexpected failure立即abort、existing run只reconcile；versioned 0600 closed artifacts、PID/PPID/binary/nonce/port/profile binding、payload/secret hit=0 |
| Contract impact | 本次评审`none`；未来corrective=`semantic`仅限private local test/deployment interface与Desktop test-driver IPC；central contracts/G2A N/A；发现public wire/durable schema影响必须停止重审 |
| Governance evidence | feature package default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`首轮及证据登记后复跑均PASS |
| 当前状态 | `DEC-126-067 Accepted / DESIGN-126-014 Complete / LIA-126-025/S10BO1 Corrective Closure Passed / Local Clean Checkpoints Formed / S10B-BLK-008 Closed / G3 Partial / G4/G6 Pending` |

## 18. DEC-126-065 / LIA-126-025 实施结论

- Owner接受DEC-126-065 Option A并仅授权S10BO1 repository corrective；未授权Docker live、isolated live或fresh R8。
- Infra、API、Host、Desktop已按DESIGN-126-014实现；Contracts与Runtime源码、公共wire、durable schema、Compose pin及默认flags未修改。
- contract-impact=`semantic`，仅覆盖private FEAT-126 local test/deployment interface与non-publishable Desktop test-driver IPC；central contracts/G2A=`N/A`。
- S10BO1-001–014 targeted matrix 14/14 PASS，四仓新增针对性测试、lint/build及Desktop default/feature build均PASS。
- FEAT-126 Governance default、strict、G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`在证据登记后最终复跑均PASS。
- 最终无沙箱能力复验确认Docker/Compose/daemon、loopback、SQLCipher/file security、bookmark与子进程能力均可用；API/Host/Desktop/Infra全量门禁和S10BO1 14/14全部PASS。Desktop首次默认clippy失败的根因是两个仅driver使用的方法缺少相同feature cfg，Owner另行授权的最小修复已通过default/feature全套回归；DEC-126-066现已接受Corrective Closure并关闭`S10B-BLK-008`。
- isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用、commit及任何远端写入仍未授权。
| 禁止 | 本轮不实施、不启动Docker/服务、不跑isolated live或fresh R8，不执行S11/MiniMax/真实数据/default activation/commit/远端写入 |

## 21. DEC-126-066 — S10BO1 Corrective Closure（Accepted）

| 项目 | 结论 |
|---|---|
| Owner决定 | 接受LIA-126-025/S10BO1 Corrective Closure；确认能力前置、API/Host/Desktop/Infra全量门禁、S10BO1-001–014及Governance证据PASS |
| Blocker | `S10B-BLK-008 Closed`；S10BO1 repository corrective不再阻塞下一次独立授权评审 |
| Gate状态 | G3 Partial、G4/G6 Pending；完整fresh S10B-001–012仍未PASS |
| Contract impact | Owner治理处置=`none`；已接受实现仍为private local test/deployment与non-publishable Desktop test-driver IPC `semantic`，central contracts/G2A=N/A |
| 未授权 | isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用、prune、volume删除、commit、push及其他远端写入 |
| Post-decision governance | PASS：default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`均已重新执行并通过 |

## 22. DEC-126-067 — Local Clean Checkpoint Closure（Accepted）

| 项目 | 结论 |
|---|---|
| Owner决定 | 仅执行DEC-126-066后的local clean checkpoint closure；不得执行isolated live或fresh R8 |
| 实现checkpoints | API `451940b282d8dd3e232ed414bd44b0677897f4c4`；Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`；Desktop `d51e435cb8ea224e69f9707831ee71022d0a7b6e`；Infra `0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c` |
| Governance checkpoint | 包含DEC-126-067与上述精确SHA的本地yijie commit；因commit不能嵌入自身SHA，精确值在执行报告中回报 |
| Gate证据 | API/Host完整contract/lint/race/build；Desktop 167/167 TS、default 129 PASS/3 ignored、feature 131 PASS/3 ignored、driver 2/2与bundle absent；Infra validate/Compose semantic/142/142、S10BO1 14/14；Governance全部门禁PASS |
| 保留状态 | Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`与Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` unchanged/clean；`S10B-BLK-008 Closed`；G3 Partial、G4/G6 Pending |
| 未授权 | isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用、prune、volume删除、push、merge、tag、publish、deploy及其他远端写入 |

## 27. DEC-126-068 / DESIGN-126-015 / LIA-126-026 S10BO2

| 项目 | 决定与证据 |
|---|---|
| Owner决定 | DEC-126-068接受Desktop + Infra跨仓corrective评审Option A；DESIGN-126-015 Complete；LIA-126-026/S10BO2仅授权repository corrective |
| 实现状态 | Desktop实际feature-only bootstrap、OIDC authorization-code + PKCE、trusted tenant/project native bookmark、Vue/Pinia/Tauri driver与FD3/FD4控制通道完成；Infra startup/abort runner、closed frame/state、ownership与cleanup完成 |
| Checkpoints | Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`；Infra `0fed8187d6051c011e67142d90feff89de326cfe`；Contracts/API/Host/Runtime本轮源码不变 |
| Contract impact | `semantic`，仅private local deployment/test与non-publishable driver IPC；public wire、durable schema、Runtime源码/pin、Compose pin和默认flags不变；central contracts/G2A=N/A |
| 验证 | Desktop完整lint/test/build、default/feature Cargo与driver/bundle门禁PASS；Infra validate/lint/test 162/162，S10BO1 14/14 + S10BO2 20/20 targeted PASS；no-log与`git diff --check` PASS |
| 当前风险 | `S10B-BLK-009 Closed`：Owner已接受repository Corrective Closure；isolated live startup/abort与fresh R8仍无执行证据，且均未授权；`s10b_r8_executed=false` |
| 当前授权 | Owner本轮另行允许将现有FEAT-126候选commit推送至对应远端分支；该授权不包含merge/tag/publish/deploy、isolated live、fresh R8、业务调用、S11、MiniMax、真实数据/Keychain或默认启用 |
| 状态 | `LIA-126-026/S10BO2 Corrective Closure Accepted`；`S10B-BLK-009 Closed`；G3 Partial、G4/G6 Pending |
| Owner Closure | Desktop feature Rust 143 PASS/0 FAIL/3 ignored、Infra 162/162、S10BO1+S10BO2 34/34及no-log/driver-absent/ownership/cleanup证据获接受；不等于isolated live、fresh R8、G4或G6 PASS |
| Post-decision Governance | default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check`全部PASS |

## 28. LIA-126-027 / S10BO2 Isolated Live Failure

| 项目 | 事实与处置 |
|---|---|
| Authorization | 单次startup/abort isolated live授权已消费；run `b68804f0-aaf9-4da4-95e1-aa3b605bfada`不得重试、续跑或复用 |
| Preconditions | 七仓exact/clean；Docker client/server 29.6.1、Compose 5.3.0、daemon、loopback、SQLCipher/文件属性、native bookmark、subprocess全部PASS |
| Closed result | `orchestrator_cleanup_unknown`；isolated live Closure FAIL；`DEC-126-069 Pending Owner Review` |
| Root cause | `executePreflight`只向子进程环境提供`FEAT126_S10B_*`，却调用要求`GOVERNANCE_SHA`等Make变量的`feat-126-s10b-preflight`；子Make在run root创建前拒绝。初始cleanup仍设置`composeAttempted=true`，absent-run stop失败后cleanup leaf覆盖原始preflight leaf |
| Evidence gap | run root、五份process identity与no-log roots不存在；因此不得声明精确process cleanup或完整no-log PASS，也不得手工kill未知PID |
| Observed containment | run project container/network/volume=0；5432/8443/9443/18080/18081/18082 listener=0；daemon前后均6 containers/0 running/6 images；未启动服务或业务调用 |
| Blocker | `S10B-BLK-010 Open`：需要独立Infra corrective评审，同时修复preflight authority forwarding、原始failure preservation与pre-run cleanup evidence semantics |
| Retained state | `S10B-BLK-009 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false`；fresh R8/S11/MiniMax/真实数据/Keychain/默认启用未授权 |
| Governance verification | default、strict、G2A、unique-key YAML、lint、test、shell syntax和`git diff --check`首轮及本行回写后的最终复跑均PASS |

## 29. DEC-126-069 / DESIGN-126-016 / LIA-126-028 S10BO3 Corrective

| 项目 | 决策与证据 |
|---|---|
| Decision | Owner采用Option A：保留LIA-126-027失败事实和不可复用run ID，接受完整Infra corrective设计并授权实施；不得直接重跑isolated live |
| Root-cause set | 七SHA跨Make边界丢失是触发原因；同时确认provisional Compose状态、primary failure覆盖、pre-run evidence、attempt reuse、partial startup、partial run-root、Make trailer、phase descendant及secondary failure持久化九类闭合缺口 |
| DESIGN-126-016 | 七SHA作为唯一Make assignments传递；严格解析JSON加唯一已知Make trailer；分离`composeAttempted`与`composeCleanupRequired`；primary始终权威，cleanup/no-log/evidence/parent仅作为secondary |
| Durable authority | canonical run attempt以`O_EXCL`消费，0700目录/0600 canonical JSON；marker、failure、closure由SHA-256绑定并拒绝symlink、hardlink、mode、script/binary drift及覆盖 |
| Cleanup/no-log | 区分`pre_run_absence`、`preflight_artifacts`、`run_artifacts`及`attempt_only` coverage；named volume按exact before/after set验证；未知Docker/listener/process identity或不完整descendant证据保持fail closed |
| Retry boundary | existing run只允许phase-aware exact reconcile cleanup，不resume、continue、retry或进入业务case；失败run `b68804f0-aaf9-4da4-95e1-aa3b605bfada`永久不可复用 |
| Verification | Node syntax PASS；Infra `pnpm validate`、`make lint`、`make test` `186/186 PASS`（严格Darwin vmmap能力提升后）；四个targeted文件 `65/65 PASS`，S10BO3-001–020全部PASS；Compose semantic与`git diff --check` PASS；Docker live NOT RUN |
| Contract impact | `semantic`，仅private FEAT-126 local deployment/test interface；central contracts、Public Tasks/Host wire、durable schema、Runtime源码/pin、Compose pin及default flags不变，G2A=N/A |
| Current state | `DEC-126-069 Accepted Option A`；`DESIGN-126-016 Complete`；Owner已接受`LIA-126-028/S10BO3 Corrective Closure`；`S10B-BLK-010 Closed` |
| Retained gates | `S10B-BLK-009 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false`；isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、commit及远端写入未授权 |
| Governance verification | 本节证据登记后，Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check`全部PASS |

## 30. DEC-126-070 / S10BO3 Local Clean Checkpoint Closure

| 项目 | 决策与证据 |
|---|---|
| Owner决定 | 仅执行S10BO3 Corrective Closure后的Infra与Governance local clean checkpoint closure；不得执行isolated live或fresh R8 |
| Scope | 七仓HEAD与worktree复核通过；仅Infra五个S10BO3 corrective文件及Governance既有九份FEAT-126治理文件进入提交，Contracts/API/Host/Desktop/Runtime保持既定clean checkpoint |
| Verification | Infra Node syntax、`pnpm validate`、`make lint`、`make test` `186/186`、四文件targeted `65/65`、Compose semantic与diff PASS；Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与diff PASS |
| Clean checkpoints | Infra=`91f7ec03372b1528abb93818abfad432a83327c4`；Governance=包含本记录与Infra精确SHA的本地commit，精确SHA在提交后报告，因为commit不能嵌入自身SHA |
| Retained state | `S10B-BLK-009/010 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false`；失败run永久不可复用 |
| Exclusions | 未执行Docker live、isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、prune或volume删除；两个checkpoint均local/not pushed，无其他远端写入 |

## 31. LIA-126-029 / Second S10BO3 Isolated-Live Failure

| 项目 | 事实与处置 |
|---|---|
| Authorization | 单次startup/abort isolated-live授权已消费；run `8b94dc6d-5984-4579-9e0c-bed43a4b872f`不得重试、续跑或复用 |
| Fixed references | Governance `f7532cc9d138a2215f75441a737be4079642ed0e`；Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `451940b282d8dd3e232ed414bd44b0677897f4c4`；Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`；Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`；Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra `91f7ec03372b1528abb93818abfad432a83327c4`；执行前均exact/clean |
| Closed result | `orchestrator_process_identity_unknown`；失败发生在attempt marker与preflight之前；component startup、ownership、readiness和abort均NOT RUN |
| Root cause | canonical Make target用相对`node`启动orchestrator；Darwin `ps -p <pid> -o comm=`返回`node`而非绝对可执行文件路径，absolute binary identity无法建立。旧claim顺序又在身份解析后才创建attempt marker，导致此类早期失败没有持久证据 |
| Business boundary | Public Tasks、conversation、turn、provider调用均为0；business cases disabled；fresh R8 NOT RUN；`s10b_r8_executed=false` |
| Observed containment | run project container/network/volume与固定listener观测均为0；run root、attempt/failure/closure文件均不存在 |
| Evidence limit | 正式cleanup与no-log Closure均NOT ESTABLISHED；零资源观测不得替代缺失的identity、ledger、no-log或cleanup证据 |
| Blocker | `S10B-BLK-011 Open`：canonical Node必须提供绝对身份，且run须在可能失败的进程身份检查前形成不可变预占与content-free failure evidence |
| Stop | 本次授权已消费；不得现场修复后重跑、resume、复用run ID或进入业务case |

## 32. DEC-126-071 / DESIGN-126-017 / LIA-126-030 Corrective

| 项目 | 决策与证据 |
|---|---|
| Owner decision | 单独授权一个repository corrective，修复canonical Node绝对身份获取与ledger创建前失败无持久证据；后续checkpoint授权表明Corrective Closure已接受 |
| DESIGN-126-017 | Make入口用`command -v node`解析并校验绝对路径，再以该路径启动orchestrator；run在进程身份与script digest检查前写0600、O_EXCL、canonical preclaim |
| Failure evidence | marker前失败写入严格content-free `preclaim-failure.v1.json`，只含run、status、failure class、`s10b_r8_executed=false`与preclaim SHA-256；失败preclaim永久阻断执行，不完整preclaim保持fail closed |
| Compatibility/no-log | preclaim纳入attempt-only、preflight与full-run no-log source set；legacy marker-only attempt仍可读取/reconcile，不改变既有公共或业务接口 |
| Verification | Infra Node syntax、`pnpm validate`、`make lint`、Compose semantic、`make test` `188/188`、四文件targeted `67/67`、绝对Node self identity、`git diff --check`全部PASS |
| Contract impact | `semantic`，仅private FEAT-126 local deployment/test interface；central contracts、Public Tasks/Host wire、durable schema、Runtime source/pin、Compose pins和default flags unchanged；G2A=N/A |
| Closure | `LIA-126-030 Corrective Closure Accepted`；`S10B-BLK-011 Closed`；没有新live/runtime evidence，G3 Partial、G4/G6 Pending |
| Exclusions | 未执行Docker/isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用或远端动作 |

## 33. DEC-126-072 / Infra and Governance Clean Checkpoints

| 项目 | 决策与证据 |
|---|---|
| Owner decision | 仅形成新的Infra/Governance local clean checkpoint；在获得新SHA和另一份isolated-live授权前不得再次live |
| Scope | Infra仅`Makefile`、orchestrator及两个测试文件；Governance仅既有九份FEAT-126文件；Contracts/API/Host/Desktop/Runtime不变 |
| Infra checkpoint | `c7edbc344daecb84553efafe86dfe335a5c0c72d`；local、clean、not pushed |
| Governance checkpoint | 包含本记录与Infra精确SHA的本地commit；精确SHA在commit后报告，因为commit不能嵌入自身SHA |
| Verification | Infra full `188/188`、targeted `67/67`及全部静态门禁PASS；Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与diff PASS |
| Retained state | 两个isolated-live失败run均永久不可复用；`S10B-BLK-009/010/011 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false` |
| Stop | 不授权新的live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、push、merge、tag、publish或deploy |

## 34. LIA-126-031 / Third S10BO3 Isolated-Live Failure Audit

| 项目 | 事实与处置 |
|---|---|
| Authorization | 单次startup/abort isolated-live授权已消费；run `056a4dab-6afc-45ff-bfff-d1fcc67d2394`不得重试、续跑或复用 |
| Fixed references | Governance `b89982af406f849aa3c6ab023ff405068ebbae3d`；Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`；API `451940b282d8dd3e232ed414bd44b0677897f4c4`；Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`；Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`；Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra `c7edbc344daecb84553efafe86dfe335a5c0c72d` |
| Primary failure | `orchestrator_control_eof` at `desktop_spawned`；Desktop process record存在，但Host/Runtime/readiness/abort未建立 |
| Root cause 1 | Desktop secure-storage profile仅接受`std::env::temp_dir()`下的run root，而canonical Infra root位于repository generated tree；driver在Tauri/WebView与Host启动前以invalid configuration退出 |
| Root cause 2 | completed no-log scan以`hit_count=1`失败且保留known `run_artifacts` scope；closure/reconcile validator错误拒绝“failure class + known scope”，产生`orchestrator_attempt_evidence_invalid`并使closure缺失 |
| Evidence gap | legacy `runtime-log-scan.v1.json`只有aggregate hit count；containers已移除，命中规则类别与来源无法离线可靠恢复，不得猜测或输出业务日志正文 |
| Durable facts | preclaim/attempt/failure均0600；attempt SHA-256=`aeda68a329e6d68c7d7a47c65c58668fbc5d61c2a76e40199366940b90729a8a`；failure SHA-256=`7f5afa4f4804ff193537589ff5fb88440f8059e5c7f520f003e057237722ed7d`；business boundary前后摘要相同且provider calls=0 |
| Retained resources | run对应四个Compose named volumes仍存在且labels/project identity精确；本次审计只读，未start/stop/reconcile/delete/prune或读取volume内容 |
| State | business cases disabled；Public Tasks/conversation/turn/provider calls=0；`s10b_r8_executed=false`；Closure FAIL事实保留 |

## 35. DEC-126-073 / DESIGN-126-018 / LIA-126-032 Minimal Corrective

| 项目 | 决策与证据 |
|---|---|
| Owner decision | 在离线根因与文件范围确定后，单独授权并完成最小Desktop + Infra repository corrective；不得再次live |
| Desktop scope | 仅`src-tauri/src/feat126_secure_storage.rs`：feature-gated、ephemeral-only、UUIDv4-bound canonical Infra suffix；default/Keychain保持fail closed，cleanup使用同一校验 |
| Infra scope | 仅orchestrator与S10BO3测试：修复known-scope failure closure/reconcile；runtime log scan写v2 content-free unique source/rule set digests并兼容legacy v1 |
| Verification | Desktop lint/test/build PASS：TS `174/174`、default Rust `134/134` + 3 ignored、feature Rust `144/144` + 3 ignored；Infra validate/lint/Compose semantic与`189/189` PASS；S10BO3 `27/27` PASS |
| Contract impact | `semantic`，仅private FEAT-126 local deployment/test interface；central contracts、public wire、durable schema、Runtime/Compose pins和default flags unchanged；G2A=N/A |
| Closure | repository Corrective Closure Accepted；`S10B-BLK-012 Closed`；没有产生新的runtime/live evidence，G3 Partial、G4/G6 Pending |
| Checkpoints | Desktop `9771da11c47406e45526dea104f3d7de05701fba`；Infra `61062143fa3c81b90792ec6f48aea7d6408ed06d`；均local、clean、not pushed |
| Stop | run `056a4dab-6afc-45ff-bfff-d1fcc67d2394`永久不可复用；another isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用与远端动作均未授权 |

## 36. DEC-126-074 / Desktop, Infra and Governance Clean Checkpoints

| 项目 | 决策与证据 |
|---|---|
| Owner decision | corrective全门禁通过后，仅形成Desktop、Infra和Governance三个local clean checkpoints |
| Exact SHAs | Desktop `9771da11c47406e45526dea104f3d7de05701fba`；Infra `61062143fa3c81b90792ec6f48aea7d6408ed06d`；Governance为包含本记录的本地commit，精确SHA在commit后报告 |
| Unchanged | Contracts/API/Host/Runtime保持既定exact clean SHA；失败run evidence与四个retained volumes保持原样 |
| Verification | Desktop与Infra完整门禁、targeted回归和diff PASS；Governance default/strict/G2A、unique-key YAML、lint/test、checker shell syntax与diff PASS |
| State | `S10B-BLK-009/010/011/012 Closed`；G3 Partial、G4/G6 Pending；`s10b_r8_executed=false` |
| Stop | no automatic live；新的isolated-live必须使用本轮全部新exact SHA并取得另一份一次性授权；fresh R8与所有远端/发布动作未授权 |

## 37. DEC-126-075 / DESIGN-126-019 / LIA-126-033 Unified Startup-Surface Corrective

| 项目 | Owner决定与边界 |
|---|---|
| Status | `DEC-126-075 Accepted as authorization / DESIGN-126-019 Complete / LIA-126-033 Implementation Complete / Corrective Closure Review Ready / Owner Acceptance Pending` |
| Scope choice | 采用一次性Desktop + Infra最小corrective，覆盖同一startup阶段中已知的failure projection、frame race、Docker log authority与no-log误报/漏报边界；不再为每个已知leaf拆分一轮repository corrective |
| Desktop | 产品范围严格为`feat126_s10_driver.rs`、`lib.rs`、`s10b-driver.ts`、`main.ts`。所有ready前失败只能投影closed class，包含`driver_control_monitor_invalid`；frame不得包含错误正文、path、token、secret或业务内容；first terminal wins。成功写出`component_ready`后不得再发`startup_failed` |
| Infra control | 严格校验`startup_failed`及其authority，即使authority malformed也只能返回closed invalid class；Desktop写完整frame后立即退出时，reader必须先drain/判定frame，不能被child-exit race折叠为`orchestrator_control_eof`；合法Desktop leaf作为primary failure，EOF仅在没有合法frame时fallback |
| Infra no-log | writer使用`runtime-log-scan.v3`；Docker source必须同时匹配exact project、`FEAT-126`、`S10E`、run ID、`synthetic-only`和四个closed service roles，拒绝unknown/duplicate/malformed source；摘要按ASCII顺序绑定stable role origins、rule set和origin-rule pair set，container ID轮换不改变source digest |
| Value awareness | `/healthz`、`local`、空`argv`和content-free ready payload可通过；token、secret、DSN、private key、绝对本机路径及无法归类的高风险字段值仍失败。v3 evidence仅存counts/digests，不存raw log、规则正文、路径或业务内容；reader保持v1/v2/v3兼容 |
| Contract impact | `semantic`，仅不可发布的Desktop↔Infra private local deployment/test control/evidence interface；`yijie-contracts`不适用。Public Tasks HTTP、Host SSE、业务IPC、durable schema、Runtime source/pin、Compose pins和default flags不变，central G2A=`N/A` |
| Repository boundary | Contracts/API/Host/Runtime不得修改；若测试暴露其源码必须变化，立即停止并按超出最小corrective报告。历史failed runs、evidence和retained volumes不得修改、resume、reconcile或读取业务内容 |
| Verification/checkpoints | Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`：TS `178/178`、default Rust `134/3 ignored`、feature Rust `149/3 ignored`、targeted TS/Rust各`11/11`及lint/build/clippy/fmt/diff PASS。Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`：targeted `50/50`、full `192/192`、Node syntax、`pnpm validate`及diff PASS；独立审查的两个P1已关闭，无open P0/P1。Infra `make lint`在静态validate后因本机Compose discovery退出125，未启动容器，且在no-Docker边界下未重试/绕过。Governance default/strict/G2A/YAML/lint/test/shell/diff最终复跑PASS |
| Stop | 本轮严格offline repository work：禁止Docker、真实组件、isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、push、merge、tag、publish和deploy；`s10b_r8_executed=false` |

## 38. DEC-126-076 / LIA-126-033 Corrective Closure Owner Acceptance

| 项目 | Owner决定与证据 |
|---|---|
| Owner decision | 接受DESIGN-126-019 / LIA-126-033 Corrective Closure；environment-bound Compose semantic gap Closed |
| Fixed checkpoints | Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`；Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`；均local、clean、not pushed |
| Evidence accepted | Desktop targeted/full/build/clippy；Infra targeted `50/50`、full `192/192`；独立review无open P0/P1；Compose `5.3.0` direct config、Infra `make lint`和`make test` `192/192` PASS |
| Preserved gap | 真实Tauri `AppHandle/setup` direct fixture仍为P2/live，不得把repository closure写成真实startup PASS |
| Gate state | G3 Partial；G4/G6 Pending；`s10b_r8_executed=false` |
| Next authorization | Governance形成包含本记录的local clean checkpoint后，任何isolated-live都必须使用新七仓精确SHA并取得另一份一次性Owner授权 |
| Prohibited | no Docker lifecycle、isolated-live、fresh R8、business case、S11、MiniMax、real data/Keychain、default activation、push/merge/tag/publish/deploy |

## 39. DEC-126-077 / DESIGN-126-020 / LIA-126-035 Corrective Closure Owner Acceptance

| 项目 | Owner决定与证据 |
|---|---|
| Owner decision | 接受DESIGN-126-020 / LIA-126-035 Desktop+Infra unified Corrective Closure；关闭`S10B-BLK-013`；仅授权Governance记录和一个local clean checkpoint |
| Preserved failure | LIA-126-034 run `41cdd1c7-e1a6-43ae-ac3a-706ff6989e99`保持FAIL、永久不可重试/续跑/复用；历史evidence与retained volumes保持不变 |
| Fixed checkpoints | Desktop `713bd5a2985c491db5d6cfc3e31f8f509994427d`；Infra `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`；均local、clean、not pushed |
| Corrective accepted | Desktop startup stage/watchdog、panic/page-load/frontend/first-IPC closed projection、real Tauri mock fixture、first-terminal/FD4 close；Infra primary-before-cleanup durability、pre-ownership known scope、FD4/child ordering、runtime-log-scan v3 field-class digests与Caddy nested value-aware classification |
| Verification | Desktop targeted TS `12/12`、frontend `179/179`、default Rust `134 pass/3 ignored`、feature Rust `152 pass/3 ignored`、real Tauri fixture `1/1`、lint/clippy/build PASS；Infra BO2/BO3 targeted `51/51`、full `193/193`、lint/syntax/Compose `5.3.0` config semantic/diff PASS；独立只读review无open P0/P1 |
| Governance verification | feature package default、strict、G2A、unique-key YAML、`pnpm lint`、`pnpm test`、checker Shell syntax及`git diff --check`全部PASS |
| Contract impact | governance disposition=`none`；被接受实现为private non-publishable Desktop↔Infra `semantic`；central contracts/G2A=N/A，Contracts/API/Host/Runtime无需修改 |
| Gate state | G3 Partial；G4/G6 Pending；`s10b_r8_executed=false`；真实isolated-live startup/ownership/readiness/abort/cleanup PASS仍待新的单次授权 |
| Governance checkpoint | 包含DEC-126-077及上述精确实现SHA的本地commit；自身SHA在commit后报告，不在commit内容中自引用 |
| Prohibited | no Docker lifecycle、isolated-live、fresh R8、business case、S11、MiniMax、real data/Keychain、default activation、push/merge/tag/publish/deploy or other remote operation |

## 40. DEC-126-078 / DESIGN-126-021 / LIA-126-036 Two-stage v4 Authority and Infra Corrective

**Status**: Accepted 2026-08-12

**Decision**:

1. 先仅更新现有FEAT-126 Governance文档与`feature.yaml`，将runtime-log-scan writer权威升级为schema v4；Governance基线精确固定为`5da2d93b7c4e3ee9884b0fedb04261b5aaf65f92`。
2. v4采用14个exact keys，在explainable v3上只新增`hit_reason_class_set_sha256`与`hit_origin_rule_field_class_reason_class_set_sha256`。writer只发出v4；reader继续接受v1、v2、legacy v3、explainable v3与v4，不接受其它key组合。
3. 固定reason classes为`literal_authority_match`、`local_machine_path_value`、`sensitive_nonempty_value`、`unclassified_context_value`、`unclassified_caddy_system_value`、`unstructured_pattern_match`。未知Caddy结构继续fail closed，不能靠修改Caddyfile或放宽规则消除门禁。
4. `hit_count=0`时，origin、rule、origin-rule、field-class、origin-rule-field-class、reason-class及origin-rule-field-class-reason-class七项hit集合摘要全部等于空串SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`；`hit_count>0`时当前schema中存在的全部hit摘要必须为非空集合摘要。
5. evidence只允许counts和稳定摘要。禁止记录原始字段名、值、路径、日志正文、token、secret或业务内容；exact Docker authority与stable ASCII origin排序不变。
6. production Desktop cargo build authority固定为精确features `feat126-s10-driver,tauri/custom-protocol`，缺一或顺序/集合不符均fail closed；不得依赖Vite dev server或1420/1421。
7. Infra `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`允许保持四个既有预期dirty文件，Governance阶段不得修改或提交这些文件。Governance门禁和local checkpoint完成后，恢复同一Infra diff，完成剩余门禁、独立只读审查并创建一个Infra local clean checkpoint。

**Risk controls**:

- 该变更为private local evidence interface的semantic变更；central Contracts/G2A、Public Tasks、Host/Runtime与产品默认行为均N/A/unchanged。
- 不在Governance checkpoint中虚构未来Infra commit SHA；最终SHA只能在Infra commit形成后报告。
- 不执行Docker lifecycle、isolated-live、fresh R8、业务case、S11、MiniMax、真实数据、Keychain、默认启用或远端操作；`s10b_r8_executed=false`。
