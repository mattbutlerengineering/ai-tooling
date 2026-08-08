# Next evals — a banded promotion queue

The 389 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 103 distinct values across these 389 leads (155 have zero overlap pressure; largest tie: 22) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 114 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 239 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 11 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| opencode | Implement | 54.9 | pressure 24, gap 4.9 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 42.3 | pressure 17, gap 6.3 | `/evaluate-tool cognee` |
| ECC | Implement | 36.9 | pressure 15, gap 4.9 | `/evaluate-tool ECC` |
| agent-browser | Verify | 36.8 | pressure 15, gap 4.8 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 36.5 | pressure 15, gap 6.5 | `/evaluate-tool langfuse` |
| spec-kit | Plan | 35.2 | pressure 14, gap 5.2 | `/evaluate-tool spec-kit` |
| OpenHands | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool OpenHands` |
| goose | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool supermemory` |
| claude-hud | Plan | 33.2 | pressure 13, gap 5.2 | `/evaluate-tool claude-hud` |
| awesome-claude-code | Reference | 33.0 | pressure 12, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| mem0 | Memory & Context | 32.3 | pressure 12, gap 6.3 | `/evaluate-tool mem0` |
| sandcastle | Implement | 30.9 | pressure 12, gap 4.9 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 29.2 | pressure 11, gap 5.2 | `/evaluate-tool OpenSpec` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool opik` |
| aider | Implement | 30.9 | pressure 13, gap 4.9 | `/evaluate-tool aider` |
| orca | Implement | 30.9 | pressure 12, gap 4.9 | `/evaluate-tool orca` |
| agentmemory | Memory & Context | 28.3 | pressure 10, gap 6.3 | `/evaluate-tool agentmemory` |
| ui-ux-pro-max | Skills & Plugins | 26.6 | pressure 9, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| ghostsecurity/skills | Review | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool ghostsecurity/skills` |
| vet | Review | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool vet` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 114 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 114 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| awesome-copilot | Reflect | 5.3 | challenges agent-skills, code-review, documentation-and-adrs, feature-dev, pr-review-toolkit · pressure 1, gap 3.3 | `/triage-lead awesome-copilot` |
| gstack | Implement | 24.9 | challenges GSD · pressure 9, gap 4.9 | `/triage-lead gstack` |
| ruflo | Implement | 24.9 | challenges GSD · pressure 9, gap 4.9 | `/triage-lead ruflo` |
| browser-use | Verify | 24.8 | challenges playwright · pressure 9, gap 4.8 | `/triage-lead browser-use` |
| ACE (agentic-context-engine) | Memory & Context | 24.3 | challenges claude-reflect · pressure 8, gap 6.3 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 24.3 | challenges claude-mem · pressure 8, gap 6.3 | `/triage-lead memU` |
| Understand-Anything | Plan | 23.2 | challenges codegraph · pressure 8, gap 5.2 | `/triage-lead Understand-Anything` |
| claude-octopus | Review | 23.2 | challenges code-review · pressure 8, gap 5.2 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.2 | challenges GSD, pr-review-toolkit, stryker-js · pressure 8, gap 5.2 | `/triage-lead tdd-guard` |
| gastown | Implement | 22.9 | challenges claude-squad · pressure 8, gap 4.9 | `/triage-lead gastown` |
| compound-engineering | Implement | 20.9 | challenges GSD · pressure 7, gap 4.9 | `/triage-lead compound-engineering` |
| ralph-claude-code | Implement | 20.9 | challenges GSD · pressure 7, gap 4.9 | `/triage-lead ralph-claude-code` |

## P3 backlog — 239 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 239 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| qwen-code | Implement | 24.9 | pressure 9, gap 4.9 | `/triage-lead qwen-code` |
| impeccable | Skills & Plugins | 24.6 | pressure 8, gap 6.6 | `/triage-lead impeccable` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| gemini-cli | Implement | 22.9 | pressure 8, gap 4.9 | `/triage-lead gemini-cli` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| ccpm | Plan | 21.2 | pressure 7, gap 5.2 | `/triage-lead ccpm` |
| buildwithclaude | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead fast-agent` |
| worktrunk | Ship | 20.7 | pressure 6, gap 6.7 | `/triage-lead worktrunk` |
| google/skills | Skills & Plugins | 20.6 | pressure 6, gap 6.6 | `/triage-lead google/skills` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 11 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| frontend-design | Skills & Plugins | 12.6 | pressure 3, gap 6.6 | `/triage-lead frontend-design` |
| prisma | MCP Servers | 12.6 | pressure 2, gap 6.6 | `/triage-lead prisma` |
| plugin-dev | Skills & Plugins | 12.6 | pressure 2, gap 6.6 | `/triage-lead plugin-dev` |
| codebase-design | Plan | 9.2 | pressure 1, gap 5.2 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.2 | pressure 1, gap 5.2 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.6 | pressure 0, gap 6.6 | `/triage-lead confluence` |
| jira | MCP Servers | 8.6 | pressure 0, gap 6.6 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| implement | Implement | 6.9 | pressure 0, gap 4.9 | `/triage-lead implement` |
| diagnosing-bugs | Verify | 6.8 | pressure 0, gap 4.8 | `/triage-lead diagnosing-bugs` |
| presentation-creator | Skills & Plugins | 6.6 | pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
