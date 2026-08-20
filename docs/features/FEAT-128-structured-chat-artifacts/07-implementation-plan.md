# FEAT-128 原子实施计划

## 1. 实施原则

- G2 已于 2026-08-20 由段成威明确批准，随后先执行 Contracts S1-S2，再只做 S2P exact pin preflight。
- Feature 总体 `contract-impact = semantic`；G2A 在真实 generate、双基线 breaking、semantic review、immutable commit 和 downstream exact pin 全部通过后获批。随后严格先完成 Host S3、Desktop S4 与 Desktop S5；三者均通过 G3 slice gate。S6A/S6B、S7F、S7A、S7A-REPAIR 与 S7B 已在后续独立用户授权下分别完成，但均不扩展 G3，也不改变公共 Contracts/Host/pin。
- 一次只完成一个可独立验证的行为；不把 v3 协议、媒体存储、native save 和四类 UI 一次混成大 diff。
- 先建立失败 fixture/测试，再实现最小能力；每个 kind 独立 flag，默认关闭。
- 不新增云资源、远程 URL、真实付费调用、通用 filesystem/shell capability 或第二套 UI 库。
- 每个仓库独立提交和验证；commit 只按用户逐切片明确授权执行，本计划不自行授权 push/PR/tag/release。

## 2. 依赖 DAG

```text
S0 Owner G2 approval (PASS)
  -> S1 Contracts v3 lifecycle/report source (PASS)
  -> S2 Contracts generate/check/immutable commit + semantic review (PASS)
     -> S2P Host/Desktop exact pin + conformance only (PASS)
        -> G2A contract-ready decision (PASS)
           -> S3 Host v3 dual route + staging/resource/synthetic producer (PASS)
           -> S4 Desktop v8 migration + native transfer/history/private IPC v3 (PASS)
        -> S5 Desktop shared Artifact state/rendering shell (PASS)
           -> S6A native image preview/save boundary (PASS)
              -> S6B image renderer/lightbox/zoom (PASS)
           -> S7F Host canonical playable/seekable fixture conformance (PASS)
              -> S7A Desktop native video Range/save boundary (PASS)
                 -> S7A-REPAIR playback-compatible Range handle lifetime (PASS)
                    -> S7B Vue native-controls video renderer (PASS)
                       -> S8-READINESS + S7-SPEC-RECONCILIATION (PASS docs only)
                          -> S8A Desktop-private bounded file preview/save (PENDING)
                             -> S8B ready-file renderer/search/save UX (PENDING)
           -> S9 report document renderer/export
              -> S10 local synthetic vertical/visual/security/performance evidence
                 -> S11 structured independent review + local G4 decision

Real provider activation:
S2 + S3 + S4 + S10
  -> S12a MiniMax image capability/eval (separate paid approval)
  -> S12b video producer (blocked: no authority)
  -> S12c file/report producer (blocked: no authority/tool permission)
```

## 3. 实施切片

| Slice | 主要意图 | AC | Repository | 允许修改 | 禁止修改 | 前置 | 验证命令 | 回滚 |
|---|---|---|---|---|---|---|---|---|
| S0 | Owner 审阅并批准 DEC-128-005..011、ACK/poster/cursor/report、Pattern、limits/CSP/save boundary | all design | yijie + yijie-desktop docs | 00-07、Pattern/summary | 业务代码、权限 | G1 | G2 package check + recorded approval | PASS；若边界改变则重开 G2 |
| S1 | 定义 v3 OpenAPI/SSE/report schema 与 canonical invalid/valid fixtures | AC-001/002/006/008/009 | yijie-contracts | source contracts、fixtures、tests | Host/Desktop 手写 DTO、tag | S0 | focused schema tests first, then `make generate` | 丢弃未合并 candidate；v1/v2 不变 |
| S2 | 完成生成物、双基线 breaking、v1/v2 equality、release note candidate | AC-009 | yijie-contracts | generated SDK、compatibility docs/tests | 发布 tag、下游激活 | S1 | `make lint/test/build` + two breaking commands | 不形成 immutable commit则阻断 G2A |
| S2P | 写入两端 exact pin、canonical snapshots/fixture checker 与 adapter 例外；不改变业务行为 | G2A provenance | yijie-agent-host + yijie-desktop | locks、generated snapshots、conformance scripts/docs | route、staging、migration、native transfer、renderer、producer | S2 immutable commit | Host/Desktop existing full gates | 回退 pin-only commit；现有行为不变 |
| S3 | Host 支持 v3 dual route、Artifact manager、owner-only GET/HEAD/range、synthetic producer | AC-001/002/008/009/011/012 | yijie-agent-host | session/resource modules、tests；使用既有 pin | 长期业务库、真实 MiniMax、cloud | G2A PASS | `make lint/test/runtime-test` | flag off，移除 v3 route，v1/v2 continue |
| S4 | Desktop v8 SQLCipher authority、native transfer/ack/TTL/delete、private IPC v3/history | AC-002/007/008/009 | yijie-desktop `src-tauri/schemas/chat-ipc-v3.schema.json` + src-tauri/domain/api | migration、repository、Host bridge、IPC schema/parser/tests | Vue renderer、plaintext files、broad capability | G2A PASS + S3 conformance | Rust focused -> `make lint/test/build` | flag off；已存 Artifact 只读；v8 roll-forward |
| S5 | 建立 provider-neutral domain/store 与稳定 Artifact shell | AC-001/002/010 | yijie-desktop src/domain/stores/components | state reducer、generic list/card/status tests | type-specific preview、wire parsing in Vue | S4 fixtures | Vitest/component/axe | generic unsupported fallback remains |
| S6A | 实现图片 opaque-handle preview protocol 与 native save boundary；无 renderer | AC-003 security/native portions | yijie-desktop private schema + src-tauri + narrow domain/api | `chat-artifact-native-v1` schema/parser/client；artifact authority reader；3 exact commands；one image scheme；exact `img-src` delta；Rust/TS tests | components/pages/renderer；Contracts/Host/pin；migration；deps/lockfile/plugin/capability；generic fs/shell/asset；bytes/path to Vue | S5 + S6 readiness APPROVED | RED focused Rust/TS -> focused GREEN -> `pnpm lint/test`、`make build`、`pnpm docs:build`、diff | remove 3 commands/registry/scheme/CSP delta；SQLCipher schema/data unchanged |
| S6B | 使用 S6A handle/result 实现 image card/lightbox/zoom/save UX | AC-003/010 UI portions | yijie-desktop TS/Vue only | components/chat、domain/api integration、icons/styles/tests | src-tauri/config/capability/deps；wire parsing；bytes/base64/path/digest；S7+ | S6A immutable PASS | Vitest/component/axe + visual matrix + full Desktop gates | disable image renderer -> S5 metadata shell remains |
| S7F | 让 Host strict-local video producer 对齐既有 canonical playable/seekable MP4 | AC-004/011 fixture portions | yijie-agent-host | synthetic producer、derived pinned snapshot/checker/lock metadata、Host tests/docs | Contracts/Desktop、fixture tree/full_commit、schema/operation、ffmpeg/codec dependency、real provider | S7 readiness + Contracts canonical fixture | RED digest/box mismatch -> exact bytes/boxes/manifest + GET/HEAD/200/206/416 + `make contract-check/lint/test/runtime-test` | revert S7F；保持 transport-only 描述和 video UI off |
| S7A | 实现隔离的 native video inspect/Range/handle/save boundary；无 renderer | AC-004 security/native portions | yijie-desktop private schema + src-tauri + narrow domain/api/config/checker | independent schema/client；3 exact commands；SQLCipher video inspect/range；one video scheme；exact `media-src`；必要 internal implementation digests | components/pages；S6A behavior；Contracts/Host/public pin；deps/plugin/capability/migration；blob/data/asset/external | S7F immutable PASS + separate S7A authorization | Rust/TS RED→GREEN + full Desktop gates | remove commands/schema/client/registry/scheme/media-src；S6/data unchanged |
| S7B | 使用 S7A handle/result 实现 ready-video native-controls/save UX | AC-004/010 UI portions | yijie-desktop TS/Vue only | components/chat、necessary typed client integration、icons/styles/tests | src-tauri/config/checker/deps/pages；autoplay/player lib/poster command；S8+ | S7A immutable PASS + separate S7B authorization | Vitest/component/axe + Range/seek runtime smoke + full Desktop gates | disable video renderer；S5 metadata shell remains |
| S8A | Desktop-private identity-only bounded file preview/save boundary；无 renderer | AC-005 security/native partial | yijie-desktop private schema + src-tauri + narrow domain/api/checker | new `chat-artifact-file-native-v1`；2 exact commands；SQLCipher double validation；plain/CSV/JSON projection；five-MIME native save；必要 Desktop implementation/readiness SHA-only checker refresh | components/pages/stores；Markdown；Contracts/Host/public pin；protocol/CSP/capability/deps/migration；S6/S7 drift；path/raw bytes to Vue | S8 readiness + separate S8A authorization | Rust/TS EXPECTED RED→GREEN + full Desktop gates | remove file commands/schema/client/runtime；restore SHA-only checker；SQLCipher/S6/S7 unchanged |
| S8B | 使用 S8A projection/result 实现 ready-file renderer、literal search、truncation/fallback/save UX | AC-005/010 UI partial | yijie-desktop TS/Vue only | components/chat、typed client integration、tokens/icons/tests | native/config/checker/pages/stores/deps；v-html/link/formula/network；Markdown/PDF/Office fake preview | S8A immutable PASS + separate S8B authorization | Vitest/component/axe/security/visual + full Desktop gates | disable file renderer；S5 metadata shell remains |
| S9 | report document v1 adapter、metric/table/chart/callout renderer | AC-006/010 | yijie-desktop domain/components/design theme | safe mapper、ECharts theme、tests | arbitrary option、HTML/URL/script | S2 report schema + S5 | schema fixture/component/axe/visual | generic report metadata/save fallback |
| S10 | deterministic end-to-end、history/TTL/delete、security/performance/visual evidence | AC-001..012 | Host + Desktop + yijie docs | exact local harness/evidence docs | real provider、真实数据、production claim | S3-S9 | full gates + Playwright/axe + migration/adversarial | close flags, preserve evidence; findings reopen slices |
| S11 | 独立结构化审查、P0/P1/P2 修复和本地 G4 decision | all | all affected | review report/fixes within original slices | self-approval、release/tag | S10 | repeat affected/full gates | G4 remains pending until owner approval |
| S12a | 验证并可选启用真实 MiniMax image | AC-012 | Runtime/Host/Desktop/docs | capability config/adapter/eval after approval | video/file/report、unbounded spend | separate paid approval + S11 | fixed provider integration/eval | per-kind kill switch off |
| S12b | 视频 producer | AC-004/012 | future authority | only after new producer design | guessing provider API | blocked | command defined after authority | N/A until unblocked |
| S12c | 文件/report producer | AC-005/006/012 | future tool/provider | only after permission/producer design | arbitrary workspace writes | blocked | command defined after authority | N/A until unblocked |

## 4. 跨仓顺序

| 阶段 | Repository | Branch/base full SHA | 输出 | 下游 Pin | Owner |
|---|---|---|---|---|---|
| Governance | yijie | `feat/feat-128-structured-chat-artifacts` | G2/G2A records + Pattern reference | N/A | 段成威 |
| Contract source | yijie-contracts | `feat/feat-128-structured-chat-artifacts@ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable, unreleased `0.4.0` source/generated/fixtures/review | Host/Desktop exact full commit | Contracts Owner |
| Provider pin preflight | yijie-agent-host | `feat/feat-128-structured-chat-artifacts@dea84d0768ebc017b7ee5faedab7f9a49ce74875` | exact pin/snapshots/checker only | contract full commit + digests | Runtime Owner |
| Host S3 | yijie-agent-host | `feat/feat-128-structured-chat-artifacts@4017785adb08e1114781d3d844e9a10a683fa933` | local v3 lifecycle/staging/resources/ACK/synthetic；default off | same contract pin | Runtime Owner |
| Consumer pin preflight | yijie-desktop | `feat/feat-128-structured-chat-artifacts@96094419d963745529ed0fa246919089e659f20d` | exact pin/checker only | contract full commit + source/fixture identities | Client/Data Owner |
| Desktop S4 | yijie-desktop | `feat/feat-128-structured-chat-artifacts@09220dd8319cfb8ec0c4d1531514bb5169107983` | SQLCipher v8/native transfer/ACK/TTL/history/private IPC；default off | contract + 10 implementation digests | Client/Data Owner |
| Consumer UI S5 | yijie-desktop | `feat/feat-128-structured-chat-artifacts@7548ea8aeacfd7274f1107786ce48ddc6789cd45` | provider-neutral reducer/store + generic metadata shell；无 type renderer | same exact pins | Product/Client Owner |
| S6 readiness docs | yijie-desktop | `feat/feat-128-structured-chat-artifacts@2b854b40379a207c19bf37fc5bc64266553c5df1` | Pattern 1.1.0 冻结 S6A/S6B、preview/save/security boundary；无 code/config diff | same exact pins | Product/Technical/Security/Data Owner |
| Desktop S6A | yijie-desktop | `feat/feat-128-structured-chat-artifacts@8b99849d418a3ef226f4133128f1ac22a438f9d5` | private schema/client、SQLCipher double validation、opaque one-shot image protocol、native atomic save、精确 `img-src` delta；无 Vue renderer | Contracts full commit/source/fixture identities unchanged；仅刷新 Desktop implementation/readiness digests | Client/Security/Data Owner |
| Desktop S6B | yijie-desktop | `feat/feat-128-structured-chat-artifacts@4a8dce6a6526e37052941f6dbb921ba2486e109f` | ready image inline preview、fresh-handle lightbox、100/125/150/200% zoom、native-save UX、lease/stale-response/focus/a11y tests；无 native/config diff | Contracts/Host/pin、S6A commands/schema/config/digests 均不变 | Product/Client Owner |
| S7 readiness docs | yijie-desktop | `feat/feat-128-structured-chat-artifacts@18b17d961ed5991cec55eeb230ea21d91f2fb8ec` | Pattern 1.2.0 冻结 canonical fixture、S7F/S7A/S7B、video Range/save/CSP/lifecycle；无 fixture/code/config diff | Contracts `ea48fe...`、Host S3、Desktop S6B 均未改变 | Product/Technical/Security/Data Owner |
| Host S7F | yijie-agent-host | `feat/feat-128-structured-chat-artifacts@1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | canonical-derived video snapshot/embed、exact source/tree/raw checker、completed manifest 与 public GET/HEAD/Range conformance；无 public wire/Contracts/Desktop 变化 | Contracts `ea48fe...` 与 resource tree `f447129c...` unchanged | Runtime/Contracts Consumer Owner |
| Desktop S7A | yijie-desktop | `feat/feat-128-structured-chat-artifacts@22b91c5a258458c87f1ac96c06bf39d1af97358f` | independent private schema/client、SQLCipher video inspect/range、bounded multi-request opaque protocol、native atomic `.mp4` save、exact `media-src`；无 renderer | Contracts `ea48fe...`、resource tree `f447129c...`、Host S7F unchanged；仅刷新 Desktop implementation/readiness digests | Client/Security/Data Owner |
| Desktop S7A-REPAIR | yijie-desktop | `feat/feat-128-structured-chat-artifacts@34991d8967de9aa2197ab2e8b9b49347774df7a5` | 移除与 WKWebView Range 探测不兼容的 64-success lifetime revocation；保留 TTL/release/context/restart/concurrency/in-flight/double-validation；增加编译期关闭的 content-free runtime harness | Contracts/Host/pin/schema/commands/protocol/config/dependencies unchanged | Technical/Security/Data Owner |
| Desktop S7B | yijie-desktop | `feat/feat-128-structured-chat-artifacts@366186b601144bdc2bc87a2cef3075b74f1e8f19` | ready-video native controls、metadata/error/expired/retry、pause-clear-load-release、stale isolation、native-save UX；无 pages/native/config diff | S7A existing typed client/protocol unchanged；real WebView metadata/playback/seek PASS | Product/Client Owner |
| S8 readiness docs | yijie-desktop | `feat/feat-128-structured-chat-artifacts@4929a73a7871056d7aeca3eb0b27c682b21bfe4b` | Pattern 1.3.0；S7 request-count supersession；S8A/S8B exact schema/limits/lifecycle/save/stop conditions；无 code/config diff | Contracts/Host/Desktop implementation/pin unchanged | Product/Technical/Security/Data Owner |
| Activation | local environment only | clean immutable candidates | synthetic profile evidence | source identities recorded | 段成威 |

实现时必须填写完整 40-character SHA、source digests 和 generator identity；本文短 SHA 只用于阅读，不能作为 pin。

## 5. Migration 实施序列

| Phase | 代码/数据动作 | 兼容要求 | 验证 | 停止/回滚点 |
|---|---|---|---|---|
| Expand | 添加 v8 Artifact tables/indexes/FK/checks，不删旧 schema | v1-v7 populated DB 保留 | checksum、migration、legacy history | transaction 失败不提升 user_version |
| Backfill | N/A；旧消息无 Artifact | 不写旧行 | old history projects empty artifacts | 无 job |
| Switch | v3 transfer commit 后写 ready/history | v1/v2 writer/readers 继续 | crash/replay/WAL/reopen | master flag off，v8 data只读 |
| Contract | 本 Feature 不删除 v1/v2 或旧表 | old consumers supported | equality + rollback reader boundary | 未来独立 Feature |

v8 采用 forward-only。若需运行旧 Desktop，只能恢复升级前完整加密备份；不能手写 down migration 或只删新表。

## 6. 每个 Codex 任务的固定 Context

```text
Feature ID / Slice ID: FEAT-128 / Sx
角色：Planner / Implementer / Tester / Reviewer
Repository、branch、base full SHA：从 feature.yaml 与实际 git 命令取得
权威输入：00-07、04 contract plan、FEAT-128 Pattern、不可变 Contracts commit
目标及 AC：仅当前 slice 映射的 AC
允许修改目录：使用第 3 节白名单
禁止修改目录：当前 slice 外仓库/模块、真实 provider/cloud/release
真实验证命令：06-test-plan.md 与仓库 Makefile
证据输出：08-verification-report.md + repository test logs/artifacts
停止条件：新权限/依赖/producer/成本/contract drift、P0/P1、dirty source pin
最终报告：diff、commands/exits、AC evidence、NOT RUN、risks、git status
```

## 7. Commit/PR 计划

| Commit/PR | 单一目的 | Files/Repo | Test evidence | Cross-link |
|---|---|---|---|---|
| C1 | v3 source、fixtures、generated SDK、compatibility/release candidate | yijie-contracts source/generated/tests/docs | full gates + dual breaking | `ea48fe190e18afba728712d1e2cc79cda57f581b`；S1/S2 PASS |
| HP | pin v3 contract + snapshots/checker；无业务 route | yijie-agent-host | sync/contract-check/lint/test | `dea84d0768ebc017b7ee5faedab7f9a49ce74875`；S2P PASS |
| DP | pin v3 contract + fixtures/checker；无 migration/adapter/UI | yijie-desktop | generate-check/lint/test/build/docs | `96094419d963745529ed0fa246919089e659f20d`；S2P PASS |
| H1/H2 | v3 dual route/event reducer + resource staging/range/synthetic producer | yijie-agent-host | contract-check/lint/test/runtime-test | `4017785adb08e1114781d3d844e9a10a683fa933`；S3 PASS |
| D1 | pin + v8 migration/native transfer/private IPC | yijie-desktop Rust/schema/domain | migration/Rust/conformance/full Desktop gates | `09220dd8319cfb8ec0c4d1531514bb5169107983`；S4 PASS |
| D2 | generic shell/state | yijie-desktop TS/Vue | `7548ea8aeacfd7274f1107786ce48ddc6789cd45`；19 focused tests + full lint/test/build/docs/diff PASS | D1；S5 PASS |
| D3 | S6A native image preview/save boundary | yijie-desktop schema/Rust/narrow domain+api/config | `8b99849d418a3ef226f4133128f1ac22a438f9d5`；focused RED/GREEN + 6 TS/11 Rust focused + full Desktop gates | D2 + Pattern 1.1.0 readiness；S6A PASS |
| D4 | S6B image renderer/lightbox/zoom/save UX | yijie-desktop TS/Vue only | `4a8dce6a6526e37052941f6dbb921ba2486e109f`；expected RED、3 files/12 focused tests、axe + full Desktop gates；runtime visual matrix deferred to S10 | D3 immutable PASS；S6B PASS |
| H3 | S7F Host canonical video fixture conformance | yijie-agent-host | expected RED + exact resource/manifest/Range + full Host gates PASS | `1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；Contracts pin/tree unchanged；S7F PASS |
| D5 | S7A native video Range/save boundary | yijie-desktop private/native/config | `22b91c5a258458c87f1ac96c06bf39d1af97358f`；TS/Rust RED→GREEN、45 files/313 tests、11 focused Rust tests、full Desktop gates PASS | H3 immutable PASS + explicit S7A authorization；S7A PASS |
| D5R | S7A playback handle lifetime repair + runtime diagnostics/smoke | yijie-desktop private native + default-off harness | `34991d8967de9aa2197ab2e8b9b49347774df7a5`；request 65 EXPECTED RED、128-request GREEN、real WebView 76 Range/metadata/playback/seek PASS | D5 immutable PASS + explicit diagnostic/repair authorization；S7A-REPAIR PASS |
| D6 | S7B video renderer/native-save UX | yijie-desktop TS/Vue | `366186b601144bdc2bc87a2cef3075b74f1e8f19`；missing-component RED、3 files/14 focused、47 files/324 full、axe/runtime seek/build/docs PASS | D5R runtime PASS + separate authorization；S7B PASS |
| D7A | S8A bounded file preview/save native boundary | yijie-desktop private schema/Rust/narrow domain+api/checker | EXPECTED RED + focused/full gates；NOT RUN | Pattern 1.3.0 + separate S8A authorization |
| D7B | S8B ready-file renderer/search/save UX | yijie-desktop TS/Vue | focused/component/axe/security/visual；NOT RUN | D7A immutable PASS + separate S8B authorization |
| D8 | report renderer | yijie-desktop | focused + visual；NOT RUN | D7B + report readiness |
| E1 | deterministic E2E/evidence/review fixes | affected repos + yijie docs | full final gates | all above |

用户的逐轮明确指令已授权并完成 C1/HP/DP/H1-H2/D1/D2/D3/D4、S7 readiness、H3/S7F、D5/S7A、D5R/S7A-REPAIR
与 D6/S7B 的本地原子 commits；S8-READINESS 已完成 docs-only 审计并仅记录 `READY FOR S8A ONLY`。S8A/S8B 尚未
实现；当前尚未批准 S9-S12、push、PR、tag、release 或真实 provider。继续实施前仍需逐仓确认用户已有改动并保持
可独立审查。

## 8. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | yijie docs candidate + Desktop `e97b2dabd724af856b4041e23b24437ec2f5dfc3` | G2 closure rewrite + Pattern 1.0.0 Accepted | package/design docs checks recorded in 08 | Owner direct approval captured | PASS |
| S1-S2 | `ea48fe190e18afba728712d1e2cc79cda57f581b` | v3 source/generated/fixtures/review/release candidate | generate/lint/test/build + dual breaking PASS | semantic review complete | PASS |
| S2P | Host `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; Desktop `96094419d963745529ed0fa246919089e659f20d` | exact pins/checkers/snapshots only | both repositories full gates PASS | consumer pin conformance complete | PASS |
| G2A | evidence in 04/08/feature.yaml | immutable contract + both downstream pins | all required checks PASS | direct user conditional authority captured | PASS |
| S3 | `4017785adb08e1114781d3d844e9a10a683fa933` | v3 dual route、encrypted staging、GET/HEAD/range、ACK/TTL/restart cleanup、四 kind strict-local synthetic | `make contract-check/lint/test/runtime-test` PASS | scope/diff/default-off reviewed | PASS |
| S4 | `09220dd8319cfb8ec0c4d1531514bb5169107983` | SQLCipher v8、closed event/report adapter、native transfer/commit/ACK、168h TTL/delete、metadata-only history v3 | `make lint/test/build` + `pnpm docs:build` PASS | 10 implementation digests pinned；no renderer/CSP/save | PASS |
| S5 | `7548ea8aeacfd7274f1107786ce48ddc6789cd45` | provider-neutral identity/status/progress reducer、session/turn/Artifact store、generic metadata shell/list；无 preview/action | RED missing-module evidence；19 focused tests；`make lint/test/build`、`pnpm docs:build`、diff checks PASS | parser-approved metadata only；no dependency/Tauri/CSP/capability/wire drift | PASS |
| G3 | evidence in 08/feature.yaml | S3/S4/S5 only | owning-repository full gates PASS | planned scope and clean worktrees verified | PASS FOR S3/S4/S5 |
| S6-READINESS | Desktop Pattern 1.1.0 + yijie governance commits | pure docs audit：private IPC/Tauri/CSP/SQLCipher/S5；freeze S6A/S6B | Desktop docs build + both repos lint/test + governance package/YAML/diff checks | Product/Technical/Security/Data readiness captured；no implementation | PASS FOR READINESS ONLY |
| S6A | `8b99849d418a3ef226f4133128f1ac22a438f9d5` | 3 exact private commands、opaque preview handle/protocol、双次 SQLCipher 校验、native atomic save、typed content-free client；无 renderer | RED TS/Rust；6 TS + 11 Rust focused；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff；full Rust 196 pass/3 ignored | 最小例外仅刷新 Desktop implementation/readiness SHA；Contracts `ea48fe...`、source/fixture/protocol 未变；无 UI/dependency/capability/migration | PASS |
| S6B | `4a8dce6a6526e37052941f6dbb921ba2486e109f` | ready-image-only renderer、inline/fresh lightbox opaque URLs、finite zoom、content-free native-save feedback、handle release 与 stale-response isolation | missing-component RED；3 files/12 focused GREEN；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff PASS；full TS 308/308 | 仅 7 个 components/chat + icon files；axe/reduced-motion PASS；无 native/contracts/pin/dependency/page/store 漂移；runtime visual matrix NOT RUN，留待 S10 | PASS AS SEPARATE SLICE |
| S7-READINESS (historical) | Desktop Pattern `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` + yijie governance commit | docs/read-only audit only；canonical/Host mismatch、Range/save/CSP/lifecycle、S7F/S7A/S7B frozen | Desktop docs/lint/test/diff + governance full docs gates | historical Product/Technical/Security/Data READY FOR S7F ONLY；S7 chain later completed separately | PASS FOR READINESS ONLY |
| S7F | `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | derived canonical MP4 snapshot/embed；lock/sync/check exact path/tree/source/raw identity；bounded Go box/sample audit；video manifest/poster/auth/GET/HEAD/Range tests | EXPECTED RED: 81 vs 1642 bytes、digest mismatch、missing `moov`；GREEN focused PASS；`make contract-check/lint/test/runtime-test`、`git diff --check` PASS | 7-file allowed Host scope；Contracts/Desktop unchanged；no dependency/provider/public wire drift | PASS AS SEPARATE SLICE |
| S7A | `22b91c5a258458c87f1ac96c06bf39d1af97358f` | private schema/typed client、3 exact commands、SQLCipher MP4 inspect/range、30min/5min opaque video protocol、GET/HEAD single Range、native atomic `.mp4` save、exact `media-src` | EXPECTED TS/Rust RED；2 TS files/5 GREEN、11 focused Rust + 1 reader；`pnpm lint/test`、`make build`、`pnpm docs:build`、diff PASS；45 files/313 tests | exact 19-file scope；无 components/pages/stores、Contracts/Host/public pin、dependency/lockfile/capability/permission/migration/S7B 漂移 | PASS AS SEPARATE SLICE |
| S7A-REPAIR | `34991d8967de9aa2197ab2e8b9b49347774df7a5` | 移除 64-success lifetime revocation；保留 TTL/release/restart/context/WebView/2 handles/2 reads/64MiB/double validation；compile-time-off content-free diagnostics/runtime harness | request 65 EXPECTED RED；128-request focused GREEN；默认 11/11、feature 12/12 Rust；real WebView 76/76 Range、metadata/playback/seek PASS；clippy/diff PASS | 无 command/schema/protocol/CSP/capability/dependency/pin/page 漂移 | PASS AS SEPARATE SLICE |
| S7B | `366186b601144bdc2bc87a2cef3075b74f1e8f19` | ready-video-only native controls/save UX；metadata/error/expired/retry；pause-clear-load-release；stale/dedup/focus/a11y | missing-component EXPECTED RED；3 files/14 focused GREEN；47 files/324 full；`pnpm lint/test`、`make build`、`pnpm docs:build`、real WebView smoke、diff PASS | components/chat only；无 native/config/checker/contracts/host/pin/dependency/pages/stores 漂移；production vertical/manual visual matrix留待 S10 | PASS AS SEPARATE SLICE |
| S8-READINESS | Desktop Pattern `4929a73a7871056d7aeca3eb0b27c682b21bfe4b` + 本次 yijie governance commit | docs/read-only audit only；S7 spec reconciliation；S8A/S8B exact boundary、Markdown/SEC-006 decision | Desktop docs/lint/test/diff + governance full docs gates | Product/Technical/Security/Data `READY FOR S8A ONLY`；AC-005 PARTIAL；no implementation | PASS FOR READINESS ONLY |
| S8A/S8B | N/A | none | NOT RUN | S8A 需下一条独立编码指令；S8B 等 S8A immutable PASS；Markdown 需 contract reopen | PENDING |
| S9-S11 | N/A | none | NOT RUN | report、vertical/performance、independent review仍需独立授权与实施 | PENDING |
| S12 | N/A | none | BLOCKED | separate real-provider authority required | BLOCKED |

## 9. 变更控制

| 变化 | 回到 |
|---|---|
| 用户行为、Artifact kind、retention 或 AC 变化 | `01-requirements.md` |
| 仓库职责、Host/Desktop authority 或云资源变化 | `02-impact-assessment.md` + ADR review |
| 权限、CSP、save、数据分类、容量或费用变化 | `03-decisions-and-risks.md` |
| event/resource/error/history 语义变化 | `04-contract-change-plan.md` |
| storage/preview/cleanup 架构变化 | `05-technical-design.md` |
| 阈值、fixture、Eval 或命令变化 | `06-test-plan.md` |

## 10. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 技术负责人 | 段成威 | G2 APPROVED for Contracts S1/S2 | 2026-08-20 |
| Security/Data Owner | 段成威 | G2 APPROVED for Contracts S1/S2 | 2026-08-20 |
| Product/Design Owner | 段成威 | FEAT-128 Pattern 1.2.0 Accepted；READY FOR S7F ONLY，S7A/S7B WAIT | 2026-08-20 |
| Feature Owner | 段成威 | G2A APPROVED after S1/S2/S2P evidence | 2026-08-20 |
| Technical Owner | 段成威 | S6A CODING APPROVED within exact schema/3-command/scheme/CSP boundary | 2026-08-20 |
| Security/Data Owner | 段成威 | S6A CODING APPROVED；no dependency/plugin/capability/migration | 2026-08-20 |
| Technical/Security/Data Owner | 段成威 | S7F canonical conformance APPROVED；no Contracts tree/pin/dependency/provider drift | 2026-08-20 |
| Technical/Security/Data Owner | 段成威 | S7A bounded Desktop-private native boundary 已按显式指令完成并独立 PASS；no renderer/public pin/dependency/capability/migration drift | 2026-08-20 |
| Technical/Security/Data Owner | 段成威 | S7A-REPAIR 已按显式诊断/修复授权完成；只修复 playback lifetime，真实 WebView metadata/playback/seek PASS | 2026-08-21 |
| Product/Technical/Security/Data Owner | 段成威 | S7B 已按显式授权完成并独立 PASS；复用既有 typed client，no native/config/public contract/page drift | 2026-08-21 |
| Product Owner | 段成威 | Pattern 1.3.0 Accepted；READY FOR S8A ONLY WITH MARKDOWN DEFERRED；AC-005 PARTIAL；S8B WAIT | 2026-08-21 |
| Technical Owner | 段成威 | S8A CODING APPROVED：exact private schema + two commands + no protocol/config；只允许 Desktop SHA-only checker refresh | 2026-08-21 |
| Security/Data Owner | 段成威 | S8A CODING APPROVED：bounded authorized-content exception、no persistence/log/snapshot、native atomic save | 2026-08-21 |

G2、G2A 与 S3/S4/S5 的 G3 slice gate 均已通过；S6A/S6B/S7F/S7A/S7A-REPAIR/S7B 也分别形成 immutable PASS，
但不并入 G3。S8 readiness 仅批准下一切片 S8A；S8A/S8B 未实现，S9-S12 继续关闭。真实 provider、tag、push、
release 和生产能力继续关闭，G4 不通过。

## 11. 已执行 Codex 指令：S6A（历史证据）

下述指令已从 Desktop baseline `2b854b40379a207c19bf37fc5bc64266553c5df1` 执行完成，产出
`8b99849d418a3ef226f4133128f1ac22a438f9d5`；保留原文用于复核范围，不再作为下一条指令。

```text
执行 FEAT-128 / S6A，仅完成 yijie-desktop 图片 native preview/save boundary，不实现 renderer、灯箱或任何 Vue UI。

开始前：
- 完整阅读 yijie-desktop/AGENTS.md、FEAT-128 feature.yaml/03/05/06/07/08、Accepted Pattern 1.1.0；
- 核对 branch=feat/feat-128-structured-chat-artifacts、HEAD=2b854b40379a207c19bf37fc5bc64266553c5df1、
  Contracts pin=ea48fe190e18afba728712d1e2cc79cda57f581b，保护 dirty worktree；
- 不修改 Contracts/Host/pin，不 push/tag/PR/release，不扩 G3 或声明 G4。

测试先行：先补并运行失败的 Rust/TS 测试，再实现最小 GREEN。必须覆盖 foreign owner/session/turn、not-ready、
expired、wrong kind/MIME、size/digest/magic mismatch、one-shot duplicate GET、30s TTL、session/context/WebView/restart
replay、4-handle/2-read/40MiB limits、query/body/HEAD/Range/CORS/redirect 拒绝、save cancel、extension mismatch、
symlink/nonregular target、overwrite、permission/disk-full/write failure、temp cleanup 与 authority retained。

只允许：
- 新建 src-tauri/schemas/chat-artifact-native-v1.schema.json；
- 在 src-tauri/src/chat/ 下新增最小 artifact_native 模块，并仅为 SQLCipher ready-image reader 修改
  artifact.rs/application.rs/worker.rs/ipc.rs/mod.rs；
- 修改 src-tauri/src/lib.rs，精确注册 chat_open_artifact_image_preview_v1、
  chat_release_artifact_image_preview_v1、chat_save_artifact_image_v1 和唯一 custom scheme
  yijie-artifact-preview；
- 修改 src-tauri/tauri.conf.json，仅在既有 img-src 追加 yijie-artifact-preview:；
- 新增最小 src/domain/chat-artifact-native.ts、src/api/chat-artifact-native-client.ts 及对应测试，保证 payload 只有
  sessionId/turnId/artifactId、响应 content-free。

严格禁止：
- 修改 src/components、src/pages 或实现图片 renderer/lightbox/zoom；
- 新增/修改依赖、Cargo.lock/pnpm-lock、Tauri plugin、capabilities/permissions、DB migration；
- generic filesystem/shell/dialog/asset protocol、external origin、connect-src/media-src/object-src/frame-src 放宽；
- bytes/base64/digest/Host href/绝对路径/bearer 进入 Vue、Pinia、DOM、log、telemetry 或 snapshot；
- S6B/S7-S12、真实 provider/tool、部署发布。

实现必须逐项遵守 Pattern 1.1.0 §9.1-9.3 的 256-bit/43-char handle、30s one-shot、main WebView/process/context/
owner/tenant/session/turn binding、双次 SQLCipher content validation、empty-404/no-CORS protocol、canonical
.png/.jpg/.webp、native rfd panel、0600 same-dir temp、chunk digest、fsync/atomic replace、stable error codes。

运行 focused RED/GREEN 后顺序运行：pnpm lint；pnpm test；make build；pnpm docs:build；git diff --check。
检查最终 diff/工作树并创建一个本地原子 S6A commit，不得 push。随后只更新 yijie FEAT-128 的 07/08/10/
feature.yaml，记录真实命令、结果与完整 SHA；S6A 可单独记 PASS，但 G3 必须仍只包含 S3/S4/S5，G4 pending。

若需要新依赖/plugin/capability/permission、DB migration、Contracts/Host/pin 漂移、generic protocol、外部 origin、
把 path/bytes 暴露给 Vue，或无法用现有 SQLCipher/rfd/Tauri boundary 实现，立即停止并报告 blocker，不得扩大范围。
```

## 12. 已执行 Codex 指令：S6B（历史证据）

下述指令已从 Desktop baseline `8b99849d418a3ef226f4133128f1ac22a438f9d5` 执行完成，产出
`4a8dce6a6526e37052941f6dbb921ba2486e109f`；保留用于复核范围，不再作为下一条指令。

```text
执行 FEAT-128 / S6B，仅实现 yijie-desktop ready image renderer/lightbox/zoom/save UX；不得修改 native boundary。

基线：
- yijie-desktop HEAD: 8b99849d418a3ef226f4133128f1ac22a438f9d5
- Contracts pin: ea48fe190e18afba728712d1e2cc79cda57f581b
- Host S3: 4017785adb08e1114781d3d844e9a10a683fa933
- G3 仍只包含 S3/S4/S5；S6A 为独立 PASS；G4 pending。

开始前完整阅读 AGENTS.md、FEAT-128 的 03/05/06/07/08/feature.yaml 与 Accepted Pattern 1.1.0，并保护现有工作树。
测试先行：先为 image ready/non-ready、open/release、load/error/expiry、save saved/cancelled/failed、键盘焦点、
aria/reduced-motion 与卸载清理补失败的 Vitest/component/axe 测试，再实现最小 GREEN。

只允许修改 yijie-desktop 的 src/components/chat、必要的 TS-only domain/api integration、现有图标/semantic-token 样式与
对应测试。Vue 只能把 sessionId/turnId/artifactId/contextId 交给既有 typed client，只使用 parser 验证后的
yijie-artifact-preview URL；每次关闭、切换、卸载或加载失败都必须 release handle。保存只能由明确用户操作调用既有
chat_save_artifact_image_v1，并仅展示 content-free 状态/稳定错误码。

严格禁止：
- 修改 src-tauri、tauri.conf.json、private schema、Contracts/Host/immutable pin 或 implementation digests；
- 新增依赖、plugin、capability/permission、migration、外部 origin 或 generic filesystem/shell/asset protocol；
- bytes/base64/digest/Host href/绝对路径/token 进入 Vue、Pinia、DOM、日志、telemetry 或 snapshot；
- 视频/文件/report renderer、真实 provider、S7-S12、push/tag/PR/release，或扩大 G3/声明 G4。

实现 preview card、dialog/lightbox、键盘关闭、焦点归还、有限缩放与 native-save trigger；不得自行 fetch/read preview
内容，不得持久化或复用已消费/过期 URL。运行 focused RED/GREEN、component/axe/visual matrix 后，依次运行：
pnpm lint；pnpm test；make build；pnpm docs:build；git diff --check。

若现有 S6A typed client/opaque URL 无法满足 UI、需要任何 native/config/dependency/permission 变化，或发现 path/bytes 泄漏，
立即停止并报告，不得扩大范围。最终审计 diff/工作树，只有在用户明确授权本切片 commit 时才创建本地原子 commit；不得 push。
```

实际执行保持在 `src/components/chat` 与既有 icon registry/test：组件级 RED 为缺少
`ChatArtifactImage.vue`（exit 1）；最终 focused GREEN 为 3 files/12 tests，全量为 43 files/308 tests。
真实 Tauri 页面集成与 light/dark/viewport/200% 运行时视觉矩阵没有执行，不纳入本切片 PASS，留给 S10。

## 13. 已执行 Codex 指令：S7F（历史证据）

下述指令已从 Host baseline `4017785adb08e1114781d3d844e9a10a683fa933` 执行完成，产出
`1045dd06534eb72d53eb7ad7b7d18e63c80284f8`；保留原文用于复核范围，不再作为下一条指令。

```text
执行 FEAT-128 / S7F，仅修复 yijie-agent-host strict-local synthetic video fixture conformance；不得实现 Desktop
native/video renderer/save，也不得修改 Contracts canonical fixture。

基线：
- yijie-agent-host HEAD: 4017785adb08e1114781d3d844e9a10a683fa933
- yijie-contracts immutable pin: ea48fe190e18afba728712d1e2cc79cda57f581b
- canonical video resource: tests/fixtures/agent/resources-v3/synthetic-video-16x16.mp4.base64
- canonical raw size/SHA-256: 1642 / 96ea070cac612d17927939c22f3c0c593fb26b171f62c4e9cee43fb596177dd5
- Desktop remains 4a8dce6a6526e37052941f6dbb921ba2486e109f; Pattern 1.2.0 is
  18b17d961ed5991cec55eeb230ea21d91f2fb8ec.

开始前完整阅读四仓 AGENTS.md、FEAT-128 03/04/05/06/07/08/feature.yaml 与 Accepted Pattern 1.2.0，核对四仓
精确 HEAD/branch/worktree 并保护用户改动。只读再次证明当前 Host syntheticMP4 只有 ftyp/free/mdat、无 moov，
不得把它描述为可播放/可 seek。

测试先行：先增加并运行 EXPECTED RED，证明当前 Host video completed manifest 的 size/digest 不等于 canonical，且
box/track/sample audit 缺少 moov、avc1/avcC、duration/dimensions/stss keyframe。随后实现最小 GREEN，使 Host
strict-local producer 使用由 immutable Contracts fixture 派生并由 checker 逐字节验证的 consumer snapshot，或生成
raw bytes 完全相同的确定性结果；不得在 Host 维护可漂移的第二 authority，不得在运行时依赖 sibling checkout。

允许修改仅限 yijie-agent-host：
- internal/session 的 synthetic fixture producer、最小 derived snapshot/embed 与对应测试；
- scripts/check-contracts.sh、scripts/sync-contracts.sh、api/contracts.lock 中仅为现有 Contracts commit 增加 exact
  canonical resource path/raw digest/tree/snapshot conformance；必要的 Host docs/AGENTS 状态说明；
- internal/app 对 video GET/HEAD/no-range/single closed/open/suffix Range、200/206/416、multi-range reject 的测试。

GREEN 必须证明 raw 1642 bytes、SHA-256 96ea070c...77dd5、front moov、H.264/avc1、16x16、0.12s、3 frames、
首帧 keyframe、completed size/digest/poster、owner-only resource、default-off/strict-local manifest gates。测试不得依赖
运行机 ffmpeg/ffprobe；可以用 bounded Go box/sample parser。当前 Host multi-range 按公共 contract 返回 invalid-range
400 的既有语义不得改写成 Desktop-private 416。

严格禁止：修改 yijie-contracts 文件/full_commit/tree/schema/operation/version、Desktop/governance、公共 wire、真实
provider/tool；新增 dependency/codec/ffmpeg runtime、云/外网、长期存储、Tauri/CSP/capability；启动 S7A/S7B/S8-S12；
push/tag/PR/release；扩大 G3 或声明 G4。

依次运行 make contract-check、make lint、make test、make runtime-test、git diff --check。审计最终 diff 和 clean
worktree，创建一个本地原子 S7F commit，不得 push。随后只更新 yijie FEAT-128 的 07/08/10/feature.yaml，记录真实
完整 SHA、RED/GREEN 与最终命令；S7F 只能记 separate PASS，G3 仍只含 S3/S4/S5，S6A/S6B 仍 separate PASS，
G4 pending。若任何实现需要 Contracts/tree/pin 漂移、新 dependency/runtime codec、真实 provider 或 Desktop 变化，
立即停止并报告 blocker，不得扩大范围。
```

实际 EXPECTED RED 为当前 `syntheticMP4()` 输出 81 bytes、SHA-256
`b4bed74c1214ad307baa3ffe766ac139782991586adc26a3771c23cf08b8599e`，与 canonical 1642 bytes/
`96ea070cac612d17927939c22f3c0c593fb26b171f62c4e9cee43fb596177dd5` 不同，结构检查因缺少 `moov` 失败。
GREEN 使用由 Contracts `ea48fe...` resource 派生的 Base64 snapshot；checker 锁定 source path、source SHA、tree OID、
raw size/SHA 与 snapshot SHA，运行时只解码 embed 并复核 raw identity，不依赖 sibling checkout。focused session/app
测试与 `make contract-check`、`make lint`、`make test`、`make runtime-test`、`git diff --check` 均 exit 0；无
Contracts/Desktop/public wire/dependency/provider 变化。S7A、S7A-REPAIR 与 S7B 后来均在独立授权下完成。

## 14. 已执行 Codex 指令：S7A（历史证据）

S7A 已从 Desktop baseline `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` 按用户显式授权执行，产出本地原子
commit `22b91c5a258458c87f1ac96c06bf39d1af97358f`，未 push。测试先行证据为：两个 TS focused suite 因
private domain/client 尚不存在而 exit 1；Rust focused suite 因 Range/MP4/registry 类型与函数尚不存在而 exit 101。
最小 GREEN 为 2 个 TS 文件/5 tests、`artifact_video_native` 11 tests 与 SQLCipher video reader 1 test。

实现严格停在 Desktop-private native boundary：独立 `chat-artifact-video-native-v1` schema/typed client、exact open/release/save
commands、SQLCipher ready-video 有界 MP4 inspect/range、`yijie-artifact-video://localhost/v1/<43-char opaque handle>`、30min
absolute/5min idle、2 handles/WebView、1/artifact、2 concurrent reads/64MiB in-flight、GET/HEAD 与
single closed/open/suffix Range 的 200/206/416，以及复用 S6A atomic kernel 的 content-free `.mp4` native save。最终
`pnpm lint`、`pnpm test`（45 files/313 tests）、`make build`、`pnpm docs:build`、`git diff --check` 均 exit 0；
额外 `make lint` 也 exit 0。仅按批准例外刷新五个 Desktop implementation/readiness digests；Contracts full commit/source/
resource tree/version/operations/schemas、Host、公共协议均未改变。没有 components/pages/stores、renderer、dependency/lockfile、
capability/permission、migration、S7B 或真实 provider 变化。原始 64-success lifetime limit 后经真实 WKWebView
诊断证明与 metadata Range 探测不兼容，并在独立 S7A-REPAIR 中移除。

## 15. 已执行 Codex 指令：S7A-REPAIR 与 S7B（历史证据）

S7A-REPAIR 从 `22b91c5a258458c87f1ac96c06bf39d1af97358f` 开始。编译期关闭、content-free diagnostics 证明 WebKit
在 metadata-ready 前需要超过 64 个合法 Range：前 64 个均通过 header、SQLCipher、digest、MP4 与 response 校验，
随后 handle 被累计次数上限撤销并产生 404。repair 测试先行将同一 handle 扩展到至少 128 次请求，旧实现于第 65
次返回 `NotFound`（EXPECTED RED）；最小 GREEN 只移除 lifetime request counter/revocation，保留 absolute/idle TTL、
release、restart、context/WebView invalidation、2 handles、2 concurrent reads、64MiB in-flight 与双次 SQLCipher 校验。
提交 `34991d8967de9aa2197ab2e8b9b49347774df7a5` 的真实 Tauri WebView smoke 为 76 GET/Range、76 个 206、
`metadataReady/playbackStarted/seeked=true`、`beginRequestFailed=0`、`responsesNotFound=0`。

S7B 提交 `366186b601144bdc2bc87a2cef3075b74f1e8f19` 只增加 reusable ready-video component 与 shell/list typed
integration：原生 `<video controls preload="metadata">`、无 autoplay/PiP/remote/browser download、稳定 loading/error/
expired/retry、同一播放会话 handle、retry fresh handle、pause-clear-load-release、stale/duplicate guard 和 content-free
native-save feedback。missing-component EXPECTED RED 后，focused 3 files/14 tests、axe/reduced-motion、全量 47 files/324
tests、lint/build/docs/diff 与上述真实 WebView playback/seek 均通过。未修改 S7A commands/schema/protocol/config、pages、
Contracts/Host/pins/checkers、依赖、capability/permission 或 migration；生产 Chat vertical/manual visual matrix仍留待 S10。

## 16. 下一条可执行 Codex 指令：S8A

```text
执行 FEAT-128 / S8A，仅实现 yijie-desktop Desktop-private bounded file preview/save boundary；禁止实现 S8B
renderer、搜索或任何 Vue component。

基线：
- yijie-desktop HEAD: 4929a73a7871056d7aeca3eb0b27c682b21bfe4b
- yijie governance: 使用本次 S8-READINESS 最终治理 commit
- Contracts pin: ea48fe190e18afba728712d1e2cc79cda57f581b
- Host S7F: 1045dd06534eb72d53eb7ad7b7d18e63c80284f8
- Accepted Pattern 1.3.0: 4929a73a7871056d7aeca3eb0b27c682b21bfe4b
- G3 仍只包含 S3/S4/S5；S6/S7 slices separate PASS；G4 pending。

开始前完整阅读 yijie-desktop/AGENTS.md、FEAT-128 03/05/06/07/08/feature.yaml 和 Pattern 1.3.0；检查并保护
Desktop/yijie 工作树，不得 reset、checkout、stash 或覆盖用户改动。确认 Contracts full commit/source/tree/fixture/
schema/operation/version 均未漂移。

测试先行：先编写并运行 EXPECTED RED 的 Rust/TS tests，再实现最小 GREEN。实现独立
chat-artifact-file-native-v1.schema.json 与 exact commands chat_read_artifact_file_preview_v1、
chat_save_artifact_file_v1；closed request <=4096 bytes，仅 schemaVersion/requestId/contextId 与
sessionId/turnId/artifactId。只接受 main WebView + current ReadSessions context。

Preview：不签发 URL/handle、不新增 protocol/CSP/release。native 前后两次校验 SQLCipher owner/tenant/session/turn/
artifact、ready/unexpired、kind=file、MIME、size/BLOB length/digest/revision/format。inline 仅 text/plain、text/csv、
application/json；PDF/XLSX metadata/save-only。source<=1,048,576B、projection<=262,144B、response<=524,288B；
text/JSON<=2,000 lines、line<=8,192 UTF-8B；CSV<=200x50、cell<=4,096B；JSON depth<=32/nodes<=20,000；
preview<=2 concurrent/WebView、source in-flight<=2,097,152B、same identity single-flight、10s timeout。UTF-8 only，
仅去一个 BOM，CRLF/CR projection->LF；TAB/LF/CR 外 C0/DEL/C1 拒绝 inline，并拒绝 Unicode `Bidi_Control`
`U+061C`、`U+200E-U+200F`、`U+202A-U+202E`、`U+2066-U+2069`。JSON full parse 后只返回 inert text；CSV
bounded RFC4180 parse 后只返回 cell strings，不执行 formula。结果严格为 Pattern 1.3.0 的 closed union，不得含
name/size/path/digest/Host href/token/bytes/base64/raw error。

Save：仅明确 click/keyboard intent；五种 current-v3 MIME，ready-file bytes `1..67,108,864`，与 1MiB preview
eligibility 独立；canonical `.txt/.csv/.json/.pdf/.xlsx`，无扩展名 native 追加，mismatch fail closed。plain/CSV
valid UTF-8 no-NUL、JSON full parse；PDF 复用既有 bounded preflight（classic xref/EOF、非加密、无 ObjStm/XRef
stream/Prev、objects<=4,096、pages 1..256、streams<=1,024、单/总 decoded stream<=8/32MiB、ratio<=100:1、
expanded traversal<=4,096 stream visits/32MiB、form depth<=16、page-tree depth<=64）；XLSX
复用既有 bounded OOXML validator（entries 1..512、safe unique names、Stored/Deflated、单/总 uncompressed<=8/32MiB、
ratio<=100:1、无 `.bin`/`vbaProject`、required `[Content_Types].xml` + `xl/workbook.xml` + matching main type）。
不得提取/渲染/执行/自动打开。dialog 前校验并释放 bytes，dialog 后重新读取/校验，复用 same-dir 0600
create-new/no-follow temp、chunk digest、fsync、atomic replace/RAII。file temp exact filename 为
`.yijie-artifact-file-save-v1-<txt|csv|json|pdf|xlsx>-<process-epoch UUID>-<22-char base64url>.tmp`；只在用户下一次
选择同一目录时清除 prior epoch 且 exact marker、regular non-symlink、current uid、0600、nlink=1、size/format
全通过的条目；当前 epoch/其它条目与 S6/S7 prefix/行为不变。Vue 只收 content-free saved/cancelled/failed。

允许修改：
- new src-tauri/schemas/chat-artifact-file-native-v1.schema.json
- new src-tauri/src/chat/artifact_file_native.rs
- 必要的 artifact.rs/application.rs/worker.rs/ipc.rs/mod.rs/lib.rs
- artifact_native.rs 仅限无 S6/S7 行为漂移的 atomic helper/residue 复用
- attachment.rs 仅限暴露/复用既有 bounded PDF/XLSX validator；不得改变 attachment import 行为或 limits
- new TS-only domain/client 及对应 tests
- 必要的 v2/v3 consumer lock/checker/test constants，但只能刷新 Desktop implementation/readiness SHA

严格禁止：components/pages/stores；Markdown；Contracts/Host/public/private existing schemas or commands；Contracts
full_commit/source/tree/fixture/version/operation；tauri.conf/capability/Cargo/pnpm dependencies/lockfile/migration；custom
protocol、CSP、generic filesystem/shell/asset、browser download、external origin；bytes/base64/digest/path/href/token 到
Vue/Pinia/DOM/log/diagnostics/snapshot；修改 S6/S7 boundary；启动 S8B/S9-S12、provider、push/tag/PR/release。

必须覆盖 authority/identity/state/MIME/expiry/length/digest/revision/format、UTF/BOM/control/bidi、所有 limits、CSV
quotes/malformed/formula、JSON depth/nodes、same-identity/concurrency/timeout、stale/drift、save extension/dialog cancel/
symlink/nonregular/atomic/fsync/residue、schema/leak negative、exact 2 commands、S6/S7/config/dependency unchanged。

依次运行 focused RED/GREEN、pnpm lint、pnpm test、make build、pnpm docs:build、git diff --check。任何测试、安全或
stop condition 失败立即停止，不做猜测性扩展。全部通过后审计 diff，创建一个 Desktop 本地原子 S8A commit，不得
push。随后只更新 yijie FEAT-128 的 07/08/10/feature.yaml，记录完整 SHA/RED/GREEN/全量命令；S8A 记 separate
PASS，不并入 G3，G4 pending。运行 G3/strict package、unique-key YAML、pnpm lint/test、bash -n、diff 后创建一个
governance 本地原子 commit，不得 push。
```
