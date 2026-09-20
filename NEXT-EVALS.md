# Next evals — a banded promotion queue

The 625 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 105 distinct values across these 625 leads (266 have zero overlap pressure; largest tie: 49) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 187 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 408 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 52.7 | pressure 22, gap 6.7 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 43.4 | pressure 18, gap 7.4 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 40.7 | pressure 16, gap 6.7 | `/evaluate-tool mem0` |
| OpenHands | Implement | 37.8 | pressure 15, gap 5.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.8 | pressure 15, gap 5.8 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.7 | pressure 13, gap 6.7 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.8 | pressure 13, gap 5.8 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool MemOS` |
| opik | Outer Loop | 31.4 | pressure 11, gap 7.4 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.8 | pressure 11, gap 5.8 | `/evaluate-tool OpenSpec` |
| vet | Review | 55.2 | pressure 23, gap 7.2 | `/evaluate-tool vet` |
| orca | Implement | 41.8 | pressure 17, gap 5.8 | `/evaluate-tool orca` |
| aider | Implement | 39.8 | pressure 17, gap 5.8 | `/evaluate-tool aider` |
| ghostsecurity/skills | Review | 39.2 | pressure 15, gap 7.2 | `/evaluate-tool ghostsecurity/skills` |
| gastown | Implement | 35.8 | pressure 14, gap 5.8 | `/evaluate-tool gastown` |
| agentmemory | Memory & Context | 34.7 | pressure 13, gap 6.7 | `/evaluate-tool agentmemory` |
| browser-use | Verify | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool browser-use` |
| impeccable | Skills & Plugins | 32.6 | pressure 12, gap 6.6 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.6 | pressure 12, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| ralph-claude-code | Implement | 31.8 | pressure 12, gap 5.8 | `/evaluate-tool ralph-claude-code` |
| worktrunk | Ship | 31.5 | pressure 11, gap 7.5 | `/evaluate-tool worktrunk` |
| claude-octopus | Review | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool claude-octopus` |
| ACE (agentic-context-engine) | Memory & Context | 28.7 | pressure 10, gap 6.7 | `/evaluate-tool ACE (agentic-context-engine)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 187 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 187 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| engram | Memory & Context | 28.7 | challenges claude-mem · pressure 10, gap 6.7 | `/triage-lead engram` |
| Understand-Anything | Plan | 27.8 | challenges codegraph · pressure 10, gap 5.8 | `/triage-lead Understand-Anything` |
| ruflo | Implement | 27.8 | challenges GSD · pressure 10, gap 5.8 | `/triage-lead ruflo` |
| openskills | Skills & Plugins | 26.6 | challenges skill-creator · pressure 9, gap 6.6 | `/triage-lead openskills` |
| gstack | Implement | 25.8 | challenges GSD · pressure 9, gap 5.8 | `/triage-lead gstack` |
| memU | Memory & Context | 24.7 | challenges claude-mem · pressure 9, gap 6.7 | `/triage-lead memU` |
| compound-engineering | Implement | 23.8 | challenges GSD · pressure 8, gap 5.8 | `/triage-lead compound-engineering` |
| roundtable | Outer Loop | 23.4 | challenges abtop · pressure 8, gap 7.4 | `/triage-lead roundtable` |
| garak | Outer Loop | 21.4 | challenges SkillSpector · pressure 6, gap 7.4 | `/triage-lead garak` |
| skill-scanner | Review | 21.2 | challenges SkillSpector · pressure 7, gap 7.2 | `/triage-lead skill-scanner` |
| agnix | Review | 21.2 | challenges SkillSpector · pressure 6, gap 7.2 | `/triage-lead agnix` |
| Skill_Seekers | Skills & Plugins | 20.6 | challenges skill-creator · pressure 6, gap 6.6 | `/triage-lead Skill_Seekers` |

## P3 backlog — 408 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 408 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| claude-code-router | Implement | 27.8 | pressure 10, gap 5.8 | `/triage-lead claude-code-router` |
| gptme | Implement | 25.8 | pressure 9, gap 5.8 | `/triage-lead gptme` |
| qwen-code | Implement | 25.8 | pressure 9, gap 5.8 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 25.4 | pressure 8, gap 7.4 | `/triage-lead NeMo-Guardrails` |
| buildwithclaude | Reference | 25.0 | pressure 8, gap 7.0 | `/triage-lead buildwithclaude` |
| scenario | Verify | 24.2 | pressure 8, gap 6.2 | `/triage-lead scenario` |
| CLIProxyAPI | Implement | 23.8 | pressure 9, gap 5.8 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.8 | pressure 8, gap 5.8 | `/triage-lead gemini-cli` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| ccpm | Plan | 21.8 | pressure 7, gap 5.8 | `/triage-lead ccpm` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 5 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 14.9 | ships inside `prisma/prisma` · pressure 3, gap 6.9 | `/triage-lead prisma` |
| confluence | MCP Servers | 8.9 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.9 | `/triage-lead confluence` |
| jira | MCP Servers | 8.9 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.9 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | ships inside `github/awesome-copilot` · pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.6 | ships inside `getsentry/skills` · pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
