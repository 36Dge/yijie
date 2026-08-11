# Contributing

## 开发流程

1. 从 `develop` 拉功能、修复或文档分支；
2. 新需求先使用 `docs/dev/codex-feature-delivery/scripts/new-feature.sh` 创建 `schema_version: 2` Package；历史 v1 包只读，不得复制；
3. 在 Package 中按 `docs/dev/contract-first.md` 标记 `contract-impact = none | additive | semantic | breaking`，完成 G0/G1/G2 和当前 Slice 需要的逐 Boundary G2C 后再修改业务实现；
4. 若为 `yijie-contracts` 治理的公共跨仓 wire 边界，先完成源契约、生成、全部适用基线兼容检查（尚无发布版本时使用已登记 fallback 完整 commit）和分级 consumer 评审；私有存储、部署接口、Runtime/第三方上游边界改走对应权威源及 migration/data/runtime/deployment compatibility；
5. 权威契约先形成不可变引用；公共 wire 下游 PR 在自身合并前固定引用、生成并增加 producer/consumer conformance，其它边界固定相应 migration/config/upstream 引用并验证受影响方；
6. 逐 Slice 完成 G3，整体完成 G4；staging/production 目标继续完成 G5/G6；
7. 运行测试和脚本检查，更新相关文档；
8. 提交 PR 并完成 Code Review；
9. CI、`feature-delivery/trusted-coverage-status` 和契约评审证据齐全后合并；尚未机器化的兄弟仓门禁由 reviewer 执行并如实记录。

长期分支晋升与 hotfix 流程以 `docs/dev/branch-and-release.md` 为准。
Contract First 的触发边界、兼容方向、例外和证据要求以
`docs/dev/contract-first.md` 为准。

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

- [ ] 新需求已创建 schema v2 Feature Package；已填写 Profile、Target、当前 Gate/instance 和 Authorization scope
- [ ] 实现路径由当前 G2 与适用 G2C/G3/G4 覆盖，Decision/Evidence 绑定当前版本且签名有效
- [ ] `feature-delivery/trusted-coverage-status` 已由预期 GitHub App 发布并通过
- [ ] 已填写 `contract-impact`；若为 `none`，已说明没有跨边界可观察变化
- [ ] 已链接适用权威源及不可变引用；公共 wire 已提供 contracts PR/tag/完整 commit 与全部适用 breaking 基线或 fallback，其它边界已提供 migration/data/runtime/deployment compatibility；不适用字段写 `N/A + 理由`
- [ ] 已列出 producer、全部已知/登记 consumers、分级评审/例外、下游 pin、合并/部署顺序及回滚
- [ ] 请求、响应、枚举和事件已按方向验证兼容，未把自动检查绿色当作端到端证明
- [ ] 公共 wire DTO 来自生成物或同源 validator，没有影子 DTO 或手改生成文件
- [ ] 是否更新测试
- [ ] 是否更新文档
- [ ] 是否涉及 DB migration
- [ ] 是否涉及安全边界
- [ ] 是否涉及高风险工具调用
