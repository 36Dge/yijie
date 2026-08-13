# FEAT-126 Local-only 原子实施计划（DESIGN-126-021 Complete / LIA-126-036 Corrective Closure Accepted / G3 Partial）

## 1. 当前执行边界

- G2/G2A已于2026-08-02通过；DEC-126-023/024与Q-017已关闭，`29317b6426578749dc698fc2ad32b986ee5c8e9f`是唯一source-contract candidate并在专用远端分支精确可达。`c000a024...`仅保留为历史远端候选，Draft PR #1与各`origin/develop`不变。
- DEC-126-022 Local-only Delivery Strategy已Accepted；LIA-126-001已于2026-08-02批准，且只允许S4–S6本地基础切片。
- S4–S6已有远端checkpoint并保持flags/routes默认关闭；DEC-126-026已接受其Closure并单独授权S7A Desktop Rust Host Bridge/Domain。
- DEC-126-027已接受S7A；DEC-126-028已接受S7B durable outbox、strict/coalesced reducer、history orchestration、title precedence与fake Host应用链。
- DESIGN-126-005把原S8重新拆为S7C/S8A/S8B；S4–S9及S10E/P1/P2F/P3/S10BP1/S10BR1/S10BM1/S10BD1/S10BF1/S10BRP1 Closure已接受。LIA-126-022/S10B-R6已消费并在S10B-001 resolver步骤fail closed；DEC-126-060/061 Option A已Accepted。LIA-126-023/S10BEP1 repository implementation及S10BEP1-014 isolated live验证已PASS，DEC-126-062已接受Corrective Closure并关闭`S10B-BLK-007`；DEC-126-063已形成Infra/Governance本地clean checkpoints。`S10B-BLK-001–007`现均Closed，G3保持Partial，fresh R7与S11仍未授权。
- 后续LIA-126-024/S10B-R7已单独授权和消费；当前执行/退出见§29。Owner已接受DEC-126-064/065/066并完成§31的LIA-126-025/S10BO1 repository corrective及Corrective Closure；DEC-126-067进一步形成API/Host/Desktop/Infra/Governance本地clean checkpoints。`S10B-BLK-008 Closed`、G3 Partial，isolated live/fresh R8/S11仍未授权。

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
                                                     → S10A read-only readiness review
                                                          → S10P0 corrective design review
                                                               → S10E isolated environment
                                                                    → S10P1 fake-provider/child profile
                                                                         → S10P2 secure-storage isolation (historical source/HOLD)
                                                                              → S10P2F ephemeral local-only adjustment (DEC-126-043 accepted; BLK-004 closed)
                                                                                   → S10P3 Public Tasks main chain
                                                                                   → S10B first run (fail-closed)
                                                                                        → S10BP0 closed bootstrap design
                                                                                             → S10BP1 corrective implementation (separate authorization)
                                                                                                  → S10B fresh full rerun (R3 fail-closed)
                                                                                                       → S10BD0 capability/resolver corrective design
                                                                                                            → S10BD1 corrective implementation (separate authorization)
                                                                                                                 → S10B-R4 fresh full rerun (separate authorization)
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
| S10A | Local E2E readiness/test-profile review | AC-035–042 planning only | yijie docs + affected repos read-only | DESIGN-126-007、DEC-126-037、process/evidence matrix | process startup、flag、business source | DEC-126-036 + Owner S10A instruction | exact SHA/tool/source inventory + docs gates | no process/data mutation |
| S10P0 | Test Profile/Main-Chain Corrective设计评审 | S10A-BLK-001–005 planning only | yijie docs + affected repos read-only | DESIGN-126-008、DEC-126-038、closed config/schema/test/rollback | corrective source、environment mutation、activation | DEC-126-037 Accepted + Owner S10P0 instruction | exact baseline/source/environment inventory + governance gates | docs-only；无runtime rollback |
| S10E | Compose/isolated identity环境准备 | S10A-BLK-001 | yijie-infra + user-level Compose discovery | recoverable plugin link、run-scoped pinned PostgreSQL/Keycloak/Caddy/TLS profile | real DB/common volume/system trust/default profile | DEC-126-038 Accepted + separate S10E authorization | version/hash/config/digest/migration/identity/TLS/cleanup | restore link backup；stop only this run |
| S10P1 | Host fake-provider与Desktop child test profile | S10A-BLK-002/003 | Host/Desktop private deployment config | loopback fake Responses、exact test profile、child env/log/PID/nonce allowlist | MiniMax/default behavior、IPC/contracts/Runtime pin | S10E Closure + separate S10P1 authorization | protocol/nonloopback/default-off/no-log/crash/restart | master profile false；terminate only this run |
| S10P2 | test-only Keychain/app-data隔离 | S10A-BLK-004 | Desktop private storage/deployment | 双exact gate、run-derived Keychain services、app-data/Home/CODEX_HOME/project manifest、cleanup recovery | real/default namespace、Keychain enumeration、DB/private IPC schema | S10P1 Closure + LIA-126-010 | 仓内矩阵PASS；DEC-126-041 Option B接受source并保持Closure HOLD；signed Protected Data proof缺identity/profile/entitlement | historical native path现为Deferred Native Hardening；Local-only BLK-004改由S10P2F Closure关闭 |
| S10P2F | Local-only ephemeral secret backend调整（DEC-126-043 Accepted） | S10A-BLK-004 Closed | Desktop Rust test-only storage + tests | double-exact、canonical run UUID、CSPRNG三secret、0700/0600、O_EXCL/O_NOFOLLOW、restart/cross-run/exact cleanup/no-log | production/default Keychain、IPC/TS/Vue/SQLCipher业务schema、central/Host/API/Runtime | LIA-126-011 | `S10P2F-001–012`与Desktop全门禁PASS；Owner接受Closure | 独立flag false即回到Protected Data；只删manifest exact files；不承诺法证擦除 |
| S10P3 | Desktop→Public Tasks content-free主链 | S10A-BLK-005 | Desktop Rust/TS/Vue private domain | SQLCipher v5 binding/outbox、idempotent Public create、Host start sequencing、closed private projection | central contracts/Host wire/Runtime pin；Public row delete guess | DEC-126-038 retained-row boundary + DEC-126-043/BLK-004 closure + **separate S10P3 authorization** | migration/schema/serde/TS/auth/idempotency/race/no-log/retention disclosure | flags off；forward reader；never guess/delete Public row |
| S10B | 本地跨仓E2E/security/resilience/performance/delete rehearsal | all Must AC/NFR incl. AC-035–044 | API/Host/Desktop/pinned Runtime | local process harness/runbook/content-free evidence | production activation、real user data、tag/publish | BLK-001–005 closed + LIA-126-008 separately approved | S10B-001–012 full matrix | stop local processes；clean temp data；flags off |
| S10BP0 | Closed synthetic bootstrap corrective设计 | S10B-BLK-001 planning only | yijie docs + API/Infra read-only | DESIGN-126-009、DEC-126-047、LIA-126-013建议 | API/Infra/business source、container/service | DEC-126-046 Accepted + Owner S10BP0 instruction | source/ordering/contract-impact inventory + governance gates | docs-only；无runtime rollback |
| S10BP1 | Closed bootstrap profile纠偏 | S10B-BLK-001 | yijie-api + yijie-infra | exact profile/matrix、atomic four-manifest batch、closed verifier、权威wrapper、v4/idempotency/no-log evidence | generic API入口变化、feat125规则、manual SQL、central wire/schema | DEC-126-047 + LIA-126-013 | S10BP1-001–013 PASS；DEC-126-048 Accepted；BLK-001 Closed | disable/remove only new local profile command；保留既有profile |
| S10BR1 | Exact repository-digest availability纠偏 | S10B-BLK-002 | yijie-infra | 从Compose pin派生repository@digest、identity/mismatch负向、live no-pull up/stop | floating tag、pull、第二套pin、业务组件或S10B重跑 | DESIGN-126-010 + DEC-126-049 | DEC-126-050 Accepted；Closure Passed；BLK-002 Closed | 移除verifier调用并恢复旧precheck；不删保留volume |
| S10BD0 | Docker execution capability/resolver纠偏设计 | S10B-BLK-004 planning only | yijie docs + Infra read-only | DESIGN-126-011、DEC-126-054 Accepted、LIA-126-017建议、read-only差分 | Infra源码、Docker启动、container/create、S10B | DEC-126-053 Accepted + Owner S10BD0 instruction | source/error/order/identity/probe/cleanup/contract-impact inventory + governance gates | docs-only；无runtime rollback |
| S10BD1 | capability-first与immutable resolver纠偏 | S10B-BLK-004 | yijie-infra local test/deployment helper | closed capability/failure classifier、原pin exact identity、no-pull create/remove probe、负向/cleanup/no-log tests | pull/retag/restart/store switch/floating pin、业务源码、S10B | DEC-126-054 Accepted + LIA-126-017 consumed | S10BD1-001–012、live probe、Infra 99/99均PASS；DEC-126-055 Accepted | Closure Passed；BLK-004 Closed；HOLD S10B-R4 |
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
| S3 | prior remote `c000a0245acb5c3f7ead5d2a877fb60c281c588c` + sole candidate `29317b6426578749dc698fc2ad32b986ee5c8e9f` | source/fixtures/generated SDK/docs only | replacement post-commit gates PASS；old Draft PR remote CI audit FAIL；sole candidate clean-clone exact | DEC-126-023/024/Q-017 closed；G2A Re-review Passed | Complete at source/remote-candidate level；no merge/tag/publish/activation |
| S4 | remote candidate checkpoint `yijie-api@a64f9f591fb594818c1778e30c6941e2574b3264` | secure v2 foundation；default-off local-lab route；16 files | exact `29317b...` projection、generate drift、race/unit/lint、isolated PostgreSQL migration 1–4/integration PASS；audit/nil tenant/idempotency/content-free P1 closed | DEC-126-026 Accepted；Owner-authorized push后经`ls-remote`与clean clone复验 | Corrective Closure Passed / exact remote candidate；未merge/启用 |
| S5 | remote candidate checkpoint `yijie-agent-host@3e8df026110f0c895262329c2384d3896598f3d9` | Host/event v2 raw/title/cleanup foundation；flags off；11 files | contract/race/lint/fixed Runtime PASS；cleanup recovery/lease/title isolation+idempotency/receipt/schema/no-log P1 closed | DEC-126-026 Accepted；Owner-authorized push后经`ls-remote`与clean clone复验 | Corrective Closure Passed / exact remote candidate；未merge/启用 |
| S6–S8A | ancestor of remote candidate `yijie-desktop@35f27447398529cca4dec85fa1f67e779c7a7cbd` | SQLCipher v1–v4、Host/domain/application/actions/IPC/TS store；38 files；当时无Vue/router/style | exact `29317b...` projection、127 TS、93/94 Rust、clippy/fmt/build、migration/no-log/race/restart PASS | DEC-126-026/027/028/030/031 Accepted；最终S8B checkpoint经远端复验 | Closure Passed through S8A / included in exact remote candidate；未merge/启用 |
| S7A | included in `3adcb0380561c294412bc24767e4651ca872455a` | HostBridge、HostEventStream、strict typed domain、nonce-bound readiness与owner-only token；无Vue | S7A门禁与canonical reasoning/multi-frame chunk/fake Host/security/fault coverage PASS | DEC-126-027 Accepted | Closure Passed |
| S7B | included in `3adcb0380561c294412bc24767e4651ca872455a` | schema v3、transactional session/message/outbox、lease/unknown-outcome controls、coalesced reducer/terminal commit、20/50 history、title CAS；无Vue | `make lint/test/build` PASS；10,000 deltas、restart/mixup/reasoning reconciliation、fake Host→SSE→SQLCipher | DEC-126-028 Accepted | Closure Passed |
| DESIGN-126-005 | no implementation SHA | ConversationApplication/Tauri/TS gap inventory、private IPC v1、fixed fixture matrix与S7C/S8A/S8B重切 | feature docs validation | DEC-126-029 Accepted | Design Accepted；S7C/S8A later separately authorized |
| S7C | included in `3adcb0380561c294412bc24767e4651ca872455a` | schema v4、300s Rust-bound context/revision/capability facade、session/project actions、stable interrupt、durable cleanup/receipt、coordinator/restart/resync/live raw source；无Vue | `make lint/test/build` PASS；fake Host cleanup、v1-v4 migration、restart/idempotency/race/cascade/WAL/receipt-expiry/auth/no-log | DEC-126-030 Accepted | Closure Passed / G3 Partial |
| S8A | included in `3adcb0380561c294412bc24767e4651ca872455a` | 20 versioned commands、listen-only event、closed schema/fixtures、native auth binding、opaque cursors、strict TS validators/real Tauri client/authoritative Pinia reducer；无Vue | `make lint/test/build` PASS；127 TS；94 Rust（93 pass/1 existing ignored）；schema↔serde↔TS、auth/expiry/tenant、caps/backpressure/cancel/stale/restart/resync/no-log | DEC-126-031 Accepted | Closure Passed / G3 Partial |
| DESIGN-126-006 / DEC-126-032 | accepted design | S8B0 UI gate/route/lifecycle/store/readiness/tasks/scroll contract | feature package/static source inventory | DEC-126-032 Accepted | LIA-126-005 separately executed |
| S8B0 | ancestor of remote candidate `yijie-desktop@35f27447398529cca4dec85fa1f67e779c7a7cbd`（slice checkpoint `5dab02a1ad5f03fead236aa7060fa6a75a234d85`） | 22-command closed IPC、Rust readiness/storage probe、exact-off gate、routes/lifecycle/store/Tasks metadata；不含完整Chat Vue visual | 135 TS；96 Rust（95 pass/1 existing ignored）；generate/lint/type/build/fmt/clippy/no-log PASS | LIA-126-005 / DEC-126-033 | Closure Passed / included in exact remote candidate；未merge/启用 |
| S8B | remote candidate checkpoint `yijie-desktop@35f27447398529cca4dec85fa1f67e779c7a7cbd` | production Vue Chat/App Shell/composer/reasoning/menus/scroll/a11y；27 files | 164 TS、95/96 Rust、lint/build/audit/bundle/security/browser/axe PASS；VoiceOver checklist retained for S11/G6 | DEC-126-034 Accepted；Owner-authorized push后经`ls-remote`与clean clone复验 | Closure Passed / exact remote candidate；未merge/启用 |
| S9 | Host `8707dea552cff74121b89aa8045f27da2c8c9378`；Desktop `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb` | test-only runner/dataset/fixtures/consumer tests；production behavior unchanged | Host gates 250/250 title、210/210 valid raw、40/40 negative；Desktop exact fixture/history/delete/plaintext projection；repo gates PASS | LIA-126-007 executed；DEC-126-036 Accepted | Closure Passed；local only / not pushed |
| S10A | governance checkpoint | read-only repo/environment/source inventory + DESIGN-126-007/DEC-126-037/LIA-126-008 draft | docs/static checks only；no process startup | DEC-126-037 Accepted / Option C | Complete as accepted review / HOLD S10B |
| S10P0 | design checkpoint `514559265ac4a675115984650a0782f09b481748`；approval checkpoint待最终门禁后回报 | DESIGN-126-008 + DEC-126-038 Accepted；FEAT-126 governance files only | package/strict/G2A/YAML/lint/test/shell/diff gates PASS | Owner Accepted Option B | Design Accepted / no corrective implementation |
| S10E | yijie-infra `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf` | local checkpoint only | IMPLEMENTED / VERIFIED | DEC-126-039 Accepted / Closure Passed | S10P1 still requires separate Owner authorization |
| S10P1 | Host `e0a8d3d29a335571d1654d95e1e262c240755674`；Desktop `fba934c524852719904657d0a4155142040e7285` | exact/keyless loopback fake Responses、fixed fixture、Desktop closed child allowlist、bounded owner-only logs、spawn前PID/run/nonce evidence与Host parent watchdog；无IPC/TS/Vue/schema/pin变化 | CLOSURE PASSED | DEC-126-040 Accepted / BLK-002/003 Closed | S10P2仍需单独授权 |
| S10P2 | Desktop `c863b2ab30d185201bff5736a308d7078ee5dc68` | Desktop Rust test-only run manifest、double exact gate、run-derived Chat DB/receipt HMAC/native-auth Keychain namespaces、app-data/Home/project binding、exact inventory、cleanup/recovery/race；无IPC/TS/Vue/schema/pin变化 | source/repository gates PASS；signed Protected Data native write BLOCKED by missing identity/profile/entitlement | LIA-126-010 executed；DEC-126-041 Option B historical native HOLD；Local-only successor later closed BLK-004 under DEC-126-043 | Native hardening Deferred/NOT RUN；not S10P3 authorization |
| S10P2F | Desktop `46107eec1e9cba0257252cae8678a4233ef20036` | double-exact ephemeral backend、CSPRNG三secret、same-run恢复/cross-run隔离/exact cleanup | CLOSURE PASSED | DEC-126-043 Option A Accepted / BLK-004 Closed | Native hardening Deferred/NOT RUN |
| S10P3/S10I | Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c` + Infra `8d7c84dc963141931c6c5d3c3aded3218247df0b` local-only | SQLCipher v5、content-free Public create/bind-before-Host、outbox/recovery、closed IPC/TS/Pinia；dynamic numeric `AUTH_TIME`→`nbf` | repository PASS；standard native OIDC + unchanged API + real create/bind/delete-retention PASS | LIA-126-012 + DEC-126-044/045 Option A Accepted | Closure Passed；BLK-005 Closed；S10B unauthorized |
| S10BM1 | Infra `bb96333df908d6fea72ec0a1f57a64477c2428e4` | migration/bootstrap shared run-scoped full API SHA authority；Make/runbook/tests；无业务wire/schema变化 | Infra validate/lint/test 87/87、Node/shell/diff PASS；runtime resources=0 | LIA-126-015 Closure Passed；BLK-003 Closed | DEC-126-052 Accepted；no rerun authorization |
| S10B-R3 | approval baseline Governance `441663faf7d505015f03d572c8e9f30b3ba1a2df`；execution Governance `784c970a7d6330fc2c2432f0ae9bf7bca400b15c` | one-time fresh run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5` | S10B-001 FAIL；002–012 NOT RUN；resource containment PASS | LIA-126-016 consumed；S10B-BLK-004 Open；DEC-126-053 Accepted/Closure rejected | S10BD0 design only；no corrective/rerun；S11 remains separate |
| S10BD0 | Governance `784c970...` + existing uncommitted R3 overlay | read-only Infra source + Docker context/capability differential | current endpoint unavailable→generic verifier misclassification；0 source/container/service | DESIGN-126-011 complete；DEC-126-054 Accepted | LIA-126-017 Approved-Held-Not-Started；no S10B-R4 |
| S10BD1 | Governance execution baseline `075a5051…4484` + Infra `2a643cae…97a` | focused 12/12 + full 99/99 + exact-commit live run `12600000-0000-4000-8000-000000000055` | 3 immutable identities + 3 no-start probes PASS；post resources=0；Docker restored stopped | CLOSURE PASSED / DEC-126-055 ACCEPTED | BLK-004 Closed；no S10B-R4/S11 authorization |
| S10B–S11 | three S10B abort evidence sets | no business-source change during executions | R3 immutable-image preflight FAIL；S11 NOT RUN | S10B-BLK-001/002/003 Closed；004 Open | S11 not authorized |
| S10BP0 | current uncommitted yijie governance overlay | DESIGN-126-009 + DEC-126-047 Accepted + LIA-126-013 recommendation | package/strict/G2A/YAML/lint/test/diff；0 source/process | DEC-126-046/047 Accepted | Design Accepted；implementation/rerun not authorized |

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
| Local Implementation Authorization | 段成威 | S4–S9与S10E/P1/P2F/P3/S10BP1/S10BR1/S10BM1/S10BD1 Closure Passed；DEC-126-046–055 Accepted；S10B-BLK-001–004 Closed | 2026-08-05 | S10B-R4、S11/MiniMax/default activation与远端动作未授权 |

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
- `LIA-126-006 / S8B`结果：Owner在DEC-126-033接受后单独授权Vue页面、交互、视觉与可访问性；实现消费真实authoritative store，fake投影只存在test harness；DEC-126-034已接受Closure，feature flag activation不随之授权。
- S7C结果：Owner已接受DEC-126-030，S7C Closure Passed。
- S8A结果：20个versioned commands、closed Schema/fixtures、Rust-bound context/event/cursors、TS validator/client/store已实现；Desktop `make lint/test/build`及安全扫描PASS；DEC-126-031已接受S8A Closure，G3仍Partial。
- 当前状态：S4–S9与S10E/P1/P2F/P3/S10BP1/S10BR1/S10BM1/S10BD1 Closure Passed、BLK-001–005及S10B-BLK-001–004 Closed。LIA-126-016已消费且S10B-R3 Closure Fail；DEC-126-055 Accepted。S10B-R4/S11保持`NOT AUTHORIZED / NOT RUN`，signed Protected Data仍Deferred Native Hardening。

### LIA-126-005 / S8B0（Approved / Executed / DEC-126-033 Closure Passed）

- 授权来源：Owner明确批准DEC-126-032，并要求其后单独授权S8B0、不得直接进入S8B。
- 允许范围：Desktop private readiness/storage schema、Rust serde/commands/coordinator intent、TS validators/client/Pinia消费；exact-off UI gate、Chat/Tasks route和capability guard、permission bind/clear/dispose、project pick/revalidate、session追加分页、cleanup完成后的reload/clear/navigation disposition、production Tasks真实metadata/default-off。
- 禁止范围：完整Vue Chat页面/组件/视觉样式、App Shell项目/session树、composer、conversation flow、reasoning/menu/dialog/delete视觉交互及S8B a11y/visual实现；不得启用任何flag。
- 实施结果：`yijie-desktop@5dab02a1ad5f03fead236aa7060fa6a75a234d85`仅包含27个S8B0文件；新增2个closed commands后总数22，7个events不变；default-off gate、深链guard、permission lifecycle、store paging/project/readiness/cleanup与真实Tasks metadata接线完成；`sampleTasks`生产文件删除。
- 验证结果：135/135 TS，95/95 Rust（另1既有Keychain ignored），generate-check、lint、vue-tsc、Vite build、cargo fmt/clippy全绿；无production dependency、MiniMax、flag activation、central pin或远端动作。
- 环境：只使用fake Host、固定fixtures、临时SQLCipher/CODEX_HOME和test harness；不调用MiniMax或处理真实数据。
- 依赖/远端：不修改central contracts、Host/Public Tasks wire或Runtime pin；不新增production dependency；不push/merge/tag/publish/deploy。
- 退出：上述门禁与DEC-126-033 / S8B0 Closure Review已通过；Owner随后通过LIA-126-006单独授权S8B，没有把授权追溯写入S8B0本身。

### LIA-126-006 / S8B（Approved / Executed / DEC-126-034 Accepted）

- 固定基线：governance=`090f0b0a2351d4a144e823aebab64b5d762593b1`；Desktop=`5dab02a1ad5f03fead236aa7060fa6a75a234d85`；contracts=`29317b6426578749dc698fc2ad32b986ee5c8e9f`；开始时两仓干净。
- 允许范围：真实`/chat`/`/chat/:sessionId`、项目/session树、纯文本composer、assistant/raw reasoning、rename/pin/remove/delete、cleanup/paging/scroll、light/dark/zoom/keyboard/focus/a11y。
- 停止条件核对：无需新增/修改private IPC、Rust domain、central contract、Host wire或Runtime pin；因此未触发停止。
- 代码checkpoint：`yijie-desktop@35f27447398529cca4dec85fa1f67e779c7a7cbd`，parent=`5dab02a1ad5f03fead236aa7060fa6a75a234d85`，27个文件，工作树clean；后续经Owner明确授权push至专用候选分支并复验exact，仍未merge/启用。
- 依赖：仅新增fixed devDependency `axe-core@4.10.3`；lockfile已记录，npm audit 0 known vulnerabilities；production dependencies/bundle无axe。
- 验证：29/29 test files、164/164 tests、axe 0 serious/critical、lint/type/build、95/95 Rust（另1既有ignored）、1180×760 light/dark、200% zoom等价、dialog focus、reduced-motion/scroll unit及security/bundle scans PASS。
- 人工项：VoiceOver checklist已提交但未声称执行；DEC-126-034将其保留到S11/G6，不阻断S8B Closure。
- 限制：该切片完成时flag仍unset/false，且无MiniMax/真实数据/S9–S11/四组件E2E。后续Owner-authorized checkpoint push不改变此切片Closure；S9后来由LIA-126-007单独授权并完成候选，未追溯扩大S8B授权。

### DEC-126-035 Remote State Reconciliation（Accepted）

- 目的：只把Owner已明确授权并已发生的checkpoint push校正为可审计事实，不重开S4–S8B Closure，也不扩大G3/G4/G6。
- 只读证据：五个candidate refs经`git ls-remote`与临时single-branch/no-tags clean clone复验，HEAD分别为`650254b3c009c4098f7d7b2d415ed8082b0139fa`、`a64f9f591fb594818c1778e30c6941e2574b3264`、`3e8df026110f0c895262329c2384d3896598f3d9`、`35f27447398529cca4dec85fa1f67e779c7a7cbd`、`29317b6426578749dc698fc2ad32b986ee5c8e9f`；clone全部clean。
- 不变项：各`origin/develop`、Draft PR #1、历史`c000a024...`、sole contracts candidate内容、merge/tag/publish/deploy/feature activation均未改变。
- 本轮动作：仅更新FEAT-126 package并创建yijie本地治理checkpoint；不追加push，不修改API/Host/Desktop/contracts/Runtime源码。
- Owner结论：接受“remote exact candidate availability”；明确其不代表Code Complete、G4、G6、发布或生产启用。

### LIA-126-007 / S9 fake-provider Eval（Authorized / Executed / DEC-126-036 Accepted）

- Authority：`yijie-agent-host`持有版本化Eval runner与dataset manifest；`yijie-desktop`只消费相同fixtures做exact sequence/final/history/plaintext projection validation，不建立第二套评分authority。
- Pins：contracts=`29317b6426578749dc698fc2ad32b986ee5c8e9f`、Host=`3e8df026110f0c895262329c2384d3896598f3d9`、Desktop=`35f27447398529cca4dec85fa1f67e779c7a7cbd`、Runtime=`3aa317ce...`固定；不得修改wire/IPC/Runtime pin。
- Dataset：`feat126-title-raw-v1`固定200普通、50对抗、train=200/holdout=50；manifest/schema/dataset/split/runner/generator/fixtures的SHA-256由Host lock在每次运行前校验。
- Title gates：PASS；strict schema/sanitizer 250/250，语义200/200，unsafe拒绝50/50，late result覆盖用户rename=0，泄漏/额外actions=0。
- Raw gates：PASS；valid 210/210，missing/gap/invalid/oversize 40/40明确识别；delta/final exact，HTML/Markdown执行=0，Host log/bbolt和Desktop bundle正文泄漏=0。
- 环境与禁止项：仅fixed fake provider、fixed fixtures、临时SQLCipher/CODEX_HOME和合成数据；不调用MiniMax、不处理真实数据、不启用任何flag、不修改central contracts/Host wire/private IPC/Runtime pin、不执行远端写入、不进入S10。
- Checkpoints：Host `8707dea552cff74121b89aa8045f27da2c8c9378`；Desktop `adfdb5b24b3277ba39bd76a8cdc63fc138caf9cb`；均仅本地且未push。
- 退出：DEC-126-036 Closure Review已由Owner接受；S10仍须另行明确授权，S9授权不延伸到MiniMax、flag、真实数据或远端动作。

### LIA-126-008 / S10B 四组件本地E2E（Executed / Blocked / Closure Fail）

- 固定基线：Governance HEAD=`85a62835dd8f5993f5c98f8f6e89342c726914b6`加当前未提交审批校正；Contracts=`29317b6426578749dc698fc2ad32b986ee5c8e9f`；API=`a64f9f591fb594818c1778e30c6941e2574b3264`；Host=`e0a8d3d29a335571d1654d95e1e262c240755674`；Desktop=`ed9eb14f3829f6e8fee427de40f76a2c549fb78c`；Runtime=`3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`；Infra=`8d7c84dc963141931c6c5d3c3aded3218247df0b`。
- 当前结论：DEC-126-039/040/043/045已关闭BLK-001–005；Owner于2026-08-05单独批准并正式执行LIA-126-008。S10B在S10B-001发现approved bootstrap profile与isolated DB name不兼容，已按停止条件结束。
- 允许范围：只在owner-only临时目录、synthetic identities/tenant/project、fixed fake Responses provider和pinned Runtime上启动隔离依赖与API/Host/Desktop/Runtime，临时exact-true运行`S10B-001–012`，保留content-free evidence。
- 永久禁止：MiniMax/外部模型、真实key/真实数据/真实项目、`.env`/CI/default config开flag、mock Vue/单仓fixture冒充、跳过migration、复用真实DB/Keychain、修改fixed contracts/Runtime pin、远端写入、push/merge/tag/publish/deploy。
- 失败与退出：任一SHA/nonce/version/sequence/persistence/delete/content-free/no-log/default-off断言失败即停止全链，终止进程、保留最小content-free failure manifest、清理临时数据，不得通过重跑/降级断言直到绿灯。
- 执行语义：本批准只覆盖本次受控local test-profile执行；因S10B-BLK-001已消费并停止。它不是默认feature activation、G4/G6通过、MiniMax授权、S11授权或远端/发布授权。DEC-126-046 Option A已接受失败事实但拒绝Closure，不授权纠偏或重跑。

### DESIGN-126-008 / DEC-126-038（S10P0 design Accepted / no implementation authorization）

- 已完成：固定六仓exact/clean基线；盘点Compose/PostgreSQL/Keycloak/Caddy/TLS、Host provider、Desktop child/Keychain和Public Tasks主链；冻结S10E/P1/P2/P3影响、schema、测试与回滚。
- 本轮未执行：未修plugin link，未安装/下载/启动，未改Infra/API/Host/Desktop/Runtime/contracts业务源码，未碰Keychain/DB，未开flag，未远端写入。
- 决策结论：Owner已接受Public Tasks candidate无delete API，即本地session删除后PostgreSQL content-free row保留；未来若要求该row同删，必须重开G2A缺口。
- 授权原则：DEC-126-038不自动开始任何切片；下列候选仍须Owner逐条授权。

### S10E Compose / Isolated Identity Environment（DEC-126-039 Accepted / Closure Passed）

- 已实现：旧stale symlink移入owner-only备份，当前用户CLI恢复到固定Docker Desktop bundled Compose v5.3.0；完整SHA-256、config与`--wait` capability均通过，未改系统目录/Docker Desktop app。
- 已实现：新`feat-126-s10` default-off Infra profile/runbook/static+runtime validators；两个pinned PostgreSQL、pinned Keycloak/Caddy、四个run-scoped volumes、loopback ports、empty migration、synthetic identity与API-local public CA。普通volume/DB和production/default profile不变。
- 网络结果：所需exact image content均已本地存在，使用`--pull never`，下载/pull=0；PostgreSQL exact content只补固定本地tag。API DB为Docker Desktop loopback publisher加入project-scoped host bridge，但仍只绑定127.0.0.1且无host/shared network。
- 交付：Infra本地checkpoint `99e50d8b47e13fc3e3b7501617a307e1ba5d6baf`；static 80/80、migration v4/idempotency、identity/TLS/runtime/no-log/rejected-run/stop验证PASS；未push。八个named volumes与两个owner-only run root因无删除授权而保留，污染run由`REJECTED` marker阻止复用。
- 边界：DEC-126-039只接受S10E并关闭BLK-001；本节不授权S10P1或S10B。

### S10P1 Host fake-provider / Desktop Child Profile（LIA-126-009 Executed / DEC-126-040 Accepted）

- 已实现DESIGN-126-008 exact master profile、canonical run ID、loopback-only fake Responses HTTP authority、managed CODEX_HOME no-key config，保持model/provider on-wire identity与Runtime pin不变。
- Desktop `env_clear()`后只传closed child allowlist；raw/cleanup exact true、title false；Host log/PID/nonce只进owner-only run root与content-free manifest，日志每stream上限256 KiB。
- 未改private IPC/central contracts/Runtime pin；停止条件未触发。Host/Desktop local checkpoints及fixed Runtime/fault/restart/default-off/no-log证据均PASS；未push。
- DEC-126-040已接受并关闭BLK-002/003；S10P2仍不得自动开始，必须另行明确授权。

### S10P2 Test-only Secure Storage（LIA-126-010 Executed / DEC-126-041 Option B Accepted / Closure HOLD）

- Desktop `c863b2ab30d185201bff5736a308d7078ee5dc68`已实现独立secure-storage exact gate；master-only/default/false继续走固定namespace，typo/orphan fail closed。
- Rust从canonical run ID派生Chat DB、receipt、native-auth三个Keychain service；test native-auth不构建legacy entry；Chat app-data、Host Home、CODEX_HOME与project绑同一closed run manifest。
- exact inventory使用属性搜索且只查3组service/account，不枚举Keychain、不读或hash secret；异常退出/中断/missing/restart只按匹配manifest删本run entries，mismatch delete=0。
- 仓内12项S10P2测试与Desktop全门禁PASS；未改SQLCipher schema/private IPC/central contracts/default namespace/依赖，未push。
- 随机原生probe确认pre/post exact tuples全absent、临时root已删除，但Protected Data首次写入因required entitlement missing失败。Owner已接受DEC-126-041 Option B与源码checkpoint；该历史native Closure保持HOLD，Local-only BLK-004后来由DEC-126-043接受S10P2F Closure而关闭。
- 历史退出条件：DEC-126-041原要求匹配local bundle/access-group的Apple Development identity/provisioning并重跑native矩阵；DEC-126-042现已将其移为Deferred Native Hardening，不再作为Local-only前置。BLK-004改由S10P2F Closure关闭。
- 签名准备盘点：bundle=`com.yijie.ai`；codesigning identity=0；installed provisioning profile=0；仓库entitlements/profile=0；active developer directory仅Command Line Tools。因Team/ApplicationIdentifierPrefix不可验证，本次未创建CSR/profile/entitlements或Keychain item，write attempt仍为2。

### LIA-126-011 / S10P2F Local-only Ephemeral Secret Backend（DEC-126-043 ACCEPTED）

- 固定基线：Governance `a5c5dde554aed38fba9390514b3c3f62a8c0ae04`，Desktop `c863b2ab30d185201bff5736a308d7078ee5dc68`；checkpoint `46107eec1e9cba0257252cae8678a4233ef20036`，contracts/Host/API/Runtime/Infra pins不变。`contract-impact=semantic`仅限Desktop-private local-test storage/deployment；central G2A=N/A。
- 仅6个Rust文件实现两个exact-true gate、canonical UUID、schema-v2 closed manifest、owner-only temp root、CSPRNG三secret、create-new/O_EXCL/O_NOFOLLOW、owner/mode/nlink/inode/device/canonical/schema、same-run SQLCipher/native-auth restart、cross-run/lease/crash/recovery、exact non-recursive cleanup与no-log。
- production/default protected schema v1与selector保持不变；没有修改private IPC/Tauri command/event、TypeScript/Pinia/Vue、SQLCipher业务schema、central contracts、Public Tasks/Host wire、API、Host、Runtime pin、依赖或`.env`/CI/build default。
- S10P2F-001–012、全量Rust 124 pass/2 native ignored、TS 165、lint/build/security/bundle/diff均通过；Keychain/MiniMax/真实数据/远端写入为0。授权范围内P1为0。
- Owner已接受DEC-126-043 Option A并关闭Local-only BLK-004。该决定不授权开始S10P3/S10B；Apple signed Keychain只能登记`Deferred Native Hardening / NOT RUN`，未来native signing/production activation前重新阻断。

### S10P3 Desktop → Public Tasks Main Chain（DEC-126-045 ACCEPTED / CLOSURE PASSED）

- LIA-126-012实现保存于Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`。Owner接受DEC-126-044 Option A并授权S10I后，Infra `8d7c84dc963141931c6c5d3c3aded3218247df0b`用Keycloak内置动态mapper补齐numeric `nbf`，API verifier保持不变。
- 只实现SQLCipher v5 content-free binding/outbox、Rust-native bearer/tenant/revision authority、先Public create/bind再Host start的幂等编排，以及`chat_get_session_control_plane_v1`/`yijie.chat.control-plane.event.v1`的closed Rust↔schema↔TS↔Pinia/UI消费。
- request/response/PostgreSQL/audit只能是既有closed metadata/reference；prompt/message/raw/title/path/bearer不得离开Desktop SQLCipher/Rust authority。不修改`29317b...`、API/Host wire或Runtime pin。
- 删除只清Desktop/Host/Runtime和local binding；Public Task row保留且必须证明正文零命中。若实现需Public delete或其他central shape，立即停止转G2A。
- 已完成：v1–v4→v5 migration、schema/serde/TS conformance、fixed auth/idempotency/unknown/restart/delete-race/no-log与仓内门禁；当前变更保持未提交，未创建完成checkpoint、未push。
- 已完成：fresh isolated run的standard Authorization Code + PKCE、capability、真实201/Public bind、本地delete/Public row retained，以及PostgreSQL task/audit正文/路径零命中；fixed error/unknown matrix继续由仓内测试覆盖。无手工bearer、mock signer或curl替代。
- Owner结论：DEC-126-045推荐方案A已批准，S10P3 Closure Passed，BLK-005 Closed；Owner随后单独批准并执行LIA-126-008。历史S10B-BLK-001/002由DEC-126-048/050关闭；Owner再单独授权LIA-126-014，但S10B-R2在新BLK-003处停止，Closure仍未通过。

### DESIGN-126-009 / DEC-126-047（Accepted Option A）

- 已完成：只读确认API profile validation先于manifest读取和数据库连接；现有`feat-125-local-lab`严格绑定`yijie_api_feat125_local`，generic nonproduction兼容路径独立保留；Infra当前没有S10 bootstrap权威命令。
- 冻结方案：新增API私有`feat-126-s10-local-lab`精确绑定nonproduction、local issuer和`yijie_api_feat126_s10` DSN；复用existing four reviewed manifests；Infra新命令内部固定profile与四条显式路径，不给调用方generic/override入口。
- 冻结结果：fresh migration v4；first pass精确2 users/2 identities/2 tenants/4 memberships/4 assignments；second passrevision不变且audit总数8；失败不留partial state；DSN/secret/token/manifest正文输出命中0；feat125与generic lane全回归。
- contract-impact：central contracts/G2A=`none/N/A`；只允许API+Infra local deployment/security profile additive change。任何central wire、verifier、schema、Desktop/Host/Runtime或现有profile变化立即停止。

### LIA-126-013 / S10BP1 实施与Closure（AUTHORIZED / EXECUTED / ACCEPTED）

- API已增加新closed profile、exact ordered matrix、API-owned atomic batch、empty/complete verifier及正负/回归测试；现有profile/generic语义与manifest字节未改。
- Infra已增加run-scoped、不可caller override的bootstrap命令；固定full API SHA/clean、profile/issuer/DSN/四路径，输出0600 content-free count/revision/audit摘要。
- `S10BP1-001–013`、API全量/integration、Infra 83/83/static/security及fresh-v4 run均PASS；临时容器、anonymous volume、secret和candidate已清理。
- Owner已接受DEC-126-048 Option A，S10BP1 Closure Passed并关闭S10B-BLK-001；该决定不授权S10B rerun。
- 验证发现的独立`S10B-BLK-002`已在DESIGN-126-010/DEC-126-049单独评审并实现：保留Compose version+digest authority，以派生的repository@digest做local availability验证，继续`--pull never`。Infra自动化和fresh四依赖no-pull up/stop通过，Owner已接受DEC-126-050 Closure并关闭BLK-002；fresh S10B rerun仍须另行授权。

## 17. LIA-126-014 / S10B-R2执行与退出

- Owner已单独授权一次fresh S10B-R2。开始前完成三项仅本地checkpoint：Governance `9db41b03072f5d427c61fa832d22e94f3e8ce02c`、API `c5f334e88d54d9e04f388d0349f4f5925124abd6`、Infra `597acb34588cc519d2482bffbf4fb3298bacc734`；Host/Desktop/Runtime/Contracts保持既有clean pin；未push。
- S10B-001在资源创建前执行权威migration preflight。Infra wrapper仍固定旧API `a64f9f...`，与当前必须使用的closed bootstrap API `c5f334e...`不一致，因此run `4ffa07b9-6e4c-45d4-b5d5-3b3be5d7d818`按设计fail closed。
- S10B-002–012未运行；run root、secret、container、network、volume、数据库、API/Desktop/Host/fake/Runtime均未创建或启动。没有需要删除的run资源。
- 登记`S10B-BLK-003`。Owner已接受DEC-126-051并拒绝Closure；不得现场替换hardcoded SHA、退回旧API、绕过wrapper或直接重跑。Owner随后单独授权LIA-126-015，纠偏结果见§18。
- 当前下一步不是S11、MiniMax smoke或自动S10B重跑。DEC-126-055已关闭BLK-004；若要执行一次fresh S10B-R4，必须另行形成并获得明确授权。G3保持Partial，G4/G6 Pending。

## 18. LIA-126-015 / S10BM1执行与退出

- 授权范围：只纠正migration/bootstrap共享完整API SHA authority；不启动容器、服务或S10B，不修改API/Desktop/Host/Runtime/contracts/wire/schema/default flag。
- 实现：migration Make target和wrapper新增强制`API_SHA`；migration/bootstrap统一调用run-scoped authority helper。helper校验canonical run、0700 owner-only root、exact clean API HEAD，并以create-new/O_EXCL/O_NOFOLLOW创建0600 closed document；另一命令只能复用同一run/SHA。
- 兼容：private FEAT-126 migration helper属于有意breaking；旧两参数调用fail closed。central contract/G2A、production/default配置与现有feat125 profile无变化。
- checkpoint：`yijie-infra@bb96333df908d6fea72ec0a1f57a64477c2428e4`，仅本地、未push、工作树clean。
- 验证：Infra validate/lint/test 87/87、Node/shell syntax、diff与负向authority矩阵PASS；container/service/secret/DB/model/Keychain/remote write均为0。
- 退出：DEC-126-052 Option A已接受，BLK-003 Closed。该接受不自动重跑S10B；先形成clean Governance SHA，再单独授权LIA-126-016。

## 19. LIA-126-016 / S10B-R3执行与退出

- 状态：`CONSUMED / EXECUTED-BLOCKED / CLOSURE FAIL`；批准基线Governance=`441663faf7d505015f03d572c8e9f30b3ba1a2df`，执行provenance Governance=`784c970a7d6330fc2c2432f0ae9bf7bca400b15c`。
- 授权：只执行一次全新的S10B-001–012，不进入S11、不调用MiniMax；执行前必须重新确认七仓exact clean并记录本次授权checkpoint HEAD。
- 固定pin：Contracts `29317b...e9f`、API `c5f334e...abd6`、Host `e0a8d3...5674`、Desktop `ed9eb14...78c`、Runtime `3aa317...d6f`、Infra `bb96333...28e4`；Governance Closure checkpoint=`441663faf7d505015f03d572c8e9f30b3ba1a2df`。
- 执行边界：new canonical run/fresh volumes+roots+secrets+token+project、fake loopback provider、temporary exact-true flags、真实Vue/Pinia/Tauri/Desktop/API/Host/Runtime主链；不得用curl、手工SQL、mock UI或旧run替代。
- 停止：任一precondition、SHA、identity、migration、authority、no-log、cleanup或用例失败立即停止并登记新blocker；不得现场修复或直接重跑。
- 实际执行：七仓exact-clean、Compose 5.3.0、Docker 29.6.1、受控端口空闲、ignored secret init与Compose config通过；accepted image verifier随后无法直接inspect冻结PostgreSQL `repository@digest`，在Compose up前fail closed。
- containment：为run `6c1d8652-7b99-4ca8-8c0e-f9a61e7ca4a5`写入owner-only `REJECTED`，执行exact stop；container/network/volume/listener=`0/0/0/0`，ignored run root与secret record保留。未调用MiniMax、未访问Keychain/真实数据、未修改源码或远端。
- 退出：S10B-001 FAIL，002–012 NOT RUN；登记新独立`S10B-BLK-004`。Owner接受DEC-126-053/054后又明确开始并消费LIA-126-017；S10BD1证据现已通过。BLK-004仍等待DEC-126-055 Owner决定；不pull/retag/重启Docker workaround、不重跑、不进入S11。

## 20. DESIGN-126-011 / S10BD0退出与后续授权建议

- 只读事实：现有verifier在Docker endpoint/socket不可达时仍返回generic image-unavailable；本轮未启动Docker Desktop。此前获准只读上下文中正确PostgreSQL exact pin可解析，故不能把R3永久归因于Docker 29.6.1或digest内容错误。
- 设计冻结：capability-first、closed/content-free failure classes、原Compose pin的Id/Descriptor/RepoDigests/repository/platform校验，以及单独授权的`docker create --pull=never`创建但不启动/精确清理probe。
- 分类：S10BD0 docs-only=`none`；已实施S10BD1为local deployment-interface `semantic`；central contracts/HTTP/SSE/private IPC/DB schema/Runtime pin均`none`，G2A=N/A。
- 交付：DESIGN-126-011完成；DEC-126-054 Option A已Accepted；`LIA-126-017 / S10BD1`已消费并完成，Infra clean checkpoint与live证据已固定；DEC-126-055待Owner。
- 退出链：DEC-126-054 Accepted → LIA-126-017 explicit consumption → Infra实现/测试/live probe PASS → DEC-126-055 Owner Accepted → BLK-004 Closed。当前停在“等待新的S10B-R4单独授权”，不得自动跳过。

## 21. LIA-126-018 / S10B-R4执行与退出

- 状态：`CONSUMED / EXECUTED-BLOCKED / CLOSURE FAIL`。固定七仓基线与工作树均精确通过，run=`96a0a80d-27d4-4022-a470-4a7f004d9c4c`。
- S10B-001已完成S10BD1 Docker capability/identity/resolver、fresh隔离依赖、TLS/OIDC、synthetic users、migration v4、closed bootstrap与API readiness；没有复用历史run、volume、token或状态。
- fake-provider readiness失败：Host source固定请求fixture为`normal-000`，本次手工编排却使用S9 dataset bundle名称`feat126-title-raw-v1`。正确canonical run ID下返回403，因此停止；先前一条run-header大小写漂移请求同样被拒绝，只作为负向记录，不作为readiness证据。
- 停止边界：没有改成`normal-000`后继续，没有启动Host/Desktop/Runtime，没有进入S10B-002–012，没有调用MiniMax/外部模型或访问Keychain/真实数据，也没有修改源码、schema、wire、pin、默认flag或远端。
- cleanup：API/fake停止；四container和四network移除；受控端口释放；临时process root删除；Docker恢复执行前stopped；四named volumes和ignored Infra run record按既定边界保留。
- 登记`S10B-BLK-005`：S10B手工步骤没有单一machine-readable fixture/orchestrator authority，S9 bundle identity与Host request fixture identity可被混用。contract-impact=`none`（本轮仅执行/治理事实），central G2A N/A。
- DEC-126-056 Option A已接受：接受fail-closed事实、拒绝S10B-R4 Closure并单独授权S10BF1。不得现场修正或把corrective当R5。

## 22. LIA-126-019 / S10BF1执行与退出

- 实现边界：Host-only test readiness authority/probe + Infra唯一组合runner；未修改业务行为、contracts、IPC、schema或Runtime pin。
- checkpoint：Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`；Infra `5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`；Governance执行基线`db12fe6ce4a8c1f84ac90781191d8a1b26dbcc4d`。
- authority：Host内部选择case并输出明确的dataset/case/digest；Infra和操作者没有dataset/fixture参数，所有headers由probe生成。
- 验证：Host full race/contract/lint PASS；Infra 103/103 + validate/lint/diff PASS；fresh run `ed22fc82-4837-4a3e-a60e-7f7c8ab6f3f4`完成七SHA、resolver、dependencies、identity、migration/bootstrap、API/fake readiness与no-log。
- cleanup：API/fake、container、network、listener归零；4 named volumes/ignored run record披露；Docker恢复stopped；summary=`8198442e…f7d9`且明确`S10B-R5=false`。
- 退出：DEC-126-057 Option A已接受，S10BF1 Closure Passed且BLK-005 Closed。仍不得自动执行S10B-R5/S11/MiniMax或远端动作；fresh R5必须另行明确授权。

## 23. LIA-126-020 / S10B-R5执行与退出

1. 一次性授权已由fresh run `24ae14b7-46d1-4fd5-a7ac-a30932586ad6`消费。
2. S10B-001通过；S10B-002在API readiness前因`feat-125-local-lab`与冻结的`feat-126-s10-local-lab`runtime authority冲突而停止；003–012未运行。
3. 当前唯一允许的下一动作是Owner评审DEC-126-058。不得把文档候选当作corrective授权。
4. 若Owner接受Option A，后续仍须依次完成：closed runtime-profile设计评审 → 单独corrective LIA → corrective Closure → 新clean checkpoint → 单独fresh E2E授权。任何一步都不自动导出下一步。
5. 本轮没有业务源码checkpoint；只允许形成FEAT-126治理文档本地checkpoint，不push。

## 24. LIA-126-021 / S10BRP1执行与退出

1. Owner最新明确指令接受DEC-126-058 Option A，并授权、消费本切片；范围仅为API closed runtime profile、Infra单一authority/preflight/continuation接线、测试与治理。
2. API在既有`c5f334e88d54d9e04f388d0349f4f5925124abd6`之上增加`feat-126-s10-local-lab`严格分支；不得改写`feat-125-local-lab`或default语义，不得放宽secure route、issuer、DSN、CA或loopback边界。
3. Infra在既有`5723ffdaa3f2c4b63914a6fd6ef7bac9f15bc0c9`之上建立唯一closed authority。组合preflight、machine-readable summary和唯一`make feat-126-s10b-api-continuation`由同一module/commit连接；launcher只收run ID与七仓SHA并从固定run路径读取安全工件，operator不能提供profile、endpoint、database、issuer、gate、binary、path或secret override。
4. 验证包括API lint/full tests及FEAT-125回归，Infra validate/lint/full 113/113 tests、authority/summary/artifact负向矩阵、preflight `api_binary_sha256`绑定、binary drift拒绝与launcher真实子进程消费/exit-code传播。任何需要修改central contracts、业务wire/schema、Desktop IPC或Runtime pin的缺口立即停止。
5. 当前Accepted clean local checkpoints为API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`与Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`，均未push；本轮不启动Docker/服务，不执行S10B-002–012，不进入S11或调用MiniMax。
6. DEC-126-059 Option A已接受，`S10B-BLK-006` Closed；该接受不等于S10B或G4 PASS。

## 25. LIA-126-022 / S10B-R6 授权消费结果

1. 状态：`Consumed 2026-08-06 / Executed-Blocked / Closure Fail`；fresh run为`28afba8b-573a-46ec-b9d1-8a635c7b9cf0`。
2. 固定候选：Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`与本次Governance clean checkpoint。
3. 唯一`make feat-126-s10b-preflight`返回`preflight_image_resolver_failed`；S10B-001 FAIL，S10B-002–012 NOT RUN。
4. 已按硬门禁停止；未现场修改源码、继续、直接重跑或转入S11。
5. 不授权MiniMax、真实数据/Keychain、default activation、push、merge、tag、publish或deploy。

## 26. S10B-BLK-007 退出顺序

1. DEC-126-060 Option A已Accepted：确认R6失败事实并拒绝Closure，不自动授权纠偏。
2. Owner已单独授权并完成DESIGN-126-013/S10BEP0设计评审；DEC-126-061 Option A于2026-08-08获批。父runner只能消费closed/versioned/content-free子结果，禁止raw stderr或路径/命令正文。
3. `LIA-126-023 / S10BEP1` Infra corrective已单独授权、消费并完成repository实现；S10BEP1-014 isolated live验证及Infra/Governance全量门禁已PASS。不得改变Compose pins、`--pull never`、contracts、业务wire/schema或Runtime pin。
4. corrective Closure已由Owner通过DEC-126-062接受并关闭BLK-007；DEC-126-063已仅形成clean Infra/Governance checkpoints。fresh R7仍须另行授权。

## 27. S10BEP0/S10BEP1切片

| Slice | 范围 | 允许仓库/文件 | 前置 | 验证 | 状态 |
|---|---|---|---|---|---|
| S10BEP0 / DESIGN-126-013 | 只读调查、closed result v1、failure mapping、安全/兼容/测试冻结 | yijie治理文档 | DEC-126-060 Accepted + Owner单独授权设计评审 | package/strict/G2A/YAML/lint/test/diff | **Completed / DEC-126-061 Accepted** |
| S10BEP1 / LIA-126-023 | resolver closed child mode、parent strict projection、0600 evidence、directional tests与单独live closure | yijie-infra resolver/preflight/tests/docs + yijie治理 | DEC-126-061 Accepted + Owner明确实施授权 | S10BEP1-001–014 + Infra full gates + isolated live resolver | **Corrective Closure Passed / DEC-126-063 Clean Checkpoints Formed / S10B-BLK-007 Closed** |
| S10B-R7 / LIA-126-024 | fresh S10B-001–012 | 固定七仓clean checkpoints | S10BEP1 Closure由Owner接受 + 独立一次性授权 | 完整权威矩阵 | **Consumed / S10B-001 PASS / 002 FAIL-CLOSED / Closure Rejected** |
| S10BO0 / DESIGN-126-014 | 四组件closed orchestrator只读设计 | yijie九份治理文档 | DEC-126-064 Option A Accepted + Owner仅授权设计评审 | Governance全量门禁 | **Complete / DEC-126-065 Accepted Option A** |
| S10BO1 / LIA-126-025 | Infra/API/Host/Desktop repository corrective | Infra/API/Host/Desktop；Contracts/Runtime源码不变 | DEC-126-065 Accepted + Owner明确实施授权 | S10BO1-001–014 + 四仓lint/test/build + Governance | **Corrective Closure Passed / DEC-126-067 Local Clean Checkpoints Formed / S10B-BLK-008 Closed** |

停止条件：S10BEP1如需改API/Host/Desktop/Runtime/contracts、业务wire/schema、Compose pin或引入operator可选resolver参数，立即停止并提交新设计缺口；不得把unit test、human CLI或单独live resolver写成S10B-R7/G4证据。

## 28. LIA-126-023 / S10BEP1执行与退出

1. Owner于2026-08-08接受DEC-126-061 Option A并单独授权执行corrective；授权范围只含Infra resolver/preflight/tests/docs与FEAT-126治理。
2. 实现已完成closed result v1、同源枚举/显式合法tuple validator、12 leaf映射与cleanup leaf保留、namespace protocol guard、fixed child process、120秒timeout、2048/4096容量、strict UTF-8/单末尾LF/duplicate-key/framing/exit/stderr/run binding、create-new 0600 evidence、closed resolver后config recheck→fixed direct up顺序与human CLI兼容。
3. Infra 128/128 tests、`pnpm validate`、targeted 34/34 S10BD1/S10BF1/S10BEP1、Node syntax/diff与完整`make lint/test` PASS；未修改Compose pin、API/Host/Desktop/Runtime/contracts、business wire/schema或默认flag。
4. Docker client/server 29.6.1、Compose 5.3.0与daemon access通过后，canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`完成isolated 3 identity/3 no-start probe、exact closed parent、0600 evidence、no-log与资源归零；三项exact image identity前后一致且image count均为6，`s10b_r7_executed=false`。Governance default/strict/G2A/YAML/lint/test/diff PASS。
5. DEC-126-062已接受S10BEP1 Corrective Closure并关闭`S10B-BLK-007`；DEC-126-063已形成Infra checkpoint `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`及包含本决策的Governance本地checkpoint。fresh R7仍须Owner明确授权；当前为Not Authorized。

## 29. LIA-126-024 / S10B-R7执行与退出

1. Owner单独授权并消费一次fresh S10B-001–012；固定七仓为Governance `3d82cda4c3c06928e0111bc1697b0153e8ef76a2`、Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Host `1ca4ee555586e5243f7101b9fe056c6fa117a560`、Desktop `ed9eb14f3829f6e8fee427de40f76a2c549fb78c`、Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`与Infra `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`；执行前均exact/clean。
2. Docker client/server 29.6.1、Compose 5.3.0与daemon access PASS。canonical run `d553e6ea-e10f-4470-b357-a41807d6fb06`的唯一preflight PASS，故S10B-001 PASS；authorization不得复用。
3. continuation authority复核发现唯一Infra launcher只启动API，且runbook明确不启动Compose/其他组件；治理process manifest仍为不可执行候选，七仓不存在完整四组件S10B-002–012 orchestrator。S10B-002因此在continuation与业务进程启动前fail closed；003–011未运行，012只执行abort cleanup subset。
4. exact stop后run container/network/process/listener均0；4个named volumes、ignored run root和content-free artifacts保留；daemon为6 containers/0 running/6 images。8个日志/证据对5个生成secret及664个冻结payload值命中0；未retry、prune或删除volume。
5. 登记`S10B-BLK-008 Open`；Owner已接受DEC-126-064 Option A，确认fail-closed事实并拒绝R7 Closure，只授权后续DESIGN-126-014设计评审。`s10b_r7_executed=true`，但R7 Closure/G4/G6均未达到；不commit、不自动corrective、fresh R8、S11或任何远端动作。

## 30. DESIGN-126-014 / S10BO0设计评审退出

1. 只读核对Governance、Infra、API、Host、Desktop与Runtime后，确认完整corrective必须涉及Infra、API、Host与Desktop；Contracts及Runtime源码保持不变。
2. 唯一入口固定为`make feat-126-s10b-orchestrator`，operator只提供canonical run ID与七仓full SHA；入口内部消费same-run preflight，并按Infra→Desktop→Host→Runtime现有所有权链运行closed S10B-002–012 state machine。
3. 设计冻结test-build-only Desktop真实Vue/Pinia/Tauri driver、synthetic authorization-code+PKCE和固定project校验、Host-owned Runtime/fake generation evidence、API-owned content-free Tasks/audit/idempotency verifier，以及版本化证据、no-log、PID reuse/parent-death containment与精确cleanup。
4. `DESIGN-126-014 Complete`；设计评审contract-impact=`none`。已实施corrective为private local test/deployment和Desktop test-driver IPC `semantic`，central contracts/G2A=`N/A`；未发现public wire或durable schema影响。
5. Governance default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax与`git diff --check`首轮及证据登记后复跑均PASS。
6. `DEC-126-065 Accepted Option A`并授权`LIA-126-025/S10BO1`四仓repository corrective。实施授权已消费，但不授权isolated live、fresh R8、S11、MiniMax、真实数据/default activation、commit或远端动作。

## 31. LIA-126-025 / S10BO1 执行与退出

1. 前置七仓HEAD与clean/scope核对通过；Contracts及Runtime保持exact clean，Governance只修改既有九份FEAT-126文件。
2. Infra、API、Host、Desktop按DESIGN-126-014完成repository corrective；未修改central contracts、Runtime源码、公共wire、durable schema、Compose pin或默认flags。
3. 最终能力前置PASS：Docker client/server `29.6.1`、Docker Compose `5.3.0`、daemon access、loopback listener、0700/0600临时文件、subprocess、native project bookmark及SQLCipher/file-security测试均可用。
4. API与Host完整lint/race/build PASS；Desktop frontend lint、30个TS文件/167 tests、Rust 129 PASS/3明确ignored、production build、default build/clippy、feature build/clippy、driver tests 2/2及production bundle driver-absent全部PASS；Infra validate、完整lint/test、Compose semantic、142/142及独立S10BO1-001–014 14/14全部PASS。
5. Desktop首次default clippy发现`run_id`与`validate_fixed_project`仅由feature driver消费却未使用同源feature cfg；按Owner单独授权的最小`contract-impact=none`修复为两个方法增加`#[cfg(feature = "feat126-s10-driver")]`，随后default/feature全套回归PASS。
6. Governance default/strict/G2A、unique-key YAML、`pnpm lint/test`、checker shell syntax及所有受影响仓库`git diff --check`最终复跑PASS。
7. DEC-126-066已接受`LIA-126-025/S10BO1 Corrective Closure`并关闭`S10B-BLK-008`。G3保持Partial，G4/G6 Pending；不得commit或开始isolated live/fresh R8。
8. 本次Owner接受不自动形成clean checkpoint、isolated live或fresh R8授权；任何后续阶段仍需新的明确授权。
9. 决策后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax及`git diff --check`均已复验PASS。

## 32. DEC-126-067 / Local Clean Checkpoint执行与退出

1. 执行前七仓HEAD与变更范围精确匹配；Contracts与Runtime保持clean，未发现范围外变更。
2. API/Host/Desktop/Infra完整门禁、S10BO1-001–014 14/14、Governance全门禁和七仓`git diff --check`全部PASS后才开始commit。
3. 形成API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`、Desktop `d51e435cb8ea224e69f9707831ee71022d0a7b6e`、Infra `0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c`四个本地clean checkpoints。
4. Governance仅更新既有九份FEAT-126文件，登记上述SHA与DEC-126-067；Governance checkpoint为包含本节的本地commit。
5. `S10B-BLK-008 Closed`、G3 Partial、G4/G6 Pending不变；未执行isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认启用、prune、volume删除或远端写入。

## 24. LIA-126-026 / S10BO2 实施结果与下一门禁

1. DEC-126-068 Option A已接受，DESIGN-126-015完成；Desktop + Infra repository corrective已按所有权链实现。
2. Desktop全量/default/feature/driver/production-absent门禁PASS，形成checkpoint `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`。
3. Infra validate/lint/test 162/162与S10BO1/S10BO2 targeted 34/34 PASS，形成checkpoint `0fed8187d6051c011e67142d90feff89de326cfe`。
4. 治理门禁通过后，本轮Owner明确授权将Governance、API、Host、Desktop与Infra现有FEAT-126提交推送至各自候选分支；Contracts/Runtime无新提交，不创建空commit。
5. Owner已接受S10BO2 Corrective Closure并关闭`S10B-BLK-009`；G3保持Partial、G4/G6 Pending。下一阶段不得自动启动，isolated live和fresh R8仍需各自独立授权。
6. Owner决定登记后的Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`首轮及证据回填后最终复跑均PASS；治理变更保持本地未提交状态。

## 25. LIA-126-027 Failure Disposition

1. 单次isolated live授权已消费，run `b68804f0-aaf9-4da4-95e1-aa3b605bfada`不得重试、续跑或复用。
2. 执行在preflight authority forwarding处fail closed；最终`orchestrator_cleanup_unknown`，startup/abort Closure未形成。
3. 不进行现场源码修复。该历史失败事实已由DESIGN-126-016与LIA-126-028/S10BO3 corrective处理，run永久不可重用。
4. corrective至少覆盖：子Make七SHA变量原子传递、pre-run cleanup不误标attempted、保留original primary leaf、无run-root失败的content-free evidence及exact zero-resource closure。
5. `S10B-BLK-009 Closed`、G3 Partial、G4/G6 Pending与`s10b_r8_executed=false`保持；fresh R8仍未授权。
6. Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check`首轮及本条回写后的最终复跑均PASS。

## 26. LIA-126-028 / S10BO3 Corrective Implementation

1. `DEC-126-069 Accepted Option A`：保留原isolated live FAIL、禁止复用run ID，采用DESIGN-126-016完整Infra failure-safe corrective。
2. 单一authority修复七SHA到nested Make assignments；preflight closed frame只允许JSON及唯一精确Make trailer。
3. 增加single-use attempt marker、immutable failure/closure、marker digest和script/binary/start identity绑定；existing run仅reconcile cleanup。
4. 分离attempted与cleanup-required，保持primary failure，持久化cleanup/no-log/evidence/parent secondary；partial startup/root和unknown outcome均fail closed。
5. 增加scope-aware cleanup/no-log、exact volume set、phase/process-role descendant完整性、fresh Docker/listener inventory及no-resume测试。
6. Infra Node syntax、validate、lint、`make test` `186/186`、targeted `65/65`及diff PASS；`S10BO3-001–020`全部PASS，Owner已接受`LIA-126-028/S10BO3 Corrective Closure`。
7. `S10B-BLK-010 Closed`；不形成因本决定而产生的新live证据，不运行Docker live、isolated live、fresh R8或业务case，不commit/push。
8. Governance default、strict、G2A、unique-key YAML、lint、test、shell syntax与`git diff --check`在本次证据回填后全部PASS。

## 27. DEC-126-070 S10BO3 Local Clean Checkpoint Closure

1. 七仓scope复核通过后，仅提交Infra五个S10BO3 corrective文件与Governance既有九份FEAT-126治理文件。
2. Infra `186/186`、四文件targeted `65/65`、validate/lint/Compose semantic/diff门禁全部PASS，形成local clean checkpoint `91f7ec03372b1528abb93818abfad432a83327c4`。
3. Governance在回填该精确SHA后重新运行default、strict、G2A、unique-key YAML、lint、test、shell syntax与diff；全部PASS后形成包含本记录的单一本地checkpoint。
4. Governance checkpoint精确SHA在提交后报告；同一commit不能把自身最终SHA写入自身内容。
5. 两个checkpoint均不push；不得自动进入isolated live、fresh R8、业务case、S11或任何发布/远端动作。
6. `S10B-BLK-009/010 Closed`、G3 Partial、G4/G6 Pending与`s10b_r8_executed=false`保持。

## 28. LIA-126-029 Failure Disposition

1. 第二次isolated-live授权仅消费run `8b94dc6d-5984-4579-9e0c-bed43a4b872f`；该run不得重试、续跑或复用。
2. 相对Node入口无法在Darwin取得absolute process identity，orchestrator在attempt marker与preflight前以`orchestrator_process_identity_unknown`停止。
3. 不创建模拟ledger、no-log或cleanup结果；外部container/network/volume/listener为0只作观测，正式Closure保持NOT ESTABLISHED。
4. Public Tasks/conversation/turn/provider调用为0，business cases disabled，`s10b_r8_executed=false`。

## 29. LIA-126-030 Corrective Execution and Exit

1. 仅修改Infra `Makefile`、orchestrator和两个测试文件；Contracts/API/Host/Desktop/Runtime源码不变。
2. Make解析绝对Node后启动；orchestrator在identity/script检查前创建single-use preclaim，并为marker前失败持久化content-free、digest-bound failure。
3. failed/incomplete preclaim fail closed；concurrent claim不产生两个fresh owner；legacy marker-only attempt保持reconcile兼容；preclaim纳入no-log。
4. Infra Node syntax、validate、lint、Compose semantic、full `188/188`、targeted `67/67`、absolute Node self identity与diff全部PASS。
5. Owner后续checkpoint授权接受Corrective Closure并关闭`S10B-BLK-011`；没有执行new live、fresh R8或业务case。

## 30. DEC-126-072 Local Checkpoint Exit

1. Infra形成local clean checkpoint `c7edbc344daecb84553efafe86dfe335a5c0c72d`；Governance只提交既有九份FEAT-126文件。
2. Governance全门禁复跑PASS后形成包含该Infra SHA的本地checkpoint；精确SHA在commit后报告。
3. Contracts `29317b6426578749dc698fc2ad32b986ee5c8e9f`、API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`、Desktop `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`与Runtime `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`保持clean/unchanged。
4. 两个checkpoint均不push；在新SHA与另一份isolated-live授权前不得再次live，fresh R8和业务case仍未授权。

## 31. LIA-126-031 Failure Disposition

1. 第三次isolated-live授权仅消费run `056a4dab-6afc-45ff-bfff-d1fcc67d2394`；不得重试、续跑或复用。
2. 离线只读审计确认Desktop temp-only run-root拒绝是`orchestrator_control_eof`主因；closure truth table与v1 no-log detail是两个独立证据缺口。
3. 保留preclaim/attempt/failure/run root和四个retained volumes；不修改旧evidence，不读取volume内容，不执行Docker lifecycle/reconcile。
4. business cases disabled，Public Tasks/conversation/turn/provider calls=0，`s10b_r8_executed=false`。

## 32. LIA-126-032 Corrective Execution and Exit

1. Desktop仅修改`src-tauri/src/feat126_secure_storage.rs`；Infra仅修改orchestrator与S10BO3测试。
2. Desktop repository-root authority只在feature driver + ephemeral + UUIDv4 + canonical Infra suffix下开放，cleanup复用同一校验。
3. Infra闭合known-scope failure closure/reconcile，并用content-free v2 unique origin/rule set digests补足未来no-log diagnosis，legacy v1保持兼容。
4. Desktop完整门禁及default/feature测试PASS；Infra `189/189`、S10BO3 `27/27`、syntax/validate/lint/Compose semantic全部PASS。
5. 形成Desktop `9771da11c47406e45526dea104f3d7de05701fba`与Infra `61062143fa3c81b90792ec6f48aea7d6408ed06d` local clean checkpoints；未push。

## 33. DEC-126-074 Local Checkpoint Exit

1. Governance仅更新既有九份FEAT-126文件，登记失败审计、corrective scope、门禁和两个实现SHA。
2. Governance全门禁PASS后形成包含本记录的单一本地checkpoint；精确SHA在commit后报告。
3. Contracts/API/Host/Runtime保持既定exact clean SHA；失败run与retained volumes不变。
4. 不自动执行新的isolated live；fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用、push、merge、tag、publish和deploy均未授权。

## 34. DESIGN-126-019 / LIA-126-033 One-shot Corrective Slice

| Slice | Allowed files | Implementation obligation | Verification / status |
|---|---|---|---|
| D1 Desktop startup terminal | yijie-desktop/src-tauri/src/feat126_s10_driver.rs, src-tauri/src/lib.rs, src/feat126/s10b-driver.ts, src/main.ts; targeted test may change | closed startup-failure allowlist and bounded content-free frame; native/Tauri/frontend pre-ready leaves; one-shot first-terminal boundary; no post-ready startup-failure projection | COMPLETE；checkpoint `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`；targeted/full/build/clippy PASS；no live |
| I1 FD4 authority/race | yijie-infra/scripts/feat-126-s10b-orchestrator.mjs; S10BO2 targeted test | validate malformed authority defensively; drain complete frame before child-exit projection; Desktop leaf primary, EOF fallback; no retry/resume/ownership continuation | COMPLETE；checkpoint `5fdba2b22b343237683f383f098fa2ffaea5bc54`；targeted/full PASS；no live |
| I2 Docker/no-log authority | same orchestrator; S10BO3 targeted test | exact labels and four service roles; stable role-origin ASCII digest; v3 rule/origin/pair digests; JSON/value-aware scanner and v1/v2 reader compatibility | COMPLETE；两个review P1已关闭；syntax/validate/test/diff PASS；原no-Docker边界未重试Compose，后续config-only门禁已以Compose 5.3.0、direct config及Infra `make lint/test` PASS补齐，无lifecycle/live |
| G1 Governance closure | FEAT-126 package documents and feature.yaml only | record scope, contract impact, tests, rollback and explicit stop; do not claim unrun results or SHA | IMPLEMENTATION RECORD COMPLETE；default/strict/G2A/YAML/lint/test/shell/diff最终复跑PASS；checkpoint SHA仅在commit后报告 |

The slices are one corrective authorization and must be reviewed as a set. No Contracts/API/Host/Runtime changes are permitted. If a required fix escapes these files, stop and report contract-impact or repository scope expansion before editing.

DEC-126-076已接受上述slice集合的Corrective Closure并关闭environment-bound Compose gap。真实Tauri `AppHandle/setup` direct fixture继续保留为P2/live；G3仍为Partial，G4/G6 Pending。包含本接受记录的新Governance checkpoint形成后，下一次isolated-live必须使用新七仓精确SHA并取得另一份一次性授权。

## 35. DESIGN-126-020 / LIA-126-035 Corrective Exit

1. LIA-126-034 run `41cdd1c7-e1a6-43ae-ac3a-706ff6989e99`保持历史FAIL且永久不可复用；不覆盖、补写或修改其evidence/retained volumes。
2. Desktop只修改已授权driver/lib/frontend及targeted test，形成checkpoint `713bd5a2985c491db5d6cfc3e31f8f509994427d`；startup stage/watchdog、panic/page-load/frontend/first-IPC terminal、real Tauri mock fixture及FD4 ordering完成。
3. Infra只修改orchestrator、BO2/BO3 tests及Caddy fixture，形成checkpoint `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`；primary failure durability、pre-ownership known scope、FD4 priority及runtime-log-scan v3 field-class分类完成。
4. Desktop和Infra全部targeted/full/lint/build/syntax/Compose config/diff门禁PASS，独立只读review无open P0/P1；Contracts/API/Host/Runtime无需修改。
5. DEC-126-077接受Corrective Closure并关闭`S10B-BLK-013`；Governance仅更新现有FEAT-126 package和feature.yaml，门禁通过后形成一个local clean checkpoint。
6. checkpoint后停止。不得自动执行isolated-live、fresh R8、业务case、S11、MiniMax、Keychain、默认启用或任何远端动作；下一次live需基于新七仓精确SHA另行一次性授权。

## 36. DESIGN-126-021 / LIA-126-036 Two-stage Corrective Exit

1. Phase G从Governance精确SHA `5da2d93b7c4e3ee9884b0fedb04261b5aaf65f92`开始，只修改现有FEAT-126文档与`feature.yaml`，登记DEC-126-078、v4 authority、compatibility、tests和rollback。
2. Phase G明确允许Infra保持HEAD `222fd36a1555bd4787798ed95bf3b4e6b76fa3e1`及四个既有预期dirty corrective文件；记录其SHA-256，禁止修改、暂存或提交Infra。
3. Governance全门禁PASS后只创建一个local commit并确认clean。该commit不预填未来Infra SHA。
4. Phase I随后恢复同一Infra corrective，完成production assets、v4 writer/reason-class/Caddy fixture的剩余targeted/full/config-only/syntax/diff门禁及独立只读审查。
5. 仅在Infra创建一个local commit并确认clean；其它六仓不修改。最终Governance与Infra SHA在执行报告中列出。
6. 两阶段均禁止Docker lifecycle、isolated-live、fresh R8、业务case、S11、MiniMax、真实数据、Keychain、默认启用与远端操作；`s10b_r8_executed=false`。

## 37. DEC-126-079 Owner Acceptance Exit

1. Phase G checkpoint=`b7542d4054efc85843ee17b7e79856045e9b385a`；Phase I checkpoint=Infra `ef9984b06c2913b1d7561360b1e3e569cbfd9d4a`。
2. Infra四文件corrective、targeted `51/51`、full `193/193`、Compose 5.3.0 config-only、syntax/diff及独立review证据由Owner接受；DESIGN-126-021 Complete，LIA-126-036 Corrective Closure Accepted。
3. Governance只更新现有FEAT-126 package与`feature.yaml`，全门禁通过后形成一个local clean checkpoint；自身SHA只在commit后报告。
4. checkpoint后停止。G3仍Partial，G4/G6 Pending；不得自动执行isolated-live或fresh R8，下一次live必须固定最终七仓clean SHA并另行一次性授权。

## 38. DEC-126-080/081 / DESIGN-126-022 Corrective Exit

1. LIA-126-037 run `5a52227e-64cf-4544-9a42-527c512433fe`保持永久FAIL和不可复用；只读审计不得把旧`driver_login_failed`虚构成某个内部stage leaf。
2. Desktop只提交六个driver/native-auth/frontend文件，形成checkpoint `b066e8d08b5f80521c87a6505649b1bb3a62d83b`；closed stage mapping、unknown fallback及FD4 allowlist成对完成。
3. Infra只提交orchestrator、BO3 test和脱敏Caddy fixture，形成checkpoint `cf00b4caacefbd35823dffafb9e23653484bc576`；login leaves、top-level exact event shapes及fail-closed malformed roots完成。
4. 两仓targeted/full/lint/build/config-only/syntax/diff门禁PASS，独立复审无open P0/P1；Contracts/API/Host/Runtime无需修改。
5. DEC-126-081接受Corrective Closure并关闭`S10B-BLK-014`；Governance只更新现有FEAT-126 package与`feature.yaml`，全门禁通过后形成local clean checkpoint。
6. 取得最终七仓exact clean SHA后，Owner可以另行签发一次全新、不可重试的isolated-live startup/abort授权并现场生成未使用UUIDv4。该授权不包含fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用或远端动作。

## 39. DESIGN-126-023 / LIA-126-040 Corrective Exit

1. LIA-126-039 run `5633d030-9486-4824-bf2c-7f0ee7954b58`保持永久FAIL、已消费且不可复用；其evidence与retained volumes不修改、不删除、不resume。
2. Desktop仅修改`synthetic_agent.rs`，形成checkpoint `475086f1e68bcd1e0820a07b727d741e22a1bf62`；Keycloak session-state格式修正，callback其余authority不放宽。
3. Infra仅修改orchestrator、BO3 test及脱敏Caddy fixture，形成checkpoint `e4e92ff1c2f7cbb7627917fb0bc04a5c9bd1b2e2`；storage-cleaning skip exact shape闭合，未知输入继续fail closed。
4. 两仓targeted/full/lint/build/config-only/syntax/diff门禁PASS，独立只读复审无open P0/P1；Contracts/API/Host/Runtime无需修改。
5. DEC-126-082接受Corrective Closure；Governance只更新现有FEAT-126 package与`feature.yaml`，全门禁通过后形成一个local clean checkpoint。
6. 取得最终七仓exact clean SHA后，LIA-126-041现场生成未使用UUIDv4并且只执行一次canonical startup/abort。失败即canonical closure并停止；不授权fresh R8、业务case、S11、MiniMax、Keychain、默认启用或远端动作。

## 40. DESIGN-126-024 / LIA-126-044 Corrective Exit

1. LIA-126-041/042/043三个run均保持已消费FAIL且永久不可复用；其evidence和retained volumes不修改、不删除、不resume。
2. Infra只修改orchestrator、BO3 test和完全脱敏Caddy fixture，形成checkpoint `d4749cb31242799d7cb8f566d44bea3c1f085d8a`；其它六仓不修改。
3. BO2/BO3 targeted `51/51`、full `193/193`、lint、Compose 5.3.0 config-only、Node/Shell syntax和diff全部PASS；独立只读复审无open P0/P1。
4. DEC-126-083接受Corrective Closure；Governance只更新现有FEAT-126 package和`feature.yaml`，门禁通过后形成一个local clean checkpoint。
5. 取得最终七仓exact clean SHA后，LIA-126-045现场生成一个未使用UUIDv4并只执行一次canonical startup/abort。任一失败形成canonical closure并停止，禁止retry/resume/reuse。
6. fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用及远端操作仍禁止。

## 41. DESIGN-126-025 / LIA-126-046 Corrective Exit

1. LIA-126-045 run `f07e9f3f-bc8f-4a3d-9da9-b79ba70054b2`保持已消费FAIL且永久不可复用；其ledger、evidence和retained volumes不修改、不删除、不reconcile。
2. Infra只修改orchestrator与BO2 regression，形成checkpoint `58dc41f16e1d3411d7170cc2f5b10843a1ad13c5`；其它六仓不修改。
3. 历史只读回放、BO2/BO3 targeted `52/52`、full `194/194`、lint、Compose 5.3.0 direct config、validate、Node/Shell syntax和diff全部PASS；独立复审无open P0/P1。
4. DEC-126-084接受Corrective Closure并关闭`S10B-BLK-015`；Governance只更新现有FEAT-126 package和`feature.yaml`，门禁通过后形成一个local clean checkpoint。
5. 取得最终七仓exact clean SHA后，LIA-126-047现场生成一个未使用UUIDv4并只执行一次canonical startup/abort。任一失败形成canonical closure；该run不得retry/resume/reuse。
6. fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用及远端操作仍禁止。
