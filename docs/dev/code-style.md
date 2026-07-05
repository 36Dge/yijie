# Code Style

## 通用

- 所有仓库保持小步提交；
- 公共 DTO、事件和 schema 不手写复制，统一从 `yijie-contracts` 生成；
- 示例数据必须是合成数据；
- 日志字段必须考虑脱敏。

## Go

- 使用仓库内 `gofmt`、`go test` 和 lint 配置；
- 模块化单体内按 domain、application、infrastructure、interfaces 分层。

## Vue / Tauri

- 页面逻辑、状态、API 调用和领域类型分层；
- 高风险操作必须经过显式审批 UI。

## Markdown

- ADR 使用统一模板；
- 安全文档必须明确边界和禁止事项。
