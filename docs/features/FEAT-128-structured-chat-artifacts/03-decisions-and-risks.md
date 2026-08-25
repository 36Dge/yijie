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
| DEC-128-007 | Modify | `report-document-v1` 根对象 closed；每个 section envelope 显式包含 `id`、`type`、`required` 和 `payload`。已知 `summary\|metrics\|paragraph\|table\|chart\|callout` payload 使用 strict safe schema；unknown type 只有 `required=false` 时可由兼容层保留为不渲染的 opaque JSON 并显示 `unsupported`，`required=true` 或已知 payload violation 拒绝整份文档。canonical MIME 为 `application/vnd.yijie.report+json;version=1`；禁止 HTML、script、iframe、URL、远程资源和任意 ECharts option；PDF/Markdown 仅为未来 derived export。 | 让 closed root 与 unknown optional fail-soft 同时可实现、可测试。 | S1 提供 known/unknown requiredness fixtures；Desktop 必须 two-stage decode 且不遍历或执行 unknown payload。 | 段成威 | 2026-08-20 |
| DEC-128-008 | Modify at S6-READINESS | WebView 只通过 `yijie-artifact-preview://localhost/v1/<opaque-handle>` 消费 ready image。handle 为 256-bit CSPRNG、30 秒 absolute TTL、one-shot GET，绑定 main WebView/process/context/owner/tenant/session/turn/artifact；每 WebView 最多 4 个未消费 handle、每 Artifact 1 个、最多 2 个并发读取/40 MiB in-flight。native 在签发和 GET 两次复核 ready/image、PNG/JPEG/WebP、20 MiB、BLOB length、digest 与 image limits。Vue 不接收 bytes/base64/digest/Host href/path/bearer；只允许 CSP `img-src` 追加该 scheme。 | 原 G2 object URL 候选无法同时满足“Vue 不接收 bytes/base64”和实际 `<img>` 取流，必须在编码前改为 non-bearer opaque handle protocol。 | S6A 只实现 native boundary；S6B 才实现 renderer。不得使用 asset/file/blob/data URL 绕过，不扩 `connect-src`/外部 origin。 | 段成威 | 2026-08-20 |
| DEC-128-009 | Modify at S6-READINESS | 用户显式触发 exact native save command；payload 只有 session/turn/artifact identity。native 双次复核 ready image authority，使用既有 `rfd` panel 和 canonical `.png/.jpg/.webp`，同目录 `0600` create-new/no-follow temp、分块复算 digest、fsync 与 atomic replace；取消/失败清 temp 并保留 SQLCipher，Vue 只收 content-free saved/cancelled/failed + stable code。现有 app-command ACL 架构不允许安全地只新增三条 capability，因此不新增 capability/plugin；精确 `generate_handler!` command list 是最小 allowlist。 | 冻结 safe name、extension/MIME、symlink/overwrite、路径不出 native、审计和 crash residue 边界。 | S6A 不新增依赖、plugin、filesystem/shell/dialog capability 或 DB migration；若这些成为必需立即停止并重开 Security/Data review。 | 段成威 | 2026-08-20 |
| DEC-128-010 | Approve | local-only synthetic producer 作为无云验收入口，仅在 `YIJIE_ENV=local`、固定 test manifest 和独立 synthetic flag 同时满足时可启动；它可以为 image/video/file/report 四类发出固定 fixture，默认关闭且不得与真实 provider 同开。每个 Artifact 必须携带并持久化 `provenance=synthetic`；非 local、manifest 不匹配或 capability 不明确时 fail closed，不调用 MiniMax 或任何付费 API。 | 提供完整、可重复、零费用的 walking skeleton，同时把 synthetic 与真实 producer authority 分层。 | 四类 synthetic contract fixtures 属 S1；真实 `provider\|tool` producer 仍只由 S12 activation gate 管理。 | 段成威 | 2026-08-20 |
| DEC-128-011 | Modify | Desktop 成功校验并提交 SQLCipher 时记录 `local_committed_at`，并计算 `expires_at = local_committed_at + 168h`；`now >= expires_at` 时进入 `expired`。到期清除 SQLCipher content、preview handle/cache 及可清理的 WAL/checkpoint 残留，并写入 Desktop 私有、幂等的 cleanup receipt；历史只保留最小安全 metadata、位置和 `expired`。Host staging 使用独立 `staged_at + 24h` TTL。会话删除 cleanup saga 失败必须可重试且不得报告物理删除完成。 | 冻结起算点、Host/Desktop 两个时钟和 receipt authority。 | retention migration/reopen/forensic 属 S4，不作为 G2 前的实现证据；G2A 前只需 public contract source 与计划一致。 | 段成威 | 2026-08-20 |

Provider gate：`Approve / Keep closed`。真实 MiniMax image、video、file、report producer 按 kind 独立关闭，不调用真实或付费 API，不发出 `provenance=provider/tool` Artifact。任何启用都必须另行固定 capability/API/model、费用与网络授权、格式/容量/失败/取消/合规语义、Host/Desktop conformance 及质量/延迟/成本 Eval，并取得单独 Owner 批准。

> 历史说明：上述 provider gate 是 2026-08-20 的阶段结论。image kind 已由 2026-08-23 的
> DEC-128-033..040 有界范围决定取代；video/file/report 仍保持关闭。

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

Owner 结论依据用户本轮明确指令由 Codex 代录，不声称独立人工批准。该 readiness 当时不是实现 PASS；S8A/S8B
现已分别完成并保持 G3 外独立 PASS，G3 仍只包含 S3/S4/S5，G4 pending。

## 2F. S9-READINESS Owner Conclusion（2026-08-21）

本轮只读核对 immutable Contracts report v1、Host synthetic producer、Desktop SQLCipher authority/private IPC、
现有 commands/config/dependency 与 S5/S8 component boundary，并将 Accepted Pattern 升为 1.4.0。readiness 文档
`contract-impact=none`；未来 S9A 的最高影响是 Desktop consumer `semantic` conformance repair 加 Desktop-private
additive schema/commands，公共 Contracts、Host、pin、fixture 与 wire 不变。本轮没有 schema、command、renderer、
dependency、config 或业务代码。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-019 | S9 重切为 S9A Desktop-private identity-only bounded report projection/canonical JSON save boundary 与 S9B provider-neutral TS/Vue renderer。S9A exact private schema 为 `chat-artifact-report-native-v1.schema.json`，exact commands 仅 `chat_read_artifact_report_preview_v1` 与 `chat_save_artifact_report_v1`；无 URL/handle/protocol/CSP/capability/dependency/migration。 | 当前 history/private IPC 只含 report metadata，SQLCipher 才持有 ready report canonical bytes；Vue 不得读取 raw JSON 或自行验证 wire。 | `READY FOR S9A ONLY`；S9B 等待 S9A immutable PASS、单独授权与 ECharts blocker 解除。 |
| DEC-128-020 | S9A 必须先修复 Desktop report consumer 对 immutable schema 的额外拒绝：Unicode `maxLength` 按 scalar 计数、接受合法 RFC 3339 offset、不要求 section ID/column key 唯一、不要求 chart labels/values 等长。修复后再以同一 full-schema validator 签发 closed bounded projection；unknown optional 只投影 ordinal/unsupported marker，unknown required 拒绝整份文档。 | Contracts exact MIME 是 `application/vnd.yijie.report+json;version=1`；known sections 为 summary/metrics/paragraph/table/chart/callout。当前 Rust adapter 会拒绝多组 Ajv-valid fixture，属于 consumer conformance 漂移，不得反向收紧公共契约。 | S9A EXPECTED RED 必须固定这些 contract-valid cases；repair 若不能保持 public pins/fixtures 不变则停止。 |
| DEC-128-021 | S9A 只允许保存同一 validated canonical report JSON（`.json`）；PDF/Markdown/image derived export 延期。S9B chart 只能从 closed projection 映射固定 ECharts option，且始终提供 accessible text table。 | 当前没有安全 derived exporter；active Desktop package/lock 没有 ECharts/vue-echarts，也没有易界 chart theme/card。 | S9B=`BLOCKED`；解除需单独批准 exact pinned ECharts dependency/lockfile、tree-shaken imports、semantic theme/card。G4 不得因此通过。 |

S9A exact limits 冻结为：request `<=4,096` encoded bytes；preview source `1..4,194,304` bytes；projection
`<=524,288` bytes；serialized response `<=1,048,576` bytes；完整 document depth `<=12`、nodes `<=100,000`、
sections `0..64`；每 WebView preview concurrency `<=2`、source in-flight `<=8,388,608` bytes、同 identity
single-flight、10s timeout；save 与 preview eligibility 独立，validated ready report `1..67,108,864` bytes。
summary/paragraph/callout text 每项 `<=8,192` scalars、heading/title `<=1,024`；metrics `<=32` items；table
`<=32` columns、前 `<=200` rows、string cell `<=1,024` scalars；chart `<=128` labels、`<=16` series、每 series
`<=128` finite JSON numbers、总 points `<=2,048`。完整 schema、source/node/depth/response、unknown required、
integrity 或 revision failure 均 fail closed；display cap 只在 scalar/section/row/cell 边界截断并标记 `truncated`。

projection 根对象只含 `schemaVersion/title/generatedAt/sourceTime/truncated/sections`；known union 只含 renderer
需要的 typed scalar/array，unknown optional 只含 ordinal/id/`type=unsupported`/`required=false`，不得返回 original
type 或 payload。CRLF/CR 规范化 LF；TAB/LF 外的 C0、DEL/C1 与 `Bidi_Control` `U+061C`、
`U+200E-U+200F`、`U+202A-U+202E`、`U+2066-U+2069` 投影成可见 ASCII `\\uXXXX`，不改变 SQLCipher/save
canonical bytes。

save 只由明确 click/keyboard intent 触发，dialog 前后执行两次 authority/full-schema validation；复用同目录
`0600` create-new/no-follow temp、chunk digest、fsync、atomic replace 与 RAII。report residue exact filename 为
`.yijie-artifact-report-save-v1-json-<process-epoch UUID>-<22-char base64url>.tmp`；仅在下一次用户明确选择同一目录时
best-effort 删除 prior epoch 且通过 exact marker、regular non-symlink、current uid、`0600`、nlink=1、size 与完整
ReportDocumentV1 recheck 的条目。Vue 只收 content-free `saved|cancelled|failed` + stable code。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product | 段成威 | READY FOR S9A ONLY；CANONICAL JSON SAVE ONLY；S9B WAITS | closed report v1、bounded projection、canonical JSON native save、Pattern 1.4.0 Accepted | derived export、S9B、S10-S12、G4 |
| Technical | 段成威 | APPROVED FOR S9A CODING | contract-conformant validator repair、exact private schema + 2 commands、typed client/tests、必要 Desktop implementation/readiness SHA-only checker refresh | public contract/pin、Host、dependency/config/protocol/migration |
| Security/Data | 段成威 | APPROVED FOR S9A CODING | 双次 SQLCipher authority/full-schema validation、bounded projection、unknown payload omission、component-local lifecycle、native atomic save/residue validation | raw JSON/path/token/error to Vue、persistence/log/snapshot、generic fs/shell/export |

Owner 结论依据用户本轮明确指令由 Codex 代录，不声称独立人工批准。该 readiness 是历史 docs-only PASS；
S9A 后续已在 `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` 独立 PASS，S9B 仍未实现；G3 仍只包含
S3/S4/S5，G4 pending。

## 2G. S9B-READINESS Owner Conclusion（2026-08-21）

本轮只读核对 S9A closed projection/client、S5/S8 UI lifecycle、semantic tokens/Naive UI/YjIcon/test
设施、active package/lock/Vite/Tauri/CSP，并以 Desktop Pattern 1.5.0
`630c3c8d55a2617499f51bd5bed263b819aaf084` 冻结以下 superseding decisions。本轮没有安装包、修改
lockfile/config 或实现 renderer；`contract-impact=none`。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-022 | S9B 拆为 S9B-D exact dependency/semantic theme/closed adapter/chart-card foundation 与 S9B-R ready-report renderer/save UX。 | dependency/lock/license/bundle/theme 与授权正文 local-DOM lifecycle 是两类不同风险；分开后可独立回滚。 | `READY FOR S9B-D ONLY`；S9B-R 等待 D immutable PASS 与单独授权。 |
| DEC-128-023 | 选择 direct exact `echarts@6.1.0` Apache-2.0 + static tree-shaken `echarts/core` + CanvasRenderer；拒绝 `vue-echarts`。exact transitives 只允许 `zrender@6.1.0` BSD-3-Clause 与 `tslib@2.3.0` 0BSD，integrity/import/notice/bundle 按 Pattern 9.12 冻结。 | active app 确实没有 ECharts/theme/card；wrapper 增加 generic option/event/lifecycle 面而无必要能力。全部 JS baseline=`655731/206580` raw/gzip-9，最终 cap=`1372531/431860`。series token 只允许 `--yj-color-chart-series-1..8`。 | 只在 S9B-D 授权 package/lock/notice/theme/adapter/card、两条 exact checker 与 test-only visual harness 增量；任何额外 package、integrity/license/install-script 或 `716800/225280` 增量超限立即停止。 |
| DEC-128-024 | accessible HTML table 始终是数据权威；chart 只是 bounded progressive enhancement。adapter 只接受 S9A closed chart projection，bar/line 限 64 labels/8 series/512 points，pie 限 one aligned non-negative non-zero series/32 labels。S9B-R 每次 explicit open 按 section ordinal 升序只增强前 4 个 adapter-eligible charts；D 只提供 pure local-budget helper，不用 global/mount/async-order counter。 | 当前 projection 没有 chart unit/data source/time range；UI 只能展示“报告未提供”，不得推断。单 chart cap 使 4 instances 合计必 `<=2048` points；mismatch/oversize/init/error 必须只降级当前 chart。 | 禁止 arbitrary option/formatter/HTML/URL/event/network/dynamic module；model/option 不得 snapshot，改用 exact-key/no-function/no-URL 结构断言。 |

Exact value imports 只为 `init/use`、`BarChart/LineChart/PieChart`、`GridComponent/TooltipComponent/AriaComponent`
与 `CanvasRenderer`；图例由 HTML `<ul>` 实现，禁止 full/root ECharts、SVG、Legend/Title/Dataset/Transform/
DataZoom/Toolbox/Graphic/Custom/UniversalTransition、CDN/import map/dynamic module。theme 使用 Pattern 9.12 的 exact light/dark
tokens，`animation=false`，rich-text confined tooltip、ARIA/decal、可见 table 与 disposal 顺序均为强制门禁。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product | 段成威 | READY FOR S9B-D ONLY；ACCESSIBLE TABLE IS AUTHORITATIVE；UNIT/SOURCE/TIME RANGE HONESTLY UNAVAILABLE | exact dependency/theme/closed adapter/chart-card foundation | S9B-R、production page、S10-S12、G4 |
| Technical | 段成威 | APPROVED FOR S9B-D CODING | exact ECharts/integrity/lock/notice/static imports/Canvas、semantic theme/card、bundle checker | S9A/native/config/pages/stores、arbitrary option/dynamic module |
| Security/Data | 段成威 | APPROVED FOR S9B-D CODING | no report read/persistence/log/snapshot/network、bounded instances、dispose lifecycle、table fallback | S9B-R authorized-content DOM lifecycle 在 D PASS 前保持关闭 |

Owner 结论依据用户本轮明确指令由 Codex 代录，不声称独立人工批准。S9B-READINESS 是 docs-only
PASS；其历史结论保留。S9B-D `0a36ca7c54460d22ea6b3228832a57f05f0bde68`、checker repair
`aec0f8a05ba7534132cbb4f46be64e333d7e9024` 与 S9B-R
`6bcc2a6bfb4db76398ecf5483c688475477f08ed` 后续均已独立 PASS；production vertical 仍 NOT RUN，G3/G4 不变。

## 2H. S9-SPEC-RECONCILIATION 与 S10-READINESS Owner Conclusion（2026-08-22，historical）

本轮只读审计确认：Host v3 是普通 turn/reasoning 与 Artifact 的同序列超集；Desktop production 仍只开 v2，
ArtifactTransferService/v3 decoder 没有生产调用；ChatClient/Store/Page 仍未接 history v3/ArtifactStore/List。现有
FEAT-128 synthetic 又因 Runtime 前置和 synthetic+fake 互斥，不能独立驱动真实 Host。Accepted Pattern 已升为
1.6.0 `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2`。本 docs rewrite `contract-impact=none`。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-025 | S10 重切为 S10A-LOCAL-PROFILE → S10B-NATIVE-LIVE → S10C-PAGE → S10D-VERTICAL → S10E-SEC-PERF；native V3/cursor 基础必须先于 Page。 | keyless Runtime/profile、ordered durable ingestion、UI authority 和纵向/性能是四种不同风险，必须独立回滚。 | `READY FOR S10A-LOCAL-PROFILE ONLY`；B-E WAIT/NOT RUN。 |
| DEC-128-026 | 新增 exact/default-off `YIJIE_FEAT128_S10_TEST_PROFILE_ENABLED=true`，只在既有 FEAT126 exact loopback fake Responses profile、v3/synthetic exact flags、manifest `feat128-artifact-v1`、local/owner/parent/run-root 条件及零 MiniMax/key/provider 时允许 synthetic+fake。其它组合 startup fail before listen/spool/child。 | 当前 StartSession/Turn 先依赖 Runtime；无 Runtime 时 synthetic 到不了，直接放宽互斥会扩大测试配置。 | S10A 只改 Host config/integration test 与 Desktop sidecar/compile-time test wiring；公共 wire/pin/fixture不变。 |
| DEC-128-027 | Artifact flag on 时 active turn 只消费 single v3 stream。started/progress/failed 与 turn-progress flush/cursor 同 SQLCipher transaction；completed 的 ready BLOB+ACK intent+cursor 同事务，ACK 在 commit 后幂等发送；网络期间不持事务。 | v2+v3 双流无共同 cursor；当前 Artifact 状态与 turn cursor 分开写，崩溃重放会撞上 strict monotonic state。 | S10B 必须证明 crash/replay/gap/duplicate/stream restart，不得用弱化 regression 检查修复。 |
| DEC-128-028 | 新增 Desktop-private content-free channel `yijie:chat:artifact:changed:v1`/schema `chat-artifact-live-v1.schema.json`，只含 subscription/context/session/turn/event identity、per-subscription sequence 与 `artifact_changed\|resync_required\|context_invalidated`；queue cap 64。history v3 是唯一 replay authority。 | 发送完整 Artifact metadata 会在 history 与 live 间产生 stale regression；content-free invalidation + coalesced history-v3 resync 保持同一 S5 reducer 和安全边界。 | S10B 实现 channel；S10C subscribe-first/buffer/control+v3-history/replay。无 public Contracts/Host wire 变化。 |
| DEC-128-029 | flag off 只禁止新 v3 producer/transfer；已持久化 metadata 与经当前 `ReadSessions` 授权的 preview/save 保持只读。Desktop parent flag 映射 Host v3 child flag但不转发自身；synthetic env 只能由 compile-time `feat128-s10-runtime` exact profile 注入。 | rollback 不能使本地 authority 数据不可读，也不能信任任意 shell synthetic env。 | 不新增 Vue-only flag；关闭后回落 single v2 active stream。 |

S10A exact process/temp/watchdog、B-E private schema/atomicity/history/store/page/vertical/security/performance、允许目录、
命令、停止条件和回滚以 Pattern 1.6.0 §§9.14-9.19 与 07 §23 为准。Markdown/AC-005 仍 PARTIAL。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product | 段成威 | READY FOR S10A-LOCAL-PROFILE ONLY；PRODUCTION VERTICAL AND MARKDOWN PENDING | strict-local zero-provider executable profile | S10B-E、S11-S12、G4 |
| Technical | 段成威 | APPROVED FOR EXACT KEYLESS LOOPBACK PROFILE AND SIDECAR FLAG MAPPING | S10A exact Host/Desktop test/config scope | single-v3/atomic-cursor B、Page、public contract/config expansion |
| Security/Data | 段成威 | APPROVED FOR S10A ONLY WITH NO KEY/PROVIDER/NON-LOOPBACK, OWNER-ONLY TEMP ROOT, WATCHDOG AND CONTENT-FREE EVIDENCE | zero-secret/network proof、bounded process lifecycle、cleanup | real provider、persistent evidence content、B-E |

Owner 结论依据用户明确指令由 Codex 代录，不声称独立人工批准。上述是当时的 docs-only capture；当时
S10A-E 均 NOT RUN。S10A/S10B/S10C 后续已在独立授权下分别 separate PASS，历史不得回写。

## 2I. S10-SPEC-RECONCILIATION 与 S10D-READINESS Owner Conclusion（2026-08-22）

只读审计确认 S10A exact keyless profile、S10B single-v3/SQLCipher/ACK/private invalidation 与 S10C
history-v3/ArtifactStore/production ChatPage wiring 已分别独立 PASS；但现有 S7B 会替换 production bootstrap，S9
visual 是 Vite fake，S10A runner 不启动 production Page，三者均不构成 real Tauri production vertical。production
auth 也不接受 ephemeral test profile，因此 bootstrap、WKWebView control/screenshot 与多进程 teardown 是必须先独立闭合的
非平凡风险。Accepted Pattern 已升为 1.7.0
`8afdc996c11bbad2d275eb8b86a0f6b82ca5da52`；本轮 `contract-impact=none`。

| ID | 冻结结论 | 理由/证据 | Gate effect |
|---|---|---|---|
| DEC-128-030 | S10D 重切为 S10D-H harness/walking skeleton → S10D-V complete vertical；S10E 继续等待 V PASS。 | 先证明 fresh binaries、production bootstrap/commands/Page、macOS control/screenshot/content-free verdict 与 teardown，才能可信运行四类/restart/history/visual matrix。 | `READY FOR S10D-H ONLY`；D-H/D-V/E 均 NOT RUN。 |
| DEC-128-031 | H 复用现有 `feat128-s10-runtime`；production App/router 先正常 mount，再加载 feature-only controller。test bootstrap 只建立 synthetic auth/project prerequisite；session/turn/Artifact/history/ACK/UI 必须走 production path。 | 禁止 S7 seeded shell、mock client、Pinia seed、direct SQLCipher/spool 与生产 Page/command 替换。 | 不新增 feature/dependency/plugin/capability/CSP/migration/public or private wire。 |
| DEC-128-032 | H 使用 isolated release build、ports 18080/18082、0700 root、20/45/180/300/10s deadlines、closed content-free verdict、transient screenshot 与 exact teardown。 | 现有依赖已足以用 Tauri raw macOS window/`objc2` 取得 window number，再调用系统 `screencapture -l`；H 要实际证明可用，失败不得降级 Vite/browser。 | H 失败只记录 blocker/failure class；不得猜测性扩大。 |

H 允许目录、EXPECTED RED/GREEN、exact runner/build、verdict schema、cleanup、完整 D-V matrix、stop/rollback 以 Pattern
1.7.0 §§9.17-9.18 与 07 §26 为准。完整 D-V 覆盖四 kind lifecycle、乱序/失败隔离、history/restart/ACK/TTL/delete、
四 renderer、light/dark/1180×760/720×760/200%/keyboard/focus/axe/reduced-motion；native save 无法安全自动化时必须
`MANUAL/NOT RUN`，不得注入目标路径。

| Review | Owner | 结论 | 批准范围 | 保持关闭 |
|---|---|---|---|---|
| Product | 段成威 | READY FOR S10D-H ONLY；H 只验一个 production walking skeleton | production ChatPage 四类 ready shell 与基本可访问状态 | renderer/save/full matrix、S10D-V/E、G4 |
| Technical | 段成威 | APPROVED FOR EXACT FRESH-BINARY REAL-TAURI HARNESS WITH PRODUCTION BOOTSTRAP/COMMANDS AND CLOSED PROCESS LIFECYCLE | default-off H bootstrap/controller/runner/checker | mock/Vite/dev server、新 feature/config/dependency、D-V |
| Security/Data | 段成威 | APPROVED FOR S10D-H ONLY WITH EXACT KEYLESS LOOPBACK PROFILE, TEST-ONLY AUTHORITY BOOTSTRAP, ZERO CANARY, CONTENT-FREE VERDICT, TRANSIENT SCREENSHOT AND COMPLETE CLEANUP | 0700 authority、minimal evidence、process/listener/WAL/spool/temp cleanup | provider/key/non-loopback、raw content/path/token/evidence persistence、D-V/E |

Owner 结论由 Codex 按用户明确指令代录，不声称独立人工批准。S10D readiness 是 docs-only PASS。其后
S10D-H 已在 Host `09d83cce5f2937db1cbe3afa36cc5461ea671574` 与 Desktop
`997345d87a5daa073c480769d57b4e59c3dfefcb` 形成实现/修复提交并执行 smoke，但从未通过；当前暂停且不能记为
PASS。S10D-V/S10E 未启动，不扩 G3，不声明 G4。

## 2J. 真实图片范围决定（2026-08-23）

本节取代此前 image kind 的“保持关闭”阶段结论，但不回写或删除历史证据。用户明确要求 FEAT-128 支持真实
文生图与图生图，并授权最多 3 至 5 次付费验证；本包固定为总上限 5 次、计划 4 次：S12E 与 S12F
分别各验证一次 T2I/I2I，另有 1 个 repair slot 只作为明确根因修复后的复验储备；它是第 5 个预算额度，
不限定物理发送序号。

| ID | 决策 | 理由 | 影响 | 状态 |
|---|---|---|---|---|
| DEC-128-033 | 使用固定 Runtime 已有 experimental `thread/start.dynamicTools` 与反向 `item/tool/call`；MiniMax-M3 决定是否调用 `generate_image`，Host 不做关键词路由 | 保留模型决策并复用 thread/turn/call identity | 先冻结 Runtime compatibility semantic candidate；除精确方法外反向请求继续 fail closed | Accepted scope；implementation NOT RUN |
| DEC-128-034 | 不改造内置 OpenAI image generation，也不经 MCP 旁路 | 内置扩展绑定 OpenAI auth/model；MCP 会弱化 Host Artifact/identity 边界 | 若当前 Runtime experimental surface 不可接受，停止并评审最小 Runtime 稳定化，不得绕行 | Accepted |
| DEC-128-035 | Host 固定中国区 `POST https://api.minimaxi.com/v1/image_generation`、`model=image-01`、`response_format=base64`、`n=1`、`prompt_optimizer=false`、验证期 `aigc_watermark=false` | 官方 API 与用户指定；避免临时 URL、多图成本和隐式默认漂移 | 模型、origin、格式、数量、optimizer、watermark 不进入工具可控参数；生产水印策略须在 Go/No-Go 复核 | Accepted |
| DEC-128-036 | 首版 I2I 只承诺当前 turn 恰有一张 PNG/JPEG 人物主体参考图，并映射为一个 `subject_reference.character` | 官方当前能力不是通用编辑 | 不支持任意编辑、多参考、上一轮 Artifact 自动回灌；用户需在当前 turn 重新附图 | Accepted |
| DEC-128-037 | Key 与 provider HTTP 只在 Host；Runtime 只收 content-free tool result，图片 bytes 只经 Artifact 链路到 Desktop | 最小化 secret/正文暴露与重复大对象 | packaged Desktop 必须设计 owner-only secret 交接；不可放命令行、普通 env 继承、WebView 或 prompt | Accepted design；secret handoff unresolved |
| DEC-128-038 | `(thread_id, turn_id, call_id)` 加参数摘要作为付费幂等 identity；请求发出后超时/取消记 outcome unknown，禁止自动重试 | MiniMax 文档没有请求幂等键或服务端取消 | 重复同参等待/复用结果；同 ID 异参协议失败；迟到结果丢弃 | Accepted |
| DEC-128-039 | 最多 5 次且每次 `n=1`；4 个 planned slots 对应 S12E T2I/I2I 与 S12F T2I/I2I，另 1 个总额度是任一失败后的单次 repair slot；不限定该 repair 的物理发送序号 | 用户授权与费用可控，同时让两种能力都形成 capability 与真实对话证据 | 单一 durable campaign `feat128-s12-image-validation-20260823`；`P1=S12E/T2I`、`P2=S12E/I2I`、`P3=S12F/T2I`、`P4=S12F/I2I`、`R1=repair(original_slot_id)`；两个 runner 共用 authority 并对 slot CAS，run root/restart 不得重置；`quota_class=planned\|repair` + `reserved_slots`/`used_calls`；repair 须绑定一次性 Owner authorization/RCA 和原失败，不能挪作新场景；pre-send 释放、sent 不可逆计 used、fake 不计；startup 回收 orphan reserved 且不补发；总 cap=5 | Accepted；S12 campaign used `0/5`、reserved `0`；此前 standalone probe 另见 08，不能借作 S12 证据 |
| DEC-128-040 | 现有 v3 Artifact shape 继续使用 `kind=image, provenance=provider`；新增的是 Runtime compatibility/tool contract，不新增 Desktop public payload | 现有 image lifecycle/preview/save 足够 | contract impact 仍为 semantic；新 candidate 需 generate/breaking/semantic review/immutable pin | Accepted design；G2A NOT RUN |

预算 epoch 解释：用户先陈述此前 standalone `image-01` 已成功生成，随后在本次 scope 指令中另行授权最多
3 至 5 次付费验证。因此 `feat128-s12-image-validation-20260823` 从本次 scope approval 开始独立建账，当前
used `0/5`、reserved `0`；历史 probe 至少一次，但不进入该 campaign，也不能用作 yijie 证据。若 Owner 对该时序解释
有异议，任何 S12 发送前必须先修订本决策并按更小剩余额度 fail closed。

### 2J.1 Owner 范围结论

| Review | Owner | 结论 | 已批准 | 仍未批准 |
|---|---|---|---|---|
| Product | 段成威 | SCOPE APPROVED | 真实 T2I、单人物主体参考 I2I、对话内展示/保存 | 通用编辑、真实 video/file/report、生产启用 |
| Technical | 段成威 | DESIGN REQUIRED BEFORE CODING | dynamic tool compatibility、Host adapter、幂等账本、Artifact 复用 | 先写 provider 再补契约、改 S10D-H 承载真实调用 |
| Security/Data | 段成威 | BOUNDED PAID VALIDATION AUTHORIZED | 最多 5 次、固定 endpoint/model、合成 prompt/参考图、content-free ledger | 真实业务图片、自动重试、任意 URL、Key 下放、生产外发 |

本节是新需求与费用边界的 Owner capture，不代表 G2/G2A/G2V、实现、真实调用或生产 PASS。

## 3. Provider activation gate

每个真实 kind 单独通过以下条件后才能启用：

1. 权威 API/tool/Runtime item 和 provider capability 有固定版本证据。
2. 用户明确授权可能产生的模型费用与外部网络访问。
3. 内容类型、最大大小、失败、取消、重试、审核和合规语义已冻结。
4. Host producer conformance、Desktop consumer conformance 和真实 local integration 通过。
5. 质量/延迟/成本 Eval 有固定 dataset 和阈值。

当前 image/video/file/report 均未通过完整 gate。image 已取得有界范围与费用授权，但工具 compatibility、Host adapter、
secret handoff、真实能力/质量与 Desktop vertical 均未形成证据；video/file/report 未获真实 producer 授权。

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
| RSK-128-014 report consumer/renderer 漂移或注入 | Desktop 额外拒绝 contract-valid document，或 raw/unknown payload、任意 chart option/formatter 进入 Vue | 合法报告不可用、XSS/代码执行、数据外传 | contract-valid conformance fixtures、native closed projection、unknown omission、fixed chart mapper、text nodes + accessible table、exact caps | Ajv-vs-Rust differential、injection/unknown/cap tests、exact-key/serializable/no-function/no-URL assertions、DOM/log/storage canary；禁止含 projection 值的 option snapshot | 关闭 S9 renderer/commands，回落 metadata shell；保留 SQLCipher canonical authority，不恢复错误契约解释 | Client/Security/Data Owner |
| RSK-128-015 chart dependency/bundle/instance 失控 | 额外 transitive、full import、license/integrity 漂移、包体超限、多 chart 未 dispose | 供应链/发行合规风险、启动回归、WebView 内存泄漏 | exact package/lock/notice/import allowlist、static tree-shaking、bundle gate、4-instance/2048-point cap、clear/dispose/disconnect | dependency/lock/source scan、raw+gzip build budget、theme/unmount/error lifecycle tests、visual matrix | 回滚 S9B-D dependency/theme/adapter/card，保留 table fallback 与 S9A canonical save | Technical/Security/Data Owner |
| RSK-128-016 v3 双流/游标非原子 | v2/v3 并跑，或 Artifact 状态先于/晚于 cursor 独立提交 | 丢事件、重复下载、严格状态机冲突、UI错位 | single v3 common decoder；event apply+cursor transaction；completed crash-safe ready/ACK intent | crash-point、replay、gap/duplicate/stream-change、cursor/state differential | 关闭 Artifact flag，恢复 single v2；保留 authority rows只读 | Runtime/Client/Data Owner |
| RSK-128-017 synthetic 测试剖面越权 | fake/synthetic 在非 exact profile、带 key/provider 或非 loopback 启动 | 误用真实 provider、付费/数据外传、错误验收 | exact master conjunction、env_clear+inject、owner/parent/run-root、fresh binary/watchdog | negative config matrix、socket/process/env evidence、zero-secret scan | 删除/关闭 profile，终止 child，清 run root；不改变默认生产路径 | Technical/Security Owner |
| RSK-128-018 UI authority/stale projection | context/tenant/session 切换后 ArtifactStore 保留旧 metadata，或 live/history竞态回退 | 跨 authority 展示、重复/错位/终态回退 | content-free invalidation、subscribe-first、v3 history authority、epoch/reset guards、trusted ids | logout/rebind/switch/delete/stale/gap tests与DOM/Pinia canary | unmount Artifact list，清 store，回落 v2 Chat UI | Client/Security/Data Owner |
| RSK-128-019 S10D harness 替代 production path 或清理不完整 | controller mount 第二 App/mock client/set store/direct DB/spool，或 Desktop/WebContent/Host/fake/WAL/temp 残留 | 虚假 vertical PASS、测试权限逃逸、内容/进程残留 | reuse exact feature、production-first bootstrap、closed test authority、scope checker、0700 root、deadlines、ordered teardown | source/static audit、real Tauri walking skeleton、PID/port/WAL/spool/temp/canary zero-hit | 删除 H hook/controller/runner；保留 S10A-C，S10D-V/E 关闭 | Technical/Security/Data Owner |
| RSK-128-020 生图工具误路由 | 普通看图/对话触发工具，或 Host 关键词猜测 | 非预期外发与付费 | 仅 Runtime structured tool call；negative intent Eval；每 turn 一次 | tool-call/no-call dataset + ledger | image flag off；保留文本/看图能力 | Product/AI Owner |
| RSK-128-021 Key 或正文越界复制 | Authorization、prompt、参考图、base64/raw response 超出已授权 input/provider/Artifact authority，或进入 result/log/evidence | secret/用户内容泄漏 | Host-only secret、closed result、授权位置 allowlist、redaction/canary、no command-line key | Key/header 全局 zero-hit（Host secret/header除外）+ prompt/reference/result/log/evidence boundary scan | kill switch、清 input/provider intermediate、轮换 Key、阻断发布；ready staging 仅按 incident evidence/deletion authority 处理 | Security/Data Owner |
| RSK-128-022 外部 URL/重定向/代理外传 | 模型注入 URL、provider client 跟随 redirect 或继承 proxy | SSRF/越区/非预期数据外发 | fixed HTTPS origin/path、redirect deny、proxy policy fixed、只用当前 turn Data URL | fake server redirect/host/proxy tests | 拒绝请求并关闭 adapter | Security Owner |
| RSK-128-023 重试与并发放大费用 | timeout/429/5xx 自动重试、duplicate call 或并行 turns | 超预算/重复图片 | durable/bounded idempotency ledger、no auto retry、single concurrency、5-call fuse | fake delayed/duplicate tests + ledger audit | image flag off；outcome unknown 等待明确新请求 | Technical/Product Owner |
| RSK-128-024 Provider 响应炸弹或伪图 | 超大 JSON/base64、invalid alphabet、magic/MIME/尺寸不符 | OOM、解析漏洞、错误 Artifact | HTTP/body/array/decoded/pixel caps、strict decode、full image validation、`n=1` | adversarial fake responses + memory bound | 丢弃 bytes、failed terminal、清中间缓冲 | Technical/Security Owner |
| RSK-128-025 内容安全/部分成功误判 | HTTP 200 但 base status 非零，或 success/failed counts 矛盾 | 违规内容/伪成功 | 同时验证 HTTP、base_resp、array、metadata；closed error mapping | official error matrix + fake fixtures | failed Artifact；不展示/保存内容 | Product/Security Owner |
| RSK-128-026 Experimental Runtime surface 漂移 | current Runtime pin 改变 dynamic tool schema/反向调用 | 工具不可用或参数错配 | Contracts compatibility candidate、fixed Runtime commit、G2V spike、exact conformance | generate/differential/runtime tests | 不注册工具；继续文本/看图；重开 G2A | Runtime/Contracts Owner |
| RSK-128-027 Packaged Desktop secret 交接缺失 | sidecar `env_clear()` 无安全 Key 来源 | 开发 Host 可用但产品链路不可用，或为求可用泄漏 Key | owner-only Key file/系统安全存储设计与双向权限测试 | packaged release-like vertical | 保持真实 image flag off；不宣称 Desktop 完成 | Client/Security Owner |
| RSK-128-028 Provider 数据保留/删除未知 | 已发送 prompt/参考图后只执行本地 rollback，或把本地清理误当 provider 删除 | 无法兑现删除承诺、真实用户内容治理失真 | S12E/F 仅合成数据；执行前复核官方当时政策并记录 known/UNKNOWN；生产用户数据另过 Go/No-Go | provider-policy snapshot + run ledger 数据分类 | 停止后续外发、清本地副本；按官方/incident 流程处置，不声称远端已删 | Security/Data Owner |

## 5. 不需要新 ADR 的前提

如果实现保持“v3 expand、Host 临时 staging、Desktop 本地 authority、无云资源、无新跨仓职责”，现有职责方向不变，可在本 Feature 决策记录内评审。若选择 Host/云端长期 Artifact 仓库、自定义共享 URL、公共分享或改变 Runtime 核心协议，必须先建立新 ADR 并取得明确批准。

## 6. 实现前批准清单

- DEC-128-005..011、ACK/poster/cursor/cancel、report compatibility、synthetic/real 分层与 Provider gate 已完成 G2 Owner 冻结。
- S6-READINESS 批准的图片 3-command/scheme/CSP 边界已由 S6A 实现，S6B 已消费而未改变 native/config；两者均为
  G3 外独立 PASS。
- S7F/S7A/S7A-REPAIR/S7B 已逐切片独立 PASS；DEC-128-016 是现行 video handle lifecycle，Pattern 1.2.0 的
  64-request 条款只保留为历史 RED。
- S8A/S8B 已分别独立 PASS，未并入 G3；Markdown 延期使 AC-005 保持 PARTIAL，G4 不得通过。
- S9A、S9B-D、checker repair 与 S9B-R 已分别独立 PASS；production Chat/Tauri vertical 仍 NOT RUN。
- S10A/S10B/S10C 已在独立授权下分别 separate PASS；S10D-READINESS/Pattern 1.7.0
  `8afdc996c11bbad2d275eb8b86a0f6b82ca5da52` 当时只批准 S10D-H。H 后续实现但 smoke FAIL/PAUSED；
  D-V/E 仍 NOT RUN；readiness 和 implementation commit 都不等于 runtime PASS。
- Contracts v3 source、基线、generator/adapter、unknown kind/section 行为和 consumer 顺序已完成 G2 设计评审；S1/S2 真实生成、检查、双 breaking 与不可变 commit 已通过。
- Desktop SQLCipher v8 migration、64 MiB 单 Artifact 上限、七天 retention 起算与恢复边界已在 S4 实现并通过迁移/reopen/TTL/delete 验证；图片 native preview/save/CSP 属 S6A，S6B 只做 renderer。
- 真实 MiniMax image 已获得最多 5 次的 S12 开发验证授权；此前另有一次用户确认成功的 standalone
  `image-01` probe，但没有经过 yijie tool/Host/Artifact/Desktop，也没有可复核的完整 run evidence，不能借作 S12 PASS。
  S12 campaign 尚未发送，生产 activation 继续关闭。
- S12A 已完成 legacy schema v1→v2 治理迁移、04A 时序矩阵和 S10D-H 失败事实/fuse 迁移并形成新 G2；S12B
  在 G2 后形成 Runtime compatibility candidate 与 G2A；S12C 在 G2A 后以 fake provider 形成 G2V；S12D/E/F
  逐项消费前置。不得把旧 G2A 自动外推到 dynamic tool contract，也不得要求尚未实现的 S12C G2V 反向阻塞 S12A。

## 7. 当前 Gate 结论

- G0：PASS，Feature ID、Owner、本地边界和初始 Git 状态已记录。
- G1：PASS，场景、AC、受影响仓库、最高 contract impact 和主要风险已识别。
- G2：active schema v2 为 `PASS`；S12A 已把真实图片设计、04A、S12 图和 H failure fuse 机器绑定。历史 v1 的 Product/Design、Technical/Contracts、Security/Data G2 capture 继续保留，但不覆盖新范围。
- G2A：active schema v2 为 `PENDING`，等待 S12B Runtime dynamic-tool contract candidate。历史 v1 Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b` 的 G2A PASS 只覆盖旧 Artifact v3 范围，不能外推到新工具协议。
- G3：只对 S3/S4/S5 原子切片通过；S6A-S10C 的历史独立 PASS 不自动转换为 schema v2 per-slice G3。
  S10D-H 已实现/执行但 smoke `FAIL`，当前暂停；S10D-V/S10E 未启动。
- 新 image scope：G0/G1/G2 与 S12A governance migration 已 `PASS`；G2A `PENDING`，G2V 因 open H cleanup fuse 与未合格 S12 harness 为 `BLOCKED`，S12B-S12F `NOT RUN`；
  历史 standalone provider probe 只证明 Key/provider 曾可用，不改变任一 yijie gate。
  S12 campaign 付费账本为 used `0/5`、reserved `0`。G4-G6 未通过，生产 provider 关闭。
