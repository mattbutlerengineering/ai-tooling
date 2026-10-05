# Evaluation: vetted

**Repo:** [nadirali1350/vetted](https://github.com/nadirali1350/vetted)
**Stars:** 2 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A zero-dependency scanner that vets any agent skill before install, paired with a small
collection of skills that document their own proof (tests/evidence the skill does what
it claims).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. Created 2026-09-29, ★2 — too early for
a hands-on run.

## Triage note

Left at `discovery-log`, not SKIPped — this is a P2 challenger citing `SkillSpector`
(STACK) in overlap pressure. The skill-scanner space is already dense
(`SkillSpector`, `skill-scanner`, `skilldoctor`, `skill-safety-checker`,
`skill-quality-suite`, `ai-skill-scanner`), which would normally argue for a
redundancy SKIP, but `vetted`'s stated angle — skills that carry their own proof of
working, not just a security scan — reads as a different question (does it work?)
from `SkillSpector`'s (is it malicious?). That distinction is a README claim, not
something this source-only pass can confirm or refute, so it is left rather than
mechanically SKIPped on the shared "skill scanner" label alone.

_Triaged 2026-10-05 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vetted](https://github.com/nadirali1350/vetted) | tool | Zero-dependency scanner (MIT) vetting any agent skill before install, paired with a skill collection that documents its own proof | Skills get installed on README claims alone, with no scan step verifying they do what they claim before trusting them | SkillSpector, skill-scanner, skilldoctor |
