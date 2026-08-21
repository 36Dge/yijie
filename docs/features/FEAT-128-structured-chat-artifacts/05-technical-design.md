# FEAT-128 技术设计

## 1. 设计摘要

- 要解决的问题：让 Agent/LLM 输出的图片、视频、文件和报告在 Chat 中以结构化、可流式更新、可历史恢复的 Artifact 展示，而不是 Markdown 链接或一次性文本。
- 选择的方案：Host v3 显式协商 + owner-only 临时资源；Desktop native 校验并写入 SQLCipher 长期 authority；
  WebView media 使用 opaque image/video handles，S8 file 使用一次性 bounded safe projection；S9 report 使用
  native closed bounded projection 与 canonical JSON save。
- 关键约束：本地-only、confidential、无云资源、v1/v2 保持兼容、真实 MiniMax output capability 默认关闭；无原始
  路径/base64/token、未授权内容或超出已批准 bounded projection 的正文进入 SSE/WebView state，用户授权 file
  projection 仅按 8.8 短暂存在；小文件 projection 可在上限内等于完整正文。
- 明确不做：生产部署、云存储、公开分享、raw HTML/脚本报告、任意本地路径、视频转码、真实付费媒体生成、跨设备同步。
- 设计状态：G2/G2A APPROVED，S3/S4/S5 与其 G3 scope 已通过；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B/S8A/S8B/S9A
  已分别作为 G3 外独立切片 PASS。S9B-READINESS/Pattern 1.5.0
  `630c3c8d55a2617499f51bd5bed263b819aaf084` 将 S9B 拆为 S9B-D/S9B-R，只批准 D 编码；D/R 均
  `NOT RUN`，G3 不扩展，G4 pending。

## 2. 组件职责与依赖方向

| Component/Repository | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| yijie-codex | 上游 Runtime canonical item authority | provider/tool output | `imageGeneration` started/completed item | 易界 Artifact 存储、下载或 UI |
| yijie-contracts | v3 wire、report document、error/fixture 权威源 | 已批准业务语义 | OpenAPI/JSON Schema/Proto/AsyncAPI/SDK | Runtime 实现、数据库或 UI |
| yijie-agent-host | Runtime item 归一化、短期 staging、v3 SSE 和认证资源读取 | Runtime notification、synthetic fixture | 安全 Artifact lifecycle + relative resource | 长期业务数据、WebView 渲染、用户保存目标 |
| Desktop native/Tauri | implemented Host fetch/SQLCipher/history 与 image/video/file/report private boundaries | v3 event/resource；private identity-only intent | metadata-only history；media opaque URL；file/report bounded projection；content-free save result | provider 选择、公共契约权威、generic filesystem |
| Desktop domain/store | implemented 单调状态机、去重、history/live projection | private IPC v3 safe metadata | stable provider-neutral view model | wire 外 I/O、bytes、文件写入 |
| Desktop Vue components | implemented generic shell + image/video/file renderer；S9B-D/R 将分别提供 chart foundation 与 report renderer | view model、typed native client result | 用户可观察 UI intent 与 component-local authorized preview | Host/SQL/path/digest/bytes/save 副作用 |

```text
Runtime or synthetic producer
  -> Agent Host v3 lifecycle + owner-only staging
  -> Desktop native authenticated transfer
  -> SQLCipher Artifact authority
  -> private IPC v3 projection
  -> Chat Artifact renderer
  -> explicit native save dialog
```

## 3. 关键时序

### 正常流式路径

1. Runtime/producer 接受生成或导出工作，Host 分配稳定 `artifact_id` 并立即发布 `item.artifact.started`。
2. Desktop 在既有 SSE sequence 中接收 started，持久化最小 metadata，并让 store 创建稳定占位；文本 delta 继续独立渲染。
3. Host 只在有真实阶段/百分比时发布 progress。Desktop 以不高于 10Hz 合并 UI 更新，但不改变持久化事件顺序。
4. Producer 完成后，Host 校验内容、媒体类型、大小和 digest，写入 owner-only staging，资源 GET/HEAD 可用后发布 completed。
5. Desktop native 通过同一 bearer 读取 resource，禁止重定向并复核 scope、Content-Length、MIME/magic 和 SHA-256；以临时记录/增量 BLOB 写入 SQLCipher。
6. 数据库事务提交 Artifact content、metadata、turn relation 和 terminal state 后，private IPC 把 UI 状态从 `transferring` 切到 `ready`。
7. S6A open command 只接收 session/turn/artifact identity，签发 one-shot opaque handle；custom image protocol 再次
   复核 SQLCipher authority 后把 bytes 直接交给 WebView resource loader，Vue JS 不接触正文。
8. 用户选择保存时，S6A native command 再校验 authority，native dialog 取得目标，内容分块写入同目录临时文件
   并原子替换；WebView 只接收 content-free outcome。
9. Desktop ack 后 Host 可删除 staging；即使 Host 重启，Desktop 已持久化历史仍可只读预览/保存。

### 报告路径

1. producer 生成 `application/vnd.yijie.report+json;version=1`。
2. Contracts closed schema 定义 root/envelope/known payload；unknown `required=false` 允许 opaque payload，unknown
   `required=true` 拒绝整份文档。Host synthetic 只负责 schema-valid lifecycle/resource，不是 canonical fixture bytes。
3. S4 已把 canonical bytes 持久化到 SQLCipher，history/private IPC 仍为 metadata-only。S9A 已在
   `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` 修复 Desktop consumer conformance，并执行完整 schema、
   authority、size/digest/revision 校验。
4. 用户明确打开后，S9A 只返回 8.9 的 closed bounded projection；unknown optional 只返回 ordinal/unsupported marker，
   不遍历或返回原 type/payload。close/error/stale/switch/unmount 后清空组件 local state/DOM。
5. S9B-D 先实现 8.10 exact dependency/theme/closed adapter/card，不读 report；S9B-R 再按 section ordinal 展示
   known union 并始终提供 accessible text table。S9B-R 等待 D immutable PASS 与单独授权。

### 失败、取消与恢复

1. provider failure 映射为 typed `item.artifact.failed`，不带 raw error；同 turn 其它 Artifact 继续。
2. 当前只支持 turn-level interrupt；它把尚未终态 Artifact 映射为 `failed(error_code=turn_interrupted)`，Desktop UI 展示“已取消”。本候选不定义 Artifact-specific cancel endpoint。
3. completed 后 transfer 失败时，Desktop 保持 `transferring_failed` 与重试入口；不伪造 ready，也不创建第二 Artifact。
4. duplicate event 由 event_id/sequence 幂等忽略；gap、stream change、double terminal 或 metadata drift 进入 resync-required。
5. Host staging 消失且 Desktop 尚未持久化时显示“结果内容已不可用”，保留安全 metadata；不可通过旧 path 猜测恢复。
6. 应用重开从 SQLCipher 恢复；过期 maintenance 清除 content/preview，保留 metadata 和 `expired`。
7. 会话删除沿用 cleanup saga；只有 SQLCipher content、relation、cache 和 Host staging 均清理后才报告完整删除。

## 4. 状态模型

| 当前状态 | 事件 | 条件 | 新状态 | 副作用 | 非法处理 |
|---|---|---|---|---|---|
| absent | started | scope/ID/kind 合法 | announced | 插入 metadata 与稳定 ordinal | 拒绝未知 schema；不创建任意链接 |
| announced | progress | sequence 连续、阶段合法 | generating/processing | 合并进度，最多 10Hz 刷新 | 百分比回退/伪造值触发 resync |
| announced/generating/processing | completed | resource metadata 合法 | transferring | native 开始一次幂等 fetch | completed 重复只复用既有 transfer |
| transferring | local commit success | digest/size/MIME 一致 | ready | 建立 preview eligibility | commit 失败保留 authority/staging，不置 ready |
| non-terminal | failed | typed code 合法 | failed/cancelled | 停止 transfer，保留 metadata | 终态后 late event 丢弃并安全诊断 |
| ready | retention due | now >= expires_at | expired | 删除 content/cache，checkpoint/WAL 验证 | 删除失败保持不可关闭错误并重试 |
| any non-deleted | session cleanup | cleanup receipt 完整 | deleted | 删除 relation/content/cache/staging | 部分失败报告 incomplete |
| any | stream gap/change | cursor 不连续 | resync_required | 停止预览新内容，加载 authority | 不基于局部缓存继续猜测 |

状态分层约定：wire `item.artifact.started` 创建本地 `announced`；wire `progress.stage` 按权威阶段映射为
`generating` 或 `processing`；wire `item.artifact.completed/status=ready` 只表示 Host resource ready，
Desktop 随后进入 `transferring`，完成本地 digest/size/MIME 校验和 SQLCipher commit 后才进入 local `ready`。
wire `failed` 映射为 `failed` 或 `cancelled`，`expired` 只由本地 retention maintenance 产生。这样 wire
终态与 local preview eligibility 不混用。

`provenance` 是受信的安全 metadata，不从模型名、kind、文件名或自然语言推断。local synthetic profile
只接受固定 manifest 并写入 `synthetic`，UI 显示“本地合成演示”；历史/resync 保留该来源值。真实
`provider`/`tool` 值在 capability 和权限门禁通过前不可发送。

## 5. 领域模型与不变量

| Entity/Value | Owner/tenant scope | ID/幂等键 | 不变量 | 生命周期 |
|---|---|---|---|---|
| Artifact | user + tenant + session + turn | Host-generated canonical `artifact_id` UUID；Runtime `item_id` 仅内部映射 | kind/provenance/status/ordinal 不可变；终态单调 | announced -> generating/processing -> transferring -> ready -> expired/deleted |
| ArtifactManifest | 同 Artifact | artifact_id + digest | ready 时 media/size/digest required；无 path/token | completed 后固定 |
| ArtifactContent | Desktop scope | artifact_id | bytes 与 manifest digest/size/MIME 一致 | transfer commit -> expiry/delete |
| HostStagingLease | 本机 Host session | artifact_id + lease generation | owner-only encrypted spool、`0600`、per-process ephemeral key、no redirect、TTL、有界 | completed -> Desktop ack/TTL/restart cleanup |
| ReportDocumentV1 | 同 Artifact | schema version + digest | closed safe sections、无 HTML/URL/script | content 生命周期内不可变 |
| ImagePreviewHandle | main WebView + process/context/session | 256-bit CSPRNG base64url | 30s、one-shot、非 bearer；不持久化/日志/Pinia/snapshot | issue -> atomic consume/release/TTL/restart |
| VideoPreviewHandle | main WebView + process/context/session | 独立 256-bit CSPRNG base64url | 30min absolute/5min idle、无累计 request cap、single Range、非 bearer；2 handles/2 concurrent/64MiB in-flight | issue -> repeated HEAD/GET -> release/TTL/restart/binding invalidation |
| FilePreviewProjection（S8A implemented） | current main WebView/context/artifact | request_id + immutable revision | one-shot bounded safe text/CSV/JSON；不持久化、不签发 URL/handle | explicit read -> component local state -> close/switch/unmount clear |
| ReportPreviewProjection（S9A planned） | current main WebView/context/artifact | request_id + immutable revision + section ordinal | full schema valid 后形成 closed bounded known union；unknown payload omitted；不持久化、不签发 URL/handle | explicit read -> component local state -> close/error/stale/switch/unmount clear |
| SaveIntent | 当前 WebView 用户动作 | request_id + artifact identity | one active；native dialog/path only；Vue 只收 content-free outcome | click -> dialog -> atomic success/cancel/failure |

## 6. 数据与 Migration 专项

- 是否涉及数据库/缓存/持久化：是，Desktop SQLCipher expand；Host 只有短期 staging，不扩展为业务主库。
- 已实现 migration：`yijie-desktop/src-tauri/migrations/chat/0008_chat_output_artifacts.sql`；S6A 不需要也不允许新增 migration。

| Phase | Schema/Data change | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | 增加 artifact metadata/content/turn relation/ordinal/expiry 表与索引 | 旧表不删不改；旧 app 对 future schema fail closed | 旧消息合成空 Artifact list | migration checksum、populated v7 fixture、FK/unique tests | 升级前完整加密备份；否则 v8 roll-forward |
| Backfill | N/A；旧消息没有 Artifact，不批量制造记录 | 完全不变 | reader 返回空集合 | legacy history tests | 无 backfill job |
| Switch | v3 completed 先 transfer/commit，再暴露 ready | v1/v2 路径继续写旧消息 | v3 history 恢复 Artifact | crash points、idempotent replay、WAL/reopen | 关闭 v3 flags，保留已存 Artifact 只读 |
| Contract | 本期不删除 v1/v2、旧 message 字段或旧 migration | 旧 consumer 继续 | 双轨共存 | v1/v2 equality + v3 conformance | 未来独立清理 Feature |

G2 选择 content 使用 SQLCipher BLOB 增量 I/O，避免 plaintext app-data 文件。`local_committed_at` 是事务提交成功时间，`expires_at = local_committed_at + 168h`。若性能验证证明 64 MiB BLOB 不可接受，必须重新打开 G2 选择版本化加密文件格式；不得静默落为 owner-only plaintext。

## 7. 一致性与韧性

- 事务边界：单个 Artifact transfer 以一个 SQLCipher transaction 提交 metadata、content 和 terminal projection；UI ready 只在 commit 后发生。
- 并发冲突：同 artifact 只允许一个 active transfer/save intent。image 每 Artifact 最多 1 个未消费 one-shot handle，
  每 WebView 最多 4 个 image handles、2 个 protocol reads、40 MiB image in-flight；video 每 Artifact 最多 1 个 active
  handle，每 WebView 最多 2 个 video handles、2 个并发 Range requests、64 MiB video in-flight；file 不签发 handle，
  每 WebView 最多 2 个 preview operations、2,097,152 bytes source in-flight，并按 identity single-flight。duplicate
  completed 复用同一 operation。
- 幂等：Host event_id/sequence、Desktop transfer operation 和数据库 unique key 共同防重复。
- 超时/取消：Host resource read、Desktop transfer、preview decode、save 和 resync 均使用 bounded timeout/AbortSignal；turn interrupt 不自动删除已 ready Artifact。
- 重试/退避/上限：仅 retryable transport/staging error 可重试，指数退避最多 3 次；integrity/protocol/unsupported 不自动重试。
- 限流/熔断/降级：每项 20/64 MiB、每 turn 128 MiB/12 项；Host 每 session staging 256 MiB、全局 1 GiB、lease 从 `staged_at` 起 24 小时。staging 使用 app-private encrypted spool，不使用 1 GiB 进程内大对象。达到上限拒绝新 Artifact，不驱逐正在读取或已持久化内容。
- 部分失败与补偿：一项失败不回滚其它 ready；Desktop commit 失败不 ack Host；Host ack 丢失依靠 TTL 清理。
- 资源释放：未消费 image handle、WebView decoded image、video handle、timer、AbortController、temp file、range
  response 和 staging lease 都必须在关闭/切换/失败时释放；image handle 在 GET 开始时原子消费；video handle
  允许 bounded multi-request，但 pause/clear source/unmount/context switch 时必须显式释放；restart 后两类均无效。

## 8. 安全设计

- 认证入口：Host 既有 owner-only loopback bearer；WebView 不读取 bearer。
- 资源级授权：每次 GET/HEAD 同时校验 token、session、artifact ownership、lease 和 state。
- 租户隔离：Desktop SQL query 与 IPC command 强制 owner_user_id + tenant_id + session_id；opaque ID 单独不构成权限。
- 输入验证：closed kind/status/error/report schema；safe filename；MIME + magic；长度、像素、时长、行列、series、UTF-8 与 digest limits。
- Secret/token 边界：API Key 只留 Runtime 子进程环境；Host bearer 只在 native bridge；content href 为相对路径且无 query token。
- PII/日志脱敏：日志只记录 kind、typed code、byte bucket、duration bucket 和 opaque correlation；不记录标题、文件名、正文、path、digest 或 raw provider error。
- 高风险审批：N/A；Artifact 查看不是电商业务写操作。保存仍需用户明确 native dialog intent，不能后台自动写文件。
- 审计：本地阶段只记录 aggregate typed operation outcome，不记录目标路径；生产审计方案当前 N/A/not designed。
- CSP/capability：S6A 已只在既有 `img-src` 追加 `yijie-artifact-preview:`，S7A 已只增加精确
  `media-src 'self' yijie-artifact-video:`，均不改 `connect-src` 或增加 external
  origin；不得将 Artifact 放入既有 asset/blob/data 路径。当前 app 没有 app-command ACL manifest，局部新增会让
  所有既有 app commands 被 ACL 检查，因此 capability/permission 文件保持不变。只允许 3 个 exact app commands，
  不引入 dialog/fs/shell plugin。S8A 直接返回 bounded projection，不新增 scheme/CSP/capability/plugin。

### 8.1 S6A image preview boundary

1. 独立 Desktop-private authority：`chat-artifact-native-v1.schema.json`，不得修改公共 Contracts、Host 或
   `chat-ipc-v3.schema.json` 的 metadata-only history 职责。
2. exact commands 仅为 `chat_open_artifact_image_preview_v1`、`chat_release_artifact_image_preview_v1`、
   `chat_save_artifact_image_v1`。envelope 使用 `requestId/contextId`；open/release/save payload 只包含
   `sessionId/turnId/artifactId`，command 同时校验 injected WebView label 必须为 `main`。
3. open 先授权 `task.read` 并查询 owner/tenant/session/turn/artifact，要求 ready、未过期、image、
   `image/png|image/jpeg|image/webp`、1..20 MiB；读取 BLOB 后复算 length/digest 并执行 image limits。成功才签发
   43-char CSPRNG handle，registry 绑定 process epoch、WebView、context 和完整 Artifact identity。
4. `yijie-artifact-preview://localhost/v1/<handle>` 只接受无 query/body 的 GET。handler 原子 consume handle，复核
   binding/authority/content，返回 allowlisted MIME + length + no-store/nosniff；不返回 CORS header、不支持
   fetch/XHR/HEAD/Range/redirect。任一 protocol failure 只返回 empty 404，不形成存在性 oracle。
5. release、session switch、context invalidation、WebView/app close、TTL 30s 清 registry；S6B 在 unmount/replace
   先清 `<img src>` 再 release。超过 4 handle、2 read 或 40 MiB 时 typed limit error，绝不隐式驱逐。

### 8.2 S6A native image save boundary

1. 只有一次明确 click/keyboard intent 可调用 save；native 在 dialog 前和 write 前复核与 preview 相同的 authority。
2. 复用现有 macOS target dependency `rfd=0.16.0`，不增加 npm/Cargo dependency 或 Tauri plugin。safe default
   filename 来自 validated display name/fallback；PNG/JPEG/WebP canonical extension 为 `.png/.jpg/.webp`，缺失时
   append，不匹配时返回 `artifact_native_extension_mismatch`，覆盖确认由 native panel 完成。
3. dialog 选择的绝对路径只在 native stack 存活，不进 SQLCipher/history/log/result。目标目录内创建随机 `0600`
   create-new/no-follow temp；从 SQLCipher BLOB 分块写出并同步复算 length/SHA-256，fsync 后同目录 atomic replace。
   目标 leaf 为 symlink/非 regular 时 fail closed。
4. 结果严格为 saved/cancelled/failed + stable code，无 path/name/digest/body。normal failure 的 RAII guard 删除 temp；
   authority copy 保留。crash/power loss 可能留下用户已选择目录内的 `0600` hidden temp，不为此持久化 path 或扫描
   arbitrary filesystem；下一次同目录显式 save 只做可验证的 best-effort stale cleanup。
5. stable error codes 与响应脱敏以 Accepted Pattern 1.3.0 §9.3 为唯一清单；cross-scope 统一 not_found。

### 8.3 Private result 与 stable error allowlist

- image/video preview open 成功只返回 opaque preview URL/handle envelope；release 成功只返回 content-free released；
  save 只返回 `saved|cancelled|failed`。S8A file 与计划中的 S9A report preview 是窄例外，只返回相应 bounded safe projection 与
  allowlisted media type；任何结果都不得包含 filename、target path、size、digest、Host href、bytes/base64、bearer、
  未授权内容、超出已批准 bounded projection 的正文或 raw native error。小文件的授权 projection 可在 caps 内等于
  完整正文，但只按 8.8 的生命周期存在。
- exact stable codes：`artifact_native_invalid_request`、`artifact_native_unauthenticated`、
  `artifact_native_forbidden`、`artifact_native_not_found`、`artifact_native_not_ready`、`artifact_native_expired`、
  `artifact_native_unsupported`、`artifact_native_integrity_failed`、`artifact_native_limit_exceeded`、
  `artifact_native_conflict`、`artifact_native_extension_mismatch`、`artifact_native_dialog_unavailable`、
  `artifact_native_permission_denied`、`artifact_native_storage_full`、`artifact_native_io_failed`、
  `artifact_native_unavailable`。cancelled 是用户动作结果，不伪装为 failure code。
- command 层只从该 closed set 返回 typed result；cross-owner/tenant/session/turn/artifact existence 全部折叠为
  `artifact_native_not_found`。custom protocol 不回传上述细节，所有失败保持 body-empty `404`。

### 8.4 已完成的 S7F canonical fixture route

1. Contracts immutable candidate 已含 canonical raw MP4：1,642 bytes、SHA-256 `96ea070c...77dd5`、H.264 High、
   16×16、25fps、0.12s、3 frames、front `moov`、首帧 keyframe。它是唯一 fixture authority，resource tree
   OID `f447129c08b9b39231e33698afc3f2fd875d6b14` 保持不变。
2. Host S3 曾以 `syntheticMP4()` 生成 `ftyp/free/mdat` transport-only bytes；S7F
   `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` 已让 strict-local producer 读取由 canonical bytes 派生、checker
   逐字节校验的 consumer snapshot，且未重新编码或引入 ffmpeg/codec/runtime dependency。
3. S7F evidence 已证明 completed manifest size/digest 与 Contracts exact fixture 一致，
   并覆盖 video GET/HEAD、无 Range `200`、single closed/open/suffix `206`、unsatisfiable `416`、multi-range reject、
   default-off/local-manifest gates。Contracts full commit/tree/source、Desktop pin 均不变。

### 8.5 已完成并修复的 S7A native video boundary

1. 新增隔离的 `chat-artifact-video-native-v1.schema.json` 与 exact commands：
   `chat_open_artifact_video_preview_v1`、`chat_release_artifact_video_preview_v1`、
   `chat_save_artifact_video_v1`。identity envelope 与 S6A 一致且仍只有 session/turn/artifact IDs。
2. `yijie-artifact-video://localhost/v1/<43-char handle>` 绑定 main WebView/process/context/owner/tenant/session/
   turn/artifact。只允许 SQLCipher ready/unexpired `video/mp4` 1..64MiB；open 与 protocol 首次请求进行两次完整
   length/SHA-256/MP4 box+sample validation，之后每次 Range 重验 authority/manifest/BLOB length 并从同一 row 读取。
3. operative limits：2 handles/WebView、1/artifact、2 concurrent responses、64MiB total in-flight；30min absolute +
   5min idle，不存在累计 successful request 终态上限。S7A-REPAIR `34991d8967de9aa2197ab2e8b9b49347774df7a5`
   supersede 原 64-request 候选：Rust 已证明同一 handle 至少 128 次合法 Range 仍有效，真实 WebView 76 次 partial
   response 完成 metadata/playback/seek 且 404=0。Tauri responder 仍是 buffered body；超过 64MiB 或需要
   streaming/new dependency 时停止。
4. 无 Range `GET|HEAD` 返回 200；single closed/open/suffix Range 返回 206；malformed/multi/unsatisfiable 返回 empty
   416 + `Content-Range: bytes */size`。成功只含 MIME/length/Accept-Ranges/必要 Content-Range/no-store/nosniff；
   no CORS/redirect/query/body/ETag/digest/filename/error body，其他错误 empty 404。`connect-src` 不允许该 scheme。
5. save 使用新的 video-only command，但复用 S6A native atomic write kernel；只允许 `.mp4`。Vue 只收
   saved/cancelled/failed + stable code。image schema/commands/limits/behavior 不变，poster_blob 本切片不暴露。

### 8.6 已完成的 S7B UI lifecycle

1. 只为 `kind=video && status=ready` 创建 `<video controls preload="metadata" playsinline>`；无 autoplay、外部
   origin、player library、browser download、remote playback 或 PiP。其他状态/kind 继续 S5 shell。
2. video handle 可被原生元素用于多次 Range，但 Vue 不 fetch、不持久化、不写 Pinia/log/snapshot。error、expiry、
   identity/context/session switch、unmount 时先 pause，清空 `src` 并 `load()`，再 release；迟到 open/save 结果不得污染新 identity。
3. 当前不新增 poster handle；使用稳定 16:9 placeholder，解码后显示首帧。loading/error/expired、keyboard/focus、
   reduced-motion、content-free save feedback 与 sensitive-data negative assertions 已有 component/axe/runtime evidence。

### 8.7 已完成的 S8A native file boundary

1. 独立 Desktop-private `chat-artifact-file-native-v1.schema.json` 只登记
   `chat_read_artifact_file_preview_v1` 与 `chat_save_artifact_file_v1`。closed request <=4,096 encoded bytes，envelope
   为 `schemaVersion/requestId/contextId`，payload 只有 `sessionId/turnId/artifactId`；只接受 `main` WebView 与当前
   `ReadSessions` context。无 open/release handle、custom protocol、CSP、capability、plugin、dependency 或 migration。
2. preview 前后两次查询 SQLCipher authority，复核 owner/tenant/session/turn/artifact、ready/unexpired、kind=file、
   MIME、declared size/BLOB length/digest/revision 与内容格式。第一次读取产生 projection 后立即重读并验证同一 revision；
   任一漂移 fail closed。inline allowlist 仅 `text/plain|text/csv|application/json`；PDF/XLSX 只提供 metadata/native save。
3. exact caps：source <=1,048,576 bytes；projection <=262,144 bytes；response <=524,288 bytes；text/JSON <=2,000 lines、
   每行 <=8,192 UTF-8 bytes；CSV <=200 rows × 50 columns、cell <=4,096 bytes；JSON depth<=32、nodes<=20,000；
   preview <=2 concurrent/WebView、in-flight source<=2,097,152 bytes、同 identity single-flight、10s timeout。
4. UTF-8 only；仅去一个 BOM，CRLF/CR 只在 projection 转 LF；TAB/LF/CR 外 C0、DEL/C1 拒绝 inline，并精确拒绝
   Unicode `Bidi_Control` code points `U+061C`、`U+200E-U+200F`、`U+202A-U+202E`、`U+2066-U+2069`。JSON full
   parse/depth/node audit 后返回 inert source text；CSV 使用 bounded RFC4180 comma parser 并返回 cell strings，不执行
   formula。closed result：text/JSON `{status,mediaType,text,truncated}`；CSV
   `{status,mediaType,rows,truncated}`，不含 name/size/path/digest/href/token/raw error。
5. save allowlist 为当前五种 v3 file MIME，ready-file bytes `1..67,108,864`，与 preview 1 MiB eligibility 相互独立；
   canonical extension `.txt/.csv/.json/.pdf/.xlsx`。用户明确 intent 后，dialog 前校验并释放 bytes，dialog 后重新读取/
   校验，复用 same-dir `0600` create-new/no-follow temp、chunk digest、fsync、atomic replace/RAII。file residue 的唯一
   prefix 是 `.yijie-artifact-file-save-v1-`，exact filename 为
   `.yijie-artifact-file-save-v1-<txt|csv|json|pdf|xlsx>-<process-epoch UUID>-<22-char base64url>.tmp`；仅在用户下一次
   明确选择同一目录保存时删除 prior-epoch 且同时通过 exact marker、regular non-symlink、current uid、`0600`、
   link count 1、size `1..67,108,864` 与对应 format recheck 的条目。当前 epoch、未知/失败条目与 S6/S7 prefix/
   behavior 保持不变。save format recheck：plain/CSV valid UTF-8 且无 NUL、JSON full parse；PDF 复用既有 bounded
   preflight（classic xref/EOF、非加密、无 ObjStm/XRef stream/Prev、objects<=4,096、pages `1..256`、streams<=1,024、
   单/总 decoded stream<=8/32 MiB、ratio<=100:1、expanded traversal<=4,096 stream visits/32 MiB、form depth<=16、
   page-tree depth<=64）；XLSX 复用既有 bounded OOXML validator（entries `1..512`、safe
   unique names、Stored/Deflated、单/总 uncompressed<=8/32 MiB、ratio<=100:1、无 `.bin`/`vbaProject`，且
   `[Content_Types].xml`、`xl/workbook.xml` 与 spreadsheet main content type 匹配）。只允许从 `attachment.rs` 暴露/
   复用 helper，既有 attachment import behavior/limits 不变；PDF/XLSX 不 inline/提取/渲染/执行或自动打开。Vue 只收
   content-free saved/cancelled/failed。

### 8.8 已完成的 S8B renderer 与数据生命周期

1. S8B 等待 S8A immutable PASS 与单独授权；只对 ready file 渲染。text/JSON 为普通 text nodes，CSV cell 为 escaped
   text nodes；PDF/XLSX 为 inline unsupported + native save。禁止 v-html、link、network、formula/macro、Agent/tool action。
2. 用户明确打开后的 bounded safe projection 只在当前组件 local state/DOM 短暂存在；不得进入 Pinia/history/router/
   storage/log/telemetry/diagnostics/snapshot。close/status/artifact/session/context switch/unmount/error/stale response 清空。
   SEC-006 zero-hit 继续覆盖未授权内容、超出已批准 bounded projection 的正文、path/token/digest/savedPath/raw
   error；小文件 projection 可在 caps 内等于完整正文，授权 canary 关闭后必须为 0。
3. search 仅对当前 projection 做 literal/no-regex search，query 1..128 Unicode scalars、最多 100 hits；truncated 时显示
   “仅预览部分内容，截断区未搜索”。重复 read/save single-flight，迟到 response 以 requestId+context/identity 丢弃。

### 8.9 S9A implemented native report boundary

1. 独立 Desktop-private `chat-artifact-report-native-v1.schema.json` 只登记
   `chat_read_artifact_report_preview_v1` 与 `chat_save_artifact_report_v1`。closed request <=4,096 encoded bytes，
   envelope 为 `schemaVersion=1/requestId/contextId/payload{sessionId,turnId,artifactId}`；只接受 `main` WebView 与当前
   `ReadSessions` context。无 URL/handle/protocol/CSP/capability/plugin/dependency/migration。
2. preview/save 前后查询 SQLCipher authority，复核 owner/tenant/session/turn/artifact、ready/unexpired、kind=report、
   exact MIME、declared size/BLOB length/SHA-256/revision 与完整 ReportDocumentV1。S9A 先修复 adapter：JSON Schema
   `maxLength` 按 Unicode scalar、date-time 接受合法 RFC 3339 offset，不增加 section ID/column key unique 或 chart
   labels/values aligned 条件；UI identity 用 ordinal。公共 Contracts/Host/pin/fixture 不变。
3. preview source `1..4,194,304` bytes；projection encoded `<=524,288` bytes；serialized response `<=1,048,576`
   bytes；document depth `<=12`、nodes `<=100,000`、sections `0..64`；每 WebView concurrent preview `<=2`、source
   in-flight `<=8,388,608` bytes、same-identity single-flight、10s timeout。save eligibility 独立为
   `1..67,108,864` validated ready bytes。
4. closed root 只含 `schemaVersion/title/generatedAt/sourceTime/truncated/sections`。summary/paragraph/callout text
   `<=8,192` scalars、heading/title `<=1,024`；metrics `<=32`；table `<=32` columns、前 `<=200` rows、string cell
   `<=1,024`；chart `<=128` labels、`<=16` series、每 series `<=128` finite JSON numbers、总 points `<=2,048`。
   unknown optional 只返回 `ordinal/id/type=unsupported/required=false`，不得返回 original type/payload；unknown required、
   schema/integrity/revision/source/node/depth/response failure 均 fail closed。display cap 只产生 bounded truncation。
5. known text 的 CRLF/CR 规范化 LF；TAB/LF 外 C0、DEL/C1 与 `Bidi_Control` `U+061C`、
   `U+200E-U+200F`、`U+202A-U+202E`、`U+2066-U+2069` 投影为可见 ASCII `\\uXXXX`。projection 仅在
   用户明确打开后的组件 local state/DOM；不得进 Pinia/history/router/storage/log/diagnostics/telemetry/snapshot。
6. save 只保存 canonical report JSON，exact `.json`；dialog 前后双次 authority/full-schema validation，复用 same-dir
   `0600` create-new/no-follow temp、chunk digest、fsync、atomic replace/RAII。residue exact filename 为
   `.yijie-artifact-report-save-v1-json-<process-epoch UUID>-<22-char base64url>.tmp`，只在下一次明确选择同一目录时清理
   prior epoch 且 exact marker/uid/mode/nlink/size/full-schema recheck 全部通过的条目。Vue 只收 content-free outcome。
   PDF/Markdown/image derived export 延期；禁止 browser download、system auto-open、generic fs/shell 与 path result。

### 8.10 S9B-D/S9B-R renderer、chart adapter 与数据生命周期

1. 依赖选择 direct exact `echarts@6.1.0`（Apache-2.0，integrity
   `sha512-q0yaFPggC9FUdsWH4blavRWFmxdrIodbkoKNAjJudAI6CA9gNPxHtV2RcZNEepZVlk4yvBYkOkbk6HIVpIyHZA==`）；
   transitives 仅 `zrender@6.1.0` BSD-3-Clause 与 `tslib@2.3.0` 0BSD，exact integrity 见 Pattern 9.12。
   拒绝 `vue-echarts`、full/root import、CDN/dynamic module。value imports 只允许 core `init/use`、Bar/Line/Pie、
   Grid/Tooltip/Aria 与 CanvasRenderer；HTML legend 代替 ECharts LegendComponent。
2. S9B-D 只允许 exact dependency/lock/notice、semantic chart tokens/theme、pure closed adapter、one-instance
   `YjChartCard` 与 tests/harness/checker，不调 S9A client、不读 report、不改 `components/chat`。bundle baseline
   为 `655731` raw/`206580` gzip-9，最终总上限 `1372531`/`431860`，中间增量上限
   `716800`/`225280`。lock 出现额外 package/install script 或 integrity/license/budget 漂移即停止。
3. 新 token 名只允许 `--yj-color-chart-series-1` 至 `--yj-color-chart-series-8`；light semantic series
   为 `#6B8E23,#356BEA,#0E7490,#7C3AED,#B45309,#C2410C,#DC2626,#475569`，
   dark 为 `#A6CC62,#78A2FF,#46C7D8,#A78BFA,#FBBF24,#FB923C,#F87171,#94A3B8`；其余使用现有
   semantic tokens。Canvas 固定 transparent、280px（窄宽/200% zoom 180px）、`animation=false`、confined
   rich-text tooltip、aria/decal、HTML legend 与可见 table；图表不作为唯一数据载体。
4. adapter 只接受 S9A chart union 并输出 frozen `renderable|fallback` + full text-table model，不接收/输出
   arbitrary ECharts option。bar/line 增强上限为 64 labels/8 aligned series/512 points；pie 为 one aligned
   non-negative/non-zero series/32 labels。D 只提供 pure budget helper；R 每次 explicit open 按 section ordinal
   升序只增强前 4 个 eligible charts，禁止全局/mount/async-order counter；单 chart `<=512` 使总量必
   `<=2048` points。不对齐、超限、非 finite、
   init/setOption/resize 失败只降级当前 section。禁止 formatter/HTML/URL/event/action/toolbox/dataZoom/dataset/
   graphic/custom/transition。model/option 不做值 snapshot，只做 exact-key/serializable/no-function/no-URL 结构断言。
5. current chart projection 没有 unit/data source/time range；UI 显示“报告未提供”，`sourceTime`
   非空时只标为“数据时间”，不做业务推断。S9B-R 只在 report+ready 且明确 open 后读 S9A；
   known text 只 text nodes，unknown 只 fixed marker，canonical save 只调 S9A client，禁止 derived export。
6. projection/model/option 只在 component local state/打开 DOM；close/error/stale/switch/unmount 时使 epoch 失效、
   清内容、unmount chart，card 执行 `clear -> dispose -> ResizeObserver.disconnect`。禁止 Pinia/history/router/
   storage/log/diagnostics/telemetry/snapshot。exact dependency/bundle checker 固定为
   `scripts/check-feat128-s9b-d-dependencies.mjs` 与 `scripts/check-feat128-s9b-d-bundle.mjs`（各有同名
   `.test.mjs`），visual harness 固定 `tests/visual/feat-128-s9b-d/`。S9B-R 等待 S9B-D immutable PASS 与单独授权。

## 9. 可观测性

| Signal | 名称/字段 | 本地成功基线 | 停止阈值 | Runbook 动作 |
|---|---|---:|---:|---|
| Metric | artifact_started_to_visible_ms{kind} | synthetic p95 < 300ms | p95 >= 1000ms | 检查事件 flush/store render |
| Metric | artifact_transfer_result{kind,code} | success fixture 100% | integrity/protocol > 0 | 停止 kind，保留 fixture 和证据 |
| Metric | artifact_preview_memory_bytes{kind} | <= 2.5x content | > 3x 或 OOM | 降级 metadata + save，调查 decode |
| Metric | artifact_staging_bytes/session/global | 低于批准上限 | 达 90% 拒绝新 work | 清理 expired lease，检查 ack |
| Log | artifact_operation_outcome | typed code only | path/body/token canary 命中 1 次 | 立即停止、清理并安全审查 |
| Audit | local save intent aggregate | success/failure only | N/A local | 不记录目标路径；生产前重审 |

当前没有生产 dashboard、告警或观察窗口。上述是候选 signal 与停止条件，不是已存在能力或基线证据。

## 10. 性能、容量与成本

| 项目 | 基线 | 目标/上限 | 测试方法 | 降级 |
|---|---:|---:|---|---|
| 占位可见延迟 | 未测 | p95 < 300ms | deterministic SSE timestamps + Playwright | 保留文本，合并低频 progress |
| UI progress 刷新 | 未测 | <= 10Hz | fake burst events | coalesce latest state |
| 单图片 | N/A | 20 MiB | boundary + magic + pixel fixtures | metadata + save |
| 单视频 | N/A | 64 MiB BLOB / 64 MiB protocol in-flight | Range/boundary/WebView smoke | metadata shell + native save |
| 单文件 | N/A | 64 MiB save；inline source 1 MiB / projection 256 KiB / response 512 KiB | parser/caps/save boundary fixtures | metadata + native save |
| 单 report | N/A | 64 MiB save authority；preview source 4 MiB / projection 512 KiB / response 1 MiB | closed-schema/projection/caps/save fixtures | metadata shell + canonical save |
| 每 turn | N/A | 12 项 / 128 MiB | aggregate admission tests | 拒绝新增、保留已 ready |
| WebView/native preview memory | 未测 | image in-flight 40 MiB；video in-flight 64 MiB；file source in-flight 2 MiB；report source in-flight 8 MiB | process memory sampling + registry/operation counters | metadata + native save |
| 模型成本 | 0（当前不调用） | synthetic 0；真实值未批准 | provider Eval 后记录 | capability off |

## 11. 配置、Feature Flag 与部署

- `YIJIE_AGENT_HOST_V3_ARTIFACTS_ENABLED=false`：Host v3 route/resource master flag，默认关闭。
- `YIJIE_CHAT_ARTIFACTS_V3_ENABLED=false`：Desktop native transfer master flag，默认关闭；关闭后已存 metadata 仍只读。
- `YIJIE_FEAT128_SYNTHETIC_ENABLED=false` + `YIJIE_FEAT128_SYNTHETIC_MANIFEST=feat128-artifact-v1`：只在 `YIJIE_ENV=local` 下接受 exact profile，不能与真实 provider profile 同开。
- kind capability 由 Host readiness 返回，Desktop 不根据模型名猜测。
- 安全关闭行为：继续 v1/v2 文本流；已持久化 Artifact 只读可见，禁止新 transfer/producer。
- 配置验证：非 local 环境拒绝 synthetic；无 v3 contract pin、limits、storage 或 CSP approval 时 master flag 拒绝启动。
- 新旧版本共存：provider-first 支持 v3 route但默认不发；Desktop v3 consumer 与 migration 就绪后再启 synthetic；真实 kind 独立启用。
- 当前无部署平台，deploy/rollback 命令 N/A；本地 source flag 不是生产 kill switch 证据。

## 12. AI 功能专项

- 是否改变 prompt/model/retrieval/tool schema：不改变 prompt/model/retrieval；改变 provider/Runtime output capability projection，并预留未来 tool-produced file/report。
- 固定版本：MiniMax-M3 与 Runtime `0ce5902...` 仅为当前调查基线，不构成 real generation approval。
- 结构化输出 Schema：Agent session event v3 + Artifact manifest + implemented
  `yijie-contracts/jsonschema/report/report-document-v1.schema.json`，canonical media type 为
  `application/vnd.yijie.report+json;version=1`；PDF/Markdown 只允许作为后续 derived export。
- 无答案/拒答：模型没有生成能力时返回文本说明；Desktop 不显示虚假生成入口或从 Markdown 推断 Artifact。
- 提示注入和越权工具控制：report/file 内容是数据，不能触发 Agent tool、network、审批或保存；真实 file/report producer 必须另行定义权限。
- Eval：先 deterministic protocol/UI dataset；真实 provider 需固定 capability、质量、延迟、费用与安全 dataset，且必须单独授权付费调用。

## 13. 方案比较

| 方案 | 优点 | 缺点 | 风险 | 结论 |
|---|---|---|---|---|
| A：SSE 携带 base64/正文 | 实现直观 | 大事件、重放内存、日志/DOM 泄漏、视频不可 seek | 高 | Reject |
| B：Host 长期 Artifact 仓库 + URL | 范围读取容易 | Host 演变为业务库，路径/生命周期复杂 | 高 | Reject for local baseline |
| C：Host 短期 staging + Desktop SQLCipher authority | 保持职责、本地加密、可历史恢复、可回滚 | 需要 transfer/ack/migration | 中 | Recommended |
| D：generic Tauri asset/file protocol | 大媒体 seek 效率好 | path scope、跨 kind 与 seek 攻击面 | 中高 | Reject |
| E：image-only opaque handle custom protocol | Vue 不接收 bytes/path；native 每次复核；可 one-shot/TTL | 需 3 private commands 与 exact CSP scheme delta | 中 | S6A Approved；image only |
| F：独立 video opaque Range protocol | Vue 不接收正文；原生 video 可多次 HEAD/GET/seek；与 image one-shot 隔离 | Tauri response buffered，必须硬限 64MiB 并维护 lifecycle registry | 中 | S7A/S7A-REPAIR/S7B implemented separate PASS |
| G：file bounded private projection + native save | 可搜索安全文本无需 URL/CSP；路径与 raw bytes 留在 native | 用户授权内容会短暂进入组件 DOM，必须严格 caps/清理 | 中 | S8A/S8B implemented separate PASS |
| H：report closed bounded projection + canonical JSON native save | Vue 不接触 raw JSON，unknown payload 不穿透；复用 SQLCipher/atomic save | 复杂 section 必须严格 caps/typed union | 中 | S9A implemented separate PASS |
| I：direct tree-shaken ECharts core + closed adapter + table authority | 满足 Accepted ECharts 标准，不开 generic option/wrapper，可单独回滚 | 新 exact dependency/license/bundle/theme 审查，必须严格 dispose | 中 | Recommended for S9B-D |
| J：`vue-echarts` wrapper | Vue 集成便利 | 仍需 ECharts，额外 generic option/event/lifecycle 与供应链 | 中高 | Reject |
| K：table-only final renderer | 零 chart dependency，可访问性最稳 | 不完成 AC-006 有限图表路径 | 中 | Fallback/rollback only |

## 14. ADR 与批准

- ADR：当前 `N/A`，前提是采用方案 C 且不改变跨仓职责；选择 Host/云长期存储、自定义公开 URL 或 Runtime 核心修改时必须新增 ADR。
- 技术负责人：段成威，结论 `G2 APPROVED for Contracts S1/S2`。
- 安全/数据 Owner：段成威，结论 `G2 APPROVED for Contracts S1/S2`。
- Product/Design：FEAT-128 Pattern 1.5.0 `Accepted`；S6-S9A separate PASS；
  `READY FOR S9B-D ONLY; ACCESSIBLE TABLE IS AUTHORITATIVE; S9B-R WAITS`。Markdown/AC-005 仍 PARTIAL。
- S9B Technical：`APPROVED FOR S9B-D CODING`，只允许 8.10 exact dependency/lock/notice、static core/Canvas、
  semantic theme/card、closed adapter/tests/bundle gate；S9B-R 等待 D immutable PASS 与单独授权。
- S9B Security/Data：批准 D 在 no-report-read/no-option/no-HTML/no-event/no-network、bounded instances 与 dispose
  lifecycle 内编码；R 的 authorized-content DOM lifecycle 仍关闭。
- 结论日期：2026-08-21；G3 仍只对 S3/S4/S5 为 PASS。S9B-D/S9B-R/S10-S11、任何真实 producer 与生产
  activation 仍未执行；所有 FEAT-128 flags 默认关闭，G4 pending。
