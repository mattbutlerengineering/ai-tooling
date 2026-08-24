# Evaluation: EvoTrace

**Repo:** [jinzijian/EvoTrace](https://github.com/jinzijian/EvoTrace)
**Stars:** 136 | **Last updated:** 2026-08-21 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-24
**Last triaged:** 2026-08-24  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting (agent trajectory logs → training/eval data)
**Layer:** Infrastructure

---

## What it does

Compiles real-world Claude Code and Codex trajectories (agent session logs) into
verified, tradable post-training assets — turning session recordings that would
otherwise be discarded into data usable for evaluation or RL/fine-tuning pipelines.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`. It cites no STACK pick in "Overlaps with" (`assay`, `scenario`,
and `harbor` are all `discovery-log`/unadopted leads and only loosely analogous — none
compiles agent trajectories into training data specifically), so it doesn't clear the P2
challenger bar. Not archived, permissively licensed, no `Ships inside` declared. Turning
agent session logs into verified training assets is a novel angle not otherwise
represented in Research & Discovery, worth a real look.

_Triaged 2026-08-24 by the P3 backlog band (daily discovery)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [EvoTrace](https://github.com/jinzijian/EvoTrace) | tool | Compiles real-world Claude Code and Codex trajectories into verified, tradable post-training assets (Apache-2.0) | Agent session logs are thrown away after the task; want them turned into verified training/eval data instead of discarded transcripts | assay, scenario, harbor |
