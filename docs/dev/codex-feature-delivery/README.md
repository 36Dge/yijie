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
    05-technical-design.md
    06-test-plan.md
    07-implementation-plan.md
    08-verification-report.md
    09-release-and-rollback.md
    10-delivery-summary.md
```

先补齐步骤 0—7 的文档和门禁，再让 Codex 开始修改业务代码。开发期间持续更新验证证据，发布后完成步骤 14。

检查结构：

```bash
./scripts/check-feature-package.sh ./work/FEAT-123-task-history-export
```

检查“可开始业务实现”文档门禁：

```bash
./scripts/check-feature-package.sh --gate G2 ./work/FEAT-123-task-history-export
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
