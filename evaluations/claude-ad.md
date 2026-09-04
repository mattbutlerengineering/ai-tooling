# Evaluation: Claude-AD

**Repo:** [ADScanPro/Claude-AD](https://github.com/ADScanPro/Claude-AD)
**Stars:** 139 | **Last updated:** 2026-08-24 (pushed) | **License:** MIT
**Last verified:** 2026-08-31
**Last triaged:** 2026-08-31  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An Active Directory pentest methodology for Claude Code — skills, agents, and slash commands for internal AD red-team work (Kerberoasting, ADCS ESC1-17, DCSync, ACL abuse, NTLM relay, delegation), with per-technique OPSEC/telemetry notes, driving netexec, impacket, certipy, bloodyAD, and BloodHound CE. Scoped to **authorized** engagements.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision that turns on differentiation from existing entries, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. The Security & Safety category already carries broad offensive-security skill bundles (`pentest-ai-agents`, `Claude-BugHunter`, `ctf-skills`) but none is Active Directory-specific — Claude-AD's per-technique coverage (Kerberoasting, ADCS ESC1-17, DCSync, ACL abuse, NTLM relay) and OPSEC/telemetry notes are a narrower, deeper niche than the generalist bundles it cites as overlaps. Not clearly redundant; worth a real look at whether the AD-specific depth earns its own slot.

_Triaged 2026-08-31 by the P3 backlog band._
