# FEAT-164 D5 日常入口与启用完成

> 恢复收口（2026-10-27）：用户已要求继续；第68号记录的最终治理检查、证据整理和保护复核已完成，详见[第69号最终收口](69-d5-resumed-final-closure.md)。第68号保留为暂停时点历史。

2026-10-27。**D5 已完成，Kimi K3.1 Pro 已作为个人本机日常入口的可用默认模型。** 正常启用→正常退出→同源暂停Kimi回退→正常退出→同一日常入口再次启用→正常退出与完整后态审计全部通过。本轮3次App启动、3次正常退出、0新增模型HTTP。没有重跑D3、改Runtime核心/补丁或推送。

## 交付入口与使用边界

- 正常入口：`/Users/jack/Desktop/易界 AI.command`。调用本轮固定canonical候选，Kimi K3.1 Pro启用。
- 兼容暂停入口：`/Users/jack/Desktop/易界 AI（暂停 Kimi）.command`。先正常退出App再使用；保持同一reader和数据，仅暂停Kimi，MiniMax保留。
- 启用记录与环境位于`feat164-d5-candidate-20261027/yijie-desktop/.local/feat164-daily/activation/`，无密钥值。记录固定精确制品/原Home/批准/D4和预检摘要；日常重开不必每天重签24小时验证记录。
- 不直接双击候选原始bundle或旧App绕过canonical装配。旧App、原dirty工作区和所有备份保留，未替换已签名产物、未改Dock/登录项/默认程序。
- workflow保持existing-ready-only；本轮未启停/恢复它，D5观察时6个primary健康并通过真实鉴权ready；暂停恢复后的文档收口不重新宣称其即时状态。日后依赖未就绪须按原受控流程恢复，入口不会隐式up/迁移/轮换凭据。

最后一次验收结束后App已正常关闭，日常入口仍启用；需要使用时打开正常入口。启用不生成计划grant、不恢复旧K3或unknown、不自动发送消息。用户今后正常使用与本次Agent零调用验收明确区分。

## 阻塞根因与最小修复

F61-02：原schema1把D5也限制为24小时有效、model_http_limit=0和no_dispatchable_work，混淆切换验收与日常使用。Desktop新增schema2、独立`feat164-daily-activated-homes-v2`和显式Owner/ADR-0022单Owner本机范围；schema1 D3/D4过期、零派发、D4暂停要求全部保留。schema2不能授权迁移或首次受限启动；候选/源/回执/Home/policy变化仍拒绝，不能自动刷新摘要。

新canonical installer只创建不存在的两个Desktop入口，采用白名单环境与逐项shell引用，固定原canonical参数；不覆盖文件、不创建新Home、不包含secret。Native/renderer/Host/Runtime业务源码未改，旧模型和计划授权保护仍由原生权威执行。

F61-03：既有validator把production_hardened G5/G6强制为public，与本地持久数据治理冲突；进一步发现ADR-0018第8条明确禁止该Profile免登录。没有只删除检查了事：先形成具体[ADR-0022](../../adr/ADR-0022-feat164-personal-local-activation.md)，Owner实际回复“批准该限定例外，继续完成 D5”，才Accepted。完整G0—G6检查保留，local G5/G6额外要求Owner/时间、单Owner范围、证据、实际Accepted ADR及精确当前Feature的scope标记，不能借别的需求批准放行。

此例外仅FEAT-164在本机固定Native身份使用，不允许公开、云端、多人、多租户或签名发布。技术治理修正为semantic；业务公共wire、Native command/SQL schema及Runtime无变更。没有重写过去失败、替代或排除项。

## 来源、验证与阶段顺序

Desktop `39b0fbeb3a8c092768a7f0dfe64bd595d5e6be00`，Contracts `d5792d6aad18352ce8d1c5d510d345004cab3bd6`；Host a3d8767、Connectors cc56cda、Skills595c927和Runtime11fd450/r5保持。Native和renderer对第66号D4逐字一致。新App SHA `e13a3aa7289dd6f4cf11875965cf078c4ebaf1c09a9818aee4967e4dddcc9e02`，receipt `f5cf6b8ff4bff57785f89156c8eaa46c1d508c77394819ed1f3edc952e041c5c`，119包内文件、1228源码输入精确核对。

13项激活测试、7项原短期绑定回归、9项入口/来源单元、19项同源生成、lint/typecheck、docs及canonical prepare-only构建通过。已验证schema2跨日/后年仍有效、缺失/撤销/未知范围拒绝、不能用于D3/D4、旧制品不支持时拒绝、原Home不重建及可重复生成的入口参数。测试仅正常数据/结构化配置；没有故障注入、替身二进制、恶意资源或权限破坏。新增代码不含Rust变更，未重复无关原生全套攻击fixture。

正式启用前完成本地G4/G5及Owner批准，检查记录先本地提交7a2b7c3，之后才创建启用记录和Desktop入口。新完整冷备份/inspection为17,394文件/522,147,353字节，与D4最终后态相符；SQL41/Host11、四Runtime库、8条跨存储映射、实例锁/无句柄、6个历史消费及全模型零派发核验通过。

真实三轮通过同一已安装入口/暂停入口执行：第一轮K31可用且默认，K3不在活动目录；原已完成答案仍可读、旧K3会话发送禁用、旧计划列表为空。第二轮仅Kimi禁用，MiniMax可选。第三轮同一正常入口恢复K31可用，没有重新生成批准、修改数据或发送消息。每轮⌘Q正常退出0，App/Host/Runtime/worker/adapter结束，锁与数据句柄释放。

## 后态、预算与交付结论

最终完整sealed+inspection为17,397文件/522,400,556字节。三轮67张Native表逐行保持，包含历史、附件、模型操作、计划、grant；Host全部值保持，Runtime目标/记忆/线程与rollout保持，旧日志不删、正常追加585条。活动DB WAL/SHM字节0；所有历史迁移备份内WAL/SHM原样保留，无手工checkpoint/清理/强杀。

仅既有Shopify metadata探测产生3组正常回执、installation revision/updated_at以及3条正常stopped generation；授权generation与凭据引用不变。共9次非模型metadata HTTP，没有商家业务工具执行；不声称零外部HTTP。模型HTTP新增0，累计13；45元上限、29.740299元保守累计、两份14.188544预占及7份旧账本/快照保持。

D5及FEAT-164本次明确批准的个人本机交付范围完成；G4/G5按启用前真实资格，G6按三轮观察与完整后态分别判定，不拿D5直接冒充G6。完整App正向never-sent取消仍NOT RUN，保留Owner已接受的安全分层替代；搜索答案正确性及亮暗/键盘/最小窗口仍OWNER_EXCLUDED。公开/云端/组织/签名发布不在本次批准范围，不能继承本地结论。

原10仓的既有改动、500份dirty及混合memory原内容保留，仅提交本轮FEAT-164专属差异。全部源码/制品、审批、检查、UI和完整备份的私有原始记录位于`feat164-d5-activation-audit-20261027`；Git只保存脱敏计数、判定、摘要索引。证据见`evidence/d5-readiness.json`、`d5-closure-summary.json`、`d5-post-state-observations.json`、`d5-review.json`及最终治理/保护记录。
