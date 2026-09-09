# FEAT-134 Host v4 projection candidate and immutable commit

Date: 2026-08-28

## D4 downstream follow-up — 2026-08-29

Host final authority 仍是 clean immutable commit `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe`，未 push。#5 持久化 content-free metadata 为 attempts=1/outbox done/completed/terminal1/v4 events187/reasoning1-part1/plan0/phase null；#6 final-source UI 观察 processing→completed、reasoning/unknown expanded、Composer 恢复并正常 Cmd+Q 清理。#6 未另取 DB counts，不继承 #5 的 187。

#5 后发现的 native/WebView/TS repeated-finalized 跨层 P2 已在 Desktop 修复；最终 TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff PASS，review 无 open P0/P1/P2。Runtime clean 固定 SHA、binary/manifest 匹配、无重编译。D4=PASS；Desktop immutable commit `7b9daa791635250d0628c9e9f553cf40fab5ad96`、clean、未 push，`yijie` 治理包未提交。历史 tranche 4/4、当前 6/7、Feature 10/11。

## Scope

This record covers the verified and committed `yijie-agent-host` FEAT-134 candidate. It is an
immutable source commit, but not a published Host release, Desktop conformance result, canonical
provider run, D4 result, or Epic completion claim.

| Identity | Value |
|---|---|
| Host branch | `feat/feat-134-desktop-streaming-progress-final-response` |
| Host immutable base | `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` |
| Host first FEAT-134 implementation commit | `201fd9f8fff6e1ee18ddc1a0477e329b0d75af0c` |
| Host corrective child / final authority | `b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` |
| Contracts version | `0.6.0` |
| Contracts immutable ref/commit | `3832a6c5e99b2a6365f193280fdb887c8fdbc2de` |
| `api/contracts.lock` SHA-256 | `c1ae8d7d363269c29a1858142c07a1c6041d9fbd394c126539e12dee767934d9` |
| AgentSessionEventV4 schema SHA-256 | `d972806e59195c5e1f5fe810db6e1df80be349b77ecc4cf192ed0f391d9ed739` |

## Implemented Host boundary

- `make sync-contracts` consumes only the clean, full Contracts commit and synchronizes v4
  OpenAPI, compatibility, JSON Schema, canonical fixtures and generated Go DTOs.
- `GET /v4/agent-sessions/{agent_session_id}/events` exists only behind exact FEAT-134 activation
  and requires explicit `event_schema_version=4` negotiation.
- AgentMessage lifecycle projects authoritative `phase=commentary|final_answer|null`; deltas remain
  text-only and require a matching AgentMessage lifecycle `item_id` in the same Turn.
- Stable `turn/plan/updated` maps only the Runtime full ordered snapshot. Missing/null source arrays,
  missing step text and non-Runtime status spellings fail closed; an empty plan remains an explicit
  clear and an empty step remains authoritative text.
- Raw reasoning uses an independent Host authority and no longer follows the v3 Artifact gate.
  V4 admits at most eight unique reasoning items per Turn. A ninth item's body is not retained;
  instead v4 publishes one content-free `reasoning_text.finalized` with `status=unavailable`,
  `reason_code=limit_exceeded` and empty contents, without failing the whole Turn projection.
- Every retained v4 event passes a closed producer validator before replay. Compact SSE data is
  limited to 1 MiB without truncation. Turn-scoped projection failure publishes content-free
  `limit_exceeded` error and one failed terminal; no-turn oversized warning becomes a content-free
  warning.
- Malformed terminal handling completes the Host Store Turn as failed, clears image/synthetic
  state, first finalizes each admitted unfinished v4 reasoning item in stable item-ID order as
  content-free `unavailable/protocol_error`, and then publishes only one v4 sanitized terminal.
  It does not inject the v4-only reasoning/terminal failure into v1-v3.
- V1-v3 payloads strip v4-only phase/plan fields. Shared v1/v2 control calls retain their previous
  trace acceptance; an over-limit trace is handled only at v4 projection.

## Exact local model behavior

Activation requires all of the following:

- exact `YIJIE_FEAT134_STREAMING_ENABLED=true`;
- explicit `YIJIE_ENV=local` and `YIJIE_LOCAL_PROFILE=demo_fast`;
- managed MiniMax provider with separate physical Host and Runtime homes;
- DynamicTools disabled, so Runtime initialization remains `experimentalApi=false`.

The managed Runtime home and every effective Turn request are fixed to reasoning effort `high`.
Managed config enables `show_raw_agent_reasoning=true` and keeps reasoning summary `none`. Physical
and symlink aliases between the two homes are rejected, including aliases whose leaf directory has
not yet been created. The flag is absent by default and is rejected outside the exact local profile,
so public/production behavior remains unchanged.

## Review corrections

An independent Contracts/Host review found five P1 boundaries before final verification. Its
post-fix review then found two remaining reasoning-policy P1s. All seven review corrections were
closed with regression tests:

1. v4 trace limits no longer reject otherwise valid shared v1/v2 control requests;
2. Host/Runtime home separation compares physical authority and fails closed on alias ambiguity;
3. malformed terminal closes Store/reasoning state and cannot create a second v4 terminal;
4. orphan, cross-Turn, wrong-item and non-AgentMessage deltas cannot enter v4;
5. a ninth reasoning item cannot place a ninth raw body into v4 while legacy v2/v3 behavior is
   unchanged;
6. malformed terminal finalizes unfinished admitted v4 reasoning as
   `unavailable/protocol_error` before its sanitized terminal; and
7. the ninth reasoning item uses the Contract's reasoning-specific
   `unavailable/limit_exceeded` finalization, does not emit a generic `error`, and does not fail
   subsequent Turn projection.

## Gate evidence

| Command | Result |
|---|---|
| `make contract-check` | PASS; exact Contracts commit and `oapi-codegen@v2.7.2` verified |
| `go test ./... -count=1` | PASS; all Host packages |
| `go test -race ./internal/session ./internal/app ./internal/codex ./cmd/desktop-host` | PASS |
| `go vet ./...` | PASS |
| `git diff --check` | PASS |
| independent post-fix rerun of full test, focused race, vet and contract check | PASS |

The tests are deterministic, local and non-destructive. They do not call a provider, invoke a tool,
read or write task files, inject faults, replace binaries, damage permissions or force-kill a
process.

## Runtime and external-action boundary

`yijie-codex` remains clean on `develop@0ce5902ed400866be0196886bb78f693a004d68d`.
No Runtime source, schema, manifest, binary, build, installation or pin was changed; no Runtime was
recompiled or synchronized. At the time this Host candidate record was first captured, canonical
`pnpm tauri:demo-fast:stable` had not started and prompt consumption was `0/1`. That historical
statement is superseded for current consumption by
`canonical-v4-content-free-2026-08-28.md` (historical `4/4`, current `6/7`, Feature `10/11`).

## Commit and handoff point

Owner authorized Host staging and commit but not push. The first FEAT-134 implementation was
committed as `201fd9f8fff6e1ee18ddc1a0477e329b0d75af0c`. Canonical verification then exposed that its
structured Item content decoder was too narrow. Its direct corrective child
`b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe` keeps general content as opaque raw JSON and decodes only
the supported completed-reasoning shape. The Host working tree was clean after the corrective
commit and nothing was pushed. The authoritative linear history is therefore
`1b7bfd… -> 201fd9… -> b9358f…`; Desktop may consume only final SHA `b9358f…`, while governance must
retain the failed-first-implementation provenance.
