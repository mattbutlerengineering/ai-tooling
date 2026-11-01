# Evaluation: stack-diagram

**Repo:** [caru-ini/stack-diagram](https://github.com/caru-ini/stack-diagram)
**Stars:** 83 | **Last updated:** 2026-11-01 (pushed) | **License:** MIT
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A Claude Code skill: describe your stack in a sentence and get back an architecture diagram rendered with official vendor logos, instead of hand-drawing one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It shares the "visualize your system" job with `floorplan` and `mycel`, but neither of those is a STACK pick and the approach (one-sentence-to-diagram, vendor-logo rendering) is distinct enough from both to deserve a first-time hands-on look rather than a mechanical disposal.

## Triage note

No STACK-pick overlap (floorplan, mycel, codegraph are cited but only `codegraph` is in STACK, and it is a code knowledge graph, not a stack-description diagrammer). P3 backlog — nothing structural turns this into a SKIP; left at `discovery-log` with a stamp.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stack-diagram](https://github.com/caru-ini/stack-diagram) | skill | Claude Code skill (MIT) turning a one-sentence stack description into an architecture diagram with official vendor logos | Drawing an accurate architecture diagram with correct vendor logos is slow manual work for a one-off explainer | floorplan, mycel, codegraph |
