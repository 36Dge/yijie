# FEAT-155 3B-2 实施报告

2026-09-18。用户明确授权按[15执行方案](15-phase-3b-2-implementation-plan.md)实施3B-2。本批源码、兼容基础和安全定向验证完成，报告后停止；**定时双层禁发、普通入口目标15保持，未进入3C。真实macOS生命周期与Provider资格尚未验收，不能激活实际投递。**

## 1. 实际范围与来源

最高`contract-impact=breaking`，来自Desktop私有schema19及跨版本占用解释。共享recovery HTTP仍为0.1.0，原Go类型/schema、Host业务和Runtime未改；新增Rust consumer由原权威源同源生成，不手写恢复DTO。

开始前复核3B-1的81份候选摘要一致。五仓仍在`chore/retirement-baseline-20260905`，HEAD分别为：

| 仓库 | 完整HEAD | 本批变化 |
|---|---|---|
| yijie | `2f616f4d24c001812c6279a520ba69ea9875247e` | 本需求方案/授权、结果、证据和机器状态 |
| Contracts | `db4458fe94572c4df41a114005d54a049bb79b1f` | 6份：recovery leaf generator/sync/lock、Rust类型、实际producer checker与说明 |
| Desktop | `4a8a67bec4903624ca98a1098572fa26f3a20849` | 29份：生成消费、私有迁移、恢复/占用/生命周期、必要回归与文档 |
| Host | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` | 仅recovery candidate清单，handler/Store/正常shutdown不改 |
| Runtime | `6c1ad767f0997845b8258a1c452fd4eb7577579f` | clean，只读、不升级 |

完整候选摘要见[来源证据](evidence/phase-3b-2-source-20260918.json)，共96份业务候选，其中本批36份变化。以上HEAD不包含未提交候选，不能冒称已发布pin或生产兼容。旧1—18迁移逐字保持；原固定Runtime、legacy契约pin和通用generator不变。

## 2. 实现结果

| 项目 | 已实现行为 |
|---|---|
| 同源恢复类型 | 原leaf增加Rust闭合类型、canonical ID、缺失与null区别、条件字段及嵌套错误对象校验；Desktop与Host候选摘要同步 |
| schema19 | 独立记录create/turn尝试和代次、只读恢复来源、不可变释放证据及静止投影。旧18记录默认unknown；RecoveryFoundation只经显式native候选构造，普通目标15 |
| 两类GET | 受管healthz实例检查、owner bearer、no-store和有界读取；不要求Runtime ready，不猜task/session/operation/turn，不重投；当前响应nonce不覆盖历史来源 |
| 原生观察 | 同一Coordinator按原run关联恢复，accepted绑定后进入原native read/SSE；原生终态与scheduled结果/释放在同一事实事务提交；查询缺失/错误不制造终态，也不阻止已有精确绑定继续只读观察 |
| 审批 | 读取当前runtime_approvals；pending保守标需处理并保持预约；回调消失/批准/拒绝均不等于执行完成，不复用旧UI授权或退役v6审批 |
| 占用释放 | 精确终态释放；所有可能出站阶段的原受管代次正常结束且当前执行/审批无占用时，仅解除unknown的互斥，保留历史与已扣额度；完整never-sent取消才一次退款 |
| 查询与索引 | 保留旧active索引谓词，只排除有证据的scheduled静止行；同步busy/active/recovery/权限/interrupt/删除；旧create/start/interrupt不重发，不将unknown改写终态来解锁 |
| 正常退出 | 主窗口关闭/ExitRequested先拦截，保留窗口和唯一owner；Coordinator分离请求停止与等待，不abort进行中future；StopPending保留join/子进程身份和capture，正常退出后才清bridge/checkpoint/释放全部DB引用 |
| 睡眠恢复 | 主线程注册/注销NSWorkspace sleep/wake observer；共用epoch覆盖claim、await后的实际I/O与permission-turns，恢复沿原有界时间计算；未实现防空闲睡眠开关或系统通知 |

普通Chat提交/审批UI及唯一显示缓冲继续复用，没有第二套聊天状态机、outbox或业务数据库。native completed仅表示原生终态，不等于商家业务目标成功。对已静止unknown后来取得的精确原生终态，可以更新结果；解除占用本身不会生成此事实。

原active索引在migration14已扩展为“streaming/stopping，或非失败/取消的queued”；19保留该原谓词，未退回migration1的简单三状态条件。静止标记只由精确run/local turn/operation释放证据同事务派生，并由数据库约束保护。

`begin_conversation_dispatch`在原发送前检查并具备分阶段事实写入路径，但本批scheduled create/start会先被原guard拒绝，未激活任何投递。收到pending/uncertain回执本身也是已存在尝试的证据，不能继续享有never-sent退款资格。旧格式、未知来源、nonce变化、lease到期及用户承认unknown均不能单独释放。

macOS所需直接依赖只使用锁中既有`objc2-app-kit 0.3.2`、`block2 0.6.2`及最小Foundation features；Cargo.lock只增加Desktop的两个直接依赖条目，没有版本升级。平台监听仅观察系统事件，不强制睡眠、改时钟或创建OS守护进程。

回退必须保留支持19的reader并关闭writer/dispatch，不降级、删表或复制用户数据库。旧reader不能被声称支持19。Host正常shutdown复用现有实现；本批只以受管正常成功退出建立停止证据，异常退出继续StopPending，不强杀、不kill-on-drop、不forget句柄。

## 3. 实际验证与失败修正

所有检查使用普通临时SQLCipher/目录、声明的正常状态、进程内HTTP响应和项目标准构建。未运行真实App/Host/Runtime/Provider或访问日常库/Keychain。

| 检查 | 实际命令/范围 | 最终结果 |
|---|---|---|
| FEAT-155安全集合 | `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture` | **45/45 PASS**，本批新增14项，前序31项保持 |
| 旧链定向回归 | 15项exact迁移/聊天/权限/native SSE/正常关闭回归，加`chat::authorization::tests::`2项 | **17/17 PASS** |
| Rust静态 | `cargo fmt --manifest-path src-tauri/Cargo.toml --check`；`cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings` | PASS |
| recovery source | `node scripts/check-scheduled-task-recovery.mjs`、`sync-scheduled-task-recovery.mjs --check`及recovery测试文件 | 确定性、strict、双consumer同步及5项契约用例PASS |
| 实际Rust输出 | recovery/plan/execution checker检查本批4份producer文件 | 全部strict conformance PASS |
| Contracts整仓lint | `pnpm lint` | PASS；24份源schema，保留12条既有unused-component提示 |
| Host | `make scheduled-recovery-test && make lint` | 4项只读安全回归、race及静态检查PASS |
| 兼容基线 | `bash scripts/check-breaking.sh <完整SHA>`，沿12登记的四基线 | 四项全部PASS，不替代语义或实际平台证明 |
| Desktop | `pnpm lint && pnpm build && pnpm docs:build` | PASS；保留既有chunk大小提示，无UI源码变化 |

四基线为`db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。

本批14项新增检查覆盖：旧18→19→reader重开/普通15；never-sent一次退款；原native read事实同事务释放；unknown静止后同聊天新turn与legacy占用保持；旧interrupt拒发；删除不改写queued unknown；grant过期后仍可读取和身份冲突拒绝；两个GET在Runtime不ready条件下的消费、404、Rust严格字段；睡眠/时钟/换代屏障；permission-turns在readiness await期间遇到睡眠后不得POST；停止等待超时后join保留并正常完成。不是实际OS睡眠或真实模型执行证据。

失败与修正如实保留：

- 初次编译修正了ChatError枚举名、objc observer转换及旧测试新增参数/字段适配。
- 首轮迁移测试暴露目标白名单遗漏19，已补齐；后续合成恢复夹具缺少public-task原inflight事实，按真实约束补齐，未放宽约束。
- 全集合暴露旧3A测试跨秒时使用bind前时间claim新outbox，已改为bind后当前时间；业务时间/重试语义未改。
- 三项旧native回归仍以v7流/v1读取设置夹具，而当前源码早已使用v8/v2；修正路径、版本和响应header后通过，没有回退生产协议。
- 结构化自审补齐permission-turns的最后I/O屏障、异常退出不能提供正常停止证据、分阶段代次证据、重复释放，以及pending回执不得退款。补充旧中断/删除保护测试并复验；收尾复核排除已闭合旧run，避免恢复扫描重开历史，追加定向断言。

15项exact旧回归为14报告的8项，加`feat132_native_facts_survive_normal_reopen_and_cold_history_conflict`、`feat132_submission_failure_stays_local_and_allows_a_new_operation`、`finished_coordinator_handle_is_not_reported_as_running`、`app_exit_shutdown_clears_host_bridge_and_is_idempotent`、`feat132_open_native_stream_dispatches_interrupt_before_terminal`、`feat132_native_sse_commits_final_objects_without_legacy_body_reconciliation`、`feat132_coordinator_recovers_missing_cursor_from_confirmed_previous_host`。均核对实际运行了1项，未将0测试当PASS。

## 4. 未执行项目、影响与停点

| 未执行项目 | 原因与影响 |
|---|---|
| 真实macOS窗口退出、NSWorkspace sleep/wake及打包行为 | 已有canonical入口会装配真实Host/Runtime和常用数据/安全存储，本批未建立满足零调用、零日常库/Keychain访问的真实入口资格；不搭第二App或强制设备睡眠。**NOT RUN，阻断实际投递激活** |
| 真实Provider审批、三目标执行、重启恢复及实际进程退出链 | 本批保持禁发、零调用；合成终态和StopPending状态测试不能替代真实执行，继续NOT RUN |
| 自动触发、重跑、草案接线、页面、防空闲睡眠控制 | 留3C/第四阶段，本批未进入；系统通知按既有决定延期 |
| 历史全量攻击/故障fixture | 用户禁止强杀、可执行文件替换、权限破坏和攻击注入；只运行已审查安全集合，不声称全仓测试或D4通过 |

未迁移日常库、调用模型/图片/商家接口、提交/推送/发布或修改分支/远端。文本累计**0/12**，图片0、商家0。全部Must仍pending，整体FEAT仍in_progress，D4 NOT RUN。本批实施完成后停止；后续仅可另行制定3C方案，不能自动解除禁发。

本轮未使用子agent。技术自审不是独立人工批准。元仓strict、D0、audit-claims、lint、50/50治理测试、Shell语法、五仓diff、文档链接/空白与96份候选/4份producer/18份旧迁移摘要复核均PASS。D0仍只是既有产品设计批准。
