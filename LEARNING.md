# Learning

Curated external learning resources — YouTube channels, conference talks, and web
references for AI-assisted development — the passive-learning companion to the tool
inventory.

**Why this is separate from `CATALOG.md`:** the catalog inventories *installable
tooling* (skills, harnesses, MCP servers, frameworks), and its integrity tooling
assumes every entry is a GitHub repo — the install resolver, link-rot detector,
and archived-repo scan only understand `github.com/owner/repo` URLs, and
`reconcile-counts.py` treats the catalog as a count of tools. These resources are
neither installable nor GitHub repos, so they live here instead and never touch
those gates. Map the topics below onto the dev loop in
[WORKFLOW.md](WORKFLOW.md).

**When a set of talks has actually been watched and distilled**, the reading lives
in `methodologies/` and this page links to it — see
[software-factory-field-notes.md](methodologies/software-factory-field-notes.md),
which reduces six of the talks listed below to what they agree on, what they split
on, and which side to take. This page stays a *pointer* list; the distillations are
their own artifacts.

**Last verified:** 2026-08-05 — the six software-factory channels and talks added
below were confirmed live at that date (metadata pulled directly, and each talk was
watched end to end). The rest of the page was last confirmed 2026-06-28 — channel
URLs, listed video links, and web resources confirmed via web fetch. Channels with
no per-video links had no specific video confirmed at verification time (channel is
still good; titles were left out rather than link to a guess). The Anthropic
harness-design entry added 2026-08-07 was confirmed live at that date via search
corroboration (official Anthropic X post + third-party coverage); the sandbox this
pass ran in could not directly fetch anthropic.com to quote it. The five entries
added 2026-08-10 (Osmani's Agentic Autonomy Levels, Hashimoto's harness-engineering
origin post, Fowler's harness-engineering series, and the "Debt Behind the AI Boom"
arXiv paper) were confirmed live via web search corroboration only — this run's
sandbox had no route to mitchellh.com, martinfowler.com, addyosmani.com, or
arxiv.org (network egress policy blocked each with a 403), and youtube.com was
blocked outright, so no video search or transcript pull ran this pass. Every fact
above is paraphrased from search-engine summaries rather than quoted from a
directly-fetched page; nothing is presented as a verbatim quote. The three entries
added 2026-08-12 (Horthy's HumanLayer talk and Osmani's Light and Dark / Own the
Outer Loop posts) hit the same wall — this pass's sandbox had no route to
addyosmani.com, arxiv.org, or any of the pages hosting the Horthy talk
(daily.dev, finance.biggo.com), and youtube.com was blocked outright — so all
three are confirmed live via web search corroboration only, cross-checked against
multiple independent search results per claim. One number initially surfaced for
the Horthy talk (a specific incident-rate percentage across a named developer
count) could not be corroborated on a second, differently-worded search and is
deliberately not repeated below — only the qualitative outcome (dark-factory run,
codebase degraded, project rebuilt) that multiple independent sources agree on.
The two arXiv papers added 2026-08-14 (the Microsoft CLI-agent rollout study and
the developer-agent misalignment study) hit the same wall from the other side:
this pass's sandbox egress proxy blocked `arxiv.org` outright (`EGRESS_BLOCKED`),
and `youtube.com` was blocked outright too, so neither paper's PDF/HTML was
directly read and no video search ran this pass. Both papers' figures below are
paraphrased from multiple independent, differently-worded search results that
themselves quote the papers' own abstracts — not from a directly-fetched page —
cross-checked the same way the three entries above were.

---

## Foundations — how LLMs & neural nets actually work

### [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy)
Ex-OpenAI founding member and former Tesla AI director. Teaches LLMs and neural
nets from first principles in code (the *Neural Networks: Zero to Hero* series) —
the gold standard for understanding what's actually happening under the hood.
- [The spelled-out intro to neural networks and backpropagation: building micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0)
- [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- [[1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- [Deep Dive into LLMs like ChatGPT (3h31m)](https://www.youtube.com/watch?v=7xTGNNLPyMI)

### [3Blue1Brown](https://www.youtube.com/@3blue1brown)
Grant Sanderson's visual-math channel. The *Deep Learning* series gives the
clearest visual intuition available for neural nets, transformers, and attention.
- [But what is a neural network? | Deep Learning Chapter 1](https://www.youtube.com/watch?v=aircAruvnKk)
- [But what is a GPT? Visual intro to transformers | Chapter 5](https://www.youtube.com/watch?v=wjZofJX0v4M)
- [Attention in transformers, visually explained | Chapter 6](https://www.youtube.com/watch?v=eMlx5fFNoYc)

### [Yannic Kilcher](https://www.youtube.com/@YannicKilcher)
ETH Zurich ML PhD. Deep, critical, full read-throughs of cutting-edge ML/LLM
research papers plus ML news — the go-to for the actual papers behind the hype.

### [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers)
Dr. Károly Zsolnai-Fehér's short, enthusiastic summaries of new AI/ML/graphics
research — stay aware of the frontier without reading every paper.

---

## Technique — AI-assisted coding & agentic dev

### [Matt Pocock](https://www.youtube.com/@mattpocockuk)
Full-time TypeScript educator (Total TypeScript) now focused on real-engineering
AI-assisted coding via AI Hero — Claude Code workflows, skills, and agentic dev
for professional engineers ("we don't do vibe coding").
- [Claude Code: Master Multi-Phase AI Coding Plans](https://www.youtube.com/watch?v=_gNgJiICLzs)
- [TypeScript Crash Course with Matt Pocock](https://www.youtube.com/watch?v=p6dO9u0M7MQ)

### [Anthropic](https://www.youtube.com/@anthropic-ai)
Official Anthropic channel — Claude product launches, Claude Code, agent-building
best practices, and the *Code with Claude* event sessions.
- [Claude Code best practices | Code w/ Claude](https://www.youtube.com/watch?v=gv0WHhKelSE)

### [Cole Medin](https://www.youtube.com/@ColeMedin)
Weekly hands-on tutorials on building AI agents and using AI coding assistants
that scale to production — Plan-Implement-Validate methodology, context
engineering, and the open-source Archon project.

### [Fireship](https://www.youtube.com/@Fireship)
Jeff Delaney's high-energy, fast-paced dev channel ("X in 100 Seconds" + same-day
breakdowns of new AI models/tools). Great for quick, opinionated orientation on
new AI tech.

### [IndyDevDan](https://www.youtube.com/@indydevdan)
Weekly agentic-engineering builds with a consistent thesis — *"agents plus code
beats agents alone"*: composable AI Developer Workflows with deterministic gate
checks between agent steps and validated JSON handoffs, rather than piling
everything into skills.
- [My Super Simple Software Factory (For Agentic Engineers)](https://www.youtube.com/watch?v=haUfb1ievTE)

### [Owain Lewis](https://www.youtube.com/@owainlewis)
Working demos of ticket→spec→worktree→implement→review→merge pipelines, run
live. Label-driven stages, worktree-per-run isolation, and scheduled jobs that
*open tickets* rather than merging.
- [I Built an Agentic Software Factory with Codex and Claude Code](https://www.youtube.com/watch?v=AbpyqAfxZ8c)

### [Agentic Development — Ben Fellows](https://www.youtube.com/@benfellows-dev)
The dissent worth keeping: generic agentic "factories" failed him, and the
alternative is bespoke per-repo pipelines built from shared blocks, plus
policy-as-code as a pre-test gate. *"There's a reason why Ford doesn't build
every one of their cars in one factory."*
- [I Tried Building with Agentic Factories. They Failed. Here's What Worked Instead.](https://www.youtube.com/watch?v=mREHBZQbhBo)

### [Zen van Riel](https://www.youtube.com/@zenvanriel)
Agentic engineering with a review-queue reality check — four effort-tiered
parallel agents rather than fifty, worktrees for real parallelism, and an honest
30–60% productivity number instead of a 5× claim. Skeptical by default of
methodology branding that hasn't survived three to four months.
- [The Agentic Engineer Workflow You Need In 2026](https://www.youtube.com/watch?v=ElYxdpYi4U0)

---

## Concepts — explainers for mixed-skill teams

### [IBM Technology](https://www.youtube.com/@IBMTechnology)
IBM's official educational channel — clean 5–10 minute whiteboard explainers on
RAG, AI agents, MCP, LLMs, embeddings, and model evaluation. Excellent for
sharing a concept with a mixed-skill team.
- [What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=qppV3n3YlF8)
- [RAG vs Agentic AI: How LLMs Connect Data for Smarter AI](https://www.youtube.com/watch?v=fB2JQXEH_94)
- [AI in the SDLC: Rethinking AI Coding Tools & AI Agents](https://www.youtube.com/watch?v=4wMRXmLpdA8)

---

## Production — applied talks & podcasts (the outer loop)

### [AI Engineer](https://www.youtube.com/@aiDotEngineer)
The conference channel (AI Engineer Summit / World's Fair / Code Summit) —
production-AI talks and workshops from engineers at Anthropic, OpenAI, Google
DeepMind, Cursor, Cognition, and more. Among the best for applied AI engineering.
- [How We Build Effective Agents — Barry Zhang, Anthropic](https://www.youtube.com/watch?v=D7_ipDqhtwk)
- [Don't Build Agents, Build Skills Instead — Barry Zhang & Mahesh Murag, Anthropic](https://www.youtube.com/watch?v=CEvIs9y1uog)
- [Claude Code & the evolution of agentic coding — Boris Cherny, Anthropic](https://www.youtube.com/watch?v=Lue8K2jqfKk)
- [Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic](https://www.youtube.com/watch?v=TqC1qOfiVcQ)
- [Building your own software factory — Eric Zakariasson, Cursor](https://www.youtube.com/watch?v=rnDm57Py54A) — the levels-of-autonomy ladder, and the primitives/guardrails/enablers/environment checklist for building one on a team
- [Harness Engineering is not Enough: Why Software Factories Fail — Dex Horthy, HumanLayer](https://www.youtube.com/watch?v=Ib5GBkD555M) — counter-evidence to the dark-factory pitch, from someone who ran one: Horthy (HumanLayer's founder) describes a "lights-off" factory he ran roughly July–November 2025 where agents wrote, reviewed, and merged code with no human reading any of it; within a few months a single bug took weeks of human debugging to trace through code nobody had ever read, and the project was shut down and rebuilt. His stated reason coding agents degrade a codebase this way: they're rewarded for passing tests, not for preserving design quality, and maintainability has no fast oracle a training loop can reward. The prescription is the opposite of dark-factory: keep humans reading code, and move planning/architecture review earlier rather than eliminating oversight at the end.

### [Arize AI](https://www.youtube.com/@arizeai)
The Observe conference channel — AI observability and evaluation talks, with the
enterprise end of agentic delivery well represented.
- [From AI Coding Agents to the Software Factory — Eno Reyes, Factory AI](https://www.youtube.com/watch?v=SkoT4RkteSA) — agent-readiness grading, and the finding that level 1–2 codebases *decelerate* delivery

### [Latent Space](https://www.youtube.com/@LatentSpacePod)
swyx (Shawn Wang) and Alessio Fanelli's podcast "by and for AI Engineers" —
interviews with founders and builders from across the AI tooling space.
- [The Rise of the AI Engineer (swyx)](https://www.youtube.com/watch?v=yj2Bm_XYOVs)

---

## Web resources & reading

Non-video learning references — curated sites and benchmarks, not catalogued tools.

### [The Loop Library](https://signals.forwardfuture.com/loop-library/) — Forward Future
~70 copy-paste AI-agent "loops" — bounded workflows with explicit success criteria,
stopping conditions, and verification — organized into Engineering, Evaluation,
Operations, Design, and Content. A practical companion to this repo's dev-loop
framing in [WORKFLOW.md](WORKFLOW.md) and the `/loop` skill. Its recurring design
principles are a good checklist for writing your own loops:
- **Explicit terminal states** — every loop defines when to stop (success metric or budget), so agents don't run forever.
- **Verification-first** — regression-test and compare against a baseline before committing.
- **Approval gates** — human sign-off for production changes and irreversible actions.
- **Composable small steps** — combine verified increments instead of one large transformation.
- **Measurable progress** — track coverage %, latency ms, test passes for objective completion.
- **Isolation & idempotence** — disposable environments / fresh clones to avoid state contamination.

### [Terminal-Bench 2.0 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0)
Benchmark ranking AI coding agents/harnesses on real terminal tasks, scored as
model + harness pairings with uncertainty margins. Useful for tracking which
harness/model combinations currently lead on agentic terminal work when deciding
what to adopt. *The leaderboard is live and shifts often — check current standings
rather than trusting a snapshot.*

### [Comprehension Debt — the hidden cost of AI-generated code](https://addyosmani.com/blog/comprehension-debt/) — Addy Osmani
Names and quantifies the failure mode this repo's [Verifiability quality
signal](WORKFLOW.md#why-verifiability-is-its-own-signal) is built to catch: teams
generating code faster than anyone can understand it. Cites convergent findings
from multiple 2026 research groups that AI coding tools produce code 5-7x faster
than developers can review it, and that PR volume rising alongside a rising
incident rate per PR is a signal standard velocity metrics miss entirely — it
shows up 6-18 months later as code nobody can confidently modify. Useful as the
named-concept companion to the Verifiability rationale already in `WORKFLOW.md`.

### [Agentic Autonomy Levels](https://addyosmani.com/blog/agentic-autonomy-levels/) — Addy Osmani
Published 2026-07-03. A different shape than the autonomy ladders already read into this
repo's own [software-factory-field-notes.md](methodologies/software-factory-field-notes.md)
(Zakariasson's six stages, Reyes's three ages) and
[bushido-ai-dlc-2026.md](methodologies/bushido-ai-dlc-2026.md)'s per-Unit HITL/OHOTL/AHOTL
mode selector: Osmani frames scaling autonomy as expansion along
orthogonal directions rather than a single rung to climb — starting from one supervised agent
on one scoped task, then outward into parallel read-heavy exploration, separate write agents on
their own worktrees, and recurring automations/agent-led orchestration. Each expansion is paired
with the new failure mode it opens (context rot on longer runs, stale assumptions from
background work, merge conflicts from parallelism, silent token spend from recurring jobs)
rather than presented as pure upside. Same author as the Comprehension Debt post above.

### [Software Factories, Light and Dark](https://addyosmani.com/blog/software-factories/) — Addy Osmani
Published 2026-07-22. Names the deliberate counterpart to "dark factory" (Dan Shapiro's January
2026 term for the top rung of his five-level autonomy ladder — the same ladder Zakariasson
attributes to Shapiro in
[`software-factory-field-notes.md`](methodologies/software-factory-field-notes.md#eric-zakariasson-cursor--the-ladder-the-checklist-and-the-silo-problem)):
a **lit factory** is the same agent-run pipeline with the lights left on wherever judgment lives —
not review tacked onto the end, but human judgment moved upstream into design and architecture
before an agent starts a loop. Its central claim is that the binding constraint on a factory is
not how much code can be produced but how quickly it can be verified — independently reaching this
repo's own [Verifiability](WORKFLOW.md#why-verifiability-is-its-own-signal) rationale and rule 8 of
[`software-factories.md`](methodologies/software-factories.md#the-ideal-workflow)'s ideal workflow.
Same author as the two Osmani entries above.

### [Own the Outer Loop](https://addyosmani.com/blog/own-the-outer-loop/) — Addy Osmani
Published 2026-07-09 as the written form of Osmani's AI Engineer World's Fair 2026 closing
keynote. Uses this repo's own inner/outer-loop vocabulary for an accountability model: agents run
the **inner loop** (investigate, implement, test, report); the engineer owns the **outer loop** —
deciding whether the work is worth doing, verifying the evidence (diffs, tests, logs, a short
why), rendering a verdict (ship, block, redirect, add a guardrail), and staying answerable for it.
Cites a trust gap as the reason this matters: roughly 96% of developers say they don't fully trust
AI-generated code, but only about 48% say they always verify before committing — skepticism
running well ahead of verification in practice, the same gap the Comprehension Debt entry above
names from the volume side.

### [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Anthropic Engineering
Official Anthropic engineering post on building harnesses for agents that work across many
sessions with no memory of what came before. Frames a harness as encoded assumptions about what
the model can't yet do alone, and describes a GAN-inspired multi-agent structure — a generator and
an evaluator agent dividing planning, generation, and evaluation to hold coherence over multi-hour,
multi-session runs (demonstrated on autonomous frontend design and application development).
Directly on-topic for this repo's "harness engineering" framing and cited as a foundational
influence by [`bushido-ai-dlc-2026.md`](methodologies/bushido-ai-dlc-2026.md)'s own attribution
section, which is how this pass found it.

### [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) — Mitchell Hashimoto
Published 2026-02-05. The originating post for "harness engineering" and the formula this
repo's own vocabulary assumes without ever naming its source — **Agent = Model + Harness**.
Hashimoto (HashiCorp co-founder, Terraform/Ghostty) describes a practice: every time an agent
is caught making the same category of mistake, engineer a permanent fix into its environment
(a rule in `CLAUDE.md`/`AGENTS.md`, a guard script, a changed default) rather than re-prompting
around it each time. The term and formula spread widely enough in the months after that the
Martin Fowler piece below credits it as the starting point.

### [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) — Martin Fowler
The most substantive practitioner treatment of harness engineering found this pass, from a
source with no product to sell — part of a longer
[exploring-gen-ai series](https://martinfowler.com/articles/exploring-gen-ai/) that also
includes ["Maintainability sensors for coding agents"](https://martinfowler.com/articles/sensors-for-coding-agents.html)
and ["Humans and Agents in Software Engineering Loops"](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html).
Frames a harness as everything around an agent except the model itself, built from **guides**
and **sensors** (computational or inferential) that a team can share as templates across a
codebase. Its sharpest claim: a good harness should not aim to eliminate human input but to
direct it to where it matters most, and a harness regulates three dimensions — maintainability,
architecture fitness, and functional behavior, the last of which it calls the hardest unsolved
problem. Complements rather than duplicates the Anthropic post above: that one is a single
company's internal architecture for long-running agents, this is the vendor-neutral vocabulary
for the discipline this repo's own `CLAUDE.md` already calls "harness engineering" throughout
its integrity-tooling section.

### [State of AI vs. Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) — CodeRabbit
A measured comparison (not a vendor claim) of 470 real open-source pull requests
(320 AI-coauthored, 150 human-only): AI-generated code averaged 1.7x more issues
per PR than human-written code, with security vulnerabilities up to 2.74x higher
and logic/correctness issues 75% more common. The most concrete evidence found
this pass for why unreviewed AI output is the wrong default — it's a data point
for the Verifiability signal's premise, not a reason to distrust AI coding tools
outright; the gap is exactly what review process closes.

### ["Debt Behind the AI Boom": A Large-Scale Empirical Study of AI-Generated Code in the Wild](https://arxiv.org/abs/2603.28592) — Yue Liu, Ratnadira Widyasari, Yanjie Zhao, Ivana Clairine Irsan, David Lo (arXiv, 2026-03)
A far larger version of the CodeRabbit claim above, on public data rather than a vendor sample:
304,362 verified AI-authored commits across 6,275 GitHub repositories from five AI coding
assistants, with before/after static analysis run on each commit to attribute exactly which
code smells, bugs, and security issues the AI introduced, then tracked forward to the latest
repository revision. Findings: more than 15% of commits from every tool studied introduce at
least one issue (code smells are 89.1% of the total); **24.2% of AI-introduced issues are still
present at the latest observed revision** — not caught, not fixed, not a burst that gets cleaned
up later. The paper's own framing is persistent technical debt rather than transient defects
that review naturally clears. The strongest counter-evidence found this pass, and exactly the
failure mode [Verifiability](WORKFLOW.md#why-verifiability-is-its-own-signal) exists to catch —
worth weighing against this repo's own optimism about review closing the gap.

### [Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI](https://arxiv.org/abs/2607.01418) (arXiv, 2026-07)
The first field study to use developer-level telemetry to measure both adoption and productivity
impact of agentic CLI coding tools — Claude Code and GitHub Copilot CLI, specifically — inside one
large engineering organization: tens of thousands of Microsoft engineers over a roughly four-month
rollout window. Findings: first use spread mainly through social/team networks rather than
top-down mandate; retention tracked with how much an engineer already codes, not with demographics;
and adopters merged roughly **24% more pull requests** than a matched counterfactual (reported
range +14.5% to +33.7%), a gain that held steady across the full four months rather than fading.
The authors ran a placebo check — testing as if the rollout had started earlier than it actually
did — and found no matching jump, a falsification test none of the vendor throughput claims this
repo already treats skeptically (8090's "80x", EY's "70%" — see
[`software-factories.md`](methodologies/software-factories.md)) ever run. Directly on point for the
practitioner-vs-vendor number gap
[`software-factory-field-notes.md`](methodologies/software-factory-field-notes.md#where-they-disagree--and-which-side-to-take)
tracks: a telemetry-grounded number sitting between van Riel's 30–60% estimate and the vendor
multiples, and — unlike either — measured on Claude Code itself rather than on a comparable tool.

### [How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions](https://arxiv.org/abs/2605.29442) (arXiv, 2026-05)
Counter-evidence to weigh against the productivity number above, from the same evidence class —
real telemetry, not a vendor benchmark. An observational study (Notre Dame, Vanderbilt, and Google,
per the paper's own listing) of 20,574 coding-agent sessions across 1,639 repositories, spanning
both IDE and CLI workflows. It operationalizes "misalignment" as any breakdown made visible through
developer pushback and reports seven recurring forms — spanning how an agent reads a project,
interprets developer intent, follows stated rules, bounds its own actions, implements and executes
code, and reports its own progress. Most episodes (reported 90.50%) cost effort and trust rather
than causing irreversible damage, but the reported **91.49%** of visible resolutions still needed
an explicit user correction — verification is not an occasional fallback here, it is the default
path back to a working state. Overall misalignment rates reportedly decline session-over-session,
but constraint violations and inaccurate self-reporting reportedly *grow* in share even as the
total shrinks — a shift a raw incident-rate trend line would hide. This is squarely the evidence
this repo's [Verifiability signal](WORKFLOW.md#why-verifiability-is-its-own-signal) and the
Comprehension Debt / Own the Outer Loop entries above already argue for: the failure mode is not
agents going rogue, it is agents needing a human to keep catching the same shapes of mistake.

---

*Suggest additions or fixes via PR. Keep entries developer-focused, verify links
resolve before adding, and prefer a stable channel/site link over a video that may
be taken down.*
