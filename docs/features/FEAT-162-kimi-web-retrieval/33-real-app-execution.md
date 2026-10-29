# FEAT-162 真实App执行记录

> 当前状态（2026-10-29）：第八代E1仍失败，累计3次模型HTTP、0REST、3元未知用量估算；Owner已暂停构建与收费验收，方案A清理完成。现已另行授权全仓Git提交/推送；完整当前状态见[34号](34-paused-state-and-cleanup.md)。下文授权与执行进度按历史时点理解。

2026-10-29，进行中。Owner当前授权为20元软停止阈值及仅本地FEAT-162提交、不推送；证据见evidence/current-authorization-20261029.json。真实E1—E7和D4尚未通过。

## 来源闭合与构建

Contracts d191ad6ed08f0e8cc89dfea1346b5ecdf010e776、Connectors ab1f8328ff50dab256b23f51d49157278421fd35、Host 34a8fdd24319ed8f289336c30d48ed27afbb7691已仅本地提交。Desktop按Contract First同步消费引用、worker目录和Host冻结来源。第一代20261029-01正规worker构建成功，随后因Native源锁仍引用旧generate.mjs失败，未启动App。已用Contracts canonical Native/MCP同步器更新来源，业务输出不变；第二代20261029-02因canonical环境选到Go1.26.4失败；本机已有官方Go1.26.5，选择其bin到构建PATH，未替换二进制。第三代因权限契约同样引用旧generate.mjs失败；正规同步后业务输出不变。使用完整实际环境复核来源和资源全部通过，第四代20261029-04构建成功。旧代产物、失败日志与原App保留。

## Workflow阻塞恢复

Docker未运行，原Workflow容器保留2026-10-28退出记录。使用原Docker正常启动及仓库既有recovery-plan/recover，恢复ID 2f0d28b2-4d4e-406b-81c1-d6b94b7a06ee。先完整复制四个停止态数据卷，校验原镜像/挂载/凭据/数据关系，启动原容器后核对存储，再正常SIGTERM无限grace停止，exit0。随后canonical workflow-local.py up成功，已有migration入口正常完成，六服务healthy及带凭据readiness通过；未增加或更改schema源、镜像或删除数据卷。既有异常记录保存在恢复快照，未伪装历史正常。

## 日常数据前态

完整冷备份17,401文件、523,139,568字节，source/sealed/inspection一致，原Native/Host/Runtime Home保留。Host11只读检查通过，8会话idle，无active turn。Native只读检查PASS：SQL41、外键/完整性/历史解码通过、无待发送消息或可派发计划，6份旧占用保持。启动前重新验证全部原Home与sealed副本未变，8组会话/任务/Runtime映射一致。当前已有FEAT-165 SQL42前向读取屏障仅SELECT 1，正常新App可能记录41→42；未新增迁移源或改写旧历史，不允许SQL41-only旧App直接回开42库。

## 当前边界

新付费调用0；v3软阈值6测试、v2 8、legacy19、worker27、前端44及来源检查通过。安全禁止项未执行；未强杀、篡改受保护二进制、破坏权限或攻击注入。最终验收、费用和D4状态待实际结果补齐。

## 第四代资格

正规构建6分43秒、未签名的本地开发App。回执a13f3d667d4349892758721add1299f2e09cc58f0bd9395bdf1a4334c2a5655d，App二进制0d1f07a627913ccc9f9e07558895b323b5df392b6c6fc05c89f5a194c90575d3。1,271项来源输入/119项bundle文件及worker逐项匹配，六仓committed+clean。已建立当前授权及真实零派发预检绑定，正在canonical daily:verify执行Kimi暂停的首次启动。此处部署D4前置不等于FEAT-162产品D4通过。

## 第四代实机失败与已修复原因

真实App显示“本地组件状态不一致”，一次正常重新同步仍失败。Host/Runtime ready不等于Native就绪。数据库保护在打开原库之前拒绝了被自动开启的FEAT-165文件候选；这也证明前述41→42只是未执行风险，实际原库始终SQL41。修复文件候选判定以排除daily，保留原数据库保护、daily媒体/v9以及非daily候选行为，不启用FEAT-165日常迁移。普通临时SQL41开库/重开回归先复现OrchestrationUnavailable，修复后PASS；fmt、Clippy和docs构建PASS。Desktop本地提交5b8530219d74f95b9b0d4d084897533944b50a10；第五代正在正规构建。

第四代通过CUA Cmd-Q正常退出，exit0、cleanup complete，所有自有子进程结束。完整后态冷备份17,403文件、523,332,080字节；Native全部行、Host全部值、Runtime业务行/旧rollout和密钥未变，Runtime只新增376条日志。保留正常生成的零字节WAL和32KiB SHM，未删除；下一次正常成功开关必须验证checkpoint。此代UI/产品D4为FAIL，新收费0，不能用于最终通过。

## 第五/六代真实入口与首次收费

第五代实际首页/原历史、正常退出、SQL41及旧数据保护通过；第六代再次实际正常重开历史与退出，WAL/SHM活跃字节0。第六代回执33704c665c05d2c1e220b49f412c4f538c3ccfb6586e99fc93ee34bfb39f0828。实际UI合成正控保留完整tools（含三Kimi工具及原生搜索），拒绝明确显示“本次外部请求未发送”；worker call_admission=rejected且web_http_send=0，新会话合成回复成功。合成拒绝后的续传被fixture parser拒绝(JSONDecodeError)，该合成回合显示失败不能归因于真实供应商；只将它用作已拒绝零REST证据。两个实际新会话的cache identity都绑定各自thread，修复后的稳定产品摘要相同；9项最新v3、8项v2、19项legacy检查通过。

E1已真实发送1次Kimi模型HTTP，HTTP200但stream不完整，usage未知，无工具审批/REST。保留1元估算（不是实际账单），REST0.105元仍只是预留；native是否已发生无法从旧观察证据确定。首次halt原因被settle/normal_stop覆盖，Runtime仅有通用失败；不得把未知原因断言为供应商故障/原生路由。该批次已关闭，E1 FAIL、E2—E7 NOT RUN，D4未通过。新观察诊断已修复并本地提交，正在第七代构建；新批次须携带1请求/1元未知估算，旧42.710457元另行保持。详见evidence/real-app-first-paid-20261029.json。

## 第七代：真实原生搜索路由失败与修复

来源回执882c94af3c08d127017c9d2a2bed69593bbb14c16047d093b315bbf28bfe67ef。新代真实App正常初始化、原历史读取和Cmd-Q退出通过；只读冷备Native SQL41、14个Host会话均idle、无可调度工作、Native/Host/Runtime完整性正常。实际E1的第二个本轮模型请求返回HTTP200，但SSE给出web_search_call，观察器保留首次停止原因native_search_already_executed并停止；未出现Kimi MCP审批，无REST。E1 FAIL，E2—E7 NOT RUN。

本轮累计2次真实模型HTTP、2元未知usage估算，非实际扣费；原生搜索观察到1个项不代表已知计费次数。历史42.710457元预占继续独立。第六代原因仍unknown。脱敏事实见evidence/real-app-second-paid-20261029.json。

根因位于Host通用运行指令：无条件要求可用时使用原生搜索，与当前选中的Kimi描述冲突。按31号先审决策修复平台选集优先级，保留原生工具和无适用连接器时的默认路径。固定r5 Runtime 6次loopback正常请求验证了实际指令、原生工具保留、专家隔离与普通续接；3个专家纯逻辑测试通过，外部HTTP0。Host本地commit 8d2f17e2ddf54f45d73636d6a42612c913fc884e；继续构建第八代并重验原冻结输入，不把此修复视为收费验收已通过。
