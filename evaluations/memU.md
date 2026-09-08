# Evaluation: memU

**Repo:** [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)
**Stars:** 14.4K | **Last updated:** 2026-09-08 (pushed) | **License:** NOASSERTION (no detected LICENSE file)
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

"File system as memory" for agents — organizes memory as a navigable tree of human-readable Markdown (`MEMORY.md` profile/events, `SKILL.md` learned patterns, `INDEX.md` map). The agent `memorize()`s sources and `retrieve()`s only the relevant sections, instead of flattening everything into one prompt or an opaque vector blob.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-mem` despite the overlap citation. memU's file-structured, human-readable Markdown-tree approach is architecturally distinct from claude-mem's semantic-search/knowledge-graph plugin design, and at 14.4K★ it is one of the largest, most established projects in the entire Memory & Context category — that scale and a genuinely different design (inspectable filesystem vs. searchable index) argue for a real hands-on comparison, not a mechanical SKIP. `repo-metadata.json` also records `license_spdx: NOASSERTION` (no LICENSE file GitHub's detector recognizes); worth confirming during a real eval before any positive verdict, per the license bar.

_Triaged 2026-09-08 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memU](https://github.com/NevaMind-AI/memU) | platform | "File system as memory" for agents (★13.9K) — organizes memory as a navigable tree of human-readable Markdown (MEMORY.md profile/events, SKILL.md learned patterns, INDEX.md map); the agent `memorize()`s sources and `retrieve()`s only the relevant sections | Flattening agent memory into one giant prompt or an opaque vector blob is unnavigable; want inspectable, file-structured memory | cognee, MemOS, supermemory, memind, claude-mem |
