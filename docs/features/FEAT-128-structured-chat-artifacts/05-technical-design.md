# FEAT-128 技术设计

## 1. 设计摘要

- 要解决的问题：让 Agent/LLM 输出的图片、视频、文件和报告在 Chat 中以结构化、可流式更新、可历史恢复的 Artifact 展示，而不是 Markdown 链接或一次性文本。
- 选择的方案：Host v3 显式协商 + owner-only 临时资源；Desktop native 校验并写入 SQLCipher 长期 authority；WebView 只消费安全 metadata 和短生命周期 blob preview；report 使用 closed JSON document。
- 关键约束：本地-only、confidential、无云资源、v1/v2 保持兼容、真实 MiniMax output capability 默认关闭、无原始路径/base64/token 进入 SSE 或 WebView state。
- 明确不做：生产部署、云存储、公开分享、raw HTML/脚本报告、任意本地路径、视频转码、真实付费媒体生成、跨设备同步。
- 设计状态：G2 APPROVED；Contracts S1/S2 与 downstream pin-only S2P 已通过，G2A APPROVED。它不构成 Host/Desktop 业务实现、Tauri/CSP/数据库实际变更或生产批准。

## 2. 组件职责与依赖方向

| Component/Repository | 职责 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| yijie-codex | 上游 Runtime canonical item authority | provider/tool output | `imageGeneration` started/completed item | 易界 Artifact 存储、下载或 UI |
| yijie-contracts | v3 wire、report document、error/fixture 权威源 | 已批准业务语义 | OpenAPI/JSON Schema/Proto/AsyncAPI/SDK | Runtime 实现、数据库或 UI |
| yijie-agent-host | Runtime item 归一化、短期 staging、v3 SSE 和认证资源读取 | Runtime notification、synthetic fixture | 安全 Artifact lifecycle + relative resource | 长期业务数据、WebView 渲染、用户保存目标 |
| Desktop native/Tauri | Host fetch、scope/MIME/size/digest 复核、SQLCipher、history、save dialog | v3 event/resource | planned `src-tauri/schemas/chat-ipc-v3.schema.json` private IPC projection 与受控 preview bytes | provider 选择、公共契约权威 |
| Desktop domain/store | 单调状态机、去重、resync、历史 projection | private IPC v3 | renderer view model | wire 解析之外的 I/O、文件写入 |
| Desktop Vue components | 图片/视频/文件/report 展示、预览和可访问交互 | view model、受控 object URL | 用户可观察 UI intent | Host 请求、路径、SQL、保存副作用 |

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
7. renderer 按 kind 提供预览；用户选择保存时，native dialog 取得目标，内容流式写入同目录临时文件并原子替换。
8. Desktop ack 后 Host 可删除 staging；即使 Host 重启，Desktop 已持久化历史仍可只读预览/保存。

### 报告路径

1. producer 生成 `application/vnd.yijie.report+json;version=1`。
2. Host/Contracts validator 拒绝 raw HTML、URL、脚本和 unknown required field。
3. Desktop native 先校验 closed root 和 section envelope，再对 known section 执行 strict payload schema；持久化原始 versioned JSON。
4. report renderer 按 section 顺序展示 `summary | metrics | paragraph | table | chart | callout`；unknown `required=false` section 只显示 unsupported metadata 且不遍历 payload，unknown `required=true` 拒绝整份文档。
5. chart adapter 将有限 schema 映射到易界 ECharts theme，不直接接受任意 option。

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
| PreviewHandle | 当前 WebView 实例 | random handle | 不持久化、不进日志、组件卸载撤销 | open -> close/session switch |
| SaveIntent | 当前用户动作 | request_id | 只写 native dialog 选择目标；不保存路径历史 | dialog -> atomic success/failure |

## 6. 数据与 Migration 专项

- 是否涉及数据库/缓存/持久化：是，Desktop SQLCipher expand；Host 只有短期 staging，不扩展为业务主库。
- 候选 migration：`0008_chat_output_artifacts.sql`，实际名称/DDL 需在 G2A 后由 Desktop authority 确认。

| Phase | Schema/Data change | Old app compatibility | New app compatibility | Validation | Rollback/roll-forward |
|---|---|---|---|---|---|
| Expand | 增加 artifact metadata/content/turn relation/ordinal/expiry 表与索引 | 旧表不删不改；旧 app 对 future schema fail closed | 旧消息合成空 Artifact list | migration checksum、populated v7 fixture、FK/unique tests | 升级前完整加密备份；否则 v8 roll-forward |
| Backfill | N/A；旧消息没有 Artifact，不批量制造记录 | 完全不变 | reader 返回空集合 | legacy history tests | 无 backfill job |
| Switch | v3 completed 先 transfer/commit，再暴露 ready | v1/v2 路径继续写旧消息 | v3 history 恢复 Artifact | crash points、idempotent replay、WAL/reopen | 关闭 v3 flags，保留已存 Artifact 只读 |
| Contract | 本期不删除 v1/v2、旧 message 字段或旧 migration | 旧 consumer 继续 | 双轨共存 | v1/v2 equality + v3 conformance | 未来独立清理 Feature |

G2 选择 content 使用 SQLCipher BLOB 增量 I/O，避免 plaintext app-data 文件。`local_committed_at` 是事务提交成功时间，`expires_at = local_committed_at + 168h`。若性能验证证明 64 MiB BLOB 不可接受，必须重新打开 G2 选择版本化加密文件格式；不得静默落为 owner-only plaintext。

## 7. 一致性与韧性

- 事务边界：单个 Artifact transfer 以一个 SQLCipher transaction 提交 metadata、content 和 terminal projection；UI ready 只在 commit 后发生。
- 并发冲突：同 artifact 只允许一个 active transfer/save intent；duplicate completed 复用同一 operation。
- 幂等：Host event_id/sequence、Desktop transfer operation 和数据库 unique key 共同防重复。
- 超时/取消：Host resource read、Desktop transfer、preview decode、save 和 resync 均使用 bounded timeout/AbortSignal；turn interrupt 不自动删除已 ready Artifact。
- 重试/退避/上限：仅 retryable transport/staging error 可重试，指数退避最多 3 次；integrity/protocol/unsupported 不自动重试。
- 限流/熔断/降级：每项 20/64 MiB、每 turn 128 MiB/12 项；Host 每 session staging 256 MiB、全局 1 GiB、lease 从 `staged_at` 起 24 小时。staging 使用 app-private encrypted spool，不使用 1 GiB 进程内大对象。达到上限拒绝新 Artifact，不驱逐正在读取或已持久化内容。
- 部分失败与补偿：一项失败不回滚其它 ready；Desktop commit 失败不 ack Host；Host ack 丢失依靠 TTL 清理。
- 资源释放：object URL、video handle、timer、AbortController、temp file、range response 和 staging lease 都必须在关闭/切换/失败时释放。

## 8. 安全设计

- 认证入口：Host 既有 owner-only loopback bearer；WebView 不读取 bearer。
- 资源级授权：每次 GET/HEAD 同时校验 token、session、artifact ownership、lease 和 state。
- 租户隔离：Desktop SQL query 与 IPC command 强制 owner_user_id + tenant_id + session_id；opaque ID 单独不构成权限。
- 输入验证：closed kind/status/error/report schema；safe filename；MIME + magic；长度、像素、时长、行列、series、UTF-8 与 digest limits。
- Secret/token 边界：API Key 只留 Runtime 子进程环境；Host bearer 只在 native bridge；content href 为相对路径且无 query token。
- PII/日志脱敏：日志只记录 kind、typed code、byte bucket、duration bucket 和 opaque correlation；不记录标题、文件名、正文、path、digest 或 raw provider error。
- 高风险审批：N/A；Artifact 查看不是电商业务写操作。保存仍需用户明确 native dialog intent，不能后台自动写文件。
- 审计：本地阶段只记录 aggregate typed operation outcome，不记录目标路径；生产审计方案当前 N/A/not designed。
- CSP/capability：图片继续用现有 `blob:`；视频 preview 候选只增加精确 `media-src 'self' blob:`。native save command 与 dialog scope 必须单独批准，禁止通用 filesystem/shell capability。

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
| 单视频/文件/report | N/A | 64 MiB | range/stream/boundary fixtures | 不内嵌 preview，仅保存 |
| 每 turn | N/A | 12 项 / 128 MiB | aggregate admission tests | 拒绝新增、保留已 ready |
| WebView memory | 未测 | <= 2.5x preview bytes | process memory sampling | lazy load/revoke/object URL |
| 模型成本 | 0（当前不调用） | synthetic 0；真实值未批准 | provider Eval 后记录 | capability off |

## 11. 配置、Feature Flag 与部署

- `YIJIE_CHAT_ARTIFACTS_V3_ENABLED=false`：Host/Desktop master flag，默认关闭。
- `YIJIE_ARTIFACT_SYNTHETIC_PROFILE_ENABLED=false`：只在 `YIJIE_ENV=local` 与固定 test manifest 下接受 exact `true`，不能与真实 MiniMax generation 同开。
- kind capability 由 Host readiness 返回，Desktop 不根据模型名猜测。
- 安全关闭行为：继续 v1/v2 文本流；已持久化 Artifact 只读可见，禁止新 transfer/producer。
- 配置验证：非 local 环境拒绝 synthetic；无 v3 contract pin、limits、storage 或 CSP approval 时 master flag 拒绝启动。
- 新旧版本共存：provider-first 支持 v3 route但默认不发；Desktop v3 consumer 与 migration 就绪后再启 synthetic；真实 kind 独立启用。
- 当前无部署平台，deploy/rollback 命令 N/A；本地 source flag 不是生产 kill switch 证据。

## 12. AI 功能专项

- 是否改变 prompt/model/retrieval/tool schema：不改变 prompt/model/retrieval；改变 provider/Runtime output capability projection，并预留未来 tool-produced file/report。
- 固定版本：MiniMax-M3 与 Runtime `0ce5902...` 仅为当前调查基线，不构成 real generation approval。
- 结构化输出 Schema：Agent session event v3 + Artifact manifest + planned
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
| D：自定义 Tauri asset protocol | 大媒体 seek 效率好 | 新 capability/CSP/路径协议攻击面 | 中高 | Defer；只有 BLOB 性能失败后重开 G2 |

## 14. ADR 与批准

- ADR：当前 `N/A`，前提是采用方案 C 且不改变跨仓职责；选择 Host/云长期存储、自定义公开 URL 或 Runtime 核心修改时必须新增 ADR。
- 技术负责人：段成威，结论 `G2 APPROVED for Contracts S1/S2`。
- 安全/数据 Owner：段成威，结论 `G2 APPROVED for Contracts S1/S2`。
- Product/Design：FEAT-128 Pattern 1.0.0 `Accepted`。
- 结论日期：2026-08-20；G2A 已通过，可按依赖先开始 S3、再开始 S4。当前尚未修改 Host/Desktop 业务代码，任何 producer 仍默认关闭。
