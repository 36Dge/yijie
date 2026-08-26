# FEAT-131 — Codex Desktop 对话一致性基线与黄金场景 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Checkpoint: `D0` · Created: `2026-08-26`

## 1. Epic 总目标、用户问题与结果

- Epic 总目标：在保留 Vue 技术栈和固定 `yijie-codex` Agent Runtime 不变的前提下，使用户从输入、流式响应、过程更新、工具执行、权限确认、文件变更，到中断、恢复和完成的端到端对话体验，与冻结基线版本 Codex Desktop 保持可观察的行为一致。
- 目标用户：负责 FEAT-132–143 的产品、设计、开发和验收人员，以及最终使用易界 Agent 对话完成任务的本地用户。
- 当前问题：“与 Codex Desktop 一致”仍是会随参考客户端更新而漂移的主观描述；当前 Host 投影又少于固定 Runtime 的稳定能力，无法客观判断每个差异应由哪一层负责。
- 本 Feature 的真实结果：后续 Feature 可引用唯一的版本身份、能力矩阵、黄金场景 ID、证据状态和可重复 test-only 回放，避免各自发明不兼容的交互模型。
- 完成边界：FEAT-131 只冻结基线，不实施生产对话交互；基线冻结后 Epic 仍未完成。

### In scope

- 冻结 Codex Desktop `26.818.61809` build `7019`、冻结日期和可取得的环境证据。
- 冻结 Runtime `0.144.6`、fork/upstream commit、schema tree hash 和 `experimentalApi=false`。
- 建立“Codex 可观察行为 → Runtime → Host/Contracts → Desktop → Owner Feature”能力矩阵。
- 建立至少 13 个覆盖成功、失败、中断、恢复、历史、滚动和异常序列的黄金场景。
- 仅在 Desktop 测试路径建立真实 parser/store 的确定性事件回放及 production bundle 隔离检查。
- 无法由安全自动化观察的 Codex 交互明确标记 `reference-unobserved`。
- 新增 `pnpm tauri:demo-fast:stable` canonical local 验证入口：使用独立 bundle identifier、Desktop app-data 和 Host/Codex home，保留 MiniMax 文本 Provider、关闭图片 dynamic tool，并以 `experimentalApi=false` 启动固定 Runtime。

### Out of scope

- 不修改生产 Chat UI、路由、Tauri command、Host API、公共 wire 契约、数据库或持久化；仅允许增加受限 local launcher 与既有 Provider 环境的 Sidecar 投影。
- 不修改、升级、同步、重编译 `yijie-codex` Runtime 或开启实验 API。
- 不伪造 Command、Tool、Approval、Diff、Steer 等尚未投影的生产事件。
- 不复制 Codex 源码、品牌资产、私有文案或逐像素实现。
- 不决定审批、文件写入或其他高风险权限策略。
- 不进行 public/production 发布、外部写或破坏性验证；真实模型调用仅限当前用户明确授权的一次 UI submission，不自动重试。
- 不修改 Host 的 Runtime 管理器，也不通过故障注入验证其 shutdown timeout/protocol failure/startup abort 的强制 Kill fallback；该风险只登记为限制。

## 2. 完整主流程

1. 实施者从 canonical `demo_fast` local 环境开始，以只读命令核对参考 App、Runtime、Contracts、Host 与 Desktop 当前事实。
2. 对每个参考行为记录 observation status 和 provenance；无法安全获取时写 `reference-unobserved`，不凭记忆补造。
3. 使用固定四类 primary classification 归类能力，并单列 delivery lane、blocker 和 Owner Feature。
4. 将可由当前 Desktop wire 表达的场景写为无敏感数据 fixture，通过测试内存 transport 进入真实 `parseChatProjectionEvent` 和 Chat Store reducer。
5. 连续回放、敏感数据扫描、版本漂移和 production bundle 边界检查通过后，记录 D4 证据。
6. 从 `pnpm tauri:demo-fast:stable` 启动隔离 identifier/data roots 的注册 debug App，先核对 `/readyz` 与 `/v1/status` 的 Runtime/Provider/`experimental_api=false`；仅在存在未使用的明确授权时执行单次 UI smoke，并用应用自身退出流程清理。
7. Owner 冻结基线；FEAT-132–143 引用场景 ID 逐步交付完整 Epic，不静默改写旧观察。

## 3. 交互与 UI

- 视觉方向：本 Feature 不改变生产 UI；Codex 截图/录屏仅作内部脱敏参考。未来生产 UI 仍以 `yijie-desktop/docs/design/docs/design` 为唯一规范。
- Idle：等待只读采集或 test-only 回放。
- Loading：正在读取版本元数据或执行有界内存回放。
- Success：基线身份、矩阵、场景、证据索引、回放和 Runtime freeze evidence 齐全。
- Empty：无法观察的参考场景显示为 `reference-unobserved`，包含原因、影响和 Owner。
- Error：记录稳定错误与受影响验收项，不记录绝对路径、正文、secret、PII 或商家数据。
- Retry：只重跑安全、幂等的读取、测试和正常应用启动。
- Cancel：只使用应用自身的停止/退出流程；禁止强杀、权限破坏、二进制替换和攻击 fixture。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 记录 Codex Desktop `26.818.61809`、build `7019`、冻结日期、环境和证据状态 | Info.plist 只读证据 + evidence index |
| AC-002 | 精确记录 Runtime fork/upstream commit、版本、schema tree 和 `experimentalApi=false` | manifest/checksum/HEAD 对账 |
| AC-003 | 至少 13 个场景包含前置、操作、状态、动作、结果、provenance 和观察状态 | 场景表 + fixture ID 测试 |
| AC-004 | 每项能力使用四类 primary classification 之一并包含交付层、阻断和 Owner | capability matrix 检查 |
| AC-005 | fixture 不含真实 prompt、路径、secret、PII 或商家数据 | fail-closed parser + sensitive-data scan |
| AC-006 | fixture 经真实 Desktop parser/store 重放且可重复；生产 bundle 不含测试入口 | focused Vitest + production build/dist scan |
| AC-007 | 参考 App 漂移时保留冻结版本，除非 Owner 新建 baseline | drift test + 变更规则审查 |
| AC-008 | Runtime HEAD、schema tree 和 pin 实施前后不变 | 前后 git/status/hash/manifest 对账 |
| AC-009 | 隔离 canonical stable 入口保留文本 Provider、关闭图片 dynamic tool，以 `experimentalApi=false` 启动；stable-only 第二实例 fail closed，Desktop supervisor 不使用 `kill_on_drop/start_kill` | launcher/config/Rust focused tests + `/v1/status` + 隔离注册 App 正常启动/Cmd-Q；不包含 Host 内部 fallback 保证 |

## 5. 工程事实与边界

- 受影响仓库：`yijie`（Feature Package）和 `yijie-desktop`（test-only fixture/harness、stable local launcher/config、stable-only second-instance 分支、既有 Provider 的受限 Sidecar 投影及 consumer pin）；`yijie-codex` 只读，不列为修改仓。
- 分支基线：`yijie@bce5c1199513b6b4f6a0c5b82edf270efc9f69df`、`yijie-desktop@6745eb793e417c6685d1900231477c59ec81a5fd`，均从用户授权的 `feat/feat-131-desktop-codex-parity-baseline` 开始。
- 真实入口：`cd ../yijie-desktop && pnpm tauri:demo-fast:stable`；它 freshly build 并启动 `com.yijie.ai.feat131-stable` debug `.app`，使用 `.local/feat131-stable` Host/Codex home，必须正常启动和退出。stable 遇到已有 Yijie instance 时非零 fail closed；默认 `pnpm tauri:dev`/`tauri:demo-fast` 的命令、图片模式、数据根和第二实例返回行为保持不变。
- local direct-entry：沿用精确 `local + demo_fast` 零登录入口；本 Feature 不改变 public/production 鉴权边界。
- `contract-impact=additive`：fixture 仍不是 wire/API/持久化契约；增量只包含 Desktop-local launcher/config/identity、stable-only second-instance 分支、既有 Provider/Desktop cleanup 环境投影与对应 implementation SHA pin。公共 Contracts、Host API 和 Runtime schema 不变。
- 权威事实：固定 Runtime app-server schema 与 `yijie-contracts/compatibility/agent-host-runtime-v1.json`；实现代码存在但未进入锁定 manifest 的路径只记为 extension observed。
- 数据/secret：所有正文为明确 synthetic copy；不允许绝对路径、真实身份、邮箱、手机号、凭据、商家或店铺字段。
- 外部动作：当前用户授权的最多一次真实 Provider/模型 submission 已由 predecessor entry 的一次 UI 点击保守记作使用；当前隔离 stable entry 不再发送 prompt。破坏性操作和生产写上限仍为 0；不 commit、push、tag、merge、发布或部署。

## 6. 推荐方案与停止条件

- 推荐方案：用测试内存 `ChatClientTransport → createChatClient → createChatStoreDefinition`，使原始 fixture 经过生产严格 parser、sequence/idempotency/resync 判断和 Store reducer；通过唯一 canary 扫描 production `dist/`。
- 取舍：只回放当前 wire 能表达的 assistant/reasoning/turn/resync/context 事件；其余能力登记到矩阵，不扩展生产契约。
- 30 分钟无新证据：回到 Runtime schema、compatibility manifest、Host mapper 和 Desktop parser 四个权威边界定位，不猜测式补事件。
- 90 分钟同一阻塞：保留版本冻结、矩阵和最小 parser/store 回放；把无法安全获取的参考证据标为 `reference-unobserved`。
- 超过 16 小时：停止增加非核心场景/格式，保留 13 个场景定义、可回放子集、bundle 隔离与精确未观察清单，不降低 Runtime 不变和不伪造证据要求。
