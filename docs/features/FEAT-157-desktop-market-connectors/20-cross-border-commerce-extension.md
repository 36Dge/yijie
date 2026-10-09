# FEAT-157 跨境电商扩展

2026-10-08。用户明确要求沿用连接器设计，新增“跨境电商”分类及PDF列出的9个应用。本次是已交付49项之后的新扩展，旧D4/Git记录保留原范围与构建事实。

## 来源与当前事实

已阅读PDF两页；第二页空白，第一页嵌入表格右侧被源图片裁切，不能从缺失列推测认证。九个应用及MCP URL清晰可读；认证以供应商官方文档补全。九个SVG来自用户指定目录，只复制到项目资产，不修改原文件。

现有市场按目录categoryId分组，可直接复用卡片、详情、搜索、安装列表、聊天入口与标签。Native/Go/worker有49项断言，默认worker状态入口残留revision1/51；公共快照与选集上限51。必须源先行同步契约、注册表与执行消费者，不能只增加卡片。

## 设计与范围

- 活动目录58项、7分类；“跨境电商”9项按PDF顺序置于电商零售之后；原49项ID/凭据别名/安装记录不变。
- 领星ERP使用固定X-Mcp-Key；Sif使用官方明确支持的secret-key URL查询认证，秘密只在已有HTTP发送层加入；Pangolinfo和Sorftime使用Authorization Bearer；卖家精灵使用secret-key Header。
- Keepa、DataHawk、Seller Labs复用现有OAuth发现、Codex Keyring、正常取消、逐次审批；不运行第三方本地包。
- Shopify经Owner明确选择Global Catalog，按当前官方keyless Catalog与UCP profile协议适配三个公开商品工具；不接单店铺、购物车或订单。
- Owner明确要求Sorftime新使用全部进入FEAT-157；新配置表单和通用发现/拒绝/单次批准本地回归通过后，退役旧启动密钥输入、环境传递、专用发现和执行批准分支。保留原生历史读取/展示、通用线程操作锁和旧受管配置迁移识别。旧凭据与批准不迁移为新执行权限；旧permission-scope接口仅返回未激活，不重启Runtime。
- 安装仍无网络，启用前完整发现；异常/取消/未知及清理状态沿用。仅请求批准模式可执行，失败不自动重发，秘密不经IPC/模型/日志。

## 契约及兼容

contract-impact = breaking：新增封闭CategoryId、可能新增keyless认证枚举及58项响应/选择，旧严格消费者不保证接受。先更新Contracts源和版本，再生成全部消费副本；Desktop UI/Native同包，Host和worker先准备后使用。旧有效49项消息仍被新消费者接受，旧安装和历史不需迁移；回退禁用新目录能力，保留已有历史兼容reader，不降级数据库。不会把本地候选当生产版本或运行发布。

## 验证与边界

逐项代码审计九个注册表、认证与图标映射；正常本地契约/Native/worker/UI测试验证58项快照、9项新分类、旧安装保留、无凭据误启用、审批与元数据适配。亮暗1180×760、搜索和详情用真实组件验证。用户此前明确无需逐项真实调用，仍沿用该约束；无剩余模型/业务额度，本扩展不调用真实账户、MCP元数据或业务工具，不为新9项伪造实连PASS。不自动继承上一轮已经执行完毕的Git提交推送授权。

当前：实现与本地验证完成；真实账户接入仍须用户按供应商要求配置。此次没有新增实连额度，不把本地验证表述为九家实连通过。

审计补缺：领星官方工具规模超过300，原通用256工具上限会使其完整发现失败。因此源先行将单服务/单选集上限调整为512，保留2MiB总schema、单schema64KiB、深度16和逐次审批限制；不截断工具目录，不放开无界列表。

## 最终实现与审计结果

| 应用 | 认证与实现 | 官方依据 |
| --- | --- | --- |
| 领星 ERP | 固定 X-Mcp-Key Header；完整发现；512项有界目录。 | [接入文档](https://www.lingxing.com/help/article/mcp) |
| Sif | secret-key 查询参数仅在实际 HTTP 发送时加入，控制面保持无凭据 URL。 | [接入文档](https://blog.sif.com/article/mcp-install/Sif-MCP安装文档) |
| Keepa | 标准 OAuth 发现与 Codex Keyring；需要供应商 API 订阅。 | [接入文档](https://keepa.com/api-docs/mcp.html) |
| Pangolinfo | Authorization Bearer 仅加一次前缀；固定 HTTPS 资源。 | [接入文档](https://docs.pangolinfo.com/en-help-center/mcp/amazon-insight/connect) |
| DataHawk | 标准 OAuth/PKCE，工作区权限以用户同意为准。 | [接入文档](https://docs.datahawk.co/help-center/modules/datahawkmcp/setup) |
| Seller Labs | 标准 OAuth 与官方5项 scope；未知读写均逐次审批。 | [接入文档](https://www.sellerlabs.com/knowledge-base/connecting-the-seller-labs-mcp-server-via-claude-code-app/) |
| Shopify MCP | 无密钥；仅三个 Global Catalog 工具；固定官方 UCP profile 在已审阅参数内。 | [接入文档](https://shopify.dev/docs/agents/catalog) |
| 卖家精灵 | 固定 secret-key Header 原值，无 Bearer 推断。 | [接入文档](https://open.sellersprite.com/mcp/16) |
| Sorftime | 固定 Authorization Bearer；新连接器配置/发现/选集/审批；旧专用执行路径退役。 | [接入文档](https://www.sorftime.com/en-US/mcp/Codex) |

Shopify资料存在版本差异：通用认证教程仍描述client_credentials与短期Bearer，当前Catalog概览明确keyless，并要求UCP Agent Profile。本实现采用Owner确认的固定Global Catalog及当前Catalog协议；配置固定公开profile URL，保留upstream完整schema约束，将meta约束作为交集，审批与执行使用同一冻结参数。不以隐藏后处理添加参数，不开放购物车/订单，也不创建单店铺域名输入。

Sorftime退役保留的是历史DTO/数据库格式/原生工具展示，以及精确旧受管配置的迁移识别；不再创建旧MCP配置，不再从启动环境取得Account-SK，不再发现或执行旧专用product_detail。旧permission-scope只返回inactive、无重启；旧elicitation直接decline，旧pending/approved记录没有决策按钮且Host决策拒绝。普通聊天、模型切换和计划草案改用同一个通用threadOperation锁。原生项目trust配置迁移及正常重启保持原字节；没有删除历史或降库。

实机补缺：首个标准App启动暴露renderer API仍有49项硬编码，从而拒绝58项快照。已改成读取同包目录的数量，更新客户端回归，并以标准App确认7分类共58项、“跨境电商”9项及Sorftime详情。不会仅以组件页面成功代替Native端到端目录验证。

## 实际验证

- Contracts五个market family普通定向测试：34通过；生成、跨仓复制、摘要检查通过。
- Connectors worker：59通过（含新Sorftime自有配置表单、通用发现/精确选集/拒绝/单次批准、Shopify完整参数约束、320工具目录及512上限）；Clippy无警告。Go目录race测试与vet通过。
- Desktop Native：40项连接器测试及2项旧原生历史测试通过。一次安装全部58项的内存数据库测试通过；Shopify无密钥不自动启用，不绕过实际连接检查；未配置Sorftime不能启用。
- Desktop前端专项：69通过，覆盖真实目录client解码、管理store、搜索/九图标、详情、旧工具与旧审批只读、启动器退役。另有旧MCP parser兼容测试通过；ESLint/类型检查及Vite构建通过。
- Host三包定向race测试、vet通过。固定原版构建的Runtime正常启动、三种权限配置、正常关闭重开与项目trust保留专项通过；不调用模型或外部MCP。
- 标准worker构建及未签名debug App使用canonical脚本；正常Cmd-Q退出后重建，无强杀。实际App可读取58项目录并搜索出跨境9项；未安装、授权或启用第三方账户。
- 1180×760亮暗主题、九图标、搜索和详情由生产组件配合明确标注的普通本地状态验证；另有标准App真实Native目录截图。截图在Desktop `.local/feat157-crossborder-visual/`，未把它们解释为供应商调用成功。

证据：`evidence/cross-border-20261008/verification.json`记录检查与构建摘要；Connectors `docs/market-cross-border-audit-2026-10-08.json`逐项记录九服务代码审计、认证与官方来源。

未执行：九家真实OAuth/Keyring账户写入、MCP远程发现、业务查询和新增模型轮次；原因是Owner限定真实验收仅Tushare，本轮也没有剩余调用额度。影响：可确认本地实现、协议和生命周期，不能保证当前账号开通状态或供应商实时schema。完整旧故障/攻击测试未执行，遵守长期安全条款；使用普通有界数据、原生读写与正常退出验证。既有49项D4和Git推送记录保持原范围，不改写为58项实连或新发布证据。本次尚未Git提交推送。

最后一次重建（仅包含已通过59项测试的512工具容量与生成消费同步）完成后，Mac已锁屏，CUA无法再检查该窗口；不要求解锁来阻塞代码交付。上文实机UI证据来自此前标准App构建，最终构建成功记录和容量回归单独记录，未冒称同构建再次实机通过。

## FastMoss分类调整与解锁后复验（2026-10-08）

Owner要求将FastMoss从行业数据移至跨境电商。`contract-impact = semantic`：仅调整非秘密目录的展示分类/顺序与对应说明，复用现有CategoryId；catalogRevision更新为7，跨境电商10项、行业数据16项、总数58项。服务ID、图标ID、认证、端点、已有安装与执行权限保持不变；无wire形状或数据库迁移。源目录更新后使用canonical脚本同步Desktop并重建worker/App。旧revision6证据保留为历史，本轮补充解锁后同构建窗口复验。

解锁后复验已完成：Go目录检查、17项client/组件回归、1项Native目录回归及canonical worker/App构建通过。同一新版App窗口确认“跨境电商10项、行业数据16项、总58项”，FastMoss搜索只落在跨境电商，详情文案正确；Sorftime统一详情、聊天连接器菜单及管理跳转正常。未安装/启用外部服务、未输入凭据、未发送模型请求。原锁屏导致的窗口复验缺项已关闭。原侧栏展开状态已恢复，App停留在跨境电商目录供查看。证据见`evidence/cross-border-20261008/fastmoss-window-recheck.json`，旧构建记录保持历史事实。

## Sorftime账号授权体验重新确认（2026-10-08）

Owner明确期望与Tushare一致：在Sorftime官方页面登录自己的账号→同意授权给易界→自动返回完成连接，而非填写MCP密钥。按该体验标准，当前Sorftime API Key方案不能视为这一项已完成；此前本地技术验收与“全部实现”表述须区分此条件。

本次只读检查：当前代码注册为api_key、Authorization Bearer，调用worker自有配置页；Tushare使用授权码/PKCE、官方issuer/授权/token/注册端点和Keyring，可复用客户端框架。Sorftime官方公开Codex与Claude Code教程仍说明先获取Account-SK并配置Bearer；未查到面向第三方应用的OAuth/委托授权文档。这仅是公开文档结论，不证明Sorftime不存在未公开的合作接口。来源：https://www.sorftime.com/zh-CN/mcp/Codex 、https://www.sorftime.com/zh-CN/mcp/ClaudeCode 、https://www.sorftime.com/en-US/mcp 。

实施前提：确认Sorftime是否提供第三方OAuth或等价的正式委托授权，及易界应用注册/回调/资源与scope要求；若支持，复用既有Codex OAuth与Keyring框架，保持逐次审批与旧批准隔离。不能仅把api_key枚举改成oauth，不能抓取网页登录Cookie或冒充官方授权，也不能把钥匙串保存包装成账号授权。若服务方仅支持Account-SK，只能简化真实密钥流程，不能满足免手工密钥的目标；不在未确认前擅自采用该替代方案。当前Header名称与Bearer格式是实现细节，不宜向普通用户暴露。

真实验收仍按Owner暂停指令暂停。本次未启动MCP连接/发现、OAuth登录、账户操作或模型/业务调用，仅查阅公开文档；未消耗已批准但暂停的本轮额度。

Owner后续提供的具体MCP介绍页已核查（`https://www.sorftime.com/zh-CN/mcp/index?tag=MjAxODA5MTMyMzIwMzU1NzAwMDE~`）：公开步骤仍是登录/激活→获取MCP地址和密钥→客户端配置；官方Codex教程使用Account-SK/Bearer，Claude Desktop使用key查询参数。Accio文档的“应用授权”是客户端菜单，实际步骤仍填写带key的MCP URL，不代表Sorftime开放OAuth。未找到应用注册、授权码回调、scope或令牌交换的正式公开协议；不能据此断言不存在未公开合作接口，也不能据此改为OAuth。公开资料核查未使用账户Cookie/密钥、未启动MCP连接或真实验收。证据：`evidence/sorftime-market-live-20261008/oauth-public-document-review.json`。
