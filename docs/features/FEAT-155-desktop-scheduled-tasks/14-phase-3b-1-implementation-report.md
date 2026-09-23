# FEAT-155 3B-1 实施报告

2026-09-18。按用户明确授权实施[13方案](13-phase-3b-1-implementation-plan.md)，完成本地目标、目录与手动组合事务后停止；**未进入3B-2或3C，定时记录仍禁止出站**。本批是本地准备基础，不是运行已受理、真实执行、恢复或D4通过。

## 1. 实际完成

| 事项 | 已实现 | 边界 |
|---|---|---|
| 稳定授权目标与实际绑定 | 专属绑定独立存储，不回填definition或改grant摘要；existing_chat按实际workspace来源核权 | 原grant重开仍有效；真实修改定义仍需重新确认 |
| schema18兼容 | 原project增加来源分支；新增专属/run关联；1—17保持；正常合成库15→17→18、重开/旧聊天/旧grant检查 | 普通入口仍目标15；LocalPreparation未被App/renderer选择，17 reader不能回退读18 |
| 原生受管目录 | 本库目录下按scope及稳定资源ID准备；专属复用、每次新聊独立、已有沿原目录；managed无用户书签 | 文件系统准备不冒称SQL原子；失败无run/outbox；未绑定目录可重用，无后台清理 |
| 手动组合事务 | 同worker内去重、授权重验、预约、run、原conversation/message/turn/v2 outbox、绑定及一次额度占用 | manual不推进next_at/cursor/自动occurrence；没有automatic/rerun producer |
| 关联与禁发保护 | 在途删除拒绝；终态合成关联删除后失效/墓碑；create及后续start保留scheduled标识 | claim与实际dispatch仍拒绝；check_run仍execution_not_ready，无强制释放接口 |

最高`contract-impact=breaking`，影响为Desktop私有持久格式和workspace/准备语义；共享wire形状、源契约、生成类型及consumer来源清单不变。Host/Runtime/API/Infra不修改，没有新增依赖、Tauri command/capability或第二队列。

## 2. 实现与兼容决策

- `0018_scheduled_local_preparation.sql`保留原project/session关联和scope索引，旧项目默认user_project及原书签；managed_schedule明确使用native资源ID且bookmark为空。普通项目列表、注册/刷新/置顶/移除/书签入口拒绝managed，原聊天查询仍保留关联。
- `schedules/workspace.rs`负责格式感知引用、scope内稳定资源ID、受管目录准备/解析及删除保护。已有受管资源缺失时拒绝，不重建已经绑定的目录；新目录失败或后续正常事务冲突不删除用户目录。
- `schedules/execution/preparation.rs`以当前native authority运行，在同一worker内先查询request既有事实；重试不受自己的预约、已耗尽额度或后来到期的旧grant阻断，也不因此取得新执行资格。新请求重验当前scope、revision、grant、Ask、目标/路径引用和前后台占用。
- `database.rs`从原v2创建/追加逻辑抽出事务helper；普通外层调用保持原验证、权限偏好及事务。scheduled新聊天显式Ask，不继承或重置前台draft_mode。run.operation_id就是原turn操作，create_operation_id独立；实际关联不回填原run快照。
- 组合事务失败由正常事务回滚撤销run、预约、outbox和占额；文件系统准备在事务外，可能保留可复用的未绑定空目录。manual只处理当前显式请求，不claim自动槽或前移日历。
- 删除检查既在入口也在事务内进行，避免检查与进入删除事务之间新建关联。dedicated/existing失效清除未来授权，new_chat历史删除不取消未来策略；run关联只留ID/墓碑，不保留被删聊天正文。

父表重建先做普通内存模型验证：只延迟外键检查时，foreign_key_check虽为空，提交仍报约束失败，未继续采用该方式。最终遵循[SQLite标准表重建流程](https://www.sqlite.org/lang_altertable.html#making_other_kinds_of_table_schema_changes)：只在跨入18时、事务外暂时关闭外键即时执行，canonical migration仍逐项在事务内检查外键后提交，正常返回/错误返回均恢复原设置；随后再验证ledger和外键。保留旧索引，不使用writable_schema或跳过完整性检查。此改动只支持已授权的正常前向迁移，不访问或迁移日常用户库。

回退只允许保留已验证的18 reader并关闭新writer/出站，不能改旧SQL、降级、删表、复制/重置日常库。当前没有新发布pin或日常writer激活资格。

## 3. 实际检查与修正

所有产品检查使用普通合成数据、临时SQLCipher/目录和原生无对话框书签转换，没有启动App/Host/Runtime/Provider。合成终态只用于验证关联复用/删除及派生标记，不是假称真实Codex完成，也没有为测试增加生产释放API。

| 检查 | 命令或明确范围 | 结果 |
|---|---|---|
| FEAT-155安全集合 | `YIJIE_FEAT155_CONFORMANCE_DIR=<临时producer目录> cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture` | 31/31 PASS；本批新增9项（迁移1、准备8），前序22项保持 |
| 真实SQLCipher旧数据升级 | 本批existing-user用例补充15库旧聊天→17授权→18→CompatibleReader正常重开 | PASS；旧书签、消息、turn/outbox和grant保持 |
| 旧聊天/权限回归 | 下列8项exact测试及`chat::authorization::tests::`2项 | 10/10 PASS |
| 实际Rust输出 | plan checker检查native-producer；execution checker分别检查phase-3a和phase-3b1输出 | PASS，沿未变权威schema的strict校验 |
| Rust静态 | `cargo fmt --manifest-path src-tauri/Cargo.toml --check`；`cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings` | PASS，零警告；随后最终31项再次全部通过 |
| Desktop前端/文档 | `pnpm lint`；`pnpm build`；`pnpm docs:build` | PASS；保留原>500KB chunk提示，未修改UI |

八项exact测试分别为：

- `chat::migrations::tests::embedded_migrations_validate_and_write_checksum_ledger`
- `chat::migrations::tests::populated_v1_migrates_to_current_and_repeated_startup_is_idempotent`
- `chat::database::tests::project_repository_is_scope_bound_and_remove_never_deletes_directory`
- `chat::database::tests::expired_outbox_lease_recovers_after_restart_without_creating_duplicate_rows`
- `chat::database::tests::public_task_host_identity_becomes_bound_only_after_normal_atomic_host_bind`
- `chat::database::tests::multimodal_blocks_bind_atomically_dispatch_v2_and_expire_content`
- `chat::database::tests::feat152_permission_storage_boundary_survives_normal_reopen`
- `chat::database::tests::reasoning_is_terminal_transactional_bounded_and_cascades_on_delete`

以上exact命令均采用`cargo test --manifest-path src-tauri/Cargo.toml --locked --lib <完整名称> -- --exact --nocapture`。没有调用模型或商家接口；CSV/图片字节仅是原普通附件回归fixture，不是图片API调用。

实际失败与修正如实保留：

1. 初次编译发现guard版本探测函数可见性不足、测试误用SessionSummary.id；限定为chat内部可见并改用session_id，不改guard判断。
2. 首轮准备测试3/6通过；合成终态漏置public-task绑定inflight，另用“确认grant之前”的PlanView与之后状态比较。修正基线和普通状态构造后暴露lease_expires_at/last_error_code既有CHECK配对要求；完整读取旧表约束后补齐，未放宽数据库约束。新增回归完成后8/8通过。
3. 丰富SQLCipher重开检查后，clippy因只读reader多余mut失败；移除mut，不关闭规则。最终静态与回归结果单独登记。
4. 结构化自审补上删除事务内的第二次关联检查，并确保绑定专属聊天改为Auto时明确拒绝。保留既有策略摘要、manual时间语义和双层出站保护；实现与审查分离，本轮未使用子agent，不冒称独立人工批准。

## 4. 来源与证据

HEAD/branch/remote保持12的基线：元仓`2f616f4d24c001812c6279a520ba69ea9875247e`、Desktop`4a8a67bec4903624ca98a1098572fa26f3a20849`、Contracts`db4458fe94572c4df41a114005d54a049bb79b1f`、Host`0e47766f494977c94bfea0e89cfbdf45a7fafa2b`、Runtime`6c1ad767f0997845b8258a1c452fd4eb7577579f`，分支均为`chore/retirement-baseline-20260905`。这是已有HEAD加未提交候选，不是包含本批变化的不可变发布来源。

实施前77份候选与12的证据相等，并保存普通源码快照区分本批和前序改动。实际变化仅Desktop的11份文件（含4份新文件）和元仓；详见[本批来源](evidence/phase-3b-1-source-20260918.json)及[本批实际producer](evidence/phase-3b-1-native-producer.json)。当前记录81份兄弟仓候选。旧migration1—17、依赖锁、共享源/生成物、Host和Runtime保持；旧阶段证据不覆盖。

本次元仓strict、D0、audit-claims、pnpm lint、50/50治理测试、逐文件Shell语法、五仓diff/status及13/14链接/空白检查均PASS。81份候选文件与3份实际producer的SHA-256复核一致，五仓HEAD/branch/remote不变。D0只证明已有设计批准和文档状态，不表示本批真实运行或D4通过。

## 5. 未执行项与停点

| 未执行 | 原因及影响 |
|---|---|
| App/Host/Runtime/Provider启动、实际定时出站、UI/E2E | 本批仅准备基础；三目标真实执行、审批/恢复、全部Must及D4保持NOT RUN |
| 日常库/Keychain访问或迁移 | 未授权为本批操作；默认目标仍15，所有新格式验证是普通合成临时数据 |
| Host恢复、审批观察、正常退出/STOP_PENDING/sleep-wake | 明确保留3B-2，不解除出站保护或以合成终态冒充恢复证明 |
| automatic/rerun、草案、页面、通知/唤醒 | 3C及第四阶段后续范围，系统通知已延期 |
| 全量历史故障/攻击测试、强杀、权限破坏、危险fixture、二进制替换 | 用户长期硬性条款禁止；使用上述正常定向集合，不声称全仓测试通过 |
| Contracts生成/全仓lint/四基线重跑及Host产品检查 | 本批源、类型及consumer清单完全未变；本次运行实际producer的严格conformance，12的原PASS保持历史适用范围，不冒充本轮重新执行 |
| 提交、推送、发布、部署 | 无授权且未执行；本地候选不等于发布 |

受管聊天在旧sidebar可能显示“项目已移除”，仍是激活前须补的来源投影/标签接续，不在本批提前改UI。目录正常准备后若数据库拒绝，未绑定空目录可能保留；没有后台删除逻辑。准备中的预约保守占用，恢复释放仍属3B-2；本批没有面向用户的启用入口。

文本模型额度仍**0/12**，图片0、商家0。完成3B-1报告后停止，不自动进入3B-2或3C；整个FEAT-155继续in_progress，D4 NOT RUN。
