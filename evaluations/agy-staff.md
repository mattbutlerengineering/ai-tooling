# Evaluation: agy-staff

**Repo:** [keli-wen/agy-staff](https://github.com/keli-wen/agy-staff)
**Stars:** 16 | **Last updated:** 2026-08-19 (pushed) | **License:** MIT
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Bridges Google's Antigravity CLI (`agy`) into Claude Code and OpenAI Codex sessions as a fast Gemini "staffer" — a cross-provider delegate reachable from within an existing session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `codex-plugin-cc` is the closest incumbent (a cross-provider bridge into Claude Code), but it targets OpenAI Codex specifically while agy-staff targets Google's Antigravity/Gemini CLI — a different provider, not a duplicate of the same bridge. Very low stars (16) and brand new (created 2026-08-18); worth a real look once the Antigravity CLI ecosystem has more track record.

_Triaged 2026-08-22 by the P3 backlog band._
