# FEAT-164 S4 方案A：原生失败终态与历史重放修复

2026-10-25，Owner明确批准最小Runtime核心与补丁、Contract First投影和下游验证；本地提交、不推送，新增真实模型HTTP=0。旧账本、14.188544元unknown预占、14.328134元累计上界及2/2已用HTTP全部保留。授权允许实现本修复，不等于S4/G3/final或发布批准。

最终结论：方案A的原生子代理终态与新历史重放缺陷已修复，并在真实canonical Runtime的安全本机验证中通过。最终来源为Runtime r4 `a28130a` → Contracts `1b357cc` → Host `b9155a3` → Desktop `2fb8989`，本轮最终contract-impact=breaking；下文初始semantic判断已由完整writer兼容审计撤回。普通App构建完成，未启动；完整FEAT-164仍为IN_PROGRESS。以下记录保留实施中的失败和纠正，不将中间结果冒称最终资格。

## 起点、事实与设计

起点Runtime074417e5 r2、Contractseddc64f、Hostdf06a3c（产品cac2d4d）、Desktopa0a4743。822份旧证据、496项既有工作区文件、154资源、119当前App项及7日常DB已摘要封存于s4e-start-baseline。30的两次实际产品FAIL保留，不重跑旧r2相同失败；仅在新候选就绪后执行有区分力的安全离线验证。

Fact：原生agent单事件投影把Error覆盖为Completed；rollout过滤Error，旧thread_history reader本身已能读取同一Error结构并标failed。推荐在原生最小处修复，不在Host/UI猜测终态。采用既有ErrorEvent结构和affects_turn_status分类，持久副本使用固定通用文本与原类型码，不保存原始错误正文；瞬时StreamError、不影响turn的rollback/steer拒绝仍不持久化为失败。agent终态对同回合Errored→TurnComplete保持错误，TurnStarted正常重置，TurnAborted/Shutdown仍走原规则。正常空答案完成不可反推失败；旧无错误证据的历史保持未知/原解释，不回填。

本轮contract-impact=semantic（需方向性验证成立，否则升breaking）；整体FEAT-164保持breaking。没有新增app-server/rollout枚举或字段，原生已支持ErrorEvent的旧读取器仍可读新失败事实；该兼容判断须以canonical schema零差异、旧reader原有逻辑测试和真实新候选重开验证支撑。不启动旧Runtime读取新产品库，不改日常SQL或旧rollout。新candidate独立r3目录拒绝覆盖r1/r2/legacy产物。

已考虑方案：新增失败事件会扩大旧reader不识别风险；只让Host改completed会遗漏原生父子工具消费者；复用已知Error结构并对持久副本脱敏，是当前最小可验证路径。待证明：turn重置/取消、不影响turn错误、两种history模式、持久过滤实际接线及新候选冷读。错误与完成必须由原生事实决定，不按正文或空回答归类。

## 实施与验收顺序

1. 固定上游原样保留，只新增0009可重放patch及独立r3 canonical build/check/manifest；安全focused tests覆盖错误→完成、下一轮正常、取消和非turn错误，持久脱敏及旧reader重放。
2. 新Runtime源本地提交后标准离线构建、schema对比、normal-EOF握手；旧r2和全部旧证据不改。
3. Contracts从不可变Runtime源与canonical产物生成精确投影，所有适用支持基线与源码/生成一致性检查；然后本地提交形成consumer可消费引用。
4. Host/Desktop通过原生成/同步入口精确pin，不新增状态推理层；安全loopback验证旧loaded子代理首次/后续拒绝的errored、thread/read新历史failed、正常退出重开保持、显式新模型恢复成功、已有自动压缩/父子迁移子集。0真实调用，不用故障注入、强杀、权限破坏或替换运行程序。
5. 完成后审计本地提交隔离、所有旧哈希、清理和未执行范围。完整S4/G2V/G3/final及计划/恢复UI/跨平台仍按实际资格判定，不借本批次放行。

任何同指纹第三次失败触发治理停止和RCA；正常退出失败保留现场并停止，禁止强杀。本文执行结果在实际检查后补充。

## 下游验证发现

首轮Renderer为旧a0a4743干净来源，12项中11PASS/1FAIL：旧FEAT-132 fixture仍发送schemaVersion3，但已生成的当前私有边界明确为4。这不是r3引入的执行状态回归。保留原失败日志；最小修正测试fixture为4、未知版本断言为5，不修改产品validator或放宽未知状态拒绝；追加空内容下failed/completed/interrupted三种原生read终态保持，验证下游不按空答案猜测。该修正属于本轮当前投影的验证材料。

首次pnpm exec发现工作区依赖布局后自动复用缓存重装少量包（日志downloaded0）；后续改为直接运行已安装vitest入口，避免重复依赖装配。未更改依赖清单/lock，原跟踪源码与资源保留性仍按起点hash核验。

## 审计追加：计量一致性修正

r3源`0b92fcb0a270d0da89ea0d90f07f20e53d9d17ba`的9个focused用例/Clippy通过后，持续审计定位到逐回合post-filter字节统计仍复用原错误长度，而batch统计已使用脱敏后长度。此问题不影响子代理错误事实，但属于本修复新增的计量一致性遗漏，必须在consumer资格前修正。保留r3全部源/0009/正在正常完成的canonical产物，不强停、不覆盖、不供下游使用。

独立r4在原9补丁后增加最小0010，仅分开保存内存中的原始与持久化字节长度，逐回合post-filter使用后者；不新增遥测输出字段、不改变真实Provider usage/费用。新普通合成ErrorEvent用例对照实际序列化持久字节，验证batch与turn两级一致。后续消费目标改为r4，既有r1/r2/legacy与初步r3保持。

兼容性复审将本轮最终分类提升为breaking：旧r2解析器能读已有ErrorEvent，不代表旧writer能保留新增持久错误事实；其原持久过滤器仍会丢Error，不能宣称旧写路径往返兼容。只证明旧reader结构可解释及新reader读旧历史，旧writer写新历史组合不支持；精确Runtime/Host/Desktop pin维持组合边界。回退限定匹配r4的兼容reader并暂停Kimi执行，不回退r2 writer、不改历史、不启动旧Runtime读取新产品库。初始semantic为待验证判断，现由完整持久链审计撤回，整体FEAT-164原breaking不变。

Host测试扩展静态检查曾两次报同一harness编译错误：ResumeThread误传cwd第三参；首次shell后续文档命令成功掩盖了组合命令退出码，复审原日志发现后按实际两参签名修正。原两份错误日志保留，单独命令`s4e-host-vet-corrected.log`实际exit0；未发生模型请求，不把首次组合shell成功记作vet通过。后续检查使用独立退出码。

旧writer保护落实在Host已有受管文件权威：新K3.1配置仅增加固定writer-v1注释，native参数必须逐项相同；升级只接受精确已知r2配置，未知用户内容仍拒绝，旧K3前身许可规则保持。原r2 Host的精确字节preflight不能接纳该新标记，从正常入口阻断旧writer；新Host可正常重开，回退使用新组合暂停执行。采用原权威函数与冻结旧字节的普通本机配置测试，不运行旧程序读新数据库、不改权限或现有用户文件。

本轮新增持久ErrorEvent副本仅含固定文本和已有类型码；原生live错误通知及既有父子工具返回语义保留，不把该修复宣传为对所有历史工具正文的统一脱敏。S4e真实Runtime driver加failfast，任何断言/正常清理失败停止后续用例；禁用Go全局强制测试期限，由各fixture自身协议/正常Shutdown边界收敛。

## 本机资格环境与隔离审计修正

首次新Runtime运行的原终态断言均通过，但新增扩展用错已加载线程resume API，Host如实拒绝effective model profile mismatch；没有旧模型出站。源码确认loaded resume忽略覆盖参数。仅修正测试为stable turn/start显式model字段，验证同一Session错误→正常下一轮，Host冷迁移仍由原graph场景独立覆盖，不冒称Host暖切换已通过。

修正后7项原生测试实际全部PASS，但Go -json把长Output切成1024字节块，旧汇总器只识别14/23请求而判FAIL。修复汇总器按package/test重组逻辑行，再对原始日志做独立只读复核：原native exit0、artifact/test摘要一致、提交间无产品或Go测试变化，复核追加HTTP0。原失败汇总与日志保留，不重新调用Runtime来掩盖观测错误。最终权威为s4e-native-terminal-rechecked；原观察来源371c86a、汇总器b9155a3，非同一提交运行须明确区分。

Desktop隔离提交预检发现原工作区同名旧测试已有用户改动，写入前拒绝。临时15项Renderer绿色仅保留为诊断：撤回隔离树内对原测试的修改，改为FEAT-164独立文件，最终本需求3项+原timing4项共7PASS；原工作区文件与未提交修正不入本提交。旧基线原测试的schemaVersion3/当前4不一致仍保留，不能声称整个前端suite绿色。

App预检曾因Desktop尚未提交、Contracts依赖目录symlink被Git视为未跟踪而停止；后者改成正常被忽略的node_modules目录内复用已安装依赖，不改.gitignore或产品源。第一次实际canonical prepare-only又在普通Skills缺少固定10c45be检出时失败，日志另存missing-skills。完整审计确认普通38包固定10c45be，专家固定595c927；已新建独立10c45be检出，未改变原Skills HEAD、专家pin或现有资源。所有失败均在App启动前，新增真实HTTP0。

旧资格目录中的Runtime实际是指向原Runtime仓的既有symlink，因此随本轮已批准Runtime提交前进；这不是独立冻结checkout。其它五个旧资格入口的HEAD未变，旧074417e5 Git对象、r2 binary/manifest/schema和旧App均保留。保留性报告须区分这一获准源更新，不能错误宣称六个旧入口HEAD全部未变。

第二次canonical准备在嵌套技能同步阶段拒绝Host来源。完整调用链审计确认原因是本轮临时wrapper选了18164端口，现有local-permission候选只认可18083；首层有显式Host路径而嵌套层没有，因而进入旧固定Host分支。没有更改或放宽该校验，也没有准备旧Host绕过；恢复既有已审阅的18083配置后再构建。此前失败另存meter-profile，流程仍prepare-only，不启动App/真实模型。

## 最终来源与实际验证

| 层 | 本地完整提交 | 验证与范围 |
| --- | --- | --- |
| Runtime | `a28130abb13d0f99a00107cd513a653bae878b77` | 0009与0010可重放补丁；核心6、rollout3、旧history reader1，共10项通过；三个修改包Clippy通过，上游子树原样保留 |
| Contracts | `1b357cce0575c492f3715b316ee5f254051acf80` | r4产物投影、精确源校验、生成/Go vet通过；10个登记/增量基线离线比较通过；安全契约子集15项通过 |
| Host | `b9155a3936c6ff5c6aedd52778d975de52b95d06` | 精确消费投影、受管writer标记，原生终态及辅助验证；最终提交只修正观察器，对前一提交原始记录只读复核 |
| Desktop | `2fb898942cb4c3b81e34feb5169bd861340a4040` | 精确Runtime/Contracts/Host来源；独立Renderer终态3+timing4、Native终态1/历史1、eslint/fmt及canonical普通App构建通过 |

r4标准构建通过，269份canonical schema与r2逐文件相同，normal-EOF握手正常。binary SHA-256为`3821bb6063825bdb0e30e367757117f7b3bc9bca84f0275cbdef9e9c660e1e5f`，manifest为`cf72b3b130c0682676603e75d40e8f4e9afaa6f5ed1a67d6be233726ff94a95f`。release构建有一条未修改上游app-server的unused_mut警告，未隐去；修改包Clippy的`-D warnings`检查通过。

[最终原生复核](evidence/s4e-native-terminal-rechecked/result.json)包含7条Go PASS记录（含子用例/父容器）、0FAIL、0SKIP，6份完整ledger、23次loopback请求。旧loaded父/子冷迁移、退役子代理首次及后续输入等待errored、thread/read失败历史、正常退出重开仍failed、同一loaded子线程下一轮显式当前模型completed、自动压缩和previous-model安全拒绝均实际断言。观察来源`371c86a330de7e482755de15bf90573b7f9c8505`与汇总器`b9155a3`分开记录；原始日志hash、产品源与Go测试源一致，复核本身未执行Runtime、追加HTTP0。不得将其写成b9155a3重新跑过全部原生用例。

[辅助验证](evidence/s4e-native-auxiliary-result.json)3项/9请求覆盖新子代理、显式压缩及普通已授权临时文件复制的Guardian链；[调用面验证](evidence/s4e-runtime-call-surfaces-result.json)4项/6请求覆盖普通、草案、标题及市场辅助入口。全部为合成本机服务，不访问真实模型或商家平台。本轮包括首次扩展误用resume的12请求，总计50次loopback；11次旧K3 producer仅用于正常生成切换前历史，切换后无旧K3 HTTP。只读复核复制的日志不重复计数，合成usage不算真实token/费用。详情见[s4e-verdict](evidence/s4e-verdict.json)。

[App构建](evidence/s4e-app-build-result.json)于20:25:48完成，标准命令为`bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro --prepare-only`，输出位于新的`feat164-s4e-qualification-20261025`。ordinary profile包含38个普通技能包，固定源10c45be；不将其冒称专家/媒体组合构建。收据记录1191项输入、42个bundle文件及Host/Runtime/manifest；App executable SHA-256为`999068669ebd161cd83cb33424addefb07d4132dcbb27f2d7508c0a9c2b0e36a`。旧S4c App 119文件未被覆盖。未启动App、未改变系统外观、未使用日常数据；当前收据仅证明同源本地构建，不代表UI或G2V。

## 审计、保护及未完成项

最终代码复审确认：状态更新使用原生watch锁内的当前状态，不在Host或Renderer推断失败；TurnStarted、取消、shutdown及非turn错误保留明确语义；普通与计量持久路径都写脱敏后的同一ErrorEvent；逐批与逐回合字节计量一致。旧reader结构可读不等于旧writer兼容，Host标记只证明正常受管r2候选入口拒绝降级，不承诺任意手工混用旧程序受到保护。新增持久副本脱敏不扩大为所有已有工具正文统一脱敏。原错误缺失的旧历史不补造。

[保留审计](evidence/s4e-preservation-audit.json)通过：原七仓496项工作区内容在仅逆向本轮已提交差异的临时副本中与起点相同；822旧证据、154资源、7日常DB、119旧App文件逐字一致；r2/legacy及r3中间产物保留。新资格树干净并与产品提交一致；普通Skills独立固定检出干净。原Desktop启动脚本工作区mode为0644，隔离应用补丁时的mode提示保留，未chmod原文件。各仓原分支/远端不变、索引空，无本轮Runtime/App残留进程。原FEAT-163记忆后缀逐字保留，元仓只暂存FEAT-164段落。

[治理检查](evidence/s4e-governance-results.json)中claims、strict、元仓lint、53/53测试与7个shell语法检查通过；S4 G3实际退出1，判定BLOCKED，未放行。旧同指纹两次产品失败及armed历史台账不改，修复后的原断言通过另记remediation；不伪造第三次或RCA cycle。中间API误用、日志观察器、fixture及构建装配失败均保留真实日志，不靠删除断言或放宽产品校验通过。

[静态与范围复核](evidence/s4e-static-review.json)核对Runtime15、Contracts4、Host8、Desktop6个最终变更文件。首次审计器把补丁文件中的10个合法空上下文行误报为尾随空白，并在Runtime允许清单中漏列canonical脚本与治理文档；逐项核对后改用精确15文件清单，未修改已冻结的产品源码或补丁字节。原始diff检查输出保留，只有内容确为单空格的unified-diff上下文标记获语法例外，其它源码diff检查通过。旧失败台账另作结构相等校验，未借本次通过改写历史计数。

下一步在现有零真实HTTP授权内，先为r4新组合建立正常loopback/dummy服务和独立产品数据，完成同源App启动、旧线程显式恢复/取消、计划及历史重开UI；专家/媒体组合需独立同源构建及资源收据，不能套用本次ordinary收据。继续使用正常停止与清理，不能强杀或修改既有二进制。当前未执行的完整UI、计划、其它平台、TCONF-164-04、当前G2V、逐切片G3/freshness及最终三类E2E，仍是FEAT-164完成条件；真实G2V需要新的明确HTTP授权，30元余额不能自行转成调用权限。

本轮未执行攻击/故障注入、权限破坏、旧Runtime写新历史、日常DB迁移、真实模型/搜索/图片或商家业务调用；原因是长期安全条款与当前授权，相关生产能力不据此宣称通过。所有产品及治理提交均仅本地，无push、tag、分支变更、PR或发布。元仓最终完整SHA以包含本文的Git记录为准，避免预填自引用。
