# FEAT-155 · 3C-3A 实施报告

2026-09-18。用户明确授权只实施[21方案](21-phase-3c-3a-implementation-plan.md)，完成后停止。本批原生管理查询、确认边界与最小typed IPC已完成；3C-3B草案、页面和真实激活均未开始。**普通入口仍为schema15、默认禁发，没有SQL schema22。** 本批文本0，累计0/12；图片/商家0，未访问或迁移日常库/Keychain，未提交、推送或发布。

## 1. 交付及契约归属

本批`contract-impact=semantic`，完整FEAT-155仍为breaking。Desktop私有IPC v1源先行，复用既有Contracts计划/执行schema和Rust/TS类型；未改变共享领域源或发布版本。权威分层沿21及FEAT-126既有Accepted决策。Owner仍为段成威；本轮实施、自审和验证由Codex完成，不声称独立人工批准。

实际修改仓为Desktop与元仓。Contracts、Host、固定Runtime的全部起点文件摘要和五仓HEAD/branch/remote保持，旧1—21迁移逐项不变。完整来源及本批文件清单见[来源证据](evidence/phase-3c-3a-source-20260918.json)。生成候选manifest仅用于local验证，不是不可变发布pin。

| 交付 | 实际行为 |
|---|---|
| 最小IPC | Desktop私有schema组合固定摘要的共享源，生成Rust/TS、严格AJV validator及native解析源；15个独立命令注册，无任意操作dispatcher或配置透传 |
| 原生确认 | 当前context、native owner/tenant、capability及授权revision在worker重新校验；同步context租约阻止提交中重绑定，提交前检查UI/native两者较早期限；返回查询前再校验 |
| 删除与幂等 | 所有原生删除入口同事务检查同计划的预约、在途、attention与未释放unknown；其他计划忙不误挡。旧Plan入口映射ExecutionNotReady，新IPC映射ReservationBusy；不强退、退款或清预约来解锁。暂停/删除复用原request表记录命名空间digest |
| 有界查询 | 默认20、上限100，固定SQL排序和keyset游标；游标绑定scope/context/命令/参数，内存上限512、300秒失效。读取不依赖Host/Runtime就绪、不写执行事实 |
| 状态与历史 | Deleted只进全部历史；Completed优先于hold；原Paused保持；仅Enabled因hold/未来额度不足映射暂停。最后已占额run独立保留；无run槽严格分型，planned及取消的未来预览不充作执行记录，关联槽不重复计数 |
| 关联与事实 | 只投影真实本地conversation/turn关联及墓碑；目标只展示目录来源，不暴露路径/bookmark。耗时缺证据返回unknown/not_started，needs_attention不伪装waiting_approval，native completed不等同业务成功 |
| typed client | 双向校验封套、字段和request ID；写入响应不匹配或传输异常返回operation_unknown，保留逻辑ID且不自动重试；保存、grant-only、启用、manual及rerun分别调用原事务 |

关键Desktop路径：`src-tauri/schemas/scheduled-task-ipc-v1.schema.json`、`scripts/generate-scheduled-ipc.mjs`、`src-tauri/src/chat/schedules/ipc.rs`及其`query/validation/tests`模块、`store.rs`/`execution_guard.rs`、`src/api/scheduled-task-native-client.ts`。生成链沿现有Contracts工具依赖，不新增依赖或改lock；AJV格式运行时代码可复现派生并保留MIT许可与来源摘要。

## 2. 实际验证

所有数据为临时SQLCipher或普通进程内协议fixture；使用正常清理退出。没有真实App/Host/Runtime/Provider、强杀、权限破坏、攻击fixture或替换二进制。编译仅由标准项目工具生成开发产物。

| 检查 | 结果与范围 |
|---|---|
| 原生专项 | `cargo test --manifest-path src-tauri/Cargo.toml --lib feat155 --offline -- --test-threads=4`：82/82 PASS（74项前序专项+当时8项本批检查）；补充和收尾`feat155_3c3a`：12/12 PASS，覆盖本批最终代码 |
| 旧回归 | [19项明细](evidence/phase-3c-3a/regressions.json)全部PASS：旧迁移/重开、聊天/原outbox、原生历史与恢复、正常退出及UI授权；未运行含禁止行为的历史全量套件 |
| IPC来源及producer | leaf generator `--check` PASS；[16份实际native交换](evidence/phase-3c-3a/phase-3c3a-ipc-producer.json)覆盖全部15命令，严格AJV及生成TS校验PASS；[11份声明输入校验对照](evidence/phase-3c-3a/phase-3c3a-validator-parity.json)Rust/AJV/TS一致 |
| 既有共享producer | 本轮实际plan、execution基础/组合准备、recovery输出分别通过Contracts canonical严格producer检查；共享源未改 |
| typed client | `pnpm exec vitest run src/api/scheduled-task-native-client.test.ts --maxWorkers=2`：5/5 PASS，覆盖请求/响应匹配、边界/未知字段、确定拒绝和不确定写入无自动重试 |
| 工程检查 | `cargo fmt --check`、`cargo clippy --all-targets --offline -- -D warnings`、Desktop lint/build/docs build及原生聊天定向生成/一致性检查PASS；build保留既有大chunk提示 |
| 总生成入口 | `pnpm generate:check`实际FAIL：第一步public API生成器因`contracts checkout has tracked changes`拒绝继续。起点已存在的Contracts改动完整保留，未关闭保护或清理工作区；上述本批/原生leaf检查独立执行且PASS，不声称总入口通过 |

本批12项原生检查包括：普通15不迁移与21 reader无写权；计划分页/同名按ID/游标失效；保存、授权、启用、暂停和删除幂等；manual重放不再扣额；当前计划在途/未知删除拒绝且其他计划可删；可信未发送释放后保留历史；Completed残留hold、最后已占额run与未来预算分离；关联墓碑与计划筛选；排队重绑定、native权限/revision和提交期限回滚；私有源校验与实际producer。

元仓strict、D0、audit-claims、lint、50/50治理测试及Shell语法均实际PASS；120处变更文档本地链接和五仓diff检查通过。D0只保留既有产品设计批准，不代表D4。原始成功日志：[原生专项](evidence/phase-3c-3a/native-suite.log)、[最终12项](evidence/phase-3c-3a/native-ipc-final.log)、[clippy](evidence/phase-3c-3a/clippy.log)、[typed client](evidence/phase-3c-3a/typed-client.log)；[总生成入口失败日志](evidence/phase-3c-3a/aggregate-generation.log)保留真实限制。

## 3. 失败、修正及技术自审

如实保留本轮发现：生成器首次组合引用的JSON pointer偏移及条件required声明触发严格校验，已在源/生成器修正；未关闭strict。初轮TS类型收窄错误、生成Rust大enum的clippy问题分别通过提前保存request ID和生成Box变体修正。初轮授权检查发现提交前拒绝被错误映射为operation_unknown，已只对成功提交后丢失context作不确定处理。扩展producer时，未绑定的专属聊天不能直接复用，合成用例改为既有new_chat_each_run模式验证独立重跑，未放宽真实目标校验。

结构化源码自审检查了权威源/共享类型、全部删除入口、worker提交与回执边界、作用域/游标、生命周期筛选优先级、未执行槽及历史关联、默认reader与发送构造、费用与安全停点。补查后将提交期限明确取UI/native较早者，回执校验后再作最后context检查。上述修正均有定向复验；无本批范围内剩余实现阻断。总生成入口的既有dirty保护限制单独保留，不等于发布门禁通过。

## 4. 未执行项和停点

真实macOS睡眠/恢复、Provider、正常产品入口、UI/页面、完整Must AC与D4均NOT RUN/pending。完整运行起止/耗时和有时效的审批证据仍需后续真实来源，不能从当前投影推导。系统通知延期，应用内重要更新和唤醒保持原需求后续范围。

本批没有新增UI事件平台、草案outputSchema、Host受限模式、候选激活入口或SQL22。候选writer/dispatch仍只能由显式native构造取得，调用IPC本身不会升级数据库、启动服务或取得发送权。兼容回退保持现有21 reader规则；移除私有IPC不会重写历史，但旧schema15-only二进制仍不能打开候选21库。

**3C-3A完成后停止，不自动进入3C-3B或第四阶段。** 后续方案需另行结合草案权限、来源和唯一确认设计；本报告不授权后续实现或真实调用。

后续方案记录：用户随后要求下一步方案，已仅保存[23：3C-3B1](23-phase-3c-3b-1-implementation-plan.md)，不改变本报告的3C-3A测试来源或停点，未开始后续实现。
