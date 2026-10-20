# Evaluation: natural-intelligence

**Repo:** [itsaspacestation/natural-intelligence](https://github.com/itsaspacestation/natural-intelligence)
**Stars:** 1 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** Apache-2.0
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin (skills, slash commands, and subagents) for planning,
building, reviewing, and merging software work, built around keeping a human in
the loop on key decisions rather than handing judgement fully to the agent.

## How we tested it

**Evidence:** SOURCE-ONLY

**Source-grounded review — not run hands-on.** This session's GitHub access is
scoped to `mattbutlerengineering/ai-tooling` only; arbitrary-repo API lookups and
installs are not available without an explicit `add_repo` grant, which an
unattended discovery pass does not request. This read comes from the repo's public
GitHub page (About text, README) via a web fetch, not from running the tool.

## What worked

- N/A — not run.

## What didn't work or surprised us

- N/A — not run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not exercised. |
| Speed | neutral | Not exercised. |
| Maintainability | neutral | Not exercised. |
| Safety | neutral | Not exercised. |
| Cost Efficiency | neutral | Not exercised. |
| Verifiability | neutral | Not exercised. |

## Triage note

Left at `discovery-log` — a P3 backlog lead. It cites `superpowers` and
`compound-engineering` in `CATALOG.md`'s Overlaps column, but it did not land in the
P2 challenger band, so it isn't being bulk-SKIPped as redundant here. At 1 star it is
a very early, single-author plugin with no stated differentiator yet over the
established methodology plugins it resembles; left for a real hands-on eval rather
than a mechanical SKIP, since "redundant" is not this lane's to assert on a tool this
new and under-described.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [natural-intelligence](https://github.com/itsaspacestation/natural-intelligence) | plugin | Claude Code skills/commands/subagents plugin for keeping a human in the loop across planning, building, reviewing, and merging | Agentic workflows tend to hand over too much judgement; want a structured methodology that keeps the human deciding | superpowers, compound-engineering |
