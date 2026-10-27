# FEAT-164 D3一次日常维护与后态审计

2026-10-27。Owner明确批准复审63后执行一次D3，先核验新候选、完整备份、数据一致性和实例锁，完成后停止，不进入D4。**已执行恰好一次，Native正常返回SQL37→41并退出；后态核对通过，当前为D3_COMPLETE_STOPPED。没有启动日常App界面、Host、Runtime或计划worker，没有新增模型HTTP。**

## 1. 复审与实际授权

执行前重新核对63号与当前源码：已消费次数不等于未结清执行，Rust与D2 reader共用同一结清SQL；缺证明、未决状态、reservation仍拒绝。维护分支在auth、DatabaseWorker、sidecar和WebView前返回；使用同一全局App实例锁，先备份、检查第二副本，再重验原文件，最后调用既有正式迁移和repository打开/正常关闭。

沿用已批准的私有存储semantic边界，没有新增契约、schema实现或产品代码修改；Runtime核心/补丁、公共wire与下游pin不变。39/40新增操作/交付证明不回填历史，41退役只处理enabled/paused旧K3计划。本机6个计划已deleted，不会复活或重新授权。

本轮D3批准记录与当前preflight SHA、候选receipt、原Home及0模型额度形成0600私有绑定。一次许可已消费，不用于重跑或D4；无自动重试、自动回滚或恢复旧库。

## 2. 迁移前四项核验

| 项目 | 实际结果 |
|---|---|
| 新候选 | Desktop `841f7c71ed3549fe02a70cff608cbbae713d6808`、Host `a3d8767add3855a28c18adbbd51251fae3520ac0`；六来源HEAD/status不变；1216源码输入及119包内文件匹配 |
| 制品回执 | App SHA `4f7adcadc59db4a6e4cf23e700ebab5858b6ae9d953cd7401780d5778cab0f42`；receipt `0e6fe8191ffc027d4f1efedf14f7e8562ee1d876068aafa7386410202a2878a7`；canonical prepare-only --reopen通过 |
| 完整备份 | D2原17,389文件/476,337,115字节和sealed完整逐项匹配；manifest SHA `fd007b8bb8857ff1f903c703124328b1a6b65dcb15444a7280db36dc129b3449`，不只检查Native内部快照 |
| 一致性及锁 | 同一正常App锁下无项目进程/数据句柄；新inspection只读SQL37/68表，integrity/FK通过；未决执行、reservation、全模型未来/待恢复工作均0；6个已消费grant保留且全部结清 |

核验用独立副本，不对封存层连接数据库API。外层检查完成后正常释放flock，Native入口自行取得同一锁并再次检查、备份和核对源文件；没有绕过锁或让父进程持锁阻塞子进程。最终内部备份又与迁移前D2摘要逐项比对相同，证实这次交接未发生数据漂移。

## 3. 一次正式执行

从63号独立候选的Desktop目录、沿用同一构建环境执行：

```sh
bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-daily --migrate-daily-k3 --reopen
```

入口解析真实D3绑定、核对来源与同一回执；Native进程只接收维护所需最小环境，不接收Provider Key或workflow凭据。2026-10-27 12:35:58（Asia/Shanghai）命令退出0，返回`migrated_or_reopened`、`from_schema=37`、`to_schema=41`、`model_http=0`。内部备份ID为`01a17ba4-baff-78a0-8e36-6dc3aa81d14c`，保存在原Native目录的`kimi-k31-migration-backups`下。

未执行D4，未重开GUI、发送消息、继续旧线程、安装日常入口或派发计划。本轮未启停或重新核验workflow；63号的workflow运行/ready是其原时点事实，不能充作本轮D4前的新检查。

## 4. 后态审计

命令正常结束后重新取得全局锁，确认无项目进程/句柄，再创建新的完整后态sealed及独立inspection。后态17,397文件/530,142,694字节，manifest SHA `5c96a86c504cbc47a1526d25ad3c135c78d784875e43f9fd72eea49f92156c1f`。读取仅限inspection，封存层和原数据再次核对保持。

- Native为SQL41、71表，integrity正常、foreign_key_check为0。逐一对比68张旧表的旧列投影：**67张业务表全部旧行摘要相同**；仅`chat_schema_migrations`增加38—41四条，原37条完整保留。
- 三张新表`chat_model_operations_v2`、`chat_delivery_proofs`、`chat_plan_model_retirements`均为空，没有构造历史意图、取消证明或退役回执。
- 8条Native→Host→Runtime会话绑定保持，8条旧K3选择仍为原值/ready；3条旧K3计划模型历史、6个deleted计划、25份grant中的6份消费、7条run及全部回执/消费/退款事实均未改。
- 原outbox未决、selection非ready、reservation、活动/不确定turn、未结清grant、全模型未来/待恢复工作仍为0。旧K3身份保留是历史兼容要求；本轮只扩展存储，不自动切换线程或生成新授权。
- 原有文件中仅Native `chat/conversations.db`字节变化；新增项仅维护内部备份及其记录。没有删除原文件。原Host、Runtime、Provider Key的全部字节/mode/mtime保持，四份原Runtime WAL也保持。
- 内部备份原DB及两密钥逐项匹配D2迁移前摘要，内部result与进程输出一致；D2完整sealed不变。完整备份不是额外加密归档，继续由既有私有目录保护，原SQLCipher加密与秘密文件保持，不进Git。
- 新候选及六源保持；7份旧账本/快照与两份预占保持，累计真实HTTP仍13、本轮0。无强杀、故障注入、手工checkpoint、WAL删除/截断或二进制替换。

这是与实际执行分开的后态复核，不冒称独立人工评审、新一次全范围App E2E或D4验收。检查没有发现需要Runtime或产品修复的问题。

## 5. 停止点、回退与剩余范围

当前原日常Native已为SQL41，App/Host/Runtime均未启动。**不能直接用旧SQL37构建打开它，也不能把原DB单独覆盖回去。** 若未来需要回退，先明确批准范围与数据损失窗口，使用完整匹配数据组；本轮没有实施恢复、降schema或清理备份。

后续仍为单独批准的D4受限启动/历史检查/正常退出；进入时重新检查候选、后态摘要、实例锁、全模型可派发工作及真实workflow ready，Kimi保持暂停，不发模型请求。D5长期日常入口和production_hardened+local的G5/G6口径仍独立待收口，本轮不提前执行。G4/G5/G6保持pending；58已接受本地证据、never-sent安全替代、完整App正向取消NOT RUN及Owner排除项保持。

证据见`evidence/d3-migration-preflight.json`、`d3-migration-post-state.json`、`d3-migration-row-preservation.json`、`d3-migration-source-binding.json`和私有证据索引。完整原始日志、真实批准绑定、前后行摘要及副本位于`feat164-d3-migration-audit-20261027`；真实数据库、密钥和行内容不提交。

收尾治理：audit-claims、strict、S4 G3、元仓lint、53/53测试及7份Shell语法通过；diff检查通过。原8仓HEAD/分支/远端、500份既有dirty文件、混合memory原内容、7账本和旧b789制品/回执保持。最后一次同锁检查确认原日常仍匹配已验证后态，无活动项目进程/数据句柄。仅本轮治理/脱敏证据本地提交，不包含真实库/密钥或其它需求。
