# FEAT-128 交付总结与关闭记录

## 1. 当前结果

- G2 closure rewrite、Product/Technical/Security/Data Owner sign-off 与 UI Pattern `Accepted` 已完成；Pattern
  1.1.0 完成 S6-READINESS，随后 S6A native preview/save boundary 已按该边界独立实现并提交。
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
- S3/S4/S5 的 G3 slice gate 已通过且范围未扩展；S6A 作为独立切片 PASS，不并入 G3。S6B-S12、真实
  provider、tag、push、release、production 与 G4-G6 仍关闭。

## 2. 实际版本与提交

| Component | Version/status | Full commit | 说明 |
|---|---|---|---|
| Feature package | G3 recorded for S3/S4/S5 + S6 readiness/S6A evidence | 本次 `yijie` 文档提交 | governance/evidence only；G3 unchanged |
| Desktop Pattern | Accepted 1.1.0 S6 readiness | `2b854b40379a207c19bf37fc5bc64266553c5df1` | docs only；G2A record `35efa147...`；initial acceptance `e97b2dab...` |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable；no tag/release |
| Agent Host | S3 PASS; default off | `4017785adb08e1114781d3d844e9a10a683fa933` | pin base `dea84d...`; strict-local synthetic only |
| Desktop | S4/S5 PASS; S6 readiness docs PASS; S6A separate PASS; default off | S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; readiness `2b854b40379a207c19bf37fc5bc64266553c5df1`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983` | Contracts pin stays `ea48fe...`; no S6B renderer/UI |

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
| AC contract portions | CONTRACT PASS | lifecycle/resource/ACK/report/fixtures/negative cases |
| AC Host/native foundation portions | PARTIAL PASS | S3/S4 lifecycle/resource/persistence/history/retention conformance |
| AC generic shell portion | S5 FOUNDATION PASS | monotonic/closed reducer、history/live shared store、generic accessible metadata shell |
| AC-003 image preview/save boundary | S6A NATIVE PASS / S6B UI NOT RUN | native security/save boundary implemented and tested；renderer/visual integration pending |
| AC type renderer/E2E portions | NOT RUN | S6B-S10 未开始 |
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
| G4 Code Complete | PENDING | N/A | S6B-S11、全部 AC/E2E/独立 review 未完成 |
| G5/G6 | NOT PASSED | N/A | local-only scope has no release/deployment/production evidence |

## 6. 未验证项与已知限制

| Item | 状态 | 下一证据 |
|---|---|---|
| Host v3 route/staging/resource/synthetic producer | S3 PASS | S10 cross-process/restart walking skeleton |
| Desktop SQLCipher/native transfer/history/private IPC | S4 PASS | S10 integrated lifecycle |
| Desktop generic domain/store/shell | S5 PASS | S10 history/live integrated lifecycle + visual/performance evidence |
| S6A native image preview/save boundary | PASS | S6B/S10 仍需 WebView renderer 与 integrated lifecycle 证据 |
| S6B image renderer/lightbox/zoom/save UX | NOT RUN | S6A prerequisite satisfied；仍需独立执行 component/visual/a11y |
| video/file/report type renderers | NOT RUN | S7-S9 component/visual/a11y |
| synthetic local vertical slice | NOT RUN | S10 E2E/security/performance/visual |
| synthetic video playback/seek | NOT RUN | 当前 S3 MP4 fixture 无 `moov`，S7/S10 需可播放本地 fixture + controls/range smoke |
| MiniMax real image | BLOCKED | fixed provider capability + separate paid authorization/eval |
| real video/file/report producers | BLOCKED | per-kind authority/ownership/security design |
| release/deployment | N/A current scope | separate G5/G6 package if later requested |

## 7. 下一步与停止条件

1. 本轮止于 S6A immutable PASS。下一候选是 `07-implementation-plan.md` §12 的独立 S6B；不得顺带启动 S7-S12。
2. S6B 必须只消费既有 typed client 与 opaque preview URL，修改 TS/Vue renderer 范围；若需要任何 src-tauri/
   config、依赖/plugin/capability/permission、DB migration、generic protocol、外部 origin 或 bytes/path to Vue，立即停止。
3. 任何 ACK、limits、retention clock、report compatibility、auth/CSP 或 authority 漂移先重开 G2；
   Contracts pin 漂移先重开 G2A。
4. 不启动真实 provider，不 tag/push/publish/release，不把 pin conformance 描述成 Code Complete。

## 8. 文档与交接

| Artifact | Path | Owner | 状态 |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-128-structured-chat-artifacts/` | 段成威 | G3 remains S3/S4/S5；S6A separate PASS recorded |
| Desktop UI Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/14-feat-128-structured-chat-artifacts.md` | 段成威 | Accepted 1.1.0；S6A conformed；S6B pending |
| Contracts semantic review | `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md` | Contracts Owner | PASS |
| Release/rollback plan | `09-release-and-rollback.md` | 段成威 | no release executed |

正式关闭时间尚未形成。当前准确状态是：`G3 PASS only for S3/S4/S5; S6A separate PASS; S6B-S11 pending; real providers closed; G4-G6 not passed`。
