# Evaluation: beads (bd)

**Repo:** [gastownhall/beads](https://github.com/gastownhall/beads)
**Stars:** 24,648 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Plan + Implement (also Reflect — persistent project memory)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Memory upgrade for coding agents." Beads is a git-backed issue ledger exposed as the `bd` CLI, designed as durable shared state for one or more coding agents. Each issue is a row in a local SQLite database (committed alongside the repo) carrying priority, status, dependencies, and an audit trail. The point is that an agent fleet — or a single agent across many sessions — never re-derives "what's left to do" or "what did we decide": work and decisions persist outside the context window.

Two mechanisms do the heavy lifting. First, a **dependency-aware ready queue**: `bd ready` returns only issues with no *open* blockers, so an agent that asks "what can I work on now?" never picks up work that is transitively blocked. Closing a blocker automatically promotes its dependents. Second, a **persistent memory** layer: `bd remember "insight"` stores keyed project memories that `bd prime` re-injects into agent context later, replacing ad-hoc `MEMORY.md` files.

The CLI is installed once system-wide (`@beads/bd` on npm, or a curl install script) and used across projects. `bd init` (or `bd init --stealth` for local-only, uncommitted use) sets up the ledger; `bd setup claude|codex|factory` wires agent integrations.

## How we tested it

**Evidence:** MEASURED

Installed the real CLI (`npm install -g @beads/bd`, v1.0.5) and ran it hands-on in a throwaway git repo, exercising the dependency-aware ready queue — the core claim — plus the memory feature. Created three tasks with a linear dependency chain (Build API depends on Design schema; Write tests depends on Build API) and verified that `bd ready` correctly excludes transitively blocked work, then that closing a blocker promotes exactly the next task.

```
npm install -g @beads/bd            # CLI = bd, NOT the bare `beads` npm package (that is unrelated)
bd init --stealth                   # local ledger, nothing committed
A=$(bd create "Design schema" -p 0 --json | jq -r .id)
B=$(bd create "Build API"     -p 1 --json | jq -r .id)
C=$(bd create "Write tests"   -p 1 --json | jq -r .id)
bd dep add "$B" "$A"                # B blocked by A
bd dep add "$C" "$B"                # C blocked by B
bd ready                            # => ONLY A (1 issue); B,C correctly hidden as blocked
bd update "$A" --claim && bd close "$A"
bd ready                            # => ONLY B (C still blocked because B is open)
bd remember "Schema uses UUID primary keys, not autoincrement"
bd prime                            # => re-injects the stored memory under "Persistent Memories (1)"
```

Observed results matched expectations exactly. `bd stats` after the run reported: Total 3, Open 2, Blocked 1, Closed 1, **Ready to Work: 1** — confirming the queue's blocker math rather than just trusting the list output.

## What worked

- **The dependency-aware ready queue is correct and is the real value.** With a linear A→B→C block chain, `bd ready` returned exactly one actionable task at each step, and closing A promoted B (not C). This is precisely the "don't pick up blocked/duplicate work" guarantee a fleet needs, and it held under test.
- **`--json` on `create` gives clean, scriptable IDs** — essential for wiring dependencies in a script or from an agent without parsing human-formatted output.
- **`remember`/`prime` round-trips persistent memory** with no extra setup — stored insight came back verbatim under "Persistent Memories" in `bd prime`, keyed for in-place update (`bd remember --key`) and removal (`bd forget`).
- **`--stealth` is a genuinely useful mode**: a local-only ledger that commits nothing, so you can trial it on a shared repo without touching tracked files.

## What didn't work or surprised us

- **The STACK install command was wrong and dangerous.** The catalog said `npm install -g beads`, but the bare `beads` npm package is an unrelated project (zenozeng/beads); the real CLI publishes as **`@beads/bd`**. Following the old instruction would silently install the wrong tool. Fixed in STACK.md as part of this evaluation.
- **Issue ID prefix is derived from the directory name**, not a fixed `bd-` — e.g. a repo at `/tmp/tmp.MNX…` produced IDs like `tmp_MNXhfloBmt-b3a`. Fine in a real project (you get a readable prefix), but it means you cannot hardcode an ID format; always capture IDs from `--json`.
- **Human-readable `create` output does not print a greppable canonical ID** in a stable place — the first attempt to scrape IDs with a regex failed. Use `--json`, not text scraping.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `bd ready` provably excludes transitively blocked work, so agents act only on genuinely actionable tasks. |
| Speed | + | One `bd ready` call replaces re-reading state to recompute what's unblocked; closing a blocker auto-promotes dependents. |
| Maintainability | + | Work + decisions persist in a git-backed ledger and `bd remember`, surviving context resets and session boundaries. |
| Safety | neutral | Local SQLite + git; no network. Stealth mode avoids committing state to shared repos. |
| Cost Efficiency | + | `bd prime` re-injects only stored memories instead of re-deriving project state from scratch each session. |

## Verdict

**ADOPT** (for multi-agent or long-horizon single-agent work)

The dependency-aware ready queue does what it claims under test, and the memory layer round-trips cleanly with zero ceremony. The one caveat is install: use `npm install -g @beads/bd` (CLI is `bd`), never the bare `beads` package. For a single short task in one session it's overkill; its payoff is fleets and work that spans many sessions, where "what's actually ready?" and "what did we already decide?" are the expensive questions.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [beads](https://github.com/gastownhall/beads) | tool | Git-backed issue ledger (`bd` CLI) with a dependency-aware ready queue and persistent agent memory | Default agent memory is too shallow or ephemeral; fleets pick up blocked or duplicate work | OMEGA, agentmemory, claude-mem |
