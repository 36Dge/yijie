# Task: Fix Bug

## Feature Delivery v2 Context

- Feature ID / Package path:
- Schema version: `2`
- Profile / Delivery target:
- Current G2 Authorization Decision and expiry:
- Required G2C / G3 instances:

Use an existing v2 Package only when the fix is within its current scope and authorization. Otherwise create a new generator-produced maintenance Feature before changing implementation. Historical v1 packages cannot authorize the fix.

## Problem

Describe the observed behavior and expected behavior.

## Scope

List affected repositories, modules, APIs, and user flows.

## Contract Impact

- Classification: `none | additive | semantic | breaking`
- Reason:
- Authority type/source and immutable ref:
- Contracts PR/baselines or routed migration/data/runtime/deployment compatibility:
- Producer / consumers:
- Applicable compatibility baselines:
- Compatibility and rollback:

## Verification

- [ ] Current G2 scope covers the exact repository, base SHA and changed paths
- [ ] Applicable G2C/G3/G4 Decisions and Evidence bind the fixed code
- [ ] `feature-delivery/trusted-coverage-status` passes
- [ ] Regression test added or updated
- [ ] Contract direction and producer/consumer conformance verified if applicable
- [ ] Relevant local command executed
- [ ] Logs and sensitive data are redacted
