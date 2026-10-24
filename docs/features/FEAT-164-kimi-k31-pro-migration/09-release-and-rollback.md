# FEAT-164 激活与回滚候选Runbook

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
