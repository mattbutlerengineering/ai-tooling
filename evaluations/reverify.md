# Evaluation: reverify

**Repo:** [2akouwu/reverify](https://github.com/2akouwu/reverify)
**Stars:** 939 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-06
**Last triaged:** 2026-09-06  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An MCP server + CLI (★939) that forces agent claims through deterministic tools before acceptance
— every claim is checked against ground truth with evidence, and grounded facts/context survive
context resets. Proven on reverse engineering / malware analysis, marketed more broadly as
anti-hallucination grounding for agent-computer interaction.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge how well
the grounding mechanism holds up hands-on.

## Triage note

Left at `discovery-log`. P3 backlog — no structural disposition (not archived, no disqualifying
license, no STACK-pick citation in "Overlaps with", no `Ships inside` container). At ★939 and
still climbing this week, it's a significant, differentiated lead (claim-grounding via
deterministic tool checks, not just prompting) that deserves a real hands-on eval rather than a
mechanical disposition; stamped and left for the P0/eval-runner lane.

_Triaged 2026-09-06 by the P3 backlog band._
