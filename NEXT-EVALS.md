# Next evals — a banded promotion queue

The 472 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 102 distinct values across these 472 leads (186 have zero overlap pressure; largest tie: 37) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 143 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 304 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 57.6 | pressure 24, gap 7.6 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 41.0 | pressure 16, gap 7.0 | `/evaluate-tool cognee` |
| agent-browser | Verify | 39.7 | pressure 15, gap 7.7 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 37.9 | pressure 15, gap 7.9 | `/evaluate-tool langfuse` |
| ECC | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool ECC` |
| OpenHands | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 35.0 | pressure 13, gap 7.0 | `/evaluate-tool supermemory` |
| pydantic-ai | Implement | 33.6 | pressure 12, gap 7.6 | `/evaluate-tool pydantic-ai` |
| spec-kit | Plan | 33.6 | pressure 13, gap 5.6 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool vercel-labs/agent-skills` |
| MemOS | Memory & Context | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool opik` |
| sandcastle | Implement | 29.6 | pressure 10, gap 7.6 | `/evaluate-tool sandcastle` |
| browser-use | Verify | 27.7 | pressure 9, gap 7.7 | `/evaluate-tool browser-use` |
| chrome-devtools-mcp | Verify | 27.7 | pressure 9, gap 7.7 | `/evaluate-tool chrome-devtools-mcp` |
| agent-kit | Implement | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool agent-kit` |
| aider | Implement | 27.6 | pressure 10, gap 7.6 | `/evaluate-tool aider` |
| gstack | Implement | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool gstack` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 143 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 143 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| gastown | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead gastown` |
| claude-octopus | Review | 25.1 | pressure 8, gap 7.1 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 25.1 | pressure 8, gap 7.1 | `/triage-lead tdd-guard` |
| compound-engineering | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead compound-engineering` |
| ralph-claude-code | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead ralph-claude-code` |
| strands-agents (harness-sdk) | Implement | 21.6 | pressure 6, gap 7.6 | `/triage-lead strands-agents (harness-sdk)` |
| Agent-Reach | Research & Discovery | 20.5 | pressure 5, gap 8.5 | `/triage-lead Agent-Reach` |
| autoresearch | Research & Discovery | 20.5 | pressure 5, gap 8.5 | `/triage-lead autoresearch` |
| garak | Outer Loop | 19.9 | pressure 5, gap 7.9 | `/triage-lead garak` |
| agent-orchestrator | Implement | 19.6 | pressure 5, gap 7.6 | `/triage-lead agent-orchestrator` |
| dmux | Implement | 19.6 | pressure 5, gap 7.6 | `/triage-lead dmux` |
| oh-my-claudecode | Implement | 19.6 | pressure 5, gap 7.6 | `/triage-lead oh-my-claudecode` |

## P3 backlog — 304 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 304 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 27.6 | pressure 9, gap 7.6 | `/triage-lead qwen-code` |
| OpenSpec | Plan | 27.6 | pressure 10, gap 5.6 | `/triage-lead OpenSpec` |
| claude-hud | Plan | 27.6 | pressure 10, gap 5.6 | `/triage-lead claude-hud` |
| ui-ux-pro-max | Skills & Plugins | 25.7 | pressure 8, gap 7.7 | `/triage-lead ui-ux-pro-max` |
| CopilotKit | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead CopilotKit` |
| daytona | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead daytona` |
| gemini-cli | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead gemini-cli` |
| voltagent | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead voltagent` |
| awesome-claude-skills (Composio) | Reference | 23.9 | pressure 7, gap 7.9 | `/triage-lead awesome-claude-skills (Composio)` |
| impeccable | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead impeccable` |
| slidev | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead slidev` |
| CLIProxyAPI | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead CLIProxyAPI` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
