# FEAT-128 影响评估

## 1. Contract impact

`contract-impact = semantic`。

现有 Agent session v1/v2 event 是 closed union，直接向 v2 增加 Artifact variant 会让严格 consumer 失败。本需求计划采用显式
`/v3/.../events?event_schema_version=3` 和 v3 history/resource surface，并保持 v1/v2 wire 不变；但 Runtime
dynamic tool/reverse request 将新增 Host 付费 side effect，结果进入可持久化、可预览、可保存的 Artifact 链路，同时引入
幂等、取消、retention 与完整性语义。按最高风险分类为 semantic，不能只按现有 v3 image 形状未变而标为 additive。

如果实施时原地扩充 v2 closed union、改变既有 `assistant_append`/terminal 顺序、让旧 history reader 读取新必填形状，或修改默认权限解释，分类必须升级为 `breaking`。

## 2. 工程事实

| Fact | Evidence |
|---|---|
| Desktop assistant history 只渲染 `message.content`，live state 只有 `liveAssistantText` | `yijie-desktop/src/pages/chat/ChatPage.vue`、`src/stores/chat.store.ts` |
| Desktop 私有 Chat IPC v2 content block 只覆盖 user text/file/image attachment | `yijie-desktop/src/domain/chat-ipc.ts`、`src-tauri/schemas/chat-ipc-v2.schema.json` |
| Host v2 event payload 只投影 text/reasoning/item lifecycle，未保存输出内容 | `yijie-agent-host/internal/session/events.go`、`service.go` |
| 固定 Runtime app-server ThreadItem 已包含 `imageGeneration` | `yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs` |
| MiniMax catalog 只声明 text/image input，provider capability 未启用 image generation | `yijie-agent-host/internal/codex/provider.go` 与固定 Runtime capability gates |
| 固定 Runtime 支持 thread-start dynamic tool 注册及反向 `item/tool/call` | `yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/thread.rs`、`item.rs` 与 `app-server/src/dynamic_tools.rs` |
| Host 当前对所有带 id 的 Runtime 反向请求统一返回 method-not-found | `yijie-agent-host/internal/codex/protocol.go` |
| 固定 Runtime 内置 image generation 扩展要求 OpenAI actor/auth 且固定 OpenAI 图片模型 | `yijie-codex/codex-rs/core/src/tools/spec_plan.rs` 与 image generation extension |
| 当前 CSP 允许 image `blob:`，没有显式 video `media-src blob:` | `yijie-desktop/src-tauri/tauri.conf.json` |
| FEAT-127 明确把模型生成图片/文件展示排除在范围外 | `docs/features/FEAT-127-multimodal-chat-attachments/` |

## 3. 推荐数据流

```text
用户请求 + 可选单张当前 turn 图片附件
  -> MiniMax-M3 选择 Host 注册的 generate_image dynamic tool
  -> Runtime 反向 item/tool/call(thread/turn/call identity + closed args)
  -> Agent Host policy/idempotency/budget gate
  -> MiniMax China image-01 adapter (T2I or subject_reference.character)
  -> strict base64/media/size/digest validation
  -> Agent Host validates and announces Artifact v3 (provenance=provider)
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
`yijie-codex` 首选保持代码不变并固定现有 dynamic tool 协议证据；若 compatibility spike 证明当前 pin 无法让
MiniMax-M3 调用或 Host 响应 `item/tool/call`，必须停止并重新评审 Runtime fork 变更，不能退回关键词路由。

## 5. 存储与 migration

- Desktop 需要 SQLCipher expand migration：Artifact metadata、message relation、content chunk/BLOB 或受控 encrypted payload、preview state、retention 和 save receipt。
- Agent Host 只保留传输所需的短期 owner-only encrypted spool 与 opaque reference，不成为长期业务数据库。spool 位于 app-private 临时目录、文件权限 `0600`、内容用每进程临时密钥加密且密钥不落盘；Host 重启时先清除不可恢复的旧 spool。Desktop 成功接收并 ACK、staging `staged_at + 24h` 到期或 Host 重启时删除。
- I2I 参考图不得写入普通 Host 日志、bbolt replay 或 Runtime transcript 副本。Host 在 StartTurnV2 校验后只为当前
  active turn 建立有界 owner-only 短期引用；tool terminal、turn terminal、interrupt、超时或重启即清除。
- Provider JSON body、base64 响应和 decoded bytes 只能存在于有硬上限的内存/加密 staging 中；完成 Artifact commit 后释放中间缓冲。
- v1-v7 Chat 数据库 reader 必须继续工作；新 reader 为旧消息合成无 Artifact 的 projection。
- migration 为 forward-only candidate 时必须记录备份/roll-forward 边界，不能假定旧 Desktop 可打开 future schema。
- G2 已批准 Desktop SQLCipher incremental BLOB；S6-READINESS 将 image preview 修改为 image-only
  `yijie-artifact-preview` opaque-handle scheme，以满足 no-bytes-to-Vue。`expires_at` 从 Desktop SQLCipher
  commit 成功时间起算。若 authority BLOB 边界不可接受，必须重新打开 G2/Data review，不能静默落为 plaintext、
  generic asset/file protocol 或把 bytes/base64 暴露给 Vue。

## 6. 安全、隐私与权限

- 数据分类：`confidential`。报告可能包含店铺经营数据，文件名、标题和缩略图也可能敏感。
- Host/Desktop event 与日志只携带 opaque ID、kind、stage、大小等安全 metadata；不记录 bytes、正文、路径、token、prompt 或 raw provider error。
- MiniMax Key 归 Host secret 配置所有；不得转交 Runtime、Desktop 或 WebView。Authorization header、完整 prompt、
  参考图 Data URL、完整 base64、provider response 与 `trace_id` 不进入公开边界；诊断只保留 content-free 稳定类与本地 correlation。
- 官方允许 I2I 使用公网 URL，但易界首版禁止 URL 输入，避免 SSRF、重定向与模型诱导外传；只接受当前 turn 已授权附件的 Base64 Data URL。
- Artifact content 只能由同一 owner/tenant/session 的 native client 读取；loopback 不是认证替代品。
- HTML/SVG/宏/脚本/远程资源不执行。report renderer 只接受 closed、versioned、安全 section schema。
- 保存属于用户显式本地文件写入，必须经过 native dialog、路径校验、symlink/覆盖处理和原子写；S6-READINESS
  已冻结 S6A 的 exact private command 与 content-free result，并确认不新增 dependency/plugin/capability。实际实现仍须
  通过 S6A RED/GREEN 与 Security/Data diff review。
- 视频 blob preview 的候选 CSP 仅为精确 `media-src 'self' blob:`；G2 批准设计方向但不授权当前修改 Desktop CSP。S7 前必须复核实际 diff，禁止放宽为通用 `*`。

## 7. AI/provider 影响

- 本次新增可选 dynamic tool 与最小 developer/tool instruction，属于 `ai_behavior_change=tool`；模型仍固定 MiniMax-M3。
- Agent Host 只响应 Runtime 的结构化调用，不从自然语言自行判断。工具只在 exact real-image flag、有效 Host Key、
  中国区 endpoint/model pin、预算与会话 authority 同时成立时注册。
- 图片 API 固定 `image-01`；按单次 POST 直接返回最终 base64 的官方请求/响应形态实现，不发明轮询接口。
- video/file/report 首期只有通用 contract/UI 与 synthetic fixture；真实 producer 要分别登记 API/tool authority、费用授权、模型版本、合规与 Eval。
- 用户已授权最多 5 次、每次 `n=1` 的图片开发验证；计划 4 次（S12E/S12F 各一次 T2I/I2I），
  另有 1 个 repair slot 只供明确根因修复后复验；它是第 5 个预算额度，不限定物理发送序号。S12 campaign 当前
  used `0/5`、reserved `0`；此前 standalone success 不进入该 epoch，也不等于 yijie capability 或生产 activation，
  也不授权自动重试或其它媒体调用。

## 8. 风险等级与依赖

- 风险等级：high。原因是跨仓公共事件、confidential 本地内容、native 文件写入、媒体解码、CSP 与大对象资源管理。
- 新增外部依赖为 MiniMax 中国区图片生成 API；不新增自建云资源。候选实现应优先使用已有 Go HTTP/图片解析能力；新增 parser/media/crypto 依赖需单独审批和许可证/漏洞检查。
- 当前根工作区不是 Git repo；每个兄弟仓独立分支、状态、提交和发布。

## 9. 冲突与处理

- FEAT-127 的非目标明确排除生成结果展示。本需求新增 FEAT-128 Pattern，只覆盖该非目标，不篡改 FEAT-127 历史。
- 通用 Chat Pattern 已要求结构化结果卡，本需求为其补齐具体协议和交互。
- 历史“MiniMax 支持多模态不等于已能输出图片”仍成立；本次计划以明确工具、Host adapter 和后续真实证据
  关闭 image kind 的能力缺口，当前尚未关闭，也不能外推到视频/文件/report。
- S10D-H 仍要求 zero-key/zero-provider；真实 provider 测试使用独立 S12 harness、flag、账本与证据，不能改写 H 的失败或授权边界。
