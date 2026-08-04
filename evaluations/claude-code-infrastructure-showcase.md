# Evaluation: claude-code-infrastructure-showcase

**Repo:** [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)
**Stars:** 9,985 | **Last updated:** 2026-07-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reference (setup patterns)
**Layer:** Process

---

## What it does

One developer's Claude Code setup, published as a reference: skill auto-activation, hooks, and
agents wired together. A worked example of a personal harness rather than an installable artifact.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** clone or run this. Source-grounded only: GitHub metadata plus the CATALOG one-liner
and "Overlaps with" cell (`mattpocock/skills`, `claude-plugins-official`, `agent-skills`).
Sufficient for a SKIP that turns on *redundancy with catalogued incumbents*; not sufficient for a
positive verdict, and none is offered.

## Verdict

**SKIP** — redundant with
[`claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) (STACK) and
[`agent-skills`](https://github.com/addyosmani/agent-skills) (STACK). It cites three STACK picks in
its overlap cell, which is the densest redundancy signal in this band, and it is the only one of
the three that is a personal snapshot rather than a maintained artifact.

The value of a showcase is that it shows the patterns; the value of the first-party plugin
repository is that it *ships and versions* them, and its `plugin-dev` component documents the same
hook/skill/agent wiring against the spec it tracks. Reading one dev's arrangement of those pieces
adds a data point, not a capability — and a 2026-07 snapshot of a fast-moving harness spec is the
kind of reference that rots quietly (the reason `**Last verified:**` staleness exists here at all).

Re-open if it becomes a maintained pattern library rather than a point-in-time showcase.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) | reference | Showcase of one dev's Claude Code infrastructure — skill auto-activation, hooks, and agents | Seeing how the pieces (skills, hooks, agents) fit together in a real personal setup | mattpocock/skills, claude-plugins-official, agent-skills |
