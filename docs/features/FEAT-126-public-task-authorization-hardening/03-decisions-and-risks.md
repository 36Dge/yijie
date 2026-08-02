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
| DEC-126-022 | FEAT-126交付模式与本地契约消费 | 生产发布型 / 本地可运行但仍强制tag/publish / Local-only Delivery | 采用**Local-only Delivery Strategy**：目标是在Owner本机完成API/Host/Desktop/Runtime构建启动和完整本地E2E；未来明确授权的本地draft consumer只固定`c000a0245acb5c3f7ead5d2a877fb60c281c588c`，可用完整SHA、已核验sibling path、workspace/path dependency、生成SDK或已核验本地tarball，浮动branch不能作为不可变身份。merge不再是开始本地draft实现的前置，但仍须满足DEC-126-021并单独审批；本期tag/package publish/registry/线上部署/生产灰度/生产启用/云数据库/真实用户数据均N/A。先用fake provider/fixtures；本地链路完成后最多一次MiniMax local smoke另行审批 | 单机开发无需为本地运行引入registry与生产发布成本；完整SHA和本地制品足以保持可复验。把merge与deployment解耦既允许稳定候选上的本地draft实现，又不绕过远端红灯。G5明确N/A，G6只表示本需求范围内Local-only Delivery Complete，不冒充Production Ready；未来产生线上意图必须重开生产轨 | 段成威 | Accepted 2026-08-02；LIA-126-001后续仅授权并完成S4–S6；MiniMax及S7–S11仍未授权 |
| DEC-126-023 | Public Tasks `input` 与本地会话数据权威冲突 | A. 保留`c000a024`并允许任意task input/正文；B. 保留`c000a024`但只约束Desktop不调用；C. 以新commit取代候选，将v2 request/response/fixtures收窄为content-free metadata/reference | **推荐C并暂停S4–S11**：`c000a024`保持不可变且不追加push；在Owner批准前不修改contracts。新候选必须使prompt、message、raw reasoning、title派生正文和项目路径不能进入`/v2/tasks`或PostgreSQL，只允许closed、content-free metadata/reference；重新生成SDK、更新fixture、做supported-baseline breaking/semantic review并取得新的完整SHA和G2A批准。若Owner选择B，必须明确Public Tasks不是local conversation数据面、Desktop不得调用该operation，并重新评审当前`conversation` fixture及S4 provider接受任意input的风险 | immutable source在`CreateTaskV2Request.input`和`TaskV2.input`上使用`additionalProperties:true`，权威fixture以`task_type=conversation`携带`input.text`并在response回显；这与ADR-0013/DEC-126-014及LIA-126-002“正文不得进入Public Tasks/PostgreSQL”直接冲突。仅在provider里私自拒绝`text`会收窄已批准wire语义并造成契约漂移 | 段成威 | Ready for Owner Approval 2026-08-02；G2A re-review required；LIA-126-002依停止条件暂停 |

## 3. ADR 判定

- 是否改变既有 Accepted ADR：不削弱 ADR-0012；Accepted DEC-126-001 保留其 FEAT-126 安全责任。若未来改成迁号，必须重开 G1、形成新 Accepted ADR 并同步全部 FEAT-125 引用。
- 是否改变跨仓职责/数据权威：是。ADR-0013 已接受 Desktop embedded SQLite 为 confidential conversation authority，并明确 PostgreSQL/Redis/pgvector/bbolt 的非替代职责；ADR-0015 冻结隔离标题，ADR-0016/DEC-126-016 冻结 Host raw-reasoning展示与Desktop SQLCipher历史权威。DESIGN-126-003/DEC-126-017现已提交 exact v2/schema/caps候选；Public Tasks ownership/auth由DEC-126-011/012提交批准。
- 是否改变 Accepted Design Pattern：是。Chat 1.1.0 的 active state 要附件/右侧面板，App Shell 2.0.0 有全局收起；必须在代码前形成新候选版本并由段成威接受。
- ADR/Decision 结论：ADR-0013/0014/0015/0016与DEC-126-011/012/016/017/018/019/020/021/022均已Accepted；Chat/App Shell Pattern已批准。LIA-126-002审计发现Public Tasks正文边界与immutable candidate冲突，已提交DEC-126-023等待Owner决定。G2保持Passed；原G2A批准作为历史事实保留，但继续实施所需的source-contract readiness已进入re-review。
- G2A/local 结论：`c000a0245acb5c3f7ead5d2a877fb60c281c588c`仍是未被修改的既有candidate，Draft PR与远端状态不变；它目前不能同时证明“arbitrary `input`”与“content-free-only”两种语义。S4/S5/S6统一调整为`Conditional / Corrective Closure Required`，G3保持Partial，G4/G6保持Pending；在DEC-126-023获批并形成新G2A结论前暂停LIA-126-002代码纠偏与S7–S11。
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
| R-126-017 | Public Tasks arbitrary `input`使conversation正文进入PostgreSQL或response | high | critical | DEC-126-023；contract schema/fixture与ADR-0013同向；provider/consumer conformance；route保持off | canonical fixture、generated DTO、repository payload scan | 暂停S4/S7；保留`c000a024`不可变；形成新candidate或明确隔离Public Tasks数据面 | 段成威 | critical / blocks G2A continuation |

## 5. 威胁建模

| 资产/边界 | 威胁 | 攻击路径 | 服务端/原生控制 | 安全测试 | 残余风险 |
|---|---|---|---|---|---|
| Public Tasks | spoofing/IDOR | 无 bearer、伪 tenant、猜 UUID | Principal + tenant scope + AuthorizationService + scoped query | SEC-001–006 | unknown consumers |
| Local DB | information disclosure | 切 tenant、直接 Tauri invoke、复制 DB | Rust-owned narrow commands、owner-only app data、row scope | SEC-007–010 | OS account compromise |
| Agent Host token/key | credential theft | WebView storage/log/URL/child env inheritance | Rust only、0600/0700、redaction、env allowlist | SEC-011–013 | same-user malware |
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
| title | model/fallback/user | 列表与路由标题 | Desktop local DB | Public Task 是否同步为 Open | 同 session | cascade | source/version/outcome |
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
- 试图在未批准新候选流程的情况下修改`c000a0245acb5c3f7ead5d2a877fb60c281c588c`、追加push到固定candidate branch或替换唯一candidate；
- 试图把浮动branch当作契约身份、把本地路径投影当作第二权威源，或在LIA-126-001范围外修改Runtime/Infra及S7–S11业务代码；
- 试图把Local Runtime Ready当成线上部署/Production Ready，或在没有新审批时调用MiniMax、配置registry、接入云数据库/真实用户数据；
- 后续consumer试图固定非`c000a0245acb5c3f7ead5d2a877fb60c281c588c`的候选，或未核对已批准digest；
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
| G2A final source-contract readiness | 段成威 | Approved / Passed；唯一source-contract candidate已确认 | 2026-08-02 | DEC-126-019；`c000a0245acb5c3f7ead5d2a877fb60c281c588c`；不授权push/tag/merge、downstream pin、业务编码或生产启用 |
| Source-contract remote availability | 段成威 | Approved / Complete；仅专用candidate branch | 2026-08-02 | DEC-126-020；remote SHA匹配、clean clone全部门禁与摘要PASS；`origin/develop`未移动；无merge/tag/发布/pin/编码 |
| Source-contract Draft PR与CI观察 | 段成威 | Approved scope / Executed；PR #1固定唯一candidate，CI已到终态并回填 | 2026-08-02 | Draft PR `develop <- feat/feat-126-contract-candidate`；head精确匹配；run 30741466028在dependency audit失败；未重跑/豁免/修复/push/merge |
| Source-contract merge readiness | 段成威 | Approved DEC-126-021 / HOLD；当前不批准merge | 2026-08-02 | CI red；`brace-expansion 2.1.2` high；`govulncheck`与`origin/main` breaking skipped；不回退G2/G2A |
| Local-only Delivery Strategy | 段成威 | Approved / DEC-126-022 Accepted；交付目标改为Local Runtime Ready | 2026-08-02 | tag/publish/deploy/G5均N/A；G6为Owner本地验收；业务编码与一次MiniMax local smoke仍分别待批准 |
| Local Implementation Authorization | 段成威 | LIA-126-001 Executed；LIA-126-002 Approved but Paused by Stop Condition；仅S4–S6 corrective closure | 2026-08-02 | local WIP checkpoints complete；S4–S6 Conditional；无MiniMax/远端动作；S7–S11禁止 |
| Public Tasks input / G2A re-review | 段成威 | Pending Owner decision | N/A | DEC-126-023 Ready for Owner Approval；Q-017 Open；blocks LIA-126-002 continuation |
