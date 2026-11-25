# FEAT-176 · 验收方案与验证状态

2026-11-25 修订 3，交付物是需求、工程方案与现有共享链的审计结果。以下是实施后的判定条件，当前 10 项产品验收均为 **NOT RUN**。测试样本使用升级后创建的普通会话、计划和授权。

## 可执行的验收矩阵

| 编号 | 场景与动作 | 通过条件与证据 |
| --- | --- | --- |
| AC-001 | 冷启动后用同一构建读取 Host `/v2/model-chat/catalog` 和原生 `model/list`，新建聊天不改选发送。另开草稿，手选 M3 后刷新、发送，再打开一份全新草稿。 | Host 的 4 个活动 profile 中 Flash 仅有一项且是默认值。原生的 3 个受管模型中，Flash 唯一 `isDefault=true` 且 `defaultReasoningEffort=xhigh`。首条 Native 提交为 Flash，手选轮为 M3/high，再新建回到 Flash。菜单可键盘操作。目录零项按格式错误处理，合法四项均不可用时禁发并提示原因。 |
| AC-002 | 在基础服务就绪、仅配置 MiniMax 测试 Key、没有已运行的 Kimi 网页执行器的环境，分别走 `pnpm client:dev` 和「易界.app」正常启动。用同一把测试 Key 执行 Flash/M3，再正常轮换和重开。另测网页服务已配置及 MiniMax 未配置。 | 仅配 MiniMax 即可启用默认聊天，普通 Flash 原生搜索可用，Kimi 专属工具明确不可用。网页服务已配置时按原资格启用。两模型在每次启动均通过同一受管凭据鉴权，只记相等性。缺 MiniMax Key 时无模型请求。有因果证据时才区分账户不具备 Flash 资格、无效凭据、额度或暂时性失败。 |
| AC-003 | 从普通发送和带权限模式的发送入口，在本地捕获首轮、追问及一次函数结果后的真实 Runtime 请求，再与经授权的供应商样本对照。 | 对每次默认 Flash 调用，选中元组、线程回执与真正出站的 `POST /v1/responses` 一致，body 有 `model=MiniMax-M3.1-Flash`、`reasoning.effort=xhigh`、`stream=true`，省略 `service_tier`。记录实际 host/path 及供应商返回的模型身份。无出站证据时不能用 UI 或 `/readyz` 判定参数正确。 |
| AC-004 | 在本版同一空闲会话做 Flash → M3 → Flash，配有 Kimi 的环境另测手选 Kimi。在活动回合或待审批时尝试正常切换。用两次正常选择读取的真实元组验证 Native 回执匹配。 | 创建、读取、恢复均接受 Flash/minimax。选择 Flash 时将 M3/minimax 元组交给本地解码器应判为不匹配。一次成功切换只增加一次 revision，thread 身份和本轮徽标正确。忙态锁定，重复读取同一操作回执产生零次新增推理。 |
| AC-005 | 发送文本、小图片及受支持的文件。观察流式推理、正文和窗口用量，正常停止后重新发送。用普通本地回环运行原生压缩，并用输出限额的正常未完成样例检验终态。 | 1,000,000 作为目录规格。同轮原生样本提供的有效容量才进入窗口条，若沿用 95% 配置则为 950,000，缺样本时显示未知。Flash 压缩请求仍使用 xhigh。`incomplete` 只有推理时保留未完成状态，停止后可再次发送。 压缩提示四态、聊天框当前/上次样本及只读交互须通过下方对照。 |
| AC-006 | 普通聊天用一个只读函数、显式技能和未覆盖模型的原生子代理。用正常本地样本观察 Auto 审核，核查 `yijie_media`、文档等已启用工具的清单与权限。 | 记录函数参数、`call_id`、结果和最终回答。继承 Flash 的子代理请求为 Flash/xhigh。Guardian 选用 Flash 时也为 xhigh，单独记其 HTTP 尝试。无法解析的审核结果不放行工具。文档和专用媒体后端按各自凭据装配。 同类调用通过同一阅读索引和组件，对照单项身份、组边界、摘要计数、工具详情与展开状态。 |
| AC-007 | 在仅 MiniMax 与独立 Kimi 网页服务就绪两种配置下分别检查普通、允许网页和受限专家。核对一次获准的 Flash hosted 搜索，并用两个本地正常搜索项验证各自来源、标题缺失及连接器绑定。 | 普通 Flash 的 hosted `web_search` 可独立工作，Kimi Pro/Basic/Fetch 仅在相应服务可用时暴露。实际搜索项 ID 对上其网址，缺标题保留网址，缺来源记录如实显示。区分供应商实测与样本展示。受限专家、标题和 input-only 草案在两种配置下均遵守禁搜策略。 对照原生搜索卡及已有 MCP 卡各自的语义、空态、标题回填和点开来源的行为。 |
| AC-008 | 同一构建分别生成 Flash 短标题与计划草案，记录实际 `text.format` 和严格解码结果。再用 M3 起草新独立计划，打开表单审阅执行模型。覆盖 `new_chat_each_run`、`dedicated_chat`、`existing_chat` 以及手动和自动派发。 | 有效标题和草案均在隔离用途生成。无效标题保留当前可读标题和主回答，无效或需澄清的草案不会入计划或签发授权。M3 起草的独立计划仍默认以 Flash 执行，可手动改选。已绑定目标按该聊天的选择执行，快照缺失或不一致时停在审阅步骤。 |
| AC-009 | 通过正常 Native 打开新测试库，在本版写入会话选择、已受理轮次、计划、切换回执和投递证明。正常退出、同版重开。对同一候选分别读 `/readyz`、`/v1/status`、会话回执，另在暂停 Kimi 配置下检查 Flash outbox 能派发。用本地配置样本核对前端、Native、Host 的模型开关。 | 正常打开与重开均读到 `PRAGMA user_version=52`，五类写入可读取，派发 SQL 包含 Flash。`/readyz` 反映 Runtime 就绪，`/v1/status` 响应的 `runtime.model` 反映启动默认。实际创建、读取和恢复的 `session.model` / `model_provider` 分别与本次所选元组相符。活动开关不一致时在新请求派发前报告配置错误。读取状态不触发推理。 重开本版测试会话，原始 Item、来源和分组与同样处于重开状态的基准模型一致。 |
| AC-010 | 从真实易界首页直接发送一条普通问题。按授权观察供应商响应与主回答终态，再用正常取消和配置恢复验证反馈边界。 | 记录按用途区分的实际请求数、可取得的输入/缓存/输出/推理 token 和脱敏响应标识。本地选择、受理回执和供应商完成分别取证。本地受理前可继续编辑。受理后失败保留该轮问题和原因。状态刷新、取消及页面重开不补发，用户显式再次发送才创建新操作。 真实 Flash 会话需保留实际供应商返回、原生事件与界面的对应证据，同时通过下方同事件对照。 |

## 同类事件的对照验收

**比较单位是相同的事件事实。** 同一构建、权限、工具配置和能力协商下，分别从正常入口选择 M3 和默认 Flash，新建独立 thread。M3 是同供应商主对照，另用已支持的 Kimi K3.1 Pro 正常样本回归相同事件，以覆盖跨供应商共用路径。用普通本地 Responses 样本驱动真实 app-server，首先核对两边实际请求为 M3/high 和 Flash/xhigh，再比 Host 通知/只读快照、Native 视图及最终组件。评审还应沿两条路径定位到同一套投影、分组与控件源码。取得真实 Flash 样本后，分别保留两种模型实际的字段和分片差异作脱敏输入，从供应商解码处重放。同一份已归一化 Item 的比较只证明后半段展示。以每次运行自身的 thread、turn、item、call 或 operation 身份建立一一对应，核对归属、顺序、动作、状态和真实字段。模型徽标、ID 字面值、实际时间和各自实测 Token 可不同。同一模型的重复通知不能凭此得到第二个阅读行。

| 对照场景 | 可判定的预期结果 | 对应验收 |
| --- | --- | --- |
| 两个原生搜索项与一个 MCP 检索结果 | 相同查询但 ID 不同的搜索各保留一项。每项来源顺序和网址/标题归属正确，迟到标题更新原卡，只有网址或无来源时使用既有文案。核对 `openPage`/`findInPage` 及 MCP 搜索/读取各用相应卡片。打开指定链接走原有用户操作，展开、滚动、收起不额外发起检索或模型调用。 | AC-007、AC-010 |
| 命令和其他工具生命周期 | 取一条含两个动作的命令、一条 MCP、文件变更、查看图片和子代理的正常记录，按相同输入对比标题、详情、输出摘要、动作与调用的归属。对照运行中、成功、失败/拒绝、部分信息和待审批的既有可见性。用户批准或拒绝仍由原审批链处理，阅读控件不能执行工具。 | AC-006、AC-010 |
| 连续活动与消息边界 | 32 个搜索、32 条普通推理、8 条命令应保留 72 个原始 Item，界面为 1 组、40 次调用。插入一条新的可见阶段说明后两侧成为 2 组。一个含两动作的命令仍计 1 次调用。核对实时组标题、并行项、首次出现正式回答时只自动合拢一次、手动重开后的选择和滚动位置。此项使用本地样本。 | AC-006、AC-010 |
| 同一压缩项的进行、完成、中断及未知 | 按各自真实生命周期分别输入四种状态。`context_update` 始终位于匹配的原 Item 位置，更新同一 `role=status` 行。同轮新的工具在它之后另起活动组。其它 thread、turn 或 item 的通知不能生成此行。缺少压缩完成事实、中断或读失败时不得渲染为已完成。 | AC-005、AC-010 |
| 切换模型时的聊天框上下文 | 用 `used_tokens=190000`、`capacity_tokens=950000` 的同一实测形状样本核对 20% 已用、80% 剩余及相应 Token 数。另测真实零、分母未知、无样本。M3 切到 Flash 且未收到新样本时，只能用带上次测量模型归属的样本。Flash 首次有效样本替换它。确认换聊天、窗口失效和迟到读结果不串值。悬停、焦点、Esc 和无障碍名称均沿用当前控件，打开浮层不产生模型请求。同草稿手选模型时核对已有工作区、附件和技能依旧绑定到原草稿。 | AC-004、AC-005 |
| 普通/专家的公开消息、审批、终态及本版重开 | 对照用户输入、公开说明、正文预览与正式 Item、思考详情、计划和需用户处理的状态。原生重试只显示已观察到的意图。成功、正常取消与失败分别取证。工具结束不会代替轮次终态，预览与正式答复只显示一份。结束后重开本次新会话，过程依原规则收起、可读结果保留且不补发。 | AC-005、AC-006、AC-009、AC-010 |

发布前留存同一场景两条路径的脱敏请求身份、原生事件与 Native 视图摘要、UI 的分组/计数或上下文行及交互结果。再用获准的真实 Flash 普通任务把至少一次可辨识的搜索或只读工具活动、最终回答与实际界面对应起来。若只有正常文字回答，证据只覆盖文字。新特性或字段不兼容须记录真实协议差异、适配位置、缺字段时的呈现及对照结果。已有组件基线通过不能抵消 Flash 接入侧的差异。

## 实施后的验证顺序

1. **契约和生成物。** 使用 Contracts 的安全生成与一致性入口，在当前活动的 chat models、model-call surfaces、scheduled-plan、experts、market 和上下文用例中增加 Flash 正例、4 项唯一性和默认值断言。校验 Node、Go、Rust 与 Tauri/Vue 读取同一份定义。就地契约变更记录预期的默认和枚举差异。[Contracts 命令](../../../../yijie-contracts/package.json) · [目录测试](../../../../yijie-contracts/tests/chat-models-v2.test.mjs) · [计划测试](../../../../yijie-contracts/tests/scheduled-plan-v2.test.mjs)
2. **零费用请求验证。** 使用真实 app-server 和只记录必要请求字段的本地 Responses 服务。在本版正常样本中补 Flash 精确 ID、嵌套 xhigh 和共享测试凭据。`feat164-local-responses.py` 只认识 Kimi/M3，`market-local-protocol.py` 仅把 M3 走 MiniMax 直接工具分支，均不能原样证明 Flash。验证经 `kimiK31MeterArguments` 设置的进程级及线程级 loopback，使子代理、Guardian、compact 和工具续答也进入同一观察范围。[本地 Responses 样本](../../../../yijie-agent-host/scripts/feat164-local-responses.py) · [市场本地样本](../../../../yijie-desktop/scripts/market-local-protocol.py) · [进程级配置](../../../../yijie-agent-host/internal/codex/feat164_meter.go) · [既有原生集成测试](../../../../yijie-agent-host/internal/codex/kimi_k31_integration_test.go)
3. **本版 UI 与持久化。** 使用日常客户端相同的 Tauri、Host、Runtime 装配及本版测试数据。记录启动清单、目录、同一 thread 中的切换和回执，核对正常退出后的新记录。检查输入框在最小窗口能区分 M3 与 Flash、键盘可选择和退出菜单，加载或失败时草稿仍可编辑。 [菜单](../../../../yijie-desktop/src/components/chat/ChatModelControl.vue) · [计划表单](../../../../yijie-desktop/src/components/schedules/ScheduledPlanForm.vue) · [轮次身份读取](../../../../yijie-desktop/src-tauri/schemas/chat-turn-model-v1.schema.json)
4. **真实供应商。** 使用获批的 FEAT-176 调用次数和费用上限，区分主回答、标题、草案、子代理、原生审核、压缩及工具续答的模型 HTTP 尝试，并另记同一响应内 hosted search 的实际次数。普通 Flash 首轮、共享凭据下的 M3 对照、Flash 工具续答、实际来源字段及辅助结构化输出是待取证点，可用同一正常场景覆盖多点。证据仅含候选版本、模型名、effort、目标域名/路径、脱敏响应标识、终态、计数与用量。真实来源字段不足时标明观察结果，不借用 M3 的实测结论。 [MiniMax Responses](https://platform.minimax.cn/docs/api-reference/responses-create) · [服务端工具](https://platform.minimax.cn/docs/guides/server-tools)

## 共享链基线

2026-11-25 在修订 3 的源码基线上执行以下检查。

| 已执行的检查 | 实际结果与覆盖边界 |
| --- | --- |
| Desktop 定向 Vitest | 15 个文件，172 项通过，1 项条件跳过。覆盖时间线、原生流式消息、工具行、搜索来源、连续活动、压缩提示、上下文环及同版重开。跳过的是 `ChatDeepSearchReceipt` 的杭州历史录制回放，运行环境未指定 `SCOPED_REPLAY_DIRECTORY`。该批录制的对照没有重验。 [分组基准](../../../../yijie-desktop/src/domain/conversation-activity-presentation.test.ts) · [渲染验收](../../../../yijie-desktop/src/components/chat/ChatTraceV2Acceptance.test.ts) · [压缩行](../../../../yijie-desktop/src/domain/context-window-timeline.test.ts) · [上下文控件](../../../../yijie-desktop/src/components/chat/ChatContextWindow.test.ts) · [条件回放](../../../../yijie-desktop/src/components/chat/ChatDeepSearchReceipt.test.ts) |
| Host 定向 Go 测试 | 8 项通过。覆盖最近一次原生用量与有效容量、零值与未知、切换后迟到重放、压缩生命周期及来源标题的逐项归属和帧边界。 [上下文观察用例](../../../../yijie-agent-host/internal/session/context_window_test.go) · [搜索标题用例](../../../../yijie-agent-host/internal/session/native_search_titles_test.go) |
| 共享阅读层的组合样本 | 直接调用 `composeConversationView`、`selectConversationTimeline`、`withContextWindowTimeline`、`conversationActivityPresentation` 和 `contextWindowPresentation`。两套独立会话身份及上下文 profile 使用同类正常样本。公开说明 → 搜索 → 普通推理 → MCP → 压缩 → 两动作命令 → 正文，在四种压缩状态下均得 2 个活动组、3 次调用、4 个工具/动作行，原搜索来源保持，跨线程压缩不匹配，示例用量为 20%。这是已经归一化的阅读层输入，未经过 Flash 供应商解码或真实客户端。 |

可在 Desktop 仓复跑同一组正常用例。下列文件展开语法适用于项目使用的 Bash 或 zsh。

```bash
pnpm exec vitest run --maxWorkers=4 \
  src/domain/{conversation-activity-presentation,context-window-timeline,context-window,web-search-presentation}.test.ts \
  src/composables/useContextWindow.test.ts \
  src/components/chat/{ChatActivityGroup,ChatTraceV2Acceptance,ChatContextWindow,ChatWebSearchItem,ChatDeepSearchReceipt,ChatNativeToolItem,ChatNativeCommand,ChatNativeStreaming,ChatPublicProgress,ChatTurnOutput}.test.ts
```

上述结果给出了现有产品的对照基准。Flash 真实协议适配、两模型完整接入路径及真实 WebView 对照仍为 **NOT RUN**。

## 修订 2 的契约与操作表实测（2026-11-24）

| 检查 | 2026-11-24 实际观察 | 对实施的影响 |
| --- | --- | --- |
| 严格校验现行 v2 契约 | 使用契约仓同配置的 Ajv 2020 和普通输入。现行 M3 定义、三项目录通过。拟定 Flash 六元组被 `const`、`oneOf`、`enum` 拒绝，四项目录还触发 `maxItems`。 | 需同时更新精确元组、活动枚举、目录条数与默认断言。 [契约用例](../../../../yijie-contracts/tests/chat-models-v2.test.mjs) |
| 现行操作表写入 | 取 `0049` 的操作表 DDL，在 SQLite 内存库中启用外键并创建一条普通测试会话。M3/high 写入成功，Flash/xhigh 被 profile CHECK 拒绝。 | 只验证了这一张表的现行约束。新版五张表、真实 SQLCipher 的打开及激活仍按 AC-009 验收。 [DDL](../../../../yijie-desktop/src-tauri/migrations/chat/0049_kimi_k31_high_effort.sql) |

## 本轮验证边界

| 项目 | 当前结果 | 原因与影响 |
| --- | --- | --- |
| 官方资料与源码 | 已核对 | 已确认模型 ID、effort 语义、请求字段、已有 M3 凭据入口和需改的模型判断。 |
| 产品实现、Runtime 构建、应用或数据库升级 | 未执行 | 本轮交付需求方案。新版可启动、可写入和可用状态留给实施验证。 |
| 供应商模型、真实搜索、媒体生成 | 0 次 | 本轮只读取公开文档。现有账户在实际端点上的 Flash 资格、输出品质、用量和费用尚无实测。 |
| 破坏性及攻击注入验证 | 未执行 | 遵守用户长期条款。替代方式为正常退出、显式取消、普通本地响应、未配置的测试配置和新样本。异常致损与对抗场景不作通过结论。 |

**修订 3 文档核验（2026-11-25）**　严格需求包校验、状态声明审计、元仓 lint 和 57 项元仓测试通过。另已核对 10 条 Must AC 在需求、登记和验收文件中的对应关系、当前原生契约全部 11 种 Item、4 种压缩状态、共享入口及本地引用。产品实施和 D4 仍待进行。

**修订 2 需求包自检（2026-11-24）**　元仓 `check-feature-package.sh --strict`、`validate-feature-package.mjs --audit-claims` 和 `pnpm lint` 通过。`pnpm test` 的 57 项元仓测试全部通过，7 个元仓 Shell 脚本语法通过。已逐项对照三份材料中的 10 个 AC 编号、两个默认 profile、共享凭据引用和请求示例，并检查文档内相对链接。D0 评审与 D4 产品验收均待后续进行。
