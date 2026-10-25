# FEAT-164 S4 生成入口与计划后续验证

本轮用户要求“执行后续方案”，继续33及s4g RCA明确的离线范围，授权仅本地提交、不推送；真实模型HTTP新增0，旧30元预算、2/2已用HTTP、14.188544元预占与14.328134元累计上界保留。已有原工作区496项改动/旧证据/数据/App另行记录基线。

## 实施前方案与RCA续办

contract-impact=none：本轮先增加只读生成检查编排，不变更wire、schema、持久化或重放、Runtime、权限及产品默认入口；整体breaking保持。通用旧入口/锁原样保留，FEAT164新增显式alias逐项保留legacy reader并补齐v2 writer检查，仅catalog provenance使用既有FEAT164精确锁。Default失败仍是历史事实，不被新入口PASS替代。具体源边界和对应检查见Desktop `docs/feat164-generation-check.md`。

RCA扩大审计发现：Node从符号链接执行generator时会按真实脚本路径解析sibling consumer，可能落到旧资格树。新S4h的Contracts/Host/Connectors均以精确HEAD建立同父目录真实checkout；Runtime/Skills只读producer复用已核实的清洁来源。新预检在任何leaf前检查完整来源和真实父目录，失败不fetch/覆盖源。上轮相关生成物没有变化，但本轮不继承错误路径假设。

当前用户继续指令按既有后续方案授权一次修正后的入口验证：先6项普通结构化配置/执行计划测试与lint，再本地固定源；仅执行一次全19项read-only入口，失败即停，不运行第4次旧通用命令。任何失败按真实新事实重新审计，不机械重跑、不扩大调用/权限。记录时间为本轮授权被记录时刻，并非虚构用户消息的精确发送时间。

成功后推进S3原生5项安全历史fixture/领域/重开复验，再走canonical普通App计划模型重新选择、保存paused与独立单次授权。当前产品数据的自然计划是K3.1，不伪造旧K3记录；旧K3迁移仅按Native结构化验证归档，完整旧K3 App迁移仍另列未验。所有模型请求仅安全本机fixture、0外部请求。

## 本轮实际结果

Desktop仅本地提交`1b5adcfc1b6b3195df5b3495de3f1c4b22599d51`，新增检查入口、6项结构化测试、package显式alias及说明共4文件。产品源/默认命令/所有原锁保持。6项测试与ESLint通过，canonical ordinary构建/同收据重开及文档build通过，未引入依赖或网络安装。

新入口第一次在预检停止，原因是本轮Contracts资格目录将node_modules做成symlink，gitignore的目录规则不匹配；0个leaf执行。准备问题由本轮负责，已保留原日志及s4h-preflight-rca。仅将新checkout依赖整理成正常ignored目录，未改gitignore/lock或产品验证断言。Owner随后明确回复“批准修正后单次检查”，又补充允许2—3次用于分析。修正后第1次完整19项全部PASS，剩余2次未用；不会为消耗授权重复验证。旧通用三次FAIL和preflight FAIL保留，失败台账通过真实RCA cycle追加resolved，不改历史或把旧默认命令写成绿色。

S3当前源5项全部通过，沿原测试逐项精确命中1/0失败/0忽略；结构化旧历史仅存在正常临时SQLCipher，未注入攻击、传输/进程故障或改候选数据库。18项计划相关前端回归通过（实际3个测试文件），不冒称全suite。

App实际步骤：现有合成计划原Kimi、关闭 → 只在关联聊天显式改MiniMax → 按旧计划“立即执行”被拒绝，模型请求0 → 编辑显示MiniMax与“旧授权不会沿用”，取消并放弃后计划仍Kimi → 再次审阅保存为MiniMax且关闭 → 新的明确“立即执行”成功，真实Native/Host/Runtime只向本机fixture请求1次MiniMax-M3/high → 关联聊天改回Kimi，重新审阅保存计划，计划保持关闭 → 正常⌘Q退出、同收据重开，原2条执行历史均保持 → 正常退出。

只读事前/事后副本证明：原grant和run记录逐字段相同；仅增加1个max_runs=1/occupied_runs=1的独立grant及对应completed/manual运行，snapshot锁定MiniMax；最终计划除revision从1增至3外全部字段恢复（含名称/内容/规则/模型），关联聊天ready/Kimi，authorization_ref/expires为空。paused计划仍保留原缓存next_at，这是原有存储语义而非自动执行许可；最初审计误以为paused要求next_at=NULL，已纠正审计假设，没有改数据库满足断言。原failed/attempted草案元数据和completed草案6条原生事实全部保持。见s4h-data-audit.json。

界面限制实录：模型与计划不一致时当前通用提示为“关联聊天已不可用，请重新选择”；能阻止执行，但未准确区分模型不一致与聊天不可用。模型切换后聊天存在既有未分类conversation_warning提示，本轮未隐藏或把合成答案当成模型业务质量。当前原计划本来是K3.1，不能把上述操作写成旧K3真实App迁移；旧K3退役目前仅Native历史fixture与组件资格。

本机fixture复用已审阅的s4f脚本，新账本`s4h-app-loopback-ledger.json`记录1次PLAN_RUN、MiniMax/high、拒绝0、external0、stopped_normally；新脚本生成检查和Native领域测试不运行模型。两次App退出0、18083/18086释放，无强杀、权限破坏、程序替换或真实平台/模型调用。旧30元/2次请求已用、14.188544元unknown预占及14.328134元累计上界不变。

## 后续边界

本轮完成生成入口RCA续办与当前计划重新审阅/独立授权的App子集；完整FEAT164仍在进行。下一优先是当前r4专家/媒体同源App组合与安全本机验证，以及完整恢复/取消UI。旧K3 App迁移、跨平台、完整TCONF、当前真实G2V、G3/freshness和final仍不通过；没有新的真实HTTP许可。继续保留当前失败草案，不重置、不据404重发；只本地提交，不推送或发布。

## 最终治理与保留核验

claims/strict、元仓lint、53/53治理测试及7个shell语法检查通过；G3实际继续BLOCKED，未提高G2V/final资格。原496项改动、1045份旧证据、154资源、7日常DB文件、245旧App文件及5524候选事前副本保持；当前source/bundle/Host/Runtime/Manifest摘要与canonical收据一致，Host/Runtime产物与上一批相同。所有原branch/remote保持。见[s4h-verdict](evidence/s4h-verdict.json)、[保留审计](evidence/s4h-preservation-audit.json)、[治理结果](evidence/s4h-governance-results.json)。元仓仅本地提交，以包含本报告的Git记录为准；没有push、tag、PR或发布。原始日志末尾空白和patch上下文保留，不为diff白名单修饰原始证据。
