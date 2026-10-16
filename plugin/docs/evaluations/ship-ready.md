# Evaluation: ship-ready

**Repo:** [notaaaronfr/ship-ready](https://github.com/notaaaronfr/ship-ready)
**Stars:** 14 | **Last updated:** not verified (pushed date not fetched this pass) | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

An agent skill (tagline: "Make AI-written code production-ready, with proof") that hardens
AI-written code with evidence — locks behavior, finds bugs/security holes, and adds property
and mutation tests.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only: the public GitHub repo page
(description, star count, license) plus the CATALOG one-liner and "Overlaps with" cell.

## Triage note

Left at `discovery-log`. Its "Overlaps with" cell (`deep-code-review (Perun)`, `code-review-skills`,
`skylos`) names catalog peers, not STACK picks, so it carries no structural redundancy signal. The
Code Review & Quality category is already dense with evidence-grounded review skills (`vet`,
`deep-code-review`, `code-review-skills`, `frank`, `prove-it`, `godkiller-mcp`), but at 14 stars and
with no hands-on read of what, if anything, differentiates its property/mutation-testing angle from
that cluster, a mechanical "redundant with X" SKIP would be a guess dressed as a verdict. Left for a
real look rather than disposed on priors.

_Triaged 2026-10-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ship-ready](https://github.com/notaaaronfr/ship-ready) | skill | Agent skill (MIT) hardening AI-written code with evidence — locks behavior, finds bugs/security holes, adds property + mutation tests | AI-written code gets marked "done" without proof it's correct, secure, or has adequate test coverage | deep-code-review (Perun), code-review-skills, skylos |
