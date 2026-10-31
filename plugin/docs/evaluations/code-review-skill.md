# Evaluation: code-review-skill

**Repo:** [kyy-logs/code-review-skill](https://github.com/kyy-logs/code-review-skill)
**Stars:** 55 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An auditable code-review skill (MIT) for Claude Code and Codex — runs four independent probes, produces evidence-backed findings, and derives a JSON merge-gate decision rather than a free-text verdict.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (deep-code-review (Perun), code-review-skills, skylos). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; none of its overlaps (deep-code-review, code-review-skills, skylos) is a STACK ADOPT/KEEP pick, so it doesn't land in P2. The JSON-derived merge-gate angle (vs. free-text findings) is a real differentiator worth a hands-on comparison against the existing evidence-grounded review skills before any disposition stronger than a lead.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-review-skill](https://github.com/kyy-logs/code-review-skill) | skill | Auditable code-review skill (MIT) for Claude Code and Codex — four independent probes, evidence-backed findings, and a JSON-derived merge gate | Agent-run code review can assert findings with no evidence trail or reproducible merge decision | deep-code-review (Perun), code-review-skills, skylos |
