# FEAT-128 原子实施计划

## 1. 实施原则

- G2 已于 2026-08-20 由段成威明确批准，随后仅执行 Contracts S1-S2；两端只在 S2P 写入 exact pin、canonical snapshot/checker 与 adapter 例外，没有实现业务行为。
- `contract-impact = semantic`；S1-S2 与 S2P 的真实 generate、双基线 breaking、semantic review、immutable commit 和 downstream exact pin 均已通过，G2A 已批准。S3/S4 从此刻起才获授权。
- 一次只完成一个可独立验证的行为；不把 v3 协议、媒体存储、native save 和四类 UI 一次混成大 diff。
- 先建立失败 fixture/测试，再实现最小能力；每个 kind 独立 flag，默认关闭。
- 不新增云资源、远程 URL、真实付费调用、通用 filesystem/shell capability 或第二套 UI 库。
- 每个仓库独立提交、PR、pin 和验证；本计划不授权 commit/push/tag/release。

## 2. 依赖 DAG

```text
S0 Owner G2 approval (PASS)
  -> S1 Contracts v3 lifecycle/report source (PASS)
  -> S2 Contracts generate/check/immutable commit + semantic review (PASS)
     -> S2P Host/Desktop exact pin + conformance only (PASS)
        -> G2A contract-ready decision (PASS)
           -> S3 Host v3 dual route + staging/resource/synthetic producer
           -> S4 Desktop v8 migration + native transfer/history/private IPC v3
        -> S5 Desktop shared Artifact state/rendering shell
           -> S6 image renderer/lightbox/save
           -> S7 video renderer/range/blob/save
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
| S6 | 图片 preview/lightbox/zoom/save 与错误状态 | AC-003/010 | yijie-desktop components/icons/styles | image renderer、dialog、tokens/tests | raw path/base64 in Pinia、clipboard/plugin | S5 + native preview/save approval | Vitest + visual matrix + Rust save tests | disable image renderer -> metadata/save fallback |
| S7 | 视频 controls/range/blob/CSP 精确变更与资源释放 | AC-004/010 | yijie-desktop components + approved Tauri config | video renderer、`media-src` exact change、tests | autoplay、external origin、player library | S5 + CSP approval + S3 range | UI/media tests + CSP/security + visual | no inline preview；metadata/save only |
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
| Provider pin preflight | yijie-agent-host | `feat/feat-128-structured-chat-artifacts@dea84d0768ebc017b7ee5faedab7f9a49ce74875` | exact pin/snapshots/checker only；S3 business not started | contract full commit + digests | Runtime Owner |
| Consumer pin preflight | yijie-desktop | `feat/feat-128-structured-chat-artifacts@96094419d963745529ed0fa246919089e659f20d` | exact pin/checker only；S4 business not started | contract full commit + source/fixture identities | Client/Data Owner |
| Consumer UI | yijie-desktop | same feature branch | Artifact shell + four renderers + harness | same exact pins | Product/Client Owner |
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
| H1 | v3 dual route/event reducer | yijie-agent-host | contract-check + unit/race | G2A PASS；not started |
| H2 | resource staging/range/synthetic producer | yijie-agent-host | security/resource/integration | H1 |
| D1 | pin + v8 migration/native transfer/private IPC | yijie-desktop Rust/schema/domain | migration/Rust/conformance | C2 + H2 |
| D2 | generic shell/state | yijie-desktop TS/Vue | unit/component/axe | D1 |
| D3-D6 | one commit per image/video/file/report renderer | yijie-desktop | focused + visual | D2 |
| E1 | deterministic E2E/evidence/review fixes | affected repos + yijie docs | full final gates | all above |

当前不授权创建上述 commit/PR。实现授权后仍需逐仓确认用户已有改动并保持可独立审查。

## 8. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | yijie docs candidate + Desktop `e97b2dabd724af856b4041e23b24437ec2f5dfc3` | G2 closure rewrite + Pattern 1.0.0 Accepted | package/design docs checks recorded in 08 | Owner direct approval captured | PASS |
| S1-S2 | `ea48fe190e18afba728712d1e2cc79cda57f581b` | v3 source/generated/fixtures/review/release candidate | generate/lint/test/build + dual breaking PASS | semantic review complete | PASS |
| S2P | Host `dea84d0768ebc017b7ee5faedab7f9a49ce74875`; Desktop `96094419d963745529ed0fa246919089e659f20d` | exact pins/checkers/snapshots only | both repositories full gates PASS | consumer pin conformance complete | PASS |
| G2A | evidence in 04/08/feature.yaml | immutable contract + both downstream pins | all required checks PASS | direct user conditional authority captured | PASS |
| S3-S11 | N/A | none | NOT RUN | now authorized; not started | PENDING |
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
| Product/Design Owner | 段成威 | FEAT-128 Pattern 1.0.0 Accepted | 2026-08-20 |
| Feature Owner | 段成威 | G2A APPROVED after S1/S2/S2P evidence | 2026-08-20 |

G2 与 G2A 均已通过。下一标准动作是从 S3 Host 业务切片开始，并保持真实 provider、tag、push、release
关闭；Desktop S4 只在 S3 conformance 满足后开始。
