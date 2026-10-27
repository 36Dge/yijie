# FEAT-164 原仓来源日常入口收敛完成

2026-10-28。**新来源受限启动、历史检查、正常退出及后态验收通过；两个日常入口已切换到原仓内固定来源，并分别实际启动、正常退出验证。旧六目录和其中26个worktree全部保留。** 本轮3次实际App启动、3次正常退出，另有1次在回执预检被拒、未启动App的尝试；新增模型HTTP为0。

本报告接续原仓集成来源与候选交付（第1—3步），记录已批准的日常资格与入口切换。FEAT-164原S1—S4/D1—D5仍保持ADR-0022个人Mac范围的完成结论；旧报告、失败和证据保留原时点含义。本轮不重新宣称新模型质量验收或公开发布资格。

## 当前入口与固定来源

- 正常入口：`/Users/jack/Desktop/易界 AI.command`，默认Kimi K3.1 Pro可用。
- 暂停入口：`/Users/jack/Desktop/易界 AI（暂停 Kimi）.command`，同一候选暂停Kimi、保留MiniMax。切换入口前先正常退出App。
- 来源根：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/daily-source/20261027-01`。原仓本地集成分支仍为`feat/feat164-consolidation-20261027`；原dirty主工作区没有切换、清空或覆盖。
- Desktop `a211c2d04def6091352c7b3674a49355cdee18ed`，Host `7309101726dcecd48b2caa02401cfcdd6126f1fb`，Contracts `d5792d6aad18352ce8d1c5d510d345004cab3bd6`；Connectors cc56cda、专家Skills595c927、Runtime11fd450/r5不变。
- App主程序SHA-256：`80b9514a9a389ed023286eee6f10021efc14caa242677b6af3d22ca192042f4e`；回执：`86de538f8bd6fc49c53a48d7cc3a9942c74a0c4b45d6763fc566602aa7420a8a`。119包内文件、1228来源输入保持。
- 新schema2启用绑定SHA-256：`57edb7a822ee0a9658c18be4efecd5c11bd74cf98689fa79c3eebb42f7aea37c`，位于新Desktop来源的`.local/feat164-daily/activation/`，绑定本轮实际受限资格及预检，没有沿用旧D4/D5摘要冒充新资格。

增量contract-impact=none：本轮不改产品、Runtime核心/补丁、公共协议、存储schema或部署绑定规则，只验证固定制品在新位置的资格并通过既有canonical installer切换入口。Native、Host、Runtime Home和原凭据引用保持，未重跑日常D3或搬迁数据。原仓内固定干净构建来源不等于原Desktop脏工作区直接运行，也没有改成monorepo。

## 备份、数据与依赖准入

取得同一应用实例锁并确认无项目进程、无数据句柄后，完整冷备份原Native应用树、Host/Runtime Home及两Provider凭据，再制作独立inspection：17,397文件、522,400,556字节。原文件与sealed逐文件内容和元数据相等；只对inspection打开数据库API。

Native SQL41/71表、完整性/FK和保存格式解码通过；Host11/8会话idle/ready，4个Runtime库及8条Native→Host→Runtime/rollout映射通过。额外核验8个public_task_id与Host task_id匹配。全模型未来派发、待恢复、outbox、未决选择、reservation、活动turn均0；6个历史已消费grant保持，未退款、清空或重新授权。

原D5最终数据清单与本轮启动前数据一致。旧完整归档SHA复核通过；旧解包副本仅多出Finder `.DS_Store`及Native根目录mtime差异，所有原有文件保持。本轮新冷备份精确相等；未修改旧副本或删除额外文件来制造相等结论。

初始workflow检查停在Docker连接：后台未运行，遗留socket拒绝连接，旧state的ready不能作为实时证据。Owner另行明确批准既有第65号流程后，正常打开原Docker，确认8个登记容器全部停止、6个primary和来源/镜像一致。新恢复ID`70b6fda5-4c35-49c0-be96-c136c0a862b0`先完成四volume完整copy/hash，再受控recover、正常停止和canonical up。保留原失败记录、数据和副本，不拉镜像、不新增服务、不删volume、不强杀。

恢复与up各发生一次正常EnsurePrincipal审计追加。使用未修改的单次启动审查策略分别校验两条真实记录，第一条与canonical恢复事件一致；其余API/Coze业务事实保持。最终6个primary健康，真实带凭据status/editor ready。workflow保持运行；入口继续existing-ready-only，不会隐式恢复。以后依赖状态变化需重新核验。

## 实际App验收与切换顺序

1. 以新回执、原Home及本轮零派发预检建立短期D4绑定，Kimi暂停。App正常进入业务页面；原8个会话在侧栏可见，工作空间历史中的完成/中断、命令记录和结果可读；附件任务保留两CSV及原失败/警告，未改成成功；旧文本答案可读。K3只作为退役历史展示且发送禁用。已删除计划历史可读、禁止重跑，活动计划列表为空。未发送、恢复任务或保存计划。
2. 通过App的Command-Q正常退出0；完整后态副本、业务行、锁、句柄和活动WAL审计通过后，才生成新schema2绑定。先另存两个旧入口并校验，再把原文件移到私有回退目录，canonical installer以exclusive-create生成两个新入口。没有覆盖旧入口、旧App或已签名产物。
3. 从新正常入口实际启动，K3.1默认可用、MiniMax可选，旧历史及K3退役发送保护仍正常；Command-Q退出0。
4. 从新暂停入口实际启动，Kimi禁用、MiniMax保留、原历史侧栏保持；Command-Q退出0。两轮各执行完整后态副本审计，没有只用脚本文本或环境变量代替实际入口验收。

首次启动预检失败的根因为私有验收启动器遗漏已记录的`CARGO_BUILD_JOBS=2`；同源回执门禁正确拒绝，App尚未启动。修正为传入原构建环境后重新通过，源码、制品、回执未改。该失败日志和RCA完整保留。其他私有观察脚本的Darwin属性读取、任务ID映射、旧解包副本比较及双启动审计口径问题均据事实修正；未放宽产品门禁、修改权限或改数据造绿。

## 最终后态、保护与范围

最终完整sealed+inspection为17,400文件、522,551,359字节。67张Native业务表逐行保持，另外4张表仅包含3轮正常metadata probe回执、对应revision/time和停止generation；Host全部值保持，Runtime业务行和rollout保持，旧日志保留并正常追加386条。活动数据库WAL/SHM为0，历史备份内WAL保持，无手工checkpoint、删除或截断。

三轮共9次既有连接器metadata HTTP，业务工具执行0、模型HTTP0；不声称所有外部HTTP均0。旧账本与两份预占未变，不消费或释放历史预算。完整App正向never-sent取消仍NOT RUN，保留Owner已接受的安全分层替代；搜索答案正确性及亮暗/键盘/最小窗口专项继续OWNER_EXCLUDED。

最终产品操作审计确认12个原仓的原分支、HEAD、index及已有改动保持；510份受保护材料中只有此次批准的两个桌面入口改变，旧原件和副本均保留。新来源1246条符号链接及两个活动入口没有指向旧六目录。旧六目录、26个clean worktree、归档/bundle和原数据保留；未删除目录、未修改Runtime或产品源码、未推送。治理记录如另行本地固化，仅包含本报告与两份脱敏证据，不混入原工作区差异。

验收结束App已关闭，正常入口仍启用，workflow保持ready。此结论仅为本机个人入口，不是签名、商店、公开、云端或多人部署。

## 回退与后续清理边界

旧入口原件及校验副本位于`yijie/.local/consolidation-audit/20261028-01/entry-rollback/`。需要选择回退入口时，应先正常退出App并核验数据/实例锁，再保留当前新入口并恢复旧入口原件；仅切换兼容入口，不降级或覆盖数据库，不重跑D3。旧六目录提供旧候选回退来源，当前明确保留。

下一阶段若清理六目录，应重新核对当前数据/制品、引用/bundle、原工作区及反向依赖，形成刷新后的精确清单，再按明确批准正常移除worktree；本报告不执行或自动授权清理。

脱敏机器证据：[结果](evidence/consolidation-daily-entry-result.json)、[摘要索引](evidence/consolidation-daily-entry-evidence.json)。本轮私有完整备份、UI、命令、失败、恢复审计与入口回退材料在`yijie/.local/consolidation-audit/20261028-01/`；前轮集成报告及全部旧记录原样保留。

治理复核：元仓lint、57项测试、FEAT-164 claims、strict/G6文档语义检查及7份Shell语法均通过。新候选canonical同回执检查和三轮真实入口资格另有上述实际证据，文档门禁没有被当作App或公开发布验收。未重跑无关产品全量CI、真实模型或Owner已移除的专项。
