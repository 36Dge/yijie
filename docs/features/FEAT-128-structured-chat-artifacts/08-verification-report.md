# FEAT-128 验证证据与审查报告

> 本报告只记录实际执行或可复核结果。Owner 决策来自用户的直接指令；Codex 负责执行、核对和记录，
> 不把自身描述成独立人工 Reviewer。G2A PASS 只证明契约与 downstream exact pin 已就绪，不证明
> Host/Desktop S3/S4/S5、独立 S6A native boundary、独立 S6B image renderer、独立 S7F Host fixture conformance
>、独立 S7A Desktop native video boundary、S7A-REPAIR、S7B reusable renderer/runtime smoke、独立 S8A
> Desktop-private file native boundary、S8B reusable file renderer、S9A Desktop-private report native boundary、S9B-D chart foundation、其 checker repair 与 S9B-R reusable report renderer 以外的实现、端到端或真实 provider 能力尚不存在。
> S7F、S7A、S7A-REPAIR、S7B、S8A、S8B、S9A、S9B-D、S9B-D-CHECKER-REPAIR 与 S9B-R 已形成 immutable commits；S9-READINESS 是历史 docs-only evidence，
> S9B-READINESS/Pattern 1.5.0 也只是 docs-only evidence。S9B-R 独立通过不代表 production vertical。
> S10-READINESS/Pattern 1.6.0 是 docs-only evidence；S10A-E 均未实现，不代表 S10/G4。

## 1. 验证上下文

| Repository | Branch | Evidence commit | FEAT-128 实际范围 | 日期 |
|---|---|---|---|---|
| `yijie` | `feat/feat-128-structured-chat-artifacts` | 本文档最终提交 | G2/G2A + S3/S4/S5 G3 + S6-S9B-R separate PASS + S10 readiness docs-only；不扩 G3 | 2026-08-22 |
| `yijie-contracts` | `feat/feat-128-structured-chat-artifacts` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | S1/S2 authoritative source/generated/fixtures/review | 2026-08-20 |
| `yijie-agent-host` | `feat/feat-128-structured-chat-artifacts` | pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; S3 `4017785adb08e1114781d3d844e9a10a683fa933`; S7F `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | exact pin + local Host v3 foundation + canonical playable/seekable strict-local video conformance | 2026-08-20 |
| `yijie-desktop` | `feat/feat-128-structured-chat-artifacts` | initial Pattern `e97b2dabd724af856b4041e23b24437ec2f5dfc3`; pin `96094419d963745529ed0fa246919089e659f20d`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45`; S6 readiness `2b854b40379a207c19bf37fc5bc64266553c5df1`; S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S6B `4a8dce6a6526e37052941f6dbb921ba2486e109f`; S7 readiness `18b17d961ed5991cec55eeb230ea21d91f2fb8ec`; S7A `22b91c5a258458c87f1ac96c06bf39d1af97358f`; S7A-REPAIR `34991d8967de9aa2197ab2e8b9b49347774df7a5`; S7B `366186b601144bdc2bc87a2cef3075b74f1e8f19`; S8 readiness `4929a73a7871056d7aeca3eb0b27c682b21bfe4b`; S8A `bf5452f7fde24d1391845deaba17ec1135716c62`; S8B `4d0238b1906f02d319f47f5e55cdc023485ef07a`; S9 readiness `b6f7401c79d5b2356bc45468f14d7fdbb17a855c`; S9A `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe`; S9B readiness `630c3c8d55a2617499f51bd5bed263b819aaf084`; S9B-D `0a36ca7c54460d22ea6b3228832a57f05f0bde68`; checker repair `aec0f8a05ba7534132cbb4f46be64e333d7e9024`; S9B-R `6bcc2a6bfb4db76398ecf5483c688475477f08ed`; S10 readiness Pattern 1.6.0 `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` | exact pin + independent S6-S9B-R；S10 docs only；production Chat/Tauri vertical NOT RUN | 2026-08-22 |
| `yijie-codex` | `develop` | `0ce5902ed400866be0196886bb78f693a004d68d` | read-only Runtime authority | 2026-08-20 |

没有 tag、push、契约发布、真实 provider 调用、云资源、部署或生产流量。Host S3 与 Desktop S4 均默认
关闭；Desktop S6A/S6B 已有 image native/rendering，S7A/S7A-REPAIR/S7B 已有 video native、playback-compatible
Range lifetime、reusable renderer 与真实 WebView metadata/playback/seek smoke，但没有 production Chat page/跨进程
vertical integration；Host 没有真实 provider producer。

## 2. Gate 时间线

| Gate/Slice | 结论 | Evidence | 授权效果 |
|---|---|---|---|
| G0/G1 | PASS | 00-03、requirements/impact/risks | 进入 G2 review |
| G2/S0 | APPROVED | 03 §2A/2B、04-07、Pattern 1.0.0 Accepted | 只授权 Contracts S1/S2 |
| S1 | PASS | v3 OpenAPI/SSE/report/Proto/AsyncAPI、四 kind fixtures 与负例 | 进入 locked generation |
| S2 | PASS | `ea48fe...`、generate/lint/test/build、双 breaking、semantic review | 允许 S2P exact pin preflight |
| S2P | PASS | Host `dea84d...`、Desktop `960944...` 与两个仓库全量门禁 | 只形成 provenance/conformance，不改变业务行为 |
| G2A | APPROVED | 全部 required evidence 已通过，用户的条件授权生效 | 可按依赖启动 S3、随后 S4 |
| S3 | PASS | Host `4017785...` + full Host gates | 允许按依赖进入 S4；不开放真实 provider |
| S4 | PASS | Desktop `09220dd...` + full Desktop gates | native foundation 完成；不等于 UI/E2E 完成 |
| S5 | PASS | Desktop `7548ea8aeacfd7274f1107786ce48ddc6789cd45` + RED/GREEN focused tests + full Desktop gates | generic domain/store/shell 完成；不等于 type preview 或 E2E |
| G3 S3/S4/S5 | PASS | planned scope、tests/build/docs、diff 与 clean worktrees | G3 scope 保持不变；G4 仍 pending |
| S6-READINESS | PASS FOR DOCS ONLY | Desktop Pattern 1.1.0 + private IPC/Tauri/CSP/SQLCipher/S5 audit + Owner capture | 只授权下一编码切片 S6A；不代表实现或 G3/G4 |
| S6A | PASS AS SEPARATE SLICE | Desktop `8b99849d418a3ef226f4133128f1ac22a438f9d5` + RED/GREEN + focused/full gates + diff/clean review | native boundary 已形成；不并入 G3，不代表 renderer 或 G4 |
| S6B | PASS AS SEPARATE SLICE | Desktop `4a8dce6a6526e37052941f6dbb921ba2486e109f` + missing-component RED + 12 focused/full 308 tests + axe/build/docs/diff/scope review | reusable ready-image UI 已形成；不并入 G3，不代表 page/E2E/visual runtime 或 G4 |
| S7-READINESS (historical) | PASS FOR DOCS ONLY / READY FOR S7F ONLY | canonical/Host/Desktop audit + Pattern 1.2.0 `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` | 当时只授权 S7F；S7 chain 后续逐切片完成；不并入 G3/G4 |
| S7F | PASS AS SEPARATE SLICE | Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` + EXPECTED RED/GREEN + exact snapshot/checker/manifest/Range + full Host gates | 修复 strict-local fixture conformance；不并入 G3，不代表 Desktop video 或 G4 |
| S7A | PASS AS SEPARATE SLICE | Desktop `22b91c5a258458c87f1ac96c06bf39d1af97358f` + EXPECTED TS/Rust RED、focused GREEN、full Desktop gates、scope/diff/clean review | native video boundary 已形成；不并入 G3，不代表 renderer/playback UI/vertical 或 G4 |
| S7A-REPAIR | PASS AS SEPARATE SLICE | Desktop `34991d8967de9aa2197ab2e8b9b49347774df7a5` + request-65 RED、128-request GREEN、content-free diagnostics、real WebView 76 Range PASS | 修复 native handle lifetime；不并入 G3，不代表 G4 |
| S7B | PASS AS SEPARATE SLICE | Desktop `366186b601144bdc2bc87a2cef3075b74f1e8f19` + missing-component RED、14 focused/324 full tests、axe/build/docs、real metadata/playback/seek PASS | reusable video UI 已形成；不并入 G3，不代表 production vertical 或 G4 |
| S8-READINESS + S7-SPEC-RECONCILIATION | PASS FOR DOCS ONLY / READY FOR S8A ONLY | four-repo read-only audit + Pattern 1.3.0 `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` + Owner capture | 只授权下一编码切片 S8A；AC-005 PARTIAL；S8A/S8B 非实现 PASS，不扩 G3/G4 |
| S8A | PASS AS SEPARATE SLICE | Desktop `bf5452f7fde24d1391845deaba17ec1135716c62` + TS/Rust EXPECTED RED、focused/full GREEN、scope/diff/clean review | private bounded file preview/save boundary 已形成；不并入 G3，不代表 S8B/Markdown/full AC/G4 |
| S8B | PASS AS SEPARATE SLICE | Desktop `4d0238b1906f02d319f47f5e55cdc023485ef07a` + EXPECTED RED、15 focused/341 full tests、axe/security/build/docs/scope review | reusable ready-file UI 已形成；不并入 G3，不代表 production page/visual、Markdown/full AC/G4 |
| S9-READINESS (historical) | PASS FOR DOCS ONLY / READY FOR S9A ONLY | four-repo read-only audit + Pattern 1.4.0 `b6f7401c79d5b2356bc45468f14d7fdbb17a855c` + Owner capture | 当时只授权 S9A；不并入 G3/G4 |
| S9A | PASS AS SEPARATE SLICE | Desktop `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` + Rust/TS EXPECTED RED、focused/full GREEN、scope/diff/clean review | native report boundary 已形成；不并入 G3，不代表 S9B/vertical/full AC/G4 |
| S9B-READINESS | PASS FOR DOCS ONLY / READY FOR S9B-D ONLY | Desktop Pattern 1.5.0 `630c3c8d55a2617499f51bd5bed263b819aaf084` + package/lock/theme/S9A/UI read-only audit + Owner capture | 只解除为 exact D 边界；不是 implementation/G3/G4 PASS |
| S9B-D | PASS AS SEPARATE SLICE | Desktop `0a36ca7c54460d22ea6b3228832a57f05f0bde68` + EXPECTED RED、5 files/13 focused、dependency/bundle/full/real-browser evidence | exact dependency/theme/closed adapter/card foundation 已形成；不并入 G3，不代表 S9B-R/production vertical/G4 |
| S9B-D-CHECKER-REPAIR | PASS AS SEPARATE SLICE | Desktop `aec0f8a05ba7534132cbb4f46be64e333d7e9024` + 3-test EXPECTED RED、5/5 与 5 files/16 GREEN、full Desktop gates | 只修复 checker ownership；D production boundary 不变；不并入 G3，不代表 S9B-R/G4 |
| S9B-R | PASS AS SEPARATE SLICE | Desktop `6bcc2a6bfb4db76398ecf5483c688475477f08ed` + EXPECTED RED、3 files/14 focused、59 files/373 full、bundle/axe/security/18-case real-browser evidence | ready-report reusable renderer/chart/save UX 已形成；不并入 G3，不代表 production vertical/S10/G4 |
| S10-READINESS + S9-SPEC-RECONCILIATION | PASS FOR DOCS ONLY / READY FOR S10A-LOCAL-PROFILE ONLY | four-repo read-only audit + Pattern 1.6.0 `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` + Owner capture | 只授权 S10A；不并入 G3/G4 |
| S10A-S10E/S11 | NOT RUN | 无对应实现 diff | 必须逐切片授权与 immutable PASS |
| S12 real producers | BLOCKED | 无 provider authority/付费授权 | 保持关闭 |

## 2A. S8-READINESS 只读审计证据

| Audit | 可复核事实 | 结论 |
|---|---|---|
| Baselines/worktrees | yijie `fda9356e39b933b1f139c12cfe97d7b4c386c386`、Desktop `366186b601144bdc2bc87a2cef3075b74f1e8f19`、Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；开始时四仓 clean | PASS；无用户改动被覆盖 |
| Contracts v3 file output | closed allowlist 只有 `text/plain`、`text/csv`、`application/json`、`application/pdf`、XLSX；`text/markdown` 只在 v2 turn input | Markdown blocker confirmed；未修改 contract/pin |
| Host file data | strict-local CSV 合法但与 Contracts canonical 20-byte CSV 非 byte-equal；ACK 后 Host staging 可清除 | S8A authority 必须是 Desktop SQLCipher；不得把两套 CSV 混称同一 canonical bytes |
| Desktop authority | SQLCipher v8 已存 ready file BLOB/size/digest/owner/TTL；现有 image/video private boundary、atomic save、stable errors 与 bounded PDF/OOXML validators 可复用；尚无 file command/schema/client | `READY FOR S8A ONLY`；无需 migration/dependency/plugin/capability/CSP/protocol；只允许无行为漂移地暴露既有 document validator helper |
| Config/security | current exact image/video schemes 与 capability 保持；file preview 可直接返回 bounded safe projection | S8A config delta 必须为 0；SEC-006 窄例外按 Pattern 1.3.0 冻结 |

`04-contract-change-plan.md` 是 G2A-era public-contract plan，当前 immutable public contract 未改变；本轮授权文件
范围不含 04，因此没有越权把 Desktop-private S8 readiness 写入该历史 plan。若未来重开 Markdown/public output，
必须同时重开 04 与 G2/G2A。

## 2B. S8A 实现证据

| Boundary | 实际实现 | 结论 |
|---|---|---|
| Private IPC | new closed `chat-artifact-file-native-v1`；exact `chat_read_artifact_file_preview_v1` / `chat_save_artifact_file_v1`；request 仅 context + session/turn/artifact identity | PASS；无 URL/handle/protocol/CSP/capability/dependency/migration |
| SQLCipher authority | main WebView/current ReadSessions；owner/tenant/session/turn/artifact、ready/unexpired、kind=file、MIME、size/BLOB length/digest/local commit revision/format 前后双读校验 | PASS；preview/save 不回读 Host staging |
| Bounded preview | inline 仅 plain/CSV/JSON；1 MiB source、256 KiB projection、512 KiB response、UTF/BOM/control/bidi、line/CSV/JSON caps；结果为 inert text/cell closed union | PASS；没有 path/name/digest/href/token/bytes/base64/raw error，未写 Pinia/DOM/component/log/snapshot |
| Native save | five current-v3 MIME、1..64 MiB、canonical extension、native dialog、第二次 authority validation、0600 create-new/no-follow temp、chunk digest/fsync/atomic replace/RAII | PASS；PDF/XLSX 复用既有 exact bounded validators；Vue 只收 content-free outcome |
| Residue cleanup | exact file-only prefix/media marker/prior process epoch；只清除 regular non-symlink/current uid/0600/nlink=1/size/format 全通过的条目 | PASS；S6/S7 prefix、commands、limits 与行为未变 |
| Contract impact | consumer checkers only refresh Desktop implementation/readiness SHA | PASS；Contracts `ea48fe...`、source SHA、fixture trees、version、operation/schema 与 Host 不变 |

## 2C. S8B 实现证据

| Boundary | 实际实现 | 结论 |
|---|---|---|
| Eligibility/intent | 仅 `kind=file && status=ready`；preview/save 都由用户明确 click/keyboard intent 触发；其它 kind/status 保持 S5 shell | PASS；无自动 content read、无 production page integration |
| Safe render/fallback | plain/JSON 为 inert `<pre>` text nodes；CSV 为 accessible text-only table；PDF/XLSX 只显示 metadata/save-only fallback | PASS；无 `v-html`、linkification、formula/macro/code/network、browser download 或 Office/PDF renderer |
| Bounded search | 只搜索当前 S8A projection；case-sensitive literal/no-regex；query <=128 Unicode scalars；最多 100 hits；truncated 显示截断区未搜索 | PASS；highlight 仅 Vue text nodes/`mark`，不重新读取文件 |
| Data lifecycle | projection/query/matches 只在组件 local state/打开态 DOM；close/error/stale、status/artifact/session/context switch 与 unmount 清空 | PASS；授权 marker close 后 zero-hit；无 Pinia/history/router/storage/log/diagnostics/telemetry/snapshot |
| Native save UX | 只调用既有 `ChatArtifactFileNativeClient.saveFile`；dedupe；仅显示 saved/cancelled/failed 稳定 content-free 文案 | PASS；无 requestId/path/name/digest/body/raw native error |
| Scope/contract impact | 5 个 `src/components/chat` 文件；消费 immutable S8A typed client | PASS；无 src-tauri、S8A schema/commands/parser/validator/save、page/store/config/checker/dependency/lockfile/Contracts/Host/pin drift |

## 2D. S9-READINESS 只读审计证据

| Audit | 可复核事实 | 结论 |
|---|---|---|
| Baselines/worktrees | yijie `9f3a80c9a0269d835ce44550f0be6ba7b987d5d5`、Desktop `4d0238b1906f02d319f47f5e55cdc023485ef07a`、Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；开始时四仓 clean | PASS；无用户改动被覆盖 |
| Contracts report v1 | exact MIME `application/vnd.yijie.report+json;version=1`；closed root/envelope；known summary/metrics/paragraph/table/chart/callout；unknown optional payload<=131,072B/depth<=8，unknown required invalid；canonical valid/unknown/injection fixtures | Authority frozen；Contracts/Host/pin/public wire 未修改 |
| Host report data | strict-local producer 使用独立 inline schema-valid report，不与 Contracts canonical bytes 等同；通用 owner-only staging/resource/size/digest 行为适用 | 不阻塞 S9A；Desktop SQLCipher 是 ACK 后长期 authority，不得回读 Host 或把 Host fixture冒充 canonical |
| Desktop authority/private IPC | 当时 SQLCipher 已持有 ready report BLOB/size/digest/revision，history/private IPC metadata-only，尚无 report private schema/commands/typed projection/client/renderer | 历史审计据此拆 S9A/S9B；S9A 后续已独立完成 |
| Consumer conformance | 当时 Rust adapter 用 UTF-8 byte length 实现 schema maxLength、只接受 `Z` date-time，并额外要求 section ID/column key unique 与 chart labels/values aligned；immutable Ajv 接受对应 differential fixtures | 历史 blocker；S9A 已修复且保留 closed schema/integrity fail-closed |
| Config/dependency | 当前只有 exact image/video schemes，capability minimal；active package/lock 无 ECharts/vue-echarts，也无易界 ECharts theme/card | S9A config/dependency delta 必须为 0；S9B blocked，readiness 不得安装依赖 |
| Save/export | S8A atomic save kernel可复用；没有 report derived exporter | S9A 只允许 validated canonical `.json` native save；PDF/Markdown/image export 延期 |

readiness docs-only `contract-impact=none`。其历史计划判断 S9A highest impact 是 Desktop consumer `semantic` conformance repair +
Desktop-private additive schema/commands；S9A 后续按该边界完成，public Contracts/Host/pins 保持不变。Pattern 1.4.0 冻结 exact limits、
unknown omission、fixed chart mapping、save/residue、stop/rollback 与 Owner 结论；当前 S9A separate PASS，S9B `NOT RUN`。

## 2E. S9A 实现证据

| Boundary | 实际实现 | 结论 |
|---|---|---|
| Consumer conformance | maxLength 按 Unicode scalar；接受合法 RFC3339 offset/任意合法 fraction；移除非契约 section-id/column-key uniqueness 与 chart alignment 拒绝 | PASS；immutable valid differential accepted，closed schema/unknown-required/integrity仍 fail closed |
| Private IPC | new closed `chat-artifact-report-native-v1`；exact preview/save two commands；request 只含 context + session/turn/artifact identity | PASS；无 protocol/CSP/capability/dependency/migration |
| SQLCipher/projection | main WebView/current ReadSessions；owner/state/kind/exact MIME/size/BLOB/digest/revision/full schema 双验；4MiB source/512KiB projection/1MiB response；unknown optional 只投影 unsupported marker | PASS；raw JSON/unknown payload/path/digest/href/token/error 不进 Vue |
| Canonical save | validated report JSON 1..64MiB；native dialog 前后双验；0600 create-new/no-follow、digest/fsync/atomic replace/RAII；report-only verified prior-epoch cleanup | PASS；Vue 只接收 content-free saved/cancelled/failed；无 derived export |
| Scope/contract impact | 16 个允许文件；consumer lock/checker 仅刷新 Desktop implementation/readiness SHA | PASS；Contracts/Host/public pin、components/pages/stores/config/dependency/S6-S8 unchanged |

## 2F. S9B-READINESS 只读审计证据

| Audit | 可复核事实 | 结论 |
|---|---|---|
| Baselines/worktrees | yijie `9c27f0a917be09330fc56debecf97f137f987897`、Desktop `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe`、Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；开始时四仓 clean | PASS；无用户改动被覆盖 |
| Existing UI/S9A | Shell/List 只挂 image/video/file，report 仍 generic shell；S9A exact typed client/closed projection union 已存在；S8B 提供 explicit-open/epoch/stale/clear/focus/save 模式 | S9B-R 可在无 native/page/store 变更下后续实现；本轮不接入 |
| Dependency/config | active package/lock 无 ECharts/vue-echarts；active `echarts-theme.ts`/`YjChartCard` 不存在；Vite 无 CDN/external，Tauri/CSP 无 chart 需求 | exact bundled ECharts 不需 Tauri/CSP/capability delta；应先独立 S9B-D |
| Registry/license | 2026-08-21 read-only registry audit；`echarts@6.1.0` Apache-2.0 integrity `sha512-q0yaFPggC9FUdsWH4blavRWFmxdrIodbkoKNAjJudAI6CA9gNPxHtV2RcZNEepZVlk4yvBYkOkbk6HIVpIyHZA==`；transitives exact zrender 6.1.0 BSD-3-Clause + tslib 2.3.0 0BSD；ECharts tar 含 NOTICE | direct exact dependency candidate PASS；`vue-echarts@8.1.0` 因额外 generic surface/supply chain 被拒绝；本轮未安装 |
| Imports/renderer | 只需 core init/use + Bar/Line/Pie + Grid/Tooltip/Aria + Canvas；HTML legend/table 可避免 generic Legend/option 表面 | 静态 tree-shaken Canvas 方案冻结；full/root/vue-echarts/SVG/dynamic/CDN/event/formatter 全禁止 |
| Bundle baseline | 同环境 `pnpm build` 后全部 `dist/assets/*.js`=`655731` minified raw / `206580` gzip-9 bytes | S9B-D/runtime 与 S9B-R final 均受 delta `716800/225280`、final `1372531/431860` gate；这是停止阈值，不是候选包已实测通过 |
| Projection gap | chart 只有 title/type/labels/series，root 只有 generatedAt/sourceTime，无 unit/data source/time range | UI 必须显示“报告未提供”，非空 sourceTime 只标“数据时间”；不得推断 |
| Adapter/theme/a11y | Pattern 1.5.0 冻结 `--yj-color-chart-series-1..8` exact tokens、Canvas/richText/ARIA/decal/HTML legend/table、bar/line 64×8/512、pie 32/one non-negative non-zero、R 每次 open 按 ordinal 取前 4 eligible/<=2048、dispose 顺序、exact checker 路径/命令与 visual matrix | `READY FOR S9B-D ONLY`；table 权威；S9B-R waits；model/option 禁止值 snapshot，改用结构断言 |

Pattern 1.5.0 为 docs-only commit `630c3c8d55a2617499f51bd5bed263b819aaf084`；readiness 当时 Desktop 只改该
Pattern，没有 package/lock/code/config diff。Product/Technical/Security/Data 当时结论为 `READY FOR S9B-D ONLY`；
S9B-D/S9B-R 当时均 `NOT RUN`，G3/G4 不变；两者后续分别在独立授权下通过，见 2G/2I/第 4 节证据。

## 2G. S9B-D 实现证据

| Boundary | 实际实现 | 结论 |
|---|---|---|
| Dependency/supply chain | exact `echarts@6.1.0`；lock 只增加 `echarts@6.1.0`、`zrender@6.1.0`、`tslib@2.3.0`；根 NOTICE 记录 exact license/source/integrity；static core/charts/Grid/Tooltip/Aria/Canvas imports | PASS；dependency checker 验证无额外 package/install-script/full/root/vue-echarts/dynamic/CDN import |
| Theme/adapter/budget | exact 8 个 light/dark semantic series tokens；computed-token theme；closed deeply frozen bar/line/pie model；complete visible fallback table；pure ordinal-first-4/2,048-point budget | PASS；只接收 closed chart TypeScript union/合成测试输入，不读 S9A client 或真实 report，不输出 generic ECharts option |
| Accessible card/lifecycle | one Canvas instance；animation false、aria/decal、rich-text confined tooltip、HTML legend、always-visible table；theme/error/unmount clear/dispose/disconnect | PASS；component/axe/reduced-motion/no-network/storage/log tests与 18-case real-browser matrix通过 |
| Bundle/scope | 17 JS assets=655,731 raw / 206,565 gzip-9；exact 18-file allowlist | PASS；delta 0/-15；无 `components/chat`、native/config/pages/stores/Contracts/Host/pin/checker drift |

S9B-D local atomic commit 为 `0a36ca7c54460d22ea6b3228832a57f05f0bde68`，未 push。该提交形成时 production Chat/Tauri
report vertical 与 S9B-R 均 `NOT RUN`；S9B-R 后续在独立授权下完成，见 2I，G3 仍只包含 S3/S4/S5，G4 pending。

## 2H. S9B-D-CHECKER-REPAIR 实现证据

| Boundary | 实际修复 | 结论 |
|---|---|---|
| Root cause | 旧 checker 把 readiness baseline `630c3c8…` 到当前工作树的全部 diff 当成 S9B-D scope | CONFIRMED；合法后续 `src/components/chat/ChatArtifactReport.vue` 会被误报为 forbidden |
| Historical audit | 固定比较 `630c3c8d55a2617499f51bd5bed263b819aaf084` → `0a36ca7c54460d22ea6b3228832a57f05f0bde68` | PASS；历史 S9B-D diff 仍只能包含原 allowlist/visual prefix |
| Current audit | 相对 immutable S9B-D commit 只保护 package/lock/NOTICE/tokens/theme/adapter/card/bundle-checker/visual-harness | PASS；任一 protected file 变化 fail closed；无关后续 slice 由自身 diff audit 负责 |
| Assertions/scope | exact ECharts/transitives/integrity/license/NOTICE/install-script/static-import 断言原样保留；只改 dependency checker 与同名 test | PASS；S9B-D production boundary、S9A、Chat/native/config/Contracts/Host/pin 均未改 |

EXPECTED RED：新增回归后 focused command exit 1，1 file/5 tests 中 3 failed、2 passed，三个失败均因新 scope
validator 尚不存在。GREEN：1 file/5 tests 与扩展 5 files/16 tests 均 PASS；完整 `pnpm test` 为 57 files/363 tests。
Desktop 原子提交为 `aec0f8a05ba7534132cbb4f46be64e333d7e9024`，未 push。S9B-D 保持独立 PASS，
该提交形成时 S9B-R 保持 `WAIT / NOT RUN`；S9B-R 后续在独立授权下完成，G3/G4 不变。

## 2I. S9B-R 实现证据

| Boundary | 实际实现/验证 | 结论 |
|---|---|---|
| Scope | `ChatArtifactReport.vue/test`、Shell/List typed report client 透传与 `tests/visual/feat-128-s9b-r/**` | PASS；10 个允许文件；S9A/S9B-D/native/config/pages/stores/dependency/pin 无变更 |
| Explicit projection | 只在用户点击后调用既有 S9A client；known sections 为 inert text；unknown 固定 marker；ordinal key；unit/source/time-range 不推断 | PASS；authorized projection 仅在 component-local/open DOM；close/stale/context/status/unmount 清空 |
| Chart/save | immutable closed adapter/YjChartCard；每 open 前 4 eligible/≤2,048 points；visible table authority；canonical JSON native save only | PASS；mismatch/budget/init error 单 section 回落；无 derived export/arbitrary option/HTML/event/network |
| Test first | 初次 focused 缺少 component 与 Shell/List action | EXPECTED RED exit 1；report suite 0 test，Shell/List 各 1 failed，既有 Shell 4 passed |
| Focused/full | focused 3 files/14；full 59 files/373；axe/security/source/lifecycle | PASS；save close single-flight、stale、focus return、authorized marker zero-hit 均覆盖 |
| Bundle | 17 JS assets；655,731 raw / 206,565 gzip-9；S9A baseline 655,731/206,580 | PASS；delta 0/-15；低于 delta/final thresholds |
| Real browser | full-known、truncated+unknown、chart-fallback/error × light/dark × 1180/720/590 = 18 cases | 18/18 PASS；无 page overflow/clipping/overlap/unknown-id/external DOM resource；tooltip/theme recovery/local table scroll/focus/close cleanup/0 console error verified |

Desktop 原子提交为 `6bcc2a6bfb4db76398ecf5483c688475477f08ed`，未 push。`contract-impact = none`：
本切片只消费 immutable S9A Desktop-private typed client 与 S9B-D provider-neutral closed model，没有改变跨进程、
跨仓、持久化或 replay 行为。production Chat page + real Tauri report vertical 仍 `NOT RUN`，留待 S10；S9B-R
只记 separate PASS，不并入 G3，G4 pending。

## 2J. S10-READINESS 只读审计证据

| Audit | 可复核事实 | 结论 |
|---|---|---|
| Baselines/worktrees | yijie `b8c1cbc9669c86266e59d8fb3c41b0be68b1f838`、Desktop `6bcc2a6bfb4db76398ecf5483c688475477f08ed`、Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；开始时四仓 clean | PASS；无用户改动被覆盖 |
| Host executable route | FEAT-128 synthetic 在 StartSession/Turn Runtime 成功后才发布；Host 当前拒绝 synthetic 与 MiniMax/fake Responses 共存 | standalone synthetic 无法驱动真实 Host；选择 exact FEAT126 loopback fake combination，不启真实 provider |
| Host v3 order | v3 hub 同时接收普通 v1/v2-compatible events 与 Artifact events；v3 SSE 有独立 stream/sequence cursor | 必须 single v3，禁止无同步 v2+v3 双流 |
| Desktop native seam | HostBridge/Application 只开 v2；v3 decoder/ArtifactTransferService 无生产调用；Artifact state 与 turn cursor 独立写 | S10B 必须 atomic event apply+cursor；不能弱化 monotonic replay |
| Desktop UI seam | `chat_load_history_v3`/parser存在，但 ChatClient/ChatStore用v2；ArtifactStore无authority reset；ChatPage未挂List/clients | S10C 必须 subscribe-first + v3 history + epoch/reset + trusted context/turn |
| Existing harnesses | S7B runtime seeded shell；S9B visual Vite fake projection；均未挂 production ChatPage/full Host lifecycle | 不能作为 S10 vertical；S10D 必须 fresh Host + real Tauri production Chat |
| Config/dependencies | sidecar env_clear 未传 Host v3/synthetic flags；当前 CSP/capability/deps无需变化 | S10A只允许 exact mapping/test feature；S10B-E若需 CSP/capability/dependency/migration立即停止 |
| Contract impact | public Contracts/Host v3 wire/pin/canonical fixture均无需改；private content-free invalidation可 additive | readiness docs=`none`；future S10B 仅 Desktop-private additive + implementation SHA-only checker |

Desktop Pattern validation 实际结果：`pnpm docs:build`、`pnpm lint`、`pnpm test`（59 files/373 tests）和
`git diff --check` 均 exit 0；Pattern 1.6.0 单文件 commit 为
`c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2`。yijie package/strict/YAML/lint/test/shell/diff 的本轮实际结果记录在
第 4 节 `Y-S10R-*`；readiness 不是 S10 implementation PASS。

## 3. Contracts 不可变候选

| Identity | Value |
|---|---|
| Version | `0.4.0 local candidate`；未 tag、未发布 |
| Full commit | `ea48fe190e18afba728712d1e2cc79cda57f581b` |
| Host OpenAPI | `cf72ba8dd6910e8454ad60feeffa5e82583303b441dad78e49910fbdb9f5420f` |
| AsyncAPI source | `e7ea38b310d406bf09441b11ff5e8a8f2931e3b246f99c51be7d10d27ac61090` |
| Session event v3 schema | `87b1284056529bde8314e6cfa6ad1fb27ffefef50ea86033875fda795330939f` |
| Report document v1 schema | `94715e5b821cca686405d06004b805e9eac6d39dc61e19c9fc38925102f79556` |
| v3 Proto | `5021a0342b84cdea0e1dd773728e4c8f013ce7d03377ade18f06f6716a81b70d` |
| Generators | `openapi-typescript 7.13.0`; `json-schema-to-typescript 15.0.4`; `oapi-codegen v2.7.2`; `protoc-gen-es 2.12.1`; `protoc-gen-go v1.36.11` |

Semantic review 位于 `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md`。它明确审查 v1/v2
隔离、`after` cursor、ACK/poster、ordinal、closed enums、report two-stage compatibility、limits、
synthetic/real provenance 与 activation gate。

## 4. 实际命令记录

| Check ID | Repository | Command | Exit | Result | 摘要 |
|---|---|---|---:|---|---|
| Y-PACKAGE | yijie | G3 package check + strict package check | 0 | PASS | S3/S4/S5 G3 structure、template variables 与未完成标记检查通过；不代表 G4 |
| Y-YAML | yijie | unique-key parse `feature.yaml` | 0 | PASS | machine-readable G3 S3/S4/S5 record valid；G4 仍 pending |
| Y-LINT-TEST | yijie | `pnpm lint && pnpm test && bash -n scripts/*.sh` | 0 | PASS | governance + repository tests + shell syntax |
| Y-DIFF | yijie | `git diff --check` | 0 | PASS | 07/08/10/feature.yaml 无 whitespace error |
| C-GENERATE | Contracts | `pnpm generate` | 0 | PASS | locked generated outputs clean，无 warning |
| C-LINT | Contracts | `pnpm lint` | 0 | PASS | sequential post-generate check 通过 |
| C-TEST | Contracts | `pnpm test` | 0 | PASS | Node `39/39` + Go 全部通过 |
| C-BUILD | Contracts | `pnpm build` | 0 | PASS | TypeScript SDK compile 通过 |
| C-BREAK-PUB | Contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | PASS | published `contracts-v0.2.0` compatibility |
| C-BREAK-CAND | Contracts | `./scripts/check-breaking.sh 747cf740f2d91e76e5c1a130e8e009f1efa821b8` | 0 | PASS | FEAT-127 `0.3.0` candidate compatibility |
| C-EQUALITY | Contracts | v1 wire equality against both baselines | 0 | PASS | v1 unchanged；v2 source/fixture equality retained |
| C-POST-COMMIT | Contracts | `pnpm test && pnpm lint` + both breaking commands | 0 | PASS | immutable commit post-check |
| H-SYNC | Host | `make sync-contracts` | 0 | PASS | exact checkout `ea48fe...`；snapshot sync clean |
| H-CONTRACT | Host | `make contract-check` | 0 | PASS | version/full SHA/digests/generated types match |
| H-LINT | Host | `make lint` | 0 | PASS | existing + pin-only diff clean |
| H-TEST | Host | `make test` | 0 | PASS | Go/race/coverage suites pass |
| D-PIN | Desktop | `pnpm generate:check` | 0 | PASS | public/v2/v3 all pin `ea48fe...` |
| H-S3 | Host | `make contract-check && make lint && make test && make runtime-test` | 0 | PASS | v3 dual route、bounded encrypted staging、GET/HEAD/range、ACK/TTL/restart cleanup 与四类 strict-local synthetic |
| D-FOCUSED | Desktop | v3 contract checker tests | 0 | PASS | exact source/fixture + 10 implementation file pins；adapter `implemented` |
| D-LINT | Desktop | `make lint` | 0 | PASS | generate check、ESLint/vue-tsc、fmt/clippy |
| D-TEST | Desktop | `make test` | 0 | PASS | frontend `37 files / 276 tests`; Rust `184 passed, 3 ignored` |
| D-BUILD | Desktop | `make build` | 0 | PASS | application build passes |
| D-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern + S4 architecture record builds |
| D-S5-RED | Desktop | `pnpm exec vitest run src/domain/chat-artifact.test.ts src/stores/artifact.store.test.ts src/components/chat/ChatArtifactShell.test.ts` | 1 | EXPECTED RED | 3 suites 因 S5 module/component 尚不存在而失败；随后才实现 |
| D-S5-FOCUSED | Desktop | same focused Vitest command after implementation | 0 | PASS | 3 files / 19 tests；duplicate、乱序/回退、terminal、history replay、independent failure、expired、无可信百分比与 axe |
| D-S5-LINT | Desktop | `make lint` | 0 | PASS | exact Contracts pin、ESLint/vue-tsc、Rust fmt/clippy 全部通过 |
| D-S5-TEST | Desktop | `make test` | 0 | PASS | frontend `40 files / 295 tests`; Rust `184 passed, 3 ignored` |
| D-S5-BUILD | Desktop | `make build` | 0 | PASS | Vue typecheck + production Vite build |
| D-S5-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | VitePress build；Accepted Pattern 保持可构建 |
| D-S5-DIFF | Desktop | `git diff --check` + staged `git diff --cached --check` | 0 | PASS | 工作树与实际 7-file staged S5 diff 均无 whitespace error |
| D-S6R-AUDIT | Desktop | read-only audit of commands/private IPC/capabilities/CSP/SQLCipher/S5 | 0 | PASS | 现有 IPC 仅 safe metadata；无 preview/save command/protocol；既有 `rfd`/crypto/SQLCipher 足够，app-command ACL partial migration 会破坏现有 commands |
| D-S6R-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.1.0 build 通过 |
| D-S6R-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc + generated checks 通过 |
| D-S6R-TEST | Desktop | `pnpm test` | 0 | PASS | frontend `40 files / 295 tests`；readiness 无业务代码 diff |
| D-S6R-DIFF | Desktop | `git diff --check` | 0 | PASS | docs-only atomic commit `2b854b40379a207c19bf37fc5bc64266553c5df1` |
| Y-S6R-PACKAGE | yijie | G3 package check + strict package check | 0 | PASS | S6 readiness 可追踪且 G3 仍精确为 S3/S4/S5；不代表 G4 |
| Y-S6R-YAML | yijie | unique-key parse + G3/readiness assertions `feature.yaml` | 0 | PASS | unique keys；readiness docs-only；S6A/S6B pending；G4 pending |
| Y-S6R-LINT | yijie | `pnpm lint` | 0 | PASS | governance lint 通过 |
| Y-S6R-TEST | yijie | `pnpm test` | 0 | PASS | repository tests 通过 |
| Y-S6R-DIFF | yijie | `git diff --check` + staged check | 0 | PASS | readiness governance diff 无 whitespace error |
| D-S6A-RED-TS | Desktop | focused native domain/client Vitest before implementation | 1 | EXPECTED RED | 2 suites 因 `chat-artifact-native` domain/client 尚不存在而失败；随后才实现 |
| D-S6A-RED-RUST | Desktop | focused `artifact_native` Rust tests before implementation | 101 | EXPECTED RED | registry/protocol/save types and functions 尚不存在；随后才实现 |
| D-S6A-FOCUSED-TS | Desktop | `pnpm exec vitest run src/domain/chat-artifact-native.test.ts src/api/chat-artifact-native-client.test.ts` | 0 | PASS | 2 files / 6 tests；exact payload/response、opaque URL、content-free save 与 fail-closed parsing |
| D-S6A-FOCUSED-RUST | Desktop | focused `artifact_native` + SQLCipher ready-image reader tests | 0 | PASS | artifact_native 11/11；ready-image reader 1/1；owner/state/kind/MIME/size/digest/magic、handle/replay/limit/protocol/save/cleanup |
| D-S6A-PIN-RED | Desktop | initial `pnpm test` before authorized digest refresh | 1 | EXPECTED CONFORMANCE STOP | checker 检出 S6A 修改后的 Desktop implementation digests 不匹配；公共 Contracts identity 未漂移，按停止条件等待用户例外 |
| D-S6A-PIN-REFRESH | Desktop | internal consumer lock/checker digest audit | 0 | PASS | 只刷新 readiness/implementation SHA 与 checker 常量；Contracts `full_commit=ea48fe...`、source SHA、fixture、version、operation/schema、Host 均未变 |
| D-S6A-LINT | Desktop | `pnpm lint` | 0 | PASS | public contract/checker、ESLint/vue-tsc、Rust fmt/clippy 全部通过 |
| D-S6A-TEST | Desktop | `pnpm test` | 0 | PASS | frontend 42 files / 301 tests；public API/contract checks固定 `ea48fe...` |
| D-S6A-BUILD | Desktop | `make build` | 0 | PASS | production application build 通过 |
| D-S6A-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.1.0 build 通过 |
| D-S6A-DIFF | Desktop | `git diff --check` | 0 | PASS | 最终 S6A diff 无 whitespace error；scope/clean worktree 审计通过 |
| D-S6A-RUST-FULL | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml` | 0 | PASS | 196 passed / 3 existing environment tests ignored / 0 failed |
| Y-S6A-PACKAGE | yijie | `check-feature-package.sh --gate G3` + `--strict` | 0 | PASS | G3 文档范围无未完成标记；全部模板变量/未完成标记检查通过；不代表 G4 |
| Y-S6A-YAML | yijie | unique-key parse + exact G3/S6A/Contracts/G4 assertions | 0 | PASS | G3 仍为 S3/S4/S5；S6A separate PASS；Contracts `ea48fe...`；G4 pending |
| Y-S6A-LINT | yijie | `pnpm lint` | 0 | PASS | repository manifest 与 central Contract First governance 通过 |
| Y-S6A-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S6A-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | shell syntax 通过 |
| Y-S6A-DIFF | yijie | `git diff --check` | 0 | PASS | 仅 07/08/10/feature.yaml，whitespace check 通过 |
| D-S6B-RED | Desktop | `pnpm exec vitest run src/components/chat/ChatArtifactImage.test.ts` before implementation | 1 | EXPECTED RED | 新测试无法解析尚不存在的 `ChatArtifactImage.vue`；随后才实现 |
| D-S6B-FOCUSED | Desktop | `pnpm exec vitest run src/components/chat/ChatArtifactImage.test.ts src/components/chat/ChatArtifactShell.test.ts src/icons/registry.test.ts` | 0 | PASS | 3 files / 12 tests；ready-only、fresh URL、load/error/expired、release/stale、save、focus/zoom、axe/reduced-motion 与敏感数据负断言 |
| D-S6B-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc 通过；public contract/checker 仍固定 `ea48fe...` |
| D-S6B-TEST | Desktop | `pnpm test` | 0 | PASS | contract generate/check PASS；43 files / 308 tests 全通过 |
| D-S6B-BUILD | Desktop | `make build` | 0 | PASS | Vue typecheck + production Vite build 通过 |
| D-S6B-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.1.0 VitePress build 通过 |
| D-S6B-DIFF | Desktop | `git diff --check` + staged scope audit | 0 | PASS | 7-file components/chat + icon diff；无 src-tauri/contracts/checker/dependency/lockfile/page/store 差异 |
| D-S6B-VISUAL | Desktop | real Tauri light/dark/viewport/200% runtime matrix | N/A | NOT RUN | S5 list 尚未做 page/vertical wiring，本切片未获准改 pages；组件 axe/reduced-motion PASS，真实视觉证据留给 S10 |
| Y-S6B-PACKAGE | yijie | `check-feature-package.sh --gate G3` + `--strict` | 0 | PASS | G3 文档范围与全包结构/未完成标记通过；G3 仍只包含 S3/S4/S5 |
| Y-S6B-YAML | yijie | unique-key parse + exact G3/S6B/Contracts/G4 assertions | 0 | PASS | S6B full SHA/separate PASS、Contracts `ea48fe...`、G4 pending 均精确 |
| Y-S6B-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifest 与 central Contract First governance 通过 |
| Y-S6B-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S6B-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | shell syntax 通过 |
| Y-S6B-DIFF | yijie | `git diff --check` | 0 | PASS | 仅 07/08/10/feature.yaml，whitespace check 通过 |
| A-S7-CONTRACT-FIXTURE | Contracts read-only | base64 decode + `xxd` + `shasum -a 256` + `ffprobe` packet/stream audit + `ffmpeg -f framemd5` | 0 | PASS | raw 1,642 bytes；`96ea070c...77dd5`；front `ftyp/moov`；H.264 High/16×16/yuv420p/25fps/0.12s/3 frames；首 packet keyframe；3 identical generated frames |
| A-S7-HOST-FIXTURE | Host pre-S7F baseline read-only | inspect `internal/session/artifacts.go`、store media gate、HTTP Range parser/tests | 0 | FINDING | baseline `syntheticMP4()` only `ftyp/free/mdat`；无 moov/track/codec/duration/dimensions/sample/keyframe；transport-only，completed size/digest 与 canonical 不同 |
| H-S7F-RED | Host | `go test ./internal/session -run '^TestSyntheticVideoFixtureCanonicalConformance$' -count=1 -v` before implementation | 1 | EXPECTED RED | 81 vs 1642 bytes；SHA `b4bed74c...599e` vs `96ea070c...77dd5`；missing `moov` |
| H-S7F-GREEN-SESSION | Host | focused canonical identity/box/sample + lifecycle/resource tests | 0 | PASS | raw 1642 + exact SHA；front moov；H.264 High/avc1/avcC；16×16；120/1000s；3 samples；first sync sample；manifest/poster |
| H-S7F-GREEN-APP | Host | focused config + Artifact HTTP resource test | 0 | PASS | default-off/exact-local/provider isolation；video bearer/session scope；GET/HEAD 200；closed/open/suffix 206；unsatisfiable 416；multi-range 400 |
| H-S7F-SYNC | Host | `YIJIE_CONTRACTS_REF=ea48fe190e18afba728712d1e2cc79cda57f581b make sync-contracts` | 0 | PASS | pinned Git object produced byte-identical derived snapshot/lock；no generated drift |
| H-S7F-CONTRACT | Host | `make contract-check` | 0 | PASS | source path/SHA、resource tree、raw size/SHA、snapshot SHA and byte equality verified |
| H-S7F-LINT | Host | `make lint` | 0 | PASS | gofmt/vet + shell syntax |
| H-S7F-TEST | Host | `make test` | 0 | PASS | race/coverage suite passed across Host packages；contract-check rerun |
| H-S7F-RUNTIME | Host | `make runtime-test` | 0 | PASS | fixed Runtime integration passed；no model/provider call |
| H-S7F-DIFF | Host | `git diff --check` + exact 7-file allowed-scope audit | 0 | PASS | no Contracts/Desktop/public wire/dependency/provider drift |
| H-S7F-COMMIT | Host | `git commit` | 0 | PASS | atomic local commit `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；not pushed |
| Y-S7F-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S7F separate evidence accepted |
| Y-S7F-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | package templates/markers valid；当时的 S7A-S11 pending 边界明确（S7A 后续独立完成） |
| Y-S7F-YAML | yijie | unique-key parse + exact Contracts/G3/S6A/S6B/S7F/G4 assertions | 0 | PASS | S7F full SHA/separate PASS and G4 pending verified without G3 drift |
| Y-S7F-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance |
| Y-S7F-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S7F-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | shell syntax passed |
| Y-S7F-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml；no implementation/Pattern/Contracts files |
| A-S7-DESKTOP | Desktop read-only | inspect SQLCipher migration/ready reader、S6A registry/protocol/save、S6B lifecycle、Tauri config/capability/deps and local Tauri 2.11.x responder | 0 | PASS FOR DESIGN | image scheme is 30s one-shot GET/no Range；SQLCipher stores ready video+poster up to 64MiB；responder buffers body；no current video command/schema/media-src/renderer |
| D-S7R-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.2.0 Accepted build passed |
| D-S7R-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc passed；docs-only diff |
| D-S7R-TEST | Desktop | `pnpm test` | 0 | PASS | contract pins verified；43 files / 308 tests passed |
| D-S7R-DIFF | Desktop | `git diff --check` + final one-file scope audit | 0 | PASS | only Accepted Pattern changed；no fixture/code/schema/command/config/dependency/capability/pin diff |
| D-S7R-COMMIT | Desktop | `git commit` | 0 | PASS | Pattern 1.2.0 docs-only atomic commit `18b17d961ed5991cec55eeb230ea21d91f2fb8ec`；not pushed |
| Y-S7R-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 scope 无未完成标记；G3 仍只包含 S3/S4/S5；不代表 G4 |
| Y-S7R-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | 全部模板变量与未完成标记检查通过；readiness/NOT RUN 边界保留 |
| Y-S7R-YAML | yijie | unique-key parse + exact G3/S6A/S6B/S7/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6A/S6B separate PASS；S7 READY FOR S7F ONLY；G4 pending |
| Y-S7R-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests 与 central Contract First governance 通过 |
| Y-S7R-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S7R-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | 全部 shell syntax 通过 |
| Y-S7R-DIFF | yijie | `git diff --check` + exact eight-file scope audit | 0 | PASS | 仅 03/05/06/07/08/09/10/feature.yaml；无其它治理/业务文件 |
| D-S7A-RED-TS | Desktop | focused Vitest for `chat-artifact-video-native` domain/client before implementation | 1 | EXPECTED RED | 2 suites 无法解析尚不存在的 private domain/client modules |
| D-S7A-RED-RUST | Desktop | focused Rust video boundary tests before implementation | 101 | EXPECTED RED | `parse_single_range`、`RequestedRange`、`validate_mp4` 与 `VideoPreviewRegistry` 尚不存在 |
| D-S7A-GREEN-TS | Desktop | focused video domain/client Vitest | 0 | PASS | 2 files/5 tests；exact identity-only payloads、opaque URL、content-free save 与 fail-closed parsing |
| D-S7A-GREEN-RUST | Desktop | focused `artifact_video_native` + SQLCipher ready-video reader tests | 0 | PASS | 11 video boundary tests + 1 reader；MP4 inspect、scope、TTL/limits、GET/HEAD/Range 200/206/416、save/cleanup |
| D-S7A-LINT | Desktop | `pnpm lint` | 0 | PASS | public contract/checker、ESLint/vue-tsc 与 required generated checks passed |
| D-S7A-TEST | Desktop | `pnpm test` | 0 | PASS | 45 files / 313 tests；Contracts identity remains `ea48fe...` |
| D-S7A-BUILD | Desktop | `make build` | 0 | PASS | production application build passed |
| D-S7A-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.2.0 build passed |
| D-S7A-DIFF | Desktop | `git diff --check` + exact 19-file scope audit | 0 | PASS | no components/pages/stores、Contracts/Host/public pin、dependency/lockfile、capability/permission、migration or S7B drift |
| D-S7A-MAKE-LINT | Desktop | `make lint` | 0 | PASS | generate:check、ESLint/vue-tsc、Rust fmt/clippy `-D warnings` all passed |
| D-S7A-COMMIT | Desktop | `git commit` | 0 | PASS | atomic local commit `22b91c5a258458c87f1ac96c06bf39d1af97358f`; not pushed |
| Y-S7A-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S7A separate evidence accepted without G3 expansion |
| Y-S7A-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | package templates/markers valid；pending S7B-S11 remains explicit |
| Y-S7A-YAML | yijie | unique-key parse + exact Contracts/G3/S7A/G4 assertions | 0 | PASS | S7A full SHA/separate PASS、Contracts `ea48fe...` and G4 pending verified without G3 drift |
| Y-S7A-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S7A-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S7A-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S7A-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml；no implementation/Pattern/Contracts files |
| D-S7AR-RED | Desktop | focused 128-request registry lifecycle test against original S7A | 101 | EXPECTED RED | request 65 returned `NotFound` because the 64-success lifetime counter revoked the handle |
| D-S7AR-GREEN | Desktop | focused registry lifecycle + default/feature `artifact_video_native` tests | 0 | PASS | 128 sequential requests remain valid；default 11/11 and runtime-feature 12/12 PASS；TTL/release/context/WebView/restart limits retained |
| D-S7AR-CLIPPY | Desktop | default + `feat128-s7b-runtime` clippy `-D warnings` | 0 | PASS | compile-time-off diagnostics and repair are warning-free |
| D-S7AR-RUNTIME | Desktop | `./scripts/run-feat128-s7b-runtime-smoke.sh` | 0 | PASS | real Tauri WebView: metadata/playback/seek true；76 GET/Range、76 partial、65 distinct、11 repeated、zero begin failure/NotFound |
| D-S7AR-COMMIT | Desktop | selective atomic `git commit` | 0 | PASS | repair + default-off content-free runtime harness `34991d8967de9aa2197ab2e8b9b49347774df7a5`; not pushed |
| D-S7B-RED | Desktop | focused video component/runtime suites before implementation | 1 | EXPECTED RED | not-yet-created renderer/harness modules could not be resolved |
| D-S7B-GREEN | Desktop | `pnpm exec vitest run` for video component/runtime/shell | 0 | PASS | 3 files / 14 tests；ready-only、controls、metadata/error/expiry/retry、seek lease、stale/dedup、save、focus/axe/reduced-motion/sensitive-data negatives |
| D-S7B-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint/vue-tsc and generated contract checks passed |
| D-S7B-TEST | Desktop | `pnpm test` | 0 | PASS | 47 files / 324 tests；Contracts identity remains `ea48fe...` |
| D-S7B-BUILD | Desktop | `make build` | 0 | PASS | production application build passed |
| D-S7B-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.2.0 build passed |
| D-S7B-DIFF | Desktop | `git diff --check` + staged scope review | 0 | PASS | no pages/contracts/host/pins/checkers/dependencies/capability/permission/migration drift |
| D-S7B-COMMIT | Desktop | selective atomic `git commit` | 0 | PASS | renderer commit `366186b601144bdc2bc87a2cef3075b74f1e8f19`; not pushed |
| Y-S7B-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S7A-REPAIR/S7B separate evidence does not expand G3 |
| Y-S7B-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | package templates and incomplete markers valid；S8-S11/G4 pending boundary explicit |
| Y-S7B-YAML | yijie | `yaml@2.9.0` unique-key parse + exact G3/separate-slice/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B separate PASS；G4 pending |
| Y-S7B-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S7B-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S7B-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S7B-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml；no Pattern/implementation/Contracts files |
| D-S8R-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | final Pattern 1.3.0 VitePress build complete in 1.73s |
| D-S8R-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc passed；readiness changed no code/config |
| D-S8R-TEST | Desktop | `pnpm test` | 0 | PASS | Contracts/checkers fixed at `ea48fe...`；47 files / 324 tests passed |
| D-S8R-DIFF | Desktop | `git diff --check` + exact one-file scope audit | 0 | PASS | only Accepted Pattern changed；atomic local commit `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` |
| Y-S8R-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S8 readiness docs evidence does not expand it |
| Y-S8R-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | templates/markers valid；S8A/S8B NOT RUN and G4 pending remain explicit |
| Y-S8R-YAML | yijie | `yaml@2.9.0` unique-key parse + exact G3/separate-slice/S8/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6/S7 separate PASS；S8 docs-only；S8A/S8B NOT RUN；G4 pending |
| Y-S8R-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S8R-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S8R-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S8R-DIFF | yijie | `git diff --check` + exact eight-file scope audit | 0 | PASS | only allowed FEAT-128 03/05/06/07/08/09/10/feature.yaml changed |
| D-S8A-RED-TS | Desktop | focused file native domain/client Vitest before implementation | 1 | EXPECTED RED | 2 suites could not resolve the not-yet-created domain/client modules |
| D-S8A-RED-RUST | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml chat::artifact_file_native::tests` before implementation | 101 | EXPECTED RED | planned file native types/functions/module did not exist |
| D-S8A-FOCUSED-TS | Desktop | `pnpm exec vitest run src/domain/chat-artifact-file-native.test.ts src/api/chat-artifact-file-native-client.test.ts` | 0 | PASS | 2 files / 5 tests；exact two commands、identity-only schema、bounded closed projections、content-free save/error |
| D-S8A-FOCUSED-RUST | Desktop | focused `artifact_file_native` + SQLCipher ready-file lifecycle test | 0 | PASS | file boundary 10/10 + authority lifecycle 1/1；format/limits/concurrency/revision/atomic/residue/leak negatives |
| D-S8A-CLIPPY | Desktop | default and `feat128-s7b-runtime` all-target clippy with `-D warnings` | 0 | PASS | S8A and unchanged compile-time-off S7 diagnostics are warning-free |
| D-S8A-RUST-FULL | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml` | 0 | PASS | 218 passed / 3 existing environment tests ignored / 0 failed |
| D-S8A-S7-REGRESSION | Desktop | runtime-feature `chat::artifact_video_native::tests` | 0 | PASS | 12/12；S7 protocol/Range/lifecycle/save behavior unchanged |
| D-S8A-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint/vue-tsc and public/v2/v3 checkers passed；Contracts identity remains `ea48fe...` |
| D-S8A-TEST | Desktop | `pnpm test` | 0 | PASS | 49 files / 329 tests；v3 checker verified 10 Desktop implementation pins |
| D-S8A-BUILD | Desktop | `make build` | 0 | PASS | Vue typecheck + production Vite build passed |
| D-S8A-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.3.0 VitePress build passed |
| D-S8A-DIFF | Desktop | `git diff --check` + exact staged scope review | 0 | PASS | 18-file S8A allowlist；no component/page/store/config/dependency/migration/S6/S7 drift |
| D-S8A-COMMIT | Desktop | selective atomic `git commit` | 0 | PASS | `bf5452f7fde24d1391845deaba17ec1135716c62`; not pushed |
| Y-S8A-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S8A separate evidence does not expand it |
| Y-S8A-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | package templates/markers valid；S8B-S11 and G4 remain pending |
| Y-S8A-YAML | yijie | `yaml@2.9.0` unique-key parse + exact G3/separate-slice/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6/S7/S8A separate PASS；S8B NOT RUN；G4 pending |
| Y-S8A-LINT | yijie | `pnpm lint` | 0 | PASS | repository manifests + central Contract First governance passed |
| Y-S8A-TEST | yijie | `pnpm test` | 0 | PASS | repository manifest tests passed |
| Y-S8A-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S8A-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S8B-RED | Desktop | `pnpm exec vitest run src/components/chat/ChatArtifactFile.test.ts src/components/chat/ChatArtifactShell.test.ts` before implementation | 1 | EXPECTED RED | `ChatArtifactFile.vue` 尚不存在，Shell 尚无 ready-file action surface；既有 3 个 Shell tests 仍通过 |
| D-S8B-FOCUSED | Desktop | same focused command after implementation | 0 | PASS | 2 files / 15 tests；explicit open、plain/JSON/CSV、PDF/XLSX fallback、truncation、literal search caps、clear/stale/dedup/save/focus/axe/reduced-motion/security |
| D-S8B-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc；S8A/private/public contract checkers unchanged |
| D-S8B-TEST | Desktop | `pnpm test` | 0 | PASS | 50 files / 341 tests；Contracts identity remains `ea48fe...`；10 Desktop implementation pins unchanged |
| D-S8B-BUILD | Desktop | `make build` | 0 | PASS | Vue typecheck + production Vite build passed |
| D-S8B-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.3.0 VitePress build passed without Pattern edit |
| D-S8B-DIFF | Desktop | `git diff --check` + exact staged scope review | 0 | PASS | only 5 `src/components/chat` files；no native/config/checker/page/store/dependency/pin drift |
| D-S8B-COMMIT | Desktop | selective atomic `git commit` | 0 | PASS | `4d0238b1906f02d319f47f5e55cdc023485ef07a`; not pushed |
| D-S8B-VISUAL | Desktop | production Chat page + real Tauri light/dark/1180x760/200-percent visual matrix | N/A | NOT RUN | production page integration explicitly forbidden；component axe/reduced-motion PASS；deferred to S10 |
| Y-S8B-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S8B separate evidence does not expand it |
| Y-S8B-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | package templates/markers valid；S9-S11 and G4 remain pending |
| Y-S8B-YAML | yijie | `yaml@2.9.0` unique-key parse + exact G3/separate-slice/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6/S7/S8A/S8B separate PASS；G4 pending |
| Y-S8B-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S8B-TEST | yijie | `pnpm test` | 0 | PASS | repository manifest test passed |
| Y-S8B-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S8B-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S9R-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.4.0 VitePress client/server build + page render complete |
| D-S9R-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc passed；readiness changed no code/config/dependency |
| D-S9R-TEST | Desktop | `pnpm test` | 0 | PASS | public/v2/v3 checkers remain at `ea48fe...`；50 files / 341 tests passed |
| D-S9R-DIFF | Desktop | `git diff --check` + exact one-file scope audit | 0 | PASS | only Accepted Pattern changed；atomic local commit `b6f7401c79d5b2356bc45468f14d7fdbb17a855c` |
| Y-S9R-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；S9 readiness docs evidence does not expand it |
| Y-S9R-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | templates/markers valid；S9A/S9B NOT RUN and G4 pending remain explicit |
| Y-S9R-YAML | yijie | `yaml` unique-key parse + exact G3/separate-slice/S9/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6/S7/S8A/S8B separate PASS；S9 docs-only；G4 pending |
| Y-S9R-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S9R-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S9R-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9R-DIFF | yijie | `git diff --check` + exact eight-file scope audit | 0 | PASS | only allowed FEAT-128 03/05/06/07/08/09/10/feature.yaml changed |
| D-S9A-RED-RUST | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml chat::artifact::tests::report_adapter_accepts_all_schema_valid_cardinality_and_datetime_forms` before repair | 101 | EXPECTED RED | immutable-schema-valid differential fixture was rejected by the old consumer |
| D-S9A-RED-TS | Desktop | focused domain/client Vitest before implementation | 1 | EXPECTED RED | report native domain/client modules did not exist |
| D-S9A-FOCUSED-RUST | Desktop | report adapter/authority/native focused tests after implementation | 0 | PASS | consumer differential + ready reader + 7 native boundary tests passed |
| D-S9A-FOCUSED-TS | Desktop | `pnpm exec vitest run src/domain/chat-artifact-report-native.test.ts src/api/chat-artifact-report-native-client.test.ts` | 0 | PASS | 2 files / 6 tests；closed parser/client and content-free failures |
| D-S9A-RUST | Desktop | `cargo test --manifest-path src-tauri/Cargo.toml` | 0 | PASS | 227 passed / 3 ignored；0 failed |
| D-S9A-CLIPPY | Desktop | `cargo clippy --manifest-path src-tauri/Cargo.toml --all-targets -- -D warnings` | 0 | PASS | no warnings |
| D-S9A-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc + public/v2/v3 consumer checks passed |
| D-S9A-TEST | Desktop | `pnpm test` | 0 | PASS | 52 files / 347 tests；Contracts identity remains `ea48fe...` |
| D-S9A-BUILD | Desktop | `make build` | 0 | PASS | Rust/Vue production build passed |
| D-S9A-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.4.0 docs build passed unchanged |
| D-S9A-DIFF | Desktop | `git diff --check` + exact staged scope audit | 0 | PASS | 16 allowed files；no component/page/store/config/dependency/migration/public pin drift |
| D-S9A-COMMIT | Desktop | selective atomic `git commit` | 0 | PASS | `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe`; not pushed |
| Y-S9A-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S9A separate evidence does not expand it |
| Y-S9A-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | templates/markers valid；S9B-S11 and G4 remain pending |
| Y-S9A-YAML | yijie | `yaml` unique-key parse + exact G3/S9A/G4 assertions | 0 | PASS | G3=S3/S4/S5；S9A separate PASS；S9B pending；G4 pending |
| Y-S9A-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S9A-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S9A-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9A-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S9BREADY-BUNDLE-BASE | Desktop | `pnpm build` + Node gzip-9 aggregate of all `dist/assets/*.js` | 0 | PASS | S9A baseline 17 JS files；655,731 raw / 206,580 gzip-9 bytes；只记基线，未安装/测量 ECharts candidate |
| D-S9BREADY-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.5.0 VitePress client/server build + page render complete |
| D-S9BREADY-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc；readiness changed no code/config/dependency |
| D-S9BREADY-TEST | Desktop | `pnpm test` | 0 | PASS | 52 files / 347 tests；public/v2/v3 checkers remain at `ea48fe...` |
| D-S9BREADY-DIFF | Desktop | `git diff --check` + exact one-file scope audit | 0 | PASS | only Accepted Pattern changed |
| D-S9BREADY-COMMIT | Desktop | selective atomic local commit | 0 | PASS | `630c3c8d55a2617499f51bd5bed263b819aaf084`; not pushed |
| Y-S9BREADY-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S9B readiness docs do not expand it |
| Y-S9BREADY-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | package templates/markers valid；S9B-D/R NOT RUN and G4 pending |
| Y-S9BREADY-YAML | yijie | unique-key YAML parse + exact G3/separate/readiness/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6-S9A separate PASS；S9B readiness docs-only；D READY/NOT RUN；R WAIT/NOT RUN；G4 pending |
| Y-S9BREADY-LINT | yijie | `pnpm lint` | 0 | PASS | repository manifests + central Contract First governance passed |
| Y-S9BREADY-TEST | yijie | `pnpm test` | 0 | PASS | repository manifest test passed |
| Y-S9BREADY-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9BREADY-DIFF | yijie | `git diff --check` + exact eight-file scope audit | 0 | PASS | only authorized FEAT-128 03/05/06/07/08/09/10/feature.yaml changed |
| D-S9BD-RED | Desktop | exact 5-suite focused Vitest before implementation | 1 | EXPECTED RED | dependency checker、bundle checker、theme、adapter/card modules did not exist；无既有回归 |
| D-S9BD-FOCUSED | Desktop | exact §20 focused Vitest | 0 | PASS | 5 files / 13 tests；dependency/bundle checker、light/dark theme、closed adapter/budget、card lifecycle/a11y |
| D-S9BD-DEPS | Desktop | `node scripts/check-feat128-s9b-d-dependencies.mjs` | 0 | PASS | exact ECharts 6.1.0 + zrender 6.1.0 + tslib 2.3.0、integrity/license/NOTICE/import allowlist 与 18-file scope通过 |
| D-S9BD-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint、vue-tsc 与 public/v2/v3 consumer checkers通过；Contracts pin unchanged |
| D-S9BD-TEST | Desktop | `pnpm test` | 0 | PASS | 57 files / 360 tests；无 `.skip`/`.only` 或既有回归 |
| D-S9BD-BUILD | Desktop | `make build` | 0 | PASS | Rust/Vue production build通过；无 native/config drift |
| D-S9BD-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.5.0 docs build通过 |
| D-S9BD-BUNDLE | Desktop | `node scripts/check-feat128-s9b-d-bundle.mjs --dist dist/assets` | 0 | PASS | 17 JS files；655,731 raw / 206,565 gzip-9；delta 0/-15；低于冻结 delta/final budgets |
| D-S9BD-VISUAL | Desktop | loopback Vite harness + real in-app browser matrix | 0 | PASS | full/fallback/error × light/dark × 1180×760/720×760/590×760=18 cases；无 page/card overflow；280/180px；table/focus/tooltip/theme re-init/零 console/network通过 |
| D-S9BD-DIFF | Desktop | `git diff --check` + exact staged scope audit | 0 | PASS | only 18 authorized dependency/notice/theme/adapter/card/checker/test-harness files；无 chat/native/config/page/store/pin漂移 |
| D-S9BD-COMMIT | Desktop | selective atomic local commit | 0 | PASS | `0a36ca7c54460d22ea6b3228832a57f05f0bde68`; not pushed |
| Y-S9BD-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S9B-D separate evidence does not expand it |
| Y-S9BD-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | templates/markers valid；S9B-R/S10-S11 and G4 remain pending |
| Y-S9BD-YAML | yijie | `yaml` unique-key parse + exact G3/S9B-D/S9B-R/G4 assertions | 0 | PASS | G3=S3/S4/S5；S9B-D separate PASS；S9B-R WAIT/NOT RUN；G4 pending |
| Y-S9BD-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S9BD-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S9BD-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9BD-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S9BDC-RED | Desktop | `pnpm exec vitest run scripts/check-feat128-s9b-d-dependencies.test.mjs` after tests only | 1 | EXPECTED RED | 1 file/5 tests；3 failed/2 passed because two-stage scope validators did not exist |
| D-S9BDC-GREEN | Desktop | same focused command after repair | 0 | PASS | 1 file/5 tests；legal synthetic `components/chat` accepted；protected/current + forbidden/historical cases fail closed |
| D-S9BDC-FOCUSED | Desktop | dependency+bundle+theme+adapter+card exact focused command | 0 | PASS | 5 files/16 tests |
| D-S9BDC-DEPS | Desktop | `node scripts/check-feat128-s9b-d-dependencies.mjs` | 0 | PASS | historical `630c3c8…→0a36ca7…` scope + immutable D protection + unchanged dependency assertions |
| D-S9BDC-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc；no contract/pin drift |
| D-S9BDC-TEST | Desktop | `pnpm test` | 0 | PASS | 57 files/363 tests；public/v2/v3 checkers and 10 implementation pins remain PASS |
| D-S9BDC-BUILD | Desktop | `make build` | 0 | PASS | Vue production build；no code/config expansion |
| D-S9BDC-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.5.0 unchanged and buildable |
| D-S9BDC-BUNDLE | Desktop | `node scripts/check-feat128-s9b-d-bundle.mjs --dist dist/assets` | 0 | PASS | 17 assets；655,731 raw/206,565 gzip-9；delta 0/-15 |
| D-S9BDC-DIFF | Desktop | `git diff --check` + staged exact two-file audit | 0 | PASS | only dependency checker + same-name test；all protected D files unchanged |
| D-S9BDC-COMMIT | Desktop | selective atomic local commit + post-commit checker | 0 | PASS | `aec0f8a05ba7534132cbb4f46be64e333d7e9024`; clean；not pushed |
| Y-S9BDC-PACKAGE | yijie | `check-feature-package.sh --gate G3` | 0 | PASS | G3 remains exact S3/S4/S5；checker repair separate evidence does not expand it |
| Y-S9BDC-STRICT | yijie | `check-feature-package.sh --strict` | 0 | PASS | templates/markers valid；S9B-R/S10-S11 and G4 remain pending |
| Y-S9BDC-YAML | yijie | unique-key parse + exact G3/repair/S9B-R/G4 assertions | 0 | PASS | repair full SHA/separate PASS、S9B-R WAIT/NOT RUN、G4 pending |
| Y-S9BDC-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S9BDC-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S9BDC-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9BDC-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S9BR-RED | Desktop | focused command after tests only | 1 | EXPECTED RED | report component missing；report suite 0 tests；Shell/List each 1 failed；existing Shell 4 passed |
| D-S9BR-FOCUSED | Desktop | `pnpm exec vitest run src/components/chat/ChatArtifactReport.test.ts src/components/chat/ChatArtifactShell.test.ts src/components/chat/ChatArtifactList.test.ts` | 0 | PASS | 3 files/14 tests；explicit projection、all sections、ordinal/budget/fallback、stale/clear/save/focus/axe/security |
| D-S9BR-DEPS | Desktop | `node scripts/check-feat128-s9b-d-dependencies.mjs` | 0 | PASS | immutable S9B-D protected files and exact dependency assertions unchanged；legal downstream Chat files accepted |
| D-S9BR-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint + vue-tsc；no native/schema/pin drift |
| D-S9BR-TEST | Desktop | `pnpm test` | 0 | PASS | 59 files/373 tests；public/v2/v3 consumer checkers and 10 implementation pins remain PASS |
| D-S9BR-BUILD | Desktop | `make build` | 0 | PASS | Vue production build；no config/page/store integration |
| D-S9BR-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Accepted Pattern 1.5.0 unchanged and buildable |
| D-S9BR-BUNDLE | Desktop | `node scripts/check-feat128-s9b-d-bundle.mjs --dist dist/assets` | 0 | PASS | 17 assets；655,731 raw/206,565 gzip-9；S9A delta 0/-15；all budgets PASS |
| D-S9BR-VISUAL | Desktop | loopback `127.0.0.1:41784` + real in-app browser | 0 | PASS | 18/18 full/truncated/fallback-error × light/dark × 1180/720/590；overflow/clipping/overlap/console/external=0；tooltip/theme/focus/close cleanup PASS |
| D-S9BR-DIFF | Desktop | `git diff --check` + staged 10-file scope audit | 0 | PASS | only ChatArtifactReport/Shell/List tests/components + S9B-R test-only visual harness |
| D-S9BR-COMMIT | Desktop | selective atomic local commit | 0 | PASS | `6bcc2a6bfb4db76398ecf5483c688475477f08ed`; clean；not pushed |
| Y-S9BR-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S9B-R separate evidence does not expand it |
| Y-S9BR-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | package templates/markers valid；S10-S11 and G4 remain pending |
| Y-S9BR-YAML | yijie | unique-key YAML parse + exact G3/separate/readiness/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6-S9B-R separate PASS；S9B readiness docs-only；G4 pending |
| Y-S9BR-LINT | yijie | `pnpm lint` | 0 | PASS | 10 repository manifests + central Contract First governance passed |
| Y-S9BR-TEST | yijie | `pnpm test` | 0 | PASS | 1/1 repository manifest test passed |
| Y-S9BR-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S9BR-DIFF | yijie | `git diff --check` + exact four-file scope audit | 0 | PASS | only 07/08/10/feature.yaml changed |
| D-S10R-DOCS | Desktop | `pnpm docs:build` | 0 | PASS | Pattern 1.6.0 built successfully |
| D-S10R-LINT | Desktop | `pnpm lint` | 0 | PASS | ESLint/vue-tsc passed；no runtime source changed |
| D-S10R-TEST | Desktop | `pnpm test` | 0 | PASS | 59 files/373 tests；all public/v2/v3/checker gates passed |
| D-S10R-DIFF | Desktop | `git diff --check` + single-file scope audit | 0 | PASS | only Accepted Pattern changed |
| D-S10R-COMMIT | Desktop | local atomic docs commit | 0 | PASS | `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2`; clean；not pushed |
| Y-S10R-PACKAGE | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G3 docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | G3 remains exact S3/S4/S5；S10 readiness docs-only |
| Y-S10R-STRICT | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-128-structured-chat-artifacts` | 0 | PASS | package structure/markers valid；S10A-E/G4 pending |
| Y-S10R-YAML | yijie | unique-key parse + exact G3/separate/S10/G4 assertions | 0 | PASS | G3=S3/S4/S5；S6-S9B-R separate PASS；S10 readiness docs-only；A-E NOT RUN；G4 pending |
| Y-S10R-LINT | yijie | `pnpm lint` | 0 | PASS | repository manifests + central governance passed |
| Y-S10R-TEST | yijie | `pnpm test` | 0 | PASS | repository manifest test passed |
| Y-S10R-SHELL | yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS | all shell syntax passed |
| Y-S10R-DIFF | yijie | `git diff --check` + exact eight-file scope audit | 0 | PASS | only authorized FEAT 03/05/06/07/08/09/10/feature.yaml changed |

一次 `pnpm lint` 曾与 `pnpm test` 并行执行，因仓库 `check-generated` 临时替换 generated 目录而产生
瞬时失败；改为仓库要求的顺序执行后通过，且 immutable commit 上再次通过。它是命令并发冲突，
不是产品或契约失败。

S6A 另有一次实现期 `pnpm lint` 因新测试 mock 的 tuple 签名错误退出 2；修正测试类型后重跑通过。
`D-S6A-PIN-RED` 则是 checker 正确执行 fail-closed：用户随后明确批准最小例外，才刷新 Desktop 内部
consumer implementation/readiness digests。该例外不改变公共 Contracts pin 或 wire/schema 语义。

S6B 实现期 focused 测试曾先暴露 3 个问题（空节点断言、Naive focus sentinel、axe `aria-hidden-focus`），随后改为
明确的 dialog Tab 约束与焦点归还并通过。`pnpm lint` 也先后检出 unused helper（exit 1）和测试 mock/nullable
类型（exit 2）；修正后按用户要求从头串行执行五条最终命令，全部 exit 0。上述迭代均未修改 native boundary。

S8A 实现期一次 `pnpm lint` 因新增 client test mock 的可选 argument tuple 签名不兼容而 exit 2；修正测试类型后，
focused Rust/TS、default/feature clippy、full Rust 与用户指定五条 Desktop 命令均从头串行重跑并 exit 0。最终审计又补齐
SQLCipher `local_committed_at` revision 的双读比较，随后再次完整重跑上述门禁；没有扩大实现范围。

## 5. Downstream pin 证据

| Consumer | Pin commit | Pin 内容 | 结论 |
|---|---|---|---|
| Agent Host | pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; S3 `4017785adb08e1114781d3d844e9a10a683fa933`; S7F `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | Contracts `0.4.0` identities + v3 snapshots/types + canonical resource path/source SHA/tree/raw/snapshot conformance；`EXC-128-001` | S2P/S3 PASS；S7F separate PASS |
| Desktop | pin `96094419d963745529ed0fa246919089e659f20d`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983`; S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45`; S6 readiness `2b854b40379a207c19bf37fc5bc64266553c5df1`; S6A `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S6B `4a8dce6a6526e37052941f6dbb921ba2486e109f`; S7 readiness `18b17d961ed5991cec55eeb230ea21d91f2fb8ec`; S7A `22b91c5a258458c87f1ac96c06bf39d1af97358f`; S7A-REPAIR `34991d8967de9aa2197ab2e8b9b49347774df7a5`; S7B `366186b601144bdc2bc87a2cef3075b74f1e8f19`; S8 readiness `4929a73a7871056d7aeca3eb0b27c682b21bfe4b`; S8A `bf5452f7fde24d1391845deaba17ec1135716c62`; S8B `4d0238b1906f02d319f47f5e55cdc023485ef07a`; S9 readiness `b6f7401c79d5b2356bc45468f14d7fdbb17a855c`; S9A `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe`; S9B-D `0a36ca7c54460d22ea6b3228832a57f05f0bde68`; checker repair `aec0f8a05ba7534132cbb4f46be64e333d7e9024`; S9B-R `6bcc2a6bfb4db76398ecf5483c688475477f08ed`; S10 Pattern `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` | Contracts source/fixture identities unchanged；S8A/S9A only SHA repair；S9B/S10 Pattern 无 public pin diff | S2P/S4/S5 PASS；S6-S9B-R separate PASS；S10 readiness docs PASS |

Desktop fixture Git tree OIDs：event v3 `21de31ceb65900bcf38bc7fe171de8238dfa30dc`、resources
`f447129c08b9b39231e33698afc3f2fd875d6b14`、Host v3
`8afbe7e88cc89401d9990e08b4b332096b53934e`、report
`3fafff6d702504f7a8a1cd44b4c717f024c88ae8`。

S6A 最终 Desktop implementation digests：`artifact.rs` `0cb51f7158503d21f08cdf028e570391cedca37e13177dce2457779c10af98a4`、
`worker.rs` `0cc60bea06a27c770628fb4b3b08f474aa6a34228540e49c947eee7ecd8132a5`、`ipc.rs`
`8cbea90459cbfe2857355c5732cc3e9b3549180cf98d1cfc7c4a516a64bfc2fb`、`application.rs`
`b96ecfbbbfa5a87cd398ff2487c77dc9e8e6192f447eecf5c9bed5f522aac547`、`mod.rs`
`6ea940c2129a2b08039eb121ae95f9790667b207b2a79c25d7560ab23b1f4474`。

S8A 最终 Desktop implementation/readiness digests：`artifact.rs`
`1f03dd893958fdb6666aad9f98764e2ab6abc54256e0bf065c76628d90ccb58f`、`worker.rs`
`d7dd8b804d644a74b9f256607ea385d93ddbeb2ba82f39162a3a6cd1b4164d22`、`ipc.rs`
`d3c0da508abb8f20118bf089f74211e33f922af223006e7111b69cf81282786a`、`application.rs`
`d8eb06f03560383f5fc6bd3f5e4057c1b148b0dae81072c049d842123ebfb415`、`mod.rs`
`c0168e149d71ffee5663008510c8f9aee5e0bf7156f1fe6a93858bb3061bee33`。

S9A 最终 Desktop implementation/readiness digests：`artifact.rs`
`a8c3128bbc647fb99db516f60627952d0d5cb4d2923fa12ff4756f5ebd6de285`、`worker.rs`
`7cf74c094e735ff26fd17c4252dc693224cd237ba9ada5809bd12aa66b4128c0`、`ipc.rs`
`d3c0da508abb8f20118bf089f74211e33f922af223006e7111b69cf81282786a`、`application.rs`
`d3290063de27db9c9da967d5eb26506a5ddd551ead67cc68611513d95838803d`、`mod.rs`
`134d878b2955e9ca3f0ad0afebdf2d8a550737288e35bed0c125556465d03e20`。

## 6. AC/NFR 当前覆盖

| 范围 | 当前结果 | 说明 |
|---|---|---|
| AC-001/002/006/008/009 contract portions | CONTRACT PASS | lifecycle/report/resource/ACK/version/negative fixtures 已自动验证 |
| AC-011 contract fixture portion | CONTRACT PASS | image/video/file/report 四类 synthetic canonical fixtures 已形成 |
| AC-001/002 S5 UI projection portions | S5 FOUNDATION PASS | 8-state monotonic reducer、four-kind stable identity/order、duplicate idempotency、generic state shell 与 fail-closed conflicts 已单元/组件验证 |
| AC-003 image preview/save security boundary | S6A NATIVE PASS / S6B COMPONENT PASS / E2E NOT RUN | 3 exact commands、opaque one-shot protocol、双次 authority validation、atomic native save；ready-only UI、fresh inline/lightbox URL、release/stale isolation 与 content-free save feedback 已验证；page/runtime visual 待 S10 |
| AC-004 video fixture/native/UI boundary | CONTRACT + HOST S7F + DESKTOP S7A/S7A-REPAIR/S7B PASS / VERTICAL PENDING | Host emits exact canonical MP4；S7A proves SQLCipher inspect/Range/save；repair proves playback-compatible lifetime；S7B proves native controls/save UX and real WebView metadata/playback/seek；production Chat vertical待 S10 |
| AC-005 Desktop file behavior | S8A NATIVE PASS / S8B COMPONENT PASS / VERTICAL NOT RUN / AC PARTIAL | current-v3 plain/CSV/JSON bounded preview + renderer/search、PDF/XLSX fallback 与 five-MIME native save UX 已实现；Markdown deferred，production page/visual待 S10，G4 blocked |
| AC-006 Desktop report behavior | CONTRACT PASS / S9A NATIVE PASS / S9B-D FOUNDATION PASS / S9B-R REUSABLE UI PASS / PRODUCTION VERTICAL NOT RUN | report schema/fixtures、Desktop projection/save、exact dependency/theme/closed adapter/card 与 ready-report renderer/chart/save UX 已验证；production Chat/Tauri vertical 留待 S10，不能记完整 AC PASS |
| AC-007 persistence/history/retention | S4/S5 FOUNDATION PASS | v8 migration、SQLCipher BLOB、metadata history、168h TTL/receipt/delete/reopen + history replay/store dedupe 已验证；跨进程 UI integration 仍待 S10 |
| AC-008 runtime auth/integrity/ACK | S3/S4 FOUNDATION PASS | owner-only Host resource、MIME/size/digest/magic、commit 后 ACK 与 replay 已验证；E2E/error UI 待 S10 |
| AC-009 Host dual route + old/new matrix | PARTIAL PASS | v1/v2 equality/pins + 实际 v3 Host route 均通过；mixed-version E2E 待 S10 |
| AC-010/NFR-002 generic/image/video/file component portions | S5/S6B/S7B/S8B FOCUSED PASS | semantic tokens、Naive UI/YjIcon、aria-live/busy/progress/focus、image lightbox、native video controls、file disclosure/search、reduced-motion 与 axe 通过；full visual matrix/performance仍待 S10 |
| AC-011 local walking skeleton | PARTIAL | 四类 strict-local Host producer 已实现，video exact canonical 且 Desktop shell真实 metadata/playback/seek smoke通过；production Chat page/跨进程 vertical smoke 未运行 |
| AC-012/real provider | BLOCKED | capability 未证、未授权付费调用 |

## 7. 专项验证状态

| 专项 | 结果 | 后续切片 |
|---|---|---|
| Contract/source/generated/breaking | PASS | 边界漂移则重开 G2/G2A |
| Consumer exact pin/conformance | PASS | S3/S4 使用相同 immutable identities |
| Host v3 auth/range/replay/staging | S3 PASS | S10 仍需跨进程/restart walking skeleton |
| Desktop SQLCipher/transfer/cleanup | S4 PASS | S10 仍需 Host+Desktop integrated lifecycle |
| Image preview/save | S6A native PASS at `8b99849d418a3ef226f4133128f1ac22a438f9d5`; S6B component/a11y PASS at `4a8dce6a6526e37052941f6dbb921ba2486e109f` | page/vertical/runtime visual integration 仍待 S10 |
| Video fixture/native/UI boundary | Pattern 1.2.0 + S7F Host + S7A native + S7A-REPAIR + S7B renderer/runtime PASS at recorded full SHAs | production Chat vertical and full visual/performance evidence remain S10 |
| File preview/save boundary | Pattern 1.3.0 + S8A native `bf5452...` + S8B component `4d0238...` PASS；current-v3 plain/CSV/JSON bounded renderer/search + PDF/XLSX fallback + five-MIME native save UX | production page/visual remains S10；Markdown requires G2/G2A reopen or remains deferred/AC-005 PARTIAL |
| Report projection/save/renderer | Pattern 1.4.0 S9 readiness docs PASS；S9A `232ea6ce...` projection/save PASS；Pattern 1.5.0 readiness docs PASS；S9B-D `0a36ca7...` dependency/theme/closed adapter/card PASS；S9B-R `6bcc2a6b...` reusable renderer/chart/save + real-browser harness PASS | production Chat page + real Tauri report vertical仍 `NOT RUN`，属 S10 |
| UI/visual/a11y/performance | S5 generic + S6B image + S7B video + S8B file unit/component/axe/reduced-motion PASS；real video media lifecycle PASS；full manual visual/performance NOT RUN | S10 |
| Local synthetic E2E | NOT RUN | S10 |
| S10 keyless/single-v3/page/vertical/security-perf | READINESS DOCS PASS ONLY | S10A-LOCAL-PROFILE READY；S10A-E implementation NOT RUN |
| MiniMax/video/file/report real producer | BLOCKED | S12，需单独 authority/eval |
| Deployment/production rollback | N/A current local-only scope; gates NOT PASSED | G5/G6 |

## 8. Review findings closure

| Finding | 原状态 | 当前状态 | Evidence |
|---|---|---|---|
| G2-128-001 Owner/G2 closure | P1 | CLOSED AT G2 | 03 §2A/2B + Pattern Accepted |
| G2-128-002 missing source/immutable pin | P1 | CLOSED AT G2A | Contracts `ea48fe...` + source digests |
| G2-128-003 ACK/poster/retention/report ambiguity | P1 | CLOSED AT S3/S4 | 03-05 frozen semantics + Host/Desktop runtime conformance |
| BLK-128-004 generator/downstream pin | P1 | CLOSED AT G2A | locked generators + Host/Desktop pin commits |
| BASE-128-001 old Contracts lint/test failure | P2 historical | CLOSED | current lint/test and post-commit recheck PASS |
| Host docs stale `0.2.0` pin | P2 | CLOSED | Host pin commit updates README/AGENTS to actual lineage |

G2A 范围没有开放 P0/P1/P2。真实 provider、runtime security/data behavior、visual/a11y/performance 是后续
slice 的未验证范围，未被降级为已接受风险。

## 9. Owner G2/G2A decision capture

- G2：用户明确要求 Codex 分别以 Product/Design、Technical、Security/Data Owner 身份记录
  `APPROVED`，完整 capture 在 03 §2A/2B；UI Pattern 1.0.0 为 `Accepted`。
- G2A：用户明确设定条件——真实 generate、breaking、semantic review 和 immutable pin 完成后才能
  通过。第 3-5 节证据全部满足后，记录为 `APPROVED`。
- S6-READINESS：用户明确要求记录 Product、Technical、Security/Data 结论；03 §2C 与 Pattern 1.1.0
  已 capture 为 S6A coding ready，S6B 等待 S6A PASS。本结论仅授权范围，不声称 Codex 是独立人工 Reviewer。
- 用户随后明确执行 S6A，并在 checker 正确阻断 stale implementation digest 后另行批准最小 Desktop consumer digest
  例外；S6A 已形成独立 PASS，但没有追加到历史 G3 决策。
- 用户再明确执行严格 TS/Vue-only 的 S6B；它在 `4a8dce6a6526e37052941f6dbb921ba2486e109f`
  形成独立 PASS，同样没有追加到历史 G3 决策，也没有修改 S6A/native/config 或公共 pin。
- 用户本轮明确要求 S7-READINESS 只做安全/fixture/切片闭环并分别记录 Owner。Pattern 1.2.0 已 capture 为
  `READY FOR S7F ONLY; S7A/S7B WAIT`；该结论不是 S7 implementation PASS，也不追加 G3。
- 用户随后明确执行 S7F；Host `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` 已完成 canonical snapshot/checker/
  producer/manifest/Range conformance，保持 Contracts/tree/Desktop/dependency/public wire 不变。它是 G3 外 separate PASS。
- 用户随后明确执行 S7A；Desktop `22b91c5a258458c87f1ac96c06bf39d1af97358f` 已完成 private video inspect/Range/
  opaque handle/native save boundary，保持 Contracts/tree/Host/public pin/dependency/capability/migration 与 Vue UI 不变。它是 G3 外 separate PASS。
- 用户随后批准 content-free runtime diagnostics 与最小 S7A repair；`34991d8967de9aa2197ab2e8b9b49347774df7a5` 修复 64-success lifetime incompatibility，并以真实 WebView 证明 76 Range、metadata/playback/seek PASS。
- 用户随后明确执行并收口 S7B；Desktop `366186b601144bdc2bc87a2cef3075b74f1e8f19` 完成 reusable ready-video renderer/native-save UX，未修改 S7A boundary 或 production pages。
- 用户本轮明确执行 S8-READINESS 与 S7-SPEC-RECONCILIATION；Pattern 1.3.0
  `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` 废止累计 request-count 撤销的 operative 语义并冻结 S8A/S8B。
  Product 延期 Markdown，AC-005 保持 PARTIAL；Technical/Security/Data 只批准下一编码切片 S8A。本结论不是 S8
  implementation PASS，也不追加 G3。
- 用户随后明确执行 S8A；Desktop `bf5452f7fde24d1391845deaba17ec1135716c62` 在冻结的 exact schema/commands/limits/
  validator/save/residue 边界内完成，不含 Vue component、config/dependency/migration 或公共 contract/pin 漂移，记为 G3 外 separate PASS。
- 用户随后明确执行 S8B；Desktop `4d0238b1906f02d319f47f5e55cdc023485ef07a` 只在 `components/chat` 消费既有 S8A typed client，完成 ready-file renderer/search/fallback/save UX，未修改 native/config/page/store。
- 用户本轮明确执行 S9-READINESS；Pattern 1.4.0 `b6f7401c79d5b2356bc45468f14d7fdbb17a855c` 冻结 S9A
  consumer-conformance repair、identity-only bounded projection/canonical JSON save、unknown-payload omission 与 S9B
  fixed chart mapping。Product/Technical/Security/Data 只批准下一编码切片 S9A；S9B 等待 S9A immutable PASS，并因
  active app 无 ECharts dependency/theme 保持 blocked。该结论是 docs-only，不是 S9 implementation PASS。
- 用户随后明确执行 S9A；Desktop `232ea6ce132faa8ac99bdf6abcc5e02ddd704ffe` 在冻结边界内完成 consumer
  conformance repair、exact private two-command projection/canonical JSON save，并保持 Contracts/Host/public pin、S6-S8、
  component/config/dependency/migration 不变，记为 G3 外 separate PASS。
- 用户本轮明确执行 S9B-READINESS；Pattern 1.5.0 `630c3c8d55a2617499f51bd5bed263b819aaf084`
  选择 exact ECharts 6.1.0/static core/Canvas，冻结 integrity/license/transitives/import/bundle、semantic theme/card、
  closed adapter/table fallback、honest-unavailable metadata、a11y/lifecycle/visual 与 D/R 回滚。Owner 只批准下一编码切片
  S9B-D；本轮没有安装依赖或实现 D/R。
- 用户随后明确执行 S9B-D；Desktop `0a36ca7c54460d22ea6b3228832a57f05f0bde68` 完成 exact ECharts/lock/NOTICE、
  semantic theme/tokens、closed adapter + pure ordinal budget、accessible one-instance chart card、checkers 与真实浏览器 test-only
  visual matrix，未调用 S9A client、读取真实 report 或修改 Chat/native/config/pages/stores/public pin。它是 G3 外 separate PASS。
- 用户随后明确授权 S9B-D-CHECKER-REPAIR；Desktop `aec0f8a05ba7534132cbb4f46be64e333d7e9024`
  只把 checker 拆为固定历史 scope audit 与当前 immutable D protection，保留全部 dependency assertions，未启动 S9B-R。
- 用户随后明确执行 S9B-R；Desktop `6bcc2a6bfb4db76398ecf5483c688475477f08ed` 只在允许的 Chat component/test-only
  visual scope 消费 immutable S9A/S9B-D，完成 ready-report reusable renderer、closed chart enhancement 与 canonical save UX；
  无 native/config/page/store/dependency/pin 漂移，production vertical 未启动。
- 用户本轮明确执行 S10-READINESS 与 S9-SPEC-RECONCILIATION；Pattern 1.6.0
  `c1095eeb7a4c4bbc1f5a2729e9f8df861ebc02c2` 纠正 S9 current state，确认现有 synthetic 无 Runtime 时不可达、
  选择 exact FEAT126 loopback fake Responses 组合 profile，并冻结 single-v3/atomic cursor、content-free invalidation、
  V3 history/store/page 与 real-Tauri/security/perf DAG。Owner 只批准 S10A-LOCAL-PROFILE；本轮无实现。
- 这些授权已用于按序完成 local-only S3/S4/S5 与独立 S6A/S6B/S7F/S7A/S7A-REPAIR/S7B/S8A/S8B/S9A/S9B-D/S9B-D-CHECKER-REPAIR/S9B-R；
  G3 只对前三个原子切片通过，不允许 real provider、付费调用、
  tag、push、publish、release、production 或直接宣称 G4-G6 通过。

## 10. 残余风险与停止条件

| Item | 当前边界 | 停止/重开条件 |
|---|---|---|
| Host/Desktop cross-process lifecycle | 两端 isolated conformance 已完成 | S10 integration 出现 replay、TTL、ACK 或 scope 偏差时重开对应 slice/G2 |
| Desktop image preview/save/CSP | S6A 已实现 native boundary；S6B 只消费 typed client，实现 ready-only component/lightbox/save UX，未触碰 native/config | S10 page/runtime 集成若需要 plaintext、bytes/path to Vue、新依赖/plugin/capability/migration、native/config 改动、generic protocol 或外部 origin，立即停止并重开 Security/Data review |
| Preview handle/recovery | 30s one-shot、main WebView/process/context/session bound；S6B 对 inline/lightbox 分别取 fresh URL，并覆盖 close/unmount/error/context-stale release | S10 若出现跨 context/session replay、CORS/oracle、handle 持久化/复用或 lease 泄漏时阻断 |
| Native save crash residue | 正常取消/失败清除 temp；S8A 只在用户下一次选择同一目录时，以 exact file-only prefix/media marker/prior epoch/current uid/0600/nlink/1..64MiB/format validator 做 best-effort cleanup；不声称 crash 零残留 | 若需持久化目标路径、扫描任意目录、删除未完全验证条目或改变 S6/S7 verifier，停止并重开 Data review |
| Synthetic video playability | Contracts canonical + Host S7F + Desktop S7A/S7A-REPAIR/S7B real WebView metadata/playback/seek PASS | production Chat page vertical、light/dark/viewport/200-percent manual visual 与 longer-media performance仍待 S10；不得外推为真实 provider PASS |
| Video protocol/memory | 30min/5min multi-request handle、2 handles/2 reads/64MiB、GET/HEAD 200/206/416；repair 移除不兼容的 lifetime request count，76 Range smoke零 404 | S10 若需要扩大 buffered/concurrency/TTL、引入 rate limiter、新 dependency/capability/migration 或持久化/跨 context 复用 handle，停止并重开 Technical/Security review |
| S8 file boundary | S8A exact private 2-command boundary `bf5452f...` 与 S8B ready-file UI `4d0238b...` 已实现并验证；无 protocol/config/dependency/page/store drift | S10 page/vertical 若要求 Markdown/public contract、raw bytes/path to Vue、持久化/log/snapshot、generic fs/shell/asset、native/config drift 或扩大 exact limits，立即停止 |
| Markdown Artifact | current immutable v3 output 不含 `text/markdown`；Product 延期，AC-005 PARTIAL | 若本期必需，重开 G2/G2A、Contracts source/generate/breaking/semantic review、immutable commit 与全部 downstream repin |
| S9 report boundary | S9A `232ea6ce...` projection/save、S9B-D `0a36ca7...` dependency/theme/adapter/card 与 S9B-R `6bcc2a6b...` reusable renderer/chart/save 已实现；production vertical未实现 | 任何反向收紧 Contracts、raw JSON/unknown payload/path/error to Vue、超 exact caps、derived export、protocol/config/migration 或 S6-S8 drift 立即停止；回落 metadata shell |
| Unknown report section | contract 限 `required=false`、128 KiB、depth 8、opaque；S9A projection 只允许 unsupported marker | native/renderer 返回、遍历、搜索或执行 original type/payload 即阻断 |
| S9B-D dependency/theme | exact `echarts@6.1.0`/3-node lock/NOTICE/static Canvas/import/bundle/theme/adapter/card 已在 `0a36ca7...` 实现并通过 18-case real-browser matrix；checker repair `aec0f8a...` 固定历史 scope 并保护 immutable D boundary | S9B-R 若要求额外 package、full/dynamic/CDN import、arbitrary option、外部 origin或突破 frozen bundle/table/dispose边界，或改变 protected D 文件，立即停止并回滚 R |
| S9B-R renderer | `6bcc2a6b...` separate PASS；当前 projection 无 unit/data source/time range，UI 固定显示“报告未提供”；18-case test-only real browser PASS | production Chat/Tauri vertical仍待 S10；若要求推断/新契约字段或 protected/native/config drift则重开 G2/G2A/相应 review |
| S10 production seam | 当前 Host synthetic+fake互斥、Desktop只消费v2、Artifact apply/cursor非原子、Chat/Page未集成；Pattern 1.6.0已冻结修复顺序 | 只允许先执行 S10A exact local profile；任何 key/provider/non-loopback/public pin/fixture/migration/config widening立即停止 |
| Real MiniMax image | blocked | 固定 capability/API/model、费用与 bounded eval 单独获批 |
| Real video/file/report | blocked | 每 kind 形成 producer/ownership/security contract 后单独评审 |

## 11. 制品与工作树完整性

- Contracts、Host S3/S7F、Desktop S4/S5、Desktop readiness 与 S6-S9B-R/Pattern 1.6.0 commits 均为完整 40-character SHA；没有使用 floating branch/tag 作为 pin。
- 每个仓库在提交后重跑关键门禁；最终应保持 clean worktree。
- 生成物来自锁定 source/generator；Feature 目录不复制 canonical payload。
- 没有 `.skip`、`.only`、弱化断言、secret、真实业务数据或付费调用。

## 12. 结论

- G2：`APPROVED`。
- S1/S2：`PASS`，Contracts immutable local candidate 已形成。
- S2P：`PASS`，Host/Desktop exact pin 与 conformance 已形成，业务行为未改变。
- G2A：`APPROVED`。
- S3/S4/S5：`PASS`；G3 对这三个切片为 `PASS`。
- S6-READINESS：`PASS FOR DOCS ONLY`；S6A 在 `8b99849d418a3ef226f4133128f1ac22a438f9d5`、S6B 在 `4a8dce6a6526e37052941f6dbb921ba2486e109f` 分别独立 `PASS`。
- S7-READINESS：Pattern 1.2.0 为 docs PASS；S7F `1045dd...`、S7A `22b91c...`、S7A-REPAIR `34991d...` 与 S7B `366186...` 分别独立 `PASS`。
- S8-READINESS：Pattern 1.3.0 为 docs PASS；S8A `bf5452...` 与 S8B `4d0238...` 分别独立 `PASS`；Markdown deferred，AC-005 `PARTIAL`。
- S9-READINESS：Pattern 1.4.0 `b6f7401c...` 为历史 docs-only PASS；S9A `232ea6ce...` 已独立 `PASS`。
- S9B-READINESS：Pattern 1.5.0 `630c3c8...` 为 docs-only PASS；S9B-D `0a36ca7...`、
  S9B-D-CHECKER-REPAIR `aec0f8a...` 与 S9B-R `6bcc2a6b...` 已分别独立 `PASS`；canonical JSON save only，derived export deferred。
- S10-READINESS：Pattern 1.6.0 `c1095eeb...` 为 docs-only PASS；`READY FOR S10A-LOCAL-PROFILE ONLY`，S10A-E NOT RUN。
- Code Complete：否；S10A-E/S11、production vertical、full performance 与 independent review 尚未完成。
- 当前状态：`G3 PASS only for S3/S4/S5 / S6-S9B-R separate PASS / S10 readiness docs-only PASS / S10A-E NOT RUN / production vertical NOT RUN / real providers closed / G4-G6 not passed`。
