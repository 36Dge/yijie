# FEAT-134 Contracts v4 source-first candidate and immutable commit

Date: 2026-08-28

## D4 downstream follow-up — 2026-08-29

Contracts authority 仍是 clean immutable commit `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`，未 tag/publish/push。最终 downstream 验证为 Desktop TS 835/835、Rust 316+3 ignored、lint/build/fmt/diff PASS，review 无 open P0/P1/P2；#6 final-source canonical UI smoke PASS。Runtime 保持 fixed SHA、binary/manifest 匹配且无重编译。FEAT-134 D4=PASS；Desktop 已提交 `7b9daa791635250d0628c9e9f553cf40fab5ad96`、clean、未 push，`yijie` 治理包未提交；不声明 production 或 Epic 完成。

历史 prompt tranche `4/4` 保留；当前 tranche `6/7`、剩余 `1`，Feature 累计 `10/11`。全部证据 content-free，不保存或哈希任何正文。dark theme、Reduce Motion、精确 1180×760 逐项 `WAIVED / NOT REQUIRED`，不是 PASS。

## Scope

This record covers the reviewed `yijie-contracts` FEAT-134 source-first candidate and its immutable
commit. It is not a tag, published contract, Host/Desktop conformance result, canonical provider
run, D4 result, or Epic completion claim.

Branch: `feat/feat-134-desktop-streaming-progress-final-response`

Immutable base: `164b14f609537d727a52326832da04430aecc4ab`

Immutable candidate commit: `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`

Planned candidate version: `0.6.0`

Contract impact: `semantic`, version-isolated through AgentSessionEventV4.

## Implemented authorities

- `jsonschema/agent/session-event-v4.schema.json`
- `protobuf/yijie/events/v4/agent_session.proto`
- `openapi/agent-host/agent-host.yaml#/v4/agent-sessions/{agent_session_id}/events`
- `asyncapi/events.yaml#agentSessionEventsV4`
- `compatibility/agent-host-runtime-v1.json`
- generated Go/TypeScript/AsyncAPI SDK projections
- synthetic `tests/fixtures/agent/session-event-v4/**` and v4 conformance tests

V4 requires explicit schema negotiation. AgentMessage lifecycle carries
`phase=commentary|final_answer|null`; stable plan uses authoritative full snapshots. V1–v3 sources
remain unchanged. Raw reasoning uses the established bounded v2/v3 semantics and is not enabled by
v4 negotiation alone.

One compact SSE data value is capped at 1 MiB UTF-8. Host must validate before replay/write and
must not truncate. Existing reasoning-limit finalization remains authoritative; any other
turn-scoped v4 projection overflow produces only a sanitized `limit_exceeded` problem and failed
terminal. Stable Runtime empty plan steps are accepted without invented replacement content.
For no-turn sources, invalid managed thread identity fails session start as sanitized
`500 internal_error`, while an oversized Runtime warning becomes a content-free
`limit_exceeded` warning without an invented Turn.

## Runtime boundary

| Fact | Value |
|---|---|
| Runtime commit | `0ce5902ed400866be0196886bb78f693a004d68d` |
| Upstream | `rust-v0.144.6@5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| Version | `0.144.6` |
| Transport | `stdio` |
| experimental API | `false` |
| Schema files/digest | `267` / `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` |

The compatibility allowlist adds only stable `item/reasoning/textDelta` and
`turn/plan/updated`. It excludes experimental `item/plan/delta`. No Runtime file, binary, schema,
build, installation, or pin was changed.

## Gate evidence

| Command | Result |
|---|---|
| `pnpm generate` | PASS; 14 JSON Schemas generated and SDK output current |
| `pnpm lint` | PASS |
| `pnpm test` | PASS; 56 tests, 0 failures |
| `pnpm build` | PASS |
| `pnpm check:v1-wire f16a497e1377f45747f8ff9292b4b60cf2027f88` | PASS |
| `./scripts/check-breaking.sh 164b14f609537d727a52326832da04430aecc4ab` | PASS |
| `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | PASS |
| `git diff --check` | PASS |

## Reviewed source/generated digests

| Artifact | SHA-256 |
|---|---|
| Agent Host OpenAPI | `49e2171e41e0fc11313a114c82ff09e11a0df396e4b366a03b0d7e3afe1766df` |
| AsyncAPI source | `c38baa3a6f48acf263a9dacea58da66d944464b1e942088e3ae15ac1c048d52c` |
| AgentSessionEventV4 JSON Schema | `d972806e59195c5e1f5fe810db6e1df80be349b77ecc4cf192ed0f391d9ed739` |
| v4 Protobuf source | `7130ffad6f7d415bbaaf35a10bc380b2b75ecaaa4762dc871ce0a274472ecdea` |
| Runtime compatibility projection | `6d28e3ad1bb941561ce08a231abf003dd0e69b5dcafe6376cc5987c3d1f07a00` |
| bundled AsyncAPI | `8ee17ea4b40f33c65736d3d60bfafc0ac8cad3775aad7cc2782b22e90ebb01e5` |
| generated Go Agent Host | `b5f2757b701b2a5336a12f69538ddf6d1aa31f45c1a820798ef0e354080bb80e` |
| generated Go v4 Protobuf | `4b0fde1dd127baf13e3f02121b88bfdf6d78035cd74ea8e6db403084d8dbd13f` |
| generated TypeScript Agent Host | `79d81e4e698b656b2018933d9e4ffaf58f89da2fa37e6d034ed54a96d28e371b` |
| generated TypeScript v4 Protobuf | `86eecfc15c7056667a4e5a9cb3f3db910907648bc3532d66cb52736095afa371` |
| generated TypeScript v4 event schema | `3e5768ca34e0ff93f79c4be2b7d864e784fda2644e0db9e22a4e6be531325b2e` |

## Immutable checkpoint

Owner authorized `git add` and one Contracts commit without push. The reviewed candidate was committed
as `3832a6c5e99b2a6365f193280fdb887c8fdbc2de`; the Contracts working tree is clean. No tag, push,
publish, Host sync, Desktop change, Runtime change, or provider prompt was performed at this evidence
capture point. Host may now pin this full commit identity before implementing the v4 projection.
Paid prompt consumption at this capture point was `0/1`; the current superseding state is historical `4/4` plus current `6/7` (Feature `10/11`) in
`canonical-v4-content-free-2026-08-28.md`.
