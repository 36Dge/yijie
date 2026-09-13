# FEAT-153 第4步：受控 local 栈与真实数据库验证

日期：2026-09-12。用户明确授权本步骤。**第4步服务与实库资格完成；第5步 Desktop/iframe 及第6步 fresh D4 尚未执行。** 模型、平台、商家、付费调用均为0；未commit/push/tag、建远端或删除数据。

## 结果与证据

| 范围 | 实际结果 | 证据 |
|---|---|---|
| 固定来源与构建 | 原厂Docker/Compose，精确registry digest/Linux arm64；API、PG runner、Coze按双采样候选构建并记录实际imageID，无浮动发布pin声明 | [最终候选](evidence/step4-final-before-reopen.json)、[初始来源](evidence/step4-build-provenance.json) |
| 独立栈与迁移 | 专用project六服务、四独立命名volume；PG/MySQL显式expand migration，六容器健康及宿主K_NA认证ready | [运行事实](evidence/step4-final-before-reopen.json)、[PG迁移](evidence/step4-api-migrate.txt)、[Coze迁移](evidence/step4-coze-migrate.txt) |
| 最终HTTP W3 | 创建/保存、两个debug、三次内部publish、指定v2再v1执行、结果/节点/真实分页历史；4个成功run、11条API回执，E正常关闭 | [最终HTTP](evidence/step4-http-final.json) |
| MySQL真实事实 | 58表（55原厂+3私有）、精确migration checksum、10条已commit的Coze操作、3内部版本、4成功execution、12节点与scope关联逐项匹配；普通rejected save未伪装成功操作 | [MySQL最终](evidence/step4-mysql-final.json) |
| 最终并发CAS W4 | 两个不同operation、同revision、独立TCP同时正常保存；恰1x200、1x409 revision_conflict；胜者草稿与completed/rejected回执读回一致，E关闭 | [CAS最终](evidence/step4-mysql-cas-final.json) |
| PostgreSQL真实事务 | race集成测试：真实已建principal/resource，8并发Claim仅1新意图、正常审计插入、数据库重新连接读回；storage probe记为unknown，不伪造引擎成功 | [PG最终](evidence/step4-postgres-final.txt)、[runner身份/退出](evidence/step4-final-before-reopen.json) |
| 正常停止与重开 | API→Coze→依赖，SIGTERM无限grace，全部exit0/noOOM，端口释放；同镜像/同四volume、新epoch重开后HTTP、MySQL、W4和原回执均一致 | [停止](evidence/step4-final-normal-stop.json)、[重开拓扑](evidence/step4-reopen-runtime.json)、[HTTP](evidence/step4-normal-reopen-http.txt)、[MySQL](evidence/step4-mysql-reopen.json)、[CAS读回](evidence/step4-normal-reopen-cas.json) |
| 最终环境保护 | 专用栈最终停止、端口释放、volume保留；原六容器状态/StartedAt/FinishedAt保持，8份用户Desktop文件逐字节保持 | [收尾](evidence/step4-final-cleanup.json)、[Desktop保护](evidence/step4-preexisting-desktop-review.json) |

最终主流程 ID `7684526620584968192`，revision `7684526621897785344` 以实际JSON为准；版本为 `v0.0.1`、`v0.0.2`、`v0.0.3`。v2/v3同revision，指定v1仍输出`v1:版本回读`，v2输出`v2:版本回读`。最终资格epoch `4e31a5bf-58b1-480e-aaea-4102ffc158b8`，正常重开为 `d2e2e6d3-d1b7-48f7-8e0f-5a2f2450b1e0`。数据库还保留初轮W1/W2诊断数据，不混入最终W3/W4资格。

## 实现和审计收敛

整体及本轮contract-impact=semantic。API/Coze私有FILE配置由服务部署源定义，Infra按精确owner-only挂载消费。Coze同仓专用InitRuntime继续组装原生workflow repository/service和节点，不拆引擎仓；只初始化实际需要的MySQL、Redis与MinIO，排除完整application.Init带入的知识库/搜索/MQ/模型。MySQL新数据集仅由Coze脚本校验固定上游schema摘要后提取55条CREATE TABLE，不执行原opencoze建库或业务seed，再显式应用三项私有表迁移。PG使用独立服务migration，不修改旧API全局migration。

Docker29实测internal-only API没有建立host端口，尽管容器内probe成功。已正常停止后改为**仅API同时连接专用workflow-edge桥**，发布127.0.0.1:18888；其余五服务和PG测试runner保持internal-only。API edge不等于物理禁止所有出站；应用仅允许固定私有Coze URL，没有通用代理或provider入口。新ready同时验证实际六服务和宿主认证status，不能只读持久phase或容器内健康。

生命周期记录精确container/child PID、epoch和image ID；已知旧镜像容器可以按原记录正常清理，新容器必须匹配当前构建，旧running不能报新candidate ready。端口preflight在移除/轮换前；状态先记录pending epoch，机密原子写后核对两段不同token同epoch。Docker子进程独立session，普通中断只报告并继续正常观察，避免Compose隐式进入有限timeout停止。up不pull、不force-recreate；stop不清卷、无强杀回退。见[Infra审阅](evidence/step4-infra-review.md)与兄弟Infra `docs/workflow-local.md`。

公开镜像下载采用独立匿名客户端配置，不修改用户Docker登录/Keychain。MinIO DockerHub旧入口不可获取，改用厂商Quay同release并锁真实digest。Docker image inspect对组合tag@digest不解析时，按实际imageID读取并同时严格核对RepoTags、RepoDigests与Linux arm64；Compose实际接受该精确引用，未放松pin。Coze Dockerignore误排除pkg/logs与tmpfs YAML逗号问题均在激活前修正。GO_IMAGE必须显式指定，Docker静态检查的InvalidDefaultArgInFrom提示保留，不使用虚构默认镜像。

## 真实发现并修复的回执问题

初轮HTTP子检查通过，但MySQL交叉核对发现W1第二save：API把先前已发布的v1复制到新save receipt，Coze正确只记录新revision；正常成功与reconcile路径因此不一致。这是操作语义缺陷，不是JSON Schema形状违规。未放松SQL断言或覆盖失败证据。

已澄清源OperationReceipt.version：仅发布/固定版本执行引用其操作结果版本，create/save/debug不附资源最近发布版本。canonical生成、三consumer同步/检查、三基线兼容与7源测试通过后，API最终修复只对publish映射Workflow.PublishedVersion，并增加正常回执一致性测试。API17顶层tests及9路由子例、Coze11项正常tests（三包race10项）、Desktop10项、Infra10项通过。旧W1已完成receipt和审计不自动重写；最终使用新的W3/W4重新资格。见[缺陷事实](evidence/step4-receipt-discrepancy.json)、[初轮失败](evidence/step4-mysql-facts.json)、[源与修复检查](evidence/step4-api-receipt-semantic-fix.md)。

## 收尾与保留边界

所有专用容器正常停止，四个数据卷及机密文件保留，18888已释放；旧六容器与既有Desktop文件保持。原厂Docker Desktop正常stop命令exit0、未force。早期默认凭据助手的下载客户端仍有等待进程，正常中断/正常Desktop停止未解除，已停止相关下载活动并记录PID；没有反复信号、强杀、运行时替换或Keychain改写。此残留不代表工作流容器仍运行，不能宣称宿主进程全部清空。详情见收尾JSON。

未执行攻击载荷、危险归档、权限破坏、二进制替换或故障强杀；旧默认危险测试按用户永久规则跳过，安全focused结果不能写全仓PASS。未启动canonical App、实现Vue/React/MessageChannel/CSP、验证dev/packaged编辑器、视觉/键盘/产品错误恢复或Chat共存。因此AC-002—010完整产品状态仍pending，D0保留PASS、D4 NOT RUN。第4步完成不等于工作流产品页面已可用。

最终源码检查附件：[Coze canonical](evidence/step4-final-coze-checks.txt)、[Coze race](evidence/step4-final-coze-race.txt)、[Desktop](evidence/step4-final-desktop-checks.md)、[Infra](evidence/step4-infra-checks.txt)、[治理](evidence/step4-governance-checks.json)、[最终工作区保护](evidence/step4-final-workspace-review.json)。
