# 新增13位第四组：跨境电商带货口播专家

日期：2026-10-17；最终状态：本组本地真实接入、App/文件验收、代码审计及全工作区lint已完成；无账号线上验证NOT RUN。按28号完整方案和三份附录回顾，复核29–32号前序实现/修复。第四组仅 `linkfox-expert-aigc-videogen-sale`，不是视频复刻专家、Remotion或专家团。沿用用户无LinkFox账号且线上验证跳过的明确条件，本地功能、程序及实际App/文件不可豁免。

## 范围、架构与兼容性

contract-impact=semantic，local/demo_fast。新增私有行为资产和候选pin；公共wire/experts/1/manifest3、SQL35/Host10、权限、provider及外部协议均未变。公共Contracts字段N/A：复用当前引用；新本地产物协议仅是专家工作区文件，不是审批/主业务状态。用户授权本机更新，不是签名发行或线上付费授权。

沿 Skills单ROLE/SKILL/短索引/程序白名单→canonical审校打包→Native准备/精确绑定/outbox→Host每轮校验与普通权限基线→现有Runtime/已选LinkFox。没有第二执行器、WorkBuddy运行时、跨专家绝对路径依赖、全局Skill注册或数据库迁移。保留先前63条资源、25版本、17专家及所有历史。完整前manifest冻结为 `FEAT-158-retained-resources-v0.17.0.json`，逐条metadata及archive验证；旧冻结文件不改动。

部署：先源/普通确定性回归→独立双打包→consumer pin与Host canonical freeze→正常Quit、确认所有owner和18081退出、历史备份→同步及canonical App构建→实际会话/文件→正常Quit后逐行保留比较→同构建重开。回退仅恢复候选和构建，历史与已安装版本保留。不commit/push，不清理用户脏改动。

## 来源与依赖审计

WorkBuddy源2.1.0与用户归档18/18文件字节相同；原件不改动。1 Agent、4 SKILL、参考/配置和头像，实际没有其文案宣称的参数校验、下载脚本。完整配置汇编与安装源、卡片逐字段来源核对。无完整根LICENSE，当前仅用户授权的本机开发候选，不推定公开分发。

已处理：图像推测材质/性能→确认事实+未知项；默认美国/英语→显式输入；按销售地锁种族→中性成年或用户明确演员要求；三方案自动跳过→明确选择+内容摘要；声音强制覆盖→用户必须明确true，不静默改false；相冲突的model/ratio/isPro→审阅共同子集SEED/SEED_FAST、5/10/15秒、16:9/9:16；Fast禁止1080p与isPro；promptOptimizer=false；最终prompt<=2000字符、既有16KiB调用边界不变。

Python3.10+标准库本地helper，无新依赖/网络/凭据。无账号仍能真实生成方案与制作草稿。远端沿已选择、当前schema合格的LinkFox generic MCP，并每次新审批；voice在线行为、额度、费用、实际生成、音轨/口型/商品一致性均NOT RUN。原文HappyHorse/WAN/adaptive/hiddenPrompt/camera矛盾未直接纳入；本地图片上传、自动下载、本地MP4及后台轮询未实现，不冒充已交付视频。

## 本地功能与事实边界

`prepare`：用户brief+恰好3套不同镜头方案，逐条source_text/spoken_text/source_reference台账、未知项、显式受众/地区/语言/演员/参数；真实输出input/inspection/review/receipt四文件并停止等待选择。每镜头仅引用确认claim_id，口播由原译句组成；不在自由分镜字段注入新商品事实。镜头总秒数准确，但实际语速、翻译等义仍需模型/人工审阅与生成后播放，程序不会声称语义自动验证。

`video`：完整原plan与选择绑定SHA256，改源事实/语言/参数/方案使旧选择失效。保留选择原话但该文本不是Native批准依据，必须对照真实用户消息。确定性输出原句、原镜头、原设置和request摘要，始终未提交。缺公共图片URL仍可出方案，无法准备远端请求，不自动上传。

`observe`：记录当前Native工具操作引用、同请求摘要、原created回执；查询只接受同taskId，分created/processing/failed/unknown/video_link_ready。多层错误/冲突/缺结果不会假成功，任何状态都不自动重建；URL不当文件，音视频质量保留not_verified。该文件只用于当前工作区对账，不另造审批或账户权威。

本版交付Markdown/JSON文件，可经系统应用打开。没有把易界现有inert本地链接说成一键打开，也没有新增HTML/MP4 Artifact桥接。界面交互验收在真实专家目录/详情/准备/召唤/草稿/选择会话和同构建恢复执行。

## 实施后审计与验证记录

证据根为 Desktop `.local/thirteen-fourth-group-20261017/`。全仓HEAD/dirty/逐文件摘要及本轮before bundle/authority已先保存。正常Quit后备份20份Runtime历史、508份安装文件和SQLCipher/Host Bolt；没有打开运行中的数据库。

源helper逐函数审阅覆盖字段/类型、唯一事实ID、三方案引用/时长、参数、不截断、选择摘要、URL格式、MCP多层错误、task归属、新目录/文件收据、主流程异常处理。发现query的creation普通类型错误会触发AttributeError，已补类型检查并回归，不留下traceback。文件不覆盖、安装包不生成__pycache__。事实语义/译文/语速不由结构校验冒充。

新Connectors普通in-process测试使用由本helper真实生成的选择2请求（另有跨仓字节语义对照），走生产generic review/execute，确认voice=true、精确prompt/images/时长、原taskId与PROCESSING/SUCCESS；正常close/join，不执行HTTP、不替换二进制。既有broker fresh-decision/exact-ref回归继续运行。此项只证明本地协议，不是线上LinkFox资格。

后续追加真实检查结果、实际文件与历史比较。未完成步骤不记PASS；若发现问题先修复再复测。

## 实际完成的检查与文件验收

新增独立口播 `0.1.0`，bundle `0.18.0`，64条资源=38普通技能+26专家版本，18位最新专家。manifest `c47cf8f90e364a7a091de5fd17885242da174249ab19932ee0170b21dafb11dd`，authority `f669791b29f46d55f9559663b9998d5d76c83da22cb1375747fbc8347ec98741`。producer `dist/skills-experts-thirteen-fourth-v010`，独立第二次打包66文件全部相同；此前63资源逐metadata/archive不变。

| 检查 | 实际结果 |
| --- | --- |
| Skills完整lint/test | PASS，119项Node测试（本组12项），171条eval只做结构校验，不冒充模型评分 |
| Native正常focused | PASS，43项，含实际候选精确26版本/18目录、资源/绑定/outbox及前序并发观察回归 |
| UI focused | PASS，13文件141项；精确producer路径同步，未改控件行为或门禁 |
| Host正常focused race | PASS，实际26版本安装/读取/生命周期、旧JD安装保护、正常版本共存、普通权限/角色组合；无SKIP。修复测试入口遗漏后复验 |
| Connectors正常focused | PASS，14项Rust及Go目录；本组真实helper构参fixture走generic协议，原fresh approval精确ref回归保持 |
| 全工作区lint | PASS，元仓标准`make lint CONTRACTS_DIR=<desktop>/.local/demo-fast-contracts` exit0；包含全部11子仓现有lint。Coze标准仅integration governance，未声称整个上游应用lint |
| 额外worker lint | PASS，canonical来源检查、规范fmt与scoped Clippy，无allow或门禁放宽 |
| 构建 | canonical `scripts/run-local-demo-fast.sh --packaged`成功；local QA/no-sign日常profile，113个App/Host/Runtime/worker文件逐一匹配构建回执；不是生产发行 |

真实App先显示18专家、原17全部ready，新口播待准备；实际prepare成功后14份安装内容与审校源逐字一致，无__pycache__。详情版本/标签/能力边界正确；快捷问题只进草稿，明确发送后才执行。选新工作区且保持Kimi-K3/max、ask/on-request、workspace-write，没有选择外部连接器。

实际Native会话 `01a1494e-fb4c-76c1-87de-2f18c74fa570`，Runtime `01a1494e-fbb4-7dd0-bc6e-ebc8b18825f0`。两轮普通合成验收，18:01:15开始首轮232秒、18:05:41第二轮151秒，共26次真实exec_command，实际运行已安装helper的prepare和video；外部业务调用0。

第一轮从product.txt只提取“米白色桌面收纳盒”“三个隔层”及两句已确认英文，9项未知属性独立保留；3套镜头结构不同，时长均15秒，真实生成plan.json及proposals-v1四文件，停止等选择。第二轮从原文件读取plan与摘要，用验收消息明确选择2，保存selection.json及production-v1四文件；10个新文件不含原2输入。两个receipt共6个文件hash/bytes全部匹配；选方案原话与真实会话消息逐字相同，第一轮7个文件全部不变。

独立复核：原plan摘要一致，方案2为4+6+5秒，原英文口播逐字构入prompt，SEED/9:16/720p/voice=true/isPro=false保持；prompt785字符、request1058字节，未超过既有边界；状态video_prepared_not_submitted、approval_granted=false、current_tool_schema_verified=false、local_file=null，无虚构taskId、视频URL或MP4。完整读回原文/台账/三方案/最终提示词；未把容量、材质、承重、防水、认证、价格、优惠、销量未知写成具备或不具备。

实际打开：TextEdit原生Open分别打开proposals-v1/review.md、production-v1/review.md及inspection.json，中文/英文/摘要/参数可读；截图及AX留证。只是普通本地文件打开，没有冒充易界原本未实现的一键Artifact预览。

真实过程中模型自己的核验命令误从video inspection读取不存在的plan，出现一次KeyError；同轮已改为读取production-v1/input.json，并重算全部摘要/参数/时长成功，独立验收脚本再次全部通过。没有修改正确产物来迁就错误核验，也没有留下待解决问题。审计脚本最初误设新建绑定revision=1，查现有Native新会话初始revision=0后纠正预期；产品协议未改，实际绑定0/ready。

实际Native：prepare succeeded；两次dispatch accepted/issueCode=null，create_session及两次start_turn outbox done且attemptCount0；两轮completed，62个item全部start/complete对应，128条fact，无orphan/diagnostic。失败的自检命令如实保留在历史，不隐藏或改写成成功。

## 历史保留与未执行项

Cmd+Q正常退出，canonical进程exit0，App/Host/Runtime/worker及18081均释放后才打开只读数据库。原20会话/105消息/53turn全部保留，现21会话；唯一旧Native变化是market dispatch的updated_at。Host原260条记录仅允许的更新时间差异，4125条旧安装journal精确保留；20份旧Runtime JSONL和507份旧安装内容（不含可追加journal）字节完全相同。新旧SQL/Host备份位于本轮私有证据目录，未删除或强杀。

本组仍明确NOT RUN：真实LinkFox账号/当前线上schema资格、收费与额度、在线生成/查询、MP4下载、实际音轨/口型/商品一致性与播放质量。原因是用户明确没有账号并允许跳过；本地/普通协议不代替线上证明。WAN/HappyHorse等矛盾参数、多结果/签名URL自动处理、本地上传下载没有冒充实现。禁止的攻击注入、强杀、权限破坏、运行时替换未执行。没有提前接入第五组、没有专家团、commit/push或发布。

## 同构建重开与最终结论

`--packaged --reopen`通过严格原回执校验，显示Same-build expert reopen verified，readyz=ready；没有重编译或换程序。实际UI恢复口播两轮232s/151s及0.1.0绑定，制作稿仍明确未提交；原JD会话保持0.1.3和原M03答复。搜索“口播”只显示新专家，清空后18专家全部ready，无专家团。App保留打开在完整专家目录。

完成本组既定本地/代码范围；下一组尚未启动。原源文件、用户归档、全部旧版本与历史保留，Git HEAD/分支未变。最终索引为本轮证据根`handoff-status.json`；实际产物在`eval-workspace/{proposals-v1,production-v1}/`，包含真实审阅稿、结构化请求和收据。线上未执行项及未实现下载等范围以上节为准，不以本次完成掩盖。
