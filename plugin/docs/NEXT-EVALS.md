# Next evals — a banded promotion queue

The 429 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 97 distinct values across these 429 leads (166 have zero overlap pressure; largest tie: 33) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 107 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 297 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 56.8 | pressure 24, gap 6.8 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 41.0 | pressure 16, gap 7.0 | `/evaluate-tool cognee` |
| agent-browser | Verify | 38.4 | pressure 15, gap 6.4 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 37.1 | pressure 15, gap 7.1 | `/evaluate-tool langfuse` |
| ECC | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool ECC` |
| OpenHands | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 35.1 | pressure 13, gap 7.1 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 35.0 | pressure 13, gap 7.0 | `/evaluate-tool supermemory` |
| spec-kit | Plan | 33.6 | pressure 13, gap 5.6 | `/evaluate-tool spec-kit` |
| pydantic-ai | Implement | 32.8 | pressure 12, gap 6.8 | `/evaluate-tool pydantic-ai` |
| MemOS | Memory & Context | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool mem0` |
| awesome-claude-code | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 30.7 | pressure 11, gap 6.7 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 30.7 | pressure 11, gap 6.7 | `/evaluate-tool vercel-labs/agent-skills` |
| opik | Outer Loop | 29.1 | pressure 10, gap 7.1 | `/evaluate-tool opik` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| sandcastle | Implement | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool sandcastle` |
| OpenSpec | Plan | 27.6 | pressure 10, gap 5.6 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 27.6 | pressure 10, gap 5.6 | `/evaluate-tool claude-hud` |
| agent-kit | Implement | 26.8 | pressure 9, gap 6.8 | `/evaluate-tool agent-kit` |
| aider | Implement | 26.8 | pressure 10, gap 6.8 | `/evaluate-tool aider` |
| gstack | Implement | 26.8 | pressure 9, gap 6.8 | `/evaluate-tool gstack` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 107 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 107 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| browser-use | Verify | 26.4 | pressure 9, gap 6.4 | `/triage-lead browser-use` |
| chrome-devtools-mcp | Verify | 26.4 | pressure 9, gap 6.4 | `/triage-lead chrome-devtools-mcp` |
| orca | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead orca` |
| ruflo | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead ruflo` |
| ghostsecurity/skills | Review | 26.4 | pressure 9, gap 6.4 | `/triage-lead ghostsecurity/skills` |
| vet | Review | 26.4 | pressure 9, gap 6.4 | `/triage-lead vet` |
| agentmemory | Memory & Context | 25.0 | pressure 8, gap 7.0 | `/triage-lead agentmemory` |
| memU | Memory & Context | 25.0 | pressure 8, gap 7.0 | `/triage-lead memU` |
| gastown | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead gastown` |
| claude-octopus | Review | 24.4 | pressure 8, gap 6.4 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 24.4 | pressure 8, gap 6.4 | `/triage-lead tdd-guard` |
| Understand-Anything | Plan | 23.6 | pressure 8, gap 5.6 | `/triage-lead Understand-Anything` |

## P3 backlog — 297 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 297 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead qwen-code` |
| CopilotKit | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead CopilotKit` |
| daytona | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead daytona` |
| gemini-cli | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead gemini-cli` |
| voltagent | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead voltagent` |
| ui-ux-pro-max | Skills & Plugins | 24.7 | pressure 8, gap 6.7 | `/triage-lead ui-ux-pro-max` |
| CLIProxyAPI | Implement | 22.8 | pressure 7, gap 6.8 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 22.8 | pressure 7, gap 6.8 | `/triage-lead fast-agent` |
| impeccable | Skills & Plugins | 22.7 | pressure 7, gap 6.7 | `/triage-lead impeccable` |
| slidev | Skills & Plugins | 22.7 | pressure 7, gap 6.7 | `/triage-lead slidev` |
| Helicone | Outer Loop | 21.1 | pressure 6, gap 7.1 | `/triage-lead Helicone` |
| bifrost | Implement | 20.8 | pressure 6, gap 6.8 | `/triage-lead bifrost` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
