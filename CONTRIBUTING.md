# Contributing

## 开发流程

1. 从 `main` 拉分支；
2. 修改代码或文档；
3. 运行测试和脚本检查；
4. 更新相关文档；
5. 提交 PR；
6. Code Review；
7. CI 通过后合并。

## 分支命名

- `feature/<scope>-<desc>`
- `fix/<scope>-<desc>`
- `chore/<scope>-<desc>`
- `refactor/<scope>-<desc>`
- `docs/<scope>-<desc>`

## Commit 规范

- `feat:` 新功能
- `fix:` 修复
- `docs:` 文档
- `refactor:` 重构
- `test:` 测试
- `chore:` 工程化
- `security:` 安全修复

## PR 检查项

- [ ] 是否更新测试
- [ ] 是否更新文档
- [ ] 是否涉及 API contract
- [ ] 是否涉及 DB migration
- [ ] 是否涉及安全边界
- [ ] 是否涉及高风险工具调用
