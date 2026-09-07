# FEAT-152 — 最终验收结论

2026-09-08 后续交付已完成：用户授权后依次提交实现仓、固定实际依赖，普通易界App已打包并通过零付费启动/菜单/正常重启恢复检查。元仓最后固定本报告；详细提交和日常入口见 [本地交付报告](04-local-delivery.md)。原S4付费验收与本次交付检查分别记录，均不表示已推送或公开发布。

**FEAT-152 本地需求已完成，S1–S4、全部 Must AC 与严格 D4 均通过。** 原生真实人工接管缺口、严格 Clippy 和实际联调发现的 Native 策略转发遗漏均已关闭。最终严格D0/D4均exit 0，治理仓lint与50项测试通过；机器检查结果见 [D0 日志](evidence/stage4/final/governance-d0.log) 与 [D4 日志](evidence/stage4/final/governance-d4.log)。

累计授权 **45 次**，实际 **37 次**，剩余 **8 次**；所有父请求、审核子请求与后续请求均计数，已全部完成。最后追加授权后只用了2次补齐请求批准回归，不为用完额度继续调用。

| 最终真实流程 | 结果 |
|---|---|
| 帮我批准 → 原生拒绝 | 真实guardian返回deny、risk low；目标文件未执行，UI显示人工复核卡片。 |
| 点击批准本次 | 原生注入准确操作上下文恰好1次；本步骤不产生模型请求，也不直接执行文件。 |
| 同任务保持auto续跑 | 真实guardian依据准确人工批准返回allow，文件内容S4-manual-approved。 |
| 完全访问 | danger-full-access/never/user，普通文件准确写入S4-full-final。 |
| 切回请求批准 | 真实Runtime恢复workspace-write/on-request/user/network=false；项目内写入成功，公网HEAD批准HTTP200，项目外写入拒绝且文件未生成。 |
| 正常重启、任务隔离 | 最终任务保留4轮完成历史与ask；另一任务保留auto，新任务默认ask。 |

最终证据见 [逐项验收矩阵](evidence/stage4/final/acceptance-matrix.md)、[真实流程](evidence/stage4/final/real-flow.json)、[原生观察](evidence/stage4/final/runtime-observations.json)、[最终请求批准回归](evidence/stage4/final/ask-real-flow.json) 和 [完整计数账本](evidence/stage4/final/provider-requests.json)。四轮属于同一最终产品源码、同一验收任务的连续流程，正常退出/重启属于恢复验证；不冒称单一进程或把旧构建执行挪作本次执行。

严格Clippy、fmt、3项Native权限检查及相关派发查询检查、UI78项、Host聚焦race/lint、Contracts3项/生成同步和canonical构建通过。最终源码hash未变；视觉使用的生产组件/主题hash也已再次核对，分层验证范围见矩阵。五仓diff检查通过，Codex核心仓干净，retained Runtime/manifest校验值未改。

人工接管验收使用用户明确批准的**原生精确文件文档复核规则**，原安全规则原文完整保留，结果由真实guardian产生；这不代表默认策略自然风险拒绝。临时规则已撤除、未持久写入Runtime配置。没有伪造回调、危险操作、强杀或修改Codex核心。

首次完全访问真实取消/确认来自S3，S4复核相同生产组件；未重置用户标记。Native菜单截图受工具限制，亮暗最小窗口采用真实主窗口/AX与生产组件视觉证据，组件页不连接审批后端。未带phase的MiniMax文本仍显示既有未分类模型消息，验收依据真实配置/工具/文件结果。

应用与计数器均正常关闭，无相关端口监听。其它用户改动保留；没有提交、推送、发布或更改生产pin。交付为local demo_fast显式权限开关候选，D4不等同公开/生产批准。用户禁止的攻击/故障旧全量测试未执行，不声称全量suite通过。

此前35次用尽时的阶段性未通过结论保留在 [当时状态](evidence/stage4/final/verification-at35.md)；用户再次追加10次后，最终ask执行缺口已通过第36–37次真实请求关闭。首次配置转发失败24–27及原文件证据继续保留。

---

# 历史阶段记录（保留当时结论，当前状态以上方为准）

# FEAT-152 — 分阶段验证

最新收尾状态：用户明确授权处理两项剩余问题后，严格 Clippy 已修复并通过，`cargo fmt --check` 与 3 项相关 Native 测试通过。当前只剩 AC-003 的真实接管验收。用户没有现成拒绝任务，已授权构思正常场景；[原生临时文档复核规则方案](evidence/stage4/closeout/manual-takeover-plan.md) 及零付费 Runtime 配置联调已准备，正在等待该验收配置与追加额度确认。本轮新模型调用为 0，累计仍为 23/25；不能把配置探针视为真实拒绝通过。

## S1：最小跨仓集成已完成

只证明 Contracts → Host 适配 → 固定 Runtime 的配置兼容，以及 Native 存储/序列化和默认关闭界面保持可用。

| 检查 | 结果 | 证据 |
|---|---|---|
| S1 real retained Runtime configuration | PASS | 三档 thread/start 生效配置符合预期；未调用 turn/start；不是执行/恢复验收。 |
| S1 contract generation, lint and real observation conformance | PASS | 专属生成和规范校验通过，3 项测试通过。旧 v6 incidental 生成漂移恢复，未扩修退役资产。 |
| S1 Host compile/lint and callback mapping | PASS | 类型、vet、脚本语法与正常进程内回调测试通过；回调测试不是模型端审批 E2E。 |
| S1 native schema and SQLCipher boundary | PASS | 2 项通过，包括正常关闭/重开数据库；未宣称 Runtime 对话重启恢复。 |
| S1 default-off UI regression | PASS | 3 文件 67 项通过。初次未排除 .local 导致加载其它任务副本，52 个失败不属于当前 src；纠正选择范围后的结果独立记录。 |
| S1 Desktop lint and build | PASS | 通过；Vite 大 chunk 警告保留。 |
| Strict native Clippy | FAIL | 仅命中 database.rs 已存在的 8 元素 tuple type_complexity；HEAD 原源码对应 3195 行同样存在，未扩修无关基线。 |

## 提前发现的问题

1. 真实保留 Runtime 的 stable schema 没有 thread/settings/update；以实际生成的 267 文件为准，不根据当前源码目录假定可用 API。
2. 首次联调在零回合 thread/resume 返回 no rollout found。无回合没有可恢复 rollout；该失败日志保留。配置验证可独立完成，真实恢复必须在实际回合之后验证。
3. 严格 Clippy 存在原基线 type_complexity；未关闭 lint、未把 FAIL 改写为 PASS。

## S2：请求批准与任务交互已完成

| 检查 | 结果 | 证据 |
|---|---|---|
| 正常 canonical 启动 | PASS | `evidence/stage2/app-final.log`；旧固定对象、退役边界、真实 retained Runtime 全保留。 |
| 真实人工批准 | PASS | 完整命令可审阅；批准前文件不存在，批准后 `S2-approved`，退出码 0。 |
| 最终版本真实拒绝 | PASS | 普通项目外写入返回 `command_declined`，任务正常完成，文件不存在。 |
| 已完成任务正常重启续跑 | PASS | 首次未 resume 导致失败，修复后同一任务真实续跑并批准成功；不是完整恢复矩阵。 |
| 每任务模式保存与重启读回 | PASS | 原任务 auto，另一个新任务 ask；正常重启保留，验证后恢复 ask。仅配置验证，无 auto 执行。 |
| 实际运行/待审批与键盘交互 | PASS | 运行中和等待审批禁用模式；完成后恢复；选中项聚焦、方向键、Enter、Esc 实际操作通过。 |
| Host focused race tests / lint | PASS | 当前 turn 关联、RPC 写回后确认、同决策幂等及 admission 后的既有操作重放，见日志。 |
| Native focused tests | PASS | 2 项；新增未绑定任务安全空快照查询验证，SQLCipher 正常重开及两任务设置隔离。 |
| Desktop focused tests / lint | PASS | 6 文件 75 项；包含 8 项新权限/候选路径检查与原默认关闭回归。 |
| Contracts conformance | PASS | 3 项；实际 S1 Runtime 配置证据仍匹配。 |
| 调用计数 | PASS | `evidence/stage2/provider-requests.json`：6 个实际 Responses 请求均完成，10 次授权剩余 4 次。 |
| 治理包 D0 / diff 检查 | PASS | strict D0 与五仓 diff --check 通过；不是 D4 完成声明。 |
| 核心只读与正常退出 | PASS | `evidence/stage2/source-identities.json`：核心仓干净，binary/manifest hash 未变；应用及计数器正常关闭。 |

详细 UI 与文件观察见 [真实流程证据](evidence/stage2/real-flow.json)。第一次过度脱敏的请求已拒绝，第一次恢复失败的本地回合保留在真实历史中；没有删除失败记录或伪造为通过。修复后的批准与拒绝都使用真实模型产生的普通命令，不注入 Runtime 响应。

## S3：用户指定的三项顺序验证已完成

| 检查 | 结果 | 证据 |
|---|---|---|
| 无付费兼容性核对 | PASS | `evidence/stage3/compatibility-review.md`：审核模型选择、供应商/地址继承、审核自身重试和人工接管原生语义。 |
| 真实原生自动审核 | PASS | 原生 guardian 子会话 MiniMax-M3/minimax，read-only/never，返回 allow；普通文件写入结果 S3-auto；无人点击批准。 |
| 审核子请求计数 | PASS | 7/8/9 分别为父请求、结构化审核请求、后续回复，均经固定地址计数；与原生 guardian rollout 对应。 |
| 首次完全访问确认与取消 | PASS | 取消保留 auto，再选仍要求确认；确认后 full；确认过后不重复弹窗。新增 2 项交互测试通过。 |
| 完全访问实际执行 | PASS | 同任务第二轮 danger-full-access/never/user，写入 S3-full；请求 10/11 无审核子请求。 |
| 同任务切回请求批准 | PASS | 第三轮恢复 workspace-write/on-request/user/network=false；重新人工审批，拒绝后目标文件不存在。 |
| S3 聚焦检查 | PASS | 界面 77 项、Desktop lint、Host race tests/lint、Contracts 3 项；canonical 构建通过。 |
| 核心、预算与正常退出 | PASS | 核心仓与 Runtime hash 未变；本轮 7 次，累计 13/15，剩余 2；应用和计数器正常关闭。 |
| 自然自动拒绝后的真实人工接管 | NOT RUN | 本次原生审核返回 allow；只有原生语义核对和既有映射/拒绝单元测试，没有真实接管批准调用。未伪造回调或制造危险操作。 |

原生回合和 guardian 元数据见 [Runtime 观察](evidence/stage3/runtime-observations.json)，用户流程、文件结果和计数见 [S3 真实流程](evidence/stage3/real-flow.json) 与 [累计请求账本](evidence/stage3/provider-requests.json)。S2 的历史记录及 10 次旧上限快照不改写；S3 结束时实际授权累计上限为 15；S4 追加后为 20。

## S4：本轮收尾验收结果

**S4 本轮验收记录已完成，完整需求尚未通过，D4 FAIL。** 自然自动拒绝后真实人工接管仍未触发，不能将单元级协议测试当作该分支 E2E。严格 Native Clippy 的原失败已在后续授权收尾中修复；历史失败日志仍保留。

付费授权已更新为累计 **25 次**。S4 使用 **10 次**，累计 **23/25**，剩余 **2 次**。所有父请求、guardian 审核及其工具后续请求都进入同一账本；无重置、漏计或超额。

| 检查 | 结果 | 证据及范围 |
|---|---|---|
| 接管关联、重复批准、失败反馈 | PASS（单元级） | Host 保留原 thread/turn/review/action，跨任务拒绝，重复只发一次，原生失败不标记成功；不是自动拒绝真实 E2E。 |
| 审批失败提示修复 | PASS | 同一请求仍 pending 时保留失败提示；解决或切换任务后清除。 |
| UI / Host / Contracts 聚焦回归 | PASS | UI 6 文件 78 项、Host race tests、两端 lint、Contracts 3 项、生成同步及退役检查。 |
| 最终 canonical 构建与正常恢复 | PASS | 首次 TS 空值收窄失败修复后构建成功；Cmd-Q 正常退出并重开；真实已完成任务恢复且续跑成功。 |
| 任务隔离及默认模式 | PASS | S4 auto / S3 ask 独立，重启后原任务 auto、新任务 ask；确认标记恢复。 |
| 主窗口亮暗及最小尺寸 | PASS | 真实 Native 1180×760 主窗口的输入框与权限入口无截断；系统恢复原浅色。 |
| 菜单/确认亮暗视觉 | PASS（生产组件） | 直接导入生产组件和主题的 1180×760 Vite 页；6 张截图覆盖三项文案、选中勾、取消/确认和亮暗弹窗；菜单无溢出。与 Native 主窗口证据共同覆盖 AC-001。 |
| 首次完全访问确认 | PASS（S3 实测 + S4 组件） | S3 真实取消/确认保留；S4 组件交互和视觉复核；未重置真实用户确认标记。 |
| 真实原生自动审核 | PASS | 第 14–17 次：guardian MiniMax-M3/minimax read-only/never 自然 allow，外部文件 S4-auto；审核工具后续请求已计数。 |
| 重启后项目内默认权限写入 | PASS | 第 18 次请求中 s4-inside.txt 写入 S4-inside，退出码 0，无人工审批。 |
| 联网批准与项目外拒绝 | PASS | 原回合解锁后分别点击：联网返回 HTTP/2 200 / exit 0；外部写入 command_declined、rejected.txt 不存在；第 19 次后续回复，回合完成。 |
| 完全访问实际写入 | PASS | 第 20/21 次：danger-full-access / never / user，full.txt 为 S4-full，无新增审批。 |
| 完全访问后切回 ask | PASS | 第 22/23 次：workspace-write / on-request / user / network=false；外部写入重新请求批准；拒绝后 after-full.txt 不存在。 |
| 自动拒绝后真实人工接管 | NOT RUN | 正常安全场景自然 allow；未强求 deny，不制造危险操作或伪造回调。 |
| 核心边界与清理 | PASS | Codex 核心仓干净，Runtime/manifest hash 不变；应用、计数器、视觉服务器均正常关闭，浏览器视口复原，无监听残留。 |

| Must AC | 当前结论 | 对应证据 |
|---|---|---|
| AC-001 | pass | 组件测试 + 真实 Native 主窗口/AX + 生产组件亮暗最小视口截图；原生弹出菜单截图限制如实保留。 |
| AC-002 | pass | S4 默认 ask、项目内写入、真实联网/项目外原生审批。 |
| AC-003 | pending | auto_review 真实 allow；自然拒绝后真实接管仍未验收。 |
| AC-004 | pass | S3 首次取消/确认；S4 组件复核、真实完全访问执行。 |
| AC-005 | pass | S4 两任务模式隔离、正常重启恢复。 |
| AC-006 | pass | Native/Host 忙时边界与聚焦测试；真实运行/待审批禁用，下一轮保存模式生效。 |
| AC-007 | pass | S4 同回合两项不同决策准确关联；Host 幂等/失败测试；真实拒绝目标未生成。 |
| AC-008 | pass | 退役边界、核心/Runtime 校验和、diff 检查及正常清理。 |

详细证据见 [S4 验证说明](evidence/stage4/verification-notes.md)、[真实流程与文件结果](evidence/stage4/real-flow.json)、[原生回合](evidence/stage4/runtime-observations.json)、[累计账本](evidence/stage4/provider-requests.json)、[生产组件视觉来源](evidence/stage4/component-visual-provenance.json)。

## 交付限制

S4 已完成本轮可安全执行的回归和记录，feature/S4 保持 active/default-off，尚未关闭。**只有补齐真实人工接管及其余门禁并通过 D4 后，才能声明完整需求完成。** 不通过重复普通模型调用追求拒绝结果，不用构造回调代替真实自然分支。

严格 Native Clippy 的既有 database.rs type_complexity 已在用户本次明确授权后通过局部类型命名修复，最新退出码 0；原失败日志保留，未抑制 lint 或修改 SQL。未运行含强杀、攻击资源、危险归档、权限破坏或 Runtime 替换的旧全量套件，原因是用户长期安全条款禁止；本结果仅覆盖已列正常 focused 场景。

菜单展开时的 Native 截图受工具限制；补充的是同一生产组件在浏览器的视觉证据，明确不连接 Native/Host/Runtime。首次完全访问真实确认来自 S3，S4 未重置用户标记来伪造首次状态。

MiniMax 未带 phase 的文本仍显示既有“未分类模型消息”；最终验收依据原生配置、工具结果和真实文件，不依赖模型口头声明。未提交、推送或发布，其它任务工作区修改保留。


## S4 后续收尾：Clippy 完成，真实接管待执行

| 检查 | 结果 | 证据 |
|---|---|---|
| 严格 Clippy | PASS | `closeout/native-clippy.log`，exit 0；8 字段 tuple 命名为 StoredStartTurnDispatchRow。 |
| Native 格式与相关回归 | PASS | fmt exit 0；权限/正常重开 2 项、受影响派发查询 1 项通过。 |
| 保留 Runtime 原生规则配置 | PASS（无模型） | config/value/write、config/read、thread/start 接受 auto_review.policy；0 个 turn、0 次付费调用。 |
| 候选规则输入边界 | PASS | 只在 exact local/demo_fast + 固定计数器 + 显式配置文件时传递；default-off、缺省规则不变测试及 Host lint/race 通过。 |
| 默认规则自然拒绝记录 | 无现成记录 | 受管 Runtime 两条 guardian 会话均为 allow；用户也确认无现成拒绝任务。 |
| 临时规则下真实拒绝/接管 | NOT RUN | 只准备了指定普通文件和原生复核规则；待用户确认验收配置与额度，尚未启用或发起模型任务。 |

本轮 Clippy 改动的 contract-impact 为 none（无 SQL、序列化、持久化、权限或跨仓可观察行为变化）；验证用原生规则文件输入属于 local 验证配置扩展，不新增公开 DTO，FEAT-152 整体 semantic 分类不变。Codex 核心与二进制未修改。

人工介入只需确认待执行方案及预算；若实际 UI 锁屏则手动解锁。无需用户制造拒绝、注入回调或改数据库。完整步骤、允许范围、预计 6–8 次请求与证据边界见上方方案。D4 继续不通过，不能将“Clippy 已通过”误读为整个需求完成。
