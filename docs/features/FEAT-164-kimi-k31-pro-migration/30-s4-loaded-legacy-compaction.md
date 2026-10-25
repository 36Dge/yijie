# FEAT-164 S4 旧模型已加载状态与自动压缩安全离线验证

2026-10-25，Owner明确要求先审计，再优先补旧K3已加载线程、子代理和自动压缩。新增真实模型HTTP为0，仅本地提交、不推送；原工作区、全部旧证据/账本及预占保留。总需求contract-impact=breaking不变；本轮先仅新增普通离线验证，contract-impact=none：不改变产品wire、执行规则、数据库或Runtime产物。若发现产品缺陷，另按事实判定影响，不静默扩张核心变更。

## 起点与边界

产品来源仍为Desktopa0a4743、Hostcac2d4d、Contractseddc64f、Runtime074417e5 r2；29记录的App子集成立，S4完整TCONF/G2V/G3/final未完成。原496工作区改动、789既有证据文件、154资源、119当前App bundle项及7日常DB已重新记录摘要；本轮不启动App、不动日常库。真实30元账本2/2 HTTP耗尽、14.188544元未知预占和14.328134元保守累计上界保留。

固定r2的0007在Responses request构造前拒绝kimi-k3，覆盖普通及辅助入口。前轮S4b覆盖新子代理和显式compact，不能替代本轮。Runtime previous-model压缩在comp_hash变化或缩小窗口时可选旧模型；custom Kimi provider不具备OpenAI/Codex-auth专用fallback。当前真实Kimi catalog无comp_hash且新旧窗口同为1048576；必须区分当前有效配置与普通兼容分支样本，不把未启用配置写成产品默认。

## 验证方案

1. 用保留的canonical旧web-sources Runtime及全进程loopback配置，经正常协议产生旧K3父/子完成历史并确认二者仍loaded；正常Shutdown收敛全部受管工作后定义cutover，再启动r2，以Host显式新profile恢复父/子，核对历史、实际新出站与旧身份拒绝。只新建临时Runtime Home，不启动旧reader读取任何新产品库。
2. 单独验证r2原生协议边界的旧K3已加载线程及显式旧模型子代理：普通合法历史身份输入应被当前请求guard拒绝、零旧HTTP；对已加载子代理的正常后续输入仍不复活旧模型。原生层资格与Host产品准入分别记录，不冒称应用允许该入口。
3. 经公开配置设置有界自动压缩阈值，使用普通长文本和明确合成usage触发自动compact，再核对原生contextCompaction事实、请求模型与正常终态。不是调用thread/compact/start代替自动压缩；不改rollout/usage数据库，不伪装供应商token用量。previous_model分支按当前有效配置和正常兼容样本分别验证，失败保持真实失败/拒绝语义。

实现位于新的Host detached资格树，保留S4c原canonical来源。所有输入仅合成文字、原生子代理与本机服务；两provider在进程级和thread级都固定loopback，启动后读取有效配置证明，不继承调用者凭据。旧Runtime只作真实历史producer，原binary/manifest不修改；新Runtime及Host仍执行精确来源验证。旧producer的本机请求单列为cutover之前，不能混进切换后零旧身份结论。

停止条件：实际模型路径不在loopback、来源不匹配、出现旧slug切换后出站、请求数超预定范围、原生终态不闭合或正常清理失败，立即停止依赖步骤并保留证据；不强杀、不改权限、不替换程序、不注入攻击或故障。不用全量历史危险suite；按精确测试selector验证非零命中与零skip。

## 实际结果与判定

结论：本轮安全离线验证已完成可执行范围，发现真实产品终态缺陷，S4仍blocked。不能将零旧模型HTTP或独立子集PASS换算成子代理正确失败、完整TCONF-164-04或G3通过。Host本地验证提交为`df06a3cda72dee14f5db1d7b46e83fd196d2b070`，仅新增Go测试、显式opt-in离线driver及验证说明三个文件，产品源码diff为0。保留S4c Host product pin `cac2d4d7e1df02868a370e204959e1842c3362c3`，未据测试提交重建App或覆盖原资格树。

| 场景 | 实际证据 | 判定与界限 |
| --- | --- | --- |
| 旧K3父子已加载后切换 | 旧canonical父3/子1完成并均在loaded/list；正常整进程Shutdown后，同Home r2显式新profile恢复原ID，父1/子1均K3.1/max，历史读取零请求 | PASS，6次本机HTTP；不是运行中热切模型 |
| 旧身份原生loaded父及loaded子后续输入 | 3条真实退役guard错误；仅当前父线程6次HTTP，旧身份0 | 出站保护PASS；首次spawn及同子send_input后的wait_agent均completed:null，child thread/read两轮均completed且仅userMessage，终态FAIL |
| 当前模型自动压缩 | 普通长文本达到公开阈值，第二次用户输入自动先compact再回答，原生contextCompaction可见 | PASS，3次本机HTTP；不是显式compact API |
| 正常旧历史切新后自动压缩 | 旧模型1轮正常完成并loaded/停机；r2当前真实catalog同窗口/无comp_hash，自动新模型compact1及answer1 | PASS，共3次本机HTTP；切换后0旧身份 |
| previous_model comp_hash变化/窗口缩小 | 两个普通兼容catalog样本分别触发原生previous_model分支；旧seed各1，r2 guard失败且零后续HTTP，旧回答仍可读 | PASS仅指安全拒绝；不是未来该配置的迁移可用性PASS |

固定来源资格运行见[evidence/s4d-qualified-independent/result.json](evidence/s4d-qualified-independent/result.json)：Go1.26.5，`-race`，6个Go PASS（含两个子用例及容器），0FAIL/0SKIP，5份fixture ledger、14次loopback。它显式排除已知失败的loaded-child用例，结果名`PASS_FOR_INDEPENDENT_SUBSET`、`full_tconf_pass=false`，不能隐藏失败。该失败测试保留原断言；诊断后不再重试。最终代码增加显式opt-in，避免一般Go测试无意启动该集成验证。

全轮有有效fixture ledger的6份日志累计71次本机合成HTTP，其中30次旧producer请求均在各自cutoff之前，41次当前模型；真实模型新增0。详见[s4d-verdict.json](evidence/s4d-verdict.json)。合成usage按普通文本字节派生，只用于原生阈值控制，不冒称厂商计量、压缩质量、实际性能或成本。旧30元账本、2/2已用HTTP、14.188544元未知预占与14.328134元累计上界原样保留；不得由剩余费用产生新HTTP授权。

## 失败时间线与根因审计

- `s4d-graph-initial`、`graph-01`在测试前失败：系统Go1.26.4低于go.mod要求；经go shim选工具链时离线sumdb校验不适用。最终使用本机已安装官方1.26.5绝对路径，不联网下载。`s4d-vet-preflight`是cwd未在模块；修正cwd后vet通过。上述日志均保留，不计作模型/产品失败。
- `s4d-cutover-01`：child场景尚未具备普通旧catalog前置，子代理未实际建立；previous_model观察器错误地从重放历史找瞬时错误。仅补合法兼容catalog和真实live error观察，不改产品或放宽断言。这是harness前置/观察失败，不能伪记为同一原生终态缺陷的第1次。
- `s4d-cutover-02`（19:26:05起）：前置成立，实际child失败状态被completed覆盖；其它独立分支通过。
- `s4d-child-diagnostic`（19:27:21起）：仅增加真实wait/error/child history观测，确认相同产品缺陷，未改产品或正确终态标准。之后停止该场景，不进行第4次非绿色child验收，也不将失败重新命名为PASS。机器台账同fingerprint实际产品失败次数为2、状态armed；手工采用更保守的停止策略。根因审计不伪造Owner批准或resolved RCA cycle。

**Fact**：当前固定Runtime的`core/src/agent/status.rs:6`对单事件投影，Error得到Errored，后续TurnComplete得到Completed(last_agent_message)。`core/src/session/mod.rs:1978`直接send_replace覆盖前状态；`tools/handlers/multi_agents/wait.rs`消费该状态。这解释实际两次wait_agent的completed:null，不能靠Host文案修正原生调用方所见事实。

**Fact**：`rollout/src/policy.rs:99`持久化TurnComplete，`:118`把Error列为transient；`app-server-protocol/src/protocol/thread_history.rs:1176`只有收到Error才标failed，`:1240`在重放无错误的结束事件时归为completed。因此原生thread/read重放只见userMessage和完成状态，与live guard拒绝冲突。app-server的live last_error分支能够发出failed并不修复上述两处。未更改原rollout或用户库；未重写旧历史。

**Fact**：退役guard在请求构造前挡住kimi-k3；既有current provider loopback配置与逐请求identity断言均成立。previous_model在普通兼容样本下失败关闭；current真实catalog同1048576窗口/无comp_hash，迁移后自动压缩正控通过。

**Assumption**：后续修复可以限定为原生退役错误的终态传播，不改变工具批准、重试、沙箱和正常取消；仍须用源审计和安全验证证实，不能提前选none/additive。

**Unknown**：最小持久终态表示及其旧reader兼容性、error是否影响同一turn、后续正常TurnStarted重置、瞬时可恢复错误是否应影响终态，须在补丁设计中逐项固定。旧缺失错误的历史不能仅凭空答案反推failed，必须保留证据不足。

**Conflict**：真实执行被拒绝，原生等待/历史却宣称完成；这是S4验收缺陷。安全出站结论不能覆盖这一冲突。

## 后续方案与批准边界

方案A（推荐）：对固定Runtime做最小、可重放的原生修复，同时闭合子代理等待终态与新生成历史的持久失败事实。先审计已有终态/错误权威结构，避免持久化原始错误正文，避免按空答案猜失败，不重写既有历史。明确同一turn的不可覆盖失败、下一正常turn重置、取消保持原语义；对旧reader不支持新持久事实的情况拒绝激活或提供经证明的兼容reader。若任何受支持reader不能正确解释，按breaking处理。方案范围包含core/rollout/协议权威及补丁，不能在Host反向发明状态。

方案B：保持当前构建禁升，先继续互不依赖的计划/恢复取消App验证；它能减少其它缺口，但不能修复本项或解除S4阻塞。方案C（不采纳）：只在Host/UI将completed:null改成failed，会伪造执行事实且遗漏Runtime内父子工具消费者。

推荐执行顺序：

1. Owner明确确认方案A的Runtime核心/补丁与潜在兼容边界后，先做源设计和最高风险contract-impact分类，再写canonical patch，不直接改上游子树。
2. 新候选通过固定上游重放、标准构建、canonical schema比较及安全focused测试；原r2/legacy/App和已审计hash继续保留。
3. Runtime权威先行，再Contracts不可变兼容投影、Host消费验证、Desktop精确pin和同源构建；需要改变持久格式时先证明兼容reader，不让旧reader写新库。
4. Owner批准的修复后资格运行覆盖：guard零旧HTTP + 原生wait failed/errored + 新历史重开仍failed + 正常新模型子代理成功 + 同一子线程正常下一轮 + 原取消/拒绝语义；先获得新候选后仅执行受限验证，失败按指纹停止。不使用强杀、攻击输入、权限故障、替换程序或原始用户数据。
5. 再补计划/显式恢复取消完整App、其它平台、当前组合G2V/freshness及最终三类E2E。当前真实HTTP额度为0；需要真实模型时须另获明确授权，旧预算余额不等于授权。

Runtime仓[AGENTS.md](../../../../yijie-codex/AGENTS.md)明确：“是否修改 Runtime 核心、协议、沙箱、权限、认证、更新或遥测行为”及“是否新增补丁、依赖、feature flag、构建目标或发布产物”属于必须先确认的决策。因此本轮已完成可独立的验证和RCA，不擅自新增Runtime补丁、产物或consumer repin。此限制来自仓库规范，不是将安全离线测试误认为付费或破坏性操作。

## 安全、保护与复核

新建普通临时Home、合成历史和loopback服务；两provider有效配置均读取校验，凭据为固定dummy，调用者密钥不继承。旧binary只正常产生旧历史，r2通过真实VerifyArtifact准入；未绕过artifact policy。每次Manager Shutdown及server Shutdown走正常流程，失败会保留现场，不调用强杀。初始兼容catalog通过公开配置载入新建普通文件，不改受管产品catalog或二进制。

本轮未执行：真实模型/搜索/图片供应商调用，故障注入或攻击测试，完整历史危险suite，日常DB迁移，App/UI或系统设置变更，跨平台及最终G2V/G3。原因分别为0授权、安全硬条款或本轮范围/已知缺陷；影响是完整FEAT-164不能验收或发布。

最终治理、静态检查与保护证据见`s4d-governance-results.json`、`s4d-static-review.json`、`s4d-preservation-audit.json`和`s4d-meta-isolation.json`；只有实际结果生成后才能据此声明通过。元仓仅新增/更新FEAT-164治理记录和长期记忆的本需求段落，提交完整SHA由Git记录定位，不预填自引用。不push/tag/branch/PR/release，不混入FEAT-162/163及其它原改动。

治理首轮claims与元仓测试因新证据段落缺canonical HTML evidence marker失败（53中51通过/2失败），未涉及产品执行；补齐四个唯一marker后复验。首轮日志保留为`s4d-claims-initial.log`和`s4d-meta-test-initial.log`，不抹除失败。

最终实测：strict、claims、元仓lint与53/53测试、7个shell语法检查通过；S4 G3按预期拒绝放行（完整前置、纵向、freshness与TCONF缺口仍在），不把该退出1记为PASS。保护审计证明496原工作区文件、789旧证据、154资源、7日常DB、119当前App文件和6个原资格树保持；固定两套Runtime binary/manifest摘要相同，无所属Runtime/App残留进程。新Host资格树df06a3c干净。

失败证据产生于最终测试提交前的诊断工作树，日志和时间原样保留；之后只加显式opt-in与独立driver等验证保护，没有再次运行已知失败的child场景。最终df06a3c只执行独立子集资格，不能把早先诊断运行伪称为该提交上的新一次完整验证。

提交审计：44文件仅属FEAT-164（含长期记忆的本需求段落）；无旧真实账本或锁文件入暂存区。非日志diff whitespace检查通过；首轮元仓失败原始日志3处尾随空白保留字节，作为证据例外，不改写日志。仅本地固定，无推送。
