# Next evals — a banded promotion queue

The 428 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 104 distinct values across these 428 leads (178 have zero overlap pressure; largest tie: 26) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 128 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 265 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 10 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| opencode | Implement | 57.1 | pressure 25, gap 5.1 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 42.2 | pressure 17, gap 6.2 | `/evaluate-tool cognee` |
| agent-browser | Verify | 41.4 | pressure 17, gap 5.4 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 40.8 | pressure 17, gap 6.8 | `/evaluate-tool langfuse` |
| ECC | Implement | 39.1 | pressure 16, gap 5.1 | `/evaluate-tool ECC` |
| claude-hud | Plan | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool claude-hud` |
| spec-kit | Plan | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 37.1 | pressure 14, gap 7.1 | `/evaluate-tool awesome-claude-code` |
| OpenHands | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool OpenHands` |
| goose | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.8 | pressure 13, gap 6.8 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool supermemory` |
| mem0 | Memory & Context | 32.2 | pressure 12, gap 6.2 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 31.1 | pressure 11, gap 7.1 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 31.1 | pressure 11, gap 7.1 | `/evaluate-tool awesome-agent-skills (libukai)` |
| sandcastle | Implement | 31.1 | pressure 12, gap 5.1 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 29.5 | pressure 11, gap 5.5 | `/evaluate-tool OpenSpec` |
| opik | Outer Loop | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool opik` |
| aider | Implement | 33.1 | pressure 14, gap 5.1 | `/evaluate-tool aider` |
| orca | Implement | 33.1 | pressure 13, gap 5.1 | `/evaluate-tool orca` |
| agentmemory | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool agentmemory` |
| ghostsecurity/skills | Review | 29.4 | pressure 11, gap 5.4 | `/evaluate-tool ghostsecurity/skills` |
| tdd-guard | Review | 27.4 | pressure 10, gap 5.4 | `/evaluate-tool tdd-guard` |
| vet | Review | 27.4 | pressure 10, gap 5.4 | `/evaluate-tool vet` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 128 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 128 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| browser-use | Verify | 27.4 | challenges playwright · pressure 10, gap 5.4 | `/triage-lead browser-use` |
| gstack | Implement | 25.1 | challenges GSD · pressure 9, gap 5.1 | `/triage-lead gstack` |
| ralph-claude-code | Implement | 25.1 | challenges GSD · pressure 9, gap 5.1 | `/triage-lead ralph-claude-code` |
| ruflo | Implement | 25.1 | challenges GSD · pressure 9, gap 5.1 | `/triage-lead ruflo` |
| ACE (agentic-context-engine) | Memory & Context | 24.2 | challenges claude-reflect · pressure 8, gap 6.2 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 24.2 | challenges claude-mem · pressure 8, gap 6.2 | `/triage-lead memU` |
| Understand-Anything | Plan | 23.5 | challenges codegraph · pressure 8, gap 5.5 | `/triage-lead Understand-Anything` |
| claude-octopus | Review | 23.4 | challenges code-review · pressure 8, gap 5.4 | `/triage-lead claude-octopus` |
| compound-engineering | Implement | 23.1 | challenges GSD · pressure 8, gap 5.1 | `/triage-lead compound-engineering` |
| gastown | Implement | 23.1 | challenges claude-squad · pressure 8, gap 5.1 | `/triage-lead gastown` |
| garak | Outer Loop | 20.8 | challenges SkillSpector · pressure 6, gap 6.8 | `/triage-lead garak` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |

## P3 backlog — 265 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 265 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| ui-ux-pro-max | Skills & Plugins | 26.5 | pressure 9, gap 6.5 | `/triage-lead ui-ux-pro-max` |
| qwen-code | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead qwen-code` |
| impeccable | Skills & Plugins | 24.5 | pressure 8, gap 6.5 | `/triage-lead impeccable` |
| ag-ui | Reference | 23.1 | pressure 7, gap 7.1 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.1 | pressure 7, gap 7.1 | `/triage-lead awesome-claude-skills (Composio)` |
| buildwithclaude | Reference | 23.1 | pressure 7, gap 7.1 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 23.1 | pressure 8, gap 5.1 | `/triage-lead CLIProxyAPI` |
| gemini-cli | Implement | 23.1 | pressure 8, gap 5.1 | `/triage-lead gemini-cli` |
| NeMo-Guardrails | Outer Loop | 22.8 | pressure 7, gap 6.8 | `/triage-lead NeMo-Guardrails` |
| worktrunk | Ship | 22.7 | pressure 7, gap 6.7 | `/triage-lead worktrunk` |
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
| diagnosing-bugs | Verify | 7.4 | ships inside `mattpocock/skills` · pressure 0, gap 5.4 | `/triage-lead diagnosing-bugs` |
| implement | Implement | 7.1 | ships inside `mattpocock/skills` · pressure 0, gap 5.1 | `/triage-lead implement` |
| presentation-creator | Skills & Plugins | 6.5 | ships inside `getsentry/skills` · pressure 0, gap 6.5 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
