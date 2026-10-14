# Evaluation: human-in-the-loop

**Repo:** [tzafrir/human-in-the-loop](https://github.com/tzafrir/human-in-the-loop)
**Stars:** 25 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A Claude Code mod in which Claude assigns tasks that only the user can do; they
queue in a "My tasks" pane until the user acts, and the answer is fed back to
Claude.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped. `facet` renders agent-written Markdown as a
live local page for a click-based approval gate; `plannotator` is visual plan/diff
annotation and review; `easel` (⚠️ GPL-3.0) is a local review board with in-browser
annotation. human-in-the-loop's shape is closer to a delegated task inbox (assign,
queue, answer, feed back) than an approval gate or review surface — a different
interaction model from all three, under a clean MIT license (unlike easel). Not
plainly dominated; left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-14 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [human-in-the-loop](https://github.com/tzafrir/human-in-the-loop) | plugin | Claude Code mod (MIT) that assigns you the tasks only you can do, queued in a pane until you answer, with your answer fed back to Claude | Agents hit decisions only a human can make but have only blocking chat prompts or nothing to hand them off with | facet, plannotator, easel |
