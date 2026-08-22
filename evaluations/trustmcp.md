# Evaluation: trustmcp

**Repo:** [v0idw4lker/trustmcp](https://github.com/v0idw4lker/trustmcp)
**Stars:** 1 | **Last updated:** 2026-08-22 (pushed) | **License:** MIT
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Review (Security & Safety)
**Layer:** Tooling

---

## What it does

A free, open-source security scanner for MCP servers — static analysis, live dynamic probing, auth posture detection, and SARIF/JSON reporting with an A-F score mapped to the OWASP MCP Top 10.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the leave decision below, which turns on what artifact class the tool scans, not on its behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped, even though the triage bands filed it as a P2 challenger citing `SkillSpector`. SkillSpector scans AI agent **skills** (SKILL.md packages) for prompt injection and malicious patterns; trustmcp scans **MCP servers** — a different artifact class — via static analysis, live dynamic probing, and auth-posture checks, explicitly mapped to the OWASP MCP Top 10 taxonomy. The two tools scan different things with different methods; "redundant with SkillSpector" would be a false claim. Also brand new (1 star, created 2026-08-18) — worth a real look once it has more track record, not a mechanical SKIP on a spurious overlap.

_Triaged 2026-08-22 by the P2 challenger band._
