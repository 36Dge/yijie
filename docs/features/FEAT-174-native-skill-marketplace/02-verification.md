# FEAT-174 实施验收记录

2026-11-14 七项代码复审修复已完成。当前结论以[最终修复验收与自审](09-review-fixes-verification.md)及[新证据](references/review-fixes/checks.json)为准，已补齐完整工具市场聊天、实际维护命令、兼容冷启动与恢复。下表保留原始分层证据，不再单独作为当前完整链路结论。

2026-11-13 实施，2026-11-14 最终复核。已完成本地候选的安全定向验证。真实供应商业务质量、生产签名分发及日常用户数据切换不在本次验证结论中。下面将真实原生窗口、真实 Runtime、本机协议回放、纯状态测试和源码自审分开记录；不把未制造的故障报告为通过。

## 证据入口

- [机器记录与摘要](references/implementation/checks.json)：实际 Runtime、UI步骤、数据范围、安全边界和日志摘要。
- [Host 定向验证](references/implementation/host-tests.log)：实际固定 Runtime；`-race`；涵盖生命周期、规则、旧数据、回滚、正常取消/重开、并发、原生加载与活动任务门闩。
- [Runtime 3项定向测试](references/implementation/runtime-tests.log)：原生Store事实、停用更新/回滚、本地策略。其余313项未运行。
- [前端79项定向测试](references/implementation/frontend-tests.log)、[资源装配测试](references/implementation/native-resource-tests.log)、[Native离线投影测试](references/implementation/offline-native-tests.log)、[契约3项测试](references/implementation/contract-tests.log)、[类型检查](references/implementation/frontend-types.log)、[lint](references/implementation/frontend-lint.log)、[Go vet](references/implementation/host-vet.log)。空日志表示相应命令成功且无诊断。
- [窗口操作后的只读核验](references/implementation/ui-state.json)：正常退出后读取实际私有日志；原生N2返回的路径下，单文件与四文件资源包逐字节一致；不推导缓存布局。
- [最终窗口数据核验](references/implementation/ui-final-state.json)：验收技能正常卸载后，15笔完成、1笔取消、零聊天会话；零安装再经真实窗口重开确认。[工作区保护核验](references/implementation/workspace-protection.json)记录六仓HEAD与26个已有Desktop文件的基线比较。

## V01–V24 分层结果

| 场景 | 结果与证据层次 |
|---|---|
| V01 首次展示 | **PASS**：真实原生窗口展示38项，分类5/9/7/9/8、零安装；卸载验收项后正常重开及重扫仍38个安装按钮、零开关。原生38项预检后库存仍空。Native/前端定向测试另验证离线目录只标记unknown、禁用管理，不把服务不可用当作零安装；没有通过终止服务制造离线故障。 |
| V02 内置添加 | **PASS**：窗口加号安装“跨境营销文案”，出现开关与卸载；Host调用原生本地install并回读。操作ID重放由真实Runtime集成覆盖。 |
| V03 导入格式 | **PASS**：窗口完成SKILL.md、根ZIP、外层目录ZIP；原生安装后默认启用。资源包4文件在实际原生路径校验字节一致，脚本未运行。 |
| V04 身份与重导 | **PASS**：停用后同内容ZIP重导保持停用且不新增卡片；同名不同内容显示两项并可独立启停；卸载重导复用身份、epoch从1/2进入3/4并开启。旧取消由集成验证。 |
| V05 独立事实 | **PASS（分层）**：原生Store测试覆盖无安装、cache-only、config-only、停用、目录外库存；invalid/in-flight分支通过源码与状态决策审计，不制造真实损坏/故障。 |
| V06 部分安装恢复 | **PASS（实现审计＋分层）**：仅绑定本操作/epoch/目标版本的cache-only可补原生配置；未归属项不启用。正常重开已验证；没有通过进程故障制造部分安装。 |
| V07 部分卸载 | **PASS（原生事实＋实现审计）**：完成条件同时要求缓存与配置消失，源后处理；config-only已由原生Store覆盖，不伪称真实故障复现。 |
| V08 取消与在途 | **PASS**：原生安装前及安装完成/发布前的正常取消均验证；在途保留尚未确认，旧epoch无副作用；窗口缺描述文件正常取消恢复。 |
| V09 并发目录 | **PASS**：真实Runtime并发导入A/B均保留；全服务写入串行覆盖两个市场，卸载/更新复用同一队列。具体导入A＋卸载B的所有排列未穷举。 |
| V10 prepared可见性 | **PASS**：真实集成在导入prepared阶段读取目录，用户项尚不可选；窗口错误导入仅显示待处理操作，没有产生技能卡片。 |
| V11 目录恢复 | **PASS（正常重开＋审计）**：来源/目录journal先行，原子发布和前后摘要校验；正常关闭重开续办。任意掉电组合未注入。 |
| V12 完成重放 | **PASS**：窗口重导与刷新、实际Host completed回执重放不重装；取消过晚的目录外卸载状态以纯决策用例确认原完成结果。 |
| V13 更新与回滚 | **PASS**：两个合法版本经原生N3更新、ForceReinstall回滚；保留停用，路径规则绑定到原生返回的新路径。 |
| V14 下架 | **PASS**：真实Runtime集成中正常撤下发行条目，已安装停用项仍有管理投影；卸载后不再作为可添加项。 |
| V15 目录外/缺源 | **PASS（分层）**：N2独立枚举不依赖当前目录；孤项不认领，只有停用/卸载；来源不存在显示来源不可用。未删除日常来源制造故障。 |
| V16 规则保持 | **PASS（正常集成＋纯映射）**：旧路径开关、附加路径规则及名称复制/相对顺序覆盖；SessionFlags/非用户层不能证明归属时在安装前停止。真实所有跨层组合未穷举。 |
| V17 writer交接 | **PASS**：实际旧格式安装/停用→原生迁移，路由提交后旧扫描不复活旧根；缺失路由事实不得授予legacy写权限的纯决策用例通过；专家受管资源既有定向用例通过。 |
| V18 日志与重放 | **PASS**：v1与v2 bbolt字节快照、旧成功回执、新v3通用reader、兼容codec后续写入均验证；未确认普通请求以既有错误codec收敛，保留原ID/指纹和迁移前字节，未重发。 |
| V19 来源/配置回退 | **PASS**：固定来源版本、原生内容回滚、兼容legacy回滚及resume验证；个人来源保留，恢复其本次停用意图；配置/用户意图冲突会停止，不整体覆盖配置。真实并发手工编辑未注入。 |
| V20 无重复更新器 | **PASS**：N3调用原生刷新函数、PluginStore、失效通知链；Host不选semver、不解析缓存目录、不复制到安装缓存。 |
| V21 门闩和来源 | **PASS**：真实活动本机turn期间安装资源保持，其他turn不能越过维护入口，任务正常结束后卸载完成；空会话不再误报busy。本地来源由Native policy和固定根约束。 |
| V22 引用/历史 | **PASS（正常链路＋边界审计）**：按实际CWD及{id,version}精确确认，使用结构化Skill输入；旧接受请求先重放；真实冷恢复保留原消息。草稿/outbox/计划数据未批量改写，不可映射时发送前拒绝。 |
| V23 原生加载/依赖 | **PASS（本机协议）**：显式正文加载、冷热恢复、新会话隐式目录、正文按需和implicit opt-out以真实Runtime＋普通本机HTTP响应验证；MCP缺失真实覆盖，授权/未知/就绪为纯事实表。真实供应商自主选择和业务效果NOT RUN。 |
| V24 原生UI | **PASS**：真实macOS窗口1180×760亮暗检查、加号/开关/卸载、原生文件选择、键盘Space/Escape、普通缺description、取消、正常菜单退出/重开。外观和窗口大小恢复。 |

## 六项复审问题关闭情况

F1由独立N2事实及幂等意图恢复关闭；F2由市场串行、目录代际journal和发布过滤关闭；F3由固定根下完整来源及兼容回滚关闭；F4由目录/库存并集与孤项管理关闭；F5由原生刷新桥接关闭；F6由v3通用reader、原字节快照、旧codec、CAS规则、路由和结构化身份关闭。具体实现和自审修正见 [07](07-implementation-self-audit.md)。

## 未执行项与影响

- 强杀、替身可执行文件、权限故障、攻击或危险ZIP：按用户长期条款未执行；用正常生命周期、合法初始事实和纯决策验证相应分支，不能等同于任意真实故障组合已复现。
- 真实供应商模型/付费工具：额度0，未执行。仅本机普通协议回放；不评价38项技能的商业效果或真实模型自主选择质量。
- 日常用户数据迁移、公开签名分发：未执行。UI使用独立Native/Host/Runtime目录；迁移验证使用普通旧格式数据及正常安装副本。没有修改历史聊天正文、清库、提交、推送或发布。
- 全量跨仓/历史故障测试：未运行。这里的PASS限定上述证据层次，不表示全仓或生产放行。
