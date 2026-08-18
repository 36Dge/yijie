# FEAT-127 原子实施计划

## 1. 原则与边界

- contract candidate -> Host provider -> Desktop native consumer -> UI activation。
- 各仓独立 diff/验证；初始授权不含 Git 操作，2026-08-19 用户追加授权 add/commit/push，仍不含 tag、merge 或 deploy。
- 不修改 `yijie-codex` Runtime core，不调用真实 MiniMax，不添加云资源。
- 保留 Desktop 既有 FEAT-126 未提交改动；禁止 reset、全仓格式化和无关重构。
- dirty sibling 阶段只支持本地 candidate；当前不可变 Contracts full commit 与下游 pin 已形成，正式 G2A 仍等待 Owner/consumer review 与 release tag。
- 自动化完成只把候选推进到用户 Desktop 人工验收；人工验收记录形成前，任何切片和总状态都不得写成 `Local Candidate Complete`，G3/G4 保持 `PENDING`。

## 2. 依赖 DAG

```text
S1 contract + idempotency
  -> S2 Host domain/runtime provider
  -> S3 Host HTTP candidate/conformance
  -> S6 Desktop HostBridge/outbox

S1 Chat schema
  -> S4 Desktop parser + migration + repository
  -> S5 Desktop IPC/domain/store/UI
  -> S6 cross-component dispatch/history
  -> S7 security/migration/visual E2E
  -> S8 independent review + delivery evidence
```

S2/S4 可并行；S5 前端可基于稳定 DTO candidate 与 S4 并行，但 S6 前必须逐字段对齐。

## 3. 实施切片

| Slice | 意图 / AC | Repository / allowed scope | 验证 | Rollback |
|---|---|---|---|---|
| S1 | Host v2 + Chat blocks + operation ID；AC-004/006/011 | contracts source/tests/generated SDK only | generate/lint/test/breaking/v1 equality | stop versioned v2 activation and revert the semantic source/generated candidate diff; retain v1 |
| S2 | strict block validation、idempotent service、Runtime `UserInput[]`；AC-004/006 | Host `internal/session`, `internal/codex`, tests | focused Go + race tests | keep v1 adapter, disable v2 |
| S3 | v2 HTTP route and contract candidate adapter；AC-003/006/011 | Host app/API candidate/tests; no lock weakening | strict decode/error/conformance, v1 regression | unregister v2 route |
| S4 | native importer/parser/authoritative SQLCipher v6->v7 chain、target-scoped `draft_ordinal`、TTL/binding；AC-002/003/007/008/009 | Desktop `src-tauri` chat + Cargo deps | fmt/clippy/unit；catalog ledger/FK、v1-v5/v6->v7、same-second/reopen/remove/append/security tests | stop v2 writes; leave forward-only schema；old app requires pre-v7 encrypted backup |
| S5 | IPC v2、client/store/composer/history/drag、draft recovery fail-closed、220ms stage display、command/event terminal race；AC-001/002/005/007/010 | Desktop `src/**`, IPC command registration | ESLint/Vitest/type/build；bind/session retry、late event、minimum stage、visual tests | hide v2 UI and continue v1 text；unknown draft remains closed |
| S6 | outbox v2/HostBridge/idempotent dispatch/resync; AC-004/006/011 | Desktop chat application/bridge/tests | fake Host integration, lost-response retry, ordered request | payload version routes old turns to v1 |
| S7 | removal、TTL、adversarial parser、session cleanup、full UI matrix、真实 Desktop 手工验收; AC-003/008/009/010 | focused tests/harness；用户本地 Desktop | full Desktop/Host suites、screenshots；用户 picker/drop/send/reopen/recovery 记录 | automated candidate may proceed to manual acceptance；no completion claim before user result |
| S8 | independent read-only review and FEAT-127 evidence | feature docs/design pattern | strict package check, diff/status review | remain Manual Acceptance Candidate；G3/G4 blocked |

## 4. DTO 对齐

Desktop IPC v2 uses camelCase under `{ schemaVersion: 2, requestId, data }`:

- commands: `chat_pick_attachments_v2`, `chat_import_attachments_v2`, `chat_remove_attachment_v2`, `chat_create_session_v2`, `chat_submit_turn_v2`, `chat_load_history_v2`, `chat_resync_session_v2`;
- attachment: `{ attachmentId, type, name, mediaType, sizeBytes, status, expiresAt }`;
- input blocks: `{ type: text, text } | { type: file|image, attachmentId }`;
- history blocks: text plus safe attachment metadata, never paths/BLOB/chunks/data URL;
- create/submit includes Desktop `operationId`; outbox forwards it as Host `operation_id`.

Any Rust/TS field divergence is a stop condition, not a reason to loosen strict parsing.

## 5. Migration 序列

| Phase | Action | Compatibility | Stop/rollback |
|---|---|---|---|
| Expand v6 | `migrations.rs` catalog applies `0006_chat_attachments` after 0001..0005；records exact name/SHA ledger | v1-v5 data and old queries unchanged；adds attachment/chunk/content-block tables and indexes | transaction rollback；ledger/FK/repeat-startup validation |
| Expand v7 | catalog next applies `0007_chat_attachment_draft_targets`；adds target columns, indexes, partial unique indexes and guards | bound v6 history preserved；ready rows require `new` or same-scope `session` target | transaction rollback before commit；after upgrade use v7 roll-forward or pre-v7 encrypted backup |
| Safe cleanup | v7 removes only unbound v6 `ready` rows whose composer target is unknowable | no cross-composer draft disclosure；bound/expired metadata remains | restore pre-v7 backup or roll forward |
| Draft order | repository allocates target-scoped `draft_ordinal = MAX + 1` and reads `ORDER BY draft_ordinal` | same-second, reopen and remove/append preserve selection order；gaps are not renumbered；bind clears draft fields | unique indexes/guards abort invalid state; retry transaction |
| Backfill | N/A; old message blocks synthesized at read | no mass data rewrite | N/A |
| Switch | write content blocks only for v2 create/submit | payload version keeps existing v1 outbox | unregister v2 UI/route |
| Contract | NOT IN SCOPE; do not remove old content/input | old Desktop/Host remain supported | future feature/ADR |

## 6. Host Contract Candidate 例外

The Host production sync tool correctly refuses dirty/floating contracts. During initial implementation S3 therefore used a generated same-source candidate adapter without changing `api/contracts.lock`. After the user's 2026-08-19 commit/push authorization, Contracts formed `ebdd30f076614ebc7f5149aebf70e851b81ff32b`; Host formally synchronized that commit, removed the temporary duplicate adapter, and passed `contract-check`, race tests and `runtime-test`. No release tag was created.

## 7. Per-slice 闭环

Each slice follows:

```text
read current files/status
  -> add failing/behavioral test
  -> minimal implementation
  -> focused checks
  -> full diff/status/check
  -> update 08 evidence
```

Stop if requirements conflict with code, secrets/real seller data appear, a capability/CSP/cloud target is needed, a test passes only after weakening assertions, or scope expands beyond the slice.

## 8. 实际状态（持续更新）

| Slice | Current status | Evidence summary |
|---|---|---|
| S1 | automated re-verification passed | contracts generate/lint/31 tests/build/supported-baseline breaking/v1 equality PASS |
| S2 | automated re-verification passed | Host strict block validation、idempotency、bounded Runtime mapping and non-persistence tests PASS |
| S3 | provider committed, pinned and pushed | v2 HTTP/conformance PASS；Host `673de86...` pins Contracts `ebdd30f...`；temporary candidate adapter removed |
| S4 | implementation and automated re-verification passed; manual candidate only | authoritative SQLCipher 0006->0007 catalog/ledger、target-scoped `draft_ordinal`、worker shutdown、TTL/WAL、PDF/OOXML adversarial tests and Rust gates PASS |
| S5 | implementation committed/pushed; automated re-verification passed | ESLint/typecheck、34 files / 263 Vitest、build；bind/session draft reload fail-closed + retry、five stages >=220ms、command rejection/late event terminal monotonicity、visual matrix PASS |
| S6 | automated re-verification passed | HostBridge/outbox v2、lost/invalid response same-operation replay、ordered history/dispatch tests PASS |
| S7 | automated checks passed; manual partial | picker/attachment-only Runtime path passed；drop first failed, fix committed, post-fix retest pending；remaining functional and macOS accessibility checks incomplete |
| S8 | documentation checks passed; G3/G4 pending | thirteen P1 findings fixed and reverified；strict feature-package check PASS after this update；complete user manual acceptance absent |

Overall state: `Manual Acceptance In Progress / Production Activation Blocked`. This wording is intentionally not `Local Candidate Complete`; S7 manual evidence is a required remaining step for G3, while G4 additionally remains blocked by G2A and Reviewer approval.

Git execution completed in dependency order: Contracts `ebdd30f...` -> Host `673de86...` -> Desktop `3efed9a...`; each commit is pushed to its existing upstream branch, and Host/Desktop cross-reference the exact Contracts commit. No PR, merge, tag or release artifact was created. Deploy、production smoke、monitoring and G5/G6 remain outside the local-only authorization and stay `N/A/not passed`.

## 9. Approval

This is the Codex implementation plan selected under the user's explicit local-feature authorization and permission to fill missing engineering detail. It is not a recorded user Desktop acceptance, human code review, merge approval or release approval. Until the user returns manual acceptance results, G3/G4 and `Local Candidate Complete` remain explicitly unclaimed; production phases remain N/A/blocked by current scope.
