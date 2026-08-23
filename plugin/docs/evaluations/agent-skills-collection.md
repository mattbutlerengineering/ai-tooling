# Evaluation: agent-skills-collection

**Repo:** [oliverb-io1902e8/agent-skills-collection](https://github.com/oliverb-io1902e8/agent-skills-collection)
**Stars:** 204 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-23
**Last triaged:** 2026-08-23  <!-- triaged: human -->
**Dev loop stage:** Reference
**Layer:** Process

---

## What it does

A curated collection of modular agent skills for LLM-based agents, spanning multiple editors
(Claude Code, Codex, ChatGPT).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against the STACK incumbents it overlaps, not enough for
any verdict, and none is offered.

## Verdict

**SKIP** — gone. `repos/oliverb-io1902e8/agent-skills-collection` returns 404, and so does
`users/oliverb-io1902e8`: the repo and the account that held it are both absent as of 2026-08-23.
There is nothing left to install, read, or compare against the skill-collection references this row
overlaps, and no successor is evident under another owner.

Unlike the sibling finding in the same sweep (`design-extract`, whose 404 turned out to be
transient), this one **reproduced**: it was reported by the 2026-08-17 link-rot sweep (#522) and
re-checked six days later with the same result, from an authenticated `gh api` call that returns 200
for other repos in the same batch. A whole-account 404 alongside the repo's is also the stronger
signal — a renamed or privatised repo leaves its owner resolvable.

The `discovery-log` reading below is superseded rather than wrong: it declined to SKIP on
*redundancy* grounds, which was the right call on the evidence it had. This SKIP rests on
availability, which is a different question and needs no per-content judgement.

_Re-triaged 2026-08-23 in an attended session, after the link-rot sweep finding (#522) reproduced._

## Triage note (superseded)

Left at `discovery-log`, not SKIPped, despite real overlap with several catalogued skill-collection
references (`awesome-agent-skills`, `buildwithclaude`, `awesome-claude-code`). The catalog already
carries a dozen-plus "awesome list" reference rows and none of them is treated as redundant with
the others on sight — a real read would need to check whether this collection's specific skills are
distinct enough to earn a slot, which is a per-content judgement this bulk pass can't make.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skills-collection](https://github.com/oliverb-io1902e8/agent-skills-collection) | reference | Curated collection of modular agent skills (MIT) for LLM-based agents across editors (⚠️ gone — repo and author account 404 as of 2026-08-23, no successor evident) | Need a catalog of reusable, modular skills to evaluate rather than authoring each from scratch | awesome-agent-skills, buildwithclaude, awesome-claude-code |
