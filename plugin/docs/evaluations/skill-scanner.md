# Evaluation: skill-scanner

**Repo:** [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner)
**Stars:** 2,399 | **Last updated:** 2026-08-04 (pushed) | **License:** NOASSERTION (Apache-2.0 per LICENSE text)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Review (supply-chain safety)
**Layer:** Tooling

---

## What it does

A static scanner from Cisco AI Defense that inspects agent skill packages — flagging prompt
injection, exfiltration paths, and supply-chain risks in `SKILL.md` files before you install them.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`SkillSpector`, `hol-guard`, `agentlint`). Enough
to place it against the STACK incumbent; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped, even though the overlap with
[`SkillSpector`](https://github.com/NVIDIA/SkillSpector) (STACK, `MEASURED`) is as direct as this
band ever gets: same artifact (`SKILL.md`), same threat model (injection and exfiltration), same
moment (before install).

That is exactly why it should not be disposed. A challenger that does the *identical* job is either
redundant or a replacement, and which one it is turns on detection quality — a question a bulk pass
cannot answer and a SKIP would foreclose. The supporting facts favour taking the question
seriously: this is Cisco AI Defense's rule coverage at ★2.4K and pushed today, against an NVIDIA
project holding a STACK slot. Two major-vendor scanners disagreeing on the same skill is precisely
the finding worth having.

Contrast `hol-guard`, which this same pass SKIPped: its overlap with SkillSpector is partial and
its delta (managed `PreToolUse` interception) collides with hooks already installed. skill-scanner
has no such conflict — it is a scanner, run at the same point in the lifecycle.

Escalated as a P0 head-to-head: run both over the same corpus of third-party skills and compare
findings, false positives, and misses. Note also the licence discrepancy to settle in that pass —
GitHub reports `NOASSERTION` while the CATALOG row records Apache-2.0 from the LICENSE text, and
per this repo's rule `NOASSERTION` means unparsed, not absent.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) | tool | Cisco AI Defense static scanner for agent skill packages (Apache-2.0 per LICENSE text, ★2.3K) — flags prompt injection, exfiltration, and supply-chain risks in SKILL.md files | Downloaded skills can carry prompt injection; want independent major-vendor rule coverage beside SkillSpector | SkillSpector, hol-guard, agentlint |
