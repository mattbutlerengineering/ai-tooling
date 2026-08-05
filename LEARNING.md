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
still good; titles were left out rather than link to a guess).

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

### [State of AI vs. Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) — CodeRabbit
A measured comparison (not a vendor claim) of 470 real open-source pull requests
(320 AI-coauthored, 150 human-only): AI-generated code averaged 1.7x more issues
per PR than human-written code, with security vulnerabilities up to 2.74x higher
and logic/correctness issues 75% more common. The most concrete evidence found
this pass for why unreviewed AI output is the wrong default — it's a data point
for the Verifiability signal's premise, not a reason to distrust AI coding tools
outright; the gap is exactly what review process closes.

---

*Suggest additions or fixes via PR. Keep entries developer-focused, verify links
resolve before adding, and prefer a stable channel/site link over a video that may
be taken down.*
