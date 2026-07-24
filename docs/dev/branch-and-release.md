# Branch And Release

## 长期分支

- `main`：生产基线，只接受从 `staging` 晋升的发布 PR 和紧急 hotfix；
- `staging`：预发基线，只接受从 `develop` 晋升的候选版本和 hotfix 回灌；
- `develop`：日常集成基线，功能与常规修复 PR 的默认目标。

三个长期分支都必须启用保护规则：禁止直接 push、要求 PR、要求 CI 通过、要求分支在合并前保持最新，并禁止 force push 和删除。

## 短期分支

- `feature/<scope>-<desc>`：从 `develop` 创建，合回 `develop`；
- `fix/<scope>-<desc>`：从 `develop` 创建，合回 `develop`；
- `docs/<scope>-<desc>`、`chore/<scope>-<desc>`：从 `develop` 创建；
- `hotfix/<scope>-<desc>`：从 `main` 创建，先合回 `main`，随后同步到 `staging` 和 `develop`。

## 晋升流程

```text
feature/fix -> develop -> staging -> main -> version tag
hotfix      -> main -> staging + develop
```

每次晋升都使用 PR，不在长期分支间直接 push。跨仓功能遵循
`docs/dev/contract-first.md`：契约先形成不可变可消费引用，每个下游 PR 在自身合并前
固定引用；功能启用和 producer 发值顺序按请求/响应/事件方向决定。
Codex Runtime 和第三方平台协议按各自上游权威源先形成候选，再进入易界兼容投影。

## PR 与发布

PR 必须说明影响仓库、安全影响、`contract-impact` 分类、权威源、不可变引用、
producer/consumers、测试和发布说明。公共跨仓 wire 边界还必须列出契约 tag/完整
commit 和全部适用 breaking 基线（尚无发布版本时为已登记 fallback 完整 commit）；
其它边界列出相应 migration/data/runtime/deployment compatibility，并把不适用的
contracts 字段写为 `N/A + 理由`。所有仓库独立发布；下游实现 PR 在适用权威源可消费
并在该 PR 中完成精确 pin 前不得合并。

增量请求能力按“provider 先支持、consumer 后使用”发布；新增响应字段、枚举和事件
必须先确认旧 consumer 容忍或先升级 consumer。兼容的 semantic 变化需人工评审和
分阶段发布；若使任一受支持交互失效则升级为 breaking，并采用 expand/新版本、双轨、
consumer 迁移、观测、弃用和清理，不能通过跳过门禁或多仓硬切发布。
