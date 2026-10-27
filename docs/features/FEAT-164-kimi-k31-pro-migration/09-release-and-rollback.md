# FEAT-164 激活与回滚候选Runbook

## 当前D5本机启用与交付完成（2026-10-27）

当前权威[67](67-d5-entry-and-activation-implementation.md)：D5已按Owner明确批准的ADR-0022个人本机范围完成。新日常入口固定Desktop39b0fbe/原Home，默认启用Kimi K3.1 Pro；真实正常启用、暂停回退和同入口再次启用均通过，3次正常退出及完整后态通过。0模型验收调用，原历史/授权/账本/预占及dirty保留，仅本地提交不推送。G4/G5本机就绪与G6实际交付观察分别留证；不授权公网/云端/多人/签名发布。以下66及更早阶段按各自时点解释。

## 当前D3实施结果（2026-10-27）

当前权威为[64 D3一次维护与后态审计](64-d3-controlled-migration-and-post-state-audit.md)。Owner批准的一次维护已完成，日常Native由SQL37升级到41后正常退出；候选、完整D2备份、实例锁/句柄及数据一致性先行核验，后态完整备份与只读复核通过。67张既有业务表全部旧行不变，仅新增4条迁移记录和3张空表；原Host/Runtime、密钥、账本/预占保持。

当前D3_COMPLETE_STOPPED，不进入D4。无GUI、Host、Runtime启动或新模型调用，无Runtime核心/补丁修改。下一步仍须单独批准D4并重验后态/锁/全模型无派发工作/既有workflow ready；D5长期入口、local G5/G6口径继续待收口。旧SQL37构建不可直接重开SQL41，未执行回退。58接受范围与Owner排除项保持。下列旧阶段按原时点解释。

## 60号历史D1实施结果（2026-10-27）

当前权威为[60 D1完成与离线资格](60-d1-daily-binding-and-offline-qualification.md)。59号D1已获批并完成六文件Desktop修正、安全测试和新canonical prepare-only/同回执复核；Host/Runtime采用已批准原Home绑定，daily不再隐式workflow-up。真实日常绑定未生成、D2—D5未执行、模型HTTP新增0、Runtime核心/补丁未改。原CUTOVER-01/03已离线修复，日常现场/启动资格仍无授权，G4不自动晋升。58接受的never-sent替代保留，完整App正向取消仍NOT RUN。

下方59及更早“尚未实施D1/原入口缺陷”按当时来源解释，不再作为当前D1未完成项。下一步仅在批准D2后进行完整冷备份和副本只读预检，不顺带迁移或启动。

## 59号历史日常切换边界（2026-10-27，S4AF）

以[59 日常切换方案](59-daily-cutover-minimal-plan-and-authorization.md)为当前部署权威。源码复审发现daily launcher将Host/Runtime Home改至候选新目录、与原Native日常库缺连续性；正常启动还可能隐式workflow迁移及恢复自动计划。日常activation为NO_GO，当前G4重新pending，先提限定部署入口修正及离线资格，尚未获准实施。58的已接受本地S1—S4/final证据与never-sent替代保持，完整App正向取消原执行仍NOT RUN；不是重新跑失败或取消Owner接受。

本轮仅方案和治理，无产品/Runtime改动，无日常数据访问/备份/预检/迁移/启动，无模型调用。阶段顺序为D1入口修正→D2完整冷备份与副本只读预检→D3一次Native维护→D4首次受限启动及退出核对→D5确认日常启用；D1—D5均未自动授权，具体边界见59。以下早期状态按各自时点解释。

## 58号历史已接受范围（2026-10-27，S4AE）

以[58 安全替代接受与最终收口](58-owner-accepted-substitute-and-final-closure.md)、feature.yaml和[当前矩阵](current-acceptance-matrix.md)为准。Owner明确接受57号never-sent正常Native API与生产消费链的安全分层替代；S4/TCONF04及三项适用最终验收按该方式收口，G4为本地代码完成。**完整App正向never-sent取消的原始执行状态仍为NOT RUN**，没有改写为已执行。原自然unknown缺Host回执，安全拒绝重发通过，原记录仍未恢复ready。

本轮仅只读审计和治理更新，真实/本机模型HTTP新增均0；产品、Runtime核心/补丁、来源锁不变。不启动或迁移日常库，日常候选保持prepare-only，G5/G6及正式交付仍pending。搜索答案正确性、亮暗/键盘/最小窗口专项保持OWNER_EXCLUDED，不恢复为待办。以下早期阶段记录按原时间和来源解释；本节覆盖其中过期的推进顺序、预算授权和“当前未通过”描述。

## 兼容组合及前置

V0：保留旧K3制品，仅在独立资格身份正常产生旧数据，不作为迁移后的回退writer。Vc/Vn：当前r5兼容candidate已构建，可读取旧/新事实并独立暂停Kimi；S4S旧/新资格App分目录、固定同一独立identity，来源和实际artifact digest见46。已有构建不等于完整回退或日常激活资格。

激活前必须：来源/pins一致，兼容reader测试通过，各适用Gate和freshness证据满足；schema迁移和回退在合成数据验证；用户库操作范围获准；旧工作正常结束；费用上限批准。保留旧binary不是回滚资格，新Host baseline未必接纳它。

## 正常激活顺序

兼容候选source freeze → 全部读者与准入资格验证 → 现有应用停止新增派发 → 正常收敛主聊/标题/Guardian/草案/子代理/worker → 正常退出并确认无在途 → 获准后前向迁移 → 在新worker启动前完成退役分类和claim/send检查 → 核验受管双文件组合 → 固定cutover → 新模型激活 → 获批smoke与观察。

已实现的候选暂停设置为 `YIJIE_KIMI_K31_EXECUTION_PAUSED=true`，通过同一canonical候选入口生效；正常结束受管工作并退出后按合格来源重开。它仅停止新Kimi执行，保留MiniMax/历史，不能用关闭全部模型代替。恢复执行仍需满足准入和当前授权；暂停不退款、不重发，也不授权启动旧reader或迁移日常库。

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

## 历史阶段记录

以下限定于各自日期与来源；当前不再受早期未构建/未批准描述约束。

### S4本地候选状态（2026-10-25）

未发布、未迁移日常库、未重建活动S1 App。仅本地来源为Contracts eddc64f、Host9ffcb6f、Desktop e408047（含704cfdb）。`YIJIE_KIMI_K31_CALL_SURFACES`显式选择ordinary/market/experts/media，缺省ordinary；不能用组合选择代替安装、账号、任务或工具授权。专家/媒体受旧资源pin不一致阻断，禁止刷新digest掩盖。仍须先让活动App正常退出，再canonical新构建及同源重开，不能用旧App验证新源码。SQL41兼容reader和暂停Kimi回退要求沿S3保留。

## S4g 旧草案状态续办（2026-10-25）

本轮仅Desktop181885b本地修复，无push/发布。旧库无写迁移；277 reader仍可读，但会恢复误导queued提示。保持旧App/账本/原失败草案，回退不能放行重发。

## S4h 生成入口与计划验收（2026-10-25）

本轮只有Desktop验证入口提交1b5adcf，默认检查/产品wire及所有旧锁保持；App沿同canonical新构建验收，原合成计划最终恢复Kimi且关闭。回退验证入口不降级用户数据或恢复旧执行授权。


## S4L 退出与备份边界

候选正常退出后Runtime SQLite仍可能保留有效且未backfill的WAL；只复制主数据库不能代表完整状态。此次完整DB/WAL/SHM审计副本可只读一致读取，未手工checkpoint或删除原文件；完整checkpoint责任仍需收敛。日常迁移/入口切换继续未授权，不能用本轮视觉PASS替代core/teardown批准。
