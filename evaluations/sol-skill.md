# Evaluation: sol-skill

**Repo:** [ozankasikci/sol-skill](https://github.com/ozankasikci/sol-skill)
**Stars:** 12 | **Last updated:** 2026-07-29 (pushed) | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process (skill)

---

## What it does

Claude Code skill that delegates implementation to GPT-5.6 Sol via Codex CLI — Claude plans and
reviews the diff, Sol writes the code, so the model that wrote the diff never grades it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (architect-loop, agents-council, claude-octopus). That is
sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's
behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `architect-loop` (Claude Fable 5 as architect, GPT-5.5 Codex as builder —
the identical cross-vendor architect/builder split, already catalogued). sol-skill swaps in a
different builder model (Sol via Codex CLI) but the technique — separate the model that writes the
diff from the model that reviews it — is the same job architect-loop already covers, with far less
traction (12 stars vs. an established entry).

_Triaged 2026-08-03 as part of today's discovery intake, not a P1/P2/P3 bulk-band pass._
