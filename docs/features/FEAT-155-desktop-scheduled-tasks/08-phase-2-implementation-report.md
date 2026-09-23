# FEAT-155 第二阶段实施报告

2026-09-18：用户已明确要求按07四步实施。第二阶段本地计划、时间与存储兼容基础完成，定向检查通过；停在第二阶段。第三阶段未开始，整体十项Must与D4仍未验收。

## 1. 实际结果

| 步骤 | 已实现及证据边界 |
|---|---|
| 时间验证 | 锁定rrule0.14.0、chrono0.4.45、chrono-tz0.10.4/TZDB2025b；统一native evaluator覆盖一次/每日/工作日/每周、IANA时区、DST fold/gap、闰日及远期参考日。只计算，不启动timer |
| 最小契约 | 独立scheduled-plan v0.1.0源；引用第一阶段草案时间/目标定义，生成Rust/TS/schema和候选摘要；实际Rust输出通过同源schema校验 |
| 兼容基础 | 普通迁移目标15与可读上限16分离；完整ledger预检；显式PlanWriter仅用于正常合成临时库。15→16、正常重开、关闭writer后读取与原聊天操作通过；未知未来格式拒绝 |
| 计划存储 | 同一SQLCipher/worker保存scoped计划、request去重与occurrence；revision冲突、规则epoch、正常恢复时间推进、目标删除保护均通过。无run/session/outbox组合或真实投递 |

新建/编辑只保存paused，授权引用为空；next_at仅是候选日历预览。恢复跨越暂停时间时记skipped_paused，不虚称授权任务漏执行或业务失败。相同确认返回当前计划事实，不再次修改；计划删除后旧确认不能复活。删除计划不删聊天；删除被引用聊天同事务清除绑定、暂停计划、撤销本地候选时刻，其他“每次新聊天”计划不受影响。

## 2. 变更与来源

本阶段最高contract-impact=**breaking**，原因是私有SQLCipher16与旧schema15 binary不兼容；新增共享结构本身为additive。旧HTTP/Runtime/权限语义没有改变。Owner仍为段成威；这是本地实现与Codex自审，不冒充独立人工验收。

- Contracts：`jsonschema/scheduled-tasks/plan-storage-v1.schema.json`、独立generate/check/sync、4项schema测试、native producer校验、Rust/TS/schema生成物和candidate manifest。原草案、第一阶段Host查询源及旧通用generator/package保持。
- Desktop：`src-tauri/src/chat/schedules/`领域、时间、存储、生成类型及测试；migration16；现有database/worker薄适配；Cargo精确锁与兼容说明。Rust类型参与本阶段native服务，TS投影待后续页面消费；未注册Tauri command或新capability。
- 元仓：授权、07结果、当前状态、本报告及来源/合成producer证据。
- Host/Codex/Skills：本阶段没有业务修改。Host第一阶段现存候选逐项保持；Runtime clean，未更新或替换制品。

起点HEAD：Desktop `4a8a67bec4903624ca98a1098572fa26f3a20849`，Contracts `db4458fe94572c4df41a114005d54a049bb79b1f`，Host `0e47766f494977c94bfea0e89cfbdf45a7fafa2b`，Runtime `6c1ad767f0997845b8258a1c452fd4eb7577579f`，元仓 `2f616f4d24c001812c6279a520ba69ea9875247e`。HEAD仅是基线，不是包含本轮改动的提交。

[源证据](evidence/phase-2-source-20260918.json)记录28个本阶段新增/变更文件及继承的第一阶段文件摘要。第一阶段supported-baselines文档追加阶段二说明；原阶段证据保留历史含义，不回写旧hash。正式Cargo.lock只新增chrono-tz、rrule及phf/phf_shared0.12.1，所有原包name/version组合保留，没有全量升级。

## 3. 时间与兼容的准确含义

时间库先在仓库外正常临时crate中验证，再进入项目。RRULE仅生成受限日历日期，chrono-tz解析当地时间：fold选较早UTC、gap跳过（一次计划的gap拒绝）。生成起点取本次参考日，而非计划创建日期；最多16个候选，调用有验证限制的all，不用all_unchecked。依赖源码、锁校验和与2025b时区数据身份已记录；不宣称未来TZDB升级无需再验证。

60秒连续awake容忍及恢复/时钟跳变不补跑为纯函数结果；真实sleep/wake信号、预约、成本计数与投递仍留第三阶段。恢复账本一次记录有界跨过区间，不为多年离线生成逐次run，也不重复消耗回拨时钟之前的逻辑槽。

默认`LATEST_SCHEMA_VERSION=15`保留原公开的已激活默认版本含义；新`MAX_READABLE_SCHEMA_VERSION=16`只表示候选reader理解范围。正常入口不会因为catalog增加16而迁移日常库；显式native PlanWriter才允许前向16。已有16由CompatibleReader完整核验后保持16，正常聊天写入/删除仍受保护；CompatibleReader不是物理只读连接，也不是旧binary。

1—15 migration原SQL/hash不改。未知版本/ledger在WAL配置与启动清理之前预检。本阶段临时SQLCipher前向验证与内存未来格式测试使用正常migration工具；不覆盖真实日常升级或第三阶段未来run/outbox格式。原15 binary不能回退写16，禁止down migration/删库/重置；实际激活日常writer前须再确认可恢复兼容候选与对应新格式。

## 4. 实际检查

| 检查 | 结果 |
|---|---|
| 临时时间库探针 | PASS；2个测试，内部覆盖8组日历边界、once fold/gap和无效时区；不代替项目测试 |
| 独立Contracts generate/check/sync | PASS；可再生、源摘要及Desktop复制逐字节一致 |
| `node --test tests/scheduled-plan.test.mjs tests/scheduled-task-recovery.test.mjs` | 9/9 PASS，含4项新增及5项第一阶段回归 |
| 当前Rust producer→源schema | PASS；见[普通合成输出](evidence/phase-2-native-producer.json)，内容不来自用户数据 |
| `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture` | 10/10 PASS；实际SQLCipher保存/重开/并发/去重/目标删除、版本边界、时间与输出；最终修正后完整复验 |
| 4项旧存储/迁移测试 | PASS，精确名单见下；两个新增强化断言同时复验通过 |
| `cargo fmt --manifest-path src-tauri/Cargo.toml --check` | PASS |
| `cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings` | PASS，最终修正后复验 |
| `pnpm lint` / `pnpm build` / `pnpm docs:build` | 全部PASS；build仅有既有大chunk提示，未为此改页面或打包策略 |
| 旧consumer `pnpm generate:check` | 固定来源稀疏检出下PASS，见下一节；原dirty sibling直接运行未通过，不能混淆 |
| 四个Contracts breaking基线 | 均PASS：当前fallback、已发布支持、native-v1、native-v2 |
| 元仓strict/D0/声明审计/lint/测试/Shell及diff | PASS，治理测试50/50；结果见02末尾，不代表产品D4 |

4项旧回归精确测试名：

- `chat::migrations::tests::embedded_migrations_validate_and_write_checksum_ledger`
- `chat::migrations::tests::populated_v1_migrates_to_current_and_repeated_startup_is_idempotent`
- `chat::database::tests::reasoning_is_terminal_transactional_bounded_and_cascades_on_delete`
- `chat::database::tests::project_repository_is_scope_bound_and_remove_never_deletes_directory`

命令为`cargo test --manifest-path src-tauri/Cargo.toml --locked --lib -- --exact <上述全名> --nocapture`；同时选入两项新增测试`feat155_storage_request_replay_revision_epoch_and_no_execution`和`feat155_storage_scoped_targets_and_compatible_deletion`的完整模块名，实际运行6项并全部通过。没有运行相邻权限破坏/损坏/攻击fixture。

兼容命令`bash scripts/check-breaking.sh <SHA>`逐一检查：`db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。新增族在这些基线不存在，另用本族conformance验证；旧族未改。结构检查不能替代私有存储及产品执行验证。

## 5. 失败、修正及来源检查说明

1. 临时时间探针首次编译失败：rrule::Tz没有FromStr。核对实际源码后使用直接锁定的chrono-tz做IANA解析/转换，RRULE负责日期选择；复验通过。临时探针曾有unused警告，不继承到正式候选；项目两处未用import清理后，最终clippy零警告。
2. 原工作区直接`pnpm generate:check`因Contracts已有tracked改动停止；没有删除改动、提交或关闭门禁。临时detached worktree初始no-checkout索引尚未装载，第二次也停在clean检查；用正常sparse/read-tree完成索引后发现Skills当前HEAD不同于既有固定pin，再为该准确pin建立稀疏来源。每次依据不同实证修正，没有机械重试或伪造通过。
3. 最终使用原检查器既有环境参数：Contracts与Host取上述基线的临时clean Git来源，Skills取固定`10c45bec29603b002e861e1499d5b4e684251af5`。它们仍按每个lock从真实Git对象核验不同历史版本；只物化AGENTS.md与.git指针，未检出危险归档、fixture或二进制。原工作区branch/HEAD/remote和业务文件未改变；三个临时worktree检查后正常remove，没有force。新阶段二candidate仍由独立source/digest检查验证，不能把历史pin检查称为新SDK发布。
4. 与实现分离的自审发现暂停计划的跨过区间不应命名为missed_offline；已改为skipped_paused，正常enabled语义的纯时间判断保持，10项测试和clippy复验通过。还补充“非时间编辑同槽不增记录”与“删计划保留真实合成聊天”的断言。没有扩展第三阶段执行能力。
5. 收尾复核发现serde默认Option解码会接受显式null，而源契约只允许字段省略。已在唯一源generator加入optional_non_null派生逻辑，防止null编辑身份被解释成新建；补充Rust/JSON Schema拒绝用例。重新生成、同步、9项契约测试、10项native、fmt和clippy均复验通过，没有手改生成类型。

## 6. 自审与未执行项

再次核对源→生成类型→native校验→scope/revision事务→SQL约束→兼容reader/删除→单worker调用链，未发现本阶段剩余阻断：

- schema15普通启动不升级，16不降级；完整ledger与未知版本边界有效。
- 时间计算使用成熟库且查询从当前参考日有界开始；fold不会产生第二逻辑槽。
- 同request不重复创建、不重放旧编辑或复活删除；时间编辑与回拨不能重开过去槽。
- 原有聊天删除与计划失效同事务；计划删除不删除聊天；没有第二writer/outbox。
- 原生输入/错误不授予scope或grant，三个目标仅存意图/已有引用；没有注册renderer入口或提供开启接口。

这是Codex结构化自审，不是独立人工审查。没有实际调度、原生执行、审批观察、Host恢复查询消费、受管工作目录创建、真实睡眠/唤醒、UI、通知、日常库迁移或最终D4。完整Rust/Vitest/Contracts历史全量测试含用户禁止的故障/攻击fixture，本轮不运行，采用已审查定向集合；不得写成全仓测试通过。

## 7. 停点与额度

第二阶段完成后停止，未进入第三阶段。后续须把native授权/预算、sleep/wake屏障、前后台预约、run/session/outbox组合事务、Host恢复及正常退出作为第三阶段完整执行闭环处理；本轮未开始这些工作。

模型验收 **0/12**，图片 **0**，商家接口 **0**。没有启动真实Desktop/Host/Runtime/Provider，没有访问/复制用户日常数据库或Keychain，未提交、推送、发布，也未改分支/远端。只有项目标准工具生成的临时/开发构建产物，没有替换用户提供或受审计二进制。
