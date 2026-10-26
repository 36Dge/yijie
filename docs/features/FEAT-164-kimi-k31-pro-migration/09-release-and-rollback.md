# FEAT-164 激活与回滚候选Runbook

> 当前以[49 r5真实功能与日常边界](49-r5-real-qualification-and-daily-cutover-boundary.md)为准：Owner已明确授权必要真实功能调用且不要求精确查价；本轮1次r5真实42、保存/重开零补发和正常退出通过。旧账本/预占保持，日常迁移未执行；完整core/剩余业务状态仍按明确缺口判定。已移除外观专项不再作为门槛。

2026-10-26当前：只实施本地独立资格，未发布、未迁日常库。r5已构建，限定正常关闭已通过；当前来源与剩余门禁见[46](46-independent-legacy-app-qualification.md)和[当前验收矩阵](current-acceptance-matrix.md)。历史阶段按其原报告解释。公网、签名、tag、推送、生产环境及G5/G6无授权。

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
