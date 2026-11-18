# Evaluation: agent-crop

**Repo:** [oriliz/agent-crop](https://github.com/oriliz/agent-crop)
**Stars:** 42 | **Last updated:** 2026-11-18 (pushed) | **License:** MIT
**Last verified:** 2026-11-18
**Last triaged:** 2026-11-18  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Local timing and "red-line" nudges for coding agents, feeding an evidence-backed, auditable
self-improvement loop that writes findings back into the agent's own instructions, skills, or
tools (targets DeepSeek Harness / Claude Code / Codex).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner plus repo metadata. Sufficient for a redundancy-based SKIP, not for an ADOPT, which
this eval does not offer.

## Verdict

**SKIP** — redundant with `claude-reflect` (STACK, KEEP, MEASURED): both capture what went wrong
in a session and turn it into a durable instruction update rather than a repeated correction.
Same job as the already-SKIPped `nomore`/`learn-from-lessons` cluster — local timing data is a
different input signal, but the loop it feeds (evidence → rewritten agent instructions) is the
one `claude-reflect` already owns.

_Triaged 2026-11-18 by the P2 challenger band._
