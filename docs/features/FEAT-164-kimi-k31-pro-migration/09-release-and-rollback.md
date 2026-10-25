# FEAT-164 激活与回滚候选Runbook

> 最新按[37 当前G2V后继验收](37-current-g2v-successor.md)：Owner已批准本轮1+2共3次真实HTTP（累计5次/30元）；工具和新canonical本机正控/重开已通过，真实新增0。等待Owner交回候选窗口，meter已正常停止；额度保留，不重批预算、不重置旧账本。

> 2026-10-26最新续办以[36 当前离线资格与下一步](36-current-offline-qualification-and-next-gate.md)为准：当前S1/S2/S3及S4专家/媒体/辅助/旧线程安全检查通过，产品代码未改；候选无旧K3会话/计划可自然升级。完整G2V/TCONF/final与日常cutover仍缺，新真实HTTP许可0；后续避免反复运行已通过子集。

> 最新续办与整项目标以[35 当前组合与完成差距](35-s4-current-media-and-completion-audit.md)、feature.yaml及S4I证据为准。旧阶段记录保留其原来源和时间；当前仍未切换日常入口，不新增真实模型HTTP。

> S4I结果：Desktop399bb19/Host090c2db配对专家切换、r4媒体/正常中断/图片、同源重开及清理通过；旧unknown仍保留阻断。当前安全子集分组通过不等于完整TCONF/G2V/G3/final。后续按35末节整项执行单推进。

> 当前（2026-10-25，S4f普通App与计划）：Host7927ee7补齐已有v2草案三路由，Desktop277f59e兼容读取原生事实2/3/4；Runtimea28130a r4与Contracts1b357cc保持。同源App验证旧历史、input-only草案、只读恢复零补发、关闭保存、单次执行、取消编辑和正常重开；App模型协议loopback共3次，真实新增0。旧失败请求/事实/账本保留；完整恢复取消、旧模型计划、专家媒体当前组合、平台/G2V/G3/final仍未通过。权威见[32](32-s4-r4-app-plan-acceptance.md)。以下记录保持原来源与时间语义。

> 当前（2026-10-25，方案A原生终态修复）：Runtime r4 a28130a → Contracts1b357cc → Hostb9155a3 → Desktop2fb8989已本地固化。原子代理错误被completed覆盖及冷历史丢失失败已修复；10项核心、269 schema零差异、7项原生/23次本机HTTP证据复核、3辅助/9次与4调用面/6次均通过。新增受管writer标记阻止旧r2候选写入新历史；不改旧历史。全轮50次合成本机HTTP、真实新增0，旧账本/预占保留。App本批仅构建，完整UI/计划/恢复取消/平台/G2V/G3/final仍未通过。最新权威见[31](31-s4-native-terminal-repair.md)及feature.yaml；以下旧阶段保持历史含义。

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S4专家/媒体/辅助续办）：专家pin已按Skills595c927不可变同内容来源修复；Hostcac2d4d、Desktop56f5284、Connectors1f15726已仅本地固化。四组合source、37专家版本安装/解析/重开及专家/媒体/原生辅助调用安全离线验证通过；S2/S3/S4当前源回归通过。完整TCONF-164-04、App/平台/G2V/G3/final仍未完成，真实模型新增0，旧账本/预占保留。最新见[28](28-s4-expert-media-auxiliary.md)及feature.yaml；下方段落保留各阶段历史范围。

> 当前（2026-10-25，S3）：Contracts2dd214d / Desktop4d04597已本地固化计划退役、SQL41和授权保护；TCONF-164-03五项、70前端及当前源S2复验通过。App/UI/平台与完整G3仍NOT RUN，真实模型新增0，旧账本/预占保留。最新见[26](26-s3-plan-retirement.md)及feature.yaml；下面旧阶段结论按原来源保留。

本轮未实施/部署/迁移/发布。exposure=local；公网、签名、tag、推送、生产环境及G5/G6均无授权。本文是需后续验证的操作设计，不是现成可执行脚本说明。

## 兼容组合及前置

V0：当前旧K3组合，作为只读审计基线。Vc：拟实现兼容构建，读取旧/新schema和Host状态、识别旧/新受管配置，可独立停止新Kimi执行且保留MiniMax/历史查询。Vn：拟实现新模型活动组合。Vc/Vn尚未构建，manifest/hash不得预填。

激活前必须：来源/pins一致，兼容reader测试通过，各适用Gate和freshness证据满足；schema迁移和回退在合成数据验证；用户库操作范围获准；旧工作正常结束；费用上限批准。保留旧binary不是回滚资格，新Host baseline未必接纳它。

## 正常激活顺序

兼容候选source freeze → 全部读者与准入资格验证 → 现有应用停止新增派发 → 正常收敛主聊/标题/Guardian/草案/子代理/worker → 正常退出并确认无在途 → 获准后前向迁移 → 在新worker启动前完成退役分类和claim/send检查 → 核验受管双文件组合 → 固定cutover → 新模型激活 → 获批smoke与观察。

同模型总开关关闭会禁历史读取和MiniMax，不能拿现成总开关替代Vc的独立新Kimi写入口控制。关闭/恢复控制必须由实现提供并验证；当前没有可引用的精确命令，因此本轮不编造生产命令或杀进程指令。

## 失败与回退

| 触发 | 动作/数据处理 |
|---|---|
| source/pin或未知配置不一致 | 在派发前拒绝，保留所有文件/数据；精确已知过渡组合才可正常收敛 |
| schema或reader资格未满足 | 不迁日常库、不启用新写入；返回设计/证据补齐 |
| Runtime配置回执未确认 | 保持unknown，允许只读历史；明确恢复同目标配置，不自动再次业务调用 |
| 发现K3新出站/重复执行/历史错写 | 立即停止新增Kimi派发，正常结束受管工作；保留证据，进入RCA |
| 新模型账号不可用或质量失败 | 明确不可用、独立停Kimi；用户可主动选MiniMax，不自动回退K3 |
| 新身份已持久化 | 用验证过Vc读取并停派发或前向修复；不直接启动旧reader、不降库、不恢复旧DB覆盖新记录 |
| 无安全退出方式 | 停止步骤、报告当前在途状态，不强杀 |

可选备份恢复只在用户另行批准可接受数据损失、备份有效性和范围后制定；不是默认回滚。不能复制用户数据库作为验收fixture。原operation/grant/run/payload/digest保持，合法取消/暂停状态另记。

## 观测与完成标准

分开观察 model/provider/effort、旧slug新请求数（必须0）、重复operation新HTTP（必须0）、unknown未决数、计划授权/slot状态、来源锁、secret泄漏（必须0）、token用量及未知计费。只记录脱敏身份摘要/状态，不导出完整正文或Key。

G4前三项final verdict独立；换source/runtime/harness后相关结果STALE。local结果不等于发布/Production Ready，G5/G6保留pending。所有实际操作步骤、命令、负责人、日期、最终artifact digest和回滚演练结果在执行获准且真实产出后填入，不虚构。

## S4本地候选状态（2026-10-25）

未发布、未迁移日常库、未重建活动S1 App。仅本地来源为Contracts eddc64f、Host9ffcb6f、Desktop e408047（含704cfdb）。`YIJIE_KIMI_K31_CALL_SURFACES`显式选择ordinary/market/experts/media，缺省ordinary；不能用组合选择代替安装、账号、任务或工具授权。专家/媒体受旧资源pin不一致阻断，禁止刷新digest掩盖。仍须先让活动App正常退出，再canonical新构建及同源重开，不能用旧App验证新源码。SQL41兼容reader和暂停Kimi回退要求沿S3保留。

## S4g 旧草案状态续办（2026-10-25）

本轮仅Desktop181885b本地修复，无push/发布。旧库无写迁移；277 reader仍可读，但会恢复误导queued提示。保持旧App/账本/原失败草案，回退不能放行重发。

## S4h 生成入口与计划验收（2026-10-25）

本轮只有Desktop验证入口提交1b5adcf，默认检查/产品wire及所有旧锁保持；App沿同canonical新构建验收，原合成计划最终恢复Kimi且关闭。回退验证入口不降级用户数据或恢复旧执行授权。
