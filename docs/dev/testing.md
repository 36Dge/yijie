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
