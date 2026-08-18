# FEAT-127 原子实施计划

## 1. 原则与边界

- contract candidate -> Host provider -> Desktop native consumer -> UI activation。
- 各仓独立 diff/验证；初始授权不含 Git 操作，2026-08-19 用户追加授权 add/commit/push，仍不含 tag、merge 或 deploy。
- 不修改 `yijie-codex` Runtime core，不调用真实 MiniMax，不添加云资源。
- 保留 Desktop 既有 FEAT-126 未提交改动；禁止 reset、全仓格式化和无关重构。
- dirty sibling 阶段只支持本地 candidate；最终 Contracts full commit、下游 pin 与 semantic Owner/consumer review 已形成，G2A 由 `EXC-127-002` 管理临时 Desktop Rust adapter 后对本地候选通过。release tag 是后续发布步骤，尚未创建。
- 自动化完成默认只把候选推进到用户 Desktop 人工验收。用户于 2026-08-19 批准 `EXC-127-001` 后，当前本地 G3 可记为 `PASS WITH EXCEPTION`，但人工结果继续记为 `PARTIAL`、可访问性继续记为 `NOT RUN`。G4 另经 contract conformance、完整门禁、独立审查、提交/推送和 Reviewer 批准后通过；不代表完整人工验收或 release-ready。

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
| S8 | independent read-only review and FEAT-127 evidence | feature docs/design pattern | strict package check, diff/status review | finding/invalid exception -> affected gate returns pending |

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

## 6. Contract Candidate 收口

The Host production sync tool correctly refuses dirty/floating contracts. During initial implementation S3 therefore used a generated same-source candidate adapter without changing `api/contracts.lock`. After the user's 2026-08-19 commit/push authorization, Contracts ultimately formed `747cf740f2d91e76e5c1a130e8e009f1efa821b8`; Host synchronized it in `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86`, removed the temporary duplicate adapter, and passed `contract-check`, race tests and `runtime-test`.

Desktop then pinned the same commit in `2cb4ffdd87055e5f70aafacc63479154e0c62cad`. Because no Rust OpenAPI generator is approved, its explicit adapter is governed by `EXC-127-002`: exact source/fixture/adapter/readiness digests, structured validation, canonical serialization, expiry and negative tests all fail closed. No release tag was created; candidate supported/release-ready status remains pending.

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
| S3 | provider committed, pinned and pushed | v2 HTTP/conformance PASS；Host `e2f0f5d...` pins Contracts `747cf740...`；temporary Host candidate adapter removed |
| S4 | implementation and automated re-verification passed; manual candidate only | authoritative SQLCipher 0006->0007 catalog/ledger、target-scoped `draft_ordinal`、worker shutdown、TTL/WAL、PDF/OOXML adversarial tests and Rust gates PASS |
| S5 | implementation committed/pushed; automated re-verification passed | ESLint/typecheck、35 files / 270 Vitest、Rust 175 passed / 3 ignored、build；bind/session draft reload fail-closed + retry、five stages >=220ms、command rejection/late event terminal monotonicity、visual matrix PASS |
| S6 | automated re-verification passed | HostBridge/outbox v2、lost/invalid response same-operation replay、ordered history/dispatch tests PASS |
| S7 | targeted automated regression passed; manual partial | manual PASS：picker、attachment-only Runtime、post-fix image drop、mixed send、sent-history reopen、unsent-draft reopen；automated-only PASS：removal/bounds/10+1 capacity；macOS accessibility NOT RUN |
| S8 | review/evidence complete; G4 pass for local candidate | original thirteen P1 plus final contract-lock audit findings fixed and reverified；P0/P1/P2 clear；strict G4/feature-package checks PASS；两项例外、semantic review 与 Reviewer approval 已记录 |

Overall state: `G4 PASS for local candidate with EXC-127-001/002 / Production Activation Blocked`. This is local code-complete only: S7 still has partial manual evidence, real macOS accessibility is `NOT RUN`, and both exceptions are temporary. It is not a release, supported contract, signed candidate, G5 or G6 claim.

Git execution completed in dependency order: Contracts `747cf740...` -> Host `e2f0f5d...` -> Desktop `2cb4ffd...`; each commit is pushed to its existing upstream branch, and Host/Desktop cross-reference the exact Contracts commit. The feature-package commit records G4 without self-referencing its own SHA. No PR, merge, tag or release artifact was created. Deploy、production smoke、monitoring and G5/G6 remain outside the local-only authorization and stay `N/A/not passed`.

## 9. Approval

This is the Codex implementation plan selected under the user's explicit local-feature authorization and permission to fill missing engineering detail. Recorded user Desktop results are limited to the scenarios listed in S7; automated-only checks are not relabeled as manual acceptance. The user separately approved G3 `PASS WITH EXCEPTION`, semantic Owner/consumer review and Reviewer acceptance for the local G4 candidate on 2026-08-19. Independent Codex audits supplied technical findings but are not presented as the human approval. G4 is `PASS` only for this local candidate under `EXC-127-001/002`; merge, tag, release and production phases remain unauthorized or N/A/not passed.
