# 第六组：亚马逊1688找货源专家接入

2026-10-17，local + demo_fast。用户指定剩余两位中的1688专家，复用既有专家与LinkFox架构，保留原专家和历史；无账号真实验证继续跳过。

## 方案与范围

回顾17的完整审计方案与18—24的累积实施：唯一ROLE/知识精确引用→canonical资源包/收据→Native绑定/outbox→Host合成→已选LinkFox/逐次审批→原工具历史。新增专家资源，不引入第二套执行引擎、连接器、OAuth、数据库迁移、后台轮询或专家团。

`contract-impact=semantic`：新增可执行内容和本地候选部署pin；experts/1、manifest v3、MCP代理、权限与持久化wire不变。权威源为Skills版本及内容摘要；Contracts公共schema变更N/A。旧50资源（38普通+12专家版本）保持，新增0.1.0并升级bundle至0.10.0。回退时同步兼容Host/Native与资源pin，保留已绑定版本和原归档，不用全局开关替代单专家停用。

原包2.2.0共44文件、14子技能，导出与WorkBuddy缓存逐文件SHA一致；只作为来源资料，不执行其指令或网络脚本。接入重点是明确ASIN/站点/offer/SKU/报价口径与缺失成本：不按文件顺序绑定货源、不借其他ASIN历史、不把广告词缺失当0、不把ACoS当TACoS，不使用默认汇率/费率补利润。退货按增量损失处理，防止重复扣采购与配送成本。

保留数据检索、候选货源比对、来源回执核对与本地计算/报告。自动公开上传、来源包HTML脚本注入、未声明JungleScout/skill-creator依赖、自动反馈不接入。仅使用已授权公开图片直链；缺少直链或账号则明确阻塞相关阶段。公开GET只用于核对官方文档，不请求业务API、账号认证或付费服务。

实施证据：`yijie-desktop/.local/sixth-group-1688-20261017`。以下结果在完成审计和检查后补齐，当前不声明通过。

## 完成的接入

新增`linkfox-expert-1688-sourcing-expert@0.1.0`，运行资源名`sourcing-1688`，17个文件：唯一SKILL/ROLE、7份参考、离线脚本、合成示例、checklist/eval/notice。10个检索方法复用已接入的LinkFox `proxy_call`，没有新增连接器，目录仍60/revision9。原生卡片10位（原专家+9位新增已接入）、展示1位（行业研究员），总11位，无专家团。展示卡转为原生安装/准备/绑定流程，仍不自动发送快捷问题。

本地脚本有三个实际可执行阶段：prepare生成明确参数；observe核对真实形状回执、ASIN/站点/offer/niche并保留来源；calculate重新检查原始观察、逐项验证报价与17项成本，生成JSON与本地静态HTML。只有候选不等于已验证同款。查询实际执行由原生工具/审批链负责，脚本不含网络客户端、凭据、shell子进程或后台任务。

定价/费用并不完全由公开回执覆盖：直接观测值仅允许匹配的供应商price、Keepa当前price或明确历史采样value；费用、汇率、数量和退货模型由用户提供资料或明确确认情景录入，不能自动猜测，不能把模型假设说成用户已确认。FBA原资料“元”单位含混，未擅自转成美元观测费用。当前版本提供人工核对规格/报价后的计算，不宣称全自动询价、供应商资质认证或完整会计净利润。

## 接入后的深入代码审计

同一Codex在实现后再次审阅，不冒称独立人工审计/平台认证。范围涵盖本组全部运行文件与增量、原利润脚本/主流程/Agent/API参数、上传/报告/预筛选/路径辅助实现及所复用的受管资源、会话、MCP执行和审批核心链。44个来源文件均清点校验；原模板和头像保留来源摘要，不作为运行指令。未审计第三方服务内部实现或整个Runtime。

| 审阅面 | 问题与落地处理 |
| --- | --- |
| 历史价格 | 原ASIN匹配失败取第一份历史。现在对象/数组都按完整ASIN唯一匹配，无匹配/重复即停止；历史点必须有时间，不自动取最高/众数充当正常售价。货币回显不符拒绝。 |
| 站点与身份 | 原源数据可能按文件顺序分配货源。现在US+target_asin与实际请求一致，顶层和所选Amazon行的站点回显不得冲突；供应商offerId独立于products.asin。错目标/错offer/重复offer不计入结果。 |
| 来源证据 | observe保留query/request/原operation_id/captured_at/原始结果摘要；calculate重新核对原始回执，不接受手工normalized结果替代。重复operation ID不覆盖，失败来源记录到source_failures。来源标记只防误用，不能证明授权/服务器真实性；Native原工具历史仍是权威。 |
| 规格与报价 | 明确variant、每采购单位、采购数量/MOQ/阶梯与确认来源。数量不得低于确认MOQ或所选源行quantityBegin；矛盾需更新报价证据，不靠改小数字通过。列表price不自动证明特定SKU成交价，保留询价/资质待核实。 |
| 细分市场 | 精确nicheId唯一选择；不按第一条、包含关系或模糊标题自动套用；行业数据不自动进入个体成本。 |
| 广告与销量 | 缺SP词数保持缺失，真实0也不推断零广告；不将ACoS当TACoS，不用竞品历史销量乘单位利润形成预期月收益。monthly_profit始终空。 |
| 缺值与计算 | 17项均要求有限非负Decimal、精确单位、日期、来源、说明；售价/采购价/汇率/换算数量需正值。0必须明确给出并说明，空/null/false不当0；缺项保留incomplete、profit/margin/rank为空。 |
| 退货公式 | 基础成本已扣采购与配送；退货只增加退款收入损失、管理/处理成本，再扣可返佣和可回收成本。约束退货率≤1、退款≤售价、返佣≤原佣金、回收≤采购+头程；净收入0时利润率未知，负利润照实保留。 |
| 结果报告 | 本地静态HTML转义所有数据，不导入原模板的模型HTML/JS/CDN；生成新目录，保留输入原字节，不覆盖历史报告。报告同时列全部假设、缺项与源失败，不把缺项表当完整结果。 |
| 错误/容量 | MCP isError、业务非200、未知状态/结构停下；成功code="200"/errmsg="ok"正确识别。完整请求16KiB、结果64KiB，超限不截断或偷偷重试，页码/范围变更再审批。 |
| 专家安装/会话 | 现有ROLE/knowledge/archive摘要、安装receipt、原Core journal、outbox/精确ExpertRef、retained保护与旧新版本共存保持；只更新canonical来源pin和测试期望，无新持久化模型。原生测试验证隐私字段不会投影进卡片。 |
| LinkFox | 生产registry/OAuth/凭据/Broker未修改；generic.rs仅新增cfg(test)模块。复用当前schema冻结、精确安装和scope绑定、write风险/ApproveOnce、单次执行许可与正常close；拒绝0执行，批准1次，重复consume拒绝。 |
| 权限与历史 | 仍为既有ask权限、专家内置web_search disabled；资料搜索走已选择LinkFox，不绕过原策略。Runtime和Contracts本轮源码均未改变，日常数据库未打开写入，运行App未替换。 |

复审补充并已修复：历史币种/采样时间校验、源MOQ矛盾校验、所选行层级的站点冲突，以及普通未知历史集合结构的受控拒绝；均补回归并重新打包、同步摘要、canonical冻结Host来源及重跑受影响检查。没有通过删校验、放宽门禁或手工伪造摘要解决失败。

原包的公开PUT上传、自动媒体下载、HTML/JS注入、反馈和未声明JungleScout/skill-creator未导入。标题/图片对照只是相关性检查；看不到图片要说明未核对，不能伪造视觉相似分。此版本不提供原包自动AIGC相似验证任务；用户已有公开图可以通过实际会话看图能力核对，真实模型效果未验收。

## 检查与证据

证据根为`yijie-desktop/.local/sixth-group-1688-20261017`。所有测试使用普通合成输入、正常拒绝、临时/内存状态与in-process MCP，正常关闭；没有强杀、权限破坏、可执行替换或攻击fixture。全量lint已运行；宽泛历史测试中涉及用户禁止行为的项目未执行，不计为PASS。真实账号验证按用户明确要求跳过。

| 检查 | 结果 |
| --- | --- |
| Skills全量lint/test/打包 | PASS，`skills-audited.log`；65项测试、92条合成eval结构检查。新增20项1688测试，含每一费用缺失/null、普通错ASIN/offer、来源顺序、原始回执重新核对、币种/时间/MOQ/站点、负利润/退款公式及静态报告。eval不是模型效果评分。 |
| Host全量lint与实际资源 | PASS，`host-complete.log`；4组race测试覆盖最终51资源/13专家版本、实际安装/读取、原39资源升级保留、Core journal生命周期及三组旧新版本会话绑定共存。新增专家用canonical实际包安装至临时目录。 |
| Desktop全量lint | PASS，`desktop-lint-complete.log`；`make lint CONTRACTS_DIR=.local/demo-fast-contracts`覆盖generate一致性、ESLint零warning、vue-tsc、cargo fmt及all-targets Clippy。沿用工程已有干净历史Contracts检出验证历史锁；当前专家/Host候选另行核验真实来源，不绕门禁。 |
| Native实际目录/连接器 | PASS，`native-functional.log`四项；最后内容摘要更新后在`native-complete.log`重跑实际包加载/安全目录投影两项。目录10位最新专家、38普通资源隔离；60连接器和无账号不能启用规则保持。 |
| 当前来源与权限门禁 | PASS，`resource-sync-complete.log`、`source-freeze-complete.log`、`preflight-complete.log`；canonical生成/同步/冻结/核查一致，原38普通包不漂移，FEAT-137永久退役权威保持，历史acceptance NOT PASSED不被改写。 |
| Connectors全量lint与协议 | PASS，`connectors-checks.log`（Go vet/catalog race、固定Runtime库来源、Rust格式/Clippy）；新文件另做rustfmt检查。`worker-functional.log`共8项普通检查，新增5次显式检索的真实generic backend/in-process MCP流程；原图片/视频、LinkFox/Sorftime逐次审批、60注册、认证metadata模式通过。 |
| UI与构建 | PASS，`ui-complete.log`4文件79测试，新增专家复用准备/绑定/预填链且不自动发送。`ui-build-final.log`前端构建通过，既有大chunk提示保留。没有CSS/组件布局变更；未运行真实App主题/最小窗/模型E2E。 |
| Contracts/元仓 | 全量lint PASS，`contracts-checks.log`；保留既有OpenAPI未使用组件warnings。元仓`meta-checks.log`lint、50测试与shell语法PASS。本轮Contracts无源码增量，不宣称解决第四组全局breaking检查的历史远程schema EOF，未以本轮lint替代该独立兼容门禁。 |
| 资源与历史保留 | `preservation-complete.json`：原50条manifest和50归档逐字节一致，9个日常已安装版本文件匹配canonical；9旧Runtime会话文件、110旧资源/收据摘要一致。未修改日常数据库，不对动态WAL作虚假一致性承诺。 |
| 架构源码保留 | `architecture-source-preservation.json`：Contracts531和Runtime5575个基线文件未变，连接器13个注册/鉴权/审批相关基线文件未变；仅generic新增测试模块。 |
| 示例产物 | `synthetic-report/report.html`、input.json/inspection.json；明确合成数据，实际计算贡献利润10.56 USD，external_calls=0，不是商家利润或在线服务验收。 |

过程中正常门禁如实拒绝过未同步资源文件集，以及未显式设置local/demo_fast的资源同步调用；按canonical同步和显式环境流程修复。第一次Vitest按子串匹配还扫入`.local`历史检出测试，失败来自旧快照；后续明确排除历史检出，仅运行当前4个目标文件，无改写旧测试或产品门禁。最初写测试的命令相对目录错误，没有生成文件，修正路径后执行；日志不冒充成功。

## 最终候选与未执行项

- Bundle `0.10.0`：`yijie-skills/dist/skills-experts-sixth-group-v010`，51资源=38普通+13专家版本；10原生+1展示。
- Manifest SHA256：`64723002cfb078cba6f2cdab3af94cf57c85bda112d56543b83c9ba0b2045f07`。
- Authority SHA256：`636ef48ba071c70f0514d463d2cd9f108e7f1023f818bc67ed390568df4ea350`。
- 内容源树：`748c3506baa76bea99f13c033dc305d9e694a15903bd759b453131909708fc4b`。
- experts Contracts source lock保持`fe49fb6cd83e11dba69861025a23a8faf1d9d3740c887c1716a3637eb34154cb`。

这是release=false的本机开发候选。未构建/替换正在运行的App，源码完成不等于旧二进制已经更新；未提交、推送或发布。第三方再分发许可未核实。

按用户指令NOT RUN：LinkFox真实OAuth/工具资格/当前schema、付费数据/图片外传、实际ASIN/供应商匹配质量、询价/资质/同款验证、真实财务费用与模型效果、真实App D4。没有账户，不读取/搬用WorkBuddy登录态。不把自动上传、自动AIGC验证或供应商认证列为“已实现但仅缺账号”；这些不在当前落地能力内。

剩余**行业研究员**仍为展示态，继续按17方案单独处理其数据、搜索与产物依赖。
