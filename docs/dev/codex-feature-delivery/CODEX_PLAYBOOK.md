# Codex 实战操作规程

## 0. Profile-aware 工作方式

新需求默认 `demo_fast`。每次任务上下文先写明：

```text
delivery_profile: demo_fast | production_hardened
exposure: local | public
current_checkpoint: D0 | D4 | DP | G0...G6
```

`demo_fast` 上下文只需 Feature ID、用户结果、Must AC、交互/UI、真实入口、受影响仓库、
contract-impact、外部授权、focused checks、时间盒、当前真实 Bug 和已有工作区改动。不要求切片 ID、
G2V、harness、freshness 或 production evidence。

推荐的 Demo 整体实现任务：

```text
按已通过 D0 的 Brief 完成整个需求，不建立治理切片。

1. 契约影响先改权威源并运行适用 generate/lint/focused conformance。
2. 按技术依赖连续完成 provider/domain/storage/event/UI。
3. 只补保护 Must AC 和核心错误语义的 focused tests。
4. 完成后立即通过正常入口启动真实服务。
   对 `demo_fast + local`，正常入口必须采用 ADR-0018 canonical direct-entry，不要求用户登录。
5. 执行真实 happy path、全部 Must AC 和一个 failure/retry。
6. 有 Bug 就修复、重启、复测，直到一次 fresh run 全部通过。
7. 记录 Artifact、实际命令、diff 和已知限制；不得把 mock 写成真实服务。
```

Demo 调试使用时间盒：30 分钟无新事实则扩大真实调用链调查；90 分钟同一阻塞则简化方案；
非核心验证 120 分钟后登记限制；核心阻塞 240 分钟后缩小 MVP/换架构；16 小时未 D4 则重新定范围。

`production_hardened` 使用下述完整规程。

## 1. production_hardened 高质量上下文包

每次 Codex 实现任务至少提供：

- Feature ID；
- 当前步骤和切片 ID；
- 当前 G2V/harness qualification 状态；
- 目标与非目标；
- 验收标准；
- 允许/禁止修改范围；
- 相关仓库规则和架构路径；
- contract-impact、权威源和不可变引用；
- 安全与数据约束；
- 测试和验证命令；
- prerequisites、required local/boundary/vertical evidence 与 freshness 引用；
- 当前 Git 状态与已有改动；
- 当前同类失败 fingerprint、尝试次数与 circuit-breaker 状态；
- 明确的停止条件。

不要把整段历史聊天当作唯一上下文。优先引用 feature package 中已确认的文档。

## 2. 推荐的任务分解

### 调查任务

```text
只读调查，不修改文件。

根据 00—03 文档核对真实代码：
- 找到入口、数据流、producer/consumers、存储、测试和发布命令；
- 区分代码事实、文档声明和推断；
- 检查工作区已有改动；
- 识别契约、安全、migration 和环境阻塞；
- 输出文件路径、命令证据和待确认问题。
```

### 设计任务

```text
基于已确认需求和调查证据起草技术设计，不实现。

必须覆盖：
- 模块边界和依赖方向；
- 正常/失败时序和状态；
- 权限、租户、审批、审计；
- 事务、并发、幂等、超时、取消、重试；
- compatibility、migration、rollout、rollback；
- 测试和观测。

不要自行选择尚未确认的认证、数据库、供应商或生产策略。
```

### 单切片实现任务

```text
实现切片 <S1>；仅在 G2V 与 prerequisites 满足后开始。

目标：
范围：
禁止范围：
前置契约/commit：
Harness/G2V reference：
Required local/boundary/vertical evidence：
Structured freshness（transitive commits、contract/fixture refs、harness commit/digest、platform、bootstrap）与 invalidation rule：
验收标准：
验证命令：

工作方式：
1. 先复核相关代码、规则和工作区状态。
2. 先补充能失败的测试或说明为何不能 test-first。
3. 只做满足当前切片的最小改动。
4. 不修改生成文件；通过生成入口更新。
5. 运行局部验证并检查完整 diff。
6. 报告真实结果、未执行项和新风险。
7. 运行 `--gate G3 --slice <S1>`，不得用聚合 G3 覆盖切片事实。
8. 如果需要新决策或扩大范围，停止并请求确认。
```

### 测试任务

```text
根据 01-requirements.md 和 06-test-plan.md 检查测试缺口。

不要先看实现意图来降低断言。覆盖：
- happy path；
- 边界和格式；
- 权限/跨租户；
- 重复、并发和幂等；
- 超时、取消、断线、重试、部分失败；
- unknown enum/event/field；
- migration 和回滚 reader；
- secret/PII 脱敏。
- Temporal Contract Matrix 中 producer/commit/notify/replay/terminal/cleanup 的顺序不变量；
- runtime harness 的 product/harness/platform/gate failure classification；
- 最终 core vertical、accessibility/visual、teardown 三项独立 verdict。

输出每个测试对应的验收标准和失败时能发现的缺陷。
```

### 独立审查任务

```text
只读审查需求、设计、diff 和测试。不要修改文件。

优先寻找：
1. 会导致错误结果、越权、数据损坏或无法回滚的问题；
2. 契约、migration、部署顺序和 consumer 兼容问题；
3. 实现与验收标准不一致；
4. 测试和实现共享同一错误假设；
5. mock/placeholder 进入生产路径；
6. 缺失日志、指标、审计和失败恢复。

每个发现必须包含严重级别、证据、触发条件、影响和验证建议。
没有可行动发现时明确说明审查范围和残余风险。
```

### 发布证据任务

```text
根据实际命令输出更新 08—10 文档。

规则：
- 不得把未运行命令写成通过；
- 不得把静态检查写成集成验证；
- 不得把本地候选引用写成已发布 tag；
- 不得把部署命令成功写成服务 ready；
- 每个未执行项写原因、风险和补充条件。
```

## 3. production_hardened 小步循环控制

Codex 每轮最多承担一个主要认知目标，例如：

- 定义一个契约；
- 实现一个 use case；
- 增加一个 repository；
- 接通一个 handler；
- 完成一个页面状态机；
- 添加一组失败路径测试。

出现下列信号时应进一步拆分：

- 修改跨越三个以上职责层；
- diff 大到 Reviewer 无法一次理解；
- 同时新增依赖、migration、API 和 UI；
- 验证需要多个环境且无法独立运行；
- Codex 开始“顺便”重构无关代码。

## 4. 反幻觉规则

Codex 必须遵守：

1. 没有打开的文件内容，不当作事实。
2. 没有实际调用的工具，不声称执行。
3. 没有命令输出，不声称测试通过。
4. 没有远端 ref 校验，不声称已发布。
5. 没有真实环境 smoke，不声称生产可用。
6. 没有 Eval，不声称模型质量提升。
7. 没有用户授权，不访问真实账户、生产数据或付费服务。
8. 遇到冲突文档时核对 ADR 与代码，不静默选一个。

## 5. Diff 审查顺序

每个切片完成后按顺序查看：

1. `git status`：是否出现意外文件。
2. `git diff --stat`：范围是否符合计划。
3. `git diff --check`：空白和冲突标记。
4. 完整 diff：业务行为、错误、权限和数据。
5. 生成物 diff：是否来自正确 generator。
6. lockfile：是否有意新增依赖。
7. migration：是否滚动兼容且无危险隐式操作。
8. 测试：是否会在实现错误时真正失败。
9. 日志与错误：是否泄露 secret/PII。
10. 文档：是否与当前事实一致。

## 6. 并行 Agent 使用规则

适合并行：

- 一个 Agent 调查现有实现；
- 一个 Agent审查契约和兼容；
- 一个 Agent审查安全和测试缺口；
- 主 Agent整合结论。

不适合并行写同一文件或同一 migration。共享工作区时：

- 每个 Agent 的文件范围必须互斥；
- 开始和结束都检查 Git 状态；
- 主 Agent负责最终 diff、集成测试和冲突处理；
- 子 Agent 的结论仍需主 Agent核对。

## 7. Commit 与 Push

提交前：

- 一个 commit 只表达一个可审查目的；
- 生成物与对应源契约同提交；
- migration 与依赖它的代码按发布顺序组织；
- 不混入用户已有改动；
- commit message 总结行为，不写“AI generated changes”。

Push、创建 tag、发布、迁移生产数据和调用真实外部写操作都是外部状态变化，必须有明确授权和精确目标。

## 8. production_hardened 三次同类失败后的工作方式

同一命令、Gate、runtime checkpoint、稳定 failure code 或实质相同条件第三次失败时：

1. 立即停止重试、timeout 调整和局部补丁，标记 `RCA_REQUIRED`；
2. 汇总三次时序、相同/变化证据以及此前修复为什么未触及根因；
3. 扩大只读审计到完整调用链、平台、harness、规范和 checker；
4. 按 `Fact / Assumption / Unknown / Conflict` 重建判断；
5. 区分 `product_failure / harness_failure / platform_failure / gate_failure`；
6. 只提出一个有区分力的诊断或根因修复，列出停止条件和回滚；
7. 等待 Owner 批准后只执行一次。再次出现同类失败立即重新熔断。

禁止删除历史尝试、改名 failure code 清零、绕过 production path、伪造 evidence 或“重跑到绿”。

`demo_fast` 不使用三次失败冻结和 production failure ledger；它必须保留实际失败摘要，并按时间盒
转入真实调用链诊断、最小 workaround 或缩小范围。任何 Profile 都禁止机械“重跑到绿”。
