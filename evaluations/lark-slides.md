# Evaluation: lark-slides

**Repo:** [larksuite/cli](https://github.com/larksuite/cli)
**Stars:** 15,368 | **Last updated:** 2026-07-10 (pushed) | **License:** MIT
**Dev loop stage:** Skills & Plugins (presentations)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A Lark/Feishu slides skill from the official larksuite CLI — 20+ agent skills and 200+ commands for
creating and editing presentations inside Lark rather than exporting files.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell. Overlaps cited: `googleworkspace/cli`,
`slidev`. Enough to place it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. First-party, MIT, ★15.4K, pushed 2026-07-10 — a vendor integration of exactly the
shape the Skills & Plugins blurb admits: a domain-specific capability, worth everything to teams inside that
ecosystem and nothing to everyone else.

Not swept up with the three presentation rows disposed in this pass, and the difference is worth stating.
`pitch-deck` went for a nine-month-dormant source collection, `powerpoint-ppt` for a ★3 collection superseded
by the catalogued `powerpoint`, `giving-presentations` for coaching a human rather than an agent. This row
is actively maintained, first-party, and *acts on a live system* — decks inside Lark, not files exported
from it. That is a different kind of capability from another deck generator, and the closest analogue here
is `googleworkspace/cli`, its named peer for a different suite.

The honest scope note is that neither Lark nor Google Workspace is where software gets written. This is
outer-loop communication tooling, findable when that is the question — a row to keep, not a lead to promote.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lark-slides](https://github.com/larksuite/cli) | skill | Lark/Feishu slides skill from the official larksuite CLI (MIT, 15K★, 20+ agent skills + 200+ commands) | Need agents to create/edit presentations in Lark/Feishu rather than .pptx or HTML | googleworkspace/cli, slidev |
