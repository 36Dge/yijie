# 第一组三位专家修复与复验

2026-10-16，用户要求继续修复18记录中的未通过项，重点为事实保真与退出异常，保留原专家和历史。沿用demo_fast/local和现有专家引擎，不新增平台能力，不提交/发布。

## 决策与验收

`contract-impact=semantic`：修正行为资产及本地版本共存/目录选择语义、修复Native文件元数据访问；experts/1和manifest v3形状、ExpertRef、权限、DB schema保持。权威源仍为Skills资产/包、Native私有数据库实现；固定Contracts不变。旧候选与旧资源精确字节保留，新的候选须配套Host/Native消费者后才能启动，不能让旧reader消费新候选。

现有manifest已经区分expert_id和安装id，但两个消费者只接受每专家单版本。为了不覆盖已被历史引用的0.1.0，用同一受管安装器增加独立安装id的0.1.1包，原0.1.0继续随包保留。目录只展示每expert_id的最高语义版本，历史精确解析按id+version；同版本重复、安装id复用和未知历史版本继续拒绝。资源保护只豁免权威目录能证明安装目录互异的版本，不能简单删除ResourceInUse检查。这是在原资源链内补齐版本保留，不另建引擎、库、权限或影子协议。

小红书与跨境新版本明确：事实→可用主张→待证主张→逐句复核；商品属性不自动推出效用/比较优势，广告正文、标题、标签、视频字幕都受同一事实边界约束。材料中旧AI文案不能升级为事实。给用户可用草稿与简短事实对照，不靠免责声明掩盖未证主张。示例、checklist、eval/rubric同步；保留0.1.0失败样本。

真实复验先使用原模型Kimi-K3/max/ask和合成资料：2份原失败输入、2份不同商品回归、1份漫剧正常回归；若出现具体失败，先诊断再决定有区分力的补验，不机械重发。0平台写/0媒体生成。旧会话重开、精确旧版本解析、新旧资源摘要及原数据库行对照都必须通过。

## 退出异常调查

内核在16:31:53记录APFS pagein读取共享内存offset16384失败，文件size=3；崩溃堆栈是walIndexRecover。当前固定SQLCipher源码unixLockSharedMemory只有获得DMS独占锁才按设计截短到3字节。应用protect_database_files在连接活跃时对db/wal/shm调用NSURL备份属性读回验证。

本轮普通空文件锁探针（无数据库、无mmap、无截短、无故障注入）确认：fcntl锁在setResourceValue后仍在，在getResourceValue后丢失。SQLite的[POSIX文件描述符说明](https://www.sqlite.org/howtocorrupt.html)解释同进程关闭任何同inode描述符会释放全部POSIX锁；[WAL文件说明](https://www.sqlite.org/walformat.html)说明共享索引和DMS协调机制。因此根因是Native元数据读回打开/关闭活跃文件，破坏SQLite持有的DMS锁，独立诊断连接随后可合法取得DMS并初始化索引，原映射仍被数据库线程访问。不是专家正文或退出checkpoint主动损坏文件。

修复保留0700目录/0600文件、安全删除、WAL/FULL/fsync和现有正常退出流程；备份排除在打开数据库前对整个专用chat目录设置和验证。活跃db/wal/shm只做路径级权限/元数据检查，不用Foundation重新打开文件。锁保持测试用普通scratch文件，正常SQLCipher提交/独立读连接/退出重开作回归；不通过制造SIGBUS验收。

本轮证据根：`yijie-desktop/.local/first-three-experts-repair-20261016/`；新停机备份与8份旧Runtime历史、80份已安装文件摘要已保存。18的失败结论不会覆盖，本记录单独填写修复后结果。

## 实际结果

本轮修复及受测范围复验完成：五个真实模型任务、事实保真核对、锁缺陷回归、正常退出、最终构建同版本重开和数据保留均通过。结构校验不替代模型质量，退出未崩溃也不替代锁缺陷的根因证据。

### 配置根因与来源闭合

原来失败的 repo 内工作区会继承 `.codex/config.toml` 中 Runtime 不接受的 `[workspace]`、`[rules]` 元数据。已将这些非 Runtime 配置改为说明注释，原安全要求仍由 AGENTS.md 执行；没有跳过严格解析、移除项目可信校验或修改固定 Runtime。隔离 `config/read` 正常成功并 EOF 退出0；本轮真实模型在此前失败的 `yijie-desktop/.local/first-three-experts-20261016/task-output` 工作区执行。旧失败任务原样保留，未重放其 outbox。

两个新包的本地使用授权单独记录于 Skills `docs/provenance/FEAT-158-first-three-local-use-authorization-v0.1.1.md`，明确引用当前用户修复/复验指令。旧版0.1.0授权文件原字节不变。最后一次元信息收口只更新两个0.1.1条目的授权引用及审阅时间；44份归档和6个精确ExpertRef均不变，模型实测内容仍为相同字节。元信息变更前候选独立保存在证据目录，不覆写模型实测构建回执；最终构建另记。

最终候选bundle为0.5.1，manifest SHA-256 `afada34e6aa816b4173c390b2a290fa16d8a5bf6b656949531f68e04b3c23847`，authority SHA-256 `a12cdbc4f290e7c66a156b18588e435f13b7da1c724f8cddef508bbb9bf7a059`。38普通技能+6个专家版本，目录仍为4位真实专家+7位展示专家，不含专家团。原42项元数据和归档保留；小红书/跨境0.1.1使用独立安装槽，原0.1.0仍可精确解析。

### 已完成的工程与界面检查

Skills最终lint、16项测试及45条合成eval格式检查通过（`skills-authorized.log`）；格式检查不计为模型质量通过。Host对最终候选的真实六版本资源生命周期、原39项升级保留、两个新旧版本共存与历史保护测试在race下通过（`host-authorized.log`）。Native锁保持、精确资源/目录、旧历史保护测试及Clippy已通过，具体最终日志保留在证据根目录。

Native界面已实际检查亮色/暗色的1180×760窗口、三列目录与专家详情，未发生文字/按钮遮挡，见 `experts-light-1180x760.jpg`、`experts-dark-1180x760.jpg`、`detail-dark-1180x760.jpg`；这些JPEG像素尺寸为2360×1520（2倍缩放）。系统外观已恢复Light、窗口恢复原尺寸。UI/launcher共95项、ESLint及设计文档build通过。Desktop旧不可变Host锁仍拒绝dirty来源，未削弱此门禁；本轮使用既有canonical本地候选校验，不声称全量`make lint`通过。

### 五次真实功能复验

全部从原生客户端选择/切换专家并发送，未直接向后端伪造提交。模型沿用Kimi-K3/max，权限为ask/on-request、workspace-write、网络关闭；同一会话 `01a144a5-cd51-75d3-a263-a5a2fd0faa46`，Runtime thread `01a144a5-cd7f-75e0-89a2-3654f47a1790`。Native停机只读结果确认5个submission accepted、5个turn completed、6条outbox done，attemptCount全部0；最终绑定漫剧0.1.0、revision2。共19次真实工具调用，退出码全部0；没有外部平台业务调用、媒体生成或额外模型补发。

| 用例 | 实际结果 | 时长/工具 |
| --- | --- | --- |
| 小红书原350ml咖啡杯 | PASS：5标题、封面、正文、10标签；不再包含清洁无死角、减少串味等无证效果；附事实对照和待确认项 | 242.927秒，4次真实资料读取 |
| 小红书A6/80张笔记本 | PASS：3标题、短正文、5标签；没有从尺寸/张数推出便携、不透墨、耐用等效果 | 86.606秒，明确复用本会话已读资料 |
| 跨境原350ml咖啡杯 | PASS：英文标题/3卖点、15秒分镜、7天排期；删除every corner、reduce residue/odor等无证主张，没有虚构利润、销量或认证；轻流未连接仍完成 | 260.749秒，6次真实资料读取 |
| 跨境100%棉圆领T恤 | PASS：英文标题/3卖点、10秒分镜；没有柔软、透气、不缩水、不起球、机洗或认证承诺 | 79.574秒，明确复用本会话已读资料 |
| 漫剧归还雨伞 | PASS：实际新建4镜20秒无对白JSON，2人物/2场景注册；实际运行安装包校验器并生成pass报告，独立重算逐字段一致 | 279.414秒，9次工具调用 |

事实保真由主任务逐项对照原合成输入和公开最终回答判定，不采纳模型自评。定位/叙事/渠道假设与产品性能区分，未把待确认清单当作正文免责。笔记本、T恤是新包示例之外的商品回归；同会话不同商品没有复用上一商品属性。20字标题为专家编辑目标而非本次用户硬性要求，不将此项计为严格格式达标。上述结论仅覆盖实际受测输入，不承诺所有未来生成都无误。

完整公开UI结果分别为 `01-xiaohongshu-cup.txt` 至 `05-comic-storyboard.txt`；人工核对为 `model-quality-review.json`。`runtime-functional-evidence.json`只取本次合成会话的公开工具命令、时间、退出码、权限和摘要，不包含思维链或凭据。`native-success-metadata.txt`为停机只读提交/绑定证据。漫剧产物在前述工作区的 `comic-storyboard.json`、`comic-validation.json`；`comic-functional-check.json`和`comic-independent-validation.json`为独立结果。校验器只验证结构、引用、ID、版本和时长，不冒充整部作品创作质量的自动认证。

### 退出与数据保留

2026-10-16 20:40通过原生Cmd+Q正常退出，canonical运行进程exit0，Host18081及Desktop进程均已消失，之后才打开只读SQLCipher/bbolt诊断连接。没有强杀、模拟崩溃、删WAL/SHM或修写旧库。`normal-exit.json`记录退出方式；根因验证另有普通空文件锁探针和实际保护函数的锁保持回归，不能只用“这次未崩溃”解释修复成立。

- SQLCipher67表的原865行全部存在：863行全字段逐字节一致；原 `chat_market_dispatch` 一行仅 `updated_at` 更新、`chat_projects` 一行仅 `last_used_at` 更新，均为正常查询/使用时间。原正文、提交状态、请求、专家引用未改变；当前1039行。详见 `sql-preservation-after.json`、`sql-row-field-diff.json`、`preservation-verdict.json`。
- Host原10会话全保留，新增1会话；4个旧会话仅 `updated_at` 因正常恢复变化。详见 `host-preservation-after.json`。
- 原8份Runtime历史文件逐字节一致，旧回合未重发；原80份安装文件中79份逐字节一致，唯一变化是正常安装操作日志 `.yijie-state/operations.v2.db`。所有旧专家内容与安装收据均保持。详见 `file-preservation-after.json`。
- 原0.1.0文案失败、早期配置失败及崩溃报告继续保留；本轮结果单列，不重写旧失败结论。

### 最终构建与重开

最终候选通过原canonical同步、freeze、`--packaged`构建；Native实际44项目录与精确引用两个测试在最终pin下通过（`native-authorized-catalog.log`），Host lint通过（`host-lint-authorized.log`）。构建回执为 `final-packaged-launch-receipt.json`，构建日志为 `canonical-build-authorized.log`；模型实测原回执 `packaged-launch-receipt.json`仍保留。两者仅授权元数据/pin收口不同，执行资源字节和ExpertRef一致，由 `authorization-final-preservation.json`证明。

最终构建恢复了本轮五个已完成结果及漫剧0.1.0绑定，同时打开原会话，原94/99/104秒三轮记录和跨境0.1.0绑定均保留，没有静默升版。目录仍11张卡，4位真实专家均显示资源已准备。证据为 `final-build-restored-five-turns.txt`、`final-build-old-v010-history.txt`、`final-build-catalog.txt`。

20:46再次Cmd+Q正常退出0（`final-normal-exit.json`），停机后再次对照原始备份，仍是原865行全在、仅2行时间字段变化，旧10个Host会话与8份Runtime历史、所有旧专家内容/回执保留。最终对照为 `sql-preservation-final.json`、`sql-row-field-diff-final.json`、`host-preservation-final.json`。随后仅运行canonical `--packaged --reopen`，日志明确 `Same-build expert reopen verified`，Host ready；五轮完成状态、漫剧绑定和空输入框再次恢复，发送按钮禁用，无新增模型回合。证据为 `reopen-final.log`、`same-build-reopen-five-turns.txt`。应用保留在此会话便于核对。

元仓manifest/governance lint、50项测试及Meta/Desktop shell语法检查通过；四个受影响仓库diff空白检查通过。原Runtime和Contracts未改，SQL35/Host10未变；没有commit/push、签名或发布。

### 原未通过项的处理

| 原问题 | 修复后结论 |
| --- | --- |
| A4小红书事实保真 | 0.1.1新资源与逐句主张约束；原输入和新商品实测均PASS |
| A6跨境营销效果推断 | 0.1.1新资源；原输入和新商品实测均PASS，未连接轻流仍完整交付 |
| A9指定工作区配置阻断 | 不兼容的repo配置元数据改为注释，严格config/read通过；同一原失败目录完成本轮5次真实任务，旧失败记录保留且未重发 |
| A10暗色/最小窗口 | 实际Native亮/暗1180×760目录及详情验收完成，已恢复原系统外观与窗口 |
| 退出SIGBUS | 已确认活跃文件元数据读回释放POSIX锁的缺陷及WAL失效机制，改为打开前目录排除；锁保持测试、完整真实任务后正常退出和最终构建退出/同构建重开通过 |

未执行强杀、崩溃故障注入、权限破坏、危险归档、攻击性fixture或运行时劫持。历史全量套件中包含这些路径的项目不运行，安全focused检查不冒充全量通过；没有主动制造SIGBUS来复现。未验证外部平台发布、实时热度、轻流接口或图片/视频生成，这些能力未新增。本轮为本地开发接入与修复验收，不构成生产/公开发布资格。
