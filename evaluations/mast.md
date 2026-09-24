# Evaluation: mast

**Repo:** [ex3del/mast](https://github.com/ex3del/mast)
**Stars:** 5 | **Last updated:** 2026-09-23 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that runs several agents in parallel from one terminal — a dispatcher assigns
tasks, each gets its own git worktree, and a docs directory is kept as the single source of truth
across the parallel runs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (claude-squad, agent-of-empires, stargate). That is sufficient
to place the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-squad` despite the overlap citation.
The parallel-agents-in-worktrees niche already holds several coexisting, non-SKIPped leads with
distinct angles on the same job (`agent-of-empires` — tmux/Docker/remote-phone; `stargate` —
vendor-agnostic token-budgeted orchestration; `diri` — native macOS remote-host orchestrator), so a
new entrant is not automatically dominated by the STACK incumbent. At 5 stars and 4 days old, mast's
own differentiator ("docs as the single source of truth") is too thin to verify from source alone,
but it is no thinner than the untested claims already carried by its uncontested peers — not a
reason to SKIP one arrival in a crowded field while leaving the rest.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mast](https://github.com/ex3del/mast) | plugin | Claude Code plugin (MIT) running several agents in parallel from one terminal — a dispatcher, a worktree per task, docs as source of truth | Running multiple agents in parallel from a single terminal means hand-rolled worktrees with no shared source of truth | claude-squad, agent-of-empires, stargate |
