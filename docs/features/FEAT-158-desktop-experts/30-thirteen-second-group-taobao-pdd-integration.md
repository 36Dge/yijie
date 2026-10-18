# FEAT-158 十三位新增专家第二组：淘宝天猫与拼多多

2026-10-17；按28号完整方案及29号第一组实证继续。用户已授权真实接入、真实功能与文件验证、代码审计和全量lint。用户已解锁并授权canonical构建与真实App验收。下文保留前轮离线阶段记录，真实验收与修复记录见末尾；最终状态以末尾实证为准。

## 架构与契约评估

contract-impact=semantic，demo_fast/local。权威源为Skills bundle-source及逐文件来源审校；consumer为Desktop Native目录/安装/SQL精确绑定、Host验证/角色注入和现有Runtime。仅新增两套expert_only本地0.1.0资源与候选摘要，不改experts/1、manifest3、公共wire、SQL35/Host10、权限或provider。Owner为当前用户；不伪造独立人工批准。先内容与确定性包，再消费者pin及兼容检查，再canonical构建与真实验收。前序54条资源/16专家版本/13位专家全部保留；目标56资源/18版本/15位专家。固定完整旧manifest并逐条比对metadata与归档摘要。回退只恢复候选指向，保留新旧已安装资源及会话，不删除历史。

七仓HEAD/dirty基线、现有manifest/authority和171份WorkBuddy原件摘要在Desktop `.local/thirteen-second-group-20261017/`。两套来源均为1.1.0，淘宝86文件、拼多多85文件；原件与用户归档不修改。不导入其plugin运行时、身份、反溯源指令或未经验证的阈值。来源全文保留为有日期的检索资料；当前平台规则须另取官方证据。无根LICENSE，不推定公开再分发；仅当前授权的本机开发候选，无commit/push/发布。

## 产品范围与决策

每位仍是一份ROLE、SKILL、索引、按需知识与本地工具。用户提供后台CSV/XLSX及明确映射；工具只用Python标准库读本地文件、Decimal计算并生成新目录中的HTML/JSON/Markdown和收据。当前会话文件权限继续生效，不新增连接器、不代登后台、不修改投放或业务记录。保留运营全流程咨询，但原脚本的默认费用、样例回退、猜测平台/表类型/百分比、无日期入窗及未知值置零不接入。

输入清单唯一：平台、店铺、时间窗、文件/工作表/表头、表类型、列映射、单位、粒度和归因口径均显式。普通缺值保留null，真实0保留0；日期未知、异平台、冲突重复记录单列。完整总额与已知小计分开；不同表/归因口径不相加。日去重访客累计不冒充周期独立访客。评分按用户明确声明的体系、尺度、单位分别展示时点，不合成健康分。未确认规则不直接给P0或关停命令。

广告毛利贡献=归因成交额×明确毛利率−消耗；毛利率40%、ROI2时每元广告毛利亏损0.2元，保本ROI2.5。不是净利润；没有完整成本、退款和税费不能宣称净利润。缺毛利率不默认40%；情景参数明确区分事实。报告建议由实际证据支持，不预测无依据收益。CSV/XLSX同数据结果等价；公式单元格要求导出值，不执行公式。

## Must验收与追踪

1. 两位真实Native准备/绑定/显式发送，经Host/Runtime读取已安装角色、知识与程序；非showcase，无专家团。
2. 两平台正常CSV和XLSX输入得到可打开HTML、JSON与来源逐字段追溯；真实模型调用保存文件，读回内容与独立计算。
3. 正常缺参、0、百分比1.2%、缺日期、异平台、重复/冲突、缺广告成交额、评分分离、粒度/归因口径分离；原报告不覆盖，修订新版本。
4. 原54资源逐项不变；原专家、SQL/Host/Runtime历史和安装记录保留。仅正常退出后备份/只读核对；完成后同构建重开。
5. 实施后逐函数审计、正常focused回归、受影响仓全量lint与严格Host来源锁；禁止强杀、权限破坏、攻击fixture、运行时劫持。不能用静态测试替代真实模型与打开文件。

当前不声称覆盖原引擎所有报表自动识别/全部阈值，也不新增Native产物预览。时间敏感政策不在离线程序中固化；需要账号或官方证据的线上商家后台验证继续NOT RUN。真实验证锁屏前置未满足时保持待验收，不伪造通过。

## 本轮已实现与离线检查（真实App验收待解锁）

两套独立0.1.0资源已完成，淘宝34文件、拼多多37文件；各一份私有ROLE/SKILL、5份入口/方法/协议/来源说明及有日期运营全文资料、正常样例/checklist/eval、2个自有标准库Python模块和独立平台profile。复制原卡片头像、补入现有目录；不创建showcase或团队。原包Agent/SKILL/诊断程序未进入可执行适配，原件仍完整保留。

候选bundle `0.13.0`，56资源/18专家版本/15位最新专家。确定性产物目录为Skills `dist/skills-experts-thirteen-second-v010`；manifest `f646d431f1d5a9c63c728dfd608602e529c95db8c2c62417213784f4f51c7583`，authority `4e16da595f8ddb69f3558e0a7720e55bcc9606a5a40c03ec7a0f3bb22d3e64ae`。这只是候选代码与资源状态，不等于本机正在运行的App已更新或两位已完成实际会话验收。

新增54条完整旧资源保护基线 `docs/provenance/FEAT-158-retained-resources-v0.12.0.json`，摘要仍为前组manifest `eae61812cdb372924b97628cdba45b4d4716303341b8f6654dde33f00c941c68`。当前全部旧metadata/归档逐字一致；旧52条基线也保留。Host固定新候选摘要；Native仍用原目录/精确引用、SQL绑定/outbox，未改Contracts/Connectors/Runtime。Host tree由现有canonical `chat-model-build-candidate.mjs --freeze`在全部consumer检查通过后重新记录，没有绕过来源锁。

实施后代码审计记录在Skills `docs/provenance/FEAT-158-thirteen-second-group-content-review-v0.1.0.md`。复核修正了评分单位分组、百分值显示单位和Excel日期原始序号追踪，另加明确日粒度与实体粒度、数据读取前后hash、普通输入错误处理。经营判断不采用原默认费率/阈值，不混评分，不宣称净利润。当前程序支持有明确日日期的8类字段；无逐行日期的周期汇总、宽评分整理、非ISO时刻规范化需要保留来源后明确处理，不能用文件名猜时间窗。原引擎的全报表自动识别、任意Excel计算、健康分与后台执行未实现，也未宣称通过。

证据根：Desktop `.local/thirteen-second-group-20261017/`。

| 检查 | 结果与证据 |
| --- | --- |
| Skills全量lint/test | PASS；96项Node测试，其中两包各19项Python正常业务回归；128条eval仅为格式校验。`skills-results.json`及日志 |
| Host全量lint、实际包focused race回归 | PASS；18版本实际安装/读取、旧专家保留、生命周期、会话与角色组合/权限基线。`host-lint-results.json`、`host-results.json` |
| Native正常focused回归 | PASS，40项，含最终实际候选目录与精确引用；`native-results.json`及12份日志 |
| UI focused | PASS，13文件141项；`ui-results.json` |
| 全54资源保留保护 | PASS，2项；`retained-resources.log`和逐metadata/归档核对 |
| Desktop全量lint | PASS，`make lint CONTRACTS_DIR=.local/demo-fast-contracts`，包含严格候选来源、ESLint/TypeScript、Rust fmt和全targets Clippy；`desktop-lint-results.json` |
| 元仓lint/test/Shell语法 | PASS，50项manifest测试；`meta-*.log` |
| 七仓与原始资料保留 | HEAD/分支未变，无旧文件删除，diff check全通过。仅本轮预期的Skills2/Host3/Desktop8个旧文件变化；Contracts/Connectors/Runtime无变化。171份WorkBuddy与用户归档原件不变。`source-preservation.json` |

禁止的历史异常注入/强杀/权限破坏/运行时替换测试未运行；没有把它们记为通过。上述全量lint完整运行，正常focused覆盖不能代表跳过的故障分支。

### 实际离线文件与尚未执行的产品验证

`eval-workspace/{taobao,pdd}`内是本任务生成的普通合成输入，不是商家真实数据。每平台各自执行CSV、XLSX和缺口案例，真实产生3个目录、共15个文件（包含receipt）；在`offline-reports/`保存。全部文件摘要/长度、JSON/HTML内容、独立算式、格式等价和输入保留由`verify-offline.py`复核。淘宝毛利40%、ROI2：贡献-20元、每广告元亏损0.2元、保本2.5；拼多多35%：贡献-30元、每广告元亏损0.3元、保本20/7。三套拼多多评分独立；1.2%保留0.012；最新观测日10月1日不冒充窗末10月2日。缺成交额/日期/异平台案例不生成完整总额或利润。`offline-verification.json`明确标注这是离线程序验证，非真实模型。

本轮尚未正常退出原App或打开运行中的SQLCipher/Host数据库，也未构建覆盖原App；用户已回复“稍后解锁”。因此以下保持NOT RUN：新App canonical构建及启动、两位实际Native准备/召唤/发送、真实模型调用已安装程序、用户可见HTML打开、实际会话/文件质量读回、正常退出后的SQL/Host/Runtime/安装日志备份与保留比较、同构建重开。未进行任何强杀或绕过锁屏。

解锁后沿同一任务继续：正常Quit并确认进程/端口退出→私有备份当前历史→按工程canonical构建/启动→分别用已准备的合成资料在真实会话生成报告及review→独立审阅、修复与新版本复测→正常退出比对所有旧记录→同构建重开。不能将当前离线通过签成整个第二组D4完成。线上商家后台/账号验证不属于离线适配路径，仍为NOT RUN，不影响上述本地验证待办。


## 解锁后真实验收与0.1.1修复（进行中）

已正常退出旧App并确认Host/Runtime/worker及18081释放，私有备份SQLCipher、Host Bolt、Runtime JSONL和已安装资源。按 `scripts/run-local-demo-fast.sh --packaged` 完成0.13.0构建；实际UI准备、召唤两位0.1.0，Kimi-K3/max、ask/on-request，各自执行CSV、XLSX、缺口三组普通合成资料。共32个真实模型产物，包含6组报告和两份review。输入保持不变；程序算式、CSV/XLSX归一值、文件收据独立核对通过。该轮原报告和会话原样保留，不签为最终通过。

发现并实修两类问题：

- 报告把评分/率不适用的总额、正常空错误项显示为“待补充”，比例快照未呈现在HTML；模型review把未知毛利成本含项断言为未包含。新增独立0.1.1版本，按字段语义渲染“不适用”“无计算缺口”，补可追溯比例快照；角色明确成本含项未知时不可判定已含/未含、receipt仅列另外4个文件、格式等价不等于来源字节相同。旧0.1.0及全部前序56资源保持精确不变。新bundle0.14.0：58资源、20版本、15位最新专家。
- 两任务正常重叠期间，Native协调器仅监听首个活跃session至终态，但其定时dispatcher已启动第二任务；Host有界重放使第二任务早期事实未完整投影。0.1.0拼多多实际Native只有14个item、28条fact且出现item_start_not_observed，Runtime原始记录完整。修复现有 `ConversationApplication`：同一协调器并发轮询各session既有SSE观察器，保留唯一outbox dispatcher并动态发现新任务；单会话直接入口保留原行为。完成一个观察器不取消在途提交；快照中刚完成的会话正常跳过，其他错误仍走原恢复路径；停机仍执行现有lifecycle检查及flush。无新调度引擎、无新权限、无wire/数据库migration，不重发旧任务、不合成或隐藏旧会话事实。

新增正常重叠回归覆盖初始1/2个已发现会话、第二个在首个结束前打开SSE、两组完整user/final事实、无diagnostic以及已完成快照。原直接SSE下的正常interrupt调度和最终对象落库回归继续执行；不使用强杀、故障注入或破坏性fixture。

0.1.1 manifest `d5bf48f6ea6e9fad6ed51a80c02bf8c13ab7ec92c1589b4875166f7d029ea2b8`，authority `0d642a31a37d0a609b686fe111b27c2255ba96a8d2109c5378cd227c6fdc60be`。Host来源锁经canonical freeze更新，未修改门禁。Native仅私有观察调度语义变化，公共Contracts字段N/A：没有改动事件格式/Runtime API/SQL版本。回退可恢复旧二进制及候选指向，安装版本和历史均保留。

0.1.0正常退出后比较：原12会话/83消息/42turn及所有旧fact/view/绑定不变；仅一条market dispatch更新时间变动。Host原190条记录仅4条session更新时间变化，安装journal原4117条记录完整保留；增加两次实际准备和会话。另存before-repair私有备份，包含14份Runtime历史和355份安装文件。

HTML打开采用TextEdit静态文档导入，已实际显示首轮标题和表格并发现上述问题。浏览器工具拒绝file协议，未通过其他浏览器/本地服务绕过；CSS浏览器渲染NOT RUN，不与静态打开混记。修复后新会话/产物和重开检查仍待完成，不能用离线通过替代。


## 0.1.1真实复测结果（2026-10-17）

按canonical `--packaged`更新本机现有项目构建App，bundle0.14.0、daily profile、release=false。App内正常准备两位0.1.1、召唤至草稿、显式发送；保持Kimi-K3/max与ask/on-request，不选择连接器。淘宝14:48:31开始、14:59:08完成（636s）；拼多多14:49:04开始、14:56:49完成（464s）。两任务重叠约465秒，使用相同的已确认普通合成输入，真实读取已安装0.1.1程序，各生成CSV/XLSX/缺口三份报告及独立review。没有用旧报告冒充新产物。

| 项目 | 实证结果 |
| --- | --- |
| 淘宝天猫真实会话 | Native `01a1489e-8905-77b0-849a-374dc2dabd12`，Runtime `01a1489e-8964-7ba0-adab-d1f96e55ef76`。44次真实exec_command；3次已安装helper生成，2次plan更新；完成 |
| 拼多多真实会话 | Native `01a1489f-0977-7881-84ce-9ad8dc040a1c`，Runtime `01a1489f-09cc-7753-8016-1700ed1dd13e`。34次真实exec_command；3次已安装helper生成；完成 |
| 实际文件 | `eval-workspace/live-taobao-v2/`与`live-pdd-v2/`各16文件，共32。每份报告5文件，收据仅登记另外4文件；6收据的24条hash/bytes全部匹配；review不冒充受原收据覆盖 |
| 独立数字与口径 | 淘宝贡献−20、每广告元亏损0.2、保本2.5；拼多多−30、0.3、20/7。1.2%→0.012、真实0保留；三套拼多多评分独立且为10-01观测；不合成健康分；日访客累计非周期去重。6报告通过独立检查 |
| 缺口 | 缺成交额/毛利时保留null；缺日期/异平台隔离；窗外正常排除。只有已知消耗50，完整总额/ROI/贡献null，不判定亏损；partial如实显示 |
| CSV/XLSX | 归一值和计算相同，来源路径/hash/sheet保留不同。淘宝逐叶59差异独立确认：49个sheet、5个path、5个sha256；没有宣称原文件字节相同 |
| 内容质量 | 完整人工读回两份review及最终回复；均明确毛利含项未知、未另行扣费、非净利润。旧0.1.0错误表述已通过新版本真实输出复测，无默认费用或现行平台规则臆断 |
| 打开文件 | 六份HTML逐一通过TextEdit原生Open对话框静态导入，标题、中文、表格、正常/partial、率与独立评分内容可读。没有保存/修改文件。浏览器CSS渲染仍NOT RUN，原因是工具禁止file导航 |
| Native实际投影 | 淘宝89项/182条fact，拼多多63项/128条fact，均完整item-start/item-complete集合相等；44/34个commandExecution与真实Runtime命令数一致；用户消息各1、终态completed、diagnostic=null。修复真实覆盖了原串行监听缺口 |
| 安装与提交 | 两位0.1.1 prepare succeeded、绑定ready；dispatch accepted/issueCode=null；create_session/start_turn outbox均done、attemptCount=0，未重发/伪造终态；原0.1.0会话保留 |
| 正常退出 | Cmd+Q正常退出，canonical进程exit0，App/Host/Runtime/worker全部退出且18081释放；无强杀。随后才进行数据库只读比较 |
| 历史保留 | 初始12会话/83消息/42turn及旧fact/view/绑定完整保留，现16会话；一条Native dispatch仅更新时间变化。Host旧190条仅4个更新时间变化；4117条旧安装journal精确保留；12份Runtime文件、281份旧安装内容字节相同。before-repair额外保留14会话/87消息/44turn、14份Runtime、354份安装内容和4119条journal。前轮V1报告也未改写 |
| 构建一致 | 102个App文件+5个Host/Runtime/worker文件，107摘要均匹配canonical回执；二次独立打包60个产物文件逐字相同；所有前56资源metadata/归档不变，171份WorkBuddy及用户归档原件不变 |

最终检查：Skills全量lint/test PASS（99项Node，含82项Python业务用例；140条eval仅格式），Host全量lint及真实候选focused race PASS，Native43项正常focused PASS，UI13文件141项PASS，retained资源2项PASS，Desktop完整 `make lint CONTRACTS_DIR=.local/demo-fast-contracts` PASS（严格来源、ESLint/TypeScript、fmt/all-targets Clippy）。第一次新增测试使用多余Vec被Clippy拒绝，改为数组后完整门禁重新通过，未添加allow或放宽门禁。Meta自身pnpm lint/test50及shell语法PASS。

额外递归全工作区命令与本组规范范围分开：默认Meta make lint使用dirty sibling Contracts而拒绝，采用现有canonical绝对CONTRACTS_DIR后相关仓及Contracts校验均通过，但递归到未改动Infra时本机Docker缺Compose子命令（unknown -f）而失败；没有隐藏Docker、跳过或降低该门禁，不声称11仓总lint通过。Meta递归make test在已通过自身50测试后，停于未改动Runtime原有build-input-only.sh非可执行检查；未改变其权限或运行禁止的后续故障套件。组方案第7步要求的受影响仓完整lint已全部通过。

上述证据位于Desktop `.local/thirteen-second-group-20261017/`：`repair-checks/`、`repair-packaged-launch-receipt.json`、`v2-runtime-execution-evidence.json`、`*-live-files-v2.json`、`v2-static-open-verification.json`、`v2-native-acceptance.json`、`final-history-preservation.json`和`repair-source-preservation-final.log`。私有备份不含凭据。没有commit/push/发布；未执行真实商家账号/后台操作，合成数据不代表真实店铺业绩。浏览器CSS、线上规则/账号以及上游全部自动识别能力未被本组本地接入替代。


### 同构建重开与最终状态

`--packaged --reopen`通过严格回执复核并显示“Same-build expert reopen verified”，readyz=ready；未再次构建或更换程序。UI实际重新打开两位0.1.1会话，分别保持completed/636s与completed/464s，原始用户输入、完整答复与专家版本恢复，无内容丢失提示。原京东会话仍绑定0.1.3并显示旧M03答复；首轮淘宝会话仍绑定0.1.0，不被新目录静默升级。专家目录仍15位且全部资源已准备，无专家团。重开后没有发送新任务或读取运行中的数据库；App停留在专家页面。

第二组本地真实接入、文件产生/静态打开、内容复核、受影响仓全量lint、正常退出/重开及历史保留在上述范围内通过。未执行项保持前述限制，不扩大为原上游全部能力或商家后台通过。最终入口为证据目录 `handoff-status.json`，前轮候选/未完成状态已另存initial文件，失败样本及全部旧版本保留。后续第三组仍应完整回顾28号方案，先核对统计及真实浏览器依赖；本轮没有提前接入其他专家。

2026-10-17 后续环境修复：Compose 并非未安装，而是用户级发现链接指向失效的 AppTranslocation 路径。恢复到本机已有、签名及摘要均匹配工程记录的 Compose 5.3.0 后，元仓及全部11个子仓的标准全工作区 lint 已 exit0。该阻塞已关闭，详见[31号修复与完整复验记录](31-workspace-compose-lint-repair.md)；上面的失败保留为当时记录。
