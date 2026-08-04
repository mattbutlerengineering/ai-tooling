# Evaluation: softaworks/agent-toolkit

**Repo:** [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)
**Stars:** 2,169 | **Last updated:** 2026-03-05 (pushed) | **License:** MIT
**Dev loop stage:** All stages (general skill collection)
**Layer:** Tooling (agent skills)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A curated collection of skills for AI coding agents spanning development, documentation, planning, and
general professional workflows — a general-purpose pack rather than a domain or vendor one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell (`NVIDIA/skills`, `tech-leads-club/agent-skills`,
`awesome-agent-skills`). Enough to place and band it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, but with a **banding defect** worth recording, because it is about the queue
rather than the tool.

This is a *general-purpose* skills pack, so its real competitor is `agent-skills` (addyosmani) — a
STACK pick with an ADOPT verdict — and a general pack competing with an installed general pack is the
textbook **P2 challenger** case. It never reached that band. `triage.py` computes the band from the
`Overlaps with` cell, and this row's cell names only `NVIDIA/skills`, `tech-leads-club/agent-skills`
and `awesome-agent-skills` — three leads, none of them in STACK — so the lead sorted to P3 where the
challenger disposal is not available.

The general shape: **a mis-pointed overlaps cell can keep a lead out of the one band that could
dispose it.** Detector `--overlaps` catches tokens naming tools that are not catalogued; it cannot
catch a cell that names real catalogued tools while omitting the incumbent that matters.

Not SKIPped anyway. Writing "redundant with `agent-skills`" here would need a read of what these
skills actually contain, and this pass has only the one-liner. The correct outcome is to fix the cell
so the next run bands it as a challenger and a pass with the tree in view can decide.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) | skill | Curated skills for AI coding agents (MIT, ★2.1K) — dev, docs, planning, and professional workflows | Finding high-quality, production-ready agent skills across workflow categories is hard | NVIDIA/skills, tech-leads-club/agent-skills, awesome-agent-skills |
