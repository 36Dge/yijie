# 快速开始

## 1. 创建需求交付目录

```bash
./scripts/new-feature.sh FEAT-123 task-history-export ./work
```

不要一开始就让 Codex “实现整个功能”。先把生成目录中的前八份文档补到足以评审。

## 2. 给 Codex 一个调查任务

第一轮只允许只读调查：

```text
目标：为 FEAT-123 建立实现前上下文，不修改任何文件。

请完成：
1. 读取仓库级 AGENTS.md、README、SECURITY、CONTRIBUTING 和相关架构文档。
2. 检查 git 状态、当前分支、现有未提交改动。
3. 查找现有实现、测试、契约、数据库和发布入口。
4. 列出受影响仓库、producer、consumers、数据流和安全边界。
5. 判断 contract-impact = none | additive | semantic | breaking，并说明理由。
6. 把确定事实和推断分开，列出必须由人确认的问题。

输出：用于更新 02-impact-assessment.md 的证据，不要实现。
```

## 3. 通过实现前门禁

编码前至少确认：

- 用户场景、目标、非目标和验收标准无歧义；
- 受影响仓库和已有用户改动已经记录；
- 契约影响、数据库影响、安全影响和发布顺序已经分类；
- 重大决策已有 ADR 或明确确认；
- 测试计划覆盖成功、失败、边界和回滚；
- 实现任务已经拆成可独立验证的小切片。

详见 [checklists/definition-of-ready.md](checklists/definition-of-ready.md)。

完成后执行结构化检查：

```bash
./scripts/check-feature-package.sh --gate G2 ./work/FEAT-123-task-history-export
```

脚本只检查文档结构和未完成标记；G2 仍必须由需求、技术及条件性安全/数据 Owner 根据真实证据批准。若 `contract-impact != none`，G2 后先落地并验证契约候选，通过 Gate 2A 后才开始 provider/consumer 业务代码。

## 4. 让 Codex 一次只实现一个切片

```text
实现 07-implementation-plan.md 中的切片 S1。

范围：
- 只修改：<文件或模块>
- 不修改：<明确排除>
- contract-impact：<分类与权威引用>

要求：
1. 修改前复核相关代码和测试。
2. 先补或更新能证明行为的测试。
3. 实现最小代码，不顺手重构无关区域。
4. 运行本切片对应的 lint/test/build/generate。
5. 检查完整 diff 和 git status。
6. 报告实际命令、结果、未执行项和剩余风险。

如果发现文档、契约或设计不成立，停止实现并说明阻塞。
```

## 5. 每个切片都执行闭环

```text
调查 → 计划 → 测试 → 实现 → 验证 → Diff 审查 → 更新证据
```

禁止把多个高风险模块一次性交给 Codex，再在最后统一测试。

## 6. 完成后做一次独立审查

最好开启一个新 Codex 任务，只给需求、设计和 diff，不给原实现对话中的辩解：

```text
作为独立 Reviewer 审查当前 diff，不修改代码。

重点查找：
- 与验收标准不一致；
- 权限、租户、PII、secret、审批或审计缺口；
- 并发、事务、幂等、超时、取消、重试和部分失败问题；
- 契约、migration、生成物或 consumer 兼容问题；
- 只验证 mock、没有验证真实生产路径；
- 测试与实现共享同一错误假设；
- 日志、指标、告警、灰度和回滚缺口。

按严重度输出可复现证据、文件和建议验证方法。
```

## 7. 发布前形成证据包

必须完成：

- `08-verification-report.md`
- `09-release-and-rollback.md`
- `10-delivery-summary.md`
- [checklists/production-readiness.md](checklists/production-readiness.md)

严格检查：

```bash
./scripts/check-feature-package.sh --strict <feature-package>
```

严格检查通过不代表代码一定正确，但缺失这些材料时不应宣称“生产就绪”。
