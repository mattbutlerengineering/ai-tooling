# Stack Exclusion Ledger

Machine-readable record of **why each ADOPT/KEEP-verdict tool is or is not in [STACK.md](STACK.md)**.
Verdict data lives in [COMPARISON.md](COMPARISON.md) (what we concluded); STACK.md is the curated
install list (what we actually recommend). This ledger is the bridge: every ADOPT/KEEP tool maps to
either *in STACK*, *conditional*, or *excluded with a recorded reason* — so the reasoning is auditable
as data instead of buried in prose. It is the data foundation the stack-derivation drift gate (issue
\#70) consumes.

Covers all ADOPT- and KEEP-verdict tools in COMPARISON.md (DEFER/CONDITIONAL/SKIP rows are out of
scope). `In STACK?` values: `yes` (in a stage table) · `conditional` (in STACK's "Conditional"
section) · `no` (excluded — a reason is required). Exclusion reasons are grounded in each tool's
`## Verdict` in `evaluations/`.

`Install evidence` answers the *other* question — **is it actually here, checked how, and when**
([ADR-0006](docs/adr/0006-install-evidence-in-the-ledger.md), \#382). It used to live inside the
`KEEP` verdict, unchecked and undated, until detector Y looked and found all four `plugin`-Type
KEEPs unbacked (\#366). A verdict now answers *do we recommend it* and this column answers *is it
here*; neither asserts the other. Values, joined on the row's `owner/repo` and **never** on its
name — name-matching is the bug this came from (\#332, \#343, \#366):

`lockfile <date>` (the row's own slug is in `~/.agents/.skill-lock.json` — installed, settled) ·
`plugins-json <date>` · `skills-dir <date>` · `cache <version> <date>` (the plugin cache holds a
**fetched** version; a fetch is not an activation and nothing records which happened) ·
`collision <date>` (this row's slug is absent **and** a *different* repo owns its name here) ·
`none <date>` (checked, nothing answered) · `n/a` (this Type leaves no install record — the
question is **unanswerable, not answered**, which is why a bare installed-yes/no column would
have been worse than nothing).

Written by `./verify-installs.py --record`, which is **local only** because these are one
machine's records. `--check` validates *shape* — every ADOPT/KEEP row declares a well-formed
value — and runs offline in `make check`. CI gates that the fact is declared, never that it is
true; a build must not fail because a laptop changed. Do not hand-edit the column.

## ADOPT / KEEP tools

| Tool | Verdict | Stage | In STACK? | Exclusion reason (required when `no`) | Install evidence |
|------|---------|-------|-----------|----------------------------------------|--------------------|
| codegraph | ADOPT | Plan | yes | | n/a |
| context7 | KEEP | Plan | yes | | n/a |
| feature-dev | KEEP | Plan | yes | | none 2026-08-05 |
| GSD (Get Shit Done) | KEEP | Plan | yes | | n/a |
| markitdown | ADOPT | Plan | yes | | n/a |
| serena | ADOPT | Plan | conditional | | n/a |
| beads | KEEP | Implement | yes | | n/a |
| caveman | ADOPT | Implement | yes | | lockfile 2026-08-05 |
| superpowers | ADOPT | Implement | yes | (install source for GSD — STACK installs `obra/superpowers`) | cache 5.1.0 2026-08-05 |
| resolving-merge-conflicts | ADOPT | Implement | yes | (listed under STACK's Ship table) | lockfile 2026-08-05 |
| playwright | ADOPT | Verify | yes | | n/a |
| code-review | KEEP | Review | yes | | collision 2026-08-05 |
| pr-review-toolkit | KEEP | Review | yes | | none 2026-08-05 |
| security-guidance | ADOPT | Review | yes | | cache 2.0.6 2026-08-05 |
| claude-code-action | ADOPT | Ship | yes | | n/a |
| claude-reflect | KEEP | Reflect | yes | | cache 3.1.0 2026-08-05 |
| documentation-and-adrs | ADOPT | Reflect | yes | | lockfile 2026-08-05 |
| documentation-writer | ADOPT | Reflect | no | Overlaps documentation-and-adrs (installed, the chosen Diátaxis/ADR pick); redundant standalone writer | lockfile 2026-08-05 |
| ccusage | ADOPT | Outer Loop | yes | | n/a |
| codeburn | ADOPT | Outer Loop | no | Retrospective cross-tool cost analysis; abtop (live TUI) is the default outer-loop pick — pull in for multi-tool bills | n/a |
| agent-skills | ADOPT | Skills & Plugins | yes | | lockfile 2026-08-05 |
| mattpocock/skills | ADOPT | Skills & Plugins | yes | | lockfile 2026-08-05 |
| skill-creator | ADOPT | Skills & Plugins | conditional | | collision 2026-08-05 |
| web-quality-skills | ADOPT | Verify | conditional | | lockfile 2026-08-05 |
| cc-skills-golang | ADOPT | Skills & Plugins | no | Language-specific (Go only); verdict explicitly scoped, irrelevant outside Go projects | none 2026-08-05 |
| claude-mem | ADOPT | Memory & Context | yes | | cache 13.4.0 2026-08-05 |
| OMEGA | KEEP | Memory & Context | no | Retained incumbent, not independently verified; claude-mem is the open, benchmarkable memory pick that holds the slot | n/a |
| fastmcp | ADOPT | MCP Servers | conditional | | n/a |
| github-mcp-server | ADOPT | MCP Servers | yes | | n/a |
| last30days-skill | ADOPT | Research & Discovery | yes | | lockfile 2026-08-05 |
| agentskills | ADOPT | Reference | no | Canonical `SKILL.md` specification — a reference, not an installable tool | n/a |
| claude-plugins-official | KEEP | Reference | no | First-party marketplace/install channel (umbrella entry); member plugins are installed individually | n/a |
| dictionary-of-ai-coding | ADOPT | Reference | no | AI-coding terminology glossary — a reference to keep open, not an installable tool | n/a |
| mcp-for-beginners | ADOPT | Reference | no | MCP-learning curriculum — teaches the protocol, nothing to install | n/a |

## Batch exclusions

Group decisions that excluded a whole discovery batch from STACK, recorded as data rather than only
prose. (These batches are mostly CONDITIONAL/SKIP, so individual rows live in `evaluations/`, not the
ADOPT/KEEP table above.)

| Batch | Date | Tools | STACK decision | Rationale | Flagged for hands-on before any promotion |
|-------|------|-------|----------------|-----------|--------------------------------------------|
| 2026-06-19 discovery (#37) | 2026-06-19 | 19 | all excluded | All evaluated source-grounded, not run hands-on; none moved a quality signal in real testing. Rest are niche, overlapping, or methodology-not-tool. | code-on-incus (per-agent isolation + active defense; Security/Safety), brooks-lint (design-decay reviewer; Review) |
