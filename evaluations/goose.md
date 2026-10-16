# Evaluation: goose

**Repo:** [aaif-goose/goose](https://github.com/aaif-goose/goose) (moved from block/goose to Linux Foundation AAIF)
**Stars:** 52,278 | **Last updated:** 2026-08-05 | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A general-purpose open-source AI agent — desktop app (macOS/Linux/Windows), full CLI, and embeddable REST API — built in Rust for performance and portability. Works with 15+ providers (Anthropic, OpenAI, Google, Ollama, OpenRouter, Azure, Bedrock, and more) via API keys or existing subscriptions through ACP (Agentic Context Protocol). Connects to 70+ extensions via MCP. Designed as a standalone agent runtime, not a Claude Code enhancement — you use goose *instead of* Claude Code, not alongside it.

The architecture is clean: a `goosed` server process exposes a REST API that any frontend (CLI, Electron desktop, custom web/mobile) can consume. Extensions are MCP servers. Providers are pluggable via a trait system. "Recipes" (YAML-based task definitions) enable guided workflows and multi-step automation. Custom distributions ("white labelling") let organizations ship preconfigured goose variants with their own providers, extensions, and branding.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed the v1.54.0 Linux CLI from the release tarball (`goose-x86_64-unknown-linux-gnu.tar.bz2`, `HOME` pointed at a scratch dir) and ran its credential-free surface: `--version`, `info`, `doctor`, `skills list`, `recipe validate` against a nine-file fixture. The sandbox has no model credentials, so the agent loop itself (`session`, `run`) stops at goose's own "No provider configured" gate.

```text
$ goose --version            -> 1.54.0   (binary 307,756,800 bytes; tarball 80,909,320 bytes; 0.011s wall)
$ goose run -i -  (stdin "say hi")
  error: No provider configured. Run 'goose configure' first.
$ goose doctor
  error: No provider configured. Run 'goose configure' first.
$ goose skills list
  goose-doc-guide | builtin://skills/goose-doc-guide   (817 content tokens)
  web-search      | builtin://skills/web-search        (546 content tokens)

fixture: 1 valid recipe + 8 single-defect recipes; baseline = PyYAML safe_load, treatment = goose recipe validate
file                              pyyaml  goose_rc  goose message
r0_valid                          ok      0         recipe file is valid
r1_yaml_syntax (bad indent)       ERR     1         parameters[0]: missing field `input_type`
r2_missing_title                  ok      1         missing field `title`
r3_no_instructions_or_prompt      ok      1         must specify at least one of `instructions` or `prompt`
r4_undeclared_param               ok      1         Missing definitions for parameters ...: path
r5_unused_param                   ok      1         Unnecessary parameter definitions: path
r6_bad_input_type (banana)        ok      1         unknown variant `banana`, expected string|number|boolean|date|file|select
r7_optional_no_default            ok      1         Optional parameters missing default values ...: path
r8_bad_template ({{ path)         ok      1         syntax error: unexpected identifier, expected end of variable block (in recipe:6)

5 x `goose recipe validate` on the valid recipe: 0.058s total
```

## Test design

- **Task/corpus:** one valid goose recipe (title, description, instructions, prompt, one required string parameter `path` used as `{{ path }}`) plus eight copies each carrying exactly one planted defect: indentation error, missing `title`, neither `instructions` nor `prompt`, template variable with no declared parameter, declared parameter never used, `input_type: banana`, optional parameter with no default, unclosed `{{`.
- **Baseline:** Python `yaml.safe_load`, the check a team has with no goose installed: parseable or not.
- **Metric:** defects flagged out of 8, false positives on the 1 valid file, process exit code.
- **Reproduce:** download the release tarball, extract, set `HOME` to a scratch directory, run `goose recipe validate <file>` over the fixture and compare with `python3 -c "import yaml; yaml.safe_load(open(f))"`; the nine files are described above and are each under 12 lines.

Result: baseline flags 1 of 8 (the indentation error); `goose recipe validate` flags 8 of 8 with 0 false positives on the valid file, and exits 1 on every invalid file, so it works as a CI gate. n=1 per defect class, a narrow slice of the product (recipe schema checking only), and the baseline is deliberately minimal.

## What worked

- **`recipe validate` is a real structural and semantic check.** It catches missing fields, bad enums, undeclared and unused template parameters, and malformed template syntax, none of which a YAML parser sees (8/8 vs 1/8 on the fixture).
- **Exit codes are right.** 0 for the valid recipe, 1 for all eight invalid ones and for a missing file, so it drops straight into a pre-commit or CI step.
- **Single static binary, instant start.** 0.011s for `--version`; no Node or Python runtime needed.
- **Fails closed with a clear message when unconfigured.** `run` and `doctor` stop at one actionable line rather than a stack trace.
- **Built-in skills surface.** `goose skills list` shows two builtin skills with token costs per skill, which makes context overhead visible.

## What didn't work or surprised us

- **The agent loop was not exercised.** No provider credentials exist here, so the claims in the earlier architecture review (15+ providers, ACP, recipes driving subagents, 70+ extensions) are still the project's own description. Nothing measured says whether goose completes coding tasks better or worse than Claude Code or aider.
- **Error output carries a Rust backtrace.** Each validation failure prints a ten-plus-line `Stack backtrace` after the one-line message, which is noise in CI logs.
- **The indentation-error case got a misleading message.** PyYAML rejects the file; goose reported `missing field input_type`, which describes a symptom of how its parser read the misindented list, not the actual cause.
- **Large binary.** 307 MB unpacked (81 MB download), against a one-binary pitch.
- **`goose mcp developer` is not a valid server name** in 1.54.0; the bundled server names are not discoverable from `--help`, which only prints `<SERVER>`.
- **Replaces Claude Code entirely.** It is a different runtime with its own config and extension model (`.goosehints`, recipes), so it is a platform choice rather than an add-on.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Recipe validation measured 8/8 defects vs 1/8 for a YAML parse; the agent's own output quality is unmeasured here |
| Speed | + | 0.011s startup, 5 validations in 0.058s; task speed unmeasured |
| Maintainability | + | Validator rejects unused and undeclared parameters, which keeps recipes tidy; clean crate layout from the earlier review |
| Safety | neutral | Fails closed without a provider; sandboxing and permission model of the agent loop unmeasured |
| Cost Efficiency | neutral | Per-skill token costs are shown by `skills list`; model spend untested |
| Verifiability | + | `recipe validate` gives a mechanical pass/fail with exit code on workflow definitions, so a human can confirm a recipe is well-formed without running it |

## Verdict

**discovery-log — tentative read** — the credential-free surface is solid (recipe validation 8/8 vs 1/8 for a YAML parse, correct exit codes, instant start), but goose's value is the agent loop, which needs a model provider this run did not have, so there is no measured basis to promote or eliminate it. A real read needs a provider key and a coding-task A/B against Claude Code or aider.

Use goose when you need a model-agnostic agent platform (multi-provider support is its primary differentiator), when you are building a custom agent distribution for an organization, or when you want to avoid Claude Code's model lock-in. Choose Claude Code when you want the deepest ecosystem (skills, plugins, marketplace), structured development methodology (superpowers, agent-skills) and Anthropic-optimized performance. The two don't compose — it's a platform choice.

## Triage note

Cites claude-squad (STACK ADOPT) in Overlaps with, but the eval's own verdict already draws the line: this is a platform choice (model-agnostic agent runtime) versus claude-squad's parallel-session TUI, not a redundant re-implementation. Apache-2.0, actively pushed. Run on 2026-10-16 to RUN level; the agent loop remains the open measurement.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [goose](https://github.com/aaif-goose/goose) | platform | Extensible AI agent that can install, execute, edit, and test with any LLM | Want a model-agnostic agent platform with plugin extensibility | OpenHands, claude-squad |
