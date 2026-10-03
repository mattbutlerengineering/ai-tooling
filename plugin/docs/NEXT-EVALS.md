# Next evals — a banded promotion queue

The 693 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 115 distinct values across these 693 leads (302 have zero overlap pressure; largest tie: 62) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 201 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 461 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| langfuse | Outer Loop | 45.6 | pressure 19, gap 7.6 | `/evaluate-tool langfuse` |
| sandcastle | Implement | 36.0 | pressure 14, gap 6.0 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.9 | pressure 12, gap 6.9 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 31.8 | pressure 12, gap 5.8 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 31.6 | pressure 11, gap 7.6 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| vet | Review | 65.5 | pressure 28, gap 7.5 | `/evaluate-tool vet` |
| cognee | Memory & Context | 54.9 | pressure 23, gap 6.9 | `/evaluate-tool cognee` |
| mem0 | Memory & Context | 44.9 | pressure 18, gap 6.9 | `/evaluate-tool mem0` |
| orca | Implement | 44.0 | pressure 18, gap 6.0 | `/evaluate-tool orca` |
| aider | Implement | 40.0 | pressure 17, gap 6.0 | `/evaluate-tool aider` |
| claude-octopus | Review | 39.5 | pressure 15, gap 7.5 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 39.5 | pressure 15, gap 7.5 | `/evaluate-tool ghostsecurity/skills` |
| OpenHands | Implement | 38.0 | pressure 15, gap 6.0 | `/evaluate-tool OpenHands` |
| gastown | Implement | 38.0 | pressure 15, gap 6.0 | `/evaluate-tool gastown` |
| goose | Implement | 38.0 | pressure 15, gap 6.0 | `/evaluate-tool goose` |
| agentmemory | Memory & Context | 36.9 | pressure 14, gap 6.9 | `/evaluate-tool agentmemory` |
| supermemory | Memory & Context | 34.9 | pressure 13, gap 6.9 | `/evaluate-tool supermemory` |
| browser-use | Verify | 33.5 | pressure 13, gap 5.5 | `/evaluate-tool browser-use` |
| impeccable | Skills & Plugins | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool ui-ux-pro-max` |
| ralph-claude-code | Implement | 32.0 | pressure 12, gap 6.0 | `/evaluate-tool ralph-claude-code` |
| worktrunk | Ship | 32.0 | pressure 11, gap 8.0 | `/evaluate-tool worktrunk` |
| claude-code-router | Implement | 30.0 | pressure 11, gap 6.0 | `/evaluate-tool claude-code-router` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 201 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 201 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| engram | Memory & Context | 28.9 | challenges claude-mem · pressure 10, gap 6.9 | `/triage-lead engram` |
| ACE (agentic-context-engine) | Memory & Context | 26.9 | challenges claude-reflect · pressure 10, gap 6.9 | `/triage-lead ACE (agentic-context-engine)` |
| openskills | Skills & Plugins | 26.7 | challenges skill-creator · pressure 9, gap 6.7 | `/triage-lead openskills` |
| Understand-Anything | Plan | 25.8 | challenges codegraph · pressure 10, gap 5.8 | `/triage-lead Understand-Anything` |
| roundtable | Outer Loop | 25.6 | challenges abtop · pressure 9, gap 7.6 | `/triage-lead roundtable` |
| skill-scanner | Review | 25.5 | challenges SkillSpector · pressure 9, gap 7.5 | `/triage-lead skill-scanner` |
| agnix | Review | 25.5 | challenges SkillSpector · pressure 8, gap 7.5 | `/triage-lead agnix` |
| memU | Memory & Context | 24.9 | challenges claude-mem · pressure 9, gap 6.9 | `/triage-lead memU` |
| mex | Memory & Context | 22.9 | challenges claude-mem · pressure 8, gap 6.9 | `/triage-lead mex` |
| garak | Outer Loop | 21.6 | challenges SkillSpector · pressure 6, gap 7.6 | `/triage-lead garak` |
| Skill_Seekers | Skills & Plugins | 20.7 | challenges skill-creator · pressure 6, gap 6.7 | `/triage-lead Skill_Seekers` |
| andrej-karpathy-skills | Skills & Plugins | 20.7 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.7 | `/triage-lead andrej-karpathy-skills` |

## P3 backlog — 461 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 461 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| gstack | Implement | 28.0 | pressure 10, gap 6.0 | `/triage-lead gstack` |
| ruflo | Implement | 28.0 | pressure 10, gap 6.0 | `/triage-lead ruflo` |
| CLIProxyAPI | Implement | 26.0 | pressure 10, gap 6.0 | `/triage-lead CLIProxyAPI` |
| gptme | Implement | 26.0 | pressure 9, gap 6.0 | `/triage-lead gptme` |
| qwen-code | Implement | 26.0 | pressure 9, gap 6.0 | `/triage-lead qwen-code` |
| buildwithclaude | Reference | 25.0 | pressure 8, gap 7.0 | `/triage-lead buildwithclaude` |
| deadeye-cc | Implement | 24.0 | pressure 9, gap 6.0 | `/triage-lead deadeye-cc` |
| compound-engineering | Implement | 24.0 | pressure 8, gap 6.0 | `/triage-lead compound-engineering` |
| gemini-cli | Implement | 24.0 | pressure 8, gap 6.0 | `/triage-lead gemini-cli` |
| NeMo-Guardrails | Outer Loop | 23.6 | pressure 8, gap 7.6 | `/triage-lead NeMo-Guardrails` |
| scenario | Verify | 23.5 | pressure 8, gap 5.5 | `/triage-lead scenario` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| webapp-testing | Verify | 9.5 | ships inside `anthropics/skills` · pressure 1, gap 5.5 | `/triage-lead webapp-testing` |
| prisma | MCP Servers | 15.1 | ships inside `prisma/prisma` · pressure 3, gap 7.1 | `/triage-lead prisma` |
| confluence | MCP Servers | 9.1 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.1 | `/triage-lead confluence` |
| jira | MCP Servers | 9.1 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.1 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.7 | ships inside `github/awesome-copilot` · pressure 0, gap 6.7 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.7 | ships inside `getsentry/skills` · pressure 0, gap 6.7 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
