# ADR-0009: Admin Web 作为独立仓库

## 状态

Accepted

## 日期

2026-07-04

## 背景

Admin Web 面向内部运营、权限、安全、知识库、插件和审计，与卖家桌面端的使用场景、权限模型和发布节奏不同。

## 决策

`yijie-admin-web` 独立于 `yijie-desktop`，不和桌面端共仓。

## 备选方案

放在桌面端仓库可以共享前端配置，但会造成边界混乱。

## 影响

- Admin 单独设计 RBAC 和审计入口；
- Admin 独立发布；
- 共享 API 类型通过 `yijie-contracts` 生成。

## 风险

设计系统可能分化，后续可按需要抽出共享 UI 包。

## 后续动作

- [ ] 初始化 Admin 权限模型文档；
- [ ] 定义 Admin API 契约。
