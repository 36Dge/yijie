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

每次晋升都使用 PR，不在长期分支间直接 push。跨仓功能按 `yijie-contracts`、服务端、客户端的依赖顺序分别晋升。

## PR 与发布

PR 必须说明影响仓库、安全影响、API 契约影响、测试和发布说明。所有仓库独立发布；破坏性契约变更必须先设计迁移方案，不能通过跳过质量门禁发布。
