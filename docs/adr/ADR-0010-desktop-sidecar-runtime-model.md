# ADR-0010: 桌面端 Sidecar Runtime 模型

## 状态

Accepted

## 日期

2026-07-04

## 背景

易界 AI 的卖家入口是 Mac 桌面端，需要在本地管理 Codex Runtime 和 Agent Host sidecar，同时也要支持未来云端 runner。

## 决策

桌面端通过 sidecar 管理 `yijie-agent-host` 和 Codex Runtime。`yijie-agent-host` 同时支持 desktop sidecar mode 和 cloud runner mode。

## 备选方案

所有任务都走云端 runner 可以简化客户端，但会降低本地体验和调试能力。

## 影响

- Desktop 负责 sidecar 进程管理和健康检查；
- Agent Host 统一抽象桌面和云端运行模式；
- Runtime build 需要可被 Mac App 打包、签名和升级。

## 风险

Mac 签名、notarize 和自动更新会带来发布复杂度。

## 后续动作

- [ ] 定义 sidecar 目录结构；
- [ ] 定义 runtime healthcheck；
- [ ] 定义桌面端发布流程。
