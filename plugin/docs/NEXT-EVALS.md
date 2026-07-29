# Next evals — a banded promotion queue

The 465 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score only has ~83 distinct values across these leads — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 154 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 286 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 57.9 | pressure 24, gap 7.9 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 39.9 | pressure 15, gap 7.9 | `/evaluate-tool cognee` |
| ECC | Implement | 39.9 | pressure 15, gap 7.9 | `/evaluate-tool ECC` |
| agent-browser | Verify | 39.7 | pressure 15, gap 7.7 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 37.9 | pressure 15, gap 7.9 | `/evaluate-tool langfuse` |
| OpenHands | Implement | 37.9 | pressure 14, gap 7.9 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.9 | pressure 14, gap 7.9 | `/evaluate-tool goose` |
| spec-kit | Plan | 36.4 | pressure 14, gap 6.4 | `/evaluate-tool spec-kit` |
| supermemory | Memory & Context | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool supermemory` |
| promptfoo | Outer Loop | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool promptfoo` |
| pydantic-ai | Implement | 33.9 | pressure 12, gap 7.9 | `/evaluate-tool pydantic-ai` |
| awesome-claude-code | Reference | 32.1 | pressure 11, gap 8.1 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool vercel-labs/agent-skills` |
| awesome-agent-skills | Reference | 30.1 | pressure 10, gap 8.1 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.1 | pressure 10, gap 8.1 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool MemOS` |
| opik | Outer Loop | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool opik` |
| ruflo | Implement | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool ruflo` |
| OpenSpec | Plan | 28.4 | pressure 10, gap 6.4 | `/evaluate-tool OpenSpec` |
| mem0 | Memory & Context | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool mem0` |
| agent-kit | Implement | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool agent-kit` |
| orca | Implement | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool orca` |
| qwen-code | Implement | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool qwen-code` |
| sandcastle | Implement | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool sandcastle` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 154 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 154 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| browser-use | Verify | 27.7 | pressure 9, gap 7.7 | `/triage-lead browser-use` |
| ghostsecurity/skills | Review | 27.1 | pressure 9, gap 7.1 | `/triage-lead ghostsecurity/skills` |
| agentmemory | Memory & Context | 25.9 | pressure 8, gap 7.9 | `/triage-lead agentmemory` |
| gstack | Implement | 25.9 | pressure 8, gap 7.9 | `/triage-lead gstack` |
| chrome-devtools-mcp | Verify | 25.7 | pressure 8, gap 7.7 | `/triage-lead chrome-devtools-mcp` |
| BMAD-METHOD | Plan | 24.4 | pressure 8, gap 6.4 | `/triage-lead BMAD-METHOD` |
| Understand-Anything | Plan | 24.4 | pressure 8, gap 6.4 | `/triage-lead Understand-Anything` |
| ACE (agentic-context-engine) | Memory & Context | 23.9 | pressure 7, gap 7.9 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 23.9 | pressure 7, gap 7.9 | `/triage-lead memU` |
| compound-engineering | Implement | 23.9 | pressure 7, gap 7.9 | `/triage-lead compound-engineering` |
| gastown | Implement | 23.9 | pressure 7, gap 7.9 | `/triage-lead gastown` |
| ralph-claude-code | Implement | 23.9 | pressure 7, gap 7.9 | `/triage-lead ralph-claude-code` |

## P3 backlog — 286 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 286 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| claude-hud | Plan | 26.4 | pressure 9, gap 6.4 | `/triage-lead claude-hud` |
| CopilotKit | Implement | 25.9 | pressure 8, gap 7.9 | `/triage-lead CopilotKit` |
| gemini-cli | Implement | 25.9 | pressure 8, gap 7.9 | `/triage-lead gemini-cli` |
| voltagent | Implement | 25.9 | pressure 8, gap 7.9 | `/triage-lead voltagent` |
| awesome-claude-skills (Composio) | Reference | 24.1 | pressure 7, gap 8.1 | `/triage-lead awesome-claude-skills (Composio)` |
| daytona | Implement | 23.9 | pressure 7, gap 7.9 | `/triage-lead daytona` |
| fast-agent | Implement | 23.9 | pressure 7, gap 7.9 | `/triage-lead fast-agent` |
| slidev | Skills & Plugins | 23.9 | pressure 7, gap 7.9 | `/triage-lead slidev` |
| ui-ux-pro-max | Skills & Plugins | 23.9 | pressure 7, gap 7.9 | `/triage-lead ui-ux-pro-max` |
| awesome-claude-skills (behisecc) | Reference | 22.1 | pressure 7, gap 8.1 | `/triage-lead awesome-claude-skills (behisecc)` |
| ag-ui | Reference | 22.1 | pressure 6, gap 8.1 | `/triage-lead ag-ui` |
| awesome-llm-agents | Reference | 22.1 | pressure 6, gap 8.1 | `/triage-lead awesome-llm-agents` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
