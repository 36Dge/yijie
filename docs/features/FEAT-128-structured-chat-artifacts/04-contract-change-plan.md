# FEAT-128 契约与兼容变更计划

## 1. Contract Impact 结论

- 分类：`semantic`。
- 理由：本需求计划新增显式协商的 Agent Session v3 事件流、Artifact 生命周期事件和
  owner-only 资源读取表面。新 path 本身是 additive expand，且 v1/v2 wire、事件联合、游标、
  重放和终态语义保持不变；但 Artifact 作为新的 response/event 输出会改变新 consumer 对
  item、进度、资源可用性、失败和本地持久化的解释，因此按最高风险归类为 semantic，而不是
  仅按新增 path 归类为 additive。
- 边界：`yijie-agent-host` 本机 HTTP/SSE producer、`yijie-desktop` native consumer、固定
  Codex Runtime `item/started` / `item/completed` 投影，以及 Desktop 本地 Artifact 历史快照。
- 业务语义变化：Agent 输出不再只有 Markdown 文本；v3 consumer 可在生成尚未完成时接收
  Artifact started/progress，并在 ready/failed 终态后预览、读取或下载对应资源。
- 安全语义变化：Artifact 正文不进入 SSE envelope、日志、trace、metric 或 Host bbolt；事件只
  携带安全 metadata 和 owner-only 相对引用。Runtime 的 `savedPath` 绝不向 Desktop/WebView
  投影。
- 旧版本隔离：`/v1/agent-sessions/{agent_session_id}/events` 与
  `/v2/agent-sessions/{agent_session_id}/events?event_schema_version=2` 必须保持逐字节兼容；Host
  只有在 consumer 调用 `/v3/.../events?event_schema_version=3` 时才可发出 Artifact 事件。

如果实现向 v1/v2 发出新事件、在既有 `item.completed` 中增加旧 schema 拒绝的字段、改变既有
游标/终态解释，或让旧 Desktop 无法继续使用 v1/v2，则分类升级为 `breaking`，必须停止当前
方案并重新设计版本迁移。

## 2. 权威源与责任

| 契约/边界 | 权威源类别 | 仓库与计划路径 | Owner | Producer | Consumers |
|---|---|---|---|---|---|
| Agent Session v3 HTTP/SSE、Artifact content/poster GET/HEAD 与 ACK | central OpenAPI | `yijie-contracts/openapi/agent-host/agent-host.yaml` 的新 `/v3/agent-sessions/{agent_session_id}/events`、`.../artifacts/{artifact_id}/content|poster` 与 `.../ack` operations | 段成威 / Contracts Owner | `yijie-agent-host` | `yijie-desktop` native bridge |
| v3 SSE event envelope、Artifact lifecycle payload | central JSON Schema | `yijie-contracts/jsonschema/agent/session-event-v3.schema.json` | 段成威 / Contracts Owner | `yijie-agent-host` | Desktop event adapter/store/UI |
| Report document v1 payload | central JSON Schema | `yijie-contracts/jsonschema/report/report-document-v1.schema.json`; canonical media type `application/vnd.yijie.report+json;version=1` | 段成威 / Contracts Owner | synthetic producer first; future report producer separately approved | Desktop report renderer/export |
| 异步 channel 与 Protobuf 等价投影 | central AsyncAPI/Protobuf | `yijie-contracts/asyncapi/events.yaml`、`protobuf/yijie/events/v3/agent_session.proto` | 段成威 / Contracts Owner | Agent Host / future async adapter | generated SDK consumers |
| Runtime image-generation item | pinned Runtime canonical schema | `yijie-codex@0ce5902ed400866be0196886bb78f693a004d68d`，`codex-rs/app-server-protocol/schema/json/v2/ItemStartedNotification.json` 与 `ItemCompletedNotification.json` 的 `imageGeneration` item | Runtime Owner | fixed Codex Runtime | Agent Host adapter |
| Runtime 到归一化 Artifact 的映射 | reviewed compatibility projection | `yijie-contracts/compatibility/agent-host-runtime-v1.json` 的后续 additive projection + Agent Host conformance | Contracts/Runtime Owner | Agent Host | Desktop v3 consumer |
| Artifact durable history 与本地文件所有权 | private Desktop data authority | implemented `yijie-desktop/src-tauri/schemas/chat-ipc-v3.schema.json` (`x-yijie-schema-version=3`) plus metadata-only `chat_load_history_v3` and private SQLCipher v8 authority；preview/save commands remain planned for later approved slices | Desktop/Data Owner | Desktop native | later Desktop versions/UI |

生成 SDK、Host snapshot、手写 adapter、fixture、数据库行和 UI view model 均为派生表示，不成为
第二权威源。JSON Schema 是 SSE payload 权威；OpenAPI 定义 transport/auth/resource response；
Protobuf 和 AsyncAPI 必须通过一致性测试证明等价，不得复制后独立演进。

当前上游事实与限制：

- 固定 Runtime canonical schema 已有 `imageGeneration` item，字段为 `id`、`status`、
  `revisedPrompt`、base64 PNG `result` 和可选 `savedPath`，并通过通用 `item/started`、
  `item/completed` 通知出现。S3 只实现 exact-local synthetic producer；真实 Runtime `imageGeneration`
  adapter 仍未投影，不能由 synthetic 证据推导为 MiniMax/Runtime 能力。
- 固定 Runtime 的 image-generation extension 只在其 provider capability gate 通过时暴露；当前
  MiniMax Host profile 没有已验证的 Images API capability 或真实生成证据。canonical item 存在不
  等于 MiniMax 当前可发出该 item。
- video、file、report 当前没有已登记的 canonical Runtime item 或其它真实 producer。
  exact-local synthetic profile 可以为四种 kind 发固定 fixture；`provenance=provider|tool` 的真实 producer 继续分别 blocked。

## 3. 语义设计

### v3 事件流请求

- `GET /v3/agent-sessions/{agent_session_id}/events` 沿用本机 owner-only bearer、`Last-Event-ID`、
  `stream_id` 和权威 v1/v2 query 参数 `after` 的语义；不新增 `after_sequence` 别名。
- query `event_schema_version=3` required 且只接受 `3`；缺失或其它值返回现有稳定
  `invalid_event_cursor` 类别的 `400`，不得静默降级到 v1/v2。
- v3 保留 v2 的全部 lifecycle/reasoning variants，并新增下列四个 closed variants：
  `item.artifact.started`、`item.artifact.progress`、`item.artifact.completed`、
  `item.artifact.failed`。
- Artifact variants 均 required `turn_id`、`item_id`、`ordinal`，顶层 `terminal=false`。Artifact 终态只关闭
  对应 `artifact_id`；只有既有 `turn.completed` 保持 turn terminal。

### Artifact 标识与类型

- `artifact_id`：required、由 Host 生成且不可复用的 UUID（wire schema 使用 `string` + `format: uuid`；
  canonical lowercase 表示）。consumer 将其视为 opaque identity，不解析、不从文件名、路径或 Runtime
  `item_id` 派生。Runtime image slice 由 Host 维护 `item_id -> artifact_id` 的稳定映射，且不得把
  `artifact_id` 与 `item_id` 直接混用。
- `kind`：closed `image | video | file | report`。新增第五种 kind 属于新的 output enum 值，必须
  重新执行 semantic review；未证明 v3 consumer 容忍前不得直接发出。当前 v3 schema/Host emission
  对 kind 保持 closed，Host 不发未评审的第五种 kind。Desktop adapter 先用宽 envelope 捕获未来的
  未知 kind/version，再在已知 variant 上执行 strict schema；未知值只创建 `unsupported` 占位并继续
  处理同 turn 的已知事件，不请求 content、执行内嵌预览或写入已知 kind 的持久化字段。
- `display_name`：optional sanitized UTF-8，1..255 bytes；不得含路径分隔符、控制字符或本机路径。
- `media_type`：started/progress 可省略，completed 时 required。consumer 只对明确 allowlist 做
  内嵌预览；`text/html`、SVG、脚本型或未知媒体默认作为下载，不直接注入 WebView DOM。
- `provenance`：safe enum `synthetic | provider | tool`；local synthetic profile 必须显式发送
  `synthetic`，Desktop 持久化该值并显示“本地合成演示”来源标识，不得根据 kind、模型名或文件名猜测。
  `provider`/`tool` 只有在对应 capability、权限和 producer review 通过后才可发送；缺失或未知值不得
  被展示为真实模型生成。

### 生命周期与流式输出

| Event | Required payload | 语义 |
|---|---|---|
| `item.artifact.started` | `artifact_id`, `kind`, `provenance`, `status=in_progress` | producer 接受生成/导出工作后立即发出；不得等待完整 bytes、digest 或最终路径 |
| `item.artifact.progress` | `artifact_id`, `kind`, `provenance`, `status=in_progress`，以及 `progress_percent` 或 `stage` 至少一项 | 只转发上游真实进度；`progress_percent` 为 0..100 且同一 artifact 不回退，未知进度只发 `stage`，不得伪造百分比 |
| `item.artifact.completed` | `artifact_id`, `kind`, `provenance`, `status=ready`, `media_type`, `size_bytes`, `sha256`, `content_href` | 只有资源已经可通过 owner-only resource GET 读取且 size/digest 已验证时发出；本 candidate 不发送 partial preview href；`poster_href` optional |
| `item.artifact.failed` | `artifact_id`, `kind`, `provenance`, `status=failed`, `error_code`, `retryable` | Artifact 终态，无 content/preview/poster href；message 若存在必须脱敏且不含 provider 原文、路径或正文 |

- 同一 `(agent_session_id, turn_id, artifact_id)` 必须先有 started，之后允许零到多个 progress，最后
  恰有一个 completed 或 failed。终态后同一 stream 内的后续 progress/第二终态为 protocol error，
  producer 必须丢弃并记录不含正文的安全诊断。
- SSE delivery 沿用 at-least-once。`sequence` 在一个 `stream_id` 内全局单调；consumer 以
  `event_id` 去重，并按 sequence 应用状态。重复 replay 不得重复下载、重复持久化或生成第二条
  Artifact 记录。
- v3 replay 仍是 Host 当前进程内有界 replay。Host 重启产生新 `stream_id`，旧 `content_href`
  可失效；Desktop durable history 必须由 Desktop 自己保存的 metadata/resource identity 恢复，
  不得把 Host replay 或 Runtime `savedPath` 当作 durable authority。
- started/progress 必须可在 turn 完成前独立 flush；实现不得为了聚合完整 Markdown、等待所有
  Artifact 或计算最终 digest 而阻塞其它 SSE 事件。
- wire `item.artifact.completed` 的 `status=ready` 只表示 Host staging 中的资源已经完成校验并可通过
  owner-only GET/HEAD 读取，不表示 Desktop 已完成本地 transfer。Desktop 消费 completed 后进入本地
  `transferring`，只有 digest/size/MIME 校验和 SQLCipher commit 成功才进入 local `ready`。
- 当前 candidate 的 progress 只承载真实阶段或百分比，不承载 partial bytes、章节快照或渐进 preview URL。
  未来若要支持 partial preview，必须新增版本化 resource reference、独立 digest/size、权限、替换和
  cleanup 语义，经 semantic review 后才能扩展 v3。

### Artifact 资源读取

- `content_href` 与 optional `poster_href` 必须分别是 Host 生成的同 session `/content`、`/poster` 相对 path，不允许 absolute URL、
  `file://`、本机绝对路径、用户输入 URL 或 bearer query parameter。`preview_href` 不在当前 candidate
  emission 中，未来 partial preview 必须按单独版本化 resource 语义评审。
- `GET|HEAD /v3/agent-sessions/{agent_session_id}/artifacts/{artifact_id}/content` 和 optional `/poster` 使用与事件流相同的
  owner-only bearer，并验证 path session 与 artifact ownership。跨 session、未知 artifact 或
  bearer 缺失均 fail closed。
- ready resource 返回准确 `Content-Type`、`Content-Length`、digest-backed `ETag`、
  `Cache-Control: no-store`、`X-Content-Type-Options: nosniff` 和安全 `Content-Disposition`。
  video/file 大对象支持单一 byte range：合法范围返回 `206` 与 `Content-Range`，非法范围返回
  `416`；不支持 range 的 producer 不得宣称可 seek 视频预览。
- stable failures：未生成完成为 `409 artifact_not_ready`，当前进程已知但资源已释放为
  `410 artifact_expired`，未知 session/artifact 为不泄露存在性的 `404 artifact_not_found`，
  完整性校验失败为 `500 artifact_integrity_failed` 并立即撤销该 resource。
- WebView 不直接持有 Host bearer。Desktop native bridge 负责 fetch、大小/digest 复核和 SQLCipher authority；
  S6A 只向 WebView 签发短期 one-shot opaque image handle，或执行 native save。关闭/替换/session switch 时
  release handle；不得用 public Contracts 暴露 Desktop-private preview/save surface。

### Artifact ACK 与 staging cleanup

- `POST /v3/agent-sessions/{agent_session_id}/artifacts/{artifact_id}/ack` 只由 Desktop native 在
  SQLCipher transaction 成功提交后调用。request required `ack_id`、`size_bytes`、`sha256` 和
  `local_committed_at`；Host 复核 session/artifact、ready state、size/digest 与 owner bearer。
- `ack_id` 是 UUID 幂等键。同一 artifact + 相同 canonical request 重放返回相同 `200` receipt；同一
  `ack_id` 携带不同 canonical input 返回 `409 artifact_ack_conflict`。资源未 ready 为
  `409 artifact_not_ready`，metadata mismatch 为 `409 artifact_ack_mismatch`，未知/已清除且无 tombstone
  为不泄露存在性的 `404 artifact_not_found`。
- response required `artifact_id`、`ack_id`、`status=acknowledged`、`cleanup_status=pending|completed` 和
  `acknowledged_at`。Host 可异步清理 encrypted spool；receipt 只证明 Host 接受提前清理，不证明 Desktop
  retention/delete cleanup。Host 为幂等重放保留无正文、无路径、无 digest 的最小 tombstone 到 lease TTL。
- ACK 丢失时 Desktop 可安全重放；始终失败时 Host 仍由 `staged_at + 24h` TTL 清理。Host 重启先清除旧
  encrypted spool，Desktop 未提交的内容变为 typed unavailable，不根据 path 猜测恢复。

### Report document v1 compatibility envelope

- 根对象与六类已知 section payload 使用 `additionalProperties=false`。每个 section 显式 required
  `id`、`type`、`required`、`payload`。
- known `summary|metrics|paragraph|table|chart|callout` 进入 strict payload schema；不得包含 HTML、URL、
  ECharts option 或可执行内容。
- unknown `type` 仅在 `required=false` 时由 schema 接受为 opaque JSON payload。consumer 只能显示
  `unsupported` metadata，不遍历、渲染、链接或执行 payload；`required=true` 的 unknown section 拒绝整份报告。
- unknown optional payload 仍受 JSON 编码后 `128 KiB` 与最大嵌套深度 `8` 的适配器上限约束；越界即拒绝整份报告，
  不能以 fail-soft 为由接受无界对象。
- `application/vnd.yijie.report+json;version=1` 与完整 document bytes/digest 是预览和保存的同一版本。
  PDF/Markdown 不进入本 candidate。

### 失败、取消与部分成功

- 初始稳定 `error_code` 集合：`generation_failed`、`unsupported_provider`、
  `resource_unavailable`、`limit_exceeded`、`integrity_failed`、`protocol_error`、
  `turn_interrupted`、`host_shutdown`。新增 code 是 output enum 变化，必须先完成 consumer 兼容评审。
- turn interrupt/Host shutdown 时，所有已 started 且未终态 Artifact 必须在可发送时以 failed
  finalization 结束；断线导致无法发出时，Desktop 以 stream gap 将本地状态标为 interrupted，
  不伪造 ready。
- 一个 Artifact failed 不自动把其它 Artifact 标为失败，也不改变既有 `turn.completed` 状态；
  部分成功由每个 artifact 终态加 turn terminal 共同表达。
- 自动重试不得复用新 `artifact_id` 覆盖旧 failed 记录。若产品允许重试，新的 attempt 使用新的
  artifact id，并通过未来可选 `supersedes_artifact_id` 扩展；该字段当前不进入 v3 candidate。

## 4. 兼容方向

```text
新 response/event：先交付 v3 consumer，producer 再启用 v3 emission
v1/v2：保持旧 path、schema、游标、重放和事件集合不变
v3：显式 path + event_schema_version=3，不做内容丢失型自动降级
```

| Version combination | Request | Response/Event | Expected | Test |
|---|---|---|---|---|
| old Host + old Desktop | v1/v2 unchanged | v1/v2 unchanged | 现有文本、reasoning 和 turn 流程不变 | v1 wire equality + v2 canonical fixture regression |
| new Host + old Desktop | old Desktop 不调用 v3 | Host 只在 v3 route 发 Artifact | 旧 consumer 不接触未知 variant | Host dual-route isolation test |
| old Host + new Desktop | v3 route 返回 404/unsupported | 无 Artifact event | Desktop fail closed，隐藏/禁用 Artifact 能力；不得从 Markdown 猜测文件或回退丢失结构 | Desktop readiness/404 negative test |
| new Host + new Desktop，feature off | v1/v2 或 v3 不激活 producer | 无新 Artifact emission | 默认行为与当前候选一致 | default-off source/config test |
| new Host + new Desktop，synthetic producer on | v3 explicit negotiation | started -> progress* -> completed/failed | UI 可渐进展示、去重、恢复和下载 synthetic resource | canonical end-to-end fixture test |
| new Host + new Desktop，MiniMax real image | v3 explicit negotiation | 仅在 provider capability 获证后发 image | 当前状态 `PENDING/BLOCKED`，不得用 Runtime schema 存在替代真实 capability | fixed-provider capability + bounded paid eval，需用户单独授权 |
| exact-local synthetic emits video/file/report | v3 explicit negotiation | 对应 kind lifecycle，`provenance=synthetic` | 允许固定 fixture 验证 contract/UI；不得冒充真实能力 | synthetic producer conformance + failure/range tests |
| real producer emits video/file/report | v3 explicit negotiation | `provenance=provider|tool` | `Unknown/BLOCKED`；必须先形成 canonical producer、容量、安全和取消语义 | producer-specific conformance + failure/range tests |
| new Desktop reads old local history | no v3 wire required | legacy text/history | 旧记录保持可读，未保存的 Host ephemeral resource 不伪造为可下载 | Desktop migration/history tests |
| rollback to old Host | new Desktop stops v3 calls | no new events | 关闭 feature flag 后继续 v1/v2；Desktop 已持久化 Artifact 保持本地只读 | rollback compatibility test |

## 5. 支持基线与 Breaking Check

| Baseline version | Full commit | Support window | Check command | Required result/evidence |
|---|---|---|---|---|
| published `contracts-v0.2.0` | `f16a497e1377f45747f8ff9292b4b60cf2027f88` | supported，直到正式弃用 | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | `PASS`：结构检查与 v1 wire equality 通过 |
| unreleased `0.3.0` local candidate | `747cf740f2d91e76e5c1a130e8e009f1efa821b8` | FEAT-128 前 Host/Desktop pin 基线 | `./scripts/check-breaking.sh 747cf740f2d91e76e5c1a130e8e009f1efa821b8` + v2 source/fixture equality test | `PASS`：v2 path、schema、reasoning limits、fixtures 与 generated surface unchanged |

- 已形成版本：未发布的 `0.4.0 local candidate`，不可变 commit
  `ea48fe190e18afba728712d1e2cc79cda57f581b`。它不重新打开 `0.3.0` candidate，也不等于 tag 或 release。
- 计划不可移动 tag：`contracts-v0.4.0`；当前不存在，不得写成已发布或 supported。
- 自动 breaking check 不能证明未知事件、资源授权、range、重放、终态或 Desktop 持久化语义，
  必须补人工 semantic review 和双向 conformance。

## 6. Generator 与下游 Pin

| Consumer/Projection | Contract version/tag | Full commit | Digest | Generator/version | Owner/Status |
|---|---|---|---|---|---|
| TypeScript SDK | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | OpenAPI `cf72ba8d...`; event v3 `87b12840...`; report v1 `94715e5b...`; proto `5021a034...` | `openapi-typescript 7.13.0`、`json-schema-to-typescript 15.0.4`、`protoc-gen-es 2.12.1` | Contracts Owner / PASS |
| Go SDK/Host HTTP types | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | generated Host `4b7c5bb7...`; generated proto `d07e6781...` | `oapi-codegen v2.7.2`、`protoc-gen-go v1.36.11` | Contracts Owner / PASS |
| Host SSE JSON adapter | `0.4.0 local candidate` | exact contract pin from `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; S3 implementation `4017785adb08e1114781d3d844e9a10a683fa933` | event v3 `87b12840...`; report v1 `94715e5b...` | explicit adapter exception `EXC-128-001`; canonical-schema checker | Agent Runtime Owner / S3 PASS；local synthetic only |
| Desktop Rust adapter | `0.4.0 local candidate` | exact contract pin from `96094419d963745529ed0fa246919089e659f20d`; S4 implementation `09220dd8319cfb8ec0c4d1531514bb5169107983` | source/fixture identities + 10 implementation file digests recorded in lock | explicit adapter exception `EXC-128-001`; source/fixture/implementation validator | Desktop Owner / S4 PASS；native foundation only |

不得从 dirty sibling、floating branch 或文档中的计划 tag 生成下游发布产物。正确顺序是 Contracts
source/generated PR 通过 -> 形成不可变完整 commit -> Host/Desktop 分别 exact pin -> conformance
通过 -> 本地 feature flag 才允许开启。

## 7. Fixtures 与 Conformance

| Fixture/Test | 唯一权威位置 | Producer test | Consumer test | 状态/通过条件 |
|---|---|---|---|---|
| image lifecycle | `yijie-contracts/tests/fixtures/agent/session-event-v3/image-{started,progress,completed,failed}.json` | canonical synthetic envelope/schema 已通过；Runtime mapper 属 S3 | Desktop pin checker读取同一 fixture；渐进 UI/transfer 属 S4-S6 | CONTRACT PASS；使用合成 PNG 与相对 href，不含本机路径 |
| video lifecycle | `.../video-{started,progress,completed,failed}.json` | exact-local synthetic contract fixture 已通过；不得冒充 Runtime 能力 | Desktop pin checker通过；poster/range/UI 属 S3-S7 | CONTRACT PASS；真实 producer 单独 blocked |
| file lifecycle | `.../file-{started,progress,completed,failed}.json` | synthetic safe filename、size、digest contract fixture 已通过 | Desktop pin checker通过；native save 属 S4/S8 | CONTRACT PASS；真实 producer 单独 blocked |
| report lifecycle/document | `.../report-{started,progress,completed,failed}.json` + `tests/fixtures/report/report-document-v1/*` | known、unknown optional、unknown required 与 injection fixtures 通过 | Desktop pin checker通过；renderer/fallback 属 S4/S9 | CONTRACT PASS；真实 producer 单独 blocked |
| artifact ACK | `tests/fixtures/agent/host-v3/artifact-ack-{request,response}.json` | request/receipt schema 与幂等错误语义通过 | Desktop 只允许在 SQLCipher commit 后发送，业务实现属 S4 | CONTRACT PASS |
| lifecycle negatives | `yijie-contracts/tests/agent-session-events-v3.test.mjs` | closed variants、ordinal、MIME/size/href/report limits 被自动验证 | Desktop 对重复、乱序、gap、expired fail closed 属 S4 | CONTRACT PASS |
| Runtime canonical projection | Host test fixture derived from pinned `ItemStartedNotification` / `ItemCompletedNotification` imageGeneration shape | parser 保留 id/status/result，验证 base64 PNG、size/digest；不输出 path | Desktop 只消费归一化 v3，不依赖 Runtime DTO | `PENDING`；固定 Runtime commit/schema tree 必须与 compatibility lock 一致 |
| v1/v2 isolation | existing v1/v2 fixtures plus equality assertions | v1/v2 source/wire 对两个 baseline 均不变 | public/v2 downstream pin checker 继续通过 | PASS |

所有 fixture 只使用合成数据。Feature 目录只引用 canonical fixture 路径和 digest，不复制 payload。

## 8. 合并、部署、启用与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | G2 批准 v3 schema、resource/ACK、error codes、容量/TTL ownership 与 `0.4.0` 版本计划 | `yijie` / 段成威 | Owner sign-off；真实 provider 保持 blocked | 重开 G2，继续 v1/v2 |
| 2 | S1/S2 实现 Contracts source、fixtures、生成物、一致性测试和 release note candidate | `yijie-contracts` / Contracts Owner | G2 PASS | 丢弃未发布 candidate，不影响现有 tag |
| 3 | 形成不可变 Contracts commit；完成双基线 breaking、v1/v2 equality 与 semantic review | `yijie-contracts` | sequential generate/lint/test/build/breaking PASS | 不创建 tag、不允许 producer 激活 |
| 4 | S2P 仅在 Host/Desktop 写入 exact pin、canonical snapshot/fixture checker 与 adapter 例外；不实现 route、迁移、transfer 或 UI | Host + Desktop / consumer Owners | Contracts immutable commit/digests | 回退 pin-only commit，业务行为不变 |
| 5 | G2A 审核 Contracts 与两个 consumer pin/conformance | `yijie` / 段成威 | 第 2-4 步全部 PASS | G2A 保持 pending，禁止 S3/S4 |
| 6 | G2A 后按 S3/S4 实现 Host route/staging/synthetic 与 Desktop native persistence/IPC；默认 flag off | Host + Desktop | G2A PASS | 关闭 v3 route/flag，v1/v2 继续服务 |
| 7 | 完成 S5-S10 UI、synthetic walking skeleton 与安全/视觉/性能证据 | Host + Desktop | S3/S4 conformance | 关闭 local flag；不删除用户已保存文件 |
| 8 | MiniMax image real activation | Runtime/Host/Desktop | `PENDING`：能力、费用/限流、固定模型/API 和 bounded eval 获单独授权 | 禁用 image producer |
| 9 | video/file/report real producer activation | 对应未来权威 producer Owner | `Unknown/BLOCKED`：每类独立 producer/security/eval 获批 | 每种 kind 独立 flag 关闭 |

本需求明确是本地服务候选：不购买云服务器、数据库或对象存储，不执行 production deployment、
tag publish 或真实用户 rollout。生产部署相关子项为 `N/A for current local-only scope`，但 G5/G6
不会因此自动通过或被豁免，当前均保持 `NOT PASSED`；本地候选仍须完成相应代码、验证、Review 和
用户验收记录。未来一旦引入云端资源、远程 URL、跨设备同步或生产发布，必须重新打开安全、数据、
成本、部署和回滚评审。

## 9. 实际检查证据

S1/S2 与 S2P 完成后，严格按依赖先执行 Host S3，再执行 Desktop S4。下表分别保留 pin preflight 与
业务基础切片的证据；S3/S4 PASS 不证明 renderer、synthetic 端到端、真实 provider 或生产能力。

| 检查 | Command | CWD | SHA/版本 | Exit code | 结果 | 证据位置/解除条件 |
|---|---|---|---|---:|---|---|
| generate | `pnpm generate` | `yijie-contracts` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | 0 | PASS | locked OpenAPI/JSON Schema/Proto/AsyncAPI 生成无漂移 |
| lint | `pnpm lint` | `yijie-contracts` | locked Node/pnpm/Go toolchain | 0 | PASS | source、generated 与 cross-format checks 通过 |
| test | `pnpm test` | `yijie-contracts` | immutable candidate | 0 | PASS | Node `39/39` + Go 全部通过 |
| build | `pnpm build` | `yijie-contracts` | immutable candidate | 0 | PASS | TypeScript SDK compile 通过 |
| published baseline breaking | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | `yijie-contracts` | `contracts-v0.2.0` | 0 | PASS | 结构检查 + v1 equality |
| local candidate compatibility | `./scripts/check-breaking.sh 747cf740f2d91e76e5c1a130e8e009f1efa821b8` | `yijie-contracts` | FEAT-127 candidate | 0 | PASS | v2 source/fixture equality + semantic review |
| Host pin conformance | `make sync-contracts && make contract-check && make lint && make test` | `yijie-agent-host` | pin commit `dea84d0768ebc017b7ee5faedab7f9a49ce74875` | 0 | PASS | exact pin/snapshot/generated types 与既有 Host baseline 通过 |
| Host S3 | `make contract-check && make lint && make test && make runtime-test` | `yijie-agent-host` | `4017785adb08e1114781d3d844e9a10a683fa933` | 0 | PASS | v3 dual route、bounded encrypted staging、GET/HEAD/range、ACK/TTL/restart cleanup 与四类 exact-local synthetic；真实 producer off |
| Desktop pin conformance | `pnpm generate:check && make lint && make test && make build && pnpm docs:build` | `yijie-desktop` | pin commit `96094419d963745529ed0fa246919089e659f20d` | 0 | PASS | public/v2/v3 pin、TS/Rust baseline、docs 通过 |
| Desktop S4 | `make lint && make test && make build && pnpm docs:build` | `yijie-desktop` | `09220dd8319cfb8ec0c4d1531514bb5169107983` | 0 | PASS | v8 SQLCipher、closed event/report adapter、resource transfer/commit/ACK、168h TTL/delete、metadata-only history v3；TS 276/276，Rust 184 pass/3 ignored |
| MiniMax real image capability | bounded provider eval command `PENDING` | isolated local environment | fixed model/API/version `Unknown` | N/A | BLOCKED | 用户批准付费调用、能力来源与固定 eval 后才可执行 |

## 10. Consumer Owner 评审与阻断项

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| Contracts / 段成威 | `G2A APPROVED` | 2026-08-20 | immutable `0.4.0` candidate、locked generate、双 baseline breaking 与 semantic review PASS |
| Agent Host/Runtime / 段成威 | `S3 CONFORMANCE PASS` | 2026-08-20 | exact pin、route/staging/resource/ACK/synthetic 实现与全量 Host 门禁通过；真实 producer 关闭 |
| Desktop/Data/UI / 段成威 | `S4 CONFORMANCE PASS` | 2026-08-20 | exact pin、v8/native transfer/history/private IPC 实现与全量 Desktop 门禁通过；renderer 未开始 |
| Desktop UI / 段成威 | `S5 CONFORMANCE PASS` | 2026-08-20 | provider-neutral reducer/store/generic shell 只消费安全 metadata；type renderer 未开始 |
| Security/Data review / 段成威 | `G3 PASS FOR S3/S4/S5 BOUNDARY` | 2026-08-20 | encrypted staging/SQLCipher、owner scope、MIME/range/digest、commit ACK、retention、no-content IPC 与 safe S5 projection 已实证 |
| S6 readiness / 段成威 | `APPROVED FOR S6A CODING ONLY` | 2026-08-20 | Desktop-private preview/save boundary 不改变本 public Contracts plan；S6A/S6B implementation NOT RUN |

Open blockers 与解除条件：

| ID | 状态 | 阻断事实 | 解除条件 |
|---|---|---|---|
| BLK-128-001 | `CLOSED AT S3` | limits、encrypted spool、24h TTL、ACK/重启清理已冻结并实现 | Host S3 commit 与 contract/lint/test/runtime-test 证据已形成；漂移则重开 |
| BLK-128-002 | `Unknown` | MiniMax 当前 Host profile 未证明 Images API 或 Runtime imageGeneration tool 可用 | 固定 MiniMax API/model/capability 来源，隔离验证 canonical started/completed，记录费用、限流、失败和最多两次短 eval；此前只能 synthetic local test |
| BLK-128-003 | `REAL PROVIDER BLOCKED; SYNTHETIC ALLOWED` | video 没有 canonical real producer；exact-local fixture 已获准 | 真实 activation 前选择 provider 并形成 immutable API、ownership、range/failure conformance；不阻断 S1 synthetic fixture |
| BLK-128-004 | `REAL PROVIDER BLOCKED; SYNTHETIC ALLOWED` | file/report 没有归一化 real producer；exact-local fixture 已获准 | 真实 activation 前明确 producer/权限/审计；不阻断 S1 contract/report fixtures |
| BLK-128-005 | `CLOSED AT S3/S4; EXPIRING EXCEPTION` | OpenAPI/Proto/TS 锁定 generator；Go/Rust JSON Schema 使用显式 adapter 例外 | Host/Desktop implementation digests、同源 conformance、Owner、到期 `2026-11-20 or G5, whichever is earlier` 与移除条件均已记录 |
| BLK-128-006 | `CLOSED AT G2A` | Contracts source/generated、双基线、semantic review 与 consumer exact pin 已形成 | commits 与命令证据见第 6、9 节；边界漂移时重开 |

结论：G2A 后已按序完成 S3/S4，G3 对这两个原子切片为 PASS；本结论不声称 Desktop renderer、walking
skeleton、真实 provider、tag、push、release 或生产交付已经完成。任何真实 v3 producer 仍默认关闭，
不得真实调用 MiniMax，也不得声称真实 video/file/report 已支持。
