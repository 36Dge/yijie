# Codex 生产级需求交付实践手册

这套手册用于指导团队以 Vibe Coding 方式使用 Codex 完成一个真实工程需求，从需求提出一直走到生产发布与线上验证。

它的目标不是让 AI “尽快写出能运行的代码”，而是让 AI 在明确边界、可验证证据和工程门禁下，稳定交付可维护、可测试、可回滚的生产级服务。

## 核心结论

> Vibe Coding 不是取消工程流程，而是让 AI 加速流程中的调查、设计、实现和验证。
> AI 生成的代码在通过契约、安全、测试、审查和发布证据前，一律视为未经验证的候选实现。

## 目录

- [QUICKSTART.md](QUICKSTART.md)：15 分钟上手路径。
- [HANDBOOK.md](HANDBOOK.md)：从步骤 0 到步骤 14 的完整实践手册。
- [DOCUMENT_CATALOG.md](DOCUMENT_CATALOG.md)：每份交付文档的作用、生成时点和事实来源。
- [CODEX_PLAYBOOK.md](CODEX_PLAYBOOK.md)：Codex 上下文组织、提示词和小步开发规程。
- [QUALITY_GATES.md](QUALITY_GATES.md)：Definition of Ready、Definition of Done 和生产发布门禁。
- `templates/feature-package/`：每个需求都可以复制使用的文档模板。
- `checklists/`：需求、编码完成和生产就绪检查清单。
- `scripts/new-feature.sh`：生成一个新的需求交付目录。
- `scripts/check-feature-package.sh`：检查需求交付目录的完整性。
- `examples/feature-package-example.md`：一个简化的只读导出功能示例。

## 推荐使用方式

在本手册目录中执行：

```bash
./scripts/new-feature.sh FEAT-123 task-history-export ./work
```

生成：

```text
work/
  FEAT-123-task-history-export/
    feature.yaml
    00-feature-brief.md
    01-requirements.md
    02-impact-assessment.md
    03-decisions-and-risks.md
    04-contract-change-plan.md
    04A-temporal-contract-matrix.md
    05-technical-design.md
    06-test-plan.md
    07-implementation-plan.md
    08-verification-report.md
    09-release-and-rollback.md
    10-delivery-summary.md
```

先补齐步骤 0—7 的文档和门禁。G2 只授权契约候选和严格受限的最小纵向
Walking Skeleton；适用 G2A 通过后，先资格验证 runtime harness，再用真实平台、
production bootstrap 和最小代表性数据通过 G2V。只有 G2V 通过或有明确 `N/A + Owner 理由`
后，才进入大规模业务实现。开发期间按 `G3/<slice-id>` 持续更新验证证据，发布后完成步骤 14。

推荐门禁顺序：

```text
G0 → G1 → G2 → G2A（条件性）→ Harness Qualification → G2V
   → G3/S1 → G3/S2 → ... → G4 → G5 → G6
```

G2V 是早期架构可行性证据，不替代 G4 前的完整 core vertical、accessibility/visual 和
teardown 三项独立 E2E verdict。

仓库 CI 会扫描 `docs/features/FEAT-*`：对 schema v2 中已经声明 PASS/N/A 的 Gate
以及每个 PASS slice 重新执行相应语义校验，并相对 PR/push base ref 审计 failure ledger 只可追加、
不得删除或改写。单包也可运行：

```bash
node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs \
  --audit-claims docs/features/FEAT-123-example

pnpm feature:audit -- --base-ref <BASE_COMMIT>
```

未声明的未来 Gate 不会被推断为 PASS；schema v1 只保留历史可读性。

检查结构：

```bash
./scripts/check-feature-package.sh ./work/FEAT-123-task-history-export
```

检查 G2 设计与切片计划门禁：

```bash
./scripts/check-feature-package.sh --gate G2 ./work/FEAT-123-task-history-export
```

检查早期纵向可行性与单个切片：

```bash
./scripts/check-feature-package.sh --gate G2V ./work/FEAT-123-task-history-export
./scripts/check-feature-package.sh --gate G3 --slice S1 ./work/FEAT-123-task-history-export
```

严格检查尚未填写的 `TBD`、`TODO`、`待补充`：

```bash
./scripts/check-feature-package.sh --strict ./work/FEAT-123-task-history-export
```

## 谁负责什么

| 角色 | 不可委托的责任 |
|---|---|
| 需求负责人 | 用户价值、优先级、非目标、验收口径 |
| 技术负责人 | 架构、数据、安全、兼容和发布决策 |
| Codex | 调查、草拟、实现、测试、生成证据和发现风险 |
| Reviewer | 独立检查正确性、边界、测试质量与回滚能力 |
| 发布负责人 | 环境、迁移、灰度、监控、回滚和线上确认 |

Codex 可以起草任何文档，但不得替人虚构业务决定、生产环境事实、测试结果或批准记录。

## 适用范围

适用于：

- 单仓或多仓功能；
- 前端、后端、桌面端、基础设施和 Agent/AI 功能；
- API、事件、数据库、缓存、工具协议和 SDK 变更；
- 需要模型 Eval、检索 Eval 或外部平台集成的功能。

对于纯文案、小型内部重构等低风险任务，可以合并部分文档，但不能省略影响分类、验收标准、验证证据和交付总结。

## Schema v2 与历史包

- 新建 Feature Package 使用 `schema_version: 2`，强制 G2V、per-slice G3、Temporal Contract
  Matrix、runtime harness qualification、拆分 E2E verdict 与三次同类失败熔断。
- 已存在于 CI base commit 的 `schema_version: 1` 包保留历史只读兼容；新建包使用 v1 会被 CI 拒绝，
  legacy checker 结果也不证明上述六项新门禁。
- v1 包在声明 G2V、G3、G4、G5 或 G6 前必须先做独立治理迁移；不得根据旧 Markdown 自动伪造
  vertical PASS、freshness 或历史失败记录。旧 checker 仅可读取历史结构，不能签发新的下游门禁。
- 活跃 v1 需求在完成当前已授权原子切片后、申请任何新下游门禁前迁移；已关闭包可保持归档。
- v2 的 evidence ref 使用 `08-verification-report.md#<EVIDENCE-ID>`，报告中必须存在唯一
  `<!-- evidence: <EVIDENCE-ID> -->`；commit、contract/fixture、harness commit/digest、平台和
  production bootstrap 由结构化 freshness 字段精确绑定。

迁移活跃 v1 包时必须在独立治理切片中完成：保护原工作树与历史失败 → 新增 04A → 把既有实现按
真实 prerequisite/commit 重建为 slices → 只迁移可追溯的 evidence，缺失项保持 `NOT RUN` → 建立
harness qualification、G2V 和三项 final E2E 的真实状态 → 由适用 Owner 复核。迁移不是把旧聚合
G3 自动抄成所有 slice PASS，也不得删除历史 failure ledger。
