# Next evals — a banded promotion queue

The 755 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 115 distinct values across these 755 leads (325 have zero overlap pressure; largest tie: 67) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 212 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 512 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 6 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 65.6 | pressure 29, gap 7.6 | `/evaluate-tool vet` |
| cognee | Memory & Context | 54.8 | pressure 24, gap 6.8 | `/evaluate-tool cognee` |
| orca | Implement | 50.2 | pressure 22, gap 6.2 | `/evaluate-tool orca` |
| langfuse | Outer Loop | 45.9 | pressure 19, gap 7.9 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 42.8 | pressure 18, gap 6.8 | `/evaluate-tool mem0` |
| aider | Implement | 40.2 | pressure 17, gap 6.2 | `/evaluate-tool aider` |
| claude-octopus | Review | 39.6 | pressure 16, gap 7.6 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 39.6 | pressure 16, gap 7.6 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool agentmemory` |
| OpenHands | Implement | 36.2 | pressure 15, gap 6.2 | `/evaluate-tool OpenHands` |
| gastown | Implement | 36.2 | pressure 15, gap 6.2 | `/evaluate-tool gastown` |
| goose | Implement | 36.2 | pressure 15, gap 6.2 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 34.2 | pressure 14, gap 6.2 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.8 | pressure 12, gap 6.8 | `/evaluate-tool MemOS` |
| worktrunk | Ship | 32.3 | pressure 12, gap 8.3 | `/evaluate-tool worktrunk` |
| OpenSpec | Plan | 32.1 | pressure 12, gap 6.1 | `/evaluate-tool OpenSpec` |
| browser-use | Verify | 31.9 | pressure 13, gap 5.9 | `/evaluate-tool browser-use` |
| opik | Outer Loop | 31.9 | pressure 11, gap 7.9 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.2 | pressure 11, gap 7.2 | `/evaluate-tool awesome-agent-skills (libukai)` |
| impeccable | Skills & Plugins | 30.7 | pressure 12, gap 6.7 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 30.7 | pressure 12, gap 6.7 | `/evaluate-tool ui-ux-pro-max` |
| ralph-claude-code | Implement | 30.2 | pressure 12, gap 6.2 | `/evaluate-tool ralph-claude-code` |
| claude-code-router | Implement | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool claude-code-router` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 212 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 212 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| codedna | Plan | 6.1 | challenges codegraph · pressure 0, gap 6.1 | `/triage-lead codedna` |
| pensieve | Plan | 6.1 | challenges claude-mem, serena · pressure 0, gap 6.1 | `/triage-lead pensieve` |
| engram | Memory & Context | 28.8 | challenges claude-mem · pressure 10, gap 6.8 | `/triage-lead engram` |
| Understand-Anything | Plan | 28.1 | challenges codegraph · pressure 11, gap 6.1 | `/triage-lead Understand-Anything` |
| skill-scanner | Review | 27.6 | challenges SkillSpector · pressure 10, gap 7.6 | `/triage-lead skill-scanner` |
| ACE (agentic-context-engine) | Memory & Context | 26.8 | challenges claude-reflect · pressure 10, gap 6.8 | `/triage-lead ACE (agentic-context-engine)` |
| openskills | Skills & Plugins | 26.7 | challenges skill-creator · pressure 9, gap 6.7 | `/triage-lead openskills` |
| roundtable | Outer Loop | 25.9 | challenges abtop · pressure 9, gap 7.9 | `/triage-lead roundtable` |
| agnix | Review | 25.6 | challenges SkillSpector · pressure 8, gap 7.6 | `/triage-lead agnix` |
| memU | Memory & Context | 24.8 | challenges claude-mem · pressure 9, gap 6.8 | `/triage-lead memU` |
| mex | Memory & Context | 22.8 | challenges claude-mem · pressure 8, gap 6.8 | `/triage-lead mex` |
| garak | Outer Loop | 21.9 | challenges SkillSpector · pressure 6, gap 7.9 | `/triage-lead garak` |

## P3 backlog — 512 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 512 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| systemprompt-core | Outer Loop | 7.9 | pressure 0, gap 7.9 | `/triage-lead systemprompt-core` |
| repopilot | Review | 7.6 | pressure 0, gap 7.6 | `/triage-lead repopilot` |
| agent-infrastructure-landscape | Reference | 7.2 | pressure 0, gap 7.2 | `/triage-lead agent-infrastructure-landscape` |
| awesome-reverse-engineering | Reference | 7.2 | pressure 0, gap 7.2 | `/triage-lead awesome-reverse-engineering` |
| graphersal | Memory & Context | 6.8 | pressure 0, gap 6.8 | `/triage-lead graphersal` |
| archify | Skills & Plugins | 6.7 | pressure 0, gap 6.7 | `/triage-lead archify` |
| PortPilot | Implement | 6.2 | pressure 0, gap 6.2 | `/triage-lead PortPilot` |
| agentplay | Implement | 6.2 | pressure 0, gap 6.2 | `/triage-lead agentplay` |
| terravision | Plan | 6.1 | pressure 0, gap 6.1 | `/triage-lead terravision` |
| claude-show-your-work | Verify | 5.9 | pressure 0, gap 5.9 | `/triage-lead claude-show-your-work` |
| gstack | Implement | 28.2 | pressure 10, gap 6.2 | `/triage-lead gstack` |
| ruflo | Implement | 28.2 | pressure 10, gap 6.2 | `/triage-lead ruflo` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 6 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 15.3 | ships inside `prisma/prisma` · pressure 3, gap 7.3 | `/triage-lead prisma` |
| webapp-testing | Verify | 9.9 | ships inside `anthropics/skills` · pressure 1, gap 5.9 | `/triage-lead webapp-testing` |
| confluence | MCP Servers | 9.3 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.3 | `/triage-lead confluence` |
| jira | MCP Servers | 9.3 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.3 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.7 | ships inside `github/awesome-copilot` · pressure 0, gap 6.7 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.7 | ships inside `getsentry/skills` · pressure 0, gap 6.7 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
