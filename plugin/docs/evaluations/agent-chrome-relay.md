# Evaluation: agent-chrome-relay

**Repo:** [aindeev/agent-chrome-relay](https://github.com/aindeev/agent-chrome-relay)
**Stars:** 251 | **Last updated:** 2026-10-11 (pushed) | **License:** MIT
**Last verified:** 2026-10-11
**Last triaged:** 2026-10-11  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A CLI that lets coding agents such as Claude Code, Codex, and Cursor drive the user's
everyday, already-signed-in Chrome from the command line in background tabs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata and a README skim. No catalogued STACK pick resolves from this row's
"Overlaps with" cell, so this is not a P2 redundancy call — see Triage note.

## Catalog entry

| [agent-chrome-relay](https://github.com/aindeev/agent-chrome-relay) | tool | CLI (MIT) letting Claude Code, Codex, and Cursor drive your signed-in Chrome in background tabs | Agents need an authenticated browser session for testing or data tasks but can't reuse your own logged-in Chrome | web-access, agent-browser, opencli |  |

## Triage note

Left at `discovery-log`: a logged-in-browser relay with moderate traction (251 stars)
and real overlap with `web-access`/`agent-browser`/`opencli`, none of which is an
adopted STACK pick, so there is no incumbent to call this redundant against. Worth a
real look if authenticated-browser automation becomes a priority; left for the
P0/eval-runner lane rather than mechanically SKIPped.

_Triaged 2026-10-11 by the P3 backlog band._
