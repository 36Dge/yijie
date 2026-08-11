# Workspace Development Prompt

Use this prompt when changing workspace-level documentation, scripts, repository manifests, or architecture governance.

Always read `AGENTS.md`, `SECURITY.md`, `repos.yaml`, `docs/dev/codex-project-memory.md`, the Feature Delivery v2 README/HANDBOOK, and the relevant architecture or ADR files before editing.

For every new requirement, create a generator-produced `schema_version: 2` Feature Package before changing implementation files. Do not copy legacy v1 packages. Treat G2C as a per-Boundary instance, require a current bounded G2 Authorization Packet before implementation, and require the relevant G3/G4 evidence plus `feature-delivery/trusted-coverage-status` before merge. Codex may draft Decisions but must never access approval private keys or self-approve a Gate.
