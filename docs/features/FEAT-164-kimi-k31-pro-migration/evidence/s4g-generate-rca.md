# S4g 通用生成检查三次失败 RCA

停止重试：三次相同命令pnpm generate:check均exit1，保留原日志。不把不同错误码当作无限重试理由。根因审计于2026-10-25执行；无产品更改后强行重跑、无降低门禁。

时间线：s4g-generate缺历史Host1b7bfd checkout；准备已有干净固定checkout引用后，s4g-generate-pinned缺Skills10c45be；补已有固定Skills引用后，s4g-generate-complete进入通用市场目录检查并发现11 != 9。

撤回假设：新资格树只有Desktop干净、其他source symlink就足够执行所有通用检查。事实上Connectors原工作区有用户其它需求revision11，FEAT164固定源revision9。进一步完整链路审计发现通用market-catalog.candidate.json本来固定旧e2792f9，FEAT164另有专属immutable锁1f15726；即使换成clean1f，通用锁仍不能代表本Feature资格。

区分证据：git show 1f15726:catalog/market-catalog.v1.json是revision9；既有干净connectors-s4-source exact1f。sync-market-catalog.mjs与277基线逐字相同，硬编码9及local-worktree旧锁；run-local-demo-fast.sh的FEAT164入口明确选择feat164-market-catalog.mjs，ordinary模式不激活market。native、scheduled生成步骤在第三轮均已通过，未修改任何源schema、生成物或版本断言。

结论：新工作树依赖准备不完整叠加通用/Feature入口混用，属于验证环境/范围问题；不是本轮草案状态产品修复回归。根因已收敛。更正新树自己的Connectors符号链接到既有clean1f来源，不动原目录或锁；Host/Skills历史检查复用既有精确checkout。通用generate:check仍标FAIL，不执行第四次、不标full-green，也不扩改用户其它需求。

下一步只在已授权范围内完成既有canonical ordinary构建与旧失败草案只读UI验收；这是本轮原计划中的独立验证，不是重跑或通过通用门禁。原生和Renderer定向检查、生成原始结果、文档与构建分别列证。整体G3仍阻断。若未来要修改通用入口/锁或重跑失败门禁，须先审阅此RCA并按当时范围授权；本轮不伪造Owner新批准或已解决的熔断状态。
