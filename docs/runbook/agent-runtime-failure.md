# Agent Runtime Failure Runbook

## 快速判断

- Agent Host 是否启动；
- Codex app-server 是否可连接；
- `yijie_task_id` 与 `codex_thread_id` 是否建立映射；
- Skill 是否成功加载；
- MCP 工具配置是否生成；
- 事件流是否有 lag。

## 恢复

优先重启 Agent Host，再检查 Codex Runtime 版本和兼容性测试结果。
