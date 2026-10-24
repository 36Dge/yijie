# FEAT-164 实施记录

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

Owner当前消息明确确认方案并要求实施、保留工作树、遵守安全条款及完成后审计验证。记录时间以evidence/implementation-baseline.json为准；不伪造独立Reviewer或发布批准。

## 当前阶段

G0/G1/G2：用户确认方案并允许实施；执行机器门禁后记录结果。G2A/G2V及S1—S4均未通过。先做业务源契约和最小独立Runtime候选，不提前改Host/Desktop日常执行。整体contract-impact=breaking。

## G2设计具体化

采用独立model-selection-v2 schema、chat-models-v2 family 0.2.0 candidate与/v2/model-chat路由；现有v1源及其consumer不变。Known ProfileId包含旧K3及两活动身份，ActiveProfileId仅新Kimi/MiniMax。Selection新增独立availability，unknown仍表示执行结果不确定；旧operation走独立只读receipt，不能以旧SelectRequest再执行。

Runtime保留0001—0006字节，新增0007仅用于新候选：新slug搜索sources与旧slug出站拒绝，正常工具/SSE补丁沿用。独立构建路径，不覆盖旧binary；上游版本、schema、权限不变。该底层拒绝保护辅助调用，但不能代替Host/Native迁移与worker准入。

## 仍需真实证据的边界

G2A需要真实不可变candidate提交/consumer pin和已生成diff评审；当前没有Git授权，不创造commit或假pin。付费真实G2V及终验需本Feature预算；日常库先有兼容回退资格。所有既有未提交变更按implementation-baseline保留。

## 2026-10-24 源候选完成

- 已新增Contracts独立模型v2源、SDK/离线API bundle/来源锁、普通契约回归与离线基线比较工具。
- 已新增Runtime0007、新构建/manifest入口和独立kimi-k31-pro-r1；真实构建及正常stdio退出通过，原上游/0001—0006/旧制品未改。
- 已从实际制品生成独立runtime-kimi-k31-pro投影，未sync Host/Desktop、未改日常入口或用户库。
- 实现后再次审计修复旧v1回执版本、availability一致性、转发错误声明和SDK枚举重复问题；最终限定检查及7基线离线比较通过。
- 真实失败/未执行项均见08；原breaking入口与Runtime make test没有伪记PASS，Owner审阅与不可变提交仍欠缺。下一步入口14，不提前进入S1—S4。
