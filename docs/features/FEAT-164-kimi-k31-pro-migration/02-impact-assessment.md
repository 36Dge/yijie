# FEAT-164 影响评估

> 当前口径：原主工作目录构建/日常入口及正常系统退出资格以[76](76-primary-workspace-execution.md)、[77](77-primary-system-quit-root-cause-and-plan.md)和[当前验收矩阵](current-acceptance-matrix.md)为准。当前源码为原`CrossBSD/yijie-desktop`，generation `20261028-02`；71—74保留为上一来源/清理历史。新来源三轮服务/模型目录/正常退出/数据后态通过，App历史界面因锁屏按Owner指示跳过，未记PASS；既有接受替代和永久移除范围保持。

## 初始影响评估（历史规划；现状见当前矩阵）

拟实施 risk=high，contract-impact=breaking，database=migrate，persistence=replay，runtime=runtime，AI=model；UI/工作流可见。数据按confidential设计，不表示本轮读取用户私密数据。权限不扩张；grant失效/恢复仍必须显式评审。

本轮文档修改 contract-impact=none，无产品行为变化；不能用文档分类替代未来实现分类。

## 仓库影响

| 仓库 | 未来工作及边界 |
|---|---|
| Contracts | 模型源、活动/历史类型、market-selection/market-host/experts/scheduled传递依赖、Runtime身份投影；禁止手改SDK/伪pin |
| Runtime | 旧slug可达性、0006、必要最小补丁、独立候选和验证入口；不升级上游、不改canonical源树或覆盖旧binary |
| Host | catalog/default/effort、旧配置前身、准入、选择operation恢复、标题/草案/专家；不新建执行循环 |
| Desktop | UI/映射、追加私有迁移、各worker准入、计划/操作恢复、候选锁；不改旧0028、不删chat解阻 |
| Connectors | 共享Key/网页工具及来源组合回归；无主model ID替换，kimi-web不改名 |
| 元仓 | 审计/方案/验收/回滚材料；不实现业务代码 |
| API/Admin/Infra/Coze/Knowledge/Skills | 影响复核；不启用Coze模型/RAG，不改历史provenance或独立生图配置 |

本轮12仓完整HEAD/branch/origin/已有状态及tracked diff摘要见 [baseline](evidence/workspace-baseline.json)。该摘要不是完整工作树身份/发布pin。保护FEAT-162/163及现有dirty变更；后续实施重新采样、获Git授权后才能固化真实source。不能只按HEAD替换用户工作树。

## 数据约束

- Desktop catalog最多可读37，基础默认15、models入口29、connectors入口37；本轮未读用户实库version。0038是当前建议下一编号，执行前核对并行占用。
- 三表chat_model_selections/chat_operation_models/chat_plan_models只扩profile存储约束；全部原列/主键/FK/CASCADE/nullable与隐式唯一索引保持。
- operation_id刻意无outbox FK（首回合operation早于outbox），不得补上；没有发现引用这三表的额外外部FK/专属trigger/命名index。
- models-only 29→38经过30—37，需证明表结构升级不自动开启关闭的功能。
- Host bbolt新增恢复阶段字段如有必要须本仓版本化迁移；不把旧JSON语义暗改，不把服务私有表当中央业务DTO。
- 前向迁移无现成downgrade，新值写入后旧reader拒读；不能宣称直接旧App回滚。

## 前序需求

FEAT-156模型基础、FEAT-155计划/grant/recovery、FEAT-157/158/159市场/专家/实际artifact-media候选、FEAT-162共享Key、FEAT-163过程展示均为依赖或保护对象。新模型不继承它们的真实额度/通过状态，尤其不关闭FEAT-163当前FAIL/in_progress。
