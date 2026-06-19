# Evaluation: ida-pro-mcp

**Repo:** [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp)
**Stars:** 9,501 | **Last updated:** 2026-06-06 (pushed; created 2025-03-25) | **License:** MIT
**Dev loop stage:** None of the standard inner/outer loop — this is **domain-specific tooling for reverse engineering / malware analysis**, not software-build work. It belongs to a security analyst's loop (triage a binary → decompile → annotate → report), which the AI-tooling dev loop doesn't model. In-scope only as a Security & Safety capability.
**Layer:** Tooling/Infrastructure — an MCP server (GUI plugin + headless `idalib-mcp` supervisor) that bridges an installed IDA Pro into any MCP client. Requires a licensed IDA Pro 8.3+ (IDA Free unsupported); maintained by mrexodia (x64dbg author).

---

## What it does

ida-pro-mcp exposes IDA Pro's analysis engine to an LLM over MCP so an agent can drive reverse engineering — "vibe reversing." It ships two transports: a **GUI plugin** (`ida-pro-mcp --install`, runs inside an open IDA session) and a **headless `idalib-mcp`** supervisor that opens binaries via Hex-Rays `idalib` with no GUI, keeping each database in its own persistent detached worker process (adopt-existing, idle-TTL self-exit, explicit `database` session IDs). It's distributed as a Claude Code plugin (`claude plugin install ida-pro-mcp@mrexodia`) and configures ~25 other MCP clients.

The tool surface is large and split by capability. **Read/query:** `decompile`, `disasm`, `xrefs_to`, `callees`, `list_funcs`, `imports`, `stack_frame`, plus MCP **Resources** (`ida://idb/metadata`, `ida://types`, `ida://struct/{name}`, `ida://cursor`). **Memory reads:** `get_bytes`, `get_int`, `get_string`, `get_global_value`. **Modification (mutates the IDB):** `set_comments`, `patch_asm`, `declare_type`, `define_func`, `define_code`, `undefine`, `add_bookmark`, `declare_stack`. **Debugger (hidden behind `?ext=dbg`):** `dbg_start`, `dbg_continue`, breakpoints, register reads, and crucially `dbg_read`/`dbg_write` — *live memory read/write of a debugged process*. The README is candid about LLM limits in RE (hallucinated base conversions — hence the `int_convert` tool — and poor performance on obfuscated/encrypted code) and supplies example prompts plus an `idapython` SKILL with bundled API docs.

## How we tested it

**Source-grounded inspection — not installed, not run.** No IDA Pro license was used, no binary was analyzed, no MCP server started, and the debugger extension was never enabled. "Vibe reversing" effectiveness on real malware is the author's demo claim (linked video + `mcp-reversing-dataset`), **not** something measured here. All findings come from repo metadata, README, the file tree, and the shipped capability/profile files.

```bash
gh api repos/mrexodia/ida-pro-mcp --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/mrexodia/ida-pro-mcp/readme --jq '.content' | base64 -d         # transports, full tool surface, dbg ext, prompts
gh api "repos/mrexodia/ida-pro-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # profiles/, skills/idapython, ida-plugin.json
gh api repos/mrexodia/ida-pro-mcp/contents/profiles/readonly.txt --jq '.content' | base64 -d  # curated no-mutation allowlist
gh api repos/mrexodia/ida-pro-mcp/commits --jq 'length'   # 30 (page-1 cap — active)
gh api repos/mrexodia/ida-pro-mcp/releases --jq 'length'  # 3 tagged releases
```

## What worked

- **Comprehensive, well-organized RE surface.** Decompile/disasm/xrefs/types/stack-frame coverage with paginated, filterable listings and MCP Resources for browsable state is a thorough mapping of IDA's API — far past a toy bridge.
- **Headless `idalib-mcp` is a serious piece of engineering.** A supervisor with per-database persistent workers, transparent adoption of already-open instances, explicit session IDs (no implicit "current database"), and idle-TTL self-exit is exactly the model you want for unattended/automated analysis pipelines.
- **Safety is designed in, not bolted on.** The repo ships **`profiles/readonly.txt`** (a curated allowlist of analysis-only tools — no rename/comment/type/patch) and **`profiles/triage.txt`**, loadable via `--profile`. The destructive debugger tools (`dbg_write`, process control) are **hidden by default** behind an explicit `?ext=dbg` query parameter. This is responsible default-deny design for a tool that can mutate state and run code.
- **Credible maintainer and real distribution.** Authored by mrexodia (x64dbg), `idalib` contributed by Willi Ballenthin (FLARE), Claude Code marketplace install, ~25 client configs, a bundled `idapython` skill with API docs, and a public reversing dataset for reproducing results.

## What didn't work or surprised us

- **Hard, expensive prerequisite.** Requires a licensed **IDA Pro 8.3+** (commercial; IDA Free explicitly unsupported) and Python 3.11+. This is not a tool a general developer can `npm install` and try — it gates the whole thing behind a niche, paid analyst environment.
- **Highest-reach Safety surface in this catalog's MCP entries.** When `?ext=dbg` is enabled, the agent can **start a process, set breakpoints, and read/write live process memory** (`dbg_write`), and `patch_asm` mutates the binary database. Pointing an LLM at malware *and* arming the debugger means an agent decision can execute/alter untrusted code — analysts must sandbox the host (VM, isolated network) themselves; the tool does not enforce containment.
- **LLM accuracy is the known weak point in RE.** The README itself warns LLMs hallucinate on base conversions and fail on obfuscated/encrypted/CFG-flattened code, recommending you de-obfuscate and resolve library code (Lumina/FLIRT) *before* involving the model. The agent is an assistant over a human-driven process, not an autonomous reverser.
- **Narrow audience.** Outside RE/malware/vulnerability-research teams, this has zero dev-loop relevance — it does not help write, review, or ship application code.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | For RE *analysis*, structured decompile/xref/type access + `int_convert` reduces the LLM's worst error modes; but the README documents persistent hallucination risk on obfuscated code, so outputs need human verification. Not applicable to general software correctness. |
| Speed | + | For an analyst, automating annotate/rename/comment/report across a binary is a large time saving over manual IDA work — within the RE domain only. |
| Maintainability | n/a | Operates on binaries/IDBs, not your source tree; no effect on a codebase's maintainability. |
| Safety | − (high reach) | Can mutate the IDB (`patch_asm`, `declare_type`) and, with `?ext=dbg`, control a debugger and read/write live process memory (`dbg_write`). Mitigated by default-hidden dbg tools and shipped read-only/triage profiles, but containment of the (often malicious) target is the operator's responsibility. |
| Cost Efficiency | neutral / − | No special token model; long decompiled functions and iterative annotation can be token-heavy on large binaries. |

## Verdict

**CONDITIONAL — adopt for reverse-engineering / malware-analysis work, with read-only or triage profiles by default and host sandboxing mandatory; out of scope for general development.** This is a well-engineered, credibly maintained RE bridge with genuinely thoughtful safety affordances (curated profiles, default-hidden debugger). Its limits are structural: it needs a paid IDA Pro license, it carries the highest host/process reach of any MCP server in this catalog when the debugger extension is on, and it only matters to security analysts. The right posture is `--profile profiles/readonly.txt` for analysis, enabling mutation/`?ext=dbg` only deliberately and only inside an isolated VM.

Compared to neighbors: **cve-mcp-server** and **pentest-ai** are *network/API-facing* security MCPs (vulnerability intel, offensive tooling) that touch remote services, not local binaries or a debugger; ida-pro-mcp is the opposite — deep *local* static/dynamic binary analysis with read/write reach into a target process. It is the most specialized and the most privileged of the security MCP entries: narrower audience than cve-mcp-server, sharper teeth than pentest-ai's remote probes. Within RE it is best-in-class; outside it, irrelevant.

## Catalog entry

**Target category: Security & Safety**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | MCP server | Bridges IDA Pro (GUI plugin + headless idalib) to any LLM/MCP client for AI-assisted reverse engineering — decompile, xrefs, annotate, types, patch, and an opt-in debugger; ships read-only/triage safety profiles | Reverse engineering and malware analysis in IDA is manual and tedious; lets an agent drive decompilation, annotation, and reporting over a binary | cve-mcp-server, pentest-ai (other security MCPs — but those are network/API-facing, not local binary/debugger analysis) |
