# Evaluation: money-review

**Repo:** [IanFoxDev/money-review](https://github.com/IanFoxDev/money-review)
**Stars:** 0 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code review focused on code that moves money — transactions, races,
idempotency, and money arithmetic.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. Day-one repo, 0 stars.

## Triage note

Left at `discovery-log`, not SKIPped — cited pressure against `code-review` and
`pr-review-toolkit` (STACK) is a P2 challenge, but those are generic review tools;
`money-review` targets a narrow, high-consequence domain (billing/payments
correctness) the way `brooks-lint` targets design decay — domain specialization, not
redundancy. Too new (0 stars, day-one) to confirm it delivers on that angle.

_Triaged 2026-10-05 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [money-review](https://github.com/IanFoxDev/money-review) | tool | Claude Code review (MIT) for code that moves money — transactions, races, idempotency, money arithmetic | Generic code review misses domain-specific money bugs (races, idempotency, arithmetic) in billing/payments code | brooks-lint, code-review, pr-review-toolkit |
