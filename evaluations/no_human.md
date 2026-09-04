# Evaluation: no_human

**Repo:** [no-human-ai/no_human](https://github.com/no-human-ai/no_human)
**Stars:** 256 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Autonomous agent that goes from ticket to reviewed pull request: plans before writing any code, runs an adversarial second-model review of its own changes, executes tests, and includes a "tamper guard" so the agent's own summary isn't the only witness to what it did. Integrates with issue trackers (Jira, Linear).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped. No structural reason to eliminate it (no overlap-pressure hit against a STACK pick, MIT-licensed, live, actively described). At ★256 it's the most-starred and most-substantiated of today's discovery batch — plan-then-code, adversarial review, and tamper detection are the same shape of concern that OpenHands/goose/aider/SWE-agent already occupy in P0, so it's a reasonable future eval-runner candidate. Eliminate-only forbids promoting it here; leaving it for a real hands-on read.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [no_human](https://github.com/no-human-ai/no_human) | harness | Autonomous ticket-to-reviewed-PR agent (MIT, ★256) — plans before coding, runs an adversarial second-model review, executes tests, and tamper-guards its own changes; integrates with Jira/Linear | Want an autonomous coding agent that produces a reviewed, trustworthy PR from a ticket, not just an unchecked diff | OpenHands, goose, aider, SWE-agent |
