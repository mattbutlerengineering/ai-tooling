# Evaluation: onlyread

**Repo:** [onlyreadai/onlyread](https://github.com/onlyreadai/onlyread)
**Stars:** 14 | **Last updated:** 2026-11-05 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-11-06
**Last triaged:** 2026-11-06  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Chrome extension that makes AI browser agents read-only, refusing writes (send, post, edit,
delete) before they leave the browser — a mechanical guardrail against an agent taking an
unintended action on a live site.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**SKIP** — AGPL-3.0. This daily discovery routine's license bar disqualifies any copyleft
license outright (only permissive, MIT-like OSS is adoptable); AGPL-3.0 fails that bar
regardless of how the tool would otherwise score. No judgement is made about the tool's
quality — overlapping guardrail tools already in the catalog (`agentlint`, `hol-guard`,
`code-on-incus`) are permissively licensed and preferred for that reason alone.

_Triaged 2026-11-06 by the daily discovery routine's license bar (copyleft ⇒ SKIP)._
