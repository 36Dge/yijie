# FEAT-172 深度复审与修订结论

> 历史审计/修订 2 记录。2026-11-12 用户追加“选定专家不可用不再内置兜底”；涉及兜底、preflight、结果归并的建议已撤回，以 [修订 3](04-implementation-design.md) 为准。源码证据保留，不作为当前实施或验收结论。

2026-11-12。用户要求重点复审原生能力复用、专家优先/内置兜底闭环及凭据过度设计；发现问题直接修订，本轮仍不执行实现。

结论：初稿的核心方向可保留，但有三类问题：把可通过现有配置完成的入口迁移扩大成Runtime补丁重基；把本机受管凭据供给扩大成新API/数据库/额度平台；未充分复用原生MCP结果、继续执行和Artifact状态，且提交前降级与事件竞争缺少落点。已直接重写04/05，并同步Brief、验证、feature.yaml及Proposed ADR。

## 1. 复审依据

本轮继续审计初稿57个文件，并新增10个入口，共67个文件；分支/HEAD/工作区和修改前方案摘要见[review-source-audit.json](references/review-source-audit.json)。未读取Keychain、未调用模型、未启动或停止产品。

核心新增证据：

- [Runtime gate](../../../../yijie-codex/.yijie/patches/chat-models/0019-host-image-generation.patch)：host_images_enabled要求yijie_host_images及Feature::ImageGeneration；两者可显式关闭。
- [Host Runtime资格](../../../../yijie-agent-host/internal/codex/runtime.go) 380–384行：当前NativeTools候选允许不启用HostImages，源码支持“保持当前Runtime、换Host装配”。不是只有删除0019才可迁移。
- [原生继续执行](../../../../yijie-codex/codex-rs/core/src/stream_events_utils.rs) 326–356行及[run_turn](../../../../yijie-codex/codex-rs/core/src/session/turn.rs) 297–372行：工具调用令needs_follow_up为true并继续原生采样。
- [原生MCP完成事件](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs) 832–950行及[app-server结果类型](../../../../yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/mcp.rs) 131–168行：已有身份、参数、结果与错误；结果存在截断边界，isError不单列在该item结果类型中。
- [Host原始事件入口](../../../../yijie-agent-host/internal/session/service.go) 700行及[native投影](../../../../yijie-agent-host/internal/session/native_conversation.go) 307行：可在UI投影前派生媒体状态；已有ReadThread获取原生快照。
- [状态查询](../../../../yijie-agent-host/internal/session/document_runtime.go) 56–89行及[Artifact Status](../../../../yijie-agent-host/internal/artifact/store.go) 263–285行：状态能力已存在，只是错误地与文档环境绑定，宜解耦而非重复创建。
- [专家提交](../../../../yijie-agent-host/internal/session/market_submit.go)、[PrepareMarket](../../../../yijie-agent-host/internal/codex/market_turns.go)及[绑定校验](../../../../yijie-agent-host/internal/session/experts_storage.go)：空选集也有worker前置，不能只在生图handler中做fallback。

## 2. 问题与直接修订

| 编号 | 严重度 | 初稿问题与影响 | 修订 |
|---|---|---|---|
| R01 | 高 | 为移除模型入口，要求删0019/重基后继链、重编Runtime并更改schema，扩大核心变更且没有先用已有gate | 当前固定Runtime不改；Host显式false两项图片配置，移除活动旧handler/注册/开关。没有产品双入口；不可达通用源码非本期清理前置 |
| R02 | 高 | 把“用户无需自备授权”直接推成必须新增媒体API、身份/额度系统和PostgreSQL表，没有结合非公开本机范围 | 易界方预置其凭据，复用Host Keychain非交互读取和SeedreamClient；API/Infra/新库表/跨仓SDK退出本期。公开分发密钥边界单独保留 |
| R03 | 高 | 新建read_media_attempt及Broker结果回执前，没有充分核对原生MCP item已含执行结果 | 复用原始item/started/completed和thread/read。Host只解释冻结业务结构，结果缺失/截断为unknown，不伪称原生item直接等于业务终态 |
| R04 | 高 | 只有“内置调用时检查是否可兜底”，缺少谁继续执行、是否仍同turn的闭环 | 工具result→原生needs_follow_up/run_turn→模型调用内置；更新专家说明并增加真实同turn闭环验收。Host不造补答turn |
| R05 | 高 | 提交前专家不可用会在ExpertsEnabled/MarketProcess/PrepareMarket阻断；描述“保留绑定”不足以让请求进入Runtime | 原提交源契约区分preferred/effective/preflight并一起冻结；合法空执行选集跳过worker，保留scope/revision/checkExpertSubmission，不临时改签名选集或purpose |
| R06 | 中 | 新get_generation及generation/operation资源重复已有Artifact查询，并衍生新持久状态 | 只新增generate_image；复用get_artifact_status，把其gateway和Host资格从document环境解耦；现turn索引与imageTurns承担有限准入 |
| R07 | 高 | 未覆盖完成通知与新MCP调用竞争，且旧专家guard依赖将被关闭的HostImagesEnabled | 原始事件先观察；有界等待+一次原生快照；无锁等待，缺证据unknown；新媒体能力继续驱动双向串行准入 |
| R08 | 高 | “删Key输入弹窗”可能仍触发SecItemCopyMatching的系统认证UI，开箱可用口径不完整 | 无交互查询明确约束，缺失/锁定/需交互返回不可用；运营方完成预置与访问配置后验收，不靠用户手工供给或自动解锁 |
| R09 | 中 | 暗含新生成平台的跨重启自动恢复、固定保留期，范围超出入口迁移且可能把unknown变成重试 | 无新业务账本/保留策略；旧活跃轮不自动派单，原生链不足即unknown；新明确生成输入使用新turn |
| R10 | 高 | 不只是PrepareMarket：Manager.Start先调用StartMarketProvider，失败直接让核心Runtime不可用；只修提交路径仍无法兜底 | Host启动拆分核心和市场就绪，普通worker不可用只禁止市场执行；核心身份/模型启动错误仍失败。增加启动到主轮的完整验证 |
| R11 | 高 | 当前ImageGenerationEnabled来源于HostImagesEnabled，直接关闭旧开关可能连SeedreamClient也不创建；原生观察若绑UI订阅也会失效 | 新MCP/provider装配与旧原生开关分离；原始通知观察独立于UI/SSE开关；旧guard改由新能力控制 |

R08的外部依据：Apple说明未显式限制时查询可允许认证交互；当前推荐认证context的interactionNotAllowed。方案只冻结“零交互、失败不绕过”，具体macOS桥接需实现时按最低平台编译核验。[Apple查询交互说明](https://developer.apple.com/documentation/security/ksecuseauthenticationui?language=objc)、[Apple禁止交互建议](https://developer.apple.com/documentation/security/ksecuseauthenticationuifail)

以上“已修订”仅指文档处理，所有对应产品行为仍NOT RUN，不记为功能缺陷已修复。

## 3. 兜底闭环的最终责任划分

| 步骤 | 唯一责任 | 验收重点 |
|---|---|---|
| 接受用户选择与计算有效能力 | Native可信绑定 + Host复核 | 明确图片服务不可用时仍能接受同次合法提交 |
| 专家调用及审批 | Runtime原生MCP + 现worker | 不能让Host代模型私调专家，不放宽原审批 |
| 记录调用与传回工具结果 | Runtime原生item/工具输出 | 不重建生命周期，不把工具completed等同provider成功 |
| 业务结果解释 | Host纯适配 | 对应精确服务/方法/任务与完整schema，拒绝/unknown不兜底 |
| 决定下一工具 | 原生run_turn中的模型 | 同turn实际调用内置；不是仅口头承诺 |
| 防止重复/并行生成 | Host有限媒体准入 + 原审批守卫 | 内置前优先专家、内置reserve后禁专家新创建 |
| 图片交付与核对 | 现Artifact/Native ACK/get_artifact_status | 文档关闭也能查；失败不触发新的生成 |

pending仍是pending：沿已审阅规则查询原任务，当前未到终态不能强行fallback。跨轮明确继续查询需绑定原task/native item；无法核验是否已兜底时保持unknown。单轮失败后是否正确继续必须真实验证，不以“原生会继续采样”替代模型行为证据。

## 4. 保留的必要复杂度与未解决的交付输入

仍保留：可信选择/权限绑定、空选集合法提交、冻结结果schema、原始通知观察、一次提交锁、取消和迟到结果处理。这些来自本次用户要求和已有边界，不能以“简化”为理由仅写一句fallback提示词。

仍需要：运营方预置的易界凭据及真实供应商资格、当前冻结LinkFox字段与实际账户匹配、两种模型真实同轮闭环证据、Native UI和固定Runtime的定向协议验证。这些是未来实施/验收输入，不是文档已经证明的事实。当前计费额度0，实施未授权。

没有新增平台服务的前置依赖；公开共享Key不能分发的限制也未消失，只是不把未来公开平台提前放进本期。新方案仍满足无用户工具安装、无用户自备供应商授权的本机产品流程。

## 5. 本轮检查

修订版声明、结构、链接、原生复用/范围一致性及67源码文件未改检查见[review-checks.json](references/review-checks.json)。初稿plan-checks.json保留但不作为本版证据。产品实现/模型外调/构建/部署全部NOT RUN；ADR保持Proposed、feature保持draft。
