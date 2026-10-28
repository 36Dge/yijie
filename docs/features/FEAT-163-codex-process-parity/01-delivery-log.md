> 最新状态：2026-10-24按用户要求再次复审，整体完成结论已撤回；以[07实现复审](07-implementation-reaudit.md)和04续办为准，以下前轮完成措辞仅为历史。

# FEAT-163 可执行步骤与实际执行记录

> 最新状态：本地实施与适用验收已完成，原步骤清单保留用于追溯；以本页末尾实际记录、02与04为准。

当前只有文档。所有下面的产品动作均为计划，必须先核对[04续办入口](04-resume.md)中的实际授权。步骤是技术依赖顺序，不建立新的治理切片或第二套执行状态机。

## 1. 步骤总表

| 步骤 | 输入与动作 | 输出/结束条件 | 当前状态 |
|---|---|---|---|
| S0 来源与范围核对 | 读取本包、最新用户决定、各仓规则与当前diff；核实源码/运行包/有效配置；登记现有入口 | 新的只读baseline、入口矩阵、授权和预算准确；不覆盖他人改动 | NOT STARTED |
| S1 分层定位 | 复用已有observer完善有界结构诊断；经授权在正常App入口观察一次有区分力的真实回合 | U01/U02/U03各给证据结论或明确缺证；不把仪表截断当产品失败 | NOT STARTED |
| S2 确定最小改动 | 按消息分支选定修复；按05补齐已证实的原生活动投影缺口，冻结版本/reader兼容；核对Runtime补丁授权 | 具体修改清单可审查；活动字段不被误当需要新Runtime；不预批准消息恢复补丁 | NOT STARTED |
| S3 原生生成与传递修复 | 修改现有指令组合及已证实的消息缺口；沿Contracts→Host→Native补活动字段安全投影与reader；维持同一Turn工具闭环 | 指令、call/output、公开消息和活动字段普通验证通过；新旧格式明确 | NOT STARTED |
| S4 现有Timeline体验调整 | 复用现有分组/展开，实现公开正文+淡色分段摘要+本段操作明细+单项详情，诊断另置 | 正式组件普通场景通过，未修改原生事实或phase；TG用例覆盖 | NOT STARTED |
| S5 联合验证 | 适用来源/契约/专项检查→canonical构建→正常入口真实Kimi验收→正常重开 | 02全部Must在同一来源最终版本证据下PASS；失败留存 | NOT STARTED |
| S6 交付核对 | 分离实施自审、差异/来源核对、预算结算、限制清单、更新续办页 | 产品结论与证据一致；Git/发布只在单独授权范围内 | NOT STARTED |

S3与S4在边界明确后可并行；S4完成不能绕过S1/S3/S5宣称机制完成。检查通过后除非有新改动、新失败或未决风险，不机械重复扩大全套验证。

## 2. S0 — 来源、入口及已有改动

1. 从`yijie/repos.yaml`确认五仓，读取各自AGENTS和相关设计文档。
2. 比较当前branch/HEAD/remote/status与规划baseline，按文件记录现有变更来源；规划baseline不是可reset目标。
3. 核对实际canonical build receipt、Runtime manifest、模型/Provider、permission/summary配置、tool surface和有效base/developer instructions摘要。源码存在不代表当前App已加载。
4. 入口逐项列出：普通新建、原会话续聊、有/无项目、模型切换、附件/看图、已有图像/Artifact生成、专家进入/退出、技能上下文、连接器工具、结构化结果slot及计划任务共用聊天路径。填写实际共用的start/resume/compose入口，必要时增加普通验证，不能默认为相同；不扩建原本未支持的功能。
5. 核对FEAT-162及其他并行任务当前变化，只保护与协调共享文件；不代其实施。新增检索工具只有其正式接口、来源、授权和验收就绪后才能作为本任务候选依赖。

## 3. S1 — 复用现有诊断，不建生产代理

修改候选：Host `scripts/responses_stream_observer.py`、`scripts/chat-model-smoke-meter.py`及现有普通observer测试。

已有request_input_summary/ConversationStreamSummary可直接复用。补足：

- response/item/call身份哈希关联；按Item累计added/delta/done次数而非只覆盖快照。
- 有界事件序号、相对时间、类型、phase、状态；公开文本字节数及hash。
- response终止类型、incomplete原因闭集、usage、实际token上限、诊断truncated标志。
- function参数、规范化后output及下一request input的hash；数组output的规范化结构摘要。
- 有效instruction、model/provider和工具定义摘要；不记录凭据/原始推理/命令正文/整个response。

现meter会改写max_output_tokens；需在现有脚本提供观察请求不变的方式，保留批准的总请求上限。若预算要求限token，该批只算受限诊断，真实配置验收另记；不得静默放宽上限。诊断容量满/truncated时相关结论为缺证，不能记全链路PASS。已有消息、命令和URL的安全处理边界保持。

模型/网络/工具时延与UI时延分别记录，可直接观察的起点是“本地边界收到Provider SSE事件”→Runtime解析→app-server通知→Host投影→Native保存/发布→DOM可见。本地observer不能测Provider内部何时生成/收到内容。各进程记录同一主机时钟的时间锚点及单调时钟耗时，以response/item身份关联；不直接相减不同进程的相对计时，注明分辨率与采样误差。不得把“最终hash相同”当实时显示证明；不得把本地180ms目标写成端到端性能事实。

生产UI仍只消费现有原生协议，不能读取rollout文件；rollout仅作为本机诊断材料。后续真实调用仍从正常产品入口发起，不另写绕过产品的模型循环。

## 4. S2 — 消息缺失与延迟决策表

| 分支 | 必须先取得的证据 | 允许的最小方向 | 失败后的下一步 |
|---|---|---|---|
| M1 Provider无公开message | added/done/completed各阶段都无公开message，未因预算或token上限终止 | 修有效沟通要求/原生工具使用方式，验证同一原生循环 | 无变化不重跑；检查Provider原生能力/配置，提出有证据的兼容选择；AC-002仍未过 |
| M2 Provider有、Runtime无 | 同response/item合法message存在，parser/map缺失 | 修现有Responses parser或event_mapping的已证实差异 | 若未知phase/字段不明，保持未知并补最小结构证据，不默认改commentary |
| M3 仅终态output有message | 真实完整message、原生身份和内容一致、逐项done确实缺失 | 评估原生终态协调最小patch；沿既有身份核验思路 | 未有此证据不得进入patch实现 |
| M4 消息存在但晚到 | 各层时间显示真实延迟位置，包含0005缓冲判定 | 只修对应缓冲/转发/呈现位置，保持原序 | 不靠前端倒排或完成后回填伪装实时 |
| M5 Runtime完整、Host不完整 | 原生Item与Host投影不对应 | 修`internal/session/native_conversation.go`等现有投影 | 不修改模型调用次数或另建消息源 |
| M6 Host完整、Desktop不完整 | SSE/history与Native/store/DOM逐层不对应 | 修既有buffer/storage/subscription/view或组件 | 不复制reducer、不做正文前缀对账、不逐项拼冷快照 |

M3特别约束：0005是空function参数补丁，不是通用恢复器。只能在真实终态证明的同Item上完成缺失步骤；已有done不二次完成；已执行工具不二次dispatch；不全量回放completed.output；冲突或缺失不能猜补。正常流式路径不应被额外缓冲。source-first、补丁可重放和实际授权均先于实施。

无正文终态：普通问答未交付记为场景失败/准确用户提示；不全局改Runtime completed为failed。合法UserShellCommandTask、CompactTask或明确Artifact交付保留原生语义。

## 5. S2 — 重复无效执行决策表

逐次记录的最小关联：`response/item/call身份 → 工具名/参数摘要 → 实际output摘要 → Runtime规范化后history → 下一request同call_id结果`。

| 证据 | 方向 |
|---|---|
| 相同原生call被重复dispatch | 修既有身份/重放处理；不是按参数内容去重 |
| 新call_id参数相同，但前次结果缺失/错配/被异常截断 | 修现有history、for_prompt、输出序列化或真实断点；normalization补aborted不是有效结果已返回 |
| 前次结果确已进入Provider，模型仍新建相同无收益读取 | 核查有效工具/沟通规则及真实output可理解性；记录模型决策重复；不能改UI假装只发生一次 |
| HTTP403/空内容/首页头部，但shell exit0 | 使实际取数策略明确检查返回内容；必要命令保留HTTP/失败信息，不以exit0宣称核验成功 |
| 相同参数有合理新信息（真实轮询、用户新指令、数据变化、修复后验证） | 不当作无效重复，不新增泛化参数拦截器 |

本次已证实的23次curl均为原生真实命令，不是前端计数制造、也未证明为Host桥接。不能使用“内部命令”标签将它们无痕隐藏。

暂无现成通用重复guard：不借用Guardian审批熔断，不新增Host调度循环。现有指令中的禁止无效重复已生效却未奏效，因此不能仅重复这句话就宣布修复；必须先证明真实call/output闭环，再以正常任务验证收敛。收敛仍失败则保持FAIL/未达标，沿原生停止正常结束，依据新增证据选择下一修复。不能自动换模型、自动新建Turn、静默缓存结果或以假输出跳过调用。

## 6. S3 — 按仓具体实现落点

### Host：有效指令和安全投影

- `internal/codex/runtime_permissions.go`：沿permissionInstructions组合恢复通用preamble/progress原则；普通助手文字承载进度，不用工具stdout。保留权限语义、普通问答交付方式与无效操作约束。
- `internal/codex/session_protocol.go`：核对start/resume实际base/developer组合一致，不重复/遗漏沟通要求。
- `internal/codex/expert_instructions.go`、`chat_models.go`：确保专家和模型切换不回退旧基础；不要盲目删除base覆盖，因为目录默认也已简化。
- `internal/session/native_conversation.go`、`native_process.go`及已有MCP安全投影：按05消费已存在的commandActions、fileChange、appContext；新闭合投影版本先Contracts源和reader兼容，旧wire保持。公开消息仅修证实断点；命令预览/路径/diff沿既有安全边界，不能直接暴露raw command。
- 工具和图片/Artifact/结构化输出的已有约束不能因进度改动被移除；对严格schema结果模式，公开消息是否能分离须先验证既有模式，不能向结构化final塞前言破坏结果校验。

### Runtime：条件性最小修复

- 候选锚点为`codex-api/src/sse/responses.rs`、`core/src/event_mapping.rs`、`core/src/session/turn.rs`、`context_manager/history.rs`等；只有对应断点证据成立才修改。
- 不直接编辑固定`codex-rs/`作为产品交付；走`.yijie/patches/`有序最小补丁与canonical构建脚本。
- 不预定全量升级。若固定版本存在已确认缺陷，比较定点回移与升级的真实影响后确定范围；不得把“版本旧”当根因。
- 配置可以完成的改动不下沉内核；不为业务城市对比写Runtime特殊逻辑。
- 05所需的CommandActions/FileChange/AppContext已经存在于固定canonical schema，纯活动显示补齐不需要新Runtime patch；优先消费原生事实。

### Contracts：先判定再生成

- 先核对`openapi/native-conversation-v4/native-conversation-v4.yaml`、现有SSE v11和Runtime兼容投影。
- 05已证明现有v4不足以显示文件动作/变更/App上下文；沿现有协议家族做版本化安全投影，按breaking/replay保守审查。保持旧端点closed shape，新reader支持旧持久格式，兼容就绪再激活新输出。
- UI局部阅读/既有普通指令且wire无变化可以none；事件顺序、终态或字段解释变动至少semantic；任一受支持consumer不兼容升breaking。
- 不新增systemProgress/phase/source枚举来装UI状态。`source=runtime_notification/projection_notice`不是模型/系统发言来源，不能借字段改语义。
- 若需新输出版本，先有兼容reader，再激活producer；按现有generate/sync/pin链，不手工复制DTO或伪改digest。

## 7. S4 — Desktop复用范围

| 文件 | 修改内容 | 必须保留 |
|---|---|---|
| `src/domain/conversation-process.ts` | 复用processActivityGroups邻接段，将计数文案换为真实动作摘要；reasoning诊断另置 | 首Item组键、Item身份/原序、只读phase兼容、末条保护；不跨公开消息合组 |
| `src/components/chat/ChatTurnGroup.vue` | 真正正文与淡色段摘要交错；复用activityChoices/membership逐段展开本段明细；无答终态提示 | 整轮/分段/单项展开相互配合，stable key、用户选择、审批、结果slot |
| `ChatWebSearchItem.vue` | 图标+动作+安全简短query/page；完整来源详情 | search/openPage/findInPage真实区别；来源不是已核验引用 |
| `ChatCommandItem.vue`、`ChatNativeToolItem.vue`、`ChatToolItem.vue`及必要文件变更展示组件 | 消费05安全结构化动作/App/文件变更，展示轻量明细和单项详情 | exit/output/approval事实；命令子动作不冒充独立调用；不regex重建动作 |
| `ChatTimelineItemShell.vue`、等待组件 | 普通成功轻量化；最多一个实际等待位 | 待审批、失败和不可用的可行动入口 |
| `conversation-timeline.ts` | 技术诊断阅读等级调整 | 原始phase/status/availability；Turn结束不封口Item |
| `ChatPage.vue`、`useChatScroll.ts` | 仅在实测必要时修折叠高度变化的锚点 | 底部跟随、上翻/选区/定位保护；不建另一滚动器 |
| `ChatSafeContent.vue`、`useChatStreamPresentation.ts` | 默认直接复用，仅修证实的缺陷 | 单一显示游标、完整字素、终态追平、历史不重播 |
| `src-tauri/src/chat/native_conversation.rs`、storage、store及生成类型 | 在既有路径承接05的新投影/持久格式与旧reader兼容；消息缺失仅修M6证实断点 | 单一buffer、事务、cursor/revision、订阅隔离；默认不新表、不保存分组结果、不回填旧unknown |

同步更新现有`docs/design/docs/design/05-patterns/02-chat-workspace.md`及`docs/chat-stream-presentation.md`，替换旧主线计数规则，不篡改历史测试结果。

当前Native publish路由固定main窗口，本次只覆盖已有多会话/订阅隔离，不宣称已支持任意多个Chat窗口。

## 8. S5/S6 — 验证、激活、回退

具体场景和命令入口见[02](02-verification.md)。测试只使用普通非破坏性样例、正常取消/EOF/退出；不注入攻击、不强杀、不改权限造故障。不得把完整测试命令名字当安全证明。

如果只有UI/指令变更：维持原wire/storage，按现有canonical构建/启动/正常重开验证；回退产品源码也不改历史数据。

消费05的已有Runtime字段：固定canonical schema→Contracts新安全投影→Host/Desktop兼容reader→reader就绪后激活新版本输出，不强制先改Runtime。只有证实Runtime本身需修，才走固定上游→可重放补丁→独立候选→canonical schema比较→Contracts及下游消费。源码依赖顺序不等于新输出可立即启用。保留原产物来源，不覆盖签名/发布/未知来源二进制。

05字段进入已有native_facts/native_views会涉及新序列化格式和reader版本，须纳入兼容与回滚；不默认增加表或改变DB schema。任何进一步存储变化先核实必要性与实际授权，不能删数据回滚。本轮仍只有方案授权。

## 9. 实际执行记录（只能追加事实）

| 日期 | 动作 | 结果 | 产品影响 |
|---|---|---|---|
| 2026-10-24 | 三路只读复审、创建本需求包、保存用户截图原样副本、登记baseline | 目标/复用/分支/验收/续办规则落盘 | 无产品代码、构建、启动、付费调用或Git提交 |
| 2026-10-24 | 新Codex工具分段截图补充、核查原生字段和下游缺口，新增05并同步主方案/验收/续办 | 明确主线分段摘要、本段明细、原生安全投影版本及TG验收 | 仍只改文档和参考图；截图删除请求没有执行 |

## 10. 后续每次结束前更新

在04填写：本轮实际动作/证据、选中分支、未决点、当前具体下一步、授权/额度/在途、共享文件变更。测试结果追加02，不把上轮失败覆盖成PASS；feature.yaml状态仅按真实门禁更新。若目标有新用户决定，先在00/03保留变更依据，再执行，不靠聊天记忆覆盖规则。

| 2026-10-24 | 用户授权按更新FEAT-163实施；完成当前源码/FEAT-162续办核对并保存implementation-baseline | S0启动，真实调用限额待答 | 尚无产品测试结果；已有共享改动保留 |

| 2026-10-24 | S0/S1基线正常App真实原题，使用获准独立有限台账 | M1样本：1搜索、0命令、1最终答、0公开进度；Provider/Runtime正文hash一致 | 未据此修改Runtime；历史重复根因仍未知 |
| 2026-10-24 | S3/S4首版：原指令组合恢复进度原则，native v5安全投影、兼容reader及分段动作/文件明细 | Contracts6、前端112、Host定向、Native check与跨仓正常重开PASS | 实现待真实模型与UI验收；构建先被来源门禁正确拒绝，走原freeze刷新候选 |

### 2026-10-24 10:28 实施检查点

用户授权无变化。新App第三版正常启动；第二次原题与本地文件任务已完成。第二次原题2进度+1答案、Provider/Runtime hash一致；4真实curl均无正文，不伪称获取了网页。第三次3进度+1答案、六工具结果完整回灌、输出文件独立计算PASS。累计3/4回合、10/40HTTP、9/20网络动作。详细证据见second/third-complete-diagnosis、third-artifact-check、各次AX/PNG。

新增实际UI缺陷：刷新后手动展开丢失、长heredoc摘要占满主线，正在沿原阅读组件修复。当前目录未启用独立apply_patch工具，已查固定Runtime已有exec_command补丁拦截，第四回合用于正常续聊验证，不添加Runtime补丁。续办主记录已更新04。

### 2026-10-24 10:40 原生补丁实测与追加批准

用户批准最多追加3回合，总7，其余上限不变。第四回合真实补丁/续聊成功，证据fourth-complete-diagnosis、fourth-patch-live/complete。实测暴露无文件头hunk统计兼容缺口，修复后Host定向PASS；文件详情展开也复用当前页阅读选择，57项组件PASS与lint PASS。累计4回合/13HTTP/9网络。原App正常退出，新canonical冻结构建进行中；不是D4。

### 最终关闭记录（2026-10-24）

S0–S6按本地适用范围完成；详细Must映射与限制见02第2/8/9节。最后构建daily-final-build已去除临时Provider覆盖，日常App启动就绪；源码/worker与实测构建一致，Runtime未改。7回合/17HTTP/10网络；meter正常停止，正常重开无新增模型请求。所有先前失败保留。当前无待执行实现步骤；未授权提交、推送或发布，未执行用户禁止测试。续办入口04与长期记忆同步为实际状态。

- 2026-10-24复审收尾：真实第9专家续聊因输出上限未交付且无公开进度；第10普通原题有进度/答案但sleep1空执行，整体FAIL/in_progress。最新逐项判定以02第10节/07为准。日常canonical App恢复、最后两轮正常重开通过；10回合授权耗尽，meter正常退出，无新增Git操作。完整续办步骤落04。
