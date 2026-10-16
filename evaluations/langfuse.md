# Evaluation: langfuse

**Repo:** [langfuse/langfuse](https://github.com/langfuse/langfuse)
**Stars:** 32,532 | **Last updated:** 2026-08-05 | **License:** NOASSERTION (GitHub could not parse the LICENSE file; unresolved here)
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (outer loop: observability and evals)
**Layer:** Infrastructure

---

## What it does

Open source AI engineering platform: tracing/observability, evals, prompt management and datasets for LLM apps. The platform is a server (self-hosted or cloud); apps send traces to it through language SDKs. The Python SDK (v5) wraps functions with an `@observe` decorator and exports spans over OpenTelemetry (OTLP/HTTP) to `/api/public/otel/v1/traces` on the configured host.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed the Python SDK with `pip install langfuse` (resolved to 5.0.1), pointed it at a local capture server on 127.0.0.1 with dummy keys (no account, no real credentials), and ran `@observe`-decorated functions against a plain-function baseline. Only the client SDK ran; the Langfuse server and UI are covered under "What didn't work".

```
$ for i in 1 2 3 4: python run.py   # N=2000 calls of a 200-iteration sum-of-squares function
baseline 20.2ms  observed 979.6ms  per-call overhead 479.7us  N=2000
baseline 20.7ms  observed 975.4ms  per-call overhead 477.3us  N=2000
baseline 20.3ms  observed 951.2ms  per-call overhead 465.5us  N=2000
baseline 20.2ms  observed 928.6ms  per-call overhead 454.2us  N=2000
requests: 4 POSTs to /api/public/otel/v1/traces (115-127 KB each)
otlp bytes 494467 contains 'outer': True 'inner': True 'langfuse.observation.type': True 'generation': True
```

## Test design

- **Task/corpus:** a 200-iteration pure-Python function called 2,000 times, plain vs wrapped in `@observe()`; plus a nested pair (`outer` calling `inner` with `as_type="generation"`) to check that span names and observation types reach the wire. Fixture is the script below, fully disclosed.
- **Baseline:** the same function without the decorator, same process, run first.
- **Metric:** wall-clock for the loop (4 runs, both arms in each run) and substring checks on the captured OTLP payloads.
- **Reproduce:** `python3 -m venv v && v/bin/pip install langfuse && v/bin/python run.py`

```python
import os, threading, http.server, json, time, gzip, sys
reqs=[]
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers.get('content-length',0)); b=self.rfile.read(n)
        if self.headers.get('content-encoding')=='gzip': b=gzip.decompress(b)
        reqs.append((self.path,len(b),b)); self.send_response(200); self.send_header('content-type','application/json'); self.end_headers(); self.wfile.write(b'{}')
    do_GET=do_POST
    def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8765),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
os.environ.update(LANGFUSE_PUBLIC_KEY='pk-lf-dummy',LANGFUSE_SECRET_KEY='sk-lf-dummy',LANGFUSE_HOST='http://127.0.0.1:8765',LANGFUSE_BASE_URL='http://127.0.0.1:8765')
from langfuse import observe, get_client
def work(x): return sum(i*i for i in range(200))+x
@observe()
def work_t(x): return work(x)
N=2000
t=time.perf_counter()
for i in range(N): work(i)
base=time.perf_counter()-t
t=time.perf_counter()
for i in range(N): work_t(i)
treat=time.perf_counter()-t
@observe()
def outer(q):
    return inner(q)+1
@observe(as_type="generation")
def inner(q): return len(q)
outer("hello")
get_client().flush()
time.sleep(1)
print(f"baseline {base*1e3:.1f}ms  observed {treat*1e3:.1f}ms  per-call overhead {(treat-base)/N*1e6:.1f}us  N={N}")
print("requests:",[(p,l) for p,l,_ in reqs][:10], "total",len(reqs))
from collections import Counter
bodies=b"".join(b for p,l,b in reqs if 'otel' in p)
print("otlp bytes",len(bodies), "contains 'outer':", b'outer' in bodies, "'inner':", b'inner' in bodies, "'langfuse.observation.type':", b'langfuse.observation.type' in bodies, "'generation':", b'generation' in bodies)
```

### Test design — skills

Not applicable: langfuse is a platform with an SDK, not a skill or plugin.

## What worked

- Install is a single `pip install langfuse` and the decorator needs no code changes beyond `@observe()`.
- Nested calls produced spans for both `outer` and `inner`, with `generation` observation type carried in the OTLP attributes (`langfuse.observation.type` present in the captured bytes).
- Export is batched in the background: 2,000 spans went out in 4 POSTs, and `flush()` returned promptly against the local capture server.
- Dummy keys and a custom host are accepted by the client with no network call to a vendor, so the client can be pointed at a self-hosted instance.

## What didn't work or surprised us

- The per-call tracing overhead was large relative to a tiny function: about 455-480 µs per decorated call (20 ms to roughly 950 ms across 2,000 calls), consistent across all four runs. That is negligible beside an LLM call that takes hundreds of milliseconds, and heavy for hot inner loops; the fixture is deliberately a worst case.
- The server was not run: the sandbox has the Docker CLI (29.8.2) but no Docker daemon socket, and the platform self-host needs several backing services. No ingestion, UI, datasets, evals or prompt-management behaviour was observed. Everything above is the client side only.
- The upstream README could not be fetched in this session (the repo is outside the session's GitHub scope), so no claims are made from it.
- Licence is recorded as NOASSERTION by GitHub; the actual terms (the repo is known to carry mixed-licence directories) were not read here, which matters for a vendored-or-hosted decision.
- The catalog row cites `evalview` as an overlap; no head-to-head was attempted.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Spans and observation types arrive on the wire as expected; whether the server renders them correctly was not observed. |
| Speed | - | About 0.46 ms added per decorated call in a worst-case micro-loop; fine for LLM-bound calls, costly for hot paths. |
| Maintainability | neutral | One decorator, but a self-hosted server is a multi-service deployment to run. |
| Safety | neutral | Traces carry function inputs/outputs by default; sending them to a server needs a data-handling decision. Not tested. |
| Cost Efficiency | neutral | SDK is free; hosting or cloud cost was not assessed. |
| Verifiability | + | Traces make an agent's calls inspectable after the fact, which helps a human confirm behaviour; the UI half of that claim was not seen. |

## Verdict

**discovery-log — tentative read** — SDK-side RUN only: install, decorator tracing and OTLP export work, with ~0.46 ms/call overhead in a worst-case loop; the server, UI, evals and licence were not exercised, so no adoption read is possible without a Docker-capable host and a licence review.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [langfuse](https://github.com/langfuse/langfuse) | platform | Open source AI engineering: evals, observability, prompt management, datasets | Can't see what agents are doing, how well they perform, or where they fail | evalview |
