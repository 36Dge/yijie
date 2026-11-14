# 装配、导入与迁移设计 修订2

日期：2026-11-13。本文保留修订2的设计决策。用户随后已批准实施；实际接口、边界与证据以[实现自审](07-implementation-self-audit.md)及[验收记录](02-verification.md)为准。修订1及其检查记录存于 history/revision-1，仅供追溯。下文“拟议/本轮文档”等措辞为实施前记录，不代表当前实现状态。

## 1. 权威与原生复用范围

Runtime 是安装缓存、实际配置、技能解析、版本选择／刷新和执行的权威。Host 只保存产品身份、来源快照、目录发布与操作意图，不能把 journal 中的 installed/enabled 快照当实时事实。Desktop 消费脱敏投影，不读缓存、解包或改配置。

| 操作 | 复用的原生能力 | 必要增量 |
|---|---|---|
| 登记两个本地市场 | marketplace/add 的 Local 分支，只登记本地根，不下载／安装技能 | 受管来源准入与首次登记适配 |
| 首次安装／卸载 | plugin/install、plugin/uninstall、PluginStore 原子替换 | Host 记录意图、对账；不复制安装器 |
| 更新／回滚内容 | refresh_non_curated_plugin_cache_detailed／force_reinstall_detailed | N3 薄 RPC 桥接、完成确认和显式触发；Host 不比较版本、不循环重装后开关 |
| 启停与规则修改 | config/read(includeLayers)、config/batchWrite(expectedVersion,reloadUserConfig) | 精确范围映射，保留原生层次／顺序／未知字段 |
| 安装事实与下架库存 | PluginStore.active_plugin_root/version、配置读取、原生 manifest／Skill 解析 | N2 独立于市场条目的只读投影，包括 cache-only／config-only |
| 发现与调用 | skills/list、UserInput::Skill、原生显式／隐式策略、按需加载与预算 | 只适配稳定产品 ID，不实现匹配器 |

不再沿用“只增加 installedVersion 即可完成恢复”的判断。也撤回由 Host 接管原生版本更新流程的安排。

## 2. 来源布局与版本固定（解决 F3、F4）

App Resources 仍携带完整内置市场和38项技能源；用户安装 App 后即可浏览。为跨 App 升级保留可恢复来源，实际登记给 Runtime 的是 **App Data 中两个固定根**，不同时登记 App Resources 内同名市场。

```text
App Resources/skill-marketplace/                 # 发行源，只读
  .agents/plugins/marketplace.json
  plugins/<builtin-plugin>/...                   # 完整内容
  presentation.json

App Data/skill-market/
  builtin/                                      # 固定根，name=yijie-builtin
    .agents/plugins/marketplace.json             # 唯一生效目录，原子替换
    sources/<plugin>/<source-revision>/...        # 不可变来源快照
    catalog-generations/<generation>.json        # 目录字节留档，不单独注册
  user/                                         # 固定根，name=yijie-user
    .agents/plugins/marketplace.json
    sources/<plugin>/<source-revision>/...
    catalog-generations/<generation>.json
  staging/<operation-id>/...

Host Home/skill-market-v2/state.db                # 新隔离格式，复用bbolt依赖
YiJie CODEX_HOME/plugins/cache/...                # 只由Runtime管理
```

来源快照是输入及回滚材料，不是第二套已安装缓存。App 升级时从签名／摘要核验后的随包源物化快照，复用既有资源校验和文件落盘能力；不把用户的原文件作为长期运行路径。第一次登记空个人市场、内置目录及快照均不调用 plugin/install，不给未安装条目写插件配置。

运行目录的 source 只指向本固定根内 `./sources/<plugin>/<source-revision>`。同一市场中一个 pluginName 只有一个条目。市场注册路径永不在更新／回滚中更换；仅通过目录代际改变该条目的本地 source。旧版本恢复时先把目标旧快照重新列为该条目 source，再调用原生 N3；不需要向 plugin/install 传它不存在的 version 参数，不改 App Resources，也不增设临时第三市场。

区分三个事实：App 当前可提供版本、运行目录本次选定的来源版本、Runtime 实际缓存版本。前两者是产品发布／操作意图，最后一个只从 N2 读取。稳定 pluginId 在切源时不变。原生 plugin/read 读取 source，只做预检，不能拿其路径执行；实际调用路径取原生缓存的 Skill 投影。

所有新来源完成完整校验、写盘和父目录同步后才可被目录引用；同一 source-revision 不可原地修改。来源保留范围至少包含当前安装、前一可回滚版本、未决操作／迁移和已冻结引用需要的版本。不能因新 App 到来删除这些来源；没有已审清理策略时不自动清理历史来源，空间不足时停止新导入并报告。

## 3. 三组拟议原生薄扩展

### N1 来源与触发策略

保留候选 `plugin_marketplace_mode=local_only`：默认保持 upstream；开启后复用原生 MarketplacePolicy，只准入上述两个固定根，拒绝远程／Git／npm目录物化、官方市场自动并入及后台下载。官方市场特例也须受此策略约束；不影响正常模型和已授权连接器网络。

内容刷新触发另设候选 `plugin_refresh_mode=explicit`，只改变既有刷新器何时运行，不改其版本比较、安装和错误汇总。Host 在应用升级／用户操作边界发 N3，不能自行重写更新算法。保持目录／配置缓存刷新，禁止 startup/list 在无操作意图时后台替换已安装内容。

继续保持 remote_plugin=false、tool_suggest=false、hooks=false、apps=false 和自动MCP依赖安装关闭；普通插件能力开启不放宽原沙箱／审批。Host 的真实有效配置验证与来源 pin 必须同步接入。以上均拟新增策略，不是已存在的配置项。

### N2 独立安装事实查询

候选只读 RPC 名 `plugin/state/read`。复用 PluginStore 和原生配置／解析能力，提供按有界 pluginIds 精确读取，以及两个准入市场中配置键与缓存的并集枚举。枚举不能先过滤到当前 marketplace.json 的条目，也不能先要求配置存在；缓存扫描在 Runtime 内进行，Host 不扫描或推导 cache 目录。

至少返回以下事实；最终 wire 由 Runtime canonical schema 冻结：pluginId、userConfigPresent、userEnabled（无配置为null）、effectiveEnabled、cacheState(absent/valid/invalid)、cacheVersion、manifestValid、catalogListed、原生技能元数据／路径和加载错误。停用插件也可只读解析缓存元数据，不启用、不注入、不执行。cacheVersion 直接来自 PluginStore，不能沿用以 installed 为前置条件的旧 installed_version 投影。

安装视图由这些事实派生。cache-only、config-only、无目录来源、disabled 和 invalid 必须可区分。查询自身不创建配置、修复缓存或触发来源刷新；即使插件功能被禁用也不能把已有事实伪装为空。

库存枚举须使用原生缓存布局和manifest身份验证，排除PluginStore自己产生的临时安装／备份目录，不能把它们当孤立插件。valid表示原生结构／manifest／技能可解析，不自动等于完整安全审查；来源摘要的核验仍是独立准入事实。

查询必须与同一 Runtime 的插件写入协调：复用 app-server config 串行入口及管理器已有刷新在途状态；写入未结束时等待或返回 busy/in_progress，不把暂时读不到当作 absent。Host 使用既有 Runtime generation 绑定结果，超时／断线／换代视为未知并重查，不把上一代快照用于补偿。

| 查询事实 | 可以做什么 | 不能做什么 |
|---|---|---|
| 无缓存、无配置 | 确认无安装；仍有有效新安装意图且未取消时可调用原生安装 | 把未确认RPC超时直接当成此状态 |
| 有有效缓存、无配置 | 显示安装未完成；对绑定本操作、版本及来源的首次安装，用原生配置接口补写；取消则原生卸载 | 自动启用没有对应授权意图的孤立缓存 |
| 有缓存、有配置且版本／有效状态吻合 | 确认安装或停用；恢复UI发布／完成回执 | 用新导入重试覆盖用户后来已确认的停用 |
| 无缓存、有配置 | 卸载意图可幂等补完原生卸载／配置清理；其他情况显示损坏／未完成并保留记录 | 自动删除来源或宣称已安装 |
| 缓存无效／事实冲突／仍在途 | reconciliation_required；保留来源与操作，提供受控恢复 | 盲目启用、重装、补偿删除或报告成功 |

完成与取消必须同时检查配置、缓存、有效状态，而不是只检查 installed=false。没有操作前态及同一操作归属证据时，不自动删除疑似安装。

### N3 原生刷新桥接

候选 RPC 名 `plugin/refresh`，作为既有刷新函数的受控入口，不是新的升级器。一次只处理一个已配置的受管插件，使用固定市场根、目标来源代际和该插件键，调用现有 IfVersionChanged；回滚／显式修复调用现有 ForceReinstall。版本选择、比较、复制、旧缓存替换和错误汇总均沿用 native 代码。

该入口不调用会默认启用的首次 plugin/install，不改变原插件启用配置；停用项更新后仍停用。无配置的首次安装使用原 plugin/install。返回未变／已刷新／失败及可核对事实，回读 N2 确认。RPC 失败不保证缓存未改变，必须按真实 cacheVersion 决定下一步。

桥接挂在既有PluginsManager刷新链上，复用其缓存失效及effective-plugins-changed回调，不能只调用底层文件复制函数就回成功。随后通过既有原生配置热刷新／skills强制快照确认加载到目标；通知与缓存替换完成前保持verifying，不以cacheVersion已变替代可见性确认，也不为刷新重建聊天。

Host 只选择经核验的产品目标源、发请求和保存操作进度；不解析缓存目录名或比较 semver。更新和回滚都走同一个原生刷新器。新增接口在源码实现时需源契约先行，本轮不创建代码或 schema。

## 4. 个人导入与共享目录事务（解决 F2）

Tauri 原生选文件产生不透明句柄，Host 消费已绑定本机身份／摘要的受控暂存，不接受 renderer 的任意绝对路径。ZIP至多64MiB、展开至多64MiB、2048普通文件；单文件SKILL.md至多1MiB。复用既有合法文件／路径／大小／碰撞校验，接受正常目录项，处理外层目录和macOS附属项，入口规范为SKILL.md；不在导入时执行脚本、嵌套归档或模型调用。

每包恰好一个技能，完整插件／嵌套插件声明不接受。Host 控制技能专用 wrapper，明确空 mcpServers，资源在 skills/main；合法 agents/openai.yaml 作为技能元数据保留，不把其依赖当自动安装授权。原生 plugin/read 预检，Host 不实现另一套 YAML 语义解析器。

**同一市场只有一个写入者。** 导入、卸载、更新、迁移、回滚、恢复共用市场级串行队列／锁；单个技能锁不能替代它。跨市场维护固定按 builtin→user 取得锁。借用既有 Host 单实例／owner 边界，不能由多个进程各写同一清单。普通读请求不写目录，按已提交发布索引过滤 pending 条目。

| 阶段 | 持久动作与提交边界 | 退出／重开行为 |
|---|---|---|
| received | 先持久 operation_id、输入摘要、生成身份、目标版本、请求意图、当前安装前态／epoch | 无有效源则等待重选／取消，不凭原文件路径自行继续 |
| source_prepared | 写完不可变源与代际清单留档，校验并同步；journal保存前后清单摘要 | 清单仍旧时可以发布，不能删除其他操作来源 |
| catalog_prepared | 在固定根临时写清单、同步、原子rename并同步目录；条目对native可读，对UI仍pending | 比较真实清单摘要与journal前／后代际，匹配后续办；不匹配则停止写入 |
| native_pending | 原生预检通过，取得提交门闩，持久发送意图后调用原生安装 | 重开先N2查询，按表恢复；不得直接重发 |
| verified | N2与skills快照确认目标身份／版本／启用；取消意图未抢先提交 | 一笔bbolt事务发布身份、目录代际与complete结果，这是UI成功提交点 |
| cleanup | 仅移除本操作暂存；来源保留／回收按引用规则 | 清理失败不重装，记录待清理 |

plugin/read 预检需要条目先存在，因此采用“原生可预检、UI未发布”的 prepared 阶段；Host 目录发布索引仅控制产品可见性，不声称它是安装真相。prepared 条目不得进入可选择列表；推荐工具和自动安装入口关闭。首期在 native_pending 至 verified／补偿结束期间使用维护门闩阻止新的聊天提交；已有任务未结束则先等待／提示稍后完成，用户仍可取消。一次完整导入只有 verified 后才算完成。

取消意图必须持久：发送前可撤回prepared条目；发送后先查N2，只有本操作拥有的首次安装可用原生卸载补偿。已存在技能的重复导入不删除旧安装。native确认无缓存、无配置后，才撤销目录条目与发布索引。任何未确认状态显示“结果待确认”，不伪装取消成功。

卸载顺序：写意图与前态→原生卸载→N2确认→同一市场锁内处理目录／来源状态→提交发布索引及结果→清理本操作暂存。当前仍发行的内置项保留运行目录条目、source和卡片，只变为未安装；个人项和已下架项才移除可见目录条目，来源按引用保留规则处理。清单更新和DB提交不是跨存储原子事务，依靠事前journal与前后代际摘要补完；不先删源再等卸载。

## 5. 稳定身份、去重与版本

内置产品skill_id沿用现值；native pluginName使用受控builtin前缀与稳定映射。个人skill_id为应用生成的UUID身份，native pluginName用不同user前缀，跨两个市场也保持唯一，避免原生命名空间只含pluginName造成同名碰撞。显示名称不做主键。

个人首次内容版本固定1.0.0；不同内容即新身份，不提供本期原地编辑／升级。归一化内容摘要对相对文件路径与字节排序计算，忽略允许移除的系统附属项，包含所有实际资源；生成ID不参与去重摘要。同一用户作用域相同摘要已安装时返回原对象，保留启停；已卸载的同内容再次显式导入复用墓碑身份、增加操作epoch，并默认启用。旧取消／清理请求必须匹配epoch，不能作用于新一轮安装。

区分 skillContentVersion、完整contentDigest、nativePackageVersion。旧聊天保存的{id,version}仍指原内容版本；native版本只用于缓存与刷新。wrapper必须显式写版本，不能落入原生缺省local。推荐native版本为 `1.0.0+yj.<32位sourceRevision前缀>`，长度小于64；sourceRevision完整SHA-256基于内容＋wrapper配方版本＋受控元数据（不含生成的version字段，避免循环摘要）。完整摘要才是来源身份，前缀冲突拒绝，不以截断值证明相等。

注册索引保留旧ID／内容版本到完整摘要及native身份的映射。未能确定历史内容摘要时不把当前最新版冒充旧版；提示重新选择。新native名称从原生快照读取，前端不继续限制为旧短名称，也不在Host改写用户自然语言来强行匹配。

## 6. 下架、无源和恢复库存（解决 F4）

页面管理视图采用“当前发行目录＋N2实际库存＋有明确未决操作的条目”的并集，按稳定身份合并。当前发行目录决定能否新增安装；实际库存决定安装／启停事实；Host registry补来源与展示，不能凭历史complete记录伪造库存。

App新包移除技能时：未安装项从可添加目录移除；已安装项保留卡片，标“已下架／不再随应用更新”，仍可启停和卸载，运行目录保留其最后核验来源。停用项也要显示。不能因plugin/list或旧plugin/installed无条目而把它隐藏。

Runtime中有缓存／配置而来源丢失时，N2仍列出“来源不可用”项；允许正常停用／卸载，不自动补装。没有可信身份映射的孤立缓存作为异常管理项，不能自动归为某个内置技能或启用。恢复需重新取得并核验来源。

下架后卸载不再提供普通加号；受控回滚只可使用原已安装来源与维护授权。保留来源不等于向新用户继续推荐下架技能。旧目录条目与缓存枚举之间的差异必须进入验收。

## 7. 迁移与旧规则（解决 F3、F6）

### 7.1 私有格式与迁移提交

旧 `.yijie-state/operations.json` 与 `operations.v2.db` 的原记录、指纹及结果按原字节保存为迁移输入，正常退出并关闭存储后制作副本。专家仍使用原记录codec和业务恢复规则，存储入口由版本化适配承接。本需求使用隔离的 `skill-market-v2/state.db`、独立schema版本和桶，复用bbolt及通用操作ID／结果重放代码，不能把新phase塞进旧closed enum。该库只含身份／来源／操作／发布和迁移意图，不镜像实时安装状态。

**降级保护先于任何native安装。** 在新库元数据、旧backend的可读写兼容副本和原字节快照均同步完成后，将旧公共入口operations.json按原子替换发布为拟议schema_version=3、operations=[]的路由标记。已核对旧Host只接受1／2，会在recoverTransactions之前拒绝3；新Host的通用loader必须识别3并按新库中的受控backend定位读取旧codec，不能依赖页面开关才启用reader。专家旧格式写入兼容backend，不能覆盖公共v3标记；其资源、记录语义与操作结果不变。原普通旧日志成功结果继续只读重放。

v3标记和新库元数据不是跨文件原子事务：元数据／副本先落盘，标记最后提交。标记未发布且没有native副作用时可仍走旧路径；标记已发布但新元数据不可读时拒绝启动管理服务，不能自动回旧writer。真正旧二进制降级不在本期支持范围；本期回滚只到保留v3 reader的兼容模式。若未来要撤销v3标记，必须另行证明所有现存普通／个人／专家状态均可由旧reader表示，不能只把数字改回2。

为既有普通技能已完成操作保留精确ID、输入指纹、旧结果及旧API reader，重放不得重新执行。旧未决普通操作须先由既有合法恢复流程收敛；未收敛对象不得转换到新writer。专家操作不能被批量迁移或裁剪。

迁移记录逐项持久 old ID、内容摘要、原根、规则快照／配置版本、原期望与有效启停、目标native身份／来源及阶段：prepared→native_verified→rules_verified→routing_committed→complete。崩溃恢复只以已同步记录＋原生事实决定续办，不按“新目录存在”猜迁移完成。

`routing_committed` 是唯一普通技能writer切换点：同一事务写该对象的 authority=native；所有普通读取、安装、启停、扫描、通知、重试、清理均先读此路由。切换前legacy为权威，新副本不接聊天；切换后legacy writer不得重注册或恢复该对象。迁移批次未全部核验前不开放新聊天；重开先完成或回退未决对象，避免同一技能两套根同时生效。

### 7.2 正常迁移顺序

1. 正常退出／维护启动，阻止新普通、专家、计划任务提交；使用现有Runtime活动事实确认无相关运行任务，关闭存储并取得单实例所有权，不强杀。
2. 去掉Starter触发，但保留旧标记reader；冻结旧状态与上述操作日志，先按7.1发布v3降级保护。验证旧源／回执，不把损坏对象当有效安装。
3. 将旧安装内容去除明确的Host回执／停用控制文件后物化为builtin根内的来源快照；技能文件及相对资源字节保持，原内容版本不变。生成受控wrapper和身份映射；新App较新来源另存，不混入本次迁移。
4. 同一catalog事务将目标条目source指向兼容快照；通过原生install创建新缓存，使用N2读取包括停用项在内的真实name/path/version。维护门闩内恢复原插件意愿，尚不开放聊天。
5. 完成下述规则重绑定与原生有效状态验证；在原生extraRoots替换中仅移除已迁移普通根，保留专家与其他已有合法根，不发送空集合误清所有根。
6. 原生配置版本与快照一致后提交routing_committed，停止该对象legacy对账，再complete。失败对象按8节回退，不能以部分成功结束维护。

### 7.3 技能规则重绑定

使用原生config/read(includeLayers=true)记录当前CWD、用户层、SessionFlags及版本；规则的解析、优先级和有效结果仍由原生config_rules处理。

- 能证明由旧Host管理且与旧意愿一致的路径启停规则，转换为插件enabled并移除该重复规则，防止迁移后的普通开关被旧false规则永久压住。证明需绑定旧回执／最近有效操作／实际配置，不仅凭路径前缀。
- 其他明确指向该技能的用户路径规则，映射到N2返回的新缓存路径；按名称规则映射到新原生全名。保持值、原层与相对顺序，保留不相关／未知条目。旧名称同时命中非受管技能时保留原规则，并为已确认受管身份增加同层对应项；不能全局重命名影响别人。
- SessionFlags保留在其原作用域，不能写成全局用户配置；只更新本需求拥有的启动／恢复参数。无法确定归属、作用域或目标身份时停止该对象自动迁移，显示需要检查，不默认开启。
- 通过原生config/batchWrite的expectedVersion和reloadUserConfig提交；版本冲突重读再计算，不覆盖用户并发修改。回滚只撤销本次有前态／后态证据的精确编辑，不整体恢复旧config.toml。
- 内容更新会改变缓存路径，同样执行路径规则重绑定；整个过程处于同一维护门闩。原生快照在实际CWD确认有效启停保持后才释放。普通开关只写plugin.enabled，用户显式的额外原生策略仍可能使runtimeVisible=false并显示原因。

历史聊天、rollout正文和已接受任务不改写、不自动压缩或重跑。有{id,version}的重发核验精确内容；仅旧短名文本保持可读／复制，不承诺它自动等于新全名，提供重新选择入口。草稿、未发送outbox、重试和计划中的引用纳入迁移清单；不可映射时在发送前拒绝，不替换最新版。

冷恢复旧会话须单独验证原生目录是否更新，不能用新会话结果覆盖旧会话。若原生仍保留旧初始目录，维持历史和旧源引用，不由Host插入目录副本，也不自动触发付费压缩；UI提供重新选择／新建任务入口。保留历史不等于保证旧初始提示立即获得新名称，验收需明确这一边界。

## 8. 更新、回滚与资源使用

Host只选择随App提供的目标来源并发布目录意图；N3决定是否变化并调用原生刷新。每次只有一个目标插件，源版本、目录前后代际、原cacheVersion与启停／规则快照预先写journal。已安装项更新，未安装项只更新目录；个人技能内容不随App升级替换。

所有会替换／删除资源的操作与turn/start入口共用维护门闩，覆盖普通／专家／计划和现有Runtime仍运行的子任务事实。先停止接纳新任务，再确认空闲；不能仅检查一次activeTurns后立即释放锁。若无法安全等待则返回busy，用户稍后重试，不新造任务调度平台。

回滚顺序：持久回滚意图→同一市场锁内恢复目标旧source及其代际→N3 ForceReinstall复用原生刷新→N2确认实际版本→原生规则映射回旧路径、恢复本次拥有的启停编辑→提交发布／路由结果→释放门闩。旧源缺失／摘要不符／结果未知则停止并保留现场，不依赖PluginStore临时备份，不直接写cache。

新安装取消与升级回滚不同：前者可卸载本操作新对象；后者必须恢复先前来源，不能通过卸载清空原有技能。副作用超时以N2重查，旧操作epoch不得清理后来重新导入的对象。

回退到legacy权威仅可使用明确支持新格式的兼容Host，按对象恢复旧源、撤销本需求native注册、原生回读和规则编辑后再提交authority=legacy；失败仍保持维护状态。不能直接用旧二进制写新数据。已具新reader的模式可保留个人来源并停用，不能删除用户导入。专家数据和不相关配置不恢复旧快照覆盖。

## 9. 契约与实施边界

本轮文档contract-impact=none；拟实施总体breaking。原生N1／N2／N3以yijie-codex源码及canonical schema为权威，先固定候选，再进入Contracts兼容投影。易界来源发布、导入操作、库存投影和新Native IPC采用版本化源契约；不得给旧38项清单reader塞个人技能或新名称。

Host／Desktop启用前共同验证新能力与私有格式最小reader；未知版本拒绝管理，不自动切回旧writer。真实commit／digest在实施时形成，本方案不伪造。跨仓依次为Runtime薄扩展→Contracts→Skills来源生产／Host接入→Desktop→定向及正常真实验收。

保留独立的产品D0／实施批准；本轮仅修改文档。不是上游升级、代码补丁、数据迁移、付费模型或发布授权。所有新增接口名称、资源根、字段和格式均为修订2设计，不能在实现前当作已存在能力调用。
