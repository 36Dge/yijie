# Workspace Test Prompt

For workspace-level changes, validate shell syntax, inspect `repos.yaml`, and verify that generated files remain inside `yijie-workspace`.

When tests support a Feature, bind their command, exit code, timestamps, repository/base/code refs, AC coverage and retained artifact digest as real v2 Evidence. `not_run` requires a reason and follow-up; planned commands, skipped environments and stale results cannot be reported as green Gate evidence. Test-only implementation changes still require a current schema v2 Package and changed-file coverage.
