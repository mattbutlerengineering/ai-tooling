# Evaluation: ponytail

**Repo:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
**Stars:** 39,695 | **Last updated:** 2026-06-19 (pushed; created 2026-06-12) | **License:** MIT
**Dev loop stage:** Implement (a behavioral skill that gates *how much* code the agent writes before it writes it); touches Review (the `ponytail-audit` / `ponytail-debt` skills flag over-build after the fact)
**Layer:** Process / Tooling (a behavioral skill distributed for 14 agents, with two small Node.js lifecycle hooks for always-on activation)

---

## What it does

The catalog one-liner: "Makes AI agents think like the laziest senior dev — write minimum code, avoid overengineering." It installs a single behavioral rule (the lazy-senior-dev persona) plus a handful of companion skills (`ponytail`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-review`, `ponytail-help`) across an unusually broad set of agents — Claude Code, Codex, Cursor, Cline, Kiro, Windsurf, OpenCode, OpenClaw, Copilot, and more (each gets its own rules/skill file in the tree).

The mechanism is a decision ladder the agent runs *before* writing code (verbatim from `.agents/rules/ponytail.md`):

```
1. Does this need to exist?   → no: skip it (YAGNI)
2. Stdlib does it?            → use it
3. Native platform feature?   → use it
4. Installed dependency?      → use it
5. One line?                  → one line
6. Only then: the minimum that works
```

The discipline is "lazy, not negligent": the rule explicitly carves out input validation at trust boundaries, data-loss-preventing error handling, security, and accessibility as *never* on the chopping block — and requires that non-trivial logic leave behind one runnable check (an assert-based self-check or one small test file). Intentional simplifications get a `ponytail:` comment that names the ceiling and the upgrade path (e.g. "global lock", "O(n²) scan"). The canonical example: asked for a date picker, a bare agent installs flatpickr and writes a wrapper; ponytail emits `<input type="date">`. Two tiny Node.js hooks provide always-on activation and a statusline indicator; the skills still work without `node`, the hook just stays quiet.

## How we tested it

**Source-grounded inspection — not installed, not run.** The skill was not installed, no agent session was run under it, and the benchmark was not reproduced, so every number below is the author's self-reported figure from the README, not anything I measured. The benchmark methodology is unusually well-documented for this category and worth reading directly: `benchmarks/results/2026-06-18-agentic.md`.

```bash
gh api repos/DietrichGebert/ponytail --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,license:.license.spdx_id}'
gh api repos/DietrichGebert/ponytail/readme --jq '.content' | base64 -d
gh api repos/DietrichGebert/ponytail/contents/.agents/rules/ponytail.md --jq '.content' | base64 -d   # the actual rule
gh api "repos/DietrichGebert/ponytail/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/DietrichGebert/ponytail/commits --jq 'length'      # 30 (capped page)
gh api repos/DietrichGebert/ponytail/releases --jq 'length'     # 9
gh api repos/DietrichGebert/ponytail/contributors --jq '[.[].login]'  # 27 contributors
```

## What worked

- **It targets the right failure mode.** Overbuild — speculative abstraction, unrequested dependencies, boilerplate — is one of the most consistent LLM coding pathologies. A pre-write decision ladder that says "stdlib > native > installed dep > one line > minimum" is a precise, well-aimed intervention, not a vibe.
- **The benchmark is honest and self-correcting.** The README *revised its own headline down* (from a flashy "80-94% less code" single-shot figure to a defensible "-54% mean" agentic figure) after issue #126 pointed out the original baseline was padded by conversational prose. It measures against a fair agentic baseline (headless Claude Code editing a real FastAPI+React repo, n=4, Haiku 4.5) and publishes per-task tables. That intellectual honesty is rare in this category and raises trust.
- **Safety is a first-class constraint, and the benchmark proves it matters.** The benchmark's separate adversarial "safe" tier shows ponytail keeps 100% of safety guards while a naive "YAGNI + one-liners" prompt drops to 95%. The skill is designed so "lazy" cannot mean "skip the validation."
- **`ponytail:` comments make shortcuts auditable.** Naming the ceiling and upgrade path on each intentional simplification is exactly the discipline that keeps "minimal" from quietly becoming "fragile."
- **Exceptional reach and traction.** 39.7K stars, 27 contributors, distributed for 14 agents from one source of truth, MIT. Companion `ponytail-audit`/`ponytail-debt` skills extend it into the Review stage (find existing over-build / debt), not just generation.

## What didn't work or surprised us

- **It is a prompt, not an enforcer — results depend on the driving model.** There is no code that *prevents* overbuild; the skill is a rule the model may or may not follow. The README is candid that a terse reasoning model spending thinking tokens deliberating the ladder can go the *other way* (it reports GPT-5.5 getting more expensive, not less).
- **Self-reported, single-repo benchmark.** Even the corrected numbers come from one repo, one model (Haiku 4.5), n=4. The honesty is commendable but the sample is narrow; the gains are biggest on contrived "overbuild traps" (date/color pickers) and "near zero on code that is already minimal" — so real-world savings vary widely by task mix.
- **Lazy can fight thorough.** A rule pushing "fewest files, deletion over addition" can collide with this catalog's own coding-style guidance ("many small files > few large files") and with intentionally explicit code. The validation/security carve-outs reduce but do not eliminate the risk of an agent under-building where the team wanted clarity.
- **Two lifecycle hooks are real surface.** Always-on activation runs Node.js hooks on every prompt; they're small and degrade gracefully, but they're executable code in your agent's hot path, and the Codex flow asks you to "review and trust" them.
- **Crowded persona-skill space.** This sits beside caveman (terse output) and andrej-karpathy-skills (pitfall-derived rules); the differentiator is the *pre-write decision ladder* and the benchmark, not the idea of "tell the agent to write less."

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Maintainability | + | Less code, fewer dependencies, fewer files, deletion-over-addition — directly fewer lines to maintain. `ponytail:` comments document intentional shortcuts and their upgrade paths. Risk: can under-build where explicit code was wanted. |
| Cost Efficiency | + / neutral | Self-reported -20% cost / -22% tokens vs. a fair agentic baseline on Haiku 4.5 — but the README warns a deliberating reasoning model (GPT-5.5) can spend *more*; depends on the model. |
| Speed | + / neutral | -27% wall time self-reported (less code to generate and review). Same model-dependent caveat. |
| Safety | + | Validation/security/accessibility/data-loss handling are explicitly never cut, and the adversarial benchmark tier shows ponytail holds 100% safety where a naive one-liner prompt drops a guard. |
| Correctness | neutral / + | Requiring one runnable check behind non-trivial logic nudges toward verified-minimal rather than golfed code; but it adds no test infrastructure and correctness still rests on the model following the rule. |

## Verdict

**CONDITIONAL** — adopt when your agent's habitual failure mode is *overbuild*: speculative abstractions, unrequested dependencies, wrapper components for things the platform already does. Its self-correcting, adversarially-safety-tested benchmark and explicit non-negligence carve-outs make it the most credible of the "write-less-code" persona skills. Skip or down-weight it on a terse reasoning model (the author's own data shows it can backfire on token cost there), and watch that "fewest files" doesn't fight a codebase that genuinely wants explicit, well-separated modules.

Compared to neighbors: **caveman** compresses the agent's *prose output* for token savings (a communication-style control) — ponytail's own benchmark uses caveman as the terse-prose baseline and beats it on every code metric, because ponytail changes *what gets built*, not just how it's described. **andrej-karpathy-skills** is a static CLAUDE.md of pitfall-derived guidelines; ponytail is narrower and sharper — a single pre-write decision ladder with measurement behind it rather than a broad rule list. Of the three, ponytail is the one with a published, peer-challenged-and-corrected benchmark, which is why it rates a confident CONDITIONAL rather than a speculative one.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ponytail](https://github.com/DietrichGebert/ponytail) | skill | "Lazy senior dev" pre-write decision ladder (YAGNI → stdlib → native → installed dep → one line → minimum) with explicit safety carve-outs; benchmarked, 14-agent distribution | Agent overengineers — speculative abstractions, unrequested dependencies, boilerplate — instead of writing the minimum code that works | andrej-karpathy-skills, caveman |
