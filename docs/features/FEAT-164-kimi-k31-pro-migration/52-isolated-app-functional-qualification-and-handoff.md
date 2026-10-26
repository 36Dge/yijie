# FEAT-164 S4Y：新源码隔离App复验、非文本工具修正与交接状态

2026-10-26至27日。Owner要求继续下一步并审计修复阻塞。本轮已完成第51号新源码的独立隔离App构建、图片/媒体工具/MiniMax本机复验、正常退出与来源绑定；修复已知测试Clippy问题和旧计量器只支持文字资格的限制。**真实非文本验证尚未发送：窗口出现用户操作后正在等待交接**。整体仍IN_PROGRESS；真实日常库未启动、连接、解密或迁移，旧daily候选保持原样。

## 修复及固定来源

1. Desktop `54e961842cb7abe7234e3d643142e99f266ec833`只将native_conversation_storage.rs中已有cfg(test)模块原样移到文件末尾，修复items_after_test_module。生产代码文本与测试断言均逐字保持，增量contract-impact=none，无权限/schema/Runtime改动。fmt、lib/bins/tests Clippy `-D warnings`及原v3/v4读取测试通过；第51号记录的全测试Clippy基线失败已在本候选修复，原失败证据保留。
2. 验收工具 `a35e619e297c793ebb6cfb08730ab558f2924356`基于既有92cbe3d独立工作树，只改meter并增测试/说明。旧schema1—4不变；新schema5保留图片、函数回灌和原生搜索/include，最多4次新增HTTP、输出8192、先存预占再出站、禁止并发花费、失败/在途恢复/未结费用停止。38项独立测试和docs构建通过；初次47计数含导入测试类的重复执行，修正测试发现后38唯一用例PASS，不虚增计数。
3. 修正文档矩阵中“真实供应商未授权”“r5 teardown未通过”和待实施日常部署方案的过期表述，依据49—51及当前用户指令；不晋升任何整项Gate。

新的App位于`feat164-s4y-qualification-20261026/yijie-desktop`，固定`com.yijie.ai.feat164-qualification-v1`，119包内文件；App SHA `879568b9ff61530806d63aaa6068053e98f1d68b1fc6506a48adecc4035c6b8a`，回执SHA `2fa120fdf031713b747600f44a4303117a81b21f571c732ac734c8f1c737a170`。Host8cd6bcc、Contracts ca06d099、Runtime11fd450/r5、Connectors cc56cdaa、Skills595c927不变；新Desktop是在ec1ab63上仅移动测试模块，生产文字一致证明见s4y-clippy-minimal-repair。S4X日常App edf9a138及其回执未动。

工具修改只作用于人工选择的验收relay，不进入产品App，不修改Runtime核心或补丁。Provider请求仍到api.moonshot.cn/v1/responses，SSE原样返回；仅保存状态/usage/工具与sources计数/摘要，不保存正文、参数明文、密钥。第三方功能字段以[Kimi Responses文档](https://platform.kimi.com/docs/api/responses)及既有固定投影为依据。整项FEAT164 breaking不变；本轮产品增量none，验收账本版本升级为私有工具边界，不是公共schema修改。

## 实际离线结果

| 项目 | 结果 |
|---|---|
| 新源码来源/生成 | 修正环境后19项PASS；首次public-api生成器缺独立node_modules，未修改product/lock；补齐两个既有固定依赖目录后单次通过 |
| canonical prepare-only | exit0，未启动daily App；独立资格identity，media完整组合 |
| 同构建正常启动 | canonical --reopen的源码/环境/制品回执校验PASS；App ready，Kimi K3.1 Pro默认可选，旧K3未列为可选模型 |
| 图片＋媒体工具 | 新任务01a178eb-0a8d-7bb1-8e7c-b80a626ff645 completed；1张合成PNG经3次K31/max本机请求，两个publish_artifact及回灌，HTML/SVG ready且逐字相符，HTML实际预览通过 |
| MiniMax共存 | 新任务01a178ec-0a19-7673-9c9a-11332f1c2dcb completed；1次MiniMax/high本机请求 |
| 正常退出 | ⌘Q exit0；无项目子进程/句柄，4 Runtime库WAL0、完整副本只读integrity ok |
| 数据保留 | 71表全部旧行hash保持，只有新任务/成果/项目及正常停止代际追加；不删回执/历史/授权 |
| 再次同构建打开 | 回执PASS，当前App已打开，历史条目仍列出；因用户操作尚未完成历史详情读取，不能称整段重开验收完成 |

总计4次合成模型协议请求，外部HTTP0，fixture正常shutdown/exit0。无故障/攻击注入、权限破坏、强杀、替身binary、手工checkpoint或WAL操作。输入中文曾未完整落入输入框，发送前已用paste核验完整文本；没有发送错误内容。UI只检查业务功能，没有恢复已移除的亮暗、键盘/焦点、最小窗口专项。

## 真实验证准备与费用边界

复用Owner已经明确的必要功能调用及搜索/图片授权；**4次是本轮自行收紧的执行上限，不冒称Owner另行指定了4次**。计划为图片1次、普通本机函数＋回灌约2次、最后原生搜索；标题/辅助同计HTTP，超过上限拒绝。未给真实日常库增加授权。

新`g2v-real-budget-ledger-functional.json`包含原schema4完整JSON与前6行，当前App/r5 digest、30元上限、原14.188544元unknown预占原样保留。旧三个账本逐字保持，累计仍6次，新增0。保留历史估算14.795856元，不冒称精确账单，也不以精确价格阻止功能验证。

每次仍用原1M＋8192历史估算预占并核验总额；已返回usage的普通成功按原估算结算。如真实发生原生搜索，完整新预占保留且本轮停止，不把独立搜索费用误算为纯文本费用；response.completed的执行成功与费用未结清分开记录。该路径已用正常合成元数据验证，但实际搜索尚未执行。

## 当前交接及后续

工具检测到用户正在操作新隔离App；刷新状态确认模型菜单由用户打开，已通过异步问题请求交回窗口，未继续点击/发送。等待期间meter已正常control/stop 204、进程exit0，当前schema5 stopped_normally且未消耗新槽，仍余4；fixture也已停止。**App有意保留打开供用户查看，不声称第二次已退出或本轮全部teardown结束。**

续办读取`feat164-s4y-audit-20261026/handoff.json`。用户回复“可以继续操作”后，先核对当前App/path/回执和账本仍6行，再启动同一工具、同一ledger/控制文件；不重建账本、不补额、不重复询问图片/搜索/费用授权。先读本机任务历史并确认重开零请求，再做实际图片、函数回灌、搜索；失败即停并审计，不按旧文本meter移除搜索或改称非文本PASS。App源和产品功能不需为此再改。

6554份活动隔离库之外的保护文件（含真实日常数据原始文件hash、日常候选包及旧账本）保持；497份原dirty保持，混合memory的原内容另行精确保护。原数据只做原始文件hash核对，没有日常数据库连接。仅本地提交，无push/tag/release。所有私有备份/Runtime home/失败日志继续保留，不提交数据库和Key。

S4/TCONF04和完整core/业务状态final仍未完成，旧G2V/前三切片结论仍按原App来源解释；本轮只登记已实测离线子集。日常cutover仍需独立具体数据执行清单及对应批准。下一步阻塞是窗口交接，不是模型预算或精确价格。
