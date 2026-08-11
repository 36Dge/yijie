# Workspace Review Prompt

Review changes for repository boundary drift, missing ADR updates, contract-first
violations, security omissions, and scripts that assume unavailable local
infrastructure. Require contract-impact classification, authority, immutable ref,
consumer pins, directional compatibility, conformance, rollout, and rollback evidence.

For every non-governance implementation path, verify that a `schema_version: 2` Feature Package owns the change, the current G2 scope covers the exact repository/base/path, applicable G2C and G3/G4 instances bind current evidence and code refs, approvals verify against the protected trust root, and `feature-delivery/trusted-coverage-status` comes from the expected App. Legacy v1 status and `ELIGIBLE` are never PASS.
