# Next evals — a banded promotion queue

The 1022 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 127 distinct values across these 1022 leads (435 have zero overlap pressure; largest tie: 100) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 298 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 693 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 76.0 | pressure 34, gap 8.0 | `/evaluate-tool vet` |
| orca | Implement | 65.0 | pressure 29, gap 7.0 | `/evaluate-tool orca` |
| cognee | Memory & Context | 61.1 | pressure 27, gap 7.1 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 50.2 | pressure 21, gap 8.2 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 49.1 | pressure 21, gap 7.1 | `/evaluate-tool mem0` |
| Understand-Anything | Plan | 44.8 | pressure 19, gap 6.8 | `/evaluate-tool Understand-Anything` |
| worktrunk | Ship | 44.8 | pressure 18, gap 8.8 | `/evaluate-tool worktrunk` |
| ghostsecurity/skills | Review | 44.0 | pressure 18, gap 8.0 | `/evaluate-tool ghostsecurity/skills` |
| aider | Implement | 43.0 | pressure 18, gap 7.0 | `/evaluate-tool aider` |
| browser-use | Verify | 42.8 | pressure 18, gap 6.8 | `/evaluate-tool browser-use` |
| claude-octopus | Review | 42.0 | pressure 17, gap 8.0 | `/evaluate-tool claude-octopus` |
| sandcastle | Implement | 41.0 | pressure 17, gap 7.0 | `/evaluate-tool sandcastle` |
| agent-scan | Review | 40.0 | pressure 16, gap 8.0 | `/evaluate-tool agent-scan` |
| claude-code-router | Implement | 39.0 | pressure 16, gap 7.0 | `/evaluate-tool claude-code-router` |
| goose | Implement | 39.0 | pressure 16, gap 7.0 | `/evaluate-tool goose` |
| AgentMemory (hsuanshao) | Memory & Context | 37.1 | pressure 15, gap 7.1 | `/evaluate-tool AgentMemory (hsuanshao)` |
| agentmemory | Memory & Context | 37.1 | pressure 15, gap 7.1 | `/evaluate-tool agentmemory` |
| OpenHands | Implement | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool OpenHands` |
| gastown | Implement | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool gastown` |
| impeccable | Skills & Plugins | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 37.0 | pressure 15, gap 7.0 | `/evaluate-tool ui-ux-pro-max` |
| awesome-agent-skills | Reference | 35.3 | pressure 13, gap 7.3 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 35.3 | pressure 13, gap 7.3 | `/evaluate-tool awesome-agent-skills (libukai)` |
| supermemory | Memory & Context | 35.1 | pressure 13, gap 7.1 | `/evaluate-tool supermemory` |
| deadeye-cc | Implement | 35.0 | pressure 14, gap 7.0 | `/evaluate-tool deadeye-cc` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 298 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 298 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| crosscheck | Review | 8.0 | challenges code-review, pr-review-toolkit · pressure 0, gap 8.0 | `/triage-lead crosscheck` |
| Chord | Implement | 7.0 | challenges claude-squad · pressure 0, gap 7.0 | `/triage-lead Chord` |
| hub (icons8) | Implement | 7.0 | challenges claude-squad · pressure 0, gap 7.0 | `/triage-lead hub (icons8)` |
| margincue | Plan | 6.8 | challenges GSD · pressure 0, gap 6.8 | `/triage-lead margincue` |
| roundtable | Outer Loop | 30.2 | challenges abtop · pressure 11, gap 8.2 | `/triage-lead roundtable` |
| skill-scanner | Review | 30.0 | challenges SkillSpector · pressure 11, gap 8.0 | `/triage-lead skill-scanner` |
| foreman (ilkemerol) | Implement | 29.0 | challenges claude-squad · pressure 11, gap 7.0 | `/triage-lead foreman (ilkemerol)` |
| Foreman | Plan | 28.8 | challenges GSD · pressure 11, gap 6.8 | `/triage-lead Foreman` |
| mcp-context-forge | MCP Servers | 27.4 | challenges fastmcp · pressure 9, gap 7.4 | `/triage-lead mcp-context-forge` |
| ACE (agentic-context-engine) | Memory & Context | 27.1 | challenges claude-reflect · pressure 10, gap 7.1 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 27.1 | challenges claude-mem · pressure 10, gap 7.1 | `/triage-lead engram` |
| openskills | Skills & Plugins | 27.0 | challenges skill-creator · pressure 9, gap 7.0 | `/triage-lead openskills` |

## P3 backlog — 693 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 693 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ARTEX-CC | Review | 8.0 | pressure 0, gap 8.0 | `/triage-lead ARTEX-CC` |
| dsh-godbot | Implement | 7.0 | pressure 0, gap 7.0 | `/triage-lead dsh-godbot` |
| vmbridge | Implement | 7.0 | pressure 0, gap 7.0 | `/triage-lead vmbridge` |
| ralph-claude-code | Implement | 35.0 | pressure 14, gap 7.0 | `/triage-lead ralph-claude-code` |
| gstack | Implement | 33.0 | pressure 12, gap 7.0 | `/triage-lead gstack` |
| OpenSpec | Plan | 32.8 | pressure 13, gap 6.8 | `/triage-lead OpenSpec` |
| MemOS | Memory & Context | 31.1 | pressure 12, gap 7.1 | `/triage-lead MemOS` |
| CLIProxyAPI | Implement | 31.0 | pressure 12, gap 7.0 | `/triage-lead CLIProxyAPI` |
| opik | Outer Loop | 30.2 | pressure 11, gap 8.2 | `/triage-lead opik` |
| cc-safety-net | Review | 30.0 | pressure 10, gap 8.0 | `/triage-lead cc-safety-net` |
| gptme | Implement | 29.0 | pressure 10, gap 7.0 | `/triage-lead gptme` |
| qwen-code | Implement | 29.0 | pressure 10, gap 7.0 | `/triage-lead qwen-code` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| webapp-testing | Verify | 18.8 | ships inside `anthropics/skills` · pressure 5, gap 6.8 | `/triage-lead webapp-testing` |
| prisma | MCP Servers | 17.4 | ships inside `prisma/prisma` · pressure 4, gap 7.4 | `/triage-lead prisma` |
| confluence | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead confluence` |
| jira | MCP Servers | 9.4 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.4 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 9.0 | ships inside `github/awesome-copilot` · pressure 0, gap 7.0 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 7.0 | ships inside `getsentry/skills` · pressure 0, gap 7.0 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
