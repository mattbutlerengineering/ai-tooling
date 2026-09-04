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

**Last verified:** 2026-08-31 (this pass's addition, confirmed via search corroboration; see the
dated footnote below for what else was checked). The rest of the page was previously verified
2026-08-05 — the six software-factory channels and talks added
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
cross-checked the same way the three entries above were. The AGENTS.md entry
added 2026-08-17 hit the identical wall — `arxiv.org` and `youtube.com` both
`EGRESS_BLOCKED` again — so both papers' figures below are likewise paraphrased
from independent search summaries quoting each paper's own abstract, cross-checked
against each other rather than read directly. The Shen & Tamkin skill-formation entry
added 2026-08-19 hit the same wall a third time (`arxiv.org` and `anthropic.com` both
`EGRESS_BLOCKED`, and `youtube.com`/`asdlc.io` too — no video search or transcript pull
ran this pass either), so its figures are likewise cross-checked across multiple
independent search summaries rather than read from the source. This pass also looked at
[ASDLC.io](https://asdlc.io/concepts/agentic-sdlc/) (villetakanen/asdlc-io, ★30) as a
possible new methodology mapping and declined it — a single-maintainer project well
below the bar 8090's Software Factory and AWS's AI-DLC set for a `methodologies/` doc.
The Faros AI "Acceleration Whiplash" entry added 2026-08-21 hit the same wall a fourth
time — `youtube.com` was blocked outright again (no video search ran), and both
`faros.ai` and the report's own `pages.faros.ai` PDF host returned `EGRESS_BLOCKED`, so
its figures are cross-checked across multiple independent third-party write-ups agreeing
on the same numbers rather than read from the report directly. This pass also checked a
search-engine claim of an AWS AI-DLC "Workflow 2.0" release dated 2026-08-14 directly
against `awslabs/aidlc-workflows`'s own GitHub releases page (reachable this pass) and
found no such release — the newest tag there is v1.0.1 — so nothing was added on that
lead; it was a search-summary artifact, not a real update. The 2026-08-24 pass re-checked
that same claim and found it partly right this time — see the dated update in
[`aws-ai-dlc.md`](methodologies/aws-ai-dlc.md) — confirmed by fetching
`awslabs/aidlc-workflows`'s own `main` and `v2` branch files directly rather than from
search summaries; `github.com`/`raw.githubusercontent.com` were the only domains this
pass's sandbox could reach. `arxiv.org`, `youtube.com`, `metr.org`, and every third-party
write-up site tried (scienceblog.com, letsdatascience.com, particula.tech, aiboffinhub.com,
valueaddvc.com, startuphub.ai, finance.biggo.com) returned `EGRESS_BLOCKED`. The two METR
entries added this pass are therefore cross-checked across multiple independent
search-engine summaries of METR's own two blog posts rather than read from the posts
directly — every figure below appeared consistently across at least two independently-
worded summaries. This pass also found a well-documented account of Uber's "Managed
Software Factory" (Uday Kiran Medisetty and Adam Huda, reportedly at AI Engineer World's
Fair) and declined to add it: every source describing it in enough detail to write an
honest entry — the talk itself and every third-party write-up found — sat on a domain this
pass could not reach, so no resolvable primary URL could be confirmed. The 2026-08-26 pass
hit the identical wall a fifth time — `youtube.com` was blocked outright at the proxy level
(not just individual videos, confirmed via a bare `ytsearch3:test` query), and `arxiv.org`,
`openai.com`, `developers.openai.com`, `alphaxiv.org`, and `newsletter.port.io` all returned
`EGRESS_BLOCKED` — so the two entries added this pass (the CMU code-review study and the
OpenAI harness entries below) are cross-checked across multiple independently-worded search
summaries rather than read from source, the same standard applied throughout this page. This
pass re-checked the Uber "Managed Software Factory" lead once more (a newsletter.port.io
write-up looked promising) and hit the same unreachable-domain wall as before — still
declined, for the same reason. `awslabs/aidlc-workflows`'s `v2` branch has not merged to
`main` since the 2026-08-24 update in [`aws-ai-dlc.md`](methodologies/aws-ai-dlc.md), so
that doc needed no further change this pass. The 2026-08-28 pass re-checked that repo directly
(cloned `main` read-only rather than via search) and confirmed it: the newest commit is a
2026-08-27 issue-template tweak ("mark v2 current in issue forms"), `v2` is still an unmerged
branch, and `main`'s own README still reads, verbatim, *"🟡 OPERATIONS PHASE — Deployment and
monitoring (future)"* — no material change since the 2026-08-24 note. This pass hit the same
egress wall a sixth time — `youtube.com` was blocked at the proxy level again (a bare
`ytsearch3:test` yt-dlp query failed with a 403 on the CONNECT tunnel, confirmed independently via
a direct `curl` to both `youtube.com` and `arxiv.org`), so no video search or transcript pull ran.
The three entries added this pass (the Galster configuration-adoption census, the Lahiri
intent-formalization paper, and the Qwen Team verification-horizon paper) are therefore
cross-checked across multiple independently-worded search summaries rather than read from source,
the same standard applied throughout this page. This pass also re-surfaced StrongDM's February
2026 "dark factory" write-up (the origin of the term this page's Osmani and Horthy entries already
discuss at length) and declined it — six months old, and it adds no claim beyond what those two
entries already cover. The 2026-08-31 pass hit the identical egress wall a seventh time — a bare
`ytsearch3:test` yt-dlp query failed with a 403 on the CONNECT tunnel and a direct `curl` to both
`youtube.com` and `arxiv.org` failed identically, so no video search or transcript pull ran and the
one entry added this pass (below) is cross-checked across independently-worded search summaries
rather than read from source. `github.com` and `raw.githubusercontent.com` were reachable this pass
(same as 2026-08-24/2026-08-28), so `awslabs/aidlc-workflows` was re-checked directly by cloning
`main` read-only rather than via search: `main`'s HEAD (`af650cf9`, 2026-08-29) still carries the
same "Announcing 2.0 (GA)" banner first noted on 2026-08-24, the `v2` branch is still separate and
unmerged, and the `OPERATIONS PHASE` section on `main` is still, verbatim, *"Deployment and
monitoring (future)"* — no material change since the 2026-08-28 note, so nothing was added on that
thread this pass. This pass also found a Mercari GEARS 2025 talk ("Specs to Code with Coding
Agents: Where Do Engineers Come In?") on one team's spec-driven-development experience and declined
it — the only public record is a slide deck, not text that can be quoted verbatim, and its own
finding (generated code matched spec but needed heavy refactoring to become "good" code) is a single
team's anecdote rather than a measured result, unlike the entries already on this page.
The 2026-09-04 pass hit the identical egress wall an eighth time — a bare `ytsearch3:test`
yt-dlp query failed with a 403 on the CONNECT tunnel and the agent-proxy's own status endpoint
recorded `connect_rejected` CONNECT failures for `www.youtube.com`, `arxiv.org`,
`martinfowler.com`, and `addyosmani.com` alike — so no video search or transcript pull ran, and
the four entries added this pass (two Anthropic research posts, an Anthropic engineering
postmortem, and a Universidad Politécnica de Madrid spec-driven-development paper) are
cross-checked across multiple independently-worded search summaries rather than read from
source, the same standard applied throughout this page. `github.com` and
`raw.githubusercontent.com` were reachable this pass (via a read-only `git clone`, the same path
used since 2026-08-24), so `awslabs/aidlc-workflows` was re-checked directly rather than via
search: `main`'s HEAD is unchanged at `a277af2`, the exact commit
[`aws-ai-dlc.md`](methodologies/aws-ai-dlc.md)'s 2026-09-02 update already confirmed, so nothing
further was added on that thread this pass. This pass also found `ai-boost/awesome-harness-engineering`,
a curated list of harness-engineering tools, patterns, and evals — plausibly worth a
discovery-lane look, named here rather than added, since a `CATALOG.md` row is outside this
lane's scope.

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

### [Codex as a platform: build on the open agent harness](https://developers.openai.com/blog/codex-as-a-platform) — OpenAI (2026-08-19)
A second major lab's production answer to the same discipline the Hashimoto/Fowler/Anthropic
cluster above documents — and, unlike those three, an artifact rather than only prose: OpenAI
open-sourced the Codex Harness core execution engine under Apache-2.0 (`codex exec`, the Codex
SDK, and the `app-server` execution loop), explicitly framing the harness — not the chat
interface — as Codex's most valuable reusable asset. Its own description matches Fowler's
framing closely: the harness "gathers context, invokes tools, enforces sandbox and approval
boundaries, streams execution progress, and carries work across multi-turn sessions." Its
companion essay from earlier the same year,
[Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
(2026-02), makes the concrete claim this repo's own harness-engineering framing has otherwise
only asserted in the abstract: a five-month internal effort shipped a production beta of
roughly one million lines of code with zero lines typed by a human, the team's own account
being that they spent the effort building the *harness* — rules, feedback loops, doc structure,
dependency ordering — rather than typing code directly. Worth reading as evidence the term and
formula (`Agent = Model + Harness`) have moved from one company's internal vocabulary
(Hashimoto) through vendor-neutral treatment (Fowler) to a second frontier lab's shipped,
open-sourced infrastructure — not merely more marketing language reusing the term. Confirmed
via multiple independent write-ups agreeing on the same facts (Open Source For You, BigGo
Finance, kenhuangus Substack, note.com) rather than a direct fetch — this pass's sandbox
blocked both `openai.com` and `developers.openai.com` outright (`EGRESS_BLOCKED`).

### [State of AI vs. Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) — CodeRabbit
A measured comparison (not a vendor claim) of 470 real open-source pull requests
(320 AI-coauthored, 150 human-only): AI-generated code averaged 1.7x more issues
per PR than human-written code, with security vulnerabilities up to 2.74x higher
and logic/correctness issues 75% more common. The most concrete evidence found
this pass for why unreviewed AI output is the wrong default — it's a data point
for the Verifiability signal's premise, not a reason to distrust AI coding tools
outright; the gap is exactly what review process closes.

### [AI Engineering Report 2026: The Acceleration Whiplash](https://pages.faros.ai/hubfs/AI_Engineering_Report_2026_The_Acceleration_Whiplash_Faros.pdf) — Faros AI (2026-03)
Two years of telemetry — not survey data — from 22,000 developers across 4,000+ teams on the Faros
platform, comparing each organization's own low-AI-adoption periods against its high-AI-adoption
periods (a within-org before/after design, pulled from task trackers, IDEs, static analysis, CI/CD,
version control, and incident-management systems, not a cross-org sample or a self-reported survey).
Findings: task completion per developer up 34%, epics completed per developer up 66% — genuine
throughput gains — while bugs per developer rose 54%, the incident-to-PR ratio more than tripled
(~243%), median PR review time rose roughly 5x (441.5%), and code churn rose 861%. Read against the
throughput half, this is the sharpest telemetry-scale illustration yet of the trade this repo's
[Verifiability signal](WORKFLOW.md#why-verifiability-is-its-own-signal) exists to catch: the same
adoption that raises delivery volume degrades the review and stability signals in lockstep, at a
scale (22K developers, real production incidents, two years of within-org comparison) well past the
470-PR CodeRabbit sample and the commit-level "Debt Behind the AI Boom" study below. Confirmed via
multiple independent write-ups agreeing on the same figures (ADTmag, Refactoring/Luca Rossi, Jim
Nielsen's Notes, Vibe Graveyard) rather than a direct fetch — this pass's sandbox blocked both
`faros.ai` and the `pages.faros.ai` PDF host outright (`EGRESS_BLOCKED`), so the numbers above are
cross-checked across independent summaries rather than read from the report itself.

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

### [How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245) — Judy Hanwen Shen, Alex Tamkin (Anthropic; arXiv, 2026-02)
A randomized controlled trial, and notably an Anthropic-authored study testing a **competitor's**
model rather than Claude — 52 professional developers worked through a warm-up, then two coding
tasks in Trio (an async Python library new to all of them), then a comprehension quiz; half had
a GPT-4o assistant available, half did not. Developers who used the assistant scored **17
percentage points lower** on the comprehension quiz (50% vs. 67%) and finished the coding tasks
**no measurably faster** — the productivity trade-off the Comprehension Debt entry above assumes
didn't appear in this design at all; AI use cost understanding without buying speed. The sharper
finding is the one worth acting on: the paper identifies **six distinct AI-usage patterns**, and
learning outcome tracks *engagement*, not AI use itself — developers who stayed cognitively
engaged (asking the assistant for explanations, verifying its output before accepting) retained
the skill; those who delegated passively learned almost nothing. Directly on point for this
repo's own [Verifiability signal](WORKFLOW.md#why-verifiability-is-its-own-signal): it is
controlled evidence, from the model vendor's own research org, that unreviewed delegation is a
specific failure mode with a specific fix (stay engaged, treat the assistant as a tutor rather
than an answer machine) rather than an unavoidable cost of AI-assisted coding. Confirmed via
search corroboration only — this pass's sandbox blocked both `arxiv.org` and
`anthropic.com` outright (`EGRESS_BLOCKED`), so neither the paper nor Anthropic's own research
post was directly fetched; the design and figures above are cross-checked across Anthropic's own
post title, the arXiv listing, and multiple independent third-party summaries agreeing on the
same 52-developer/Trio/17-point figures.

### [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988) — Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev (ETH Zurich; arXiv, 2026-02)
Counter-evidence against a practice this repo's own harness-engineering entries above treat as
settled — Hashimoto's *"engineer a permanent fix into its environment (a rule in
`CLAUDE.md`/`AGENTS.md`... rather than re-prompting around it each time)"*. This study built
AGENTBENCH (138 real-world Python SWE tasks from niche repositories) plus SWE-bench tasks
carrying LLM-generated context files, and tested both LLM-generated and developer-committed
`AGENTS.md` files across multiple LLMs and coding agents. Finding: repository-level context files
do not generally improve task success rate — they measurably *reduce* it in the niche-repository
setting — while increasing inference cost by over 20% on average, holding across models and
agents. That directly contradicts a same-cluster study published three weeks earlier,
[Lulla et al., "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents"](https://arxiv.org/abs/2601.20404)
(arXiv, 2026-01), which ran agents with and without an `AGENTS.md` across 124 pull requests in 10
repositories and found the opposite on cost — a lower median runtime (Δ28.64%) and reduced output
token consumption (Δ16.58%) — with comparable task completion. Two controlled studies, three weeks
apart, disagreeing on both the sign of the cost effect and the direction of the success-rate
effect: the practice of writing a durable agent-instructions file is still a genuinely open
empirical question, not the settled win this repo's own harness-engineering reading currently
implies. Worth weighing the next time `CLAUDE.md` itself is treated as an unqualified good rather
than a cost this repo has never measured against a no-`CLAUDE.md` baseline.

### [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR (2025-07-10)
A randomized controlled trial — real day-to-day issues in developers' own mature open-source
repositories, not a synthetic benchmark — that became one of the most-cited pieces of
counter-evidence in the AI-coding-productivity debate: experienced developers allowed to use AI
tools (mainly Cursor Pro with Claude 3.5/3.7 Sonnet) completed their tasks reportedly **19%
slower** than a matched control group working without AI, even though the same developers
predicted beforehand they'd be roughly 24% faster and, after finishing, still estimated they'd
been roughly 20% faster — a self-perception gap running the opposite direction from the measured
result. Directly on point for this repo's own [Verifiability
signal](WORKFLOW.md#why-verifiability-is-its-own-signal): a controlled study finding that trust in
AI assistance and its actual effect can point in opposite directions, in the same population, on
the same tasks.

### [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/) — METR (2026-02-24)
METR's own follow-up, worth reading against the 2025-07-10 entry above rather than in isolation.
Continuing the same style of trial into 2026 reportedly surfaced **selection effects that
undermined the randomization itself**: developers grew reluctant to be assigned to the no-AI
condition, and some avoided submitting tasks they specifically wanted AI's help with — so the
tasks and people most likely to show an AI benefit were increasingly missing from the "with AI"
arm by design, not by chance. Revisiting the same developer cohort under a revised design, METR
reportedly now estimates roughly **18% faster** with AI — but with a confidence interval of
**-38% to +9%**, still wide enough to include no effect or a slowdown. METR's own explanation for
the roughly 37-point swing in seven months is that both the tools and developers' skill using them
improved — not that the original RCT was wrong, but that a clean randomized estimate of "AI
coding uplift" gets harder to hold onto the longer developers have had access to what's being
measured. Read together, the two posts are the strongest documented case that a single
productivity RCT — however rigorous — is a point-in-time snapshot, not a settled number; worth
weighing against this repo's own habit of citing a study's headline percentage without dating how
fast the ground under it moves.

### [3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse](https://arxiv.org/abs/2607.07980) — Shyam Agarwal, Courtney Miller, Christian Kästner, Bogdan Vasilescu (CMU; arXiv, 2026-07)
Directly on point for this repo's [Verifiability signal](WORKFLOW.md#why-verifiability-is-its-own-signal)
and a useful caution against several of the single-number repo-mining stats cited elsewhere on
this page. Rather than one more measurement of "does AI help or hurt code review," the authors
collect 38,709 grey-literature documents about code review (7,630 web articles, 31,079 Reddit
threads), LLM-code a stratified sample of 3,100, and build a falsifiable causal theory — named
constructs and moderators — out of where practitioners agree and sharply disagree on whether
review becomes the bottleneck, whether human review is still necessary, and whether AI quietly
erodes the understanding review used to build. The paper's own motivating example is the sharpest
part: an observational analysis of public GitHub activity finds agent-authored pull requests are
reviewed less often, merged several times faster, and discussed less than human-authored ones —
and then reports that **the direction of every one of those trends flips under different but
equally defensible analysis choices**. That is not a result this repo should copy as a headline
number; it is a warning that a simple PR-mining metric (the same shape as several other findings
cited on this page) can point either way depending on decisions an author makes without noticing
they're decisions. Confirmed via multiple independently-worded search summaries converging on the
same methodology and the same abstract phrasing — this pass's sandbox blocked `arxiv.org` outright
(`EGRESS_BLOCKED`), so the paper itself was not directly read.

### [Configuring Agentic AI Coding Tools: An Exploratory Study](https://arxiv.org/abs/2602.14690) — Matthias Galster, Seyedmoein Mohsenimofidi, Jai Lal Lulla, Muhammad Auwal Abubakar, Christoph Treude, Sebastian Baltes (arXiv, 2026-02; accepted AIware 2026)
The adoption census the two AGENTS.md efficacy studies above (Gloaguen et al. and Lulla et al.)
run without one — not whether a context file helps, but whether anyone actually writes one, and
which of the richer mechanisms this repo's own stack layers on top ever get used. Surveys 2,853
public GitHub repositories configuring five agentic coding tools (Claude Code, GitHub Copilot,
Cursor, Gemini, Codex) and catalogs eight configuration mechanisms spanning static context through
executable and external integrations. Adoption counts by repo: Context files 2,586, Settings 290,
Rules 238, Commands 169, **Skills 158**, Subagents 131, MCP 75, Hooks 42 — context files alone
account for the large majority, and every mechanism this repo's own `.claude/skills/` and
`.opencode/plugins/` investment sits in (skills, subagents, hooks) is minority practice by a wide
margin in the wild. One author (Lulla) co-authored the AGENTS.md *efficacy* study already cited
above, which is what makes this a companion rather than a duplicate finding — that paper measures
whether the file helps, this one measures whether it gets written at all, and by very different
denominators for skills/subagents/hooks versus context files. Worth weighing next to this repo's
own bet that skills and hooks (not just a `CLAUDE.md`) are worth the investment. Confirmed via
multiple independent search summaries (the arXiv abstract page, dblp's author listing, the ACM
AIware 2026 proceedings entry) converging on the same repo count and mechanism breakdown — this
pass's sandbox blocked `arxiv.org` outright (`EGRESS_BLOCKED`), and `youtube.com` was blocked at
the proxy level too (a bare `ytsearch3:test` yt-dlp query failed with a 403 on the CONNECT tunnel,
confirmed independently via a direct `curl` to both domains), so no video search ran this pass and
the paper itself was not directly read.

### [Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents](https://arxiv.org/abs/2603.17150) — Shuvendu K. Lahiri (Microsoft Research; arXiv, 2026-03)
Names the mechanism behind the failure mode this repo's Verifiability reading already worries
about from two other angles — Comprehension Debt's volume problem and Own the Outer Loop's trust
gap: the *intent gap* between informal natural-language requirements and precise program
behavior, which the paper argues AI-generated code widens "to an unprecedented scale" rather than
closes, because a model can satisfy an ambiguous instruction in ways its author never considered.
Its proposed fix is a tradeoff spectrum rather than one tool — from lightweight tests that
disambiguate likely misreadings, through full functional specifications suitable for formal
verification, to domain-specific languages from which correct code is synthesized directly —
arguing that whether AI makes software more reliable or merely more abundant turns on which point
on that spectrum a team actually invests in. Directly on point for the spec-driven-development
cluster this repo already maps (`8090-software-factory-sdlc.md`'s PRD/Blueprints stages,
`aws-ai-dlc.md`'s Inception phase): both name a spec artifact as the thing that keeps an agent
honest, and this paper is the formal argument for why that artifact needs to be *checkable*, not
merely readable, to do that job. Confirmed via multiple independent search summaries (the arXiv
abstract, Microsoft Research's own publication listing, the RiSE MSR lab's own blog writeup, all
naming the same single author and submission date) — same egress block as the entry above, so the
paper was not directly read.

### [The Verification Horizon: No Silver Bullet for Coding Agent Rewards](https://arxiv.org/abs/2606.26300) — Binghai Wang et al. (Qwen Team; arXiv, 2026-06)
Counter-evidence to a classical intuition this repo's own Verifiability rationale leans on without
stating it outright — that verifying a solution is easier than producing one. The Qwen Team's own
account is the reverse for today's coding agents: as raw generation ability improved, reliably
verifying what a model produced became the harder problem, because every verifier is only a proxy
for human intent and never the intent itself. The paper frames verification quality along three
axes — scalability (can the signal be produced cheaply at scale), faithfulness (how much of true
intent it reflects), and robustness (resistance to reward hacking as training optimizes against
it) — and argues hitting all three at once is the open problem, testing the claim across four
verifier constructions: a test verifier for general coding tasks, a rubric verifier for frontend
work, the user as verifier for real-world agent tasks, and an automated agent verifier for
long-horizon tasks. Notable as a frontier model lab's own research org stating outright that the
bottleneck has moved from generation to verification — the same claim this repo's Verifiability
signal exists to operationalize, from a source with every commercial incentive to say the
opposite. Confirmed via multiple independent search summaries (the arXiv abstract, the Hugging
Face paper page, EmergentMind's paper summary, all agreeing on the four-verifier structure and
three-axis framing) — same egress block as the two entries above, so the paper was not directly
read.

### [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](https://arxiv.org/abs/2605.01160) — Sabry E. Farrag (University of East London; arXiv, 2026-05)
A synthesis rather than new primary data — a multivocal literature review of 67 sources (2022-2026)
— and worth citing for what it names rather than what it measures: the **Productivity-Reliability
Paradox (PRP)**, the same contradiction several entries on this page already document piecemeal
(METR's 19% slowdown above, the Microsoft rollout study's +24% above, Faros AI's telemetry) folded
into one formal claim that it is a systematic phenomenon, not a fluke of any one study, arising from
non-deterministic code generators paired with insufficient specification discipline. Its own headline
telemetry citation — 10,000+ developers, 98% more pull requests merged, PR review time up 91%, flat
delivery metrics — is Faros AI's *earlier* 2025 dataset (1,255 teams), a smaller predecessor to the
22,000-developer "Acceleration Whiplash" report this page already cites, not a new measurement. What
is new here is the **AI-Augmented Methodology Taxonomy (AAMT)**, classifying six established
methodologies (TDD, BDD, DDD, Agile, Waterfall, DevOps) across three tiers of AI integration
(Passive/Active/Autonomous) to isolate which methodological dimension a given tier of AI adoption
actually stresses, and the **Specification Governance Model (SGM)** — a Transaction-Cost-Economics
argument that treats a specification as the artifact that lowers the coordination cost non-deterministic
generation otherwise imposes. Directly on point for the spec-driven-development cluster this repo
already maps (`8090-software-factory-sdlc.md`'s PRD/Blueprints stages, `aws-ai-dlc.md`'s Inception
phase, the Lahiri "intent gap" paper above): all three now converge on treating the spec as a
governance artifact rather than documentation, from three independent angles. Confirmed via multiple
independently-worded search summaries agreeing on the author, venue, and the PRP/AAMT/SGM structure —
this pass's sandbox blocked `arxiv.org` outright (`EGRESS_BLOCKED`), so the paper itself was not
directly read.

### [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) — Anthropic Engineering (2026-04-23)
Anthropic's own engineering postmortem tracing six weeks of user reports that Claude Code had
gotten worse (2026-03-04 to 2026-04-20) to three independent harness/product-layer changes rather
than a model regression: (1) 2026-03-04, the default reasoning effort quietly dropped from high to
medium to cut thinking latency and usage-limit pressure — Anthropic's own ablations found this cost
roughly 3% quality on both Opus 4.6 and 4.7; (2) 2026-03-26, a caching optimization meant to clear
thinking-block context only from sessions idle over an hour instead cleared it on every turn for the
rest of any session; (3) an overly aggressive system-prompt verbosity limit, costing a further ~3%.
All three shipped independently, overlapped for weeks before anyone connected them, and were fixed
by 2026-04-20 (v2.1.116); Anthropic reset usage limits for every subscriber as compensation. Worth
reading as the concrete case this page's harness-engineering cluster (Hashimoto/Fowler/Anthropic/
OpenAI above) has otherwise only argued in the abstract: **Agent = Model + Harness**, demonstrated
here by its own negative case — three changes invisible to any model eval degraded real usage for
six weeks while the underlying model was untouched, and the fix was the harness-engineering
discipline those posts already prescribe (find the environmental regression, encode a check against
its recurrence) rather than anything about the model. Confirmed via multiple independent write-ups
(VentureBeat, InfoQ, GIGAZINE) quoting the same official Anthropic language, dates, and version
number — this pass's sandbox blocked `anthropic.com` outright (`EGRESS_BLOCKED`), so the postmortem
itself was not directly read.

### [Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — Anthropic (2026-02)
Anthropic's own measured data on the autonomy-ladder topic this page's Zakariasson, Reyes, Osmani,
and `bushido-ai-dlc-2026.md` entries have so far only theorized: an analysis of millions of Claude
Code and API tool calls, each scored by Claude itself for risk (1-10) and autonomy (1-10). Roughly
73% of tool calls show a human in the loop and only 0.8% appear irreversible; software engineering
alone accounts for roughly half of all tool calls on the public API. The sharper finding is
behavioral rather than static: auto-approval rises from ~20% of turns for users under 50 sessions to
over 40% by ~750 sessions, while the interrupt rate rises *alongside* it (roughly 5% → 9%) rather
than falling — read together, that is not less oversight but a shift from approving each action to
monitoring a stream and intervening selectively. Turn duration at the 99.9th percentile nearly
doubled in three months studied (Oct 2025-Jan 2026), from under 25 minutes to over 45. Worth reading
as this page's first autonomy entry grounded in measured usage rather than a proposed framework.
Confirmed via multiple independent write-ups (Latent Space's AINews, Cosmic JS, AgentMarketCap,
the-decoder.com) converging on the same figures — this pass's sandbox blocked `anthropic.com`
outright (`EGRESS_BLOCKED`), so the post itself was not directly read.

### [Agentic coding and persistent returns to expertise](https://www.anthropic.com/research/claude-code-expertise) — Anthropic (2026-06-16)
A companion field study to the autonomy post above, at similar scale: roughly 400,000 Claude Code
sessions from roughly 235,000 users, October 2025-April 2026. Its central finding complicates the
Shen & Tamkin skill-formation RCT elsewhere on this page from the opposite direction — that study
found passive delegation costs comprehension; this one finds what predicts *success* in the first
place is domain expertise in the problem, not coding proficiency. Every one of the ten largest
occupation groups succeeds at nearly the software-engineer rate (engineers verified 34%; every group
lands within seven points), expert-rated sessions succeed 28-33% of the time against 15% for novice
sessions, and the gap narrows further between experts and intermediates — proficiency, not mastery,
is most of what the tool rewards. The division of labor holds throughout: people decide what to
build, the agent decides how, and expert users trigger roughly 12 Claude actions per prompt against
5 for novices. Over the seven-month window the share of sessions spent debugging fell by roughly
half as usage shifted toward end-to-end agentic work (deploy, run, analyze data). Worth reading
alongside Shen & Tamkin's 52-developer RCT as a field-scale complement rather than a duplicate: a
different question (what drives success, not what it costs), converging on the same answer that
engagement with the problem — not raw tool skill — is what separates good outcomes from bad ones.
Confirmed via multiple independent write-ups (TIGZIG, digitalapplied.com, techjacksolutions.com, AI
Weekly) converging on the same session/user counts and percentages — same `anthropic.com` egress
block as the entry above, so the post itself was not directly read.

### [Spec-Driven Development for Agentic Software Engineering: Harnessing Human-Agent Teamwork](https://arxiv.org/abs/2609.00252) — Jessica Díaz, Joaquín Gayoso, Andrea Cimminio, Jorge Pérez (Universidad Politécnica de Madrid; arXiv, 2026-08-31)
Names the same productivity paradox this page already documents piecemeal (Faros AI, the Microsoft
rollout study, CodeRabbit, "Debt Behind the AI Boom", Farrag's PRP synthesis above) from the
spec-driven-development side: as individual productivity rises under agentic delegation, team
throughput, review capacity, and stability degrade because team-scale engineering discipline gets
neglected. Its contribution is conceptual rather than measured — a gray-literature synthesis, by the
paper's own account, since peer-reviewed evidence here is still thin — but it is the first entry on
this page to explicitly frame Spec-Driven Development itself *as* the harness: the technical and
methodological mechanism through which a team governs agent behavior at scale, rather than a
documentation practice bolted onto the workflow after the fact. That framing bridges two clusters
this page tracks separately — the spec-as-governance-artifact reading (`8090-software-factory-sdlc.md`'s
PRD/Blueprints stages, `aws-ai-dlc.md`'s Inception phase, Lahiri's intent-gap paper, Farrag's PRP/SGM
synthesis above) and the harness-engineering reading (Hashimoto/Fowler/Anthropic/OpenAI above,
plus the Anthropic postmortem added this pass) — treating them as one discipline rather than two.
Confirmed via multiple independent search summaries (the arXiv abstract page and its HTML rendering)
agreeing on the authors, affiliation, and framing — this pass's sandbox blocked `arxiv.org` outright
(`EGRESS_BLOCKED`), so the paper itself was not directly read.

---

*Suggest additions or fixes via PR. Keep entries developer-focused, verify links
resolve before adding, and prefer a stable channel/site link over a video that may
be taken down.*
