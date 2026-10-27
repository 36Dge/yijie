# FEAT-164 D1补证及D2完整备份/只读预检结果

2026-10-27。Owner明确批准复审61、补D1正向组合、准备D2工具并完成整个D2。本轮已执行完整冷备份、第二副本检查、跨存储映射与受管文件核对，以及既有workflow只读检查和失败归因。**D2检查完成，D3准入NO_GO：发现历史授权计数误拦截、未覆盖的已知旧catalog前身、Docker不可用三项阻塞。没有迁移日常库、启动App/Host/Runtime/Docker/workflow、清零授权或新增模型调用。**

## 1. 范围、来源和资格

本轮增量contract-impact=none：只增加测试/运维工具和说明，不改变产品协议、Native迁移谓词、Host受管准入、Runtime或共享治理。用户本轮直接确认涵盖备份/副本读取、必要本地secret保护及既有workflow只读依赖检查；不延伸D3—D5、服务启动或新核心修改。

工具在独立`feat164-d2-tools-20261027/yijie-desktop`从b789建立，只本地提交`b54ea00`，9文件：三份Python运维脚本、一份Go bbolt reader及测试、两份Python测试、SECURITY和daily说明。实际daily App仍是60号b789 / SHA944b6b2 / receipt490e35d；本轮没有构建新App，更没有把工具提交当作新App构建来源。原dirty仓、旧候选及回执不改。

| 检查 | 真实结果 |
|---|---|
| D1真实load_binding组合 | 7/7通过：正常私有binding→receipt/helper SHA→D3/D4/D5→原两Home；摘要/字段/暂停拒绝；原记录保持 |
| D2 Python工具 | 4/4通过，含完整两层冷拷贝、manifest绑定、正常Runtime SQLite/rollout、自然SQL29与37保留样例、workflow纯状态 |
| Host reader | 1/1 Go测试通过，正常bbolt副本ReadOnly/Check及前后字节保持；使用Host已锁定Go/bbolt，不加依赖 |
| 静态/文档 | Python AST、Go格式、Desktop lint和docs:build通过；原chunk体积警告保留 |

首次Python样例选了仅producer输出的目录，该目录没有secret，测试在读取检查副本的key路径前停止；改用已保留的完整正常迁移前快照后通过。首次Go默认工具链因关闭checksum数据库而拒绝自动选择工具链；改为已经缓存的精确Go1.26.5路径、GOTOOLCHAIN=local后通过，不联网安装。原失败日志保留，没有放宽产品准入。诊断catalog指令来源时一个临时只读解析器未排除Go注释，报KeyError；修正解析后只做字符串/hash比较，未执行源代码或改任何数据。

测试不重定向HOME、不制造权限故障、不替换可执行、不注入攻击fixture；没有运行含禁止行为的全仓业务suite。SQLCipher使用此前从项目正常构建归档得到且摘要匹配的审计库，SHA555cce3…，没有替换产品binary。

## 2. 完整冷备份

开始时没有活动易界App/Host/项目Runtime，无需启动或强行退出任何进程。取得产品同一个日常`com.yijie.ai.desktop.instance.lock`，核对无数据句柄；持锁串行完成备份、Native/Runtime/Host副本检查、workflow首次观察、源/封存层最终比对及句柄复核，然后正常释放。后续只读归因仍只打开inspection，不连接原库。

已确认原入口的canonical daily receipt及identity；Native→Host→Runtime的8条实际映射全部一致，证明下面两Home属于同一日常链，而非仅沿用默认路径猜测：

- 整棵`/Users/jack/Library/Application Support/com.yijie.ai`（含现存三个数据后缀及App Skills）。
- 原`yijie-desktop/.local/demo-fast/host-home`及`codex-home`整棵树。
- 原Host两份provider key文件；只在私有备份保存，不打印、不提交、不导出环境。

私有保留根：`feat164-d2-audit-20261027/cold-backup-01`。`sealed/`为不连接数据库的封存层，`inspection/`为独立第二副本；`source-manifest.json`及`manifest.json`记录路径、文件摘要和必要元数据。共**17,389个文件、476,337,115字节**，源→封存→检查副本首次一致，检查后原文件和封存层仍一致；备份在源树外、外层0700，不覆盖旧备份、不改源权限。SQLCipher原密文保留；rollout等保持原文件格式，因此不冒称整包独立加密归档。

Runtime四个WAL原大小分别为：goals 82,432、logs 4,260,112、memories 12,392、state 4,128,272字节。它们全部保留，连同DB/SHM一起复制；副本integrity通过，不执行手工checkpoint或删除/截断WAL，也不把旧Runtime正常停止后的非零WAL伪称r5 teardown失败。

唯一外部符号链接是Runtime临时arg0 wrapper指向既有项目构建的codex。链接原样备份，目标摘要已记录，未跟随执行或替换binary；它不属于新的权威数据根。原临时spool正常退出可能已清理，完整备份只承诺当时实际存在内容。原provider文件和SQL/HMAC秘密保留于私有层，所有公开证据只含脱敏计数/摘要。

## 3. 副本预检结果

| 项目 | 观察结果 |
|---|---|
| Native | SQL37，在已资格版本内；68表；integrity及FK通过；scope一致 |
| Host | Store10，8 sessions，全部idle/model ready；bbolt Check无错误，读前后字节一致 |
| Runtime | 四个SQLite integrity通过；8 threads及8条rollout都存在 |
| 三存储连续性 | 8 Native→8 Host→8 Runtime精确绑定，无缺失或错误映射 |
| 原操作/未决状态 | pending/inflight outbox、非ready selection、reservation、uncertain/active turn、缺失/不可读/非终态Native view均0 |
| 全模型自动工作 | enabled future计划的保守上界0，pending recovery0；不是只检查Kimi暂停 |
| 旧模型与计划 | 8个ready选择仍为K3；6个计划均deleted；3条历史plan model为K3，全部保留 |
| 维护准入 | occupied_runs>0的grant有6条，因此当前维护入口仍必定拒绝 |
| 受管文件 | 原配置TOML精确符合原Home；catalog不在当前两个精确前身中；2个project trust项与原config完整保留 |

预检只读取第二副本，用正常只读数据库API和固定查询；所有查询成功，未把缺表或读取失败转成零。未运行Repository::open、Host OpenStore、Runtime、维护CLI或任何load_or_create。生成的结果不授予线程选择、计划执行或D3权限。

## 4. 三项阻塞的本质原因

### D2-B01：把历史消耗额度等同于仍未结清的执行（D3阻塞）

6个grant均`occupied_runs=1/max_runs=1`，各自对应1个`terminal/completed`运行，`release_kind=native_terminal`、`refunded=0`，没有未释放记录或reservation。另1个正常never-sent取消的运行已按原规则退款。数据不是卡住的6个活动任务。

源码`src-tauri/src/chat/schedules/recovery.rs:294/306`表明：只有可信never-sent取消会减occupied；正常终态release清预约并保留已消费次数。维护`isolated_model_migration.rs:258`的无条件`occupied_runs>0`检查因此拒绝合法历史已消费记录。这是迁移准入谓词过于保守，不应“修数据”。

下一步最小方案应只审阅Desktop维护预检及对应测试：在逐grant/run/回执/预约事实可完整对账时，区分已结清消费与真实未决占用；保留非终态、缺proof、数量不符、unknown或reservation的拒绝。不清零、不退款、不改变旧run/grant。具体允许条件及自然正负样例先给Owner确认，未在本轮改实现或迁移。

### D2-B02：真实日常catalog含FEAT-163已存在指令，未进入FEAT-164冻结前身（D4阻塞）

与当前冻结`v1-current.json`的解析差异仅`models[0].base_instructions`；其余字段相同。该值精确匹配原dirty Host `runtime_permissions.go`的`permissionInstructions`，完整文件SHA及常量摘要已保存；不是凭猜测认作用户随意编辑。

当前候选Host `kimi_k31_activation.go`只允许两个旧catalog精确字节，`provider_authority.go`也执行精确匹配，所以真实启动仍会拒绝。**不能手改日常catalog或放宽为任意文本，也不能把FEAT-163整个dirty工作区混入FEAT-164。** 后续先固定这个真实旧producer/制品来源与具体字节，明确现有指令兼容范围；若确认增加精确前身，仅修改受管兼容白名单和定向验证，必要下游来源按Contract First更新。此处尚未授予该变更，也未承诺直接复制旧指令即可保持全部其它需求行为。

### D2-B03：workflow记录陈旧，Docker不可用（D4依赖阻塞）

首次真实只读检查在`all_containers`失败，原工具只返回固定安全错误。补充阶段/异常类型诊断后仅再观察一次：state仍为`phase=ready`，Docker读取抛WorkflowError。只读进程/本机socket归因显示无Docker进程，socket虽存在但connect返回`ECONNREFUSED`（61）。因此旧state文件不能证明当前ready；鉴权状态/editor GET尚未到达，真实就绪为UNVERIFIED。

两次失败原日志和私有state/双凭据字节不变证据保留；停止继续Docker命令重试。未执行workflow-up/status/record、轮换或数据库迁移，也未启动Docker。后续若要恢复依赖，须单独确认正常Docker/服务启动及workflow可能发生的迁移范围，不能把本轮“检查就绪”解释为“修复并启动”。

## 5. 下一步与本轮停止位置

当前判定为`D2_COMPLETE_WITH_BLOCKERS`，不是`D3_READY`。原执行日志里的`execution_complete=false`表示workflow检查子命令失败，保留该原始事实；完成归因和NO_GO清单后，D2调查本身已完成。数据库检查/备份成功不覆盖依赖失败，工具测试PASS也不覆盖真实数据拒绝。

推荐先并行概念审阅B01最小维护谓词、B02精确前身兼容和B03依赖恢复范围；实际修改/服务动作仍按明确范围批准，不因本报告自动实施。B01/B02修复若获批，先安全离线验证并固定必要新候选，再依据源数据是否变化重新确认备份/预检有效性；不能直接复用今天的摘要无限期授权迁移。没有证据需要新增Runtime核心/补丁。

其后才可能批准D3一次维护→D4受限启动/正常退出→G4/G5→D5正式启用/观察→G6。61的D5长期入口设计与local G5/G6规则冲突仍未解决，本轮不夹带共享门禁修改。58已接受S1—S4、never-sent替代及完整App正向取消NOT RUN保持；搜索质量和外观专项继续OWNER_EXCLUDED，不再补试。

全部原工作区改动、账本、两份预占及旧制品保持。累计真实HTTP仍13，本轮真实/本机模型HTTP均0；45元上限和原保守账本不改。数据与工具证据在私有`feat164-d2-audit-20261027`保留，Git只提交脱敏摘要、工具和治理。无App窗口、模型计量器或本轮启动服务需要交接。

完成后元仓audit-claims、strict、S4 G3、lint、53/53测试及7份Shell语法通过。再次取得正常App锁，确认全部日常源与封存层在归因后仍匹配；500份原dirty、混合memory原内容、7账本、b789的1207构建输入/119包内文件和receipt保持。最终reader增加manifest目录/摘要绑定后，正常副本组合测试及本次实际manifest校验均通过，没有重新打开原库。仅脱敏摘要与私有证据摘要进入Git。
