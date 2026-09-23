# FEAT-155 3A 契约校验收口报告

2026-09-18。按用户明确授权执行[11收口方案](11-phase-3a-contract-closure-plan.md)，**收口完成并停止，未进入3B**。Contracts完整`pnpm lint`已从原FAIL修复为PASS，未关闭strict或跳过定时源。此前[10](10-phase-3a-implementation-report.md)及各日志中的FAIL是当时真实结果，保持原记录。

## 1. 范围与来源

本批`contract-impact=semantic`：规范源引用的解释和校验工具行为；JSON payload形状、有效/无效边界及native运行行为保持不变。整个FEAT因数据库及执行兼容仍为breaking，不能用本批分类降级。三族仍为未发布0.1.0 local candidate，未增加功能、依赖、HTTP/IPC入口、数据库版本或Runtime改动。

实施前复现通用checker在`x-family-version`失败，并核对[3A来源证据](evidence/phase-3a-source-20260918.json)的73份候选文件全部相等。另保存这些普通文本及原通用checker于仓库外临时目录，用于区分既有用户改动与本批差异；没有复制用户数据库或二进制。

| 仓库 | 本批前后保持的完整HEAD | 本批范围 |
|---|---|---|
| yijie | `2f616f4d24c001812c6279a520ba69ea9875247e` | 状态、日志、报告与证据 |
| yijie-contracts | `db4458fe94572c4df41a114005d54a049bb79b1f` | 通用checker、三族源的同义声明、leaf生成/校验、样例及派生物 |
| yijie-desktop | `4a8a67bec4903624ca98a1098572fa26f3a20849` | plan schema及plan/execution candidate共3文件 |
| yijie-agent-host | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` | recovery schema及candidate共2文件 |
| yijie-codex | `6c1ad767f0997845b8258a1c452fd4eb7577579f` | 只读，工作区clean |

分支均保持`chore/retirement-baseline-20260905`，远端未改。完整SHA是现有HEAD，**不是包含当前未提交候选的发布pin**。按已批准demo_fast/local范围进行本地同源验证；没有冒称consumer Owner独立人工批准、生产兼容或合并/发布资格。

## 2. 实际修复及同义性审查

1. 通用checker继续`strict:true`，只注册带字符串及版本格式约束的`x-family-version`注解；预注册全部源后编译根和定时族每个定义。其它既有关键字和workflow专用校验保留，不全局容忍未知关键字。
2. 外部`$ref`改为既有canonical `$id`+fragment。新增`scheduled-schema-source.mjs`以封闭仓内注册表解析，不联网加载schema；未知ID/fragment直接失败。跨源片段的内部引用仍按原文档解释，避免draft引用误落到storage根；本地命名引用保留供类型生成。resolver已纳入plan/execution来源锁。
3. draft条件required补充对原字段定义的引用；storage条件增加已由外层强制的object类型及原conversation_id引用。没有修改枚举、required清单、范围、additionalProperties或null规则。recovery条件为required字段生成`{}`声明，父级字段约束仍生效，forbidden仍为false。
4. 三族均由canonical leaf generator重新生成并同步；源、投影、定向测试及actual-producer checker采用适用的`strict:true`。旧通用generator/package/依赖锁和旧consumer pin保持原样。

结构化自审逐项复核了源→resolver上下文→投影→来源锁→consumer摘要。上述条件新增约束要么重复父级已有约束，要么为空声明，原父级验证不会被覆盖。修复前抓取的240个普通合成样例，在当前源与投影上的判定均一致：**68接受、172拒绝**。覆盖草案澄清/候选、四频率条件、三目标/已有聊天ID、grant次数/期限形状、trigger/slot/rerun、恢复状态、缺字段、显式null及额外字段。这是回归证据，不能代替完整业务语义或未来真实执行验收。

修复前源不满足strict、引用也不能直接按标准编译；基线判定由当时可运行的旧投影和旧draft校验方式捕获，原源/投影hash记录在测试fixture及来源证据。**没有声称旧源原本已通过严格检查**。当前全部定时校验入口均保持strict。

Contracts与consumer共10份生成Rust/TypeScript/Go类型逐字节不变。Desktop业务Rust、迁移、授权/预约/出站保护，Host业务Go、两个GET及原恢复OpenAPI也均不变。最终核对：前序73份候选中47份不变，26份按收口范围修改，加上通用checker和3份新文件，本批共30份兄弟仓文件变化；29份旧generator/package/依赖锁/consumer来源记录与HEAD逐字相同。本轮没有借schema修复改变运行逻辑。本次由Codex结构化自审，没有使用子agent，也不等同独立人工批准。

## 3. 实际命令与结果

下表均为本批实际执行并退出0；除注明外在相应仓库执行。检查源码/生成与正常临时合成数据，没有启动App/Host/Runtime服务。

| 仓库/检查 | 实际命令 | 结果 |
|---|---|---|
| Contracts完整lint | `pnpm lint` | PASS；OpenAPI/AsyncAPI、24份JSON Schema、buf、TS noEmit、Go vet；保留12条既有未使用component提示 |
| 三族生成 | `node scripts/generate-scheduled-task-recovery.mjs`；`node scripts/generate-scheduled-plan.mjs`；`node scripts/generate-scheduled-execution.mjs` | PASS；来源锁与schema按源派生 |
| 三族重生/严格检查 | `node scripts/check-scheduled-task-recovery.mjs`；`node scripts/check-scheduled-plan.mjs`；`node scripts/check-scheduled-execution.mjs` | PASS；确定性重生、digest及严格编译 |
| 三族同步 | `node scripts/sync-scheduled-task-recovery.mjs`；`node scripts/sync-scheduled-plan.mjs`；`node scripts/sync-scheduled-execution.mjs`；三者再分别加`--check`复核 | PASS；Desktop/Host candidate一致 |
| Contracts定向测试 | `node --test tests/scheduled-task-recovery.test.mjs tests/scheduled-plan.test.mjs tests/scheduled-execution.test.mjs tests/scheduled-schema-closure.test.mjs` | PASS 17/17；原13项加收口4项，含240样例判定对比 |
| Desktop实际producer/回归 | `YIJIE_FEAT155_CONFORMANCE_DIR=<临时输出目录> cargo test --manifest-path src-tauri/Cargo.toml --locked --lib feat155_ -- --nocapture` | PASS 22/22；本次实际输出已另存证据 |
| actual-producer conformance | `node scripts/check-scheduled-plan-producer.mjs <本次native-producer.json>`；`node scripts/check-scheduled-execution-producer.mjs <本次phase-3a-native-producer.json>` | 两份输出均PASS，strict:true |
| Desktop静态 | cargo fmt检查；`cargo clippy --manifest-path src-tauri/Cargo.toml --locked --all-targets -- -D warnings`；`pnpm lint` | PASS |
| Host同步/只读回归 | `make scheduled-recovery-check scheduled-recovery-test` | PASS；4个明确筛选的安全顶层测试，含race和实际HTTP producer检查 |
| Host静态 | `make lint` | PASS |
| 兼容基线 | `bash scripts/check-breaking.sh <SHA>`，分别运行下列四个完整SHA | 全部PASS；不替代语义与producer证明 |

四个基线：`db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`。这些基线没有新增定时族，族内兼容另由同源生成、语义对比及实际producer证明。

本次失败与修正：先复现原始注解错误；源修复后，原13项测试首次为12 PASS/1 FAIL，旧TimeRule用“原源对象等于展开投影”断言，canonical内部引用展开后不再结构相同。改为核对权威canonical引用和字段定义一致，保留既有频率拒绝用例，并用新增240样例比较源/投影的实际判定；最终17/17通过。没有放宽字段约束迁就测试。

本次元仓`check-feature-package.sh --strict`、`--gate D0`、`validate-feature-package.mjs --audit-claims`、`pnpm lint`、`pnpm test`（50/50）、逐文件`bash -n scripts/*.sh`、五仓`git diff --check`以及11/12本地链接/空白检查均PASS。来源证据逐文件hash复核一致；D0只是已有设计批准及文档状态，不能换算成D4。临时证据收集脚本首轮仅按`.gen.*`后缀识别类型，漏计Desktop的`*_generated.rs`/`*.generated.ts`而在计数断言处退出；改为明确登记四个Desktop文件后10/10字节核对通过，没有修改这些类型文件或产品逻辑。

## 4. 证据与边界

- [当前来源及检查摘要](evidence/phase-3a-contract-closure-source-20260918.json)：逐文件修复前后hash、候选基线、未变化类型/旧来源、实际命令状态。
- [本次计划producer](evidence/contract-closure/native-producer.json)与[本次执行producer](evidence/contract-closure/phase-3a-native-producer.json)：由本次22项native测试实际写出，普通合成数据，不是手写的运行回执。
- 修复前240样例固定在Contracts `tests/fixtures/scheduled-schema-closure.json`；旧[3A证据](evidence/phase-3a-source-20260918.json)、旧producer及[10报告](10-phase-3a-implementation-report.md)不覆盖。

| 未执行项目 | 原因及影响 |
|---|---|
| 含历史攻击、权限破坏、故障注入或强杀的全量测试/全局fixture生成 | 用户长期条款禁止；只运行已审查leaf及安全定向集合，不声称全仓测试通过 |
| App/Host/Runtime/Provider真实启动、UI/E2E及实际定时投递 | 本批仅契约收口；全部Must仍pending，D4 NOT RUN |
| 日常用户库/Keychain访问、迁移或复制 | 不在授权范围；仅正常临时合成库，普通入口仍迁移目标15、reader上限17 |
| 本批前端build/docs build及全套旧聊天回归 | 本批无UI、生成类型、native/Host业务或迁移代码变化；本次以静态检查、22项native和Host4项覆盖受影响范围，不冒用3A旧结果为本次结果 |
| 模型、图片、商家接口；通知/唤醒 | 没有本批调用或平台验收；文本预算仍0/12，图片0，商家0 |
| 提交、推送、发布、部署或新分支 | 未授权且未执行；本地候选不等于发布 |

## 5. 停点

Contracts通用lint缺口已收口，整体FEAT继续in_progress、Must未验收、D4 NOT RUN。3B/3C/UI均未开始，本批不新增可投递资格或移除保护。11 §5所列稳定授权策略与实际会话/目录绑定问题留给后续3B接入前设计；本轮不顺手修改。完成报告后停止，不自动继续。
