# FEAT-164 D3前阻塞修复、依赖恢复与准入复核

2026-10-27。Owner本轮明确要求“深入分析并执行，解决进入D3前的所有阻塞”。本轮在独立来源中完成62号B01/B02最小修复，正常恢复既有workflow，完成安全验证和新canonical daily prepare-only构建。**三项技术阻塞均已解除，当前D3技术前置就绪；没有执行真实日常D3迁移或D4 App启动，没有新增模型HTTP，没有修改Runtime核心/补丁。**

## 1. 授权、契约与来源

本轮批准覆盖62已列的维护准入修复、精确受管前身兼容和既有依赖恢复；原“不启动workflow”是62当轮D2范围，现由本轮解决全部阻塞的明确执行指令扩展。只恢复已登记本地数据集及既有镜像/入口，不新建云资源、不拉取新镜像、不删volume、不强杀。D3实际日常迁移仍未执行，也未生成冒充D3批准的绑定记录。

增量`contract-impact=semantic`，私有权威是Desktop维护准入SQL及Host精确受管文件兼容规则。公共HTTP/RPC/DTO、SQL schema、Runtime协议/核心/补丁不变；公共Contracts生成版本与其pins保持。顺序为Host独立固定→Desktop固定精确Host构建输入→安全来源检查→新canonical制品。不是修改公共wire后补契约，也不把旧dirty生产者当成发布来源。

| 对象 | 当前固定来源 |
|---|---|
| Host | `a3d8767add3855a28c18adbbd51251fae3520ac0`，6文件，精确前身兼容/测试/说明 |
| Desktop | 实现`32191137c883daeee870becc45ff045e8018a49b`，7文件；canonical来源冻结`841f7c71ed3549fe02a70cff608cbbae713d6808`，1派生构建清单 |
| Contracts / Connectors | `c5d138374c102f1a8a11e328a869ec8f91724efd` / `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9`，未改 |
| Runtime / Skills | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a` / `595c927ae101d3d31c234f60565041eee0864680`，未改 |

独立目录`feat164-d3-ready-candidate-20261027`。原工作区、b789旧候选、所有旧制品/回执和D2封存不覆盖。Runtime仍r5 SHA `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`。

## 2. B01：正确区分历史消费和未结清执行

深入核对正常生命周期后确认：占用次数在创建run时增加；可信never-sent取消才退款；正常终态释放reservation但保留消费。当前7条run对应的目标会话均已正常删除，binding保留`target_deleted=1`、conversation为空，原run/recovery仍保留。因此不能要求已经删除的Native view继续存在，也不能仅凭计数大于0拒绝全部历史。

新增私有`settled_schedule_history.sql`为唯一判定源，由Rust维护入口和D2只读reader共用，替换原`occupied_runs>0`拒绝条件。逐grant核对全部run、同scope/plan revision、原版本1 release、无reservation及计数：

- 非退款记录必须有原`native_terminal`证明、非空原reference、已尝试turn、明确terminal outcome且无needs_attention。
- 退款只接受原`never_sent_cancel`、原run reference、never/not_required尝试和cancelled事实。
- 目标仍在时同时核验Native binding/view或持久取消状态；正常删除时只接受已删除标志与保留的完整release事实。
- 所有run必须可对账，非退款已结清数必须等于occupied；缺proof、未知版本、scope/revision不符、数量不符、非终态或reservation仍拒绝。原outbox、model selection、turn和Native view前置保持。

这是只读准入修复，不改grant/run/回执，不清零、不退款、不恢复授权或删除会话。副本实际结果：`occupied_grants=6`保持，新增`unsettled_grant_history=0`，真实Rust `preflight()`返回SQL37；全模型未来/待恢复工作仍0。完成后还复审原retire_before_worker只选择enabled/paused计划，不会复活当前6个deleted计划。

## 3. B02：增加已核实的整文件精确前身

从冻结`v1-current.json`配方与原生产者公开源码中的已核实指令重建第三个前身；仅Kimi base_instructions不同，生成字节精确等于D2封存catalog，SHA `4b0b3fab2e6ca7d8b924248204c745c8e5abbe271e815ba21ecdd8527b1d31af`。原Host binary仍精确匹配原canonical receipt；生产者源码文件/常量/制品/目录摘要都记录在provenance中。

新前身只参与现有显式allow-managed-predecessor的整字节比较；仍要求完整原TOML配对，未知格式/字节或隐式激活拒绝。正常合成Home两次prepare及validate证明旧v1、TOML和trust保持。K31当前v2 catalog/指令配方不变；不合入FEAT-163实现，不在日常库手改配置，不把“接受前身”解释为移植该需求全部行为。

Desktop通过既有`kimi-k31-build-candidate.mjs --freeze-commit`生成新的Host构建清单，再独立提交；没有手改生成内容或旧锁。当前19项检查绑定精确新Host/旧Contracts来源。

## 4. B03：正常恢复既有workflow并证明ready

正常打开原厂Docker Desktop后，观测到3个既有primary保留退出码255，其余依赖与两one-off已停止。未执行普通up去绕过该门禁。使用Infra已有`recovery-plan`/`recover`，恢复ID `efeb4606-28c2-4fef-b327-04c56ad9d7a9`：

1. 固定原8个容器、6个primary、镜像/网络/挂载/credential/编辑器字节，并保存原失败状态。
2. 对四个停止态volume正常copy-out及完整hash清单，之后才正常start原依赖。
3. 用API/Coze自身只读SQL和既有恢复策略核对原operation、执行终态与跨库scope；不重发或标记完成未决业务。
4. 正常启动原API/Coze，确认带凭据ready/编辑器及业务事实保持，然后沿SIGTERM无限grace正常停止。
5. 恢复结束后使用canonical `up`：按已记录当前源码/镜像执行既有幂等migration与正常重开，volume保留；没有强制终止、删除数据集、覆盖binary或手改state。

最终只读检查：6个primary均running/healthy，带K_NA的真实状态与原editor检查通过，`READY`。与恢复前相比，Coze业务事实完全相同，API除两次正常启动各追加1条principal/success审计外相同，原audit前缀保持。原退出255记录、四份volume副本、旧state/credential记录均保留。Infra/API/Coze源码没有修改。

Docker和这6项workflow服务**保持运行**供后续阶段使用。它们不启动Desktop、Kimi或计划执行。两次正常启动按源码写入的审计、canonical轮换的workflow epoch/凭据是本轮允许的生命周期变化；不能把它们描述为全文件字节不变。日常Native/Host/Runtime数据和模型Key则保持D2原字节。

## 5. 验证及真实失败记录

| 项目 | 结果 |
|---|---|
| 结清历史纯值状态矩阵 | 6项通过；覆盖正常消费/退款/删除目标、未决/未知、scope/版本/数量/Native证明不符 |
| 真实Rust只读预检 | 精确1项通过、0 ignored；inspection副本SQL37、原消费次数保持、0迁移/模型请求 |
| 正常旧SQL迁移回归 | SQL29/37×isolated/daily共4项通过；各自含自然held拒绝、review升级、备份/旧事实/重复维护/正常reader；真实日常未参与 |
| Host前身/退役准入 | 1顶层、12子项通过；第三前身正向、未知额外字节拒绝、暂停/身份/旧文件保持；Go vet通过 |
| Native/前端/文档 | fmt、严格Clippy（lib/bins/tests）、Desktop lint/docs通过；6项generation入口测试、4项D2工具回归通过 |
| 六源/生成 | 最终串行19/19通过，前后HEAD/status均相同；原失败和过期来源结果保留 |
| 制品 | canonical prepare-only及同环境prepare-only --reopen通过，119包内文件/1216源码输入hash核对 |
| 数据/依赖 | D2源及sealed再次同锁核验一致；workflow真实ready和业务事实核对通过 |

首次Native精确测试路径遗漏`database`命名空间，实际选择0项，不算PASS；修正后真实1项通过。首次fmt发现本次新增测试的格式，限定本文件格式化后通过。一次只读schema探查误用了不存在的binding列，查询被拒绝，随后按实际schema审计正常删除语义，没有改数据。

来源检查前两次分别遇到新目录缺旧版只读checkout、下游Host input manifest尚未冻结；两项都有具体RCA并修正。第三次19项退出0但与冻结提交尾段重叠，记录旧Desktop HEAD，标`SOURCE_METADATA_STALE`，不计当前资格。完成提交、固定六来源并停止并发修改后，仅再执行一次完整只读检查，19项及前后源一致性通过。详见generation RCA；没有把旧失败、0项测试或来源过期改写为PASS，也没有以此新增真实模型验证。

以上是定向安全验证，不声称全仓CI或新一次全范围App E2E。旧危险fixture、强杀/权限故障/攻击测试未执行；用户排除的搜索质量、外观专项及已接受的never-sent替代不重新开启。

## 6. 新制品、数据有效期与下一步

当前App：`feat164-d3-ready-candidate-20261027/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app`，identity `com.yijie.ai`，仅本地未签名开发构建。

- App SHA `4f7adcadc59db4a6e4cf23e700ebab5858b6ae9d953cd7401780d5778cab0f42`。
- receipt SHA `0e6fe8191ffc027d4f1efedf14f7e8562ee1d876068aafa7386410202a2878a7`。
- Host binary SHA `3be7cb7321362eb90cc0eed929438f27b550c157731a1ab98b3a2ce2ab0d4002`。
- Runtime r5保持；没有创建新的Host/Runtime数据Home，没有启动daily App。

原17,389文件与D2 sealed仍匹配，source manifest SHA `fd007b8bb8857ff1f903c703124328b1a6b65dcb15444a7280db36dc129b3449`；原Native仍SQL37，WAL保持，不手工checkpoint。本轮副本只读预检和既有冷备份因字节一致可绑定到当前结论，不无限期保证未来状态。

当前结论：`D3_PRECONDITIONS_READY`。下一步是依据这套新制品/备份/实际结果执行单独明确的D3一次维护；进入时仍须重验数据freshness、同一实例锁/无句柄并形成真实批准绑定。D3成功也停止，后态核对后再批准D4。长期D5入口及local G5/G6冲突是后续交付项，本轮未实施、也不把它们充作已通过。

原已接受本地S1—S4/final与58替代保留；G4/G5/G6不因本轮prepare-only或ready检查自动晋升。原500份dirty、混合memory、7账本和两份预占保持；累计真实模型HTTP仍13，本轮新增0。仅本地提交、不推送、无branch/tag/release。

当前证据：`evidence/d3-ready-summary.json`、`evidence/d3-ready-source-binding.json`、`evidence/d3-ready-workflow-summary.json`及审计索引；私有完整证据/复制数据保存在`feat164-d3-ready-audit-20261027`和原Infra recovery目录，真实秘密/数据库内容不进Git。

最终元仓audit-claims、strict、S4 G3、lint、53/53测试及7份Shell语法通过；原8仓HEAD/分支/远端、500份dirty与混合memory原内容、7账本、旧b789的119文件/1207输入/receipt保持。结束前workflow只读复核仍为6 running/healthy及READY。记录见d3-ready-governance-checks、preservation与workflow-handoff；无G4/G5/G6自动晋升。
