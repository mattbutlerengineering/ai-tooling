# Next evals — a banded promotion queue

The 460 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 103 distinct values across these 460 leads (194 have zero overlap pressure; largest tie: 29) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 139 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 286 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 10 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| cognee | Memory & Context | 44.3 | pressure 18, gap 6.3 | `/evaluate-tool cognee` |
| ECC | Implement | 43.1 | pressure 18, gap 5.1 | `/evaluate-tool ECC` |
| agent-browser | Verify | 42.0 | pressure 17, gap 6.0 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 40.9 | pressure 17, gap 6.9 | `/evaluate-tool langfuse` |
| spec-kit | Plan | 39.5 | pressure 16, gap 5.5 | `/evaluate-tool spec-kit` |
| claude-hud | Plan | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool claude-hud` |
| awesome-claude-code | Reference | 37.0 | pressure 14, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| mem0 | Memory & Context | 36.3 | pressure 14, gap 6.3 | `/evaluate-tool mem0` |
| OpenHands | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool OpenHands` |
| goose | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.9 | pressure 13, gap 6.9 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool supermemory` |
| sandcastle | Implement | 31.1 | pressure 12, gap 5.1 | `/evaluate-tool sandcastle` |
| awesome-agent-skills | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| MemOS | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.9 | pressure 10, gap 6.9 | `/evaluate-tool opik` |
| tdd-guard | Review | 36.0 | pressure 14, gap 6.0 | `/evaluate-tool tdd-guard` |
| orca | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool orca` |
| vet | Review | 34.0 | pressure 13, gap 6.0 | `/evaluate-tool vet` |
| aider | Implement | 33.1 | pressure 14, gap 5.1 | `/evaluate-tool aider` |
| agentmemory | Memory & Context | 32.3 | pressure 12, gap 6.3 | `/evaluate-tool agentmemory` |
| ghostsecurity/skills | Review | 32.0 | pressure 12, gap 6.0 | `/evaluate-tool ghostsecurity/skills` |
| browser-use | Verify | 28.0 | pressure 10, gap 6.0 | `/evaluate-tool browser-use` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 139 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 139 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ralph-claude-code | Implement | 27.1 | challenges GSD · pressure 10, gap 5.1 | `/triage-lead ralph-claude-code` |
| memU | Memory & Context | 26.3 | challenges claude-mem · pressure 9, gap 6.3 | `/triage-lead memU` |
| claude-octopus | Review | 26.0 | challenges code-review · pressure 9, gap 6.0 | `/triage-lead claude-octopus` |
| gstack | Implement | 25.1 | challenges GSD · pressure 9, gap 5.1 | `/triage-lead gstack` |
| ruflo | Implement | 25.1 | challenges GSD · pressure 9, gap 5.1 | `/triage-lead ruflo` |
| ACE (agentic-context-engine) | Memory & Context | 24.3 | challenges claude-reflect · pressure 8, gap 6.3 | `/triage-lead ACE (agentic-context-engine)` |
| engram | Memory & Context | 24.3 | challenges claude-mem · pressure 8, gap 6.3 | `/triage-lead engram` |
| Understand-Anything | Plan | 23.5 | challenges codegraph · pressure 8, gap 5.5 | `/triage-lead Understand-Anything` |
| compound-engineering | Implement | 23.1 | challenges GSD · pressure 8, gap 5.1 | `/triage-lead compound-engineering` |
| gastown | Implement | 23.1 | challenges claude-squad · pressure 8, gap 5.1 | `/triage-lead gastown` |
| garak | Outer Loop | 20.9 | challenges SkillSpector · pressure 6, gap 6.9 | `/triage-lead garak` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |

## P3 backlog — 286 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 286 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ui-ux-pro-max | Skills & Plugins | 26.5 | pressure 9, gap 6.5 | `/triage-lead ui-ux-pro-max` |
| qwen-code | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead qwen-code` |
| worktrunk | Ship | 24.7 | pressure 8, gap 6.7 | `/triage-lead worktrunk` |
| impeccable | Skills & Plugins | 24.5 | pressure 8, gap 6.5 | `/triage-lead impeccable` |
| CLIProxyAPI | Implement | 23.1 | pressure 8, gap 5.1 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.1 | pressure 8, gap 5.1 | `/triage-lead gemini-cli` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| buildwithclaude | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead buildwithclaude` |
| NeMo-Guardrails | Outer Loop | 22.9 | pressure 7, gap 6.9 | `/triage-lead NeMo-Guardrails` |
| slidev | Skills & Plugins | 22.5 | pressure 7, gap 6.5 | `/triage-lead slidev` |
| ccpm | Plan | 21.5 | pressure 7, gap 5.5 | `/triage-lead ccpm` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 10 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 14.7 | ships inside `prisma/prisma` · pressure 3, gap 6.7 | `/triage-lead prisma` |
| plugin-dev | Skills & Plugins | 12.5 | ships inside `anthropics/claude-plugins-official` · pressure 2, gap 6.5 | `/triage-lead plugin-dev` |
| codebase-design | Plan | 9.5 | ships inside `mattpocock/skills` · pressure 1, gap 5.5 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.5 | ships inside `mattpocock/skills` · pressure 1, gap 5.5 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead confluence` |
| jira | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.5 | ships inside `github/awesome-copilot` · pressure 0, gap 6.5 | `/triage-lead typescript-mcp-server-generator` |
| diagnosing-bugs | Verify | 8.0 | ships inside `mattpocock/skills` · pressure 0, gap 6.0 | `/triage-lead diagnosing-bugs` |
| implement | Implement | 7.1 | ships inside `mattpocock/skills` · pressure 0, gap 5.1 | `/triage-lead implement` |
| presentation-creator | Skills & Plugins | 6.5 | ships inside `getsentry/skills` · pressure 0, gap 6.5 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
