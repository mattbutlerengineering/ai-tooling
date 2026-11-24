# Evaluation: filament

**Repo:** [invertibleMatrix/filament](https://github.com/invertibleMatrix/filament)
**Stars:** 26 | **Last updated:** 2026-11-22 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

An agent harness giving your own agent, on any model, and every coding agent already on your computer, one shared memory — cross-tool rather than per-tool persistence.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — cross-agent shared memory, a different value proposition than a single-tool memory plugin.

## Triage note

Left at `discovery-log`, not SKIPped. It cites `beads` and `claude-mem` in Overlaps, but both are memory upgrades for a single coding agent, while filament's stated job is sharing one memory *across* every agent on a machine (Claude Code, Codex, etc. at once) — a cross-harness capability neither incumbent offers. Left for a real eval.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [filament](https://github.com/invertibleMatrix/filament) | harness | Agent harness (Apache-2.0) giving your own agent, on any model, and every coding agent on your computer, one shared memory | Each coding agent on a machine keeps its own memory, so nothing learned in one tool carries over to another | OMEGA, claude-mem, beads |
