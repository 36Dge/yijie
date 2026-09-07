# FEAT-152 — 交付记录

## 2026-09-06

已加载本轮全部用户确认、各受影响仓 AGENTS、项目记忆、Handbook 和 Compact 模板。当前处于 D0 产品/UX 定稿与 Contract First 调查。用户批准的规则已完整记录在 Brief 和 feature.yaml。未启动真实服务、未调用模型、未提交代码。

## S1 / 追加约束后的收敛

用户要求分阶段、禁止 Codex 核心改动、最小跨仓集成提前。已加入默认关闭的独立开关，暂停扩写 S2/S3。此前候选代码保留为未验收草稿，未发布。

从保留的 FEAT-136 binary 正常生成 267 份 schema 到系统临时目录，binary SHA-256 仍为 4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d。实际 stable API 包含 approvalsReviewer 与 thread/approveGuardianDeniedAction，不包含当前源码里可见的 thread/settings/update；因此以真实 artifact 能力为准。

第一次真实 Host→Runtime 联调：ask 配置成功，但无回合 thread/resume 返回 no rollout found。保留 FAIL 原始日志，不伪造恢复通过。第二次检查只验证无模型可证明的三档 thread/start 配置；恢复明确留到有真实回合的阶段 S4。进程通过原生 EOF 正常退出；无强杀、无模型请求或工具执行。

## S1 结果

真实三档配置与 Contracts 3 项检查通过；Host lint/race callback tests 通过；Native 存储/IPC 2 项、默认关闭 UI 67 项通过；Desktop lint/build、生成同步和旧审批退役检查通过。

严格 Clippy 未通过：database.rs 已有 type_complexity，git show HEAD 同一 tuple 声明可复核。未扩大范围修复或屏蔽该 lint。首次 UI 命令遗漏排除 .local，加载其它任务副本并失败；纠正为仓库标准排除范围后，当前 src 的 67 项全部通过。原始结果不篡改。

已独立审查 S1 范围：核心仓零修改，保留 binary/manifest hash 未变；新功能三个边界均默认关闭；新协议不改旧 v1-v6；新存储仅可逆扩展，无清理历史。

S2/S3 候选仍未验收：需继续核对真实命令/文件/权限请求、待审批与新回合的服务端关联、自动拒绝后的用户批准、实际模型和重启恢复、菜单视觉/键盘。不得依 S1 结果打开默认入口。当前停在阶段反馈点。

## 2026-09-07 — 恢复 S2

沿用本对话中用户明确的 10 次付费模型调用授权；暂停期间未调用模型。现在执行已批准的 S2 方案：审查审批绑定、重复提交与忙时切换，尽早真实批准/拒绝，完成一个真实回合后正常关闭/重开验证。S3/S4 不展开；核心源码及保留 Runtime 二进制只读。

暂停后 Desktop HEAD 为 c3a6195c540982e6304d02a2918f70eb0f49eb1a，其它任务的图标、包脚本和设计文档改动均保留。

## S2 / 真实链路优先验证与修复

付费验证使用固定 MiniMax Responses 地址的透明本地计数器：每次转发前持久记账，合计硬上限 10，不记录凭据、请求正文或模型响应。显式 local/demo_fast 开关下传递 provider base URL 与零自动重试；非验证入口不改变供应商配置。原生审批和模型输出均来自真实 retained Runtime，没有 fixture producer。

启动首先被旧检查器的 dirty Host/Contracts 要求阻断；新增仅完整本地权限开关和固定计数地址下生效的候选检查。旧 immutable commit/origin/digest、Runtime binary/manifest 与 FEAT-137 退役检查全部保留，额外验证新 OpenAPI bundle、Host 生成类型与 Desktop 类型一致。Skills 主工作区已前进，canonical launcher 现在尊重既有 Skills 路径参数，使用已存在的干净 `skills-pinned-10c45be` worktree；没有修改 Skills pin 或清理主工作区。

首次真实命令审批出现后，确认目标文件尚不存在，但旧输出日志脱敏器隐藏了整条普通命令和路径。通过 UI 拒绝该请求；未在不可审阅状态下批准。修复审批专用展示，保留普通操作、路径和 URL，沿用凭据保护及长度限制。命令的 scope 标为工作目录，实际目标保留在命令和理由中。

完成真实回合后正常退出并重新启动，首次继续原任务立即失败且没有新模型调用：原有本地绑定流程没有调用 Runtime thread/resume。新权限开关下复用现有恢复入口，在 coordinator 派发前恢复既有对话；不打开旧 v6 审批权威。再次正常启动后，同一任务成功产生审批并执行命令。

同步修复新建排队任务尚未绑定 Host 时的误报：先在 Native DB 校验任务所有者；未绑定时返回空审批快照。真正的读取/提交失败仍禁用发送并允许重读。菜单补齐选中项焦点、方向键、Enter 与 Esc；过期任务响应不覆盖当前状态，保存结果不确定时先回读，批准决策重复点击只提交一次。

## S2 结果 / 阶段结束

- 真实批准：任务 `01a077a8-5b96-7af2-a9ce-9f45761a0b23`，批准前文件不存在；点击批准本次后命令退出码 0，`approved.txt` 内容恰为 `S2-approved`。
- 最终版本真实拒绝：任务 `01a077b3-b979-7db2-bb57-e53f4c851384`，Runtime 返回 `command_declined`，任务正常结束且 `rejected.txt` 始终不存在。
- 同一已完成任务正常重启续跑通过。临时将原任务设置为 auto，仅验证配置保存；新任务仍 ask，正常重启后原任务仍 auto；结束时恢复 ask。未执行 auto/full 模型任务。
- Go callback/admission race tests、Host lint、Native 2 项、Desktop 75 项及 lint、Contracts 3 项、canonical build 均通过。原有 strict Clippy type_complexity 失败仍保留，未扩大范围修复。
- 模型请求共 6/10，剩余 4 次；真实 task/工具回合和后续模型回复均已计入。应用正常退出，Host 18081 与计数器 18083 均关闭。计数器通过正常 Ctrl-C 结束。
- 核心仓零修改，保留 binary/manifest SHA-256 与 S1 一致；没有提交/推送，没有强杀、权限破坏、可执行文件替换或攻击注入。

证据见 `evidence/stage2/real-flow.json`、`provider-requests.json`、`source-identities.json` 与聚焦验证日志。S2 已完成，停在阶段反馈点。S3 原生自动审核/完全访问及 S4 完整恢复、亮暗/最小窗口视觉矩阵与 D4 均未执行。供应商回复未带 phase 时仍按既有协议显示“未分类模型消息”，本需求不猜测最终阶段。

治理校验首次提示付费授权时间必须包含 ISO-8601 时刻；通过当前对话原始 turn 元数据回查用户“付费调用授权调为 10”的时间为 2026-09-06T15:23:31.000Z，已准确补齐，未推测授权时间或再次请求授权。

## 2026-09-07 — S3 启动

用户在 2026-09-07T01:24:38.000Z 明确追加 5 次授权：累计 15，保留 S2 已用 6、剩余 9。按原生自动审核兼容性核对、真实自动审核、完全访问及权限收敛顺序推进；S3 单独反馈，S4 不执行。contract-impact 维持本需求的 semantic 分类，不扩大仓库职责或 Runtime 核心范围。

## S3 / 按用户确认顺序完成

无付费核对确认：原生 guardian 优先查找 codex-auto-review，当前固定 catalog 无该模型且无 override，因此回退到 MiniMax-M3；审核配置克隆父供应商、base URL 和认证。审核自身会把 request/stream 重试设为 1，计数器必须覆盖这些请求，不能按主任务的零重试推算成本。计数器硬上限按新增授权扩到 15，保留全部旧账，只新增受限模型名与结构化输出标记；没有记录提示词或回复正文。

真实自动审核通过：Desktop 任务 `01a0797c-6d49-7872-9615-1d929bcc8ddb` 的 Runtime 父线程为 `01a0797c-6d7a-7623-8951-b4564547f0a2`。原生创建来源为 guardian 的子会话 `01a0797c-a58d-7471-8c06-f61cdd013bdd`，模型 MiniMax-M3、供应商 minimax、read-only/never；实际返回 `{"outcome":"allow"}`，随后写入 `auto.txt`，内容为 `S3-auto`。没有人工点击批准。主请求、审核子请求、工具后回复分别为计数器 7、8、9，均到固定 MiniMax Responses 地址。

完全访问通过：首次选择显示确认弹窗；取消后保持 auto，再选仍要求确认；确认后保存 full。第二轮真实 Runtime 配置为 danger-full-access/never/user，普通文件 `full.txt` 内容为 `S3-full`，未出现人工或自动审核；请求计数 10、11。后续再次选择 full 不重复首次确认。

同任务权限收敛通过：切回 ask 后，第三轮真实配置恢复 workspace-write/on-request/user，network_access=false；项目外 `after-full.txt` 写入重新显示人工审批。决定前文件不存在，经 UI 拒绝后 Runtime command_declined，任务完成且文件仍不存在；计数 12、13。结束时任务恢复 ask。

S3 本轮新增 7 次，累计 13/15，剩余 2 次。应用正常退出，Host 和 Runtime 正常清理；计数器通过 Ctrl-C 正常关闭，18081/18083 无监听。Codex 核心仓无变更，Runtime binary/manifest hash 保持原值；未提交、推送或发布。

补充的 2 项确认交互测试覆盖取消不保存、确认才保存、忙时不接受未完成确认；本轮界面聚焦测试共 77 项通过，Desktop lint、Host race tests/lint、Contracts 3 项通过。S3 未改产品公开 DTO、审批引擎或 Runtime，只完成候选行为的真实验证与已授权计数扩展。

阶段结论：用户最新指定的 S3 三项顺序验证完成，停在 S3 反馈点。自然自动拒绝后转人工的真实分支没有发生；只核对了原生 inject_no_new_turn 语义，并保留已有事件投影/拒绝单元测试。未伪造拒绝回调或制造危险操作，该分支与 AC-003 全分支不声明通过。S4、完整 Must AC 和 D4 尚未完成；既有 Clippy type_complexity 与未分类模型消息限制继续保留。

## S4 启动

用户于 2026-09-07T04:34:39.000Z 明确进入 S4 并追加 5 次调用，累计上限 20，保留已用 13，剩余 7。先完成零付费检查，再真实安全场景与整体回归；不能自然触发的自动拒绝/人工接管保留 NOT RUN，不伪造回调、不制造危险操作、不声明 D4 通过。


## S4 / 零付费修复与真实回归进度

人工接管新增进程内协议测试：原请求关联、跨任务拒绝、重复批准只发送一次原生接口、原生失败不标记成功。只属于单元级协议验证，不是伪造真实 Runtime 拒绝事件。发现并修复审批失败提示被后续成功轮询立即清除的问题；pending 请求继续显示可重试反馈。完全访问警示文字改为现有主题警示文字 token，未改全局设计系统。首次 TS 收窄构建失败修复后，canonical 构建、UI 78 项、Host focused race/lint、Desktop lint 与 Contracts 3 项通过。

实际完成浅/深色主窗口与最小 1180×760 检查，恢复系统浅色。菜单 AX 三项及键盘操作通过，但菜单打开时工具无法取得截图，完整菜单视觉矩阵保留未验收。首次 full 取消/确认沿用 S3 实测和 S4 组件测试，不篡改真实首确认标记。

真实 S4 auto 任务自然返回 allow，项目外 auto.txt 内容 S4-auto。原生 guardian 执行一次工具并发送后续审核请求，故请求 14–17 共 4 次；全部入同一 ledger。真实自动拒绝接管未触发，不制造危险场景追求 deny。

正常 Cmd-Q 退出后以 canonical 入口重新构建启动，S4 auto / S3 ask 独立保存，新任务默认 ask，原任务历史与模式恢复。同任务 full → ask 后发起第 18 次请求，一次产生三项独立工具：项目内写入成功、公开网页 HEAD 联网审批、项目外普通写入审批。读取待审批界面时 Mac 锁定且工具无法自动解锁，已请用户手动解锁，尚未执行两个 UI 决策。账本当前 18/20，剩余 2；保留应用和计数器等待继续。

S4 尚未结束，AC-001/002/003 pending，D4 不通过。核心仓干净，Runtime 与 manifest 校验值不变；无强杀、权限破坏、可执行文件替换、攻击注入、提交或推送。其余任务工作区修改原样保留。


## S4 / 解锁后恢复与第二次追加授权

用户解锁后，在原待审批回合拒绝项目外写入、批准公开网页 HEAD 请求。Runtime 返回 command_declined 与 HTTP/2 200，项目外文件未生成，回合完成，累计 19 次。用户于 2026-09-07T05:33:10.840Z 再追加 5 次，累计上限 25，剩余 6。正常 Ctrl-C 停止空闲计数器后扩充原账本上限并重启，不重置既有 19 条记录；继续补 S4 完全访问执行及切回 ask 后的实际收敛。


## S4 / 本轮最终结果

新增授权后完成请求 20/21 的真实 full 外部写入（S4-full，danger-full-access/never/user），再完成 22/23 的同任务 ask 收敛：workspace-write/on-request/user/network=false，原生重新请求批准，UI 拒绝后 after-full.txt 未生成。原回合联网批准与外部拒绝也已完成；S4 四轮真实流程均正常结束。

原生菜单截图工具限制使用分层视觉补证：在 .local 临时 Vite 页直接导入生产权限组件和主题，仅本页属性交互，不连接审批后端。1180×760 下浅暗菜单/确认弹窗、三档选中勾与取消/确认均检查通过，截图/几何/源码校验保留。此证据不是全应用截图或真实 Runtime 接管。未修改生产组件实现来取得截图。

最终累计 23/25，剩余 2，S4 共 10 次；没有为消耗预算重复尝试自然拒绝。应用正常 Cmd-Q（launcher exit 0），计数器 Ctrl-C（exit 0），临时 Vite Ctrl-C（exit 130），18081/18083/5177 无监听。浏览器视口复原、临时 tab 关闭，系统早已恢复原浅色。核心仓和 Runtime hash 保持不变。

结论：S4 本轮收尾记录完成但未通过，AC-003 真实自动拒绝转人工保持 pending，其它 AC 有所列证据。原有 strict Clippy type_complexity FAIL 保留。D0 结构检查不代替 D4，严格 D4 不通过；完整需求、S4 均不标记 complete，不提交/推送/发布。


## S4 / 用户要求继续关闭两项问题

用户明确要求执行 Clippy 修复和真实人工接管验收，并在需要人工介入时说明方式。Clippy 通过命名局部查询 tuple 修复，SQL/字段顺序/解码保持不变；随后只整理本需求既有 Rust 片段的 rustfmt 格式。严格 Clippy、fmt、权限 2 项及派发查询 1 项全部实际通过，原 S1 失败日志原样保留，不抑制 lint。

只读核对原生策略明确 low/medium 普通操作默认 allow；当前受管 Runtime 两条 guardian 会话均 allow。用户确认没有现成拒绝任务，并明确授权模型构思正常操作和范围。进一步找到官方 auto_review.policy 配置路径，固定 retained Runtime 的无付费配置读写与 thread/start 实测通过，未发起 turn/start。

准备的场景只涉及新的普通文件 manual-review/pending/reviewed.txt，原生默认 policy.md 原文完整保留并追加精确文件的人工文档复核要求。Host 验证输入仅在现有 exact local/demo_fast + 固定计数器下，显式读取有界普通 UTF-8 配置文件并转发原生字段；默认无变化，不实现风险引擎、不产生或伪造审批事件。边界 race tests 与 lint 通过。

该场景验证“指定原生规则下的真实拒绝/接管”，不冒充“默认规则自然风险拒绝”。已向用户请求确认这一验收配置及追加 6 次预算：现余 2，初次和接管续跑预计各 3 次，审核查验工具可能再增加 2 次，总计 6–8。审批尚待回复，当前账本仍 23/25，本轮新付费调用 0，不提前修改额度或 AC-003 状态。核心仓与 retained Runtime 保持只读。


## 最终执行授权

用户于 2026-09-07T06:39:38.090Z 明确采用原生临时复核规则方案并追加 10 次，累计上限 35，保留已用 23、剩余 12；强调最终目标完成 FEAT-152，不偏离范围。现在执行真实接管及最终验收，不把先前建议的 31 次误记为实际授权。


## 最终真实执行首次问题与修复

请求 24–27 实际返回 allow，目标文件写入。只读核对发现 Native sidecar 使用 env_clear 与环境白名单，未转发新增策略文件路径，guardian base_instructions 中没有复核规则；不是原生规则拒绝或接管通过。首次结果、原文件字节/hash 与原始应用日志保留到 evidence/stage4/final/first-attempt.json。普通测试文件正常重命名为 reviewed-first-allow.txt 保存，未删除或篡改历史。

修复 Native 白名单：只在既有本地权限开关与精确计数器下转发规则文件。新增纯环境映射回归，Native 3 项、fmt 和严格 Clippy 通过；应用正常退出后重新 canonical 构建。再次付费前检查实际 Host 已收到策略文件与计数器变量，继续仅在剩余 8/35 预算内补真实接管。


## S4 / 真实接管与最终零付费收尾

修复 Native 环境白名单并正常 canonical 重建后，实际 Host 已收到精确策略文件和固定计数器。请求 28–30 由真实 guardian 返回 deny（risk low、authorization high），普通目标文件未创建，UI 出现真实人工复核卡片。点击批准后，父 rollout 增加 1 条原生 exact-action 批准上下文；此时计数仍30、文件仍不存在，符合 inject_no_new_turn 语义。

请求 31–33 在同一任务保持 auto，执行同一准确命令；真实 guardian 返回 allow，明确以原生人工批准为依据，文件准确为 S4-manual-approved。请求 34–35 同任务 full 写入单独普通文件 S4-full-final。随后切回 ask，正常 Cmd-Q，撤除临时策略环境变量后 canonical 重建重启；新任务 ask、原任务 ask 和三轮完成记录恢复。Host 环境不含规则，Runtime config.toml 无策略残留。原安全策略与 Codex 核心/Runtime 均未改。

Native 3 项、严格 Clippy/fmt、UI 78 项、两端 lint/canonical 构建与五仓 diff 检查通过。应用正常 Cmd-Q、计数器正常 Ctrl-C 均 exit 0，18081/18083 无监听。累计 35/35，剩余 0，全部请求完成 HTTP 200；原失败 24–27 和原文件正常重命名后的字节证据保留。

原有真实接管缺口与 Clippy 问题均关闭，implementation 标 complete，AC-003 单项标 pass。严格核对 D4 时发现最终白名单修复后的构建尚未实际重跑 ask 项目内/联网/外部拒绝和 full→ask 收敛；旧 S4 18–23 的实测结果不冒称最终构建 fresh run。因此 feature/S4 保持 active，verification FAIL，real_smoke NOT RUN。剩余任务只补最终构建 ask 实际回归并重跑 D4；预计2次、建议最多4次调用的具体清单已落盘，但未获追加授权、不修改35上限。没有新功能范围。


## 最终请求批准回归追加授权

用户于2026-09-07T07:19:55.228Z明确再追加10次，累计上限45，保留已用35条、剩余10。计数器已正常停止后扩充同一账本与硬上限；仅继续已列最终ask回归和D4，不增加产品范围。


## S4 / 最终请求批准与恢复通过

追加授权后只用第36–37次，最终同一任务第4轮ask实际完成：项目内普通文件无需审批准确写入；公网HEAD通过独立卡片批准返回HTTP/2 200；项目外写入通过另一卡片拒绝，文件不存在。Runtime为workspace-write/on-request/user/network=false，确认此前full权限已收敛。待审批禁用菜单，完成后恢复。没有使用之前reviewed.txt的批准越权执行新文件。

随后正常Cmd-Q/canonical重启，新任务ask、原任务ask与4轮完成历史、另一任务auto各自保留。实际菜单3项文案/描述/选中核对，视觉生产源码hash一致。最终产品源码在修复后的接管、full和ask之间未改变。应用与计数器正常退出、无18081/18083监听，核心及Runtime/manifest校验值保持。

最终累计37/45，剩余8；S2=6、S3=7、S4=24。原生人工接管、三档真实执行与权限收敛、正常恢复、UI/Native/Host/Contract聚焦检查均已通过，全部Must证据见final/acceptance-matrix.md。implementation complete、feature usable、S4 complete；严格D0/D4结果在最终日志独立记录。仅local demo_fast，不提交/推送/发布，不以剩余预算增加范围或调用。


严格D0与D4实际exit0，元仓pnpm lint通过、pnpm test共50项通过、Shell语法通过。最终结论：FEAT-152 local demo_fast已完成，S1–S4关闭；37/45、剩余8，无待执行付费步骤或人工介入。完整结果见evidence/stage4/final/completion.json。


## 2026-09-08 / 四仓交付固化准备

用户要求先整理变更、获得提交授权后按Contracts→Host→Desktop→治理记录提交与固定依赖，随后完成日常入口和打包。现已准备逐文件manifest及三个实现仓的可应用patch；未改真实索引或提交。Desktop package.json/ChatComposer按片段选择，43个其它工作保留。UI80 PASS/1按安全规则跳过，lint、Contracts3同源conformance和无计数器入口预检PASS。本轮0次付费调用，下一步仅等待具体本地提交授权，完整清单见03-delivery-commit-plan.md。S4历史D4通过结论保留；尚不声明后续固定提交/打包已完成。


## 2026-09-08 / 已授权四仓提交与普通App交付

用户明确授权按清单执行本地Git提交。Contracts=0bdef80491db8263bad4d54cfe1d1950785a6b64，Host=af8d370277569cb5a9b6a229f10386690aaebb0f，Desktop最终=af69d6e740351b6006a1b8aaa716d3c2e04df235（3个Desktop提交均先于元仓记录）。Host/Contracts工作区干净；Desktop其它工作保留，mixed package/ChatComposer未混入图标命令或配色。固定真实Git对象和Host构建输入的验证通过。

普通App新增canonical --packaged入口，保留com.yijie.ai及日常历史；首次case形状被旧stable隔离校验拒绝，改为预解析普通参数并保留原stable分支后通过，失败log保留。已有固定Skills目录自动选择通过。打包、正常退出/重启、三档菜单、原草稿auto与既有任务ask各自恢复通过，Runtime ready；未改变权限或发模型任务。应用已留用户使用。本轮0次调用，37/45、剩余8。

详情见04-local-delivery.md、delivery-results.json。元仓最终提交固定本报告与证据，自身SHA在提交后本机回执记录，不制造自指SHA。未push/tag/发布，核心及retained Runtime不变。
