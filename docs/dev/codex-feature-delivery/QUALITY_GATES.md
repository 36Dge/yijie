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

## Gate 2：Ready for Contract/Vertical Candidate

- [ ] 重大决策已有确认或 ADR
- [ ] 公共契约设计已评审，权威源、基线、generator 和 consumer pin 计划明确
- [ ] Temporal Contract Matrix 覆盖 producer、持久化、通知、replay、terminal、cleanup 及 executable Test ID，或有 `N/A + Owner 理由`
- [ ] 每条 temporal invariant 已绑定适用 required slices，且每个 slice 有属于自身的 required TCONF
- [ ] 数据和部署兼容方案明确
- [ ] 技术设计覆盖失败、回滚和观测
- [ ] 测试计划映射全部验收标准
- [ ] 实现已拆成可独立验证的切片

失败处理：不得进入正式实现。允许隔离的 draft/spike，但必须标记不可发布。G2 PASS 也只授权
适用的契约候选和后续最小 G2V Walking Skeleton，不授权大规模业务实现。

### Gate 2A：Ready for Downstream Vertical Candidate（条件性）

当 `contract-impact != none` 时，G2 只允许先落地契约候选；provider/consumer 业务代码还必须满足：

- [ ] 权威契约源已由锁定 generator 生成
- [ ] lint、test、全部支持基线 breaking check 有真实结果
- [ ] 人工语义兼容与适用 Consumer Owner 评审完成
- [ ] 候选 version、完整 commit、digest 和 generator 可验证
- [ ] 每个下游已固定不可变引用，而非 dirty/floating sibling

失败处理：不得开始或合并下游候选实现。`contract-impact = none` 时写明可复核理由并标记 G2A 为
`N/A`。G2A 是进入最小 G2V candidate 的必要但不充分条件；在 G2V 前仍不得展开完整下游业务实现。

## Gate 2V：Vertical Feasibility（条件性）

以下任一条件成立时必须执行：风险为 high/critical、跨仓或跨进程、公共契约、持久化/重放、
Runtime/平台、认证/权限，或用户可见工作流语义发生变化。其他低风险任务只能由 Technical Owner
记录 `N/A + 可复核理由`，不得默认跳过。

G2V 前置顺序为 G2 → 适用的 G2A → runtime harness qualification。G2/G2A 只允许实现契约候选
和严格受限、默认安全的最小 Walking Skeleton，不授权大规模分层实现。

- [ ] 使用真实目标平台/Runtime，而非 browser-only 或 mock-only 替代
- [ ] 使用 production bootstrap、production entrypoint、真实路由/组合根和安全边界
- [ ] 使用最小代表性合成或已授权数据，不直接 seed DB/Store 绕过生产路径
- [ ] 至少穿过适用的 producer、边界、持久化、consumer 与用户可观察结果，并验证资源释放
- [ ] 阻断该门禁的 runtime harness 已固定不可变引用并独立资格验证
- [ ] harness 能以 closed、content-free 结果区分 `product_failure`、`harness_failure`、`platform_failure`、`gate_failure`
- [ ] 命令、环境、完整 commit、harness 引用、结果、时间和未覆盖风险已记录

失败处理：不得开始大规模业务实现。必须保留真实失败分类；harness/platform/gate failure 不得冒充
product failure，G2V PASS 也不得冒充最终完整 E2E。

## Gate 3/<slice-id>：Per-slice Complete

- [ ] 只修改计划范围
- [ ] prerequisites 均已 PASS 或有结构化、获批的 `N/A`
- [ ] 每个受影响仓库记录完整、不可变 commit
- [ ] 测试先失败后通过，或记录无法 test-first 的理由
- [ ] required local evidence 通过
- [ ] required boundary evidence 通过
- [ ] required vertical evidence 通过
- [ ] evidence 固定 source commits、contract/fixture/harness/platform 引用和验证时间，且仍 fresh
- [ ] 完整 diff 和 Git 状态已检查
- [ ] 没有手改生成物、未知依赖或真实敏感数据
- [ ] 验证报告已更新

`NOT RUN`、`FAIL`、`STALE`、未资格验证 harness 或与当前依赖 commit 集不一致的 evidence 均不得支持
PASS。G3 不再是可手写覆盖的全 Feature 聚合状态；每个切片通过
`--gate G3 --slice <slice-id>` 独立判定。

`feature.yaml` 是机器索引；每个 evidence ref 必须使用
`08-verification-report.md#<EVIDENCE-ID>`，并在验证报告中精确对应一个
`<!-- evidence: <EVIDENCE-ID> -->`。报告可保留未来切片的 `NOT RUN`，因此 G2V/G3 不以全文件
marker grep 代替定点 evidence 解析。结构化 YAML evidence 是机器判定权威，Markdown marker 只做
唯一的人类可读证据索引；两者冲突时不得以报告 prose 覆盖 YAML 门禁事实。

失败处理：当前切片不能记为完成，也不能启动依赖它的后续切片。

## Gate 4：Code Complete

- [ ] 所有切片和验收标准实现
- [ ] Contract/migration/consumer pin 完整
- [ ] Unit、integration、conformance 和适用 E2E 通过
- [ ] 最终 E2E 分别记录 `core_vertical`、`accessibility_visual`、`teardown`，全部适用 verdict 均 PASS 且 fresh
- [ ] 所有 required slices 的 per-slice G3 均 PASS 且 evidence 未失效
- [ ] 没有开放的三次同类失败熔断或未完成 RCA
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

## 三次同类失败熔断（适用于全部 Gate）

同一 Feature/Slice/Gate、evidence 或 harness ID、责任层、稳定 failure code/checkpoint 组成的实质相同
失败第三次出现时，门禁立即进入 `RCA_REQUIRED`：

1. 禁止第四次重试、自动 retry、延长 timeout、重命名 failure code 或继续局部补丁；
2. 允许扩大只读审计到完整调用链、平台、harness、规范和 checker，但不扩大写入授权；
3. 必须记录时间线以及 `Fact / Assumption / Unknown / Conflict`；
4. 必须区分 product、harness、platform、gate，提出可证伪候选和最小区分证据；
5. 只允许推荐一个下一诊断或根因修复，并由 Owner 明确批准后取得一次执行授权；每次授权、结果
   和 evidence 必须追加到 RCA cycle，不能覆盖前三次尝试；
6. 历史失败不得删除、改名或回写成“从未发生”。

修复后若再次出现同一实质失败，立即重新熔断，不重新获得三次机械重试额度。

## CI 声明审计

`pnpm test` 必须扫描所有 committed schema v2 Feature Package，并对每个已声明 PASS/N/A Gate 与
PASS slice 重放 semantic validator。门禁命令没有执行、evidence ref 不能唯一解析、freshness 失效或
存在开放熔断时，CI 必须失败；不得依赖 PR 作者自觉运行 checker。

CI 还必须以 PR/push base commit 为基线审计 `failure_circuit_breaker`：既有 incident identity、
attempt 和已记录 RCA cycle 不得删除或改写，只能追加新的真实记录。新建 Package 无历史基线时从
空 ledger 开始且必须直接使用 schema v2；后续提交不能以降级 schema、重命名、删除 YAML 或改写
旧 attempt 的方式重置三次失败计数。CI 无法取得不可变 base commit（包括全零 first-push base）时
必须 fail closed，不能退化为 current-only 审计。
