# yijie-codex Runtime Freeze Evidence

> Captured before implementation: `2026-08-26T10:01:56+08:00`
> Evidence classification: `real-runtime-metadata`
> Runtime repository is strictly read-only for FEAT-131.

## Before snapshot

| Field | Frozen value | Authority |
|---|---|---|
| Yijie Runtime repository HEAD | `0ce5902ed400866be0196886bb78f693a004d68d` | `git rev-parse HEAD` in `yijie-codex` |
| Runtime worktree | `clean` | empty `git status --porcelain=v1` |
| Upstream tag | `rust-v0.144.6` | `.yijie/upstream.env` + schema baseline |
| Upstream commit | `5d1fbf26c43abc65a203928b2e31561cb039e06d` | `.yijie/upstream.env` + schema baseline |
| Runtime version | `0.144.6` | `.yijie/upstream.env` + compatibility manifest |
| Schema file count | `267` | `yijie-contracts/compatibility/agent-host-runtime-v1.json` |
| Schema tree SHA-256 | `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` | canonical `runtime_manifest.sha256_tree` computation |
| Experimental API | `false` | `.yijie/schemas/app-server/baseline.json` + compatibility manifest |
| Runtime transport | `stdio` | schema baseline + compatibility manifest |

The local Runtime branch is one commit behind `origin/develop`. That drift is intentionally preserved: FEAT-131 must not fetch, pull, rebase, checkout, generate, build, replace, or upgrade the Runtime.

## Locked Host projection snapshot

- Contracts source commit: `164b14f609537d727a52326832da04430aecc4ab`
- Compatibility manifest SHA-256: `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311`
- Host transport/auth/safety: `local-http-sse` / `owner-only-bearer` / `read-only` / approval policy `never`.
- Locked methods: `skills/config/write`, `skills/extraRoots/set`, `skills/list`, `thread/resume`, `thread/start`, `turn/interrupt`, `turn/start`.
- Locked notifications: `error`, `item/agentMessage/delta`, `item/completed`, `item/started`, `skills/changed`, `thread/started`, `turn/completed`, `turn/started`, `warning`.

Implementation code paths not listed above are recorded only as `implementation extension observed`; FEAT-131 does not promote them to supported projection.

## After snapshot

> Captured after implementation, final isolated canonical startup and automated verification: `2026-08-26T13:07:39+08:00`

| Field | After value | Comparison |
|---|---|---|
| Yijie Runtime repository HEAD | `0ce5902ed400866be0196886bb78f693a004d68d` | exact match |
| Runtime worktree | `clean` | exact match |
| Schema file count | `267` | exact match |
| Schema tree SHA-256 | `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1` | exact match |
| Contracts repository HEAD | `164b14f609537d727a52326832da04430aecc4ab` | unchanged authority |
| Compatibility manifest SHA-256 | `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311` | exact match |
| Experimental API baseline | `false` | unchanged; canonical stable `/v1/status` also observed `experimental_api=false` |

Canonical hash calculation used the repository-owned `scripts/runtime_manifest.py::sha256_tree` over `.yijie/schemas/app-server/generated-json-schema`; a generic shell tree hash is not equivalent and is not used as evidence.

### 2026-08-27 scope-amendment recheck

Read-only recheck at `2026-08-27T01:03:50+08:00` again returned Runtime HEAD `0ce5902ed400866be0196886bb78f693a004d68d`, clean worktree, 267 schema files and tree SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`. The Contracts checkout also remained clean at `164b14f609537d727a52326832da04430aecc4ab`; `compatibility/agent-host-runtime-v1.json` SHA-256 remained `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311`.

An additional read-only `python3 scripts/check_agent_host_contracts.py` diagnostic returned non-zero because the Runtime-side checker expects the Host projection without `skills/config/write`, `skills/extraRoots/set`, `skills/list` and `skills/changed`, while the unchanged Contracts manifest includes them. This is a pre-existing checker/manifest expectation mismatch, not Runtime drift and not caused by the FEAT-131 policy amendment. The hard Runtime constraint forbids changing either Runtime code or schema to make this optional diagnostic green; the mismatch is therefore reported rather than patched or hidden.

### 2026-08-27 final D4 recheck

Read-only recheck at `2026-08-27T01:38:36+08:00` again returned Runtime HEAD `0ce5902ed400866be0196886bb78f693a004d68d`, clean worktree, 267 schema files and the canonical tree SHA-256 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`. Contracts remained clean at `164b14f609537d727a52326832da04430aecc4ab`; the compatibility manifest SHA-256 remained `5eadca026cdc8813cf529fa8e074de7532a2c78bebc5c89d9364180942869311`.

## Canonical stable startup observation

The Desktop-local `pnpm tauri:demo-fast:stable` entrypoint freshly built the isolated `com.yijie.ai.feat131-stable` Yijie debug App, used its own Desktop app-data and `.local/feat131-stable` Host/Codex home, and launched the already pinned Runtime through the normal Host/Sidecar path. It did not build, replace or edit the Runtime.

For the final current implementation, the authorized happy-path run and the later safe failure/retry run showed:

- `/readyz` returned `status=ready` and `runtime_state=ready`;
- `/v1/status` reported Runtime `0.144.6`, `ready=true`, `model_provider=minimax`, model `MiniMax-M3`, transport `stdio`, and `experimental_api=false`;
- the authorized happy-path run selected a clean detached worktree and submitted exactly one no-sensitive-data text prompt that explicitly prohibited tools and file reads/writes; the UI Turn completed with the exact response `FEAT-131_SMOKE_OK`, with no tool call and no retry;
- while a freshly built canonical first instance was ready, a direct second launch of the same stable bundle exited `1` with the stable message `yijie desktop instance is already running`; the first instance remained ready with `experimental_api=false`;
- after normally exiting that first instance, the canonical entry restarted to ready again; after the final normal quit, the App, Host and Runtime exited, ports `18081`/`1420` were released and no owned process remained.

The predecessor-entry UI submission had produced no observed Runtime `thread_started`, `turn_started`, `assistant_delta` or `turn_completed` event, so it remains a separate `pre-runtime: FAIL` and is not rewritten as successful evidence. Together with the current successful request it exhausts the `yijie-agent-host` repository's stricter two-short-request total gate; no paid retry was used or remains permitted.

The unchanged Host implementation still contains `Process.Kill()` fallbacks for Runtime shutdown timeout, protocol failure and startup abort. Those paths were not triggered or fault-injected. The real representative failure is limited to stable-only second-instance rejection plus a normal canonical restart; neither that result nor normal `Cmd-Q` may be generalized into an end-to-end abnormal-cleanup guarantee.

Result: **PASS for AC-008**. No fetch, pull, rebase, checkout, Runtime generation/build, binary replacement, schema edit or Runtime file edit was performed. The Runtime remains one commit behind `origin/develop` exactly as captured before implementation.
