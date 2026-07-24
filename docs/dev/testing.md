# Testing

## 测试分层

| 类型 | 主要仓库 |
|---|---|
| Unit Test | 所有仓库 |
| Integration Test | API、Agent Host、Connectors、Knowledge |
| Contract Test | Contracts、API、前端、连接器 |
| E2E Test | Desktop、Admin |
| Runtime Compatibility Test | Codex、Agent Host |
| Skill Eval | Skills |
| Retrieval Eval | Knowledge |
| Security Test | API、Connectors、Infra |

## Workspace 检查

```bash
make lint
make test
make generate
```

统一脚本要求 `repos.yaml` 中的仓库和 Makefile 全部存在；缺失仓库或缺失质量命令会失败，不再静默跳过。Infra 始终执行静态 Compose 模型校验，有 Docker 时额外执行 `docker compose config`。

Codex fork 管理骨架与 Runtime 源码测试分开：`make test` 校验当前管理骨架，源码接入后使用 `make runtime-test` 执行兼容性测试。

## Contract First 验证

以下四层适用于 `yijie-contracts` 治理的公共跨仓 wire 边界，任何一层绿色都不能替代
其它层：

1. **源契约结构**：OpenAPI、Protobuf、AsyncAPI 和 JSON Schema lint；
2. **生成与漂移**：从权威源重新生成，工作区不得出现未提交差异；
3. **版本兼容**：相对所有仍受支持或处于生产兼容窗口的 tag + 完整 commit 逐一执行 breaking check，并人工审查语义变化；尚无发布版本时使用契约仓登记的 fallback 完整 commit，禁止零基线放行；
4. **实现符合性**：producer 验证实际请求、响应和事件符合契约，consumer 验证未知字段、未知枚举/事件、失败与版本不兼容路径。

公共 wire 下游测试必须记录不可变 contract tag/完整 commit 和可用时的 digest。
从 dirty sibling 工作树生成只允许用于本地候选验证，不能作为发布证明。独立 CI
因缺少 sibling 而跳过的兼容测试必须明确报告为未完成。

私有存储、部署接口、Runtime 和第三方上游边界不伪造 contracts breaking 结果，分别
记录 migration/data、deployment、双向 Runtime 或 adapter/upstream compatibility，
固定各自权威源引用，并验证受影响方与回滚路径。
