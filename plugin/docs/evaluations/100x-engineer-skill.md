# Evaluation: 100x-engineer-skill

**Repo:** [DeadInternetStudios/100x-engineer-skill](https://github.com/DeadInternetStudios/100x-engineer-skill)
**Stars:** 31 | **Last updated:** 2026-11-25 (pushed) | **License:** MIT
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A skill (MIT), authored by a former Cursor engineer, that enforces senior-engineer
discipline to turn prompts into formally verified, production-ready code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none, and "formally verified" is the author's own claim, unverified
here.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. No STACK pick
is cited in "Overlaps with" (pressure 0) — it names `vet`, `skylos`, and
`brooks-lint` as conceptual peers in the Code Review & Quality cluster, none of
which it clearly duplicates (those are static-analysis gates; this is a discipline
skill). Left at `discovery-log` for a real hands-on eval, including checking what
"formally verified" actually means in practice here.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [100x-engineer-skill](https://github.com/DeadInternetStudios/100x-engineer-skill) | skill | Skill (MIT) by a former Cursor engineer enforcing senior-engineer discipline to turn prompts into formally verified production code | AI-written code gets marked done with no formal verification or senior-engineer-level discipline behind it | vet, skylos, brooks-lint |
