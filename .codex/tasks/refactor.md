# Task: Refactor

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
