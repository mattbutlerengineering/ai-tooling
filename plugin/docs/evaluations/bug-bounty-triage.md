# Evaluation: bug-bounty-triage

**Repo:** [Sequester-AG/bug-bounty-triage](https://github.com/Sequester-AG/bug-bounty-triage)
**Stars:** 71 | **Last updated:** 2026-10-10 (pushed) | **License:** MIT
**Last verified:** 2026-10-10
**Last triaged:** 2026-10-10  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill (MIT) for bug-bounty report triage — reproduces findings where testing
is authorized, separates observed evidence from inference, rejects weak or
non-actionable reports before submission, pursues the highest defensible impact
without overstating severity, and writes a concise submission-ready report while
keeping internal triage notes out of the submission file.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to assess
whether a cited overlap is a genuine redundancy, not the tool's behaviour — a
question this eval does not attempt to answer.

## Verdict

**discovery-log — tentative read**

## Triage note

`triage.py` bands this lead **P2 challenger**, citing `SkillSpector` as the
overlapping STACK pick (shared "security tooling" peer tag in the CATALOG
`Overlaps with` column). The two tools do different jobs: SkillSpector statically
scans *installed* skill packages for prompt injection / exfiltration risk;
bug-bounty-triage is a workflow skill for triaging *externally submitted*
vulnerability reports (reproduction, evidence/inference separation, impact
escalation, report writing). Neither covers the other's job, so `SKIP — redundant
with SkillSpector` would be a false claim of redundancy, not a defensible one.
Left at `discovery-log` rather than SKIPped; stamped as examined.

_Triaged 2026-10-10 by the P2 challenger band._
