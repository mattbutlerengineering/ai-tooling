# Next evals — a banded promotion queue

The 365 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 96 distinct values across these 365 leads (140 have zero overlap pressure; largest tie: 21) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 106 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 234 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 55.1 | pressure 24, gap 5.1 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.2 | pressure 16, gap 6.2 | `/evaluate-tool cognee` |
| agent-browser | Verify | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 36.2 | pressure 15, gap 6.2 | `/evaluate-tool langfuse` |
| ECC | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool ECC` |
| OpenHands | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool OpenHands` |
| goose | Implement | 35.1 | pressure 14, gap 5.1 | `/evaluate-tool goose` |
| supermemory | Memory & Context | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool supermemory` |
| promptfoo | Outer Loop | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool promptfoo` |
| spec-kit | Plan | 33.1 | pressure 13, gap 5.1 | `/evaluate-tool spec-kit` |
| pydantic-ai | Implement | 31.1 | pressure 12, gap 5.1 | `/evaluate-tool pydantic-ai` |
| awesome-claude-code | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool vercel-labs/agent-skills` |
| MemOS | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 28.2 | pressure 10, gap 6.2 | `/evaluate-tool opik` |
| sandcastle | Implement | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool sandcastle` |
| OpenSpec | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool claude-hud` |
| browser-use | Verify | 25.5 | pressure 9, gap 5.5 | `/evaluate-tool browser-use` |
| chrome-devtools-mcp | Verify | 25.5 | pressure 9, gap 5.5 | `/evaluate-tool chrome-devtools-mcp` |
| aider | Implement | 25.1 | pressure 10, gap 5.1 | `/evaluate-tool aider` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 106 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 106 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| gstack | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead gstack` |
| orca | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead orca` |
| ruflo | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead ruflo` |
| ghostsecurity/skills | Review | 25.0 | pressure 9, gap 5.0 | `/triage-lead ghostsecurity/skills` |
| vet | Review | 25.0 | pressure 9, gap 5.0 | `/triage-lead vet` |
| agentmemory | Memory & Context | 24.2 | pressure 8, gap 6.2 | `/triage-lead agentmemory` |
| memU | Memory & Context | 24.2 | pressure 8, gap 6.2 | `/triage-lead memU` |
| gastown | Implement | 23.1 | pressure 8, gap 5.1 | `/triage-lead gastown` |
| Understand-Anything | Plan | 23.1 | pressure 8, gap 5.1 | `/triage-lead Understand-Anything` |
| claude-octopus | Review | 23.0 | pressure 8, gap 5.0 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.0 | pressure 8, gap 5.0 | `/triage-lead tdd-guard` |
| ACE (agentic-context-engine) | Memory & Context | 22.2 | pressure 8, gap 6.2 | `/triage-lead ACE (agentic-context-engine)` |

## P3 backlog — 234 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 234 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| agent-kit | Implement | 25.1 | pressure 9, gap 5.1 | `/triage-lead agent-kit` |
| fast-agent | Implement | 21.1 | pressure 7, gap 5.1 | `/triage-lead fast-agent` |
| claudian | Implement | 13.1 | pressure 3, gap 5.1 | `/triage-lead claudian` |
| codex-plugin-cc | Implement | 13.1 | pressure 3, gap 5.1 | `/triage-lead codex-plugin-cc` |
| nanobot | Implement | 13.1 | pressure 3, gap 5.1 | `/triage-lead nanobot` |
| phantom | Implement | 13.1 | pressure 3, gap 5.1 | `/triage-lead phantom` |
| re_gent | Implement | 13.1 | pressure 3, gap 5.1 | `/triage-lead re_gent` |
| Archon | Implement | 11.1 | pressure 2, gap 5.1 | `/triage-lead Archon` |
| agency-agents | Implement | 11.1 | pressure 2, gap 5.1 | `/triage-lead agency-agents` |
| happy | Implement | 11.1 | pressure 2, gap 5.1 | `/triage-lead happy` |
| cli-continues | Implement | 9.1 | pressure 1, gap 5.1 | `/triage-lead cli-continues` |
| jetbrains-cc-gui | Implement | 9.1 | pressure 1, gap 5.1 | `/triage-lead jetbrains-cc-gui` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
