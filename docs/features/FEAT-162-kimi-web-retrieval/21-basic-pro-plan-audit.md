# FEAT-162 Basic / Pro 意图选择方案复审

> 2026-10-29续审：本文保留2026-10-28审计时点。A05的期限、A07的五用例/11模型/0.065元方案及“设计已关闭”结论已由[23号修订复审](23-requirements-gap-closure-reaudit.md)与当前22号替代；本文旧数字不是当前预算或验收标准。

日期：2026-10-28，Asia/Shanghai。审查性质：Codex对侧聊方案进行结构化自审，不宣称独立人工评审。Owner本轮指令：“再次认真审计上面的方案，审计后，按照易界需求治理规范落成 feat-162 需求。”本轮授权仅覆盖需求文档落盘及文档检查，不执行产品实现、跨仓生成、提交、激活或收费调用。

结论：原方案可作为增量方向，但不能直接按原文实施。以下遗漏已在[22号执行设计](22-basic-pro-intent-routing-plan.md)和当前需求主文件中修订。这里的“已关闭”仅指设计决策已补齐，不表示代码修复或真实验收通过。

## 1. 事实、冲突与未验证项

| 类别 | 事实及影响 |
|---|---|
| Fact | 当前代码只有kimi_web_search和kimi_web_fetch；Basic固定include_content=false，HTTP总上限15秒、上游搜索10秒。Pro和Basic正文模式均未实现。 |
| Fact | Contracts web-retrieval/1当前版本0.2.0，源加载器明确检查两工具集合及固定限额；不能只改Connectors端点而跳过源契约。 |
| Fact | Basic工具描述仍引导一般联网回答使用原生搜索；要实现选中Kimi连接器后问答优先Pro，必须更新同源描述。 |
| Fact | Broker审批最长60秒、租约最长300秒；consume_execution把call.deadline的剩余时间交给backend，审批等待和执行共用该期限。Host工具等待为60秒。 |
| Fact | 第20号真实客户端验收FAIL：模型4、Basic0、Fetch0，最新模型错误rate_limit_exceeded；三个未知用量预占保持。新增Pro不能被当作修复模型限流。 |
| Fact | 当前K3.1基线、Key复用及正常构建均存在；新扩展没有必要重建Agent循环、变更Runtime或再次迁移数据。 |
| Conflict | 原方案9次模型的完整验收没有覆盖新增Basic include_content=true；“Pro结果存在但chunks为空”与工具计费判据也未分开。 |
| Assumption | 在当前会话显式选用kimi-web且有有效权限时，模型选择Basic/Pro/Fetch；自动复用凭据不等于替用户选择连接器或自动批准。 |
| Unknown | 新Pro真实账号权限、模型意图选择质量、正常用户在期限内完成审批及实际服务时延，必须实施后验证；文档、mock或旧Basic/Fetch成功均不能替代。 |

工程定位：Contracts `scripts/web-retrieval-source.mjs`、`compatibility/web-retrieval/{tools.json,wire.schema.json}`；Connectors `worker/src/{kimi_web.rs,broker.rs}`；Host `internal/codex/market_turns.go`；Desktop现有连接器和审批入口。分支、完整HEAD、远端、既有dirty和原文件摘要见[落盘前记录](evidence/basic-pro-requirements-before-20261028.json)。元仓既有FEAT-165未跟踪目录保留，不属于本轮范围。

## 2. 审查发现与修订

| ID / 优先级 | 原方案缺口 | 本次设计修订 | 验收关联 |
|---|---|---|---|
| A01 / P1 | “普通查询默认Basic”不能覆盖官方对问答/RAG的Pro建议 | 按交付结果选择：列表/采集Basic，模型综合问答Pro，读取指定URL用Fetch；URL出现本身不等于读取意图 | AC-023 |
| A02 / P1 | 限站点/时间同时要求整页正文时，单个接口无法完整满足 | Pro筛选来源，再按需要Fetch；不得将未过滤的Basic结果冒充满足筛选，额外调用单独审批计量 | AC-023/025/030 |
| A03 / P1 | Basic新增text可能破坏旧严格reader，旧PASS不能直接继承 | 默认输入输出逐字结构保持；正文仅显式opt-in；新版本消费者就绪后激活，保留旧记录读取及兼容回退 | AC-022/024 |
| A04 / P1 | 仅因生成器断言两工具就宣称已证实wire breaking，证据不足 | breaking作为保守治理分类；真正检查请求/响应方向、工具资格快照、预算语义和旧消费者；不通过删除旧断言伪造兼容 | AC-022 |
| A05 / P1 | Pro 30秒参数与原15秒HTTP、审批执行共用60秒存在冲突 | 固定按工具预算，Pro/Basic正文为30/35秒；发送前检查所有剩余期限，预算不足零HTTP；不把执行预算加到过期批准之后 | AC-027 |
| A06 / P1 | 有搜索结果但无chunks，可能错误判免费或当成全文证据 | 空列表、缺正文、截断、工具失败分开；search_results非空的成功响应按收费可能性计账，正文不足单独提示 | AC-025/028/030 |
| A07 / P1 | 收费验收遗漏Basic正文模式，原9次不能覆盖全范围 | 增加该模式后完整最小集合为5会话，模型最多11、Basic3、Pro1、Fetch2；工具上界0.065元，模型预算另算且单独授权 | AC-024/030 |
| A08 / P1 | 隔离qualification或合成UI成功可能被误用为D4 | 隔离构建仅预检；D4必须在拟交付的canonical实际客户端入口、同源构建中完成fresh run与重开 | AC-029/030 |
| A09 / P1 | 同义重复、无理由Basic→Pro升级和原生搜索重复调用会增加成本 | 一项信息需求形成一个有效query；禁止盲目双搜；成功但证据不足可提出有意义的新调用，错误不自动换端点重试 | AC-023/026 |
| A10 / P2 | score和authority可能被解释成跨查询可信度，完整文本也可能被过度承诺 | score仅同次查询相对意义；authority原样保留不设未经证实阈值；正文是可提取文本且可截断，不承诺完整HTML或完整网页 | AC-025/028 |
| A11 / P1 | 新范围沿用旧implementation=complete、Must PASS会制造假完成 | 当前实现改为pending，新AC-021至030均pending；旧AC、原brief和feature快照保全，20号FAIL及账本不变 | 全部 |
| A12 / P2 | 缺少定位限流的供应商请求标识和HTTP200失败终态判定 | 模型、Basic、Pro、Fetch分别计量；保留受限错误码/请求ID/计数/耗时；模型HTTP200仍检查终态与usage，未知预占不释放 | AC-026/030 |
| A13 / P1 | 落盘期间共享Contracts/Host/Desktop出现FEAT-165相关dirty，旧clean快照已不代表当前工作树 | 保留全部并行改动，只记录前后状态；实施前重新核对准确来源与修改窗口，不恢复旧工作树或把新资源变更混入本需求 | AC-022/030 |

## 3. 取舍

采用三个独立MCP工具：旧Basic名称保持，新增Pro名称，Fetch保持。一个工具加mode虽能做，但会使旧Basic语义、审批名称和计费边界更容易混淆；额外分类模型或后台意图路由服务会增加费用及Agent编排，本次不采用。

Basic正文模式纳入本次，因为Owner提供的最佳实践明确包含采集/自行加工场景。它只返回文本，不执行入库或切块工作流。真实验收因此增加一个有界用例，不能在未验证时把它列为PASS。

工具描述是普通对话可见的运行规则入口；Skills仅承载确有必要的同源行为资产/评测/来源同步，不创建必须手动启用的额外技能，也不扩大既有专家来源权限。

## 4. 治理状态

沿用schema v3、demo_fast、local和FEAT-162身份。用户已授权本轮审计后落需求，Codex可完成产品/UX设计就绪自检和D0机器检查；这不是Owner对产品实现、真实调用、本地提交或日常激活的额外授权。D4保持未通过，DP为N/A。

本轮文档修改的contract-impact为none：未改变任何运行时wire、代码或持久化行为；文档所规划的产品扩展按breaking管理。所有产品开发、跨仓来源同步、构建、消费者资格、真实结果及模型选择评测仍为未执行。

## 5. 外部依据与证据边界

- Owner在本侧聊提供了“联网搜索最佳实践”全文；选择规则依据该全文，不将其中的“Token通常降低一个数量级”写成产品性能保证。
- 官方Basic：[tools-search](https://platform.kimi.com/docs/api/tools-search)。
- 官方Pro：[tools-search-pro](https://platform.kimi.com/docs/api/tools-search-pro)，已核对sites、time_window、chunks、空正文、错误码和诊断响应头。
- 官方Fetch：[tools-fetch](https://platform.kimi.com/docs/api/tools-fetch)。
- 官方价格：[websearch](https://platform.kimi.com/docs/pricing/websearch)，Basic0.01、Pro0.015、Fetch0.01元/成功有效次，模型费用独立。
- 文档索引llms.txt本次读取超时；不声称已完整读取索引，不因此触发任何供应商账户或收费接口。

本次结论只证明需求设计已复审；最终文档检查结果记录到02及requirements-checks证据，不由本报告预先声明成功。

最终保护检查的第一次整体不变断言因上述并行dirty而失败，未修改或回滚相关文件。随后将“本轮写入范围/历史证据保持”和“共享仓状态变化”分别记录；不能把这一检查失败抹除后宣称所有兄弟仓工作树不变。已核对的产品工具源事实仍有效，后续构建必须以届时准确来源重新冻结。
