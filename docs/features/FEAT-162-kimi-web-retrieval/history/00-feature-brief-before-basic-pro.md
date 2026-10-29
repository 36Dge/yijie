# FEAT-162 — Kimi Search / Fetch 完整实施方案

Profile：demo_fast · Exposure：local · 日期：2026-10-24（Asia/Shanghai）

状态：实施前方案。本文先于任何产品代码修改落盘；用户已要求“按建议接入，先落完整实施方案，然后执行”。Owner、技术负责人、Reviewer、发布负责人均为段成威。此授权覆盖本地实施与正常非破坏性验证，不等于真实付费调用、Git 提交推送、公开部署或发布授权。

## 1. 用户结果与范围

保留 Kimi Responses 原生搜索及现有来源展示。另在现有连接器市场新增一个 **Kimi 网页检索** 服务（serviceId `kimi-web`），经原有 MCP Gateway 暴露两个工具：

- `kimi_web_search`：按查询词返回可直接使用的标题、URL、摘要列表。
- `kimi_web_fetch`：按用户指定 URL 返回页面标题和 Markdown 正文。

用户追加授权目录容量可以增加 2 个：管理契约上限从 60 扩到 **62**；本次实际只新增一个连接器，目录从 revision 9 / 60 项更新为 revision 10 / **61 项**，一个服务包含两个工具并共用凭据，保留一个目录余位。

不实现无头浏览器、JavaScript 渲染控制、原始 HTML 输出、登录态网页、Search Pro、爬虫队列、知识库入库或自动递归抓取。不重建 Agent 循环，不修改 yijie-codex 源码、补丁、协议或 Runtime 二进制，不改原生 web_search 的启用策略及来源语义。

## 2. 已核实事实、假设与未知

| 类别 | 内容及影响 |
|---|---|
| Fact | 当前普通 Kimi 会话使用 kimi-k3/max、原生 Responses；原生搜索及 URL/title sources 已有实现和真实记录，不重复建设。 |
| Fact | Connectors worker 已有 ProviderBackend、私有 Broker、官方 rmcp Gateway、逐次审批、selection/lease、Keyring 与受管凭据页；REST 供应商可以适配到同一执行链。 |
| Fact | 市场 ServiceId/ToolName 是有界字符串，已有 http/api_key 分类；无需新增通用 transport/auth 枚举。目录旧 reader 上限60，新增61项会拒绝，整体按 breaking 处理。 |
| Fact | generic MCP backend 面向远程 MCP、默认未知风险 write，不适合伪装成 Kimi REST。应增加 Connectors 私有 REST backend，复用 Broker 审批而非重写 MCP。 |
| Fact | Kimi 官方独立 Search 接口返回 title/url/snippet 等；Fetch 返回 url/title/markdown，后者不保证可控 JS 渲染。 |
| Fact | 模型 Kimi key 属于 Host 的模型配置边界，不是 Connectors Keyring 连接；不自动读取、复制或继承。 |
| Fact | 本地参考专家只禁用 hosted web_search，现有市场选集仍可能显式提供外部工具；定时草拟关闭工具，定时执行不承载市场选集。 |
| Assumption | 用户采用已有市场安装、独立配置与显式选择流程；两个新工具沿当前非空选集 ask 权限模式使用，不新增自动批准。 |
| Unknown | 当前账户对 Search/Fetch 的实际权限、余额、目标页面可读取性，必须由授权后的真实调用确认；代码和基础连接检查不能证明。 |
| Conflict | 部分 AGENTS/README 仍描述旧目录数量或旧实现状态，计划依据当前源码/来源锁；不顺手重写无关历史文档。 |

初始 HEAD、branch、remote 与已有改动见 `evidence/workspace-before.json`。当前 Host/Desktop 存在会话清理及过程展示等既有修改；不覆盖、回滚或混入本需求。特别保留 runtime-chat-models 来源锁及其已有派生更改。

官方权威（2026-10-24 已读取，字节摘要见 `evidence/official-source-review.json`）：

- https://platform.kimi.com/docs/api/tools-search
- https://platform.kimi.com/docs/api/tools-fetch
- https://platform.kimi.com/docs/api/list-models
- https://platform.kimi.com/docs/api/responses

## 3. 完整用户流程与交互

1. 使用现有 canonical local/demo_fast 入口进入应用，市场显示“Kimi 网页检索”，描述说明“搜索标题/链接/摘要；读取指定网页正文；服务按次计费”。使用已有分类与组件，不新增页面布局。
2. 安装只保存原有非秘密安装状态，默认不启用，不产生搜索或抓取请求。
3. 用户点击配置，打开 Connectors 自有 loopback/nonce 安全页，输入 Kimi API Key；密钥由 worker 写入现有 Keyring，renderer、Host、Runtime 和 SQL 只持有不透明引用。表单不要求用户理解 HTTP Header。
4. 配置/启用时，用固定 `GET https://api.moonshot.cn/v1/models` 作基础连接检查，并加载本地 canonical 两工具 schema。该检查只证明此接口可达且接受凭据，不证明 Search/Fetch 余额、授权或结果；产品配置说明及验证记录明确此限制。不得用收费 Search/Fetch 自动探测。若当前官方规范或实际权限不支持该基础检查，则明确失败，不能将读到 Keyring 冒充已连接。
5. 用户启用后，在当前会话的连接器选择器选中它。复用冻结选集、安装 generation、工具 schema digest、Host grant 和 worker lease；空选集不提供新工具。
6. 模型按需要调用 Search 或 Fetch。原生搜索仍用于一般联网回答；工具说明明确仅在需要结构化列表或指定 URL 正文时使用，避免无理由重复搜索。工具可被兼容的已选模型使用，不把 REST 工具绑定为第二个 Kimi 模型循环。
7. 原有审批显示工具名、只读性质、按次费用提示及完整 query/limit 或 URL。每次批准只允许一次 HTTP 请求；拒绝不发送。继续保持当前市场工具仅 ask 模式可用。
8. 结果进入既有 MCP Item / 历史显示。URL 保持惰性文本，不额外预取；网页文本作为外部内容，不变成指令或权限。独立工具结果不混入原生 web_search sources，不自动成为逐句引用。
9. 停用/卸载复用正常撤权与清理；不删除历史、不重放过去搜索。应用重开读取原有安装及历史格式，须重新取得当前有效执行资格。

| 状态 | 用户行为与反馈 |
|---|---|
| idle | 未安装、已安装未配置、已配置未启用、已启用状态沿现有管理权威展示。 |
| loading | 配置、基础检查、调用分别使用原操作 busy；禁止重复提交；无模型“研究进度”伪造。 |
| success | Search 展示真实列表；Fetch 展示标题/URL/正文及截断标记；工具成功与整轮完成分开。 |
| empty | Search 的 results=[] 是成功空结果；Fetch 无正文是明确 no_content，不伪造空成功。 |
| error | 使用闭集安全错误与中文说明，不回显上游响应原文、请求头或秘密。 |
| retry | 只允许用户发起新的明确调用并重新批准；429/超时/未知结果均不自动重试。 |
| cancel | 关闭配置页、拒绝审批、取消在途请求各沿既有语义；发送后取消不承诺免计费，不把已取消结果冒充成功。 |

视觉沿既有亮暗主题、图标系统、焦点和最小窗口；优先复用本仓现有 Kimi 模型图标作为本地资产，不生成或远链加载新品牌图。

专家：不自动选新连接器、不修改 hosted-search disabled；沿已有显式市场选集与审批规则，用户显式选用即访问外部资料，不宣称纯本地来源。定时草拟和定时执行均不在本期接入范围，不从历史选集生成权限。

## 4. 技术方案与替代方案

推荐链路：

```text
Desktop 原有安装/Keyring配置入口/显式会话选集
  → Host 现有 selection/grant/原生审批适配
  → Connectors Broker/Gateway（现有 lease + 每次批准）
  → Connectors 私有 Kimi REST Backend
  → 固定 api.moonshot.cn /v1/tools/search 或 /v1/tools/fetch
  → canonical 归一化结果 → 原生 MCP Item → 模型与既有历史
```

在 `ProviderBackend` / 内部 Execution 中增加专用分支，工具注册、review、execute、available、revoke、close 接入已有生命周期。HTTP 初始方案复用固定 Codex 库公开接口；实施审查发现其底层 reqwest 默认允许协议级重试，因此采用文末审查修订：仅在 Connectors 直接引用锁中已有的同版 reqwest，显式禁用重试。不加新的 SDK、MCP transport、运行时进程或依赖版本升级。

| 备选 | 取舍 |
|---|---|
| 专用 REST Backend＋现有 Gateway（采用） | 保留统一审批/密钥/生命周期，明确供应商语义与结果 schema，改动集中。 |
| 将 REST 假作远端 MCP 接给 generic client | 协议不相同，需要额外桥接服务并误用发现/风险语义，增加维护，无必要。 |
| 改 Runtime 内建搜索或新 Agent 循环 | 用户明确排除；也会混淆原生搜索和应用结果，不采用。 |

## 5. 工具契约（实施冻结目标）

权威源新增 `yijie-contracts/compatibility/web-retrieval/` 独立工具 family；manifest、input/output JSON Schema、错误和预算同源。专用 generator 生成 Connectors 使用的描述/验证材料；不手写复制公共 DTO，不改 Tushare-only `market-provider.tool_profile`。MCP 公共名称固定为下表；Gateway 不额外换成另一组同名工具。

| 项目 | Search | Fetch |
|---|---|---|
| 工具名 | kimi_web_search | kimi_web_fetch |
| 输入 | query：非空字符串，最长2048字符；limit：可选整数1–20，默认5；拒绝未知字段 | url：必填 http/https URL，最长4096字符；拒绝未知字段 |
| 上游映射 | POST /v1/tools/search；text_query=query、limit=limit或5、timeout_seconds=10、include_content=false | POST /v1/tools/fetch；仅传原 URL |
| 成功输出 | `{results:[{title,url,snippet}],truncated}`；缺标题/摘要映射空串，URL不得编造 | `{url,title,markdown,truncated}`；正文保留原顺序，空白正文不算成功 |
| 空结果 | results=[]、truncated=false | 返回 no_content 错误 |
| 语义 | 不包含正文，不承诺搜索引擎总命中数或分页 | Markdown 正文，不承诺完整 HTML、图片下载或 JS 运行 |

两个工具输出均支持统一错误分支 `{error:{code,message}}`，MCP `isError=true`；成功 `isError=false`。错误闭集：`invalid_arguments`、`authentication_failed`、`permission_denied`、`rate_limited`、`timeout`、`unavailable`、`no_content`、`response_too_large`、`invalid_response`、`cancelled`。用户安全消息由本地映射，供应商任意错误正文不透传。HTTP 401/403/429/408/5xx 和 Fetch 404 按对应已核实语义映射；不能从未知错误推断没有网页或没有搜索结果。

MCP descriptor 使用同源 inputSchema/outputSchema；规范化结构同时提供 JSON 文本 content 和 structuredContent（若现有输出路径不消费后者，文本仍完整可读）。两个表示必须相同，且合计遵守既有 65536 字节预算。只读 `readOnlyHint=true`、`destructiveHint=false`；计费操作不承诺自动重试安全，`idempotentHint=false`；保留 `openWorldHint=true` 与每次审批。

## 6. 凭据、网络、容量与执行语义

- 服务端 API 地址在 Connectors 固定，API Key 只作为 `Authorization: Bearer` 发给该固定主机；不允许用户配置 base URL，不跟随重定向，不把 Key 发送给目标网页。
- Fetch 目标 URL 作为 Kimi API 的业务参数，本地不直接访问目标站点、不解析/执行网页脚本。校验协议、主机、无 userinfo/控制字符及既有秘密检测；明确本地/私有字面地址不进入该公开网页工具。沿供应商安全限制，不绕过登录或访问限制。
- 每个连接器执行串行，同一已批准调用只发送一次；等待串行锁后再次检查 lease、取消、deadline、参数与凭据有效性。重复回执不产生重复 HTTP。
- HTTP 总超时上限15秒，且不越过原审批/租约期限；Search 供应商 timeout_seconds=10。Fetch 超时如实显示，不通过无限延长或自动重试掩盖。
- 使用 streaming HTTP 读取，原始响应上限1 MiB；超限明确 response_too_large。下游整个 MCP 结果上限仍65536字节，计算 JSON 文本和 structuredContent 的实际序列化字节。
- 结果压缩不是摘要生成：保留原文 UTF-8 边界。Fetch 必要时截短 markdown 并设 truncated=true；Search 必要时裁剪过长摘要/列表尾部并设 truncated=true。不得截断 URL 成另一个链接，不编造缺失字段。即使最小必要元数据也超限时返回明确错误。
- 无自动业务重试、后台刷新、结果缓存、自动跟链接或第二个模型请求。每次重试重新批准；“只读”不等于“免费”。
- 复用 secret guard、结构验证与惰性文本输出；审计只记服务/工具/阶段/状态/计数/哈希和安全错误，不记密钥、完整查询、目标URL或网页正文。用户明确请求的工具结果仍按现有加密历史规则保存，不新增数据库或保留周期。
- 取消/revoke/close 复用 CancellationToken 与正常收尾；无强杀、无可执行替换、无权限故障、无攻击 fixture。无法正常结束即记录 STOP_PENDING 并停止相关步骤。

## 7. Contract First、兼容与仓库分工

整体 `contract-impact=breaking`：新工具本身为独立增量，但目录61项会被旧60项reader拒绝；扩容62与 REST provider 的资格语义须一起审查。用户已明确授权接入和增加2项容量；这不构成生产兼容或已发布版本的声明。

| 仓库 | 改动范围 |
|---|---|
| yijie-contracts | market-connectors family 0.5.0→0.6.0，上限62；五族来源锁级联；独立 web-retrieval v1 schema/manifest/generator/conformance；REST基础检查语义说明。 |
| yijie-connectors | revision10/61项目录、固定 kimi-web provider配置、专用REST backend、凭据页说明、Probe基础检查、Broker分支、同源tool材料、普通验证与标准worker构建。 |
| yijie-agent-host | 同步受影响生成reader/来源锁；保持原market grant/审批/循环；仅必要consumer conformance与合法构建摘要更新。 |
| yijie-desktop | 同步reader和目录；61项断言、Kimi本地图标、普通市场UI测试；沿标准构建更新候选回执，不改无关聊天展示。 |
| yijie-skills | 仅接受专家family对market-connectors的间接来源回执同步；专家内容、业务输出、技能包不改变。此依赖由标准App来源检查发现。 |
| yijie | 本方案、交付日志、验证证据与限制。 |
| yijie-codex | 不修改、不构建、不替换；仅核对已有固定Runtime。 |

技术依赖顺序（整个需求连续实施，不建立治理切片）：

1. 落盘本方案和Must AC，记录工作区及官方来源。
2. Contracts 源先行：management 62容量＋独立工具schema＋错误/安全/计费语义；生成并检查五族与工具材料。
3. 先同步Host/Desktop/Connectors可接受62项的reader，再追加61项目录与专用Backend。保持旧60项/已有记录可读；不向旧reader激活新目录。
4. Connectors完成 Keyring/基础Probe/审批/REST/结果/lifecycle；三个consumer沿现有生成入口同步。
5. focused普通测试、source-check、格式/lint/构建；代码审查后修复问题，不运行未筛选的全套测试。
6. 通过 canonical scripts 正规构建新worker和本地App，按内容地址保存产物；使用既有冻结脚本记录真实hash，不手改hash过门禁，不覆盖固定Runtime。
7. 本地UI非收费检查。代码及结果可审查后，如仍缺真实额度/凭据，再申请最小真实验收；完成授权后做同构建fresh run和正常重开。

旧→新：新reader接受旧60项及新61/62项；63项明确拒绝。单次选集上限58保持，不随目录扩大。DB migration=N/A，现有安装/历史记录格式不变。

回滚：先停用新连接器并正常撤销资格，再回到仍能读取现有记录的兼容reader；保留新安装记录与历史、Keyring和旧产物，不降库、不清空数据。旧60项reader不得承接61项目录。全部为 release:false 本地候选，Git提交/tag/公开发布另行授权。

## 8. Must 验收矩阵

| AC | 可判定标准 | 证据 |
|---|---|---|
| AC-001 | 方案先落盘；Runtime/原生搜索实现不变；一个连接器两个工具，目录61、容量62 | 文档时序、diff、Runtime status/hash |
| AC-002 | 两工具descriptor/input/output与Contracts一致，旧60/新61/62可读，63拒绝 | focused生成检查和跨语言conformance |
| AC-003 | 安装不收费调用，Keyring配置不泄漏，基础Probe与收费验证明确分开 | 普通provider测试、真实UI配置状态（需用户输入凭据） |
| AC-004 | 只提供选中且有效工具，ask逐次批准；拒绝零HTTP、停用后不再调用 | 既有Broker正常批准/拒绝/取消测试与真实拒绝流程 |
| AC-005 | Search返回title/url/snippet且空结果区别于错误；Fetch返回指定URL正文 | 同源结果验证、普通受控HTTP、授权后各一次真实结果 |
| AC-006 | 超时/错误/取消/容量限制可解释，不自动重试；截断显式、URL不改写 | 普通结果/状态映射与边界单测，不注入故障攻击 |
| AC-007 | 新工具与原生搜索共存，MCP结果/历史和正常重开沿原链路 | canonical App真实会话与历史验证 |
| AC-008 | 标准构建、来源检查、定向回归和diff审查通过，既有用户改动保留 | 实际日志、构建manifest、前后workspace证据 |

## 9. 验证方案与费用边界

本地验证：Contracts独立focused generators和对应JS/Go/Rust；Connectors新backend普通schema/请求映射/响应解析/大小截断/取消测试；使用进程内受控HttpClient或正常loopback服务，无真实凭据。Host已有Broker正常生命周期/选集门禁；Desktop目录decode/市场/详情/选择/图标和Native正常测试；按实际依赖运行格式、lint、source-check与标准构建。

不能直接运行包含危险归档、恶意fixture或故障注入的默认全套generate/test。优先已存在的safe/focused入口；跳过项目、原因和影响逐项记录。普通错误码映射直接测试纯函数/普通响应结构，不强杀、不破坏权限、不注入攻击资源。

真实验收拟定最小范围：一次Search、一条公开官方文档URL的Fetch、一次审批拒绝（应零业务请求）、同构建正常重开；如需模型驱动，另计最多2个用户回合及其HTTP请求上限。**当前真实模型/供应商收费调用授权额度为0**，不转用任何旧Feature额度，不自动读取模型密钥。实施与本地验证先完成；到真实验收前提供具体构建、用例、费用上限请求与安全凭据入口。

D4只有同构建真实fresh run与Must AC均有证据后才能PASS。mock/编译/基础models检查不能替代真实Search/Fetch。若等待额度或用户凭据，明确记录“本地实现/验证完成，真实验收NOT RUN”，不得宣称整体已完成。

## 10. 自检、时间盒与交付物

本方案已覆盖主流程、空/错/取消/重试/并发/恢复、权限/秘密/审计、费用、契约、兼容、容量和回滚。无数据库/Runtime/浏览器/后台Agent扩建。工具结果与原生搜索来源保持真实语义；无数据不编造。

30分钟无新事实则扩大链路诊断；90分钟同一核心阻塞则简化非核心实现；非核心验证120分钟登记限制；核心240分钟仍不可用则报告单个关键阻塞与方案；总16小时停止扩建并重新定范围。不通过反复付费重试或伪造通过完成验收。

交付：本文件、`feature.yaml`、`01-delivery-log.md`、`02-verification.md`、实际source/test/build/diff证据，以及相关仓库可审查的未提交更改。未获明确授权不commit/push/tag。

## 11. 实施中审查修订（2026-10-24，修订先于对应代码）

独立审查发现：固定 `codex-rs/exec-server/src/client/reqwest_http_client.rs` 的客户端仅配置timeout/redirect，未关闭底层重试；锁定 reqwest 0.12.28 的 `retry.rs` 默认允许最多2次协议NACK重试。因此，单次Broker许可不能保证传输层不重发。

为满足已经确定的“一次批准、一次HTTP、无自动重试”，Connectors worker直接声明现有锁内 `reqwest = =0.12.28`，使用专用客户端显式 `.retry(reqwest::retry::never())`、禁重定向、固定HTTPS API、原超时和流读取上限。不是升级或下载新SDK；只允许worker包依赖清单增加该已存在依赖，外部依赖版本/checksum集合必须与原锁一致并通过既有source checker。Codex源码/Runtime不修改。验证用静态策略审查及普通HTTP成功流程，不构造HTTP2故障或攻击注入。

另有原Node同步formatter通过socket stdin等待EOF的问题：定向改用正规临时文件作为真实rustfmt/gofmt的stdin，生成结果逐字节比较相同。没有替换可执行程序、跳过格式化或改生成结果。旧等待进程无可用正常退出通路，保留STOP_PENDING，不强杀；修订后的检查正常完成。

标准App构建检查进一步发现专家family间接记录market-connectors源摘要。应经canonical生成/同步更新experts来源锁及Desktop/Host/Skills回执；11项专家业务生成输出逐字节不变。原五族之外的该来源依赖计入本需求，不改变专家内容、工具选择策略或技能资产。

专家资源消费者另固定了上述Contracts来源锁与producer authority。为完成同一标准App装配，增加显式local-only来源刷新入口：验证原manifest/authority及全部既有archive，使用现有Skills正规打包器生成新的来源证据；必须证明全部skills元信息、archive内容、内容审查和本地使用授权不变，才从真实producer输出生成新的消费pin。仍执行原完整schema/retained-resources/ordinary38库存/授权/文件核对并正常安装资源。失败不通过手改hash或关闭检查处理，不改专家正文、版本或权限，不触发模型或平台请求。

### 恢复后的启动修复补充（先于对应代码）

用户于2026-10-24恢复，明确要求修复本地服务未就绪并完成连接器UI，真实收费调用继续禁止。只读核对确认Host仍以旧 `ReviewedExpertCatalogDigest` 校验已正规刷新后的专家manifest；现有freeze记录Host源文件字节，但未核对Host与资源pin是否一致。当前修复范围仅为补齐这一既有部署来源消费链：从通过原完整资产校验的canonical pin确定性生成Host编译期常量（保留严格`VerifyExpertCandidate`校验），增加显式本地同步/只读检查入口，将一致性检查接入标准freeze/build。不得接受renderer或运行时环境传入的任意摘要，不手改常量绕过来源验证，不改变资源内容/授权、Host业务协议、Agent循环或Runtime。

验证采用当前真实本地资源的正常加载/Host资格校验、必要定向回归及canonical App重构，使用正常启动/退出与无密钥配置取消验收。先保留旧pin拒绝当前资源的真实失败证据，再验证正规同步后的通过；不注入损坏资源或恶意fixture。若修正此遗漏后仍未就绪，继续基于真实观察定位，不提前宣称根因闭环。
