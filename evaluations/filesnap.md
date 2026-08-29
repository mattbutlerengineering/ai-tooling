# Evaluation: filesnap

**Repo:** [extracurricular-ai/filesnap](https://github.com/extracurricular-ai/filesnap)
**Stars:** 21 | **Last updated:** 2026-08-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-29
**Last triaged:** 2026-08-29  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A git-free file snapshot and rewind CLI (Rust) — puts a directory back the way it was without a repository or touching version control. Content-addressable storage under the hood, published to crates.io as `filesnap-cli`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`opendot`, `Jixu`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. Not SKIPped: `opendot` and `Jixu` both bundle undo/recovery *inside* a harness, but this is a standalone, harness-agnostic CLI for the same job — usable alongside any coding agent, not just those two. Whether that's differentiated enough to earn a seat, or is better served by just using git, needs a real look.

_Triaged 2026-08-29 by the P3 backlog band ([#565](https://github.com/mattbutlerengineering/ai-tooling/issues/565))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [filesnap](https://github.com/extracurricular-ai/filesnap) | tool | Git-free file snapshot and rewind CLI (Apache-2.0, Rust) — puts a directory back the way it was without a repository or touching version control | Coding-agent runs need lightweight, disposable checkpoints outside git, not a full repository for every scratch change | opendot, Jixu |
