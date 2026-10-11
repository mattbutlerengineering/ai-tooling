# Evaluation: asd-ste100-skill

**Repo:** [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)
**Stars:** 4,400 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-11
**Last triaged:** 2026-10-11  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A Claude Code skill that applies the ASD-STE100 Simplified Technical English rules to
rewrite ambiguous English meant for AI agents — tool descriptions, error messages, and
inter-agent instructions — rather than human-facing prose.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata and a README skim. No catalogued STACK pick resolves from this row's
"Overlaps with" cell, so this is not a P2 redundancy call — see Triage note.

## Catalog entry

| [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | skill | Claude Code skill (MIT) applying ASD-STE100 Simplified Technical English to rewrite ambiguous agent-facing text | Tool descriptions, error messages, and inter-agent instructions read ambiguous to agents with no STE-style discipline applied | writing-skills, iso-24495-skill, documentation-writer |  |

## Triage note

Left at `discovery-log`: same author and instinct as the already-catalogued
`iso-24495-skill`, but a distinct, more specific target (agent-facing text — tool
descriptions, error messages, inter-agent instructions — rather than human-facing
docs). `writing-skills` already covers STE-100 for general prose, but not this
agent-facing angle specifically. Real traction (4.4K stars). Deserves a look rather
than a mechanical SKIP; left for the P0/eval-runner lane.

_Triaged 2026-10-11 by the P3 backlog band._
