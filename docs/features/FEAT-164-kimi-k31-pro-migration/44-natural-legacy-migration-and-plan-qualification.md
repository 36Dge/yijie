# FEAT-164 S4Q：旧 K3 迁移、恢复取消与计划授权离线验收

2026-10-26，Asia/Shanghai。依据 Owner 本轮授权审计43号与实际实现，优先推进S2，再推进S3；仅本地提交，真实模型HTTP新增0。整项仍IN_PROGRESS。

## 复审结论与范围

43号的provider-only根因、launcher五行修复及两次r5 App只读正常退出结论保持。本轮验证前核对7仓branch/HEAD/remote、497份原dirty和7838份受保护文件；不复跑错误启动组合。当前可复用App仍为S4P独立canonical构建，119个bundle文件逐一核验保持。

发现的证据缺口：原S2 Native/Host边界从MiniMax开始，旧K3图验证未覆盖本轮“当前r5内已加载旧身份→实际Host切换→正常取消→恢复”；原S3主要使用直接历史格式fixture。预先复审采用正常旧Runtime历史producer及默认旧模型模式的真实计划API producer；不改库制造旧身份或unknown，不改日常数据，不把模型选择当业务授权。

增量`contract-impact=none`：只增加opt-in测试、测试helper和离线driver；无产品实现、公共wire、SQL迁移、权限或Runtime补丁改变。完整FEAT-164的breaking分类不变。Host产品来源894671b、Desktop产品来源b6f0ad7、Contracts5b5dad、Runtime11fd/r5均保持；测试提交单独记录，不要求无产品变化的下游重新pin或覆盖App。

## S2：已加载旧线程迁移与正常恢复取消

新增Host `TestFEAT164LoadedLegacyMigrationResumeCancel`，使用保留的canonical旧web-sources Runtime与r5；两个provider进程级和线程级均为loopback，dummy凭据、重试0，并读取实际配置核对。没有外部转发能力。

1. 旧Runtime通过正常thread/start和turn/start生成完成的K3合成历史，确认thread仍loaded，正常Shutdown后切换代次。
2. r5用stable原生resume加载同一个旧K3身份用于历史观察，不发送旧turn；确认loaded且本机HTTP计数未增加。该原生历史准备不是产品Host对旧模型的新执行准入。
3. 调用实际Host `SwitchThread` 的状态/审批检查、unsubscribe、resume流程；同一thread确认K3.1 Pro/max，正常完成新回合。
4. 下一轮普通有限SSE正在处理时调用原生正常interrupt；观察interrupted。合成响应自然结束后正常退出、重启，原旧/新历史及interrupted保留，读取没有补发；显式同thread恢复后新回合完成。
5. cutoff后全部HTTP均为kimi-k3.1-pro/max。最终Runtime四库WAL字节0；保留完整home副本，只读integrity_check四库均ok。没有手工checkpoint、删截WAL或强杀。

首次运行原生步骤满足断言，但fixture等待远端连接关闭30秒，而HTTP正常Shutdown只等15秒，整项真实FAIL。错误假设是把native interrupted等同服务端HTTP断开。复审后只把fixture改为正常1秒有限响应，并等待handler结束；原生/身份/历史断言不降级。修正运行race PASS、正常服务关闭PASS；首次失败及root仍保留。不能用这一结果推定真实供应商取消计费或连接一定立即断开。

本轮S2两次各4次loopback，共8次；每次1旧K3、3新K3.1，真实模型0。旧真实账本不记入这些合成usage。详细证据见`s4q-s2-first-result`、`s4q-s2-first-run-rca`、`s4q-s2-corrected-result`及`s4q-s2-retained-state-audit`。

此处通过的是实际Host Manager/Runtime生命周期子集，不冒称Desktop SQL/Host Store/原生UI全链旧线程迁移已通过。

## S3：自然旧计划与当前领域链路

两份新建、保留的SQLCipher fixture均由当前默认非candidate构建的真实Repository/计划API生成SQL29：K3暂停计划及旧grant、K3启用计划、MiniMax启用对照；第二份另有正常prepare形成的旧K3未发送run及occupied=1。没有直接INSERT/UPDATE历史model、授权、snapshot或unknown。

第一次直接以candidate正常open旧SQL29，真实FAIL为`OrchestrationUnavailable`，发生在migration之前；拒绝后所有fixture文件逐字保持。源码database.rs仅接纳空库及38/39/40/41，这是22号明确保留的旧库入口门禁，不是计划退役算法失败，也不是Runtime问题。当前App没有旧K3记录还不足以解释整个缺口：**产品旧库准入本身仍未开放**。

不删除此门禁。单列测试`expand`阶段：默认兼容reader仅对自己的合成库调用已有权威`migrations::migrate_to_target(38)`，原身份和事实不改；随后candidate实际open完成38→41并在worker可见前执行正常退役。此显式测试迁移不能作为App旧库准入已通过的证据。

最终driver五个精确阶段、0skip通过：produce → admission（明确拒绝且源库不变）→ expand → upgrade → reopen。实际证明：

- 两个旧K3计划各仅增加一次revision，保留原model/definition，暂停并清空有效授权和next_at；MiniMax计划逐字段相同。
- 旧grant重放stale，新执行拒绝，旧出站不可claim；旧held run/grant/snapshot/outbox/reservation等14行事实保持，occupied仍1，没有退款或换grant。
- 未占用的旧计划显式选择K3.1并保存后仍paused、无有效授权；独立确认产生新grant和新definition digest。新prepare冻结K3.1；正常never-sent取消一次退款，重复取消无变化。
- 正常drop/reopen保持计划、旧事实、新回执和取消结果，退役收据各2条，不重复退役。

四份完整快照仅只读检查，integrity均ok；每份原29条migration ledger在41中逐行保持。review旧6行事实全部保持，只增加1个新grant/新run；held旧14行事实全部保持，grant/run数量不变。`s4q-s3-sql-preservation`提供摘要，private完整数据库不提交。

重现命令：在本轮Desktop资格树执行`python3 scripts/feat164-natural-plans.py --output <新的绝对证据目录>`。driver仅继承工具链基础环境、离线依赖和显式本机开关，不继承模型凭据；不启动App/Host/Runtime，也不访问模型。本轮生产模式准入、人工WebView重新审阅与授权UI仍NOT RUN，不以领域通过替代。

## 实现后审查、提交与限制

Host测试提交`d49c005f8e533e1251179bb2319f6e3e2ec2db08`，仅2个测试文件；Desktop测试提交`fd0c575e4465dea6bb72ec9681248f664000551b`，仅test模块注册、新测试和driver共3文件。均从干净资格树仅本地提交，再ff到原分支；原dirty不入index。验证时原HEAD/status如实保留，最终Git对象与测试字节hash绑定见`s4q-source-binding`，不伪称提交后重跑。

Go race与vet、Rust fmt、产品lib Clippy通过。首次test Clippy发现本轮三处常量断言写法及既有排布错误；本轮三处已修正，并以修正后字节重新跑完整五阶段通过。严格`--tests -D warnings`仍仅被既有`native_conversation_storage.rs:46`的`items_after_test_module`阻断，没有压制warning或改无关源码。全仓测试、完整Runtime make test和远端CI没有因此成为PASS。原有Runtime执行位限制继续按42号保留。

没有启动或操作App；当前S4P产物、日常/候选数据、旧账本和14.188544元预占保持。真实次数5/5已用尽、30元cap与14.679001元保守累计均不变；无push/tag/release/日常cutover。无新Runtime/core/patch范围需要批准。

## 下一步最小方案与停止条件

1. 优先收口旧**隔离**库准入，不能直接删除database.rs的版本白名单，也不能把测试expand接到所有启动路径。先明确canonical候选身份、唯一数据根、正常静止/旧工作收敛、reader/ledger兼容与回退证据；普通日常根继续拒绝。将这一入口的具体差异与授权边界作为下一项实施审查。
2. 通过真实入口后，再把自然旧会话/计划带入同源App，补S2 SQL/Host/Runtime/UI显式选择恢复及never-sent取消、S3表单重新审阅/独立授权；保留旧请求与占用，不能以复制原始SQL或篡改版本绕过准入。
3. S4/TCONF04、当前来源全部final及日常切换仍独立未完成。r5真实G2V未新增，旧r4真实结果不自动继承。后续核心/补丁如确需变化先另报方案；真实HTTP仍0许可。

停止条件：旧库身份/来源/静止状态不明、现有unknown/占用无法安全解释、正常退出未完成、或需要扩大Runtime/数据写入范围，停止依赖步骤并保留证据。当前无需重复8次loopback或旧141项来替代准入缺项。

最终治理claims/strict/manifest及Contract First规则、元仓53项测试、7份Shell语法通过。原497份dirty和7838份受保护文件逐一保持，现有App119文件保持；原分支/远端不变、无残留候选服务。此文档检查不晋升S2/S3/G3或全项状态。完整原始日志、测试及诊断源码定位与SHA见`s4q-audit-index.json`；秘密/数据库副本不入Git。
