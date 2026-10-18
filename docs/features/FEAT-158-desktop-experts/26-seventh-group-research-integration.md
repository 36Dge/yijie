# 第七组：行业研究员接入

2026-10-17，local/demo_fast。完整回顾17方案九节及18—25的累积接入记录，保持唯一ROLE/知识索引、canonical包/收据、Native会话/outbox、Host普通基线、选定连接器与逐次审批主链。原51资源（38普通+13专家版本）、10原生+1展示、60连接器/revision9作为基线，保留原专家和历史。

`contract-impact=semantic`：新增版本化研究内容与本地资源部署pin，专家/连接器公共wire、数据库、Runtime和搜索权限策略不变。新增market-researcher适配版0.1.0，来源原包0.1.0另行记录，不能据同版本号声称行为等价。新增内容权威在Skills，公共Contracts变更N/A；bundle拟为0.11.0。同步消费精确摘要，回退保留旧资源及历史引用，不能用旧pin执行新绑定。

原84文件/7技能已重新枚举，与WorkBuddy安装缓存逐字节一致。NeoData专属凭据迁移/自动pip/HTTP、WeStock混淆运行脚本、受限制Office资源及LD_PRELOAD流程不引入。统一发行人披露优先的来源策略；默认中文，用户可指定语言。缺失note-writer和comps模板由本地明确产物生成替代。

数据/搜索选择现有渠道：Tushare仅已实现的单日A股行情，不暗示支持income/balancesheet；东方财富等金融服务只使用本轮实际已选择、已授权、完整发现并冻结的工具schema，不假造方法名；LinkFox Google检索是来源发现，不把摘要当已读原披露。外部调用仍需已有机器审批，专家内置web_search保持disabled；无新provider/凭据/隐藏网络脚本。无账号真实调用按用户要求NOT RUN。

本轮证据：`yijie-desktop/.local/seventh-group-research-20261017`。实现、审计与检查结果完成后记录于下文。

## 实际实现

新增`market-researcher@0.1.0`，运行资源`industry-research`，17文件，包括唯一ROLE/SKILL、7份参考、自有研究/OOXML脚本、合成示例与eval/checklist。所有原51项资源保留；新的52资源=38普通+14专家版本。最后一张展示卡改为原Native资源准备/绑定/快捷问题链，11位原生专家，无展示占位、无专家团；旧目录/加载失败不伪造新卡片。全部转原生后发现原无展示卡的错误状态缺少重试提示，已在原YjEmpty上补提示，布局/CSS和权限逻辑未改。

`research.py`是真实本地程序，包含prepare/observe/build：

- LinkFox查询：固定既有proxy_call/aiMode/googleSearch参数，返回仅标来源发现，不升级为金融事实。
- Tushare行情：仅现有tushare_daily的单代码/单交易日，回执精确核对service/tool/arguments、代码/日期/close，不能把价格当市值或完整财务表。
- 当前金融工具：支持已注册东方财富/Wind/晨星/恒生聚源的Native暴露工具元数据。核对service/title和既有命名算法的一致性，参数保留原样，完整schema验证仍由原Native/Broker执行；本地文件不能赋予资格/权限。只准备研究查询，不建立端点或私有认证，不声称这些供应商覆盖/字段等同NeoData/WeStock。
- 证据与计算：保留原工具回执和引用文本，校验来源身份/期间索引、数值引用、发布与获取日期、币种/单位/FY或LTM/EBITDA定义；只对相容数值计算，缺项保留N/A，不删同行。EV五项缺一不算，负/零盈利倍数NM，负利润率保留，统计显示有效样本数。
- 文件产物：实际生成HTML研究稿（四部分、完整同行表、离线SVG收入对比、来源、完整核对记录）、可编辑XLSX（Comps/Evidence/Sources/Method四页）、inspection.json及输入原字节。Python标准库，无pip/npm/Office运行依赖、CDN、自动下载、上传或发布。

本版**没有实现DOCX/PPTX和机构模板导出**，原Office组件未迁入；不是“已实现但缺账号”。HTML/XLSX明确列为当前支持格式，不能改扩展名冒充Office。也没有新增NeoData/WeStock provider、自动提取任意扫描PDF或构造共识预测数据库。资料可由当前会话已支持的读取工具取得，读取能力不足时明确缺输入。

## 接入后的深入审计

同一Codex在实现后重新复读增量及所依赖的既有资源/Native/Host/连接器路径；不是独立人工批准。原84文件重新枚举和SHA核对；重点审阅原Agent、研究方法、数据/认证/脚本路径和Office限制，未执行混淆vendor，也不把其数百万字节代码称为已逐行审计。本次全量代码审计指本组实现及其接入调用链，不包含整个第三方服务/Runtime。

| 范围 | 审计结论/处理 |
| --- | --- |
| 来源冲突 | 去掉NeoData独占、固定覆盖比例和不合本工程的WebSearch/WebFetch假定；发行人/交易所/监管优先，提供方与用户资料明确标识。搜索摘要不做直接数值来源，来源矛盾不自动平均。 |
| 认证/运行依赖 | 排除WorkBuddy token读取迁移、保存、固定sub_channel、自动pip/HTTP回退；WeStock脚本不执行、不补历史bin。Office整个子树不打包，禁止原LD_PRELOAD流程；独立自有HTML/XLSX替代缺失note-writer/comps模板。 |
| 搜索与金融调用 | 不新增expert-name网络例外、不改web_search=disabled、不切full。数据由现有已选择连接器提供，当前工具schema/安装/权限/审批仍为执行权威。财务元数据不含具体线上工具名的伪造常量；测试中的synthetic_public_query明确只为普通合成schema。 |
| 回执身份 | 实际service/tool/arguments与原计划逐项相等；Tushare单行代码/日期/close匹配。错误/空/未知结果不变成功；金融内容只标source_requires_review，搜索为discovery_only，不直接生成verified facts。 |
| 证据边界 | 来源ID唯一，entity_ids/period_ends登记实际文档/回执范围，quote确在保留文本中且完整数值匹配；100不匹配1000或-100。provider来源正文须来自所附原回执，搜索不能伪装provider。所有这些仅证明机械一致性，文档真实性、索引登记和语义仍需分析师复核，不能把用户写的JSON当服务证明。 |
| 期间/币种 | FY/LTM必须是明确完整年度范围，NTM/季度不混入；不同币种/scale/EBITDA定义阻断受影响指标，不默认汇率。来源发布日晚于研究截止日或早于声称已知的数值日期拒绝，避免前视数据混入。 |
| 估值 | EV=市值+债务+优先股+少数股权−现金，缺任一项EV未知；只在正分子/分母计算倍数，负盈利保留且倍数NM；现金/债务等显式0不等同缺失。原毛利率层级绝对规则和IFERROR(...,0)不采用。行业是否适用EV/EBITDA仍是分析判断，不对银行/REIT等自动套结论。 |
| 精度/表格 | Decimal内部计算和规范化值不提前四舍五入，避免小额/百万单位被舍成0。XLSX真实公式引用输入，COUNT/ISNUMBER/正分母保护空白和NM；初始未知也写带保护公式及字符串缓存，不伪造0。来源长文本分片保留并按Excel UTF-16单元格限制留余量。 |
| HTML/报告 | 所有数据转义，纯本地CSS/SVG，无脚本/CDN。四部分均存在，unknown显式；保留所有同行/缺项/来源和统计。实际生成中文研究稿，完整结构化核对记录可展开查看。 |
| 历史/架构 | 仍是Skills规范包/authority、Host受管安装receipt与Core journal、Native精确ExpertRef/outbox、单会话选择与retained引用保护。只增资源和精确pin，无SQL/Runtime/权限协议变更；资源准备不自动发消息。 |
| Connector生产边界 | catalog/registry/OAuth/凭据/生产provider代码保持；broker.rs只在现有cfg(test)模块增加四金融服务审批回归。现有write风险、冻结schema、ApproveOnce及一次执行许可不变；拒绝0执行、批准1次，重复consume拒绝，正常close。 |

实现中测试实际找出并修复了来源索引循环变量覆盖source ID的问题，未降低引用检查；长来源测试最初直接数XML中的短语，短语跨单元格边界后计数少1，改为解析单元格并重组整段与原文逐字比较；这不是丢文本，也未放松保真。Decimal展示从固定4位改为保留精度后，测试改为按数值验证百分比（20.0=20），避免把格式当算术错误。无展示卡状态的恢复提示已修复并重测。

## 验证结果

证据根：`yijie-desktop/.local/seventh-group-research-20261017`。均为正常开发/测试，使用普通合成数据、临时或内存状态、in-process MCP及正常关闭；无强杀、权限破坏、攻击fixture、二进制/运行时替换。含禁止故障/攻击注入的宽泛历史测试未运行，不计PASS；全量lint实际运行。

| 项目 | 结果与日志 |
| --- | --- |
| Skills全量lint/test/规范打包 | PASS，`skills-audited.log`，81项测试、104条合成eval格式；新增16项研究回归涵盖数据/工具身份、来源、期间币种、负盈利/缺值、公式、精度及长文本保留。合成eval不调用模型。 |
| Host全量lint/实际资源 | PASS，`host-checks.log`；4组race测试覆盖最终52资源/14专家版本的实际安装与读取、原39资源扩容保留、Core journal生命周期、旧新版本与会话引用共存。新增专家在临时测试根实际安装。 |
| Desktop全量lint | PASS，`desktop-lint.log`；`make lint CONTRACTS_DIR=.local/demo-fast-contracts`，generate一致性、ESLint零warning、vue-tsc、cargo fmt、all-targets Clippy完整通过。沿用合法干净历史Contracts检出验证旧锁，当前候选另行核查真实源，不绕门禁。 |
| 当前资源/Host来源门禁 | PASS，`resource-sync-final.log`、`source-freeze-final.log`、`preflight-final.log`；canonical资源同步/冻结、实际Host源码、38普通包/旧权限门禁一致。FEAT-137历史acceptance仍NOT PASSED，不因本轮检查改写。 |
| Native实际目录 | PASS，`native-functional.log`4项：真实bundle加载、11位最新专家安全目录与精确引用、60连接器、缺账号不可启用门禁。普通38包隔离。 |
| UI与前端构建 | PASS，`ui-build-final.log`5文件97测试及pnpm build；11卡无重复，旧目录/初始加载/失败无伪造，资源准备与快捷问题仍不自动发送。原大chunk提示保留。未启动真实App主题/最小窗/模型E2E。 |
| Connectors全量lint/普通协议 | PASS，`connectors-checks.log`：Go vet/catalog race、固定Runtime来源、Rust格式/Clippy。`worker-functional.log`5组普通检查：四金融服务的现有Broker审批、LinkFox审批、Tushare in-process调用与单行投影、60注册。没有实际账号或收费网络请求。 |
| Contracts/元仓 | Contracts全量lint PASS，`contracts-checks.log`，原OpenAPI未使用组件警告保留；元仓`meta-checks.log`lint/50测试/shell语法通过。Contracts本轮531源文件未改变，未重跑或冒称解决第四组全局breaking历史远程schema EOF。 |
| 实际产物 | `synthetic-report-final`生成HTML/XLSX/JSON，合成甲EV=220、EV/EBITDA=11、P/E=20，合成乙负盈利倍数NM。所有OOXML成员解析、真实公式/缓存/证据页校验通过；`artifact-preview-final.log`确认两文件均由macOS Quick Look正常生成预览，已查看HTML与工作簿缩略图。XLSX缩略图只覆盖局部，不冒称完整Office视觉或外部Excel重算通过。 |
| 原资源/历史 | `preservation-final.json`：原51条manifest及51归档逐字节一致，9日常安装版本匹配canonical；9旧Runtime会话文件与110旧资源/收据摘要一致。未打开日常数据库写入，不对动态WAL作伪造一致性结论。 |
| 架构/工作区 | `architecture-preservation.json`：Contracts531、Runtime5575基线文件未变，12个注册/鉴权/provider相关基线文件未变；broker仅新增测试。7仓HEAD/分支未动，git diff --check通过；无提交/推送。增量/状态见`increment-source-changes.json`、`final-repository-state.json`。 |

原始包没有执行；公开浏览仅核验官方产品/接口资料，没有拿公开说明当当前账号工具schema。金融服务在线字段和费用未核实，需账户后分别进行实际发现、资格与业务验收。

## 最终候选与后续边界

- Bundle `0.11.0`，`yijie-skills/dist/skills-experts-seventh-group-v010`，52资源=38普通+14专家版本。
- Manifest：`fa320bc5f3caa0caca0e7851061b186f4b975b20c2d0f6da8351715a2d377fa7`。
- Authority：`89b38b499e551eaa21c215b769b09c69384cf0166d12d6bbea40f565ded54518`。
- 内容源树：`358cb9538a4ed7e185096d26725b64990cbfb3b3f3efe319be95a4156ea19a03`。
- experts Contracts锁保持`fe49fb6cd83e11dba69861025a23a8faf1d9d3740c887c1716a3637eb34154cb`。

十位新增专家均进入现有原生专家模块，加原资深电商运营操盘手共11位。此结论仅覆盖各自记录的已实现范围；不把三位LinkFox未接入的自动上传/下载等、行业DOCX/PPTX或其他源包能力追溯改为完成。

按用户要求NOT RUN：真实金融/搜索账号认证与当前schema、实际收费取数/搜索质量、真实市场数字/财务含义/同业可比性与模型效果、真实App D4。没有账户、不搬用WorkBuddy登录态。HTML/XLSX离线产物与安装/协议测试不能替代这些在线验收。

本机候选release=false，第三方再分发未核实；没有重建/替换正在运行的App、发布、提交或推送。源码接入完成不表示当前旧App二进制已加载新目录。
