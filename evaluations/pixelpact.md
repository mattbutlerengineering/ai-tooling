# Evaluation: pixelpact

**Repo:** [jamalkamaladdin/pixelpact](https://github.com/jamalkamaladdin/pixelpact)
**Stars:** 20 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A CLI that extracts a design "contract" (spacing, color, type, layout rules) from a
reference page and checks a coding agent's implementation against it, returning
numeric pass/fail results instead of a human eyeballing a screenshot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is enough to place it in the
catalog and note its nearest neighbors, not to judge whether its contract-extraction
is accurate on a real design system.

## Triage note

Left at `discovery-log` rather than SKIPped: `passmark` does self-healing Playwright
*regression* testing (does the UI still work the same as before), a different question
from pixelpact's *conformance* testing (does the UI match a stated design contract).
`design-extract` extracts design tokens from a live site but doesn't check an
implementation against them. Low stars and 6 days old, but the contract-testing niche
for agent-built UI isn't otherwise covered — worth a real eval rather than a
mechanical SKIP.

_Triaged 2026-09-11 — daily discovery pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pixelpact](https://github.com/jamalkamaladdin/pixelpact) | tool | Contract-testing CLI (MIT) that extracts a design contract from a reference page and checks a coding agent's UI implementation against it, numerically | Agent-built UI is eyeballed against a reference design with no measurable pass/fail signal | passmark, design-extract, agentic-playwright |
