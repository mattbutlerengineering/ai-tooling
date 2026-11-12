# Evaluation: pstack

**Repo:** [nevertoday/xxd-pstack](https://github.com/nevertoday/xxd-pstack)
**Stars:** 60 | **Last updated:** 2026-11-11 (pushed) | **License:** NOASSERTION
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A plain-language guide (in 10 languages) that makes an AI try its own work first before
claiming "fixed" — a protocol for Claude Code, Cursor, and Codex to self-verify a change
rather than assert success on its own say-so.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns
on the repository's own declared license, not on the tool's behavior.

## Verdict

**SKIP** — no declared license (GitHub reports NOASSERTION, no LICENSE file found). A
vendored skill/guide is copied into the consuming repo; text carrying no license grant
cannot be adopted that way. The job itself is not novel — `doneguard` (MIT) already
blocks a false "done" claim mechanically via a stop hook, and `tdd-guard`/`ratchet` cover
adjacent ground under permissive licenses.

_Triaged 2026-11-12 by the P4 mechanical-skip band._
