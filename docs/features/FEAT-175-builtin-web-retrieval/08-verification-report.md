# FEAT-175 当前验证记录

2026-11-16 用户要求暂停功能推进，转为 Git 阶段存档与中间产物清理。当前结论保持“本地集成完成、行为验收部分通过”；第 39 页的失败、费用边界和公开交付缺口不因提交／推送而转为通过。本轮不执行新付费调用。提交边界、复用检查及清理结果见 [40](40-pause-checkpoint-and-cleanup.md)。

最新真实复验（2026-11-16）：三个原始 MiniMax 自然任务已执行，2 项自然完成、1 项因多余检索正常中止。本次 Basic 首次选路成功，MCP Fetch 未重复同 URL／锚点；但 Basic 使用正文参数并继续 Fetch，两项最终答复仍超长，研究亦先并行 Fetch 后 Pro。新 Host 指令在三个实际会话中均已确认，不能继续归因于旧规则未传达。已知用量约 ¥2.00，中断在途结算不完整。详见 [39](39-minimax-natural-task-recheck.md)及[机器记录](references/minimax-natural-recheck-result.json)。正常退出，批次关闭，无产品修改／公开分发，整体未通过。

最新修复（2026-11-16）：已消除会话级“未选连接器只走原生”的旧规则冲突，补齐 Basic 独立函数的选路／完成条件，以及三工具共同的按交付范围收尾规则，并明确换锚点不是 Fetch 分页。7 项原有契约检查、四消费者同步、固定 Runtime 双模型 race 协议验证和正常开发构建通过。新增真实调用／费用 0。详见 [38](38-basic-routing-and-retrieval-convergence-fix.md)及[机器记录](references/basic-routing-convergence-fix-result.json)。新规则的真实模型遵循仍待复验；C01 历史首个请求工具表缺失的边界及下述真实失败均保留。

最新产品验收（2026-11-16）：五项自然任务及一个 MiniMax 显式 Basic 对照均自然完成；自然首个应用检索 4/5 符合预期，内容／格式 2/5 通过，对照执行通过。MiniMax 研究已产生有依据的完整三点答复，但过长；自然 Basic 选路仍未通过。C05 约 185 秒，观察时限偏差单列。保守估算 ¥12.519372，授权已关闭，正常退出。详见 [37](37-minimum-product-acceptance-result.md)与[机器记录](references/minimum-product-acceptance-result.json)。没有修改产品代码或公开分发，整项未关闭。

最新根因修复（2026-11-16）：已复核追加检索的必要性，在既有网关补齐容量 2／最多等待 5 秒的可取消发送限流，并复用现有诊断接通服务端 HTTP 状态与本机超时分类。7 项契约、8 项 Rust、1 项 Go race、双模型原生发现及正常 App 构建通过，真实调用 0。旧 Fetch 的具体上游状态未保留，仍不能伪造确诊。详见 [36](36-retrieval-followup-cause-and-fix.md)及[机器记录](references/retrieval-followup-fix-result.json)。

最新真实复验（2026-11-16）：原始研究任务的单次 MiniMax 样本已自动调用 Pro，全部 Pro 尝试带合法 `sites`，成功返回的 24 条结果均在对应站点内。因追加并行检索触发执行方观察护栏而正常停止，完整答复未验收；已知用量保守估算 ¥0.461554，最终结算不完整。见 [35](35-minimax-original-research-live-result.md)及[机器记录](references/minimax-original-research-live-result.json)。没有追加样本、产品修改或 QA 扩建。

最新修复（2026-11-16）：MiniMax 的 Pro 独立函数已补齐与 Kimi 工具组同源的研究规则；原有 7 项契约检查、四消费者同步、固定 Runtime 双模型协议用例及正常 App 构建通过。见 [34](34-minimax-shared-rule-projection-fix.md)及[机器记录](references/minimax-projection-fix-result.json)。本轮新增费用为 0；真实 MiniMax 选路尚未复验，上批失败结论保留。

最新状态（2026-11-16）：产品最小闭环及正常 App 入口见 27—31；本轮已完成四项真实复验，见 [33](33-focused-real-recheck-result.md)及[机器记录](references/focused-recheck-result.json)。自然研究选 Pro 1/2，受控截断 Fetch 不重复 2/2；MiniMax 研究选路和错误执行次数自述仍未通过。保守估算 ¥5.233163，四项授权已消费关闭，App 和自有服务正常停止。没有新增产品代码、扩建 QA 或公开分发，正式 Q2／FEAT-175 整体资格没有转为通过。

以下保留 2026-11-15 的阶段验证历史；其中“尚未接线／未启动 App”等状态只表示当时边界，不覆盖 27—33 的后续事实。

2026-11-15，修订3限定S1／Q1及后续零费用准备。最新零费用采样／诊断见[25](25-q2-v2-sampling-and-diagnostics.md)与[检查记录](references/q2-v2-checks.json)；首轮真实失败见24，保持原样；19及s1-q1-checks保留原始运行与当时阻塞事实。

| 项目 | 当前状态 | 覆盖边界 |
| --- | --- | --- |
| 独立源契约、SDK与Host候选一致性 | PASS | 未发布工作树候选，原稳定工具名／输入复用 |
| 固定Runtime＋Host race检查 | PASS | 11个顶层用例、10个子例；正常本机Responses／MCP，没有真实模型 |
| 原生确认／模型等待 | PASS | 90秒／120秒；后续工具执行完成，等待中零MCP执行 |
| 原有rmcp有效时间暂停测试 | PASS | canonical准备源，精确1项；其余77项未运行 |
| 双模型配置、默认auto、专家政策、切换／恢复 | PASS（Q1） | 实际wire与原生Item；完整资源安装和产品接线仍属S3 |
| 取消、拒绝、晚到确认、并发隔离 | PASS（本机） | 本次MCP取消通知为0；Host撤销在途I/O有效；不能推定云端停止 |
| builtin／market／media共存 | PASS（本机） | 正规Runtime与现有市场worker，正常EOF；共享worker新增web transport仍待S3 |
| 7项契约测试、新API lint、TS、Go vet／格式 | PASS | 本需求定向范围；9个适用保留基线均无新family，130个引用本地解析 |
| 全量生成／完整lint | PASS | 补齐3个family及严格注解类型；37个family核验，SDK代码/schema保持；12项原有unused警告 |
| Q2离线准备／专属接线 | PASS（本机） | 12任务、43来源冻结、13项费用测试、10项评分、1项schema、2项纯Go／5子项；真实模式仍需授权 |
| Q2本机原生执行／正常停止 | PASS（合成） | 固定Runtime执行12任务／24个本机模型HTTP／8个MCP；另1个请求验证原生interrupted与正常退出 |
| Q2-v2采样／拒绝诊断 | PASS（本机QA） | 14项评分、8项诊断；12个首次采样、12个完整流程与配额拒绝原生race场景；首次结果与完整任务成功分开 |
| Q2-v2只读重评／保留 | PASS | 旧Python样本首次路由MATCH、完整任务FAILED；原始score／账本／已消费授权不变，新付费调用0 |
| 真实v2前置审计 | live阻塞 | 新增纯状态用例发现：采样关闭后首次出现身份仍可准入；没有Runtime／HTTP／真实出站。需先修补任务级关闭与原生绑定，并补真实SSE收尾资格，见26 |
| B01依赖盘点 | 完成（仅源码） | 6项交接清单；公开环境／账户／实际服务未查询 |
| 首轮真实Q2 | 未通过／已停批 | Kimi 2项已观察，1项完成、1项失败；模型HTTP 5／hosted 3／本机MCP准入4；其余10项缺失，包含MiniMax全部6项 |
| Q2费用与停止 | 已核对原生／计量事实 | 保守费用2.487164元，未核对账单；供应商REST 0；Runtime与计量器正常退出，一次性授权已消费 |
| Q3／Q4及B01公开依赖 | NOT RUN | 未自动扩展公开／供应商REST／部署资格 |
| 日常App激活、真实UI、部署、迁移、提交／推送 | NOT RUN | 本轮未执行 |

首轮失败、修复及复验均保留，不把调试中的失败日志删掉。禁止的强杀、可执行文件伪装、权限破坏和攻击fixture未执行；未跑全量历史测试，不声称其通过。
