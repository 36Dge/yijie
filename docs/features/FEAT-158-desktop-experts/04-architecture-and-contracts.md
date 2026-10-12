# FEAT-158 — 架构复用与契约计划

> 2026-10-11 · 候选需求设计，未实现、未激活；Runtime 资格与契约验证均为 `NOT RUN`。
> 本轮只编写需求包。以下字段和操作是拟议领域语义，不是已存在的 API、数据库表或已发布 schema。

## 1. 推荐架构与边界

专家是易界管理的一组角色配置和知识资源。安装复用 FEAT-129 受管 Skill 包；会话角色投送复用固定 Runtime 的 `baseInstructions`；已存在会话的变更复用 FEAT-156 `SwitchThread` 的同 ID 正常生命周期。Desktop 继续通过 Native → Agent Host → 固定 Codex Runtime 执行，不新增 Agent 执行器、插件管理器、prompt 引擎、模型客户端或知识检索服务。

首期内置专家不依赖新增 MCP 服务。专家不会声明或自动启用 MCP、hooks、apps、subagents，也不改变当前模型、权限模式、审批、Provider 或网络配置。用户原有的市场服务选择继续受 FEAT-157 管理；专家角色不是工具授权。WorkBuddy 的目录层次可作为来源、专家身份、版本相互解耦的设计参考，不能直接照搬其安装路径、manifest 或能力开关。

| 责任 | 所属仓库与复用机制 | 本需求最小扩展 |
|---|---|---|
| 专家目录、角色和知识源文件 | `yijie-skills` 的资产生产、打包、版本和来源记录 | 增加专家用途、角色与知识资源声明；沿用确定性归档和来源摘要 |
| 跨仓包格式与请求/回执 | `yijie-contracts` 源契约 | 专家包用途、绑定修订、发送快照、兼容与失败语义；不手写影子 DTO |
| 安装、校验、恢复与 Runtime 适配 | `yijie-agent-host` 受管 Skills 服务、会话适配与原生切换 | 识别专家资源包，排除普通 Skills 全局投影；从受管资源解析已确认角色；绑定适配回执 |
| 目录、详情、召唤、聊天绑定和发送 | `yijie-desktop` 现有市场/聊天壳、Native 协调器、SQLCipher 与 outbox | 专家产品视图、每会话一个持久绑定、版本冻结、发送快照及历史展示 |
| 执行、历史、沙箱和审批事实 | 固定 `yijie-codex` Runtime | 复用已有接口，计划不修改 Runtime 核心、patch、版本或 transport |

`yijie-api`、`yijie-connectors`、`yijie-knowledge`、Coze 与云部署没有首期实现职责。知识库附件作为本地版本化参考资料使用，不引入 embedding、向量库、RAG、云知识上传或新的付费服务。

## 2. 已核实的工程事实

下列路径相对于 CrossBSD 工作区。调查时 Runtime HEAD 为 `7fd463bcef07f37b0211acd9f62b9f93ea0a4b12`，Host HEAD 为 `dce7a3c4e51e08c74e009a0ce3eeee256d929b3e`；此处是只读证据基线，不是 FEAT-158 交付 pin。完整工作区记录见 `evidence/repository-baseline.json`。

| Fact | 文件与行号 | 对方案的约束 |
|---|---|---|
| Runtime canonical schema 有 `baseInstructions` 和 `developerInstructions` | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/ThreadStartParams.json:315`、`:334`；`ThreadResumeParams.json:1353`、`:1372` | 可以使用现有原生字段，不发明 `setExpert`、`clearPrompt` 等 Runtime API |
| Personality 是三个固定枚举 | 同上 `ThreadStartParams.json:222` | `none/friendly/pragmatic` 不能代表任意专家人格 |
| 原生插件 manifest 解析 skills/MCP/apps/hooks/interface | `yijie-codex/codex-rs/core-plugins/src/manifest.rs:24`；`loader.rs:815` | 未发现 WorkBuddy 专家 `agent/systemPrompt` 等字段的等效直接导入；有 plugin API 不等于支持 WorkBuddy 专家 |
| 当前市场运行层明确禁用插件并检查隔离 | `yijie-agent-host/internal/codex/market_runtime.go:146`、`:169` | 保持 `plugins=false` 等既有约束；本期不以专家接入为由开启原生插件 |
| 已加载会话的 resume 可能忽略指令覆盖 | `yijie-codex/codex-rs/app-server/src/request_processors/thread_processor.rs:131`、`:3081` | 不能收到 resume 响应就认定角色已经更新；无订阅、idle、非运行且正常关闭完成后才可冷恢复 |
| 既有同 ID 正常切换已经存在 | `yijie-agent-host/internal/codex/chat_models.go:142` | `SwitchThread` 检查原生状态、待审批，再 unsubscribe/resume；不 fork、不改历史、不强杀进程 |
| 当前 Host 已经组装基础策略、模型与市场配置 | `yijie-agent-host/internal/codex/session_protocol.go:525`、`:545`、`:560`、`:601`、`:612`、`:628` | 专家叠加必须在既有组装链上完成，不能用专家全文替换权限基础模板或漏掉模型/MCP配置 |
| 显式基础指令优先于历史基础指令 | `yijie-codex/codex-rs/core/src/session/mod.rs:599`；`yijie-agent-host/internal/codex/scheduled_draft.go:101` | 移除必须显式恢复普通完整基础指令；省略/null 可能回退到历史基础指令。开发者历史可能仍保留原文 |
| Skills 有校验、receipt、操作持久化及回滚 | `yijie-agent-host/internal/skills/archive.go:21`、`:135`；`service.go:37`、`:815` | 复用安装核心；角色和知识等普通资源可放同一包，不能重复实现安装器 |
| 单归档仅允许声明的一个 SKILL.md | `yijie-agent-host/internal/skills/archive.go:80` | 角色和知识使用独立普通资源文件，不能伪装多个未经声明的 Skill 入口 |
| 当前 Skills 是进程级额外根及全局启用投影 | `yijie-agent-host/internal/codex/skills_protocol.go:305`；`internal/skills/service.go:697`、`:777` | 专家资源包的用途/投影过滤尚未实现；不能按会话增删全局 roots 或切全局 enabled 来模拟绑定 |
| 显式 Skill 输入必须匹配已加载且未禁用技能 | `yijie-codex/codex-rs/core-skills/src/injection.rs:140`、`:175`、`:179` | 不能将未注册或 disabled 的角色文件路径直接作为 Skill 输入；这不是隔离捷径 |
| Host 输入目前没有 Skill 分支 | `yijie-agent-host/internal/codex/session_protocol.go:166`、`:190`；`internal/session/multimodal.go:351` | 现有 text/image/file 不能冒称已支持专家显式 Skill 输入 |
| 市场提交已有意图持久化、互斥和同 ID切换链 | `yijie-agent-host/internal/session/market_submit.go:31`、`:132`、`:160`、`:174` | 复用发送与幂等边界，把专家纳入组合意图；不旁路既有流程 |
| 受管市场工具仍限制在 ask 模式 | `yijie-agent-host/internal/codex/market_turns.go:69` | 专家不扩大工具执行模式或把角色指令作为批准 |

源码中有 `policy.allow_implicit_invocation`（`yijie-codex/codex-rs/core-skills/src/model.rs:28`），但该元数据不能替代专家产品的会话绑定和资产投影边界。首选方案不依赖把专家当全局可用 Skill 后再靠提示词约束使用。

## 3. 资产、绑定与每轮快照

### 3.1 受管专家资源包

继续使用现有 Bundle/Archive/Receipt 的版本、校验、原子安装、扫描和错误恢复路径。候选字段在正式 source-first 阶段进入现有受管资产 manifest 的兼容扩展或新版本，不另外发布一套平行 manifest 解析器。

| 拟议领域字段 | 语义 |
|---|---|
| `asset_kind` | 区分普通 Skill 与专家资源包；新值不得直接发给不支持的旧 consumer |
| `expert_id`、`version`、`source_id` | 稳定专家身份、不可变内容版本、已核实来源；展示名称不是主键 |
| `role_resource` | 包内相对路径、UTF-8 文本摘要和字节数；只允许受管安装 receipt 中列明的普通资源 |
| `knowledge_resources[]` | 资源 ID、标题、包内相对路径、摘要、字节数和资料版本/时效说明 |
| `runtime_projection` | 专家仅作为资源和角色配置消费，不注册到普通聊天的全局 Skills 根/启用目录 |
| 现有 archive/provenance/license 字段 | 沿用现有不可变版本、来源和归档摘要；未核实分发依据不能伪填 reviewed/approved |

当前共享包权威源为 `yijie-contracts/jsonschema/skills/skill-bundle-manifest-v2.schema.json`；`yijie-skills/contracts/` 是精确消费的副本（该仓 README:24），不得当成第二权威。上述名称为设计词汇，最终字段名、枚举和生成物由 `yijie-contracts` 决定。专家资源的启用状态与“是否进入 Runtime Skills 投影”必须分开；仅把 `enabled=false` 当专家安装完成不可取，因为其旧含义是普通 Skill 不可用。

Host 根据受管 ID、版本与 receipt 解析文件。Renderer 不传任意绝对路径或任意系统提示词；包中的路径也不能决定 Runtime 的 CODEX_HOME、工作区、Provider、MCP 地址或可执行程序。知识正文按需读取，初始基础指令只带角色与简短资源索引，不把完整知识库每轮灌入上下文。

本期不复制 `~/.workbuddy/plugins/`。物理目录继续服从易界现有安装根，由安装服务拥有；不为模仿三级路径迁移既有 Skill 安装。来源、专家、版本的独立性先体现在 manifest 和快照身份。活动绑定及待发送快照必须解析到同一不可变内容；若当前安装核心不能保留被引用旧版本，采用“有引用时禁止升级/卸载并提示解除绑定”的首期限制，不另建旁路版本仓或静默指向新版本。

### 3.2 Desktop 业务状态与 Host 适配状态

Desktop SQLCipher 是会话专家绑定及用户可见记录的业务权威；复用当前 identity/tenant、会话主键与 Native 数据访问，不建立新业务数据库。候选数据形态：

| 对象 | 候选字段 | 不变量 |
|---|---|---|
| `ConversationExpertBinding` | `conversation_id`、`binding_revision`、`expert_ref|null`、`updated_at` | 每会话至多一名；普通模式也有明确 revision；绑定按完整版本，不指向 latest |
| `ExpertRef` | `expert_id`、`version`、`archive_sha256`、`role_sha256`、`knowledge_manifest_sha256` | 能证明实际解析的是选中内容；展示名称变化不改变身份 |
| `TurnExpertSnapshot` | `format_version`、`binding_revision`、`expert_ref|null`、`snapshot_digest` | 与当前 turn/outbox 原子冻结，重试、恢复和重放不读新的绑定覆盖旧意图 |
| 绑定变更操作 | `operation_id`、`expected_binding_revision`、`requested_expert_ref|null`、状态与失败类别 | CAS 检查修订；重复同意图返回原回执，不同意图复用 ID 返回冲突 |
| Host 适配 receipt | 操作/会话/原生 thread ID、快照摘要、应用结果或未知结果 | 只保存恢复与防重复所需事实，不保存第二份可编辑专家目录或第二套业务绑定主状态 |

`snapshot_digest` 需使用 Contracts 定义的确定性编码，并纳入既有发送意图摘要，不能只 hash 专家名称。普通模式的 `expert_ref=null` 是显式状态；缺失字段仅供旧格式解析，不能在新格式下悄悄解释成“沿用上次专家”。角色、知识正文和绝对安装路径不进入普通诊断日志、审计错误或回执。

新迁移采用 expand：旧聊天读作普通模式；已有消息、原生历史与旧 outbox 不重写、不补发、不伪造专家快照。不在本设计中预占实际 SQL migration 编号、bbolt schema 版本或表名；实现时以对应仓库当前版本为准。

## 4. 会话和投送时序

### 4.1 首次召唤与首次发送

1. 侧栏详情“召唤”回首页新对话输入区域；从已有对话菜单进入时回原对话，均沿03保存的返回上下文形成绑定意图。此动作不调用模型、不连接新工具、不发送专家开场白。
2. 首次发送在 Native 现有事务和协调器中确认安装可用、绑定版本与修订，冻结普通或专家快照，连同用户消息、模型、权限和既有市场选择进入当前 outbox。
3. Host 从可信边界接收版本化意图，按受管资源 receipt 解析角色及索引；不接受 Renderer 自由文本覆盖系统指令。
4. 复用 `StartThread`：先计算当前普通会话本应使用的完整基础指令与原生配置，再追加专家角色和资源索引。保留当前模式、模型、动态工具、权限及市场配置的既有组装与校验。专家不能把 `approvalPolicy`、`sandbox` 或 `approvals_reviewer` 改成其文档中的值。
5. 原生创建、turn 发送、事件及历史仍走现有链路；回执与产品记录关联实际同一 thread/turn，未知结果仍未知，不自动重新发送。

### 4.2 持续、多轮和变更

专家绑定持续到用户显式移除或更换；每次发送仍冻结一次完整快照，不能只在首次消息中塞入角色后靠模型“记住”。应用重开、模型切换、权限变更、市场重新绑定等任何可能 resume 的入口，都应从该次已确认组合意图恢复同一专家基础指令。

绑定修改、模型修改、权限修改、市场重绑定和发送必须进入同一会话串行化决策。复用并补齐现有 Native 协调器、outbox admission、Host `modelOperationMu` 和 Runtime `threadOperation` 的一致锁顺序，不新增互不知情的“专家锁”。现有各入口是否已经完整共享该语义尚未证明，是实施核对项；不能仅加一把锁便宣布并发问题解决。

以下任一状态阻止专家绑定变更：已有发送准备/待投递、原生 turn 运行中、待批准/待输入、清理中、未确定送达的 outbox 或适配操作。UI 保留原绑定并解释需先完成当前操作；不先改标签再让后台追赶，也不取消原审批、更换在途快照或产生隐藏 turn。

对于已有原生 thread，推荐变更顺序：

1. 获取既有会话操作所有权，校验 `expected_binding_revision`；确认无进行中或未知发送/批准。
2. 保存版本化变更意图，校验拟用专家资源；移除则准备普通模式快照。
3. 复用 `SwitchThread` 的状态检查与同 ID unsubscribe/resume，携带当前组合的完整基础指令和原生配置；不 fork、不新建隐藏 thread、不重建历史。
4. 正常完成且符合已验证的 Runtime 资格后提交新绑定修订并显示成功。若 Runtime/存储结果未知，保留可恢复操作并禁止新发送，不把未知当旧配置未生效或新配置已生效。
5. 恢复复用原操作 ID、原版本和现有回执/原生状态能力；不得自动发送业务消息探测角色。正常重绑可作为修复动作，但必须先排除在途 turn 和原操作冲突。

切换所需“指令确已生效”的观察方法须在资格验证阶段核实。当前 `ThreadResumeResponse` 并不提供本需求的角色摘要回显；不能发明 response 字段，或以仅校验 model/thread ID 代替角色投送证据。

### 4.3 移除及历史边界

`x` 移除成功后，下一次用户发送必须显式使用**当前模式、模型和工具组合下的完整普通基础指令**，不能发送空字符串、null 或省略字段期待 Runtime 自动恢复。组合函数应继续调用现有普通组装逻辑；禁止把固定权限基础模板删除、改写为专家模板，或在普通模式恢复时丢失其它已选配置。

过去轮次中的专家指令、已读取资料和对话仍是原生历史的一部分。移除表示停止后续轮加载该角色及其资源索引，不意味着模型忘记历史、知识脱敏、删除上下文或撤回之前执行。基础指令可说明当前专家已取消且不再沿用此前角色约束，但它不能成为清除历史的保证。历史中的专家标识/版本保留为当时事实，不被新的绑定覆盖。

计划任务草案及其它受限内部线程不继承普通聊天专家；保持原有 input-only/工具限制。原生模型或权限能力不满足角色投送资格时，功能显示不可用，不能退化为重写用户输入、创建隐形 thread 或另开模型请求。

## 5. 知识与工具复用

角色配置只声明专业方法、输出偏好、边界和可用资料索引。工作经历、专家能力和平台规则是参考资料的陈述，不能变成 Runtime 已有能力或真实资质保证。京东知识库必须附来源版本和时效提示；示例参数、费率、政策、时效或流程不被当作实时平台事实。

知识文件继续是受管普通文本，复用当前 Runtime 的原生文件/命令能力按需读取。固定源码已见 `exec_command`（`yijie-codex/codex-rs/core/src/tools/handlers/shell_spec.rs:89`）；不把 WorkBuddy 的 `Read/Write/Edit` 工具名写成易界必备 API。初次设计时所选包安装目录在每个现有权限模式下是否实际可读尚未验证；阶段4已补同一实际安装M03文件在ask/auto/full下的原生只读资格，边界见07；若不可读，应报告资料暂不可用或调整到已有合规资源访问路径，不能因此增加沙箱权限、部署新文件服务器或新建检索器。

能力声明必须与实际读取一致：当前共享 manifest 的 `model-only` 要求 `filesystem=none` 且无工具；Host `internal/skills/service.go:1129` 也只把这类普通 Skill 直接投影为 ready，其他可安装项可能为 degraded。本专家需要按需文件/命令读取，应使用源契约可表达的只读资源/工具声明，不可标成 `model-only` 或冒用 WorkBuddy 工具名；现有枚举表达不足时先扩权威源。专家就绪由受管内容有效、绑定可应用和所选权限模式资源读取资格共同决定，不能把普通 Skill 的 enabled/runtimeVisible/ready 直接复制作专家 ready，也不能为得到 ready 放宽权限。

没有外部实时资料或工具返回时，专家应区分资料结论与待核实信息。安装/召唤专家不会安装新连接器、读取凭据、拉取商家数据或申请外部网络授权；知识文件中的操作指令是资料内容，不能绕过用户意图和易界权限。

## 6. Contract First 与兼容顺序

本轮文档编辑本身 `contract-impact=none`：未改变执行、wire、数据库、Runtime 或发布产物。FEAT-158 计划实现按最保守 `contract-impact=breaking` 评审：现有 closed schema、manifest consumer、发送摘要、持久 outbox/reader 可能拒绝或误解新增专家形态，当前未取得方向性兼容证据。将来若有充分证明可重新分类，但不能因新增字段而先假设 additive。

| 边界 | 权威源与 producer/consumer | 计划 |
|---|---|---|
| 专家用途、角色和知识资源声明 | `yijie-contracts` 受管资产源 schema；Skills 产出，Host/Desktop 消费 | 先扩展/版本化源 schema、正常 fixture 与生成链；新用途不可先进入旧 consumer |
| Native → Host 专家意图、快照、回执 | `yijie-contracts` 现有相关共享 payload/操作源；Desktop producer，Host consumer及回执 producer | 先核对当前 Native 私有通道及发送契约，再在原权威源扩展；不另发明公开 `/experts` API |
| Host → Runtime | 固定 Runtime canonical schema；Contracts 兼容投影，Host adapter | 仅使用已存在 start/resume/unsubscribe；先验证语义资格，再更新兼容投影与消费说明；不反向发明 Runtime API |
| SQLCipher 绑定及快照存储 | Desktop migration/data compatibility | expand/版本化 reader；保留旧记录和普通路径；只有跨仓共享部分进入 Contracts |
| Host 恢复 receipt | Host 私有存储权威 | 按现有格式路由设计 reader/writer 升级；适配信息不升格业务数据库 |

实施依赖顺序：固定 Runtime 源码事实与无副作用资格 → Contracts 实际源 schema/正常示例/同源校验 → Skills 包生产与 Host provider/reader → Desktop reader/Native 消费与 expand migration → 新 writer 与专家入口激活。Runtime 无需源码候选变更时，明确记录“复用当前固定基线”，不为文档制造新 Runtime commit。

新请求先 provider 支持后 consumer 发送；新响应/枚举先让相应 reader 就绪后 producer 发出。旧普通请求保持原语义，新格式必须显式表达普通或专家。若旧 closed consumer 不容忍，采用版本化或双轨读取，禁止多仓同时硬切。新 outbox/回执必须验证旧数据→新 reader及新数据→已声明回滚 reader；未知格式不触发旧发送路径重新执行。

`demo_fast + local` 依手册允许 source-first、适用 generate/lint/focused conformance 完成后用当前 sibling commits 做本地闭环；必须记录真实来源，不能写成已发布兼容或消费者批准。下游可发布来源需固定精确版本、完整 commit、digest/generator 与实际 consumer pin；公开/生产前补齐相应治理与不可变发布要求。此文尚无 FEAT-158 契约版本、tag、PR、migration 编号或 consumer pin，均不伪填。

安全回退顺序：停止新专家写入/召唤 → 等待既有正常操作结束并保存未知状态 → 保留兼容 reader、已冻结快照与版本资源 → 仅对 idle 会话正常切回完整普通基础指令 → 根据已验证 reader/migration 兼容范围回退代码。不能删原生历史、清空 outbox、改 DB 版本绕过 reader、卸载被引用资产或从受管目录直接删除文件。存在未知在途状态时停止切换并报告，不能以强杀或重发解决。

## 7. 激活前资格与安全验证

以下全为 `NOT RUN`，是后续实现的必要验证，不是本轮已完成工作。按正常非破坏性路径验证；真实模型/外部服务调用必须另获当前任务授权与额度，不挪用其它 Feature 的历史预算。

| 编号 | 资格/验收事实 | 失败时边界 |
|---|---|---|
| Q-158-01 | 固定产物与选定 Provider 下，同一 thread 启用专家、连续多轮、移除、再启用的基础指令投送符合快照；thread ID 不变 | 无资格不激活专家执行；不另开模型客户端或隐藏 thread |
| Q-158-02 | 已加载 idle 会话 unsubscribe/resume 正常完成；仍有订阅或原生未关闭时不误报指令已更新 | 保留原绑定/未确定变更，阻止新发送；不忽略 override 警告 |
| Q-158-03 | 冷恢复、正常退出重开、模型切换、权限变化、市场重新绑定均保留当前专家/普通完整基础组合 | 修复统一组装入口，不逐路径复制不同 prompt 模板 |
| Q-158-04 | 运行、待批、pending/unknown outbox 时变更被一致阻止；重复操作、revision冲突和正常重试不更改原意图 | 不取消审批、不猜终态、不补发旧消息 |
| Q-158-05 | 两个聊天各自绑定不会串角色；普通聊天没有专家包的全局 Skills 投影或隐式角色注入 | 不以每轮全局 roots/enabled 开关作为补救 |
| Q-158-06 | 所选受管知识文件在现有实际权限模式下可正常读取，引用可定位到冻结版本；不可读时明确反馈 | 不扩大权限、不新建 RAG、不承诺全部资料已读取 |
| Q-158-07 | 安装、扫描、启用/不可用、正常卸载限制与升级限制复用同一受管机制；引用资源不被替换 | 禁止静默追随 latest；首期必要时限制有引用资产升级/卸载 |
| Q-158-08 | 旧普通记录和新专家记录可被新 reader 正常读取；未知格式不会降级重发；回退只到合格 reader | 不执行未获授权的不可逆迁移，不篡改数据库版本 |
| Q-158-09 | 原生审批、沙箱、模型配置及现有市场边界不变；专家文本不能产生工具授权 | 不自动安装/连接 MCP，不依据角色文档扩大执行权 |
| Q-158-10 | 正常路径能观测角色恢复普通；UI/历史准确说明旧知识与对话仍在上下文中 | 不把移除宣称为清除历史或完全遗忘 |

本轮未运行任何 Runtime、构建、模型、MCP、数据库 migration 或进程生命周期验证。后续同样禁止强杀制造异常、替换二进制、破坏文件权限及攻击性 fixture；若既有测试包含这些步骤，跳过并记录未执行项目、原因及影响，采用正常启动、退出、只读检查和普通样例验证。

## 阶段4显式恢复源与实现边界

`experts/1`本地候选增加两条Native命令和两条原管道方法，当前共10条Native/11条private，仍按整体breaking管理，未发布。UI只交原operationId（绑定另带local session）；Native从原SQLCipher journal取完整原请求，外层另带当前scope和Host身份。Host用当前写权许可此次恢复，用原完整payload的HMAC匹配已有意图，保留原scope、Host nonce、ref与revision。

绑定恢复在原会话/线程、原模型修订/权限和空闲条件下，复用完整base正常重绑；仅豁免自身未完成binding，不豁免其他turn/outbox/审批或计划预约。资源恢复只观察原Skills journal，或在既有mutation lane/operation锁内明确结束确认未执行的操作，防止晚到同ID再开始安装。正常刷新、查询和重开仍只读；恢复失败不清unknown，不另开ID，不发探测turn，不扩大权限。具体源与current pins见Contracts `docs/experts-v1.md` 和本包阶段4证据。
