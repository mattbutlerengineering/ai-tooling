# Evaluation: Quant-Off/skills

**Repo:** [Quant-Off/skills](https://github.com/Quant-Off/skills)
**Stars:** 1 | **Last updated:** 2026-08-08 (pushed) | **License:** MIT
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Review (security audit skills)
**Layer:** Process

---

## What it does

A Claude Code plugin marketplace for security auditing — evidence-based skills for constant-time crypto review, compiler-survival checks in binaries, and zero-trust codebase audits.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge whether the individual skills' audit methodology is sound.

## Verdict

**discovery-log — tentative read** — A different job than SkillSpector/skill-scanner (which scan *agent skills themselves* for malicious patterns): this equips an agent with skills to audit *target code* for crypto-timing and binary-hardening issues, a narrower niche than ghostsecurity/skills' general AppSec/OWASP coverage. Worth a real look at what the skills actually check before disposing of it as redundant.

_Triaged 2026-08-09 by the P2 challenger band._
