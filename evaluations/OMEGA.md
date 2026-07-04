# Evaluation: OMEGA

**Repo:** _none public_ (proprietary MCP server; no public GitHub repository to inspect)
**Stars:** n/a | **Last updated:** n/a | **License:** proprietary / freemium (✓/$)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect (cross-session continuity) — a memory/coordination layer that spans the whole loop rather than sitting in one stage
**Layer:** Infrastructure (MCP server providing persistent memory + coordination tools)

---

## What it does

The catalog one-liner: "Persistent cross-session memory with semantic search, knowledge graphs, and coordination." OMEGA is an MCP server that gives an agent durable memory across conversations. Its tool surface (as exercised in normal sessions) includes `omega_welcome` (start-of-session context briefing), `omega_protocol` (operating instructions the agent follows), `omega_store` (save decisions/lessons/preferences with a type tag), `omega_query` (retrieve prior context before a task), `omega_checkpoint` (snapshot state when context fills), `omega_profile` (load user context), `omega_reflect` (review prior thinking on a topic before architecture decisions), and `omega_memory`/`omega_call` for graph linking and arbitrary tool dispatch. Hooks surface `[MEMORY]`/`[HANDOFF]`/`[COORD]` blocks into the session as ground-truth context.

The mechanism is a persistent store (semantic search + a knowledge graph of linked memories) fronted by MCP tools, plus a session lifecycle protocol that instructs the agent to brief at start, store decisions after tasks, and checkpoint when context runs low. It is positioned as the always-on memory substrate for a multi-session workflow.

## How we tested it

**Evidence:** REVIEW

**Incumbent assessment — not source-inspectable, no hands-on benchmark in this evaluation.** OMEGA has **no public repository**, so the source-grounded GitHub inspection used for every other catalog entry is impossible here — there is no README, file tree, license, commit history, or star count to examine. This evaluation is therefore an honest *incumbent* assessment based on (a) the catalog description, (b) the documented tool/protocol surface, and (c) the fact that it is the operator's installed, mandated memory system in active daily use. No independent benchmark of recall quality, latency, or correctness was run, and none of OMEGA's self-reported capabilities (semantic search quality, graph reasoning) were verified against a baseline.

```
# No gh commands apply — there is no public repo.
# Assessed from: catalog entry, MCP tool surface, and operator's active usage.
```

## What worked

- **Fills a real, persistent gap.** Cross-session amnesia is the single biggest structural weakness of stateful agent work; a durable memory + briefing/checkpoint protocol directly addresses it, which is why it's wired in as always-on.
- **Lifecycle protocol, not just a store.** The welcome → query → store → checkpoint loop is an opinionated discipline that makes the memory actually get used, rather than a passive KV store the agent forgets to write to.
- **Coordination surface.** `[MEMORY]`/`[HANDOFF]`/`[COORD]` blocks and a query-before-subagent pattern give it a role in multi-agent / multi-session handoffs, not just single-thread recall.
- **In active production use.** As the operator's mandated system it has the strongest possible adoption signal in this catalog — it is relied on every session.

## What didn't work or surprised us

- **No public repo = unverifiable and unauditable.** There is nothing to inspect: no source, no license terms beyond "freemium," no security posture, no release cadence. Every capability claim (semantic search, knowledge-graph reasoning) is taken on trust. This is the single biggest mark against it for anyone outside the operator's setup.
- **Lock-in.** Memory accreted in a proprietary store with no documented export is a switching cost that compounds over time; the data has gravity and the format isn't open.
- **Protocol overhead.** The mandated welcome/protocol/store/checkpoint calls spend tokens and turns every session; valuable when memory pays off, pure overhead on short or stateless tasks.
- **Not reproducible for readers.** Unlike `server-memory` (open reference) or `claude-mem` (inspectable), a reader of this catalog cannot adopt, fork, or even read OMEGA — so its catalog value is mostly as a *pattern reference* (what a good memory layer looks like) rather than an installable recommendation.
- **Trust boundary.** An always-on server that ingests decisions, preferences, and project context across all sessions is a meaningful data-flow surface; with no published security model, that has to be accepted on faith.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / unverified | Recalling prior decisions and constraints reduces re-litigation and contradiction across sessions — but recall quality is not independently benchmarked here. |
| Speed | + / − | Saves re-deriving context each session; offset by per-session protocol calls (welcome/store/checkpoint) that cost tokens and turns on every task, including ones that don't need memory. |
| Maintainability | + / − | Durable decision/lesson history aids long-running projects; the store itself is opaque and proprietary, so the knowledge can't be inspected or version-controlled like docs-in-repo. |
| Safety | neutral / − | Always-on ingestion of decisions and project context with no published security model or audit surface; accepted on trust. |
| Cost Efficiency | neutral | Freemium pricing plus per-session token overhead; net value depends on how often cross-session memory actually changes the outcome. |

## Verdict

**KEEP** — retained incumbent, not an independently verified recommendation. OMEGA is the operator's mandated, always-on memory and coordination layer, and the cross-session-continuity problem it solves is real and high-value, so removing it is not on the table. But this is explicitly a *keep-the-incumbent* call, **not** an ADOPT-everywhere endorsement: with no public repository, no inspectable source or license, and no benchmark in this evaluation, none of its capabilities can be verified, and it carries proprietary lock-in plus per-session protocol overhead. For anyone outside this setup it is not installable and serves only as a *pattern reference* for what a memory layer should do — in which case the open, inspectable alternatives are the actionable picks.

Compared to neighbors: **server-memory** (CONDITIONAL) is the open, minimal reference implementation — inspectable and forkable but stops at CRUD + substring search; **claude-mem** and **agentmemory** are open and benchmarkable. OMEGA is richer in protocol and coordination than any of them *as described*, but it is the only one in the cluster you cannot read, audit, or independently verify — so it wins on incumbency and feature surface, and loses decisively on transparency.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| OMEGA | MCP server | Persistent cross-session memory with semantic search, knowledge graphs, and coordination (proprietary; no public repo) | Agents forget everything between sessions; no continuity | agentmemory, beads, claude-mem, server-memory |
