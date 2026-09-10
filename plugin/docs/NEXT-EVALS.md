# Next evals — a banded promotion queue

The 556 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 103 distinct values across these 556 leads (242 have zero overlap pressure; largest tie: 42) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 162 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 364 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 48.7 | pressure 20, gap 6.7 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 43.2 | pressure 18, gap 7.2 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 40.7 | pressure 16, gap 6.7 | `/evaluate-tool mem0` |
| OpenHands | Implement | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.7 | pressure 13, gap 6.7 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.5 | pressure 13, gap 5.5 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool MemOS` |
| opik | Outer Loop | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.6 | pressure 11, gap 5.6 | `/evaluate-tool OpenSpec` |
| vet | Review | 44.8 | pressure 18, gap 6.8 | `/evaluate-tool vet` |
| orca | Implement | 39.5 | pressure 16, gap 5.5 | `/evaluate-tool orca` |
| aider | Implement | 37.5 | pressure 16, gap 5.5 | `/evaluate-tool aider` |
| gastown | Implement | 35.5 | pressure 14, gap 5.5 | `/evaluate-tool gastown` |
| ghostsecurity/skills | Review | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 34.7 | pressure 13, gap 6.7 | `/evaluate-tool agentmemory` |
| impeccable | Skills & Plugins | 32.6 | pressure 12, gap 6.6 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.6 | pressure 12, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| ralph-claude-code | Implement | 31.5 | pressure 12, gap 5.5 | `/evaluate-tool ralph-claude-code` |
| browser-use | Verify | 29.8 | pressure 11, gap 5.8 | `/evaluate-tool browser-use` |
| worktrunk | Ship | 29.5 | pressure 10, gap 7.5 | `/evaluate-tool worktrunk` |
| claude-octopus | Review | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool claude-octopus` |
| ACE (agentic-context-engine) | Memory & Context | 28.7 | pressure 10, gap 6.7 | `/evaluate-tool ACE (agentic-context-engine)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 162 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 162 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ruflo | Implement | 27.5 | challenges GSD · pressure 10, gap 5.5 | `/triage-lead ruflo` |
| engram | Memory & Context | 26.7 | challenges claude-mem · pressure 9, gap 6.7 | `/triage-lead engram` |
| Understand-Anything | Plan | 25.6 | challenges codegraph · pressure 9, gap 5.6 | `/triage-lead Understand-Anything` |
| gstack | Implement | 25.5 | challenges GSD · pressure 9, gap 5.5 | `/triage-lead gstack` |
| memU | Memory & Context | 24.7 | challenges claude-mem · pressure 9, gap 6.7 | `/triage-lead memU` |
| openskills | Skills & Plugins | 24.6 | challenges skill-creator · pressure 8, gap 6.6 | `/triage-lead openskills` |
| compound-engineering | Implement | 23.5 | challenges GSD · pressure 8, gap 5.5 | `/triage-lead compound-engineering` |
| roundtable | Outer Loop | 21.2 | challenges abtop · pressure 7, gap 7.2 | `/triage-lead roundtable` |
| garak | Outer Loop | 21.2 | challenges SkillSpector · pressure 6, gap 7.2 | `/triage-lead garak` |
| Skill_Seekers | Skills & Plugins | 20.6 | challenges skill-creator · pressure 6, gap 6.6 | `/triage-lead Skill_Seekers` |
| andrej-karpathy-skills | Skills & Plugins | 20.6 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.6 | `/triage-lead andrej-karpathy-skills` |
| strands-agents (harness-sdk) | Implement | 19.5 | challenges fastmcp · pressure 6, gap 5.5 | `/triage-lead strands-agents (harness-sdk)` |

## P3 backlog — 364 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 364 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| gptme | Implement | 25.5 | pressure 9, gap 5.5 | `/triage-lead gptme` |
| qwen-code | Implement | 25.5 | pressure 9, gap 5.5 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 25.2 | pressure 8, gap 7.2 | `/triage-lead NeMo-Guardrails` |
| buildwithclaude | Reference | 24.9 | pressure 8, gap 6.9 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 23.5 | pressure 9, gap 5.5 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.5 | pressure 8, gap 5.5 | `/triage-lead gemini-cli` |
| ag-ui | Reference | 22.9 | pressure 7, gap 6.9 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 22.9 | pressure 7, gap 6.9 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| ccpm | Plan | 21.6 | pressure 7, gap 5.6 | `/triage-lead ccpm` |
| claude-code-router | Implement | 21.5 | pressure 7, gap 5.5 | `/triage-lead claude-code-router` |
| fast-agent | Implement | 21.5 | pressure 7, gap 5.5 | `/triage-lead fast-agent` |

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
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | ships inside `github/awesome-copilot` · pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.6 | ships inside `getsentry/skills` · pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
