# Evaluation: SlopSquatShield

**Repo:** [agivanttechnologies/SlopSquatShield](https://github.com/agivanttechnologies/SlopSquatShield)
**Stars:** 53 | **Last updated:** 2026-11-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-27
**Last triaged:** 2026-11-27  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Checks the packages a developer or their AI coding agent installs and blocks names
that don't exist or look like slopsquatting traps (hallucinated or typosquatted
package names an LLM invents or a bad actor plants). Supports npm, PyPI, and Maven;
runs in the terminal, in AI agent hooks, on `git commit`, and in the IDE.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata from GitHub's search API (this session's
GitHub access is scoped to this repo only, so a direct per-repo metadata fetch was
not available; stars/license/pushed-date come from the search endpoint instead).

## Triage note

Left at `discovery-log` — cites no STACK pick in its "Overlaps with" cell
(`agentshield`, `agent-scan`, `skylos` are catalogued peers but none is installed in
STACK today), so no mechanical P2 redundancy SKIP applies. It fills a gap the
existing Security & Safety scanners don't cover directly: those audit *code*,
*skills*, and *MCP configs* for vulnerabilities, while this checks the *package name*
an agent is about to install against a slopsquatting/typosquat pattern before the
install happens. Worth a real hands-on eval rather than a mechanical disposition.

_Triaged 2026-11-27 by the daily discovery routine (new lead, same-day triage)._
