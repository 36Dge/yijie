# 易界项目 Codex 长期协作记忆

## 文档状态

- 状态：Accepted
- Owner：段成威
- 最后更新：2026-09-10
- 适用范围：`yijie` 多仓项目的需求起草、调查、设计、实现、验证、评审与发布协作

## FEAT-132 当前权威（2026-09-09）

用户已授权将 FEAT-132 改为“Codex 原生对话机制接入与视图适配”，删除自建 reducer、hydrate/reconcile、正文对账、身份猜测与自动封口；不得迁移或换名保留。Codex 决定执行事实，Desktop 保存加密产品记录，Native 仅一处显示缓冲；旧记录只读。

当前实施已授权并完成本地源码提交，最终 contract-impact=breaking，必须版本化迁移旧消费者。Desktop migration 14 / Host schema 5 都不允许无兼容方案降级写入。固定 Runtime/FEAT-136 产物不变，FEAT-137 永久退役，FEAT-152 权限语义不变。

原 D4 不继承。本次已固定 Contracts 6f632f155eacdaf93df0e0b00b5dab9e369c5442、Host 9e9d317f7e4ecff5f8aeec94fa467f9bede32139、Desktop 5e6ada73ed8b9d49dde51e4b6659ce5337304a6e；FEAT-152来源阻塞已解除，FEAT-137永久退役。用户明确授权本地提交、必要修复及25次文本/3次图片预算；实际19次文本、1次图片，临时权限模式已恢复请求批准。真实canonical启动/附件/命令/三种权限模式/原生中断/退出重启/Artifact验收通过，十项AC与local D4均PASS；未推送或发布。详见[最终验收](../features/FEAT-132-desktop-conversation-domain-state-machine/02-verification.md)。

2026-09-09日常入口收尾已通过：Desktop当前为c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b，包含单独提交的权限弹窗UI、说明修正及旧清理记录的只读历史修复；Contracts/Host来源不变。普通canonical入口沿用原Host Home和app-data，8条原Host映射及最后Turn身份/状态保持一致，旧附件历史与Artifact正常重开。本轮未增加模型调用，历史清理未完成、附件过期及隔离Host缺少映射仍如实保留。详见[日常入口报告](../features/FEAT-132-desktop-conversation-domain-state-machine/05-daily-entry-verification-2026-09-09.md)。

用户随后明确授权所有仓库审计、提交与推送；上述验收报告中的“未推送”是当时的历史状态。本次同步现有工作分支，修正Contracts/Host说明，源码consumer pin保持不变；Desktop CI来源/目录布局和Host旧测试断言仍列为合并前事项，不能把Git推送等同完整CI或发布通过。详见[多仓审计与同步记录](workspace-git-sync-2026-09-09.md)。

## FEAT-134 当前权威（2026-09-09）

FEAT-134已按用户确认任务收敛为FEAT-132 native v7之上的流式/过程展示：summary与raw按原生类别/索引分开，Item availability及安全诊断可见，UI busy仅由当前有效订阅观察驱动，Turn结束不封口Item。旧v4/v5历史及资源适配保留，无调用发布残留及冲突测试已清理。原2026-08-29 D4完整归档，本次八项AC与local D4通过。

当前本地提交：Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3、Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b、Desktop 6e5047d1c23041c46dd495ddb89e24c7e4db5d47。native Contracts源仍固定6f632f…；Desktop权限消费者及CI改用真实Host提交，42项来源校验通过。CI目录布局已修正，但本轮不推送，不代表远端CI/合并/发布通过。

普通canonical入口使用原app-data/Host Home，两次正常启动/退出，既有历史/附件/Artifact/权限入口复查通过，8条原Host映射及原生终态未变；233项前端定向测试及Host/Native/SQLCipher验证通过。本轮模型请求0，不转用FEAT-132或原FEAT-134预算。原生缺阶段/冷历史不完整、Command完成后展示输出、附件过期、清理未完成和隔离任务无Host映射等限制仍保留。详见[FEAT-134最终验收](../features/FEAT-134-desktop-streaming-progress-final-response/02-verification.md)。

## FEAT-131～136 一致性审计（2026-09-09）

FEAT-134 四个本地提交在用户“授权执行”后已按 Contracts → Host → Desktop → 元仓顺序普通推送，远端 SHA 相等；精确 SHA 的 Actions 查询均无运行，CI NOT RUN。没有合并、tag 或部署。本轮新增修改没有混入这四个提交。最新状态以 [FEAT-134 远端记录](../features/FEAT-134-desktop-streaming-progress-final-response/04-remote-delivery-2026-09-09.md) 为准。

FEAT-136 现状审计确认：命令执行和最终输出来自 Codex，Desktop 复用 FEAT-132 native v7/唯一缓冲/SQLCipher；Host native 主动不传 Command delta 正文，等待 aggregatedOutput 后安全投影。旧 v5 有真实兼容路由和容量计数，不能整包删除。审计发现的目录标签、输出完整性、空输出与历史 running 文案问题已按[执行方案](../features/FEAT-136-desktop-command-tool-items/03-native-command-audit-and-plan-2026-09-09.md) 实施并取得本次八项 local D4 PASS；真实3/10文本、0图片，两条 Command 成功/失败及正常重开通过。本次交付收尾已另获明确授权，Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688 → 元仓 4e6645574fdfe7d29f7c551564bf807cf8222d48 已普通推送且远端 SHA 相等；两提交 CI 未触发，NOT RUN。详见 FEAT-136 的 04-delivery-closure-2026-09-09.md。原验收 base commit 与逐文件 SHA-256 保留；原 2026-08-30 五项 Command D4 保持历史语义，Tool 仍属 FEAT-144 blocked / NOT RUN。

六项需求已补充当前依赖与证据适用范围，能力矩阵修正为当前 native 事实。后续不恢复 ConversationState/reducer、正文对账、身份猜测、自动封口或历史重建；日常 app 与原 stable 隔离数据、FEAT-152 与已终止 FEAT-137 分开记录。详见[整体一致性复核](../features/FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。审计阶段模型调用为0，授权后的FEAT-136实施验收为3/10文本、0图片。

## FEAT-144 当前需求权威（2026-09-10，AC-004用户排除、业务授权10次）

固定Runtime0.144.6原生元数据连接阻塞已关闭：操作7初始化ready、操作8返回97工具/Sorftime MCP1.1.6；无query URL、原生bearer_token_env_var引用及真实User-Agent codex-mcp-client/0.144.6。连接技术依据保留13；当前范围/预算权威为[15用户决策](../features/FEAT-144-desktop-real-tool-producer-items/15-owner-scope-and-business-budget-2026-09-10.md)及分账台账。没有等待输入或存留诊断Runtime，不重复消耗额度验证同一连接。

累计10次元数据操作授权（含正常握手/重试/清理）已用完；模型4/8、业务1逻辑调用保守扣2/10尝试、图片0。正常unsubscribe/EOF exit0、新目录和输出秘密精确扫描无命中；操作7/8的6 POST span来自共享进程摘要，不能重复加为12；完整HTTP尝试数未知。产品原生配置/Prompt与canonical真实成功已验证；D4被权限重启配置冲突阻断，见20。

原操作1–3及6的HTTP400/request error失败历史保留。两版实际二进制对普通localhost服务的初始化观测除真实版本外一致，固定版缺User-Agent；仅补真实UA后固定版远端成功，足以确认该原生配置可用，不等于证明服务端唯一拒绝规则。操作4/5的本地Codex0.153.4对照仍为历史证据。固定binary SHA 4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d不变；未升级/修改/替换Runtime或安装ZIP bridge。

product_detail及asin/amz_site输入schema当前由固定操作8确认，asin必填、US显式传入；只启用该单工具。enabled_tools不限制参数，审批要呈现原生tool_params中的实际ASIN/站点；参数不明或越界拒绝，不从助手正文推定授权。首期只读US公开商品查询，无商家写入，不承诺服务端幂等或免费。

结果采用原生text块/稳定索引、最多32个原始content条目和既有256KiB UTF-8容量、复用既有完整文本脱敏后纯文本展示。safeNativeText仅NUL/容量处理，不能冒称脱敏。未返回outputSchema/annotations或progress不补造，也不独立阻断该展示设计；没有可展示文本不代表商品无数据。status/availability/诊断/busy分离，原生failed即使error=null也不改completed。

[12契约与reader方案](../features/FEAT-144-desktop-real-tool-producer-items/12-independent-contract-and-reader-plan-2026-09-10.md)已细化：Contract First；兼容reader/格式版本拒绝先于新producer写入；未知格式用本地recordDiagnostics定位，不生成NativeView或触发冷读补建；DB user_version过高仍整体拒绝。schema15 expand migration已实现并通过合成数据前向验证，旧JSON/历史migration不改，回滚仅到已验证兼容reader，不复制用户DB。

秘密首期只存受管进程内存，正常重开重新输入；原生shell_environment_policy.exclude需核对set和实际执行环境不重注入。稳定elicitation空form按request/thread/可信turn关联，原生accept/decline/cancel/resolved处理，无itemId不猜卡片；其它未支持请求继续拒绝。FEAT-152语义不变，FEAT-137永久退役。

首期Sorftime只在“请求批准”及已核实原生on-request/user/workspaceWrite/networkAccess=false、工具approval_mode=prompt的受管配置下激活；不把prompt当必出面板的保证。自动审查/完全访问保持FEAT-152原语义，但本期Sorftime不在这些模式激活，不自动切换模式；未知有效配置或审批被hook/插件替代时不激活。实际thread响应/配置与Prompt已验证；正常模式切换时重启被配置门禁阻断，权限保持ask；原生Prompt不复用Auto批准缓存。

用户已明确“不做业务失败场景的验证，跳过这个逻辑实现”：AC-004/F144-S03从当前Must范围移出，标OWNER_EXCLUDED/NOT RUN，原编号不复用、旧四文件逐字归档、不算PASS。不新增Sorftime业务错误字段、分类器、失败专用分支或样本；已有原生failed与通用安全处理仍如实保留。无需再索取官方正常失败条件，不用成功/空结果或权限拒绝替代业务失败通过。

用户确认业务余额充足并授权10次Sorftime业务请求。保守口径为tools/call尝试共10次，含原生404重发；每个逻辑调用先预留最多2次，不足则不启动，不能视为10逻辑加10重试。业务1次逻辑调用、HTTP次数未知，保守扣2/10；元数据10/10独立；模型另获8次文本授权、已用4/8；图片0且未授权。扣费公式未核实但不再阻塞该明确预算，不承诺重试免费。14备用取样在这份预算内但非D0必要步骤，本轮不消耗额度。

D0根据用户新范围与授权重新审定并实跑PASS（exit0），strict及50项元仓测试通过；9项活动Must为6项PASS、AC-006 pending、AC-007/008 fail；产品实现与本地来源已固定，真实查询/拒绝与返回值对照通过。权限切换重启受原生projects/受管模板冲突阻断，D4未通过且无等待输入。通用D4仍保留AC-007的既有输入/原生权限正常拒绝检查，不能冒充AC-004或另做业务失败逻辑。继续复用Codex与FEAT-132唯一缓冲/SQLCipher/thread-read，不造执行器/推演/对账/重建/封口。后续Contracts→兼容reader→Host/Desktop→定向验证→canonical→D4；产品实施/migration、本地提交与8次模型请求已明确授权，推送未授权，业务预算不代替它们。

前期D0收尾仅改元仓文档，后续产品实现和必要启动修复已本地提交；最新权限重启阻塞只追加证据与文档，不改产品代码或来源锁。Desktop228a95a4929a53bbb6aafc76156161d642d72153并发界面内容保护；无推送/tag/部署。原包和05–12阶段历史保留，当前事实以20和分账台账为准。

## 1. 单人开发角色默认值

易界当前采用“段成威一人使用 Codex 开发”的工作模式。除非段成威针对某个需求明确指定其他人，新 Feature Package 和交付文档默认使用以下角色：

| 角色 | 默认负责人 |
|---|---|
| 需求负责人 | 段成威 |
| Product/Design 决策人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |

Codex 起草新需求包时应直接填入这些默认值，不重复询问。某个需求存在临时协作者、外部评审人或专门 Owner 时，以段成威在该需求中的最新明确指令覆盖默认值。

同一人承担多个角色不表示适用 Profile 的确认可以伪造：

- `production_hardened` 的需求确认、技术批准、代码评审和发布批准仍是不同动作，必须分别记录真实日期与结论。
- `demo_fast` 至少分别记录 D0 产品/UX确认、D4 真实可用结论，以及条件性的付费/破坏性/公开操作批准。
- Reviewer 为段成威时，不得把 Codex 自己的总结描述为“独立人工评审”。
- Codex 必须在实现完成后执行一次与实现阶段分离的结构化审查，主动寻找错误假设、回归、权限、兼容、测试与回滚缺口；最终批准仍由段成威作出。
- 高风险安全、资金、数据删除、生产迁移或不可逆架构决策即使由同一人负责，也不得降低确认、验证、审计和回滚要求。

## 2. Codex 与段成威的职责边界

Codex 默认负责：

- 调查当前代码、文档、测试、Git 状态和多仓影响；
- 起草需求、验收标准、影响评估、决策选项和风险；
- 给出有证据的推荐方案及取舍；
- 起草契约、技术设计、测试计划、实施切片和验证证据；
- 在获得适用门禁后实现、测试、审查和整理交付材料；
- 如实报告失败、未执行项、假设、未知项和残余风险。

段成威负责：

- 最终确认用户价值、范围、优先级和业务语义；
- 最终确认产品、设计、技术、安全和生产决策；
- 审阅 Codex 的候选方案、代码和验证证据；
- 明确授权提交、推送、发布、迁移和外部写操作。

Codex 不得虚构段成威已经批准尚未展示或尚未确认的内容。段成威明确授权“由大模型自行构思/定稿”时，Codex可以选择推荐方案并写成候选决策，但仍要说明理由、影响和验证方式。

## 3. 每次需求起草前的强制高质量协议

Codex 在输出需求结论或开始修改文件前，必须完成以下检查。不能用“快速总结”代替真实调查。

### 3.1 加载上下文

1. 读取本文件、当前作用域的 `AGENTS.md`、Feature Delivery Handbook 和已有 Feature Package。
2. 读取用户本轮请求、附件、视觉稿、已确认决策和前序未完成事项。
3. 从 `repos.yaml` 确认可能受影响的仓库；进入仓库后重新读取该仓规则。
4. 检查相关仓库的 branch、完整 HEAD、remote 和 `git status`，保护已有改动。

### 3.2 核对工程事实

1. 找到真实入口、路由、调用链、状态管理、持久化、权限、测试、构建和发布入口。
2. 阅读相关源码、测试、设计 Pattern、ADR、安全和契约文档，不根据文件名或聊天印象猜实现。
3. 明确区分：
   - Fact：已有代码、命令输出或用户明确确认；
   - Assumption：为继续推理采用、但尚未确认的前提；
   - Unknown：必须调查或由段成威决定的事项；
   - Conflict：代码、设计、需求或 ADR 之间的不一致。
4. 对可能随时间变化的外部事实使用当前权威来源验证，不依赖旧记忆。

### 3.3 完整推演需求

起草时至少推演：

- 目标用户、问题、价值、主流程与明确非目标；
- success、loading、empty、error、permission denied；
- 超时、取消、重试、重复、并发、部分成功和恢复；
- 认证、资源授权、租户隔离、secret、PII、日志和审计；
- 数据生命周期、持久化、migration、兼容和回滚；
- 性能、可访问性、主题、最小窗口和可观测性；
- 外部副作用、审批、费用、生产账户和不可逆操作；
- 公共契约、Runtime、第三方、模型或 AI Eval 是否受影响。

`demo_fast` 仍需推演这些场景以避免逻辑和 UI 空洞，但可以把不影响本地正常使用的性能、完整安全
专项、韧性、migration、可访问性和生产观测明确登记为延后；`production_hardened` 逐项写
`N/A + 理由`，不能静默省略。

### 3.4 形成高质量决策

1. 对重要未知项给出 2—3 个真实可行方案、取舍和推荐理由。
2. `demo_fast` 优先选择逻辑完整、交互清晰、依赖最少、能最快通过真实服务的方案；`production_hardened` 优先选择可维护、可测试、可回滚且不扩大权限/契约范围的方案。
3. 段成威已经授权 Codex 自行决定时，使用最佳工程判断推进，并把决定、理由、兼容和回滚写入文档。
4. 只有会实质改变目标、安全、数据、成本或不可逆架构的缺失信息才停止请求确认；其余问题给出推荐默认值并继续。
5. 不因赶进度降低当前 Profile 的 Must AC、Contract First、secret/PII、服务端授权、审批/审计和真实服务标准；Demo 可按已声明边界延后非必要生产加固，不能把延后项写成 PASS。

### 3.5 建立可追踪交付链

`production_hardened` 必须能追踪：

```text
用户价值
  → 业务规则
  → 验收标准
  → 技术设计
  → 测试用例
  → 实施切片
  → 验证证据
  → 发布与回滚
```

`demo_fast` 使用更短链路：

```text
用户结果 → 业务规则/UI 状态 → Must AC → 整体实现 → 真实服务 fresh run → Artifact/限制
```

Codex 完成需求草案后必须自检：

- 是否存在相互冲突的 Must 规则；
- 每条验收标准是否可判定、可测试；
- 是否把假设写成事实或把候选写成批准；
- 是否遗漏失败、权限、持久化、兼容和回滚；
- 是否错误扩大到用户没有要求的业务能力；
- 当前 Gate 状态是否与真实文档和验证证据一致。

## 4. 开发与门禁原则

- 新需求默认 schema v3 `demo_fast + local`：D0 后整个需求连续实现，不建立治理切片；实现结束立即启动真实服务，有 Bug 就修复、重启、复测，直到一次 fresh run 中全部 Must AC、真实 happy path 和代表性 failure/retry 通过 D4。
- `demo_fast` 默认目标 12 小时、硬停止 16 小时。`exposure: public` 在首次对外访问前补 DP；出现付费用户、SLA、多租户/PII、重要持久数据、不可逆 migration、合规或生产责任时建立显式 `production_hardened`。
- `production_hardened` 保留原规则：G0/G1/G2 前不开始正式实现；`contract-impact != none` 完成适用 G2A；provider/consumer 大规模实现等待 G2V；按 per-slice G3→G4→G5→G6 推进。
- 两种 Profile 都必须 source-first：先确定并修改契约权威源，再生成/验证和更新下游；不得复制影子 DTO。Demo 本地 sibling 结果不冒充不可变 tag、发布兼容或生产批准。
- 测试、构建、视觉检查、集成、生产 smoke 和发布状态只根据真实命令与环境证据填写。
- commit、push、tag、发布、生产迁移和外部写操作仍需要段成威的明确授权。

### 4.1 production_hardened 三次失败熔断

当同一命令、门禁、runtime 阶段、稳定错误码或实质相同的失败条件连续出现三次时，Codex
必须停止机械重试以及“改一点—再验证”的惯性循环。即使此前获准多次重试，第三次同点失败后
也必须先进入深度反思；重复执行相同命令不能算作新增证据，不能以“再跑一次可能会绿”代替
根因分析。

进入深度反思后必须：

1. 汇总三次失败的时间线、完全相同与发生变化的证据、已做修改及每次修改为何没有触及根因；
2. 重新区分 Fact、Assumption、Unknown 和 Conflict，撤回已被证据否定的判断，不把稳定
   failureCode 的命名直接当成已证明的根因；
3. 从局部症状扩展到完整调用链和状态生命周期，允许扩大只读搜索/审计范围至受影响仓库、
   路由、权限、状态管理、构建配置、runtime、平台行为、测试 harness、规范和门禁，寻找所有
   重试共同依赖的不变量；
4. 明确区分实现缺陷、harness/观测缺陷、环境或平台缺陷、规范/门禁矛盾及数据/时序竞态；
5. 形成按证据排序、可证伪的根因假设，为每个假设列出最小区分证据，并只推荐一个下一步
   诊断或最小修复；
6. 复核安全、权限、契约、持久化、cleanup 和用户已有工作树，确保扩大审计范围不等于扩大
   写入或实施授权；需要新写入范围、外部副作用或新的真实 runtime 时，先取得明确授权；
7. 在根因未收敛前，不提交、不更新 PASS/门禁状态、不启动依赖该门禁的后续切片，也不通过
   绕过 production 路径、放宽断言或把失败分类改名来制造绿色结果。

深度反思的输出至少包含：当前真正卡住的最早阶段、三次失败证明了什么和没有证明什么、
此前方法的错误假设、扩大审计后的候选根因、区分候选所需的最小证据，以及推荐方案的停止
条件和回滚。修复完成后优先执行 focused 静态验证，再在单独授权下执行一次有区分力的真实
验证；不得重新进入无上限的验证—修复循环。

### 4.2 demo_fast 调试时间盒

- 30 分钟没有新事实：停止猜测式补丁，检查真实日志和完整调用链；
- 90 分钟同一核心阻塞：采用最简单方案、关闭非核心花活或提出一个 workaround；
- 非核心测试/harness 累计 120 分钟：登记限制并降级，不继续阻断业务结果；
- 核心结果 240 分钟仍不可用：更换架构、缩小 MVP 或请求一个关键决定；
- 总工时达到 16 小时仍未 D4：停止扩建流程并重新定范围。

时间盒不允许“重跑到绿”、隐藏失败或降低 Must AC。每轮修复必须基于新增事实，D4 仍要求一次真实
fresh run 完整通过。

## 5. 长期记忆的使用边界

本文件记录稳定的协作偏好和角色默认值，不替代对当前代码与环境的调查：

- 当前实现、版本、仓库状态、API、依赖和生产环境必须每次重新验证。
- 最新的用户明确指令优先于本文件中的默认值。
- Feature Package 是单个需求的权威交付记录；本文件不能替代需求内的具体决策和证据。
- 如果工作方式发生长期变化，应更新本文件的状态、日期和变更内容，不依赖聊天历史维持隐含规则。

## 6. 本地优先开发与生产安全补齐

本节保留 FEAT-125 等历史 `production_hardened` 包的里程碑语义。2026-08-23 之后的新本地需求默认
直接使用 `demo_fast + local`，不再为本地 Demo 机械建立 G0–G6；历史 v1/v2 Gate 状态不因新默认而重写。

易界当前允许在尚未购买云资源、未准备生产 IdP 和签名发布能力时，把安全基础需求登记为
`Local Engineering Baseline Complete / Production Activation Blocked`。该状态只表示契约、
服务端领域能力、consumer、默认关闭策略及本地合成验证足以支撑后续业务代码开发，不等于
Code Complete、Production Ready、Delivery Complete 或发布授权。

进入该状态后：

- 可以继续开发首页、聊天、Tasks 等业务功能，并使用本地合成 identity、tenant、RBAC 和
  capability 数据验证流程；
- 每个新业务需求仍须建立自己的需求包并通过适用的 G0/G1/G2/G2A、测试与结构化审查；
  FEAT-125 本地基线只解除对生产身份环境的等待，不是跳过后续需求门禁的通行证；
- 身份与权限 feature flag 必须继续默认关闭，业务 API 的服务端授权、租户隔离和审计要求
  不得用前端投影、mock 或本地里程碑替代；
- 未完成的真实 IdP、签名 Keychain、跨仓 bearer、refresh-family、性能、监控、部署和回滚
  证据必须作为可追踪的生产激活阻断项保留，不得写成已接受风险或 PASS；
- 当段成威决定真实部署整个 yijie、购买/准备服务器数据库公网资源、选择生产 IdP，或准备
  Desktop 签名发布时，必须先恢复完整生产级身份安全链路，复跑对应 S7/G4/G5/G6，之后
  才能打开 feature flag、创建 release tag 或进行生产激活。

FEAT-125 是该策略的首个实例：本地工程基线完成，S7 冻结到真实部署准备阶段；FEAT-124
G4-001 与 FEAT-126 的 Tasks 服务端资源授权仍按各自生产门禁保持开放/阻断。

## 7. 变更记录

- 2026-07-30：建立单人开发角色默认值和需求起草前的强制高质量协议。
- 2026-08-01：增加本地优先里程碑规则；FEAT-125 本地工程基线完成后允许继续业务开发，完整生产级身份安全链路在真实部署前强制补齐。
- 2026-08-22：增加“三次同点失败后强制深度反思”规则；停止机械重试，扩大只读审计范围并以可证伪证据寻找根因后，才允许提出下一步诊断或修复。
- 2026-08-23：依据 ADR-0017 建立双 Profile；新需求默认 `demo_fast + local`，以产品/UX完整、整体实现、时间盒和真实服务 D4 闭环为准；公开 Demo 增加 DP，生产加固保留原 G0–G6 与三次失败熔断。


FEAT-144当前检查点以[20实际D4与权限重启阻塞](../features/FEAT-144-desktop-real-tool-producer-items/20-d4-permission-restart-blocker-2026-09-10.md)为准。Contracts db54c617c65db5431b950eb297ba148a43a8e600、Host 635846f72ef4b0d940798215e7b79d58aed6c591、Desktop 95afd425fd5b55ada9f13b43421ad2c06830dc5c；最低reader 25b004fbd5a4dcf642a503d302c21a7d6e3b817f先于writer固定。均仅本地提交，Runtime未改、FEAT-137永久退役、FEAT-152语义不变。

普通canonical使用现有app-data和日常Host Home完成真实Sorftime查询、原生Prompt正常拒绝、返回值对照及UI/旧历史检查。用户已授权本次临时auto/full并恢复ask，但auto触发旧Runtime正常退出后，Codex原生projects信任记录与Host精确受管模板冲突，重启被拒绝；权限仍ask，full未尝试。所有进程已正常退出，没有等待输入。Tool事实已存SQLCipher，普通Tool重开尚未验证；D4未通过，AC-004仍用户排除。先审定原生信任记录与受管配置兼容，不忽略/删除projects，不换Home掩盖问题，不放宽门禁。元数据10/10、模型4/8、业务1逻辑调用保守扣2/10、图片0；重连另需元数据授权，不转用额度。
