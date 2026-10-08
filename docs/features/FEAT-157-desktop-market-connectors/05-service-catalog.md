# FEAT-157 — 51 项服务目录与来源核对

> 状态：设计候选，实施 pending。核对日期：2026-10-07（Asia/Shanghai）。Owner：段成威。
> 本文、JSON 及 manifest 只记录设计输入和审计结果，不是运行配置、授权或真实服务验收。

## 1. 范围、权威与事实边界

本次文档新增的 `contract-impact=none`：不改变产品代码、跨仓 wire、Runtime 配置或持久化/重放行为。后续连接器实现的契约影响、凭据边界与批准状态由本需求设计和 `feature.yaml` 独立管理；本文不预先批准架构变更。

- 来源：用户提供 `market_mcp_onboarding_51.md` 和 `icons/INDEX.csv`；逐项保留全部原始列于 [catalog-51.json](sources/catalog-51.json)。类别、序号、来源行号和候选约束是审计新增字段。
- 资产：对 51 个本地文件进行只读格式、尺寸、SHA-256 核对，见 [assets-manifest.json](sources/assets-manifest.json)。未复制或修改原图，也未将 PDF、截图或账户资料纳入仓库。
- `reference.authType` 表示另一应用目录声称的接入类型；`effectiveAuthStrategy=null` 表示 yijie 尚未验证最终认证策略。不能直接把该 JSON 导入 Codex、宿主配置或生产目录。
- 各服务 `verification=NOT RUN`：没有运行远端 MCP initialize、tools/list、tools/call、OAuth、真实账户、计费调用或 npx。静态原值比对成功与真实服务联通是两项事实。
- 公开官方/维护者文档只补充其能证明的范围，不把另一应用的“实测”继承为 yijie 的通过证据。

## 2. 真实统计与来源矛盾

| 项目 | 只读核对结果 |
|---|---|
| 总数/标识 | 51；serverName 唯一，MD 与 CSV 六个业务列逐条一致 |
| 分类 | 知识文档 2、电商零售 6、数据分析 2、效率工具 14、行业数据 18、市场营销 9 |
| transport | 49 HTTP、2 stdio |
| 原 authType | **44 oauth、1 gateway-oauth、6 none**；来源摘要 45/1/5 不正确 |
| none 分布 | 4 HTTP（FTShare、执中、Agentic Engine、豆蔻医生）+ 2 stdio（Google 日历/地图） |
| 图标文件 | 51 个一一对应，无缺失、多余或重复 |
| 图标扩展名/字节 | 扩展名为 45 PNG+6 SVG；真实格式是 **44 PNG+1 JPEG+6 SVG** |
| 尺寸 | 仅 8 PNG 为 240×240；Google 2 PNG 为 80×80；其它不是统一 240px |
| 原图地址 | 48 个 skills-assets.qwenwork.cn、1 个 img.alicdn.com（Todoist）、2 个无远程 URL |

原资料“45 官方 PNG + 6 SVG + 2 Google 截图”的文字会得到 53；实际 45 个 `.png` 文件名已经含 2 个 Google 截图，且其中 1 个字节格式是 JPEG。`thinkingdata.png` 实际为 100×100 JPEG。资产消费前应在项目正常资产构建流程中正确标识 MIME/输出扩展名，保留原 sha；本轮不重写原文件。SVG 应保留 viewBox 比例，不能把百分比宽度当作像素尺寸；微博 declared 200×200 但 viewBox 404×323，单小二 width=100% 且未声明 height。UI 采用统一容器和 contain，不能按“全为正方形 240px”裁切。

## 3. 51 项完整原始目录

下表每行的真实连接/授权/业务验证状态均为 **NOT RUN**。地址和命令均为来源值，不意味着可执行或已获账户授权。

| # | 类别 | serverName / 名称 | transport | 来源 authType | 原始地址或命令 | 原图文件 |
|---|---|---|---|---|---|---|
| 1 | 知识文档 | `cue` / cue | http | `oauth` | `https://cue.humanmeetsai.com/mcp` | `cue.png` |
| 2 | 知识文档 | `baixiao-mcp` / 百晓智能 | http | `oauth` | `https://mcp.know-pa.cn/qw/mcp` | `baixiao-mcp.png` |
| 3 | 电商零售 | `dxe-mcp-server` / 单小二 | http | `oauth` | `https://api.zhongyifu.cn/mcp` | `dxe-mcp-server.svg` |
| 4 | 电商零售 | `Hologrow` / Hologrow | http | `oauth` | `https://mcp.hologrow.ai/mcp` | `Hologrow.png` |
| 5 | 电商零售 | `X-Store` / 好多店 | http | `oauth` | `https://mcp-ai.coolstore.cn/mcp` | `X-Store.png` |
| 6 | 电商零售 | `yintai-open-platform` / 银泰商业开放平台 | http | `oauth` | `https://open.linkheer.com/mcp` | `yintai-open-platform.png` |
| 7 | 电商零售 | `yuyidata` / 语忆Neosight | http | `oauth` | `https://service-api.yuyidata.com/gateway/ai-chat/mcp/v2/neosight` | `yuyidata.png` |
| 8 | 电商零售 | `taobao-flash-sale-retail` / 淘宝闪购零售商家版 | http | `gateway-oauth` | `https://mcp.qwenwork.cn/connectors/taobao-flash-sale-retail/mcp` | `taobao-flash-sale-retail.png` |
| 9 | 数据分析 | `FTShare` / FTShare 金融数据 | http | `none` | `https://market.ft.tech/gateway/mcp` | `FTShare.png` |
| 10 | 数据分析 | `yunting-consumerlens` / 云听ConsumerLens | http | `oauth` | `https://open-mcp.sv.yuntingai.com/mcp` | `yunting-consumerlens.png` |
| 11 | 效率工具 | `google-calendar` / Google 日历 | stdio | `none` | `command: npx @cocal/google-calendar-mcp` | `google-calendar.png` |
| 12 | 效率工具 | `google-maps` / Google 地图 | stdio | `none` | `command: npx -y @modelcontextprotocol/server-google-maps` | `google-maps.png` |
| 13 | 效率工具 | `speechclaw` / 思必驰AI办公 | http | `oauth` | `https://officeclaw.beta.duiopen.com/speechclaw/mcp` | `speechclaw.png` |
| 14 | 效率工具 | `caoliao` / 草料二维码 | http | `oauth` | `https://open.cli.im/mcp` | `caoliao.png` |
| 15 | 效率工具 | `wavenote` / WaveNote | http | `oauth` | `https://mcp.wavenote.cn/mcp/audio` | `wavenote.png` |
| 16 | 效率工具 | `yida` / 宜搭 | http | `oauth` | `https://www.aliwork.com/openyida/agent-api/mcp` | `yida.png` |
| 17 | 效率工具 | `qingflow` / 轻流 | http | `oauth` | `https://mcp.qingflow.com/mcp` | `qingflow.png` |
| 18 | 效率工具 | `uupt` / UU跑腿 | http | `oauth` | `https://api-open.uupt.com/mcp/order?source=qwenwork` | `uupt.png` |
| 19 | 效率工具 | `fenbeitong` / 分贝通 | http | `oauth` | `https://mcp.fenbeitong.com/mcp/source/qwenwork` | `fenbeitong.png` |
| 20 | 效率工具 | `bazhuayu` / 数阔八爪鱼 | http | `oauth` | `https://mcp.bazhuayu.com` | `bazhuayu.png` |
| 21 | 效率工具 | `camscanner-mcp` / 扫描全能王 | http | `oauth` | `https://ai-tools.camscanner.com/mcp` | `camscanner-mcp.png` |
| 22 | 效率工具 | `todoist` / Todoist | http | `oauth` | `https://ai.todoist.net/mcp` | `todoist.svg` |
| 23 | 效率工具 | `agentkey-qwen` / Agentkey | http | `oauth` | `https://api.agentkey.app/qwen/v1/mcp` | `agentkey-qwen.png` |
| 24 | 效率工具 | `huida-erp` / 惠搭ERP | http | `oauth` | `https://mcp.3cuan.com/mcp` | `huida-erp.png` |
| 25 | 行业数据 | `FastMoss` / FastMoss | http | `oauth` | `https://mcp.fastmoss.com/mcp` | `FastMoss.png` |
| 26 | 行业数据 | `smartsalary` / 薪智·市场人才薪酬数据 | http | `oauth` | `https://ai.smartsalary.cn/smartsalary-mcp/mcp` | `smartsalary.png` |
| 27 | 行业数据 | `qixin_insight` / 启信慧眼 | http | `oauth` | `https://mcp.qixin.com/mcp` | `qixin_insight.png` |
| 28 | 行业数据 | `zerone` / 执中·金融数据 | http | `none` | `https://ai.zerone.com.cn/mcp/pe` | `zerone.png` |
| 29 | 行业数据 | `patent-analysis` / 智慧芽·专利分析 | http | `oauth` | `https://connect.zhihuiya.com/e14e5f/logic-mcp` | `patent-analysis.svg` |
| 30 | 行业数据 | `thinkingdata` / Agentic Engine | http | `none` | `https://ta-sdk-service.thinkingdata.cn/mcp` | `thinkingdata.png` |
| 31 | 行业数据 | `morningstar` / 晨星 Morningstar | http | `oauth` | `https://mcp.morningstar.cn/mcp` | `morningstar.png` |
| 32 | 行业数据 | `dichanai-mcp` / CRIC 克而瑞地产数据 | http | `oauth` | `https://mcp.dichanai.com/mcp-server` | `dichanai-mcp.svg` |
| 33 | 行业数据 | `Yingmi` / 盈米基金 | http | `oauth` | `https://stargate-partner.yingmi.com/mcp/v2/oauth/qieman` | `Yingmi.png` |
| 34 | 行业数据 | `wind` / Wind Alice万得金融数据 | http | `oauth` | `https://mcp.wind.com.cn/vserver_qwenwork/mcp/` | `wind.png` |
| 35 | 行业数据 | `yidian-company` / 质数幻方·企业数据 | http | `oauth` | `https://mcp.yidian.cn/mcp/company` | `yidian-company.png` |
| 36 | 行业数据 | `investoday` / 今日投资·金融数据 | http | `oauth` | `https://data-api.investoday.net/data/mcp?source=qwen_work` | `investoday.png` |
| 37 | 行业数据 | `dzh-mcp` / 大智慧 | http | `oauth` | `https://mcpali.dzh.com.cn/mcp` | `dzh-mcp.png` |
| 38 | 行业数据 | `Octoparse-data-hub` / 八爪鱼Data Hub | http | `oauth` | `https://mcp-v2.bazhuayu.com` | `Octoparse-data-hub.png` |
| 39 | 行业数据 | `doukou-doctor` / 豆蔻医生 | http | `none` | `https://mcp.testonelife.com/mcp-servers/deap-clinical-server` | `doukou-doctor.png` |
| 40 | 行业数据 | `tushareMcp` / Tushare·金融数据 | http | `oauth` | `https://api.tushare.pro/mcp/` | `tushareMcp.png` |
| 41 | 行业数据 | `eastmoney` / 东方财富妙想MCP | http | `oauth` | `https://mxapi.eastmoney.com/mxds/v2/mcp` | `eastmoney.png` |
| 42 | 行业数据 | `gildata_finance_data_qwen` / 恒生聚源金融问数 | http | `oauth` | `https://ft.gildata.com/ai-sso/mcp/qoderwork` | `gildata_finance_data_qwen.png` |
| 43 | 市场营销 | `fanruan-growth-advisor` / MOSS增长谋士 | http | `oauth` | `https://www.mossdo.com/api/v1/mcp` | `fanruan-growth-advisor.png` |
| 44 | 市场营销 | `weibo` / 微博 | http | `oauth` | `https://cli.weibo.com/mcp` | `weibo.svg` |
| 45 | 市场营销 | `jinshuju` / 金数据 | http | `oauth` | `https://jinshuju.net/mcp` | `jinshuju.svg` |
| 46 | 市场营销 | `xiaoe-mcp` / 小鹅通 | http | `oauth` | `https://agent.xiaoe-tech.com/mcp` | `xiaoe-mcp.png` |
| 47 | 市场营销 | `feisentry` / 飞哨GEO | http | `oauth` | `https://mcp.feisentry.com.cn/mcp` | `feisentry.png` |
| 48 | 市场营销 | `xiaoliebian` / 小裂变SCRM | http | `oauth` | `https://w.xiaoliebian.com/api/demo-wechat-work/mcp/scrm` | `xiaoliebian.png` |
| 49 | 市场营销 | `ysk_mcp_3f824505d1faf80bc60c052729620929` / 智客AI | http | `oauth` | `https://open.yscredit.com/ys-mcp/report` | `ysk_mcp_3f824505d1faf80bc60c052729620929.png` |
| 50 | 市场营销 | `3chat` / 3Chat私域客户运营 | http | `oauth` | `https://app.3chatai.cn/mcp` | `3chat.png` |
| 51 | 市场营销 | `xiaoliebian-geo` / 小裂变GEO | http | `oauth` | `https://w.xiaoliebian.com/api/xiaoliebian-geo/mcp/geo` | `xiaoliebian-geo.png` |

## 4. 分组接入策略与证据

以下为候选策略，具体产品 wire、存储和授权边界以正式设计为准。

| 分组 | 当前证据 | yijie 所需补全 |
|---|---|---|
| 44 OAuth HTTP | 原资料声明 oauth，并非本轮逐站实测 | 使用既有 Codex MCP OAuth 能力的适用部分；逐站核验 discovery、registration、callback、PKCE、scope、resource audience、refresh 与凭据归属 |
| FTShare HTTP | 当前维护者中文 README 指定 `FTSHARE_API_KEY` HTTP Header | 独立 API Key 字段与精确 header 绑定；不能默认 Bearer 或 query token |
| 执中 HTTP | 官网确认 API_KEY；本轮未获得 `/mcp/pe` 的具体承载契约 | header/query/body/调用参数的具体字段 UNKNOWN；未核实前不生成猜测配置 |
| Agentic Engine HTTP | 原资料是 HTTP；当前官网展示另一 stdio 包 `@thinkingdata/mcp-server` 及 `API_TOKEN` env | 该 env 不证明 HTTP endpoint 使用同名 header；先核验 HTTP 正式契约，不擅自切换另一接入 |
| 豆蔻医生 HTTP | 原资料仅有 endpoint 与无宿主授权说明 | 凭据名、位置、格式、需要性及数据范围 UNKNOWN |
| Google 日历 stdio | 维护者要求 `GOOGLE_OAUTH_CREDENTIALS` 指向 credentials JSON，server 自己执行 Google OAuth | Node/固定包来源、Desktop App OAuth client 文件、Google API/consent 与 server-managed token 边界；启动成功不等于账户已授权 |
| Google 地图 stdio | `GOOGLE_MAPS_API_KEY` env 明确；reference package 已归档且不再维护 | 固定包来源、Node 兼容、当前 Google API、key、启用 API、额度/计费；不得以旧 README 声称当前实测可用 |
| 淘宝闪购 | 原地址是千问办公网关，原资料提到私有 `biz/user/v1/connector-oauth/taobao-open-platform/` 路由 | yijie 自有接入资格、AppKey、服务端 AppSecret、登记回调、零售商家业务 API/权限及供应商授权的 MCP/Connectors 适配层 |

公开依据（2026-10-07 读取；均未进行账户或服务调用）：

- [MCP Authorization 规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)：HTTP OAuth 与 stdio 凭据边界、发现规则和注册方式。
- [FTShare 维护者仓库](https://github.com/FTShare-Lab/FTShare-MCP)：中文 README 给出精确 `FTSHARE_API_KEY` header。英文 README 的一般调用示例并未完整反映中文页最新鉴权，不能用其无凭据示例覆盖明确鉴权说明。
- [执中官网](https://www.zerone.com.cn/products/mcp)：API_KEY 与 MCP/CLI 介绍。其公开 PDF 使用说明书此次网络读取超时；未猜测其中内容，HTTP binding 仍 UNKNOWN。
- [ThinkingAI 官网](https://www.thinkingai.cn/product/mcp-service/)：展示 stdio/`API_TOKEN` 方案，未据此验证来源 HTTP endpoint。
- [Google Calendar 维护者仓库](https://github.com/nspady/google-calendar-mcp)及[认证说明](https://github.com/nspady/google-calendar-mcp/blob/main/docs/authentication.md)：credentials 文件、server 自管授权；并非 Google 官方提供的该 MCP 包。
- [Google Maps reference server](https://github.com/modelcontextprotocol/servers-archived/blob/main/src/google-maps/README.md)及[归档声明](https://github.com/modelcontextprotocol/servers-archived)：环境变量和维护状态；不能冒称 Google 官方维护服务。
- [淘宝开放平台 OAuth](https://developer.alibaba.com/docs/doc.htm?articleId=102635&docType=1&treeId=154)：注册应用、AppKey/AppSecret、回调与用户授权是一般前提；**不证明**淘宝闪购业务资格已批准，也不证明一般淘宝 token 能调用千问网关。

淘宝不能仅凭通用 OAuth 按钮标为接入完成，不能使用第三方应用会话/私有 API 或捏造“自有网关”来消除阻断。目录仍保留该项及明确未具备的配置条件，不能从 51 项中静默移除。

## 5. 宿主耦合与环境线索

| serverName | 原值中的线索 | 核对要求 |
|---|---|---|
| baixiao-mcp | `/qw/` | 缩写含义及是否允许非原宿主调用待确认 |
| uupt | `source=qwenwork` | 来源参数的业务/资格语义待确认 |
| fenbeitong | `/source/qwenwork` | 渠道路径待确认 |
| agentkey-qwen | `/qwen/`，ID 含 qwen | 路径/标识保持原样作为 reference |
| wind | `/vserver_qwenwork/` | 渠道 endpoint 待确认 |
| investoday | `source=qwen_work` | 来源参数待确认 |
| gildata_finance_data_qwen | `/qoderwork`，ID 含 qwen | 混合宿主命名待确认 |
| taobao-flash-sale-retail | `mcp.qwenwork.cn` | 明确第三方宿主网关；单独接入阻断 |

上述前七项是兼容性线索，不能据字符串断定一定不可用，也不能擅自去掉、替换成 `yijie` 或视为供应商已授权的通用入口。额外保留 `speechclaw` 的 beta 域名、`xiaoliebian` 的 demo-wechat-work 路径、`patent-analysis` 的 e14e5f 不透明片段；盈米的 qieman 也不自行改写。这些含义未验证。

## 6. OAuth 与状态设计纠错

来源中的 `{url}/.well-known/oauth-protected-resource` 不是通用正确算法。标准先使用 `WWW-Authenticate` 的 `resource_metadata`；缺失时按规范尝试路径插入的 well-known 和根 well-known。例如 endpoint `https://example.com/public/mcp` 对应路径候选是 `https://example.com/.well-known/oauth-protected-resource/public/mcp`。应优先复用固定 Codex 的已验证原生实现，检查版本能力缺口；不另写一个按字符串拼接的 OAuth 客户端，也不默认所有服务支持 dynamic registration。涉及凭据边界的架构决策仍需在正式设计确认，原生能力存在不等于可直接接触商家平台 secret。

产品数据应分开记录目录身份、用户配置、全局启用、账户授权、实时连接及 Composer 当前选择。`serverName` 原值需完整保留大小写；UI 名称不是主键。Composer 展示标签不等于将密钥写进 prompt，不等于新的业务授权；“连接成功”“配置已保存”“已启用”不能互相替代。所有未知状态保留未知，不用绿灯弥补缺证据。

建议设计输入包含：稳定目录 ID、类别、source ordinal、原始 serverName/URL/auth/icon、候选策略、凭据字段定义及来源、runtime 依赖、channelDependency、外部前提和验证状态。秘密只记录引用，不记录值。JSON 中这些字段是需求候选，不能成为绕过 Contract First 的影子 DTO。

## 7. 接入与验收阻断台账

| ID | 阻断或未执行项 | 原因与影响 | 解除证据 |
|---|---|---|---|
| CAT-01 | 51 服务真实连接、授权、业务闭环 NOT RUN | 本轮只读审计/需求起草；不证明任何账号可用 | 按获准范围逐项记录 yijie 真实来源、平台、固定版本与成功/失败/取消结果 |
| CAT-02 | 44 OAuth 的 yijie 注册/回调/PKCE/scopes UNKNOWN | 原宿主 metadata/auth 声明不能继承 | 实际官方 metadata、适用注册契约及 yijie 受管授权证据 |
| CAT-03 | 7 个带宿主标记的直连 endpoint 可移植性 UNKNOWN | 来源/渠道可能涉及合作范围 | 供应商对 yijie 的正式文档或确认及适用 endpoint |
| CAT-04 | 执中/Agentic Engine/豆蔻医生 HTTP credential binding UNKNOWN | 不统一猜测 Bearer、query 或 tool 参数 | 与参考 endpoint 一致的供应商鉴权契约 |
| CAT-05 | 淘宝闪购网关与业务能力未具备 | 缺自有应用资格、供应商业务协议和已评审适配方案 | yijie 自有授权/权限、正式业务接口与 MCP/Connectors 集成及真实验收 |
| CAT-06 | Google 2 stdio 包未安装/执行；版本与 runtime 未固定 | 资料只有浮动 npx 命令，Maps 已归档 | 受管固定包来源及校验、正常生命周期、凭据准备、实际兼容结果 |
| CAT-07 | 图标打包/视觉验收 NOT RUN | 只有本地元信息检查；JPEG 扩展名、非统一尺寸、SVG geometry 与 Google 截图需处理 | 正常资产构建输出与实际浅/深主题 contain/失败回退视觉检查 |
| CAT-08 | 业务写入、真实账户、费用和健康/商家数据测试 NOT RUN | 来源文档不产生外部操作或费用授权；避免以自测替代用户授权 | 明确范围/账户/额度/操作授权后按安全正常流程验证 |

验收必须区分 51 项目录齐全、配置 UI 可用、实际平台联通、业务能力可用，不能把前两者当成“51 项全部接入完成”。必要的供应商资格/凭据缺失是未完成项，不通过 mock、静态 metadata 或另一宿主截图冒充。

本轮未进行任何强杀/故障注入、权限破坏、运行时替换、攻击 fixture 或恶意资源注入；后续验收亦不得采用这些方式。正常取消、无网络/失败由自然发生或非破坏性的普通合成返回验证时，要分别标明合成与真实证据。
