# Plugin docs sync uses an explicit file allowlist, not a glob

Status: accepted

`sync-plugin-docs.sh` mirrors root documentation into `plugin/docs/` by copying a
fixed, named set of files — `CATALOG.md`, `WORKFLOW.md`, `STACK.md`,
`STACK-LEDGER.md`, plus the `evaluations/` and `discovery/` trees — rather than
globbing every root-level `*.md`. We chose an allowlist so the installable plugin
never picks up internal or working docs (`CLAUDE.md`, `README.md`, `COMPARISON.md`,
`docs/`) by accident.

## Consequences

- A **new standalone root doc does not propagate** to `plugin/docs/` until it is added
  to `sync-plugin-docs.sh`. The omission is silent — no error, the file simply never
  appears in the plugin.
- Therefore, **put cross-cutting content inside an already-synced file** (e.g. a new
  section in `WORKFLOW.md`) rather than a new top-level doc — unless the content truly
  warrants its own synced file, in which case update the sync script's allowlist in the
  same change.
- The `--check` gate only verifies drift for allowlisted files, so it cannot warn you
  about a never-synced new doc.
