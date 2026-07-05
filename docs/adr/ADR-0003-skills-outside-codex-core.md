# ADR-0003: Skills 放在 Codex Core 之外

## 状态

Accepted

## 日期

2026-07-04

## 背景

跨境电商领域能力变化快，包括 Listing、广告、合规、物流和经营分析等 Skills。

## 决策

领域 Skills、Plugins、Prompt Packs 和 Evals 统一放在 `yijie-skills`，不写入 `yijie-codex`。

## 备选方案

把 Skills 写进 Runtime 仓库可以减少集成工作，但会污染上游 fork，增加升级难度。

## 影响

- Runtime 保持通用；
- Skills 可独立评测、灰度、发布；
- Agent Host 负责加载 Skills。

## 风险

Skills 与 Runtime 协议变化需要兼容性测试覆盖。

## 后续动作

- [ ] 定义 Skill 包格式；
- [ ] 定义 Skill eval 和发布流程。
