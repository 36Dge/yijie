# FEAT-128 原子实施计划

## 1. 实施原则

- G2 已于 2026-08-20 由段成威明确批准，随后先执行 Contracts S1-S2，再只做 S2P exact pin preflight。
- Feature 总体 `contract-impact = semantic`；G2A 在真实 generate、双基线 breaking、semantic review、immutable commit 和 downstream exact pin 全部通过后获批。随后严格先完成 Host S3、Desktop S4 与 Desktop S5；三者均通过 G3 slice gate。S6A native boundary 与 S6B image renderer 已在后续独立用户授权下分别完成，但均不扩展 G3，也不改变公共 Contracts/Host/pin。
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
              -> S7A Desktop native video Range/save boundary
                 -> S7B Vue native-controls video renderer
           -> S8 file preview/save
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
| S8 | 文本/MD/JSON/CSV 有界预览与其它格式 fallback/save | AC-005/010 | yijie-desktop components/domain | plain-text renderers、search/caps/tests | `v-html`、macro/PDF/Office fake preview | S5 | unit/component/security/visual | metadata/save only |
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
| D5 | S7A native video Range/save boundary | yijie-desktop private/native/config | Rust/TS RED/GREEN + full Desktop gates | H3 immutable PASS + separate authorization |
| D6 | S7B video renderer/native-save UX | yijie-desktop TS/Vue | component/axe/runtime seek/visual + full Desktop gates | D5 immutable PASS + separate authorization |
| D7-D8 | one commit per file/report renderer | yijie-desktop | focused + visual | D6 + per-slice readiness |
| E1 | deterministic E2E/evidence/review fixes | affected repos + yijie docs | full final gates | all above |

用户的逐轮明确指令已授权并完成 C1/HP/DP/H1-H2/D1/D2/D3/D4、S7 readiness 与 H3/S7F 的本地原子 commits；当前
尚未批准 D5/D6、S8-S12、push、PR、tag、release 或真实 provider。D5/S7A 虽已满足 immutable predecessor，仍需
单独用户授权；继续实施前仍需
逐仓确认用户已有改动并保持可独立审查。

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
| S7-READINESS | Desktop Pattern `18b17d961ed5991cec55eeb230ea21d91f2fb8ec` + yijie governance commit | docs/read-only audit only；canonical/Host mismatch、Range/save/CSP/lifecycle、S7F/S7A/S7B frozen | Desktop docs/lint/test/diff + governance full docs gates | Product/Technical/Security/Data READY FOR S7F ONLY；no implementation | PASS FOR READINESS ONLY |
| S7F | `1045dd06534eb72d53eb7ad7b7d18e63c80284f8` | derived canonical MP4 snapshot/embed；lock/sync/check exact path/tree/source/raw identity；bounded Go box/sample audit；video manifest/poster/auth/GET/HEAD/Range tests | EXPECTED RED: 81 vs 1642 bytes、digest mismatch、missing `moov`；GREEN focused PASS；`make contract-check/lint/test/runtime-test`、`git diff --check` PASS | 7-file allowed Host scope；Contracts/Desktop unchanged；no dependency/provider/public wire drift | PASS AS SEPARATE SLICE |
| S7A/S7B-S11 | N/A | none | NOT RUN | S7A requires separate authorization；S7B waits for S7A immutable PASS | PENDING |
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

G2、G2A 与 S3/S4/S5 的 G3 slice gate 均已通过；S6A/S6B/S7F 也分别形成 immutable PASS，但不并入 G3。
S7A/S7B 与 S8-S12 继续关闭，S7A 需要新的显式编码授权；真实 provider、tag、push、release 和生产能力继续
关闭，G4 不通过。

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
Contracts/Desktop/public wire/dependency/provider 变化。S7A/S7B 仍未授权或启动。
