# FEAT-126 Local-only 原子实施计划（S8B0 Closure Passed，G3 Partial）

## 1. 当前执行边界

- G2/G2A已于2026-08-02通过；DEC-126-023/024与Q-017已关闭，`29317b6426578749dc698fc2ad32b986ee5c8e9f`是唯一source-contract candidate并在专用远端分支精确可达。`c000a024...`仅保留为历史远端候选，Draft PR #1与各`origin/develop`不变。
- DEC-126-022 Local-only Delivery Strategy已Accepted；LIA-126-001已于2026-08-02批准，且只允许S4–S6本地基础切片。
- S4–S6已有远端checkpoint并保持flags/routes默认关闭；DEC-126-026已接受其Closure并单独授权S7A Desktop Rust Host Bridge/Domain。
- DEC-126-027已接受S7A；DEC-126-028已接受S7B durable outbox、strict/coalesced reducer、history orchestration、title precedence与fake Host应用链。
- DESIGN-126-005把原S8重新拆为S7C/S8A/S8B；DEC-126-030已接受S7C，DEC-126-031已接受LIA-126-004 S8A Closure。Owner现已接受DESIGN-126-006/DEC-126-032并单独授权LIA-126-005/S8B0；S8B及S9–S11仍须逐切片获得明确授权并重新核对full SHA/worktree。

## 2. 实施原则

- 一次只完成一个可独立验证的行为；contract-first；provider/consumer/activation 分离。
- Public Tasks安全轨与local conversation产品轨的S4–S8A Closure已批准；S8A在Rust/TypeScript补齐private IPC、validator/client和store，但仍不提供Vue UI。DEC-126-031不自动授权S8B。
- 先 consumer tolerance，再 producer 发新 output/event；先 schema expand，再 writer/switch，最后 cleanup。
- message body 只进入批准的 local DB/Runtime/provider，不进入 Public Tasks DB、普通日志或 fixture。
- 每个 repo 独立 commit/PR；不混入当前 yijie 的 FEAT-123 删除。

## 3. 依赖 DAG

```text
S0 G1 product decisions (Passed) + G2 Pattern/ADR design (Passed)
  ├─ S1 read-only Runtime capability investigation (schema/source complete; integration pending)
  │    → any canonical candidate waits for G2
  └─ S2 contract design freeze
       → S3 contracts source/generate/breaking/review → G2A
            ├─ S4 Public Tasks provider hardening
            ├─ S5 Agent Host provider/events/cleanup/title
            └─ S6 Desktop Rust local DB/project/sidecar foundation
                  → S7A Desktop Rust Host Bridge/wire domain
                       → S7B session/outbox/event reducer/history/title precedence
                            → S7C Rust actions/delete/interrupt/coordinator
                                 → S8A private IPC + TypeScript store/view-model
                                      → S8B0 gate/route/lifecycle/store/readiness integration
                                           → S8B production Vue UI/a11y
                                                → S9 fake-provider title/raw-reasoning Eval
                                                     → S10 local cross-repo security/resilience/migration E2E
                                                          → S11 Owner Local Runtime Ready acceptance (local G6)
```

## 4. 实施切片

| Slice | 主要意图 | AC | Repository | 允许修改 | 禁止修改 | 前置 | 未来验证 | 回滚 |
|---|---|---|---|---|---|---|---|---|
| S0 | 记录 G1/G2 产品与架构结论 | all scope | yijie + yijie-desktop docs | ADR/DEC/Pattern approval record | business source/contract schema | G1/G2 Passed；业务写入仍未授权 | package/links/Pattern review | revert docs; no runtime effect |
| S1 | 只读验证canonical Runtime reasoning/delete/title能力并补exact pin/Host/MiniMax证据 | AC-010/011/017/020/021/030 | yijie-codex | delete/name/summary/raw/outputSchema confirmed；delete functional PASS + forensic residue；MM title PASS/旧summary FAIL；raw delta/history/interleaving/interruption fixed fixtures 4/4 PASS | G2前禁止source write/额外模型调用；不把单样本当raw稳定性PASS | S0；exact Runtime base；任何写入还需G2 Passed | existing fake/delete + exhausted MM evidence | keep pin；raw flag off直到contract/conformance/Eval |
| S2 | 冻结 Public Tasks/Host/events/Desktop IPC/private DB contract design | AC-003/007/014/020–030 | yijie docs + design source | DESIGN-126-003、DEC-126-017/011/012与Accepted Pattern | provider/consumer code | S0/S1 findings | semantic review/consumer inventory | Complete / G2 Passed |
| S3 | 生成权威契约候选并通过 G2A | AC-007/010/014/025–028 | yijie-contracts | source schemas/fixtures/generator outputs/version docs | sibling handwritten DTO/implementation | G2 approved; S2 | generate/lint/test/all breaking/conformance review | no tag/pin; discard candidate PR |
| S4 | Public Tasks identity/tenant/owner/resource hardening本地draft | AC-025–030 | yijie-api | auth middleware, tasks domain/repo, local migrations/tests, exact contract projection | Desktop/Host；任何production route/legacy retirement | LIA-126-001 + exact candidate | lint/unit/local integration/security/migration | local flags/routes off; forward schema |
| S5 | Host raw-reasoning/title/cleanup与对账边界本地draft | AC-007/010/011/013/014/017/020/021 | yijie-agent-host | exact contract projection、raw adapter/no-log tests、fake Runtime fixtures | conversation DB、raw正文落bbolt/log、unapproved tools、MiniMax | LIA-126-001 + exact Runtime/candidate | contract-check/lint/test/fake runtime raw fixtures | keep raw/title flags off |
| S6 | Desktop Rust local DB、narrow commands、native project、sidecar supervisor本地draft | AC-001–006/015/020–024/029/030/034/035/037 | yijie-desktop | SQLCipher migrations/repository/Rust commands/native picker/local transport/tests | final Vue UI、token in WebView、arbitrary path/SQL、线上配置 | LIA-126-001 + exact candidate/DEC | Rust unit/local integration/migration/path/secret tests | chat flag off; forward repair |
| S7A | Desktop Rust Host Bridge/wire domain | AC-003/007/013/017/020/021 | yijie-desktop | owner-only bearer、exact loopback HTTP/SSE、spawn nonce readiness、strict v2 schema/cursor、typed session/turn/reasoning/cleanup domain与Rust tests | Tauri invoke、Vue/composables、outbox/reducer/history orchestration、title call、flag activation | DEC-126-026 + S5/S6 contracts | Rust fake Host/canonical fixture/security/fault + full Desktop lint/test/build | drop local bridge diff；flags remain off |
| S7B | Session state/outbox/SSE reducer/history/title precedence | AC-003/005/007/013–018/025/029 | yijie-desktop | Rust application/domain orchestration、outbox、event reducer、history/title precedence及tests | Tauri invoke、CSS/model picker/files、Vue UI、title Host call | DEC-126-027 + separate authorization | Rust/TS unit + fake Host domain E2E | flag off; no DB contract drop |
| S7C | Rust session/project actions、delete/interrupt与coordinator | AC-013/019–024/039/040/046/047 | yijie-desktop Rust | Rust-bound authorization context；session/project pin；interrupt；durable delete/cleanup status；background dispatch/subscribe/restart/resync projection source及tests | Tauri invoke/event、TypeScript/Vue、route/flag、central contracts/Runtime | DESIGN-126-005 + DEC-126-029 Accepted + separate S7C authorization | Rust repository/application + fake Host fault/race/restart/no-log | drop S7C diff；保持S7B DB/flags off |
| S8A | Private Tauri IPC与TypeScript store/view-model | AC-003/005/007/013/015/016/022/034/045–047; NFR-008/009 | yijie-desktop Rust + TS | authoritative IPC schema/fixtures、closed commands/events、runtime validators/client、Pinia store/view-model、selection/backpressure/resync tests | Vue页面/样式/route activation、mock production transport、central contracts/Runtime | S7C Closure + separate S8A authorization | schema↔serde↔TS conformance、security/no-log/restart/race、lint/test/build | drop S8A diff；无UI/flag |
| S8B0 | UI integration readiness，不含完整Vue视觉页 | AC-048–052；AC-002/016/028/029/034 subset | yijie-desktop Rust + TS integration | exact-off UI config、route/meta guards、permission lifecycle adapter、Pinia project/paging/cleanup actions、Tasks real/default-off、DESIGN-126-006 readiness schema/serde/TS fixtures/commands | 完整Chat Vue页面/组件/样式、visual design、flag activation、production mock、central contract/Runtime | DEC-126-032 Accepted + separate S8B0 authorization | gate truth table、route/loader/auth、schema conformance、store/restart/race/no-log、lint/test/build | drop S8B0 diff；all flags false |
| S8B | 极简production-grade Vue UI、交互与可访问性（仅本地运行） | AC-001/002/004/006/008–013/019/022/031–034/036/048–052 | yijie-desktop Vue | approved components/pages/tokens、真实S8B0 store接线、visual/a11y/tests/Pattern implementation | mock transport作为真实链、excluded actions/attachments/right panel/unrelated shell refactor、未经批准flag activation | S8B0 Closure + Accepted Pattern + separate S8B authorization | lint/test/build/visual/a11y/manual + real local chain | disable local chat UI flag；revert Vue slice |
| S9 | fake-provider title/raw-reasoning Eval | AC-010/011/017/018/042; NFR-007 | Host/Desktop + eval authority | fixed pin/dataset/runner；raw availability、sequence、content/security、no-log metrics | real data、MiniMax、unbounded calls、事后改写旧MM结果 | S5/S7C/S8A/S8B + later authorization | local fake Eval；future MM-126-003 separately approved only | title/raw flags off；missing raw blocks local G6 |
| S10 | 本地跨仓E2E/security/resilience/performance/delete rehearsal | all Must AC/NFR incl. AC-035–042 | API/Host/Desktop/pinned Runtime | local harness/runbook/evidence | production activation、real user data、tag/publish | S4–S9 + later authorization | full local matrix in 06/08 | stop local processes；fix/revert failing slice；flags off |
| S11 | Owner Local Runtime Ready验收 | AC-043 | all local | local startup guide、exact refs、evidence summary | merge/tag/publish/deploy/Production Ready声明 | G4 evidence + Owner review | local startup + complete functional chain | keep feature disabled until accepted；reopen failed slice |

## 5. 跨仓顺序

| 阶段 | Repository | Branch/base full SHA at planning time | 输出 | 下游 Pin | Owner |
|---|---|---|---|---|---|
| Governance | yijie | `develop@6c23dc3d9fa0d979948dbb10356fc5929ac2513b` | approved scope/ADR/gates | feature paths | 段成威 |
| Runtime candidate | yijie-codex | `develop@3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | canonical schema/artifact full SHA/digest | Host compatibility manifest | agent-runtime-team |
| Contract | yijie-contracts | `develop@9ec34abd6e7dfb5a23b0154d467694167224ebbb` | candidate version/full SHA/digests/generator/fixtures | API/Host/Desktop locks | platform-team |
| Public provider | yijie-api | `develop@faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | secure versioned Tasks + migration | Infra/Desktop only if consumed | backend-team |
| Local provider | yijie-agent-host | `develop@34e94acf293f6daad61c4d42fa47028a2d1318e4` | local Host operations/events | Desktop lock | agent-runtime-team |
| Consumer/storage/UI | yijie-desktop | `develop@155854cf3662384caa2c8bffe0a47935ef4a70b5` | app artifact + local schema | release manifest | client-team |
| Local orchestration | existing per-repo local commands; no yijie-infra source change initially | N/A | local startup/readiness/E2E evidence | exact local process/config manifest | 段成威 |

Base SHAs must be refreshed at slice start；this table is a planning snapshot, not branch creation or pin approval。

## 6. Migration 实施序列

| Phase | 代码/数据动作 | 兼容要求 | 验证 | 停止/回滚点 |
|---|---|---|---|---|
| Expand | Desktop current schema；API nullable owner/indexes/versioned route；Host v2 operation/event schema disabled且 v1 output不变 | old apps/providers still safe；old Host consumers不协商 v2；routes/flags off | empty/old DB + old/new consumers + explicit event-version negotiation | rollback binaries, keep additive DB/versioned contracts |
| Backfill | no Desktop legacy content; API legacy rows按批准 owner policy batches | no guessed owner; ambiguous inaccessible | counts/FK/scope sampling | pause/resume; forward repair |
| Switch local | enable local chat slices and secure route only in the approved synthetic local profile | exact local projection/tolerance and rollback app proven | local E2E/security assertions | close local flag/route |
| Contract cleanup | N/A in Local-only scope；legacy Public operation/production isolation remains | no production retirement | NOT RUN | future production feature/reopened gate only |

## 7. 每个 Codex 任务的固定 Context

```text
Feature ID / Slice ID: FEAT-126 / Sx
角色: Planner | Implementer | Tester | Reviewer
Repository / branch / base full SHA / worktree owner:
批准的需求 AC + decisions + Gate evidence:
权威契约/Runtime/private-schema reference and digest:
目标和唯一认知边界:
允许修改目录/files:
禁止修改目录/files:
真实验证命令/toolchain/environment:
secret/real-data/paid-call policy:
证据写入 08 的位置:
停止条件:
最终报告: diff/status/commands/results/NOT RUN/risks/next gate
```

## 8. Commit/PR 计划

| Commit/PR | 单一目的 | Files/Repo | Test evidence | Cross-link |
|---|---|---|---|---|
| PR-126-GOV | approve requirement/ADR/Pattern | yijie + Desktop docs | package/Pattern checks | Q/DEC IDs |
| PR-126-RT | canonical Runtime candidate if required | yijie-codex | Runtime schema/tests/artifact digest | S1/contract candidate |
| PR-126-CON | source contracts + fixtures + generated artifacts | yijie-contracts | generate/lint/test/breaking/semantic review | all consumer PRs |
| LOCAL-126-API-EXPAND | owner/auth/schema/secure route flag off | yijie-api local draft | unit/integration/security/migration | exact contract projection |
| LOCAL-126-HOST | raw-reasoning/title/cleanup provider flags off | yijie-agent-host local draft | contract/conformance/fault/runtime/no-log | Runtime+contract refs |
| LOCAL-126-DESKTOP-DATA | Rust DB/project/sidecar foundation flag off | yijie-desktop local draft | Rust migration/path/secret tests | exact contract projection |
| LOCAL-126-DESKTOP-BRIDGE | S7A exact Host transport + typed wire domain | yijie-desktop Rust local draft | bearer/nonce/SSE/schema/unknown/fault tests | data/Host contract refs |
| PR-126-DESKTOP-DOMAIN | S7B session/outbox/event/history application domain | yijie-desktop | reducer/DB/component tests | S7A/data/Host refs |
| LOCAL-126-DESKTOP-ACTIONS | S7C Rust actions/delete/interrupt/coordinator | yijie-desktop Rust | fake Host fault/race/restart/no-log | S7B + DESIGN-126-005 |
| LOCAL-126-DESKTOP-IPC | S8A schema/Tauri/TS store-view-model | yijie-desktop Rust/TS | IPC conformance/security/backpressure/restart | S7C Closure |
| LOCAL-126-DESKTOP-UI | S8B approved Vue UI/a11y | yijie-desktop Vue | visual/a11y/build/real-store assertions | S8A Closure + Pattern version |
| PR-126-EVAL | title/raw-reasoning dataset/runner/results | approved repo(s) | fixed Eval | prompt/model/runtime pins |
| LOCAL-126-E2E | local startup/readiness/E2E evidence | API/Host/Desktop/pinned Runtime | full fake-provider local matrix | Local-only G6 |

No commit/push/PR is authorized by this document。上述`LOCAL-*`只是未来本地change-set标识；是否提交或创建PR仍需另行授权。

## 9. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | no implementation SHA | requirement package + G1/G2 decision record + Accepted Desktop Pattern | package/links/docs build evidence in `08` | Owner approved G2 | G1/G2 Complete |
| S1 | no implementation SHA | read-only Runtime/Host/Public Tasks/storage investigation；fixed fake tests；historical bounded MiniMax evidence；no source diff | raw upstream 4/4 + prior title/summary/delete evidence | bounded facts complete；no implementation claim | Investigation Complete |
| S2 | no implementation SHA | DESIGN-126-003、Public Tasks inventory、DEC-126-017/011/012 | design consistency/package validation | Owner Approved | Complete / G2 Passed |
| S3 | prior remote `c000a0245acb5c3f7ead5d2a877fb60c281c588c` + sole candidate `29317b6426578749dc698fc2ad32b986ee5c8e9f` | source/fixtures/generated SDK/docs only | replacement post-commit gates PASS；old Draft PR remote CI audit FAIL | DEC-126-023/024/Q-017 closed；G2A Re-review Passed | Complete at source level；no remote or implementation authorization |
| S4 | local checkpoint `yijie-api@a64f9f591fb594818c1778e30c6941e2574b3264` | secure v2 foundation；default-off local-lab route；16 files | exact `29317b...` projection、generate drift、race/unit/lint、isolated PostgreSQL migration 1–4/integration PASS；audit/nil tenant/idempotency/content-free P1 closed | DEC-126-026 Accepted；checkpoint scope re-audited | Corrective Closure Passed / local commit / not pushed |
| S5 | local checkpoint `yijie-agent-host@3e8df026110f0c895262329c2384d3896598f3d9` | Host/event v2 raw/title/cleanup foundation；flags off；11 files | contract/race/lint/fixed Runtime PASS；cleanup recovery/lease/title isolation+idempotency/receipt/schema/no-log P1 closed | DEC-126-026 Accepted；checkpoint scope re-audited | Corrective Closure Passed / local commit / not pushed |
| S6–S8A | local checkpoint `yijie-desktop@3adcb0380561c294412bc24767e4651ca872455a` | SQLCipher v1–v4、Host/domain/application/actions/IPC/TS store；38 files；无Vue/router/style | exact `29317b...` projection、127 TS、93/94 Rust、clippy/fmt/build、migration/no-log/race/restart PASS | DEC-126-026/027/028/030/031 Accepted；checkpoint scope re-audited | Closure Passed through S8A / local commit / not pushed |
| S7A | included in `3adcb0380561c294412bc24767e4651ca872455a` | HostBridge、HostEventStream、strict typed domain、nonce-bound readiness与owner-only token；无Vue | S7A门禁与canonical reasoning/multi-frame chunk/fake Host/security/fault coverage PASS | DEC-126-027 Accepted | Closure Passed |
| S7B | included in `3adcb0380561c294412bc24767e4651ca872455a` | schema v3、transactional session/message/outbox、lease/unknown-outcome controls、coalesced reducer/terminal commit、20/50 history、title CAS；无Vue | `make lint/test/build` PASS；10,000 deltas、restart/mixup/reasoning reconciliation、fake Host→SSE→SQLCipher | DEC-126-028 Accepted | Closure Passed |
| DESIGN-126-005 | no implementation SHA | ConversationApplication/Tauri/TS gap inventory、private IPC v1、fixed fixture matrix与S7C/S8A/S8B重切 | feature docs validation | DEC-126-029 Accepted | Design Accepted；S7C/S8A later separately authorized |
| S7C | included in `3adcb0380561c294412bc24767e4651ca872455a` | schema v4、300s Rust-bound context/revision/capability facade、session/project actions、stable interrupt、durable cleanup/receipt、coordinator/restart/resync/live raw source；无Vue | `make lint/test/build` PASS；fake Host cleanup、v1-v4 migration、restart/idempotency/race/cascade/WAL/receipt-expiry/auth/no-log | DEC-126-030 Accepted | Closure Passed / G3 Partial |
| S8A | included in `3adcb0380561c294412bc24767e4651ca872455a` | 20 versioned commands、listen-only event、closed schema/fixtures、native auth binding、opaque cursors、strict TS validators/real Tauri client/authoritative Pinia reducer；无Vue | `make lint/test/build` PASS；127 TS；94 Rust（93 pass/1 existing ignored）；schema↔serde↔TS、auth/expiry/tenant、caps/backpressure/cancel/stale/restart/resync/no-log | DEC-126-031 Accepted | Closure Passed / G3 Partial |
| DESIGN-126-006 / DEC-126-032 | accepted design | S8B0 UI gate/route/lifecycle/store/readiness/tasks/scroll contract | feature package/static source inventory | DEC-126-032 Accepted | LIA-126-005 separately executed |
| S8B0 | local checkpoint `yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85` | 22-command closed IPC、Rust readiness/storage probe、exact-off gate、routes/lifecycle/store/Tasks metadata；不含完整Chat Vue visual | 135 TS；96 Rust（95 pass/1 existing ignored）；generate/lint/type/build/fmt/clippy/no-log PASS | LIA-126-005 / DEC-126-033 | Closure Passed / Accepted / not pushed |
| S8B、S9–S11 | N/A | none | NOT RUN | Not authorized | Pending separate sequential authorization |

## 10. 变更控制

| 变化 | 回到 |
|---|---|
| FEAT 编号/用户行为/AC | `00`/`01` + G1 |
| 仓库/authority/consumer | `02` + architecture review |
| permission/ownership/delete/data/security | `03` + security/data approval |
| HTTP/SSE/IPC/error/sorting semantics | `04` + contract review/G2A |
| DB/Runtime/component/state design | `05` + ADR/G2 |
| thresholds/Eval/tests | `06` + test owner review |
| dependency/order/slice scope | `07` + technical approval |

## 11. 计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| Product/G1 | 段成威 | Approved recommended product scheme；G1 Passed；no business slice authorized | 2026-08-01 |
| 技术负责人/G2 | 段成威 | Passed — DEC-126-017、DEC-126-011/012与FEAT-126 Pattern Accepted；进入G2A，仍不开始业务编码 | 2026-08-02 |
| Contracts/G2A/remote | 段成威 | DEC-126-023/024/025 Accepted，`29317b...`为唯一candidate并已远端可达；`c000a024...`仅为历史远端候选，旧PR与develop不变；未merge/tag/发布/启用 | 2026-08-02 |
| Contracts Draft PR / merge | 段成威 | DEC-126-021 Accepted/HOLD；CI failed dependency audit；merge不是local draft前置但当前仍不批准 | 2026-08-02 |
| Local-only delivery strategy | 段成威 | DEC-126-022 Accepted；Local Runtime Ready目标，tag/publish/deploy/G5 N/A | 2026-08-02 |
| Local Implementation Authorization | 段成威 | S7A–S8A已接受；DEC-126-032/033 Accepted并以LIA-126-005完成S8B0 Closure。S8B、S9–S11、MiniMax/flag activation与新增远端动作仍禁止 | 2026-08-03 |

## 12. Local Implementation Authorization 审批候选

### LIA-126-001（Approved / Executed）

- 批准范围：只启动`S4–S6`本地基础切片，分别限于`yijie-api`、`yijie-agent-host`、`yijie-desktop`；`yijie-codex`保持固定pin，`yijie-infra`不改。
- 契约输入：只允许`yijie-contracts@c000a0245acb5c3f7ead5d2a877fb60c281c588c`及其摘要匹配的已核验本地投影；不得用浮动branch、手写影子DTO或修改candidate。
- 模型/数据：仅fake provider、固定fixtures、本地合成identity/tenant和临时数据库；MiniMax调用、真实key/用户数据、云数据库均禁止。
- Git/远端：允许未来批准后修改本地业务工作树；本候选不包含commit、push、PR、merge、tag、publish或registry配置。
- 验证：逐仓使用各自`AGENTS.md`指定命令，至少完成lint/unit、契约/生成一致性、API本地security/migration、Host fake Runtime/no-log、Desktop SQLCipher migration/path/secret测试；结果回填`08`。
- 停止条件：contract digest不符、需要Runtime source change、需要外部/付费调用、真实数据、跨slice修改、未归属工作区改动、任一安全/删除/secret门禁只能靠降级断言通过。
- 首批完成后：提交S4–S6结构化review与证据；未获下一次批准前不启动S7–S11。

Owner审批结论：`批准LIA-126-001，仅授权S4–S6本地基础实现；继续禁止MiniMax、远端写入、merge/tag/publish/deploy及S7–S11。`执行结果与摘要见`08-verification-report.md`；该授权现已耗尽，不自动延伸到下一切片。

### LIA-126-002（Approved / Closure Accepted by DEC-126-026）

- 批准范围：仅S4–S6 Foundation Corrective Closure和四仓本地checkpoint；已由DEC-126-026接受。
- 已执行：创建四个`feat/feat-126-foundation-closure`本地分支及WIP checkpoint；元仓checkpoint未纳入FEAT-123删除。
- 停止事实：历史`c000a024`将Public Tasks v2 `input`定义为任意对象，canonical `conversation` fixture携带`input.text`并在response回显，与content-free-only边界冲突。
- Remote State Reconciliation：sole candidate与四个checkpoint分支已远端可达且SHA精确匹配；旧candidate/PR、各`origin/develop`、merge/tag/publish/deploy均不变。
- 退出结果：S4–S6 P1逐项以真实测试和安全/migration/no-log证据关闭；DEC-126-026 Accepted。该LIA不自动授权后续切片。

### S7A Desktop Rust Host Bridge/Domain（Authorized / Executed / Closure Accepted）

- 授权来源：Owner接受DEC-126-026并明确“单独授权S7A Desktop Rust Host Bridge/Domain实现”。
- 允许范围：owner-only bearer/token、exact IPv4 loopback HTTP/SSE、Host instance nonce/readiness、v2 schema/cursor及typed wire/domain adapter；仅Desktop Rust。
- 实际结果：新增`host_bridge.rs`、`host_domain.rs`并由`ChatRuntime`内部持有；支持session/turn/interrupt/cleanup/v2 event stream；不实现title operation；未知非terminal event丢payload、未知terminal fail closed。
- 安全边界：token以`O_NOFOLLOW`和owner/mode/nlink约束读取；no-proxy/no-redirect；错误和Debug不含Host message、token、project path或raw正文；没有新增Tauri command/invoke handler或Vue diff。
- 验证（S7A获批时）：Desktop全量门禁与fake Host/canonical fixture通过；只用fake Host和固定contract fixtures，MiniMax/provider call为0。
- 未授权：S8–S11、Vue/UI、feature flag activation、MiniMax、远端写入、push/merge/tag/publish/deploy；S7B仅由后续DEC-126-027单独授权。
- 退出状态：DEC-126-027已Accepted；G3保持Partial；Owner另行授权S7B。

### S7B Desktop Rust Application Orchestration/Domain（Authorized / Executed / Closure Accepted）

- 授权来源：Owner接受DEC-126-027并明确“单独授权S7B Desktop Application Orchestration/Domain Integration”。
- 允许范围：仅Rust侧outbox、事件reducer、历史加载编排和标题优先级；不新增Tauri/WebView/Vue入口。
- 实际结果：新增schema v3索引与`ConversationApplication`；create/turn幂等outbox、lease恢复/unknown-outcome fail closed、严格cursor reducer、批量checkpoint、terminal原子对账、20/50 turn history和user-wins title CAS。
- 验证：`make lint && make test && make build` PASS；113 TS tests；79 Rust tests（78 passed、1个既有signed Keychain integration ignored）；10,000 ordered deltas及fake TCP Host→SSE→SQLCipher完整Rust应用链PASS；MiniMax/provider call为0。
- 契约：本切片为Desktop私有durable/application semantic change，不修改Host/Public Tasks wire或唯一source candidate。
- 未授权：S8–S11、Vue/UI、Tauri invoke、feature flag activation、MiniMax、远端写入、push/merge/tag/publish/deploy。
- 退出状态：DEC-126-028已Accepted；G3保持Partial，未授权进入S7C/S8A/S8B或S9–S11。

### DEC-126-029至DEC-126-031逐切片授权（S8A Closure Accepted）

- 设计输入：DESIGN-126-005已完成ConversationApplication/Tauri invoke/TypeScript gap inventory，并冻结private IPC v1、安全边界、capacity、event/backpressure/cancel/stale/restart语义。
- Owner决定：DESIGN-126-005与DEC-126-029已接受；G3继续Partial，不启用flag，不改central contracts或Runtime pin。
- `LIA-126-003 / S7C`：已单独授权Desktop Rust authorization context、session/project actions、interrupt、durable delete/cleanup status、background coordinator与restart/resync projection source；仅使用fake Host、固定fixture、临时SQLCipher和临时CODEX_HOME；禁止Tauri invoke/event、TS/Vue、MiniMax、远端动作。退出需Rust fault/race/restart/no-log Closure Review。
- `LIA-126-004 / S8A`：Owner接受DEC-126-030后已单独授权authoritative IPC schema/fixtures、窄Tauri commands/events、TS validators/client/Pinia store/view-model；禁止Vue页面/样式/route activation和production mock transport。退出需schema↔serde↔TS、auth/no-log/backpressure/stale/restart/race Closure Review。
- `S8B0`结果：Owner接受DEC-126-032后单独授权LIA-126-005；exact-off gate、route/permission lifecycle、store consumption和closed readiness/storage private IPC已在`5dab02a1…34d85`完成；未实现完整Vue visual page，flag未启用。
- `S8B`授权候选：只在S8B0 Closure被Owner接受后另行授权Vue页面、交互、视觉与可访问性；必须消费真实authoritative store，mock只可存在test harness；feature flag activation仍不随S8B自动授权。
- S7C结果：Owner已接受DEC-126-030，S7C Closure Passed。
- S8A结果：20个versioned commands、closed Schema/fixtures、Rust-bound context/event/cursors、TS validator/client/store已实现；Desktop `make lint/test/build`及安全扫描PASS；DEC-126-031已接受S8A Closure，G3仍Partial。
- 当前状态：S8A Closure已由DEC-126-031 Accepted；DEC-126-032/033 Accepted且S8B0 Closure Passed。G3仍Partial；S8B实现/测试保持`NOT RUN`并继续未授权。

### LIA-126-005 / S8B0（Approved / Executed / DEC-126-033 Closure Passed）

- 授权来源：Owner明确批准DEC-126-032，并要求其后单独授权S8B0、不得直接进入S8B。
- 允许范围：Desktop private readiness/storage schema、Rust serde/commands/coordinator intent、TS validators/client/Pinia消费；exact-off UI gate、Chat/Tasks route和capability guard、permission bind/clear/dispose、project pick/revalidate、session追加分页、cleanup完成后的reload/clear/navigation disposition、production Tasks真实metadata/default-off。
- 禁止范围：完整Vue Chat页面/组件/视觉样式、App Shell项目/session树、composer、conversation flow、reasoning/menu/dialog/delete视觉交互及S8B a11y/visual实现；不得启用任何flag。
- 实施结果：`yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85`仅包含27个S8B0文件；新增2个closed commands后总数22，7个events不变；default-off gate、深链guard、permission lifecycle、store paging/project/readiness/cleanup与真实Tasks metadata接线完成；`sampleTasks`生产文件删除。
- 验证结果：135/135 TS，95/95 Rust（另1既有Keychain ignored），generate-check、lint、vue-tsc、Vite build、cargo fmt/clippy全绿；无production dependency、MiniMax、flag activation、central pin或远端动作。
- 环境：只使用fake Host、固定fixtures、临时SQLCipher/CODEX_HOME和test harness；不调用MiniMax或处理真实数据。
- 依赖/远端：不修改central contracts、Host/Public Tasks wire或Runtime pin；不新增production dependency；不push/merge/tag/publish/deploy。
- 退出：上述门禁与DEC-126-033 / S8B0 Closure Review已通过；S8B继续等待单独明确授权。
