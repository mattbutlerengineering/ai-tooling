# Next evals — a banded promotion queue

The 466 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 101 distinct values across these 466 leads (201 have zero overlap pressure; largest tie: 32) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 136 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 295 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 10 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 44.3 | pressure 18, gap 6.3 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 40.8 | pressure 17, gap 6.8 | `/evaluate-tool langfuse` |
| mem0 | Memory & Context | 36.3 | pressure 14, gap 6.3 | `/evaluate-tool mem0` |
| OpenHands | Implement | 35.2 | pressure 14, gap 5.2 | `/evaluate-tool OpenHands` |
| goose | Implement | 35.2 | pressure 14, gap 5.2 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 31.2 | pressure 12, gap 5.2 | `/evaluate-tool sandcastle` |
| awesome-agent-skills | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.8 | pressure 11, gap 6.8 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 29.3 | pressure 11, gap 5.3 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool opik` |
| orca | Implement | 37.2 | pressure 15, gap 5.2 | `/evaluate-tool orca` |
| vet | Review | 36.1 | pressure 14, gap 6.1 | `/evaluate-tool vet` |
| aider | Implement | 35.2 | pressure 15, gap 5.2 | `/evaluate-tool aider` |
| agentmemory | Memory & Context | 32.3 | pressure 12, gap 6.3 | `/evaluate-tool agentmemory` |
| ghostsecurity/skills | Review | 32.1 | pressure 12, gap 6.1 | `/evaluate-tool ghostsecurity/skills` |
| ui-ux-pro-max | Skills & Plugins | 30.6 | pressure 11, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| impeccable | Skills & Plugins | 28.6 | pressure 10, gap 6.6 | `/evaluate-tool impeccable` |
| claude-octopus | Review | 28.1 | pressure 10, gap 6.1 | `/evaluate-tool claude-octopus` |
| browser-use | Verify | 27.7 | pressure 10, gap 5.7 | `/evaluate-tool browser-use` |
| ralph-claude-code | Implement | 27.2 | pressure 10, gap 5.2 | `/evaluate-tool ralph-claude-code` |
| memU | Memory & Context | 26.3 | pressure 9, gap 6.3 | `/evaluate-tool memU` |
| gastown | Implement | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool gastown` |
| gstack | Implement | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool gstack` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 136 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 136 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ruflo | Implement | 25.2 | challenges GSD · pressure 9, gap 5.2 | `/triage-lead ruflo` |
| ACE (agentic-context-engine) | Memory & Context | 24.3 | challenges claude-reflect · pressure 8, gap 6.3 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 24.3 | challenges claude-mem · pressure 8, gap 6.3 | `/triage-lead engram` |
| Understand-Anything | Plan | 23.3 | challenges codegraph · pressure 8, gap 5.3 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.2 | challenges GSD · pressure 8, gap 5.2 | `/triage-lead compound-engineering` |
| garak | Outer Loop | 20.8 | challenges SkillSpector · pressure 6, gap 6.8 | `/triage-lead garak` |
| andrej-karpathy-skills | Skills & Plugins | 20.6 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.6 | `/triage-lead andrej-karpathy-skills` |
| openskills | Skills & Plugins | 20.6 | challenges skill-creator · pressure 6, gap 6.6 | `/triage-lead openskills` |
| strands-agents (harness-sdk) | Implement | 19.2 | challenges fastmcp · pressure 6, gap 5.2 | `/triage-lead strands-agents (harness-sdk)` |
| mcp-use | MCP Servers | 18.7 | challenges fastmcp · pressure 5, gap 6.7 | `/triage-lead mcp-use` |
| Skill_Seekers | Skills & Plugins | 18.6 | challenges skill-creator · pressure 5, gap 6.6 | `/triage-lead Skill_Seekers` |
| SocratiCode | Plan | 17.3 | challenges codegraph · pressure 5, gap 5.3 | `/triage-lead SocratiCode` |

## P3 backlog — 295 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 295 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| qwen-code | Implement | 25.2 | pressure 9, gap 5.2 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 24.8 | pressure 8, gap 6.8 | `/triage-lead NeMo-Guardrails` |
| worktrunk | Ship | 24.7 | pressure 8, gap 6.7 | `/triage-lead worktrunk` |
| CLIProxyAPI | Implement | 23.2 | pressure 8, gap 5.2 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.2 | pressure 8, gap 5.2 | `/triage-lead gemini-cli` |
| gptme | Implement | 23.2 | pressure 8, gap 5.2 | `/triage-lead gptme` |
| ag-ui | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead awesome-claude-skills (Composio)` |
| buildwithclaude | Reference | 22.8 | pressure 7, gap 6.8 | `/triage-lead buildwithclaude` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| ccpm | Plan | 21.3 | pressure 7, gap 5.3 | `/triage-lead ccpm` |
| fast-agent | Implement | 21.2 | pressure 7, gap 5.2 | `/triage-lead fast-agent` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 10 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 14.7 | ships inside `prisma/prisma` · pressure 3, gap 6.7 | `/triage-lead prisma` |
| plugin-dev | Skills & Plugins | 12.6 | ships inside `anthropics/claude-plugins-official` · pressure 2, gap 6.6 | `/triage-lead plugin-dev` |
| codebase-design | Plan | 9.3 | ships inside `mattpocock/skills` · pressure 1, gap 5.3 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.3 | ships inside `mattpocock/skills` · pressure 1, gap 5.3 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead confluence` |
| jira | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | ships inside `github/awesome-copilot` · pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| diagnosing-bugs | Verify | 7.7 | ships inside `mattpocock/skills` · pressure 0, gap 5.7 | `/triage-lead diagnosing-bugs` |
| implement | Implement | 7.2 | ships inside `mattpocock/skills` · pressure 0, gap 5.2 | `/triage-lead implement` |
| presentation-creator | Skills & Plugins | 6.6 | ships inside `getsentry/skills` · pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
