# Evaluation: claude-code-data-engineering-skills

**Repo:** [DataWithBaraa/claude-code-data-engineering-skills](https://github.com/DataWithBaraa/claude-code-data-engineering-skills)
**Stars:** 82 | **Last updated:** 2026-11-06 (pushed) | **License:** MIT
**Last verified:** 2026-11-07
**Last triaged:** 2026-11-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

16 Claude Code skills (MIT) for data engineers — profile a new source, investigate a
failed run, review a change, document the platform. Most end in a shareable page.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to check it
against the STACK incumbents it cites, not to support an ADOPT.

## Triage note

P2 challenger — cites STACK picks `agent-skills`, `documentation-and-adrs`, and
`mattpocock/skills` in "Overlaps with". Left at discovery-log rather than SKIPped:
none of the three cover data-engineering's own recurring tasks (dbt/Airflow/Dagster/
Spark/Snowflake/BigQuery/Databricks/Kafka/Iceberg-adjacent source profiling, failed-run
investigation, and pipeline docs) — they are general-purpose engineering skill packs,
not domain-specific ones. Not clearly dominated; left for a real eval.
