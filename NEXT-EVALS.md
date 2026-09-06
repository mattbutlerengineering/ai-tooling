# Next evals — a banded promotion queue

The 527 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 108 distinct values across these 527 leads (227 have zero overlap pressure; largest tie: 39) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 154 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 343 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 5 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 44.5 | pressure 18, gap 6.5 | `/evaluate-tool cognee` |
| langfuse | Outer Loop | 40.9 | pressure 17, gap 6.9 | `/evaluate-tool langfuse` |
| OpenHands | Implement | 37.4 | pressure 15, gap 5.4 | `/evaluate-tool OpenHands` |
| goose | Implement | 37.4 | pressure 15, gap 5.4 | `/evaluate-tool goose` |
| mem0 | Memory & Context | 36.5 | pressure 14, gap 6.5 | `/evaluate-tool mem0` |
| supermemory | Memory & Context | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 33.4 | pressure 13, gap 5.4 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool MemOS` |
| awesome-agent-skills | Reference | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 30.9 | pressure 11, gap 6.9 | `/evaluate-tool awesome-agent-skills (libukai)` |
| OpenSpec | Plan | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.9 | pressure 10, gap 6.9 | `/evaluate-tool opik` |
| orca | Implement | 39.4 | pressure 16, gap 5.4 | `/evaluate-tool orca` |
| vet | Review | 38.5 | pressure 15, gap 6.5 | `/evaluate-tool vet` |
| aider | Implement | 37.4 | pressure 16, gap 5.4 | `/evaluate-tool aider` |
| gastown | Implement | 35.4 | pressure 14, gap 5.4 | `/evaluate-tool gastown` |
| ghostsecurity/skills | Review | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool ghostsecurity/skills` |
| agentmemory | Memory & Context | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool agentmemory` |
| impeccable | Skills & Plugins | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool impeccable` |
| ui-ux-pro-max | Skills & Plugins | 32.5 | pressure 12, gap 6.5 | `/evaluate-tool ui-ux-pro-max` |
| ralph-claude-code | Implement | 31.4 | pressure 12, gap 5.4 | `/evaluate-tool ralph-claude-code` |
| worktrunk | Ship | 29.5 | pressure 10, gap 7.5 | `/evaluate-tool worktrunk` |
| browser-use | Verify | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool browser-use` |
| claude-octopus | Review | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool claude-octopus` |
| ACE (agentic-context-engine) | Memory & Context | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool ACE (agentic-context-engine)` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 154 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 154 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| jump-skills | Skills & Plugins | 6.5 | challenges skill-creator · pressure 0, gap 6.5 | `/triage-lead jump-skills` |
| pi-posthorse | Memory & Context | 6.5 | challenges claude-mem · pressure 0, gap 6.5 | `/triage-lead pi-posthorse` |
| timeboxed-execution | Implement | 5.4 | challenges GSD · pressure 0, gap 5.4 | `/triage-lead timeboxed-execution` |
| ruflo | Implement | 27.4 | challenges GSD · pressure 10, gap 5.4 | `/triage-lead ruflo` |
| memU | Memory & Context | 26.5 | challenges claude-mem · pressure 9, gap 6.5 | `/triage-lead memU` |
| gstack | Implement | 25.4 | challenges GSD · pressure 9, gap 5.4 | `/triage-lead gstack` |
| openskills | Skills & Plugins | 24.5 | challenges skill-creator · pressure 8, gap 6.5 | `/triage-lead openskills` |
| engram | Memory & Context | 24.5 | challenges claude-mem · pressure 8, gap 6.5 | `/triage-lead engram` |
| Understand-Anything | Plan | 23.5 | challenges codegraph · pressure 8, gap 5.5 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.4 | challenges GSD · pressure 8, gap 5.4 | `/triage-lead compound-engineering` |
| garak | Outer Loop | 20.9 | challenges SkillSpector · pressure 6, gap 6.9 | `/triage-lead garak` |
| Skill_Seekers | Skills & Plugins | 20.5 | challenges skill-creator · pressure 6, gap 6.5 | `/triage-lead Skill_Seekers` |

## P3 backlog — 343 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 343 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| italia-mcp-servers | Reference | 6.9 | pressure 0, gap 6.9 | `/triage-lead italia-mcp-servers` |
| super-prototyping | Skills & Plugins | 6.5 | pressure 0, gap 6.5 | `/triage-lead super-prototyping` |
| explain-for-dumb | Plan | 5.5 | pressure 0, gap 5.5 | `/triage-lead explain-for-dumb` |
| codex-remote-pro | Implement | 5.4 | pressure 0, gap 5.4 | `/triage-lead codex-remote-pro` |
| mini-harness | Implement | 5.4 | pressure 0, gap 5.4 | `/triage-lead mini-harness` |
| mobilecode | Implement | 5.4 | pressure 0, gap 5.4 | `/triage-lead mobilecode` |
| gptme | Implement | 25.4 | pressure 9, gap 5.4 | `/triage-lead gptme` |
| qwen-code | Implement | 25.4 | pressure 9, gap 5.4 | `/triage-lead qwen-code` |
| NeMo-Guardrails | Outer Loop | 24.9 | pressure 8, gap 6.9 | `/triage-lead NeMo-Guardrails` |
| buildwithclaude | Reference | 24.9 | pressure 8, gap 6.9 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 23.4 | pressure 9, gap 5.4 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.4 | pressure 8, gap 5.4 | `/triage-lead gemini-cli` |

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
