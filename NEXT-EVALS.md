# Next evals — a banded promotion queue

The 583 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 107 distinct values across these 583 leads (250 have zero overlap pressure; largest tie: 43) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 172 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 381 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 48.8 | pressure 20, gap 6.8 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 43.3 | pressure 18, gap 7.3 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 40.8 | pressure 16, gap 6.8 | `/evaluate-tool mem0` |
| OpenHands | Implement | 37.6 | pressure 15, gap 5.6 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.6 | pressure 15, gap 5.6 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.6 | pressure 13, gap 5.6 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.8 | pressure 12, gap 6.8 | `/evaluate-tool MemOS` |
| opik | Outer Loop | 31.3 | pressure 11, gap 7.3 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.7 | pressure 11, gap 5.7 | `/evaluate-tool OpenSpec` |
| vet | Review | 50.9 | pressure 21, gap 6.9 | `/evaluate-tool vet` |
| orca | Implement | 41.6 | pressure 17, gap 5.6 | `/evaluate-tool orca` |
| aider | Implement | 39.6 | pressure 17, gap 5.6 | `/evaluate-tool aider` |
| gastown | Implement | 35.6 | pressure 14, gap 5.6 | `/evaluate-tool gastown` |
| ghostsecurity/skills | Review | 34.9 | pressure 13, gap 6.9 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool agentmemory` |
| impeccable | Skills & Plugins | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool ui-ux-pro-max` |
| browser-use | Verify | 32.2 | pressure 12, gap 6.2 | `/evaluate-tool browser-use` |
| ralph-claude-code | Implement | 31.6 | pressure 12, gap 5.6 | `/evaluate-tool ralph-claude-code` |
| worktrunk | Ship | 31.5 | pressure 11, gap 7.5 | `/evaluate-tool worktrunk` |
| claude-octopus | Review | 28.9 | pressure 10, gap 6.9 | `/evaluate-tool claude-octopus` |
| ACE (agentic-context-engine) | Memory & Context | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool ACE (agentic-context-engine)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 172 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 172 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| engram | Memory & Context | 28.8 | challenges claude-mem · pressure 10, gap 6.8 | `/triage-lead engram` |
| ruflo | Implement | 27.6 | challenges GSD · pressure 10, gap 5.6 | `/triage-lead ruflo` |
| openskills | Skills & Plugins | 26.5 | challenges skill-creator · pressure 9, gap 6.5 | `/triage-lead openskills` |
| Understand-Anything | Plan | 25.7 | challenges codegraph · pressure 10, gap 5.7 | `/triage-lead Understand-Anything` |
| gstack | Implement | 25.6 | challenges GSD · pressure 9, gap 5.6 | `/triage-lead gstack` |
| memU | Memory & Context | 24.8 | challenges claude-mem · pressure 9, gap 6.8 | `/triage-lead memU` |
| compound-engineering | Implement | 23.6 | challenges GSD · pressure 8, gap 5.6 | `/triage-lead compound-engineering` |
| roundtable | Outer Loop | 21.3 | challenges abtop · pressure 7, gap 7.3 | `/triage-lead roundtable` |
| garak | Outer Loop | 21.3 | challenges SkillSpector · pressure 6, gap 7.3 | `/triage-lead garak` |
| agnix | Review | 20.9 | challenges SkillSpector · pressure 6, gap 6.9 | `/triage-lead agnix` |
| Skill_Seekers | Skills & Plugins | 20.5 | challenges skill-creator · pressure 6, gap 6.5 | `/triage-lead Skill_Seekers` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |

## P3 backlog — 381 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 381 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| gptme | Implement | 25.6 | pressure 9, gap 5.6 | `/triage-lead gptme` |
| qwen-code | Implement | 25.6 | pressure 9, gap 5.6 | `/triage-lead qwen-code` |
| buildwithclaude | Reference | 25.0 | pressure 8, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 23.6 | pressure 9, gap 5.6 | `/triage-lead CLIProxyAPI` |
| claude-code-router | Implement | 23.6 | pressure 8, gap 5.6 | `/triage-lead claude-code-router` |
| gemini-cli | Implement | 23.6 | pressure 8, gap 5.6 | `/triage-lead gemini-cli` |
| NeMo-Guardrails | Outer Loop | 23.3 | pressure 8, gap 7.3 | `/triage-lead NeMo-Guardrails` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 22.5 | pressure 7, gap 6.5 | `/triage-lead slidev` |
| scenario | Verify | 22.2 | pressure 7, gap 6.2 | `/triage-lead scenario` |
| ccpm | Plan | 21.7 | pressure 7, gap 5.7 | `/triage-lead ccpm` |

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
