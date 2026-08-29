# FEAT-135 整体实现与调试记录

> 当前阶段：`D0 complete / implementation NOT STARTED`。本记录只固定后续方案与本轮治理事实，不声明任何实现或 D4 结果。

## 1. 整体实现方案

- 真实调用链：`ChatComposer` 用户意图 → `ChatPage` target-scoped draft/submit coordinator → `chat.store.ts` authority、canonical blocks 与 operation ID → 现有 Desktop private IPC → native SQLCipher atomic transaction/outbox → local durable response → FEAT-132/134 Timeline；Host/Runtime 后续状态异步进入既有 control-plane。
- 跨层实现顺序：先写 submission result、target draft 和 submit race 的纯 TypeScript/页面测试；再最小修改 Composer auto-grow/focus/状态；最后组合页面并回归 FEAT-127/128/132/133/134 authority。不得先改 Vue 文案伪造接受语义。
- Contract First 实施与验证：D0 只读矩阵结论为 `contract-impact=none`。后续不改 Contracts/Host/Runtime/private IPC/数据库；若任何测试证明必须改变这些边界，停止编码、重分类并申请新授权。
- 明确不做的生产加固：不做 public/production、应用重启后的未提交文本恢复、跨设备草稿、后台离线编辑、工具/文件操作、模型配置或 active Turn 控制。
- 草稿清空边界：仅在 native local durable response 回显当前 operation ID，且提交返回时 target/epoch 仍匹配时清空；pre-durable failure 保留，post-durable Host failure 不恢复。
- 防重复边界：同一 target + canonical ordered blocks 在 pending 期间只允许一个提交意图并重用 operation ID；不同 canonical input 必须获得不同 operation ID。

本 Profile 不建立治理切片。可以按技术依赖顺序编码，但最终以一个完整用户结果统一验收。

## 2. 实际改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| `yijie` | `docs/features/FEAT-135-desktop-codex-style-composer/` | 新增 schema v3 D0 治理包、工作区隔离记录与只读 Contract First 能力矩阵 | Owner 授权先完成正式 D0，不进入实现 |
| `yijie-desktop` | branch ref only | 从 clean FEAT-134 HEAD 创建 FEAT-135 分支；文件保持 clean | 隔离后续实现，当前禁止修改实现代码 |
| `yijie-contracts` / `yijie-agent-host` / `yijie-codex` | none | 无分支、文件、配置、binary、schema 或 Runtime 变化 | 只读审计结论无需跨仓 contract 变更，且 Owner 明确禁止创建这些分支 |

## 3. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复 | 结果 | 累计耗时 |
|---|---|---|---|---|---:|
| 2026-08-29 D0 | `ChatComposer` 已覆盖 Enter/Shift+Enter/IME，但 textarea 固定高度且无 focus API | 现有组件可复用键盘基线，缺口集中于 auto-grow、focus 和统一状态 | 本轮只登记到能力矩阵与 Must AC，不改代码 | D0 evidence captured | N/A |
| 2026-08-29 D0 | 已有会话 `submitTurn()` 可静默 `return`，`ChatPage` await 后仍无条件清空 `prompt` | `Promise<void>` 无法让页面区分 no-op 与 local durable acceptance | 推荐后续建立 Desktop 内部显式 submission result | D0 decision captured | N/A |
| 2026-08-29 D0 | Host OpenAPI 202 与 Desktop native response 容易被混称为 accepted | Desktop native 先完成 SQLCipher/outbox transaction 后返回，Host/Runtime 接受发生在异步 coordinator 后续 | 将 Composer 清空边界明确为 local durable confirmation | D0 semantic boundary fixed | N/A |
| 2026-08-29 D0 | 附件草稿已 target-scoped，而文本仅为页面全局 ref | 会话切换时纯文本可能串 target | 推荐 WebView 内 target map，不引入 durable migration | D0 design decision captured | N/A |

调试规则：30 分钟无新事实则停止猜测式补丁；90 分钟同一阻塞则简化方案；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP。

## 4. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 分支创建 | `yijie` 与 `yijie-desktop` FEAT-135 分支 | Owner / 2026-08-29 | 2 | 2 | PASS；均从指定 clean FEAT-134 HEAD 创建 |
| 付费 Provider prompt | N/A | 未授权 | 0 | 0 | NOT RUN；FEAT-134 额度不继承 |
| 破坏性操作 | N/A | 未授权 | 0 | 0 | NOT RUN |
| 生产写入/public 发布 | N/A | 未授权 | 0 | 0 | NOT RUN |
| `git add` / `git commit` / `git push` | 所有仓库 | 未授权 | 0 | 0 | NOT RUN |

没有启动 canonical、发送 prompt、调用工具、读写任务文件、修改系统设置、强杀进程、故障注入、破坏权限、替换 binary、重编译 Runtime 或使用攻击性 fixture。

## 5. 已知限制

- 所有实现、Must AC、focused tests、canonical smoke 与 D4 都尚未执行；本轮通过仅代表 D0 治理完整。
- 当前审计发现的 `ChatComposer` 重复附件移除 `@click` 属于既有实现缺口；不在 D0 修改，后续只有在 scoped diff 与测试证明属于 FEAT-135 时才能修复。
- WebView target-scoped 文本草稿方案不保证应用重启恢复；若未来要求 durable draft，需要独立 persistence/contract 治理。
- FEAT-135 `accepted` 只表示 Desktop local durable/queued；不能用此状态宣称 Host/Runtime 已接受或完成。
- 现有 active Turn Stop 是 predecessor 行为；FEAT-135 只保留 action slot，不重新定义或扩展其语义。
- 没有 Codex Desktop 人工 reference evidence；视觉方向是 Owner 接受的近似推测，不声明逐像素或版本一致。
