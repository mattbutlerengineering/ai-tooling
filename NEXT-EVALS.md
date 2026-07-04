# Next evals — a ranked promotion queue

The `discovery-log` leads most worth evaluating next, **derived** (not hand-maintained) from data already in the repo. Regenerate with `python3 next-evals.py`; do not edit between the markers.

Score = `2*overlap_pressure + stage_gap_weight + evidence_bonus`, where `overlap_pressure` is how many other catalog rows cite the tool in "Overlaps with", `stage_gap_weight` is `10*(1 - Validated/Tools)` for the tool's [COMPARISON.md](COMPARISON.md) stage (hungriest stage highest), and `evidence_bonus` is +2 when some homework exists (Evidence `REVIEW`). The weights are a starting heuristic — see `next-evals.py`. The queue *selects*; a human or attended agent runs `/evaluate-tool` (unattended runs produce thin verdicts the fabrication gates exist to catch).

_Showing the top 25 of 473 discovery-log candidates — 448 not shown (no silent cap: rerun and read the source for the tail)._

<!-- NEXT-EVALS:START -->

| Rank | Tool | Stage | Score | Why (pressure/gap) | Eval command |
|------|------|-------|-------|--------------------|--------------|
| 1 | opencode | Implement | 58.5 | pressure 24, gap 8.5 | `/evaluate-tool opencode` |
| 2 | cognee | Memory & Context | 40.5 | pressure 15, gap 8.5 | `/evaluate-tool cognee` |
| 3 | OpenHands | Implement | 38.5 | pressure 14, gap 8.5 | `/evaluate-tool OpenHands` |
| 4 | goose | Implement | 38.5 | pressure 14, gap 8.5 | `/evaluate-tool goose` |
| 5 | langfuse | Outer Loop | 38.2 | pressure 15, gap 8.2 | `/evaluate-tool langfuse` |
| 6 | agent-browser | Verify | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool agent-browser` |
| 7 | supermemory | Memory & Context | 36.5 | pressure 13, gap 8.5 | `/evaluate-tool supermemory` |
| 8 | ECC | Implement | 36.5 | pressure 13, gap 8.5 | `/evaluate-tool ECC` |
| 9 | promptfoo | Outer Loop | 36.2 | pressure 13, gap 8.2 | `/evaluate-tool promptfoo` |
| 10 | pydantic-ai | Implement | 34.5 | pressure 12, gap 8.5 | `/evaluate-tool pydantic-ai` |
| 11 | tech-leads-club/agent-skills | Skills & Plugins | 32.6 | pressure 11, gap 8.6 | `/evaluate-tool tech-leads-club/agent-skills` |
| 12 | vercel-labs/agent-skills | Skills & Plugins | 32.6 | pressure 11, gap 8.6 | `/evaluate-tool vercel-labs/agent-skills` |
| 13 | awesome-claude-code | Reference | 32.3 | pressure 11, gap 8.3 | `/evaluate-tool awesome-claude-code` |
| 14 | code-context-engine | Plan | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool code-context-engine` |
| 15 | spec-kit | Plan | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool spec-kit` |
| 16 | MemOS | Memory & Context | 30.5 | pressure 10, gap 8.5 | `/evaluate-tool MemOS` |
| 17 | awesome-agent-skills | Reference | 30.3 | pressure 10, gap 8.3 | `/evaluate-tool awesome-agent-skills` |
| 18 | awesome-agent-skills (libukai) | Reference | 30.3 | pressure 10, gap 8.3 | `/evaluate-tool awesome-agent-skills (libukai)` |
| 19 | opik | Outer Loop | 30.2 | pressure 10, gap 8.2 | `/evaluate-tool opik` |
| 20 | mem0 | Memory & Context | 28.5 | pressure 9, gap 8.5 | `/evaluate-tool mem0` |
| 21 | agent-kit | Implement | 28.5 | pressure 9, gap 8.5 | `/evaluate-tool agent-kit` |
| 22 | qwen-code | Implement | 28.5 | pressure 9, gap 8.5 | `/evaluate-tool qwen-code` |
| 23 | ruflo | Implement | 28.5 | pressure 9, gap 8.5 | `/evaluate-tool ruflo` |
| 24 | sandcastle | Implement | 28.5 | pressure 9, gap 8.5 | `/evaluate-tool sandcastle` |
| 25 | browser-use | Verify | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool browser-use` |

<!-- NEXT-EVALS:END -->
