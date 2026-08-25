# demo_fast DP：公开 Demo 最小检查

只在 `exposure: public` 使用，并以 D4 PASS 为前置。

- [ ] secret 仅在服务端环境或 Keychain，不进入客户端、源码、日志和错误
- [ ] 鉴权与数据边界适合公开访问，或服务不处理受保护数据
- [ ] 输入、文件、URL、大小和超时有边界
- [ ] 付费 API 有频率、并发和成本上限
- [ ] 错误不泄露敏感信息、凭据或调试栈
- [ ] 有最简停止/恢复方式
- [ ] 公网入口真实 smoke PASS

付费用户、SLA、多租户/PII、重要持久数据、不可逆 migration、合规或组织级生产责任必须升级到
`production_hardened`，不能以本清单代替生产治理。
