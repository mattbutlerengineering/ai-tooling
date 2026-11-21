# Next evals — a banded promotion queue

The 982 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 120 distinct values across these 982 leads (413 have zero overlap pressure; largest tie: 93) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 284 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 667 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 71.8 | pressure 32, gap 7.8 | `/evaluate-tool vet` |
| orca | Implement | 64.9 | pressure 29, gap 6.9 | `/evaluate-tool orca` |
| cognee | Memory & Context | 61.0 | pressure 27, gap 7.0 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 50.1 | pressure 21, gap 8.1 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 49.0 | pressure 21, gap 7.0 | `/evaluate-tool mem0` |
| Understand-Anything | Plan | 44.8 | pressure 19, gap 6.8 | `/evaluate-tool Understand-Anything` |
| aider | Implement | 42.9 | pressure 18, gap 6.9 | `/evaluate-tool aider` |
| worktrunk | Ship | 42.8 | pressure 17, gap 8.8 | `/evaluate-tool worktrunk` |
| browser-use | Verify | 42.6 | pressure 18, gap 6.6 | `/evaluate-tool browser-use` |
| claude-octopus | Review | 41.8 | pressure 17, gap 7.8 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 41.8 | pressure 17, gap 7.8 | `/evaluate-tool ghostsecurity/skills` |
| sandcastle | Implement | 40.9 | pressure 17, gap 6.9 | `/evaluate-tool sandcastle` |
| claude-code-router | Implement | 38.9 | pressure 16, gap 6.9 | `/evaluate-tool claude-code-router` |
| goose | Implement | 38.9 | pressure 16, gap 6.9 | `/evaluate-tool goose` |
| AgentMemory (hsuanshao) | Memory & Context | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool AgentMemory (hsuanshao)` |
| agentmemory | Memory & Context | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool agentmemory` |
| impeccable | Skills & Plugins | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool ui-ux-pro-max` |
| OpenHands | Implement | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool OpenHands` |
| gastown | Implement | 36.9 | pressure 15, gap 6.9 | `/evaluate-tool gastown` |
| supermemory | Memory & Context | 35.0 | pressure 13, gap 7.0 | `/evaluate-tool supermemory` |
| deadeye-cc | Implement | 34.9 | pressure 14, gap 6.9 | `/evaluate-tool deadeye-cc` |
| ralph-claude-code | Implement | 34.9 | pressure 14, gap 6.9 | `/evaluate-tool ralph-claude-code` |
| awesome-agent-skills | Reference | 33.3 | pressure 12, gap 7.3 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 33.3 | pressure 12, gap 7.3 | `/evaluate-tool awesome-agent-skills (libukai)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 284 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 284 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| roundtable | Outer Loop | 30.1 | challenges abtop · pressure 11, gap 8.1 | `/triage-lead roundtable` |
| agent-scan | Review | 29.8 | challenges SkillSpector · pressure 11, gap 7.8 | `/triage-lead agent-scan` |
| skill-scanner | Review | 29.8 | challenges SkillSpector · pressure 11, gap 7.8 | `/triage-lead skill-scanner` |
| mcp-context-forge | MCP Servers | 27.4 | challenges fastmcp · pressure 9, gap 7.4 | `/triage-lead mcp-context-forge` |
| ACE (agentic-context-engine) | Memory & Context | 27.0 | challenges claude-reflect · pressure 10, gap 7.0 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 27.0 | challenges claude-mem · pressure 10, gap 7.0 | `/triage-lead engram` |
| openskills | Skills & Plugins | 26.9 | challenges skill-creator · pressure 9, gap 6.9 | `/triage-lead openskills` |
| foreman (ilkemerol) | Implement | 26.9 | challenges claude-squad · pressure 10, gap 6.9 | `/triage-lead foreman (ilkemerol)` |
| Foreman | Plan | 26.8 | challenges GSD · pressure 10, gap 6.8 | `/triage-lead Foreman` |
| agnix | Review | 25.8 | challenges SkillSpector · pressure 8, gap 7.8 | `/triage-lead agnix` |
| memU | Memory & Context | 25.0 | challenges claude-mem · pressure 9, gap 7.0 | `/triage-lead memU` |
| mex | Memory & Context | 25.0 | challenges claude-mem · pressure 9, gap 7.0 | `/triage-lead mex` |

## P3 backlog — 667 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 667 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| gstack | Implement | 32.9 | pressure 12, gap 6.9 | `/triage-lead gstack` |
| OpenSpec | Plan | 32.8 | pressure 13, gap 6.8 | `/triage-lead OpenSpec` |
| MemOS | Memory & Context | 31.0 | pressure 12, gap 7.0 | `/triage-lead MemOS` |
| CLIProxyAPI | Implement | 30.9 | pressure 12, gap 6.9 | `/triage-lead CLIProxyAPI` |
| opik | Outer Loop | 30.1 | pressure 11, gap 8.1 | `/triage-lead opik` |
| cc-safety-net | Review | 29.8 | pressure 10, gap 7.8 | `/triage-lead cc-safety-net` |
| gptme | Implement | 28.9 | pressure 10, gap 6.9 | `/triage-lead gptme` |
| qwen-code | Implement | 28.9 | pressure 10, gap 6.9 | `/triage-lead qwen-code` |
| ruflo | Implement | 28.9 | pressure 10, gap 6.9 | `/triage-lead ruflo` |
| buildwithclaude | Reference | 27.3 | pressure 9, gap 7.3 | `/triage-lead buildwithclaude` |
| compound-engineering | Implement | 26.9 | pressure 9, gap 6.9 | `/triage-lead compound-engineering` |
| toolpermit | Review | 25.8 | pressure 9, gap 7.8 | `/triage-lead toolpermit` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 17.4 | ships inside `prisma/prisma` · pressure 4, gap 7.4 | `/triage-lead prisma` |
| webapp-testing | Verify | 16.6 | ships inside `anthropics/skills` · pressure 4, gap 6.6 | `/triage-lead webapp-testing` |
| confluence | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead confluence` |
| jira | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.9 | ships inside `github/awesome-copilot` · pressure 0, gap 6.9 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.9 | ships inside `getsentry/skills` · pressure 0, gap 6.9 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
