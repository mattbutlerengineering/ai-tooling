# Next evals — a banded promotion queue

The 677 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 116 distinct values across these 677 leads (294 have zero overlap pressure; largest tie: 58) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 207 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 440 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| langfuse | Outer Loop | 43.5 | pressure 18, gap 7.5 | `/evaluate-tool langfuse` |
| sandcastle | Implement | 35.9 | pressure 14, gap 5.9 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.8 | pressure 12, gap 6.8 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 31.8 | pressure 12, gap 5.8 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 31.5 | pressure 11, gap 7.5 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| vet | Review | 65.6 | pressure 28, gap 7.6 | `/evaluate-tool vet` |
| cognee | Memory & Context | 52.8 | pressure 22, gap 6.8 | `/evaluate-tool cognee` |
| mem0 | Memory & Context | 42.8 | pressure 17, gap 6.8 | `/evaluate-tool mem0` |
| orca | Implement | 41.9 | pressure 17, gap 5.9 | `/evaluate-tool orca` |
| aider | Implement | 39.9 | pressure 17, gap 5.9 | `/evaluate-tool aider` |
| OpenHands | Implement | 37.9 | pressure 15, gap 5.9 | `/evaluate-tool OpenHands` |
| gastown | Implement | 37.9 | pressure 15, gap 5.9 | `/evaluate-tool gastown` |
| goose | Implement | 37.9 | pressure 15, gap 5.9 | `/evaluate-tool goose` |
| claude-octopus | Review | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool claude-octopus` |
| ghostsecurity/skills | Review | 37.6 | pressure 14, gap 7.6 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool agentmemory` |
| supermemory | Memory & Context | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool supermemory` |
| browser-use | Verify | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool browser-use` |
| impeccable | Skills & Plugins | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.7 | pressure 12, gap 6.7 | `/evaluate-tool ui-ux-pro-max` |
| worktrunk | Ship | 32.0 | pressure 11, gap 8.0 | `/evaluate-tool worktrunk` |
| ralph-claude-code | Implement | 31.9 | pressure 12, gap 5.9 | `/evaluate-tool ralph-claude-code` |
| claude-code-router | Implement | 29.9 | pressure 11, gap 5.9 | `/evaluate-tool claude-code-router` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 207 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 207 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| engram | Memory & Context | 28.8 | challenges claude-mem · pressure 10, gap 6.8 | `/triage-lead engram` |
| gstack | Implement | 27.9 | challenges GSD · pressure 10, gap 5.9 | `/triage-lead gstack` |
| ruflo | Implement | 27.9 | challenges GSD · pressure 10, gap 5.9 | `/triage-lead ruflo` |
| ACE (agentic-context-engine) | Memory & Context | 26.8 | challenges claude-reflect · pressure 10, gap 6.8 | `/triage-lead ACE (agentic-context-engine)` |
| openskills | Skills & Plugins | 26.7 | challenges skill-creator · pressure 9, gap 6.7 | `/triage-lead openskills` |
| Understand-Anything | Plan | 25.8 | challenges codegraph · pressure 10, gap 5.8 | `/triage-lead Understand-Anything` |
| agnix | Review | 25.6 | challenges SkillSpector · pressure 8, gap 7.6 | `/triage-lead agnix` |
| roundtable | Outer Loop | 25.5 | challenges abtop · pressure 9, gap 7.5 | `/triage-lead roundtable` |
| memU | Memory & Context | 24.8 | challenges claude-mem · pressure 9, gap 6.8 | `/triage-lead memU` |
| compound-engineering | Implement | 23.9 | challenges GSD · pressure 8, gap 5.9 | `/triage-lead compound-engineering` |
| skill-scanner | Review | 23.6 | challenges SkillSpector · pressure 8, gap 7.6 | `/triage-lead skill-scanner` |
| mex | Memory & Context | 22.8 | challenges claude-mem · pressure 8, gap 6.8 | `/triage-lead mex` |

## P3 backlog — 440 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 440 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| CLIProxyAPI | Implement | 25.9 | pressure 10, gap 5.9 | `/triage-lead CLIProxyAPI` |
| gptme | Implement | 25.9 | pressure 9, gap 5.9 | `/triage-lead gptme` |
| qwen-code | Implement | 25.9 | pressure 9, gap 5.9 | `/triage-lead qwen-code` |
| buildwithclaude | Reference | 25.0 | pressure 8, gap 7.0 | `/triage-lead buildwithclaude` |
| scenario | Verify | 24.3 | pressure 8, gap 6.3 | `/triage-lead scenario` |
| deadeye-cc | Implement | 23.9 | pressure 9, gap 5.9 | `/triage-lead deadeye-cc` |
| gemini-cli | Implement | 23.9 | pressure 8, gap 5.9 | `/triage-lead gemini-cli` |
| NeMo-Guardrails | Outer Loop | 23.5 | pressure 8, gap 7.5 | `/triage-lead NeMo-Guardrails` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| slidev | Skills & Plugins | 22.7 | pressure 7, gap 6.7 | `/triage-lead slidev` |
| bifrost | Implement | 21.9 | pressure 7, gap 5.9 | `/triage-lead bifrost` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 5 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 15.1 | ships inside `prisma/prisma` · pressure 3, gap 7.1 | `/triage-lead prisma` |
| confluence | MCP Servers | 9.1 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.1 | `/triage-lead confluence` |
| jira | MCP Servers | 9.1 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 7.1 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.7 | ships inside `github/awesome-copilot` · pressure 0, gap 6.7 | `/triage-lead typescript-mcp-server-generator` |
| presentation-creator | Skills & Plugins | 6.7 | ships inside `getsentry/skills` · pressure 0, gap 6.7 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
