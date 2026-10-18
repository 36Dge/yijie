# 第二组：本地报价与数据报告真实接入

2026-10-16。用户要求完整回顾审计方案后继续下一组真实接入，保留原专家和历史，并完成真实功能及全量lint。范围来自[17审计](17-ten-expert-integration-feasibility-audit.md)§7.2第二步：NextB2B报价、数据报告可视化。已复核原审计、内容/执行/打包笔记及[18](18-first-three-live-integration.md)、[19](19-first-three-repair-and-revalidation.md)、[20](20-host-source-lock-lint-repair.md)；第一组失败记录与修复证据保留。

## 实现范围

`contract-impact=semantic`：新增可执行内容与目录、更新本地部署pin；不改experts/1、manifest v3、SQL35/Host10、Runtime、权限或outbox语义。Skills仍为内容权威，沿规范bundle/authority、Host与Native精确资源、原会话绑定/发送和恢复。两位只使用既有会话工具，没有新增连接器或第二套专家引擎。

- `tradebuddy-baojia@0.1.0`：用户给价，读取本地CSV/XLSX，明确含税/未税及运费最终额；Python标准库Decimal逐行舍入，生成含公式/缓存的quotation.xlsx、calculation.json、本地台账新版本及精确SKU同口径比较。未知不填0、不估价、不代发；旧输入/台账不覆盖。原包的本地Excel替代路径在本组落实，腾讯文档与私有行业资产库未接入。
- `report-viz-expert@0.1.1`（初版0.1.0保留）：用户CSV/JSON，明确维度/系列/单位/时间/来源，完整表格、离线交互HTML、ECharts SSR SVG及数据/统计文件。复用Desktop精确ECharts6.1.0 UMD原字节和Apache许可/NOTICE，去掉原Chart.js CDN与未锁定AntV临时安装。图表色来自易界语义token；未修改应用CSP。缺失保留空、统计为已知值小计，图表分页但不丢行。PNG渲染器和在线BI不在本地包内。

两位独立易界版本与WorkBuddy原版本区分。原20个文件（报价11、报告9）重新与本机WorkBuddy原目录逐文件匹配，原始资料未修改。来源审校、逐文件摘要及本轮本地授权在Skills provenance单独保存；local-development、release=false、原专家素材公开再分发资格未核验。

最终候选0.6.1共47资产：38普通技能、9个专家版本；相对第一组原44条元信息/归档全部相同；相对本组初版原46条也全部相同，8个旧ExpertRef保持。UI用真实Native目录替换两个同ID展示卡，保留头像映射与三列组件。6位真实专家+5位展示，共11位，无专家团。旧小红书/跨境0.1.0仍按精确引用保留，目录最高版0.1.1。

## 验收方式与数据保留

证据根为Desktop `.local/second-group-experts-20261016/`。正常Cmd+Q退出且canonical进程exit0、App/Host端口消失后，才备份当前加密库和Host库、9份Runtime历史及113份安装文件。禁止在运行时诊断连接SQLCipher；不删旧会话、收据、数据库或失败记录。

实际验收使用现有Kimi-K3/max/ask和五条合成任务（最后一条为SVG修复版复验）：CSV报价/台账、缺价阻断、补价并读取旧XLSX新版本台账与比较、CSV数据报告。真实任务完成后独立重算、打开产物、正常退出后对照原记录、同构建重开并确认绑定。未执行危险fixture、强杀、故障注入、权限破坏、运行时劫持；安全focused检查不冒充含禁止路径的历史全量测试。

## 工程检查

- Skills lint、20项测试、60条合成eval格式、规范确定性47包已通过；格式检查不是模型质量结论。
- Host九版本实际资源生命周期、原jd39项目录升级保留、旧新版本共存（race）和lint通过。
- Native47条资产/6位最新目录投影与全部9版本精确包测试通过；私有资源不进入全局Skills。
- 5文件86项UI/launcher测试通过。Desktop全量lint（含generate:check、ESLint、vue-tsc、Rust fmt与all-targets Clippy）通过，修复版日志为`desktop-full-lint-svg-repair.log`；暂停其他构建、真实复验和同构建恢复之后，再次对当前工作区完整执行`make lint`并exit0，最终日志`desktop-full-lint-final.log`。没有降低或跳过来源锁、生成一致性、ESLint、类型、格式或Clippy门禁。
- 首次Host实测使用相对路径，Go按package工作目录解析导致bundle_missing；改正确绝对路径后通过，未改资源门禁。Native另一测试残留旧44/6数量与集合期望，初次更新为审阅后的46/8并复验，SVG修复后最终47/9再次通过；非生产加载器放宽。
- 两次canonical构建分别在既有Contracts生成检查的只读gofmt输入读取等待，sample证据显示read阻塞；各自只对该只读工具一次正常SIGINT取消，失败沿父流程退出1，没有产品进程/强杀/门禁跳过。最终用已安装且工程支持的Node24.19.0构建工具重跑原canonical流程，保留所有校验；Node24也曾遇到该等待，因此不能写成Node26缺陷或已修复工具链根因。未替换Runtime或篡改可执行文件；产物仅由工程canonical构建生成。

上述结构检查与下方真实功能结论分别记录，不把合成eval格式通过当作模型质量通过。

## 本组实际验收发现并修复的SVG问题

0.1.0实测报告的统计与全量数据正确，但独立XML解析chart-1.svg报第11行无效token：ECharts SSR把带双引号的CSS字体列表直接嵌入style属性，造成属性引号提前闭合。原模型只做正则和前600字节读回，未发现这个错误，不能把模型自述“可打开”当作通过。

按现有版本保留机制新增report-viz-expert@0.1.1（独立安装ID）；字体栈去掉嵌套引号，在写出任何文件前用Python标准库独立解析每张SVG，失败立即停止。固定ECharts原字节不变；ROLE/执行说明、来源审校、授权和测试同步。已使用的0.1.0、旧输出及本次失败记录保留，未覆写历史。正常样例与65行分页测试、独立XML解析及sharp/librsvg静态渲染通过；真实客户端修复版复验单列下方。

CUA浏览器安全策略拒绝本地file://协议。未使用替代浏览器、HTTP服务或其他方式绕过；允许的更安全验证为无网页脚本执行的本地SVG渲染、静态HTML结构/内嵌数据/网络CSP检查。HTML图例点击/悬停的浏览器交互仍未执行，不能写PASS；这不代表已发现交互失败。

## 构建一致性与真实准备失败的处理

修复版第一次真实准备产生明确拒绝回执：Native为resource_unavailable、核心安装日志为complete/bundle_missing；该操作未安装0.1.1，未改旧绑定或旧资源。停止客户端后只读取得原操作回执，没有读取运行中的数据库或重新提交同一操作。对当前App资源目录全部九版本进行正常临时安装测试通过，修复归档的字节/hash正确。

随后canonical --reopen正确拒绝“Packaged artifacts drift”：仅App可执行文件的摘要从构建回执值改变，当前文件与debug构建输出一致；源输入和已打包资源校验相同。用户随后明确确认存在其他并行构建，并已暂停。可执行文件漂移是已确认事实；结合Host保留`os.Root`、通过路径重新读manifest的代码，运行时App bundle被替换而旧句柄仍指向旧目录是与证据一致的故障机制推断，未做故障注入来重现具体替换时刻。保留失败回执及漂移证据，重新走完整canonical构建，不手改回执、不绕过来源/重开门禁。后续只在正常重建和当前资源核验后允许一次明确的新安装操作。

暂停并行构建后，完整canonical重建成功；实际App与新回执一致。新UI准备操作`6b7f1138-2806-4273-8d82-8d2c48dfd038`成功，原失败操作仍为rejected，没有改写或删除回执。会话正常更换到0.1.1并执行第五条任务。任务后正常退出时再次逐项验证96项构建产物，全部与回执相同（`final-artifact-consistency.json`）。

## 五条真实客户端任务与独立产物验证

通过日常App现有入口运行，local session `01a1451a-25ae-7583-8cc6-f9bd36a69da0`，Runtime thread `01a1451a-25f1-78f3-a545-f5413c8b9445`；2026-10-16 22:25–23:05（Asia/Shanghai），Kimi-K3/max、ask/on-request、workspace-write、network=false。全部为合成数据，没有真实商家资料。完成5次实际提交、58次工具调用；真实安装路径下脚本执行可追踪。一次资料读取命令的`echo ===`触发zsh等号展开错误，模型随后拆分读取恢复，生成器与独立校验成功；不隐藏该工具失败。

| 真实任务 | 结果与独立核对 | 耗时 |
| --- | --- | --- |
| CSV报价与首版台账 | 3行逐行ROUND_HALF_UP，净额170.39、税22.16、运费18.60，总额211.15 CNY；实际生成双页XLSX/计算记录/台账。独立表格引擎读入、渲染、重算无错误；仅在内存把数量12改13后总额219.45，未改原文件。PASS | 192.066秒 |
| 缺少新单价 | 未沿用历史7.35、未填0、未生成新报价/台账；已确认运费0不被误判缺失。PASS | 42.742秒 |
| 补价并读旧XLSX | 新单价8.02、数量5，总额45.31；旧3行逐字段保留、新增1行；同规格/单位/币种/税口径比较7.35与8.02。旧报价字节不变。PASS | 106.811秒 |
| 原报告0.1.0 | 6行/备注/统计正确，SVG因字体引号不合法而独立XML解析FAIL；旧文件和失败结果保留。 | 174.157秒 |
| 修复报告0.1.1 | 实际安装脚本生成全新report-v2；独立XML解析与sharp/librsvg静态渲染PASS，中文与两系列可见，真实零和缺失断点正确。6行所有字段与原CSV逐项相同，直营792；经销380.75明确为已知值小计、缺失1项。HTML内嵌数据/系列/全量表/禁网络CSP检查PASS。浏览器交互NOT RUN。 | 157.888秒 |

报告前后9个输入/旧产物文件hash一致；另独立确认原报价首版4文件与首次记录一致、最终审阅期间13个旧产物均未改变。实际交付位于证据根`eval-workspace/quote-v1/`、`quote-v2/`和`report-v2/`。渲染图片和表格检查位于`workbook-check/`及`report-v011-actual-chart.png`。使用表格校验工具仅用于离线独立验收，不给产品增加运行时依赖。

真实UI验证了资源准备、召唤/更换确认、取消保持旧绑定、参考问题只填草稿不发送；最终目录6位资源已准备+5位展示、三列样式和原专家0.1.3详情/历史均正常，无专家团。此次没有改通用组件和样式；当前亮色实际截图留存，暗色/1180×760沿用19中的组件验证，本轮未重新执行，不能记作新版本视觉全覆盖。

## 历史保留与正常退出

最终正常Cmd+Q退出，canonical session 89465 exit0，App与Host 18081端口均消失后才离线读取数据库。没有SIGBUS、崩溃或在运行中诊断连接SQLCipher。离线比对结果：

- Native 67表：旧9会话、63消息、32轮次、4专家绑定和既有专家操作/提交记录原行摘要均保持；仅一条旧`chat_market_dispatch.updated_at`因正常恢复检查更新，字段级比对确认没有状态、内容或权限变化。新增1个合成会话、10条消息、5轮次。
- 本次5条dispatch均accepted，5轮completed；6条outbox均done且attemptCount=0，最终绑定report-viz-expert@0.1.1、revision2、ready。原准备失败与后来成功回执同时保留。
- Host原11会话没有删除；4条仅updated_at正常更新，无其他字段变化，新增1个验收会话。
- 原9份Runtime历史文件全部逐字节不变。原113份安装文件无缺失，112份字节不变；唯一变化为正常新增操作的operations.v2.db，旧专家内容文件均不变。
- bundle新增采用新版本/安装ID，原44资产与本组初版46资产两次逐字节保留检查均通过，没有数据库schema变更。

证据：`final-native-preservation.txt`、`final-native-field-diff.json`、`final-host-preservation.json`、`file-preservation-after.json`、`final-native-execution.txt`、`final-normal-exit.json`。

同构建恢复验证：规范`--packaged --reopen`通过来源与产物一致性门禁，Host `/readyz`为ready；真实打开验收会话，5轮历史全部显示，report-viz-expert@0.1.1绑定恢复、输入为空、发送禁用，没有新增提交或自动发送。证据为`final-same-build-reopen.log`和`final-same-build-restored.txt`。应用保留在该会话供复查。

## 验收边界

已完成第二组两位的本地真实接入及上述核心文件任务。HTML浏览器内图例点击/悬停未执行，不宣称整套交互Must AC或D4全部PASS；其静态SVG、完整表格/数据和计算已独立验证。腾讯文档写入、NextB2B私有行业资产查询、在线BI、PNG产品能力仍不在本组范围。其余5位展示专家待原审计后续组推进。

用户禁止的强杀、故障注入、权限破坏、攻击归档/fixture和运行时劫持均未执行；包含这些路径的历史全量测试未运行，影响是相关对抗与故障覆盖没有新增实测。本轮Skills全量lint/test、Host正常资源测试/lint、Desktop全量lint及相关正常UI/Native测试的通过结论不扩大到未运行项目。最终元仓`pnpm lint`、50项`pnpm test`、Shell语法和六仓`git diff --check`通过，HEAD均未改变；Contracts与Runtime工作树仍干净。最后完整lint后再次核验96项构建产物无漂移（`final-artifact-consistency-after-lint.json`）。没有提交、推送、发布、变更Runtime或清理历史数据。
