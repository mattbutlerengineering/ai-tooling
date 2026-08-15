# Evaluation: skill-safety-checker

**Repo:** [maludb-ed/skill-safety-checker](https://github.com/maludb-ed/skill-safety-checker)
**Stars:** 3 | **Last updated:** 2026-08-14 (pushed) | **License:** none specified
**Last verified:** 2026-08-15
**Last triaged:** 2026-08-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin that security-audits already-installed skills and marketplace
plugins for data capture, secret exfiltration, prompt injection, and malicious code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (no LICENSE file present) plus its declared Type. That is sufficient
for the mechanical SKIP below, which turns on license and vendoring, not on the
tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no declared license, and a `plugin` is vendored (its skill/hook text is
copied into the consuming repo), so a missing license blocks adoption outright. Zero
judgement on the tool's quality; re-triage if the repo adds an OSS license.

_Triaged 2026-08-15 by the P4 mechanical-skip band._
