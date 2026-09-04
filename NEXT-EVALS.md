# Next evals — a banded promotion queue

The 512 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 108 distinct values across these 512 leads (222 have zero overlap pressure; largest tie: 38) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 150 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 332 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 44.5 | pressure 18, gap 6.5 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 40.9 | pressure 17, gap 6.9 | `/evaluate-tool langfuse` |
| OpenHands | Implement | 37.3 | pressure 15, gap 5.3 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.3 | pressure 15, gap 5.3 | `/evaluate-tool goose` |
| mem0 | Memory & Context | 36.5 | pressure 14, gap 6.5 | `/evaluate-tool mem0` |
| supermemory | Memory & Context | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.3 | pressure 13, gap 5.3 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool MemOS` |
| awesome-agent-skills | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.9 | pressure 10, gap 6.9 | `/evaluate-tool opik` |
| orca | Implement | 39.3 | pressure 16, gap 5.3 | `/evaluate-tool orca` |
| vet | Review | 38.5 | pressure 15, gap 6.5 | `/evaluate-tool vet` |
| aider | Implement | 37.3 | pressure 16, gap 5.3 | `/evaluate-tool aider` |
| gastown | Implement | 35.3 | pressure 14, gap 5.3 | `/evaluate-tool gastown` |
| agentmemory | Memory & Context | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool agentmemory` |
| ghostsecurity/skills | Review | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool ghostsecurity/skills` |
| ui-ux-pro-max | Skills & Plugins | 30.5 | pressure 11, gap 6.5 | `/evaluate-tool ui-ux-pro-max` |
| worktrunk | Ship | 29.5 | pressure 10, gap 7.5 | `/evaluate-tool worktrunk` |
| browser-use | Verify | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool browser-use` |
| ralph-claude-code | Implement | 29.3 | pressure 11, gap 5.3 | `/evaluate-tool ralph-claude-code` |
| ACE (agentic-context-engine) | Memory & Context | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool ACE (agentic-context-engine)` |
| impeccable | Skills & Plugins | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool impeccable` |
| claude-octopus | Review | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool claude-octopus` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 150 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 150 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| memU | Memory & Context | 26.5 | challenges claude-mem · pressure 9, gap 6.5 | `/triage-lead memU` |
| gstack | Implement | 25.3 | challenges GSD · pressure 9, gap 5.3 | `/triage-lead gstack` |
| ruflo | Implement | 25.3 | challenges GSD · pressure 9, gap 5.3 | `/triage-lead ruflo` |
| engram | Memory & Context | 24.5 | challenges claude-mem · pressure 8, gap 6.5 | `/triage-lead engram` |
| openskills | Skills & Plugins | 24.5 | challenges skill-creator · pressure 8, gap 6.5 | `/triage-lead openskills` |
| Understand-Anything | Plan | 23.5 | challenges codegraph · pressure 8, gap 5.5 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.3 | challenges GSD · pressure 8, gap 5.3 | `/triage-lead compound-engineering` |
| garak | Outer Loop | 20.9 | challenges SkillSpector · pressure 6, gap 6.9 | `/triage-lead garak` |
| Skill_Seekers | Skills & Plugins | 20.5 | challenges skill-creator · pressure 6, gap 6.5 | `/triage-lead Skill_Seekers` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |
| strands-agents (harness-sdk) | Implement | 19.3 | challenges fastmcp · pressure 6, gap 5.3 | `/triage-lead strands-agents (harness-sdk)` |
| mcp-use | MCP Servers | 18.8 | challenges fastmcp · pressure 5, gap 6.8 | `/triage-lead mcp-use` |

## P3 backlog — 332 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 332 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| qwen-code | Implement | 25.3 | pressure 9, gap 5.3 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 24.9 | pressure 8, gap 6.9 | `/triage-lead NeMo-Guardrails` |
| buildwithclaude | Reference | 24.8 | pressure 8, gap 6.8 | `/triage-lead buildwithclaude` |
| gemini-cli | Implement | 23.3 | pressure 8, gap 5.3 | `/triage-lead gemini-cli` |
| gptme | Implement | 23.3 | pressure 8, gap 5.3 | `/triage-lead gptme` |
| ag-ui | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 22.5 | pressure 7, gap 6.5 | `/triage-lead slidev` |
| ccpm | Plan | 21.5 | pressure 7, gap 5.5 | `/triage-lead ccpm` |
| CLIProxyAPI | Implement | 21.3 | pressure 8, gap 5.3 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 21.3 | pressure 7, gap 5.3 | `/triage-lead fast-agent` |
| Helicone | Outer Loop | 20.9 | pressure 6, gap 6.9 | `/triage-lead Helicone` |

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
