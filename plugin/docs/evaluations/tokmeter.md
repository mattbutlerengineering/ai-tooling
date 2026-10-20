# Evaluation: tokmeter

**Repo:** [sriinnu/tokmeter](https://github.com/sriinnu/tokmeter)
**Stars:** 1 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** AGPL-3.0
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Reads the local session logs that AI coding agents (Claude Code, Codex, and others)
already write to disk, and turns them into token and cost totals broken down by
project, model, provider, and day — entirely locally, no telemetry sent out.

## How we tested it

**Evidence:** SOURCE-ONLY

**Source-grounded review — not run hands-on.** This session's GitHub access is scoped
to `mattbutlerengineering/ai-tooling` only; arbitrary-repo API lookups and installs
are not available without an explicit `add_repo` grant, which an unattended discovery
pass does not request. This read comes from the repo's public GitHub page (About
text, README, file tree) via a web fetch, not from running the tool or calling the
GitHub API.

## What worked

- N/A — not run.

## What didn't work or surprised us

- N/A — not run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not exercised; no accuracy claim to check. |
| Speed | neutral | Not exercised. |
| Maintainability | neutral | Not exercised. |
| Safety | neutral | Reads local log files only, per its own description; no elevated access claimed. |
| Cost Efficiency | neutral | The tool's whole purpose is cost *visibility*, not a change to spend itself. |
| Verifiability | neutral | Not exercised. |

## Triage note

Left at `discovery-log` rather than SKIPped. It cites `abtop` (a STACK pick) in
`CATALOG.md`'s Overlaps column, which puts it in `NEXT-EVALS.md`'s P2 challenger band,
but the two aren't a clean redundancy: `abtop` is a real-time TUI for watching live
agent sessions (tokens/context%/rate limits/ports across projects right now), while
tokmeter reads historical session logs into retrospective cost totals by project,
model, provider, and day (a billing ledger, not a live monitor). That's a genuine
difference in job, not just presentation, so a mechanical "redundant with abtop" SKIP
would misdescribe it. Left for a real hands-on eval if someone wants a cost-ledger
tool; note the AGPL-3.0 license if it's ever considered for anything beyond running it
as a standalone local CLI.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tokmeter](https://github.com/sriinnu/tokmeter) | tool | Reads local session logs from AI coding agents (⚠️ AGPL-3.0) to produce token/cost totals by project, model, provider, and day, entirely locally | Can't tell what AI coding sessions actually cost without stitching together logs from several tools by hand | tokencost, abtop, Infracost |
