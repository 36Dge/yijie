# FEAT-174 实施记录

2026-11-13：用户明确授权按修订2实施，D0检查已通过。总体contract-impact=breaking；无付费、提交推送或发布授权。

基线：六仓状态与46份原有文件/完整diff保存在元仓.local/diagnostics/2026-11-13-feat174/baseline。现有Desktop改动保持。

原生：独立.local/native-skills-market/workspace经canonical patch链生成，新增0025补丁实现N1/N2/N3；canonical codex-rs未编辑。cargo check codex-app-server通过；3个managed_plugin_定向测试通过（部分状态、下架库存、停用更新及回滚、来源策略）。独立release构建进行中；未激活日常Runtime。

契约：skills/market-v2源、生成器与3项定向契约测试通过；已按源生成Go/Rust/TS消费。Runtime投影生成器等待canonical构建输出，不从手写schema生成原生契约。

技能：新增本地原生源打包器，已生成38项，安装数为0；未改原专家资源。

仍需：完成原生构建与协议握手、Runtime投影、Host服务/导入/迁移/回滚/门闩、Desktop接入、正常客户端验收与自审。所有产品AC保持pending。

## 实施检查点（继续执行中）

- Runtime独立release已构建，canonical schema已生成，manifest SHA-256 `6f4bae289481949d029eef420682f772d7eb4db96b2d7da01ba81cd536e095b6`；binary `eed043017769f3483c08cc459768850e5589c1a1626f0b38f29c3ba7d3a9edf8`。原版canonical源码未修改。
- Contracts的原生投影、skills v2 Go/Rust/TS及离线validator均已生成并消费；新增版本化HTTP源 `openapi/agent-host/skill-market-v2.yaml`。修正原生union Go类型需使用RawMessage别名的问题。
- Host新增 `internal/skillmarket`，安装/卸载/版本刷新/技能解析都调用原生接口；来源准备、校验、目录代际、操作意图和身份在Host。补入普通ZIP/单md导入、去重/epoch、取消/恢复、库存/下架、App发布更新、规则重绑定和维护门闩。
- 旧Skills通用loader识别v3标记，旧codec兼容backend与原字节快照保留，专家继续旧codec。新Host先获取现有sessions.db的进程所有权，再做旧恢复/交接。新增兼容回滚/恢复维护入口 `desktop-host --skill-market-maintenance=rollback|resume`；有用户规则/意图变化时停止，不能覆盖。
- Desktop接入v2命令与受控原生文件选择；源随App资源打包；移除Starter自动安装触发；前端复用现有卡片/Store并显示个人技能及未决操作。新模式使用结构化Skill引用，ChatPage仅改动对应的一行，保留用户此前所有变更。
- 首批7个前端文件81项测试通过（后续新增/调整仍须重跑相关项）；vue-tsc与cargo check通过（后续变化待复验）。
- Host真实原生测试6项通过，日志 `/tmp/feat174-safe-integration.log`：零安装初始目录、格式/字节、重复/重导、停用刷新、规则/回滚/下架、旧迁移/旧结果/v3reader、正常取消后补偿、正常重开、并发双导入。原生独立握手记录在 `yijie-agent-host/.local/native-skill-marketplace/probe.log`，实际发现并修正marketplacePath应为清单文件路径。

仍需完成：兼容回滚恢复及v2旧DB/专家证据补测；实际CWD/新旧会话原生加载与维护门闩证明；HTTP/Native消费定向测试；来源/契约check和Host完整编译；冻结新的本地source closure；规范开发App构建及正常界面验收；最终自审及逐项V01–V24证据分层记录。日常Home未迁移，未启动付费/外部模型；本地loopback加载验证尚待执行。严禁强杀、替换可执行文件、权限故障及攻击fixture。

## 完成记录

后续独立候选修复空会话busy判定，最终来源 `8d1ac11567b3a7c47296c89ecad1272d6f886c2904a5c23f546874b3a0ba508c`，binary `e03bdbd2b4167022ee85c2df86dacff1a0a5c082321a9aa19875b29136a96cf5`。旧候选保留，canonical源未改。

最终已完成真实Runtime正常生命周期/迁移/兼容回滚及resume、原生隐式目录与opt-out/显式正文/冷热恢复、依赖事实、v1/v2日志快照/旧回执/未确认请求收敛、活动任务门闩与晚到取消等定向检查。窗口验收通过规范start-ui入口，三套数据目录明确隔离；38项初始零安装，导入/重复/同名/启停/卸载/重导、错误/取消、1180×760亮暗、键盘、正常退出/重开均实际观察。资源包4文件字节和单文件内容在正常退出后从N2前态给出的原生路径验证，未推断缓存布局。

Docker最初未就绪，按正常应用流程启动；规范入口随后通过原有容器身份与存储检查。开发资源stager原先只接纳两槽位，已把新完整来源槽位加入同一精确校验及bundle配方，没有绕过校验。每次App退出后专用服务正常停止。

最终状态与分层未执行项以02、07、feature.yaml和references/implementation为准；前面的记录为过程检查点，不再表示当前待办。无付费供应商调用，无日常数据迁移，无提交推送或发布。

2026-11-14最终复核：补齐离线浏览unknown状态与legacy路由缺失时拒绝接管的边界，重新生成契约消费者并冻结源码候选。前端79项、Native离线投影1项、契约3项及安全定向Host检查通过；工作区26个已有Desktop文件和六仓HEAD再次比较一致。验收App、专用服务、Docker Desktop均正常退出，证据按实际运行结果归档。
