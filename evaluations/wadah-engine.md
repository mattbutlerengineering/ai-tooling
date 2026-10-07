# Evaluation: wadah-engine

**Repo:** [techwadah-web/wadah-engine](https://github.com/techwadah-web/wadah-engine)
**Stars:** 8 | **Last updated:** 2026-10-07 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-07
**Last triaged:** 2026-10-07  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local, read-only MCP server and CLI, written in Rust with tree-sitter, that gives AI coding
assistants a commit-pinned map of your codebase, per the repo description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to compare it against the
already-adopted incumbent's stated job, not to judge its output hands-on.

## Verdict

**SKIP** — redundant with [`codegraph`](https://github.com/colbymchenry/codegraph) (STACK, `MEASURED`, ADOPT). `codegraph` is the first-party incumbent for exactly this job — an always-on code-intelligence graph that agents query instead of reading whole files, auto-syncing as the codebase changes. wadah-engine advertises a commit-pinned (i.e. point-in-time, not continuously synced) codebase map over the same MCP-server shape, with no stated capability `codegraph` lacks. A two-day-old, 8-star tool claiming the identical structural-awareness job, with "pinned to one commit" read as a narrower feature rather than a differentiator, does not clear the bar for a second tool in the same slot.

## Triage note

P2 challenger — the row's `Overlaps with` cell names `codegraph`, a STACK pick, directly. Both are
MCP servers giving agents a structural map of the codebase instead of raw file reads; `codegraph`
already covers the always-on case and auto-syncs, which is the harder and more useful version of
what wadah-engine does. No README claim here (API design, performance, language coverage) points to
an axis `codegraph` is weak on. SKIP is the defensible, reversible call.

_Triaged 2026-10-07 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [wadah-engine](https://github.com/techwadah-web/wadah-engine) | MCP server | Local, read-only MCP server + CLI (Apache-2.0) giving coding agents a commit-pinned map of your codebase | Agent structural awareness goes stale as a session edits files; want a codebase map pinned to a specific commit instead of re-scanned ad hoc | codegraph, Understand-Anything, graphify |
