# FEAT-158 阶段6：内容修订与剩余验收

> 本文保留阶段6的实施、实测与范围收窄事实。用户随后仅重新授权快捷问题替换和Shopify握手的定点根因排查，当前进展见 [10 定点排查](10-targeted-root-cause-audit.md)；不据此恢复本页早期整体验收计划。

状态：按用户最新指令转为定点逻辑审计与修复；停止追加真实调用，未通过项不改为完成。用户2026-10-11明确授权修订、修复评测问题、完成剩余验收并追加真实模型额度；外观继续跳过。阶段5全部记录保留于08，开始时状态见evidence/phase6-before-feature.yaml。

## 范围与权威

Feature整体contract-impact继续breaking；本阶段增量为semantic：新专家内容版本和本地候选启动/重开行为变化，不新增wire、安装器、Runtime执行器、数据库、权限或连接器授权。内容权威为yijie-skills现有专家源/打包产物；Host/Desktop只更新同一受管候选pin，固定Runtime不改。旧0.1.1已安装内容、DB与历史不原地篡改，新0.1.2按既有安装和引用守卫验证。

新授权记入evidence/phase6-real-model-ledger.json。先控制在额外24条合成用户消息内（这是执行预算，非用户原话中的数字），每次发送前计数；先固定新候选执行完整内容与功能轮，再根据明确新事实做必要回归，不以重复抽样挑好答案。此前18条不清零、不转为通过；消息数不等于Provider HTTP请求数。仅使用既有Kimi/MiniMax；平台经营调用与写操作继续为0。所有退出使用正常Quit/Shutdown，不强杀、不攻击注入、不破坏权限或资源。

## 内容修订依据

| 阶段5问题 | 0.1.2修订目标 | 验证 |
|---|---|---|
| c01漏新店设置 | 多问逐项覆盖；索引区分M01店铺级设置与M03商品级上架 | 新会话首答实际读取相应场景并给完整有依据清单，未知项待填 |
| c05过度确定95成因 | 已证明的算术差异与未见中间过程的原因假设分开 | 算术与业务规则边界正确，不从结果唯一反推成因 |
| c07把访客/曝光称点击率 | 指标名称须匹配分子、分母、单位、范围；缺关键量列采集项 | 无点击量时不写点击率，不能把人数与次数等同 |
| c10未找到即不存在 | 报告检查范围；无法核对指定版本时不作全域存在性断言 | 不以当前包替历史包、不伪称全机检索 |
| c11库存条件过宽 | 比较可售/实盘/占用量；缺数据不判断虚高 | 区分待审变更与已执行，比较方向和前提完整 |
| MiniMax数量标题不一致 | 输出前核对列表计数、条件与正文一致 | 生命周期轮单独审阅，不与固定模型Eval混算 |

保留原12条良性用例、全部通过的阈值、严重错误0与引用可定位100%的要求。允许澄清预期表达但不改失败定义来制造通过。优先修通用引导，不把测试问题与固定答案写成路由特例。

## 剩余工程验证

1. 内容正常升版与打包，普通38技能字节不变；Host/Desktop精确消费同一新manifest，旧资源和证据保留。
2. 新候选独立数据profile复用现有canonical入口。正常重开复用本轮标准构建产物，须核对源、资源和实际二进制摘要；不绕过drift检查、不追认旧产物、不引入通用缓存/新进程管理器。
3. 新版在旧0.1.1隔离profile正常打开时，旧历史与绑定保持原版本，继续可用或明确不可用，不能静默升级。0.1.2内容评测用新隔离profile。
4. 新候选真实完成内容、A/B隔离、解绑普通、重绑、模型切换和正常重开；实际引用对照源文件，元数据不代替模型效果。
5. 正常审批拒绝优先采用workspace外一份合成报告的普通写入请求，由原生审批UI拒绝，不伪造工具/破坏权限。若未真实触发，只记未执行。连接器选集只有真实合格且无需扩大经营请求范围时才验证，不捏造registry或借用其他需求额度。
6. 未知操作只读原ID，不重发自然出现的未知提交；无自然未知的binding/resource恢复保留正常journal与UI状态测试证据，不为了填表制造故障。按原AC区分代表性真实失败与纯状态覆盖，未满足项不标PASS。

当前所有阶段6计划均不是通过证据；最终按实际源码、构建、模型、包版本与逐项结果更新。

## 阶段6审计新增事实

合法连接器选集准备只能使用真实product registry。当前没有纯本地免凭据连接器；Shopify Global Catalog为固定官方公开、无凭据目标，可仅initialize/tools/list，不执行tools/call。最多2次显式初始化/发现逻辑流程，逐次记录；失败先诊断，不自动重发。该准备属于完成剩余验收的必要只读步骤，不继承FEAT-157业务额度、不进行OAuth或新增平台账户。

源码审计发现，worker共享resource transport在credential=None时仍对非GET要求Bearer，与Shopify现有authMode=none声明冲突。修复范围仅固定registry keyless service，继续保持精确URL/方法/metadata路由和业务one-shot permit；不得对所有credential=None放行。新增受影响仓为yijie-connectors；先正常本地测试和canonical worker构建，再由Desktop既有来源检查接入。该项尚未获得真实metadata结果，不提前记通过。

## 最新范围收窄与实际结果

用户随后明确：“只做逻辑实现检测（逻辑没有bug），不要过多的实测调用。 不要盲目扩大测试验收范围。”此指令覆盖本页较早的剩余实测计划。停止追加模型与连接器请求，停止后续产品验收；不再以原fresh-run流程作为继续实测的授权。只修已发现问题，运行必要、正常的局部逻辑检查，不新增产品profile、不扩大内容评测集。外观仍跳过。

run8实际只发送6条（本阶段6，累计24），均在停止前自然完成；第7–17条未发送。当前App正常Cmd+Q退出，canonical launcher返回0、18160端口释放；没有强杀。前6题5PASS、1FAIL，严重事实错误1：c01把“无销量资料”改成“新品无销量”。c02标题、c03资料不足、c04冲突、c05算术与归因、c06跨平台边界均PASS；12/12支持场景引用可定位，8次本地读取，无内置联网工具调用。引用正确不能抵消事实错误，AC-007和D4继续未通过。原始结果见 `evidence/phase6-run8-eval-review.json`，不得用后续修订覆盖原结果。

公开Shopify只做1次显式启用流程，内部6个metadata HTTP请求返回200，但初始化终态Unavailable，未进入tools/list，业务tools/call为0。现有日志不足以判断响应格式，不猜测修改SDK/协议，不新增诊断功能或外部请求。此前keyless认证修复的6项正常逻辑检查通过不等于握手通过。记录见 `evidence/phase6-shopify-handshake-source-review.json`。

当前构建的草稿与附件保留、取消待选、搜索空结果、详情Esc/Tab、资源准备均有实际观察。快捷问题首次“保留当前草稿”正常；从已选专家详情再次“替换文字”未预填且未返回，记录为失败观察，进入局部逻辑复核。未执行的真实审批拒绝、非空合格连接器选集、同build重开与后续生命周期，不标PASS。审批目标在真实workspace之外只是只读元数据，不是审批实跑证据。

修订的契约影响仍为本阶段semantic增量（Feature整体breaking不变）：只调整当前内容候选和已有交互，不新增wire、schema、权限或执行器。已安装0.1.2不原地覆写；事实保真修订使用正常内容升版0.1.3并同步现有单一消费者pin。0.1.3真实模型效果和修后UI均NOT RUN，不为取得全绿继续付费调用。


### 快捷问题定点逻辑结论

用真实memory router、ExtensionsPage、useExpertSummon、共享draft store、专家详情NModal/NDialog与ChatExpertChip，覆盖同一条正常“首次问题保留 → 已选胶囊深链 → 第二问题替换”序列。1项回归、vue-tsc与ESLint通过，未触发submit、prepare或setBinding调用。检查没有复现UI观察，未据此推定WebView问题已修复；Chat目标是共享draft harness，未包含真实Native与异步权限刷新。生产交互逻辑不作猜测修改，scope与导航守卫保持。实际证据见 `evidence/phase6-prefill-logic-check.json`；AC-002/003仍pending。


### 0.1.3定点内容修订

内容0.1.3／bundle0.4.3已生成；实质只改ROLE和M03：事实表逐字段对应证据原文，缺证保持未知，资料经验、计算和条件推断单列，不以店铺阶段推断商品历史。其余知识版本机械同步。原12条用例的事实、问法、预期和阈值不改，仅当前内容版本参数同步；版本差异见 `evidence/phase6-content-v013-eval-version-only-diff.json`。

Skills的11项正常测试、16条格式数据、lint、契约同步检查和canonical打包通过；38个普通技能元信息与归档字节不变。旧0.1.2的41份产物和40份源快照保持，实际已安装树/历史未改。ROLE3188字节，仍仅角色与索引进入基础上下文，知识按需读取。当前manifest为`46e3e5b9e101c252a4dcb0bc9d27c1da024ea6457be43e5be5736ccf047c6b58`；检查见 `evidence/phase6-content-v013-checks.json`。这是局部内容与结构验证，0.1.3模型效果NOT RUN。


### Host定点集成

Host现有单一ReviewedExpertCatalogDigest与三处真实包版本期望同步0.1.3；5项正常focused测试（含6个恢复子例）、scoped vet、gofmt与diff检查通过。当前角色3188字节，Host短索引4420字节，专家全局Runtime技能投影为0。仅使用正常临时安装目录验证现有journal与引用守卫，未启动服务或调用模型。证据见 `evidence/phase6-host-v013-checks.json`。

当前文档严格结构、D0声明审计、元仓lint/50项治理测试及Shell语法检查通过，记录于 `evidence/phase6-meta-logic-checks.json`。这些检查不替代D4、真实模型或UI验收。


### Desktop来源同步与本轮收口

Desktop现有单一资产pin同步0.1.3；canonical资源sync/check、专家与普通两份来源freeze、两条完整check-only权限/38技能门禁均通过。维持三个已存在的本地profile，没有新增profile或再启动产品。快捷问题生产逻辑不变，只保留一条针对实际观察的正常回归。检查见 `evidence/phase6-desktop-v013-checks.json`。

最终逻辑源码状态见 `evidence/phase6-final-logic-source-state.json`。各仓diff检查通过，Git HEAD/分支保持原样；Runtime仍无改动。0.1.3及本轮新增回归未构建/启动最终App进行UI或模型验收；旧v012构建回执仅保留当时运行来源，不代表当前源码的可重开通过。源漂移门禁不被绕过。

本轮定点逻辑修订与检查完成。FEAT-158整体仍active，D4未通过；AC-002/003保持pending，AC-007保留fail，AC-006/008/009/010仍pending。后续验收按用户最新指令停止，不把“未复现”写成“已修复”，不把“未执行”写成“通过”。
