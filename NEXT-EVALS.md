# Next evals — a banded promotion queue

The 369 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 99 distinct values across these 369 leads (143 have zero overlap pressure; largest tie: 22) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 105 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 227 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 12 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 54.8 | pressure 24, gap 4.8 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.3 | pressure 16, gap 6.3 | `/evaluate-tool cognee` |
| agent-browser | Verify | 36.8 | pressure 15, gap 4.8 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 36.4 | pressure 15, gap 6.4 | `/evaluate-tool langfuse` |
| ECC | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool ECC` |
| OpenHands | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.4 | pressure 13, gap 6.4 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool supermemory` |
| spec-kit | Plan | 33.1 | pressure 13, gap 5.1 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 30.6 | pressure 11, gap 6.6 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 30.6 | pressure 11, gap 6.6 | `/evaluate-tool vercel-labs/agent-skills` |
| MemOS | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 28.4 | pressure 10, gap 6.4 | `/evaluate-tool opik` |
| OpenSpec | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool claude-hud` |
| sandcastle | Implement | 26.8 | pressure 10, gap 4.8 | `/evaluate-tool sandcastle` |
| orca | Implement | 28.8 | pressure 11, gap 4.8 | `/evaluate-tool orca` |
| ui-ux-pro-max | Skills & Plugins | 26.6 | pressure 9, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| ghostsecurity/skills | Review | 25.1 | pressure 9, gap 5.1 | `/evaluate-tool ghostsecurity/skills` |
| vet | Review | 25.1 | pressure 9, gap 5.1 | `/evaluate-tool vet` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 105 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 105 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| browser-use | Verify | 24.8 | pressure 9, gap 4.8 | `/triage-lead browser-use` |
| aider | Implement | 24.8 | pressure 10, gap 4.8 | `/triage-lead aider` |
| gstack | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead gstack` |
| ruflo | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead ruflo` |
| agentmemory | Memory & Context | 24.3 | pressure 8, gap 6.3 | `/triage-lead agentmemory` |
| memU | Memory & Context | 24.3 | pressure 8, gap 6.3 | `/triage-lead memU` |
| claude-octopus | Review | 23.1 | pressure 8, gap 5.1 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.1 | pressure 8, gap 5.1 | `/triage-lead tdd-guard` |
| Understand-Anything | Plan | 23.1 | pressure 8, gap 5.1 | `/triage-lead Understand-Anything` |
| gastown | Implement | 22.8 | pressure 8, gap 4.8 | `/triage-lead gastown` |
| ACE (agentic-context-engine) | Memory & Context | 22.3 | pressure 8, gap 6.3 | `/triage-lead ACE (agentic-context-engine)` |
| compound-engineering | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead compound-engineering` |

## P3 backlog — 227 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 227 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead qwen-code` |
| impeccable | Skills & Plugins | 24.6 | pressure 8, gap 6.6 | `/triage-lead impeccable` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| gemini-cli | Implement | 22.8 | pressure 8, gap 4.8 | `/triage-lead gemini-cli` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| ag-ui | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead ag-ui` |
| buildwithclaude | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead fast-agent` |
| worktrunk | Ship | 20.7 | pressure 6, gap 6.7 | `/triage-lead worktrunk` |
| google/skills | Skills & Plugins | 20.6 | pressure 6, gap 6.6 | `/triage-lead google/skills` |
| open-slide | Skills & Plugins | 20.6 | pressure 6, gap 6.6 | `/triage-lead open-slide` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 12 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| frontend-design | Skills & Plugins | 12.6 | pressure 3, gap 6.6 | `/triage-lead frontend-design` |
| prisma | MCP Servers | 10.6 | pressure 2, gap 6.6 | `/triage-lead prisma` |
| plugin-dev | Skills & Plugins | 10.6 | pressure 1, gap 6.6 | `/triage-lead plugin-dev` |
| server-memory | Memory & Context | 10.3 | pressure 1, gap 6.3 | `/triage-lead server-memory` |
| codebase-design | Plan | 9.1 | pressure 1, gap 5.1 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.1 | pressure 1, gap 5.1 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.6 | pressure 0, gap 6.6 | `/triage-lead confluence` |
| jira | MCP Servers | 8.6 | pressure 0, gap 6.6 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| implement | Implement | 6.8 | pressure 0, gap 4.8 | `/triage-lead implement` |
| diagnosing-bugs | Verify | 6.8 | pressure 0, gap 4.8 | `/triage-lead diagnosing-bugs` |
| presentation-creator | Skills & Plugins | 6.6 | pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
