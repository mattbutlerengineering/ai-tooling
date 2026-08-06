# Evaluation: Terminal coding agent cluster — which one do I run?

**Cluster:** Implement (standalone terminal coding agents — the "instead of `claude`" category)
**Contenders:** 21 catalog rows, all at `discovery-log` — see the selection table below
**Stars:** n/a — a 21-row cluster with no single subject; every contender's count is in the selection table (repo-metadata.json, fetched 2026-08-05)
**Last verified:** 2026-08-05
**Dev loop stage:** Implement (a few also touch Plan and Verify, noted per row)
**Layer:** Harness — every row here *replaces* the harness rather than extending it

---

## What it does

Twenty-one catalog rows answer one question: **which terminal coding agent do I run?** They are
genuinely different artifacts (unlike [#343](https://github.com/mattbutlerengineering/ai-tooling/issues/343)'s
case, where several rows were facets of one thing), and none is redundant with another on current
evidence. That is exactly the problem: a newcomer reading the Implement stage gets twenty-one rows
and no way to choose between them, and the eliminate-only triage lane
([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268)) cannot resolve it, because
ruling that one vendor's ecosystem matters less than another's is not an elimination an unmeasured
pass may make. Every pass over the cluster spends its budget re-deriving that fact and moves nothing.

This entry does the one thing that *is* available without measurement: it reads what the twenty-one
evals already say about themselves and turns it into a **routing table**. It changes no verdicts.
Every row stays at `discovery-log`, which is the correct status for a tool nobody here has run.

## How we tested it

**Source-grounded synthesis — nothing was installed or run.** No agent in this cluster was executed,
no task set was attempted, no latency or token figure was measured, and no model was held fixed
across two harnesses. Vendor benchmarks quoted in the underlying evals (SmallCode's headline number,
ClawCodex's "230× cheaper", jcode's performance claims) stay attributed to their vendors and are not
repeated here as findings.

What this *is*: a re-reading of 21 existing evaluations plus the catalog rows and `repo-metadata.json`,
extracting each tool's **own stated differentiator** and arranging them so the differentiators can be
compared side by side. The differentiators are quoted, not paraphrased into a ranking, because a
ranking is precisely what the evidence does not support.

**Evidence:** REVIEW

Sources read and cross-referenced:

```
evaluations/{qwen-code,gemini-cli,grok-cli,mimo-code,kimi-code,deepseek-reasonix}.md   # vendor-native
evaluations/{opencode,goose,openhands,forgecode,aichat,gptme,pi-earendil}.md            # model-agnostic
evaluations/{smallcode,osaurus,open-interpreter,clawcodex,jcode}.md                     # constraint-first
evaluations/{kilocode,lazycodex,ralph}.md                                               # adjacent, see below
evaluations/{plandex,command-code}.md                                                   # already SKIPped
CATALOG.md (Agent Harnesses + Dev Workflow rows) · repo-metadata.json (fetched 2026-08-05)
```

## Test design

> Not a measured eval, so this section records the design a measured one would need — and why it is
> harder than it looks. This is the part of [#347](https://github.com/mattbutlerengineering/ai-tooling/issues/347)
> worth having in writing even before anyone runs it.

- **Task/corpus:** a disclosed fixed task set with mechanical oracles, per
  [`measurement-protocols.md`](measurement-protocols.md) — e.g. N bug-fix tasks in a checked-out repo
  where "correct" is *the existing test suite passes*, so no human grades the output.
- **Baseline:** *not* "without the tool". The with-vs-without shape does not apply: the comparison
  here is agent-A-vs-agent-B, so the baseline is one designated harness and the metric is a paired
  `k/N` on the same tasks.
- **Metric:** pass-rate `k/N` per harness on the same tasks; Speed as a median over N≥3 runs; tokens
  from each harness's own accounting.
- **Reproduce:** not run — no command to publish.

**The design constraint that decides the subset.** A comparison across *vendor-native* CLIs measures
the **models**, not the harnesses: if `gemini-cli` runs Gemini and `kimi-code` runs Kimi, the `k/N`
delta is the model's, and the harness is a confound you cannot remove — you cannot point `kimi-code`
at Gemini. Fourteen of the twenty-one rows are vendor- or runtime-bound in this way. A measurement
that isolates the *harness* is only possible where the model can be held fixed, which is the
model-agnostic subset: **opencode, goose, forgecode, OpenHands** (plus `aichat`, `gptme` and `pi`,
which are toolkits with coding as one mode rather than coding agents first).

So the defensible measurement subset is **four**, all pointed at one model, and its result would
answer "which harness gets more out of the same model" — a real question with a real answer. It
would *not* rank the vendor CLIs, and no measurement can: those are chosen by which model and
ecosystem you are already in, which is a fact about the reader, not about the tool.

## What worked

- **Every eval in the cluster already names its own differentiator, and they do not collide.** This
  is the finding that makes a routing table possible at all. The differentiators were written
  independently, by different passes, at different times, and they partition cleanly: model family,
  context size, offline capability, host platform, surface (TUI vs editor), and cost economics. No
  two rows claim the same edge.
- **The evals also already agree the category is saturated on *capability*.** `forgecode`: "the
  category is saturated — its edge over opencode/goose/grok-cli is multi-model + configurability, not
  a distinct capability." `kimi-code`: "another member of a crowded category with no inner-loop edge
  beyond model choice … interchangeable with the other vendor CLIs." `jcode`: "it sits in a deep
  field of equally-capable harnesses." `MiMo-Code`: "doesn't yet show a clear advantage over the
  established CLIs." Four independent readings, one conclusion — which is itself the strongest
  evidence available that the *capability* axis is not where the choice gets made.
- **The cluster is smaller than it looks, on scope rather than on merit.** Five of the twenty-one
  answer a materially different question, by their own descriptions: `ralph` is "the canonical
  minimal autonomous agent loop … re-runs *a coding agent* repeatedly" — a pattern over whatever
  harness you point it at, not a harness; `lazycodex` runs *inside* Codex ("the choice here is
  host-driven"); `kilocode`'s own eval says its "edge is that it lives *inside* the IDE with native
  context rather than in a TUI"; `osaurus` is a Mac-native agent *runtime* where "agents, memory,
  identity, and tools live on your machine"; `aichat` is an all-in-one LLM CLI whose eval concedes
  "for deep multi-file coding, a dedicated agent … does more." Setting those aside leaves **sixteen**
  actual standalone terminal coding agents. That is a scoping observation, not an elimination — no
  verdict changes, and all five keep their rows.
- **The model-agnostic subset is the one place a measurement is possible**, and it is only four tools
  wide. That answers #347's first scoping question with a reason rather than a preference.

## What didn't work or surprised us

- **Star count is actively misleading in this cluster, in three separate ways.** `open-interpreter`
  carries ★67.6K, and its own eval states plainly that "the 64K stars belong to a retired Python
  project" — a star ranking here measures a dead repo. `opencode` at ★193K and `goose` at ★52K are
  the two model-agnostic incumbents whose evals describe them as peers ("this is a platform choice");
  the 3.7× star gap is not a 3.7× capability gap. And `pi` at ★83.7K — the cluster's third-largest —
  has only a `SOURCE-ONLY` stub eval, because `next-evals.py` scores on overlap pressure and stage
  gap and never on stars. So: **no**, stars are not a useful tiebreak here (#347's third scoping
  question), and this cluster is the case that shows why. Attention tracks vendor marketing budget.
- **#347's claim that `pi` has "no evaluation at all" is no longer true** — `evaluations/pi-earendil.md`
  exists as a `SOURCE-ONLY` bulk-triage stub, dated 2026-08-04. The underlying point stands: the
  cluster's third-most-starred row has never been exercised.
- **`pi`'s catalog one-liner reads ★67K against a live ★83.7K.** Recorded rather than fixed here: the
  figure is mirrored in `pi-earendil.md`'s `## Catalog entry` block, so editing one side alone creates
  exactly the drift detector U reports (#345), and a one-liner star refresh is a mechanical sweep of
  its own, not part of this cluster reading.
- **Two rows are already disposed and stay that way.** `plandex` — SKIP, dormant (last push
  2025-10-03; a *coding agent* rots when model APIs turn over, which is why it was SKIPped at 13
  months while `ralph` was left at ~6). `command-code` — SKIP, no declared license, confirmed against
  a live fetch. Neither is in the twenty-one.
- **The routing table cannot be derived mechanically, and that is the honest limit.** It rests on each
  eval's prose claim about itself. Nothing here verifies that `smallcode` actually works well on an 8B
  model, that `grok-cli`'s scheduler is reliable, or that `kimi-code`'s Windows support is genuinely
  first-class. The table routes you to the row whose *stated* differentiator matches your constraint;
  reading that row's eval is still the next step, and running the tool is the step after that.

## Selection table

Sorted by the constraint that decides the pick, not by rank. Every row is `discovery-log` — none of
these has been exercised here, and the "differentiator" column quotes or compresses the row's own
eval. Stars from `repo-metadata.json`, fetched 2026-08-05.

**If the model is already chosen for you** — vendor-native CLIs. The harness differences are small;
you are picking an ecosystem.

| Pick it when | Tool | ★ | Its stated differentiator |
|---|---|---|---|
| You want the biggest context window and the strongest free tier | [gemini-cli](https://github.com/google-gemini/gemini-cli) | 106.4K | 1M-token window, Google-owned, weekly releases, search-grounded + multimodal input |
| Your stack is Qwen-centric — **or** you want a delegated executor *under* Claude Code | [qwen-code](https://github.com/QwenLM/qwen-code) | 26.7K | the Claw/acpx ACP delegation path: offload grunt work to a cheap executor, keep Claude orchestrating |
| DeepSeek is your model and sessions are long | [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 30.9K | optimizes for **prefix-cache economics**, not model capability; static Go binary, signed releases |
| Grok is your model of record, and you want overnight/remote runs | [grok-cli](https://github.com/superagent-ai/grok-cli) | 3.4K | the autonomy stack — scheduler, batch, `--verify`, Telegram remote control, live X/web search |
| You want Kimi models, or you develop on Windows | [kimi-code](https://github.com/MoonshotAI/kimi-code) | 6.0K | Moonshot models, 24-release cadence, first-class Windows support |
| You want to sample another vendor CLI with the least setup | [MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) | 12.6K | zero-config free channel + one-step Claude Code auth import + persistent memory |

**If you want to keep choosing the model** — the model-agnostic set. This is also the only subset a
harness measurement can isolate (see Test design).

| Pick it when | Tool | ★ | Its stated differentiator |
|---|---|---|---|
| You want the largest open alternative, forkable, with a read-only plan mode | [opencode](https://github.com/anomalyco/opencode) | 193.4K | multi-provider; the plan agent's read-only exploration mode; SKILL.md portable from Claude Code |
| You are building an agent distribution for an organization | [goose](https://github.com/aaif-goose/goose) | 52.3K | model-agnostic *platform* with a custom-distribution story; "a platform choice, not a complement" |
| You need agents on shared infrastructure, with triggers | [OpenHands](https://github.com/OpenHands/OpenHands) | 83.1K | self-hosted orchestration: multi-backend, scheduled/webhook triggers, ACP multi-agent management |
| You want one interactive CLI pairing across many models | [forgecode](https://github.com/tailcallhq/forgecode) | 7.5K | Rust, MCP-enabled multi-model pair programmer; edge is consolidation, not capability |

**If a hard constraint decides it** — the constraint-first set. These exist *because* of the
constraint, which is why they are not interchangeable with the above.

| Pick it when | Tool | ★ | Its stated differentiator |
|---|---|---|---|
| Fully offline, local 8B–35B models, zero cost | [smallcode](https://github.com/Doorman11991/smallcode) | 2.0K | built *for* small local models: forgiving tool parsing, context budgeting, patch edits — its own docs say use a frontier model if you have one |
| Cheap open models **and** you need the code sandboxed | [open-interpreter](https://github.com/openinterpreter/openinterpreter) | 67.6K | harness emulation + first-class native sandboxing (★ belong to the retired predecessor — see above) |
| You run many concurrent sessions and footprint compounds | [jcode](https://github.com/1jehuang/jcode) | 15.9K | Rust, low-footprint, cross-platform; "lighter and faster for many sessions" rather than a unique capability |
| You want a Python-embeddable agent and cache-cost economics | [clawcodex](https://github.com/agentforce314/clawcodex) | 0.8K | Python rebuild of Claude Code + byte-stable prefix caching (headline claims unverified — pilot on throwaway work) |

**Toolkits with coding as one mode** — reach for these when the coding agent is not the whole ask.

| Pick it when | Tool | ★ | Its stated differentiator |
|---|---|---|---|
| You want one Rust binary for shell assist + REPL + RAG + agents | [aichat](https://github.com/sigoden/aichat) | 10.3K | consolidation over a pile of single-purpose tools; mind the Shell Assistant's execution risk |
| You want a minimal, hackable base to build bespoke agents on | [gptme](https://github.com/gptme/gptme) | 4.4K | local-first, fully transparent, extendable into custom persistent agents |
| You want a batteries-included agent toolkit, coding CLI included | [pi](https://github.com/earendil-works/pi) | 83.7K | unified LLM API + agent loop + TUI + coding CLI in one package (**never exercised — stub eval only**) |

**Adjacent — answers a different question.** Kept in the catalog and findable by name; listed here so
a reader stops mistaking them for entries in this decision.

| Row | What it actually is |
|---|---|
| [ralph](https://github.com/snarktank/ralph) | an autonomous **loop** that re-runs a coding agent until the PRD is done — a pattern over whatever harness you point it at |
| [lazycodex](https://github.com/code-yeongyu/lazycodex) | an agent harness **inside Codex** — "the choice here is host-driven" |
| [kilocode](https://github.com/Kilo-Org/kilocode) | an **in-editor** agent (VS Code/JetBrains), not a TUI — the catalog's representative of that category |
| [osaurus](https://github.com/osaurus-ai/osaurus) | a Mac-native agent **runtime** (agents, memory, identity, tools local), not a coding agent per se |
| [plandex](https://github.com/plandex-ai/plandex) · [command-code](https://github.com/CommandCodeAI/command-code) | already **SKIP** — dormant since 2025-10, and no declared license, respectively |

## Quality signals affected

Signals of *the cluster reading*, not of any tool in it — no tool was run, so no tool's signals moved.

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Nothing was measured; no claim here is stronger than the eval it is quoted from. |
| Speed | + | The decision that took reading 21 evals now takes reading one table; the constraint you already have picks the row. |
| Maintainability | + | One page absorbs the next pass over this cluster instead of each pass re-deriving "saturated on capability, chosen on ecosystem". |
| Safety | neutral | Routing only. The execution-risk notes that matter (`aichat`'s Shell Assistant, `open-interpreter`'s host execution) are carried through, not resolved. |
| Cost Efficiency | + | Retires the recurring triage cost the cluster imposes — four passes have now hit it (#341, #342, #344, #347). |
| Verifiability | + / − | **+** every routing claim is traceable to a named eval's own words. **−** those evals are themselves REVIEW-grade, so the table is only as checkable as its sources, and no amount of arranging them makes it measured. |

## Verdict

**Not a verdict on any tool — a routing table, and a scoping answer.** Every one of the 21 rows stays
at `discovery-log`, which is the honest status for a tool nobody here has run. Nothing is promoted;
nothing is eliminated. What changes is that the cluster now has a page that answers "which one do I
run" with *your constraint decides, here is the map*, instead of twenty-one rows in alphabetical
order.

**The cluster is saturated on capability and decided on ecosystem** — four of its own evals say so
independently, and none of the twenty-one claims an edge another one claims. That is why no
elimination is available and why every triage pass over it stalls: the eliminate-only rule is working
exactly as designed, refusing to let an unmeasured pass cut fifteen rows on vibes.

**#347's three scoping questions, answered:**

1. **Which subset would a measurement cover?** **Four** — `opencode`, `goose`, `forgecode`,
   `OpenHands` — pointed at one fixed model. Not a preference: a comparison across vendor-native CLIs
   measures the *models*, since you cannot point `kimi-code` at Gemini, so the harness is an
   unremovable confound for fourteen of the twenty-one rows. The measurable question is "which
   harness gets more out of the same model", and only the model-agnostic set can be asked it.
2. **One cluster row or twenty?** **Keep the rows, add this page.** Every row names a real, separately
   installable artifact, so collapsing them would make tools unfindable by name — the opposite of
   #343's case, where rows were facets of one artifact. The gap was a router, and this is it.
3. **Is star count a useful tiebreak?** **No**, and this cluster is the proof: `open-interpreter`'s
   ★67.6K belong to a retired predecessor, `opencode`'s 3.7× star lead over `goose` is not a
   capability lead by either eval's account, and ★83.7K `pi` has never been exercised. Stars measure
   attention, and attention here tracks vendor marketing.

**What would change this page.** A measured four-way run per the Test design section above. That
would let the model-agnostic block carry a `k/N` instead of a differentiator, and would be the first
thing in this cluster to earn a verdict word.

## Catalog entry

n/a — this reads existing catalog entries (the 21 terminal-coding-agent rows) rather than introducing
a new one. Per #347's scoping question 2, the rows stay as they are.
