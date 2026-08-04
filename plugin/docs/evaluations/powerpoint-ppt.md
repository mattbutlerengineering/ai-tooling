# Evaluation: powerpoint-ppt

**Repo:** [PracticalSwan/agent-skills](https://github.com/PracticalSwan/agent-skills)
**Stars:** 3 | **Last updated:** 2026-06-23 (pushed) | **License:** MIT
**Dev loop stage:** Skills & Plugins (presentations)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

PowerPoint `.pptx` manipulation through an MCP server — slides, placeholders, templates, images.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell. Overlaps cited: `powerpoint`, `slidev`,
`open-slide`. Sufficient for a SKIP that turns on redundancy with a catalogued incumbent; not sufficient
for a positive verdict, and none is offered.

## Verdict

**SKIP** — superseded by a catalogued incumbent, and the CATALOG row already says so in its own one-liner:
*"⚠️ source collection low adoption, 3★"*.

Three stars is not a signal to interpret; it is the absence of one. The catalogued `powerpoint` skill covers
`.pptx` manipulation, `wowerpoint` covers AI-written business decks, and `open-slide` covers agent-authored
web decks with a visual edit loop. There is no gap here for a fourth implementation from a collection with
no adoption behind it.

Worth stating that the disclaimer already in the row is the honest thing to have done at entry time, and
this verdict is just following it through. A catalog that flags a weak row and then never disposes it
accumulates exactly the drift this triage band exists to clear.

MIT, pushed 2026-06-23, so it is neither abandoned nor broken — simply redundant.

Re-open if the source collection gains adoption or the skill develops something `powerpoint` lacks.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [powerpoint-ppt](https://github.com/PracticalSwan/agent-skills) | skill | PowerPoint .pptx manipulation via MCP server — slides, placeholders, templates, images (⚠️ source collection low adoption, 3★) | Need programmatic .pptx editing/formatting when MCP presentation tools are available | powerpoint, slidev, open-slide |
