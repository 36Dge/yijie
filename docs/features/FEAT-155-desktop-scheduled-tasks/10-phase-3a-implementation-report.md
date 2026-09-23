# FEAT-155 3A 实施报告

2026-09-18 · **3A 本地候选已实施，完成定向检查后停止。** 用户明确要求只实施执行契约、兼容读取、原生授权与共享预约基础。没有进入3B/3C或第四阶段；整体Must和D4仍未验收。

## 1. 本批结果

| 3A事项 | 实际完成 | 适用边界 |
|---|---|---|
| 最小执行契约 | 独立execution-v1源、Rust/TypeScript/schema投影、确定性生成/同步、严格schema lint及真实native输出conformance | 没有Host新接口、renderer command或Runtime变更 |
| 兼容读取 | catalog17；默认迁移目标15；正常合成15→16→17与重开/旧聊天；未知高版本拒绝；兼容reader扣住带定时标识的原outbox | 未迁移日常库；旧15/16 reader不能打开17；不代表兼容3B未来新格式 |
| 原生授权/额度 | 每次获取native authority，scope/read/manage/run分离；UI管理不续期旧context；grant绑定plan版本/定义/目标/authority/有限次数与期限；重试不续额 | 确认grant仍保持计划暂停；运行预检最终execution_not_ready |
| 共享预约 | 同worker事务内run/预约/扣额基础；前台四类提交、claim、dispatch读取和实际I/O前门禁；queued/inflight/运行/审批等待/unknown/删除处理中阻断 | 没有单独提交预约的生产入口、可投递定时outbox或自动触发器 |

**检查边界：** 本批定向检查通过；额外运行的Contracts通用`pnpm lint`未通过，原因及影响见§4。不声明全仓full-green、产品真实执行或发布资格。

## 2. 源码与职责

本批新增/修改29份Contracts/Desktop业务文件，逐文件SHA-256及相对第二阶段的变化见[来源记录](evidence/phase-3a-source-20260918.json)。全部为未提交local candidate，不是SDK发布pin。已有改动保留，没有新依赖或Cargo lock版本变化。

基线仍为：Contracts `db4458fe94572c4df41a114005d54a049bb79b1f`、Desktop `4a8a67bec4903624ca98a1098572fa26f3a20849`、Host `0e47766f494977c94bfea0e89cfbdf45a7fafa2b`、Runtime `6c1ad767f0997845b8258a1c452fd4eb7577579f`。branch/remote不变；Host前序候选和Runtime保持原样。

- Contracts唯一源：`jsonschema/scheduled-tasks/execution-v1.schema.json`。Identity引用已存在的计划存储定义，目录引用只含source/resource_id，不接收原始路径。旧恢复/草案/计划源不改；新族以leaf工具生成/同步并记录摘要。
- Desktop私有migration17增加grant/run/全局reservation，在**原chat_outbox**加scheduled_run_id，没有第二队列。migration1—16保持原字节；PlanWriter仍只主动迁到16，ExecutionFoundation是显式native候选选项，普通入口仍CompatibleReader/目标15。
- `schedules/execution.rs`承担授权管理服务、额度校验、运行读取及事务内预约primitive；`execution_guard.rs`承担兼容reader及前台/出站占用保护。复用原worker，不开第二writer。
- `NativeAuthRuntime::schedule_authority`只在既有exact local/demo_fast模式生成当前native authority，非本地模式拒绝；不改旧WebView capability投影，不持久化bearer，也不调用bind刷新UI context。
- 计划写管理复用旧存储逻辑但经当前UI授权和native scope校验；grant确认没有enabled或scope输入。新旧授权、计划编辑、过期、耗尽、目标移除、Auto/Full均在预检中按明确错误拒绝。已有Ask可接受；未绑定新聊天只返回native分配策略引用，没有创建工作目录。
- 预约写入helper没有生产服务调用者：它只在测试的正常临时事务中运行，不claim occurrence、不推进next-at、不创建会话/outbox。未来3B必须加入授权/生命周期/审批/时钟门禁及会话/outbox的组合事务后才可使用，不能单独提交成为调度器。
- 新run权限快照固定Ask，预约不读写前台draft_mode；未持有定时预约时原前台之间的并发保持。真正定时新聊天权限落库及受管目录绑定仍待3B，不能把本批快照检查当作已执行。

## 3. 实际检查

以下均正常运行，不含强杀、权限破坏、攻击fixture、系统时钟修改或二进制替换。

| 检查 | 命令/范围 | 结果 |
|---|---|---|
| 定向native | `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture` | 最终22/22 PASS：3A新增12项、前两阶段10项 |
| 旧聊天/迁移 | 下列6项各用`--lib <完整名称> -- --exact --nocapture` | 6/6 PASS |
| 旧UI授权 | `cargo test ... --lib chat::authorization::tests:: -- --nocapture` | 2/2 PASS |
| Rust静态 | `cargo fmt --manifest-path src-tauri/Cargo.toml --check`；`cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings` | PASS |
| 新契约源/派生 | `make scheduled-execution-check scheduled-execution-test` | 同源/确定性同步、每个定义的strict:true lint、4项schema测试PASS |
| 旧契约回归 | `node --test tests/scheduled-execution.test.mjs tests/scheduled-plan.test.mjs tests/scheduled-task-recovery.test.mjs`；各旧leaf source/check | 总13/13 PASS；旧生成物无漂移 |
| 实际producer | `check-scheduled-execution-producer.mjs <本次临时输出>`；旧`check-scheduled-plan-producer.mjs`同次输出 | PASS；新输出保留为[合成native证据](evidence/phase-3a-native-producer.json) |
| 契约兼容 | `bash scripts/check-breaking.sh <下列四个完整SHA>` | 四基线PASS，新族另做自身conformance |
| Desktop前端 | `pnpm lint`；`pnpm build`；`pnpm docs:build` | PASS；build保留既有>500KB chunk提示 |
| Contracts通用lint | `pnpm lint` | FAIL，详见§4；API部分通过并有12条既有unused-component提示，后续全链未完成 |

六项旧存储检查：

- `chat::migrations::tests::embedded_migrations_validate_and_write_checksum_ledger`
- `chat::migrations::tests::populated_v1_migrates_to_current_and_repeated_startup_is_idempotent`
- `chat::database::tests::reasoning_is_terminal_transactional_bounded_and_cascades_on_delete`
- `chat::database::tests::project_repository_is_scope_bound_and_remove_never_deletes_directory`
- `chat::database::tests::expired_outbox_lease_recovers_after_restart_without_creating_duplicate_rows`
- `chat::database::tests::public_task_host_identity_becomes_bound_only_after_normal_atomic_host_bind`

四个兼容基线：`db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。结构检查不证明实际Provider或私有库可降级。

## 4. 失败、修正及通用lint限制

1. 新测试首次编译把既有`DraftContentBlock::Text(String)`误写成结构体变体；按真实类型修正，后续编译通过。
2. 首轮运行暴露阶段二`schedule_readable`要求恰好schema16；已改为允许完整migration校验后的兼容扩展版本，默认目标仍15。正常合成future格式检查随catalog变为18，去掉旧测试里的固定17断言，没有改低版本SQL或校验账本。
3. 合成聊天准备起初漏掉既有public task绑定；按正常`bind_public_task`后再绑定Host身份。另一个claim用例用库打开前的参考秒查询，可能早于实际入队秒；改为在查询时读取当前秒，不改系统时钟或放宽断言。
4. clippy指出grant读取元组的类型复杂度；抽成私有类型别名后零警告。未关闭clippy规则。
5. 首次导出producer时，旧阶段二用例要求调用者先创建输出目录，因目录尚不存在失败；改用已创建的独立临时目录后，完整22项和两份actual-producer conformance通过。没有用手写JSON替代实际Rust输出。
6. 新族strictRequired lint要求条件分支显式声明required字段；源中添加对同一字段定义的引用，语义不变，再生成与同步。新族最终对所有定义保持`strict:true`，未关闭严格检查。
7. **Contracts通用lint仍未通过。** `scripts/validate-json-schemas.mjs`直接严格编译原始源，不认识定时族沿用的`x-family-version`注解；前序计划/草案还有该通用流程不支持的相对源引用/条件schema表达。未修改固定旧通用生成器、前序Host草案源或放宽通用lint来制造绿色。本批新增execution族用摘要校验后的标准投影完成严格lint；前两阶段继续用各自已登记的leaf检查。此限制阻止宣称Contracts全仓lint/默认流水线通过，进入整仓合并/发布前须专门收敛，不能继承本批定向PASS。

没有重跑历史全量Rust/Vitest/Contracts测试，它们包含用户禁止的故障/攻击fixture。使用上述已审查的正常定向集合；未执行范围不算PASS。固定旧consumer的全量`generate:check`本轮未重跑，前序需要干净不可变来源的条件未改变；本次三族leaf生成和同步实际执行，不把旧来源证据换算为新发布pin。

## 5. 分离自审与实际停点

代码和检查完成后，按权威源→native授权→worker→SQL事务→reader/claim→实际dispatch顺序复核。发现聊天删除开始时可取消queued/inflight turn的outbox，但Host清理仍未结束；已在共享预约查询中纳入删除job，并在出站时重新确认记录仍inflight、没有删除job。新增正常删除流程用例通过，未修改或扩建聊天删除引擎。

自审确认：schema15没有自动升级；writer关闭仍扣住定时记录；重复请求/事务回滚不多占额度；unknown/需处理不因超时自动释放；前台draft偏好保持；grant不是执行或工具批准；没有真实定时出站路径。这是Codex结构化自审，本轮没有使用子agent，不冒称独立人工批准。

尚未实施：3B组合会话/outbox、真实目录分配、Host恢复查询消费、原生审批观察、正常退出/STOP_PENDING/sleep-wake屏障；3C自动触发和草案模型接线；第四阶段页面/通知/防空闲睡眠开关。当前reservation只具有基础持久/互斥语义，没有可供生产调用的释放或独立claim入口；后续必须补实际执行事实闭环。

日常用户库/Keychain未访问或迁移；Desktop/Host/Runtime/Provider均未启动。模型 **0/12**，图片 **0**，商家/MCP业务 **0**。未提交、推送、发布或改变分支/远端。完成本批后停止，不自动进入3B。

收尾治理检查：元仓strict、D0、audit-claims、pnpm lint、50/50治理测试、逐文件Shell语法与差异检查实际PASS。前序52份业务文件44份未变、8份按3A范围更新；本批另有21份新文件，共29份。旧migration1—15与HEAD、16与阶段二证据逐字一致。此记录不改变Contracts通用lint FAIL或产品D4 NOT RUN。
