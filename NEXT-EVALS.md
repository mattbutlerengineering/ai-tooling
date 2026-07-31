# Next evals — a banded promotion queue

The 465 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score only has ~83 distinct values across these leads — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 151 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 289 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 57.6 | pressure 24, gap 7.6 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 39.9 | pressure 15, gap 7.9 | `/evaluate-tool cognee` |
| agent-browser | Verify | 39.7 | pressure 15, gap 7.7 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 37.9 | pressure 15, gap 7.9 | `/evaluate-tool langfuse` |
| ECC | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool ECC` |
| OpenHands | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool supermemory` |
| promptfoo | Outer Loop | 35.9 | pressure 13, gap 7.9 | `/evaluate-tool promptfoo` |
| spec-kit | Plan | 34.1 | pressure 13, gap 6.1 | `/evaluate-tool spec-kit` |
| pydantic-ai | Implement | 33.6 | pressure 12, gap 7.6 | `/evaluate-tool pydantic-ai` |
| awesome-claude-code | Reference | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 31.7 | pressure 11, gap 7.7 | `/evaluate-tool vercel-labs/agent-skills` |
| awesome-agent-skills | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool MemOS` |
| opik | Outer Loop | 29.9 | pressure 10, gap 7.9 | `/evaluate-tool opik` |
| sandcastle | Implement | 29.6 | pressure 10, gap 7.6 | `/evaluate-tool sandcastle` |
| OpenSpec | Plan | 28.1 | pressure 10, gap 6.1 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 28.1 | pressure 10, gap 6.1 | `/evaluate-tool claude-hud` |
| mem0 | Memory & Context | 27.9 | pressure 9, gap 7.9 | `/evaluate-tool mem0` |
| browser-use | Verify | 27.7 | pressure 9, gap 7.7 | `/evaluate-tool browser-use` |
| agent-kit | Implement | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool agent-kit` |
| gstack | Implement | 27.6 | pressure 9, gap 7.6 | `/evaluate-tool gstack` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 151 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 151 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| orca | Implement | 27.6 | pressure 9, gap 7.6 | `/triage-lead orca` |
| ruflo | Implement | 27.6 | pressure 9, gap 7.6 | `/triage-lead ruflo` |
| ghostsecurity/skills | Review | 26.9 | pressure 9, gap 6.9 | `/triage-lead ghostsecurity/skills` |
| BMAD-METHOD | Plan | 26.1 | pressure 9, gap 6.1 | `/triage-lead BMAD-METHOD` |
| agentmemory | Memory & Context | 25.9 | pressure 8, gap 7.9 | `/triage-lead agentmemory` |
| chrome-devtools-mcp | Verify | 25.7 | pressure 8, gap 7.7 | `/triage-lead chrome-devtools-mcp` |
| gastown | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead gastown` |
| vet | Review | 24.9 | pressure 8, gap 6.9 | `/triage-lead vet` |
| Understand-Anything | Plan | 24.1 | pressure 8, gap 6.1 | `/triage-lead Understand-Anything` |
| ACE (agentic-context-engine) | Memory & Context | 23.9 | pressure 7, gap 7.9 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 23.9 | pressure 7, gap 7.9 | `/triage-lead memU` |
| compound-engineering | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead compound-engineering` |

## P3 backlog — 289 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 289 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 27.6 | pressure 9, gap 7.6 | `/triage-lead qwen-code` |
| CopilotKit | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead CopilotKit` |
| daytona | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead daytona` |
| gemini-cli | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead gemini-cli` |
| voltagent | Implement | 25.6 | pressure 8, gap 7.6 | `/triage-lead voltagent` |
| awesome-claude-skills (Composio) | Reference | 23.9 | pressure 7, gap 7.9 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead slidev` |
| ui-ux-pro-max | Skills & Plugins | 23.7 | pressure 7, gap 7.7 | `/triage-lead ui-ux-pro-max` |
| CLIProxyAPI | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 23.6 | pressure 7, gap 7.6 | `/triage-lead fast-agent` |
| ag-ui | Reference | 21.9 | pressure 6, gap 7.9 | `/triage-lead ag-ui` |
| awesome-llm-agents | Reference | 21.9 | pressure 6, gap 7.9 | `/triage-lead awesome-llm-agents` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
