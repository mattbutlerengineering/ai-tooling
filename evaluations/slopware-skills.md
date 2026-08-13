# Evaluation: slopware-skills

**Repo:** [transcendr/slopware-skills](https://github.com/transcendr/slopware-skills)
**Stars:** 30 | **Last updated:** 2026-08-12 (pushed) | **License:** NOASSERTION (GitHub); README declares CC BY 4.0
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A portable pack of Agent Skills and plugins for Codex and Claude Code, built around what the
author calls the "MSW Kernel" (Minimum Sufficient Work) — a discipline aimed at stopping agents
from doing more than a task actually needs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus a fetch of the repo's license declaration. That is sufficient for a SKIP that turns on the
*license*, not on the tool's behaviour — a question the metadata answers directly. It would not
support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no OSS-recognized LICENSE file (GitHub reports `NOASSERTION`/"Other"); the README's
License section declares Creative Commons Attribution 4.0 (CC BY 4.0) instead. CC BY 4.0 is a
content license, not a permissive OSS code license GitHub recognizes for this repo, and it is
not "MIT-like" — vendoring this skill pack's prompt text into a consuming repo would carry an
attribution obligation this catalog's permissive-only bar for vendored artifacts (skill/plugin
Type) does not accept. Not a judgement on quality; the license is the reason.

_Triaged 2026-08-13 by the P3 backlog band (license bar applied per this pass's governance,
ahead of the mechanical P4 regex, which excludes NOASSERTION on purpose since it normally means
"GitHub could not parse the file" rather than "none exists" — here the repo's own README settles
the question the raw SPDX field leaves open)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [slopware-skills](https://github.com/transcendr/slopware-skills) | skill | Portable Agent Skills/plugins pack (⚠️ no LICENSE file) built around a Minimum Sufficient Work discipline for Codex and Claude Code | Agents overbuild past what a task actually needs; want a skill enforcing minimum-sufficient scope | HERO-Anti-OverDefense, pristine-skill, ratchet |
