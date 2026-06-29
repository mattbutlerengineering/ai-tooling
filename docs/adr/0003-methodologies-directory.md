# ADR-0003: Home external-methodology writeups in a synced `methodologies/` directory

- **Status:** Accepted
- **Date:** 2026-06-29
- **Issue:** #173
- **Relates to:** [ADR-0001 (plugin-docs sync allowlist)](0001-plugin-docs-sync-allowlist.md)

## Context

We want to document external AI-native SDLC methodologies (the first being 8090's
Software Factory, #172) as operating-manual reference — each a stage-by-stage mapping
onto our [inner/outer dev loop](../../WORKFLOW.md) and the catalogued tools that fill
each role. The question is *where* this content lives.

[ADR-0001](0001-plugin-docs-sync-allowlist.md) frames the tension directly: `plugin/docs/`
is mirrored from an explicit file allowlist in `sync-plugin-docs.sh`, so a **new
standalone root doc does not propagate to the plugin** unless the allowlist is updated —
and the omission is silent. ADR-0001's default guidance is therefore to put cross-cutting
content *inside* an already-synced file (e.g. a `WORKFLOW.md` section) "unless the content
truly warrants its own synced file, in which case update the sync script's allowlist in
the same change."

Two options:

1. **A section per methodology inside `WORKFLOW.md`.** No new surface; auto-synced.
2. **A dedicated `methodologies/` directory**, added to the sync allowlist.

## Decision

**Create a top-level `methodologies/` directory and add it to the `sync-plugin-docs.sh`
allowlist in the same change.** Each methodology is one file.

Rationale for a directory over a `WORKFLOW.md` section:

- `WORKFLOW.md` is *our* prescribed loop. Methodology writeups are *other people's*
  models read against ours — mixing them into the prescription muddies what we recommend
  vs. what we're surveying.
- This is an open-ended, growing set (one file per methodology). Inlining N external
  frameworks into `WORKFLOW.md` would bloat the one doc every reader starts from.
- It "truly warrants its own synced file" per ADR-0001's escape hatch — methodology
  reference is operating-manual content peer to `WORKFLOW.md`, so it belongs in the
  installable plugin, not just the working tree.

## Consequences

- `methodologies/` is mirrored into `plugin/docs/methodologies/`; the `--check` gate now
  verifies its sync alongside `evaluations/` and `discovery/`. New methodology docs
  propagate automatically — no per-file allowlist edits.
- The directory is a single shared rsync line in `sync-plugin-docs.sh`; both harnesses
  (Claude Code, opencode) and CI call that one script, so there is no lockstep/drift
  surface to maintain (consistent with the lockstep invariant in `CLAUDE.md`).
- These docs are reference, not authoritative tool data — they carry no counts, verdicts,
  or Evidence fields, so the catalog drift detectors (D/G/J/K) and `reconcile-counts` do
  not apply to them.
