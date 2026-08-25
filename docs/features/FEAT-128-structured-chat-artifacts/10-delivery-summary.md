# FEAT-128 交付总结与当前状态

> **当前执行路线（2026-08-23）**：真实图片生成改由 [`demo-fast/`](demo-fast/) 独立账本连续实现并以
> fresh local real-service D4 为完成条件。以下 schema v2 总结是历史 `production_hardened` 状态；其中
> S10D-H 继续保持 `FAIL/PAUSED` 且 fuse open，不因路线切换而关闭、重试或改写。

## 1. 当前结果

- 2026-08-23 用户把真实图片生成正式纳入 FEAT-128：MiniMax-M3 通过结构化 tool 决策，Agent Host 固定调用
  中国区 `image-01`，支持文生图与当前轮单张人物参考图生图，校验 base64 后发布现有 v3 image Artifact，
  Desktop 复用既有展示/预览/保存链路。最多 5 次 S12 campaign 付费验证已获授权，计划 4 次，当前 used `0/5`、
  reserved `0`；实现与 yijie 链路验证尚未开始。用户确认 scope 前已有一次 standalone `image-01` 成功 probe，
  但它没有经过 yijie 且证据不完整，不进入 S12 campaign。
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
  编码切片 S8A。
- S8A 已在 Desktop `bf5452f7fde24d1391845deaba17ec1135716c62` 完成 exact two-command、identity-only、双次
  SQLCipher/revision/format 校验、plain/CSV/JSON bounded projection、five-MIME native atomic save、file-only
  verified residue cleanup 与 typed domain/client；没有 Vue component、protocol/config/dependency/migration。
- S8B 已在 Desktop `4d0238b1906f02d319f47f5e55cdc023485ef07a` 完成 ready-file explicit preview、inert
  plain/JSON/CSV、PDF/XLSX fallback、bounded literal search、projection lifecycle 与 content-free native-save UX；没有
  native/config/checker/page/store/dependency/pin 变化。
- S9-READINESS 已把 Accepted Pattern 升为 1.4.0 `b6f7401c79d5b2356bc45468f14d7fdbb17a855c`：确认 report
  SQLCipher authority 已有 canonical bytes但 history/private IPC 仍 metadata-only；冻结 S9A consumer conformance repair、
  exact identity-only bounded projection/canonical JSON native save 与 S9B fixed chart adapter。active app 没有 ECharts
  dependency/theme，故只批准 S9A，S9B blocked/waits；本轮无业务代码/config/dependency diff。
- S9A 已在 Desktop `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` 完成 immutable-schema-valid consumer repair、
  exact two-command bounded closed projection、canonical report JSON native save 与 verified residue cleanup；没有 renderer、
  component、config、dependency、migration、Contracts/Host/public pin 或 S6-S8 漂移。
- S9B-READINESS 已把 Accepted Pattern 升为 1.5.0 `630c3c8d55a2617499f51bd5bed263b819aaf084`：选择
  exact `echarts@6.1.0` + static tree-shaken core + Canvas，拒绝 `vue-echarts`；冻结 exact integrity/license/
  transitives/NOTICE/import/bundle、accessible semantic theme/card、closed adapter/table fallback、honest-unavailable
  unit/source/time-range、local lifecycle、visual/a11y 与 S9B-D/S9B-R 回滚。本轮未安装依赖、未改
  lockfile/config、未实现 renderer；Owner 只批准下一编码切片 S9B-D，S9B-R 等待 D immutable PASS。
- S9B-D 已在 Desktop `0a36ca7c54460d22ea6b3228832a57f05f0bde68` 完成 exact ECharts/3-node lock/NOTICE、
  semantic chart tokens/theme、closed frozen adapter + pure ordinal budget、accessible one-instance `YjChartCard`、dependency/
  bundle checker 与 test-only visual harness；57 files/360 tests、bundle 655,731 raw/206,565 gzip-9 与 18-case real-browser
  matrix PASS。未调用 S9A client、读取真实 report 或修改 Chat/native/config/pages/stores/public pin。
- S9B-D-CHECKER-REPAIR 已在 Desktop `aec0f8a05ba7534132cbb4f46be64e333d7e9024` 修复旧 checker 将 readiness
  后所有 diff 误归 S9B-D 的问题：历史 `630c3c8…→0a36ca7…` scope 固定审计，当前只保护 immutable D production
  boundary。只改两个 checker 文件；57 files/363 tests 与全量 Desktop gates PASS；S9B-R 后续在独立授权下完成。
- S9B-R 已在 Desktop `6bcc2a6bfb4db76398ecf5483c688475477f08ed` 完成 ready-report 显式预览、inert
  known/unknown sections、ordinal identity、每次打开 4 charts/2,048 points 的受控增强、始终可见的 accessible table、
  stale/clear/dispose lifecycle 与 canonical JSON native-save UX；3 files/14 focused、59 files/373 full、bundle 与
  18-case real-browser matrix PASS。S10C production ChatPage wiring 后续已通过；real Tauri report vertical 仍 NOT RUN。
- FEAT126 compile-guard repair `c257fe9e31979cc3f2f426ab1cb7c11ce8781732` 恢复了 S6 image protocol 与 S7 video
  commands/protocol 的 compile reachability，没有注册 surface；consumer digest refresh
  `3e5a3830a34718bf7bf0632cc71fc4c4ab9ea4b7` 只同步内部 `chat/mod.rs` readiness/runtime-gate SHA。
- S10A-LOCAL-PROFILE 已在 Host `0debd877a4afe1bf2da8c988caeb1124d0fa7272` 与 Desktop
  `f4a3d42ad837ecdc8a8ba4198b269d4717285791` 独立 PASS：post-commit runner 四类 lifecycle/GET/ACK=`4/4/4/4/4`，
  zeroProvider/zeroNonLoopback/cleanup=true。
- S10B-NATIVE-LIVE 已在 Desktop `f787d70b4cfb51cde76bdce047ba630f4b7b1250` 独立 PASS：single-v3 common
  order、Artifact/assistant/cursor atomic commit、ready/ACK-intent/cursor crash recovery 与 content-free private invalidation 已验证。
- S10C-PAGE 已在 Desktop `86f02b4def4d07f76d66ebdafafda5a9bb75035c` 独立 PASS：closed history v3、
  subscribe-first buffering、ArtifactStore authority epoch、bounded live resync 与 production ChatPage/List/four-client wiring 已验证。
- S10D-READINESS/S10-SPEC-RECONCILIATION 已把 Accepted Pattern 升为 1.7.0
  `8afdc996c11bbad2d275eb8b86a0f6b82ca5da52`：确认 S7B seeded shell、S9 Vite fake 与 S10A sidecar runner 均不能
  证明 production vertical；S10D 拆为 H harness/walking skeleton 与 V full vertical，当时只批准 H 编码。H 后续在
  Host `09d83cce5f2937db1cbe3afa36cc5461ea671574` 与 Desktop `997345d87a5daa073c480769d57b4e59c3dfefcb`
  形成实现提交，但没有一次完整 runtime smoke PASS，最新已知主失败类为 `runtime_axe_serious_critical`，并已按用户指令暂停。
- S3/S4/S5 的历史 G3 slice gate 已通过且范围未扩展；S6A-S10C、guard/digest repair 均为独立 PASS，不并入
  schema v2 per-slice G3。S10D-H 为 FAIL/PAUSED，S10D-V/S10E 未运行。S12A schema v2 governance/G2 已完成；S12B-F、qualified provider 调用、tag、push、
  release、production Tauri vertical 与 G4-G6 均未发生或未通过；历史 standalone probe 只保留为未限定观察。

## 2. 实际版本与提交

| Component | Version/status | Full commit | 说明 |
|---|---|---|---|
| Feature package | active schema v2；S12A governance/G2 PASS；historical G3 S3/S4/S5 + S6-S10C/guard/digest separate PASS；S10D-H FAIL/PAUSED | 本次 `yijie` 文档工作树；提交未形成 | G2A pending；G2V blocked；G4 pending |
| Desktop Pattern | Accepted 1.7.0 historical S10D readiness | `8afdc996c11bbad2d275eb8b86a0f6b82ca5da52` | docs-only readiness；READY FOR S10D-H ONLY at capture；H later FAIL/PAUSED，V/E NOT RUN |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable；no tag/release |
| Agent Host | S3 PASS + S7F/S10A separate PASS；H failed candidate；real-image adapter absent/default off | H `09d83cce5f2937db1cbe3afa36cc5461ea671574`; S10A `0debd877a4afe1bf2da8c988caeb1124d0fa7272`; S7F `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`; S3 `4017785adb08e1114781d3d844e9a10a683fa933` | H SHA 不是 PASS pin；dynamic-tool router/provider/secret handoff 未实现 |
| Desktop | S4/S5 PASS；S6-S10C + guard/digest separate PASS；H failed candidate；default off | H `997345d87a5daa073c480769d57b4e59c3dfefcb`; S10C `86f02b4def4d07f76d66ebdafafda5a9bb75035c`; S10B `f787d70b4cfb51cde76bdce047ba630f4b7b1250`; S10A `f4a3d42ad837ecdc8a8ba4198b269d4717285791`; earlier SHAs见08 | public pin unchanged；现有 image renderer 可复用；packaged Key handoff 未实现 |

关键 source digests：OpenAPI `cf72ba8dd6910e8454ad60feeffa5e82583303b441dad78e49910fbdb9f5420f`，
event v3 `87b1284056529bde8314e6cfa6ad1fb27ffefef50ea86033875fda795330939f`，report v1
`94715e5b821cca686405d06004b805e9eac6d39dc61e19c9fc38925102f79556`，v3 Proto
`5021a0342b84cdea0e1dd773728e4c8f013ce7d03377ade18f06f6716a81b70d`。

## 3. 验收结果

| 范围 | 结果 | Evidence |
|---|---|---|
| Historical requirements/design traceability | PASS for legacy scope | historical 00-07 + Pattern Accepted + immutable legacy package evidence |
| S12 real-image traceability | S12A GOVERNANCE/G2 PASS / MACHINE-BOUND | active schema v2 + 00-07 + 04A + 08；S12B-F implementation/evidence NOT RUN |
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
| Desktop S8A | PASS AS SEPARATE SLICE | EXPECTED TS missing-module RED + Rust missing-function RED；2 TS files/5 + Rust 10/10 + reader 1/1 focused GREEN；218 Rust/3 ignored、49 TS files/329 tests、default/feature clippy、S7 12/12 regression、lint/build/docs/diff PASS；`bf5452f7fde24d1391845deaba17ec1135716c62` |
| Desktop S8B | PASS AS SEPARATE SLICE | missing-component/Shell-action EXPECTED RED；2 files/15 focused、50 files/341 full、axe/security/lint/build/docs/diff PASS；5-file components/chat scope；runtime/page visual NOT RUN；`4d0238b1906f02d319f47f5e55cdc023485ef07a` |
| S9-READINESS | PASS FOR DOCS ONLY / READY FOR S9A ONLY | four-repo read-only audit；Pattern 1.4.0；contract facts/consumer drift/exact projection/unknown/chart/save/export/lifecycle/tests/rollback frozen；Desktop docs/lint/341 tests/diff 与 yijie package/strict/YAML/lint/test/shell/diff；无业务代码/config/dependency diff |
| Desktop S9A | PASS AS SEPARATE SLICE | Rust/TS EXPECTED RED；consumer differential + ready reader + 7 native tests、2 TS files/6 tests focused GREEN；227 Rust/3 ignored、52 TS files/347 tests、clippy/lint/build/docs/diff PASS；`232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` |
| S9B-READINESS | PASS FOR DOCS ONLY / READY FOR S9B-D ONLY | package/lock/Vite/Tauri/CSP/S9A/Shell/tokens/test read-only audit；Pattern 1.5.0；exact registry/integrity/license/import/bundle/theme/adapter/lifecycle/a11y/visual/D-R rollback frozen；Desktop docs/lint/347 tests/diff PASS；无 package/lock/code/config diff |
| Desktop S9B-D | PASS AS SEPARATE SLICE | EXPECTED RED 5 missing suites；5 files/13 focused、57 files/360 full、dependency checker、lint/build/docs/diff PASS；655,731 raw/206,565 gzip-9；18-case real-browser matrix；`0a36ca7c54460d22ea6b3228832a57f05f0bde68` |
| Desktop S9B-D-CHECKER-REPAIR | PASS AS SEPARATE SLICE | root-cause regression EXPECTED RED 3/5 failed；GREEN 5/5、5 files/16、57 files/363；dependency/lint/build/docs/bundle/diff PASS；two-checker-file scope；`aec0f8a05ba7534132cbb4f46be64e333d7e9024` |
| Desktop S9B-R | PASS AS SEPARATE SLICE | missing-component/Shell/List EXPECTED RED；3 files/14 focused、59 files/373 full；dependency/lint/build/docs/bundle/diff PASS；18/18 real-browser matrix；`6bcc2a6bfb4db76398ecf5483c688475477f08ed` |
| FEAT126-DRIVER-COMPILE-GUARD-REPAIR | PASS AS SEPARATE SLICE | 67+29 dead-code EXPECTED RED；262 passed/3 ignored + four independent clippy matrix GREEN；five compile-only references；`c257fe9e31979cc3f2f426ab1cb7c11ce8781732` |
| FEAT126 guard consumer digest refresh | PASS AS SEPARATE SLICE | checker SHA mismatch EXPECTED RED；2 files/7 tests + v2/v3 checker + 59 files/373 tests GREEN；internal SHA only；`3e5a3830a34718bf7bf0632cc71fc4c4ab9ea4b7` |
| Host/Desktop S10A-LOCAL-PROFILE | PASS AS SEPARATE SLICE | Host `0debd877a4afe1bf2da8c988caeb1124d0fa7272`；Desktop `f4a3d42ad837ecdc8a8ba4198b269d4717285791`；exact keyless profile、sidecar mapping、content-free runner/full gates PASS |
| Desktop S10B-NATIVE-LIVE | PASS AS SEPARATE SLICE | Desktop `f787d70b4cfb51cde76bdce047ba630f4b7b1250`；single-v3、atomic Artifact/cursor、post-commit ACK replay、closed content-free private event、full gates PASS |
| Desktop S10C-PAGE | PASS AS SEPARATE SLICE | Desktop `86f02b4def4d07f76d66ebdafafda5a9bb75035c`；EXPECTED RED、6 files/67 focused、61 files/385 full、subscribe-first/history-v3/authority/bounded resync/four clients/axe/security/full gates PASS |
| Host/Desktop S10D-H | FAIL / PAUSED | implementation heads exist；no complete runtime smoke PASS；latest known primary class `runtime_axe_serious_critical`；exact attempt ledger must be recovered，not invented |
| S12 real-image scope/API/design | DESIGN RECORDED / IMPLEMENTATION NOT RUN | 00-07 + 04A + 08 scope/validation indexes；official MiniMax endpoint/model/response contract checked；S12 campaign used `0/5`、reserved `0`；standalone probe unqualified |
| AC contract portions | CONTRACT PASS | lifecycle/resource/ACK/report/fixtures/negative cases |
| AC Host/native foundation portions | PARTIAL PASS | S3/S4 lifecycle/resource/persistence/history/retention conformance |
| AC generic shell portion | S5 FOUNDATION PASS | monotonic/closed reducer、history/live shared store、generic accessible metadata shell |
| AC-003 image preview/save boundary | S6A NATIVE PASS / S6B COMPONENT + S10C PAGE PASS / E2E NOT RUN | native security/save boundary、ready image/lightbox/save UX 与 trusted Page wiring implemented；runtime visual pending |
| AC-004 video boundary | S7A NATIVE + S7A-REPAIR + S7B COMPONENT/RUNTIME PASS / VERTICAL PENDING | MP4 inspect/Range/save、playback-compatible lifetime、native controls/save UX 与真实 metadata/playback/seek 已验证；production vertical待 S10 |
| AC-005 file behavior | S8A NATIVE PASS / S8B COMPONENT + S10C PAGE PASS / VERTICAL NOT RUN / AC PARTIAL | current-v3 file UI/native save与 trusted Page wiring implemented；Markdown deferred/G4 blocked |
| AC-006 report behavior | CONTRACT/NATIVE/FOUNDATION/UI/S10C PAGE PASS / PRODUCTION VERTICAL NOT RUN | report projection/save、closed chart renderer 与 trusted Page wiring已通过；real Tauri vertical 留待 S10D/E，不记完整 AC PASS |
| AC type renderer/E2E portions | PARTIAL | image/video/file/report reusable components与 production Page code integration PASS；real Tauri production E2E 尚未开始 |
| Real image provider capability | STANDALONE OBSERVED / YIJIE PATH UNKNOWN | 历史 standalone `image-01` success 只证明 Key/provider 曾可用；adapter、secret handoff、Runtime compatibility、Artifact/Desktop 路径均未验证；S12 campaign used `0/5`、reserved `0` |

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
- 四种 exact-local synthetic fixtures 已存在。真实 image `provider|tool` 的需求范围已打开，但 activation 仍默认关闭，
  必须按 S12A-F 逐门禁实施；video/file/report real producer 继续关闭。
- canonical video resource 是 raw 1,642 bytes、SHA-256 `96ea070c...77dd5`、H.264 High/16×16/25fps/0.12s/
  3 frames、front `moov`/first keyframe；Host S7F 已从锁定 source 派生并复核 exact bytes，不依赖 runtime sibling。
- S7A 已实现 `yijie-artifact-video://localhost/v1/<opaque-handle>`：30min absolute/5min idle、2 handles/
  WebView、1/artifact、playback-compatible multi-request lifetime、2 reads/64MiB；identity-only 3 commands、GET/HEAD
  single Range 200/206/416、no CORS/query/body/redirect/error body，CSP 只新增精确 video scheme。S7A-REPAIR 只移除
  累计请求撤销；S7B Vue 只持有当前播放 lease 的 opaque URL，不 fetch、不持久化，并在切换/错误/卸载释放。
- S8A 已仅实现 `chat_read_artifact_file_preview_v1` 与 `chat_save_artifact_file_v1`：identity-only、SQLCipher 双次
  authority/revision/format 校验、plain/CSV/JSON bounded projection、PDF/XLSX metadata/native save-only，不新增 protocol/CSP/
  capability/dependency/migration。S8B 只在用户明确打开后将 safe projection 短暂放入组件 local state/DOM；不进入
  Pinia/history/storage/log/diagnostics/snapshot，并在关闭/错误/stale/切换/卸载后清空；search 不重新读取内容。
- Immutable v3 file output 不含 `text/markdown`；不得从 v2 turn input 偷渡或伪装为 plain。若本期要求 Markdown，
  必须重开 G2/G2A、Contracts semantic flow 与 downstream repin。
- S9A 只能从 SQLCipher canonical report 形成 closed bounded projection：request 仅 context/session/turn/artifact identity；
  双次复核 owner/state/kind/exact MIME/size/digest/revision/full schema；source 4MiB、projection 512KiB、response 1MiB、
  depth 12、nodes 100,000、sections 64；unknown optional 仅 unsupported marker，unknown required fail closed。Vue 不接收
  raw JSON、unknown payload、path/digest/href/token/error，projection 只允许在明确打开后的 component local state/DOM。
- S9A save 只允许 validated canonical report `.json`、明确用户 intent、dialog 前后双验、native atomic write 与 exact
  report-only residue validation；PDF/Markdown/image derived export 延期。S9B-D 已以精确 `echarts@6.1.0`、
  Canvas static core + Bar/Line/Pie + Grid/Tooltip/Aria 与仅 zrender 6.1.0/tslib 2.3.0 实现；最终 bundle
  `655731/206565` raw/gzip-9，满足 delta `<=716800/225280`、final `<=1372531/431860`。S9B-R 始终以
  visible accessible table 为权威；chart 禁止 arbitrary option/formatter/HTML/URL/event/dynamic module。当前契约无
  unit/data source/time range，UI 必须显示“报告未提供”而不得推断。series token 只允许
  `--yj-color-chart-series-1..8`；D 提供 pure budget helper，R 每次 open 按 section ordinal 只增强前 4 个
  eligible charts。dependency/bundle checker 与 loopback visual harness 路径/命令已在 Pattern/07 精确冻结。

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
| S8A Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `bf5452f7fde24d1391845deaba17ec1135716c62` + RED/GREEN/full gates；无 renderer/config/dependency/migration/public pin/S6/S7 drift |
| S8B Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `4d0238b1906f02d319f47f5e55cdc023485ef07a` + RED/GREEN/full gates；无 native/config/checker/page/store/dependency/public pin drift；runtime/page visual NOT RUN |
| S9 Readiness | READY FOR S9A ONLY；CANONICAL JSON SAVE ONLY；S9B WAIT/BLOCKED | 2026-08-21 | 03 §2F + Pattern 1.4.0 `b6f7401c79d5b2356bc45468f14d7fdbb17a855c`；docs only |
| S9A Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` + RED/GREEN/full gates；无 renderer/config/dependency/migration/public pin/S6-S8 drift |
| S9B Readiness (historical) | READY FOR S9B-D ONLY；ACCESSIBLE TABLE AUTHORITATIVE；S9B-R WAIT AT CAPTURE | 2026-08-21 | 03 §2G + Pattern 1.5.0 `630c3c8d55a2617499f51bd5bed263b819aaf084`；docs only；D/R later separate PASS |
| S9B-D Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `0a36ca7c54460d22ea6b3228832a57f05f0bde68` + RED/GREEN/full/dependency/bundle/real-browser evidence；无 report read/Chat/native/config/page/store/public pin drift |
| S9B-D-CHECKER-REPAIR Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `aec0f8a05ba7534132cbb4f46be64e333d7e9024` + RED/GREEN/full gates；历史 scope 固定 + immutable D protection；无 production boundary/S9B-R drift |
| S9B-R Slice | PASS OUTSIDE G3 | 2026-08-21 | Desktop `6bcc2a6bfb4db76398ecf5483c688475477f08ed` + RED/GREEN/full/dependency/bundle/18-case real-browser evidence；无 native/config/page/store/dependency/pin drift；production vertical NOT RUN |
| S10 Readiness + S9 Spec Reconciliation | HISTORICAL READY FOR S10A-LOCAL-PROFILE ONLY；DOCS PASS | 2026-08-22 | Pattern 1.6.0 `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` + four-repo read-only audit；S10A-E NOT RUN at capture，S10A later PASS |
| FEAT126 Driver Compile Guard Repair | PASS OUTSIDE G3 | 2026-08-22 | Desktop `c257fe9e31979cc3f2f426ab1cb7c11ce8781732`；compile reachability only；four independent clippy matrix |
| FEAT126 Guard Consumer Digest Refresh | PASS OUTSIDE G3 | 2026-08-22 | Desktop `3e5a3830a34718bf7bf0632cc71fc4c4ab9ea4b7`；only `mod.rs` internal readiness/runtime-gate SHA |
| S10A-LOCAL-PROFILE Slice | PASS OUTSIDE G3 | 2026-08-22 | Host `0debd877a4afe1bf2da8c988caeb1124d0fa7272` + Desktop `f4a3d42ad837ecdc8a8ba4198b269d4717285791` + post-commit content-free runner |
| S10B-NATIVE-LIVE Slice | PASS OUTSIDE G3 | 2026-08-22 | Desktop `f787d70b4cfb51cde76bdce047ba630f4b7b1250` + RED/GREEN/full gates + atomic/restart/private-event evidence；no Page/Store/Host/public wire drift |
| S10C-PAGE Slice | PASS OUTSIDE G3 | 2026-08-22 | Desktop `86f02b4def4d07f76d66ebdafafda5a9bb75035c` + RED/GREEN/full gates + subscribe-first/v3/authority/resync/Page/axe/security evidence；no native/config/dependency/public wire drift |
| S10D-H execution | FAIL / PAUSED | 2026-08-23 | Host `09d83cce...` + Desktop `997345d8...`；无一次完整 smoke PASS；用户明确暂停；不关闭 H |
| S12 real-image scope | APPROVED FOR DESIGN + MAX 5 S12 CAMPAIGN CALLS / NOT IMPLEMENTED | 2026-08-23 | fixed China `image-01`、T2I + current-turn single-person-reference I2I、Host Artifact pipeline；planned 4，S12 campaign used `0/5`、reserved `0`；standalone probe predates epoch |
| G4 Code Complete | PENDING | N/A | S10D-H 失败、S10D-V/S10E/S11、S12B-F、Markdown/full AC、E2E/full production visual/performance/独立 review 未完成 |
| G5/G6 | NOT PASSED | N/A | local-only scope has no release/deployment/production evidence |

## 6. 未验证项与已知限制

| Item | 状态 | 下一证据 |
|---|---|---|
| Host v3 route/staging/resource/synthetic producer | S3 PASS | S10 cross-process/restart walking skeleton |
| Desktop SQLCipher/native transfer/history/private IPC | S4 PASS | S10 integrated lifecycle |
| Desktop generic domain/store/shell | S5 PASS | S10 history/live integrated lifecycle + visual/performance evidence |
| S6A native image preview/save boundary | PASS | S10C Page wiring 已完成；real Tauri integrated lifecycle待 S10D |
| S6B image renderer/lightbox/zoom/save UX | COMPONENT + S10C PAGE PASS | focused/full/axe 通过；真实 Tauri visual/runtime 与 vertical lifecycle待 S10D/E |
| S7A/S7A-REPAIR native video inspect/Range/save | PASS | S10 仍需 production vertical/longer-media lifecycle evidence |
| S7B ready-video renderer/native-save UX | COMPONENT + REAL WEBVIEW MEDIA + S10C PAGE PASS | production Page wiring已完成；light/dark/1180x760/200% manual matrix与 performance待 S10D/E |
| S8A file native boundary | PASS | `bf5452f7fde24d1391845deaba17ec1135716c62` + focused/full Desktop gates；S8B 已单独完成 |
| S8B file renderer | COMPONENT + S10C PAGE PASS | `4d0238b...` + `86f02b4...`；production light-dark/1180x760/200% runtime visual NOT RUN，留待 S10D/E |
| S9A report native projection/save | PASS | `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` + EXPECTED RED/focused/full Desktop gates；S9B-R 已单独完成 |
| S9B-D dependency/theme/adapter/card | PASS | `0a36ca7c54460d22ea6b3228832a57f05f0bde68` + exact dependency/integrity/license、5/13 focused、57/360 full、bundle 与 18-case browser matrix；checker repair `aec0f8a05ba7534132cbb4f46be64e333d7e9024` 保持 production boundary immutable |
| S9B-R report renderer/chart/save UX | REUSABLE COMPONENT + REAL-BROWSER MATRIX + S10C PAGE PASS | renderer/browser matrix与 trusted production Page wiring已通过；real Tauri vertical留待 S10D/E |
| S10 production seam | S10A LOCAL PROFILE + S10B NATIVE LIVE + S10C PAGE PASS / S10D-H FAIL+PAUSED | keyless profile、single-v3、atomic cursor/Artifact、history/store/Page已闭环；H没有完整 smoke PASS；V/E 未运行 |
| synthetic local vertical slice | NOT RUN | S10 E2E/security/performance/visual |
| synthetic video playback/seek | CONTRACT + HOST S7F + DESKTOP S7A/S7A-REPAIR/S7B PASS | real Tauri WebView shell smoke metadata/playback/seek true；production Chat vertical仍待 S10D |
| MiniMax real image | S12A GOVERNANCE PASS / S12B-F NOT RUN / S12 CAMPAIGN `0/5` | 历史 standalone success 不可借作链路证据；下一步完成 Runtime compatibility、fake adapter、secure Key handoff，再按 shared campaign hard max 5 执行 S12E/F |
| real video/file/report producers | BLOCKED | per-kind authority/ownership/security design |
| release/deployment | N/A current scope | separate G5/G6 package if later requested |

## 7. 下一步与停止条件

1. `S12A` 已完成：active `feature.yaml` 已迁移到 schema v2，04A、S12A-F graph、G2V harness、真实图片 gate 与
   `INC-128-S10D-H-EMPTY-WAL` 已机器绑定；没有补造 H PASS/RCA。
2. 下一步只执行 `S12B`：形成 Runtime dynamic-tool compatibility candidate、双向 fixture、generate/breaking/semantic review
   与 exact consumer pin，完成后才可声明新范围 G2A。
3. S12A 未修改业务仓、未运行 S10D-H、未调用 MiniMax。S12B-E 依次是 Runtime compatibility contract、Host fake
   adapter、consumer repin/secure secret handoff与 bounded paid probe。S12F 前还必须在 schema v2 显式解决与 H 重叠的
   real-Tauri blocker；不得跳序、借用证据或删除 H failure ledger。
4. S10D-H 保持 FAIL/PAUSED；恢复执行需要单独 Owner 指令和迁移后的失败账本。S10D-V/S10E 仍等待 H immutable PASS。
5. 真实图片调用只有 S12E/F 可执行，`n=1`、逐次、hard max 5；timeout/outcome-unknown 不自动重试。生产 activation、
   video/file/report real producer、tag/push/publish/release 均未获批准。

## 8. 文档与交接

| Artifact | Path | Owner | 状态 |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-128-structured-chat-artifacts/` | 段成威 | active schema v2；S12A governance/G2 PASS；S12B-F pending；G2A pending/G2V blocked；S10D-H FAIL/PAUSED；campaign `0/5` |
| Desktop UI Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/14-feat-128-structured-chat-artifacts.md` | 段成威 | Accepted 1.7.0 at `8afdc996...`；historical READY FOR S10D-H ONLY；H later FAIL/PAUSED，production vertical NOT RUN |
| Contracts semantic review | `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md` | Contracts Owner | PASS |
| Temporal contract matrix | `04A-temporal-contract-matrix.md` | 段成威 | real-image lifecycle/invariants planned；conformance NOT RUN |
| Release/rollback plan | `09-release-and-rollback.md` | 段成威 | no release executed；image kill switch/budget/secret rollback planned |

正式关闭时间尚未形成。当前准确状态是：`schema v2 active; S12A governance/G2 PASS; S12B-F pending; G2A pending; G2V blocked by open H cleanup fuse and unqualified S12 harness; historical G3 only S3/S4/S5; S6-S10C + FEAT126 guard/digest separate historical PASS; S10D-H FAIL/PAUSED; campaign 0/5; production vertical NOT RUN; G4-G6 pending`。
