# 第三组：TikTok 店铺运营专家与出海匠接入

2026-10-16（Asia/Shanghai）。本轮完整复核17原审计、执行/打包/内容笔记及18—21前两组结果。用户随后说明没有出海匠/LinkFox账号，明确要求“做接入与接入后做深入完整代码审计，对于真实验证现跳过”。本轮据此完成工程接入、代码审计与正常本地测试；真实授权、店铺数据、模型质量、付费业务和客户端业务验收均NOT RUN，不计D4。

## 范围与决定

下一组先做TikTok店铺运营专家。该专家原包8文件，店铺诊断有官方标准MCP/OAuth入口，能直接沿现有连接器发现/资格/显式启用/选择/逐次审批链；LinkFox媒体异步生成、1688多源找货与行业研究的搜索/数据依赖继续后置，不用咨询文本冒称已生成媒体或已查询货源。

重新核对剩余五位179份文件：WorkBuddy源、导出副本、既有摘要全部一致，原目录无清单外新增文件。未读取任何凭据、执行源脚本或搬运WorkBuddy认证。

官方公开发现（无凭据GET、无DCR/业务调用）已确认出海匠资源`https://mcp.gateway.chuhaijiang.com/mcp/oauth`；受保护资源元数据给出授权服务器，授权元数据支持DCR、PKCE S256、authorization_code/refresh_token、公开客户端token_endpoint_auth_method=none。当前仅声明`mcp.full`，不能伪称供应商授予只读scope；易界继续逐次批准具体工具/参数，供应商账号授权另行由用户完成。公开GET资源返回405，不当作MCP故障；标准well-known两页返回200。依据：https://developer.chuhaijiang.com/getting-started 及证据根public metadata JSON。

## 契约与兼容

`contract-impact=breaking`：新增第59项目录会超过旧消费者Snapshot的58项容量。沿当前本地候选源优先流程扩大目录/安装快照上限，先生成并验证所有受影响reader，再同步新目录；保留现有58项逐字段原值，不绕过验证。每轮连接器选择上限仍58，不需要为59项目录改变选择摘要格式/排序或历史引用。旧消费者不得与新目录混装；回退保留兼容reader与所有已有专家精确包，不能直接退回旧58容量构建。

源权威不变：Contracts定义跨仓快照约束；Connectors拥有固定目录与provider注册；Skills拥有专家资源；Host/Native消费精确摘要。仅本地未发布候选，不改Runtime、OAuth实现、Keyring、权限、审批、SQL35/Host10、outbox或数据库schema。无新增SDK/网络代理/业务数据库。不修改已安装资源或用户历史；旧47资产及原9ExpertRef保持。

## 实现方案与可检查条件

1. 新增出海匠固定HTTP/OAuth注册和跨境电商目录项，使用现有标准发现、受控浏览器授权、Keyring及schema冻结。默认unverified/provider_onboarding_required；不自动授权、探测账号或启用。
2. 单一TikTok专家ROLE/SKILL入口，分别说明自有卖家诊断与用户报表分析；地区/卖家身份/时间/时区/币种/口径必须明确，未知不补0、不猜因果。实时订单与T-2分析不可直接相减；工具schema不由原包示例替代。
3. 本地Python标准库辅助处理明确列结构的用户合成报表；新输出不覆盖输入和旧版本。缺关键字段/日期、币种或口径不一致应明确失败或分组，不制造诊断。
4. 专家与连接器独立选择；资源已准备不表示账号/卖家授权成功。缺服务给出易界连接器入口，禁止搬用WorkBuddy工具/凭据、切full、直接shell联网或自动重发可能计费请求。
5. 只读经营诊断为本组业务目标；发布/评论/私信/删除/解绑不在此轮执行验收。现有通用工具审批和destructive拒绝保持，不用ROLE代替机器权限。
6. 全部新增资源单独版本/来源审校/本地使用依据；现有真实专家与头像/三列组件复用，替换同ID展示项，不添加专家团。
7. 正常本地用例覆盖来源、旧资产保留、目录/安装/选择、schema与历史摘要、OAuth配置与普通协议、金额口径/缺失/真实零，以及UI的资源/服务状态。对新改动做独立一轮完整代码审计，发现问题先修复再复验。
8. Desktop全量lint及受影响仓lint、生成一致性和安全focused测试通过；禁止攻击fixture、故障注入、强杀、权限破坏或运行时劫持，未执行项明确记录。

证据根：`yijie-desktop/.local/third-group-experts-20261016/`。基线保存各仓HEAD/分支/远端/status/diff；旧未提交修改全部保留。真实验证按用户指令跳过，不创建新模型任务/外部账号授权/店铺请求。结果与限制如下。

## 实现结果与逐层代码审计

本轮新增 **TikTok店铺运营专家 0.1.0** 和固定 **出海匠** provider。项目源码目录现在是7位走原生专家架构的专家（原京东+第一组3位+第二组2位+本轮1位），另4位仍为明确的展示卡；总数11，无专家团。未把展示卡状态伪造为已接入，Native旧目录或读取失败时也不合成新专家。剩余4位为亚马逊1688找货源、人台换模特图、爆款视频复刻及市场研究专家，继续等待后续组次。

本组14份运行资源来自重新审阅的8份原包资料，ROLE、任务索引、5份参考、检查表、评测、示例及一个标准库报表脚本沿单一ExpertRef打包。没有搬用WorkBuddy提示词执行入口、依赖安装器、认证或远端调用脚本。资源包当前48项：38普通Skills+10个专家版本；旧47项完整保留。出海匠只增加固定注册和目录，OAuth/Keyring/Native状态机/Host/Broker/Runtime主干均复用。

| 审计面 | 结论与处理 |
| --- | --- |
| 权威源与容量 | 从Contracts只改变Snapshot目录及安装数组58→59，选择上限58保持；Native/Host/worker派生物全由canonical生成同步。复审修复worker启动仍使用revision7/58的遗漏，Native回归断言同步revision8/59。 |
| 真实目录与界面 | TikTok从展示数组移到受管资源目录，原头像复用；详情/参考问题/资源准备沿现有客户端。参考问题只预填，不能自动发消息或绑定。 |
| 资源注入与权限 | v3明确约束包的capabilities为filesystem=read/network=none，表示受控读取角色资源，不是脚本或服务调用许可。复审过程中尝试把执行用途写入该字段被原schema正确拒绝，已按原架构恢复；联网、输出文件及收费边界在ROLE/参考/risk中如实说明，不修改schema放行。 |
| 连接器选择与店铺授权 | 专家安装、出海匠账号授权、卖家店铺授权、当前会话选择、工具资格及逐次批准互相独立。新安装无凭据、未连接、未启用；未授权不能直接启用。无自动连接、全局Skill投影或权限升级。 |
| OAuth来源与凭据 | 固定官方HTTPS资源、mcp.full、标准发现/DCR/PKCE/Keyring；无自创endpoint、明文token、WorkBuddy凭据或授权URL来源。保留严格issuer一致性。公开元数据实质阻塞见下节。 |
| 工具执行边界 | 沿generic现有完整schema冻结与服务隔离、参数校验和逐次审批；未知风险按write请求批准，destructive仍拒绝；不自动重发未知结果。ROLE的只读诊断目标不冒称机器scope变为只读。 |
| 事实与计算 | 明确单店、来源、日期、IANA时区、币种、数据可用日及口径；Decimal核算，不把缺失变零，不算零基数增长，不跨期间/币种/口径混比。退款事件日与原订单cohort分开，未确认cohort不输出退款率。输出保留原输入字节及摘要，新目录不覆盖已有文件。脚本不证明用户来源真实性。 |
| 历史与恢复 | 原安装器、journal、精确版本引用、撤销/移除保护、正常重开与历史回执复用；旧9个专家版本与新版本并存。没有SQLCipher/Host schema变化，没有打开日常数据库或改写收据。 |
| 内容中的开发状态 | 移除运行SKILL中“用户本轮仅授权代码审计”的开发时指令；本轮验证限制在交付记录和明确日期的来源说明中记录，不把此次开发对话当未来用户的业务权限。 |
| 生成器等待 | 最终复跑定位scheduled IPC生成器的rustfmt等待stdin EOF。一次正常SIGINT中断本任务检查组（exit130），没有SIGKILL、产品进程操作或故障制造。改为普通临时文件作为stdin，rustfmt命令/cwd/格式规则保持；canonical重新生成仅更新生成器来源摘要，7个派生文件逐字节不变。完整lint复验通过。 |

这是一轮逐层源代码、既有调用链及正常执行测试复核，不宣称模型质量或供应商服务已经验证。下述外部阻塞仍然成立。

## 出海匠授权的具体阻塞

2026-10-16匿名GET公开metadata得到：

- 受保护资源 `authorization_servers[0]` 为 `https://openapi.gateway.chuhaijiang.com/`。
- 授权服务器 `issuer` 为 `https://openapi.gateway.chuhaijiang.com`。
- 末尾斜杠不同；现有 `oauth_policy.rs::validate_metadata` 的精确字符串比较返回InvalidMetadata，注册/token POST许可仍未开放。

[RFC 8414 §3.3](https://www.rfc-editor.org/rfc/rfc8414.html#section-3.3)要求issuer与用于构造metadata请求的issuer一致；不通过URL归一化、例外注册或放宽检查伪造成功。两项普通本地测试保留公开响应的实际差异并证明拒绝，以及一个独立普通合成服务的标准匹配路径。**真实OAuth没有执行，不能宣称已经成功或线上请求实际失败；已观察到的公开响应与当前代码结合可确定此发现路径不满足校验。**

专家详情、出海匠目录说明和参考流程已明确“授权元数据不一致，待服务方修正后验证”。服务方修正后仍需有账号的用户完成授权、卖家确认、工具发现和真实经营验收；本地报表模式不依赖该服务。未联系服务方、发送用户资料或创建账号。

## 最终验证

所有日志位于前述证据根，失败/中断记录保留，没有覆盖为PASS。

| 检查 | 最终结果与证据 |
| --- | --- |
| Desktop完整lint | PASS / exit0；`make lint CONTRACTS_DIR=.local/demo-fast-contracts`，完整generate:check、ESLint、vue-tsc、Rust fmt、all-targets Clippy，`desktop-lint-verified.log`。 |
| 历史来源与实际构建来源 | 历史Public/Host契约使用工程已有干净Contracts副本，仍校验canonical origin、固定完整Git对象/摘要。当前新增契约生成检查直接读取实际Contracts sibling；实际Host完整source snapshot、专家资源和既有权限链单独PASS，`host-source-freeze-final.log`、`current-canonical-preflight-verified.log`。未将历史副本冒称当前实现，也未改来源门禁。 |
| 生成器修复 | `generator-byte-preservation.json`证明7个生成物不变；原等待采样与正常中断单独保存。 |
| Skills | lint、25项测试、66条合成eval格式PASS（非模型评分），`skills-verified.log`；48项确定性打包、资源sync PASS。 |
| Host | lint及race测试PASS；10版本实际归档安装解析、原39项目录升级保留、10版本资源生命周期/绑定移除保护、3组版本共存，`host-verified.log`。普通进程内Runtime投影，不是模型实跑。 |
| Native | 4项PASS：真实48项包加载、7位最新专家目录与精确引用、59项目录、59项安装快照与新OAuth服务未授权不能启用；`native-verified.log`。仅临时/内存库。 |
| 界面 | 4文件76项PASS，含真实目录/展示卡分隔、详情、预填、资源准备、不可用与头像回退、连接器列表；`ui-verified.log`。 |
| Connectors | 完整Go lint、catalog race测试、既有worker-lint PASS；新增文件rustfmt额外检查PASS，`connectors-verified.log`。11项普通worker测试PASS，覆盖固定注册、请求header、精确issuer、PKCE本地回调、正常取消与owner退出及凭据身份隔离，`worker-normal-tests.log`。无真实账号。 |
| Contracts | 完整lint PASS（保留既有12条Redocly warning）；专项12项Node、Go、6项Rust及Clippy PASS，`contracts-lint.log`、`contracts-market-tests.log`；当前容量差异与双向兼容独立验证见`capacity-direction-compatibility.json`。 |
| 前端构建/元仓 | `pnpm build` PASS，`desktop-build.log`；元仓lint及50项测试PASS，`meta-checks.log`；7仓diff空白检查PASS。 |

### 兼容性检查的明确限制

全局 `scripts/check-breaking.sh` 对已发布f16a497、Native 6f632f1/811f38d三个完整基线PASS。对FEAT-157 fallback 1a213ac、FEAT-158 fallback 35e0949、当前增量e35ae9a均在既有scheduled-plan-draft远程schema引用解析EOF处exit102；与工程2026-10-07已有记录一致，未更改脚本忽略该项。随后独立执行这些基线的Buf、AsyncAPI、JSON Schema各9项均PASS，**不替代未完成的全局检查**。详情`breaking-results.json`、`blocked-baseline-component-results.json`。

本次market family源码相对e35ae9a的精确差异只有version与2个maxItems；专项实测旧58快照被新reader接受、新59快照被旧reader拒绝/新reader接受、60条被拒绝。故明确按breaking本地候选同步全部reader，不做发布或旧客户端混装；不是“全局兼容已通过”。

## 保留证明与未执行项

`resource-preservation.json`：旧47项元数据与归档逐项逐字节相同；原58个连接器及58个provider注册逐字段不变；当前已安装9个专家版本的内容仍与旧固定归档完全相同，原基线9份Runtime历史及110份专家内容/收据文件无变化（排除活动数据库操作日志）。没有日常数据库逐行审计的新结论，因为本轮没有打开数据库；原数据库历史结论沿用21，未伪称重新验证。

`final-source-state.json`：7仓HEAD、分支、origin均未变，Runtime工作区保持干净。既有未提交工作保留；没有commit/push/tag/签名/发布。本轮只构建前端并编译检查源码/测试，未重建或替换运行中的App、Host或Runtime，没有启动新产品进程、安装新专家到日常用户目录或发送模型请求。新组的客户端实际使用与App重建实跑留待后续明确验证。

按用户最新指令，真实出海匠/LinkFox账号授权、卖家绑定、MCP工具发现与业务查询、收费调用、模型输出质量、实际客户端端到端及D4均 **NOT RUN**。未运行含攻击fixture/故障注入/强杀/权限破坏的历史全库测试；以上正常用例与全量lint不扩大为全库或真实业务PASS。

结论：本组工程接入、正常本地功能测试与代码审计完成；真实服务可用性尚未验收，出海匠公开授权元数据存在具体阻塞，4位后续专家继续保留展示状态。

最终本地包manifest：`95e145ad2e0b55f81b23bdbf0a84033a51cf38a699a2e79851247850a3d113e9`；authority：`5330b4f864eec7dd8b89df96594539163e5fb2d996705a9e14b88c22c5436816`。本地bundle版本0.7.0，非发行版本。
