# Next evals — a banded promotion queue

The 806 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 111 distinct values across these 806 leads (348 have zero overlap pressure; largest tie: 70) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 229 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 546 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 65.7 | pressure 29, gap 7.7 | `/evaluate-tool vet` |
| cognee | Memory & Context | 54.9 | pressure 24, gap 6.9 | `/evaluate-tool cognee` |
| orca | Implement | 54.3 | pressure 24, gap 6.3 | `/evaluate-tool orca` |
| langfuse | Outer Loop | 47.9 | pressure 20, gap 7.9 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 42.9 | pressure 18, gap 6.9 | `/evaluate-tool mem0` |
| aider | Implement | 40.3 | pressure 17, gap 6.3 | `/evaluate-tool aider` |
| claude-octopus | Review | 39.7 | pressure 16, gap 7.7 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 39.7 | pressure 16, gap 7.7 | `/evaluate-tool ghostsecurity/skills` |
| AgentMemory (hsuanshao) | Memory & Context | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool AgentMemory (hsuanshao)` |
| agentmemory | Memory & Context | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool agentmemory` |
| OpenHands | Implement | 36.3 | pressure 15, gap 6.3 | `/evaluate-tool OpenHands` |
| gastown | Implement | 36.3 | pressure 15, gap 6.3 | `/evaluate-tool gastown` |
| goose | Implement | 36.3 | pressure 15, gap 6.3 | `/evaluate-tool goose` |
| sandcastle | Implement | 36.3 | pressure 15, gap 6.3 | `/evaluate-tool sandcastle` |
| supermemory | Memory & Context | 34.9 | pressure 13, gap 6.9 | `/evaluate-tool supermemory` |
| worktrunk | Ship | 34.6 | pressure 13, gap 8.6 | `/evaluate-tool worktrunk` |
| browser-use | Verify | 34.0 | pressure 14, gap 6.0 | `/evaluate-tool browser-use` |
| Understand-Anything | Plan | 32.5 | pressure 13, gap 6.5 | `/evaluate-tool Understand-Anything` |
| ralph-claude-code | Implement | 32.3 | pressure 13, gap 6.3 | `/evaluate-tool ralph-claude-code` |
| awesome-agent-skills | Reference | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 30.9 | pressure 12, gap 6.9 | `/evaluate-tool MemOS` |
| impeccable | Skills & Plugins | 30.7 | pressure 12, gap 6.7 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 30.7 | pressure 12, gap 6.7 | `/evaluate-tool ui-ux-pro-max` |
| OpenSpec | Plan | 30.5 | pressure 12, gap 6.5 | `/evaluate-tool OpenSpec` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 229 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 229 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| roundtable | Outer Loop | 27.9 | challenges abtop · pressure 10, gap 7.9 | `/triage-lead roundtable` |
| skill-scanner | Review | 27.7 | challenges SkillSpector · pressure 10, gap 7.7 | `/triage-lead skill-scanner` |
| ACE (agentic-context-engine) | Memory & Context | 26.9 | challenges claude-reflect · pressure 10, gap 6.9 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 26.9 | challenges claude-mem · pressure 10, gap 6.9 | `/triage-lead engram` |
| openskills | Skills & Plugins | 26.7 | challenges skill-creator · pressure 9, gap 6.7 | `/triage-lead openskills` |
| agnix | Review | 25.7 | challenges SkillSpector · pressure 8, gap 7.7 | `/triage-lead agnix` |
| memU | Memory & Context | 24.9 | challenges claude-mem · pressure 9, gap 6.9 | `/triage-lead memU` |
| garak | Outer Loop | 23.9 | challenges SkillSpector · pressure 7, gap 7.9 | `/triage-lead garak` |
| mcp-context-forge | MCP Servers | 23.4 | challenges fastmcp · pressure 7, gap 7.4 | `/triage-lead mcp-context-forge` |
| mex | Memory & Context | 22.9 | challenges claude-mem · pressure 8, gap 6.9 | `/triage-lead mex` |
| ownmem | Memory & Context | 22.9 | challenges claude-mem · pressure 8, gap 6.9 | `/triage-lead ownmem` |
| dev3000 | Outer Loop | 21.9 | challenges playwright · pressure 7, gap 7.9 | `/triage-lead dev3000` |

## P3 backlog — 546 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 546 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| opik | Outer Loop | 29.9 | pressure 11, gap 7.9 | `/triage-lead opik` |
| claude-code-router | Implement | 28.3 | pressure 11, gap 6.3 | `/triage-lead claude-code-router` |
| gstack | Implement | 28.3 | pressure 10, gap 6.3 | `/triage-lead gstack` |
| ruflo | Implement | 28.3 | pressure 10, gap 6.3 | `/triage-lead ruflo` |
| CLIProxyAPI | Implement | 26.3 | pressure 10, gap 6.3 | `/triage-lead CLIProxyAPI` |
| deadeye-cc | Implement | 26.3 | pressure 10, gap 6.3 | `/triage-lead deadeye-cc` |
| compound-engineering | Implement | 26.3 | pressure 9, gap 6.3 | `/triage-lead compound-engineering` |
| gptme | Implement | 26.3 | pressure 9, gap 6.3 | `/triage-lead gptme` |
| qwen-code | Implement | 26.3 | pressure 9, gap 6.3 | `/triage-lead qwen-code` |
| cc-safety-net | Review | 25.7 | pressure 8, gap 7.7 | `/triage-lead cc-safety-net` |
| buildwithclaude | Reference | 25.2 | pressure 8, gap 7.2 | `/triage-lead buildwithclaude` |
| bifrost | Implement | 24.3 | pressure 8, gap 6.3 | `/triage-lead bifrost` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 15.4 | ships inside `prisma/prisma` · pressure 3, gap 7.4 | `/triage-lead prisma` |
| webapp-testing | Verify | 12.0 | ships inside `anthropics/skills` · pressure 2, gap 6.0 | `/triage-lead webapp-testing` |
| confluence | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead confluence` |
| jira | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.7 | ships inside `github/awesome-copilot` · pressure 0, gap 6.7 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.7 | ships inside `getsentry/skills` · pressure 0, gap 6.7 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
