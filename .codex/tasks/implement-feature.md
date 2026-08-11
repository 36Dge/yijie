# Task: Implement Feature

## Feature Delivery v2 Context

- Feature ID:
- Package path: `docs/features/FEAT-...`
- Schema version: `2`
- Profile: `lite | standard | controlled`
- Delivery target: `local_engineering | staging | production`
- Current Gate / instance:
- Current G2 Authorization Decision and expiry:
- Required Boundary instances (`G2C/BND-NNN`):
- Slice instance (`G3/SLC-NNN`):

## Background

Describe the business or platform reason for the change.

## Goal

Describe the concrete result expected from this task.

## Impacted Repositories

- yijie-contracts
- yijie-api
- yijie-desktop

## Contract Impact

- Classification: `none | additive | semantic | breaking`
- Reason:
- Authority type and source:
- Authority immutable ref:
- Contract PR / immutable tag / full commit (public wire only; otherwise `N/A + reason`):
- Migration / data / runtime / deployment compatibility (as applicable):
- Producer:
- Known/registered consumers:
- Consumer-owner reviews / waivers:
- Merge and rollout order:
- Compatibility window and rollback:

## Constraints

- Do not modify implementation files until the generator-created v2 Package has valid G0/G1/G2, every Boundary required by the current Slice has valid G2C, and the current G2 Authorization Packet covers the exact repository, base SHA, path, capability, environment, data class and time window.
- Codex may prepare Decision drafts and Evidence indexes, but it must not access approval private keys, sign for an owner, or turn `ELIGIBLE` into `passed`.
- Legacy v1 packages and G2A labels are historical only and cannot authorize this implementation.
- Follow `docs/dev/contract-first.md`; a downstream draft may run in parallel, but it
  cannot merge or be enabled before the contract is consumable and pinned.
- Treat behavior, errors, auth, idempotency, enums and event semantics as contract
  changes even when the DTO shape is unchanged.
- Do not introduce real token, secret, cookie, or merchant data.
- High-risk operations must go through approval policy.
- Update tests and documentation.

## Acceptance Criteria

- [ ] Feature Package is schema v2 and evaluates against its exact policy digest
- [ ] Applicable G2C/G3 instances and G4 evidence bind current repository/code refs
- [ ] Changed implementation paths pass `feature-delivery/trusted-coverage-status`
- [ ] Contract impact classified with evidence
- [ ] Applicable authority reviewed, immutable and pinned
- [ ] Public-wire conformance/baselines or routed migration/data/runtime/deployment compatibility verified
- [ ] Implementation completed
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Security boundary reviewed
