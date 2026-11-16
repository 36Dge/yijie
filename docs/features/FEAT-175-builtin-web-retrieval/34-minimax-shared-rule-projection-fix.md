# FEAT-175 MiniMax 独立函数公共规则投影修复

2026-11-16。用户授权按第 [33 页](33-focused-real-recheck-result.md)建议做最小产品修复、定向验证和复审，不扩建通用 QA。本轮已完成源码修复、四消费者同步、正常 App 构建及固定 Runtime 双模型协议验证；**没有新增真实模型或付费搜索调用，不能把上批 MiniMax 研究选路失败改写为通过**。

`contract-impact=semantic`：修正模型可见的工具指导，并明确需要联网研究／显式站点或时间限制时应执行 Pro。工具 wire、权限、审批、错误及存储没有变化；FEAT-175 整体原有 breaking 判定保留。此次为未发布 `0.1.0` 本地候选，Owner 为段成威；producer 为共享 worker，消费者为当前 Host／Desktop／API／Connectors 的同源候选。没有新增 Runtime patch、Host 调度器、意图分类器或工具选择开关。

## 最小实现

权威源 `yijie-contracts/compatibility/builtin-web-retrieval/policy.json` 增加一份 `research_instructions`，由已有 `loadBuiltinWebSource()` 机械组合到两个既有表面：

- MCP `initialize.instructions` 使用的完整 `ServerInstructions`；
- `kimi_web_search_pro` 的工具描述。

两处消费同一份规则，避免今后只改工具组说明而遗漏独立函数。未把全套工具说明复制到每个函数，没有新增通用规则配置框架。共享文本为 588 字符，生成后的 Pro 描述为 759 字符。

规则明确：普通问答默认原生 `web_search`；明确读取 URL 使用 Fetch；联网研究、需要网页证据的比较、正文证据采集及显式站点／时间限制，在答复前调用 Pro 并传入要求的过滤。供应商预搜索即使已经提供足够材料，也不能替代这里的 Pro 步骤。相同信息需求已有足够 Pro 证据时直接复用，避免把“必须使用”误解为必须反复调用。

Pro 专属描述继续说明正文片段、来源链接、查询词中的站点不等于 `sites` 过滤，以及截断后缺失事实可用聚焦查询。Basic／Fetch 描述逐值保持；成功截断处理、无分页与相同 URL 不重复的规则保持。

复用链路不变：同源政策 → 原 generator → worker MCP 元数据 → 固定 Codex Runtime。Kimi 从原生工具发现／命名空间获得规则；MiniMax 既有 `function_namespaces` 适配保留函数描述，因此这次无需修改会丢弃 namespace 描述的 Runtime 适配本身。规则仍是模型指导，不是硬调度或供应商预搜索禁令。

## 定向验证结果

| 验证 | 结果与边界 |
| --- | --- |
| 原有 7 项 FEAT-175 契约检查 | 全部通过；在原用例中补充共享规则两处各一份、关键语义及 Basic／Fetch 保持的断言，没有新增框架 |
| 四消费者生成一致性 | `generate-builtin-web.mjs --consumer=host --consumer=api --consumer=connectors --consumer=desktop` 及同参数 `--check` 通过；派生物由原 generator 生成 |
| 固定 Runtime＋正规 worker | 复用 `TestFEAT175SharedWorkerBuiltinDiscovery`，两个模型 profile 均通过 race 检查；检查实际模型请求／工具发现输出中的 Pro 描述，三条关键语义均到达 |
| 原生协议执行边界 | Kimi 本机合成 Responses 3 次、MiniMax 2 次；各一次正常本机资格拒绝，均在供应商派发前结束；真实模型、hosted 搜索、供应商 REST 均为 0；正常 Shutdown／EOF |
| 输入输出及旧工具兼容 | 7 份 wire／HTTP／旧工具源逐字节保持；除公共说明、共享研究规则和 Pro 描述外，政策字段逐值保持，含工具名、参数、注解、auto、超时、专家政策及授权语义 |
| 格式、语法及构建 | 修改的 JS 语法、Go 格式通过；正常开发入口 build-only 完成 Host、worker、Native 及 App 装配；Runtime 与媒体制品复用 |

本轮只改了 2 个产品源文件（政策及既有源加载器）和 2 个已有测试文件；其他 18 项变化是该 family 的生成物／来源记录，包括正常构建更新的 Native Skill 构建来源清单。构建前后检查了原工作区变化，所有其余已登记 dirty 文件保持，Git 状态路径未增加产品或测试文件；Runtime 仓保持干净。没有修改模型配置、用户提示、旧付费轨迹或上批评分。

首次正常构建在启动服务前识别到 API 镜像来源落后于同步后的候选生成物并退出 1，记录保留。按既有 `workflow-local.py build`／`up` 更新当前本地构建，再走原 build-only 入口成功；没有修改构建门禁或迁移文件，沿用现有正常启动、幂等迁移及保留数据流程。正常入口自带来源核验是本轮产品装配依赖，不另扩展 A0 或通用 QA。

最终构建 ID：`d6c749d9-3d14-4530-8542-ec1db6c72cdf`；worker：`540c21c6f0d6570e45369b2bc4097cc2db68a78810e561ad991cbb304473eff6`。原生协议验证使用这个 worker，Runtime 仍为 `e03bdbd2b4167022ee85c2df86dacff1a0a5c082321a9aa19875b29136a96cf5`。

## 复审结论与剩余边界

已关闭第 33 页指出的公共规则投影缺口，并消除了“只有发生应用检索时才需要 Pro”的措辞空隙。普通问答、指定 URL、研究过滤、已有证据复用、成功截断、权限拒绝及离线专家的影响均按当前实现核对；本轮不改变这些场景的执行机制。源政策缺少共享规则时 generator 明确失败，不静默生成不完整指导。

已经通过的是**产品接线及实际模型入口的规则交付**。尚未执行的是修复后的真实 MiniMax 自然研究选路；模型可能仍不遵循说明，不能由本机合成响应推断其成功率。原先两项实际截断 Fetch 的成功证据继续保留，本轮未机械重跑。MiniMax 答复误称“三次抓取”的独立真实性问题没有在此修复，也没有被包装成执行重试问题。

如需后续真实复验，应只针对尚未通过的 MiniMax 自然研究样本使用新的适用费用授权。若同源规则已完整交付而行为仍不满足标准，应重新判断产品入口／原生工具策略，不继续无限追加提示。公开分发、完整 Q2 和 FEAT-175 整体验收仍未完成。

回退只需恢复本轮政策与源加载器的先前内容，通过原 generator 同步后正常重建；保留数据库、历史和已完成操作，不回退 Runtime 或迁移。当前没有提交、推送或发布。

App、队列和模型均未启动。构建使用的自有服务已正常停止，活动委托 0、非终态检索 0，服务端历史操作仍为 7（无新增），本轮没有强杀、权限破坏、程序伪装或攻击 fixture。与本次变更无关的全量回归、旧 A0 和付费评测未运行，沿用用户要求的定向范围。

机器记录：[minimax-projection-fix-result.json](references/minimax-projection-fix-result.json)。本机源码差异、构建与原生协议日志位于工作区 `.local/feat175-minimax-projection-fix-20261116/`。
