# Evaluation: Brain4Agent

**Repo:** [SparkofSpike/Brain4Agent](https://github.com/SparkofSpike/Brain4Agent)
**Stars:** 147 | **Last updated:** 2026-11-12 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A CJK-first memory module for mainstream AI agents, per the repo's own description — a
memory layer whose design target is Chinese/Japanese/Korean content rather than the
English-tuned defaults of most agent-memory tools.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`. `mem0`, `cognee`, and `claude-mem` all cover general agent
memory, but none is CJK-first, and none of those three is itself a STACK ADOPT/KEEP
incumbent for this specific niche (claude-mem is ADOPT but is English/general-purpose, not
CJK-tuned) — so there is no clean P2 redundancy call. The CJK-first framing is a real
differentiator worth a hands-on eval against non-English content rather than a mechanical
SKIP.
