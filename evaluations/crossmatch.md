# Evaluation: crossmatch

**Repo:** [filip131311/crossmatch](https://github.com/filip131311/crossmatch)
**Stars:** 35 | **Last updated:** 2026-09-11 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Finds where an iOS app and its Android counterpart disagree — feature parity, layout, and behavior — and produces a side-by-side video of every difference it finds, rather than a text diff.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `SceneProof`, `passmark`, and `midscene` on visual/UI verification, but none is a STACK pick, and its specific angle — cross-platform (iOS vs Android) parity checking with a rendered video diff, rather than single-platform visual regression — looks differentiated enough to leave for a real look rather than a mechanical SKIP. 35★ and 4 days old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [crossmatch](https://github.com/filip131311/crossmatch) | tool | Cross-platform QA diffing for iOS/Android (MIT) — finds where the two apps disagree and renders a side-by-side video | Verifying iOS/Android feature parity means manually comparing two apps screen by screen | SceneProof, passmark, midscene |
