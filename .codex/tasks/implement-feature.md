# Task: Implement Feature

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

- Follow `docs/dev/contract-first.md`; a downstream draft may run in parallel, but it
  cannot merge or be enabled before the contract is consumable and pinned.
- Treat behavior, errors, auth, idempotency, enums and event semantics as contract
  changes even when the DTO shape is unchanged.
- Do not introduce real token, secret, cookie, or merchant data.
- High-risk operations must go through approval policy.
- Update tests and documentation.

## Acceptance Criteria

- [ ] Contract impact classified with evidence
- [ ] Applicable authority reviewed, immutable and pinned
- [ ] Public-wire conformance/baselines or routed migration/data/runtime/deployment compatibility verified
- [ ] Implementation completed
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Security boundary reviewed
