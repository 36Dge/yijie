# 文档产物目录

这张表回答三个问题：什么时候生成、解决什么问题、事实从哪里来。Codex 可以起草内容，但不得生成业务批准、commit、tag、digest、测试结果或生产状态等不存在的事实。

| 产物 | 生成时点 | 作用 | 生成方法 | 主要批准人 |
|---|---|---|---|---|
| `feature.yaml` | 步骤 0，持续更新 | 机器可读地索引 Owner、风险、仓库、不可变版本和门禁状态 | 脚本创建；从 Git、契约仓、CI 和发布平台回填真实值 | 技术负责人 |
| `00-feature-brief.md` | 步骤 0 | 固定问题、价值、范围、非目标和成功指标 | 需求负责人给事实，Codex 结构化整理 | 需求负责人 |
| `01-requirements.md` | 步骤 1 | 保存业务规则、状态、错误、数据和编号化 AC | 访谈/需求原文 → Codex 转为 Given/When/Then → 人确认 | 需求负责人 |
| `02-impact-assessment.md` | 步骤 2 | 防止改错仓、漏 consumer 或基于想象设计 | Codex 只读扫描规则、代码、Git、CI、契约和调用链 | 技术负责人/仓库 Owner |
| `03-decisions-and-risks.md` | 步骤 3 | 关闭安全、数据、架构、第三方和生产决策 | Codex列事实、选项与风险；有权 Owner 做选择并留证 | 架构/安全/数据 Owner |
| ADR（条件性） | 步骤 3/5 | 保存跨团队、高成本、难回滚的架构决策 | 与 Accepted ADR 比对；Codex 起草；架构 Owner 接受 | 架构 Owner |
| `04-contract-change-plan.md` | 步骤 4 | 固定权威源、语义、兼容方向、consumer 和发布顺序 | 从真实 Schema、owner、支持基线和生成器起草；逐 consumer 评审 | Contracts/Consumer Owner |
| 契约 Schema 与生成物 | 步骤 9 的首个切片 | 成为机器可验证的跨边界真相源 | 步骤 4 先评审设计；建立基线后只改权威源，用锁定 generator 生成并检查 drift/breaking | Contracts Owner |
| `05-technical-design.md` | 步骤 5 | 说明职责、数据流、状态、失败、安全、观测和恢复 | Codex 基于批准需求与真实代码起草；Owner 审查取舍 | 技术负责人 |
| Migration Plan（在 05 中） | 步骤 5 | 保证新旧应用/数据共存，并能暂停、恢复、前向修复 | 读取实际 schema/migration；采用 expand/backfill/switch/contract | 数据库 Owner |
| AI 行为设计（在 05 中） | 步骤 5 | 固定 model/prompt/tool/retrieval 边界和安全控制 | 从锁定版本与实际 runner 起草；禁止主观“试几次”定结论 | AI/业务 Owner |
| `06-test-plan.md` | 步骤 6 | 先定义如何证明正确，建立 AC→风险→测试映射 | Codex从 AC/风险/设计提取矩阵；独立测试视角补反例 | 测试/技术 Owner |
| Fixture/Dataset Manifest | 步骤 6 | 固定合成数据、canonical fixture 和 Eval 数据版本 | 在唯一权威位置创建，Feature 包只保存索引/引用 | 数据/测试 Owner |
| `07-implementation-plan.md` | 步骤 7 | 将大需求拆成可验证、可回滚的 Codex 原子切片 | Planner 只计划不改代码；按 contract→provider→consumer→activation 排序 | 技术负责人 |
| `08-verification-report.md` | 步骤 8–12，持续更新 | 防止口头“已通过”，保存 baseline、命令、退出码、SHA、AC 证据和独立审查 | 由真实终端/CI/Eval/测试输出回填；Codex 只总结，不伪造 | Verifier/Reviewer |
| Review Findings（在 08 中） | 步骤 11 | 打破实现上下文的确认偏误 | 新会话或独立 Agent 只读审查完整 diff、调用链和证据 | 独立 Reviewer |
| `09-release-and-rollback.md` | 步骤 13 | 控制制品、迁移、灰度、监控、停止和恢复 | 从目标环境真实配置、Dashboard 和控制面起草并演练 | 发布负责人 |
| Release Notes/Approval | 步骤 13 | 说明用户影响并保存组织审批 | 从最终 diff/版本生成；批准来自真实流程 | 业务/发布负责人 |
| `10-delivery-summary.md` | 步骤 14 | 保存实际生产版本、验收、观察、审计、遗留和关闭 | 从部署平台、监控、trace、审计和 Issue 系统汇总 | 需求/发布负责人 |

## 文档生成的统一规则

1. 先引用事实，再写结论：仓库、commit、文件、符号、命令、版本和 Owner 尽量精确。
2. 区分 `Fact / Assumption / Unknown`；未知项不得被 Codex 自动补成业务规则。
3. 条件性文档不能静默删除；写 `N/A + 理由`。
4. 计划和事实分开：计划中的命令、tag、环境不能被写成“已执行”。
5. 真实证据至少记录：时间、repository/cwd、完整 SHA、工具版本、命令、退出码、结果和日志/artifact 位置。
6. 文档与代码发生冲突时，停止并重新确认权威源；不能让实现悄悄改变需求。
