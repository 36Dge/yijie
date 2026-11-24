# MiniMax-M3 原生网页搜索来源实测与 Desktop 接入方案

2026-11-24，易界日常客户端使用的 MiniMax-M3、中国区 Responses 接口。

**可以支持。** MiniMax 能在同一响应里分别给出每次搜索命中的网址，随后在回答引用中给出标题。运行时显式请求来源，用搜索记录确定网址的归属，用同一响应中网址完全相同的引用补标题，即可复用现有 Kimi 搜索卡片。供应商能力已实测。随后已在日常 Desktop 完成接入和城市对比真实验收。[交付与实测](48-minimax-native-search-sources-delivery.md)[结构化实测证据](references/minimax-native-search-sources-20261124.json)

## 两项验证

通过项目日常使用的模型和供应商地址，直接对 `POST /v1/responses` 发送 3 次流式请求。三次使用同一条公开输入，让模型分别搜索郑州天气和 Python 最新稳定版。均使用 `MiniMax-M3`、`reasoning.effort=high`、`store=false` 和内置 `web_search`。请求体只改变 `include`。每次均返回 HTTP 200、模型名 `MiniMax-M3`、响应状态 `completed` 以及两个不同的搜索项 ID。

| 组别 | 在原有 `reasoning.encrypted_content` 上追加的字段 | 郑州搜索的网址 | Python 搜索的网址 | 回答引用 | 能匹配标题的来源行 |
|---|---|---:|---:|---:|---:|
| A 日常请求规则 | 无 | 未提供 | 未提供 | 20 条 | 无逐次归属依据 |
| B 请求来源 | `web_search_call.action.sources` | 10 | 10 | 20 条 | 20/20 |
| C 检查能否提早取得标题 | `web_search_call.action.sources` 和 `web_search_call.results` | 10 | 10 | 20 条 | 20/20 |

**逐次来源。** B、C 两组的两个搜索项在 `response.output_item.done` 就分别带有自己的 `action.sources`，最终 `response.completed.output` 保留相同的顺序与网址。每条来源只有 `type=url` 和 `url`。C 组追加 `results` 后也没有返回独立的结果字段或逐条标题。A 组的搜索完成事件只有查询词和动作类型，与商品查询截图的表现一致。历史 Kimi 天气记录的一次搜索带 23 条标题和网址，同轮 MiniMax 商品查询的 13 次搜索均缺少来源字段。[原请求规则](../../../../yijie-codex/.yijie/patches/chat-models/0007-feat-164-kimi-k31-pro.patch) · [历史项目审计](../../dev/web-search-audit-20261115.md)

**引用归属。** 每组均观察到 20 条 `url_citation`。引用事件的 `item_id` 属于回答消息，引用对象本身没有搜索调用 ID。A 组仅凭这些引用无法把链接可靠地分给两次搜索。B、C 组各自的 20 个来源网址与同一响应的 20 条带标题引用按原始网址指纹全部匹配，各组内两次搜索的网址交集均为零。C 组两个搜索项在序号 22、24 完成，标题引用在序号 57–76 到达。这一时序允许先显示链接、随后更新标题。[逐次 URL 与引用指纹](references/minimax-native-search-sources-20261124.json) · [MiniMax 官方服务端工具说明](https://platform.minimax.cn/docs/guides/server-tools)

以上计数来自原始供应商流，先于 Host 的网址显示校验。网址与标题在取证时使用原始字符串的 SHA-256 前 96 位作指纹，按同一响应逐条核对。共计 3 次模型请求、6 次服务端搜索。供应商报告输入 43,741、输出 2,220 token。证据记录了三份本机回执的 SHA-256、输入差异、字段集合、各次搜索和回答消息的 ID 指纹。

## 推荐实现

1. **在 Runtime 为 MiniMax 请求来源。** 在 `yijie-codex` 构造 Responses 请求时，对当前受管 MiniMax 提供方、模型 `MiniMax-M3` 且实际工具列表含原生 `web_search` 的请求，追加一次 `web_search_call.action.sources`。保留已有 `include`。更新原先期望 M3 排除该字段的用例，覆盖无搜索工具和其他模型。运行时继续把每个搜索项的原始 ID、动作、网址顺序投影到已有的 `WebSearchAction::Search.sources`。[请求逻辑](../../../../yijie-codex/.yijie/patches/chat-models/0006-native-web-search-sources.patch) · [M3 现有请求用例](../../../../yijie-codex/.yijie/patches/chat-models/0007-feat-164-kimi-k31-pro.patch)
2. **在供应商流解析时提取标题。** 从 `output_text.annotations` 中只取 `type=url_citation` 的原始网址和非空标题。当前 Runtime 的 `ContentItem::OutputText` 只建模正文，提取应发生在这一步之前。以单次供应商响应为范围，记录搜索项 ID、已有来源网址和其顺序。归属始终由该搜索自己的 `action.sources` 确定。只给完整原始网址相等的来源补标题。批次以回答完成项为准，终包用于补齐缺失的完成项，重复交付幂等处理。[流式解析入口](../../../../yijie-codex/codex-rs/codex-api/src/sse/responses.rs) · [现有正文数据结构](../../../../yijie-codex/codex-rs/protocol/src/models.rs)
3. **在原卡片上补标题。** 搜索项完成即发布真实网址。标题批次随已有的回答完成通知携带可选展示元数据，每条只包含目标搜索项 ID、已记录的网址与标题。仅从响应终包得到的新标题可随该轮的自然结束通知补交。Runtime 保存同一份展示元数据供 `thread/read` 重放，Host 与 Desktop Native 在原搜索项上应用，执行次数、顺序、持续时间和完成状态只取自原来的搜索事件。展示元数据独立于回传模型的输入。现有 Vue 组件即可显示标题、站点图标及可点击链接。[搜索历史构造器](../../../../yijie-codex/codex-rs/app-server-protocol/src/protocol/thread_history.rs) · [Host 来源投影](../../../../yijie-agent-host/internal/session/native_process.go) · [Desktop 搜索卡片](../../../../yijie-desktop/src/components/chat/ChatWebSearchItem.vue)
4. **约束标题更新的范围。** 原来源已有标题时优先使用原值。若同一响应内一个网址有多个互相冲突的标题，或没有匹配引用，该行继续显示网址。若两个搜索项各自确实列出了同一网址，两项均可采用其无冲突标题。未列入任何搜索项的回答引用单独属于回答。跨响应、跨会话和同域不同网址分别匹配。沿用 Host 已有的地址校验、来源数量边界、标题过滤和项内去重，Native 打开链接继续核验该会话、轮次、原搜索项与完整网址的关系。[来源归属与打开规则](../../../../yijie-desktop/src-tauri/src/chat/ipc/web_sources.rs)

## 实施顺序、兼容与验收

本次验证与文档的 `contract-impact = none`，产品的 Desktop、Host、Runtime 接口和本地历史格式均未改动。拟实施方案的 `contract-impact = semantic`，会改变已有 M3 搜索的可见元数据和重放行为。先固定 Runtime 协议候选与现有来源结构，再为标题补充元数据做版本化兼容，更新 Contracts 投影和 Host、Desktop Native 消费端，最后启用发送端。旧读者只接收它支持的字段，旧记录继续按当时保存的证据显示。回退时关闭 M3 的新请求与标题发送，保留新格式的读取能力。[契约变更规范](../../dev/contract-first.md)

| 验收场景 | 可判定结果 |
|---|---|
| 同一响应执行两次不同搜索 | 保留两个原生 ID。搜索完成即可展开，每项展示的链接与该 ID 的供应商来源经过现有 Host 校验后的结果逐条一致。 |
| 标题晚到，重复收到完成项或终包 | 匹配到的标题在原行更新一次。展开状态和滚动位置保留，搜索次数和历史顺序稳定。 |
| 来源没有标题、同一网址跨搜索出现、同名标题指向不同网址 | 分别按真实网址归属。缺标题时显示网址，重复标题也不会将不同页面合并。 |
| 搜索完成后正常取消、缺引用或流式响应不完整 | 已确认的来源仍可见，取消与部分完成遵循原状态。未取得网址的记录继续使用现有空态。 |
| 重开同一会话 | 实时、落盘重开、`thread/read` 三处的搜索 ID、网址与标题一致。来源链接打开可追溯到相同搜索项。 |
| Kimi、旧 MiniMax 历史及其他网页动作 | 重放已有 Kimi 天气记录检查原有标题与交互。旧 M3 商品记录按已存的两条空态展示。阅读网页仍显示对应的打开动作。 |

接入后用脱敏的真实数据做定向回放，再在日常 Desktop 中执行一次新的 M3 双查询，核对录制字段、展开列表、图标回退、打开目的地与重开结果。供应商返回的 10 条是本次样本值，产品验收应与每次实际允许展示的来源集合比较。两轮真实执行结果和达到大批次边界后的修正已记录在交付报告中。
