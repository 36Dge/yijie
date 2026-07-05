# Security Policy

## 密钥管理

禁止提交：

- 平台 access token；
- refresh token；
- cookie；
- private key；
- 数据库密码；
- OpenAI/API key；
- 云厂商 access key。

## 数据分类

- Public：公开文档；
- Internal：内部配置；
- Confidential：商家经营数据；
- Restricted：平台 token、PII、财务数据。

## 日志规范

日志必须脱敏：

- token；
- email；
- 电话；
- 地址；
- 订单号；
- 买家信息；
- 店铺敏感经营数据。

## 高风险操作

涉及价格、库存、广告预算、listing 发布、买家消息等操作必须经过审批。

## 漏洞响应

发现安全问题后必须通知 Security Owner，并创建 private security issue。
