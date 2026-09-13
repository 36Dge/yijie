# Step 5 — Infra editor overlay preparation

Date: 2026-09-12. This is implementation/static evidence only. Deployment impact is
semantic within the approved opt-in local/demo_fast FEAT-153 scope; business wire is
unchanged and remains the canonical workflow-local/bridge source.

## Implemented

- `yijie-infra/compose/workflow-editor.yml:1`: separate optional overlay, only the
  existing API service, three service-authority editor environment inputs and one
  public readonly bind mount. `create_host_path: false`; no new service, network,
  port, image, private mount or browser credential.
- `yijie-infra/scripts/workflow-local.py:127`: the base Compose file remains the
  default. The controller adds the fixed overlay only after explicit registration.
- `yijie-infra/scripts/workflow-local.py:180`: bounded normal public-file reads,
  no symlink resolution, descriptor/path identity and metadata/size stability.
- `yijie-infra/scripts/workflow-local.py:194`: reads the API deployment schema;
  validates manifest shape, identity, paths/MIME, file counts/bytes/digests and total
  budget. Runs Coze canonical `workflow-editor.mjs check` and Contracts canonical
  api/coze/desktop consumer `--check`, with normal logged completion. No build or
  install fallback. Checks exact canonical producer lock bytes and copied API/Coze
  locks, current Coze base commit, and before/after candidate/manifest stability.
- `yijie-infra/scripts/workflow-local.py:260`: `editor` requires recorded normal
  stopped state and retains registration history. It records fixed bundle path,
  manifest hash, manifest source_digest and independent Infra Coze candidate,
  producer/consumer lock hashes, deployment schema hash, entry and byte budget.
  Current equality of the two candidate algorithms is not used as runtime proof.
- `yijie-infra/scripts/workflow-local.py:406` and `:429`: build/up compare the whole
  registration with fresh canonical verification before and after normal execution.
  Drift rejects continuation and retains state/data. The controller does not
  automatically rebuild an editor or cancel its registration.
- `yijie-infra/scripts/workflow-local.py:272` and `:328`: readiness keeps all six
  healthy primary services and authenticated host status. Registered editor mode
  additionally checks unauthenticated fixed-loopback `/editor/` HTML hash/bytes,
  no-store/nosniff/no-referrer and the exact API CSP. No credentials are attached
  to that static request.
- `yijie-infra/Makefile:250` and `yijie-infra/docs/workflow-local.md:44`: explicit
  `make workflow-editor` → build → up sequence after canonical bundle completion
  and normal stop; API-only default behavior and lifecycle retention documented.

## Verification actually run

1. `pnpm validate:workflow` — PASS, once.
2. `pnpm test:workflow` — PASS, once, 13/13 tests. The three added checks inspect
   the actual overlay, canonical registration boundaries and public readiness;
   the original ten lifecycle/topology/PG/CAS checks still pass.
3. `python3 -c 'import ast,pathlib; ast.parse(pathlib.Path("scripts/workflow-local.py").read_text()); print("Python syntax PASS; no lifecycle action executed")'`
   — PASS, once; no module lifecycle invocation.
4. `git diff --check` — PASS, once.
5. Manual read-only comparison with
   `yijie-api/config/workflow-editor-assets.schema.json`, API editorassets handler,
   and `yijie-coze/scripts/yijie/workflow-editor.mjs`: directory, schema budgets,
   MIME/path rules, producer source-lock hash and CSP agree.

The focused model/test additions are at
`yijie-infra/scripts/workflow-local-model.mjs:253` and
`yijie-infra/tests/workflow-local.test.mjs:60`.

## Not run / remaining qualification

- This subtask did not read/write the PRIVATE directory, run `editor`, install or
  build sources, invoke Docker/Compose, migrate, start/stop services, or make HTTP
  requests. The real bundle was still being completed by its owner; canonical
  registration and overlay Compose semantics/runtime remain NOT RUN here.
- Parent/root schedules canonical bundle completion → registration → exact image
  build → normal up. Only successful actual `/editor/` and browser/native checks
  can close the runtime qualification; these static tests do not prove iframe
  load, MessageChannel, save, E expiry, reconnect, or dev/packaged WebKit behavior.
- Historical attack/permission-fault/strong-kill fixtures and broad historical
  test suites were not run under the user's permanent safety instructions.
  No failure injection, executable substitution, forced termination or permission
  sabotage was used. Result is focused static PASS, not full repository/runtime PASS.
