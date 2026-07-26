# 质量门禁

## Gate 0：需求可进入调查

- [ ] Feature ID、Owner、目标和非目标存在
- [ ] 初始 Git 状态已记录
- [ ] 真实数据、账户和外部副作用边界明确

失败处理：不开始代码修改。

## Gate 1：Ready for Design

- [ ] 用户场景和验收标准可判定
- [ ] 受影响仓库、producer、consumers 和权威源明确
- [ ] contract-impact 已分类
- [ ] 安全、数据、migration 和第三方影响已识别
- [ ] 阻塞问题已回答

失败处理：回到步骤 1—3。

## Gate 2：Ready for Implementation

- [ ] 重大决策已有确认或 ADR
- [ ] 公共契约设计已评审，权威源、基线、generator 和 consumer pin 计划明确
- [ ] 数据和部署兼容方案明确
- [ ] 技术设计覆盖失败、回滚和观测
- [ ] 测试计划映射全部验收标准
- [ ] 实现已拆成可独立验证的切片

失败处理：不得进入正式实现。允许隔离的 draft/spike，但必须标记不可发布。

### Gate 2A：Ready for Downstream Business Implementation（条件性）

当 `contract-impact != none` 时，G2 只允许先落地契约候选；provider/consumer 业务代码还必须满足：

- [ ] 权威契约源已由锁定 generator 生成
- [ ] lint、test、全部支持基线 breaking check 有真实结果
- [ ] 人工语义兼容与适用 Consumer Owner 评审完成
- [ ] 候选 version、完整 commit、digest 和 generator 可验证
- [ ] 每个下游已固定不可变引用，而非 dirty/floating sibling

失败处理：不得开始或合并下游业务实现。`contract-impact = none` 时写明可复核理由并标记 G2A 为 `N/A`。

## Gate 3：Slice Complete

- [ ] 只修改计划范围
- [ ] 测试先失败后通过，或记录无法 test-first 的理由
- [ ] 局部 lint/test/build/generate 通过
- [ ] 完整 diff 和 Git 状态已检查
- [ ] 没有手改生成物、未知依赖或真实敏感数据
- [ ] 验证报告已更新

失败处理：当前切片不能提交为完成。

## Gate 4：Code Complete

- [ ] 所有切片和验收标准实现
- [ ] Contract/migration/consumer pin 完整
- [ ] Unit、integration、conformance 和适用 E2E 通过
- [ ] 安全、失败和恢复场景覆盖
- [ ] 独立审查完成，P0/P1 清零
- [ ] 工作区干净，提交可独立审查

失败处理：不能声明“开发完成”。

## Gate 5：Production Ready

- [ ] 最终验证报告有实际命令和环境证据
- [ ] 制品、commit、tag、digest 可追溯
- [ ] migration、配置、secret 和权限准备完成
- [ ] 灰度、观测、告警和停止条件明确
- [ ] 回滚已验证或演练
- [ ] 生产批准真实存在

失败处理：不能发布或启用功能。

## Gate 6：Delivery Complete

- [ ] 部署与生产 smoke 成功
- [ ] 业务成功率、错误率、延迟和资源稳定
- [ ] 审计和安全记录完整
- [ ] 灰度观察窗口完成
- [ ] 文档、runbook、release notes 更新
- [ ] 已知限制和后续任务已登记

失败处理：需求保持“已部署、观察中”，不能关闭。

## 绝对禁止的“绿色”

以下结果不能替代完整门禁：

- 编译通过 ≠ 功能正确；
- Unit Test 通过 ≠ 集成正确；
- Mock E2E 通过 ≠ 真实依赖可用；
- Breaking checker 通过 ≠ 语义兼容；
- 部署命令退出 0 ≠ 服务 ready；
- 页面能显示 ≠ 后端已授权；
- Prompt 看起来合理 ≠ 模型质量通过；
- Codex 总结“已完成” ≠ 有验证证据。
