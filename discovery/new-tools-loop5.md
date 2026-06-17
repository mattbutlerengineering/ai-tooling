# New Tools Evaluation (Loop 5)

High-star catalog tools assessed for WORKFLOW.md inclusion.

## andrej-karpathy-skills
**Repo:** [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
**Stars:** 176,263 | **Last updated:** 2026-04-20 | **Forks:** 18,001
**What it does:** A single CLAUDE.md file distilling Karpathy's observations on LLM coding failure modes into four behavioral guardrails: Think Before Coding (surface assumptions), Simplicity First (no speculative features, YAGNI), Surgical Changes (touch only what's relevant), and Goal-Driven Execution (verifiable success criteria before starting).
**Current workflow alternative:** mattpocock/skills (L2) provides engineering conventions. agent-skills (L3) adds lifecycle structure. The user's own `implementation-discipline.md` already encodes all four Karpathy principles almost verbatim.
**Key difference:** Framed around LLM failure mode awareness — names the specific ways models go wrong (silent assumptions, overengineering, scope creep) rather than engineering methodology per se.

**Verdict:** SKIP
**Justification:** The 176K stars reflect the value of the ideas, not a gap in the current workflow. The user's global `implementation-discipline.md` already implements every Karpathy principle at the same or greater fidelity. mattpocock/skills (L2) and agent-skills (L3) cover the engineering methodology side. For users who don't already have these rules encoded, installing this skill is a great starting point — but it doesn't earn a recommended workflow slot because the rules should already be in your CLAUDE.md by L2.

---

## autoresearch
**Repo:** [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
**Stars:** 87,032 | **Last updated:** 2026-03-26 | **Forks:** 12,605
**What it does:** Gives an AI agent a single-GPU LLM training setup and lets it experiment autonomously overnight. The agent edits train.py (model architecture, optimizer, hyperparameters), runs 5-minute training bursts, checks validation loss, keeps improvements, and repeats.
**Current workflow alternative:** Nothing — the workflow is about software development, not ML research.
**Key difference:** This is a self-modifying ML research harness, not a coding assistant. The human programs `program.md` (instructions for the agent) rather than the Python source files.

**Verdict:** SKIP
**Justification:** Solves a fundamentally different problem than AI-assisted software development. Its massive star count reflects viral interest in autonomous AI research agents, not broad utility for everyday dev workflows. Teams doing active LLM pretraining/fine-tuning might track it as a reference, but it earns no slot in an L2-L6 coding workflow.

---

## google/skills
**Repo:** [google/skills](https://github.com/google/skills)
**Stars:** 13,734 | **Last updated:** 2026-06-13 | **Forks:** 1,036
**What it does:** First-party, Google-maintained skill pack targeting their ecosystem — Gemini API, BigQuery, Cloud SQL, AlloyDB, Cloud Run, GKE, Firebase, and Well-Architected Framework guidance. Installed via `npx skills add google/skills`.
**Current workflow alternative:** mattpocock/skills (L2) and agent-skills (L3) cover general engineering. Neither addresses Google Cloud service integrations.
**Key difference:** Operational skills for invoking and managing live Google Cloud services from within Claude agents. Domain-specific, not general-purpose.

**Verdict:** CONDITIONAL at L3 for Google Cloud teams
**Justification:** High-signal, well-supported (13.7K stars, updated 2 days ago), but narrowly scoped to the Google ecosystem. Developers not using GCP, Firebase, or Gemini get no value. Should be called out as a required add-on for Google Cloud shops alongside a note about equivalent packs for AWS/Azure.

---

## impeccable
**Repo:** [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
**Stars:** 38,680 | **Last updated:** 2026-06-16 | **Forks:** 2,135
**What it does:** Multi-platform skill and CLI that gives AI coding agents a design language and command vocabulary for building distinctive UIs. Provides 23 specialized commands (`/impeccable craft`, `audit`, `animate`, `polish`, etc.), runs 41 deterministic anti-pattern detectors without needing an API key, and captures brand/product context during init.
**Current workflow alternative:** ui-ux-pro-max is in the catalog but not recommended at any ACMM level.
**Key difference:** Ships a real CLI with deterministic static analysis (41 rules, no LLM required), multi-platform install, and persistent brand context docs. Functions as a design linter, not just advisory prompting. At 38K stars, dramatically higher adoption than ui-ux-pro-max.

**Verdict:** CONDITIONAL at L3 for UI-building teams
**Justification:** Earns a slot for any team building user-facing UIs — the deterministic CLI rules catch real design anti-patterns before they ship, which is a concrete quality gate. Irrelevant for backend services, CLIs, or data pipelines. Should replace or subsume ui-ux-pro-max in the catalog given stronger tooling and dramatically higher adoption.
