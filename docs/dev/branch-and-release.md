# Branch And Release

## 分支

- `main`：稳定主干；
- `feature/<scope>-<desc>`：功能；
- `fix/<scope>-<desc>`：修复；
- `docs/<scope>-<desc>`：文档；
- `chore/<scope>-<desc>`：工程化。

## PR

PR 必须说明影响仓库、安全影响、API 契约影响、测试和发布说明。

## 发布

所有仓库独立发布，但跨仓功能必须先发布 `yijie-contracts`，再发布依赖仓库。
