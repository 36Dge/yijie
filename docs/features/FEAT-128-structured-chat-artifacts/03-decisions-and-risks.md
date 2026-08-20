# FEAT-128 决策与风险

## 1. 已确认决策

| ID | 决策 | 理由 | 状态 |
|---|---|---|---|
| DEC-128-001 | 本地优先，不购买云资源，不部署生产 | 用户明确要求 | Accepted 2026-08-20 |
| DEC-128-002 | 目标 UI 覆盖图片、视频、文件、数据分析报告，并支持流式阶段 | 用户明确要求 | Accepted 2026-08-20 |
| DEC-128-003 | 使用现有 Desktop Design System、Naive UI、YjIcon、ECharts/token | 用户明确要求且仓库规范强制 | Accepted 2026-08-20 |
| DEC-128-004 | 不把“多模态输入”当作“媒体输出生成已可用” | 当前 MiniMax catalog 与 Host 实现只证明输入和文本输出 | Accepted engineering constraint |

## 2. 推荐候选决策

下列选择最初作为推荐候选，直接决策回复见 2A；本轮 G2 closure 已按 2B 的 Owner 明确指令完成冻结。G2 只授权 Contracts S1/S2，不代表 G2A、下游实现或生产批准。

| ID | 推荐方案 | 备选 | 推荐理由 | G2 批准点 |
|---|---|---|---|---|
| DEC-128-005 | 新增 v3 event/history/resource surface | 原地扩充 v2 closed union | 保持 v1/v2 严格 consumer 兼容 | Contract/Consumer Owner |
| DEC-128-006 | Desktop SQLCipher 为长期 authority，Host 仅短期 staging | Host 长期保存，或 event 携带 base64 | 延续本地加密边界，避免大事件与第二业务库 | Data/Security Owner |
| DEC-128-007 | report 使用 closed versioned JSON document | raw HTML/iframe 或任意 ECharts option | 可访问、可测试、无脚本/远程资源攻击面 | Product/Client/Security Owner |
| DEC-128-008 | WebView 仅通过 one-shot opaque handle custom image protocol 消费 bounded preview；超限降级为保存 | bytes/base64/object URL、generic asset protocol 或直接本地路径 | 同时满足 no-bytes-to-Vue、无路径、可原生复核与有界生命周期 | Client/Security Owner |
| DEC-128-009 | native save dialog + streaming temp file + atomic replace | 浏览器 download、直接 workspace 写入 | 符合 macOS 预期并绑定明确用户意图 | Client/Security Owner |
| DEC-128-010 | local-only synthetic producer 为无云验收入口，默认关闭 | 把 fixture 混入普通 provider | 可重复验证且不误报真实模型能力 | Technical/Reviewer |
| DEC-128-011 | Artifact 默认保留七天，与 FEAT-127 对齐 | 会话永久保留或应用退出即删 | 当前本地数据治理一致，限制 confidential 残留 | Data Owner |

## 2A. G2 Owner Decision Capture（2026-08-20）

> 决策人按 `feature.yaml` 登记为段成威（Feature Owner）；本节依据用户明确授权的直接回复整理。Codex 仅代拟和记录，不把自身描述为独立人工 Reviewer。`Modify` 的完整替代文本已在 2B closure 中冻结。

| ID | 结论 | 完整决策文本 | 理由 | 影响 | 决策人 | 日期 |
|---|---|---|---|---|---|---|
| DEC-128-005 | Approve | 采用显式 v3 event/resource/ack surface，并使用 `event_schema_version=3` 协商；游标参数沿用权威 v1/v2 的 `after`、`stream_id` 与 `Last-Event-ID`。Artifact 只在 v3 surface 发出。v1/v2 endpoint、wire、事件集合、cursor、replay、终态和字节语义保持不变；Desktop durable history/resource 仍是 private surface，本期不新增 Host public history endpoint。 | 隔离 semantic change，保护严格 v1/v2 consumer 兼容性并避免发明第二条 history API。 | S1 必须形成 v3 event、content/poster、ack source 与双基线 equality；G2A 才要求真实生成、不可变引用和 consumer pin。 | 段成威 | 2026-08-20 |
| DEC-128-006 | Modify | Desktop SQLCipher 是 Artifact 唯一长期 authority。Host staging 使用 app-private encrypted spool：文件权限 `0600`、每进程临时密钥且密钥不落盘，Host 重启先清除不可恢复旧 spool；不使用 1 GiB 进程内大对象或 owner-only plaintext。冻结每 session 256 MiB、全局 1 GiB、`staged_at + 24h` TTL。Desktop 校验 scope/size/MIME/magic/SHA-256 并提交 SQLCipher 后，调用 owner/session-scoped 幂等 ACK；ACK、TTL 或 Host 重启触发清理，不驱逐读取中的内容。 | 冻结存储介质、容量、TTL、ack、重启和明文边界。 | S1 定义 ACK operation；Host cleanup transport receipt 与 Desktop 私有 retention cleanup receipt 分开，后者留在 S4 private data design。 | 段成威 | 2026-08-20 |
| DEC-128-007 | Modify | `report-document-v1` 根对象 closed；每个 section envelope 显式包含 `id`、`type`、`required` 和 `payload`。已知 `summary|metrics|paragraph|table|chart|callout` payload 使用 strict safe schema；unknown type 只有 `required=false` 时可由兼容层保留为不渲染的 opaque JSON 并显示 `unsupported`，`required=true` 或已知 payload violation 拒绝整份文档。canonical MIME 为 `application/vnd.yijie.report+json;version=1`；禁止 HTML、script、iframe、URL、远程资源和任意 ECharts option；PDF/Markdown 仅为未来 derived export。 | 让 closed root 与 unknown optional fail-soft 同时可实现、可测试。 | S1 提供 known/unknown requiredness fixtures；Desktop 必须 two-stage decode 且不遍历或执行 unknown payload。 | 段成威 | 2026-08-20 |
| DEC-128-008 | Modify at S6-READINESS | WebView 只通过 `yijie-artifact-preview://localhost/v1/<opaque-handle>` 消费 ready image。handle 为 256-bit CSPRNG、30 秒 absolute TTL、one-shot GET，绑定 main WebView/process/context/owner/tenant/session/turn/artifact；每 WebView 最多 4 个未消费 handle、每 Artifact 1 个、最多 2 个并发读取/40 MiB in-flight。native 在签发和 GET 两次复核 ready/image、PNG/JPEG/WebP、20 MiB、BLOB length、digest 与 image limits。Vue 不接收 bytes/base64/digest/Host href/path/bearer；只允许 CSP `img-src` 追加该 scheme。 | 原 G2 object URL 候选无法同时满足“Vue 不接收 bytes/base64”和实际 `<img>` 取流，必须在编码前改为 non-bearer opaque handle protocol。 | S6A 只实现 native boundary；S6B 才实现 renderer。不得使用 asset/file/blob/data URL 绕过，不扩 `connect-src`/外部 origin。 | 段成威 | 2026-08-20 |
| DEC-128-009 | Modify at S6-READINESS | 用户显式触发 exact native save command；payload 只有 session/turn/artifact identity。native 双次复核 ready image authority，使用既有 `rfd` panel 和 canonical `.png/.jpg/.webp`，同目录 `0600` create-new/no-follow temp、分块复算 digest、fsync 与 atomic replace；取消/失败清 temp 并保留 SQLCipher，Vue 只收 content-free saved/cancelled/failed + stable code。现有 app-command ACL 架构不允许安全地只新增三条 capability，因此不新增 capability/plugin；精确 `generate_handler!` command list 是最小 allowlist。 | 冻结 safe name、extension/MIME、symlink/overwrite、路径不出 native、审计和 crash residue 边界。 | S6A 不新增依赖、plugin、filesystem/shell/dialog capability 或 DB migration；若这些成为必需立即停止并重开 Security/Data review。 | 段成威 | 2026-08-20 |
| DEC-128-010 | Approve | local-only synthetic producer 作为无云验收入口，仅在 `YIJIE_ENV=local`、固定 test manifest 和独立 synthetic flag 同时满足时可启动；它可以为 image/video/file/report 四类发出固定 fixture，默认关闭且不得与真实 provider 同开。每个 Artifact 必须携带并持久化 `provenance=synthetic`；非 local、manifest 不匹配或 capability 不明确时 fail closed，不调用 MiniMax 或任何付费 API。 | 提供完整、可重复、零费用的 walking skeleton，同时把 synthetic 与真实 producer authority 分层。 | 四类 synthetic contract fixtures 属 S1；真实 `provider|tool` producer 仍只由 S12 activation gate 管理。 | 段成威 | 2026-08-20 |
| DEC-128-011 | Modify | Desktop 成功校验并提交 SQLCipher 时记录 `local_committed_at`，并计算 `expires_at = local_committed_at + 168h`；`now >= expires_at` 时进入 `expired`。到期清除 SQLCipher content、preview handle/cache 及可清理的 WAL/checkpoint 残留，并写入 Desktop 私有、幂等的 cleanup receipt；历史只保留最小安全 metadata、位置和 `expired`。Host staging 使用独立 `staged_at + 24h` TTL。会话删除 cleanup saga 失败必须可重试且不得报告物理删除完成。 | 冻结起算点、Host/Desktop 两个时钟和 receipt authority。 | retention migration/reopen/forensic 属 S4，不作为 G2 前的实现证据；G2A 前只需 public contract source 与计划一致。 | 段成威 | 2026-08-20 |

Provider gate：`Approve / Keep closed`。真实 MiniMax image、video、file、report producer 按 kind 独立关闭，不调用真实或付费 API，不发出 `provenance=provider/tool` Artifact。任何启用都必须另行固定 capability/API/model、费用与网络授权、格式/容量/失败/取消/合规语义、Host/Desktop conformance 及质量/延迟/成本 Eval，并取得单独 Owner 批准。

取消边界：当前 candidate 只复用既有 turn interrupt；没有 Artifact-specific cancel operation。turn interrupt 将尚未终态项发为 `item.artifact.failed(error_code=turn_interrupted)`，Desktop 显示 `cancelled`。

poster/ACK 边界：`poster_href` 只允许指向同 session 的 `/poster` 相对资源；content 与 poster 均由 owner-only GET/HEAD 读取。ACK 是独立幂等 POST，校验 artifact、session、size、digest 和 Desktop commit identity，成功只表示 Host 可提前清理 staging，不代表 Desktop retention cleanup 完成。

Generator/adapter 边界：OpenAPI、Protobuf 和 TypeScript JSON Schema 继续使用仓库锁定 generator。当前没有获批的 Go/Rust JSON Schema generator；G2 批准沿用显式 adapter 例外方案。Host/Desktop 的 pin-only commits 已记录 Owner、同源 schema/fixture conformance、最晚 2026-11-20 或 G5（以较早者为准）的到期日，以及“接入获批 generator 或生产前重新批准”的移除条件。S3/S4 实现现已分别固定在 Host `4017785adb08e1114781d3d844e9a10a683fa933` 与 Desktop `09220dd8319cfb8ec0c4d1531514bb5169107983`；生产前仍须移除或重新批准例外。

## 2B. G2 Owner Sign-off（2026-08-20）

用户在本轮明确指令执行 G2 closure rewrite，并要求分别记录 Product、Technical、Security/Data Owner 的 `G2 APPROVED`。Codex 只负责把该 Owner 指令和审查结果写入文档；这不是 Codex 自我批准或独立人工 Review。

| Review | Owner | 结论 | 批准范围 | 不包含 |
|---|---|---|---|---|
| Product/Design | 段成威 | APPROVED | 四类 Artifact、流式状态、本地 synthetic、Pattern 1.0.0 Accepted | 真实 provider、生产 UX 验收 |
| Technical/Contracts | 段成威 | APPROVED | v3 event/content/poster/ack、`after` cursor、report envelope、S1/S2 顺序 | Host/Desktop 业务实现、tag/push |
| Security/Data | 段成威 | APPROVED | encrypted spool、owner/session scope、容量/TTL、Desktop commit retention clock、bounded preview/save | Tauri/CSP/DB 实际变更、生产数据 |
| Test/Reviewer | 段成威 | APPROVED FOR G2 | 06 的 synthetic contract、failure、安全、兼容和双 baseline 计划 | G2A/G4 测试结果或“独立人工评审”声明 |

G2 结论：`APPROVED`，只授权 `yijie-contracts` S1/S2。真实 source/generate/lint/test/breaking/semantic review/immutable commit 与下游 exact pin 是 G2A 证据，不是 G2 前置实现证据。

## 2C. S6-READINESS Owner Conclusion（2026-08-20）

用户明确要求本轮只完成图片 preview/save 安全与实施边界闭环并记录各 Owner 结论。Codex 依据指定基线完成
private IPC、Tauri command/capability/CSP、SQLCipher authority 与 S5 shell 的只读审计并代录下表；不把本轮
文档批准描述为 renderer、command、protocol、CSP 或 save 已实现，也不把 Codex 描述为独立人工 Reviewer。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product/Design | 段成威 | READY FOR S6A；S6B WAITS FOR S6A PASS | ready image preview、明确用户 save、content-free result 与稳定失败 UX | renderer/lightbox/zoom、S7-S12、G4 |
| Technical | 段成威 | APPROVED FOR S6A CODING | 独立 private artifact-native v1 schema、3 个 exact commands、one-shot custom image scheme、SQLCipher reader/save tests | Contracts/Host/pin、依赖/plugin、DB migration、generic protocol |
| Security/Data | 段成威 | APPROVED FOR S6A CODING | owner/context/WebView binding、双次 content validation、30s/4-handle/2-read/40MiB limits、exact `img-src` scheme delta、native atomic save | bytes/path/token to Vue、generic fs/shell/dialog capability、external origin |

S6-READINESS 的 contract impact 为 Desktop-private `additive`；Feature 总体仍为 `semantic`。S6A 通过前 S6B
不得开始；S6A/S6B 都未纳入 G3，G3 仍只包含 S3/S4/S5，G4 pending。

## 2D. S7-READINESS Owner Conclusion（2026-08-20）

本轮从指定 clean baselines 只读审计 Contracts canonical resource、Host S3 synthetic/GET/HEAD/Range、Desktop
SQLCipher authority、S6A private protocol/save、S6B handle lifecycle、Tauri 2.11.x responder、CSP/capability 与依赖，
并只更新治理文档和 Accepted Pattern 1.2.0。readiness 文档本身 `contract-impact=none`；计划中的 S7F 是在既有
immutable contract 下修复 exact-local producer 输出的 `semantic` conformance，S7A 是 Desktop-private
`additive`，均不改变公共 Contracts source/schema/operation/version。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-012 | Contracts `ea48fe...` 的 `synthetic-video-16x16.mp4.base64` 是唯一 canonical video fixture：raw 1,642 bytes、SHA-256 `96ea070c...77dd5`、H.264 High/16×16/25fps/0.12s/3 frames、front `moov`、首帧 keyframe；Host S3 自造的 `ftyp/free/mdat` 无 `moov`，只能 transport，不可播放/seek。 | `ffprobe`、box/packet/frame audit 与 source inspection；canonical resource tree OID `f447129c...` 已由 Desktop exact pin 固定。 | 首个编码切片只能 S7F，让 Host 消费/逐字节校验现有 canonical fixture；不得改 Contracts full commit/tree/pin。 |
| DEC-128-013 | 视频不得使用 `blob:`/`data:`，不得复用 one-shot image scheme；采用独立 `yijie-artifact-video://localhost/v1/<43-char handle>` 和独立 private schema/3 exact commands。 | blob/data 会把正文交给 Vue 并扩大 CSP；image scheme 明确只支持一次 GET，无 HEAD/Range。 | S7A 只在 S7F immutable PASS 后可请求；若需 dependency/plugin/capability/migration/public pin，停止。 |
| DEC-128-014 | video handle 绑定 main WebView/process/context/owner/tenant/session/turn/artifact；30min absolute + 5min idle、2 handles/WebView、1/artifact、原始候选 64 requests/handle、2 concurrent、64MiB in-flight；GET/HEAD 支持单 closed/open/suffix Range 和 200/206/416。 | 原生 video 会重复 HEAD/GET/Range；Tauri 2.11.x responder 缓冲 body，必须把 64MiB 设为硬上限。 | 历史 readiness 决策；其中累计 64 request 撤销条款已被 DEC-128-016 supersede，其余边界继续有效。 |
| DEC-128-015 | video save 新增 video-only exact command，但复用 S6A native dialog/safe-name/same-dir 0600 temp/chunk digest/fsync/atomic replace 内核；只允许 ready `video/mp4` 和 `.mp4`。S7B 使用原生 controls、`preload=metadata`、无 autoplay/player library/external origin；本切片不消费 poster_blob。 | kind/MIME/64MiB 校验不能由 image command 猜测；renderer 不应再实现第二套写盘能力。 | S7B 只在 S7A immutable PASS 后可请求；未满足时保留 S5 metadata shell。 |

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product/Design | 段成威 | READY FOR S7F ONLY；S7A/S7B WAIT | canonical strict-local playable/seekable fixture conformance；Pattern 1.2.0 Accepted | video native/UI、S8-S12、G4 |
| Technical | 段成威 | APPROVED FOR S7F CANONICAL CONFORMANCE | Host producer/snapshot/checker/test 对齐现有 immutable fixture；不重新编码 | Contracts/tree/pin、ffmpeg/codec/runtime dependency、provider |
| Security/Data | 段成威 | APPROVED FOR S7F WITH NO PIN/TREE/DEPENDENCY/PROVIDER DRIFT | synthetic-only、default-off、owner resource/Range 既有边界；后续 S7A 按已冻结 private limits 单独授权 | native/config/CSP/command、bytes/path to Vue、capability/migration |

Owner 结论依据用户当轮明确指令由 Codex 代录，不声称独立人工批准。上表是 2026-08-20 的历史 readiness：
S7F/S7A/S7A-REPAIR/S7B 后续已在逐切片显式授权下形成独立 PASS，但不扩 G3、不声明 G4；真实 video provider
继续 blocked。

## 2E. S7-SPEC-RECONCILIATION 与 S8-READINESS Owner Conclusion（2026-08-21）

本轮只读核对 Contracts/Host/Desktop 当前实现，并把 operative specification 与已完成的 S7 evidence 对齐；文档
改写 `contract-impact=none`。Accepted Pattern 已升为 1.3.0。S8A 未来实现是 Desktop-private `additive`，S8B 不改
contract；本轮没有 command/schema/renderer/config 代码。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-016 | 累计请求次数不再撤销 video handle。同一合法 handle 在 30min absolute TTL、5min idle TTL、显式 release、restart 或 context/WebView/session/identity/revision 失效前持续支持 WebKit 多次 Range；保留 2 handles/WebView、1/artifact、2 concurrent、64MiB in-flight、双次 SQLCipher/MP4/Range fail-closed。 | historical RED：第 65 个合法请求因 64 上限返回 404；S7A-REPAIR `34991d8967de9aa2197ab2e8b9b49347774df7a5` 后 128-request Rust GREEN，真实 WebView 76/76 partial responses 达到 metadata/playback/seek，404=0。 | Supersedes DEC-128-014 的 request-budget clause；保留历史故障，不把它回写为“从未发生”。 |
| DEC-128-017 | S8 重切为 S8A Desktop-private identity-only bounded file preview/save boundary 与 S8B ready-file-only TS/Vue renderer。S8A exact schema 为 `chat-artifact-file-native-v1.schema.json`，exact commands 仅 `chat_read_artifact_file_preview_v1` 与 `chat_save_artifact_file_v1`；无 URL/handle/protocol/CSP/capability/dependency/migration。 | SQLCipher 已是长期 authority；一次性 bounded projection 可满足搜索与文本 DOM，不需要把 bytes/path 交给 Vue。 | `READY FOR S8A ONLY`；S8B 必须等待 S8A immutable PASS 与单独授权。 |
| DEC-128-018 | 当前 v3 file output 只允许 plain/CSV/JSON/PDF/XLSX；inline 只允许前三类，PDF/XLSX metadata + native save。延期 Markdown，不伪装成 `text/plain`。用户明确打开后的 bounded safe projection 只可短暂进入组件 local state/DOM；不得进入 Pinia/history/storage/router/log/telemetry/diagnostics/snapshot。 | `text/markdown` 只存在于 v2 turn input；扩充 v3 closed output 会重开 public semantic contract。SEC-006 的 zero-hit 应针对未授权内容、超出已批准 bounded projection 的正文、path/token/digest/savedPath/raw error；小文件 projection 可在 caps 内等于完整正文，授权 preview 关闭后也必须 zero-hit。 | AC-005=`PARTIAL`，G4 仍 blocked。若本期坚持 Markdown，重开 G2/G2A、Contracts generate/breaking/semantic review、immutable pin 与 downstream repin。 |

S8A exact limits 已冻结为：source `1..1,048,576` bytes；projection `<=262,144` bytes；response `<=524,288`
bytes；text/JSON `<=2,000` lines、每行 `<=8,192` UTF-8 bytes；CSV `<=200×50`、cell `<=4,096` bytes；JSON
depth `<=32`、nodes `<=20,000`；每 WebView preview concurrency `<=2`、in-flight source `<=2,097,152` bytes、
同 identity single-flight、10s timeout；S8B literal search query `1..128` Unicode scalars、最多 100 hits。UTF-8 only，
仅去一个 BOM，CRLF/CR 仅在 projection 规范化 LF；TAB/LF/CR 外 C0/DEL/C1 拒绝 inline，并拒绝 Unicode
`Bidi_Control` `U+061C`、`U+200E-U+200F`、`U+202A-U+202E`、`U+2066-U+2069`。save 与 preview eligibility
相互独立，五类 ready-file save 接受 `1..67,108,864` bytes。file temp 唯一使用
`.yijie-artifact-file-save-v1-<txt|csv|json|pdf|xlsx>-<process-epoch UUID>-<22-char base64url>.tmp`；仅在下一次用户
明确选择同一目录时，删除 prior epoch 且 exact marker、regular non-symlink、current uid、`0600`、link count 1、
size/对应 format recheck 全部通过的条目；S6/S7 prefix/validator/behavior 不变。
save 的 PDF/XLSX recheck 不停留在 magic sniff：PDF 复用既有 bounded preflight（classic xref/EOF、非加密、无
ObjStm/XRef stream/Prev、objects<=4,096、pages `1..256`、streams<=1,024、单/总 decoded stream<=8/32 MiB、
ratio<=100:1、expanded traversal<=4,096 stream visits/32 MiB、form depth<=16、page-tree depth<=64）；
XLSX 复用既有 bounded OOXML package validator（entries `1..512`、safe unique names、Stored/Deflated、单/总
uncompressed<=8/32 MiB、ratio<=100:1、无 `.bin`/`vbaProject`，且 `[Content_Types].xml`、`xl/workbook.xml` 与
spreadsheet main content type 匹配）。只允许暴露/复用 helper，既有 attachment import 行为与 limits 不变。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product | 段成威 | READY FOR S8A ONLY WITH MARKDOWN DEFERRED；AC-005 PARTIAL；S8B WAITS | 当前 v3 五种 file MIME、三类 bounded inline、五类 native save/fallback | Markdown contract、S8B、S9-S12、G4 |
| Technical | 段成威 | APPROVED FOR S8A CODING | exact private schema + 2 commands、双次 authority/format validation、typed client/tests、仅 Desktop implementation/readiness SHA checker refresh | public pin/source/tree/schema/operation/version、protocol/config/dependency/migration |
| Security/Data | 段成威 | APPROVED FOR S8A CODING | bounded authorized-content exception、no persistence/log/snapshot、native dialog + atomic save、file-specific crash residue validation | generic fs/shell/asset、path/body/token leakage、S6/S7 behavior drift |

Owner 结论依据用户本轮明确指令由 Codex 代录，不声称独立人工批准。Readiness 不是实现 PASS；S8A/S8B 均未
实现，G3 仍只包含 S3/S4/S5，G4 pending。

## 3. Provider activation gate

每个真实 kind 单独通过以下条件后才能启用：

1. 权威 API/tool/Runtime item 和 provider capability 有固定版本证据。
2. 用户明确授权可能产生的模型费用与外部网络访问。
3. 内容类型、最大大小、失败、取消、重试、审核和合规语义已冻结。
4. Host producer conformance、Desktop consumer conformance 和真实 local integration 通过。
5. 质量/延迟/成本 Eval 有固定 dataset 和阈值。

当前 image/video/file/report 均未通过完整 gate。固定 Runtime 的 `imageGeneration` item 只满足第 1 项的一部分，MiniMax capability 仍未证明。

## 4. 风险登记

| Risk | 触发条件 | 影响 | 预防控制 | 检测 | 恢复/回滚 | Owner |
|---|---|---|---|---|---|---|
| RSK-128-001 旧 consumer 被未知事件击穿 | 新 variant 发到 v1/v2 | 对话流中断 | 显式 v3 协商、v1/v2 wire equality | compatibility + strict consumer test | 关闭 v3 producer，回退到文本 | Contracts Owner |
| RSK-128-002 confidential 内容泄漏 | bytes/path/token 进入 event/log/DOM | 数据泄漏 | opaque ref、native fetch、日志脱敏、no-store | canary fixture + log/DOM scan | 停止 producer，删除 staging/cache，轮换 token | Security Owner |
| RSK-128-003 媒体炸弹/OOM | 伪装 MIME、巨大尺寸、压缩/解码放大 | crash/卡死 | magic、length、pixel/duration/row limits、lazy decode | adversarial fixture、memory threshold | 终止 decode，降级 metadata + save | Client Owner |
| RSK-128-004 存储不一致 | Host ready 但 Desktop 写入失败 | UI 显示不可用/丢失结果 | staged transfer、digest、原子 commit、ack 后清理 | mismatch metric/log code | 重试 transfer；不可恢复标 failed | Runtime/Client Owner |
| RSK-128-005 保存越界或覆盖错误 | 恶意名称、symlink、已有目标 | 任意文件写/数据覆盖 | native dialog、safe name、no-follow、明确 overwrite、atomic replace | security tests | 删除 temp，保留 authority copy | Client/Security Owner |
| RSK-128-006 raw report 内容执行 | HTML/script/remote URL 进入 renderer | XSS/数据外传 | closed report schema、文本转义、无 iframe/HTML | schema/adversarial UI tests | 拒绝 section，继续已知 section | Security Owner |
| RSK-128-007 伪造进度 | UI 显示无依据百分比 | 误导用户 | percent optional、只显示 provider stage | event/UI conformance | 回退不确定进度文案 | Product Owner |
| RSK-128-008 synthetic 被误当真实 | fixture 在普通模式启用 | 验收/用户信任失真 | exact local env gate、明显 synthetic source、默认 off | startup/config tests | 关闭 profile、清理 fixture session | Technical Owner |
| RSK-128-009 provider 费用失控 | 自动调用媒体生成 API | 不可控成本 | 默认 capability off、显式费用批准、per-turn limits | cost counter/budget stop | kill switch、禁止新请求 | Product/Release Owner |
| RSK-128-010 retention 清理失败 | DB/WAL/cache 或 Host staging 残留 | confidential 长期残留 | TTL job、session cleanup saga、WAL/cache verification | reopen/forensic test | retry cleanup、阻断关闭/发布 | Data Owner |
| RSK-128-011 preview handle 重放/资源探测 | handle 泄漏、跨 WebView/session 重放或协议被当 generic fetch | 跨会话显示、内容枚举或 JS 读取 | 256-bit one-shot handle、main WebView/process/context/session binding、30s TTL、no CORS、empty 404 | registry/expiry/replay/session-switch/adversarial protocol tests | revoke all handles、关闭 image preview、保持 metadata/save fallback | Client/Security Owner |
| RSK-128-012 video Range handle 滥用/OOM | multi-request handle 被猜测、跨 context 重放、恶意 Range 或 64MiB buffered response 并发 | 内容泄漏、内存放大、播放卡死 | 独立 256-bit binding、30min/5min TTL、无累计次数撤销、2 handle/2 read/64MiB total、single Range parser、no CORS/fetch | >=128 legal Range lifecycle、76-Range WebView zero-404、replay/expiry/context/in-flight/memory tests | revoke video registry、移除 `media-src` scheme、回落 metadata/save-disabled shell | Client/Security/Data Owner |
| RSK-128-013 file preview 内容执行/泄漏 | raw/未授权正文进入全局 state/log/snapshot，CSV formula/HTML/link 被执行，或 save path 返回 Vue | XSS、工具越权、数据泄漏、任意写入 | native bounded projection、text nodes only、exact limits、no v-html/link/formula execution、component-local lifecycle、native atomic save | control/bidi/CSV/JSON adversarial tests、authorized/unauthorized canary open/close scans、path/token/digest zero-hit | 关闭 S8 renderer/commands，回落 metadata shell，保留 SQLCipher authority | Client/Security/Data Owner |

## 5. 不需要新 ADR 的前提

如果实现保持“v3 expand、Host 临时 staging、Desktop 本地 authority、无云资源、无新跨仓职责”，现有职责方向不变，可在本 Feature 决策记录内评审。若选择 Host/云端长期 Artifact 仓库、自定义共享 URL、公共分享或改变 Runtime 核心协议，必须先建立新 ADR 并取得明确批准。

## 6. 实现前批准清单

- DEC-128-005..011、ACK/poster/cursor/cancel、report compatibility、synthetic/real 分层与 Provider gate 已完成 G2 Owner 冻结。
- S6-READINESS 批准的图片 3-command/scheme/CSP 边界已由 S6A 实现，S6B 已消费而未改变 native/config；两者均为
  G3 外独立 PASS。
- S7F/S7A/S7A-REPAIR/S7B 已逐切片独立 PASS；DEC-128-016 是现行 video handle lifecycle，Pattern 1.2.0 的
  64-request 条款只保留为历史 RED。
- S8-READINESS/Pattern 1.3.0 只批准下一编码切片 S8A；S8B 等待 S8A immutable PASS 与单独授权。Markdown 延期使
  AC-005 保持 PARTIAL，G4 不得通过。
- Contracts v3 source、基线、generator/adapter、unknown kind/section 行为和 consumer 顺序已完成 G2 设计评审；S1/S2 真实生成、检查、双 breaking 与不可变 commit 已通过。
- Desktop SQLCipher v8 migration、64 MiB 单 Artifact 上限、七天 retention 起算与恢复边界已在 S4 实现并通过迁移/reopen/TTL/delete 验证；图片 native preview/save/CSP 属 S6A，S6B 只做 renderer。
- 真实 MiniMax 调用保持关闭；如需启用，另行取得费用和 provider activation 批准。

## 7. 当前 Gate 结论

- G0：PASS，Feature ID、Owner、本地边界和初始 Git 状态已记录。
- G1：PASS，场景、AC、受影响仓库、最高 contract impact 和主要风险已识别。
- G2：`PASS`，Product/Design、Technical/Contracts、Security/Data 与测试计划已由 Owner 明确批准；只允许进入 Contracts S1/S2。
- G2A：`PASS`，Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875` 与 Desktop pin `96094419d963745529ed0fa246919089e659f20d` 已满足真实 generate、双 breaking、semantic/consumer review 与不可变 pin 条件。批准依据是用户本轮给出的条件授权与实际证据，不声称 Codex 是独立人工 Reviewer。
- G3：只对 S3/S4/S5 原子切片通过；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B 为独立 PASS，均不扩展 G3。
  S8-READINESS 仅 `READY FOR S8A ONLY`，不是实现 PASS；G4-G6 仍未通过，Host/Desktop master/synthetic flags
  与真实 provider 继续关闭。
