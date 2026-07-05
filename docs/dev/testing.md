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
./scripts/lint-all.sh
./scripts/test-all.sh
```

在子仓尚未初始化前，脚本会跳过未配置测试命令的仓库。
