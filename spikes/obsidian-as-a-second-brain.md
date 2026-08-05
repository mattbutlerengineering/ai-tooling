# Spike: Obsidian as a second brain

**Issue:** [#257](https://github.com/mattbutlerengineering/ai-tooling/issues/257) · **Date:** 2026-08-05 · **Outcome:** the practice, the AI-integration layer, and the failure modes — documented; nothing installed, no vault audited

**Why this belongs in an AI-tooling repo.** A generic PKM tutorial would not. This one
earns its place on a single property: **an Obsidian vault is a directory of plain
markdown with YAML frontmatter, so an agent reads and writes it with exactly the tools
it uses on a repo.** It is the same substrate as `CLAUDE.md`, as a skill, as the
evaluations in this repo — which makes a vault the one knowledge store you can hand to
an agent without an import step, an embedding pipeline, or a vendor.

This repo already carries five catalog rows and evaluations in this space —
[`claude-obsidian`](../evaluations/claude-obsidian.md),
[`obsidian-skills`](../evaluations/obsidian-skills.md),
[`obsidian-second-brain`](../evaluations/obsidian-second-brain.md),
[`claudian`](../evaluations/claudian.md), and the `claude-code-memory-setup` recipe —
and every one of them is a *tool* evaluation. **None documents the practice.** That is
the gap #257 names. (Note the name collision this file deliberately avoids:
`evaluations/obsidian-second-brain.md` is a **tool** called *obsidian-second-brain*;
this spike is about the practice.)

## The methodologies, and which parts survive contact

Four systems get cited constantly, and they are not competitors — they answer different
questions.

| System | The question it answers | The durable part |
|---|---|---|
| **PARA** (Tiago Forte) | *Where does this note go?* Four top-level folders by **actionability**: **P**rojects (active, with an end), **A**reas (ongoing responsibility), **R**esources (topics of interest), **A**rchives (inactive) | Sorting by actionability rather than by topic. Topic taxonomies rot; "am I working on this?" doesn't. |
| **CODE** (Forte) | *What do I do with it?* **C**apture → **O**rganize → **D**istill → **E**xpress | **Distill** is the only step that compounds, and the only one people skip. |
| **Zettelkasten** (Luhmann) | *What makes a note worth keeping?* One idea per note, written in **your own words**, explicitly linked. Four kinds: fleeting, literature, permanent, structure | Atomicity + own-words. A note you can't restate is a note you don't understand. |
| **LLM-wiki / update-not-append** (Karpathy's pattern, and what the newer AI vault tools implement) | *How does it stay coherent?* New sources **update existing pages** and contradictions get reconciled, rather than piling up | The answer to append-only rot — and the reason the AI tools in this space exist at all. |

**How they compose, in one sentence:** use **PARA for the folders**, **Zettelkasten for
one atomic-notes folder inside it**, **CODE as the verb list**, and treat
**update-not-append** as the rule you enforce during review. PARA answers *where*;
Zettelkasten answers *what's worth writing*; they do not conflict, and picking one and
arguing about it is the most common way to spend a week not writing notes.

## The minimum viable practice

Six steps. Everything else is optional.

1. **Capture, cheaply and in one place.** An inbox note or a daily note. Friction here
   is fatal — if capture costs more than ten seconds you will stop.
2. **Daily note as the append surface.** Timestamped, unstructured, no filing decision
   required at capture time.
3. **Distill on a schedule, not on capture.** Once a week, walk the inbox: each item
   becomes an atomic note in your own words, gets merged into an existing note, or gets
   deleted. **Deleting is a valid outcome and most items deserve it.**
4. **Link as you write, not afterwards.** A `[[link]]` you add while the context is in
   your head is worth ten added later during a "linking session."
5. **Maps of Content over folders for retrieval.** A hand-written index note per theme
   (`[[MOC — Agentic workflows]]`) beats both a folder tree and search, because writing
   the MOC *is* the distillation.
6. **Review, and let things die.** Projects finish and move to Archives; Areas get
   revisited. A vault that only grows is a landfill with backlinks.

If you do only one of these, do **3**. Capture without distillation is the collector's
fallacy with better software.

## Tooling: keep it small

Obsidian ships more of this natively than the plugin lists suggest.

**Core (no install):** Daily notes · Templates · Graph view · Canvas
([JSON Canvas](https://github.com/obsidianmd/jsoncanvas), an open format, ★3.6K) ·
**Bases** — a *core* plugin (`.base` files, or embedded in a code block) giving
table / list / cards / map views over notes and their properties, with the data staying
in plain markdown.

**Community, in rough order of payoff:** Dataview (query notes as data) · Templater
(scripted templates) · Tasks · Calendar · **Git** — see below · Style Settings ·
Excalidraw.

**Official first-party:** [Web Clipper](https://github.com/obsidianmd/obsidian-clipper)
(★4.9K) for web → vault · [Importer](https://github.com/obsidianmd/obsidian-importer)
(★1.6K) from Notion / Evernote / Apple Notes / OneNote / Keep ·
[obsidian-headless](https://github.com/obsidianmd/obsidian-headless) (★212) to sync a
vault from the command line without the desktop app.

**Git in the vault is not optional once an agent can write to it.** It is the undo for
every automated edit, and the diff is how you review what the agent decided to
"reconcile."

## Wiring an agent to the vault — three ways

Ordered by how much infrastructure they cost. Facts checked 2026-08-05.

### 1. Filesystem — start here

Point the agent at the vault directory. That is the whole setup. It works when Obsidian
is closed, needs no plugin, no port, no daemon, and gives the agent the same
Read/Write/Grep it uses on any repo.

What you give up: live metadata, the active file, the command palette, and Obsidian's
own link resolution — the agent sees `[[Note]]` as text, not as an edge.

### 2. MCP over the Local REST API — when you want the live vault

| Server | License | Stars | Shape |
|---|---|---|---|
| [`coddingtonbear/obsidian-local-rest-api`](https://github.com/coddingtonbear/obsidian-local-rest-api) | MIT | ★2,754 | The Obsidian **plugin** itself, and it now ships a built-in MCP server at `/mcp/` — so the agent talks to the running app: live metadata, active file, command palette, surgical section-level patches |
| [`MarkusPfundstein/mcp-obsidian`](https://github.com/MarkusPfundstein/mcp-obsidian) | MIT | ★4,260 | Separate MCP server that connects *through* the Local REST API plugin |
| [`cyanheads/obsidian-mcp-server`](https://github.com/cyanheads/obsidian-mcp-server) | Apache-2.0 | ★649 | Read/write/search/surgical-edit incl. tags and frontmatter; STDIO or Streamable HTTP |

The trade is real: **Obsidian must be running.** For an agent that works while you
don't, that is a dependency on a GUI app being open, which is exactly the kind of thing
that fails silently — the same class as the `claude-reflect` hook that stopped loading
and went three weeks unobserved ([#366](https://github.com/mattbutlerengineering/ai-tooling/issues/366)).

### 3. Skills and vault-resident tools — when you want opinions, not just access

All four are catalogued here, and all four evaluations currently read
**`discovery-log`** — they are reviewed, not run:

- [`kepano/obsidian-skills`](../evaluations/obsidian-skills.md) (MIT, ★44K,
  first-party) — the eval calls it the best Agent-Skills hygiene in the catalog, and
  singles out **`defuddle`** (web → clean markdown) as the one piece worth lifting even
  if you never keep a vault.
- [`claude-obsidian`](../evaluations/claude-obsidian.md) — 15 skills, a compounding
  wiki, hybrid retrieval (contextual prefix + BM25 + rerank), multi-writer safety.
- [`obsidian-second-brain`](../evaluations/obsidian-second-brain.md) — the
  update-not-append mechanic as a cross-CLI skill; the eval's own caution is to review
  its edits, because auto-rewriting can remove wanted content.
- [`claudian`](../evaluations/claudian.md) — embeds Claude Code / Codex / OpenCode
  *inside* Obsidian, vault as working directory, with word-level inline diffs.

**Take the pattern before the tool.** Update-not-append is a review rule you can enforce
by hand in step 3 of the practice above; none of these has been run hands-on here, and
handing an unreviewed agent write access to a knowledge base is how you find out which
notes you cared about.

## Failure modes

The interesting half of this research. Each has a countermeasure.

| Failure | What it looks like | Countermeasure |
|---|---|---|
| **Collector's fallacy** | 4,000 clipped articles, no atomic notes | Step 3. Distillation on a schedule, deletion as a normal outcome |
| **Append-only rot** | Six notes on the same idea, three contradicting | Update-not-append, enforced during review |
| **Unreviewed agent writes** | A "reconcile" pass quietly removes the paragraph you needed | Git in the vault; read the diff. Non-negotiable |
| **Tool-before-writing** | Three weeks configuring Dataview, eleven notes | Core plugins only until the practice sticks |
| **Graph aesthetics** | The graph view looks beautiful and is never used to find anything | MOCs are the retrieval surface; the graph is a picture |
| **Sync conflicts** | Two devices, two copies of the same daily note | One sync mechanism only (Obsidian Sync *or* git *or* a file syncer — never two) |
| **Vault as agent memory** | Vault grows into an undifferentiated context dump | See the boundary below |

## Where this meets the dev loop

| [Loop stage](../WORKFLOW.md) | What the vault does | [Signal](../WORKFLOW.md#quality-signals) |
|---|---|---|
| **Plan** | Retrieval of prior art — what did I decide last time, and why | Correctness, Speed |
| **Reflect** | The capture surface for corrections and decisions that would otherwise live only in a session transcript | Correctness |
| Outer **Discover** | Where research accumulates before it is a spec | Speed |
| Outer **Retrospect** | Where the weekly review actually happens | All |

**The boundary with the memory tools already catalogued** (`claude-mem`, `agentmemory`,
`supermemory`, `memory-os`, and the bake-off between them) is worth stating plainly,
because it is the question that decides whether you need both:

> **A memory tool is written for the agent. A vault is written for you and is *readable*
> by the agent.** Pick by who the primary reader is. Agent-only working memory —
> corrections, session context, retrieval for the next prompt — belongs in a memory
> tool, where you never look at it. Durable thinking you will re-read, argue with, and
> reshape belongs in the vault, in your own words. They are not substitutes, and using a
> vault as agent scratch memory is the fastest way to ruin it.

## What was not done

No vault was audited and no tool was installed or run — this is documented practice plus
verified tool facts, not a hands-on evaluation. Repo facts (stars, licences, push dates)
were pulled from the GitHub API on **2026-08-05**; the Obsidian Bases description is from
the [official help](https://obsidian.md/help/bases). The four Obsidian tools this routes
to all sit at `discovery-log` — **promoting any of them to a real verdict needs a
hands-on run**, and the update-not-append tools are the ones where that matters most,
since the whole mechanic is an agent editing text you did not re-read.

## Sources

- Practice: PARA / CODE (Tiago Forte, *Building a Second Brain*); Zettelkasten (Luhmann; fleeting / literature / permanent / structure notes); MOC-first retrieval (LYT); the LLM-wiki update-not-append pattern
- [Obsidian Bases](https://obsidian.md/help/bases) — core plugin, `.base` files, database views over plain markdown
- First-party repos: [obsidian-clipper](https://github.com/obsidianmd/obsidian-clipper) · [obsidian-importer](https://github.com/obsidianmd/obsidian-importer) · [obsidian-headless](https://github.com/obsidianmd/obsidian-headless) · [jsoncanvas](https://github.com/obsidianmd/jsoncanvas)
- MCP: [obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api) · [mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) · [obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server)
- This repo: [`claude-obsidian`](../evaluations/claude-obsidian.md) · [`obsidian-skills`](../evaluations/obsidian-skills.md) · [`obsidian-second-brain`](../evaluations/obsidian-second-brain.md) · [`memory-systems`](../evaluations/memory-systems.md) · [`agentmemory-vs-claude-mem-bakeoff`](../evaluations/agentmemory-vs-claude-mem-bakeoff.md)
