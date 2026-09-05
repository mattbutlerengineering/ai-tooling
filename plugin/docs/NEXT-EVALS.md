# Next evals — a banded promotion queue

The 518 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 102 distinct values across these 518 leads (222 have zero overlap pressure; largest tie: 37) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 151 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 337 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 44.4 | pressure 18, gap 6.4 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 40.9 | pressure 17, gap 6.9 | `/evaluate-tool langfuse` |
| OpenHands | Implement | 37.4 | pressure 15, gap 5.4 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.4 | pressure 15, gap 5.4 | `/evaluate-tool goose` |
| mem0 | Memory & Context | 36.4 | pressure 14, gap 6.4 | `/evaluate-tool mem0` |
| supermemory | Memory & Context | 34.4 | pressure 13, gap 6.4 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.4 | pressure 13, gap 5.4 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.4 | pressure 12, gap 6.4 | `/evaluate-tool MemOS` |
| awesome-agent-skills | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.9 | pressure 10, gap 6.9 | `/evaluate-tool opik` |
| orca | Implement | 39.4 | pressure 16, gap 5.4 | `/evaluate-tool orca` |
| vet | Review | 38.5 | pressure 15, gap 6.5 | `/evaluate-tool vet` |
| aider | Implement | 37.4 | pressure 16, gap 5.4 | `/evaluate-tool aider` |
| gastown | Implement | 35.4 | pressure 14, gap 5.4 | `/evaluate-tool gastown` |
| ghostsecurity/skills | Review | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 34.4 | pressure 13, gap 6.4 | `/evaluate-tool agentmemory` |
| ui-ux-pro-max | Skills & Plugins | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool ui-ux-pro-max` |
| impeccable | Skills & Plugins | 30.5 | pressure 11, gap 6.5 | `/evaluate-tool impeccable` |
| worktrunk | Ship | 29.5 | pressure 10, gap 7.5 | `/evaluate-tool worktrunk` |
| browser-use | Verify | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool browser-use` |
| ralph-claude-code | Implement | 29.4 | pressure 11, gap 5.4 | `/evaluate-tool ralph-claude-code` |
| claude-octopus | Review | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool claude-octopus` |
| ACE (agentic-context-engine) | Memory & Context | 28.4 | pressure 10, gap 6.4 | `/evaluate-tool ACE (agentic-context-engine)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 151 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 151 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| oh-my-fable | Skills & Plugins | 6.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 0, gap 6.5 | `/triage-lead oh-my-fable` |
| memU | Memory & Context | 26.4 | challenges claude-mem · pressure 9, gap 6.4 | `/triage-lead memU` |
| gstack | Implement | 25.4 | challenges GSD · pressure 9, gap 5.4 | `/triage-lead gstack` |
| ruflo | Implement | 25.4 | challenges GSD · pressure 9, gap 5.4 | `/triage-lead ruflo` |
| openskills | Skills & Plugins | 24.5 | challenges skill-creator · pressure 8, gap 6.5 | `/triage-lead openskills` |
| engram | Memory & Context | 24.4 | challenges claude-mem · pressure 8, gap 6.4 | `/triage-lead engram` |
| Understand-Anything | Plan | 23.5 | challenges codegraph · pressure 8, gap 5.5 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.4 | challenges GSD · pressure 8, gap 5.4 | `/triage-lead compound-engineering` |
| garak | Outer Loop | 20.9 | challenges SkillSpector · pressure 6, gap 6.9 | `/triage-lead garak` |
| Skill_Seekers | Skills & Plugins | 20.5 | challenges skill-creator · pressure 6, gap 6.5 | `/triage-lead Skill_Seekers` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |
| strands-agents (harness-sdk) | Implement | 19.4 | challenges fastmcp · pressure 6, gap 5.4 | `/triage-lead strands-agents (harness-sdk)` |

## P3 backlog — 337 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 337 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| bough | Outer Loop | 6.9 | pressure 0, gap 6.9 | `/triage-lead bough` |
| search-mcp | MCP Servers | 6.8 | pressure 0, gap 6.8 | `/triage-lead search-mcp` |
| reverify | Review | 6.5 | pressure 0, gap 6.5 | `/triage-lead reverify` |
| claude-rotate | Implement | 5.4 | pressure 0, gap 5.4 | `/triage-lead claude-rotate` |
| codex-remote-pro | Implement | 5.4 | pressure 0, gap 5.4 | `/triage-lead codex-remote-pro` |
| qwen-code | Implement | 25.4 | pressure 9, gap 5.4 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 24.9 | pressure 8, gap 6.9 | `/triage-lead NeMo-Guardrails` |
| buildwithclaude | Reference | 24.8 | pressure 8, gap 6.8 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 23.4 | pressure 9, gap 5.4 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.4 | pressure 8, gap 5.4 | `/triage-lead gemini-cli` |
| gptme | Implement | 23.4 | pressure 8, gap 5.4 | `/triage-lead gptme` |
| ag-ui | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead ag-ui` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 5 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 14.8 | ships inside `prisma/prisma` · pressure 3, gap 6.8 | `/triage-lead prisma` |
| confluence | MCP Servers | 8.8 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.8 | `/triage-lead confluence` |
| jira | MCP Servers | 8.8 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.8 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.5 | ships inside `github/awesome-copilot` · pressure 0, gap 6.5 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.5 | ships inside `getsentry/skills` · pressure 0, gap 6.5 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
