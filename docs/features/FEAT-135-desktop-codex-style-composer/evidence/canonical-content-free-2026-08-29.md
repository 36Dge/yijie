# FEAT-135 canonical content-free D4 证据

> Final source: `yijie-desktop@fc52ef33cdf040d9b6e8d71bd7498811c5c38c51` · Captured: `2026-08-29` · Content policy: no prompt/reasoning/final body persisted

## 1. 启动事实

- 入口：`pnpm tauri:demo-fast:stable`
- Profile/exposure：`demo_fast / local`
- 路由：零登录直达 `tauri://localhost/chat`
- Host：`service=yijie-agent-host`、`status=ok`
- Runtime：`state=ready`、`ready=true`、`runtime_version=0.144.6`、`model=MiniMax-M3`、`model_provider=minimax`、`transport=stdio`、`experimental_api=false`
- Runtime source identity：upstream tag `rust-v0.144.6`、upstream commit `5d1fbf26c43abc65a203928b2e31561cb039e06d`

## 2. 真实提交事实

- Owner 在最终发送动作前明确确认“发送”。
- Provider/付费动作：1/1；无自动重试。
- 输入：无敏感纯文本；要求禁止工具调用和任务文件读写。本文不保存、哈希、复述输入正文。
- 结果：进入新 session，Composer 清空，当前 Turn 终态 `completed`。
- 脱敏 session ref：`01a04ce5-836b-7272-a91e-252d61efd5c6`。
- 未保存、哈希或复述 reasoning、plan、final 正文。

## 3. 失败与重试证据

代表性 failure/retry 由最终源码 deterministic tests 提供：deny/no-op/throw、operation mismatch、stale target/route race、duplicate intent、unchanged-input operation reuse、post-durable failed/interrupted。全部使用正常生命周期和合成非敏感 fixture；没有强杀、故障注入、权限破坏、binary 替换或攻击性输入。

## 4. 退出与保护事实

- 两次 canonical 进程均使用应用自身 Cmd+Q 正常退出；第一次在 submit 前因桌面自动化焦点陷阱重启，Provider 调用为 0。
- 最终 runner exit 0；App、Host、Runtime 与 TCP `127.0.0.1:18081` listener 均已清理。
- 收口对账：Desktop `fc52ef33...`、Contracts `3832a6c5...`、Host `b9358f06...`、Runtime `0ce5902e...` 均 clean；未 push。

## 5. Waiver

- AC-001 人工视觉复验：`WAIVED / NOT REQUIRED`（Owner 2026-08-29 指令）；不是 PASS。
- reduced-motion：`WAIVED / NOT REQUIRED`；不是 PASS。
- AC-001 自动化部分：auto-grow、max-scroll、底部 actions 不重叠、窄布局发送列由 `ChatComposer.test.ts` 先红后绿并在 22/22、focused 141/141、full 872/872 中通过。

该证据仅支持 FEAT-135 `demo_fast + local` D4，不声明 public/production、逐像素 Codex Desktop 一致、已 push 或完整 Epic 完成。
