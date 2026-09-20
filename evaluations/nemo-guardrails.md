# Evaluation: NeMo-Guardrails

**Repo:** [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
**Stars:** ~6,500 | **Last updated:** 2026-06-19 | **License:** Apache-2.0 (repo SPDX returns NOASSERTION)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (runtime guardrails / Outer Loop)
**Layer:** Infrastructure

---

## What it does

An open-source toolkit from NVIDIA for adding **programmable guardrails** ("rails") to LLM-based conversational applications. Rails are specific ways of controlling model behavior — and they sit as a layer between the user and the LLM.

Per the README and the accompanying paper (arXiv:2310.10501), rails can: keep the model on allowed topics (e.g. not talking about politics), respond in predefined ways to specific requests, follow a predefined dialog path, enforce a language/style, extract structured data, and block jailbreaks or unsafe output. You define rails declaratively (Colang config + policies) and NeMo intercepts inputs and outputs to enforce them at runtime. It integrates with common LLM stacks and supports Python 3.10–3.13.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the documented rail types, and the arXiv paper reference. Confirmed the declarative "rails between user and model" architecture, the categories of control (topic/jailbreak/dialog-path/format/structured-extraction), and the runtime interception model. License resolves to NOASSERTION via the API but is Apache-2.0 per the project. Not wired into a live app, so condition-gated.

```bash
gh api repos/NVIDIA-NeMo/Guardrails --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/NVIDIA-NeMo/Guardrails/readme --jq '.content' | base64 -d
```

## What worked

- **Declarative, programmable control.** Defining rails as config rather than scattering ad-hoc checks gives a coherent, auditable policy layer between user and model.
- **Broad rail types.** Topic limits, jailbreak blocking, dialog flows, output format, and structured extraction cover most conversational-safety needs in one toolkit.
- **Credible + documented.** NVIDIA-maintained and paper-backed, with a real evaluation — a serious option, not a prototype.

## What didn't work or surprised us

- **Conversational-app focus.** Strongest for chatbot/dialog systems; mapping rails onto a coding-agent harness is less of a direct fit.
- **Latency + complexity.** Rails add interception steps (some rails call an LLM), and Colang/config has a learning curve.
- **Overlaps superagent/Portkey guardrails.** Several tools now offer runtime guardrails; NeMo's edge is the programmable dialog-flow depth and NVIDIA pedigree.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Output rails (format/fact-check/structured) reduce malformed/unsafe responses |
| Speed | - | Interception and LLM-based rails add latency |
| Maintainability | + | Centralized, declarative policy beats scattered checks |
| Safety | + | Topic/jailbreak/unsafe-output rails at runtime |
| Cost Efficiency | neutral | OSS; some rails add extra model calls |

## Verdict

**discovery-log — tentative read**

Adopt when you ship an LLM-backed conversational application and need a programmable, auditable runtime guardrail layer (topics, jailbreaks, dialog flow, output format). Weigh added latency and Colang complexity. For PII specifically use presidio; for agent-tool-call safety + red-teaming, superagent; NeMo's strength is conversational dialog control.

## Triage note

Left at `discovery-log`. Programmable runtime rails for conversational LLM applications — topics,
jailbreaks, dialog flow, output format — with Colang as the policy language. NVIDIA behind it, ★6.7K,
pushed this week.

The licence needs a note, not a disposition. `repo-metadata.json` records **`NOASSERTION`**, which per
CLAUDE.md means GitHub could not parse the LICENSE file and never that a grant is absent. NVIDIA ships
this under Apache-2.0; `Memori` in the previous slice was the same misread. A bulk lane must not guess
either way, and the check is cheap for whoever picks this up.

Not disposed as redundant, because the safety cluster is genuinely differentiated and the eval maps it
cleanly: NeMo for conversational dialog control, `presidio` for PII specifically, `superagent` for
agent-tool-call safety plus red-teaming, `garak` for adversarial probing. Four tools, four failure
modes. Composing best-of-breed versus taking a bundle is the real decision, and `superagent`'s eval
frames it the same way from the other side.

Weigh at promotion: added latency, and Colang is a language your team has to learn.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

**Re-triaged 2026-09-04 by the P3 backlog band (daily discovery pass):** no change — still a live, permissively-licensed guardrails toolkit with genuine overlaps (`superagent`, `presidio`, `garak`) rather than a clean incumbent to be redundant with; left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [NeMo-Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | tool | Programmable guardrails for LLM apps (Apache-2.0, ★6.5K, by NVIDIA) — declarative "rails" between user and model controlling topics, jailbreaks, dialog paths, output format, and tool-use; arXiv-backed | "Prompt + model" apps go off-topic, get jailbroken, or emit unsafe output; want declarative, programmable runtime guardrails | superagent, presidio, garak, strands-agents (harness-sdk) |
