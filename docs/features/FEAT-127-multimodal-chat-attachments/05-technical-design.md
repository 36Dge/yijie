# FEAT-127 技术设计

## 1. 设计摘要

Desktop 是附件原件、解析文本、索引、消息绑定和七天生命周期的唯一 authority。Agent Host 只接收一次 turn 所需的有界图片 data URL 与文件片段，严格验证后按原顺序映射到固定 Runtime `UserInput[]`；Host 不保存附件正文。公共 v1 与旧文本投影保持不变。

明确不做：云存储、云数据库、向量服务、OCR、压缩包、legacy `.doc`、宏 Office、SVG、远程 URL、生成文件/图片展示、真实模型质量声明和生产部署。

当前状态是“Desktop 人工验收进行中”，不是 `Local Candidate Complete`。picker 与仅附件 Runtime 路径已由用户验收通过；拖拽首次失败后已修复，修复后复验及 mixed send、重开和失败恢复等场景仍待记录，因此 G3/G4 保持 `PENDING`。Contracts/Host/Desktop commit、push 与精确 pin 已形成；tag、merge、签名制品和 deploy 未授权。

## 2. 组件职责

| Component | 职责 | 不负责 |
|---|---|---|
| `ChatComposer.vue` | 单一加号、草稿附件状态、remove/reselect、drag overlay、可访问名称 | 路径校验、文件读取、持久化 |
| Pinia/API/domain | v2 envelope、strict DTO、target-scoped 草稿恢复、进度/命令对账、仅附件发送、失败保留 | magic/owner/TTL authority |
| Tauri IPC | picker/import/remove/create/submit/history 边界和安全错误映射 | 业务正文日志 |
| `attachment.rs` | O_NOFOLLOW 读取、10 MiB bound、类型/容器验证、解析、分块 | 云扫描、模型调用 |
| SQLCipher repository | BLOB/chunks/blocks、owner/tenant、原子绑定、TTL、幂等 outbox | 公共业务主状态 |
| Desktop HostBridge | v2 JSON、data URL、selected chunks、response/error 映射 | 附件长期存储 |
| Agent Host | request/idempotency/aggregate validation、Runtime mapping | 原始文件解析、业务数据库 |
| Codex Runtime 0.144.6 | 消费 ordered text/image inputs | 七天生命周期与附件授权 |

## 3. 正常时序

```text
plus or drop
  -> native picker / transient path IPC
  -> O_NOFOLLOW regular-file read + size/magic/container checks
  -> bounded parse and deterministic chunks
  -> one SQLCipher transaction stores BLOB + chunks
  -> aggregate progress events are validated and queued for observable stage display
  -> safe attachment metadata returns to WebView
  -> user submits ordered text/file/image IDs with operation_id
  -> repository transaction creates message/turn/outbox and binds ready attachments
  -> dispatcher rechecks owner/state/expiry/hash and selects <=256 KiB file context
  -> Host v2 idempotency + semantic validation
  -> Runtime turn/start UserInput[] in original order
  -> history reload returns text projection + ordered attachment metadata
```

图片仅在 dispatch 时从 SQLCipher BLOB 生成 data URL；不会建立 plaintext cache。文件片段带不可信附件边界标记进入 Runtime text input，不赋予 tool 或文件系统权限。

## 4. 拖拽路径边界

macOS Tauri `onDragDropEvent` 会把用户本次显式拖入的绝对路径瞬时交给页面回调。该路径只可立即作为 `chat_import_attachments_v2` 参数使用：

- 只接受 1..10 个 absolute、无 NUL、无重复路径；
- native 使用 `O_NOFOLLOW` 打开并从 file descriptor 验证 regular file、大小与读取长度；
- 路径不得进入 Pinia state、DOM、response DTO、数据库、日志、错误、测试 snapshot 或遥测；
- command 完成后 JS 局部数组释放，返回值只有 opaque ID 和安全 metadata。

这是对早期“WebView 完全看不到路径”表述的受控实现澄清，不是通用文件系统 capability。若未来威胁模型要求路径绝不跨 WebView，改为 Rust `on_window_event` 导入并只 emit metadata，公共 DTO 不变。

## 5. 状态与不变量

UI attempt 状态：`queued -> importing -> parsing -> indexing -> ready`，失败为 `error_terminal`。Native 可以快速完成，但 Store 的展示队列必须让 `queued`、`importing`、`parsing`、`indexing`、`ready` 每个成功阶段至少可观察 `220ms`；`ready` 满足最短展示后才清除 attempt。失败前缀同样按允许顺序展示，`error_terminal` 保留到用户显式关闭。失败恢复是关闭失败 attempt 后通过统一入口重新选择，不提供附件原地重试。

进度事件不是单独的成功 authority。Store 只接受当前 context、operation、draft epoch、连续 sequence、稳定 item count 和合法状态转换；command 成功但事件过快或缺少成功阶段时补齐合法成功链，返回附件与已接收事件数量/终态冲突时删除本次新持久化草稿并报协议错误。command 在 native 终态事件到达前拒绝时，根据 typed `attachmentIssue` 和 `attachmentItemCount` 合成合法前缀及 `error_terminal`；之后到达的 queued/中间事件不能把终态改回 importing/ready。该单调终态规则关闭了“命令先拒绝、事件迟到”的竞态。

草稿 target 恢复状态独立于单次导入 attempt：

| Draft recovery state | Send/add/drop | Recovery |
|---|---|---|
| target 未加载或 `listDraftAttachments` 失败 | 全部 fail closed；不得把未知草稿当作空草稿 | 页面稳定错误入口调用 `retryDraftRecovery` |
| `new` target 重载成功 | 恢复 new composer 草稿与操作能力 | 原 context 内原地恢复 |
| `session` target 重载成功 | 恢复该 session 草稿后再完成订阅、history/resync/control-plane | 对相同 session 执行完整选择恢复 |

`draftTargetReady` 只有在当前 target 的持久草稿列表通过数量、唯一 ID 和 `ready` 状态校验后才为 true；bind、new/session target 切换或恢复失败期间 `canSend` 与 `canAttach` 均为 false。

持久状态：

| State | Content | Message binding | Allowed operation |
|---|---|---|---|
| `ready` | BLOB + optional chunks | none | bind once, remove, expire |
| `bound` | BLOB + optional chunks | exactly one message | dispatch/history/expire |
| `expired` | no BLOB/chunks | retained message | metadata history only |

不变量：附件 owner_user_id/tenant_id 必须匹配当前 context；单附件 <= 10 MiB；每消息 attachment <= 10；每 attachment 只绑定一次；image bytes 合计 <= 10 MiB；content blocks <= 16；text projection <= 1 MiB；过期内容不可构造 Host request。

## 6. 数据模型与 Migration

`migrations.rs` 的七项 catalog、逐版本 `user_version` 和 `chat_schema_migrations` 名称/SHA-256 ledger 是 Desktop schema 的运行时 authority。FEAT-127 必须按既有 `0001`..`0005` 之后的 `0006_chat_attachments` -> `0007_chat_attachment_draft_targets` 顺序迁移，不能只应用 v7 或绕过 ledger/foreign-key check：

- v6 `0006_chat_attachments.sql`：增加 `chat_attachments`、`chat_attachment_chunks`、`chat_message_content_blocks` 及索引，承载 scope、加密 BLOB、解析 chunks、message FK 和有序 blocks；不改变 v1-v5 表/列语义。
- v7 `0007_chat_attachment_draft_targets.sql`：先删除无法判定 composer 归属的未绑定 v6 `ready` rows，再增加 `draft_target_kind`、`draft_session_id`、`draft_ordinal`、target indexes、partial unique indexes 和 insert/update guards；bound/expired 历史附件保留且三个 draft 字段必须为 NULL。
- `ready` 附件必须绑定 `new` 或 owner/tenant 匹配的 `session` target。`draft_ordinal` 在 `(owner, tenant, target)` 内取当前 `MAX + 1`，批量按用户选择顺序递增；删除不重排，后续追加使用新 ordinal。读取只按 `draft_ordinal ASC`，不使用同秒 timestamp 或 UUID 打破顺序。

迁移重复启动会先校验已应用 ledger digest，再迁到最终 `user_version = 7` 并执行 foreign-key check。v7 应用对没有 blocks 的旧 message 合成 text block；没有历史正文 backfill。旧应用按既有安全策略拒绝 future schema，因此不支持在同一已升级文件上原地降级。删除 session 依赖 FK cascade，之后沿用现有 WAL checkpoint/truncate 流程；首次写多模态即 switch，contract phase 不在本期。

## 7. 解析与索引

- 图片：magic 与扩展名一致；JPEG/PNG/WebP/GIF。
- plain text：UTF-8、无 NUL；TXT/Markdown/CSV/JSON/YAML/XML/HTML/RTF。
- PDF：`%PDF-` + bounded extraction；空或不可解析文本失败。
- OOXML：DOCX/XLSX/PPTX；验证 canonical marker、entry name、entry count、单 entry/总解压上限、compression method，拒绝 traversal、duplicate、`.bin` 与 VBA。
- 输出：规范化后最多 512 KiB，按 UTF-8 边界切 <= 8 KiB chunks；最多 128 chunks。
- 检索：使用用户 text 的规范化 token 与 chunk lexical score，稳定按 score/ordinal 选取；无查询词时按 ordinal；总 context <= 256 KiB。

解析结果不是可信指令。Host/Runtime input 使用明确的文件上下文界限；附件内容不能改变 read-only/never policy。

## 8. 事务、并发与幂等

- import 一组附件使用单 repository transaction；任一 native validation 失败时不写入该项，UI 保留已有草稿。
- create/submit 在一个 transaction 内创建 turn/message/outbox/content blocks，并把所有 `ready` 附件条件更新为 `bound`；任一失败全部回滚。
- outbox 已有 `operation_id` 同时作为 Host v2 operation ID；canonical block digest 写入私有 dispatch state。相同 ID/相同 input 返回原 turn，相同 ID/不同 input 冲突。
- repository worker 串行化 TTL、binding 与 dispatch，避免 expiry race；attempt generation 阻止迟到 retry 覆盖新结果。
- 草稿 target 读取失败不发布空数组为可用状态；bind 保留有效 context 供原地重试，session target 重试重新执行草稿恢复与完整 session resync。
- 导入 command 与 aggregate event 通过 operation/epoch/sequence/item count 对账；合成终态后拒绝迟到事件，command 成功但协议不一致时补偿删除本次返回的 ready rows。
- 未收到 202 但远端结果未知时只以同一 operation ID重试；不得换 ID 自动重放。
- 用户移除未绑定附件调用 native remove，条件删除 `state=ready AND message_id IS NULL`；bound/expired 删除请求 fail closed。

## 9. TTL 与删除

`expires_at = imported_at + 604800`。启动、导入、历史加载、消息提交和 dispatch 前触发 maintenance：先删 chunks，再把 bound 附件 BLOB 置空/state=`expired`；未绑定 ready 附件到期直接删除。历史保留安全 metadata 与 ordinal。

七天仅约束 Desktop 原件、解析文本、索引及未来检索资格。Runtime 会把已经发送的图片/文本上下文写入自身 thread rollout；本期没有可证明的历史追溯擦除能力。会话永久删除仍按 FEAT-126 multi-surface cleanup saga 删除 Runtime thread/Host mapping/Desktop rows，但 OS snapshot/SSD 物理擦除不作绝对承诺。

## 10. 安全与隐私

- confidential 数据只存 SQLCipher；禁止 plaintext cache、localStorage、Host bbolt、Public Tasks、API PostgreSQL。
- 路径、文件名、正文、chunks、data URL 和 SHA 不进入日志；Debug 只允许 opaque ID、kind、byte/chunk count。
- 文件名 NFC 规范化、移除 control/path separator、1..255 bytes；错误使用稳定 code 和恢复动作。
- symlink、目录、设备、空文件、TOCTOU length mismatch、archive、macro、active SVG、伪装 magic 均拒绝。
- 不新增 CSP、Tauri filesystem capability、外部 URL、云 secret 或平台 token。
- 附件不能提升 Runtime 权限；prompt injection 只作为 untrusted context，不触发写工具。

## 11. 性能与资源上限

| Resource | Limit |
|---|---:|
| single attachment | 10 MiB |
| attachments/message | 10 |
| image bytes/turn | 10 MiB |
| extracted text/file | 512 KiB |
| chunks/file | 128 x <=16 KiB DB bound; parser targets <=8 KiB |
| file context/turn | 256 KiB UTF-8 |
| content blocks/message | 16 |
| OOXML entries/uncompressed | 512 / 32 MiB |

所有读取、base64 decode、XML/ZIP walk 和 request body 都必须先有界。当前不声明大型文件 latency SLO；最终报告记录合成 10 MiB 边界测试结果。

## 12. UI 与可访问性

- 40px Ghost 加号位于 composer 左下角、权限入口之前；使用 `YjIcon` Lucide registry，tooltip/aria-label 均为“添加图片或文件”。
- 红框只属于参考截图标注，不进入样式。
- 附件队列不嵌套卡片；长名称 ellipsis，状态含文字；remove 为图标按钮并有 tooltip，失败文案引导重新选择。
- 五个成功阶段各至少显示 220ms；阶段变化不改变操作区尺寸。`error_terminal` 不自动消失，且迟到 native 事件不得覆盖失败终态。
- 草稿恢复失败时发送、加号和拖拽入口同时禁用；页面级“重试”重新读取当前 new/session target，不把未知持久草稿展示为空。
- 任一附件非 ready 时 send disabled；失败项保留并提供恢复；允许 attachment-only。
- drag overlay 使用 fixed/stable dimensions，不引发布局位移；light/dark、1180x760、keyboard、200% zoom、VoiceOver 与 reduced motion 进入检查矩阵。

## 13. 方案比较与回滚

| 方案 | 结论 |
|---|---|
| SQLCipher BLOB + local chunks | 采用；零云资源、authority 清晰、可随 session cleanup |
| app-data plaintext files | 拒绝；残留与路径泄漏风险高 |
| 云对象存储 + server parser/vector DB | 拒绝；超出当前资源、部署和安全范围 |
| Runtime localImage path | 拒绝；跨路径 authority 且难证明 TTL；采用 data URL |

数据库迁移不 down。若本地候选失败，优先关闭 v2 调用、保留 v1 并使用 v7 应用 roll-forward；如必须回到旧应用，必须整体恢复与该旧版本匹配的迁移前加密备份，不得让 v5/v6 应用打开 v7 数据库。没有 production flag 或生产数据迁移。

## 14. ADR 与批准状态

不新增 ADR：沿用 ADR-0013/0014 的 Desktop local confidential authority 和 deletion boundary，公共能力以 versioned v2 expand。若未来引入云存储、服务端解析、向量索引或跨设备同步，必须新 ADR。

技术/安全设计依据用户 2026-08-17 明确要求完成本地实现并授权模型补足高质量交互而进入本地候选实施。该授权覆盖 G2 的本地设计与实施方向，不构成独立人工代码评审、Contracts Owner 合并批准或生产批准。

截至 2026-08-19，最终 Contracts/Host/Desktop commit 已推送，精确 pin 与提交后自动门禁通过。人工验收只形成 picker 与仅附件 Runtime 路径的部分记录，拖拽修复后复验及其余场景仍未完成；因此不得声明 `Local Candidate Complete`、G3 Slice Complete 或 G4 Code Complete。tag、merge、签名制品与任何 deploy 仍未授权。
