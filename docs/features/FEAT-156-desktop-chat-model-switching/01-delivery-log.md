# FEAT-156 — 工程事实、候选方案与需求编制记录

2026-10-02，Asia/Shanghai。**仅调查与文档**；以下实现顺序是未来方案。本次不改产品、契约源、启动配置、数据库、密钥或二进制，不启动/停止服务，不调用模型。没有 D0/实施/提交/推送批准。

## 1. 已加载治理与权威

已读取元仓 `AGENTS.md`、`repos.yaml`、`docs/dev/codex-project-memory.md`、Feature Delivery Handbook 的 demo_fast 路径与证据原则、QUALITY_GATES、模板与 validator；读取 `docs/dev/contract-first.md`、ADR-0017/0018、`docs/architecture/003-agent-runtime.md`、`docs/security/secret-management.md`，以及 FEAT-132/134/135/144/152/155 当前边界。Desktop/Host/Contracts/Runtime 各自 AGENTS 与相关 README、原生对话和设计文档已只读核对。

UI 基准为 Desktop `docs/design/docs/design/05-patterns/02-chat-workspace.md` 与活跃实现。部分 README/AGENTS 的“早期占位”、旧 Baseline/FEAT-137 描述已经落后于源码；此处依当前 native、FEAT-137永久退役与 FEAT-155 input-only 事实规划，不复活旧 reducer/历史重建或审批平台。

### 工作区基线

全部 origin 与 `repos.yaml` 的 `https://github.com/36Dge/<仓库>.git` 一致；当前工作分支均为 `chore/retirement-baseline-20260905`，不是 manifest 的默认集成分支；本轮不切分支。

| 仓库 | 完整 HEAD | 调查前状态 | 本需求影响 |
|---|---|---|---|
| yijie | ca0dc335f8901d16c1514dfbb09efb2538c3475f | clean | 本轮仅新增此需求目录 |
| yijie-desktop | a1357969c5f60e3aa0b301bd8b105adb7b97d55b | 16 tracked modified、4 untracked，见下表 | 未来 UI、private IPC、模型快照/outbox、reader、启动装配 |
| yijie-agent-host | 24d1bcc4291464887908aa5ee0f789b40989b77d | clean | 未来受管模型目录、secret、路由、原生切换与 durable 快照 |
| yijie-contracts | 54be9314dce5319b049dc0a236800fd1a1fdd7a1 | clean | 后续源契约、兼容投影、版本与 conformance |
| yijie-codex | fb79b1d53501ec90084b584af5fdbe221c7a25aa | clean | 固定原生能力核验；首选不改 Runtime 源码/产物 |

已存在的 Desktop 改动全部保留，本轮未修改其文件。源码引用若位于这些文件，代表**调查时工作树**而非纯 HEAD；未来实施须重新检查状态与差异，不能用本表作为干净构建凭证。

```text
 M docs/chat-native-conversation.md
 M docs/design/docs/design/02-tokens/06-motion-zindex-opacity-tokens.md
 M docs/design/docs/design/03-ui-system/02-iconography.md
 M docs/design/docs/design/05-patterns/02-chat-workspace.md
 M src/components/chat/ChatComposer.vue
 M src/components/chat/ChatNativeStreaming.test.ts
 M src/components/chat/ChatSafeContent.vue
 M src/components/chat/ChatTimelineItemShell.test.ts
 M src/components/chat/ChatTimelineItemShell.vue
 M src/components/chat/ChatTurnGroup.test.ts
 M src/components/chat/ChatTurnGroup.vue
 M src/composables/useChatTurnTiming.test.ts
 M src/composables/useChatTurnTiming.ts
 M src/domain/chat-turn-timing.ts
 M src/icons/registry.ts
 M src/styles/variables.css
?? src/components/chat/ChatStreamText.test.ts
?? src/components/chat/ChatStreamText.vue
?? src/components/chat/ChatThinkingIndicator.test.ts
?? src/components/chat/ChatThinkingIndicator.vue
```

API/Admin/Connectors/Knowledge/Skills/Infra/Coze 不计划新增业务改动；模型 Provider 由 Runtime/Host 的已有边界承接，不因其也是外部服务而移交到电商 Connectors。若调查出现实际 consumer，再扩展影响清单，不预先改无关仓库。

## 2. 已核实的工程事实

下列路径以兄弟仓为根，行号用于定位 2026-10-02 快照；未来代码变动后以符号与版本重新定位。

| ID | 路径/符号与事实 | 对需求的影响 |
|---|---|---|
| F01 | Desktop `src/components/chat/ChatComposer.vue:18,388,417`：无模型 props，`modelValue` 是文字；尾部仅发送/停止，无麦克风 | 新增独立模型状态，不混用 v-model；保留停止槽 |
| F02 | Desktop `src/pages/chat/ChatPage.vue:457,724,944`：新任务、普通续聊、textOnly计划草案共用 Composer，三条 submit 不带模型 | 三入口一致覆盖，组件不直接调 Provider |
| F03 | Desktop `src/stores/chat.store.ts:535,3678,3799`：submissionKey 是 kind/target/input/blocks；已有 target epoch、durable acceptance | 模型加入新请求身份，旧请求原 digest 保留，防异步串台 |
| F04 | Desktop `src/api/chat-client.ts:574–610`、`src-tauri/src/chat/ipc.rs:2477,2486,2551,2566`：v1/v2 payload 无模型，Rust deny_unknown_fields | 要有版本/能力协商，不能盲加字段 |
| F05 | Desktop `src-tauri/src/chat/database.rs:234,244,347` 和 `application.rs:1214,1710,1925,2153`：outbox dispatch 无模型快照，普通/草案/permission turn共用发送框架 | 冻结快照进同一事务，不新增出站系统 |
| F06 | Desktop `src-tauri/src/chat/host_bridge.rs:1587`：仅 MiniMax-M3/minimax 通过；`host_domain.rs:449–477`只存 model_ready | 必须保留精确 effective model/provider，不能仅放宽 bool |
| F07 | Desktop `host_bridge.rs:2933,2978`：现有测试明确禁止请求含 model/effort；`src/domain/chat-composer-draft.ts:1–42`仅内存草稿 | 修改权威契约及测试预期，不绕过旧测试 |
| F08 | Desktop `src-tauri/src/chat/migrations.rs:166–186`：catalog 已到27（projectless），普通常量仍15；FEAT-155日常扩展启用由launcher控制 | 不能照旧memory预定schema28或只认15/26；执行前核实所选入口实际schema，不读/降级日常库试错 |
| F09 | Desktop `scripts/run-local-demo-fast.sh:22,140,302`、`src-tauri/src/chat/sidecar.rs:30,184,256,363`：MiniMax固定key-file/provider，native reasoning启用也有provider条件 | 新默认必须落到 canonical 装配，独立两个secret引用；不能只改 Vue |
| F10 | Host `internal/codex/provider.go:17–20,244–276,389–423`：MiniMax、Responses、none/high目录；`internal/app/app.go:98–125`只接受minimax；`runtime.go:489`精确核验目录 | 受管两模型profile；Kimi默认max、能力/窗口独立，继续来源校验 |
| F11 | Host `internal/session/service.go:368,430`模型强校验；`multimodal.go:130–138,193–200`只认none/high且native覆盖high；`session_protocol.go:744–748`同样限制 | 这些是当前限制，Runtime支持max不等于Host已接通 |
| F12 | Runtime `codex-rs/protocol/src/openai_models.rs:40–64`有Max/Ultra/Custom；canonical `TurnStartParams.json:183`为非空字符串；`core/src/client.rs:802–819`需 supports_reasoning_summaries 才构造 reasoning | 直接传max可行；目录未正确配置会漏参数，须验证实际请求 |
| F13 | Runtime `codex-rs/core/src/session/turn_context.rs:215–246`：with_model对不支持effort会选择其它档；`model-provider-info/src/lib.rs:57–81`仅Responses，拒绝chat | Kimi支持档包含max，禁止静默降档；无需新增协议桥 |
| F14 | Runtime `app-server-protocol/src/protocol/v2/turn.rs:119–133`：turn/start有model/effort无provider；`thread.rs:346–380`：resume可覆写model/provider/config | 单改turn.model不能换供应商 |
| F15 | Runtime `app-server/src/request_processors/thread_processor.rs:147–227,3067–3123`：loaded线程有订阅/运行时忽略override；仅无订阅且Idle等条件下正常shutdown后冷恢复 | 同会话切换需要串行原生生命周期核验；超时不伪成功 |
| F16 | 同文件`:835–860`支持unsubscribe；Contracts `compatibility/agent-host-native-mcp-v2.json:16`及Host `internal/codex/title.go:169–173`已用于标题清理；普通native投影尚无该用途 | 可复用原生方法，但模型切换投影/验证须独立补齐 |
| F17 | Host `internal/session/store.go:70–112`有session model/provider无每轮模型；`multimodal.go:243–264`旧digest含effort/blocks无provider/model | 版本化模型快照；不能重算已接受旧操作digest |
| F18 | Host `internal/app/app.go:2070–2106`owner-only文件或env二选一；`runtime.go:975–1010`子进程显式注入；`sorftime.go:70–73,293–297`排除秘密并核验配置 | 扩展Kimi scrub、仅Runtime注入、工具子进程排除，禁止简单全局export |
| F19 | Host `internal/codex/title.go:130,152`独立标题thread固定MiniMax；`scheduled_draft.go:94–115,164`草案固定MiniMax；Desktop `host_bridge/scheduled_draft.rs:66,98,123`独立API | 辅助请求、受限草案必须显式选型，不漏费控与能力 |
| F20 | Desktop `src-tauri/src/chat/schedules/execution.rs:434`有snapshot/digest/grant；Host `runtime.go:145–146`图像工具注册依赖MiniMax enabled | 新模型快照接入既有grant/run；保留独立image-01 Provider与工具审批 |

Runtime来源不能混为一次验收：当前 input-only `compatibility/runtime-input-only/source.lock.json` 指向 `fb79b1d53501ec90084b584af5fdbe221c7a25aa`、269 schemas、tree `34d353815dc8d800cb432a876d5b43350511f63b91ad9766f861e8bc8290cc92`；普通 native 历史投影另有旧来源。后续使用实际激活的固定产物与 canonical schema对齐，本轮未构建/运行二进制核验。

## 3. 官方资料与接入选择

读取日期 2026-10-02；均为公开文档 GET，无 API Key、无账号/模型调用。以下只摘必要协议事实，不把示例当成对本地配置的修改指令。

| 来源 | 已核实的必要事实 |
|---|---|
| [Kimi K3 快速开始](https://platform.kimi.com/docs/guide/kimi-k3-quickstart) | 模型 ID kimi-k3，默认推理max；Chat Completions与Responses字段不能混淆；真实调用需要账户具备使用资格，本轮未检查账户。 |
| [Codex接入指引](https://platform.kimi.com/docs/guide/codex-kimi) | 官方支持原生Responses直连，base URL为 `https://api.moonshot.cn/v1`，env引用KIMI_API_KEY；窗口1048576。不需要本地转换代理。 |
| [Responses API](https://platform.kimi.com/docs/api/responses) / [同页Markdown/OpenAPI](https://platform.kimi.com/docs/api/responses.md) | POST /v1/responses；嵌套reasoning.effort支持low/high/max且默认max。Markdown展开schema验证了折叠字段；只使用原生响应/工具关联，不依赖服务端保存历史。 |
| [推理强度](https://platform.kimi.com/docs/guide/use-reasoning-effort) | Chat Completions使用顶层reasoning_effort；多轮不能只留content而丢失必要assistant/tool信息。 |

拟受管profile（**设计数据，不在本轮写入任何运行配置**）：

| 项 | Kimi K3 | MiniMax M3 |
|---|---|---|
| provider/model | kimi / kimi-k3 | minimax / MiniMax-M3 |
| wire/base URL | responses / https://api.moonshot.cn/v1 | responses / 既有 https://api.minimaxi.com/v1 |
| effort | max；保留为精确原生值 | 既有native high；保留legacy兼容none/high |
| catalog | 默认max，明确支持max，reasoning能力开启；窗口1048576，与官方核对 | 保持现有能力配置，不能套用Kimi窗口/effort |
| secret | 独立受管Kimi secret引用，值不入config | 原有MiniMax引用不改写 |

官方quickstart与Codex接入页对不同工具路径的联网能力描述不同，不能据此自动增开联网工具。本期复用易界已经授权的工具集合，逐实际工具类型验证；不附带Formula、视频或新增web-search范围。

## 4. 推荐方案与重要取舍

| 决策 | 比较的可行选项 | 推荐与理由 | 状态 |
|---|---|---|---|
| DEC-01 默认作用域 | A全局记最后选择；B每新聊天默认Kimi、已有会话独立记忆；C打开任何聊天都重置Kimi | B。符合新增默认，同时保护旧上下文与费用预期；选择只作用当前target。 | 候选 |
| DEC-02 Provider接入 | A原生Responses；B新增Chat Completions网关/adapter | A。官网与原生wire匹配，避免新增网络/状态边界；B不作为失败后自动实施路径。 | 候选 |
| DEC-03 同会话切换 | A正常unsubscribe/冷resume同thread；B固定每会话provider仅新建可换；C原生能力确有缺口后提出最小Runtime patch | A优先；B不满足本期已有会话切换Must；C须在A有确定证据失败后另行审议，不能预先改内核。 | 需后续资格验证 |
| DEC-04 推理默认 | A显式max；B依赖服务默认；C映射high/xhigh | A。可观测且不受漏配/中间层默认影响；B无法证明请求意图，C不满足用户要求。 | 候选 |
| DEC-05 忙碌行为 | A锁定到空闲；B允许选择下轮并新建配置队列 | A。沿现有canSend/预约边界，避免第二队列与误投；停止可用。 | 候选 |
| DEC-06 持久化 | A只存在前端；B会话选择＋native/Host每操作快照 | B。恢复/排队/幂等必须持有不可变模型事实；A无法保证实际路由。 | 候选 |
| DEC-07 辅助与计划 | A标题/草案暗用旧全局模型；B标题跟随来源会话，草案显式选择，计划执行独立确认快照 | B。避免选择Kimi却隐藏调用MiniMax；标题保持既有触发次数/失败降级，不新增title刷新；计划不因默认更改扩大旧授权。 | 候选 |

### 同 thread 切换时序（源码推导，尚未执行）

1. Native 在现有会话/执行协调器内获取该会话互斥资格，核对scope、会话revision、outbox和计划预约；Host再读真实原生状态。未知或不空闲则拒绝，不把Desktop busy=false当证明。
2. 保存最后已确认profile；解除当前Host连接对该thread的订阅；不操作其它未知观察者、不停止其它会话。
3. 用同一thread ID调用原生resume，显式 model/provider，并按目标profile设置受管effort（Kimi为max，MiniMax保持既有配置）。原生正常结束旧loaded实例并冷恢复；shutdown失败/超时/closing/仍有观察者时不强行切换、不新建thread。
4. 核对回执thread ID、model/provider以及实际有效配置/目录effort；恢复订阅。回执仍旧值或不确定时不显示成功、不发下一轮。
5. 原生已换而本地保存/回执不确定时，保留“切换结果待核实”并阻止发送，按原切换操作只读查证/恢复；不能假装已回退，也不能无条件再发切换。确定未应用才恢复旧选择。
6. 一致性收敛后原子保存会话revision/profile并释放预约。未来发送冻结当前revision；并发旧发送明确冲突，不能路由到错误供应商。用户需再次显式发送，切换没有模型请求副作用。

该设计复用FEAT-132原生对话及唯一显示缓冲。不得新建reducer、复制消息正文、猜测turn身份、依赖标题/回答猜模型、把unsubscribe回执当作已卸载；原生工具/权限、MCP重连的费用和既有批准须纳入资格核验。固定Runtime下原生上下文跨provider不可用则报告阻塞，不能自行搬运私有推理密文。

### 密钥与付费边界

只记录“用户已提供Kimi凭据”，不写值、前后缀或校验指纹。未来local装配首选复用既有owner-only普通secret文件读取流程，以**独立Kimi引用**读取并仅向受管Runtime进程注入 `KIMI_API_KEY`；不读取/覆盖原MiniMax文件，不改全局 `~/.codex/config.toml`、shell profile或用户Codex设置。实际文件位置与导入在实施授权后通过受管方式确定；本轮不创建secret文件、不写Keychain。

Host清理继承环境、来源二选一、有效配置白名单、Runtime专用注入、所有工具/MCP子进程排除、错误和日志脱敏需同时扩展。新secret名应进入排除和set校验，不能仅在一个shell exclude中出现；密钥不通过Vue props、IPC/API请求、outbox、计划快照、进程命令行、URL或prompt传递。读取缺配置不是凭据有效性的证据；绝不通过报错回显secret。

当前允许的外部活动仅公开文档读取。真实模型/图片/商家/MCP调用授权均0，不复用历史额度；未来预算需包括两模型、多轮工具续推、重试、标题等隐含调用并采用有界计数。max可能增加延迟/token成本；不承诺和MiniMax同延迟/同价格，不设置未经证实的费用数字。不执行充值或生产接入。

## 5. Contract First 与数据兼容

本次修改仅文件文档，impact=none。功能包统一按 **breaking** 规划：旧IPC拒绝额外参数，旧Host/Desktop仅认MiniMax，新增响应值和durable快照可能令支持中的reader失败；默认改变另有semantic影响。最终应通过独立版本/显式能力协商保护旧交互，而不是因为新增可选字段就降为additive。

| 边界 | 权威源/Owner | producer → consumer | 候选变更及兼容要求 |
|---|---|---|---|
| Provider protocol | Kimi官方；Host/Runtime adapter负责 | Runtime → Kimi Responses | 受管profile、catalog、精确max与上下文/工具；官方能力不等于本产品已测 |
| Codex app-server | 固定Runtime canonical schema | Host ↔ Runtime | 复用既有方法；Contracts新增适用用途投影/来源/conformance。若改Runtime源，先候选Runtime再投影 |
| 易界Host wire | yijie-contracts源契约；段成威 | Desktop native ↔ Host | 模型目录/能力、选择请求与有效模型响应、错误/版本；普通/多模态/权限turn/草案都覆盖。名称路径在源设计时固定，本轮不发明已存在endpoint |
| Desktop private IPC | Desktop同源schema/generator；段成威 | Vue/store ↔ Rust | 选择revision、模型profile快照、结构化结果/冲突；不手抄影子DTO、不把任意URL/key开放给renderer |
| durable存储 | Desktop migration与Host Store；段成威 | writer/outbox/plan/grant/run → reader/replay | expand，新的可识别版本与兼容reader；旧digest/domain与旧已受理记录原样保留，新版本才纳入profile/effort |

实施技术顺序为：官方/固定Runtime事实 → Contracts权威源与native投影、Desktop私有IPC源 → 生成及focused conformance → Host/provider与兼容reader → Native模型事务/出站与计划快照 → Vue入口 → 一次整体真实验收。**不建立治理切片、per-slice G3或独立D1门禁。** 若固定Runtime无需改动，不能为流程凑步骤重编译/替换它。

方向兼容：先让provider接受新请求版本，再由新consumer发送；先部署能读新响应/快照的consumer，producer才激活Kimi。旧客户端继续旧MiniMax语义与原操作ID，不能收到无法解码的新枚举；新客户端遇旧Host显示“当前执行环境不支持模型切换”并禁用，不谎称Kimi就绪。生产所需全支持基线/tag/Owner审查等并未完成；本地sibling结果不得冒充发布兼容。

数据采用最小expand，不重写原生历史或旧每轮来源；缺旧字段表示legacy/unknown，可信现有session绑定可作为下一轮模型依据，但不能推定全部历史轮次。新请求指纹涵盖profile版本/provider/model/effort，旧请求仍用旧domain计算和查证。计划模型成为授权语义：启用/立即运行/重跑预览与grant digest/run snapshot一致，模型变化须新审阅；三类目标的执行不能在投递时重新读取全局默认。

回滚候选：先关闭新选择/新writer，正常处理或保留在途/未知操作；保持可读新格式的reader及原数据根，正常退出后回到兼容版本。不能降schema、清库、复制日常库来回覆盖、重跑旧outbox或无提示把Kimi请求改给MiniMax。已是Kimi的会话如果回退版本不能执行，明确只读/不可执行，历史可读；原生同thread历史是否可被旧Runtime继续读取也须验证后才能承诺。

## 6. Fact / Assumption / Unknown / Conflict 与风险

| 类型/ID | 内容 | 后续解除方式及停止条件 |
|---|---|---|
| Fact-01 | 用户明确默认Kimi/max、保留MiniMax、只落包；当前Host链路固定MiniMax；Runtime源支持max/Responses | 以U01–U05与F01–F20定位；无运行验收声明 |
| Assumption-01 | 默认按新建聊天解释；已有会话记自身选择；busy禁改；标题跟随来源 | D0审阅可整体调整，当前标候选不虚构确认 |
| Unknown-01 | 固定实际产物在受管多profile下能否稳定原生卸载/冷恢复同thread并保持权限/MCP/上下文 | 实施获准后优先无模型正常资格检查；失败则停止该路径，形成最小改动决策 |
| Unknown-02 | Kimi目录、实际max、图片/工具/草案schema在当前固定Runtime组合下是否兼容 | 先源码/声明式参数检查，再获独立额度的真实链路；未核实不能D4 |
| Unknown-03 | 用户key账户资格、余额、限速及实际可用性 | 本轮不测；后续受管注入和明确调用授权后验证；失败不自动充值/换模型 |
| Unknown-04 | 所选日常入口实际SQL/Host schema及回滚reader，当前dirty改动与实施候选合并方式 | 实施前重核workspace/source/migration，不覆盖既有20文件 |
| Conflict-01 | 截图有麦克风，实际Composer没有 | 用户要模型入口，定位到真实发送/停止左侧，不扩语音 |
| Conflict-02 | “默认Kimi”与既有会话/已批准计划的旧模型 | 新建默认与已有选择分开；历史不回写、计划授权不静默扩展 |
| Conflict-03 | 模型选择成功但底层override被忽略/effort被降档 | 以真实配置和模型请求证据判定，未收敛阻止发送 |
| Risk-01 | 换provider改变上下文序列/加密推理/工具结果可重放性 | 原生权威处理、跨provider工具多轮测试；不在UI重建上下文 |
| Risk-02 | max、标题、工具循环、重试隐含增加费用与等待 | 明确预算覆盖全链、总时限/调用上限与正常取消；不额外轮询模型 |
| Risk-03 | 新secret进入shell/MCP或错误 | 精确注入/排除与内容无关证据；发现泄漏阻断，不把key作为fixture |

非核心生产性能、跨设备同步、完整韧性矩阵、所有平台工具质量评测、生产secret vault和发布/灰度明确延期；本地正常使用、数据不损坏、秘密不泄漏、核心可访问性与Must不延期。不能因16h停点删除AC或改PASS。

## 7. 本轮实际改动与调用账

| 项 | 实际结果 |
|---|---|
| 文档创建 | 使用canonical new-feature.sh生成四文件，填入需求/事实/计划/未执行状态；增加用户截图只读副本 |
| 产品/契约/配置/数据库/二进制 | 0修改；未generate跨仓产物、未读取运行中库 |
| 服务和本机产品验收 | 未启动/停止；未运行原生资格、UI或D4 |
| 外部活动 | 仅公开Kimi文档GET；未访问凭据文件/余额/模型endpoint |
| 付费/业务调用 | 模型0；图像生成0；外部MCP业务0；无新增授权 |
| Git动作 | 只读status/branch/HEAD/remote；未commit/push/branch/tag/发布 |

编制期间进行了两个并行只读工程调查，分别核对Desktop与Host/Runtime/Contracts；整合时以精确源码修正早期“Runtime不支持max”的误判，最终本包记录的事实是**Runtime支持max，当前Host/目录/consumer限制尚未适配**。不会把交叉复核称为独立人工评审或产品测试。

文档检查及最终需求自检见02。下一步仅由Owner审阅本包；本次任务完成后停止，不自动进入实现或要求提供重复授权。

## 8. 2026-10-02 Owner授权后的实施记录

用户明确“开始执行 feat-156 需求”，按现有包批准D0及local整体实现；不另建治理切片，不自动提交/推送，不转用历史调用预算。此前只落包与NOT RUN是起草阶段事实。初始五仓状态见[evidence/implementation-initial-state.json](evidence/implementation-initial-state.json)；原20项Desktop改动保留。

固定Runtime真实产物在新临时CODEX_HOME、普通本机Responses测试服务下，完成同thread Kimi→MiniMax→Kimi三轮，实际请求effort=max/high/max；未使用凭据或远程Provider，EOF正常退出0。脚本为Host `scripts/verify-model-switch-runtime.py`，结果见[evidence/native-model-switch.json](evidence/native-model-switch.json)。这只证明原生路由/参数/正常冷恢复可行，不代表真实模型、产品E2E或D4。无需新增Runtime补丁。

下一步按源契约→生成与conformance→Host/provider/store→Desktop native/outbox/计划→Composer接通。真实调用额度已单独询问，在明确答复前保持0。

用户已回复“授权上述24次验收额度”：两Provider合计24次模型HTTP请求，含标题/工具续推/重试，最多2次图片理解，单次输出8192 tokens；图片生成与外部MCP禁用。实际调用台账见[evidence/paid-call-ledger.json](evidence/paid-call-ledger.json)，当前真实0。此额度不是Git/发布授权。

Contracts独立model-selection-v1源、新模型感知路由、Go/Rust/TS生成及3项普通conformance已通过；采用显式local_worktree_candidate摘要同步，不假造不可变commit、不改旧锁。Host两模型受管层、profile来源、同thread切换与Store7恢复字段进入实现；编译检查通过，2项模型selection/replay定向测试通过。Desktop新增SQL28模型选择/operation快照表与native接线正在实现。上述均非产品AC/D4通过。

### 9. 真实资格发现与 Runtime 最小兼容候选（待 Owner 确认）

2026-10-02：真实请求 1–3 HTTP 200，固定 Runtime 同 thread 完成 Kimi/max → MiniMax/high → Kimi/max；请求 4–5 草案均 HTTP 400。第5次保留安全错误分类：`responses: unsupported tool_choice value: "none"`。当前 Kimi Responses 官方 schema 的 `ResponsesToolChoice` 仅声明 `auto`。问题不在 max、账户资格或结构化 schema；草案结构化输出尚未得到可判断结果。调用账保留失败次数，不自动重试。

当前 Runtime `.yijie/patches/input-only/0003-input-only-execution.patch:174` 在 `prompt.tools.is_empty()` 时把上游 `tool_choice="auto"` 改成 `none`。原生 input-only 的空工具集、贡献者禁用、无文件/网络权限及非文本响应拒绝是独立 native 约束；不能移除这些约束，也不能在 Host 建转发桥或自动改用 MiniMax。

可审阅候选：在固定上游与现有三补丁之后新增一个独立、可重放的 `0004` 兼容补丁，仅将 Responses 的 tool_choice 恢复为上游 `auto`，包括空工具集请求；保持 tools=[]、input-only admission、response-item 拒绝、sandbox/permission/MCP/扩展限制不变。不直接修改 codex-rs 原始子树。由 canonical 构建脚本产生独立 FEAT-156 候选目录，保留现有 input-only 已核验产物和 hash；生成并比较全部 stable schemas，预期零形状差异；先补真实固定新产物下的正常无工具/草案检查，再更新 Contracts/Host/Desktop 的精确候选来源，最后在剩余额度内重验草案与普通对话。不得以代理改写 tool_choice 或 mock 响应替代产品验证。

需确认依据：`yijie-codex/AGENTS.md`「是否修改 Runtime 核心、协议、沙箱、权限、认证、更新或遥测行为」「是否新增补丁、依赖、feature flag、构建目标或发布产物」要求先确认；本包 brief §5 亦要求遇新 Runtime patch 停止依赖步骤并形成候选决定。本次开始执行已授权 Host/Desktop/Contracts 和正常验收，未把该新的 Runtime 事实视作预先批准。等待答复时继续非依赖的 UI、编译、文档和本地测试；D4/AC 不标通过。


### 10. 非依赖工作收尾（Runtime决定待答复）

Host/Native/前端已接入模型目录、选择、固定profile与operation快照；普通和草案提交共用原有执行协调器，计划definition/grant/run包含模型，卡片与记录显示有效配置。SQLite28使用新表，无历史回填；Store7保护新模型管理状态。精确源候选与旧不可变来源分开：新增chat-model-consumer-source与chat-model-build-candidate，不改既有committed helper/旧locks。所有Git仍仅工作树编辑，无提交或推送。

实测发现并修复首轮outbox尚未物化的外键问题、迟到同revision覆盖switching、重开后切换原operation丢失、标题绕过验证计数器与关闭writer后模型outbox进入旧dispatch的问题。均用正常状态/持久化fixture验证，不使用故障注入或假Runtime可执行文件。用户既有Desktop改动保留。

完整记录见02 §4。5个ChatPage失败在HEAD版页面对照中完全重现，未篡改断言；全量生成门禁仍受旧公共契约clean-checkout要求限制，不将focused通过写成make test/lint整体PASS。100%菜单与键盘已实测；1180×760/200%发现浮层重复缩放，已修复并标准构建，随后Mac锁屏导致复核未完成。计数器已正常关闭，模型HTTP5/24、图片0/2。等待Owner对§9候选确认；依赖步骤没有继续，也未激活日常默认writer。

### 11. Owner批准最小Runtime兼容补丁（2026-10-02）

Owner明确接受恢复上游tool_choice=auto，保留空工具集、input-only、沙箱和权限；独立候选产物且复用现有约24GiB编译缓存。本授权解除§9依赖步骤的暂停。按0001→0002→input-only0003→FEAT156独立0004顺序重放；原始codex-rs子树、旧构建脚本与固定产物均保留。新build只使用现有codex-rs/target，不另复制缓存。真实调用额度沿原账继续，构建开始时5/24、图片0/2。

### 12. Owner暂停（2026-10-02T10:46:34+08:00）

用户要求暂停执行。已停止新增工作并保存[恢复状态](PAUSED-STATE.md)。新Runtime构建和零付费资格检查已完成；最终Host消费编译、App重建与新产物真实验收未运行。调用账仍5/24、图片0/2，meter停止。无在途本任务服务，D4及全部AC不晋升。

### 13. Owner恢复执行（2026-10-02T17:16:40+08:00）

新Runtime受管Host本机4次Responses全部通过：同thread Kimi→MiniMax→Kimi记号保留与canonical草案，tools=[]且tool_choice=auto；原生input-only实时资格保持。Host go vet与TestChatModel通过。Synthetic实际累计11（计数器停止后将台账7补记+4，不并发编辑运行中的meter账）。本轮真实Kimi草案重测开始，沿原5/24额度续用。

### 14. fresh原生验收与Store7草案缺口

正常启动发现cmd/desktop-host仍只接受旧input-only产物，已改为复用精确SupportsInputOnly产物对校验，旧产物仍支持。另修复模型读取确认成功后前端未清除旧pending operation的问题；缺Kimi配置与原操作恢复两个回归用例、launcher共18项通过。

最终候选App已真实完成Kimi→MiniMax→Kimi同对话记号连续性、文件138B的7+5=12及本地只读命令exit0续推；Kimi与MiniMax各1次图片理解均正确。13/24次、图片2/2；今后不再发图片请求。亮色1180×760/200%菜单定位通过；Owner授权临时系统深色，原生深色100%菜单可读，随后恢复原浅色。标题接口原有LoadConfig门禁仍关闭，未新增启用或额外标题请求。

桌面草案未调用Provider就卡住：只读诊断证实create_attempted=1、turn_attempted=0、Host映射不存在。根因validatePurposeWrite只接受Store6；Model writer已升Store7。已修复v7合法草案写入，保留draftWriter与purpose/workspace/schema/policy一致性；新增Store7单测和Native模型草案原claim/bind/turn流程测试均通过。失败记录保留，不重写attempt标志，不自动重发。单条失败验收草案的正常永久删除确认框已准备，按电脑操作规则单独询问Owner；其它成功聊天和台账均保留。详见evidence/draft-store7-failure.json。

### 15. 草案暂停确认与绑定计划模型重审补齐

按R09，FEAT156草案确认改用既有schedule_confirm_draft_v1，仅保存关闭状态；FEAT155非模型入口保持原命令。绑定专属聊天此前未读取当前模型的缺口已补齐：私有IPC源PlanDetail新增只读bound_conversation_id，再canonical生成Rust/TS/严格validator；Native在scope内读取有效绑定，页面读取该聊天已确认模型供审阅，未新增设置中心或切换请求。save同时核对绑定模型；执行事务中模型不匹配返回既有grant_stale，提示编辑重审或显式把聊天切回。

新增前端6个目标模型用例（现有/专属、未绑定默认、未知/迟到读取）；相关前端46项、lint通过。Native普通持久化fixture证明两类绑定目标冲突不创建run、不消耗grant、不改旧turn快照；更新计划后旧grant拒绝，新grant按新模型在同聊天创建turn。测试须显式local/demo_fast/model writer环境（默认关闭时按设计拒绝）；已在显式环境通过。无恶意fixture、假Runtime或真实数据修改。App正常退出exit0后canonical重建中。

Mac锁屏中断了第一次退出动作，Owner手动解锁后才继续；未尝试绕过锁屏。失败草案永久删除仍等待单独确认，成功聊天与原失败事实均保留。当前13/24真实请求、图片2/2；本节不构成D4。

### 16. 实际草案、停止、缺配置与恢复（2026-10-02约19:00）

请求14：当时canonical App中Kimi/max生成合法草案，真实请求structured_output=true、tool_choice=auto、tools=0、HTTP200。审阅表单明确关闭保存，确认回执“已暂停”，定时任务开关off，执行模型Kimi K3/max。随后立即执行被旧失败草案的结果不明状态挡住，未产生模型调用；该历史阻塞后来通过§17中Owner明确授权的单条正常删除解除。该草案未自动开启。

请求15：通过正常Stop按钮中止Kimi生成，原生显示已中断并保留部分文本，模型入口随后恢复；meter的BrokenPipeError来自正常取消，未标为完整模型回复。无强杀。

显式YIJIE_KIMI_API_KEY_FILE为空的正常未配置启动暴露缺口：自动恢复所有历史Kimi thread使全局readiness失败。现仅当目录明确not_configured且该聊天没有活动/待提交操作时，保留终态历史不自动resume；未知/活动请求仍走原恢复限制。新增声明式测试覆盖三种未结束字段及目录未配置条件。真实重建后，默认Kimi保留但禁发，草稿不丢，明确选MiniMax恢复发送；已有Kimi历史仍可读并可显式切MiniMax。正常退出后恢复受管key来源，新聊默认Kimi、原聊仍MiniMax；显式切回Kimi并发送请求16，正确返回原记号青山。恢复过程不重发任何历史请求。

最新检查：原生FEAT156五项（含显式环境用例）全部通过；cargo fmt/clippy全部target通过；前端定向46项/lint、generate:check（既有clean固定目录）、docs:build通过；feature schema/audit-claims通过。原固定Runtime与新候选四个hash均保持。累计16/24，图片2/2。最终删除确认框仅指向失败草案147a52f0，尚未确认；成功聊天和已暂停计划保留。当前阻塞是该不可逆清理所需的单独授权，未通过数据库改写、重复请求或新数据根绕过。

### 17. 单条删除授权、计划真实运行与无项目聊天兼容

Owner明确“永久删除FEAT156专用验收这条失败草案”。通过应用最终确认执行，清理后失败草案与其目录从侧栏消失，自动返回保留的主聊天；无修改SQL/attempt、伪造状态或强杀。请求17专属聊天Kimi/max完成；随后显式切专属聊天为MiniMax，原Kimi计划真实阻止投递并提示重审，无新增HTTP。编辑读取已绑定聊天的MiniMax，审阅保存后请求18 MiniMax/high完成；旧记录仍为Kimi。请求19每次新建聊天Kimi/max完成，实际新chat/turn与专属目标不同。两计划均关闭，仅做单次运行。

最后已有聊天目标的只读列表失败，定位为已有SQL27 managed_chat工作目录未进入共享WorkspaceSource闭集，同时旧grant/run SQL17 CHECK只接受user_project/managed_schedule。R09要求已有聊天沿原目录/模型执行，故纳入FEAT156既定breaking/local范围：先把scheduled-execution源家族升未发布0.2.0并添加精确managed_chat含义，再canonical生成/sync Rust/TS/IPC，再扩展Native引用与SQL29兼容迁移。未把managed_chat伪装成用户书签或计划目录，没有新路径权限或新DB。历史enum值、旧grant/run/snapshot字节、摘要与幂等身份保持；支持新版reader后再写新值，旧不识别版本安全拒读，无降库。无生产发布或不可变版本宣称。

定向检查已通过：共享严格schema和确定生成/同步、Native目标列表及授权工作区、旧grant/run/snapshot/外键/触发器保留及不降库、前端25项、lint/fmt/clippy。首次遗漏显式local candidate flag导致同步中止，补显式环境重跑后通过，未放宽旧committed helper；首次native用例准确暴露旧CHECK，补正式迁移后通过。当前19/24，图片2/2。Mac在正常退出动作前再次锁屏，已请求手动解锁；当前App仍旧构建，禁止宣称新迁移真实验收或覆盖运行中App。


### 18. 日常默认、只读边界与最后真实诊断

SQL29最新构建下请求20已有聊天计划执行成功，保留青山记号及原附件。新增只读/无权限模型选择保护：前端与native binding/project/deletion再校验，原生和页面focused用例通过。canonical日常入口默认跟随现行scheduled入口启用模型，stable/显式rollback保持独立。原用户旧MiniMax聊天只读检查未改，新建默认为Kimi。

请求21日常Kimi成功；22–24 MiniMax文件/只读工具回合收到空参数，后续由24次上限拦截，不超额；失败记录保留。切回Kimi又发现终态systemError被Host拒绝：固定上游确认该状态不含运行、pending审批/input，故仅补允许此终态沿正常unsubscribe/resume恢复；in-process协议测试先失败后通过，active/未知仍拒绝。正常Quit、冻结最新Host来源、canonical重建，解锁后原operation重试切换Kimi成功，无新增HTTP。

Owner再次解锁并明确“授权追加16次及2次图片理解”：任务总上限40HTTP/4图片、每次8192，图片生成与外部MCP仍不调用。正常关闭旧meter后将synthetic7补至11，并保存原授权及追加记录。新增仅长度/摘要的被动SSE观察，不记录prompt、响应正文或密钥，不改写响应。

25简化API参数完整；26/27独立MiniMax原生命令exit0。28/29原跨模型会话再次失败，观测到delta及response.completed参数完整且摘要相等，而两个中间完成事件arguments为空；30模型据实报告工具失败。定位为固定Runtime消费中间Item、不恢复终态完整参数的协议兼容缺口。新方案03已可审阅并按Runtime仓AGENTS提交新增补丁确认；未应用/构建。当前AC-005FAIL、AC-010pending、D4未通过，不能以独立工具成功覆盖跨模型失败。


### 19. Owner批准流式参数兼容并继续执行

收到上述明确执行授权。复核确认30次HTTP及2次图片用量、28/29参数delta与最终Item摘要一致而中间Item为空、独立工具26/27成功，故不做Provider整体降级。现按03实施单一SSE重组补丁：仅空参数完成Item等待终态、有界缓冲并保持顺序、严格身份/增量一致；正常非空路径、权限与input-only保持。独立新产物继续复用原target缓存。

### 20. 最小修复资格与最终原生验收完成

0005只改Responses SSE空参数完成Item的安全承接：有界缓存、严格身份/终态/增量一致、一次交付；输入限制/工具路由/权限继续由原生层控制。canonical新增build/test/manifest脚本生成独立chat-models-stream-args候选，复用原target；4新用例、34项完整SSE、clippy、269schema逐字节、正常EOF与补丁可重放全部通过。原两组Runtime和manifest四hash不变，codex-rs原样子树未写。

新Runtime实际请求33再次遇到同一Provider问题（中间参数0bytes，delta/terminal18bytes且摘要相等），本次原生命令执行exit0，34续推保留远山/12。32有效JSON缺cmd仍被原生schema拒绝，没有猜测命令。31→32–34→39在同一聊天形成最终Kimi→MiniMax→Kimi上下文闭环；35/36两模型图片正确，37 Kimi受限草案合法。确认时明确选MiniMax并保持关闭保存；38专属MiniMax、39已有聊天Kimi、40每次新建Kimi完成。随后专属chat改Kimi，旧MiniMax计划前置拒投，0HTTP；编辑重新审阅后保存Kimi/off，历史run仍MiniMax。

补齐取消未提交草案后的新聊默认重置，页面回归先失败后通过；readonly+reset两项及lint/build/generate/docs全部通过。Owner追加10次授权后累计上限50，图片仍4；计数器正常退出后才更新授权和tuple，不覆盖运行中内存账。41/42最终Kimi只读工具exit0并保留远山/12，43正常Stop中断及恢复，44 MiniMax受限结构草案合法且确认默认Kimi（审阅取消，未保存计划）。累计44/50、图片4/4、synthetic17、标题/生图/外部MCP0。

最终亮暗100%、1180×760/200%菜单与滚动发送可达，外观/倍率/窗口恢复。App正常Quit，meter正常Ctrl-C，之后原daily入口无meter覆盖启动ready；新聊天Kimi，已保存MiniMax草案选择及中断历史保留，三个计划全部关闭。仅原失败草案147a52f0按此前明确授权删除，其余记录保留。

五仓diff与源摘要已刷新；初始19份有hash的Desktop文件16份字节不变、3份必要叠加，secret-like扫描0。保留ChatPage5项基线失败、FEAT155授权刷新关闭未提交表单的既有交互限制、未运行禁止的历史测试以及未作生产发布等边界。最终Must映射与D4结论以02 §8及feature.yaml为准。

### 21. 授权分仓本地提交，保留原工作区改动

Owner明确授权审查并提交FEAT-156、暂不推送。核对最终源码摘要无漂移后按Runtime→Contracts→Host→Desktop提交；Runtime提交变化由原generator重新生成精确来源投影，Host提交后由canonical freeze生成Desktop构建快照，未改已资格的二进制/manifest。两处Desktop文档更新旧阶段文案，Host补Kimi凭据隔离说明。

Desktop四份混合文件通过index-only内容拆分，只提交FEAT-156；全部初始20份用户改动留在工作树，19份初始hash逐项验证。纯暂存源码单独lint/build及29个定向用例通过，不依赖未提交流式/图标/耗时修改。源码与本地提交清单、运行工具的小范围修正和已知限制见02 §9及evidence/local-commit-review.json。无新增付费调用、强杀、二进制覆盖、推送或发布。
