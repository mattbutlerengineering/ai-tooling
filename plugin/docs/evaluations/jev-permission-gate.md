# Evaluation: jev-permission-gate

**Repo:** [madisonrickert/jev-permission-gate](https://github.com/madisonrickert/jev-permission-gate)
**Stars:** 30 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code mod that sends each auto-mode tool call to TypeSafe's Jev, a cheap
yes/no safety classifier, and allows or denies the call (or passes it to Claude
Code's own built-in classifier) based on the answer.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped. `toolpermit` is a local-first permission
firewall but is not itself Jev-powered; `jev-judge-mcp` exposes Jev's judgment
model generically via MCP; `jev-use` hands steps needing no text output to Jev.
jev-permission-gate is the first catalogued tool specifically wiring Jev into
Claude Code's own auto-mode approval path as a drop-in for (or override of) the
built-in classifier — a narrower, more specific claim than any of the three. Not
plainly redundant with any; left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-14 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jev-permission-gate](https://github.com/madisonrickert/jev-permission-gate) | plugin | Claude Code mod (MIT) routing auto-mode tool-call decisions through TypeSafe's Jev classifier instead of the built-in one | Auto-mode tool-call approval relies on Claude Code's own classifier with no faster/cheaper alternative to compare in | toolpermit, jev-judge-mcp, jev-use |
