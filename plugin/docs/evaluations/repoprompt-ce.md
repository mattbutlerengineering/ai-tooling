# Evaluation: repoprompt-ce

**Repo:** [repoprompt/repoprompt-ce](https://github.com/repoprompt/repoprompt-ce)
**Stars:** 850 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Plan (context engineering)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Community edition of RepoPrompt — a native macOS context-engineering app with an MCP CLI for curating
exactly which files reach the model.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell (`repomix`, `opensrc`, `code-context-engine`). Enough to place
it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Its premise — pasting whole repos wastes tokens and dilutes focus, so curate the
context by hand before prompting — is one of the few in the Plan stage with an unambiguous measurement
attached: token count and task success, with and without curation, on a disclosed task set.

Not disposed. `repomix` packs a repo into one file, `opensrc` reads dependency source at the resolved
version, `code-context-engine` indexes for retrieval; this row is the *human-in-the-loop selection* surface,
which is a different intervention from all three. The overlap cell reads like a redundancy cluster and is
not one.

Two things to weigh at promotion. It is **macOS-native**, which is a platform constraint the catalog has
disposed rows over in the other direction (`code-on-incus` is Linux-only) — here it happens to match this
environment, and that is luck rather than a property of the tool. And "community edition" signals an
open-core split, so the Apache-2.0 grant covers this tree and not necessarily the full product; the same
shape as `agent-vault`'s reserved `ee/` directory and `sentrux`'s BSL Pro tier.

★850 and pushed today.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [repoprompt-ce](https://github.com/repoprompt/repoprompt-ce) | tool | Community edition of RepoPrompt — native macOS context-engineering app for AI coding agents, with an MCP CLI for curating exactly which files reach the model (Apache-2.0) | Pasting whole repos wastes tokens and dilutes focus; need hand-curated, structured context selection before prompting an agent | repomix, opensrc, code-context-engine |
