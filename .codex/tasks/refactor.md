# Task: Refactor

## Feature Delivery v2 Context

- Feature ID / Package path:
- Schema version: `2`
- Profile / Delivery target:
- Current G2 Authorization Decision and expiry:
- Slice instance:

Reference a current v2 Package whose scope explicitly includes the refactor, or create a generator-produced maintenance Feature before changing implementation. A behavior-preserving classification does not waive v2 authorization or changed-file coverage.

## Goal

Describe what becomes simpler, safer, or easier to evolve.

## Contract Impact

- Classification: `none | additive | semantic | breaking`
- Reason:

## Guardrails

- Preserve public contracts unless explicitly changed in `yijie-contracts`.
- A behavior-preserving refactor must justify `none`; transport, error, auth, default,
  ordering or SDK-surface changes follow `docs/dev/contract-first.md`.
- Do not move business logic across repository boundaries.
- Keep behavior covered by tests.
- Require current G2/G3/G4 evidence and `feature-delivery/trusted-coverage-status`; legacy v1 status cannot authorize the refactor.
