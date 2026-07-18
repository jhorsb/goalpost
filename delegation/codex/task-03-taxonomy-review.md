# Codex task 03 — `goalpost taxonomy-review` rendering

## Context (all you need)
Goalpost's normaliser writes an audit trail of every reason/recourse item it
mapped: `audits/<id>/normalised/<version>/<sut-id>/mapping_log.jsonl`, one
JSON object per line with fields `raw`, `normalised`, `cluster`,
`source` (`rule` | `llm` | `passthrough` | `passthrough_novel`), `all_hits`
(list of every cluster whose keywords matched). A human spot-checks the
LLM-made mappings before promoting them into the keyword taxonomy. Build the
CLI rendering for that review. This is rendering only — do not touch the
normaliser or the mapping-log format.

## Interface contract
New typer command in `src/goalpost/cli.py`:

```
goalpost taxonomy-review <audit_dir> [--rule-sample N]   # N default 20
```

- Recursively find every `mapping_log.jsonl` under `<audit_dir>/normalised/`;
  exit non-zero with a message containing "mapping_log" if none found.
- Print a review table (plain text/markdown, one row per item):
  ALL `llm`- and `passthrough_novel`-sourced mappings first, then a sample
  of at most `--rule-sample` `rule`-sourced rows (deterministic selection —
  e.g. first N sorted by normalised id; no randomness).
- Rows show: source, raw, normalised, cluster, and remaining `all_hits`
  beyond the first (multi-hit surfacing).
- Deduplicate identical (normalised, cluster, source) rows across files.

## Failing tests (already committed — your job is GREEN)
`tests/codex/test_task03_taxonomy_review.py` — run:
`uv run pytest -m codex tests/codex/test_task03_taxonomy_review.py`

## File-touch allowlist
- `src/goalpost/cli.py` — the new command + private helpers only. Do not
  modify existing commands, `_plan`, or `_run_live`.

## Constraints
- No new dependencies. No network in tests. Do not modify any test file.
- Read-only over the audit dir: this command must never write.

## Definition of done
- `uv run pytest -m codex tests/codex/test_task03_taxonomy_review.py` green
- `uv run pytest` (default suite) green
- Nothing else in the diff

## Branch
`codex/task-03-taxonomy-review`

## Return format
Short summary of approach + anything you could not satisfy and why.
