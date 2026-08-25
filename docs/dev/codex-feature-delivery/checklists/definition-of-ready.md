# production_hardened Definition of Ready

> 仅适用于显式 `production_hardened`。默认 `demo_fast` 使用 `demo-fast-done.md` 中的 D0/D4。

只有以下项目全部满足，才可以从调查/设计和最小 G2V Walking Skeleton 进入大规模正式业务实现。
`N/A` 必须附理由。

## 需求与责任

- [ ] Feature ID、需求负责人、技术负责人、Reviewer、发布负责人明确
- [ ] 目标用户、问题、用户价值、范围和非目标已确认
- [ ] Must 需求均有编号化、可判定的验收标准
- [ ] 成功、失败、空数据、权限、超时、取消、重复和部分成功有预期
- [ ] 阻塞性 Open Questions 已关闭

## 代码与工作区事实

- [ ] 逐仓读取本仓 `AGENTS.md`、README、SECURITY、CONTRIBUTING 和相关 ADR
- [ ] 记录 remote、branch、完整 HEAD SHA、工具链与 `git status`
- [ ] 用户已有改动已标记归属并受到保护
- [ ] 入口、调用链、存储、测试、生成和发布命令来自真实代码/CI
- [ ] 每项改动有明确仓库和 Owner，没有按目录名猜职责

## 架构、契约与数据

- [ ] `contract-impact` 已在 `none/additive/semantic/breaking` 中分类并说明理由
- [ ] 权威源、producer、全部已知 consumers 和数据方向明确
- [ ] 公共契约先设计；无手写影子 DTO 或第二权威源
- [ ] Temporal Contract Matrix 覆盖 producer/persistence/notification/replay/terminal/cleanup 及 executable Test ID，或有 `N/A + Owner 理由`
- [ ] 兼容、版本 pin、合并、部署、启用和回滚顺序明确
- [ ] 架构变化有 Accepted ADR；不需要 ADR 时写明理由
- [ ] 数据 migration 使用 expand/backfill/switch/contract 思路
- [ ] 新旧应用与新旧数据的共存策略明确

## 安全、隐私与外部副作用

- [ ] 数据完成分类；测试数据为公开、授权或合成数据
- [ ] 认证、资源授权、租户隔离、secret 和日志脱敏已设计
- [ ] 高风险写操作有用户意图、审批、幂等、影响范围和审计
- [ ] 未知高风险写操作默认拒绝
- [ ] 第三方、模型、Runtime、费用、限流和生产账户事实已确认

## 测试与实施

- [ ] 每条 AC 和高风险项映射到测试/验证证据
- [ ] 测试计划包含 Unit、Integration、Contract/Conformance 和适用 E2E
- [ ] 安全、失败恢复、migration、性能、AI Eval 等专项已判定
- [ ] 实现拆成可独立验证、可回滚的切片
- [ ] 每个切片有允许/禁止范围、prerequisites、完整 commit 计划、local/boundary/vertical evidence、freshness、验证命令和停止条件
- [ ] 相关仓库 baseline 已执行，既有失败已单独记录
- [ ] runtime harness qualification 覆盖四类失败、positive/negative controls、timeout 与 cleanup
- [ ] G2V 适用性、真实平台、production bootstrap、最小代表性数据和 Walking Skeleton 已冻结

## Ready 结论

- [ ] G0、G1、G2 均通过
- [ ] 若 `contract-impact != none`，Gate 2A 的真实 generate/lint/test/breaking、语义评审和不可变 pin 已通过
- [ ] G2V 已 PASS；不适用时有 Technical Owner 的 `N/A + 可复核理由`
- [ ] 需求负责人确认业务语义
- [ ] 技术负责人确认实现可开始
- [ ] 高风险领域 Owner 完成条件性批准

任一项缺失：允许继续只读调查或隔离 Spike。G2 通过后可以执行契约候选；适用 G2A 后只允许
最小 G2V Walking Skeleton。大规模 provider/consumer 业务实现必须同时满足 G2V。
