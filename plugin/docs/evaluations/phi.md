# Evaluation: phi

**Repo:** [pulseaiclub/phi](https://github.com/pulseaiclub/phi)
**Stars:** 17 | **Last updated:** 2026-08-08 (pushed) | **License:** MIT
**Last verified:** 2026-08-08
**Last triaged:** 2026-08-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (coding-agent CLI)

---

## What it does

A coding agent CLI (Go) with sub-agents, hashline edits, and a permission gate.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: the terminal-coding-agent space is crowded (aider, command-code,
pi, opendot, …), but "hashline edits" (a specific edit-tracking mechanism) plus an explicit
permission gate is a narrower claim than any named overlap makes — worth a hands-on look
rather than a mechanical redundancy SKIP against a much larger incumbent class.

_Triaged 2026-08-08 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [phi](https://github.com/pulseaiclub/phi) | harness | Coding agent CLI (MIT, Go) with sub-agents, hashline edits, and a permission gate | Want a lightweight coding agent with fine-grained edit tracking and explicit permission gating, not a heavyweight harness | command-code, pi, opendot |
