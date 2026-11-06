# FEAT-168 生图工具工程设计记录

设计阶段的事实、方案与当时授权保留如下。后续开发、隔离验收以及个人日常启用分别记录。[实施记录](04-implementation.md) · [本地 D4](05-local-verification.md) · [日常启用记录](06-daily-activation.md)

## 1. 整体实现方案

### 现有能力与退役对象

| 核查对象 | 代码事实 | 对 FEAT-168 的约束 |
|---|---|---|
| 已有生图 | FEAT-128 本机限定配置通过 `thread/start.dynamicTools` 注册 `generate_image`，由 Host 接收反向 `item/tool/call`，调用 MiniMax `image-01`。旧交付记录覆盖文生图及当前轮单张 PNG/JPEG 人物参考图，结果进入会话 Artifact。 | 替换旧图片执行器、固定模型、入参构造和注册条件。MiniMax-M3 仍可承担主聊。当前受支持格式的历史图片按原 Artifact 身份读取；ADR-0023 已退役的旧库不恢复。见 [FEAT-128 验收](../FEAT-128-structured-chat-artifacts/demo-fast/02-verification.md)、[工具注册 imageGenerationToolSpec](../../../../yijie-agent-host/internal/codex/session_protocol.go)、[旧图片客户端](../../../../yijie-agent-host/internal/imagegen/client.go)。 |
| 显式专家 | 易界已登记 LinkFox 专家及其 AIGC 生图工作流，专家记录能关联既有工具资源。 | 保留专家、工具及既有配置。点名要求使用、或在界面选中该专家时，使用所选专家的生图配置。仅提及品牌、同类任务描述、隐式技能匹配和通用 MCP 可见性不能触发此例外。见 [专家目录](../../../../yijie-desktop/src-tauri/src/skills/experts.rs)、[LinkFox 生图专家工作流](../../../../yijie-skills/plugins/yijie-desktop-skills/experts/linkfox-expert-aigc-imagegen-mannequin-to-model/skills/mannequin-to-model/references/tool-workflow.md)。 |
| 当前日常候选 | Desktop 的 `native-public-messages-r3` 本机候选锁定 fork `2b79447c363165ecd3b9d12dffe300c1adddbbb0`、上游 `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d`、Runtime SHA-256 `cf358a9140a5e1f7e74c02bf94d55c871c28d3f5f871dfd95fbdd0e7a327b0aa`、`experimental_api=false`；日常启动器启用 market 时显式关闭 FEAT-128。Host 拒绝 `KimiK31Candidate + DynamicToolsEnabled`。 | 将日常普通聊天作为目标入口，保留原 market、专家、权限及 stable app-server 配置。旧实验组合不能代表当前日常可用。见 [Runtime 候选锁](../../../../yijie-desktop/contracts/runtime-kimi-k31-pro.candidate.json)、[日常配置，305–321、382–386 行](../../../../yijie-desktop/scripts/run-local-demo-fast.sh)、[Host 配置，116–118 行](../../../../yijie-agent-host/internal/codex/runtime.go)。 |
| fork 原生生图 | app-server 安装 image-generation extension；它通过 `ToolContributor` 注册 `ImageGenerationTool`，以 `ToolExecutor` 接入同一调度器。工具以 call ID 产生原生开始和成功/失败终态。 | 保留原生工具选择、调度、取消、结果返给主模型及 turn 续行。见 [安装处](../../../../yijie-codex/codex-rs/app-server/src/extensions.rs)、[注册](../../../../yijie-codex/codex-rs/ext/image-generation/src/extension.rs)、[ImageGenerationTool::handle_call](../../../../yijie-codex/codex-rs/ext/image-generation/src/tool.rs)。 |

### 同一次工具调用如何出图

1. 普通聊天及有相应权限的专家聊天继续使用所选主聊模型。以现有会话/本轮有效的显式专家选择和专家配置决定执行路径：明确点名要求使用或界面选中指定生图专家时，沿用该专家已配置的生图工具及既有权限；点名与界面选择均建立可见的会话绑定，跨轮保留至移除或切换。无绑定或所选专家确实未提供生图工具时走内置；发现失败、权限不足或工具暂不可用不能解释成配置中没有该能力。两条路径在一次请求中互斥。已明确选择但无法解析身份、资源不可用或权限不足时，提示对应原因，不调用另一条路径。参考图取自当前已准入的输入，保留单图人物参考能力。看图、问图、写提示词和历史回放均不产生生图调用。计划草案、标题等 input-only 回合继续执行原生无工具策略。计划执行只有在原有授权明确涵盖该能力和外部调用时才可使用同一工具。见 [input-only 配置与核验](../../../../yijie-agent-host/internal/codex/scheduled_draft.go)。
2. Runtime 保留原生工具身份与 `ImageGenerationItem` 生命周期。现有 extension 把 OpenAI 身份检查、provider capability、namespace、图像输入能力与 feature 共同用于工具可见性，后端具体类型也直接耦合 `CodexImagesBackend`。原客户端要求 `data[].b64_json`，工具固定 `gpt-image-2`。实施时需要在这些接缝提供受管的易界后端选择。保留原 OpenAI 分支的鉴权条件，单独核验易界条件；复用原生注册与执行器，对易界后端收窄工具规格。Kimi 与 MiniMax 主聊的配置均走 Responses；对这两种模型分别证明其支持的工具形式。不得假设替换模型名或 base URL 即可生效。见 [extension 的配置和注册](../../../../yijie-codex/codex-rs/ext/image-generation/src/extension.rs)、[spec_plan，372–398、997–1013 行](../../../../yijie-codex/codex-rs/core/src/tools/spec_plan.rs)、[后端实现](../../../../yijie-codex/codex-rs/ext/image-generation/src/backend.rs)、[ImageResponse](../../../../yijie-codex/codex-rs/codex-api/src/images.rs)。
3. 易界后端拟由受管 Host 适配方舟鉴权、请求和结果交付。Runtime 与 Host 间只衔接原生调用上下文、获准输入与必要结果；Host 只为已绑定的 thread、turn、call 执行一次。现有 extension 未提供可通过配置替换成远程 Host backend 的公开接口。实施先依据固定 fork 确定最小适配面，冻结两端契约，再接入。不可将 FEAT-128 的 experimental 动态工具同时注册或另建 Host 任务循环。见 [原生 backend 的实际边界](../../../../yijie-codex/codex-rs/ext/image-generation/src/backend.rs)、[现有 Host 调用绑定与产物写入](../../../../yijie-agent-host/internal/session/provider_image.go)。
4. Host 调用方舟北京区图片生成 API。一张新图的请求提供 `model=doubao-seedream-5-0-pro-260628`、实际 `prompt`、默认 `size=1.5K`、默认 `watermark=false`；参考图场景增加必要的 `image` 输入。省略 `stream`，按普通 JSON 回包处理；其余可选参数留给 API 默认值。已有比例要求可作为提示词中的画面构图约束，不透传旧 API 的 `aspect_ratio` 或私自改成其他尺寸档。主聊模型沿用原 Responses 调度，图片请求使用 images/generations。详见 [图片生成 API](https://console.volcengine.com/ark/region:cn-beijing/docs/image-generation-api)。
5. 方舟默认以 URL 返回生成结果。受信 Host 客户端限时、限量取得图片；取图请求独立于模型鉴权，不向结果 URL 或重定向目标转发方舟 Bearer 凭据。验证来源、格式、大小和实际可解码内容后，交给已有加密 spool。对话继续展示已有图片卡片的生成中、完成或失败，预览与保存走本机 Artifact。按同一调用绑定单个 artifact ID；只有图片可读取才发布完成。主模型收到简短的结果说明。供应商临时 URL、密钥、图片字节和本机暂存路径均不得写入模型消息、公共事件或日志。原生 raw 图像返回/保存行为应在该易界后端定向适配，不能期望重开会话时由 Runtime 回放图片。见 [原生结果与暂存行为](../../../../yijie-codex/codex-rs/ext/image-generation/src/tool.rs)、[publishV3](../../../../yijie-agent-host/internal/session/artifacts.go)、[v9/v12 投影](../../../../yijie-agent-host/internal/session/artifact_media.go)。
6. 取消须传至请求和下载，迟到结果不得发布成功。网络中断且供应商是否接单不明时记录失败或不确定，禁止自动重发付费请求。重放、重开和重复通知只恢复已有结果，显式重试才形成新的请求。内置工具不可用时清楚提示用户，禁止重新调用 `image-01`，也禁止经脚本、隐式技能或未明确选择的专家工具绕开。密钥仅在实际配置阶段通过受保护的输入弹窗提供。

### 固定 fork 与 Host 的适配接缝

| 接缝 | 首选设计及资格条件 |
|---|---|
| 工具名称与分发 | 优先核验两种主聊对原生 `image_gen.imagegen` namespace 的真实调用。若其中一种仅支持普通 function，则按该 profile 同时选择相匹配的 `ToolName` 和 `ToolSpec`，复用同一 executor。`ToolRouter` 用返回的 namespace/name 构造键，`ToolRegistry` 按全名精确查询；只改对外 JSON 名会找不到 handler。现有图像可见性检查也按原始 namespaced 名识别，故易界准入应作用于该 executor 的注册和实际执行，覆盖普通 direct 与已启用的 code mode 嵌套入口；不得靠平名绕过检查。每次只登记一种模型可见规格。见 [router.rs · build_tool_call](../../../../yijie-codex/codex-rs/core/src/tools/router.rs)、[registry.rs · tool](../../../../yijie-codex/codex-rs/core/src/tools/registry.rs)、[spec_plan.rs · add_extension_tools 所在模块](../../../../yijie-codex/codex-rs/core/src/tools/spec_plan.rs)。 |
| 当轮参考图 | 上游工具可在调用后端前读取最多五个本地绝对路径，或搜索历史消息中的最近图片；上游说明也会诱导模型使用这两种参数。易界后端的模型可见说明和解析器仅描述 prompt 及是否使用当前轮单图。在读取文件、历史或进入 Ark 客户端前拒绝路径、URL、base64 与跨轮图片参数。Host 复用 `imageReferences/beginImageTurn/bindImageTurn`，从已绑定、已准入的本轮附件解析那张图片；模型不能自报身份或提交任意素材。见 [原生参数与引用分支，83–91、259–307 行](../../../../yijie-codex/codex-rs/ext/image-generation/src/tool.rs)、[原生工具说明](../../../../yijie-codex/codex-rs/ext/image-generation/imagegen_description.md)、[受管附件](../../../../yijie-agent-host/internal/session/provider_image.go)。 |
| 受管 backend | 首选评估在原生图像 executor 与 Host 之间复用 app-server 已有双向 stdio、请求关联和返回通路，由调用上下文绑定 thread/turn/call，Host 只执行单一方舟操作并返回短结果。现有 `ToolCall` 有 turn ID、call ID、emitter，线程级 extension 可取得 thread ID；接口没有通用 Host RPC handle。`item/tool/call` 的现成生产者只接受 `DynamicToolCall` 原生 item，Host 也按旧实验开关及确切工具名准入。须先证明能在 stable 受管 profile 中复用已有请求**语义**、取消与调用身份；不能伪装成动态工具、制造第二个模型调用项或更改既有消费者的解释。如果现有语义无法承载，备选仅为在同一 stdio transport 上提出最小、可审计、显式能力协商的图像后端请求/回复；由 fork 先形成候选。未证明授权、取消、版本相容或来源绑定即停在设计评审。既有 `publish_artifact` 用于登记已存在于工作区中的文件，不可拿它充当付费生图代理。见 [ToolCall](../../../../yijie-codex/codex-rs/tools/src/tool_call.rs)、[app-server 反向请求，951–976 行](../../../../yijie-codex/codex-rs/app-server/src/bespoke_event_handling.rs)、[Host 接收边界，330–362 行](../../../../yijie-agent-host/internal/codex/session_protocol.go)、[已有媒体发布](../../../../yijie-agent-host/internal/session/artifact_media.go)。 |
| 已选专家工具优先与 LinkFox 的执行准入 | 界面选择或明确点名使用应先解析成现有专家 ID、版本与资源绑定，经本次 `TurnExpertSnapshot` 固定，绑定至 turn operation。持续绑定的每一轮均使用受信快照，按所选专家的确切版本和配置选路；无绑定或专家确无生图能力时才走内置。已点名但成功冻结前身份不明时停止。对发起有费用的生图调用，在内置 backend 和 LinkFox 实际调用准入处均复核同一快照：所选专家的同领域工具优先。当前已核实的 LinkFox 人台换模特图专家使用自己的已配置工具；该规则依据绑定及资源配置，不按品牌名授予特权。普通/隐式匹配不能走这个外部创建入口。对于通用 `proxy_call`，须以已发现 schema 核验内部业务方法，覆盖 `aigc/imageGenAsync`，只看外层工具名或提示词不能实现互斥。原有专家租约、鉴权与审批继续生效。既有任务的只读查询按原 taskId 和原授权办理，其他连接器与非生图操作沿用各自准入。见 [专家快照与申请](../../../../yijie-agent-host/internal/session/experts.go)、[market 操作绑定](../../../../yijie-agent-host/internal/session/market_submit.go)、[worker · register_call / consume_call](../../../../yijie-connectors/worker/src/broker.rs)、[LinkFox 真实方法与查询规则](../../../../yijie-skills/plugins/yijie-desktop-skills/experts/linkfox-expert-aigc-imagegen-mannequin-to-model/skills/mannequin-to-model/references/tool-workflow.md)。 |
| 结果、重开与重试 | 原生 `ImageGenerationItem.result` 为必填字符串，上游 `GeneratedImageOutput` 的直接调用和 code mode 均返回 base64，保存路径与 legacy end 还可携带图像数据。易界分支须同时处理 item/result、legacy end、两种 tool output 和 save root；主模型只获安全结果，Artifact 是交付的权威，不能把临时 URL 塞入原生 result。用现有 Host spool 和 Desktop 校验、持久提交、ACK、重开读取；原生工具活动与 Artifact 关联为同一次执行，仅产生一个结果卡。Host 以受信的用户提交/turn 操作与 call ID 核验唯一调用，核对重复通知、产生不同 call ID 的同轮第二次提交、取消与晚到结果。旧 `turn.called` 是进程内保护，不能作为崩溃后可重发的证明。接单未知则保持未知或失败，重连与重开不再派单。显式新请求重试时单独核算费用，不能承诺供应商取消已受理工作。见 [ImageGenerationItem](../../../../yijie-codex/codex-rs/ext/items/src/image_generation.rs)、[原生直接/嵌套输出，492–540 行](../../../../yijie-codex/codex-rs/ext/image-generation/src/tool.rs)、[Runtime 原生取消](../../../../yijie-codex/codex-rs/core/src/tools/parallel.rs)、[Desktop Artifact 提交与 ACK](../../../../yijie-desktop/src-tauri/src/chat/artifact.rs)。 |

### 实施顺序与兼容检查

先在固定 fork 重读原生 extension、模型工具规格与历史读写行为，形成最小、可重放的候选 patch 和 canonical schema/行为差异；原样上游子树按 fork 规则保留。随后由 Contracts 固定候选 commit、schema digest 和 Host 所消费的投影，再由 Host 接入方舟、Desktop 复用 Artifact 交互。Runtime 通知以固定 fork 的 schema/实现为权威，Host 公共事件与跨进程兼容投影以 Contracts 为权威，Ark 请求/响应以型号对应的官方文档为权威；分别检验形状和语义变化。凡须新增请求、改结果语义或修改消费者资格，先列出旧版本的拒绝或受限行为，按候选→不可变投影→消费者的顺序交付，不能将源码树中“已有该类型”视为日常已获准。两种主聊模型分别验证工具可见性、一次分发、结果返回和同轮收尾，普通/专家、旧会话 resume、受限草案与计划单独核验；通过同版本组合与历史 reader 检查后才具备切换条件。旧 profile 与新 profile 的并存版本必须保证每个请求只进入所选的一条执行路径，旧 `image-01` 不得执行。暂停新功能只影响新任务，保留历史读路径，禁止把旧图标为 Seedream 所出。本需求按最高影响判为 breaking：旧实验入口执行 `image-01` 的有效交互将退役，即使历史图片的 schema 可原样读取。迁移时先准备可读新旧数据的消费者，再启用新的生产者。见 [Contract First](../../dev/contract-first.md)。

## 2. 实际改动

本阶段交付为需求及设计记录。首次起草前的源码基线为元仓 `5415b22`，Host 为 `25117cd`，Contracts 为 `af6245a`，Desktop 为 `ca98af3`，Skills 为 `704d2cc`，Connectors 为 `2cac465`。首次起草前各仓干净；本次复审前元仓已有 FEAT-168 四份未跟踪草案，完整快照见[复审证据](references/requirements-audit.json)。此处记录源码基线，实际部署制品与消费者版本须在实施阶段另行核实。

## 3. 调试循环

本阶段无运行记录。后续区分模型是否看见工具、原生调用是否进入后端、方舟是否接单、产物是否可读取，以及同一 Artifact 是否已发布，按出现问题的首个接缝诊断。

## 4. 外部授权与实际调用

FEAT-168 当前生图调用数为 0。FEAT-128 的五次旧模型验证已结清；新模型真实调用的额度和配置在实施阶段另记。

## 5. 已知限制

本次判断依据固定源码、候选锁与历史验收材料，未读取个人凭据，也未检查运行中的日常进程。原生后端接缝、方舟账户对精确模型与尺寸的准入、真实返回图片与新旧读写兼容均待后续验证。
