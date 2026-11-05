# Evaluation: exterminator

**Repo:** [spider12223/exterminator](https://github.com/spider12223/exterminator)
**Stars:** 12 | **Last updated:** 2026-11-04 (pushed) | **License:** MIT
**Last verified:** 2026-11-05
**Last triaged:** 2026-11-05  <!-- triaged: bulk -->
**Dev loop stage:** Verify (debug)
**Layer:** Process

---

## What it does

A Claude Code + Codex skill that fixes a reported bug at its root cause, then searches
the rest of the codebase for every sibling of the same bug pattern, with an included
eval lab for checking the skill's own fixes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The claimed sibling-bug hunt and the bundled eval
lab are untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Overlaps
`systematic-debugging` (superpowers) and `diagnosing-bugs` (mattpocock/skills), both
root-cause-first debugging disciplines, but neither is a STACK pick, so no redundancy
SKIP applies. Not examined further in this pass.

_Triaged 2026-11-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [exterminator](https://github.com/spider12223/exterminator) | skill | Claude Code + Codex skill (MIT) fixing a bug at its root cause, then hunting down every sibling of the same bug, with an included eval lab | Agents patch the reported symptom and leave the same bug pattern live elsewhere in the codebase | systematic-debugging (superpowers), diagnosing-bugs, vet |
