# FEAT-131 — Codex 风格近似对话基线与黄金场景 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Checkpoint: `D4` · Created: `2026-08-26`
>
> Governance amendment `2026-08-30`：Owner-authorized FEAT-136 minimal Runtime repair 后 final re-freeze 为 `b2b20e2…` / 0.144.6；CAP-017 / GS-004 由新增 FEAT-144 承接。原 FEAT-131 D4 与 original freeze 证据保持历史，不重跑、不追溯改写。

## 1. Epic 总目标、用户问题与结果

- Epic 总目标：在保留 Vue 技术栈和固定 `yijie-codex` Agent Runtime 不变的前提下，使用户从输入、流式响应、过程更新、工具执行、权限确认，到中断、恢复和完成的端到端对话体验具有 Codex 风格且整体相近，同时遵守 Yijie UI 规范；不要求逐像素或逐状态完全一致。
- 目标用户：负责 active FEAT-132–137、FEAT-139–144 的产品、设计、开发和验收人员，以及最终使用易界 Agent 对话完成任务的本地用户。
- 当前问题：逐版本、逐场景采集 Codex Desktop 人工证据成本过高，会让参考取证替代真正的产品交付。
- Reference policy：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`。不建立 Codex Desktop version/build Freeze ID，不要求任何人工截图、录屏、hash 或 drift 跟踪。
- 本 Feature 的真实结果：后续 Feature 引用同一能力矩阵、13 个稳定场景 ID、推测策略和主动排除项，避免各自发明不兼容的交互模型。
- 完成边界：FEAT-131 只固定工程边界和近似目标，不实施生产对话交互；Epic 仍需后续 Feature 完成。

### In scope

- 固定 Runtime `0.144.6`、fork/upstream commit、schema tree hash 和 `experimentalApi=false`。
- 建立“推测的 Codex 风格目标 → Runtime → Host/Contracts → Desktop → Owner Feature”能力矩阵。
- 建立 13 个覆盖成功、失败、中断、恢复、历史、滚动和异常序列的稳定场景 ID；GS-006 作为明确排除的负范围记录保留。
- 仅在 Desktop 测试路径建立真实 parser/store 的确定性事件回放及 production bundle 隔离检查。
- 使用 Yijie UI 规范、当前实现和固定能力进行工程推测，不把推测写成版本专属实测事实。
- 保留 `pnpm tauri:demo-fast:stable` canonical local 验证入口：独立 bundle/data roots、MiniMax 文本 Provider、图片 dynamic tool 关闭、`experimentalApi=false`。

### Out of scope

- 不修改生产 Chat UI、路由、Tauri command、Host API、公共 wire 契约、数据库或持久化；FEAT-131 只建立基线资产与 local 验证入口。
- 不修改、升级、同步、重编译 `yijie-codex` Runtime 或开启实验 API。
- 不伪造 Runtime/Host 未提供的 Command、Tool、Approval、Steer 等生产事件。
- 不复制 Codex 源码、品牌资产、私有文案，不要求逐像素复刻或一模一样。
- 不要求或保存 Codex Desktop 人工参考证据；先前图 1、2、3 及派生资产均已撤回。
- Owner 明确不实现 8 项主动产品差异：语音、模型版本信息、模型推理强度信息、右上角分享、切换置顶摘要、显示侧边面板、分支到新聊天、GS-006 文件修改与 Diff；FEAT-138 已于 2026-08-29 从本 Epic 正式取消/排除。
- “模型推理强度信息”只指配置/档位 UI，不等于用户可见 reasoning summary；后者仍由 CAP-011 / GS-002 承接。
- GS-006 排除不删除既有 Artifact 能力，但不得把 Artifact 卡片包装成 FileChange/Diff。
- 不决定高风险审批或其他权限策略；不进行 public/production 发布、外部写或破坏性验证。
- 不修改 Host Runtime 管理器，也不通过故障注入验证其强制 Kill fallback。

## 2. 完整主流程

1. 实施者先读取 `reference-inference-policy.md`、固定 Runtime、Contracts、Host、Desktop 和 Yijie UI 规范。
2. 将每项行为标记为 `owner-approved-inference` 或 `intentional product difference`，不等待外部 UI 证据。
3. 使用固定四类 primary classification 归类能力，并单列 delivery lane、blocker 和 Owner Feature。
4. 将当前 Desktop wire 可表达的场景写为无敏感数据 fixture，通过测试内存 transport 进入真实 parser/store。
5. 执行重复回放、敏感数据扫描、policy ID 一致性和 production bundle 边界检查。
6. 通过 `pnpm tauri:demo-fast:stable` 核对 Runtime/Provider/`experimental_api=false`；真实 prompt 只能在明确授权与仓库级更严格调用上限内提交。
7. Active FEAT-132–137、FEAT-139–144 按场景和矩阵实现近似体验，并以 Yijie 规范、自动化检查、真实 local smoke 与 Owner 体验反馈验收；FEAT-138 不建包、不实施、不执行 D4；FEAT-144 独立承接 CAP-017 / GS-004。

## 3. 交互与 UI

- 视觉方向：Codex-inspired，但 Yijie-first。信息层级、流式/终态、可用动作和整体布局相近即可；颜色、间距、图标、文案和局部结构允许不同。
- 本 Feature 不改变生产 UI；后续生产 UI 以 `yijie-desktop/docs/design/docs/design` 为唯一设计规范。
- Idle：等待策略/矩阵核对或 test-only 回放。
- Loading：正在读取 Runtime/Contracts 或执行有界回放。
- Success：策略、主动排除项、矩阵、场景、Runtime freeze 和回放检查一致。
- Empty：没有人工参考媒体是预期状态，不是 blocker。
- Error：记录稳定错误与受影响 AC，不记录 secret、PII、路径或真实业务数据。
- Retry/Cancel：只重跑安全幂等检查，只使用应用自身停止/退出流程。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 固定 owner-approved inference 策略、近似而非完全一致标准、人工证据撤回和全部主动排除项 | policy + brief + matrix + scenario index |
| AC-002 | 精确记录 Runtime fork/upstream/version/schema 和 `experimentalApi=false` | manifest/checksum/HEAD 对账 |
| AC-003 | 13 个场景均包含目标行为或明确 exclusion；GS-006 为主动产品差异 | 场景表 + catalog ID/classification 测试 |
| AC-004 | 每项能力使用四类 primary classification 并包含交付层、阻断和 Owner | capability matrix 检查 |
| AC-005 | fixture 不含真实 prompt、路径、secret、PII 或商家数据；推测只在 catalog reference basis | fail-closed parser + sensitive-data scan |
| AC-006 | fixture 经真实 Desktop parser/store 重放且可重复；生产 bundle 不含测试入口 | focused Vitest + production build/dist scan |
| AC-007 | 仓库无撤回媒体、hash/manifest、旧 Freeze authority 或人工采集 gate；test-only 只锁 policy ID | 负向扫描 + policy consistency test |
| AC-008 | Runtime HEAD、schema tree 和 pin 实施前后不变 | git/status/hash/manifest 对账 |
| AC-009 | 隔离 canonical stable 入口保留文本 Provider、关闭图片 dynamic tool，以 `experimentalApi=false` 启动 | focused tests + `/v1/status` + 正常启动/Cmd-Q |

## 5. 工程事实与边界

- 受影响仓库：`yijie` 与 `yijie-desktop`；`yijie-codex` 严格只读。
- 分支基线：`yijie@bce5c1199513b6b4f6a0c5b82edf270efc9f69df`、`yijie-desktop@6745eb793e417c6685d1900231477c59ec81a5fd`。
- 真实入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`；使用独立 `com.yijie.ai.feat131-stable` 与 `.local/feat131-stable`。
- `contract-impact=additive`：公共 Contracts、Host API 和 Runtime schema 不变；fixture 与 policy 不是公共 wire/persistence 契约。
- 外部动作：predecessor 一次 UI submission 与当前 canonical 一次成功 submission 合计达到 `yijie-agent-host` 更严格的最多 2 次短请求上限；当前请求首轮精确返回 `FEAT-131_SMOKE_OK`，未调用工具、未重试，后续不再发送付费请求。破坏性操作、生产写、commit/push/tag/merge/发布均未授权。

## 6. 推荐方案与停止条件

- 使用测试内存 `ChatClientTransport → createChatClient → createChatStoreDefinition`，让 raw fixture 经过生产严格 parser、sequence/idempotency/resync 判断和 Store reducer。
- 只回放当前 wire 能表达的事实；不可投影能力登记 gap，主动排除能力登记 `intentional product difference`。
- 不因缺少 Codex 截图停止开发；实现不确定时优先 Yijie UI 规范、固定 Runtime/Contracts 和 Owner 最新反馈。
- 超过 16 小时则停止增加非核心格式，保留 13 个场景、能力矩阵、回放子集、bundle 隔离和精确排除项，不降低 Runtime 不变要求。
