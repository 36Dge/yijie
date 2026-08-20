# FEAT-128 影响评估

## 1. Contract impact

`contract-impact = semantic`。

现有 Agent session v1/v2 event 是 closed union，直接向 v2 增加 Artifact variant 会让严格 consumer 失败。本需求计划采用显式 `/v3/.../events?event_schema_version=3` 和 v3 history/resource surface，并保持 v1/v2 wire 不变；但现有 Runtime `imageGeneration` item 的解释将从无内容的普通 lifecycle item 变为可持久化、可预览、可保存结果，同时新增 retention、完整性和 native 保存语义。按最高风险分类为 semantic，不能只按新增 v3 形状标为 additive。

如果实施时原地扩充 v2 closed union、改变既有 `assistant_append`/terminal 顺序、让旧 history reader 读取新必填形状，或修改默认权限解释，分类必须升级为 `breaking`。

## 2. 工程事实

| Fact | Evidence |
|---|---|
| Desktop assistant history 只渲染 `message.content`，live state 只有 `liveAssistantText` | `yijie-desktop/src/pages/chat/ChatPage.vue`、`src/stores/chat.store.ts` |
| Desktop 私有 Chat IPC v2 content block 只覆盖 user text/file/image attachment | `yijie-desktop/src/domain/chat-ipc.ts`、`src-tauri/schemas/chat-ipc-v2.schema.json` |
| Host v2 event payload 只投影 text/reasoning/item lifecycle，未保存输出内容 | `yijie-agent-host/internal/session/events.go`、`service.go` |
| 固定 Runtime app-server ThreadItem 已包含 `imageGeneration` | `yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs` |
| MiniMax catalog 只声明 text/image input，provider capability 未启用 image generation | `yijie-agent-host/internal/codex/provider.go` 与固定 Runtime capability gates |
| 当前 CSP 允许 image `blob:`，没有显式 video `media-src blob:` | `yijie-desktop/src-tauri/tauri.conf.json` |
| FEAT-127 明确把模型生成图片/文件展示排除在范围外 | `docs/features/FEAT-127-multimodal-chat-attachments/` |

## 3. 推荐数据流

```text
Runtime/provider/tool output
  -> Agent Host validates and announces Artifact v3
  -> authenticated local content transfer with opaque reference
  -> Desktop native validates length/media/digest/scope
  -> SQLCipher artifact authority + bounded preview cache
  -> private IPC v3 projection
  -> type renderer in Chat conversation
  -> explicit native save dialog
```

历史方向：Desktop SQLCipher Artifact/message relation -> history/resync v3 -> Pinia projection -> renderer。会话删除和七天 maintenance 清除 content 与 cache。

## 4. 仓库、职责与初始状态

| Repository | 影响 | Owner | 初始 branch / full HEAD / worktree |
|---|---|---|---|
| yijie | FEAT-128 交付包与跨仓治理 | 段成威 | `feat/feat-126-foundation-closure` / `3d6988daa7a36b24bb2e86308e4cc7213c967426` / 创建前 clean |
| yijie-contracts | v3 Agent event/resource schema、`jsonschema/report/report-document-v1.schema.json`、fixtures、SDK | Platform Team | `feat/feat-126-content-free-candidate` / `747cf740f2d91e76e5c1a130e8e009f1efa821b8` / clean |
| yijie-agent-host | Runtime item adapter、Artifact staging/transfer、v3 SSE、synthetic producer | Agent Runtime Team | `feat/feat-126-foundation-closure` / `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86` / clean |
| yijie-desktop | native transfer/persistence、private IPC v3、store、renderer、save action、visual tests | Client Team | `feat/feat-126-foundation-closure` / `2cb4ffdd87055e5f70aafacc63479154e0c62cad` / clean |
| yijie-codex | read-only upstream Runtime authority/capability investigation | Runtime Team | `develop` behind remote by 1 / `0ce5902ed400866be0196886bb78f693a004d68d` / clean |

`yijie-api`、Infra、Connectors、Knowledge、Admin Web 首期本地 slice 不修改。生产云存储、分享和业务主状态不进入本需求。

## 5. 存储与 migration

- Desktop 需要 SQLCipher expand migration：Artifact metadata、message relation、content chunk/BLOB 或受控 encrypted payload、preview state、retention 和 save receipt。
- Agent Host 只保留传输所需的短期 owner-only encrypted spool 与 opaque reference，不成为长期业务数据库。spool 位于 app-private 临时目录、文件权限 `0600`、内容用每进程临时密钥加密且密钥不落盘；Host 重启时先清除不可恢复的旧 spool。Desktop 成功接收并 ACK、staging `staged_at + 24h` 到期或 Host 重启时删除。
- v1-v7 Chat 数据库 reader 必须继续工作；新 reader 为旧消息合成无 Artifact 的 projection。
- migration 为 forward-only candidate 时必须记录备份/roll-forward 边界，不能假定旧 Desktop 可打开 future schema。
- G2 已批准 Desktop SQLCipher incremental BLOB + 有界 WebView blob preview 作为首选；`expires_at` 从 Desktop SQLCipher commit 成功时间起算。若 S4 性能证据证明 64 MiB BLOB 不可接受，必须重新打开 G2 选择版本化加密文件格式，不能静默落为 plaintext 或自定义 URL scheme。

## 6. 安全、隐私与权限

- 数据分类：`confidential`。报告可能包含店铺经营数据，文件名、标题和缩略图也可能敏感。
- Host/Desktop event 与日志只携带 opaque ID、kind、stage、大小等安全 metadata；不记录 bytes、正文、路径、token、prompt 或 raw provider error。
- Artifact content 只能由同一 owner/tenant/session 的 native client 读取；loopback 不是认证替代品。
- HTML/SVG/宏/脚本/远程资源不执行。report renderer 只接受 closed、versioned、安全 section schema。
- 保存属于用户显式本地文件写入，必须经过 native dialog、路径校验、symlink/覆盖处理和原子写；G2 只批准这项最小权限设计，具体 Tauri command/capability 仍须在 S4 实现前复核且不得早于 G2A。
- 视频 blob preview 的候选 CSP 仅为精确 `media-src 'self' blob:`；G2 批准设计方向但不授权当前修改 Desktop CSP。S7 前必须复核实际 diff，禁止放宽为通用 `*`。

## 7. AI/provider 影响

- 本需求不修改 MiniMax prompt 或模型本身，改变的是 Runtime/Host output projection 与能力 gating。
- 固定 Runtime `imageGeneration` 只构成上游形状证据，不构成 MiniMax 可用性、费用、延迟或质量证据。
- video/file/report 首期只有通用 contract/UI 与 synthetic fixture；真实 producer 要分别登记 API/tool authority、费用授权、模型版本、合规与 Eval。
- 未经用户明确授权，不调用真实付费模型或媒体生成 API。

## 8. 风险等级与依赖

- 风险等级：high。原因是跨仓公共事件、confidential 本地内容、native 文件写入、媒体解码、CSP 与大对象资源管理。
- 不新增云依赖。候选实现应优先使用已有 Go/Rust/TypeScript 依赖；新增 parser/media/crypto 依赖需单独审批和许可证/漏洞检查。
- 当前根工作区不是 Git repo；每个兄弟仓独立分支、状态、提交和发布。

## 9. 冲突与处理

- FEAT-127 的非目标明确排除生成结果展示。本需求新增 FEAT-128 Pattern，只覆盖该非目标，不篡改 FEAT-127 历史。
- 通用 Chat Pattern 已要求结构化结果卡，本需求为其补齐具体协议和交互。
- “MiniMax 支持多模态”与当前代码事实不等价。交付包记录为 capability gate，而不是默认开启真实媒体生成。
