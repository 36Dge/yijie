# 第五组：股票研究专家与量化策略回测师

日期：2026-10-17。状态：真实接入、文件与交互验收、全工作区 lint、本机 App 更新及同构建正常退出重开均通过。仅 local/demo_fast；没有账号的线上验收 NOT RUN。

## 范围与权威

已重新回顾 28 总方案、外部内容附录、33 第四组交付及现有私有专家链路。源包 equity-research@2.1.2、strategy-backtest-expert@1.0.0 与归档各 35 份文件逐字节一致。原始资料只作审计数据，不承接上游宿主命令。

contract-impact=semantic：变更固定资源目录、信任摘要和专家执行指令，兼容原 experts/1，不新增 wire/provider、迁库或全局 Skill。权威为 Skills bundle-source、逐文件审校与 canonical 产物；消费者 Desktop Native/Host 分别更新精确 pin 并验证。原 bundle 0.18.0 的 64 资源、26 版本、18 位专家全部保留。首轮新增两份 0.1.0 资源，bundle 0.19.0；经过 0.20.0 中间候选与真实语义复测，最终交付为 0.21.0。Owner 为当前本地工程实施者，用户已授权实施、真实验证与本机更新，未授权公开再分发。

## 必须关闭的验收

- 股票：多期三表勾稽；税前债务成本只扣一次税盾；WACC 6.875% 独立算例；WACC≤g 不估值；缺净债务/稀释股数不补零；亏损倍数 NM；公式、缓存及独立重算一致；敏感性、模型更新保留原版；真实 HTML/XLSX 与研究文件。
- 回测：单标的日线多头，SMA 交叉或明确收盘信号，下一交易日开盘执行；预热不交易；显式费用/最小费/税费/滑点/lot/最短持有；期末持仓按市值保留；期初权益与首日收益完整；逐笔净收益及现金/权益闭合；普通 5–10 笔成交及零交易等正常边界独立复算；真实 equity/trades/summary、代码及交互报告。
- 两位各真实 App 会话、保存文件、修改后另存、系统应用打开及浏览器交互；准备/召唤不自动发送，精确引用与普通审批不变。所有旧历史及资源保留，正常退出/重开。
- 深入代码审查、普通 focused regression、全工作区 canonical lint；再通过标准 launcher 构建并更新本机 App，精确回执核对。

## 依赖与未纳入能力

运行时采用当前普通 Python3.10+ 标准库，复用已有本地文件交付及受限前台预览方式。工作簿 writer 从工程自有 OOXML helper 显式复制并审查；Codex 的表格工具仅用于独立校验/渲染，不作为易界依赖。没有自动安装软件、外部取数客户端、凭据迁移或后台服务。

原 WeStock 混淆 JS、NeoData 明文代理及自动安装程序排除。在线数据只允许当前已选且合格连接器、现有逐次审批；本轮缺账号不取数。原 15 个有效股票工作流保留任务路由与所需证据，废弃 earnings-preview 不注册。全量首次覆盖大型 DOCX/25–35 图、复杂组合/做空/事件研究引擎与自动在线历史行情不冒称实现。

所有验证使用正常合成业务数据与正常生命周期。禁止强杀、故障注入、权限破坏、攻击性 fixture、替换运行时；不打开运行中的 SQLCipher/Bolt。

本轮证据目录：`yijie-desktop/.local/thirteen-fifth-group-20261017/`。下列保留各阶段失败及修订，最终结论见文末。

## 实施与首轮工程证据

新增两个私有0.1.0包，Python3.10+标准库，自有计算器/报告/受限前台loopback预览。股票15项工作流映射保留；历史三表核对不冒称完整预测三表。回测支持SMA交叉与明确收盘信号；CSV价格导入、无未来价格参与买入预算、费用及未成交原因可追溯。

审查修复：工作簿缺预测输入不再当0；非法增长、权重、缺股数/净债务的公式结果不可用；独立引擎重算和输入改变已实际验证。改进数字格式/输入颜色/长来源行换行。输出复制的代码可在新目录复算，不依赖原安装路径；避免重复叠加CSS。预览仅提供receipt一致的4个冻结静态文件，限制loopback Host，正常stop退出。

普通回归覆盖9组（各含多组正常边界），独立手算9笔成交：期末11094.9157，已实现904.5205，末日400股含买费浮动损益190.3952；没有强平。税盾算例WACC6.875%，企业价值854.627371647993，股权844.627371647993，1000万股每股84.4627371647993。所有均明确合成，非真实证券收益。首轮前缀回归失败来自CSV行尾CRLF解析，修正测试按记录行解析后结果一致，未改计算器迎合断言。

首轮canonical bundle0.19.0：66资源/28专家版本/20位；manifest `c8cdd20ffb221205b68008592162aa5e3e43769d4d2bb84093f4bd8aef0b9f51`，authority `a386f227c6e41bc8be6d96e97225eeabe453c2c894fdd4be848b4041cf4414c3`。两次独立构建68文件逐字节一致，原64资源元数据/归档保留。Host精确来源锁经canonical freeze重建，不手改来源hash或降低检查。

全工作区canonical lint已通过，Docker Compose语义验证通过；Coze仍按工程规定只做integration governance，上游application lint未执行，不扩称其通过。正常退出后备份确认21会话/109消息/55轮、21Runtime历史文件、523安装文件。实际App与更新/打开验收仍待下节，不以这些工程证据替代。

## 首次真实App发现与修订（未以已知问题放行）

0.1.0实际会话`01a14994-c1f8-7842-b000-80f0eda155ae`，Runtime `01a14994-c261-7df2-ae4f-1456df180c87`，正常完成444秒。真实执行installed helper、生成JSON/XLSX/HTML及独立复算代码/备忘录。WPS实际打开，浏览器章节/筛选/键盘与无错误通过，前台preview正常stop。新App的115个构建文件与canonical receipt完全一致。

但语义审计发现备忘录把净利润/EBIT增速差确定归因于经营杠杆（同时承认无成本证据），并把敏感性概括为±1个百分点改变20–40%，不能由情景表支持。数学计算本身正确，问题位于模型研究稿的因果和近似表述。首版业务语义不签PASS。

已正常退出、保存首轮原输出摘要/历史副本，不改0.1.0。新增股票0.1.1：程序输出真实同比、每个情景相对基准变化、终值PV占比及memo-facts.md；上期非正时同比不可用；ROLE与方法明确数值需实际计算、因果需具体来源，缺成本/费用/税项等无法归因，免责声明不能抵消确定断言。新普通测试独立复算派生指标。待使用同一输入新会话复测。

修订bundle0.20.0，67资源/29版本/20位，保留0.19.0全部66资源。manifest `21775b8fdc907ab90e1bcd7834189bf7ca7896dcf13b555f5ed3a0af9bc123bc`，authority `dac924a22c208aba2ce5b51864a98ea41c01821e1133afc9d685b1a0020c0811`。修订回归与真实验收结果待补，不沿用首版作为最终完成证据。

修订首轮全量Skills测试129项通过，但场景格式校验发现复制版本的eval ID仍为v010；已只修正新版本ID为v011，未删除旧场景。重新canonical打包/固定摘要/freeze后，全量Skills与189场景校验通过，修订全工作区lint再次通过。相关失败与复测日志分别保存，不以首次失败为PASS。

## 修订工程检查与实际文件验证

0.20.0 两次独立打包的69个文件逐字节相同，canonical构建回执116个App/Host/Runtime/资源文件与实际磁盘完全一致。`checks-v011`：Skills 129项Node测试、189条合成场景格式校验（非真实模型eval）；Native 43项正常focused测试；UI 141项/13文件；Host `-race`覆盖全部29版本的资源生命周期、旧版共存、同Thread绑定/移除/正常重开；全工作区canonical lint再次通过。未改动的worker复用本轮先前14项Rust+Go catalog正常回归。

股票0.1.1真实输出的JSON、每个敏感性格、同比与终值PV比例已经独立Decimal复算，receipt字节一致；WPS实际打开显示WACC6.875%、企业854.63、股权844.63和每股84.46，关闭时不保存重算产生的脏标记，原字节保留。研究稿明确缺成本/费用/税项不能归因，各情景使用准确计算值，首版两处语义错误已纠正。

量化0.1.0首轮真实会话正常完成，19行权益、9笔成交、4笔平仓、末日400股；独立Fraction现金账本验证所有成交、每日收益、回撤、费用、净收益及短样本NA。Chrome实际章节切换、成交流水sell筛选4/9与清空9/9、权益曲线通过，浏览器无error/warn；CSV在TextEdit实际打开，未编辑。验收preview正常stdin stop退出。

## 自然出现的模型服务限流与恢复

在股票0.1.1首轮末尾和后续会话中，实际上游返回429。正常退出后只读Native终态确认：`responseTooManyFailedAttempts`，`exceeded retry limit, last status: 429 Too Many Requests`。股票第一轮已产生完整文件但未最终回答，下一轮未开始计算即失败；量化第二轮读入后同样失败。Runtime JSONL的`task_complete`只说明结束，不能当成功；Native真实终态为failed，未改写。已保留`before-provider-recovery`诊断与DB副本，按canonical同构建正常重开，等待限流缓解后串行恢复，不扩大审批权限、不换账号规避限制。

## 第二次真实语义修订：版本差异不再依赖模型心算

用户授权改用已配置MiniMax-M3后，两条原Thread均正常续办；原模型/专家历史未替换。股票实际kd=6%产出WACC7.25%、EV793.050642700992、股权783.050642700992、每股78.3050642700992；缺股数输出null，独立复算与WPS实际打开一致。量化SMA(2,3)+最小费8，5笔成交/2笔平仓/末日300股，期末7984.5066、费用46.5934，独立Fraction账本通过。

但稿件审计再次发现模型手写比较错误：股票股权降幅写成7.275868%（正确为7.290402%，应与股数不变时的每股降幅相同），终值写成859而真实850；量化把annual_return与Sharpe两版均null的差值写0，并出现不存在的术语。未把数学正确等同于研究稿通过。

因此保留上述版本、会话和所有原输出，新增股票0.1.2与量化0.1.1。两者加入`--previous-input`：以当前已审校计算器重新计算两份保存输入，校验同主体/币种/方法或同标的/区间，生成previous-input.json、comparison.json、change-note.md并纳入receipt。明确这是当前计算器重算，不伪称复现旧计算器；缺值差值为N/A，上版非正的相对变化不可用；股票同格EV与相对各自基准的变化分开。ROLE/协议要求直接引用程序差异，不重写数字表，研究解释只基于证据。原WorkBuddy上游程序与本易界已审校helper的措辞也明确区分，避免不必要的执行路径误解。

0.21.0候选为69资源/31专家版本/20位，原0.20.0的67项元数据与归档全部保留。manifest `756ce70db4df8158b414a1b114f2a8753c7e40e0847f14911c85fbbbab05f552`，authority `695ff82d093ff3ad4b4eeef8378f1a9d075d36dc43d4e104b2635b79ade19f88`。新增独立比较回归验证正确降幅、终值850、股数缺值、非正上版、不同主体拒绝，以及量化annual/Sharpe空值差不补0；计算器原数值逻辑不变。

最新Skills131测试、201条合成格式场景校验/33数据集通过；Native严格目录集合首次因漏列两条新版期望而失败，补齐期望集合（不删旧版、不放宽断言）后43项重新通过，失败日志保留。最终lint、App与新版本真实会话验收继续进行。用户随后说明Kimi-K3已恢复并建议切回，待当前任务正常结束后已恢复Kimi选择。

## 最终构建与真实功能证据

最终固定bundle **0.21.0**，股票 **0.1.2**、量化 **0.1.1**，20位专家/31个保留版本/38个普通Skills。包第二次独立构建71文件逐字节一致，前版67资源元数据与归档逐项一致。标准 `scripts/run-local-demo-fast.sh --packaged` 构建更新日常`com.yijie.ai` App，118个构建文件、大小、模式和SHA256与canonical回执一致。没有修改Runtime、公共wire、数据库schema、连接器权限或全局Skills行为。

| 最终真实会话 | 版本与模型 | 结果 |
|---|---|---|
| Native `01a149cf-12e8-7210-b034-ce141ea7fbf4` / Runtime `01a149cf-1387-7993-925f-d05dde74e3fb` | 股票0.1.2，Kimi-K3，max，on-request/workspace-write | 同Thread两轮均completed；47次真实exec；基础/更新/缺股数三个新目录、公式XLSX、HTML、JSON、回执、代码、研究稿和复核稿实际生成 |
| Native `01a149da-c996-7622-b5cd-802e02547d99` / Runtime `01a149da-ca00-7c33-ac30-bd53e89e0c3d` | 量化0.1.1，Kimi-K3，max，on-request/workspace-write | 同Thread两轮均completed；42次真实exec；基准/更新两个新目录、三份CSV、JSON、HTML、回执、代码、说明和复核稿实际生成 |

这四个最终turn的Native view均completed且diagnostic为空；dispatch accepted、outbox done、重试次数0；所有原生item started/completed配对，无孤立delta，精确专家引用与revision保持。此前4次429失败不改写为成功，原会话完整保留。此前MiniMax恢复成功证明普通模型切换与原Thread续办；用户随后明确Kimi已恢复，最终四轮使用Kimi。

### 计算、文稿与实际界面

- 股票：独立Decimal脚本不导入产品代码，核对3套FCFF/WACC/估值、各格敏感性与所有6项版本比较；5%→6%税前债务成本使WACC6.875%→7.25%，EV854.627371647993→793.050642700992，终值850，股权/每股相对变化同为-7.290402%。缺股数时每股值、绝对差、相对差均不可用。程序差异文件与previous-input均被receipt覆盖。
- 回测：独立Fraction现金账本不导入产品代码，核对逐笔成交、现金、费用、每日权益/收益、回撤、平仓净PnL和未平仓计值。基准9成交/4平仓/400股，期末11094.9157；更新5成交/2平仓/300股，期末7984.5066，费用46.5934。13项比较指标独立核对，annual_return/Sharpe及其差值均N/A。
- 研究稿语义逐项核对：没有无来源利润归因、无统一区间敏感性概括、无错误版本百分比、无null补0。最后发现的作者身份/基础版文件清单，以及量化13/19行样本数笔误，均通过原App会话续办另存reviewed稿修正，原稿保留；只有修正稿作为最终交付。模型稿不能免审，也不冒称独立人工评审。
- 股票模型自行生成的独立核对脚本曾有递归累积器和Decimal键类型两处错误，均在同轮修正后实际重跑通过；产品计算器/回执没有为迎合断言而修改。验收方另有完全独立的Decimal/Fraction核对，不以模型自评代替。
- WPS实际打开更新版和最终缺股数版XLSX，显示7.250%、793.05、783.05及N/A；关闭不保存，文件原字节与receipt一致。最终量化CSV在TextEdit实际打开，5笔流水可见且未编辑。
- Chrome实际打开最终冻结报告：股票per_share筛选1/7且N/A；量化成交流水5/5→sell筛选2/5，权益曲线/章节切换正常。浏览器error/warn为空。前台preview均以stdin stop正常退出，无常驻服务、无强杀。专家详情/版本、准备、召唤、无自动发送、工作区和权限均在真实App验证。

## 最终工程检查

`checks-v012/`：Skills **131项测试**、**201条合成格式场景/33数据集**；Native **43项正常focused测试**；UI **141项/13文件**；Host `-race`覆盖全部31个资源版本及既有绑定/恢复链路；均PASS。worker未改动，沿用本轮已通过的14项Rust与Go catalog正常回归。最终 **全工作区 `make lint CONTRACTS_DIR=.../.local/demo-fast-contracts` PASS**，Docker Compose语义检查通过；Coze按工程标准仅integration governance，上游application lint仍NOT RUN。未执行用户禁止的攻击fixture、强杀、权限破坏或二进制替换，也不把未执行的全套Rust/Host测试称作通过。

## 数据保留与证据边界

正常Quit后确认App/Host/Runtime/worker进程均退出、18081无监听，launcher退出码0，才读取SQLCipher/Bolt。原始完整db/wal/shm快照逐行比较：**21个原会话、109条原消息、55轮原记录**保留；仅一处已观察dispatch更新时间变化。原Host270行、资源journal4126行保留；原21份Runtime历史逐字节相同，原522份安装文件逐字节相同（journal另按行验证）。当前新增至26个会话。三个中间版本会话的原捕获Native身份、专家引用、turn、dispatch/outbox、view和事件头与最终逐项相同；所有旧输出哈希与5份原输入保持。

辅助`before-v012/conversations.db`仅复制main文件，不能作为完整SQLite终态备份；其缺少WAL而出现的状态滞后不作为数据丢失证据。最终保留结论使用完整的`preservation-before`/`preservation-after`三件套，并将最终完整快照与正常停止的真实库逐表再次核对一致。辅助副本和说明均保留，不伪装成完整备份。

关键本地证据：`live-acceptance.json`、`final-history-preservation.json`、`intermediate-observed-history-preservation.json`、`final-output-verification.json`、`*-independent-verification.json`、`*-comparison-verification.json`、`latest-*-installed-code-verification.json`、`determinism-v012.json`、`built-artifacts-verification.json`与实际UI截图。

所有来源原包/归档70文件未改，12仓HEAD/分支未变，没有删除既有文件、commit、push、发布或修改账号配置。没有账号的金融线上取数/业务验证继续NOT RUN；本地资源ready不等于账号或实时行情资格。完整首次覆盖大型DOCX/图包、自动在线历史取数、复杂组合/事件研究/做空引擎仍不在本次有界接入范围，不冒称上游全部能力。

## 同构建重开终核

正常退出与完整数据核对后，以 canonical `scripts/run-local-demo-fast.sh --packaged --reopen` 重开，日志明确 `Same-build expert reopen verified`。再次逐项核对118个构建文件与回执一致；实际UI恢复两位最终会话、两轮完成状态、股票0.1.2/量化0.1.1精确胶囊及Kimi-K3选择，输入为空、发送禁用，无自动续发。完整专家目录20位均资源已准备；清空验证搜索后保留App在专家页。`final-reopen-*-ax.txt`、`final-reopen-*-card.png`和`final-reopen-catalog.png`记录实际终核。第五组有界真实接入已完成，线上账号依赖及未覆盖高级能力仍按上文如实保留。
