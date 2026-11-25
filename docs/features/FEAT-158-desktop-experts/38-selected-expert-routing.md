# 输入框所选专家在本轮优先

2026-11-26 · FEAT-158 · 修复方案与实施前复审

发送时，输入框里已生效的专家等同于用户在这条消息中点名的专家。它决定本轮由谁回答、“这个专家”指谁，以及询问用法时应该查哪份资料。用户仍可让当前专家处理上轮的内容，例如请分镜师把京东开店清单改编成短剧。

## 本次故障与连接器先例

11 月 26 日北京时间 01:15，MiniMax-M3 在同一聊天里使用了京东运营专家 `jd-ops-expert@0.1.3`。随后 Host 记录了移除成功（绑定修订 1）和选用“漫剧编剧与分镜师”成功（修订 2）。01:18:46 发送“如何使用这个专家”时，Host 受理回执中的专家已经是 `agentgrid-comic-storyboard-director@0.1.0`、修订 2。原生执行记录里，上轮京东回答和本轮提问之间只有一条连接器选择说明，内容为“无”。工具随后读取了京东包的 `SKILL.md` 等资料，01:19:20 的最终回答也介绍了京东专家。回执和原生记录可以核实选择与工具动作，本次未取得该轮发给供应商的完整请求。

11 月 24 日连接器从微博切换到 Tushare 时，只更新线程基础指令的版本也答成了微博。修复版除了更新基础指令，还在每次发送前把已核验的选择写成一条开发者消息，放在旧回答和新问题之间。用同一个原生线程和原句复测，回答转为介绍 Tushare 的 `tushare_daily`。[连接器修复与两次真实验收](../FEAT-157-desktop-market-connectors/29-selected-connector-routing.md)

## 建议改动

1. **让基础指令和本轮说明指向同一个专家。** Host 以本次提交冻结的 `TurnExpertSnapshot` 为依据，核对绑定修订、专家 ID、版本和包摘要。沿用 `ResolveExpert` 的解析结果，从同一份已校验的目录条目取展示名。在线程新建和正常恢复时，用该专家的角色、知识索引及指代规则组装 `baseInstructions`。当用户问身份、能力或用法，优先点名当前专家、给出它所需的输入和典型产出，按需查它自己的资料。[提交与校验](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/market_submit.go) · [资源解析](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/skills/experts.go) · [专家指令组装](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/expert_instructions.go)
2. **每次发送都把专家选择放在用户原文前。** 在 `StartTurnV2` 现有线程锁内，复用连接器调用的原生 `thread/inject_items`。同一次调用中可分别写入连接器说明和专家说明，然后执行 `turn/start`。例如“本条消息选用「漫剧编剧与分镜师」（agentgrid-comic-storyboard-director，0.1.0）。用户说的‘这个专家’指这位分镜师。”角色全文与资料索引留在基础指令里，用户气泡、用户消息 ID 和原文沿用现有流程。专家决定答题身份，连接器选择约束适用的服务操作，调用继续遵守当前原生权限。[现有发送入口](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/session_protocol.go) · [连接器说明](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/market_turns.go) · [原生接口](https://github.com/36Dge/yijie-codex/blob/54bc9de9092a604863abe46aaaea8a4ead436368/codex-rs/app-server-protocol/src/protocol/common.rs)
3. **处理移除、恢复和重复提交。** 已有专家的会话，移除后随下一条消息明确写“本条消息未选用专家”，此时再问“这个专家”可提示用户选择或点名。普通会话缺少专家快照时走原流程。只在派发新一轮时写说明，切换页面、恢复绑定和回读已受理操作都无需追加。若写说明失败，停止派发，沿原操作查询和恢复。切模型、重开聊天或查询重试都以对应提交的快照为准。[绑定与恢复](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/experts.go) · [原回执重读](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/market_submit.go)
4. **让输入框的选择也优先于正文自动匹配。** 修复前，Desktop 在发送前会解析“请用某某专家……”并可能调用选择器改绑。建议点击发送时记下已选专家的 ID、版本和绑定修订，提交前复核。如异步准备期间绑定已变化，保留草稿并提示当前选择。已有有效专家时，正文照常交给它处理。只有输入框没有选中专家时，才使用现有正文点名和歧义提示。准备中或版本不可用时，沿用现有发送限制。此次原句以“如何”开头，没有触发正文改绑。[发送前解析](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src/pages/chat/ChatPage.vue) · [专家名称匹配](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src/domain/explicit-expert.ts) · [Native 提交复核](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src-tauri/src/chat/experts/store.rs)

拟议实现的 `contract-impact = semantic`，涉及 Desktop 解释选择的优先级和 Host 将选择提供给模型的方式。可复用现有提交、回执和原生接口，旧聊天及数据库无需迁移。回退点为 Desktop 的正文匹配分支和 Host 的模型输入组装。

## 实施顺序与完整执行链

| 执行位置 | 现有职责和本次落点 |
| --- | --- |
| 选择与发送 | 新聊天从共享草稿取专家，已有聊天从 Native 已确认的 `BindingView` 取专家。点击发送时保存该次意图。权限、技能目录或模型异步准备完成后按会话、绑定修订、ID 和版本复核。有选中项时直接使用原选择，无选中项时仍可通过正文明确调用。查询已有提交时使用原提交意图。[页面](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src/pages/chat/ChatPage.vue) · [绑定与提交](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src/stores/chat-experts.store.ts) |
| 冻结与派发 | Native 在现有消息和 outbox 事务内核对绑定、冻结专家快照，继续通过原私有授权提交。Host 先查原回执，再核对快照与绑定并解析安装包。只把本版本目录展示名加到进程内的解析结果，复用原有引用、角色、知识索引和媒体、联网策略。[Native 冻结](https://github.com/36Dge/yijie-desktop/blob/8e0b9ecf0dc3c2ea3117ae9618d75a3f0e618f5b/src-tauri/src/chat/experts/store.rs) · [Host 受理](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/market_submit.go) |
| 建立或恢复原线程 | 复用 `StartThread` 和 `SwitchThread`。本轮已核验的同一专家身份同时供基础指令和轮前说明使用。显式移除、从未选用及内部仅提供角色文本的调用分别处理。[会话适配](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/experts.go) · [原线程切换](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/chat_models.go) |
| 启动本轮与显示结果 | 在 `StartTurnV2` 校验完输入和权限后，使用原线程锁一次提交本轮选择，再以原用户消息 ID、文字、附件和技能启动一次。原生事件和回执继续承担回答展示与结果恢复。通过固定 Runtime 发到本地模型端的实际请求验证顺序，并分别核对真实 MiniMax 回答。[轮次发送](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/session_protocol.go) · [既有连接器回归](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/market_search_routing_test.go) |

## 实施前复审

逐段复核后确认四个实现约束。

- 草稿初次发送和已有聊天续发共用发送入口。异步期间比较绑定值，允许相同内容的目录刷新。对“没有选中、正文明确点名”的路径，只有选择器成功返回并且 ID、版本相符，才能采用新意图。此前冻结的原提交优先由现有回执恢复。
- 专家资源同时供本轮提交、绑定切换和历史恢复使用。解析资源时只构建进程内身份；写入轮前说明的时机限定在实际发送。旧版本的展示名取自该版本受管条目，模型入口只需展示名、公开 ID 和版本。
- 普通上下文、明确移除及旧的内部角色调用有不同语义。明确移除要覆盖历史指代，普通对话保持原始输入。连接器的已选和清空说明独立保留。只问用法时可按需读取当前包资料。
- 开发者消息写入和启动轮次是两次原生请求。同一线程锁保证顺序，原回执负责重复请求和未知结果。验收分别核对请求内容、真实回答与工具来源。[快照校验](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/experts_storage.go) · [原回执与启动顺序](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/session/market_submit.go)

## 验收

| 场景 | 通过标准 |
| --- | --- |
| 原例，同一 MiniMax-M3 聊天 | 京东专家先回答开店问题，切到分镜师后原样发送“如何使用这个专家”。首句或首段点名“漫剧编剧与分镜师”，给出故事梗概、目标时长等输入，以及脚本、镜头表等产出。若读取专家资料，来源属于分镜师。仅问用法即可得到说明，无需启动创作或调用业务服务。[分镜师角色和交付范围](https://github.com/36Dge/yijie-skills/blob/ed3614f3d6aea41a84be1ebc7221bd5b74874465/plugins/yijie-desktop-skills/experts/agentgrid-comic-storyboard-director/skills/comic-storyboard/ROLE.md) |
| 实际模型请求的顺序 | 用固定 Runtime 和本地模型端检查请求。基础指令使用新角色及索引。输入中保留旧京东回答，其后出现本轮分镜师声明，再出现一次用户原句。连续两轮选同一专家，每条消息都有自己的声明。[连接器已有回归范式](https://github.com/36Dge/yijie-agent-host/blob/bdb142a6309b6e5d71f74bfb888fbcf324fa7b1d/internal/codex/market_search_routing_test.go) |
| 同时选择专家和连接器 | “这个专家”指向分镜师，“这个连接器”指向当前服务。两项可以独立更换或移除，清空其中一项只清除该项的指代。 |
| 移除、切模型、重开和新聊天 | 移除后发出的消息记录“未选用”。切模型或重开已有聊天后使用有效绑定。从未选专家的新聊天沿用普通输入。复核原提交只返回对应回执，同一用户消息只执行一次。 |
| 正文提及其他专家 | 已选分镜师时，即使正文点名京东专家，发送快照仍是分镜师。用户可以把旧专家的答案当作改编素材。清空选择后，正文明确调用的专家仍可按原入口选用。 |
