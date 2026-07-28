# Next evals — a banded promotion queue

The 461 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score only has ~83 distinct values across these leads — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 154 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 282 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 58.0 | pressure 24, gap 8.0 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.1 | pressure 15, gap 8.1 | `/evaluate-tool cognee` |
| ECC | Implement | 40.0 | pressure 15, gap 8.0 | `/evaluate-tool ECC` |
| OpenHands | Implement | 38.0 | pressure 14, gap 8.0 | `/evaluate-tool OpenHands` |
| goose | Implement | 38.0 | pressure 14, gap 8.0 | `/evaluate-tool goose` |
| langfuse | Outer Loop | 37.9 | pressure 15, gap 7.9 | `/evaluate-tool langfuse` |
| agent-browser | Verify | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool agent-browser` |
| supermemory | Memory & Context | 36.1 | pressure 13, gap 8.1 | `/evaluate-tool supermemory` |
| promptfoo | Outer Loop | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool promptfoo` |
| pydantic-ai | Implement | 34.0 | pressure 12, gap 8.0 | `/evaluate-tool pydantic-ai` |
| spec-kit | Plan | 32.2 | pressure 12, gap 6.2 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 32.1 | pressure 11, gap 8.1 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool vercel-labs/agent-skills` |
| awesome-agent-skills | Reference | 30.1 | pressure 10, gap 8.1 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.1 | pressure 10, gap 8.1 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 30.1 | pressure 10, gap 8.1 | `/evaluate-tool MemOS` |
| orca | Implement | 30.0 | pressure 10, gap 8.0 | `/evaluate-tool orca` |
| ruflo | Implement | 30.0 | pressure 10, gap 8.0 | `/evaluate-tool ruflo` |
| opik | Outer Loop | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool opik` |
| mem0 | Memory & Context | 28.1 | pressure 9, gap 8.1 | `/evaluate-tool mem0` |
| agent-kit | Implement | 28.0 | pressure 9, gap 8.0 | `/evaluate-tool agent-kit` |
| qwen-code | Implement | 28.0 | pressure 9, gap 8.0 | `/evaluate-tool qwen-code` |
| sandcastle | Implement | 28.0 | pressure 9, gap 8.0 | `/evaluate-tool sandcastle` |
| browser-use | Verify | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool browser-use` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 154 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 154 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| ghostsecurity/skills | Review | 27.1 | pressure 9, gap 7.1 | `/triage-lead ghostsecurity/skills` |
| agentmemory | Memory & Context | 26.1 | pressure 8, gap 8.1 | `/triage-lead agentmemory` |
| gstack | Implement | 26.0 | pressure 8, gap 8.0 | `/triage-lead gstack` |
| chrome-devtools-mcp | Verify | 25.6 | pressure 8, gap 7.6 | `/triage-lead chrome-devtools-mcp` |
| BMAD-METHOD | Plan | 24.2 | pressure 8, gap 6.2 | `/triage-lead BMAD-METHOD` |
| Understand-Anything | Plan | 24.2 | pressure 8, gap 6.2 | `/triage-lead Understand-Anything` |
| ACE (agentic-context-engine) | Memory & Context | 24.1 | pressure 7, gap 8.1 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 24.1 | pressure 7, gap 8.1 | `/triage-lead memU` |
| compound-engineering | Implement | 24.0 | pressure 7, gap 8.0 | `/triage-lead compound-engineering` |
| gastown | Implement | 24.0 | pressure 7, gap 8.0 | `/triage-lead gastown` |
| ralph-claude-code | Implement | 24.0 | pressure 7, gap 8.0 | `/triage-lead ralph-claude-code` |
| dmux | Implement | 22.0 | pressure 6, gap 8.0 | `/triage-lead dmux` |

## P3 backlog — 282 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 282 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| claude-hud | Plan | 26.2 | pressure 9, gap 6.2 | `/triage-lead claude-hud` |
| CopilotKit | Implement | 26.0 | pressure 8, gap 8.0 | `/triage-lead CopilotKit` |
| gemini-cli | Implement | 26.0 | pressure 8, gap 8.0 | `/triage-lead gemini-cli` |
| voltagent | Implement | 26.0 | pressure 8, gap 8.0 | `/triage-lead voltagent` |
| OpenSpec | Plan | 24.2 | pressure 8, gap 6.2 | `/triage-lead OpenSpec` |
| awesome-claude-skills (Composio) | Reference | 24.1 | pressure 7, gap 8.1 | `/triage-lead awesome-claude-skills (Composio)` |
| daytona | Implement | 24.0 | pressure 7, gap 8.0 | `/triage-lead daytona` |
| fast-agent | Implement | 24.0 | pressure 7, gap 8.0 | `/triage-lead fast-agent` |
| slidev | Skills & Plugins | 23.9 | pressure 7, gap 7.9 | `/triage-lead slidev` |
| ui-ux-pro-max | Skills & Plugins | 23.9 | pressure 7, gap 7.9 | `/triage-lead ui-ux-pro-max` |
| awesome-claude-skills (behisecc) | Reference | 22.1 | pressure 7, gap 8.1 | `/triage-lead awesome-claude-skills (behisecc)` |
| ag-ui | Reference | 22.1 | pressure 6, gap 8.1 | `/triage-lead ag-ui` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
