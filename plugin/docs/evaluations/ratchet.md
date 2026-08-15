# Evaluation: ratchet

**Repo:** [0xwilliamortiz/ratchet](https://github.com/0xwilliamortiz/ratchet)
**Stars:** 409 | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** Code Review & Quality
**Layer:** Tooling

---

## What it does

A git-hook compliance monitor for coding agents: intercepts agent edits via a `PostToolUse` hook and grades findings (certain/likely/heuristic) against complexity, duplication, and new-dependency rules, maintaining a session ledger of complexity trends. Blocks edits in strict mode or advises in guard mode (default).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: README, install instructions, and test-suite description gathered via web fetch (115 passing tests reported by the project, not independently re-run here).

## Verdict

**SKIP** — the repo and its author account (`0xwilliamortiz`) are both gone (404 via the GitHub
API) as of 2026-08-15, caught by the link-rot sweep after detector C moved onto authenticated
`gh api` (#498). Nothing left to install or evaluate, and no successor is evident.

_Triaged 2026-08-15 after the account/repo was found gone during a repo audit._

## Triage note (superseded)

Previously left at `discovery-log` (triaged 2026-08-02): `tdd-guard` enforces test-first
discipline and `cc-safety-net` blocks destructive commands, but neither graded mid-session
complexity/duplication/dependency drift the way this tool claimed to — the differentiation looked
worth a real hands-on eval. Moot now that the repo is gone.
