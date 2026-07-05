# 发布策略

## 发布节奏

| 仓库 | 发布方式 |
|---|---|
| yijie-desktop | 独立版本，Mac App 打包、签名、升级 |
| yijie-admin-web | 独立 Web 发布 |
| yijie-api | 后端服务发布 |
| yijie-agent-host | 跟随 Runtime / API 兼容性发布 |
| yijie-codex | 上游同步后发布 Runtime build |
| yijie-skills | Skill / Plugin 版本和灰度 |
| yijie-connectors | 按平台 API 变更和功能发布 |
| yijie-knowledge | 按知识库版本和检索服务发布 |
| yijie-contracts | 先于依赖方发布 |
| yijie-infra | 按环境变更发布 |

## 版本命名

```text
desktop-vX.Y.Z
admin-vX.Y.Z
api-vX.Y.Z
agent-host-vX.Y.Z
codex-yijie-vX.Y.Z
skills-vX.Y.Z
connectors-vX.Y.Z
knowledge-vX.Y.Z
contracts-vX.Y.Z
infra-vX.Y.Z
```

## 发布前检查

- [ ] Contract 兼容；
- [ ] Migration 可回滚；
- [ ] 高风险工具配置审批；
- [ ] 日志脱敏；
- [ ] 关键路径测试通过；
- [ ] 观测 dashboard 更新；
- [ ] Runbook 更新；
- [ ] Changelog 更新。
