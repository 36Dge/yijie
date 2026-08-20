# FEAT-128 交付总结与关闭记录

## 1. 当前结果

- G2 closure rewrite、Product/Technical/Security/Data Owner sign-off 与 UI Pattern `Accepted` 已完成；Pattern
  1.1.0 完成 S6-READINESS，随后 S6A native boundary 与 S6B image renderer 已分别独立实现并提交。
- Contracts S1/S2 已形成真实、不可变、未发布的 `0.4.0` local candidate；locked generation、lint、test、
  build、双 baseline breaking、v1/v2 equality 与 semantic review 全部通过。
- G2A 后严格先完成 Host S3：v3 dual route、bounded encrypted staging、owner-only content/poster、range、
  ACK/TTL/restart cleanup 与四类 exact-local synthetic producer。
- Host S3 通过后完成 Desktop S4：SQLCipher v8、closed event/report adapter、native transfer/commit/ACK、
  168h retention/delete、metadata-only history v3 与实现级 pin；没有 renderer、CSP 或 save。
- Desktop S5 已完成 provider-neutral identity/status/progress reducer、按 session/turn/Artifact 管理的 Pinia store
  与稳定 generic metadata shell/list；只消费 parser-approved metadata，没有 preview/action/wire parsing。
- S6-READINESS 已将图片能力拆成 S6A native preview/save boundary 与 S6B renderer，冻结 exact private schema/
  commands、opaque image scheme、最小 CSP 和 native save 边界，并记录 Owner 只批准 S6A 编码。
- S6A 已完成 3 exact private commands、双次 SQLCipher 校验、30s one-shot opaque preview、native atomic save、
  typed content-free client 与精确 `img-src` 增量；没有 Vue renderer、依赖、capability 或 migration。
- S6B 已完成 ready-image-only inline preview、每次 fresh handle 的 lightbox、100/125/150/200% 有限缩放、
  content-free native-save UX、focus/keyboard/reduced-motion/axe 与 stale/release 防护；没有 native/config/page/pin 变化。
- S7-READINESS 曾确认 Contracts canonical MP4 可播放/可 Range seek，而当时 Host S3 synthetic MP4 是无 `moov`
  的 transport-only 输出；Pattern 1.2.0 冻结 S7F/S7A/S7B、独立 video protocol/native save/精确 CSP，并历史性
  只批准 S7F。后续 S7 全链已完成。
- S7F 已在 Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` 让 strict-local video 对齐 immutable
  canonical raw bytes，并以 snapshot/source/tree checker、bounded MP4 audit、manifest/poster/auth/Range 与全量 Host 门禁通过。
- S7A 已在 Desktop `22b91c5a258458c87f1ac96c06bf39d1af97358f` 完成独立 private video schema/client、
  SQLCipher bounded inspect/Range、multi-request opaque protocol、native atomic `.mp4` save 与 exact `media-src`；无 renderer/UI。
- S7A-REPAIR 已在 Desktop `34991d8967de9aa2197ab2e8b9b49347774df7a5` 移除不兼容的 64-success lifetime
  revocation，并以编译期关闭、content-free harness 证明真实 WebView 76 Range、metadata/playback/seek PASS、零 404。
- S7B 已在 Desktop `366186b601144bdc2bc87a2cef3075b74f1e8f19` 完成 ready-video native controls、稳定
  metadata/error/expired/retry、pause-clear-load-release、stale isolation 与 content-free native-save UX。
- S8-READINESS/S7-SPEC-RECONCILIATION 已把 Pattern 升为 1.3.0：累计 request-count 不再撤销 video handle；S8
  拆为 S8A bounded native file preview/save 与 S8B renderer。Owner 延期 Markdown，AC-005 `PARTIAL`；只批准下一
  编码切片 S8A，S8A/S8B 均未实现。
- S3/S4/S5 的 G3 slice gate 已通过且范围未扩展；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B 作为独立切片 PASS，均不并入
  G3。S8A-S12、真实 provider、tag、push、release、production 与 G4-G6 仍关闭。

## 2. 实际版本与提交

| Component | Version/status | Full commit | 说明 |
|---|---|---|---|
| Feature package | G3 S3/S4/S5 + S6/S7 separate PASS + S8 readiness docs PASS | 本次 `yijie` 文档提交 | governance/evidence only；G3 unchanged；G4 pending |
| Desktop Pattern | Accepted 1.3.0 S8 readiness/S7 reconciliation | `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` | docs only；S8A/S8B NOT RUN；Pattern 1.2.0 history retained |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable；no tag/release |
| Agent Host | S3 PASS + S7F separate PASS; default off | S7F `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`; S3 `4017785adb08e1114781d3d844e9a10a683fa933` | canonical strict-local video conformance；Contracts/tree unchanged |
| Desktop | S4/S5 PASS; S6A/S6B/S7A/S7A-REPAIR/S7B separate PASS; default off | S7B `366186b601144bdc2bc87a2cef3075b74f1e8f19`; S7A-REPAIR `34991d8967de9aa2197ab2e8b9b49347774df7a5`; S7A `22b91c5a258458c87f1ac96c06bf39d1af97358f`; S6B `4a8dce6a6526e37052941f6dbb921ba2486e109f`; S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983` | Contracts/Host/pins unchanged；production page/vertical仍待 S10 |

关键 source digests：OpenAPI `cf72ba8dd6910e8454ad60feeffa5e82583303b441dad78e49910fbdb9f5420f`，
event v3 `87b1284056529bde8314e6cfa6ad1fb27ffefef50ea86033875fda795330939f`，report v1
`94715e5b821cca686405d06004b805e9eac6d39dc61e19c9fc38925102f79556`，v3 Proto
`5021a0342b84cdea0e1dd773728e4c8f013ce7d03377ade18f06f6716a81b70d`。

## 3. 验收结果

| 范围 | 结果 | Evidence |
|---|---|---|
| Requirements/design traceability | PASS | 00-07 + Pattern Accepted + package checks |
| Contracts S1/S2 | PASS | `pnpm generate/lint/test/build`、39/39 Node + Go、双 breaking、semantic review |
| Host exact pin | PASS | sync/contract-check/lint/test at `dea84d...` |
| Desktop exact pin | PASS | generate-check/lint/test/build/docs at `960944...` |
| Host S3 | PASS | contract-check/lint/test/runtime-test at `4017785...` |
| Desktop S4 | PASS | generate-check/lint/test/build/docs at `09220dd...`; TS 276/276, Rust 184 pass/3 ignored |
| Desktop S5 | PASS | RED first；19 focused tests；`make lint/test/build`、`pnpm docs:build`、diff checks；TS 295/295, Rust 184 pass/3 ignored at `7548ea8...` |
| S6-READINESS | PASS FOR DOCS ONLY | Desktop audit + Pattern 1.1.0；`pnpm docs:build/lint/test`、diff check；yijie package/strict/YAML/lint/test/diff checks；无业务代码/config diff |
| Desktop S6A | PASS AS SEPARATE SLICE | expected RED；6 TS + 11 Rust focused；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff；TS 301/301、full Rust 196 pass/3 ignored；`8b99849d...` |
| Desktop S6B | PASS AS SEPARATE SLICE | missing-component RED；3 files/12 focused GREEN；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff；TS 308/308、axe/reduced-motion；`4a8dce6a...`；runtime visual matrix NOT RUN |
| S7-READINESS (historical) | PASS FOR DOCS ONLY / READY FOR S7F ONLY at capture | canonical/Host/Desktop read-only audits；Pattern 1.2.0；S7 chain later separate PASS；`18b17d961ed5991cec55eeb230ea21d91f2fb8ec` |
| Host S7F | PASS AS SEPARATE SLICE | EXPECTED RED 81-byte/digest/missing-moov；GREEN exact 1,642-byte raw identity + bounded MP4/manifest/poster/auth/GET/HEAD/Range；`make contract-check/lint/test/runtime-test`、diff PASS；`1045dd06534eb72d53eb7ad7b7d18e63c80284f8` |
| Desktop S7A | PASS AS SEPARATE SLICE | EXPECTED TS/Rust RED；2 TS files/5 tests、11 focused Rust + 1 SQLCipher reader GREEN；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff PASS；45 files/313 tests；`22b91c5a258458c87f1ac96c06bf39d1af97358f` |
| Desktop S7A-REPAIR | PASS AS SEPARATE SLICE | request 65 EXPECTED RED；128-request GREEN；default 11/11 + feature 12/12 Rust；real WebView 76 Range、metadata/playback/seek、零 404；clippy/diff PASS；`34991d8967de9aa2197ab2e8b9b49347774df7a5` |
| Desktop S7B | PASS AS SEPARATE SLICE | missing-component RED；3 files/14 focused；47 files/324 full；axe/reduced-motion、lint/build/docs/diff、real WebView metadata/playback/seek PASS；`366186b601144bdc2bc87a2cef3075b74f1e8f19` |
| S8-READINESS | PASS FOR DOCS ONLY / READY FOR S8A ONLY | four-repo read-only audit；Pattern 1.3.0；exact two-command/limits/lifecycle/save/rollback；Desktop docs/lint/test/diff 与 yijie package/strict/YAML/lint/test/shell/diff；无业务代码/config diff |
| AC contract portions | CONTRACT PASS | lifecycle/resource/ACK/report/fixtures/negative cases |
| AC Host/native foundation portions | PARTIAL PASS | S3/S4 lifecycle/resource/persistence/history/retention conformance |
| AC generic shell portion | S5 FOUNDATION PASS | monotonic/closed reducer、history/live shared store、generic accessible metadata shell |
| AC-003 image preview/save boundary | S6A NATIVE PASS / S6B COMPONENT PASS / E2E NOT RUN | native security/save boundary + reusable ready image/lightbox/save UX implemented and tested；page/runtime visual integration pending |
| AC-004 video boundary | S7A NATIVE + S7A-REPAIR + S7B COMPONENT/RUNTIME PASS / VERTICAL PENDING | MP4 inspect/Range/save、playback-compatible lifetime、native controls/save UX 与真实 metadata/playback/seek 已验证；production vertical待 S10 |
| AC-005 file behavior | READINESS PASS / AC PARTIAL / IMPLEMENTATION NOT RUN | current-v3 plain/CSV/JSON bounded preview + five-MIME native save frozen；Markdown deferred/G4 blocked；S8A/S8B pending |
| AC type renderer/E2E portions | PARTIAL | image/video reusable components PASS；file/report renderer 与 integrated production E2E 未开始 |
| Real provider capability | BLOCKED/UNKNOWN | 无付费调用或 authority |

## 4. 安全、数据与兼容边界

- v1/v2 wire、schema、fixtures 与语义保持不变；v3 使用显式 path 与 `event_schema_version=3`。
- Artifact content/poster/ACK、owner/session scope、relative href、MIME/size/digest、range 与 stable errors 已入契约。
- Report known sections strict；unknown 只允许 `required=false`、opaque、128 KiB/depth 8，禁止 HTML/URL/script。
- Host encrypted staging、24h TTL 与 ACK cleanup 已在 S3 实现；Desktop commit+168h retention 与 cleanup
  receipt 已在 S4 实现。S6A 只允许 `yijie-artifact-preview://localhost/v1/<opaque-handle>`：256-bit/
  43-char、30s absolute TTL、one-shot、main WebView/process/context/owner/tenant/session/turn bound、4 handles/
  WebView、1/artifact、2 reads、40 MiB in-flight；签发与 GET 双次复核 ready image/MIME/20 MiB/digest/image limits。
- S6A native save 只由明确用户操作触发，native 管理 `.png/.jpg/.webp`、dialog/overwrite、同目录 `0600`
  no-follow temp、分块 digest、fsync/atomic replace；Vue 只收 content-free saved/cancelled/failed，不收 path/name/
  digest/bytes。只允许 `img-src` 追加该 scheme，不新增依赖/plugin/capability/migration 或 generic fs/shell。
- 用户批准的最小例外只刷新 Desktop 内部 consumer implementation/readiness digests 与 checker 常量；Contracts
  `full_commit=ea48fe...`、source SHA、fixtures、version、operation/schema、Host 与公共协议均未改变。
- 四种 exact-local synthetic fixtures 已存在；真实 `provider|tool` activation 仍分 kind blocked。
- canonical video resource 是 raw 1,642 bytes、SHA-256 `96ea070c...77dd5`、H.264 High/16×16/25fps/0.12s/
  3 frames、front `moov`/first keyframe；Host S7F 已从锁定 source 派生并复核 exact bytes，不依赖 runtime sibling。
- S7A 已实现 `yijie-artifact-video://localhost/v1/<opaque-handle>`：30min absolute/5min idle、2 handles/
  WebView、1/artifact、playback-compatible multi-request lifetime、2 reads/64MiB；identity-only 3 commands、GET/HEAD
  single Range 200/206/416、no CORS/query/body/redirect/error body，CSP 只新增精确 video scheme。S7A-REPAIR 只移除
  累计请求撤销；S7B Vue 只持有当前播放 lease 的 opaque URL，不 fetch、不持久化，并在切换/错误/卸载释放。
- S8A 只批准 `chat_read_artifact_file_preview_v1` 与 `chat_save_artifact_file_v1`：identity-only、SQLCipher 双次
  authority/format 校验、plain/CSV/JSON bounded projection、PDF/XLSX metadata/native save-only，不新增 protocol/CSP/
  capability/dependency/migration。用户明确打开后的 safe projection 只可短暂进入组件 local state/DOM；不得进入
  Pinia/history/storage/log/diagnostics/snapshot，关闭/切换/卸载后必须清空。
- Immutable v3 file output 不含 `text/markdown`；不得从 v2 turn input 偷渡或伪装为 plain。若本期要求 Markdown，
  必须重开 G2/G2A、Contracts semantic flow 与 downstream repin。

## 5. G2/G2A Owner 结论

用户明确要求 Codex 将其 Owner 指令分别记录为 Product/Design、Technical、Security/Data 的
`G2 APPROVED`，并把 UI Pattern 改为 `Accepted`。用户还明确给出 G2A 条件：真实 generate、breaking、
semantic review 与 immutable pin 完成后才能开始 Host/Desktop。实际证据满足后，G2A 记录为
`APPROVED`。这是用户授权的 Owner capture，不是 Codex 自称独立人工批准。

| Gate | Decision | Date | Evidence |
|---|---|---|---|
| G0 Intake | PASS | 2026-08-20 | explicit request + 00/feature.yaml |
| G1 Design Ready | PASS | 2026-08-20 | 01-03 + repository investigation |
| G2 Implementation Ready | APPROVED for S1/S2 | 2026-08-20 | 03 §2A/2B + 04-07 + Pattern Accepted |
| G2A Contract Ready | APPROVED | 2026-08-20 | Contracts immutable candidate + dual breaking + semantic review + downstream exact pins |
| G3 Slice Complete | PASS for S3/S4/S5 | 2026-08-20 | immutable Host/Desktop commits + focused/full gates + diff/clean checks |
| S6 Readiness | APPROVED FOR S6A CODING ONLY | 2026-08-20 | 03 §2C + Pattern 1.1.0；S6B waits for S6A immutable PASS；不扩 G3 |
| S6A Slice | PASS OUTSIDE G3 | 2026-08-20 | `8b99849d418a3ef226f4133128f1ac22a438f9d5` + RED/GREEN/full gates；无 renderer |
| S6B Slice | PASS OUTSIDE G3 | 2026-08-20 | `4a8dce6a6526e37052941f6dbb921ba2486e109f` + RED/GREEN/full gates；无 native/config/page drift；runtime visual NOT RUN |
| S7 Readiness | HISTORICAL READY FOR S7F ONLY | 2026-08-20 | Pattern 1.2.0 `18b17d961ed5991cec55eeb230ea21d91f2fb8ec`；readiness docs only；不扩 G3 |
| S7F Slice | PASS OUTSIDE G3 | 2026-08-20 | Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` + RED/GREEN/full gates；Contracts/tree/Desktop/dependency/public wire unchanged |
| S7A Slice | PASS OUTSIDE G3 | 2026-08-20 | Desktop `22b91c5a258458c87f1ac96c06bf39d1af97358f` + RED/GREEN/full gates；无 renderer/public pin/dependency/capability/migration drift |
| S7A-REPAIR Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `34991d8967de9aa2197ab2e8b9b49347774df7a5` + request-limit RED/GREEN + real WebView 76 Range PASS；无 schema/protocol/config drift |
| S7B Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `366186b601144bdc2bc87a2cef3075b74f1e8f19` + component/full/runtime gates；无 native/config/page drift |
| S8 Readiness | READY FOR S8A ONLY；AC-005 PARTIAL；S8B WAIT | 2026-08-21 | 03 §2E + Pattern 1.3.0 `4929a73a7871056d7aeca3eb0b27c682b21bfe4b`；docs only |
| G4 Code Complete | PENDING | N/A | S8A/S8B/S9-S11、Markdown/full AC、E2E/full visual/performance/独立 review 未完成 |
| G5/G6 | NOT PASSED | N/A | local-only scope has no release/deployment/production evidence |

## 6. 未验证项与已知限制

| Item | 状态 | 下一证据 |
|---|---|---|
| Host v3 route/staging/resource/synthetic producer | S3 PASS | S10 cross-process/restart walking skeleton |
| Desktop SQLCipher/native transfer/history/private IPC | S4 PASS | S10 integrated lifecycle |
| Desktop generic domain/store/shell | S5 PASS | S10 history/live integrated lifecycle + visual/performance evidence |
| S6A native image preview/save boundary | PASS | S10 仍需 integrated lifecycle 证据 |
| S6B image renderer/lightbox/zoom/save UX | COMPONENT PASS | focused/full/axe 通过；Chat page、真实 Tauri visual/runtime 与 vertical lifecycle 待 S10 |
| S7A/S7A-REPAIR native video inspect/Range/save | PASS | S10 仍需 production vertical/longer-media lifecycle evidence |
| S7B ready-video renderer/native-save UX | COMPONENT + REAL WEBVIEW MEDIA PASS | production Chat page、light/dark/1180x760/200% manual matrix 与 performance待 S10 |
| S8A file native boundary | NOT RUN；READY FOR CODING ONLY | next explicit S8A instruction + RED/GREEN/full Desktop gates |
| S8B file renderer | NOT RUN | S8B waits S8A immutable PASS；S9 report renderer/component/visual/a11y later |
| synthetic local vertical slice | NOT RUN | S10 E2E/security/performance/visual |
| synthetic video playback/seek | CONTRACT + HOST S7F + DESKTOP S7A/S7A-REPAIR/S7B PASS | real Tauri WebView shell smoke metadata/playback/seek true；production Chat vertical仍待 S10 |
| MiniMax real image | BLOCKED | fixed provider capability + separate paid authorization/eval |
| real video/file/report producers | BLOCKED | per-kind authority/ownership/security design |
| release/deployment | N/A current scope | separate G5/G6 package if later requested |

## 7. 下一步与停止条件

1. 下一步只执行 07 §16 的 S8A Desktop-private bounded file preview/save boundary；S8B 等 S8A immutable PASS 与单独
   授权。不得启动 S9-S12 或 production page integration。
2. S8A 不得修改既有 S6/S7 boundary；若需要 protocol/CSP/dependency/plugin/capability/migration、扩大 frozen limits、
   Markdown/Contracts/Host/public pin 漂移或真实 provider，立即停止。
3. 任何 ACK、limits、retention clock、report compatibility、auth/CSP 或 authority 漂移先重开 G2；
   Contracts pin 漂移先重开 G2A。
4. 不启动真实 provider，不 tag/push/publish/release，不把 pin conformance 描述成 Code Complete。

## 8. 文档与交接

| Artifact | Path | Owner | 状态 |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-128-structured-chat-artifacts/` | 段成威 | G3 remains S3/S4/S5；S6/S7 separate PASS；S8 readiness docs PASS；S8A-S11 pending |
| Desktop UI Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/14-feat-128-structured-chat-artifacts.md` | 段成威 | Accepted 1.3.0 at `4929a73a...`；S8A/S8B frozen, not implemented |
| Contracts semantic review | `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md` | Contracts Owner | PASS |
| Release/rollback plan | `09-release-and-rollback.md` | 段成威 | no release executed |

正式关闭时间尚未形成。当前准确状态是：`G3 PASS only for S3/S4/S5; S6A, S6B, S7F, S7A, S7A-REPAIR and S7B separate PASS; S8 readiness docs PASS / S8A-S11 pending; real providers closed; G4-G6 not passed`。
