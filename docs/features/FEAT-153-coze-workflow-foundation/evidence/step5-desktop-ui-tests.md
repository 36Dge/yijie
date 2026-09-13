# Step 5 — Desktop normal UI unit tests

Date: 2026-09-12. This subtask added only
`yijie-desktop/src/pages/workflows/use-workflow-workspace.test.ts`.
Contract impact of the test addition is **none**: no application, native command,
wire, capability, persistent state or deployment behavior changed.

## Scope and actual results

The test consumes generated workflow/bridge TypeScript types and the application's
real AOT validators. A mounted minimal Vue harness exercises the real workspace
composable; ordinary asynchronous native mocks and a real MessageChannel exercise
the client/channel state transitions. All IDs, workflow names and canvas text are
synthetic. No API/database/native process is invoked by the final test harness.

Seven focused tests passed:

1. `use-workflow-workspace.test.ts:111`: cancelling pending open A retains the open
   barrier until A's late native result is normally closed; B cannot open before
   that close completes and can open afterwards.
2. `:146`: an ordinary source-defined `operation_unknown` create result retains its
   operation ID, prevents duplicate create, remains queryable while recorded, and
   opens the completed resource only after querying the same operation. The query
   contains no history-only `limit`.
3. `:177`: a normal pending MessageChannel save raises `pendingWrites` and blocks
   reconnect; normal completion releases it, then reconnect preserves dirty state.
4. `:216`: the real generated native-client input validator accepts an operation
   query without `limit`; the invoker receives exactly that source request.
5. `:228`: source-defined unknown-result projection preserves the operation ID and
   uses the fixed UI message, rather than rendering raw provider text.
6. `:241`: the source connect/ready handshake and ordinary dirty/request-close
   notifications use the same binding/generation and do not invoke an exchange.
7. `:261`: a normal read result returns on its source request/generation and passes
   the real envelope validator; a read does not increment pending writes.

Exact commands and execution counts:

| Command | Executions | Result |
| --- | ---: | --- |
| `pnpm exec vitest run src/pages/workflows/use-workflow-workspace.test.ts --maxWorkers=1` | 2 | Both runs had 7/7 assertions PASS; only the second is the final offline harness result. See initial incidental requests below. |
| `pnpm exec eslint src/pages/workflows/use-workflow-workspace.test.ts --max-warnings 0` | 2 | PASS, no warnings |
| `pnpm exec vue-tsc --noEmit` | 1 | PASS |
| `git diff --check` | 1 | PASS |

Final focused Vitest run started at 15:21:57 local time, took 676 ms, and reported
one test file / seven tests passed, with no network error output. No tests were
rerun while writing this evidence or doing the later read-only review.

## Initial incidental iframe requests — retained fact

The first test version created and appended a real happy-dom iframe with the
fixed editor URL before mocking its `postMessage`. Happy-dom automatically tried
to load `http://127.0.0.1:18888/editor/` in the three channel tests. The initial
15:20:50 run printed **three ECONNREFUSED connection attempts** to that address;
its seven assertions still passed. This was unintended page loading by the test
environment, not a deliberate network fault test. It did not start a service,
reach a workflow endpoint, send credentials or perform a workflow write, and it
does not establish static-editor or application qualification.

The test was corrected to use an ordinary fixed-URL frame transport mock which
captures the transferred **real MessagePort**, without creating an iframe or
calling the happy-dom page loader. The second run used that final harness. Its
client invocations remain normal mocks and the channel stays in-process; no HTTP
or native App request is part of the final harness. The initial output has not
been reclassified as an offline run or a real service PASS.

## Follow-up read-only race review

The later review inspected current application/native source without edits or
additional tests. No new P1/P2 issue was found in this bounded scope:

- `yijie-desktop/src/pages/workflows/use-workflow-workspace.ts:56` and `:85`:
  openPending/openingSettled cover the late-open revocation path; the next open
  stays blocked until close settles. Reconnect rejects pending writes. The create
  query at `:117` preserves the original operation lookup and optional limit.
- `yijie-desktop/src/components/workflows/WorkflowEditorPane.vue:59` and `:89`:
  callbacks are guarded by the current bridge ID; reconnect replaces the channel
  while retaining the iframe. The parent overlay, inert/tabindex and pending-write
  button gate are present at `:114` and `:123`.
- `yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.vue:54`:
  route leave first resolves the close decision, waits for pending-open cancellation,
  then waits for normal editor close before allowing navigation.
- `yijie-desktop/src-tauri/src/workflows/runtime.rs:176`: native open captures the
  context revision before the serialized-open queue/status awaits, checks it before
  opening and again before installing the binding, and normally revokes a decoded
  session when installation is abandoned. A completed exchange rechecks its lease;
  a stale write result keeps its operation ID and is reported unknown.
- `yijie-desktop/src-tauri/src/workflows/runtime.rs:740` and `:766`: close removes
  only the matching binding; synchronous context invalidation precedes async
  revocation. `revoke_invalidated` at `:774` only removes bindings at or before the
  captured invalidation revision, protecting a later binding from delayed cleanup.
- `yijie-desktop/src-tauri/src/workflows/window.rs:46`: page-load handling inspects
  the actual top document rather than interpreting every iframe load as a top-level
  context change. Commands use the trusted main app URL gate. The app exit callback
  at `yijie-desktop/src-tauri/src/lib.rs:435` awaits normal workflow shutdown.

This is a source review of these paths, not proof of arbitrary concurrency or
platform behavior. Actual Tauri/WebKit event ordering, E expiry and dev/packaged
reconnect qualification remain for the root-managed normal application run.

## Not executed

No App, browser automation, container or service lifecycle was run in this test
subtask. No PRIVATE file was read. No clock was advanced to fabricate actual expiry;
there was no process termination, binary substitution, permission sabotage,
malicious fixture or attack/fault injection. Broad historical suites containing
prohibited fixtures were not run. These are focused unit-test and read-only review
results, **not** real editor, real E-expiry, dev/packaged App or full FEAT-153 PASS.
