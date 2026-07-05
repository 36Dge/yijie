# Secret Management

## 禁止

- 禁止提交真实密钥；
- 禁止在 `.env.example` 中写真实值；
- 禁止把 token 放入日志、fixtures、eval 数据集或 prompt 示例；
- 禁止让 Codex Runtime 直接读取平台 token。

## 要求

- 生产密钥使用云密钥服务或专用 vault；
- 本地开发使用假值；
- 连接器负责 token refresh、rotation 和审计；
- 所有 secret 访问必须有最小权限。
