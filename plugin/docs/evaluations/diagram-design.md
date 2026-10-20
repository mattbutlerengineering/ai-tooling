# Evaluation: diagram-design

**Repo:** [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)
**Stars:** 58,800 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** MIT
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Plan / Reflect (outer loop)
**Layer:** Process

---

## What it does

An agent skill for Claude Code, Codex, GitHub Copilot, Cursor, Factory Droid, and
Pi that draws editorial-quality diagrams — 44 types — as a single, self-contained
HTML+SVG file styled to match a given brand, with no shadows. It can also redraw
existing draw.io, Mermaid, and Excalidraw files into the same style.

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

Left at `discovery-log` — a P3 backlog lead, and deliberately not a mechanical SKIP.
At ~58.8K stars and genuinely broader scope than any single existing diagram skill in
the catalog (44 diagram types, multi-harness, redraws existing draw.io/Mermaid/
Excalidraw files rather than only generating new ones), this is a significant,
differentiated tool that deserves a real hands-on eval, not a "redundant with
`archify`"-style dismissal — eliminate-only bulk triage is not the lane to make that
call on a tool this prominent. Flagging for `P0`/`eval-runner`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [diagram-design](https://github.com/cathrynlavery/diagram-design) | skill | Editorial diagram-design skill (MIT, ★59K) for Claude Code, Codex, Copilot, Cursor and more — 44 diagram types as self-contained HTML+SVG, can redraw existing draw.io/Mermaid/Excalidraw files | Agent-drawn diagrams look generic or inconsistent with brand style; want editorial-quality diagrams across many types, not just one format | excalidraw-diagram-skill, SeeCode, archify |
