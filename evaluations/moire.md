# Evaluation: moire

**Repo:** [jamescazzetta/moire](https://github.com/jamescazzetta/moire)
**Stars:** 31 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Warns parallel AI coding agents when their in-flight work would break each other before either
lands — catching the case where git would merge the two changes cleanly but the result is logically
broken.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby merge/coordination tools, not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log`. `weave` resolves conflicts Git already flagged via structure-aware
merging; `moire`'s stated job is different — catching conflicts Git *won't* flag because the diff
merges cleanly but the two changes are logically incompatible. That is a distinct, narrower claim
worth checking rather than disposing as redundant.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [moire](https://github.com/jamescazzetta/moire) | tool | Warns parallel AI coding agents when their in-flight work will conflict (MIT) — before either lands, even where git would merge cleanly | Parallel agents editing related code silently produce logically-conflicting changes that git's line-based merge can't see | weave, worktrunk, h5i, re_gent |
