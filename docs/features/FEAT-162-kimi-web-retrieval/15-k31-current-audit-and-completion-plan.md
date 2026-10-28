# FEAT-162 当前状态、K3.1 Pro影响与继续完成方案

日期：2026-10-28，Asia/Shanghai。状态：AUDITED / COMPLETION_PLAN_PROPOSED。本轮只审阅对话要求、需求包、当前与保全源码、既有验收和公开官方资料，未实施产品修改、启动App、读取Key值、打开业务数据库或调用收费接口。

## 结论

Search/Fetch曾经完成本地候选实现，并在2026-10-24通过真实产品worker的Search一次、Fetch一次和拒绝零请求验证；真实客户端模型驱动的完整对话尚未验收。2026-10-28当前日常源码及制品采用FEAT-164已审基线，**未包含FEAT-162实现**；相关代码完整保存在各仓`retained/primary-wip-20261028-01`，不是因K3退役而不可恢复，也不能说当前客户端已经可用。

推荐继续方式是：**保留当前K3.1 Pro及r5 Runtime，选择性整合已有FEAT-162源码，修正契约/来源衔接，补齐新模型真实对话验收。无需从头重写Search/Fetch，不重新建设Agent循环，不为本需求修改Codex内核或补丁。**

本轮增量contract-impact=none，仅文档/只读证据；后续恢复仍按原FEAT-162最高breaking影响审查，不能把旧通过记录当作当前消费者兼容批准。

## 1. 对话要求和历史完成程度

需求先从能力调查收敛为：保留原生搜索，在现有Connectors/MCP链增加Search Basic和Fetch；目录上限60→62获授权；一个`kimi-web`服务、两个工具；暂不做无头浏览器。之后用户先要求复用模型Key，再明确无需本地绑定、重复配置或启用，直接自动复用客户端已有Kimi凭据。早期独立Keyring配置、/models探测、已配置未启用流程均已被后续决定替代，不应恢复。

自动准备不等于自动批准收费操作：仍保留当前任务选用和现有逐次审批；新安装客户端也必须已有可用Kimi模型凭据，不把个人Key打入安装包。Fetch本期返回Markdown正文，原始HTML、登录态、可控JS渲染及爬虫不在已确认范围。

| 内容 | 2026-10-24实际完成程度 | 证据与限制 |
|---|---|---|
| 两项工具及契约 | 已实现 | Search返回title/url/snippet，Fetch返回url/title/markdown及截断标记；同源schema、错误、容量等已实现 |
| 现有执行链 | 已接入 | 使用现有Provider/Broker/Gateway、选集/租约/审批；无新Agent循环 |
| 凭据直接复用 | 已实现并实际UI验证 | 原Host加载的Key快照经匿名FD3交给worker；默认本地准备，无独立安装/配置/启用，无/models探测 |
| 单次发送与安全行为 | 本地定向验证及真实拒绝通过 | 固定Kimi端点，禁止重定向/自动重试，有界正文；拒绝后供应商0请求；未做禁止的故障/攻击测试 |
| 实际Search | PASS | 1次HTTP200，3条标题/URL/摘要，未截断 |
| 实际Fetch | PASS | 1次HTTP200，IANA Example Domains，751字符Markdown，未截断 |
| 模型自动选工具→UI审批→结果回传→答案 | NOT RUN | 13号真实工具验收模型调用为0；不能说已用K3跑通完整对话 |
| 实际工具结果历史重开、原生搜索共存 | 未完成端到端确认 | 09号验证的是自动准备/开关/同构建重开，不是带Search/Fetch结果的真实对话历史 |
| 完整交付 | 未完成 | AC-004/007仍pending，D4未通过；14号仅提出端到端方案，未获本轮执行确认 |

真实工具核算费用为0.02元，依据成功次数与公开单价，未查询账单；该一次性额度已关闭。先前Go工具链、空SSE priming、progressToken问题均是验收驱动问题，已修复后通过，不是需要重写Kimi服务的证据。详见[09](09-direct-use-verification.md)、[13](13-search-fetch-live-verification.md)及其原始证据。

## 2. 当前源码和实际日常制品发生了什么变化

FEAT-164第[76号](../FEAT-164-kimi-k31-pro-migration/76-primary-workspace-execution.md)明确：完整保全未采纳WIP后，原主目录选择已验收的FEAT-164基线，不把其它需求一起激活；第[80号](../FEAT-164-kimi-k31-pro-migration/80-final-audit-and-feature-closure.md)关闭模型迁移范围，并明确FEAT-162/163独立。

本轮重新核对当前Git和源码，并验证日常generation `20261028-02`构建回执中的目录摘要等于当前目录文件：

| 核对项 | 当前活动基线 | 保全的FEAT-162实现 |
|---|---|---|
| 连接器目录 | revision9 / 60项，无kimi-web | revision11 / 61项，有kimi-web |
| 管理契约容量 | 60，family0.5.0 | 62，family0.7.0 |
| Provider/Broker契约 | 0.4.0 | 0.6.0，含模型凭据管道与本地准备语义 |
| web-retrieval工具契约 | 不存在 | 0.2.0，两个工具 |
| worker REST代码 | 无kimi_web.rs/model_credentials.rs | 两文件、生成工具材料及普通测试均存在 |
| Host凭据交接 | NewOwnerWithStorage，不交接Kimi模型快照 | NewOwnerWithModelCredential及FD3生命周期实现存在 |
| Native直接可用 | 无本期store_builtin实现、无Kimi目录入口 | 默认准备、UI及对应测试保留 |
| 旧真实验收脚本 | 当前源码中不存在 | 修复后的测试客户端与Go启动脚本保留 |

当前来源：Contracts `d5792d6`，Host `7309101`，Connectors `8e62101`，Desktop `24a231f`，Runtime `11fd450`/r5。Runtime当前SHA为`283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`；旧FEAT-162验证的Runtime与worker不是当前制品，不能直接沿用旧hash或回执。

可复用的保全引用（只读核对，不切分支、不恢复文件）：

| 仓库 | retained/primary-wip-20261028-01完整commit |
|---|---|
| Contracts | b28c9636d1a3a94cb549d5a09f291c6af9066785 |
| Host | fab200984bc9fa70870859a5e3a4f855a2cb1c94 |
| Connectors | d2d65c8e78e5d1c5d23c27d4de10181ef03a54b9 |
| Desktop | a0172399993e66555414b188e18c8d76b5e7a78a |
| Skills | 78bbfd119f261e735c55127332f446800bf34fb7 |

这些是混合工作保护提交，**不能整分支合并、整目录覆盖或把全部差异视为FEAT-162**。当前源与保全源的差异同时包含FEAT-164后续修复和其它工作，尤其不能退回旧历史writer、模型目录、停止流程或部署入口。

只读证据见[evidence/k31-current-source-audit-20261028.json](evidence/k31-current-source-audit-20261028.json)。本轮没有启动App，当前客户端行为结论来自活动源码及同源制品回执，不冒充新的UI实测。

## 3. K3换成K3.1 Pro的实际影响

### 工具核心：直接影响小

保全adapter的Search请求只传`text_query/limit/timeout_seconds/include_content`；Fetch只传`url`。两者不传`model`、profile或推理强度，不调用推理接口。2026-10-28官方[Search](https://platform.kimi.com/docs/api/tools-search)和[Fetch](https://platform.kimi.com/docs/api/tools-fetch)仍使用上述独立REST路径及MOONSHOT_API_KEY Bearer鉴权。模型名称改变不要求重写这两个HTTP适配器或另建专用Key。

原凭据交接也以Host的KimiAPIKey快照为源，不按kimi-k3字符串选Key。当前K3.1仍沿同一模型凭据加载器；应重新接回该来源，不能从旧配置复制Key、从历史恢复执行资格或建立第二份持久密钥。

### 模型驱动与集成：必须重新验证

活动profile已为`kimi-k3-1-pro-max-v1`、实际model为`kimi-k3.1-pro`，旧K3只保留历史语义。K3.1支持工具调用，FEAT-164第[53号](../FEAT-164-kimi-k31-pro-migration/53-real-functional-results-and-search-source-fix-plan.md)已有真实function_call→function_call_output→答案的证据，但工具是只读文件命令，不能替代这两个MCP工具的验收。官方能力说明见[K3.1 Pro](https://platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart)。

因此需要核对新profile选集准入、MCP工具可见性、原生审批关联、参数、结果回灌、正常终态和历史保存；保留当前Kimi激活/暂停及旧K3禁发规则。工具可用性与模型是否触发调用必须分开，不因HTTP接口正常就断言模型一定调用。

FEAT-164还独立验证/修复了原生web_search sources传递，但把“搜索答案正确性/指定页面命中”移出了其范围。这既不证明FEAT-162完成，也不取消用户在本需求要求的结构化Search与指定URL Fetch。后续只验收本需求固定场景的工具输出和回答依据，不重开FEAT-164的泛化搜索质量项目。

### 旧方案与记录：必须刷新

14号方案中的kimi-k3、旧Runtime/来源、旧App启动方式和Host chat-model-smoke-meter.py不再适合作为直接执行清单。该旧meter仍硬编码kimi-k3；新基线已有K3.1专用计量入口，应评估复用其计量机制，但不能复用FEAT-164授权/台账或覆盖其历史预占。

当前K3.1公开输入/输出单价为13/68元每百万token，已不同于旧K3；Search Basic和Fetch仍各0.01元/成功次。参考[官方模型价格](https://platform.kimi.com/)及[工具计价](https://platform.kimi.com/docs/pricing/websearch)。旧14号的5元是未确认的条件预算，完整输入上界门禁仍未完成，不得称其已保证。

此外，保全`compatibility/web-retrieval/tools.json`的`semantics.credentials`仍写“独立Keyring”，与同文件qualification、Broker契约、已实现FD3及用户最终要求冲突。这是应先修正的源契约说明残留，不是模型升级造成的新故障。

## 4. 推荐继续完成方案

三种路径比较：整包恢复旧工作会回退/混入其它功能，不采用；重新编写全部工具会重复已有实现与验证，不采用；**以当前已审基线为基础选择性整合并补验收，采用**。

### 第一步：冻结本需求差异，先更新源契约

- 从上述保全commit提取FEAT-162相关路径和代码段清单，逐项对照当前源。只恢复两个工具、对应凭据交接、目录和直接准备流程，排除其它需求WIP。
- 在当前Contracts上恢复web-retrieval、容量62、not_configured及既有模型凭据交接语义；统一修正独立Keyring旧文案。保留当前K3.1 profile、旧历史兼容、审批与FEAT-164修复。
- 先确定当前版本和consumer依赖，再通过canonical generator同步；不能直接复制旧生成文件、来源锁和hash。Skills仅更新必要的间接来源，专家内容不变。
- 该恢复涉及旧reader容量及闭集错误兼容，沿原breaking计划验证，不能以“只是换模型”省略跨仓检查。

完成条件：可审查的精确差异清单、无需求混入、源语义无冲突、全部当前消费者仍保留K3.1准入能力。

### 第二步：恢复连接器装配，完成零收费验证

- Connectors复用既有REST adapter、固定两工具、无重试/重定向、有界结果及普通测试；适配当前固定库来源并用正规构建生成新worker，不覆盖旧内容地址产物。
- Host接回统一模型Key快照与匿名管道，核对当前进程代际和正常关闭；不改模型密钥配置，不允许旧历史/停用状态授予执行资格。
- Desktop恢复默认本地准备和任务选用：无需重新安装、填写、绑定或启用；缺Key明确提示统一模型配置，尊重显式停用/卸载；准备HTTP为0。
- 验证K3.1新对话能获得正确工具定义、ask批准/拒绝关联、空搜索、非空正文、普通错误映射、大小上限、正常取消/EOF。以普通合成值及受控本地响应完成，不使用攻击fixture、权限破坏、强杀或替身二进制。
- 在当前canonical primary流程建立新generation，复核Host专家摘要与worker来源，检查自动可用及正常重开。原generation20261028-02及数据保持；不得直接启动旧tauri候选覆盖日常制品，不重跑FEAT-164 D3或降库。后续日常激活须有新来源资格和对应绑定，不能刷新旧回执冒充。

完成条件：本期定向检查通过、K3.1身份及旧K3禁发不回归、准备和拒绝均0外部发送、无重复Key输入、Runtime核心/补丁不变。

### 第三步：更新最小真实端到端验收单，再确认执行

- 使用普通空白对话及现有K3.1 Pro/max、原Kimi Key，一条固定任务：Search IANA example domains（limit3），Fetch固定IANA网页，给出简短有来源的答案。
- 目标上限：模型HTTP最多3次（所有续推理/辅助调用计入）、Search最多1次、Fetch最多1次、重试0。把两项真实工具复验纳入这一次对话，不再额外先跑一套收费工具直验。
- 先沿现有计量组件完成独立FEAT-162台账及本地验证。继续以5元作为可讨论目标，但只有能在发送前证明完整输入/输出和所有付费入口受限时才提交该金额的执行单。当前FEAT-164 meter默认按1M上下文预留，不能仅修改model或金额就承诺5元；如无法合理收敛，向用户报告具体差额/约束后再定，不能带着未实现的硬上限发送。
- 供应商未触发工具、参数错、权限失败、超时、输出截断或次数触顶，均记本轮未通过并停止；不自动追问或重试。无关联网工具和辅助模型请求也必须纳入限额，不能只靠提示词约束。
- 从真实界面逐次批准，证明Search实际产生标题/URL/摘要，Fetch实际产生指定URL正文，模型收到两个对应输出并作答；不能用原生搜索来源卡、shell抓页或旧结果代替这两个工具。
- 正常退出、同构建重开，检查两项工具结果及答案仍在，无新增调用；再按新generation完成受控日常激活/正常退出核对。只在上述证据完整后关闭本需求对应未完成项。

本轮用户仅要求分析和后续方案，**未授权上述恢复实施或新增收费调用**。上一轮0.02元已关闭；14号5元未确认；FEAT-164的授权不转用。确认恢复方案后可先完成前两步；收费前提交当前模型/构建/次数/金额明确的验收单。

## 5. 完成定义与未覆盖项

本需求完成需同时成立：当前活动源码及新制品实际包含两工具；自动复用现有Key；正常准备无外部调用；真实K3.1对话中两工具参数/审批/结果/回灌/答案可追踪；拒绝零发送；失败不重试；重开历史无重放；原生搜索能力和当前模型迁移保护不回退。

已有09/13的历史PASS保留其日期和来源，重新验证项按新来源追加，不覆盖旧失败。无头浏览器/HTML、登录网页、递归抓取、定时任务自动接入、公开/签名分发及其它Feature验收不加入本次范围。当前不读取真实凭据值、不探测账户或服务、不将本轮静态审阅冒充执行通过。

本轮检查：活动七仓初始均干净；四仓核心保全引用及Skills引用可读；9个关键组件保全可定位；当前目录60项、无Kimi，摘要与日常回执一致；官方两个REST接口仍无model参数。所有模型/Search/Fetch新增请求均0。后续文档检查结果见恢复记录，不据此声称产品测试通过。
