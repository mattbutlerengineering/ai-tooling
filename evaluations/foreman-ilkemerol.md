# Evaluation: foreman (ilkemerol)

**Repo:** [ilkemerol/foreman](https://github.com/ilkemerol/foreman)
**Stars:** 36 | **Last updated:** 2026-11-04 (pushed) | **License:** MIT
**Last verified:** 2026-11-07
**Last triaged:** 2026-11-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Orchestrator mode (MIT) for Claude Code where the main session plans and delegates
work to subagents, rather than the user manually deciding and dispatching each piece.

Note: this is a different tool from the catalog's existing `Foreman` entry
([Turki-Sh/Foreman](https://github.com/Turki-Sh/Foreman), a website-build playbook
plugin) — same display word, unrelated repos and unrelated jobs. Disambiguated here
by author handle per the catalog's existing convention for name collisions (e.g.
`AgentMemory (hsuanshao)`, `claude-code-mods (hamzafer)`).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to check it
against the STACK incumbent it cites, not to support an ADOPT.

## Triage note

P2 challenger — cites STACK pick `claude-squad` in "Overlaps with". Left at
discovery-log rather than SKIPped: `claude-squad` manages several separate AI terminal
agent *processes* in parallel, while `foreman (ilkemerol)` is a single Claude Code
session's main agent planning and delegating to its own subagents — a different
delegation mechanism (intra-session vs multi-process), not a clear duplicate. Left for
a real hands-on eval rather than a mechanical SKIP.
