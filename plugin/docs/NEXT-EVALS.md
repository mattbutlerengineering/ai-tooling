# Next evals — a banded promotion queue

The 465 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score only has ~83 distinct values across these leads — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 148 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 292 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 57.8 | pressure 24, gap 7.8 | `/evaluate-tool opencode` |
| agent-browser | Verify | 39.8 | pressure 15, gap 7.8 | `/evaluate-tool agent-browser` |
| cognee | Memory & Context | 39.8 | pressure 15, gap 7.8 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 37.9 | pressure 15, gap 7.9 | `/evaluate-tool langfuse` |
| ECC | Implement | 37.8 | pressure 14, gap 7.8 | `/evaluate-tool ECC` |
| OpenHands | Implement | 37.8 | pressure 14, gap 7.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.8 | pressure 14, gap 7.8 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 35.8 | pressure 13, gap 7.8 | `/evaluate-tool supermemory` |
| spec-kit | Plan | 33.8 | pressure 13, gap 5.8 | `/evaluate-tool spec-kit` |
| pydantic-ai | Implement | 33.8 | pressure 12, gap 7.8 | `/evaluate-tool pydantic-ai` |
| awesome-claude-code | Reference | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool vercel-labs/agent-skills` |
| awesome-agent-skills | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool opik` |
| agent-kit | Implement | 29.8 | pressure 10, gap 7.8 | `/evaluate-tool agent-kit` |
| sandcastle | Implement | 29.8 | pressure 10, gap 7.8 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 29.8 | pressure 10, gap 7.8 | `/evaluate-tool MemOS` |
| vet | Review | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool vet` |
| OpenSpec | Plan | 27.8 | pressure 10, gap 5.8 | `/evaluate-tool OpenSpec` |
| browser-use | Verify | 27.8 | pressure 9, gap 7.8 | `/evaluate-tool browser-use` |
| gstack | Implement | 27.8 | pressure 9, gap 7.8 | `/evaluate-tool gstack` |
| orca | Implement | 27.8 | pressure 9, gap 7.8 | `/evaluate-tool orca` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 148 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 148 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| ruflo | Implement | 27.8 | pressure 9, gap 7.8 | `/triage-lead ruflo` |
| mem0 | Memory & Context | 27.8 | pressure 9, gap 7.8 | `/triage-lead mem0` |
| ghostsecurity/skills | Review | 26.8 | pressure 9, gap 6.8 | `/triage-lead ghostsecurity/skills` |
| BMAD-METHOD | Plan | 25.8 | pressure 9, gap 5.8 | `/triage-lead BMAD-METHOD` |
| chrome-devtools-mcp | Verify | 25.8 | pressure 8, gap 7.8 | `/triage-lead chrome-devtools-mcp` |
| gastown | Implement | 25.8 | pressure 8, gap 7.8 | `/triage-lead gastown` |
| agentmemory | Memory & Context | 25.8 | pressure 8, gap 7.8 | `/triage-lead agentmemory` |
| Understand-Anything | Plan | 23.8 | pressure 8, gap 5.8 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.8 | pressure 7, gap 7.8 | `/triage-lead compound-engineering` |
| ralph-claude-code | Implement | 23.8 | pressure 7, gap 7.8 | `/triage-lead ralph-claude-code` |
| ACE (agentic-context-engine) | Memory & Context | 23.8 | pressure 7, gap 7.8 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 23.8 | pressure 7, gap 7.8 | `/triage-lead memU` |

## P3 backlog — 292 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 292 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 27.8 | pressure 9, gap 7.8 | `/triage-lead qwen-code` |
| claude-hud | Plan | 25.8 | pressure 9, gap 5.8 | `/triage-lead claude-hud` |
| CopilotKit | Implement | 25.8 | pressure 8, gap 7.8 | `/triage-lead CopilotKit` |
| gemini-cli | Implement | 25.8 | pressure 8, gap 7.8 | `/triage-lead gemini-cli` |
| voltagent | Implement | 25.8 | pressure 8, gap 7.8 | `/triage-lead voltagent` |
| awesome-claude-skills (Composio) | Reference | 23.9 | pressure 7, gap 7.9 | `/triage-lead awesome-claude-skills (Composio)` |
| daytona | Implement | 23.8 | pressure 7, gap 7.8 | `/triage-lead daytona` |
| fast-agent | Implement | 23.8 | pressure 7, gap 7.8 | `/triage-lead fast-agent` |
| slidev | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead slidev` |
| ui-ux-pro-max | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead ui-ux-pro-max` |
| worktrunk | Ship | 22.7 | pressure 7, gap 6.7 | `/triage-lead worktrunk` |
| ag-ui | Reference | 21.9 | pressure 6, gap 7.9 | `/triage-lead ag-ui` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
