# FEAT-164 S4AF：日常切换最小方案与分阶段授权

2026-10-27。本轮只审计源码、58号证据和候选制品，落盘方案；**没有访问、枚举、hash、复制、连接或迁移真实日常数据，没有启动App或workflow，没有新增真实/本机模型HTTP**。不读取真实provider密钥，不修改产品、Runtime核心/补丁或来源锁。仅FEAT-164治理本地提交，不推送。

结论：先修正日常部署入口，再批准数据动作。现有日常候选仍具有prepare-only资格，**不能直接拿来切换日常库或启动**。58号已接受的隔离主路径与never-sent替代继续有效，完整App正向取消仍NOT RUN；本轮新发现日常Home连续性问题，当前G4重新置pending，等待最小修正和相关来源重资格。58的历史PASS不改写，也不以本轮只读审计冒称新的运行失败。

## 一、已确认事实、未知事实及冲突

只读复核58索引28个证据文件、六个干净产品来源、当前日常App119文件和1206个Desktop构建输入均一致。Desktop ea8763d、Host4f966e8、Contractsc5d1383、Runtime11fd/r5、Connectorscc56、Skills595未变化。当前日常App SHA `c29f7e07942038d4c3849ef3a711ed4b501d17daab1478329ba5de6b6321a4d0`，receipt `ee4c53922b9642ffa81c3d6356827df6e8dbdcf6c0ec582e108bc954d768add7`。这是旧合格prepare-only制品身份，不是下面修正后的未来执行制品。

| 编号 | 源码事实 | 后果与最小处理 |
|---|---|---|
| CUTOVER-01（P1，日常部署） | 普通入口Home在`<原Desktop>/.local/demo-fast/{host-home,codex-home}`；K31 daily入口284—288行改为`<候选Desktop>/.local/feat164-daily/{host-home,codex-home}`。Native仍使用`com.yijie.ai/demo-fast-v1/chat`，sidecar只在isolated分支改Home | 原Native会话可能指向新空Host/Runtime，线程映射和rollout不连续。不能仅迁Native库后直接启动；需制品位置与原数据Home分离、显式绑定 |
| CUTOVER-02（授权边界） | `migrate_target`先snapshot→副本preflight→原库写迁移→正式Repository open→计划退役。内部snapshot仅chat DB/WAL/SHM和两份本地secret | 没有独立只读预检CLI；不能以“先跑维护看看”为预检，也不能把该snapshot称完整多存储备份 |
| CUTOVER-03（部署/授权边界） | 正常daily launcher调用`workflow-up`；其停止态分支可移除停止容器、轮换epoch/凭据、启动依赖并运行Coze/API迁移。`workflow-status`也会record写state，且CLI不把false ready自动变成失败码。当前候选workspace缺Infra/Coze | 不得把up/status当纯只读检查；不能靠退出码或单端口证明ready。新daily启动必须只核验既有ready栈，不隐式补建、迁移或停启它 |
| CUTOVER-04（零调用边界） | App setup启动schedule检查，`automatic_startup_work`可因future或pending工作启动Host/Coordinator；K31暂停不屏蔽MiniMax | 无inflight不等于无自动请求。首次启动需检查全模型未来授权和未决计划工作；不靠“我不点发送”或只暂停Kimi保证零调用 |
| CUTOVER-05（写入边界） | Native维护不启动Host/Runtime；Host `OpenStore`使用写事务准备v2存储并清理过期receipt，Runtime启动准备受管文件，计划时钟可推进 | Native迁移与首次启动必须独立批准；第一次看历史也不是只读数据库动作 |

源码依据及逐文件SHA见`evidence/s4af-source-review.json`。关键位置：Desktop `scripts/run-local-demo-fast.sh:25/284/482/544/635`、`src-tauri/src/chat/sidecar.rs:835`、`isolated_model_migration.rs:172/233/270`、`chat/mod.rs:1016`、`schedules/automatic.rs:106`；Host `internal/session/store.go:158`；Infra `scripts/workflow-local.py:164/429/472`。以上为正常源码审计，没有制造故障或实际触发问题。

**仍未知且本轮不调查日常数据**：真正被使用的日常启动来源、Host/Runtime实际Home、Native schema/owner、unknown/outbox/grant/reservation、未来计划、受管配置前身、外置资源、可用空间及workflow当前运行状态。代码默认路径是候选线索，不是这些现场事实。原隔离R1的unknown/occupied记录不得推定存在于日常库。

## 二、推荐方案与取舍

推荐复用原日常三份权威存储：固定Native数据根＋经批准绑定的原Host Home＋原Runtime Home。制品留在新干净目录，原dirty工作区和已签名/旧App不覆盖。新增本地部署绑定记录把identity、原启动来源、两个Home、provider文件引用、Infra来源、候选receipt摘要及本次预检摘要连在一起；记录不含密钥或消息正文，不进入Git。缺失、漂移、根冲突或不匹配立即拒绝，不默认创建空Home。

另一个可行但不推荐的方向是完整克隆Host/Runtime后切换权威位置：需要额外处理绝对路径、workspace trust、rollout/MCP/资源绑定和双份可写状态，扩大复制、迁移和回退范围。本次不采用。把代码合入dirty原目录也不能解决`.local/demo-fast`→`.local/feat164-daily`的路径改变，并会混入其它需求；不作为部署捷径。

本轮contract-impact=none，仅文档与证据；整需求breaking不降级。下面D1若获批，增量为Desktop私有部署语义semantic，须按Contract First登记消费者与来源并重新资格；公共wire、Native command、数据库schema、Runtime核心/补丁不变，不改Infra实现。

## 三、先行最小代码修正范围（本轮不实施）

拟限定Desktop两个既有实现文件、一个新增支持脚本、一份对应测试和两份说明：

| 文件 | 拟变更及不得扩张的边界 |
|---|---|
| `scripts/run-local-demo-fast.sh` | 仅daily模式分离artifact root与原Host/Runtime数据Home；正常daily启动要求已批准绑定，禁止隐式新建/改权限/拷贝Home。daily正常启动改为existing-ready-only workflow核验；prepare-only/维护继续不启动服务。其它入口行为不改 |
| `scripts/kimi-k31-packaged-receipt.mjs` | 绑定新的daily部署策略/脚本来源；构建回执仍只记制品及编译输入。实际数据Home由独立受保护部署记录绑定，记录摘要纳入启动审计，不能把prepare-only回执当作数据迁移授权 |
| 新 `scripts/feat164-daily-deployment.py` | 校验精确daily identity、只读部署记录、既有canonical Home及授权摘要；无DB写入/自动修复。workflow只复用固定Infra源码的`read_state/all_containers/validate_owned/observed_ready`等已审只读逻辑，要求ready和epoch匹配，以明确非零退出拒绝失败；不得调用`record/status/up/init/build/render/credentials`或输出credential。使用`-B`避免向Infra写pycache |
| `scripts/run-local-demo-fast.test.mjs` | 正常合成目录与纯参数矩阵验证路径连续、无绑定不启动、prepare-only零业务副作用、workflow未ready拒绝而不up、维护不启动；无替身binary、故障/攻击fixture或权限破坏 |
| `docs/feat164-daily-deployment.md`、`SECURITY.md` | 明确新绑定策略、阶段权限、零调用先决条件、完整备份和回退限制 |

部署记录由后续D2基于现场事实生成，不从候选目录猜原Home；D1测试只用新合成目录。只读helper需限制目标在已确认原daily范围、校验owner/文件类型/规范路径；不能发展为任意数据目录覆盖器。workflow身份/镜像/epoch校验不得降为无鉴权HTTP探活。若现有只读函数的复用必须扩大到Infra修改或新增Native权限，先补具体差异方案，不在这份限定范围内直接实施。

D1完成后：来源/生成检查、入口与纯绑定测试、安全合成Home连续性/旧记录读取、旧隔离入口回归、独立canonical daily prepare-only及receipt复核。只生成新可复现制品，不覆盖c29f7e0或旧receipt。产品来源改变后的相关freshness重验；不继承58为新制品自动PASS，不新增真实模型调用，不运行实际日常或workflow栈。确认无开放P0/P1后才恢复G4。

## 四、执行顺序与每阶段授权

| 顺序 | 进入条件 | 允许动作 | 停止点/本轮状态 |
|---|---|---|---|
| D0 方案 | 本轮授权 | 源码/既有证据审计、方案、治理本地提交 | 已完成；没有日常数据访问 |
| D1 修正与离线资格 | 用户确认上节文件/私有部署权限范围 | 新隔离源码中最小修正、安全合成验证、prepare-only构建 | 未授权实施；不能读取实际日常库/凭据或启动服务 |
| D2 完整备份＋只读预检 | D1合格；用户批准明确目标根、原进程正常退出及备份/只读范围 | 下节完整冷备份、第二副本检查、形成绑定和实际NO-GO清单 | 未授权；不能迁移、启动App/Host/Runtime/workflow，不能改计划/grant |
| D3 一次Native维护 | 用户看到并接受D2具体结果、目标/备份hash、候选hash及写入范围 | 同canonical已绑定候选的显式daily维护、后态冷副本核验 | 未授权；成功也立即停在此，不自动启动App |
| D4 首次受限启动 | D3核对完成；用户批准原Host/Runtime首次写入及正常生命周期 | K31暂停、全模型无可派发工作、既有workflow只读ready，查看历史/目录/关闭计划，再正常退出和后态核验 | 未授权；0模型HTTP，不发消息、不切旧thread、不点恢复、不授新grant、不执行workflow |
| D5 日常入口启用 | 用户接受D4结果并确认启用范围 | 指向合格新canonical入口，按批准解除Kimi暂停；复核禁旧准入和原数据根连续 | 未授权；不覆盖旧/已签名App，不发验收消息。正式发布另行处理 |

不得将“同意方案”自行解释为D2—D5全部批准；每次批准以阶段和具体目标清单为准。D2→D3、D3→D4有可审阅实际结果作为后续批准输入。无需在本轮请求数据授权，用户已明确暂不执行。

### D2：完整冷备份与副本只读预检

1. 确认原日常启动入口及已知数据路径，用户停止新派发；有活动工作时只用App正常停止/退出。不能为本轮零调用要求启动旧App“检查”，不能强杀。锁屏时跳过需UI步骤并停在不可跨越的静止前置，不以锁屏为退出证据。
2. 正常退出后核验项目进程/句柄，按产品相同全局instance lock独占维护窗口。锁文件可能需要正常创建，属于明确的cache协调写，不称全文件系统零写；不删锁、不强解锁、不改原权限。无安全停止或不能取得锁即NO-GO。
3. 完整受保护冷备份覆盖`/Users/jack/Library/Application Support/com.yijie.ai`整棵App数据及经现场确认的原Host Home、原Runtime Home。包含所有DB/WAL/SHM组合、Host映射/receipt、Runtime rollout/config/catalog/writer marker、spool/附件/Artifact、受管Skills、授权与计划事实，以及原SQLCipher/HMAC和必需的provider文件引用对应本地secret。外置App自有资源须先列入批准清单；不擅自复制用户整个工程目录、Keychain或其它需求数据。
4. 备份在数据根外新建唯一私有目录，禁止覆盖既有备份、硬链接到原文件或把备份放进待递归复制根。保留文件字节及必要元数据/目录结构；DB保持SQLCipher密文，key仅在受限本地目录保留，不在命令参数/日志/Git输出。此方案不是“有独立密钥隔离的整包加密归档”，不能夸大。完成源→备份逐文件hash、清单及源前后稳定性核验；完整backup封存后不直接用数据库连接打开。
5. 从封存backup再复制inspection，使用已审SQLCipher/SQLite只读＋query_only及bbolt ReadOnly读取；Key只在私有进程内加载。SQLite只读仍可能更新SHM，因此inspection与封存层分离。不调用生产Repository::open、Host OpenStore、维护CLI、Runtime或任何`load_or_create`路径做预检。先审定reader脚本只接受该inspection根；旧57 reader路径硬编码R1审计根，不能原封不动拿来读日常。
6. 输出脱敏计数/字段hash：Native schema/完整性/FK/owner，Host版本/映射/操作回执，Runtime完整DB组合/rollout/受管前身，原配置/trust与资源连续性。Native只接受已资格的29/37/38—41；其他版本停止，不临时修改白名单。跨Native→Host→Runtime记录须逐层绑定，不能仅看一个库integrity就声称可迁。
7. 按产品预检核对pending/inflight outbox、非ready model selection、reservation、occupied_runs、uncertain/streaming/stopping turn、缺失/不可读/非终态native view及跨owner记录；同时扩展核对Host未决、未来自动计划和pending recovery。`occupied_runs>0`保持保守拒绝，即使看似终态也不清零/退款；unknown不猜为never-sent。普通查询不改变原operation和计划。
8. 零模型首次启动另要求所有模型均无可派发future/pending计划工作。暂停K31不是全模型闸门；若MiniMax/其它计划仍有效，停止并提出正常UI暂停的独立数据动作方案，不在本阶段执行、不改SQL。只读查询`scheduled_startup_needed`的等价条件，不能直接调用该生产函数，因为它包含expire/tick写入。
9. 备份大小/实际剩余容量、预检结果、原Home精确路径、源/制品/配置hash、权限、时间和有效期形成D2报告/部署绑定。任何未知项仍NO-GO；不能把查询失败当作计数0。维护窗口结束正常释放锁；若之后用户重开或有文件变化，D2证据失效，必须重新取稳定副本，不能继续用旧hash执行D3。

本轮未执行上述任何数据操作，也没有检查日常数据是否存在、可读或满足条件。未来完整备份不是模型fixture，不用真实内容测试新算法，不提交密钥/数据库/原始消息。

### D3：受控Native迁移及停止核验

使用D1重资格的新制品和D2实际绑定。执行前再次核对同一目标、全体数据摘要/无句柄及正常独占；有变化即停，不自动刷新许可。

现有维护参数形态为：`bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-daily --migrate-daily-k3 --reopen`。**这不是只读命令，本轮禁止执行；未来必须在D1新目录并携带其受审部署绑定，不能照此运行旧c29f7e0候选。** Native自己再次取得相同锁并预检。最小env不含provider/workflow凭据，返回早于auth、DatabaseWorker、Host、Runtime、worker、WebView。

允许写入仅固定日常Native根：新增内部迁移backup/inspection/result、正式schema链至41、旧K3计划退役暂停/新revision/撤有效授权及未来slot收敛。历史run/grant原事实不回填、不退款，原消息及operation不改。内部snapshot不能替代D2多存储backup。SQL38—41同样走正式open/退役，不能称完全无写。

成功receipt应为`migrated_or_reopened`、schema41、backup_id、model_http=0。随后保持App关闭，用新的完整后态副本对照原列值/PK/FK/nullable、原请求和授权事实及允许的迁移字段差异。Host/Runtime尚未启动，其数据须保持；不得写“所有表逐字完全不变”。失败保留result、原库和全部快照；一次失败即停止诊断，不自动重试/回写备份。

### D4：首次启动是第二次数据写入授权

此阶段授权应明确包含：原Host Store兼容升级及正常receipt保留期处理、原Runtime受管K31配置/catalog准备和正常SQLite/日志写入、Native启动代际/计划时间槽等正常生命周期变化，以及必要的本机鉴权只读ready请求。它不包括新增模型/商家调用或workflow数据库迁移。

启动前再次确认D2/D3绑定仍新鲜、全模型零可派发工作。保持`YIJIE_KIMI_K31_EXECUTION_PAUSED=true`作为Kimi额外保护，但不能取代全模型检查。沿原provider文件引用，不复制Key到新表单/前端，不用假key、网络断链或故障端点阻止请求。

完整daily UI仍保留workflow编译装配，新的入口只允许已存在且身份/epoch/镜像合格的ready栈。若缺Infra/Coze来源、凭据或ready服务，停止；**不调用workflow-up来补齐**，不静默设workflow=false绕过回执。需要启动workflow时，必须另列既有服务/容器与数据库迁移、完整数据保护范围，再授权；不夹带在FEAT-164聊天库迁移内。

允许观察模型目录、旧历史/附件、退役/关闭计划状态和本地readiness；不发消息、不生成标题、不点旧模型切换/恢复、不保存或启用计划、不运行workflow。正常退出后保留后态副本，核验原线程映射、历史、账本/预占、四Runtime数据库及WAL/句柄。观察到任何新模型调用即停止后续步骤、保留原事实，不以“未点击发送”否认调用。新unknown不改写成成功。

## 五、分界回退与失败处理

| 时间点 | 安全动作 |
|---|---|
| D1/D2或D3尚未进入业务数据写入 | 停止后续操作，保留原制品/数据及新backup；不需要恢复数据。不能在零调用范围内擅自重开旧App |
| D3已写或部分写 | 不启动旧Native writer、不降schema、不用旧DB覆盖现库；留在关闭状态，基于后态诊断。只有已验证的新兼容reader才可在另有授权下读取/修复 |
| D4已启动并写Host/Runtime | 先正常停止派发、退出全部受管进程，保留三个权威存储的最新组合；回退为合格新reader＋Kimi暂停，或保持关闭，不退回旧K3配置/二进制 |
| 无法安全退出 | 停止相关步骤并报告在途/句柄，不强杀、不重复启动、不手工checkpoint或删/截断WAL |
| 确需从backup恢复 | 单独设计数据损失范围、三存储一致点及副本恢复演练；取得新授权后再做。当前备份不等于允许自动restore |

不得通过清空unknown、清除occupied grant、重新生成operation、修改权限、删除WAL或替换可执行文件让预检“通过”。所有正常退出、清理和退役结果如实记录；旧账本与两份预占永远不能充作可回收额度。

## 六、门禁、验证与下一步

S1—S4已有本地来源证据、三项适用final及Owner接受的never-sent替代保留；完整App正向取消仍NOT RUN，不再补试，搜索质量与亮暗/键盘/最小窗口仍OWNER_EXCLUDED。59新增的daily路径P1是此前隔离验收未覆盖的部署缺口，当前G4 pending、implementation active、日常activation NO_GO；不是删掉58原始PASS或重复原模型验收。G5/G6与发布继续pending。

下一步最小动作是**只批准D1限定代码修正与安全离线资格**，仍不接触真实日常数据。D1合格后，再请求D2完整备份/副本预检；D2报告具备实际事实后才有可批准的D3/D4。不能现在预判日常schema、占用或workflow状态，也不能预批准所有后续写入。

本轮静态审计脚本PASS；治理包audit-claims/strict、S4 G3及元仓lint/53项测试/7份Shell语法实际结果见evidence/s4af-governance-checks.json。G4实际退出1，唯一错误为`gate G4 must be pass`，记录为EXPECTED_BLOCK，不列为新产品执行故障。验证不运行业务仓含禁止行为的全套测试。提交前已核验500份dirty（另混合memory）、7份账本/快照逐字保持；日常库完全未触碰，不以本轮无操作冒称重新验证其字节或状态。

证据索引：evidence/s4af-audit-index.json；私有工作区保护记录位于feat164-s4af-audit-20261027。全部仅本地提交、不推送。
