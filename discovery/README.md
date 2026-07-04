# Discovery logs (historical)

This directory holds the historical bulk-triage logs — `new-tools-loopN.md` files
from the 2026-06 scanning era (loops 1–21). Each file is a one-liner-verdict pass
over a batch of candidate tools: quick triage that feeds `CATALOG.md`, not a full
hands-on evaluation (those live in `evaluations/`). The logs are kept as the audit
trail of what was scanned and when; they are no longer the active intake path — see
[Where scans live now](#where-scans-live-now).

> There are 20 files covering 21 loops: loop 12 was folded into
> `new-tools-loop11.md` ("Loop 11-12"), so there is no `new-tools-loop12.md`.

## Index

| File | Date | Scope |
|------|------|-------|
| [new-tools-loop1.md](new-tools-loop1.md) | 2026-06-17 | New Tools Evaluation (Loop 1) |
| [new-tools-loop2.md](new-tools-loop2.md) | 2026-06-17 | New Tools Evaluation (Loop 2) |
| [new-tools-loop3.md](new-tools-loop3.md) | 2026-06-17 | New Tools Evaluation (Loop 3) |
| [new-tools-loop4.md](new-tools-loop4.md) | 2026-06-17 | New Tools Evaluation (Loop 4) |
| [new-tools-loop5.md](new-tools-loop5.md) | 2026-06-17 | New Tools Evaluation (Loop 5) |
| [new-tools-loop6.md](new-tools-loop6.md) | 2026-06-17 | New Tools Evaluation (Loop 6) |
| [new-tools-loop7.md](new-tools-loop7.md) | 2026-06-17 | New Tools Evaluation (Loop 7) |
| [new-tools-loop8.md](new-tools-loop8.md) | 2026-06-17 | New Tools Evaluation (Loop 8) |
| [new-tools-loop9.md](new-tools-loop9.md) | 2026-06-17 | New Tools Evaluation (Loop 9) |
| [new-tools-loop10.md](new-tools-loop10.md) | 2026-06-17 | New Tools Evaluation (Loop 10) |
| [new-tools-loop11.md](new-tools-loop11.md) | 2026-06-17 | New Tools Evaluation (Loop 11-12) |
| [new-tools-loop13.md](new-tools-loop13.md) | 2026-06-17 | Loop 13 — Tool Evaluations |
| [new-tools-loop14.md](new-tools-loop14.md) | 2026-06-17 | Loop 14 — Tool Evaluations |
| [new-tools-loop15.md](new-tools-loop15.md) | 2026-06-17 | Loop 15 — Catalog Quality Audit & Workflow Gap Analysis |
| [new-tools-loop16.md](new-tools-loop16.md) | 2026-06-17 | Loop 16 — Outer Loop Infrastructure & Fresh Discovery |
| [new-tools-loop17.md](new-tools-loop17.md) | 2026-06-17 | Loop 17 — Installed Tools Audit & Optimal Setup Analysis |
| [new-tools-loop18.md](new-tools-loop18.md) | 2026-06-17 | Loop 18 — Final Discovery Pass & Session Summary |
| [new-tools-loop19.md](new-tools-loop19.md) | 2026-06-19 | Discovery loop 19 |
| [new-tools-loop20.md](new-tools-loop20.md) | 2026-06-19 | Discovery loop 20 |
| [new-tools-loop21.md](new-tools-loop21.md) | 2026-06-19 | Discovery loop 21 — coding-agent/ai-coding vector |

## Where scans live now

New tool scans are **GitHub issues labeled [`scan`](../docs/agents/triage-labels.md)**,
not new `new-tools-loopN.md` files in this directory. Each scan issue lists its
findings (with star counts) in a table and is closed by the pull request that
catalogs those findings. Exemplars:

- [#189](https://github.com/mattbutlerengineering/ai-tooling/issues/189) — Star sync: 29 new tools found (2026-07-01), closed by PR #191
- [#213](https://github.com/mattbutlerengineering/ai-tooling/issues/213) — Skills ecosystem scan: 4 new skills found (2026-07-03), closed by PR #214

To find scan intake: `gh issue list --label scan --state all`.
