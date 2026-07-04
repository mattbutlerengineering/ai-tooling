# Evaluation: agmsg

**Repo:** [fujibee/agmsg](https://github.com/fujibee/agmsg)
**Stars:** 757 | **Last updated:** 2026-06-19 (pushed; created 2026-04-02) | **License:** MIT | **Requires:** `bash` + `sqlite3`
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Agent Orchestration (peer-to-peer messaging across CLI agents)
**Layer:** Tooling (a shared local SQLite file + a skill/command per agent)

---

## What it does

agmsg is **cross-agent messaging for CLI AI agents** — Claude Code, Codex, Gemini CLI, GitHub Copilot CLI, and other CLI agents **message each other directly** through a shared local SQLite database, "no human in the middle." It deliberately avoids infrastructure: no daemon, no network, no MCP, no broker — just `bash` + `sqlite3`, where "the SQLite file is the floor; agents are the players." It was #5 Product of the Day on Product Hunt.

It's explicit about what it is *not*:
- **Not MCP** — no MCP server, no extra runtime.
- **Not subagents** — it connects *peer* sessions across different tools; `spawn` can launch a new peer in its own terminal, but that peer is an independent session you talk to, not a managed child process.
- **Not a message queue** — no broker.

The demo: two `monitor`-mode Claude Code instances play tic-tac-toe against each other with no human; in real use, Claude Code asks Codex for a code review and gets it back — all over agmsg.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No agents wired together, no messages exchanged. Behavior comes from the README and metadata, not observed runs.

```bash
gh api repos/fujibee/agmsg --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 757, MIT
gh api repos/fujibee/agmsg/readme --jq '.content' | base64 -d | head -40   # SQLite-as-bus, peer (not subagent), not-MCP framing
```

## What worked

- **Radically simple transport.** Using a local SQLite file as the message bus (no daemon/network/broker) is elegant and dependency-light — `bash` + `sqlite3` is on most dev machines.
- **Cross-*vendor* peer messaging is the novel bit.** Most coordination tools are within one harness; agmsg lets Claude Code, Codex, Gemini, and Copilot talk *to each other* as peers — useful for "ask the other model for a review" patterns.
- **Honest scoping.** Clearly distinguishing peer-messaging from subagents, MCP, and queues sets correct expectations.
- **MIT, actively pushed, real traction** (Product Hunt, ~757 stars).

## What didn't work or surprised us

- **You're wiring up autonomy.** Agents messaging each other with no human in the loop is powerful and risky — loops, runaway exchanges, or one agent acting on another's unverified output need guardrails the tool doesn't impose.
- **SQLite-as-bus has limits.** Fine locally; not built for distributed, high-throughput, or untrusted-peer scenarios (and it isn't trying to be).
- **Coordination semantics are thin.** It's a transport, not a protocol — who owns what, ordering, and conflict handling are up to the agents/teams you define (compare beads/guild, which model the *work*, not just the channel).
- **Young, single-author.** Promising but early.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Cross-model peer review ("Claude asks Codex to review") can catch issues; unmonitored exchanges can also propagate errors. |
| Speed | + | Removes the human copy-paste courier between agents/tools. |
| Maintainability | neutral | Tiny footprint (SQLite + skill); but multi-agent autonomy adds operational complexity to reason about. |
| Safety | − | Peer agents acting on each other's messages without a human is a real autonomy/blast-radius surface. |
| Cost Efficiency | neutral | Negligible infra; token cost scales with how chatty the agents are. |

## Verdict

**CONDITIONAL** — agmsg is a clever, MIT, near-zero-infrastructure way to let **CLI agents from different vendors message each other as peers** through a shared local SQLite file — no daemon, no MCP, no broker. Adopt it for cross-model collaboration patterns (e.g. Claude Code asking Codex for a review, or splitting work across peer sessions) where you want them to coordinate without you as the courier. Treat the autonomy seriously: keep a human checkpoint or `monitor` mode on important exchanges, since peer agents acting on each other's unverified output is the main risk. It's a transport, not a work-coordination model — pair with beads/guild if you need to track the *work* itself.

Compared to neighbors: **beads** is a work-coordination ledger; **guild** shares context/memory/task coordination across agents. agmsg's distinguishing pitch is the **cross-vendor peer message channel itself** — the dumb-simple SQLite bus that lets different CLI agents talk directly.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agmsg](https://github.com/fujibee/agmsg) | tool | Cross-vendor peer messaging for CLI AI agents (MIT) — Claude Code, Codex, Gemini, Copilot message each other directly via a shared local SQLite file; no daemon/network/MCP/broker (`bash` + `sqlite3`) | You're the copy-paste courier between agents; want different CLI agents to coordinate directly as peers | beads, guild |
