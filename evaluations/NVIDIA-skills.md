# Evaluation: NVIDIA/skills

**Repo:** [NVIDIA/skills](https://github.com/NVIDIA/skills)
**Stars:** 2,790 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (domain vertical)
**Layer:** Tooling

---

## What it does

First-party agent skills for NVIDIA products — Physical AI, robotics, simulation (Omniverse), CUDA
and RAG workflows — installable into Claude Code, Codex and other coding agents to run those
workflows end to end.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched 2026-08-04 plus
the CATALOG one-liner and "Overlaps with" cell (`softaworks/agent-toolkit`, `SkillSpector`,
`awesome-agent-skills`). Enough to judge whether it duplicates a catalogued incumbent; not enough
for any positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped — the overlap that banded it is a category error. The STACK
pick it cites is [`SkillSpector`](https://github.com/NVIDIA/SkillSpector), which *scans* third-party
skills for prompt injection. NVIDIA/skills *is* a skill collection. They share a vendor, not a job;
"redundant with SkillSpector" would be nonsense.

What it actually is: a hardware/domain vertical (CUDA, robotics, Omniverse, RAG) that a
general-purpose dev-loop stack collects nothing from unless it does that work. Off-scope is the
honest reading, and this catalog holds domain packs as leads rather than SKIPping them on scope
alone.

**Metadata correction.** The CATALOG row carries "⚠️ license NOASSERTION". A live fetch on
2026-08-04 returns **Apache-2.0**, so the warning is false and the row is corrected in this pass.
The stale record is the failure mode detector R exists to age: `repo-metadata.json` is a committed
snapshot, and every record in it is currently undated.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | skill | AI agent skills published and maintained by NVIDIA (★2.8K, Apache-2.0) | Running NVIDIA-stack workflows (CUDA, robotics, Omniverse, RAG) from a coding agent | softaworks/agent-toolkit, SkillSpector, awesome-agent-skills |
