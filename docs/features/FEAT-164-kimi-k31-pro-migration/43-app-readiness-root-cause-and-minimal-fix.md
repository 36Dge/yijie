# FEAT-164 S4P：App未就绪根因与最小修复

2026-10-26，Asia/Shanghai。Owner授权审计42、定位App根因、复审最小方案后执行；Runtime核心/补丁修改仍须另行确认。真实模型HTTP新增0，仅本地提交、不推送。

## 修改前证据与根因

以42号同一c76558e App、原记录的无凭据media环境做一次定位运行。核对实际PID与可执行路径，白名单进程环境确认local/demo_fast、Kimi候选/专家/media均开启，但`YIJIE_MARKET_PROVIDER_ONLY=true`。CUA读取Web Inspector；已有`runtime_health`返回ok，`native_auth_status`为signed_in，前端store记录`lastBindFailureStage=context`、`lastErrorCode=chat_host_not_ready`。不是全部IPC不可用或未登录。

完整链路：

1. canonical launcher发现MiniMax凭据文件缺失，自动选`market_provider_only=true`。S4O为了不带真实凭据选择的环境因此变成了连接器管理模式，而不是完整聊天模式。
2. Native `with_scheduled_tasks`会将Host Home改为App隔离数据目录下的`host`。42号检查资格目录的空host-home不足以证明Host从未启动；本报告纠正该推断，42号原始观察保留。
3. Native `market_management_only`分支正常清空模型/Runtime/计划配置，只传连接器管理所需的最小环境。这个边界是刻意的安全设计，不能通过放宽它修验收。
4. Host main只据实际启用的模型v2配置加入`WithChatModelV2Storage`。本轮实际候选`sessions.db`为schema11、base10；provider-only没有该能力，`OpenStore`在任何正常服务监听前返回`ErrModelUnavailable`。
5. Native无法取得子进程连接，映射为`chat_host_not_ready`。UI因此停在本地服务未就绪。

安全证明使用原`sessions.db`的独立普通副本及实际Host代码：只读检查schema11/base10，再以真实provider-only options打开，精确得到`ErrModelUnavailable`，拒绝前后副本校验值相同，原库也相同。仅测试overlay增加诊断case，未改产品源码、未伪造数据库版本、未注入故障。定位运行通过⌘Q正常退出，无模型/工具请求、无强杀。

## 最小方案复审（先于修改）

增量`contract-impact=semantic`，仅部署入口的无效配置提前拒绝；完整FEAT-164仍breaking。有效聊天配置、公共wire、Native权限、Host reader和Runtime制品均保持。

推荐只改Desktop既有`run-local-demo-fast.sh`：当显式FEAT-164聊天候选已落入provider-only且不是`--prepare-only`时，给出明确配置错误并停止，避免打开一个注定不能读取现有模型库的聊天窗口。`--prepare-only`仍允许无凭据完成构建。标准日常/连接器独立管理入口不改，不读取或写入真实凭据，不把fixture自动加入产品配置。

实际验收按已有S4L装配：独立普通fixture凭据文件只含固定合成值，Provider地址绑定现有127.0.0.1 Responses服务；fresh独立构建绑定该环境与原r5来源。fixture没有外部客户端/转发能力，运行账本单独留存。先验证正常启动、历史只读、正常退出/重开，预期模型协议请求0；不点击旧unknown继续，不新增计划授权、不发送真实模型请求。

不采用：让provider-only获得模型reader/writer开关、降级/重建schema11库、修改Runtime、关闭同构建来源校验、给旧App换binary、放宽UI的ready判定。这些都比修正错误装配扩大风险或掩盖失败。

验证：拒绝无效聊天启动且不创建App/Host进程；无凭据prepare-only仍正常；正确本机配置的fresh canonical App实际ready且能只读原历史；正常退出后进程/监听/句柄释放，读取完整副本验证数据库；原unknown/计划/账本保持。现有已签名/旧制品不覆盖；如核心或patch事实需要新增修改，再另报，不沿本方案自动扩张。

实施与最终结果将在本报告后续追加；本段是修改前的方案复审，不代表已经通过。

## 实施与实际验证结果

最小产品修改已本地提交Desktop `b6f0ad7c5181e7ea488c019a1eccd76396eab16e`：既有launcher增加5行，仅限制显式FEAT-164候选的错误启动组合。`--prepare-only`豁免保留；没有新增Key、Provider地址或fixture产品默认值。实际无凭据`--reopen`在App/Host启动前明确exit1，未运行App或打开数据库；这是正常配置准入验证，不是权限/进程/数据故障注入。

Runtime仍为11fd450、binary SHA `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`；Host仍为894671b、binary SHA `1d880cb0f6b990940583abf875fc9b7c551e1135174d675f3caae43ed6f0118c`，均与42号相同。Contracts5b5dad、Connectorscc56cda、Skills595c927保持。未修改Runtime核心/patch、Host实现、兼容reader、授权、SQL、契约生成物或模型请求。

新输出在`feat164-s4p-qualification-20261026`，保留S4O及更早App。标准canonical入口使用显式本机合成凭据文件和127.0.0.1 Responses地址，完整media组合构建/同构建回执通过。19项来源检查第二次通过：首次新checkout缺少嵌套public-api-generator的既有node_modules，核对后仅配置同版本已安装依赖的忽略目录，无依赖/lock/checker改动；首次日志保留。Shell语法与diff检查通过。

### 当前App就绪与正常生命周期：PASS_SCOPED

1. 正确装配首次启动：`/healthz`、`/readyz`、`/v1/status`均200；Runtime为ready、kimi-k3.1-pro、kimi、managed-stdio、固定0.144.6。实际进程链为App→Host→r5 Runtime/worker/adapter，均对应本轮canonical产物。
2. CUA主页面任务树、Kimi K3.1 Pro和请求批准控件正常；只读原真实会话`01a17433-9720-7043-b659-5a6c27a20f4c`，42/50/8及已完成保持。查看原计划仍关闭、Kimi K3.1 Pro/max，未编辑、授权或执行。
3. ⌘Q正常exit0；App/Host/Runtime/worker/adapter、18086监听和数据句柄全部释放。state/logs/goals/memories四库退出后WAL均0；完整副本mode=ro integrity_check均ok，检查未修改源文件。
4. 同一构建正常重开再次ready。只读原草案`01a17315-c3f9-7e93-a6f8-56a7b7876520`仍“提交结果待确认”，发送/模型切换禁用；没有点击继续或刷新请求。再次⌘Q正常exit0，四库WAL再次为0、完整性/资源释放再次通过。
5. 本机fixture通过自身shutdown接口正常结束；整个定位/修复/验收新增真实模型HTTP **0**，本机模型协议HTTP也为 **0**。复用原S4K fixture代码，账本scope字样原样保留；本轮新账本及限定用途独立记录，未修改旧账本或借旧剩余额度。

### 数据审计：区分原记录与正常运行元数据

SQLCipher仅在完整私有副本上只读检查，用标准clang从当前canonical构建的SQLCipher静态库链接审计库；来源/hash/命令保留，不运行来源不明旧helper、不输出密钥或消息正文。71张表中70张逐行hash完全一致，唯一变化是`chat_scheduled_stopped_generations`追加两条正常停止记录；全部旧行不变。旧unknown、草案、计划/授权和真实会话事实保持。

Host初始“所有值逐字相等”检查真实FAIL，原输出未改。随后独立字段审计确认：115个键全部保留，未新增/删除键；14条session只更新`updated_at`，其他字段及所有非session值逐字相同。固定源码`Service.resumeSession→Store.Resume→Store.update`本来就在正常resume时更新该时间戳；没有因失败重写业务记录或改断言伪造同一个测试PASS。字段级结论单独保存。

当前候选允许正常生命周期写入：SQLCipher两条停止记录、Host恢复时间戳及Runtime日志/索引/自然WAL处理。完整before/after副本保留；原rollout等其他文件未变。四库WAL从原非空自然变为0，并非手工checkpoint或截断。不能再把“候选所有文件逐字不变”当作本轮结论；已有工作区改动、旧账本、预占、旧制品及日常数据仍独立核验。

## 剩余边界与后续顺序

42号App未就绪根因及本轮限定修复已收口。r5正常启动/历史只读/两次退出checkpoint子集通过，尚不能把整项G2V/G3或完整final一并置PASS。下一步在当前r5来源上推进S2自然旧K3已加载线程迁移/恢复取消、S3旧计划重新审阅授权及S4/TCONF04余项；活动turn/完整业务/全部final按新来源另验。r5真实G2V未执行，累计5/5授权耗尽，保守14.679001元含14.188544元unknown预占、30元cap不变。

本轮未发生日常切换/迁移、push、tag或发布。核心/补丁若出现新必要范围仍先报告确认；不要把本次错误的provider-only验收装配继续当作r5源码失败，也不要重复旧141项代替剩余场景。

证据：`s4p-pre-implementation-review`、`s4p-store-reader-proof`、`s4p-invalid-launch-preflight`、`s4p-generation-result`、`s4p-corrected-readiness1`、`s4p-corrected-app-observation`、`s4p-reopen-app-observation`、两次normal-exit-audit、`s4p-sqlcipher-final-comparison`、`s4p-host-store-semantic-audit`、`s4p-loopback-ledger`、`s4p-final-review`。原始成功/失败日志和可重现诊断源码的绝对路径/hash见`s4p-audit-index.json`；私有DB/Key副本不提交。

最终治理：claims、strict、manifest、Contract First规则检查、元仓53项测试及7份Shell语法通过。497份原dirty保留；7785份受保护基线中7773份当前逐字一致，另12份是已审计的候选正常运行数据变化，其原始字节完整保留于before副本；无意外改动。两旧预算账本校验值保持，端口18083/18086、候选进程与数据句柄均释放。全程未强杀、未手工checkpoint/删截WAL。
