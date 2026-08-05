# Software factories — field notes from practitioners

**What this is:** what six 2026 talks on "software factories" actually say, read end-to-end and
distilled. It is the *practitioner* half of the software-factory material in this repo; the
*vendor* half is [`software-factories.md`](software-factories.md), which uses these notes as one
of its two inputs. Gathered for
[#307](https://github.com/mattbutlerengineering/ai-tooling/issues/307).

**How it was gathered (and what is not here).** Subtitles and metadata were pulled with `yt-dlp`
(`--write-auto-subs --skip-download`), cleaned of timing/markup, and read in full — six
transcripts, ~34,500 words. The transcripts themselves are **not committed**: they are
third-party content, and this repo is a curated manual, not a transcript archive. What is
committed is the reading. Every claim below is attributable to the talk named beside it;
quotations are from the auto-generated captions, so they carry caption-level transcription
noise (a talk saying "Kimi K3" captions as "ChemK 3"; "Context7" as "Coptic 7") — quoted
wording is verbatim from the captions, and names are corrected silently where the intent is
unambiguous.

## The corpus

| Talk | Speaker / channel | Date | Length | Position |
|---|---|---|---|---|
| [My Super Simple Software Factory (For Agentic Engineers)](https://www.youtube.com/watch?v=haUfb1ievTE) | IndyDevDan | 2026-08-03 | 30 min | build one, from agents **plus code** |
| [Building your own software factory](https://www.youtube.com/watch?v=rnDm57Py54A) | Eric Zakariasson (Cursor) · AI Engineer | 2026-04-28 | 84 min | build/run/scale one on a team |
| [From AI Coding Agents to the Software Factory](https://www.youtube.com/watch?v=SkoT4RkteSA) | Eno Reyes (CEO, Factory AI) · Arize Observe | 2026-07-01 | 15 min | the enterprise case |
| [I Built an Agentic Software Factory with Codex and Claude Code](https://www.youtube.com/watch?v=AbpyqAfxZ8c) | Owain Lewis | 2026-07-25 | 21 min | a working ticket→merge pipeline |
| [I Tried Building with Agentic Factories. They Failed.](https://www.youtube.com/watch?v=mREHBZQbhBo) | Ben Fellows | 2026-04-27 | 12 min | **against** generic factories |
| [The Agentic Engineer Workflow You Need In 2026](https://www.youtube.com/watch?v=ElYxdpYi4U0) | Zen van Riel | 2026-05-20 | 17 min | **against** the whole framing |

The first two are the URLs [#307](https://github.com/mattbutlerengineering/ai-tooling/issues/307)
names. The other four came from a YouTube-scoped search, chosen to include two dissents — a
corpus of five enthusiasts would have produced a consensus that isn't one.

## Per-talk notes

### IndyDevDan — agents **plus code** beats agents alone

The thesis is a comparison, not a product: *"agents plus code beats agents alone."* A factory is
a system that "operates without you just as well and sometimes even better than you would," and
*"the amount of leverage you can get is determined by the quality of your investment into your
software factory."*

- **The unit is the AI Developer Workflow (ADW)**, not the skill. Atomic workflows — scout, plan,
  build, quality-check (lints, formats, type checks, docs) — compose into the ones that do real
  work: `plan → build`, `plan → build → test`, `build → review`. *"I'm not thinking at the skill
  level."*
- **Deterministic gate checks between agent steps.** "Code that runs at the end of the plan step"
  verifies the step happened before the next agent starts. The stated anti-pattern is the obvious
  one: *"a lot of engineers are just going to start throwing everything into skills, everything
  into a bunch of agents"* — instead move what is mechanical into code, and hand back to the agent
  only when it fails.
- **Typed handoffs.** *"My agents are outputting JSON, it's getting formatted, it's getting
  validated."* The planner leaves "a note for the next agent" — a structured artifact, not a
  conversation to inherit.
- **Per-role models.** The planner runs a high-thinking frontier model; the builder runs a fast
  cheap one. Role, not preference, picks the model.
- **The factory is portable.** The whole thing ships as one skill with an installer that "allows
  this software factory to be built into new code bases" — an artifact you carry between repos.

### Eric Zakariasson (Cursor) — the ladder, the checklist, and the silo problem

The longest and most systematic of the six: build the factory, run the factory, scale the factory.

- **Levels of autonomy.** A six-stage ladder (attributed in the talk to a Dan Shapiro post):
  spicy autocomplete → pair programmer → *AI generates the majority, human reviews* → *manager
  delegating, reviewing outputs before code* → the **software factory**, which Shapiro calls the
  *"dark factory"*: a black box where "you as a manager just provide the intent and the
  instructions and the goal." His read: most adopters sit between levels two and three; he is at
  four. **The factory is the top of a ladder, not a starting position.**
- **Why:** throughput (agents don't sleep) and consistency — *"assembly lines produce consistent
  outputs. If you build your factory right, you can probably have very consistent output."*
- **The diagnostic that makes the whole talk useful:** when agents start feeling probabilistic and
  you feel you are "losing a lot of determinism… that's probably a sign that you need to build
  more guardrails for the factory." Agent flakiness is read as a *missing-guardrail* signal rather
  than a model problem.
- **The build checklist — four layers:**
  1. **Primitives and patterns** — how the code is structured. Modular and co-located means an
     agent can `ls` one folder and find everything, "instead of having to grep and search all of
     the codebase."
  2. **Guardrails** — can the agent verify its own work? Tests it can run to know "oh, I messed
     something up."
  3. **Enablers** — "what can you allow the agents to do to actually let them be free?" Skills and
     MCP servers that add *capability*. His example: a skill for adding a feature flag, so an
     autonomous run can ship behind a flag and hand you a toggle instead of a merge decision.
  4. **Environment** — can an agent start your dev environment unattended? If yes, "you can scale
     it up infinitely on separate VMs." If no, that is the bottleneck.
- **Running it — automations:** a daily-review automation; an automation that learns from comments
  on merged PRs; **agentic code owners**, because human code owners "were right most of the time,
  like 80% of the time, but for these 20% of the time they caused a lot of bottlenecks" — blocked
  merges waiting on a reviewer in another timezone.
- **Scaling it — the silo failure.** Because rules and skills are new, "almost everybody feels *oh,
  this is a rule for me and I don't want to inflict it on other people*," and you get "each
  engineer ends up having their own separate different factory." The fix is to treat guardrails,
  enablers and primitives as shared team infrastructure held to the same engineering discipline as
  product code.

### Eno Reyes (Factory AI) — agent-readiness, and the deceleration finding

The enterprise framing, and the one talk with a claim that would change what you do first.

- **Three ages.** Autocomplete (line → paragraph → page → repo, in one tool) → the **coding
  agent**, which is still human-initiated: "a human being saying *do this task for me please*,
  waiting for the response" → the **software factory**, "a much more continuous and 24/7 process…
  agents that operate across the entire software development life cycle."
- **Most of the pipeline is not code.** Signals → triage → planning → code → validation (review,
  QA, testing) → ship → monitor → back to signals. "People vastly underestimate how much of the
  SDLC pipeline is not code." One bottleneck on the critical path cancels the ROI of everything
  upstream.
- **Agent readiness, graded 1–5.** The system must give "deterministic signals of correctness
  regardless of if a human is in the loop" — tests, linters, type checkers, formatters. Level 4–5
  codebases show "massive acceleration of end-to-end product life cycles." **Level 1–2 codebases
  show "very active deceleration."** Stated bluntly: you can adopt every agent tool, do everything
  the mandate asked, "and you're actually slowing down your company." (Factory publishes the model
  as [nine pillars with a gated 80%-of-previous-level rule](https://docs.factory.ai/web/agent-readiness/overview);
  see [`software-factories.md`](software-factories.md#agent-readiness-is-the-prerequisite-nobody-sells-you).)
- **Model agnosticism as a principle, not a feature:** "every one of the model labs can give you
  their best model, but a model-agnostic approach gives you the best model at any given moment" —
  for cost *and* quality.
- **Sovereignty:** don't outsource to "a blackbox system where you don't have the ability to say
  what is actually happening… where's the data being stored." SaaS is fine; losing the *optionality*
  to own it is not.
- **A caution about building your own harness.** If you want one agent across CLI, desktop, TUI,
  Slack, web, API and CI, "I wouldn't even say it's a bad idea, I just think that it's a massive
  investment to maintain an agent" — effectively a second product, with compaction and token
  caching to own.
- **The role becomes stewardship** — "gardening" a living system: observing, intervening, refining,
  and setting the policies and autonomy tolerance.
- **Measure outcomes, not tokens or lines.** Cycle time, plus your equivalent of the metric that
  licensed self-driving cars: "bugs or incidents in production… how many are humans introducing
  versus our agents introducing." Without that instrumentation you can never justify raising
  autonomy — "you are never going to be able to transition."

### Owain Lewis — a factory you can watch run

The most concrete of the six: a working, open-source pipeline demonstrated live.

- **Tickets are the queue.** A label drives the stage: apply `factory ready for spec` and the
  spec workflow runs. "Factory will move stuff through the pipeline without us doing anything."
  Config is a `config.toml` pairing a **source** (GitHub issues) with a **trigger** (the label).
- **Stages:** vague ticket → agent rewrites it into an implementable ticket → spec → isolated
  worktree → plan → implement → tests → review → merge. Every stage is an agent, and the shape is
  fixed: "we can be very, very consistent in our dev process."
- **Isolation is structural.** "I'm using worktree-based isolation, which means every time we run
  an agent, we're going to spawn a new git worktree and run it there." Plus VM or Docker
  sandboxing for production runs — with an honest "I'm still new to sandboxing and still figuring
  out the right approach myself."
- **Harness-agnostic by construction:** "exactly the same process whether I was using Claude Code
  or Codex or Pi." The demo delegates a ticket to Codex.
- **Scheduled work generates its own queue.** `factory run bug finder` spawns a worktree, finds a
  bug, and *opens a ticket* — output is a queue item for review, not a merge.
- **The economic argument for pipelines** is wall-clock: a typical task runs an agent "maybe 20
  minutes to even up to an hour… I don't want to be waiting in my terminal for 34 minutes." And
  the honest scope: "there's a percentage of tickets that we can now just give to agents" —
  mechanical work, security upgrades, bug fixes, "trivial tedious work that developers don't like
  doing anyway."

### Ben Fellows — against generic factories, for bespoke pipelines

Tried four or five factory products; "none of them have particularly worked well for me."

- **The argument:** *"There's a reason why Ford doesn't build every one of their cars in one
  factory."* One pipeline that claims to fit every codebase is the flaw. Keep what factories got
  right — reusable agents, custom prompts, shared memory — and build **bespoke pipelines per repo
  and per task type**: eight to ten in a project, one for feature work, one for test automation,
  and so on.
- **Why a pipeline beats one long agent run** — four reasons, all context-shaped:
  chaining **different personalities** (planner, executor, reviewer, verifier, manager) that are
  "not influenced by the previous instance"; **cross-vendor** composition, since the handoff is
  evidence and documentation in a repo, so Codex and Claude Code can share one pipeline;
  **escaping the context ceiling** by passing full transcripts instead of compressed summaries;
  and **owning the git story end to end** — "a pipeline owns its own worktree, creates its own
  branch, keeps it super super clean."
- **Fresh context per block.** "Each block gets a fresh context every time… significantly more
  accurate at scale."
- **Role structure:** planner → executor writes a failing test → executor makes it pass →
  refactorer, with review and verify steps between, and a **manager that blocks or promotes**
  before merge to main.
- **Governance by design.** They wrote an app over the pipeline: the manifest, the build steps,
  the test runs, every commit. Every run makes a branch and commits each step.
- **How this differs from skills and commands:** "a pipeline forces a deterministic system."
  Skills and commands are not the alternative — they are *parts*: "they should just be part of the
  pipeline."
- **Policy-as-code as the pre-test gate.** "Hundreds and hundreds of rules" constraining
  development, run *before* the tests, on the grounds that "policy-as-code is all about the quality
  of the code, and then your tests are much more about the business outcomes of the code."
- **The honest cost is time.** Pipelines "run significantly longer" than a single agent. "It's not
  going to be like the dopamine hit of AI doing something in 2 minutes" — the output is a
  merge-ready branch.

### Zen van Riel — against the framing itself

The dissent that questions whether any of this survives contact with a review queue.

- **Four parallel agents, not fifty.** "I'm not going to pretend like I'm running 50 agents at the
  same time. My mental capacity is pretty much at four parallel work streams." The four panes are
  **effort-tiered** — two high, one medium, one low — and the task picks the lane: the low-effort
  pane answers "which languages does this use" while the high-effort pane is still scoping five
  features.
- **Methodology skepticism.** Spec-driven development, BMAD, "context engineer vs prompt engineer
  vs agentic engineer" — "a lot of these things are just gimmicks that don't really stand the test
  of time… anything that does work will just be rolled up into something like Claude Code," his
  example being to-do tracking moving out of markdown files and into the tool. His filter: wait out
  the hype and adopt what survives three to four months.
- **Ground quality commands in engineering books, not prompt repos.** A `smell` command built on
  *Clean Code* and design-pattern literature, versus copy-pasting from "a prompt repository that
  has 60,000 stars… prompts that say *you are a senior engineer, code and do not make any
  mistakes*."
- **There is no universal review command** — it depends on the language, the complexity, how many
  human reviewers exist and what they prefer, the team's agreed style. Which is why he declines to
  publish his.
- **MCP vs CLI vs bash is a judgement, not a rule.** For GitHub or Jira the CLI exists and the
  agent is already authenticated, so bash wins. MCP earns its place for *unknown internal
  services*, and for specialized backends — he names Context7 (docs chunked for a model rather
  than a generic web search) and Serena (language-server-backed search).
- **Worktrees, because git context is shared.** Four panes on one checkout "will get messy
  quickly." And the reusable-skill move: if every new worktree needs its dependencies reinstalled,
  make *that* a skill.
- **The number.** "The people who are doing the best with agentic coding aren't screaming from the
  rooftops that they're five times more productive. They might see 30 to 60% performance gains."
- **The ceiling is human review, and it is not going away.** "If you come to other developers with
  10,000 lines of code every single day, I can guarantee you that things aren't going to end very
  well." His own story: a feature built in two days, pushed back by a senior reviewer for lacking
  long-term architectural thinking — and when he actually read the code, "because I only skimmed
  it, I wanted to create AI code faster," he agreed.

## Where they agree

Six talks, three of them selling nothing, two of them arguing against the term:

1. **Deterministic code between agent steps is the load-bearing part.** IndyDevDan's gate checks,
   Fellows's policy-as-code before tests, Zakariasson's guardrails, Reyes's "deterministic signals
   of correctness regardless of if a human is in the loop." Nobody credits the wins to better
   prompts.
2. **Fresh context per stage beats one long run.** Explicit in Fellows ("each block gets a fresh
   context") and IndyDevDan (validated JSON handoffs); implicit in the per-stage agents of Lewis's
   pipeline; and it is the standing pane-hygiene discipline in van Riel.
3. **Isolation is structural, not optional.** Worktree-per-run in Lewis, Fellows and van Riel; VMs
   or Docker sandboxes once it runs unattended.
4. **Harness- and model-agnostic by design.** Reyes as a purchasing principle; Fellows because the
   handoff is files in a repo; Lewis demonstrating it with Codex; IndyDevDan choosing a different
   model per role.
5. **The queue is tickets, and feedback re-enters it.** Lewis's labels, Fellows's manifest,
   Reyes's signals→triage front end. Scheduled jobs *open tickets* rather than merging.
6. **The role shifts from worker to manager** — Zakariasson's ladder, Reyes's gardener, van Riel's
   "AI-native engineer" — and *review capacity*, not generation capacity, is the binding
   constraint.

## Where they disagree — and which side to take

| Question | The split | Read |
|---|---|---|
| **Buy or build the factory?** | Reyes: buying beats maintaining "effectively a fully different product." Fellows: bought factories failed him — "Ford doesn't build every one of their cars in one factory." | Not actually opposed. Reyes means the *harness*; Fellows means the *pipeline*. Buy or adopt the harness; own the pipeline. |
| **One pipeline or many?** | Fellows: 8–10 bespoke pipelines per project, keyed to task type. Everyone else demos one. | Fellows is describing a later stage. Start with one; split when a task type keeps fighting the shape. |
| **How many parallel agents?** | van Riel: four, matched to human attention. Zakariasson: "scale it up infinitely on separate VMs." | The variable is whether *you* are the reviewer. Four is a limit on synchronous supervision; infinite assumes the queue absorbs the output. |
| **Does the methodology matter?** | van Riel: mostly gimmicks that get absorbed into the tool. Everyone else: the methodology *is* the product. | van Riel's filter (adopt what survives 3–4 months) is compatible with the rest — it is a *timing* rule, not a rejection. It correctly predicts which vocabulary to skip. |
| **What is the honest speedup?** | van Riel: 30–60%. Vendors: 70% productivity, 80× delivery. | The vendor numbers in [`software-factories.md`](software-factories.md) are self-reported and unaudited. van Riel's is the number to plan against. |

## What this means for this repo

The consensus items map onto machinery that already exists here, which is the useful finding:
this repo is closer to the practitioner consensus than to any vendor's product.

- **Deterministic gates between agent steps** → `make check` / `audit-evals.py`. The detector
  suite *is* Fellows's policy-as-code layer: rules that run before the semantic review, gate CI,
  and hand failures back with a file and a line.
- **Tickets as the queue, feedback re-entering it** → GitHub Issues plus the `triage` state
  machine and the eliminate-only rule, which is precisely the "scheduled jobs open tickets, they
  don't merge" discipline in stronger form (a bulk lane may write `SKIP`, never `ADOPT`).
- **Fresh context and typed handoffs per stage** → the stage skills in
  [`intent-to-production-recipe.md`](intent-to-production-recipe.md).
- **Agent readiness** → the one idea with no counterpart here, and the one worth acting on: this
  repo has linters and a gated test suite but has never scored itself on whether an *agent* can
  get a correctness signal without a human. That is the recommendation carried into
  [`software-factories.md`](software-factories.md#the-ideal-workflow).

The two dissents are the ones to keep visible. Fellows's is a warning against adopting a
prefabricated pipeline — the same reasoning that makes this repo's evaluations skeptical of
end-to-end frameworks. Van Riel's is the throughput ceiling: generation is not the bottleneck,
**review is**, which is exactly the sixth quality signal ([Verifiability](../WORKFLOW.md)) this
repo added for its own reasons and which no vendor in the corpus measures.
