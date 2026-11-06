# Next evals — a banded promotion queue

The 879 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 122 distinct values across these 879 leads (366 have zero overlap pressure; largest tie: 74) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 247 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 601 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 67.7 | pressure 30, gap 7.7 | `/evaluate-tool vet` |
| orca | Implement | 60.6 | pressure 27, gap 6.6 | `/evaluate-tool orca` |
| cognee | Memory & Context | 56.9 | pressure 25, gap 6.9 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 48.0 | pressure 20, gap 8.0 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 46.9 | pressure 20, gap 6.9 | `/evaluate-tool mem0` |
| aider | Implement | 42.6 | pressure 18, gap 6.6 | `/evaluate-tool aider` |
| Understand-Anything | Plan | 42.6 | pressure 18, gap 6.6 | `/evaluate-tool Understand-Anything` |
| claude-octopus | Review | 41.7 | pressure 17, gap 7.7 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 39.7 | pressure 16, gap 7.7 | `/evaluate-tool ghostsecurity/skills` |
| goose | Implement | 38.6 | pressure 16, gap 6.6 | `/evaluate-tool goose` |
| sandcastle | Implement | 38.6 | pressure 16, gap 6.6 | `/evaluate-tool sandcastle` |
| AgentMemory (hsuanshao) | Memory & Context | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool AgentMemory (hsuanshao)` |
| agentmemory | Memory & Context | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool agentmemory` |
| worktrunk | Ship | 36.8 | pressure 14, gap 8.8 | `/evaluate-tool worktrunk` |
| OpenHands | Implement | 36.6 | pressure 15, gap 6.6 | `/evaluate-tool OpenHands` |
| gastown | Implement | 36.6 | pressure 15, gap 6.6 | `/evaluate-tool gastown` |
| supermemory | Memory & Context | 34.9 | pressure 13, gap 6.9 | `/evaluate-tool supermemory` |
| ralph-claude-code | Implement | 34.6 | pressure 14, gap 6.6 | `/evaluate-tool ralph-claude-code` |
| browser-use | Verify | 34.2 | pressure 14, gap 6.2 | `/evaluate-tool browser-use` |
| awesome-agent-skills | Reference | 33.2 | pressure 12, gap 7.2 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 33.2 | pressure 12, gap 7.2 | `/evaluate-tool awesome-agent-skills (libukai)` |
| impeccable | Skills & Plugins | 32.8 | pressure 13, gap 6.8 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.8 | pressure 13, gap 6.8 | `/evaluate-tool ui-ux-pro-max` |
| MemOS | Memory & Context | 30.9 | pressure 12, gap 6.9 | `/evaluate-tool MemOS` |
| claude-code-router | Implement | 30.6 | pressure 12, gap 6.6 | `/evaluate-tool claude-code-router` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 247 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 247 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| roundtable | Outer Loop | 28.0 | challenges abtop · pressure 10, gap 8.0 | `/triage-lead roundtable` |
| skill-scanner | Review | 27.7 | challenges SkillSpector · pressure 10, gap 7.7 | `/triage-lead skill-scanner` |
| ACE (agentic-context-engine) | Memory & Context | 26.9 | challenges claude-reflect · pressure 10, gap 6.9 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 26.9 | challenges claude-mem · pressure 10, gap 6.9 | `/triage-lead engram` |
| openskills | Skills & Plugins | 26.8 | challenges skill-creator · pressure 9, gap 6.8 | `/triage-lead openskills` |
| agnix | Review | 25.7 | challenges SkillSpector · pressure 8, gap 7.7 | `/triage-lead agnix` |
| mcp-context-forge | MCP Servers | 25.3 | challenges fastmcp · pressure 8, gap 7.3 | `/triage-lead mcp-context-forge` |
| memU | Memory & Context | 24.9 | challenges claude-mem · pressure 9, gap 6.9 | `/triage-lead memU` |
| ownmem | Memory & Context | 24.9 | challenges claude-mem · pressure 9, gap 6.9 | `/triage-lead ownmem` |
| garak | Outer Loop | 24.0 | challenges SkillSpector · pressure 7, gap 8.0 | `/triage-lead garak` |
| agent-scan | Review | 23.7 | challenges SkillSpector · pressure 8, gap 7.7 | `/triage-lead agent-scan` |
| mex | Memory & Context | 22.9 | challenges claude-mem · pressure 8, gap 6.9 | `/triage-lead mex` |

## P3 backlog — 601 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 601 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| deadeye-cc | Implement | 30.6 | pressure 12, gap 6.6 | `/triage-lead deadeye-cc` |
| gstack | Implement | 30.6 | pressure 11, gap 6.6 | `/triage-lead gstack` |
| OpenSpec | Plan | 30.6 | pressure 12, gap 6.6 | `/triage-lead OpenSpec` |
| opik | Outer Loop | 30.0 | pressure 11, gap 8.0 | `/triage-lead opik` |
| cc-safety-net | Review | 29.7 | pressure 10, gap 7.7 | `/triage-lead cc-safety-net` |
| CLIProxyAPI | Implement | 28.6 | pressure 11, gap 6.6 | `/triage-lead CLIProxyAPI` |
| gptme | Implement | 28.6 | pressure 10, gap 6.6 | `/triage-lead gptme` |
| qwen-code | Implement | 28.6 | pressure 10, gap 6.6 | `/triage-lead qwen-code` |
| ruflo | Implement | 28.6 | pressure 10, gap 6.6 | `/triage-lead ruflo` |
| compound-engineering | Implement | 26.6 | pressure 9, gap 6.6 | `/triage-lead compound-engineering` |
| buildwithclaude | Reference | 25.2 | pressure 8, gap 7.2 | `/triage-lead buildwithclaude` |
| bifrost | Implement | 24.6 | pressure 8, gap 6.6 | `/triage-lead bifrost` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 17.3 | ships inside `prisma/prisma` · pressure 4, gap 7.3 | `/triage-lead prisma` |
| webapp-testing | Verify | 14.2 | ships inside `anthropics/skills` · pressure 3, gap 6.2 | `/triage-lead webapp-testing` |
| confluence | MCP Servers | 9.3 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.3 | `/triage-lead confluence` |
| jira | MCP Servers | 9.3 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.3 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.8 | ships inside `github/awesome-copilot` · pressure 0, gap 6.8 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.8 | ships inside `getsentry/skills` · pressure 0, gap 6.8 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
