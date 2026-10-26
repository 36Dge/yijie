# FEAT-164 S4S：独立自然旧数据 App 资格

2026-10-26。Owner于18:01要求暂停，随后明确“开始继续执行”。暂停记录和失败证据保留；恢复核验原497份dirty（剔除本任务记忆插入）及8482份保护文件全部相同，六资格来源干净，最终42个bundle文件与原回执一致。此报告完成S4S结果绑定，整项继续IN_PROGRESS，不能等同完整G3/final或日常激活。

增量实现为semantic，权威源为Desktop私有部署/存储/历史读取；公共wire/schema不变，Contracts公共字段N/A。旧Runtime投影只由原generator更新来源元数据，Host产品binary保持；整项breaking不变。Owner/consumer段成威，本地实施/提交由本轮及既有明确指令授权。Codex复审不是独立人工批准。

## 已完成

- 原SQL41只读归因：unknown为原K3.1→MiniMax选择；两份occupied grant对应completed/native_terminal已释放运行，无reservation。保留原记录，不是全局执行占用，不清理、退款或重发。
- 新固定 `com.yijie.ai.feat164-qualification-v1` 身份及原隔离目录、全局单实例锁；没有任意数据路径、HOME重定向或日常库复制。旧/新canonical App分目录保留，新增入口只接受原固定loopback模型地址。
- 旧来源预检暴露历史base_commit不完整；原Contracts generator唯一更新旧投影来源号，artifact/patch/schema/generated Go及Host产品实现不变，按Contracts→Host→Desktop本地固化。
- 正常旧App自然创建K3完成会话和K3/MiniMax明日计划，正常退出。实际compiled维护入口完成SQL29→41，原备份逐字相等、29条ledger保持、8类身份/事实表保持；仅旧K3计划退役，MiniMax保持。
- 实际新App发现并修复两处Desktop缺口：固定资格身份将既有受审前身许可传给Host；精确旧K3终态历史跳过eager resume，活动/未决检查与显式模型选择保持。Runtime核心/补丁没有新增修改。
- 最终App可读旧历史，显式切换新增0HTTP；原Runtime thread保留四轮，完成新模型继续、正常停止和停止后继续，选择revision1→2。旧计划明确选K3.1保存仍关闭，单次新grant(max_runs1/occupied1)执行completed，两份旧grant逐字段保持。
- 两条本轮测试计划最后正常关闭。最终同构建重开保存全部历史、中断/计划/运行记录，新增0HTTP；两次最终App正常exit0，四Runtime库自然WAL0、完整副本integrity ok。无手工checkpoint/WAL操作、强杀、攻击或权限故障测试。

## 来源与证据边界

最终Desktop `9f5814fec6cd071d39f0c12f8f48097ce661cb6a`，位于 `feat164-s4s-candidate-20261026/yijie-desktop`；旧producer及实际迁移入口为Desktop54921df，位于 `feat164-s4s-qualification-20261026/yijie-desktop`。维护源码与依赖文件相同，证据按来源绑定，**不声称最终binary重新执行过一次SQL29迁移**。

Contracts `ca06d0999c9a08afe80ab3f34a537d492b830ac7`、Host `8cd6bccbdc1ac3906aea53d95441299f7cfefcce`均在上述独立工作树；r5投影仍5b5dad，Runtime11fd/原r5保持。最终App binary SHA `0173715c292dbea39262fcfcd70730e18c329dfc2a2ce782a353d241d3787c0c`；Host binary仍1d880cb，Runtime仍283d12e。主Desktop仍fd0c575，主仓未快进，原dirty不混入。

最终19来源、canonical构建/42文件回执、定向历史/准入/环境投影测试、产品lib/bins Clippy、fmt、docs通过。原始失败单列保留：两次旧来源检查、首次旧启动参数、前身许可/历史恢复、过宽测试筛选缺环境(20pass/20fail/4ignored)、旧测试漏列已有环境flag。没有全量测试或整项PASS声明。

本轮loopback模型HTTP5次（旧K3 producer1，新K3.1四次），真实新增0；正常重开0新增。5/5历史真实次数耗尽、30元cap、14.679001保守累计含14.188544元预占保持。恢复后原497dirty/8482保护文件已完成逐一复核；治理结果以本轮记录为准。

## 审计结论与剩余边界

S4S自然旧App、维护、模型切换、正常中断/继续、旧计划重审和新单次授权、正常退出/重开取得限定通过证据。最终Native模型切换和计划事实在只读副本复核；两次最终退出四库自然WAL0，重开SQL71表仅增加正常停止记录，身份/计划事实不变。MiniMax在迁移期间保持原模型和开启状态，验收完成后通过正常UI关闭本轮测试计划，不混淆为迁移修改。

本轮source-bound迁移证据由54921df实际compiled29→41、与9f5814f未改的迁移权威源码hash组成，完整final fresh run仍不能据此填PASS。r4真实G2V/视觉属于其原来源，十项AC整体pending。当前唯一来源与缺项见[验收矩阵](current-acceptance-matrix.md)。

剩余观察：UI的generic conversation_warning对应保存的Native view诊断runtime_notice；Host会把warning/error原文收敛为该闭集code，不能反推具体Runtime日志。personality/model_messages和previous_model fallback日志另记，切换后实际本机出站均为K3.1，没有观察到旧K3出站。计划表单刷新与原context/authorization watcher失效关闭链一致；当时未保存，重新明确编辑才成功，不声称已经证明刷新触发源或修复UX。

下一步：在既有最终来源上推进S4四组合/辅助调用的适用资格与三项final；unknown/never-sent完整App缺项仍不能靠故障注入制造。日常切换和新增真实请求仍须独立授权，新Runtime核心/patch先提交方案。不要重复已通过的S2/S3模型回合。

证据索引：[s4s-audit-index](evidence/s4s-audit-index.json)，涵盖原始失败与成功日志、source/构建回执、迁移保存判定、正常reopen判定和暂停记录。完整加密库/密钥/历史保留在私有audit目录，不提交Git。恢复审计位于 `feat164-s4t-audit-20261026/s4s-final-review.json`。

恢复后的claims/strict、元仓manifest/Contract First规则与测试、7份Shell语法均通过；详见[s4s-closeout-audit](evidence/s4s-closeout-audit.json)。这是本批记录与范围核验，不晋升整项门禁。
