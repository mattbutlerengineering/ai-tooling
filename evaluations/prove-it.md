# Evaluation: prove-it

**Repo:** [Pablo-aps/prove-it](https://github.com/Pablo-aps/prove-it)
**Stars:** 15 | **Last updated:** 2026-08-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-19
**Last triaged:** 2026-08-19  <!-- triaged: bulk -->
**Dev loop stage:** Code Review & Quality / Verify
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Adversarial verification Agent Skill (Apache-2.0) making coding agents prove bug fixes, CI, logs, and deployments before claiming done." An open Agent Skill (`agentskills.io` standard) for Claude Code, Codex, and Cursor that checks whether a passing test or green check was weakened or faked rather than trusting it at face value, with a 12-case reproducible benchmark.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

P3 backlog — no STACK pick cited in "Overlaps with" (vet and tdd-guard are catalogued but not STACK picks), so no mechanical redundancy call applies. Left at `discovery-log`; stamped only.

_Triaged 2026-08-19 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [prove-it](https://github.com/Pablo-aps/prove-it) | skill | Adversarial verification Agent Skill (Apache-2.0) making coding agents prove bug fixes, CI, logs, and deployments before claiming done | Agents present passing tests or green CI as proof without checking whether the check itself was weakened or faked | vet, tdd-guard, godkiller-mcp |
