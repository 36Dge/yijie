# FEAT-126 Local-only 原子实施计划（S4–S6 已完成）

## 1. 当前执行边界

- G2/G2A已于2026-08-02通过；DEC-126-021 Accepted/HOLD，Draft PR #1保持exact head，红色CI只阻断merge。
- DEC-126-022 Local-only Delivery Strategy已Accepted；LIA-126-001已于2026-08-02批准，且只允许S4–S6本地基础切片。
- S4–S6已在API/Host/Desktop本地未提交工作树完成并保持flags/routes默认关闭；未调用MiniMax，未修改Runtime/Infra，未commit/push/merge/tag/publish/deploy。
- S7–S11仍是未来评审候选；开始前必须获得下一次明确授权并重新核对full SHA/worktree。

## 2. 实施原则

- 一次只完成一个可独立验证的行为；contract-first；provider/consumer/activation 分离。
- Public Tasks安全轨与local conversation产品轨的S4–S6基础已完成，但G4/Local-only G6不因基础切片完成而通过。
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
                  → S7 Desktop domain/outbox/event reducer/history
                       → S8 production UI/a11y
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
| S7 | Session state/outbox/SSE reducer/history/title precedence | AC-003/005/007/013–018/025/029 | yijie-desktop | domain/store/composables/generated types/tests | CSS redesign/model picker/files | S5/S6 provider contracts | TS unit/component + fake Host E2E | flag off; no DB contract drop |
| S8 | 极简production-grade UI与可访问性（仅本地运行） | AC-001/002/004/006/008–013/019/022/031–034 | yijie-desktop | approved components/pages/tokens/tests/Pattern implementation | excluded actions/attachments/right panel/unrelated shell refactor | S0 Pattern + S7 + later authorization | lint/test/build/visual/a11y/manual | disable local chat UI flag |
| S9 | fake-provider title/raw-reasoning Eval | AC-010/011/017/018/042; NFR-007 | Host/Desktop + eval authority | fixed pin/dataset/runner；raw availability、sequence、content/security、no-log metrics | real data、MiniMax、unbounded calls、事后改写旧MM结果 | S5/S7/S8 + later authorization | local fake Eval；future MM-126-003 separately approved only | title/raw flags off；missing raw blocks local G6 |
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
| PR-126-DESKTOP-DOMAIN | session/outbox/event/history domain | yijie-desktop | reducer/DB/component tests | data/Host PRs |
| PR-126-DESKTOP-UI | approved UI/a11y | yijie-desktop | visual/a11y/build | Pattern version |
| PR-126-EVAL | title/raw-reasoning dataset/runner/results | approved repo(s) | fixed Eval | prompt/model/runtime pins |
| LOCAL-126-E2E | local startup/readiness/E2E evidence | API/Host/Desktop/pinned Runtime | full fake-provider local matrix | Local-only G6 |

No commit/push/PR is authorized by this document。上述`LOCAL-*`只是未来本地change-set标识；是否提交或创建PR仍需另行授权。

## 9. Slice 完成记录

| Slice | Head full SHA | Actual diff | Test result | Review | Status |
|---|---|---|---|---|---|
| S0 | no implementation SHA | requirement package + G1/G2 decision record + Accepted Desktop Pattern | package/links/docs build evidence in `08` | Owner approved G2 | G1/G2 Complete |
| S1 | no implementation SHA | read-only Runtime/Host/Public Tasks/storage investigation；fixed fake tests；historical bounded MiniMax evidence；no source diff | raw upstream 4/4 + prior title/summary/delete evidence | bounded facts complete；no implementation claim | Investigation Complete |
| S2 | no implementation SHA | DESIGN-126-003、Public Tasks inventory、DEC-126-017/011/012 | design consistency/package validation | Owner Approved | Complete / G2 Passed |
| S3 | `c000a0245acb5c3f7ead5d2a877fb60c281c588c`；remote candidate branch；Draft PR #1 | source/fixtures/generated SDK/docs only；no business code | clean clone 29 generated current、27/27、Go/lint/build/breaking/v1 equality与九项摘要PASS；remote CI audit FAIL | DEC-126-018/019/020/021/022 Accepted；G2A Passed；merge HOLD | Source candidate complete；red CI blocks merge only；tag/publish N/A；S4–S6已用exact SHA投影 |
| S4 | uncommitted draft on `yijie-api@faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | secure v2 auth/tenant/permission/creator-private repo、idempotency/audit与expand migration；default-off local-lab route | generate-check/race/unit/vet/lint + isolated PostgreSQL migration/integration PASS | structured security/migration review；no blocker | Complete under LIA-126-001 |
| S5 | uncommitted draft on `yijie-agent-host@34e94acf293f6daad61c4d42fa47028a2d1318e4` | exact Host/event v2 projection、bounded raw、isolated title、Runtime cleanup、content-free receipt与bbolt v1→v2 migration | contract-check/race/unit/vet/lint PASS；fake Runtime/no-log/no-bbolt/symlink tests PASS | structured Runtime/delete/secret review；no blocker | Complete under LIA-126-001 |
| S6 | uncommitted draft on `yijie-desktop@155854cf3662384caa2c8bffe0a47935ef4a70b5` | exact Public projection、SQLCipher forward migrations/repository、Keychain、native project、serialized DB worker、local sidecar supervisor；default off | 113 TS + 51 Rust PASS；fmt/Clippy/lint/build PASS | structured DB/scope/path/sidecar/no-secret review；no blocker | Complete under LIA-126-001 |
| S7–S11 | N/A | none | NOT RUN | Not reviewed | Pending separate authorization |

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
| Contracts/G2A/remote | 段成威 | Approved / Passed — DEC-126-018/019/020 Accepted；`c000a0245acb5c3f7ead5d2a877fb60c281c588c`为唯一candidate并已在专用branch远端可用；未merge/tag/发布/pin，不开始业务编码 | 2026-08-02 |
| Contracts Draft PR / merge | 段成威 | DEC-126-021 Accepted/HOLD；CI failed dependency audit；merge不是local draft前置但当前仍不批准 | 2026-08-02 |
| Local-only delivery strategy | 段成威 | DEC-126-022 Accepted；Local Runtime Ready目标，tag/publish/deploy/G5 N/A | 2026-08-02 |
| Local Implementation Authorization | 段成威 | Approved — LIA-126-001仅授权S4–S6；实现与证据完成，S7–S11仍禁止 | 2026-08-02 |

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
