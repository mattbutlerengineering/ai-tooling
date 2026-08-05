# Evaluation: deadeye-cc

**Repo:** [deepaksinghcs14/deadeye-cc](https://github.com/deepaksinghcs14/deadeye-cc)
**Stars:** 3 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (plugin/hooks)

---

## What it does

A Claude Code plugin that fits the model, effort, and context window to each task through a
deterministic, hooks-based policy kernel — every number it reports is measured, not
estimated.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (claude-code-router, litellm, codeburn). That
is sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: claude-code-router and litellm route *between providers*; codeburn
*reports* spend after the fact. None proactively fits model/effort/context *to the task
before it runs* via a deterministic hooks-based policy. A real, differently-timed
optimization worth a hands-on look rather than a redundancy SKIP. Very early (3 stars).

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
